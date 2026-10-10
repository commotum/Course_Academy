# Full content review

This preparation reviews the four newer capture streams under `/home/jake/Developer/Course_Academy/reference/mathacademy`: `question-capture`, `question-capture-workers/linear`, `question-capture-workers/multivariable`, and `question-capture-workers/differential`.

## Sources and content

| Material | Original saved evidence | Prepared representation |
|---|---|---|
| Practice prompts and response controls | `state.json` question `before`, `q-<id>-before.json`, original question HTML | `question/problem`, owned answer-field and answer entities; original `q-` identities |
| Worked solutions | MA revealed after-answer/history HTML in `state.json`, `q-<id>-after.json`, or `history-q-<id>.json` | `question/worked-solution`, including source mistakes |
| Explicit answer keys | MA `source_correct` controls and completed activity-page `raw_html` in `activity-metadata.json` | Exact displayed source key; dropdown choices preserved |
| Graded choices | MA’s Correct outcome plus the captured radio/dropdown selection and authored choice list | That existing MA choice, not a new distractor or a solver-selected key |
| Solution-derived keys | Explicit named choice, final expression/equality, completed template, labeled table cell, or stated truth labels in MA’s worked solution | Faithful extraction with per-field evidence; no algebraic solving, generated alternatives, or mathematical corrections |
| Entered answer keys | MA-displayed correct answers; in the few accepted-submission cases, values also confirmed in MA’s authored solution | Authored source value; q-263419 uses MA’s final `\frac{65}{2}` rather than the submitted decimal `32.5` |
| Canonical worked examples | `example-<id>.json` and its saved MA HTML | Canonical `e-` entities; absent interactive controls do not remove earlier controls |
| Tutorial explanations, formulas, diagrams, tables and links | `tutorial-<content-id>.html` | Markdown/LaTeX; exact saved SVG when textual conversion cannot preserve the source formula |
| Multipart context and order | MA HTML/JSON captured into `shared_contexts`, per-question local prompts, and `content.json` `question_order` | A reusable multistep, owned inner steps, one assigned-problem with topic coverage, and a titled assignment activity |
| Assessment/diagnostic introductory instructions | `assessment-instructions.html`, `diagnostic-instructions.html` | Standalone tutorial text. Attempt IDs are not substituted for definition IDs |
| KP identity and membership | Captured topic IDs, canonical-example IDs, question/KP associations, and captured example titles | Existing new-database KPs resolved by topic/example identity; three observed new KPs created with their examples and practice pools |
| Images | Capture `assets/manifest.json`, exact inline SVG bytes, or archived MA images with the same source graphic identifier | Hashed files in `math/images/`; relative references in EDN |

**All ready original facts use `:org/Math-Academy`.** New UUIDs, Markdown conversion, schema mapping, deduplication, and explicit-solution key extraction are derived representations of source material. They are not new mathematical content. No LLM-generated answer keys or locally authored choices are included in the original batches.

`questions-with-local-images.json` is the reviewed ready question/example set with its key evidence. `source-occurrences.json` retains the 27,324 verified source occurrences and extraction evidence. Original evidence files remain at their recorded paths. The full source records for held questions remain in `held-questions.json`.

## Identity, sequence, and coverage

Questions are deduplicated by `math_academy_id`; examples retain the `e-` namespace and practice retains `q-`. Existing question UUIDs and KP UUIDs are reused. Old database numeric entity IDs and transaction EDNs are not replayed. Repeated-source differences are indexed in `normalized-content-variants.json`; this preparation selects the latest complete source occurrence available by recorded old basis and task order. Verified no-write captures legitimately have no old commit basis.

All 972 captured topics already exist. The three new KPs are listed in `new-knowledge-points.json`. Their topic membership, title, canonical example, and question pool are prepared; their insertion into a generic lesson sequence is not guessed.

The saved captures do not contain a complete generic step/placement sequence for each lesson. Tutorial content IDs are not generic step IDs. Existing archived lesson sequencing remains intact. The 11 new tutorial identities are preserved as content and indexed in `unplaced-tutorials.json`; their missing placements remain explicit. Live topic 6377 confirms that tutorial 15932 replaces 14488 in the third section, and placement 655321 replaces 588705. Batch 058 updates the existing tutorial and step through their stable UUIDs; lesson ownership and sequence links remain unchanged. The source page is retained in `source-evidence/topic-6377.html`. `original-batches.json` records both old and new MA IDs against each stable UUID for subsequent import resolution. Two legacy tutorial content IDs (8472 and 8544) occur in multiple topics; those resolve through the already imported archived placement identities rather than incorrectly collapsing them.

All 28 multipart problems have one captured shared-context block and a complete captured question order. Their outer assignment wrapper and topic-coverage mapping are schema translations; their titles, context, questions, and inner ordering come from MA. A generated UUID is not represented as an MA placement ID. See `multisteps-reviewed.json`.

Assessment introductory text is preserved. Attempt-specific selections do not establish a universal assessment question bank or diagnostic routing tree. Timing rules and other task metadata remain recorded in `activity-definition-evidence.json` where no complete definition can be established with the installed schema.

## Holds and exclusions

**2,103 practice questions are held for unresolved answer keys.** Their controls and worked solutions were captured; the problem is confirming every correct answer without substituting a solver’s interpretation. No partial answer-field question enters the ready batches.

**All 35 previously missing graphics have been recovered, and all 27 affected tutorials are ready.** The user authorized account-specific authenticated retrieval. Each separate saved account was verified against its configured username and enrolled course before fetching its stream’s captured image URLs: Mathematical Methods 22, Linear Algebra 1, Multivariable Calculus 6, and Differential Equations 6. The original PNG responses were verified, hashed, and copied to the SSD library; the affected tutorials’ exact saved SVG formulas are also preserved. See `graphic-recovery.json`. No activities were performed and no generated diagrams were substituted.

The 12 unfinished activities are excluded. Learner submissions, attempt outcomes, elapsed times, XP earned, mastery, learner state, engine state, recovery bookkeeping, screenshots, and grading/model decisions are not imported as reusable MA content. Their relevant source evidence remains available in the capture folders. Authored scoring instructions can be included as instructional text; learner XP facts are excluded.

## Later corrections

`correction-review.md` and `correction-events.json` describe the 88 verified correction events on 83 questions/examples. The archive `mathematical-corrections/` preserves their original evidence and review records. All 83 original entities have ready MA-original representations, including source errors. The 74 correction drafts follow the original batches and require the assistant source to be created later.

The 198 answer-replacement decisions in `answer-reconciliations.json` are separately preserved: these include source restoration and formatting, so they are not all mathematical corrections. Original batches reconstruct MA evidence directly rather than trusting locally revised `content.json` keys.

Corrections replace component ownership links without deleting original field/answer entities. Stable identities refer to this new database. The correction drafts passed structural checks, including correct-choice membership and absence of old numeric IDs or entity-deletion operations. Their sequential database preview requires the original commits and assistant source; they have not been applied.

## Validation

All 60 original EDNs passed EDN round-trip checks, per-file size limits, complete field/correct-choice references, unique question identities and component ownership, local image-path checks, and native EDB `with` previews. All preview facts were attributed to MA’s source entity. Exact standalone SVG syntax and internal references were checked. Final prepared bytes match the validated bytes. The database status after validation remains basis 71.

After explicit authorization, graphic retrieval used each stream’s existing saved browser profile directly. No cookie values or passwords were copied into preparation files or printed. All 60 final original batches remain validated; only the eight tutorial batches changed by recovery required new native previews. The database remains at basis 71.
