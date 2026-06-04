# Estalv-IA

Software Engineering G11 project for a personal finance app focused on students, young adults and early professionals.

## Team

- Victor Ferre u232180
- Eloi Garcia u231989
- Biel Azema u232848
- Marco de Paco u231728
- Daniel Ibanez u231958

## Product Vision

Estalv-IA helps users understand where their money goes during the month, control category budgets and receive practical saving suggestions based on their own income and expenses.

## Development Process

The project has been built in phases so the app could grow without losing the original MVP idea.

- Sprint 2 started with the first working prototype of the finance dashboard and the main user flows: add income, add expenses, review monthly totals and check budgets.
- Sprint 3 moved that prototype into Python. The goal was to keep the same behaviour while separating the interface from the finance calculations and adding tests.
- The current public preview keeps the Python app, removes the internal Privacy tab from the navigation and adds AI Advisor and AI Coach pages with saving suggestions based on the current month.
- Sprint 4 planning focuses on notifications, privacy/security improvements, usability testing and polishing the saving advice for a more complete delivery.

## How To Open The Web App

Run:

```powershell
cd "Estalv-IA prototype"
python app.py
```

Then open `http://127.0.0.1:8000` in the browser.

## Current Public Preview

The current version includes a public-facing AI Advisor tab, an interactive AI Coach and a Monthly Review page. They review monthly income, expenses, category spending, budget status and custom saving target progress for each month. The Advisor now presents a structured saving plan, while the Coach keeps a saved conversation history and works as a hybrid system: it can use a local Ollama model when available, and falls back to the app's own rule-based logic when Ollama is not running.

The dashboard `Restore demo` action loads a final-presentation scenario with budget alerts, previous months, custom goals and AI Coach history.

## Optional Local AI With Ollama

To enable the smarter local AI mode without paid APIs:

```powershell
ollama run llama3.2
```

Keep Ollama available in the background, then run the web app normally. The AI Coach will use `llama3.2` by default through `http://127.0.0.1:11434`.

## How To Run Tests

```powershell
cd "Estalv-IA prototype"
python -m unittest discover -s tests
```

## Project Documentation

Sprint 3 work is documented in `Sprint 3/DEVELOPMENT.md`.

Sprint 4 planning is documented in `Sprint 3/SPRINT_4_PLANNING.md`, based on the Kanban objectives and the work that still needs to be improved after Sprint 3.
