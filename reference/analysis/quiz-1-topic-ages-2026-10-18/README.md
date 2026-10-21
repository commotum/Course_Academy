# Topics in captured Quiz 1s and their learning ages

Read-only audit, October 18, 2026. No scheduler or database changes.

## Result

Found 15 ordinary course-level Quiz 1 tasks across four captured accounts, containing 123 topic appearances. Successful same-account lesson timestamps were available for 100 appearances; all 100 were at least 48 hours old at the first captured quiz offer. The other 23 remain unknown. These are appearances, not 100 independent learners or necessarily 100 distinct topics. Ten quizzes have complete age coverage, four have partial coverage, and one has no matched lesson dates.

The youngest matched topic was Interiors and Boundaries of Sets, approximately 48.036 hours old. The original interruption capture bounds its successful lesson completion; the later recovery snapshot is not used as its learning time. The observed boundary supports retaining a per-topic age floor as a working model. It does not prove a backend hard cutoff or exclude a sufficiently strong age-weighting policy. There is no demonstrated numerical oldest-topic multiplier in this audit.

A four-topic Quiz 1 was captured for the multivariable account after switching to Linear Algebra (14234848). A rule requiring five new topics in every assessment would therefore be a local product choice, not a recovered universal Math Academy minimum. A course-level Quiz 1 is not necessarily that account's first-ever quiz.

[Full question/topic/lesson/offer evidence](evidence.json) · [Per-topic CSV](topics.csv)

## Summary

| Account | Course | Quiz task | Topics | At least 48h | Under 48h | Unknown | Known ages (hours) |
|---|---|---:|---:|---:|---:|---:|---|
| foundations | Mathematical Foundations III | 13949162 | 13 | 0 | 0 | 13 | Unknown |
| multivariable | Multivariable Calculus | 14093183 | 9 | 9 | 0 | 0 | 48.036–56.885 |
| linear | Linear Algebra | 14093211 | 10 | 10 | 0 | 0 | 48.744–54.462 |
| differential | Differential Equations | 14093248 | 7 | 7 | 0 | 0 | 48.498–55.376 |
| linear | Methods of Proof | 14097922 | 7 | 7 | 0 | 0 | 48.455–62.333 |
| foundations | Mathematical Methods for the Physical Sciences I | 14116310 | 6 | 6 | 0 | 0 | 48.160–48.853 |
| differential | Mathematics for Machine Learning | 14165325 | 6 | 6 | 0 | 0 | 48.097–48.914 |
| multivariable | Mathematical Methods for the Physical Sciences II | 14177361 | 8 | 6 | 0 | 2 | 50.756–125.509 |
| linear | Mathematical Foundations I | 14196134 | 12 | 12 | 0 | 0 | 48.270–50.171 |
| linear | Mathematical Foundations II | 14199677 | 10 | 6 | 0 | 4 | 49.029–56.442 |
| multivariable | Calculus II | 14220202 | 6 | 6 | 0 | 0 | 49.354–164.613 |
| foundations | Mathematical Methods for the Physical Sciences II | 14220773 | 7 | 7 | 0 | 0 | 49.910–101.167 |
| multivariable | Linear Algebra | 14234848 | 4 | 4 | 0 | 0 | 63.169–95.374 |
| multivariable | Methods of Proof | 14252104 | 7 | 4 | 0 | 3 | 54.141–100.732 |
| linear | Mathematical Foundations III | 14273614 | 11 | 10 | 0 | 1 | 50.966–213.241 |

## Method and limits

- Identify exact Quiz 1 titles, excluding retakes, from the frozen October 11 activity audit and all 4,409 modern activity metadata records present during this run. This found six quizzes in the earlier audit plus nine newer quizzes.
- Read each quiz's original captured content and verify all 123 question topic IDs against their `/topics/<id>#<kp>` source attribution links. Each quiz contained one question per distinct topic.
- Reconstruct first saved offers from the earlier audit and 4,404 modern post-activity records, inspecting their saved unlocked dashboard cards. Use original-document capture times when available. All 15 quizzes had a captured offer; none required a start/completion fallback.
- Match only successful lesson completions from the same account and topic. Use the earliest observed successful acquisition across that account's course switches. Ordinary reviews do not replace the lesson anchor. Shared curriculum is used for topic/course names only, never another learner's learning dates.
- Preserve the two original completion-bound corrections documented in the October 11 topic-age audit. The Multivariable Quiz 1 correction is material here; the Speed-Time Graphs correction concerns later quizzes.
- Unknown lesson dates do not count as younger than 48 hours or as confirmed compliance. Earlier unobserved learning may exist. Diagnostic resets and relearning can make the first observed historical lesson different from the current acquisition event.
- A first saved offer can be later than backend creation. These are observational ages, not exact internal eligibility timestamps. The sample cannot prove Math Academy's complete current algorithm.

Earlier analyses: [topic-age report](../../mathacademy/capture-audits/2026-10-11-assessment-patterns/topic-age-report.md), [original availability report](../../mathacademy/capture-audits/2026-10-11-assessment-patterns/report.md), [topic-sampling audit](../assessment-topic-sampling-2026-10-12/README.md).

## Every included topic

### foundations · Mathematical Foundations III · Quiz 1 (13949162)

First captured offer: 2026-10-05T06:23:19.435716+00:00. [Captured questions](../../../reference/mathacademy/question-capture/13949162/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| Midpoints in the Coordinate Plane | 485 | Unknown | Not captured |
| The Rational Roots Theorem | 757 | Unknown | Not captured |
| Vieta's Formulas | 729 | Unknown | Not captured |
| The Constant Multiple Rule for Indefinite Integrals | 43 | Unknown | Not captured |
| Adding and Subtracting Rational Expressions | 437 | Unknown | Not captured |
| Properties of Transformed Logarithmic Functions | 1610 | Unknown | Not captured |
| Solving Quadratic Equations With Complex Roots | 895 | Unknown | Not captured |
| Coterminal Angles | 261 | Unknown | Not captured |
| The Rules of Sum and Product | 161 | Unknown | Not captured |
| The Power and Root Rules for Limits | 37 | Unknown | Not captured |
| Inverses of Reciprocal Functions | 3944 | Unknown | Not captured |
| Fibonacci Sequences | 73 | Unknown | Not captured |
| Finding Trigonometric Ratios of Special Angles Using the Unit Circle | 268 | Unknown | Not captured |

### multivariable · Multivariable Calculus · Quiz 1 (14093183)

First captured offer: 2026-10-10T08:13:14.767689+00:00. [Captured questions](../../../reference/mathacademy/question-capture-workers/multivariable/14093183/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| The Inverse of an Affine Transformation | 3707 | 50.207 h | 14040441 |
| Surfaces in Spherical Polar Coordinates | 3570 | 48.226 h | 14038412 |
| Type I and II Regions in Two-Dimensional Space | 1979 | 52.982 h | 14038811 |
| Moments and Center of Mass | 2026 | 49.742 h | 14033857 |
| Double Summations | 1983 | 50.689 h | 14033856 |
| Interiors and Boundaries of Sets | 4063 | 48.036 h | 14041552 |
| The Domain of a Vector-Valued Function | 1737 | 56.885 h | 14033854 |
| Probability Density Functions of Continuous Random Variables | 1347 | 51.364 h | 14040017 |
| Solving First-Order ODEs Using Separation of Variables | 466 | 48.558 h | 14041320 |

### linear · Linear Algebra · Quiz 1 (14093211)

First captured offer: 2026-10-10T08:16:25.024843+00:00. [Captured questions](../../../reference/mathacademy/question-capture-workers/linear/14093211/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| The Determinant of an NxN Matrix | 1769 | 49.757 h | 14039717 |
| Indexed Sets | 55 | 52.824 h | 14038863 |
| Solving 3x3 Systems of Equations Using Gaussian Elimination | 1048 | 50.696 h | 14040313 |
| Vectors in N-Dimensional Euclidean Space | 1849 | 54.462 h | 14037236 |
| Matrices With Easy-to-Find Inverses | 42 | 48.889 h | 14041215 |
| The Vector Equation of a Line | 1376 | 48.744 h | 14041286 |
| Integration Using the Double-Angle Formulas | 1038 | 49.872 h | 14040629 |
| Inverses of 2x2 Matrices | 864 | 52.006 h | 14039644 |
| Introduction to Integration by Parts | 317 | 53.959 h | 14038125 |
| Equations of Ellipses Centered at the Origin | 848 | 52.445 h | 14039348 |

### differential · Differential Equations · Quiz 1 (14093248)

First captured offer: 2026-10-10T08:20:24.711704+00:00. [Captured questions](../../../reference/mathacademy/question-capture-workers/differential/14093248/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| General Solutions of First-Order Linear ODEs | 6678 | 53.212 h | 14037647 |
| Introduction to Recurrence Relations | 1989 | 54.263 h | 14036387 |
| The Norm of a Vector in Inner Product Spaces | 2098 | 50.151 h | 14040608 |
| Introduction to Systems of Linear ODEs | 2086 | 51.876 h | 14037202 |
| The Floor and Ceiling Functions | 290 | 55.376 h | 14036384 |
| Differential Operators | 650 | 54.505 h | 14036386 |
| Analyzing Slope Fields for Autonomous Differential Equations | 3220 | 48.498 h | 14040443 |

### linear · Methods of Proof · Quiz 1 (14097922)

First captured offer: 2026-10-10T15:33:10.906039+00:00. [Captured questions](../../../reference/mathacademy/question-capture-workers/linear/14097922/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| Set Complements | 2829 | 62.333 h | 14035973 |
| Statements and Predicates | 58 | 61.997 h | 14037109 |
| The Area Bounded by a Curve and the X-Axis | 1040 | 56.932 h | 14040771 |
| The Fundamental Theorem of Algebra with Cubic Equations | 896 | 58.837 h | 14039932 |
| Calculating a Scalar Projection | 1285 | 49.768 h | 14046465 |
| Powers of Matrices | 1725 | 48.455 h | 14048771 |
| The Complex Plane | 157 | 61.886 h | 14035975 |

### foundations · Mathematical Methods for the Physical Sciences I · Quiz 1 (14116310)

First captured offer: 2026-10-11T09:46:18.896251+00:00. [Captured questions](../../../reference/mathacademy/capture/foundations/14116310/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| Introduction to First-Order Linear ODEs | 906 | 48.728 h | 14071102 |
| Systems of Equations as Augmented Matrices | 148 | 48.577 h | 14071100 |
| Set Complements | 2829 | 48.160 h | 14071504 |
| Cardinality of Finite Sets | 48 | 48.853 h | 14071099 |
| The Eigenvalues and Eigenvectors of a 2x2 Matrix | 1375 | 48.420 h | 14071103 |
| Elementary Row Operations | 149 | 48.272 h | 14071448 |

### differential · Mathematics for Machine Learning · Quiz 1 (14165325)

First captured offer: 2026-10-13T11:55:47.963369+00:00. [Captured questions](../../../reference/mathacademy/capture/differential/14165325/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| Matrices With Easy-to-Find Inverses | 42 | 48.914 h | 14116678 |
| The Eigenvalues and Eigenvectors of a 2x2 Matrix | 1375 | 48.248 h | 14116680 |
| The Parametric Equations of a Plane | 1806 | 48.747 h | 14116683 |
| Vectors in N-Dimensional Euclidean Space | 1849 | 48.384 h | 14116975 |
| Logical Equivalence with Conditional Statements | 247 | 48.564 h | 14116679 |
| Modeling With the Binomial Distribution | 1395 | 48.097 h | 14116681 |

### multivariable · Mathematical Methods for the Physical Sciences II · Quiz 1 (14177361)

First captured offer: 2026-10-13T16:30:14.561922+00:00. [Captured questions](../../../reference/mathacademy/capture/multivariable/14177361/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| The Inner Product in Vector Spaces Over the Complex Numbers | 2097 | 52.033 h | 14117155 |
| Solving Homogeneous Systems of ODEs With Distinct Eigenvalues and Initial Conditions | 2088 | 50.756 h | 14118414 |
| Properties of Line Integrals With Respect to X and Y | 3708 | 116.626 h | 14059897 |
| Projecting Vectors Onto Subspaces in Inner Product Spaces | 2126 | Unknown | Not captured |
| Orthogonal Linear Transformations | 4319 | Unknown | Not captured |
| Surfaces of Revolution | 3372 | 102.199 h | 14071875 |
| The Work-Energy Principle | 3687 | 125.509 h | 14043252 |
| The Sample Mean | 2980 | 51.869 h | 14117157 |

### linear · Mathematical Foundations I · Quiz 1 (14196134)

First captured offer: 2026-10-14T04:32:43.555582+00:00. [Captured questions](../../../reference/mathacademy/capture/linear/14196134/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| The Cartesian Coordinate System | 92 | 48.522 h | 14129504 |
| Multiplying Fractions by Unit Fractions Using Models | 565 | 49.465 h | 14130082 |
| Dividing Whole Numbers by Unit Fractions Using Models | 529 | 49.584 h | 14129499 |
| Introduction to Algebraic Expressions | 63 | 50.171 h | 14129503 |
| Strategies to Simplify Whole Number and Fraction Multiplication | 2458 | 48.754 h | 14130367 |
| Dividing Whole Numbers by Unit Fractions | 533 | 49.362 h | 14130083 |
| Dividing Unit Fractions by Whole Numbers Using Models | 528 | 49.136 h | 14129811 |
| Multiplying Fractions by Whole Numbers Using Models | 3968 | 49.731 h | 14129810 |
| Dividing Unit Fractions by Whole Numbers | 530 | 48.954 h | 14130366 |
| Multiplying Fractions by Whole Numbers | 2360 | 49.269 h | 14130141 |
| Multiplying Fractions Using Models | 3079 | 48.270 h | 14130839 |
| Multiplying Unit Fractions by Whole Numbers Using Models | 564 | 49.961 h | 14129500 |

### linear · Mathematical Foundations II · Quiz 1 (14199677)

First captured offer: 2026-10-14T10:48:58.105811+00:00. [Captured questions](../../../reference/mathacademy/capture/linear/14199677/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| Divisibility of Integers by 3, 9, 6, and 7 | 3543 | 51.205 h | 14132610 |
| Subtracting a Positive Number From a Smaller Positive Number | 327 | 50.681 h | 14132866 |
| Multiplying and Dividing With Zero | 299 | Unknown | Not captured |
| Equivalent Ratios | 553 | 49.370 h | 14133433 |
| Comparing Fractions, Percents, and Decimals | 2457 | Unknown | Not captured |
| Introduction to Algebraic Expressions | 63 | 56.442 h | 14129503 |
| The Cartesian Coordinate System | 92 | 54.793 h | 14129504 |
| Natural Numbers, Integers, and Rational Numbers | 2558 | Unknown | Not captured |
| Multiplying Positive Numbers With Negative Numbers | 298 | Unknown | Not captured |
| Writing Ratios Using Fractions | 552 | 49.029 h | 14133630 |

### multivariable · Calculus II · Quiz 1 (14220202)

First captured offer: 2026-10-15T00:15:19.282013+00:00. [Captured questions](../../../reference/mathacademy/capture/multivariable/14220202/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| The Arc Length of a Polar Curve | 999 | 128.372 h | 14077889 |
| Logistic Growth Models With First-Order ODEs | 1163 | 49.354 h | 14151805 |
| Using Integration by Parts to Calculate Integrals With Logarithms | 1140 | 69.844 h | 14124251 |
| Surface Areas of Revolution for Parametric Curves | 1995 | 125.916 h | 14082905 |
| The Candidates Test | 364 | 130.178 h | 14075289 |
| Right-Angle Rotations as Linear Transformations | 931 | 164.613 h | 14039248 |

### foundations · Mathematical Methods for the Physical Sciences II · Quiz 1 (14220773)

First captured offer: 2026-10-15T00:48:59.350057+00:00. [Captured questions](../../../reference/mathacademy/capture/foundations/14220773/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| Equality of Mixed Partial Derivatives | 1957 | 101.167 h | 14108255 |
| Subspaces of Abstract Vector Spaces | 1907 | 50.611 h | 14150135 |
| The Curl of a Vector Field | 2132 | 100.543 h | 14108829 |
| The Invertible Matrix Theorem in Terms of Dimension, Rank and Nullity | 1869 | 69.463 h | 14130262 |
| Resonance in Vibrating Systems | 6720 | 60.516 h | 14135067 |
| Second-Order Homogeneous Initial Value Problems | 2741 | 66.484 h | 14131838 |
| Tangent Lines to Level Curves | 1940 | 49.910 h | 14151942 |

### multivariable · Linear Algebra · Quiz 1 (14234848)

First captured offer: 2026-10-15T15:57:31.275726+00:00. [Captured questions](../../../reference/mathacademy/capture/multivariable/14234848/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| The Image and Rank of a Linear Transformation | 1963 | 63.169 h | 14154149 |
| The Least-Squares Solution of a Linear System (With Collinearity) | 2167 | 86.346 h | 14123678 |
| Singular Value Decomposition of 2x2 Matrices | 3132 | 94.184 h | 14121427 |
| Projecting Vectors Onto Subspaces in Euclidean Spaces (Arbitrary Bases): Applications | 3818 | 95.374 h | 14119588 |

### multivariable · Methods of Proof · Quiz 1 (14252104)

First captured offer: 2026-10-16T07:08:35.401362+00:00. [Captured questions](../../../reference/mathacademy/capture/multivariable/14252104/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| Power Sets | 51 | 61.494 h | 14180007 |
| Limits of Inverse Trigonometric Functions | 3811 | 55.811 h | 14189988 |
| Further Logarithmic Differentiation | 344 | 54.141 h | 14192839 |
| Further Limits Involving the Exponential Function | 3671 | Unknown | Not captured |
| Using Integration by Parts to Calculate Integrals With Logarithms | 1140 | 100.732 h | 14124251 |
| Recognizing Derivatives in Limits | 637 | Unknown | Not captured |
| The Extreme Value Theorem | 3571 | Unknown | Not captured |

### linear · Mathematical Foundations III · Quiz 1 (14273614)

First captured offer: 2026-10-17T04:12:51.364317+00:00. [Captured questions](../../../reference/mathacademy/capture/linear/14273614/content.json).

| Topic | MA topic ID | Learning age | Successful lesson task |
|---|---:|---:|---:|
| Factoring Biquadratic Expressions | 2336 | 52.832 h | 14219091 |
| Special Trigonometric Ratios | 765 | 53.805 h | 14217763 |
| Multiplying Rational Expressions | 435 | 51.950 h | 14220059 |
| Advanced Rational Equations | 708 | 51.084 h | 14220061 |
| Perfect Square Quadratic Equations with One or No Solutions | 1425 | 50.966 h | 14221074 |
| Finding the Existence of a Limit Using One-Sided Limits | 625 | Unknown | Not captured |
| Problem Solving Using Vector Diagrams | 1102 | 213.241 h | 14040990 |
| Graphing the Square Root Function | 2038 | 51.369 h | 14220666 |
| Vertical Reflections of Functions | 1150 | 53.703 h | 14217907 |
| Even and Odd Functions | 725 | 60.832 h | 14205615 |
| The Change of Base Formula for Logarithms | 28 | 58.064 h | 14211604 |

