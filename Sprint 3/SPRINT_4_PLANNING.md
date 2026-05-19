# Sprint 4 Planning

## Sprint 4 Goal

Improve the Estalv-IA MVP from a working prototype into a more complete and trustworthy finance app by adding notifications, strengthening privacy/security, testing the new behaviour and preparing final delivery material.

## Sprint 4 Backlog

| Priority | Issue | Task | Reason |
|---|---|---|---|
| High | #8 | Implement notification system | Users should receive budget or spending alerts before limits are exceeded. |
| High | #10 | Ensure data security and privacy | Personal finance data needs clear privacy handling. |
| High | #12 | Test notification system | Notification behaviour should be reliable and covered by tests. |
| Medium | #13 | Conduct usability testing | The team needs user feedback to validate ease of use. |
| Medium | #14 | Prepare project documentation and presentation | Final delivery needs clear explanation of the product and process. |
| Medium | #15 | Implement AI-based saving recommendations | Current recommendations are rule-based, so this is the next improvement. |

## Planned Work

### 1. Notification System

Deliverables:

- Budget warning notifications.
- Exceeded-budget notifications.
- Notification messages visible in the app.

Acceptance criteria:

- Warning appears when a category reaches 80% of its budget.
- Exceeded message appears when spending passes the budget limit.
- Notifications update after adding a transaction.

### 2. Privacy And Data Security

Deliverables:

- Clearer privacy section in the app.
- Documentation of local data storage.
- Data reset/export option if feasible.

Acceptance criteria:

- Users know what data is stored.
- Users can remove local data.
- Documentation explains future secure storage needs.

### 3. Notification Testing

Deliverables:

- Unit tests for notification thresholds.
- Tests for warning and exceeded states.

Acceptance criteria:

- Tests pass locally.
- GitHub Actions passes after the changes.

### 4. Usability Testing

Deliverables:

- Short usability test script.
- Feedback table with user observations.
- Improvement list based on feedback.

Acceptance criteria:

- Users can add income and expenses without help.
- Users can understand the budget status.
- Findings are documented in the repository.

### 5. Documentation And Presentation

Deliverables:

- Final README updates.
- Sprint 4 summary.
- Presentation outline or final slides content.

Acceptance criteria:

- A new user can run and test the app using the documentation.
- The team can explain the product, implementation, testing and next steps.

### 6. AI-Based Saving Recommendations

Deliverables:

- Decide whether AI recommendations are implemented now or documented as a future improvement.
- If implemented, add smarter recommendation logic and tests.
- If deferred, explain the technical requirements.

Acceptance criteria:

- Recommendation scope is clear.
- Any new recommendation logic has tests.


