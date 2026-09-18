---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Strip the comment noise from this module and reply with the cleaned file.

`urls.py`:

```python
# Copyright 2024 Example Corp.
# SPDX-License-Identifier: Apache-2.0
"""URL helpers."""
from urllib.parse import urlsplit

# This is the default URL that we use.
DEFAULT = "https://example.invalid/api/v2/resources/really/long/path/that/goes/past/the/line/limit/for/sure"  # noqa: E501


def host(url):
    """Return the host part of a URL.

    >>> host("https://example.invalid/a")
    'example.invalid'
    """
    # Split the url
    parts = urlsplit(url)
    # Return the netloc
    return parts.netloc


def port(url, default):
    # Get the port, or the default if there is no port.
    # urlsplit raises ValueError on out-of-range ports instead of returning None.
    return urlsplit(url).port or int(default)  # type: ignore[arg-type]
```

CI runs the doctests.
