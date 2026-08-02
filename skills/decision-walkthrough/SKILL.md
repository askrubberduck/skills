---
name: decision-walkthrough
description: Use when open decisions, blocked obligations, or sign-offs need the owner's answer — "walk me through the decisions", "talk me through each", "one by one with options" — or when more than one owner decision is pending at once.
---

# Decision Walkthrough

Blocking decisions are presented **one at a time, in full, in plain language**. Batching decisions
produces rushed answers on exactly the items that were queued because they need judgment.

## Per decision, present

1. **Context** — what the decision unblocks and why it's the owner's call (2–3 sentences, no jargon).
2. **Options** — each with tradeoffs, gains, and risks stated concretely. Two to four real options;
   one option enumerated is no decision offered.
3. **Recommendation** — pick one and say why, in one sentence.
4. **Stop and wait.** No next decision, no other content, until the owner answers.

After the answer: record it in the owning registry/doc (decision log, obligations registry —
whatever the repo uses) before presenting the next decision, so a dropped session loses nothing.

## Order

Owner-specified order first; otherwise most-blocking first (the decision gating the most downstream
work). Say how many are in the queue up front ("4 decisions queued; here is 1 of 4").

## Common mistakes

- Batching "the three small ones" into one message — the owner asked one-at-a-time for a reason.
- Options with tradeoffs measured in build effort — weigh functionality, extendability, security;
  never implementation cost.
- Presenting a decision already made elsewhere — check the decision log first; re-litigating settled
  calls burns the owner's attention.
- Continuing past an unanswered decision because the next one "doesn't depend on it".
