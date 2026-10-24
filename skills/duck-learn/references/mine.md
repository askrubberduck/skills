# Mining the transcript stores

Read this when counting owner prompts. Both stores are JSON lines, one event per row, mixing the
owner's words with text the host injected. Count the first; the second is tool evidence.

**Claude**, `~/.claude/projects/<dir>/<session>.jsonl`. An owner prompt is a row with
`type == "user"` whose `message.content` is a string, or a list holding `text` parts. A list of
`tool_result` parts is a tool answer. `isMeta` rows are loaded skill bodies; `isCompactSummary`
rows are the host's summary. A slash command arrives as `<command-name>` and `<command-args>` and
is the owner's directive: keep both. A row opening "Another Claude session sent a message" is a
subagent reporting back. Delegated logs sit in `<session>/subagents/`, so a one-level glob reports
roots only.

**Codex**, `$CODEX_HOME/sessions/**` and `archived_sessions/**`: every project on the host, so
counts may span projects; say which workspaces each came from. An owner prompt is a row whose
`payload` has `type == "message"` and `role == "user"`, its words in `content[].text`. The first
row, `session_meta`, says whose session it is: `originator` `codex_exec` is a non-interactive
dispatch, and a spawned agent carries `parent_thread_id`; count neither. An SDK originator may be
an app the owner types into or an automated dispatch: count it only with positive evidence of
interactive input, otherwise report it as unknown, and name the originators you counted. A fork
names its parent in `forked_from_id` and replays the parent's prompts under new timestamps: drop
that replayed prefix. Never fold by text alone, which also folds every honest repeat of a short
directive.

Strip only wrappers the host is known to inject; a pattern that removes any paired tag also removes
markup an owner pasted.

Write a one-off extractor over the two globs. It folds a fork by walking its prompts beside the
parent's and dropping the matching prefix; keeps a fork whose parent is missing or not older, and
says so; counts each session id once; and prints one `partial:` line per class of thing it skipped
or kept on doubt: an empty or missing store, a malformed row, a prompt without a readable
timestamp, a prompt folded as replay.

Keep the extracted rows in scratch: they hold raw prompt text, and only counts reach durable
output. Every `partial:` line goes into the report, with the limit that the fold drops a fork
prompt retyping the parent's next one, since the store does not mark where replay ends. A store
this page does not describe yields nothing: locate it first, or mark the result partial.
