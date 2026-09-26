---
name: duck-learn
description: Turn session and delivery evidence into reusable lessons, so each mistake is only paid for once. Use when the user asks for a retrospective, wants to mine sessions or outcomes, asks what should become a skill or where tokens were wasted, or after a campaign, incident, or review gate needed many rounds.
---

# Duck Learn

The feedback loop: evidence from past work becomes durable updates — a skill, a memory, a rule —
or gets consciously discarded. Lessons that live only in a chat transcript are lessons lost.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.

## Recipe

1. **Gather evidence, don't reminisce.** `$LEDGER` below is `python3` with the absolute path of
   `../duck-review/scripts/ledger.py`, resolved from this skill's directory.
   - **Numbers first.** `$LEDGER thresholds` reads
     `~/.askrubberduck/dispatches.tsv` and prints lesson candidates — a pin's outage rate, a pin
     whose reviews among its last twenty dispatches found no unique blocker, minutes that drifted —
     each one an occurrence for step 3's bar.
   - **New models.** `$LEDGER roster -` reads host model ids on stdin (`agy models | $LEDGER
     roster -`; codex prints none, so the owner names its
     new pins) and prints ids nobody has configured, trialled or dispatched; `promote` prints each
     trial pin's verdict: still `shadow`, or `replace`, `add` or `drop` once decided.
     `[learn].discover` (default `auto`) decides what follows: `off` ignores both; `propose` queues
     each through `duck-decide`; `auto` puts at most one new pin per family into `[learn].trial` and
     applies each `replace`, `add` or `drop` verdict to `~/.askrubberduck/config.toml`, taking the
     pin out of `[learn].trial` in the same edit, and reports it. This is the owner's config, not a
     policy file: step 4's review path does not apply to it.
   - **Sources.** Transcript-store locations — Claude `~/.claude/projects/<dir>/*.jsonl`, Codex
     `$CODEX_HOME/sessions` and `archived_sessions` — are the hosts whose stores are known, not the
     whole set: another host has its store located before the mine, or the result is partial and
     says so. Alongside them, recorded outcomes, review trajectories, and token stats. Missing or
     malformed store? Say so and mark the result partial.
   - **Count.** Extract counts: repeated directives, repeated failures, repeated tool patterns.
     Count independent owner tasks, not files: fold every derived log — subagents, retries,
     forwarded copies — into its parent, by event timestamp rather than file mtime, roots and
     delegated logs reported apart. Generated prompts, task notifications, and tool results are
     tool evidence, never owner directives.
   - **Never raw.** Big transcripts are mined by script or subagent, never read raw into the main
     context, and no raw prompt text goes into durable output. [Mining the
     stores](references/mine.md) has the row shapes, the wrappers to strip and what any extractor
     must report.
2. **Classify each candidate lesson** by its durable home — one authoritative home per lesson:
   - Repeatable multi-step workflow **the user asks for in words** → a **skill** (new, or a section
     of an existing one — prefer extending; a new skill is a cost).
   - Behavior that must fire on **repo state** rather than phrasing — a campaign left open, a gate
     pending, a stale base — → the checked-in instructions doc. **A skill description matches words;
     it cannot see state.**
   - Fact, preference, or project state → **memory**.
   - A **defect class** the doer repeated → `defect-classes.md`, which `duck-proof` reads
     before every pass. Classes compound; instances do not.
   - Rule that must bind every turn → the checked-in instructions doc (CLAUDE.md/AGENTS.md).
   - One-off, derivable, or already recorded → **discard, say so**.
3. **Evidence bar**: 2+ independent occurrences or an explicit owner directive → build it.
   One occurrence → park it as a note in the nearest existing home, not a new artifact.
4. **Apply the updates** — write the edit now, not a recommendation to write it.
   While in each home, delete what the new lesson supersedes; stale guidance is worse than none.
   Policy files are the limit, and the limit is authority rather than effort: an edit to a skill, a
   gate, or an instruction file is trust-touching, so it travels the same plan and review path as
   any other change to them — derive it, write it up, hand it on, never land it unreviewed.
5. **Close the loop**: procedural guidance (a skill, a workflow rule) gets one rep before it's
   trusted. Reserve one occurrence as a holdout BEFORE deriving — at exactly two, derive from the
   other — state the expected outcome, then run the guidance against that holdout and attack the
   result with `duck-proof` discipline; a failed rep sends the guidance back to draft, and the
   redraft waits for a fresh occurrence to serve as its holdout — the used one cannot validate
   twice, so at exactly two a failed rep parks the lesson until a third arrives. Check
   observable behavior, not whether the agent repeats the new rule: execute a counterexample,
   verify final artifacts, and record the candidate guidance, prompt, oracle and result. Pair
   opposite user preferences when testing agreement bias. Use an old-guidance baseline before
   claiming improvement; one successful rep proves only that case.
   Directive-derived guidance has no occurrence to reserve — it stays draft until its first real
   occurrence, which serves as its holdout rep. Memory entries instead record their source
   occurrence. Guidance that has never fired is a draft, not a lesson.

## Common mistakes

- Saving what the repo already records (git history, code structure) — memory duplicating the repo
  rots; link, don't copy.
- Mining only failures — validated approaches that WORKED are equally worth encoding (with their
  evidence), or they'll be re-derived at full cost next time.
