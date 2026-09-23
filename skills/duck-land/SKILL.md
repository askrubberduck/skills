---
name: duck-land
description: Merge approved work, update project records, and clean up the branch and worktree; landed means nothing left behind. Use when a change has passed its review gate, the user authorizes landing or merging, an authorized gate-passed PR is ready, or merged work was never recorded in status or outcome documentation.
---

# Duck Land

The ship step: gate passed → merge → record → clean. A merge without a recorded outcome is work
the repo forgot; a record without a verified merge is fiction.

Follow the user’s language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.

A passed gate establishes readiness, not permission to merge. Use the endpoint already authorized
by the user: a request only to push or prepare a PR does not authorize merging or branch deletion.

Work that already merged and was never recorded enters at the read-back: verify what is on the
default branch, record it, and name any evidence that can no longer be recovered. It needs no
candidate branch and merges nothing.

## Preconditions (fail closed — any miss stops the landing)

- The gate actually returned **`APPROVE`** per the repo's policy, and its receipt records the
  required different-family reviewer identities, evidence, and adjudication — `duck-review` is how
  this collection produces that authorization; any gate yielding the same proof qualifies.
  `NOTE`, a raw reviewer approval, and "probably fine" are not gate-passed states.
- **The branch head equals the candidate SHA** — the exact commit the authorization covers — and
  the fix passes behind it are **squashed into one candidate commit** before that authorization
  is given, its message carrying the evidence. Delegated builders commit on detached HEADs and
  wrong branches; confirm the branch you are landing from — and the PR head where there is one —
  points at the candidate. The remote default branch is what landing *moves*, so it is never
  part of this equality check; step 2 is what verifies where it ended up.
- Re-verify the base: `git fetch`, compare origin/<base> to what was branched from. **If it
  advanced, integrating it produces a new head nobody authorized** — conflict resolutions and
  semantic merges ride in unexamined. Integrate, re-run the repo's checks, and **re-authorize the
  resulting SHA** the same way this landing was authorized — the review gate, or the owner's renewed
  written waiver; landing on the strength of the old authorization merges an unexamined diff.
- CI green on the exact head being merged.
- **Commit messages and the PR description meet `duck-dry`'s prose bar**, checked before
  merge: a squash merge promotes the description into the commit body, so slop in either ships
  into history. A claim without its receipt is the overclaim the gate exists to stop.
- **Where this landing is a repository's first push to a public remote — or the one that flips it
  public — scan the bytes the push will transfer, where they land, never the working
  repository's view of them**: push the refs into a throwaway bare repository first
  (`git init --bare "$SP/pub.git" && git push "$SP/pub.git" <refs>`), then read every object
  there as stored — `git -C "$SP/pub.git" rev-list --objects --all | cut -d' ' -f1 |
  git -C "$SP/pub.git" cat-file --batch | grep -a -c <pattern>` — and locate a hit with
  `git -C "$SP/pub.git" grep -a <pattern> $(git -C "$SP/pub.git" rev-list --all)` and
  `git -C "$SP/pub.git" log --all --grep=<pattern>`. Every view of the working repository has
  hidden something in a gate round: the current tree misses a file added and deleted before the
  push, `git grep` reads no messages, `log -p` skips a merge's own content without `-m` and any
  file under a `.gitattributes -diff` rule, and `cat-file` obeys a local `git replace` that the
  push ignores. The throwaway receives exactly what the public remote would. The list to scan
  for: private repo and product
  names, machine-local paths (`~/…`), internal URLs, and codenames that outlived the rename of the
  files carrying them. Derive the list from the machine rather than guessing — the other remotes,
  the sibling private repos, the codenames in the history. A leaked reference is public the
  moment it pushes; a later deletion leaves it in the history and in every clone.
- **A precondition the owner directs you to waive is waived only in writing before the push** —
  which precondition, and the owner's decision, recorded where the repo keeps decisions at the
  moment it is given; step 3's outcome record then **names what was waived**. Waiving is the
  owner's call on a named precondition, never the doer's, and never a blanket exemption from the
  rest; a waiver a reviewer discovers afterward is a second violation, not a footnote.
- **A registry entry is not an authorization unless it says who authorized it** — `duck-scan`'s
  attribution rule. The doer writes to the same decision log the owner does, so an unattributed
  entry is the doer's note, and reading one as permission is how a run authorizes itself in writing.

## Land

1. Merge per the repo's policy — **ask the remote for its enforced policy first, the base's history
   only for its shape, never habit**.
   - **Policy.** Server-side rules are the actual policy where the host exposes them
     (`gh api repos/<owner>/<repo>/rulesets`, branch protection); history is a proxy. A rule the
     remote enforces is the policy whether or not your account can get past it; **a landing this
     run cannot make within the rules is an owner decision, never a route around them** —
     `duck-decide`.
   - **Shape.** Where the last 20 commits on `origin/<base>` carry no merge commit, the branch is
     flat and this landing is not the one that mints the first — rebase or squash, one commit per
     packet; a stray merge in an otherwise flat log is not a license, match the dominant shape.
     No config enforces this; the history is the only guard.
   - **Pin the base.** Squash-merge the PR, or direct push where that is the standard, **pinning
     the base at merge time**: a base that advances between the precondition check and the merge
     lands a combination nobody reviewed, and no later check can un-land it. The merge must FAIL
     when the base moved — so **verify your mechanism blocks, never infer it from its name.** Prove
     it once per host, mechanism and CLI version on a throwaway copy of the remote: run the exact
     invocation with its expected-base argument against a stationary base and record the success,
     advance the base and record the refusal, quoted. That record — `merge-pin-<host>.md` at the
     durable records home, with the invocation string, CLI version and date — is reused while the
     invocation and version match, and re-proven when either changes; a refusal alone also fits
     bad credentials, which is why both observations are kept. Where no throwaway remote is
     possible, use only a mechanism whose vendor documentation names the base-SHA comparison for
     that exact operation, record that as tier `documentary`, and rely on step 2's read-back.
     Pin an explicitly recorded base SHA, never a ref — a ref a background fetch refreshes pins
     nothing, and the cost of a false pin is the other branch's commit.
2. **Confirm the merge landed**: the new SHA is on the default branch and **its tree matches the
   candidate tree** — read it back, don't assume. Read the push's full output too, not its exit
   status: the remote prints policy objections ("Changes must be made through a pull request")
   even when the ref moves, and an objection inside a green push is a finding, never noise. This
   is the backstop for whatever step 1's pinning could not prevent: on a mismatch the landed
   commit goes through the gate before it is recorded. It runs **after** the branch has moved, so
   it cannot hold a deployment that a push triggers.
3. Record the outcome where the repo keeps truth: shipped log / status doc / delivery board — with
   PR number, candidate SHA, merged SHA, and what changed. One recorded outcome per landing. Where that record
   lives in the repo, landing it by the same route is part of this landing's authorization.
4. Close or queue obligations the change touched — the doer never closes an item that needs the
   owner's sign-off; queue those (`duck-decide` presents them).
5. Clean up: delete the merged branch and its worktree under `duck-sweep`'s step 3, which settles
   untracked and ignored files before a worktree goes; a matching tree says nothing about a
   `.env` beside it. Step 2's read-back is what makes the branch safe to delete and what
   `duck-sweep` cannot derive on its own — a squash leaves no metadata linking the branch
   to the commit that replaced it, so **record the candidate and landed SHAs in step 3's outcome
   entry** and delete against that, not against a classifier's guess. A cleanup held on a queued
   `duck-sweep` keep decision leaves the landing complete and recorded, with the pending worktree
   named in step 3's entry. Record a resumable boundary; continue other authorized work if the
   host and task allow it.

## Common mistakes

- Leaving the worktree "for reference" — the record is the reference; the worktree is debt.
- Skipping the base re-verify because the branch is "fresh" — fresh was true when you last fetched.
