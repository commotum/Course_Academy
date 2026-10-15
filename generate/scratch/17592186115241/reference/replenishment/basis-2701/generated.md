Consider the system of linear equations

$$
\left\{\begin{aligned}2x-2y-2z &=-16 \\ 2x+y+7z &=-1 \\ 2x+4z &=-6.\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

- $\begin{bmatrix}-2z-3 \\ -3z+5 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}-3z+5 \\ -2z-3 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}-2z+3 \\ -3z+5 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}-2z-3 \\ 5 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}2z-3 \\ -3z+5 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$

The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}2 & -2 & -2 & -16 \\ 2 & 1 & 7 & -1 \\ 2 & 0 & 4 & -6\end{array}\right].
$$

Using the standard Gauss-Jordan method, we can reduce this matrix to reduced row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}2 & -2 & -2 & -16 \\ 2 & 1 & 7 & -1 \\ 2 & 0 & 4 & -6\end{array}\right] & {R}_{1}:=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & -1 & -8 \\ 2 & 1 & 7 & -1 \\ 2 & 0 & 4 & -6\end{array}\right] & {R}_{2}:={R}_{2}+(-2){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & -1 & -8 \\ 0 & 3 & 9 & 15 \\ 2 & 0 & 4 & -6\end{array}\right] & {R}_{2}:=\frac{1}{3}{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & -1 & -8 \\ 0 & 1 & 3 & 5 \\ 2 & 0 & 4 & -6\end{array}\right] & {R}_{3}:={R}_{3}+(-2){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & -1 & -8 \\ 0 & 1 & 3 & 5 \\ 0 & 2 & 6 & 10\end{array}\right] & {R}_{3}:={R}_{3}+(-2){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & -1 & -8 \\ 0 & 1 & 3 & 5 \\ 0 & 0 & 0 & 0\end{array}\right] & {R}_{1}:={R}_{1}+(1){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 2 & -3 \\ 0 & 1 & 3 & 5 \\ 0 & 0 & 0 & 0\end{array}\right]\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x+2z &=-3 \\ y+3z &=5.\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y$, and we have one free variable, $z$. That means we need to find $x$ and $y$ in terms of $z$.

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=-2z-3 \\ y &=-3z+5 \\ z &=z,\end{aligned}\right.
$$

where $z$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}-2z-3 \\ -3z+5 \\ z\end{bmatrix},\,z\in (-\infty ,\infty ).
$$

---

Consider the system of linear equations

$$
\left\{\begin{aligned}2x+2y+14z &=-6 \\ x+4y+16z &=-18 \\ -2x-4y-20z &=16.\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

- $\begin{bmatrix}-4z-2 \\ -3z-5 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}-4z+2 \\ -3z-5 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}-3z-5 \\ -4z+2 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}-4z+2 \\ -5 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}4z+2 \\ -3z-5 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$

The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}2 & 2 & 14 & -6 \\ 1 & 4 & 16 & -18 \\ -2 & -4 & -20 & 16\end{array}\right].
$$

Using the standard Gauss-Jordan method, we can reduce this matrix to reduced row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}2 & 2 & 14 & -6 \\ 1 & 4 & 16 & -18 \\ -2 & -4 & -20 & 16\end{array}\right] & {R}_{1}:=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 7 & -3 \\ 1 & 4 & 16 & -18 \\ -2 & -4 & -20 & 16\end{array}\right] & {R}_{2}:={R}_{2}+(-1){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 7 & -3 \\ 0 & 3 & 9 & -15 \\ -2 & -4 & -20 & 16\end{array}\right] & {R}_{2}:=\frac{1}{3}{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 7 & -3 \\ 0 & 1 & 3 & -5 \\ -2 & -4 & -20 & 16\end{array}\right] & {R}_{3}:={R}_{3}+(2){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 7 & -3 \\ 0 & 1 & 3 & -5 \\ 0 & -2 & -6 & 10\end{array}\right] & {R}_{3}:={R}_{3}+(2){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 7 & -3 \\ 0 & 1 & 3 & -5 \\ 0 & 0 & 0 & 0\end{array}\right] & {R}_{1}:={R}_{1}+(-1){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 4 & 2 \\ 0 & 1 & 3 & -5 \\ 0 & 0 & 0 & 0\end{array}\right]\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x+4z &=2 \\ y+3z &=-5.\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y$, and we have one free variable, $z$. That means we need to find $x$ and $y$ in terms of $z$.

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=-4z+2 \\ y &=-3z-5 \\ z &=z,\end{aligned}\right.
$$

where $z$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}-4z+2 \\ -3z-5 \\ z\end{bmatrix},\,z\in (-\infty ,\infty ).
$$

---

Consider the system of linear equations

$$
\left\{\begin{aligned}2x-2y+2z &=-4 \\ -2x+5y-14z &=22 \\ 2x-4y+10z &=-16.\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

- $\begin{bmatrix}3z+4 \\ 4z+6 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}3z+4 \\ 6 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}3z-4 \\ 4z+6 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}-3z+4 \\ 4z+6 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}4z+6 \\ 3z+4 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$

The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}2 & -2 & 2 & -4 \\ -2 & 5 & -14 & 22 \\ 2 & -4 & 10 & -16\end{array}\right].
$$

Using the standard Gauss-Jordan method, we can reduce this matrix to reduced row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}2 & -2 & 2 & -4 \\ -2 & 5 & -14 & 22 \\ 2 & -4 & 10 & -16\end{array}\right] & {R}_{1}:=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & -2 \\ -2 & 5 & -14 & 22 \\ 2 & -4 & 10 & -16\end{array}\right] & {R}_{2}:={R}_{2}+(2){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & -2 \\ 0 & 3 & -12 & 18 \\ 2 & -4 & 10 & -16\end{array}\right] & {R}_{2}:=\frac{1}{3}{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & -2 \\ 0 & 1 & -4 & 6 \\ 2 & -4 & 10 & -16\end{array}\right] & {R}_{3}:={R}_{3}+(-2){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & -2 \\ 0 & 1 & -4 & 6 \\ 0 & -2 & 8 & -12\end{array}\right] & {R}_{3}:={R}_{3}+(2){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & -2 \\ 0 & 1 & -4 & 6 \\ 0 & 0 & 0 & 0\end{array}\right] & {R}_{1}:={R}_{1}+(1){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & -3 & 4 \\ 0 & 1 & -4 & 6 \\ 0 & 0 & 0 & 0\end{array}\right]\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x-3z &=4 \\ y-4z &=6.\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y$, and we have one free variable, $z$. That means we need to find $x$ and $y$ in terms of $z$.

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=3z+4 \\ y &=4z+6 \\ z &=z,\end{aligned}\right.
$$

where $z$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}3z+4 \\ 4z+6 \\ z\end{bmatrix},\,z\in (-\infty ,\infty ).
$$

---

Consider the system of linear equations

$$
\left\{\begin{aligned}2x+2y+4z &=-16 \\ -2x+y+5z &=10 \\ -x-2y-5z &=10.\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

- $\begin{bmatrix}-z-6 \\ -3z-2 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}-3z-2 \\ z-6 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}z+6 \\ -3z-2 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}z-6 \\ -3z-2 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}z-6 \\ -2 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$

The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}2 & 2 & 4 & -16 \\ -2 & 1 & 5 & 10 \\ -1 & -2 & -5 & 10\end{array}\right].
$$

Using the standard Gauss-Jordan method, we can reduce this matrix to reduced row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}2 & 2 & 4 & -16 \\ -2 & 1 & 5 & 10 \\ -1 & -2 & -5 & 10\end{array}\right] & {R}_{1}:=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 2 & -8 \\ -2 & 1 & 5 & 10 \\ -1 & -2 & -5 & 10\end{array}\right] & {R}_{2}:={R}_{2}+(2){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 2 & -8 \\ 0 & 3 & 9 & -6 \\ -1 & -2 & -5 & 10\end{array}\right] & {R}_{2}:=\frac{1}{3}{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 2 & -8 \\ 0 & 1 & 3 & -2 \\ -1 & -2 & -5 & 10\end{array}\right] & {R}_{3}:={R}_{3}+(1){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 2 & -8 \\ 0 & 1 & 3 & -2 \\ 0 & -1 & -3 & 2\end{array}\right] & {R}_{3}:={R}_{3}+(1){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 2 & -8 \\ 0 & 1 & 3 & -2 \\ 0 & 0 & 0 & 0\end{array}\right] & {R}_{1}:={R}_{1}+(-1){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & -1 & -6 \\ 0 & 1 & 3 & -2 \\ 0 & 0 & 0 & 0\end{array}\right]\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x-z &=-6 \\ y+3z &=-2.\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y$, and we have one free variable, $z$. That means we need to find $x$ and $y$ in terms of $z$.

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=z-6 \\ y &=-3z-2 \\ z &=z,\end{aligned}\right.
$$

where $z$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}z-6 \\ -3z-2 \\ z\end{bmatrix},\,z\in (-\infty ,\infty ).
$$

---

Consider the system of linear equations

$$
\left\{\begin{aligned}2x-4y-8z &=-16 \\ 2x-y+4z &=-10 \\ 2x-5y-12z &=-18.\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

- $\begin{bmatrix}4z-4 \\ -4z+2 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}-4z-4 \\ 2 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}-4z+4 \\ -4z+2 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}-4z-4 \\ -4z+2 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$
- $\begin{bmatrix}-4z+2 \\ -4z-4 \\ z\end{bmatrix},\,z\in (-\infty ,\infty )$

The augmented matrix for this system is

$$
M=\left[\begin{array}{ccc|c}2 & -4 & -8 & -16 \\ 2 & -1 & 4 & -10 \\ 2 & -5 & -12 & -18\end{array}\right].
$$

Using the standard Gauss-Jordan method, we can reduce this matrix to reduced row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}2 & -4 & -8 & -16 \\ 2 & -1 & 4 & -10 \\ 2 & -5 & -12 & -18\end{array}\right] & {R}_{1}:=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & -4 & -8 \\ 2 & -1 & 4 & -10 \\ 2 & -5 & -12 & -18\end{array}\right] & {R}_{2}:={R}_{2}+(-2){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & -4 & -8 \\ 0 & 3 & 12 & 6 \\ 2 & -5 & -12 & -18\end{array}\right] & {R}_{2}:=\frac{1}{3}{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & -4 & -8 \\ 0 & 1 & 4 & 2 \\ 2 & -5 & -12 & -18\end{array}\right] & {R}_{3}:={R}_{3}+(-2){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & -4 & -8 \\ 0 & 1 & 4 & 2 \\ 0 & -1 & -4 & -2\end{array}\right] & {R}_{3}:={R}_{3}+(1){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & -2 & -4 & -8 \\ 0 & 1 & 4 & 2 \\ 0 & 0 & 0 & 0\end{array}\right] & {R}_{1}:={R}_{1}+(2){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 4 & -4 \\ 0 & 1 & 4 & 2 \\ 0 & 0 & 0 & 0\end{array}\right]\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x+4z &=-4 \\ y+4z &=2.\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y$, and we have one free variable, $z$. That means we need to find $x$ and $y$ in terms of $z$.

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=-4z-4 \\ y &=-4z+2 \\ z &=z,\end{aligned}\right.
$$

where $z$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}-4z-4 \\ -4z+2 \\ z\end{bmatrix},\,z\in (-\infty ,\infty ).
$$

---

Consider the system of linear equations

$$
\left\{\begin{aligned}2x-2y-4z+2w &=22 \\ 2x+y-z+8w &=16 \\ 2x+4w &=12.\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

- $\begin{bmatrix}-2w+6 \\ -3w+1 \\ w-3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}2w+6 \\ -3w+1 \\ w-3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}-2w-6 \\ -3w+1 \\ w-3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}-2w+6 \\ 1 \\ w-3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}-3w+1 \\ -2w+6 \\ w-3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cccc|c}2 & -2 & -4 & 2 & 22 \\ 2 & 1 & -1 & 8 & 16 \\ 2 & 0 & 0 & 4 & 12\end{array}\right].
$$

Using the standard Gauss-Jordan method, we can reduce this matrix to reduced row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{cccc|c}2 & -2 & -4 & 2 & 22 \\ 2 & 1 & -1 & 8 & 16 \\ 2 & 0 & 0 & 4 & 12\end{array}\right] & {R}_{1}:=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & -1 & -2 & 1 & 11 \\ 2 & 1 & -1 & 8 & 16 \\ 2 & 0 & 0 & 4 & 12\end{array}\right] & {R}_{2}:={R}_{2}+(-2){R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & -1 & -2 & 1 & 11 \\ 0 & 3 & 3 & 6 & -6 \\ 2 & 0 & 0 & 4 & 12\end{array}\right] & {R}_{3}:={R}_{3}+(-2){R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & -1 & -2 & 1 & 11 \\ 0 & 3 & 3 & 6 & -6 \\ 0 & 2 & 4 & 2 & -10\end{array}\right] & {R}_{2}:=\frac{1}{3}{R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & -1 & -2 & 1 & 11 \\ 0 & 1 & 1 & 2 & -2 \\ 0 & 2 & 4 & 2 & -10\end{array}\right] & {R}_{3}:={R}_{3}+(-2){R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & -1 & -2 & 1 & 11 \\ 0 & 1 & 1 & 2 & -2 \\ 0 & 0 & 2 & -2 & -6\end{array}\right] & {R}_{3}:=\frac{1}{2}{R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & -1 & -2 & 1 & 11 \\ 0 & 1 & 1 & 2 & -2 \\ 0 & 0 & 1 & -1 & -3\end{array}\right] & {R}_{2}:={R}_{2}+(-1){R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & -1 & -2 & 1 & 11 \\ 0 & 1 & 0 & 3 & 1 \\ 0 & 0 & 1 & -1 & -3\end{array}\right] & {R}_{1}:={R}_{1}+(2){R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & -1 & 0 & -1 & 5 \\ 0 & 1 & 0 & 3 & 1 \\ 0 & 0 & 1 & -1 & -3\end{array}\right] & {R}_{1}:={R}_{1}+(1){R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & 0 & 0 & 2 & 6 \\ 0 & 1 & 0 & 3 & 1 \\ 0 & 0 & 1 & -1 & -3\end{array}\right]\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x+2w &=6 \\ y+3w &=1 \\ z-w &=-3.\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y$ and $z$, and we have one free variable, $w$. That means we need to find $x$ and $y$ and $z$ in terms of $w$.

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=-2w+6 \\ y &=-3w+1 \\ z &=w-3 \\ w &=w,\end{aligned}\right.
$$

where $w$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{bmatrix}x \\ y \\ z \\ w\end{bmatrix}=\begin{bmatrix}-2w+6 \\ -3w+1 \\ w-3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty ).
$$

---

Consider the system of linear equations

$$
\left\{\begin{aligned}2x+2y-4z+2w &=-30 \\ x+4y+z+7w &=-12 \\ -2x-4y+4z-4w &=40.\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

- $\begin{bmatrix}-2w-2 \\ -w-5 \\ -w+6 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}-2w+2 \\ -5 \\ -w+6 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}-2w+2 \\ -w-5 \\ -w+6 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}-w-5 \\ -2w+2 \\ -w+6 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}2w+2 \\ -w-5 \\ -w+6 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cccc|c}2 & 2 & -4 & 2 & -30 \\ 1 & 4 & 1 & 7 & -12 \\ -2 & -4 & 4 & -4 & 40\end{array}\right].
$$

Using the standard Gauss-Jordan method, we can reduce this matrix to reduced row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{cccc|c}2 & 2 & -4 & 2 & -30 \\ 1 & 4 & 1 & 7 & -12 \\ -2 & -4 & 4 & -4 & 40\end{array}\right] & {R}_{1}:=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & -2 & 1 & -15 \\ 1 & 4 & 1 & 7 & -12 \\ -2 & -4 & 4 & -4 & 40\end{array}\right] & {R}_{2}:={R}_{2}+(-1){R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & -2 & 1 & -15 \\ 0 & 3 & 3 & 6 & 3 \\ -2 & -4 & 4 & -4 & 40\end{array}\right] & {R}_{3}:={R}_{3}+(2){R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & -2 & 1 & -15 \\ 0 & 3 & 3 & 6 & 3 \\ 0 & -2 & 0 & -2 & 10\end{array}\right] & {R}_{2}:=\frac{1}{3}{R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & -2 & 1 & -15 \\ 0 & 1 & 1 & 2 & 1 \\ 0 & -2 & 0 & -2 & 10\end{array}\right] & {R}_{3}:={R}_{3}+(2){R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & -2 & 1 & -15 \\ 0 & 1 & 1 & 2 & 1 \\ 0 & 0 & 2 & 2 & 12\end{array}\right] & {R}_{3}:=\frac{1}{2}{R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & -2 & 1 & -15 \\ 0 & 1 & 1 & 2 & 1 \\ 0 & 0 & 1 & 1 & 6\end{array}\right] & {R}_{2}:={R}_{2}+(-1){R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & -2 & 1 & -15 \\ 0 & 1 & 0 & 1 & -5 \\ 0 & 0 & 1 & 1 & 6\end{array}\right] & {R}_{1}:={R}_{1}+(2){R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & 0 & 3 & -3 \\ 0 & 1 & 0 & 1 & -5 \\ 0 & 0 & 1 & 1 & 6\end{array}\right] & {R}_{1}:={R}_{1}+(-1){R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & 0 & 0 & 2 & 2 \\ 0 & 1 & 0 & 1 & -5 \\ 0 & 0 & 1 & 1 & 6\end{array}\right]\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x+2w &=2 \\ y+w &=-5 \\ z+w &=6.\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y$ and $z$, and we have one free variable, $w$. That means we need to find $x$ and $y$ and $z$ in terms of $w$.

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=-2w+2 \\ y &=-w-5 \\ z &=-w+6 \\ w &=w,\end{aligned}\right.
$$

where $w$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{bmatrix}x \\ y \\ z \\ w\end{bmatrix}=\begin{bmatrix}-2w+2 \\ -w-5 \\ -w+6 \\ w\end{bmatrix},\,w\in (-\infty ,\infty ).
$$

---

Consider the system of linear equations

$$
\left\{\begin{aligned}2x+4y-4z-26w &=-20 \\ 2x+7y+2z-23w &=-17 \\ -2x-5y+4z+29w &=25.\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

- $\begin{bmatrix}3w+6 \\ 3w-5 \\ -2w+3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}3w-5 \\ 3w+6 \\ -2w+3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}-3w+6 \\ 3w-5 \\ -2w+3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}3w-6 \\ 3w-5 \\ -2w+3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}3w+6 \\ -5 \\ -2w+3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cccc|c}2 & 4 & -4 & -26 & -20 \\ 2 & 7 & 2 & -23 & -17 \\ -2 & -5 & 4 & 29 & 25\end{array}\right].
$$

Using the standard Gauss-Jordan method, we can reduce this matrix to reduced row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{cccc|c}2 & 4 & -4 & -26 & -20 \\ 2 & 7 & 2 & -23 & -17 \\ -2 & -5 & 4 & 29 & 25\end{array}\right] & {R}_{1}:=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & -2 & -13 & -10 \\ 2 & 7 & 2 & -23 & -17 \\ -2 & -5 & 4 & 29 & 25\end{array}\right] & {R}_{2}:={R}_{2}+(-2){R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & -2 & -13 & -10 \\ 0 & 3 & 6 & 3 & 3 \\ -2 & -5 & 4 & 29 & 25\end{array}\right] & {R}_{3}:={R}_{3}+(2){R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & -2 & -13 & -10 \\ 0 & 3 & 6 & 3 & 3 \\ 0 & -1 & 0 & 3 & 5\end{array}\right] & {R}_{2}:=\frac{1}{3}{R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & -2 & -13 & -10 \\ 0 & 1 & 2 & 1 & 1 \\ 0 & -1 & 0 & 3 & 5\end{array}\right] & {R}_{3}:={R}_{3}+(1){R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & -2 & -13 & -10 \\ 0 & 1 & 2 & 1 & 1 \\ 0 & 0 & 2 & 4 & 6\end{array}\right] & {R}_{3}:=\frac{1}{2}{R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & -2 & -13 & -10 \\ 0 & 1 & 2 & 1 & 1 \\ 0 & 0 & 1 & 2 & 3\end{array}\right] & {R}_{2}:={R}_{2}+(-2){R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & -2 & -13 & -10 \\ 0 & 1 & 0 & -3 & -5 \\ 0 & 0 & 1 & 2 & 3\end{array}\right] & {R}_{1}:={R}_{1}+(2){R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & 0 & -9 & -4 \\ 0 & 1 & 0 & -3 & -5 \\ 0 & 0 & 1 & 2 & 3\end{array}\right] & {R}_{1}:={R}_{1}+(-2){R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & 0 & 0 & -3 & 6 \\ 0 & 1 & 0 & -3 & -5 \\ 0 & 0 & 1 & 2 & 3\end{array}\right]\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x-3w &=6 \\ y-3w &=-5 \\ z+2w &=3.\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y$ and $z$, and we have one free variable, $w$. That means we need to find $x$ and $y$ and $z$ in terms of $w$.

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=3w+6 \\ y &=3w-5 \\ z &=-2w+3 \\ w &=w,\end{aligned}\right.
$$

where $w$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{bmatrix}x \\ y \\ z \\ w\end{bmatrix}=\begin{bmatrix}3w+6 \\ 3w-5 \\ -2w+3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty ).
$$

---

Consider the system of linear equations

$$
\left\{\begin{aligned}2x+2y+2z-8w &=-22 \\ -x+2y+2z-2w &=-16 \\ x+2y+4z-12w &=-26.\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

- $\begin{bmatrix}2w-2 \\ -w-6 \\ 3w-3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}2w-2 \\ -6 \\ 3w-3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}-2w-2 \\ -w-6 \\ 3w-3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}2w+2 \\ -w-6 \\ 3w-3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}-w-6 \\ 2w-2 \\ 3w-3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cccc|c}2 & 2 & 2 & -8 & -22 \\ -1 & 2 & 2 & -2 & -16 \\ 1 & 2 & 4 & -12 & -26\end{array}\right].
$$

Using the standard Gauss-Jordan method, we can reduce this matrix to reduced row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{cccc|c}2 & 2 & 2 & -8 & -22 \\ -1 & 2 & 2 & -2 & -16 \\ 1 & 2 & 4 & -12 & -26\end{array}\right] & {R}_{1}:=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & 1 & -4 & -11 \\ -1 & 2 & 2 & -2 & -16 \\ 1 & 2 & 4 & -12 & -26\end{array}\right] & {R}_{2}:={R}_{2}+(1){R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & 1 & -4 & -11 \\ 0 & 3 & 3 & -6 & -27 \\ 1 & 2 & 4 & -12 & -26\end{array}\right] & {R}_{3}:={R}_{3}+(-1){R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & 1 & -4 & -11 \\ 0 & 3 & 3 & -6 & -27 \\ 0 & 1 & 3 & -8 & -15\end{array}\right] & {R}_{2}:=\frac{1}{3}{R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & 1 & -4 & -11 \\ 0 & 1 & 1 & -2 & -9 \\ 0 & 1 & 3 & -8 & -15\end{array}\right] & {R}_{3}:={R}_{3}+(-1){R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & 1 & -4 & -11 \\ 0 & 1 & 1 & -2 & -9 \\ 0 & 0 & 2 & -6 & -6\end{array}\right] & {R}_{3}:=\frac{1}{2}{R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & 1 & -4 & -11 \\ 0 & 1 & 1 & -2 & -9 \\ 0 & 0 & 1 & -3 & -3\end{array}\right] & {R}_{2}:={R}_{2}+(-1){R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & 1 & -4 & -11 \\ 0 & 1 & 0 & 1 & -6 \\ 0 & 0 & 1 & -3 & -3\end{array}\right] & {R}_{1}:={R}_{1}+(-1){R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & 0 & -1 & -8 \\ 0 & 1 & 0 & 1 & -6 \\ 0 & 0 & 1 & -3 & -3\end{array}\right] & {R}_{1}:={R}_{1}+(-1){R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & 0 & 0 & -2 & -2 \\ 0 & 1 & 0 & 1 & -6 \\ 0 & 0 & 1 & -3 & -3\end{array}\right]\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x-2w &=-2 \\ y+w &=-6 \\ z-3w &=-3.\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y$ and $z$, and we have one free variable, $w$. That means we need to find $x$ and $y$ and $z$ in terms of $w$.

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=2w-2 \\ y &=-w-6 \\ z &=3w-3 \\ w &=w,\end{aligned}\right.
$$

where $w$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{bmatrix}x \\ y \\ z \\ w\end{bmatrix}=\begin{bmatrix}2w-2 \\ -w-6 \\ 3w-3 \\ w\end{bmatrix},\,w\in (-\infty ,\infty ).
$$

---

Consider the system of linear equations

$$
\left\{\begin{aligned}2x+4y-4z-18w &=20 \\ -2x-y+7z+24w &=-20 \\ x+y-z-5w &=2.\end{aligned}\right.
$$

Use the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.

- $\begin{bmatrix}w-6 \\ 4 \\ -3w-4 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}w+6 \\ w+4 \\ -3w-4 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}w+4 \\ w-6 \\ -3w-4 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}w-6 \\ w+4 \\ -3w-4 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$
- $\begin{bmatrix}-w-6 \\ w+4 \\ -3w-4 \\ w\end{bmatrix},\,w\in (-\infty ,\infty )$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cccc|c}2 & 4 & -4 & -18 & 20 \\ -2 & -1 & 7 & 24 & -20 \\ 1 & 1 & -1 & -5 & 2\end{array}\right].
$$

Using the standard Gauss-Jordan method, we can reduce this matrix to reduced row echelon form as follows:

$$
\begin{aligned}M & =\left[\begin{array}{cccc|c}2 & 4 & -4 & -18 & 20 \\ -2 & -1 & 7 & 24 & -20 \\ 1 & 1 & -1 & -5 & 2\end{array}\right] & {R}_{1}:=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & -2 & -9 & 10 \\ -2 & -1 & 7 & 24 & -20 \\ 1 & 1 & -1 & -5 & 2\end{array}\right] & {R}_{2}:={R}_{2}+(2){R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & -2 & -9 & 10 \\ 0 & 3 & 3 & 6 & 0 \\ 1 & 1 & -1 & -5 & 2\end{array}\right] & {R}_{3}:={R}_{3}+(-1){R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & -2 & -9 & 10 \\ 0 & 3 & 3 & 6 & 0 \\ 0 & -1 & 1 & 4 & -8\end{array}\right] & {R}_{2}:=\frac{1}{3}{R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & -2 & -9 & 10 \\ 0 & 1 & 1 & 2 & 0 \\ 0 & -1 & 1 & 4 & -8\end{array}\right] & {R}_{3}:={R}_{3}+(1){R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & -2 & -9 & 10 \\ 0 & 1 & 1 & 2 & 0 \\ 0 & 0 & 2 & 6 & -8\end{array}\right] & {R}_{3}:=\frac{1}{2}{R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & -2 & -9 & 10 \\ 0 & 1 & 1 & 2 & 0 \\ 0 & 0 & 1 & 3 & -4\end{array}\right] & {R}_{2}:={R}_{2}+(-1){R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & -2 & -9 & 10 \\ 0 & 1 & 0 & -1 & 4 \\ 0 & 0 & 1 & 3 & -4\end{array}\right] & {R}_{1}:={R}_{1}+(2){R}_{3} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & 0 & -3 & 2 \\ 0 & 1 & 0 & -1 & 4 \\ 0 & 0 & 1 & 3 & -4\end{array}\right] & {R}_{1}:={R}_{1}+(-2){R}_{2} \\  & ∼\left[\begin{array}{cccc|c}1 & 0 & 0 & -1 & -6 \\ 0 & 1 & 0 & -1 & 4 \\ 0 & 0 & 1 & 3 & -4\end{array}\right]\end{aligned}
$$

The corresponding system is now

$$
\left\{\begin{aligned}x-w &=-6 \\ y-w &=4 \\ z+3w &=-4.\end{aligned}\right.
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x$ and $y$ and $z$, and we have one free variable, $w$. That means we need to find $x$ and $y$ and $z$ in terms of $w$.

Therefore, the general solution is

$$
\left\{\begin{aligned}x &=w-6 \\ y &=w+4 \\ z &=-3w-4 \\ w &=w,\end{aligned}\right.
$$

where $w$ (the free variable) is an arbitrary number.

In vector form, the solution can be written as

$$
\begin{bmatrix}x \\ y \\ z \\ w\end{bmatrix}=\begin{bmatrix}w-6 \\ w+4 \\ -3w-4 \\ w\end{bmatrix},\,w\in (-\infty ,\infty ).
$$