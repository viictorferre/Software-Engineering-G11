from __future__ import annotations

import csv
from datetime import date
from io import StringIO
from uuid import uuid4

CATEGORIES = [
    "Food",
    "Transport",
    "Leisure",
    "Housing",
    "Studies",
    "Health",
    "Income",
    "Other",
]

DEFAULT_BUDGETS = [
    {"category": "Food", "limit": 260.0},
    {"category": "Transport", "limit": 90.0},
    {"category": "Leisure", "limit": 150.0},
    {"category": "Studies", "limit": 120.0},
]

CATEGORY_RULES = [
    {"category": "Food", "words": ["supermarket", "groceries", "food", "coffee", "restaurant", "shopping"]},
    {"category": "Transport", "words": ["metro", "bus", "train", "fuel", "taxi", "uber"]},
    {"category": "Leisure", "words": ["cinema", "dinner", "bar", "concert", "game"]},
    {"category": "Housing", "words": ["rent", "electricity", "water", "internet"]},
    {"category": "Studies", "words": ["university", "book", "material", "course"]},
    {"category": "Health", "words": ["pharmacy", "doctor", "gym"]},
]


def create_id() -> str:
    return str(uuid4())


def month_date(day: int, today: date | None = None) -> str:
    base = today or date.today()
    return date(base.year, base.month, day).isoformat()


def create_demo_transactions(today: date | None = None) -> list[dict]:
    return [
        {
            "id": create_id(),
            "type": "income",
            "amount": 850.0,
            "description": "Part-time job",
            "category": "Income",
            "date": month_date(1, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 42.7,
            "description": "Weekly groceries",
            "category": "Food",
            "date": month_date(3, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 18.5,
            "description": "Metro and bus",
            "category": "Transport",
            "date": month_date(4, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 32.0,
            "description": "Dinner with friends",
            "category": "Leisure",
            "date": month_date(4, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 64.9,
            "description": "University material",
            "category": "Studies",
            "date": month_date(5, today),
        },
    ]


def default_budgets() -> list[dict]:
    return [budget.copy() for budget in DEFAULT_BUDGETS]


def normalize_transactions(raw_transactions: object) -> list[dict]:
    if not isinstance(raw_transactions, list):
        return create_demo_transactions()

    transactions = []
    for raw in raw_transactions:
        if not isinstance(raw, dict):
            continue

        transaction_type = raw.get("type")
        category = raw.get("category")
        amount = raw.get("amount")
        description = str(raw.get("description", "")).strip()
        transaction_date = str(raw.get("date", "")).strip()

        if transaction_type not in {"income", "expense"}:
            continue
        if category not in CATEGORIES:
            category = "Other"

        try:
            amount = float(amount)
            date.fromisoformat(transaction_date)
        except (TypeError, ValueError):
            continue

        transactions.append(
            {
                "id": str(raw.get("id") or create_id()),
                "type": transaction_type,
                "amount": amount,
                "description": description or "Untitled transaction",
                "category": category,
                "date": transaction_date,
            }
        )

    return transactions or create_demo_transactions()


def normalize_budgets(raw_budgets: object) -> list[dict]:
    if not isinstance(raw_budgets, list):
        return default_budgets()

    budgets = []
    for raw in raw_budgets:
        if not isinstance(raw, dict):
            continue

        category = raw.get("category")
        if category not in CATEGORIES or category == "Income":
            continue

        try:
            limit = float(raw.get("limit"))
        except (TypeError, ValueError):
            continue

        if limit <= 0:
            continue

        budgets.append({"category": category, "limit": limit})

    return budgets or default_budgets()


def get_month_transactions(transactions: list[dict], today: date | None = None) -> list[dict]:
    base = today or date.today()
    month_transactions = []

    for transaction in transactions:
        try:
            transaction_date = date.fromisoformat(str(transaction["date"]))
        except (KeyError, ValueError):
            continue

        if transaction_date.year == base.year and transaction_date.month == base.month:
            month_transactions.append(transaction)

    return month_transactions


def get_totals(transactions: list[dict]) -> dict:
    income = 0.0
    expense = 0.0

    for transaction in transactions:
        amount = float(transaction.get("amount", 0))
        if transaction.get("type") == "income":
            income += amount
        else:
            expense += amount

    return {
        "income": round(income, 2),
        "expense": round(expense, 2),
        "balance": round(income - expense, 2),
    }


def get_saving_rate(totals: dict) -> int:
    income = totals.get("income", 0)
    if income <= 0:
        return 0

    return max(0, round((totals.get("balance", 0) / income) * 100))


def get_expense_by_category(transactions: list[dict]) -> dict[str, float]:
    summary: dict[str, float] = {}

    for transaction in transactions:
        if transaction.get("type") != "expense":
            continue

        category = str(transaction.get("category", "Other"))
        summary[category] = round(summary.get(category, 0.0) + float(transaction.get("amount", 0)), 2)

    return summary


def suggest_category(description: str, transaction_type: str) -> str:
    if transaction_type == "income":
        return "Income"

    text = description.lower()
    for rule in CATEGORY_RULES:
        if any(word in text for word in rule["words"]):
            return str(rule["category"])

    return "Other"


def sorted_transactions(transactions: list[dict]) -> list[dict]:
    return sorted(transactions, key=lambda transaction: str(transaction.get("date", "")), reverse=True)


def budget_status(spent: float, limit: float) -> dict:
    if limit <= 0:
        percentage = 100
    else:
        percentage = min(round((spent / limit) * 100), 100)

    if percentage >= 100:
        return {"percentage": percentage, "status": "danger", "label": "Exceeded"}
    if percentage >= 80:
        return {"percentage": percentage, "status": "warning", "label": "Warning"}
    return {"percentage": percentage, "status": "ok", "label": "On track"}


def get_budget_snapshots(budgets: list[dict], transactions: list[dict]) -> list[dict]:
    summary = get_expense_by_category(transactions)
    snapshots = []

    for budget in sorted(budgets, key=lambda item: item["category"]):
        spent = summary.get(budget["category"], 0.0)
        limit = float(budget["limit"])
        status = budget_status(spent, limit)

        snapshots.append(
            {
                "category": budget["category"],
                "spent": spent,
                "limit": limit,
                "remaining": round(limit - spent, 2),
                **status,
            }
        )

    return snapshots


def format_money(value: float) -> str:
    return f"EUR {value:,.2f}"


def format_transaction_date(value: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return value

    return parsed.strftime("%d %b %Y")


def build_recommendations(transactions: list[dict]) -> list[dict]:
    totals = get_totals(transactions)
    summary = get_expense_by_category(transactions)
    highest_category = None
    if summary:
        highest_category = sorted(summary.items(), key=lambda item: item[1], reverse=True)[0]

    recommendations = []

    if totals["income"] == 0:
        recommendations.append(
            {
                "title": "Register your income",
                "body": "Adding income allows the app to calculate your savings rate and detect whether the month is balanced.",
            }
        )

    if highest_category:
        category, amount = highest_category
        recommendations.append(
            {
                "title": f"Review {category}",
                "body": (
                    f"It is your highest spending category this month: {format_money(amount)}. "
                    f"Reducing it by 10% would free up {format_money(amount * 0.1)}."
                ),
            }
        )

    if totals["balance"] > 0:
        recommendations.append(
            {
                "title": "Automate a small goal",
                "body": f"You could set aside {format_money(totals['balance'] * 0.25)} this month.",
            }
        )
    elif totals["expense"] > totals["income"]:
        recommendations.append(
            {
                "title": "Prioritize variable expenses",
                "body": "Your balance is negative. Start by reviewing leisure, transport and small purchases.",
            }
        )

    recommendations.append(
        {
            "title": "Keep a weekly habit",
            "body": "A short weekly review prevents the budget from getting out of control at the end of the month.",
        }
    )

    return recommendations


def build_budget_alerts(budgets: list[dict], transactions: list[dict]) -> list[dict]:
    snapshots = get_budget_snapshots(budgets, transactions)
    alerts = []

    for snapshot in snapshots:
        category = snapshot["category"]
        label = snapshot["label"]
        spent = snapshot["spent"]
        limit = snapshot["limit"]
        remaining = snapshot["remaining"]

        if label == "Exceeded":
            alerts.append(
                {
                    "level": "danger",
                    "title": f"{category} budget exceeded",
                    "body": f"You have spent {format_money(spent)} out of {format_money(limit)}.",
                }
            )
        elif label == "Warning":
            alerts.append(
                {
                    "level": "warning",
                    "title": f"{category} budget almost reached",
                    "body": f"You only have {format_money(remaining)} left in this category.",
                }
            )

    return alerts

def build_transactions_csv(transactions: list[dict]) -> str:
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["Date", "Type", "Category", "Description", "Amount"])

    for transaction in sorted_transactions(transactions):
        writer.writerow(
            [
                transaction.get("date", ""),
                transaction.get("type", ""),
                transaction.get("category", ""),
                transaction.get("description", ""),
                transaction.get("amount", 0),
            ]
        )

    return output.getvalue()
