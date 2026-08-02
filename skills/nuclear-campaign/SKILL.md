---
name: nuclear-campaign
description: Use when the user asks to start a campaign, "take all plannable work and execute", turn vision/backlog/competitor gaps into parallel builds, or hands one broad directive that implies many work items — and no campaign structure exists yet.
---

# Campaign Bootstrap

Cold-start: one vague directive becomes packets, plans, and parallel builds. Continuing an existing
campaign is a different job (polling, takeover, merge chaining) — hand that to the repo's campaign
driver once this bootstrap ends.

## Recipe

1. **Survey** the repo's vision/delivery/decision docs plus open registries; scout the product code
   with read-only subagents. Output: a candidate list of shippable changes with evidence, not ideas.
2. **Cut pass.** Argue against each candidate (speculative? superseded? mergeable?). Survivors only.
3. **Carve packets** — one packet per independently shippable change, in the repo's work-item
   convention (e.g. `docs/05-work/YYYY-MM-DD-topic/`). No mega-packet; if two changes can ship
   separately, they are two packets.
4. **Plan each packet** via askrubberduck:nuclear-plan before any build starts.
5. **Launch builds in parallel worktrees** (`.worktrees/<task>/` — never the shared checkout), cheap
   executor agents for mechanical slices, one session per packet.
6. **Hand off**: state the campaign roster (packet, worktree, branch, state) and stop — the
   bootstrap's job ends where the driving loop begins. End this session at the boundary.

## Common mistakes

- Building the first candidate before the cut pass — the survey exists to kill work, not queue it.
- One marathon session bootstrapping AND driving AND reviewing — each packet gets its own session;
  the bootstrap session ends at handoff.
- Packets carved by code area instead of shippable outcome — a packet that can't ship alone isn't one.
- Skipping plan co-authoring because the campaign is "mostly mechanical" — the mechanical slices are
  cheap precisely because the plan was not.
