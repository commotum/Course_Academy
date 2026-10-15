# Triangle area from quadrilateral generator

Validated generator with easy, moderate and hard entrypoints and JSON/Markdown CLI. Current source capture is basis2738; the original basis1356 capture is preserved under reference/. Publication evidence and exact receipts are under reference/replenishment/.

```sh
.venv/bin/python generate/scratch/17592186105906/validate.py
.venv/bin/python generate/scratch/17592186105906.py --difficulty all --seed 12 --count 2 --format markdown
```

Use `generate('hard', template='q-18192', parameters=..., profile='raw_q-18192')` for public faithful omission replay. `repaired_q-*` profiles are evidence-only minimal repairs with opaque historical banks. Ordinary defaults use complete method-derived authored banks and preserve the source arithmetic-stage families. classification.md describes the authored missing levels; template-extraction.md maps every source choice/stage/error; plot-extraction.md specifies full-resolution inspected rasters and Matplotlib geometry. review.md/review.json show originals, supported repairs, two generated examples per source family plus authored easy/moderate examples. validation.json and native-report.json report exact replay separately from correctness/grading.

Unresolved: intended historical radio error operations cannot be recovered from lone scalar banks. q18192 has no observed key/solution/difficulty; these exist only as explicitly inferred/authored repairs. Raw q285754 has an intermediate unit typo, and three raw substitution rows transpose the side labels. No repair is counted as raw fidelity. All raw/opaque records carry eligible_for_learning=false and evidence_only=true.

Native nearest-integer checking accepts canonical integer entries and surrounding whitespace; mathematically equivalent unevaluated expressions and leading-zero numerals are rejected by its form-sensitive rounding check. This is tested and retained because genuine rounding is requested.


## Inventory publication

Version1.1.0 extends the frozen source capture to eleven records at basis2738 while retaining the original basis1356 capture under reference/. Native validation now uses reference/check-engine-current compiled against the application's current release engine. Run `replenish.py --prepare-only` to inspect fresh inventory and candidates; `replenish.py` previews, saves the exact request, commits with a basis guard under api.lock, and verifies additive datoms and source preservation at db-after. Durable requests, receipts, inventory rechecks and verification are under reference/replenishment/. The registered UUID is deterministic under the KP UUID and reused on subsequent runs. No source question or learner record is modified.
