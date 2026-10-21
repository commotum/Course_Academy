#!/usr/bin/env bash
# Run from the supplied workspace. All writes stay under evidence/ or /tmp.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
"$PY" checks/latest_failure.py
"$PY" checks/source_replay.py
"$PY" checks/validate_repair.py
"$PY" generator.py --difficulty easy --count 5 --seed 20261021 --format json > evidence/batch.json
"$PY" - <<'PY'
import json
from pathlib import Path
p=Path('evidence')
samples=json.loads((p/'easy-samples.json').read_text())
controls=[r for r in json.loads((p/'counterfactual-records.json').read_text()) if r['generation']['difficulty']=='easy']
(p/'delivery-input.json').write_text(json.dumps(samples+controls))
PY
"$REPO/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-results.json
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-batch --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$PY" checks/finish_checks.py
"$REPO/generate/runs/current/check-engine" evidence/delivered-grader-input.json evidence/delivered-grader-results.json
"$PY" "$REPO/generate/pipeline/render_preview.py" --input evidence/repaired-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
