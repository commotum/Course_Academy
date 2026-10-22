Run from this evidence directory. All artifacts and copies stay here; `-B` prevents bytecode writes in package/repo paths.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B review.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json
```

Delivery commands (executed once each with NAME/FILE = catalog/catalog.json, fresh/fresh.json, batch/batch.json):

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input FILE --source /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186119848/source/source.json --inventory /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186119848/source/inventory.json --difficulty easy --output delivery-NAME --asset-root . --math-root /media/jake/SSD/EDB/math
```

UI inputs are retained in render-records.json and render-more-records.json (ten profile representatives + three counterfactual records + five runner records, split6/12).

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --asset-root . --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-more-records.json --output render-more --asset-root . --math-root /media/jake/SSD/EDB/math --limit 12
/home/jake/Developer/Course_Academy/.venv/bin/python -B audit_delivery.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine shortcut-grader-input.json shortcut-grader-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B check_batch_decisions.py --input batch.json --report batch-regression.json
```

The last command must exit1 on this batch, with A forced true in both members of the visible subgroup. Its input can be replaced with minimal-failing-batch.json to reproduce the same defect on the minimal two-record pool.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B finish_report.py
python3 -B verify_evidence.py
```

`verify_evidence.py` uses system Python's installed jsonschema; it is absent from the generator venv, so no dependency was installed or added to the package. The review's initial regression-copy attempt omitted its package.json and was corrected before the retained check was assessed. Final packaging-results.json records successful current-package execution and the failing restored-import fixture. Raw stored-bank positions are distinguished from actual UI display order in rendered-position-probe.json; the UI first-option probe succeeds0/3. Neither reviewer tooling correction is reported as a generator defect.
