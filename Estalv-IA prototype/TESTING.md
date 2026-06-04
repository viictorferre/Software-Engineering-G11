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
- Monthly review summaries, custom monthly saving goals and saving target status.
- AI-assisted recommendation, hybrid coach answer generation and Ollama fallback behaviour from the current financial state and budget alerts.

## Manual Browser Checks

Run:

```powershell
python app.py
```

Open `http://127.0.0.1:8000`.

## Final Demo Data Check

Goal: confirm that the presentation demo shows all main product features.

Steps:

1. Click `Restore demo` on the dashboard.
2. Confirm that the dashboard shows budget alerts and current-month category spending.
3. Go to `Budgets` and confirm that some categories are near or over their limits.
4. Go to `Monthly Review` and confirm that several previous months appear with different saving goals.
5. Go to `AI Advisor` and confirm that it shows a priority insight and recommended next steps.
6. Go to `AI Coach` and confirm that a saved conversation appears inside the scrollable chat box.

Expected result: the app is ready for a live walkthrough without manually creating data during the presentation.

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

## Monthly Review Test

Goal: confirm that users can compare monthly income, expenses and saving target progress.

Steps:

1. Add income and expenses using dates from at least two different months.
2. Go to `Monthly Review`.
3. Confirm that each month appears as a separate card.
4. Confirm that income, expenses, balance, savings rate and target are shown.
5. Change the saving goal for one month and click `Update goal`.
6. Confirm that only that month uses the new target percentage.
7. Confirm that the card says `Goal met` when balance reaches the configured monthly target and `Below target` otherwise.

Expected result: previous months are summarized clearly, each month can keep its own saving objective and the status is visible.

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

Goal: confirm that the public advisor page gives a structured saving plan.

Steps:

1. Add an income transaction.
2. Add expenses in at least one category.
3. Add a budget limit and enough expenses to trigger a warning or exceeded state.
4. Go to `AI Advisor`.
5. Confirm that the page shows a priority insight, monthly goal status, budget risk, spending focus and recommended next steps.

Expected result: the advisor uses the current month data and shows a practical plan without requiring the internal Privacy page.

## AI Coach Test

Goal: confirm that the user can ask questions and receive answers based on the current month data.

Steps:

1. Add an income transaction.
2. Add expenses in more than one category.
3. Add a budget limit that is close to being reached or exceeded.
4. Go to `AI Coach`.
5. Ask `How can I save more this month?`.
6. Ask `Which budget is most at risk?`.
7. Confirm that both questions remain visible inside the scrollable chat history.
8. Click `Clear chat` and confirm that the conversation is removed.

Expected result: the coach answers using the user's income, expenses, category spending and budget status, and the conversation can be reviewed or cleared.

## Ollama Hybrid Mode Test

Goal: confirm that the AI Coach remains usable with or without Ollama.

Steps:

1. Run the app without Ollama.
2. Go to `AI Coach`.
3. Ask `How can I save more this month?`.
4. Confirm that the page shows `Local fallback`.
5. Install/run Ollama and start `llama3.2`.
6. Ask the same question again.
7. Confirm that the page shows `Ollama local model: llama3.2`.

Expected result: the app never breaks. It uses Ollama when available and falls back to local logic when Ollama is unavailable.
