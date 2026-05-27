# Python Prototype Testing

This file documents the checks used to validate the Python version of Estalv-IA. The tests are written around the behaviour that users actually see in the app: transactions, monthly totals, budgets and saving advice.

## Automated Tests

Run:

```powershell
python -m unittest discover -s tests
```

Expected result: all tests pass.

The tests validate:

- Category suggestions for common descriptions such as `coffee`, `metro` and income.
- Monthly income, expense, balance and saving-rate calculations.
- Monthly transaction filtering.
- Expense totals by category.
- Budget status changes from `On track` to `Warning` and `Exceeded`.
- AI-assisted recommendation generation from the current financial state and budget alerts.

## Manual Browser Checks

Run:

```powershell
python app.py
```

Open `http://127.0.0.1:8000`.

## Expense Tracking Test

Goal: confirm that users can register expenses and see them reflected in the app.

Steps:

1. Open the app in the browser.
2. Go to `Transactions`.
3. Select `Expense`.
4. Enter an amount, description, category or `Auto suggest`, and date.
5. Click `Save transaction`.
6. Confirm that the app returns to `Dashboard`.
7. Confirm that total expenses increase.
8. Confirm that the new expense appears in `Latest movements` and `History`.
9. Confirm that the expense category appears in `Expenses by category`.

Expected result: the expense is saved in local JSON storage and all dashboard values update.

## Income Tracking Test

Goal: confirm that users can register income and see the monthly overview update.

Steps:

1. Go to `Transactions`.
2. Select `Income`.
3. Enter an amount, description and date.
4. Click `Save transaction`.
5. Confirm that total income and balance increase.

Expected result: the income is saved and included in the monthly overview.

## Budget Limit Test

Goal: confirm that users can define a budget limit and receive visual feedback.

Steps:

1. Go to `Budgets`.
2. Select a category.
3. Enter a monthly limit.
4. Click `Save budget`.
5. Add expenses for that category from `Transactions`.
6. Return to `Budgets`.
7. Confirm that the spent amount, remaining amount and status badge update.

Expected result: budget status changes from `On track` to `Warning` near the limit and `Exceeded` after passing it.

## Category Suggestion Test

Goal: confirm that expense categorization reduces manual work.

Steps:

1. Go to `Transactions`.
2. Select `Expense`.
3. Type a description such as `coffee`, `metro`, `dinner` or `university book`.
4. Leave category as `Auto suggest`.
5. Click `Save transaction`.
6. Confirm that the saved transaction uses the expected category.

Expected result: the Python logic suggests and saves the category automatically, while still allowing the user to choose a category manually.

## AI Advisor Test

Goal: confirm that the public recommendations page gives personalized saving suggestions.

Steps:

1. Add an income transaction.
2. Add expenses in at least one category.
3. Add a budget limit and enough expenses to trigger a warning or exceeded state.
4. Go to `AI Advisor`.
5. Confirm that the page suggests a category reduction, a saving transfer or a budget-focused action.

Expected result: the advisor uses the current month data and does not require the internal Privacy page.