---
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill]
runs: 3
---
Review this change from multiple angles before I merge it.

Ticket: "Dashboard users see stale prices. A price on the dashboard must never be more than 30 seconds old."

The PR adds a cache in `prices.py`:

```diff
+from cachetools import TTLCache
+
+_cache = TTLCache(maxsize=1024, ttl=300)
+
 def fetch_price(client, symbol):
-    return client.quote(symbol)
+    if symbol in _cache:
+        return _cache[symbol]
+    price = client.quote(symbol)
+    _cache[symbol] = price
+    return price
```

PR description: "Caches quotes so the dashboard loads faster and users stop seeing stale prices."
