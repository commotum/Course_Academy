Run from this evidence directory. All generated outputs remain here. Use the job Python; system `python3` does not have SymPy.

```bash
REVIEW_REPO=/home/jake/Developer/Course_Academy
REVIEW_PY=$REVIEW_REPO/.venv/bin/python
REVIEW_JOB=$(dirname "$PWD")
REVIEW_WORK=$REVIEW_JOB/workspace

# Independent current source replay, math, construction boundaries and counterfactuals.
# Explicit seeds and parameters are in review.py and complete generated records.
"$REVIEW_PY" -B review.py

# Retained exact minimal regression: old fails with three KeyErrors, current passes.
"$REVIEW_PY" -B reproduce_missing.py --workspace regression-old
"$REVIEW_PY" -B reproduce_missing.py --workspace "$REVIEW_WORK"

# Author regression runs only on the evidence-local relocated copy, since it writes reports.
"$REVIEW_PY" -B relocated/checks/source_regression.py

# Actual read-only normalization, captured-inventory deduplication and difficulty filter.
for REVIEW_STAGE in controlled sample batch; do
  case "$REVIEW_STAGE" in
    controlled) REVIEW_INPUT=controlled-records.json ;;
    sample) REVIEW_INPUT=random-records.json ;;
    batch) REVIEW_INPUT=runner-batch.json ;;
  esac
  "$REVIEW_PY" -B "$REVIEW_REPO/generate/pipeline/check_delivery.py" \
    --input "$REVIEW_INPUT" --source "$REVIEW_JOB/source/source.json" \
    --inventory "$REVIEW_JOB/source/inventory.json" --difficulty easy \
    --output "delivery-$REVIEW_STAGE" --asset-root "$REVIEW_WORK" \
    --math-root /media/jake/SSD/EDB/math
done

"$REVIEW_PY" -B post_delivery.py
"$REVIEW_REPO/generate/runs/current/check-engine" grader-input.json grader-results.json

# Complete UI inputs contain batch, all counterfactual pairs and restored source replays.
"$REVIEW_PY" -B "$REVIEW_REPO/generate/pipeline/render_preview.py" \
  --input render-records.json --output render --limit 17 \
  --asset-root "$REVIEW_WORK" --math-root /media/jake/SSD/EDB/math
# Existing evidence used a six-record first render plus eleven-record render-rest.
"$REVIEW_PY" -B "$REVIEW_REPO/generate/pipeline/render_preview.py" \
  --input render-rest-records.json --output render-rest --limit 11 \
  --asset-root "$REVIEW_WORK" --math-root /media/jake/SSD/EDB/math
"$REVIEW_PY" -B "$REVIEW_REPO/generate/pipeline/render_preview.py" \
  --input delivery-batch/accepted.json --output render-delivered --limit 5 \
  --asset-root delivery-batch/assets --math-root /media/jake/SSD/EDB/math

"$REVIEW_PY" -B variation.py
node ui-order.cjs
node ui-id-probe.cjs
# ui-id-probe creates the first ID fixture. The second saved fixture is normalized
# batch record index 3, moved from fixture item ID 4 to item ID 1.
"$REVIEW_PY" -B "$REVIEW_REPO/generate/pipeline/render_preview.py" \
  --input render-id-counterfactual-2.json --output render-id-counterfactual-2 \
  --limit 1 --asset-root delivery-batch/assets --math-root /media/jake/SSD/EDB/math
python3 -B finalize.py
```

`repair-regression-results.json` retains exact old/current commands and outputs, including the author regression's compatibility alias needed to reach its substantive completeness assertion on the old interface. `provenance.json` identifies reused independent scripts and evidence. Source-key correction to the earlier review account is in `source-key-context.json` and `source-analysis.json`. No publication or database transaction was performed.
