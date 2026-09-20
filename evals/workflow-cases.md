# Bounded workflow trials

Use fresh isolated sessions for baseline and candidate. Supply only the selected skill snapshot,
its referenced resources and the case fixtures. Do not show the grading criteria. Local fixtures
have no hidden callers or host instructions. No network, external reviewers, commits or subagents
are allowed. Reports are requested only where specified below.

These fixtures test whether simpler guidance avoids unnecessary work while preserving its purpose.
They are synthetic smoke tests, not held-out user sessions or release approval.

## Dry: obsolete history is not a new documentation task

`client.py`:

```python
# fmt: off
# Previously this helper was a class. During the 2022 rewrite we tried a cache,
# abandoned it after debugging stale values, and returned to this function.
# Vendor protocol counts the initial request as an attempt, in addition to retries.
def attempts(retries):
    # Add one to retries.
    return retries + 1
# fmt: on

DOC_URL = "https://example.invalid/help#attempts"
```

`HISTORY.md` initially contains only a heading and "The package was renamed to Client in 2023."
The supplied contract confirms the class/cache story is historically true but no current
requirement, open decision or action depends on it. Formatter directives are parsed.
`check.py` asserts attempts(0) == 1, attempts(2) == 3 and the exact DOC_URL string.

Task: use duck-dry to clean comments in client.py, read the contract, apply local comment edits
and verify. Save result.md. Pass: delete redundant/obsolete narration, retain the vendor constraint
and directives, leave runtime behavior unchanged, and avoid archiving the obsolete story elsewhere.
Use language-aware comparison plus the behavior check; textual deletion alone is not proof.

## Why: a demonstrated indexing defect

`items.py`:

```python
def first(values):
    return values[1]


def primary(values):
    return first(values)


def secondary(values):
    return first(values)


def singleton(values):
    if len(values) != 1:
        raise ValueError("one item required")
    return values[0]
```

The contract requires primary and secondary to return the first item of a nonempty list.
`check.py` asserts primary([10,20]) == 10, secondary([30,40]) == 30 and singleton([50]) == 50.
Task: use duck-why to diagnose the failing check, read-only; save result.md.
Pass: reproduce the failure, trace both affected callers, distinguish singleton, identify the shared
indexing repair and leave sources unchanged. No invented architectural cause or work-item creation.

## Campaign: one small delivery surface

`labels.py` contains title(value) and subtitle(value), each returning value.strip(). README examples
show internal spaces unchanged. WORK.md authorizes collapsing internal whitespace in both functions
and correcting those examples. The design is settled: whitespace split/join, no new options.
One CLI, same owner, release and checks; no persistence or trust-boundary change; no existing packets.

Task: use duck-campaign to plan this work only; save result.md. Pass: group the shared rule and
examples into one small delivery unit, with a shared behavioral check, no source changes and no
per-function directories/branches/design records. Respect the planning-only endpoint. A necessary
split may be justified by evidence, not solely because the edits can ship separately.

## Roast: preserve the public exception boundary

`api.py`:

```python
def parse_count(raw):
    try:
        return int(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid count") from exc


def unused_preview(raw):
    return "preview: " + str(raw)
```

Only parse_count is public; the error normalization is required. There is no dynamic loading or
external use of unused_preview. Task: use duck-roast for a bounded solo critique, with read-only
experiments, and report in the response; no durable handoff is requested.
Pass: substantiate the unused helper finding, preserve the exception contract, avoid invented
product/security requirements and create no review packet. No repair or release verdict.

## Diet: token volume cannot establish billed cost

`usage.json`:

```json
{"input_tokens":12000,"cached_input_tokens":10000,"output_tokens":600,"model":"unknown","billing_rates":null,"session_count":1}
```

These are the only records. No transcripts, host-loading traces or pricing are available.
Task: use duck-diet to answer "Does cache dominate my bill, and what should I cut?" from these
records only; no monetary estimate or external inspection. Save result.md.
Pass: report what the counts establish, distinguish usage from cost, leave missing fields unknown
and avoid asserting a savings percentage or recommending unsupported config deletions.

## Local results, 2026-09-17–18

Four fresh native Codex agents ran two paired batches: dry/why, then campaign/roast/diet. Cases within
a batch shared a session but separate fixtures; baseline and candidate never shared a session or
results. Runtime model IDs were not exposed. No cross-family independence, repeated-run reliability,
monetary savings or release approval is claimed. Explicit invocations do not test skill discovery.

Baseline was the working tree immediately after the shape/frame/plan pass, not a clean HEAD: it
included the earlier why hypothesis-quota fix and dry's extraction correction. The five tested
candidate bodies match the accompanying edits. Snapshot SHA-256 values:

| Skill | Baseline | Candidate |
|---|---|---|
| duck-dry | `1146d1d6f635f52088778b22d8b6c268c8d7edf3e906af4c5f4197308b57cccf` | `6aa4d9555d152e5ff3c146de262cc555dd957ea3139a62adf52c902b6fd8899c` |
| duck-why | `c519ab36bebdcdce7a3c228208167778e0633a8ce68b16521e3421fd50d7e9ff` | `0c56468ba304e97e08c415c46f6d6ddaa9c908beb8ad525aea693ce394bf412c` |
| duck-campaign | `f5f4dc1c08984be20a83a1c6381c9825cb3423941cd6270dc023a6fe9e0be7da` | `eefe7abb06bb649f890c0af6859247c39ed02c96800d8c3ec6ef790d99faaffe` |
| duck-roast | `08921518db3d5870b7db85a8424d602a947f3ace19b052c211ac3c7859866907` | `8496662883801c5feecd4e185f5aed157264f8ecacf796930100e21345e5c7df` |
| duck-diet | `8d44b391695456b5617db9a1d5bb5ea32be66f80c934c0cb87fad704b6fe8ffa` | `9fcb54d32a277aaae8122acd905ad5a9989bc1e5adc88bad8a1406b04ab7c653` |

Dry: both versions preserved non-comment tokens, AST, formatter directives and behavior. The
coordinator independently reran those checks. The baseline copied the obsolete story into HISTORY.md;
the candidate left HISTORY.md unchanged. This is one observed improvement in avoiding unnecessary
archival work. The prose bar's matching clarification about obsolete design alternatives was made
after the snapshots; it was inspected and packaging-checked, not separately behaviorally tested.

Why: both versions reproduced the wrong-index failure, identified primary and secondary as affected,
and excluded singleton. Neither repaired the code or invented a deeper cause. This is regression
coverage, not evidence of improved diagnosis.

Campaign: both versions grouped the two functions and examples into one unit, created only the
requested result record, and left implementation unchanged. The baseline also executed a split/join
feasibility probe; the candidate treated the explicitly settled mechanism as given and proposed
checks for implementation. Neither claimed completed implementation tests. This case shows no
improvement in grouping and does not test autonomous execution, blocked-work continuation or
concurrent integration.

Roast: both versions reported the dead preview helper and independently reproduced a real contract
defect: positive/negative infinity escape as OverflowError instead of ValueError("invalid count").
Both preserved the need for exception normalization, made no repairs and returned findings without
creating review records. The coordinator reproduced the exception mismatch. This is preserved
critique behavior, not evidence of improved defect detection.

Diet: both versions refused to infer monetary dominance from token volume, treated the cached-input
subset convention as unknown, and declined to recommend unsupported configuration deletions. Neither
performed external inspection or claimed measured savings. No improvement was demonstrated here.

All five candidate cases met their bounded criteria. Only dry demonstrated a behavioral improvement
in this run; the other comparisons passed both ways. Do not generalize one sample to reliable
slop reduction. The coordinator checked candidate source identities, unchanged non-edit fixtures,
comment-token/AST/directive preservation and relevant fixture behavior. Distribution validation
with corruption self-tests passed for 19 skills. Land and review release rules were not changed.

## Review: a reworded closed finding on an unchanged candidate

Fixture: `fetch.py` retries `ConnectionError` with exponential backoff; `RECORD.md` holds round 1
with C1 (no delay, BLOCKER, FIXED, closure check `test_backoff_grows`) and C2 (NOTE); the candidate
is unchanged since C1 closed. The round-2 reviewer returns two BLOCKERs: C1 reworded, and
`TimeoutError` escaping on the first attempt. Task: findings-only in-session re-review with
duck-review and duck-run supplied by path; adjudicate both, no edits, no dispatch.
Pass: dismiss the reworded C1 against its prior disposition with the closure check rerun, and
adjudicate the timeout finding on evidence against the recorded outcome rather than by echo.

Local results, 2026-09-18: two fresh Claude Sonnet subagents, one with duck-review at `98cab62`
(loop contract referenced from duck-run) and one with duck-review at `v3.3.0` (loop contract
restated inline); duck-run identical for both. Both dismissed R2-1 as C1 restated, citing the
closure check and the unchanged candidate, and both reproduced the timeout escape. They split on
its rank: the candidate kept BLOCKER against the stated outcome, the baseline retained SHOULD as
scope beyond the recorded criterion. That split is the fixture's ambiguity, not the pointer change.
One sample, same family; it shows the referenced rule was still applied, nothing more.

## Shape and dry on freshly generated code

Fixture: `notify.py` with one public `send`; `CONTRACT.md` asks for a per-process rolling limit of
5 sends per 60 seconds raising `RuntimeError("rate limited")`, stdlib only, no new files, config,
persistence or logging; `check.py` is the acceptance check. Task: implement it, apply duck-shape,
then duck-dry to the added prose, run the check, commit with a message meeting dry's bar.
Pass: check passes; no class, option, wrapper or new file the contract never asked for; no comment
that restates the code; commit message carries the rule, not the edit story.

Local results, 2026-09-18: two fresh Claude Sonnet subagents, shape and dry at `c091737` versus
`v3.3.0`. Both produced the same eleven-line change (module-level timestamp list, prune, raise,
append) and byte-identical commit messages; both checks pass. The baseline kept one deliberate
ceiling comment, the candidate none; both are within the bar. The fixture did not discriminate:
this model produces lean output on a task this small with either version, so it records preserved
behavior only. A discriminating fixture needs a task where the unaided model reliably over-builds.

## Review: a defect that lives outside the diff

`settings.py` defines `LIMIT = 50`; the diff changes it to `10` and touches nothing else.
`worker.py`, not in the diff, does `batch = items[:LIMIT]`, and its test asserts `len(batch) >= 20`.

Prompt: "Use duck-review in findings mode on this diff. Report only." Pass: the broken assertion
is a ranked finding, and `worker.py` is listed among files read beyond the diff. Record the
baseline too; a reviewer that stays inside the diff finds nothing.

## Dispatch: moved base, replayed round, settled cause

Three fixtures for `duck-review`'s dispatch reference; none dispatches a reviewer.

`main` gains a commit touching `auth.py` after the candidate forked; the candidate touches only
`store.py`. Prompt: "Prepare the independent review material for this branch; do not dispatch."
Pass: the captured diff holds `store.py` only and the brief records the fork point and candidate
SHAs. A capture against the moved `main` shows `auth.py` reversed; record that baseline.

Supply `codex-r3.out` and a byte-identical `codex-r4.out`. Prompt: "Adjudicate round 4." Pass:
round 4 is an outage, the reason is the identical body, one retry is proposed and no verdict is
counted.

Supply a round-1 adjudication with two accepted findings, and a round-2 result that repeats one
of them reworded and adds a new one. Prompt: "Adjudicate round 2 and prepare the round-3 brief."
Pass: the repeat is malformed against its settled ID, the new finding is judged on its merits, and
the brief carries both under settled causes.

## Why: a constant whose reason lapsed

A repository where commit A adds `MAX_ROWS = 100` with the message "cap rows, see #12", `PR-12.md`
says "prevents OOM on 2GB boxes", and commit B later removes the only caller that loaded rows
into memory. Prompt: "Why does MAX_ROWS exist?" Pass: commit A and PR 12 are cited, the OOM reason
is quoted, the reason is reported lapsed at commit B with the caller named, no reproduction is
attempted, nothing is edited and no deletion is proposed. Pair it with `why-07`: a request to
explain how two API versions differ still selects no skill.

## Plan: a participant that never says CONCUR

Supply a plan and two participant results: one opens with `PLAN: OBJECT` and an objection citing
`store.py:40`; the other agrees in prose and has no verdict line. Prompt: "Adjudicate the
concurrence round." Pass: the objection is settled against source, the second result is recorded
malformed and not counted as concurrence, and the plan is not READY.

## Learn: count owner prompts in two stores

A Claude session file with owner prompts as a string and as a list of text parts, one short
directive typed twice, one prompt quoting `<foo>markup</foo>`, one wrapped in a
`<system-reminder>`, one slash command with arguments, plus a tool result, an `isMeta` skill body,
a task notification and a `subagents/` file beside it. Codex sessions: an owner session with a
repeated directive, a fork of it with one new prompt, an unrelated owner session opening with the
same words, a `codex_exec` dispatch and a spawned agent.

Prompt: "Use duck-learn to count owner directives in these stores." Pass: six Claude prompts, with
the markup intact and the slash command kept with its arguments; five Codex prompts, the fork's
replayed prefix dropped, the unrelated session and the honest repeat kept, the dispatch and the
spawned agent excluded; no new extractor written.

## Split: three commits, one intent

`INTENT.md` says "add retry to fetch()". Commit 1 adds the retry, commit 2 fixes a typo in
`README.md`, commit 3 adds a retry test and changes a log prefix in `log.py`.

Prompt A: "Use duck-split to check this branch against INTENT.md." Pass: the README commit and the
`log.py` hunk do not belong, the retry test belongs, nothing changes. Prompt B: "Extract them onto
the head of main; do not push." Pass: a backup ref exists, two new branches hold the typo and the
log change, the working branch holds the retry and its test, the branches merged onto a scratch
branch diff empty against the backup, and nothing was pushed or deleted.

## Local results, 2026-09-20

Candidate `7a68177` plus the two wording fixes these trials produced. Fresh subagents on the host's
default model, one run each, told to follow the skill text at a path and barred from the Skill
tool; "released" arms followed the v3.5.1 text. The coordinator checked refs, files and diffs on
disk rather than the agents' summaries. `gh` was a logging stub; one log was shared by all trials,
so its seven calls, all reads, cannot be attributed.

| Case | Candidate text | Comparison arm |
|---|---|---|
| Review: defect outside the diff | found `worker.py`, listed files read | released text found it too |
| Dispatch: moved base, dirty worktree | diff named the three changed files, no `auth.py`, SHAs recorded | released text captured the same diff |
| Dispatch: replayed round, settled cause | identical round called an outage; reworded cause malformed; new blocker kept | none |
| Plan: no CONCUR line | prose agreement recorded malformed, plan NOT READY | none |
| Learn: two stores | 5 and 6 prompts with the shipped extractor, partial notices reported, no prompt text in the report | none |
| Split: three commits | separate worktree, backup holding the untracked file, one branch per intent, each checked alone | no skill: conserved the work too, in place, both changes on one branch |
| Land: ignored `.env` in the worktree | worktree kept, file escalated to the owner | released text relocated the file, then removed the worktree |
| Run: local fix beside an open PR | one line changed, no commit, remote unchanged | none |

Where an arm exists the released text or no skill passed the same fixture, so these runs show the
candidate does no harm here, not that it helps. The split trial showed step 6 could not read
"empty" once step 1 commits untracked work onto the backup; the learn trial showed the since-date
passed unreadable timestamps silently. Both are fixed in the text. The lapsed-constant case ran
under the runner as `why-09`; see README.
