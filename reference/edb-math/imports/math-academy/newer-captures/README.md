# Newer Math Academy captures — prepared

Supporting documentation is stored under `/home/jake/Developer/Course_Academy/reference/edb-math`. Database files, images, schema, seeds, and prepared transaction EDNs remain under `/media/jake/SSD/EDB/math`; relative data paths below refer to that database folder.

Nothing has been transacted. `math` remains at basis **71**.

`1-originals/` contains **61 ordered EDN batches**, to be transacted as **`:org/Math-Academy`**. All passed EDB’s noncommitting `with` validation. Their contents are:

- **19,700 practice questions** with **23,108 complete answer fields**, original choices, and confirmed keys. **17,445** of those question identities are new to `math`.
- **2,823 canonical worked examples**, preserving their `e-` identities and canonical-example roles.
- **1,998 tutorials**, including **11 new tutorial identities** and **one update to an existing tutorial**.
- **28 multipart problems**, with captured context and part order, wrapped as reusable assignment activities with their MA titles.
- **28 distinct assessment/diagnostic instruction bodies** from **37 captures**.
- **3 new knowledge points**, attached to their existing topics. **No new topics**.

The reviewed input is **2,198 verified completed captures** across the four streams. **12 unfinished activities are excluded**.

`held-questions.json` preserves **2,103 questions** with captured controls and solutions whose full keys could not be confirmed without interpretation. They are absent from the ready transactions. All **35 previously missing graphics** were recovered through the separately verified account for each capture stream; all **27 affected tutorials** are now in the ready batches. `held-tutorials.json` is empty. See `graphic-recovery.json`. `unplaced-tutorials.json` is empty. Final batch `061-lesson-activities.edn` updates all six affected lesson activities to the current source order, adds the 11 tutorials and three new example/practice sections through 14 new steps, and preserves 28 existing step UUIDs. It also updates the title of topic 6669 and its lesson to “Piecewise Continuity and Piecewise Smoothness.” All 19 canonical examples are linked to their knowledge points. The current sequences and raw source evidence are recorded in `original-batches.json` and `source-evidence/`.

The original question/example/multipart images are already in `math/images/`. Available tutorial graphics have also been copied there by SHA-256, using the same two-character folders and preserving PNG/SVG extensions. EDN references relative image paths; no image bytes enter EDB. Original captures remain in place.

`2-corrections/` contains **74 later transaction drafts** representing **88 verified correction events on 83 entities**. Review `correction-review.md`. Apply these only **after the original MA content**, using the **assistant source that will be created later**. The assistant source has not been created. Do not attribute these corrections to Jake or MA. All 83 affected original entities are included in the ready original batches.

Read `full-content-review.md` for sources, transformations, exclusions, and limitations. `original-batches.json` is the exact original transaction order; `correction-batches.json` is the later correction order. `original-preview-validation.json` and `structural-validation.json` record validation. An EDB `with` result showing a hypothetical later basis is a preview; it did not commit.
