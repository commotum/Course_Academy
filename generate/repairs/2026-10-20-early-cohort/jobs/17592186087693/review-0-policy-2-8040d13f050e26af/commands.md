Run from evidence_root. No command publishes assets or connects to the database.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B audit.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input samples.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-sample --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input runner-batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-input.json --output render --limit 6 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-remaining.json --output render-remaining --limit 10 --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
python3 variation.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B replay_regression.py --package ../workspace
python3 -B finish_review.py
```

The replay regression intentionally fails with exit 1 on the reviewed package. All other listed checks completed successfully. `finish_review.py` uses system Python for the installed JSON Schema validator; generator dependency/version tests use the supplied virtual-environment Python. The first finalization attempt under that virtual environment lacked jsonschema; rerunning with system Python validated the saved schema successfully. No generator test was substituted.

Seeds and complete explicit parameters are retained in audit.py, samples.json, boundaries.json and counterfactual-records.json. No repair history or preflight file was present at the supplied paths. No author validation reports were included in the package. Inspection used the source capture, actual package and shared grader/delivery/UI tools.
