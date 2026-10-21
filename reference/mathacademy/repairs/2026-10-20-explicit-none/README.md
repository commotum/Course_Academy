# Restore explicit None answers

The user corrected the October 19 interpretation of Math Academy “None” answers: an explicit source choice belongs in the visible checkbox list. An empty selection is not its replacement. This overrides the radio2checkbox skill's older empty-subset convention.

The read-only census captured database `math`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, at basis 5088: 3,231 checkbox questions, including 2,939 with Math Academy source identities. Migration choice mappings and retained original database answer banks establish 555 questions with explicit source choices mapped to the empty subset. A historical database read establishes five more original None choices not present in those mappings. The initial migration also separately detached the existing None field from q-96676 (17592186234490); that field is restored with its original identity and banks.

The resulting scope is 561 questions: 104 have None as the correct response, and 457 retain it as a distractor. Twenty-one answers use an equivalent source phrase such as “The function has no vertical asymptotes”; that complete statement is retained. Other source None wording is displayed as “None of the above.”

`resolutions.json`, `source-candidates.json`, `source-proof.json`, `originals.json`, and the retained native reads record the evidence. Duplicate historical answer banks are treated as one source choice, not duplicated visible checkboxes. The separately restored existing field is recorded by `repair.py::ledger` and its original removal receipt/plan.

Each batch captures a native database value, reads at that basis, checks original source banks and prospective UUID absence, and previews the complete transaction with application validators. New fields have owned text true/false answers. Existing ordinary fields, keys, solutions, difficulty and memberships remain unchanged. Prompts lose the obsolete instruction to leave all boxes unchecked. Original question and answer identities are retained.

A saved response gains a true None answer only when all its existing choices were false; otherwise it gains false. Unattempted items stay unattempted. Every other item attribute is preserved. Native grading exhaustively checks every ordinary subset and its explicit None mapping, every single-box flip, an entirely unchecked answer, and contradictory None-plus-ordinary selections. All repaired questions pass fresh-practice validation. Presentation lint and desktop/phone renders check the labels. Each confirmed receipt is checked against the exact allowed datoms and contributor, followed by committed readback and reproduction of the historical snapshot.

Batches are committed independently with stable saved requests, `:agent/codex`, and database-basis guards. Confirmed stale-basis preparations are preserved under `rejected/`; they are refreshed only after a definitive rejection. Unknown outcomes must be reconciled with the identical saved request. Do not rerun successful requests as new repairs.

The generator policy still rejects a checkbox question with no correct selectable option. A visible, correctly keyed source None option satisfies that rule. This repair restores database content; it does not reenable previously excluded generator sampling branches. `generate/docs/6-template-generator.md` now explicitly requires visible source None choices, source replay fidelity and equivalent learner-response migration, without inventing None choices to rescue invalid generated content.

Final commit counts, bases and verification are recorded in `verification.json` after all three batches finish. The earlier October 19 evidence remains unchanged.
