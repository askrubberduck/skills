---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Dry the comments here. Comment-only cleanup, please.

`fetch.py`:

```python
# Timeout is in seconds.
DEFAULT_TIMEOUT = 3000


def fetch(client, url):
    # Call the client.
    # Pass the timeout to the client.
    return client.get(url, timeout_ms=DEFAULT_TIMEOUT)
```
