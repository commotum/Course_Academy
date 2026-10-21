# Moderate templates

Source basis 2348, matching classification.md. Preserve one selection field, five matrix choices, one concrete solution per instance, delimiter-free answer values, and source-owned choice patterns. All moderate questions use two linear equations in three variables. No equation solving or row reduction is added. Variables and their order are fixed because column-order distractors refer to these precise supplied roles. Number signs and missing-variable patterns remain fixed to the observed domains; this is a conservative sampling policy, not a claim that other signs are impossible.

## Coefficient profile q-1070

Original: 2 x₂ + 4 x₁ = 3 x₃; -11 x₃ = 12. Request the coefficient matrix, not the augmented matrix. Parameters (a,b,c,d,e)=(4,2,3,-11,12). General supplied equations: b x₂+a x₁=c x₃ and d x₃=e. Ordered variables x₁,x₂,x₃. Correct coefficient matrix [[a,b,-c],[0,0,d]]. RHS [0,e]. Preserve rearrangement, explicit zero coefficients, then reading coefficients; no augmentation solution stage.

Slots: a,b,c positive integers 1..15, d negative integer -15..-1, e positive integer 1..15. Normal sampling uses magnitudes 2..15 for nontrivial coefficients, and 1..15 for e. Reject a=b since appearance-order distractors would merge. Original parameters retained for replay. Every slot affects prompt, organized system, answers and intermediate values together.

| Source option value at original parameters | Complete parameter recipe |
|---|---|
| [[4,2,-3],[0,0,-11]] (correct) | [[a,b,-c],[0,0,d]] |
| [[4,2,-3,0],[0,0,-11,12]] | Append RHS to coefficient matrix |
| [[2,4,3,0],[0,0,-11,12]] | Swap a,b, retain RHS coefficient sign, append RHS |
| [[4,2,3],[0,0,-11]] | Retain RHS variable sign |
| [[2,4,3],[0,0,-11]] | Swap a,b and retain RHS variable sign |

## Augmented profile q-1073

Original: a-c=4b; 3c-11a=-1. Parameters (k,l,m,r)=(4,11,3,-1). General supplied equations a-c=kb; mc-la=r. Ordered variables a,b,c. Correct matrix [[1,-k,-1,0],[-l,0,m,r]]. Preserve rearrangement with missing b in the second equation, read coefficient matrix, then append RHS. The unit coefficients of a,c in the first equation are fixed to preserve source form and workload; k,l,m,r vary.

Slots: k,l,m positive integers 2..15; r negative integer -15..-1. Dependent references, matrices, constants and solution grammar derive from the same parameter object. No resampling in solutions or answer rendering.

| Source option at original parameters | Complete parameter recipe |
|---|---|
| [[1,-4,-1,0],[-11,0,3,-1]] (correct) | [[1,-k,-1,0],[-l,0,m,r]] |
| [[1,0,-1,4],[-11,0,3,-1]] | Treat b coefficient as first-row constant: [[1,0,-1,k],[-l,0,m,r]] |
| [[1,-1,4],[3,-11,-1]] | Omit b column and retain second-row appearance order: [[1,-1,k],[m,-l,r]] |
| [[1,-4,-1,0],[-11,0,3,1]] | Reverse second RHS: [[1,-k,-1,0],[-l,0,m,-r]] |
| [[1,-1,0,4],[-3,-11,0,-1]] | Appearance-order/misplacement and second-row c sign: [[1,-1,0,k],[-m,-l,0,r]] |

The compound last recipe is retained exactly as an observed transformation; its psychological cause is unresolved. No inferred feedback is shown to learners. Each profile is selected whole before constructing its bank. Matrices require exact entrywise equality, not equivalence by row operations. Fidelity compares all five complete values and correct designation independently of ordering and LaTeX wrapper differences. Worked-solution operative sentences and ordered stages are retained, with whitespace and explicit unit coefficients normalized. No mathematical operation, response shape or target type is added.

Declared variation is numeric only. Validators change every slot with other data fixed, exercise boundaries, and parse the rendered prompt, organized equations and solution matrices independently. Distinctness normalizes coefficient rows for coefficient tasks (excluding the irrelevant RHS), and full augmented rows for augmented tasks, by their first nonzero coefficient to reject common scaling aliases, ignores choice order/seed/identity, and retains the requested matrix kind. Fixed variable order, missing-variable positions, equation order and target type are checked on every record. Review.md contains original/replay and two changed-number examples per template.
