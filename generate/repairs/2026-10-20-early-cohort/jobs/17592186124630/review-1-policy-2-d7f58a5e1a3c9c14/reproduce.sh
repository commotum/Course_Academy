#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
export PYTHONDONTWRITEBYTECODE=1
export TMPDIR="$PWD/tmp"
mkdir -p "$TMPDIR"
REPO=/home/jake/Developer/Course_Academy
JOB="$PWD/.."
PY="$REPO/.venv/bin/python"
"$PY" audit.py
"$REPO/generate/runs/current/check-engine" grader-input.json grader-report.json
for spec in fresh-samples:delivery-fresh runner-batch:delivery-batch duplicate-probe:delivery-duplicates; do
  "$PY" "$REPO/generate/pipeline/check_delivery.py" --input "${spec%:*}.json" --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty easy --output "${spec#*:}" --asset-root . --math-root /media/jake/SSD/EDB/math
done
"$PY" "$REPO/generate/pipeline/render_preview.py" --input render-records.json --output render-all --asset-root . --math-root /media/jake/SSD/EDB/math --limit 19
python3 variation_checks.py
python3 finalize_evidence.py
