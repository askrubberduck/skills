# Mining the transcript stores

Read this when counting owner prompts. Both stores are JSON lines, one event per row, and both mix
the owner's words with text the host injected. Count the first; the second is tool evidence.

**Claude**, `~/.claude/projects/<dir>/<session>.jsonl`. An owner prompt is a row with
`type == "user"` whose `message.content` is a string, or a list holding `text` parts. A list of
`tool_result` parts is a tool answer. `isMeta` rows are loaded skill bodies; `isCompactSummary`
rows are the host's own summary. A slash command arrives as `<command-name>` and `<command-args>`
and is the owner's directive: keep both. A row that opens "Another Claude session sent a message"
is a subagent reporting back. Delegated logs sit apart, in `<session>/subagents/`, so a
one-level glob already reports roots only.

**Codex**, `$CODEX_HOME/sessions/**` and `archived_sessions/**`: every project on the host, where
the Claude path names one. Counts may span projects; say which workspaces each came from. An owner
prompt is a row whose `payload` has `type == "message"` and `role == "user"`, its words in
`content[].text`. The first row, `session_meta`, says whose session it is: `originator`
`codex_exec` is a non-interactive dispatch, and a spawned agent carries `parent_thread_id`. Count
neither; a store full of reviewer briefs otherwise reads as an owner who types briefs. An SDK originator can be an app the owner types into, so it is
counted: name the originators you counted. A fork names its parent in `forked_from_id` and
replays the parent's prompts under new timestamps: drop that replayed prefix. Never fold by text
alone, which also folds every honest repeat of a short directive.

Strip only wrappers the host is known to inject. A pattern that removes any paired tag also
removes the markup an owner pasted.

A one-off extractor is a few lines over two globs. Whatever it looks like, it folds a fork by
walking its prompts beside the parent's and dropping the matching prefix; it keeps a fork whose
parent is missing, or not older than it, and says so; it counts each session id once; and it prints
one `partial:` line per class of thing it skipped or kept on doubt: a store that is empty or
missing, a malformed row, a prompt without a readable timestamp, a prompt folded as replay.

Keep the extracted rows in scratch: they hold raw prompt text, and only counts reach durable
output. Every `partial:` line goes into the report. The store does not mark where a fork's replay
ends, so an owner who retypes the parent's next prompt in the fork loses that one to the fold. A
store this page does not describe yields nothing: locate it first, or mark the result partial.
