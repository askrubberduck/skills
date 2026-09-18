---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Implement W-03 from this backlog. Reply with the updated script.

| ID | Title | State |
|---|---|---|
| W-02 | Rename `report.py` to `summary.py` | open |
| W-03 | Add a `--json` flag to `report.py` that prints the counts as JSON | open |

`report.py`:

```python
import argparse
from collections import Counter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("words", nargs="+")
    args = parser.parse_args()
    counts = Counter(args.words)
    for word, n in counts.most_common():
        print(f"{word}\t{n}")


if __name__ == "__main__":
    main()
```
