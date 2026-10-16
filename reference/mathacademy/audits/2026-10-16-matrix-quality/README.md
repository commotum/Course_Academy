# Matrix curriculum quality audit — October 16, 2026

The audit covers **194 matrix and related linear-algebra topics, 610 knowledge points, 7,560 questions/examples, and 452 tutorials**. The three requested topics received independent mathematical checks of every stored question and canonical example. The wider curriculum received automated structure, source-loss, native grading, rendered DOM, asset-path, and generator checks. **This is not a claim that every one of the 7,560 mathematical problems has been independently solved or that the entire library is now clean.**

Inventory reads are pinned to EDB **basis 2855**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Repairs committed at **2857** and **2859** and were read back at those exact bases. Unrelated later/importer transactions are outside this frozen inventory. All rendering checks used text and DOM geometry; **no screenshots, image viewing, or image analysis**. Image loading was blocked in the DOM fixtures.

## The three requested topics

| Topic | Entity | Math checks | Remaining content gap |
| --- | --- | --- | --- |
| Zero, Square, Diagonal and Identity Matrices | `17592186048252` | All 31 questions/examples independently solved | None found by these checks |
| Scalar Multiplication of Matrices | `17592186050979` | All 48 questions/examples independently solved | q-11532 (`17592186233218`) has no response fields; original interaction still needs recovery |
| The Transpose of a Matrix | `17592186050727` | All 51 questions/examples independently solved | None found by these checks |

The independent checks read displayed matrix entries and ordered dimensions, calculate the required result, and compare each stored correct answer and field position. They identified 17 missing correct links, two of which belonged to redundant legacy fields; **15 active correct links** were completed using existing field-owned answers. All existing correct links in these topics matched the independently computed result. Final worked-solution results/conclusions were also checked for all 130 items (124 automated, six direct checks); this does not exhaustively re-prove every intermediate algebra line. See [solution checks](named-solution-results.json). The source contained a wrong nonzero-witness coordinate in q-126201: `i_12=0.1` became `i_21=0.1`, preserving the final selection.

Restored the missing diagonal/identity examples, lost assignment labels and scalar-multiplication formula. Replaced the image-only transpose example with TeX recovered from its original HTML, without opening its images. Supplied the missing original payoff matrix in q-139431 from the captured source/context and its own worked solution. Completed 15 missing worked solutions using the matching KP method. Standardized givens and converted **22 response tables into bracketed matrix answers**, preserving every control identity and cell position.

The three topics passed **1,215 live-asset DOM checks**: 135 question/tutorial cases × 3 widths (893, 375, 320px) × editable/correct/incorrect states. No MathJax errors, control-construction exceptions, or card overflows occurred after the narrow-layout fix. Detailed evidence: [independent math checks](after-priority-math-report.json), [remaining named-topic findings](after-priority-math-issues.json), [DOM checks](priority-dom-report.json).

## Repairs saved

- **468 distinct text attributes across 419 content entities** changed through 469 text updates in two transactions.
- **92 attributes** recovered complete original compound equations from a unique exact first-fragment anchor. Each proposal retains its original source file, line, first fragment, full recovered equation, and old/new stored text. Remaining source comparisons stay review candidates, not automatically confirmed damage.
- **15 canonical answer links** and **15 worked solutions** completed. Native application grading of these completed fields accepted all 15 correct options and rejected all 60 distractors.
- **89 equivalent redundant field bindings** detached. The old fields and all 436 owned answer entities remain stored; a pre-repair history query found **zero learner task responses** referencing those old answers. No answer entities or learner attempts, timing, XP, mastery, or queue records were changed.
- **236 LaTeX syntax attributes** repaired: malformed hat accents, literal percentages that commented out closing TeX, printed blank lines incorrectly encoded as repeated subscripts, and malformed line-segment overlines. The four augmented matrices in q-78749 were retained verbatim and stacked with their operation labels outside the matrices.
- Fixed `ui/question-fields.js` so inline response placement preserves complete TeX environments and exponent/subscript arguments. Previously, inserting a field into an `aligned` equation could split it into invalid math fragments. Regression tests cover aligned equations and script arguments.
- `ui/learning.css` contains wide matrix operands and fits four-column matrix editors at small widths.

Both native transaction previews passed. Exact committed readback verified **297 records** in the first batch and **207** in the syntax batch. See [first verification](repair-verification.json), [syntax verification](render-repair-verification.json), [first receipt](repair-receipt.edn), and [syntax receipt](render-repair-receipt.edn). The scoped frontend tests and all eight shared math-format tests passed.

## Wider audit results and remaining work

The first renderer pass covered all **8,012** question/example/tutorial records, their stored solutions, and displayed choice banks at 893px using actual application Markdown, controls, MathJax, MathLive, and CSS. It found 67 records with MathJax errors and six card overflows. After the syntax and environment fixes, all previously failing records plus every syntax-repaired record were rechecked: **220 cases × 9 states/widths = 1,980 checks**, with **zero MathJax errors or construction exceptions**. Desktop card overflow was zero for this repaired set. **28 records still overflow at phone widths** and require further layout work; those are explicitly listed in [remaining review](remaining-review.json). The six initial desktop overflow records are incomplete legacy imports; fixing their mathematics/structure needs source recovery, not just smaller styling.

Native grading exercised **6,590 stored questions, 9,687 accepted submissions, and 26,270 rejected submissions** (35,967 checks total). Ten expected-result checks returned unresolved: the canonical and wrong-control submissions for **five blank fields in four questions**. This validates grading behavior against stored keys, **not the mathematical truth of every key**. Unresolved entities: `17592186295091`, `17592186295092` (matrix-entry subscripts), `17592186479854`, `17592186495074` (captured function notation). See [native results](grader-report.json).

Remaining structural findings after the saved repairs:

| Finding | Occurrences | Distinct entities |
| --- | ---: | ---: |
| no-practice-solution | 342 | 342 |
| no-correct | 485 | 374 |
| duplicate-field-keys | 32 | 32 |
| tex-structure | 137 | 129 |
| no-fields | 3 | 3 |
| unplaced-field | 2 | 1 |

These are stored-pool quality findings; missing keys, duplicate keys and fieldless practice records fail the application's ordinary-question validation. A structurally complete record is not thereby certified mathematically correct. TeX-structure findings include legacy forms and unsupported notation and need record-level review; the DOM results identify actual renderer failures separately. See [full findings](after-structure-findings.json).

Two specific legacy ODE inconsistencies merit source recovery:

- `17592186167220` / q-332755: the system has repeated eigenvalue −2 but its displayed fragment uses `e^{2t}`.
- `17592186167223` / q-332878: for x′=−4y, y′=9x, the displayed general solution mixes frequencies 6 and 2. Both coordinates should use frequency 6. Neither record has a complete correct-answer field set. Their mathematical repairs were not guessed or silently applied.

The source pass compared **2,027 compound-formula occurrences** from the original saved HTML. Exact-anchor repairs were narrow; **1,644 occurrences initially required further review**, and seven source formulas could not be converted by this checker. Formatting differences, annotations, images, and later revisions can explain a mismatch. The old MA export extractor still selects the first nested MathML fragment before the surrounding compound SVG title; that original exporter is outside this repair. [Source comparison](source-comparison.json) records all statuses and evidence.

All **3,316 distinct referenced image paths** (4,003 references) resolved through the application's asset allowlist. This was file/path checking only; image-based mathematical correctness was not inspected.

All **77 registered generator scripts/packages** were checked at recorded SHA-256 values. **271 deterministic fresh samples** passed the basic identity/field/bank contracts; their DOM render pass produced zero MathJax errors. One finite-domain generator correctly returned no new tasks; one over-workload draw was rejected by its bounds. Nineteen scripts produced formatting-convention warnings, despite renderable sampled output. Two sampled outputs from KP `17592186119772` overflowed at desktop width. These sample checks do not constitute an independent mathematical proof of every generator or exhaustive parameter coverage. See [generator results](generator-report.json) and [sample render results](render-recheck-report.json).

## Reproduction and evidence

[Scope](scope.json) records topic inclusion reasons: matrix/determinant/eigenvalue/linear-map/row-reduction/related titles or membership in a Matrices/Linear Algebra unit. [Snapshot](snapshot.json), `content-batches`, and the saved query/input files retain the frozen reads. [Structural checker](structural.py), [source comparison](source_compare.py), [independent named-topic solver](priority_math.py), [native grader harness](grader.rs), and [DOM harness](check-dom.cjs) document the checks. Native executables are kept under `.local/matrix-quality`, not among the report artifacts.

This report separates verified repairs from the remaining review queue. **The named-topic pass is detailed; the broader pass is a curriculum-wide automated audit with explicit mathematical and image-review limits.**
