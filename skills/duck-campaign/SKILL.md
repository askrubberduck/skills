---
name: duck-campaign
description: Carve a grand vision into independent workstreams that ship without waiting on each other. Use when the user asks to start a campaign, execute all plannable work, turn a vision, a backlog, or competitor gaps into parallel builds, or provides a broad directive spanning many work items without an existing campaign structure.
---

# Duck Campaign

One vague directive becomes packets, plans, parallel builds — and this skill keeps driving them
until the roster is empty. Bootstrap and continuation are one job here: polling, takeover, and merge
chaining have no separate owner, because a campaign whose next iteration belongs to something else
is a campaign that stalls the first time that something else is not there.

Follow the user’s language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.

## Recipe

1. **Survey & scan.** Run `duck-scan` over the repo's registries, read the vision, delivery, and
   decision docs, and scout the product code with read-only subagents. Output: a candidate list of
   shippable changes with evidence, not ideas.
2. **Cut pass.** Run `duck-cut` — or apply its cut bias by hand — against the candidate list. Argue
   against each candidate (speculative? superseded? mergeable?). Survivors only. For each survivor,
   name the outcome that dies if it is never built — a candidate with no such answer is a habit, not
   work. Re-run this pass whenever a packet grows mid-flight: the cut is a standing lens, not a
   one-time gate at the survey.
3. **Frame the campaign.** Run `duck-frame` on the system the surviving candidates land in — not
   on the candidates themselves, because a frame that decomposes work is a second planner. It
   settles the macro-architecture, the boundaries every packet must respect, and the failure
   models; a campaign running on an unwritten architecture is a collision waiting to happen. The
   work item here is the campaign itself — open its record now if the repo has none — so the
   frame's durable home is the campaign's directory, never a packet's: packets do not exist yet,
   and each one frames itself against this artifact later. A `CUT` verdict ends the campaign;
   `OWNER DECISION` ends the turn, because there is no packet yet to move on to.
4. **Carve packets** — one packet per independently shippable change, in the repo's work-item
   convention (e.g. `<work-items>/YYYY-MM-DD-topic/`). No mega-packet; if two changes can ship
   separately, they are two packets. The converse holds too: **findings that share a seam are one
   packet**, carved first, whose acceptance evidence is the executable check over that seam — the
   class-level check `duck-proof`'s ledger demands — and each finding is a case of it. One packet
   per finding is how a campaign spends a review round per instance.
5. **Plan each packet** via `duck-plan` before dependent implementation. Record its outcome,
   checks, selected challenge and actual participants. A solo plan stays labeled solo; independent
   input required by repository policy cannot be replaced by a claim. Read the durable record,
   not scratch paths from an earlier session. Local execution does not require a committed plan.
6. **Run each packet** through `duck-run`, which owns that packet's execution, verification, and
   superreview, and provisions its own worktree so concurrent builds cannot collide. Launch the runs
   in parallel where the host has subagents; where it has none, run the same packets sequentially in
   one session — the sequencing is the method, parallelism is only how a capable host spends it
   faster. Apply `duck-diet` to the fleet either way: batched agent traffic, no raw output in
   context.
7. **Drive the roster to empty; never hand off into silence.**
   - **Roster.** State it (packet, worktree, branch, state) where a new session can read it — the
     durable records home, never the scratchpad — then take the next iteration yourself.
   - **Context and resumption.** Apply `duck-diet` using the host's real capabilities. At a
     handoff preserve the roster, candidate identities, valid evidence and next authorized actions.
     Use compaction or isolated sessions when useful; neither a forced reset nor one marathon
     session is universally required. Book a scheduled continuation only if the host supports it
     and the task authorizes it, and verify the booking. Otherwise continue in the current session
     as possible and state any external limit; do not invent a scheduled wakeup. Landing removes
     its worktree; `duck-sweep` can clear authorized leftovers at the end.
   - **Obstacles and decisions.** The gap between packets is where a long campaign quietly dies,
     so between them the turn continues: dispatch the next one. A packet that hits an obstacle is
     re-routed or re-scoped and the route recorded, never abandoned — only a refused authorization
     is an answer rather than an obstacle. **A packet that raises an owner decision queues it and
     the campaign moves to the next packet**; it does not sit on the queued question. Independent
     workstreams that stop for one packet's unanswered decision are not independent, whatever the
     roster says. When a packet's execution disproves the campaign shape, re-frame it in writing
     rather than bending the remaining packets around the damage; the campaign may argue its own
     goal, never substitute one.

## Common mistakes

- Building the first candidate before the cut pass — the survey exists to kill work, not queue it.
- Losing packet state during a reset or compaction, or claiming a continuation that was never
  booked.
- Packets carved by code area instead of shippable outcome — a packet that can't ship alone is
  not one.
- Skipping a required independent challenge, or running extra co-authors without a question they
  can help resolve.
- Ending the bootstrap turn with "say the word and I'll start the builds". The go-sign was the
  directive that started the campaign; asking for a second one is where autonomy dies.

Carry the owner's endpoint through every packet: local-only means local execution and verification,
not automatic commits, PRs or landing. Do not install a scheduler or expand authority to keep a
campaign running. Queued decisions block their dependent actions, not independent packets.
