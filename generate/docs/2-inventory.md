# 2. Inventory

For each existing generator, aim to maintain five fresh questions in every difficulty per KP. An unobserved band needs classification and review; absence alone does not prove it can or cannot be generated. Record unsupported bands and finite limits explicitly.

| Background reserve | Easy | Moderate | Hard | Scope |
|---|---:|---:|---:|---|
| Generator replenishment | 5 | 5 | 5 | Each knowledge point |

Activity admission has smaller total-stock requirements:

| Activity | Required available questions | Scope |
|---|---|---|
| Lesson | 5 usable questions in total, across difficulties | Every lesson KP |
| Review | 5 usable questions in total, across difficulties | Topic, pooled across KPs |
| Assessment | 1 valid rated question | Each eligible topic, pooled across KPs |

An ordinary assessment topic must also be currently learned and at least 48 hours past its first successful lesson. No prior review is required. A missing band does not exclude an otherwise usable topic. Assembly uses one question per topic and the maximum jointly feasible band coverage within its 15-minute estimated budget.

An assessment retake needs a fresh usable rated alternative for every original KP, with a feasible route covering all original topics within the budget. It does not require five questions per band or an alternative at every difficulty. Preserve fresh alternatives while preparing the preceding remedial reviews.

**Lesson admission:** each skill needs at least five fresh, gradable practice
questions **in total**, across difficulties. This applies to selected lessons,
queued lessons, and required relearning. A shortage in one difficulty band
triggers background replenishment without blocking an otherwise usable lesson.
Already started or paused lessons retain their existing resume/deferral behavior.

Use the most efficient practices supported by [$edb](../../skills/edb/SKILL.md): reuse the project's integration, batch related reads against one database value, use Datalog for selection and joins, and Pull only the details needed for validation.

1. Identify the activity's knowledge points or topics, including the original knowledge points for an assessment retake.
2. Count distinct available questions by difficulty and scope using existing knowledge-point membership and difficulty facts; exhausted supported bands count as zero. Count only validated, gradable practice questions that the learner has never been shown and that are not reserved for another activity. Exclude canonical examples, retired questions, and structurally contained multistep parts. Audit generated descendants by retained source references: copies lose that containment and can otherwise inflate usable inventory. Unrated questions can contribute to lesson/review total stock but not rated-band reserves or assessments.
3. Read `:knowledge-point/question-generator` and its registered `:question-generator/script`. Batch generator lookups with the question-inventory reads wherever possible.
4. For each shortage, use the existing generator to produce the missing questions. If the knowledge point has no generator, launch the generator creator, beginning with [Classify](3-classify.md). Once its generator is ready, generate the missing questions. Validate every generated question and keep it associated with its knowledge point; topic inventory combines those pools without duplicating questions.
5. Recheck inventory against the current database basis. Apply the activity admission totals above, and continue filling per-band reserves in the background. Lesson, review, and assessment preparation do not wait for a full 5/5/5 reserve when their admission and assembly requirements are already satisfied.

Previously shown questions do not return to available inventory. The per-band reserves support weighted selection rather than specifying how many questions of each difficulty an activity must serve.

A verified generator package may record an unsupported band or a finite variant limit. Keep the exception and its evidence visible; do not repeatedly demand impossible questions or claim that a shortage is filled. New source evidence reopens classification. Legacy unrated banks need classification before they contribute to difficulty-weighted assessments.

The native `/api/inventory` read batches selection and counts at one captured EDB basis. The live worker uses the [finder's ordering rules](../scripts/README.md): actual active/requested/remedial shortages, other activity shortages, distinct-topic assessment variety, then advance preparation and routine replenishment. Self-directed new lessons use Study's bounded scope and band filter; roots and depth-two prerequisites share one relevance tier, and earlier deficient lessons come first. The five-per-band reserve does not gate this work; the direct-selection completion gate remains specific to course mode. Durable jobs in `.local/learning/inventory/<database>/<learner>/` deduplicate builds per KP and refills per KP/band. The server checks committed changes and time-based eligibility, and rechecks preparation after verified replenishment. Reuse native batched reads rather than adding independent per-question queries.
