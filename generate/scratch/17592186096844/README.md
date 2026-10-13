# Chain and quotient rules generator

Script: generate/scratch/17592186096844.py. Generator UUID: 5d07f6a1-5bae-51f9-8a91-974d704729c8. KP: 17592186096844. Source basis: 1943; math lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Read classification.md, template-extraction.md, plot-extraction.md and capabilities.json before extending bounds or levels.

Supported: moderate and hard. Easy lacks evidence for a validated template and stays explicit. The hard family has nine distinct tasks, including its one valid source task. Never replenish by copying a task under another UUID, seed, or answer order. The generator may return fewer records than requested when its finite task universe is exhausted.

```bash
python3 generate/scratch/17592186096844.py --difficulty hard --count 5 --seed 27 --format json
.venv/bin/python generate/scratch/17592186096844/validate.py
.venv/bin/python generate/scratch/17592186096844/replenish.py
```

The generator's system-Python entry point delegates to the existing project virtual environment when SymPy is unavailable. `generate(level, seed, template, parameters, profile)` supports exact source replay; `batch` rejects bank collisions and deduplicates tasks. Generated questions retain original field keys, field-owned answer UUIDs, math value types and response shapes. The motion prompt repair is explicitly documented and does not overwrite source facts.

validate.py independently parses displayed math, checks complete source banks and all computed solution stages, checks deterministic replay and native learner grading. It saves source/variant review.md and separate correctness, fidelity and grading evidence. Original source records always remain in source.json. No plots are needed.

replenish.py uses the existing Database, native inventory, native predicate preview and durable commit interfaces. It resolves :application/ca-engine, locks the application's api.lock, rechecks current source and inventory at one basis, validates distinct eligible records, persists exact typed EDN and intent, previews and submits with a basis guard, verifies exact receipt and db-after, checks additive datoms and unchanged source records, and saves the inventory/result. Existing saved requests are reconciled before new intent; receipts are preserved. The application, scheduler and other KPs are not modified.
