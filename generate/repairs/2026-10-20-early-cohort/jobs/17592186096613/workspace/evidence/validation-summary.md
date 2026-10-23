# Repair validation

Finding `6bbaf15dc6703e79f686` is repaired in the existing package. The original unit-fraction call failed before the change (original-failure.json); the retained reviewer reproduction and the stronger executable regression now pass. No historical runner batch was edited.

Fidelity: all 11 supplied source questions replay exact prompts, solutions where supplied, original rating presence, and all 10 complete answer banks. The new quotient uses its source's five-stage rewriting solution and complete radio bank. The old nonunit-numerator condition is now bank-specific; it remains where removing it would create duplicate choices.

Correctness: independent parsing of visible functions, keys, all solution equalities, and full answer banks passed for 84 records before delivery and 58 surviving records. The focused delivered sample retains 22 distinct derivatives, covering both signs and all denominators 2..12. There is no claim that shuffles or changed UUIDs increase semantic diversity.

Grading: the real native `learning::grade_field` passed 212 accepted and 535 rejected responses, with no unresolved outcomes. Tests include every radio option, equivalent unit-fraction blank expressions, incorrect derivatives, and stale answers after relevant counterfactual changes.

Decision variation: seven controlled pairs exercise denominator, sign, coefficient, and answer-order changes. Within quotient cases all five answer positions occur; both signs and all denominators survive filtering. For the other retained families, observed positions and derivatives vary. A positive sign is not a complete selection heuristic in the positive fraction bank because every choice there is positive. Likewise, the report's positive-key counts describe sign exposure rather than successful selection of a unique positive option. Fixed single-answer cardinality follows the radio response contract. The intended rule is to carry the signed constant through D(ln x)=1/x; direct use of this rule is not an incidental shortcut.

Delivery: the exact requested CLI batch (`--difficulty easy --count 5 --seed 3129290382 --format json`) has five accepted records, including three different quotient cases with both signs. The retained checks inspect both the prospective batch and accepted array. Broader focused input has 79 records, 53 accepted after content deduplication. Selection code was inspected read-only: with positive easy weight, fresh usable candidates within easy are sampled uniformly; actual learner history and policy were not provided.

Rendering: shared unmodified UI renderer passed five quotient examples; positive and negative screenshots were visually inspected. Original denominator 4, negative denominator-2 example, choices, and all five worked rows are legible and unclipped. The final source-basis-only metadata change does not alter rendered question content.

Packaging: only the four declared runtime files were copied into a relocated directory. The requested CLI reproduced the current batch exactly. Installed Python 3.13.5 and SymPy 1.14.0 match the manifest and pinned requirements. No generated assets are required. Existing authored nonrequested moderate/hard behavior is preserved but not newly certified by this easy repair.

Inventory: inspected all 12 captured entries for identity, response completeness, and retirement attributes. The reported omission is not corrupt stored content. No affected stored record was demonstrated; affected-inventory.json is empty. This does not claim a fresh exhaustive audit of all historic content. No publication, database changes, or edits outside the workspace occurred.

Commands (run from the workspace):

```sh
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python checks/reproduce_source_gap.py --package . --output evidence/source-gap.json
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python checks/quotient_regression.py
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python checks/quotient_regression.py --input evidence/prospective-batch.json
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python checks/quotient_regression.py --input evidence/delivery-prospective-batch/accepted.json
/home/jake/Developer/Course_Academy/generate/runs/current/check-engine evidence/grader-input.json evidence/grader-report.json
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python /home/jake/Developer/Course_Academy/generate/pipeline/render_preview.py --input evidence/render-records.json --output evidence/render --asset-root evidence/assets
PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python checks/package_check.py
```

The retained regression runs `check_delivery.py` itself on current generated output with the supplied source and inventory snapshots. Full reports, current records, and exact filtering implementation hashes are in the evidence directory. The original reviewer script is retained separately; the registered regression uses independent visible-math witnesses and fails immediately if current unit-fraction support disappears.
