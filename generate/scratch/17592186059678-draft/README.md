# Draft generator and review

Run from the repository:

```
.venv/bin/python generate/scratch/17592186059678-draft.py --difficulty all --count 1 --seed 173 --format json
.venv/bin/python generate/scratch/17592186059678-draft/validate.py
```

JSON output is a flat list. `all --count 1` returns three records; count is per level. Markdown and JSON are supported for easy, moderate, hard and all. Invalid counts, booleans, unsupported profiles/levels, incompatible profile selections, malformed parameter keys/types and capacity overflow fail closed.

Read classification and extraction before reviewing. `source.json` preserves the full basis-2275 Pull snapshot including omissions and source identities. `source-cases.json` contains only MA originals and exact raw record replays with ID/parameters. `independent-inventory.json` isolates independently authored inventory. `served-originals.json` is actual normalized source-template replication. `source-replay.json` reports full bank, key, prompt and solution fidelity separately from correctness. `side-by-side.json` and `review.md` compare every source profile and authored hard variant.

The private validator independently parses the actual printed supplied function and every intermediate, validates formal derivative order, operator input, target, names, domain, whole banks and field contracts, then executes mutation controls. Exact SymPy and private parser/formatter versions/hashes are in `runtime.json`. Native grading uses the frozen root check-engine binary with required SHA; it never accesses EDB. It exhausts the public finite catalog, testing canonical/equivalent blank responses, ordinary wrong 0/1/+1, all owned radio IDs, and the partial-blank trap. Foreign-ID diagnostics are isolated. See capacity and validation reports for actual counts.

`registered-baseline.json` records the entire registered filepath set and SHA256 values captured before importing any generator. Validator verifies those paths and hashes remain unchanged. `freeze.json` records the draft's hash set. Worker validation leaves root independent review pending; no DB writes, registration changes, commits, shared QA or engine edits occur.
