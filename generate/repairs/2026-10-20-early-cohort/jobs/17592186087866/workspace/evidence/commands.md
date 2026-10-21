Run from the workspace. `PY` is `/home/jake/Developer/Course_Academy/.venv/bin/python`; `REPO` is `/home/jake/Developer/Course_Academy`; `JOB` is the parent of this workspace. All commands are database-free. No publication command was run.

```bash
export PYTHONDONTWRITEBYTECODE=1
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
JOB="$PWD/.."
"$PY" evidence/validate_repair.py
"$PY" evidence/controlled_bank.py
"$PY" evidence/package_check.py
"$PY" evidence/inventory_check.py
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/easy-records.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty easy --output evidence/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/controlled-easy-records.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty easy --output evidence/delivery-controlled --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/runner-records.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty easy --output evidence/delivery-runner --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$PY" evidence/probes.py
"$PY" evidence/delivery_checks.py
"$REPO/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-results.json
"$REPO/generate/runs/current/check-engine" evidence/controlled-bank-grader-input.json evidence/controlled-bank-grader-results.json
"$REPO/generate/runs/current/check-engine" evidence/delivered-grader-input.json evidence/delivered-grader-results.json
python3 "$REPO/generate/pipeline/render_preview.py" --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math --limit 22
python3 "$REPO/generate/pipeline/render_preview.py" --input evidence/layout-fix-records.json --output evidence/render-layout-fix --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math --limit 2
```

`before-records.json` and `before-delivered.json` preserve the preceding independent review's complete failing inputs. `probes.py` reruns the reported frequency rule on those exact records as well as on the repaired raw and delivered samples. Boundary and source-parameter probes are deliberately concentrated; their option-length rates do not estimate normal sampling. `controlled-bank-results.json` checks five different correct values against each identical unordered answer bank. Position cues are measured separately.

`render-boundaries/` preserves the earlier clipping reproduction, despite its passing DOM report. `render-layout-fix/` is the visually verified correction. The final main render uses the current layout. `refresh_hard_display.py` records the earlier targeted sign-formatting check; the final full validation supersedes that intermediate run.

Final collection after the checks and screenshot inspection:

```bash
"$PY" evidence/final_report.py
```

This checks the saved results and current runtime hashes, then writes `author-results.json`, `pedagogical-variation.json`, and `render-inspection.json`.
