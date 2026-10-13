# KP 17592186096653

Internal segment ratio position vectors; basis 1356, topic 1106. Two layouts, 13 radio banks, 10 two-coefficient blank sources and one duplicate legacy bank. All observed levels are moderate except one explicitly assigned unrated record. Easy/hard are authored bounded ratio-arithmetic peers.

Run `.venv/bin/python generate/scratch/17592186096653/validate.py` from the repository root. CLI: `.venv/bin/python generate/scratch/17592186096653.py --difficulty all --seed 4 --count 2 --format json`. API exposes generate_easy/moderate/hard and generate(level, seed, template, field_type, parameters, profile).

Raw source banks require explicit source-ID profiles. Four erroneous blank answer-key pairs are replayed only as raw evidence; use corresponding `q-ID-repaired` profiles for corrected source instances. Normal defaults are correct authored banks. q-12212-legacy preserves its duplicate field as a single-field replay profile. Source distractor intent remains underdetermined, documented independently of exact coefficient fidelity. Observed replay parameters retain labels and permit moderate ratios up to 12. No database operations or engine changes.


Hard admission requires coprime ratio entries: both reduced numerator weights are at least 5 and the irreducible denominator is at least 19 and at most 39. Scaling an easy ratio does not make it hard. Explicit (10,10) and (20,10) regression cases reject; mathematical task identity deduplicates common ratio scaling.
