from __future__ import annotations

import unittest
from datetime import date

from estalvia_core import (
    build_budget_alerts,
    build_recommendations,
    build_transactions_csv,
    budget_status,
    create_demo_transactions,
    get_budget_snapshots,
    get_expense_by_category,
    get_month_transactions,
    get_saving_rate,
    get_totals,
    suggest_category,
)


class EstalviaCoreTest(unittest.TestCase):
    def test_category_suggestion_matches_rules(self) -> None:
        self.assertEqual(suggest_category("coffee before class", "expense"), "Food")
        self.assertEqual(suggest_category("metro ticket", "expense"), "Transport")
        self.assertEqual(suggest_category("salary", "income"), "Income")
        self.assertEqual(suggest_category("unknown thing", "expense"), "Other")

    def test_totals_and_saving_rate(self) -> None:
        transactions = [
            {"type": "income", "amount": 1000, "category": "Income", "date": "2026-05-01"},
            {"type": "expense", "amount": 250, "category": "Food", "date": "2026-05-02"},
        ]

        totals = get_totals(transactions)

        self.assertEqual(totals, {"income": 1000.0, "expense": 250.0, "balance": 750.0})
        self.assertEqual(get_saving_rate(totals), 75)

    def test_month_filter_and_expense_summary(self) -> None:
        transactions = [
            {"type": "expense", "amount": 15, "category": "Food", "date": "2026-05-02"},
            {"type": "expense", "amount": 5, "category": "Food", "date": "2026-05-03"},
            {"type": "expense", "amount": 20, "category": "Leisure", "date": "2026-04-30"},
        ]

        may_transactions = get_month_transactions(transactions, today=date(2026, 5, 13))

        self.assertEqual(len(may_transactions), 2)
        self.assertEqual(get_expense_by_category(may_transactions), {"Food": 20.0})

    def test_budget_status_boundaries(self) -> None:
        self.assertEqual(budget_status(50, 100)["label"], "On track")
        self.assertEqual(budget_status(80, 100)["label"], "Warning")
        self.assertEqual(budget_status(120, 100)["label"], "Exceeded")

    def test_budget_snapshots_include_remaining_amount(self) -> None:
        budgets = [{"category": "Food", "limit": 100}]
        transactions = [{"type": "expense", "amount": 40, "category": "Food", "date": "2026-05-01"}]

        snapshots = get_budget_snapshots(budgets, transactions)

        self.assertEqual(snapshots[0]["remaining"], 60.0)
        self.assertEqual(snapshots[0]["percentage"], 40)

    def test_recommendations_use_current_financial_state(self) -> None:
        transactions = create_demo_transactions(today=date(2026, 5, 13))

        titles = [recommendation["title"] for recommendation in build_recommendations(transactions)]

        self.assertIn("Review Studies", titles)
        self.assertIn("Automate a small goal", titles)


    def test_budget_alerts_warn_and_exceeded_budgets(self) -> None:
        budgets = [
            {"category": "Food", "limit": 100},
            {"category": "Transport", "limit": 50},
        ]
        transactions = [
            {"type": "expense", "amount": 85, "category": "Food", "date": "2026-05-01"},
            {"type": "expense", "amount": 70, "category": "Transport", "date": "2026-05-02"},
        ]

        alerts = build_budget_alerts(budgets, transactions)
        titles = [alert["title"] for alert in alerts]

        self.assertIn("Food budget almost reached", titles)
        self.assertIn("Transport budget exceeded", titles)

    def test_budget_alerts_not_triggered_below_warning_threshold(self) -> None:
        budgets = [{"category": "Food", "limit": 100}]
        transactions = [
            {"type": "expense", "amount": 40, "category": "Food", "date": "2026-05-01"},
        ]

        alerts = build_budget_alerts(budgets, transactions)

        self.assertEqual(alerts, [])

    def test_budget_alert_message_for_warning_budget(self) -> None:
        budgets = [{"category": "Food", "limit": 100}]
        transactions = [
            {"type": "expense", "amount": 85, "category": "Food", "date": "2026-05-01"},
        ]

        alerts = build_budget_alerts(budgets, transactions)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["level"], "warning")
        self.assertEqual(alerts[0]["title"], "Food budget almost reached")
        self.assertIn("EUR 15.00 left", alerts[0]["body"])

    def test_budget_alert_message_for_exceeded_budget(self) -> None:
        budgets = [{"category": "Transport", "limit": 50}]
        transactions = [
            {"type": "expense", "amount": 70, "category": "Transport", "date": "2026-05-01"},
        ]

        alerts = build_budget_alerts(budgets, transactions)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["level"], "danger")
        self.assertEqual(alerts[0]["title"], "Transport budget exceeded")
        self.assertIn("EUR 70.00 out of EUR 50.00", alerts[0]["body"])

    def test_transactions_can_be_exported_to_csv(self) -> None:
        transactions = [
            {
                "type": "income",
                "amount": 1000,
                "category": "Income",
                "description": "Salary",
                "date": "2026-05-01",
            },
            {
                "type": "expense",
                "amount": 25.5,
                "category": "Food",
                "description": "Lunch",
                "date": "2026-05-02",
            },
        ]

        csv_content = build_transactions_csv(transactions)

        self.assertIn("Date,Type,Category,Description,Amount", csv_content)
        self.assertIn("2026-05-02,expense,Food,Lunch,25.5", csv_content)
        self.assertIn("2026-05-01,income,Income,Salary,1000", csv_content)
        
               
if __name__ == "__main__":
    unittest.main()
