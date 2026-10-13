# Resonant first-order particular-solution generator

Local review records only; no EDB transactions. Captured math basis1356. Eight easy + four moderate exact observed replays, authored hard two-term signed fractional coefficient matching. No plots.

```sh
.venv/bin/python generate/scratch/17592186229163/validate.py
.venv/bin/python generate/scratch/17592186229163.py --difficulty all --seed 42 --count 2 --format json
```

API: generate_easy, generate_moderate, generate_hard and generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None). Field type blank only. Explicit profiles braced/plain/duplicate_legacy/punctuated preserve observed banks and layouts; normal is the method-based default. All source cases call that API with extracted coefficients; none returns a literal payload or answer lookup. Normal minimally removes one duplicate legacy answer. Fraction strings in the sources are valid TeX; serialized escaping does not constitute an anomaly. Exact raw replay and repair counts are separate in validation.json. Review contains every source, every observed-profile variant and two normal examples per level. Native check-engine uses memory-only fixtures.

Stable content UUIDs depend on version, difficulty, actual prompt, full solution, complete answer bank and correct value. Mathematical fingerprints depend only on the canonical displayed ODE coefficients. Seed/order cannot alter identity for fixed parameters and displayed content. All explicit parameters obey the same workload guards as random samplers.

Normal also clarifies that no complementary-solution term should be added. Raw observed prompts preserve the original mathematically nonunique wording. Native grading checks equivalent expressions for the intended trial-form particular function; raw exact source fidelity does not imply grader acceptance of arbitrary complementary additions.
