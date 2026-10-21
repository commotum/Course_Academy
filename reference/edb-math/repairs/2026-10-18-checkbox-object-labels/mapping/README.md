# Complete-object mapping evidence

This directory contains read-only mapping work for the full checkbox audit captured at basis 3704. Database submissions and receipts belong to the parent repair directory.

The historical October 12 conversion code deliberately retained the selectable lists in question prompts and assigned only source labels to new field keys. In `finder-easy/prepare.py`, `labels_and_prompt()` inserted or retained Roman labels in the stem, then `plan()` asserted `:answer-field/key` equal to `label`. `discovery-next/prepare.py` did the same even though its reviewed `atomic_options` already recorded full objects. Consequently the Boolean banks and learner-subset migrations could be correct while the displayed checkboxes still required matching labels against a separate list. This was a response-presentation defect, not a MathML import defect.

`historical-plans.json` records 2,853 converted question plans from finder-easy, finder-remaining, discovery-direct, discovery-next, and discovery-keyed-incomplete. Superseded preparations, retained radios, and separate content-only repairs are excluded. These historical rows establish provenance and positional mappings; current prompt and solution bytes always take priority.

The current mapping covers 2,994 questions and 9,239 existing checkbox fields:

- 2,620 explicit labelled lists;
- 221 unlabelled lists whose source order is established by historical plans or the current worked solution;
- 77 named-matrix assignment blocks;
- 76 sets of separate matrix blocks or stacked HTML matrix children.

The separate exceptions review owns 80 questions with shared diagrams, variable-occurrence annotations, standard number-set universes, or an inline congruence-system list. The parent review owns 85 questions with already descriptive or differently structured field keys.

`cases.json` records exact original option spans, the complete objects, existing field IDs and labels, current prompt/solution before and after, historical-plan paths, and every solution-reference substitution. No field, answer, correctness, or learner-response identity is rebuilt. Named matrices keep their names, while obsolete Roman-choice references in explanations become references to the actual objects.

Short objects receive natural captions where helpful: number-set symbols are spelled out, numbers and points are identified, and every choice in a variable-identification question receives the neutral caption “The expression …”. This preserves the mathematical content and avoids using the word “variable” to reveal the answer. Identical values in shared givens remain in place.

`verify_mapping.py` independently checks all moved source content and original field-label identities, and proves that all content outside removed option spans survives except whitespace normalization and empty layout wrappers. It also checks the complete partition of the captured questions. `review.py` runs the skill's presentation lint; all 2,994 cases pass after narrowly correcting the linter's shared-matrix and numeric-substring false positives.

Solution-reference review protects original mathematical spans and domain names such as type I/II and quadrant I/II/III. Five ranges `I–III` expand to all three objects. The nonstandard reference contexts in `solution-edge-contexts.json` were inspected; they refer to pairs, predicates, intervals, vector fields, and explicit selections. No source solution references an absent choice label. In question 17592186172648, quadrant numerals are mathematical terminology, so its entire solution remains byte-for-byte unchanged.

Necessary formatting repairs are explicitly recorded in the cases: 13 extraneous trailing `$$` openers on options across ten questions, two matching stray openers in solutions, and literal set-brace escaping in the solution of 17592186055072. The last issue caused a pre-existing MathJax “Misplaced &” error because an unescaped TeX group crossed aligned columns. These edits preserve all mathematical tokens and claims.

The user’s exemplar 17592186272202 was inspected in the actual rendered mobile output: shared setup remains above the options and all three complete statements appear beside their checkboxes. The worked solution now refers to the corresponding statements directly.

The remaining 2,794 mapped questions received 5,588 actual application renders at desktop and 375px mobile widths. The parent isolated 179 questions requiring math or mobile layout repair. `final-cases.json` contains their frozen final proposals; `final-format-proofs.json` records each narrowly scoped format change. Three hundred checkbox objects were reflowed at existing mathematical boundaries, and two additional choices received visible set delimiters to match the third choice in the same question. Identical full-object references in solutions reuse the same layout, while separate display equations are preserved.

Set-builder rows retain all members and conditions inside visible braces. The renderer treats a bracket immediately following `\begin{gathered}` as an optional argument, so bracket-leading vector rows receive a thin-space token and the two long polynomial associativity statements break at their inequality. Actual screenshots confirmed that no vector or polynomial operand is swallowed. Fifteen pre-existing math-error cases and two literal-source theorem spans also received minimal delimiter repairs, documented by the exceptions review.

`final-render-approved/` contains 358 verified final views with exact payload provenance: 174 unchanged questions reuse the successful v2 replay, and five use the final v4 replay. There are no critical math, image, or checkbox-control failures. The three 4px internal-table width metrics on question 17592186406882 are accepted visual exceptions: every matrix and delimiter is visible, with all SVG right edges inside the checkbox label. Both mapping and independent validation inspected this case; `metric-only-reviewed.json` records the measurements. No database writes were made by this mapping subtask.
