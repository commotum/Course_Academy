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

This **private draft** implements all three user-requested levels without changing the registered easy-only package. Easy covers both axes 2..6 (25 ordered tasks). Moderate extends exactly one axis to 7..12 and keeps the other 2..6 (60 tasks, counting both orientations). Hard extends both axes to 7..12 (36 tasks). The meaningful union is 121 tasks, counted by ordered row/column counts only.

The missing-level rationale is deliberately limited: the lesson defines dimensions by counting every row and column and places no upper bound on rectangular arrays. Two unlabelled sequential enumerations remain the method. Easy requires zero counts beyond six, moderate exactly one, hard two. The two moderate orientations are equal-workload peers; every hard peer requires two extended counts. Number forms and entry arithmetic add no difficulty. The observed 6×6 easy source prevents us from calling another 6×6 array moderate merely because it has different entries or a different label. Extending an axis beyond six adds enumeration/bookkeeping demand; extending the second axis adds that demand again. These authored labels have no empirical MA difficulty validation and do not introduce a new mathematical technique. Variation is bounded within each band; no progression or new branch is asserted.

Maximum width/height is twelve, with single-digit integer entries for moderate/hard. Display math keeps the entire rectangular array visible; no row labels, ellipses, hidden entries, resizing puzzle, or entry manipulation is introduced. The extrema are inspected in render-qa.png. If a learner interface makes twelve columns unreadable at its viewport, the draft requires display support rather than inventing another skill. This review rendering does not certify every external interface.

All raw observed profiles are evidence-only and ineligible for default learning. They retain raw dot notation, the R/P source anomaly, missing legacy correct refs, missing worked solutions, and omitted unrated difficulty. Unlike the registered package, this draft does not add absent attributes to raw replay. Normal easy sampling uses all five original prompt/field families with separately authored full counting-operation banks. Moderate and hard use legible display-radio/display-dual-blank masks; source radio count and two-fragment blank shape remain unchanged.
