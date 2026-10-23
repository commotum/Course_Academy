Run from this evidence directory. `PY=/home/jake/Developer/Course_Academy/.venv/bin/python`; `REPO=/home/jake/Developer/Course_Academy`.

```sh
$PY -B review.py
$PY -B stage_review.py
$PY -B author-current/check_repair.py
$PY -B author-current/check_batch_repair.py --small-sample
$PY -B author-old-frequency/check_repair.py  # expected assertion: retained 36-case failure
$PY -B author-old-batch/check_batch_repair.py --small-sample  # expected assertion: uniform sign cue
$PY -B reproduce_shortcut.py
$PY -B reproduce_shortcut.py author-old-frequency/17592186161967.py  # expected exit 1
$PY -B reproduce_batch_shortcut.py delivery-batch/accepted.json
$PY -B reproduce_batch_shortcut.py ../review-1-policy-2-fa94c3c9d1dc4929/batch.json  # expected exit 1
$PY -B "$REPO/generate/pipeline/check_delivery.py" --input batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root relocated --math-root /media/jake/SSD/EDB/math
$PY -B "$REPO/generate/pipeline/check_delivery.py" --input fresh-samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-fresh --asset-root relocated --math-root /media/jake/SSD/EDB/math
$PY -B "$REPO/generate/pipeline/check_delivery.py" --input fresh-batches.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-fresh-batches --asset-root relocated --math-root /media/jake/SSD/EDB/math
$PY -B post_review.py
"$REPO/generate/runs/current/check-engine" all-grader-input.json grader-report.json
$PY -B "$REPO/generate/pipeline/render_preview.py" --input render-records.json --output render --asset-root relocated --math-root /media/jake/SSD/EDB/math
$PY -B "$REPO/generate/pipeline/render_preview.py" --input target-render-records.json --output target-render --asset-root relocated
$PY -B layout_probe.py
python3 finalize_review.py
```

Independent fresh CLI seed/count pairs: 881901/5, 881902/9, 881903/12. Direct per-profile diagnostic seeds: 672109–672111. Explicit counterfactuals, source replay parameters, and boundaries are in review.py and complete record files. The author check copies change only their input paths; they write under their evidence-root copies. Preservation origins and unchanged-function comparison are recorded in provenance.json and change-scope.json.
