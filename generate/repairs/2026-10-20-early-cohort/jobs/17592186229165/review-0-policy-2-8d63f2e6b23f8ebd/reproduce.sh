#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
"$PY" audit.py
"$PY" focused_checks.py
"$REPO/generate/runs/current/check-engine" grader-input.json grader-report.json
"$REPO/generate/runs/current/check-engine" grader-exponent-input.json grader-exponent-report.json
"$REPO/generate/runs/current/check-engine" grader-role-input.json grader-role-report.json
"$REPO/generate/runs/current/check-engine" grader-delivered-input.json grader-delivered-report.json
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input runner-batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input independent-easy.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-independent --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input independent-hard.json --source ../source/source.json --inventory ../source/inventory.json --difficulty hard --output delivery-hard --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input generated-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty hard --output delivery-stored --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/render_preview.py" --input render-records.json --output render --limit 6 --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/render_preview.py" --input counterfactual-records.json --output render-pairs --limit 7 --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/render_preview.py" --input render-hard-records.json --output render-hard --limit 2 --math-root /media/jake/SSD/EDB/math
python3 summarize.py
# Strict acceptance test intentionally exits 1 on the reviewed generator:
"$PY" test_role_exchange.py
