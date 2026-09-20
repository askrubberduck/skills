# Evals

`evals.json` holds eleven positive and seven negative cases. They are the submission test cases for
the OpenAI plugin directory and the regression set for skill triggering, and they are the same
cases either way.

Every case runs in a clone of this repository with no credentials, no network, and no third-party
CLIs. A reviewer needs nothing that is not in the clone.

## Running one

A case is graded against a baseline, not against a feeling. Run the prompt twice in a fresh
session each time — once with the plugin installed, once without — and compare:

    with:     the behavior in `expect`, in the shape `result_shape` describes
    baseline: whatever the host does unprompted

A positive case that passes both ways does not demonstrate an improvement from the skill; record
selection and behavior separately. A negative case should stay out of the way in either setup.

## Negative cases

Cases 6-8, 12, 15, 16, and 18 pass when the plugin declines, confirms, or stays out of the way.
Cases 6, 12, 15, 16, and 18 fail if any skill fires at all. Cases 7 and 8 fail if the destructive or unreviewed action happens
quietly — doing it after an explicit, informed reaffirmation is a pass.

## Other languages, same duck

English remains the language of the skills and their public presentation. Start with the same
English descriptions for every request language. Cross-language intent matching is a hypothesis;
translating a phrase does not earn a pass.

`routing.json` holds English and Russian selection probes for every skill. In a fresh session with
the candidate installed, ask the host to select the primary skill or none for one probe without
executing the workflow. Do not show the expected `skill`, other probes, or this guide. These are
selection-only checks: they can cover dispatching skills without running their model workflows.
Also run the no-skill cases in `evals.json` as selection probes to detect false matches.

The Russian phrases formerly embedded in descriptions now live in this corpus. No hint has a
recorded comparison demonstrating benefit, so the baseline has none. Keep expected skill names
out of the model's input; copying an answer from the corpus is not routing.

Cases 9-12 run in Russian. Cases 9 and 10
are cases 2 and 1 translated — same fixture, same expected cause — so a language regression shows up
as one case passing while its twin fails. Case 11 reaches a skill the English cases do not. Case 12
is a possible false match across languages: «почисти» aimed at prose rather than at a
backlog, a repository, or code comments.

An answer that drifts back to English fails a Russian-response case even when the right skill fired.
The user's explicit language request takes precedence. Paths, commands, identifiers, quoted errors,
and machine-readable verdicts are never translated.

Cases 13-18 probe the boundary: a paraphrase absent from the description, a mixed-language status
request, prose simplification, a toy duck race, an explicit English reply request on a Russian task,
and the English twin of the prose false match. The verb alone does not get to choose the workflow.

For another trigger language, add prompts to the existing routing cases and reuse behavioral
fixtures. Include natural task wording, unseen paraphrases, mixed-language requests, false matches,
and explicit reply-language overrides. Keep the same outcome checks; select the skill from English
descriptions before considering a language hint.

When a miss survives clearer English scope, compare the same candidate with and without one short
hint in `description`. Rerun the failing request, unseen variants, English cases, neighboring skills,
and false matches. Retain a hint only when recorded results show the benefit without new misrouting.
Keep English purpose and scope at the front and the 600-character ceiling fixed. Ten languages do
not buy ten times the discovery context.

Record the host, model, candidate revision (plus a diff or snapshot for uncommitted work), prompts,
actual skill selection, response language, and observed results after running. Separate selection-only
results from workflow results. Scope any support claim to the tested skills, cases, host, and model.
A case file is a question to ask the duck, not a receipt saying it passed.

## Current evidence

| Language | Prepared coverage | Evidence for the current descriptions |
|---|---|---|
| English | Selection probes for every skill; existing behavioral cases; runner suites for why, dry, shape and scan | Two bounded selection probes on 2026-09-17; with/without runs for four skills on 2026-09-18, see Runner suites |
| Russian | Selection probes for every skill; behavioral cases 9-17 | No recorded host/model routing runs |

The rest of the routing corpus and cases 13-18 are unrun. Earlier runs, if any, do not verify changed
descriptions. Package validation checks distribution structure; it cannot establish language support.

### Local selection probes, 2026-09-17

Two fresh Codex subagents each received the current English names/descriptions and one prompt, with
no expected answer or skill body. Runtime model identity was not exposed by the collaboration tool;
these results establish neither a pinned-model comparison nor cross-host reliability.

| Prompt | Observed selection |
|---|---|
| Trunk is still failing in CI after this PR. Find the cause. | `duck-why` |
| Explain how this API worked in version 1 compared with version 2. Nothing is failing; I only want a historical explanation. | none |

Both match the oracle. On the probe date `duck-why`'s description was unchanged from `4dff3ea`; the supplied roster
included the initial findings-only `duck-review` description, before its scope was broadened beyond
PRs. No workflow ran and no improvement over old routing is claimed. The broader review description
and added non-PR probes remain untested. These probes did not justify expanding `duck-why`'s
description; the runner suites below did, a day later.

## Coverage

Directory-submission cases avoid independent `duck-review` and `duck-race` workflows, which need
another model family and tools a reviewer may not have installed. Diet can audit supplied usage
records without dispatching another model; model-routing experiments need their own tools and checks.
Selection probes do not verify those workflows. `proof-cases.md` also covers
in-session findings-only review without external CLIs. Running the gate on this repository can
exercise independent review, but only a recorded run establishes what actually happened.

## Cleanup and planning

[Cleanup cases](cleanup-cases.md) compare old and revised shape/frame/plan guidance on bounded
code-cleanup and CSV-design fixtures. Both versions passed; the record distinguishes observed
output changes from unproven improvement and lists the untested companion edits.

[Workflow cases](workflow-cases.md) exercise dry, why, campaign, roast and diet against unnecessary
archiving, over-planning, invented findings and unsupported cost claims, with paired baseline results.

## Runner suites

The `why-*`, `dry-*`, `shape-*` and `scan-*` directories are `claude plugin eval` cases: a prompt
with its fixture pasted inline, outcome graders beside it. Each prompt runs with the plugin and
without it; the number to read is the difference. One flow per run, because a mean across flows
describes none of them:

    claude plugin eval . --ablation with-without --judge-model sonnet -j 4 --case 'scan-*'

Cases grant only the Skill tool, so nothing is edited or executed. The reproduce and verify halves
of `duck-why`, `duck-dry` and `duck-shape` are untested here; the cases check that the answer
admits that limit. The judge sees the answer and the rubric, never the prompt — a rubric that
compares against the original file carries that file.

### Run of 2026-09-18

Candidate `290d548` (plugin 3.5.0), Claude Code 2.1.274, default agent model, Sonnet judge, three
runs per arm.

| Flow | With | Without | Mean Δ | Skill fired on should-fire runs |
|---|---|---|---|---|
| `scan` | 1.00 | 0.65 | +0.35 | 18/18 |
| `dry` | 0.98 | 0.86 | +0.12 | 15/15 |
| `shape` | 0.98 | 1.00 | −0.02 | 3/15 |
| `why` | 0.87 | 0.90 | −0.03 | 9/18 |

Six cases (`why-04`, `why-05`, `shape-02`, `shape-03`, `shape-04`, `scan-06`) were rerun the same day after
their graders failed correct answers; the table uses the reruns, which ran the graders as
committed (`why-04` gained `gives-local-reproducer` in its rerun, so both runs score it the same way). The first three `why-05` fixtures
were decidable — per-worker counters and a "well below 500" cue let arithmetic rule one cause out,
and the answers that did so were right. The committed fixture shares the counter and gives no rate.

No should-not-fire case fired in either arm. `duck-why` never loaded for the decoy traceback and
loaded once in six runs for the CI-only failure (8/18 in the first run, the ninth in the `why-04`
rerun); `duck-shape` loaded only for the prompt that said "AI slop". Where a skill did
not load, both arms ran the same agent and the difference is noise. In `why-06` the with-plugin arm
passed only in the run where the skill loaded. In `why-05` the skill loaded every time and the
answer led with one "most likely cause" in two runs of three, while the no-plugin arm passed three
of three; on a second draw the no-plugin arm passed one of three, so three runs do not settle this
case. No run in either arm of `why-04` offers a local reproducer. The `duck-cut` regex in `scan-04` can only pass
with the plugin installed and carries half weight for that reason.

### Description experiment, 2026-09-18

A scratch copy of `290d548` changed only the `duck-why` and `duck-shape` descriptions: symptom
phrasings the missed prompts used (a pasted traceback, passes locally and fails in CI, shorten,
over-engineered, too defensive, which of two designs carries less) and a clause that a pasted
snippet still counts. With-plugin arm only, three runs, same judge. The phrasings were taken from
the prompts that had failed to load the skill, so the firing rates below are in-sample: they show
the misses are closed, not how unseen wording routes. `routing.json` was not rerun, and misrouting
into neighbours other than `duck-dry` — `duck-roast` shares "over-engineered" and "bloat" with the
new `duck-shape` text — is unmeasured.

| | `290d548` | candidate |
|---|---|---|
| `duck-why` fired on should-fire runs | 9/18 | 18/18 |
| `duck-shape` fired on should-fire runs | 3/15 | 14/15 |
| Fired on a should-not-fire case (`why`, `shape`, `dry`) | 0/18 | 0/18 |
| `dry-*` still selected `duck-dry` | 15/15 | 15/15 |

With the skill loading, `why-04` gave a local reproducer in three runs of three (none before) and
`why-06` dropped the unrequested cleanup list in three of three. `why-05` did not improve: the skill
loaded and the answer still led with one likely cause. A one-line addition to the `duck-why` body,
telling it to lead with the unresolved question when nothing separates two causes, changed the
opening in three runs of three and the grade in two; the no-plugin arm swung between one and three
passes across draws, so that line is not yet shown to help. A `duck-shape` line about swallowed
errors changed nothing measurable. Neither candidate is applied here. `why-07` failed three of three
in the candidate's with-plugin arm without the skill loading; the cause is not known.

### Run on the new descriptions, 2026-09-18

Candidate `21addad` (the `duck-why` and `duck-shape` descriptions above, nothing else), same host,
judge and run count as the first run.

| Flow | With | Without | Mean Δ | Skill fired on should-fire runs |
|---|---|---|---|---|
| `scan` | 0.99 | 0.75 | +0.24 | 18/18 |
| `why` | 0.93 | 0.74 | +0.19 | 18/18 (was 9/18) |
| `shape` | 0.98 | 1.00 | −0.02 | 12/15 (was 3/15; 14/15 on the scratch copy) |
| `dry` | 0.91 | 0.95 | −0.04 | 15/15 |

No should-not-fire case fired in either arm. `duck-why` now loads every time; its with-plugin score
rose from 0.87 to 0.93, with `why-04` and `why-06` passing three of three. The rest of the `why` Δ is
the no-plugin arm falling from 0.90 to 0.74 on the same prompts. `dry` and `scan` did not change
between the runs and their Δ still moved by 0.16 and 0.11. Both tables predate the tightening of
three half-weight regexes; replayed, the committed patterns change one reported cell, the `why`
no-plugin mean, from 0.74 to 0.73. At three runs a flow's Δ carries about 0.1 to 0.2 of noise, so
a single run settles only the large effects (`scan-02`, `scan-05`, `why-03`).
`duck-shape` loads and changes nothing the graders can see; the no-plugin arm already passes these
fixtures.

### `why-05` at ten runs, 2026-09-18

Released v3.5.1 against a scratch copy that adds one sentence to `duck-why`, under "Separate
plausible causes": *When two explanations fit and no available observation separates them, lead
with the unresolved question and the discriminator; plausibility is not evidence, so do not rank
one as near-certain.* Same fixture, same judge; the skill loaded in all twenty with-plugin runs.

| Arm | Passed `stays-unresolved` | Judge votes |
|---|---|---|
| v3.5.1, with plugin | 3/10 | 9/30 |
| v3.5.1, no plugin | 5/10 | 15/30 |
| scratch copy with the sentence, with plugin | 9/10 | 27/30 |

As released, `duck-why` names one cause as most likely on evidence that fits two, no less often
than the agent without it. The sentence is not applied in this repository.

### `why` and `split` on the archaeology clause and the new skill, 2026-09-20

Candidate `7a68177`: `duck-why`'s description gains "when or why an existing constant, check or
behavior was introduced", and `duck-split` is new. Same host, judge and run count as above.

| Case | With | Without | Skill fired |
|---|---|---|---|
| `why-07-neg-history` | 0.83 | 0.67 | 0/3, as required |
| `why-09-lapsed-constant` | 1.00 | 0.78 | 3/3 |
| `split-01-mixed-commit` | 1.00 | 1.00 | 3/3 |
| `split-02-neg-rebase` | 1.00 | 1.00 | 0/3, as required |

The clause did not pull the history explanation into `duck-why`; `why-07`'s lost points are its
answer rubric, in both arms. `why` as a flow scored 0.94 with and 0.77 without, the skill loading on
21 of 21 should-fire runs. `duck-split` routes and adds nothing the graders can see: the agent
without it already sorts a mixed commit by hunk. Both phrasings come from the prompts the skills
were written for, so neither says how unseen wording routes.

Both tables above predate a rewrite of the `duck-why`, `duck-split` and `duck-review` descriptions
on 2026-09-21; the shipped wording is unmeasured.
