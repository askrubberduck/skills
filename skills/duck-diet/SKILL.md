---
name: duck-diet
description: Put agent context, memory, and token costs on a diet without starving the essential guidance. Use when the user asks for minimum tokens, a session-cost analysis, an agent setup health check, or trimming of CLAUDE.md, AGENTS.md, or memory, when picking which model tier or agent type a stage runs on, or before a long campaign or multi-agent run.
---

# Duck Diet

Reduce measured waste in agent context and work: repeated reads, duplicated guidance, unnecessary
dispatches or retries. Smaller output alone does not establish lower cost or better results.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires a skill's procedure, load that skill and follow the named section
within existing authority; a conditional or routing mention needs no load until it applies.
Respect existing edit authority. An audit reports proposed changes; a request to trim applies
justified local edits and verifies them without another approval request. Preserve owner decisions
and model choices, safety rules, security boundaries, non-obvious constraints, repository
requirements and required workflow evidence.

## Runtime rules

1. **Preserve state at context boundaries.** Compact or isolate a session when useful, not
   automatically per stage. The handoff carries outcome, source/candidate identity, valid evidence,
   unresolved claims and next authorized action; evidence needed later survives scratch cleanup. A
   scheduled continuation needs a supported, authorized host mechanism and a confirmed booking; a
   written next step is not a scheduled task.
2. **Read what the task needs.** Search first, then read relevant sections with enough context,
   paths and working directories explicit. Large output may call for filtering, paging or a bounded
   investigator, not automatically another agent. Never compress away an error, contract or
   contradictory observation.
3. **Route by demonstrated capability.** Reuse the current worker when delegation costs more than
   the separation is worth. Delegating mechanical work to a cheaper model needs a verified pinned
   identity and a named executable check that catches its failure, run before accepting the result;
   without both there is no validated cheaper route. On failure inspect the cause and escalate when
   capability is the limit; two failed attempts at one slice end the experiment. `[models].worker`
   for delegated builders (default the host's choice) and `[models].explore` for read-only search
   (default the host's choice) name the model to ask the host for; identity and check still apply,
   and a same-family worker is never an independent reviewer. Independent or high-risk judgments
   follow [`duck-review`](../duck-review/SKILL.md)'s challenge-selection policy.
4. **Batch communication.** Dispatch bounded independent tasks with the necessary context; request
   findings and decisive evidence, not transcripts or idle updates. More workers or rounds need a
   question they can resolve.
5. **Keep raw output separate.** Raw logs stay in authorized scratch storage; decisive evidence a
   later stage needs goes into the work record before cleanup. Never commit raw session logs or
   private prompt contents.

## Session cost audit

Use actual host usage records; [`duck-learn`](../duck-learn/SKILL.md) owns the transcript-store
locations and how owner tasks are told from derived logs. Count subagents and retries without
double-counting derived logs. Report input, cached input and output usage, elapsed time, repeated
reads/dispatches and retry outcomes. A missing field or inaccessible store is unknown, never zero.

Separate measured tokens, context size and billed cost. Bytes and word counts are size proxies, not
tokens. Cached-input volume alone does not establish the dominant billed cost; conversion needs
model rates and billing semantics. Verify current official pricing before a monetary
recommendation, or leave cost uncomputed; never invent a savings percentage.

Tie each recommendation to an observed source of waste and a check that useful behavior survives.
Claim savings only from a before/after comparison on equivalent work; label estimates and their
assumptions. A long session or a large file is not itself proof of waste.

## Installed-config audit

Inspect the active host's actual configuration, instruction includes, skill/plugin discovery and
broken links, using host diagnostics where they answer a real health question. Distinguish
always-loaded content from on-demand bodies.

Find duplicated or stale guidance and locate its authoritative home. Keep a reference where another
host needs it; never delete a host's only working instruction path. Compare invocation evidence
when available; absence of explicit invocation does not prove an implicitly applied rule unused,
and unreadable logs do not justify disabling a skill.

Remove generic or redundant advice that existing authority covers; do not change an unresolved
owner policy under the label of compression. Report proposed/applied cuts, measured size change
and verification limits. Recheck links and host loading after edits; a shorter configuration that
loses required behavior failed.
