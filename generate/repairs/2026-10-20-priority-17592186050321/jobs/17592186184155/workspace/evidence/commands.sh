#!/usr/bin/env bash
# Run from the supplied workspace. All outputs stay below it; no publication/database operations.
set -euo pipefail
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
SOURCE=/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-priority-17592186050321/jobs/17592186184155/source
"$PY" validate.py
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/test-records.json --source "$SOURCE/source.json" --inventory "$SOURCE/inventory.json" --difficulty hard --output evidence/delivery --math-root /media/jake/SSD/EDB/math
"$PY" validate.py --after-delivery evidence/delivery/accepted.json
"$REPO/generate/runs/current/check-engine" evidence/grader-input.json evidence/native-grading.json
"$PY" generator.py --difficulty hard --count 5 --seed 20261020 --format json > evidence/runner-batch.json
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/runner-batch.json --source "$SOURCE/source.json" --inventory "$SOURCE/inventory.json" --difficulty hard --output evidence/runner-delivery --math-root /media/jake/SSD/EDB/math
python3 "$REPO/generate/pipeline/render_preview.py" --input evidence/render-records.json --output evidence/render --asset-root evidence --math-root /media/jake/SSD/EDB/math
"$PY" relocation_check.py
"$PY" finalize_evidence.py
# Inspect evidence/render/question-001.png through question-005.png visually; record observations in visual-inspection.json.
