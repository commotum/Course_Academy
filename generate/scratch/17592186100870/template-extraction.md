# Matrix product dimensions

Source basis 2636; KP 17592186100870. See source.json for the complete frozen record.

The core move is to follow the requested multiplication order, verify matching inner dimensions, then report the outer dimensions in order. All observed rated sources have conformable products. No undefined-product variants are introduced.

## Backbones and fields

| Family | Sources | Fields |
|---|---|---|
| easy-blank | q-320315 | field-1 rows and field-2 columns, separate math blanks |
| easy-radio | q-77473, q-129480, q-70703 | selection, five-option radio; four dimension pairs and one undefined choice |
| moderate-blank | q-320344 | field-1 rows and field-2 columns, separate math blanks |
| moderate-radio | q-129461, q-129486, q-70702, q-70705 | selection, five-option radio; four dimension pairs and one undefined choice |

Easy prompts request the factors in the order they are supplied. Moderate prompts request the reverse order, requiring the learner to track the requested product. The radio prompts differ between easy and moderate. Blank prompts supply a times sign between two answer fields. Preserve each source prompt, field keys, exact whitespace, and step sequence. Profiles within a family keep their complete observed banks; they are not mixed.

## Slots and bounds

Let the requested ordered factors be m by n and n by p. Independently vary m,n,p through integers 1..10, pairwise distinct. This is a conservative same-method generalization of observed positive dimensions, including dimension 1 and 10. Distinctness preserves unambiguous five-choice banks. Values outside this bounded policy are not claimed. All occurrences in the supplied dimensions, requested result, bank, prose, and shape chain change simultaneously. Matrix labels remain fixed per profile as notation; label variation alone contributes no distinct task.

The q-129461 profile retains its unexplained fixed distractor constant 5 in m by 5; p=5 is excluded to prevent a duplicate correct answer. The q-70702 profile retains fixed constant 3 in n by 3; m=3 is excluded. These literal patterns replay the complete observed values; their misconception meanings are unresolved. Do not invent explanations or silently replace them. Other bank components are dimension-role recipes recorded below.

## Solution and plots

Compute the ordered matrix-product shape exactly with SymPy. Render the source stages: count columns of the first requested matrix, count rows of the second, state conformability, report m by p, and display the boxed equal inner dimensions with the outer dimensions. q-70702 requires the documented factor-label correction from R,S to S,R. No plots or assets are needed; all source displays are standalone math. Stages 5 and 7 therefore have no asset work.

## Source profiles and exact component mappings

### q-129461

Suppose $A$ is a $4\times 6$ matrix and $B$ is a  $2\times 4$ matrix. What are the dimensions of $BA?$

Observed m,n,p: {"m": 2, "n": 4, "p": 6}

| Field | Exact source value | Parameter recipe | Key |
|---|---|---|---|
| selection | `6\times 2` | `p\times m` | False |
| selection | `2\times 5` | `m\times 5` | False |
| selection | `The product is undefined` | `The product is undefined` | False |
| selection | `4\times 2` | `n\times m` | False |
| selection | `2\times 6` | `m\times p` | True |
### q-129486

Suppose $A$ is a $8\times 7$ matrix and $B$ is a  $2\times 8$ matrix. What are the dimensions of $BA?$

Observed m,n,p: {"m": 2, "n": 8, "p": 7}

| Field | Exact source value | Parameter recipe | Key |
|---|---|---|---|
| selection | `2\times 7` | `m\times p` | True |
| selection | `2\times 8` | `m\times n` | False |
| selection | `The product is undefined` | `The product is undefined` | False |
| selection | `8\times 7` | `n\times p` | False |
| selection | `7\times 2` | `p\times m` | False |
### q-320315

If $P$ is a $4\times 3$ matrix and $Q$ is a $3\times 7$ matrix, then the dimensions of $PQ$ are{{field-1}}$\times $
{{field-2}}.

Observed m,n,p: {"m": 4, "n": 3, "p": 7}

| Field | Exact source value | Parameter recipe | Key |
|---|---|---|---|
| field-2 | `7` | `p` | True |
| field-1 | `4` | `m` | True |
### q-320344

If $X$ is a $5\times 7$ matrix and $Y$ is a $10\times 5$ matrix, then the dimensions of $YX$ are{{field-1}}$\times $
{{field-2}}.

Observed m,n,p: {"m": 10, "n": 5, "p": 7}

| Field | Exact source value | Parameter recipe | Key |
|---|---|---|---|
| field-1 | `10` | `m` | True |
| field-2 | `7` | `p` | True |
### q-70702

Suppose $R$ is a $4\times 5$ matrix and $S$ is a  $2\times 4$ matrix. What are the dimensions of $SR?$

Observed m,n,p: {"m": 2, "n": 4, "p": 5}

| Field | Exact source value | Parameter recipe | Key |
|---|---|---|---|
| selection | `4\times 3` | `n\times 3` | False |
| selection | `3\times 5` | `3\times p` | False |
| selection | `2\times 5` | `m\times p` | True |
| selection | `5\times 2` | `p\times m` | False |
| selection | `The product is undefined` | `The product is undefined` | False |
### q-70705

Suppose $U$ is a $2\times 3$ matrix and $V$ is a $5\times 2$ matrix. What are the dimensions of $VU?$

Observed m,n,p: {"m": 5, "n": 2, "p": 3}

| Field | Exact source value | Parameter recipe | Key |
|---|---|---|---|
| selection | `5\times 5` | `m\times m` | False |
| selection | `2\times 2` | `n\times n` | False |
| selection | `3\times 5` | `p\times m` | False |
| selection | `5\times 3` | `m\times p` | True |
| selection | `The product is undefined` | `The product is undefined` | False |
### q-77473

What are the dimensions of $HK$, if $H$ is a $3\times 7$ matrix and $K$ is a $7\times 5$ matrix?

Observed m,n,p: {"m": 3, "n": 7, "p": 5}

| Field | Exact source value | Parameter recipe | Key |
|---|---|---|---|
| selection | `3\times 5` | `m\times p` | True |
| selection | `5\times 5` | `p\times p` | False |
| selection | `The product is undefined` | `The product is undefined` | False |
| selection | `3\times 3` | `m\times m` | False |
| selection | `5\times 3` | `p\times m` | False |
### q-129480

What are the dimensions of $CD$, if $C$ is a $5\times 7$ matrix and $D$ is a $7\times 1$ matrix?

Observed m,n,p: {"m": 5, "n": 7, "p": 1}

| Field | Exact source value | Parameter recipe | Key |
|---|---|---|---|
| selection | `5\times 1` | `m\times p` | True |
| selection | `1\times 5` | `p\times m` | False |
| selection | `5\times 5` | `m\times m` | False |
| selection | `The product is undefined` | `The product is undefined` | False |
| selection | `7\times 5` | `n\times m` | False |
### q-70703

What are the dimensions of $ML$, if $M$ is a $4\times 3$ matrix and $L$ is a $3\times 6$ matrix?

Observed m,n,p: {"m": 4, "n": 3, "p": 6}

| Field | Exact source value | Parameter recipe | Key |
|---|---|---|---|
| selection | `3\times 6` | `n\times p` | False |
| selection | `The product is undefined` | `The product is undefined` | False |
| selection | `6\times 4` | `p\times m` | False |
| selection | `4\times 6` | `m\times p` | True |
| selection | `3\times 3` | `n\times n` | False |

## Validation and limits

validate.py checks the complete bounded domain, every complete source bank, correct designations, displayed labels and dimension chains, deterministic replay, one-slot changes with the other dimensions held constant, and the actual application grader for radio selections and equivalent/correct/incorrect blank entries. review.md contains originals, replay and changed-slot variants. The two unrated incomplete sources remain excluded. Hard has no validated source backbone in the inspected practice bank or canonical example and remains unsupported under this bounded package; new evidence reopens classification. No universal mathematical impossibility is asserted.

Task novelty uses the ordered shapes of the requested factors. Changing seed, labels, response type, difficulty label, choice order, or bank alone never creates additional inventory. One record per unseen task is admitted. The bounded domain contains 720 ordered distinct triples before profile exclusions and existing-content exclusions. Replenishment rechecks all current questions, canonical content, learner usage and reservations at a captured basis, then uses an additive transaction.

Within the verified backbone, larger dimension numerals, renamed matrices, or reordered options add no reasoning stages. A harder workload involving unknown dimensions, three factors, powers, or a different response contract would need an additional source-supported backbone. Those changes were not inferred to manufacture a hard label. This is a bounded capability exception, not proof that hard questions can never exist for the KP.
