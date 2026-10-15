# Evaluating Definite Integrals draft

Frozen math basis2275. No EDB writes, registration, shared QA edits, or engine changes. Source wrapper and private dependency snapshots are preserved.

Run from repository root:

```bash
.venv/bin/python generate/scratch/17592186184352.py --difficulty all --count 1 --format json
.venv/bin/python generate/scratch/17592186184352/validate.py
```

Eight parameterized source families span easy/moderate/hard. q-30977 has an explicitly authored moderate designation, correct reference, and missing solution. Normal radios use an explicitly authored complete method bank; observed complete banks replay with source_bank. Source blank wording replays with source_presentation; normal source_blank avoids the known native “round” form restriction. source-cases.json lists the exact public replay inputs. capacity.json and validation.json separate source fidelity, displayed mathematics, bounded variety, and native grading. review.md pairs originals and variants. Parent independent review remains required.

Native grading limitation: a valid general log difference such as `2(ln(11)-ln(5))` is unresolved against `2ln(11/5)` by the frozen engine. Supported unreduced endpoint ratios pass throughout the full hard domain. This is recorded separately from malformed input and ownership diagnostics and requires parent review; native grading is not claimed unrestricted.
