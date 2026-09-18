---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Bug report from support, this is everything we have:

> After Tuesday's deploy raised the API rate limit from 100 to 500 requests/min per key, several customers still get HTTP 429 while, by their own count, staying under 500/min. We don't have their actual request rates. It only happens during the afternoon peak. Off-peak nobody can reproduce it.

Facts I can confirm:

- Two worker processes sit behind the load balancer; a key's requests are spread across both. The per-key counters are shared between the workers in Redis. Each worker reads the limit from `limits.yaml` at startup and re-reads it on SIGHUP. The deploy script sends SIGHUP to both workers; nothing checks that they reloaded.
- The load balancer retries a request once, on the other worker, when the first worker takes longer than 1 s to answer. The first attempt is not cancelled, so it still gets counted. At the afternoon peak p95 latency is about 1.3 s; off-peak it is about 200 ms. Retry counts are not logged.
- The 429 log line contains only the API key and a timestamp. No worker pid, no effective limit, no counter value.
- The limiter itself has unit tests for counting and window reset, and they pass.

Why are customers being limited early?
