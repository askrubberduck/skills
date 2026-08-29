---
name: duck-run
description: Deliver a high-risk change end to end without trusting any stage of it. Use when the user requests end-to-end delivery with adversarial plan critique, says "duck it" or "plan, critique, red team, execute on green", asks for a duck run or duck simplification, says "wear ponytail + duck soul", or invokes duck-run with a task.
---

# Duck Run

The bundled directive stack the user otherwise types as a preamble. Argument: the task.

## Precondition: isolate

Provision a dedicated worktree for this run — `.worktrees/<task>/` **at the repo root**, never the
shared checkout — then switch to it before proceeding: a run that mutates the shared checkout
collides with parallel runs and breaks campaign isolation. Every worktree this run later spawns
(Superreview's remediation lanes, a `duck-race` racer) is a sibling under that root, never a child
of this one. Step back out to the root checkout before `duck-land` runs, because it deletes this
worktree and cannot delete the directory it is standing in. No `git`, or a host without worktrees?
Say so and take the next isolation the host has — a clone, or a dedicated branch when nothing else
runs against that checkout. Sharing a live checkout with another run is the one option ruled
out. The short path below is the one exemption, and it is bought with a committed line.

**Short path.** Work that moves no seam — no boundary between components, no public surface,
nothing trust-touching — takes `duck-frame`'s short form, skips the worktree, and runs Execute
through Verify in one pass. What it never skips is Superreview: the gate is the last thing to go,
not the first. Bought with one committed line, `short-path because: …`, because the judgment that
work is small is itself a claim to attack.

## Stages
1. **Ground.** Run `duck-frame`: it reads the project's quality bar, traces the real flow end to
   end, and settles the shape before anything is planned or written. Laziness shortens the solution,
   never the reading. **Under a campaign** the campaign's frame binds this one but does not replace
   it: pass it in as a constraint and frame against this packet's own work item, because
   `duck-frame` resolves artifacts beside the work item it is given and would otherwise hand the
   campaign's frame back as this packet's answer. Its `READY` artifact comes back here; this stage
   decides what follows, and a `CUT` verdict ends the run.
2. **Plan.** Detailed decomposition: units of work, gates per unit, acceptance evidence.
   Steel-man at least one alternative decomposition before committing; the first idea is a
   candidate, not a decision.
   Packet-sized or trust-touching: co-author the plan via `duck-plan` instead of
   drafting solo. In doubt about the size, default up — the solo path is bought with one committed
   line, `solo-drafted because: …`; a routing choice without a receipt is the doer grading its own
   rigor. **Do not reach Execute without a settled plan** — either a committed plan carrying a
   `duck-plan` co-authorship line, or a solo-drafted plan that has survived Critique. An unsettled
   plan is the rejections arriving later instead of now. A plan that already carries that line —
   one a campaign committed, say — **is** settled: it does not get re-planned here, and Critique is
   for solo drafts only.
3. **Critique (adversarial, pre-code) — for solo-drafted plans only.** When `duck-plan` ran in
   Plan, its multi-round concurrence loop already **is** this stage; a second gate on a
   co-authored plan is redundancy, not rigor. Otherwise: red-team the plan — wrong decomposition,
   missing edge cases, simpler design that deletes a concept. Default the critic toward refute, use
   the strongest available tier, fold findings, loop until the plan survives.
4. **Execute on green.** Use the host's native staged or multi-agent orchestration when available;
   otherwise execute the settled stages sequentially. Route stages per `duck-diet`'s stage-routing
   rule — the full cheap-routing precondition lives there; Verify additionally re-checks its
   output (a record is checked by reading it back); any unmet precondition runs the stage on the
   inherited model.
   TDD for code units: failing test first, minimal pass, then simplify.
   Draft commits already meet `duck-dry`'s prose bar — draft slop is not free: it leaks
   through cherry-picks and is the raw material the squash message gets built from.
5. **Ponytail lens throughout.** Delete before add; stdlib/existing helper before new code; one
   home per fact; smallest diff after full understanding. Simplify touched code before building on
   it; clear superseded paths as the last step of each unit. No migrations, no back-compat shims
   unless the repo demands them.
6. **Dry it — write for a senior reader.** Code explains itself; comments supplement it. Run
   `duck-dry` over each unit's diff before Verify: it settles what a comment must carry, and where
   the prose that does not belong in code goes instead.
7. **Verify.** Run the project's gates (tests/build/vet or doc gates) — a gate that takes minutes
   runs in the background, so the turn keeps working while it does; a blocked loop is the cost, and
   an unread result is the trap — then invoke `duck-proof` on your own diff. It leaves
   `proof-<unit>.md`, or `proof-r1.md` when Superreview is next, in the project's durable records
   home — never the scratchpad, which is where the gate looks; no file, no proof pass happened.
   Trust-touching work additionally gets the `duck-break` attacks executed before the gate. Evidence
   over assertion — a failed or unrun check means not done; say so with output.
8. **Independent superreview.** Never self-approve — which forbids granting yourself the verdict,
   not doing the thinking: Verify exists because the doer is expected to have questioned and
   validated the change before anyone else reads it. Use the project's review policy — default:
   the `duck-review` / proven different-family gate. `duck-review` executes one review,
   adjudicates its reviewers, and returns one authoritative `APPROVE | REJECT | NOTE`; this stage
   acts on that result without reinterpreting the raw reviewer votes.

   **a. Prepare and invoke.** Commit the candidate first and record its SHA — the review names an
   exact target and landing requires that SHA, so a review of an uncommitted worktree cannot be
   landed. Produce `proof-rN.md` via `duck-proof`; for trust-touching work, also produce
   `break-rN.md` via `duck-break`. Both go to the durable records home, never the scratchpad and
   never a commit on the candidate branch — a receipt committed there advances the head past the
   SHA the review is about to authorize. **Run `duck-proof` before recording the candidate SHA**,
   not after: its fifth section fixes what it finds, and a proof pass that edits the candidate
   leaves the authorization pointing at code nobody reviewed. Confirm any required committed plan
   evidence, then invoke `duck-review`. The review checks these artifacts but never creates them.

   **b. Act on the superreview result.**
   - `APPROVE`: for a mergeable change, invoke `duck-land` to ship and record it.
   - `REJECT`: name each substantiated blocker's cause before touching it — `duck-why` when the
     blocker reports a symptom and the defect behind it is not already obvious from the diff. Then
     execute by deleting the unnecessary thing, fixing the defect, or escalating a genuine owner
     decision through `duck-decide`. Never treat a raw reviewer claim that the superreview
     dismissed as a work order.
   - `NOTE`: record and surface what stood out. It neither authorizes landing nor rejects the
     candidate. If a gate decision is required, resolve the missing criterion, evidence, or owner
     decision before requesting another review.

   When confirmed blockers fan wide, split remediation by **file ownership** — one lane owns a
   file, and a finding spanning two files belongs to exactly one lane named in both briefs.
   Concurrent lanes get a worktree each; one checkout shared by lanes that each rebuild and run the
   suite collides on the index and on test output, and the result is neither lane's. Lanes never
   self-approve. **Lanes converge before the next review, never after it**: each rebases onto the
   candidate branch in turn, the file-ownership split guaranteeing no lane rewrites another's work,
   and the merged result becomes the new candidate. It gets one verification run of its own —
   per-lane green does not compose, exactly as it does not for `duck-race`'s merged candidate. A
   lane whose worktree still exists is a lane that has not landed. After a material change, rerun
   verification and `duck-proof`, then request a new superreview of the new candidate.
   Never re-dispatch an unchanged candidate or loop to
   manufacture reviewer unanimity. **The loop has a circuit breaker**: when a fix pass introduces
   new substantiated blockers for the second consecutive round, the loop is diverging, not
   converging. Stop dispatching reviews and judge the loop's shape before spending anything else.
   The diagnosis is a judgment, not a routing table — recorded in one committed line
   (`loop-diagnosis: <shape> → <exit>, because …`) — and it picks the exit from the whole toolbox:
   - Blockers contradict the settled design: re-run `duck-frame` naming the contradiction —
     the same rule this run already applies to any disproved stage-1 claim.
   - Blockers cluster on unit seams or the decomposition itself: replan via `duck-plan`.
   - Blockers attack remediation-born code under settled criteria — the review is red-teaming
     its own byproducts and iteration cannot terminate it: rebuild the contested unit via
     `duck-race`'s race mode, where executed evidence adjudicates and review becomes selection
     instead of iteration, or lock each finding class in as a failing test via its rally mode, so
     a regression is executable instead of prose.
   - Blockers dispute scope or design intent: `duck-decide`; a written owner freeze is a valid
     exit.
   Buying round N+1 bare is not on the list, and the breaker is not self-graded: `duck-review`
   refuses a third round's dispatch that carries no recorded diagnosis.

## Rules

- **A turn ends for five reasons and no others**: a decision genuinely the owner's; an owner
  instruction to stop or narrow; an external block (spend limit, refused authorization); the work
  complete; or a scheduled handoff. Anything else: keep going.
- **An obstacle is a stage, not an exit.** An unreadable path or a failed assumption means route
  around it and record the route. A refused authorization is the exception — that is a hard stop,
  and no alternative route may shed the authorization the first one needed.
- **Ground's design is a claim like any other.** When execution disproves it, re-run `duck-frame`
  naming the contradiction instead of improvising against it. Argue the goal; never swap it.
- **Mid-flight input is an extra command, not a new job.** Finish the running step, apply the
  addition, report both. **Exceptions that take effect immediately:** input that narrows, redirects,
  or withdraws authority ("stop", "don't merge").
- **Close every turn against the ask.** Reconcile item by item: what was requested, what was
  delivered, what was not. Name the open owner-decision count when it is non-zero.

## Common mistakes

- **"Say the word and I'll start"** — handing a plan back for a "go" is a bug, not politeness. The
  go-sign was the initial directive.
- **Treating a review finding as a work order** — under pressure the fastest way to look responsive
  is to add code. Every fix pass starts with "would deleting this end the finding?".
- **Judging by diffstat instead of shape** — shrinking a diff while tangling the flow is worse than
  growing it to untangle it.
- **Silently dropping deferrals** — unresolved decisions go into the project's registry, never into
  the void.
- **Adding complexity for ambiguous scope** — if the scope is ambiguous, cut the edge case; do not
  over-build for a hypothetical.
