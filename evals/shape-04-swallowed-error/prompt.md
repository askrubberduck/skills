---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Clean this up, there's too much defensive stuff in it. Reply with the result.

`orders.py`:

```python
import time


def fetch_orders(client, user_id):
    for attempt in range(3):
        try:
            return client.get(f"/users/{user_id}/orders")
        except TimeoutError:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def recent_orders(client, user_id):
    try:
        return fetch_orders(client, user_id)[:10]
    except Exception:
        return []
```

The dashboard shows "No orders yet" when `recent_orders` returns an empty list. The orders service times out a few times a day.
