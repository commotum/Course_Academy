# Four-stage template extraction

## 1. Specific source descriptions

All original number forms, prompts, banks and prose are preserved in source.json and shown in review.md. The table in classification.md records every original coefficient, exponent, equation order and zero/y/forcing role. Easy asks for homogeneous equations; moderate asks for inhomogeneous equations. All use y(x), prime notation, three bullet equations, text subset answers and a single selection radio. The coefficients are small signed integers; forcing is zero, a constant or monomial, or a y term that must be moved. There are no rational/singular coefficient functions or domain exclusions.

## 2. Shared mathematical pattern

The invariant is a first-order linear ODE. Move every y term to the left, normalize the derivative coefficient where needed, and inspect the resulting forcing function as an identity in x, rather than its value at one point. Source examples with x or x^3 on the right remain inhomogeneous even when that forcing vanishes at x=0. Each solution examines the equations in displayed order and concludes with a subset of Roman positions.

## 3. Components and complete-bank mapping

Each observed profile below lists every source choice one-to-one. Since these answers are subsets, recipes are exact categorical selection mistakes rather than numerical perturbations. A singleton may select only one inspected equation; the all-three response treats all equally; a pair includes or excludes another equation. No specific historical learner misconception is inferred beyond the exact subset selected. Identical bank membership across sources does not imply an authoring algorithm. Raw profiles are explicitly evidence-only; observed profiles use the exact same supported full bank in normal generation.

### q-331601

Original parameters: `{"a": 2, "n": 1, "rhs": [[0, 0, 0], [0, 4, 0], [-1, 0, 0]]}`. Correct subset: **I and III only**.

| Source option | Parameterized categorical operation | Reproduced |

|---|---|---|

| II only | Select exactly the displayed Roman positions II only | yes |

| I, II, and III | Select exactly the displayed Roman positions I, II, and III | yes |

| I and III only | Select exactly the displayed Roman positions I and III only | yes |

| I only | Select exactly the displayed Roman positions I only | yes |

| III only | Select exactly the displayed Roman positions III only | yes |

Prompt mask:
```text
Which of the following first-order linear differential equations are homogeneous?

- ${{eq0}}$
- ${{eq1}}$
- ${{eq2}}$
```

Worked-solution mask (full shared prose and operative stages):
```text
A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{{eq0}}.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
{{eq1}}.
$$

The presence of the constant term ${{force1}}$ means the right-hand side is not zero, and so it cannot be rewritten in homogeneous form. Thus, this equation is *not* homogeneous.

- Finally, we consider the equation

$$
{{eq2}}.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{{aligned_eq2}} \\ {{move2}} \\ {{collect2}}\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "I and III only."
```

### q-331744

Original parameters: `{"a": -1, "n": 1, "rhs": [[0, 0, 0], [1, 0, 0], [0, 1, 3]]}`. Correct subset: **III only**.

| Source option | Parameterized categorical operation | Reproduced |

|---|---|---|

| III only | Select exactly the displayed Roman positions III only | yes |

| II only | Select exactly the displayed Roman positions II only | yes |

| I only | Select exactly the displayed Roman positions I only | yes |

| I, II, and III | Select exactly the displayed Roman positions I, II, and III | yes |

| I and III only | Select exactly the displayed Roman positions I and III only | yes |

Prompt mask:
```text
Which of the following first-order linear differential equations are inhomogeneous?

- ${{eq0}}$
- ${{eq1}}$
- ${{eq2}}$
```

Worked-solution mask (full shared prose and operative stages):
```text
A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{{eq0}}.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
{{eq1}}.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{{aligned_eq1}} \\ {{move1}} \\ {{collect1}}.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{{eq2}}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)={{force2}}$ is not identically zero. Therefore, this equation is inhomogeneous.

Therefore, the correct answer is "III only."
```

### q-331605

Original parameters: `{"a": 1, "n": 2, "rhs": [[0, 3, 1], [0, 0, 0], [1, 0, 0]]}`. Correct subset: **I only**.

| Source option | Parameterized categorical operation | Reproduced |

|---|---|---|

| I only | Select exactly the displayed Roman positions I only | yes |

| II only | Select exactly the displayed Roman positions II only | yes |

| III only | Select exactly the displayed Roman positions III only | yes |

| I and II only | Select exactly the displayed Roman positions I and II only | yes |

| I, II, and III | Select exactly the displayed Roman positions I, II, and III | yes |

Prompt mask:
```text
Which of the following first-order linear differential equations are inhomogeneous?

- ${{eq0}}$
- ${{eq1}}$
- ${{eq2}}$
```

Worked-solution mask (full shared prose and operative stages):
```text
A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{{eq0}}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)={{force0}}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{{eq1}}.
$$

Notice that this equation has the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{{eq2}}.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{{aligned_eq2}} \\ {{move2}} \\ {{collect2}}.\end{aligned}
$$

Since our equation can be written in the form ${y}^{′}+P(x)y=0,$ the equation is homogeneous.

Therefore, the correct answer is "I only."
```

### q-331724

Original parameters: `{"a": 2, "n": 3, "rhs": [[0, 1, 2], [-3, 0, 0], [0, 0, 0]]}`. Correct subset: **II and III only**.

| Source option | Parameterized categorical operation | Reproduced |

|---|---|---|

| III only | Select exactly the displayed Roman positions III only | yes |

| I, II, and III | Select exactly the displayed Roman positions I, II, and III | yes |

| II only | Select exactly the displayed Roman positions II only | yes |

| I only | Select exactly the displayed Roman positions I only | yes |

| II and III only | Select exactly the displayed Roman positions II and III only | yes |

Prompt mask:
```text
Which of the following first-order linear differential equations are homogeneous?

- ${{eq0}}$
- ${{eq1}}$
- ${{eq2}}$
```

Worked-solution mask (full shared prose and operative stages):
```text
A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{{eq0}}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)={{force0}}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{{eq1}}.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{{aligned_eq1}} \\ {{move1}} \\ {{collect1}}\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{{eq2}}.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "II and III only."
```

### q-331725

Original parameters: `{"a": -1, "n": 1, "rhs": [[-1, 0, 0], [0, 0, 0], [-5, 0, 0]]}`. Correct subset: **I, II, and III**.

| Source option | Parameterized categorical operation | Reproduced |

|---|---|---|

| II only | Select exactly the displayed Roman positions II only | yes |

| I only | Select exactly the displayed Roman positions I only | yes |

| I, II, and III | Select exactly the displayed Roman positions I, II, and III | yes |

| I and III only | Select exactly the displayed Roman positions I and III only | yes |

| III only | Select exactly the displayed Roman positions III only | yes |

Prompt mask:
```text
Which of the following first-order linear differential equations are homogeneous?

- ${{eq0}}$
- ${{eq1}}$
- ${{eq2}}$
```

Worked-solution mask (full shared prose and operative stages):
```text
A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{{eq0}}.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{{aligned_eq0}} \\ {{move0}} \\ {{collect0}}\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Next, we consider the equation

$$
{{eq1}}.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{{eq2}}.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{{aligned_eq2}} \\ {{move2}} \\ {{collect2}}\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "I, II and III."
```

### q-331727

Original parameters: `{"a": 1, "n": 2, "rhs": [[-3, 0, 0], [0, 1, 1], [0, 0, 0]]}`. Correct subset: **I and III only**.

| Source option | Parameterized categorical operation | Reproduced |

|---|---|---|

| I only | Select exactly the displayed Roman positions I only | yes |

| III only | Select exactly the displayed Roman positions III only | yes |

| I and III only | Select exactly the displayed Roman positions I and III only | yes |

| I, II, and III | Select exactly the displayed Roman positions I, II, and III | yes |

| II only | Select exactly the displayed Roman positions II only | yes |

Prompt mask:
```text
Which of the following first-order linear differential equations are homogeneous?

- ${{eq0}}$
- ${{eq1}}$
- ${{eq2}}$
```

Worked-solution mask (full shared prose and operative stages):
```text
A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{{eq0}}.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{{aligned_eq0}} \\ {{move0}} \\ {{collect0}}\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Next, we consider the equation

$$
{{eq1}}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)={{force1}}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Finally, we consider the equation

$$
{{eq2}}.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I and III only."
```

### q-331728

Original parameters: `{"a": -4, "n": 1, "rhs": [[1, 0, 0], [0, 0, 0], [0, 9, 0]]}`. Correct subset: **I and II only**.

| Source option | Parameterized categorical operation | Reproduced |

|---|---|---|

| II only | Select exactly the displayed Roman positions II only | yes |

| III only | Select exactly the displayed Roman positions III only | yes |

| I and II only | Select exactly the displayed Roman positions I and II only | yes |

| I only | Select exactly the displayed Roman positions I only | yes |

| I, II, and III | Select exactly the displayed Roman positions I, II, and III | yes |

Prompt mask:
```text
Which of the following first-order linear differential equations are homogeneous?

- ${{eq0}}$
- ${{eq1}}$
- ${{eq2}}$
```

Worked-solution mask (full shared prose and operative stages):
```text
A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{{eq0}}.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{{aligned_eq0}} \\ {{move0}} \\ {{collect0}}\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Next, we consider the equation

$$
{{eq1}}.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{{eq2}}.
$$

The presence of the constant term ${{force2}}$ means the right-hand side is not zero, and so it cannot be rewritten in homogeneous form. Thus, this equation is *not* homogeneous.

Therefore, the correct answer is "I and II only."
```

### q-331729

Original parameters: `{"a": 7, "n": 1, "rhs": [[0, 5, 0], [0, 0, 0], [-2, 0, 0]]}`. Correct subset: **II and III only**.

| Source option | Parameterized categorical operation | Reproduced |

|---|---|---|

| II and III only | Select exactly the displayed Roman positions II and III only | yes |

| I, II, and III | Select exactly the displayed Roman positions I, II, and III | yes |

| III only | Select exactly the displayed Roman positions III only | yes |

| II only | Select exactly the displayed Roman positions II only | yes |

| I only | Select exactly the displayed Roman positions I only | yes |

Prompt mask:
```text
Which of the following first-order linear differential equations are homogeneous?

- ${{eq0}}$
- ${{eq1}}$
- ${{eq2}}$
```

Worked-solution mask (full shared prose and operative stages):
```text
A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

Now, let's consider each equation in turn.

- First, we consider the equation

$$
{{eq0}}.
$$

The presence of the constant term ${{force0}}$ means the right-hand side is not zero, and so it cannot be rewritten in homogeneous form. Thus, this equation is *not* homogeneous.

- Next, we consider the equation

$$
{{eq1}}.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{{eq2}}.
$$

We move the term involving $y$ to the left side so that all $y$-terms are together:

$$
\begin{aligned}{{aligned_eq2}} \\ {{move2}} \\ {{collect2}}\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "II and III only."
```

### q-331738

Original parameters: `{"a": 4, "n": 1, "rhs": [[0, 2, 0], [0, 0, 0], [1, 0, 0]]}`. Correct subset: **I only**.

| Source option | Parameterized categorical operation | Reproduced |

|---|---|---|

| I, II, and III | Select exactly the displayed Roman positions I, II, and III | yes |

| III only | Select exactly the displayed Roman positions III only | yes |

| II only | Select exactly the displayed Roman positions II only | yes |

| I and II only | Select exactly the displayed Roman positions I and II only | yes |

| I only | Select exactly the displayed Roman positions I only | yes |

Prompt mask:
```text
Which of the following first-order linear differential equations are inhomogeneous?

- ${{eq0}}$
- ${{eq1}}$
- ${{eq2}}$
```

Worked-solution mask (full shared prose and operative stages):
```text
A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{{eq0}}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)={{force0}}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{{eq1}}.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

- Finally, we consider the equation

$$
{{eq2}}.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{{aligned_eq2}} \\ {{move2}} \\ {{collect2}}.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."
```

### q-331739

Original parameters: `{"a": -1, "n": 2, "rhs": [[0, 1, 3], [1, 0, 0], [0, 0, 0]]}`. Correct subset: **I only**.

| Source option | Parameterized categorical operation | Reproduced |

|---|---|---|

| I, II, and III | Select exactly the displayed Roman positions I, II, and III | yes |

| I only | Select exactly the displayed Roman positions I only | yes |

| II only | Select exactly the displayed Roman positions II only | yes |

| I and II only | Select exactly the displayed Roman positions I and II only | yes |

| III only | Select exactly the displayed Roman positions III only | yes |

Prompt mask:
```text
Which of the following first-order linear differential equations are inhomogeneous?

- ${{eq0}}$
- ${{eq1}}$
- ${{eq2}}$
```

Worked-solution mask (full shared prose and operative stages):
```text
A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{{eq0}}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)={{force0}}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{{eq1}}.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{{aligned_eq1}} \\ {{move1}} \\ {{collect1}}.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{{eq2}}.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."
```

### q-331742

Original parameters: `{"a": 2, "n": 0, "rhs": [[1, 0, 0], [0, 1, 1], [0, 0, 0]]}`. Correct subset: **II only**.

| Source option | Parameterized categorical operation | Reproduced |

|---|---|---|

| II only | Select exactly the displayed Roman positions II only | yes |

| I, II, and III | Select exactly the displayed Roman positions I, II, and III | yes |

| III only | Select exactly the displayed Roman positions III only | yes |

| I and II only | Select exactly the displayed Roman positions I and II only | yes |

| I only | Select exactly the displayed Roman positions I only | yes |

Prompt mask:
```text
Which of the following first-order linear differential equations are inhomogeneous?

- ${{eq0}}$
- ${{eq1}}$
- ${{eq2}}$
```

Worked-solution mask (full shared prose and operative stages):
```text
A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{{eq0}}.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{{aligned_eq0}} \\ {{move0}} \\ {{collect0}}.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Next, we consider the equation

$$
{{eq1}}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)={{force1}}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Finally, we consider the equation

$$
{{eq2}}.
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

Therefore, the correct answer is "II only."
```

### q-331743

Original parameters: `{"a": 1, "n": 2, "rhs": [[0, -2, 0], [1, 0, 0], [0, 0, 0]]}`. Correct subset: **I only**.

| Source option | Parameterized categorical operation | Reproduced |

|---|---|---|

| III only | Select exactly the displayed Roman positions III only | yes |

| I and II only | Select exactly the displayed Roman positions I and II only | yes |

| I, II, and III | Select exactly the displayed Roman positions I, II, and III | yes |

| II only | Select exactly the displayed Roman positions II only | yes |

| I only | Select exactly the displayed Roman positions I only | yes |

Prompt mask:
```text
Which of the following first-order linear differential equations are inhomogeneous?

- ${{eq0}}$
- ${{eq1}}$
- ${{eq2}}$
```

Worked-solution mask (full shared prose and operative stages):
```text
A first-order linear differential equation is homogeneous if it can be written in the form

$$
{y}^{′}+P(x)y=0.
$$

A first-order linear differential equation is inhomogeneous if it is not homogeneous, i.e., if it can be written as

$$
{y}^{′}+P(x)y=Q(x)
$$

where $Q$ is not identical to zero.

To determine which equations are inhomogeneous, we examine each one in turn.

- First, we consider the equation

$$
{{eq0}}.
$$

Notice that this is written in the form ${y}^{′}+P(x)y=Q(x)$ where $Q(x)={{force0}}$ is not identically zero. Therefore, this equation is inhomogeneous.

- Next, we consider the equation

$$
{{eq1}}.
$$

We collect the $y$-terms on the left side:

$$
\begin{aligned}{{aligned_eq1}} \\ {{move1}} \\ {{collect1}}.\end{aligned}
$$

This matches the homogeneous form ${y}^{′}+P(x)y=0.$  Therefore, this equation *is* homogeneous.

- Finally, we consider the equation

$$
{{eq2}}.
$$

The right-hand side is already zero, so the equation directly matches the form ${y}^{′}+P(x)y=0.$ Therefore, this equation is homogeneous.

Therefore, the correct answer is "I only."
```

## 4. Reusable backbone and slots

Each source mask uses whole equation slots eq0..eq2, aligned originals, the expanded move-y rows, the collected-y row, and complete forcing operands. No short substring is substituted across prose or function notation. Original-mask rendering reproduces the whole decoded prompt and solution byte-for-byte. The normal path uses the same shared prose and stage masks under changed parameters. Labels/order are held by the chosen source layout; all observed layouts are eligible in default sampling.

Allowed slots: a has source sign and |a|=1..9; n remains 0 for the constant-coefficient mask and otherwise ranges 1..3. A y RHS has the observed sign, |b|=1..5, and c=m=0. A nonzero forcing has |c|=1..9, either fixed m=0 for constant-forcing masks or m=1..3 for monomials. A zero RHS stays (0,0,0). Constant-coefficient instances reject a=b to retain collection workload. The whole bank is chosen before these parameters; no option replacement or pooled-first-valid recipes are used. All explicit inputs enforce the same bounds.

Hard uses exactly three rows of (k,a,n,b,d,e,m), rendered as k y′ + a x^n y + d x^m = b y + e x^m. k=2..5, |a|,|b|,|d|,|e|=1..5, n,m=1..3; d=e for two positions and d!=e for the bank’s selected nonzero-forcing position. All x are real and division is only by the nonzero integer k, so domains are established before cancellation. Its three complete banks are the observed I/II/III single-correct banks, selected before sampling. Stage sequence: original, move-y (separate terms), collect y and forcing, divide to standard form, inspect forcing, conclude.

Meaningful categorical variety is finite. Magnitudes, variable lettering and option order do not create new semantic fingerprints. Source-layout roles, forcing type, requested criterion, constant-coefficient collection and normalization workload do. The complete policy has 15 categorical task fingerprints: six easy source role/layout demands, six moderate demands, and three hard nonzero-forcing positions. Independent coefficient/power values provide valid practice objects at the same method; they do not inflate that finite count. Do not describe the numerical parameter count as infinitely many skills.

There are no source repairs. Source q-331725 concludes “I, II and III,” while its bank spells “I, II, and III”; the exact prose is retained and the validator recognizes their identical subset meaning. Raw records preserve all source question/field/answer attribute-presence after removing EDB internal numeric IDs and normalizing schema enum/correct-reference representation to the required local review shape. UUID identity is regenerated and field-owned. source.json retains the untouched capture including internal IDs. No original omissions were present.

Validation reads concrete equations, all initial/intermediate/final operands and forcing values back from actual learner strings. Every intermediate equation must be equivalent after nonzero derivative normalization to its own prompt equation. Required expanded/collected/divided structures are checked separately from equality. Native grading selects each owned UUID and requires exactly the derived correct subset to pass. Mutation regressions corrupt a sign, remove an expanded row, stale the conclusion, or insert a control byte.
