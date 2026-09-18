---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Don't edit anything and don't write code. Just tell me which of these two designs carries less, and why.

We send one kind of notification: a welcome email and a password-reset email, from two call sites. There is no SMS or push on the roadmap.

Design A: an abstract `Notifier` base class, an `EmailNotifier` subclass, a `NotifierRegistry` that loads notifier plugins by name from `notifiers.yaml`, and a `NotificationService` facade the two call sites use. Rationale given: "so we can add SMS later without touching callers."

Design B: one function `send_email(user, template, context)` in `mail.py`, called directly from the two call sites.
