# Amplitude generator

Current production version: 1.1.0. Script: `../17592186129121.py`.
Supported bands: easy and moderate; five-option math radio fields, no plots.

```sh
.venv/bin/python generate/scratch/17592186129121/validate.py
.venv/bin/python generate/scratch/17592186129121.py --difficulty easy --count 5 --seed 10 --format json
.venv/bin/python generate/scratch/17592186129121/replenish.py
```

The current capability decision supersedes the version 1.0 hard extension in
`classification.md`, `template-extraction.md`, `freeze.json` and old review files.
Their historical evidence is preserved under `reference/v1-evidence/`.
`capabilities.json` and `validation.json` describe current production support.

Hard remains unsupported. Its earlier outer multiplication added an operation
and a rewrite stage absent from the source templates, contrary to stages 4/6.
It is rejected by the public API and never counted as filled. No source question
has been reclassified or repaired. Two sources still lack correct references,
and two others still lack fields. Public `raw:q-ID` profiles preserve those
omissions and remain evidence only.

Production profiles preserve complete observed banks: positive coefficients
(q-117570), implicit coefficients (q-117569), negative coefficients (q-117574),
and numerator quotients (q-117576 and q-43278). The negative profile now uses
`1/abs(A), B, 1/B, abs(A), C`, matching q-117574, rather than the earlier authored
replacement. Raw replay still covers all seven source banks and all 35 values,
including banks excluded from normal production because error intentions are
unresolved. Normal notation uses `\sin`/`\cos`; values, supplied information,
response contract and solution stages preserve the corresponding source family.
The q-43278 bank's key and solution are explicitly authored from its mathematical
coefficient and the observed quotient solution, without modifying its source.

`validate.py` independently parses printed functions, every solution rewrite,
correct answers and complete banks; checks all production profiles, deterministic
replay, task deduplication, slot variation and real application radio grading.
`reference/current-validation/side-by-side.md` contains original and changed
instances reviewed together. No targets change roles: the requested object
remains the amplitude, with direct or single-division coefficient extraction.
Changing trig aliases or argument/offset values does not create a distinct task.
The CLI deduplicates by assessed coefficient and operation, and reports a bounded
sampling failure when a requested distinct batch cannot be produced.

`replenish.py` uses the existing EDB Database integration, native inventory,
validation specs and configured application contributor. It acquires `api.lock`
for fresh-basis preparation through exact-request submission and readback,
recovers retained intents before new work, checks stable identities and existing
mathematical tasks, and verifies only additive content datoms under this KP.
Exact EDN, request keys, expected basis, receipts and verification are retained
under `reference/replenishment/`. Learner and engine facts are never written.
