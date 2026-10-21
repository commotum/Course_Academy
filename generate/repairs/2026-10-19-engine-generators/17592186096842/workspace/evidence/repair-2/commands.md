# Reproduction

Run from the supplied workspace with `/home/jake/Developer/Course_Academy/.venv/bin/python`.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python repair_validate.py > evidence/repair-2.log 2>&1
/home/jake/Developer/Course_Academy/.venv/bin/python repair_finalize.py > evidence/repair-2/finalize.log 2>&1
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/repair-2/render-records.json --output evidence/repair-2/render --asset-root evidence/repair-2/assets --math-root /media/jake/SSD/EDB/math
```

The validation script saves the exact shared delivery and native harness command arrays in commands.json and individual *-command.json files. It checks all source cases, only a small unrelated regression sample, the concrete review cohort, affected boundaries, controlled roles and evidence changes. It asserts that the required native blocker probes fail; script success therefore does **not** mean grading is fixed.

Required probes, expected to exit 1 until the native grader is fixed:

```sh
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/repair-2/grading-blocker-input.json evidence/repair-2/grading-blocker-report.json
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/repair-2/zero-blocker-input.json evidence/repair-2/zero-blocker-report.json
```

Key-representation diagnostic (observed unresolved outcomes explicitly declared; not a passing required-grading check):

```sh
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/repair-key-probes.json evidence/repair-key-results.json
```

Native commands use the supplied, unchanged application harness. Rendering used the shared actual-UI preview tool; all six resulting PNGs were opened and inspected, as recorded in visual-inspection.md. Existing author-1 scripts/evidence remain available and are not silently overwritten by these new repair results.
