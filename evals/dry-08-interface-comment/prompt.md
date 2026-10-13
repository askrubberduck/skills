---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Dry the comments in this module and reply with the cleaned file. Public usage docs live in `docs/api.md`, if that matters.

`stock.py`:

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

`take` and `record` live in another package; callers of `reserve` never read `warehouse.store`.
