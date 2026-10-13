# Segment one-form generator

Local review only, database math basis 1356. Nothing is registered or transacted.

```sh
.venv/bin/python generate/scratch/17592186179728/validate.py
.venv/bin/python generate/scratch/17592186179728.py --difficulty all --seed 7 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186179728.py --difficulty easy --template q-124663 --profile q-124663_observed --seed 8 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Only source-shaped radio fields are supported. Explicit inputs reject invalid scopes and whole ambiguous banks; samplers resample the whole question.

Nine complete observed banks reproduce through explicit scalar-multiplier profiles; their wrong-answer intent remains unresolved and they are **not** the default. Normal defaults use operation-derived complete banks. Easy defaults also vary endpoints/coefficient forms; moderate/hard are authored within the same line-segment differential-sum method. See classification for precise bounds and rationale. Observe the separately reported raw/repaired q-124663 endpoint typo.

`texmath.py` independently reads actual displayed endpoints, one-forms, vector parameterization, limits, derivatives, each integrand, antiderivative and endpoint/scalar row. `validate.py` compares all original prompts/banks/full prose/stage sequences, tests explicit bounds and identity, rejects deliberately corrupted display stages, and invokes the existing native grader with every selected option. Full engine records are in engine-input/engine-validation.json. Review artifacts contain nine originals, replay profiles and generated authored variants for each level. Plots are absent, so no renderer is needed.

Authored endpoint evaluation retains each separately evaluated primitive term, including zero terms at the starting endpoint, as an unevaluated component sum before the final scalar collection. The validator checks the ordered component masks and rejects a same-value collapsed endpoint row.
