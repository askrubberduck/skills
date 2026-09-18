---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
This test passes on my laptop (I'm in New York) and fails in CI every time. Why?

`buckets.py`:

```python
from datetime import datetime


def bucket(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
```

`tests/test_buckets.py`:

```python
from buckets import bucket


def test_daily_bucket():
    assert bucket(1700008200) == "2023-11-14"
```

CI log excerpt:

```
env: CI=true TZ=UTC PYTHONHASHSEED=0
tests/test_report.py::test_header PASSED
  /app/report.py:14: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version.
tests/test_buckets.py::test_daily_bucket FAILED
    def test_daily_bucket():
>       assert bucket(1700008200) == "2023-11-14"
E       AssertionError: assert '2023-11-15' == '2023-11-14'
```
