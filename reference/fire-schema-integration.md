# How the learning engine plugs into our schema

The algorithm belongs in **Rust application code**. EDB stores the content, relationships, learner activity, and progress that the algorithm reads and updates. EDN defines those attributes and their constraints; it does not implement the algorithm. Formulas, grading rules, review scheduling, test selection, time limits, and XP calculations belong in code and configuration.

The standalone [FIRe schemas](../schema-v2/fire/) grew around reproducing and inspecting calculations. That made policy records, calibration sets, and application receipts too prominent in the proposed product model. We need the underlying learning data, but those research-oriented records do not all need to become permanent application entities.

Our existing structure already provides the content:

```text
lesson → topic
lesson → ordered steps → knowledge point or tutorial
knowledge point → worked example + question bank
question → answer fields → answers
```

The engine selects questions from those banks. A learner's submitted answer is separate from the stored correct answer. The main additions are records describing someone using that content:

| Where the data belongs | What the engine needs |
| --- | --- |
| **Existing content** | Topic and question identities, prerequisites, knowledge points, answers, and difficulty. `question/difficulty` already holds E/M/H; `topic/difficulty` is a separate aggregate accuracy-based measure whose scale we must define. Learner ability belongs elsewhere. |
| **Encompassing relationship** | A topic owns encompassing records through `topic/encompasses`. Each contains a component topic, fractional weight, and optional rationale; the parent supplies the source. Ordinary prerequisite refs do not tell FIRe how much practice transfers. |
| **Activity** | Learner, activity kind (lesson, review, assessment, diagnostic), content refs, start/completion times, status, result, awarded XP, and whether selection was automatic or student-directed. A delivered activity can also record its assigned time budget. |
| **Question attempt** | Activity and question refs, assessed knowledge point/topic, presentation order, submitted field values, correctness, timestamps, active solving duration, and assistance used. Each occurrence has its own identity, including repeat presentations of the same question. |
| **Learner and learner-topic progress** | Global and topic-specific accuracy evidence; for each learner/topic pair, learned status, fractional repetitions, memory estimate and its timestamp, retention interval, and last direct practice. The prototype's learner/state attributes already cover these concepts. Progress is shared across courses containing the same topic. |

Elapsed solving time belongs on the **question attempt**, not on the reusable question or lesson. It differs from elapsed calendar time since earlier practice: the current FIRe calculation uses the latter for memory decay. Capturing solving duration is useful, but its effect on grading or scheduling needs an explicit rule. XP is a separate reward calculation.

At runtime, Rust grades submissions, applies the activity's completion rules, and groups the evidence by topic. Several questions can support one repetition; an assessment can produce evidence for several topics. FIRe then updates direct and implicit repetition credit, memory, and accuracy. A database transaction saves the completed result, affected progress, and XP together, with safeguards against crediting a retried completion twice. The scheduler reads that state to choose subsequent reviews, tests, remediation, or lessons. Due times and learning speed can be computed from stored state rather than maintained as additional authoritative values.

A student-selected lesson follows this same path. Selection changes how the activity begins; completion still feeds the ordinary retention, review, assessment, and XP mechanisms.

We can therefore integrate FIRe through normal activity records and progress attributes without requiring a second event log or a full calculation receipt for every action. Reusable review/test definitions are needed only where there is reusable authored structure; delivered questions and results belong to activities. Detailed traces can remain optional debugging output.

**Current status:** the runnable implementation is a [Python reference engine](../engine/fire/core.py). The Rust implementation, EDB persistence integration, and general activity/question-attempt schemas remain to be built. This page proposes the integration; it does not change any EDN schemas.
