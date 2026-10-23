All commands ran from evidence_root. Python was `/home/jake/Developer/Course_Academy/.venv/bin/python`; every Python command used `-B` to avoid package bytecode writes. No database access or publication occurred.

Reproduction sequence (absolute paths supplied by the job; outputs remain here):

```bash
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
REPO=/home/jake/Developer/Course_Academy
JOB=$REPO/generate/repairs/2026-10-20-early-cohort/jobs/17592186096842
$PY -B audit.py > audit.log 2>&1
$PY -B generate_pairs.py
$PY -B verify_saved.py > verify-saved.log 2>&1
$REPO/generate/runs/current/check-engine grader-input.json grader-results.json > grader.log 2>&1
$PY -B author-check/regression.py > author-regression.log 2>&1
$PY -B shortcut_probe.py prior-failing-batch.json > prior-shortcut.log 2>&1
# Previous line intentionally exits 1 on the preserved historical defect.
$PY -B $REPO/generate/pipeline/check_delivery.py --input batch-records.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty easy --output delivery-batch --asset-root assets --math-root /media/jake/SSD/EDB/math > delivery-batch.log 2>&1
$PY -B $REPO/generate/pipeline/check_delivery.py --input independent-easy.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty easy --output delivery-independent --asset-root assets --math-root /media/jake/SSD/EDB/math > delivery-independent.log 2>&1
$PY -B $REPO/generate/pipeline/render_preview.py --input render-records.json --output render --limit 6 --asset-root assets --math-root /media/jake/SSD/EDB/math > render.log 2>&1
$PY -B $REPO/generate/pipeline/render_preview.py --input render-extra-records.json --output render-extra --limit 7 --asset-root assets --math-root /media/jake/SSD/EDB/math > render-extra.log 2>&1
$PY -B review_checks.py > review-checks.log 2>&1
$PY -B finish_report.py > finish-report.log 2>&1
```

The initial `audit.py` symbolic equality check does not assume positive radicands; `verify_saved.py` resolves its apparent reciprocal-root mismatches using the source's real positive domain. Its corrected independent math and grader expectations are the final results.

`audit.py`, `audit_helpers.py`, `shortcut_probe.py`, and `verify_saved.py` originated in the prior independent review. Seeds and sample counts were adjusted as recorded in `reuse-provenance.json`. `generate_pairs.py` retains the controlled extensions initially created in a Python invocation. `author-check` is a copied retained regression with package and output locations adapted; its original assertions were independently tested against the historical failing batch. No author script was allowed to write under the package.

`finish_report.py` records the human screenshot inspection already completed in this review; rerunning it alone is not a new visual inspection.
