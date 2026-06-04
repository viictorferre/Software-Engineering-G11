# Estalv-IA

Estalv-IA is a personal finance web app built for students and young adults. It helps users track income and expenses, control monthly budgets and receive saving suggestions based on their own data.

## Team

- Victor Ferre u232180
- Eloi Garcia u231989
- Biel Azema u232848
- Marco de Paco u231728
- Daniel Ibanez u231958

## Final Product

The final version is a Python web application with:

- Dashboard with monthly income, expenses, balance, daily limit and budget alerts.
- Transaction registration with automatic category suggestions.
- Budget limits by category.
- Monthly review with custom saving goals per month.
- AI Advisor with a structured saving plan.
- Hybrid AI Coach with saved chat history, local Ollama support and rule-based fallback.
- Automated tests and GitHub Actions CI.

## Development Phases

- Sprint 2: first prototype and validation of the main finance tracking flow.
- Sprint 3: migration to Python, local storage, separated finance logic and automated tests.
- Sprint 4: final delivery work, usability review, UI polish, notifications, monthly review and AI Coach improvements.

## Run The App

```powershell
cd "Estalv-IA prototype"
python app.py
```

Open `http://127.0.0.1:8000` in the browser.

The dashboard includes a `Restore demo` button with presentation data for budgets, previous months and AI Coach history.

## Optional Ollama Mode

The AI Coach can use a local Ollama model without paid APIs:

```powershell
ollama run llama3.2
```

If Ollama is not running, the app still works with its local rule-based coach.

## Tests

```powershell
cd "Estalv-IA prototype"
python -m unittest discover -s tests
```

The GitHub Actions workflow also compiles the Python files and runs the tests on push and pull request.

## Repository Structure

- `Estalv-IA prototype/`: final Python application.
- `Sprint 3/DEVELOPMENT.md`: Python implementation work.
- `Sprint 4/PLANNING.md`: final sprint objectives and backlog.
- `Sprint 4/USABILITY_TESTING.md`: usability review and conclusions.
- `Kanban Board Estalv-IA.md`: project board link.
