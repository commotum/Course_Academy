# Angle bracket vector generator

Local step3–7 generator only, database math basis1356. No EDB writes, registration, engine edits or commits. Script: `../17592186059711.py`.

```sh
.venv/bin/python generate/scratch/17592186059711/validate.py
.venv/bin/python generate/scratch/17592186059711.py --difficulty all --seed 12 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186059711.py --difficulty easy --profile raw_q1304 --parameters '{"a":[12,5],"b":[9,-2]}' --format json
```

API: generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None), generate_easy, generate_moderate, generate_hard. Exact integer or rational-string input; explicit invalid parameters raise without resampling. All normal responses are supported five-choice radio vectors. Raw public source profiles preserve individually absent fields, difficulty, refs and solutions; they are evidence-only, ineligible for learners. CLI previews tolerate these omissions.

Four source prompts replay exactly, both complete captured banks reproduce all10 options, both captured solutions replay exactly, and all source attribute-presence omissions are preserved. Every original correct ref is absent: no designation fidelity or original-fixture grading is claimed. Completed records add independently inferred refs, plus authored missing fields/solutions, and are separately verified through the actual native grader. Unrated subtraction is assigned easy and the one-scaled-vector source moderate as authored difficulty claims. Hard is an authored two-scaled-vector extension within the same method, dimensions and notation.

See classification.md, template-extraction.md, source-cases.json, review.md/review.json and validation.json for provenance, bank operations, bounds, actual displayed-math validation, native grading and limitations. No plots or graphical assets occur in the assigned sources.
