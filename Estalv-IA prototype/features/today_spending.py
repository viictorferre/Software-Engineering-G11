from __future__ import annotations

from datetime import date


def calculate_today_spending(transactions: list[dict], today: date | None = None) -> float:
    """
    Calculate how much money the user has spent today.

    It only includes transactions where:
    - type is "expense"
    - date is today's date
    """
    current_date = today or date.today()
    total = 0.0

    for transaction in transactions:
        if transaction.get("type") != "expense":
            continue

        try:
            transaction_date = date.fromisoformat(str(transaction.get("date", "")))
        except ValueError:
            continue

        if transaction_date == current_date:
            total += float(transaction.get("amount", 0))

    return round(total, 2)