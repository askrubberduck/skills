---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
`python3 check.py` fails. Why?

`items.py`:

```python
def first(values):
    return values[1]


def primary(values):
    return first(values)


def secondary(values):
    return first(values)


def singleton(values):
    if len(values) != 1:
        raise ValueError("one item required")
    return values[0]
```

`check.py`:

```python
from items import primary, secondary, singleton

assert primary([10, 20]) == 10
assert secondary([30, 40]) == 30
assert singleton([50]) == 50
```

Contract: `primary` and `secondary` return the first item of a non-empty list.
