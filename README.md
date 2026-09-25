<p align="center">
  <img src="assets/logo.svg" width="112" alt="askrubberduck">
</p>

# askrubberduck

[English](README.md) · [Русский](README.ru.md)

**Agent Skills that make the work prove itself.**

For Claude Code, Codex, Cursor, Copilot, and any host that reads Agent Skills.

Rubber duck debugging works because the duck says nothing. You explain the bug line by line, and
somewhere around the fourth line you hear it yourself.

Your coding agent has no duck. When it says the change is done, who checked?

These skills are the duck. Explain the goal. Show the path. Run the check. The duck keeps asking
where the claim could break, including the claim that this thing needed building at all.

Your preferred answer gets the same treatment as every other answer. So does the duck's.

## Say it to the duck

Install once, then talk to your agent as usual. The descriptions do the routing.

Ask in your language; the skill descriptions stay in English.
Routing evidence: two English selection probes, plus with/without runs for four skills — see the [eval guide](evals/README.md).

| You say | What comes back |
|---|---|
| "duck it" | `duck-run`: challenge it, plan it, build it, try to break it. Stop where you authorized; local means local. |
| "why is this broken?" | `duck-why`: the cause, its evidence and where the fix goes, or the hypotheses still standing and the check that would decide. Nobody has written the fix yet. |
| "prove this goal or plan" | `duck-proof`: what would make it wrong, what was tried, and what survived. Your favorite answer gets no head start. |
| "frame it before we plan" | `duck-frame`: the smallest design that meets the contract, traced through what already exists. Deleting something is one of the options. |
| "plan it" | `duck-plan`: units someone can build and check, and the cheap experiment run before the expensive guess. Everyone agreeing does not make it feasible. |
| "clean up the AI slop" | `duck-shape`: make every layer earn its place. Cut the needless machinery, keep the contracts, run the checks. |
| "simplify it deeply" | `duck-shape`: take the mechanism apart, keep the contracts, rebuild the path with less to remember. Then check it. |
| "gate it" | `duck-review`: one verdict, the reviewers named, and the evidence behind every finding. No participation trophies. |
| "review this work from multiple angles" | `duck-review`: findings backed by evidence on a design, plan, document or implementation, reported in-session. No edits or publication. |
| "are these review comments still valid?" | `duck-review`: each thread judged against what you pushed since, with a drafted reply. Nothing posted or resolved for you. |
| "land it" | `duck-land`: merge what the gate approved, read back what landed, record it, clean up. A merge nobody recorded is work the repo forgot. |
| "try to break it" | `duck-break`: attacks actually run, with inputs and results. Imagining a crash is not crashing it. |
| "dry it" | `duck-dry`: prose that earns its place, with checks that the sweep did not smuggle in a code change. |
| "trim the backlog" | `duck-cut`: retire obsolete work, merge duplicates, unblock what still matters. Every task earns its place. |
| "walk me through my decisions" | `duck-decide`: one decision at a time, options with their costs, and a recommendation. Your silence decides nothing. |
| "what doesn't belong in this branch?" | `duck-split`: every part sorted against the intent, and where each hitchhiker belongs. Moving them is a separate ask, and comes with proof nothing fell through the cracks. |
| "what's next?" | `duck-scan`: what is ready, what is blocked, and why. Looking is free. |
| "do all the plannable work" | `duck-campaign`: workstreams that ship without waiting on each other, and one roster that says what is blocked and why. |
| "race it" | `duck-race`: two independent attempts, the same outcome checks, and a winner that earned it. |
| "roast it" | `duck-roast`: the findings that stand up, what to do about them, and an end to the round. |
| "why does this session cost so much?" | `duck-diet`: measured waste, not a hunch, and cuts that keep the guidance the work needs. |
| "clean up stale branches" | `duck-sweep`: checks that work is preserved before deleting it; discarding unique work takes your explicit decision. Unknown means keep. |
| "what did we learn?" | `duck-learn`: lessons from sessions and outcomes, each in one home, tried once before it is trusted. |

## Install

Hosts read skills at startup. Whichever route you take, start a new session afterwards.

### Claude Code

```
/plugin marketplace add askrubberduck/skills
/plugin install askrubberduck@askrubberduck
```

Or from a shell:

```bash
claude plugin marketplace add askrubberduck/skills
claude plugin install askrubberduck@askrubberduck --yes
```

Or link a clone into your personal skills directory, which loads them unnamespaced:

```bash
git clone https://github.com/askrubberduck/skills askrubberduck-skills
mkdir -p ~/.claude/skills
ln -s "$PWD"/askrubberduck-skills/skills/* ~/.claude/skills/
```

**Cloud sessions.** Claude Code on the web, `claude --cloud`, and routines clone the repo into a
fresh container and never read `~/.claude/`. A cloud session on this repository needs no setup: its
`.claude/skills/` links every skill, so `/duck-cut` resolves from the checked-out branch. For any
other repository, declare the plugin in that repository's `.claude/settings.json`; repo-declared
plugins install at session start, plugins enabled only in your user settings do not travel:

```json
{
  "extraKnownMarketplaces": {
    "askrubberduck": { "source": { "source": "github", "repo": "askrubberduck/skills" } }
  },
  "enabledPlugins": { "askrubberduck@askrubberduck": true }
}
```

### Codex

```bash
codex plugin marketplace add askrubberduck/skills
codex plugin add askrubberduck@askrubberduck
```

`master` moves. To pin a release, add `--ref <tag>` to the first command.

### Cursor, Copilot, Codex IDE, and any host that reads Agent Skills

Link the clone into the directory these hosts share:

```bash
git clone https://github.com/askrubberduck/skills askrubberduck-skills
mkdir -p ~/.agents/skills
ln -s "$PWD"/askrubberduck-skills/skills/* ~/.agents/skills/
```

`npx skills add askrubberduck/skills` does the same through the `skills` CLI and picks the
directory per host. A host that reads `AGENTS.md` but discovers no skills gets
[`AGENTS-CATALOG.md`](AGENTS-CATALOG.md) pasted into it.

Do not add standalone links to a profile that already has the plugin; the host then lists every
skill twice.

### What you type

| Installed as | You type |
|---|---|
| Claude Code plugin | `/askrubberduck:duck-run` |
| Codex plugin | `$askrubberduck:duck-run` |
| Standalone links, any host | `/duck-run`, `$duck-run`, or the host's picker |

Inside a skill, a sibling is named bare, `duck-proof`, because that is the one name every host
resolves.

## Meet the ducks

<!-- skills-table:start -->
| Skill | What it does |
|---|---|
| `duck-break` | Try to break a system's claimed behavior, then show what actually happened |
| `duck-campaign` | Carve a grand vision into independent workstreams that ship without waiting on each other |
| `duck-cut` | Shrink a backlog the honest way — obsolete work out, duplicates merged, viable items unblocked |
| `duck-decide` | Walk the owner through the decisions they have been ducking, one at a time |
| `duck-diet` | Put agent context, memory, and token costs on a diet without starving the essential guidance |
| `duck-dry` | Strip comments, docstrings, commit messages, and PR descriptions until only unobvious decisions, contracts, and traps survive |
| `duck-frame` | Settle a system's target design before planning begins, because 'we'll figure out the architecture later' means never |
| `duck-land` | Merge approved work, update project records, and clean up the branch and worktree; landed means nothing left behind |
| `duck-learn` | Turn session and delivery evidence into reusable lessons, so each mistake is only paid for once |
| `duck-plan` | Find the hole in the plan before building over it; assumptions and acceptance checks must survive challenge |
| `duck-proof` | Make the goal, the path, and the finished work earn your trust through counterexamples and executed checks |
| `duck-race` | Put two different model families on the same problem and let executed evidence pick the result |
| `duck-review` | Review work from multiple angles or deliver an independent judgment |
| `duck-roast` | Roast the whole solution until its weak claims show; a finding must earn its place, and a round must end |
| `duck-run` | Challenge the goal, shape the plan, build it, and make it prove itself; local means local |
| `duck-scan` | Find ready, blocked, and remaining work without changing anything; looking is free |
| `duck-shape` | Make every layer earn its place; cut the machinery the problem never asked for |
| `duck-split` | Hold a branch, PR or document to the one thing it was opened for; nothing rides along, nothing falls off |
| `duck-sweep` | Clean out stale branches, worktrees, checkouts, scratch directories, and ignore rules; the pond stays clean |
| `duck-why` | Name the cause of a failure before anyone writes a fix, because the symptom is not the defect |
<!-- skills-table:end -->

## What the duck holds to

**The duck asks for proof.** “The tests pass” starts a conversation. Which tests? Against whose
requirements? What input should break this? Did you run them after the last fix? A gate returns
`APPROVE`, `REJECT`, or `NOTE`, with evidence someone else can check. Confidence earns nothing.

**The duck travels light.** One home per fact. One owner per rule. A layer that makes the reader
open three more files has some explaining to do. A comment that repeats the next line goes. A necessary
boundary stays, however tempting the deletion count. Shorter code can still leave a bigger mess.

**The duck reads first.** Follow the path from the input to what actually happens. Read the callers.
Find the constraint that made the ugly bit necessary before removing it. When the cause is still a
hypothesis, call it one. A plausible story does not become a reproducer by being told twice.

**The duck knows when to stop.** The agent owns the work and the review loop. You own the decisions
that change the goal, scope or policy. Settled decisions stay settled until evidence changes them.
Another reviewer wanting another abstraction is not evidence. Nobody gets to move the finish line
just because the code reached it.

**The duck asks before it acts outside your checkout.** Commits, pushes, pull requests, merges,
posted review comments and resolved threads each need your go-ahead; a passed review does not
grant one. So does sending your code to another model vendor, deleting work that exists nowhere
else, and waiving any rule a gate enforces. Local edits you asked for need no second permission.
One exception is the duck's own config: with `[learn].discover` left at `auto`, `duck-learn` puts a
new model on trial and applies trial verdicts to `~/.askrubberduck/config.toml` itself, then tells
you what it changed. Set it to `propose` to be asked first.

## How the duck carries a task

`duck-run` carries the work. Each stage hands the next something it can check.

1. **Frame**, `duck-frame`. What outcome dies if this never ships? What already solves it?
   Use `duck-shape` while choosing the boundaries, before a bad seam becomes a plan.
2. **Plan**, `duck-plan`. Shape the path before dividing the work. Name the assumptions and the
   checks that could kill them. Run the cheap experiment before building on the expensive guess.
3. **Execute.** Make the meaningful check fail, make it pass, then apply `duck-shape` and
   `duck-dry` inside that unit. “We'll simplify it later” has had enough chances.
4. **Prove**, `duck-proof`. Attack the goal, the behavior and the finished shape. `duck-break`
   runs hostile experiments where needed. Fix something? Run the affected checks again. Yesterday's
   green does not cover today's edit.
5. **Review**, `duck-review`. Where the task or release policy requires it, independent reviewers
   challenge the exact candidate. A missing reviewer leaves a missing review, never a quiet pass.
6. **Land**, `duck-land`. When you authorized a merge: merge, read back what landed, record it,
   clean up. Asked for local changes? The verified local diff is the finish line.

Around the run: `duck-scan`, `duck-cut` and `duck-decide` before it; `duck-diet` throughout;
`duck-split` before review, when a branch or document picked up hitchhikers; `duck-sweep` and
`duck-learn` after.

## How the duck clears a backlog

A backlog grows by itself. The duck makes it smaller before it makes it busier.

1. **See what is there**, `duck-scan`. Ready, blocked, and why, without touching anything. The
   backlog lives where your instructions say it does, even outside the repository. A blocker
   nobody can confirm is unknown, and unknown is never ready.
2. **Argue against every item**, `duck-cut`. Close what is done, cut what nobody needs any more,
   merge duplicates, unblock what is no longer blocked. Each verdict carries its evidence. The
   rest stays, with the sentence that saved it.
3. **Ask you only what is yours**, `duck-decide`. One decision at a time, with options, costs and a
   recommendation. Your answer is written down before the next question.
4. **Run what is left**, `duck-campaign`.

## How the duck runs a campaign

`duck-campaign` takes a vision, a backlog or a list of gaps and carries many tasks at once. Each
one ships without waiting on the others.

1. **Find what is needed**, `duck-scan` and `duck-cut`. What is open? What already solves it?
   Which findings share one cause? Speculative work leaves before it becomes a packet.
2. **Settle what the packets share**, `duck-frame`. A shared contract is decided once, not once
   per packet.
3. **Group by how the work runs.** Changes that share a rule or a check stay together. Different
   owners, release timing or risk split apart. Each packet names its outcome, dependencies and
   the check that says it is done.
4. **Run each packet**, `duck-run`. In parallel only where the work is independent. One roster
   says what is ready, what is blocked, and why.
5. **Finish before starting.** A packet waiting on a review this run could finish beats a new one.
   Blocked work waits with its blocker named; everything else keeps moving.

The campaign stops when the authorized work is done or everything left is blocked, and says which.
Your answer is needed only where a decision is really yours.

## How the duck shapes code

`duck-shape` removes what makes code hard to change without losing what it must do. Smaller is
not the goal. Easier to change is.

1. **Pin what must survive.** Outcomes, errors, recovery, public contracts. Run the existing checks
   before touching anything. A material contract with no check gets one that pins what the code
   does today.
2. **Look for what can go.** Duplicate rules, dead paths and flags, pass-through wrappers,
   reimplemented helpers, guards for states that cannot happen, tests that mirror the code.
3. **Decide each one on evidence**: remove it, replace it with something that already exists, or
   keep it. A caller, a contract or a failure case decides. "Separation of concerns" and "we might
   need it" do not.
4. **Cut the smallest justified piece, then check.** Rerun the checks and try a realistic next
   change. Is there one rule fewer to remember, one place fewer where a fact lives?

"Nothing to cut" is a valid answer. When local cleanup cannot fix a wrong boundary, `duck-shape`
takes the mechanism apart and rebuilds it with less to remember. Asked only which of two designs
carries less, it compares them and edits nothing.

## How the duck races two models

`duck-race` gives one problem to two different model families, and executed checks pick the
result. It has two modes.

- **Race**: which implementation? Both attempt the problem in isolated worktrees from the same
  frozen statement. The same outcome checks run on both. The evidence picks the winner; parts are
  combined only when that improves the result, and the combination is checked again.
- **Rally**: which edge cases? One side writes a single failing test and proves it fails for the
  right reason. The other makes it pass without touching the test. Then they swap. The rally ends
  when every requirement has a passing test, the turn limit is reached, or both sides run out of
  ideas.

The rival must be a proven different family, and sending it your code needs your authorization.
The result is a tested candidate, not an approved one: it still goes through `duck-proof` and
`duck-review`.

## How many ducks review your work?

Enough to challenge the claim. More seats at the table do not make an experiment stronger.

A narrow proof may need one decisive self-check. A plan may need one independent critic. A race
needs two isolated attempts; a rally alternates a failing test and a repair. Choose the method that
can expose the mistake, and set the bound before starting. The agent picks a sensible setup unless
you specify one; you do not have to configure a committee for every change.

Release review has a firmer bar: by default, one reviewer from a verified different model family
for ordinary work; two reviewers of different families, at least one different from the builder,
for security, privacy, data or gate-policy changes. Your explicit setup and repository policy govern.
A smaller analysis does not satisfy a stronger release gate. A missing participant does not lower
the bar. The [challenge rules](skills/duck-review/references/challenge.md) carry the details.

Sending your repository to another vendor needs your authorization. Once it covers the work,
the duck remembers it. Asking twice is not being careful.

Evidence needs a home someone can find. A standalone proof can answer directly. Work handed to
another stage uses the project's existing record, with the candidate, checks and open claims named.
Proof and break can share a page. A pile of receipts is not a pile of proof.

### Where the duck keeps score

Who caught the bug last time? The duck writes it down. Every dispatch — a reviewer, a rival, a
critic — leaves one row in `~/.askrubberduck/dispatches.tsv`; every finding, once judged, one row
in `~/.askrubberduck/findings.tsv`. Your repository gets nothing. The rows stay on your machine, and
`~/.askrubberduck/config.toml` holds the pins and the ceilings. No file there? The bounds and the
`[learn]` values below are the defaults, and the duck works as before. The models and effort
levels are an example; the reviewer list is empty until you name one.

```toml
[families]
doer = "anthropic"
reviewers = ["openai:gpt-6-sol:high", "google:gemini-3.1-pro-high"]  # family:model:effort

[models]                    # per role; unset review, race, plan use reviewers, worker and explore the host
review = ["openai:gpt-6-sol:high", "google:gemini-3.1-pro-high"]
race = ["google:gemini-3.8-flash-high"]
plan = ["openai:gpt-6-sol:medium"]
worker = ["anthropic:claude-sonnet-5:medium"]
explore = ["anthropic:claude-haiku-4-5:low"]

[effort]                    # by risk; overrides a pin's effort, unset keeps it
ordinary = "medium"
trust = "high"

[learn]
select = "adaptive"         # adaptive: by track record; fixed: list order
discover = "auto"           # new models: off | propose | auto
shadow = 3                  # gates a trial model rides along without counting
trial = []                  # models on trial; duck-learn fills and empties it

[bounds]                    # ceilings; inside them, evidence decides when to stop
review_rounds = 3           # duck-run
trust_rounds = 2            # duck-run, trust-touching work
roast_passes = 2            # duck-roast
plan_rounds = 2             # duck-plan
rally_turns = 10            # duck-race, counted in turns
dispatch_timeout = "45m"    # every background dispatch

[review]
default = "findings"        # what a bare duck-review runs

[repo."github.com/askrubberduck/skills"]   # one origin's overrides; a list replaces, never merges
review_rounds = 2
```

The rows answer questions the duck used to guess at. How many defects did both reviewers miss?
`scripts/ledger.py remaining <gate_id>` estimates it from what they found in common. Which family catches
which class? `precision`. Who reviews next? `pick <stage>` samples from recorded catches per minute,
inside the set the gate requires. Did the change help? `paired` compares two arms on the same
cases. What is drifting? `thresholds` hands `duck-learn` its occurrences. What will this gate
cost? `cost <setup>` reads past gates. Is there a new model? `roster <models|->` lists host
models that are in no role list, no trial and no ledger row; after its shadow gates, `promote` says whether it replaces its family's reviewer, joins the
list, or goes. `scripts/ledger.py --self-check` runs each of these on a
fixture and asserts what it prints. Standard library only. A `-` means unknown; unknown never counts as zero.

### How the duck keeps review rounds bounded

The coordinating agent carries the agreed outcome, constraints and checks through every round.
Reviewers can find new defects against that agreement. They cannot turn a fresh preference into a
new requirement. Findings keep their cause and closure evidence; rephrasing one does not reopen it.

A rejection goes back to its cause: `duck-why` if it is hidden, frame if the premise broke, plan
if the decomposition failed, race or rally if the method keeps missing the same class of defect.
Before a third round, the agent must explain what new evidence that round will buy.

The default ceiling is three review rounds for ordinary work and two for trust-touching work. Changing reviewers or renaming the problem does
not reset the clock. At the limit, the agent stops dispatching, preserves the candidate and
unresolved findings, and leaves the release unapproved. A different bound comes from you or the
repo's policy. No endless pursuit of unanimous approval. No passing because everyone got tired.

When you are away, the agent still owns technical decisions within the task. It continues independent
work and holds only what needs your answer. Your silence does not choose a new goal.

## How the duck proves its work

Every push runs `scripts/validate-distribution.py --self-test`: manifests parse, skills are linked,
references resolve, generated files match, and deliberate corruptions get caught.

That proves the package holds together. To find out whether the duck does its job, give it a task
where agreement would be wrong, a green test hides a bug, or a reviewer moves the goalposts. Inspect
what it actually did. The [eval guide](evals/README.md) links the behavioral cases and records which trials
have run. An unrun trial stays unrun, even in the duck's own README.

Versions and what changed: the [releases page](https://github.com/askrubberduck/skills/releases).

[Contributing and translations](CONTRIBUTING.md) · [MIT license](LICENSE).
