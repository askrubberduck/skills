---
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill]
runs: 3
---
The implementation is finished. Prove its shape before I send it to review: is every piece here earning its place?

`quotes.py`:

```python
ISO_CODES = {"USD", "EUR", "GBP", "JPY"}


def normalize_currency(code: str) -> str:
    code = code.strip().upper()
    if code not in ISO_CODES:
        raise ValueError(f"unsupported currency: {code!r}")
    return code


class QuoteService:
    def __init__(self, client):
        self._client = client

    def get_quote(self, currency):
        return self._client.quote(currency)


def quote_for(client, raw_currency):
    return QuoteService(client).get_quote(normalize_currency(raw_currency))
```

`quote_for` is the only public entry point; nothing else constructs `QuoteService`. The API behind `client.quote` rejects lowercase codes with an opaque 500.
