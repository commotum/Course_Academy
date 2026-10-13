# Vertex-coordinate parallelepiped volume

One exact-arithmetic generator with easy/moderate/hard entrypoints, six observed solution/layout families, public normal/raw source profiles, and separate authored complete method banks. Only this script and private evidence folder are written; no DB operations or registration.

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186105909/build_specs.py
.venv/bin/python generate/scratch/17592186105909/build_notes.py
.venv/bin/python generate/scratch/17592186105909/validate.py
.venv/bin/python generate/scratch/17592186105909.py --difficulty all --count 2 --seed 42 --format markdown
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). Parameters contain exactly points: four integer triples. Source-cases list original parameters and public raw profiles. Raw preserves missing fields of metadata and one known erroneous teaching row; normal profiles provide supported repairs. validate.py independently reads actual displayed mathematics, compares complete source payloads and uses the native grade_field harness; scalar source distractor intent and authored missing-level claims are documented separately. The review contains originals, normal replay, dilation/translation variants of every source profile, and two radio plus two blank examples for each level.
