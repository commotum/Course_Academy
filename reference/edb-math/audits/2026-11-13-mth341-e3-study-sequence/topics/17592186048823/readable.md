# 17592186048823 Finding a Basis of the Null Space of a Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121041 — Introduction

Remember that the null space $\textrm{Null}(A)$ of a matrix $A$ consists of the solutions to the equation $A\mathbf{x} = \mathbf{0}.$ To find a basis of $\textrm{Null}(A),$ we solve the equation $A\mathbf{x} = \mathbf{0}$ and express the solution as a linear combination of linearly independent vectors. Those vectors form a basis of $\textrm{Null}(A).$

To illustrate, consider the matrix $A={\left[ \begin{array}{ccc}1 & 2 & 2 \\ 2 & 4 & 4 \\ 1 & 3 & 3\end{array} \right]}.$ Computing the reduced row echelon form of $A,$ we get

$$
A \sim 
	{\left[ \begin{array}{ccc}\bbox[2pt,lightgray]{ {\color{blue}1}} & {\color{blue}0} & {\color{red}0} \\ {\color{blue}0} & \bbox[2pt,lightgray]{ {\color{blue}1}} & {\color{red}1} \\ {\color{blue}0} & {\color{blue}0} & {\color{red}0}\end{array} \right]}.
$$

So, the equation $A\mathbf{x} = \mathbf{0}$ is equivalent to the system

$$
{\left\{  \begin{array}{l}{\color{blue}{x}_{1}} = 0 \\ {\color{blue}{x}_{2}} + {\color{red}{x}_{3}} = 0 \\ 0 = 0\end{array} \right. }
\qquad \Longrightarrow \qquad
{\left\{  \begin{array}{l}{\color{blue}{x}_{1}} = 0 \\ {\color{blue}{x}_{2}} = - {\color{red}{x}_{3}} ,\end{array} \right. }
$$

where $\color{blue}x_1$ and $\color{blue}x_2$ are basic variables (corresponding to the pivot columns) and $\color{red}x_3$ is a free variable (corresponding to the non-pivot column).

Therefore, any vector $\mathbf{x}$ in $\textrm{Null}(A)$ has the form

$$
{\left[ \begin{array}{c}{x}_{1} \\ {x}_{2} \\ {x}_{3}\end{array} \right]} = {\left[ \begin{array}{c}0 \\ - {x}_{3} \\ {x}_{3}\end{array} \right]} = x_3{\left[ \begin{array}{c}0 \\ - 1 \\ 1\end{array} \right]}, \qquad x_3\in\mathbb{R}.
$$

So, the set $\mathcal{B}=\left\{ {\left[ \begin{array}{c}0 \\ - 1 \\ 1\end{array} \right]} \right\}$ is a basis of $\textrm{Null}(A)$ since it is a linearly independent set and the vector $\begin{bmatrix}0 \\ -1 \\ 1\end{bmatrix}$ generates the null space of $A.$

**Note:** It might be the case that $\textrm{Null}(A)$ for a particular matrix $A$ equals the so-called zero subspace $\{ \mathbf{0} \}$ containing only the zero-vector. The basis of $\{ \mathbf{0} \}$ is said to be the *empty set*, which is a set that does not contain any vectors. The empty set is denoted by $\emptyset$ or $\{\,\}.$



### example 17592186119628 — Finding a Basis for a Given Null Space

Given that  $$
\displaystyle \textrm{Null}(A)=\left\{ {\left[ \begin{array}{c}3 {x}_{3} - {x}_{4} \\ 4 {x}_{3} \\ {x}_{3} \\ {x}_{4}\end{array} \right]} \: : \: x_3, x_4 \in \mathbb{R} \right\},
$$ find a basis for $\textrm{Null}(A).$

Any vector in $\textrm{Null}(A)$ has the form

$$
{\left[ \begin{array}{c}3 {x}_{3} - {x}_{4} \\ 4 {x}_{3} \\ {x}_{3} \\ {x}_{4}\end{array} \right]}, \qquad  x_3, x_4 \in \mathbb{R}.
$$

Expanding, we get

$$
\begin{aligned}\begin{bmatrix}3{x}_{3}-{x}_{4} \\ 4{x}_{3} \\ {x}_{3} \\ {x}_{4}\end{bmatrix} & =\begin{bmatrix}3{x}_{3} \\ 4{x}_{3} \\ {x}_{3} \\ 0\end{bmatrix}+\begin{bmatrix}-{x}_{4} \\ 0 \\ 0 \\ {x}_{4}\end{bmatrix} \\  & ={x}_{3}\begin{bmatrix}3 \\ 4 \\ 1 \\ 0\end{bmatrix}+{x}_{4}\begin{bmatrix}-1 \\ 0 \\ 0 \\ 1\end{bmatrix}.\end{aligned}
$$

Therefore, a basis for $\textrm{Null}(A)$ is

$$
\mathcal{B} =\left\{ {\left[ \begin{array}{c}3 \\ 4 \\ 1 \\ 0\end{array} \right]}, {\left[ \begin{array}{c}- 1 \\ 0 \\ 0 \\ 1\end{array} \right]} \right\}
$$

since it is a linearly independent set and its vectors generate $\textrm{Null}(A).$

### example 17592186119629 — Finding a Basis for the Null Space of a Matrix Given in Reduced Row Echelon Form

Find a basis of the null space of the matrix $A={\left[ \begin{array}{cccc}1 & 3 & 0 & 0 \\ 0 & 0 & 1 & - 4 \\ 0 & 0 & 0 & 0\end{array} \right]}.$

To find a basis of $\textrm{Null}(A),$ we need to solve the equation $A\mathbf{x} = \mathbf{0}$ and express the solution as a linear combination of linearly independent vectors. Those vectors form a basis of $\textrm{Null}(A).$

The given matrix is already in reduced row echelon form. So, the equation $A\mathbf{x}=\mathbf{0}$ corresponds to the following system:
$$
{\left\{  \begin{array}{l}{x}_{1} + 3 {x}_{2} = 0 \\ {x}_{3} - 4 {x}_{4} = 0 \\ 0 = 0\end{array} \right. }
\qquad \Longrightarrow \qquad
{\left\{  \begin{array}{l}{x}_{1} = - 3 {x}_{2} \\ {x}_{3} = 4 {x}_{4}\end{array} \right. }
$$

Here, $x_1$ and $x_3$ are basic variables corresponding to the pivot columns ($1$st and $3$rd) and $x_2,x_4$ are free variables corresponding to the non-pivot columns. Therefore, if $\mathbf{x} \in \textrm{Null}(A),$ then

$$
\begin{aligned}\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3} \\ {x}_{4}\end{bmatrix} & =\begin{bmatrix}-3{x}_{2} \\ {x}_{2} \\ 4{x}_{4} \\ {x}_{4}\end{bmatrix} \\  & =\begin{bmatrix}-3{x}_{2} \\ {x}_{2} \\ 0 \\ 0\end{bmatrix}+\begin{bmatrix}0 \\ 0 \\ 4{x}_{4} \\ {x}_{4}\end{bmatrix} \\  & ={x}_{2}\begin{bmatrix}-3 \\ 1 \\ 0 \\ 0\end{bmatrix}+{x}_{4}\begin{bmatrix}0 \\ 0 \\ 4 \\ 1\end{bmatrix}\end{aligned}
$$

where $x_2,x_4\in\mathbb{R}.$ This implies that

$$
\mathcal{B}=\left\{ {\left[ \begin{array}{c}- 3 \\ 1 \\ 0 \\ 0\end{array} \right]} ,{\left[ \begin{array}{c}0 \\ 0 \\ 4 \\ 1\end{array} \right]} \right\}
$$

is a basis of $\textrm{Null}(A)$ since it is a linearly independent set and its vectors generate $\textrm{Null}(A).$

### example 17592186119627 — Finding a Basis of the Null Space of a Matrix Given a Row Equivalent Matrix

The matrices $A$ and $B$ are given below. If $A$ is row equivalent to $B$, then find a basis of $\textrm{Null}(A).$

$$
A={\left[ \begin{array}{cccc}- 9 & 3 & - 1 & 2 \\ 1 & 3 & - 1 & 2 \\ - 5 & 9 & - 3 & 6\end{array} \right]}, \qquad
B={\left[ \begin{array}{cccc}1 & 0 & 0 & 0 \\ 0 & 1 & - {\displaystyle \frac{1}{3}} & {\displaystyle \frac{2}{3}} \\ 0 & 0 & 0 & 0\end{array} \right]}
$$

To find a basis of $\textrm{Null}(A),$ we need to solve the equation $A\mathbf{x} = \mathbf{0}$ and express the solution as a linear combination of linearly independent vectors. Those vectors form a basis of $\textrm{Null}(A).$

Since $A\sim B,$ the equation $A \mathbf{x} = \mathbf{0}$ is equivalent to the equation $B\mathbf{x}=\mathbf{0},$ which corresponds to the following system:

$$
\left\{\begin{aligned}{x}_{1} &=0 \\ {x}_{2}-\frac{1}{3}{x}_{3}+\frac{2}{3}{x}_{4} &=0\end{aligned}\right.
$$

So, the general solution is $x_1=0$ and $x_2=\dfrac{1}{3}x_3 - \dfrac{2}{3} x_4$ where $x_3$ and $x_4$ are free variables. Therefore, if $\mathbf{x}\in\textrm{Null}(A),$ then

$$
\begin{aligned}\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3} \\ {x}_{4}\end{bmatrix} & =\begin{bmatrix}0 \\ \frac{1}{3}{x}_{3}-\frac{2}{3}{x}_{4} \\ {x}_{3} \\ {x}_{4}\end{bmatrix}={x}_{3}\begin{bmatrix}0 \\ \frac{1}{3} \\ 1 \\ 0\end{bmatrix}+{x}_{4}\begin{bmatrix}0 \\ -\frac{2}{3} \\ 0 \\ 1\end{bmatrix},\,{x}_{3},{x}_{4}\in R.\end{aligned}
$$

This implies that

$$
\mathcal{B}=\left\{ {\left[ \begin{array}{c}0 \\ {\displaystyle \frac{1}{3}} \\ 1 \\ 0\end{array} \right]}, {\left[ \begin{array}{c}0 \\ - {\displaystyle \frac{2}{3}} \\ 0 \\ 1\end{array} \right]} \right\}
$$

is a basis of $\textrm{Null}(A)$ since it is a linearly independent set and its vectors generate $\textrm{Null}(A).$

### example 17592186119630 — Finding a Basis for the Null Space of a Matrix That Is Not in Reduced Row Echelon Form

Given the matrix $A={\left[ \begin{array}{ccc}1 & 0 & 2 \\ 0 & 1 & 2 \\ 0 & 2 & 5\end{array} \right]},$ find a basis of $\textrm{Null}(A).$

First, we reduce the matrix $A$ to reduced row echelon form (RREF):

$$
\begin{aligned}A & =\begin{bmatrix}1 & 0 & 2 \\ 0 & 1 & 2 \\ 0 & 2 & 5\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 2 \\ 0 & 1 & 2 \\ 0 & 0 & 1\end{bmatrix} & {R}_{2} & :={R}_{2}+(-2){R}_{3} \\  & ∼\begin{bmatrix}1 & 0 & 2 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{3} \\  & ∼\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}\end{aligned}
$$

So, the equation $A\mathbf{x} = \mathbf{0}$ is equivalent to the system

$$
\left\{\begin{aligned}{x}_{1} &=0 \\ {x}_{2} &=0 \\ {x}_{3} &=0.\end{aligned}\right.
$$

This implies that the only solution of $A\mathbf{x}=\mathbf{0}$ is $\mathbf{x}=\mathbf{0}.$ So $\textrm{Null}(A)=\{ \mathbf{0} \},$ which means that the basis of $\textrm{Null}(A)$ is the empty set, i.e., $\mathcal{B}=\{\,\}.$

## Representative practice (first three per skill; full bank in practice.json)

### Finding a Basis for a Given Null Space (11 captured questions)

Question 17592186120388 — question.difficulty/easy

Given that  $\text{Null}(A)={\begin{bmatrix}-3{x}_{3} \\ 4{x}_{3} \\ {x}_{3}\end{bmatrix}\,:\,{x}_{3}\in R}$, find a basis for $\text{Null}(A).$

Solution: Any vector in $\text{Null}(A)$ has the form

$$
\begin{bmatrix}-3{x}_{3} \\ 4{x}_{3} \\ {x}_{3}\end{bmatrix},\,{x}_{3}\in R.
$$

Expanding, we get

$$
\begin{bmatrix}-3{x}_{3} \\ 4{x}_{3} \\ {x}_{3}\end{bmatrix}={x}_{3}\begin{bmatrix}-3 \\ 4 \\ 1\end{bmatrix}.
$$

Therefore, a basis for $\text{Null}(A)$ is

$$
B={\begin{bmatrix}-3 \\ 4 \\ 1\end{bmatrix}}
$$

since it is a linearly independent set and its vectors generate $\text{Null}(A).$

Answer selection: B={\begin{bmatrix}-3 \\ 4 \\ 1\end{bmatrix}}

Question 17592186120394 — question.difficulty/easy

Given that  $$
\displaystyle \text{Null}(A)={\begin{bmatrix}-3{x}_{3}+2{x}_{4} \\ 2{x}_{3}-5{x}_{4} \\ {x}_{3} \\ {x}_{4}\end{bmatrix}\,:\,{x}_{3},{x}_{4}\in R},
$$ find a basis for $\text{Null}(A).$

Solution: Any vector in $\text{Null}(A)$ has the form

$$
\begin{bmatrix}-3{x}_{3}+2{x}_{4} \\ 2{x}_{3}-5{x}_{4} \\ {x}_{3} \\ {x}_{4}\end{bmatrix},\,{x}_{3},{x}_{4}\in R.
$$

Expanding, we get

$$
\begin{aligned}\begin{bmatrix}-3{x}_{3}+2{x}_{4} \\ 2{x}_{3}-5{x}_{4} \\ {x}_{3} \\ {x}_{4}\end{bmatrix} & =\begin{bmatrix}-3{x}_{3} \\ 2{x}_{3} \\ {x}_{3} \\ 0\end{bmatrix}+\begin{bmatrix}2{x}_{4} \\ -5{x}_{4} \\ 0 \\ {x}_{4}\end{bmatrix} \\  & ={x}_{3}\begin{bmatrix}-3 \\ 2 \\ 1 \\ 0\end{bmatrix}+{x}_{4}\begin{bmatrix}2 \\ -5 \\ 0 \\ 1\end{bmatrix}.\end{aligned}
$$

Therefore a basis for $\text{Null}(A)$ is

$$
B={\begin{bmatrix}-3 \\ 2 \\ 1 \\ 0\end{bmatrix},\begin{bmatrix}2 \\ -5 \\ 0 \\ 1\end{bmatrix}}
$$

since it is a linearly independent set and its vectors generate $\text{Null}(A).$

Answer selection: B={\begin{bmatrix}-3 \\ 2 \\ 1 \\ 0\end{bmatrix},\begin{bmatrix}2 \\ -5 \\ 0 \\ 1\end{bmatrix}}

Question 17592186345010 — question.difficulty/easy

Given that  $$
\displaystyle \text{Null}(A)={\begin{bmatrix}3{x}_{4}-2{x}_{3} \\ {x}_{3}+2{x}_{4} \\ {x}_{3} \\ {x}_{4}\end{bmatrix}\,:\,{x}_{3},{x}_{4}\in R},
$$ find a basis for $\text{Null}(A).$

Solution: Any vector in $\text{Null}(A)$ has the form

$$
\begin{bmatrix}3{x}_{4}-2{x}_{3} \\ {x}_{3}+2{x}_{4} \\ {x}_{3} \\ {x}_{4}\end{bmatrix},\,{x}_{3},{x}_{4}\in R.
$$

Expanding, we get

$$
\begin{aligned}\begin{bmatrix}3{x}_{4}-2{x}_{3} \\ {x}_{3}+2{x}_{4} \\ {x}_{3} \\ {x}_{4}\end{bmatrix} & =\begin{bmatrix}-2{x}_{3} \\ {x}_{3} \\ {x}_{3} \\ 0\end{bmatrix}+\begin{bmatrix}3{x}_{4} \\ 2{x}_{4} \\ 0 \\ {x}_{4}\end{bmatrix} \\  & ={x}_{3}\begin{bmatrix}-2 \\ 1 \\ 1 \\ 0\end{bmatrix}+{x}_{4}\begin{bmatrix}3 \\ 2 \\ 0 \\ 1\end{bmatrix}.\end{aligned}
$$

Therefore a basis for $\text{Null}(A)$ is

$$
B={\begin{bmatrix}-2 \\ 1 \\ 1 \\ 0\end{bmatrix},\begin{bmatrix}3 \\ 2 \\ 0 \\ 1\end{bmatrix}}
$$

since it is a linearly independent set and its vectors generate $\text{Null}(A).$

Answer selection: B={\begin{bmatrix}-2 \\ 1 \\ 1 \\ 0\end{bmatrix},\begin{bmatrix}3 \\ 2 \\ 0 \\ 1\end{bmatrix}}

### Finding a Basis for the Null Space of a Matrix Given in Reduced Row Echelon Form (16 captured questions)

Question 17592186120387 — question.difficulty/easy

Find a basis of the null space of the matrix $A=\begin{bmatrix}1 & 0 & 0 & -1 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 1 & -3\end{bmatrix}.$

Solution: To find a basis of $\text{Null}(A),$ we need to solve the equation $Ax=0$ and express the solution as a linear combination of linearly independent vectors. Those vectors form a basis of $\text{Null}(A).$

The given matrix is already in reduced row echelon form. So, the equation $Ax=0$ corresponds to the following system:

$$
\left\{\begin{aligned}{x}_{1}-{x}_{4} &=0 \\ {x}_{2}+2{x}_{4} &=0 \\ {x}_{3}-3{x}_{4} &=0\end{aligned}\right.\,⟹\,\left\{\begin{aligned}{x}_{1} &={x}_{4} \\ {x}_{2} &=-2{x}_{4} \\ {x}_{3} &=3{x}_{4}\end{aligned}\right.
$$

Here, ${x}_{1}$, ${x}_{2}$, and ${x}_{3}$ are basic variables corresponding to the pivot columns ($1$st, $2$nd, and $3$rd) and ${x}_{4}$ is a free variable corresponding to the non-pivot column. Therefore, if $x\in \text{Null}(A),$ then

$$
\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3} \\ {x}_{4}\end{bmatrix}=\begin{bmatrix}{x}_{4} \\ -2{x}_{4} \\ 3{x}_{4} \\ {x}_{4}\end{bmatrix}={x}_{4}\begin{bmatrix}1 \\ -2 \\ 3 \\ 1\end{bmatrix},
$$

where ${x}_{4}\in R.$ This implies that

$$
B={\begin{bmatrix}1 \\ -2 \\ 3 \\ 1\end{bmatrix}}
$$

is a basis of $\text{Null}(A)$ since it is a linearly independent set and its vectors generate the $\text{Null}(A).$

Answer selection: B={\begin{bmatrix}1 \\ -2 \\ 3 \\ 1\end{bmatrix}}

Question 17592186120391 — None

Find a basis of the the null space of the matrix $A = \begin{bmatrix}1 & 0 & 0 & -4 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 5\end{bmatrix}$.

Solution: 

Question 17592186247220 — question.difficulty/easy

Find a basis of the null space of the matrix $A=\begin{bmatrix}1 & 0 & 0 & 3 \\ 0 & 1 & -6 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}.$

Solution: To find a basis of $\text{Null}(A),$ we need to solve the equation $Ax=0$ and express the solution as a linear combination of linearly independent vectors. Those vectors form a basis of $\text{Null}(A).$

The given matrix is already in reduced row echelon form. So, the equation $Ax=0$ corresponds to the following system:

$$
\left\{\begin{aligned}{x}_{1}+3{x}_{4} &=0 \\ {x}_{2}-6{x}_{3} &=0\end{aligned}\right.\,⟹\,\left\{\begin{aligned}{x}_{1} &=-3{x}_{4} \\ {x}_{2} &=6{x}_{3}\end{aligned}\right.
$$

Here, ${x}_{1}$ and  ${x}_{2}$ are basic variables corresponding to the pivot columns ($1$st and $2$nd), and ${x}_{3}$ and ${x}_{4}$ are free variable corresponding to the non-pivot columns. Therefore, if $x\in \text{Null}(A),$ then

$$
\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3} \\ {x}_{4}\end{bmatrix}=\begin{bmatrix}-3{x}_{4} \\ 6{x}_{3} \\ {x}_{3} \\ {x}_{4}\end{bmatrix}={x}_{3}\begin{bmatrix}0 \\ 6 \\ 1 \\ 0\end{bmatrix}+{x}_{4}\begin{bmatrix}-3 \\ 0 \\ 0 \\ 1\end{bmatrix},
$$

where ${x}_{3},\,{x}_{4}\in R.$ This implies that

$$
B={\begin{bmatrix}0 \\ 6 \\ 1 \\ 0\end{bmatrix},\begin{bmatrix}-3 \\ 0 \\ 0 \\ 1\end{bmatrix}}
$$

is a basis of $\text{Null}(A)$ since it is a linearly independent set and its vectors generate the $\text{Null}(A).$

Answer selection: B={\begin{bmatrix}0 \\ 6 \\ 1 \\ 0\end{bmatrix},\begin{bmatrix}-3 \\ 0 \\ 0 \\ 1\end{bmatrix}}

### Finding a Basis of the Null Space of a Matrix Given a Row Equivalent Matrix (14 captured questions)

Question 17592186120336 — question.difficulty/easy

The matrices $A$ and $B$ are given below. Given that $A$ is row equivalent to $B$, then find a basis of $Null(A)$.

$$
\displaystyle A = \begin{bmatrix}1 & 0 & 1 & 0 \\ 1 & 2 & 1 & 2 \\ 2 & 1 & 2 & 1\end{bmatrix}, B = \begin{bmatrix}1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \\ 0 & 0 & 0 & 0\end{bmatrix}
$$

Solution: 

Question 17592186120343 — question.difficulty/easy

The matrices $A$ and $B$ are given below. Given that $A$ is row equivalent to $B$, then find a basis of $\text{Null}(A).$

$$
A=\begin{bmatrix}1 & -2 & 1 \\ 2 & -5 & 2 \\ 1 & 0 & 1\end{bmatrix},\,B=\begin{bmatrix}1 & 0 & 1 \\ 0 & 1 & 0 \\ 0 & 0 & 0\end{bmatrix}
$$

Solution: To find a basis of $\text{Null}(A),$ we need to solve the equation $Ax=0$ and express the solution as a linear combination of linearly independent vectors. Those vectors form a basis of $\text{Null}(A).$

Since $A∼B,$ the equation $Ax=0$ is equivalent to the equation $Bx=0,$ which corresponds to the following system:

$$
\left\{\begin{aligned}{x}_{1}+{x}_{3} &=0 \\ {x}_{2} &=0\end{aligned}\right.
$$

So, the general solution is ${x}_{1}=-{x}_{3}$ and ${x}_{2}=0,$ where ${x}_{3}$ is a free variable. Therefore, if $x\in \text{Null}(A),$ then

$$
\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3}\end{bmatrix}=\begin{bmatrix}-{x}_{3} \\ 0 \\ {x}_{3}\end{bmatrix}={x}_{3}\begin{bmatrix}-1 \\ 0 \\ 1\end{bmatrix},\,{x}_{3}\in R.
$$

This implies that 

$$
B=\left\{\begin{bmatrix}-1 \\ 0 \\ 1\end{bmatrix}\right\}
$$

is a basis of $\text{Null}(A)$ since it is a linearly independent set and its vectors generate $\text{Null}(A).$

Answer selection: B=\left\{\begin{bmatrix}-1 \\ 0 \\ 1\end{bmatrix}\right\}

Question 17592186247224 — question.difficulty/easy

The matrices $A$ and $B$ are given below. Given that $A$ is row equivalent to $B$, then find a basis of $\text{Null}(A).$

$$
A=\begin{bmatrix}2 & 0 & -1 & -6 \\ -2 & 3 & -1 & 3 \\ 0 & 0 & -1 & 0\end{bmatrix},\,B=\begin{bmatrix}1 & 0 & 0 & -3 \\ 0 & 1 & 0 & -1 \\ 0 & 0 & 1 & 0\end{bmatrix}
$$

Solution: To find a basis of $\text{Null}(A),$ we need to solve the equation $Ax=0$ and express the solution as a linear combination of linearly independent vectors. Those vectors form a basis of $\text{Null}(A).$

Since $A∼B,$ the equation $Ax=0$ is equivalent to the equation $Bx=0,$ which corresponds to the following system:

$$
\left\{\begin{aligned}{x}_{1}-3{x}_{4} &=0 \\ {x}_{2}-{x}_{4} &=0 \\ {x}_{3} &=0\end{aligned}\right.
$$

So, the general solution is ${x}_{1}=3{x}_{4}$ and ${x}_{2}={x}_{4},$  and ${x}_{3}=0,$ where  ${x}_{4}$ is a free variable. Therefore, if $x\in \text{Null}(A),$ then

$$
\begin{aligned}\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3} \\ {x}_{4}\end{bmatrix} & =\begin{bmatrix}3{x}_{4} \\ {x}_{4} \\ 0 \\ {x}_{4}\end{bmatrix}={x}_{4}\begin{bmatrix}3 \\ 1 \\ 0 \\ 1\end{bmatrix}\,{x}_{4}\in R.\end{aligned}
$$

This implies that 

$$
B={\begin{bmatrix}3 \\ 1 \\ 0 \\ 1\end{bmatrix}}
$$

is a basis of $\text{Null}(A)$ since it is a linearly independent set and its vectors generate $\text{Null}(A).$

Answer selection: B={\begin{bmatrix}3 \\ 1 \\ 0 \\ 1\end{bmatrix}}

### Finding a Basis for the Null Space of a Matrix That Is Not in Reduced Row Echelon Form (12 captured questions)

Question 17592186120395 — question.difficulty/moderate

Given the matrix $A = \begin{bmatrix}1 & -2 & -1 \\ 0 & 0 & 5 \\ 5 & -10 & 7\end{bmatrix}$, find a basis of $Null(A)$.

Solution: 

Question 17592186120396 — None

Given the matrix $A = \begin{bmatrix}1 & -2 & 8 \\ 0 & -4 & 10 \\ -2 & 0 & -6\end{bmatrix}$, find a basis of $Null(A)$.

Solution: 

Question 17592186247226 — question.difficulty/moderate

Given the matrix $A=\begin{bmatrix}1 & 1 & 2 \\ 0 & 0 & -1 \\ -1 & -1 & 2\end{bmatrix}$, find a basis of $\text{Null}(A).$

Solution: First, we reduce the matrix $A$ to reduced row echelon form (RREF):

$$
\begin{aligned}A & =\begin{bmatrix}1 & 1 & 2 \\ 0 & 0 & -1 \\ -1 & -1 & 2\end{bmatrix} & {R}_{3} & :={R}_{3}+{R}_{1} \\  & ∼\begin{bmatrix}1 & 1 & 2 \\ 0 & 0 & -1 \\ 0 & 0 & 4\end{bmatrix} & {R}_{3} & :={R}_{3}+4{R}_{2} \\  & ∼\begin{bmatrix}1 & 1 & 2 \\ 0 & 0 & -1 \\ 0 & 0 & 0\end{bmatrix} & {R}_{2} & :=(-1){R}_{2} \\  & ∼\begin{bmatrix}1 & 1 & 2 \\ 0 & 0 & 1 \\ 0 & 0 & 0\end{bmatrix} & {R}_{1} & :={R}_{1}+(-2){R}_{2} \\  & ∼\begin{bmatrix}1 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

So, the equation $Ax=0$ is equivalent to the system

$$
\left\{\begin{aligned}{x}_{1}+{x}_{2} &=0 \\ {x}_{3} &=0.\end{aligned}\right.
$$

The general solution is ${x}_{1}=-{x}_{2}$ and ${x}_{3}=0,$ where ${x}_{2}$ is a free variable. Therefore, if $x\in \text{Null}(A),$ then

$$
\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3}\end{bmatrix}=\begin{bmatrix}-{x}_{2} \\ {x}_{2} \\ 0\end{bmatrix}={x}_{2}\begin{bmatrix}-1 \\ 1 \\ 0\end{bmatrix},\,{x}_{2}\in R.
$$

This implies that 

$$
B=\left\{\begin{bmatrix}-1 \\ 1 \\ 0\end{bmatrix}\right\}
$$

is a basis of $\text{Null}(A)$ since it is a linearly independent set and its vectors generate $\text{Null}(A).$

Answer selection: B=\left\{\begin{bmatrix}-1 \\ 1 \\ 0\end{bmatrix}\right\}
