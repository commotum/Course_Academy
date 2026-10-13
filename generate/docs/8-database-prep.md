# 8. Database Preparation

Python turns validated generator output into reviewable transactions for the configured `math` database. Follow [$edb](../../skills/edb/SKILL.md), reusing the project's integration and installed schema.

1. Read the generated questions, plot assets, validation results, and current database at one recorded basis and lineage; batch identity and pool lookups with Datalog and Pull.
2. Validate the difficulty, mathematics, complete answer fields, correct answers, worked solutions, and actual learner grading; return invalid instances to the generator for correction or resampling.
3. Hash plot asset bytes with SHA-256, publish them through the existing content-addressed asset store, rewrite references relative to the database folder, and verify stored bytes and availability.
4. Match stable generated identities and mathematical content against existing questions, reusing unchanged question, field, and field-owned answer UUIDs; changing seed or option order alone does not establish a new question.
5. Convert review JSON into typed EDN using existing attributes, enum refs, UUIDs, and lookup refs; associate accepted questions with `:knowledge-point/questions` and their intended difficulty.
6. Resolve the configured contributor for generated content and prepare one coherent information set per transaction, preserving unrelated facts, existing pool members, and historical responses.
7. Request the installed question, answer-field, answer, and applicable knowledge-point validation specs with `:db/ensure`, using the native predicates deployed on the writer.
8. Save complete batches, source attribution, asset hashes, generator version, parameters, validation evidence, and preparation basis and lineage, then pass them to [Database Commit](9-database-commit.md).

Keep generated content separate from captured source identities: omit Math Academy content IDs from new questions and retain source-template references as evidence. Preserve authored answer shapes and field keys; canonical answers belong to their field's bank, including blanks. Do not import incomplete or ungradable generated practice questions. Unsupported instances leave the inventory shortage pending.

`knowledge-point/question-generator` is a ref whose target representation still needs finalizing. Keep scripts and recipe metadata in the saved generation package until that schema and interface are defined; do not store a file path in the ref or invent generator attributes. New content must preserve existing questions and referenced answer values rather than revise previously served instances.

Persist preparation evidence under `reference/`. Database outages retain pending work for automatic retry against a fresh basis. Preparation does not preview or commit; unchanged batches are recorded as no changes.
