# Broadened structural mathematics audit — 2026-10-26

Committed repairs to **5,020 distinct content fields on 3,862 entities, spanning 490 lesson topics**. This includes 2,929 questions/canonical examples affected directly or through their choices. Counts are net differences from the task's starting state, not the sum of transaction updates. See [completion.json](completion.json).

| Content attribute | Net repaired fields |
|---|---:|
| `question/worked-solution` | 2,515 |
| `question/problem` | 1,538 |
| `tutorial/content` | 338 |
| `answer/value` | 629 |

The audit expanded beyond the earlier fenced-matrix spacing signature. It checked structure, recovered whole formulas, compared source grids and renders, and replayed the legacy converters where possible. The final full-database scan at **T8666** covered 2,940,190 facts and 1,468,728 strings. All **5,021 touched field values** matched the expected final values; the extra field was a reconstruction regression that was reverted to its original good value. The repaired mechanical signatures have zero remaining matches. See [postscan-final.json](postscan-final.json) and [final-structure-verification.json](final-structure-verification.json).

The related failures came from several lossy import paths:

- Generic MathML tables became `aligned` without retaining their data-column alignment or rules. This affected sign charts, Pascal diagrams, ratio layouts and root lists, in addition to matrices. Source matching also missed equivalent ASCII and Unicode derivative-prime spellings; the comparison now recognizes those aliases without rewriting stored expressions merely for spelling.
- The legacy JSON converter serialized table columns with pipes and rows with semicolons. The Markdown converter then guessed matrix boundaries from those strings, sometimes across TeX groups. Absolute values, cardinalities, fractions, congruences and parallel derivations could become false matrices or determinants. Other tables remained visibly flattened as `x|=...; ...`.
- Piecewise braces became unmatched grouping braces, equation systems lost their row structure, and zero-rule fraction stacks became division fractions rather than binomial-style notation.
- Limit operators became ordinary `{lim}` atoms, parenthesized legacy subscripts or malformed `\limits` constructions. An overbroad command-argument guard also skipped limits after `\displaystyle`. Standalone limit expressions now use display math; references within prose remain inline.
- Sized bars were confused with relation bars. The evaluation-bar parser could reinterpret `|x|^3`, or produce invalid `\Big\right|` combinations. Punctuation stripping also removed the invisible delimiter dot in `\right.`.
- Duplicate display delimiters broke equation segmentation. One reviewed question also had unescaped visible set braces split across its response slots.

Initial source work examined 2,964 archive metadata files, read 216 relevant HTML pages and retained question captures, and indexed 4,104 source table records; see [source-summary.json](source-summary.json). The later literal-table pass reviewed **404 fields containing 706 candidate formula blocks**: **673 blocks were repaired**, while **33 legitimate conditional, set, absolute-value or punctuation cases were retained**. Its source files are hashed in [batch-05/source-provenance.json](batch-05/source-provenance.json) and [batch-06/source-provenance.json](batch-06/source-provenance.json). Repairs use identity-bound source formulas, equivalent token streams, legacy serialization replay, or explicitly documented individual review. They do not replace every pipe with a matrix separator.

Ten formula blocks required layout-only reconstruction: their archived currency MathML was itself corrupt. The archived grid established the rows, while the database's previously repaired currency signs and mathematical expressions were retained. Other reviewed source labels recovered their explicit nested-math annotations without displaying transport wrappers. The before/after values and repair bases are retained in each batch's `fields.json` and source-edit records. The evaluation-bar batch contains three exact archived formula recoveries and one structural correction that removes an invalid sizing command without changing operands or bounds.

| Transaction | Field updates | Evidence |
|---|---:|---|
| T8633 | 3,032 | [Verification](verification.json), [render checks](render-verification.json) |
| T8635 | 1,585 | [Verification](batch-02/verification.json), [render checks](batch-02/render-verification.json) |
| T8637 | 1 | [Verification](batch-03/verification.json), [render checks](batch-03/render-verification.json) |
| T8647 | 4 | [Verification](batch-04/verification.json), [render checks](batch-04/render-verification.json) |
| T8666 | 450 | [Verification](batch-05/verification.json), [render checks](batch-05/render-verification.json) |
| T8669 | 27 | [Verification](batch-06/verification.json), [render checks](batch-06/render-verification.json) |

The supplemental literal-table pass initially reused an earlier candidate-only value cache. Reconciliation against the full database snapshot exposed another 47 formula blocks on 30 fields: 44 were repaired in T8669 and three legitimate set expressions were retained. The final literal-table scanner reads the full fact export and explicitly reconciles all retained cases; the filtered cache is not its audit universe.

T8637 corrected a regression in this audit's source reconstruction: one existing determinant choice, answer `17592186263008`, had been changed back into a fenced `aligned` layout in T8633. Its final bytes equal its starting bytes, so it is excluded from the net repair count. Complete-formula normalization and the shared structural validator now check this case.

Every transaction used exact old-value CAS, an explicit `:agent/codex` source, a stable request key, native preview, receipt reconciliation and readback at its committed basis. Across six transactions there were 5,099 field updates and 10,204 datoms, including transaction timestamps. Only the four content attributes above changed. Entity IDs, answer types, correct-answer links, choice identities, response slots, images and learner history were preserved. Intentional source illustrations remain images.

All batches passed actual Markdown/DOMPurify/MathJax rendering checks with zero final rendering or page errors and unchanged image references. [Representative before/after renders](structural-before-after.png) show the layout differences; this fixture checks content rendering, not full interactive answer-control behavior. Native grading fixtures ran 1,358 before/after checks: 186 accepted, 744 rejected and 428 explicitly unresolved outcomes remained unchanged. The unresolved outcomes come from **51 pre-existing selection fields without correct-answer keys**; this formatting repair did not invent keys. Native previews also checked that answer-field validity was preserved.

Prevention changes cover the historical importer, both browser MathML extractors, shared formatting/validation and generator publication. They preserve table roles, zero-rule stacks, cases and limits, distinguish bar roles, and reject malformed groups, grids, fences and matrix layouts. Generator and capture documentation now state these requirements. The external legacy Markdown converter has corresponding matrix, limit, evaluation-bar and invisible-delimiter fixes. The legacy JSON fallback now **rejects unsupported MathML table conversion** and requires structural reconstruction instead of silently emitting pipe-and-semicolon placeholders. Hash records for those external changes are retained alongside this report; replay bases are preserved as `external-legacy-md.py` and `external-json-replay-base.py`.

Validation passed: 32 shared-formatting tests, 17 browser/historical-import tests, 41 publication tests, 27 external Markdown tests and 13 external JSON tests. Publication and importer test logs are retained here. The final literal-table scan records the retained legitimate cases separately in [pipe-postscan-final.json](pipe-postscan-final.json).

This is a database-wide audit of these structural defect families, not a proof that every mathematical statement or source-dependent layout is correct. The initial 1,178 unmatched table occurrences were candidate matches, not a confirmed defect count; many were subsequently resolved by whole-formula recovery, and others are ordinary derivations or lack sufficient matching evidence. Their evidence remains in the source-review files. A default-versus-explicit centered-column ambiguity was reviewed as source-equivalent and left unchanged. General source disagreements and the missing answer keys remain separate from this formatting repair.
