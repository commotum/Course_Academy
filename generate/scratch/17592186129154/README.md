# Polynomial graph statement generator

Run `.venv/bin/python generate/scratch/17592186129154/validate.py` from the repository root. Preview with `.venv/bin/python generate/scratch/17592186129154.py --difficulty all --seed 37 --count 2 --format json`.

API: `generate_easy`, `generate_moderate`, `generate_hard`, or `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`. Template names are source MA IDs or `mixed_categories_four_roots`. `source:<template>` preserves missing source fields/solutions/correct refs; `repaired:<template>` derives missing supported data and is normal presentation. Parameters are `roots`, `multiplicities`, `coefficient`, validated without silent repair. Complete banks are chosen before sampling and never pooled.

Ten raw source replays, nine original complete banks/45 choices, seven original correct designations and eight original solution sequences are covered. Two unrated records receive explicit authored easy assignments; the fieldless moderate record receives an authored bank for normal presentation; hard is one authored family supported by the canonical and ordered lesson. No DB/engine/shared edits or registration. Root QA is required independently.

See `classification.md`, `template-extraction.md`, `plot-extraction.md`, `source-cases.json`, `review.md`/`review.json`, and `validation.json`. Original graph equations/amplitudes/exponents are generally opaque. Renderer representatives preserve observable categories; incidental magnitude/exponent changes never inflate task fingerprints. Native grader results are separate from original-bank and mathematical fidelity.
