---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Why does MAX_ROWS exist, and when was it added? Nothing is failing, I am only deciding whether it still earns its place. You cannot run anything; this is what I pulled.

```
$ git log -S'MAX_ROWS' --oneline -- loader.py
9f3c2aa cap rows, see #12
$ git show 9f3c2aa --stat --format='%h %ad %s' --date=short
9f3c2aa 2023-03-02 cap rows, see #12
 loader.py | 3 +++
```

PR #12, description: "load_all() reads the whole export into a list before writing. Prevents OOM on the 2GB workers. Cap at 100 until we stream."

```
$ git log --oneline -- loader.py
c41d7e0 stream rows to the writer; drop load_all()
9f3c2aa cap rows, see #12
```

loader.py today:

```python
MAX_ROWS = 100

def stream(source, writer):
    for n, row in enumerate(source):
        if n >= MAX_ROWS:
            break
        writer.write(row)
```
