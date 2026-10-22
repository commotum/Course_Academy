# Review reproduction

Run from `/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186119847/review-4-policy-2-f0e377c88f1ec20e`. All scripts and outputs stay below this directory. No publication or database mutation is performed.

1. `/home/jake/Developer/Course_Academy/.venv/bin/python -B audit.py > audit.stdout 2> audit.stderr`
2. `/home/jake/Developer/Course_Academy/.venv/bin/python -B regression-driver.py > regression-driver.stdout 2> regression-driver.stderr`

For each input/difficulty below, run:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input INPUT.json --source /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186119847/source/source.json --inventory /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186119847/source/inventory.json --difficulty LEVEL --output delivery-INPUT --math-root /media/jake/SSD/EDB/math
```

Inputs: easy-records/easy, moderate-records/moderate, runner-batch/easy, controls-easy/easy, controls-moderate/moderate, restriction-easy/easy, restriction-moderate/moderate, cli-easy-12/easy, cli-moderate-98/moderate. The repaired-control-records/moderate set uses output delivery-repaired-controls.

3. `/home/jake/Developer/Course_Academy/.venv/bin/python -B finish-tests.py > finish-tests.stdout 2> finish-tests.stderr`
4. Render render-records.json with default limit 6 into render; render its tail from index 6 as render-tail-records.json with --limit 8 into render-tail; render delivery-repaired-controls/accepted.json with --limit 3 into render-repaired.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input RECORDS.json --output OUTPUT --limit LIMIT --math-root /media/jake/SSD/EDB/math
```

5. `/home/jake/Developer/Course_Academy/.venv/bin/python -B variation-tests.py > variation-tests.stdout 2> variation-tests.stderr`
6. `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input-final.json grader-report-final.json > grader-final.stdout 2> grader-final.stderr`
7. Inspect saved actual UI screenshots as described in render-inspection.json.
8. `python3 -B finalize-review.py`

Fresh profile seeds: 194029,284767,981011,918717,723419,554137. Independent repaired cases use 28907; paired repaired counterfactuals use 517319. Complete records contain exact parameters and generation metadata. Original strict regressions use 17. Finite-capacity CLI/relocation uses 428163.

The paired repaired control records hold profile q-79409, name Q, columns 7, seed 517319 fixed: (rows,count)=(5,3),(5,2),(4,3). Their expected ranks are 4,5,4.

Prerequisite source-analysis.json was copied/confirmed and verified before any package inspection; provenance.json identifies the prior independent scripts. Package baseline and final hashes match.
