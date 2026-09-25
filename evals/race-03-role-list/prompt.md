---
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read]
runs: 3
---
Race it: add a `--json` flag to `report.py` that prints the same rows as JSON. Two model families, one problem.

My `~/.askrubberduck/config.toml`:

```toml
[families]
doer = "anthropic"
reviewers = ["openai:gpt-6-sol:high"]

[models]
race = ["google:gemini-3.8-flash-high"]

[bounds]
dispatch_timeout = "7m"
```

Before spending anything, tell me which model you would dispatch as the rival and why, and show the command. Do not run it.
