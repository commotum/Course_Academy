#!/usr/bin/env bash
# Run from the supplied workspace. All outputs stay in ./evidence.
set -eu
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
JOB=/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186161967
# Original finding: exit 1 before repair (36/36), exit 0 after repair (9/36).
"$PY" -B "$JOB/review-0-policy-2-b2ba6e2b0f4d64c5/reproduce_shortcut.py" "$PWD/17592186161967.py"
"$PY" -B check_repair.py
"$PY" -B validate_repair.py
"$REPO/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-report.json
"$PY" -B "$REPO/generate/pipeline/check_delivery.py" --input evidence/delivery-input.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty easy --output evidence/delivery --asset-root evidence --math-root /media/jake/SSD/EDB/math
"$PY" -B check_delivery_repair.py
python3 "$REPO/generate/pipeline/render_preview.py" --input evidence/render-records.json --output evidence/render --asset-root evidence --math-root /media/jake/SSD/EDB/math
"$PY" -B check_package.py
