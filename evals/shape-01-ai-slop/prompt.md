---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
An agent wrote this and it's full of AI slop. Clean it up and reply with the result.

`signup.py`:

```python
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class SignupError(ValueError):
    pass


def _validate_email(email):
    if not EMAIL_RE.match(email):
        raise SignupError("invalid email")


def normalize(email, strategy="lower"):
    if strategy == "lower":
        return email.strip().lower()
    raise NotImplementedError(strategy)


def normalize_email(email):
    return normalize(email)


def create_user(db, email):
    if not EMAIL_RE.match(email):
        raise SignupError("invalid email")
    return db.insert("users", {"email": normalize_email(email)})


def signup(db, form):
    """HTTP boundary: form is untrusted."""
    email = form.get("email", "")
    _validate_email(email)
    return create_user(db, email)


def invite(db, email):
    """Called by the admin CLI."""
    _validate_email(email)
    return create_user(db, email)
```

This file is the whole module. Nothing outside it calls `normalize`, `normalize_email` or `_validate_email`, and nobody ever passes `strategy`. `signup`, `invite`, `create_user` and `SignupError` are used elsewhere.
