---
type: llm
focus: last_message
weight: 1
---
PASS only if all hold:
- It identifies the cause as `first()` returning `values[1]` (index 1) where the contract requires index 0.
- It says both `primary` and `secondary` are affected because they route through `first`.
- It explicitly says `singleton` is NOT affected (it indexes `values[0]` itself / does not call `first`).
- The repair it points to is one change inside `first`, not separate changes in `primary` and `secondary`.
FAIL if any of the four is missing, or if it proposes a broader redesign as the needed fix.
