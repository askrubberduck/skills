---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Rename `calc` to `compute_total` across this file. Nothing else. Reply with the file.

```python
TAX = 0.2


def calc(items):
    return sum(price * qty for price, qty in items)


def with_tax(items):
    return calc(items) * (1 + TAX)


def report(items):
    return f"subtotal={calc(items)} total={with_tax(items)}"
```
