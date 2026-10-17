# Checkbox statement label review

Reviewed question: `17592186562914`. This is a presentation defect: each checkbox should carry its complete statement, without an additional Roman-numbered copy in the prompt. This review performs no database or UI mutations.

The existing UI already supports the desired presentation:

- `ui/question-fields.js:22–37` renders `field.key` through its supplied renderer. The input and hidden Boolean response use field and answer entity IDs, independent of the label text.
- `ui/learning.js:703` and `ui/assignments.js:137` render checkbox labels as text answers, passing them to the normal Markdown and math renderer. `ui/activity.js:94` uses the same Markdown path for saved history.
- `ui/learning.js:272–346` protects inline TeX during Markdown parsing and typesets it with MathJax. A key such as `The product $SP$ is well defined.` therefore needs no renderer change.
- `engine/edb/answer_fields.rs:35` requires a nonempty string key. `engine/rust/learning.rs:169–171` requires keys to be unique within the question. Full statements satisfy these constraints when the selectable statements are distinct.
- `engine/rust/learning.rs:1594–1690` validates submitted field and answer IDs and compares the selected answer entity to the canonical answer entity. Renaming existing field keys preserves grading when field/answer identities, banks, and correct references stay fixed.

The scoped repair is to CAS-update each existing Roman field key to its matching complete statement, remove only the duplicate Roman list from the prompt, and retain the mathematical setup and one selection instruction. Any solution references to “statement I”, “II”, or “III” must identify the actual products instead, because the visible Roman labels will no longer exist. Preserve the actual mathematical explanation, truth values, difficulty, question membership, field and answer identities, and saved responses.

Historical evidence shows this particular question was created as a checkbox by `generate/scratch/17592186100869-draft.py` during its basis-2750 replenishment. The generator inherited the same representation as the earlier migration helpers; it was not itself necessarily a radio-to-checkbox database conversion. The historical `finder-easy/prepare.py:98–131` and `discovery-direct/prepare.py:74–84` deliberately retained the listed cases and assigned Roman field keys. Their evidence and receipts should remain unchanged. Future conversion guidance should distinguish internal case identifiers from learner-facing, self-contained checkbox labels.

The generator's existing `render-preview.py` uses the real application rendering and response-collection functions. Its validator and replenishment code assume Roman keys and prompt-located product statements; those assumptions need corresponding changes when the generator is repaired. A useful validation is to parse each product from its new field label, independently recompute conformability from the printed matrices, and check all eight Boolean selections. Verify saved-response IDs and state remain identical after the database text repair, and visually confirm that the prompt no longer repeats the choices and that all three labels typeset correctly.
