# askrubberduck skills

Portable process skills mined from real agent sessions: decorrelated review gates, plan
co-authoring, backlog scans, git hygiene, decision facilitation. No repo-specific paths — each
skill detects the host repo's registries (STATUS/OBLIGATIONS/backlog docs) or asks once.

## Install

Plugin marketplace:

```
/plugin marketplace add askrubberduck/skills
/plugin install askrubberduck@askrubberduck
```

Or symlink for local use:

```bash
ln -s "$(pwd)/skills/"* ~/.claude/skills/
```

## Skills

<!-- skills-table:start -->
| Skill | Use when |
|---|---|
| `nuclear-campaign` | the user asks to start a campaign, "take all plannable work and execute", turn vision/backlog/competitor gaps into parallel builds, or hands one broad directive that implies many work items — and no campaign structure exists yet |
| `nuclear-cut` | the user asks to reduce work scope, critique or clean the backlog, "run critique on every open but blocked task", "finish all possible items autonomously", or the open/blocked/deferred item count keeps growing |
| `nuclear-decide` | open decisions, blocked obligations, or sign-offs need the owner's answer — "walk me through the decisions", "talk me through each", "one by one with options" — or when more than one owner decision is pending at once |
| `nuclear-diet` | the user says "min tokens", asks why sessions are expensive, wants a Claude Code setup health-check or CLAUDE.md/memory trim, before starting a campaign or multi-agent run, or when a session has crossed days/compactions — any context or token cost needing audit or prevention |
| `nuclear-plan` | about to plan or implement packet-sized, architectural, or trust-touching work — a plan or draft exists or is about to be written — or when past review gates for similar work took many REJECT rounds |
| `nuclear-proof` | Force a skeptical second pass on your own work |
| `nuclear-review` | a PR, diff, packet, or trust-touching change hits its review gate, or the user says "redteam", "decorrelated review", or "codex+agy review" |
| `nuclear-roast` | the user asks for a "roast", a full critique of the whole product, solution, or architecture from multiple angles, says "run and run again", or wants a milestone-level adversarial read — solution-scoped, not a change review or backlog sweep |
| `nuclear-run` | Full-rigor delivery loop — detailed plan, adversarial critique/red-team of the plan, execute on green via Workflow with per-stage model routing, ponytail simplification lens, verify before claiming done |
| `nuclear-scan` | the user asks "what's next", "what's open for me", "what can be picked up", "status?", "what's left", or pings readiness of named work items ("B28 ready? X ready?") — any read-only backlog question |
| `nuclear-sweep` | the user asks to clean up branches, worktrees, stale checkouts, temp/scratch dirs, or .gitignore across one or more repos, or when stale worktrees accumulate after merged work |
<!-- skills-table:end -->

Generated from skill frontmatter — edit descriptions in `skills/<name>/SKILL.md`, then run
`python3 scripts/render-catalog.py`.

## Conventions baked into every skill

- **Absolute paths, no `cd` chains** — path boilerplate was the #2 token sink in the sessions these
  skills came from.
- **Grep-first, delegate large reads** — no >20KB file pulls into the main context; page with
  offset/limit or send an investigator subagent.
- **Never commit raw CLI stdout** — extract verdicts/findings; raw outputs stay in the scratchpad.
- **End the session at stage boundaries** — plan→build→review transitions are compaction points;
  marathon sessions re-bill the whole window every turn.
- **Fail closed** — a missing reviewer, empty output, or unverified claim is never an implicit pass.

## Credits

`nuclear-proof` adapts Josh Pigford's (Shpigford) "but-for-real" skill; author retained in its
frontmatter metadata.

## Status

v0.1.0 — authored from 15 days of session evidence (baseline failures documented from transcripts).
Discipline skills (`nuclear-review`, `nuclear-plan`, `nuclear-diet`) passed one-rep
subagent pressure scenarios (fail-closed under ship pressure, coauthor-skip temptation,
marathon-split); coverage is thin — file issues on any rationalization loophole an agent finds.
