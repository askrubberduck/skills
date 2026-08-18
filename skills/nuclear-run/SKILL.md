---
name: nuclear-run
description: Plan, implement, test, and independently review a high-risk change. Use when the user requests end-to-end delivery with adversarial plan critique, says "nuclear" or "plan, critique, red team, execute on green", asks for a nuclear run or nuclear simplification, says "wear ponytail + nuclear soul", or invokes nuclear-run with a task.
---

# Nuclear Run

The bundled directive stack the user otherwise types as a preamble. Argument: the task.

## Stages

1. **Ground.** Run `nuclear-frame`: it reads the project's quality bar, traces the real flow end to
   end, and settles the shape before anything is planned or written. Laziness shortens the
   solution, never the reading. Its `READY` artifact comes back here; this stage decides what
   follows, and a `CUT` verdict ends the run.
2. **Plan.** Detailed decomposition: units of work, gates per unit, acceptance evidence.
   Steel-man at least one alternative decomposition before committing; first idea is a candidate, not a decision.
   Packet-sized or trust-touching: co-author the plan via `nuclear-plan` instead of
   drafting solo. In doubt about the size, default up — the solo path is bought with one committed
   line, `solo-drafted because: …`; a routing choice without a receipt is the doer grading its own
   rigor. **Do not enter stage 4 until the committed plan carries its co-authorship
   line** — an uncoauthored plan is the rejections arriving later instead of now.
3. **Critique (adversarial, pre-code) — for solo-drafted plans only.** When `nuclear-plan` ran in
   stage 2, its multi-round concurrence loop already **is** this stage; a second gate on a
   co-authored plan is redundancy, not rigor. Otherwise: red-team the plan — wrong decomposition,
   missing edge cases, simpler design that deletes a concept. Default the critic toward refute, use
   the strongest available tier, fold findings, loop until the plan survives.
4. **Execute on green.** Use the host's native staged or multi-agent orchestration when available;
   otherwise execute the settled stages sequentially. Route stages per `nuclear-diet`'s stage-routing
   rule — the full cheap-routing precondition lives there; stage 6 additionally re-checks its output
   (a record is checked by reading it back); any unmet precondition runs the stage on the
   inherited model.
   TDD for code units: failing test first, minimal pass, then simplify.
5. **Ponytail lens throughout.** Delete before add; stdlib/existing helper before new code; one
   home per fact; smallest
   diff after full understanding. Simplify touched code before building on it; clear superseded paths
   as the last step of each unit. No migrations, no back-compat shims unless the repo demands them.
   **Write for a senior reader.** Code explains itself; comments supplement it. Run
   `nuclear-dry` over each unit's diff before stage 6 — it settles what a comment must carry and
   where the prose that does not belong in code goes instead.
6. **Verify.** Run the project's gates (tests/build/vet or doc gates) — a gate that takes minutes
   runs in the background, so the turn keeps working while it does; a blocked loop is the cost, and
   an unread result is the trap — then invoke `nuclear-proof`
   on your own diff — it leaves `proof-<unit>.md`, or `$SP/proof-r1.md` when stage 7's review is
   next (`$SP`: `nuclear-review`'s dispatch scratchpad), which is where the gate looks; no file, no
   proof pass happened. Trust-touching work additionally gets the `nuclear-break` attacks executed
   before the gate. Evidence over assertion — a failed or unrun check means not done; say so with
   output.
7. **Independent superreview.** Never self-approve — which forbids granting yourself the verdict,
   not doing the thinking: stage 6 exists because the doer is expected to have questioned and
   validated the change before anyone else reads it. Use the project's review policy — default:
   the `nuclear-review` / proven different-family gate. `nuclear-review` executes one review,
   adjudicates its reviewers, and returns one authoritative `APPROVE | REJECT | NOTE`; this stage
   acts on that result without reinterpreting the raw reviewer votes.

   **a. Prepare and invoke.** Commit the candidate first and record its SHA — the review names an
   exact target and landing requires that SHA, so a review of an uncommitted worktree cannot be
   landed. Produce `$SP/proof-rN.md` via `nuclear-proof`; for trust-touching work, also produce
   `$SP/break-rN.md` via `nuclear-break`. Confirm any required committed plan evidence, then invoke
   `nuclear-review`. The review checks these artifacts but never creates them.

   **b. Act on the superreview result.**
   - `APPROVE`: for a mergeable change, invoke `nuclear-land` to ship and record it.
   - `REJECT`: execute each substantiated blocker by deleting the unnecessary thing, fixing the
     defect, or escalating a genuine owner decision through `nuclear-decide`. Never treat a raw
     reviewer claim that the superreview dismissed as a work order.
   - `NOTE`: record and surface what stood out. It neither authorizes landing nor rejects the
     candidate. If a gate decision is required, resolve the missing criterion, evidence, or owner
     decision before requesting another review.

   When confirmed blockers fan wide, split remediation by **file ownership** — one lane owns a file,
   and a finding spanning two files belongs to exactly one lane named in both briefs. Concurrent
   lanes get a worktree each; one checkout shared by lanes that each rebuild and run the suite
   collides on the index and on test output, and the result is neither lane's. Lanes never
   self-approve. After a material change, rerun verification and `nuclear-proof`, then request a new
   superreview of the new candidate. Never re-dispatch an unchanged candidate or loop to manufacture
   reviewer unanimity. **The loop has a stopping rule**: when a fix pass introduces new
   substantiated blockers for the second consecutive round, the loop is diverging, not converging —
   stop dispatching and take the convergence failure to the owner via `nuclear-decide` instead of
   buying the next round.

## Rules

- **A turn ends for five reasons and no others**: a decision genuinely the owner's, where no
  defensible default exists; an owner instruction to stop, retarget, or narrow scope; an external
  block — spend limit, missing credential, refused authorization; the work complete and recorded; or
  a handoff whose next step is dispatched or scheduled and named, a running dispatch counting only
  with a named waiter, deadline, or resume. Anything else: keep going. "Say the word and I'll…" is a
  bug, not politeness — handing an already-made plan back for a "go" is how an autonomous run
  becomes a manual one.
- **An obstacle is a stage, not an exit.** An unreadable path, a missing tool, an assumption that
  did not hold: route around it and record the route. A refused authorization is the exception —
  that is an answer, and no alternative route may shed the authorization the first one needed.
- **Stage 1's design is a claim like any other.** When execution disproves it, re-run
  `nuclear-frame` naming the contradiction instead of improvising against it; it returns here and
  that stage resumes. An outcome the evidence no longer supports is worth challenging in writing —
  a recorded re-frame, or an entry in the owner's registry. Argue the goal; never swap it.
- **Mid-flight input is an extra command, not a new job.** An instruction arriving while work runs
  joins the queue; it neither cancels what is in flight nor becomes the whole task. Finish the
  running step, apply the addition, report both. **Input that narrows, redirects, or withdraws
  authority is the exception and takes effect immediately** — "not production", "don't merge",
  "stop" — whether or not it is phrased as a command, because the running step is exactly what it
  is about, and a side effect landed while the instruction queued cannot be taken back.
- **Close every turn against the ask.** Before reporting, reconcile item by item: what was
  requested, what was delivered, what was not. **An unreconciled turn is an unverified claim** —
  naming a gap costs a sentence, and leaving one unnamed is how "done" becomes false. The
  close-out also names the open owner-decision count when it is non-zero — a queue nobody
  surfaces is how decisions rot.
- Ambiguous scope → cut it; don't add complexity for hypothetical edge cases.
- **A finding is not a work order.** Under review pressure the fastest way to look responsive is to
  add code, so every fix pass starts with "would deleting this end the finding?" and every unit asks
  what outcome dies if the code is not written. The most reliable code is the code never written;
  that is the spirit, not a tiebreaker for close calls.
- **Judge the shape, not the diffstat** — `nuclear-proof`'s §6 test: concepts a reader holds, one
  path traceable without jumping, cause near effect. Fewer lines is a smell, never the goal.
- Record deferrals and owner decisions in the project's registry (never silently drop).
