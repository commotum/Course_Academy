# KP 17592186119806 generator

The current package entry point is `../17592186119806.py`; its runtime file list and exact Python/SymPy versions are in `../package.json`. From the supplied workspace, use the declared Python environment:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python 17592186119806.py --difficulty easy --count 5 --seed 48291 --format json
/home/jake/Developer/Course_Academy/.venv/bin/python checks/validate_repair.py
```

The repaired v2 design is specified in `../instructional-account.md`. Current checks and evidence live in `../checks/` and `../evidence/`; `../repair-regressions.json` binds both retained findings to executable checks. The capture now includes all 14 complete easy source banks, including q-105158, at basis 5402. Exact source replay uses `generate('easy', seed, profile, {'scale': 1, 'target': original_target})`. Normal sampling uses authored interchangeable candidate banks and derives compatible vector data, replacing the old fixed affine bank transformation. Only easy is supported.

The other extraction notes, validation reports, and maintenance helpers in this subdirectory are retained historical v1 material. In particular, old finite-capacity and affine-bank claims are superseded by the current instructional account. They are excluded from the runtime package. Publication is reserved for the runner after independent review; legacy replenishment helpers were not used in this repair.
