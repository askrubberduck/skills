---
type: llm
focus: last_message
weight: 0.5
---
The user supplied a `stock.py` in which `normalize_sku` had the docstring `"""Return the SKU stripped and uppercased."""` over the one-line body `return sku.strip().upper()`.

Judge the `stock.py` code block the answer returns. PASS only if `normalize_sku` no longer carries that docstring, nor any docstring or comment restating its name or body (that it normalizes, strips or uppercases), and its body `return sku.strip().upper()` is unchanged. FAIL otherwise.
