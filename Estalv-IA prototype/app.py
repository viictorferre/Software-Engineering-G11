from __future__ import annotations

import html
import json
import os
from datetime import date
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from features.daily_spending_limit import calculate_daily_spending_limit

from estalvia_core import (
    CATEGORIES,
    build_recommendations,
    build_budget_alerts,    
    build_transactions_csv,
    create_demo_transactions,
    create_id,
    default_budgets,
    format_money,
    format_transaction_date,
    get_budget_snapshots,
    get_expense_by_category,
    get_month_transactions,
    get_saving_rate,
    get_totals,
    normalize_budgets,
    normalize_transactions,
    sorted_transactions,
    suggest_category,
    get_biggest_expense_of_month,
)


DATA_FILE = Path("data") / "estalvia_state.json"
HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "8000"))
 

STYLE = """
:root {
  --bg: #f6f8f7;
  --surface: #ffffff;
  --ink: #15231f;
  --muted: #64736e;
  --line: #dbe3dd;
  --green: #16745d;
  --green-dark: #0f503f;
  --blue: #286f9e;
  --red: #b33a3a;
  --yellow: #d59a25;
  --sidebar: #122822;
  --shadow: 0 14px 34px rgba(18, 40, 34, 0.09);
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  color: var(--ink);
  background: var(--bg);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
}

a {
  color: inherit;
  text-decoration: none;
}

button,
input,
select {
  font: inherit;
}

button {
  cursor: pointer;
}

.sidebar {
  min-height: 100vh;
  padding: 24px 18px;
  background: var(--sidebar);
  color: #f7fbf8;
  position: sticky;
  top: 0;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 30px;
}

.brand-mark {
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  color: #10211d;
  background: #97dfc3;
  border-radius: 8px;
  font-weight: 900;
}

.brand strong,
.brand span {
  display: block;
}

.brand span {
  color: #bdd0c7;
  font-size: 0.86rem;
  margin-top: 2px;
}

.nav {
  display: grid;
  gap: 8px;
}

.nav a {
  min-height: 44px;
  border: 1px solid transparent;
  border-radius: 8px;
  padding: 0 12px;
  color: #dce7e2;
  display: flex;
  align-items: center;
  gap: 10px;
}

.nav a span {
  width: 20px;
  text-align: center;
  color: #97dfc3;
}

.nav a:hover,
.nav a.active {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.14);
  color: #ffffff;
}

.app-shell {
  min-width: 0;
  padding: 28px;
}

.topbar,
.section-heading,
.panel-header,
.transaction-row,
.budget-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.topbar {
  margin-bottom: 26px;
}

.eyebrow {
  margin: 0 0 5px;
  color: var(--green);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0;
  text-transform: uppercase;
}

h1,
h2,
h3,
p {
  margin-top: 0;
}

h1 {
  margin-bottom: 0;
  font-size: clamp(2rem, 4vw, 3.2rem);
}

h2 {
  margin-bottom: 0;
  font-size: 1.55rem;
}

h3 {
  margin-bottom: 14px;
  font-size: 1.02rem;
}

.month-chip {
  flex: 0 0 auto;
  padding: 10px 14px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  color: var(--muted);
  font-weight: 700;
}

.section-heading {
  margin-bottom: 18px;
}

.actions-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.actions-row form {
  display: block;
}

.primary-button,
.secondary-button {
  min-height: 42px;
  border-radius: 8px;
  border: 0;
  padding: 0 16px;
  font-weight: 800;
}

.primary-button {
  background: var(--green);
  color: #ffffff;
}

.secondary-button {
  border: 1px solid var(--line);
  background: var(--surface);
  color: var(--green-dark);
}

.primary-button:hover {
  background: var(--green-dark);
}

.secondary-button:hover {
  background: #f1faf6;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}

.kpi,
.panel {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  box-shadow: var(--shadow);
}

.kpi {
  min-height: 126px;
  padding: 18px;
}

.kpi span {
  color: var(--muted);
  font-weight: 800;
  font-size: 0.82rem;
}

.kpi strong {
  display: block;
  margin-top: 12px;
  font-size: 1.75rem;
}

.insight-card {
  display: grid;
  gap: 10px;
  border-left: 4px solid var(--green);
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  box-shadow: var(--shadow);
}

.insight-card.warning {
  border-left-color: var(--yellow);
}

.insight-card.danger {
  border-left-color: var(--red);
}

.insight-card p {
  margin: 0;
  color: var(--muted);
  line-height: 1.5;
}

.insight-value {
  font-size: 1.45rem;
  font-weight: 900;
  color: var(--ink);
}


.panel {
  padding: 18px;
}

.panel-header {
  margin-bottom: 8px;
}

.panel-header h3 {
  margin-bottom: 0;
}

.category-bars,
.transaction-list,
.recommendation-list,
.budget-grid {
  display: grid;
  gap: 12px;
}

.cashflow-chart {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  min-height: 220px;
  align-items: end;
  padding-top: 10px;
}

.cashflow-item {
  display: grid;
  gap: 10px;
  text-align: center;
}

.cashflow-stage {
  height: 145px;
  border-bottom: 1px solid var(--line);
  display: flex;
  align-items: end;
  justify-content: center;
}

.cashflow-bar {
  width: 72%;
  min-height: 8px;
  border-radius: 8px 8px 0 0;
  background: var(--green);
}

.cashflow-bar.expense {
  background: var(--red);
}

.cashflow-bar.balance {
  background: var(--blue);
}

.cashflow-bar.negative {
  background: var(--red);
}

.cashflow-label {
  color: var(--muted);
  font-size: 0.82rem;
  font-weight: 900;
}

.cashflow-value {
  font-weight: 900;
}

.bar-row {
  display: grid;
  grid-template-columns: 110px minmax(0, 1fr) 90px;
  align-items: center;
  gap: 12px;
}

.bar-row span:first-child {
  color: var(--muted);
  font-weight: 800;
}

.bar-track {
  height: 12px;
  overflow: hidden;
  border-radius: 999px;
  background: #e4ebe7;
}

.bar-fill {
  height: 100%;
  border-radius: inherit;
  background: var(--green);
}

.bar-row strong {
  text-align: right;
}

.transaction-row {
  min-height: 64px;
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
}

.transaction-title {
  display: grid;
  gap: 4px;
}

.transaction-title strong {
  font-size: 0.96rem;
}

.transaction-title span {
  color: var(--muted);
  font-size: 0.84rem;
}

.amount {
  font-weight: 900;
  text-align: right;
}

.amount.income {
  color: var(--green);
}

.amount.expense {
  color: var(--red);
}

.compact .transaction-row:nth-child(n + 6) {
  display: none;
}

.form-panel {
  align-self: start;
}

form {
  display: grid;
  gap: 14px;
}

label {
  display: grid;
  gap: 7px;
  color: var(--muted);
  font-size: 0.84rem;
  font-weight: 800;
}

input,
select {
  width: 100%;
  min-height: 42px;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 0 12px;
  background: #ffffff;
  color: var(--ink);
}

input:focus,
select:focus,
button:focus-visible {
  outline: 3px solid rgba(22, 116, 93, 0.22);
  outline-offset: 2px;
}

.inline-form {
  align-items: end;
  display: grid;
  gap: 10px;
  grid-template-columns: minmax(0, 1fr) auto;
}

.budget-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.budget-card {
  padding: 18px;
}

.budget-meta {
  margin-bottom: 12px;
}

.budget-meta h3 {
  margin-bottom: 0;
}

.status-pill {
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 0.78rem;
  font-weight: 900;
  background: #e6f5ed;
  color: var(--green-dark);
}

.status-pill.warning {
  background: #fff2cf;
  color: #805600;
}

.status-pill.danger {
  background: #ffe1dc;
  color: var(--red);
}

.budget-numbers {
  display: flex;
  justify-content: space-between;
  color: var(--muted);
  font-weight: 800;
}

.progress-track {
  height: 12px;
  margin: 12px 0;
  border-radius: 999px;
  background: #e4ebe7;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: inherit;
  background: var(--green);
}

.progress-fill.warning {
  background: var(--yellow);
}

.progress-fill.danger {
  background: var(--red);
}

.recommendation {
  border-left: 5px solid var(--green);
}

.recommendation h3 {
  margin-bottom: 8px;
}

.recommendation p {
  margin-bottom: 0;
  color: var(--muted);
  line-height: 1.55;
}

.empty-state,
.alert {
  padding: 18px;
  border: 1px dashed var(--line);
  border-radius: 8px;
  color: var(--muted);
  background: rgba(255, 255, 255, 0.75);
}

.alert {
  border-color: #ffb4a8;
  color: var(--red);
  margin-bottom: 18px;
}

@media (max-width: 980px) {
  body {
    grid-template-columns: 1fr;
  }

  .sidebar {
    min-height: auto;
    position: static;
  }

  .nav {
    grid-template-columns: repeat(5, minmax(0, 1fr));
  }

  .nav a {
    justify-content: center;
    text-align: center;
  }

  .nav a span {
    display: none;
  }

  .kpi-grid,
  .dashboard-grid,
  .split-layout,
  .budget-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 620px) {
  .app-shell,
  .sidebar {
    padding: 18px;
  }

  .topbar,
  .section-heading,
  .panel-header,
  .inline-form {
    align-items: stretch;
    flex-direction: column;
    grid-template-columns: 1fr;
  }

  .nav {
    grid-template-columns: 1fr 1fr;
  }

  .kpi strong {
    font-size: 1.45rem;
  }

  .cashflow-chart {
  grid-template-columns: 1fr;
}

.cashflow-stage {
  height: 120px;
}

  .bar-row {
    grid-template-columns: 1fr;
    gap: 6px;
  }

  .bar-row strong,
  .amount {
    text-align: left;
  }

  .transaction-row,
  .budget-meta,
  .budget-numbers {
    align-items: flex-start;
    flex-direction: column;
  }
}
"""


ROUTES = [
    ("/", "D", "Dashboard"),
    ("/transactions", "T", "Transactions"),
    ("/budgets", "B", "Budgets"),
    ("/recommendations", "A", "AI Advisor"),
]


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def load_state() -> tuple[list[dict], list[dict]]:
    if not DATA_FILE.exists():
        return create_demo_transactions(), default_budgets()

    try:
        raw_state = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return create_demo_transactions(), default_budgets()

    return (
        normalize_transactions(raw_state.get("transactions")),
        normalize_budgets(raw_state.get("budgets")),
    )


def save_state(transactions: list[dict], budgets: list[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps({"transactions": transactions, "budgets": budgets}, indent=2),
        encoding="utf-8",
    )


def selected_attr(value: str, selected: str) -> str:
    return " selected" if value == selected else ""


def category_options(selected: str = "", include_auto: bool = False, include_all: bool = False) -> str:
    options = []
    if include_all:
        options.append(f'<option value="all"{selected_attr("all", selected)}>All</option>')
    if include_auto:
        options.append(f'<option value="auto"{selected_attr("auto", selected)}>Auto suggest</option>')

    for category in CATEGORIES:
        options.append(f'<option value="{escape(category)}"{selected_attr(category, selected)}>{escape(category)}</option>')

    return "\n".join(options)


def expense_category_options(selected: str = "") -> str:
    return "\n".join(
        f'<option value="{escape(category)}"{selected_attr(category, selected)}>{escape(category)}</option>'
        for category in CATEGORIES
        if category != "Income"
    )


def nav_html(active_path: str) -> str:
    links = []
    for path, initial, label in ROUTES:
        active_class = " active" if path == active_path else ""
        links.append(
            f'<a class="{active_class}" href="{path}"><span aria-hidden="true">{initial}</span>{label}</a>'
        )
    return "\n".join(links)


def layout(active_path: str, body: str) -> bytes:
    month_label = date.today().strftime("%B %Y")
    document = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Estalv-IA | Python dashboard</title>
    <style>{STYLE}</style>
  </head>
  <body>
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark" aria-hidden="true">E</div>
        <div>
          <strong>Estalv-IA</strong>
          <span>Clear personal finance</span>
        </div>
      </div>
      <nav class="nav" aria-label="Main sections">
        {nav_html(active_path)}
      </nav>
    </aside>
    <main class="app-shell">
      <header class="topbar">
        <div>
          <p class="eyebrow">Public preview - AI Advisor</p>
          <h1>Monthly control</h1>
        </div>
        <div class="month-chip">{escape(month_label)}</div>
      </header>
      {body}
    </main>
  </body>
</html>"""
    return document.encode("utf-8")


def section_heading(eyebrow: str, title: str, action: str = "") -> str:
    return f"""
    <div class="section-heading">
      <div>
        <p class="eyebrow">{escape(eyebrow)}</p>
        <h2>{escape(title)}</h2>
      </div>
      {action}
    </div>
    """


def transaction_row(transaction: dict) -> str:
    sign = "+" if transaction["type"] == "income" else "-"
    amount_class = "income" if transaction["type"] == "income" else "expense"
    return f"""
    <article class="transaction-row">
      <div class="transaction-title">
        <strong>{escape(transaction["description"])}</strong>
        <span>{escape(transaction["category"])} - {escape(format_transaction_date(transaction["date"]))}</span>
      </div>
      <div class="amount {amount_class}">{sign}{escape(format_money(transaction["amount"]))}</div>
    </article>
    """

def cashflow_chart_html(totals: dict) -> str:
    income = float(totals.get("income", 0))
    expense = float(totals.get("expense", 0))
    balance = float(totals.get("balance", 0))
    daily_limit = calculate_daily_spending_limit(totals["balance"])
    max_value = max(income, expense, abs(balance), 1)

    chart_items = [
        ("Income", income, "income"),
        ("Expenses", expense, "expense"),
        ("Balance", abs(balance), "balance negative" if balance < 0 else "balance"),
    ]

    return "\n".join(
        f"""
        <div class="cashflow-item">
          <div class="cashflow-stage" aria-hidden="true">
            <div class="cashflow-bar {css_class}" style="height: {max(round((value / max_value) * 100), 4)}%"></div>
          </div>
          <div>
            <div class="cashflow-label">{escape(label)}</div>
            <div class="cashflow-value">{escape(format_money(balance if label == "Balance" else value))}</div>
          </div>
        </div>
        """
        for label, value, css_class in chart_items
    )


def smart_saving_goal_html(totals: dict) -> str:
    balance = float(totals.get("balance", 0))
    if balance > 0:
        suggested_saving = balance * 0.25
        return f"""
        <section class="panel insight-card">
          <div class="panel-header"><h3>Smart saving goal</h3></div>
          <p>You could save:</p>
          <div class="insight-value">{escape(format_money(suggested_saving))}</div>
          <p>This is 25% of your current positive balance.</p>
        </section>
        """

    return f"""
        <section class="panel insight-card danger">
          <div class="panel-header"><h3>Smart saving goal</h3></div>
          <p>No saving goal suggested yet.</p>
          <div class="insight-value">{escape(format_money(0))}</div>
          <p>Try reducing expenses before setting a monthly saving goal.</p>
        </section>
        """


def render_dashboard(transactions: list[dict], budgets: list[dict]) -> bytes:
    
    month_transactions = get_month_transactions(transactions)
    budget_alerts = build_budget_alerts(budgets, month_transactions)
    
    totals = get_totals(month_transactions)
    saving_rate = get_saving_rate(totals)
    summary = get_expense_by_category(month_transactions)
    daily_limit = calculate_daily_spending_limit(totals["balance"])
    latest = sorted_transactions(transactions)[:5]
    cashflow_chart = cashflow_chart_html(totals)
    saving_goal_card = smart_saving_goal_html(totals)
    biggest_expense = get_biggest_expense_of_month(transactions)

    if biggest_expense:
        biggest_expense_card = f"""
        <div class="insight-card warning">
            <h3>Biggest expense this month</h3>
            <div class="insight-value">{escape(format_money(biggest_expense["amount"]))}</div>
            <p>
                {escape(biggest_expense["description"])} · 
                {escape(biggest_expense["category"])} · 
                {escape(format_transaction_date(biggest_expense["date"]))}
            </p>
        </div>
        """
    else:
        biggest_expense_card = """
        <div class="insight-card">
            <h3>Biggest expense this month</h3>
            <p>No expenses registered this month yet.</p>
        </div>
        """

    dashboard_actions = """
    <div class="actions-row">
      <form method="get" action="/export">
        <button class="secondary-button" type="submit">Export CSV</button>
      </form>
      <form method="post" action="/reset">
        <button class="secondary-button" type="submit">Restore demo</button>
      </form>
    </div>
    """

    if summary:
        max_amount = max(summary.values())
        category_bars = "\n".join(
            f"""
            <div class="bar-row">
              <span>{escape(category)}</span>
              <div class="bar-track" aria-hidden="true">
                <div class="bar-fill" style="width: {round((amount / max_amount) * 100)}%"></div>
              </div>
              <strong>{escape(format_money(amount))}</strong>
            </div>
            """
            for category, amount in sorted(summary.items(), key=lambda item: item[1], reverse=True)
        )
    else:
        category_bars = '<div class="empty-state">There are no expenses this month yet.</div>'

    latest_rows = "\n".join(transaction_row(transaction) for transaction in latest)
    if not latest_rows:
        latest_rows = '<div class="empty-state">Add a transaction to get started.</div>'

    if budget_alerts:
        alerts_html = "\n".join(
            f"""
            <article class="alert">
              <strong>{escape(alert["title"])}</strong>
              <p>{escape(alert["body"])}</p>
            </article>
            """
            for alert in budget_alerts
        )
    else:
        alerts_html = ""
    body = f"""
    <section>
      {section_heading("Overview", "Financial situation", dashboard_actions)}
      {alerts_html}
      <div class="kpi-grid" aria-label="Main indicators">
        <article class="kpi"><span>Income</span><strong>{escape(format_money(totals["income"]))}</strong></article>
        <article class="kpi"><span>Expenses</span><strong>{escape(format_money(totals["expense"]))}</strong></article>
        <article class="kpi"><span>Balance</span><strong>{escape(format_money(totals["balance"]))}</strong></article>
        <article class="kpi"><span>Daily limit</span><strong>{escape(format_money(daily_limit))}</strong></article>
        <article class="kpi"><span>Estimated savings</span><strong>{saving_rate}%</strong></article>
      </div>
      {biggest_expense_card}
      <div class="dashboard-grid">
        <section class="panel" aria-labelledby="cashflow-title">
          <div class="panel-header"><h3 id="cashflow-title">Income vs expenses</h3></div>
          <div class="cashflow-chart" aria-label="Monthly income, expenses and balance comparison">
            {cashflow_chart}
          </div>
        </section>

        {saving_goal_card}

        <section class="panel" aria-labelledby="categories-title">
          <div class="panel-header"><h3 id="categories-title">Expenses by category</h3></div>
          <div class="category-bars">{category_bars}</div>
        </section>

        <section class="panel" aria-labelledby="latest-title">
          <div class="panel-header"><h3 id="latest-title">Latest movements</h3></div>
          <div class="transaction-list compact">{latest_rows}</div>
        </section>
      </div>
    </section>
    """
    return layout("/", body)


def render_transactions(transactions: list[dict], error: str = "", selected_filter: str = "all") -> bytes:
    sorted_rows = sorted_transactions(transactions)
    if selected_filter != "all":
        sorted_rows = [transaction for transaction in sorted_rows if transaction["category"] == selected_filter]

    history = "\n".join(transaction_row(transaction) for transaction in sorted_rows)
    if not history:
        history = '<div class="empty-state">There are no transactions for this filter.</div>'

    error_html = f'<div class="alert">{escape(error)}</div>' if error else ""
    today = date.today().isoformat()

    body = f"""
    <section>
      {section_heading("Register", "Transactions")}
      {error_html}
      <div class="split-layout">
        <form class="panel form-panel" method="post" action="/transactions">
          <h3>New transaction</h3>
          <label>
            Type
            <select name="type" required>
              <option value="expense">Expense</option>
              <option value="income">Income</option>
            </select>
          </label>
          <label>
            Amount
            <input name="amount" type="number" min="0.01" step="0.01" placeholder="24.50" required />
          </label>
          <label>
            Description
            <input name="description" type="text" maxlength="50" placeholder="Grocery shopping" required />
          </label>
          <label>
            Category
            <select name="category" required>
              {category_options(selected="auto", include_auto=True)}
            </select>
          </label>
          <label>
            Date
            <input name="date" type="date" value="{today}" required />
          </label>
          <button class="primary-button" type="submit">Save transaction</button>
        </form>
        <section class="panel" aria-labelledby="history-title">
          <div class="panel-header">
            <h3 id="history-title">History</h3>
          </div>
          <form class="inline-form" method="get" action="/transactions">
            <label>
              Filter by category
              <select name="category">
                {category_options(selected=selected_filter, include_all=True)}
              </select>
            </label>
            <button class="secondary-button" type="submit">Apply</button>
          </form>
          <div class="transaction-list">{history}</div>
        </section>
      </div>
    </section>
    """
    return layout("/transactions", body)


def render_budgets(transactions: list[dict], budgets: list[dict], error: str = "") -> bytes:
    month_transactions = get_month_transactions(transactions)
    snapshots = get_budget_snapshots(budgets, month_transactions)

    cards = "\n".join(
        f"""
        <article class="panel budget-card">
          <div class="budget-meta">
            <h3>{escape(snapshot["category"])}</h3>
            <span class="status-pill {escape(snapshot["status"])}">{escape(snapshot["label"])}</span>
          </div>
          <div class="progress-track" aria-hidden="true">
            <div class="progress-fill {escape(snapshot["status"])}" style="width: {snapshot["percentage"]}%"></div>
          </div>
          <div class="budget-numbers">
            <span>Spent: {escape(format_money(snapshot["spent"]))}</span>
            <span>Limit: {escape(format_money(snapshot["limit"]))}</span>
            <span>Remaining: {escape(format_money(snapshot["remaining"]))}</span>
          </div>
        </article>
        """
        for snapshot in snapshots
    )
    if not cards:
        cards = '<div class="empty-state">Create a budget to start tracking limits.</div>'

    error_html = f'<div class="alert">{escape(error)}</div>' if error else ""

    body = f"""
    <section>
      {section_heading("Planning", "Budgets")}
      {error_html}
      <div class="split-layout">
        <form class="panel form-panel" method="post" action="/budgets">
          <h3>Set budget limit</h3>
          <label>
            Category
            <select name="category" required>
              {expense_category_options()}
            </select>
          </label>
          <label>
            Monthly limit
            <input name="limit" type="number" min="1" step="1" placeholder="200" required />
          </label>
          <button class="primary-button" type="submit">Save budget</button>
        </form>
        <div class="budget-grid">{cards}</div>
      </div>
    </section>
    """
    return layout("/budgets", body)


def render_recommendations(transactions: list[dict], budgets: list[dict]) -> bytes:
    month_transactions = get_month_transactions(transactions)
    recommendations = "\n".join(
        f"""
        <article class="panel recommendation">
          <h3>{escape(recommendation["title"])}</h3>
          <p>{escape(recommendation["body"])}</p>
        </article>
        """
        for recommendation in build_recommendations(month_transactions, budgets)
    )
    body = f"""
    <section>
      {section_heading("AI Advisor", "Personalized saving plan")}
      <div class="recommendation-list">{recommendations}</div>
    </section>
    """
    return layout("/recommendations", body)


class EstalviaHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        transactions, budgets = load_state()
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        if path == "/":
            self.send_html(render_dashboard(transactions, budgets))
        elif path == "/export":
            self.send_csv(transactions)
        elif path == "/transactions":
            selected_filter = query.get("category", ["all"])[0]
            if selected_filter not in [*CATEGORIES, "all"]:
                selected_filter = "all"
            self.send_html(render_transactions(transactions, selected_filter=selected_filter))
        elif path == "/budgets":
            self.send_html(render_budgets(transactions, budgets))
        elif path == "/recommendations":
            self.send_html(render_recommendations(transactions, budgets))
        elif path == "/privacy":
            self.redirect("/")
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        transactions, budgets = load_state()
        parsed_url = urlparse(self.path)
        fields = self.read_form()

        if parsed_url.path == "/transactions":
            self.save_transaction(transactions, budgets, fields)
        elif parsed_url.path == "/budgets":
            self.save_budget(transactions, budgets, fields)
        elif parsed_url.path == "/reset":
            save_state(create_demo_transactions(), default_budgets())
            self.redirect("/")
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def save_transaction(self, transactions: list[dict], budgets: list[dict], fields: dict[str, str]) -> None:
        transaction_type = fields.get("type", "")
        description = fields.get("description", "").strip()
        category = fields.get("category", "auto")
        transaction_date = fields.get("date", "")

        try:
            amount = float(fields.get("amount", "0"))
            date.fromisoformat(transaction_date)
        except ValueError:
            self.send_html(render_transactions(transactions, error="Use a valid amount and date."))
            return

        if transaction_type not in {"income", "expense"} or amount <= 0 or not description:
            self.send_html(render_transactions(transactions, error="Complete the transaction fields before saving."))
            return

        if category == "auto" or category not in CATEGORIES:
            category = suggest_category(description, transaction_type)

        transactions.append(
            {
                "id": create_id(),
                "type": transaction_type,
                "amount": amount,
                "description": description,
                "category": category,
                "date": transaction_date,
            }
        )

        save_state(transactions, budgets)
        self.redirect("/")

    def save_budget(self, transactions: list[dict], budgets: list[dict], fields: dict[str, str]) -> None:
        category = fields.get("category", "")

        try:
            limit = float(fields.get("limit", "0"))
        except ValueError:
            self.send_html(render_budgets(transactions, budgets, error="Use a valid budget limit."))
            return

        if category not in CATEGORIES or category == "Income" or limit <= 0:
            self.send_html(render_budgets(transactions, budgets, error="Choose a valid category and limit."))
            return

        existing_budget = next((budget for budget in budgets if budget["category"] == category), None)
        if existing_budget:
            existing_budget["limit"] = limit
        else:
            budgets.append({"category": category, "limit": limit})

        save_state(transactions, budgets)
        self.redirect("/budgets")

    def read_form(self) -> dict[str, str]:
        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(raw_body, keep_blank_values=True)
        return {key: values[0] for key, values in parsed_body.items()}

    def redirect(self, location: str) -> None:
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", location)
        self.end_headers()

    def send_csv(self, transactions: list[dict]) -> None:
        content = build_transactions_csv(transactions).encode("utf-8")

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Disposition", 'attachment; filename="estalvia-transactions.csv"')
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_html(self, content: bytes) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format: str, *args: object) -> None:
        return

def run_server(host: str = HOST, port: int = PORT) -> None:
    server = ThreadingHTTPServer((host, port), EstalviaHandler)
    print(f"Estalv-IA is running at http://{host}:{port}")
    print("Press Ctrl+C to stop the server.")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
