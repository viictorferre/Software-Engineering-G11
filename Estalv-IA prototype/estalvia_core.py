import csv
import json
from datetime import date
from io import StringIO
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
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
    {"category": "Food", "limit": 105.0},
    {"category": "Transport", "limit": 65.0},
    {"category": "Leisure", "limit": 95.0},
    {"category": "Housing", "limit": 420.0},
    {"category": "Studies", "limit": 90.0},
    {"category": "Health", "limit": 70.0},
    {"category": "Other", "limit": 40.0},
]

DEFAULT_OLLAMA_MODEL = "llama3.2"
DEFAULT_OLLAMA_API_URL = "http://127.0.0.1:11434/api/chat"
DEFAULT_SAVINGS_TARGET_RATE = 10

CATEGORY_RULES = [
    {"category": "Food", "words": ["supermarket", "groceries", "food", "coffee", "restaurant", "shopping"]},
    {"category": "Transport", "words": ["metro", "bus", "train", "fuel", "taxi", "uber"]},
    {"category": "Leisure", "words": ["cinema", "dinner", "bar", "concert", "game"]},
    {"category": "Housing", "words": ["rent", "electricity", "water", "internet"]},
    {"category": "Studies", "words": ["university", "book", "material", "course"]},
    {"category": "Health", "words": ["pharmacy", "doctor", "gym"]},
]


def clean_ai_text(value: object) -> str:
    text = str(value or "").strip()
    return text.replace("**", "").replace("__", "")


def create_id() -> str:
    return str(uuid4())


def month_date(day: int, today: date | None = None) -> str:
    base = today or date.today()
    return date(base.year, base.month, day).isoformat()


def demo_month_date(month_offset: int, day: int, today: date | None = None) -> str:
    base = today or date.today()
    month_index = (base.year * 12) + base.month - 1 + month_offset
    year = month_index // 12
    month = (month_index % 12) + 1
    return date(year, month, day).isoformat()


def create_demo_transactions(today: date | None = None) -> list[dict]:
    return [
        {
            "id": create_id(),
            "type": "income",
            "amount": 1200.0,
            "description": "Part-time job",
            "category": "Income",
            "date": month_date(1, today),
        },
        {
            "id": create_id(),
            "type": "income",
            "amount": 250.0,
            "description": "Scholarship payment",
            "category": "Income",
            "date": month_date(2, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 390.0,
            "description": "Student room rent",
            "category": "Housing",
            "date": month_date(1, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 64.7,
            "description": "Weekly groceries",
            "category": "Food",
            "date": month_date(3, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 28.4,
            "description": "Lunch and coffee",
            "category": "Food",
            "date": month_date(3, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 45.0,
            "description": "Monthly metro pass",
            "category": "Transport",
            "date": month_date(2, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 22.0,
            "description": "Taxi after class project",
            "category": "Transport",
            "date": month_date(3, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 72.0,
            "description": "Dinner with friends",
            "category": "Leisure",
            "date": month_date(2, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 38.0,
            "description": "Cinema and snacks",
            "category": "Leisure",
            "date": month_date(3, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 86.0,
            "description": "University books",
            "category": "Studies",
            "date": month_date(5, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 28.0,
            "description": "Pharmacy",
            "category": "Health",
            "date": month_date(2, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 18.0,
            "description": "Streaming subscription",
            "category": "Other",
            "date": month_date(3, today),
        },
        {
            "id": create_id(),
            "type": "income",
            "amount": 1320.0,
            "description": "May salary",
            "category": "Income",
            "date": demo_month_date(-1, 1, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 410.0,
            "description": "May rent",
            "category": "Housing",
            "date": demo_month_date(-1, 1, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 210.0,
            "description": "May food shopping",
            "category": "Food",
            "date": demo_month_date(-1, 9, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 170.0,
            "description": "May leisure plan",
            "category": "Leisure",
            "date": demo_month_date(-1, 14, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 350.0,
            "description": "Laptop repair",
            "category": "Studies",
            "date": demo_month_date(-1, 18, today),
        },
        {
            "id": create_id(),
            "type": "income",
            "amount": 1250.0,
            "description": "April salary",
            "category": "Income",
            "date": demo_month_date(-2, 1, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 390.0,
            "description": "April rent",
            "category": "Housing",
            "date": demo_month_date(-2, 1, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 190.0,
            "description": "April groceries",
            "category": "Food",
            "date": demo_month_date(-2, 8, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 120.0,
            "description": "April transport",
            "category": "Transport",
            "date": demo_month_date(-2, 12, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 250.0,
            "description": "April leisure",
            "category": "Leisure",
            "date": demo_month_date(-2, 20, today),
        },
        {
            "id": create_id(),
            "type": "expense",
            "amount": 45.0,
            "description": "Old pharmacy purchase",
            "category": "Health",
            "date": demo_month_date(-3, 11, today),
        },
    ]


def create_demo_monthly_goals(today: date | None = None) -> dict[str, float]:
    return {
        demo_month_date(0, 1, today)[:7]: 20.0,
        demo_month_date(-1, 1, today)[:7]: 15.0,
        demo_month_date(-2, 1, today)[:7]: 20.0,
        demo_month_date(-3, 1, today)[:7]: 10.0,
    }


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


def normalize_monthly_goals(raw_goals: object) -> dict[str, float]:
    if not isinstance(raw_goals, dict):
        return {}

    goals: dict[str, float] = {}
    for raw_month, raw_rate in raw_goals.items():
        month_key = str(raw_month).strip()
        try:
            date.fromisoformat(f"{month_key}-01")
            target_rate = float(raw_rate)
        except (TypeError, ValueError):
            continue

        if target_rate < 0 or target_rate > 100:
            continue

        goals[month_key] = round(target_rate, 2)

    return goals


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


def build_monthly_summaries(
    transactions: list[dict],
    target_rate: float = DEFAULT_SAVINGS_TARGET_RATE,
    monthly_goals: dict[str, float] | None = None,
) -> list[dict]:
    grouped_transactions: dict[str, list[dict]] = {}

    for transaction in transactions:
        try:
            transaction_date = date.fromisoformat(str(transaction["date"]))
        except (KeyError, ValueError):
            continue

        month_key = transaction_date.strftime("%Y-%m")
        grouped_transactions.setdefault(month_key, []).append(transaction)

    summaries = []
    for month_key, month_items in grouped_transactions.items():
        month_date_value = date.fromisoformat(f"{month_key}-01")
        totals = get_totals(month_items)
        saving_rate = get_saving_rate(totals)
        month_target_rate = target_rate
        if monthly_goals and month_key in monthly_goals:
            month_target_rate = monthly_goals[month_key]

        target_amount = round(totals["income"] * (month_target_rate / 100), 2)
        gap = round(totals["balance"] - target_amount, 2)

        if totals["income"] <= 0:
            status = "neutral"
            status_label = "No income"
            progress = 0
        elif gap >= 0:
            status = "ok"
            status_label = "Goal met"
            progress = 100
        else:
            status = "warning"
            status_label = "Below target"
            progress = max(0, min(round((totals["balance"] / target_amount) * 100), 100)) if target_amount else 0

        summaries.append(
            {
                "month": month_key,
                "label": month_date_value.strftime("%B %Y"),
                "income": totals["income"],
                "expense": totals["expense"],
                "balance": totals["balance"],
                "saving_rate": saving_rate,
                "target_rate": month_target_rate,
                "target_amount": target_amount,
                "gap": gap,
                "status": status,
                "status_label": status_label,
                "progress": progress,
                "transaction_count": len(month_items),
            }
        )

    return sorted(summaries, key=lambda item: item["month"], reverse=True)


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


def build_recommendations(transactions: list[dict], budgets: list[dict] | None = None) -> list[dict]:
    totals = get_totals(transactions)
    summary = get_expense_by_category(transactions)
    highest_category = None
    if summary:
        highest_category = sorted(summary.items(), key=lambda item: item[1], reverse=True)[0]

    recommendations = []
    saving_rate = get_saving_rate(totals)

    if totals["income"] == 0:
        recommendations.append(
            {
                "title": "Add income to unlock your plan",
                "body": (
                    "The advisor needs this month's income to calculate savings capacity "
                    "and detect whether spending is balanced."
                ),
            }
        )
        recommendations.append(
            {
                "title": "Start with category tracking",
                "body": (
                    "Keep adding expenses by category so the advisor can identify "
                    "the habits with the biggest saving potential."
                ),
            }
        )
        return recommendations

    if highest_category:
        category, amount = highest_category
        reduction = amount * 0.1
        share = round((amount / totals["income"]) * 100)
        recommendations.append(
            {
                "title": f"Reduce {category} by 10%",
                "body": (
                    f"This is your highest spending category at {format_money(amount)} "
                    f"({share}% of income). A 10% reduction would free up {format_money(reduction)}."
                ),
            }
        )

    if budgets:
        for alert in build_budget_alerts(budgets, transactions):
            recommendations.append(
                {
                    "title": alert["title"],
                    "body": f"{alert['body']} Prioritize this before adding new discretionary spending.",
                }
            )

    if totals["balance"] > 0:
        suggested_saving = totals["balance"] * 0.25
        recommendations.append(
            {
                "title": "Automate a realistic saving transfer",
                "body": (
                    f"Your current balance is positive. Move {format_money(suggested_saving)} "
                    "to savings now and keep the rest available for the month."
                ),
            }
        )
    elif totals["expense"] > totals["income"]:
        gap = totals["expense"] - totals["income"]
        recommendations.append(
            {
                "title": "Close the monthly gap first",
                "body": (
                    f"Expenses are {format_money(gap)} above income. Pause non-essential spending "
                    "until the balance is back above zero."
                ),
            }
        )

    if saving_rate < 10 and totals["balance"] > 0:
        target_balance = totals["income"] * 0.1
        extra_needed = max(0, target_balance - totals["balance"])
        recommendations.append(
            {
                "title": "Aim for a 10% savings rate",
                "body": (
                    f"Your estimated savings rate is {saving_rate}%. Freeing up "
                    f"{format_money(extra_needed)} would put you close to a healthier 10% target."
                ),
            }
        )

    recommendations.append(
        {
            "title": "Review the plan weekly",
            "body": "A short weekly review keeps budgets realistic and helps the advisor adapt before the end of the month.",
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


def build_advisor_plan(
    transactions: list[dict],
    budgets: list[dict] | None = None,
    monthly_goals: dict[str, float] | None = None,
    today: date | None = None,
) -> dict:
    budgets = budgets or []
    base = today or date.today()
    month_key = base.strftime("%Y-%m")
    totals = get_totals(transactions)
    saving_rate = get_saving_rate(totals)
    category_summary = get_expense_by_category(transactions)
    budget_snapshots = get_budget_snapshots(budgets, transactions)
    budget_alerts = build_budget_alerts(budgets, transactions)
    target_rate = (monthly_goals or {}).get(month_key, DEFAULT_SAVINGS_TARGET_RATE)
    target_amount = round(totals["income"] * (target_rate / 100), 2)
    saving_gap = round(max(0, target_amount - totals["balance"]), 2)

    top_category = None
    if category_summary:
        top_category = sorted(category_summary.items(), key=lambda item: item[1], reverse=True)[0]

    riskiest_budget = None
    if budget_snapshots:
        riskiest_budget = sorted(budget_snapshots, key=lambda item: item["percentage"], reverse=True)[0]

    if totals["income"] <= 0:
        priority = {
            "title": "Add income to activate the plan",
            "body": "The advisor needs this month's income before it can measure saving capacity or budget pressure.",
            "impact_label": "Next step",
            "impact_value": "Register income",
        }
        actions = [
            "Add this month's income.",
            "Register at least three expenses with categories.",
            "Create limits for the categories you use most.",
        ]
    elif budget_alerts:
        alert = budget_alerts[0]
        priority = {
            "title": alert["title"],
            "body": f"{alert['body']} Control this before adding new discretionary spending.",
            "impact_label": "Immediate focus",
            "impact_value": "Protect budget",
        }
        actions = [
            "Pause new spending in the risky category for the next few days.",
            "Move planned purchases to a category with more remaining budget.",
            "Check the budget again after the next transaction.",
        ]
    elif saving_gap > 0:
        priority = {
            "title": "Close the monthly saving gap",
            "body": f"You need {format_money(saving_gap)} more positive balance to reach this month's saving goal.",
            "impact_label": "Needed to goal",
            "impact_value": format_money(saving_gap),
        }
        actions = [
            "Reduce one flexible expense this week.",
            "Avoid creating new non-essential transactions until the gap is smaller.",
            "Use the AI Coach to test whether a planned purchase fits the goal.",
        ]
    elif top_category:
        category, amount = top_category
        estimated_saving = round(amount * 0.1, 2)
        priority = {
            "title": f"Reduce {category} by 10%",
            "body": f"{category} is the highest spending area this month at {format_money(amount)}.",
            "impact_label": "Estimated saving",
            "impact_value": format_money(estimated_saving),
        }
        actions = [
            f"Set a short weekly cap for {category}.",
            f"Try to reduce {category} by about {format_money(estimated_saving)} this month.",
            "Review the impact after adding the next expense.",
        ]
    else:
        priority = {
            "title": "Keep building the spending picture",
            "body": "There is not enough expense data yet to detect a strong saving opportunity.",
            "impact_label": "Next step",
            "impact_value": "Add expenses",
        }
        actions = [
            "Add expenses as soon as they happen.",
            "Create budgets for the categories you expect to use.",
            "Return to the advisor after the first week of data.",
        ]

    if totals["income"] <= 0:
        goal_body = "Add income before evaluating the monthly saving target."
        goal_status = "neutral"
    elif saving_gap == 0:
        goal_body = f"You are meeting the {target_rate:g}% saving goal for this month."
        goal_status = "ok"
    else:
        goal_body = f"You still need {format_money(saving_gap)} to reach the {target_rate:g}% saving goal."
        goal_status = "warning"

    if riskiest_budget:
        budget_body = (
            f"{riskiest_budget['category']} is at {riskiest_budget['percentage']}% "
            f"with {format_money(riskiest_budget['remaining'])} remaining."
        )
        budget_status_label = riskiest_budget["label"]
    else:
        budget_body = "No category budgets have been created yet."
        budget_status_label = "No budgets"

    if top_category:
        category, amount = top_category
        share = round((amount / totals["expense"]) * 100) if totals["expense"] else 0
        spending_body = f"{category} leads spending at {format_money(amount)}, about {share}% of expenses."
        spending_title = category
    else:
        spending_body = "No expenses have been registered for the current month."
        spending_title = "No expense focus"

    return {
        "priority": priority,
        "monthly_goal": {
            "title": "Monthly goal",
            "body": goal_body,
            "status": goal_status,
            "target_rate": target_rate,
            "target_amount": target_amount,
            "saving_gap": saving_gap,
            "saving_rate": saving_rate,
        },
        "budget_risk": {
            "title": budget_status_label,
            "body": budget_body,
            "category": riskiest_budget["category"] if riskiest_budget else "",
            "percentage": riskiest_budget["percentage"] if riskiest_budget else 0,
        },
        "spending_focus": {
            "title": spending_title,
            "body": spending_body,
        },
        "actions": actions,
        "totals": totals,
    }


def answer_financial_question(transactions: list[dict], budgets: list[dict], question: str) -> dict:
    totals = get_totals(transactions)
    saving_rate = get_saving_rate(totals)
    category_summary = get_expense_by_category(transactions)
    budget_snapshots = get_budget_snapshots(budgets, transactions)
    budget_alerts = build_budget_alerts(budgets, transactions)
    text = question.lower().strip()

    if not text:
        return {
            "title": "Ask your finance coach",
            "answer": "Write a question about savings, spending, budgets or income and I will use this month's data to answer.",
            "evidence": [
                f"Income: {format_money(totals['income'])}",
                f"Expenses: {format_money(totals['expense'])}",
                f"Savings rate: {saving_rate}%",
            ],
        }

    highest_category = None
    if category_summary:
        highest_category = sorted(category_summary.items(), key=lambda item: item[1], reverse=True)[0]

    if any(word in text for word in ["save", "saving", "ahorro", "ahorrar"]):
        if highest_category:
            category, amount = highest_category
            reduction = amount * 0.1
            answer = (
                f"Start with {category}. It is your highest expense at {format_money(amount)} this month. "
                f"Reducing it by 10% would free up around {format_money(reduction)} without changing the full budget."
            )
        elif totals["income"] > 0:
            answer = (
                "You have income registered, but not enough expense data yet. "
                "Add more expenses so I can find the best saving opportunity."
            )
        else:
            answer = (
                "Add this month's income first. Once income exists, I can compare it "
                "with expenses and suggest a realistic saving target."
            )

        return {
            "title": "Best saving move",
            "answer": answer,
            "evidence": [
                f"Balance: {format_money(totals['balance'])}",
                f"Savings rate: {saving_rate}%",
                f"Expenses: {format_money(totals['expense'])}",
            ],
        }

    if any(word in text for word in ["budget", "presupuesto", "limit", "risk", "riesgo", "alert"]):
        if budget_alerts:
            first_alert = budget_alerts[0]
            answer = f"{first_alert['title']}. {first_alert['body']} This is the first area I would control before new spending."
        elif budget_snapshots:
            closest = sorted(budget_snapshots, key=lambda item: item["percentage"], reverse=True)[0]
            answer = (
                f"The closest budget to its limit is {closest['category']} at {closest['percentage']}%. "
                f"You still have {format_money(closest['remaining'])} available in that category."
            )
        else:
            answer = "No budgets have been created yet. Add limits by category so I can warn you before overspending."

        return {
            "title": "Budget risk check",
            "answer": answer,
            "evidence": [f"{item['category']}: {item['percentage']}% used" for item in budget_snapshots[:4]],
        }

    if any(word in text for word in ["expense", "spending", "gasto", "gastos", "category", "categoria"]):
        if category_summary:
            top_categories = sorted(category_summary.items(), key=lambda item: item[1], reverse=True)[:3]
            details = ", ".join(f"{category} ({format_money(amount)})" for category, amount in top_categories)
            answer = (
                f"Your main spending areas this month are {details}. "
                "I would review the first one before changing smaller habits."
            )
        else:
            answer = "There are no expenses for this month yet. Add expenses to see which category has the biggest impact."

        return {
            "title": "Spending analysis",
            "answer": answer,
            "evidence": [
                f"{category}: {format_money(amount)}"
                for category, amount in sorted(
                    category_summary.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )[:4]
            ],
        }

    if any(word in text for word in ["income", "ingreso", "salary", "balance", "saldo"]):
        if totals["balance"] >= 0:
            answer = (
                f"Your monthly balance is positive at {format_money(totals['balance'])}. "
                f"That gives you a savings rate of {saving_rate}% based on the current data."
            )
        else:
            answer = (
                f"Your monthly balance is negative at {format_money(totals['balance'])}. "
                "The priority should be reducing flexible expenses or adding income before setting a saving target."
            )

        return {
            "title": "Monthly balance",
            "answer": answer,
            "evidence": [
                f"Income: {format_money(totals['income'])}",
                f"Expenses: {format_money(totals['expense'])}",
                f"Balance: {format_money(totals['balance'])}",
            ],
        }

    recommendations = build_recommendations(transactions, budgets)
    first = recommendations[0]
    return {
        "title": "Finance coach summary",
        "answer": f"{first['title']}: {first['body']}",
        "evidence": [
            f"Income: {format_money(totals['income'])}",
            f"Expenses: {format_money(totals['expense'])}",
            f"Savings rate: {saving_rate}%",
        ],
    }


def build_financial_context(transactions: list[dict], budgets: list[dict]) -> str:
    totals = get_totals(transactions)
    saving_rate = get_saving_rate(totals)
    summary = get_expense_by_category(transactions)
    snapshots = get_budget_snapshots(budgets, transactions)

    lines = [
        f"Monthly income: {format_money(totals['income'])}",
        f"Monthly expenses: {format_money(totals['expense'])}",
        f"Monthly balance: {format_money(totals['balance'])}",
        f"Estimated savings rate: {saving_rate}%",
    ]

    if summary:
        lines.append("Expenses by category:")
        for category, amount in sorted(summary.items(), key=lambda item: item[1], reverse=True):
            lines.append(f"- {category}: {format_money(amount)}")

    if snapshots:
        lines.append("Budget status:")
        for snapshot in snapshots:
            lines.append(
                f"- {snapshot['category']}: {snapshot['percentage']}% used, "
                f"{format_money(snapshot['remaining'])} remaining, status {snapshot['label']}"
            )

    return "\n".join(lines)


def _post_ollama_chat(api_url: str, payload: dict, timeout: float) -> dict:
    request = Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def answer_with_hybrid_coach(
    transactions: list[dict],
    budgets: list[dict],
    question: str,
    model: str = DEFAULT_OLLAMA_MODEL,
    api_url: str = DEFAULT_OLLAMA_API_URL,
    timeout: float = 45.0,
    http_post=_post_ollama_chat,
) -> dict:
    if not question.strip():
        local_response = answer_financial_question(transactions, budgets, question)
        return {
            **local_response,
            "provider": "Local rules",
            "fallback": False,
        }

    context = build_financial_context(transactions, budgets)
    payload = {
        "model": model,
        "stream": False,
        "options": {
            "temperature": 0.3,
        },
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Estalv-IA AI Coach, a personal finance assistant for students and young adults. "
                    "Answer only using the financial context provided by the app. Be practical, concise and specific. "
                    "Do not claim to be a certified financial advisor. If the question is outside personal finance, "
                    "briefly redirect the user to ask about savings, spending, budgets or monthly balance."
                ),
            },
            {
                "role": "user",
                "content": f"Financial context:\n{context}\n\nUser question:\n{question.strip()}",
            },
        ],
    }

    try:
        raw_response = http_post(api_url, payload, timeout)
        answer = str(raw_response["message"]["content"]).strip()
        if not answer:
            raise ValueError("Ollama returned an empty answer")

        return {
            "title": "Ollama AI Coach",
            "answer": answer,
            "evidence": build_coach_evidence(transactions, budgets),
            "provider": f"Ollama local model: {model}",
            "fallback": False,
        }
    except (HTTPError, URLError, OSError, TimeoutError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        local_response = answer_financial_question(transactions, budgets, question)
        return {
            **local_response,
            "provider": "Local fallback",
            "fallback": True,
            "fallback_reason": f"Ollama was not available ({error.__class__.__name__}).",
        }


def build_coach_evidence(transactions: list[dict], budgets: list[dict]) -> list[str]:
    totals = get_totals(transactions)
    saving_rate = get_saving_rate(totals)
    summary = get_expense_by_category(transactions)
    snapshots = get_budget_snapshots(budgets, transactions)
    evidence = [
        f"Income: {format_money(totals['income'])}",
        f"Expenses: {format_money(totals['expense'])}",
        f"Balance: {format_money(totals['balance'])}",
        f"Savings rate: {saving_rate}%",
    ]

    if summary:
        category, amount = sorted(summary.items(), key=lambda item: item[1], reverse=True)[0]
        evidence.append(f"Top category: {category} ({format_money(amount)})")

    if snapshots:
        highest_budget = sorted(snapshots, key=lambda item: item["percentage"], reverse=True)[0]
        evidence.append(f"Highest budget usage: {highest_budget['category']} at {highest_budget['percentage']}%")

    return evidence


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


def get_biggest_expense_of_month(
    transactions: list[dict],
    today: date | None = None,
) -> dict | None:
    base = today or date.today()
    month_transactions = get_month_transactions(transactions, base)

    expenses = [
        transaction
        for transaction in month_transactions
        if transaction["type"] == "expense"
    ]

    if not expenses:
        return None

    biggest_expense = max(expenses, key=lambda transaction: transaction["amount"])

    return {
        "amount": biggest_expense["amount"],
        "category": biggest_expense["category"],
        "date": biggest_expense["date"],
        "description": biggest_expense.get("description", ""),
    }
