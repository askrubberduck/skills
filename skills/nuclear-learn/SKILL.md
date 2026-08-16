---
name: nuclear-learn
description: Turn session and delivery evidence into reusable lessons. Use when the user asks for a retrospective, wants to mine sessions or outcomes, asks what should become a skill or what wasted tokens, or after a campaign, incident, or review gate needed many rounds.
---

# Nuclear Learn

The feedback loop: evidence from past work becomes durable updates — a skill, a memory, a rule —
or gets consciously discarded. Lessons that live only in a chat transcript are lessons lost.

## Recipe

1. **Gather evidence, don't reminisce.** Session transcripts — Claude
   `~/.claude/projects/<dir>/*.jsonl`, Codex `$CODEX_HOME/sessions` and `archived_sessions` —
   alongside recorded outcomes, review trajectories, and token stats. Extract **counts**: repeated
   directives, repeated failures, repeated tool patterns. Filter by event timestamp, not file mtime,
   and count independent owner/root tasks, not JSONL files: deduplicate canonical session IDs; fold
   subagents, workflow journals, forwarded copies, retries, and cross-host reviewer executions into
   their parent task when lineage is available; report roots and delegated logs separately. Generated
   prompts, task notifications, and tool results are tool evidence, never owner directives. Big
   transcripts are mined by script or subagent, never read raw into the main context, and no raw
   prompt text goes into durable output. Missing or malformed store? Say so and mark the result
   partial.
2. **Classify each candidate lesson** by its durable home — one authoritative home per lesson:
   - Repeatable multi-step workflow **the user asks for in words** → a **skill** (new, or a section
     of an existing one — prefer extending; a new skill is a cost).
   - Behavior that must fire on **repo state** rather than phrasing — a campaign left open, a gate
     pending, a stale base — → the checked-in instructions doc. **A skill description matches words;
     it cannot see state.**
   - Fact, preference, or project state → **memory**.
   - A **defect class** the doer repeated → the repo's defect ledger, which `nuclear-proof` reads
     before every pass. Classes compound; instances do not.
   - Rule that must bind every turn → the checked-in instructions doc (CLAUDE.md/AGENTS.md).
   - One-off, derivable, or already recorded → **discard, say so**.
3. **Evidence bar**: 2+ independent occurrences or an explicit owner directive → build it.
   One occurrence → park it as a note in the nearest existing home, not a new artifact.
4. **Apply the updates** — write the skill/memory/rule edit now, not a recommendation to write it.
   While in each home, delete what the new lesson supersedes; stale guidance is worse than none.
   Policy files are the limit, and the limit is authority rather than effort: an edit to a skill, a
   gate, or an instruction file is trust-touching, so it travels the same plan and review path as
   any other change to them — derive it, write it up, hand it on, never land it unreviewed.
5. **Close the loop**: procedural guidance (a skill, a workflow rule) gets one rep before it's
   trusted — reserve one occurrence as a holdout BEFORE deriving (derive from the rest; deriving
   from every occurrence leaves nothing to test with), state the expected outcome, then run the
   guidance against that holdout — an occurrence it was NOT derived from — and attack the result
   with `nuclear-proof` discipline; a failed rep sends the guidance back to draft.
   Directive-derived guidance (step 3's owner-directive path) has no occurrence to reserve — it
   stays draft until its first real occurrence, which serves as its holdout rep. Memory entries
   instead record their source occurrence. Guidance that has never fired is a draft, not a lesson.

## Common mistakes

- Saving what the repo already records (git history, code structure) — memory duplicating the repo
  rots; link, don't copy.
- Mining only failures — validated approaches that WORKED are equally worth encoding (with their
  evidence), or they'll be re-derived at full cost next time.
- A retro that ends in chat — if nothing was written to a durable home, the learn didn't happen.
