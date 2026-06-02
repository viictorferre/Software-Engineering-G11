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


## Participants

This usability evaluation was conducted as a simulated pilot test using 6 representative user profiles.

| User | Profile |
|---|---|
| User 1 | Parent, low technical background |
| User 2 | Parent, medium digital experience |
| User 3 | Engineering student |
| User 4 | Engineering student |
| User 5 | Engineering student |
| User 6 | Engineering student |

The goal of this simulated test was to anticipate usability issues before conducting a full real-user validation.

## Results

| User | T1 | T2 | T3 | T4 | T5 | Main observations |
|---|---|---|---|---|---|---|
| User 1 | Completed | Partial | Partial | Partial | Completed | Understood the dashboard values, but needed help understanding where to add and filter transactions. |
| User 2 | Completed | Completed | Partial | Completed | Completed | Could use the app mostly without help, but did not notice the category filter immediately. |
| User 3 | Completed | Completed | Completed | Completed | Completed | Completed all flows quickly and suggested improving visual feedback after saving data. |
| User 4 | Completed | Completed | Completed | Completed | Completed | Found the interface clear, but suggested explaining the AI Advisor logic more explicitly. |
| User 5 | Completed | Completed | Completed | Partial | Completed | Was unsure whether the budget limit was monthly or total. |
| User 6 | Completed | Completed | Completed | Completed | Completed | Completed all tasks and suggested adding confirmation before restoring demo data. |

## Observation Notes

### User 1

- What was easy: understanding the general dashboard indicators such as income, expenses and balance.
- What was confusing: finding where to add a transaction and how to filter previous movements.
- Suggestions: add clearer section descriptions and make the transaction filter more visible.

### User 2

- What was easy: adding a new transaction and understanding the AI Advisor recommendations.
- What was confusing: the transaction category filter was not immediately visible.
- Suggestions: highlight the filter area or add a title above it.

### User 3

- What was easy: navigating between dashboard, transactions, budgets and AI Advisor.
- What was confusing: there was no clear success message after saving a transaction.
- Suggestions: add a confirmation message after saving or updating data.

### User 4

- What was easy: using the main financial flows and understanding the budget cards.
- What was confusing: the AI Advisor could be interpreted as a production AI system instead of an MVP recommendation engine.
- Suggestions: add a short explanation of how the recommendations are generated.

### User 5

- What was easy: adding expenses and reading the dashboard.
- What was confusing: the budget form did not clearly explain that the limit is monthly.
- Suggestions: rename the field to "Monthly category limit" and include an example.

### User 6

- What was easy: completing all tasks without external help.
- What was confusing: the "Restore demo" button could be risky because it does not explain that data may be reset.
- Suggestions: rename the button or add a confirmation message.
## Positive Feedback

- The dashboard was generally easy to understand because the main indicators are visible at the top.
- Engineering students completed the main flows quickly and found the navigation simple.
- Users liked having budgets and recommendations in separate sections.
- The AI Advisor page was considered useful, especially as a quick summary of possible saving actions.

## Proposed Improvements

| Priority | Improvement | Reason |
|---|---|---|
| High | Clarify the AI Advisor description | Avoids misunderstanding the MVP advisor |
| High | Add success messages after saving data | Makes user actions feel confirmed |
| Medium | Improve visibility of transaction filters | Makes history exploration easier |
| Medium | Add more context to budget labels | Helps users understand monthly limits |
| Low | Rename Restore demo action | Reduces possible confusion |

## Conclusion

The simulated usability pilot showed that the main Estalv-IA flows are understandable, especially for users with technical or digital experience. The dashboard, transaction form and AI Advisor were generally clear.

However, the test also identified several usability improvements. The most important ones are clarifying the AI Advisor behaviour, adding success messages after saving data, improving the visibility of transaction filters and making the monthly budget concept more explicit.

Overall, Estalv-IA is usable in its current Sprint 4 state, but small interface and wording improvements would make the experience clearer and more trustworthy before final delivery.

