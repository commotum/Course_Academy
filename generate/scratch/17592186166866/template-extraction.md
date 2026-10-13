# Template extraction — four stages

## 1. Specific original questions

Each original asks “Find dy/dx for the ellipse shown above” after one diagram. q-127362 and q-127364 use unstyled `dy/dx`; the other seven use `\text{d}`. All choices are full rational derivative expressions, no equation fragments. Every field is `selection`, radio, five math answers. `source-cases.json` contains original parameters and bank identifiers. `source.json` preserves complete raw schemas and strings.

| Source | label | center | horizontal a | vertical b | complete operation sequence |
|---|---|---|---:|---:|---|
| q-127362 | absent | (0,0) | 3 | 2 | -lXY, +rXY, +iXY, -vXY, -rXY |
| q-127364 | absent | (2,-1) | 3 | 4 | -vYX, -rXY, -lXY, +rXY, +iYX |
| q-127511 | easy | (0,0) | 1 | 2 | -iYX, +vXY, -rXY, -lXY, +vYX |
| q-127512 | easy | (0,0) | 5 | 3 | -rYX, +iYX, +vYX, -rXY, -lXY |
| q-127513 | easy | (0,0) | 2 | 5 | -rXY, +lXY, -lYX, -lXY, +rYX |
| q-127514 | easy | (0,0) | 3 | 1 | -lXY, -rXY, -vXY, -iYX, -vYX |
| q-127523 | moderate | (-1,-1) | 2 | 1 | -rXY, +rWV, -vYX, +rVW, -vXY |
| q-127525 | moderate | (0,1) | 2 | 3 | -vYX, +lYX, +lXY, -rXY, +vXY |
| q-127526 | moderate | (3,0) | 3 | 2 | -iYX, +lXY, -rYXt, +vXYt, -rXY |

Each sequence maps the full observed bank one-to-one in original source order. Signs are part of each operation. `bank-mapping.json` records every original UUID, exact displayed value and parameterized symbolic value. q-127364 uniquely has spaced ASCII rational notation; replay retains it. No mathematical source error or equivalent duplicate was found. The two missing records are omissions, never counted as observed answers or solutions.

## 2. Shared mathematical pattern

Read h,k,a,b from the plot. Form (x-h)²/a²+(y-k)²/b²=1. Apply d/dx to both sides, split the sum, differentiate x and y terms retaining dy/dx on the y term, move the x term, and divide. The requested full derivative is -b²(x-h)/(a²(y-k)), defined for y≠k; at the two horizontal-axis vertices the tangent is vertical.

## 3. Components and banks

Set X=x-h, Y=y-k, r=b²/a², v=a²/b², l=b/a, i=a/b. `±rXY` denotes ±rX/Y, and likewise v,l,i and reversed YX. VW uses x+h over y+k; WV reverses those incorrectly signed center factors. Suffix t transfers horizontal center h to the y factor: YXt=(y-h)/x, XYt=x/(y-h). These are complete operation recipes grounded in the actual standard-ellipse and isolation method: lost minus sign, unsquared axis lengths, inverted squared scale, reversed coordinate quotient, wrong center sign, or assigning the horizontal shift to the vertical factor. Compound recipes retain every component. Their historical intent remains hypothetical; exact numerical reproduction does not prove which cognitive mistake a source author intended.

Historical banks are evidence only (`observed-*` and `completed-*`). Authored default uses a complete fixed method bank [-rXY,+rXY,-vXY,-lXY,-vYX]: correct isolation; lost rearrangement sign; reciprocal squared scale; unsquared axis lengths; reversed x/y isolation and reciprocal scale. No unrelated a+1, uniform doubling or halving is introduced. Whole-bank collision rejection precedes output. Parameter sampling never substitutes first-valid unrelated wrong values.

## 4. Reusable templates

Fixed: plot placement, prompt wording, selection field, five choices, shared explanatory sentences, and five ordered solution rows. Variable: center, semiaxes, squared denominators, derivative operator arguments, formal sum, chain factors, reduced factors, final ratio, geometry asset and bank profile. Conditional: origin versus coordinate center prose; omit denominator 1; strip shifted numerator grouping only when its coefficient is 1; preserve redundant simplification-row omission from all practice sources; source absent attributes remain absent. The normal script constructs source replay through these same recipes rather than returning a source JSON branch or an answer lookup table.

Exact replay requires complete prompt, every answer string, complete shared solution prose and ordered math, correct designation where originally present, and key-presence parity. Mathematics is separately established by parsing the actual displayed equation and every derivative row, including both formal d/dx inputs and the split derivatives. Source canonical e-9578 has one extra simplified-sum row; it anchors scope but is not one of the nine practice replays.

The difficulty partition is by reduced workload, not unreduced axis magnitudes. Origin remains easy. Moderate peers are single shift/nonunit reduced ratio or two shifts/unit reduced ratio, supported by the three graded originals. Hard requires two shifts/nonunit reduced ratio and coprime semiaxes 3..8. The unrated q-127364 is independently routed to hard in its completion; raw replay still omits difficulty. Actual level participates in content identity. All nine historical banks and all present source solution stages remain exact.
