# 3x3 Gauss–Jordan generator

KP: `17592186096675`, UUID `95a32907-8304-5dfd-8759-9e91503445bf`.

The registered entry point is `generate/scratch/17592186096675.py`.
It supports **Moderate** questions with one `selection` radio field and five
field-owned math answers. Output is a JSON array accepted by the existing
inventory worker:

```sh
python3 generate/scratch/17592186096675.py --difficulty moderate --count 5 --seed 96675 --format json
.venv/bin/python generate/scratch/17592186096675/validate.py
.venv/bin/python generate/scratch/17592186096675/replenish.py
```

The generator uses Python's standard library and SymPy 1.14.0. If the invoking
Python lacks SymPy, the CLI uses the repository's existing `.venv/bin/python`.
It produces no plot assets. It does not access or mutate the database.

`source.json` retains the complete live source capture. `classification.json`
and `template-extraction.json` account for every source and every choice in
the 11 complete Moderate profiles. The extraction describes the conservative
fixed-coefficient policy and the explicitly inferred affine translation of each
complete observed choice bank. Causal interpretations of these offsets are
unresolved; no such interpretations appear in learner content.

Every varying template samples a different integer solution and derives its
right-hand sides and intermediate matrices consistently. Identity includes
the authored system, requested answer shape, profile and full choice bank;
seed and choice order do not create identity. Inventory deduplication uses
the augmented system itself, excluding alternate answer shapes for the same
system. The homogeneous source family has one replay-only variant.

`validation.json` records independent rendered-prompt and row-operation checks,
full source-bank replay, coordinate boundary coverage, deterministic replay,
and actual application grading. `reference/side-by-side.md` presents source
and variant examples for both response shapes. The review confirms that
equations, matrix columns, row-operation labels and final solutions agree;
the source q-10636 final label is corrected only in generated output.

Easy and Hard remain unclassified and unfilled. The incomplete unrated source
q-20266 is preserved and excluded. These bounded capability exceptions are
recorded in `capabilities.json`; new rated evidence should reopen classification.

The scoped replenisher rechecks inventory and historical learner presentations
under `.local/learning/requests/math/api.lock`, preserves every existing source
fact, prepares typed additive EDN with native validation specs, and retains the
exact guarded request and receipt. It holds the lock through exact-basis
readback and checks every committed datom for source attribution and scope.
Evidence and any pending requests live in `reference/replenishment/`.
