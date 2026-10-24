---
name: duck-land
description: Merge approved work, run a described release process when asked, record what landed, and clean up the branch and worktree; landed means nothing left behind. Use when the user authorizes landing, merging or a release — of gate-passed work, or with the gate waived ("PR, admin merge, release, no gate") — when a gate-passed PR or version bump is ready, when the user asks what the landing or the push itself will check first, including a push that makes a repository public, or when merged work was never recorded in status or outcome documentation.
---

# Duck Land

The ship step: gate passed → merge → record → clean. A merge without a recorded outcome is work the
repo forgot; a record without a verified merge is fiction.

Follow the user's language unless they ask otherwise. Keep commands, paths, identifiers,
quoted errors and machine-readable verdicts unchanged; the duck asks for evidence in any language.
Before a step that requires a skill's procedure, load that skill and follow the named section
within existing authority; a conditional or routing mention needs no load until it applies.

A passed gate establishes readiness, not permission to merge. Use the endpoint already authorized
by the user: a request only to push or prepare a PR does not authorize merging or branch deletion.

Merged-but-unrecorded work enters at the read-back: verify what is on the default branch, record
it, name any evidence that can no longer be recovered, and merge nothing.

## Preconditions (fail closed — any miss stops the landing)

- The gate returned **`APPROVE`** per the repo's policy, with a receipt recording the required
  different-family reviewer identities, evidence, and adjudication.
  [`duck-review`](../duck-review/SKILL.md) produces that authorization; any gate yielding the same
  proof qualifies. `NOTE`, a raw reviewer approval, and "probably fine" are not gate-passed states.
- **The branch head and PR head, where present, equal the candidate SHA** the authorization covers.
  Follow repository commit conventions; no pre-squash is required. Rewriting commits before merge
  changes that SHA and requires renewed verification and authorization. The remote default branch
  is not part of this check; step 2 verifies where it ended up.
- Re-verify the base: `git fetch`, compare origin/<base> to what was branched from. **If it
  advanced, integrating it produces a new head nobody authorized**: integrate, re-run the repo's
  checks, and **re-authorize the resulting SHA** the same way this landing was authorized
  ([`duck-review`](../duck-review/SKILL.md)'s release-gate path, or the owner's renewed written
  waiver).
- CI green on the exact head being merged.
- **Commit messages and the PR description meet [`duck-dry`](../duck-dry/SKILL.md)'s prose bar**
  before merge; a squash promotes the description into the commit body.
- **A repository's first push to a public remote, or the one that flips it public: scan the bytes
  the push will transfer, never the working repository's view of them**, per
  [the public-push scan](references/public-push.md).
- **A precondition the owner directs you to waive is waived only in writing before the landing**:
  which precondition and the owner's decision, recorded where the repo keeps decisions when given;
  step 3's outcome record **names what was waived**. Waiving is the owner's call on a named
  precondition, never the doer's, never a blanket exemption.
- **A registry entry is not an authorization unless it says who authorized it**
  ([`duck-scan`](../duck-scan/SKILL.md)'s attribution rule).

## Land

1. Merge per the repository's written conventions and enforced policy. Ask the remote for its
   rules; commit history alone imposes no merge method or commit count. If neither specifies a
   method, use the sole method the remote allows; if several remain, follow the owner's stated
   preference, else the owner chooses.
   - **Policy.** Server-side rules are the policy where the host exposes them
     (`gh api repos/<owner>/<repo>/rulesets`, branch protection), whether or not your account can
     get past them; **a landing this run cannot make within the rules is an owner decision, never
     a route around them** ([`duck-decide`](../duck-decide/SKILL.md)).
   - **Shape.** Use the permitted merge method and commit format; do not rewrite a reviewed
     candidate to match inferred history.
   - **Pin the base.** Merge, or push directly where policy permits, **pinning the base at merge
     time** with a mechanism proven to refuse a moved base, per
     [pinning the base](references/pin-the-base.md).
2. **Confirm the merge landed**: read back that the new SHA is on the default branch and **its tree
   matches the candidate tree**. Read the push's full output, not its exit status: an objection the
   remote prints inside a green push ("Changes must be made through a pull request") is a finding.
   On a mismatch the landed commit goes through the gate before it is recorded. This step runs
   **after** the branch has moved, so it cannot hold a deployment a push triggers.
3. Record the outcome where the repo keeps truth (shipped log, status doc, delivery board): PR
   number, candidate SHA, landed SHA, what changed. One recorded outcome per landing. Where that
   record lives in the repo, landing it by the same route is part of this landing's authorization.
4. Close or queue obligations the change touched; items needing the owner's sign-off are queued for
   [`duck-decide`](../duck-decide/SKILL.md), never closed by the doer.
5. Clean up: load [`duck-sweep`](../duck-sweep/SKILL.md) and follow step 3 against the recorded
   candidate and landed SHAs. Before removal, check
   `git status --short --untracked-files=all --ignored`; unknown files stay kept until the owner
   decides, kept files are verified at their durable home, and nothing is deleted on a
   classifier's guess. A cleanup held on a queued `duck-sweep` keep decision leaves the landing
   complete and recorded, with the pending worktree named in step 3's entry. Record a resumable
   boundary; continue other authorized work if the host and task allow it.

## Release

A release runs a described process, never one this skill invents. Two places can describe it:

1. The repository's own release procedure, found by what it says (versioning, tagging,
   publishing), not by file name. Its rules come first.
2. `[release].procedure` (default unset) in `~/.askrubberduck/config.toml`, or a bare `procedure` in
   the origin's `[repo."<origin>"]` table: a path to a procedure the owner keeps outside the
   repository. It fills what the repository leaves open and replaces a repository rule only where
   it says so. Quote nothing from it into public text.

Found one: a release request authorizes what the procedure describes as well as the merge. The
preconditions still bind, the gate covers the last release tag through the candidate
([`duck-review`](../duck-review/SKILL.md)'s code-release target), the landing ends by reading back
what the procedure produced, and step 3's record names the version and tag.

Found none: the request is a landing (merge, read back, record, clean up) and the report says no
release procedure was found. Tagging and publishing wait for one.

## Common mistakes

- Leaving the worktree "for reference": the record is the reference; the worktree is debt.
- Skipping the base re-verify because the branch is "fresh": fresh was true when you last fetched.
