# Describing Properties of the Cosine Function

Generator: `../17592186176047.py`; captured database `math`, basis 1356. Run from repository root:

```bash
.venv/bin/python generate/scratch/17592186176047/validate.py
.venv/bin/python generate/scratch/17592186176047.py --difficulty all --seed 8 --count 2 --format json
```

The normal API is `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, with easy/moderate/hard convenience functions. Source replay uses all eight explicit inputs in `source-cases.json`; e.g. moderate, template q-103230, profile observed-q-103230, explicit slot parameters from that file. Recorded enums/UUIDs are local review JSON, not database transactions.

Validation exhausts all **32 easy, 72 moderate and 216 hard** authored semantic claim sets, checks changed observed masks and full original banks, and calls the real native grader on canonical/equivalent/wrong entries. Variation is finite and stays within the unit cosine graph. Easy/hard labels are authored because no source examples have those labels. The later periodicity/evenness sibling KPs are not included.

Eight original prompts and 40 answer values replay exactly. All six available original solutions and correct question designations match; two original keys/solutions are missing and independently supplied, never counted as exact matches. q-167631 is a sine mislink: raw replay remains available; normal generation repairs it to cosine with the inspected matching raster. Its TeX answers have valid single slashes. All 300 native checks pass with zero unresolved checks.

`review.md`/`review.json` show every original, public API replay and changed normal variant, then two examples for every difficulty. Classification/extraction/plot evidence and hashes are local. Work stops after steps 3–7, with no registration or database writes.

Incorrect symmetric range bounds 2, 3 and π are incidental magnitudes in a truth-classification task: their lower/upper endpoint positions are identical relative to [-1,1], so they share a mathematical fingerprint. Similarly, output magnitudes outside the range share the below/above classification fingerprint. Their actual displayed values still affect complete content identity and source-bank fidelity.
