# Skills catalog

Paste-ready block for any agent that reads `AGENTS.md` (Cursor, Antigravity, Codex, Copilot, …)
but lacks native Agent Skills discovery. Regenerate with `python3 scripts/render-catalog.py`.

---

## Skills

The following skills provide specialized instructions for specific tasks. When a task matches a
skill's description, read the `SKILL.md` at the listed path and follow it before proceeding.
Installed location: `~/.agents/skills/<name>/SKILL.md` (or this repo's `skills/<name>/SKILL.md`).

- **nuclear-break** — Use when a build claims done and needs breaking — "try to break it", "nuclear break" — or when trust-touching work needs dynamic evidence before its review gate; also when a green test suite is the only proof a change works.
- **nuclear-campaign** — Use when the user asks to start a campaign, "take all plannable work and execute", turn vision/backlog/competitor gaps into parallel builds, or hands one broad directive that implies many work items — and no campaign structure exists yet.
- **nuclear-cut** — Use when the user asks to reduce work scope, critique or clean the backlog, "run critique on every open but blocked task", "finish all possible items autonomously", or the open/blocked/deferred item count keeps growing.
- **nuclear-decide** — Use when open decisions, blocked obligations, or sign-offs need the owner's answer — "walk me through the decisions", "talk me through each", "one by one with options" — or when more than one owner decision is pending at once.
- **nuclear-diet** — Use when the user says "min tokens", asks why sessions are expensive, wants an agent setup health-check or CLAUDE.md/AGENTS.md/memory trim, before starting a campaign or multi-agent run, or when a session has crossed days/compactions — any context or token cost needing audit or prevention.
- **nuclear-land** — Use when a change has passed its review gate and needs merging plus outcome recording — "land it", "merge and record", a gate-passed PR is ready — or when merged work was never recorded in the repo's truth docs.
- **nuclear-learn** — Use when asked to mine sessions or outcomes for lessons, extract skills from repeated workflows, "what should become a skill", "what wasted tokens", or for a retro after a campaign, incident, or many-round review gate.
- **nuclear-plan** — Use when about to plan or implement packet-sized, architectural, or trust-touching work — a plan or draft exists or is about to be written — or when past review gates for similar work took many REJECT rounds.
- **nuclear-proof** — Force a skeptical second pass on your own work. Because 'it should work' has never once been true.
- **nuclear-review** — Use when a PR, diff, packet, or trust-touching change hits its review gate, or the user says "redteam", "decorrelated review", or "codex+agy review". Also when work from any model family needs an independent judge, or when one gate's findings span several files and fix work needs parallel lanes.
- **nuclear-roast** — Use when the user asks for a "roast", a full critique of the whole product, solution, or architecture from multiple angles, says "run and run again", or wants a milestone-level adversarial read — solution-scoped, not a change review or backlog sweep.
- **nuclear-run** — Full-rigor delivery loop — detailed plan, adversarial critique/red-team of the plan, execute on green with host-native orchestration, ponytail simplification lens, and verification before claiming done. Use when the user says "nuclear", "wear ponytail + nuclear soul", "plan, critique, red team, execute on green", "nuclear simplification", or invokes /nuclear-run with a task.
- **nuclear-scan** — Use when the user asks "what's next", "what's open for me", "what can be picked up", "status?", "what's left", or pings readiness of named work items ("B28 ready? X ready?") — any read-only backlog question.
- **nuclear-sweep** — Use when the user asks to clean up branches, worktrees, stale checkouts, temp/scratch dirs, or .gitignore across one or more repos, or when stale worktrees accumulate after merged work.
