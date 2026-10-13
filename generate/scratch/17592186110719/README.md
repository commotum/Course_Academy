# Infinitely many solutions: identity classification

Run `.venv/bin/python generate/scratch/17592186110719/validate.py`.
Preview `.venv/bin/python generate/scratch/17592186110719.py --difficulty all --seed 12 --count 2 --format markdown`.

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`
and the three `generate_easy`, `generate_moderate`, `generate_hard` wrappers.
Templates are direct (easy), one_distribution (moderate), two_distributions (hard).
Four complete observed radio profiles remain available at all levels.

The basis1356 snapshot has five easy source questions, one selection radio field
per question and five choices per field. Five full prompts/solutions, twenty-five
choices and twenty distractors replay exactly. Moderate/hard are explicitly
authored prerequisite-supported distribution variants of the same identity
classification skill. No unknown parameters, systems, plots, engine changes or
database writes occur. All normal profiles enforce level bounds on explicit
parameters and the actual reduced objects.

`source.json` is the current captured wrapper, `source-cases.json` provides public
API replay inputs, `review.md` and `review.json` show originals and generated
variants for every profile and level, and validation separates source fidelity,
independent printed mathematics and real application radio grading.
The older checkbox-only scratch evidence and unsupported-level claims have been
superseded by these artifacts.

Existing `reference/` and `replenish.py` are historical artifacts from the prior
run, outside this generator workflow; this rebuild neither imports nor executes
them. Current evidence is the basis1356 source wrapper and the named validation
and review files above.
