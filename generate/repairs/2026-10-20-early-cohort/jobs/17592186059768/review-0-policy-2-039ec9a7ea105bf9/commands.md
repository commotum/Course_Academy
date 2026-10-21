Reproduction commands (run from this evidence directory; all tools are read-only with respect to the package and database):

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B audit.py
# audit.py also invokes reproduce_inventory.py for exact historical replay
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-input.json grader-results.json
/home/jake/Developer/Course_Academy/.venv/bin/python -B variation_audit.py
```

`variation_audit.py` intentionally exits 1 on the fixed-corner family regression. Its failure is saved in regression-command.log and regression-results.json. It permits source instances with a useful sign simplification; the failing criterion is that the same shortcut succeeds throughout the independently sampled recognizable family.

The shared delivery command was run for each tuple `(input, difficulty, output)`:

- `(independent-easy.json, easy, delivery-easy)`
- `(independent-moderate.json, moderate, delivery-moderate)`
- `(runner-batch.json, easy, delivery-batch)`
- `(delivery-duplicate-input.json, easy, delivery-duplicate)`

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input INPUT --difficulty DIFFICULTY --output OUTPUT --source /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186059768/source/source.json --inventory /home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186059768/source/inventory.json --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-input.json --output render --asset-root delivery-batch/assets --asset-root delivery-moderate/assets --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input render-remaining-input.json --output render-remaining --asset-root delivery-moderate/assets --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python -B finish_report.py
```

The renderer defaults to six records. First invocation inspected records 1–6 of render-input.json; the second uses its final four records as render-remaining-input.json. Together they cover all five exact batch members, three controlled-pair records, and both moderate profiles.

Initial source-analysis.json was written and verified before reading the package. Source analysis was subsequently corrected only to remove a mistaken inference about doubled backslash encoding; no captured TeX defect is asserted. repair-history.json, repair-preflight.json, and publication/preparation.json did not exist. There was no previous review to reuse.

Inventory basis 5352 has ten original source questions and seven previously generated questions. `reproduce_inventory.py` reconstructs complete historical records using original instructional templates at archived parameters and current generated matrix banks. It restores historical field/answer UUIDs by exact answer-value correspondence with the original archived generated records. It does not copy stored question content. Publisher normalized-question comparison then verifies exact prompts, worked solutions, full banks, keys, and all identities against captured inventory. Display-dollar whitespace differs from current generator normalization in two profiles; the historical template presentation is preserved for exact reproduction. `generated-records.json` retains exact archived generation metadata. `affected-inventory.json` lists only these seven demonstrated generated records, never original source questions. Standalone reproduction: `/home/jake/Developer/Course_Academy/.venv/bin/python -B reproduce_inventory.py`.
