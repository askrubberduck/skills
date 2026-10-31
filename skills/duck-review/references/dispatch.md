# Independent dispatch

Read this only when dispatching a participant. Prefer a native isolated agent or supported API when
it supplies the required model identity, tools and authority; a CLI is one transport, not the test
of independence.

Confirm existing authorization covers sending this repository to the named vendor; record its
source and reuse it without asking again. A permission rejection is not an outage and must not be
retried through another route. Without authority, return the missing requirement to the caller.

Record the doer's runtime family and each participant's pinned model id and family from provider or
harness metadata; executable names and the model's self-description are not identity evidence, and
unknown stays unknown. For an unfamiliar CLI, confirm the model pin is honored (an invalid model
must fail rather than select a default); do not repeat a proven probe unless the harness changed.

Give independent participants separate scratch directories and initial context. Share the same
criteria and source snapshot; participants never read each other's draft conclusions. `$SP` is an
absolute directory under the host's sanctioned scratch root. Preserve essential evidence in the
work record before disposing of scratch output.

The brief states the language to answer in — the user's, unless they asked otherwise — and that
verdicts, rankings, paths and quoted errors stay verbatim. It says the participant is one
perspective and dispatches no reviewers of its own. Each criterion taken from a repository rule is
a verbatim quote with its path and line; the task's own requirements and any explicit owner
requirement travel with their recorded source, including applicable earlier instructions. Include
governing rules and deployment facts with their sources, distinguishing documented facts from
assumptions; do not withhold a governing fact as an owner preference. Keep the doer's hypotheses
and unwritten owner preferences or precedents out of the initial brief; the adjudicator checks them
separately. Agreement on a premise the brief supplied is not independent evidence for it.

Capture a code candidate from its fork point: `git diff $(git merge-base <base> <candidate>)
<candidate>`, and record both SHAs in the brief; a moved base otherwise shows up reversed in the
diff. For a dirty worktree, load [`duck-split`](../../duck-split/SKILL.md) and follow its git
capture rules first: include staged, unstaged and relevant untracked work, inventory ignored files,
and preserve the user's checkout while constructing the snapshot in isolation; the captured ref is
the candidate.

A brief for round two or later carries the prior adjudication and the settled causes by stable ID,
with the instruction not to re-report them in any rewording and to refute one only with new
evidence. A settled cause re-raised without new evidence is dismissed; the rest of that result
still counts.

## Run the reviewers

Run each seat with `python3 "$DISPATCH"` (`$DISPATCH` is the absolute path of `duck-review`'s
`scripts/dispatch.py`, whatever the working directory) in the background; its `--help` lists the
flags, so run that rather than reading the script. Take the seat's exit from the host's completion
notice. Where none reaches you — a subagent, or a `claude -p` turn whose end kills a background
seat (`error: interrupted`) — wait on the exit in one bounded call: a condition monitor, or an
until-loop inside the tool's time limit, repeated as needed. Never `sleep` and then read the output
file; Claude Code refuses that call.
The pinned ids come from `~/.askrubberduck/config.toml`, never from memory (a `[repo."<origin>"]`
table there overrides any key for that origin): `[models].review` (a review or a disposition),
`[models].race` and `[models].plan`, each defaulting to `[families].reviewers` (default empty: the
owner's setup names them).

```bash
python3 "$DISPATCH" --gate "$GATE" --round "$N" --stage review --setup independent --trust 0 --pin "$MODEL" \
  --prompt "$SP/codex/prompt.md" --out "$SP/codex/r$N.out" --add-dir "$SP/material" \
  --candidate "$CHECKOUT"
```

The script picks `codex exec`, `agy` or `claude -p` by the pin's family, runs from the `--out`
file's directory — the seat's own scratch directory, never the target checkout, unless `--workdir`
names a worktree the seat is meant to change (codex `-C`; refused for agy and Claude) — closes
stdin, kills the whole process group past `[bounds].dispatch_timeout` (default 45m), and refuses a
round past the caller's bound unless `--extended` carries the owner's words. It exits 0 with a
verdict, 1 on an outage and its cause, 2 when it refused, 3 when the seat changed the
`--candidate` checkout. A race rival adds `--diff-base <sha> --diff-out <path>`: after a verdict
the script writes the `--workdir` diff against that base whole; an outage writes none, and an
empty diff is an outage, since a race rival's answer is a change.

A codex seat runs with a fresh `CODEX_HOME` holding only a link to the owner's `auth.json`: no
AGENTS.md, config, plugins, memories or MCP servers; model and effort come from the pin. A review
seat also gets that directory as `HOME`, which hides `~/.agents/skills`; a `--workdir` rival keeps
`HOME`, and those skills, so the owner's toolchains still build.

An agy seat runs with a fresh `HOME` holding only links to the owner's Google login
(`~/.gemini/oauth_creds.json`, `~/.gemini/google_accounts.json`) and `~/Library/Keychains`, so
`~/.gemini/config` stays out. Headless agy ends a seat on any permission it would ask for: the
seat's settings run every command in agy's sandbox and allow reading agy's built-in skills and the
`--add-dir` folders. The sandbox has no network and refuses a command's reads outside the
workspace and its writes to the `--add-dir` folders, the seat's home and other scratch
directories; it does let a command write directly under `/tmp`. A seat that writes with a tool,
reads a file elsewhere, fetches a web page or asks to run a command outside the sandbox ends with
no answer, so a brief for an agy seat asks for reading, not changing, names its files under an
`--add-dir` folder and names no URL.

**`--prompt` takes a UTF-8 brief file path; the script passes its contents as a CLI argument.**
The brief names the diff, corpus or files by absolute path for the reviewer to open — never paste
that material into the command.

The Anthropic route uses `claude -p` with an exact model pin and optional effort, plan permissions,
read-only file tools and no MCP servers. It excludes user settings, disables customizations with
`--safe-mode`, and disables session persistence (`--no-session-persistence`; exclude these
transcripts when mining owner sessions). Admin-managed settings still apply, including managed
hooks; inspect those before claiming a shell-free seat. The tool route approves no writes or shell
execution. Claude and agy seats cannot take `--workdir` or serve as writable race/rally rivals; use
a supported writable transport. Read-only seats give source evidence for break/proof, not executed
behavioral checks: treat source-only findings as `tier = read` and claim executed evidence only
when the seat supplies observed command output. Selection still excludes the doer's family; an
Anthropic doer cannot use a Claude pin as its different-family seat. The outer runner bounds all
transports and finalizes their ledger rows on timeout or failure.

Sanity-check a new invocation form with the prompt `Reply with exactly: OK`, run as the bare CLI
command outside `$DISPATCH`, which would record that answer as an outage. These traps yield
plausible reviews at exit 0:

- An unpinned invocation can silently use the wrong model family. The script always pins; prove a
  new pin with the identity checks above.
- The prompt must be an **argument**, as the script passes it. agy's `--print "<text>"` can drop
  it, and a prompt on **stdin** is discarded entirely — the reviewer answers with a greeting at
  exit 0. `codex exec` reads a stdin prompt, but appends piped stdin to an argument prompt.
- After a repair, require the reviewer to show it read the new candidate: have it open its result
  with the candidate's revision and one current line quoted from a named changed artifact, and
  compare each round's output with the last: an identical body is an outage, not a verdict.

A zero-byte, greeting-only, timed-out or crashed dispatch is an outage; the script names its
cause. A `capacity` outage (overload, a bare rate limit)
clears in minutes, so the one retry applies. A `credits` or `quota` outage is the account's, and an
immediate retry only adds a row: send that family no further seat until it answers again, say once
that its seats are parked, and resume without the owner's word. Where the owner's procedure offers
waiting against a waiver, that offer comes first. To wait: at a stated reset time, one wakeup then;
otherwise a background probe, the bare CLI with `Reply with exactly: OK` every 15 minutes within a
budget the report names. On `OK`, recheck each parked candidate's SHA and dispatch its seats. A
family with a `credits` or `quota` outage among its last twenty ledger dispatches runs one seat at
a time, so the next one loses a single review, not a batch. A `model rejected` outage is a dead
pin: no retry; report the missing participant, name the config file that holds the pin, and never
substitute another model. **A degraded dispatch is the harder case — full length, well formed, and
wrong.** The exit status cannot tell, so before trusting any result check that its quoted
justifications support its verdict.

Ask participants to open with a labeled result line, `VERDICT: APPROVE | REJECT | NOTE` or
`PLAN: CONCUR | OBJECT`; race and rally answers end with `VERDICT: DIFF`. The script reads only
the answer's first and last non-empty lines. A labeled boundary result inside a quote or fence
counts as an unsupported conflict, so it cannot silently hide a final rejection. Body result labels
and severity headings cannot become results. Two different boundary results are unsupported. Bare
NOTE remains a severity heading, not an overall result; other bare result words conflict with a
labeled boundary result. A plan critic's `PLAN: CONCUR | OBJECT` is recorded as verdict
`CONCUR | OBJECT`.

Two kinds of malformed result: *unranked* — a verdict with findings that carry no severity: the
participant counts, its findings are claims to adjudicate; *unsupported* — no verdict, or a
verdict whose cited justification is the claim under attack: the participant did not answer, the
gate is short a reviewer, and its findings are still claims. **A REJECT is never an outage.**

**A pin on trial rides along.** A pin in `[learn].trial` (default empty) rides along for its first
`[learn].shadow` (default 3) gates, and up to twice that while its comparison stays undecided;
`$LEDGER pick review` names it on a `shadow` line while it does (`$LEDGER` means
`python3 "<absolute path of duck-review's scripts/ledger.py>"`). Dispatch it beside the required
set with the same brief and the same export authorization for its vendor, or skip it and say so.
Its verdict never counts toward the gate, its outage never leaves the gate short, and its findings
are adjudicated like any other. Its row carries `setup = shadow`. A trial's gates count in
whichever repository they ran; its comparison pairs it with its family's reviewer on the same gate
of the same repository.

Every dispatch attempt gets a row in `~/.askrubberduck/dispatches.tsv`, written by `$DISPATCH`:
`pending` before the seat launches, finalized when the seat exits with minutes, verdict and outage.
A watchdog process stops the seat's process group however dispatch ends, by any signal including
SIGKILL, and finalizes a row still `pending` with outage `-` a moment later. SIGTERM, SIGHUP and
SIGINT leave the watchdog running; a row that stays `pending` means SIGKILL ended the watchdog or
the ledger is locked. A seat process that leaves its process group (`setsid`) is beyond the stop.
`$LEDGER schema` prints the columns and their domains.
