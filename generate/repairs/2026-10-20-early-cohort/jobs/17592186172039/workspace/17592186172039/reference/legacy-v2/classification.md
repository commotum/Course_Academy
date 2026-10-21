# Classification, steps 3–7

Snapshot: math at basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is an unchanged copy of the current source wrapper. All eight practice questions are included; the canonical e8506 is context, not a ninth practice source.

Every practice question has one `selection` radio field with exactly five text answers. There are no mathematical blanks or mixed layouts. Prompts and choices have no plots, but seven available worked solutions contain one quadrant sign diagram each. Plot rating is **light**: only the fixed solution uses a simple diagram; the equation and statements suffice to answer the question. Diagram selection depends on the actual sign pattern and zero set.

| Observed level | Template | Practice sources | Profiles | Sequence distinction |
|---|---|---|---|---|
| Moderate | bilinear_open_thin | q96767 | bank96767 | Three statement checks; no final answer sentence; math rows end with `\,` |
| Moderate | bilinear_closed | q119766, q119769 | bank119766, bank119769 | Three checks plus final answer sentence |
| Moderate | bilinear_open | q97477, q97482 | bank97477, bank97482 | Three checks; no final answer sentence |
| Hard | parity_closed | q119774 | bank119774 | Both coordinates squared; final answer sentence |
| Hard | parity_open | q97487 | bank97487 | y squared, x linear; no final answer sentence |
| Unrated | parity_numbered | q97483 | bank97483 | Numbered statements, plain dy/dx fraction; missing solution and correct designation |

The observed coverage is **0 easy, 5 moderate, 2 hard, 1 unrated**. Six observed presentation templates and eight distinct whole bank profiles are retained. q97483 receives an explicitly **authored hard assignment** because its xy² workload matches observed hard q97487. Its canonical correct subset is independently derived, not reported as an observed correct match. The original local MA widget confirms all five choices and numbered layout; it provides no correct marker or solution. See `q97483-widget.json`.

## Curriculum and authored scope

The owning topic is 3352, Slope Fields for Nonautonomous Differential Equations. Following `activity/first-step` then `step/next` gives Introduction → isolated-point slope-field sketching → **this quadrant KP** → rectangular-region sign identification → Symmetry in Slope Fields → slope-field type identification. This order is reconstructed from links, not collection order. The prerequisite is Solving Two-Variable Nonlinear Inequalities (2076).

The canonical example uses -2xy and three global quadrant statements. Easy is an authored reduction to **cx**, keeping three statements, open quadrants, one five-choice radio field, and the same sign-classification purpose. It requires the sign of one coordinate and coefficient, eliminating multiplication of two coordinate signs. Although cx is independent of y, it is still nonautonomous (depends on x); the lesson introduction distinguishes f(x), g(y), and f(x,y). Easy is a design claim, not a recovered MA difficulty label.

Moderate varies nonzero signed coefficients of xy and the quadrant/sign claims. Hard varies the observed parity structure using exponent pairs (1,2), (2,1), (2,2); x²y is the coordinate-exchanged same-workload authored extension. These are unordered equal-level variations, without a progression or extra algebra. Coefficients are signed integers of magnitude 1–9 at all levels, preserving source arithmetic simplicity. Magnitude affects display only, not assessed sign classification.

Every instance asks about **every point in an open quadrant**. Axes are excluded. Each admitted monomial is continuous and nonzero throughout each quadrant; independent positive-symbol substitution proves its sign on the entire quadrant. Sums, shifted factors, logarithms, trig, sign-changing curves within a quadrant and nonreal/undefined expressions are not admitted. Consequently test-point diagrams cannot incorrectly establish a global claim for an expression that changes sign within a quadrant. The generator never enters the sibling rectangular-region, isolated-point sketching, or slope-field type KPs.

## Finite meaningful variety

A canonical task excludes |c|, complete answer-bank profile, layout and statement order. It retains coefficient sign, exponent workload/parity, the three selected quadrants and their claimed signs. With unordered distinct quadrant selections there are `2 × C(4,3) × 2³ = 64` tasks for easy and moderate each, and `3 × 64 = 192` hard tasks. All **320** are exhaustively validated; 1,000 random seeds recover all tasks in each level. Ordered statement permutations provide valid presentations, but do not inflate those counts. There is no claim of an infinite meaningful bank or of new skill recovery from number changes.
