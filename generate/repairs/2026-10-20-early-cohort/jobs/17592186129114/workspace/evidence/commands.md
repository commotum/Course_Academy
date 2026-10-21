# Reproduction

Run from the supplied workspace, with bytecode writes disabled:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python checks/regression_pool.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python checks/validate_repair.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python checks/shortcut_probes.py
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root . --math-root /media/jake/SSD/EDB/math --limit 4
```

`commands.log` retains the exact delivery and batched native grader commands and
their output/status. `regression_pool.py` invokes the historical strict probe and
requires its failure, then tests newly generated current-code batches and requires
the same strict probe to pass after actual shared delivery filtering. The
registered finding check does not accept copied historical keys as evidence that
the current generator is repaired.

The retained original delivered batch and C counterexample were copied from
review-0-policy-2-342253086f871c08. They remain immutable input witnesses. The
preservation check reads that review's captured per-profile records and compares
two per profile to current individual generation; it does not rerun the original
416-record audit. All active implementation, evidence, and generated UI files
are inside this workspace; no publication or database commands run.
