---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Dry the comments in this file.

`backoff.py`:

```python
def backoff(attempt):
    # Gateway drops connections idle for 30 s; keep the cap below that.
    return min(2 ** attempt, 25)
```
