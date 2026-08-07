---
name: nuclear-review
description: Find release-blocking risks through an independent cross-model change review. Use when a PR or diff is ready to review, a security-, privacy-, or data-sensitive change reaches its release gate, the user asks for a red-team or independent second opinion, or findings span several files and need separate fixes.
---

# Decorrelated Red-Team Review

The doer is never the final judge. The gate is a **different model family** — never a same-family
second pass. If no decorrelated family is available, the change waits (fail closed).

For packet-sized or trust-touching work, run `nuclear-plan` BEFORE building —
gates converge in far fewer rounds when the red team co-authored the plan.

## Dispatch

`$SP` is this dispatch's scratchpad: an absolute path under the host's sanctioned scratchpad root
(e.g. `<scratchpad-root>/<topic>-review`), created before step 1; every artifact below lands there.
**Trust-touching** — one spelling, collection-wide — means security-, privacy-, or data-sensitive
work, or a change to any gate's semantics.

1. Resolve target into review material: `gh pr diff <N>` / packet draft / `git diff <ref>`.
   Review the **committed object** (`git show <sha>:path`) or the correct worktree — never a stale
   main checkout or dirty tree; both families produce false rejects from wrong snapshots.
2. Record the doer's self-reported model family, then select reviewers relative to it. At least one
   required reviewer must self-report a different model family, and each required reviewer runs the
   **strongest tier of its family the host lists and you can pin** — decorrelation buys
   independence, tier buys rigor; two weak families still approve junk. Record the pinned model id
   and the listing that ranked it (the command and its output) beside each verdict — a pinned id
   alone proves what ran, not that nothing stronger was listed. A dispatch that had to fall back
   below that tier is recorded as downgraded, with the failed stronger dispatch as its evidence —
   a downgraded verdict is a lesser reviewer, never an outage (step 8's outage still means no
   verdict at all), and it never closes the gate: the gate waits for a strongest-tier verdict, or
   the owner's recorded acceptance of the downgrade. Executable
   names are not proof:
   `agy` can host Gemini, Claude, or other models, and a nested `codex` session remains same-family
   when the doer is OpenAI/GPT. Unknown identity never counts as decorrelated.
3. **Before round 1, not only before re-dispatch**: invoke `nuclear-proof` on the diff and write
   `$SP/proof-r1.md`; on packet-sized **or trust-touching** work — the same scope that required
   planning above — confirm the committed plan carries its `nuclear-plan` co-authorship line. **No receipt, no dispatch — at every round.** A first round is the round most
   likely to burn 45 minutes on defects the doer could have found in five.
4. Write one prompt to the session scratchpad: the diff/design, acceptance criteria, the round's
   receipt from step 3 — attached as the doer's claim to attack, never a coverage map, and a
   receipt whose sections lack artifacts or skip reasons is itself a finding that blocks APPROVE —
   the break receipt (step 10) when the work is trust-touching, and
   "verdict line required: APPROVE | REJECT | APPROVE-W-CONDITIONS, with findings list".
   Reviewer default: refute, not bless.
5. Run from a **neutral cwd** (scratchpad, never the repo — reviewers can derail when launched in
   the target checkout), stdin closed, in the background (runs take 10–45 min). Absolute paths
   everywhere. Choose only reviewers whose model identity you can verify. Example CLI forms:
   ```bash
   SP=<scratchpad>/<topic>-review
   # Decorrelated only when the doer is not OpenAI/GPT; pin the strongest model codex lists.
   codex exec -m "<strongest-listed-model>" --skip-git-repo-check "$(cat $SP/prompt.md)" </dev/null > $SP/codex-rN.out 2>&1
   # Pin the strongest listed model from a family different from the doer; verify the self-report.
   agy --model "<verified-non-doer-model>" --add-dir "$SP" --print-timeout 45m \
       -p "Read $SP/header.md (task) and $SP/change.diff (full diff). ..." \
       </dev/null > $SP/agy-rN.out 2>&1
   ```
   **agy traps — each yields a plausible EMPTY review at exit 0:**
   - agy is a model HOST: unpinned it may serve a **Claude** model, silently breaking decorrelation.
     Always pin `--model`; it self-reports, so decorrelation is verifiable.
   - `--print "<text>"` silently drops the prompt — use `-p`.
   - Large inlined diffs die on timeout — pass by file, absolute paths (agy ignores cwd).
   Sanity-check a new invocation form with `-p "What is 2+2?"`. Zero-byte, greeting-only, or
   timed-out output is a **failed dispatch, never an implicit APPROVE**.

## Adjudicate

6. Parse every verdict. Per finding there are **four** dispositions, and fixing is not the default:
   **delete the thing the finding is about**, **fix**, **reject with recorded reason**, or
   **escalate** to the owner (queue in the repo's obligations registry if it has one; present queued
   decisions via `nuclear-decide`).
   - **Ask what the code is for before you patch it.** A finding says "this is broken"; it does not
     say the thing should exist. The most reliable code is the code never written, so the first
     question on every finding is whether deleting the feature, flag, branch, or check ends the
     finding outright. A reviewer optimises what you put in front of it — it will not tell you the
     whole mechanism was unnecessary.
   - **The growth ratchet.** If one rule draws findings round after round, the rule is wrong, not
     under-patched. Stop fixing and ask what it is replacing that already works — a stdlib call, a
     built-in flag, a human decision. A branch-deletion rule here survived six rounds of patching
     before anyone checked what `git branch --merged` and `-d` already decided — and then a seventh
     pass to find that the built-in guarantees something narrower than it looks.
   - **Count concepts, not lines.** Each round, say what a reader must now hold that they didn't
     before — a new branch, a new exception, a new place the same fact lives. That number rising every
     round is the loop; a diffstat is not. Shrinking a diff while tangling the flow is a loss, and it
     is the loss a line metric scores as a win.
   - On deletion-heavy diffs, check the diff prefix char + post-change file before accepting a
     "fact destroyed" finding — context lines and moved facts are common false BLOCKERs.
   - Family disagreement about framework internals → settle by reading the dependency source, not by vote.
   - Carry settled refutations into the next round's prompt so rounds converge.
7. Fix pass → invoke `nuclear-proof` on your own fixes, writing its findings to
   `$SP/proof-rN.md`
   → only then re-dispatch every required reviewer. **No `proof-rN.md`, no dispatch** — a round sent
   without it is a skipped step, not a fast round. Self-refutation costs minutes and saves whole
   30-minute rounds; it is doer hygiene and never a substitute for the decorrelated gate.
8. **The required set is two reviewers from two different model families, at least one of them
   different from the doer's.** Name them before round 1; the gate closes only when every one of
   them APPROVES in the same round. One reviewer is the **outage exception, not the standard**, and
   "outage" means exactly one thing: a dispatch that was attempted and produced **no verdict** —
   zero-byte output, greeting-only, timeout, crash — with that evidence recorded beside the verdict.
   **A REJECT is never an outage.** A reviewer that answered and refused is the gate working; routing
   around it is not an exception, it is the doer overruling its own judge. The remaining approval must
   still be a proven different family. A same-family pass never substitutes, and an unverified model
   identity is not a family.

## Multi-lane fix-pass (when findings fan wide)

When one round's findings span several files/modules and a single fix agent would serialize them,
fan the fix pass across N parallel lanes by **file ownership** — one lane owns a file, no two lanes
edit the same file. The gate stays singular: lanes fix, the coordinator re-dispatches the review.

1. Partition findings by owned file set, not by finding type; a finding touching two lanes' files
   goes to exactly one lane, named in both briefs.
2. Brief each lane with only its findings plus the shared invariants (perimeter/LOC budget, test
   suite, naming). Full finding list to every lane = N× tokens for zero extra coverage.
3. Re-pin the shared budget every round ("LOC 30418, +13 all yours") — drift is additive and
   invisible per lane.
4. Crossed reports ("already fixed" / "still broken" about another lane's file) may be reading
   pre-fix code — settle by reading the current tree, never by lane vote.
5. Poll lanes at round boundaries; an idle ping with no new state gets no reply. Lanes never talk
   to the gate or self-approve; round ends when every lane is landed + green → ONE re-dispatch.

## Optional lens: product fit

On request, one extra round after correctness APPROVE with the lens shifted: does this fit the
product's scope, what shipped that should be cut, is the boundary where users need it. Same
mechanics; weigh functionality/extendability/security, never build effort.

## Record

9. Fold verdicts + adjudications + trajectory (`REJECT/REJECT → APPROVE/APPROVE r2`) into the work
   item's review log. **Never commit raw CLI stdout** — extract verdict + findings, keep outputs in
   the scratchpad (a committed 8.7MB stdout blob once forced a git-history rewrite).
10. Trust-touching changes ship `nuclear-break`'s `break-rN.md` with the review material; without
   that receipt the attacks are unproven and the gate does not close. On final APPROVE of a
   mergeable change: `nuclear-land` ships and records it.
