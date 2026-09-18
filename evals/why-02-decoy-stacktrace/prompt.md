---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Our ingest worker blows up inside the JSON parser on some messages. Is the json module choking on something? Why is this failing?

```
Traceback (most recent call last):
  File "worker.py", line 31, in <module>
    handle(queue)
  File "ingest.py", line 17, in handle
    event = load_event(base64.b64decode(body))
  File "ingest.py", line 12, in load_event
    return json.loads(payload)
  File "/usr/lib/python3.12/json/__init__.py", line 341, in loads
    s = s.decode(detect_encoding(s), 'surrogatepass')
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
```

`ingest.py`:

```python
import base64
import json


def fetch(queue):
    """Pop one message and return its JSON body as bytes."""
    raw = queue.pop()
    return base64.b64decode(raw)


def load_event(payload):
    return json.loads(payload)


def handle(queue):
    body = fetch(queue)
    event = load_event(base64.b64decode(body))
    return event["id"]


def replay(path):
    with open(path, "rb") as fh:
        return load_event(fh.read())["id"]
```

Messages on the queue are base64-encoded JSON. `replay` works fine on the same events dumped to disk.
