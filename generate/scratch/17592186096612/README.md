# Local generator review

Run `.venv/bin/python generate/scratch/17592186096612/validate.py` from the repository root. Preview with `.venv/bin/python generate/scratch/17592186096612.py --difficulty all --seed 42 --count 2 --format markdown` (JSON is also supported).

Seven original practice cases replay through `generate`, `generate_easy` and `generate_moderate` using explicit parameters and `profile='observed'`; this includes two unrated questions assigned authored easy labels. `raw_source` is an alias for original evidence. Normal output repairs one formal operator and one stale blank alias. `generate_hard` is an authored two-base derivative/evaluation extension. Scope and all original banks are documented in classification.md and template-extraction.md. No plots, database writes, registration, engine edits or preparation.

masks.json is required extracted template data. source.json is immutable evidence. Native fixtures are transient in-memory snapshots; native-input.json and native-report.json provide actual grading results. validation.json separates exact source counts from recovered/missing source facts. review.md and review.json show originals and two parameter variants for every source family plus two authored hard examples. freeze.json hashes all delivery files after validation; avoid editing frozen artifacts during parent review. Native QA can be rerun against an output file under /tmp without modifying frozen evidence.

The exploratory zero-power domain probe is preserved separately in exploratory-native-input.json and exploratory-native-report.json; see grading-limitations.md. It is not counted as a passing equivalent-entry check. The baseline native report requires zero unresolved checks for generated/replayed valid responses.
