All commands run from this evidence_root. `PY=/home/jake/Developer/Course_Academy/.venv/bin/python`; `REPO=/home/jake/Developer/Course_Academy`; `JOB=$REPO/generate/repairs/2026-10-20-early-cohort/jobs/17592186184172`.

```sh
$PY audit.py > audit-console.json
$PY - <<'PY_SPLIT'
import json
rows=json.load(open('fresh-records.json'))
for level in ['moderate','hard']:
    json.dump([r for r in rows if r['question'][':question/difficulty'].endswith('/'+level)],open('fresh-'+level+'.json','w'),indent=2)
PY_SPLIT
$PY $REPO/generate/pipeline/check_delivery.py --input runner-batch.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty moderate --output delivery-batch --asset-root relocated --math-root /media/jake/SSD/EDB/math
$PY $REPO/generate/pipeline/check_delivery.py --input fresh-moderate.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty moderate --output delivery-moderate --asset-root relocated --math-root /media/jake/SSD/EDB/math
$PY $REPO/generate/pipeline/check_delivery.py --input fresh-hard.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty hard --output delivery-hard --asset-root relocated --math-root /media/jake/SSD/EDB/math
$PY followup.py > followup-console.txt
$REPO/generate/runs/current/check-engine native-input.json native-report.json
$PY $REPO/generate/pipeline/render_preview.py --input render-records.json --output render-all --limit 13 --asset-root relocated --math-root /media/jake/SSD/EDB/math
$PY reproduce_profile_omission.py --assert-coverage
# Previous command intentionally fails with the demonstrated profile omission.
$PY $REPO/generate/pipeline/check_delivery.py --input profile-omission-records.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty moderate --output delivery-profile-omission --asset-root relocated --math-root /media/jake/SSD/EDB/math
$PY assess.py > assessment-console.json
$PY finish_report.py
```

`followup.py` needs the three delivery outputs before constructing its final combined native input. The initial `audit.py` native input can be run independently. `fresh-moderate.json` and `fresh-hard.json` retain the exact arrays chosen from `fresh-records.json` for shared delivery. All seeds and explicit parameters are in generated record metadata and the reproduction scripts. No author validation oracle was executed. Source-analysis.json was saved and verified before package inspection.

The initial original-generator copy ran successfully inside the repository because its ancestor search could find the undeclared dependency. `standalone_discovery.py` then hid only external `scripts/generator_policy.py` discovery and reproduced the exact original StopIteration failure without writing outside evidence_root. That distinction is retained in both packaging evidence files. Current normal manifest-only relocated execution passes. Python `-I` failure is not treated as a package failure because isolated mode disables sibling modules generally.

Source, math, grading, runtime and rendering checks passed their stated bounds. Final REVISE is for the normal CLI profile-prefix restriction, with a strict failing runnable acceptance test. `evidence-contract-validation.json` confirms schema and all referenced relative files. All 15 captured inventory questions are original sources, so `affected-inventory.json` is empty after provenance inspection, not because generated inventory was left untested.
