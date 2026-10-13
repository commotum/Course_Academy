# Integrating-factor general-solution generator

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186087878.py --difficulty all --seed 3 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186087878/validate.py
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and easy/moderate/hard wrappers. Field type is select; both IF and solution fields are retained. CLI supports difficulty, seed, count, JSON/Markdown and complete template/profile selection. Original parameters/cases live in `source-cases.json`.

Eight captured sources at math basis 1356. The three unrated originals receive explicitly authored supported levels, correct refs and explanations. Five stored explanations and eight prompts replay exactly. Raw hard bank has a duplicate correct option: its original profile permits fixed-parameter evidence-only replay and rejects random learner generation; `q-335409-repaired` preserves five choices with one documented wrong exponent replacement. Raw fidelity and normal repaired fidelity remain separate. `source.json` is untouched evidence; `bank-mapping.json` maps every captured option.

Normal defaults use separately labeled authored banks; hard cosine is a peer anchored to canonical e-21742. Scope is general solutions using IF and direct integration/one IBP; no initial conditions or additional ODE branches. No plots. `review.md` shows all originals and two changed-parameter authored variants per template. `validation.json` records exact fidelity denominators, printed-stage checks, native select grading and frozen script SHA. The grader calls the real application in memory and performs no database operations. No registration, engine edits, shared writes or commits. Work stops after step 7.

Raw replay example (review evidence, never a normal learner record):

```python
generate('hard', template='power_sin', parameters={'n': 2, 'r': 1}, profile='q-335409')
```

The returned generation metadata marks `evidence_only` and `raw_ambiguous_bank`; the repaired normal record uses profile `q-335409-repaired`.
