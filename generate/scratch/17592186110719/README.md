# Infinitely many solutions: identity classification

Run `.venv/bin/python generate/scratch/17592186110719/validate.py`.
Preview `.venv/bin/python generate/scratch/17592186110719.py --difficulty all --seed 12 --count 2 --format markdown`.

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`
and the three `generate_easy`, `generate_moderate`, `generate_hard` wrappers.
Templates are direct (easy), one_distribution (moderate), two_distributions (hard).
All levels emit three Boolean checkbox fields keyed I, II and III. The prompt
labels each equation and says “Select all that apply.” An empty selection means
none of the equations is an identity; there is no separate None checkbox.

The historical basis1356 snapshot has five easy source questions with combination
radio answers. Version `affine-identities-checkbox-4` preserves their equations,
correct subsets and full worked solutions while converting the response format.
The four source profiles remain sampling policies at all levels: they choose an
identity subset before sampling equations. Explicit parameters accept every
subset under any profile, and profile names do not affect question identities.
`field_type` accepts only `None`, `checkbox`, or `:answer-field.type/checkbox`.
Moderate/hard are explicitly
authored prerequisite-supported distribution variants of the same identity
classification skill. No unknown parameters, systems, plots, engine changes or
database writes occur. All normal profiles enforce level bounds on explicit
parameters and the actual reduced objects.

`source.json` is the retained historical wrapper, `source-cases.json` provides public
API replay inputs, `review.md` and `review.json` show originals and generated
variants for every profile and level, and validation separates source fidelity,
independent printed mathematics and real application checkbox grading. Validation
also replays the two questions converted on 2026-10-16 (I; I and II), checks all
eight subsets at each difficulty, and rejects the obsolete radio API request.

Existing `reference/` and `replenish.py` are historical artifacts from the prior
run, outside this generator workflow; this update neither imports nor executes
them. The live registration uses the repository script directly; see
`checkbox-update-2026-10-16/registration.json`. This fix needs no database writes
and does not change already served questions or learner state.
