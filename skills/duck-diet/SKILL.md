---
name: duck-diet
description: Put agent context, memory, and token costs on a diet without starving the essential guidance. Use when the user asks for minimum tokens, a session-cost analysis, an agent setup health check, or trimming of CLAUDE.md, AGENTS.md, or memory, when picking which model tier or agent type a stage runs on, or before a long campaign or multi-agent run.
---

# Duck Diet

Reduce measured waste in agent context and work: repeated reads, duplicated guidance, unnecessary
dispatches or retries. Smaller output alone does not prove lower cost or better results.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires the procedure of a skill, load that skill. Follow its named section
within existing authority. A conditional or routing mention needs no load until it applies.

Respect existing edit authority. An audit reports proposed changes. A request to trim applies
justified local edits and verifies them without another approval request. Preserve owner decisions
and model choices, safety rules, security boundaries, non-obvious constraints, repository
requirements and required workflow evidence.

## Runtime rules

1. **Preserve state at context boundaries.** Compact or isolate a session when useful, not
   automatically per stage. The handoff carries the fields
   [`duck-proof`](../duck-proof/SKILL.md)'s "Evidence and handoff" lists. A scheduled continuation
   needs a supported, authorized host mechanism and a confirmed booking; a written next step is not
   a scheduled task.
2. **Read what the task needs.** Search first, then read relevant sections with enough context
   and explicit paths and working directories. Large output can need filtering, paging or a
   bounded investigator, not automatically another agent. Never compress away an error, contract
   or contradictory observation.
3. **Route by demonstrated capability.** If delegation costs more than the separation is worth,
   reuse the current worker. Delegation of mechanical work to a cheaper model needs a
   verified pinned identity and a named executable check that catches its failure; run the check
   before you accept the result. Without both, no cheaper route is validated. On failure,
   examine the cause and escalate when capability is the limit; two failed attempts at one slice
   end the experiment. `[models].worker` for delegated workers (default the host's choice) and
   `[models].explore` for read-only search (default the host's choice) name the model to ask the
   host for; identity and check still apply. A same-family worker is never an independent
   reviewer. Independent or high-risk judgments follow
   [`duck-review`](../duck-review/SKILL.md)'s challenge-selection policy.
4. **Batch communication.** Dispatch bounded independent tasks with necessary context. Request
   findings and decisive evidence, not transcripts or idle updates. More workers or rounds need a
   question they can resolve.
5. **Keep raw output separate.** Raw logs stay in authorized scratch storage. Before cleanup, put
   decisive evidence a later stage needs into the work record. Never commit raw session logs or
   private prompt contents.

## Session cost audit

Use actual host usage records; [`duck-learn`](../duck-learn/SKILL.md) owns the transcript-store
locations and how owner tasks are told from derived logs. Count subagents and retries without
double-counting derived logs. Report input, cached input and output usage, elapsed time, repeated
reads/dispatches and retry outcomes. A missing field or inaccessible store is unknown, never zero.

Separate measured tokens, context size and billed cost. Bytes and word counts are size proxies,
not tokens. Cached-input volume alone does not prove the dominant billed cost; conversion needs
model rates and billing semantics. Before a monetary recommendation, verify current official
pricing, or leave cost uncomputed. Never invent a savings percentage.

Tie each recommendation to an observed source of waste and a check that useful behavior survives.
Claim savings only from a before/after comparison on equivalent work. Label estimates and their
assumptions. A long session or large file is not itself proof of waste.

## Installed-config audit

Examine the active host's actual configuration, instruction includes, skill/plugin discovery and
broken links. Use host diagnostics where they answer a real health question. Separate
always-loaded content from on-demand bodies.

Find duplicated or stale guidance and locate its authoritative home. Keep a reference where
another host needs it. Never delete a host's only working instruction path. Compare invocation
evidence when available. Absence of explicit invocation does not prove an implicitly applied rule
unused, and unreadable logs do not justify disabling a skill.

Remove generic or redundant advice that existing authority covers. Do not change an unresolved
owner policy as a compression. Report proposed and applied cuts, measured size
change and verification limits. After edits, recheck links and host loading. A shorter
configuration that loses required behavior failed.
