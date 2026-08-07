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

1. Resolve target into review material: `gh pr diff <N>` / packet draft / `git diff <ref>`.
   Review the **committed object** (`git show <sha>:path`) or the correct worktree — never a stale
   main checkout or dirty tree; both families produce false rejects from wrong snapshots.
2. Record the doer's self-reported model family, then select reviewers relative to it. At least one
   required reviewer must self-report a different model family. Executable names are not proof:
   `agy` can host Gemini, Claude, or other models, and a nested `codex` session remains same-family
   when the doer is OpenAI/GPT. Unknown identity never counts as decorrelated.
3. **Before round 1, not only before re-dispatch**: invoke `nuclear-proof` on the diff and write
   `$SP/proof-r1.md`; on packet-sized **or trust-touching** work — the same scope that required
   planning above — confirm the committed plan carries its `nuclear-plan` co-authorship line. **No receipt, no dispatch — at every round.** A first round is the round most
   likely to burn 45 minutes on defects the doer could have found in five.
4. Write one prompt to the session scratchpad: the diff/design, acceptance criteria, and
   "verdict line required: APPROVE | REJECT | APPROVE-W-CONDITIONS, with findings list".
   Reviewer default: refute, not bless.
5. Run from a **neutral cwd** (scratchpad, never the repo — reviewers can derail when launched in
   the target checkout), stdin closed, in the background (runs take 10–45 min). Absolute paths
   everywhere. Choose only reviewers whose model identity you can verify. Example CLI forms:
   ```bash
   SP=<scratchpad>/<topic>-review
   # Count this as decorrelated only when the doer is not from the OpenAI/GPT family.
   codex exec --skip-git-repo-check "$(cat $SP/prompt.md)" </dev/null > $SP/codex-rN.out 2>&1
   # Pin an available model from a family different from the doer and verify the self-report.
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

6. Parse every verdict. Per finding: **fix**, **reject with recorded reason**, or **escalate** to the
   owner (queue in the repo's obligations registry if it has one; present queued decisions via
   `nuclear-decide`).
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

On request ("critique product match and fit", "strategic scope review") run ONE extra round after
correctness APPROVE, lens shifted: does the change fit the product's vision and scope, is anything
shipped that should be cut, is the boundary drawn where users need it. Same dispatch mechanics, same
verdict line. Findings weigh functionality/extendability/security — never build effort.

## Record

9. Fold verdicts + adjudications + trajectory (`REJECT/REJECT → APPROVE/APPROVE r2`) into the work
   item's review log. **Never commit raw CLI stdout** — extract verdict + findings, keep outputs in
   the scratchpad (a committed 8.7MB stdout blob once forced a git-history rewrite).
10. Trust-touching changes ship `nuclear-break`'s `break-rN.md` with the review material; without
   that receipt the attacks are unproven and the gate does not close. On final APPROVE of a
   mergeable change: `nuclear-land` ships and records it.
