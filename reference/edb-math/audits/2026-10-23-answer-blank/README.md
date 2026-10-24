Read-only diagnosis of question `17592186491432` at `math` basis **T6099**.

The problem ends with `{{selection}}`, while its sole answer field is a radio-choice field named `selection`, with five choices and a linked correct answer. The stray token becomes an extra, non-interactive “Answer” underline above the actual choices.

The owning KP is `17592186064281`, “Differentiating a Trigonometric Function Using the Chain Rule,” in topic 305, “The Chain Rule With Trigonometric Functions.” Its registered generator is [17592186064281.py](../../../../generate/scratch/17592186064281.py). Line 84 explicitly appends `\n\n{{<field-key>}}` whenever the source field type is radio.

The source template is `q-31163` at T1977. Its original problem has no selection placeholder. Running the generator with that profile and `t=12` reproduces both the exact UUID `edc669f2-8811-573d-b7ea-ebf03a0592e1` and the exact stored problem, including the trailing marker. [Generator reproduction](generator-reproduction.json) records the source, parameters and code hash. The same behavior occurs in all 38 eligible radio parameter cases in this generator's three radio families; this is a generator-output count, not a count of existing affected database records.

The retained [question history](history.jsonl) contains the marker in the T1978 assertion, attributed to `:application/ca-engine`. The source text reaches this record through generated-question creation.

The player’s [inlinePrompt](../../../../ui/question-fields.js:122) places only `blank` and `select` fields inline, so it leaves `{{selection}}` untouched for a radio field. The later [generic Markdown fallback](../../../../ui/learning.js:277) recognizes all field keys and converts the leftover marker into a `field-location` span. [fieldLabel](../../../../ui/learning.js:116) labels the key `selection` as “Answer.” That span has no `data-field-key` and is not an answer input.

[Renderer replay](renderer-reproduction.json), produced by [reproduce_render.py](reproduce_render.py), confirms that the stored prompt yields exactly one “Answer” span and zero inline answer slots. Removing only the trailing radio marker in memory eliminates that span without producing math errors. The stored answer fields, choices and correct-answer link are intact.

The repair should remove these misplaced radio markers from stored prompts and stop generators from appending them. A renderer/validation guard can also prevent a radio marker from becoming a blank. Database contents, generator code and player code were unchanged during this diagnosis.
