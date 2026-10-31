---
name: duck-learn
description: Turn session and delivery evidence into reusable lessons, so each mistake is only paid for once. Use when the user asks for a retrospective, wants to mine sessions or outcomes, asks what should become a skill or where tokens were wasted, or after a campaign, incident, or review gate needed many rounds.
---

# Duck Learn

Evidence from past work becomes durable updates — a skill, a memory, a rule — or is consciously
discarded. Lessons that live only in a chat transcript are lost.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires a skill's procedure, load that skill and follow the named section
within existing authority; a conditional or routing mention needs no load until it applies.

## Recipe

1. **Gather evidence.** `$LEDGER` below means
   `python3 "<absolute path of ../duck-review/scripts/ledger.py>"`, resolved from this skill's
   directory and typed out in every command.
   - **Numbers first.** `$LEDGER thresholds` reads `~/.askrubberduck/dispatches.tsv` and prints
     lesson candidates — a pin's outage rate, a pin whose reviews among its last twenty dispatches
     found no unique blocker, minutes that drifted — each an occurrence for step 3's bar.
   - **New models.** `$LEDGER roster -` reads host model ids on stdin (`agy models | $LEDGER
     roster -`; codex prints none, so the owner names its new pins) and prints ids nobody has
     configured, trialled or dispatched; `promote` prints each trial pin's verdict: still `shadow`,
     or `replace`, `add` or `drop` once decided; a `replace` lists, with severity, each incumbent
     cause the trial missed. `[learn].discover` (default `propose`) decides what follows: `off`
     ignores both; `propose` queues each through [`duck-decide`](../duck-decide/SKILL.md); `auto`
     puts at most one new pin per family into `[learn].trial`, applies each `replace`, `add` or
     `drop` verdict to `~/.askrubberduck/config.toml`, taking the pin out of `[learn].trial` in the
     same edit, and reports it. That file is the owner's config, not policy: step 4's review path
     does not apply.
   - **Sources.** Known transcript stores: Claude `~/.claude/projects/<dir>/*.jsonl`, Codex
     `$CODEX_HOME/sessions` and `archived_sessions`. Locate another host's store before the mine,
     or mark the result partial and say so; likewise for a missing or malformed store. Also use
     recorded outcomes, review trajectories and token stats.
   - **Count.** Count repeated directives, failures and tool patterns as independent owner tasks,
     not files: fold every derived log — subagents, retries, forwarded copies — into its parent
     by event timestamp, not file mtime, reporting roots and delegated logs apart. Generated
     prompts, task notifications and tool results are tool evidence, never owner directives.
   - **Never raw.** Mine big transcripts by script or subagent, never into the main context, and
     put no raw prompt text in durable output. [Mining the stores](references/mine.md) has the row
     shapes, the wrappers to strip and what an extractor must report.
2. **Classify each candidate lesson** by its one authoritative home:
   - Repeatable multi-step workflow the user asks for in words → a skill; prefer extending an
     existing one, since a new skill is a cost.
   - Behavior that must fire on repo state (a campaign left open, a gate pending, a stale base)
     → the checked-in instructions doc; a skill description matches words and cannot see state.
   - Fact, preference or project state → memory.
   - A defect class the doer repeated → `defect-classes.md`, which
     [`duck-proof`](../duck-proof/SKILL.md) reads before every pass. Classes compound; instances
     do not.
   - Rule that must bind every turn → the checked-in instructions doc (CLAUDE.md/AGENTS.md).
   - One-off, derivable or already recorded → discard, and say so.
3. **Evidence bar**: 2+ independent occurrences or an explicit owner directive → build it. One
   occurrence → park it as a note in the nearest existing home, not a new artifact.
4. **Apply the updates**: write the edit now, not a recommendation, and delete what the new lesson
   supersedes in each home. An edit to a skill, a gate or an instruction file is trust-touching:
   derive it, write it up and hand it on through the same plan and review path as any other change
   to them, never landed unreviewed.
5. **Close the loop**: procedural guidance (a skill, a workflow rule) gets one rep before it is
   trusted. Reserve one occurrence as a holdout before deriving — at exactly two, derive from the
   other — state the expected outcome, run the guidance against the holdout and attack the result
   with [`duck-proof`](../duck-proof/SKILL.md) discipline. A failed rep returns the guidance to
   draft, and the redraft waits for a fresh occurrence as its holdout; a used holdout never
   validates twice. Directive-derived guidance stays draft until its first real occurrence. Check
   observable behavior, not whether the agent repeats the rule: execute a counterexample, verify
   final artifacts, and record the candidate guidance, prompt, oracle and result. Pair opposite
   user preferences when testing agreement bias. Compare against an old-guidance baseline before
   claiming improvement; one rep proves only that case. Memory entries instead record their source
   occurrence.

## Common mistakes

- Saving what the repo already records (git history, code structure): link, don't copy.
- Mining only failures; approaches that worked are equally worth encoding, with their evidence.
