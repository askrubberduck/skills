---
name: duck-run
description: Plan, implement, test, and independently review a high-risk change; trust is not part of the pipeline. Use when the user requests end-to-end delivery with adversarial plan critique, says "duck it" or "plan, critique, red team, execute on green", asks for a duck run or duck simplification, says "wear ponytail + duck soul", or invokes duck-run with a task.
---

# Duck Run

The bundled directive stack the user otherwise types as a preamble. Argument: the task.

## Stages

1. **Ground.** Run `duck-frame`: it reads the project's quality bar, traces the real flow end to
   end, and settles the shape before anything is planned or written. Laziness shortens the
   solution, never the reading. Its `READY` artifact comes back here; this stage decides what
   follows, and a `CUT` verdict ends the run.
2. **Plan.** Detailed decomposition: units of work, gates per unit, acceptance evidence.
   Steel-man at least one alternative decomposition before committing; first idea is a candidate, not a decision.
   Packet-sized or trust-touching: co-author the plan via `duck-plan` instead of
   drafting solo. In doubt about the size, default up — the solo path is bought with one committed
   line, `solo-drafted because: …`; a routing choice without a receipt is the doer grading its own
   rigor. **Do not enter stage 4 until the committed plan carries its co-authorship
   line** — an uncoauthored plan is the rejections arriving later instead of now.
3. **Critique (adversarial, pre-code) — for solo-drafted plans only.** When `duck-plan` ran in
   stage 2, its multi-round concurrence loop already **is** this stage; a second gate on a
   co-authored plan is redundancy, not rigor. Otherwise: red-team the plan — wrong decomposition,
   missing edge cases, simpler design that deletes a concept. Default the critic toward refute, use
   the strongest available tier, fold findings, loop until the plan survives.
4. **Execute on green.** Use the host's native staged or multi-agent orchestration when available;
   otherwise execute the settled stages sequentially. Route stages per `duck-diet`'s stage-routing
   rule — the full cheap-routing precondition lives there; stage 6 additionally re-checks its output
   (a record is checked by reading it back); any unmet precondition runs the stage on the
   inherited model.
   TDD for code units: failing test first, minimal pass, then simplify.
   Draft commits already meet `duck-dry`'s prose bar — draft slop is not free: it leaks
   through cherry-picks and is the raw material the squash message gets built from.
5. **Ponytail lens throughout.** Delete before add; stdlib/existing helper before new code; one
   home per fact; smallest
   diff after full understanding. Simplify touched code before building on it; clear superseded paths
   as the last step of each unit. No migrations, no back-compat shims unless the repo demands them.
   **Write for a senior reader.** Code explains itself; comments supplement it. Run
   `duck-dry` over each unit's diff before stage 6 — it settles what a comment must carry and
   where the prose that does not belong in code goes instead.
6. **Verify.** Run the project's gates (tests/build/vet or doc gates) — a gate that takes minutes
   runs in the background, so the turn keeps working while it does; a blocked loop is the cost, and
   an unread result is the trap — then invoke `duck-proof`
   on your own diff — it leaves `proof-<unit>.md`, or `$SP/proof-r1.md` when stage 7's review is
   next (`$SP`: `duck-review`'s dispatch scratchpad), which is where the gate looks; no file, no
   proof pass happened. Trust-touching work additionally gets the `duck-break` attacks executed
   before the gate. Evidence over assertion — a failed or unrun check means not done; say so with
   output.
7. **Independent superreview.** Never self-approve — which forbids granting yourself the verdict,
   not doing the thinking: stage 6 exists because the doer is expected to have questioned and
   validated the change before anyone else reads it. Use the project's review policy — default:
   the `duck-review` / proven different-family gate. `duck-review` executes one review,
   adjudicates its reviewers, and returns one authoritative `APPROVE | REJECT | NOTE`; this stage
   acts on that result without reinterpreting the raw reviewer votes.

   **a. Prepare and invoke.** Commit the candidate first and record its SHA — the review names an
   exact target and landing requires that SHA, so a review of an uncommitted worktree cannot be
   landed. Produce `$SP/proof-rN.md` via `duck-proof`; for trust-touching work, also produce
   `$SP/break-rN.md` via `duck-break`. Confirm any required committed plan evidence, then invoke
   `duck-review`. The review checks these artifacts but never creates them.

   **b. Act on the superreview result.**
   - `APPROVE`: for a mergeable change, invoke `duck-land` to ship and record it.
   - `REJECT`: execute each substantiated blocker by deleting the unnecessary thing, fixing the
     defect, or escalating a genuine owner decision through `duck-decide`. Never treat a raw
     reviewer claim that the superreview dismissed as a work order.
   - `NOTE`: record and surface what stood out. It neither authorizes landing nor rejects the
     candidate. If a gate decision is required, resolve the missing criterion, evidence, or owner
     decision before requesting another review.

   When confirmed blockers fan wide, split remediation by **file ownership** — one lane owns a file,
   and a finding spanning two files belongs to exactly one lane named in both briefs. Concurrent
   lanes get a worktree each; one checkout shared by lanes that each rebuild and run the suite
   collides on the index and on test output, and the result is neither lane's. Lanes never
   self-approve. After a material change, rerun verification and `duck-proof`, then request a new
   superreview of the new candidate. Never re-dispatch an unchanged candidate or loop to manufacture
   reviewer unanimity. **The loop has a circuit breaker**: when a fix pass introduces new
   substantiated blockers for the second consecutive round, the loop is diverging, not
   converging. Stop dispatching reviews and judge the loop's shape before spending anything
   else. The diagnosis is a judgment, not a routing table — recorded in one committed line
   (`loop-diagnosis: <shape> → <exit>, because …`) — and it picks the exit from the whole
   toolbox:
   - Blockers contradict the settled design: re-run `duck-frame` naming the contradiction —
     the same rule this run already applies to any disproved stage-1 claim.
   - Blockers cluster on unit seams or the decomposition itself: replan via `duck-plan`.
   - Blockers attack remediation-born code under settled criteria — the review is red-teaming
     its own byproducts and iteration cannot terminate it: rebuild the contested unit via
     `duck-race`, where executed evidence adjudicates and review becomes selection instead of
     iteration, or lock each finding class in as a failing test via `duck-pingpong`, so a
     regression is executable instead of prose.
   - Blockers dispute scope or design intent: `duck-decide`; a written owner freeze is a valid
     exit.
   Buying round N+1 bare is not on the list, and the breaker is not self-graded: `duck-review`
   refuses a third round's dispatch that carries no recorded diagnosis.

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
  `duck-frame` naming the contradiction instead of improvising against it; it returns here and
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
- **Judge the shape, not the diffstat** — `duck-proof`'s §6 test: concepts a reader holds, one
  path traceable without jumping, cause near effect. Fewer lines is a smell, never the goal.
- Record deferrals and owner decisions in the project's registry (never silently drop).
