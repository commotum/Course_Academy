Run from the supplied workspace. No command publishes, contacts a service, or writes database content.

Initial exact reproduction (before runtime edits; failures retained):

```sh
python3 ../review-0-policy-2-95271fa8a661a89b/strict-regression.py "$PWD" > evidence/before-none.txt 2>&1
python3 ../review-0-policy-2-95271fa8a661a89b/strict-source-regression.py > evidence/before-source.txt 2>&1
```

Current source, mathematical, historical-inventory and retained-findings checks:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python checks/repair_check.py
```

Result: all 11 complete captured banks; all captured keys where present match the independent oracle. First three missing source keys/solutions/difficulty are explicitly recovered. The original seed 827461 is exercised, plus its exact old sqrt(0), Z+, Q-, Z-, N counterexample regardless of the seed's changed profile mapping. Five relevant/irrelevant counterfactual pairs pass, including the zero boundary, roots, decimal classification and universal target classes. All 16 ordinary checkbox patterns use distinct mathematical banks. One fixed 180-record production sample covers all six number/class profiles, all five bank profiles, all five finite-decimal classes, and all 20 radio-bank correct choices. This bounded sample was used to test within-profile cues, not to count cosmetic variations. Retained history IDs are all bound to this runnable script in repair-regressions.json.

Actual delivery and post-filter variation:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/check_delivery.py --input evidence/delivery-input.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
/home/jake/Developer/Course_Academy/.venv/bin/python checks/stage_check.py
```

Result: 220 input, 10 duplicates skipped, 210 accepted. All 16 checkbox patterns and all 20 radio-bank outcomes survive. Thirty representation/bank subgroups each vary their final correct response. The script reports fixed subset strategies, authored correct-choice positions, correct counts, and UI radio choice-order positions for content/item IDs 1, 2 and 3 using the actual learning.js FNV ordering rule. No subgroup has a constant final response or a constant UI radio ordinal under those probes, before or after delivery. Mathematical symbols, including universal C membership for real targets, carry intended lesson meaning. The source radio banks restrict possible subsets; no claim of all 16 subsets for radio banks is made. Live policy and learner history are unavailable, so actual learner exposure is not certified.

Native learner grader (one batch; expected values from the visible-content oracle):

```sh
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-results.json
```

Result: 488 accepted and 944 rejected response checks, no unexpected or unresolved outcomes, no database operations. Every authored choice in the source replays, sampled records, truth patterns and controlled pairs is tested, including rejection of the all-unchecked response in the repaired zero case.

Relocation and dependencies:

```sh
/home/jake/Developer/Course_Academy/.venv/bin/python checks/package_check.py
/home/jake/Developer/Course_Academy/.venv/bin/python generator.py --difficulty easy --count 5 --seed 827461 --format json > evidence/sample-five.json
```

Result: exact Python 3.13.5; standard library only; seeded output identical after relocation using only package.json files, all eleven source replays work, invalid band/count fail, no assets required or written.

Actual Learning UI:

```sh
python3 /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
```

Result: six successful renders, no MathJax errors/broken images/dangling glyphs. Screenshots question-001.png through question-006.png were individually inspected: four complete radio banks, a correctly selected None with matching conclusion, and a restored source bank with false None between ordinary fields. The UI shows readable symbols, selected controls and full worked solutions without clipping/overlap.

Historical inventory: checks/repair_check.py reconstructs all five generated inventory records with the preserved pre-repair constructor, validates their content fingerprints and publisher UUIDs, and saves complete captured records with reproduction parameters and entity/basis metadata. Exactly one stored generated question has an empty correct subset: UUID 6e7f7e59-12b8-5d8f-a27b-48f0bd02db19, entity 17592186624696. Its old implicit-empty explanation agrees with its old empty key; the source-backed explicit-None replacement is saved separately in replacement-proposals.json and was not applied. No stored instance of the newer contradictory explicit-None solution was present among the five captured generated questions. Original source questions were examined for fidelity only, never relabeled generated. Historical sampling seeds were not captured; exact mathematical parameters reproduce their full content and published identities. affected-inventory.json uses ../workspace/evidence/generated-records.json relative to the requested author-1 evidence root because all author writes are restricted to this workspace.
