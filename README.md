<p align="center">
  <img src="assets/logo.svg" width="112" alt="askrubberduck">
</p>

# askrubberduck

**Agent Skills that make the work prove itself.**

For Claude Code, Codex, Cursor, Copilot, and any host that reads Agent Skills. MIT.

Rubber duck debugging works because the duck says nothing. You explain the bug line by line, and
somewhere around the fourth line you hear it yourself.

Your coding agent has no duck. When it says the change is done, who checked?

These skills are the duck. Explain the goal. Show the path. Run the check. The duck keeps asking
where the claim could break, including the claim that this thing needed building at all.

Your preferred answer gets the same treatment as every other answer. So does the duck's.

## What the duck holds to

**The duck asks for proof.** “The tests pass” starts a conversation. Which tests? Against whose
requirements? What input should break this? Did you run them after the last fix? A gate returns
`APPROVE`, `REJECT`, or `NOTE`, with evidence someone else can check. Confidence earns nothing.

**The duck travels light.** One home per fact. One owner per rule. A layer that makes the reader
open three more files has explaining to do. A comment that repeats the next line goes. A necessary
boundary stays, however tempting the deletion count. Shorter code can still leave a bigger mess.

**The duck reads first.** Follow the path from the input to what actually happens. Read the callers.
Find the constraint that made the ugly bit necessary before removing it. When the cause is still a
hypothesis, call it one. A plausible story does not become a reproducer by being told twice.

**The duck knows when to stop.** The agent owns the work and the review loop. You own the decisions
that change the goal, scope or policy. Settled decisions stay settled until evidence changes them.
Another reviewer wanting another abstraction is not evidence. Nobody gets to move the finish line
just because the code reached it.

## Say it to the duck

Install once, then talk to your agent as usual. The descriptions do the routing.

| You say | What comes back |
|---|---|
| "duck it" | `duck-run`: challenge it, plan it, build it, try to break it. Stop where you authorized; local means local. |
| "why is this broken?" | `duck-why`: the cause and its evidence, or the hypotheses still standing. The fix has an address; nobody has written it yet. |
| "prove this goal or plan" | `duck-proof`: what would make it wrong, what was tried, and what survived. Your favorite answer gets no head start. |
| "simplify it deeply" | `duck-shape`: take the mechanism apart, keep the contracts, rebuild the path with less to remember. Then check it. |
| "gate it" | `duck-review`: one verdict, the reviewers named, and the evidence behind every finding. No participation trophies. |
| "try to break it" | `duck-break`: attacks actually run, with inputs and results. Imagining a crash is not crashing it. |
| "dry it" | `duck-dry`: prose that earns its place, with checks that the sweep did not smuggle in a code change. |
| "what's next?" | `duck-scan`: what is ready, what is blocked, and why. Looking is free. |
| "race it" | `duck-race`: two independent attempts, the same outcome checks, and a winner that earned it. |
| "roast it" | `duck-roast`: the findings that stand up, what to do about them, and an end to the round. |

## Where to point the duck

| Looking at | Skill |
|---|---|
| a goal, design, plan, or completed change | `duck-proof` |
| one change at its gate | `duck-review`, plus `duck-break` when the change touches trust |
| the backlog | `duck-cut` |
| the whole solution | `duck-roast` |

## One change through the pond

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

### The review loop has a keeper

The coordinating agent carries the agreed outcome, constraints and checks through every round.
Reviewers can find new defects against that agreement. They cannot turn a fresh preference into a
new requirement. Findings keep their cause and closure evidence; rephrasing one does not reopen it.

A rejection goes back to its cause: `duck-why` if it is hidden, frame if the premise broke, plan
if the decomposition failed, race or rally if the method keeps missing the same class of defect.
Before a third round, the agent must explain what new evidence that round will buy.

The default is three review rounds total. Changing reviewers or renaming the problem does not
refill the meter. At the limit, the agent stops dispatching, preserves the candidate and unresolved
findings, and leaves the release unapproved. A different bound comes from you or the repo's policy.
No endless pursuit of unanimous approval. No passing because everyone got tired.

When you are away, the agent still owns technical decisions within the task. It continues independent
work and holds only what needs your answer. Your silence does not choose a new goal.

Around the run: `duck-scan`, `duck-cut`, `duck-decide`, and `duck-campaign` before it;
`duck-diet` throughout; `duck-sweep` and `duck-learn` after.

## Every skill

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
| `duck-race` | Put two decorrelated model families on the same problem and let executed evidence pick the result |
| `duck-review` | Run one independent cross-model superreview and deliver an evidence-backed APPROVE, REJECT, or NOTE; no participation trophies |
| `duck-roast` | Roast the whole solution until its weak claims show; a finding must earn its place, and a round must end |
| `duck-run` | Challenge the goal, shape the plan, build it, and make it prove itself; local means local |
| `duck-scan` | Find ready, blocked, and remaining work without changing anything; looking is free |
| `duck-shape` | Take the mechanism apart and rebuild the simplest robust path; leave the reader less to hold in their head |
| `duck-sweep` | Clean out stale branches, worktrees, checkouts, scratch directories, and ignore rules; the pond stays clean |
| `duck-why` | Name the cause of a failure before anyone writes a fix, because the symptom is not the defect |
<!-- skills-table:end -->

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

## How many ducks?

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
the duck remembers it. Asking again is not extra care.

Evidence needs a home someone can find. A standalone proof can answer directly. Work handed to
another stage uses the project's existing record, with the candidate, checks and open claims named.
Proof and break can share a page. A pile of receipts is not a pile of proof.

## Does the duck's own work pass?

Every push runs `scripts/validate-distribution.py --self-test`: manifests parse, skills are linked,
references resolve, generated files match, and deliberate corruptions get caught.

That proves the package holds together. To find out whether the duck does its job, give it a task
where agreement would be wrong, a green test hides a bug, or a reviewer moves the target. Inspect
what it actually did. The [behavioral cases](evals/proof-cases.md) state the checks and which trials
have run. An unrun trial stays unrun, even in the duck's own README.

Versions and what changed: the [releases page](https://github.com/askrubberduck/skills/releases).
