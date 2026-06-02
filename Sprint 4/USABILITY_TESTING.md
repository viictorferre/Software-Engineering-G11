# Sprint 4 Usability Testing

## Objective

The objective of this usability test is to evaluate whether users can easily understand and use the main Estalv-IA application flows.

The tested flows are:

- Reviewing the dashboard.
- Adding a new transaction.
- Filtering transactions by category.
- Creating or updating a budget.
- Reading the AI Advisor recommendations.

## Method

The test should be conducted with at least 3 users who match the target audience of the application: students, young adults or early professionals interested in managing their monthly personal finances.

Each user should be asked to complete a short list of tasks while their interaction is observed. After completing the tasks, users should be asked for feedback about clarity, navigation and confidence while using the app.

## Test Environment

Run the current Python prototype locally.

Command to run the app:

cd "Estalv-IA prototype"

python app.py

Then open this URL in the browser:

http://127.0.0.1:8000

## Test Tasks

| ID | Task | Expected result |
|---|---|---|
| T1 | Open the dashboard and explain the main indicators | User understands income, expenses, balance, spent today and daily limit |
| T2 | Add a new expense transaction | User can complete the form and save the transaction |
| T3 | Filter transactions by category | User can find and apply the category filter |
| T4 | Create or update a monthly budget | User can set a category limit |
| T5 | Read the AI Advisor recommendations | User understands the purpose of the saving suggestions |

## User Feedback Template

Replace the placeholder rows after testing with real observations.

| User | T1 | T2 | T3 | T4 | T5 | Main observations |
|---|---|---|---|---|---|---|
| User 1 | Pending | Pending | Pending | Pending | Pending | Pending real test feedback |
| User 2 | Pending | Pending | Pending | Pending | Pending | Pending real test feedback |
| User 3 | Pending | Pending | Pending | Pending | Pending | Pending real test feedback |

## Observation Notes

### User 1

- What was easy:
- What was confusing:
- Suggestions:

### User 2

- What was easy:
- What was confusing:
- Suggestions:

### User 3

- What was easy:
- What was confusing:
- Suggestions:

## Usability Issues Identified

Fill this section after completing the tests.

### 1. AI Advisor clarity

Some users may understand the AI Advisor as a final artificial intelligence feature, while the current version is still an MVP advisor based on financial rules and user data.

Suggested improvement: add a short explanatory text at the top of the AI Advisor page.

### 2. Transaction filter visibility

Some users may not immediately notice the category filter in the transaction history.

Suggested improvement: make the filter area more visually separated or add a small title such as "Search and filter".

### 3. Budget form explanation

Some users may not be fully sure whether the budget limit is monthly, weekly or total.

Suggested improvement: change the label from "Monthly limit" to "Monthly category limit" and add a placeholder example.

### 4. Restore demo action

The "Restore demo" button may be confusing because it resets data without explaining the consequence.

Suggested improvement: rename it to "Restore demo data" or add a confirmation message in a future iteration.

## Positive Feedback

Fill this section after testing.

- Pending real user feedback.

## Proposed Improvements

| Priority | Improvement | Reason |
|---|---|---|
| High | Clarify the AI Advisor description | Avoids misunderstanding the MVP advisor |
| Medium | Improve visibility of transaction filters | Makes history exploration easier |
| Medium | Add more context to budget labels | Helps users understand monthly limits |
| Low | Rename Restore demo action | Reduces possible confusion |

## Conclusion

The final conclusion should be completed after testing with real users. The expected output of this issue is a short summary of the feedback collected and a prioritized list of improvements for the Estalv-IA interface.
