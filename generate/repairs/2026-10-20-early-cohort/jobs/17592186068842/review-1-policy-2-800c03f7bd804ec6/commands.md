Run from this evidence directory. All commands read the package; all artifacts are written here. `PYTHONDONTWRITEBYTECODE=1` prevents package cache writes. Reused scripts and bindings are documented in reuse-provenance.json. No publisher or database writes occurred.

```bash
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python review.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python revision_checks.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python independent_checks.py
python3 counterfactual_check.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-report.json
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input easy-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-control --math-root /media/jake/SSD/EDB/math
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output delivery-batch --math-root /media/jake/SSD/EDB/math
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python shortcut_reproduction.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python bank_shortcut.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python minimal_repro.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python delivery_current.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-records.json --output render-all --limit 32 --math-root /media/jake/SSD/EDB/math
python3 finalize_review.py
python3 write_result.py
```

The old `shortcut_reproduction.py` now exits 0 (prior unique-fractionless rule defeated). `bank_shortcut.py` and `minimal_repro.py` deliberately exit 1 on the current package, retaining complete records and probe results. This is a demonstrated failure, not an unavailable check. The retained author regression is run on evidence-only relocated current/previous packages by revision_checks.py; it exits 1 on the previous implementation and 0 on current, with matching script digest. The old review's requirements.txt was absent in its relocation snapshot, so the current requirements file was used for that historical executable test; its Python/SymPy versions are identical. The math helper itself is unchanged by this repair.

Fresh independent seeds: 9357 for source replay; 59173 for boundaries/fresh generation; 9106/9107 for unchanged-template counterfactual regression; 0/1 for both changed quotient profiles and all powers; 61093 for radical boundaries; 9106 for radical controlled pairs; 0/5 for seed-only changed-bank shuffle. Prior witnesses seed 17, n=1 and seed 2404317989, base=4,a=3,n=4 are retained, alongside the exact new batch (same last seed, a=4).
