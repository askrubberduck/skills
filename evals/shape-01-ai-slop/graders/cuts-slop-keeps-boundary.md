---
type: llm
focus: last_message
weight: 1
---
You are shown only the answer, so here is the ORIGINAL file the user supplied, for comparison:

```python
import re

EMAIL_RE = re.compile(r"^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$")


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

Judge the cleaned module the answer returns. PASS only if all hold:
- The `normalize` / `normalize_email` pair is collapsed: there is no pass-through wrapper left (one function, or the normalisation inlined).
- The `strategy` parameter and its `NotImplementedError` branch are gone.
- The email validation rule now lives in one place on the path to the insert, instead of being repeated in `signup`, `invite` and `create_user`.
- An untrusted email is still validated before `db.insert` on the `signup` path, still raising `SignupError("invalid email")`.
- `signup`, `invite`, `create_user` and `SignupError` still exist with the same call signatures.
- For each material removal the answer gives a concrete reason (no callers, single value never passed, duplicate rule), not just "cleaner".
FAIL if validation on the signup path is lost, a public name/signature changes, or a new abstraction (class, registry, config) is introduced.
