# Classification at basis 2210

Knowledge point 17592186110755, `3c73db44-2ec2-5025-9431-acb02e414916`:
Computing a Trigonometric Ratio Using the Pythagorean Identity.
Database math; lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`.
The captured `source.json` and `reference/source.edn` contain all seven practice
questions and canonical example at one immutable basis. No generator was registered.

| Band | Fields | Markdown/value templates | Profiles | Plots | Sources |
|---|---|---:|---:|---|---|
| Easy | one radio, key selection, five math choices | 2 | 4 | moderate | q-124625, q-37899, q-64681, q-65059 |
| Moderate | one radio, key selection, five math choices | 1 | 1 | moderate | q-37915 |
| Hard | no evidence | 0 | 0 | unknown | none |
| Unrated | one radio, key selection, five math choices, no correct key | 2 provisional | 2 evidence-only | moderate | q-37821, q-64731 |

The easy backbone asks for sine from a rational x-coordinate in quadrant I.
q-37899 uses “The point P lies on the unit circle” instead of “The diagram above
shows the unit circle,” with slightly different capitalization and final punctuation.
Keep this prompt layout separate; the other three share the same numeric/solution
backbone but have three different full banks. Moderate asks for 2 cos² from a
radical y-coordinate, without taking a square root or choosing a sign.
The unrated sources supply a radical x-coordinate or a radical y-coordinate,
respectively. They lack rating, correct key, and worked solution; preserve their
complete observed banks but exclude them from supported practice generation.
Canonical e-3482 supports the easy reasoning and positive branch, not inventory.

All plots were inspected in `reference/source-plots.png`. They supply the unit
circle and quadrant-I location; prompt and solution each have one diagram.
The solution diagrams label P(cos theta, sin theta). Some source diagrams are
schematic or reused with different coordinates, so their drawn angle is not
numerical evidence. Generated diagrams derive exact coordinates from the same
instance, preserving the mathematical relationships and quadrant.

No hard level can be justified from this captured evidence. The bounded capability
exception leaves its nominal five-question reserve unfilled. The two incomplete
unrated originals continue to trigger classification; they are not counted or repaired.
