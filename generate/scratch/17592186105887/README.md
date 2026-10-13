# Evaluating Surface Integrals draft

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186105887/validate.py
.venv/bin/python generate/scratch/17592186105887.py --difficulty all --seed 7 --count 2
.venv/bin/python generate/scratch/17592186105887.py --difficulty moderate --template plane_log --profile raw:q-161347 --format json
```

The script exposes `generate`, `generate_easy`, `generate_moderate`, `generate_hard`. Explicit normal parameters are `a,b,c,lo,hi,k`; only meaningful components for each family enter mathematical identity. Raw source profiles accept the genuine integrand `scale` parameter 1..4, preserve omitted source attributes, and reproduce complete original strings/banks at unit scale. They are evidence only and ineligible for learning, because historical scalar banks do not establish historical error operations. The malformed legacy inline integral in q-160836 is preserved in raw evidence; normal output uses standard LaTeX.

Defaults cover ten observed moderate families and four explicitly authored easy/hard families with full method-derived operation banks. Invalid explicit parameters and whole-bank equivalences raise errors. Random sampling resamples the complete instance after selecting family and bank. There are no plots, database calls, environment changes or transactions. Evidence is frozen after step 7 for independent parent review. Native radio grading is separate from actual displayed mathematical verification.

Version 2 retains source-family aligned worked solutions in all normal supported families. `normal-structure-regression.json` records original-parameter and varied-parameter structural checks; `family_chains.py` contains complete mathematical masks. Supplemental endpoint rows are documented in template extraction. Shared source prose, cancellation/expansion stages, metric placement, primitive stages and the natural-log convention remain in learner presentation.
