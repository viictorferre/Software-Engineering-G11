# Technology Recommendation

## Current Phase: Python Public Preview

The app currently uses:

- Python 3
- Python standard library HTTP server
- Local JSON storage
- Unit tests with `unittest`
- GitHub Actions for basic CI checks

This stack was chosen because the team needed a version that was simple to run in class, easy to review and focused on the product logic. It also lets us keep the same MVP behaviour from the first prototype while writing the core finance calculations in Python.

## Application Structure

- `app.py` renders the web interface and handles local HTTP routes.
- `estalvia_core.py` contains the finance logic used by the dashboard, budgets and AI Advisor.
- `data/estalvia_state.json` is created automatically when the user saves data.
- `tests/test_core.py` checks calculations, category suggestions, budget status and recommendations.

## Development Phases

- Sprint 2: first prototype and validation of the basic finance dashboard.
- Sprint 3: Python implementation, local storage, business logic separation and automated tests.
- Public preview: navigation cleanup and first AI Advisor version for saving suggestions.
- Sprint 4: notifications, privacy/security work, usability testing and final delivery preparation.

## Future Improvements

If the project grows, the next technical steps could be:

- Flask or FastAPI for cleaner routing.
- SQLite for structured local storage.
- User authentication and encrypted storage for real personal finance data.
- A more advanced recommendation model or AI API integration for richer savings advice.

## Team Decision

For this prototype stage, the team keeps the stack intentionally small. The priority is to prove that the main flows work: add transactions, review monthly totals, manage budgets and receive useful saving guidance.