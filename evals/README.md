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
| English | Selection probes for every skill; existing behavioral cases | No recorded host/model routing runs |
| Russian | Selection probes for every skill; behavioral cases 9-17 | No recorded host/model routing runs |

The new routing corpus and cases 13-18 are unrun. Earlier runs, if any, do not verify the changed
descriptions. Package validation checks distribution structure; it cannot establish language support.

## Coverage

Behavioral cases avoid `duck-review`, `duck-race`, and `duck-diet` on purpose: those dispatch a
second model family through `codex` or `agy`, which a reviewer will not have installed. Their
selection probes do not verify those workflows. Running the gate on this repository can exercise
them, but only a recorded run establishes what actually happened.
