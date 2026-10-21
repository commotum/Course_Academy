# Author validation commands and results

All commands ran from the workspace with `/home/jake/Developer/Course_Academy/.venv/bin/python` (3.13.5). `../source` below refers only to the supplied immutable source directory. No publication command was run. `run-checks.sh` contains the equivalent complete reproduction sequence; the commands were run in stages during development.

```
$PYTHON validate.py build
$PYTHON generator.py --difficulty easy --count 5 --seed 17592186152131 --format json > evidence/runner-sample.json
$PYTHON $REPO/generate/pipeline/check_delivery.py --input evidence/domain-records.json --source ../source/source.json --inventory ../source/inventory.json --difficulty easy --output evidence/delivery --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math
$PYTHON validate.py delivered evidence/delivery/accepted.json
$REPO/generate/runs/current/check-engine evidence/native-grader-input.json evidence/native-grader.json
$REPO/generate/runs/current/check-engine evidence/delivered-native-grader-input.json evidence/delivered-native-grader.json
```

* Source replay: 3/3 complete banks, 15/15 choices, 12/12 distractors; source prompts exact and both available source solutions exact after shared normalization. q-69158's missing fields are explicitly recorded.
* Independent exact rational-power checks: 227 template/domain points, representing 124 different (radicand,index) instances. Excludes equal-role banks, (2,4)'s duplicate wrong choices, and square x=4's division/key collision. Checks read the served prompt and solution instead of trusting generation metadata.
* Delivery: 227 input, 225 accepted, 2 captured-inventory duplicates. Both size cases, every template, all answer positions, and square decimal cases on either side of 2 survive.
* Native grader: source/boundary/controlled input: 19 accepted, 77 rejected. Delivered finite domain: 225 accepted, 900 rejected. Zero unexpected or unresolved outcomes. All five choices tested per record; extra swapped-role test rejects the former correct expression.

The same delivery command was run with these input/output substitutions:

| Input | Output | Before → accepted | Follow-up |
| --- | --- | --- | --- |
| evidence/seeded-records.json | evidence/seeded-delivery | 150 → 92 | `validate.py delivered evidence/seeded-delivery/accepted.json`; move report to seeded-delivered-variation.json; native grader 92 accepted/368 rejected |
| evidence/runner-sample.json | evidence/runner-delivery | 5 → 5 | all records independently checked; no source or batch duplicates |
| evidence/counterfactual-records.json | evidence/counterfactual-delivery | 10 → 9 | `finish_checks.py`; native grader 9 accepted/36 rejected |

The 150 raw seeded records are thirty five-question batches (seeds 0..29). Each batch has five distinct semantic instances after the without-replacement repair. Cross-batch repeats are expected and deduplicated; all declared cases and positions survive. See seeded-variation.json and seeded-delivered-variation.json for the same within-template probes before and after filtering.

```
$PYTHON finish_checks.py
$REPO/generate/runs/current/check-engine evidence/counterfactual-native-grader-input.json evidence/counterfactual-native-grader.json
$PYTHON $REPO/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/assets --math-root /media/jake/SSD/EDB/math --limit 8
```

* Five controlled pairs: swapped numeric roles (same two input numbers and complete mathematical bank, different key), changed index only, changed radicand only, changed square radicand with n fixed, irrelevant option order. All semantic instances survive delivery. Reordering alone is correctly deduplicated. Prompts, solutions and native grading agree with the changed/preserved response.
* Relocation: copy exactly the three declared runtime files into a temporary directory, clear PYTHONPATH, run from an unrelated working directory, compare five records to the original generator, replay all source cases there, and reject hard difficulty. All passed. Temporary files removed. Generator creates no assets.
* Rendering: 8/8 passed with no MathJax, font, broken-image, or JavaScript errors. The author visually inspected question-001.png through question-008.png at full height: readable indices, bases, decimal points and exponents; complete five-choice banks and solutions; no clipping or raw TeX.

# Interpretation limits

The native radio grader checks selected choice identities, not learner-entered equivalent expressions; no free entry is part of this source contract. Exact independent rational-power tests establish mathematical equivalence separately. Finite domain coverage is not 227 independent mathematical instances: the semantic count is 124 before delivery and 123 after inventory filtering. Integer-only square roots retain a justified conditional larger-base elimination; decimal cases on both sides of 2 remove it as a predictor for the whole square template. The fixed square index and numerator 1 express the taught rule. No claim of eliminating all possible mathematical elimination strategies is made.

Read-only inspection of `engine/rust/question_selection.rs` lines 133 onward shows history exclusion before selection, configured difficulty weights followed by uniform hash selection within a band, and an unconfigured first-candidate branch. No learner snapshot or active live policy was supplied. The delivery audit certifies captured-inventory eligibility, not a particular learner's eventual draw. No database content or published image changed.
