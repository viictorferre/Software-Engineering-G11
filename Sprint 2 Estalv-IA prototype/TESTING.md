# Sprint 2 Testing

This file documents the functional checks used to validate the Sprint 2 prototype.

## Expense Tracking Test

Goal: confirm that users can register expenses and see them reflected in the app.

Steps:

1. Open `index.html` in a browser.
2. Go to `Transactions`.
3. Select `Expense`.
4. Enter an amount, description, category and date.
5. Click `Save transaction`.
6. Confirm that the app returns to `Dashboard`.
7. Confirm that total expenses increase.
8. Confirm that the new expense appears in `Latest movements` and `History`.
9. Confirm that the expense category appears in `Expenses by category`.

Expected result: the expense is saved in localStorage and all dashboard values update immediately.

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
4. Confirm that the suggested category changes automatically.

Expected result: the app suggests the category before the transaction is saved, and the user can still change it manually.

## Browser Smoke Test

A browser smoke test was run with Microsoft Edge in headless mode. It verified that the app loads, opens the transaction view, saves an expense and returns to the dashboard without console errors.
