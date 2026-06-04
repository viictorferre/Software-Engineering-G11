# Estalv-IA Application

This folder contains the final Python version of Estalv-IA for the Software Engineering project.

## Main Features

- Add income and expenses.
- Review monthly income, expenses, balance and estimated saving rate.
- Check recent movements and expenses by category.
- Create monthly budget limits by category.
- Review previous months with a different saving goal for each month.
- Use the AI Advisor to get a structured saving plan.
- Ask the hybrid AI Coach questions about spending, budgets and monthly balance.
- Keep local chat history for the coach and clear it when needed.

## How It Evolved

The first version focused on the basic finance dashboard. During Sprint 3, the app was rebuilt in Python and the financial calculations were moved into `estalvia_core.py` so they could be tested separately. During Sprint 4, the team polished the interface, added monthly review, improved budget alerts and prepared the AI Advisor and AI Coach for the final demo.

## Files

- `app.py`: web interface and local HTTP server.
- `estalvia_core.py`: finance calculations, budgets, advisor logic and coach fallback.
- `features/`: small feature modules for daily indicators.
- `tests/test_core.py`: unit tests for the finance logic.
- `assets/logo.png`: app logo.
- `data/estalvia_state.json`: local data file created when the app is used.

## Run

```powershell
python app.py
```

Open `http://127.0.0.1:8000`.

Use `Restore demo` before the presentation to load sample data with budget alerts, previous months, saving goals and coach history.

## Optional Local AI

The AI Coach can connect to Ollama:

```powershell
ollama run llama3.2
```

When Ollama is not available, the app uses its local rule-based coach so the demo remains reliable.

## Tests

```powershell
python -m unittest discover -s tests
```

## Current Limits

This is the final course delivery, not a production banking product. Data is stored locally, there are no user accounts and there is no external database.
