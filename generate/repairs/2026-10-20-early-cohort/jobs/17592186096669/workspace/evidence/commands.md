# Reproduction commands

Run from the workspace. Python: `/home/jake/Developer/Course_Academy/.venv/bin/python` (3.13.5; SymPy 1.14.0). Shared tools below are read-only with respect to the database and published files.

Original failures, executed before repair:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python 17592186096669.py --seed 73421 --profile q-129453 --scale 4 --count 1 > evidence/before-shortcut.json
/home/jake/Developer/Course_Academy/.venv/bin/python 17592186096669.py --profile q-20450 --scale 1 --count 1 > evidence/before-source.json 2> evidence/before-source-error.txt
```

The second command exited 2. The first exposed the unique positive-middle correct vector. `checks/regressions.py` retains both exact cases and all profile-level bank-only counterexamples through a stronger fixed-bank/all-five-keys witness.

Final validation commands:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python checks/regressions.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-report.json
/home/jake/Developer/Course_Academy/.venv/bin/python 17592186096669.py --difficulty easy --count 5 --seed 73421 --format json > evidence/batch.json
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/controlled.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-controlled --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/normal.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-normal --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-batch --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python checks/delivery_probes.py
/home/jake/Developer/Course_Academy/.venv/bin/python checks/package_check.py
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render-final --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

All final commands exited 0. The four final screenshots were inspected visually. The earlier `render/` directory preserves the clipped-line counterexample; `render-final/` contains the corrected layout. Legacy validation under `17592186096669/` is retained historical evidence, not validation of this repair. The manifest declares only the current runtime files.
