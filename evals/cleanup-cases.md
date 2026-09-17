# Cleanup, framing and planning trials

Run each candidate/baseline in a fresh isolated session. Supply only the selected skill snapshot,
its referenced resources and the fixture. No source-repository access, external dispatch or commits.
Compare actual artifacts and checks; a successful trial alone does not demonstrate improvement.

## Cleanup without removing validation

Task: use duck-shape to clean up this fixture, apply justified local edits and verify.

`CONTRACT.md`: only `greet` and `farewell` are public. No other callers, dynamic loading or published
packages exist. Both trim nonempty strings and reject other inputs with
`ValueError("name required")`. Preserve output and exception behavior; no new functionality.

`greetings.py`:

```python
def require_name(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("name required")
    return value.strip()


def normalize_name(value):
    return require_name(value)


class GreetingFactory:
    def create(self, name):
        return "Hello, " + name


def greet(value):
    name = normalize_name(value)
    return GreetingFactory().create(name)


def farewell(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("name required")
    return "Bye, " + value.strip()


def unused_preview(value):
    return "Preview: " + str(value)
```

`check.py` (run with `python3 check.py`):

```python
from greetings import greet, farewell
for operation, prefix in ((greet, "Hello, "), (farewell, "Bye, ")):
    assert operation("  Ada  ") == prefix + "Ada"
    for bad in ("", "  ", None, 42):
        try:
            operation(bad)
        except ValueError as error:
            assert str(error) == "name required"
        else:
            raise AssertionError((operation.__name__, bad))
print("greeting contracts passed")
```

Pass: remove unnecessary indirection and dead code, consolidate validation, retain the required
checks and public behavior, and execute verification after the last edit. A helper with two callers
is not itself slop. Do not grade against an exact implementation.

## CSV design and plan without a framework

`report.py`:

```python
import json

def report(rows, output):
    output.write(json.dumps(rows))
```

`CONTRACT.md`: a local one-shot CLI exports a caller-provided list of dictionaries as JSON. Add an
optional CSV choice. JSON remains the default with unchanged behavior. CSV columns are the sorted
union of keys; missing fields are blank; empty input emits nothing. Values are strings. Python stdlib
only; no persistence, plugins, new dependency or remote service. Implementation is not authorized.

Task: use duck-frame to recommend a design, then duck-plan for the implementation plan. Save
`frame.md` and `plan.md`. Local read-only experiments are permitted. Use a solo self-check for this
bounded trial; no independent reviewer dispatch. The supplied fixture has no CLI parser.

Pass: preserve JSON, establish CSV quoting and empty-input behavior with an actual experiment,
reuse stdlib capabilities, specify outcome checks, and leave `report.py` unchanged. Acknowledge the
missing CLI integration without fabricating it. Do not introduce an exporter framework, persistence,
or speculative migration. A READY design must not be represented as a verified implementation.

## Local results, 2026-09-17

Baseline: skills from `039d8170064253c4cdd283ee52bf6fc729ae7747`. Candidate: the uncommitted
shape/frame/plan rewrite accompanying this record. Four fresh native Codex subagents ran the paired
fixtures, without each other's results or an expected answer. The trial host did not expose a pinned
runtime model ID; no cross-family independence or release approval is claimed. Each design trial
applied frame then plan in one session; baseline and candidate were separate sessions.

The coordinator inspected the cleanup artifacts and reran both checks: exit 0,
`greeting contracts passed`. Both produced the same simplified implementation: one shared validator,
`greet`, and `farewell`. Both removed the wrapper, factory, dead preview and duplicate validation.
This fixture shows preserved behavior, not an improvement over the baseline.

Both design/plan trials chose one function extension plus an assertion check, preserved JSON and
left `report.py` unchanged (SHA-256
`07914f52a0cf7451f77927e51124e654ea9dae54c619de7102ccfe6320e644fc`). Both acknowledged the absent
CLI parser and ran successful stdlib CSV feasibility checks. The baseline demonstrated that
first-row header inference loses a later key; the candidate demonstrated that an unconditional
empty DictWriter header emits `"\r\n"`, so the empty-input guard is necessary.

The baseline frame enumerated three options, including an unrequested exporter registry, and
reported an adds/removes inventory. The candidate recommended the direct extension without that
inventory or a registry alternative. Both plans still selected the same minimal implementation.
This is one observed reduction in design ceremony, not evidence of better implementation quality,
reliable slop reduction, or lower runtime cost. No repetitions, held-out user failures, broader
routing trials or high-risk design trials ran.

Candidate core skill SHA-256 values (the trial used these bodies):

- `duck-shape`: `1b1b59b72fe113782496be3c0f648db15cdb7e90e9d5fb09e95c82804809b91c`
- `duck-frame`: `4a155354ab51d32525531496299a1fc613ed3ecaf0b649e7cc1f3f6c9736ef2a`
- `duck-plan`: `7632e978c8e7e0d212a2bea18e54379799e296401369e5fd74ec6ed1bfdfd7fc`

The snapshot preceded the small companion edits to dry's prose bar, why's hypothesis rule and
proof's structural prompts. Those changes were inspected but not behaviorally compared here.
The UI prompts and catalog were updated afterward; these were explicit skill-invocation trials,
not tests of discovery or the UI prompts.

## Wider instruction review

The local review read all 19 skill entrypoints and followed the relevant shape/frame/plan callers.
Changes outside those three were limited to evidenced instruction problems:

- Dry's prose bar inferred a responsibility defect from a docstring list and encouraged extraction.
  It now requires a concrete ambiguity and prefers simpler code before another helper.
- Why required two hypotheses even with decisive direct evidence. It now asks for a competitor
  when uncertainty remains.
- Proof's structural check was abstract. It now uses shape's specific cleanup candidates and asks
  which concrete mechanism or obligation can disappear.

Run and campaign already invoke structural cleanup during implementation; no extra stage was added.
Break, review, race, land and sweep contain operational and authorization safeguards whose removal
was not justified by this review. Other entrypoints received no edits. This was an in-session
instruction review, not behavioral verification of every skill or an independent release gate.

Validation: `python3 scripts/validate-distribution.py --self-test` passed for 19 skills, including
corruption checks. The generic skill-creator `quick_validate.py` could not start because its Python
environment lacks PyYAML; the repository's stdlib distribution validator supplied packaging checks.

A subsequent [workflow pass](workflow-cases.md) revised dry, why, campaign, roast and diet and records
its own baseline comparisons; the scope and results above describe the earlier pass.
