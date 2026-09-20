# Mining the transcript stores

Read this when counting owner prompts. Both stores are JSON lines, one event per row, and both mix
the owner's words with text the host injected. Count the first; the second is tool evidence.

**Claude**, `~/.claude/projects/<dir>/<session>.jsonl`. An owner prompt is a row with
`type == "user"` whose `message.content` is a string, or a list holding `text` parts. A list of
`tool_result` parts is a tool answer. `isMeta` rows are loaded skill bodies; `isCompactSummary`
rows are the host's own summary. A slash command arrives as `<command-name>` and `<command-args>`
and is the owner's directive: keep both. Delegated logs sit apart, in `<session>/subagents/`, so a
one-level glob already reports roots only.

**Codex**, `$CODEX_HOME/sessions/**` and `archived_sessions/**`. The first row, `session_meta`,
says whose session it is: `originator` `codex_exec` is a non-interactive dispatch, and a spawned
agent carries `parent_thread_id`. Count neither; a store full of reviewer briefs otherwise reads
as an owner who types briefs. An SDK originator can be an app the owner types into, so it is
counted: name the originators you counted. A fork names its parent in `forked_from_id` and
replays the parent's prompts under new timestamps: drop that replayed prefix. Never fold by text
alone, which also folds every honest repeat of a short directive.

Strip only wrappers the host is known to inject. A pattern that removes any paired tag also
removes the markup an owner pasted.

```python
import collections, glob, json, os, re, sys

SINCE = sys.argv[1] if len(sys.argv) > 1 else ""  # ISO date; row timestamps compare as strings
CLAUDE = os.path.expanduser(os.environ.get("CLAUDE_STORE", "~/.claude/projects"))
CODEX = os.path.expanduser(os.environ.get("CODEX_HOME", "~/.codex"))
INJECTED = ("system-reminder|task-notification|command-message|local-command-stdout|bash-input|"
            "bash-stdout|bash-stderr|ide_opened_file|ide_selection|teammate-message|"
            "environment_context|user_instructions|permissions_instructions|skills_instructions|"
            "collaboration_mode|turn_aborted")
WRAPPER = re.compile(rf"<({INJECTED})\b[^>]*>.*?</\1>", re.S)
COMMAND = re.compile(r"</?command-(?:name|args)>")

def text_of(content):
    if isinstance(content, str):
        return content
    parts = content if isinstance(content, list) else []
    return " ".join(p.get("text", "") for p in parts
                    if isinstance(p, dict) and p.get("type", "text").endswith("text"))

def clean(text):
    return " ".join(COMMAND.sub(" ", WRAPPER.sub("", text)).split())

def rows(path):
    for line in open(path, errors="ignore"):
        try:
            yield json.loads(line)
        except ValueError:
            pass  # a truncated last row is normal in a live session

def sessions():
    for path in glob.glob(CLAUDE + "/*/*.jsonl"):
        yield "claude", path.split("/")[-2], None, None, [
            (r.get("timestamp"), clean(text_of(r.get("message", {}).get("content"))))
            for r in rows(path)
            if r.get("type") == "user" and not r.get("isMeta") and not r.get("isCompactSummary")]
    for path in sorted(glob.glob(CODEX + "/sessions/**/*.jsonl", recursive=True) +
                       glob.glob(CODEX + "/archived_sessions/**/*.jsonl", recursive=True)):
        meta, found = {}, []
        for r in rows(path):
            payload = r.get("payload") if isinstance(r.get("payload"), dict) else r
            if r.get("type") == "session_meta":
                meta = payload
            elif payload.get("type") == "message" and payload.get("role") == "user":
                found.append((r.get("timestamp"), clean(text_of(payload.get("content")))))
        if not meta:
            skipped["codex session without session_meta"] += 1
        elif meta.get("originator") != "codex_exec" and not meta.get("parent_thread_id"):
            yield "codex", meta.get("cwd"), meta.get("id"), meta.get("forked_from_id"), found

skipped = collections.Counter()
found_in = [(host, workspace, session, parent, [(ts, text) for ts, text in found if text])
            for host, workspace, session, parent, found in sessions()]
texts = {session: [text for _, text in found] for _, _, session, _, found in found_in if session}
for host, workspace, session, parent, found in found_in:
    if parent and parent not in texts:
        skipped["fork whose parent is missing, replay kept"] += 1
    replayed = 0
    for (_, mine), theirs in zip(found, texts.get(parent, []) if parent else []):
        if mine != theirs:
            break
        replayed += 1
    for n, (ts, text) in enumerate(found[replayed:], replayed):
        if not ts:
            skipped["prompt without timestamp, kept"] += 1
        if not ts or ts >= SINCE:
            print(json.dumps({"host": host, "workspace": workspace, "ts": ts,
                              "first": n == 0, "text": text[:1500]}))
for reason, count in skipped.items():
    print(f"partial: {count} {reason}", file=sys.stderr)
```

Run it with a since-date and redirect the rows to scratch; count and classify from that file. The
rows hold raw prompt text, so they stay in scratch and only counts reach durable output. Every
`partial:` line on stderr goes into the report. A store this
script does not know yields nothing: locate it first, or mark the result partial.
