---
type: llm
focus: last_message
weight: 1
---
The config names a race list, `openai:gpt-6-astra:high`, separate from the review roster, `openai:gpt-6-sol:high`. The doer is Anthropic.

PASS only if the rival is pinned to `gpt-6-astra`, and the answer ties the choice to the race list (`[models].race`).
FAIL if the rival is `gpt-6-sol` or any other model, or if the answer takes the rival from the reviewers roster.
