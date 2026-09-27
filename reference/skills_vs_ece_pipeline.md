# Study Skills Compared with the ECE Curriculum Pipeline

Review date: September 26, 2026

## Scope

This report compares the nine study skills reviewed in [skills_v1.md](skills_v1.md) with the pipeline coordinated by:

`/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/electrical-and-computer-engineering.py`

The original study skills were reviewed at `/home/jake/Developer/study/util/skills`. The comparison continues to exclude `create-course-map` and `gather-course-information`. ECE's own upstream course-map stages are discussed because they are part of the requested pipeline.

Evidence includes orchestration code, stage implementations, prompts, schemas, validators, compilation behavior, and a read-only quiz compatibility check against one compiled ECE lesson. This was not a complete pipeline execution or a comprehensive mathematical audit of generated content.

## Main finding

Both systems use the same instructional pattern: identify one concrete core move, introduce it directly, demonstrate a simplest case, attach closely matched practice, and deepen the same move through controlled variations.

Their organizing goals differ:

- **Study skills:** build instructional support around real assignment problems, reusing equivalent Math Academy lessons where possible and generating focused fallbacks where necessary.
- **ECE pipeline:** build a curriculum from a course structure, with persistent intermediate artifacts for instructional planning, content, questions, figures, and compiled lesson packages.

ECE separates much of the reasoning inside `core-move-lesson` into individually persisted and validated stages. It has more developed build and recovery machinery. The study skills have stronger explicit requirements for source fidelity, response-specific corrective feedback, post-generation pedagogical refinement, and final prose review.

## Workflow comparison

### Study skills

```text
Create assignment skeleton
  → Add source questions and screenshots
  → Clean and normalize the assessment material
  → Examine each problem for an equivalent MA lesson
      → Match: copy lesson, source assets, and direct prerequisites
      → No match: generate → refine → edit prose → validate
  → Verify assignment coverage
```

The preparation sequence is inferred from skill input/output contracts. The matching and fallback sequence is explicitly prescribed by `setup-lessons`.

### ECE pipeline

```text
0. Ingest
   Register courses and source documents
   Scaffold course directories and indices

1. Build Course Data
   1. Prepare shared teaching-design context
   2. Build course maps                  [currently a placeholder]
   3. Extract course hierarchy into graph tables
   4. Identify one core move per fixed topic
   5. Identify the ordered teaching steps

2. Build Lessons
   1. Outline instructional, question, and image requirements
   2. Generate tutorials and worked examples
   3. Generate practice questions
   4. Generate instructional figures
   5. Compile lesson packages
```

The ECE hierarchy is:

```text
Course → Unit → Module → Topic → Step → Questions
```

A topic corresponds to a complete lesson; a step corresponds to a section within that lesson. Existing JSON fields retain the older terminology: `lesson_*` refers to topics and `section_*` refers to steps.

Topic-set preparation is a separate upstream dependency. A producer helper exists, but the stage runner does not invoke it. Its default output directory also differs from the topic-identification runner's default input directory.

Sources: [top-level runner](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/electrical-and-computer-engineering.py:104), [course-data runner](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/1-Build-Course-Data/build-course-data.py:80), and [lesson-build documentation](ece-build-lessons.md).

## Skill-to-stage mapping

| Study skill | Closest ECE counterpart | Difference |
|---|---|---|
| `skeleton` | Ingest/scaffold | The skill creates an assignment workspace; ECE creates course infrastructure and indexes source documents. |
| `lesson-cleanup` | No direct equivalent | ECE does not provide the same supplied-question cleanup, screenshot deduplication, precision review, and source-fidelity workflow. |
| `setup-lessons` | Overall orchestration and parts of compilation | The skill coordinates assignment coverage and study-vault integration; ECE coordinates curriculum production. |
| `match-ma-lesson` | No direct equivalent | ECE has no branch that verifies and copies an equivalent existing MA lesson. |
| `lesson-pipeline` | `build-lessons.py` | Both coordinate generation; ECE persists intermediate artifacts and manages finer-grained recovery. |
| `core-move-lesson` | Topic identification, step identification, step outline, tutorial/example generation, and question generation | One skill's instructional reasoning is distributed across several ECE stages. |
| `core-move-refiner` | Shared setup and exemplar analysis, partially | ECE studies MA pedagogy before generation; the skill revisits MA lessons after drafting and edits the result. |
| `llm-deodorizer` | No distinct stage | ECE checks structure and formatting, but has no equivalent final semantic prose audit. |
| `quiz-block-factory` | Question schemas, validators, and compiler | ECE has its own assessment representation and rendering code, with a different authoring contract. |

## Shared teaching model

Both systems define a core move as an operational action that the learner should master. They discourage broad descriptions such as “understand the topic.” Both seek a progression that introduces one meaningful complication at a time while retaining the same underlying skill.

ECE makes the instructional decomposition explicit:

1. Topic identification assigns a core move to each already selected topic.
2. Step identification chooses the ordered tutorial/example progression.
3. Step outline specifies learning goals, worked examples, solution steps, practice models, distractors, and image requirements.
4. Content generation fills one tutorial or worked-example step at a time.
5. Question generation produces practice that closely mirrors the corresponding example.

The study generation skill performs similar reasoning within a worker responsible for a single problem lesson, then writes the final Markdown directly.

The source of scope differs. For the skills, the assignment problem supplies the givens, required action, answer form, and constraints. For ECE, the course map supplies fixed topic identities and sequence, with neighboring topics informing the boundaries of each lesson.

Once ECE topic and step identities are established, later stages must preserve them. Code validates these identities and counts. This supports consistency, but an instructional scope error introduced upstream requires correction in that earlier artifact; later stages are instructed to retain the boundary.

Sources: [topic-identification prompt](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/1-Build-Course-Data/4-Topic-Identification/topic-identification.md:15), [step-identification guidance](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/1-Build-Course-Data/5-Step-Identification/step-identification.md:80), and [step-outline prompt](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/1-Step-Outline/step-outline.md).

## How each system uses Math Academy

The study skills use MA in two ways:

- **Content reuse:** inspect actual lesson questions and examples, verify task equivalence, and copy suitable lessons with direct prerequisites.
- **Pedagogical refinement:** compare a generated lesson with several MA lessons and apply useful teaching patterns without copying proprietary wording or question content.

ECE primarily uses MA as a teaching-design reference. Its setup stage studies exemplar lessons 14, 2754, and 3003, produces reviewed setup artifacts, and saves a reusable session. Later stages inherit or reference this preparation. The lesson template is explicitly derived from the MA “Imaginary Numbers” lesson.

This gives ECE shared pedagogical context before generation. It does not replace the study refiner's distinct after-drafting comparison and revision pass.

Sources: [setup exemplar sequence](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/1-Build-Course-Data/1-Setup/setup.py:119), [setup session contract](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/1-Build-Course-Data/1-Setup/setup.py:588), and [lesson template](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/1-Build-Course-Data/5-Step-Identification/0-Source/1-Templates/Lesson-Template.md).

## Build machinery and recovery

ECE persists structured artifacts between stages and checks them before downstream use. Its implementation includes:

- Stage and target state with success/failure records.
- Granular topic, step, and question artifacts.
- Input hashes, prompt signatures, model settings, and cache metadata.
- Worker retries and repair flows.
- Filtered generation with merging into full canonical artifacts.
- Separate partial-output support.
- Build-progress tables derived from stage state.
- Compiled packages that retain generation provenance and image source code.

The study pipeline instead assigns one worker to each missing problem lesson and relies on the worker to complete generation, refinement, prose review, and final validation. Existing nonempty `Problem-N.md` files count as coverage and are skipped by default.

ECE's artifact validation is stronger than a file-presence check, but neither system's deterministic checks establish mathematical correctness or instructional quality. Identity, count, schema, and reference checks can succeed while the explanation or core move is pedagogically weak.

The ECE cache policy is not uniform. Tutorial and question stages contain explicit stale-metadata handling, while the outline stage reuses structurally valid artifacts on metadata mismatch even without the stale-reuse flag. The documentation's broad claim of strict cache matching therefore needs qualification.

Sources: [lesson-build contract](ece-build-lessons.md), [outline reuse](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/1-Step-Outline/step-outline.py:1717), and [question reuse](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/3-Question-Generation/question-generation.py:2740).

## Assessment and feedback contracts

Both systems ultimately produce Obsidian lesson Markdown with practice near the corresponding explanation. Their quiz authoring requirements differ.

| Property | Study skills | ECE pipeline |
|---|---|---|
| Shared authority | Quiz Block Factory | ECE question schemas, validators, and compiler |
| Supported output types | Radio, checkbox, select, multi-select, noodle, free, blank | Compiler handles radio, checkbox, blank, and fallback free |
| Typical generated practice | Radio by default; source response shape matters in cleanup | Planning strongly favors single-answer, five-choice questions |
| Feedback | Corrective feedback for every selectable option | General answer explanation attached to correct choices |
| Distractor diagnosis | Explicit authoring requirement | No per-distractor feedback field in the reviewed choice schema |
| Radio shuffling | Required by factory policy, with an unresolved cleanup-policy conflict documented in `skills_v1.md` | Compiler emits no shuffle setting |
| Final prose review | Refiner followed by deodorizer in the generation pipeline | No distinct equivalent final stage |

The ECE question generator ordinarily creates two questions per example. It validates answer cardinality, choice labels, question counts, and consistency between correct labels and correctness flags. These are structural checks; they do not prove that the marked answer is mathematically correct.

### Compatibility check against a compiled lesson

The original study validator was run read-only against this compiled ECE lesson:

[Pole Locations in the s-Plane](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/5-Compile/1-Outputs/Continuous-Time-Signal-Processing/EE01-M13-02/EE01-M13-02-L07/EE01-M13-02-L07.md)

Validator options:

```text
--strict-ids --require-feedback --lint-feedback --require-radio-shuffle
```

| Result | Count |
|---|---:|
| Quiz blocks inspected | 10 |
| Missing distractor feedback fields | 40 |
| Missing radio shuffle settings | 10 |
| Total reported issues | 50 |

The validator exited with status 1. These failures demonstrate incompatibility with the study skills' stricter authoring contract. They do not by themselves establish that the quizzes fail to render in Obsidian. This was one representative compatibility check, not a survey of every compiled lesson.

Sources: [question schema](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/3-Question-Generation/0-Source/question.schema.json:160), [question validation](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/3-Question-Generation/question-generation.py:2342), and [quiz compilation](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/5-Compile/compile.py:929).

## Images and visual instruction

ECE has a substantial figure-production stage. Earlier stages identify image slots for tutorial support, worked examples, question prompts, and answer choices. The image stage classifies support against visual patterns, generates Matplotlib code using shared style guidance, renders figures, and records unsupported requests in a backlog.

This complements the cleanup skill, which focuses on preserving and organizing supplied source images. Cleanup addresses ownership, semantic naming, broken references, and duplicate detection; it is not a comparable curriculum-wide figure generator.

ECE's image checks cover metadata, schemas, requested slots, Python syntax and code restrictions, successful execution, and nonempty output files. The reviewed pipeline has no distinct post-render visual or mathematical certification stage. Successful rendering is therefore evidence of an operational artifact, not proof that a graph or diagram teaches the intended concept correctly.

Sources: [topic image-generation prompt](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/4-Image-Generation/0-Source/Lesson-Matplotlib-Images.md:39), [image validation](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/4-Image-Generation/image-generation.py:1657), and [render checks](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/4-Image-Generation/image-generation.py:1746).

## Outputs, registration, and progress

ECE compilation produces packages under:

```text
5-Compile/1-Outputs/<course>/<group>/<lesson>/
├── <lesson>.md
└── Source/
    ├── <lesson>.json
    ├── Images/
    ├── Image-Code/
    ├── Image-Context/
    └── Upstream source artifacts as applicable
```

Packages preserve content, provenance, source hashes, compile options, image code, and supporting context. ECE's progress tables describe production status across build stages. Missing required images normally defer a lesson's compilation, and the progress logic accounts for these incomplete packages.

The study setup skill has a different integration target: assignment links, course topic and prerequisite indices, Home/TOC navigation, and the learner's Obsidian progress plugin. It registers copied MA content in those systems.

ECE compilation does not perform that study-vault registration. The study generation branch also lacks a complete registration handoff for new fallback lessons, as documented in `skills_v1.md`.

Production completion and learner progress should remain distinct concepts. A common registration step could make either copied or generated lesson packages available to the learner without confusing build state with study completion.

Sources: [package provenance](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/5-Compile/compile.py:1261), [package writing](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/5-Compile/compile.py:1570), and [build-progress table rendering](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/0-Source/progress-table.py:919).

## Implementation caveats

1. **Map generation is a placeholder.** `1-Build-Course-Data/2-Map/map.py` contains only a comment. Existing course maps are a practical prerequisite for the downstream workflow.
2. **Topic-set preparation is not connected to the runner.** A separate helper produces fixed topic sets, but the ECE runner does not invoke it. Producer and consumer defaults also use different directories.
3. **Strict cache behavior is not uniform.** Outline reuse accepts structurally valid artifacts when cache metadata differs, contrary to the documentation's blanket strict-cache description.
4. **The outer launcher exposes fewer options than the lesson runner.** Its lesson-stage allowlist omits `--reuse-stale`, `--cache-report`, `--subset-output`, and `--no-runners`. Those options are silently filtered out rather than forwarded through the top-level launcher.
5. **Output validation does not enforce the study feedback contract.** ECE compilation lacks per-distractor feedback and radio shuffle settings, confirmed by the representative validator run.
6. **Compiled packages are not registered in the study environment.** Build completion alone does not supply assignment coverage links, study-vault topic registration, or learner progress integration.

Sources: [map stub](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/1-Build-Course-Data/2-Map/map.py:1), [topic-set producer default](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/1-Build-Course-Data/4-Topic-Identification/0-Source/course-map-topics.py:40), [topic-set consumer default](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/1-Build-Course-Data/4-Topic-Identification/topic-identification.py:90), [outer launcher flag allowlist](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/electrical-and-computer-engineering.py:63), and [argument filtering](/home/jake/Developer/MA/PIPELINE/0-lib/stage_runner.py:86).

## Implications for Course Academy

The following are design recommendations from the comparison, not implemented changes:

1. **Use ECE's persistent generation stages and recovery mechanisms as the build foundation.** Keep instructional decisions inspectable in intermediate artifacts and preserve provenance through compilation.
2. **Retain the assignment-based entry point and verified reuse branch.** Course-wide generation and assignment-driven coverage can feed the same lesson library, while exact task matching remains a separate decision.
3. **Adopt one assessment authoring contract.** Carry response-specific feedback through the structured question schema and compiler, and reconcile source-fidelity, type-selection, and shuffle rules before enforcing them consistently.
4. **Add explicit pedagogical and editorial review after generation.** Preserve the study refiner's comparison-based improvement and the deodorizer's semantic audit within the artifact workflow so compiled output reflects the reviewed content.
5. **Register copied and generated lessons through a common handoff.** Persist identities, problem coverage, prerequisites, navigation, and learner-progress integration independently of production state.
6. **Repair the upstream and launcher gaps before treating the top-level script as a complete unattended workflow.** Connect map/topic-set preparation, align supported flags, and make cache behavior match its stated policy.

## Verification boundary

The comparison inspected implementation and documentation and performed the single compiled-lesson compatibility check described above. No generation pipeline was executed, and no source skills, pipeline files, or compiled lessons were modified. The report makes no claim that either system's generated curriculum has been comprehensively checked for mathematical accuracy or learning effectiveness.
