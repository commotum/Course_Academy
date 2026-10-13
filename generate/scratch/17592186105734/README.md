# Altitude from triangle vertices

Local generator at math basis 1356; steps 3–7 only, no database operations.

```sh
.venv/bin/python generate/scratch/17592186105734.py --difficulty all --seed 4 --count 2 --format json
.venv/bin/python generate/scratch/17592186105734/validate.py
```

Public API: generate_easy/moderate/hard and generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). Parameters have `vertices: {A: [x,y,z], ...}` using the selected mask's names. Authored templates are `authored_LEVEL_radio` and `authored_LEVEL_blank`; observed presentation masks use source q-IDs. Complete observed radios use `observed_q-ID`; blanks use `none`. Invalid explicit parameters raise ValueError. CLI also accepts --template, --profile and --field-type.

Source replay cases, complete bank mapping, scope rationale, raw evidence, review examples, independent displayed-stage checks, real native-engine results and final hashes are beside the script. Missing easy/moderate are authored peer extensions; q-20028 has authored hard placement/key/full solution. q-128008's incorrect reduced-basis j is corrected to k. Scalar distractor intent remains underdetermined and is documented; observational banks remain explicit replay profiles while normal radios use a complete method-error bank.

Verified: 18 exact prompts, 58/58 displayed source values, 40/40 distractors, 10/10 complete radio banks and 17/17 supplied correct designations. Supplied solutions: 16 exact, one minimally corrected; q-20028 has an authored missing key/solution. Independent displayed-stage checks cover 180 authored defaults, 18 changed source masks, 76 implicit-product combinations and 288 additional parent-reader instances. Native grading: 94 accepted, 138 rejected, zero unresolved. Six CLI output records also pass independent checks.
