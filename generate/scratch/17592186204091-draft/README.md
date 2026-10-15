# Draft parameter generator

Registered `../17592186204091.py` and its entire finished artifact directory remain unchanged. `baseline.json` records their pre-import path set and SHA-256 hashes. This draft is local only: no database mutation, registration, engine change, or commit.

Run `.venv/bin/python generate/scratch/17592186204091-draft/validate.py` to reproduce private exact fidelity, algebra, API, capacity, CLI, native grading, and baseline checks. Run `python3 generate/scratch/17592186204091-draft.py --difficulty hard --seed 811 --count 5 --format json` (or `markdown`) for seeded previews. Public `generate_easy`, `generate_moderate`, `generate_hard`, `generate`, and `batch` produce served content. `replay_source(math_academy_id, original_parameters=None)` returns a deep copied complete raw Pull record, preserving missing attributes too; it is evidence only and does not claim eligibility.

Source basis is 2275. Every complete MA source is replayed before extensions. The incomplete MA source remains raw. Hard is an authored conservative same-method rating with no observed hard source; see `capacity.json` for overlap. Finite normalized-equation capacities are easy 144, moderate 543, hard 432. Parameter roots, unequal constant pairs and eligible outer scales provide arithmetic variety; labels, seeds, IDs, ratings and uniform entire-equation scaling do not inflate it. No plots occur.

Served coefficient annotations use canonical `\underbrace{operand}_{a/b}`. The private formatter repairs legacy Unicode capture wrappers without changing operands, roles, source wording or raw Pull records. Fidelity separates mathematical/full-prose preservation from this presentation normalization. The private parser checks annotation operands and roles independently and rejects legacy wrappers, stale coefficients and stale role labels.

CLI `--difficulty all --count N` emits a flat JSON list with N questions per easy/moderate/hard level, or the corresponding flat Markdown preview. `cli-validation.py` checks both formats at counts 0, 1, each relevant capacity boundary and invalid inputs.
