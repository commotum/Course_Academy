#!/usr/bin/env bash
set -eu
cd -- "$(dirname -- "$0")"
export PYTHONDONTWRITEBYTECODE=1
repo=/home/jake/Developer/Course_Academy
py="$repo/.venv/bin/python"
"$py" focused_review.py > focused-review.log 2>&1
"$py" "$repo/generate/pipeline/check_delivery.py" --input delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-samples --asset-root ../workspace --math-root /media/jake/SSD/EDB/math > delivery-samples.log 2>&1
"$py" "$repo/generate/pipeline/check_delivery.py" --input batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root ../workspace --math-root /media/jake/SSD/EDB/math > delivery-batch.log 2>&1
"$repo/generate/runs/current/check-engine" grader-input.json grader-report.json > grader.log 2>&1
"$py" "$repo/generate/pipeline/render_preview.py" --input render-input.json --output render --limit 10 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math > render.log 2>&1
"$py" finish_review.py > finish-review.log 2>&1
# write_review.py includes the recorded human screenshot inspection.
"$py" write_review.py
