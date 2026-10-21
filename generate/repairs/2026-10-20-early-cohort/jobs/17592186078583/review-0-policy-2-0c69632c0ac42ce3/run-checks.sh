#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
repo=/home/jake/Developer/Course_Academy
job="$repo/generate/repairs/2026-10-20-early-cohort/jobs/17592186078583"
py="$repo/.venv/bin/python"
"$py" audit.py > audit-summary.json
"$repo/generate/runs/current/check-engine" grader-input.json grader-report.json > grader-stdout.txt 2>&1
for level in easy moderate; do
  python3 - "$level" <<'PY'
import json,sys
from pathlib import Path
level=sys.argv[1]
Path('samples-'+level+'.json').write_text(json.dumps([r for r in json.load(open('samples.json')) if r['question'][':question/difficulty'].endswith('/'+level)],indent=2))
PY
  "$py" "$repo/generate/pipeline/check_delivery.py" --input "samples-$level.json" --source "$job/source/source.json" --inventory "$job/source/inventory.json" --difficulty "$level" --output "delivery-$level" --math-root /media/jake/SSD/EDB/math > "delivery-$level-stdout.txt" 2>&1
done
"$py" "$repo/generate/pipeline/check_delivery.py" --input batch.json --source "$job/source/source.json" --inventory "$job/source/inventory.json" --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math > delivery-batch-stdout.txt 2>&1
"$py" variation.py > variation-summary.json
"$repo/generate/runs/current/check-engine" delivered-grader-input.json delivered-grader-report.json > delivered-grader-stdout.txt 2>&1
# Existing render inputs hold the exact independently chosen controlled pairs/layouts.
"$py" "$repo/generate/pipeline/render_preview.py" --input render-records.json --output render --math-root /media/jake/SSD/EDB/math > render-stdout.txt 2>&1
"$py" "$repo/generate/pipeline/render_preview.py" --input render-extra-records.json --output render-extra --math-root /media/jake/SSD/EDB/math > render-extra-stdout.txt 2>&1
"$py" "$repo/generate/pipeline/render_preview.py" --input shortcut-render-records.json --output render-shortcut --math-root /media/jake/SSD/EDB/math > render-shortcut-stdout.txt 2>&1
# The two strict acceptance regressions deliberately fail on this package.
set +e
"$py" reproduce_failures.py cake > failure-cake.txt 2>&1
cake_status=$?
"$py" reproduce_failures.py shortest > failure-shortest.txt 2>&1
shortcut_status=$?
set -e
[[ "$cake_status" == 1 && "$shortcut_status" == 1 ]]
python3 make_report.py
