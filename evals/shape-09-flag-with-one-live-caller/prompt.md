---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
This export module has modes nobody uses. Simplify it and reply with the file.

`export.py`:

```python
import csv
import io
import json
from xml.sax.saxutils import escape


def export(rows, mode="csv"):
    if mode == "csv":
        return _delimited(rows, ",")
    if mode == "tsv":
        return _delimited(rows, "\t")
    if mode == "xml":
        return _xml(rows)
    if mode == "json":
        return json.dumps(rows)
    raise ValueError(f"unknown export mode: {mode}")


def _delimited(rows, delimiter):
    out = io.StringIO()
    writer = csv.writer(out, delimiter=delimiter)
    writer.writerows(rows)
    return out.getvalue()


def _xml(rows):
    parts = ["<rows>"]
    for row in rows:
        cells = "".join(f"<c>{escape(str(cell))}</c>" for cell in row)
        parts.append(f"<r>{cells}</r>")
    parts.append("</rows>")
    return "".join(parts)
```

Every call site in the repo (`grep -rn "export("`):

```
report.py:41:        body = export(rows)
partner_feed.py:18:    payload = export(rows, mode="tsv")
```

The module is internal; nothing outside this repo imports it.
