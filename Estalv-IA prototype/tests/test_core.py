import unittest
from datetime import date

from estalvia_core import (
    answer_financial_question,
    answer_with_hybrid_coach,
    build_advisor_plan,
    build_financial_context,
    build_budget_alerts,
    build_monthly_summaries,
    build_recommendations,
    build_transactions_csv,
    budget_status,
    clean_ai_text,
    create_demo_transactions,
    get_biggest_expense_of_month,
    get_budget_snapshots,
    get_expense_by_category,
    get_month_transactions,
    get_saving_rate,
    get_totals,
    normalize_monthly_goals,
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

    def test_monthly_summaries_track_savings_goal_by_month(self) -> None:
        transactions = [
            {"type": "income", "amount": 1000, "category": "Income", "date": "2026-04-01"},
            {"type": "expense", "amount": 850, "category": "Food", "date": "2026-04-02"},
            {"type": "income", "amount": 900, "category": "Income", "date": "2026-05-01"},
            {"type": "expense", "amount": 850, "category": "Transport", "date": "2026-05-03"},
        ]

        summaries = build_monthly_summaries(transactions, target_rate=10)

        self.assertEqual([summary["month"] for summary in summaries], ["2026-05", "2026-04"])
        self.assertEqual(summaries[0]["income"], 900.0)
        self.assertEqual(summaries[0]["expense"], 850.0)
        self.assertEqual(summaries[0]["status_label"], "Below target")
        self.assertEqual(summaries[1]["status_label"], "Goal met")

    def test_monthly_summaries_use_custom_goal_for_each_month(self) -> None:
        transactions = [
            {"type": "income", "amount": 1000, "category": "Income", "date": "2026-04-01"},
            {"type": "expense", "amount": 850, "category": "Food", "date": "2026-04-02"},
            {"type": "income", "amount": 900, "category": "Income", "date": "2026-05-01"},
            {"type": "expense", "amount": 730, "category": "Transport", "date": "2026-05-03"},
        ]

        summaries = build_monthly_summaries(
            transactions,
            target_rate=10,
            monthly_goals={"2026-04": 20, "2026-05": 15},
        )

        may_summary = summaries[0]
        april_summary = summaries[1]

        self.assertEqual(may_summary["target_rate"], 15)
        self.assertEqual(may_summary["target_amount"], 135.0)
        self.assertEqual(may_summary["status_label"], "Goal met")
        self.assertEqual(april_summary["target_rate"], 20)
        self.assertEqual(april_summary["target_amount"], 200.0)
        self.assertEqual(april_summary["status_label"], "Below target")

    def test_monthly_goals_ignore_invalid_values(self) -> None:
        goals = normalize_monthly_goals(
            {
                "2026-05": "12.5",
                "bad-month": 20,
                "2026-06": -5,
                "2026-07": 105,
            }
        )

        self.assertEqual(goals, {"2026-05": 12.5})

    def test_monthly_summaries_handle_month_without_income(self) -> None:
        transactions = [
            {"type": "expense", "amount": 45, "category": "Food", "date": "2026-05-02"},
        ]

        summaries = build_monthly_summaries(transactions)

        self.assertEqual(summaries[0]["status_label"], "No income")
        self.assertEqual(summaries[0]["target_amount"], 0.0)

    def test_budget_status_boundaries(self) -> None:
        self.assertEqual(budget_status(50, 100)["label"], "On track")
        self.assertEqual(budget_status(80, 100)["label"], "Warning")
        self.assertEqual(budget_status(120, 100)["label"], "Exceeded")

    def test_budget_snapshots_include_remaining_amount(self) -> None:
        budgets = [{"category": "Food", "limit": 100}]
        transactions = [
            {"type": "expense", "amount": 40, "category": "Food", "date": "2026-05-01"},
        ]

        snapshots = get_budget_snapshots(budgets, transactions)

        self.assertEqual(snapshots[0]["remaining"], 60.0)
        self.assertEqual(snapshots[0]["percentage"], 40)

    def test_recommendations_use_current_financial_state(self) -> None:
        transactions = create_demo_transactions(today=date(2026, 5, 13))

        titles = [recommendation["title"] for recommendation in build_recommendations(transactions)]

        self.assertIn("Reduce Housing by 10%", titles)
        self.assertIn("Automate a realistic saving transfer", titles)

    def test_recommendations_include_budget_alerts(self) -> None:
        budgets = [{"category": "Food", "limit": 100}]
        transactions = [
            {"type": "income", "amount": 1000, "category": "Income", "date": "2026-05-01"},
            {"type": "expense", "amount": 120, "category": "Food", "date": "2026-05-02"},
        ]

        titles = [recommendation["title"] for recommendation in build_recommendations(transactions, budgets)]

        self.assertIn("Food budget exceeded", titles)

    def test_advisor_plan_prioritizes_top_spending_with_goal_context(self) -> None:
        transactions = [
            {"type": "income", "amount": 1000, "category": "Income", "date": "2026-05-01"},
            {"type": "expense", "amount": 300, "category": "Food", "date": "2026-05-02"},
            {"type": "expense", "amount": 100, "category": "Leisure", "date": "2026-05-03"},
        ]

        plan = build_advisor_plan(
            transactions,
            [{"category": "Food", "limit": 500}],
            {"2026-05": 20},
            today=date(2026, 5, 12),
        )

        self.assertEqual(plan["priority"]["title"], "Reduce Food by 10%")
        self.assertEqual(plan["priority"]["impact_value"], "EUR 30.00")
        self.assertEqual(plan["monthly_goal"]["target_rate"], 20)
        self.assertEqual(plan["monthly_goal"]["status"], "ok")
        self.assertEqual(plan["spending_focus"]["title"], "Food")

    def test_clean_ai_text_removes_markdown_emphasis_markers(self) -> None:
        self.assertEqual(clean_ai_text("**Reduce Food first**"), "Reduce Food first")
        self.assertEqual(clean_ai_text("__Check budgets__"), "Check budgets")

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

    def test_get_biggest_expense_of_month_returns_largest_expense(self) -> None:
        transactions = [
            {
                "type": "income",
                "amount": 1000,
                "category": "Income",
                "date": "2026-05-01",
            },
            {
                "type": "expense",
                "amount": 40,
                "category": "Food",
                "date": "2026-05-03",
                "description": "Groceries",
            },
            {
                "type": "expense",
                "amount": 120,
                "category": "Shopping",
                "date": "2026-05-12",
                "description": "New headphones",
            },
            {
                "type": "expense",
                "amount": 20,
                "category": "Transport",
                "date": "2026-05-14",
                "description": "Metro card",
            },
        ]

        result = get_biggest_expense_of_month(
            transactions,
            today=date(2026, 5, 20),
        )

        self.assertEqual(result["amount"], 120)
        self.assertEqual(result["category"], "Shopping")
        self.assertEqual(result["description"], "New headphones")

    def test_financial_coach_answers_saving_questions_with_user_data(self) -> None:
        transactions = [
            {"type": "income", "amount": 1000, "category": "Income", "date": "2026-05-01"},
            {"type": "expense", "amount": 220, "category": "Food", "date": "2026-05-02"},
            {"type": "expense", "amount": 80, "category": "Transport", "date": "2026-05-03"},
        ]

        answer = answer_financial_question(transactions, [], "How can I save more this month?")

        self.assertEqual(answer["title"], "Best saving move")
        self.assertIn("Food", answer["answer"])
        self.assertIn("EUR 220.00", answer["answer"])

    def test_financial_coach_detects_budget_risk(self) -> None:
        budgets = [{"category": "Food", "limit": 100}]
        transactions = [
            {"type": "income", "amount": 900, "category": "Income", "date": "2026-05-01"},
            {"type": "expense", "amount": 120, "category": "Food", "date": "2026-05-02"},
        ]

        answer = answer_financial_question(transactions, budgets, "Which budget is at risk?")

        self.assertEqual(answer["title"], "Budget risk check")
        self.assertIn("Food budget exceeded", answer["answer"])

    def test_financial_context_summarizes_user_data_for_ai(self) -> None:
        budgets = [{"category": "Food", "limit": 100}]
        transactions = [
            {"type": "income", "amount": 900, "category": "Income", "date": "2026-05-01"},
            {"type": "expense", "amount": 120, "category": "Food", "date": "2026-05-02"},
        ]

        context = build_financial_context(transactions, budgets)

        self.assertIn("Monthly income: EUR 900.00", context)
        self.assertIn("Food: EUR 120.00", context)
        self.assertIn("Food: 100% used", context)

    def test_hybrid_coach_uses_ollama_when_available(self) -> None:
        transactions = [
            {"type": "income", "amount": 1000, "category": "Income", "date": "2026-05-01"},
            {"type": "expense", "amount": 200, "category": "Food", "date": "2026-05-02"},
        ]

        def fake_post(api_url: str, payload: dict, timeout: float) -> dict:
            self.assertEqual(api_url, "http://ollama.test/api/chat")
            self.assertEqual(payload["model"], "llama3.2")
            self.assertIn("Monthly income: EUR 1,000.00", payload["messages"][1]["content"])
            return {"message": {"content": "Reduce Food first and keep the remaining balance for savings."}}

        answer = answer_with_hybrid_coach(
            transactions,
            [],
            "How can I save?",
            api_url="http://ollama.test/api/chat",
            http_post=fake_post,
        )

        self.assertFalse(answer["fallback"])
        self.assertEqual(answer["provider"], "Ollama local model: llama3.2")
        self.assertIn("Reduce Food", answer["answer"])

    def test_hybrid_coach_falls_back_when_ollama_is_unavailable(self) -> None:
        transactions = [
            {"type": "income", "amount": 1000, "category": "Income", "date": "2026-05-01"},
            {"type": "expense", "amount": 200, "category": "Food", "date": "2026-05-02"},
        ]

        def failing_post(api_url: str, payload: dict, timeout: float) -> dict:
            raise OSError("Ollama is not running")

        answer = answer_with_hybrid_coach(
            transactions,
            [],
            "How can I save?",
            http_post=failing_post,
        )

        self.assertTrue(answer["fallback"])
        self.assertEqual(answer["provider"], "Local fallback")
        self.assertIn("Food", answer["answer"])


if __name__ == "__main__":
    unittest.main()
