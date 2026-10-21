#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
repo=/home/jake/Developer/Course_Academy
job="$repo/generate/repairs/2026-10-20-early-cohort/jobs/17592186059772"
py="$repo/.venv/bin/python"
export PYTHONDONTWRITEBYTECODE=1
"$py" revision_audit.py
"$py" "$repo/generate/pipeline/check_delivery.py" --input easy-samples.json --source "$job/source/source.json" --inventory "$job/source/inventory.json" --difficulty easy --output delivery-sample --asset-root "$job/workspace" --math-root /media/jake/SSD/EDB/math
"$py" "$repo/generate/pipeline/check_delivery.py" --input runner-batch.json --source "$job/source/source.json" --inventory "$job/source/inventory.json" --difficulty easy --output delivery-batch --asset-root "$job/workspace" --math-root /media/jake/SSD/EDB/math
"$py" delivery-analysis.py
"$py" packaging-check.py
"$py" finish_checks.py
"$repo/generate/runs/current/check-engine" grader-input.json grader-results.json
"$py" "$repo/generate/pipeline/render_preview.py" --input render-records.json --output render-all --limit 24 --asset-root "$job/workspace" --math-root /media/jake/SSD/EDB/math
"$py" "$repo/generate/pipeline/render_preview.py" --input delivery-batch/accepted.json --output render-delivered --limit 5 --asset-root delivery-batch/assets --math-root /media/jake/SSD/EDB/math
"$py" ui_order_audit.py
"$py" write_report.py
