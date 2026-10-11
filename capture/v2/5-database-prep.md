# 5. Database Preparation

Python turns the checked capture into reviewable transactions for `/media/jake/SSD/EDB/math`. It detects exceptions and calls an agent only when a database identity or revision match needs judgment.

1. Read the checked capture and the current database at one recorded basis. Validate the required source content and answer evidence. Any newly discovered source gap returns to Activity Capture for resolution; do not fill it with a guess.
2. Convert source content to Markdown with LaTeX and build answer fields from the confirmed choices and answers. Preserve Math Academy's content, including errors, and the separately recorded disagreements.
3. Hash original image bytes with SHA-256 and copy them to `math/images/<first-two-hash-characters>/<full-hash>.<extension>`, reusing identical files. Rewrite content references as `images/...` relative to the database folder and verify every image exists.
4. Match known source identities and reuse existing UUIDs. Python detects multiple possible matches, conflicting mappings, or possible revisions with changed source IDs. It sends only those cases, candidate entities, and source evidence to an agent. The agent proposes a match or a new entity with reasons; Python checks the references and consistency before accepting it. Missing captured fields must not erase existing content.
5. Prepare the schema relationships: knowledge-point question pools and canonical examples, lesson content references and step order, and multistep shared context and ordered parts.
6. Calculate `topic/difficulty` from the lesson's base XP and the [agreed workload formula](../../reference/xp-docs/expected-distribution-base-xp.md), retaining the selected questions, inputs, and formula version.
7. Build EDN containing the required changes. Attribute Math Academy's original content to `:org/Math-Academy`. Keep calculated metadata separate with its own source attribution. Save proposed corrections for later review and transaction after the originals.
8. Validate entities, answer fields, references, ordering, images, and attribution. Pass complete batches and the database basis used to Transaction/Commit. Keep unresolved cases explicit and out of those batches; complete, independent content can proceed.

Steps 1–8 are scripted in Python; step 4 includes the conditional agent call. Content interpretation and source-page recovery belong to Activity Capture. Keep learner attempts, XP/progress observations, and reasoning as evidence for later import. Save preparation notes with the captures under `reference/`. Previewing and committing transactions belong to the next stage.
