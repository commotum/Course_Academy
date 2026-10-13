# Point-information coordinate generator

Draft stops after steps 3–7. Script: `generate/scratch/17592186092219.py`. Only local review artifacts; no registration, database writes or shared engine changes.

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186092219/validate.py
.venv/bin/python generate/scratch/17592186092219.py --difficulty all --seed 2 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186092219.py --difficulty hard --profile raw_q-40826 --format json
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None); generate_easy, generate_moderate and generate_hard. Easy uses `radius,factor,angle`; source-shaped templates use `scale`. Explicit bounds and complete-bank validity match sampling. Original masks are public `raw_<source-id>` profiles, with missing source attributes preserved; `observed_<source-id>` profiles supply independently inferred missing keys/solutions. Both evidence modes are ineligible for learning because historical distractor operations are opaque. Defaults use source-shaped solutions and authored complete operation banks.

Raw exact fidelity, normal prose/stage fidelity, mathematics and real native grading are reported separately in validation.json. review.json / review.md show each original, two normal variants and two historical-bank evidence variants, plus two default examples per level. source-cases.json lists every practice record. build_masks.py regenerates documented extraction masks only; it is not a separate question-return branch.

Easy is curriculum-grounded authored scope; two unrated source assignments are authored. q-276838's axis/quadrant teaching error is retained in raw evidence and minimally repaired in normal output. No graphics are needed.
