---
type: llm
focus: last_message
weight: 1
---
PASS only if all hold:
- It identifies the cause as the misspelled variable name `DATABSE_URL` in `app/settings.py` (the CI environment defines `DATABASE_URL`), so the lookup raises KeyError.
- It explains why it works locally: `DEBUG=1` returns the sqlite config before the misspelled lookup is reached.
- The repair it names is correcting that one name. It does NOT recommend, as part of the needed fix, refactoring the settings module, introducing a config library, splitting modules, or other structural changes. A single brief optional aside is tolerated; a list of cleanup recommendations is a FAIL.
FAIL otherwise.
