# Testing

The tests focus on the behaviour that matters for the app: transactions, budgets, monthly summaries and saving advice.

## Automated Tests

Run:

```powershell
python -m unittest discover -s tests
```

The test suite checks:

- Category suggestions.
- Monthly totals and saving rate.
- Expense summaries by category.
- Budget status and alert messages.
- Monthly review with custom goals.
- CSV export.
- AI Advisor plan generation.
- AI Coach local fallback and Ollama response handling.

## Manual Demo Check

Before presenting:

1. Run `python app.py`.
2. Open `http://127.0.0.1:8000`.
3. Click `Restore demo`.
4. Check that the dashboard shows alerts, latest movements and category spending.
5. Check `Budgets`, `Monthly Review`, `AI Advisor` and `AI Coach`.
6. Confirm that the coach history scrolls and can be cleared.

Expected result: the app can be presented without creating data manually.

## Main User Flow Checks

| Flow | What to check |
|---|---|
| Transactions | Add income and expenses, then confirm dashboard values update. |
| Categories | Use `Auto suggest` and confirm common descriptions are categorized correctly. |
| Budgets | Create or update a monthly limit and check the status badge. |
| Monthly Review | Compare previous months and update one saving goal. |
| AI Advisor | Confirm that it uses current income, expenses, budgets and saving goal. |
| AI Coach | Ask a finance question and confirm the answer uses the current data. |

## CI

GitHub Actions runs on push and pull request. It compiles the Python files and runs the unit tests.
