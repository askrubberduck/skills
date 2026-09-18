---
type: llm
focus: last_message
weight: 1
---
The working directory is empty and no backlog was supplied. PASS only if all hold:
- The answer says it found no backlog / registry / status document (or no files at all) to answer from.
- It asks the user where the work is tracked (file, issue tracker, PRs, elsewhere), or asks them to supply it.
- It does NOT conclude that nothing is open, that everything is done, or that there is no work.
FAIL otherwise.
