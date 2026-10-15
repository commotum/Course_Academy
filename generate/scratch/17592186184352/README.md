# Evaluating Definite Integrals draft

Frozen math basis2275. No EDB writes, registration, shared QA edits, or engine changes. Source wrapper and private dependency snapshots are preserved.

Run from repository root:

```bash
.venv/bin/python generate/scratch/17592186184352.py --difficulty all --count 1 --format json
.venv/bin/python generate/scratch/17592186184352/validate.py
```

Eight parameterized source families span easy/moderate/hard. q-30977 has an explicitly authored moderate designation, correct reference, and missing solution. Normal radios use an explicitly authored complete method bank; observed complete banks replay with source_bank. Source blank wording replays with source_presentation; normal source_blank avoids the known native “round” form restriction. source-cases.json lists the exact public replay inputs. capacity.json and validation.json separate source fidelity, displayed mathematics, bounded variety, and native grading. review.md pairs originals and variants. Parent independent review remains required.

Native grading limitation: a valid general log difference such as `2(ln(11)-ln(5))` is unresolved against `2ln(11/5)` by the frozen engine. Supported unreduced endpoint ratios pass throughout the full hard domain. This is recorded separately from malformed input and ownership diagnostics and requires parent review; native grading is not claimed unrestricted.

## Finite semantic batch API

`generate` and the three level entrypoints preserve single-instance and exact source-parameter/profile replay. `seed` and every declared numeric slot require a built-in Python `int`; booleans, floats, strings, and integer-like subclasses are rejected. Explicit parameter dictionaries require exactly the family’s declared keys. Batch `count` likewise requires a positive built-in `int`.

`semantic_catalog(level, template=None, field_type=None, profile=None)` exposes one valid representative per normalized integrand, integration interval, and exact integral-value target. The response target is always the value of the displayed definite integral. Entire choice-bank profiles, radio/blank presentation, source wording, alternate exponential bases, and common scaling of numerator/denominator never add semantic capacity. `catalog` is an alias. `capacity` returns the catalog size. `generate_batch(level, count=1, seed=0, ...)` (`batch` alias) samples that finite catalog without replacement and fails if count exceeds capacity.

The default semantic capacities are easy135, moderate69, and hard600, totaling804. These differ from the 810-task union in the earlier full source-bank/default evidence because six tasks are eligible only under empirical source-bank profiles. Profile-specific catalogs retain their own valid complete banks and original-anchor source presentation restrictions. They still use the same semantic key. At the same supplied slot values, single-instance records and all source anchors remain exactly unchanged.

The CLI now uses `generate_batch` once per requested level. Thus `--difficulty all --count 4` returns twelve flat records: four distinct mathematical tasks per level. Oversized counts fail without returning a partial batch. `interface-validation.py` checks strict inputs, full-capacity batches, independent readback of every task key, bank/wording/base/common-scale aliases, and exact compatibility with every previously graded question record. It preserves the full prior mathematics/native evidence byte-for-byte.

Interface verification command: `.venv/bin/python generate/scratch/17592186184352/interface-validation.py`. `prior-validation-before-interface.json` preserves the prior bounded mathematics/native summary; `validation.json` links its generator version to the unchanged-record compatibility proof.
