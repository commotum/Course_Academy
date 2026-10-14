# Classification at frozen math basis 1356

Database `math`, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Eight captured practice records; the canonical example is not included in the counts. All plots: **none**. There are no image references in these practice questions or their worked solutions; lesson illustrations are outside the assessed calculation.

| Family | Original ID | Observed level | Field | Prompt/function and solution distinction |
|---|---:|---|---|---|
| linear_y2 | 17592186124962 | absent | radio, 5 | 2x+y², point (0,1), supplied vector (5,2); no solution/correct ref |
| chain_square | 17592186125029 | absent | radio, 5 | (x+y²)², A(-1,-2) toward B(2,2); no solution/correct ref |
| supplied_gradient | 17592186235525 | easy | blank, 1 | div V at (1,1), v=(-3,4), prior part-3 gradient (4,2) only supplied in solution |
| xy | 17592186265867 | easy | radio, 5 | xy at (2,1), vector (√3,1); gradient evaluation directly reduced |
| log | 17592186265868 | easy | radio, 5 | ln(x²+y²) at (0,-1), vector (3,4); quotient substitution and negative component |
| quadratic | 17592186265869 | easy | radio, 5 | x²+y²−xy at (1,1), vector (1,−1); dot cancellation to zero |
| exp | 17592186323790 | moderate | radio, 5 | xeʸ+x²y at A(1,0) toward B(0,1); two component products, evaluate e⁰ and dot directly |
| x2_linear | 17592186354470 | easy | radio, 5 | 6x²+2y at (0,1), vector (3,5); zero x partial and radical denominator |

Eight source prompt/value families and eight complete observed banks. Two missing labels are preserved in raw API replay. Normal linear_y2 has an authored easy assignment; normal chain_square has an authored hard assignment. Five observed easy records, one observed moderate record, no observed hard label.

The ordered lesson route (first-step 17592186125299, then next 17592186125300) places the introductory gradient·unit-vector formula immediately before this KP. Its next tutorial 17592186125301 introduces maximum increase and precedes sibling KP 17592186124459. That optimization branch and sibling maximum-rate KP 17592186124460 are excluded. Prerequisites are gradient vectors, component dot product, and 2D magnitude. The unrated nested-square practice question demonstrates the chain-rule derivative within this calculation. Hard is an authored workload claim: nonzero inner value, nonzero y chain factor, two-stage chain partials, A-to-B subtraction, normalization and dot product; it does not add optimization or geometry.

`supplied_gradient` is context-limited: original local MA lesson 1938 Markdown/JSON contains older 36273/37077 sources but not q-168116 (read-only search conducted). The captured solution explicitly supplies ∇f(1,1)=(4,2). We can verify the directional calculation from that datum, but cannot independently verify it is the gradient of the missing original V. Normal prompts supply the gradient explicitly, so they stand alone; this is a documented context completion.
