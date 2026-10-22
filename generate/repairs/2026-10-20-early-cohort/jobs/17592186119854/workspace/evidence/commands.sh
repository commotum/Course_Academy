#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
export PYTHONDONTWRITEBYTECODE=1
# Original failure reproduced before edits: exit 1; retained complete records:
# evidence/before-minimal-failing-cases.json. Current equivalent probe exits 0.
"$PY" evidence/reproduce-latest.py
"$PY" regressions.py
"$REPO/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-results.json
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/fresh-moderate.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/delivery-fresh --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$PY" 17592186119854.py --difficulty moderate --count 5 --seed 3719145341 --format json > evidence/batch.json
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/delivery-batch --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$PY" evidence/finish-checks.py
"$REPO/generate/runs/current/check-engine" evidence/batch-grader-input.json evidence/batch-grader-results.json
"$PY" "$REPO/generate/pipeline/render_preview.py" --input evidence/render-input.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
# Inspect the four PNG screenshots; DOM checks alone do not certify layout.
