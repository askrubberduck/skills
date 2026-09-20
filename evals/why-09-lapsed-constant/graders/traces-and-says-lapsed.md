---
type: llm
focus: last_message
weight: 1
---
PASS only if all hold:
- It names commit 9f3c2aa and PR #12 as where the constant was introduced.
- It gives the stated reason: `load_all()` held the whole export in memory and ran out of memory on the 2GB workers.
- It says that reason no longer holds (lapsed), because c41d7e0 replaced `load_all()` with streaming, so rows are no longer held in memory.
- It notes that the cap still has an effect today: `stream` silently stops after 100 rows.
FAIL if it treats the question as a failure to reproduce (asks for or invents a reproducer, a traceback, a "root cause" of a bug), or if it says the reason still holds.
