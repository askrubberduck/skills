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
verdicts, rankings, paths and quoted errors stay verbatim whatever the prose language. It also
says the participant is one perspective and dispatches no reviewers of its own.

Each criterion the brief takes from a repository rule is a verbatim quote of that rule, with its path
and line; the task's own requirements travel with their own source. Include governing rules and
deployment facts with their sources, distinguishing documented facts from assumptions. Do not withhold
a governing fact as an owner preference. Keep the doer's hypotheses and unwritten owner preferences or
precedents out of the initial brief; the adjudicator checks them separately. An explicit owner
requirement travels with its recorded source, including applicable earlier instructions. Shared
agreement on a premise supplied by the brief is not independent evidence for that premise.

For a dirty candidate, load [`duck-split`](../../duck-split/SKILL.md) and follow its git capture rules
before dispatch: include
staged, unstaged and relevant untracked work; inventory ignored files and preserve the user's
checkout while constructing the snapshot in isolation.

Capture a code candidate from its fork point: `git diff $(git merge-base <base> <candidate>)
<candidate>`, and record both SHAs in the brief; a base that moved otherwise shows up reversed in
the diff. A dirty worktree is first captured as a ref the way [`duck-split`](../../duck-split/SKILL.md)
does; that ref is the
candidate.

A brief for round two or later carries the prior adjudication and the settled causes by stable
ID, with the instruction not to re-report them in any rewording and to refute one only with new
evidence. A settled cause re-raised without new evidence is dismissed; the rest of that result
still counts.

## Run the reviewers

Run each seat with `python3 "$DISPATCH"` (`$DISPATCH` is the absolute path of `duck-review`'s
`scripts/dispatch.py`, whatever the working directory), in the background. Where the turn is the
whole session (`claude -p`), its end kills a background seat (`error: interrupted`) and strands its
row `pending`: poll the seat's exit in bounded waits and end the turn only after it. The pinned ids
come from `~/.askrubberduck/config.toml`, never from memory (a `[repo."<origin>"]` table there
overrides any key for that origin): `[models].review` (a review or a disposition), `[models].race`
and `[models].plan`, each defaulting to `[families].reviewers` (default empty: the owner's setup
names them).

```bash
python3 "$DISPATCH" --gate "$GATE" --round "$N" --stage review --setup independent --trust 0 --pin "$MODEL" \
  --prompt "$SP/codex/prompt.md" --out "$SP/codex/r$N.out" --add-dir "$SP/material" \
  --candidate "$CHECKOUT"
```

The script picks `codex exec`, `agy` or `claude -p` by the pin's family, runs from the
`--out` file's directory — the seat's own scratch directory, never the target checkout, unless
`--workdir` names a worktree the seat is meant to change (codex `-C`; refused for agy and Claude) — closes
stdin, kills the whole process group past `[bounds].dispatch_timeout` (default 45m) and confirms it
exited, and refuses a round past the caller's bound unless `--extended` carries the owner's
words. It exits 0 with a verdict, 1 on an outage and its cause, 2 when it refused, 3 when the seat
changed the `--candidate` checkout. A race rival adds `--diff-base <sha> --diff-out <path>`: after
a verdict the script writes the `--workdir` diff against that base whole; an outage writes none, and
an empty diff is an outage, since a race rival's answer is a change.

**`--prompt` takes a UTF-8 brief file path; the script passes its contents as a CLI argument.**
The material under review is a path inside that brief. Hand the reviewer
your instructions on the command line, and have those instructions name the diff, corpus, or files
by absolute path for the reviewer to open — never paste that material into the command.

The Anthropic route uses `claude -p` with an exact model pin and optional effort, plan permissions,
read-only file tools and no MCP servers. It does not approve writes or shell execution. Claude and agy
seats cannot take `--workdir` or serve as writable race/rally rivals; use a supported writable transport
instead. agy headless writes are denied, not a sandbox guarantee. Treat source-only findings as
`tier = read`; claim executed evidence only when the seat supplies observed command output. The outer
runner bounds all transports and finalizes their ledger rows on timeout or failure.

Sanity-check a new invocation form with the prompt `Reply with exactly: OK`, run as the bare CLI
command outside `$DISPATCH`, which would record that answer as an outage. These traps yield
plausible reviews at exit 0:

- An unpinned invocation can silently use the wrong model family. The script always pins; prove a
  new pin using the identity checks above.
- The prompt must be an **argument**, as the script passes it. agy's `--print "<text>"` can drop
  it, and a prompt it gets on **stdin** is discarded entirely — the reviewer answers with a greeting
  at exit 0. `codex exec` reads a stdin prompt, but appends piped stdin to an argument prompt.
- After a repair, require the reviewer to show it read the new candidate: have it open its result
  with the candidate's revision and one current line quoted from a named changed artifact, and
  compare each round's output with the last: an identical body is an outage, not a verdict.

A zero-byte, greeting-only, timed-out, or crashed dispatch is an outage: a dispatch attempted that
produced no verdict; the script names its cause. An output that holds only a quota or credit
error, or a rejection of the pinned model id, is an outage no retry clears: skip the retry and
report the missing participant, naming the config file that holds a dead pin. **A degraded
dispatch is the harder case — full length, well formed, and wrong.** Nothing in the exit status
distinguishes it, so before trusting any result, check that its quoted justifications actually
support its verdict.

Ask participants to label the overall result `VERDICT: APPROVE | REJECT | NOTE` (or
`PLAN: CONCUR | OBJECT`). The parser prioritizes explicit result lines; otherwise it uses the opening
standalone verdict, preserving terminal bare `DIFF` for race/rally output. A later bare severity
heading cannot overwrite the opening review verdict. Ambiguous output still
requires inspection rather than treating its parsed label as independent judgment.

Two kinds of malformed result:
*unranked* — a verdict with findings that carry no severity: the participant counts, its findings
are claims to adjudicate; *unsupported* — no verdict, or a verdict whose cited justification is
the claim under attack: the participant did not answer, the gate is short a reviewer, and its
findings are still claims. **A REJECT is never an outage.**

**A pin on trial rides along.** A pin in `[learn].trial` (default empty) rides along for its first
`[learn].shadow` (default 3) gates, and up to twice that while its comparison stays undecided;
`$LEDGER pick review` names it on a `shadow` line while it does (`$LEDGER` is `python3` with the
absolute path of `duck-review`'s `scripts/ledger.py`, whatever the working directory, typed out as
`python3 "<path>" <subcommand>` rather than held in one variable). Dispatch it beside the required
set with the same brief and the same export authorization for its vendor, or skip it and say so.
Its verdict never counts toward the gate, its outage never leaves the gate short, and its findings
are adjudicated like any other. Its row carries `setup = shadow`. A trial's gates count in
whichever repository they ran; its comparison pairs it with its family's reviewer on the same gate
of the same repository.

Every dispatch attempt gets a row in `~/.askrubberduck/dispatches.tsv`, and `$DISPATCH` writes it:
`pending` before the seat launches, finalized when the seat exits with minutes, verdict and outage.
A row left `pending` is an interrupted run. `$LEDGER schema` prints the columns and their domains;
a plan critic's `PLAN: CONCUR | OBJECT` is recorded as verdict `CONCUR | OBJECT`.
