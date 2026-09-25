---
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read]
runs: 3
---
Run the release gate on PR #31 (an ordinary change: one file, 40 lines, no security or data impact). Before dispatching anything, tell me exactly which reviewers you will send, how each one's verdict counts toward the gate, and what happens if one of them times out.

My `~/.askrubberduck/config.toml`:

```toml
[families]
doer = "anthropic"
reviewers = ["openai:gpt-6-sol:high", "google:gemini-3.1-pro-high"]

[learn]
trial = ["google:gemini-3.8-flash-high"]
shadow = 3
```

`~/.askrubberduck/dispatches.tsv` has no rows for `gemini-3.8-flash-high` yet. Export to OpenAI and Google is authorized. Do not dispatch yet.
