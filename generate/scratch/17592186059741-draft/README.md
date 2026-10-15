# Scalar recovery draft

Owned implementation: `../17592186059741-draft.py`. Immutable numeric generator/evidence and matching sibling bytecode are audited in baseline.json and baseline-verification.json; none are imported or modified. No shared, registration, EDB, engine or manifest writes.

Run from repository root:

```
.venv/bin/python generate/scratch/17592186059741-draft/validate.py
.venv/bin/python generate/scratch/17592186059741-draft/render.py
.venv/bin/python generate/scratch/17592186059741-draft.py --difficulty all --count 1 --seed 0 --format json
```

The rendering command needs localhost binding/headless Chromium permission. It uses actual player Markdown, field controls, sanitization and MathJax, inspecting errors, undefined output, matrix dimensions, field slots and overflow. Screenshots are private evidence.

API: generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None), generate_easy/moderate/hard and batch. Raw evidence profile: raw-q-981 (matching template q-981), similarly all seven originals. Explicit parameters contain matrix (exact integer strings), scalar (exact rational string) and target ([zero-based row,column]). Method banks are default. Evidence profiles are ineligible, including exact raw source with known mathematical/context defects. CLI count1 always returns a list; difficulty all returns three records. All seeds/counts require built-in integers.

Snapshot: basis2275 refresh of2026-10-14, exact wrapper in source.json. Seven original MA practices, nineteen complete source answer values, six stored correct designations; one source has no correct reference. No independent captured inventory. See classification.md and template-extraction.md for repair accounting and authored moderate/hard rationale. Root independent QA/approval remains pending.
