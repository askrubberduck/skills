---
name: redteam-review
description: Use when a PR, diff, packet, or trust-touching change hits its review gate, or the user says "redteam", "decorrelated review", or "codex+agy review". Also when a change was authored by a Claude-family agent and needs an independent judge.
---

# Decorrelated Red-Team Review

The doer is never the final judge. The gate is a **different model family** — never a same-family
second pass. If no decorrelated family is available, the change waits (fail closed).

For packet-sized or trust-touching work, run askrubberduck:plan-redteam-coauthor BEFORE building —
gates converge in far fewer rounds when the red team co-authored the plan.

## Dispatch

1. Resolve target into review material: `gh pr diff <N>` / packet draft / `git diff <ref>`.
   Review the **committed object** (`git show <sha>:path`) or the correct worktree — never a stale
   main checkout or dirty tree; both families produce false rejects from wrong snapshots.
2. Write one prompt to the session scratchpad: the diff/design, acceptance criteria, and
   "verdict line required: APPROVE | REJECT | APPROVE-W-CONDITIONS, with findings list".
   Reviewer default: refute, not bless.
3. Run from a **neutral cwd** (scratchpad, never the repo — codex in-repo derails into a security
   scan), stdin closed, `run_in_background: true` (runs take 10–45 min). Absolute paths everywhere.
   The two CLIs take the prompt **differently**:
   ```bash
   SP=<scratchpad>/<topic>-review
   codex exec --skip-git-repo-check "$(cat $SP/prompt.md)" </dev/null > $SP/codex-rN.out 2>&1
   agy --model "Gemini 3.1 Pro (High)" --add-dir "$SP" --print-timeout 45m \
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

4. Parse both verdicts. Per finding: **fix**, **reject with recorded reason**, or **escalate** to the
   owner (queue in the repo's obligations registry if it has one).
   - On deletion-heavy diffs, check the diff prefix char + post-change file before accepting a
     "fact destroyed" finding — context lines and moved facts are common false BLOCKERs.
   - Family disagreement about framework internals → settle by reading the dependency source, not by vote.
   - Carry settled refutations into the next round's prompt so rounds converge.
5. Fix pass → re-dispatch both. Loop until **both families APPROVE in the same round**.
6. One CLI down: the remaining decorrelated family alone meets the bar — record the coverage gap.
   Never substitute a same-family reviewer.

## Optional lens: product fit

On request ("critique product match and fit", "strategic scope review") run ONE extra round after
correctness APPROVE, lens shifted: does the change fit the product's vision and scope, is anything
shipped that should be cut, is the boundary drawn where users need it. Same dispatch mechanics, same
verdict line. Findings weigh functionality/extendability/security — never build effort.

## Record

7. Fold verdicts + adjudications + trajectory (`REJECT/REJECT → APPROVE/APPROVE r2`) into the work
   item's review log. **Never commit raw CLI stdout** — extract verdict + findings, keep outputs in
   the scratchpad (a committed 8.7MB stdout blob once forced a git-history rewrite).
