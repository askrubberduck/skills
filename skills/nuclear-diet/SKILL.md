---
name: nuclear-diet
description: Use when the user says "min tokens", asks why sessions are expensive, wants a Claude Code setup health-check or CLAUDE.md/memory trim, before starting a campaign or multi-agent run, or when a session has crossed days/compactions — any context or token cost needing audit or prevention.
---

# Nuclear Diet

Context cost has two bodies: what sessions burn at runtime (cache-read of marathon sessions was
93%+ of a measured 7.3B-token fortnight) and what the installed config bills every turn before
work even starts. Both diets here; the product of the audit is deletions.

## The six runtime rules

1. **End the session at stage boundaries.** Plan→build, build→review, packet→packet: new session or
   `/compact`. Every turn re-bills the whole window; a forced auto-compaction pays a summarization
   tax AND loses state. One session per packet.
2. **Absolute paths, once.** No `cd` chains, no re-declared `VAR=/long/path` boilerplate per Bash
   call (measured: 1500+ redeclarations of one 80-char path in a fortnight). Long scratchpad root →
   `ln -s` a short alias once.
3. **Grep-first; delegate big reads.** Nothing >20KB into the main context: page with offset/limit,
   or send an investigator subagent that returns a summary. Main context is the most expensive place
   to store a file.
4. **Route by stage, both model AND agent type.** Mechanical work → cheap-model executor agents;
   general-purpose + strong model only for adversarial/synthesis/trust stages.
5. **Batch agent traffic.** Poll teammates at round boundaries; never relay no-op idle pings into the
   coordinator context. Compress subagent output contracts ("return table, no prose").
6. **Raw output stays out of git and out of context.** CLI stdout, logs, diffs: extract the decisive
   lines; full text lives in the scratchpad only.

## Session audit mode

Asked "why was this expensive": per-session, report cache_read vs output tokens, session span,
compaction count, `cd`/redeclaration counts, results >20KB — each mapped to the rule above that was
broken. Numbers first, then the two highest-leverage fixes only.

## Installed-config audit mode

Everything always-loaded (CLAUDE.md chain, memory index, plugin skill descriptions, hooks context)
is billed every turn of every session:

1. **Installation health**: `claude doctor` if available; version, plugin cache integrity, broken
   symlinks in skills dirs.
2. **Always-loaded inventory**: user + project CLAUDE.md/AGENTS.md (follow `@includes`), memory
   index, enabled plugins. Estimate each block's size; rank by cost.
3. **Usage cross-check**: grep recent session transcripts (`~/.claude/projects/<dir>/*.jsonl`) for
   each plugin/skill actually invoked. Loaded-never-invoked for weeks = disable candidate.
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
