# Statistical breakdown of captured knowledge-band changes

Period: 2026-10-03 17:49:59 PDT through 2026-10-04 20:24:46 PDT.

153 completed activity snapshots; 810 observed band changes; 172 changed topics out of 1039 distinct tracked topics. Prerequisite graph read at database basis 504; this analysis makes no database calls or transactions.

An update is one topic whose displayed color/band differs from its comparison snapshot. This is not every internal knowledge-state update, a per-question update, or evidence that the associated activity caused the change. Band differences are ordinal display steps, not calibrated quantities of knowledge. Each snapshot reads the three course pages sequentially. Every one of the 810 logged changes was cross-checked against its saved before/after snapshot, with zero mismatches.

Shortest graph distance uses only authoritative `:topic/next` prerequisite edges. Upstream goes toward prerequisites, downstream toward dependent topics, and either-direction distance permits both. Assessments/multisteps use the nearest of their captured question topics. Means over changes weight frequently changing topics more heavily.

## Overall activity and topic spread

| Measure | Value |
|---|---|
| Mean updates per activity | 5.29 |
| Median updates per activity | 4 |
| Population SD of updates per activity | 5.60 |
| Range of updates per activity | 0–26 |
| Middle 50% of activities | 1–8 updates |
| 90th percentile | 12.00 |
| 95th percentile | 17.00 |
| Activities with zero updates | 30 (19.6%) |
| Mean updates per nonzero-update activity | 6.59 |
| Mean updates per changed topic | 4.71 |
| Median updates per changed topic | 2.00 |
| Mean updates per tracked topic, including zeros | 0.78 |
| Tracked topics with no changes | 867 (83.4%) |
| Practiced lesson/review topics | 104 |
| Lesson/review activities with own-topic band change | 73/142 (51.4%) |
| Rising / falling updates | 571 (70.5%) / 239 (29.5%) |
| Mean absolute band-step change | 1.35 |

## By activity type

| Type | Activities | Updates | Mean/activity | Median | SD | Maximum | Zero-update activities | Rises | Falls | Mean either-direction edges |
|---|---|---|---|---|---|---|---|---|---|---|
| assessment | 5 | 36 | 7.20 | 5 | 7.36 | 19 | 2 | 25 | 11 | 2.53 |
| lesson | 91 | 518 | 5.69 | 5 | 5.47 | 25 | 14 | 397 | 121 | 4.30 |
| multistep | 6 | 42 | 7 | 6.50 | 4.55 | 13 | 1 | 26 | 16 | 2.98 |
| review | 51 | 214 | 4.20 | 2 | 5.54 | 26 | 13 | 123 | 91 | 4.18 |

## Complete updates-per-activity distribution

| Changed topics after activity | Activities | Share of activities |
|---|---|---|
| 0 | 30 | 19.6% |
| 1 | 22 | 14.4% |
| 2 | 14 | 9.2% |
| 3 | 9 | 5.9% |
| 4 | 8 | 5.2% |
| 5 | 12 | 7.8% |
| 6 | 7 | 4.6% |
| 7 | 6 | 3.9% |
| 8 | 10 | 6.5% |
| 9 | 4 | 2.6% |
| 10 | 7 | 4.6% |
| 11 | 5 | 3.3% |
| 12 | 7 | 4.6% |
| 13 | 1 | 0.7% |
| 14 | 1 | 0.7% |
| 15 | 1 | 0.7% |
| 16 | 0 | 0.0% |
| 17 | 2 | 1.3% |
| 18 | 0 | 0.0% |
| 19 | 1 | 0.7% |
| 20 | 0 | 0.0% |
| 21 | 2 | 1.3% |
| 22 | 2 | 1.3% |
| 23 | 0 | 0.0% |
| 24 | 0 | 0.0% |
| 25 | 1 | 0.7% |
| 26 | 1 | 0.7% |

## Where the changes lie in the prerequisite graph

These four groups are mutually exclusive; they add up to all 810 changes. Other branch means there is an undirected connection but no entirely upstream or downstream path from an activity origin.

| Relation | Updates | Share | Rises | Falls | Mean relevant distance |
|---|---|---|---|---|---|
| Activity topic itself | 84 | 10.4% | 82 | 2 | 0 |
| Prerequisite | 115 | 14.2% | 99 | 16 | 2.45 |
| Downstream dependent | 22 | 2.7% | 16 | 6 | 2.55 |
| Other branch | 589 | 72.7% | 374 | 215 | 5.14 |

## Distance summary

| Distance population | Updates | Mean edges | Median | SD | 90th percentile | 95th percentile | Maximum |
|---|---|---|---|---|---|---|---|
| All changes, either direction | 810 | 4.12 | 5.00 | 2.10 | 6.00 | 7.00 | 8 |
| Activity topic plus prerequisites | 199 | 1.42 | 1 | 1.82 | 4.00 | 5.00 | 9 |
| Prerequisites only | 115 | 2.45 | 2 | 1.79 | 4.60 | 6.00 | 9 |

## Complete distance distribution

Level 0 is the activity topic itself and appears in both directed columns; count it once. The two directed columns do not cover other-branch changes. Either-direction counts cover every update. Up/down below means rising/falling display bands, not graph direction.

| Edges | Prerequisite count | Prerequisite rises | Prerequisite falls | Downstream count | Either-direction count | Either-direction share | Either-direction rises | Either-direction falls | Mean either-direction count/activity |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 84 | 82 | 2 | 84 | 84 | 10.4% | 82 | 2 | 0.55 |
| 1 | 45 | 41 | 4 | 7 | 52 | 6.4% | 46 | 6 | 0.34 |
| 2 | 26 | 24 | 2 | 5 | 45 | 5.6% | 38 | 7 | 0.29 |
| 3 | 22 | 17 | 5 | 5 | 70 | 8.6% | 52 | 18 | 0.46 |
| 4 | 10 | 8 | 2 | 2 | 121 | 14.9% | 68 | 53 | 0.79 |
| 5 | 5 | 2 | 3 | 2 | 192 | 23.7% | 125 | 67 | 1.25 |
| 6 | 2 | 2 | 0 | 1 | 184 | 22.7% | 116 | 68 | 1.20 |
| 7 | 0 | 0 | 0 | 0 | 59 | 7.3% | 43 | 16 | 0.39 |
| 8 | 3 | 3 | 0 | 0 | 3 | 0.4% | 1 | 2 | 0.02 |
| 9 | 2 | 2 | 0 | 0 | 0 | 0.0% | 0 | 0 | 0.00 |

## Size of changes in display bands

| Band step change | Updates | Share |
|---|---|---|
| -5 | 1 | 0.1% |
| -4 | 4 | 0.5% |
| -3 | 14 | 1.7% |
| -2 | 37 | 4.6% |
| -1 | 183 | 22.6% |
| 1 | 439 | 54.2% |
| 2 | 86 | 10.6% |
| 3 | 26 | 3.2% |
| 4 | 15 | 1.9% |
| 5 | 5 | 0.6% |

## Counts starting and ending at each band

| Band | Updates starting here | Rises from here | Falls from here | Updates ending here |
|---|---|---|---|---|
| 0 | 159 | 159 | 0 | 23 |
| 1 | 182 | 159 | 23 | 237 |
| 2 | 154 | 90 | 64 | 178 |
| 3 | 104 | 39 | 65 | 101 |
| 4 | 86 | 60 | 26 | 80 |
| 5 | 89 | 64 | 25 | 101 |
| 6 | 36 | 0 | 36 | 90 |

## Full band transition matrix

Rows are the old band; columns are the new band.

| Old → new | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 137 | 21 | 1 | 0 | 0 | 0 |
| 1 | 23 | 0 | 98 | 35 | 16 | 5 | 5 |
| 2 | 0 | 64 | 0 | 58 | 16 | 6 | 10 |
| 3 | 0 | 25 | 40 | 0 | 30 | 6 | 3 |
| 4 | 0 | 8 | 11 | 7 | 0 | 52 | 8 |
| 5 | 0 | 2 | 6 | 0 | 17 | 0 | 64 |
| 6 | 0 | 1 | 2 | 0 | 1 | 32 | 0 |

## Complete updates-per-tracked-topic distribution

| Updates recorded for a topic | Number of topics |
|---|---|
| 0 | 867 |
| 1 | 72 |
| 2 | 34 |
| 3 | 12 |
| 4 | 8 |
| 5 | 5 |
| 6 | 7 |
| 7 | 2 |
| 8 | 5 |
| 9 | 3 |
| 10 | 2 |
| 11 | 2 |
| 12 | 1 |
| 13 | 4 |
| 14 | 3 |
| 15 | 1 |
| 17 | 1 |
| 19 | 1 |
| 20 | 1 |
| 21 | 2 |
| 22 | 1 |
| 25 | 1 |
| 29 | 2 |
| 43 | 1 |
| 45 | 1 |

## Course breakdown

| Course ID | Tracked topics | Updates | Share | Rises | Falls | Mean either-direction distance |
|---|---|---|---|---|---|---|
| 113 | 357 | 88 | 10.9% | 61 | 27 | 3.78 |
| 111 | 360 | 679 | 83.8% | 489 | 190 | 4.20 |
| 136 | 323 | 43 | 5.3% | 21 | 22 | 3.47 |

The course pages contain 1,040 rows but 1,039 distinct topic IDs because one topic appears in two courses. No update in this dataset is duplicated across courses.

## Reversals and comparison quality

Among 638 successive recorded-change pairs for the same topic/course, 430 (67.4%) reverse direction; 379 (59.4%) exactly undo the previous band transition. These need not be adjacent activities. Frequent reversals mean repeated updates should not be equated with durable learning.

5 snapshots were recovered after interruption and 15 do not compare with the immediately preceding completed snapshot (categories overlap). Restricting to 134 consecutive, unrecovered snapshots leaves 621 updates: mean 4.63 per activity, mean either-direction distance 4.08 edges. The maximum upstream distance remains 9.

## Every changed topic, ranked by update frequency

| Topic ID | Topic | Updates | Rises | Falls | Sum of band steps | Own-topic updates | Prerequisite updates | Mean either-direction edges |
|---|---|---|---|---|---|---|---|---|
| 1453 | Using the Pythagorean Identity in the First Quadrant | 45 | 24 | 21 | 2 | 0 | 2 | 5.24 |
| 1634 | The Mean of a Data Set | 43 | 24 | 19 | 10 | 0 | 2 | 5.12 |
| 774 | Factorials | 29 | 18 | 11 | 10 | 0 | 1 | 4.93 |
| 1531 | Graphing Exponential Decay Functions | 29 | 16 | 13 | 7 | 2 | 2 | 3.83 |
| 817 | Vertical Translations of Exponential Growth Functions | 25 | 14 | 11 | 4 | 1 | 2 | 4.68 |
| 673 | Sigma Notation | 22 | 12 | 10 | 2 | 0 | 1 | 4.68 |
| 332 | Calculating the Slope of a Tangent Line Using Differentiation | 21 | 13 | 8 | 6 | 0 | 11 | 4.05 |
| 3557 | Describing Properties of the Cosine Function | 21 | 12 | 9 | 3 | 0 | 1 | 5.33 |
| 456 | Vertical Translations of Exponential Decay Functions | 20 | 11 | 9 | 2 | 1 | 1 | 4.55 |
| 3558 | Describing Properties of the Tangent Function | 19 | 10 | 9 | 2 | 1 | 1 | 4.79 |
| 167 | Negative Angles in the Coordinate Plane | 17 | 10 | 7 | 3 | 0 | 3 | 6 |
| 729 | Vieta's Formulas | 15 | 10 | 5 | 7 | 1 | 0 | 4.13 |
| 280 | Differentiating Trigonometric Functions | 14 | 10 | 4 | 8 | 1 | 6 | 3.07 |
| 512 | The Distance Formula in Three Dimensions | 14 | 9 | 5 | 4 | 1 | 0 | 4.79 |
| 3566 | Describing Properties of the Cotangent Function | 14 | 7 | 7 | 1 | 1 | 0 | 5.21 |
| 37 | The Power and Root Rules for Limits | 13 | 9 | 4 | 5 | 1 | 2 | 3.62 |
| 278 | The Sum and Constant Multiple Rules for Differentiation | 13 | 11 | 2 | 10 | 0 | 5 | 4.54 |
| 1114 | Differentiating Exponential Functions | 13 | 9 | 4 | 5 | 1 | 5 | 3.31 |
| 2050 | End Behavior of Polynomials | 13 | 9 | 4 | 5 | 1 | 0 | 4.69 |
| 893 | The Argument of a Complex Number | 12 | 7 | 5 | 2 | 1 | 0 | 5.25 |
| 846 | The Factor Theorem | 11 | 7 | 4 | 3 | 0 | 2 | 4.82 |
| 3769 | The Sum Rule for Indefinite Integrals | 11 | 6 | 5 | 1 | 0 | 3 | 3.55 |
| 203 | Simplifying Expressions Using Basic Trigonometric Identities | 10 | 4 | 6 | -2 | 0 | 0 | 3.10 |
| 606 | Special Limits Involving Sine | 10 | 4 | 6 | -2 | 0 | 0 | 3.70 |
| 1087 | Limits of Sequences | 9 | 4 | 5 | -1 | 0 | 0 | 4.33 |
| 1719 | Limits of Trigonometric Functions | 9 | 5 | 4 | 0 | 1 | 1 | 3.67 |
| 1903 | Limits at Infinity and Horizontal Asymptotes of Rational Functions | 9 | 4 | 5 | -1 | 0 | 0 | 4.33 |
| 161 | The Rules of Sum and Product | 8 | 6 | 2 | 7 | 0 | 1 | 5.38 |
| 1263 | Limits at Infinity of Polynomials | 8 | 7 | 1 | 6 | 1 | 0 | 4.62 |
| 1289 | The Power of Quotient Rule for Exponents | 8 | 5 | 3 | 3 | 0 | 3 | 4.38 |
| 1530 | Graphing Exponential Growth Functions | 8 | 5 | 3 | 5 | 0 | 3 | 3.88 |
| 1644 | Heights of Triangles | 8 | 5 | 3 | 2 | 1 | 2 | 4.12 |
| 775 | Ordering Objects | 7 | 5 | 2 | 6 | 1 | 0 | 5 |
| 1583 | Solving Exponential Equations With Different Bases | 7 | 6 | 1 | 10 | 1 | 0 | 4.43 |
| 454 | Graphing the Cube Root Function | 6 | 4 | 2 | 2 | 0 | 1 | 5.17 |
| 1397 | Areas of Triangles | 6 | 4 | 2 | 2 | 1 | 2 | 2.83 |
| 1654 | Graphing Cubic Curves Containing Three Distinct Real Roots | 6 | 6 | 0 | 6 | 0 | 2 | 5 |
| 1656 | Graphing Cubic Curves Containing a Double Root | 6 | 6 | 0 | 17 | 0 | 2 | 5.33 |
| 1814 | Infinite Limits from Graphs | 6 | 3 | 3 | 0 | 0 | 1 | 3.83 |
| 1986 | Limits of Radical Functions | 6 | 4 | 2 | 2 | 0 | 1 | 5.50 |
| 2049 | Graphing General Polynomials | 6 | 6 | 0 | 6 | 2 | 0 | 3.83 |
| 705 | Combinations | 5 | 5 | 0 | 5 | 1 | 0 | 4.80 |
| 807 | Vertical Asymptotes of Rational Functions | 5 | 5 | 0 | 5 | 1 | 0 | 4 |
| 1682 | Vertical Reflections of Exponential Functions | 5 | 5 | 0 | 5 | 1 | 0 | 4.20 |
| 1873 | Limits at Infinity from Graphs | 5 | 5 | 0 | 25 | 0 | 1 | 4.40 |
| 1889 | Invertible Functions | 5 | 5 | 0 | 5 | 0 | 0 | 5.60 |
| 285 | Integrating Trigonometric Functions | 4 | 3 | 1 | 2 | 2 | 0 | 1.75 |
| 312 | Integrating Exponential Functions | 4 | 3 | 1 | 2 | 1 | 0 | 3.50 |
| 755 | Finding Lowest Common Multiples Using Prime Factorization | 4 | 3 | 1 | 2 | 0 | 2 | 5 |
| 1007 | The Chain Rule With Exponential Functions | 4 | 4 | 0 | 4 | 1 | 0 | 3.50 |
| 1081 | Systems of Linear Equations With Decimal Coefficients | 4 | 3 | 1 | 2 | 0 | 1 | 4.25 |
| 1109 | The Product Rule for Differentiation | 4 | 3 | 1 | 2 | 0 | 1 | 3.75 |
| 1573 | Graphing Secant and Cosecant | 4 | 4 | 0 | 5 | 0 | 3 | 2.25 |
| 3725 | Properties of Lines Given in Standard Form | 4 | 4 | 0 | 4 | 0 | 1 | 4.50 |
| 88 | Multiplicities of the Roots of Polynomials | 3 | 2 | 1 | 1 | 0 | 0 | 5 |
| 259 | Graphing Reflections of Trigonometric Functions | 3 | 2 | 1 | 1 | 0 | 0 | 6.33 |
| 388 | Solving Compound Inequalities | 3 | 2 | 1 | 1 | 1 | 0 | 3.67 |
| 703 | Permutations | 3 | 3 | 0 | 3 | 0 | 0 | 5.67 |
| 757 | The Rational Roots Theorem | 3 | 3 | 0 | 3 | 2 | 0 | 1.67 |
| 1108 | The Chain Rule for Differentiation | 3 | 3 | 0 | 3 | 0 | 0 | 4.67 |
| 1116 | Differentiating Logarithmic Functions | 3 | 3 | 0 | 3 | 1 | 0 | 4 |
| 1249 | Calculating Derivatives From Data and Tables | 3 | 3 | 0 | 3 | 2 | 0 | 2.33 |
| 1427 | Perpendicular Lines in the Coordinate Plane | 3 | 3 | 0 | 3 | 1 | 0 | 3.33 |
| 2033 | Graphing Reciprocal Functions | 3 | 3 | 0 | 7 | 0 | 2 | 3.33 |
| 2148 | Periodic Functions | 3 | 3 | 0 | 3 | 0 | 2 | 4 |
| 3735 | Graph Transformations of Reciprocal Functions | 3 | 3 | 0 | 6 | 0 | 2 | 2.67 |
| 34 | The Magnitude of a Complex Number | 2 | 2 | 0 | 2 | 0 | 0 | 6.50 |
| 43 | The Constant Multiple Rule for Indefinite Integrals | 2 | 2 | 0 | 3 | 1 | 0 | 2 |
| 116 | Solving Radical Equations | 2 | 2 | 0 | 6 | 0 | 1 | 3 |
| 141 | Finding Points on Transformed Curves | 2 | 2 | 0 | 2 | 2 | 0 | 0 |
| 206 | Vertical Translations of Trigonometric Functions | 2 | 1 | 1 | 0 | 0 | 0 | 5.50 |
| 281 | Second and Higher-Order Derivatives | 2 | 2 | 0 | 2 | 2 | 0 | 0 |
| 296 | Interpreting the Meaning of the Derivative in Context | 2 | 2 | 0 | 2 | 1 | 0 | 2.50 |
| 419 | Solving Quadratic Equations by Completing the Square | 2 | 2 | 0 | 2 | 1 | 0 | 1.50 |
| 455 | Combining Graph Transformations of Reciprocal Functions | 2 | 2 | 0 | 2 | 1 | 0 | 2 |
| 462 | Determining Continuity from Graphs | 2 | 1 | 1 | 0 | 0 | 0 | 6.50 |
| 469 | Determining the Roots of Polynomials | 2 | 2 | 0 | 2 | 0 | 0 | 4 |
| 485 | Midpoints in the Coordinate Plane | 2 | 2 | 0 | 2 | 1 | 0 | 2.50 |
| 627 | Calculating the Inverse of a Function | 2 | 2 | 0 | 4 | 1 | 0 | 2.50 |
| 654 | Graph Transformations of Tangent and Cotangent | 2 | 1 | 1 | 0 | 0 | 0 | 6 |
| 735 | Complex Numbers | 2 | 2 | 0 | 2 | 0 | 0 | 4 |
| 895 | Solving Quadratic Equations With Complex Roots | 2 | 2 | 0 | 8 | 0 | 0 | 2.50 |
| 1042 | Left and Right Riemann Sums in Sigma Notation | 2 | 2 | 0 | 4 | 0 | 2 | 1 |
| 1102 | Problem Solving Using Vector Diagrams | 2 | 2 | 0 | 2 | 0 | 1 | 4 |
| 1153 | Exponential Functions | 2 | 2 | 0 | 5 | 0 | 0 | 4.50 |
| 1361 | Integrating the Reciprocal Function | 2 | 2 | 0 | 2 | 1 | 0 | 1 |
| 1473 | The Product Rule for Logarithms | 2 | 1 | 1 | 0 | 0 | 0 | 5.50 |
| 1482 | Solving Exponential Equations Using Logarithms | 2 | 2 | 0 | 5 | 0 | 1 | 2.50 |
| 1491 | Graphing Sine and Cosine | 2 | 2 | 0 | 2 | 0 | 1 | 4 |
| 1493 | Graphing Tangent and Cotangent | 2 | 2 | 0 | 2 | 0 | 2 | 2.50 |
| 1661 | Vertical Stretches of Trigonometric Functions | 2 | 1 | 1 | 0 | 0 | 0 | 6 |
| 2021 | Extending the Pythagorean Identity to All Quadrants | 2 | 2 | 0 | 2 | 1 | 0 | 3.50 |
| 2082 | Domain and Range of Transformed Reciprocal Functions | 2 | 2 | 0 | 2 | 1 | 0 | 1.50 |
| 2119 | Factoring Cubic Polynomials Using the Factor Theorem | 2 | 2 | 0 | 2 | 0 | 1 | 3 |
| 2625 | The Least Common Multiple of Two Monomials | 2 | 2 | 0 | 3 | 0 | 2 | 1 |
| 2979 | Solving Exponential Equations Using the Zero-Product Property | 2 | 2 | 0 | 2 | 0 | 0 | 5.50 |
| 3540 | Describing Properties of the Sine Function | 2 | 2 | 0 | 2 | 0 | 2 | 1.50 |
| 3562 | Finding Equations of Perpendicular Lines | 2 | 2 | 0 | 2 | 1 | 0 | 3 |
| 3563 | Describing Properties of the Secant Function | 2 | 2 | 0 | 2 | 0 | 0 | 5.50 |
| 3944 | Inverses of Reciprocal Functions | 2 | 2 | 0 | 8 | 0 | 0 | 1.50 |
| 28 | The Change of Base Formula for Logarithms | 1 | 1 | 0 | 4 | 0 | 1 | 2 |
| 30 | Combining the Laws of Logarithms | 1 | 1 | 0 | 1 | 0 | 1 | 1 |
| 157 | The Complex Plane | 1 | 1 | 0 | 1 | 0 | 1 | 1 |
| 175 | Addition and Scalar Multiplication of Cartesian Vectors in 3D | 1 | 1 | 0 | 2 | 1 | 0 | 0 |
| 226 | Solving Logarithmic Equations | 1 | 1 | 0 | 1 | 0 | 1 | 2 |
| 244 | Addition and Scalar Multiplication of Cartesian Vectors in 2D | 1 | 1 | 0 | 2 | 0 | 1 | 1 |
| 261 | Coterminal Angles | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 305 | The Chain Rule With Trigonometric Functions | 1 | 1 | 0 | 1 | 0 | 0 | 2 |
| 314 | Defining Continuity at a Point | 1 | 1 | 0 | 1 | 0 | 0 | 5 |
| 408 | Calculating the Intersection of Two Lines | 1 | 1 | 0 | 3 | 0 | 1 | 1 |
| 437 | Adding and Subtracting Rational Expressions | 1 | 1 | 0 | 4 | 0 | 1 | 1 |
| 440 | Rational Equations With Three Terms | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 450 | Completing the Square | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 459 | The Distance Formula | 1 | 1 | 0 | 1 | 0 | 1 | 1 |
| 474 | Left and Right Continuity | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 526 | The Shortest Distance Between a Point and a Line | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 558 | Solving Problems Using Unit Rates | 1 | 1 | 0 | 1 | 0 | 0 | 4 |
| 563 | Reasoning With Equivalent Ratios | 1 | 1 | 0 | 3 | 0 | 1 | 1 |
| 612 | Continuity Over an Interval | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 708 | Advanced Rational Equations | 1 | 1 | 0 | 1 | 0 | 0 | 7 |
| 711 | The Z-Score | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 742 | Introduction to the Elimination Method | 1 | 1 | 0 | 1 | 0 | 1 | 4 |
| 778 | Properties of Transformed Secant and Cosecant Functions | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 870 | Solving Equations Containing the Exponential Function | 1 | 1 | 0 | 1 | 0 | 0 | 3 |
| 986 | Calculating the Equation of a Tangent Line Using Differentiation | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 987 | Calculating the Equation of a Normal Line Using Differentiation | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 1036 | The Chain Rule With Logarithmic Functions | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 1045 | Systems of Linear Equations With Fractional Coefficients | 1 | 1 | 0 | 1 | 0 | 0 | 4 |
| 1086 | Defining Definite Integrals Using Left and Right Riemann Sums | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 1106 | Describing the Position Vector of a Point Using Known Vectors | 1 | 1 | 0 | 1 | 0 | 0 | 6 |
| 1110 | The Quotient Rule for Differentiation | 1 | 1 | 0 | 1 | 0 | 0 | 3 |
| 1115 | Selecting Procedures for Calculating Derivatives | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 1117 | Calculating Derivatives From Graphs | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 1166 | Three-Dimensional Vectors in Component Form | 1 | 1 | 0 | 1 | 0 | 1 | 1 |
| 1252 | Vertical Stretches of Functions | 1 | 1 | 0 | 1 | 0 | 1 | 4 |
| 1254 | Combining Graph Transformations: Two Operations | 1 | 1 | 0 | 1 | 0 | 1 | 3 |
| 1262 | Limits of Piecewise Functions | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 1275 | The Area of a General Triangle | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 1414 | Linear Equations With Infinitely Many Solutions | 1 | 1 | 0 | 2 | 0 | 0 | 4 |
| 1475 | The Power Rule for Logarithms | 1 | 1 | 0 | 2 | 0 | 1 | 2 |
| 1551 | Solving Logarithmic Equations Containing the Natural Logarithm | 1 | 1 | 0 | 1 | 0 | 0 | 3 |
| 1608 | Calculating Areas of Right Triangles Using Trigonometry | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 1609 | Properties of Transformed Exponential Functions | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 1632 | Variance and Standard Deviation | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 1686 | Differentiating Reciprocal Trigonometric Functions | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 1717 | Limits of Exponential Functions | 1 | 1 | 0 | 1 | 0 | 0 | 4 |
| 2046 | Unbounded Behavior of Functions Near a Point | 1 | 1 | 0 | 1 | 0 | 1 | 3 |
| 2062 | Properties of Transformed Sine and Cosine Functions | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 2064 | Properties of Transformed Tangent and Cotangent Functions | 1 | 1 | 0 | 1 | 0 | 0 | 6 |
| 2327 | Speed-Time Graphs | 1 | 1 | 0 | 2 | 0 | 0 | 3 |
| 2468 | Nets of Polyhedrons | 1 | 1 | 0 | 1 | 0 | 1 | 1 |
| 2484 | Faces, Vertices, and Edges of Polyhedrons | 1 | 1 | 0 | 1 | 0 | 1 | 2 |
| 2585 | Scatter Plots | 1 | 1 | 0 | 2 | 1 | 0 | 0 |
| 2609 | Trend Lines | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 2626 | The Least Common Multiple of Two Polynomials | 1 | 1 | 0 | 2 | 1 | 0 | 0 |
| 3567 | Describing Properties of the Cosecant Function | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 3591 | Covariance | 1 | 1 | 0 | 1 | 0 | 0 | 5 |
| 3593 | Speed as a Unit Rate | 1 | 1 | 0 | 2 | 0 | 0 | 4 |
| 3710 | Factorials in Variable Expressions | 1 | 1 | 0 | 2 | 1 | 0 | 0 |
| 3737 | Solving Exponential Equations With Different Bases Using Logarithms | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 3739 | Adding Rational Expressions With No Common Factors in the Denominator | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 3746 | Further Reasoning With Equivalent Ratios | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 3753 | Making Predictions Using Trend Lines | 1 | 1 | 0 | 2 | 0 | 0 | 7 |
| 3824 | Completing the Square With Leading Coefficients | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 3842 | Completing the Square With Odd Linear Terms | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 3849 | Solving Quadratic Equations With Leading Coefficients by Completing the Square | 1 | 1 | 0 | 1 | 0 | 0 | 5 |
| 3850 | Combining Graph Transformations of Tangent and Cotangent | 1 | 1 | 0 | 1 | 0 | 0 | 6 |
| 4026 | Solving Systems of Linear Equations Using Elimination: One Transformation | 1 | 1 | 0 | 1 | 0 | 1 | 3 |
| 4236 | Solving Systems of Linear Equations Using Elimination: Two Transformations | 1 | 1 | 0 | 1 | 0 | 0 | 3 |
| 5088 | Finding Zeros and Extrema of Transformed Sine and Cosine Functions | 1 | 1 | 0 | 1 | 1 | 0 | 0 |
| 5572 | Linear Equations With No Solutions | 1 | 1 | 0 | 2 | 1 | 0 | 0 |
| 6351 | Combining Graph Transformations of Exponential Functions | 1 | 1 | 0 | 1 | 1 | 0 | 0 |

## Every practiced lesson/review topic, ranked by mean associated changes

This groups by the activity topic. It describes changes observed after its activities, without claiming they were caused by it. Small sample sizes should not be used to rank intrinsic topic effects. Assessments and multisteps are excluded because they have multiple origins.

| Topic ID | Topic | Activities | Associated updates | Mean updates/activity | Activities with own-topic change |
|---|---|---|---|---|---|
| 708 | Advanced Rational Equations | 1 | 25 | 25 | 0 |
| 280 | Differentiating Trigonometric Functions | 1 | 22 | 22 | 1 |
| 305 | The Chain Rule With Trigonometric Functions | 1 | 21 | 21 | 0 |
| 1686 | Differentiating Reciprocal Trigonometric Functions | 2 | 37 | 18.50 | 1 |
| 526 | The Shortest Distance Between a Point and a Line | 1 | 14 | 14 | 1 |
| 281 | Second and Higher-Order Derivatives | 2 | 27 | 13.50 | 1 |
| 987 | Calculating the Equation of a Normal Line Using Differentiation | 2 | 25 | 12.50 | 1 |
| 1106 | Describing the Position Vector of a Point Using Known Vectors | 2 | 24 | 12 | 0 |
| 2609 | Trend Lines | 1 | 12 | 12 | 1 |
| 2626 | The Least Common Multiple of Two Polynomials | 1 | 12 | 12 | 1 |
| 3591 | Covariance | 1 | 12 | 12 | 0 |
| 807 | Vertical Asymptotes of Rational Functions | 2 | 22 | 11 | 1 |
| 2049 | Graphing General Polynomials | 2 | 22 | 11 | 2 |
| 1453 | Using the Pythagorean Identity in the First Quadrant | 1 | 11 | 11 | 0 |
| 1958 | Limits of Reciprocal Trigonometric Functions | 1 | 11 | 11 | 0 |
| 1117 | Calculating Derivatives From Graphs | 1 | 10 | 10 | 1 |
| 1262 | Limits of Piecewise Functions | 1 | 10 | 10 | 1 |
| 1608 | Calculating Areas of Right Triangles Using Trigonometry | 1 | 10 | 10 | 1 |
| 3710 | Factorials in Variable Expressions | 1 | 10 | 10 | 1 |
| 1644 | Heights of Triangles | 1 | 9 | 9 | 1 |
| 3558 | Describing Properties of the Tangent Function | 1 | 9 | 9 | 1 |
| 1036 | The Chain Rule With Logarithmic Functions | 2 | 17 | 8.50 | 1 |
| 440 | Rational Equations With Three Terms | 1 | 8 | 8 | 1 |
| 1115 | Selecting Procedures for Calculating Derivatives | 1 | 8 | 8 | 1 |
| 1414 | Linear Equations With Infinitely Many Solutions | 1 | 8 | 8 | 0 |
| 3824 | Completing the Square With Leading Coefficients | 1 | 8 | 8 | 1 |
| 2082 | Domain and Range of Transformed Reciprocal Functions | 2 | 15 | 7.50 | 1 |
| 2021 | Extending the Pythagorean Identity to All Quadrants | 2 | 14 | 7 | 1 |
| 285 | Integrating Trigonometric Functions | 1 | 7 | 7 | 1 |
| 6351 | Combining Graph Transformations of Exponential Functions | 1 | 7 | 7 | 1 |
| 419 | Solving Quadratic Equations by Completing the Square | 2 | 12 | 6 | 1 |
| 1682 | Vertical Reflections of Exponential Functions | 2 | 12 | 6 | 1 |
| 314 | Defining Continuity at a Point | 1 | 6 | 6 | 0 |
| 711 | The Z-Score | 1 | 6 | 6 | 1 |
| 1045 | Systems of Linear Equations With Fractional Coefficients | 1 | 6 | 6 | 0 |
| 1275 | The Area of a General Triangle | 1 | 6 | 6 | 1 |
| 3746 | Further Reasoning With Equivalent Ratios | 1 | 6 | 6 | 1 |
| 1110 | The Quotient Rule for Differentiation | 2 | 11 | 5.50 | 0 |
| 1632 | Variance and Standard Deviation | 2 | 11 | 5.50 | 1 |
| 1361 | Integrating the Reciprocal Function | 2 | 10 | 5 | 1 |
| 1531 | Graphing Exponential Decay Functions | 2 | 10 | 5 | 2 |
| 627 | Calculating the Inverse of a Function | 1 | 5 | 5 | 1 |
| 817 | Vertical Translations of Exponential Growth Functions | 1 | 5 | 5 | 1 |
| 3530 | Roots of Transformed Radical Functions | 1 | 5 | 5 | 0 |
| 3567 | Describing Properties of the Cosecant Function | 1 | 5 | 5 | 1 |
| 5088 | Finding Zeros and Extrema of Transformed Sine and Cosine Functions | 1 | 5 | 5 | 1 |
| 1086 | Defining Definite Integrals Using Left and Right Riemann Sums | 2 | 9 | 4.50 | 1 |
| 1249 | Calculating Derivatives From Data and Tables | 2 | 9 | 4.50 | 2 |
| 705 | Combinations | 3 | 13 | 4.33 | 1 |
| 450 | Completing the Square | 2 | 8 | 4 | 1 |
| 1263 | Limits at Infinity of Polynomials | 2 | 8 | 4 | 1 |
| 3739 | Adding Rational Expressions With No Common Factors in the Denominator | 2 | 8 | 4 | 1 |
| 259 | Graphing Reflections of Trigonometric Functions | 1 | 4 | 4 | 0 |
| 312 | Integrating Exponential Functions | 1 | 4 | 4 | 0 |
| 388 | Solving Compound Inequalities | 1 | 4 | 4 | 1 |
| 1114 | Differentiating Exponential Functions | 1 | 4 | 4 | 1 |
| 1116 | Differentiating Logarithmic Functions | 2 | 7 | 3.50 | 1 |
| 3563 | Describing Properties of the Secant Function | 2 | 7 | 3.50 | 0 |
| 1427 | Perpendicular Lines in the Coordinate Plane | 2 | 6 | 3 | 1 |
| 175 | Addition and Scalar Multiplication of Cartesian Vectors in 3D | 1 | 3 | 3 | 1 |
| 474 | Left and Right Continuity | 1 | 3 | 3 | 1 |
| 775 | Ordering Objects | 1 | 3 | 3 | 1 |
| 1397 | Areas of Triangles | 1 | 3 | 3 | 1 |
| 2062 | Properties of Transformed Sine and Cosine Functions | 1 | 3 | 3 | 1 |
| 3566 | Describing Properties of the Cotangent Function | 1 | 3 | 3 | 1 |
| 1109 | The Product Rule for Differentiation | 2 | 5 | 2.50 | 0 |
| 456 | Vertical Translations of Exponential Decay Functions | 3 | 7 | 2.33 | 1 |
| 455 | Combining Graph Transformations of Reciprocal Functions | 2 | 4 | 2 | 1 |
| 1108 | The Chain Rule for Differentiation | 2 | 4 | 2 | 0 |
| 512 | The Distance Formula in Three Dimensions | 1 | 2 | 2 | 1 |
| 778 | Properties of Transformed Secant and Cosecant Functions | 1 | 2 | 2 | 1 |
| 1609 | Properties of Transformed Exponential Functions | 1 | 2 | 2 | 1 |
| 2469 | Finding Surface Areas Using Nets | 1 | 2 | 2 | 0 |
| 870 | Solving Equations Containing the Exponential Function | 2 | 3 | 1.50 | 0 |
| 986 | Calculating the Equation of a Tangent Line Using Differentiation | 2 | 3 | 1.50 | 1 |
| 1007 | The Chain Rule With Exponential Functions | 2 | 3 | 1.50 | 0 |
| 141 | Finding Points on Transformed Curves | 2 | 2 | 1 | 2 |
| 703 | Permutations | 2 | 2 | 1 | 0 |
| 893 | The Argument of a Complex Number | 2 | 2 | 1 | 1 |
| 88 | Multiplicities of the Roots of Polynomials | 1 | 1 | 1 | 0 |
| 296 | Interpreting the Meaning of the Derivative in Context | 1 | 1 | 1 | 1 |
| 612 | Continuity Over an Interval | 1 | 1 | 1 | 1 |
| 757 | The Rational Roots Theorem | 1 | 1 | 1 | 1 |
| 1583 | Solving Exponential Equations With Different Bases | 1 | 1 | 1 | 1 |
| 2050 | End Behavior of Polynomials | 1 | 1 | 1 | 1 |
| 2585 | Scatter Plots | 1 | 1 | 1 | 1 |
| 3557 | Describing Properties of the Cosine Function | 1 | 1 | 1 | 0 |
| 3737 | Solving Exponential Equations With Different Bases Using Logarithms | 1 | 1 | 1 | 1 |
| 3842 | Completing the Square With Odd Linear Terms | 1 | 1 | 1 | 1 |
| 5572 | Linear Equations With No Solutions | 1 | 1 | 1 | 1 |
| 3562 | Finding Equations of Perpendicular Lines | 2 | 1 | 0.50 | 1 |
| 1889 | Invertible Functions | 2 | 0 | 0 | 0 |
| 278 | The Sum and Constant Multiple Rules for Differentiation | 1 | 0 | 0 | 0 |
| 332 | Calculating the Slope of a Tangent Line Using Differentiation | 1 | 0 | 0 | 0 |
| 462 | Determining Continuity from Graphs | 1 | 0 | 0 | 0 |
| 1081 | Systems of Linear Equations With Decimal Coefficients | 1 | 0 | 0 | 0 |
| 1634 | The Mean of a Data Set | 1 | 0 | 0 | 0 |
| 1717 | Limits of Exponential Functions | 1 | 0 | 0 | 0 |
| 2064 | Properties of Transformed Tangent and Cotangent Functions | 1 | 0 | 0 | 0 |
| 2979 | Solving Exponential Equations Using the Zero-Product Property | 1 | 0 | 0 | 0 |
| 3593 | Speed as a Unit Rate | 1 | 0 | 0 | 0 |
| 3753 | Making Predictions Using Trend Lines | 1 | 0 | 0 | 0 |
| 3849 | Solving Quadratic Equations With Leading Coefficients by Completing the Square | 1 | 0 | 0 | 0 |
| 3850 | Combining Graph Transformations of Tangent and Cotangent | 1 | 0 | 0 | 0 |

