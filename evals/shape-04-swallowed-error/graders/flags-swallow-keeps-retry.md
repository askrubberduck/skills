---
type: llm
focus: last_message
weight: 1
---
In the user's code, `recent_orders` wraps its call in `except Exception: return []`, so a failure looks like "this user has no orders". `fetch_orders` has a bounded retry on `TimeoutError`.

PASS if all hold:
- The answer identifies that `except Exception: return []` turns a failure into a success-looking empty result.
- It handles that as a behavior change, in either of two acceptable ways: (1) it leaves the handler in place and asks or flags it for the user's decision; or (2) it removes or narrows the handler AND states plainly that `recent_orders` will now raise where it used to return `[]`, so the caller/dashboard needs to handle that.
- The bounded retry on `TimeoutError` is kept.

FAIL if the handler is removed with no statement that callers will now see exceptions, if the handler is kept with no comment on the problem, or if the retry is removed as "defensive stuff".
