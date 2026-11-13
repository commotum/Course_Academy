# 17592186050656 The Column Space of a Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121037 — Introduction

The **column space** of a matrix $A$ is denoted $\text{Col}(A)$ and is the span of the columns of $A$ (i.e., the set of all possible linear combinations of columns of $A$). For example, consider the matrix

$$
A={\left[ \begin{array}{cc}{\color{red}1} & {\color{blue}3} \\ {\color{red}2} & {\color{blue}- 1}\end{array} \right]},
$$
where we denote its columns by $\color{red}\mathbf{a}_1$ and ${\color{blue}\mathbf{a}_2},$ respectively. The column space of this matrix is given by
$$
\textrm{Col}(A) = 
	\textrm{Span}
		\Bigg\{
			\underbrace{ {\left[ \begin{array}{c}{\color{red}1} \\ {\color{red}2}\end{array} \right]}}_{\color{red}\mathbf{a}_1},
			\underbrace{ {\left[ \begin{array}{c}{\color{blue}3} \\ {\color{blue}- 1}\end{array} \right]}}_{\color{blue}\mathbf{a}_2}
		\Bigg\}.
$$

Now, suppose we would like to determine whether the vector $\mathbf{b} = {\left[ \begin{array}{c}2 \\ - 3\end{array} \right]}$ lies in $\textrm{Col}(A).$ In other words, we need to check if $\mathbf{b} \in \textrm{Span}\{ {\color{red}\mathbf{a}_1}, {\color{blue}\mathbf{a}_2} \}.$ So, we need to determine whether $\mathbf{b}$ can be written as some linear combination of $\color{red}\mathbf{a}_1$ and ${\color{blue}\mathbf{a}_2}\mathbin{:}$

$$
\begin{aligned}{x}_{1}{a}_{1}+{x}_{2}{a}_{2}=b\end{aligned}
$$

Notice that the equation above can be written as follows:

$$
\begin{aligned}\begin{bmatrix}{\color{red}{{\mathbf{a}}_{1}}} & {\color{blue}{{\mathbf{a}}_{2}}}\end{bmatrix}\begin{bmatrix}{x}_{1} \\ {x}_{2}\end{bmatrix} & =\mathbf{b} \\ \underbrace{\begin{bmatrix}{\color{red}{1}} & {\color{blue}{3}} \\ {\color{red}{2}} & {\color{blue}{-1}}\end{bmatrix}}_{A}\underbrace{\begin{bmatrix}{x}_{1} \\ {x}_{2}\end{bmatrix}}_{\mathbf{\text{x}}} & =\underbrace{\begin{bmatrix}2 \\ -3\end{bmatrix}}_{\mathbf{\text{b}}}\end{aligned}
$$

So, the equation is equivalent to $A\mathbf{x}=\mathbf{b}.$ To solve the equation, let's find the row echelon form of the augmented matrix $[A \,|\, \mathbf{b}]$ as follows:

$$
\begin{aligned}{}[A\hspace{0.167em}|\hspace{0.167em}\mathbf{b}] & =\left[\begin{array}{cc|c}1 & 3 & 2 \\ 2 & -1 & -3\end{array}\right] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 3 & 2 \\ 0 & -7 & -7\end{array}\right]\end{aligned}
$$

Now, we have the system

$$
\left\{\begin{aligned}{x}_{1}+3{x}_{2} &=2 \\ -7{x}_{2} &=-7.\end{aligned}\right.
$$

From the second equation, we get $x_2=1.$ Substituting into the first equation, we get $x_1=-1.$

Since we have a solution, the equation $A\mathbf{x}=\mathbf{b}$ is consistent, which implies that $\mathbf{b} \in \textrm{Col}(A).$

Moreover, there is exactly one solution, so we have exactly one way to write $\mathbf{b}$ as a linear combination of $\color{red}\mathbf{a}_1$ and ${\color{blue}\mathbf{a}_2}\mathbin{:}$
$$
\underbrace{ {\left[ \begin{array}{c}2 \\ - 3\end{array} \right]}}_{\mathbf{b}} = 
	(-1) \cdot \underbrace{ {\left[ \begin{array}{c}{\color{red}1} \\ {\color{red}2}\end{array} \right]}}_{\color{red}\mathbf{a_1}} + 
	1 \cdot \underbrace{ {\left[ \begin{array}{c}{\color{blue}3} \\ {\color{blue}- 1}\end{array} \right]}}_{\color{blue}\mathbf{a_2}}
$$



### example 17592186119621 — Determining if a Vector is in the Column Space of a Matrix

The matrix $B$ and the vector $\mathbf{b}$ are given below. 
Determine if $\mathbf{b} \in \textrm{Col}(B).$ 
In the affirmative case, find the values of $x_1$ and $x_2,$ where $x_1$ and $x_2$ are the real numbers such that $\mathbf{b}=x_1\mathbf{b}_1+x_2\mathbf{b}_2,$ and $\mathbf{b}_1,$ $\mathbf{b}_2$ are the respective columns of $B.$

$$
B={\left[ \begin{array}{cc}5 & - 2 \\ 15 & - 6 \\ 0 & 1\end{array} \right]},
\qquad
\mathbf{b}={\left[ \begin{array}{c}7 \\ 21 \\ 0\end{array} \right]}
$$

In order to determine whether $\mathbf{b}$ lies in $\textrm{Col}(B),$ we need to check if the equation $B\mathbf{x}=\mathbf{b}$ is consistent. So, let's find the row echelon form of the augmented matrix $[B \,|\, \mathbf{b}]$ as follows:

$$
\begin{aligned}{}[B\hspace{0.167em}|\hspace{0.167em}\mathbf{b}] & =\left[\begin{array}{cc|c}5 & -2 & 7 \\ 15 & -6 & 21 \\ 0 & 1 & 0\end{array}\right] & {R}_{2} & :={R}_{2}-3{R}_{1} \\  & ∼\left[\begin{array}{cc|c}5 & -2 & 7 \\ 0 & 0 & 0 \\ 0 & 1 & 0\end{array}\right] & {R}_{2} & \leftrightarrow {R}_{3} \\  & ∼\left[\begin{array}{cc|c}5 & -2 & 7 \\ 0 & 1 & 0 \\ 0 & 0 & 0\end{array}\right]\end{aligned}
$$

Now, we have the system

$$
\left\{\begin{aligned}5{x}_{1}-2{x}_{2} &=7 \\ {x}_{2} &=0 \\ 0 &=0.\end{aligned}\right.
$$

From the third equation, we get the true statement $0=0.$ So the system is equivalent to the following:

$$
\left\{\begin{aligned}5{x}_{1}-2{x}_{2} &=7 \\ {x}_{2} &=0\end{aligned}\right.
$$

From the second equation, we get $x_2=0.$ Substituting into the first equation gives $x_1=\dfrac 7 5.$ 

Since we have a solution, the equation $B\mathbf{x}=\mathbf{b}$ is consistent, which implies that $\mathbf{b}\in\textrm{Col}(B).$

Moreover, there is exactly one solution, so we have exactly one way to write $\mathbf{b}$ as a linear combination of $\mathbf{b}_1$ and $\mathbf{b}_2\mathbin{:}$
$$
\underbrace{ {\left[ \begin{array}{c}7 \\ 21 \\ 0\end{array} \right]}}_{\mathbf{b}} = \dfrac{7}{5} \cdot \underbrace{ {\left[ \begin{array}{c}5 \\ 15 \\ 0\end{array} \right]}}_{\mathbf{b}_1} + 0 \cdot \underbrace{ {\left[ \begin{array}{c}- 2 \\ - 6 \\ 1\end{array} \right]}}_{\mathbf{b}_2}
$$

### example 17592186119670 — Determining the Value of an Unknown Given a Vector That’s in the Column Space of a Matrix

Consider the matrix given by $A={\left[ \begin{array}{cc}1 & 2 \\ 3 & - 2 \\ 5 & - 1\end{array} \right]}.$ Determine the value of $k$ for which the vector $\mathbf{b}={\left[ \begin{array}{c}10 \\ - 2 \\ 2 + k\end{array} \right]}$ belongs to $\textrm{Col}(A).$

If $\mathbf{b}$ lies in $\textrm{Col}(A),$ then the equation $A\mathbf{x}=\mathbf{b}$ must be consistent. So, let's find the row echelon form of the augmented matrix $[A \,|\, \mathbf{b}]$ as follows:

$$
\begin{aligned}{}[A\hspace{0.167em}|\hspace{0.167em}\mathbf{b}] & =\left[\begin{array}{cc|c}1 & 2 & 10 \\ 3 & -2 & -2 \\ 5 & -1 & 2+k\end{array}\right] & {R}_{2} & :={R}_{2}-3{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 2 & 10 \\ 0 & -8 & -32 \\ 5 & -1 & 2+k\end{array}\right] & {R}_{3} & :={R}_{3}-5{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 2 & 10 \\ 0 & -8 & -32 \\ 0 & -11 & k-48\end{array}\right] & {R}_{2} & :=-\frac{1}{8}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & 2 & 10 \\ 0 & 1 & 4 \\ 0 & -11 & k-48\end{array}\right] & {R}_{3} & :={R}_{3}+11{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & 2 & 10 \\ 0 & 1 & 4 \\ 0 & 0 & k-4\end{array}\right]\end{aligned}
$$

So, we have the system

$$
\left\{\begin{aligned}{x}_{1}+2{x}_{2} &=10 \\ {x}_{2} &=4 \\ 0 &=k-4.\end{aligned}\right.
$$

In order for this system to be consistent, we require $0=k-4,$ which means that $k=4.$

### tutorial 17592186121038 — Properties of the Column Space of a Matrix

The column space is defined for matrices of *any* dimensions. In general, if ${\color{black}\mathbf{a}_1}, {\color{black}\mathbf{a}_2}, \ldots, {\color{black}\mathbf{a}_n}$ are the columns of a matrix $A,$ that is to say,
$$
A = 
	\left[
		{\begin{array}{cccc}{\color{black}|} & {\color{black}|} &  & {\color{black}|} \\ {\color{black}{\mathbf{a}}_{1}} & {\color{black}{\mathbf{a}}_{2}} & \ldots  & {\color{black}{\mathbf{a}}_{n}} \\ {\color{black}|} & {\color{black}|} &  & {\color{black}|}\end{array}}
	\right],
$$
then $\textrm{Col}(A) = \textrm{Span} \{ {\color{black}\mathbf{a}_1}, {\color{black}\mathbf{a}_2}, \ldots, {\color{black}\mathbf{a}_n} \}.$

The column space satisfies the following properties:

- If $A$ is an ${\color{blue}m}\times n$ matrix, then $\textrm{Col}(A)$ is a subspace of $\mathbb{R}^{\color{blue}m}.$ This is because each column has ${\color{blue}m}$ entries.

- $\mathbf{b}\in\textrm{Col}(A)$ if and only if the equation $A\mathbf{x}=\mathbf{b}$ is consistent (has a solution).

- If the equation $A\mathbf{x}=\mathbf{b}$ is inconsistent (has no solution), then $\mathbf{b}\not\in\textrm{Col}(A).$

These hold for any $m\times n$ matrix, and the matrix does not necessarily have to be square.



### example 17592186119622 — Determining if a Vector Is in the Column Space of a Larger Matrix

The matrix $C$ and the vector $\mathbf{b}$ are given below. Determine if $\mathbf{b} \in \textrm{Col}(C).$ In affirmative case, find the value of $x_1 \cdot x_2 \cdot x_3$, where $x_1$, $x_2$, and $x_3$ are real numbers such that $\mathbf{b}=x_1\mathbf{c}_1+x_2\mathbf{c}_3+x_3\mathbf{c}_3,$ and $\mathbf{c}_1,$ $\mathbf{c}_2,$ and $\mathbf{c}_3$ are the respective columns of $C.$

$$
C={\left[ \begin{array}{ccc}1 & 1 & 4 \\ - 1 & 2 & 0 \\ 0 & - 3 & 1\end{array} \right]},
\qquad
\mathbf{b}={\left[ \begin{array}{c}5 \\ - 4 \\ 4\end{array} \right]}
$$

In order to determine whether $\mathbf{b}$ lies in $\textrm{Col}(C),$ we need to check if the equation $C\mathbf{x}=\mathbf{b}$ is consistent. So, let's find the row echelon form of the augmented matrix $[C \,|\, \mathbf{b}]$ as follows:

$$
\begin{aligned}{}[C\hspace{0.167em}|\hspace{0.167em}\mathbf{b}] & =\left[\begin{array}{ccc|c}1 & 1 & 4 & 5 \\ -1 & 2 & 0 & -4 \\ 0 & -3 & 1 & 4\end{array}\right] & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 4 & 5 \\ 0 & 3 & 4 & 1 \\ 0 & -3 & 1 & 4\end{array}\right] & {R}_{3} & :={R}_{3}+{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 4 & 5 \\ 0 & 3 & 4 & 1 \\ 0 & 0 & 5 & 5\end{array}\right]\end{aligned}
$$

Now, we have the system

$$
\left\{\begin{aligned}{x}_{1}+{x}_{2}+4{x}_{3} &=5 \\ 3{x}_{2}+4{x}_{3} &=1 \\ 5{x}_{3} &=5.\end{aligned}\right.
$$

From the third equation, we get $x_3=1$. Substituting into the second equation gives 

$$
\begin{aligned}3{x}_{2}+4(1) & =1 \\ 3{x}_{2} & =-3 \\ {x}_{2} & =-1.\end{aligned}
$$

Finally, from the first equation, we get 

$$
\begin{aligned}{x}_{1} & =5-{x}_{2}-4{x}_{3} \\  & =5-(-1)-4(1) \\  & =2.\end{aligned}
$$

Since we have a solution, the equation $C\mathbf{x}=\mathbf{b}$ is consistent, which implies that $\mathbf{b}\in\textrm{Col}(C).$ 

Moreover, there is exactly one solution, so we have exactly one way to write $\mathbf{b}$ as a linear combination of $\mathbf{c}_1,$ $\mathbf{c}_2,$ and $\mathbf{c}_3\mathbin{:}$
$$
\underbrace{ {\left[ \begin{array}{c}5 \\ - 4 \\ 4\end{array} \right]}}_{\mathbf{b}} =  2 \cdot \underbrace{ {\left[ \begin{array}{c}1 \\ - 1 \\ 0\end{array} \right]}}_{\mathbf{c}_1} + (-1) \cdot \underbrace{ {\left[ \begin{array}{c}1 \\ 2 \\ - 3\end{array} \right]}}_{\mathbf{c}_2}+ 1 \cdot \underbrace{ {\left[ \begin{array}{c}4 \\ 0 \\ 1\end{array} \right]}}_{\mathbf{c}_3}
$$

Finally, we get $x_1 \cdot x_2 \cdot x_3 = 2 \cdot (-1) \cdot 1 = -2$.

## Representative practice (first three per skill; full bank in practice.json)

### Determining if a Vector is in the Column Space of a Matrix (12 captured questions)

Question 17592186120313 — None

The matrix $B$ and the vector $\mathbf{b}$ are given below. Determine if $b ∈ Col(B)$. In the affirmative case, find the value of $x_{1} \cdot x_{2}$, where $x_{1}$ and $x_{2}$ are real numbers such that $\mathbf{b}={x}_{1}{\mathbf{b}}_{1}+{x}_{2}{\mathbf{b}}_{2}$, and ${\mathbf{b}}_{1}$, ${\mathbf{b}}_{2}$ are the respective columns of $B$.

$$
B=\begin{bmatrix}2 & -1 \\ 4 & 0\end{bmatrix},\hspace{2em}\mathbf{b}=\begin{bmatrix}1 \\ -4\end{bmatrix}
$$

Solution: To decide whether $b\in\operatorname{Col}(B)$, solve $B\mathbf{x}=b$:

$$
\left\{\begin{aligned}2x_1-x_2&=1\\4x_1&=-4.\end{aligned}\right.
$$

The second equation gives $x_1=-1$. Substitution into the first gives $x_2=-3$. Thus the system is consistent, so $b\in\operatorname{Col}(B)$, and $x_1x_2=(-1)(-3)=3$.

Answer selection: 3

Question 17592186120339 — question.difficulty/easy

The matrix $H$ and the vector $\mathbf{b}$ are given below. Determine if $\mathbf{b}\in \text{Col}(H).$ In the affirmative case, find the value of ${x}_{1}\cdot {x}_{2}$, where ${x}_{1}$ and ${x}_{2}$ are real numbers such that $\mathbf{b}={x}_{1}{\mathbf{h}}_{1}+{x}_{2}{\mathbf{h}}_{2},$ and ${\mathbf{h}}_{1},$ ${\mathbf{h}}_{2}$ are the respective columns of $H.$

$$
H=\begin{bmatrix}-1 & 4 \\ 0 & 1 \\ 0 & 2\end{bmatrix},\hspace{2em}\mathbf{b}=\begin{bmatrix}7 \\ 2 \\ 2\end{bmatrix}
$$

Solution: In order to determine whether $b$ lies in $\text{Col}(H),$ we need to check if the equation $Hx=b$ is consistent. So, let's find the row echelon form of the augmented matrix $[H\,|\,b]$ as follows:

$$
\begin{aligned}{}[H\,|\,b] & =\left[\begin{array}{cc|c}-1 & 4 & 7 \\ 0 & 1 & 2 \\ 0 & 2 & 2\end{array}\right] & {R}_{3} & :={R}_{3}-2{R}_{2} \\  & ∼\left[\begin{array}{cc|c}-1 & 4 & 7 \\ 0 & 1 & 2 \\ 0 & 0 & -2\end{array}\right]\end{aligned}
$$

Now, we have the system

$$
\left\{\begin{aligned}-{x}_{1}+4{x}_{2} &=7 \\ {x}_{2} &=2 \\ 0 &=-2.\end{aligned}\right.
$$

From the third equation, we get the false statement $0=-2.$ 

Therefore, the system is inconsistent, which implies that $b\notin \text{Col}(H).$

Answer selection: \mathbf{b}\notin \text{Col}(H)

Question 17592186247182 — question.difficulty/easy

The matrix $A$ and the vector $\mathbf{b}$ are given below. Determine if $\mathbf{b}\in \text{Col}(A).$ In the affirmative case, find the value of ${x}_{1}\cdot {x}_{2}$, where ${x}_{1}$ and ${x}_{2}$ are real numbers such that $\mathbf{b}={x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2},$ and ${\mathbf{a}}_{1},$ ${\mathbf{a}}_{2}$ are the respective columns of $A.$

$$
A=\begin{bmatrix}1 & 2 \\ \hspace{-0.167em}\hspace{-0.167em}-2 & \hspace{-0.167em}\hspace{-0.167em}-2 \\ \hspace{-0.167em}\hspace{-0.167em}-1 & \hspace{-0.167em}\hspace{-0.167em}-1\end{bmatrix},\hspace{2em}\mathbf{b}=\begin{bmatrix}\hspace{-0.167em}\hspace{-0.167em}-4 \\ 2 \\ 2\end{bmatrix}
$$

Solution: In order to determine whether $\mathbf{b}$ lies in $\text{Col}(A),$ we need to check if the equation $A\mathbf{x}=\mathbf{b}$ is consistent. So, let's find the row echelon form of the augmented matrix $[A\hspace{0.167em}|\hspace{0.167em}\mathbf{b}]$ as follows:

$$
\begin{aligned}{}[A\,|\,b] & =\left[\begin{array}{cc|c}1 & 2 & \,\,-4 \\ \,\,-2 & \,\,-2 & 2 \\ \,\,-1 & \,\,-1 & 2\end{array}\right] &  & \begin{aligned}{R}_{2}:={R}_{2}+2{R}_{1} \\ {R}_{3}:={R}_{3}+{R}_{1}\end{aligned} \\  & ∼\left[\begin{array}{cc|c}1 & 2 & \,\,-4 \\ 0 & \,\,2 & -6 \\ 0 & 1 & -2\end{array}\right] &  & {R}_{3}:={R}_{3}-\frac{1}{2}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & 2 & \,\,-4 \\ 0 & \,\,2 & -6 \\ 0 & 0 & 1\end{array}\right]\end{aligned}
$$

Now, we have the system

$$
\left\{\begin{aligned}{x}_{1}+2{x}_{2} &=-4 \\ 2{x}_{2} &=-6 \\ 0 &=1.\end{aligned}\right.
$$

From the third equation, we get the false statement $0=1.$ 

Therefore, the system is inconsistent, which implies that $\mathbf{b}\notin \text{Col}(A).$

Answer selection: \mathbf{b}\notin \text{Col}(A)

### Determining the Value of an Unknown Given a Vector That’s in the Column Space of a Matrix (16 captured questions)

Question 17592186120397 — question.difficulty/moderate

Consider the matrix given by $A=\begin{bmatrix}3 & 8 \\ -2 & -11 \\ 1 & 6\end{bmatrix}.$ Determine the value of $k$ for which the vector $\mathbf{b}=\begin{bmatrix}14 \\ -15 \\ k+5\end{bmatrix}$ belongs to $\text{Col}(A).$

Solution: If $b$ lies in $\text{Col}(A),$ then the equation $Ax=b$ must be consistent. So, let's find the row echelon form of the augmented matrix $[A\,|\,b]$ as follows:

$$
\begin{aligned}{}[A\,|\,b] & =\left[\begin{array}{cc|c}3 & 8 & 14 \\ -2 & -11 & -15 \\ 1 & 6 & k+5\end{array}\right] & {R}_{1} & ↔{R}_{3} \\  & ∼\left[\begin{array}{cc|c}1 & 6 & k+5 \\ -2 & -11 & -15 \\ 3 & 8 & 14\end{array}\right] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 6 & k+5 \\ 0 & 1 & 2k-5 \\ 3 & 8 & 14\end{array}\right] & {R}_{3} & :={R}_{3}-3{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 6 & k+5 \\ 0 & 1 & 2k-5 \\ 0 & -10 & -3k-1\end{array}\right] & {R}_{3} & :={R}_{3}+10{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & 6 & k+5 \\ 0 & 1 & 2k-5 \\ 0 & 0 & 17k-51\end{array}\right]\end{aligned}
$$

So, we have the system

$$
\left\{\begin{aligned}{x}_{1}+6{x}_{2} &=k+5 \\ {x}_{2} &=2k-5 \\ 0 &=17k-51.\end{aligned}\right.
$$

In order for this system to be consistent, we require $0=17k-51,$ which means that $k=3.$

Answer selection: 3

Question 17592186120398 — question.difficulty/easy

Consider the matrix given by $A = \begin{bmatrix}1 & -2 \\ 2 & -2 \\ 5 & -8\end{bmatrix}$. Determine the value of $k$ for which the vector $\mathbf{b}=\begin{bmatrix}1 \\ 3 \\ k\end{bmatrix}$ belongs to $Col(A)$.

Solution: For $b$ to lie in $\operatorname{Col}(A)$, the system $A\mathbf{x}=b$ must be consistent. Subtract twice row 1 from row 2 and five times row 1 from row 3:

$$
\left[\begin{array}{cc|c}1&-2&1\\2&-2&3\\5&-8&k\end{array}\right]
\sim\left[\begin{array}{cc|c}1&-2&1\\0&2&1\\0&2&k-5\end{array}\right]
\sim\left[\begin{array}{cc|c}1&-2&1\\0&2&1\\0&0&k-6\end{array}\right].
$$

The last row requires $0=k-6$, so $k=6$.

Answer selection: 6

Question 17592186247187 — question.difficulty/easy

Consider the matrix given by $A=\begin{bmatrix}1 & -3 \\ -1 & 1 \\ 2 & -2\end{bmatrix}.$ Determine the value of $k$ for which the vector $\mathbf{b}=\begin{bmatrix}1 \\ -5 \\ k\end{bmatrix}$ belongs to $\text{Col}(A).$

Solution: If $\mathbf{b}$ lies in $\text{Col}(A),$ then the equation $A\mathbf{x}=\mathbf{b}$ must be consistent. So, let's find the row echelon form of the augmented matrix $[A\hspace{0.167em}|\hspace{0.167em}\mathbf{b}]$ as follows:

$$
\begin{aligned}{}[A\hspace{0.167em}|\hspace{0.167em}\mathbf{b}] & =\left[\begin{array}{cc|c}1 & -3 & 1 \\ -1 & 1 & -5 \\ 2 & -2 & k\end{array}\right] & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & 1 \\ 0 & -2 & -4 \\ 2 & -2 & k\end{array}\right] & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & 1 \\ 0 & -2 & -4 \\ 0 & 4 & k-2\end{array}\right] & {R}_{3} & :={R}_{3}+2{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & 1 \\ 0 & -2 & -4 \\ 0 & 0 & k-10\end{array}\right]\end{aligned}
$$

So, we have the system

$$
\left\{\begin{aligned}{x}_{1}-3{x}_{2} &=1 \\ -2{x}_{2} &=-4 \\ 0 &=k-10.\end{aligned}\right.
$$

In order for this system to be consistent, we require $0=k-10,$ which means that $k=10.$

Answer selection: 10

### Determining if a Vector Is in the Column Space of a Larger Matrix (16 captured questions)

Question 17592186120314 — None

The matrix $C$ and the vector $\mathbf{b}$ are given below.
Determine if $b ∈ Col(C)$.
In the affirmative case, find the value of $x_{1} \cdot x_{2} \cdot x_{3}$, where $x_{1}, x_{2}$ and $x_{3}$ are real numbers such that $\mathbf{b}={x}_{1}{\mathbf{c}}_{\mathbf{1}}+{x}_{2}{\mathbf{c}}_{\mathbf{2}}+{x}_{3}{\mathbf{c}}_{\mathbf{3}}$, and ${\mathbf{c}}_{1}$, ${\mathbf{c}}_{2}$, and ${\mathbf{c}}_{\mathbf{3}}$ are the respective columns of $C$.

$$
C=\begin{bmatrix}1 & -1 & 3 \\ 2 & 0 & 4 \\ 1 & -3 & 0\end{bmatrix},\hspace{2em}\mathbf{b}=\begin{bmatrix}2 \\ -1 \\ 7\end{bmatrix}
$$

Solution: Solve $C\mathbf{x}=b$ using Gaussian elimination:

$$
\left[\begin{array}{ccc|c}1&-1&3&2\\2&0&4&-1\\1&-3&0&7\end{array}\right]
\sim\left[\begin{array}{ccc|c}1&-1&3&2\\0&2&-2&-5\\0&-2&-3&5\end{array}\right]
\sim\left[\begin{array}{ccc|c}1&-1&3&2\\0&2&-2&-5\\0&0&-5&0\end{array}\right].
$$

Back-substitution gives $x_3=0$, $x_2=-\frac52$, and $x_1=-\frac12$. The system is consistent, so $b\in\operatorname{Col}(C)$. Finally, $x_1x_2x_3=0$.

Answer selection: 0

Question 17592186120515 — question.difficulty/hard

The matrix $E$ and the vector $\mathbf{b}$ are given below.
Determine if $\mathbf{b}\in \text{Col}(E).$ 
In the affirmative case, find the value of ${x}_{1}\cdot {x}_{2}\cdot {x}_{3}\cdot {x}_{4}$, where ${x}_{1}$, ${x}_{2}$, ${x}_{3}$, and ${x}_{4}$ are real numbers such that $\mathbf{b}={x}_{1}{\mathbf{e}}_{\mathbf{1}}+{x}_{2}{\mathbf{e}}_{\mathbf{2}}+{x}_{3}{\mathbf{e}}_{\mathbf{3}}+{x}_{4}{\mathbf{e}}_{\mathbf{4}},$ and ${\mathbf{e}}_{1}$, ${\mathbf{e}}_{2}$, ${\mathbf{e}}_{3}$, and ${\mathbf{e}}_{4}$ are respective columns of $E.$

$$
E=\begin{bmatrix}1 & -4 & 7 & 1 \\ 4 & -16 & 28 & 4 \\ 1 & -3 & 0 & -1\end{bmatrix},\hspace{2em}\mathbf{b}=\begin{bmatrix}2 \\ 7 \\ 0\end{bmatrix}
$$

Solution: In order to determine whether $\mathbf{b}$ lies in $\text{Col}(E),$ we need to check if the equation $E\mathbf{x}=\mathbf{b}$ is consistent. So, let's find the row echelon form of the augmented matrix $[E\hspace{0.167em}|\hspace{0.167em}\mathbf{b}]$ as follows:

$$
\begin{aligned}{}[E\hspace{0.167em}|\hspace{0.167em}\mathbf{b}] & =\left[\begin{array}{cccc|c}1 & -4 & 7 & 1 & 2 \\ 4 & -16 & 28 & 4 & 7 \\ 1 & -3 & 0 & -1 & 0\end{array}\right] & {R}_{2} & :={R}_{2}+(-4){R}_{1} \\  & ∼\left[\begin{array}{cccc|c}1 & -4 & 7 & 1 & 2 \\ \text{ }0 & 0 & 0 & 0 & -1 \\ 1 & -3 & 0 & -1 & 0\end{array}\right]\end{aligned}
$$

Now, we have the system

$$
\left\{\begin{aligned}{x}_{1}-4{x}_{2}+7{x}_{3}+{x}_{4} &=2 \\ 0 &=-1 \\ {x}_{1}-3{x}_{2}-{x}_{4} &=0.\end{aligned}\right.
$$

From the second equation, we get a false statement $0=-1.$ Therefore, the system is inconsistent, and we conclude that $\mathbf{b}\notin \text{Col}(E).$

Answer selection: \mathbf{b}\notin \text{Col}(E)

Question 17592186247191 — question.difficulty/moderate

The matrix $C$ and the vector $\mathbf{b}$ are given below.
Determine if $\mathbf{b}\in \text{Col}(C).$ 
In the affirmative case, find the value of ${x}_{1}\cdot {x}_{2}\cdot {x}_{3}$, where ${x}_{1},{x}_{2}$ and ${x}_{3}$ are real numbers such that $\mathbf{b}={x}_{1}{\mathbf{c}}_{\mathbf{1}}+{x}_{2}{\mathbf{c}}_{\mathbf{2}}+{x}_{3}{\mathbf{c}}_{\mathbf{3}},$ and ${\mathbf{c}}_{1}$, ${\mathbf{c}}_{2}$, and ${\mathbf{c}}_{\mathbf{3}}$ are the respective columns of $C.$

$$
C=\begin{bmatrix}1 & 3 & 3 \\ 0 & 2 & -1 \\ -1 & 1 & 0\end{bmatrix},\hspace{2em}\mathbf{b}=\begin{bmatrix}-8 \\ -12 \\ -6\end{bmatrix}
$$

Solution: In order to determine whether $\mathbf{b}$ lies in $\text{Col}(C),$ we need to check if the equation $C\mathbf{x}=\mathbf{b}$ is consistent. So, let's find the row echelon form of the augmented matrix $[C\hspace{0.167em}|\hspace{0.167em}\mathbf{b}]$ as follows:

$$
\begin{aligned}{}[C\hspace{0.167em}|\hspace{0.167em}\mathbf{b}] & =\left[\begin{array}{ccc|c}1 & 3 & 3 & -8 \\ 0 & 2 & -1 & -12 \\ -1 & 1 & 0 & -6\end{array}\right] & {R}_{3} & :={R}_{3}+{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & 3 & -8 \\ 0 & 2 & -1 & -12 \\ 0 & 4 & 3 & -14\end{array}\right] & {R}_{3} & :={R}_{3}-2{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 3 & 3 & -8 \\ 0 & 2 & -1 & -12 \\ 0 & 0 & 5 & 10\end{array}\right]\end{aligned}
$$

Now, we have the system

$$
\left\{\begin{aligned}{x}_{1}+3{x}_{2}+3{x}_{3} &=-8 \\ 2{x}_{2}-{x}_{3} &=-12 \\ 5{x}_{3} &=10.\end{aligned}\right.
$$

From the third equation, we get ${x}_{3}=2.$ Substituting it into the second equation gives 

$$
\begin{aligned}2{x}_{2}-(2) & =-12 \\ {x}_{2} & =-5.\end{aligned}
$$

Finally, from the first equation, we get 

$$
\begin{aligned}{x}_{1} & =-8-3{x}_{2}-3{x}_{3} \\  & =-8-3(-5)-3(2) \\  & =1.\end{aligned}
$$

Since we have a solution, the equation $C\mathbf{x}=\mathbf{b}$ is consistent, which implies that $\mathbf{b}\in \text{Col}(C).$ 

Moreover, there is exactly one solution, so we have exactly one way to write $\mathbf{b}$ as a linear combination of ${\mathbf{c}}_{1},$ ${\mathbf{c}}_{2},$ and ${\mathbf{c}}_{3}:$

$$
\underbrace{\begin{bmatrix}-8 \\ -12 \\ -6\end{bmatrix}}_{\mathbf{b}}=1\cdot \underbrace{\begin{bmatrix}1 \\ 0 \\ -1\end{bmatrix}}_{{\mathbf{c}}_{1}}+(-5)\cdot \underbrace{\begin{bmatrix}3 \\ 2 \\ 1\end{bmatrix}}_{{\mathbf{c}}_{2}}+2\cdot \underbrace{\begin{bmatrix}3 \\ -1 \\ 0\end{bmatrix}}_{{\mathbf{c}}_{3}}
$$

Finally, we get ${x}_{1}\cdot {x}_{2}\cdot {x}_{3}=1\cdot (-5)\cdot 2=-10.$

Answer selection: -10
