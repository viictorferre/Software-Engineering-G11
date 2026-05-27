# Sprint 3 Development

## Objective

The objective for Sprint 3 was to take the Estalv-IA prototype from the previous sprint and turn it into a working Python application without changing the main product idea. The team wanted the same finance dashboard to keep working, but with cleaner code, local persistence and tests.

## Starting Point

At the beginning of the sprint, the project already had the basic MVP flow:

- add income,
- add expenses,
- review monthly totals,
- check recent transactions,
- review expenses by category,
- define budget limits,
- see simple saving recommendations.

The main task was not to redesign the product from zero, but to rebuild the prototype in Python and make it easier to test.

## Completed Work

- Renamed the app folder to `Estalv-IA prototype` so it no longer looks tied only to Sprint 2.
- Converted the prototype into a Python web application.
- Preserved the main MVP behaviour from the first version.
- Split the project into interface code and finance logic.
- Added local JSON persistence for transactions and budgets.
- Added unit tests for calculations, categories, budgets and recommendations.
- Added a GitHub Actions workflow that compiles the Python files and runs the tests on push and pull request.
- Updated the public preview by removing the internal Privacy tab from navigation.
- Added the first AI Advisor version for monthly saving suggestions.

## Main Files

- `Estalv-IA prototype/app.py`
- `Estalv-IA prototype/estalvia_core.py`
- `Estalv-IA prototype/tests/test_core.py`
- `Estalv-IA prototype/README.md`
- `Estalv-IA prototype/TECH_STACK.md`
- `.github/workflows/python-ci.yml`

## How To Run

```powershell
cd "Estalv-IA prototype"
python app.py
```

Then open `http://127.0.0.1:8000` in the browser.

## How To Test

```powershell
cd "Estalv-IA prototype"
python -m unittest discover -s tests
```

## Notes For Next Sprint

The AI Advisor is currently a first approximation based on the user's monthly data and rule-based analysis. For Sprint 4, the team should improve the advice, add notification behaviour, review privacy/security and prepare usability testing.