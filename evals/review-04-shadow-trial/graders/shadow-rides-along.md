---
type: llm
focus: last_message
weight: 1
---
`gemini-3.8-flash-high` is on trial with zero of three shadow reviews done, so it should ride along as an extra reviewer.

PASS only if all hold:
- The plan dispatches `gemini-3.8-flash-high` in addition to the required reviewer(s), not instead of one.
- It says that model's verdict does not count toward the gate (it cannot approve or block), and that its timeout or outage does not leave the gate short.
FAIL if the trial model is left out without a stated reason, replaces a required reviewer, or its REJECT or APPROVE is said to count.
