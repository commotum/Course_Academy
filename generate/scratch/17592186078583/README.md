# Modeling Inhibited Decay generator

Script: `../17592186078583.py`. Run from repository root:

```bash
.venv/bin/python generate/scratch/17592186078583.py --difficulty all --seed 21 --count 2
.venv/bin/python generate/scratch/17592186078583/validate.py
```

Evidence uses math basis1356. All eight originals and full banks replay via the same generate API with source-cases.json parameters/profiles. Exact bank/wording fidelity, independent displayed mathematics, bank uniqueness and native grading have separate results in validation.json. The raw oil source bank has two equivalent wrong options; normal output uses a repaired complete bank. q105917 key/solution/level and all hard examples are authored and explicitly distinguished from observed matches.

The hard extension uses an extra reading present in the lesson's Newton tutorial but keeps exactly the generic and substituted Newton-law equation stages. No ODE solving, k fitting, additional branch or within-level progression. All answer fields are radio; blank-equivalent-entry grading is inapplicable. No plots or database writes. templates.json contains operational extracted component masks and is required alongside the script. review.md/review.json show originals, every changed source template/bank, repairs and at least two normal generated questions at each level. freeze.json records final file hashes after verification.
