---
type: llm
focus: last_message
weight: 1
---
PASS only if all hold:
- It provides an updated script in which `--verbose` is a boolean flag (e.g. `action="store_true"`) and, when set, each counted file name is printed; the total is still printed.
- It does not diagnose a failure: no root-cause analysis, no reproducer, no claims that the original script is broken.
FAIL otherwise.
