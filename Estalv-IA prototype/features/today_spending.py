from datetime import date


def calculate_today_spending(transactions: list[dict], today: date | None = None) -> float:
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
