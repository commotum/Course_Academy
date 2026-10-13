# Integrating Secant-Tangent and Cosecant-Cotangent

Generator: `generate/scratch/17592186064179.py`. Source capture: math basis 1871, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Generator UUID derives from the existing KP UUID and is reused for registration. The script runs in the repository's existing SymPy environment, including when launched by system Python.

`classification.json`, `extraction.md` and `templates.json` preserve every source assignment and exact component/bank mapping. The six supported complete source banks use radio fields. One additional complete bank is ambiguous and explicitly excluded; five other sources are incomplete or unrated. No source is edited. Hard has no source-backed capability and its nominal shortage stays explicit in `capabilities.json`.

Run mathematical, full-domain, fidelity and actual learner-grader validation:

```sh
.venv/bin/python generate/scratch/17592186064179/validate.py
```

Run seeded previews without database operations:

```sh
python3 generate/scratch/17592186064179.py --difficulty easy --count 5 --seed 123 --format json
python3 generate/scratch/17592186064179.py --difficulty moderate --count 5 --seed 123 --format markdown
```

Counts are bounded: 16 parameterized easy integrands and 171 moderate integrands, with the observed negative-unit easy profile retained as a singleton replay. `batch` returns fewer instances at exhaustion; it never pads. The integrand fingerprint normalizes variable names and excludes seed, identity, bank and ordering. Content identity includes the complete authored bank and fixed solution. New instances are filtered against every existing source/generated integrand and the canonical example before commit.

`replenish.py` uses the application's existing EDB integration, native inventory reader and native preview validator. It takes `.local/learning/requests/math/api.lock`, rechecks inventory, lineage and basis, verifies unchanged source evidence, validates supplied `.generated` artifacts if present, and prepares additive content plus generator registration. Every submission retains exact EDN, stable request key, source, basis guard, lineage and receipts. Readback checks all affected records at the exact committed basis and confirms the receipt contains no source mutation, learner mutation, unrelated KP mutation or retraction.

```sh
.venv/bin/python generate/scratch/17592186064179/replenish.py
```

A repeat run reconciles the saved exact request and readback before considering any new intent. It does not create additional questions solely because a different seed or bank can be selected. Inventory exclusions and remaining unsupported/incomplete source work stay visible in the job's JSON result.
