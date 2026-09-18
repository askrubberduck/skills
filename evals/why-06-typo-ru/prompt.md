---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
Сборка в CI падает на шаге миграций, локально всё работает. Почему?

```
$ python manage.py migrate
Traceback (most recent call last):
  File "manage.py", line 9, in <module>
    from app.settings import DB
  File "/app/app/settings.py", line 21, in <module>
    DB = _db()
  File "/app/app/settings.py", line 16, in _db
    url = os.environ["DATABSE_URL"]
KeyError: 'DATABSE_URL'
```

`app/settings.py`:

```python
import os, sys, json  # noqa

DEBUG = os.environ.get("DEBUG", "0") == "1"
_tmp = {}


def _env(name, default=None):
    return os.environ.get(name, default)


def _db():
    # TODO: вынести в отдельный модуль
    if DEBUG:
        return {"url": "sqlite:///dev.db"}
    url = os.environ["DATABSE_URL"]
    return {"url": url, "pool": int(_env("DB_POOL", "5"))}


DB = _db()
```

`.ci/env`:

```
DATABASE_URL=postgres://ci:ci@db:5432/app
DB_POOL=5
```

Локально у меня в `.env` стоит `DEBUG=1`.
