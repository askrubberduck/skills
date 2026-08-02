---
name: token-hygiene
description: Use when the user says "min tokens", asks why sessions are expensive, before starting a campaign or multi-agent run, or when a session has crossed days/compactions — any time token burn needs auditing or prevention.
---

# Token Hygiene

Cache-read of marathon sessions dominates real burn (measured: 93%+ of a 7.3B-token fortnight).
Everything here attacks that or the next four sinks, in order of measured size.

## The six rules

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
   general-purpose + strong model only for adversarial/synthesis/trust stages. Check the agent-type
   default, not just the model flag.
5. **Batch agent traffic.** Poll teammates at round boundaries; never relay no-op idle pings into the
   coordinator context. Compress subagent output contracts ("return table, no prose").
6. **Raw output stays out of git and out of context.** CLI stdout, logs, diffs: extract the decisive
   lines; full text lives in the scratchpad only.

## Audit mode

Asked "why was this expensive": per-session, report cache_read vs output tokens, session span,
compaction count, `cd`/redeclaration counts, results >20KB — each mapped to the rule above that was
broken. Numbers first, then the two highest-leverage fixes only.

## Common mistakes

- Treating cache reads as free because they're discounted — the window re-bills every turn; length
  is the cost driver.
- "One more turn, then I'll split" across a stage boundary — the split is cheapest exactly at the
  boundary, before the next stage's context piles on.
- Compressing prose while pasting whole files — rule 3 outweighs terse wording 100:1.
