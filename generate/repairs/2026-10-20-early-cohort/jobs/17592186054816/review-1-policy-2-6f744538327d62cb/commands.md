Run from this evidence_root:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python review.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-samples --math-root /media/jake/SSD/EDB/math
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render --math-root /media/jake/SSD/EDB/math
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input counterfactual-records.json --output render-pairs --limit 12 --math-root /media/jake/SSD/EDB/math
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python author-harness/workspace/checks/repair_check.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python stages.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python finish.py
```

`review.py` retains independently derived prompt-based mathematics and strict acceptance assertions for each prior defect. It reproduces baseline failures using the retained legacy constructor and tests unchanged explicit parameters on the current constructor. Fresh seed:493127; retained seed:827461; rejection test seed:61409. The author preflight executes an evidence-local copy with its own outputs contained under author-harness; the package's check is not run in place because it writes author artifacts.

`prior-oracle.py` is the original independent review's reusable oracle prefix. `legacy-generator.py` is the author's retained historical constructor; its source-bank and None failures are independently reproduced, and it reconstructs the stored inventory fingerprints and publisher UUIDs. Provenance is explicit in provenance.json. Source passages were independently reconfirmed before copying the source account.

The final schema validation uses system python3's installed jsonschema, because the generator's prescribed Python environment has no jsonschema package. Generator execution and runtime dependency verification use the prescribed Python3.13.5. No dependency was installed.
