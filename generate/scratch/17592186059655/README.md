# Expansion and Pythagorean identity generator

Read-only local generator at math basis1356. Run:

```sh
.venv/bin/python generate/scratch/17592186059655/validate.py
.venv/bin/python generate/scratch/17592186059655.py --difficulty all --count 2
.venv/bin/python generate/scratch/17592186059655.py --difficulty easy --template paired_squares --profile observed_raw
```

Seven source banks are retained by angle/common-scalar-slotted `observed_raw` replay, including missing original attributes. `observed_completed` supplies mathematically supported correct references and authored easy levels/solutions for the two unrated sources. Five complete records retain source worked-solution strings exactly. These replay profiles preserve limited source workload and are not a claim that coefficient ranges or error intent have been recovered. Normal `authored` records vary coefficients, using explicitly authored complete banks and the canonical expansion → grouping → identity → conclusion solution structure.

Every observed_raw and observed_completed record is evidence-only and ineligible for learning because historical bank intent is underdetermined; normal learning uses explicitly authored banks. Raw unrated previews say “Unrated — original difficulty absent”; completed repairs say “Inferred Easy”. All three levels have entrypoints. Missing moderate and hard are authored scope claims; see classification. No plots, DB writes or engine changes. Source wrapping provenance is retained in `source.json`; raw replay does not reproduce EDB db IDs or answer UUIDs, but does preserve learner attribute presence, values, bank count, existing designation and solution strings. New UUIDs are content/field-owned. Native grader checks radio selection of every bank member. This KP has no blank field requiring text-equivalence grading.

The independent validator parses displayed TeX into sin/cos symbols, checks all ordered solution equalities against the original displayed expression, and compares complete options modulo the Pythagorean identity. Its parser is deliberately limited to this generator's documented algebra. `review.md`/`review.json` show original raw evidence, supported completions, and two coefficient variants for every observed template, plus two examples of each authored missing level. `validation.json` separates source counts from correctness and native grading.

The normal cos-reciprocal template has two named complete banks: `cos_reciprocal_unit` (a=1;2,1,0,−1,−2) and `cos_reciprocal_nonunit` (a2–6;a+1,a,1,0,−a−1). The sampler selects a whole bank before sampling a from its permitted domain. Explicit mismatches raise ValueError. Both profiles are available through `--profile` with `--template cos_reciprocal`; metadata records selected name, eligible a values and full recipes. No distractor replacement/fallback occurs. Fixed parameters retain the previous prompt, solution, complete bank and IDs.
