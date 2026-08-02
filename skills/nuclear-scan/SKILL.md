---
name: nuclear-scan
description: Use when the user asks "what's next", "what's open for me", "what can be picked up", "status?", "what's left", or pings readiness of named work items ("B28 ready? X ready?") — any read-only backlog question.
---

# Pickable Work Scan

Read-only. Answers "what's next" from the repo's own registries without a full-doc re-read and
without acting on anything. Writes (close/approve/park) route to the repo's disposition workflow.

## Locate registries (detect, don't configure)

Look for, in order: `STATUS.md`, `OBLIGATIONS.md`, a delivery/backlog doc
(`docs/03-delivery/README.md`, `BACKLOG.md`, `TODO.md`), active work dirs (`docs/05-work/`),
open PRs (`gh pr list`). Use whichever exist; if none do, say so and ask where the backlog lives —
once, then remember the answer for the session.

## Scan

Grep-first: pull item IDs, states, and blockers with targeted `grep`/`rg` over the registries —
never full-file Reads of large docs. Only Read the specific sections of items that survive the
filter. For readiness pings on named IDs, check exactly those items plus their gate state
(PR open? review verdict? CI green?) and nothing else.

## Answer shape

One table, then one sentence of recommendation:

| Item | State | Blocked on | Pickable? |
|---|---|---|---|

- **Pickable** = open AND unblocked AND not awaiting an owner decision.
- Items awaiting the owner's decision/sign-off are listed separately — they are *the owner's* next
  actions, not pickable work.
- If the user asked about specific IDs, answer those first, in the order asked.

## Common mistakes

- Re-deriving the whole backlog for a two-ID ping — scan only what was asked.
- Treating "in review" as pickable — a change at its gate belongs to the reviewer, not a new doer.
- Mutating anything. This skill never edits registries; it hands off to disposition/close flows.
