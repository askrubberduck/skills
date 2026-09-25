---
type: llm
focus: last_message
weight: 1
---
The config names a race list, `google:gemini-3.8-flash-high`, separate from the review roster, `openai:gpt-6-sol:high`. The doer is Anthropic.

PASS only if the rival is Google/Gemini pinned to `gemini-3.8-flash-high`, and the answer ties the choice to the race list (`[models].race`).
FAIL if the rival is OpenAI/`gpt-6-sol` or Codex, or if the answer takes the rival from the reviewers roster.
