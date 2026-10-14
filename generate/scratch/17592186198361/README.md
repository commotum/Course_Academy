# Performing a Change of Variables (local draft)

Implemented in `../17592186198361.py`, stopped after steps 3–7 with zero database writes. Frozen provenance: math basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.

Run:

```sh
.venv/bin/python generate/scratch/17592186198361.py --difficulty all --seed 31 --count 2 --format json
.venv/bin/python generate/scratch/17592186198361/validate.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus documented easy/moderate/hard entrypoints. Parameters are exact integer `ul,uh,vl,vh`. Only observed radio layouts are supported; `field_type='radio'` or its schema enum is accepted. Template names and bounds are in classification.md and template-extraction.md. Normal sampling chooses complete family banks and rejects every instance with equivalent full answer values.

Use `profile='observed'` and source-cases.json for public source replay. These records always carry evidence_only=true/eligible_for_learning=false; two preserve missing difficulty/solution/correct refs, and one contains equal complete integral answers. They are evidence, not completed practice records. Normal defaults complete the unrated difference question explicitly, use method-derived banks for opaque sources, and author the absent hard level using the same supplied nonlinear transformation with a squared integrand. The malformed sum/product original remains excluded from practice because its rectangular-image and injectivity assumptions fail; no missing key is invented.

Validation separates exact bank/prose/key-presence replay from mathematical validity and real native ID grading. It parses actual printed coordinate definitions, integrands, bounds, options, determinant/inverse blocks, substitution/expansion rows, primitives and both endpoint components. It rejects an algebraically equal mutation that removes the expanded-square stage, correlated endpoint errors that preserve the final result, and C0 control bytes. It checks all 84 moderate and 45 hard tasks in the finite nonlinear domain, plus 60 easy sampled records covering all five families and changed-parameter scope boundaries. Native radio checks use the shared memory-only harness; source missing-key records cannot supply grading fixtures and are explicitly excluded from native-source counts.

Raw evidence: source.json, source-cases.json, templates.json, source-analysis.json. Review: review.md and review.json. Validation/native summaries: validation.json/native-report.json. No writes outside this script's own scratch evidence directory are required.
