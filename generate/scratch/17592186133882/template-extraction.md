# Supported extraction: triangle polynomial

Source q-109111 supplies the triangle with vertices (−1,0), (1,0), (0,1), P=y²,
Q=3xy, and asks for the full function f(x,y) in Green's double integral. Its field
is `selection`, a single radio response with five math choices. Its source values
are y (correct), 3x, −y, y−x and x−y. The original source UUIDs, exact notation and
field ownership are retained in `source.json`; `source-fidelity.json` maps each
choice to its generated expression with one-to-one mathematical comparison.

The backbone is to identify P and Q, compute P_y and Q_x, subtract Q_x−P_y, and
place the resulting scalar curl into the double integral over the same D. The
worked solution retains the theorem/hypotheses, diagram, P/Q identification,
two derivative computations, theorem substitution, concrete subtraction,
simplification, and final function. It is independent of the learner's choice.
The target is the entire scalar curl, fixed in role and notation. No integration,
new operation, changed field layout or additional reasoning stage is introduced.

| Slot | Source | Sampling bounds | Dependent components |
|---|---|---|---|
| a, coefficient of y² in P | 1 | integer 1..5 | P, P_y=2ay, bank, prompt and every solution occurrence |
| b, coefficient of xy in Q | 3 | integer 1..9, b≠2a | Q, Q_x=by, bank, prompt and every solution occurrence |
| curve and orientation | fixed triangle, positive | fixed | prompt vertices, diagram, D and theorem hypotheses |
| requested object | f=Q_x−P_y | fixed | exact complete function selected through radio |

The two coefficient slots are conservative same-method extensions beyond the
single observed pair. Nonzero positive coefficients retain both derivative
steps; b≠2a prevents the zero answer and ±answer collision. The bounds limit
arithmetic size. There are exactly 41 pairs, including the source pair; at most
40 new tasks relative to that source can ever be added, before deducting further
existing content. Distinctness uses both supplied P and Q, excludes seeds, IDs,
choice order, and requires deduplication against the source task too.

The complete source bank is selected before rendering:

| Source value | Parameterized value | Interpretation |
|---|---|---|
| y (correct) | (b−2a)y | Q_x−P_y |
| 3x | bx | derivative of bxy with respect to y instead of x, with P term omitted |
| −y | (2a−b)y | reversed subtraction |
| y−x | a(y−x) | observed expression-shape extension; original mistake unresolved |
| x−y | a(x−y) | observed expression-shape extension; original mistake unresolved |

The last two recipes are explicitly inferred coefficient extensions, not claims
about the source author's error algorithm. All five options must be inequivalent
as functions (equality at a particular point is irrelevant). No feedback is added.
Replay matches all five original mathematical objects ignoring option order.

The source worked solution accidentally repeats Q as xy in its line integral
while its prompt, derivative and answer use 3xy. Newly generated solutions derive
all occurrences from bxy and use positive orientation; the source is preserved.

## Plot extraction and reuse

The inspected 361×304 PNG has black Cartesian axes with arrowheads, a pale blue
filled triangle D, orange edges joining (−1,0), (1,0), (0,1), and black boundary
arrows showing counterclockwise traversal. It labels D, x, y, and the unit
coordinates. The base arrow points right; the right edge points toward the apex.
The vertices, orientation, fill and labels are meaningful; exact colors are style.
Changing a,b changes only the differential form, so this region illustration is
reused byte-for-byte in the solution. No new plots are required (rating none).
The content-addressed path and verified byte hash are in `validation.json`.
No separate renderer or asset publication is needed for an already stored asset.

Other source templates and banks remain exact evidence in the source capture;
they are not generalized by this generator or claimed as fidelity successes.
