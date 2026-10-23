# Multistep context repair — 2026-10-22

The Integrating Trigonometric Functions lesson had selected historical question
`17592186233488` (`q-143522`) without the shared definition of `v(t)`.

At basis **5670**, the unanswered, paused presentation `17592186674268` in task
`17592186409333` was retargeted to unused question `17592186250145`, from the same
knowledge point. The task remained paused, with eight answered questions and
232.545 recorded seconds. No response, grade, XP, progress, or completed item was
changed. The prior content reference remains in EDB transaction history.

At basis **5671**, five historical activities were reconstructed using generic
activity steps, assigned-problem wrappers, multistep contexts, and ordered inner
steps that reference the original question entities. The original particle-motion
variant is now activity `17592186674431`, with seven parts. The app preview confirms
that its fourth part includes `v(t)=4\csc^2 t`.

The reconstructed setups in `reviewed-contexts.json` are locally authored from
explicit definitions and units in the retained prompts and worked solutions.
They are not represented as verbatim captures of MA's original shared context.
Existing same-title variants, question content, answer fields, canonical answers,
and KP membership were preserved. These repairs do not assign new work to Jake.

Of the 81 historical multistep parts audited, 47 now have structural containment
(38 repaired, nine already correct). The other 34, from four activities, lack the
required original shared graphs or setup. They are withdrawn from fresh practice
using `question/retired`; their records and history remain intact. See
`withdrawn-source-incomplete.json`. Their full activities have **not** been
reconstructed. Restoring them requires verified source setup, not another
same-title variant or a graph inferred from answer values.

A separate audit found 787 distinct question IDs in other saved multistep
captures. Of the 781 present in the database, none was an uncontained, unretired
part. The six absent questions cannot enter the current practice pools.

The historical extractor now retains task type and task ID in provenance.
Question-only preparation defers multistep parts. Both content transaction
builders reject flattened historical multistep inputs, including older exports
whose task type must be recovered from their saved source. Complete multistep
imports continue through the existing structural importer; no question-parent
attribute or new runtime schema was added.

## Verification

- Exact-basis readback: original question content, answers and KP links unchanged;
  no learner/progress mutations in the structural repair; rerun produces no writes.
- App readback: replacement question and preserved lesson progress; restored
  particle-motion preview has seven ordered questions and the shared context.
- Python: five provenance/flattening tests, three repair-plan tests, 13 content
  tests, 18 activity tests, and 11 import transaction tests passed.
- Rust: six multistep tests and one retired-question history test passed.
- Python compilation and diff whitespace checks passed.

`replacement-receipt.edn` and `receipt.edn` are confirmed commit receipts.
`verification.json`, `app-verification.json`, and `other-captures-verification.json`
record the corresponding readbacks. `scripts/repair_historical_multisteps.py`
defaults to a preview; `--apply` reuses the saved guarded intent and receipt.
