# Portable repaired generator

Run `python3 generator.py --difficulty easy|moderate|hard --count 5 --seed 71 --format json` from any working directory. Output is the complete original record structure: knowledge point, question with worked solution and full answer fields/choices/key, and generation provenance. All runtime dependencies are standard-library Python; no database, network, assets or repository imports.

See `instructional-account.md` for the actual learner operation, source families and honest calibration limits. See `runtime-manifest.json` for the full runtime closure and hashes. The related source audit is retained unchanged under `reference/edb-math/audits/2026-11-04-four-trig-lessons/`; imported records are evidence, not guaranteed-correct answer banks.

Run `python3 check_repair.py` from the repository to reproduce visible-TeX numeric checks, pairwise radio-choice separation, derivation equalities, same-parameter source-family checks, deterministic small seeded CLI batches and relocation. This verification script uses the repository's independent audit reader, while the runtime closure is portable. `evidence/validation-results.json` contains actual counts and limitations; `evidence/math-checks.json` retains witnesses. Native learner grading, actual UI rendering and publication are reviewed separately by the root agent.

Runtime files:

- `generator.py`
- `math_format.py`

Both moderate and hard use common-factor recognition followed by a single identity application. Hard is an authored continuation with modest fractional coefficients and optional term reordering; its workload overlaps moderate. No imported hard example calibrates it. Whole plausible error profiles are resampled only to reject numerical equivalence and incidental bank cues; the stem's angle/coefficient are sampled first and preserved during bank resampling. The hard label does not license extra identities or hidden quartic algebra.
