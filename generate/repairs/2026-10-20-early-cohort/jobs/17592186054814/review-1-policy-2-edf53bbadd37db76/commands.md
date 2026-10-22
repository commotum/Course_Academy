Review commands run from evidence_root. All reviewer scripts/results and package copies stay here. No publication or database access.

```sh
python3 -B confirm_source.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B review_checks.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input sample-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-sample --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --asset-root ../workspace --math-root /media/jake/SSD/EDB/math --limit 15
/home/jake/Developer/Course_Academy/.venv/bin/python -B variation_review.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B finish_review.py
```

Fresh sample seed 731905 (40 records); controlled seed 731907; full negative bounded domain seed 731906; relocation seed 942137. Retained independent source_acceptance.py runs automatically against earlier failing bound bytes and current package. The author's named preflight runs against evidence_root/preflight-package so all its output remains here.
