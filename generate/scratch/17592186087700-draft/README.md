# Larger-matrix inverse verification draft

Local steps 3–7 only. Script: `../17592186087700-draft.py`. No registration, transactions, shared-engine writes, commits or numeric-generator imports. The baseline numeric script, directory and matching pycs were absent before imports; baseline.json records that capture.

Run from the repository root:

```
.venv/bin/python generate/scratch/17592186087700-draft/validate.py
.venv/bin/python generate/scratch/17592186087700-draft/render.py
.venv/bin/python generate/scratch/17592186087700-draft.py --difficulty all --count 1 --format json
```

The API is `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, with named wrappers for all three levels. JSON CLI always returns a list, including all/count1 → three records. Explicit parameter dictionaries are strict; source parameters contain a permutation, coordinate signs and one witness per solution stage. Unknown templates/profiles/levels and out-of-scope inputs fail. Batches deduplicate actual mathematical objects/roles and use bounded search with an explicit finite-bank exhaustion error. Exact capacities are easy 120, moderate 204 and hard 288; each source mask has only 12, 24 or 96 tasks. Requests beyond the applicable finite capacity fail before sampling.

Raw source public profiles are evidence-only. Normal profiles repair documented source defects. Easy is authored and uncalibrated; transformed source-level instances are also uncalibrated design claims. Arithmetic, full source prose/stages, all banks, default family coverage, target variation and negative controls are checked separately from the real native grader and player rendering. Native Boolean fields grade selected true/false answer IDs; symbolic equivalent-entry blank probes are inapplicable. No native engine fixes are included.

check-engine is a private read-only copy of the parent's current native helper. reference/grader-build.json is copied unchanged, and all 42 referenced source/library/binary/dependency hashes were verified before copying. The stale runs/current/check-engine executable is not used.

Parent independent QA and approval remain pending. freeze.json provides the final owned immutable path set and SHA-256 hashes; its own SHA is reported separately.
