# Skills catalog

Paste-ready block for any agent that reads `AGENTS.md` (Cursor, Antigravity, Codex, Copilot, …)
but lacks native Agent Skills discovery. Regenerate with `python3 scripts/render-catalog.py`.

---

## Skills

The following skills provide specialized instructions for specific tasks. When a task matches a
skill's description, read the `SKILL.md` at the listed path and follow it before proceeding.
Installed location: `~/.agents/skills/<name>/SKILL.md` (or this repo's `skills/<name>/SKILL.md`).

- **but-for-real** — Force a skeptical second pass on your own work. Because 'it should work' has never once been true.
- **campaign-bootstrap** — Use when the user asks to start a campaign, "take all plannable work and execute", turn vision/backlog/competitor gaps into parallel builds, or hands one broad directive that implies many work items — and no campaign structure exists yet.
- **cc-config-diet-audit** — Use when the user asks to health-check their Claude Code setup, find extensions that cost context but never get used, deduplicate memory files against checked-in instructions, or trim CLAUDE.md/AGENTS.md bloat.
- **decision-walkthrough** — Use when open decisions, blocked obligations, or sign-offs need the owner's answer — "walk me through the decisions", "talk me through each", "one by one with options" — or when more than one owner decision is pending at once.
- **multi-lane-fixpass** — Use when one review gate returns findings spanning several files/modules and a single fix-pass agent would serialize them — or when parallel fix teammates start crossing reports, drifting budgets, or flooding the coordinator with idle pings.
- **nuclear-run** — Full-rigor delivery loop — detailed plan, adversarial critique/red-team of the plan, execute on green via Workflow with per-stage model routing, ponytail simplification lens, verify before claiming done. Use when the user says "nuclear", "wear ponytail + nuclear soul", "plan, critique, red team, execute on green", "nuclear simplification", or invokes /nuclear-run <task>.
- **obligations-critique-sweep** — Use when the user asks to reduce work scope, critique or clean the backlog, "run critique on every open but blocked task", "finish all possible items autonomously", or the open/blocked/deferred item count keeps growing.
- **pickable-work-scan** — Use when the user asks "what's next", "what's open for me", "what can be picked up", "status?", "what's left", or pings readiness of named work items ("B28 ready? X ready?") — any read-only backlog question.
- **plan-redteam-coauthor** — Use when about to plan or implement packet-sized, architectural, or trust-touching work — a plan or draft exists or is about to be written — or when past review gates for similar work took many REJECT rounds.
- **redteam-review** — Use when a PR, diff, packet, or trust-touching change hits its review gate, or the user says "redteam", "decorrelated review", or "codex+agy review". Also when a change was authored by a Claude-family agent and needs an independent judge.
- **token-hygiene** — Use when the user says "min tokens", asks why sessions are expensive, before starting a campaign or multi-agent run, or when a session has crossed days/compactions — any time token burn needs auditing or prevention.
- **worktree-git-hygiene** — Use when the user asks to clean up branches, worktrees, stale checkouts, temp/scratch dirs, or .gitignore across one or more repos, or when stale worktrees accumulate after merged work.
