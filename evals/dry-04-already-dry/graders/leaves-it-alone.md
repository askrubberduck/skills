---
type: llm
focus: last_message
weight: 1
---
You are shown only the answer, so here is the ORIGINAL file the user supplied, for comparison:

```python
def backoff(attempt):
    # Gateway drops connections idle for 30 s; keep the cap below that.
    return min(2 ** attempt, 25)
```

The file's only comment records an external constraint (the gateway's 30 s idle drop) that explains the otherwise arbitrary cap of 25 and cannot be recovered from the code. The correct result is no change. PASS only if all hold:
- The answer says the comment stays (or that nothing needs to change), and gives the reason: it carries a constraint the code does not show.
- Any file it returns still has that comment with the same meaning, and the code unchanged.
- It does not invent deletions, rewrites, renames or additional comments to look productive.
FAIL if it deletes the comment, replaces it with a named constant "to make the comment unnecessary", or pads the answer with made-up cleanup.
