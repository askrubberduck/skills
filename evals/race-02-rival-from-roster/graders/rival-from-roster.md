---
type: llm
focus: last_message
weight: 1
---
The configured reviewer roster holds only one family: OpenAI, `gpt-6.1-sol`. The doer is Anthropic.

PASS only if the rival is OpenAI/Codex pinned to `gpt-6.1-sol` (for example through `--pin openai:gpt-6.1-sol` or `codex -m gpt-6.1-sol`), taken from the configured roster.
FAIL if the rival is Google/Gemini/agy, or if the model id is left as a placeholder the owner must fill in.
