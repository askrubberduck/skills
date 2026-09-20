# Independent dispatch

Read this only when dispatching a participant. Prefer a native isolated agent or supported API when
it supplies the required model identity, tools and authority; a CLI is one transport, not the test
of independence. Native same-family agents can provide useful forward tests but do not count as
cross-family reviewers.

Confirm existing authorization covers sending this repository to the named vendor. Record its
source and reuse it; do not ask again when it already covers this dispatch. A permission rejection
is not an outage and must not be retried through another route. Without authority, return the
missing requirement to the caller.

Record the doer's runtime family and each participant's pinned model id and family from provider
or harness metadata. Executable names and the model's conversational self-description are not
identity evidence. A provider roster or trustworthy invocation metadata can establish the identity;
unknown stays unknown. For an unfamiliar CLI, confirm the model pin is honored (for example, an
invalid model must fail rather than silently select a default). Do not repeat a proven transport
probe every round unless the harness changed.

Give independent participants separate scratch directories and initial context. Share the same
criteria and source snapshot; do not let participants read each other's draft conclusions. `$SP`
is an absolute directory under the host's sanctioned scratch root. Preserve essential evidence
in the work record before disposing of scratch output.

The brief states the language to answer in — the user's, unless they asked otherwise — and that
verdicts, rankings, paths and quoted errors stay verbatim whatever the prose language. A reviewer
told nothing answers in its own default and returns findings nobody asked for in that language.

Capture a code candidate from its fork point: `git diff $(git merge-base <base> <candidate>)
<candidate>`, and record both SHAs in the brief. For a dirty worktree drop the second argument so
the diff reaches the working tree, add each untracked file, and say the candidate has no SHA. A
plain `git diff <base>` against a base that has moved shows the base's newer commits reversed, and
the reviewer reports a blocker in a file the branch never touched.

A brief for round two or later carries the prior adjudication — each finding accepted with the
check that proves the fix, or refuted with evidence — and the settled causes by stable ID, with the
instruction not to re-report them in any rewording and to refute one only with new evidence. A
settled cause re-raised without new evidence is a malformed finding; the rest of that result still counts.

## Run the reviewers

Run from a neutral scratch directory, never the target checkout. Close stdin, use absolute paths,
and run in the background because reviews can take 10–45 minutes. Minimum shapes:

```bash
codex exec -m <pinned-model> --skip-git-repo-check "$(cat "$SP/prompt.md")" </dev/null > "$SP/codex-rN.out" 2>&1
agy --model <verified-non-doer> --add-dir "$SP" --print-timeout 45m -p "..." </dev/null > "$SP/agy-rN.out" 2>&1
```

**The prompt is an argument; the material under review is a path inside it.** Hand the reviewer
your instructions on the command line, and have those instructions name the diff, corpus, or files
by absolute path for the reviewer to open — never paste that material into the command. Pasted
material degrades the verdict — the reviewer quotes the corpus fluently and wrong, and flips
toward letting findings stand — and forces a no-tools constraint, the prompt shape that provokes
the permission-denied outage.

Sanity-check a new invocation form with `-p "Reply with exactly: OK"`. These traps yield plausible
reviews at exit 0:

- An unpinned invocation can silently use the wrong model family. Always pin `--model`, and prove
  the pin using the identity checks above.
- The prompt must be an **argument**. `--print "<text>"` can drop it, and a prompt redirected on
  **stdin** is discarded entirely — the reviewer answers with a greeting at exit 0.
- After a repair, a reviewer can replay its previous round instead of reading the new candidate.
  Have it open its result with the candidate's revision and one current line quoted from a named
  changed artifact, and compare each round's output with the last: an identical body is an outage, not a verdict.

A zero-byte, greeting-only, timed-out, or crashed dispatch is an outage: a dispatch attempted that
produced no verdict. An output that holds only a quota or credit error is an outage no retry
clears: skip the retry and report the missing participant. **A degraded dispatch is the harder
case — full length, well formed, and wrong.** Nothing in the exit status distinguishes it, so before trusting any result, check that
its quoted justifications actually support its verdict; one that cites the claim under attack as
proof of that claim is a malformed result, recorded as such and not counted.
**A REJECT is never an outage**, and a same-family pass never substitutes for a required reviewer.
