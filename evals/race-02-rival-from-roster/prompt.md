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
reviewers = ["google:gemini-3.1-pro-high"]

[bounds]
dispatch_timeout = "7m"
```

Before spending anything, show me the exact command you would use to dispatch the rival, with every variable it needs bound. Do not run it.
