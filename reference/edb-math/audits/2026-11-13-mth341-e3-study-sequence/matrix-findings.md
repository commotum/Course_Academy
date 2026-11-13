# Matrix, systems, determinants, and algebra findings

Read-only audit at basis **14416**. This is a branch report; the parent report supplies the complete sequence and in-class coverage. No lesson, assignment, learner, or EDB mutations.

The official guide explicitly includes **whole WHW 4 and WHW 5**, not only its three proof questions. WHW 4 3.1.9/.12/.17/.19/.20/.24 directly support determinant-law and4x4 row-operation study. Named textbook sections primarily address vector spaces and transformations. The PDF text inspected is `/tmp/mth341-kuttler-audit.txt`; original textbook path is recorded in JSON.

## Proposed full-lesson branch order

1. **Gaussian Elimination For NxM Systems of Equations** — `17592186048445`
1. **Finding Determinants Using Laplace Expansions** — `17592186048505`
1. **Basic Properties of Determinants** — `17592186049159`
1. **Row and Column Operations on Determinants** — `17592186048462`
1. **Finding Determinants Using Row and Column Operations** — `17592186049685`
1. **Conditions When a Determinant Equals Zero** — `17592186049312`
1. **Further Properties of Determinants** — `17592186049875`
1. **The Invertible Matrix Theorem in Terms of 2x2 Systems of Equations** — `17592186050906`
1. **The Dimension of the Null Space of a Matrix** — `17592186050996`
1. **The Invertible Matrix Theorem in Terms of Dimension, Rank and Nullity** — `17592186049340`

Interleave retained Column Space, Null Space, Finding a Basis, Dimension of a Span, and Rank before the last two entries as appropriate. Dimension of Null Space is a useful outside-expansion addition. Gaussian elimination can be studied independently of the determinant branch.

## Candidate decisions

### KEEP: Gaussian Elimination For NxM Systems of Equations — `17592186048445`

Extends already studied square-system reduction to genuinely rectangular systems, including overdetermined inconsistency, underdetermined general solutions, and parameter conditions.

**Evidence:** Tutorial 17592186116493 and example 17592186115070 solve2 equations / 3 variables. question 17592186115751 finds x=6, y=13-2z; question 17592186115752 classifies3 equations / 2 variables. All27 parameter questions were inspected: coefficient k enters linearly; question 17592186115753 gives k=4/3.

**Contribution:** WHW 4 4.10.4 span test and WHW 5 rectangular generator/rank matrices; retained Null Space and later rectangular column/image computations.

**Mastery:** learned=false; practice accuracy0.8614, mass10.5; no last-direct-at, assessment mass0, repetitions0. Studied RREF accuracy0.8916, mass21.5 and singular3x3 accuracy0.9136, mass14.17 support arithmetic readiness but do not demonstrate rectangular mastery.

Captured 5 lesson sections and 104 practice questions. [Actual content](topics/17592186048445/readable.md); full bank `topics/17592186048445/practice.json`.

### KEEP: Finding Determinants Using Laplace Expansions — `17592186048505`

Keep non-first-row and column expansion because full retained lessons require this method, even though first-row expansion/elimination could compute the same number.

**Evidence:** Examples 17592186119657/17592186119588 explicitly require fourth-row/second-column cofactor combinations. question 17592186120425 explicitly requires second-row expansion. Bank46:13 row-expression,16 row-calculation,17 column-calculation.

**Contribution:** Retained Basic Properties has31 many-zero and27 n-dimensional-volume questions; retained Finding Determinants Using Row and Column Operations has30 questions asking equivalent3x3 determinants obtained through a designated row/column, plus14 calculations.

**Mastery:** No progress row captured; studied NxN determinant50092 accuracy0.99925, mass6 only teaches expansion across first row.

Captured 5 lesson sections and 46 practice questions. [Actual content](topics/17592186048505/readable.md); full bank `topics/17592186048505/practice.json`.

### KEEP: Basic Properties of Determinants — `17592186049159`

Supplies triangular/identity/transpose determinant properties and meaningful practice; whole lesson also teaches determinant-volume interpretation that must remain in readiness analysis.

**Evidence:** Tutorial 17592186121130 gives triangular product and det(A^T)=det(A). question 17592186120429 expands down third column; question 17592186120154 computes4-dimensional volume via sparse determinant.

**Contribution:** WHW 4 3.1.9 transposition; 3.1.24 row reduction to triangular form; 3.1.19 orthogonal determinant proof; prerequisites for retained row operations and determinant laws.

**Mastery:** learned=false, accuracy0.7311, mass1, assessment mass0; studied2x2 geometric determinant48857 and studied triangular matrix concept50283 support readiness, not mastery of these laws.

Captured 6 lesson sections and 110 practice questions. [Actual content](topics/17592186049159/readable.md); full bank `topics/17592186049159/practice.json`.

### KEEP: Row and Column Operations on Determinants — `17592186048462`

Teaches effects of swapping, row scaling, replacement, whole-matrix scaling, and corresponding column operations, with dedicated concept practice.

**Evidence:** Examples 17592186119589/.590/.591 and question 17592186120431 distinguish swap sign from replacement invariance. question 17592186120512 uses det(5A)=5^3det(A).

**Contribution:** Direct WHW 4 3.1.12 row scaling and 3.1.24 required row operations; retained determinant computation and zero-determinant concepts.

**Mastery:** No target progress row. Scope marks Creating Rows or Columns Containing Zeros Using Gaussian Elimination50527 studied; inspected its3x3/4x4 row AND column operation tutorial/bank 59, so no need to add a column-operations prerequisite lesson.

Captured 10 lesson sections and 77 practice questions. [Actual content](topics/17592186048462/readable.md); full bank `topics/17592186048462/practice.json`.

### KEEP: Conditions When a Determinant Equals Zero — `17592186049312`

Retain basic zero-determinant conceptual practice before full Further Properties; this is not optional merely because its facts can be rederived during downstream exercises.

**Evidence:** Tutorial 17592186135154 connects determinant zero to a dependent row/column; bank 36 covers zero/identical/proportional rows and necessary-vs-sufficient claims. question 17592186134414 distinguishes proportional from identical rows.

**Contribution:** Further Properties question 17592186120457 and question 17592186265950 use identical-row determinant=0 when splitting by linearity; also reinforces dependence/determinant connection for square rank concepts.

**Mastery:** No progress row; studied Linear Dependence and Independence50426 accuracy0.7415, mass8.67 helps vocabulary but not learned determinant-zero practice.

Captured 8 lesson sections and 36 practice questions. [Actual content](topics/17592186049312/readable.md); full bank `topics/17592186049312/practice.json`.

### KEEP: Finding Determinants Using Row and Column Operations — `17592186049685`

Actual4x4 reduction practice is needed for whole WHW 4; retain row AND column variants because this is a whole lesson.

**Evidence:** Examples 17592186119690/.691 reduce using row/column operations; question 17592186120434 zeros above a42 and asks equivalent3x3; question 17592186120545 requires column replacements; question 17592186120419 asks full4x4 value.

**Contribution:** WHW 4 3.1.24 explicitly requires row operations to simplify a4x4 determinant first.

**Mastery:** No progress row; studied50527 supplies creating zeros, studied50092 supplies minor/cofactor computations; neither trains determinant-preserving4x4 reduction as this lesson does.

Captured 4 lesson sections and 44 practice questions. [Actual content](topics/17592186049685/readable.md); full bank `topics/17592186049685/practice.json`.

### KEEP: Further Properties of Determinants — `17592186049875`

Multiplicativity, inverse determinant, and row/column linearity directly support required homework proofs. Computing det(A^-1) does not require computing A^-1.

**Evidence:** Tutorial 17592186121023 proves det(A^-1)=1/det(A); question 17592186120436 asks inverse determinant from3x3 A and solves via det(A), not cofactor inverse. question 17592186120457 uses identical-row determinant zero.

**Contribution:** WHW 4 3.1.17 nonadditivity of whole determinant,3.1.19 orthogonal det=±1,3.1.20 similarity invariance.

**Mastery:** learned=false, accuracy0.58485, mass1, assessment mass0. No basis to omit determinant-law practice.

Captured 6 lesson sections and 48 practice questions. [Actual content](topics/17592186049875/readable.md); full bank `topics/17592186049875/practice.json`.

### KEEP: The Invertible Matrix Theorem in Terms of 2x2 Systems of Equations — `17592186050906`

Conceptual equivalences for invertibility/unique systems/determinant connect studied inverse basics to retained full rank theorem. Entire bank is theorem reasoning; inverse solver prerequisite is dispensable.

**Evidence:** Tutorial 17592186116491 gives five equivalences. question 17592186115811 links unique solution, det≠0, and homogeneous solution; question 17592186115884 has6k+6≠0, linear parameter only. Bank46 has no inverse computation.

**Contribution:** Retained49340 practice assumes det=0/±1 ↔ invertibility; textbook4.10.5 theorem equivalences include unique homogeneous solution and consistency for every RHS.

**Mastery:** No target progress row. Studied Inverses of 2x2 Matrices49548 accuracy0.9232, mass14.33 covers invertible iff det≠0 and explicit inverse; studied singular-system lessons supply consistency vocabulary.

Captured 4 lesson sections and 46 practice questions. [Actual content](topics/17592186050906/readable.md); full bank `topics/17592186050906/practice.json`.

### KEEP: The Invertible Matrix Theorem in Terms of Dimension, Rank and Nullity — `17592186049340`

Practices the full square-matrix bridge among rank, dimension, column space, null space, and invertibility; relevant beyond computational basis extraction.

**Evidence:** Tutorial 17592186125780, question 17592186446374(det=0⇒not invertible, rank≠5), question 17592186125167(nonzero determinant⇒empty nullspace basis and n pivots), question 17592186446380(nullity0⇒full column-space dimension).

**Contribution:** Actual textbook4.10.5 includes invertible iff rank = n and full row/column rank equivalences. Supports WHW 5 4.10.55 independent n vectors span R^n and conceptual rank/nullspace exam scope.

**Mastery:** No target progress row. Should follow retained Rank, Column/Null Space, Dimension of Span, and added Dimension of Null Space; parent can integrate shared branch dependencies.

Captured 4 lesson sections and 64 practice questions. [Actual content](topics/17592186049340/readable.md); full bank `topics/17592186049340/practice.json`.

### KEEP: The Dimension of the Null Space of a Matrix — `17592186050996`

Useful outside-expansion addition: provides explicit non-pivot/free-variable-to-nullspace-dimension concept practice before full retained49340, with no unrelated branches.

**Evidence:** Tutorial 17592186125778 produces nullspace basis(-5/3,1,0) and dimension1. question 17592186124317 asks9x11 matrix with 9 pivots; question 17592186124319 computes4x4 nullity by reduction. Bank36 consists of12 each counting, inspection, reduction.

**Contribution:** Whole49340 contains nullity and dimension-of-nullspace in statement completions; textbook4.10.5 includes nullspace, and5.7 kernel bases.

**Mastery:** No progress row captured; not classified mastered. Core vector branch may jointly own this addition.

Captured 5 lesson sections and 36 practice questions. [Actual content](topics/17592186050996/readable.md); full bank `topics/17592186050996/practice.json`.

### SKIP: Calculating the Inverse of a 3x3 Matrix Using the Cofactor Method — `17592186049043`

No retained lesson requires3x3 inverse entries or cofactor inverse computation; avoid adding an alternate system-solving algorithm.

**Evidence:** Tutorial 17592186060933 computes all 9 minors and transpose; question 17592186060448 inverse matrix, question 17592186060153 individual inverse entry, question 17592186060450 unknown k via inverse entry.

**Contribution:** Would become necessary if49392 were retained, which explicitly asks3x3 systems by calculating inverse. Further Properties asks determinant OF inverse and uses reciprocal determinant instead. Textbook5.3 inverse examples/exercises are2x2.

**Mastery:** learned=false, accuracy0.6539, mass1.5; skipped for lack of contribution, not mastery.

Captured 5 lesson sections and 68 practice questions. [Actual content](topics/17592186049043/readable.md); full bank `topics/17592186049043/practice.json`.

### SKIP: Solving 2x2 Systems of Equations Using Inverse Matrices — `17592186050944`

2x2 inverse-system numerical method adds no needed capability beyond studied2x2 inverse and Gaussian solving. Graph prerequisite for50906 is not a content requirement.

**Evidence:** Tutorial 17592186093402 derives x=A^-1b; bank 54 only2x2 solve/reorganization.50906 bank instead reasons from equivalences and supplied uniqueness.

**Contribution:** Studied49548 and matrix-column multiplication cover2x2 inverse transformations in textbook5.3. No retained bank explicitly requires inverse2x2 system solving.

**Mastery:** repetitions0 only; no learned/accuracy evidence.

Captured 4 lesson sections and 54 practice questions. [Actual content](topics/17592186050944/readable.md); full bank `topics/17592186050944/practice.json`.

### SKIP: Solving Systems of Equations Using Inverse Matrices — `17592186049392`

Full lesson includes3x3 inverse-system calculation and symbolic premultiplication; no required task or retained bank calls for this computation.

**Evidence:** Bank82:29 given-inverse multiplication,28 calculating inverse,25 matrix algebra; question 17592186092709 explicitly requires finding inverse.

**Contribution:** Textbook5.3 examples/exercises requiring inverse transformations are2x2; determinant inverse law is reciprocal scalar; NxM Gaussian method handles actual homework coefficient systems.

**Mastery:** learned=false, accuracy0.9164, mass2, last direct2026-10-30; insufficient mastery evidence, but not required for chosen sequence.

Captured 4 lesson sections and 82 practice questions. [Actual content](topics/17592186049392/readable.md); full bank `topics/17592186049392/practice.json`.

### SKIP: Orthogonal Matrices — `17592186049606`

Homework supplies definition A^TA=I and asks only determinant possibilities; retained determinant laws and studied transpose/product/inverse definitions suffice. Whole orthogonal lesson adds checks, orthonormal columns, products/inverses not otherwise demanded.

**Evidence:** Bank53:17 orthogonality checks,12 transpose inverses,12 determinant-product applications,12 abstract closure statements. Full-bank question 17592186272134 includes the conceptual statement that every REAL eigenvalue of an orthogonal matrix is ±1; it asks no characteristic-polynomial computation.

**Contribution:** WHW 4 3.1.19 proof can take determinants directly from supplied identity using Basic/Further Properties; textbook5.4 rotations/reflections need their matrices/action, not general orthogonal group lesson.

**Mastery:** learned=false, accuracy0.6485, mass1.5; skipped for excess scope. If later retained, reassess eigenvalue-concept readiness using question 17592186272134; it does not itself require characteristic-root computation.

Captured 8 lesson sections and 53 practice questions. [Actual content](topics/17592186049606/readable.md); full bank `topics/17592186049606/practice.json`.

### SKIP: The Characteristic Equation of a Matrix — `17592186050376`

Eigenvalue/characteristic-polynomial branch is outside named sections and reviewed homework tasks; cannot justify it merely through Orthogonal Matrices graph dependency.

**Evidence:** Bank36:12 triangular3x3 eigenvalues,12 block4x4 characteristic/eigenvalue statements,12 general3x3 polynomial roots. Example 17592186124332 uses rational roots and synthetic division.

**Contribution:** No contribution to retained determinant laws, rank/nullity/subspace or transformation sequence.

**Mastery:** No progress row.

Captured 5 lesson sections and 36 practice questions. [Actual content](topics/17592186050376/readable.md); full bank `topics/17592186050376/practice.json`.

### SKIP: The Eigenvalues and Eigenvectors of a 2x2 Matrix — `17592186048819`

Eigenvectors/eigenvalues are not a requested-section or WHW 4/5 task and are only reached through excluded eigen/orthogonal branch.

**Evidence:** Full tutorial defines Av=λv and tests examples; bank 51 trains eigenvalue/eigenvector identification and eigenvalues from transformation geometry.

**Contribution:** No evidence of need for retained determinant or rectangular-system lessons.

**Mastery:** No target mastery evidence used.

Captured 6 lesson sections and 51 practice questions. [Actual content](topics/17592186048819/readable.md); full bank `topics/17592186048819/practice.json`.

### SKIP: Introduction to Systems of Linear Equations — `17592186048678`

Studied augmented-matrix/Gaussian/RREF lessons already require solving simultaneous equations. Reads intersection of two graphed lines and graph word problems.

**Evidence:** example 17592186138083 and17592186138084; bank 46graph-based questions

**Contribution:** No retained bank requires graph-reading or substitution specifically; required linear systems can be solved with retained Gaussian Elimination For NxM Systems of Equations.

**Mastery:** Legacy repetitions=6.0 is not a learned flag. Redundancy conclusion instead uses inspected studied3x3/singular/RREF tutorials and practice (e.g.50178 general parametric solutions and48742 RREF).

Captured 3 lesson sections and 46 practice questions. [Actual content](topics/17592186048678/readable.md); full bank `topics/17592186048678/practice.json`.

### SKIP: Solving Systems of Linear Equations Using Elimination: One Transformation — `17592186050190`

Studied augmented-matrix/Gaussian/RREF lessons already require solving simultaneous equations. Elementary2-variable elimination, including choosing multiplier and back substitution.

**Evidence:** examples 17592186192585–17592186192588; bank103questions

**Contribution:** No retained bank requires graph-reading or substitution specifically; required linear systems can be solved with retained Gaussian Elimination For NxM Systems of Equations.

**Mastery:** Legacy repetitions=5.0 is not a learned flag. Redundancy conclusion instead uses inspected studied3x3/singular/RREF tutorials and practice (e.g.50178 general parametric solutions and48742 RREF).

Captured 5 lesson sections and 103 practice questions. [Actual content](topics/17592186050190/readable.md); full bank `topics/17592186050190/practice.json`.

### SKIP: Solving Systems of Equations by Substitution — `17592186048826`

Studied augmented-matrix/Gaussian/RREF lessons already require solving simultaneous equations. Alternative2-variable substitution method, including reorganizing equations.

**Evidence:** examples 17592186073445/.446; bank57questions

**Contribution:** No retained bank requires graph-reading or substitution specifically; required linear systems can be solved with retained Gaussian Elimination For NxM Systems of Equations.

**Mastery:** Legacy repetitions=6.0 is not a learned flag. Redundancy conclusion instead uses inspected studied3x3/singular/RREF tutorials and practice (e.g.50178 general parametric solutions and48742 RREF).

Captured 3 lesson sections and 57 practice questions. [Actual content](topics/17592186048826/readable.md); full bank `topics/17592186048826/practice.json`.

### SKIP: Solving Equations Using the Square Root Method — `17592186048187`

No retained new matrix/determinant lesson needs isolating x^2. These enter graph through already studied determinant/minor/inverse topics or excluded eigenvalue branch.

**Evidence:** tutorial 17592186070019; examples 17592186068475–.477; bank 35integer/fraction/radical roots

**Contribution:** Retained NxM parameter bank 27questions uses linear k only; determinant banks operate on constant matrices or determinant symbols/scalars. WHW 4 orthogonal det proof gives simple y^2=1; it does not justify complete quadratic algorithms.

**Mastery:** Legacy repetitions=6.0 only; not a valid learned/mastery claim. If an added whole transformation lesson has quadratic-eigenvalue questions, reassess rather than silently importing all algebra.

Captured 4 lesson sections and 35 practice questions. [Actual content](topics/17592186048187/readable.md); full bank `topics/17592186048187/practice.json`.

### SKIP: Solving Quadratic Equations Using a Difference of Squares — `17592186048157`

No retained new matrix/determinant lesson needs difference-of-squares factorization. These enter graph through already studied determinant/minor/inverse topics or excluded eigenvalue branch.

**Evidence:** tutorial 17592186069945; example 17592186068484 explicitly requires difference-of-squares method; bank 16

**Contribution:** Retained NxM parameter bank 27questions uses linear k only; determinant banks operate on constant matrices or determinant symbols/scalars. WHW 4 orthogonal det proof gives simple y^2=1; it does not justify complete quadratic algorithms.

**Mastery:** Legacy repetitions=6.0 only; not a valid learned/mastery claim. If an added whole transformation lesson has quadratic-eigenvalue questions, reassess rather than silently importing all algebra.

Captured 4 lesson sections and 16 practice questions. [Actual content](topics/17592186048157/readable.md); full bank `topics/17592186048157/practice.json`.

### SKIP: Perfect Square Quadratic Equations with One or No Solutions — `17592186049668`

No retained new matrix/determinant lesson needs one/no-real-root quadratics. These enter graph through already studied determinant/minor/inverse topics or excluded eigenvalue branch.

**Evidence:** tutorial 17592186111919/.920; bank 26including parameter inequalities with no real roots

**Contribution:** Retained NxM parameter bank 27questions uses linear k only; determinant banks operate on constant matrices or determinant symbols/scalars. WHW 4 orthogonal det proof gives simple y^2=1; it does not justify complete quadratic algorithms.

**Mastery:** Legacy repetitions=6.0 only; not a valid learned/mastery claim. If an added whole transformation lesson has quadratic-eigenvalue questions, reassess rather than silently importing all algebra.

Captured 6 lesson sections and 26 practice questions. [Actual content](topics/17592186049668/readable.md); full bank `topics/17592186049668/practice.json`.

### SKIP: Solving Quadratic Equations by Factoring — `17592186048774`

No retained new matrix/determinant lesson needs quadratic factoring. These enter graph through already studied determinant/minor/inverse topics or excluded eigenvalue branch.

**Evidence:** tutorial 17592186065344; bank 21monic quadratic factoring/reorganization

**Contribution:** Retained NxM parameter bank 27questions uses linear k only; determinant banks operate on constant matrices or determinant symbols/scalars. WHW 4 orthogonal det proof gives simple y^2=1; it does not justify complete quadratic algorithms.

**Mastery:** Legacy repetitions=6.0 only; not a valid learned/mastery claim. If an added whole transformation lesson has quadratic-eigenvalue questions, reassess rather than silently importing all algebra.

Captured 4 lesson sections and 21 practice questions. [Actual content](topics/17592186048774/readable.md); full bank `topics/17592186048774/practice.json`.

### SKIP: Solving Quadratic Equations with Leading Coefficients by Factoring — `17592186049832`

No retained new matrix/determinant lesson needs nonmonic quadratic factoring. These enter graph through already studied determinant/minor/inverse topics or excluded eigenvalue branch.

**Evidence:** tutorial 17592186111830; bank 41leading coefficients/common factors

**Contribution:** Retained NxM parameter bank 27questions uses linear k only; determinant banks operate on constant matrices or determinant symbols/scalars. WHW 4 orthogonal det proof gives simple y^2=1; it does not justify complete quadratic algorithms.

**Mastery:** Legacy repetitions=6.0 only; not a valid learned/mastery claim. If an added whole transformation lesson has quadratic-eigenvalue questions, reassess rather than silently importing all algebra.

Captured 4 lesson sections and 41 practice questions. [Actual content](topics/17592186049832/readable.md); full bank `topics/17592186049832/practice.json`.

### SKIP: The Quadratic Formula — `17592186050465`

No retained new matrix/determinant lesson needs general quadratic formula. These enter graph through already studied determinant/minor/inverse topics or excluded eigenvalue branch.

**Evidence:** tutorial 17592186069948; bank 38framework, roots, and no-real-solution cases

**Contribution:** Retained NxM parameter bank 27questions uses linear k only; determinant banks operate on constant matrices or determinant symbols/scalars. WHW 4 orthogonal det proof gives simple y^2=1; it does not justify complete quadratic algorithms.

**Mastery:** Legacy repetitions=6.0 only; not a valid learned/mastery claim. If an added whole transformation lesson has quadratic-eigenvalue questions, reassess rather than silently importing all algebra.

Captured 5 lesson sections and 38 practice questions. [Actual content](topics/17592186050465/readable.md); full bank `topics/17592186050465/practice.json`.

### SKIP: Solving Quadratic Equations With Complex Roots — `17592186049695`

No retained new matrix/determinant lesson needs complex quadratic roots. These enter graph through already studied determinant/minor/inverse topics or excluded eigenvalue branch.

**Evidence:** tutorial 17592186088886/.887; bank 36also requires completing square

**Contribution:** Retained NxM parameter bank 27questions uses linear k only; determinant banks operate on constant matrices or determinant symbols/scalars. WHW 4 orthogonal det proof gives simple y^2=1; it does not justify complete quadratic algorithms.

**Mastery:** Legacy repetitions=2.0 only; not a valid learned/mastery claim. If an added whole transformation lesson has quadratic-eigenvalue questions, reassess rather than silently importing all algebra.

Captured 5 lesson sections and 36 practice questions. [Actual content](topics/17592186049695/readable.md); full bank `topics/17592186049695/practice.json`.

## Why equivalent methods differ here

Laplace expansion remains because the retained lessons ask explicitly for designated row/column expansions or equivalent3x3 determinants; using only first-row expansion or triangular elimination would not prepare their whole practice. Cofactor inversion and inverse-system solving are excluded because no retained task demands those methods. In particular, computing a determinant of an inverse uses the reciprocal determinant and never requires a3x3 inverse matrix.

Conditions When a Determinant Equals Zero remains before Further Properties because its linearity questions use identical-row zero determinants. Its volume interpretation is already developed in Basic Properties; it does not force the scalar triple product/projection/3D volume branch.

## Content order edges

- **The Determinant of an NxN Matrix** (`17592186050092`) → **Finding Determinants Using Laplace Expansions** (`17592186048505`).
- **Finding Determinants Using Laplace Expansions** (`17592186048505`) → **Basic Properties of Determinants** (`17592186049159`).
- **Basic Properties of Determinants** (`17592186049159`) → **Row and Column Operations on Determinants** (`17592186048462`).
- **Row and Column Operations on Determinants** (`17592186048462`) → **Conditions When a Determinant Equals Zero** (`17592186049312`).
- **Row and Column Operations on Determinants** (`17592186048462`) → **Finding Determinants Using Row and Column Operations** (`17592186049685`).
- **Finding Determinants Using Laplace Expansions** (`17592186048505`) → **Finding Determinants Using Row and Column Operations** (`17592186049685`).
- **Basic Properties of Determinants** (`17592186049159`) → **Further Properties of Determinants** (`17592186049875`).
- **Conditions When a Determinant Equals Zero** (`17592186049312`) → **Further Properties of Determinants** (`17592186049875`).
- **The Invertible Matrix Theorem in Terms of 2x2 Systems of Equations** (`17592186050906`) → **The Invertible Matrix Theorem in Terms of Dimension, Rank and Nullity** (`17592186049340`).
- **The Dimension of the Null Space of a Matrix** (`17592186050996`) → **The Invertible Matrix Theorem in Terms of Dimension, Rank and Nullity** (`17592186049340`).
- **Gaussian Elimination For NxM Systems of Equations** (`17592186048445`) → **The Dimension of the Null Space of a Matrix** (`17592186050996`).

## Limits

- In-classW5D1–W6D3 content not inspected by this branch; parent owns capture/coverage crosscheck.
- Parent must interleave Rank/Null Space/Column Space/Dimension lessons before50996/49340; study_order_branch is not complete global sequence.
- Orthogonal Matrices tutorial/solution contains an overbroad claim that all eigenvalues are ±1; question 17592186272134 correctly qualifies its option as REAL eigenvalue. Its practice does contain this conceptual eigenvalue task. No repairs performed.
- Studied graph prerequisite50527 has no row in target progress capture, so scope studied classification is used without inventing accuracy statistics.
