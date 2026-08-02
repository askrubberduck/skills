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
| `redteam-review` | Decorrelated codex+agy review of a PR/diff/packet; fix-pass loop to two-family APPROVE |
| `plan-redteam-coauthor` | Red team co-authors the plan before build; kills REJECT churn at the code gate |
| `pickable-work-scan` | Read-only "what's next / what's open / is X ready" backlog answers |
| `worktree-git-hygiene` | Verify-then-delete sweep of branches, worktrees, scratch dirs across repos |
| `decision-walkthrough` | Owner decisions one at a time: options, tradeoffs, gains, risks, wait |
| `obligations-critique-sweep` | Adversarial backlog sweep with cut bias; close/cut/merge/unblock autonomously |

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
Not yet pressure-tested with subagent scenarios; treat wording as v0 and file issues on any
rationalization loophole an agent finds.
