# Four-stage template extraction

## Stage 1 — specific observed instances

Each below lists all supplied root categories inferred from the actual native artwork, every original bank option, response presence, statement roles and parameterized masks. Exponents in the drawing model are representatives; the source graph does not determine their exact values.

### q-38762

Source database ID 17592186129698. -1: simple, 1: simple, 2: multiple even. Leading sign positive.

Statement roles: `[["even", 2], ["odd_pair", 0, 1], ["value", 2]]`.

Complete bank: II and III only / I and II only / III only / I only / None

Field key/type: selection / :answer-field.type/radio. Original correct ref present: False.

Prompt operative mask:
```text
![]({asset})

The graph of a polynomial $p(x)$ is shown above. Which of the following statements are true?

1. $x = {r2}$ is a root of even multiplicity.
2. $x = ± {symmetric_root}$ are roots of odd multiplicity.
3. $p(0) = 2$.
```

Solution ordered operative mask:
```text
[Absent in source; raw replay preserves absence.]
```

### q-38768

Source database ID 17592186129699. -1: multiple even, 0: simple, 2: multiple even. Leading sign positive.

Statement roles: `[["even", 1], ["even_pair", 0, 2], ["limit", 1, 1]]`.

Complete bank: I and II only / I, II, and III / II only / II and III only / I only

Field key/type: selection / :answer-field.type/radio. Original correct ref present: False.

Prompt operative mask:
```text
![]({asset})

The graph of a polynomial $p(x)$ is shown above. Which of the following statements are true?

1. $x = {r1}$ is a root of even multiplicity.
2. $x ={r0}$ and $x = {r2}$ are roots of even multiplicity.
3. $p(x) → ∞$ as $x → ∞$.
```

Solution ordered operative mask:
```text
[Absent in source; raw replay preserves absence.]
```

### q-112591

Source database ID 17592186233151. -2: simple, 0: multiple odd, 2: multiple even. Leading sign positive.

Statement roles: `[["simple", 0], ["odd", 1], ["even", 2]]`.

Complete bank: [No source field.]

Field key/type: None / None. Original correct ref present: False.

Prompt operative mask:
```text
![]({asset})

The graph of a polynomial $p(x)$ is shown above. Which of the following statements are true?

I. - $x={r0}$ is a simple root.
II. - $x={r1}$ is a root of odd multiplicity.
III. - $x={r2}$ is a root of even multiplicity.
```

Solution ordered operative mask:
```text
Let's analyze each statement in turn.

- Statement I is true. The root $x={r0}$ is a simple root because the graph crosses the 
$x$-axis at the point and the curve is not tangent to the $x$-axis at that point.

- Statement II is true. The root $x={r1}$ has an odd multiplicity because the graph passes through the $x$-axis at this point.

- Statement III is true. The root $x={r2}$ has an even multiplicity because at $x={r2}$ the graph just touches the $x$-axis and reverses direction.

Therefore, the correct answer is "I, II, and III".
```

### q-112585

Source database ID 17592186247289. -2: simple, 0: multiple odd, 2: simple. Leading sign negative.

Statement roles: `[["positive"], ["limit", 1, -1], ["odd", 1]]`.

Complete bank: I and III only / I only / I and II only / II and III only / II only

Field key/type: selection / :answer-field.type/radio. Original correct ref present: True.

Prompt operative mask:
```text
![]({asset})

The graph of a polynomial $p(x)$ is shown above. Which of the following statements are true?

- $p(0)$ is positive.
- $p(x)\to -\infty $ as $x\to \infty .$
- $x={r1}$ is a root of odd multiplicity.
```

Solution ordered operative mask:
```text
Let's analyze each statement in turn.

- Statement I is false. The graph passes through the $y$-axis at $y=0,$ which means that $p(0)=0.$

- Statement II is true. As $x$ moves right in the positive direction towards $\infty ,$ the $y$ value moves down in the negative direction towards $-\infty .$

- Statement III is true. The root $x={r1}$ has an odd multiplicity because the graph passes through the $x$-axis at this point.

Therefore, the correct answer is "II and III only".
```

### q-112587

Source database ID 17592186247290. -2: simple, 0: multiple even, 1: simple. Leading sign negative.

Statement roles: `[["limit", -1, 1], ["value", 0], ["even", 2]]`.

Complete bank: None of those listed / I and II only / III only / I and III only / II only

Field key/type: selection / :answer-field.type/radio. Original correct ref present: True.

Prompt operative mask:
```text
![]({asset})

The graph of a polynomial $p(x)$ is shown above. Which of the following statements are true?

- $p(x)\to \infty $ as $x\to -\infty .$
- $p(0)=0.$
- $x={r2}$ is a root of even multiplicity.
```

Solution ordered operative mask:
```text
Let's analyze each statement in turn.

- Statement I is false. As $x$ moves left in the negative direction towards $-\infty ,$ the $y$ value moves down in the negative direction towards $-\infty .$

- Statement II is true. The graph passes through the $y$-axis at $y=0$, which means that $p(0)=0.$

- Statement III is false. The root $x={r2}$ has an odd multiplicity because the graph passes through the $x$-axis at this point.

Therefore, the correct answer is "II only".
```

### q-38680

Source database ID 17592186326706. -3: simple, -1: multiple odd, 2: simple. Leading sign negative.

Statement roles: `[["limit", 1, -1], ["simple", 1], ["even", 2]]`.

Complete bank: III only / I only / II and III only / I and II only / II only

Field key/type: selection / :answer-field.type/radio. Original correct ref present: True.

Prompt operative mask:
```text
![]({asset})

The graph of a polynomial $p(x)$ is shown above. Which of the following statements are correct?

- $p(x)\to -\infty $ as $x\to \infty .$
- $x={r1}$ is a simple root.
- $x={r2}$ is a root of even multiplicity.
```

Solution ordered operative mask:
```text
Let's analyze each statement in turn.

- Statement I is true. As $x$ moves right in the positive direction towards $+\infty ,$ the $y$ value moves down in the negative direction towards $-\infty .$

- Statement II is false. The root $x={r1}$ is not a simple root because the graph crosses the $x$-axis at the point, and the curve is tangent to the $x$-axis at that point.

- Statement III is false. The root $x={r2}$ has an odd multiplicity because the graph passes through the $x$-axis at this point.

Therefore, the correct answer is "I only".
```

### q-38770

Source database ID 17592186326713. -2: simple, -1: multiple even, 2: simple. Leading sign positive.

Statement roles: `[["simple", 2], ["even", 1], ["limit", 1, -1]]`.

Complete bank: II only / I and II only / III only / II and III only / I, II and III

Field key/type: selection / :answer-field.type/radio. Original correct ref present: True.

Prompt operative mask:
```text
![]({asset})

The graph of a polynomial $p(x)$ is shown above. Which of the following statements are true?

I. $x={r2}$ is a simple root.

II. $x={r1}$ is a root of even multiplicity.

III. $p(x)\to -\infty $ as $x\to \infty .$
```

Solution ordered operative mask:
```text
Let's analyze each statement in turn.

- Statement I is true. The root $x={r2}$ is a simple root because the graph crosses the $x$-axis at the point and the curve is not tangent to the $x$-axis at that point.

- Statement II is true. The root $x={r1}$  has an even multiplicity because at $x={r1}$ the graph just touches the $x$-axis and reverses direction.

- Statement III is false. As $x$ moves right in the positive direction towards $+\infty ,$ the $y$ value moves up in the positive direction towards $+\infty .$

Therefore, the correct answer is "I and II only".
```

### q-38779

Source database ID 17592186326715. -4: multiple even, 1: simple, 3: multiple even. Leading sign negative.

Statement roles: `[["odd", 0], ["value", 3], ["odd", 1]]`.

Complete bank: III only / II and III only / II only / I and III only / I and II only

Field key/type: selection / :answer-field.type/radio. Original correct ref present: True.

Prompt operative mask:
```text
![]({asset})

The graph of a polynomial $p(x)$ is shown above. Which of the following statements are true?

- $x={r0}$ is a root of odd multiplicity.
- $p(0)={y0}.$
- $x={r1}$ is a root of odd multiplicity.
```

Solution ordered operative mask:
```text
Let's analyze each statement in turn.

- Statement I is false. The root $x={r0}$ has an even multiplicity because at $x={r0}$ the graph just touches the $x$-axis and reverses direction.

- Statement II is true. The graph passes through the $y$-axis at $y={y0}$, which means that $p(0)={y0}.$

- Statement III is true. The root $x={r1}$ has an odd multiplicity because the graph passes through the $x$-axis at the point.

Therefore, the correct answer is "II and III only".
```

### q-80302

Source database ID 17592186348356. -3: simple, -1: simple, 2: multiple odd. Leading sign positive.

Statement roles: `[["simple", 1], ["odd", 2], ["simple", 2]]`.

Complete bank: III only / II only / I and II only / I only / I,II and III

Field key/type: selection / :answer-field.type/radio. Original correct ref present: True.

Prompt operative mask:
```text
![]({asset})

The graph of a polynomial $p(x)$ is shown above. Which of the following statements are true?

- $x={r1}$ is a simple root.
- $x={r2}$ is a root of odd multiplicity.
- $x={r2}$ is a simple root.
```

Solution ordered operative mask:
```text
Let's analyze each statement in turn.

- Statement I is true. The root $x={r1}$ is a simple root because the graph crosses the $x$-axis at the point and the curve is not tangent to the $x$-axis at that point.

- Statement II is true. The root $x={r2}$ has an odd multiplicity because at $x={r2}$ the graph passes through the $x$-axis at this point.

- Statement III is false. The root $x={r2}$ is not a simple root because the graph crosses the $x$-axis at that point, and the curve is tangent to the $x$-axis at that point.

Therefore, the correct answer is "I and II only".
```

### q-80303

Source database ID 17592186348357. -2: simple, 1: multiple odd, 4: simple. Leading sign positive.

Statement roles: `[["even", 0], ["not_simple", 1], ["even", 1]]`.

Complete bank: I only / II only / III only / II and III only / I and II only

Field key/type: selection / :answer-field.type/radio. Original correct ref present: True.

Prompt operative mask:
```text
![]({asset})

The graph of a polynomial $p(x)$ is shown above. Which of the following statements are true?

I. $x={r0}$ is a root of even multiplicity.

II. $x={r1}$ is **not** a simple root.

III. $x={r1}$ is a root of even multiplicity.
```

Solution ordered operative mask:
```text
Let's analyze each statement in turn.

- Statement I is false. The root $x={r0}$ has an odd multiplicity because at $x={r0}$ the graph passes through the $x$-axis at this point.

- Statement II is true. The root $x={r1}$ is not a simple root because the graph crosses the $x$-axis at that point, and the curve is tangent to the $x$-axis at that point.

- Statement III is false. The root $x={r1}$ has an odd multiplicity because at $x={r1}$ the graph passes through the $x$-axis at this point.

Therefore, the correct answer is "II only".
```

## Stage 2 — shared pattern

Read one graph, evaluate three statements about visible root categories, a displayed intercept or end behavior, and select the complete true subset. The exact polynomial equation is never supplied or requested. The worked solution analyzes I, II, III in that order before a single final subset sentence.

## Stage 3 — component and bank mapping

Every bank string maps to the subset of I/II/III named by that complete string; “None” and “None of those listed” map to the empty subset. Each option is a full assertion of precisely which statements are true, with every omitted statement false. The correct subset is computed from the actual polynomial, independently of the stored bank. Wrong subsets are derived by their included/omitted statement claims, not numerical perturbation and not a source answer table. Original banks differ and are never pooled. The fieldless source bank is an explicitly authored five-option extension. Every source option and presence/absence key is preserved in `source:*` API replay.

## Stage 4 — extracted reusable backbone and slots

`recipes.json` contains prompt and solution masks with only complete x=integer operands replaced by root role slots. The assessed positive y-intercept in q-38779 replaces complete p(0)=3/y=3 operands. ± root notation retains its symmetric pair. Numeric operands elsewhere, infinite-limit signs, source truth words, paragraphs, line breaks, double spaces and punctuation are unchanged in observed masks. Replacing complete components avoids accidental modifications to prose or commands. Shared masks are checked both at anchors and changed parameters.

Fixed: three supplied statements, one graph, source statement roles/categories/leading sign, ordered analysis and source field layout. Variable: ordered root locations within role constraints, marked positive intercept 1…4, and category-compatible polynomial rendering representatives. Optional: raw absent source keys; repaired keys are explicitly labeled. Conditional: figure source reuse only for exact anchor rendering parameters; otherwise the same public API recreates the actual parameter-dependent plot. Solution truth/category/end claims derive from the same polynomial and its role constraints. One fixed worked solution per instance never depends on the selected learner error.

Canonical mathematical fingerprints include visible root zero sets/categories, leading end signs and assessed statement roles/values. Coefficient magnitude, seed, option order, template/profile aliases and exact exponents within an unassessed category do not add tasks. Content IDs depend on actual displayed prompt, solution and complete bank/presence contract.

## Interpretation limits

All source wrong options are transparent subset alternatives, requiring no speculative wrong-value recipe. Unknown source exponent values or amplitude are explicitly not recovered. A minimal category-compatible polynomial is a defensible renderer default only. Qualitative plots do not assess exact degree, leading-coefficient magnitude or exponent 3 versus 5. q-38779 alone marks an exact nonzero intercept. The wrong positive p(0)=2 claim in q-38762 is rejectable from its negative intercept without needing a vertical scale.

## Finite meaningful domains

`finite-domains.json` enumerates eligible increasing root tuples in the explicit -6…6 domain, preserving category patterns, source symmetry/zero constraints and .04 lobe legibility. It records 9/30/21/24/30/96/136/228/137/96 meaningful tasks for the ten observed layouts respectively, and 116 for hard. The narrow ± root source has only nine eligible meaningful tasks and is not advertised as unlimited variety. q-38779 includes four assessed marked intercept values; other coefficient magnitudes and within-category exponents do not add tasks. Exact same predicates at the same roots are rejected; equal truth status alone does not make distinct root predicates equivalent. Whole subset choices name different complete truth vectors.
