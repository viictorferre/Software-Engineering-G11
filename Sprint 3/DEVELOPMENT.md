# Sprint 3 Development

## Objective

Sprint 3 was the implementation sprint. The goal was to take the first Estalv-IA prototype and rebuild it as a working Python application while keeping the original finance tracking idea.

## Starting Point

The project already had the basic product flow:

- Add income.
- Add expenses.
- Review monthly totals.
- Check recent transactions.
- See expenses by category.
- Define budget limits.
- Receive simple saving suggestions.

## Completed Work

- Rebuilt the app in Python.
- Kept the main dashboard and finance tracking behaviour.
- Added local JSON persistence.
- Moved finance calculations into `estalvia_core.py`.
- Added unit tests for totals, categories, budgets and recommendations.
- Added GitHub Actions CI for build and tests.
- Removed internal navigation that was not useful for the public-facing app.

## Main Files

- `Estalv-IA prototype/app.py`
- `Estalv-IA prototype/estalvia_core.py`
- `Estalv-IA prototype/tests/test_core.py`
- `.github/workflows/python-ci.yml`

## Result

By the end of Sprint 3, Estalv-IA had a working Python base that could be tested and extended during Sprint 4. The remaining work was mainly product polish, usability review and stronger saving advice.
