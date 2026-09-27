# Available MA data and remaining gaps

Audit date: September 26, 2026. Primary scope: `/home/jake/Developer/MA`. Related learner observations in `/home/jake/Developer/study/vault/252` are identified separately.

We have a substantial captured curriculum, instructional library, and prerequisite graph. We do **not** yet have a complete graded question bank or the data needed to reproduce MA's retention model faithfully. In particular, the inspected MA corpus has no populated question-difficulty catalog and no exported encompassing relationships/weights.

“Available” below means an actual artifact contains values. Documentation describing a field, code mentioning it, and a proposed schema are not populated data. Counts describe the local snapshot, not the entire live MA platform.

**Data already present in `Developer/MA`**

| Data | What we have | Location / qualification |
| --- | --- | --- |
| Courses | 32 course identities | [Courses.csv][courses] |
| Course structure | 315 units and 1,122 modules | [Units.csv][units], [Modules.csv][modules] |
| Topic catalog | 2,971 distinct topics | [Topics.csv][topics]; primarily IDs and names |
| Course-topic membership | 7,555 placements; 2,002 topics appear in multiple courses | [Catalog.csv][catalog]; hierarchical codes are local normalization |
| Reference lessons | 2,964 topics with source HTML, normalized JSON, and Markdown | [Lessons directory][lessons]; seven catalog topics lack captured structure |
| Instructional steps | 15,652 tutorial/example placements | [Steps.csv][steps]; 6,016 tutorials and 9,636 examples |
| Worked-example solutions | All 9,636 example placements have problem and explanation sections in normalized JSON | These solve the worked examples, not the separate practice questions |
| Practice-question content | 19,646 placements referencing 19,644 distinct question IDs | [Questions.csv][questions] and per-topic JSON; these are captured reference-page samples |
| Question response structure | Multiple-choice options, free-response positions, select inputs, and relevant rich content | 16,570 multiple-choice placements, 2,010 free-response, 1,066 select-list |
| Question content availability | Every normalized question placement has a nonempty prompt and is marked as present in the snapshot; none requires hydration according to the export | Availability flags are not a mathematical or rendering-quality audit |
| Direct prerequisites | 6,560 topic-to-required-topic pairs | [Prerequisites.csv][prereqs] |
| Key prerequisites | 9,167 step-to-required-topic rows | [Key-Prerequisites.csv][keyprereqs]; distinct from direct prerequisite edges |
| Figures and screenshots | 14,715 PNG files under `Images`, 38,283 under `Sections` | Includes capture/render artifacts; file counts are not counts of distinct mathematical figures |
| PDFs | 2,605 lesson PDFs | Under per-topic `Source` directories; another rendering of captured content |
| Engine descriptions | Book chapters, diagrams, excerpts, and interpretation notes | [Proprietary.md][proprietary], [Proprietary-Notes.md][notes]; useful specifications but not production-state exports |

All 2,964 current per-topic JSON files parsed successfully. The question objects consistently contain content/format fields, with no structured difficulty, timing, grading, solution, or encompassing fields found in the question-object audit.

Some identity relationships are also available but need careful import. A step is an ordered placement of typed tutorial/example content. Example content can correspond to a KP; a verified completed-task KP link maps to example 2993 at step 9670. Questions can be reused across placements, with different choice orders. The [schema report](mathacademy_schema_architecture.md) documents these distinctions.

The later [authorized live inspection](fire-live-account-analysis.md) adds 162
question occurrences with 160 distinct question IDs, E/M/H labels, outcomes,
timing strings and exact topic/example links. All topic/example pairs resolve
to saved lesson content; six of the question IDs occur in the reference-question
CSV. Two IDs repeat across diagnostics. The new source also records one current
360-topic graph-color snapshot and a five-lesson offered menu. These observations
are outside `MA/DATA` and do not supply numeric FIRe state or complete banks.

**Missing or partial data**

| Needed data | Current status | Consequence |
| --- | --- | --- |
| Per-question difficulty ratings | **Missing from the inspected MA question corpus** | No complete mapping from question ID to MA difficulty |
| Topic difficulty/calibration | **Missing** | No populated topic-level difficulty estimates used to determine FIRe learning speed |
| Expected solve times | **Missing** | Observed task XP or an individual's elapsed time cannot supply each item's expected duration |
| Speed-bonus thresholds | **Missing values** | Public client code names the concept, but we have not captured item-specific thresholds |
| Canonical practice-question answer keys | **Missing from the normalized corpus** | Captured questions are not automatically gradable merely because they render |
| Practice-question worked solutions | **Missing from the normalized question records** | Worked lesson examples are available, but do not answer all captured practice items |
| Per-option corrective feedback | **Not available as a populated MA question dataset** | Cannot assume the richer feedback required by our skills was captured from MA |
| Full question banks | **Partial** | Reference lessons expose samples, not every item used in reviews, diagnostics, or tests |
| Encompassing relationships | **No production edge dataset found** | Prerequisite pairs do not tell us which skills receive implicit practice |
| Encompassing weights | **No production values found** | No calibrated fraction of review credit to propagate between topics |
| Non-ancestor encompassing links | **Not captured as data** | Cross-branch implicit practice cannot be reproduced from the current prerequisite graph alone |
| Diagnostic correlation/coverage parameters | **Conceptual descriptions only** | The diagnostic's complete inference weights and coverage policy are not recovered |
| Complete core/supplemental and course-specific optionality metadata | **No authoritative normalized dataset established** | Cannot assume all MA prioritization attributes are present in course maps or topic names |
| Full quiz/test definitions and selection rules | **Not recovered** | Question samples and public resource names do not supply assembled assessments or their blueprints |
| MA question generators/templates | **Not recovered** | Reused questions do not establish a parameterized generation system |
| Learner knowledge profile | **Not captured inside MA** | No exported diagnostic balances, conditional-credit state, or per-topic proficiency estimates |
| Learner retention state | **Not captured** | No actual repetition progress, memory estimates, learning-speed values, or review due times |
| Recommended menus and decision history | **One current five-lesson menu captured; historical decisions missing** | Availability at capture time does not reveal first offer times, rejected candidates, or selection reasons |
| Full item/content/graph version history | **Not captured** | Current snapshots and generation logs are not the platform's historical database |

**Question difficulty: what is missing, and what exists elsewhere**

The captured [Questions.csv][questions] contains only:

```text
topic-id, step-id, question-id, question-type, answer-cardinality
```

The full audit of current normalized lesson JSON found no difficulty fields on any of the 19,646 question placements. Targeted raw-source searches also did not locate a populated difficulty-label dataset. This is a data gap, not just a missing column in the CSV.

There is a small real sample **outside `MA`**, in [mathacademy-xp-observations.json][observations]. It contains difficulty labels for all 308 question occurrences across 34 completed tasks:

| Label | Occurrences |
| --- | ---: |
| Easy | 146 |
| Moderate | 130 |
| Hard | 32 |

However, those reduced question records omit question IDs, topic IDs, and KP IDs. We cannot directly join their difficulty labels onto the captured question catalog. They are useful for studying scoring behavior, not for filling a `questions.difficulty` column at scale.

Keep three quantities separate: an item's categorical difficulty, the topic-level difficulty used in the retention model, and expected solve time. We do not have a populated MA-wide dataset for any of them. Local estimates are possible, but must remain labeled as estimates rather than recovered MA values.

**Encompassing: the prerequisite graph is only part of what FIRe needs**

We have structural prerequisite edges and more focused key-prerequisite links. We do not have a dataset giving advanced-topic/component-topic pairs with their encompassing weights. The book contains descriptions and illustrative values, but those do not constitute the platform's edge database.

The normalized key-prerequisite objects do include a `type` field, but all 9,167 captured entries leave it empty. Its existence is not evidence that encompassing classifications or weights were captured and merely omitted from the CSV.

For example, knowing that topic B requires topic A does not establish that practicing B exercises A's procedure, or how much of A it exercises. That is precisely why an encompassing weight cannot simply be filled with 1 for every prerequisite edge. [FIRe technical chapter][fire].

The existing dependencies and instructional content provide candidate relationships for analysis. A content-grounded process could estimate actual practice coverage and record evidence/confidence. Such a graph would be our reconstruction until supported by direct source observations or calibration.

**Answer keys are another substantial gap**

The current lesson captures preserve prompts, options/input structures, and instructional examples. They do not preserve a canonical correct answer or worked solution for every practice question. The [answer-key document][answers] proposes such a structure; it is not a populated answer database. The files `WORKING-PROGRESS/Answers/answers.py` and its companion Markdown file are both empty.

This does not mean answers are irrecoverable. Many can be solved and verified from the captured problem; some can be recovered from richer source results. But deriving an answer is an additional step, with provenance and validation. The correct option must be associated with answer content or the exact presentation, because option letters can change between captures.

A useful generation/recovery status model is: captured prompt → response structure verified → answer established → independently checked → solution/feedback available → eligible for the intended learning task. Rendering successfully is only an early step.

**Learner data we have elsewhere**

The related [study progress CSV][progress] contains 217 completed activities with task IDs, activity types, displayed timestamps, and XP. The 34-task reduced observation set preserves 308 question outcomes, difficulty labels, answer-visibility states, and elapsed times. The [activity-schema report][activity] documents a separate inspection of 17 completed pages; those samples overlap.

These are not stored in the `MA` content corpus. They also are not a full account export: there is no complete retained question-ID-linked result dataset, hidden knowledge profile, offered-menu history, or review schedule. Observed elapsed time is not expected solve time, and completed status is not proof of mastery.

Files with “progress” in the MA pipeline generally track downloading or generating artifacts. They are production state, not student learning state. SAT/Test-Prep folders similarly contain curriculum material, not a recovered history of timed assessments.

**What can be recovered locally versus what must be acquired or estimated**

| Work | Existing foundation | Additional requirement |
| --- | --- | --- |
| Load a curriculum and display lessons | Topics, course placement, instruction, assets | Import/identity validation and rendering checks |
| Navigate prerequisite paths | Direct and key prerequisite links | Resolve dangling references and preserve edge semantics/provenance |
| Grade captured practice | Prompts and response structure | Verified answer keys and grading rules |
| Offer varied reviews/tests | Some reusable questions and worked examples | More valid items, explicit coverage, novelty tracking, and assessment assembly |
| Select by difficulty/effort | Content plus a small unjoinable historical label sample | Source metadata linked to item IDs or clearly labeled local calibration |
| Apply implicit review credit | Prerequisite candidates plus lesson contents and published FIRe principles | Encompassing edges/weights and a specified propagation policy |
| Maintain ongoing retention | Published conceptual model and partial activity history | Chosen model functions, new learner state, and correctly linked performance evidence |
| Reproduce MA's exact behavior | Public explanations and partial observations | Undisclosed parameters/data remain unavailable; exact reproduction cannot be claimed |

For a working reproduction, the largest gaps are **reliable grading keys, a sufficiently broad question supply, encompassing coverage/weights, and initialized learner state under an explicit retention policy**. Difficulty and timing calibration are additional important gaps. We already have enough content and prerequisite structure to begin a limited, honest implementation while addressing those missing layers.

**Coverage qualifications**

The seven catalog topics without current normalized lesson captures are 555, 2383, 2384, 2385, 2386, 2387, and 2520. Four IDs referenced as global prerequisites are absent from the catalog: 5555, 6050, 6737, and 6747. Those are different coverage problems; neither should be hidden by dropping records.

Generated ECE and older experimental artifacts are also present elsewhere under `MA`. Their proposed difficulties, answers, or dependencies are our generated material, not captured MA metadata. The top-level `ECE-DATA` indexes currently contain two course rows and zero rows in the other eight index files; generated lesson artifacts can live elsewhere. File names and schemas should not be mistaken for populated central tables.

This audit read structured data, relevant source HTML, code, and documentation. It did not execute a capture/generation pipeline, access a live account, OCR every image, or mathematically validate all captured questions. Absence claims concern the inspected datasets and machine-readable fields; they do not claim that MA lacks the information internally.

[courses]: /home/jake/Developer/MA/DATA/Courses.csv
[units]: /home/jake/Developer/MA/DATA/Units.csv
[modules]: /home/jake/Developer/MA/DATA/Modules.csv
[topics]: /home/jake/Developer/MA/DATA/Topics.csv
[catalog]: /home/jake/Developer/MA/DATA/Catalog.csv
[lessons]: /home/jake/Developer/MA/DATA/Lessons
[steps]: /home/jake/Developer/MA/DATA/Lesson-Data/Steps.csv
[questions]: /home/jake/Developer/MA/DATA/Lesson-Data/Questions.csv
[prereqs]: /home/jake/Developer/MA/DATA/Prerequisites.csv
[keyprereqs]: /home/jake/Developer/MA/DATA/Lesson-Data/Key-Prerequisites.csv
[proprietary]: Proprietary.md
[notes]: Proprietary-Notes.md
[answers]: answers.md
[progress]: progress.csv
[observations]: mathacademy-xp-observations.json
[activity]: mathacademy-activity-schema.md
[fire]: <The Math Academy Way/V-TECHNICAL-DEEP-DIVES/29-Technical-Deep-Dive-on-Spaced-Repetition/29-Technical-Deep-Dive-on-Spaced-Repetition.md>
