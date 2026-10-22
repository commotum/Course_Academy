Run from evidence_root. All command output and artifacts are local.

```sh
export PYTHONDONTWRITEBYTECODE=1
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
JOB="$PWD/.."
"$PY" reproduce_profile_omission.py --assert-coverage
"$PY" review_tests.py
for band in moderate hard; do
  "$PY" "$REPO/generate/pipeline/check_delivery.py" --input "delivery-input-$band.json" --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty "$band" --output "delivery-$band" --asset-root "$JOB/workspace" --math-root /media/jake/SSD/EDB/math
done
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input runner-batch.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty moderate --output delivery-batch --asset-root "$JOB/workspace" --math-root /media/jake/SSD/EDB/math
"$PY" prepare_native.py
"$REPO/generate/runs/current/check-engine" native-input.json native-report.json
"$PY" "$REPO/generate/pipeline/render_preview.py" --input render-records.json --output render-all --limit 10 --asset-root "$JOB/workspace" --math-root /media/jake/SSD/EDB/math
"$PY" assess_revision.py
"$PY" complete_report.py
```

The original-import reproduction command and failure are retained in legacy-import-retest.json. The old-versus-current profile regression commands and seeds are in retained-regression.json. Scripts copied from prior review retain provenance in reuse-provenance.json; no author validation oracle was used.
