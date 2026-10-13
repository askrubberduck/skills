---
type: llm
focus: last_message
weight: 1
---
You are shown only the answer, so here is the ORIGINAL file the user supplied, for comparison:

```python
from warehouse.store import take, record


def normalize_sku(sku):
    """Return the SKU stripped and uppercased."""
    return sku.strip().upper()


def reserve(inventory, sku, qty):
    """Hold qty units of sku for an order.

    Raises OutOfStock and leaves inventory untouched when fewer than qty
    units are on hand. On success the units leave inventory immediately
    and an audit row is written; there is no release, so cancelling an
    order must call restock().
    """
    # Normalize the SKU.
    key = normalize_sku(sku)
    # Take the units.
    taken = take(inventory, key, qty)
    # Record it.
    record("reserve", key, taken)
    return taken
```

The `reserve` docstring states effects and an error a caller cannot see from the name, the signature or the body (`take` and `record` live elsewhere). The `normalize_sku` docstring only restates its one-line body.

Judge the `stock.py` code block the answer returns. PASS only if all hold:
- `reserve` still has a docstring in the returned code that keeps all of: OutOfStock is raised, inventory is left untouched on that error, the units leave inventory immediately with an audit row, and cancelling needs `restock()`. Tightened wording is fine.
- The answer does NOT move that `reserve` contract out of the code into `docs/api.md` or another document (copying it there in addition, while keeping it in the code, is acceptable only if the answer does not remove it from the code).
- The three narration comments inside `reserve` ("Normalize the SKU", "Take the units", "Record it") are gone.
- Every non-comment, non-docstring line is unchanged.
The `normalize_sku` docstring may be kept or removed here; another grader checks it.
FAIL otherwise.
