---
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read]
runs: 3
---
Run duck-learn's step for new models. My `~/.askrubberduck/config.toml`:

```toml
[families]
doer = "anthropic"
reviewers = ["openai:gpt-6-sol:high", "google:gemini-3.1-pro-high"]

[learn]
trial = ["google:gemini-4-pro:high"]
shadow = 3
```

`skills/duck-review/scripts/ledger.py promote` printed:

```
add google:gemini-4-pro:high to review
```

`agy models | skills/duck-review/scripts/ledger.py roster -` printed:

```
new google:gemini-4-flash:high
new google:gemini-4-flash-lite:low
```

Tell me exactly what the config should look like afterwards and what you report. Do not run anything.
