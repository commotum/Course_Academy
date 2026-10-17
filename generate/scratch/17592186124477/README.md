# Pivot columns of a REF matrix

Validated easy checkbox generator: `generate/scratch/17592186124477.py`, version `pivot-columns-ref-checkbox-2`. Each displayed matrix column has its own field (`Column 1`, `Column 2`, ...) and owned `false`/`true` answers. Moderate/hard exceptions and the 40-task structural bound are unchanged in capabilities.json.

The authorized 2026-10-16 update preserves every original matrix, solution, difficulty and correct subset, while adding “Select all that apply.” Source captures and the original radio review remain historical evidence. Current source replay, sampling preservation, review examples and native grading are in [checkbox-update-2026-10-16](checkbox-update-2026-10-16/verification.json).

```sh
.venv/bin/python generate/scratch/17592186124477.py --difficulty easy --count 5 --seed 19 --format json
.venv/bin/python generate/scratch/17592186124477.py --profile q-73607 --seed 19 --format markdown
.venv/bin/python generate/scratch/17592186124477/validate.py
```

Python and SymPy versions are retained with each instance. Validation uses the existing check-engine executable to test the actual application grader for both Boolean answers of every column. The generator itself performs no database operations. `replenish.py` retains the prior inventory job's recovery workflow and captured-state guards; the checkbox update does not execute or repurpose that historical job. Original source records and learner history are immutable inputs to this package.
