# Inhibited growth identification generator

Verify from repository root:

```sh
.venv/bin/python generate/scratch/17592186124673/validate.py
.venv/bin/python generate/scratch/17592186124673.py --difficulty all --seed 42 --count 2 --format json
```

CLI arguments require spaces: `--seed 42 --count 2`. Public API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus generate_easy/moderate/hard. Four mathematical families, eleven complete profiles. Six original sources/seven original banks/five present solutions, including missing attributes and legacy duplicate field in raw observed profiles. Five authored default profiles supply all levels; easy's label/solution/correct completion is inferred, not observed. No plots or database writes. validation.json separates exact fidelity, present-designation native grading, and normal-output repairs. Native source fixtures project original designated fields because missing correct refs cannot grade.

Root QA: raw and opaque banks expose explicit evidence-only/ineligible metadata; defaults remain eligible. Review choices show present correct designations and actual difficulty labels. Excluded negative-slope IVPs must be strictly above capacity, including explicit inputs.
