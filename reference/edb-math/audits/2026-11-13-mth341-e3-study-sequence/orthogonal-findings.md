# Orthogonality and geometry whole-lesson findings

Basis **14416**. Read-only audit; whole lessons only. Actual tutorials, all worked examples, representative practice from every captured skill, and full relevant Orthogonal-Matrices true-statement and Component-Dot-Product unknown banks were inspected.

## Recommendation

Keep **Calculating the Dot Product Using Angle and Magnitude (17592186050938)** for proof linearity, **Dilations and Reflections as Linear Transformations (17592186049719)** and **Rotations as Linear Transformations (17592186049891)** for textbook5.4, and **Shear and Stretch as Linear Transformations (17592186050231)** as a real whole-practice prerequisite of retained composition lesson17592186050646. These are missing from the original119; learned Standard Matrix does not teach their geometric formulas.

The proposed27 roots also include material overscope: default omit **Calculating the Dot Product Using Components (17592186048954)** because learned nD vectors/matrix products cover it, and default omit **Orthogonal Matrices (17592186049606)** unless in-class evidence requires its full tests/inverse/product work. WHW4 gives the orthogonal definition in the determinant-proof prompt.

Textbook5.4 was read in the local Kuttler extraction, printedpp286–291: rotations/reflections, their vector action, compositions, arbitrary-line reflections, and one3D combined transformation. It does **not** teach shear/stretch. This branch has not inspected actual W5D1–W6D3 activities.

## Decisions and actual-content evidence

### KEEP: Rotations as Linear Transformations — 17592186049891

Learned: False (flag present); repetitions 0.0. Whole captured practice: 43 questions. Rotating a Vector About the Origin: 13; Interpreting a Given Matrix as a Rotation: 18; Rotating an Object About the Origin: 12.

Textbook 5.4 explicitly requires general rotation matrices and action on vectors; learned Standard Matrix only reads coefficients and does not teach the geometric matrix. This is an omitted root worth adding to the proposed sequence.

Downstream: Whole lesson includes object rotation, so matrix multiplication and reading planar coordinates are real dependencies; its worked example 17592186092069 fully teaches the column-packing procedure, avoiding a compulsory extra Objects lesson.

Evidence: 17592186093435 — General counterclockwise and clockwise rotation matrices.; 17592186092805 — Apply pi/3 rotation to (2,-1).; 17592186092829 — Infer angle/quadrant from a given rotation matrix and rotate a diagram vector.; 17592186092515 — Rotate all triangle vertices; requires ordinary row-by-column products..

Capture: [topics/17592186049891/readable.md](topics/17592186049891/readable.md).

### KEEP: Dilations and Reflections as Linear Transformations — 17592186049719

Learned: False (flag absent); repetitions 0.0. Whole captured practice: 38 questions. Finding the Standard Matrix of a Dilation Given a Vector and its Image: 21; Identifying the Linear Transformation Represented by a Matrix: 17.

Textbook 5.4 requires axes reflections and rotation/reflection compositions; this is the closest captured whole lesson for reflection matrices. Its dilation skill adds overhead but the reflection tutorial and skill are substantive, unlearned, and absent from learned Standard Matrix.

Downstream: Needs coordinate scalar multiples and standard matrices, already represented in learned nD Vectors/Standard Matrix. It does not require calculating images of arbitrary line equations.

Evidence: 17592186088931 — Matrices of x-axis and y-axis reflection.; 17592186088956 — Matrices of reflection in y=x and y=-x.; 17592186088359 — Choose matrix of y-axis reflection.; 17592186088155 — Dilation matrix from vector/image ratio; additional whole-lesson cost..

Capture: [topics/17592186049719/readable.md](topics/17592186049719/readable.md).

### SKIP: Linear Transformations of Points and Lines in the Plane — 17592186049063

Learned: False (flag present); repetitions 0.0. Whole captured practice: 43 questions. Computing the Image of a Point Under a Linear Transformation of a Plane: 10; Computing the Image of a Line Given by an Equation in Slope-Intercept Form: 17; Computing the Image of a Line Given by an Equation in Standard Form: 16.

Whole practice is 10 point-image multiplications plus 33 images of line equations. Textbook 5.4 asks rotation/reflection matrices and their vector action, not the equation of an arbitrary image line. Learned Standard Matrix covers the point/vector mechanic. No retained rotation/reflection lesson question requires its slope-intercept or standard-line reconstruction.

Condition: Reconsider only if actual in-class tasks explicitly require image-line equations; do not infer from the word transformation.

Downstream: Not needed by retained general rotation/reflection whole practice; prerequisite for excluded Objects in the stored graph is not a substantive dependency of its polygon multiplication.

Evidence: 17592186151976 — Find image equation of y=3x-2 using two transformed points.; 17592186152772 — Find equation of image of 2x+y-3=0.; 17592186153366 — Tutorial proves nonsingular maps take lines to lines using T(p+td); useful but not practiced as a proof..

Capture: [topics/17592186049063/readable.md](topics/17592186049063/readable.md).

### CONDITIONAL: Linear Transformations of Objects in the Plane — 17592186049420

Learned: False (flag absent); repetitions 0.0. Whole captured practice: 32 questions. Computing the Image of a Line Segment Under the Action of a Linear Transformation: 16; Computing the Image of a Polygon Under the Action of a Linear Transformation: 16.

Whole lesson teaches endpoint/vertex packing and matrix products (32 segment/polygon questions), which genuinely recur in retained Rotations. However, every needed multiplication is already learned and the general rotation worked example repeats the procedure completely; default omit to avoid redundant whole lessons.

Condition: Keep as a short preparatory whole lesson if reading diagrams or treating several vertices as columns is a current difficulty; it is a legitimate smoother foundation for retained rotation object practice, not an eigenvalue prerequisite by itself.

Downstream: Would precede Rotations/Dilations and Reflections. If retained, learned Matrix Multiplication suffices; Points and Lines whole lesson is not needed for its actual segment/polygon questions.

Evidence: 17592186087566 — Pack triangle vertices as columns and multiply TX.; 17592186088388 — Compute vertices of image triangle.; 17592186292882 — Transform both endpoints of a segment..

Capture: [topics/17592186049420/readable.md](topics/17592186049420/readable.md).

### CONDITIONAL: Right-Angle Rotations as Linear Transformations — 17592186048712

Learned: False (flag present); repetitions 0.0. Whole captured practice: 46 questions. Using a Matrix That Represents a Rotation of 180 Degrees: 14; Identifying Rotation Matrices: 17; Using a Matrix That Represents a Rotation of 90 Degrees: 15.

Right-angle direction conventions are useful for textbook 5.4, but whole 46-question lesson duplicates the general rotation formula and application already taught in retained Rotations. Default omit given learned matrix multiplication and prior geometry repetitions.

Condition: Keep before General Rotations if clockwise/counterclockwise direction or basis-image geometry is not secure; no need to require solely because graph lists it.

Evidence: 17592186093431 — Derive 90-degree rotation from standard basis images.; 17592186092520 — Clockwise 90-degree rotation of triangle vertices.; 17592186092827 — Interpret right-angle matrix and choose vector graph..

Capture: [topics/17592186048712/readable.md](topics/17592186048712/readable.md).

### KEEP: Shear and Stretch as Linear Transformations — 17592186050231

Learned: False (flag absent); repetitions 0.0. Whole captured practice: 27 questions. Finding the Standard Matrix of a Stretch Transformation Given a Vector and its Image: 6; Identifying a Shear or Stretch Transformation Given the Images of the Standard Basis Vectors: 7; Identifying a Shear or Stretch Transformation Represented by a Matrix: 7; Finding the Image of a Square Under a Shear or Stretch Transformation: 7.

Retain as instructional preparation for the retained whole Combining Linear Transformations Using 2x2 Matrices (17592186050646): parent inspected its full bank and found assumed shear/stretch matrices in questions17592186092830,17592186281513,17592186092525,17592186092860. This is a real downstream requirement even though textbook5.4 itself has only rotations/reflections.

Condition: Keep because the actual retained composition whole lesson needs it; not a claim that textbook5.4 directly covers shears.

Downstream: Whole practice needs basis-vector images and polygon coordinates, covered in its own examples plus studied multiplication; no angle or projection chain. Order before whole Combining Linear Transformations Using2x2 Matrices.

Evidence: 17592186107089 — Horizontal shear matrix via basis images.; 17592186106035 — Interpret [[1,10],[0,1]] as horizontal shear.; 17592186106307 — Choose image of a square under shear..

Capture: [topics/17592186050231/readable.md](topics/17592186050231/readable.md).

### SKIP: Calculating the Dot Product Using Components — 17592186048954

Learned: False (flag absent); repetitions 2.0. Whole captured practice: 55 questions. Calculating the Dot Product Using the General Formula: 29; Solving for an Unknown Given Two Perpendicular Vectors: 26.

Mapped root is materially redundant for this learner: learned Vectors in N-Dimensional Euclidean Space defines nD component dot products and practices both direct products and unknown dot-product equations; learned matrix multiplication uses the same row/column arithmetic. WHW5 needs dot-product linearity, not another 55-question component lesson.

Condition: If retained after evidence of a real component/perpendicularity gap, square-root solving and perfect-square recognition are actual whole-practice dependencies; this is not permission to add quadratic formula or complex roots.

Downstream: Whole Orthogonal Matrices can use already learned matrix multiplication; it does not force this redundant root. For proof linearity prefer the short Angle and Magnitude lesson condition below.

Evidence: 17592186060030 — Direct component dot product.; 17592186060184 — Perpendicular condition gives x^2-4=0 with sign restriction.; 17592186060185 — Perpendicular condition gives (x-3)^2=0.; 17592186633605 — Another perfect-square trinomial unknown..

Capture: [topics/17592186048954/readable.md](topics/17592186048954/readable.md).

### KEEP: Calculating the Dot Product Using Angle and Magnitude — 17592186050938

Learned: False (flag absent); repetitions 2.0. Whole captured practice: 13 questions. Calculating the Dot Product of Two Vectors Given Their Magnitudes and Angle: 2; Calculating the Dot Product of Two Vectors Given Their Magnitudes and Directions: 2; Calculating Dot Product Expressions Using the Properties of the Dot Product: 2; Calculating the Dot Product of Perpendicular Vectors: 7.

Despite its geometry title, this 13-question whole lesson explicitly teaches distributivity/scalar linearity, the exact algebra used in WHW5 4.10.44. Retain this modest whole lesson to make the proof algebra explicit; learned nD Vectors practices component products, while this lesson directly practices distributivity. Graph has prior repetitions 2 but no learned flag.

Condition: Recommended keep as a smoother proof foundation; omit only on explicit evidence that dot-linearity is already fluent. Do not expand its trigonometry graph blindly.

Downstream: Useful before WHW5 subspace proof and optionally orthogonal material. The cosine angle computations are whole-lesson overhead but small compared with Components plus its quadratic support.

Evidence: 17592186060918 — Dot product distributes and scalars factor out.; 17592186059541 — Worked expansion of (2a-b) dot c.; 17592186060156 — Expand (5a+2b) dot c from known dot products.; 17592186677698 — Use perpendicularity plus distributivity..

Capture: [topics/17592186050938/readable.md](topics/17592186050938/readable.md).

### CONDITIONAL: Orthogonal Matrices — 17592186049606

Learned: False (flag present); repetitions 0.0. Whole captured practice: 53 questions. Identifying Orthogonal Matrices: 17; Calculating the Inverse of an Orthogonal Matrix: 12; Calculating the Determinant of a Product of Matrices: 12; Identifying True Statements About Orthogonal Matrices: 12.

Mapped root has some relevant determinant content, but WHW4 3.1.19 supplies A^T A=I and needs determinant product/transpose laws; textbook 5.4 rotation/reflection matrices do not require a full orthogonal-matrix classification course. Default skip unless in-class orthogonal tests/inverse identities are genuinely in scope.

Condition: Keep if actual in-class work calls for full orthogonality, transpose inverse, or product identities. This changes prerequisite judgments, not just selected pages.

Downstream: Actual practice needs learned transpose/product/inverse meaning and retained determinant laws. A single real-eigenvalue recognition option is the only captured eigenvalue demand; no characteristic polynomial computation. Solving via known transpose does not require cofactor inversion or generic inverse-system lessons.

Evidence: 17592186135178 — Properties tutorial states det(Q)=±1 and eigenvalue modulus 1; later text omits real qualifier.; 17592186134146 — Test a 3x3 matrix using AA^T.; 17592186134242 — Solve Ax=b using A^T when A orthogonal.; 17592186134244 — Compute |det(PQ)| using orthogonal det magnitude 1.; 17592186272134 — One true/false option says a REAL eigenvalue of Q is ±1; same question tests determinant converse and Q-I singularity.; 17592186485514 — Similarity determinant, product orthogonality, and counterexample for 2P+Q..

Capture: [topics/17592186049606/readable.md](topics/17592186049606/readable.md).

### CONDITIONAL: Orthogonal Sets in Euclidean Spaces — 17592186049811

Learned: False (flag present); repetitions 0.0. Whole captured practice: 46 questions. Determining Whether Sets are Orthogonal: 11; Determining Whether Sets are Orthonormal: 12; Extending a Set to Form an Orthogonal Basis: 12; Extending a Set to Form an Orthonormal Basis: 11.

Whole lesson adds 23 questions constructing orthogonal/orthonormal bases, beyond the few pairwise tests needed to understand Orthogonal Matrices. Useful if that downstream whole root is retained and orthonormality is unfamiliar; otherwise omit.

Condition: Keep only for genuine orthogonal-set/basis work or as deliberate smoother preparation for retained full Orthogonal Matrices.

Downstream: If retained, normalization and homogeneous free-variable solving are actual requirements; no projection formula or angle inverse calculation appears.

Evidence: 17592186135090 — Defines orthonormality and nonzero orthogonal-set independence.; 17592186134220 — Extend three vectors to orthogonal basis of R4 by homogeneous elimination.; 17592186134221 — Extend orthonormal set by solving homogeneous constraints and normalizing..

Capture: [topics/17592186049811/readable.md](topics/17592186049811/readable.md).

### CONDITIONAL: Unit Vectors — 17592186049360

Learned: False (flag absent); repetitions 6.0. Whole captured practice: 77 questions. Finding a Unit Vector Parallel to a Given Vector: 26; Finding a Unit Vector Parallel to a Given Vector in a Diagram: 24; Finding a Unit Vector Parallel to a Vector Sum: 27.

Unit vectors matter if whole Orthogonal Sets is kept, but this lesson is 77 questions including diagrams and compass-direction vector sums. Orthogonal Matrices tests can use squared self-dot=1 from its own introduction, and default selected sequence omits orthogonal basis construction.

Condition: Keep only if normalization is a genuine difficulty before retained Orthogonal Sets; prior repetitions6 suggests familiarity despite no learned flag.

Downstream: A needed normalization skill does not automatically justify 77 whole questions when learned norms and the orthogonal-set worked examples already supply the procedure.

Evidence: 17592186097833 — Normalize by vector magnitude.; 17592186097161 — Normalize sum read from a scaled grid.; 17592186097043 — Normalize northeast plus southeast vectors via Pythagoras..

Capture: [topics/17592186049360/readable.md](topics/17592186049360/readable.md).

### SKIP: Parallel Vectors — 17592186049715

Learned: False (flag absent); repetitions 6.0. Whole captured practice: 74 questions. Creating Parallel Vectors: 25; Determining Whether Two Vectors are Parallel: 25; Identifying Parallel Vectors From a Diagram: 24.

Graph-only geometric precursor; learned vector scalar operations and dependence work supply scalar multiples. Whole lesson largely draws/identifies parallel arrows and compares coefficients, adding no needed new operation to retained rotation/reflection lessons.

Downstream: Prior repetitions6 but no learned flag; do not treat that flag as proof of an actual deficit.

Evidence: 17592186097030 — Scale factor in 4a-12b=lambda(a-3b).; 17592186096968 — Choose drawn 3a and -a..

Capture: [topics/17592186049715/readable.md](topics/17592186049715/readable.md).

### SKIP: The Angle Between Two Vectors — 17592186050336

Learned: False (flag absent); repetitions 0.0. Whole captured practice: 51 questions. Finding the Angle Between Two Vectors Given Their Components: 18; Finding the Angle Between Two Vectors Given Three Points: 16; Finding the Angle Between Two Vectors Given the Value of Their Dot Product: 17.

51 questions compute inverse-cosine angles from components/points/unknown dot-product constraints. Retained rotation-matrix angle recognition reads sine/cosine entries and quadrants; it is not the angle-between-vectors procedure. Orthogonal tests use dot=0 without angle computation.

Downstream: No retained downstream lesson question needs arbitrary vector-angle recovery; projection chain is excluded.

Evidence: 17592186105588 — Compute arccos of normalized dot product.; 17592186106107 — Find angle QPR from three points.; 17592186106109 — Solve unknown then calculate angle..

Capture: [topics/17592186050336/readable.md](topics/17592186050336/readable.md).

### SKIP: Calculating a Scalar Projection — 17592186049653

Learned: False (flag present); repetitions 0.0. Whole captured practice: 102 questions. Calculating a Scalar Projection Using Angles and Magnitudes: 37; Calculating a Scalar Projection Using Components: 38; Projecting a Vector Onto a Perpendicular Vector: 27.

Whole 102-question scalar-projection lesson covers |a|cos(theta), component projection, and zero-projection unknowns. None is required by determinant proofs, dot-linear subspace proof, or rotation/reflection matrix practice.

Downstream: Matrix auditor confirms determinant/volume instruction is available without retaining full Volumes of Parallelepipeds; no hidden retained volume requirement.

Evidence: 17592186105489 — Compute component scalar projection -15/sqrt53.; 17592186106213 — Zero scalar projection implies dot=0, solve x..

Capture: [topics/17592186049653/readable.md](topics/17592186049653/readable.md).

### SKIP: Calculating a Vector Projection — 17592186050394

Learned: False (flag absent); repetitions 0.0. Whole captured practice: 73 questions. Calculating a Vector Projection Using Angle and Magnitude: 17; Calculating a Vector Projection Using Components: 28; Perpendicular Vectors: 28.

Whole 73-question vector-projection lesson teaches (a dot b)/(b dot b)b and angle/magnitude projection. It is not needed just because orthogonality or rotations are in scope.

Downstream: No retained downstream question uses projection decomposition; scalar-dot subspace proof does not project.

Evidence: 17592186105479 — Compute projection vector from components.; 17592186106172 — Zero projection implies perpendicular and solve unknown..

Capture: [topics/17592186050394/readable.md](topics/17592186050394/readable.md).

### CONDITIONAL: The Eigenvalues and Eigenvectors of a 2x2 Matrix — 17592186048819

Learned: False (flag present); repetitions 0.0. Whole captured practice: 51 questions. Finding the Eigenvalue that Corresponds to a Given Eigenvector: 10; Plotting the Product of a Matrix and an Eigenvector Given its Corresponding Eigenvalue: 13; Determining the Value of an Unknown Given an Eigenvalue and Eigenvector of a Matrix: 15; Identifying True Statements About Eigenvalues and Eigenvectors: 13.

Basic Av=lambda v meaning could smooth the lone REAL-eigenvalue option in retained Orthogonal Matrices, but whole 51-question lesson contains plotting, unknown eigenvector parameters, and inverse eigenvalue statements; no independent exam eigenvalue scope found.

Condition: Default skip when Orthogonal Matrices is omitted. If that root is kept and eigenvalue meaning is unknown, this is the bounded existing whole-lesson candidate; do not force its irrelevant Objects graph prerequisite.

Downstream: Unknown-parameter exercises can solve a linear coordinate equation and check the other; no characteristic equation required.

Evidence: 17592186107090 — Defines eigenvector/eigenvalue via Av=lambda v.; 17592186106296 — Check supplied eigenvector, read lambda.; 17592186244030 — Eigenvector of inverse has reciprocal eigenvalue..

Capture: [topics/17592186048819/readable.md](topics/17592186048819/readable.md).

### SKIP: Calculating the Eigenvalues of a 2x2 Matrix — 17592186050001

Learned: False (flag absent); repetitions 0. Whole captured practice: 56 questions. Finding the Characteristic Equation of a Matrix: 15; Computing the Eigenvalues of a Matrix With Two Distinct Eigenvalues: 13; Computing the Eigenvalues of a Matrix With At Most One Distinct Eigenvalue: 13; Calculating the Eigenvalues of a Triangular/Diagonal Matrix: 15.

Whole 56-question 2x2 characteristic-equation/root-computation lesson exceeds the only downstream eigenvalue recognition demand. Orthogonal Matrices never asks to calculate its eigenvalues.

Downstream: Skipping this removes need for quadratic-formula/discriminant chains on this branch; do not add complex-root computation merely because tutorial acknowledges complex eigenvalues.

Evidence: 17592186092076 — Characteristic quadratic solved with quadratic formula.; 17592186092691 — Negative discriminant gives no real eigenvalue..

Capture: [topics/17592186050001/readable.md](topics/17592186050001/readable.md).

### SKIP: The Characteristic Equation of a Matrix — 17592186050376

Learned: False (flag absent); repetitions 0. Whole captured practice: 36 questions. Calculating the Eigenvalues of a 3x3 Matrix Containing a Block of Zeros: 12; Calculating the Eigenvalues of a 4x4 Matrix Containing a Block of Zeros: 12; Finding the Eigenvalues of a General 3x3 Matrix: 12.

Whole 36-question characteristic lesson calculates 3x3/4x4 eigenvalues and cubic roots. It is materially unnecessary for any retained whole lesson in this branch, including Orthogonal Matrices.

Downstream: Reject graph prerequisite from Orthogonal Matrices; no captured question in that lesson computes characteristic roots.

Evidence: 17592186124332 — General cubic characteristic polynomial, rational roots and synthetic division.; 17592186125062 — 4x4 expansion and multiplicity..

Capture: [topics/17592186050376/readable.md](topics/17592186050376/readable.md).

### CONDITIONAL: Solving Equations Using the Square Root Method — 17592186048187

Learned: False (flag absent); repetitions 6.0. Whole captured practice: 35 questions. Solving Equations With Integer Solutions: 8; Solving Equations With Fractional Solutions: 14; Solving Equations With Radical Solutions: 13.

Square-root method is an actual requirement if redundant whole Components is retained: many perpendicularity questions give x^2=c, including non-square radical values. Default omit because learned nD vectors already covers dot-product arithmetic and the new Components root is omitted.

Condition: Keep only following a demonstrated square-root gap and a retained downstream need; prior repetitions6 suggests familiarity.

Evidence: 17592186068477 — Worked radical solutions.; 17592186069139 — Solve z^2=50..

Capture: [topics/17592186048187/readable.md](topics/17592186048187/readable.md).

### CONDITIONAL: Solving Perfect Square Quadratic Equations — 17592186048963

Learned: False (flag absent); repetitions 6.0. Whole captured practice: 41 questions. Equations Where the Perfect Square is Isolated: 18; Equations Where the Perfect Square Is Not Isolated: 20; Solving Equations by Factoring: 3.

Perfect-square recognition is an actual requirement in Components questions 17592186060185/17592186633605 and learned nD example17592186119615. Whole 41-question lesson also solves shifted squares and even semicircle equations, a substantial expansion beyond zero repeated roots.

Condition: Default omit unless repeated-root solving is demonstrably weak in retained downstream practice; do not mechanically require this 41-question lesson.

Evidence: 17592186110347 — Factor t^2-10t+25 before square-root solving.; 17592186235497 — Practice includes deriving semicircle equations..

Capture: [topics/17592186048963/readable.md](topics/17592186048963/readable.md).

### SKIP: Three-Dimensional Vectors in Component Form — 17592186050173

Learned: False (flag present); repetitions 3.0. Whole captured practice: 15 questions. Expressing a Position Vector in Component Form Given Its Graph: 7; Converting Between Alternative Notations: 4; Expressing a Position Vector in Component Form Given Its Endpoints: 4.

15-question 3D notation/position-vector lesson is graph precursor to Components, but learned nD vectors and heavily practiced matrix-vector multiplication already use its column-vector representation. No retained rotation question needs 3D picture-to-position conversion.

Evidence: 17592186101950 — i,j,k / angle-bracket / column-vector conversion.; 17592186101274 — Endpoint displacement in 3D..

Capture: [topics/17592186050173/readable.md](topics/17592186050173/readable.md).

### SKIP: Two-Dimensional Vectors Expressed in Component Form — 17592186048816

Learned: False (flag absent); repetitions 6.0. Whole captured practice: 16 questions. Expressing a Position Vector in Component Form: 4; Expressing a Position Vector in Angle Bracket Notation: 5; Expressing a Vector in Component Form: 7.

16-question planar component/position-vector lesson is familiar foundational notation with prior repetitions6. Retained rotations and reflection examples state coordinates and use learned matrix-vector mechanics.

Evidence: 17592186100675 — Endpoint subtraction in the plane.; 17592186101254 — Convert AB from given coordinates..

Capture: [topics/17592186048816/readable.md](topics/17592186048816/readable.md).

### SKIP: Describing Properties of the Cosine Function — 17592186049091

Learned: False (flag present); repetitions 0.0. Whole captured practice: 88 questions. Describing Properties of the Cosine Function: 38; Utilizing the Periodicity Property of the Cosine Function: 27; Utilizing the Evenness Property of the Cosine Function: 23.

Whole 88-question cosine graph-property lesson is dominated by zeros/maxima/range and periodicity expressions. General rotation needs sign/evenness but teaches clockwise conversion itself; learned inverse-trig work and prior trig expressions support actual special-angle calculations.

Downstream: Do not enforce broad cosine property graph as prerequisite to a retained rotation matrix lesson.

Evidence: 17592186177082 — Cos(-x)=cos(x).; 17592186176449 — Zeros/extrema/range recognition.; 17592186176355 — Simplify cos(-x+16pi)..

Capture: [topics/17592186049091/readable.md](topics/17592186049091/readable.md).

### CONDITIONAL: Describing Properties of the Sine Function — 17592186050172

Learned: False (flag present); repetitions 3.0. Whole captured practice: 15 questions. Describing Properties of the Sine Function: 4; Utilizing the Periodicity Property of the Sine Function: 6; Utilizing the Oddness Property of the Sine Function: 5.

Small 15-question sine-property lesson gives oddness/periodicity useful for negative-angle rotations, but the rotation lesson explicitly teaches its clockwise matrix and does not ask graph maxima/minima.

Condition: Default omit; keep only if negative-angle signs remain a demonstrated obstacle. Prior repetitions3 indicates familiarity.

Evidence: 17592186173261 — Sin(-x)=-sin(x).; 17592186172316 — Evaluate sin(-a) from sin(a)..

Capture: [topics/17592186050172/readable.md](topics/17592186050172/readable.md).

### CONDITIONAL: Elementary Trigonometric Equations Containing Tangent — 17592186050105

Learned: False (flag absent); repetitions 0.0. Whole captured practice: 41 questions. Solving a Trigonometric Equation Involving Tangent with Special Angles: 7; Solving a Trigonometric Equation Involving Tangent with Non-Special Angles: 12; Solving a Trigonometric Equation Involving Tangent Under a Modified Domain: 11; Finding the Points of Intersection of a Horizontal Line and a Tangent Curve: 11.

41-question tangent-equation lesson helps choose angle in correct quadrant in whole Rotations interpretation skill, but most practice generates all solutions in intervals and intersects curves, exceeding rotation needs. Learned inverse trig already supplies principal-value evaluations.

Condition: Keep before Rotations only if matrix-angle interpretation fails because quadrant selection is unknown; do not mandate the whole lesson from graph alone.

Evidence: 17592186093388 — Arctan principal value plus pi.; 17592186256517 — All roots of tan=-sqrt3 on [0,2pi).; 17592186092624 — Graph intersection root..

Capture: [topics/17592186050105/readable.md](topics/17592186050105/readable.md).

### SKIP: Projection Matrices, Linear Transformations and Their Properties — 17592186049489

Learned: False (flag present); repetitions 0.0. Whole captured practice: 46 questions. Finding a Matrix that Defines an Orthogonal Projection Onto the Subspace Spanned by a Vector: 10; Finding a Matrix That Defines an Orthogonal Projection Onto the Subspace Spanned by a Plane: 12; Identifying an Orthogonal Projection Matrix: 12; Finding an Orthogonal Projection Matrix Given Vectors That Span the Orthogonal Complement: 12.

Whole 46-question advanced projection matrix lesson includes A(A^TA)^-1 A^T onto lines/planes and orthogonal complements. Neither textbook5.4 nor WHW4/5 requires this; arbitrary-line reflection is not a license to study all projection machinery.

Evidence: 17592186133599 — Projection matrix onto 3D line.; 17592186134304 — Projection onto span of two 3D vectors.; 17592186134255 — Projection onto R4 orthogonal complement..

Capture: [topics/17592186049489/readable.md](topics/17592186049489/readable.md).

### SKIP: Orthogonal Linear Transformations — 17592186050910

Learned: False (flag present); repetitions 0.0. Whole captured practice: 27 questions. Applying the Angle Preserving Property of Orthogonal Linear Transformations: 12; Identifying the Orthogonality of a Two-Vector Set: 15.

Whole 27-question orthogonal-map lesson practices norm/dot preservation and orthogonal/orthonormal sets. Textbook5.4 mentions length/angle preservation to justify rotation linearity but tests explicit matrices and compositions; this extra root does not fill missing arbitrary-line reflection formulas.

Evidence: 17592186198978 — Use norm preservation to read transformed norm.; 17592186198749 — Classify transformed orthogonal/orthonormal set..

Capture: [topics/17592186050910/readable.md](topics/17592186050910/readable.md).

## Existing learned foundations

- **Vectors in N-Dimensional Euclidean Space (17592186049814)**: learned=True, repetitions=1.9760257288696197. Evidence content IDs 17592186121033, 17592186119614, 17592186119615, 17592186120308. Use existing mastery; no default whole relearning.

- **Multiplying a Matrix by a Column Vector (17592186050825)**: learned=True, repetitions=3.2700995120750584. Evidence content IDs 17592186101956, 17592186101957, 17592186101115. Use existing mastery; no default whole relearning.

- **Multiplying Square Matrices (17592186048297)**: learned=True, repetitions=2.3444168126549085. Evidence content IDs 17592186060930, 17592186059555, 17592186059599. Use existing mastery; no default whole relearning.

- **The Standard Matrix of a Linear Transformation (17592186048203)**: learned=True, repetitions=1.1535913405212241. Evidence content IDs 17592186125781, 17592186124324, 17592186125111. Use existing mastery; no default whole relearning.

- **The Transpose of a Matrix (17592186050727)**: learned=True, repetitions=2.4547614926628514. Evidence content IDs 17592186060928, 17592186060929, 17592186059967. Use existing mastery; no default whole relearning.

- **Introduction to the Inverse of a Matrix (17592186049125)**: learned=True, repetitions=1.815739353224678. Evidence content IDs 17592186088893, 17592186087507. Use existing mastery; no default whole relearning.

- **Evaluating Expressions Containing Inverse Trigonometric Functions (17592186050071)**: learned=True, repetitions=1.5521325240577042. Evidence content IDs 17592186060956, 17592186060961, 17592186059610, 17592186060245. Use existing mastery; no default whole relearning.

In particular, nD Vectors tutorial17592186121033 defines component dot products in any dimension; worked examples17592186119614/615 and practice17592186120308 include component arithmetic and unknown zero-dot equations. Matrix-vector tutorial17592186101956 uses row-dot-column products; tutorial17592186101957 supplies the linear-combination-of-columns view. These are substantive evidence against reopening the unlearned Components graph root.

## Order and prerequisite boundaries

- Learned Standard Matrix / Matrix Multiplication → retained Rotations and Dilations/Reflections.

- Objects is optional smoothing before retained geometric lessons; its endpoint/vertex packing is repeated in their own worked examples. Points-and-Lines equation reconstruction is not required by any retained question.

- Right-angle rotations and tangent-equation repair precede General Rotations only if direction/quadrant difficulties are observed. Do not add cosine graph88 questions or sine graph properties merely from edges.

- If full Orthogonal Matrices is independently retained: learned transpose/product/inverse meaning plus determinant properties precede it. Its Ax=b questions use a *given* orthogonal matrix and x=Aᵀb; no cofactor inversion is required. Its only eigenvalue demand is one real-eigenvalue recognition option17592186272134. Basic eigenvalue meaning may justify the introductory eigenvector whole lesson conditionally; characteristic roots, cubic equations, quadratic formula, and complex roots do not follow.

- If full Orthogonal Sets is independently retained: homogeneous-system/free-variable work and normalization are real requirements, because constructing orthogonal/orthonormal bases is actually practiced. Projection and inverse-angle chains still do not follow.

- If full Components is retained despite redundancy: x²=c and perfect-square recognition are genuinely required by actual practice. Distinguish these bounded algebra needs from the large eigenvalue quadratic chain.

## Remaining scope gaps

- Textbook5.4 arbitrary-line reflection Q_m and exercise5.4.16 rotate-reflect-rotate are not directly taught by retained Dilations and Reflections (axes/y=±x only). Parent composition/basis branch should assess existing whole lessons; do not pretend these two roots close it.

- Textbook5.4.15 z-axis rotation plus xy-plane reflection in R3 is outside captured 2D lesson practice.

- Rotation-angle sum derivation and non-special pi/12,5pi/12 exact values need composition/sum-angle evidence; main parent is checking composition.

- No W5D1–W6D3 source content was supplied to this branch; full orthogonal tests remain conditional on that independent scope. Shear/stretch is retained for actual composition practice rather than a direct textbook claim.

## Actual prerequisite sufficiency for retained geometry

**Trigonometry has substantive existing mastery evidence.** Evaluating Expressions Containing Inverse Trigonometric Functions (17592186050071) is learned, repetitions1.5521325240577042. Its actual tutorial17592186060961 uses the unit circle and quadrant signs; example17592186059620 adjusts a coterminal angle; example17592186059610 and practice17592186060245 evaluate arctan of ±sqrt3. Therefore the basic exact-angle, quadrant, principal-value work is already represented in mastered content. Evaluating Trigonometric Expressions (17592186050848) has no learned flag but repetitions5; actual examples17592186184051/17592186184106 and question17592186578809 use special-angle sine/cosine in degrees/radians. Default omit this15-question whole lesson; retain only if exact-value evaluation proves weak.

General Rotations requires special-angle sine/cosine and reverse matrix-angle interpretation; its tutorial17592186093435 explicitly supplies the clockwise negative-angle formula. Broad cosine88 questions, sine15 graph-properties questions, and tangent41 all-solutions questions are not automatic requirements. The needed row-by-column products are learned; polygon vertex packing is explicitly re-taught in the retained rotation example17592186092069. Objects remains optional smoothing; image-line reconstruction has no downstream role in these whole lessons.

Shear and Stretch (17592186050231) must precede retained Combining Linear Transformations Using2x2 Matrices (17592186050646), because the parent inspected actual whole composition practice that assumes these matrices. This corrects the exam-only impression that shear/stretch is dispensable: it is absent from textbook5.4 but necessary for the retained existing lesson's questions.

## Read-only content-quality flag

Tutorial says every orthogonal matrix has only ±1 eigenvalues without a real qualifier; true for real eigenvalues, not all complex eigenvalues. Practice17592186272134 correctly includes real qualifier in option. Read-only flag only; no correction performed.

Availability: all inspected lesson/practice APIs returned basis14416. Some legacy practice items have empty worked solutions and some rely on captured image references; this does not remove their whole-lesson question demand. No database, assignment, learner-progress, question, or lesson content was changed.
