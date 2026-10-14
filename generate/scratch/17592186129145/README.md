# Graph-to-factored-polynomial generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186129145/validate.py
.venv/bin/python generate/scratch/17592186129145.py --difficulty all --seed 12 --count 2 --format json
```

Local review only. Public API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None) and generate_easy/moderate/hard. Parameters are h (integer -3..3), s (1 or2; hard1), v (1/2,1,2). Explicit inputs are validated. Source replay uses source ID as profile and h=0,s=1,v=1, through the ordinary parameterized construction. All ten sources replay; two fieldless banks and the unrated key/solution are clearly authored/inferred.

q-38671 and q-38774 retain exact historical banks as evidence-only public profiles because two incorrect options have the same qualitative graphical signature. Normal defaults select their separately authored complete banks, plus all other eligible source families and four authored hard positional profiles. Never count positive amplitude or exponent changes within the same parity/tangency category as assessed variety. Source-cases, full originals and changed examples are in review.md/review.json; mathematical and native grading results are separate in validation.json/native-report.json. Parent QA is required. No DB, registry, engine, shared-file changes or commits.
