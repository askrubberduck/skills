---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Dry this commit message before I commit. Reply with the message to use.

```
fix(limiter): count retries once

First I looked at limiter.py and saw that allow() was being called twice. Then I
changed line 41 to check the request id. After that I added a set called seen_ids.
Then I updated the test file. I also renamed a variable from c to count on line 12.

Changed limiter.py line 41: added if request_id in seen_ids.
Changed limiter.py line 12: c -> count.
Changed tests/test_limiter.py: added test_retry_counted_once.

The load balancer retries without cancelling the first attempt, so one customer
request was counted twice. seen_ids is bounded to the current window because
request ids are only unique per minute upstream.

Tested: pytest tests/test_limiter.py, 14 passed.
```
