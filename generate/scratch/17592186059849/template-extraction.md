# Template extraction

## 1. Specific descriptions

The following per-source entries retain the exact original prompt, fields, choices, solution and matrix coefficients. The source wrapper is copied without modification in source.json. Each constant entry c0..c8, linear coefficient v0..v8 and quadratic coefficient w0..w8 is row-major. All variables are real.

## 2. Shared patterns

Easy: expand the three first-row minors, collect an affine determinant and solve one linear equation. Moderate: expand to a quadratic, set the determinant to its specified value or zero, and solve by the original factorization, square-root or quadratic-formula method; two blanks retain ascending root order. Observed hard profiles: expand an identically zero determinant and conclude all real parameter values, retaining either proportional rows or a zero first column. Authored default hard: expand a dense affine matrix and distinguish an identity from a linear or quadratic singularity equation. Every default hard outcome uses the same five-option text-radio format, including finite sets, so neither response format nor difficulty determines the answer. Named/unnamed and blank/radio/checkbox prompts remain distinct source layouts. In observed finite-set checkbox profiles, individual Boolean fields test membership.

## 3. Components and complete bank mapping

Coefficient formulas in the observed bank column are value-preserving inferred expressions, with unknown misconception intent. They are supported only as evidence replay and explicit profile variants. They are not default learner banks. Radio options are compared as complete root sets. Checkbox options are individual values with Boolean membership in the complete root set; both roots must appear in the pool. Their current expressions and labels are recorded in checkbox-recipes.json.

## 4. Reusable templates and constraints

The prompt layout masks the whole parameter-dependent matrix and target. Matrix entry i is c_i+v_i*u+w_i*u². Constant zeros, variable positions and degrees are retained. Constants sample from small signed integers; easy targets from -50..80. Moderate named/given targets are computed by evaluating a new determinant at an integer in -8..8, giving rational roots; the symmetric square template samples target 2..50 and permits radicals. Singular quadratics must retain the variable-factor structure. Explicit observed hard profiles retain row2=-2 row1 or column1=0. The separate authored default hard family constructs dense affine matrices for identity, linear, and quadratic determinants after selecting a complete five-choice bank. Its roots r and s are nonzero, distinct, and not opposites, making all five candidate sets distinct. The bank has all real values, r only, s only, r and s only, and -r and -s only, with identical rendering and a single radio field across outcomes. Easy/moderate sampling changes at most two nonzero constants, preserving variable coefficients and zero positions: fresh variants within observed structures, not broad coverage of arbitrary determinant equations. Repeated roots, no-real-root cases and cubics do not occur in the captured sources and remain outside scope. Complete banks are selected first and whole-instance equivalence/domain rejection follows. Explicit input never silently resamples.

Default radio banks are authored operation-derived five-option profiles. Default checkbox pools take the distinct individual values from the corresponding whole operation-derived profile, include both roots and at least one nonroot, and label this an authored extension. Observed checkbox replay retains every captured value label and option count; any collision rejects the complete instance. Easy errors reverse the numerator, omit division, or report a coefficient/constant. The q-9961 default retains its observed Any real number alternative, so learners still distinguish a unique solution from an identity. Other default numeric alternatives remain authored and differ from the captured bank; complete source bank coverage describes explicit source profiles, not identical default distractor coverage. Moderate errors reverse formula signs, lose a root or omit the quadratic constant; singular banks distinguish the zero and nonzero roots. Explicit authored source-profile hard banks retain alternatives obtained by incorrectly demanding one minor be zero or equating variable-column entries to fixed entries. The authored default hard bank instead tests identity versus finite roots, omission of a root, and root-sign confusion. Every candidate set can be the correct set, independently of the displayed option bank. No diagnosis text is added to learner solutions.

The shared worked solution retains source opening/singularity/conclusion sentences and cofactor → collect → solve sequence. Per-source product/expansion stage order and solve methods are retained; product notation is reconstructed and standardized; exact per-source row typography is a fidelity limitation. q-280403 is corrected from det(F) to the given det(A); q-280541 retains ± in the intermediate where the source incorrectly prints only +.

Current database keys are present for all 24 questions. q-9657 now has Boolean keys for {-8,-2}; q-9852 retains the repaired Any value of k radio key. Database keys are preserved and independently checked. Both source difficulty labels remain absent, so their moderate/hard assignments are still authored. The database now supplies brief explanations on those two questions; the generator retains its independently checked full cofactor derivations, documented as a solution expansion rather than literal prose fidelity.

### q-9657 — quadratic_determinant_checkbox

**Original prompt**

Given that the determinant of
$\begin{bmatrix}2 & -1 & 3 \\ x & 2 & 4 \\ -2 & 1 & x + 3\end{bmatrix}$
is $8$, find all the possible values of $x$.

Select all that apply. If none apply, leave all boxes unchecked.

- **I.** $x=-8$
- **II.** $x=-2$
- **III.** $x=2$
- **IV.** $x=5$
- **V.** $x=6$
- **VI.** $x=8$

Coefficients: `{"constants": [2, -1, 3, 0, 2, 4, -2, 1, 3], "linear": [0, 0, 0, 1, 0, 0, 0, 0, 1], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 8}`. Fields: `I, II, III, IV, V, VI`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| false | :answer.type/text | `('Boolean membership for I', 'r0')` |
| true | :answer.type/text | `('Boolean membership for I', 'r0')` |
| false | :answer.type/text | `('Boolean membership for II', 'r1')` |
| true | :answer.type/text | `('Boolean membership for II', 'r1')` |
| false | :answer.type/text | `('Boolean membership for III', 'c0')` |
| true | :answer.type/text | `('Boolean membership for III', 'c0')` |
| false | :answer.type/text | `('Boolean membership for IV', 'c5+c7')` |
| true | :answer.type/text | `('Boolean membership for IV', 'c5+c7')` |
| false | :answer.type/text | `('Boolean membership for V', 'c2*c4')` |
| true | :answer.type/text | `('Boolean membership for V', 'c2*c4')` |
| false | :answer.type/text | `('Boolean membership for VI', 'D')` |
| true | :answer.type/text | `('Boolean membership for VI', 'D')` |

Original worked solution:

The determinant is $x^{2} + 10 x + 24$. Setting it equal to $8$ gives $\left\{-8, -2\right\}$.

### q-9669 — linear_singular_radio

**Original prompt**

Find the possible values of the constant $k$ given that the matrix $[\begin{aligned}2 & 1 & -4 \\ 2k+1 & 3 & k \\ 1 & 0 & 1\end{aligned}]$ is singular.

Coefficients: `{"constants": [2, 1, -4, 1, 3, 0, 1, 0, 1], "linear": [0, 0, 0, 2, 0, 1, 0, 0, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 0}`. Fields: `selection`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| 17 | :answer.type/math | `('correct',)` |
| -6 | :answer.type/math | `('-c0*c4',)` |
| -1 | :answer.type/math | `('-c3',)` |
| 5 | :answer.type/math | `('-c2+c3',)` |
| 6 | :answer.type/math | `('c0*c4',)` |

Original worked solution:

First, let's use our formula to find an expression for the determinant in terms of $k:$ 

$$
\begin{aligned}|\begin{aligned}2 & 1 & -4 \\ 2k+1 & 3 & k \\ 1 & 0 & 1\end{aligned}| & =2|\begin{aligned}3 & k \\ 0 & 1\end{aligned}|-1|\begin{aligned}2k+1 & k \\ 1 & 1\end{aligned}|-4|\begin{aligned}2k+1 & 3 \\ 1 & 0\end{aligned}| \\  & =2(3-0)-(2k+1-k)-4(0-3) \\  & =2\cdot 3-(k+1)-4\cdot (-3) \\  & =6-k-1+12 \\  & =17-k\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}17-k & =0 \\ k & =17\end{aligned}
$$

Therefore, the solution is $k=17.$

### q-9852 — identity_singular_radio

**Original prompt**

Find the possible values of the constant $k$ given that the matrix
$\begin{bmatrix}0 & 7 & 4k \\ 0 & 9 & 5k \\ 0 & 11 & 6k\end{bmatrix}$ is singular.

Coefficients: `{"constants": [0, 7, 0, 0, 9, 0, 0, 11, 0], "linear": [0, 0, 4, 0, 0, 5, 0, 0, 6], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 0}`. Fields: `selection`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| Any value of $k$ | :answer.type/text | `('all',)` |
| $10$ only | :answer.type/text | `('(c4+c7)/2',)` |
| $0$ only | :answer.type/text | `('0',)` |
| $2$ only | :answer.type/text | `('v8-v2',)` |
| $3$ and $-3$ only | :answer.type/text | `('v8/2', '-v8/2')` |

Original worked solution:

The determinant is $0$. Setting it equal to $0$ gives $\mathbb{R}$.

### q-128500 — linear_named_determinant_radio

**Original prompt**

Given that
$B=[\begin{aligned}1 & 2 & -5 \\ 1 & 2 & 1 \\ y & 2 & 1\end{aligned}]$
and $det(B)=12,$ find the value of $y.$

Coefficients: `{"constants": [1, 2, -5, 1, 2, 1, 0, 2, 1], "linear": [0, 0, 0, 0, 0, 0, 1, 0, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 12}`. Fields: `selection`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| -8 | :answer.type/math | `('c1*c2+c1',)` |
| 10 | :answer.type/math | `('-c1*c2',)` |
| 13 | :answer.type/math | `('D+c0',)` |
| 2 | :answer.type/math | `('correct',)` |
| -5 | :answer.type/math | `('c2',)` |

Original worked solution:

Let's use our formula to find an expression for the determinant in terms of $y:$

$$
\begin{aligned}\text{det}(B) & =|\begin{aligned}1 & 2 & -5 \\ 1 & 2 & 1 \\ y & 2 & 1\end{aligned}| \\  & =1|\begin{aligned}2 & 1 \\ 2 & 1\end{aligned}|-2|\begin{aligned}1 & 1 \\ y & 1\end{aligned}|-5|\begin{aligned}1 & 2 \\ y & 2\end{aligned}| \\  & =0-2\cdot (1-y)-5\cdot (2-2y) \\  & =12y-12\end{aligned}
$$

Since the determinant of the matrix is $12,$ we have:

$$
\begin{aligned}12y-12 & =12 \\ 12y & =24 \\ y & =2\end{aligned}
$$

### q-128502 — linear_named_determinant_radio

**Original prompt**

Given that 
$C=[\begin{aligned}2 & 3 & 1 \\ -1 & q & 5 \\ 0 & -5 & 1\end{aligned}]$ 
and $det(C)=28,$ find the value of $q.$

Coefficients: `{"constants": [2, 3, 1, -1, 0, 5, 0, -5, 1], "linear": [0, 0, 0, 0, 1, 0, 0, 0, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 28}`. Fields: `selection`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| -10 | :answer.type/math | `('2*c3*c5',)` |
| 20 | :answer.type/math | `('-c7*c0*c0',)` |
| 2 | :answer.type/math | `('c0',)` |
| 12 | :answer.type/math | `('c0*c0*c1',)` |
| -15 | :answer.type/math | `('correct',)` |

Original worked solution:

Let's use our formula to find an expression for the determinant in terms of $q:$

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}2 & 3 & 1 \\ -1 & q & 5 \\ 0 & -5 & 1\end{aligned}| \\  & =2|\begin{aligned}q & 5 \\ -5 & 1\end{aligned}|-3|\begin{aligned}-1 & 5 \\ 0 & 1\end{aligned}|+1|\begin{aligned}-1 & q \\ 0 & -5\end{aligned}| \\  & =2\cdot (q+25)-3\cdot (-1)+5 \\  & =2q+58\end{aligned}
$$

Since the determinant of the matrix is $28,$ we have:

$$
\begin{aligned}2q+58 & =28 \\ 2q & =-30 \\ q & =-15\end{aligned}
$$

### q-130575 — quadratic_determinant_checkbox

**Original prompt**

Given that the determinant of
$[\begin{aligned}2 & 1 & 5 \\ 2 & 3 & z \\ z & -1 & 1\end{aligned}]$
is $-48$, find all the possible values of $z.$

Select all that apply. If none apply, leave all boxes unchecked.

- **I.** $z=-5$
- **II.** $z=-2$
- **III.** $z=3$
- **IV.** $z=5$
- **V.** $z=6$
- **VI.** $z=7$

Coefficients: `{"constants": [2, 1, 5, 2, 3, 0, 0, -1, 1], "linear": [0, 0, 0, 0, 0, 1, 1, 0, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": -48}`. Fields: `I, II, III, IV, V, VI`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| false | :answer.type/text | `('Boolean membership for I', '-c2')` |
| true | :answer.type/text | `('Boolean membership for I', '-c2')` |
| false | :answer.type/text | `('Boolean membership for II', 'c7-1')` |
| true | :answer.type/text | `('Boolean membership for II', 'c7-1')` |
| false | :answer.type/text | `('Boolean membership for III', 'c4')` |
| true | :answer.type/text | `('Boolean membership for III', 'c4')` |
| false | :answer.type/text | `('Boolean membership for IV', 'c2')` |
| true | :answer.type/text | `('Boolean membership for IV', 'c2')` |
| false | :answer.type/text | `('Boolean membership for V', 'r0')` |
| true | :answer.type/text | `('Boolean membership for V', 'r0')` |
| false | :answer.type/text | `('Boolean membership for VI', 'r1')` |
| true | :answer.type/text | `('Boolean membership for VI', 'r1')` |

Original worked solution:

Let's use our formula to find an expression for the determinant in terms of $z:$

$$
\begin{aligned}|\begin{aligned}2 & 1 & 5 \\ 2 & 3 & z \\ z & -1 & 1\end{aligned}| & =2|\begin{aligned}3 & z \\ -1 & 1\end{aligned}|-1|\begin{aligned}2 & z \\ z & 1\end{aligned}|+5|\begin{aligned}2 & 3 \\ z & -1\end{aligned}| \\  & =2(3+z)-(2-{z}^{2})+5(-2-3z) \\  & =6+2z-2+{z}^{2}-10-15z \\  & ={z}^{2}-13z-6\end{aligned}
$$

Since the determinant of the matrix is $-48,$ we have:

$$
\begin{aligned}{z}^{2}-13z-6 & =-48 \\ {z}^{2}-13z+42 & =0 \\ z & =\frac{-(-13)\pm \sqrt{{13}^{2}-4\cdot 1\cdot 42}}{2\cdot 1} \\  & =\frac{13\pm \sqrt{1}}{2} \\  & =\frac{13\pm 1}{2} \\  & =6,7\end{aligned}
$$

Therefore, the solutions are $z=6$ and $z=7.$

### q-130580 — quadratic_determinant_checkbox

**Original prompt**

Given that the determinant of
$[\begin{aligned}x & 2x & 3 \\ 5 & x & 7 \\ 3 & 2 & 1\end{aligned}]$
is $22$, find all the possible values of $x.$

Select all that apply. If none apply, leave all boxes unchecked.

- **I.** $x=-8$
- **II.** $x=-5$
- **III.** $x=-3$
- **IV.** $x=-1$
- **V.** $x=3$
- **VI.** $x=5$
- **VII.** $x=7$
- **VIII.** $x=8$

Coefficients: `{"constants": [0, 0, 3, 5, 0, 7, 3, 2, 1], "linear": [1, 2, 0, 0, 1, 0, 0, 0, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 22}`. Fields: `I, II, III, IV, V, VI, VII, VIII`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| false | :answer.type/text | `('Boolean membership for I', 'r0')` |
| true | :answer.type/text | `('Boolean membership for I', 'r0')` |
| false | :answer.type/text | `('Boolean membership for II', '-c3')` |
| true | :answer.type/text | `('Boolean membership for II', '-c3')` |
| false | :answer.type/text | `('Boolean membership for III', '-c2')` |
| true | :answer.type/text | `('Boolean membership for III', '-c2')` |
| false | :answer.type/text | `('Boolean membership for IV', 'r1')` |
| true | :answer.type/text | `('Boolean membership for IV', 'r1')` |
| false | :answer.type/text | `('Boolean membership for V', 'c2')` |
| true | :answer.type/text | `('Boolean membership for V', 'c2')` |
| false | :answer.type/text | `('Boolean membership for VI', 'c3')` |
| true | :answer.type/text | `('Boolean membership for VI', 'c3')` |
| false | :answer.type/text | `('Boolean membership for VII', 'c5')` |
| true | :answer.type/text | `('Boolean membership for VII', 'c5')` |
| false | :answer.type/text | `('Boolean membership for VIII', '-r0')` |
| true | :answer.type/text | `('Boolean membership for VIII', '-r0')` |

Original worked solution:

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}x & 2x & 3 \\ 5 & x & 7 \\ 3 & 2 & 1\end{aligned}| & =x|\begin{aligned}x & 7 \\ 2 & 1\end{aligned}|-2x|\begin{aligned}5 & 7 \\ 3 & 1\end{aligned}|+3|\begin{aligned}5 & x \\ 3 & 2\end{aligned}| \\  & =x(x-14)-2x(5-21)+3(10-3x) \\  & ={x}^{2}-14x+32x+30-9x \\  & ={x}^{2}+9x+30\end{aligned}
$$

Since the determinant of the matrix is $22,$ we have:

$$
\begin{aligned}{x}^{2}+9x+30 & =22 \\ {x}^{2}+9x+8 & =0 \\ x & =\frac{-9\pm \sqrt{{9}^{2}-4\cdot 1\cdot 8}}{2\cdot 1} \\  & =\frac{-9\pm \sqrt{49}}{2} \\  & =\frac{-9\pm 7}{2} \\  & =-8,-1\end{aligned}
$$

Therefore, the solutions are $x=-8$ and $x=-1.$

### q-130620 — linear_singular_radio

**Original prompt**

Find the possible values of the constant $x$ given that the matrix $[\begin{aligned}3 & 5 & 8 \\ 1 & 1 & 2 \\ x & -1 & -x\end{aligned}]$ is singular.

Coefficients: `{"constants": [3, 5, 8, 1, 1, 2, 0, -1, 0], "linear": [0, 0, 0, 0, 0, 0, 1, 0, -1], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 0}`. Fields: `selection`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| \frac{1}{2} | :answer.type/math | `('correct',)` |
| \frac{7}{4} | :answer.type/math | `('(c2-c3)/B',)` |
| 8 | :answer.type/math | `('c2',)` |
| 5 | :answer.type/math | `('c1',)` |
| -9 | :answer.type/math | `('-c2-c3',)` |

Original worked solution:

First, let's use our formula to find an expression for the determinant in terms of $x:$ 

$$
\begin{aligned}|\begin{aligned}3 & 5 & 8 \\ 1 & 1 & 2 \\ x & -1 & -x\end{aligned}| & =3|\begin{aligned}1 & 2 \\ -1 & -x\end{aligned}|-5|\begin{aligned}1 & 2 \\ x & -x\end{aligned}|+8|\begin{aligned}1 & 1 \\ x & -1\end{aligned}| \\  & =3(-x+2)-5(-x-2x)+8(-1-x) \\  & =-3x+6+15x-8-8x \\  & =4x-2\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}4x-2 & =0 \\ x & =\frac{1}{2}\end{aligned}
$$

Therefore, the solution is $x=\frac{1}{2}.$

### q-130626 — identity_singular_radio

**Original prompt**

Find the possible values of the constant $p$ given that the matrix
$[\begin{aligned}1 & -3p & 4 \\ -2 & 6p & -8 \\ 1 & -1 & 1\end{aligned}]$ is singular.

Coefficients: `{"constants": [1, 0, 4, -2, 0, -8, 1, -1, 1], "linear": [0, -3, 0, 0, 6, 0, 0, 0, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 0}`. Fields: `selection`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| $\frac{5}{2}$ only | :answer.type/text | `('(c2+c0)/abs(c3)',)` |
| Any value of $p$ | :answer.type/text | `('all',)` |
| $-3$ and $3$ only | :answer.type/text | `('v1', '-v1')` |
| $-3$ only | :answer.type/text | `('v1',)` |
| $-10$ only | :answer.type/text | `('-abs(c5)-abs(c3)',)` |

Original worked solution:

First, let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}|\begin{aligned}1 & -3p & 4 \\ -2 & 6p & -8 \\ 1 & -1 & 1\end{aligned}| & =1|\begin{aligned}6p & -8 \\ -1 & 1\end{aligned}|-(-3p)|\begin{aligned}-2 & -8 \\ 1 & 1\end{aligned}|+4|\begin{aligned}-2 & 6p \\ 1 & -1\end{aligned}| \\  & =(6p-8)+3p(-2+8)+4(2-6p) \\  & =6p-8+18p+8-24p \\  & =0.\end{aligned}
$$

Therefore, this matrix is singular for all values of $p.$

### q-18252 — linear_singular_radio

**Original prompt**

Find the possible values of the constant $p$ given that the matrix $[\begin{aligned}1 & 0 & 1 \\ 2 & 1 & 2 \\ 6 & -5 & 2p-4\end{aligned}]$ is singular.

Coefficients: `{"constants": [1, 0, 1, 2, 1, 2, 6, -5, -4], "linear": [0, 0, 0, 0, 0, 0, 0, 0, 2], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 0}`. Fields: `selection`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| -3 | :answer.type/math | `('c7+c3',)` |
| 5 | :answer.type/math | `('correct',)` |
| 3 | :answer.type/math | `('c0+c3',)` |
| -5 | :answer.type/math | `('-r0',)` |
| 2 | :answer.type/math | `('c3',)` |

Original worked solution:

First, let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}|\begin{aligned}1 & 0 & 1 \\ 2 & 1 & 2 \\ 6 & -5 & 2p-4\end{aligned}| & =1|\begin{aligned}1 & 2 \\ -5 & 2p-4\end{aligned}|-0|\begin{aligned}2 & 2 \\ 6 & 2p-4\end{aligned}|+1|\begin{aligned}2 & 1 \\ 6 & -5\end{aligned}| \\  & =(2p-4+10)-0+(-10-6) \\  & =2p-4+10-10-6 \\  & =2p-10\end{aligned}
$$

Since the matrix is singular, the determinant is $0.$ So,  we have:

 

$$
\begin{aligned}2p-10 & =0 \\ 2p & =10 \\ p & =\frac{10}{2} \\  & =5\end{aligned}
$$

Therefore, the solution is $p=5.$

### q-18256 — quadratic_determinant_checkbox

**Original prompt**

Given that the determinant of 
$[\begin{aligned}4 & 2 & 3 \\ -3y & -2 & 1 \\ 2 & y & -5\end{aligned}]$
 is $81,$ find all the possible values of $y.$

Select all that apply. If none apply, leave all boxes unchecked.

- **I.** $y=- \frac{25}{9}$
- **II.** $y=- \frac{5}{3}$
- **III.** $y=-1$
- **IV.** $y=1$

Coefficients: `{"constants": [4, 2, 3, 0, -2, 1, 2, 0, -5], "linear": [0, 0, 0, -3, 0, 0, 0, 1, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 81}`. Fields: `I, II, III, IV`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| false | :answer.type/text | `('Boolean membership for I', 'r0')` |
| true | :answer.type/text | `('Boolean membership for I', 'r0')` |
| false | :answer.type/text | `('Boolean membership for II', 'c8/c2')` |
| true | :answer.type/text | `('Boolean membership for II', 'c8/c2')` |
| false | :answer.type/text | `('Boolean membership for III', 'r1')` |
| true | :answer.type/text | `('Boolean membership for III', 'r1')` |
| false | :answer.type/text | `('Boolean membership for IV', 'c5')` |
| true | :answer.type/text | `('Boolean membership for IV', 'c5')` |

Original worked solution:

Let's use our formula to find an expression for the determinant in terms of $y:$

$$
\begin{aligned}|\begin{aligned}4 & 2 & 3 \\ -3y & -2 & 1 \\ 2 & y & -5\end{aligned}| & =4|\begin{aligned}-2 & 1 \\ y & -5\end{aligned}|-2|\begin{aligned}-3y & 1 \\ 2 & -5\end{aligned}|+3|\begin{aligned}-3y & -2 \\ 2 & y\end{aligned}| \\  & =4\cdot (10-y)-2\cdot (15y-2)+3\cdot (-3{y}^{2}+4) \\  & =40-4y-30y+4-9{y}^{2}+12 \\  & =-9{y}^{2}-34y+56\end{aligned}
$$

Since the determinant of the matrix is $81,$ we have:

$$
\begin{aligned}-9{y}^{2}-34y+56 & =81 \\ -9{y}^{2}-34y-25 & =0 \\ 9{y}^{2}+34y+25 & =0 \\ y & =\frac{-34\pm \sqrt{{34}^{2}-4\cdot 9\cdot 25}}{2\cdot 9} \\  & =\frac{-34\pm \sqrt{256}}{18} \\  & =\frac{-34\pm 16}{18} \\  & =\frac{-17\pm 8}{9}\end{aligned}
$$

Therefore, the solutions are $y=-\frac{25}{9}$ and $y=-1.$

### q-18271 — linear_named_determinant_radio

**Original prompt**

Given that
$A=[\begin{aligned}-k & 0 & -3 \\ 1 & 3 & -1 \\ 2k & 0 & 1\end{aligned}]$
and $det(A)=-30,$ find the value of $k.$

Coefficients: `{"constants": [0, 0, -3, 1, 3, -1, 0, 0, 1], "linear": [-1, 0, 0, 0, 0, 0, 2, 0, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": -30}`. Fields: `selection`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| 3 | :answer.type/math | `('c4',)` |
| 1 | :answer.type/math | `('c3',)` |
| 2 | :answer.type/math | `('-r0',)` |
| -3 | :answer.type/math | `('-c4',)` |
| -2 | :answer.type/math | `('correct',)` |

Original worked solution:

Let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}\text{det}(A) & =|\begin{aligned}-k & 0 & -3 \\ 1 & 3 & -1 \\ 2k & 0 & 1\end{aligned}| \\  & =-k|\begin{aligned}3 & -1 \\ 0 & 1\end{aligned}|-0|\begin{aligned}1 & -1 \\ 2k & 1\end{aligned}|-3|\begin{aligned}1 & 3 \\ 2k & 0\end{aligned}| \\  & =-k\cdot 3+0-3\cdot (-6k) \\  & =-3k+18k \\  & =15k\end{aligned}
$$

Since the determinant of the matrix is $-30,$ we have:

$$
\begin{aligned}15k & =-30 \\ k & =-2\end{aligned}
$$

### q-18272 — quadratic_named_determinant_checkbox

**Original prompt**

Given that $M=[\begin{aligned}0 & -3 & 2 \\ 1 & p & 0 \\ p-3 & 0 & -1\end{aligned}]$ and $det(M)=-23,$ find all the possible values of $p.$

Select all that apply. If none apply, leave all boxes unchecked.

- **I.** $p=-2$
- **II.** $p=2$
- **III.** $p=4$
- **IV.** $p=5$

Coefficients: `{"constants": [0, -3, 2, 1, 0, 0, -3, 0, -1], "linear": [0, 0, 0, 0, 1, 0, 1, 0, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": -23}`. Fields: `I, II, III, IV`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| false | :answer.type/text | `('Boolean membership for I', 'r0')` |
| true | :answer.type/text | `('Boolean membership for I', 'r0')` |
| false | :answer.type/text | `('Boolean membership for II', '-r0')` |
| true | :answer.type/text | `('Boolean membership for II', '-r0')` |
| false | :answer.type/text | `('Boolean membership for III', 'c2*c2')` |
| true | :answer.type/text | `('Boolean membership for III', 'c2*c2')` |
| false | :answer.type/text | `('Boolean membership for IV', 'r1')` |
| true | :answer.type/text | `('Boolean membership for IV', 'r1')` |

Original worked solution:

Let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}\text{det}(M) & =|\begin{aligned}0 & -3 & 2 \\ 1 & p & 0 \\ p-3 & 0 & -1\end{aligned}| \\  & =0|\begin{aligned}p & 0 \\ 0 & -1\end{aligned}|-(-3)|\begin{aligned}1 & 0 \\ p-3 & -1\end{aligned}|+2|\begin{aligned}1 & p \\ p-3 & 0\end{aligned}| \\  & =0+3\cdot (-1)+2\cdot (3p-{p}^{2}) \\  & =-3-2{p}^{2}+6p \\  & =-2{p}^{2}+6p-3\end{aligned}
$$

Since the determinant of the matrix is $-23,$ we have:

$$
\begin{aligned}-2{p}^{2}+6p-3 & =-23 \\ 2{p}^{2}-6p-20 & =0 \\ {p}^{2}-3p-10 & =0 \\ p & =\frac{-(-3)\pm \sqrt{(-3)^{2}-4\cdot 1\cdot (-10)}}{2\cdot 1} \\  & =\frac{3\pm \sqrt{49}}{2} \\  & =\frac{3\pm 7}{2}\end{aligned}
$$

Therefore,  the solutions are $p=-2$ and $p=5.$

### q-280403 — linear_named_determinant_blank

**Original prompt**

Given that $A=[\begin{aligned}2 & 1 & 0 \\ 3 & x & 4 \\ -2 & 5 & 1\end{aligned}]$ and $det(A)=37$, find the value of $x.$

$x=$
{{field-1}}

Coefficients: `{"constants": [2, 1, 0, 3, 0, 4, -2, 5, 1], "linear": [0, 0, 0, 0, 1, 0, 0, 0, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 37}`. Fields: `field-1`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| 44 | :answer.type/math | `('ascending root field-1',)` |

Original worked solution:

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}\text{det}(F) & =|\begin{aligned}2 & 1 & 0 \\ 3 & x & 4 \\ -2 & 5 & 1\end{aligned}| \\  & =2|\begin{aligned}x & 4 \\ 5 & 1\end{aligned}|-1|\begin{aligned}3 & 4 \\ -2 & 1\end{aligned}|+0|\begin{aligned}3 & x \\ -2 & 5\end{aligned}| \\  & =2(x\cdot 1-4\cdot 5)-(3\cdot 1-4\cdot (-2)) \\  & =2(x-20)-(3+8) \\  & =2x-40-11 \\  & =2x-51\end{aligned}
$$

Since the determinant of the matrix is $37,$ we have

$$
\begin{aligned}2x-51 & =37 \\ 2x & =88 \\ x & =44.\end{aligned}
$$

### q-280404 — linear_singular_blank

**Original prompt**

Find the possible values of the constant $k$ given that the matrix $[\begin{aligned}k+1 & 2k & 3 \\ 0 & 5 & 0 \\ -2 & k & 1\end{aligned}]$ is singular.

$k=$
{{field-1}}

Coefficients: `{"constants": [1, 0, 3, 0, 5, 0, -2, 0, 1], "linear": [1, 2, 0, 0, 0, 0, 0, 1, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 0}`. Fields: `field-1`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| -7 | :answer.type/math | `('ascending root field-1',)` |

Original worked solution:

Let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}det & =|\begin{aligned}k+1 & 2k & 3 \\ 0 & 5 & 0 \\ -2 & k & 1\end{aligned}| \\  & =(k+1)|\begin{aligned}5 & 0 \\ k & 1\end{aligned}|-2k|\begin{aligned}0 & 0 \\ -2 & 1\end{aligned}|+3|\begin{aligned}0 & 5 \\ -2 & k\end{aligned}| \\  & =(k+1)(5\cdot 1-0\cdot k)-2k(0\cdot 1-0\cdot -2)+3(0\cdot k-5\cdot (-2)) \\  & =(k+1)(5)-2k(0)+3(10) \\  & =5k+5+30 \\  & =5k+35\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have

$$
\begin{aligned}5k+35 & =0 \\ 5k & =-35 \\ k & =-7.\end{aligned}
$$

### q-280519 — linear_singular_blank

**Original prompt**

Given that $G=[\begin{aligned}x & 2x-1 & 6 \\ 0 & 3 & 0 \\ -1 & x+1 & -4\end{aligned}]$ is singular, find the value of $x.$

$x=$
{{field-1}}

Coefficients: `{"constants": [0, -1, 6, 0, 3, 0, -1, 1, -4], "linear": [1, 2, 0, 0, 0, 0, 0, 1, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 0}`. Fields: `field-1`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| \frac{3}{2} | :answer.type/math | `('ascending root field-1',)` |

Original worked solution:

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}det & =|\begin{aligned}x & 2x-1 & 6 \\ 0 & 3 & 0 \\ -1 & x+1 & -4\end{aligned}| \\  & =x|\begin{aligned}3 & 0 \\ x+1 & -4\end{aligned}|-(2x-1)|\begin{aligned}0 & 0 \\ -1 & -4\end{aligned}|+6|\begin{aligned}0 & 3 \\ -1 & x+1\end{aligned}| \\  & =x(3\cdot (-4)-0\cdot (x+1))-(2x-1)(0)+6(0\cdot (x+1)-3\cdot (-1)) \\  & =x(-12)+0+6(3) \\  & =-12x+18\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have

$$
\begin{aligned}-12x+18 & =0 \\ -12x & =-18 \\ x & =\frac{3}{2}.\end{aligned}
$$

### q-280540 — quadratic_square_determinant_blank

**Original prompt**

Given that the determinant of $[\begin{aligned}{x}^{2}-2 & 3 & 0 \\ x & -2 & -1 \\ 1 & 4 & 0\end{aligned}]$ is $32$, find all the possible values of $x$ **in ascending order**.

In ascending order, $x=$
{{field-1}} and $x=$
{{field-2}}.

Coefficients: `{"constants": [-2, 3, 0, 0, -2, -1, 1, 4, 0], "linear": [0, 0, 0, 1, 0, 0, 0, 0, 0], "quadratic": [1, 0, 0, 0, 0, 0, 0, 0, 0], "target": 32}`. Fields: `field-2, field-1`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| \frac{\sqrt{43}}{2} | :answer.type/math | `('ascending root field-2',)` |
| -\frac{\sqrt{43}}{2} | :answer.type/math | `('ascending root field-1',)` |

Original worked solution:

Let’s use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}det(A) & =|\begin{aligned}{x}^{2}-2 & 3 & 0 \\ x & -2 & -1 \\ 1 & 4 & 0\end{aligned}| \\  & =({x}^{2}-2)|\begin{aligned}-2 & -1 \\ 4 & 0\end{aligned}|-3|\begin{aligned}x & -1 \\ 1 & 0\end{aligned}|+0 \\  & =({x}^{2}-2)(-2\cdot 0-(-1)(4))-3(x\cdot 0-(-1)(1)) \\  & =({x}^{2}-2)(4)-3(1) \\  & =4{x}^{2}-8-3 \\  & =4{x}^{2}-11\end{aligned}
$$

Since the determinant of the matrix is $32$, we have

$$
\begin{aligned}4{x}^{2}-11 & =32 \\ 4{x}^{2} & =43 \\ {x}^{2} & =\frac{43}{4} \\ x & =\pm \sqrt{\frac{43}{4}} \\  & =\pm \frac{\sqrt{43}}{2}\end{aligned}
$$

Therefore, **in ascending order**, the solutions are $x=-\frac{\sqrt{43}}{2}$ and $x=\frac{\sqrt{43}}{2}.$

### q-280541 — quadratic_determinant_blank

**Original prompt**

Given that the determinant of $[\begin{aligned}x & 2x & 5 \\ 3 & x & 4 \\ 7 & 1 & 2\end{aligned}]$ is $40$, find all the possible values of $x$ **in ascending order**.

In ascending order, $x=$
{{field-1}} and $x=$
{{field-2}}.

Coefficients: `{"constants": [0, 0, 5, 3, 0, 4, 7, 1, 2], "linear": [1, 2, 0, 0, 1, 0, 0, 0, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 40}`. Fields: `field-2, field-1`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| \frac{5}{2} | :answer.type/math | `('ascending root field-2',)` |
| -5 | :answer.type/math | `('ascending root field-1',)` |

Original worked solution:

Let’s use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}det(A) & =|\begin{aligned}x & 2x & 5 \\ 3 & x & 4 \\ 7 & 1 & 2\end{aligned}| \\  & =x|\begin{aligned}x & 4 \\ 1 & 2\end{aligned}|-2x|\begin{aligned}3 & 4 \\ 7 & 2\end{aligned}|+5|\begin{aligned}3 & x \\ 7 & 1\end{aligned}| \\  & =x(2x-4)-2x(3\cdot 2-4\cdot 7)+5(3-7x) \\  & =x(2x-4)-2x(-22)+15-35x \\  & =2{x}^{2}-4x+44x+15-35x \\  & =2{x}^{2}+5x+15\end{aligned}
$$

Since the determinant of the matrix is $40$, we have

$$
\begin{aligned}2{x}^{2}+5x+15 & =40 \\ 2{x}^{2}+5x-25 & =0 \\ x & =\frac{-5\pm \sqrt{{5}^{2}-4(2)(-25)}}{2(2)} \\ x & =\frac{-5+\sqrt{225}}{4} \\  & =\frac{-5\pm 15}{4}.\end{aligned}
$$

Therefore, **in ascending order**, the solutions are $x=-5$ and $x=\frac{5}{2}.$

### q-9911 — quadratic_singular_checkbox

**Original prompt**

Find the possible values of the constant $k$ given that the matrix
$[\begin{aligned}1 & -1 & k \\ 1 & k & -k \\ 5 & k & k\end{aligned}]$ is singular.

Select all that apply. If none apply, leave all boxes unchecked.

- **I.** $k=-3$
- **II.** $k=0$
- **III.** $k=3$

Coefficients: `{"constants": [1, -1, 0, 1, 0, 0, 5, 0, 0], "linear": [0, 0, 1, 0, 1, -1, 0, 1, 1], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 0}`. Fields: `I, II, III`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| false | :answer.type/text | `('Boolean membership for I', '-r1')` |
| true | :answer.type/text | `('Boolean membership for I', '-r1')` |
| false | :answer.type/text | `('Boolean membership for II', 'r0')` |
| true | :answer.type/text | `('Boolean membership for II', 'r0')` |
| false | :answer.type/text | `('Boolean membership for III', 'r1')` |
| true | :answer.type/text | `('Boolean membership for III', 'r1')` |

Original worked solution:

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}1 & -1 & k \\ 1 & k & -k \\ 5 & k & k\end{aligned}| & =1|\begin{aligned}k & -k \\ k & k\end{aligned}|-(-1)|\begin{aligned}1 & -k \\ 5 & k\end{aligned}|+k|\begin{aligned}1 & k \\ 5 & k\end{aligned}| \\  & =({k}^{2}+{k}^{2})+(k+5k)+k(k-5k) \\  & =2{k}^{2}+6k+k\cdot (-4k) \\  & =2{k}^{2}+6k-4{k}^{2} \\  & =-2{k}^{2}+6k\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}-2{k}^{2}+6k & =0 \\ k(-2k+6) & =0\end{aligned}
$$

Therefore, the solutions are $k=0$ and $k=3.$

### q-9961 — linear_determinant_radio

**Original prompt**

Given that the determinant of  $[\begin{aligned}1 & n & 0 \\ 1 & 2 & 0 \\ -1 & 1 & 2\end{aligned}]$ is $-6$, find the value of $n.$

Coefficients: `{"constants": [1, 0, 0, 1, 2, 0, -1, 1, 2], "linear": [0, 1, 0, 0, 0, 0, 0, 0, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": -6}`. Fields: `selection`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| 1 | :answer.type/math | `('c0',)` |
| Any real number | :answer.type/text | `('all',)` |
| 5 | :answer.type/math | `('correct',)` |
| -1 | :answer.type/math | `('c6',)` |
| 0 | :answer.type/math | `('0',)` |

Original worked solution:

Let's use our formula to find an expression for the determinant in terms of $n:$

$$
\begin{aligned}|\begin{aligned}1 & n & 0 \\ 1 & 2 & 0 \\ -1 & 1 & 2\end{aligned}| & =1|\begin{aligned}2 & 0 \\ 1 & 2\end{aligned}|-n|\begin{aligned}1 & 0 \\ -1 & 2\end{aligned}|+0|\begin{aligned}1 & 2 \\ -1 & 1\end{aligned}| \\  & =4-n\cdot 2+0 \\  & =4-2n\end{aligned}
$$

Since the determinant of the matrix is $-6,$ we have:

$$
\begin{aligned}4-2n & =-6 \\ -2n & =-10 \\ n & =5\end{aligned}
$$

### q-280402 — linear_named_determinant_blank

**Original prompt**

Given that $B=[\begin{aligned}3 & 0 & 2 \\ 1 & k+2 & -5 \\ 4 & -1 & 6\end{aligned}]$ and $det(B)=70$, find the value of $k.$

$k=$
{{field-1}}

Coefficients: `{"constants": [3, 0, 2, 1, 2, -5, 4, -1, 6], "linear": [0, 0, 0, 0, 1, 0, 0, 0, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 70}`. Fields: `field-1`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| \frac{67}{10} | :answer.type/math | `('ascending root field-1',)` |

Original worked solution:

Let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}\text{det}(B) & =|\begin{aligned}3 & 0 & 2 \\ 1 & k+2 & -5 \\ 4 & -1 & 6\end{aligned}| \\  & =3|\begin{aligned}k+2 & -5 \\ -1 & 6\end{aligned}|-0|\begin{aligned}1 & -5 \\ 4 & 6\end{aligned}|+2|\begin{aligned}1 & k+2 \\ 4 & -1\end{aligned}| \\  & =3(6\cdot (k+2)-(-5)(-1))+2(1\cdot (-1)-4\cdot (k+2)) \\  & =3(6k+12-5)+2(-1-4k-8) \\  & =3(6k+7)+2(-4k-9) \\  & =18k+21-8k-18 \\  & =10k+3\end{aligned}
$$

Since the determinant of the matrix is $70,$ we have

$$
\begin{aligned}10k+3 & =70 \\ 10k & =67 \\ k & =\frac{67}{10}.\end{aligned}
$$

### q-280543 — quadratic_singular_blank

**Original prompt**

Find, in **ascending order**, the values ​​of $x$ for which the following matrix is singular.

$$
A=[\begin{aligned}x+2 & 2x & 4 \\ 3 & x & x+1 \\ 1 & 0 & 3\end{aligned}]
$$

In ascending order, $x=$
{{field-1}} and $x=$
{{field-2}}.

Coefficients: `{"constants": [2, 0, 4, 3, 0, 1, 1, 0, 3], "linear": [1, 2, 0, 0, 1, 1, 0, 0, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 0}`. Fields: `field-1, field-2`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| 0 | :answer.type/math | `('ascending root field-1',)` |
| \frac{14}{5} | :answer.type/math | `('ascending root field-2',)` |

Original worked solution:

First, let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}x+2 & 2x & 4 \\ 3 & x & x+1 \\ 1 & 0 & 3\end{aligned}| & =(x+2)|\begin{aligned}x & x+1 \\ 0 & 3\end{aligned}|-2x|\begin{aligned}3 & x+1 \\ 1 & 3\end{aligned}|+4|\begin{aligned}3 & x \\ 1 & 0\end{aligned}| \\  & =(x+2)(3x)-2x(8-x)+4(-x) \\  & =3x(x+2)-2x(8-x)-4x \\  & =3{x}^{2}+6x-16x+2{x}^{2}-4x \\  & =5{x}^{2}-14x\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have
 

$$
\begin{aligned}5{x}^{2}-14x & =0 \\ x(5x-14) & =0 \\ x & =0\,\text{or}\,x=\frac{14}{5}.\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=0$ and $x=\frac{14}{5}.$

### q-9913 — quadratic_singular_checkbox

**Original prompt**

Find the possible values of the constant $k$ given that the matrix  $[\begin{aligned}k & 0 & 0 \\ 0 & 3 & 1 \\ 0 & 6 & k\end{aligned}]$ is singular.

Select all that apply. If none apply, leave all boxes unchecked.

- **I.** $k=-2$
- **II.** $k=0$
- **III.** $k=2$

Coefficients: `{"constants": [0, 0, 0, 0, 3, 1, 0, 6, 0], "linear": [1, 0, 0, 0, 0, 0, 0, 0, 1], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": 0}`. Fields: `I, II, III`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| false | :answer.type/text | `('Boolean membership for I', '-r1')` |
| true | :answer.type/text | `('Boolean membership for I', '-r1')` |
| false | :answer.type/text | `('Boolean membership for II', 'r0')` |
| true | :answer.type/text | `('Boolean membership for II', 'r0')` |
| false | :answer.type/text | `('Boolean membership for III', 'r1')` |
| true | :answer.type/text | `('Boolean membership for III', 'r1')` |

Original worked solution:

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}k & 0 & 0 \\ 0 & 3 & 1 \\ 0 & 6 & k\end{aligned}| & =k|\begin{aligned}3 & 1 \\ 6 & k\end{aligned}|+0|\begin{aligned}0 & 1 \\ 0 & k\end{aligned}|+0|\begin{aligned}0 & 3 \\ 0 & 6\end{aligned}| \\  & =k(3k-6)+0+0 \\  & =k(3k-6)\end{aligned}
$$

Since the matrix is singular, the determinant is $0.$ So,  we have:

 

$$
\begin{aligned}k(3k-6) & =0 \\ 3k(k-2) & =0 \\ k & =0,2\end{aligned}
$$

Therefore, the solutions are $k=0$ and $k=2.$

### q-128506 — quadratic_determinant_checkbox

**Original prompt**

Given that the determinant of
$[\begin{aligned}1 & 6 & m \\ m & 3 & 0 \\ 2 & 1 & 1\end{aligned}]$
is $-29$, find all the possible values of $m.$

Select all that apply. If none apply, leave all boxes unchecked.

- **I.** $m=-6$
- **II.** $m=-5$
- **III.** $m=1$
- **IV.** $m=3$
- **V.** $m=4$
- **VI.** $m=8$

Coefficients: `{"constants": [1, 6, 0, 0, 3, 0, 2, 1, 1], "linear": [0, 0, 1, 1, 0, 0, 0, 0, 0], "quadratic": [0, 0, 0, 0, 0, 0, 0, 0, 0], "target": -29}`. Fields: `I, II, III, IV, V, VI`.

| Original answer | Type | Parameterized recipe |
|---|---|---|
| false | :answer.type/text | `('Boolean membership for I', '-c1')` |
| true | :answer.type/text | `('Boolean membership for I', '-c1')` |
| false | :answer.type/text | `('Boolean membership for II', '-(c1-c0)')` |
| true | :answer.type/text | `('Boolean membership for II', '-(c1-c0)')` |
| false | :answer.type/text | `('Boolean membership for III', 'c0')` |
| true | :answer.type/text | `('Boolean membership for III', 'c0')` |
| false | :answer.type/text | `('Boolean membership for IV', 'c4')` |
| true | :answer.type/text | `('Boolean membership for IV', 'c4')` |
| false | :answer.type/text | `('Boolean membership for V', 'r0')` |
| true | :answer.type/text | `('Boolean membership for V', 'r0')` |
| false | :answer.type/text | `('Boolean membership for VI', 'r1')` |
| true | :answer.type/text | `('Boolean membership for VI', 'r1')` |

Original worked solution:

Let's use our formula to find an expression for the determinant in terms of $m:$

$$
\begin{aligned}|\begin{aligned}1 & 6 & m \\ m & 3 & 0 \\ 2 & 1 & 1\end{aligned}| & =1|\begin{aligned}3 & 0 \\ 1 & 1\end{aligned}|-6|\begin{aligned}m & 0 \\ 2 & 1\end{aligned}|+m|\begin{aligned}m & 3 \\ 2 & 1\end{aligned}| \\  & =(3-0)-6(m-0)+m(m-6) \\  & =3-6m+{m}^{2}-6m \\  & ={m}^{2}-12m+3\end{aligned}
$$

Since the determinant of the matrix is $-29,$ we have:

$$
\begin{aligned}{m}^{2}-12m+3 & =-29 \\ {m}^{2}-12m+32 & =0 \\ m & =\frac{-(-12)\pm \sqrt{{12}^{2}-4\cdot 1\cdot 32}}{2\cdot 1} \\  & =\frac{12\pm \sqrt{16}}{2} \\  & =\frac{12\pm 4}{2} \\  & =6\pm 2\end{aligned}
$$

Therefore, the solutions are $m=4$ and $m=8.$

## 5. Authored mixed hard extension

`mixed_singular_radio` / `authored:hard_mixed` is the default hard family. It is not included among the 24 observed matrix recipes or 12 source-template families. A candidate bank is chosen before the correct outcome; all five sets can be correct. Dense affine 3x3 matrices then realize the selected identity, linear, or quadratic equation. All variants share one prompt, one radio field, five text choices, and the same domain of a real variable. Generated source provenance records no replayed question IDs; q-130626 and q-9852 are references only. Difficulty is an authored assignment and is not independently calibrated by the original hard source.

Explicit q-130626 / q-9852 and their authored:q-* banks remain available for source-focused review. Their identity-only behavior does not describe default hard generation. The generated review includes one default example for each of the three outcome families.
