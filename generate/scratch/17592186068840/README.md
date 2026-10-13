# Explicit separable ODE solution generator

Run from repository root:

```bash
.venv/bin/python generate/scratch/17592186068840/validate.py
.venv/bin/python generate/scratch/17592186068840.py --difficulty all --count 2 --seed 41
```

Public API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), and individually documented generate_easy/moderate/hard. `observed_<template>` selects complete original evidence banks; normal operation_errors profiles select authored complete method-error banks. Source profiles intentionally preserve documented duplicate, domain, and wrong-form observations. They are fidelity evidence, not normal learner banks. Hard is an authored level with two same-method peers derived from canonical and lesson-intro examples.

JSON contains schema-shaped local review records and generation metadata. No EDB access, registration, git action, plot assets or writes outside the assigned folder. Native grading uses the captured real application checker. Independent displayed mathematics uses SymPy with the existing read-only cached Lark wheel, no dependency installation.

Documented native limitations: the original temperature blank accepts rational/distributed forms of its exponent, but the equivalent reciprocal exponential is unresolved. For original replay, a nonzero factor absorbed into arbitrary K (e.g. 2e^(-rt)) represents the same complete temperature family and is independently recognized as such, but the fragment-value grader rejects it. These limitations are explicit expected outcomes in the native report; Normal questions ask for a single exponential with leading coefficient 1; no engine changes are authorized here.
