This review distinguishes MA's captured content types from our proposed EDB entities. It rechecked all 2,964 normalized lesson captures under `/home/jake/Developer/MA/DATA/Lessons/*/Source/*.json`, the HTML for topic 14, the capture normalizer, the ECE generation schemas, and the current v2 EDN. The agreed tutorial/example separation is now implemented in the v2 EDN. Lesson placement and teaching sequence remain future work.

MA's reference captures contain two instructional step types and a separate question item type:

| Captured category | Placements | Structure |
| --- | ---: | --- |
| Tutorial | 6,016 | Expository content and optional graphics |
| Example | 9,636 | A worked-example problem and explanation |
| Question | 19,646 | A separate practice item with an interaction format |

These are placement counts, not unique content counts or an inventory of MA's complete production system. There were no other item categories in this normalized snapshot. Tutorial/example is copied from the source HTML's `steptype` attribute. Our normalizer distinguishes `item_type=step` from `item_type=question`; it classifies example sections using the source `exampleQuestion` and `exampleExplanation` classes. See [normalizer](/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py:1087).

Every example had exactly one `example_question` section and one `example_explanation` section, separated by a content section containing the explanation heading. Tutorials instead contained prose/math content sections and, sometimes, graphic sections. Images appeared in 2,230 tutorial placements and 2,789 example placements. Neither instructional category had captured free-entry or dropdown controls. This describes the reference captures, not every possible interactive MA client behavior.

A concrete sequence appears in [topic 14](/home/jake/Developer/MA/DATA/Lessons/14/Source/14.json):

1. Tutorial 2787, “Introduction,” introduces imaginary numbers and explains the square root of a negative number. The source gives it step placement 14286.
2. Example 4031, “Finding the Square Root of a Negative Number,” asks the reader to evaluate the square root of −36 and demonstrates the solution 6i. Its step placement is 14287.
3. Practice questions 58 and 57 ask different problems involving the square roots of −49 and −25, with selectable options.

The source explicitly marks the [tutorial](/home/jake/Developer/MA/DATA/Lessons/14/Source/14.html:1279) and [example](/home/jake/Developer/MA/DATA/Lessons/14/Source/14.html:1512). The distinction is structural and pedagogical, not merely a title convention.

For example, [topic 6295](/home/jake/Developer/MA/DATA/Lessons/6295/Source/6295.json) contains a tutorial titled “A Concrete Example.” It demonstrates parametrizing a system as part of the exposition, but MA still classifies it as a tutorial. [Topic 1980](/home/jake/Developer/MA/DATA/Lessons/1980/Source/1980.json) includes an introductory tutorial, a conceptual note, tutorials interleaved with worked examples/practice, and two concluding derivations. A tutorial therefore need not be an introduction or a problem/explanation pair.

Only 1,263 lessons have exactly one tutorial. The other 1,701 have between two and ten. Attaching one tutorial to every KP, or allowing only a single introductory tutorial per topic, would impose a structure the captures do not support.

The ECE generation pipeline already follows this distinction: its [step schema](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/1-Build-Course-Data/5-Step-Identification/0-Source/step-entry.schema.json) permits tutorial/example; its [tutorial schema](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/2-Tutorial-Example-Generation/0-Source/tutorial.schema.json) stores content blocks, while its [example schema](/home/jake/Developer/MA/PIPELINE/Electrical-and-Computer-Engineering/2-Build-Lessons/2-Tutorial-Example-Generation/0-Source/example.schema.json) stores an example prompt and explanation blocks. Those block types are paragraph, display-math, and image. They are rendering/content blocks, not additional instructional step types.

MA's description of a knowledge point associates a worked example with similar practice questions. The former KP attributes `example-question` and `example-explanation` reflected that worked-example content; their replacement is the example entity. Calling their replacement a tutorial would merge two source categories. See the [local MA excerpts](/home/jake/Developer/MA/WORKING-PROGRESS/Proprietary.md:152). An earlier [identity analysis](/home/jake/Developer/Course_Academy/mathacademy_schema_architecture.md:79) also documents an activity KP link whose fragment matches example content 2993 rather than its step placement ID. That verified case supports the association; it does not establish a universal internal schema.

The implemented entities and relationships are:

| Entity | Proposed content/refs | Reason |
| --- | --- | --- |
| [Tutorial](tutorial.edn) | id, title, content | Exposition in Markdown with mathematics and images; no required answer |
| [Example](06-example.edn) | id, problem, explanation | The demonstrated problem and worked solution |
| [Knowledge point](05-knowledge-point.edn) | id, title, key-prerequisites refs, example ref, questions refs, question-generator ref | The skill being practiced, its key prerequisite topics, and the content teaching/assessing it |
| [Question](07-question.edn) | Problem, type, fields, explanation, metadata | An item prepared for the learner to answer |
| Answer field → answer | [Answer field](08-answer-field.edn) and [answer](09-answer.edn) | Expected values and selection options for each question field |

`example/problem` is textual problem content, not a mandatory ref to a question entity. A title can stay on the KP in this initial design, matching how it currently names the demonstrated skill. Separating the example content makes its problem and explanation reviewable as a unit without duplicating the entire question hierarchy.

The illustrative connection is:

```text
Lesson sequence
  ├─ Tutorial
  ├─ Knowledge point
  │    ├─ Example: problem + explanation
  │    └─ Questions → answer fields → answers
  ├─ Another tutorial
  └─ Another knowledge point
```

A lesson sequence is a future placement/scheduling concern. Tutorials can precede, occur between, and follow KP practice groups. Captured step IDs and content IDs are separate, so a content entity should not also be forced to represent its occurrence in a lesson. The previous decision to omit answer-choice positions remains appropriate; instructional sequencing is a different relationship, and should not be recovered by sorting arbitrary IDs or shuffling tutorial/KP refs.

We could instead reuse a question entity for an example, but the present question model requires an interaction type and at least one field with a correct answer. Importing a worked example into that model would require authoring a response interface and extracting/verifying a grading target from its explanation. That can be useful when deliberately turning an example into an exercise, but it is additional content creation, not a direct mapping of captured example data. Converting the demonstrated example into practice also does not mean it should automatically enter an assessment pool for a learner who has just seen its solution.

The two KP example strings have been replaced with a required `knowledge-point/example` ref. The example and tutorial each have their own schema file. Writers explicitly ensure `knowledge-point/validate` and `example/validate` separately; the reference does not automatically validate its target. The example ref is noncomponent so instructional content can be reused without cascading deletion. Questions own fields and their overall explanation directly; answer-field/correct-answer references the expected answer value. The example's explanation demonstrates its problem; question/explanation explains a separately authored practice question. These similar field names do not imply duplicated content or require a shared explanation entity.

If later requirements call for arbitrary reuse of the same problem across demonstrations and assessment interfaces, a shared problem entity would be another option. It would require changing question/problem and defining ownership and explanation reuse carefully. The current captures do not require that extra abstraction.

The readability review uses this presentation convention: enum declarations in a labeled section when needed, followed by identity, descriptive metadata, content and relationships, explanation, and validation. Attribute maps retain the order ident, value type, cardinality, uniqueness/component flags when relevant, and documentation. Topic difficulty now precedes knowledge-points, matching question difficulty before problem/fields. Field choices precede answer, presenting available options before identifying the correct one. Application validation requires choices for selection questions and omits them for blanks; the common field specification requires the correct-answer ref in both cases. The approved knowledge-point and example layouts are unchanged.

Math Academy identifiers are optional source identifiers wherever modeled; our own entity IDs are required. Source identifiers remain unique when supplied, allowing independently created content alongside imported content.

| Schema | Attribute presentation after any enum declarations |
| --- | --- |
| Course | id, math-academy-id, title, code, description, overview, outcomes, units, validate |
| Course outcome | id, index, category, text, validate |
| Unit | id, math-academy-id, title, index, modules, validate |
| Module | id, math-academy-id, title, index, topics, validate |
| Topic | id, math-academy-id, title, difficulty, prerequisites, knowledge-points, validate |
| Tutorial | id, title, content, validate |
| Knowledge point | id, math-academy-id, title, key-prerequisites, example, questions, question-generator, validate |
| Example | id, problem, explanation, validate |
| Question | id, math-academy-id, type, difficulty, requires-calculator, problem, answer-fields, explanation, validate |
| Answer field | id, key, answer-choices, correct-answer, validate |
| Answer | id, type, value, validate |

Course outcomes use one model for both observed formats: a bullet's text and an optional category heading. Of the 32 captured course maps, 16 use flat lists and 16 use categorized lists. The create-course-map guide explicitly allows both and does not equate outcome categories with curriculum units. Course-owned outcome entities are defined in [course-outcome.edn](course-outcome.edn); their 1-based index preserves order across the entire list, including category boundaries. The application renders bullets and optional headings and supplies the standard introductory sentence from the [skill](../skills/create-course-map/SKILL.md). No separate category entity is needed. Course description and overview retain their section bodies as Markdown strings.

Tutorial content was checked against five concrete captures:

| Topic / tutorial ID | Observed document structure | Source |
| --- | --- | --- |
| Imaginary Numbers / 2787 | Six content sections: prose, definition, equations, a short demonstration | [JSON](/home/jake/Developer/MA/DATA/Lessons/14/Source/14.json) |
| Tangent Planes / 3921 | Fifteen sections including two diagrams interleaved with explanation and calculations | [JSON](/home/jake/Developer/MA/DATA/Lessons/1980/Source/1980.json), [Markdown](/home/jake/Developer/MA/DATA/Lessons/1980/1980.md:29) |
| Tangent Planes / 3915 | Nineteen content sections: a derivation, equations, and a two-item list | [JSON](/home/jake/Developer/MA/DATA/Lessons/1980/Source/1980.json) |
| Parametrizing Systems / 13823 | Seven content sections: a worked illustration woven into prose and equations | [JSON](/home/jake/Developer/MA/DATA/Lessons/6295/Source/6295.json) |
| Reciprocal Trig Derivatives / 2629 | Ten content sections including a formula table, explanation, and calculation | [JSON](/home/jake/Developer/MA/DATA/Lessons/1686/Source/1686.json), [Markdown](/home/jake/Developer/MA/DATA/Lessons/1686/1686.md:23) |

Tutorials have document structure, but these samples do not establish a common set of semantic fields like the problem/explanation pair on worked examples. The capture normalizer creates sections from immediate HTML children; it does not establish that each paragraph is a separately identifiable domain entity. A string holding Markdown can encode the ordered document structure rather than reducing it to plain text. The existing Markdown files demonstrate equations, lists, tables, and images in the body. They still need content-quality review during migration: normalized readable-text placeholders are not themselves clean Markdown/LaTeX, and complex source layouts or math conversion may need correction.

For now, tutorial/content remains one Markdown body. Its documentation explicitly mentions tables, lists, and interleaved images. An ordered block model would be warranted for per-block editing, citations, reuse, interactive widgets, or structured asset references. That would require explicit ordering and block identities, because cardinality-many refs alone do not preserve document order. Such a model could serve other rich-text bodies too; the samples do not justify introducing it solely for tutorials yet.
