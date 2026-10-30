Completed the requested review and database repairs for all four lessons:

| Topic | Lesson |
| --- | --- |
| 17592186050463 | Representing 2x2 Systems of Equations Using a Matrix Product; reported question 17592186604616 |
| 17592186049548 | Inverses of 2x2 Matrices; reported question 17592186638274 |
| 17592186049043 | Calculating the Inverse of a 3x3 Matrix Using the Cofactor Method |
| 17592186050092 | The Determinant of an NxN Matrix |

The review covered **215 questions and examples, nine tutorials, and all 21 ordered lesson steps**. Source-backed repairs and authored completions changed **95 distinct database fields on 92 entities**. The confirmed transactions are T11628, T11632, T11633 and T11638. [Final complete-scope database readback](full-review/live-verification.json) passed at T11638.

The first reported prompt retained the source's nested HTML layout tables but lost their styles. In the original, borders on empty cells draw matrix brackets; empty cells between operands provide spacing. After style removal, the learner UI applied ordinary data-table grid styling, exposed the spacer cells, and produced excessive width. Another old import path flattened nested tables into Markdown and duplicated their rows. The second reported prompt used an inverse-answer table with a decorative middle row for its label, which became an extra Markdown row. These are stored-content/import defects. Existing matrix-input styles worked after the mathematical structure was restored.

Repairs:

- Reconstructed **26 answer layouts** from archived source: 11 matrix-product equations, five editable equation systems, and ten inverse-matrix grids. Each field appears once in its original cell; scalar-prefactor blanks remain outside the matrix. Matrix products and equation systems were checked algebraically, and every inverse grid was verified by both multiplication orders. [First lesson's source reconstruction](source-reconstruction.json), [linear-equation checks](algebra-verification.json), and [inverse-grid source/algebra evidence](expanded-scope/layout-source-evidence.json).
- Completed **12 older questions** missing both a worked solution and a canonical answer link. Their answers were independently derived, selected from the existing owned banks, and explained using the same-KP canonical-example templates. These solutions are explicitly recorded as authored completions, not recovered Math Academy explanations. [Completion derivations and template evidence](completion-evidence.json).
- Restored source emphasis in **45 existing solution/tutorial fields**, including 333 colored or shaded cells and 21 colored verification ticks. Ordered mathematical cells were checked before restoring colors and pivot boxes. This preserves the visual explanation of cofactor expansion and matrix operations. [Source emphasis verification](full-review/color-verification.json).

Question, field and answer UUIDs, entity IDs, existing answer values, banks, field positions, valid answer links and learner history were preserved. Twelve previously absent correct-answer links were added. No QA learner attempts, exposure, timing, XP or progress were created. Guarded CAS transactions used the configured Codex source, native specifications and exact datom/readback verification.

Validation:

- [Source comparison](full-review/source-grid-audit.json) matched the ordered numeric/symbolic matrix grids for all 215 prompts and nine tutorials, including matrices rendered in checkbox labels. Reconstructed interactive cells have separate archived-source and algebra checks.
- [Lesson-step verification](full-review/lesson-step-verification.json) confirmed source order and membership in all four lessons.
- [Matrix shape verification](full-review/matrix-shape-verification.json) found no malformed or empty cells among 1,648 mathematical matrix environments.
- [Actual-player rendering](full-review/render-verification.json): 1,337 fields passed strict MathJax/layout checks. [All 45 source-emphasis repairs](full-review/color-render-verification.json), including the three updated tutorials, also passed separately.
- [Actual controls](full-review/control-verification.json): all 215 prompts passed 1,935 desktop/phone and editable/correct/incorrect display cases, with no prompt or card overflow. All repaired controls mounted once; their matrix tables were borderless and unnested. Representative visuals: [system](full-review/17592186604576-760.png), [reported inverse](full-review/17592186638274-760.png).
- [Native grading](full-review/grading-verification.json): all 203 practice questions checked; 296 accepted and 680 rejected responses, with no unresolved checks. The final database readback verified 296 fields and all 853 existing answer entities.

Prevention now recognizes explicit source bracket/brace decoration in the shared Python table renderer and both browser extractors before sanitization or Markdown conversion. The shared formatter supplies matrix-product, inverse-grid and equation-system layouts. Extraction rejects lost controls instead of copying submitted values into a problem. Source-data tables retain their existing semantics. A small responsive system-brace style supports the repaired equation inputs. Capture and generation instructions describe the field-position and emphasis requirements. None of the 12 scoped knowledge points has a registered generator requiring a package replacement.

Targeted tests passed: 65 formatter/activity tests, eight existing source-table tests, and three new archived matrix-layout tests exercising both browser extractors and the Python importer. A broader 125-test capture run had three failures and one error; all four were reproduced with the original table extractor and predate this repair. They concern existing percent/display expectations, an old Markdown-table expectation, and a saved dropdown-recovery checkpoint. Their exact results and reproduction are retained in [baseline verification](full-review/preexisting-capture-test-failures.json); the broader suite is not reported as clean.

The database repairs are live. Refresh the learner page to load the updated equation-system display style.
