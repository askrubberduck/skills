---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Rebase this branch onto main. What is the command, and what do I do if `fetch.py` conflicts?

```
$ git status -sb
## work...origin/work [ahead 3]
$ git log --oneline main..HEAD
c3 retry test
c2 typo
c1 add retry
```
