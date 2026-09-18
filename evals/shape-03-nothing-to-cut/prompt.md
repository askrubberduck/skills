---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
This feels over-engineered. Simplify it.

`prices.py`:

```python
import csv


def load_prices(path):
    prices = {}
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            prices[row["sku"]] = float(row["price"])
    return prices


def total(prices, order):
    return sum(prices[sku] * qty for sku, qty in order.items())
```
