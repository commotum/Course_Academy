Run from /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186105746/review-1-policy-2-4301bd9690936d29. All generated artifacts stay in this evidence directory. Set PYTHONDONTWRITEBYTECODE=1 for package imports.

Independent retained regressions (current exits 0):
  PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python targeted-regressions.py
Old-package falsification (exits 1 with both retained failures):
  REVIEW_PACKAGE=/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186105746/review-0-policy-2-f4f6723c67ba4318/relocated-package PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python targeted-regressions.py
The old report was saved as old-targeted-regressions.json before rerunning current. old-failing-records.json retains the complete scale-2 q-42157 record. The missing-source failure is the explicit q-20964 call in targeted-regressions.py.

Redirected author preflight (checks unchanged; all outputs redirected here):
  PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python author-check-copy.py
Independent fresh source/math/controlled-pair/packaging checks:
  PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python audit.py

Actual publisher delivery filters:
  PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input delivery-input.json --source /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186105746/source/source.json --inventory /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186105746/source/inventory.json --difficulty easy --output delivery-domain --math-root /media/jake/SSD/EDB/math
  PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch-records.json --source /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186105746/source/source.json --inventory /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186105746/source/inventory.json --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math
Decision, inventory, selection and executable-preflight verification:
  PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python finish.py
Actual native grader (one batched final invocation):
  /home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-final-input.json grader-final-results.json
Actual UI renderer:
  PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --math-root /media/jake/SSD/EDB/math
  PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input delivery-batch/accepted.json --output render-batch --asset-root delivery-batch/assets --math-root /media/jake/SSD/EDB/math --limit 5
The first renderer invocation deliberately uses its default 6-record limit; those six are the two counterfactual types, recovered source, zero boundary and moderate negative-pivot case. The separate batch invocation renders all five publisher-accepted records. Screenshots inspected are listed in visual-review.json.

Report assembly (run once after tests; it appends a UI probe):
  python3 write_report.py
Schema validation used system python3 jsonschema.validate against /home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json, plus local nonempty evidence-reference assertions; see evidence-contract-check.json.
No database, publication or package mutation commands were run.
