# Distance of logged knowledge changes from activity topics

Read-only database basis: 504. Graph: 2977 topics and 6560 direct `:topic/next` edges.

Analyzed 153 completed-activity snapshots and 810 changed course/topic rows.

Distance means the shortest path, then the maximum among changed topics. Prerequisite distance traces edges backward from the activity; downstream follows them forward; undirected permits either direction. For assessments/multisteps the origin is the nearest of their actually captured question topics. No encompassing or KP remediation edges are included.

These are changes in displayed bands between snapshots, not exact repetitions or proof that the activity caused every change. Recovered or nonconsecutive comparisons are retained and identified in results.json.

## Maximum prerequisite distance: 9 edges

Task 13944891 (lesson): Defining Continuity at a Point → Negative Angles in the Coordinate Plane; band 5 → 6.

Defining Continuity at a Point → Limits of Piecewise Functions → Limits of Reciprocal Trigonometric Functions → Combining Graph Transformations of Secant and Cosecant → Vertical Translations of Trigonometric Functions → Graphing Sine and Cosine → Further Extensions of the Special Trigonometric Ratios → Trigonometric Ratios of Quadrantal Angles Outside the Standard Range → Coterminal Angles → Negative Angles in the Coordinate Plane

Task 13944891 (lesson): Defining Continuity at a Point → The Factor Theorem; band 5 → 6.

Defining Continuity at a Point → Limits of Piecewise Functions → Limits of Reciprocal Functions → Limits at Infinity of Polynomials → End Behavior of Polynomials → Graphing Cubic Curves Containing One Distinct Real Root → Graphing Cubic Curves Containing a Double Root → Multiplicities of the Roots of Polynomials → Factoring Cubic Polynomials Using the Factor Theorem → The Factor Theorem

## Maximum undirected distance: 8 edges

Task 13943082 (review): Integrating the Reciprocal Function → Negative Angles in the Coordinate Plane; band 6 → 5.

Integrating the Reciprocal Function → Combining the Laws of Logarithms → The Power Rule for Logarithms → Logarithmic Differentiation → Simplifying Expressions Using Basic Trigonometric Identities → The Reciprocal Trigonometric Ratios → Special Trigonometric Ratios → Angles in the Coordinate Plane → Negative Angles in the Coordinate Plane

Task 13944891 (lesson): Defining Continuity at a Point → Negative Angles in the Coordinate Plane; band 5 → 6.

Defining Continuity at a Point → Determining Continuity from Graphs → Infinite Limits from Graphs → Unbounded Behavior of Functions Near a Point → Graphing Tangent and Cotangent → Further Extensions of the Special Trigonometric Ratios → Trigonometric Ratios of Quadrantal Angles Outside the Standard Range → Coterminal Angles → Negative Angles in the Coordinate Plane

Task 13947257 (review): Differentiating Reciprocal Trigonometric Functions → Finding Lowest Common Multiples Using Prime Factorization; band 6 → 5.

Differentiating Reciprocal Trigonometric Functions → The Chain Rule With Trigonometric Functions → Selecting Procedures for Calculating Derivatives → Calculating Velocity for Straight-Line Motion Using Differentiation → Distance-Time Graphs → Speed as a Unit Rate → Solving Problems Using Unit Rates → Modeling Work Problems → Finding Lowest Common Multiples Using Prime Factorization

## Maximum downstream distance: 6 edges

Task 13939908 (assessment): multiple captured topics → Limits of Trigonometric Functions; band 2 → 1.

Coterminal Angles → Trigonometric Ratios of Quadrantal Angles Outside the Standard Range → Further Extensions of the Special Trigonometric Ratios → Graphing Sine and Cosine → Vertical Translations of Trigonometric Functions → Combining Graph Transformations of Sine and Cosine → Limits of Trigonometric Functions

## Per-activity maxima

| Task | Activity | Changed topics | Upstream prerequisite edges | Either direction | Farthest upstream changed topic |
|---|---|---:|---:|---:|---|
| 13831128 | lesson: Determining Continuity from Graphs | 0 | — | — |  |
| 13831126 | lesson: Combining Graph Transformations of Reciprocal Functions | 4 | 3 | 3 | Combining Graph Transformations: Two Operations |
| 13831127 | lesson: Finding Points on Transformed Curves | 1 | 0 | 0 | Finding Points on Transformed Curves |
| 13927791 | review: The Rational Roots Theorem | 1 | 0 | 0 | The Rational Roots Theorem |
| 13929099 | review: The Argument of a Complex Number | 0 | — | — |  |
| 13929463 | review: Defining Definite Integrals Using Left and Right Riemann Sums | 1 | 1 | 1 | Left and Right Riemann Sums in Sigma Notation |
| 13831125 | lesson: Completing the Square | 1 | 0 | 0 | Completing the Square |
| 13929491 | review: Multiplicities of the Roots of Polynomials | 1 | 1 | 1 | Factoring Cubic Polynomials Using the Factor Theorem |
| 13929637 | review: Addition and Scalar Multiplication of Cartesian Vectors in 3D | 3 | 1 | 1 | Addition and Scalar Multiplication of Cartesian Vectors in 2D; Three-Dimensional Vectors in Component Form |
| 13929975 | review: The Distance Formula in Three Dimensions | 2 | 1 | 1 | The Distance Formula |
| 13930198 | lesson: Interpreting the Meaning of the Derivative in Context | 1 | 0 | 0 | Interpreting the Meaning of the Derivative in Context |
| 13930137 | review: Solving Equations Containing the Exponential Function | 3 | 2 | 2 | The Change of Base Formula for Logarithms; The Power Rule for Logarithms |
| 13930176 | review: Adding Rational Expressions With No Common Factors in the Denominator | 3 | 1 | 2 | Adding and Subtracting Rational Expressions |
| 13930486 | review: The Argument of a Complex Number | 2 | 1 | 1 | The Complex Plane |
| 13928579 | lesson: End Behavior of Polynomials | 1 | 0 | 0 | End Behavior of Polynomials |
| 13930500 | review: Finding Surface Areas Using Nets | 2 | 2 | 2 | Faces, Vertices, and Edges of Polyhedrons |
| 13930102 | lesson: Solving Quadratic Equations by Completing the Square | 10 | 0 | 7 | Solving Quadratic Equations by Completing the Square |
| 13930907 | lesson: Vertical Translations of Exponential Growth Functions | 5 | 0 | 7 | Vertical Translations of Exponential Growth Functions |
| 13929417 | lesson: Domain and Range of Transformed Reciprocal Functions | 15 | 3 | 7 | Graphing Reciprocal Functions |
| 13930905 | review: The Sum and Constant Multiple Rules for Differentiation | 0 | — | — |  |
| 13931416 | lesson: Vertical Translations of Exponential Decay Functions | 2 | 0 | 5 | Vertical Translations of Exponential Decay Functions |
| 13931523 | lesson: Calculating the Slope of a Tangent Line Using Differentiation | 0 | — | — |  |
| 13931612 | lesson: Calculating the Equation of a Tangent Line Using Differentiation | 2 | 1 | 1 | Calculating the Slope of a Tangent Line Using Differentiation |
| 13931548 | review: Graphing Exponential Decay Functions | 1 | 0 | 0 | Graphing Exponential Decay Functions |
| 13930906 | lesson: Ordering Objects | 3 | 1 | 4 | The Rules of Sum and Product |
| 13931667 | lesson: The Chain Rule for Differentiation | 0 | — | — |  |
| 13931731 | lesson: Permutations | 2 | — | 6 |  |
| 13931806 | review: Vertical Translations of Exponential Decay Functions | 3 | 1 | 6 | Graphing Exponential Decay Functions |
| 13931761 | lesson: Perpendicular Lines in the Coordinate Plane | 5 | 1 | 7 | Properties of Lines Given in Standard Form |
| 13931473 | lesson: Vertical Asymptotes of Rational Functions | 12 | 0 | 6 | Vertical Asymptotes of Rational Functions |
| 13931816 | review: Completing the Square | 7 | — | 6 |  |
| 13930904 | lesson: Limits at Infinity of Polynomials | 8 | 1 | 6 | Limits at Infinity from Graphs; The Power and Root Rules for Limits |
| 13931990 | lesson: Solving Exponential Equations With Different Bases | 1 | 0 | 0 | Solving Exponential Equations With Different Bases |
| 13932041 | lesson: Vertical Reflections of Exponential Functions | 4 | 2 | 5 | Graphing Exponential Decay Functions |
| 13932058 | lesson: Invertible Functions | 0 | — | — |  |
| 13932088 | lesson: Graphing General Polynomials | 5 | 4 | 6 | Graphing Cubic Curves Containing Three Distinct Real Roots |
| 13932118 | review: Domain and Range of Transformed Reciprocal Functions | 0 | — | — |  |
| 13931854 | lesson: Combinations | 11 | 0 | 7 | Combinations |
| 13931905 | lesson: Using the Pythagorean Identity in the First Quadrant | 11 | — | 7 |  |
| 13931643 | lesson: Differentiating Trigonometric Functions | 22 | 3 | 6 | The Sum and Constant Multiple Rules for Differentiation |
| 13931259 | lesson: Describing the Position Vector of a Point Using Known Vectors | 22 | — | 7 |  |
| 13932295 | multistep: Limits and Continuity of Functions From Graphs | 5 | — | 7 |  |
| 13932272 | assessment: multiple captured topics | 5 | 3 | 3 | Unbounded Behavior of Functions Near a Point |
| 13932633 | review: Solving Quadratic Equations by Completing the Square | 2 | — | 5 |  |
| 13932637 | lesson: The Mean of a Data Set | 0 | — | — |  |
| 13932636 | lesson: Differentiating Exponential Functions | 4 | 2 | 6 | The Sum and Constant Multiple Rules for Differentiation |
| 13932635 | lesson: Calculating the Inverse of a Function | 5 | 0 | 6 | Calculating the Inverse of a Function |
| 13932634 | review: Roots of Transformed Radical Functions | 5 | 1 | 6 | Solving Radical Equations |
| 13932868 | lesson: The Chain Rule With Exponential Functions | 1 | — | 4 |  |
| 13932901 | lesson: Differentiating Logarithmic Functions | 6 | 3 | 5 | The Sum and Constant Multiple Rules for Differentiation |
| 13932638 | lesson: Extending the Pythagorean Identity to All Quadrants | 7 | 1 | 6 | Using the Pythagorean Identity in the First Quadrant |
| 13932839 | lesson: Variance and Standard Deviation | 11 | 2 | 7 | Sigma Notation |
| 13933098 | lesson: Second and Higher-Order Derivatives | 6 | 4 | 5 | The Sum and Constant Multiple Rules for Differentiation |
| 13933323 | lesson: The Chain Rule With Logarithmic Functions | 5 | 0 | 7 | The Chain Rule With Logarithmic Functions |
| 13933387 | lesson: Integrating the Reciprocal Function | 0 | — | — |  |
| 13933451 | lesson: The Product Rule for Differentiation | 5 | — | 5 |  |
| 13933487 | lesson: Describing Properties of the Cosine Function | 1 | — | 6 |  |
| 13933642 | review: Calculating the Equation of a Tangent Line Using Differentiation | 1 | — | 6 |  |
| 13933611 | lesson: The Quotient Rule for Differentiation | 2 | — | 6 |  |
| 13933730 | multistep: Graphs of Trigonometric Functions, Indefinite Integrals, and Tangent Lines | 4 | 1 | 3 | The Sum and Constant Multiple Rules for Differentiation |
| 13933758 | lesson: Graphing Reflections of Trigonometric Functions | 4 | 3 | 6 | Periodic Functions |
| 13933552 | lesson: Integrating Exponential Functions | 4 | — | 7 |  |
| 13933668 | review: Combinations | 2 | — | 6 |  |
| 13932983 | lesson: Solving Exponential Equations Using the Zero-Product Property | 0 | — | — |  |
| 13933833 | lesson: Calculating Derivatives From Data and Tables | 8 | 0 | 7 | Calculating Derivatives From Data and Tables |
| 13933873 | lesson: Describing Properties of the Tangent Function | 9 | 2 | 7 | Periodic Functions |
| 13933939 | lesson: Finding Equations of Perpendicular Lines | 1 | 0 | 0 | Finding Equations of Perpendicular Lines |
| 13934099 | review: Combining Graph Transformations of Reciprocal Functions | 0 | — | — |  |
| 13934039 | lesson: Describing Properties of the Secant Function | 7 | — | 6 |  |
| 13933898 | assessment: multiple captured topics | 19 | 1 | 5 | Negative Angles in the Coordinate Plane |
| 13934288 | lesson: Calculating the Equation of a Normal Line Using Differentiation | 17 | 0 | 6 | Calculating the Equation of a Normal Line Using Differentiation |
| 13934289 | lesson: Calculating Derivatives From Graphs | 10 | 6 | 7 | Calculating the Slope of a Tangent Line Using Differentiation |
| 13938271 | review: Invertible Functions | 0 | — | — |  |
| 13934292 | lesson: Describing Properties of the Cotangent Function | 3 | 2 | 2 | Graphing Tangent and Cotangent |
| 13934287 | lesson: The Shortest Distance Between a Point and a Line | 14 | 4 | 6 | Introduction to the Elimination Method |
| 13934290 | lesson: Scatter Plots | 1 | 0 | 0 | Scatter Plots |
| 13938313 | review: Variance and Standard Deviation | 0 | — | — |  |
| 13934291 | lesson: The Least Common Multiple of Two Polynomials | 12 | 1 | 7 | The Least Common Multiple of Two Monomials |
| 13938412 | review: Describing the Position Vector of a Point Using Known Vectors | 2 | 1 | 7 | Problem Solving Using Vector Diagrams |
| 13938518 | review: Vertical Reflections of Exponential Functions | 8 | 2 | 6 | Vertical Translations of Exponential Growth Functions |
| 13938605 | review: The Chain Rule for Differentiation | 4 | — | 6 |  |
| 13938989 | lesson: Trend Lines | 12 | 0 | 7 | Trend Lines |
| 13938687 | review: Permutations | 0 | — | — |  |
| 13938817 | review: Perpendicular Lines in the Coordinate Plane | 1 | — | 5 |  |
| 13938893 | review: The Quotient Rule for Differentiation | 9 | 4 | 7 | Calculating the Slope of a Tangent Line Using Differentiation |
| 13939267 | multistep: Limits of Trigonometric Functions and Instantaneous Rates of Change | 8 | 2 | 5 | Graphing Secant and Cosecant |
| 13939331 | lesson: Differentiating Reciprocal Trigonometric Functions | 11 | 5 | 7 | Calculating the Slope of a Tangent Line Using Differentiation |
| 13938930 | review: Solving Equations Containing the Exponential Function | 0 | — | — |  |
| 13939090 | review: The Chain Rule With Logarithmic Functions | 12 | 3 | 7 | Calculating the Slope of a Tangent Line Using Differentiation |
| 13939163 | review: Vertical Asymptotes of Rational Functions | 10 | — | 5 |  |
| 13939587 | lesson: Integrating Trigonometric Functions | 7 | 4 | 6 | Differentiating Trigonometric Functions |
| 13938136 | assessment: multiple captured topics | 0 | — | — |  |
| 13939871 | review: Adding Rational Expressions With No Common Factors in the Denominator | 5 | 0 | 5 | Adding Rational Expressions With No Common Factors in the Denominator |
| 13939872 | review: Finding Points on Transformed Curves | 1 | 0 | 0 | Finding Points on Transformed Curves |
| 13939873 | review: Limits at Infinity of Polynomials | 0 | — | — |  |
| 13940224 | lesson: Describing Properties of the Cosecant Function | 5 | 1 | 6 | Describing Properties of the Sine Function; Graphing Secant and Cosecant |
| 13939874 | review: The Chain Rule With Exponential Functions | 2 | 2 | 2 | Calculating the Slope of a Tangent Line Using Differentiation |
| 13939876 | review: The Product Rule for Differentiation | 0 | — | — |  |
| 13940317 | review: Limits of Reciprocal Trigonometric Functions | 11 | 3 | 5 | Graphing Tangent and Cotangent |
| 13939908 | assessment: multiple captured topics | 12 | 0 | 4 | The Rational Roots Theorem; Vieta's Formulas |
| 13941097 | lesson: The Chain Rule With Trigonometric Functions | 21 | 8 | 6 | The Power of Quotient Rule for Exponents |
| 13941632 | review: Second and Higher-Order Derivatives | 21 | 5 | 6 | The Power of Quotient Rule for Exponents |
| 13941880 | lesson: Selecting Procedures for Calculating Derivatives | 8 | 0 | 7 | Selecting Procedures for Calculating Derivatives |
| 13941630 | review: Graphing Exponential Decay Functions | 9 | 2 | 6 | The Power of Quotient Rule for Exponents |
| 13941629 | review: Graphing General Polynomials | 17 | 4 | 7 | Graphing Cubic Curves Containing Three Distinct Real Roots |
| 13941631 | review: Combinations | 0 | — | — |  |
| 13942110 | multistep: Modeling Particle Motion Using Trigonometric Functions | 12 | 4 | 5 | Differentiating Trigonometric Functions |
| 13941973 | lesson: Covariance | 12 | — | 7 |  |
| 13941829 | review: Vertical Translations of Exponential Decay Functions | 2 | — | 5 |  |
| 13942972 | review: Describing Properties of the Secant Function | 0 | — | — |  |
| 13943082 | review: Integrating the Reciprocal Function | 10 | 1 | 8 | Combining the Laws of Logarithms |
| 13943150 | lesson: Completing the Square With Odd Linear Terms | 1 | 0 | 0 | Completing the Square With Odd Linear Terms |
| 13943261 | lesson: Completing the Square With Leading Coefficients | 8 | 0 | 7 | Completing the Square With Leading Coefficients |
| 13943411 | lesson: Solving Quadratic Equations With Leading Coefficients by Completing the Square | 0 | — | — |  |
| 13943118 | review: Calculating the Equation of a Normal Line Using Differentiation | 8 | — | 6 |  |
| 13943521 | lesson: Combining Graph Transformations of Tangent and Cotangent | 0 | — | — |  |
| 13942892 | lesson: Factorials in Variable Expressions | 10 | 1 | 6 | Factorials |
| 13943741 | lesson: Combining Graph Transformations of Exponential Functions | 7 | 3 | 6 | Vertical Translations of Exponential Growth Functions |
| 13941628 | review: Extending the Pythagorean Identity to All Quadrants | 7 | 1 | 6 | Using the Pythagorean Identity in the First Quadrant |
| 13943819 | lesson: Properties of Transformed Exponential Functions | 2 | 5 | 3 | Graphing Exponential Growth Functions |
| 13943873 | lesson: Limits of Exponential Functions | 0 | — | — |  |
| 13944026 | lesson: Solving Compound Inequalities | 4 | 0 | 5 | Solving Compound Inequalities |
| 13944109 | lesson: Limits of Piecewise Functions | 10 | 8 | 7 | Negative Angles in the Coordinate Plane; The Factor Theorem |
| 13942024 | lesson: Solving Exponential Equations With Different Bases Using Logarithms | 1 | 0 | 0 | Solving Exponential Equations With Different Bases Using Logarithms |
| 13944255 | lesson: Properties of Transformed Sine and Cosine Functions | 3 | 4 | 4 | Vertical Stretches of Functions |
| 13944593 | multistep: Applying the Rules of Differentiation and Integration | 13 | 2 | 5 | Calculating the Slope of a Tangent Line Using Differentiation |
| 13944377 | assessment: multiple captured topics | 0 | — | — |  |
| 13944891 | lesson: Defining Continuity at a Point | 6 | 9 | 8 | Negative Angles in the Coordinate Plane; The Factor Theorem |
| 13944893 | lesson: Finding Zeros and Extrema of Transformed Sine and Cosine Functions | 5 | 3 | 6 | Describing Properties of the Cosine Function |
| 13945035 | lesson: Left and Right Continuity | 3 | 0 | 7 | Left and Right Continuity |
| 13945218 | review: Finding Equations of Perpendicular Lines | 0 | — | — |  |
| 13945113 | lesson: Properties of Transformed Secant and Cosecant Functions | 2 | 0 | 6 | Properties of Transformed Secant and Cosecant Functions |
| 13945275 | lesson: Continuity Over an Interval | 1 | 0 | 0 | Continuity Over an Interval |
| 13945429 | lesson: Properties of Transformed Tangent and Cotangent Functions | 0 | — | — |  |
| 13945582 | lesson: Linear Equations With Infinitely Many Solutions | 8 | — | 6 |  |
| 13945712 | lesson: Heights of Triangles | 9 | 0 | 7 | Heights of Triangles |
| 13945792 | lesson: Speed as a Unit Rate | 0 | — | — |  |
| 13945897 | lesson: Areas of Triangles | 3 | 0 | 4 | Areas of Triangles |
| 13946053 | review: Differentiating Logarithmic Functions | 1 | 0 | 0 | Differentiating Logarithmic Functions |
| 13944896 | lesson: Systems of Linear Equations With Fractional Coefficients | 6 | — | 6 |  |
| 13946119 | lesson: Calculating Areas of Right Triangles Using Trigonometry | 10 | 2 | 6 | Heights of Triangles |
| 13946345 | lesson: Systems of Linear Equations With Decimal Coefficients | 0 | — | — |  |
| 13946476 | lesson: The Area of a General Triangle | 6 | 3 | 6 | Heights of Triangles |
| 13946663 | review: Calculating Derivatives From Data and Tables | 1 | 0 | 0 | Calculating Derivatives From Data and Tables |
| 13946716 | multistep: Stock and Commodity Prices With Piecewise-Continuous Functions | 0 | — | — |  |
| 13946554 | lesson: Further Reasoning With Equivalent Ratios | 6 | 1 | 7 | Reasoning With Equivalent Ratios |
| 13946894 | lesson: Linear Equations With No Solutions | 1 | 0 | 0 | Linear Equations With No Solutions |
| 13946940 | lesson: The Z-Score | 6 | 2 | 5 | The Mean of a Data Set |
| 13944892 | lesson: Making Predictions Using Trend Lines | 0 | — | — |  |
| 13947210 | review: Defining Definite Integrals Using Left and Right Riemann Sums | 8 | 1 | 7 | Left and Right Riemann Sums in Sigma Notation |
| 13947039 | lesson: Rational Equations With Three Terms | 8 | 2 | 5 | Finding Lowest Common Multiples Using Prime Factorization |
| 13947355 | lesson: Advanced Rational Equations | 25 | 3 | 7 | Finding Lowest Common Multiples Using Prime Factorization |
| 13947257 | review: Differentiating Reciprocal Trigonometric Functions | 26 | 5 | 8 | Calculating the Slope of a Tangent Line Using Differentiation |
