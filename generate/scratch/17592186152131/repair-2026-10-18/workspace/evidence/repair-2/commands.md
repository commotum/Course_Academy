# Current repair reproduction and results

Run from the supplied workspace:

```sh
bash run-repair-checks.sh
```

`run-checks.sh` delegates to this current sequence. The script uses the job Python (`/home/jake/Developer/Course_Academy/.venv/bin/python`, 3.13.5), shared `check_delivery.py`, native `check-engine`, and shared `render_preview.py`. All outputs are below `evidence/repair-2`. It never publishes or opens the database. Read `instructional-account.md` for the final specification. Older `evidence/*` outside repair-2 are retained first-pass evidence and are superseded for repaired practice behavior.

The sequence was run in stages. After the base-frequency repair the complete sequence passed. Subsequent changes added the same-bank target counterfactual, explicit immutable-source comparison, alternate-base rendering examples, and one seeded gap case. Affected build/delivery/native checks and rendering were rerun, as follows:

```sh
$PYTHON repair_checks.py build
$PYTHON $REPO/generate/pipeline/check_delivery.py --input evidence/repair-2/test-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/repair-2/delivery --asset-root evidence/repair-2/assets --math-root /media/jake/SSD/EDB/math
$PYTHON $REPO/generate/pipeline/check_delivery.py --input evidence/repair-2/bank-counterfactual-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/repair-2/bank-counterfactual-delivery --asset-root evidence/repair-2/assets --math-root /media/jake/SSD/EDB/math
$PYTHON repair_checks.py delivered
$REPO/generate/runs/current/check-engine evidence/repair-2/native-grader-input.json evidence/repair-2/native-grader.json
$REPO/generate/runs/current/check-engine evidence/repair-2/delivered-native-grader-input.json evidence/repair-2/delivered-native-grader.json
COURSE_ACADEMY_VALIDATION_EVIDENCE_DIR=evidence/repair-2 $PYTHON finish_checks.py
$REPO/generate/runs/current/check-engine evidence/repair-2/counterfactual-native-grader-input.json evidence/repair-2/counterfactual-native-grader.json
$PYTHON $REPO/generate/pipeline/render_preview.py --input evidence/repair-2/render-records.json --output evidence/repair-2/render --asset-root evidence/repair-2/assets --math-root /media/jake/SSD/EDB/math --limit 7
```

The complete script also filters the ten original controlled records (9 survive; irrelevant reorder deduplicated), ten new bank/target counterfactual records (10 survive), and requested five-record runner-seed sample (5 survive). All native grader inputs batch every response into one process per suite.

Results:

- Fidelity: immutable source correspondence exact; 3/3 banks, 15/15 choices, 12/12 distractors; both captured solutions match after shared normalization. Missing q-69158 fields explicitly inferred/documented.
- Correctness: exact rational-power equivalence independently verifies prompt, all five choices, unique key, distinct choices and solution for all 336 affected square configurations, 35 ordinary regression records, source and controlled cases. The square configurations represent 21 numerical tasks, not 336 numerical tasks. Indexed runtime behavior is unchanged and earlier full-domain evidence is retained.
- Delivery: 371 inputs, 358 accepted, 13 duplicates; all 336 square configurations survive. Inventory basis 3777. Ordinary sample has every foil index, both base directions and both inverted-base assignments. Seed 7 was added specifically because the initial 30-item regression omitted denominator 3.
- Decision variation: the exact reported first-match strategy succeeds 87/336 after filtering (integer 48/192; decimal 39/144), versus 100% in review. Most-frequent-base among half-powers succeeds 168/336. Fixed-position and rank probes and conditional groups are in raw-variation.json/delivered-variation.json; none of the asserted incidental probes is perfect. Same-bank sqrt(7)/sqrt(8) target swap changes prompt/key/solution; old key is actually rejected. Eight irrelevant bank changes preserve response and solution; all survive delivery.
- Grading: raw/source/controlled suite 394 accepted, 1577 rejected; delivered suite including shortcut attempts and new counterfactuals 455 accepted, 1722 rejected; original controlled-delivery suite 9 accepted, 36 rejected. No unexpected/unresolved outcomes.
- Packaging: exact manifest/runtime hashes, Python version, deterministic relocation, source replay after relocation and unsupported hard-band rejection pass. No runtime external paths/imports, generated assets, database writes or publication.
- Rendering: seven application UI records passed; all screenshots inspected, including the two changed lower-base/other-inversion cases. See visual-inspection.json. No clipped content, broken math or unreadable decimal/exponent notation observed.

Limits: native grading assesses radio identities, while exact independent math establishes answer truth. The finite domain is intentionally bounded; no claim of eliminating all mathematical elimination strategies. Captured delivery does not simulate live learner history, configured weights, future database IDs or publication. Read-only selector inspection confirms positive-weight band selection is uniform over eligible IDs; history can remove cases and unconfigured policies use the first candidate.
