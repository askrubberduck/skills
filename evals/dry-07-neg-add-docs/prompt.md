---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Write docstrings for these three functions. Reply with the updated code.

```python
def slugify(title):
    return "-".join(title.lower().split())


def clamp(value, low, high):
    return max(low, min(value, high))


def initials(name):
    return "".join(part[0].upper() for part in name.split())
```
