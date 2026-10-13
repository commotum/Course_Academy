# Stokes circulation generator

Frozen local draft; steps 3–7 only. No registration or database writes.

```sh
.venv/bin/python generate/scratch/17592186133927/validate.py
.venv/bin/python generate/scratch/17592186133927.py --difficulty all --count 2 --format json
```

API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), plus all three difficulty entrypoints. Normal parameters are k, a, h. Raw evidence profiles are raw:q-ID with only k; all originals remain publicly replayable including missing attributes and legacy banks. Raw evidence is always ineligible. Defaults choose supported source-shaped families and complete method banks, with whole-instance collision rejection.

See classification.md and template-extraction.md for exact source mapping, authored missing easy and normal repairs; validation.json separates fidelity, mathematics and native checks. Source scalar error intent remains opaque. review.md labels original evidence and generated variants. Matplotlib renderer uses read-only cached dependencies and private atomic assets. There are no hidden unresolved grading failures.


Final QA: 66 normal records independently checked from displayed math; 83 native accepted and 283 rejected checks; no native unresolved outcomes. Source fidelity: 11/11 questions, 12/12 fields, 56/56 options, 10/10 available correct designations, 10/10 supplied solutions. Two absent correct refs and one absent solution remain absent in public raw evidence. The malformed legacy bank, ambiguous integral bank, incomplete prompt and faulty historical primitive stages remain ineligible and are explicitly documented.

Finite-domain enumeration (`.venv/bin/python generate/scratch/17592186133927/enumerate.py`) gives 32 easy, 168 moderate and 152 hard mathematical tasks; source-math-audit.json records independent complete historical bank evaluation, and render-concurrency.json records fresh concurrent atomic writes. freeze.json records final file hashes for parent QA.

Root QA updated the region renderer to version 4: plain labels clear of axes, arrows inside actual integration slices, and actual 140-dpi geometry/hash sidecars. Markdown CLI output now labels provenance, actual difficulty and designated answers; source image paths resolve in previews. Stored question values were unchanged by the Markdown-only patch.
