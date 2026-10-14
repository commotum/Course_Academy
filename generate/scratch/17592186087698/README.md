# Identifying Other Matrices generator

Registered script: `generate/scratch/17592186087698.py`. Generator UUID: `59ccd5bd-2e7f-5a1b-9d4e-06ec327ee7f6`. KP UUID: `7b6ddadb-471a-5195-a0f5-fd44bdc8f780`.

The generator emits local JSON/Markdown only; database preparation/commit is a separate scoped workflow. System Python falls back to the existing repository `.venv/bin/python` when SymPy is unavailable, matching scheduler execution without installing or changing application dependencies.

```sh
python3 generate/scratch/17592186087698.py --difficulty easy --count 5 --seed 20261013 --format json
.venv/bin/python generate/scratch/17592186087698/validate.py
.venv/bin/python generate/scratch/17592186087698/replenish.py
```

Only easy is supported. Moderate and hard leave explicit nominal shortages in capabilities.json; invoking those levels fails. The bounded normal domain contains at most 830 distinct mathematical recognition tasks before excluding existing or exposed tasks. Entries, labels, seed and choice order do not establish distinct tasks. Source replay covers all five complete easy banks and both source checkbox families; two incomplete unrated source radios remain untouched. The canonical example is never practice inventory.

Validation independently parses the printed matrix dimensions/entries, checks solution targets and every field's correct key, tests actual learner grading, rejects boundary violations, and freezes script/source/validator hashes. source-components.json maps every original choice. review.md and review.json retain originals and variants. No plots or assets are needed.

The first locked recheck at basis 2198 found five distinct unseen gradable easy source questions, so no new questions were persisted. Only the generator registration was committed through `:application/ca-engine` at basis 2199. Exact EDN, basis-guarded request, preview, receipt and readback are retained under reference/replenishment/basis-2198. All seven source questions, canonical example and learner history were verified unchanged. Repeated execution recovers this exact request and verifies it before any new intent.

The registration-time script, validation, and freeze snapshots are archived as `at-commit-*` files alongside the request. The current frozen version adds the system-Python fallback and prevents a randomly sampled all-ones diagonal from becoming an out-of-scope identity matrix; it has the same registered UUID/path and preserves the supported templates and all source replays. runtime-verification.json records the scheduler CLI check and current hashes. No scheduler, other application code, or other KP is changed.
