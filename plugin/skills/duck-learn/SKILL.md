---
name: duck-learn
description: Turn session and delivery evidence into reusable lessons, so each mistake is only paid for once. Use when the user asks for a retrospective, wants to mine sessions or outcomes, asks what should become a skill or where tokens were wasted, or after a campaign, incident, or review gate needed many rounds.
---

# Duck Learn

Evidence from past work becomes a durable update (a skill, a memory or a rule), or the doer
discards it on purpose. A lesson only in a chat transcript is lost.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires the procedure of a skill, load that skill. Follow its named section
within existing authority. A conditional or routing mention needs no load until it applies.

## Recipe

1. **Gather evidence.**
   - **Numbers first.** Read `~/.askrubberduck/dispatches.tsv`. A pin's outage rate above 20%, or
     its minutes drifting by half from its mean, is a lesson candidate. Each is one occurrence for
     step 3's bar.
   - **New models.** Compare `agy models` with the pins in `~/.askrubberduck/config.toml`. Codex
     prints no list, so the owner names its new pins. Queue each new pin through
     [`duck-decide`](../duck-decide/SKILL.md); the owner changes that file, not this skill.
   - **Sources.** Known transcript stores: Claude `~/.claude/projects/<dir>/*.jsonl`, Codex
     `$CODEX_HOME/sessions` and `archived_sessions`. Locate another host's store before the mine,
     or mark the result partial and say so. Mark a missing or malformed store partial too. Use
     recorded outcomes, review trajectories and token stats.
   - **Count.** Count repeated directives, failures and tool patterns as independent owner tasks,
     not files. Fold every derived log (subagents, retries, forwarded copies) into its parent
     by event timestamp, not file mtime. Report roots and delegated logs apart. Generated prompts,
     task notifications and tool results are tool evidence, never owner directives.
   - **Never raw.** Mine big transcripts by script or worker, never into the main context. Put no
     raw prompt text in durable output. [Mining the stores](references/mine.md) has the row
     shapes, the wrappers to strip and what an extractor must report.
2. **Classify each candidate lesson** by its one authoritative home:
   - A repeatable multi-step workflow the user asks for in words goes to a skill. Prefer to
     extend an existing one; a new skill is a cost.
   - Behavior that must fire on repo state (a campaign left open, a gate pending, a stale base)
     goes to the checked-in instructions doc. A skill description matches words and cannot see
     state.
   - A fact, preference or project state goes to memory.
   - A defect class the doer repeated goes to `defect-classes.md`, which
     [`duck-proof`](../duck-proof/SKILL.md) reads before every pass. Classes compound; instances
     do not.
   - A rule that must bind every turn goes to the checked-in instructions doc (CLAUDE.md/AGENTS.md).
   - Discard a one-off, derivable or recorded lesson; say so.

3. **Evidence bar**: Build a lesson with 2+ independent occurrences or an explicit owner directive.
   Park a single occurrence as a note in the nearest existing home, not a new artifact.
4. **Apply the updates**: Write the edit now, not a recommendation, and delete what it supersedes
   in each home. An edit to a skill, a gate or an instruction file is trust-touching. Derive it,
   document it and send it through the plan and review path of other changes to them. Never
   land it unreviewed.
5. **Close the loop**: Procedural guidance (a skill, a workflow rule) gets one rep before anyone
   trusts it. Before you derive, reserve one occurrence as a holdout; at exactly two, derive from
   the other. State the expected outcome. Run the guidance against the holdout, and attack the
   result with [`duck-proof`](../duck-proof/SKILL.md) discipline. A failed rep returns the
   guidance to draft, and the redraft waits for a fresh holdout occurrence. A used holdout
   never validates twice. Directive-derived guidance stays draft until its first real occurrence.
   Check observable behavior, not whether the agent repeats the rule. Execute a counterexample,
   verify final artifacts, and record the candidate guidance, prompt, oracle and result. To test
   agreement bias, pair opposite user preferences. Before you claim improvement, compare against
   an old-guidance baseline. One rep proves only that case. Memory entries instead record their
   source occurrence.

## Common mistakes

- Link to what the repo records (git history, code structure); do not copy it.
- Encode what worked, not only failures, with evidence.
