# Integrating Secant Squared — unregistered draft

Script: `../17592186064180-draft.py`. This draft preserves the registered numeric script and all its prior evidence unchanged. It has no database, registration or engine writes.

Verify from the repository root:

```bash
.venv/bin/python generate/scratch/17592186064180-draft/validate.py
.venv/bin/python generate/scratch/17592186064180-draft.py --difficulty all --seed 91 --count 2 --format json
```

Public interface: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`, plus `generate_easy`, `generate_moderate`, `generate_hard`. All normal records have a five-choice radio field. CLI supports optional `--template`/`--profile`. Exact raw replay uses `profile="raw:q-ID"` and the corresponding template/parameters in source-cases.json; raw records deliberately preserve missing difficulty, fields, keys and solutions and are evidence-only.

Evidence is immutable math basis2275. Raw fidelity: ten prompts, eight available worked solutions, seven full radio banks (35 choices), five captured keys and two preserved absent keys. Five independent inventory records are exact, separate records. The only opaque historical bank is q-49118; its complete expression pattern is public but never a learning default. Missing-field completions and unrated completions use separate authored method banks. Hard is an authored conservative combination of three directly recalled terms with the source distribution/sum rule; its difficulty calibration remains uncertain.

Semantic domains contain54 easy,227 moderate and1458 hard mathematical tasks after removing bank and notation aliases. Review contains every original/replay/changed evidence pair and at least two generated variants for every normal family. Source-shaped normal solutions retain their source wording and operative chain. No plots/assets are required.

Validation differentiates every displayed primitive and formal integral stage from actual learner text, compares full banks modulo arbitrary antiderivative constants, checks every owned choice with the real memory-only native grader, tests boundary guards, changed slots, IDs, profile coverage and mathematical/structural corruption. Validation and grader provenance are in validation.json and engine-provenance.json. Registered baseline before/after pathset and hashes are recorded separately.
