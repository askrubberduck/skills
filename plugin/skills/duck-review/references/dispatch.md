# Independent dispatch

Read this file only when you dispatch a participant. Prefer a native isolated agent or supported API
when it supplies the required model identity, tools and authority. A CLI is one transport, not the
test of independence.

Confirm existing authorization covers sending this repository to the named vendor. Record its source
and reuse it without asking again. A permission rejection is not an outage; never retry it through
another route. Without authority, return the missing requirement to the caller.

Record the doer's runtime family and each participant's pinned model id and family from provider or
harness metadata. Executable names and the model's self-description are not identity evidence;
unknown stays unknown. For an unfamiliar CLI, confirm it honors the pin: an invalid model must fail,
not select a default. Do not repeat a proven probe unless the harness changed.

Give each independent participant its own scratch directory and initial context, with the same
criteria and source snapshot. Participants never read each other's draft conclusions. `$SP` is an
absolute directory under the host's sanctioned scratch root. Before you delete scratch output, keep
its essential evidence in the work record.

The brief must state:

- the answer language: the user's, unless they asked otherwise;
- that verdicts, rankings, paths and quoted errors stay verbatim;
- that the participant is one perspective and dispatches no reviewers of its own.

Quote each criterion from a repository rule verbatim, with its path and line. The task's
requirements and explicit owner requirements carry their recorded source, including applicable
earlier instructions. Include governing rules and deployment facts with their sources, and mark
facts as documented or assumed. Do not withhold a governing fact as an owner preference. Keep the
doer's hypotheses and unwritten owner preferences or precedents out of the initial brief; the
adjudicator checks them separately. Agreement on a premise the brief supplied is not independent
evidence for it.

Capture a code candidate from its fork point:
`git diff $(git merge-base <base> <candidate>) <candidate>`, and record both SHAs in the brief.
Otherwise a moved base shows reversed. For a dirty worktree, first load
[`duck-split`](../../duck-split/SKILL.md) and follow its git capture rules:

- include staged, unstaged and relevant untracked work;
- inventory ignored files;
- keep the user's checkout unchanged and build the snapshot in isolation.

The captured ref is the candidate.

A brief for round two or later carries the prior adjudication and the settled causes by stable ID.
It tells the participant not to re-report them in any wording and to refute one only with new
evidence. Dismiss a settled cause raised again without new evidence; the rest of that result still
counts.

## Run the reviewers

Run each seat in the background with `python3 "$DISPATCH"`. `$DISPATCH` is an absolute path,
whatever the working directory. Take the first one that exists:

1. `[dispatch].script` in `~/.askrubberduck/config.toml`.
2. `../../../scripts/dispatch.py`, resolved from the real path of `duck-review`'s directory, after
   symlinks. A GitHub install or a linked clone has it.

If neither exists, no seat runs. Report each missing participant and name both sources. The script's
`--help` lists the flags; run it instead of reading the script. Get the seat's exit from the host's
completion notice. If no notice reaches you, wait on the exit in one bounded call, repeated as
needed. This happens in a subagent or a `claude -p` turn whose end kills a background seat
(`error: interrupted`). Use a condition monitor, or an until-loop inside the tool's time limit.
Never `sleep`, then read the output file; Claude Code refuses that call.

Take the pinned ids from `~/.askrubberduck/config.toml`, never from memory; a `[repo."<origin>"]`
table there overrides any key for that origin. The keys are `[models].review` (a review or a
disposition), `[models].race` and `[models].plan`. Each defaults to `[families].reviewers`
(default empty: the owner's setup names them).

```bash
python3 "$DISPATCH" --gate "$GATE" --round "$N" --stage review --setup independent --trust 0 --pin "$MODEL" \
  --prompt "$SP/codex/prompt.md" --out "$SP/codex/r$N.out" --add-dir "$SP/material" \
  --candidate "$CHECKOUT"
```

The script:

- picks `codex exec`, `agy` or `claude -p` by the pin's family;
- runs from the `--out` file's directory, the seat's own scratch directory, never the target
  checkout, unless `--workdir` names a worktree the seat is meant to change (codex `-C`; refused for
  agy and Claude);
- closes stdin;
- kills the whole process group after `[bounds].dispatch_timeout` (default 45m);
- refuses a round past the caller's bound unless `--extended` carries the owner's words.

It exits 0 with a verdict, 1 on an outage with its cause, 2 when it refused, and 3 when the seat
changed the `--candidate` checkout. A race rival adds `--diff-base <sha> --diff-out <path>`: after a
verdict, the script writes the whole `--workdir` diff against that base. An outage writes no diff,
and an empty diff is an outage, because a race rival's answer is a change.

A codex seat runs with a fresh `CODEX_HOME` that holds only a link to the owner's `auth.json`: no
AGENTS.md, config, plugins, memories or MCP servers. The pin sets the model and effort. A review
seat also gets that directory as `HOME`, which hides `~/.agents/skills`. A `--workdir` rival keeps
`HOME` and those skills, so the owner's toolchains still build.

An agy seat runs with a fresh `HOME` that holds only links to the owner's Google login
(`~/.gemini/oauth_creds.json`, `~/.gemini/google_accounts.json`) and `~/Library/Keychains`, so
`~/.gemini/config` stays out. Headless agy ends a seat on any permission request. The seat's
settings run every command in agy's sandbox and allow reads of:

- agy's built-in skills;
- the logs of the seat's own commands under its home's `.gemini/antigravity-cli/brain`;
- the `--add-dir` folders.

The sandbox has no network. It refuses a command's reads outside the workspace, and writes to the
`--add-dir` folders, the seat's home and other scratch directories. It lets a command write directly
under `/tmp`. A seat ends with no answer if it writes with a tool, reads elsewhere, fetches a web
page or asks to run outside the sandbox. An agy brief must ask for reading, not changing. It names
its files under an `--add-dir` folder and names no URL. A seat that checks a claim tries the
project's tests, finds no dependencies or sockets, and asks to run outside the sandbox. The script
puts those limits and the readable folders before every agy brief, whatever it says.

**`--prompt` takes a UTF-8 brief file path; the script passes its contents as a CLI argument.** The
brief names the diff, corpus or files by absolute path for the reviewer to open; never paste that
material into the command.

The Anthropic route uses `claude -p` with an exact model pin and optional effort, plan permissions,
read-only file tools and no MCP servers. It excludes user settings, disables customizations with
`--safe-mode`, and disables session persistence (`--no-session-persistence`). Exclude these
transcripts when you mine owner sessions. Admin-managed settings still apply, including managed
hooks; inspect them before you claim a shell-free seat. The tool route approves no writes or shell
execution. Claude and agy seats cannot serve as writable race or rally rivals; use a supported
writable transport. Read-only seats give source evidence for break and proof, not executed
behavioral checks. Treat source-only findings as `tier = read`. Claim executed evidence only when
the seat supplies observed command output. The required different-family seat excludes the doer's
family: an Anthropic doer cannot use a Claude pin for that seat. The outer runner bounds all
transports and finalizes their ledger rows on timeout or failure.

Sanity-check a new invocation form with the prompt `Reply with exactly: OK` through the bare CLI,
not `$DISPATCH`, which records that answer as an outage. These traps give plausible reviews at exit
0:

- An unpinned invocation can silently use the wrong model family. The script always pins; prove a
  new pin with the identity checks above.
- The prompt must be an **argument**, as the script passes it. agy's `--print "<text>"` can drop it.
  A prompt on **stdin** is discarded; the reviewer answers with a greeting at exit 0. `codex exec`
  reads a stdin prompt, but appends piped stdin to an argument prompt.
- After a repair, the reviewer must show it read the new candidate: its result opens with the
  candidate's revision and one current line quoted from a named changed artifact. Compare each
  round's output with the last; an identical body is an outage, not a verdict.

A zero-byte, greeting-only, timed-out or crashed dispatch is an outage. A `capacity` outage
(overload, a bare rate limit) clears in minutes, so the one retry applies. A `credits` or `quota`
outage is the account's, and an immediate retry only adds a row. Send that family no further seat
until it answers again. Say once that its seats are paused. When it answers, resume without the
owner's word. If the owner's procedure offers a wait against a waiver, that offer comes first.

To wait:

- at a stated reset time, set one wakeup then;
- otherwise, run a background probe: the bare CLI with `Reply with exactly: OK` every 15 minutes,
  within a budget the report names.

On `OK`, recheck each paused candidate's SHA and dispatch its seats. A family with a `credits` or
`quota` outage among its last twenty ledger dispatches runs one seat at a time, so the next outage
loses one review, not a batch. A `model rejected` outage is a dead pin: do not retry. Report the
missing participant, name the config file that holds the pin, and never substitute another model.
**A degraded dispatch is the harder case — full length, well formed, and wrong.** The exit status
cannot show it, so before you trust any result, check that its quoted justifications support its
verdict.

Tell participants to open with a labeled result line: `VERDICT: APPROVE | REJECT | NOTE` or
`PLAN: CONCUR | OBJECT`. Race and rally answers end with `VERDICT: DIFF`. The script reads only the
answer's first and last non-empty lines. A labeled boundary result inside a quote or fence counts as
an unsupported conflict, so it cannot silently hide a final rejection. Body result labels and
severity headings cannot become results. Two different boundary results are unsupported. A bare NOTE
stays a severity heading, not an overall result; other bare result words conflict with a labeled
boundary result. The script records a plan critic's `PLAN: CONCUR | OBJECT` as verdict
`CONCUR | OBJECT`.

Two kinds of result are malformed:

- *unranked*: a verdict with findings that carry no severity. The participant counts; its findings
  are claims to adjudicate.
- *unsupported*: no verdict, or a verdict whose cited justification is the claim under attack. The
  participant did not answer and the gate is short a reviewer; its findings are still claims.

**A REJECT is never an outage.**

`$DISPATCH` writes a row in `~/.askrubberduck/dispatches.tsv` for every dispatch attempt: `pending`
before the seat launches, finalized with minutes, verdict and outage when the seat exits. However
dispatch ends, by any signal including SIGKILL, a watchdog process stops the seat's process group. A
moment later, it finalizes a row still `pending` with outage `-`. SIGTERM, SIGHUP and SIGINT leave
the watchdog running. A row that stays `pending` means SIGKILL ended the watchdog or the ledger is
locked. The stop does not reach a seat process that leaves its process group (`setsid`).
The file's first line names the columns.
