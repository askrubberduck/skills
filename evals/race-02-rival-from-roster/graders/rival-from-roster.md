---
type: llm
focus: last_message
weight: 1
---
The configured reviewer roster holds only one family: Google, `gemini-3.1-pro-high`. The doer is Anthropic.

PASS only if the rival is Google/Gemini pinned to `gemini-3.1-pro-high` (for example through `agy --model gemini-3.1-pro-high`), taken from the configured roster.
FAIL if the rival is OpenAI/Codex/GPT, or if the model id is left as a placeholder the owner must fill in.
