# Inhibited decay identification generator

Script: `../17592186078582.py`. Math capture basis 1356; seven sources, three observed templates, six complete bank/notation profiles. No plots or database writes. Easy recognizes factored negative linear form, moderate factors expanded form, hard also checks an initial value above equilibrium. Applications and solving belong to sibling KPs.

```sh
.venv/bin/python generate/scratch/17592186078582/validate.py
.venv/bin/python generate/scratch/17592186078582.py --difficulty all --seed 42 --count 2 --format json
.venv/bin/python generate/scratch/17592186078582.py --difficulty hard --profile ivp_decimal_grouped --seed 31
```

Validation independently parses learner-facing equations and solution intermediates; compares every complete original bank and exact source wording; tests invalid inputs, corrupted banks/math/solutions/identities, deterministic identities; renders representative math; and exercises every option in the actual native learning grader. A failure exits nonzero and writes `passed:false`. No correctness claim is based solely on selected answer IDs.

Math preview rendering uses read-only cached Matplotlib and Python 3.10 when Matplotlib is absent from the primary Python 3.13 environment. `render-provenance.json` records dependency paths; nothing is installed or downloaded. The validation command remains `.venv/bin/python`.

q-105893 lacks an observed difficulty/correct reference/solution. Its full bank and prompt match exactly; unique correct equation and moderate label/solution are explicitly authored repairs. Six available source designations and solutions match exactly. See classification.md, template-extraction.md, q-105893-widget.json, and raw source.json. No unresolved mathematical bank discrepancies remain. Review includes every original and two generated examples for every profile (four per level). Rendered images are typesetting checks, not new plots.
