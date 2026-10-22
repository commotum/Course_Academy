# Reproduction and validation commands

All commands ran from the supplied workspace. Python is `/home/jake/Developer/Course_Academy/.venv/bin/python` (3.13.5), SymPy 1.14.0.

Before repair, the review's reproduction script was copied into `checks/original_counterexamples.py` and run with `shortcut --package .` and `source --package .`. Both failed as reported: exact bank [0,2,3,4,5] keyed 2; supplied five-component source rejected. Logs: `before-shortcut.txt`, `before-source.txt`. The copied script now tests the exact old input plus its same-bank counterfactual, and the exact source rejection case. Run:

```
/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/original_counterexamples.py shortcut
/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/original_counterexamples.py source
/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/repair_regressions.py
```

`repair_regressions.py` contains both retained findings and runs shared delivery validation in subprocesses; exact commands and results are in `delivery-easy-command.json`, `delivery-moderate-command.json`, and `delivery-batch-command.json`. It parses public prompts/solutions independently, replays all 15 original complete banks, checks all normal bank cue groups, exercises the old shortcut strategy, compares the identical raw/delivered pool, regenerates the exact five old seeds, validates mathematical rejection, tests deterministic replay and copies only manifest runtime files into `relocated/` for CLI validation. Its source-derived records and checks are saved alongside the compact results.

```
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-report.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence --math-root /media/jake/SSD/EDB/math --limit 8
```

The native grader checks all five alternatives on 18 independently solved records (18 accepted, 72 rejected). UI uses the unmodified application, with five batch members, two repaired five-component source examples and a four-component three-parameter display. The renderer initially used its default limit of six; it was rerun with the explicit limit of eight so both layouts and all requested representatives are covered. Screenshots were visually inspected; results are saved in `visual-inspection.json`.

No database writes, publication, image publication or service calls occurred. Shared tools run read-only; generated evidence and relocation files remain under the workspace.

Additional bounded checks after visual inspection:

```
/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/check_scroll.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B checks/summarize.py
```

`check_scroll.py` reuses the shared renderer and adds only scroll geometry observations on the two long three-vector solutions. `summarize.py` reads saved evidence, records actual UI positions and runtime hashes, and writes `final-validation.json`; it does not regenerate or modify the runtime package.
