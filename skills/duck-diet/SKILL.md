---
name: duck-diet
description: Put agent context, memory, and token costs on a diet without starving the essential guidance. Use when the user asks for minimum tokens, a session-cost analysis, an agent setup health check, or trimming of CLAUDE.md, AGENTS.md, or memory, when picking which model tier or agent type a stage runs on, or before a long campaign or multi-agent run.
---

# Duck Diet

Reduce measured waste in agent context and work. Find repeated reads, duplicated guidance,
unnecessary dispatches or retries before recommending a new setup. Smaller output alone does not
establish lower cost or better results.

Follow the user's language unless they ask otherwise; preserve commands, paths, identifiers, quoted errors and verdicts.
Respect existing edit authority. An audit alone reports proposed changes; a request to trim applies
justified local edits and verifies them without another approval request. Preserve owner decisions,
security boundaries and required workflow evidence.

## Runtime rules

1. **Preserve state at context boundaries.** Use host compaction or an isolated session when useful,
   not automatically per stage. Carry outcome, source/candidate identity, valid evidence, unresolved
   claims and next authorized action into the handoff. Evidence needed later must survive scratch
   cleanup. A scheduled continuation requires a supported, authorized host mechanism and a confirmed
   booking; a written next step is not a scheduled task.
2. **Read what the task needs.** Search first, then read relevant sections with enough surrounding
   context to understand them. Keep paths and working directories explicit. Large output may call
   for filtering, paging or a bounded investigator; it does not automatically justify another agent.
   Do not compress away an error, contract or contradictory observation.
3. **Route by demonstrated capability.** Reuse the current worker for small tasks when delegation
   adds more overhead than useful separation. For mechanical work worth delegating, a cheaper model
   needs a verified pinned identity and a named executable check that catches its failure. Run that
   check before accepting the result; without identity or a suitable check, do not claim a validated
   cheaper route. If it fails, inspect the cause and escalate when capability is the limit, rather
   than retrying the same attempt. Two failed attempts at the same slice end that routing experiment.
   Use `duck-review`'s challenge-selection policy for independent or high-risk judgments; honor the
   owner's model choices and repository requirements.
4. **Batch useful communication.** Dispatch bounded independent tasks with the necessary context.
   Request findings and decisive evidence, not transcripts or repeated idle updates. More workers
   and more rounds need a question they can resolve.
5. **Keep raw output separate.** Extract the evidence needed for the decision. Keep raw logs in
   authorized scratch storage; preserve decisive evidence in the work record before cleanup when
   a later stage needs it. Avoid committing raw session logs or private prompt contents.

## Session cost audit

Use actual host usage records. `duck-learn` owns known transcript-store locations and counting rules;
include subagents and retries without double-counting derived logs. Report available input, cached
input and output usage, measured elapsed time, repeated reads/dispatches and retry outcomes.
A missing field or inaccessible store is unknown, never zero.

Separate measured tokens, context size and billed cost. Bytes or word counts are size proxies, not
measured tokens. Cached-input volume alone does not establish the dominant billed cost: conversion
requires the applicable model rates and billing semantics. Verify current official pricing when a
monetary recommendation needs it, or leave cost uncomputed. Do not invent a savings percentage.

Tie each recommendation to an observed source of waste and a check that useful behavior survives.
Compare before and after on equivalent work when claiming savings; label estimates and their
assumptions. A long session or a large file is not itself proof of waste.

## Installed-config audit

Inspect the active host's actual configuration, instruction includes, skill/plugin discovery and
broken links. Use available host diagnostics when they answer a real health question. Distinguish
always-loaded content from on-demand bodies instead of assuming all installed files are loaded.

Find duplicated or stale guidance and locate its authoritative home. Keep a reference where another
host needs it; do not delete a host's only working instruction path. Compare invocation evidence
when available, but absence of explicit invocation does not prove an implicitly applied rule was
unused. Unreadable logs do not justify disabling a skill.

Preserve non-obvious constraints, owner decisions and safety rules. Remove generic or redundant
advice when existing authority covers it. Do not change an unresolved owner policy under the label
of compression. Report proposed/applied cuts, measured size change and verification limits. Recheck
links and host loading after edits; a shorter configuration that loses required behavior failed.
