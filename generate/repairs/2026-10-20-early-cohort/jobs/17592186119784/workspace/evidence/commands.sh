# Run from workspace. Original pre-repair failure output: before-regressions.txt.
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
JOB=$REPO/generate/repairs/2026-10-20-early-cohort/jobs/17592186119784
$PY -B regression_tests.py
$PY -B validate_repair.py
$REPO/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-results.json
for BAND in moderate hard; do
 $PY $REPO/generate/pipeline/check_delivery.py --input evidence/$BAND-records.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty $BAND --output evidence/delivery-$BAND --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
done
$PY -B check_delivery_variation.py
$PY -B verify_package.py
$PY $REPO/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY $REPO/generate/pipeline/render_preview.py --input evidence/render-extra-records.json --output evidence/render-extra --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
# The native engine is used without rebuilding or modifying it.
