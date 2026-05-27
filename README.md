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
- The current public preview keeps the Python app, removes the internal Privacy tab from the navigation and adds an AI Advisor page with saving suggestions based on the current month.
- Sprint 4 planning focuses on notifications, privacy/security improvements, usability testing and polishing the saving advice for a more complete delivery.

## How To Open The Web App

Run:

```powershell
cd "Estalv-IA prototype"
python app.py
```

Then open `http://127.0.0.1:8000` in the browser.

## Current Public Preview

The current version includes a public-facing AI Advisor tab. It reviews monthly income, expenses, category spending and budget status to suggest realistic saving actions. The suggestions are still part of the MVP: they are generated from the app's own rules and financial data, not from a final production AI service.

## How To Run Tests

```powershell
cd "Estalv-IA prototype"
python -m unittest discover -s tests
```

## Project Documentation

Sprint 3 work is documented in `Sprint 3/DEVELOPMENT.md`.

Sprint 4 planning is documented in `Sprint 3/SPRINT_4_PLANNING.md`, based on the Kanban objectives and the work that still needs to be improved after Sprint 3.