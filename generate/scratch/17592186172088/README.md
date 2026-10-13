# Identifying a Three-Dimensional Vector Field

Local generator at `../17592186172088.py`; no registration, EDB writes, or transactions.

```bash
.venv/bin/python generate/scratch/17592186172088/validate.py
.venv/bin/python generate/scratch/17592186172088.py --difficulty all --seed 4 --count 2 --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and individual easy/moderate/hard entrypoints. Parameters are `permutation` (one of xyz, xzy, yxz, yzx, zxy, zyx), `flip` (±1), `scale` (integer 1..3). Explicit invalid inputs fail. Template names: constant_sign, constant_match, constant_none. Source cases replay exact bank, problem prose, images and solution stages through this API. Explicit `observed:q-123750` preserves its documented source explanation error; `q-123750` and normal sampling use the supported correction.

Ten original practice questions: 7 moderate, 3 hard. Easy is authored within constant field axis/sign recognition. All levels preserve 5 choices and the radio field. Meaningful plotted target count is six per level; positive common scale and banks do not inflate it. Native grader verifies every owned answer selection. Validator parses displayed formulas independently and checks source banks/prose, elimination logic, domains/zero sets, identity, formatting, complete sampler bounds and fresh concurrent renders. Source reasoning errors are reported separately from exact fidelity.

`render.py` uses cached Python3.10/Matplotlib dependencies read-only when project Python lacks Matplotlib; no dependency installation or shared environment edits. Generated PNG/JSON assets remain under this evidence folder. `review.md` pairs each original with two labeled changed-parameter variants, plus two authored easy examples; `review.json` contains these generated variants.
