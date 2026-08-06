---
name: nuclear-review
description: Use when a PR, diff, packet, or trust-touching change hits its review gate, or the user says "redteam", "decorrelated review", or "codex+agy review". Also when work from any model family needs an independent judge, or when one gate's findings span several files and fix work needs parallel lanes.
---

# Decorrelated Red-Team Review

The doer is never the final judge. The gate is a **different model family** — never a same-family
second pass. If no decorrelated family is available, the change waits (fail closed).

Use `$askrubberduck:<name>` as the canonical bundled-skill reference. Before its step starts, resolve
it with the active host's invocation syntax while retaining the `askrubberduck:` namespace. Use
`$<name>` or `<name>` only for a deliberate standalone install. If no installed form resolves, stop
and name the missing skill; never retry under another name after that step's side effects start.

For packet-sized or trust-touching work, run `$askrubberduck:nuclear-plan` BEFORE building —
gates converge in far fewer rounds when the red team co-authored the plan.

## Dispatch

1. Resolve target into review material: `gh pr diff <N>` / packet draft / `git diff <ref>`.
   Review the **committed object** (`git show <sha>:path`) or the correct worktree — never a stale
   main checkout or dirty tree; both families produce false rejects from wrong snapshots.
2. Record the doer's self-reported model family, then select reviewers relative to it. At least one
   required reviewer must self-report a different model family. Executable names are not proof:
   `agy` can host Gemini, Claude, or other models, and a nested `codex` session remains same-family
   when the doer is OpenAI/GPT. Unknown identity never counts as decorrelated.
3. Write one prompt to the session scratchpad: the diff/design, acceptance criteria, and
   "verdict line required: APPROVE | REJECT | APPROVE-W-CONDITIONS, with findings list".
   Reviewer default: refute, not bless.
4. Run from a **neutral cwd** (scratchpad, never the repo — reviewers can derail when launched in
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

5. Parse every verdict. Per finding: **fix**, **reject with recorded reason**, or **escalate** to the
   owner (queue in the repo's obligations registry if it has one; present queued decisions via
   `$askrubberduck:nuclear-decide`).
   - On deletion-heavy diffs, check the diff prefix char + post-change file before accepting a
     "fact destroyed" finding — context lines and moved facts are common false BLOCKERs.
   - Family disagreement about framework internals → settle by reading the dependency source, not by vote.
   - Carry settled refutations into the next round's prompt so rounds converge.
6. Fix pass → invoke `$askrubberduck:nuclear-proof` on your own fixes, writing its findings to
   `$SP/proof-rN.md`
   → only then re-dispatch both. **No `proof-rN.md`, no dispatch** — a round sent without it is a
   skipped step, not a fast round. Self-refutation costs minutes and saves whole 30-minute rounds;
   it is doer hygiene and never a substitute for the decorrelated gate. Loop until every required,
   successfully dispatched reviewer **APPROVES in the same round**, subject to the outage rule below.
7. Completion requires approval from at least one reviewer proven to be from a different model
   family than the doer. A same-family pass never substitutes. If the only decorrelated reviewer is
   unavailable or fails, the gate blocks; record an additional reviewer outage only after a proven
   different-family approval exists.

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

8. Fold verdicts + adjudications + trajectory (`REJECT/REJECT → APPROVE/APPROVE r2`) into the work
   item's review log. **Never commit raw CLI stdout** — extract verdict + findings, keep outputs in
   the scratchpad (a committed 8.7MB stdout blob once forced a git-history rewrite).
9. For trust-touching changes, include `$askrubberduck:nuclear-break`'s executed-attack evidence in
   the review material. On final APPROVE of a mergeable change: `$askrubberduck:nuclear-land` ships and
   records it.
