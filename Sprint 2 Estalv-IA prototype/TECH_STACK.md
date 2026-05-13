# Technology Recommendation

## Current Phase: Sprint 2 Python Prototype

Use:

- Python 3
- Python standard library HTTP server
- Local JSON storage
- Unit tests with `unittest`

Reason: this keeps the prototype simple, easy to run and fully focused on Python. It avoids external dependencies while preserving the same dashboard, transactions, budgets and recommendations that the previous browser prototype had.

## Application Structure

- `app.py` renders the web interface and handles local HTTP routes.
- `estalvia_core.py` contains the finance logic.
- `data/estalvia_state.json` is created automatically when the user saves data.
- `tests/test_core.py` checks the calculations, category suggestions, budgets and recommendations.

## Future Improvements

If the project grows, the next Python step could be:

- Flask or FastAPI for cleaner routing.
- SQLite for structured local storage.
- User authentication and encrypted storage for real personal finance data.
- A Python recommendation model or AI API integration for richer savings advice.

## Team Decision

For Sprint 2, the stack is now Python. The prototype remains an MVP and keeps the original product behavior: add transactions, review monthly totals, manage budgets and receive rule-based recommendations.
