# Restore substitution recognition in ordinary practice

Published and verified at EDB basis T7075. All 12 generators under topics
17592186050489, 17592186048189 and 17592186048245 now assess complete
integration. The learner must recognize the substitution without being given u.

The defect was a change in the assessed objective: the previous easy bands
supplied the substitution and asked only for the transformed integral. That
format came from a different KP's guided algebraic-substitution tasks. It did
not preserve these KPs' imported complete-calculation objective. For example,
q-13469 (17592186658964) asks for the complete integral of
2x² csc²(x³), while q-350908 (17592186580897) asks for a complete definite
quotient integral. These are family analogues, not claimed direct parents.

Easy questions now use small source-supported forms and full-answer choices.
Moderate uses exact entry where the engine supports it. Inverse-trig
antiderivatives retain multiple choice because inverse-function exact entry is
unsupported. For inverse secant specifically, easy has an exact differential
match with an integer factor no greater than three; moderate requires a small
fractional adjustment; hard adds absolute-value normalization. These are authored
bands, with imported labels preserved rather than presented as external calibration.

Retired and replaced 98 generated questions: 96 supplied-u transformations and
two inverse-secant moderate questions that did not fit the revised progression.
The final pool has 8 easy, 8 moderate and 8 hard per KP: 288 active generated
questions. Preserved 190 existing full calculations, 183 imported questions,
12 canonical examples, old question/answer content and saved learner references.

| Reported retired question | Replacement |
| --- | --- |
| 17592186678309 | 17592186690914 |
| 17592186678394 | 17592186690960 |

The author/reviewer prompts and generator documentation now require scaffolding
to preserve the target decision. Publication guards reject supplied-u prompts,
transformation-only choices and blanket primitive/endpoint hints for these KPs,
including prompts whose metadata falsely claims no guidance. Explicitly guided
stages in other KPs remain legitimate when their own objective supports them.

Answer banks vary factor and structural errors, use consistent notation across
correct and incorrect options, and reject equivalent antiderivatives. In
particular, ln(2u) cannot be treated as a wrong answer to ln(u)+C.

Validation: 70 Python tests; independent reading of all 288 printed derivations;
1,440 pairwise checks of distinct answer options; 1,246 native grading checks
(526 accepted, 720 rejected, zero unresolved); 48 rendered previews with selected
screenshots visually inspected; and 102 read-only live grading checks. All passed.
Immutable packages were reproduced after relocation; installed mirrors and all
12 live registrations were checked against the published packages. No learner
attempts were created by validation.

The current source snapshots include a separate HTML-table fidelity repair.
`source-review.json` confirms those differences preserve the ordered mathematical
expressions. Those source changes were retained.

Evidence: `completion.json`, `replacement-map.json`, `generator-verification.json`,
`grader-verification.json`, `tests.json`, `render/rendering.json`,
`render/visual-review.json`, `source-review.json`, and each KP's
`publication/` preparation, immutable-package manifest, request, receipt and
readback verification. Earlier guided-stage reports are historical and are
superseded by this complete-calculation contract.
