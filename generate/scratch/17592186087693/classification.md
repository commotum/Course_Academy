# Classification — matrix dimensions

Evidence: `math`, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`; all eight captured practice questions. Source wrappers are preserved in `source.json`, `topics.json`, `lessons.json`.

| Template | Practice sources | Original difficulty | Fields | Banks | Plots |
|---|---|---|---|---|---|
| bmatrix-radio | q-11454, q-7806 | unrated; authored easy assignment | one radio, five choices | two distinct ordered-dimension banks | none |
| aligned-radio-inline | q-125527, q-125528, q-125529 | easy | one radio, five choices | three distinct banks | none |
| aligned-radio-break | q-69542 | easy | one radio, five choices | one bank | none |
| context-dual-blank | q-139406 | easy | field-1 then field-2 in prompt; captured field collection order field-2, field-1 | two single-count banks | none |
| let-dual-blank | q-319310 | easy | same two-count layout/order | two single-count banks | none |

Six observed easy cases; no observed moderate or hard cases. The two unrated cases have neither correct references nor worked solutions in EDB. Their captured original widgets confirm one five-choice radio each (`legacy-widget-evidence.json`); screenshot `/home/jake/Developer/MA/DATA/Lessons/861/Source/Sections/04-question-11454.png` was inspected. It displays ×, while EDB spells the separator `\cdot`. This is a capture notation artifact, not evidence that dimensions are commutative multiplication. Raw EDB strings remain available through explicit observed profiles. Normal output uses ×. Correct inferred keys are ordered (2,4) and (2,3), independently counted from their actual arrays; these are not matched original designations.

q-139406 prompts P but its source solution names R. Explicit original replay preserves the raw error; normal authored output names the actual matrix. Renamed observed variants also name their actual matrix. No dimension value is wrong. All source placeholders exist. q-139406's long whitespace is preserved in exact replay rather than treated as a missing field.

Lesson route was reconstructed from first-step 17592186088514, following next references: Introduction → Square Matrices → this KP (17592186088515) → one-row/column introduction → sibling KP → identifying by description → modeling → route-planning KP. Pull collection order was not used. The canonical example is a 4×3 displayed matrix. Prerequisite Surds makes radical entries familiar; entries are incidental here. This generator excludes one-row/column matrices, choosing a matrix from a description, graph/table construction, index notation, determinants, and every matrix operation.

Only **easy** is supported in version 1.1.0. The former moderate/hard peer labels assessed the same two counts and are withdrawn. Neither the larger arrays nor more complicated entries increase the mathematical demand: both already occur in easy sources. Moderate/hard remain bounded package exceptions with nominal shortages of five each, rather than filled bands. New source evidence can reopen classification. The old version is retained in `history/v1-peer-labels/`.

The supported finite domain is 25 ordered shapes, with 2..6 rows and columns. Matrix entries, names, bank profiles, field layouts, seeds and identities do not increase this count. Source IDs and original records are preserved; missing legacy keys and solutions are derived solely for replay and new output.
