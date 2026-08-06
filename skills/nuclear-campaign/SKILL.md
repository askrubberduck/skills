---
name: nuclear-campaign
description: Break a large initiative into prioritized workstreams that can ship independently. Use when the user asks to start a campaign, execute all plannable work, turn vision, backlog, or competitor gaps into parallel builds, or provides a broad directive spanning many work items without an existing campaign structure.
---

# Campaign Bootstrap

Cold-start: one vague directive becomes packets, plans, and parallel builds. Continuing an existing
campaign is a different job (polling, takeover, merge chaining) — hand that to the repo's campaign
driver once this bootstrap ends.

Use `$askrubberduck:<name>` as the canonical bundled-skill reference. Before its step starts, resolve
it with the active host's discovered invocation syntax. Preserve `askrubberduck:` when the host
exposes plugin namespaces; use `$<name>` or `<name>` when it exposes skills unqualified or for a
standalone install. If no installed form resolves, stop and name the missing skill; never retry
under another name after that step's side effects start.

## Recipe

1. **Survey** the repo's vision/delivery/decision docs plus open registries; scout the product code
   with read-only subagents. Output: a candidate list of shippable changes with evidence, not ideas.
2. **Cut pass.** Argue against each candidate (speculative? superseded? mergeable?). Survivors only.
3. **Carve packets** — one packet per independently shippable change, in the repo's work-item
   convention (e.g. `docs/05-work/YYYY-MM-DD-topic/`). No mega-packet; if two changes can ship
   separately, they are two packets.
4. **Plan each packet** via `$askrubberduck:nuclear-plan` before any build starts.
5. **Launch builds in parallel worktrees** (`.worktrees/<task>/` — never the shared checkout), cheap
   executor agents for mechanical slices, one session per packet. Apply `$askrubberduck:nuclear-diet`
   rules to the fleet: batched agent traffic, per-stage routing, no raw output in context.
6. **Hand off into a running loop, never into silence.** State the campaign roster (packet, worktree,
   branch, state), then in the same turn give the next iteration an owner: invoke the repo's campaign
   driver, or book the wake that will (`/loop`, a scheduled wakeup, cron), roster as its input. The
   bootstrap's context ends at the boundary; the campaign's momentum must not. A roster with nobody
   holding the next iteration is a stalled campaign wearing the word "handoff". When the campaign's
   packets have merged, `$askrubberduck:nuclear-sweep` clears the worktrees they leave behind.

## Common mistakes

- Building the first candidate before the cut pass — the survey exists to kill work, not queue it.
- One marathon session bootstrapping AND driving AND reviewing — each packet gets its own session;
  the bootstrap session ends at handoff.
- Packets carved by code area instead of shippable outcome — a packet that can't ship alone isn't one.
- Skipping plan co-authoring because the campaign is "mostly mechanical" — the mechanical slices are
  cheap precisely because the plan was not.
- Ending the bootstrap turn with "say the word and I'll start the builds". The go-sign was the
  directive that started the campaign; asking for a second one is where autonomy dies.
