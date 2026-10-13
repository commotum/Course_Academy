# Triangle area from quadrilateral generator

Draft review only; no registration, database writes, or shared changes. Basis1356 source capture is preserved in source.json. The script supplies easy, moderate, hard entrypoints and JSON/Markdown CLI.

```sh
.venv/bin/python generate/scratch/17592186105906/validate.py
.venv/bin/python generate/scratch/17592186105906.py --difficulty all --seed 12 --count 2 --format markdown
```

Use `generate('hard', template='q-18192', parameters=..., profile='raw_q-18192')` for public faithful omission replay. `repaired_q-*` profiles are evidence-only minimal repairs with opaque historical banks. Ordinary defaults use complete method-derived authored banks and preserve the source arithmetic-stage families. classification.md describes the authored missing levels; template-extraction.md maps every source choice/stage/error; plot-extraction.md specifies full-resolution inspected rasters and Matplotlib geometry. review.md/review.json show originals, supported repairs, two generated examples per source family plus authored easy/moderate examples. validation.json and native-report.json report exact replay separately from correctness/grading.

Unresolved: intended historical radio error operations cannot be recovered from lone scalar banks. q18192 has no observed key/solution/difficulty; these exist only as explicitly inferred/authored repairs. Raw q285754 has an intermediate unit typo, and three raw substitution rows transpose the side labels. No repair is counted as raw fidelity. All raw/opaque records carry eligible_for_learning=false and evidence_only=true.

Native nearest-integer checking accepts canonical integer entries and surrounding whitespace; mathematically equivalent unevaluated expressions and leading-zero numerals are rejected by its form-sensitive rounding check. This is tested and retained because genuine rounding is requested.
