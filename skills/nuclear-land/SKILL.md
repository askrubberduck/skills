---
name: nuclear-land
description: Merge approved work, update project records, and clean up its branch and worktree. Use when a change has passed its review gate, the user says to land, merge, push, ship, tag, cut a release, or "merge and release", a gate-passed PR is ready, or merged work was never recorded in status or outcome documentation.
---

# Nuclear Land

The ship step: gate passed → merge → record → clean. A merge without a recorded outcome is work
the repo forgot; a record without a verified merge is fiction.

## Preconditions (fail closed — any miss stops the landing)

- The gate actually returned **`APPROVE`** per the repo's policy, and its receipt records the
  required decorrelated reviewer identities, evidence, and adjudication — `nuclear-review` is how
  this collection produces that authorization; any gate yielding the same proof qualifies.
  `NOTE`, a raw reviewer approval, and "probably fine" are not gate-passed states.
- **The branch head equals the candidate SHA** — the exact commit the authorization covers — and
  the fix passes behind it are **squashed into one candidate commit** before that authorization
  is given, its message carrying the evidence. Delegated builders commit on detached HEADs and
  wrong branches; confirm the branch you are landing from — and the PR head where there is one —
  points at the candidate. The remote default branch is what landing *moves*, so it is never
  part of this equality check; step 2 is what verifies where it ended up.
- Re-verify the base: `git fetch`, compare origin/<base> to what was branched from. **If it advanced,
  integrating it produces a new head nobody authorized** — conflict resolutions and semantic
  merges ride in unexamined. Integrate, re-run the repo's checks, and **re-authorize the resulting
  SHA** the same way this landing was authorized — the review gate, or the owner's renewed written
  waiver; landing on the strength of the old authorization merges an unexamined diff.
- CI green on the exact head being merged.
- **Where this landing is a repository's first push to a public remote — or the one that flips it
  public — scan the whole shipped tree *and* its commit messages for internal identifiers** before
  the push: private repo and product names, machine-local paths (`~/code/docs/<project>`), internal
  URLs. Derive the list from the machine rather than guessing — the other remotes, the sibling
  private repos, the codenames in the history. Measured: an internal docs path shipped in a public
  README, and product codenames survived in comments after the files carrying them were renamed.
  A leaked reference is public the moment it pushes; a later deletion leaves it in the history and
  in every clone.
- **A precondition the owner directs you to waive is waived only in writing before the push** —
  which precondition, and the owner's decision, recorded where the repo keeps decisions at the
  moment it is given; step 3's outcome record then **names what was waived**. Waiving is the
  owner's call on a named precondition, never the doer's, and never a blanket exemption from the
  rest; a waiver a reviewer discovers afterward is a second violation, not a footnote.
- **A registry entry is not an authorization unless it says who authorized it.** The doer writes to
  the same decision log the owner does — re-frames, challenges, queued questions all land there — so
  an entry read as a waiver carries the owner's own words and when they were given. An unattributed
  entry is the doer's note, and reading one as permission is how a run authorizes itself in writing.

## Land

1. Merge per the repo's policy — **read that policy off the base's own history, never from habit**:
   where the last 20 commits on `origin/<base>` carry no merge commit, the branch is flat and this
   landing is not the one that mints the first — rebase or squash, one commit per packet; a stray
   merge in an otherwise flat log is not a licence, match the dominant shape. Measured:
   four `--no-ff` merges landed a campaign onto a flat `main`, breaking a convention that no config
   enforced and no reviewer flagged. Squash-merge the PR, or direct push where that is the standard,
   **pinning the base at merge time**: a base that advances between the precondition check and
   the merge lands a combination nobody reviewed, and no later check can un-land it. The merge
   must FAIL when the base moved — so **verify your mechanism blocks, never infer it from its
   name**. Measured: a bare `--force-with-lease` leases against a remote-tracking ref that any
   background `git fetch` refreshes, and it force-landed over an advanced base and **destroyed
   the other branch's commit**. Also checked and not pins: the merge-API `sha` (matches the PR
   head), a merge queue (lands a combination), require-branches-up-to-date (needs a defined check;
   admins bypass). What blocked: `--force-with-lease=<ref>:<recorded-base-sha>`, value spelled out.
2. **Confirm the merge landed**: the new SHA is on the default branch and **its tree matches the
   candidate tree** — read it back, don't assume. This is the backstop for whatever step 1's
   pinning could not prevent: on a mismatch the landed commit goes through the gate before it is
   recorded. This check runs **after** the branch has already moved, so where a push triggers
   deployment the hold has to exist before step 1 — a promise to quarantine afterwards is one
   this step cannot keep.
3. Record the outcome where the repo keeps truth: shipped log / status doc / delivery board — with
   PR number, merged SHA, and what changed. One recorded outcome per landing.
4. Close or queue obligations the change touched — the doer never closes an item that needs the
   owner's sign-off; queue those (`nuclear-decide` presents them).
5. Clean up: delete the merged branch and its worktree (`nuclear-sweep` discipline —
   verify merged, then delete). End the session at this boundary; landing is a stage transition.

## Common mistakes

- Recording the outcome before step 2's read-back — squash merges mint a new SHA; record the one
  that actually landed, not the branch head.
- Leaving the worktree "for reference" — the record is the reference; the worktree is debt.
- Skipping the base re-verify because the branch is "fresh" — fresh was true when you last fetched.
