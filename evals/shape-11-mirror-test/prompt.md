---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Three tests for a four-line function is too many. Simplify the tests and reply with the test file.

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
