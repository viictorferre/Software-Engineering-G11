# Estalv-IA Python Prototype

This folder contains the current Python version of Estalv-IA. It comes from the first Sprint 2 prototype, but the app has now been reorganized so it can be tested, maintained and shown as a public preview.

## What The App Does

- Add income and expenses.
- See monthly income, expenses, balance and estimated savings.
- Review previous months and set a different saving target for each month.
- Review recent movements and expenses by category.
- Create monthly budget limits by category.
- Get an automatic AI Advisor saving plan with priority insight, goal progress, budget risk and next steps.
- Ask an interactive AI Coach questions about savings, spending, budgets and balance, with saved chat history.
- Use a hybrid AI mode: local Ollama model when available, rule-based fallback when not.
- Store local data in `data/estalvia_state.json`.
- Use public navigation focused on the product pages, without the previous internal Privacy tab.

## How The Version Evolved

1. The first prototype defined the main screens and user flow for tracking money.
2. Sprint 3 moved the app to Python while keeping the same dashboard behaviour.
3. The finance calculations were moved into `estalvia_core.py` so they can be tested separately from the web interface.
4. The latest preview adds a structured AI Advisor plan, an AI Coach with saved conversation history and editable monthly saving goals as a first version of personalized saving advice.

## Project Files

- `app.py`: Python web app and local HTTP server for the finance dashboard.
- `estalvia_core.py`: finance logic for totals, categories, budgets and AI-assisted recommendations.
- `tests/test_core.py`: unit tests for the financial logic.
- `requirements.txt`: dependency list. The app currently uses the Python standard library.

## Run The App

```powershell
python app.py
```

Then open `http://127.0.0.1:8000` in the browser.

## Final Presentation Demo

Use `Restore demo` from the dashboard before presenting. The demo data includes current-month expenses, budgets close to or over their limits, previous months for `Monthly Review`, custom saving goals and a saved AI Coach conversation.

## Optional Ollama Mode

The AI Coach can use Ollama locally. This keeps the demo free and avoids sending personal finance data to an external paid API.

Install Ollama, then run:

```powershell
ollama run llama3.2
```

Run the app after that. If Ollama is not available, the AI Coach automatically uses the local fallback.

## Run Tests

```powershell
python -m unittest discover -s tests
```

## Notes

This is still an MVP. It stores data locally and does not include user accounts, authentication, encrypted storage or a real database yet.
