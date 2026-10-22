# Rank inspection generator package

`package.json` declares the complete relocatable runtime. Default difficulty is
`easy`; moderate and hard are unsupported. No images or database writes occur.

Run using Python 3.13.5 with `requirements.txt` installed:

```sh
python 17592186119848.py --difficulty easy --count 5 --seed 119848 --format json
python checks/check_runtime.py
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
generated instances. `repair-regressions.json` uses the retained event code
`legacy_packaging_or_sampling` because repair history contains no named findings.

Older reports and extraction documents in `17592186119848/` are retained history,
not current validation. Their old claim of unrated incomplete sources, implicit
empty checkbox responses, scratch paths, and publication instructions is
superseded. Do not execute `replenish.py` as part of this package workflow.
