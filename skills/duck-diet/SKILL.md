---
name: duck-diet
description: Put agent context, memory, and token costs on a diet without starving the essential guidance. Use when the user asks for minimum tokens, session-cost analysis, an agent setup health check, CLAUDE.md, AGENTS.md, or memory trimming, when picking which model tier or agent type a stage runs on, or before a long campaign or multi-agent run.
---

# Duck Diet

Context cost has two bodies: what sessions burn at runtime — cache-read of a marathon session
dominates it — and what the installed config bills every turn before work even starts. Both diets
here; the product of the audit is deletions.

## The six runtime rules

1. **End the session at stage boundaries.** Plan→build, build→review, packet→packet: new session or
   `/compact`. Every turn re-bills the whole window; a forced auto-compaction pays a summarization
   tax AND loses state. One session per packet. Two conditions first, because a boundary is a
   handoff and not an exit: the next step is named and dispatched or scheduled, and **anything the
   next stage must read has left the scratchpad** — `$SP` dies with the session, and the review gate
   refuses to dispatch without receipts a new session can no longer see. Unmet, the boundary waits.
2. **Absolute paths, once.** No `cd` chains, no re-declared `VAR=/long/path` boilerplate per Bash
   call. Long scratchpad root: `ln -s` a short alias once.
3. **Grep-first; delegate big reads.** Nothing >20KB into the main context: page with offset/limit,
   or send an investigator subagent that returns a summary. Main context is the most expensive place
   to store a file.
4. **Stage routing: start cheap, bounce up on failure.** Route by stage, both model AND agent type.
   - **Mechanical work** (investigation, scripted edits, rebases, clerical verification, recording)
     defaults to cheap-model executor agents — but only with a pinned model whose self-report is
     verified, and a named gate (tests, compiler, a dedicated check script) that catches the stage's
     failure, executed and its result recorded before the stage's output is used. No pin or no gate,
     no cheap tier.
   - **Bounce up on failure.** A cheap agent that fails its gate, or fails to converge on a second
     attempt at the same slice, has answered the routing question: re-dispatch that slice to the
     strongest tier, or to an agent with elevated reasoning limits, carrying the failure context
     with it. A passing gate proves cheap was sufficient, never that it was best — the bounce is
     what stops a wrong cheap route from becoming the answer.
   - **Strong by default.** Trust-touching, adversarial, and synthesis stages are never mechanical,
     whatever the stage type: they get general-purpose agents on the strongest tier. Everything else
     inherits the current model.
5. **Batch agent traffic.** Poll teammates at round boundaries; never relay no-op idle pings into
   the coordinator context. Compress subagent output contracts ("return table, no prose").
6. **Raw output stays out of git and out of context.** CLI stdout, logs, diffs: extract the decisive
   lines; full text lives in the scratchpad only.

## Session audit mode

Asked "why was this expensive": per-session, report cache_read vs output tokens, session span,
compaction count, `cd`/redeclaration counts, results >20KB — each mapped to the rule above that was
broken. Numbers first, then the two highest-leverage fixes only.

## Installed-config audit mode

Everything always-loaded (CLAUDE.md chain, memory index, plugin skill descriptions, hooks context)
is billed every turn of every session:

1. **Installation health**: use the active host's diagnostics when available (`claude doctor` for
   Claude Code; `codex --version` plus plugin/skill configuration checks for Codex); inspect plugin
   cache integrity and broken symlinks in skill directories.
2. **Always-loaded inventory**: user + project CLAUDE.md/AGENTS.md (follow `@includes`), memory
   index, enabled plugins. Estimate each block's size; rank by cost.
3. **Usage cross-check**: read the host's transcripts — `duck-learn` step 1 owns the
   transcript-store locations; use those rather than re-deriving them — and count what each
   always-loaded block was actually used for. Loaded-never-invoked for weeks = disable
   candidate. Report counts and metadata, never raw prompt content. Can't find a store, or it's
   malformed? Say so and mark the audit partial — a missing store is never zero usage.
4. **Dedupe**: local memory files repeating checked-in CLAUDE.md facts — keep the checked-in copy,
   delete the memory. Same for AGENTS.md vs copilot-instructions duplication: one canonical file.
5. **Trim to non-derivable**: a CLAUDE.md line earns its place only if a fresh session could NOT
   derive it from the repo. Owner decisions, invariants, and workflow rules stay.
6. Present cuts as one list with per-item size saved; apply on approval.

## Common mistakes

- Treating cache reads as free because they're discounted — the window re-bills every turn; length
  is the cost driver.
- "One more turn, then I'll split" across a stage boundary — the split is cheapest exactly at the
  boundary.
- Compressing prose while pasting whole files — rule 3 outweighs terse wording 100:1.
- Trimming config rules the owner put there deliberately — when a line reads like a decision, ask.
- Deleting the checked-in copy and keeping the local memory — backwards; checked-in serves every
  agent, not one machine.
