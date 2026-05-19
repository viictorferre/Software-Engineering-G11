# Sprint 3 Testing

## Objective

The testing objective for Sprint 3 was to validate the most important finance logic and make sure the project can be checked automatically.

## Completed Tests

The unit tests cover:

- category suggestion rules,
- income, expense and balance calculations,
- saving-rate calculation,
- monthly transaction filtering,
- expense totals by category,
- budget status boundaries,
- recommendation generation.

## Main Files

- `Sprint 2 Estalv-IA prototype/tests/test_core.py`
- `Sprint 2 Estalv-IA prototype/TESTING.md`
- `.github/workflows/python-ci.yml`

## Local Test Command

```powershell
cd "Sprint 2 Estalv-IA prototype"
python -m unittest discover -s tests
```

Latest local result: 6 tests passed.

## CI

GitHub Actions runs automatically on every push and pull request.

The workflow checks:

1. Python files compile.
2. Unit tests pass.

This gives the team a basic quality gate before merging new changes.
