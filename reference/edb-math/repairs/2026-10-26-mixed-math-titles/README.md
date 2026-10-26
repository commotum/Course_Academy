# Mixed SVG title formula repair

Completed 2026-10-26 using the EDB skill. The requested tutorial **17592186060931** was repaired first at **T8029**. A subsequent database-wide source audit produced a second atomic repair at **T8044**: **354 formulas in 157 content fields, across 140 entities and 89 lessons**. Together, the transactions restore **357 formulas in 158 fields**.

## Cause

The legacy Math Academy HTML-to-JSON extractor selected the first descendant assistive MathML root. Some archived SVG titles combine literal outer TeX with nested MathJax for only a small inner fragment. Selecting that fragment silently discarded the equation around it. Later formatting passes could typeset the remaining fragment successfully without recovering the missing mathematics.

In tutorial 17592186060931, that discarded `det(A) =`, the determinant fences, `= ad-bc`, the leading `A =` labels on two matrices, and explanatory colors. The original source and retained database history establish that the loss already existed at the first retained import, T35. See the [original investigation](../../audits/2026-10-25-question-17592186060931/README.md) for the exact source and reproduction.

## Scope and selection

The audit examined all **2,964 archived lesson HTML pages** against a native current-fact snapshot at T8029. There were **4,164 mixed-title source formula occurrences across 653 pages**; these are source shapes, not defect counts. Many database expressions were already complete.

Candidates are bound to the source lesson, tutorial/question identity, content attribute, exact source title, and exact current math span. Full formula sequence alignment and surrounding prose distinguish truncated formulas from legitimate repeated values such as `0`, `1`, and `n`. The audit excluded 1,500 coincidental candidate pairs using sequence evidence. Residual prose and individual source review added five restorations and excluded the remaining coincidental matches. The three final individual restorations are a borrowing calculation and two labeled systems of equations. No identified candidate is awaiting review.

`final-resolved.json` retains the source title and matching evidence for every bulk restoration. `context-review.json` independently checks surrounding source prose for the first 351 selections; `individual-review.json` records the final residual review. `nondefects.json` retains sequence exclusions. Intermediate candidate files remain provenance, not outstanding work queues.

## Repair and verification

The reconstruction walks each complete title in order, retaining literal TeX and converting each embedded MathML fragment in place. It preserves supported colors, cases, phantom widths, borders, padding, and enclosures. Unsupported structures raise explicit gaps rather than silently losing information.

The transactions use exact old-value `:db/cas` guards. They modify only `:tutorial/content`, `:question/problem`, and `:question/worked-solution`. Canonical answer values, types, field links, question IDs, and learner history are untouched. Source question markers outside mathematics are preserved. Two changed probability problems also receive the equivalent sized delimiter correction `\big\mid` → `\big\vert`: reconstructing their earlier malformed piecewise formulas exposed the otherwise hidden invalid delimiter.

Both batches passed speculative native EDB validation and exact committed readback. Receipts establish only the reviewed content retractions/assertions plus the transaction timestamp. Every one of the 157 bulk fields passed the actual UI MathJax rendering comparison with no new math errors and unchanged image references. The first tutorial was also visually inspected; its unchanged illustration is available from the live asset endpoint. Seven reconstruction tests and ten upstream extractor tests pass.

- [First repair verification](first-17592186060931/verification.json), [transaction](first-17592186060931/transaction.edn), and [rendered tutorial](first-17592186060931/after.png).
- [Bulk verification](batch-001/verification.json), [transaction](batch-001/transaction.edn), [native preview](batch-001/native-preview.json), and [render verification](batch-001/render-verification.json).
- [Completion counts](completion.json).

## Prevention

Patched `/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py` and its regression tests. Mixed titles with literal outer text and partial descendant MathML now stop extraction with a descriptive error, instead of publishing the fragment as the complete formula. This is a guard, not an automatic reconstruction feature. The original HTML and derived legacy artifacts remain retained evidence.

Current browser capture already preserves the whole SVG when mixed-title reconstruction is unsupported. Updated `capture/docs/3-activity-capture.md` and `generate/docs/6-template-generator.md` to require complete-expression preservation and comparison against the original source; a zero-error MathJax render alone does not establish completeness. This audit addresses source-confirmed loss from this particular extraction defect, not every possible mathematical error in the database.
