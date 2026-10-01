---
name: duck-decide
description: Walk the owner through the decisions they have been ducking, one at a time. Use when open decisions, blocked obligations, or approvals need the owner's answer, the user asks to walk through decisions or options, or several owner decisions are pending.
---

# Duck Decide

Blocking decisions are presented **one at a time, in full, in plain language**. Batching decisions
produces rushed answers on exactly the items that were queued because they need judgment.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.

## Per decision, present

1. **Context** — what the decision unblocks and why it's the owner's call, in plain language the
   owner can read at a glance.
2. **Options** — each with tradeoffs, gains, and risks stated concretely. Two to four real options;
   one option enumerated is no decision offered.
3. **Recommendation** — pick one and say why, in one sentence.
4. **Wait on the dependent action.** In a standalone decision walkthrough, stop until the owner
   answers before presenting the next decision. Embedded in an executing workflow, return the
   pending decision to the caller so separately authorized independent work can continue. Silence
   never supplies an answer or permission.

After the answer: record it, and whether it is executed or still outstanding, in the owning
registry/doc (decision log, obligations registry — whatever the repo uses) before presenting the
next decision, so a dropped session loses nothing.

## Order

Owner-specified order first; otherwise most-blocking first (the decision gating the most downstream
work). Say how many are in the queue up front ("4 decisions queued; here is 1 of 4").

A queue longer than five gets one question first, because eighteen walkthroughs in a row get the
answer "later". Offer: one at a time; take every recommendation; take every recommendation except
the policy items; later. Name the policy items — money, risk, anything that changes what an
operator or user can do — since they never ride in a batch. Then walk only the ones the owner kept,
and record each batched decision as the owner's answer with the words that took it. The owner may
batch; the doer never does.

## Common mistakes

- Hiding material cost or schedule tradeoffs. Include them when relevant to the owner's decision,
  alongside functionality, maintainability and risk; sunk effort does not justify keeping a defect.
- Presenting a decision already made elsewhere — check the decision log first; re-litigating settled
  calls burns the owner's attention.
- Executing an action that depends on an unanswered decision; continuing independent work is the
  caller's responsibility, not implied approval of the blocked action.
