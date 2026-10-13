# Template extraction

## 1. Describe each observed question

The table below records original numerical matrices, exact arithmetic, signed/zero coefficients, number of equations/variables, and observed operation chains before generalization. Every source is moderate. Integers predominate; q-74643 has a half coefficient, and q-74635/q-74634 generate short rational elimination stages. q-74637 uses a row swap and seventh-denominator back-substitution. q-131722/q-131720 normalize the first row.


### q-32242

Original augmented matrix: `[[-1, 2, 6], [2, -3, 13], [5, -1, 45]]`. Operations in printed order: `[["add", 1, 0, 2], ["add", 2, 0, 5], ["add", 2, 1, -9]]`. Inconsistent: preserve the final zero-left/nonzero-right equation and implication.


### q-42061

Original augmented matrix: `[[1, -3, 1, 0], [-4, 6, 0, 2]]`. Operations in printed order: `[["add", 1, 0, 4]]`. Dependent: preserve basic/free-variable discussion, without adding a full general-solution task.


### q-131719

Original augmented matrix: `[[1, 4, -1], [2, 8, -2], [-3, -12, 3]]`. Operations in printed order: `[["add", 1, 0, -2], ["add", 2, 0, 3]]`. Dependent: preserve basic/free-variable discussion, without adding a full general-solution task.


### q-131723

Original augmented matrix: `[[1, -1, 1, 3], [-3, 3, -3, 10]]`. Operations in printed order: `[["add", 1, 0, 3]]`. Inconsistent: preserve the final zero-left/nonzero-right equation and implication.


### q-131724

Original augmented matrix: `[[1, -2, 2], [-3, -4, 3], [2, -4, -1]]`. Operations in printed order: `[["add", 1, 0, 3], ["add", 2, 0, -2]]`. Inconsistent: preserve the final zero-left/nonzero-right equation and implication.


### q-74635

Original augmented matrix: `[[-2, 4, 3, 0], [1, 3, 0, 2]]`. Operations in printed order: `[["add", 1, 0, "1/2"]]`. Dependent: preserve basic/free-variable discussion, without adding a full general-solution task.


### q-74637

Original augmented matrix: `[[2, 3, -1], [1, -2, 1], [-1, -5, 2]]`. Operations in printed order: `[["swap", 0, 1], ["add", 1, 0, -2], ["add", 2, 0, 1], ["add", 2, 1, 1]]`. Unique: preserve removal of the zero row and the precise corresponding-system/substitution steps.


### q-131718

Original augmented matrix: `[[1, -3, 1, 2], [-2, 7, 2, -1]]`. Operations in printed order: `[["add", 1, 0, 2]]`. Dependent: preserve basic/free-variable discussion, without adding a full general-solution task.


### q-74643

Original augmented matrix: `[[3, 2, 8], [1, 1, -2], [1, 1/2, 5]]`. Operations in printed order: `[["swap", 0, 1], ["add", 1, 0, -3], ["add", 2, 0, -1], ["add", 2, 1, "-1/2"]]`. Unique: preserve removal of the zero row and the precise corresponding-system/substitution steps.


### q-131720

Original augmented matrix: `[[2, -6, -2, 4], [3, -9, -3, 6]]`. Operations in printed order: `[["scale", 0, "1/2"], ["add", 1, 0, -3]]`. Dependent: preserve basic/free-variable discussion, without adding a full general-solution task.


### q-131721

Original augmented matrix: `[[1, 2, -1], [3, 7, 1], [-2, -4, 2]]`. Operations in printed order: `[["add", 1, 0, -3], ["add", 2, 0, 2]]`. Unique: preserve removal of the zero row and the precise corresponding-system/substitution steps.


### q-131722

Original augmented matrix: `[[3, -3, 6], [-2, 1, -3], [4, -4, 8]]`. Operations in printed order: `[["scale", 0, "1/3"], ["add", 1, 0, 2], ["add", 2, 0, -4], ["scale", 1, -1]]`. Unique: preserve removal of the zero row and the precise corresponding-system/substitution steps.


### q-42020

Original augmented matrix: `[[1, 2, -1], [3, 1, 3], [-2, 1, -2]]`. Operations in printed order: `[["add", 1, 0, -3], ["add", 2, 0, 2], ["add", 2, 1, 1]]`. Inconsistent: preserve the final zero-left/nonzero-right equation and implication.


### q-74634

Original augmented matrix: `[[2, -1, -1], [2, -4, 3], [1, 1, 2]]`. Operations in printed order: `[["add", 1, 0, -1], ["add", 2, 0, "-1/2"], ["add", 2, 1, "1/2"]]`. Inconsistent: preserve the final zero-left/nonzero-right equation and implication.


## 2. Generalized shared mathematical pattern

Fourteen per-source replay aliases/masks map to thirteen observed families (`families.json`). The q-74637/q-74643 aliases share one family; their different coefficient forms and source prose whitespace are conditional presentation components, and their two full banks remain separate profiles. The other twelve families retain distinct layouts, dimensions, fixed prose or ordered stage sequences. This family count does not infer distinct skills from changed numbers.

Classify the *printed* real linear system by Gaussian elimination. A contradiction means inconsistent; otherwise a pivot for each variable means consistent independent, while a free variable means consistent dependent. The response identifies the unique true statement among the three displayed statements, preserving the complete source subset-choice bank. This does not assess choosing a parameter for consistency, vector solution form, or null spaces.

## 3. Components and every source choice

`templates.json` records complete-component masks for all source prompts/solutions, every original math component, every ordered operation, all five bank values, and the original correct value. Masks cover whole equations, matrices and math regions; numerical tokens are never globally replaced in prose. Row operation indexes are zero-based in author metadata. The following mapping accounts for every original option one-to-one; “None” denotes the empty statement subset, singleton options the indicated proposition, and pair options the conjunction/exact selected subset. Wrong subsets remain categorically false because the three statements are mutually exclusive. This is a defensible semantic recipe; no numerical distractor error is inferred.


### q-32242 — bank-0a7d92f7

| Field | Original exact value | Recipe | Source designation |
|---|---|---|---|
| selection / radio | I and III only | exact statement subset ['I', 'III'] | incorrect |
| selection / radio | III only | exact statement subset ['III'] | incorrect |
| selection / radio | None | exact statement subset [] | incorrect |
| selection / radio | II only | exact statement subset ['II'] | correct |
| selection / radio | I only | exact statement subset ['I'] | incorrect |

### q-42061 — bank-a2a138a0

| Field | Original exact value | Recipe | Source designation |
|---|---|---|---|
| selection / radio | II only | exact statement subset ['II'] | incorrect |
| selection / radio | I and II only | exact statement subset ['I', 'II'] | incorrect |
| selection / radio | None | exact statement subset [] | incorrect |
| selection / radio | I only | exact statement subset ['I'] | correct |
| selection / radio | III only | exact statement subset ['III'] | incorrect |

### q-131719 — bank-e97c8f76

| Field | Original exact value | Recipe | Source designation |
|---|---|---|---|
| selection / radio | II only | exact statement subset ['II'] | correct |
| selection / radio | I only | exact statement subset ['I'] | incorrect |
| selection / radio | II and III only | exact statement subset ['II', 'III'] | incorrect |
| selection / radio | III only | exact statement subset ['III'] | incorrect |
| selection / radio | None | exact statement subset [] | incorrect |

### q-131723 — bank-e97c8f76

| Field | Original exact value | Recipe | Source designation |
|---|---|---|---|
| selection / radio | None | exact statement subset [] | incorrect |
| selection / radio | II and III only | exact statement subset ['II', 'III'] | incorrect |
| selection / radio | I only | exact statement subset ['I'] | correct |
| selection / radio | III only | exact statement subset ['III'] | incorrect |
| selection / radio | II only | exact statement subset ['II'] | incorrect |

### q-131724 — bank-a2a138a0

| Field | Original exact value | Recipe | Source designation |
|---|---|---|---|
| selection / radio | I and II only | exact statement subset ['I', 'II'] | incorrect |
| selection / radio | II only | exact statement subset ['II'] | incorrect |
| selection / radio | III only | exact statement subset ['III'] | correct |
| selection / radio | None | exact statement subset [] | incorrect |
| selection / radio | I only | exact statement subset ['I'] | incorrect |

### q-74635 — bank-06fb682b

| Field | Original exact value | Recipe | Source designation |
|---|---|---|---|
| selection / radio | II only | exact statement subset ['II'] | incorrect |
| selection / radio | I and III only | exact statement subset ['I', 'III'] | incorrect |
| selection / radio | III only | exact statement subset ['III'] | correct |
| selection / radio | I and II only | exact statement subset ['I', 'II'] | incorrect |
| selection / radio | I only | exact statement subset ['I'] | incorrect |

### q-74637 — bank-06fb682b

| Field | Original exact value | Recipe | Source designation |
|---|---|---|---|
| selection / radio | I only | exact statement subset ['I'] | incorrect |
| selection / radio | II only | exact statement subset ['II'] | correct |
| selection / radio | I and III only | exact statement subset ['I', 'III'] | incorrect |
| selection / radio | I and II only | exact statement subset ['I', 'II'] | incorrect |
| selection / radio | III only | exact statement subset ['III'] | incorrect |

### q-131718 — bank-a2a138a0

| Field | Original exact value | Recipe | Source designation |
|---|---|---|---|
| selection / radio | I only | exact statement subset ['I'] | correct |
| selection / radio | III only | exact statement subset ['III'] | incorrect |
| selection / radio | None | exact statement subset [] | incorrect |
| selection / radio | I and II only | exact statement subset ['I', 'II'] | incorrect |
| selection / radio | II only | exact statement subset ['II'] | incorrect |

### q-74643 — bank-321622ff

| Field | Original exact value | Recipe | Source designation |
|---|---|---|---|
| selection / radio | II and III only | exact statement subset ['II', 'III'] | incorrect |
| selection / radio | I and III only | exact statement subset ['I', 'III'] | incorrect |
| selection / radio | I only | exact statement subset ['I'] | incorrect |
| selection / radio | III only | exact statement subset ['III'] | incorrect |
| selection / radio | II only | exact statement subset ['II'] | correct |

### q-131720 — bank-e97c8f76

| Field | Original exact value | Recipe | Source designation |
|---|---|---|---|
| selection / radio | II and III only | exact statement subset ['II', 'III'] | incorrect |
| selection / radio | I only | exact statement subset ['I'] | incorrect |
| selection / radio | III only | exact statement subset ['III'] | correct |
| selection / radio | None | exact statement subset [] | incorrect |
| selection / radio | II only | exact statement subset ['II'] | incorrect |

### q-131721 — bank-e97c8f76

| Field | Original exact value | Recipe | Source designation |
|---|---|---|---|
| selection / radio | II and III only | exact statement subset ['II', 'III'] | incorrect |
| selection / radio | I only | exact statement subset ['I'] | correct |
| selection / radio | III only | exact statement subset ['III'] | incorrect |
| selection / radio | None | exact statement subset [] | incorrect |
| selection / radio | II only | exact statement subset ['II'] | incorrect |

### q-131722 — bank-a2a138a0

| Field | Original exact value | Recipe | Source designation |
|---|---|---|---|
| selection / radio | I only | exact statement subset ['I'] | incorrect |
| selection / radio | III only | exact statement subset ['III'] | incorrect |
| selection / radio | None | exact statement subset [] | incorrect |
| selection / radio | I and II only | exact statement subset ['I', 'II'] | incorrect |
| selection / radio | II only | exact statement subset ['II'] | correct |

### q-42020 — bank-3c9aea05

| Field | Original exact value | Recipe | Source designation |
|---|---|---|---|
| selection / radio | II and III only | exact statement subset ['II', 'III'] | incorrect |
| selection / radio | I only | exact statement subset ['I'] | incorrect |
| selection / radio | III only | exact statement subset ['III'] | correct |
| selection / radio | I and II only | exact statement subset ['I', 'II'] | incorrect |
| selection / radio | II only | exact statement subset ['II'] | incorrect |

### q-74634 — bank-3c9aea05

| Field | Original exact value | Recipe | Source designation |
|---|---|---|---|
| selection / radio | II and III only | exact statement subset ['II', 'III'] | incorrect |
| selection / radio | I only | exact statement subset ['I'] | incorrect |
| selection / radio | III only | exact statement subset ['III'] | correct |
| selection / radio | I and II only | exact statement subset ['I', 'II'] | incorrect |
| selection / radio | II only | exact statement subset ['II'] | incorrect |

## 4. Reusable template and constraints

For each observed template let the original augmented matrix be [A|b]. Parameters are nonzero coordinate scales s_i∈{−2,−1,1,2} and translations t_i∈{−2,−1,0,1,2}. Generate [A diag(s)|b−At]. This represents substituting old coordinates u_i=s_i x_i+t_i, an invertible affine change, preserving ranks, pivot/free-variable positions, solution category, and the original elimination workload. Execute the original whole ordered row-operation chain on this matrix, emitting every computed stage. Corresponding system rows and isolated variable values use the resulting printed matrix; unique solutions are derived exactly. Back-substitution expressions preserve distinct substitution and isolated-answer stages. Identity replay s_i=1,t_i=0 is the ordinary recipe, not a literal-source-return mode.

The source-specific fixed prose and component wrappers remain fixed. Systems escape a malformed bare opening brace (supported presentation repair). q-32242 removes an unstated R1 sign flip in the final matrix; the printed R3 operation cannot change R1. The original −150 contradiction and classification were already correct. All raw evidence is retained in `source.json` and `source-errors.json`. Full normalized source prose/stage comparisons separate 13 exact solutions from one supported mathematical repair.

Source profiles preserve each complete five-option bank. The interface permits any of the six complete observed profiles on any layout; all contain the three singleton options, so the unique correct answer exists. Options have stable owned UUIDs and are shuffled deterministically. Every wrong choice is checked as a complete statement subset; pairs/None are not silently dropped. There are no invented option explanations.

### Authored easy scope

The canonical e-6173 already classifies a 2×2 dependent system in one elimination. The prerequisite “Systems of Equations With No Solutions and Infinitely Many Solutions” supplies the geometric/categorical distinction. Easy therefore authors 2×2 systems requiring exactly one nonzero row elimination, all three categories, integer coefficients with magnitude ≤16 and integral/half-integral stages. This is a difficulty design claim, not an observed label. The single task stays classification; solving explicit variables is not an extra assessment.

### Authored hard scope

The owning topic is Gaussian Elimination For NxM Systems of Equations. The actual lesson route follows first-step→next: Introduction → solving consistent NxM systems → category definitions → this KP → constant-for-consistency sibling. The Introduction uses three variables, pivots/free variables, and Gaussian/Gauss-Jordan row operations; the earlier sibling demonstrates them, so a 3×3 classification does not enter the constant-parameter sibling or later null-space topics. Hard authors 3×3 systems requiring exactly three nonzero elimination operations; rank two yields a free variable or contradiction, rank three yields uniqueness. Integer coefficients have magnitude ≤40, and every exact intermediate denominator is ≤6. These are parallel classification variations at one workload, not a progression. No determinant, symbolic parameter, general vector form, or newly taught method is introduced.

### Meaningful variety and identity

Coordinate scaling changes variable coefficient ratios; translation changes RHS and back-substitution arithmetic. They affect the assessed elimination, not only decorative names. Authored systems construct a triangular rank pattern and reverse elementary row additions, varying actual coefficients/constants/category/statement order. All parameters are checked on explicit inputs as well as sampled inputs. Canonical mathematical fingerprints sort complete printed equations after dividing each row by its first nonzero component, preserving variable roles and ignoring row order, scalar-equivalent equations, profiles and banks. Arbitrary row combinations are *not* collapsed to solution-set identity because they change the assessed elimination arithmetic. Content UUIDs include version, mathematical fingerprint, full displayed prompt, one fixed solution and entire bank; seed/order and parameter spelling cannot change identity.

