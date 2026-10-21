#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/fresh-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/delivery-fresh --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/batch-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/delivery-batch --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/counterfactual-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/delivery-cf --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
