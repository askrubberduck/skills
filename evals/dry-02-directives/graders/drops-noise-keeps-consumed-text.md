---
type: llm
focus: last_message
weight: 1
---
You are shown only the answer, so here is the ORIGINAL file the user supplied, for comparison:

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

Judge only the code block the answer returns; the answer may quote deleted comments in its explanation, and that is fine. PASS only if all hold for that returned `urls.py` code block:
- The narration comments are gone: "This is the default URL that we use", "Split the url", "Return the netloc", "Get the port, or the default...".
- The copyright and SPDX license lines are still present, unchanged.
- `# noqa: E501` and `# type: ignore[arg-type]` are still present on their original lines.
- The doctest in `host` (the `>>>` line and its expected output) is still present, unchanged.
- The fact that `urlsplit` raises ValueError on out-of-range ports is still present as a comment.
- The imports, the `DEFAULT` assignment and the bodies of `host` and `port` look intact (same statements as a normal URL-helper module; you do not need the original to check this).
FAIL otherwise.
