# Jacobian determinant generator

Local script: `../17592186129187.py`. Symbolic 2x2 Jacobian only; all three levels, ten original five-option banks, authored default banks, canonical-supported hard powers. No database writes. Plots: none.

```sh
.venv/bin/python generate/scratch/17592186129187/validate.py
.venv/bin/python generate/scratch/17592186129187.py --difficulty all --seed 42 --count 2
.venv/bin/python generate/scratch/17592186129187.py --difficulty easy --template polar --profile observed_polar --format json
```

The validator parses displayed functions, choices, derivatives and scalar solution equalities, independently differentiates, matches complete original banks, checks identities and invalid-input rejection, and calls the real application grader via memory-only fixtures. `validation.json` records honest denominators: 50 source options, 10 banks, 9 present designations; q-38244's missing designation/level/solution is authored. q-38078's intermediate trig typo is explicitly corrected. `review.md` includes raw originals, replay and two variants per complete profile, including easy/moderate/hard.

Observed profile error intentions are unresolved hypotheses; those profiles preserve expression patterns for explicit replay. Defaults use separately labeled method-error recipes. Standard vector/trig LaTeX normalizes source notation without changing mathematical answer shapes.


## Parent variety review

Hard retains the canonical powers-of-linear-forms method and adds inner coefficients 1 or 2: x=a(pu+qv)^m, y=b(ru-sv)^n. Outer scales remain 1..3 and powers (3,2),(2,3),(3,3). All-one inner coefficients reproduce the canonical form. These 432 bounded parameter combinations vary the four chain-rule factors without adding a mathematical branch, evaluation, orientation, or area scaling. This extension addresses the initial 27-combination limit; it is authored variation rather than an observed template.

Parent QA independently verified all50 immutable source values and all432 hard parameter combinations. Content identity includes version, rendered prompt and worked solution as well as the complete displayed bank.
