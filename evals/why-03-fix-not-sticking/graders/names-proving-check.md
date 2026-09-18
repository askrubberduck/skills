---
type: llm
focus: last_message
weight: 1
---
PASS if the answer names a concrete check that would show the failure is gone — e.g. calling `get_profile` (or `handler_b`) for an existing user with a cold/empty cache and expecting the profile rather than None/TypeError. FAIL if it offers no check, or only a vague "test it" / "run the tests".
