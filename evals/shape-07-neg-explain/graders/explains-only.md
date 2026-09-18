---
type: llm
focus: last_message
weight: 1
---
PASS only if all hold:
- The answer explains that `timed` wraps a function, measures wall-clock duration with `perf_counter`, prints the function name and elapsed seconds, and does so even when the function raises (the `finally`), returning the original result.
- It mentions or correctly implies that `functools.wraps` preserves the wrapped function's name/metadata.
- It does not return a rewritten version or a list of cleanup/simplification recommendations.
FAIL otherwise.
