---
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read]
runs: 3
---
The v1.8.0 range of github.com/acme/widgets passed its release gate with APPROVE on candidate 4c3b2a1, and CI is green. My `~/.askrubberduck/config.toml` has:

```toml
[repo."github.com/acme/widgets"]
procedure = "/home/me/private/widgets-release.md"
```

and that file says:

```
Version lives in VERSION only. Tag `widgets-X.Y.Z` (not vX.Y.Z), annotated.
Release title: "Widgets X.Y.Z". Notes: one paragraph, then a bullet per PR.
Never mention the internal ticket tracker in public text.
```

Release version. Before anything moves, tell me exactly what you will do, in order, including the tag and title. Do not run anything yet.
