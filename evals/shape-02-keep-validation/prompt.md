---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Make this shorter. It's way too long for what it does. Reply with the result.

`reserve.py`:

```python
class BadRequest(Exception):
    pass


def parse_quantity(raw):
    """HTTP boundary: raw comes straight from the query string."""
    if raw is None or raw == "":
        raise BadRequest("quantity is required")
    try:
        qty = int(raw)
    except ValueError:
        raise BadRequest("quantity must be an integer")
    if not 1 <= qty <= 100:
        raise BadRequest("quantity must be between 1 and 100")
    return qty


def reserve(stock, raw_qty):
    qty = parse_quantity(raw_qty)
    return _reserve(stock, qty)


def _reserve(stock, qty):
    if not isinstance(qty, int):
        raise TypeError("qty must be int")
    if qty < 1 or qty > 100:
        raise ValueError("qty out of range")
    return stock.take(qty)
```

`_reserve` is only called from `reserve`. API clients match on the three `BadRequest` messages.
