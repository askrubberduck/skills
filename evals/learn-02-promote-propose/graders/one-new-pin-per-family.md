---
type: llm
focus: last_message
weight: 1
---
`roster` listed two new Google models. At most one new pin per family goes on trial at once.

PASS only if the resulting `[learn].trial` holds at most one of `google:gemini-4-flash:high` and `google:gemini-4-flash-lite:low` (holding one, or none with a stated reason, both pass).
FAIL if both new Google models are put on trial together.
