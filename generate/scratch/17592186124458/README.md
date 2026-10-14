# Directional derivative generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186124458/validate.py
.venv/bin/python generate/scratch/17592186124458.py --difficulty all --seed 8 --count 2
```

API `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and three level entrypoints. Normal parameters are integer a,b,c,d=1..4, x0,y0=−3..3 and nonzero direction components (integers −5..5 or, for xy, ±√3), with narrower moderate/hard direction bounds 4. Hard evaluated gradient components are bounded by 48 and each component product by 192. Exp requires y0=0 and x0≠0; chain square requires y0≠0 and nonzero inner value. Explicit invalid inputs raise; sampled invalid complete banks are wholly rejected. Unused coefficients do not inflate mathematical identity. Common positive direction scaling is canonicalized using the actual unit direction.

Raw replay example: `generate('easy', template='xy', profile='raw_xy', parameters={'scale':1})`. Raw scale 1..6 scales the complete function, gradient and bank, retaining the original components and solutions. Raw records are evidence-only: scalar bank intention is underdetermined; absent source attributes remain absent. The incomplete originals have no native grading check until a correct ref is authored. Normal radio defaults select complete method-derived banks before parameters, with optional explicitly authored blank layout; supplied-gradient keeps its blank layout. `review.md` contains originals and generated variants; `validation.json` separates exact source fidelity, intended correctness and actual native grading.

No database writes, engine edits or plots. Hard assignment is authored from the observed unrated nested-square family. The supplied-gradient source has limited recoverable prior context; normal prompts supply its gradient datum. This draft stops at step 7.
