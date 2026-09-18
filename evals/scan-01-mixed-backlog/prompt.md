---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
What's next? Here is our `STATUS.md`:

| ID | Title | State | Notes |
|---|---|---|---|
| W-01 | Add CSV export | done | merged in #41 |
| W-02 | Rate-limit login | open | — |
| W-03 | Migrate to Postgres 16 | blocked | waiting on W-05 |
| W-04 | Dark mode | in review | PR #52 open, awaiting reviewer |
| W-05 | Upgrade ORM | open | — |
| W-06 | Drop legacy API v1 | needs owner decision | owner to choose the sunset date |
| W-07 | Fix flaky upload test | open | blocked on CI runner access (infra ticket INF-9, still open) |
