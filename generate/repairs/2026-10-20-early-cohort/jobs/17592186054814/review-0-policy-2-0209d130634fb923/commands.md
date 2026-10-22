All commands run from evidence_root; Python bytecode disabled. No DB or publication actions.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B audit.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B source_acceptance.py # expected exit 1 until repaired
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input sample-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-sample --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --asset-root ../workspace --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --asset-root ../workspace --math-root /media/jake/SSD/EDB/math --limit 11
/home/jake/Developer/Course_Academy/.venv/bin/python -B variation_audit.py
/home/jake/Developer/Course_Academy/.venv/bin/python -B finalize_evidence.py
```

Fresh sample seed 229173, 80 records; controlled seed 229174; CLI deterministic relocation seed 419623. No retained repair_history/preflight files present. Initial source analysis saved before implementation inspection.
