# Sprint 3 Development

## Objective

The development objective for Sprint 3 was to turn the Estalv-IA prototype into a working Python version while keeping the same product behaviour.

## Completed Work

- Converted the prototype into a Python web application.
- Preserved the main MVP features:
  - income tracking,
  - expense tracking,
  - monthly overview,
  - recent transactions,
  - expenses by category,
  - budget limits,
  - saving recommendations,
  - privacy section,
  - restore demo data.
- Split the project into interface code and business logic.
- Added local JSON persistence for transactions and budgets.
- Updated the project documentation to explain how to run the Python app.

## Main Files

- `Sprint 2 Estalv-IA prototype/app.py`
- `Sprint 2 Estalv-IA prototype/estalvia_core.py`
- `Sprint 2 Estalv-IA prototype/README.md`
- `Sprint 2 Estalv-IA prototype/TECH_STACK.md`

## How To Run

```powershell
cd "Sprint 2 Estalv-IA prototype"
python app.py
```

Then open `http://127.0.0.1:8000` in the browser.

## Notes For Next Sprint

The current saving recommendations are rule-based. The Kanban includes an AI-based recommendation task, so that should be planned as Sprint 4 work unless the team decides to keep it as a future improvement.
