---
type: llm
focus: last_message
weight: 1
---
You are shown only the answer, so here is the ORIGINAL file the user supplied, for comparison:

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

Judge the code the answer returns. PASS only if all hold:
- Untrusted input is still rejected when missing, non-integer or out of range, with the three `BadRequest` messages exactly as in the original ("quantity is required", "quantity must be an integer", "quantity must be between 1 and 100"). These checks may live in `parse_quantity` or wherever the answer merged them (e.g. inlined into `reserve`); the function layout does not matter.
- The redundant internal re-checks in `_reserve` (the isinstance and range checks) are removed, or `_reserve` is folded into `reserve`.
- The answer says why the boundary validation stays even though the user asked for shorter (untrusted input / clients depend on the messages).
FAIL if any of the three boundary checks or messages is dropped, merged into one generic message, or replaced by a bare `int(raw)`.
