# Portable repaired generator

Run `python3 generator.py --difficulty easy|moderate|hard --count 5 --seed 71 --format json` from any working directory. Output is the complete original record structure: knowledge point, question with worked solution and full answer fields/choices/key, and generation provenance. All runtime dependencies are standard-library Python; no database, network, assets or repository imports.

See `instructional-account.md` for the actual learner operation, source families and honest calibration limits. See `runtime-manifest.json` for the full runtime closure and hashes. The related source audit is retained unchanged under `reference/edb-math/audits/2026-11-04-four-trig-lessons/`; imported records are evidence, not guaranteed-correct answer banks.

Run `python3 check_repair.py` from the repository to reproduce visible-TeX numeric checks, pairwise radio-choice separation, derivation equalities, same-parameter source-family checks, deterministic small seeded CLI batches and relocation. This verification script uses the repository's independent audit reader, while the runtime closure is portable. `evidence/validation-results.json` contains actual counts and limitations; `evidence/math-checks.json` retains witnesses. Native learner grading, actual UI rendering and publication are reviewed separately by the root agent.

Runtime files:

- `generator.py`
- `math_format.py`
- `replay-data.json`

The meaningful hard catalog has eight original angles, two unit presentations and only two distinct final values (1/2 and 3/4). Those two values do not establish broad evaluation mastery; inner quadrant signs and square recognition remain the assessed decisions. No original special angle or zero outcome enters new hard output. CLI requests beyond the finite presentation catalog fail explicitly. Cosmetic unit/response variations are served only after all available angle/form calculations in the pool have been used once.
