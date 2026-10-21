All commands ran from this workspace. No publication or database operation was run.

```sh
JOB=/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186068844
REPO=/home/jake/Developer/Course_Academy
PY=/home/jake/Developer/Course_Academy/.venv/bin/python
PYTHONDONTWRITEBYTECODE=1 "$PY" checks/reproduce-shortcut.py
# Before implementation: exit 1; evidence/before-minimal-failure.json.
# After implementation: exit 0; evidence/minimal-failure.json.
PYTHONDONTWRITEBYTECODE=1 "$PY" checks/validate_repair.py
# Exit 0: 11 exact source banks, 13 controlled families, 109 math records,
# 344 evaluated solution rows. Writes complete records and grader cases.
PYTHONDONTWRITEBYTECODE=1 "$PY" checks/inventory.py
# Exit 0: 10/10 captured non-source generated questions replay and expose old cue.
"$PY" 17592186068844.py --difficulty easy --count 5 --seed 829331 --format json > evidence/samples.json
"$REPO/generate/runs/current/check-engine" evidence/grader-input.json evidence/grader-report.json
# Exit 0: 122 accepted, 436 rejected, no unresolved.
"$PY" "$REPO/generate/pipeline/check_delivery.py" --input evidence/delivery-input.json --source "$JOB/source/source.json" --inventory "$JOB/source/inventory.json" --difficulty easy --output evidence/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
# Exit 0: 99 input, 1 duplicate, 98 accepted; all 11 matched role groups survive.
PYTHONDONTWRITEBYTECODE=1 "$PY" checks/probes.py
# Exit 0: old unique-key shortcut has zero hits; six visible-choice policies
# each score exactly 1/5 on matched groups before and after delivery.
PYTHONDONTWRITEBYTECODE=1 "$PY" checks/packaging.py
# Exit 0: declared runtime files run from /tmp after relocation; five records identical.
"$PY" "$REPO/generate/pipeline/render_preview.py" --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
# Exit 0: five previews. Visually inspected screenshots 002,003,004,005.
"$PY" "$REPO/generate/pipeline/render_preview.py" --input evidence/render-final-records.json --output evidence/render-final --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
# Exit 0: corrected domain-clause punctuation; final screenshot visually inspected.
```

`delivery-input.json` contains all easy records from `test-records.json`; the 10 polynomial moderate/hard records are excluded by the requested easy band. The native grader tests all 109 records, then 13 option-order counterfactuals. Source banks are compared with the supplied source capture, not a copied expected table. Independent math parses the displayed prompt and equations. Complete matched-bank groups establish that even an unenumerated choice-only policy has no invariant key: every visible equation is correct for one of the five otherwise matched ODEs.
