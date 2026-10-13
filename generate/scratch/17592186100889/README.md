# KP 17592186100889

Nontrigonometric Cartesian equations by parameter elimination. Steps 3–7 only; no DB writes, registration, shared engine edits, or dependencies installed.

```sh
.venv/bin/python generate/scratch/17592186100889/validate.py
.venv/bin/python generate/scratch/17592186100889.py --difficulty all --seed 42 --count 2
.venv/bin/python generate/scratch/17592186100889.py --difficulty moderate --template native_factors --format json
```

API: generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None), plus generate_easy/moderate/hard. Source cases replay via raw_observed with source_id,a=1,h=0. Normal observed defaults use repaired_observed; empirical q15653/q6828 instead use authored_method. Raw source anomalies are explicitly evidence-only and never selected as normal defaults. Native families use authored_native. All variants are deterministic and invalid explicit inputs fail.

source.json/topic.json/lesson.json preserve database/basis/lineage. source-cases.json includes every original. classification.md and template-extraction.md record classification/four extraction stages/complete banks/repairs/scope. extraction.json maps every source answer. review.md shows all originals and two generated variants per observed/native template; review.json is executable validation data. validation.json separates exact raw fidelity, normal correctness, diversity and real native grader checks. engine-input.json/engine-validation.json contain memory-only application grading evidence. q15755's missing designation remains derived, never counted as matched.
