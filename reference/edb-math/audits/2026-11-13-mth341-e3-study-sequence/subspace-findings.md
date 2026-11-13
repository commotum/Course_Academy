# Subspace, basis, rank and image branch audit

Captured lesson/practice/graph/progress basis: **14416**. Read-only manual audit; no assignment, learner, target or match changes. All recommendations mean complete lessons.

Keep concrete foundations even when later lessons repeat definitions: column-space membership, span basis, column-space basis, coordinates, dimension, rectangular elimination, null-space membership and null-basis work each stage a genuinely unlearned idea before later combined questions. This is an efficient learning sequence, not a smallest topic count.

## Recommended whole-lesson order

1. **Gaussian Elimination For NxM Systems of Equations — 17592186048445**
2. **Subspaces of N-Dimensional Space — 17592186051046**
3. **Subspaces of N-Dimensional Space: Geometric Interpretation — 17592186048337**
4. **The Column Space of a Matrix — 17592186050656**
5. **The Null Space of a Matrix — 17592186048181**
6. **Finding a Basis of a Span — 17592186049222**
7. **Expressing the Coordinates of a Vector in a Given Basis — 17592186050638**
8. **Finding a Basis of the Column Space of a Matrix — 17592186049009**
9. **The Dimension of a Span — 17592186048218**
10. **The Rank of a Matrix — 17592186050028**
11. **Finding a Basis of the Null Space of a Matrix — 17592186048823**
12. **The Dimension of the Null Space of a Matrix — 17592186050996**
13. **The Invertible Matrix Theorem in Terms of 2x2 Systems of Equations — 17592186050906**
14. **The Invertible Matrix Theorem in Terms of Dimension, Rank and Nullity — 17592186049340**
15. **The Rank-Nullity Theorem — 17592186048978**
16. **The Image and Rank of a Linear Transformation — 17592186049539**
17. **The Kernel of a Linear Transformation — 17592186049903**
18. **The Rank-Nullity Theorem in Terms of Linear Transformations — 17592186049880**

Several adjacent lessons can commute: see each after constraint below. Parent verified textbook5.7 explicitly covers kernel/image subspaces and bases, trivial-kernel criterion, and dimension(V)=dimension(kernel)+dimension(image); Kernel and transformation Rank-Nullity are therefore firm keeps. Coordinates belongs after basis and before the guide4 proof, not necessarily before numerical rank.

## Decisions with actual content evidence

### KEEP: Gaussian Elimination For NxM Systems of Equations — 17592186048445

The rectangular/free-variable extension is short enough to earn its place before null-space and 4x6 homework work. Studied RREF/singular 3x3 supply operations, but no direct learned rectangular lesson exists.

Actual content: 17592186116493: 2 equations/3 unknowns reduced to x=1-4z,y=-3z and affine vector form.; 17592186115751: Rectangular consistent system: reduce and give its general solution..

Downstream benefit or bypass: Ease Null Space, null-basis and WHW-5 4x6 rank work; explicit free versus pivot variables.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186048445/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: Subspaces of N-Dimensional Space — 17592186051046

First actual subspace criterion lesson; symbolic arbitrary-vector closure examples have real instructional value before image proofs. Entire practice is line/plane classification, so proof production remains a separate transfer demand.

Actual content: 17592186121126: Proves y=3x closed using arbitrary u,v,c; explains zero necessity.; 17592186121127: Builds line through origin from two points, proves closure componentwise.; 17592186121128: Proves z=4x-2y closed by symbolic addition and scaling.; 17592186120145: Select zero membership/addition/scalar closure/subspace for x=2y..

Downstream benefit or bypass: Guide 2 Subspace Test; guide 3 scalar-closure disproof; WHW-5 dot-product and parametric-set subspace claims.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186051046/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: Subspaces of N-Dimensional Space: Geometric Interpretation — 17592186048337

Outside expansion, but earns a place as a concrete sequel: bounded and nonlinear sets containing zero defeat the misleading origin-only heuristic from line/plane examples.

Actual content: 17592186193877: Explains failure of addition/scaling on non-subspace diagrams.; 17592186192505: x^2=y fails scaling; shifted parametric line requires testing origin.; 17592186193383: Disk radius 1 fails sufficiently large scaling; half-plane fails negation.; 17592186193313: Distinguishes homogeneous plane, affine set, and trivial zero set defined by sum of squares <=0..

Downstream benefit or bypass: Guide 3 bounded slab |u1|<=4; basis/null/column lessons use zero/line/plane interpretation.

Order: Subspaces of N-Dimensional Space (17592186051046).

Evidence: [lesson and representative practice](topics/17592186048337/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: The Column Space of a Matrix — 17592186050656

Keep the concrete membership/consistency foundation even though Image/Rank repeats the definition later. Learner has no learned column-space lesson; this stages a new set concept before basis extraction/rank/image vocabulary.

Actual content: 17592186121037: Defines column space as span and converts membership to Ax=b.; 17592186119670: Finds k for consistency with a 3x2 coefficient matrix.; 17592186121038: Col(A) is a subspace of R^m for m x n A; membership iff consistency.; 17592186120313: Solve membership then coefficient product..

Downstream benefit or bypass: Image witness idea and WHW-5 column-space/rank interpretation; separates output space R^m from input space R^n.

Order: Gaussian Elimination For NxM Systems of Equations (17592186048445), Subspaces of N-Dimensional Space: Geometric Interpretation (17592186048337).

Evidence: [lesson and representative practice](topics/17592186050656/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: The Null Space of a Matrix — 17592186048181

Keep elementary zero-product membership and parametric null-set work before extracting a basis. Matrix-vector product is mastered; the null-set interpretation is unstudied and has only one recorded practice mass.

Actual content: 17592186119623: Checks three candidates by computing A b_i.; 17592186121063: Null(A)={(-3x2,x2):x2 real}; distinguishes free/basic variable.; 17592186119625: Invertible 2x2 example yields Null(A)={0}.; 17592186120333: Find k so vector belongs to Null(A)..

Downstream benefit or bypass: Null-basis/nullity/IMT chain; WHW-5 dependence via nonzero homogeneous solution.

Order: Gaussian Elimination For NxM Systems of Equations (17592186048445), Subspaces of N-Dimensional Space: Geometric Interpretation (17592186048337).

Evidence: [lesson and representative practice](topics/17592186048181/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: Finding a Basis of a Span — 17592186049222

Foundational basis lesson is needed despite learned independence: distinguishes independent spanning subset from redundant generating set and explains why deletion preserves span.

Actual content: 17592186121040: Substitutes a3=-a1+3a2 into an arbitrary original linear combination to prove unchanged span.; 17592186121064: Find basis via pivots, explicitly original columns.; 17592186119673: Check proposed basis and express fourth vector using three coefficients.; 17592186120523: Both independence and same-span reasoning, then coefficients..

Downstream benefit or bypass: WHW-4 dependence relations/independent same-span sets; WHW-5 basis/dimension; generic basis expansion in guide 4.

Order: Subspaces of N-Dimensional Space: Geometric Interpretation (17592186048337).

Evidence: [lesson and representative practice](topics/17592186049222/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: Expressing the Coordinates of a Vector in a Given Basis — 17592186050638

Coordinates for an arbitrary ordered basis are not supplied by mastered standard-matrix computation. Concrete forward/reverse representation practice substantially eases applying T to an expansion in an arbitrary basis.

Actual content: 17592186121042: Defines basis coordinates as unique coefficients; 2D subspace of R3 example.; 17592186119633: Solves coordinates in a three-vector nonstandard basis.; 17592186121066: Shows standard basis independence, spanning, and equality of standard coordinates and components.; 17592186120525: Permuted standard vectors make order matter..

Downstream benefit or bypass: Guide 4 im(T)=span(T(v_i)); matrix in basis/standard basis course coverage.

Order: Finding a Basis of a Span (17592186049222).

Evidence: [lesson and representative practice](topics/17592186050638/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: Finding a Basis of the Column Space of a Matrix — 17592186049009

Although Basis of a Span has the algorithm, retain matrix-specific practice and original-column warning: WHW-5 #8 requires the column-space basis alongside a different row-basis rule. No mastered basis-extraction topic supplies this distinction.

Actual content: 17592186151943: Col(A) basis from original pivot columns, not echelon columns.; 17592186153353: Nonpivot RREF entries supply a redundant original column combination.; 17592186151945: 3x4 matrix, check proposed column basis and recover fourth-column coefficients.; 17592186152581: 3x3 matrix has rank 2; retain original columns 1,2..

Downstream benefit or bypass: WHW-5 bases for spans and column space; prepares dimension/rank with concrete objects.

Order: Finding a Basis of a Span (17592186049222), The Column Space of a Matrix (17592186050656).

Evidence: [lesson and representative practice](topics/17592186049009/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: The Dimension of a Span — 17592186048218

Basis size as dimension is new; includes ambient dim(R^n)=n needed for cardinality proofs, not merely numerical rank.

Actual content: 17592186121056: Every basis has the same number of vectors; defines dimension.; 17592186119660: Row reduction finds dimension 1 of redundant 3-vector span.; 17592186121057: Standard basis has n vectors, dim(R^n)=n.; 17592186120365: Compute dimension by row reduction..

Downstream benefit or bypass: WHW-5 basis/dimension and too-many-vectors arguments; rank definition.

Order: Finding a Basis of a Span (17592186049222).

Evidence: [lesson and representative practice](topics/17592186048218/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: The Rank of a Matrix — 17592186050028

Links dimension/column basis to pivots and nonzero echelon rows. No learned rank record exists, so do not replace conceptual rank learning with mastered pivot counting.

Actual content: 17592186121058: Defines rank=dim Col(A) and explains two original columns form basis.; 17592186119661: 4x7 matrix with 3 nonpivots has rank 4.; 17592186121068: Rank equals pivot count and nonzero echelon-row count.; 17592186120385: Reduce 4x4 matrix and find rank..

Downstream benefit or bypass: WHW-5 final 4x6 rank task, ambient dimension bounds, image rank and nullity.

Order: Finding a Basis of the Column Space of a Matrix (17592186049009), The Dimension of a Span (17592186048218).

Evidence: [lesson and representative practice](topics/17592186050028/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: Finding a Basis of the Null Space of a Matrix — 17592186048823

Outside expansion and necessary for efficient whole-lesson nullity/IMT learning: turns free-variable descriptions into independent generators, including empty basis of zero space.

Actual content: 17592186121041: Derives a null basis and explicitly states basis of {0} is empty set.; 17592186119628: Two free parameters in R4 split into two generators.; 17592186119629: Rectangular RREF with pivots 1,3 gives free coordinates 2,4.; 17592186120387: 3x4 RREF yields a one-vector null basis..

Downstream benefit or bypass: Dimension of Null Space introductory derivation and IMT practice about empty basis; kernel basis practice if retained.

Order: The Null Space of a Matrix (17592186048181), Finding a Basis of a Span (17592186049222).

Evidence: [lesson and representative practice](topics/17592186048823/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: The Dimension of the Null Space of a Matrix — 17592186050996

Outside expansion but supplies the genuinely new correspondence free variables <-> null basis size before IMT asks students to interpret parametric null spaces.

Actual content: 17592186125778: One nonpivot gives explicit one-vector basis and dimension 1.; 17592186124317: 9x11 with 9 pivots has null dimension 2.; 17592186124319: 4x4 row reduction yields nullity 1.; 17592186124871: 4x5 null dimension from reduction..

Downstream benefit or bypass: IMT full rank/nullity-zero equivalence; WHW-5 too-many-columns nontrivial homogeneous solution.

Order: Finding a Basis of the Null Space of a Matrix (17592186048823), The Rank of a Matrix (17592186050028).

Evidence: [lesson and representative practice](topics/17592186050996/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: The Invertible Matrix Theorem in Terms of 2x2 Systems of Equations — 17592186050906

Keep a concrete first statement of inverse/determinant/unique-solution equivalence before its higher-dimensional vector-space reformulation. Entire questions are theorem implications, so inverse-matrix solving lesson is not required beforehand.

Actual content: 17592186116491: Equivalent invertibility, unique Ax=b for all b, unique homogeneous zero, one line intersection, nonzero determinant.; 17592186115066: Parameterized 2x2 determinant used to infer system properties.; 17592186115734: Given two lines intersect once, complete implication..

Downstream benefit or bypass: General dimension/rank/nullity IMT and determinant implications from homework.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186050906/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: The Invertible Matrix Theorem in Terms of Dimension, Rank and Nullity — 17592186049340

New finite-dimensional equivalences explicitly explain why nullity zero forces all columns pivotal and Col(A)=R^n. This eases WHW-5 independent n vectors -> full span rather than leaving a theorem-transfer leap.

Actual content: 17592186125780: Explains invertible -> Null={0} -> nullity0 -> all columns pivot -> rank n -> Col=R^n.; 17592186124320: Parametric 1D null space of 4x4 gives noninvertibility/rank not 4.; 17592186125167: Nonzero determinant implies empty null-space basis and n pivot columns..

Downstream benefit or bypass: WHW-5 independent five vectors in R5 span; rank/nullity section coverage; integrates determinant and vector-space views.

Order: The Invertible Matrix Theorem in Terms of 2x2 Systems of Equations (17592186050906), The Dimension of the Null Space of a Matrix (17592186050996).

Evidence: [lesson and representative practice](topics/17592186049340/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: The Rank-Nullity Theorem — 17592186048978

Outside expansion, compact and explicitly covers matrix rank-nullity (confirmed textbook 4.10.5); rank and nullity separately do not themselves give the integrated theorem practice.

Actual content: 17592186185320: Pivot+nonpivot columns=n yields rank+nullity=n for nonsquare matrices.; 17592186184070: 3x5 matrix with 3-element column basis has null dimension 2.; 17592186184759: Infer rank from a two-parameter null space in R4.; 17592186184755: Combine IMT with rank-nullity and a given null-space span..

Downstream benefit or bypass: Rectangular rank/nullity inference; WHW-5 dimension bounds; whole course section explicitly named.

Order: The Invertible Matrix Theorem in Terms of Dimension, Rank and Nullity (17592186049340).

Evidence: [lesson and representative practice](topics/17592186048978/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: The Image and Rank of a Linear Transformation — 17592186049539

Actual image membership, standard-matrix bridge and rank(T)=dim im(T) need a complete lesson. It does not prove image closure or the arbitrary-basis image equality.

Actual content: 17592186125783: Defines image by existence of preimage and gives concrete witness.; 17592186125819: im(T)=Col(T)=span of standard-matrix columns.; 17592186124328: Find a preimage by solving Tx=b.; 17592186125116: Compute transformation rank from matrix..

Downstream benefit or bypass: Guide 2 image witness interpretation; guide 4 standard-basis special case; chapter5 image/rank.

Order: The Rank of a Matrix (17592186050028), Expressing the Coordinates of a Vector in a Given Basis (17592186050638).

Evidence: [lesson and representative practice](topics/17592186049539/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: The Kernel of a Linear Transformation — 17592186049903

Outside expansion; first kernel vocabulary, basis and nullity of a transformation. Parent verified textbook5.7 explicitly requires kernels, kernel bases and trivial-kernel criterion.

Actual content: 17592186125818: Ker(T)=Null(standard matrix).; 17592186125820: Nullity(T)=dim Ker(T)=nullity(matrix).; 17592186125105: Find basis of kernel from a 2x2 map..

Downstream benefit or bypass: Course kernel coverage; transfers null-space learning to transformation language.

Order: The Dimension of the Null Space of a Matrix (17592186050996).

Evidence: [lesson and representative practice](topics/17592186049903/readable.md); full captured bank is adjacent `practice.json`.

### KEEP: The Rank-Nullity Theorem in Terms of Linear Transformations — 17592186049880

Outside expansion; parent verified textbook5.7 explicitly requires dimension(V)=dimension(kernel)+dimension(image). Descriptions of image/kernel and bijection implications make transfer from the matrix theorem substantially easier.

Actual content: 17592186189365: Rank/nullity of transformation with image y+2z=0.; 17592186188207: Given independent image generators, infer standard-matrix rank/nullity/bijection.; 17592186188924: Infer nullity from image defined by -x+z=0..

Downstream benefit or bypass: Rank-nullity in transformation language and image-dimension reasoning.

Order: The Rank-Nullity Theorem (17592186048978), The Image and Rank of a Linear Transformation (17592186049539), The Kernel of a Linear Transformation (17592186049903).

Evidence: [lesson and representative practice](topics/17592186049880/readable.md); full captured bank is adjacent `practice.json`.

### SKIP: Linear Combinations of Vectors in N-Dimensional Euclidean Space — 17592186048499

Genuinely useful elementary coefficient training, but current learned Span and Independence lessons already use exactly the same vector-to-system conversion and solve 2/3 coefficients. Eight direct practice mass on this unlearned topic further supports bypassing its whole lesson.

Actual content: 17592186119618: Two coefficients from vector equality.; 17592186119669: Three coefficients from 3D vectors.; 17592186120311: One coefficient with R4 vectors..

Downstream benefit or bypass: Skills supplied by learned Span 48315 and Independence50426; no new dependency is introduced by skipping.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186048499/readable.md); full captured bank is adjacent `practice.json`.

### SKIP: Linear Combinations of Vectors and Their Properties — 17592186051014

Geometric head-to-tail combination drawing plus equating abstract coefficients for nonparallel vectors is not used by retained lessons; numerical linear combination meaning is already practiced in learned span/independence.

Actual content: 17592186096449: Draw 2a+3b.; 17592186096450: Solve alpha,beta by coefficient equality for a nonparallel pair.; 17592186096970: 5a+4b=(2s+t)a+(s-t)b..

Downstream benefit or bypass: No required retained downstream question uses diagram construction or this abstract coefficient trick.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186051014/readable.md); full captured bank is adjacent `practice.json`.

### SKIP: Subspaces of Abstract Vector Spaces — 17592186050453

Whole lesson is polynomial/matrix/function subspace classification, outside supplied Euclidean coursework. Basic+geometric subspace lessons already supply closure proofs and counterexamples; no retained question needs abstract vector axioms or polynomial/function ambient spaces.

Actual content: 17592186124402: Polynomial subset at^3-bt.; 17592186124401: Matrices with nonnegative trace: addition yes, negative scaling no.; 17592186124301: Continuous functions satisfying f(0)=-f(2).; 17592186125156: Constant continuous functions, select closure statements..

Downstream benefit or bypass: Retained lessons use R^n only; skip stops its continuity/axiom prerequisite branch.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186050453/readable.md); full captured bank is adjacent `practice.json`.

### SKIP: Defining Abstract Vector Spaces — 17592186049064

Formal axiom definition and completing axiom-labelled proofs are not used by any retained subspace/rank/image question. Closure criterion is directly taught in retained Euclidean lessons.

Actual content: 17592186184065: Fill axiom labels in proof w+w=w implies w=0.; 17592186184094: Degree exactly3 polynomials fail addition closure..

Downstream benefit or bypass: No formal axiomatic proof demand in actual guide2-4 or WHW4/5.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186049064/readable.md); full captured bank is adjacent `practice.json`.

### SKIP: Introduction to Abstract Vector Spaces — 17592186049737

Mostly abstract closure/property identification and eight-property tables for polynomials/functions/matrices. Useful for a later abstract-vector course, but no retained lesson needs those settings.

Actual content: 17592186125860: Degree>=5 polynomials not closed under addition.; 17592186124765: Identify matrix identity/commutativity statements.; 17592186125240: Functions f(0)=1 fail closure..

Downstream benefit or bypass: Euclidean closure retained directly; no need to add polynomial/function/complex prerequisite chain.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186049737/readable.md); full captured bank is adjacent `practice.json`.

### SKIP: Continuity Over an Interval — 17592186048176

Continuity of graph intervals is only relevant to skipped abstract-function examples. Even those examples ask evaluation closure, not diagnosing discontinuities.

Actual content: 17592186078987: Identify open intervals of continuity from a graph.; 17592186078991: Identify largest continuity intervals..

Downstream benefit or bypass: No retained downstream question uses continuity or endpoint analysis.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186048176/readable.md); full captured bank is adjacent `practice.json`.

### SKIP: Describing Planar Regions Using Set-Builder Notation — 17592186051063

Whole lesson trains describing shaded planar sets, with boundary inclusion. Retained subspace lesson explicitly introduces its needed set-builder reading, and geometric sequel asks membership/closure rather than authoring regions.

Actual content: 17592186198772: Write rectangle inequalities with open/closed edges.; 17592186198774: Describe parabolic shaded region in set-builder notation..

Downstream benefit or bypass: Guide bounded slab notation and retained set conditions require reading a condition only; supplied by basic subspace tutorial.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186051063/readable.md); full captured bank is adjacent `practice.json`.

### SKIP: The Cartesian Equation of a Plane — 17592186050830

Whole normal-vector/cross-product Cartesian plane construction is not used by retained subspace questions; those give an equation or derive simple parameterized coordinates inside the lesson.

Actual content: 17592186119643: Find Cartesian plane through point perpendicular to normal.; 17592186119646: Find plane parallel to two vectors using normal..

Downstream benefit or bypass: Retained Subspaces51046 checks a supplied plane equation; no need for normal-vector construction.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186050830/readable.md); full captured bank is adjacent `practice.json`.

### SKIP: The Vector Equation of a Plane — 17592186049436

Dot-product normal form of a plane and finding parallel vectors/perpendicular-line planes do not appear in retained subspace questions. Learned Parametric Plane50308 supplies the representation actually used.

Actual content: 17592186119642: Find plane perpendicular to a parametric line.; 17592186120248: Find missing components in a vector parallel to plane..

Downstream benefit or bypass: WHW5 w dot u=0 uses closure/linearity, not constructing a normal-form plane.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186049436/readable.md); full captured bank is adjacent `practice.json`.

### SKIP: The Cartesian Equation of a Line — 17592186048850

Retained basic subspace lesson derives its own simple Cartesian ratio from a direction vector. Full Cartesian-line lesson adds zero-denominator cases and equation conversions not asked downstream.

Actual content: 17592186119638: Convert given parametric line to Cartesian ratios.; 17592186119656: Handle zero direction component..

Downstream benefit or bypass: Studied Vector Equation Line49485 (practice accuracy~1.00,mass21.25) and retained subspace derivation suffice.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186048850/readable.md); full captured bank is adjacent `practice.json`.

### SKIP: The Parametric Equations of a Line — 17592186048729

Parametric/vector conversion and line segments are supplied where needed by learned vector-line and parametric-plane work; no retained question asks restricted line segments.

Actual content: 17592186124227: Rewrite parametric equations as vector equation.; 17592186124230: Parametrize a bounded line segment..

Downstream benefit or bypass: Retained subspace lessons use unrestricted real parameters and derive coordinate form themselves.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186048729/readable.md); full captured bank is adjacent `practice.json`.

### SKIP: Solving 2x2 Systems of Equations Using Inverse Matrices — 17592186050944

The IMT2x2 whole lesson asks implications and determinant recognition, not solving by A inverse b. Learned Inverses2x2 and MatrixColumnVector already supply inverse/product meanings and computations if needed.

Actual content: 17592186092023: Solve system specifically using inverse matrix.; 17592186093404: Inverse method unavailable when determinant0..

Downstream benefit or bypass: No retained IMT question requires performing inverse solution; learned inverse accuracy .923,mass14.33 and product accuracy~1,mass21.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186050944/readable.md); full captured bank is adjacent `practice.json`.

### SKIP: The Four Fundamental Subspaces of a Matrix — 17592186049881

Does define row space, but entire lesson adds orthogonal complements, four-space dimension identities and their images; does not teach row-basis extraction. Poor whole-lesson bridge for WHW5 final problem. Flag narrow row-space/row-operation transfer rather than asserting this topic repairs it.

Actual content: 17592186135110: Row space=Col(A^T); left nullspace and orthogonal complements.; 17592186133704: Image of row space under A is Col(A).; 17592186134077: Orthogonal subspace of Null(XY) requires transpose product.; 17592186134070: Dimension of Col from left-null dimension..

Downstream benefit or bypass: Can compute a valid row basis by applying retained BasisSpan to original rows (transpose); row-space definition and reduced-nonzero-row rule still need course transfer evidence.

Order: No new prerequisite lesson required in this branch..

Evidence: [lesson and representative practice](topics/17592186049881/readable.md); full captured bank is adjacent `practice.json`.

## Mastery supplied by already studied lessons

- **Linear Span of Vectors in N-Dimensional Euclidean Space — 17592186048315**: Actual lesson converts membership to two-coefficient systems, handles consistency and parameter k; practice17592186120303/17592186120294. Recorded learned=True; practice accuracy=0.8614142088603246; practice mass=10.5.
- **Linear Dependence and Independence — 17592186050426**: Actual lesson converts three-vector independence to homogeneous system; tutorial17592186121124, example17592186119499, practice17592186120300. Recorded learned=True; practice accuracy=0.7414777348305867; practice mass=8.666666666666666.
- **Reduced Row Echelon Form — 17592186048742**: Actual full RREF procedure, including one/two pivots and free variables; examples17592186096546/17592186096547. Recorded learned=True; practice accuracy=0.8915913974272565; practice mass=21.5.
- **Solving 3x3 Singular Systems of Equations Using Gaussian Elimination — 17592186050178**: Actual general solutions for 3x3 singular one/two-pivot systems; examples17592186105604/17592186105605. Recorded learned=True; practice accuracy=0.9136494774646351; practice mass=14.166666666666666.

The unlearned N-dimensional-combinations lesson also has practice mass8, accuracy0.837. This supports skipping its elementary one/two/three-coefficient operations only because the actual learned span/independence lessons already exercise the same operations. Learned flags alone are not proof mastery. Studied vector-line and parametric-plane lessons also support skipping Cartesian normal/line conversion branches.

## Transfer and remaining coverage gaps

- **Guide2 image subspace proof (required written transfer)**: Retained subspace lessons show symbolic closure and image lesson gives witnesses, but practice asks classification/numerical preimages. Student must choose preimages u=Ax,v=Ay and use A(x+y),A(cx),A0; no captured lesson asks constructing this proof.
- **Guide4 arbitrary-basis image equality (required written transfer)**: Coordinates teaches arbitrary basis expansion; ImageRank proves/uses standard matrix column-space equality only. Need both inclusions using x=sum c_i v_i, linearity, and converse sum c_i T(v_i)=T(sum c_i v_i). Parent set-proof audit covers inclusion technique.
- **Guide3 |u1|<=4 (required written transfer)**: Geometric disk/half-plane counterexamples teach the move but practice is classification. Need explicit member (4,0,0,0) and scalar2 to disprove scalar closure.
- **Textbook5.7 kernel/image subspace and basis proofs (required written transfer)**: Kernel49903 proves T(0)=0 and identifies Ker(T)=Null(matrix), but its questions are numerical membership, basis or nullity. No retained question asks arbitrary u,v in Ker(T) then T(alpha u+beta v)=0. ImageRank similarly lacks symbolic image closure. BasisSpan/ColumnBasis/NullBasis provide computations; learner must connect a spanning image set or null parameterization to proof of independent spanning.
- **Rank-nullity on V a subspace, and one-to-one criterion (required generalization)**: TransformationRankNullity49880 states its theorem for T:R^n->R^n and uses n as domain dimension; its mixed practice also assumes bijection/invertibility vocabulary. Actual textbook5.7 needs dimension(V) for an arbitrary subspace domain, including non-square maps. Parent transformation branch must cover trivial-kernel iff one-to-one, and the basis argument for dimension(V)=dimensionKer+dimensionImage; retained numerical rank-nullity lessons alone do not prove it.
- **WHW5 final row-space basis (coverage gap unless coursework supplies it)**: Retained BasisSpan can be applied to transposed rows to yield a valid original-row basis. None of kept lessons explicitly names row space or proves elementary row operations preserve it / nonzero echelon rows form its basis. FourFundamental defines row space but does not teach extraction and brings unrelated orthogonal-complement machinery. Parent should identify existing coursework treatment; do not silently claim no gap.
- **WHW5 #6/#7 cardinality (required written justification)**: Retained dimension, nullity, IMT teach needed pivot facts. Their practice remains numerical/statement classification, so learner must write independent columns -> no free variables -> full square rank -> every RHS attainable, and m x (m+1) -> free variable -> nontrivial relation.

## Prerequisite closure decisions

Graph arrows run from prerequisite to dependent. For retained subspace lesson, unlearned linear-combination operations are supplied by actual studied span/independence work; Cartesian plane and set-builder authoring add operations unused by any retained question. Its geometric sequel is retained because bounded/nonlinear counterexamples materially ease the actual task. Basis prerequisites are the retained subspace bridge and studied independence. Column-space and null-space use retained rectangular elimination plus learned matrix products. Column-basis uses retained span-basis and column-space; coordinates and dimension use retained span-basis. Rank uses retained dimension/column-basis; image uses retained rank and studied standard matrix. Null-basis is an outside bridge after retained null-space and basis; nullity follows null-basis/rank. IMT uses concrete IMT2x2 plus nullity. The inverse-system-solving prerequisite of IMT2x2 can be skipped: actual IMT questions ask implications, not inverse-based system computation, and inverse/product calculations are already learned. Rank-nullity is a second outside bridge after IMT; its mixed questions use the full theorem chain.

Abstract subspaces is excluded on actual polynomial/function/matrix content, so its continuity and formal abstract-vector prerequisite branches are pruned rather than recursively added. None of the retained lessons uses formal axiom labels. Four Fundamental Subspaces is excluded despite attractive title: it adds orthogonal complement and four-space image machinery without teaching the missing row-basis extraction.

## Content caveats

- **The Dimension of a Span (17592186048218)**: Tutorial17592186121057 labels zero-space basis as no basis; mathematically empty set is its basis. Retained NullBasis48823 and IMT practice17592186125167 correctly explain empty basis. Do not repeat the tutorial error.
- **Subspaces of N-Dimensional Space (17592186051046)**: First criterion omits explicit nonempty condition; all practiced lines/planes are nonempty. Written general subspace tests must establish zero membership/nonemptiness (image via A0).

## Final independent challenge: function sets and proof methods

**Keep Sets and Functions — 17592186050312** before image/range work. Tutorial17592186173160 distinguishes range from codomain using missing arrows and domain restriction; example17592186171840 and practice17592186645038 test the exact false inference that the declared target equals the range. This supplies an actual conceptual gap in the learned introductory transformation lesson.

**Skip Proving Subset Relations — 17592186048468 in the current whole-lesson sequence.** Its arbitrary-element/witness rewriting and two-inclusion explanations are directly useful (tutorials17592186205271/17592186205285; example17592186203728), and it is the better conceptual bridge than the set-laws lesson. However, the whole lesson includes modular and trigonometric set examples. All18select fields in its8practice questions lack answer keys, all solutions are empty, and the prompts ask proof openings/inclusion headings rather than the actual complete argument. `available=true` establishes accessible content, not a complete assessment. A mandatory incomplete general-proof prerequisite does not efficiently resolve the actual production gap.

**Skip Proving Elementary Properties of Set Operations — 17592186048715.** Its whole lesson adds set laws, biconditional chains, contradiction and Cartesian products. Its6practice questions are also scaffolds with missing keys. Those methods add little to direct image/kernel closure and basis-image witness inclusion proofs.

Original guide2–4 and textbook5.7 written proofs remain **required completion work**, not optional enrichment. Their full original problems provide the needed production setting after the retained mathematics lessons. This recommendation does not declare proof mastery, does not propose a partial study of either general proof lesson, and does not add newly authored lessons.

## Late prerequisite challenge: transformation invertibility

**Keep The Invertible Matrix Theorem in Terms of Linear Transformations — 17592186049371**, a compact outside-expansion bridge (4sections,34captured questions). Place it after matrix IMT49340, ImageRank49539 and Kernel49903, and **before transformation Rank-Nullity49880**.

Tutorial17592186125784 defines inverse linear transformation/bijection, states equivalence with standard-matrix invertibility, then translates column/null space into image/kernel language. This is not supplied merely by the learned general Invertible Functions49731 lesson. Actual practice17592186125118 and17592186272020 requires the useful argument that distinct v1,v2 with T(v1)=T(v2) give the nonzero kernel vector v1-v2, hence deficient rank. Practice17592186125164 begins with a missing image vector and asks for rank/kernel/invertibility consequences. This whole practice materially eases both textbook5.3 and the mixed bank of retained49880, rather than merely repeating definitions.

The lesson remains limited to square maps Rn→Rn. Original textbook5.7 proof practice for arbitrary subspaces V,W, the general one-to-one/trivial-kernel equivalence and rank-nullity remains required. Do not transfer its one-to-one/onto equivalence to arbitrary rectangular maps. This adds one firm keep to the original branch decisions (19keep,13skip; Sets and Functions is separately endorsed in the preceding addendum).
