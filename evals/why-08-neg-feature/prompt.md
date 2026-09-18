---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Add a `--verbose` flag to this script that prints each file name as it is counted. Just show me the updated script.

```python
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    args = parser.parse_args()
    total = 0
    for path in Path(args.root).rglob("*.py"):
        total += 1
    print(total)


if __name__ == "__main__":
    main()
```
