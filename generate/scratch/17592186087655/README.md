# Center and radius → complete circle equation

Private generator: `../17592186087655.py`. Source database math, basis 1356. Stops after steps 3–7; no EDB registration or writes.

```sh
.venv/bin/python generate/scratch/17592186087655.py --difficulty all --seed 42 --count 2 --format json
.venv/bin/python generate/scratch/17592186087655/build-evidence.py
.venv/bin/python generate/scratch/17592186087655/validate.py
```

Easy reproduces all 8 source practice banks/field layouts and preserves the raw omissions. Moderate/hard are authored exact-rational number-form extensions within the same substitution/squaring method. `classification.md` states strict reduced workload bounds and source anomalies. `source-components.json` maps all 36 original choices. `source-cases.json` gives public replay arguments. `review.md` shows originals and two generated variants for every bank plus all three levels; `review.json` contains those generated records. `validation.json` separates literal source fidelity, actual displayed mathematics, native grading, domain/identity/formatting and raster geometry checks.

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, plus `generate_easy/moderate/hard`. Parameters exactly `{h,k,r,orientation}` using integers or exact rational strings (orientation horizontal/vertical). Normal templates graph_radio/graph_blank; raw stripped source blank uses missing_input_blank. `raw:q-ID` preserves original missing attributes and marks incomplete evidence ineligible for learning. `completed:q-ID` or `q-ID` supplies inferred missing attributes/diagram while preserving each complete observed operation bank. All explicit inputs are validated without resampling. Source profiles retain integer number-form bounds; default moderate/hard use reduced fractions. Public API never supplies a literal source answer lookup.

Images regenerated through Matplotlib are private hashed PNGs with atomic sidecars and cached read-only Python 3.10 runtime fallback; no dependency installation. Original raster replays keep exact source refs; review Markdown resolves them to their absolute paths. The stripped q-167932 input has no recoverable original image, and two legacy radios have no original correct designation; those limitations are explicit rather than hidden by completed profiles.

Native limitation: the existing symbolic grader does not parse full equations in blanks (`unconsumed mathematical notation`). All default easy/moderate/hard learning outputs use supported radio fields. Explicit blank records preserve full source shape as evidence only, with `grading_compatibility.supported=false` and `eligible_for_learning=false`; mathematical/fidelity checks still apply. The validator accepts only that documented exact unsupported result and fails any unexpected native behavior. See `engine-report.json` for actual outcomes; source blank native support is never claimed passed.
