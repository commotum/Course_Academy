Circle center/radius generator, frozen version `circle-extraction-frozen-1`.

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186087656/validate.py
.venv/bin/python generate/scratch/17592186087656.py --difficulty all --seed 71 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186087656.py --difficulty easy --profile q-7527 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and easy/moderate/hard entrypoints. Template `standard_circle_radio`; field type `radio`; explicit parameters are `a`, `b`, `S` (integers or exact rational strings). Profiles in the script are complete banks, not distractor pools. Invalid explicit inputs fail.

Fidelity: 8/8 prompts, 8/8 complete banks (40/40 choices), 7/7 supplied worked solutions, 7/7 present correct designations, and attribute-presence parity for all eight. q-7527 is an unrated legacy source with omitted solution/correct ref; raw replay is evidence-only. `q-7527_completed` is explicitly inferred and independently graded, never claimed as original source designation fidelity.

Moderate and hard are authored standard-form extraction extensions; see classification for strict, disjoint finite number-form domains. Scope excludes construction, distance, midpoint, completing squares, intercepts and diagrams. All supported fields are radio; blank-equivalence testing does not apply. Native choice grading and independent actual displayed mathematics are separate checks. No plots, external reads or database writes are performed by generation/validation. Review artifacts contain answer keys and metadata and are author previews.
