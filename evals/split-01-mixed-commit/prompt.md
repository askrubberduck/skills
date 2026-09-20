---
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill]
runs: 3
---
What in this branch doesn't belong to the task? The PR says "Add retry to fetch()". You cannot run anything; here is the branch against its fork point.

```
$ git log --oneline main..HEAD
c3 retry test
c2 typo
c1 add retry
```

c1:
```diff
--- a/fetch.py
+++ b/fetch.py
@@
 def fetch():
-    return get()
+    for _ in range(3):
+        try:
+            return get()
+        except IOError:
+            pass
```

c2:
```diff
--- a/README.md
+++ b/README.md
@@
-Teh readme
+The readme
```

c3:
```diff
--- /dev/null
+++ b/test_fetch.py
@@
+from fetch import fetch
+
+def test_retry():
+    assert fetch
--- a/log.py
+++ b/log.py
@@
 def log(m):
-    print(m)
+    print("[x]", m)
```
