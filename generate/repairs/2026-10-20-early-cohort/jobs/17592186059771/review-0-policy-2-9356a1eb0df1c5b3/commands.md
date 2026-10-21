All commands run from this evidence directory. Python imports used -B or sys.dont_write_bytecode; no package files or database content were written.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B review.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B supplemental.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B target_check.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B regressions.py
```

The strict regressions command exits 1 on this package: two unknown source profiles and missing distinct-destination hard generation. Regression results are saved before exit. The exploratory extra `operations` field in hard-restriction-records is not a promised API; ignoring it is not reported as an input-validation defect. The construction omission is independently established by the delivered source cases, sampled normal prompts, and hard.operations/validate rules.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input easy-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-control --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input counterfactual-records.json --output render-pairs --limit 5 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-other-records.json --output render-other --limit 2 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input target-records.json --output render-targets --limit 2 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
python3 finalize.py
```

The first renderer invocation used its default limit of six: all five exact batch records and the first swap control. render-pairs covers all five pair records, render-other covers moderate/hard, and render-targets covers the additional two target cases. All reports passed. Final grader invocation includes 21 records / 105 native checks.
