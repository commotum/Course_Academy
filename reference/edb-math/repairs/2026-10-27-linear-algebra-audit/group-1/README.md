# Group 1: linear algebra formatting and source audit

Read-only audit at **T9047**. Final integration files are `proposals.json` (**326 content CAS values**), `missing-key-proposals.json` (**15 existing-answer links**), and `cas.edn` (**341 CAS forms**). No EDB writes, generator publication, or shared production edits were performed. Root owns final preview, membership repair and commit.

| MA topic | Lesson | Questions (source/generated) | Tutorials | Direct sources | Content proposals | Missing keys |
|---|---|---:|---:|---:|---:|---:|
| 1908 | Linear Independence in Abstract Vector Spaces | 48 (48/0) | 2 | 40 | 46 | 1 |
| 1772 | Row and Column Operations on Determinants | 82 (82/0) | 5 | 57 | 6 | 1 |
| 1851 | Linear Combinations of Vectors in N-Dimensional Euclidean Space | 123 (61/62) | 1 | 48 | 87 | 2 |
| 1909 | Bases in Abstract Vector Spaces | 46 (46/0) | 3 | 28 | 5 | 1 |
| 1373 | Solving 2x2 Singular Systems of Equations Using Gaussian Elimination | 61 (35/26) | 3 | 28 | 2 | 1 |
| 1731 | Elementary 3x3 Matrices | 38 (38/0) | 2 | 26 | 27 | 1 |
| 2089 | Row Operations on 3x3 Matrices as Products of Elementary Matrices | 47 (47/0) | 1 | 27 | 2 | 1 |
| 1171 | Multiplying a Matrix by the Identity Matrix | 57 (27/30) | 3 | 23 | 0 | 0 |
| 1048 | Solving 3x3 Systems of Equations Using Gaussian Elimination | 27 (27/0) | 2 | 24 | 2 | 0 |
| 1855 | Finding a Basis of a Span | 83 (47/36) | 3 | 27 | 110 | 4 |
| 2201 | Conditions When a Determinant Equals Zero | 39 (39/0) | 5 | 24 | 15 | 0 |
| 1867 | The Rank of a Matrix | 50 (38/12) | 2 | 22 | 4 | 3 |
| 1861 | Linear Dependence and Independence | 76 (47/29) | 4 | 39 | 20 | 0 |

The final content proposals restore658source formula annotations in227fields; visible set braces, vector notation, coefficient/row/column colors, augmented partitions and shaded pivot markers are retained. Sixty additional radio-answer values recover source-visible set braces with the parent’s explicit review, preserving answer/field IDs and links. Fourteen worked solutions are authored completions. Eight solution fields receive nine independently demonstrated intermediate-cell corrections; three prompts recover matrix-dimension crosses. Twenty-six initial aligned brackets receive exact `{}` guards (17additional fields beyond the309prior proposals).

`source-formula-proposals.json`, `completion-proposals.json`, `independent-proposals.json`, `answer-format-proposals.json` and `initial-bracket-proposals.json` are component evidence, not additive transactions; overlapping changes are merged only in final `proposals.json`. Source caches were regenerated after the shared renderer font fix; final values contain no duplicated mathcal wrapper.

Validation:5,900current content values including381checkbox display keys, all326final changed values, and1,544fresh-generator content values pass the actual Markdown/MathJax renderer (309initial final values plus26final guard values were rendered, with9overlap). All18blank questions mount original MathLive controls and fit390px. The proposed records pass4,034native grading checks;180fresh generator records pass1,108checks. All830numeric matrix stages across225existing solutions and306stages across68fresh solutions pass row-equivalence checks. Source comparison verifies656given matrices across265questions; all413available source prompts have matching given-matrix collections, including148without matrices. Representative source/current/proposed screenshots under `screens/` were visually compared. Three retained pedagogical images were inspected directly and remain unchanged.

The q-42156duplicate selection field is documented in `duplicate-history.json`. Independently solving x−2y=1 identifies original answer17592186104028. All incoming references atT9047 were checked for the question, both fields and tenchoices; none are learner task/response references. Keep the missing-key repair for the original field; root will separately detach its redundant question membership while retaining every entity and choice.

All16active generator files were inspected read-only; `generator-inspection.json` includes paths, hashes, functions and imports. Forty-five supported package/difficulty combinations yielded180samples. Unsupported bands were correctly rejected. No replacement candidate is staged; the exact recurrence reasoning is in `generator-recurrence-review.json`.

Limits are explicit in `summary.json`:169original questions lack direct retained-source prompts;141fields have changed math-fragment segmentation due checkbox migration or solution rewrites; native grading does not independently prove all existing keys; generator samples are not exhaustive domain testing. No source fidelity is claimed where direct evidence is absent.
