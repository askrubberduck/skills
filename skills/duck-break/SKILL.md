---
name: duck-break
description: Attack a 'finished' build to find out how finished it actually is. Use when a build claims completion, security-, privacy-, or data-sensitive work lacks dynamic evidence, only a green test suite supports the claim, or the user asks to "try to break it", "red team it", or "duck break".
---

# Duck Break

The breaker EXECUTES hostile intent against the running thing. It never reads-and-opines — that is
review's job. A claim of robustness without an executed attack behind it is an opinion.

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
   are claims until executed. Start the target in **its own process group** and kill the group, not
   the pid: a killed parent leaves its children running, and the survivors hold the ports and locks
   the restart needs, so the recovery you then measure is not the one the product performs. Confirm
   no survivors before the next attack.
5. **Run the real artifact** — the built binary/app on its critical paths, not the test harness.
   The suite passing and the product working are different facts.

## Contract

- Every finding's evidence is the **reproducing command or input** — paste it, don't describe it.
- Measure the artifact's exit status **directly, never through a pipe**: `cmd | head` reports the
  tail's status, bash `PIPESTATUS` is zsh `pipestatus`, and grep exits 1 on zero matches — three
  measured ways a break run reported green while the artifact was red.
- Entire finding list, no severity triage — the owner weighs, the breaker surfaces. No triage is
  not no validation: a finding whose reproducing command does not reproduce is not a finding, and
  reporting it unchecked spends someone else's round.
- **The breaker never fixes.** Doer and judge stay separate: findings route to the normal pipeline
  (fix → `duck-review`). Fixing mid-break contaminates both roles. Separation bars the fix, not
  the thinking — the breaker still questions every attack it runs and every result it gets.
- "Unbreakable" is only claimable per attack actually executed — list what was run, including the
  attacks that found nothing. Unattempted ≠ survived.
- **Attack a disposable copy, never the candidate checkout.** Attack 1 deletes load-bearing code; a
  crash mid-attack in the shared tree leaves corruption for the next stage to read as the candidate.
- **A dirty candidate does not survive `git worktree add` or `git clone`** — both carry committed
  state only, so the copy silently holds the base commit and every attack passes against code that
  is not the candidate. Measured: an uncommitted marker present in the source was absent in the
  worktree copy. Either commit the candidate first and copy that, or copy the working tree itself
  (`cp -a`, `rsync`), and **verify the copy carries the change before attacking** — grep it for
  something only the candidate has. An unverified copy is an unrun attack list.
- Record the tree's exact pre-attack state and restore *that*, not "clean" — the candidate under
  review is allowed to be a dirty worktree, so a clean tree is the wrong target and a mismatch is
  itself a finding against the breaker.
- **Leave the receipt.** The attack list — each attack carrying the command run and its observed
  output, no-finding attacks under the same bar as findings — and the restored-state confirmation
  go to `break-rN.md`, in the project's durable records home — the same location `duck-proof`
  resolves for its own receipt, and the only place `duck-review` looks. Never the scratchpad and
  never a commit on the candidate branch. An attack listed without its artifact is claimable
  without execution, which is exactly the overclaim this receipt exists to prevent. Trust-touching
  changes cannot pass that gate without it — an unwritten break run is indistinguishable from one
  that never happened.

## Common mistakes

- Reading the code carefully instead of running it — that's review with extra steps.
- Skipping the mutation pass because "the suite is green" — green is the reason to run it.
- Attacking only the happy-path module — boundaries and recovery paths are where builds actually break.
- Stopping at the first break — one finding is a start; the attack list finishes regardless.
