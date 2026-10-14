# Two multivariable polynomial LCM generator

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186152118/validate.py
.venv/bin/python generate/scratch/17592186152118.py --difficulty all --seed 42 --count 2
.venv/bin/python generate/scratch/17592186152118.py --difficulty hard --format json
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)`; separate `generate_easy`, `generate_moderate`, `generate_hard` wrappers. Two templates: factored_blank/factored_radio. Full source replay cases are in source-cases.json, with `observed_q-*` raw and `completed_q-*` independently completed profiles. Normal banks use method_bank.

Scope: exactly two already factored multivariable polynomials, exactly two independent monic linear factor bases, integer content LCM and maximum powers. Hard and moderate/hard radio layout are authored; one unrated source's level/key/solution are completed separately. All14 source values remain exact, including two interpretation-limited expression patterns used only for replay. No plots or database writes. Validation reads actual displayed prompts, all complete choices and every ordered formal/arithmetic/prose stage, compares complete source solutions, rejects invalid explicit parameters and invokes the native grader. frozen-manifest.json records hashes. Independent parent QA passed; see parent-qa.json.

Known native-grader limitation: a fully expanded high-power equivalent can exceed the512-token input cap. Such entries are separately documented as unresolved; compact factored, partially expanded and unreduced equivalents are tested as accepted. No engine changes.

Replenishment: `.venv/bin/python generate/scratch/17592186152118/replenish.py` rechecks inventory, executes the generator CLI, validates displayed mathematics and actual grading, and serializes additive EDB registration/content commits with the application api.lock. Exact requests, previews, receipts and exact-basis verification are retained under reference/replenishment. Generated content uses application/ca-engine attribution. Captured unrated incomplete source is preserved and excluded.
