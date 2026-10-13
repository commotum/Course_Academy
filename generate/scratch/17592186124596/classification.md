# Classification

Database math, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` is an unchanged copy of the capture wrapper. Seven practice questions, four easy and three moderate; no observed hard questions. Every question has one radio field keyed `selection`, five complete mathematical expression choices, and a correct reference. No field/bank anomalies or plots occur. The canonical example is curriculum evidence, not an eighth practice question.

| Level | Observed templates | Authored templates | Field/layout | Plot requirement |
|---|---:|---:|---|---|
| Easy | 4 | 0 | one radio, five expressions | none |
| Moderate | 3 | 0 | one radio, five expressions | none |
| Hard | 0 | 2 | one radio, five expressions | none |

All seven observed complete banks remain available as `observed` profiles. Defaults use one complete `authored_operations` profile per template, with exactly five options. Original wrong-expression intent is underdetermined; explicit replay profiles parameterize their mathematical patterns without claiming the source author used those errors. Normal default generation uses documented operations on the assessed derivatives.

## Easy

Target cylindrical z: differentiate the Cartesian polynomial in z, leaving x and y fixed; then substitute x=r cos(theta), y=r sin(theta). The extra coordinate path contributions are zero because x_z=y_z=0 and the shared z coordinate has derivative 1. Four templates cover mixed z terms, square/cross terms with a double-angle collection, a single surviving derivative, and square/linear terms. The source's same-symbol z convention is retained in replay; defaults explicitly distinguish holding r/theta on the left and x/y in the Cartesian derivative before substitution.

## Moderate

Two angular templates exercise two chain-rule branches, one with cancellation and one with a negative Cartesian derivative. One radial cubic template substitutes two squared Cartesian partials and factors their sum. These are observed equal-level applications; there is no progression inside the sampler. Coefficients are nonzero signed integers with absolute value 1..5, powers in the cubic template satisfy 1 <= q < p <= 4. Both sampled and explicit parameters obey the same bounds.

## Hard — authored missing-level definition

The canonical w=z^3(x^2+2y^2) angular example uses the same two branch formula and collection into sin(2theta). Add a nonzero xy term to a weighted quadratic, with unequal x^2/y^2 coefficients. This produces four nonzero distributed products followed by one trig collection. The radial companion uses x^2, xy and y^2 terms with two different existing z-power coefficients: again four distributed products, followed by collection. This is a supported design claim, not an observed hard label. It adds coupled terms to existing first-order polynomial differentiation, without adding inverse coordinate transforms, spherical coordinates, higher derivatives, logarithms, evaluation angles, or a new mathematical branch.

Hard angular: z^k(a x^2+bxy+c y^2), 2 <= k <= 4, a != c. Hard radial: a x^2 z^p+bxy z^q+c y^2 z^p, p=2..4, q=1..3, p != q, a != c. All a,b,c are nonzero with absolute value <= 5. Neither family can lose its cross component under explicit parameters. Every instance has four nonzero pre-collection products regardless of signs.

## Curriculum order and prerequisites

The owning topic is 17592186048635 / MA 1942, The Multivariable Chain Rule With Polar Coordinates. Following the captured activity first-step and step/next gives 17592186125531 (plane-polar introduction), 25532 (Cartesian to plane polar), 25562 (inverse formulas), 25533 (polar to Cartesian), 25534 (cylindrical tutorial), 25535 (this KP), 25563 (spherical tutorial). The cylindrical tutorial states the r/theta formulas and unchanged z differentiation. Preceding topic links identify Cylindrical Polar Coordinates (1981), The Multivariable Chain Rule (3173), and Spherical Polar Coordinates (1982); only the first two are used here. Spherical material is outside these templates. Sibling canonical examples support the two-branch method, not a move into their inverse/plane KPs.

## Source mathematical anomaly

DB 17592186360582, q-95172, v=2y-xz: the first generic chain row prints (partial v/partial y)(partial v/partial theta), where the coordinate factor must be partial y/partial theta. Raw evidence is retained unchanged. The generator makes only that mathematically supported symbol repair; the rest of the bank and solution is correct. Report 6/7 unrepaired-equivalent ordered solutions and 1/7 minimally repaired solutions. All seven prompts/solutions use notation normalization, so raw exact string counts are separately zero. Field and bank repair counts are zero.
