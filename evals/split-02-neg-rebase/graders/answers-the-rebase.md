---
type: llm
focus: last_message
weight: 1
---
PASS only if it gives a working rebase command (`git rebase main`, optionally after fetching, or `git rebase origin/main`) and says how to handle a conflict in `fetch.py`: resolve the file, `git add` it, `git rebase --continue`, with `git rebase --abort` as the way out.
FAIL if it turns the request into an audit of what the branch contains, proposes splitting the branch, or refuses to answer without more information.
