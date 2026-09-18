---
type: llm
focus: last_message
weight: 1
---
Judge only the commit message the answer proposes (its code block); the surrounding explanation may quote the removed narration. PASS only if all hold:
- The subject line keeps the conventional `fix(limiter): ...` format.
- It keeps the why: the load balancer retries without cancelling the first attempt, so a request was counted twice.
- It keeps the constraint: `seen_ids` is bounded to the current window because request ids are only unique per minute upstream.
- It keeps the verification line (pytest tests/test_limiter.py, 14 passed) in some form.
- The first-person editing narrative and the per-line "Changed ... line N" restatement of the diff are gone.
- It is clearly shorter than the original.
FAIL otherwise.
