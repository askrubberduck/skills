---
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Simplify this deeply. Reply with the file.

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

Contracts that must survive: `dispatch(event)` is the only public entry point and keeps its signature; an unknown `event["type"]` raises `UnknownEvent` carrying the type name; `dispatch` returns whatever the handler returns. Nothing outside this file imports `Handler`, `HandlerFactory`, `UserCreated` or `UserDeleted`. `send_welcome` and `purge` are defined elsewhere in the module.
