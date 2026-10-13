# Candidate KP absence confidence scores

Discovery at 2026-10-12T19:34:48.863Z, EDB `math` basis **1522**. Each distinct surfaced KP appears once.

**384 KPs across 120 topics:** 358 have rated questions; 26 have no rated evidence and receive no score.

For each missing level: **score = 100 × (1 − (1 − p)ⁿ)**. n counts distinct rated practice questions in the KP. Unrated questions and repeated appearances do not increase n. Scores are heuristic evidence of absence, not posterior probabilities.

The **hybrid score** measures the entire missing-level pattern: **100 × [1 − (1 − Σ p_missing)ⁿ]**. For two missing levels A and B, the chance of observing neither under the reference distribution is (1 − p_A − p_B)ⁿ. For one missing level, the hybrid equals that level's score. With no missing levels or no rated evidence, the hybrid is not applicable.

A high hybrid score says the combined gap is surprising. It does not imply equally strong evidence for every missing level; read the separate scores alongside it. All scores use the same reference-distribution and independent-draw assumptions.

The global reference distribution deduplicates KP-linked questions by entity. An observed database or captured question establishes that a level exists; its cell says ‘Observed’.

| Level | Reference questions | Expected share | KPs scored | Scores ≥99 |
|---|---:|---:|---:|---:|
| Easy | 13,601 | 44.6256% | 117 | 74 |
| Moderate | 12,347 | 40.5112% | 93 | 41 |
| Hard | 4,530 | 14.8632% | 233 | 0 |

## All groups

Scores below are **medians of the per-KP scores**, not a pooled group confidence. The detailed tables retain every KP's individual scores.

| Missing levels | KPs | Median easy score | Median moderate score | Median hard score | Median hybrid score |
|---|---:|---:|---:|---:|---:|
| None | 38 | — | — | — | — |
| Easy | 67 | 99.5105 | — | — | 99.5105 |
| Moderate | 6 | — | 94.0588 | — | 94.0588 |
| Hard | 124 | — | — | 72.3981 | 72.3981 |
| Easy–moderate | 14 | 99.3132 | 98.7492 | — | >99.9999 |
| Moderate–hard | 73 | — | 98.4315 | 72.3981 | 99.8427 |
| Easy–hard | 36 | 99.7289 | — | 79.9934 | 99.9881 |
| No rated evidence | 26 | — | — | — | — |

## Missing levels: None — 38 KPs

| Topic | KP | KP entity | Total | Rated | Unrated | Easy | Moderate | Hard | Easy absence score | Moderate absence score | Hard absence score | Hybrid score |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Calculating Flux Through Cartesian Surfaces | Expressing Flux Over a Surface as a Repeated Integral Using a Formula | 17592186198392 | 12 | 12 | 0 | 5 | 4 | 3 | Observed | Observed | Observed | — |
| Cartesian Equations of Parametric Curves | Finding the Cartesian Equation of a Curve Defined Parametrically | 17592186100889 | 21 | 20 | 1 | 11 | 6 | 3 | Observed | Observed | Observed | — |
| Cartesian Equations of Parametric Curves | Finding the Cartesian Equation of a Curve Defined Parametrically With Trigonometric Functions | 17592186100890 | 20 | 20 | 0 | 11 | 2 | 7 | Observed | Observed | Observed | — |
| Describing Properties of the Cosine Function | Utilizing the Evenness Property of the Cosine Function | 17592186176057 | 6 | 5 | 1 | 3 | 1 | 1 | Observed | Observed | Observed | — |
| Differentiating Logarithmic Functions | Differentiating a Sum Containing a Natural Logarithm Function | 17592186096614 | 11 | 10 | 1 | 6 | 1 | 3 | Observed | Observed | Observed | — |
| Differentiating Parametric Curves | Calculating the Slope of the Tangent to a Parametric Curve at a Given Point | 17592186083243 | 19 | 19 | 0 | 8 | 5 | 6 | Observed | Observed | Observed | — |
| Differentiation Rules for Vector-Valued Functions | Using the Product Rules for Differentiation | 17592186115393 | 13 | 13 | 0 | 4 | 5 | 4 | Observed | Observed | Observed | — |
| Double Integrals Between Polar Curves | Converting an Integral Over an Annular Region to Polar Coordinates | 17592186157300 | 10 | 9 | 1 | 2 | 2 | 5 | Observed | Observed | Observed | — |
| Double Integrals Between Polar Curves | Evaluating a Double Integral Over a Region Enclosed Between Two Curves | 17592186157299 | 12 | 11 | 1 | 5 | 1 | 5 | Observed | Observed | Observed | — |
| Double Integrals in Plane Polar Coordinates | Evaluating a Double Integral by Converting To Polar Coordinates | 17592186129200 | 9 | 9 | 0 | 4 | 3 | 2 | Observed | Observed | Observed | — |
| Factoring Quartic Polynomials Using the Factor Theorem | Factoring a Quartic Polynomial Given Two Roots | 17592186054804 | 7 | 5 | 2 | 3 | 1 | 1 | Observed | Observed | Observed | — |
| Factoring Quartic Polynomials Using the Factor Theorem | Factoring a Quartic Polynomial With Only Two Real Factors | 17592186054805 | 8 | 6 | 2 | 1 | 4 | 1 | Observed | Observed | Observed | — |
| Inhibited Decay Models With First-Order ODEs | Identifying Inhibited Decay Equations and Initial Value Problems | 17592186078582 | 7 | 6 | 1 | 2 | 2 | 2 | Observed | Observed | Observed | — |
| Inhibited Growth Models With First-Order ODEs | Solving an Inhibited Growth Model | 17592186124675 | 9 | 8 | 1 | 3 | 3 | 2 | Observed | Observed | Observed | — |
| Interpreting the Meaning of the Derivative in Context | Interpreting the Derivative of a Function in a Given Context | 17592186064153 | 6 | 5 | 1 | 1 | 3 | 1 | Observed | Observed | Observed | — |
| Introduction to First-Order Linear ODEs | Identifying First-Order Linear ODEs | 17592186087867 | 12 | 12 | 0 | 4 | 5 | 3 | Observed | Observed | Observed | — |
| Introduction to Integration by Parts | Using Integration by Parts to Compute an Indefinite Integral Containing a Trigonometric Expression | 17592186064246 | 15 | 15 | 0 | 8 | 6 | 1 | Observed | Observed | Observed | — |
| Introduction to Integration by Parts | Using Integration by Parts to Compute an Indefinite Integral Containing an Exponential Expression | 17592186064245 | 14 | 13 | 1 | 2 | 6 | 5 | Observed | Observed | Observed | — |
| Linear Equations With No Solutions | Solving For an Unknown Parameter | 17592186204090 | 6 | 5 | 1 | 1 | 2 | 2 | Observed | Observed | Observed | — |
| Parametric Equations of Circles | Parametrizing Part of a Circle | 17592186087784 | 15 | 14 | 1 | 10 | 2 | 2 | Observed | Observed | Observed | — |
| Parametric Equations of Ellipses | Parametrizing Part of an Ellipse | 17592186152190 | 18 | 18 | 0 | 8 | 5 | 5 | Observed | Observed | Observed | — |
| Perpendicular Lines in the Coordinate Plane | Determining Unknown Parameters Given Two Perpendicular Lines | 17592186110601 | 11 | 8 | 3 | 1 | 4 | 3 | Observed | Observed | Observed | — |
| Solving Exponential Equations With Different Bases | Solving Exponential Equations Containing Different Bases by Rewriting One Exponent | 17592186115200 | 9 | 7 | 2 | 3 | 1 | 3 | Observed | Observed | Observed | — |
| Solving Exponential Equations With Different Bases | Solving Exponential Equations Containing Different Bases by Rewriting Two Exponents | 17592186115219 | 12 | 10 | 2 | 3 | 4 | 3 | Observed | Observed | Observed | — |
| Solving First-Order IVPs Using Separation of Variables | Finding Particular Solutions of Differential Equations by Separating the Variables | 17592186100893 | 20 | 20 | 0 | 8 | 7 | 5 | Observed | Observed | Observed | — |
| Solving First-Order Linear ODEs Using Integrating Factors | Solving First-Order Linear ODEs Using Integrating Factors | 17592186087878 | 9 | 6 | 3 | 2 | 3 | 1 | Observed | Observed | Observed | — |
| Solving First-Order Linear ODEs With Exponential Forcing | Finding a Particular Solution to a First-Order Inhomogeneous ODE With Exponential Forcing | 17592186229162 | 10 | 8 | 2 | 4 | 3 | 1 | Observed | Observed | Observed | — |
| The Arc Length of a Parametric Curve | Finding the Arc Length of a Parametric Curve | 17592186092377 | 18 | 18 | 0 | 10 | 5 | 3 | Observed | Observed | Observed | — |
| The Arc Length of a Vector-Valued Function | Computing the Arc Length of a Three-Dimensional Spatial Curve | 17592186119860 | 10 | 9 | 1 | 7 | 1 | 1 | Observed | Observed | Observed | — |
| The Chain Rule for Differentiation | Differentiating a Polynomial Raised to a Power Using the Chain Rule | 17592186096841 | 9 | 8 | 1 | 3 | 3 | 2 | Observed | Observed | Observed | — |
| The Chain Rule for Differentiation | Differentiating a Radical Function Using the Chain Rule | 17592186096842 | 9 | 8 | 1 | 2 | 4 | 2 | Observed | Observed | Observed | — |
| The Determinant of a 2x2 Matrix | Solving for an Unknown in an Expression Involving the Determinant of a 2x2 Matrix | 17592186059750 | 15 | 13 | 2 | 6 | 6 | 1 | Observed | Observed | Observed | — |
| The Determinant of a 3x3 Matrix | Solving for an Unknown Given the Determinant | 17592186059849 | 24 | 22 | 2 | 11 | 10 | 1 | Observed | Observed | Observed | — |
| The Divergence of a Vector Field | Interpreting Divergence | 17592186133880 | 14 | 14 | 0 | 5 | 7 | 2 | Observed | Observed | Observed | — |
| Vertical Asymptotes of Rational Functions | Calculating Vertical Asymptotes When the Denominator Has Complex Roots | 17592186087844 | 13 | 13 | 0 | 3 | 7 | 3 | Observed | Observed | Observed | — |
| Vertical Asymptotes of Rational Functions | Calculating Vertical Asymptotes With Common Factors When the Denominator Has Complex Roots | 17592186087845 | 10 | 8 | 2 | 1 | 3 | 4 | Observed | Observed | Observed | — |
| Vertical Asymptotes of Rational Functions | Calculating Vertical Asymptotes With Common Factors in the Numerator and Denominator | 17592186087843 | 13 | 10 | 3 | 1 | 5 | 4 | Observed | Observed | Observed | — |
| Vertical Asymptotes of Rational Functions | Calculating the Vertical Asymptotes of a Rational Function | 17592186087842 | 10 | 7 | 3 | 4 | 2 | 1 | Observed | Observed | Observed | — |

## Missing levels: Easy — 67 KPs

| Topic | KP | KP entity | Total | Rated | Unrated | Easy | Moderate | Hard | Easy absence score | Moderate absence score | Hard absence score | Hybrid score |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Calculating Flux Through Cartesian Surfaces | Evaluating Flux Over a Surface | 17592186198379 | 12 | 12 | 0 | 0 | 6 | 6 | 99.9169 | Observed | Observed | 99.9169 |
| Calculating Flux Through Parametric Surfaces | Evaluating Flux Through a Surface | 17592186198380 | 11 | 11 | 0 | 0 | 6 | 5 | 99.8499 | Observed | Observed | 99.8499 |
| Calculating Slopes of Circles, Ellipses, and Parabolas | Calculating the Slope of the Tangent to a Parabola | 17592186166867 | 10 | 8 | 2 | 0 | 4 | 4 | 99.1160 | Observed | Observed | 99.1160 |
| Calculating Tangent and Normal Lines with Parametric Equations | Computing the Normal Line to a Parametric Curve | 17592186083245 | 8 | 7 | 1 | 0 | 5 | 2 | 98.4035 | Observed | Observed | 98.4035 |
| Calculating Tangent and Normal Lines with Parametric Equations | Computing the Tangent Line to a Parametric Curve | 17592186083244 | 6 | 5 | 1 | 0 | 2 | 3 | 94.7935 | Observed | Observed | 94.7935 |
| Calculating the Cross Product Using Determinants | Solving for an Unknown in an Equation Involving the Cross Product | 17592186059737 | 21 | 20 | 1 | 0 | 9 | 11 | 99.9993 | Observed | Observed | 99.9993 |
| Calculating the Magnitude of Cartesian Vectors in 2D | Calculating a Unit Vector Parallel to a Given Vector | 17592186059716 | 5 | 3 | 2 | 0 | 2 | 1 | 83.0204 | Observed | Observed | 83.0204 |
| Combining Graph Transformations of Reciprocal Functions | Graphing a Transformed Reciprocal Function | 17592186068779 | 10 | 8 | 2 | 0 | 4 | 4 | 99.1160 | Observed | Observed | 99.1160 |
| Combining Graph Transformations of Reciprocal Functions | Solving for Some Unknowns Given the Graph of a Transformed Reciprocal Function | 17592186068780 | 8 | 7 | 1 | 0 | 4 | 3 | 98.4035 | Observed | Observed | 98.4035 |
| Combining Graph Transformations of Tangent and Cotangent | Identifying the Horizontal Shift of a Horizontally Stretched Tangent or Cotangent Curve | 17592186184149 | 14 | 14 | 0 | 0 | 11 | 3 | 99.9745 | Observed | Observed | 99.9745 |
| Computing Areas Using a Change of Variables | Mapping an Area to a Rectangular Region: Transformations Not Given | 17592186129262 | 6 | 5 | 1 | 0 | 3 | 2 | 94.7935 | Observed | Observed | 94.7935 |
| Computing Triple Integrals Using a Change of Variables | Computing the Volume of a Region Using a Change of Variables | 17592186198399 | 6 | 5 | 1 | 0 | 3 | 2 | 94.7935 | Observed | Observed | 94.7935 |
| Converting from Polar Coordinates to Cartesian Coordinates | Finding the Cartesian Coordinates of a Point Given Some Information About Another Point | 17592186092219 | 10 | 8 | 2 | 0 | 6 | 2 | 99.1160 | Observed | Observed | 99.1160 |
| Describing Properties of the Cosine Function | Utilizing the Periodicity Property of the Cosine Function | 17592186176048 | 7 | 5 | 2 | 0 | 4 | 1 | 94.7935 | Observed | Observed | 94.7935 |
| Describing the Position Vector of a Point Using Known Vectors | Finding a Scalar Factor When Direction Reverses | 17592186235285 | 14 | 14 | 0 | 0 | 7 | 7 | 99.9745 | Observed | Observed | 99.9745 |
| Directional Derivatives | Finding the Rate of Change of a Function in a Given Direction | 17592186124460 | 7 | 5 | 2 | 0 | 3 | 2 | 94.7935 | Observed | Observed | 94.7935 |
| Double Integrals in Plane Polar Coordinates | Rewriting a Double Integral Over a Circle or Part-Circle Not Centered at the Origin | 17592186129275 | 10 | 8 | 2 | 0 | 3 | 5 | 99.1160 | Observed | Observed | 99.1160 |
| Equations of Circles | Finding the Equation of a Circle Given the Endpoints of a Diameter | 17592186087657 | 9 | 7 | 2 | 0 | 3 | 4 | 98.4035 | Observed | Observed | 98.4035 |
| Extending Green's Theorem | Applying Green's Theorem to Regions With Holes: Advanced Cases | 17592186133900 | 11 | 11 | 0 | 0 | 6 | 5 | 99.8499 | Observed | Observed | 99.8499 |
| Finding Points on Transformed Curves | Finding a Point That Lies on a Transformed Curve Given Another Transformed Curve | 17592186059669 | 13 | 11 | 2 | 0 | 8 | 3 | 99.8499 | Observed | Observed | 99.8499 |
| Gaussian Elimination For NxM Systems of Equations | Determining the Value of a Constant for Which a Given Linear System Is Consistent or Inconsistent | 17592186115242 | 15 | 15 | 0 | 0 | 8 | 7 | 99.9859 | Observed | Observed | 99.9859 |
| Gradient Vector Fields | Using the Relationship Between the Vector Field of a Function and Its Contour Plot | 17592186179712 | 11 | 11 | 0 | 0 | 6 | 5 | 99.8499 | Observed | Observed | 99.8499 |
| Graphing General Polynomials | Identifying the Graph of a Factored Polynomial | 17592186129147 | 7 | 7 | 0 | 0 | 5 | 2 | 98.4035 | Observed | Observed | 98.4035 |
| Green's Theorem in Polar Coordinates | Evaluating a Line Integral Using Green's Theorem | 17592186176023 | 10 | 9 | 1 | 0 | 6 | 3 | 99.5105 | Observed | Observed | 99.5105 |
| Inhibited Growth Models With First-Order ODEs | Identifying Inhibited Growth Equations and Initial Value Problems | 17592186124673 | 6 | 5 | 1 | 0 | 1 | 4 | 94.7935 | Observed | Observed | 94.7935 |
| Interpreting the Meaning of the Derivative in Context | Interpreting the Derivative of a Function | 17592186064152 | 7 | 6 | 1 | 0 | 3 | 3 | 97.1169 | Observed | Observed | 97.1169 |
| Introduction to Green's Theorem | Expressing a Line Integral as a Repeated Integral Using Green's Theorem | 17592186133884 | 13 | 13 | 0 | 0 | 11 | 2 | 99.9540 | Observed | Observed | 99.9540 |
| Invertible Functions | Identifying the Intervals on Which a Function is Invertible Given Its Graph | 17592186124473 | 13 | 13 | 0 | 0 | 6 | 7 | 99.9540 | Observed | Observed | 99.9540 |
| Line Integrals With Respect to X and Y | Evaluating Line Integrals With Respect to X and Y | 17592186133893 | 11 | 11 | 0 | 0 | 8 | 3 | 99.8499 | Observed | Observed | 99.8499 |
| Line Integrals of Scalar Functions | Evaluating the Line Integral of a Scalar Function Using a Substitution | 17592186133827 | 6 | 5 | 1 | 0 | 4 | 1 | 94.7935 | Observed | Observed | 94.7935 |
| Line Integrals of Scalar Functions Over Paths Expressed as Functions of X | Computing a Line Integral of a Scalar Function Along a Curve Given in Explicit Cartesian Form | 17592186152158 | 8 | 7 | 1 | 0 | 3 | 4 | 98.4035 | Observed | Observed | 98.4035 |
| Line Integrals of Scalar Functions Over Paths Expressed as Functions of Y | Evaluating the Line Integral of a Function Over Curve Expressed as a Function of Y | 17592186179718 | 6 | 5 | 1 | 0 | 3 | 2 | 94.7935 | Observed | Observed | 94.7935 |
| Modeling Mixture Problems With First-Order Linear ODEs | Constructing and Solving a Dilution Model | 17592186229182 | 7 | 5 | 2 | 0 | 2 | 3 | 94.7935 | Observed | Observed | 94.7935 |
| Parametric Equations of Circles | Finding the Cartesian Equation of a Parametrized Circle | 17592186087786 | 16 | 15 | 1 | 0 | 4 | 11 | 99.9859 | Observed | Observed | 99.9859 |
| Parametric Equations of Ellipses | The Cartesian Equation of an Ellipse | 17592186152188 | 15 | 15 | 0 | 0 | 10 | 5 | 99.9859 | Observed | Observed | 99.9859 |
| Parametric Equations of Ellipses | The Parametric Equations of an Ellipse Centered at a General Point | 17592186152189 | 15 | 14 | 1 | 0 | 5 | 9 | 99.9745 | Observed | Observed | 99.9745 |
| Simplifying Expressions Using the Pythagorean Identity | Simplifying a Rational Expression Using the Pythagorean Identity | 17592186059642 | 10 | 8 | 2 | 0 | 5 | 3 | 99.1160 | Observed | Observed | 99.1160 |
| Simplifying Expressions Using the Pythagorean Identity | Simplifying a Trigonometric Expression Using a Common Denominator and the Pythagorean Identity | 17592186059643 | 11 | 9 | 2 | 0 | 8 | 1 | 99.5105 | Observed | Observed | 99.5105 |
| Slope Fields for Nonautonomous Differential Equations | Identifying Quadrants Where a Slope Field Is Positive or Negative | 17592186172039 | 8 | 7 | 1 | 0 | 5 | 2 | 98.4035 | Observed | Observed | 98.4035 |
| Slope Fields for Nonautonomous Differential Equations | Identifying Rectangular Regions Where a Slope Field Is Positive or Negative | 17592186172041 | 7 | 6 | 1 | 0 | 3 | 3 | 97.1169 | Observed | Observed | 97.1169 |
| Slope Fields for Nonautonomous Differential Equations | Identifying a Possible Slope Field Based on the Type of Equation | 17592186172040 | 8 | 7 | 1 | 0 | 3 | 4 | 98.4035 | Observed | Observed | 98.4035 |
| Solving First-Order Linear ODEs Using Integrating Factors | Solving First-Order Initial Value Problems Using Integrating Factors | 17592186087879 | 9 | 8 | 1 | 0 | 6 | 2 | 99.1160 | Observed | Observed | 99.1160 |
| Solving First-Order ODEs Using Separation of Variables | Finding General Solutions by Rearranging Then Integrating | 17592186068841 | 14 | 14 | 0 | 0 | 8 | 6 | 99.9745 | Observed | Observed | 99.9745 |
| Stokes' Theorem | Evaluating a Line Integral Using Stokes' Theorem | 17592186133927 | 11 | 10 | 1 | 0 | 5 | 5 | 99.7289 | Observed | Observed | 99.7289 |
| Stokes' Theorem | Evaluating a Surface Integral Using Stokes' Theorem | 17592186133928 | 11 | 10 | 1 | 0 | 5 | 5 | 99.7289 | Observed | Observed | 99.7289 |
| Sums of Line Integrals With Respect to X and Y | Evaluating Line Integrals With Respect to X and Y Along Cartesian Curves | 17592186179674 | 11 | 11 | 0 | 0 | 8 | 3 | 99.8499 | Observed | Observed | 99.8499 |
| Surface Integrals Over Parametric Surfaces | Evaluating Surface Integrals Over Parametric Surfaces | 17592186172131 | 13 | 13 | 0 | 0 | 7 | 6 | 99.9540 | Observed | Observed | 99.9540 |
| The Arc Length of a Parametric Curve | Finding an Integral Expression For the Arc Length of a Parametric Curve Containing Special Functions | 17592186092376 | 12 | 11 | 1 | 0 | 9 | 2 | 99.8499 | Observed | Observed | 99.8499 |
| The Chain Rule for Differentiation | Differentiating a Function Using the Chain Rule and Prime Notation | 17592186096843 | 9 | 7 | 2 | 0 | 4 | 3 | 98.4035 | Observed | Observed | 98.4035 |
| The Curl of a Vector Field | Interpreting the Curl of a Vector Field | 17592186133881 | 12 | 11 | 1 | 0 | 6 | 5 | 99.8499 | Observed | Observed | 99.8499 |
| The Fundamental Theorem for Line Integrals | Applying the Fundamental Theorem of Line Integrals When the Potential Function Is Not Given | 17592186133879 | 12 | 12 | 0 | 0 | 6 | 6 | 99.9169 | Observed | Observed | 99.9169 |
| The Gradient Vector | Calculating the Gradient Using the Properties of the Gradient | 17592186124447 | 9 | 8 | 1 | 0 | 6 | 2 | 99.1160 | Observed | Observed | 99.1160 |
| The Gradient Vector | Finding the Points Where a Gradient Vanishes | 17592186124445 | 10 | 10 | 0 | 0 | 5 | 5 | 99.7289 | Observed | Observed | 99.7289 |
| The Gradient as a Normal Vector | Finding the Equation of the Normal Line to a Plane Curve Using the Gradient | 17592186124462 | 15 | 14 | 1 | 0 | 11 | 3 | 99.9745 | Observed | Observed | 99.9745 |
| The Gradient as a Normal Vector | Finding the Equation of the Normal Line to a Surface Using the Gradient | 17592186124464 | 14 | 14 | 0 | 0 | 6 | 8 | 99.9745 | Observed | Observed | 99.9745 |
| The Jacobian of a Three-Dimensional Transformation | Finding the Jacobian of an Inverse Transformation | 17592186129269 | 12 | 12 | 0 | 0 | 6 | 6 | 99.9169 | Observed | Observed | 99.9169 |
| The Multivariable Chain Rule | Calculating the Derivative of a Function of Three Intermediate Variables and Two Independent Variables | 17592186166750 | 12 | 12 | 0 | 0 | 6 | 6 | 99.9169 | Observed | Observed | 99.9169 |
| The Multivariable Chain Rule | Calculating the Derivative of a Multivariable Function With Two Independent Variables | 17592186166749 | 11 | 11 | 0 | 0 | 6 | 5 | 99.8499 | Observed | Observed | 99.8499 |
| The Multivariable Chain Rule in Vector Form | Applying the Vector Form of the Chain Rule to a Function of Three Variables | 17592186124470 | 8 | 6 | 2 | 0 | 5 | 1 | 97.1169 | Observed | Observed | 97.1169 |
| The Multivariable Chain Rule in Vector Form | Computing the Rate of Change of a Multivariable Function at a Point Using the Chain Rule | 17592186124471 | 8 | 6 | 2 | 0 | 3 | 3 | 97.1169 | Observed | Observed | 97.1169 |
| Triangular Matrices | Identifying Correct Statements About a Matrix | 17592186119784 | 10 | 9 | 1 | 0 | 5 | 4 | 99.5105 | Observed | Observed | 99.5105 |
| Triple Integrals in Cylindrical Polar Coordinates | Evaluating a Triple Integral by Converting to Cylindrical Coordinates | 17592186129278 | 10 | 8 | 2 | 0 | 3 | 5 | 99.1160 | Observed | Observed | 99.1160 |
| Triple Integrals in Cylindrical Polar Coordinates | Rewriting a Triple Integral Defined Over a Shifted Cylindrical Solid | 17592186129268 | 6 | 4 | 2 | 0 | 1 | 3 | 90.5977 | Observed | Observed | 90.5977 |
| Using Green's Theorem to Calculate Area | Calculating an Area Using Green's Theorem | 17592186133897 | 8 | 7 | 1 | 0 | 4 | 3 | 98.4035 | Observed | Observed | 98.4035 |
| Using Green's Theorem to Calculate Area | Expressing the Area Bounded by a Closed Curve Using Green’s Theorem | 17592186133896 | 8 | 7 | 1 | 0 | 1 | 6 | 98.4035 | Observed | Observed | 98.4035 |
| Vector Fields | Finding the Domain of a Vector Field | 17592186172086 | 9 | 9 | 0 | 0 | 4 | 5 | 99.5105 | Observed | Observed | 99.5105 |
| Visualizing Vector Fields | Identifying a Three-Dimensional Vector Field | 17592186172088 | 10 | 10 | 0 | 0 | 7 | 3 | 99.7289 | Observed | Observed | 99.7289 |

## Missing levels: Moderate — 6 KPs

| Topic | KP | KP entity | Total | Rated | Unrated | Easy | Moderate | Hard | Easy absence score | Moderate absence score | Hard absence score | Hybrid score |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Describing Properties of the Cosecant Function | Utilizing the Oddness Property of the Cosecant Function | 17592186176060 | 7 | 5 | 2 | 3 | 0 | 2 | Observed | 92.5497 | Observed | 92.5497 |
| Describing Properties of the Tangent Function | Utilizing the Oddness Property of the Tangent Function | 17592186176058 | 6 | 5 | 1 | 3 | 0 | 2 | Observed | 92.5497 | Observed | 92.5497 |
| Differentiating Logarithmic Functions | Differentiating a Logarithmic Function With a General Base | 17592186096615 | 12 | 10 | 2 | 9 | 0 | 1 | Observed | 99.4449 | Observed | 99.4449 |
| Introduction to First-Order Linear ODEs | Writing First-Order Linear ODEs in Standard Form | 17592186087866 | 9 | 9 | 0 | 8 | 0 | 1 | Observed | 99.0669 | Observed | 99.0669 |
| The Antiderivative | Finding the Antiderivative of a Radical Function | 17592186064168 | 8 | 6 | 2 | 4 | 0 | 2 | Observed | 95.5679 | Observed | 95.5679 |
| The Least Common Multiple of Two Polynomials | Finding the LCM of Two Single-Variable Polynomials | 17592186152117 | 7 | 5 | 2 | 2 | 0 | 3 | Observed | 92.5497 | Observed | 92.5497 |

## Missing levels: Hard — 124 KPs

| Topic | KP | KP entity | Total | Rated | Unrated | Easy | Moderate | Hard | Easy absence score | Moderate absence score | Hard absence score | Hybrid score |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Calculating Flux Through Parametric Surfaces | Expressing Flux Through a Surface as a Double Integral | 17592186198378 | 10 | 10 | 0 | 5 | 5 | 0 | Observed | Observed | 79.9934 | 79.9934 |
| Calculating Slopes of Circles, Ellipses, and Parabolas | Calculating the Slope of the Tangent to a Circle | 17592186166865 | 7 | 5 | 2 | 1 | 4 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Calculating Slopes of Circles, Ellipses, and Parabolas | Calculating the Slope of the Tangent to an Ellipse | 17592186166866 | 9 | 7 | 2 | 4 | 3 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Calculating Tangent and Normal Lines with Parametric Equations | Determining the Points Where the Normal is Horizontal or Vertical | 17592186083280 | 7 | 6 | 1 | 3 | 3 | 0 | Observed | Observed | 61.9193 | 61.9193 |
| Calculating Tangent and Normal Lines with Parametric Equations | Determining the Points Where the Tangent is Horizontal or Vertical | 17592186083278 | 8 | 7 | 1 | 5 | 2 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Calculating a Scalar Projection | Calculating a Scalar Projection Using Components | 17592186105917 | 24 | 23 | 1 | 14 | 9 | 0 | Observed | Observed | 97.5300 | 97.5300 |
| Calculating the Dot Product Using Components | Solving for an Unknown Given Two Perpendicular Vectors | 17592186059731 | 8 | 6 | 2 | 3 | 3 | 0 | Observed | Observed | 61.9193 | 61.9193 |
| Combining Graph Transformations of Reciprocal Functions | Graphing a Stretched Negative Reciprocal Function | 17592186068814 | 9 | 7 | 2 | 3 | 4 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Combining Graph Transformations of Reciprocal Functions | Graphing a Stretched Reciprocal Function | 17592186068813 | 5 | 5 | 0 | 3 | 2 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Completing the Square | Completing the Square When the Perfect Square is Isolated | 17592186068873 | 8 | 5 | 3 | 3 | 2 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Completing the Square | Completing the Square When the Perfect Square is Isolated: Negative Linear Term | 17592186068874 | 8 | 6 | 2 | 5 | 1 | 0 | Observed | Observed | 61.9193 | 61.9193 |
| Completing the Square | Completing the Square on a Quadratic Expression | 17592186068875 | 9 | 7 | 2 | 5 | 2 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Completing the Square | Completing the Square on a Quadratic Expression with a Negative Linear Term | 17592186068876 | 10 | 8 | 2 | 5 | 3 | 0 | Observed | Observed | 72.3981 | 72.3981 |
| Computing Areas Using a Change of Variables | Mapping an Area to a Rectangular Region: Transformations Given | 17592186129261 | 4 | 2 | 2 | 1 | 1 | 0 | Observed | Observed | 27.5172 | 27.5172 |
| Computing Double Integrals Using a Change of Variables | Performing a Change of Variables | 17592186198361 | 7 | 5 | 2 | 4 | 1 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Conservative Vector Fields in the Cartesian Plane | Identifying the Vector Field Corresponding to a Given Potential Function | 17592186166846 | 9 | 9 | 0 | 5 | 4 | 0 | Observed | Observed | 76.5006 | 76.5006 |
| Converting from Polar Coordinates to Cartesian Coordinates | Finding the Cartesian Coordinates of a Point Given in Polar Coordinates | 17592186092217 | 7 | 5 | 2 | 4 | 1 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Describing Properties of the Cosecant Function | Utilizing the Periodicity Property of the Cosecant Function | 17592186176054 | 7 | 5 | 2 | 2 | 3 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Describing the Position Vector of a Point Using Known Vectors | Finding Two Scalar Factors in a Linear Combination | 17592186096652 | 21 | 21 | 0 | 2 | 19 | 0 | Observed | Observed | 96.5923 | 96.5923 |
| Describing the Position Vector of a Point Using Known Vectors | Finding a Scalar Factor in a Linear Combination | 17592186096701 | 14 | 14 | 0 | 7 | 7 | 0 | Observed | Observed | 89.4890 | 89.4890 |
| Determining Continuity from Graphs | Determining Whether a Function Is Continuous at a Given Point | 17592186068695 | 9 | 9 | 0 | 4 | 5 | 0 | Observed | Observed | 76.5006 | 76.5006 |
| Differentiating Exponential Functions | Differentiating an Exponential Function with a Base Other Than e | 17592186096612 | 7 | 5 | 2 | 3 | 2 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Differentiating Exponential Functions | Differentiating the Product of a Constant and the Exponential Function, Plus a Polynomial | 17592186096611 | 9 | 7 | 2 | 5 | 2 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Differentiating Parametric Curves | Finding the Derivative of a Parametric Curve | 17592186083240 | 18 | 18 | 0 | 12 | 6 | 0 | Observed | Observed | 94.4778 | 94.4778 |
| Differentiation Rules for Vector-Valued Functions | Using the Scalar Function Multiple Rule for Differentiation | 17592186115391 | 14 | 13 | 1 | 9 | 4 | 0 | Observed | Observed | 87.6540 | 87.6540 |
| Differentiation Rules for Vector-Valued Functions | Using the Sum and Constant Multiple Rules for Differentiation | 17592186115390 | 11 | 10 | 1 | 6 | 4 | 0 | Observed | Observed | 79.9934 | 79.9934 |
| Directional Derivatives | Calculating a Directional Derivative | 17592186124458 | 8 | 6 | 2 | 5 | 1 | 0 | Observed | Observed | 61.9193 | 61.9193 |
| Directional Derivatives | Finding the Direction of Maximum Increase or Maximum Decrease of a Function | 17592186124459 | 6 | 5 | 1 | 3 | 2 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Double Integrals in Plane Polar Coordinates | Evaluating Repeated Integrals Expressed in Polar Coordinates | 17592186129198 | 10 | 9 | 1 | 4 | 5 | 0 | Observed | Observed | 76.5006 | 76.5006 |
| Double Integrals in Plane Polar Coordinates | Rewriting a Double Integral Over a Circle or Part-Circle Centered at the Origin | 17592186129199 | 9 | 8 | 1 | 3 | 5 | 0 | Observed | Observed | 72.3981 | 72.3981 |
| Equations of Ellipses Centered at the Origin | Determining the Equation of a Tall Ellipse | 17592186087840 | 22 | 21 | 1 | 14 | 7 | 0 | Observed | Observed | 96.5923 | 96.5923 |
| Equations of Ellipses Centered at the Origin | Determining the Equation of a Wide Ellipse | 17592186087839 | 12 | 12 | 0 | 6 | 6 | 0 | Observed | Observed | 85.4986 | 85.4986 |
| Extending Green's Theorem | Applying Green's Theorem to Regions With Holes | 17592186133886 | 8 | 7 | 1 | 3 | 4 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Extending Green's Theorem | Calculating the Circulation of a Vector Field Over a Region Containing Holes | 17592186133899 | 11 | 10 | 1 | 4 | 6 | 0 | Observed | Observed | 79.9934 | 79.9934 |
| Factoring Quartic Polynomials Using the Factor Theorem | Factoring a Quartic Polynomial Given Two Factors | 17592186054803 | 8 | 5 | 3 | 3 | 2 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Finding Areas Using the Cross Product | Calculating the Area of the Triangle Spanned by Two Vectors | 17592186105732 | 11 | 10 | 1 | 6 | 4 | 0 | Observed | Observed | 79.9934 | 79.9934 |
| Finding Points on Transformed Curves | Finding a Point That Lies on a Transformed Curve | 17592186059668 | 9 | 9 | 0 | 6 | 3 | 0 | Observed | Observed | 76.5006 | 76.5006 |
| Finding Points on Transformed Curves | Identifying Extrema on Transformed Curves | 17592186059670 | 12 | 12 | 0 | 6 | 6 | 0 | Observed | Observed | 85.4986 | 85.4986 |
| Gradient Vector Fields | Calculating the Gradient Vector Field of a Function | 17592186179714 | 9 | 8 | 1 | 3 | 5 | 0 | Observed | Observed | 72.3981 | 72.3981 |
| Graphing Curves Defined Parametrically | Determining the Range of a Parametric Equation Defined in Terms of Trigonometric Functions | 17592186087736 | 16 | 15 | 1 | 8 | 7 | 0 | Observed | Observed | 91.0513 | 91.0513 |
| Graphing General Polynomials | Identifying True Statements Regarding the Graph of a Given Polynomial | 17592186129154 | 10 | 8 | 2 | 5 | 3 | 0 | Observed | Observed | 72.3981 | 72.3981 |
| Graphing General Polynomials | Identifying the Factored Polynomial Shown in a Graph | 17592186129145 | 10 | 9 | 1 | 4 | 5 | 0 | Observed | Observed | 76.5006 | 76.5006 |
| Green's Theorem in Polar Coordinates | Expressing a Line Integral Along a Circular Path as a Double Integral Using Green's Theorem | 17592186176024 | 8 | 7 | 1 | 4 | 3 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Inhibited Decay Models With First-Order ODEs | Modeling Inhibited Decay | 17592186078583 | 8 | 7 | 1 | 2 | 5 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Inhibited Decay Models With First-Order ODEs | Solving an Inhibited Decay Model | 17592186078584 | 8 | 8 | 0 | 4 | 4 | 0 | Observed | Observed | 72.3981 | 72.3981 |
| Interpreting the Meaning of the Derivative in Context | Determining a Rate of Change | 17592186064154 | 11 | 9 | 2 | 7 | 2 | 0 | Observed | Observed | 76.5006 | 76.5006 |
| Interpreting the Meaning of the Derivative in Context | Relating a Derivative to a Rate of Change | 17592186064272 | 9 | 8 | 1 | 7 | 1 | 0 | Observed | Observed | 72.3981 | 72.3981 |
| Introduction to Differential Equations | Determining Whether an Ordinary Differential Equation is Autonomous or Nonautonomous | 17592186166814 | 15 | 15 | 0 | 8 | 7 | 0 | Observed | Observed | 91.0513 | 91.0513 |
| Introduction to Differential Equations | Identifying the Order of an Ordinary Differential Equation | 17592186166813 | 14 | 14 | 0 | 7 | 7 | 0 | Observed | Observed | 89.4890 | 89.4890 |
| Introduction to First-Order Linear ODEs | Identifying Homogeneous and Inhomogeneous ODEs | 17592186087868 | 12 | 12 | 0 | 6 | 6 | 0 | Observed | Observed | 85.4986 | 85.4986 |
| Introduction to Matrices | Matrices for Route Planning | 17592186087819 | 7 | 5 | 2 | 4 | 1 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Invertible Functions | Identifying an Invertible Function From Its Graph | 17592186124472 | 10 | 8 | 2 | 5 | 3 | 0 | Observed | Observed | 72.3981 | 72.3981 |
| Invertible Functions | Identifying the Intervals on Which a Function is Invertible Given a Description | 17592186124474 | 12 | 12 | 0 | 4 | 8 | 0 | Observed | Observed | 85.4986 | 85.4986 |
| Line Integrals of Scalar Functions | Evaluating the Line Integral of a Scalar Function | 17592186133830 | 7 | 5 | 2 | 2 | 3 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Line Integrals of Scalar Functions | Writing the Line Integral of a Scalar Function as a Definite Integral | 17592186133829 | 6 | 5 | 1 | 1 | 4 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Line Integrals of Scalar Functions Over Paths Expressed as Functions of Y | Constructing the Line Integral of a Function Over Curve Expressed as a Function of Y | 17592186179709 | 7 | 5 | 2 | 2 | 3 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Linear Equations With Infinitely Many Solutions | Solving For an Unknown Parameter | 17592186110720 | 5 | 5 | 0 | 4 | 1 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Linear Equations With Infinitely Many Solutions | Solving a General Equation With Infinitely Many Solutions For Unknown Parameters | 17592186110721 | 7 | 5 | 2 | 3 | 2 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Linear Equations With No Solutions | Solving For an Unknown Parameter - Constants on Both Sides | 17592186204091 | 6 | 5 | 1 | 3 | 2 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Linear Equations With No Solutions | Solving For an Unknown Parameter - Variables and Constants on Both Sides | 17592186204092 | 7 | 5 | 2 | 1 | 4 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Modeling Mixture Problems With First-Order Linear ODEs | Constructing and Solving a Dilution Model: Inflow Equals Outflow | 17592186229181 | 7 | 5 | 2 | 3 | 2 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Parametric Equations of Circles | Finding the Parametric Equations of a Circle Centered at a General Point | 17592186087743 | 13 | 12 | 1 | 5 | 7 | 0 | Observed | Observed | 85.4986 | 85.4986 |
| Parametric Equations of Circles | Finding the Parametric Equations of a Circle Centered at the Origin | 17592186087742 | 12 | 10 | 2 | 5 | 5 | 0 | Observed | Observed | 79.9934 | 79.9934 |
| Parametric Equations of Ellipses | The Parametric Equations of an Ellipse Centered at the Origin | 17592186152187 | 13 | 12 | 1 | 5 | 7 | 0 | Observed | Observed | 85.4986 | 85.4986 |
| Perpendicular Lines in the Coordinate Plane | Determining Whether Two Lines in Slope-Intercept Form are Perpendicular | 17592186110599 | 7 | 5 | 2 | 4 | 1 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Perpendicular Lines in the Coordinate Plane | Determining Whether Two Lines in Standard Form are Perpendicular | 17592186110600 | 8 | 8 | 0 | 5 | 3 | 0 | Observed | Observed | 72.3981 | 72.3981 |
| Properties of Transformed Sine and Cosine Functions | Determining the Amplitude of a Transformed Sinusoidal Function | 17592186129121 | 9 | 7 | 2 | 4 | 3 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Properties of Transformed Sine and Cosine Functions | Finding the Range of a Transformed Sinusoidal Function | 17592186129124 | 9 | 7 | 2 | 4 | 3 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Simplifying Expressions Using the Pythagorean Identity | Simplifying an Expression by Factoring and Using the Pythagorean Identity | 17592186059641 | 10 | 8 | 2 | 4 | 4 | 0 | Observed | Observed | 72.3981 | 72.3981 |
| Solving Exponential Equations Using the Zero-Product Property | Solving an Exponential Equation by Factoring | 17592186157437 | 14 | 13 | 1 | 5 | 8 | 0 | Observed | Observed | 87.6540 | 87.6540 |
| Solving Exponential Equations Using the Zero-Product Property | Solving an Exponential Equation by Rearranging the Equation and Then Factoring | 17592186157438 | 12 | 10 | 2 | 4 | 6 | 0 | Observed | Observed | 79.9934 | 79.9934 |
| Solving First-Order IVPs Using Separation of Variables | Finding Particular Solutions of Differential Equations by First Rearranging and Then Separating | 17592186100894 | 24 | 24 | 0 | 11 | 13 | 0 | Observed | Observed | 97.8971 | 97.8971 |
| Solving First-Order Linear ODEs Using Integrating Factors | Transforming First-Order Linear ODEs Using Integrating Factors | 17592186087877 | 8 | 6 | 2 | 2 | 4 | 0 | Observed | Observed | 61.9193 | 61.9193 |
| Solving First-Order Linear ODEs With Exponential Forcing | Finding a Particular Solution When the Forcing Term is Part of the Complementary Solution | 17592186229163 | 12 | 12 | 0 | 8 | 4 | 0 | Observed | Observed | 85.4986 | 85.4986 |
| Solving First-Order Linear ODEs With Exponential Forcing | Finding the General Solution to a First-Order Inhomogeneous ODE With Exponential Forcing | 17592186229164 | 10 | 9 | 1 | 5 | 4 | 0 | Observed | Observed | 76.5006 | 76.5006 |
| Solving First-Order Linear ODEs With Exponential Forcing | Solving an Initial Value Problem | 17592186229165 | 15 | 13 | 2 | 6 | 7 | 0 | Observed | Observed | 87.6540 | 87.6540 |
| Solving First-Order ODEs Using Direct Integration | Finding the General Solution of a Differential Equation Using Integration | 17592186096696 | 8 | 7 | 1 | 3 | 4 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Solving First-Order ODEs Using Direct Integration | Finding the General Solution of a Second Order Differential Equation by Integrating Twice | 17592186096697 | 11 | 11 | 0 | 4 | 7 | 0 | Observed | Observed | 82.9670 | 82.9670 |
| Solving First-Order ODEs Using Direct Integration | Finding the Solution of a Differential Equation With a Given Condition | 17592186096699 | 14 | 12 | 2 | 10 | 2 | 0 | Observed | Observed | 85.4986 | 85.4986 |
| Solving First-Order ODEs Using Direct Integration | Sketching the Solution Curves of a Differential Equation | 17592186096698 | 11 | 11 | 0 | 7 | 4 | 0 | Observed | Observed | 82.9670 | 82.9670 |
| Solving First-Order ODEs Using Separation of Variables | Finding a General Solution in Explicit Form | 17592186068840 | 11 | 11 | 0 | 4 | 7 | 0 | Observed | Observed | 82.9670 | 82.9670 |
| Solving First-Order ODEs Using Separation of Variables | Separating the Variables in a Differential Equation | 17592186068842 | 10 | 10 | 0 | 6 | 4 | 0 | Observed | Observed | 79.9934 | 79.9934 |
| Stokes' Theorem | Circulation Over Space Curves | 17592186133926 | 8 | 7 | 1 | 5 | 2 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Sums of Line Integrals With Respect to X and Y | Computing Line Integrals With Respect to X and Y Along Circles and Ellipses | 17592186179673 | 11 | 11 | 0 | 6 | 5 | 0 | Observed | Observed | 82.9670 | 82.9670 |
| Surface Integrals Over Parametric Surfaces | Constructing Surface Integrals Over Parametric Surfaces | 17592186172130 | 12 | 12 | 0 | 6 | 6 | 0 | Observed | Observed | 85.4986 | 85.4986 |
| The Antiderivative | Finding the Antiderivative of a Reciprocal Function | 17592186064169 | 6 | 4 | 2 | 1 | 3 | 0 | Observed | Observed | 47.4625 | 47.4625 |
| The Arc Length of a Vector-Valued Function | Computing the Arc Length of a Planar Curve | 17592186119744 | 10 | 10 | 0 | 5 | 5 | 0 | Observed | Observed | 79.9934 | 79.9934 |
| The Arc Length of a Vector-Valued Function | Finding an Integral Expression For the Arc Length of a Curve | 17592186119743 | 8 | 8 | 0 | 6 | 2 | 0 | Observed | Observed | 72.3981 | 72.3981 |
| The Chain Rule With Exponential Functions | Differentiating a General Exponential Function Using the Chain Rule | 17592186092261 | 10 | 9 | 1 | 7 | 2 | 0 | Observed | Observed | 76.5006 | 76.5006 |
| The Chain Rule With Exponential Functions | Differentiating an Exponential Function with a Linear Exponent | 17592186092260 | 9 | 7 | 2 | 2 | 5 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| The Chain Rule With Exponential Functions | Differentiating an Exponential Function with a Nonlinear Exponent | 17592186092263 | 14 | 13 | 1 | 5 | 8 | 0 | Observed | Observed | 87.6540 | 87.6540 |
| The Curl of a Vector Field | Calculating the Curl of a Vector Field | 17592186133877 | 11 | 9 | 2 | 4 | 5 | 0 | Observed | Observed | 76.5006 | 76.5006 |
| The Curl of a Vector Field | Calculating the Scalar Curl of a Vector Field | 17592186133898 | 15 | 14 | 1 | 7 | 7 | 0 | Observed | Observed | 89.4890 | 89.4890 |
| The Determinant of a 2x2 Matrix | Calculating the Determinant of a 2x2 Matrix With Integer Entries | 17592186059748 | 9 | 8 | 1 | 4 | 4 | 0 | Observed | Observed | 72.3981 | 72.3981 |
| The Determinant of a 2x2 Matrix | Calculating the Determinant of a 2x2 Matrix With Non-Integer Entries | 17592186059749 | 13 | 12 | 1 | 6 | 6 | 0 | Observed | Observed | 85.4986 | 85.4986 |
| The Determinant of a 3x3 Matrix | Identifying Singular Matrices | 17592186059848 | 17 | 17 | 0 | 9 | 8 | 0 | Observed | Observed | 93.5137 | 93.5137 |
| The Divergence Theorem | Calculating Flux Across the Surface of a Known Solid | 17592186133930 | 10 | 10 | 0 | 6 | 4 | 0 | Observed | Observed | 79.9934 | 79.9934 |
| The Divergence Theorem | Writing the Flux Across a Closed Surface as a Triple Integral | 17592186133929 | 8 | 7 | 1 | 3 | 4 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| The Divergence of a Vector Field | Finding the Divergence of a Vector Field in Three Dimensions | 17592186133889 | 16 | 16 | 0 | 9 | 7 | 0 | Observed | Observed | 92.3813 | 92.3813 |
| The Divergence of a Vector Field | Finding the Divergence of a Vector Field in Two Dimensions | 17592186133876 | 14 | 13 | 1 | 7 | 6 | 0 | Observed | Observed | 87.6540 | 87.6540 |
| The Fundamental Theorem for Line Integrals | Applying the Fundamental Theorem of Line Integrals Over Cartesian Curves | 17592186133890 | 12 | 12 | 0 | 6 | 6 | 0 | Observed | Observed | 85.4986 | 85.4986 |
| The Fundamental Theorem for Line Integrals | Applying the Fundamental Theorem of Line Integrals Over Parametric Curves | 17592186133878 | 12 | 12 | 0 | 7 | 5 | 0 | Observed | Observed | 85.4986 | 85.4986 |
| The Gradient Vector | Calculating the Gradient of a Function of Two Variables | 17592186124443 | 11 | 10 | 1 | 5 | 5 | 0 | Observed | Observed | 79.9934 | 79.9934 |
| The Jacobian | Finding the Jacobian Determinant of a Transformation | 17592186129187 | 11 | 10 | 1 | 5 | 5 | 0 | Observed | Observed | 79.9934 | 79.9934 |
| The Jacobian of a Three-Dimensional Transformation | Finding the Jacobian of a Three-Dimensional Transformation | 17592186129271 | 9 | 9 | 0 | 4 | 5 | 0 | Observed | Observed | 76.5006 | 76.5006 |
| The Least Common Multiple of Two Polynomials | Finding the LCM of Three Polynomials | 17592186152119 | 8 | 6 | 2 | 3 | 3 | 0 | Observed | Observed | 61.9193 | 61.9193 |
| The Least Common Multiple of Two Polynomials | Finding the LCM of Two Multivariable Polynomials | 17592186152118 | 6 | 5 | 1 | 3 | 2 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| The Least Common Multiple of Two Polynomials | Finding the LCM of Two Polynomials that Differ by a Constant Factor | 17592186152116 | 7 | 5 | 2 | 2 | 3 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| The Multivariable Chain Rule With Polar Coordinates | Calculating the Derivative of a Cartesian Function With Respect to Cylindrical Polar Coordinates | 17592186124596 | 7 | 7 | 0 | 4 | 3 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| The Multivariable Chain Rule in Vector Form | Evaluating the Derivative at a Point Using the Chain Rule | 17592186124593 | 8 | 8 | 0 | 6 | 2 | 0 | Observed | Observed | 72.3981 | 72.3981 |
| The Scalar Triple Product | Calculating the Scalar Triple Product Using a Determinant | 17592186105736 | 23 | 22 | 1 | 11 | 11 | 0 | Observed | Observed | 97.0988 | 97.0988 |
| The Scalar Triple Product | Calculating the Scalar Triple Product Using the Definition | 17592186105735 | 15 | 15 | 0 | 9 | 6 | 0 | Observed | Observed | 91.0513 | 91.0513 |
| Triangular Matrices | Describing a Triangular Matrix | 17592186119771 | 10 | 9 | 1 | 6 | 3 | 0 | Observed | Observed | 76.5006 | 76.5006 |
| Triangular Matrices | Identifying a Triangular Matrix | 17592186119772 | 8 | 8 | 0 | 6 | 2 | 0 | Observed | Observed | 72.3981 | 72.3981 |
| Triple Integrals in Cylindrical Polar Coordinates | Rewriting a Triple Integral Defined Over a Cylindrical Solid | 17592186129267 | 8 | 7 | 1 | 4 | 3 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Using Green's Theorem to Calculate Area | Identifying Vector Fields That Satisfy the Unit Curl Property | 17592186133895 | 7 | 7 | 0 | 2 | 5 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Using the Pythagorean Identity in the First Quadrant | Computing a Tangent or Cotangent Using the Pythagorean Identity | 17592186110758 | 8 | 7 | 1 | 5 | 2 | 0 | Observed | Observed | 67.5793 | 67.5793 |
| Using the Pythagorean Identity in the First Quadrant | Computing a Trigonometric Ratio Using the Pythagorean Identity | 17592186110755 | 7 | 5 | 2 | 4 | 1 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Verifying Solutions of Differential Equations | Identifying a Solution to a First-Order Differential Equation | 17592186100888 | 9 | 9 | 0 | 8 | 1 | 0 | Observed | Observed | 76.5006 | 76.5006 |
| Vertical Translations of Exponential Growth Functions | Identifying a Vertically Shifted Exponential Growth Curve | 17592186087821 | 7 | 5 | 2 | 3 | 2 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Vertical Translations of Exponential Growth Functions | Identifying a Vertically Shifted and Stretched Exponential Growth Curve | 17592186087823 | 6 | 5 | 1 | 1 | 4 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Vertical Translations of Exponential Growth Functions | Identifying the Shift Applied to an Exponential Growth Curve | 17592186087822 | 8 | 6 | 2 | 5 | 1 | 0 | Observed | Observed | 61.9193 | 61.9193 |
| Vertical Translations of Exponential Growth Functions | Identifying the Shift and Stretch Applied to an Exponential Growth Curve | 17592186087824 | 7 | 5 | 2 | 1 | 4 | 0 | Observed | Observed | 55.2712 | 55.2712 |
| Visualizing Vector Fields | Identifying a Two-Dimensional Vector Field | 17592186172084 | 9 | 8 | 1 | 3 | 5 | 0 | Observed | Observed | 72.3981 | 72.3981 |

## Missing levels: Easy–moderate — 14 KPs

| Topic | KP | KP entity | Total | Rated | Unrated | Easy | Moderate | Hard | Easy absence score | Moderate absence score | Hard absence score | Hybrid score |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Calculating Potential Functions | Reconstructing a Three-Variable Function From Its Gradient | 17592186124574 | 13 | 12 | 1 | 0 | 0 | 12 | 99.9169 | 99.8036 | Observed | >99.9999 |
| Computing Areas Using a Change of Variables | Finding an Area by Transforming to a Type I Region | 17592186129197 | 7 | 6 | 1 | 0 | 0 | 6 | 97.1169 | 95.5679 | Observed | 99.9989 |
| Computing Double Integrals Using a Change of Variables | Cases When the Transformation Is Inferred From the Integrand | 17592186198374 | 6 | 5 | 1 | 0 | 0 | 5 | 94.7935 | 92.5497 | Observed | 99.9927 |
| Converting from Polar Coordinates to Cartesian Coordinates | Finding the Cartesian Coordinates of a Point Using a Diagram | 17592186092273 | 10 | 8 | 2 | 0 | 0 | 8 | 99.1160 | 98.4315 | Observed | >99.9999 |
| Describing Properties of the Tangent Function | Describing Properties of the Tangent Function | 17592186176049 | 6 | 5 | 1 | 0 | 0 | 5 | 94.7935 | 92.5497 | Observed | 99.9927 |
| Finding Areas Using the Cross Product | Calculating the Altitude of a Triangle Given Its Vertices | 17592186105734 | 18 | 17 | 1 | 0 | 0 | 17 | 99.9957 | 99.9854 | Observed | >99.9999 |
| Geometric Interpretations of Partial Derivatives | Finding the Tangent Vector to a Curve at a Point | 17592186124439 | 15 | 15 | 0 | 0 | 0 | 15 | 99.9859 | 99.9586 | Observed | >99.9999 |
| Introduction to Green's Theorem | Evaluating Line Integrals Using Green's Theorem | 17592186133883 | 12 | 12 | 0 | 0 | 0 | 12 | 99.9169 | 99.8036 | Observed | >99.9999 |
| Line Integrals of Vector-Valued Functions Over Parametric Curves | Evaluating Line Integrals of Vector-Valued Functions Over Space Curves | 17592186133894 | 8 | 7 | 1 | 0 | 0 | 7 | 98.4035 | 97.3634 | Observed | 99.9998 |
| Surface Integrals Over Cartesian Surfaces | Evaluating Surface Integrals Using Polar Coordinates | 17592186105888 | 11 | 10 | 1 | 0 | 0 | 10 | 99.7289 | 99.4449 | Observed | >99.9999 |
| Tangent Lines to Level Curves | Finding the Points on a Curve at which the Tangent Vector is Perpendicular to a Given Vector | 17592186124456 | 11 | 9 | 2 | 0 | 0 | 9 | 99.5105 | 99.0669 | Observed | >99.9999 |
| The Area of a General Triangle | Finding the Area of a Triangle Given the Area of a Quadrilateral | 17592186105906 | 8 | 7 | 1 | 0 | 0 | 7 | 98.4035 | 97.3634 | Observed | 99.9998 |
| Unit Vectors | Finding a Unit Vector Parallel to a Given Vector in a Diagram | 17592186096814 | 3 | 1 | 2 | 0 | 0 | 1 | 44.6256 | 40.5112 | Observed | 85.1368 |
| Volumes of Parallelepipeds | Calculating the Volume of a Parallelepiped Spanned by Three Position Vectors Given Their Coordinates | 17592186105909 | 17 | 15 | 2 | 0 | 0 | 15 | 99.9859 | 99.9586 | Observed | >99.9999 |

## Missing levels: Moderate–hard — 73 KPs

| Topic | KP | KP entity | Total | Rated | Unrated | Easy | Moderate | Hard | Easy absence score | Moderate absence score | Hard absence score | Hybrid score |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Addition and Scalar Multiplication of Cartesian Vectors in 2D | Addition and Scalar Multiplication of Vectors in Component Form | 17592186059710 | 4 | 2 | 2 | 2 | 0 | 0 | Observed | 64.6108 | 27.5172 | 80.0855 |
| Addition and Scalar Multiplication of Cartesian Vectors in 2D | Calculating Sums and Scalar Multiplication of Vectors Given in Alternative Notation | 17592186059713 | 4 | 2 | 2 | 2 | 0 | 0 | Observed | 64.6108 | 27.5172 | 80.0855 |
| Addition and Scalar Multiplication of Cartesian Vectors in 2D | Calculating Sums and Scalar Multiplication of Vectors Using Angle Bracket Notation | 17592186059711 | 4 | 2 | 2 | 2 | 0 | 0 | Observed | 64.6108 | 27.5172 | 80.0855 |
| Calculating Flux Through Cartesian Surfaces | Expressing Flux Over a Surface as a Repeated Integral | 17592186198389 | 12 | 12 | 0 | 12 | 0 | 0 | Observed | 99.8036 | 85.4986 | 99.9938 |
| Calculating Potential Functions | Reconstructing a Two-Variable Function From Its Gradient | 17592186124569 | 14 | 13 | 1 | 13 | 0 | 0 | Observed | 99.8831 | 87.6540 | 99.9972 |
| Calculating a Scalar Projection | Calculating a Scalar Projection Using Angles and Magnitudes | 17592186105916 | 17 | 16 | 1 | 16 | 0 | 0 | Observed | 99.9754 | 92.3813 | 99.9998 |
| Calculating the Cross Product Using Determinants | Calculating the Cross Product Using Determinants | 17592186059736 | 27 | 26 | 1 | 26 | 0 | 0 | Observed | 99.9999 | 98.4758 | >99.9999 |
| Calculating the Dot Product Using Components | Calculating the Dot Product Using the General Formula | 17592186059730 | 7 | 6 | 1 | 6 | 0 | 0 | Observed | 95.5679 | 61.9193 | 99.2102 |
| Calculating the Magnitude of Cartesian Vectors in 2D | Calculating the Magnitude of a Vector Given in Component Form | 17592186059714 | 4 | 2 | 2 | 2 | 0 | 0 | Observed | 64.6108 | 27.5172 | 80.0855 |
| Combining Graph Transformations of Tangent and Cotangent | Identifying the Horizontal Stretch and Vertical Shift of a Transformed Tangent Curve | 17592186184236 | 6 | 5 | 1 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| Computing Triple Integrals Using a Change of Variables | Performing a Change of Variables in a Triple Integral | 17592186198397 | 5 | 3 | 2 | 3 | 0 | 0 | Observed | 78.9474 | 38.2905 | 91.1130 |
| Conservative Vector Fields in the Cartesian Plane | Finding a Parameter in a Given Conservative Vector Field | 17592186166864 | 10 | 10 | 0 | 10 | 0 | 0 | Observed | 99.4449 | 79.9934 | 99.9687 |
| Determining Continuity from Graphs | Determining the Behavior of a Function in the Neighborhood of a Point | 17592186068697 | 12 | 11 | 1 | 11 | 0 | 0 | Observed | 99.6698 | 82.9670 | 99.9860 |
| Determining Continuity from Graphs | Identifying Points of Discontinuity | 17592186068696 | 17 | 17 | 0 | 17 | 0 | 0 | Observed | 99.9854 | 93.5137 | 99.9999 |
| Differentiating Exponential Functions | Differentiating the Product of a Constant and the Exponential Function, Plus a Constant | 17592186096610 | 7 | 5 | 2 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| Differentiating Logarithmic Functions | Calculating the Slope of the Tangent Line of a Logarithmic Function at a Point | 17592186096616 | 13 | 11 | 2 | 11 | 0 | 0 | Observed | 99.6698 | 82.9670 | 99.9860 |
| Differentiating Logarithmic Functions | Differentiating the Product of a Constant and the Natural Logarithm Function | 17592186096613 | 9 | 7 | 2 | 7 | 0 | 0 | Observed | 97.3634 | 67.5793 | 99.6476 |
| Differentiation Rules for Vector-Valued Functions | Using the Chain Rule for Differentiation | 17592186115392 | 12 | 12 | 0 | 12 | 0 | 0 | Observed | 99.8036 | 85.4986 | 99.9938 |
| Equations of Circles | Finding the Center and Radius of a Circle Given Its Equation | 17592186087656 | 8 | 7 | 1 | 7 | 0 | 0 | Observed | 97.3634 | 67.5793 | 99.6476 |
| Equations of Circles | Finding the Equation of a Circle Given the Center and the Radius | 17592186087655 | 8 | 6 | 2 | 6 | 0 | 0 | Observed | 95.5679 | 61.9193 | 99.2102 |
| Equations of Ellipses Centered at the Origin | Determining the Lengths of the Major and Minor Axes Given the Equation of an Ellipse | 17592186087841 | 23 | 22 | 1 | 22 | 0 | 0 | Observed | 99.9989 | 97.0988 | >99.9999 |
| Gaussian Elimination For NxM Systems of Equations | Solving a Consistent System of Equations Using Gauss-Jordan Elimination | 17592186115241 | 11 | 9 | 2 | 9 | 0 | 0 | Observed | 99.0669 | 76.5006 | 99.9298 |
| Geometric Interpretations of Partial Derivatives | Finding the Slope of the Tangent Line to a Curve at a Point | 17592186124437 | 12 | 11 | 1 | 11 | 0 | 0 | Observed | 99.6698 | 82.9670 | 99.9860 |
| Gradient Vector Fields | Sketching the Gradient Vector Field of a Function | 17592186179719 | 11 | 11 | 0 | 11 | 0 | 0 | Observed | 99.6698 | 82.9670 | 99.9860 |
| Graphing Curves Defined Parametrically | Filling a Table of Values for a Parametric Curve | 17592186087717 | 18 | 17 | 1 | 17 | 0 | 0 | Observed | 99.9854 | 93.5137 | 99.9999 |
| Graphing Curves Defined Parametrically | Graphing a Curve Defined Parametrically | 17592186087721 | 16 | 16 | 0 | 16 | 0 | 0 | Observed | 99.9754 | 92.3813 | 99.9998 |
| Graphing General Polynomials | Identifying Multiplicity of a Root Given a Graph | 17592186129253 | 7 | 5 | 2 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| Index Notation for Matrices | Describing an Entry of a Matrix in Index Notation | 17592186100990 | 8 | 6 | 2 | 6 | 0 | 0 | Observed | 95.5679 | 61.9193 | 99.2102 |
| Index Notation for Matrices | Finding an Entry of a Matrix | 17592186100988 | 7 | 5 | 2 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| Index Notation for Matrices | Finding an Entry of a Square Matrix | 17592186100989 | 6 | 5 | 1 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| Inhibited Growth Models With First-Order ODEs | Modeling Inhibited Growth | 17592186124674 | 11 | 9 | 2 | 9 | 0 | 0 | Observed | 99.0669 | 76.5006 | 99.9298 |
| Interpreting the Meaning of the Derivative in Context | Determining the Units of a Derivative | 17592186064271 | 9 | 7 | 2 | 7 | 0 | 0 | Observed | 97.3634 | 67.5793 | 99.6476 |
| Introduction to Differential Equations | Initial Value Problems and Initial Conditions | 17592186166815 | 11 | 11 | 0 | 11 | 0 | 0 | Observed | 99.6698 | 82.9670 | 99.9860 |
| Introduction to Green's Theorem | Expressing a Line Integral as a Double Integral Using Green's Theorem | 17592186133882 | 12 | 12 | 0 | 12 | 0 | 0 | Observed | 99.8036 | 85.4986 | 99.9938 |
| Introduction to Matrices | Determining the Dimensions of a Matrix | 17592186087693 | 8 | 6 | 2 | 6 | 0 | 0 | Observed | 95.5679 | 61.9193 | 99.2102 |
| Introduction to Matrices | Determining the Dimensions of a Matrix with One Row or Column | 17592186087694 | 7 | 5 | 2 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| Line Integrals With Respect to X and Y | Constructing Line Integrals With Respect to X | 17592186133891 | 7 | 6 | 1 | 6 | 0 | 0 | Observed | 95.5679 | 61.9193 | 99.2102 |
| Line Integrals With Respect to X and Y | Constructing Line Integrals With Respect to Y | 17592186133892 | 9 | 9 | 0 | 9 | 0 | 0 | Observed | 99.0669 | 76.5006 | 99.9298 |
| Line Integrals of Scalar Functions Over Paths Expressed as Functions of X | Reducing the Line Integral of a Scalar Function Along a Curve to a Definite Integral | 17592186152159 | 9 | 8 | 1 | 8 | 0 | 0 | Observed | 98.4315 | 72.3981 | 99.8427 |
| Line Integrals of Vector-Valued Functions Over Parametric Curves | Constructing Line Integrals of a Vector-Valued Functions Over Plane Curves | 17592186133831 | 5 | 5 | 0 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| Linear Equations With Infinitely Many Solutions | Identifying Equations With Infinitely Many Solutions | 17592186110719 | 5 | 5 | 0 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| Linear Equations With No Solutions | Identifying an Equation With No Solutions | 17592186204089 | 7 | 5 | 2 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| Modeling Mixture Problems With First-Order Linear ODEs | Determining an Amount at an Overflow Point | 17592186229183 | 7 | 6 | 1 | 6 | 0 | 0 | Observed | 95.5679 | 61.9193 | 99.2102 |
| Perpendicular Lines in the Coordinate Plane | Finding Equations of Perpendicular Horizontal and Vertical Lines | 17592186110602 | 8 | 6 | 2 | 6 | 0 | 0 | Observed | 95.5679 | 61.9193 | 99.2102 |
| Properties of Transformed Sine and Cosine Functions | Calculating the Period of a Transformed Sinusoidal Function | 17592186129122 | 8 | 7 | 1 | 7 | 0 | 0 | Observed | 97.3634 | 67.5793 | 99.6476 |
| Properties of Transformed Sine and Cosine Functions | Finding the Midline of a Transformed Sinusoidal Function | 17592186129123 | 8 | 7 | 1 | 7 | 0 | 0 | Observed | 97.3634 | 67.5793 | 99.6476 |
| Simplifying Expressions Using the Pythagorean Identity | Simplifying an Expression by Expanding Parentheses and Using the Pythagorean Identity | 17592186059655 | 7 | 5 | 2 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| Slope Fields for Nonautonomous Differential Equations | Sketching the Slope Field of a Differential Equation at Some Isolated Points | 17592186172038 | 7 | 5 | 2 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| Solving First-Order ODEs Using Separation of Variables | Finding a General Solution in Implicit Form | 17592186068844 | 11 | 11 | 0 | 11 | 0 | 0 | Observed | 99.6698 | 82.9670 | 99.9860 |
| Solving Systems of Equations by Substitution | Solving a System of Linear Equations Using Substitution | 17592186073752 | 6 | 3 | 3 | 3 | 0 | 0 | Observed | 78.9474 | 38.2905 | 91.1130 |
| Sums of Line Integrals With Respect to X and Y | Evaluating Line Integrals With Respect to X and Y Over Segments | 17592186179728 | 9 | 9 | 0 | 9 | 0 | 0 | Observed | 99.0669 | 76.5006 | 99.9298 |
| Surface Integrals Over Cartesian Surfaces | Express Surface Integrals as Repeated Integrals | 17592186105889 | 8 | 7 | 1 | 7 | 0 | 0 | Observed | 97.3634 | 67.5793 | 99.6476 |
| Tangent Lines to Level Curves | Finding the Tangent Line to a Level Curve | 17592186124454 | 7 | 5 | 2 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| The Antiderivative | Finding the Antiderivative of a Monomial | 17592186064167 | 6 | 4 | 2 | 4 | 0 | 0 | Observed | 87.4761 | 47.4625 | 96.0341 |
| The Arc Length of a Parametric Curve | Finding an Integral Expression For the Arc Length of a Parametric Curve | 17592186092375 | 10 | 8 | 2 | 8 | 0 | 0 | Observed | 98.4315 | 72.3981 | 99.8427 |
| The Area of a General Triangle | Calculating the Area of a Triangle | 17592186105903 | 6 | 5 | 1 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| The Determinant of a 3x3 Matrix | Calculating the Determinant of a 3x3 Matrix | 17592186059847 | 15 | 13 | 2 | 13 | 0 | 0 | Observed | 99.8831 | 87.6540 | 99.9972 |
| The Gradient as a Normal Vector | Finding a Normal Vector to a Level Curve | 17592186124461 | 10 | 8 | 2 | 8 | 0 | 0 | Observed | 98.4315 | 72.3981 | 99.8427 |
| The Gradient as a Normal Vector | Finding a Normal Vector to a Level Surface | 17592186124463 | 12 | 12 | 0 | 12 | 0 | 0 | Observed | 99.8036 | 85.4986 | 99.9938 |
| The Jacobian | Evaluating a Jacobian Determinant | 17592186129263 | 11 | 11 | 0 | 11 | 0 | 0 | Observed | 99.6698 | 82.9670 | 99.9860 |
| The Jacobian | Identifying the Local Area Scale Factor of a Transformation | 17592186129282 | 11 | 11 | 0 | 11 | 0 | 0 | Observed | 99.6698 | 82.9670 | 99.9860 |
| The Multivariable Chain Rule | Calculating the Derivative of a Multivariable Function With One Independent Variable | 17592186166747 | 12 | 11 | 1 | 11 | 0 | 0 | Observed | 99.6698 | 82.9670 | 99.9860 |
| The Multivariable Chain Rule | Calculating the Derivative of a Multivariable Function With One Independent Variable in the Special Case | 17592186166748 | 10 | 10 | 0 | 10 | 0 | 0 | Observed | 99.4449 | 79.9934 | 99.9687 |
| The Multivariable Chain Rule With Polar Coordinates | Calculating the Derivative of a Cartesian Function With Respect to Plane Polar Coordinates | 17592186124594 | 7 | 6 | 1 | 6 | 0 | 0 | Observed | 95.5679 | 61.9193 | 99.2102 |
| The Multivariable Chain Rule in Vector Form | Applying the Vector Form of the Chain Rule to a Function of Two Variables | 17592186124469 | 6 | 5 | 1 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| The Product Rule for Differentiation | Differentiating a Product Containing a Trigonometric Function | 17592186096617 | 10 | 8 | 2 | 8 | 0 | 0 | Observed | 98.4315 | 72.3981 | 99.8427 |
| The Product Rule for Differentiation | Differentiating a Product Containing an Exponential or Logarithmic Function | 17592186096618 | 13 | 11 | 2 | 11 | 0 | 0 | Observed | 99.6698 | 82.9670 | 99.9860 |
| Using the Pythagorean Identity in the First Quadrant | Using the Pythagorean Theorem on the Unit Circle | 17592186110754 | 7 | 5 | 2 | 5 | 0 | 0 | Observed | 92.5497 | 55.2712 | 98.2302 |
| Vector Fields | Identifying Vector Fields on Three-Dimensions | 17592186172087 | 9 | 9 | 0 | 9 | 0 | 0 | Observed | 99.0669 | 76.5006 | 99.9298 |
| Vector Fields | Identifying Vector Fields on Two-Dimensions | 17592186172085 | 8 | 8 | 0 | 8 | 0 | 0 | Observed | 98.4315 | 72.3981 | 99.8427 |
| Verifying Solutions of Differential Equations | Identifying Solutions to Initial Value Problems | 17592186100951 | 19 | 17 | 2 | 17 | 0 | 0 | Observed | 99.9854 | 93.5137 | 99.9999 |
| Visualizing Vector Fields | Sketching a Two-Dimensional Vector Field | 17592186172083 | 10 | 9 | 1 | 9 | 0 | 0 | Observed | 99.0669 | 76.5006 | 99.9298 |
| Volumes of Parallelepipeds | Calculating the Volume of a Parallelepiped Spanned by Three Vectors | 17592186105907 | 11 | 9 | 2 | 9 | 0 | 0 | Observed | 99.0669 | 76.5006 | 99.9298 |

## Missing levels: Easy–hard — 36 KPs

| Topic | KP | KP entity | Total | Rated | Unrated | Easy | Moderate | Hard | Easy absence score | Moderate absence score | Hard absence score | Hybrid score |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Addition and Scalar Multiplication of Cartesian Vectors in 2D | Calculating Sums and Scalar Multiplication of Column Vectors | 17592186059712 | 4 | 2 | 2 | 0 | 2 | 0 | 69.3368 | Observed | 27.5172 | 83.5884 |
| Calculating a Scalar Projection | Projecting a Vector Onto a Perpendicular Vector | 17592186105918 | 22 | 22 | 0 | 0 | 22 | 0 | 99.9998 | Observed | 97.0988 | >99.9999 |
| Calculating the Magnitude of Cartesian Vectors in 2D | Calculating a Vector From Position Vectors and then Computing its Magnitude | 17592186059715 | 5 | 3 | 2 | 0 | 3 | 0 | 83.0204 | Observed | 38.2905 | 93.3515 |
| Combining Graph Transformations of Tangent and Cotangent | Identifying the Horizontal Stretch and Vertical Shift of a Transformed Cotangent Curve | 17592186184148 | 12 | 12 | 0 | 0 | 12 | 0 | 99.9169 | Observed | 85.4986 | 99.9980 |
| Computing Double Integrals Using a Change of Variables | Cases When the Transformation Is Inferred From the Domain | 17592186198373 | 6 | 5 | 1 | 0 | 5 | 0 | 94.7935 | Observed | 55.2712 | 98.9089 |
| Computing Triple Integrals Using a Change of Variables | Evaluating a Triple Integral Using a Change of Variables | 17592186198398 | 7 | 5 | 2 | 0 | 5 | 0 | 94.7935 | Observed | 55.2712 | 98.9089 |
| Conservative Vector Fields in the Cartesian Plane | Identifying Conservative Vector Fields | 17592186166863 | 11 | 11 | 0 | 0 | 11 | 0 | 99.8499 | Observed | 82.9670 | 99.9952 |
| Converting from Polar Coordinates to Cartesian Coordinates | Finding the Cartesian Coordinates of a Point Given a Description of the Radius and Angle | 17592186092218 | 12 | 10 | 2 | 0 | 10 | 0 | 99.7289 | Observed | 79.9934 | 99.9881 |
| Describing Properties of the Cosecant Function | Describing the General Properties of the Cosecant Function | 17592186176053 | 7 | 5 | 2 | 0 | 5 | 0 | 94.7935 | Observed | 55.2712 | 98.9089 |
| Describing Properties of the Cosine Function | Describing Properties of the Cosine Function | 17592186176047 | 8 | 6 | 2 | 0 | 6 | 0 | 97.1169 | Observed | 61.9193 | 99.5580 |
| Describing Properties of the Tangent Function | Utilizing the Periodicity Property of the Tangent Function | 17592186176050 | 7 | 5 | 2 | 0 | 5 | 0 | 94.7935 | Observed | 55.2712 | 98.9089 |
| Describing the Position Vector of a Point Using Known Vectors | Expressing a Vector That Satisfies a Ratio in Terms of Known Vectors | 17592186096653 | 23 | 22 | 1 | 0 | 22 | 0 | 99.9998 | Observed | 97.0988 | >99.9999 |
| Double Integrals Between Polar Curves | Converting an Integral Over a Region Enclosed Between Two Curves to Polar Coordinates | 17592186157298 | 11 | 10 | 1 | 0 | 10 | 0 | 99.7289 | Observed | 79.9934 | 99.9881 |
| Equations of Circles | Finding the Equation of a Circle Given the Center and a Point on the Circle | 17592186087768 | 7 | 6 | 1 | 0 | 6 | 0 | 97.1169 | Observed | 61.9193 | 99.5580 |
| Finding Areas Using the Cross Product | Calculating the Area of a Triangle Given Its Vertices | 17592186105733 | 19 | 18 | 1 | 0 | 18 | 0 | 99.9976 | Observed | 94.4778 | >99.9999 |
| Gaussian Elimination For NxM Systems of Equations | Classifying a System as Consistent Dependent, Consistent Independent, or Inconsistent | 17592186115299 | 14 | 14 | 0 | 0 | 14 | 0 | 99.9745 | Observed | 89.4890 | 99.9997 |
| Geometric Interpretations of Partial Derivatives | Finding the Equation of the Tangent Line to a Curve at a Point | 17592186124438 | 14 | 14 | 0 | 0 | 14 | 0 | 99.9745 | Observed | 89.4890 | 99.9997 |
| Graphing Curves Defined Parametrically | Determining the Range of a Parametric Equation | 17592186087722 | 23 | 21 | 2 | 0 | 21 | 0 | 99.9996 | Observed | 96.5923 | >99.9999 |
| Green's Theorem in Polar Coordinates | Expressing a Line Integral Along a Path as a Double Integral Using Green's Theorem | 17592186175987 | 11 | 11 | 0 | 0 | 11 | 0 | 99.8499 | Observed | 82.9670 | 99.9952 |
| Introduction to Integration by Parts | Computing a Definite Integral Using Integration by Parts | 17592186064274 | 23 | 23 | 0 | 0 | 23 | 0 | 99.9999 | Observed | 97.5300 | >99.9999 |
| Introduction to Matrices | Identifying a Matrix by Its Description | 17592186087713 | 8 | 6 | 2 | 0 | 6 | 0 | 97.1169 | Observed | 61.9193 | 99.5580 |
| Line Integrals of Vector-Valued Functions Over Parametric Curves | Evaluating Line Integrals of a Vector-Valued Functions Over Plane Curves | 17592186133828 | 8 | 8 | 0 | 0 | 8 | 0 | 99.1160 | Observed | 72.3981 | 99.9275 |
| Surface Integrals Over Cartesian Surfaces | Evaluating Surface Integrals | 17592186105887 | 10 | 9 | 1 | 0 | 9 | 0 | 99.5105 | Observed | 76.5006 | 99.9706 |
| Tangent Lines to Level Curves | Finding a Tangent Vector to a Plane Curve | 17592186124455 | 11 | 10 | 1 | 0 | 10 | 0 | 99.7289 | Observed | 79.9934 | 99.9881 |
| The Area of a General Triangle | Calculating an Angle or Side of a Triangle Given the Area of a Triangle | 17592186105904 | 9 | 7 | 2 | 0 | 7 | 0 | 98.4035 | Observed | 67.5793 | 99.8209 |
| The Area of a General Triangle | Calculating the Area of a Quadrilateral | 17592186105905 | 10 | 8 | 2 | 0 | 8 | 0 | 99.1160 | Observed | 72.3981 | 99.9275 |
| The Divergence Theorem | Calculating Flux Across a Closed Surface | 17592186133931 | 11 | 10 | 1 | 0 | 10 | 0 | 99.7289 | Observed | 79.9934 | 99.9881 |
| The Gradient Vector | Calculating the Gradient of a Function of Three Variables | 17592186124444 | 11 | 11 | 0 | 0 | 11 | 0 | 99.8499 | Observed | 82.9670 | 99.9952 |
| The Jacobian | Finding Regions Where a Transformation is Orientation-Preserving or Reversing | 17592186129283 | 12 | 12 | 0 | 0 | 12 | 0 | 99.9169 | Observed | 85.4986 | 99.9980 |
| The Jacobian of a Three-Dimensional Transformation | Determining the Critical Points of a Transformation | 17592186129270 | 12 | 12 | 0 | 0 | 12 | 0 | 99.9169 | Observed | 85.4986 | 99.9980 |
| The Multivariable Chain Rule With Polar Coordinates | Calculating the Derivative of a Polar Function With Respect to Cartesian Coordinates | 17592186124595 | 9 | 7 | 2 | 0 | 7 | 0 | 98.4035 | Observed | 67.5793 | 99.8209 |
| The Product Rule for Differentiation | Finding the Slope of the Tangent Line to a Product  at a Given Point | 17592186096619 | 13 | 11 | 2 | 0 | 11 | 0 | 99.8499 | Observed | 82.9670 | 99.9952 |
| The Scalar Triple Product | Calculating Scalar Triple Products Using Its Properties | 17592186105737 | 19 | 19 | 0 | 0 | 19 | 0 | 99.9987 | Observed | 95.2986 | >99.9999 |
| Using the Pythagorean Identity in the First Quadrant | Computing a Reciprocal Ratio Using the Pythagorean Identity | 17592186110756 | 6 | 5 | 1 | 0 | 5 | 0 | 94.7935 | Observed | 55.2712 | 98.9089 |
| Verifying Solutions of Differential Equations | Identifying Solutions to First-Order Differential Equations | 17592186100959 | 11 | 11 | 0 | 0 | 11 | 0 | 99.8499 | Observed | 82.9670 | 99.9952 |
| Volumes of Parallelepipeds | Determining Whether Three Vectors are Coplanar | 17592186105908 | 17 | 15 | 2 | 0 | 15 | 0 | 99.9859 | Observed | 91.0513 | 99.9999 |

## Missing levels: No rated evidence — 26 KPs

| Topic | KP | KP entity | Total | Rated | Unrated | Easy | Moderate | Hard | Easy absence score | Moderate absence score | Hard absence score | Hybrid score |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Graphing Linear Equations | Identifying Points That Lie on a Line | 17592186054676 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Graphing Linear Equations | Identifying a Line Given a Graph | 17592186054802 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Graphing Linear Equations | Plotting a Line Using a Table | 17592186054694 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Graphing Linear Equations | Sketching a Line Using Two Points | 17592186054695 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Interval Notation | Converting Between Intervals and Inequalities: Closed Intervals | 17592186059829 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Interval Notation | Converting Between Intervals and Inequalities: Open Intervals | 17592186059826 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Interval Notation | Translating Between Half-Open Intervals and Inequalities | 17592186059827 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Interval Notation | Translating Between Half-Open Intervals and Number Lines | 17592186059828 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Introduction to Systems of Linear Equations | Finding the Solution to a System From Its Graph | 17592186138428 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Introduction to Systems of Linear Equations | Word Problems | 17592186138429 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Parallel Lines in the Coordinate Plane | Finding Unknown Parameters | 17592186087688 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Parallel Lines in the Coordinate Plane | Identifying Parallel Lines Given in Slope-Intercept Form | 17592186087686 | 3 | 0 | 3 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Parallel Lines in the Coordinate Plane | Identifying Parallel Lines Given in Standard Form | 17592186087687 | 3 | 0 | 3 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Parallel Vectors | Creating Parallel Vectors | 17592186096649 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Parallel Vectors | Determining Whether Two Vectors are Parallel | 17592186096648 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Parallel Vectors | Identifying Parallel Vectors From a Diagram | 17592186096700 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Solving Systems of Equations by Substitution | Solving a Challenging System of Linear Equations Using Substitution | 17592186073753 | 3 | 0 | 3 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Solving Systems of Linear Equations Using Elimination: One Transformation | Eliminating the First Variable | 17592186192654 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Solving Systems of Linear Equations Using Elimination: One Transformation | Eliminating the Second Variable | 17592186192655 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Solving Systems of Linear Equations Using Elimination: One Transformation | Solving a System of Equations by Eliminating the First Variable | 17592186192656 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Solving Systems of Linear Equations Using Elimination: One Transformation | Solving a System of Equations by Eliminating the Second Variable | 17592186192657 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Systems of Equations With No Solutions and Infinitely Many Solutions | Finding the General Solution to a System With Infinitely Many Intersection Points | 17592186073778 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Systems of Equations With No Solutions and Infinitely Many Solutions | Finding the Number of Intersection Points of Two Lines | 17592186073777 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Systems of Equations With No Solutions and Infinitely Many Solutions | Finding the Number of Solutions to a System | 17592186073776 | 3 | 0 | 3 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Unit Vectors | Finding a Unit Vector Parallel to a Given Vector | 17592186096813 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |
| Unit Vectors | Finding a Unit Vector Parallel to a Vector Sum | 17592186096815 | 2 | 0 | 2 | 0 | 0 | 0 | No rated evidence | No rated evidence | No rated evidence | — |

Counts in Easy/Moderate/Hard columns are database pool counts. Scores for different missing levels are calculated separately. Values that would round to 100.0000 are displayed as >99.9999; the JSON retains zero-observation probabilities for these cases.

[Full precision scores and metadata](scores.json) · [Discovery output](candidates.json)
