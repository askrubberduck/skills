---
type: llm
focus: last_message
weight: 1
---
The candidate is executable code about to face its release gate.

PASS only if the plan runs a rally (ping-pong: one side writes a failing test, the other makes it pass, alternating) with a model of a different family against the code's contract before the gate reviewers are dispatched, and treats its result as evidence for the gate.
FAIL if the plan goes from local tests or a self-check straight to the gate reviewers, or mentions a rally only as an optional idea or only after a rejection.
