#!/usr/bin/env bash
set -eu
cd -- "$(dirname -- "$0")"
export PYTHONDONTWRITEBYTECODE=1
repo=/home/jake/Developer/Course_Academy
py="$repo/.venv/bin/python"
"$py" audit.py
"$py" "$repo/generate/pipeline/check_delivery.py" --input samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-samples --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
"$py" "$repo/generate/pipeline/check_delivery.py" --input batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
"$repo/generate/runs/current/check-engine" grader-input.json grader-report.json
"$py" "$repo/generate/pipeline/render_preview.py" --input render-input.json --output render --limit 6 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
"$py" -c 'import json; json.dump(json.load(open("render-input.json"))[6:],open("render-extra-input.json","w"),indent=2)'
"$py" "$repo/generate/pipeline/render_preview.py" --input render-extra-input.json --output render-extra --limit 8 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
"$py" finish_checks.py
# This strict assertion MUST fail on the reviewed package. It is the demonstrated defect.
if "$py" shortcut_regression.py > shortcut-regression.log 2>&1; then
  printf '%s\n' 'Shortcut regression no longer reproduces; independently review the changed construction.'
else
  printf '%s\n' 'Demonstrated shortcut reproduced; inspect shortcut-regression.log.'
fi
# write_report.py records the human visual inspection performed in this review.
