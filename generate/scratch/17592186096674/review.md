## q-131586 original

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+3z &=1 \\ y-2z &=-1 \\ z &=2\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 0 & 3 & 1 \\ 0 & 1 & -2 & -1 \\ 0 & 0 & 1 & 2\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 0 & 3 & 1 \\ 0 & 1 & -2 & -1 \\ 0 & 0 & 1 & 2\end{bmatrix} & {R}_{2} & :={R}_{2}+2{R}_{3} \\  & ∼\begin{bmatrix}1 & 0 & 3 & 1 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & 2\end{bmatrix} & {R}_{1} & :={R}_{1}+(-3){R}_{3} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -5 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & 2\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=-5 \\ y &=3 \\ z &=2.\end{aligned}\right.
$$

So, we have the solution $x=-5$, $y=3$, and $z=2.$

## Scale 3 variant

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+3z &=3 \\ y-2z &=-3 \\ z &=6\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

* $x=-15$, $y=9$, and $z=6$
- $x=-9$, $y=15$, and $z=6$
- $x=-15$, $y=-9$, and $z=6$
- $x=15$, $y=-9$, and $z=6$
- $x=9$, $y=-15$, and $z=6$

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 0 & 3 & 3 \\ 0 & 1 & -2 & -3 \\ 0 & 0 & 1 & 6\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 0 & 3 & 3 \\ 0 & 1 & -2 & -3 \\ 0 & 0 & 1 & 6\end{bmatrix} & {R}_{2} & :={R}_{2}+2{R}_{3} \\  & ∼\begin{bmatrix}1 & 0 & 3 & 3 \\ 0 & 1 & 0 & 9 \\ 0 & 0 & 1 & 6\end{bmatrix} & {R}_{1} & :={R}_{1}+(-3){R}_{3} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -15 \\ 0 & 1 & 0 & 9 \\ 0 & 0 & 1 & 6\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=-15 \\ y &=9 \\ z &=6.\end{aligned}\right.
$$

So, we have the solution $x=-15$, $y=9$, and $z=6.$

---

## q-131590 original

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+2y+3z &=-1 \\ y-z &=0 \\ z &=1\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 2 & 3 & -1 \\ 0 & 1 & -1 & 0 \\ 0 & 0 & 1 & 1\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & 3 & -1 \\ 0 & 1 & -1 & 0 \\ 0 & 0 & 1 & 1\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 3 & -1 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & 1\end{bmatrix} & {R}_{1} & :={R}_{1}+(-3){R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 0 & -4 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & 1\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -6 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & 1\end{bmatrix}.\end{aligned}
$$

## Scale 3 variant

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+2y+3z &=-3 \\ y-z &=0 \\ z &=3\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

- M∼\begin{bmatrix}1 & 0 & 0 & -6 \\ 0 & 1 & 0 & -3 \\ 0 & 0 & 1 & 3\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & -18 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 3\end{bmatrix}
* M∼\begin{bmatrix}1 & 0 & 0 & -18 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & 3\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & 18 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & 3\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & -6 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 3\end{bmatrix}

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 2 & 3 & -3 \\ 0 & 1 & -1 & 0 \\ 0 & 0 & 1 & 3\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & 3 & -3 \\ 0 & 1 & -1 & 0 \\ 0 & 0 & 1 & 3\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 3 & -3 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & 3\end{bmatrix} & {R}_{1} & :={R}_{1}+(-3){R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 0 & -12 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & 3\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -18 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & 3\end{bmatrix}.\end{aligned}
$$

---

## q-20590 original

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+y+2z &=0 \\ y+2z &=0 \\ z &=1\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 1 & 2 & 0 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 1 & 1\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 1 & 2 & 0 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 1 & 1\end{bmatrix} & {R}_{2} & :={R}_{2}+(-2){R}_{3} \\  & ∼\begin{bmatrix}1 & 1 & 2 & 0 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 1\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{3} \\  & ∼\begin{bmatrix}1 & 1 & 0 & -2 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 1\end{bmatrix} & {R}_{1} & :={R}_{1}+(-1){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 1\end{bmatrix}.\end{aligned}
$$

## Scale 3 variant

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+y+2z &=0 \\ y+2z &=0 \\ z &=3\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

* M∼\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & -6 \\ 0 & 0 & 1 & 3\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 6 \\ 0 & 0 & 1 & 3\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & -6 \\ 0 & 0 & 1 & -3\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & -9 \\ 0 & 0 & 1 & 12\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & 3 \\ 0 & 1 & 0 & -6 \\ 0 & 0 & 1 & 3\end{bmatrix}

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 1 & 2 & 0 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 1 & 3\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 1 & 2 & 0 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 1 & 3\end{bmatrix} & {R}_{2} & :={R}_{2}+(-2){R}_{3} \\  & ∼\begin{bmatrix}1 & 1 & 2 & 0 \\ 0 & 1 & 0 & -6 \\ 0 & 0 & 1 & 3\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{3} \\  & ∼\begin{bmatrix}1 & 1 & 0 & -6 \\ 0 & 1 & 0 & -6 \\ 0 & 0 & 1 & 3\end{bmatrix} & {R}_{1} & :={R}_{1}+(-1){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & -6 \\ 0 & 0 & 1 & 3\end{bmatrix}.\end{aligned}
$$

---

## q-20591 original

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+3y+4z &=-6 \\ y+z &=-1 \\ z &=-2\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 3 & 4 & -6 \\ 0 & 1 & 1 & -1 \\ 0 & 0 & 1 & -2\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 3 & 4 & -6 \\ 0 & 1 & 1 & -1 \\ 0 & 0 & 1 & -2\end{bmatrix} & {R}_{2} & :={R}_{2}+(-1){R}_{3} \\  & ∼\begin{bmatrix}1 & 3 & 4 & -6 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & -2\end{bmatrix} & {R}_{1} & :={R}_{1}+(-4){R}_{3} \\  & ∼\begin{bmatrix}1 & 3 & 0 & 2 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & -2\end{bmatrix} & {R}_{1} & :={R}_{1}+(-3){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -1 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & -2\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=-1 \\ y &=1 \\ z &=-2.\end{aligned}\right.
$$

So, we have the solution $x=-1$, $y=1$, and $z=-2.$ In vector form $⟨-1,1,-2⟩.$

## Scale 3 variant

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+3y+4z &=-18 \\ y+z &=-3 \\ z &=-6\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

- ⟨3,3,-6⟩
- ⟨-3,3,6⟩
- ⟨-3,6,-6⟩
* ⟨-3,3,-6⟩
- ⟨-3,0,-6⟩

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 3 & 4 & -18 \\ 0 & 1 & 1 & -3 \\ 0 & 0 & 1 & -6\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 3 & 4 & -18 \\ 0 & 1 & 1 & -3 \\ 0 & 0 & 1 & -6\end{bmatrix} & {R}_{2} & :={R}_{2}+(-1){R}_{3} \\  & ∼\begin{bmatrix}1 & 3 & 4 & -18 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & -6\end{bmatrix} & {R}_{1} & :={R}_{1}+(-4){R}_{3} \\  & ∼\begin{bmatrix}1 & 3 & 0 & 6 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & -6\end{bmatrix} & {R}_{1} & :={R}_{1}+(-3){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -3 \\ 0 & 1 & 0 & 3 \\ 0 & 0 & 1 & -6\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=-3 \\ y &=3 \\ z &=-6.\end{aligned}\right.
$$

So, we have the solution $x=-3$, $y=3$, and $z=-6.$ In vector form $⟨-3,3,-6⟩.$

---

## q-20593 original

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+5y-2z &=1 \\ y+3z &=0 \\ z &=1\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 5 & -2 & 1 \\ 0 & 1 & 3 & 0 \\ 0 & 0 & 1 & 1\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 5 & -2 & 1 \\ 0 & 1 & 3 & 0 \\ 0 & 0 & 1 & 1\end{bmatrix} & {R}_{2} & :={R}_{2}+(-3){R}_{3} \\  & ∼\begin{bmatrix}1 & 5 & -2 & 1 \\ 0 & 1 & 0 & -3 \\ 0 & 0 & 1 & 1\end{bmatrix} & {R}_{1} & :={R}_{1}+2{R}_{3} \\  & ∼\begin{bmatrix}1 & 5 & 0 & 3 \\ 0 & 1 & 0 & -3 \\ 0 & 0 & 1 & 1\end{bmatrix} & {R}_{1} & :={R}_{1}+(-5){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 18 \\ 0 & 1 & 0 & -3 \\ 0 & 0 & 1 & 1\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=18 \\ y &=-3 \\ z &=1.\end{aligned}\right.
$$

So, we have the solution $x=18$, $y=-3$, and $z=1.$ Or, in vector form $⟨18,-3,1⟩.$

## Scale 3 variant

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+5y-2z &=3 \\ y+3z &=0 \\ z &=3\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

- ⟨54,-6,-3⟩
- ⟨33,-9,-3⟩
- ⟨54,9,3⟩
- ⟨33,-9,6⟩
* ⟨54,-9,3⟩

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 5 & -2 & 3 \\ 0 & 1 & 3 & 0 \\ 0 & 0 & 1 & 3\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 5 & -2 & 3 \\ 0 & 1 & 3 & 0 \\ 0 & 0 & 1 & 3\end{bmatrix} & {R}_{2} & :={R}_{2}+(-3){R}_{3} \\  & ∼\begin{bmatrix}1 & 5 & -2 & 3 \\ 0 & 1 & 0 & -9 \\ 0 & 0 & 1 & 3\end{bmatrix} & {R}_{1} & :={R}_{1}+2{R}_{3} \\  & ∼\begin{bmatrix}1 & 5 & 0 & 9 \\ 0 & 1 & 0 & -9 \\ 0 & 0 & 1 & 3\end{bmatrix} & {R}_{1} & :={R}_{1}+(-5){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 54 \\ 0 & 1 & 0 & -9 \\ 0 & 0 & 1 & 3\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=54 \\ y &=-9 \\ z &=3.\end{aligned}\right.
$$

So, we have the solution $x=54$, $y=-9$, and $z=3.$ Or, in vector form $⟨54,-9,3⟩.$

---

## q-20594 original

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+2y+z &=14 \\ y+z &=8 \\ z &=4\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 2 & 1 & 14 \\ 0 & 1 & 1 & 8 \\ 0 & 0 & 1 & 4\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & 1 & 14 \\ 0 & 1 & 1 & 8 \\ 0 & 0 & 1 & 4\end{bmatrix} & {R}_{2} & :={R}_{2}+(-1){R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 1 & 14 \\ 0 & 1 & 0 & 4 \\ 0 & 0 & 1 & 4\end{bmatrix} & {R}_{1} & :={R}_{1}+(-1){R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 0 & 10 \\ 0 & 1 & 0 & 4 \\ 0 & 0 & 1 & 4\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 2 \\ 0 & 1 & 0 & 4 \\ 0 & 0 & 1 & 4\end{bmatrix}.\end{aligned}
$$

## Scale 3 variant

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+2y+z &=42 \\ y+z &=24 \\ z &=12\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

- M∼\begin{bmatrix}1 & 0 & 0 & -6 \\ 0 & 1 & 0 & 12 \\ 0 & 0 & 1 & 9\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & 6 \\ 0 & 1 & 0 & -12 \\ 0 & 0 & 1 & 12\end{bmatrix}
* M∼\begin{bmatrix}1 & 0 & 0 & 6 \\ 0 & 1 & 0 & 12 \\ 0 & 0 & 1 & 12\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & 6 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & -9\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & 3 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 12\end{bmatrix}

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 2 & 1 & 42 \\ 0 & 1 & 1 & 24 \\ 0 & 0 & 1 & 12\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & 1 & 42 \\ 0 & 1 & 1 & 24 \\ 0 & 0 & 1 & 12\end{bmatrix} & {R}_{2} & :={R}_{2}+(-1){R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 1 & 42 \\ 0 & 1 & 0 & 12 \\ 0 & 0 & 1 & 12\end{bmatrix} & {R}_{1} & :={R}_{1}+(-1){R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 0 & 30 \\ 0 & 1 & 0 & 12 \\ 0 & 0 & 1 & 12\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 6 \\ 0 & 1 & 0 & 12 \\ 0 & 0 & 1 & 12\end{bmatrix}.\end{aligned}
$$

---

## q-20597 original

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-2y-3z &=0 \\ y+2z &=0 \\ z &=-2\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & -2 & -3 & 0 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 1 & -2\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -2 & -3 & 0 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 1 & -2\end{bmatrix} & {R}_{2} & :={R}_{2}+(-2){R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & -3 & 0 \\ 0 & 1 & 0 & 4 \\ 0 & 0 & 1 & -2\end{bmatrix} & {R}_{1} & :={R}_{1}+3{R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 0 & -6 \\ 0 & 1 & 0 & 4 \\ 0 & 0 & 1 & -2\end{bmatrix} & {R}_{1} & :={R}_{1}+2{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 2 \\ 0 & 1 & 0 & 4 \\ 0 & 0 & 1 & -2\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=2 \\ y &=4 \\ z &=-2.\end{aligned}\right.
$$

So, we have he solution $x=2$, $y=4$ and $z=-2.$ Or, in vector form $⟨2,4,-2⟩.$

## Scale 3 variant

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-2y-3z &=0 \\ y+2z &=0 \\ z &=-6\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

- ⟨-6,-12,-6⟩
- ⟨6,12,6⟩
- ⟨3,12,-6⟩
* ⟨6,12,-6⟩
- ⟨6,3,-6⟩

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & -2 & -3 & 0 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 1 & -6\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -2 & -3 & 0 \\ 0 & 1 & 2 & 0 \\ 0 & 0 & 1 & -6\end{bmatrix} & {R}_{2} & :={R}_{2}+(-2){R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & -3 & 0 \\ 0 & 1 & 0 & 12 \\ 0 & 0 & 1 & -6\end{bmatrix} & {R}_{1} & :={R}_{1}+3{R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 0 & -18 \\ 0 & 1 & 0 & 12 \\ 0 & 0 & 1 & -6\end{bmatrix} & {R}_{1} & :={R}_{1}+2{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 6 \\ 0 & 1 & 0 & 12 \\ 0 & 0 & 1 & -6\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=6 \\ y &=12 \\ z &=-6.\end{aligned}\right.
$$

So, we have he solution $x=6$, $y=12$ and $z=-6.$ Or, in vector form $⟨6,12,-6⟩.$

---

## q-20599 original

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+2y+8z &=90 \\ y+4z &=50 \\ z &=10\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 2 & 8 & 90 \\ 0 & 1 & 4 & 50 \\ 0 & 0 & 1 & 10\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & 8 & 90 \\ 0 & 1 & 4 & 50 \\ 0 & 0 & 1 & 10\end{bmatrix} & {R}_{2} & :={R}_{2}+(-4){R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 8 & 90 \\ 0 & 1 & 0 & 10 \\ 0 & 0 & 1 & 10\end{bmatrix} & {R}_{1} & :={R}_{1}+(-8){R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 0 & 10 \\ 0 & 1 & 0 & 10 \\ 0 & 0 & 1 & 10\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -10 \\ 0 & 1 & 0 & 10 \\ 0 & 0 & 1 & 10\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=-10 \\ y &=10 \\ z &=10.\end{aligned}\right.
$$

So, we have the solution $x=-10$, $y=10$, and $z=10.$ Or, in vector form $⟨-10,10,10⟩.$

## Scale 3 variant

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+2y+8z &=270 \\ y+4z &=150 \\ z &=30\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

- ⟨30,-30,-30⟩
- ⟨30,30,-30⟩
* ⟨-30,30,30⟩
- ⟨30,30,30⟩
- ⟨-30,-30,30⟩

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 2 & 8 & 270 \\ 0 & 1 & 4 & 150 \\ 0 & 0 & 1 & 30\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 2 & 8 & 270 \\ 0 & 1 & 4 & 150 \\ 0 & 0 & 1 & 30\end{bmatrix} & {R}_{2} & :={R}_{2}+(-4){R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 8 & 270 \\ 0 & 1 & 0 & 30 \\ 0 & 0 & 1 & 30\end{bmatrix} & {R}_{1} & :={R}_{1}+(-8){R}_{3} \\  & ∼\begin{bmatrix}1 & 2 & 0 & 30 \\ 0 & 1 & 0 & 30 \\ 0 & 0 & 1 & 30\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & -30 \\ 0 & 1 & 0 & 30 \\ 0 & 0 & 1 & 30\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=-30 \\ y &=30 \\ z &=30.\end{aligned}\right.
$$

So, we have the solution $x=-30$, $y=30$, and $z=30.$ Or, in vector form $⟨-30,30,30⟩.$

---

## q-20600 original

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-2y+18z &=380 \\ y+9z &=190 \\ z &=19\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & -2 & 18 & 380 \\ 0 & 1 & 9 & 190 \\ 0 & 0 & 1 & 19\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -2 & 18 & 380 \\ 0 & 1 & 9 & 190 \\ 0 & 0 & 1 & 19\end{bmatrix} & {R}_{2} & :={R}_{2}+(-9){R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 18 & 380 \\ 0 & 1 & 0 & 19 \\ 0 & 0 & 1 & 19\end{bmatrix} & {R}_{1} & :={R}_{1}+(-18){R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 0 & 38 \\ 0 & 1 & 0 & 19 \\ 0 & 0 & 1 & 19\end{bmatrix} & {R}_{1} & :={R}_{1}+2{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 76 \\ 0 & 1 & 0 & 19 \\ 0 & 0 & 1 & 19\end{bmatrix}.\end{aligned}
$$

## Scale 3 variant

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x-2y+18z &=1140 \\ y+9z &=570 \\ z &=57\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

- M∼\begin{bmatrix}1 & 0 & 0 & 228 \\ 0 & 1 & 0 & 57 \\ 0 & 0 & 1 & -57\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & 228 \\ 0 & 1 & 0 & -57 \\ 0 & 0 & 1 & -57\end{bmatrix}
* M∼\begin{bmatrix}1 & 0 & 0 & 228 \\ 0 & 1 & 0 & 57 \\ 0 & 0 & 1 & 57\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & -228 \\ 0 & 1 & 0 & -57 \\ 0 & 0 & 1 & 57\end{bmatrix}
- M∼\begin{bmatrix}1 & 0 & 0 & -228 \\ 0 & 1 & 0 & 57 \\ 0 & 0 & 1 & -57\end{bmatrix}

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & -2 & 18 & 1140 \\ 0 & 1 & 9 & 570 \\ 0 & 0 & 1 & 57\end{bmatrix}.
$$

Notice that the matrix $M$ is already in row echelon form.

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & -2 & 18 & 1140 \\ 0 & 1 & 9 & 570 \\ 0 & 0 & 1 & 57\end{bmatrix} & {R}_{2} & :={R}_{2}+(-9){R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 18 & 1140 \\ 0 & 1 & 0 & 57 \\ 0 & 0 & 1 & 57\end{bmatrix} & {R}_{1} & :={R}_{1}+(-18){R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 0 & 114 \\ 0 & 1 & 0 & 57 \\ 0 & 0 & 1 & 57\end{bmatrix} & {R}_{1} & :={R}_{1}+2{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 228 \\ 0 & 1 & 0 & 57 \\ 0 & 0 & 1 & 57\end{bmatrix}.\end{aligned}
$$