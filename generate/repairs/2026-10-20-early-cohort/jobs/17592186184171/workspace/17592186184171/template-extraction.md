# Template extraction and source fidelity

Source basis: 2516. All values and complete field/answer records remain in `reference/source.json`. Source-specific parameter values are reproduced in the generator's `ORIGINAL` map and in `source-choice-mapping.json`; the validator independently reconstructs them from the displayed source rather than trusting that map.

## Easy: column-space basis to nullity

Fixed backbone: real m by n matrix A; explicit list B of k basis vectors for Col(A); request dim(Null(A)); one five-choice radio field. No matrix entries are supplied. The learner uses the number of basis vectors as rank and subtracts it from the number of columns. Changing the matrix label, basis symbol or row count alone cannot produce fresh assessed work.

| Source | m | n | k | Answer n-k | Complete bank profile |
| --- | --- | --- | --- | --- | --- |
| q-35305 | 3 | 5 | 3 | 2 | small |
| q-35433 | 3 | 6 | 3 | 3 | small |
| q-141230 | 5 | 7 | 4 | 3 | small |
| q-142487 | 6 | 8 | 5 | 3 | offset-minus1 |
| q-142485 | 4 | 5 | 2 | 3 | offset-minus2 |
| q-141232 | 6 | 10 | 4 | 6 | dimensions |

Ordered solution stages and wording follow the source: state rank-nullity with n columns; read n and the number of vectors in B; identify rank k; substitute k+nullity=n; isolate nullity=n-k; conclude dim(Null(A))=n-k. All numerical tokens, the explicit basis list and the final equation derive from the same m,n,k record.

Conservative sampling extension: integer m in 2..7, n in 4..12 and 1<=k<=min(m,n-1). These are sampling limits, not observed bounds (observed m=3..6, n=5..10, k=2..5). k<=m ensures such a matrix can exist, and k<n avoids a new zero-nullity edge workload. Positive ranks and explicit basis lists retain the source method. m is a supplied context slot, n and k determine the assessed task; the mathematical distinctness key is (n,k).

Let r=n-k. Complete profiles, preserving five choices:

- small: [0,1,2,3,4], eligible only when r occurs.
- offset-minus1: [r-1,r,r+1,r+2,r+3], all nonnegative.
- offset-minus2: [r-2,r,r+1,r+2,r+3], all nonnegative.
- dimensions: [0,n-2k,k,n-k,n], only when all five are distinct and nonnegative.

The first three are observed numeric patterns; the source does not identify the cognitive error behind each offset, so their interpretations remain unresolved. The dimension profile uses 0, n-2k, k, n-k and n; these formulas reproduce the complete original bank at n=10,k=4. Their error interpretations are also not presented to learners. Sparse source evidence limits distractor inference; no new feedback is added. Every incorrect source choice is accounted for by its exact recipe index in `source-choice-mapping.json`.

## Moderate: parametrized null space to rank

Fixed backbone: Null(A) is an explicitly supplied four-component homogeneous linear vector in either two independent real parameters x2,x3 or three independent real parameters x1,x2,x3; request rank(A). The vector has coefficient matrix C with full column rank. Counting parameters is justified only because the coefficient vectors are independent; the validator verifies this exactly. n=4 remains fixed to retain the source dimension and workload. Parameter-vector dependence, nonlinear entries, extra parameters and changed requested invariants are outside this package.

| Source | Coefficient matrix C (rows) | Parameters | Profile | Prompt layout |
| --- | --- | --- | --- | --- |
| q-35306 | (2,0); (1,0); (0,1); (1,1) | x2,x3 | one-through5 | Inline |
| q-142486 | (1,0,0); (-1,1,0); (0,0,1); (1,0,-1) | x1,x2,x3 | zero-through4 | Inline |
| q-35434 | (1,2,0); (0,1,-1); (-3,0,1); (1,1,1) | x1,x2,x3 | one-through5 | Display |
| q-79352 | (1,0,0); (0,1,0); (0,0,1); (0,0,0) | x1,x2,x3 | zero-through4 | Inline |
| q-139982 | (1,0,0); (0,-1,0); (0,1,1); (0,1,0) | x1,x2,x3 | zero-through4 | Inline |

Ordered solution stages and shared wording: state rank-nullity; infer n from the four vector components; rewrite the given vector as a sum of parameters times coefficient vectors; conclude nullity equals the number of independent coefficient vectors; substitute rank+k=4; isolate rank=4-k and evaluate. The concrete vector decomposition, all variable references and numerical conclusions derive from the same C and parameter index list. The worked solution is independent of the learner's selected choice.

Conservative generalization: each coefficient may range over integers -3..3, including zeros and both signs, with exact full-column-rank rejection sampling. This includes all observed coefficients. Each coefficient is an explicit variable slot; changing it updates the vector and its expansion together. Both parameter-count patterns and both prompt layouts are exercised. The requested rank and the ambient dimension are fixed because changing them changes the question's supplied/requested roles or workload.

The two complete banks are zero-through4=[0,1,2,3,4] and one-through5=[1,2,3,4,5]. These are observed consecutive integer profiles; values above the ambient dimension are preserved source distractors. No unsupported error labels or learner-facing feedback are invented. Every bank reproduces all original options and the correct designation, ignoring order.

Distinctness identifies the rational column space of C using RREF(C transpose), so scaling, permuting or recombining the parameter vectors cannot inflate the number of assessed null spaces. Merely changing bank profile or inline/display layout cannot create a fresh task.

## Formatting and validation

Generated set braces are visible, vectors use the shared `matrix_tex` bmatrix helper, and bare answers use `normalize_tex`. Prompt and solution use `normalize_prose` before content UUID calculation; the public `generate` API is decorated with `checked_math_content`. Stable question identity includes the whole authored bank, but replenishment also compares mathematical tasks before insertion. Field and answer UUIDs are owned by the generated question/field.

`validate.py` compares source prose and ordered stages after explicit presentation normalization, independently parses prompt expressions and every solution coefficient vector, compares all 55 source choices and all 44 distractors, tests deterministic replay and complete-profile sampling, exhausts easy parameter/profile boundaries and changes each moderate coefficient while holding the rest fixed. A deliberately stale solution vector must fail. Native `learning::grade_field` checks acceptance of the correct option and rejection of every distractor. `side-by-side.md` shows source, replay and varied instances for both levels and the display family.

No plots or assets are needed. No source IDs are imported into generated content. `capabilities.json` records unsupported hard and the bounded sampler policy. Finite limits are not used to disguise an unsupported level as filled.

The application starts registered generators with system Python. The generator CLI forwards to the existing project `.venv/bin/python` when SymPy is absent, preserving all CLI arguments. Both supported levels were executed with `/usr/bin/python3`; see `registered-cli-validation.json`. This launcher adjustment followed initial registration, preserved the UUID/path and question semantics, and was revalidated without altering the retained original registration request.
