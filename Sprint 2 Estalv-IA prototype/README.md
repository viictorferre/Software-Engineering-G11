# Estalv-IA Python Prototype

Estalv-IA is a personal finance prototype for students, young adults and early professionals. This version rewrites the Sprint 2 HTML/CSS/JavaScript prototype as a Python app using only the Python standard library.

## What The App Does

- Add income and expenses.
- See monthly income, expenses, balance and estimated savings.
- Review recent movements and expenses by category.
- Create monthly budget limits by category.
- Get simple saving recommendations based on spending rules.
- Store local data in `data/estalvia_state.json`.

## Project Files

- `app.py`: Python web app and local HTTP server for the finance dashboard.
- `estalvia_core.py`: Python business logic for totals, categories, budgets and recommendations.
- `tests/test_core.py`: unit tests for the financial logic.
- `requirements.txt`: Python dependency list.

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

This is still an MVP. It stores data locally and does not include user accounts, authentication, encrypted storage or a real database.
