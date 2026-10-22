Run from this workspace using `/home/jake/Developer/Course_Academy/.venv/bin/python`.

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python repair_checks.py
/home/jake/Developer/Course_Academy/.venv/bin/python validate_delivery.py
/home/jake/Developer/Course_Academy/.venv/bin/python 17592186119807.py --difficulty moderate --count 5 --seed 119807 --format json
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

`repair_checks.py` reads visible matrices, solves with Fraction determinants, checks all fourteen complete source banks and the corrected source arithmetic, and invokes the actual shared delivery filter on its complete test records and replacement batch. It tests the exact q-34568 target (3,4,5) versus (3,4,7), q-105166 at translation -1 with ranks 1 and 4, all ranks within every profile at fixed mathematical evidence, both residual branches, irrelevant order changes, and a small unforced sampler probe. It fails on any retained defect, including after delivery. All three retained finding IDs point to it in repair-regressions.json.

`validate_delivery.py` batches 135 acceptance/rejection checks into one call to `/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/native-input.json evidence/native-report.json`. Expected keys come from the independent visible-system oracle. It verifies inventory UUIDs and relocated execution using runtime files alone. It saves six representative render records.

Results: 14/14 complete banks, 70/70 source choices (56 distractors); 158 checked records including 16 unforced sampler cases. Native grader 135/135 responses. Five replacement records survive delivery and the old second-largest strategy answers 0/5. Every profile retains both branches and all four numeric ranks after filtering. The source five-numeric banks remain in exact replay; the shared delivery filter removes their inventory duplicates. Semantic system counts and subgroup counts are in post-delivery-shortcuts.json; bank/order variants are not counted as new systems.

Six actual UI screenshots were inspected. A subsequent fractional typography improvement changed only the fractional case; it was rerendered with:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-fraction-record.json --output evidence/render-fraction --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

The current fractional screenshot is evidence/render-fraction/question-001.png; the other five unchanged screenshots are in evidence/render/. All are readable without clipping or visible TeX errors. Runtime data, manifest, records, filtering, native grading and relocation were rechecked after that typography change.

Inventory retrospective: all 14 captured UUIDs match supplied original source questions; there are no stored generated instances in that capture. affected-inventory.json is empty for this verified reason, not because inventory was skipped. Original source questions are not classified as generated. Live learner history/policy and concurrent publication are outside this offline check; selection limitations are recorded in validation-summary.json. No database content, published images, or engine code was changed.

Current runtime manifest supersedes the legacy manifest. Existing legacy analysis in 17592186119807/ is retained for history and excluded from runtime files. Current evidence is in evidence/ and current instructional scope is in ../instructional-account.md.
