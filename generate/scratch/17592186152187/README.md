# Origin-centered ellipse parametrization

Local script: `../17592186152187.py`. Scope: select or construct full origin-centered ellipse parametrizations; easy graph reading, moderate supplied radii and traversal, authored hard half-unit graph reading and traversal. No EDB writes or engine edits.

Verification:

```sh
.venv/bin/python generate/scratch/17592186152187/validate.py
.venv/bin/python generate/scratch/17592186152187.py --difficulty all --seed 4 --count 2 --format json
```

Public source replay uses `generate(level, template=case['template'], parameters=case['parameters'], profile=case['bank_profile'])` with `source-cases.json`. `observed:` profiles preserve raw missing attributes and duplicate legacy layout; anomaly/opaque records are explicitly evidence-only. Normal profiles omit the legacy field and infer missing source completion; these repairs are counted separately from captured correct designations. q-106701's opaque bank has no normal profile; other fully method-derived complete banks serve that graph family. Source source-cases contain all practice records, including the unrated one.

`validation.json` reports full bank/value fidelity, exact prose/key-presence replay, notation normalization, mathematical checks and actual native grading separately. `review.md` and `review.json` contain originals, changed variants for every source bank and at least two examples at each level. `freeze.json` records private generator/evidence hashes. Renderer uses the cached Python 3.10 Matplotlib environment read-only if the primary .venv has no Matplotlib; no installation occurs.
