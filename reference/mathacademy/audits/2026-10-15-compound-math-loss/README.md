# Compound-math import-loss audit — October 15, 2026

Original lesson HTML preserves complete compound equations, but the legacy extractor often selected only the first nested MathML fragment. This can remove matrix operands, names, operators, or most of a non-matrix formula. The issue precedes the current Markdown renderer.

Scanned **2,964 original lesson HTML captures**. Found 4,111 candidate formula occurrences across 652 lessons, and read 1,910 matching current database records at **EDB basis 2832**. No source scan errors occurred.

## Direct first-matrix-only losses

**21 content attributes in 13 lessons** have the same particularly clear signature as the reported examples: the original formula contains multiple matrices, while the corresponding current problem/tutorial/solution contains only one matrix, matching the first source matrix. This is a conservative subset of the broader results, not a complete list of all import damage.

| Lesson | Source topic | Affected attributes | Database entities | Original source evidence |
| --- | ---: | ---: | --- | --- |
| Adding and Subtracting Matrices | 29 | 3 | `17592186054545`, `17592186054546`, `17592186054547` | [step-16080](/home/jake/Developer/MA/DATA/Lessons/29/Source/29.html:1592) |
| Basic Properties of Determinants | 1771 | 1 | `17592186121130` | [step-41735](/home/jake/Developer/MA/DATA/Lessons/1771/Source/1771.html:1393) |
| Euler's Method for Systems of ODEs | 3245 | 1 | `17592186168011` | [step-587388](/home/jake/Developer/MA/DATA/Lessons/3245/Source/3245.html:6812) |
| Introduction to Linear Transformations | 865 | 1 | `17592186087562` | [step-19996](/home/jake/Developer/MA/DATA/Lessons/865/Source/865.html:5002) |
| Introduction to the Inverse of a Matrix | 863 | 2 | `17592186087506`, `17592186087507` | [step-16453](/home/jake/Developer/MA/DATA/Lessons/863/Source/863.html:2167) |
| Inverses of 2x2 Matrices | 864 | 1 | `17592186087509` | [step-16460](/home/jake/Developer/MA/DATA/Lessons/864/Source/864.html:2730) |
| Multiplying Matrices | 1196 | 1 | `17592186101960` | [step-16188](/home/jake/Developer/MA/DATA/Lessons/1196/Source/1196.html:6569) |
| Multiplying Square Matrices | 147 | 1 | `17592186059599` | [step-19318](/home/jake/Developer/MA/DATA/Lessons/147/Source/147.html:3788) |
| Phase Portraits for Linear Systems With Repeated Eigenvalues | 3240 | 1 | `17592186166545` | [step-588334](/home/jake/Developer/MA/DATA/Lessons/3240/Source/3240.html:2460) |
| Properties of Matrix Addition | 1168 | 1 | `17592186100686` | [step-464513](/home/jake/Developer/MA/DATA/Lessons/1168/Source/1168.html:2008) |
| Solving 2x2 Systems of Equations Using Inverse Matrices | 934 | 1 | `17592186093404` | [step-16614](/home/jake/Developer/MA/DATA/Lessons/934/Source/934.html:3189) |
| The Hadamard Product | 5916 | 4 | `17592186208273`, `17592186208274`, `17592186208275`, `17592186208559` | [step-610699](/home/jake/Developer/MA/DATA/Lessons/5916/Source/5916.html:2314) |
| Zero, Square, Diagonal and Identity Matrices | 862 | 3 | `17592186087502`, `17592186087503`, `17592186087504` | [step-16107](/home/jake/Developer/MA/DATA/Lessons/862/Source/862.html:1668) |

[Detailed first-matrix-only evidence](first-matrix-only.json) records the original matrices, missing matrices and labels, source lines, current text, and exact database entity/attribute.

## Broader source-loss matches

The automated comparison flagged **368 attributes in 365 content records across 201 lessons**. These matches include the direct cases above. Treat the full list as a review queue: formula normalization and later content revisions can require judgment. The audit does not claim that every broader match has been manually checked.

| Signature | Matched attributes |
| --- | ---: |
| Source matrices absent from the current attribute | 57 |
| Matrix values found, but source assignment labels absent | 109 |
| An isolated first MathML fragment appears instead of the complete compound formula | 202 |

Non-matrix spot checks confirm the same loss mechanism:

- **Directrices of Ellipses** (`17592186093469`): the complete focus/directrix set definition became a display containing only `P`.
- **Solving Geometric Series Problems Using Exponential Equations and Inequalities** (`17592186093398`): the underbraced sum inequality became only `N`.
- **Multiplying Two-Digit Decimals** (`17592186056062`): the annotated decimal placement example became only `2`.

Another **2,855 source formula occurrences** could not be confidently compared automatically. Unsupported MathML and legitimate rendering differences stay in [needs-review.json](needs-review.json). The scan also identified 726 candidate occurrences whose required matrices/formulas were already present. A clean result for a particular occurrence does not certify the entire lesson.

## Reported items repaired during this session

| Reported entity | Content changed | Result |
| --- | --- | --- |
| `17592186100992` | Canonical example `17592186100687`, MA e-4379 | Restored A/B/C definitions from the source; verified at basis 2831. |
| `17592186088890` | Tutorial 2982 | Restored the missing 2×2 zero matrix and 3×3 square matrix. |
| `17592186087696` | Canonical example `17592186087503`, MA e-4391 | Restored U/W/Z definitions from the source. |
| `17592186403293` | Question q-68727 | Stacked W/X/Y vertically; matrix values preserved. |

The last three text repairs committed together at **basis 2843**, after the audit snapshot. Therefore, two content records in the snapshot’s match list are now repaired (`17592186088890` and `17592186087503`). The remaining snapshot queue has 363 records / 366 matched attributes across the same 201 lessons. No answer entities, field identities, grades, attempts, XP, or learner history were changed. Nine live-app DOM checks at 893, 375, and 320px verified the three reported repairs, without screenshots or learner submissions.

## Cause and scope

The legacy [extract_math_from_node()](/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py:532) calls `node.find("mjx-assistive-mml")`, finds the first descendant, and returns its MathML before reading the outer SVG title. In a title such as `A = [matrix], B = [matrix]`, that descendant represents only the first matrix. The outer equation still exists in the original HTML.

This audit targets that specific import failure. It does not certify unrelated Markdown tables, image extraction, blank placement, or every possible equation conversion. It also does not apply an unreviewed bulk rewrite to the broader match list. Original source files remain unchanged.

## All lessons with automated matches

The following counts are matched attributes, not counts of questions. Tutorial content and worked solutions can also be affected. Entity IDs support direct review in the app.

| Lesson | Source topic | Matched attributes | Content entity IDs |
| --- | ---: | ---: | --- |
| Adding Decimal Fractions | 3916 | 1 | `17592186188123` |
| Adding Fractions With Unlike Denominators Using Models | 2374 | 1 | `17592186142618` |
| Adding Two-Digit Whole Numbers | 3875 | 1 | `17592186189460` |
| Adding and Subtracting Matrices | 29 | 4 | `17592186054545`, `17592186054546`, `17592186054547`, `17592186055975` |
| Addition With Unequal Numbers of Decimals | 2339 | 3 | `17592186138153`, `17592186138157`, `17592186139709` |
| Additional Rules of Logical Inference | 4306 | 1 | `17592186199614` |
| Adjacency Matrices | 2757 | 5 | `17592186151886`, `17592186151887`, `17592186153309`, `17592186153310`, `17592186153323` |
| Adjacency Matrices of Directed Graphs | 5415 | 2 | `17592186203794`, `17592186205161` |
| Affine Transformations | 3387 | 1 | `17592186173206` |
| Approximating Areas With the Left Riemann Sum | 477 | 1 | `17592186070007` |
| Approximating Areas With the Midpoint Riemann Sum | 944 | 2 | `17592186092002`, `17592186093487` |
| Approximating Areas With the Right Riemann Sum | 1281 | 1 | `17592186107152` |
| Basic Properties of Determinants | 1771 | 1 | `17592186121130` |
| Bilinear Forms | 3121 | 1 | `17592186163234` |
| Boolean Functions | 3778 | 2 | `17592186184028`, `17592186185386` |
| Breadth-First Search | 2893 | 1 | `17592186157032` |
| Calculating Trigonometric Ratios From Descriptions | 6175 | 2 | `17592186212774`, `17592186212775` |
| Calculating the Cross Product Using Determinants | 245 | 1 | `17592186060922` |
| Calculating the Eigenvalues of a 2x2 Matrix | 990 | 1 | `17592186093438` |
| Calculating the Eigenvectors of a 2x2 Matrix | 991 | 1 | `17592186093440` |
| Calculating the Eigenvectors of a 3x3 Matrix With Distinct Eigenvalues | 1977 | 1 | `17592186130347` |
| Calculating the Eigenvectors of a 3x3 Matrix in the General Case | 1965 | 1 | `17592186125787` |
| Calculating the Number of Terms in an Arithmetic Series | 676 | 1 | `17592186079659` |
| Cantor's Theorem | 3428 | 1 | `17592186173284` |
| Closure Properties of Rational Expressions | 2039 | 1 | `17592186129068` |
| Cofunction Relationships and Identities | 6022 | 1 | `17592186208346` |
| Combining Linear Transformations Using 2x2 Matrices | 933 | 2 | `17592186093492`, `17592186093493` |
| Comparing Exponents | 2474 | 4 | `17592186147259`, `17592186147261`, `17592186148705`, `17592186148706` |
| Comparing Whole Numbers | 2324 | 1 | `17592186138063` |
| Comparing Whole Numbers Using Place Value | 3919 | 1 | `17592186188015` |
| Computing Probabilities Using Combinatorics | 132 | 1 | `17592186055986` |
| Conditional Probabilities From Two-Way Frequency Tables | 6606 | 1 | `17592186228765` |
| Confidence Intervals for One Mean: Known Population Variance | 260 | 1 | `17592186060967` |
| Confidence Intervals for One Mean: Unknown Population Variance | 3855 | 1 | `17592186189370` |
| Confidence Intervals for One Proportion | 3300 | 1 | `17592186173213` |
| Confidence Intervals for Two Means: Equal and Unknown Population Variance | 4946 | 1 | `17592186205093` |
| Confidence Intervals for Two Means: Known and Unequal Population Variances | 3298 | 1 | `17592186173242` |
| Confidence Intervals for Two Proportions | 4943 | 1 | `17592186205139` |
| Conformability for Matrix Multiplication | 1198 | 2 | `17592186101958`, `17592186101985` |
| Connecting Fraction Multiplication and Area | 569 | 1 | `17592186073544` |
| Constrained Optimization of Quadratic Forms | 3171 | 1 | `17592186168155` |
| Constrained Optimization of Quadratic Forms: Determining Where Extrema are Attained | 4238 | 3 | `17592186198088`, `17592186198089`, `17592186198090` |
| Continuity and Differentiability of Functions | 1691 | 1 | `17592186116514` |
| Converting From Expanded Form to Standard Form | 2311 | 1 | `17592186138108` |
| Counting Trees | 1714 | 1 | `17592186116414` |
| Decomposing Fractions Into Sums | 3955 | 2 | `17592186192562`, `17592186193927` |
| Defining Continuity at a Point | 314 | 1 | `17592186063917` |
| Diagonalizing a 2x2 Matrix | 1968 | 1 | `17592186125839` |
| Diagonalizing a 3x3 Matrix in the General Case | 1971 | 3 | `17592186125793`, `17592186125856`, `17592186125857` |
| Dijkstra's Algorithm | 2899 | 3 | `17592186157047`, `17592186158444` |
| Direct Proof | 2801 | 4 | `17592186157014`, `17592186157054`, `17592186157055`, `17592186158575` |
| Directrices of Ellipses | 1028 | 1 | `17592186093469` |
| Directrices of Hyperbolas | 1033 | 1 | `17592186093468` |
| Disproving Universal Statements | 3412 | 2 | `17592186171736`, `17592186173275` |
| Dot Plots | 2499 | 1 | `17592186147309` |
| Equivalent Place Value Representations and Borrowing | 3954 | 3 | `17592186192552`, `17592186193920` |
| Euler's Method for Systems of ODEs | 3245 | 1 | `17592186168011` |
| Evaluating Exponents | 2321 | 3 | `17592186138136`, `17592186139702`, `17592186139743` |
| Evaluating Exponents With Decimal Bases | 2477 | 4 | `17592186147183`, `17592186147184`, `17592186147185`, `17592186148798` |
| Evaluating Exponents With Fractional Bases | 2476 | 1 | `17592186147187` |
| Evaluating Larger Exponents | 3537 | 1 | `17592186171759` |
| Expressing Inhomogeneous ODEs as First-Order Systems | 3635 | 1 | `17592186176958` |
| Feature Extraction Using PCA | 5289 | 1 | `17592186203876` |
| Finding Complex Eigenvectors of Real 2x2 Matrices | 3574 | 1 | `17592186176975` |
| Finding Determinants Using Laplace Expansions | 1770 | 1 | `17592186121018` |
| Finding Equivalent Fractions Using Area Models | 2368 | 2 | `17592186142737`, `17592186142739` |
| Finding Lowest Common Multiples Using Prime Factorization | 755 | 1 | `17592186084484` |
| Finding Side Lengths Using Fraction Division | 6740 | 5 | `17592186231305`, `17592186231311`, `17592186231312`, `17592186231313`, `17592186232002` |
| Finding the Canonical Form of a Quadratic Form Using Lagrange's Method | 3124 | 1 | `17592186163228` |
| Finding the Canonical Form of a Quadratic Form Using Orthogonal Transformations | 3126 | 1 | `17592186161798` |
| Finding the Inverse of a 2x2 Matrix Using Row Operations | 1728 | 1 | `17592186116498` |
| Formal and Informal Language | 2798 | 1 | `17592186157009` |
| Fraction Multiplication Number Sense | 571 | 2 | `17592186073441`, `17592186073442` |
| Frequency Tables | 2509 | 1 | `17592186147307` |
| Histograms | 2510 | 1 | `17592186147322` |
| Incidence Matrices | 1673 | 4 | `17592186114933`, `17592186114934`, `17592186116401`, `17592186116402` |
| Index Notation for Matrices | 1167 | 1 | `17592186101952` |
| Interpreting Descriptions of Physical Phenomena | 6339 | 1 | `17592186218328` |
| Introduction to Exponents | 2314 | 5 | `17592186138174`, `17592186138175`, `17592186138176`, `17592186138177`, `17592186139721` |
| Introduction to Linear Transformations | 865 | 3 | `17592186087562`, `17592186087563`, `17592186088928` |
| Introduction to Matrices | 861 | 2 | `17592186087511`, `17592186088898` |
| Introduction to Systems of Linear ODEs | 2086 | 2 | `17592186128889`, `17592186128891` |
| Introduction to Turing Machines | 3802 | 1 | `17592186184015` |
| Introduction to the Inverse of a Matrix | 863 | 2 | `17592186087506`, `17592186087507` |
| Inverses of 2x2 Matrices | 864 | 5 | `17592186087508`, `17592186087509`, `17592186087510`, `17592186088895`, `17592186088896` |
| Inverting Linear Transformations | 988 | 2 | `17592186092071`, `17592186093436` |
| Jordan Blocks and Jordan Matrices | 3114 | 2 | `17592186163269`, `17592186163270` |
| Jordan Canonical Decomposition of a 2x2 Matrix | 3652 | 3 | `17592186175863`, `17592186177016`, `17592186177018` |
| Jordan Canonical Form of a 2x2 Matrix | 3629 | 2 | `17592186177015`, `17592186177017` |
| Jordan Canonical Form of a 3x3 Matrix | 3115 | 2 | `17592186163277`, `17592186163278` |
| Linear Independence for Homogeneous Systems of ODEs | 6374 | 1 | `17592186222472` |
| Linear Maps Between Two Different Vector Spaces | 907 | 2 | `17592186087569`, `17592186088932` |
| Linear Transformations of Objects in the Plane | 866 | 3 | `17592186087566`, `17592186087608`, `17592186088929` |
| Linear Transformations of Points and Lines in the Plane | 2706 | 3 | `17592186151975`, `17592186151976`, `17592186153365` |
| Markov Chains | 1911 | 1 | `17592186124354` |
| Matrix Exponentials | 6375 | 1 | `17592186222482` |
| Matrix Functions | 2927 | 1 | `17592186158433` |
| Midpoints in the Coordinate Plane | 485 | 3 | `17592186073483`, `17592186073484`, `17592186073485` |
| Modeling Financial Problems Using Geometric Series | 3681 | 1 | `17592186180695` |
| Multi-Digit by One-Digit Division Using Partial Quotients | 2425 | 1 | `17592186142484` |
| Multi-Digit by One-Digit Multiplication Using Area Models | 2393 | 1 | `17592186142539` |
| Multiple Linear Regression With Matrices | 2171 | 2 | `17592186133617`, `17592186133618` |
| Multiplying Decimals by Powers of Ten Using Place Value | 110 | 1 | `17592186054454` |
| Multiplying Decimals by Powers of Ten With Exponents | 2317 | 5 | `17592186138259`, `17592186138260`, `17592186138261`, `17592186138262`, `17592186139627` |
| Multiplying Matrices | 1196 | 2 | `17592186101959`, `17592186101960` |
| Multiplying Numbers by Powers of Ten With Exponents | 2316 | 5 | `17592186138178`, `17592186138179`, `17592186138180`, `17592186138181`, `17592186139722` |
| Multiplying Square Matrices | 147 | 3 | `17592186059555`, `17592186059556`, `17592186059599` |
| Multiplying Three-Digit Decimals | 2355 | 6 | `17592186138203`, `17592186138206`, `17592186138208`, `17592186138210`, `17592186139736`, `17592186139738` |
| Multiplying Two-Digit Decimals | 111 | 6 | `17592186054461`, `17592186054462`, `17592186054463`, `17592186054464`, `17592186056062`, `17592186056063` |
| Multiplying Two-Digit Decimals by Three-Digit Decimals | 2348 | 6 | `17592186138182`, `17592186138183`, `17592186138184`, `17592186138185`, `17592186139723`, `17592186139724` |
| Multiplying a Decimal by a Multi-Digit Whole Number | 2347 | 5 | `17592186138149`, `17592186138150`, `17592186138151`, `17592186138152`, `17592186139708` |
| Multiplying a Decimal by a One-Digit Whole Number | 2346 | 5 | `17592186138201`, `17592186138204`, `17592186138207`, `17592186139734`, `17592186139737` |
| Multiplying a Matrix by a Column Vector | 1195 | 1 | `17592186101956` |
| Multiplying a Matrix by the Identity Matrix | 1171 | 1 | `17592186101962` |
| Multiplying and Dividing Binary Integers | 3760 | 1 | `17592186180747` |
| Multiplying by 10, 100, and 1,000 Using the Pattern of Zeros | 2338 | 3 | `17592186138114`, `17592186138115`, `17592186139688` |
| Necessary and Sufficient Conditions | 2793 | 4 | `17592186151814`, `17592186151815`, `17592186151831`, `17592186153432` |
| Negating Quantified Statements | 2791 | 1 | `17592186151809` |
| Numerical Word Problems | 6036 | 1 | `17592186208298` |
| Operations on Relations | 4832 | 1 | `17592186205267` |
| Partitioned and Block Matrices | 1735 | 4 | `17592186116538`, `17592186116539`, `17592186116540`, `17592186116541` |
| Phase Portraits for Linear Systems With Repeated Eigenvalues | 3240 | 1 | `17592186166545` |
| Place Value With Numbers Up to Four Digits | 2312 | 1 | `17592186139603` |
| Point Discontinuities | 2002 | 1 | `17592186128900` |
| Powers of Matrices | 1725 | 2 | `17592186116488`, `17592186116489` |
| Powers of Ten | 2315 | 3 | `17592186138256`, `17592186138258`, `17592186139626` |
| Prenex Normal Form | 4423 | 1 | `17592186199573` |
| Probability From Experimental Data | 130 | 2 | `17592186054357`, `17592186054358` |
| Projection Matrices, Linear Transformations and Their Properties | 2125 | 2 | `17592186133599`, `17592186133676` |
| Proof by Cases | 4432 | 1 | `17592186198200` |
| Proof by Contrapositive | 2807 | 1 | `17592186157016` |
| Properties of Diagonalization | 1969 | 2 | `17592186124340`, `17592186124381` |
| Properties of Matrix Addition | 1168 | 2 | `17592186100686`, `17592186101954` |
| Proving Biconditional Statements | 4925 | 4 | `17592186203729`, `17592186203732`, `17592186205280`, `17592186205281` |
| Proving Divisibility | 2795 | 1 | `17592186157056` |
| Proving Divisibility by Contrapositive | 2808 | 1 | `17592186157061` |
| Proving Irrationality by Contradiction | 4922 | 1 | `17592186205224` |
| Proving Matrix Identities Using Induction | 781 | 2 | `17592186082927`, `17592186084520` |
| Proving Parity by Contrapositive | 4437 | 1 | `17592186198212` |
| Proving a Relation Is an Equivalence Relation | 4942 | 1 | `17592186203743` |
| QR Factorization | 2129 | 2 | `17592186133607`, `17592186133679` |
| Reducing a Quadratic Curve to Its Principal Axes | 3129 | 1 | `17592186161803` |
| Regular Graphs | 3032 | 1 | `17592186161750` |
| Representing 2x2 Systems of Equations Using a Matrix Product | 1729 | 1 | `17592186116490` |
| Representing 3x3 Systems of Equations Using a Matrix Product | 155 | 1 | `17592186060935` |
| Right-Angle Rotations as Linear Transformations | 931 | 2 | `17592186092065`, `17592186092066` |
| Rotation-Scaling Matrices | 2017 | 1 | `17592186128890` |
| Rotations as Linear Transformations | 932 | 1 | `17592186092069` |
| Scalar Multiplication of Matrices | 146 | 1 | `17592186060926` |
| Second-Degree Taylor Polynomials of Multivariable Functions | 4171 | 2 | `17592186198077`, `17592186198078` |
| Shear and Stretch as Linear Transformations | 1358 | 1 | `17592186107101` |
| Shortest Paths in Unweighted Graphs | 2895 | 1 | `17592186157035` |
| Significant Figures | 4033 | 1 | `17592186193913` |
| Significant Figures With Decimals | 4314 | 2 | `17592186198155`, `17592186199535` |
| Singular Linear Transformations in the Plane | 1351 | 3 | `17592186105461`, `17592186107154`, `17592186107155` |
| Singular Value Decomposition and the Pseudoinverse Matrix | 3134 | 1 | `17592186161902` |
| Solving 2x2 Systems of Equations Using Inverse Matrices | 934 | 2 | `17592186093402`, `17592186093404` |
| Solving Geometric Series Problems Using Exponential Equations and Inequalities | 1018 | 1 | `17592186093398` |
| Solving Homogeneous Systems of ODEs Using Matrix Methods | 6690 | 1 | `17592186228911` |
| Solving Homogeneous Systems of ODEs With Repeated Eigenvalues | 2818 | 2 | `17592186157074`, `17592186157075` |
| Solving Inequalities Involving Positive and Negative Factors | 2982 | 1 | `17592186157176` |
| Solving Inhomogeneous Systems of ODEs Using Matrix Methods | 6691 | 1 | `17592186228915` |
| Solving Systems of Equations Using Inverse Matrices | 1023 | 1 | `17592186092026` |
| Squaring Rational Numbers | 2174 | 1 | `17592186133510` |
| Subspaces of N-Dimensional Space | 1853 | 1 | `17592186119501` |
| Subtracting Fractions With Unlike Denominators Using Models | 2372 | 1 | `17592186142619` |
| Subtraction With Unequal Numbers of Decimals | 2340 | 3 | `17592186138192`, `17592186138193`, `17592186139727` |
| Symmetric Matrices | 3118 | 2 | `17592186161816`, `17592186163254` |
| The "And" and "Or" Connectives | 60 | 2 | `17592186054365`, `17592186054366` |
| The "Not" Connective | 2790 | 1 | `17592186151800` |
| The "Not" Connective With Predicates | 4256 | 1 | `17592186198102` |
| The Cardinality of the Power Set of Natural Numbers | 4424 | 1 | `17592186199604` |
| The Characteristic Equation of a Matrix | 1964 | 1 | `17592186125785` |
| The Column Space of a Matrix | 1850 | 1 | `17592186121037` |
| The Determinant of a 2x2 Matrix | 152 | 3 | `17592186059557`, `17592186059558`, `17592186060931` |
| The Determinant of a 3x3 Matrix | 153 | 2 | `17592186061006`, `17592186061008` |
| The Determinant of an NxN Matrix | 1769 | 1 | `17592186121025` |
| The Distance Formula | 459 | 2 | `17592186068508`, `17592186068509` |
| The Distance Formula in Three Dimensions | 512 | 1 | `17592186073659` |
| The Eigenvalues and Eigenvectors of a 2x2 Matrix | 1375 | 1 | `17592186107090` |
| The Geometric Interpretation of the 2x2 Determinant | 1169 | 3 | `17592186101963`, `17592186101964`, `17592186101966` |
| The Gram-Schmidt Process for Two Vectors | 2127 | 1 | `17592186133604` |
| The Hadamard Product | 5916 | 7 | `17592186208273`, `17592186208274`, `17592186208275`, `17592186208559`, `17592186209879`, `17592186209881` |
| The Hypergeometric Distribution | 3073 | 4 | `17592186161749`, `17592186161828`, `17592186161830`, `17592186163206` |
| The Image and Rank of a Linear Transformation | 1963 | 1 | `17592186125819` |
| The Image of an Affine Transformation | 3706 | 5 | `17592186179428`, `17592186179429`, `17592186179430`, `17592186179434`, `17592186180755` |
| The Inverse of an Affine Transformation | 3707 | 1 | `17592186179431` |
| The Least-Squares Solution of a Linear System (With Collinearity) | 2167 | 2 | `17592186133611`, `17592186133634` |
| The Least-Squares Solution of a Linear System (Without Collinearity) | 2166 | 3 | `17592186133608`, `17592186133609`, `17592186135059` |
| The Minors of a 3x3 Matrix | 233 | 1 | `17592186060932` |
| The PMF of the Hypergeometric Distribution | 5412 | 2 | `17592186203880`, `17592186205176` |
| The Quadratic Formula | 422 | 1 | `17592186068637` |
| The Standard Matrix of a Linear Transformation | 1959 | 1 | `17592186125781` |
| The Total Area Bounded by a Single Polar Curve | 2833 | 2 | `17592186157101`, `17592186158485` |
| Translating Between Logical and Set Operations | 251 | 1 | `17592186059429` |
| Trees and Forests | 1284 | 1 | `17592186105506` |
| Triangular Matrices | 1777 | 1 | `17592186121017` |
| Trivial and Vacuous Proofs | 2815 | 1 | `17592186158573` |
| Two-Digit by One-Digit Division Using Partial Quotients | 2424 | 1 | `17592186142489` |
| Weighted Least-Squares | 3135 | 2 | `17592186163308`, `17592186163312` |
| Zero, Square, Diagonal and Identity Matrices | 862 | 6 | `17592186087502`, `17592186087503` (repaired), `17592186087504`, `17592186087505`, `17592186088890` (repaired), `17592186088892` |

Machine-readable evidence: [matches](matches.json), [lesson index](affected-lessons.json), [source candidates](source-candidates.json), [scan summary](scan-summary.json), [comparison summary](comparison-summary.json). All database projections and source/input query templates are retained alongside this report.
