#!/usr/bin/env bash
# Read-only audit; all generated artifacts stay in this evidence directory.
set -eu
E="$(cd "$(dirname "$0")" && pwd)"
J="$(dirname "$E")"
R=/home/jake/Developer/Course_Academy
P="$R/.venv/bin/python"
export PYTHONDONTWRITEBYTECODE=1
cd "$E"
"$P" audit.py
"$R/generate/runs/current/check-engine" grader-input.json grader-results.json
"$P" - <<'PY'
import json,pathlib
rs=json.load(open('independent-samples.json'))
for d in ['moderate','hard']:
 pathlib.Path('samples-'+d+'.json').write_text(json.dumps([r for r in rs if r['question'][':question/difficulty'].endswith('/'+d)],indent=2))
rs=json.load(open('render-input.json'));pathlib.Path('render-pairs-input.json').write_text(json.dumps(rs[5:],indent=2))
PY
for d in moderate hard; do
 "$P" "$R/generate/pipeline/check_delivery.py" --input "samples-$d.json" --source "$J/source/source.json" --inventory "$J/source/inventory.json" --difficulty "$d" --output "delivery-$d" --math-root /media/jake/SSD/EDB/math
done
"$P" "$R/generate/pipeline/check_delivery.py" --input runner-batch.json --source "$J/source/source.json" --inventory "$J/source/inventory.json" --difficulty moderate --output delivery-batch --math-root /media/jake/SSD/EDB/math
"$P" "$R/generate/pipeline/render_preview.py" --input render-input.json --output render --limit 6 --math-root /media/jake/SSD/EDB/math
"$P" "$R/generate/pipeline/render_preview.py" --input render-pairs-input.json --output render-pairs --limit 5 --math-root /media/jake/SSD/EDB/math
"$P" finish_review.py
"$P" write_report.py
# Strict independent regression intentionally exits 1 on the reviewed package.
"$P" regressions.py
