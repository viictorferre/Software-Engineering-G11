# Technology Stack

## Current Stack

- Python 3.11
- Python standard library HTTP server
- Local JSON storage
- `unittest` for automated tests
- GitHub Actions for CI
- Optional Ollama local model for the AI Coach

## Why This Stack

The team kept the stack small so the project is easy to run, review and explain during the final presentation. The app does not need external dependencies to work, and the core finance logic can be tested without starting the web server.

## Application Structure

- `app.py` handles routes, forms and HTML rendering.
- `estalvia_core.py` contains calculations, budgets, monthly review, AI Advisor logic and the AI Coach fallback.
- `features/` contains small focused calculations used by the dashboard.
- `tests/test_core.py` covers the finance logic and hybrid coach behaviour.
- `data/estalvia_state.json` is created locally when the app stores user data.

## AI Coach

The coach first tries to use Ollama at `http://127.0.0.1:11434/api/chat` with `llama3.2`. If Ollama is not running, the app falls back to local rule-based answers using the same income, expense and budget data.

This keeps the demo free, local and reliable.

## Possible Future Work

- Replace the local HTTP server with Flask or FastAPI.
- Use SQLite instead of JSON for structured storage.
- Add user accounts and better privacy controls.
- Add confirmation messages after saving or resetting data.
