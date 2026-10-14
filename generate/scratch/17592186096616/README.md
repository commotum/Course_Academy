# Logarithmic tangent slopes

Frozen basis 1356. Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186096616/validate.py
.venv/bin/python generate/scratch/17592186096616.py --difficulty all --count 2 --seed 7 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and three level entrypoints. Default normal profile is `method`; public evidence profiles are `raw:q-NNN`, with parameters in `source-cases.json`. Raw unrated replay uses the easy API routing level but omits the actual difficulty attribute. Raw source metadata includes evidence-only/ineligible flags. Source parameter replay reconstructs masks and banks; it never returns source payloads or uses answer lookup tables.

No plots. `source.json` is the complete captured wrapper. `masks.json` and its documented extraction script specify the ordered roles in whole mathematical components. `review.md/json` contain all original/raw/normal/variant comparisons and two defaults per level. `validation.json` separates fidelity, mathematics and native grading. Old draft/replenishment artifacts live only in `archive-pre-frozen1356/` and are not current evidence. No EDB writes or registration.

Moderate/hard definitions are authored conservative calibrations; see classification. Complete historical banks preserve expressions but some wrong-answer interpretations remain unknown and are never promoted to defaults. Native numerical scientific-notation tokenization can misread an ungrouped coefficient followed by Euler e and +integer; normal stored scalar answers use explicit multiplication when Euler e is unpowered. Source raw spellings remain intact.

`parser-limit-input.json` is a separately labeled native parser probe, not a generator/source record. The real grader rejects `8e+4` against the Euler scalar while accepting `8\cdot e+4` and `4+8e`; `parser-limit-report.json` records those outcomes. Normal unpowered Euler coefficients are rendered with explicit multiplication.
