# Separable initial-value generator

`../17592186100893.py` implements easy/moderate/hard with deterministic API and CLI. Twenty captured source templates preserve whole original banks, RHS-only blanks, and worked stages; three labeled coefficient extensions provide further same-skill variety. No plots or database writes.

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186100893/validate.py
.venv/bin/python generate/scratch/17592186100893.py --difficulty all --seed 42 --count 2 --format markdown
.venv/bin/python generate/scratch/17592186100893.py --difficulty easy --template source_8310 --profile observed --format json
```

`source-cases.json` replays originals through the same normal generator and explicit original profiles. `validation.json` separates full displayed-value fidelity, independent primitive/ODE/initial-value checks, and actual native grading. `solution-stage-validation.json` records parsed algebraic stages and derivative/branch handling. `review.md`/`review.json` include every original template and multiple generated instances at all three levels. Source empirical profiles intentionally make no claim about original distractor intent. All full radio equations and RHS fragments are independently parsed by `parse_math.py`; unsupported TeX fails closed.

`native-grading-limitations.md` documents one additional unsupported split-exponential learner entry. Canonical and expanded-exponent equivalent entries pass; the unsupported product form is reproduced separately in `engine-equivalence-limitation.json` and is not counted as accepted.

Parent QA canonicalizes the mathematical fingerprint from the displayed task's
ODE, initial values and requested particular relation, independently of
field type, template names and parameter spelling. Equivalent reciprocal source/extension
layouts deduplicate while their different displayed banks retain separate
question identities. `generate/runs/current/qa-ivp.py` independently reads the
printed IVPs and verifies differentiation, initial conditions and every source
bank; the native grading limitation remains explicit.
