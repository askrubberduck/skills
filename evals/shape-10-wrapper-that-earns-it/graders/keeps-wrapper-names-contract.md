---
type: llm
focus: last_message
weight: 1
---
You are shown only the answer, so here is what the user supplied:

`rates.py`:

```python
def fetch_rate(client, currency):
    try:
        return client.get_rate(currency, timeout=2.0)
    except VendorTimeout as exc:
        raise RateUnavailable(currency) from exc
```

Callers:

```python
# checkout.py
try:
    rate = fetch_rate(client, order.currency)
except RateUnavailable:
    rate = cached_rate(order.currency)

# invoice.py
rate = fetch_rate(client, invoice.currency)

# quote.py
rate = fetch_rate(client, currency)
```

`fetch_rate` is not a pass-through: it pins a 2-second timeout (the SDK default is 30 s) and translates the vendor's `VendorTimeout` into the domain exception `RateUnavailable`, which `checkout.py` catches.

PASS only if all hold:
- The answer's recommendation is to keep `fetch_rate` (pushing back on the request), not to inline it.
- It names both things the wrapper protects: the 2.0 s timeout and the `VendorTimeout` → `RateUnavailable` mapping (or that `checkout.py` depends on `RateUnavailable`).
- It says what inlining would cost: the timeout and the exception handling repeated in three callers, or callers coupled to the vendor exception.
It may additionally show what faithful inlining would look like, as long as the recommendation is to keep the wrapper.
FAIL if it inlines the call as requested, or inlines it while dropping the timeout or the exception mapping, or agrees that the wrapper is pointless.
