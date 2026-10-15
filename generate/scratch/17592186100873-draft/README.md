# Selected matrix-product entry draft

Only owned draft files were changed; the registered numeric script/tree/caches
are protected by registered-before.json and rechecked in validate.py. No EDB
writes, registration, engine edits or shared changes. Stop after generator step7.

Run from repo root:

```
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186100873-draft/validate.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python generate/scratch/17592186100873-draft/render.py
.venv/bin/python -B generate/scratch/17592186100873-draft.py --difficulty all --count 2 --format markdown
```

Browser rendering needs loopback permission; it uses local installed Chromium
and actual player routines/assets. Native private grader is copied from the
current59716 draft and42 actual source/dependency hashes are verified before/after.
Old shared grader is not used to establish results. Native scalar equivalents
and all displayed radio choices are tested separately from mathematical QA.
Wrong matrix-shaped blank submissions trigger36 documented unsupported-notation
errors; they are not accepted or counted as ordinary wrong-answer rejections.
Raw two missing-key sources cannot be graded and remain ineligible evidence;
normal inferred variants are complete and grade normally. No valid scalar-answer
native failures are hidden. Moderate/Hard bounds are authored scope claims.
