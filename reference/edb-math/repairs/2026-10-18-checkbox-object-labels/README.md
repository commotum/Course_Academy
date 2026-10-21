# Checkbox option placement repair

The checkbox audit covered all 3,159 questions and 9,831 attached checkbox fields. Repairs to 3,122 questions are committed and verified through basis **3773** in 21 transactions; 37 questions already contained complete choices. No affected questions remain pending. This includes the user's example, `17592186272202`.

The October 12 radio conversions kept independently selectable statements or matrices in the prompt and assigned only source labels to the new checkbox fields. Later generated/authored copies repeated this presentation. The problem is independent of the MathML import failures repaired earlier.

The repair moves complete objects into existing `:answer-field/key` values, removes the old selectable lists from prompts, and replaces obsolete Roman-choice references in solutions. Shared mathematical setup is preserved. All fields, Boolean answers, correct references, difficulty, curriculum/canonical memberships, and saved responses retain their identities and values.

## Scope and evidence

- 2,994 statement, equation, and matrix questions: `mapping/cases.json`, with exact extraction spans and historical provenance.
- 48 other cases: complete pivot-column vectors beside their checkboxes, plus one placeholder-based True/False question.
- 80 exceptional cases: 13 text/occurrence cases, 11 verified shared graphs, and 56 independent diagram-option cases.
- 37 questions already contained complete selectable content and required no repair.

The 191 independent diagram assets are standalone SVG viewports embedding unchanged original raster bytes. Each rendered viewport was compared pixel-for-pixel with its source rectangle. Publication hashes, source rectangles, and the asset receipt are in `exceptions/`. Shared-graph exceptions retain the common coordinate graph because removing that context would change what the point choices mean.

`status.json`, `case-ledger.json`, `remaining-question-ids.json`, and `confirmed-batches.json` are the live checkpoint. Only confirmed receipts and successful committed readbacks count as completed repairs. `batches/` preserves every guarded attempt, original transaction, intent, receipt, preview, datom verification, and full readback.

The final read-only census is in `final-census-after-piecewise/`; reconciliation is recorded in [final-verification.json](final-verification.json). The initial native index census also identified one unattached checkbox field, `17592186408178`; it is not part of a question and was left unchanged.

## Validation

Each batch refreshes its full questions, choices, saved uses, and incoming references at one immutable basis. It CAS-updates only reviewed prompt, solution, and field-key strings. Native installed validators, exhaustive Boolean grading, canonical/flip/incomplete responses, actual application checkbox controls, and desktop/mobile rendering are checked. Committed full Pulls and incoming references are compared against the preview, and every data datom must match the exact intended change with contributor `:agent/codex`.

Incidental pre-existing TeX errors exposed by rendering and necessary narrow-screen math wrapping are recorded separately in mapping/formatting evidence. These do not change the mathematics or answer keys.

Every question has actual application rendering evidence at desktop and 375px mobile widths. The final [visible-choice audit](validation/final-visible-choice-audit.json) covers 6,318 question views and 19,662 choice views with no leaked TeX syntax or critical rendering failures. It caught six piecewise-function cases that did not raise MathJax errors; their 18 field delimiters and matching solution references were corrected and committed in the final supplemental transaction. The independent [final invariant audit](validation/final-invariant-audit.json) confirms that all 49 saved learner items, field/answer identities, Boolean banks, correct references, and other nonpresentation attributes were preserved.

The presentation linter was narrowly corrected so it does not mistake the bullet `- $0$` for the term `-0.5`, or confuse a proposition about a shared matrix with selecting the matrix itself. Its eight regression tests pass.

## Reproduction and recovery

`audit.py --output DIRECTORY [--basis N]` performs a complete read-only native-index census. `run_batch.py CASES.json NAME --commit` captures, validates, previews, submits, and verifies one reviewed group. An existing persisted intent is recovered under its original exact request key; only a confirmed stale-basis rejection permits a refreshed request. `checkpoint.py` rebuilds the ledger from confirmed evidence.

The database repairs do not update generator scripts. Read-only probes confirmed **46 registered generators still produce the old label-only checkbox format**. Their scripts, source hashes, sample arguments, and generated records are recorded in the [generator audit](validation/generators/README.md). They remain unchanged, so newly generated questions can repeat the defect. Updating the conversion skill alone does not repair those generators.
