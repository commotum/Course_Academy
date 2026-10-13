# Checkbox generator refresh

The two affected scratch generators now use read-only EDB captures from math basis 1522. The original basis-1356 sources, generator code and review/validation artifacts are retained under each KP's history/basis-1356 directory. The broader generate/runs/current capture remains historical and unchanged.

- 17592186059848: Identifying Singular Matrices. All 17 practice questions now use three Boolean checkbox fields. Current labels, instructions, keys and complete banks are reproduced.
- 17592186059849: Solving for an Unknown Given the Determinant. Eight practice questions use 40 individual-value checkbox fields; nine radio questions and seven blank questions retain their shapes. All-real answers stay radio. All 59 current database fields and keys are reproduced.

`generator-refresh.json` records source bases, generator/source hashes, validation/review locations and grading counts. `source-query.edn`, `source-inputs.edn` and `source.edn` retain the parameterized fixed-basis read evidence. No database transaction or generator registration occurred.

The runtime mathematics and difficulty scopes remain the same. Numeric checkbox option recipes parameterize the normalized union of the retained legacy banks for explicit observed replay, with unknown distractor intent documented. Default numeric checkbox pools use the distinct atoms from the previously authored operation-derived banks and are labeled authored extensions. Every complete pool must contain both real roots; duplicate or invalid observed atoms reject the whole instance. Current database keys are independently verified and take precedence over historical or external keys.

The native helper links the existing application library and checks both field grading and whole-question grading, including explicit unchecked false answers, flipped boxes and missing responses. Its build provenance is in `native-build.json`.

The subsequent feedback fixes are in generator version 3. For 17592186059848, false determinant claims now derive from the displayed matrix arithmetic and include fractions, radicals, additive radicals and large integers. Six moderate matrix families cover mixed radical placement and sparse rational/radical entries; singular sampling includes proportional rows and columns. Each family is selected before rejection. Easy/moderate arithmetic stays within independently measured source maxima. The twelve extracted patterns are layout/order/stage distinctions within one mathematical method. Hard remains an authored extension without original calibration.

For 17592186059849, the q-9961 default retains Any real number, and authored checkbox profiles work through the CLI. Explicit source banks remain separate from authored default alternatives. Hard remains the two observed identity structures and always answers all values; hard-only practice is predictable, so practice should mix levels. Easy/moderate parameter variation deliberately stays within the observed equation structures.

Validation after these fixes matched all 41 source practice questions and 110 fields, checked 1,240 sampled variants plus 39 layout-specific variants, and passed 1,233 native field checks and 191 whole-question checks. The follow-up refinement excludes zero rows and columns from normal sampling and adds a seed-181 regression; explicit replay remains unchanged. Fresh sampling checks include 360 additional easy/moderate records and demonstrate both singularity states in every moderate matrix family. `../17592186059848/sampling-review.json` retains representative normal samples; each KP's validation.json separates replay from sampling coverage. The native helper was linked against the freshly rebuilt review engine in /tmp/determinant-review-20261012/current-target. Pre-review checkbox artifacts are retained in each KP's history/checkbox-v2-pre-review directory.

Reproduce from the repository root:

```sh
.venv/bin/python generate/scratch/source-refresh-2026-10-12/build-native.py
.venv/bin/python generate/scratch/17592186059848/build_evidence.py
.venv/bin/python generate/scratch/17592186059848/write_review.py
.venv/bin/python generate/scratch/17592186059849/build-evidence.py
.venv/bin/python generate/scratch/17592186059848/validate.py
.venv/bin/python generate/scratch/17592186059849/validate.py
```

To link that review build instead of the default repository target directory, append `--target-dir /tmp/determinant-review-20261012/current-target` to build-native.py.

The numeric generator retains its existing full cofactor derivations for q-9657 and q-9852, where the current database now has brief authored explanations. This is recorded as a solution expansion rather than literal prose fidelity. Equivalent arithmetic typography and the previously documented source errors remain explicit in each KP's review and validation.
