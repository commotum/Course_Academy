# Content reconciliation and import plan

## Goal

Enrich the existing durable `course-academy` EDB database with the best available content from `MA/DATA/Lessons`, `study/vault/MA`, and `study/vault/SU26`. Preserve canonical entity identities and course relationships. Course and assignment copies are candidate sources for the same content; they do not automatically create additional lessons or questions.

Use `study/util` as source evidence too: its answer CSVs, layout registries, repair records, and Python scripts document how the vault keys and corrected questions were created. The current global question ledger is `study/vault/MA/Questions.csv`; older scripts refer to a lowercase path that is now stale.

This pass covers Mathematical Foundations I, II, III (`MF1`, `MF2`, `MF3`), Linear Algebra (`LAL`), Multivariable Calculus (`MVC`), Differential Equations (`DEQ`), Calculus I (`CA1`), and Calculus II (`CA2`), in that order. Use `Catalog.csv` course membership to select topics. Process each shared topic once, at its earliest course in this list. Copies in other courses may supply evidence for those topics; topics outside this union are deferred.

## Evidence driving the import

Topic 1176, **Telescoping Series**, has three substantive forms: the DATA capture has malformed summation notation and no keys; the SU26/253/M2/OHW-3 copy repairs the notation but remains unkeyed; MA vault and SU26/253/M4/OHW-8 copies have repaired notation and eight marked answers. The current database imported the raw prompt for question 53560 and has no correct-answer ref for it.

Topic 1263, **Limits at Infinity of Polynomials**, demonstrates why IDs alone are insufficient. The CA1 Markdown assigns `ma-65470` to a polynomial limit, while its accompanying JSON and the MF2 Markdown identify that ID with a ratio of polynomials. The Markdown IDs shifted between questions. Matching by ID without checking content would attach the wrong key.

The initial inventory found 22,517 syntactically keyed MA-vault quiz-block occurrences out of 23,151, and 5,237 keyed SU26 quiz-block occurrences. These include duplicate copies. The MA vault has a fully keyed copy for 1,968 topic IDs. Its quiz blocks mention 12,363 of the 19,644 distinct question IDs in DATA, before checking their identity mappings. A populated key does not itself prove mathematical correctness.

## Import rules

1. **Match components.** Index candidate copies by topic ID. Use captured JSON/CSV to anchor step IDs, content IDs, question identities, and field structure. Match tutorials, examples, questions, and answers individually. Do not select an entire folder or the newest file as universally authoritative.
2. **Compare actual content.** Ignore navigation, course codes, whitespace, quiz wrappers, option order, and equivalent asset paths. Match question prompts and answer values, with image content checked where needed. An ID, ordinal, or fuzzy similarity alone cannot authorize an answer-key transfer. Keep unresolved differences in a review report.
3. **Recover existing improvements.** Prefer unambiguous corrected LaTeX and complete instructional text from vault copies. Parse radio keys, inline blank answers, and select-list keys into ordinary schema entities. For selection questions, resolve the correct answer by its value to an existing candidate entity. For blanks, create a deterministic expected-answer entity. Import question explanations only when actually supplied for that question.
4. **Check quality.** Require complete field mapping, a unique correct selection, consistent keys among matching candidates, valid local image targets, and no obvious worsening of mathematical markup. Independently verify the pilot answers and tractable mathematical cases. Report sourced keys separately from mathematically verified keys; never claim universal mathematical verification from structural checks.
5. **Update in place.** Reuse existing UUIDs and existing field/choice entities. Do not create additional topics, lessons, knowledge points, or practice questions for duplicate file copies. Do not copy a key across genuinely different questions sharing an ID. Keep provenance and conflicts in a compact migration manifest, without loading old file variants into the canonical database.
6. **Audit a failed match.** A parser or matching failure is not evidence of a missing answer. Check the original answer registry, corrected layouts, manual repair records, every associated vault copy, and asset locations. Record whether the answer is actually absent, safely recovered, or present but blocked by a specific conflict. Registered additions to deficient answer choices may require a new answer entity; retain the original question and field identities.

## Execution

- Build independent question/answer and tutorial/example reconciliation scripts. Generate small EDN batches plus source-selection and unresolved-case reports under ignored `.local/edb/reconciliation/`.
- Validate pilots 1176 and 1263. Confirm repaired text, correct keys, unchanged question identities/counts, and correct handling of the shifted vault IDs. Submit final batches in the course order above.
- Independently audit proposed transactions before submission. Use explicit lookups for existing records and deterministic IDs only for newly required expected answers.
- Submit approved unambiguous updates through the existing local durable writer with stable request keys. Validate referenced answers and fields, and the completed question, in the same transaction.
- Query the durable database to confirm the pilot and bulk counts. Check that topic, lesson, KP, question, field, and existing candidate counts do not grow from duplicate source copies. Added blank-answer entities are expected and counted separately.

## Remaining cases

Ambiguous identity matches, conflicting keys, uncertain mathematical changes, unsupported response formats, missing assets, and missing source content remain explicit review items. Do not infer question difficulty, encompassing weights, or unknown keys from formatting or neighboring questions. Generated answers and new lesson content require a separate verified pass.

## Status

### Remaining-course import — October 2, 2026

The deferred source-backed enrichment is committed to `course-academy-v2`, advancing from basis 210 to 248. All 32 MA course identities and all 2,964 captured lessons were already present; this pass reconciled the remaining 1,292 captured topics against their vault copies and original captures. No files were moved, and no duplicate courses, lessons, questions, or fields were created.

Recovered canonical correct answers for **1,615 questions**, adding **1,625 field-to-answer links** and one verified missing answer choice. Repaired 110 practice prompts, 589 existing answer values, and 417 answer representation types. Five radio rewrites were mapped back to their original dropdown fields; four probability questions retained the complete original table headings and columns. Source classifications are preserved: 1,557 manual keys, 57 previously marked image-derived keys, and one recorded mathematical repair. No new feedback was available in the matched copies.

Reviewed 2,014 vault instruction copies comprising 11,020 components. They contained no substantive improvements over the captured instruction text. Original MathML supported repairs to **210 components** across 119 topics: 73 tutorials, 131 worked solutions, and six example problems. All 278 changed math expressions passed rendering checks. Partial SVG fragments, ambiguous expressions, unsupported brace glyphs, and components whose changed expressions still failed rendering were excluded.

Post-import database verification confirmed every planned value, all 187,625 existing UUID identities, unchanged learner facts and curriculum relationships, and correct-answer membership without new duplicate answer values. The catalog has **19,646 captured practice questions: 12,378 fully keyed and 7,268 still missing a canonical correct answer**. Of those gaps, 6,910 belong to this remaining-course pass; the other 358 belong to the earlier scope. Missing answers were not synthesized.

Seven sixth-grade topics still have no captured lesson: 555, 2383, 2384, 2385, 2386, 2387, and 2520. Their vault entries explicitly record missing source material. Instruction review also retains 104 known malformed components and 45 unsupported/ambiguous source components; these sets overlap and remain repair work.

The [course coverage CSV](.local/edb/remaining-courses/after-courses.csv), [remaining-pass question gaps](.local/edb/remaining-courses/remaining-question-gaps.csv), [question evidence](.local/edb/remaining-courses/questions/manifest.json), [instruction evidence](.local/edb/remaining-courses/instruction/report.json), and [database verification](.local/edb/remaining-courses/verification.json) record the result. Backup points 210 and 248 remain in `.local/edb/backups/remaining-courses-before/`; the matching before/after exports and transaction receipts are under `.local/edb/remaining-courses/`.

### Earlier eight-course import

Existing answer-key recovery for the eight selected courses is committed to the durable `course-academy` database. The database advanced from basis 64 to 140 across 76 batches: 51 in the first pass, then 25 corrective follow-up batches. GPT-6-sol agents at high reasoning prepared the reconciliations; the main agent reviewed and applied them in the requested course order. Source vaults were not modified, and no Git commit was made.

The user subsequently selected the original `MA/DATA/Lessons/296` versions of questions 48557 and 48616. Their original prompts and choices were retained; a stray Markdown navigation fragment was removed from one choice at basis 141. At basis 142, both received verified keys and explanations. The farmer question requires tons squared per dollar, so that missing choice was added while retaining its original five options. The circle question uses its existing rate-of-change answer (B), also confirmed in a CA1 vault copy whose Markdown question ID had shifted to `ma-48615`.

The first pass recovered 8,283 keyed questions but left 2,838 under unresolved categories. Calling that pass complete was premature: most remaining answers existed in the vault and original utility records. The follow-up inspected all 8,852 Markdown files under MA/SU26, the original answer workflow, and every associated copy of the remaining questions.

| Course | Distinct topics processed | Captured questions | Questions now fully keyed | Still unkeyed |
| --- | ---: | ---: | ---: | ---: |
| Mathematical Foundations I | 353 | 2,450 | 2,450 | 0 |
| Mathematical Foundations II | 357 | 2,460 | 2,460 | 0 |
| Mathematical Foundations III | 322 | 2,081 | 2,081 | 0 |
| Linear Algebra | 181 | 1,201 | 1,168 | 33 |
| Multivariable Calculus | 187 | 1,181 | 1,165 | 16 |
| Differential Equations | 151 | 962 | 647 | 315 |
| Calculus I | 60 | 401 | 387 | 14 |
| Calculus II | 61 | 385 | 384 | 1 |
| **Total** | **1,672** | **11,121** | **10,742** | **379** |

Shared topics are counted under their first course in this order; later courses still reference the same enriched content. These final counts were calculated from the database's fully keyed question identities, not merely from proposed transactions.

### What the original utilities established

- [ma_free_response_answer_key.csv](/home/jake/Developer/study/util/ma_free_response_answer_key.csv), [ma_free_response_layouts.json](/home/jake/Developer/study/util/ma_free_response_layouts.json), and [ma_imported_free_response_manifest.csv](/home/jake/Developer/study/util/ma_imported_free_response_manifest.csv) supplied explicit answers and source identity evidence for **452** previously omitted free-response questions. The 252/253 registries and manual-answer JSON supplied corroborating history.
- [build_ma_free_response_registry.py](/home/jake/Developer/study/util/build_ma_free_response_registry.py) explains how solved answers and revised layouts were assembled. Comma-joined CSV values are not enough to reconstruct individual fields; the structured layouts and manual answer arrays matter.
- [ma_missing_answer_repairs.json](/home/jake/Developer/study/util/ma_missing_answer_repairs.json) and [repair_ma_missing_answers.py](/home/jake/Developer/study/util/repair_ma_missing_answers.py) record deliberate prompt corrections, added correct choices, and converted selection questions. These explain differences that a strict comparison to the initial capture rejected.
- The current [global question ledger](/home/jake/Developer/study/vault/MA/Questions.csv) marks 2,457 previously unmatched questions as answered. The historical scripts explain the labels and provenance, but neither a ledger flag nor a marked option proves mathematical correctness.

### Follow-up recovery

The follow-up populated **2,457 additional questions**: 1,969 multiple-choice, 452 free-response, and 36 select-list. It added 2,693 field-to-answer links, 649 expected-answer entities for blanks, and 11 corrective choices. No question or field entities were added.

The multiple-choice pass recovered keys using complete prompt/choice comparisons, verified image export relationships, and reviewed repairs. Broken vault image links were resolved against the captured DATA assets only with supporting source evidence. Matching now handles parentheses in image paths and preserves the semantic distinction between a set such as `{0}` and the number `0`.

Seven questions required original HTML/MathML to restore choices: four truncated sign tables, two integral questions that lost roots or exponents, and a vector question whose invisible spacing minus signs had become visible. Another seven needed reviewed prompt corrections. Eleven recorded added choices were mathematically checked. One recorded repair was rejected: topic 759/question 49796 must use the existing “II only” choice under the lesson's explicit definition of an improper integral of the second kind.

For blanks, 59 revised vault layouts changed the number or meaning of input fields. Their solved values were mapped back into the original 133 fields and checked independently. The original complete question prompts were retained because some revised layouts omit givens. Two further registry answers containing full equations were reduced to the expressions needed by their original fields. Selection recovery mapped 21 radio rewrites and 15 split select quizzes back to the captured fields.

The initial pass also refreshed 1,112 prompts, repaired 2,724 choice values and 2,201 choice types, and replaced 14 tutorial bodies and 36 example explanations with reviewed notation repairs. Follow-up repairs supplement those changes. These figures overlap; they are not additional question records.

Most keys remain recovered source keys with identity and structural checks. The pilots, disputed choices, manual field mappings, and specified repairs received additional mathematical or content review. This is not a claim that every imported question was independently solved.

### Database verification

At basis 140, all **10,976 stored field-to-answer links** match the submitted transactions. There are **10,740 fully keyed questions**, no partially keyed questions, and no selection keys pointing outside their own field's choices.

Topic, activity, step, KP, question, field, tutorial, and example counts remain unchanged. The database contains 19,646 questions and 22,840 fields across all seeded courses. Answer entities increased from 94,640 to 95,489: exactly 838 expected answers for blanks and 11 corrective choices across both passes. Duplicate course/vault copies did not create duplicate questions.

The two targeted resolutions at basis 142 add two correct-answer links and one corrective choice, bringing the totals to 10,978 links, 10,742 fully keyed questions, and 95,490 answer entities. Targeted database pulls confirmed both original prompts, all ten original choices, the added units choice, both correct-answer refs, and both explanations.

At basis 143, another 27 question explanations were recovered from four MA-vault lessons: Completing the Square, its Odd Linear Terms and Leading Coefficients lessons, and Dividing Polynomials Using Synthetic Division. Their quiz IDs had been rewritten to `q-*`; matching the actual problems and response structures established their captured MA identities. Seven explanations came from whole-question feedback and twenty from correct-option feedback. The importer had omitted this feedback. Exact database reads now confirm all 27 texts, bringing `question/explanation` to 29 populated questions without changing answer keys. Incorrect-option feedback remains in the source files and the reconciliation evidence; the current answer schema has no attribute for it.

### Remaining work

- **379 questions with no key recovered yet:** 204 free-response and 175 select-list questions. All 768 associated current vault occurrences contain matching raw unanswered question blocks. None of these question identities appears in the checked manual-answer, layout, or repair registries. Their distribution is LAL 33, MVC 16, DEQ 315, CA1 14, CA2 1. The user identified an abandoned conversion of free-response/dropdown questions to multiple choice followed by later answer-key work. The later July 14 registry does exist, but its builder only scans existing quiz blocks, excluding raw questions. A follow-up inspection of all 434 committed revisions of the 179 affected lesson files found no keys in those question sections. This establishes absence from the checked sources and history, not that no answer exists elsewhere.
- **1,105 instructional review entries** from the earlier pass remain: malformed notation without an accepted replacement or substantive differences requiring review. Completing answer-key recovery does not finish those instructional repairs.
- Other courses remain outside this enrichment pass.

### Implementation and import records

- [Initial question reconciler](scripts/reconcile_ma_questions.py), [instruction reconciler](scripts/reconcile_ma_instruction.py), [follow-up multiple-choice reconciler](scripts/reconcile_unmatched_mc.py), and [follow-up field reconciler](scripts/reconcile_unmatched_fields.py).
- [Apply driver](scripts/apply_ma_reconciliation.py) previews each batch, then commits with a content-derived idempotency key. New answers use transaction tempids; existing entities use UUID lookup refs.
- [Follow-up summary](.local/edb/reconciliation/followup-summary.json), [multiple-choice evidence](.local/edb/reconciliation/followup-mc/manifest.json), [field evidence](.local/edb/reconciliation/followup-fields/manifest.json), [manual field mappings](.local/edb/reconciliation/field-shape-review.json), and [unpopulated-key audit](.local/edb/reconciliation/absent-key-audit.json).
- [Initial batch order](.local/edb/reconciliation/apply-files.json) and [journal](.local/edb/reconciliation/commits/journal.jsonl); [follow-up batch order](.local/edb/reconciliation/followup-apply-files.json) and [journal](.local/edb/reconciliation/followup-commits/journal.jsonl).
- [Final verification](.local/edb/reconciliation/followup-verification.json) records exact link, completeness, selection-membership, and entity-count checks. Generated evidence, EDN batches, and query snapshots are local artifacts under ignored `.local/edb/reconciliation/`.
- [Original-source verification](.local/edb/reconciliation/source-priority/verification.json) confirms both selected original prompts and all ten choices at basis 141, with no vault answer keys imported.
- [Resolved-answer verification](.local/edb/reconciliation/source-priority/resolved-verification.json) records the two completed keys, retained original content, and supporting reasoning at basis 142.
- [Feedback verification](.local/edb/reconciliation/feedback/verification.json) confirms the 27 imported explanations at basis 143; [source mappings](.local/edb/content-audit/feedback-mapping-review.json) identify the matched questions and vault locations.
