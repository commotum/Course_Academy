# Classification

Frozen database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Source wrapper is preserved verbatim in `source.json`. Owning topic17592186050190 is **Solving Systems of Linear Equations Using Elimination: One Transformation**, MA4026.

Both practice originals are unrated, lack every correct lookup reference, and lack worked solutions. They are included rather than omitted. There are **two observed prompt/layout templates**, one complete five-option radio bank and one two-blank layout with no captured answer values. No observed easy/moderate/hard labels exist.

| Source | Observed layout | Template/profile | Independently derived answer | Authored level assignment | Plots |
|---|---|---|---|---|---|
| q-18787 / 17592186193226 | one radio field `selection`, five complete tuples | `radio_solution` / `raw-q-18787` | (-5,-4) | moderate: smaller x coefficient2, multiplier-2 | none |
| q-208816 / 17592186193236 | `field-1`, `field-2` blanks; choices and correct refs absent | `blank_solution` / `raw-q-208816` | x=2, y=-1 | easy: unit smaller x coefficient-1, multiplier4 | none |

These level assignments are design claims, not recovered calibration. Easy/moderate/hard defaults each support both observed layouts. All complete records author missing correct references and fixed worked solutions; they never invent source ratings or source answer values. The historical radio distractors are opaque and remain evidence only, including their separately completed grading fixture. Normal radio defaults use a labeled authored bank of four actual method errors.

The captured authoritative original widget is `/home/jake/Developer/MA/DATA/Lessons/4026/Source/4026.json`; extracted relevant items are in `authoritative-layout.json`. It confirms Question5 has two free-response boxes and Question6 has five tuple options. No duplicate legacy field is being dropped.

The lesson route is reconstructed from activity/first-step17592186193457 and linked step/next: introduction → first-variable elimination setup192654 → second-variable setup192655 → **full first-variable solution192656** → full second-variable solution192657. Pull collection order is not used. Prerequisite MA742 explains elimination followed by substitution; its prerequisite MA2225 treats complete system solutions. The current KP assesses both coordinates, unlike192654/655, and requires first-variable elimination unlike192657. The subsequent two-transformations topic4236 is outside scope.

Presentation anomalies: both raw systems start with an unmatched TeX group `{`; raw blank punctuation has an orphan `$$`. Raw replay projects pulled field/answer enum refs to local ident strings, preserves every other captured value and attribute omission, and explicitly fails normal formatting checks with these known findings. Completed learner records escape the literal system glyph as `\{` and balance the blank punctuation. Omitted refs cannot count as matched correct designations. There are no mathematical source-option ambiguities: exactly one complete radio tuple satisfies both equations.

Normal workload bounds apply both to displayed rows and equivalent primitive equation triples. Common system factors and independent row factors cannot create a moderate/hard nonunit demand from an easy task. Same-level row rescaling remains allowed but deduplicates as one mathematical task; it changes presentation identity. Primitive reduction is an author-side eligibility check, never an added learner step.

Authored radio defaults can retain rational wrong tuples from their actual method errors, but every complete bank must include at least one entirely integer wrong pair beside its integer correct pair. This whole-instance eligibility guard avoids a correct-only integer shortcut; it does not alter source banks or blank questions.

## Current-source reclassification at basis 2154

A concurrent Math Academy capture refreshed q-18787 and added q-238082 after the initial read at basis 2150. The precommit source guard rejected that stale preparation without submission. `current-source.edn` and `current-source.json` preserve all three current practice records, while `source.json` continues to preserve historical basis 1356.

The current radio q-18787 is **easy**, has the same five mathematical tuples (spacing and four answer identities updated by capture), a valid correct reference, and a full worked solution. q-238082 is **moderate**, with two scalar blanks and the system `6x+13y=21; 2x+6y=12`, solution `(-3,3)`. Its prompt omits the elimination hint and uses an aligned display; its solution substitutes into the first row. q-208816 remains unrated and incomplete and contributes zero inventory. There are now three observed prompt structures including the historical blank-with-hint structure; all require no plots. Complete source values and source layout/solution evidence are preserved in the current snapshot. Every current rated field, complete radio bank, and arithmetic solution stage passed independent mathematical and current native grader checks in `current-source-validation.json`.

Current captured ratings supersede the historical suggested labels for those identities. Normal generated questions retain authored bounds; new moderate sampling is narrowed to multipliers 3–4 in response to the easy ratio-2 source. Easy unit-coefficient and hard ratio-5–7 families remain authored scope choices; hard has no captured rating. The legacy explicit moderate ratio-2 replay API remains archival evidence and is not selected for new moderate reserves. The new b=13 aligned blank template is retained and validated as source inventory, but is outside the generator's narrower b<=7 presentation policy. We do not claim exact Markdown/solution fidelity to that newly captured template. Existing source replay coverage and current-source grading coverage are reported separately.
