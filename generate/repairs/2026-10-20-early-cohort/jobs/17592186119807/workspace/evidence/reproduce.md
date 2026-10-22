Current second-repair evidence (supersedes earlier completion counts):

Run from this workspace with `/home/jake/Developer/Course_Academy/.venv/bin/python`:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python repair_checks.py
/home/jake/Developer/Course_Academy/.venv/bin/python batch_checks.py
/home/jake/Developer/Course_Academy/.venv/bin/python validate_delivery.py
/home/jake/Developer/Course_Academy/.venv/bin/python batch_regression.py
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/sign-repair/render-records.json --output evidence/sign-repair/render --asset-root evidence/sign-repair/assets --math-root /media/jake/SSD/EDB/math
```

`repair_checks.py` retains the three earlier findings: all fourteen complete source banks (70 choices, 56 distractors), both consistency branches for every profile, the exact c/d target flip, all four numeric ranks, boundary arithmetic, irrelevant choice ordering, and shared delivery checks. It passes 158 checked records. Source q-105163's previously documented arithmetic correction remains intact. Source evidence and item construction have not changed in this repair.

`batch_checks.py` retains finding a78c7e8e37b394728e63 and adopts the reviewer's exact visible-bank assertion in `batch_regression.py`. It first requires the original captured five-item pool to fail that assertion with 3/3 nonpositive banks keyed No solution. See sign-repair/original-failure.json and original-records.json. The exact minimal generator call remains reproducible. Changing only its decisive target residual yields the correct sum -4 with the same all-negative bank; both records are in sign-repair/controlled-records.json.

For every source profile, the new sign controls change the bank's sign class while holding the complete mathematical prompt and worked solution fixed, and test both consistency outcomes. All 58 controlled records survive the shared delivery filter; these represent 30 distinct vector systems (bank changes are not counted as new systems). Four unforced CLI batch seeds (0, 1, 119807, 291807) each return five distinct systems. Every pool retains both consistency outcomes under both sign conditions after normalization and inventory deduplication. Repeated name, coefficient-profile, all-negative, zero-containing, mixed-sign and fractional subgroups do not predict consistency, and the numeric keys vary in rank. See sign-repair/batch-results.json and delivery-*/delivery.json. Singleton groups do not establish conditional coverage; controlled family tests supply that evidence. In-memory sampling trace and its limitations are in sign-repair/resampling.json.

Runtime batches of at least five now sample the necessary sign/consistency witnesses first, fill other slots normally, reject incidental predictors and shuffle output order. Counts below five retain ordinary sampling and make no finite-pool coverage guarantee. No source profiles or legitimate sign patterns were removed. Future inventory or learner history can remove witnesses, so a newly filtered pool requires another acceptance check.

`validate_delivery.py` passes 49 native grader cases / 245 radio responses, using independent Fraction solutions of visible vectors to choose expected acceptance and rejection. This includes the exact negative-bank counterfactual and all twenty delivered CLI records. Relocated execution of only the four manifest runtime files matches the current five-record CLI output. Dependencies match installed Python 3.13.5 / SymPy 1.14.0.

All six new actual-UI screenshots were visually inspected: the exact replacement pool at seed 119807 and the all-negative consistent counterexample. No visible TeX errors, clipping or broken assets. See sign-repair/render-inspection.json and sign-repair/render/rendering.json. Earlier unchanged screenshot evidence remains available separately.

Inventory: all fourteen captured questions match original source UUIDs; there are no stored generated instances in the supplied inventory. evidence/affected-inventory.json is empty for this verified reason. No original source question was marked generated. Live inventory and learner history were not queried; question_selection.rs selects within difficulty and does not enforce subgroup coverage. No database writes, engine changes, image publication, or edits outside the workspace occurred.

All four history finding IDs are wired to executable tests in repair-regressions.json. Runtime hashes are in evidence/runtime-hashes.json. The runtime manifest excludes tests, evidence and legacy analysis under 17592186119807/; current instructional scope is ../instructional-account.md.
