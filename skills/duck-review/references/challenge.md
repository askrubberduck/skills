# Choose the challenge before dispatch

Separate the object being challenged, the method, participants, effort bound, and action authority.
The owner's explicit setup and repository policy constrain anything a config supplies. Select once
per stage, carry it through retries, and name it briefly; do not ask the owner to configure every
routine call.

| Setup | Default use | Evidence claim |
|---|---|---|
| Self-check | Narrow local verification with a decisive experiment | No independent review |
| Independent | Ordinary plan challenge or release review: one reviewer from a verified different family than the doer | One cross-family perspective |
| Broad | Trust-touching release review: two required reviewers from different families, at least one different from the doer; also useful for several independent risk surfaces | Broader independent input |
| Race | Two isolated implementations against common outcome checks | Comparative execution |
| Rally | Alternating test and implementation turns | Executable counterexamples |

Trust-touching means security-, privacy-, or data-sensitive work, gate-semantics changes, or an
edit to a skill, a gate or an instruction file. Repository requirements bind release gates. A
change to gate policy is judged under PRE-change rules, including prerequisites and participant
count; it never grants its own approval. Never shrink the required set after an outage or an
adverse finding, or mid-gate. A roster that cannot supply a row's required families is a missing
participant, never a quietly smaller gate.

## Start level, then escalate on evidence

Start from risk and size. Small means one file and at most fifty changed lines. The table sets
the first round of a *release* review; an analysis pass is not a round of it.

| | small | otherwise |
|---|---|---|
| not trust-touching | Independent, after a self-check of the decisive experiment | Independent |
| trust-touching | Broad | Broad |

Continue only for a named unresolved claim and a new discriminating observation, changed candidate
or different approach, within the caller's recorded bound and the owner's explicit effort limit. A
substantiated blocker holds approval; repair and recheck it before another review. A complete
review with no substantiated blocker needs no extra round. Uncertainty at the limit stays
uncertainty, not approval or an invented defect.

`remaining` and `precision` are optional measurements, not stop, continuation, escalation or
approval criteria. Do not turn an estimate or its absence into a finding.

`[bounds].review_rounds` and `[bounds].trust_rounds`, enforced by `dispatch.py`, cap the run.
Broad's budget is its two reviews, their two cross-family dispositions, and one outage retry per
participant. Before dispatch, `$LEDGER cost <setup>` reports past cost when useful; `$LEDGER` means
`python3 "<absolute path of duck-review's scripts/ledger.py>"`.

Choose the method that separates plausible explanations: rival causes, a deletion alternative, an
independent plan, an outcome oracle, or a reconstruction. Different role names or contexts are not
different families, and different families may share a faulty premise: test the premise too.
Select an available, pinned model capable of the challenge — `$LEDGER pick <stage>` chooses within
the required set in configured list order by default (`[learn].select = "fixed"`); explicit
`adaptive` selection uses recorded catches per minute for `review` only, and other stages keep
list order. The pin's effort is `[effort].trust` (default the pin's own) for trust-touching work
and `[effort].ordinary` (default the pin's own) otherwise. Use the strongest available tier for
trust-touching or unfamiliar high-risk judgments unless the owner specifies otherwise; ordinary
work may use a cheaper tier. Record the choice, with no universal cost or
quality claim.
