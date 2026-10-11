# 5. Database Preparation

Turn the saved capture into complete, reviewable transactions for `/media/jake/SSD/EDB/math`.

1. Recover missing or ambiguous content from saved HTML, history, images, and additional source-page reads. Use a recovery sub-agent when needed to resolve content without repeating the activity.
2. Convert source content to Markdown with LaTeX. Prepare complete answer fields and original choices; confirm correct answers from Math Academy's grading or worked solutions. Preserve Math Academy's content, including errors, and record disagreements separately.
3. Hash original image bytes with SHA-256 and copy them to `math/images/<first-two-hash-characters>/<full-hash>.<extension>`, reusing identical files. Rewrite content references as `images/...` relative to the database folder and verify every image exists.
4. Compare with the current database and deduplicate by source identity. Reuse existing UUIDs for questions, examples, knowledge points, tutorials, steps, and activities, including confirmed source revisions. Missing captured fields must not erase existing content.
5. Prepare the schema relationships: knowledge-point question pools and canonical examples, lesson content references and step order, and multistep shared context and ordered parts.
6. Calculate `topic/difficulty` from the lesson's base XP and the [agreed workload formula](../../reference/xp-docs/expected-distribution-base-xp.md), retaining the selected questions, inputs, and formula version.
7. Build EDN containing the required changes. Attribute Math Academy's original content to `:org/Math-Academy`. Keep calculated metadata separate with its own source attribution. Save proposed corrections for later review and transaction after the originals.
8. Validate entities, answer fields, references, ordering, images, and attribution. Pass complete batches and the database basis used to Transaction/Commit. Continue recovery for incomplete items while complete, independent content proceeds.

Keep learner attempts, XP/progress observations, and reasoning as evidence for later import. Save preparation notes with the captures under `reference/`. Previewing and committing transactions belong to the next stage.
