# Triangle-complement generator repair — 2026-10-27

Deployed at EDB T8900 and verified against the live learning API.

KP `17592186105906` — Finding the Area of a Triangle Given the Area of a Quadrilateral. Topic `17592186050149` — The Area of a General Triangle.

The old reported question `17592186561416` supplied both areas, eliminating the triangle-area calculation. The registered v2.1.0 generator had repaired that particular stem for new questions, but used right angles throughout easy and moderate and supplied the method in easy. Old generated stock was still active.

## Evidence and progression

The canonical example `e-3297` uses sides 25 and 32, included angle 70°, and quadrilateral area 300: compute the enclosing triangle area, then subtract. All 12 imported practice diagrams were inspected during the preceding evidence review. Eleven records are stored as hard; `q-18192` has no difficulty or worked solution. There are no imported easy/moderate anchors. Imported labels and the incomplete record remain unchanged.

Three source examples illustrate manageable arithmetic while retaining the full task: `q-285740` has sides 6 and 4, angle 75°, quadrilateral area 10; `q-161104` has sides 9 and 7, angle 46°, quadrilateral area 17; `q-285769` has sides 6 and 2.5, angle 63°, quadrilateral area 5. Their stored labels are all hard; the numerical progression below is our authored design, not an observed upstream classification.

| Band | Numerical demand | Common task |
|---|---|---|
| Easy | One side 2 or 4, other side 4–10; small integer half-product | Sine-area calculation, then subtract the quadrilateral area |
| Moderate | Odd whole-number sides from 5, 7, 9, 11; half-integer half-product | Same |
| Hard | One half-unit decimal side from 2.5–6.5, one odd whole-number side 5–9; quarter-valued half-product | Same |

All bands give the two sides and included angle directly, allow a scientific calculator, and round only the final missing area to the nearest integer. Angles, labels, orientation, measurement units and question format vary. No enclosing area or method hint appears in the prompt. The 90° imported example is legitimate and remains untouched; authored practice uses nonright angles to retain a meaningful sine calculation. Difficulty differences are intentionally modest and have not been empirically calibrated.

## Published outcome

- Registered v3.0.0: `generators/df/dfc9c346aa5ffd2d4e03b3c1e1bed5ed888a3a71c1ce99147caf2c3ad15514a4/generator.py`.
- Retired 16 unused generated questions; retained their question, field and answer content and memberships.
- Added 15 new questions: five easy, five moderate, five hard. Live readback confirms all 15 are unused and available.
- Preserved the two used generated records, `17592186561416` and `17592186719520`, and all learner history. Existing selection excludes previously seen questions from fresh practice.
- Preserved all 12 imported practice records, the canonical example, imported coverage and other KP attributes.

New published questions:

| Question entity | Band |
|---|---|
| `17592186725424` | easy |
| `17592186725379` | easy |
| `17592186725362` | easy |
| `17592186725385` | easy |
| `17592186725352` | easy |
| `17592186725378` | moderate |
| `17592186725389` | moderate |
| `17592186725419` | moderate |
| `17592186725421` | moderate |
| `17592186725377` | moderate |
| `17592186725360` | hard |
| `17592186725353` | hard |
| `17592186725411` | hard |
| `17592186725405` | hard |
| `17592186725361` | hard |

## Verification and prevention

- Independently reconstructed arithmetic from the printed measurements, verified geometric areas and side lengths, and checked rounded distractors against their stated calculation errors: 15 delivered questions and 180 additional fresh samples.
- Reproduced all 15 records exactly through the immutable relocated package CLI.
- Native engine: 21 accepted and 42 rejected checks, including integer/decimal equivalence on free-entry questions; no unresolved checks.
- Live answer API: the same 63 checks passed, with no learner writes.
- All 15 questions rendered through the unmodified learning UI with no math or asset errors. All 15 diagrams were visually inspected using the two contact sheets; full UI screenshots 003, 007 and 011 were also inspected.
- 53 focused tests passed: triangle regression, publisher and package tests. The original supplied-area question and a reintroduced hint are negative controls.
- The publisher now checks this KP’s actual displayed measurements, calculation, numerical band, worked steps, rounding and choice separation after localization and deduplication. The package contains the same regression check.
- Author/reviewer prompts now explicitly permit a modest numerical progression with identical reasoning, and reject easy scaffolding that gives away the intermediate result or hard bands that add unrelated skills. The learning service was reloaded to use the new publication guard.

Reproduce checks with `.venv/bin/python reference/edb-math/repairs/2026-10-27-triangle-area-progression/check.py` and `.venv/bin/python -m unittest tests.test_triangle_complement_progression tests.test_generator_publish tests.test_generator_packages -q`. `deploy.py` retains the original request and exact readback; a verified rerun installs the published package without creating additional questions.

Evidence: `capture.json`, `before.json`, `fresh-source/`, `candidate-pool.json`, `generator-verification.json`, `grader-verification.json`, `render/rendering.json`, `publication/`, `verification.json`, `live-grading-verification.json`, `completion.json`. Temporary sampling and duplicate image directories were removed; the generator and check scripts reproduce them.
