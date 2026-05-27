# Estalv-IA Python Prototype

This folder contains the current Python version of Estalv-IA. It comes from the first Sprint 2 prototype, but the app has now been reorganized so it can be tested, maintained and shown as a public preview.

## What The App Does

- Add income and expenses.
- See monthly income, expenses, balance and estimated savings.
- Review recent movements and expenses by category.
- Create monthly budget limits by category.
- Get AI-assisted saving recommendations based on monthly income, expenses, categories and budgets.
- Store local data in `data/estalvia_state.json`.
- Use public navigation focused on the product pages, without the previous internal Privacy tab.

## How The Version Evolved

1. The first prototype defined the main screens and user flow for tracking money.
2. Sprint 3 moved the app to Python while keeping the same dashboard behaviour.
3. The finance calculations were moved into `estalvia_core.py` so they can be tested separately from the web interface.
4. The latest preview adds the AI Advisor page as a first version of personalized saving advice.

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

## Run Tests

```powershell
python -m unittest discover -s tests
```

## Notes

This is still an MVP. It stores data locally and does not include user accounts, authentication, encrypted storage or a real database yet.