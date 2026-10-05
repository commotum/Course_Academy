# Historical question response-format audit

All 1,506 questions in the committed historical batch were checked against saved lesson questions from their own knowledge points. The batch covers 605 KPs in 308 topics. Every KP matched its saved lesson through the database's canonical example ID. There was no need to infer a format from another topic or from a global majority.

The original history captures, preparation files, and `import-ready/questions.json` remain unchanged. They record what was captured and what was first imported. This directory records the subsequent corrections.

## Findings and repairs

| Finding | Questions | Action |
|---|---:|---|
| Historical records contain answer controls | 360 | Preserve the observed controls, including symbolic blanks |
| Locally reconstructed blanks; saved same-KP questions consistently use multiple choice | 952 | Author local radio choices with a saved-solution correct key |
| Mixed or other saved formats | 194 | Repair 22; retain 172 compatible responses |
| Total repaired | **974** | 970 radio questions and 4 questions with corrected component blanks |

Missing historical choices were not recovered. The replacement choices are **locally authored**. Saved same-KP options supply suitable option families where usable; local sign, coefficient, component, membership, and categorical errors supply other distractors. Each question's `preparation.response_repair` records the source examples and the authorship of its alternatives.

The four examples that exposed the problem now have these formats:

| Question | Topic | Response |
|---|---|---|
| q-10289 | 278, Sum and Constant Multiple Rules for Differentiation | Radio; correct derivative `24x^5` |
| q-64921 | 268, Trigonometric Ratios of Special Angles | Radio; correct value `sqrt(3)/2` |
| q-16295 | 33, Multiplying Complex Numbers | Two numeric blanks: real part `81`, imaginary coefficient `15` |
| q-118705 | 1467, Volumes of Cubes | Radio; correct volume `8/27 yd^3` |

Three graph-inequality questions now have the same two-blank structure shown in their saved KP examples: a relation and a boundary expression. They still require symbolic grading. Their IDs are q-29440, q-6054, and q-6056.

One reconstructed answer was substantively wrong. **q-23188** asks which listed angles are coterminal with 145 degrees. Its saved solution explicitly concludes: “So the correct answer is II and III only.” The initial reconstruction incorrectly chose an intermediate `145°` formula. The new field uses the confirmed statement subset. The response prompt also removes stray list-bullet hyphens outside the mathematical expressions.

Committed at database basis **652 → 653**. All 974 repairs were applied; none were deferred. All 1,506 stored response formats match the content checked by the native grader. The 4,587 protected facts retain the same fingerprint as before the repair.

## Verification and limits

The native engine accepts the canonical response and rejects every authored noncanonical option for each supported question. Engine readiness increases from **801 to 1,346** questions. All 971 repaired questions intended for current practice pass; the remaining three repairs intentionally preserve the source's symbolic two-blank interaction.

**160 questions remain unavailable for practice:** 156 retain confirmed historical symbolic blanks; three have the repaired source-style inequality blanks; one, q-133897, already matches its KP's single full symbolic blank. These need broader grading support, rather than a forced multiple-choice conversion. The engine's existing filter excludes them.

Mathematical authoring checks reject equivalent options using numerical counterexamples or set-membership witnesses for supported expressions. The checks cover degrees versus radians, trigonometric identities, arbitrary integration constants, finite sums with a bound index, and absolute values. Coterminal-angle alternatives are checked modulo a full turn. Complex inverse-function formulas, infinite sums, and infinite sets use explicit, recorded review rules. This is a conservative authoring aid, not a general symbolic grading system or a statistical evaluation of the new distractors' difficulty. The retained MA difficulty labels describe the original questions.

The database repair uses fresh, versioned fields and answers. It detaches old field ownership while retaining the old field and answer entities unchanged. A question already presented or answered by a learner is excluded from this operation. The preview found no prior learner use of the selected questions.

The transaction is restricted to question prompts and owned answer fields/choices. Question identities, worked solutions, difficulties, KP memberships, learner progress, outcomes, XP, and engine configuration are preserved. Before/after database reads and the protected-fact fingerprint verify this. Reapplication is checked against the exact repaired content.

## Records and reproduction

- `audit.json`: one decision for every imported question.
- `kp-source-index.json`: saved lesson examples, canonical-example matching, format counts, and source hashes.
- `repairs.json`: exact before/after content and question-specific authorship evidence.
- `questions.json`: complete current content after the response repairs.
- `runtime-readiness.json`: native grading results for all 1,506 questions.
- `report.json`: aggregate counts and database verification.
- `database-repair/`: frozen before/after reads, usage checks, preview, guarded intent, transaction, receipt, and verification.

Preparation: `/home/jake/Developer/MA/.venv/bin/python scripts/audit_historical_question_formats.py`.

Database preview: `/home/jake/Developer/MA/.venv/bin/python scripts/repair_historical_question_formats.py`.

Commit the reviewed preview: add `--commit`. A saved intent always retries its exact transaction; the script does not silently replace an existing intent. Do not rerun preparation while resolving an intent, because its content hash is part of the retry guard.
