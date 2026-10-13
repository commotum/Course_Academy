# Challenging integer-coefficient substitution systems

Run from repository root:

```bash
.venv/bin/python generate/scratch/17592186073753/validate.py
.venv/bin/python generate/scratch/17592186073753.py --difficulty all --seed 12 --count 2 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`.
Default profile `method` creates valid five-choice radio assessments. All levels
are author-designed because the three captured originals are unrated. Source
profiles are explicit empirical replay, not recovered authoring algorithms.
`source_q12457_raw` is incomplete evidence with five wrong options and no correct
ref; `source_q12457_repaired` is the supported minimal bank repair. Raw anomalies
are documented, never silently counted as valid native assessments.

Validation independently reads the printed equations, all isolate/substitute/
distribute/collect/back-substitute rows, final tuple or scalar and complete banks.
It also checks source fidelity, level guards, content identities, genuine task
variety, source malformed-brace repair and real application native grading.
`source.json` and `authoritative-lesson-487.json` preserve raw evidence. See
`validation.json`, `review.md`, `source-choice-map.json` and extraction documents
for fidelity counts and limitations. No plots, database writes or registration.
