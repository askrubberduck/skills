---
name: nuclear-learn
description: Turn session and delivery evidence into reusable lessons. Use when the user asks for a retrospective, wants to mine sessions or outcomes, asks what should become a skill or what wasted tokens, or after a campaign, incident, or review gate needed many rounds.
---

# Nuclear Learn

The feedback loop: evidence from past work becomes durable updates — a skill, a memory, a rule —
or gets consciously discarded. Lessons that live only in a chat transcript are lessons lost.

Use `$askrubberduck:<name>` as the canonical bundled-skill reference. Before its step starts, resolve
it with the active host's discovered invocation syntax. Preserve `askrubberduck:` when the host
exposes plugin namespaces; use `$<name>` or `<name>` when it exposes skills unqualified or for a
standalone install. If no installed form resolves, stop and name the missing skill; never retry
under another name after that step's side effects start.

## Recipe

1. **Gather evidence, don't reminisce.** Inspect explicit session roots first, then add recognized
   default stores unless the caller explicitly limits scope: Claude transcripts
   (`~/.claude/projects/<dir>/*.jsonl`) and Codex transcripts (`$CODEX_HOME/sessions` and
   `$CODEX_HOME/archived_sessions`, default `~/.codex/...`) alongside recorded outcomes, review
   trajectories, and token stats. Label evidence by its declared host; when an explicit root has no
   label, infer from a recognized schema or mark it `unknown`. Deduplicate only identical canonical
   paths or stable IDs within the same host/schema — never merge unrelated hosts merely because IDs
   match. Do not follow symlinks outside the selected root. A missing, malformed, or unknown requested
   store makes the overall result **partial/incomplete**, but valid stores still proceed; no recognized
   store stops the transcript-mining path. Missing schema fields are `unavailable`, never estimated.
   Extract counts and patterns without copying raw prompts into durable output. Big transcripts are
   mined by script or subagent — never read raw into the main context.
2. **Classify each candidate lesson** by its durable home — one authoritative home per lesson:
   - Repeatable multi-step workflow **the user asks for in words** → a **skill** (new, or a section
     of an existing one — prefer extending; a new skill is a cost).
   - Behavior that must fire on **repo state** rather than phrasing — a campaign left open, a gate
     pending, a stale base — → the checked-in instructions doc. **A skill description matches words;
     it cannot see state.** A driver skill triggered on "continue campaign" sat at zero invocations
     for a month while the owner typed "continue" eleven times.
   - Fact, preference, or project state → **memory**.
   - Rule that must bind every turn → the checked-in instructions doc (CLAUDE.md/AGENTS.md).
   - One-off, derivable, or already recorded → **discard, say so**.
3. **Evidence bar**: 2+ independent occurrences or an explicit owner directive → build it.
   One occurrence → park it as a note in the nearest existing home, not a new artifact.
4. **Apply the updates** — write the skill/memory/rule edit now, not a recommendation to write it.
   While in each home, delete what the new lesson supersedes; stale guidance is worse than none.
5. **Close the loop**: new or edited skills get at least a one-rep pressure check
   (`$askrubberduck:nuclear-proof` discipline applied to authored guidance) before they're trusted.

## Common mistakes

- Saving what the repo already records (git history, code structure) — memory duplicating the repo
  rots; link, don't copy.
- Minting a new skill for every lesson — most lessons are one line in an existing skill.
- Mining only failures — validated approaches that WORKED are equally worth encoding (with their
  evidence), or they'll be re-derived at full cost next time.
- A retro that ends in chat — if nothing was written to a durable home, the learn didn't happen.
