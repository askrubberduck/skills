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

| Skill | Gate/task it covers |
|---|---|
| `nuclear-review` | Decorrelated codex+agy review of a PR/diff/packet; fix-pass loop to two-family APPROVE |
| `nuclear-plan` | Red team co-authors the plan before build; kills REJECT churn at the code gate |
| `nuclear-scan` | Read-only "what's next / what's open / is X ready" backlog answers |
| `nuclear-sweep` | Verify-then-delete sweep of branches, worktrees, scratch dirs across repos |
| `nuclear-decide` | Owner decisions one at a time: options, tradeoffs, gains, risks, wait |
| `nuclear-cut` | Adversarial backlog sweep with cut bias; close/cut/merge/unblock autonomously |
| `nuclear-campaign` | One broad directive → surveyed, cut, carved into packets, parallel worktree builds |
| `nuclear-diet` | Token + context diet: six runtime rules, session audit, installed-config audit |
| `nuclear-proof` | Skeptical second pass on your own work before claiming done |
| `nuclear-run` | Full-rigor delivery loop: plan, adversarial critique, execute on green, verify |

## Conventions baked into every skill

- **Absolute paths, no `cd` chains** — path boilerplate was the #2 token sink in the sessions these
  skills came from.
- **Grep-first, delegate large reads** — no >20KB file pulls into the main context; page with
  offset/limit or send an investigator subagent.
- **Never commit raw CLI stdout** — extract verdicts/findings; raw outputs stay in the scratchpad.
- **End the session at stage boundaries** — plan→build→review transitions are compaction points;
  marathon sessions re-bill the whole window every turn.
- **Fail closed** — a missing reviewer, empty output, or unverified claim is never an implicit pass.

## Status

v0.1.0 — authored from 15 days of session evidence (baseline failures documented from transcripts).
Discipline skills (`nuclear-review`, `nuclear-plan`, `nuclear-diet`) passed one-rep
subagent pressure scenarios (fail-closed under ship pressure, coauthor-skip temptation,
marathon-split); coverage is thin — file issues on any rationalization loophole an agent finds.
