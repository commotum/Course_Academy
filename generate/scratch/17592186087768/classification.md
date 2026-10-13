# Classification

Snapshot: database `math`, basis **1356**, lineage
`01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The unmodified capture wrapper is
`source.json`; its canonical example is not counted as practice coverage.

Seven practice questions have one `selection` radio field with exactly five
complete circle equations. Six are observed moderate questions; q-72616 is
unrated and also lacks a worked solution and correct designation. No observed
easy, hard or blank field exists. q-72616 remains present in raw public replay.

| Level | Field | Markdown/value templates | Complete bank profiles | Plot rating |
|---|---|---:|---:|---|
| Observed moderate | radio | 4 | 6 | moderate |
| Unrated q-72616 | radio | 1 incomplete | 1 | moderate |
| Authored easy | radio | 1 | 1 | moderate |
| Authored hard | radio | 1 | 1 | moderate |

Observed families are `integer_center_first` (q-54215),
`radical_simplified` (q-117096, q-117099), `integer_signed` (q-72617), and
`radical_unsimplified` (q-72619, q-72621). All prompts have a diagram above the
text giving center C and an on-circle point X. The distance calculation differs
in subtraction direction, evaluated sign conventions and radius-stage count;
those differences are retained. Multiple bank profiles sharing one family are
kept separate. `incomplete_radio` preserves q-72616's absent attributes, including
the missing correct lookup ref. It is evidence-only and ineligible for learning.

All diagrams change with parameters; axes, the red circle, center dot, on-circle
dot and coordinate labels matter. Numbers are printed in the prompt as well, so
no inferred grid-reading skill is added. Source rasters were inspected at their
360 × 304 native dimensions. Exact source geometry permits unchanged replay
assets; all changed geometry uses Matplotlib.

The lesson route was reconstructed from first-step and next refs:
Introduction → center and radius → extracting center and radius → **center and
on-circle point** → diameter endpoints. The captured prerequisite is Equations
of Circles Centered at the Origin (842). The canonical example establishes
distance-formula computation followed by center/radius substitution, with a
zero center coordinate and a 3-4-5 distance. Source q-54215 includes the 6-8-10
distance; sources also include unsimplified and simplified radical radii.

Authored easy reduces only center-substitution bookkeeping: exactly k = 0,
nonzero integer h of magnitude at most 5, and signed/oriented 3-4 or 6-8 offsets.
Both distance components remain nonzero. Every easy instance has the same two
coordinate differences, two squares, sum, integer square root and substitution.
Authored hard increases only the number-form workload: both center coordinates
and both differences are noninteger half-integers of magnitude at most 9/2;
the point coordinates are integers and squared radius is noninteger. Every hard
instance has two integer-minus-half-integer differences, two fractional squares,
their sum and the same radius/substitution stages. These are design claims,
not recovered source labels. Fractions use the same pre-existing coordinate
arithmetic; no additional circle method or mathematical branch is introduced.

Normal moderate uses nonzero integer center coordinates of magnitude at most 5,
nonzero integer differences of magnitude at most 8, and squared radius ≤ 100.
The bounds preserve observed short exact arithmetic and signed shifts. All
source parameters satisfy them. Explicit calls enforce the same bounds.
The two four-row integer-radius masks, q-54215 and q-72617, additionally require
perfect-square squared radius. Their final radius row must actually simplify
the preceding square root to an integer. This source-grounded profile guard
applies equally to sampling and explicit calls; all original parameters remain
accepted. The simplified-radical masks q-117096/q-117099 require nonsquare R
with a nonunit extractable square factor, so their final radius really performs
radical reduction. The unsimplified masks q-72619/q-72621 require nonsquare R,
retaining their deliberate unreduced square-root conclusion. These shape
constraints apply equally to explicit calls and samplers and preserve every
original practice question. Their filtered finite domains are quantified in
`validation.json`; no broader normal profile is introduced.
The ordinary moderate entrypoint chooses uniformly among all six rated source
profiles before parameter sampling and retains the chosen family's solution
mask. A colliding complete bank causes its parameters to be resampled within
that selected profile; no profile is replaced or mixed. q-72616 is excluded from
this default selection because it lacks the original correct designation.

The remaining source deficiency is q-72616's incomplete metadata. Its original
MA JSON confirms a five-choice multiple-choice widget and no captured solution
or designation (`authoritative-layout.json`). Distance independently determines
(x+1)²+(y−2)²=10. `complete_incomplete` produces a separately labeled authored
completion; it never contributes a matched original designation or solution.
