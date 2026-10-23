Run from this evidence directory. All paths below are read-only inputs except outputs beneath this directory. Set `PYTHONDONTWRITEBYTECODE=1` for Python package imports.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python review_checks.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python reproduce_source_gap.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python source_completion_check.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-combined-input.json grader-report.json
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-samples --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render-pairs --limit 20 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input delivery-batch/accepted.json --output render-delivered --limit 5 --asset-root delivery-batch/assets --math-root /media/jake/SSD/EDB/math
python3 variation_checks.py --candidate-records batch.json
```

`reproduce_source_gap.py` intentionally exits 1 on the current package. `review_checks.py` records observed source failures without stopping the independent remaining tests. Native grader combined input retains every complete record and expected response, including the single historical generated record with captured generation metadata. The preliminary reviewer TeX-parser mistake was corrected before final math and grader results; see render-inspection.json. No preliminary tool error is treated as a generator defect.

Fresh sample seeds: 89321–89344. Boundary cases use seed 808. Controlled pairs use seeds 53 and 54 with explicit coefficients. Runner CLI replay uses seed 3129290382, count 5, easy. Historical record generation seed: 2997460248, version constant-ln-1; it was read and checked, not regenerated or published.
