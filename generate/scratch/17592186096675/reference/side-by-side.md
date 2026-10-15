## q-20267

### Source

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+y+z &=2 \\ x+2y+z &=0 \\ x+y+2z &=3\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

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

### Variant

Consider the following system of linear equations:

$$
\left\{\begin{aligned} & x + y + z=2 \\ & x + 2 y + z=-9 \\ & x + y + 2 z=6\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 1 & 1 & 2 \\ 1 & 2 & 1 & -9 \\ 1 & 1 & 2 & 6\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 1 & 1 & 2 \\ 1 & 2 & 1 & -9 \\ 1 & 1 & 2 & 6\end{bmatrix} & {R}_{2} & :={R}_{2}-{R}_{1} \\  & ∼\begin{bmatrix}1 & 1 & 1 & 2 \\ 0 & 1 & 0 & -11 \\ 1 & 1 & 2 & 6\end{bmatrix} & {R}_{3} & :={R}_{3}-{R}_{1} \\  & ∼\begin{bmatrix}1 & 1 & 1 & 2 \\ 0 & 1 & 0 & -11 \\ 0 & 0 & 1 & 4\end{bmatrix} & {R}_{1} & :={R}_{1}-{R}_{3} \\  & ∼\begin{bmatrix}1 & 1 & 0 & -2 \\ 0 & 1 & 0 & -11 \\ 0 & 0 & 1 & 4\end{bmatrix} & {R}_{1} & :={R}_{1}-{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 9 \\ 0 & 1 & 0 & -11 \\ 0 & 0 & 1 & 4\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=9 \\ y &=-11 \\ z &=4.\end{aligned}\right.
$$

So, we have the solution $x=9$, $y=-11$, and $z=4.$ Or, in vector form, $⟨9,-11,4⟩$.

## q-10633

### Source

Consider the following system of linear equations:

$$
\left\{\begin{aligned}x+z &=2 \\ 2y+z &=0 \\ -x+2y+z &=0\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

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

### Variant

Consider the following system of linear equations:

$$
\left\{\begin{aligned} & x + z=13 \\ & 2 y + z=-18 \\ & - x + 2 y + z=-27\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

The augmented matrix for this system is

$$
M=\begin{bmatrix}1 & 0 & 1 & 13 \\ 0 & 2 & 1 & -18 \\ -1 & 2 & 1 & -27\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}1 & 0 & 1 & 13 \\ 0 & 2 & 1 & -18 \\ -1 & 2 & 1 & -27\end{bmatrix} & {R}_{3} & :={R}_{3}+{R}_{1} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 13 \\ 0 & 2 & 1 & -18 \\ 0 & 2 & 2 & -14\end{bmatrix} & {R}_{2} & :=\frac{1}{2}{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 13 \\ 0 & 1 & \frac{1}{2} & -9 \\ 0 & 2 & 2 & -14\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 13 \\ 0 & 1 & \frac{1}{2} & -9 \\ 0 & 0 & 1 & 4\end{bmatrix} & {R}_{2} & :={R}_{2}+(-\frac{1}{2}){R}_{3} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 13 \\ 0 & 1 & 0 & -11 \\ 0 & 0 & 1 & 4\end{bmatrix} & {R}_{1} & :={R}_{1}+(-1){R}_{3} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 9 \\ 0 & 1 & 0 & -11 \\ 0 & 0 & 1 & 4\end{bmatrix}.\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x &=9 \\ y &=-11 \\ z &=4.\end{aligned}\right.
$$

So, we have the solution $x=9$, $y=-11$, and $z=4.$ Or, in vector form, $⟨9,-11,4⟩$.

## q-131603

### Source

Consider the following system of linear equations:

$$
\left\{\begin{aligned}2x-4y+7z &=-4 \\ -x+3y-4z &=5 \\ x-2y+3z &=-1\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

The augmented matrix for this system is

$$
M=\begin{bmatrix}2 & -4 & 7 & -4 \\ -1 & 3 & -4 & 5 \\ 1 & -2 & 3 & -1\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}2 & -4 & 7 & -4 \\ -1 & 3 & -4 & 5 \\ 1 & -2 & 3 & -1\end{bmatrix} &  & {R}_{1}↔{R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 3 & -1 \\ -1 & 3 & -4 & 5 \\ 2 & -4 & 7 & -4\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\begin{bmatrix}1 & -2 & 3 & -1 \\ 0 & 1 & -1 & 4 \\ 2 & -4 & 7 & -4\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\  & ∼\begin{bmatrix}1 & -2 & 3 & -1 \\ 0 & 1 & -1 & 4 \\ 0 & 0 & 1 & -2\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 3 & -1 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 1 & -2\end{bmatrix} & {R}_{1} & :={R}_{1}+(-3){R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 0 & 5 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 1 & -2\end{bmatrix} & {R}_{1} & :={R}_{1}+2{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 9 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 1 & -2\end{bmatrix}.\end{aligned}
$$

### Variant

Consider the following system of linear equations:

$$
\left\{\begin{aligned} & 2 x - 4 y + 7 z=90 \\ & - x + 3 y - 4 z=-58 \\ & x - 2 y + 3 z=43\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form.

The augmented matrix for this system is

$$
M=\begin{bmatrix}2 & -4 & 7 & 90 \\ -1 & 3 & -4 & -58 \\ 1 & -2 & 3 & 43\end{bmatrix}.
$$

Transforming $M$ to reduced row echelon form, we have

$$
\begin{aligned}M & ∼\begin{bmatrix}2 & -4 & 7 & 90 \\ -1 & 3 & -4 & -58 \\ 1 & -2 & 3 & 43\end{bmatrix} &  & {R}_{1}↔{R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 3 & 43 \\ -1 & 3 & -4 & -58 \\ 2 & -4 & 7 & 90\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\begin{bmatrix}1 & -2 & 3 & 43 \\ 0 & 1 & -1 & -15 \\ 2 & -4 & 7 & 90\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\  & ∼\begin{bmatrix}1 & -2 & 3 & 43 \\ 0 & 1 & -1 & -15 \\ 0 & 0 & 1 & 4\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 3 & 43 \\ 0 & 1 & 0 & -11 \\ 0 & 0 & 1 & 4\end{bmatrix} & {R}_{1} & :={R}_{1}+(-3){R}_{3} \\  & ∼\begin{bmatrix}1 & -2 & 0 & 31 \\ 0 & 1 & 0 & -11 \\ 0 & 0 & 1 & 4\end{bmatrix} & {R}_{1} & :={R}_{1}+2{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 0 & 9 \\ 0 & 1 & 0 & -11 \\ 0 & 0 & 1 & 4\end{bmatrix}.\end{aligned}
$$
