# askrubberduck skills

Ask the duck. It listens to your plan, assumes it is wrong somewhere, and makes you prove
otherwise. The skills are dry, straightforward, and skeptical to a fault.

Your agent is relentlessly agreeable. It will tell you the plan is sound, the change is done, and
the tests pass, and roughly two of those will be true. These are the skills that disagree with it.

## The soul — carried by every skill

- **The doer is never the final judge** — a self-pass earns the dispatch, never the approval.
- **Evidence over assertion** — a claim without output is not done.
- **Skeptical by default** — every finding is adjudicated against source, your own fix included.
- **The most reliable code is the code never written** — would deleting this end it?
- **Cut before add** — a fix pass that only grows is not progress.
- **Concepts, not lines** — line count is a smell, never a target.
- **Token discipline** — nothing raw is dumped into your context; the rules live in `duck-diet`.
- **Fail closed** — a missing reviewer, empty output, or unverified claim is never an implicit pass.

## The map

Who hands what to whom.

### duck-run — one change, from unframed to landed

```
                  +---------------+
                  |   duck-frame  |
                  +-------+-------+
                          |          ..CUT..>  the cheapest run ends here
                  +-------v-------+
                  |   duck-plan   |  co-authored, or a solo draft that survives Critique
                  +-------+-------+
                          |
                  +-------v-------+
   +------------->|     build     |  per unit: test, pass, duck-shape, duck-dry
   |              +-------+-------+
   |                      |
   |              +-------v-------+
   |              |   duck-proof  |  ..>  duck-break first when trust-touching
   |              +-------+-------+
   |                      |
   |              +-------v-------+
   |              |  duck-review  |  the doer never votes
   |              +-------+-------+
   |                      |
   +- duck-why <- REJECT -+          ..>  a diverging loop exits to
                          |               duck-frame | duck-plan | duck-race | duck-decide
                          |          APPROVE
                  +-------v-------+
                  |   duck-land   |
                  +---------------+
```

### duck-campaign — a backlog, carved into packets that each run that line

```
                  +---------------+
                  |   duck-scan   |  candidates, with evidence
                  +-------+-------+
                          |
                  +-------v-------+
   +------------->|    duck-cut   |  standing lens: re-cut whenever a packet grows
   |              +-------+-------+
   |                      |
   |              +-------v-------+
   |              |   duck-frame  |  the system every packet lands in
   |              +-------+-------+
   |                      |          ..CUT..>  the cheapest campaign ends here
   |              +-------v-------+
   |              | carve packets |  one independently shippable change each
   |              +-------+-------+
   |                      |
   |              +-------v-------+
   |              |   duck-plan   |  every packet, before any build starts
   |              +-------+-------+
   |                      |
   |             +--------+--------+
   |             |                 |
   |       +-----v----+      +-----v----+
   |       | duck-run |  ... | duck-run |  parallel; duck-diet routes the fleet
   |       | packet 1 |      | packet N |
   |       +-----+----+      +-----+----+
   |             |                 |
   |             +--------+--------+
   |                      |
   +----------------------+          roster not empty:  the campaign books the next
                          |             session and drives the roster to empty
                          |          roster empty:
                  +-------v-------+
                  |   duck-sweep  |  nothing left behind
                  +---------------+
```

- `build` becomes `duck-race` when one attempt is not enough — race mode for which implementation,
  rally mode for which edge cases.
- A packet arrives at `duck-run` already planned, so it is never planned twice.
- On neither line: `duck-roast` at a milestone, `duck-learn` after one, `duck-scan` to look without
  touching anything.
- `duck-shape` rides `build` on both lines: the doer's lens while the code is being written, scored
  in concepts a reader must hold rather than lines or nesting. `duck-roast`'s simplicity angle is
  the same lens at milestone altitude, and `duck-review` applies it per change.
- Where a body disagrees with the map, the body wins.

## Skills

`AGENTS-CATALOG.md` carries the full trigger text.

<!-- skills-table:start -->
| Skill | What it does |
|---|---|
| `duck-break` | Attack a 'finished' build to find out how finished it actually is |
| `duck-campaign` | Carve a grand vision into independent workstreams that ship without waiting on each other |
| `duck-cut` | Shrink a backlog the honest way — obsolete work out, duplicates merged, viable items unblocked |
| `duck-decide` | Walk the owner through the decisions they have been ducking, one at a time |
| `duck-diet` | Put agent context, memory, and token costs on a diet without starving the essential guidance |
| `duck-dry` | Strip comments, docstrings, commit messages, and PR descriptions until only unobvious decisions, contracts, and traps survive |
| `duck-frame` | Settle a system's target design before planning begins, because 'we'll figure out the architecture later' means never |
| `duck-land` | Merge approved work, update project records, and clean up the branch and worktree; landed means nothing left behind |
| `duck-learn` | Turn session and delivery evidence into reusable lessons, so each mistake is only paid for once |
| `duck-plan` | Catch architectural and implementation risks before the code catches them for you |
| `duck-proof` | Give 'completed' work a skeptical second pass before anyone trusts it; 'it should work' is not evidence |
| `duck-race` | Put two decorrelated model families on the same problem and let executed evidence pick the result |
| `duck-review` | Run one independent cross-model superreview and deliver an evidence-backed APPROVE, REJECT, or NOTE; no participation trophies |
| `duck-roast` | Roast an entire product, solution, or architecture from every angle until only the defensible parts remain |
| `duck-run` | Deliver a high-risk change end to end without trusting any stage of it |
| `duck-scan` | Find ready, blocked, and remaining work without changing anything; looking is free |
| `duck-shape` | Shape code as it is written so the next reader holds as little as possible; the unit is concepts, not lines |
| `duck-sweep` | Clean out stale branches, worktrees, checkouts, scratch directories, and ignore rules; the pond stays clean |
| `duck-why` | Name the cause of a failure before anyone writes a fix, because the symptom is not the defect |
<!-- skills-table:end -->

## Prerequisites

The gate works by **sending your repository's contents to model vendors outside your machine** —
that is what decorrelation buys, and `duck-review` will not dispatch until you have authorized it
for that repository. Where the answer is no, the gate fails closed and says so; it does not
silently review with one family.

`git`, `gh`, and **two reviewer CLIs from two different model families**, at least one proven
different from the doer — the quorum `duck-review` enforces, not one. Gemini and Codex when the
doer is Claude, say. One reviewer fails the gate, by design. Executable names are not identities;
pin the model and verify what it reports — the duck has been lied to before.

## Install

Every route needs a new host session; hosts read skills at startup. Skills that need a project
registry — `STATUS.md`, `OBLIGATIONS.md`, a backlog doc — detect it or ask once. No paths are
hardcoded.

### Claude Code

```
/plugin marketplace add askrubberduck/skills
/plugin install askrubberduck@askrubberduck
```

Or symlink a clone:

```bash
git clone https://github.com/askrubberduck/skills askrubberduck-skills
mkdir -p ~/.claude/skills
ln -sfn "$PWD"/askrubberduck-skills/skills/* ~/.claude/skills/
```

#### Cloud sessions

Neither install reaches the cloud. Claude Code on the web, `claude --cloud`, and routines run a
fresh container that clones the repo and never reads `~/.claude/`. Cloud sessions load project
skills from the cloned `.claude/skills/`; this repo symlinks its own skills there, so a cloud
session on this repo runs `/duck-cut` from the checked-out branch with no setup.

For a different repo, declare the plugin in that repo's `.claude/settings.json`. Repo-declared
plugins install at session start; plugins enabled only in user settings do not transfer:

```json
{
  "extraKnownMarketplaces": {
    "askrubberduck": { "source": { "source": "github", "repo": "askrubberduck/skills" } }
  },
  "enabledPlugins": { "askrubberduck@askrubberduck": true }
}
```

That form tracks the published default branch and needs network access to GitHub.

The third route is enabling the skills on your claude.ai account — the only one that reaches Cowork.
Every skill here carries `name` and `description` only, so every skill uploads as-is.

### Codex CLI and the Codex app

```bash
codex plugin marketplace add askrubberduck/skills
codex plugin add askrubberduck@askrubberduck
codex plugin list
```

Pin a release instead of tracking `master`:

```bash
release_tag="$(gh release view --repo askrubberduck/skills --json tagName --jq .tagName)"
codex plugin marketplace add askrubberduck/skills --ref "$release_tag"
codex plugin add askrubberduck@askrubberduck
```

### Agy

```bash
git clone https://github.com/askrubberduck/skills askrubberduck-skills
agy plugin validate ./askrubberduck-skills
agy plugin install ./askrubberduck-skills
agy plugin list
```

### Standalone Agent Skills

For hosts that read Agent Skills but not this repository's plugin format — Codex IDE, Agy, Cursor,
Copilot:

```bash
git clone https://github.com/askrubberduck/skills askrubberduck-skills
mkdir -p ~/.agents/skills
ln -sfn "$PWD"/askrubberduck-skills/skills/* ~/.agents/skills/
```

Do not add standalone links to a profile that already has the plugin; the host then lists every
skill twice.

### Invocation

| Installation | User invocation | Description source |
|---|---|---|
| Codex plugin | `$askrubberduck:duck-run` | `agents/openai.yaml`, with `SKILL.md` for triggering |
| Claude plugin | `/askrubberduck:duck-run` | `SKILL.md` |
| Agy plugin | `/duck-run`; namespaced only when needed | `SKILL.md` |
| Standalone Agent Skills | Unqualified, using the host's syntax | `SKILL.md` |

The table is what a person types; skill bodies name each other by bare frontmatter name, the one
form every host resolves.

### Updating an existing install

Nothing here updates itself. The symlink forms link each skill individually, so a `git pull` that
adds a skill leaves it invisible until you relink:

```bash
git -C askrubberduck-skills pull
ln -sfn "$PWD"/askrubberduck-skills/skills/* ~/.claude/skills/    # or ~/.agents/skills/
```

Plugins update through the host — `/plugin` for Claude Code, `agy plugin install` again for Agy, and
for Codex:

```bash
codex plugin marketplace upgrade
codex plugin add askrubberduck@askrubberduck
```

### Agents without native skill discovery

Paste the block from [`AGENTS-CATALOG.md`](AGENTS-CATALOG.md) into the repo's `AGENTS.md`.

## Works well with

None of these are required — the collection is self-contained — but they compound it:

- **[ponytail](https://github.com/DietrichGebert/ponytail)** — lazy-senior-dev mode, worn rather
  than invoked, so its ladder fires before anyone asks for it.
- **[caveman](https://github.com/JuliusBrussee/caveman)** — terse-prose mode; pairs with
  `duck-diet`'s token discipline (diet cuts payloads, caveman cuts prose).
- **[rtk](https://www.rtk-ai.app/)** — hook-level CLI proxy that shrinks dev-command output before
  it reaches the context; the runtime complement to `duck-diet`'s rules.

## Credits

`duck-proof` began as an adaptation of Josh Pigford's (Shpigford) "but-for-real" skill. It has
since been rewritten and no longer carries his text; the section arc is the surviving debt.

## Status

v2.4.0, one duck — [release notes](https://github.com/askrubberduck/skills/releases).
