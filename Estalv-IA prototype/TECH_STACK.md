# Technology Recommendation

## Current Phase: Python Public Preview

The app currently uses:

- Python 3
- Python standard library HTTP server
- Local JSON storage
- Unit tests with `unittest`
- GitHub Actions for basic CI checks
- Optional local Ollama model for the AI Coach

This stack was chosen because the team needed a version that was simple to run in class, easy to review and focused on the product logic. It also lets us keep the same MVP behaviour from the first prototype while writing the core finance calculations in Python.

## Application Structure

- `app.py` renders the web interface and handles local HTTP routes.
- `estalvia_core.py` contains the finance logic used by the dashboard, budgets, AI Advisor, AI Coach and Ollama fallback flow.
- `data/estalvia_state.json` is created automatically when the user saves data.
- `tests/test_core.py` checks calculations, category suggestions, budget status and recommendations.

## Development Phases

- Sprint 2: first prototype and validation of the basic finance dashboard.
- Sprint 3: Python implementation, local storage, business logic separation and automated tests.
- Public preview: navigation cleanup, first AI Advisor version and hybrid AI Coach for saving suggestions.
- Sprint 4: notifications, privacy/security work, usability testing and final delivery preparation.

## Future Improvements

If the project grows, the next technical steps could be:

- Flask or FastAPI for cleaner routing.
- SQLite for structured local storage.
- User authentication and encrypted storage for real personal finance data.
- A more advanced recommendation model, larger local Ollama model or external AI API integration for richer conversational savings advice.

## Team Decision

For this prototype stage, the team keeps the stack intentionally small. The priority is to prove that the main flows work: add transactions, review monthly totals, manage budgets and receive useful saving guidance.

## AI Coach Mode

The AI Coach first tries to use Ollama at `http://127.0.0.1:11434/api/chat` with `llama3.2`. If Ollama is not installed, not running or unavailable, the app automatically uses the local rule-based coach. This keeps the presentation reliable and avoids paid API usage.
