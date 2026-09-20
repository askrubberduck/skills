---
type: llm
focus: last_message
weight: 1
---
You are shown only the answer, so here is what the user supplied:

`events.py`:

```python
from abc import ABC, abstractmethod


class UnknownEvent(Exception):
    pass


class Handler(ABC):
    @abstractmethod
    def handle(self, event):
        ...


class HandlerFactory:
    _registry = {}

    @classmethod
    def register(cls, name):
        def decorator(handler_cls):
            cls._registry[name] = handler_cls
            return handler_cls
        return decorator

    @classmethod
    def create(cls, name):
        if name not in cls._registry:
            raise UnknownEvent(name)
        return cls._registry[name]()


@HandlerFactory.register("user.created")
class UserCreated(Handler):
    def handle(self, event):
        return send_welcome(event["email"])


@HandlerFactory.register("user.deleted")
class UserDeleted(Handler):
    def handle(self, event):
        return purge(event["id"])


def dispatch(event):
    return HandlerFactory.create(event["type"]).handle(event)
```

Stated contracts: `dispatch(event)` keeps its signature and is the only public entry; an unknown type raises `UnknownEvent` with the type name; `dispatch` returns the handler's result; nothing else imports the classes.

PASS only if all hold:
- The abstract base class, the factory/registry class and the decorator registration are gone, replaced by something plainly smaller — e.g. two functions (or lambdas) and one dict keyed by event type.
- `dispatch(event)` still exists with the same signature and returns the handler's result.
- An unknown event type still raises `UnknownEvent` with the type name (not a bare `KeyError`).
- `"user.created"` still leads to `send_welcome(event["email"])` and `"user.deleted"` to `purge(event["id"])`.
- No new abstraction is introduced in place of the old ones (no Protocol, dataclass registry, plugin loader).
FAIL if any contract is broken, if the class hierarchy survives, or if the answer only trims comments/whitespace.
