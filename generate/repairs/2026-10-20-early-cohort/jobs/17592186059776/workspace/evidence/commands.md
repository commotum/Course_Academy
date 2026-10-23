# Reproduction and validation commands

Run from this workspace. Python is `/home/jake/Developer/Course_Academy/.venv/bin/python`.

Before repair (exit 1, 24/24 shortcut hits):

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python evidence/before/reproduce-shortcut.py "$PWD/17592186059776.py"
```

The copied script is unchanged; its original failing output and records are retained under `evidence/before/`. Running it now tests the repaired code, so preserve that historical output.

After repair:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python evidence/after/reproduce-shortcut.py "$PWD/17592186059776.py"
/home/jake/Developer/Course_Academy/.venv/bin/python check_repair.py
/home/jake/Developer/Course_Academy/.venv/bin/python validate_repair.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/validation/native-input.json evidence/validation/native-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python check_role_witnesses.py
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/roles/native-input.json evidence/roles/native-results.json
```

The main native run passed 162 correct and 648 incorrect responses. After discovering and repairing the q-20500 number-form cue, only its affected 13 records were regraded (13 accepted, 52 rejected) with:

```sh
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/validation/native-affected-input.json evidence/validation/native-affected-results.json
```

The final main input contains the repaired records. In the saved earlier main native results, q-20500 entries are superseded by `native-affected-results.json`; all other entries remain current. The separate role-witness grading passed 78 correct and 312 incorrect responses. These witnesses vary banks at fixed equations and do not inflate semantic-instance counts.

Actual delivery filters:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/validation/easy-delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-easy --asset-root evidence --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/validation/moderate-delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty moderate --output evidence/delivery-moderate --asset-root evidence --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/validation/exact-batch.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery-batch --asset-root evidence --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python inspect_delivery.py
```

Actual UI:

```sh
python3 /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/validation/render-input.json --output evidence/render --asset-root evidence --math-root /media/jake/SSD/EDB/math
python3 /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/validation/render-affected-input.json --output evidence/render-affected --asset-root evidence --math-root /media/jake/SSD/EDB/math
```

The first two screenshots in `render/` are current. Its third screenshot exposed the number-form cue and is retained as intermediate evidence; the final q-20500 screenshot is `render-affected/question-001.png`. All four screenshots were visually inspected; see `visual-inspection.json`.

Exact batch regenerated with original seed 3334594587 and original template/parameter selections. All five survive actual delivery filtering; the reported second-smallest strategy now succeeds on 0/5, versus 4/5 before. The 24 retained family probes now give 9/24 hits with no fixed-rank family. Complete source replay remains 10/10. Twelve numerical probes per profile give 100 distinct solution tasks across the supported bands. Every rank and authored position has an explicit fixed-prompt witness in every profile. Delivery-filtered non-source records vary ranks and positions in all ten profiles.

No publication, database mutation, service calls, or writes outside the workspace were performed. Native tools and renderer were used through their supplied read-only interfaces. Live learner-history eligibility was not simulated; see delivery-comparison.json.
