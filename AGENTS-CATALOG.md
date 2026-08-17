# Skills catalog

Paste-ready block for any agent that reads `AGENTS.md` (Cursor, Antigravity, Codex, Copilot, …)
but lacks native Agent Skills discovery. Regenerate with `python3 scripts/render-catalog.py`.

---

## Skills

The following skills provide specialized instructions for specific tasks. When a task matches a
skill's description, read the `SKILL.md` at the listed path and follow it before proceeding.
Installed location: `~/.agents/skills/<name>/SKILL.md` (or this repo's `skills/<name>/SKILL.md`).

- **nuclear-break** — Attack a finished build to expose false confidence before review. Use when a build claims completion, security-, privacy-, or data-sensitive work lacks dynamic evidence, only a green test suite supports the claim, or the user asks to "try to break it" or run a "nuclear break".
- **nuclear-campaign** — Break a large initiative into prioritized workstreams that can ship independently. Use when the user asks to start a campaign, execute all plannable work, turn vision, backlog, or competitor gaps into parallel builds, or provides a broad directive spanning many work items without an existing campaign structure.
- **nuclear-cut** — Shrink a backlog by removing obsolete work, merging duplicates, and unblocking viable items. Use when the user asks to cut or clean a backlog, critique open or blocked work, finish every viable item autonomously, or when open, blocked, and deferred work keeps accumulating.
- **nuclear-decide** — Resolve owner decisions and sign-offs one at a time. Use when open decisions, blocked obligations, or approvals need the owner's answer, the user asks to walk through decisions or options, or several owner decisions are pending.
- **nuclear-diet** — Reduce agent context, memory, and token costs without losing essential guidance. Use when the user asks for minimum tokens, session-cost analysis, an agent setup health check, CLAUDE.md, AGENTS.md, or memory trimming, or before a long campaign or multi-agent run.
- **nuclear-dry** — Cut comment and docstring noise so only unobvious decisions, contracts, and traps survive. Use when generated code or tests carry narration, storytelling, or change history in comments, when a comment restates the line under it, before committing or reviewing generated code, or the user asks to dry, prune, or de-slop comments.
- **nuclear-frame** — Analyze a system and settle its target design before planning begins. Use when the user asks for system analysis, system design, architecture options, or requirements and constraints before planning, when implementation is about to start against an architecture nobody wrote down, or when a change is large, architectural, security-, privacy-, or data-sensitive.
- **nuclear-land** — Merge approved work, update project records, and clean up its branch and worktree. Use when a change has passed its review gate, the user says to land, merge, push, ship, tag, cut a release, or "merge and release", a gate-passed PR is ready, or merged work was never recorded in status or outcome documentation.
- **nuclear-learn** — Turn session and delivery evidence into reusable lessons. Use when the user asks for a retrospective, wants to mine sessions or outcomes, asks what should become a skill or what wasted tokens, or after a campaign, incident, or review gate needed many rounds.
- **nuclear-pingpong** — Alternate test-writing and implementation between two decorrelated model families, one failing test per rally. Use when the user says "ping-pong" or "nuclear pingpong", wants TDD across two models, a spec is clear but its edge cases are not, or generated tests keep passing without catching real defects.
- **nuclear-plan** — Catch architectural and implementation risks before coding begins. Use when about to plan OR about to implement large, architectural, security-, privacy-, or data-sensitive work — including when implementation is about to start and no plan exists yet — when a draft plan needs independent critique, or when similar work previously failed several review rounds.
- **nuclear-proof** — Give completed work a skeptical second pass before anyone trusts it. Use when an implementation claims completion, the evidence is mostly "it should work", the user asks to verify or prove the work, or before handing a change to an independent review gate.
- **nuclear-race** — Race two decorrelated model families independently against the same frozen problem, then adjudicate on executed evidence. Use when the user says "race it" or "nuclear race", wants two models tackling the same problem at once, a task has several plausible implementations worth comparing, or single-attempt builds of similar work kept failing review.
- **nuclear-review** — Run one independent cross-model superreview and synthesize an evidence-backed APPROVE, REJECT, or NOTE. Use when a PR or diff is ready to review, a security-, privacy-, or data-sensitive change reaches its release gate, the user says "gate it" or asks for a red-team or independent second opinion. It reviews and judges; it does not fix, repeat, or land.
- **nuclear-roast** — Critique an entire product, solution, or architecture from multiple angles. Use when the user asks for a roast or repeated full critique, or wants a milestone-level adversarial assessment of the standing solution rather than a change review or backlog sweep.
- **nuclear-run** — Plan, implement, test, and independently review a high-risk change. Use when the user requests end-to-end delivery with adversarial plan critique, says "nuclear" or "plan, critique, red team, execute on green", asks for a nuclear run or nuclear simplification, says "wear ponytail + nuclear soul", or invokes nuclear-run with a task.
- **nuclear-scan** — Find ready, blocked, and remaining work without changing anything. Use when the user asks what is next, open, ready, left, or available to pick up, requests status, or asks whether a named work item is ready.
- **nuclear-sweep** — Clean stale branches, worktrees, checkouts, scratch directories, and ignore rules. Use when the user asks for repository cleanup across one or more repos, or when stale worktrees and temporary artifacts have accumulated after merged work.
