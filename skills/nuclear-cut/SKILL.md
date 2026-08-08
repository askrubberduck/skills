---
name: nuclear-cut
description: Shrink a backlog by removing obsolete work, merging duplicates, and unblocking viable items. Use when the user asks to cut or clean a backlog, critique open or blocked work, finish every viable item autonomously, or when open, blocked, and deferred work keeps accumulating.
---

# Obligations Critique Sweep

Adversarial sweep over **every** open, blocked, and deferred item with a cut bias: the goal is a
smaller backlog, not a tidier one. "Cut this" findings are first-class, equal to "do this".
Differs from a disposition flow (which acts on IDs the owner names) — this one hunts.

## Sweep

1. Enumerate all items from the repo's registries (status doc, obligations registry, delivery
   backlog, active work dirs). Grep-first; read only surviving items in full.
2. Per item, argue **against its existence** before anything else. Verdict, one of:
   - **CLOSE NOW** — already satisfied, obsolete, or superseded; close with evidence.
   - **CUT** — the need was speculative or the product moved past it; delete, don't park.
   - **MERGE** — duplicate or subset of another item; fold and close.
   - **UNBLOCK** — the stated blocker no longer holds (verify, don't assume); make it pickable.
   - **KEEP** — survives the critique; record the one-sentence justification that saved it.
3. Act autonomously on everything that doesn't need the owner: land CLOSE/MERGE/UNBLOCK edits in the
   registries with evidence, one commit per batch.
4. Items needing the owner (sign-offs, policy calls, anything the doer may not close): queue them and
   run `nuclear-decide` — never close an owner-gated item yourself, never drop it
   silently.

## Report shape

Counts first ("14 items: 4 closed, 2 cut, 1 merged, 2 unblocked, 3 kept, 2 to owner"), then the
per-item verdict list with evidence links.

## Common mistakes

- Parking instead of cutting — "deferred" items that fail the critique die; parking one is still
  backlog debt.
- Closing on assumption — CLOSE NOW requires evidence (the commit, the shipped PR, the doc) that the
  need is met, not a recollection.
- Sweeping only the obligations registry — blocked delivery items and stale active-work dirs are the
  same disease.
