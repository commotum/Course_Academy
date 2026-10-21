#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
review_python=/home/jake/Developer/Course_Academy/.venv/bin/python
review_repo=/home/jake/Developer/Course_Academy
review_job=$(dirname "$PWD")
"$review_python" audit.py > audit-run.log 2>&1
python3 - <<'PY'
import json
rows=json.load(open('samples.json'))
json.dump([r for r in rows if r['question'][':question/difficulty'].endswith('/easy')],open('easy-samples.json','w'),indent=2)
PY
"$review_python" "$review_repo/generate/pipeline/check_delivery.py" --input easy-samples.json --source "$review_job/source/source.json" --inventory "$review_job/source/inventory.json" --difficulty easy --output delivery-samples --math-root /media/jake/SSD/EDB/math > delivery-samples.log 2>&1
"$review_python" "$review_repo/generate/pipeline/check_delivery.py" --input runner-batch.json --source "$review_job/source/source.json" --inventory "$review_job/source/inventory.json" --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math > delivery-batch.log 2>&1
"$review_repo/generate/runs/current/check-engine" grader-input.json grader-report.json > grader-run.log 2>&1
"$review_python" "$review_repo/generate/pipeline/render_preview.py" --input render-input.json --output render --limit 6 --math-root /media/jake/SSD/EDB/math > renderer-run.log 2>&1
"$review_python" pipeline_audit.py > pipeline-run.log 2>&1
# This command is expected to fail until the demonstrated bank rule is repaired.
"$review_python" reproduce_failures.py > minimal-failure-run.log 2>&1
