# Independent source-first review account

Saved before inspecting repaired generator code or generated outputs. Evidence is the Math Academy imported questions (17 for KP 17592186119924; 14 for KP 17592186119925) and canonical examples e-10907 and e-10908 in `../../2026-11-10-linear-dependence-checkboxes/topic-before.json`, together with the response contract supplied in the review task. No generated question is used as instructional evidence.

## Response contract

Each displayed mathematical statement is a separate checkbox whose key contains its complete statement. The learner selects every true statement. There is no additional “None of the above” checkbox. An empty selected subset is a valid response and must be submitted as explicit false answers for every actual statement field; absence of submission is a different state. This contract supersedes the legacy imported None fields and radio combination menus.

## KP 17592186119924: evaluate a proposed relation and interpret independence

The student receives two or three vectors in R^3 and three propositions: a particular numerical linear combination equals zero, the homogeneous vector equation has only the all-zero coefficient solution, and the set is either dependent or independent. The operations are (1) multiply and add vectors component by component to check the proposed relation, (2) translate the homogeneous vector equation to a coordinate system or use a demonstrated nontrivial relation, and (3) apply the definition of linear independence. A failed proposed relation alone does not prove independence.

The canonical example e-10907 computes a nonzero residual for a proposed relation, then solves the sparse coordinate equations by back substitution and selects the uniqueness and independence propositions. q-156591 verifies a zero residual and uses its nonzero coefficient triple (1,1,-2) to disprove uniqueness. q-157254 is an essential counterexample to treating a failed candidate relation as proof of independence: its proposed relation is false, but a_2=-2a_1, so only the dependence proposition is true.

Correctness can be checked independently with A formed from the displayed vectors as columns. For the displayed coefficient vector c, the relation statement is true exactly when Ac=0. The uniqueness statement is true exactly when rank(A) equals its column count. An independence proposition has the same truth value as uniqueness; a dependence proposition has its negation. A nonzero c with Ac=0 is sufficient evidence of dependence. The all-zero coefficient tuple cannot serve as that evidence.

The question family must preserve these cases:

- Independent vectors: candidate nontrivial relation false, uniqueness true, classification true or false according to whether it says independent or dependent.
- Dependent vectors with a correct candidate relation: relation true, uniqueness false; classification follows its wording.
- Dependent vectors with an incorrect candidate relation: relation false and uniqueness false; dependence remains true if offered. If the classification instead says independent, all three propositions are false, so the correct selected subset is empty. This is mathematically legitimate even though the sampled imported items do not demonstrate this particular all-false arrangement.
- Changing the order or wording of propositions must not change their underlying truth conditions. A false component or residual must not be rounded into zero.

Source difficulty distinctions are substantive. Easy imported items use two vectors in R^3, including scalar-multiple dependence (q-157255, q-157256) and sparse independent pairs (q-155967). Moderate items use three dependent vectors with the displayed nontrivial relation providing a direct dependence witness (q-156591, q-157236, q-157238, q-157252). Hard items use three independent vectors whose sparse coordinate equations can be reordered and solved by back substitution (e-10907, q-155965, q-157225, q-157227). Difficulty must therefore reflect the intended reasoning and structure, not merely a label or larger random integers.

## KP 17592186119925: eliminate a homogeneous system and interpret its solution space

The student receives three vectors in R^3 and propositions about dependence, independence, and either uniqueness of the trivial solution or infinitely many nonzero solutions. Unlike the previous KP's explicit proposed relation, the instructional work is to construct the homogeneous augmented matrix, perform Gaussian elimination, identify pivots/free variables, and connect the result to the propositions. The canonical example e-10908 exhibits two row operations, a zero last row, two basic variables, and one free variable; it concludes infinitely many nonzero solutions and dependence.

For real coefficients, let n=3. Full column rank means only the trivial solution, independence, and no nonzero solutions. Rank less than n means at least one free variable, dependence, and infinitely many nonzero solutions. “Nonzero solution” means a coefficient tuple that is not identically zero, not a tuple with every coordinate nonzero. Homogeneous systems always possess the trivial solution, so they are never inconsistent. Dependence and independence are complementary; an offered pair guarantees at least one selected statement. An empty selection is still a supported response state, but it is not expected for this source family's usual three propositions containing both complementary classification statements. The generator should not invent an all-false key for such a proposition set.

The source's moderate imported items are dependent rank-two systems with one free variable after elimination (q-34153, q-105308, q-34711). Hard imported items have a nonzero final pivot and require back substitution to establish all three coefficients vanish (q-105315, q-105317, q-75660). There are no imported easy items for this KP in the evidence. Any easy branch needs an explicit defensible simplification rather than an unsupported claim that it reproduces a demonstrated source difficulty.

## Requirements for the next review stage

For each repaired package, check mathematics against displayed data independently of generator flags; require complete, unique statement keys with boolean true/false choices, no Roman-numeral surrogate fields and no separate None field. Check that every worked solution proves the displayed claims, including a valid nontrivial witness or intelligible elimination/back-substitution evidence. Check family/difficulty coverage and prove the all-false first-KP case remains possible and explicitly graded. Preserve the second KP's Gaussian-elimination instructional operation rather than replacing its solution entirely with a determinant or an unexplained rank claim.
