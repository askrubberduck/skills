---
type: llm
focus: last_message
weight: 1
---
`QuoteService` is a pass-through: one method that forwards to `client.quote`, constructed only inside `quote_for`. `normalize_currency` carries a real contract: the upstream API rejects lowercase codes with an opaque 500, and unsupported codes get a clear error.

PASS only if all hold:
- `QuoteService` is named as removable, with what removing it loses (nothing required) or equivalent reasoning.
- `normalize_currency` is kept, citing the contract it protects (uppercase for the API, clear error for unsupported codes).
FAIL if `normalize_currency` is proposed for removal, or `QuoteService` is kept on "separation of concerns" or future-use grounds alone.
