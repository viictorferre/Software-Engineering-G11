# Estalv-IA

[![Python CI](https://github.com/viictorferre/Software-Engineering-G11/actions/workflows/python-ci.yml/badge.svg)](https://github.com/viictorferre/Software-Engineering-G11/actions/workflows/python-ci.yml)

Software Engineering G11 project for creating a technology startup focused on personal finance.

## Team

- Victor Ferre u232180
- Eloi Garcia u231989
- Biel Azema u232848
- Marco de Paco u231728
- Daniel Ibanez u231958

## Product Vision

Estalv-IA helps students, young adults and early professionals understand where their money goes, control budgets and receive simple recommendations to save better.

## Sprint 2: Python Prototype

For Sprint 2 we created a first prototype of the Estalv-IA web app. The goal of this version is to show how the app could work and to test the main idea before building a more advanced version.

The prototype lets the user add income and expenses, see a monthly summary, check recent transactions, view expenses by category, manage simple budgets and receive basic saving recommendations.

The repository also includes a GitHub Actions CI workflow. It runs automatically on every push and pull request, verifies that the Python files compile and runs the unit tests.

## Project Files

The prototype is inside the folder `Sprint 2 Estalv-IA prototype`.

- `Sprint 2 Estalv-IA prototype/app.py`: contains the Python web app and local HTTP server.
- `Sprint 2 Estalv-IA prototype/estalvia_core.py`: contains the financial logic for totals, categories, budgets and recommendations.
- `Sprint 2 Estalv-IA prototype/tests/test_core.py`: contains unit tests for the main Python logic.
- `Sprint 2 Estalv-IA prototype/TECH_STACK.md`: explains the Python technology decision and possible future improvements.
- `Sprint 2 Estalv-IA prototype/TESTING.md`: explains the automated and manual tests used to check the Sprint 2 features.
- `.github/workflows/python-ci.yml`: runs the CI pipeline on every push and pull request.

## How To Open The Web App

Run:

```powershell
cd "Sprint 2 Estalv-IA prototype"
python app.py
```

Then open `http://127.0.0.1:8000` in the browser.

## How To Run Tests

```powershell
cd "Sprint 2 Estalv-IA prototype"
python -m unittest discover -s tests
```
