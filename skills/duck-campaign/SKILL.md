---
name: duck-campaign
description: Carve a grand vision into independent workstreams that ship without waiting on each other. Use when the user asks to start a campaign, execute all plannable work, turn vision, backlog, or competitor gaps into parallel builds, or provides a broad directive spanning many work items without an existing campaign structure.
---

# Campaign Bootstrap

One vague directive becomes packets, plans, parallel builds — and this skill keeps driving them
until the roster is empty. Bootstrap and continuation are one job here: polling, takeover, and merge
chaining have no separate owner, because a campaign whose next iteration belongs to something else
is a campaign that stalls the first time that something else is not there.

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
   and each one frames itself against this artifact later. A `CUT` verdict ends the campaign.
4. **Carve packets** — one packet per independently shippable change, in the repo's work-item
   convention (e.g. `docs/05-work/YYYY-MM-DD-topic/`). No mega-packet; if two changes can ship
   separately, they are two packets.
5. **Plan each packet** via `duck-plan` before any build starts. **No co-authorship line, no
   execute** — a packet whose committed plan does not name the families that co-authored it has not
   been planned, whatever the roster says. Read the committed plan, never the scratchpad: a driver
   wakes in a new session and the scratchpad is already gone.
6. **Run each packet** through `duck-run`, which owns that packet's execution, verification, and
   superreview, and provisions its own worktree so concurrent builds cannot collide. Launch the runs
   in parallel where the host has subagents; where it has none, run the same packets sequentially in
   one session — the sequencing is the method, parallelism is only how a capable host spends it
   faster. Apply `duck-diet` to the fleet either way: batched agent traffic, no raw output in
   context.
7. **Drive the roster to empty; never hand off into silence.** State the roster (packet, worktree,
   branch, state) where a new session can read it — the durable records home, never the scratchpad —
   then take the next iteration yourself.

   **The loop ends and resumes a session per packet; it is not one long session.** `duck-diet`'s
   rule stands unchanged and this skill is not an exception to it: at each packet boundary the
   roster is written, the session ends, and the next one is booked (`/loop`, a scheduled wakeup,
   cron) with the roster as its input. What the loop owns is that the booking happens — the failure
   this step exists to prevent is a roster with nobody holding the next iteration, not a session
   that ended. A campaign that keeps one session alive across every packet has broken the rule, not
   applied it.

   Each packet's landing removes its own worktree; `duck-sweep` at the end clears whatever landing
   left behind.

   The gap between packets is where a long campaign quietly dies, so between them the turn
   continues: dispatch the next one. A packet that hits an obstacle is re-routed or re-scoped and
   the route recorded, never abandoned — only a refused authorization is an answer rather than an
   obstacle. **A packet that raises an owner decision queues it and the campaign moves to the next
   packet**; it does not sit on the queued question. Independent workstreams that stop for one
   packet's unanswered decision are not independent, whatever the roster says. When a packet's
   execution disproves the campaign shape, re-frame it in writing rather than bending the remaining
   packets around the damage; the campaign may argue its own goal, never substitute one.

## Common mistakes

- Building the first candidate before the cut pass — the survey exists to kill work, not queue it.
- One marathon session bootstrapping AND driving AND reviewing — each packet gets its own session.
  Owning the loop means booking the next session, never holding the current one open.
- Packets carved by code area instead of shippable outcome — a packet that can't ship alone is
  not one.
- Skipping plan co-authoring because the campaign is "mostly mechanical" — the mechanical slices
  are cheap precisely because the plan was not.
- Ending the bootstrap turn with "say the word and I'll start the builds". The go-sign was the
  directive that started the campaign; asking for a second one is where autonomy dies.
