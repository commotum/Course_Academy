# Hat-accent audit and repair — committed

The authorized transaction committed to `math` at **basis 3693**, from basis 3692, with source `:agent/codex`. It repairs **1,416 malformed hats in 388 fields on 326 entities**, spanning [30 topics](lessons.json). The full committed readback matches the preview. The final exhaustive audit scanned **633,415 current text values across all 29 string attributes** and found **zero remaining malformed hat patterns**.

## Scope and transaction

| Attribute | Repaired fields |
|---|---:|
| `:question/worked-solution` | 163 |
| `:question/problem` | 100 |
| `:answer/value` | 110 |
| `:tutorial/content` | 15 |

The repair covers 1,174 structured `\overset{^}{...}` occurrences and 242 flattened `...^(^)` occurrences. Source MathML determines the full base and whether to use `\hat` or `\widehat`: **92 narrow hats and 1,324 wide hats**. Existing valid hats and other oversets are preserved.

Rendering also exposed literal percent signs commenting out the closing delimiter of aligned equations. The same transaction includes **45 source-verified percent escapes in 15 of the affected fields**, allowing those formulas to render without changing their mathematics.

The transaction contains 388 compare-and-swap forms and 341 validation assertions. Answer identities, choice banks, canonical links, question difficulty, and curriculum placement are preserved. Of the 110 math answer values, 95 belong to 19 radio fields and 15 are unowned legacy records. None are referenced by historical learner responses. Four of the radio fields already lacked a correct-answer link; that pre-existing incompleteness is preserved, and their choice banks remain distinct. The other 15 fields pass native answer-field validation.

- [Exact transaction](transaction.edn), [readable diff](changes.diff), [plan](plan.json)
- [Saved request](request.json), [commit receipt](receipt.edn), [committed verification](commit-verification.json)
- SHA256: `9b854197ac2acc7b5ee5674df7e92307f6112737b402a262a80a527bc71e8962`
- Database lineage: `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`

## Audit and source recovery

The initial audit at basis 3672 scanned every string attribute, including prompts, solutions, tutorials, answers, feedback, multistep contexts, titles, metadata, and generator scripts. The broad candidate filter also collected valid hats and non-hat oversets; balanced parsing then distinguished the actual malformed patterns. No additional whitespace/wrapper, stackrel, Unicode circumflex, combining-hat, fullwidth-caret, or mover variants were present in those candidates. [Audit summary](audit-summary.json).

Two import paths caused the defects: the generic MathML `mover` conversion emitted a bare caret inside `\overset`, while an older archive converter flattened movers to `base^(mark)`. Both lost the semantic accent operation. Source operator `stretchy="false"` requires a narrow hat; default stretchiness requires a wide hat. [Source investigation and importer history](source/README.md).

All 282 structured fields preserve their original base expressions and surrounding text exactly: [independent verification](structured/verification.json). All 106 flattened fields were recovered from their original archive source, including the full three-letter base of angle names such as `COD`. All 15 orphan answers were traced through their original answer UUIDs: [source proofs](flattened/changes.json), [independent verification](flattened/independent-verification.json). The necessary percent escapes have separate [source proofs](companion/changes.json) and [independent verification](companion/independent-verification.json).

## Import prevention and validation

Both maintained JavaScript converters and the historical Python importer now preserve hat width, complete bases, and supported source font variants. Unsupported styling is explicitly flagged instead of silently discarded. No UI dependency changes were needed; the source archives were not modified. These importer changes are local working-tree changes, not a Git commit or deployment.

- **53 regression tests passed**: [test commands, results, and hashes](importer-validation.json).
- All **383 archived hat accents** produce matching results across all three converters, for 1,149 source cases; all 29 distinct outputs render successfully: [source validation](importer-source-validation.json).
- [Native preview](preview-verification.json) and [committed readback](commit-verification.json) verify exact intended datoms and complete question/tutorial/answer projections.
- [Browser validation](browser-validation.json) covers 1,552 before/after renders at 893px and 375px. **All 388 repaired fields have zero MathJax parse errors**, and math-expression counts are unchanged. [Angle example](sample-2.png).
- [Final exhaustive audit](post-commit-census/summary.json) at basis 3693 found zero remaining malformed hats. Retained history intentionally keeps the earlier values.

## Remaining unrelated limitations

Twenty-one fields have long inline formulas exceeding the 375px mobile width; 16 became visible as real math replaced short error messages. No new desktop overflow was found. These cases are recorded in [render findings](render-findings.json); this transaction preserves their source layout.

Five pre-existing prose delimiter findings and the four missing answer keys are also documented in [structural validation](structural-validation.json) and [the plan](plan.json). This repair does not claim that unrelated formatting or incomplete content elsewhere in the database is corrected.

## Reproducibility

`native/census.rs` scans all string attributes at a pinned basis. `repair.py` classifies candidates and performs the structured repair; source recovery scripts and proofs are under `source/`, `structured/`, and `flattened/`. `prepare.py` composes the guarded transaction. `finalize.py` refreshes all affected records, previews, verifies, and submits using the persisted exact request. `verify.py --commit` checks pinned committed readback; `post_commit_scan.py` repeats the complete database audit at the receipt basis.

Full-census evidence was refreshed through basis 3690. Final affected-record snapshots and the preview use basis 3692, and the exhaustive post-commit audit uses basis 3693. Earlier evidence snapshots are retained in their `evidence-b.../` directories.
