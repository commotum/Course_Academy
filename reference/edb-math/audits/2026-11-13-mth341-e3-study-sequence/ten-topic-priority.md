# MTH 341 E3: ten-lesson priority plan

This supersedes the 32-lesson recommendation only for the user’s new ten-lesson time budget. It is exam triage with explicit omissions, not a claim of complete coverage. All selections are whole lessons. No assignment, target, progress or content changes.

## Recommended study order

1. **Subspaces of N-Dimensional Space** — `17592186051046`
   Core zero/addition/scalar-closure criteria for guide problems 2 and 3; supports all later spaces.
2. **Subspaces of N-Dimensional Space: Geometric Interpretation** — `17592186048337`
   Bounded and nonlinear counterexamples directly prepare guide problem 3. Keeps this explicit-guide skill ahead of peripheral transformations.
3. **Finding a Basis of a Span** — `17592186049222`
   Basis definition, independence, deleting redundant generators, original pivot columns and basis expansions. Guide problem 4 and WHW5; also addresses limited basis practice and the missed E2 independence question.
4. **The Dimension of a Span** — `17592186048218`
   Basis cardinality, ambient dimension and dimension computations for WHW5 and the named subspace sections.
5. **The Rank of a Matrix** — `17592186050028`
   Connects pivots, column-space dimension and nonzero echelon rows. Especially useful for the E1 pivot/free-variable mistakes.
6. **The Image and Rank of a Linear Transformation** — `17592186049539`
   Direct image-as-column-span bridge for guide problems 2 and 4; includes image membership and rank(T), consolidating the separate Column Space lesson.
7. **The Kernel of a Linear Transformation** — `17592186049903`
   Consolidates kernel/null-space membership, homogeneous solutions, basis examples and nullity; new textbook5.7 coverage using already practiced elimination.
8. **The Rank-Nullity Theorem** — `17592186048978`
   Explicitly covers rectangular matrices: rank plus nullity equals number of COLUMNS. Intro expands a two-parameter null space into two generators; directly targets the E1 equation/variable-count confusion. Prefer this version over the square-map-only transformation version under this budget.
9. **The Invertible Matrix Theorem in Terms of Linear Transformations** — `17592186049371`
   Combines image, kernel, rank, nullity, collisions and invertibility in conceptual questions. Useful for textbook5.3/5.7 and the prior exams’ question style; does not replace the general injectivity proof.
10. **Rotations as Linear Transformations** — `17592186049891`
   One whole lesson for genuinely new geometric formulas from textbook5.4, protecting some breadth beyond the three sample proof questions. Lowest priority of these ten.

## Personal evidence

- E1 Q13:9/9 on row-reduction work; E1 Q3:1/3 and Q5:0/2 on pivots/free variables versus variable count. Keep conceptual rank/nullity and avoid spending scarce lesson slots repeating elimination mechanics.
- E2 Q3:6/6 on a 4x4 determinant; Q9:6/6 on determinant-based singularity (submitted0? shows uncertainty despite full credit); Q10:6/6 on a 3x3 inverse. E2 Q8:0/2 on independence. These are task-level observations, not proof of permanent mastery.
- E2 Q5:0/2 on the determinant-of-product-with-inverse identity; revisit this exact item, assuming B is invertible as required for its expression. The score does not tell us whether the cause was a law misconception or the omitted hypothesis.
- Current graph basis 14431 marks all ten unstudied; question readiness at 14432 confirms sufficient inventory for all ten. Earlier practice snapshot: limited BasisSpan practice around60% over mass1.83, versus RREF around89% over mass21.5. The newer exam performance strengthens prioritization of interpretation over repeated algorithms.

## Deliberate consolidation

- BasisSpan teaches selecting original pivot columns and interpreting redundant generators, so no separate ColumnBasis lesson in this budget.
- ImageRank defines image=column space=span(columns) and practices consistency, so no separate ColumnSpace lesson.
- Kernel teaches Ker(T)=Null(T), how to solve it, a kernel-basis example/practice, and nullity. MatrixRankNullity includes explicit two-parameter null-space decomposition. Defer the three separate null-space/basis/nullity lessons.
- Matrix RankNullity explicitly supplies matrix IMT implications in its worked conceptual example. Transformation IMT restates the equivalent image/kernel conditions. Accept the extra transfer rather than spending three slots on intermediate theorem lessons.
- BasisSpan already teaches expressing a vector as a combination of basis vectors. Guide4 needs existence of a basis expansion, not the full ordered-coordinate computational skill; defer Coordinates.
- IntroLinearTransform and StandardMatrix are already studied. Multiplication and inverse-product order were correct in E2 Q1–2. Defer full composition/inversion lessons and their shear/stretch chain.

## Original problems remain necessary

After the first six lessons, work guide2–4 completely without the answer reveal. They require writing proofs/counterexamples, which the lesson banks do not fully test. Reserve that attempt before spending the last slot on rotations.

Also recheck the WHW5 row-space/column-space task: original pivot columns give a column basis, while nonzero echelon rows give a row basis. The retained MA lessons do not explicitly teach the latter rule. Revisit E1 Q3/Q5 and E2 Q5/Q8 as short existing-problem checks, not partial lesson assignments.

## Residual risk

This plan leaves dedicated reflection/composition practice, some determinant-law proofs and row-operation determinant bookkeeping, and a full proof of general-domain rank-nullity less prepared. It does not claim that those sections cannot appear. The two previous exams support retaining some breadth; they do not establish E3 point weights or which exact questions will repeat. No complete W5D1–W6D3 activity packet was available in the earlier audit.

Sources: original guide and homework captures in this directory; actual exam/response imports at `/home/jake/Developer/study/vault/F26/source/341/E-1/canvas-submission.json` and the corresponding `E-2` file.
