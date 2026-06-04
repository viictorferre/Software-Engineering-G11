import html
import json
import os
from datetime import date, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from features.today_spending import calculate_today_spending
from features.daily_spending_limit import calculate_daily_spending_limit

from estalvia_core import (
    CATEGORIES,
    DEFAULT_OLLAMA_API_URL,
    DEFAULT_OLLAMA_MODEL,
    DEFAULT_SAVINGS_TARGET_RATE,
    answer_with_hybrid_coach,
    build_advisor_plan,
    build_budget_alerts,
    build_monthly_summaries,
    build_transactions_csv,
    create_demo_monthly_goals,
    clean_ai_text,
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
    normalize_monthly_goals,
    normalize_transactions,
    sorted_transactions,
    suggest_category,
    get_biggest_expense_of_month,
)


DATA_FILE = Path("data") / "estalvia_state.json"
ASSETS_DIR = Path("assets")
HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "8000"))
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", DEFAULT_OLLAMA_API_URL)
OLLAMA_TIMEOUT = float(os.environ.get("OLLAMA_TIMEOUT", "45"))
MAX_COACH_HISTORY = 20

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
  --coach-panel-height: 640px;
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
}

a {
  color: inherit;
  text-decoration: none;
}

button,
input,
select,
textarea {
  font: inherit;
}

button {
  cursor: pointer;
}

.app-header {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 14px 28px;
  border-bottom: 2px solid rgba(15, 80, 63, 0.24);
  background: #c7e6d8;
  backdrop-filter: blur(14px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: fit-content;
}

.brand-logo {
  width: 38px;
  height: 38px;
  display: block;
  border-radius: 8px;
}

.brand strong,
.brand span {
  display: block;
}

.brand span {
  color: var(--muted);
  font-size: 0.86rem;
  margin-top: 2px;
}

.nav {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  min-width: 0;
}

.nav a {
  min-height: 42px;
  border: 1px solid var(--line);
  border-radius: 999px;
  padding: 0 12px;
  color: var(--muted);
  background: rgba(255, 255, 255, 0.74);
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  font-weight: 800;
  white-space: nowrap;
}

.nav-icon {
  width: 18px;
  height: 18px;
  color: var(--green);
  flex: 0 0 auto;
}

.nav a:hover,
.nav a.active {
  border-color: rgba(22, 116, 93, 0.28);
  background: #eaf7f1;
  color: var(--green-dark);
}

.app-shell {
  min-width: 0;
  padding: 28px;
  max-width: 1480px;
  margin: 0 auto;
}

.topbar,
.section-heading,
.panel-header,
.transaction-row {
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

.dashboard-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(320px, 0.65fr);
  gap: 18px;
  margin-bottom: 18px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.kpi-grid.compact {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.kpi,
.panel {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  box-shadow: var(--shadow);
}

.kpi {
  min-height: 112px;
  padding: 16px;
}

.kpi span {
  color: var(--muted);
  font-weight: 800;
  font-size: 0.82rem;
}

.kpi strong {
  display: block;
  margin-top: 12px;
  font-size: 1.48rem;
  line-height: 1.15;
}

.kpi.primary {
  border-color: rgba(22, 116, 93, 0.22);
  background: #f2fbf7;
}

.overview-panel {
  display: grid;
  gap: 14px;
}

.daily-panel {
  display: grid;
  gap: 14px;
}

.insight-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
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

.insight-card h3 {
  margin-bottom: 0;
}

.insight-card.warning {
  border-left-color: var(--green);
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

.split-layout {
  display: grid;
  grid-template-columns: minmax(280px, 0.42fr) minmax(0, 1fr);
  gap: 22px;
  align-items: start;
}

.split-layout.wide-form {
  grid-template-columns: minmax(320px, 0.36fr) minmax(0, 1fr);
}

.panel-header {
  margin-bottom: 8px;
}

.panel-header h3 {
  margin-bottom: 0;
}

.panel-subtitle {
  margin: 8px 0 0;
  color: var(--muted);
  line-height: 1.5;
}

.category-bars,
.transaction-list,
.budget-grid {
  display: grid;
  gap: 12px;
}

.category-bars,
.transaction-list,
.budget-grid,
.monthly-review-list,
.advisor-action-list {
  scrollbar-gutter: stable;
}

.history-panel .transaction-list {
  max-height: 560px;
  overflow-y: auto;
  overscroll-behavior: contain;
  padding-right: 4px;
}

.transaction-list.compact {
  max-height: 340px;
  overflow-y: auto;
  overscroll-behavior: contain;
  padding-right: 4px;
}

.category-bars {
  max-height: 430px;
  overflow-y: auto;
  overscroll-behavior: contain;
  padding-right: 4px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  align-items: stretch;
}

.dashboard-grid .wide-panel {
  grid-column: 1 / -1;
}

.dashboard-scroll-panel {
  display: flex;
  height: 430px;
  max-height: 430px;
  flex-direction: column;
  overflow: hidden;
}

.dashboard-scroll-panel .panel-header {
  flex: 0 0 auto;
}

.dashboard-scroll-panel .panel-subtitle {
  flex: 0 0 auto;
  margin-bottom: 14px;
}

.dashboard-scroll-panel .transaction-list,
.dashboard-scroll-panel .category-bars {
  flex: 1 1 auto;
  min-height: 0;
  max-height: none;
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
  gap: 11px;
  padding: 14px;
  border: 1px solid rgba(22, 116, 93, 0.13);
  border-radius: 8px;
  background: linear-gradient(135deg, #fbfefd 0%, #f0faf5 100%);
  box-shadow: 0 8px 18px rgba(18, 40, 34, 0.05);
}

.bar-row-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.bar-label {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  min-width: 0;
  color: var(--ink);
  font-weight: 900;
}

.category-icon {
  width: 19px;
  height: 19px;
  color: var(--green);
  flex: 0 0 auto;
}

.bar-label .category-icon {
  width: 22px;
  height: 22px;
  padding: 3px;
  border-radius: 999px;
  background: #e4f3ec;
  color: var(--green-dark);
}

.bar-track {
  height: 10px;
  overflow: hidden;
  border-radius: 999px;
  background: #dfe9e4;
}

.bar-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--green-dark), var(--green));
}

.bar-row strong {
  min-width: max-content;
  color: var(--ink);
  font-variant-numeric: tabular-nums;
  font-size: 1.04rem;
  text-align: right;
  white-space: nowrap;
}

.transaction-row {
  min-height: 72px;
  padding: 14px 16px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
}

.transaction-row:hover {
  border-color: rgba(22, 116, 93, 0.32);
  background: #fbfefd;
}

.transaction-title {
  display: grid;
  gap: 4px;
}

.transaction-title strong {
  font-size: 0.96rem;
}

.transaction-title span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--muted);
  font-size: 0.84rem;
}

.transaction-title .category-icon {
  width: 15px;
  height: 15px;
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
  padding: 22px;
}

.form-panel h3 {
  margin-bottom: 4px;
}

.budget-form-card {
  border-color: rgba(22, 116, 93, 0.16);
  background: linear-gradient(180deg, #ffffff 0%, #f3faf6 100%);
}

form {
  display: grid;
  gap: 16px;
}

label {
  display: grid;
  gap: 7px;
  color: var(--muted);
  font-size: 0.84rem;
  font-weight: 800;
}

input,
select,
textarea {
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #ffffff;
  color: var(--ink);
}

input,
select {
  min-height: 46px;
  padding: 0 12px;
}

textarea {
  min-height: 132px;
  padding: 12px;
  resize: vertical;
}

input:focus,
select:focus,
textarea:focus,
button:focus-visible {
  outline: 3px solid rgba(22, 116, 93, 0.22);
  outline-offset: 2px;
}

.inline-form {
  align-items: end;
  display: grid;
  gap: 12px;
  grid-template-columns: minmax(0, 1fr) auto;
  margin-bottom: 18px;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #f7fbf9;
}

.history-panel,
.budget-list-panel {
  padding: 22px;
}

.budget-overview {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}

.budget-overview-card {
  padding: 14px;
  border: 1px solid rgba(22, 116, 93, 0.14);
  border-radius: 8px;
  background: #f2fbf7;
}

.budget-overview-card span,
.budget-main span,
.budget-stat span,
.budget-card-title span {
  display: block;
  color: var(--muted);
  font-size: 0.76rem;
  font-weight: 900;
  text-transform: uppercase;
}

.budget-overview-card strong {
  display: block;
  margin-top: 6px;
  font-size: 1.22rem;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.budget-grid {
  grid-template-columns: repeat(2, minmax(260px, 1fr));
  gap: 16px;
}

.budget-list-panel .budget-grid {
  max-height: 720px;
  overflow-y: auto;
  overscroll-behavior: contain;
  padding-right: 4px;
  align-content: start;
}

.budget-card {
  display: grid;
  gap: 14px;
  padding: 20px;
  border-color: rgba(22, 116, 93, 0.16);
  background: linear-gradient(135deg, #ffffff 0%, #f4fbf7 100%);
  box-shadow: 0 10px 24px rgba(18, 40, 34, 0.07);
}

.budget-card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
}

.budget-card-title {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.budget-card-title h3 {
  margin-bottom: 0;
}

.budget-card-title span {
  margin-top: 3px;
}

.budget-main {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 14px;
  padding: 14px;
  border: 1px solid rgba(22, 116, 93, 0.12);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.72);
}

.budget-main strong {
  color: var(--green-dark);
  font-size: 1.55rem;
  font-variant-numeric: tabular-nums;
  line-height: 1.1;
  text-align: right;
  white-space: nowrap;
}

.budget-meter-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 12px;
}

.budget-meter-row strong {
  color: var(--green-dark);
  font-size: 0.88rem;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
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
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.budget-stat {
  padding: 10px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.74);
}

.budget-stat strong {
  display: block;
  margin-top: 5px;
  font-size: 1rem;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.budget-overview-card strong.danger,
.budget-stat strong.danger {
  color: var(--red);
}

.monthly-review-list {
  display: grid;
  gap: 16px;
  max-height: 760px;
  overflow-y: auto;
  overscroll-behavior: contain;
  padding-right: 4px;
}

.month-card {
  display: grid;
  gap: 16px;
}

.month-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
}

.month-card-header h3 {
  margin-bottom: 4px;
}

.month-card-header p {
  margin: 0;
  color: var(--muted);
  line-height: 1.45;
}

.month-metrics {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 10px;
}

.month-metric {
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #f7fbf9;
}

.month-metric span {
  display: block;
  margin-bottom: 6px;
  color: var(--muted);
  font-size: 0.78rem;
  font-weight: 900;
  text-transform: uppercase;
}

.month-metric strong {
  font-size: 1rem;
}

.month-metric small {
  display: block;
  margin-top: 4px;
  color: var(--muted);
  font-weight: 800;
}

.goal-summary {
  color: var(--muted);
  line-height: 1.55;
}

.goal-form {
  display: grid;
  grid-template-columns: minmax(190px, 1fr) auto;
  gap: 12px;
  align-items: end;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #f7fbf9;
}

.goal-form label {
  margin: 0;
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

.advisor-hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(180px, 0.28fr);
  gap: 18px;
  align-items: center;
  margin-bottom: 18px;
  border-left: 5px solid var(--green);
  background: linear-gradient(135deg, #ffffff 0%, #edf8f2 100%);
}

.advisor-hero h3 {
  margin-bottom: 8px;
  font-size: 1.25rem;
}

.advisor-hero p {
  margin-bottom: 0;
  color: var(--muted);
  line-height: 1.58;
}

.advisor-impact {
  padding: 16px;
  border: 1px solid rgba(22, 116, 93, 0.16);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.76);
}

.advisor-impact span,
.advisor-card span {
  display: block;
  color: var(--muted);
  font-size: 0.76rem;
  font-weight: 900;
  text-transform: uppercase;
}

.advisor-impact strong {
  display: block;
  margin-top: 8px;
  color: var(--green-dark);
  font-size: 1.35rem;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
}

.advisor-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 18px;
}

.advisor-card {
  display: grid;
  gap: 10px;
}

.advisor-card h3 {
  margin-bottom: 0;
}

.advisor-card p {
  margin-bottom: 0;
  color: var(--muted);
  line-height: 1.55;
}

.advisor-actions {
  display: grid;
  gap: 12px;
}

.advisor-action-list {
  display: grid;
  gap: 10px;
  max-height: 360px;
  overflow-y: auto;
  overscroll-behavior: contain;
  margin: 0;
  padding: 0;
  list-style: none;
}

.advisor-action-list li {
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #f7fbf9;
  color: var(--muted);
  font-weight: 800;
}

.coach-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  align-items: stretch;
}

.coach-grid > .panel {
  height: var(--coach-panel-height);
  min-height: 0;
  max-height: var(--coach-panel-height);
}

.coach-question-card {
  display: grid;
  grid-template-rows: auto auto minmax(0, 1fr) auto;
  align-content: stretch;
  overflow: hidden;
}

.coach-question-card label {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.coach-question-card textarea {
  flex: 1 1 auto;
  min-height: 0;
  resize: none;
  overflow-y: auto;
  overscroll-behavior: contain;
}

.coach-thread-panel {
  display: grid;
  gap: 14px;
  grid-template-rows: auto minmax(0, 1fr);
  overflow: hidden;
}

.coach-thread-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.coach-thread-header h3 {
  margin-bottom: 4px;
}

.coach-chat-window {
  min-height: 0;
  overflow-y: auto;
  overscroll-behavior: contain;
  display: grid;
  align-content: start;
  gap: 14px;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #f7fbf9;
}

.chat-turn {
  display: grid;
  gap: 8px;
}

.chat-bubble {
  max-width: 88%;
  padding: 12px 14px;
  border-radius: 8px;
  line-height: 1.55;
}

.chat-bubble.user {
  justify-self: end;
  background: var(--green);
  color: #ffffff;
}

.chat-bubble.assistant {
  justify-self: start;
  border: 1px solid rgba(22, 116, 93, 0.16);
  background: #ffffff;
  color: var(--ink);
}

.chat-bubble strong {
  display: block;
  margin-bottom: 5px;
}

.chat-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-top: 8px;
  color: var(--muted);
  font-size: 0.76rem;
  font-weight: 800;
}

.chat-evidence {
  display: grid;
  gap: 5px;
  margin: 10px 0 0;
  padding: 0;
  list-style: none;
  color: var(--muted);
  font-size: 0.78rem;
  font-weight: 800;
}

.coach-empty {
  align-self: center;
  text-align: center;
}

.coach-provider {
  display: inline-flex;
  width: fit-content;
  margin-bottom: 12px;
  border-radius: 999px;
  padding: 6px 10px;
  background: #e8f4ff;
  color: var(--blue);
  font-size: 0.78rem;
  font-weight: 900;
}

.coach-provider.fallback {
  background: #fff2cf;
  color: #805600;
}

.chat-meta .coach-provider {
  margin-bottom: 0;
}

.fallback-note {
  margin: 12px 0 0;
  color: var(--yellow);
  font-weight: 800;
}

.sample-prompts,
.coach-capabilities {
  display: grid;
  gap: 10px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.sample-prompts li,
.coach-capabilities li {
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #f7fbf9;
  color: var(--muted);
  font-weight: 700;
}

.coach-capabilities {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.sample-prompts {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.coach-capabilities li strong {
  display: block;
  margin-bottom: 4px;
  color: var(--ink);
}

.coach-helper {
  color: var(--muted);
  line-height: 1.55;
}

.coach-prompts {
  margin-top: 18px;
}

.coach-mode-note {
  margin-bottom: 18px;
}

.coach-mode-note p {
  color: var(--muted);
  line-height: 1.58;
}

.empty-state,
.alert {
  padding: 18px;
  border: 1px solid var(--line);
  border-left: 5px solid var(--green);
  border-radius: 8px;
  color: var(--muted);
  background: rgba(255, 255, 255, 0.75);
}

.alert {
  margin-bottom: 18px;
}

.alert p {
  margin: 6px 0 0;
  line-height: 1.5;
}

.alert-carousel {
  display: grid;
  grid-template-columns: 46px minmax(0, 1fr) 46px;
  gap: 10px;
  align-items: stretch;
  margin-bottom: 22px;
}

.alert-window {
  position: relative;
  min-width: 0;
}

.alert-carousel .alert {
  display: none;
  min-height: 122px;
  margin-bottom: 0;
  padding-right: 92px;
}

.alert-carousel .alert.active {
  display: block;
}

.alert-control {
  min-height: 100%;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.82);
  color: var(--green-dark);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(18, 40, 34, 0.05);
}

.alert-control:hover {
  border-color: rgba(22, 116, 93, 0.28);
  background: #eaf7f1;
}

.alert-control:disabled {
  cursor: default;
  opacity: 0.45;
}

.alert-arrow-icon {
  width: 20px;
  height: 20px;
}

.alert-count {
  position: absolute;
  top: 14px;
  right: 16px;
  z-index: 1;
  border-radius: 999px;
  padding: 5px 9px;
  background: rgba(255, 255, 255, 0.78);
  color: var(--green-dark);
  font-size: 0.78rem;
  font-weight: 900;
  box-shadow: 0 5px 14px rgba(18, 40, 34, 0.08);
}

.alert.warning {
  border-color: #f1cc7a;
  border-left-color: var(--yellow);
  background: #fff8e8;
  color: #765000;
}

.alert.danger {
  border-color: #ffb4a8;
  border-left-color: var(--red);
  background: #fff1ef;
  color: var(--red);
}

"""


ROUTES = [
    ("/", "dashboard", "Dashboard"),
    ("/transactions", "transactions", "Transactions"),
    ("/budgets", "budgets", "Budgets"),
    ("/monthly-review", "review", "Monthly Review"),
    ("/recommendations", "advisor", "AI Advisor"),
    ("/coach", "coach", "AI Coach"),
]


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def format_goal_rate(value: float) -> str:
    return f"{float(value):g}"


def normalize_coach_history(raw_history: object) -> list[dict]:
    if not isinstance(raw_history, list):
        return []

    history = []
    for raw in raw_history:
        if not isinstance(raw, dict):
            continue

        question = clean_ai_text(raw.get("question", ""))
        answer = clean_ai_text(raw.get("answer", ""))
        if not question or not answer:
            continue

        evidence = raw.get("evidence", [])
        if not isinstance(evidence, list):
            evidence = []

        history.append(
            {
                "question": question[:600],
                "title": clean_ai_text(raw.get("title", "AI Coach"))[:120] or "AI Coach",
                "answer": answer[:2400],
                "provider": clean_ai_text(raw.get("provider", "Local coach"))[:120] or "Local coach",
                "fallback": bool(raw.get("fallback", False)),
                "fallback_reason": clean_ai_text(raw.get("fallback_reason", ""))[:240],
                "evidence": [clean_ai_text(item)[:180] for item in evidence if clean_ai_text(item)][:5],
                "created_at": str(raw.get("created_at", ""))[:32],
            }
        )

    return history[-MAX_COACH_HISTORY:]


def format_chat_time(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return ""

    return parsed.strftime("%d %b, %H:%M")


def coach_history_entry(question: str, response: dict) -> dict:
    return {
        "question": clean_ai_text(question),
        "title": clean_ai_text(response.get("title", "AI Coach")),
        "answer": clean_ai_text(response.get("answer", "")),
        "provider": clean_ai_text(response.get("provider", "Local coach")),
        "fallback": bool(response.get("fallback", False)),
        "fallback_reason": clean_ai_text(response.get("fallback_reason", "")),
        "evidence": [clean_ai_text(item) for item in response.get("evidence", [])],
        "created_at": datetime.now().isoformat(timespec="minutes"),
    }


def create_demo_coach_history() -> list[dict]:
    created_at = datetime.now().isoformat(timespec="minutes")
    return normalize_coach_history(
        [
            {
                "question": "Which budget is closest to the limit?",
                "title": "Budget risk check",
                "answer": (
                    "Transport and Leisure need attention first because they are already over the monthly limit. "
                    "Housing, Food and Studies are also close to their limits, so avoid adding new spending there."
                ),
                "provider": "Local fallback",
                "fallback": True,
                "fallback_reason": "Demo conversation saved locally.",
                "evidence": [
                    "Transport: 100% used",
                    "Leisure: 100% used",
                    "Housing: 93% used",
                ],
                "created_at": created_at,
            },
            {
                "question": "Can I afford a 30 euro dinner this week?",
                "title": "Ollama AI Coach",
                "answer": (
                    "You can afford it from your current balance, but it would make the Leisure budget worse. "
                    "A safer choice is to keep the dinner under EUR 15.00 or move it to next month."
                ),
                "provider": f"Ollama local model: {OLLAMA_MODEL}",
                "fallback": False,
                "evidence": [
                    "Monthly balance is positive",
                    "Leisure budget is exceeded",
                    "Saving goal is still on track",
                ],
                "created_at": created_at,
            },
        ]
    )


def load_state() -> tuple[list[dict], list[dict], dict[str, float], list[dict]]:
    if not DATA_FILE.exists():
        return create_demo_transactions(), default_budgets(), create_demo_monthly_goals(), create_demo_coach_history()

    try:
        raw_state = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return create_demo_transactions(), default_budgets(), create_demo_monthly_goals(), create_demo_coach_history()

    if not isinstance(raw_state, dict):
        return create_demo_transactions(), default_budgets(), create_demo_monthly_goals(), create_demo_coach_history()

    return (
        normalize_transactions(raw_state.get("transactions")),
        normalize_budgets(raw_state.get("budgets")),
        normalize_monthly_goals(raw_state.get("monthly_goals")),
        normalize_coach_history(raw_state.get("coach_history")),
    )


def save_state(
    transactions: list[dict],
    budgets: list[dict],
    monthly_goals: dict[str, float] | None = None,
    coach_history: list[dict] | None = None,
) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(
            {
                "transactions": transactions,
                "budgets": budgets,
                "monthly_goals": normalize_monthly_goals(monthly_goals or {}),
                "coach_history": normalize_coach_history(coach_history or []),
            },
            indent=2,
        ),
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


def nav_icon(name: str) -> str:
    icons = {
        "dashboard": """
          <path d="M4 13a8 8 0 0 1 16 0" />
          <path d="M12 13l4-5" />
          <path d="M6 17h12" />
        """,
        "transactions": """
          <path d="M7 7h10" />
          <path d="M7 12h10" />
          <path d="M7 17h6" />
          <path d="M4 5v14" />
        """,
        "budgets": """
          <rect x="4" y="5" width="16" height="14" rx="3" />
          <path d="M8 9h8" />
          <path d="M8 13h4" />
          <path d="M16 15h.01" />
        """,
        "review": """
          <path d="M5 19V7" />
          <path d="M10 19V4" />
          <path d="M15 19v-9" />
          <path d="M20 19v-5" />
        """,
        "advisor": """
          <path d="M12 3l1.8 4.2L18 9l-4.2 1.8L12 15l-1.8-4.2L6 9l4.2-1.8L12 3Z" />
          <path d="M5 15l.8 1.7L7.5 18l-1.7.8L5 21l-.8-2.2L2.5 18l1.7-1.3L5 15Z" />
        """,
        "coach": """
          <path d="M6 7h12a3 3 0 0 1 3 3v4a3 3 0 0 1-3 3h-5l-4 3v-3H6a3 3 0 0 1-3-3v-4a3 3 0 0 1 3-3Z" />
          <path d="M8 11h.01" />
          <path d="M12 11h.01" />
          <path d="M16 11h.01" />
        """,
    }
    paths = icons.get(name, icons["dashboard"])
    return f"""
    <svg class="nav-icon" aria-hidden="true" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      {paths}
    </svg>
    """


def category_icon(category: str) -> str:
    icons = {
        "Food": """
          <path d="M7 3v8" />
          <path d="M10 3v8" />
          <path d="M7 7h3" />
          <path d="M8.5 11v10" />
          <path d="M16 3v18" />
          <path d="M16 3c2.1 1.4 3 3.5 3 5.5 0 2.3-1.1 3.8-3 4.5" />
        """,
        "Transport": """
          <path d="M5 16h14" />
          <path d="M7 16l1.3-6h7.4L17 16" />
          <path d="M9 10l1-3h4l1 3" />
          <circle cx="8" cy="17" r="1.6" />
          <circle cx="16" cy="17" r="1.6" />
        """,
        "Leisure": """
          <path d="M5 8h14v4a2 2 0 0 0 0 4v3H5v-3a2 2 0 0 0 0-4V8Z" />
          <path d="M10 9v10" />
          <path d="M14 12h2" />
          <path d="M14 16h2" />
        """,
        "Housing": """
          <path d="M3 11l9-7 9 7" />
          <path d="M5 10v10h14V10" />
          <path d="M10 20v-6h4v6" />
        """,
        "Studies": """
          <path d="M5 5.5A2.5 2.5 0 0 1 7.5 3H20v16H7.5A2.5 2.5 0 0 0 5 21V5.5Z" />
          <path d="M5 17.5A2.5 2.5 0 0 1 7.5 15H20" />
          <path d="M9 7h7" />
        """,
        "Health": """
          <path d="M20.5 8.5c0 5.2-8.5 10.2-8.5 10.2S3.5 13.7 3.5 8.5A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 8.5 1.5Z" />
          <path d="M8 12h2l1-2 2 4 1-2h2" />
        """,
        "Income": """
          <rect x="4" y="6" width="16" height="13" rx="3" />
          <path d="M16 12h.01" />
          <path d="M12 16V8" />
          <path d="M9 11l3-3 3 3" />
        """,
        "Other": """
          <circle cx="12" cy="12" r="8" />
          <path d="M9 12h.01" />
          <path d="M12 12h.01" />
          <path d="M15 12h.01" />
        """,
    }
    paths = icons.get(category, icons["Other"])
    return f"""
    <svg class="category-icon" aria-hidden="true" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">
      {paths}
    </svg>
    """


def nav_html(active_path: str) -> str:
    links = []
    for path, icon, label in ROUTES:
        active_class = " active" if path == active_path else ""
        links.append(
            f'<a class="{active_class}" href="{path}">{nav_icon(icon)}{escape(label)}</a>'
        )
    return "\n".join(links)


def alert_arrow_icon(direction: str) -> str:
    path = '<path d="M15 18l-6-6 6-6" />' if direction == "previous" else '<path d="M9 18l6-6-6-6" />'
    return f"""
    <svg class="alert-arrow-icon" aria-hidden="true" viewBox="0 0 24 24" fill="none"
         stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
      {path}
    </svg>
    """


def layout(active_path: str, body: str) -> bytes:
    month_label = date.today().strftime("%B %Y")
    interaction_script = """
    <script>
      (function () {
        document.querySelectorAll("[data-alert-carousel]").forEach(function (carousel) {
          const alerts = Array.from(carousel.querySelectorAll(".alert"));
          const previous = carousel.querySelector("[data-alert-prev]");
          const next = carousel.querySelector("[data-alert-next]");
          const count = carousel.querySelector("[data-alert-count]");
          let current = 0;

          function showAlert(index) {
            if (!alerts.length) {
              return;
            }

            current = (index + alerts.length) % alerts.length;
            alerts.forEach(function (alert, alertIndex) {
              alert.classList.toggle("active", alertIndex === current);
            });

            if (count) {
              count.textContent = String(current + 1) + " / " + String(alerts.length);
            }
          }

          if (alerts.length <= 1) {
            if (previous) {
              previous.disabled = true;
            }
            if (next) {
              next.disabled = true;
            }
          }

          if (previous) {
            previous.addEventListener("click", function () {
              showAlert(current - 1);
            });
          }

          if (next) {
            next.addEventListener("click", function () {
              showAlert(current + 1);
            });
          }

          showAlert(0);
        });
      }());
    </script>
    """
    document = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Estalv-IA | Python dashboard</title>
    <style>{STYLE}</style>
  </head>
  <body>
    <header class="app-header">
      <div class="brand">
        <img class="brand-logo" src="/assets/logo.png" alt="" aria-hidden="true" />
        <div>
          <strong>Estalv-IA</strong>
          <span>Clear personal finance</span>
        </div>
      </div>
      <nav class="nav" aria-label="Main sections">
        {nav_html(active_path)}
      </nav>
    </header>
    <main class="app-shell">
      <header class="topbar">
        <div>
          <p class="eyebrow">Final product demo</p>
          <h1>Monthly control</h1>
        </div>
        <div class="month-chip">{escape(month_label)}</div>
      </header>
      {body}
    </main>
    {interaction_script}
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
        <span>
          {category_icon(transaction["category"])}
          {escape(transaction["category"])} - {escape(format_transaction_date(transaction["date"]))}
        </span>
      </div>
      <div class="amount {amount_class}">{sign}{escape(format_money(transaction["amount"]))}</div>
    </article>
    """


def cashflow_chart_html(totals: dict) -> str:
    income = float(totals.get("income", 0))
    expense = float(totals.get("expense", 0))
    balance = float(totals.get("balance", 0))
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
    today_spending = calculate_today_spending(month_transactions)
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
                {escape(biggest_expense["description"])} &middot;
                {escape(biggest_expense["category"])} &middot;
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
            <article class="bar-row">
              <div class="bar-row-top">
                <span class="bar-label">{category_icon(category)}{escape(category)}</span>
                <strong>{escape(format_money(amount))}</strong>
              </div>
              <div class="bar-track" aria-hidden="true">
                <div class="bar-fill" style="width: {round((amount / max_amount) * 100)}%"></div>
              </div>
            </article>
            """
            for category, amount in sorted(summary.items(), key=lambda item: item[1], reverse=True)
        )
    else:
        category_bars = '<div class="empty-state">There are no expenses this month yet.</div>'

    latest_rows = "\n".join(transaction_row(transaction) for transaction in latest)
    if not latest_rows:
        latest_rows = '<div class="empty-state">Add a transaction to get started.</div>'

    if budget_alerts:
        alert_cards = "\n".join(
            f"""
            <article class="alert {escape(alert["level"])}{' active' if index == 0 else ''}">
              <strong>{escape(alert["title"])}</strong>
              <p>{escape(alert["body"])}</p>
            </article>
            """
            for index, alert in enumerate(budget_alerts)
        )
        alerts_html = f"""
        <section class="alert-carousel" data-alert-carousel aria-label="Budget notifications">
          <button class="alert-control" type="button" data-alert-prev aria-label="Previous notification">
            {alert_arrow_icon("previous")}
          </button>
          <div class="alert-window" aria-live="polite">
            <span class="alert-count" data-alert-count>1 / {len(budget_alerts)}</span>
            {alert_cards}
          </div>
          <button class="alert-control" type="button" data-alert-next aria-label="Next notification">
            {alert_arrow_icon("next")}
          </button>
        </section>
        """
    else:
        alerts_html = ""
    body = f"""
    <section>
      {section_heading("Overview", "Financial situation", dashboard_actions)}
      {alerts_html}
      <div class="dashboard-hero">
        <section class="panel overview-panel" aria-labelledby="monthly-summary-title">
          <div class="panel-header"><h3 id="monthly-summary-title">Monthly summary</h3></div>
          <div class="kpi-grid" aria-label="Monthly indicators">
            <article class="kpi primary"><span>Income</span><strong>{escape(format_money(totals["income"]))}</strong></article>
            <article class="kpi"><span>Expenses</span><strong>{escape(format_money(totals["expense"]))}</strong></article>
            <article class="kpi primary"><span>Balance</span><strong>{escape(format_money(totals["balance"]))}</strong></article>
          </div>
        </section>
        <section class="panel daily-panel" aria-labelledby="daily-control-title">
          <div class="panel-header"><h3 id="daily-control-title">Daily control</h3></div>
          <div class="kpi-grid compact" aria-label="Daily spending indicators">
            <article class="kpi"><span>Spent today</span><strong>{escape(format_money(today_spending))}</strong></article>
            <article class="kpi"><span>Daily limit</span><strong>{escape(format_money(daily_limit))}</strong></article>
          </div>
          <article class="kpi primary"><span>Estimated savings</span><strong>{saving_rate}%</strong></article>
        </section>
      </div>
      <div class="insight-grid">
        {saving_goal_card}
        {biggest_expense_card}
      </div>
      <div class="dashboard-grid">
        <section class="panel wide-panel" aria-labelledby="cashflow-title">
          <div class="panel-header"><h3 id="cashflow-title">Income vs expenses</h3></div>
          <div class="cashflow-chart" aria-label="Monthly income, expenses and balance comparison">
            {cashflow_chart}
          </div>
        </section>

        <section class="panel dashboard-scroll-panel" aria-labelledby="latest-title">
          <div class="panel-header"><h3 id="latest-title">Latest movements</h3></div>
          <div class="transaction-list compact">{latest_rows}</div>
        </section>

        <section class="panel dashboard-scroll-panel" aria-labelledby="categories-title">
          <div class="panel-header"><h3 id="categories-title">Expenses by category</h3></div>
          <p class="panel-subtitle">Top spending areas for the current month.</p>
          <div class="category-bars">{category_bars}</div>
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

    error_html = f'<div class="alert danger">{escape(error)}</div>' if error else ""
    today = date.today().isoformat()

    body = f"""
    <section>
      {section_heading("Register", "Transactions")}
      {error_html}
      <div class="split-layout wide-form">
        <form class="panel form-panel" method="post" action="/transactions">
          <h3>New transaction</h3>
          <p class="panel-subtitle">Add income or expenses and let the app categorize common descriptions automatically.</p>
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
        <section class="panel history-panel" aria-labelledby="history-title">
          <div class="panel-header">
            <h3 id="history-title">History</h3>
          </div>
          <p class="panel-subtitle">Review all registered movements or filter them by category.</p>
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
    total_spent = round(sum(snapshot["spent"] for snapshot in snapshots), 2)
    total_limit = round(sum(snapshot["limit"] for snapshot in snapshots), 2)
    total_remaining = round(total_limit - total_spent, 2)
    remaining_class = " danger" if total_remaining < 0 else ""

    cards = "\n".join(
        f"""
        <article class="panel budget-card">
          <div class="budget-card-top">
            <div class="budget-card-title">
              {category_icon(snapshot["category"])}
              <div>
                <h3>{escape(snapshot["category"])}</h3>
                <span>{snapshot["percentage"]}% used</span>
              </div>
            </div>
            <span class="status-pill {escape(snapshot["status"])}">{escape(snapshot["label"])}</span>
          </div>
          <div class="budget-main">
            <div>
              <span>Spent this month</span>
              <strong>{escape(format_money(snapshot["spent"]))}</strong>
            </div>
          </div>
          <div class="budget-meter-row">
            <div class="progress-track" aria-hidden="true">
              <div class="progress-fill {escape(snapshot["status"])}" style="width: {snapshot["percentage"]}%"></div>
            </div>
            <strong>{snapshot["percentage"]}%</strong>
          </div>
          <div class="budget-numbers">
            <div class="budget-stat">
              <span>Monthly limit</span>
              <strong>{escape(format_money(snapshot["limit"]))}</strong>
            </div>
            <div class="budget-stat">
              <span>Remaining</span>
              <strong class="{'danger' if snapshot["remaining"] < 0 else ''}">
                {escape(format_money(snapshot["remaining"]))}
              </strong>
            </div>
          </div>
        </article>
        """
        for snapshot in snapshots
    )
    if not cards:
        cards = '<div class="empty-state">Create a budget to start tracking limits.</div>'

    error_html = f'<div class="alert danger">{escape(error)}</div>' if error else ""

    body = f"""
    <section>
      {section_heading("Planning", "Budgets")}
      {error_html}
      <div class="budget-overview" aria-label="Budget overview">
        <article class="budget-overview-card">
          <span>Total limit</span>
          <strong>{escape(format_money(total_limit))}</strong>
        </article>
        <article class="budget-overview-card">
          <span>Spent this month</span>
          <strong>{escape(format_money(total_spent))}</strong>
        </article>
        <article class="budget-overview-card">
          <span>Remaining</span>
          <strong class="{remaining_class.strip()}">{escape(format_money(total_remaining))}</strong>
        </article>
      </div>
      <div class="split-layout wide-form">
        <form class="panel form-panel budget-form-card" method="post" action="/budgets">
          <h3>Set budget limit</h3>
          <p class="panel-subtitle">Create or update monthly category limits to receive early spending warnings.</p>
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
        <section class="panel budget-list-panel" aria-labelledby="budget-list-title">
          <div class="panel-header"><h3 id="budget-list-title">Current limits</h3></div>
          <p class="panel-subtitle">Track category progress and remaining money for the current month.</p>
          <div class="budget-grid">{cards}</div>
        </section>
      </div>
    </section>
    """
    return layout("/budgets", body)


def render_monthly_review(transactions: list[dict], monthly_goals: dict[str, float], error: str = "") -> bytes:
    summaries = build_monthly_summaries(transactions, monthly_goals=monthly_goals)
    if summaries:
        cards = "\n".join(month_summary_card(summary) for summary in summaries)
    else:
        cards = '<div class="empty-state">Add transactions to build your monthly review.</div>'

    error_html = f'<div class="alert danger">{escape(error)}</div>' if error else ""

    body = f"""
    <section>
      {section_heading("Monthly Review", "Previous months")}
      {error_html}
      <section class="panel" aria-labelledby="monthly-review-title">
        <div class="panel-header"><h3 id="monthly-review-title">Savings objective history</h3></div>
        <p class="panel-subtitle">
          The default saving objective is {DEFAULT_SAVINGS_TARGET_RATE}% of income, but each month can have its own goal.
        </p>
        <div class="monthly-review-list">{cards}</div>
      </section>
    </section>
    """
    return layout("/monthly-review", body)


def month_summary_card(summary: dict) -> str:
    target_rate = format_goal_rate(summary["target_rate"])
    if summary["status"] == "ok":
        goal_text = f"Goal met by {format_money(summary['gap'])}."
    elif summary["status"] == "warning":
        goal_text = f"Needs {format_money(abs(summary['gap']))} more to reach the monthly saving target."
    else:
        goal_text = "Income is needed before the saving objective can be evaluated."

    return f"""
    <article class="month-card panel">
      <div class="month-card-header">
        <div>
          <h3>{escape(summary["label"])}</h3>
          <p>{escape(summary["transaction_count"])} registered movements</p>
        </div>
        <span class="status-pill {escape(summary["status"])}">{escape(summary["status_label"])}</span>
      </div>
      <div class="month-metrics">
        <div class="month-metric"><span>Income</span><strong>{escape(format_money(summary["income"]))}</strong></div>
        <div class="month-metric"><span>Expenses</span><strong>{escape(format_money(summary["expense"]))}</strong></div>
        <div class="month-metric"><span>Balance</span><strong>{escape(format_money(summary["balance"]))}</strong></div>
        <div class="month-metric"><span>Savings rate</span><strong>{summary["saving_rate"]}%</strong></div>
        <div class="month-metric">
          <span>Target</span>
          <strong>{escape(target_rate)}%</strong>
          <small>{escape(format_money(summary["target_amount"]))}</small>
        </div>
      </div>
      <div class="progress-track" aria-hidden="true">
        <div class="progress-fill {escape(summary["status"])}" style="width: {summary["progress"]}%"></div>
      </div>
      <p class="goal-summary">{escape(goal_text)}</p>
      <form class="goal-form" method="post" action="/monthly-review">
        <input type="hidden" name="month" value="{escape(summary["month"])}" />
        <label>
          Saving goal for this month
          <input name="target_rate" type="number" min="0" max="100" step="0.5" value="{escape(target_rate)}" required />
        </label>
        <button class="secondary-button" type="submit">Update goal</button>
      </form>
    </article>
    """


def render_recommendations(transactions: list[dict], budgets: list[dict], monthly_goals: dict[str, float]) -> bytes:
    month_transactions = get_month_transactions(transactions)
    plan = build_advisor_plan(month_transactions, budgets, monthly_goals)
    actions = "\n".join(f"<li>{escape(action)}</li>" for action in plan["actions"])
    monthly_goal = plan["monthly_goal"]
    budget_risk = plan["budget_risk"]
    spending_focus = plan["spending_focus"]

    body = f"""
    <section>
      {section_heading("AI Advisor", "Personal saving plan")}
      <section class="panel advisor-hero" aria-labelledby="advisor-priority-title">
        <div>
          <p class="eyebrow">Priority insight</p>
          <h3 id="advisor-priority-title">{escape(plan["priority"]["title"])}</h3>
          <p>{escape(plan["priority"]["body"])}</p>
        </div>
        <div class="advisor-impact">
          <span>{escape(plan["priority"]["impact_label"])}</span>
          <strong>{escape(plan["priority"]["impact_value"])}</strong>
        </div>
      </section>
      <div class="advisor-grid">
        <article class="panel advisor-card">
          <span>Monthly goal</span>
          <h3>{escape(format_goal_rate(monthly_goal["target_rate"]))}% target</h3>
          <p>{escape(monthly_goal["body"])}</p>
        </article>
        <article class="panel advisor-card">
          <span>Budget risk</span>
          <h3>{escape(budget_risk["title"])}</h3>
          <p>{escape(budget_risk["body"])}</p>
        </article>
        <article class="panel advisor-card">
          <span>Spending focus</span>
          <h3>{escape(spending_focus["title"])}</h3>
          <p>{escape(spending_focus["body"])}</p>
        </article>
      </div>
      <section class="panel advisor-actions" aria-labelledby="advisor-actions-title">
        <div class="panel-header"><h3 id="advisor-actions-title">Recommended next steps</h3></div>
        <ul class="advisor-action-list">{actions}</ul>
      </section>
    </section>
    """
    return layout("/recommendations", body)


def render_coach_history(coach_history: list[dict]) -> str:
    if not coach_history:
        return """
        <div class="empty-state coach-empty">
          Ask your first question to start a saved conversation with the hybrid coach.
        </div>
        """

    turns = []
    for entry in coach_history:
        provider_class = " fallback" if entry.get("fallback") else ""
        timestamp = format_chat_time(str(entry.get("created_at", "")))
        time_html = f"<span>{escape(timestamp)}</span>" if timestamp else ""
        fallback_note = (
            f'<p class="fallback-note">{escape(entry["fallback_reason"])}</p>'
            if entry.get("fallback_reason")
            else ""
        )
        evidence_items = "".join(f"<li>{escape(item)}</li>" for item in entry.get("evidence", [])[:3])
        evidence_html = f'<ul class="chat-evidence">{evidence_items}</ul>' if evidence_items else ""
        turns.append(
            f"""
            <article class="chat-turn">
              <div class="chat-bubble user">
                <strong>You</strong>
                {escape(entry["question"])}
              </div>
              <div class="chat-bubble assistant">
                <strong>{escape(entry["title"])}</strong>
                <p>{escape(entry["answer"])}</p>
                {fallback_note}
                {evidence_html}
                <div class="chat-meta">
                  <span class="coach-provider{provider_class}">{escape(entry["provider"])}</span>
                  {time_html}
                </div>
              </div>
            </article>
            """
        )

    return "\n".join(turns)


def render_coach(transactions: list[dict], budgets: list[dict], coach_history: list[dict], question: str = "") -> bytes:
    chat_history = render_coach_history(coach_history)
    clear_button = (
        """
        <form method="post" action="/coach/clear">
          <button class="secondary-button" type="submit">Clear chat</button>
        </form>
        """
        if coach_history
        else ""
    )
    body = f"""
    <section>
      {section_heading("AI Coach", "Hybrid financial coach")}
      <section class="panel coach-mode-note" aria-labelledby="coach-mode-title">
        <p class="eyebrow">Mixed AI mode</p>
        <h3 id="coach-mode-title">One coach, two ways to answer</h3>
        <p>
          The coach first tries to use the local Ollama model for more flexible conversations.
          If Ollama is not available, the app still answers with its own rule-based financial logic,
          using the current income, expenses, budgets and monthly balance.
        </p>
      </section>
      <div class="coach-grid">
        <form class="panel form-panel coach-question-card" method="post" action="/coach">
          <h3>Ask the hybrid coach</h3>
          <p class="coach-helper">
            Write a free question, choose your own wording and ask about spending,
            income, budgets, monthly goals or specific purchase decisions.
          </p>
          <label>
            Your question
            <textarea
              name="question"
              placeholder="Example: Which expense should I reduce first this month?"
            >{escape(question)}</textarea>
          </label>
          <button class="primary-button" type="submit">Ask coach</button>
        </form>
        <section class="panel coach-thread-panel" aria-labelledby="coach-thread-title">
          <div class="coach-thread-header">
            <div>
              <p class="eyebrow">Saved conversation</p>
              <h3 id="coach-thread-title">Coach history</h3>
              <p class="coach-helper">Scroll inside this box to review previous questions and answers.</p>
            </div>
            {clear_button}
          </div>
          <div class="coach-chat-window">
            {chat_history}
          </div>
        </section>
      </div>
      <div class="panel coach-prompts">
        <h3>How the user can interact with it</h3>
        <ul class="coach-capabilities">
          <li><strong>Free questions</strong>Ask naturally instead of selecting from fixed buttons.</li>
          <li><strong>Ollama mode</strong>Use the local model for more open and conversational answers when it is running.</li>
          <li><strong>Local fallback</strong>Get a reliable rule-based answer even when Ollama is not active.</li>
          <li><strong>Monthly savings</strong>Review income, expenses, balance, saving rate and monthly goals.</li>
          <li><strong>Budget checks</strong>Find which category is closest to its limit or already exceeded.</li>
          <li><strong>Purchase decisions</strong>Ask whether a planned expense fits the current financial situation.</li>
        </ul>
      </div>
      <div class="panel coach-prompts">
        <h3>Examples, not fixed buttons</h3>
        <p class="coach-helper">These are just ideas. The user can write their own question:</p>
        <ul class="sample-prompts">
          <li>How can I save more this month?</li>
          <li>Which budget is closest to the limit?</li>
          <li>Where am I spending too much?</li>
          <li>Can I afford a 30 euro dinner this week?</li>
          <li>What is my monthly balance?</li>
          <li>Which category should I reduce first?</li>
        </ul>
      </div>
    </section>
    """
    return layout("/coach", body)


class EstalviaHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        transactions, budgets, monthly_goals, coach_history = load_state()
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        if path == "/assets/logo.png":
            self.send_asset("logo.png")
        elif path == "/":
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
        elif path == "/monthly-review":
            self.send_html(render_monthly_review(transactions, monthly_goals))
        elif path == "/recommendations":
            self.send_html(render_recommendations(transactions, budgets, monthly_goals))
        elif path == "/coach":
            self.send_html(render_coach(transactions, budgets, coach_history))
        elif path == "/privacy":
            self.redirect("/")
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        transactions, budgets, monthly_goals, coach_history = load_state()
        parsed_url = urlparse(self.path)
        fields = self.read_form()

        if parsed_url.path == "/transactions":
            self.save_transaction(transactions, budgets, monthly_goals, coach_history, fields)
        elif parsed_url.path == "/budgets":
            self.save_budget(transactions, budgets, monthly_goals, coach_history, fields)
        elif parsed_url.path == "/monthly-review":
            self.save_monthly_goal(transactions, budgets, monthly_goals, coach_history, fields)
        elif parsed_url.path == "/coach":
            self.save_coach_message(transactions, budgets, monthly_goals, coach_history, fields)
        elif parsed_url.path == "/coach/clear":
            save_state(transactions, budgets, monthly_goals, [])
            self.redirect("/coach")
        elif parsed_url.path == "/reset":
            save_state(create_demo_transactions(), default_budgets(), create_demo_monthly_goals(), create_demo_coach_history())
            self.redirect("/")
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def save_transaction(
        self,
        transactions: list[dict],
        budgets: list[dict],
        monthly_goals: dict[str, float],
        coach_history: list[dict],
        fields: dict[str, str],
    ) -> None:
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

        save_state(transactions, budgets, monthly_goals, coach_history)
        self.redirect("/")

    def save_budget(
        self,
        transactions: list[dict],
        budgets: list[dict],
        monthly_goals: dict[str, float],
        coach_history: list[dict],
        fields: dict[str, str],
    ) -> None:
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

        save_state(transactions, budgets, monthly_goals, coach_history)
        self.redirect("/budgets")

    def save_monthly_goal(
        self,
        transactions: list[dict],
        budgets: list[dict],
        monthly_goals: dict[str, float],
        coach_history: list[dict],
        fields: dict[str, str],
    ) -> None:
        month_key = fields.get("month", "").strip()

        try:
            date.fromisoformat(f"{month_key}-01")
            target_rate = float(fields.get("target_rate", ""))
        except ValueError:
            self.send_html(render_monthly_review(transactions, monthly_goals, error="Use a valid month and saving goal."))
            return

        if target_rate < 0 or target_rate > 100:
            self.send_html(
                render_monthly_review(
                    transactions,
                    monthly_goals,
                    error="The saving goal must be between 0% and 100%.",
                )
            )
            return

        monthly_goals[month_key] = round(target_rate, 2)
        save_state(transactions, budgets, monthly_goals, coach_history)
        self.redirect("/monthly-review")

    def save_coach_message(
        self,
        transactions: list[dict],
        budgets: list[dict],
        monthly_goals: dict[str, float],
        coach_history: list[dict],
        fields: dict[str, str],
    ) -> None:
        question = fields.get("question", "").strip()
        if not question:
            self.send_html(render_coach(transactions, budgets, coach_history))
            return

        month_transactions = get_month_transactions(transactions)
        response = answer_with_hybrid_coach(
            month_transactions,
            budgets,
            question,
            model=OLLAMA_MODEL,
            api_url=OLLAMA_API_URL,
            timeout=OLLAMA_TIMEOUT,
        )
        coach_history.append(coach_history_entry(question, response))
        coach_history = normalize_coach_history(coach_history)
        save_state(transactions, budgets, monthly_goals, coach_history)
        self.send_html(render_coach(transactions, budgets, coach_history))

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

    def send_asset(self, filename: str) -> None:
        asset_path = ASSETS_DIR / filename
        if not asset_path.exists():
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content = asset_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "image/png")
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
