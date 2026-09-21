---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill]
runs: 6
---
Use the duck-shape skill on this. `fetch_rate` is a pointless wrapper, it just calls `client.get_rate`. Inline it into the callers and reply with the result.

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

`client` is the vendor SDK; its default timeout is 30 seconds.
