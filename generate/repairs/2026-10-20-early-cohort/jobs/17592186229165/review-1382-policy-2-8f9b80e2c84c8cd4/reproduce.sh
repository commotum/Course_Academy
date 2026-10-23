#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
review_python=/home/jake/Developer/Course_Academy/.venv/bin/python
review_repo=/home/jake/Developer/Course_Academy
"$review_python" audit.py > audit.log 2>&1
"$review_python" targeted.py > targeted.log 2>&1
"$review_python" package_checks.py > package-checks.log 2>&1
"$review_python" run_delivery.py > delivery-summary.log 2>&1
"$review_python" variation.py > variation.log 2>&1
"$review_python" review_history.py
"$review_python" "$review_repo/generate/pipeline/render_preview.py" --input render-records.json --output render --limit 6 --asset-root "$PWD" > render.log 2>&1
"$review_python" "$review_repo/generate/pipeline/render_preview.py" --input render-rest-records.json --output render-rest --limit 20 --asset-root "$PWD" > render-rest.log 2>&1
python3 finalize_review.py
