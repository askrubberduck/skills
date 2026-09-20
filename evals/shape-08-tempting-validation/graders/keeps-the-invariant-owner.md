---
type: llm
focus: last_message
weight: 1
---
You are shown only the answer, so here is what the user supplied:

`handler.py`:

```python
def post_withdraw(request, service):
    """HTTP boundary: request.form is untrusted."""
    try:
        amount = int(request.form["amount"])
    except (KeyError, ValueError):
        raise BadRequest("amount must be an integer")
    if amount <= 0:
        raise BadRequest("amount must be positive")
    return service.withdraw(request.user_id, amount)
```

`service.py`:

```python
class WalletService:
    def __init__(self, repo):
        self.repo = repo

    def withdraw(self, user_id, amount):
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("amount must be a positive integer")
        if self.repo.balance(user_id) < amount:
            raise InsufficientFunds(user_id)
        return self.repo.debit(user_id, amount)
```

`repo.py`:

```python
class WalletRepo:
    def balance(self, user_id):
        return self.balances[user_id]

    def debit(self, user_id, amount):
        with self.lock:
            balance = self.balances[user_id]
            if balance - amount < 0:
                raise InsufficientFunds(user_id)
            self.balances[user_id] = balance - amount
            return self.balances[user_id]
```

Facts: `post_withdraw` is the only caller of `withdraw`, which is the only caller of `debit`; requests for one user can be concurrent.

PASS only if all hold:
- `repo.debit` still checks, inside the lock, that the balance cannot go negative, and still raises `InsufficientFunds`. This is the only race-free check and must survive.
- The handler still rejects a missing/non-integer amount and a non-positive amount with the two original `BadRequest` messages.
- At least one genuinely redundant check is removed from `WalletService.withdraw`: the amount re-validation, the unlocked balance pre-check, or both.
- The answer gives a reason the repo check stays (it is the one made under the lock / the service pre-check is check-then-act and racy / the repo owns the invariant).
FAIL if the locked check in `debit` is removed or moved outside the lock, if a `BadRequest` message is dropped or changed, or if nothing is removed.
