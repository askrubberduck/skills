---
type: llm
focus: last_message
weight: 1
---
You are shown only the answer, so here is what the user supplied:

`shop/pricing.py`:

```python
def apply_discount(total, code):
    if code == "WELCOME10":
        return round(total * 0.9, 2)
    return total
```

`tests/test_pricing.py`:

```python
import shop.pricing
from shop.pricing import apply_discount


def test_apply_discount_is_called(mocker):
    mocked = mocker.patch("shop.pricing.apply_discount", return_value=90.0)
    assert shop.pricing.apply_discount(100, "WELCOME10") == 90.0
    mocked.assert_called_once_with(100, "WELCOME10")


def test_welcome_code_takes_ten_percent():
    assert apply_discount(100, "WELCOME10") == 90.0


def test_unknown_code_changes_nothing():
    assert apply_discount(100, "NOPE") == 100
```

`test_apply_discount_is_called` patches the very function it then calls, so it asserts only that the mock returns what the mock was told to return; it passes even if `apply_discount` is broken. The other two tests check real outcomes (the discount branch and the no-discount branch).

PASS only if all hold:
- The mock-based test is removed (or identified as the one to remove), with the reason that it tests the mock, not the function.
- Both outcome tests are kept, or their two behaviours remain covered (e.g. one parametrized test covering the WELCOME10 case and the unknown-code case).
- The answer does not change `apply_discount` itself.
FAIL if either real behaviour loses coverage, if the mock test is kept, or if the answer deletes tests just to reduce the count without saying why that one.
