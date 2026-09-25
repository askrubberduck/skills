---
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read]
runs: 3
---
We're carrying this task with duck-run. I rewrote `billing/proration.py` (about 200 lines of logic: day counts, mid-cycle plan changes, refunds), its unit tests pass locally, and I committed the candidate. The owner wants it released, which needs the independent release gate. Codex and Gemini are both available and export to them is authorized.

What exactly do you do between now and dispatching the gate reviewers? Do not run anything.
