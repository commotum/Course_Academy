# Rank inspection generator package

`package.json` declares the complete relocatable runtime. Default difficulty is
`easy`; moderate and hard are unsupported. No images or database writes occur.

Run using Python 3.13.5 with `requirements.txt` installed:

```sh
python 17592186119848.py --difficulty easy --count 5 --seed 119848 --format json
python checks/check_runtime.py
python checks/check_batch_decisions.py
python checks/validate_content.py
python checks/check_delivery_variation.py
python checks/audit_inventory.py
```

The checks use the job's supplied source and inventory plus the repository's
read-only delivery filter and native learner grader. Only runtime files listed
in the manifest are needed after relocation. `checks/` and `evidence/` are review
materials, not runtime dependencies. The compatibility validator at
`17592186119848/validate.py` runs the current content check.

Read `instructional-account.md` for source evidence, allowed variation and
source-backed extensions. Current results live in `evidence/validation.json`,
`evidence/source-replay.json`, `evidence/pedagogical-variation.json`, and
`evidence/visual-review.json`. `affected-inventory.json` is empty; the separate
inventory audit explains the two incomplete originals and absence of stored
generated instances. `repair-regressions.json` retains the import event code
`legacy_packaging_or_sampling` and batch shortcut finding
`6900891930e4bdc756fa`.

The targeted batch-selection repair and current results are in
`evidence/repair-2/verification.md` and `evidence/repair-2/batch-regression.json`.
The exact prior failing batch remains a negative control. Repeated profile
decisions now share a visible subgroup and vary every eligible qualifying label.
Source banks, mathematical construction and semantic capacity are preserved.

Older reports and extraction documents in `17592186119848/` are retained history,
not current validation. Their old claim of unrated incomplete sources, implicit
empty checkbox responses, scratch paths, and publication instructions is
superseded. Do not execute `replenish.py` as part of this package workflow.
