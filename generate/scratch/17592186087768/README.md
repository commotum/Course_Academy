# Circle given center and on-circle point

Frozen script: `../17592186087768.py`. Work stops at steps 3–7; no registration,
database transaction, engine edits or shared file writes.

```sh
.venv/bin/python generate/scratch/17592186087768/validate.py
.venv/bin/python generate/scratch/17592186087768.py --difficulty all --seed 61 --count 2 --format json
.venv/bin/python generate/scratch/17592186087768.py --difficulty moderate --profile bank-q-72617 --seed 23
```

The API exposes `generate_easy`, `generate_moderate`, `generate_hard`, and
`generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None)`. Parameters require exactly h,k,u,v as exact integer or rational
values; invalid explicit calls raise ValueError. Bank profiles are complete and
chosen before sampling. All answer fields are five-choice radios.

Ordinary moderate generation selects uniformly with the seeded RNG from all
six rated source bank profiles before sampling parameters. Each selection keeps
its original worked-solution mask. Explicit profiles retain their replay
behavior; q-72616 is available only through explicit evidence/completion.
The q-54215 and q-72617 masks require perfect-square R in sampled and explicit
calls, retaining their observed square-root-to-integer radius stage. Source
parameters remain accepted and byte-exact; non-square explicit inputs for these
integer masks raise ValueError instead of printing duplicate radius rows.
The q-117096/q-117099 masks require nonsquare R with a nonunit square factor,
retaining their actual radical reduction. The q-72619/q-72621 masks require
nonsquare R and deliberately leave √R unreduced in their solutions. All guards
apply equally to explicit calls and samplers; `validation.json` quantifies each
filtered profile domain without counting bank aliases as new tasks.
`default-moderate-review.json` covers all six default profiles across seeds 0–35,
with complete displayed banks, formal operands and solution stages independently
verified and all 36 records checked by the native grader.

`source-cases.json` replays all seven practice sources through the public API.
`source.json` preserves the original capture and provenance. Six source
solutions, all seven prompts and all 35 answer strings are reproduced exactly;
all six original correct designations match. q-72616's missing difficulty,
solution and correct ref remain absent in raw replay, which is evidence-only.
An independently derived authored completion is in `completed-incomplete.json`.
That completion uses an integer-radius mask for square R and an unreduced
radical mask otherwise, avoiding duplicate radius rows without inventing a
captured source solution.
No unsupported full-equation blank is introduced or asserted to grade.

Easy and hard are explicit authored scopes documented in classification and
the script. `review.md` and `review.json` contain two changed examples for every
source bank and two for each authored level; correct choices are review labels.
`validation.json` separates fidelity, independent displayed math, native grader
checks and source incompleteness. Native checks use the real application's
`learning::grade_field` through the memory-only shared check-engine executable.
Source metadata deficiencies remain documented; no missing source designation
is counted as matched.

Content IDs include the full displayed prompt, fixed solution, difficulty and
complete bank; ordering and seed do not change IDs for fixed content. Task
fingerprints use the center and given point, excluding bank/profile/notation
aliases. No answer choices or metadata belong in learner-facing pre-submission
views. Local UUID/enum strings are review records, not transaction EDN.
