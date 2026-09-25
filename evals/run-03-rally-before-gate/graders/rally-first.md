---
type: llm
focus: last_message
weight: 1
---
The candidate is executable code about to face its release gate.

PASS only if the plan runs a `duck-race` rally (or ping-pong) with a model of a different family against the code's contract, and does it before the final proof pass and before the gate reviewers are dispatched, treating its result as evidence for the gate.
FAIL if the plan goes from local tests or a self-check straight to the gate reviewers, puts the rally after the final proof pass, or mentions a rally only as an optional idea or only after a rejection.
