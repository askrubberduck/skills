---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Explain how our users list API worked in version 1 compared with version 2. Nothing is failing; I only want a historical explanation for the onboarding doc.

v1:

```
GET /v1/users?page=2&per_page=50
200 OK
X-Total-Count: 1240
[{"id": 51, "name": "..."}, ...]
```

v2:

```
GET /v2/users?limit=50&cursor=eyJpZCI6NTB9
200 OK
{"data": [{"id": 51, "name": "..."}, ...], "next_cursor": "eyJpZCI6MTAwfQ"}
```
