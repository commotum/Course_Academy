# Rectangular slope sign-region generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186172041/validate.py
.venv/bin/python generate/scratch/17592186172041.py --difficulty all --seed 13 --count 2 --format markdown
```

API: generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None), generate_easy/moderate/hard. Only one radio selection field with five text choices. Parameters specify full factored expression and three strict rectangle claims. No DE solving, slope-field identification, plots at isolated points, or quadrant-only questions. Root locations are nonzero.

7 source prompts and 35 displayed choices; 6 available markers and 6 full solutions exact. q-96475 has missing marker/solution: independently derived I only, authored moderate assignment and solution, documented separately. Easy is authored from the canonical example's simple shifted-factor task. Original banks are explicit replay profiles; default whole truth-flip bank is authored.

Source provenance is preserved at basis1356. source-cases.json covers all seven, profiles.json records every complete bank, classification/template/plot extraction documents scope and interpretation, review.md/review.json contains originals and two changed variants per bank and at least two per level. validate.py independently reads displayed equations, regions and full worked stages, enumerates finite meaningful banks, checks strict input bounds and concurrency, and calls the real memory-only native grader. validation.json reports denominators and native results. No database writes, engine changes or commits.
