# Definite integration by parts

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186064274.py --seed 42 --profile q-349299 --json /tmp/ibp-preview.json
.venv/bin/python generate/scratch/17592186064274/validate.py
.venv/bin/python generate/scratch/17592186064274/replenish.py
```

Moderate only. The source-derived coefficient/frequency/bound slots and exact transported complete banks are documented in template-extraction.json and profiles.json. Generator output separates database content from provenance, recipes, seed and parameters. Blanks expect the full exact scalar value, without math delimiters. Math and distractors use SymPy; actual grading uses the existing application engine built in target/release. build-native.py copies only the read-only fixture harnesses into this KP package and records executable/library hashes. No application code is changed.

The public generator was executed for every source profile and four boundary/interior variants per profile. source-replay.json records mathematical/complete-bank fidelity; validation.json records independent displayed-math and grader checks. review.md pairs original-parameter replay with scale-only, dilation-only, combined and boundary variants. Original source prose/equations remain in source.edn. Source notation is normalized, and repeated arithmetic simplification rows may be combined; setup, parts substitution, remaining integration, endpoint evaluation and final simplification are retained.

Deduplicate by displayed integrand and bounds against source questions, canonical examples and all existing/generated content. A different seed, bank, answer UUID or option ordering never creates another task. Identity includes the bank profile to prevent collisions while preparation excludes task duplicates. Supported-level exhaustion is a finite-limit result; easy and hard remain explicit unfilled capability exceptions.

replenish.py uses the configured EDB integration and contributor, serializes with the application api.lock, recovers exact retained requests first, captures fresh inventory/basis, previews with installed native entity specs, persists the exact request, then submits with a basis guard and verifies the exact committed basis before releasing the lock. Source questions and learner facts are immutable.
