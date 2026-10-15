# Private constant-multiple power substitution draft

Script: `generate/scratch/17592186068723-draft.py`. Evidence: this private tree. No database write, registration, queue/engine/shared-QA edit, commit, or child agent is involved. The registered numeric script and all existing evidence/cache paths remain untouched; `registered-baseline.json` predates imports and `preservation-proof.json` compares full path sets and file bytes.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186068723-draft/validate.py
.venv/bin/python generate/scratch/17592186068723-draft/diagnostics.py
.venv/bin/python generate/scratch/17592186068723-draft.py --difficulty all --count 2 --seed 7 --format markdown
```

The CLI also accepts `--template` and `--profile`. Python exposes `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, all three difficulty helpers, `capacity`, and finite deduplicated `batch`. Parameters contain exactly the nonzero inner constant `b`; fixed mathematical parameters are reported separately. Original replay profiles are `source:q-...` and always ineligible evidence; ordinary `q-...` profiles are normal records. Hard profile names are `hard-signed-cubic-root` and `hard-signed-square-root`.

Basis 2275 source/context wrappers are copied unchanged. `classification.md` and `template-extraction.md` state the level and slot bounds. `bank-recipes.json`, `source-cases.json`, `source-fidelity.json`, `independent-inventory.json`, `review.json` and `review.md` distinguish raw originals, opaque banks, repairs, changed variants and authored hard. q-12494 is retained as incomplete raw evidence and separately completed normally. q-113715's dropped +C row is repaired normally. Normal q-12496 uses an explicitly authored method bank; its full original bank stays in public raw replay.

`validate.py` reads printed TeX independently over all 920 normal and 800 raw bounded variants, checks every bank modulo additive constants and every displayed solution stage, runs real native grading for all supported normal records, verifies strict API/capacity/identity rules, and rejects targeted printed-math/stage/format mutations. `diagnostics.py` separates foreign/malformed radio transport from correct/wrong owned-ID grading and records legitimate +1 primitive equivalents. Its authored blank fixtures expose the actual native equality grader's inability to recognize arbitrary-constant shifts; those equivalents are valid mathematics, never wrong-answer probes. Logarithmic scale equivalence is outside this KP. Radio output remains fully supported.

Formatter and mathematical parser are private copied modules loaded by explicit file paths. Native grading uses this tree's exact frozen application engine executable. `freeze.json` records implementation/source/dependency hashes and runtime versions. No runtime imports from live `scripts/question_capture` or registered numeric files occur.
