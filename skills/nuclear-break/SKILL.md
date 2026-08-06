---
name: nuclear-break
description: Attack a finished build to expose false confidence before review. Use when a build claims completion, security-, privacy-, or data-sensitive work lacks dynamic evidence, only a green test suite supports the claim, or the user asks to "try to break it" or run a "nuclear break".
---

# Nuclear Break

The breaker EXECUTES hostile intent against the running thing. It never reads-and-opines — that is
review's job. A claim of robustness without an executed attack behind it is an opinion.

Use `$askrubberduck:<name>` as the canonical bundled-skill reference. Before its step starts, resolve
it with the active host's discovered invocation syntax. Preserve `askrubberduck:` when the host
exposes plugin namespaces; use `$<name>` or `<name>` when it exposes skills unqualified or for a
standalone install. If no installed form resolves, stop and name the missing skill; never retry
under another name after that step's side effects start.

## The five attacks

1. **Mutation pass** — delete or invert load-bearing code; the suite MUST go red. Green-after-
   deletion proves the tests don't bite, and that is a finding against the tests, not a pass.
   A green suite alone proves little; delete-the-code is the only real test check.
2. **Boundary abuse** — empty, null, huge, malformed, duplicate, and concurrent inputs at every
   trust boundary. The stated validation either holds under execution or you have a finding.
3. **Invariant attack** — take each named invariant (containment, fail-closed, isolation,
   authorization) and actively try to violate it from outside, as a hostile caller would. An
   invariant nobody attacked is a hope.
4. **Crash consistency** — kill the process mid-operation, restart, inspect state. Recovery paths
   are claims until executed.
5. **Run the real artifact** — the built binary/app on its critical paths, not the test harness.
   The suite passing and the product working are different facts.

## Contract

- Every finding's evidence is the **reproducing command or input** — paste it, don't describe it.
- Entire finding list, no severity triage — the owner weighs, the breaker surfaces.
- **The breaker never fixes.** Doer and judge stay separate: findings route to the normal pipeline
  (fix → `$askrubberduck:nuclear-review`). Fixing mid-break contaminates both roles.
- "Unbreakable" is only claimable per attack actually executed — list what was run, including the
  attacks that found nothing. Unattempted ≠ survived.
- Revert every mutation and restore clean state before reporting; a dirty tree after a break run is
  itself a finding against the breaker.

## Common mistakes

- Reading the code carefully instead of running it — that's review with extra steps.
- Skipping the mutation pass because "the suite is green" — green is the reason to run it.
- Attacking only the happy-path module — boundaries and recovery paths are where builds actually break.
- Stopping at the first break — one finding is a start; the attack list finishes regardless.
