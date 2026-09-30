The content model follows this chain:

```text
knowledge-point/questions → question/answer-fields → answer-field/correct-answer
                                             answer-field/answer-choices → answer entities
```

The question owns its fields and worked explanation directly. Each field has a required correct-answer ref. Selection fields also have optional-in-schema answer-choices containing the correct answer; blanks have no choices. Multiple blanks are separate named fields. There is no intermediate response entity or separate choice entity.

| File | Entity | Purpose |
| --- | --- | --- |
| [4-question.edn](../schema/content/4-question.edn) | Question | Interaction metadata, problem, answer fields, and overall explanation |
| [5-answer-field.edn](../schema/content/5-answer-field.edn) | Answer field | A named response location, optional choices, and required correct answer |
| [6-answer.edn](../schema/content/6-answer.edn) | Answer | Identity, representation type, and a required string value |

The answer type is local to each answer, allowing a question or selection field to mix mathematical, textual, and image options. Every answer stores its content in the required string attribute `answer/value`, interpreted using `answer/type`: LaTeX without Markdown delimiters for math, plain text for text, and an image path or URI for images. There is no separate image entity. Image locations are strings, so resolving them and checking availability belong to the application, not EDB reference traversal.

| Interaction | Fields | Application evaluation |
| --- | --- | --- |
| Multiple choice | One | Compare selected answer identity with answer-field/correct-answer |
| Single blank | One | Parse and compare the entry with the expected answer value |
| Multiple blanks | Several named fields | Evaluate each entry against its field's expected answer |
| Dropdowns | One or several named fields | Each field has its own choices and correct-answer ref |

There are no evaluation attributes or grading enums. Application code dispatches basic checking by question/type and answer/type. Mathematical parsing and comparison and text normalization are not implemented by these schemas. If questions later need differing tolerances, required mathematical forms, or other acceptance requirements, those requirements need an explicit content model; a generic evaluation enum does not solve them. Student submissions and their outcomes belong to future activity data.

No positions are stored. The application controls option order. Each answer-field/key is unique within its question and binds the expected answer to a problem location such as `{{answer-field:x}}`. This is a proposed template convention, not recovered MA syntax.

Question/type and question/difficulty enum entities are declared in the question file; answer/type enum entities are declared in the answer file. Categorical attributes are ordinary refs. Undeclared idents fail resolution, but refs to an existing entity outside the intended enum group still need membership validation. This follows the [documented Datomic enum pattern](https://docs.datomic.com/schema/schema-modeling.html).

The question owns its fields through component refs. Each field owns its correct answer and choices through component refs; a selection's correct answer is reached by both refs from that same field. Answer entities must not be shared between fields. Deleting an image answer removes its stored location string, not the external image file. Enum refs are ordinary refs.

The samples that motivated this structure were:

| Topic / question | Observed structure | Local source |
| --- | --- | --- |
| Tangent Planes to Surfaces / 37721 | Five mathematical text options | [1980.json](/home/jake/Developer/MA/DATA/Lessons/1980/Source/1980.json) |
| Graphical Representations of Relations / 213011 | Five image options; inspected a local mapping diagram | [4837.json](/home/jake/Developer/MA/DATA/Lessons/4837/Source/4837.json) |
| Rational equations / 215061 | One mathematical blank | [3555.json](/home/jake/Developer/MA/DATA/Lessons/3555/Source/3555.json) |
| Principal Normal Vectors / 222843 | Two blanks for separate vector components | [1795.json](/home/jake/Developer/MA/DATA/Lessons/1795/Source/1795.json) |
| Solving Linear Congruences / 213469 | Five blanks for successive modular powers and the solution | [4839.json](/home/jake/Developer/MA/DATA/Lessons/4839/Source/4839.json) |
| Paired-sample confidence intervals / 251528 | Four dropdowns containing 2, 4, 2, and 3 options respectively | [3970.json](/home/jake/Developer/MA/DATA/Lessons/3970/Source/3970.json) |
| Logical inference / 175874 | One dropdown with four options | [4305.json](/home/jake/Developer/MA/DATA/Lessons/4305/Source/4305.json) |

These captures establish interaction shapes and option content; they do not uniformly provide correct-answer keys. This is our proposed EDB model, not a recovered internal MA schema.

Writers explicitly ensure question/validate, answer-field/validate, and answer/validate for the corresponding entities. Native checks require at least one question field, a field key and correct-answer ref, and an answer identity, type, and string value. They do not automatically validate referenced entities. Application validation must additionally enforce enum membership, field-key uniqueness, selection choice membership, the absence of choices for blanks, and nonempty and correctly formatted values appropriate to each answer type. Image availability and mathematical evaluation are separate application responsibilities.
