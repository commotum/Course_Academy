Commands are from the supplied workspace. PY denotes /home/jake/Developer/Course_Academy/.venv/bin/python; REPO denotes /home/jake/Developer/Course_Academy; JOB is the supplied job directory (parent of workspace). Output paths are relative to workspace. No publication or database writes.

Before editing, imported the existing entrypoint using importlib.util and called `generate('easy',941713401,profile='q-71722',parameters={'2':v,'3':4})` for v = 1, -1, 2, -2. Both unit inputs raised `ValueError: Not enough distinct same-mask entry assignments`; adjacent inputs returned full records. Exact exceptions/tracebacks and adjacent records: unit-before-repair.json. Existing checks/regression.py passed before implementation.

After implementing the repeated-value fallback:

```sh
$PY -B checks/regression.py
$PY -B checks/unit_regression.py
$REPO/generate/runs/current/check-engine evidence/unit-grader-input.json evidence/unit-grader-results.json
$PY -B $REPO/generate/pipeline/check_delivery.py --input evidence/unit-easy.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty easy --output evidence/unit-delivery-easy --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY -B $REPO/generate/pipeline/check_delivery.py --input evidence/unit-moderate.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty moderate --output evidence/unit-delivery-moderate --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY -B checks/unit_delivery.py
$PY -B checks/relocation.py
$PY -B $REPO/generate/pipeline/check_delivery.py --input evidence/batch.json --source $JOB/source/source.json --inventory $JOB/source/inventory.json --difficulty easy --output evidence/delivery-batch --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PY -B $REPO/generate/pipeline/render_preview.py --input evidence/unit-render-input.json --output evidence/unit-render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

The shared scripts were run without -B initially; -B only suppresses bytecode writing and is safe to use when reproducing. No runtime change followed their execution. check-engine was batched once per input file, never once per answer. The first post-delivery assertion caught a missing adjacent +2 counterfactual in the test input. Added that input and reran affected math, grading, and delivery checks; no acceptance check was weakened. Final counts: 63 affected records (43 easy, 20 moderate); 96 graded records with 480 selections; 6 rendered records. The 96 include 3 fixed-evidence counterfactuals, 10 source replays, and 20 ordinary samples, with some intentional repeated baselines.

Preview selection: exact ±1 q-71722 pair; q-71722 all positive/negative unit literals; q-1068 positive units; q-1051 negative units. All six screenshots were opened and inspected. Ordinary five-record batch was regenerated at seed 941713401, independently parsed, and compared against its previous complete question objects before filtering; all are identical. See batch-preservation-results.json. Older, broader validation and commands are retained in commands.md; current scoped results take precedence.
