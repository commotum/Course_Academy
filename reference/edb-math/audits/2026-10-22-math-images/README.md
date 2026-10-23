# Math formulas imported as images

At database **`math`, basis 5565**, **1,526 content entities** contain **6,919 confirmed formula-image occurrences** in **1,973 attributes**, across **547 topics**. They are **934 canonical worked examples and 592 tutorials**. No current ordinary practice question, answer value, answer-field key, feedback, or multipart context was found to contain this MathJax-to-image conversion defect.

| Attribute | Affected attributes |
| --- | ---: |
| `question/problem` | 716 |
| `question/worked-solution` | 665 |
| `tutorial/content` | 592 |
| Total | 1,973 |

The formulas use **4,754 distinct SVGs and 740 distinct raster images**. Reuse accounts for the larger occurrence count: **6,159 SVG occurrences and 760 raster occurrences**.

This investigation changed no database facts or production import behavior. The scripts added for it only read EDB and write local audit artifacts. The inventory is bound to one captured basis; later imports are outside that snapshot.

## What went wrong

The affected captures sometimes retained only MathJax's rendered SVG paths, without a TeX annotation, SVG title, or assistive MathML. Other fallback cases have complicated SVG titles containing both literal TeX and nested rendered MathML. The extractors preserve these renderings as image assets instead of declaring semantic formula extraction incomplete.

The legacy extractor explicitly says “Some server-rendered formulas have only SVG paths, with no local TeX or assistive MathML. Preserve their visible rendering as a formula image.” See [asset selection in `dom.js`](../../../../scripts/question_capture/dom.js:60). The [active extractor](../../../../capture/scripts/browser/extract.js:47) retains the same behavior. The formula renderer returns the SVG's asset marker when it cannot obtain MathML or title text. These cases produce **`errors: []`**.

The legacy [browser reader](../../../../scripts/question_capture/browser.py:629) saves those assets with `asset.screenshot()`, making PNG formula images. Newer [asset collection](../../../../capture/scripts/browser/assets.py:416) and [saved-source recovery](../../../../capture/scripts/recovery.py:104) preserve standalone SVG bytes, which improves graphic fidelity but still leaves mathematical text represented as an image.

The newer-captures importer then accepted these nonempty, error-free source records and preferred the latest complete occurrence by old basis/task order. It did not compare formula recoverability with the existing text. See [source extraction](../../imports/math-academy/newer-captures/extract-newer-source.py:44) and [latest-occurrence selection](../../imports/math-academy/newer-captures/prepare-newer-common.py:33). Its [review documentation](../../imports/math-academy/newer-captures/full-content-review.md) explicitly accepted saved SVG when textual conversion could not preserve a formula. Thus this was an accepted fallback and a missing quality guard, rather than an image-display bug in Study.

That distinction matters: the import could overwrite good, already stored LaTeX with a newer visual-only capture. Content/schema validation, local-image checks, and EDB previews all pass because an image link is valid Markdown and a nonempty problem or solution satisfies the required fields.

## Exact trace for the reported example

Entity **17592186092122**, UUID `7df7fed3-c172-5cc2-aca8-abd31a0902a0`, is canonical example **`e-731`** in topic **1036**, “The Chain Rule With Logarithmic Functions.”

| Current-lineage transaction T | UTC instant | Representation |
| --- | --- | --- |
| 42 | 2026-10-11 08:30:45.802 | Correct Markdown/LaTeX in the problem and solution |
| 80 | 2026-10-11 08:33:22.587 | Two problem formulas and four solution formulas replaced by PNG links |
| 2368 | 2026-10-14 21:01:13.954 | The same six formulas represented by SVG links |

All three changes were attributed to **`:org/Math-Academy`**. The original archived lesson Markdown still contains the textual derivation, including `y = \log_2(\ln{x})` and its derivative. Its [JSON](../../../../../MA/DATA/Lessons/1036/Source/1036.json), [HTML](../../../../../MA/DATA/Lessons/1036/Source/1036.html), and [Markdown](../../../../../MA/DATA/Lessons/1036/1036.md) remain available locally.

The intervening source occurrence is recorded in `newer-captures/source-occurrences.json`: stream `question-capture`, task **13933323**, source `reference/mathacademy/question-capture/13933323/example-731.json`. That saved example contains **six SVGs, no `<math>`, no `<title>`, and no extraction errors**. Its six original SVG byte hashes match the six SVG references currently stored on the entity. No image recognition is needed to establish their lineage.

An offline browser reproduction against that exact saved HTML gives the same result for **both** extractors: six image asset markers, zero textual formulas, and an empty errors array. See [example-reproduction.json](example-reproduction.json) and [example-lineage.json](example-lineage.json).

The comparison entity **17592186093370**, tutorial **1272**, retains LaTeX, including `y = \ln(2x+1)` and an aligned derivative calculation. The database supports the desired representation; the degradation is upstream.

## Inventory and coverage

- [affected.csv](affected.csv): one row per affected entity/attribute, with topic IDs, source content identity, transaction, contributor, occurrence count, and current-value hash.
- [findings.json](findings.json): exact current values, each formula-image path and character offset, and ownership/topic context.
- [assets.json](assets.json): every referenced canonical asset and its classification/evidence.
- [summary.json](summary.json): machine-readable counts and attribute coverage.
- [export-manifest.json](export-manifest.json): exact database basis and domain attribute counts.

The export examined all current domain string values, including fields outside the original example: problem and solution text, tutorials, answer values and feedback, field keys, titles, and multipart context. It examined **2,719,295 exported current facts**, **37,458 image-bearing facts**, **47,591 canonical image occurrences**, and **41,223 distinct referenced assets**. No topic/course restriction was used.

SVG classification uses MathJax structural markers and rendering geometry, not the `.svg` suffix alone. Raster formulas are linked to saved original SVG metadata. The source pass read **12,395 distinct evidence files**; 2,911 byte-identical file copies were skipped. Genuine source images were checked against their original image metadata and the archived MA image map.

The remaining **1,846 raster assets** were reviewed separately: **1,486 generated graphics** and **360 graphs/diagrams**. Their producer metadata, review indices, and contact sheets are retained in [raster-review-index.json](raster-review-index.json) and [raster-review-decisions.json](raster-review-decisions.json). They are not standalone formula screenshots. The automated unresolved-raster review is now empty. Three noncanonical `/api/asset?...` references were also checked; they are school-assignment diagrams, listed in [noncanonical-image-review.json](noncanonical-image-review.json).

This is an inventory of currently retained formula images, not a claim that every historical conversion remains broken. Corrected content with no current formula-image reference is excluded. A history record's first image assertion is not necessarily its first bad formula conversion when the field also contains legitimate diagrams.

## Recovery sources and batch repair boundary

[recovery-candidates.json](recovery-candidates.json) binds every affected attribute to retained history and archived lesson content IDs:

| Available source | Attributes |
| --- | ---: |
| Earlier image-free math and matching archived lesson content | 1,568 |
| Earlier image-free math, without a matching archived content ID | 7 |
| Matching archived lesson content, without earlier image-free math | 265 |
| Formula-level source recovery still needed | 133 |

Thus **1,575 attributes have earlier image-free math** and **1,833 match archived lesson content**; the union covers **1,840 of 1,973**. The remaining 133 stay in the same inventory and retain their exact image/capture evidence. They require recovery at formula level from source HTML/SVG titles, alternate captures, or a source reread before a complete repair can be prepared.

Older whole-field text is a candidate, not an approved rollback. Some earlier content predates subsequent mathematical, notation, or prose corrections. A repair should recover each formula, preserve valid diagrams, current prose and answer-field placeholders, and retain all entity identities and learner references. The current value hashes and source bindings permit exact preflight comparisons and attribute CAS. Restore all reviewed formulas in a prepared batch only after source comparison and rendering through the actual Markdown/MathJax player.

The prevention change should distinguish **formula rendering preserved** from **formula text recovered**, recover semantic math from alternate source evidence where possible, and prevent a visual-only capture from silently replacing valid textual math. Missing semantic math must remain visible to preparation/review even when the screenshot or SVG renders correctly. No such production change was made during this investigation.

## Reproduction tools

The read-only exporters are [export_math_image_audit.rs](../../../../scripts/export_math_image_audit.rs) and [export_math_image_history.rs](../../../../scripts/export_math_image_history.rs). They are built against the application's EDB release library. [audit_math_image_imports.py](../../../../scripts/audit_math_image_imports.py) scans the export and source evidence; [summarize_math_image_history.py](../../../../scripts/summarize_math_image_history.py) binds recovery sources. Raw current/history exports remain under ignored `.local/edb/math-image-import-audit-2026-10-22/`.

The audit classification tests passed: `python3 -m unittest discover -s tests -p test_math_image_audit.py` (four tests). They cover formula-versus-diagram discrimination, raster provenance, repeated occurrences, noncanonical references, and preserving conflicting math evidence beyond the provenance-example limit. The offline reproduction opens no external URLs, and no database writer is used by these tools.
