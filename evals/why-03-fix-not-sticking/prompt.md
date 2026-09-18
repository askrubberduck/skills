---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Yesterday I added a None-guard in `handler_a` because it crashed with `TypeError: 'NoneType' object is not subscriptable`. Today the same TypeError comes from `handler_b`. The fix keeps not sticking. Why?

`profiles.py`:

```python
_cache = {}


def load_profile(user_id):
    """Read the profile row from the database. Raises LookupError if the user does not exist."""
    ...


def warm(user_id):
    _cache[user_id] = load_profile(user_id)


def get_profile(user_id):
    """Return the profile dict for user_id, loading it on a cache miss."""
    return _cache.get(user_id)


def handler_a(user_id):
    profile = get_profile(user_id)
    if profile is None:  # added yesterday
        return {"error": "unknown user"}
    return {"name": profile["name"]}


def handler_b(user_id):
    return {"email": get_profile(user_id)["email"]}


def handler_c(user_id):
    warm(user_id)
    return {"plan": get_profile(user_id)["plan"]}
```
