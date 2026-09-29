# Reference collection

Project reports and schema design notes live here. External documents were copied
on September 26, 2026; their originals remain in place. Links to other documents
in this collection use the local copies. Links to source code and uncopied data
still lead to their original locations.

## Project reports

- [FIRe reconstruction](fire-reconstruction.md): executable algorithm, recovered rules, and chosen policies.
- [FIRe source evidence](fire-source-evidence.md): primary sources, diagram checks, and unresolved details.
- [FIRe history analysis](fire-history-analysis.md): observation audit and sensitivity replays.
- [Live account findings](fire-live-account-analysis.md): recovered question identities, diagnostic results, targeted remediation, and repeated-item evidence; [captured observations](fire-live-observations-2026-09-26.json).
- [FIRe data model](fire-data-model.md): required state, events, weights, EDN schemas, and acquisition plan.

- [Math Academy's inflexibility](ma_inflexibility.md): motivation and requirements.
- [Engine analysis](mathacademy_engine_analysis.md): published mechanisms, observations, and inference.
- [Schema and architecture](mathacademy_schema_architecture.md): source evidence and earlier architecture proposals.
- [Data inventory](ma_data_inventory.md): available data and remaining gaps.
- [Study skills review](skills_v1.md): the homework/exam-driven authoring workflow.
- [Skills versus ECE pipeline](skills_vs_ece_pipeline.md): comparison with curriculum-first generation.

## Current schema design

- [Scheduling proposal](scheduling-proposal.md): recommendations, required work, assessment assembly, and fresh-question supply.
- [XP proposal](xp-proposal.md): concrete scoring rules, evidence, and deliberate local choices.
- [Answer grading proposal](answer-grading-proposal.md): selection and mathematical verification, plus Python generator storage.
- [How the learning engine plugs into the schema](fire-schema-integration.md): one-page proposal for Rust logic, ordinary activity records, and learner progress.
- [Instructional content model](instructional-content-model.md): lessons, steps, knowledge points, examples, and tutorials.
- [Answer model](answer-model.md): questions, answer fields, and answers.
- [EDN schema index](../schema/README.md): grouped definitions for curriculum data, instructional content, learner state/history, and remaining FIRe prototypes.
- [EDB schema reference](edb-schema-reference.md): supported database schema features.

The current EDN and its companion notes supersede conflicting design proposals
in the older reports; those reports remain useful as evidence and rationale.

## Research and pedagogy

- [Proprietary mechanism excerpts](Proprietary.md) and [interpretive notes](Proprietary-Notes.md).
- [Active learning loop](Active-Learning-Loop.md) and [lesson progression](Lesson-Progression.md).
- [Earlier progression tags](lesson_progression_tags.md).
- [Explanation example](explanation-format.md), [earlier answer-key proposal](answers.md), and [prerequisite pipeline proposal](prerequisite-goal.md).
- [The Math Academy Way](<The Math Academy Way/>): the existing local book collection.

## Activity evidence

- [Activity schema notes](mathacademy-activity-schema.md) and [JSON Schema](mathacademy-activity.schema.json).
- [XP analysis](mathacademy-xp-analysis.md), [observations](mathacademy-xp-observations.json), [analyzer](analyze-mathacademy-xp.py), and [saved results](mathacademy-xp-model-results.json).
- [Progress history](progress.csv) and [progress notes](progress-notes.md).

The progress CSV has 217 activities; the saved XP analysis uses a 214-activity
snapshot, and the progress notes describe 212. Saved observations and results
retain their original provenance strings. The analyzer's default inputs remain
beside it in this folder.

## Pipeline references

- [Math Academy ingestion pipeline](mathacademy-pipeline.md).
- [ECE lesson generation pipeline](ece-build-lessons.md).

## External originals

| Local copy | Original |
| --- | --- |
| [Proprietary.md](Proprietary.md) | [/home/jake/Developer/MA/WORKING-PROGRESS/Proprietary.md](/home/jake/Developer/MA/WORKING-PROGRESS/Proprietary.md) |
| [Proprietary-Notes.md](Proprietary-Notes.md) | [/home/jake/Developer/MA/WORKING-PROGRESS/Proprietary-Notes.md](/home/jake/Developer/MA/WORKING-PROGRESS/Proprietary-Notes.md) |
| [explanation-format.md](explanation-format.md) | [/home/jake/Developer/MA/WORKING-PROGRESS/explanation-format.md](/home/jake/Developer/MA/WORKING-PROGRESS/explanation-format.md) |
| [answers.md](answers.md) | [/home/jake/Developer/MA/WORKING-PROGRESS/answers.md](/home/jake/Developer/MA/WORKING-PROGRESS/answers.md) |
| [prerequisite-goal.md](prerequisite-goal.md) | [/home/jake/Developer/MA/WORKING-PROGRESS/prerequisite-goal.md](/home/jake/Developer/MA/WORKING-PROGRESS/prerequisite-goal.md) |
| [mathacademy-activity-schema.md](mathacademy-activity-schema.md) | [/home/jake/Developer/study/vault/252/mathacademy-activity-schema.md](/home/jake/Developer/study/vault/252/mathacademy-activity-schema.md) |
| [mathacademy-activity.schema.json](mathacademy-activity.schema.json) | [/home/jake/Developer/study/vault/252/mathacademy-activity.schema.json](/home/jake/Developer/study/vault/252/mathacademy-activity.schema.json) |
| [mathacademy-xp-analysis.md](mathacademy-xp-analysis.md) | [/home/jake/Developer/study/vault/252/mathacademy-xp-analysis.md](/home/jake/Developer/study/vault/252/mathacademy-xp-analysis.md) |
| [mathacademy-xp-observations.json](mathacademy-xp-observations.json) | [/home/jake/Developer/study/vault/252/mathacademy-xp-observations.json](/home/jake/Developer/study/vault/252/mathacademy-xp-observations.json) |
| [analyze-mathacademy-xp.py](analyze-mathacademy-xp.py) | [/home/jake/Developer/study/vault/252/analyze-mathacademy-xp.py](/home/jake/Developer/study/vault/252/analyze-mathacademy-xp.py) |
| [mathacademy-xp-model-results.json](mathacademy-xp-model-results.json) | [/home/jake/Developer/study/vault/252/mathacademy-xp-model-results.json](/home/jake/Developer/study/vault/252/mathacademy-xp-model-results.json) |
| [progress.csv](progress.csv) | [/home/jake/Developer/study/vault/252/progress.csv](/home/jake/Developer/study/vault/252/progress.csv) |
| [progress-notes.md](progress-notes.md) | [/home/jake/Developer/study/vault/252/progress-notes.md](/home/jake/Developer/study/vault/252/progress-notes.md) |
| [lesson_progression_tags.md](lesson_progression_tags.md) | [/home/jake/Developer/MA/Z/3-First-Attempt/lesson_progression_tags.md](/home/jake/Developer/MA/Z/3-First-Attempt/lesson_progression_tags.md) |
| [edb-schema-reference.md](edb-schema-reference.md) | [/home/jake/Developer/EDB/docs/03_schema/02_schema_reference.md](/home/jake/Developer/EDB/docs/03_schema/02_schema_reference.md) |
| [mathacademy-pipeline.md](mathacademy-pipeline.md) | [/home/jake/Developer/MA/PIPELINE/Math-Academy/README.md](/home/jake/Developer/MA/PIPELINE/Math-Academy/README.md) |
| [ece-build-lessons.md](ece-build-lessons.md) | [/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/build-lessons.md](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/build-lessons.md) |
| [Active-Learning-Loop.md](Active-Learning-Loop.md) (already present) | [/home/jake/Developer/MA/Z/3-First-Attempt/Active-Learning-Loop.md](/home/jake/Developer/MA/Z/3-First-Attempt/Active-Learning-Loop.md) |
