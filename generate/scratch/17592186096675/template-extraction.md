# Template extraction

Source basis 2517. Scope: 17592186096675.

Each family retains its source coefficient matrix, requested object, field contract, five-choice profile, and ordered row operations. Varying the right-hand sides keeps the same elimination workload. Fixed coefficients are a conservative sampling policy, not a mathematical necessity. No target positions vary.

For an invertible coefficient matrix A, sample an integer solution s and supply b=A s. Every displayed intermediate augmented matrix is [B | B s], with B taken from the source stage. The validator independently applies each printed operation to all four columns.

Choice-bank generalization: retain each complete source bank, with option recipe s + (original_option - original_solution). This is an explicitly inferred affine extension, not a claimed causal misconception. The observed additive offsets are retained exactly and never pooled across profiles. Each incorrect offset is nonzero and all offsets differ, so all five choices remain distinct and exactly one solves A s=b. No distractor feedback is added.

The homogeneous q-10636 retains b=0 and s=0; it has exactly one variant. Easy and Hard are not classified by the available source evidence.

No source practice question uses plots; matrices and equations are LaTeX, not mathematical diagrams. The canonical example images contain unchanged standalone math and are not used by the generator.

## q-20267

Response: ordered solution vector. Profile: q-20267. Plot rating: none.

Observed coefficient matrix: `[['1', '1', '1'], ['1', '2', '1'], ['1', '1', '2']]`; RHS: `['2', '0', '3']`; solution: `['3', '-2', '1']`.

Source prompt:

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+y+z &=2 \\ x+2y+z &=0 \\ x+y+2z &=3\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Source solution stages:

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 1 & 1 & 2 \\ 1 & 2 & 1 & 0 \\ 1 & 1 & 2 & 3\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 1 & 1 & 2 \\ 1 & 2 & 1 & 0 \\ 1 & 1 & 2 & 3\end{bmatrix} & {R}_{2} & :={R}_{2}-{R}_{1} \\  & ∼\begin{bmatrix}1 & 1 & 1 & 2 \\ 0 & 1 & 0 & -2 \\ 1 & 1 & 2 & 3\end{bmatrix} & {R}_{3} & :={R}_{3}-{R}_{1} \\  & ∼\begin{bmatrix}1 & 1 & 1 & 2 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 1\end{bmatrix} & {R}_{1} & :={R}_{1}-{R}_{3} \\  & ∼\begin{bmatrix}1 & 1 & 0 & 1 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 1\end{bmatrix} & {R}_{1} & :={R}_{1}-{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 3 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 1\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=3 \\ y &=-2 \\ z &=1.\end{aligned}\right.
$$

So, we have the solution $x=3$, $y=-2$, and $z=1.$ Or, in vector form, $⟨3,-2,1⟩.$

Complete source bank and exact option recipes are in template-extraction.json.

## q-10633

Response: ordered solution vector. Profile: q-10633. Plot rating: none.

Observed coefficient matrix: `[['1', '0', '1'], ['0', '2', '1'], ['-1', '2', '1']]`; RHS: `['2', '0', '0']`; solution: `['0', '-1', '2']`.

Source prompt:

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+z &=2 \\ 2y+z &=0 \\ -x+2y+z &=0\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Source solution stages:

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 0 & 1 & 2 \\ 0 & 2 & 1 & 0 \\ -1 & 2 & 1 & 0\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 0 & 1 & 2 \\ 0 & 2 & 1 & 0 \\ -1 & 2 & 1 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+{R}_{1} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 2 \\ 0 & 2 & 1 & 0 \\ 0 & 2 & 2 & 2\end{bmatrix} & {R}_{2} & :=\frac{1}{2}{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 2 \\ 0 & 1 & \frac{1}{2} & 0 \\ 0 & 2 & 2 & 2\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 2 \\ 0 & 1 & \frac{1}{2} & 0 \\ 0 & 0 & 1 & 2\end{bmatrix} & {R}_{2} & :={R}_{2}+(-\frac{1}{2}){R}_{3} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 2 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & 2\end{bmatrix} & {R}_{1} & :={R}_{1}+(-1){R}_{3} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & 2\end{bmatrix}.\end{aligned}
$$

The corresponding system is now  

$$
\left\{\begin{aligned}x &=0 \\ y &=-1 \\ z &=2.\end{aligned}\right.
$$

So, we have the solution $x=0$, $y=-1$, and $z=2.$ Or, in vector form $⟨0,-1,2⟩.$

Complete source bank and exact option recipes are in template-extraction.json.

## q-10636

Response: ordered solution vector. Profile: q-10636. Plot rating: none.

Observed coefficient matrix: `[['1', '2', '0'], ['-3', '-1', '5'], ['-2', '-4', '1']]`; RHS: `['0', '0', '0']`; solution: `['0', '0', '0']`.

Source prompt:

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+2y &=0 \\ -3x-y+5z &=0 \\ -2x-4y+z &=0\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Source solution stages:

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 2 & 0 & 0 \\ -3 & -1 & 5 & 0 \\ -2 & -4 & 1 & 0\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & 0 & 0 \\ -3 & -1 & 5 & 0 \\ -2 & -4 & 1 & 0\end{bmatrix} & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 0 & 0 \\ 0 & 5 & 5 & 0 \\ -2 & -4 & 1 & 0\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 0 & 0 \\ 0 & 5 & 5 & 0 \\ 0 & 0 & 1 & 0\end{bmatrix} & {R}_{2} & :=\frac{1}{5}{R}_{2} \\  & ∼\begin{bmatrix}1 & 2 & 0 & 0 \\ 0 & 1 & 1 & 0 \\ 0 & 0 & 1 & 0\end{bmatrix} & {R}_{2} & :={R}_{2}+(-1){R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0\end{bmatrix} & {R}_{2} & :={R}_{1}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=0 \\ y &=0 \\ z &=0.\end{aligned}\right.
$$

So, we have the solution $x=0$, $y=0$ and $z=0.$ Or, in vector form $⟨0,0,0⟩.$

Complete source bank and exact option recipes are in template-extraction.json.

## q-131603

Response: RREF augmented matrix. Profile: q-131603. Plot rating: none.

Observed coefficient matrix: `[['2', '-4', '7'], ['-1', '3', '-4'], ['1', '-2', '3']]`; RHS: `['-4', '5', '-1']`; solution: `['9', '2', '-2']`.

Source prompt:

Consider the following system of linear equations:

$$
\left\{\begin{aligned}2x-4y+7z &=-4 \\ -x+3y-4z &=5 \\ x-2y+3z &=-1\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

Source solution stages:

The augmented matrix for this system is

$$
M=\begin{bmatrix}2 & -4 & 7 & -4 \\ -1 & 3 & -4 & 5 \\ 1 & -2 & 3 & -1\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}2 & -4 & 7 & -4 \\ -1 & 3 & -4 & 5 \\ 1 & -2 & 3 & -1\end{bmatrix} &  & {R}_{1}↔{R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 3 & -1 \\ -1 & 3 & -4 & 5 \\ 2 & -4 & 7 & -4\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\begin{bmatrix}1 & -2 & 3 & -1 \\ 0 & 1 & -1 & 4 \\ 2 & -4 & 7 & -4\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\  & ∼\begin{bmatrix}1 & -2 & 3 & -1 \\ 0 & 1 & -1 & 4 \\ 0 & 0 & 1 & -2\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 3 & -1 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 1 & -2\end{bmatrix} & {R}_{1} & :={R}_{1}+(-3){R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 0 & 5 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 1 & -2\end{bmatrix} & {R}_{1} & :={R}_{1}+2{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 9 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 1 & -2\end{bmatrix}.\end{aligned}
$$

Complete source bank and exact option recipes are in template-extraction.json.

## q-131618

Response: ordered solution vector. Profile: q-131618. Plot rating: none.

Observed coefficient matrix: `[['1', '-1', '2'], ['2', '-1', '7'], ['1', '-1', '3']]`; RHS: `['5', '7', '5']`; solution: `['2', '-3', '0']`.

Source prompt:

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-y+2z &=5 \\ 2x-y+7z &=7 \\ x-y+3z &=5\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Source solution stages:

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & -1 & 2 & 5 \\ 2 & -1 & 7 & 7 \\ 1 & -1 & 3 & 5\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -1 & 2 & 5 \\ 2 & -1 & 7 & 7 \\ 1 & -1 & 3 & 5\end{bmatrix} & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\begin{bmatrix}1 & -1 & 2 & 5 \\ 0 & 1 & 3 & -3 \\ 1 & -1 & 3 & 5\end{bmatrix} & {R}_{3} & :={R}_{3}-{R}_{1} \\  & ∼\begin{bmatrix}1 & -1 & 2 & 5 \\ 0 & 1 & 3 & -3 \\ 0 & 0 & 1 & 0\end{bmatrix} & {R}_{2} & :={R}_{2}-3{R}_{3} \\  & ∼\begin{bmatrix}1 & -1 & 2 & 5 \\ 0 & 1 & 0 & -3 \\ 0 & 0 & 1 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}-2{R}_{3} \\  & ∼\begin{bmatrix}1 & -1 & 0 & 5 \\ 0 & 1 & 0 & -3 \\ 0 & 0 & 1 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}+{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 2 \\ 0 & 1 & 0 & -3 \\ 0 & 0 & 1 & 0\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=2 \\ y &=-3 \\ z &=0.\end{aligned}\right.
$$

So, we have the solution $x=2$, $y=-3$, and $z=0.$ Or, in vector form, $⟨2,-3,0⟩.$

Complete source bank and exact option recipes are in template-extraction.json.

## q-131620

Response: RREF augmented matrix. Profile: q-131620. Plot rating: none.

Observed coefficient matrix: `[['1', '-3', '1'], ['3', '-8', '5'], ['-2', '6', '-1']]`; RHS: `['4', '10', '-5']`; solution: `['-23', '-8', '3']`.

Source prompt:

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-3y+z &=4 \\ 3x-8y+5z &=10 \\ -2x+6y-z &=-5\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

Source solution stages:

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & -3 & 1 & 4 \\ 3 & -8 & 5 & 10 \\ -2 & 6 & -1 & -5\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -3 & 1 & 4 \\ 3 & -8 & 5 & 10 \\ -2 & 6 & -1 & -5\end{bmatrix} & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 1 & 4 \\ 0 & 1 & 2 & -2 \\ -2 & 6 & -1 & -5\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 1 & 4 \\ 0 & 1 & 2 & -2 \\ 0 & 0 & 1 & 3\end{bmatrix} & {R}_{2} & :={R}_{2}+(-2){R}_{3} \\  & ∼\begin{bmatrix}1 & -3 & 1 & 4 \\ 0 & 1 & 0 & -8 \\ 0 & 0 & 1 & 3\end{bmatrix} & {R}_{1} & :={R}_{1}-{R}_{3} \\  & ∼\begin{bmatrix}1 & -3 & 0 & 1 \\ 0 & 1 & 0 & -8 \\ 0 & 0 & 1 & 3\end{bmatrix} & {R}_{1} & :={R}_{1}+3{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -23 \\ 0 & 1 & 0 & -8 \\ 0 & 0 & 1 & 3\end{bmatrix}.\end{aligned}
$$

Complete source bank and exact option recipes are in template-extraction.json.

## q-131627

Response: ordered solution vector. Profile: q-131627. Plot rating: none.

Observed coefficient matrix: `[['1', '3', '2'], ['1', '4', '2'], ['-2', '-6', '-3']]`; RHS: `['-5', '-2', '8']`; solution: `['-10', '3', '-2']`.

Source prompt:

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+3y+2z &=-5 \\ x+4y+2z &=-2 \\ -2x-6y-3z &=8\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

Source solution stages:

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 3 & 2 & -5 \\ 1 & 4 & 2 & -2 \\ -2 & -6 & -3 & 8\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 3 & 2 & -5 \\ 1 & 4 & 2 & -2 \\ -2 & -6 & -3 & 8\end{bmatrix} & {R}_{2} & :={R}_{2}-{R}_{1} \\  & ∼\begin{bmatrix}1 & 3 & 2 & -5 \\ 0 & 1 & 0 & 3 \\ -2 & -6 & -3 & 8\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & 3 & 2 & -5 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & -2\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{3} \\  & ∼\begin{bmatrix}1 & 3 & 0 & -1 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & -2\end{bmatrix} & {R}_{1} & :={R}_{1}+(-3){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -10 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & -2\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=-10 \\ y &=3 \\ z &=-2.\end{aligned}\right.
$$

So, we have the solution $x=-10$, $y=3$, and $z=-2.$ Or, in vector form, $⟨-10,3,-2⟩.$

Complete source bank and exact option recipes are in template-extraction.json.

## q-74601

Response: RREF augmented matrix. Profile: q-74601. Plot rating: none.

Observed coefficient matrix: `[['1', '2', '-1'], ['-2', '-3', '2'], ['2', '3', '-1']]`; RHS: `['3', '0', '3']`; solution: `['-6', '6', '3']`.

Source prompt:

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+2y-z &=3 \\ -2x-3y+2z &=0 \\ 2x+3y-z &=3\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

Source solution stages:

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 2 & -1 & 3 \\ -2 & -3 & 2 & 0 \\ 2 & 3 & -1 & 3\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & -1 & 3 \\ -2 & -3 & 2 & 0 \\ 2 & 3 & -1 & 3\end{bmatrix} & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & -1 & 3 \\ 0 & 1 & 0 & 6 \\ 2 & 3 & -1 & 3\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & -1 & 3 \\ 0 & 1 & 0 & 6 \\ 0 & -1 & 1 & -3\end{bmatrix} & {R}_{3} & :={R}_{3}+{R}_{2} \\  & ∼\begin{bmatrix}1 & 2 & -1 & 3 \\ 0 & 1 & 0 & 6 \\ 0 & 0 & 1 & 3\end{bmatrix} & {R}_{1} & :={R}_{1}+{R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 0 & 6 \\ 0 & 1 & 0 & 6 \\ 0 & 0 & 1 & 3\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -6 \\ 0 & 1 & 0 & 6 \\ 0 & 0 & 1 & 3\end{bmatrix}.\end{aligned}
$$

Complete source bank and exact option recipes are in template-extraction.json.

## q-74603

Response: RREF augmented matrix. Profile: q-74603. Plot rating: none.

Observed coefficient matrix: `[['1', '-1', '2'], ['3', '-2', '6'], ['-2', '2', '-1']]`; RHS: `['0', '-1', '3']`; solution: `['-3', '-1', '1']`.

Source prompt:

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-y+2z &=0 \\ 3x-2y+6z &=-1 \\ -2x+2y-z &=3\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

Source solution stages:

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & -1 & 2 & 0 \\ 3 & -2 & 6 & -1 \\ -2 & 2 & -1 & 3\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -1 & 2 & 0 \\ 3 & -2 & 6 & -1 \\ -2 & 2 & -1 & 3\end{bmatrix} & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\begin{bmatrix}1 & -1 & 2 & 0 \\ 0 & 1 & 0 & -1 \\ -2 & 2 & -1 & 3\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & -1 & 2 & 0 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 3 & 3\end{bmatrix} & {R}_{3} & :=\frac{1}{3}{R}_{3} \\  & ∼\begin{bmatrix}1 & -1 & 2 & 0 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & 1\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{3} \\  & ∼\begin{bmatrix}1 & -1 & 0 & -2 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & 1\end{bmatrix} & {R}_{1} & :={R}_{1}+{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -3 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & 1\end{bmatrix}.\end{aligned}
$$

Complete source bank and exact option recipes are in template-extraction.json.

## q-10644

Response: RREF augmented matrix. Profile: q-10644. Plot rating: none.

Observed coefficient matrix: `[['3', '4', '-1'], ['1', '1', '0'], ['2', '2', '1']]`; RHS: `['11', '2', '-6']`; solution: `['7', '-5', '-10']`.

Source prompt:

Consider the following system of linear equations:

$$
\left\{\begin{aligned}3x+4y-z &=11 \\ x+y &=2 \\ 2x+2y+z &=-6\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

Source solution stages:

The augmented matrix for this system is

$$
M=\begin{bmatrix}3 & 4 & -1 & 11 \\ 1 & 1 & 0 & 2 \\ 2 & 2 & 1 & -6\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}3 & 4 & -1 & 11 \\ 1 & 1 & 0 & 2 \\ 2 & 2 & 1 & -6\end{bmatrix} & {R}_{1} & ↔{R}_{2} \\  & ∼\begin{bmatrix}1 & 1 & 0 & 2 \\ 3 & 4 & -1 & 11 \\ 2 & 2 & 1 & -6\end{bmatrix} & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\begin{bmatrix}1 & 1 & 0 & 2 \\ 0 & 1 & -1 & 5 \\ 2 & 2 & 1 & -6\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\  & ∼\begin{bmatrix}1 & 1 & 0 & 2 \\ 0 & 1 & -1 & 5 \\ 0 & 0 & 1 & -10\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{3} \\  & ∼\begin{bmatrix}1 & 1 & 0 & 2 \\ 0 & 1 & 0 & -5 \\ 0 & 0 & 1 & -10\end{bmatrix} & {R}_{1} & :={R}_{1}+(-1){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 7 \\ 0 & 1 & 0 & -5 \\ 0 & 0 & 1 & -10\end{bmatrix}.\end{aligned}
$$

Complete source bank and exact option recipes are in template-extraction.json.

## q-74604

Response: RREF augmented matrix. Profile: q-74604. Plot rating: none.

Observed coefficient matrix: `[['1', '-3', '0'], ['0', '1', '2'], ['5', '-7', '17']]`; RHS: `['1', '1', '7']`; solution: `['40', '13', '-6']`.

Source prompt:

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-3y &=1 \\ y+2z &=1 \\ 5x-7y+17z &=7\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

Source solution stages:

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & -3 & 0 & 1 \\ 0 & 1 & 2 & 1 \\ 5 & -7 & 17 & 7\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -3 & 0 & 1 \\ 0 & 1 & 2 & 1 \\ 5 & -7 & 17 & 7\end{bmatrix} & {R}_{3} & :={R}_{3}+(-5){R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 0 & 1 \\ 0 & 1 & 2 & 1 \\ 0 & 8 & 17 & 2\end{bmatrix} & {R}_{3} & :={R}_{3}+(-8){R}_{2} \\  & ∼\begin{bmatrix}1 & -3 & 0 & 1 \\ 0 & 1 & 2 & 1 \\ 0 & 0 & 1 & -6\end{bmatrix} & {R}_{2} & :={R}_{2}+(-2){R}_{3} \\  & ∼\begin{bmatrix}1 & -3 & 0 & 1 \\ 0 & 1 & 0 & 13 \\ 0 & 0 & 1 & -6\end{bmatrix} & {R}_{1} & :={R}_{1}+3{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 40 \\ 0 & 1 & 0 & 13 \\ 0 & 0 & 1 & -6\end{bmatrix}.\end{aligned}
$$

Complete source bank and exact option recipes are in template-extraction.json.
