# 2. Inventory

Before preparing an activity, check these rolling minimums for each **supported** difficulty. An unobserved band needs classification; absence alone does not prove it can or cannot be generated.

| Activity | Easy | Moderate | Hard | Scope |
|---|---:|---:|---:|---|
| Lesson | 5 | 5 | 5 | Each knowledge point used by the lesson |
| Review | 5 | 5 | 5 | The topic, pooled across its knowledge points |
| Assessment | 5 | 5 | 5 | Each selected topic, pooled across its knowledge points |

Apply the same minimums to retakes of each activity type. An assessment retake must also have a fresh alternative at each supported difficulty level for every original knowledge point being retested. Preserve those alternatives while preparing the preceding remedial reviews.

Use the most efficient practices supported by [$edb](../../skills/edb/SKILL.md): reuse the project's integration, batch related reads against one database value, use Datalog for selection and joins, and Pull only the details needed for validation.

1. Identify the activity's knowledge points or topics, including the original knowledge points for an assessment retake.
2. Count distinct available questions by difficulty and scope using existing knowledge-point membership and difficulty facts; exhausted supported bands count as zero. Count only validated, gradable practice questions that the learner has never been shown and that are not reserved for another activity. Exclude canonical examples and unrated questions.
3. Read `:knowledge-point/question-generator` and its registered `:question-generator/script`. Batch generator lookups with the question-inventory reads wherever possible.
4. For each shortage, use the existing generator to produce the missing questions. If the knowledge point has no generator, launch the generator creator, beginning with [Classify](3-classify.md). Once its generator is ready, generate the missing questions. Validate every generated question and keep it associated with its knowledge point; topic inventory combines those pools without duplicating questions.
5. Recheck the inventory against the current database basis before preparing the activity. If a shortage remains, keep preparation pending until it is filled.

These are rolling minimums. Replenish them before each new activity; previously shown questions do not return to available inventory. The reserves support weighted selection, rather than specifying how many questions of each difficulty an activity must serve.

A verified generator package may record an unsupported band or a finite variant limit. Keep the exception and its evidence visible; do not repeatedly demand impossible questions or claim that a shortage is filled. New source evidence reopens classification. Legacy unrated banks need classification before they contribute to difficulty-weighted assessments.

The native `/api/inventory` read batches selection and counts at one captured EDB basis. Durable jobs in `.local/learning/inventory/<database>/<learner>/` merge overlapping triggers, rank exhausted bands first, then required work, queued topics, targets and later opportunities. The server checks committed changes and time-based eligibility, and rechecks preparation after verified replenishment. Use the most efficient supported $edb practice when extending it; reuse the native reader's incremental transaction-log projection rather than adding independent per-question queries.
