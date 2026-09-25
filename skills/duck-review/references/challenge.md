# Choose the challenge before dispatch

Separate the object being challenged, the method, participants, effort bound, and action authority.
Honor the owner's explicit setup and repository policy; both constrain anything a config supplies.
Select once per stage, carry it through retries, and name it briefly; do not ask the owner to
configure every routine call.

| Setup | Default use | Evidence claim |
|---|---|---|
| Self-check | Narrow local verification with a decisive experiment | No independent review |
| Independent | Ordinary plan challenge or release review: one reviewer from a verified different family than the doer | One cross-family perspective |
| Broad | Trust-touching release review: two required reviewers from different families, at least one different from the doer; also useful for several independent risk surfaces | Broader independent input |
| Race | Two isolated implementations against common outcome checks | Comparative execution |
| Rally | Alternating test and implementation turns | Executable counterexamples |

Trust-touching means security-, privacy-, or data-sensitive work, or gate-semantics changes.
Repository requirements bind release gates. An explicit smaller analysis can return useful evidence
without satisfying a stronger release gate. A change to gate policy is judged under PRE-change
rules; it never grants its own approval. Never shrink the required set after an outage or an adverse
finding to manufacture a pass. A roster that cannot supply a row's required families is a missing
participant, never a quietly smaller gate. Report incomplete participation and its effect on the
claim.

## Start level, then escalate on evidence

Start from risk and size. Small means one file and at most fifty changed lines. The table sets
the first round of a *release* review; an analysis pass is not a round of it.

| | small | otherwise |
|---|---|---|
| not trust-touching | Independent, after a self-check of the decisive experiment | Independent |
| trust-touching | Broad | Broad |

After each round, one of these holds, in this order:

1. A substantiated `BLOCKER` → one more round, because defects cluster.
2. Two eligible captures (Broad, or Independent escalated once) → `scripts/ledger.py remaining`;
   another round while its estimate is at least one, stop below; "insufficient evidence" from it
   counts as at least one.
3. One capture and no `BLOCKER` → stop, unless the round found nothing at all and the reviewer
   has no recorded precision at or above 0.8 for any class on this repository
   (`scripts/ledger.py precision`, which filters by origin) — then escalate
   once to Broad, because a silent review with no history is the case with the least evidence.
   Precision measures substantiation of what was claimed, not what was missed; it earns a stop
   only together with a clean round.

Ceilings against a wrong estimate: `[bounds].review_rounds` and `[bounds].trust_rounds` in
`~/.askrubberduck/config.toml`, whose defaults `duck-run` states. Broad's budget is its two
reviews, their two cross-family dispositions, and one outage retry per participant. Never reduce
the set mid-gate; a smaller start applies to the next gate. Before the first dispatch, say what
it will cost: `scripts/ledger.py cost <setup>` reads it from past dispatches.

Choose the method that separates plausible explanations: rival causes, a deletion alternative,
an independent plan, an outcome oracle, or a reconstruction. Share requirements and source access;
keep initial conclusions independent. Different role names or contexts are not different families,
and different families may share a faulty premise. Test the premise too. Select an available,
pinned model capable of the challenge — `scripts/ledger.py pick <stage>` chooses within the
required set from the stage's list by recorded catches per minute, or in list order when
`[learn].select` is `fixed` (default `adaptive`). The chosen pin's effort is `[effort].trust`
(default the pin's own) for trust-touching work and `[effort].ordinary` (default the pin's own)
otherwise. Use the strongest available tier for trust-touching or unfamiliar high-risk judgments
unless the owner specifies otherwise. Ordinary work may use a cheaper tier; record the choice
without making a universal cost or quality claim. The participant counts and tiers above are
conventions, not measured calibration; the dispatch ledger is where that measurement accumulates.

A new round needs a named unresolved claim and new evidence or a different approach. Keep explicit
owner effort limits. Uncertainty at the limit stays uncertainty, not approval or an invented defect.
