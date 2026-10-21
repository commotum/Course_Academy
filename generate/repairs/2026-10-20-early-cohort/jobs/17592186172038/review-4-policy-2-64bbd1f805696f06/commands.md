All commands run from this evidence_root. No publication or database mutations are performed. Generator imports suppress bytecode; generated images are configured inside this directory. Initial independent source write is documented by source-analysis.json and test-provenance.json.

```bash
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python review.py > audit.log 2>&1
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python source_and_package.py > source-package.log 2>&1
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python inventory_check.py > inventory-check.log 2>&1
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json > grader.log 2>&1
```

Delivery inputs are retained in delivery-input.json (24 independently sampled records, 32 controlled records, one boundary record, one intentional duplicate) and runner-batch.json (verbatim runner batch). The following shared adapter commands use the captured inventory and source directly:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input delivery-input.json --source /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186172038/source/source.json --inventory /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186172038/source/inventory.json --difficulty easy --output delivery-independent --asset-root assets --math-root /media/jake/SSD/EDB/math
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input runner-batch.json --source /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186172038/source/source.json --inventory /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186172038/source/inventory.json --difficulty easy --output delivery-runner --asset-root /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186172038/outputs-4 --math-root /media/jake/SSD/EDB/math
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python delivery_analysis.py > delivery-analysis.log 2>&1
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine delivered-grader-input.json delivered-grader-results.json > delivered-grader.log 2>&1
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python extra_checks.py > extra-checks.log 2>&1
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-complete-records.json --output render-complete --limit 51 --asset-root assets --asset-root delivery-runner/assets --math-root /media/jake/SSD/EDB/math > render-complete.log 2>&1
python3 finalize_report.py > finalize-report.log 2>&1
```

Fresh sample seeds: 862100–862103, 862200–862203, 862300–862303, 862400–862403, 862500–862503, 862600–862603. Fixed-bank intervention seeds: 863000–863005. Source replays: 862001–862008. Irrelevant reorder: 863199. Boundary: 863210. Relocation: 863981. CLI: 864002. Exact parameters and complete records are saved in their corresponding JSON files.

The inherited audit.py provides helper functions only; review.py is the current test driver. Initial pixel PCA diagnostics are retained in pixel-initial-diagnostic.json; axis text/spines invalidate isolation at axis-coincident points. extra_checks.py explicitly excludes those points, measures 335 off-axis segments, and separately verifies runtime and external-output behavior. System python3 is used for final JSON Schema validation because jsonschema is installed there; generator/runtime tests use the supplied Python 3.13.5 executable.
