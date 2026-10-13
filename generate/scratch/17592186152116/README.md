# Constant-factor polynomial LCM generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186152116/validate.py
.venv/bin/python generate/scratch/17592186152116.py --difficulty all --seed 12 --count 2
.venv/bin/python generate/scratch/17592186152116.py --difficulty hard --format json
```

API: `generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None)` and `generate_easy`, `generate_moderate`, `generate_hard`. Source case parameters/profiles are in `source-cases.json`. `observed_q-...` preserves raw missing keys; `derived_q-...` provides mathematically verified completion. Raw records without captured answer keys are evidence, not native-grading-ready questions.

Normal easy/moderate retain one identical monic binomial/square. Easy requires coprime contents, moderate shared content; these guards also apply to explicit observed/derived source profiles. Unrated q-76238 is completed as authored easy, q-218482 as authored moderate, while raw missing difficulty attributes remain absent; authored hard extracts integer content from two signed expanded multiples of one identical primitive nonmonic quadratic. No distinct-factor, different-power, multivariable or three-input branches. LCM means the positive integer-content LCM times the shared positive-leading primitive part. Complete source profiles and authored default banks are separated; collisions reject the whole instance.

`validate.py` checks actual printed inputs, every solution equality and multiple list, full source prompts/field presence/banks/solutions, normalized LCM semantics, identity, explicit guards, TeX/control bytes and native grading with `generate/runs/current/check-engine`. Review examples cover every source profile and two per level/field layout. `validation.json` records separate fidelity/derived counts and a generator hash. No EDB or shared file writes. Parent QA is required before acceptance.
