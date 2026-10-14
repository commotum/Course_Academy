# Negative linear term completion generator

Source evidence: math basis 1356, rechecked unchanged at basis 2213. Generator registration and replenishment were committed and verified at basis 2214. The generator itself emits local drafts; `replenish.py` handles validated additive database writes.

```sh
.venv/bin/python generate/scratch/17592186068876/validate.py
.venv/bin/python generate/scratch/17592186068876.py --difficulty all --seed 42 --count 2
.venv/bin/python generate/scratch/17592186068876.py --difficulty easy --profile source:q-141611 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and individual level entrypoints. Families: easy `direct`, `fragment`; moderate/hard `pq_plus`, `pq_minus`. Plain and enum field selectors radio/blank work. `authored_method` is normal generation; `source:<id>` exposes faithful parameterized evidence with raw omissions and is always marked evidence-only/ineligible. Explicit input is validated, never resampled. Historical opaque-bank scalar parameters are available only in evidence profiles, never defaults.

For `parameters`, supply integer `h` (positive half-coefficient), integer `c` (constant), and variable `v` in x/y/z. Easy: h1..12,c1..144, c≠h². Moderate: h1..12,c0..144,c≠h². Hard: h3..12,c−60..−1. Radio h1 causes the unsquared-correction recipe to collide and rejects the complete instance; blanks support h1. Normal binomial blanks specify positive leading variable coefficient. This avoids the raw source's sign ambiguity, while faithful raw records retain original wording.

Validation reads displayed equations/stages, checks all original choice values and optional-attribute presence separately from correctness, rejects C0 bytes and equal-but-collapsed teaching stages, checks identity semantics and native grading. Raw anomalies remain raw; inferred completed versions are separate review artifacts. Three missing designations and opaque historical distractor intention are documented limitations, not passed comparisons. Validation reports exact Python/SymPy versions and grader binary hash.

## Verified inventory replenishment

The existing generator passed source replay, independent mathematical checks on 360 samples, and native grading (112 accepted, 149 rejected, no unresolved results). All 31 present source answer values and all 11 complete field banks replay; missing source keys remain documented omissions. Hard is an authored same-method signed-constant band, not a recovered source rating.

At basis 2213 the requested KP had four fresh gradable easy tasks, three moderate, and zero hard. The application lock was held from current inventory/basis recheck through preview, guarded submission and exact-basis readback. Basis 2214 verified one new easy, two moderate and five hard questions, five usable distinct tasks per band, and generator registration. The registered UUID and script path are recorded in `capabilities.json` and the verified outcome.

`reference/replenishment/basis-2213/` retains the original typed transaction, exact durable request, speculative preview, receipt, grader checks, source/readback snapshots and inventory verification. All ten original questions, the canonical example, and learner history were preserved. Additive datoms were attributed to the configured application contributor. Repeat preparation at the verified basis adds no content.

Distinctness uses polynomial coefficients globally; variable aliases, answer shapes, p-sign conventions, seed and choice order cannot produce a fresh task. The two incomplete unrated originals remain excluded and their unresolved source-content exception remains explicit in the outcome; the final native inventory reports no remaining jobs for this KP. No unsupported level is claimed filled.
