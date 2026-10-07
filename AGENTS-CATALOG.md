# Bring your agent a duck

No native skill discovery? Give this block to any agent that reads `AGENTS.md` (Cursor, Antigravity, Codex, Copilot, …)
but lacks native Agent Skills discovery. Regenerate with `python3 scripts/render-catalog.py`.

---

## Skills

The duck reads before it speaks. When a task matches a skill below, read its `SKILL.md` and
follow it before proceeding. Challenge the claim, run the check, keep the evidence.
English is the home language; match task intent across languages. Follow the user's
requested language, keeping commands, paths, identifiers, quoted errors and verdicts unchanged.
Installed location: `~/.agents/skills/<name>/SKILL.md` (or this repo's `skills/<name>/SKILL.md`).

- **duck-break** — Use when asked to break or red-team a system, exercise hostile inputs, or test behavioral claims dynamically.
- **duck-campaign** — Use when asked to turn a vision, backlog or broad directive into independent workstreams and execute them.
- **duck-cut** — Use when asked to clean a backlog, retire obsolete work, merge duplicates or unblock viable items.
- **duck-decide** — Use when asked to walk through owner decisions, options, blocked obligations or pending approvals.
- **duck-diet** — Use when asked to audit agent setup, reduce context or token costs, trim instructions or memory, or choose model tiers.
- **duck-dry** — Use when asked to trim redundant code comments, docstrings, commit messages or PR descriptions. Not ordinary prose editing.
- **duck-frame** — Use when asked to analyze a system, settle requirements and boundaries, or choose architecture before planning.
- **duck-land** — Use when asked to merge approved work, run a release process, or record and clean up work already merged.
- **duck-learn** — Use when asked for a retrospective, to mine sessions and outcomes, or extract reusable lessons and skill improvements.
- **duck-plan** — Use when asked to plan implementation, challenge a plan, identify consequential assumptions or define acceptance checks.
- **duck-proof** — Use when asked to prove necessity, correctness or simplicity, verify a plan or implementation, or check work before review.
- **duck-race** — Use when asked to race models, ping-pong a task, compare independent implementations or generate adversarial tests across model families.
- **duck-review** — Use when asked to review code, local changes, PRs, plans or documents, give an independent verdict or release gate, or assess and draft replies to received review comments.
- **duck-roast** — Use when asked to roast a whole solution, repeat full critique or audit a codebase for over-engineering and deletions.
- **duck-run** — Use when asked to duck a task, apply selected findings or carry work through planning, implementation and verification.
- **duck-scan** — Use when asked what work is ready, blocked, open or remaining, or for repository status without changes.
- **duck-shape** — Use when asked to simplify code, remove abstractions or bloat, compare structures or check the shape of completed work.
- **duck-split** — Use when asked to check task scope, extract unrelated work or split a branch, PR, document or plan.
- **duck-sweep** — Use when asked to clean stale branches, worktrees, checkouts, scratch directories or ignore rules.
- **duck-why** — Use when asked to diagnose a failure or ineffective fix, or trace who introduced a value, guard or behavior and why. Not a plain explanation of how code works.
