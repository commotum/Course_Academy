# Vector magnitude generator

Registered script: `generate/scratch/17592186059714.py`. Output is local JSON or Markdown; no database operations occur in the generator.

```sh
.venv/bin/python generate/scratch/17592186059714.py --difficulty easy --count 5 --seed 42
.venv/bin/python generate/scratch/17592186059714/build-grader.py
.venv/bin/python generate/scratch/17592186059714/validate.py
.venv/bin/python generate/scratch/17592186059714/replenish.py
```

Python 3 and SymPy 1.14.0 are used. The grader build records exact current Rust sources, library, and binary hashes. Validation freezes generator/source/validator/grader hashes. See classification.md, template-extraction.md, templates.json, capabilities.json, source.json, review.md, validation.json, and reference/native-report.json for source fidelity, authored completions, mathematics, and actual learner grading as separate claims.

Supports easy only, with two complete observed radio banks under positive integer vector scales 1..8 (q-1325) and 1..3 (q-18046), with coordinates bounded by 36. Finite catalog: 9 different squared norms; excludes all existing practice/canonical tasks at preparation. Other bands reject explicitly. Fewer than the requested count can be returned when the finite catalog is exhausted; the commit worker deduplicates against current inventory and reports remaining shortages. It does not count unavailable, unrated, or incomplete source records.

replenish.py serializes with the application using api.lock. It resolves :application/ca-engine, rechecks inventory/basis/lineage/source preservation under the lock, retains exact typed EDN and durable intent, previews installed validation specs, submits with a basis guard through the configured integration, verifies exact-basis readback and allowed additive datoms, then rechecks inventory. Unknown outcomes are recovered under the original request key. Registration uses the KP's existing generator identity if present; no source content or learner facts are rewritten.
