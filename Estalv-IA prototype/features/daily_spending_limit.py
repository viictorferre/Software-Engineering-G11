from __future__ import annotations

from calendar import monthrange
from datetime import date


def calculate_daily_spending_limit(balance: float, today: date | None = None) -> float:
    current_date = today or date.today()
    days_in_month = monthrange(current_date.year, current_date.month)[1]
    remaining_days = max(days_in_month - current_date.day + 1, 1)

    if balance <= 0:
        return 0.0

    return round(balance / remaining_days, 2)