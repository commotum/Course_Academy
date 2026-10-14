# Classification — Identifying Points of Discontinuity

Frozen provenance: database `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` retains the complete capture wrapper. Topic 17592186050574 / MA 462 is Determining Continuity from Graphs.

| Difficulty | Observed questions | Layouts | Semantic families | Plot rating |
|---|---:|---|---|---|
| easy | 17 | radio/text/math, radio/image, one blank, two ascending-order blanks | list all breaks; choose broken graph at stated x; single-coordinate blank; two-coordinate blanks | heavy |
| moderate | 0 | authored radio/text | three mixed graphical breaks, exactly one half-unit coordinate on labelled half-unit ticks | heavy |
| hard | 0 | authored radio/text | three mixed breaks, exactly two half-unit coordinates on unit ticks, connected corner to disregard | heavy |

The 17 frozen source presentation recipes retain differing operative prose, punctuation, worked-solution sentence sequences, answer fragments and whitespace. They are grouped into four semantic response families without merging their source banks: **13 full radio banks** (including the legacy duplicate widget) and **6 blank fields**, totalling **71 displayed answer values**. Radio banks each have five choices. There is one additional fieldless source. All observed questions are explicitly easy; there is no inferred original difficulty.

Source mapping and every option's literal value/type/field ownership are in `source-bank-map.json`. All 36 captured PNGs were inspected at native dimensions in `source-sheet-0.png` through `source-sheet-3.png`, including plotted answer distractors and highlighted solution figures. `plot-spec.json` records each separately.

Lesson order was reconstructed from activity/first-step and step/next:
Introduction (69567) → Continuity at a Point (69576) → determining continuity at one point (KP68695/69568) → this KP (68696/69569) → behavior near a point (68697/69570).
The introduction supplies the pencil-break criterion and a jump; the preceding KP includes an asymptote; this KP's canonical example has breaks at 0, 1 and 2.5. The following KP separately asks definedness and one-sided limit behavior. Authored levels stay before that boundary: they never ask for a limit, its existence/value, derivatives, formulas, or discontinuity classifications.

The missing-level workload claims are authored, not recovered source labels. Easy retains its observed integer-coordinate workload, even where three breaks are shown. Moderate requires all three mixed graphical breaks and reading exactly one half-unit coordinate from half-unit labelled ticks. Hard requires exactly two midpoints from unit labelled ticks plus ignoring a continuous corner. Signed coordinates and minimum separation 1.5 are mandatory; explicit inputs obey the same constraints. Each level is an unordered same-workload family, not a progression within a level.


## Current inventory reclassification (basis 2230)

The live source still contains 17 practice questions. Seven coordinate-set
questions now have checkbox fields; five remain five-image radio questions, four
remain one/two-blank records without captured graphs, and one has no answer fields.
The complete live read, including every field-owned Boolean bank and correct
reference, is retained in `reference/replenishment/initial.edn` and
`basis-2230/before.edn`. `basis-2230/current-classification.json` assigns every
source to a profile, reports field types/counts and eligibility, and records the
10 distinct fresh usable easy tasks after historical exposure/reservation reads.
The fieldless and four missing-widget records are preserved and excluded.

The checkbox migration changes the response layout; it does not change the
underlying graph or worked solution. Historical radio evidence at basis 1356 and
its complete-bank fidelity reports remain valid historical evidence, separately
from these current Boolean-bank checks. This job samples only the existing
validated authored moderate/hard templates and does not replace a live checkbox
question with a radio question. Source graph locations and all 17 worked
solutions are unchanged. All plots remain heavy.
