# Choose the challenge before dispatch

Keep separate the object under challenge, the method, the participants, the effort bound and the
action authority. The owner's explicit setup and repository policy constrain every config value.
Select the setup once per stage, keep it through retries and name it briefly. Do not ask the owner
to configure every routine call.

| Setup | Default use | Evidence claim |
|---|---|---|
| Self-check | Narrow local verification with a decisive experiment | No independent review |
| Independent | Ordinary plan challenge or release review: one reviewer from a verified family other than the doer's | One cross-family perspective |
| Broad | Trust-touching release review: two required reviewers from different families, at least one outside the doer's family; also useful for several independent risk surfaces | Broader independent input |
| Race | Two isolated implementations against common outcome checks | Comparative execution |
| Rally | Alternating test and implementation turns | Executable counterexamples |

Trust-touching means security-, privacy- or data-sensitive work, gate-semantics changes, or an edit
to a skill, a gate or an instruction file. Repository requirements bind release gates. Judge a
change to gate policy under PRE-change rules, including prerequisites and participant count; it
never grants its own approval. Never shrink the required set after an outage or adverse finding, or
during a gate. A roster that cannot supply the families a row requires is a missing participant,
never a quietly smaller gate.

## Start level, then escalate on evidence

Start from risk and size. Small means one file and fifty changed lines or fewer. The table sets the
first round of a *release* review. An analysis pass is not one of its rounds.

| | small | otherwise |
|---|---|---|
| not trust-touching | Independent, after a self-check of the decisive experiment | Independent |
| trust-touching | Broad | Broad |

Continue only for a named unresolved claim with a new discriminating observation, a changed
candidate or a different approach. Stay within the caller's recorded bound and the owner's explicit
effort limit. A substantiated blocker holds approval. Repair and recheck it before another review. A
complete review with no substantiated blocker needs no extra round. Uncertainty at the limit stays
uncertainty, not approval or an invented defect.

`remaining` and `precision` are optional measurements, not stop, continuation, escalation or
approval criteria. Do not turn an estimate or its absence into a finding.

`dispatch.py` enforces the run caps `[bounds].review_rounds` and `[bounds].trust_rounds`. The Broad
budget is two reviews, their two cross-family dispositions, and one outage retry per participant.
Before dispatch, `$LEDGER cost <setup>` shows past cost when useful. `$LEDGER` means
`python3 "<absolute path of duck-review's scripts/ledger.py>"`.

Choose the method that separates plausible explanations: rival causes, a deletion alternative, an
independent plan, an outcome oracle or a reconstruction. Different role names or contexts are not
different families. Different families can share a faulty premise; test it too. Select an available
pinned model capable of the challenge. By default, `$LEDGER pick <stage>` chooses within the
required set in configured list order (`[learn].select = "fixed"`). Explicit `adaptive` selection
uses recorded catches per minute for `review` only. The pin's effort is `[effort].trust`
(default the pin's own) for trust-touching work and `[effort].ordinary` (default the pin's own)
otherwise. Unless the owner specifies otherwise, use the strongest available tier for trust-touching
or unfamiliar high-risk judgments. Ordinary work may use a cheaper tier. Record the choice, with no
universal cost or quality claim.
