# Determining the Dimensions of a Matrix

Version 1.1.0 validates **easy only**. Moderate/hard lack a supported difficulty escalation and reject generation. The finite domain has 25 ordered shapes with 2..6 rows and columns. Changing entries, names, seed, bank, choice order or response layout does not replenish a used shape. Earlier peer-label evidence is retained in history/v1-peer-labels.

```sh
.venv/bin/python generate/scratch/17592186087693/validate.py
.venv/bin/python generate/scratch/17592186087693.py --difficulty easy --seed 20 --count 5 --format json
.venv/bin/python generate/scratch/17592186087693/replenish.py
```

All eight original source banks and layouts replay exactly. Six supplied solutions replay exactly, including a documented R/P naming error in q-139406. Two missing keys and solutions are independently derived, not original-designation matches. Normal output repairs the matrix label and uses ordered dimensions. Source questions and learner history remain unchanged.

validate.py independently counts printed arrays and complete ordered banks, exercises all 25 shapes and both field layouts, and invokes the actual native learner grader. review.md compares originals and generated variants. capabilities.json records bounded exceptions. replenish.py rechecks current inventory under the application api.lock, uses the configured application contributor and existing EDB integration, retains exact guarded requests/receipts, and verifies at db_after. It reuses the existing generator identity or the deterministic KP generator UUID when registering it.
