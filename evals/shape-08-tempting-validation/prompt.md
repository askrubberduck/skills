---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Everything here is checked two or three times. Cut the duplication and reply with the three files.

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

`post_withdraw` is the only caller of `WalletService.withdraw`, and `withdraw` is the only caller of `debit`. API clients match on the two `BadRequest` messages. Requests for the same user can arrive concurrently.
