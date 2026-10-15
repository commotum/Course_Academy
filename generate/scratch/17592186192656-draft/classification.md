# Classification at frozen basis 2275

Database math, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json`, `reference/topic.json`, and `reference/lesson.json` are complete frozen wrappers. The three original-only `source-cases.json` records retain all raw attributes and omissions. Thirteen non-MA generated records are retained verbatim as independent inventory, with their original IDs, prompts, banks, keys, and solutions; they supply no MA evidence.

| Original | Difficulty | Response | Layout and solution | Plots |
|---|---|---|---|---|
| q-18787 | easy | one radio, five complete tuples | Explicit elimination prompt and first-variable hint; scale second equation by −2, distribute, cancel first variable, collect and solve y; substitute into FIRST original row and recover x | none |
| q-238082 | moderate | field-1 then field-2 blanks | Supplied ordered-pair context; scale second equation by −3, distribute, cancel first variable, collect and solve y; substitute into FIRST original row and recover x | none |
| q-208816 | absent | field-1 then field-2 blanks | Explicit first-variable elimination prompt. Captured system and tuple delimiters malformed; values, keys, solution, and rating absent | none |

There are three distinct prompt/layout templates, one observed complete radio bank, and two blank contexts. The source radio has five observed values and a captured correct reference; q-238082 has two observed singleton answer values and correct references. q-208816 has no captured answer bank or keys. Its independently solved result is (2, −1); supported keys and solution are expressly authored, never attributed to the capture.

The owning lesson proceeds from selecting one row multiplication and first-variable cancellation to recovering both coordinates. Its next systems lesson requires two transformations; that is excluded. Second-variable elimination belongs to a sibling KP and is excluded. Back-substitution occurs only after first-variable elimination. No matrices, determinants, or primary substitution method appear in learner content.

Easy and moderate have one example each. The historical default sampler remains a conservative subset: easy unit smaller first-variable coefficient, multiplier magnitude 2–7; moderate smaller coefficient 2–3, multiplier 3–4; hard smaller coefficient 2–3, multiplier 5–7. These are uncalibrated workload bands, not inferred MA calibration. Easy source replay also retains its observed nonunit coefficients. No progression is claimed within a band; all templates stand alone. Hard has no source example and is explicitly authored.
