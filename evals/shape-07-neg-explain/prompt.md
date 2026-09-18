---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Explain what this decorator does. I don't want it changed.

```python
import functools
import time


def timed(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            print(f"{fn.__name__} took {time.perf_counter() - start:.3f}s")
    return wrapper
```
