# 17592186049222 Finding a Basis of a Span

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121040 — Introduction

A **basis** of a subspace $U$ (in $\mathbb{R}^n$) is a set of vectors in $\mathbb{R}^n$ that is linearly independent and spans $U.$

For example, consider the following subspace consisting of the span of three vectors:
$$
U = \textrm{Span}
	\Bigg\{ 
		\underbrace{ {\left[ \begin{array}{c}{\color{blue}1} \\ {\color{blue}0}\end{array} \right]}}_{\color{blue}\mathbf{a}_1}, 
		\underbrace{ {\left[ \begin{array}{c}{\color{blue}0} \\ {\color{blue}1}\end{array} \right]}}_{\color{blue}\mathbf{a}_2}, 
		\underbrace{ {\left[ \begin{array}{c}{\color{red}- 1} \\ {\color{red}3}\end{array} \right]}}_{\color{red}\mathbf{a}_3} 
	\Bigg\}
$$

To find a basis of $U,$ we need to find a set of linearly independent vectors that spans $U.$

**Watch out!** The set
$$
\Bigg\{ 
		\underbrace{ {\left[ \begin{array}{c}{\color{blue}1} \\ {\color{blue}0}\end{array} \right]}}_{\color{blue}\mathbf{a}_1}, 
		\underbrace{ {\left[ \begin{array}{c}{\color{blue}0} \\ {\color{blue}1}\end{array} \right]}}_{\color{blue}\mathbf{a}_2}, 
		\underbrace{ {\left[ \begin{array}{c}{\color{red}- 1} \\ {\color{red}3}\end{array} \right]}}_{\color{red}\mathbf{a}_3} 
	\Bigg\}
$$
is *not* a basis of $U.$ It's true that this set *spans* $U,$ but the vectors in this set are *not* linearly independent. In particular, the vector $\color{red}\mathbf{a}_3$ can be written as a linear combination of $\color{blue}\mathbf{a}_1$ and $\color{blue}\mathbf{a}_2$ as follows:

$$
\underbrace{ {\left[ \begin{array}{c}{\color{red}- 1} \\ {\color{red}3}\end{array} \right]} }_{\color{red}\mathbf{a}_3} = 
	(-1) \cdot \underbrace{ {\left[ \begin{array}{c}{\color{blue}1} \\ {\color{blue}0}\end{array} \right]} }_{\color{blue}\mathbf{a}_1} + 
	3 \cdot \underbrace{ {\left[ \begin{array}{c}{\color{blue}0} \\ {\color{blue}1}\end{array} \right]} }_{\color{blue}\mathbf{a}_2}
$$

To find a basis of $U = \textrm{Span} \{ {\color{blue}\mathbf{a}_1}, {\color{blue}\mathbf{a}_2}, {\color{red}\mathbf{a}_3} \},$ we can start with $\{ {\color{blue}\mathbf{a}_1}, {\color{blue}\mathbf{a}_2}, {\color{red}\mathbf{a}_3} \},$ but we need to remove any "redundant" vectors that can be written as a linear combination of other vectors in the set. In this case, we remove ${\color{red}\mathbf{a}_3}$ because it can be written as a linear combination of $\color{blue}\mathbf{a}_1$ and ${\color{blue}\mathbf{a}_2}.$

We are left with the set

$$
\Bigg\{ 
		\underbrace{ {\left[ \begin{array}{c}{\color{blue}1} \\ {\color{blue}0}\end{array} \right]}}_{\color{blue}\mathbf{a}_1}, 
		\underbrace{ {\left[ \begin{array}{c}{\color{blue}0} \\ {\color{blue}1}\end{array} \right]}}_{\color{blue}\mathbf{a}_2}
	\Bigg\}.
$$

These two vectors are linearly independent (since they are not parallel), and removing a redundant vector does not change the span, so these vectors still span $U.$ That is to say,

$$
U = \textrm{Span} \{ {\color{blue}\mathbf{a}_1}, {\color{blue}\mathbf{a}_2}, {\color{red}\mathbf{a}_3} \} = \textrm{Span} \{ {\color{blue}\mathbf{a}_1}, {\color{blue}\mathbf{a}_2} \}.
$$

Therefore, the set $\mathcal{B} = \{ {\color{blue}\mathbf{a}_1}, {\color{blue}\mathbf{a}_2} \}$ is a basis of $U.$

**Note:** To see that the vectors $\{ {\color{blue}\mathbf{a}_1}, {\color{blue}\mathbf{a}_2} \}$ still span $U,$ first note that any vector $\mathbf{b} \in U$ can be written as a linear combination of the three original vectors:

$$
\mathbf{b} = x_1 {\color{blue}\mathbf{a}_1} + x_2 {\color{blue}\mathbf{a}_2} + x_3 {\color{red}\mathbf{a}_3}
$$

Since ${\color{red}\mathbf{a}_3} = -{\color{blue}\mathbf{a}_1}+3{\color{blue}\mathbf{a}_2},$ then we must have 

$$
\begin{aligned}\mathbf{b} & ={x}_{1}{\color{blue}{\mathbf{a}}_{1}}+{x}_{2}{\color{blue}{\mathbf{a}}_{2}}+{x}_{3}(-{\color{blue}{\mathbf{a}}_{1}}+3{\color{blue}{\mathbf{a}}_{2}}) \\  & =({x}_{1}-{x}_{3}){\color{blue}{\mathbf{a}}_{1}}+({x}_{2}+3{x}_{3}){\color{blue}{\mathbf{a}}_{2}},\end{aligned}
$$

which shows that $\mathbf{b}$ can actually be written as a linear combination of only two vectors, ${\color{blue}\mathbf{a}_1}$ and ${\color{blue}\mathbf{a}_2}.$

Therefore, we can conclude that the set $\{ {\color{blue}\mathbf{a}_1}, {\color{blue}\mathbf{a}_2} \}$ spans the subspace $U = \textrm{Span} \{ {\color{blue}\mathbf{a}_1}, {\color{blue}\mathbf{a}_2}, {\color{red}\mathbf{a}_3} \}.$



### example 17592186119626 — Finding a Basis of the Space Spanned by a Set of Vectors Using Inspection

Consider the vectors $$
\displaystyle \mathbf{a}_1={\left[ \begin{array}{c}2 \\ 3\end{array} \right]},\mathbf{a}_2={\left[ \begin{array}{c}3 \\ 4\end{array} \right]},
$$ and $\mathbf{a}_3={\left[ \begin{array}{c}1 \\ 1\end{array} \right]}.$ Find a basis of $S=\textrm{Span}\{\mathbf{a}_1,\mathbf{a}_2,\mathbf{a}_3 \}$ by inspection.

Remember that a basis of $S$ is a set of linearly independent vectors that spans $S.$

From the given vectors, we can see that $\mathbf{a}_2$ is a linear combination of vectors $\mathbf{a}_1$ and $\mathbf{a}_3\mathbin{:}$

$$
\mathbf{a}_2=1\cdot \mathbf{a}_1+1\cdot \mathbf{a}_3
$$

Consequently, the vector $\mathbf{a}_2$ can be removed from $\textrm{Span}\{\mathbf{a}_1,\mathbf{a}_2,\mathbf{a}_3 \}$ without changing the span. So $S = \textrm{Span}\{\mathbf{a}_1,\mathbf{a}_2,\mathbf{a}_3 \}$ is spanned by just $\{\mathbf{a}_1,\mathbf{a}_3\}.$ 

Lastly, note that $\mathbf{a}_1$ and $\mathbf{a}_3$ are linearly independent since they are not parallel. So the set $\{\mathbf{a}_1,\mathbf{a}_3\}$ is a linearly independent set that spans $S.$

Therefore, a basis of $S$ is $\{\mathbf{a}_1,\mathbf{a}_3\},$ that is to say,

$$
\mathcal{B} = \Bigg\{ 
		\underbrace{ {\left[ \begin{array}{c}2 \\ 3\end{array} \right]}}_{\color{black}\mathbf{a}_1}, 
		\underbrace{ {\left[ \begin{array}{c}1 \\ 1\end{array} \right]}}_{\color{black}\mathbf{a}_3} 
	\Bigg\}.
$$

### tutorial 17592186121064 — Finding a Basis by Identifying Pivot Columns

In the previous example, it was easy to see that one vector was a linear combination of the others. But what can we do when it's not so easy to tell? For example, consider the subspace

$$
U = \textrm{Span}
	\Bigg\{ 
		\underbrace{ {\left[ \begin{array}{c}1 \\ - 2\end{array} \right]}}_{\color{black}\mathbf{a}_1}, 
		\underbrace{ {\left[ \begin{array}{c}- 1 \\ 3\end{array} \right]}}_{\color{black}\mathbf{a}_2}, 
		\underbrace{ {\left[ \begin{array}{c}- 1 \\ 7\end{array} \right]}}_{\color{black}\mathbf{a}_3} 
	\Bigg\}.
$$

To find a subset of linearly independent vectors, we can put the vectors in a matrix and compute the reduced row echelon form:

$$
\begin{aligned} & \phantom{=\hspace{0.222em}\hspace{0.167em}}\begin{bmatrix}1 & -1 & -1 \\ -2 & 3 & 7\end{bmatrix} & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & -1 & -1 \\ 0 & 1 & 5\end{bmatrix} & {R}_{1} & :={R}_{1}+{R}_{2} \\  & ∼\begin{bmatrix}\bbox[lightgray, 2pt]{{\color{blue}1}} & 0 & {\color{red}4} \\ 0 & \bbox[lightgray, 2pt]{{\color{blue}1}} & {\color{red}5}\end{bmatrix}\end{aligned}
$$

The pivot columns correspond to linearly independent vectors, while the non-pivot columns correspond to linearly dependent (or redundant) vectors that can be removed. Here, the $1$st and $2$nd columns are pivot columns, while the $3$rd column is a non-pivot column.

**But watch out!** We need to pick the pivot columns from the *original matrix*, not from the reduced one.

The $1$st and $2$nd columns from the original matrix are $\mathbf{a}_1$ and $\mathbf{a}_2.$ So, a basis of $U$ is $\{ \mathbf{a}_1, \mathbf{a}_2 \},$ that is to say, 

$$
\mathcal{B} = \Bigg\{ 
		\underbrace{ {\left[ \begin{array}{c}1 \\ - 2\end{array} \right]}}_{\color{black}\mathbf{a}_1}, 
		\underbrace{ {\left[ \begin{array}{c}- 1 \\ 3\end{array} \right]}}_{\color{black}\mathbf{a}_2} 
	\Bigg\}.
$$



### example 17592186119672 — Finding a Basis of the Space Spanned by a Set of Vectors by Identifying Pivot Columns

Consider the vectors $\mathbf{a}_1={\left[ \begin{array}{c}5 \\ 2\end{array} \right]},$ $\mathbf{a}_2={\left[ \begin{array}{c}10 \\ 4\end{array} \right]},$ and $\mathbf{a}_3={\left[ \begin{array}{c}15 \\ 5\end{array} \right]}.$ Find a basis of $S=\textrm{Span}\{\mathbf{a}_1,\mathbf{a}_2,\mathbf{a}_3 \}.$

We need to find a subset of linearly independent vectors. So, we start by creating a matrix whose columns are made up of our vectors, and then we reduce the matrix to row echelon form:

$$
\begin{aligned} & \begin{bmatrix}5 & 10 & 15 \\ 2 & 4 & 5\end{bmatrix} & {R}_{1} & :=\frac{1}{5}{R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 3 \\ 2 & 4 & 5\end{bmatrix} & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 3 \\ 0 & 0 & -1\end{bmatrix}\end{aligned}
$$

The pivot columns correspond to linearly independent vectors, while the non-pivot columns correspond to linearly dependent vectors that can be removed. Here, the $1$st and $3$rd columns are pivot columns, while the $2$nd column is a non-pivot column.

Remember that we need to pick the pivot columns from the *original matrix*, not from the reduced one.

The $1$st and $3$rd columns from the original matrix are $\mathbf{a}_1$ and $\mathbf{a}_3.$ So, a basis of $S$ is $\{ \mathbf{a}_1, \mathbf{a}_3 \},$ that is to say, 

$$
\mathcal{B} = \Bigg\{ 
		\underbrace{ {\left[ \begin{array}{c}5 \\ 2\end{array} \right]}}_{\color{black}\mathbf{a}_1}, 
		\underbrace{ {\left[ \begin{array}{c}15 \\ 5\end{array} \right]}}_{\color{black}\mathbf{a}_3} 
	\Bigg\}.
$$

### tutorial 17592186121065 — Finding a Particular Linear Combination of Vectors

Earlier, we computed a basis of 

$$
U = \textrm{Span}
	\Bigg\{ 
		\underbrace{ {\left[ \begin{array}{c}1 \\ - 2\end{array} \right]}}_{\color{black}\mathbf{a}_1}, 
		\underbrace{ {\left[ \begin{array}{c}- 1 \\ 3\end{array} \right]}}_{\color{black}\mathbf{a}_2}, 
		\underbrace{ {\left[ \begin{array}{c}- 1 \\ 7\end{array} \right]}}_{\color{black}\mathbf{a}_3} 
	\Bigg\}.
$$

The basis that we found was

$$
\mathcal{B} = \Bigg\{ 
		\underbrace{ {\left[ \begin{array}{c}1 \\ - 2\end{array} \right]}}_{\color{black}\mathbf{a}_1}, 
		\underbrace{ {\left[ \begin{array}{c}- 1 \\ 3\end{array} \right]}}_{\color{black}\mathbf{a}_2} 
	\Bigg\}.
$$

The vector $\mathbf{a}_3$ was not included in the basis. This means that $\mathbf{a}_3$ can be written as a linear combination of $\mathbf{a}_1$ and $\mathbf{a}_2.$

Now, what if we want to find the exact linear combination of $\mathbf{a}_1$ and $\mathbf{a}_2$ that yields $\mathbf{a}_3?$ That is to say, we want to find $x_1, x_2 \in \mathbb{R}$ such that 

$$
{\color{black}x_1} \underbrace{ {\left[ \begin{array}{c}1 \\ - 2\end{array} \right]}}_{\mathbf{a}_1} + {\color{rblack}x_2} \underbrace{ {\left[ \begin{array}{c}- 1 \\ 3\end{array} \right]}}_{\mathbf{a}_2} = \underbrace{ {\left[ \begin{array}{c}- 1 \\ 7\end{array} \right]}}_{\mathbf{a}_3}.
$$

This is equivalent to a system with the augmented matrix
$$
\left[
	{\begin{array}{cc|c}1 & - 1 & - 1 \\ - 2 & 3 & 7\end{array}}
	\right].
$$

If we reduced this matrix to the *reduced* row echelon form, we get

$$
\left[
	{\begin{array}{cc|c}\bbox[3pt,lightgray]{ {\color{blue}1}} & 0 & {\color{red}4} \\ 0 & \bbox[3pt,lightgray]{ {\color{blue}1}} & {\color{red}5}\end{array}}
	\right].
$$

Finally, the third column of the *reduced* matrix tells us that $x_1=4$ and $x_2=5,$ meaning that
$$
\underbrace{ {\left[ \begin{array}{c}- 1 \\ 7\end{array} \right]}}_{\mathbf{a}_3} = {\color{red}4}\cdot \underbrace{ {\left[ \begin{array}{c}1 \\ - 2\end{array} \right]}}_{\mathbf{a}_1} + {\color{red}5}\cdot \underbrace{ {\left[ \begin{array}{c}- 1 \\ 3\end{array} \right]}}_{\mathbf{a}_2}.
$$

**Watch out!** The matrix must be written in *reduced* row echelon form (with $1$'s for pivots and $0$'s above and below the pivots), not just row echelon form.



### example 17592186119673 — Determining Whether a Given Set Is a Basis of a Span

The vectors $\mathbf{a}_1,$ $\mathbf{a}_2,$ $\mathbf{a}_3,$ and $\mathbf{a}_4$ are given below. Determine whether $\mathcal{B} = \{ \mathbf{a}_1, \mathbf{a}_2, \mathbf{a}_3 \}$ is a basis of $\textrm{Span}\{\mathbf{a}_1,\mathbf{a}_2,\mathbf{a}_3, \mathbf{a}_4 \}.$ If that is the case, find $x_1 + x_2 + x_3,$ where $\mathbf{a}_4=x_1\mathbf{a}_1+x_2\mathbf{a}_2+x_3\mathbf{a}_3.$
$$
\mathbf{a}_1={\left[ \begin{array}{c}1 \\ - 1 \\ - 3\end{array} \right]}, \qquad
\mathbf{a}_2={\left[ \begin{array}{c}0 \\ 1 \\ 0\end{array} \right]}, \qquad
\mathbf{a}_3={\left[ \begin{array}{c}1 \\ - 1 \\ - 2\end{array} \right]}, \qquad
\mathbf{a}_4={\left[ \begin{array}{c}2 \\ - 2 \\ 1\end{array} \right]}
$$

We want to determine if $\mathcal{B}$ is indeed a basis of $\textrm{Span}\{\mathbf{a}_1,\mathbf{a}_2,\mathbf{a}_3,\mathbf{a}_4 \}.$ So, we want to find $x_1, x_2, x_3 \in \mathbb{R}$ such that 
$$
{\color{black}x_1} \underbrace{ {\left[ \begin{array}{c}1 \\ - 1 \\ - 3\end{array} \right]}}_{\mathbf{a}_1} + {\color{rblack}x_2} \underbrace{ {\left[ \begin{array}{c}0 \\ 1 \\ 0\end{array} \right]}}_{\mathbf{a}_2} + {\color{rblack}x_3} \underbrace{ {\left[ \begin{array}{c}1 \\ - 1 \\ - 2\end{array} \right]}}_{\mathbf{a}_3}  = \underbrace{ {\left[ \begin{array}{c}2 \\ - 2 \\ 1\end{array} \right]}}_{\mathbf{a}_4}.
$$

This equation is equivalent to the system

$$
\left\{\begin{aligned}{x}_{1}+{x}_{3} &=2 \\ -{x}_{1}+{x}_{2}-{x}_{3} &=-2 \\ -3{x}_{1}-2{x}_{3} &=1\end{aligned}\right.
$$

Now, we reduce the augmented matrix of the system to reduced row echelon form (RREF):

$$
\begin{aligned} & \,\,\left[\begin{array}{ccc|c}1 & 0 & 1 & 2 \\ -1 & 1 & -1 & -2 \\ -3 & 0 & -2 & 1\end{array}\right] & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 1 & 2 \\ 0 & 1 & 0 & 0 \\ -3 & 0 & -2 & 1\end{array}\right] & {R}_{3} & :={R}_{3}+3{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 1 & 2 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 7\end{array}\right] & {R}_{1} & :={R}_{1}+(-1){R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 0 & -5 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 7\end{array}\right]\end{aligned}
$$

From the reduced matrix above, we see that the pivot columns are the $1$st, $2$nd, and $3$rd columns. So,  $\mathcal{B}$ is indeed a basis of $\textrm{Span}\{\mathbf{a}_1,\mathbf{a}_2,\mathbf{a}_3,\mathbf{a}_4 \}.$
Also, the matrix tells us that $x_1=-5,$ $x_2=0,$ and $x_3=7,$ meaning that
$$
(-5) \cdot \underbrace{ {\left[ \begin{array}{c}1 \\ - 1 \\ - 3\end{array} \right]}}_{\mathbf{a}_1} + 0 \cdot \underbrace{ {\left[ \begin{array}{c}0 \\ 1 \\ 0\end{array} \right]}}_{\mathbf{a}_2} + 7 \cdot \underbrace{ {\left[ \begin{array}{c}1 \\ - 1 \\ - 2\end{array} \right]}}_{\mathbf{a}_3}  = \underbrace{ {\left[ \begin{array}{c}2 \\ - 2 \\ 1\end{array} \right]}}_{\mathbf{a}_4}.
$$

Therefore, $x_1 + x_2 +  x_3 = (-5) + 0 + 7 = 2.$

## Representative practice (first three per skill; full bank in practice.json)

### Finding a Basis of the Space Spanned by a Set of Vectors Using Inspection (25 captured questions)

Question 17592186120517 — question.difficulty/easy

Consider the vectors ${\mathbf{a}}_{1}=\begin{bmatrix}3 \\ 1\end{bmatrix},{\mathbf{a}}_{2}=\begin{bmatrix}2 \\ 2\end{bmatrix}$, and ${\mathbf{a}}_{3}=\begin{bmatrix}1 \\ -1\end{bmatrix}$. Find a basis of $S=\text{Span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$ by inspection.

Solution: A basis is a linearly independent set that spans the given space. By inspection,

$$
a_1=\begin{bmatrix}3\\1\end{bmatrix}
=\begin{bmatrix}2\\2\end{bmatrix}+\begin{bmatrix}1\\-1\end{bmatrix}
=a_2+a_3.
$$

Thus $a_1$ can be removed without changing the span. The vectors $a_2$ and $a_3$ are not parallel, so they are linearly independent. Therefore, a basis is

$$
B=\left\{\begin{bmatrix}2\\2\end{bmatrix},\begin{bmatrix}1\\-1\end{bmatrix}\right\}.
$$

Answer selection: \mathcal{B}=\left\{\begin{bmatrix}2 \\ 2\end{bmatrix},\begin{bmatrix}1 \\ -1\end{bmatrix}\right\}

Question 17592186120518 — None

Consider the vectors ${\mathbf{a}}_{1}=\begin{bmatrix}2 \\ 0\end{bmatrix},{\mathbf{a}}_{2}=\begin{bmatrix}1 \\ 3\end{bmatrix}$, and ${\mathbf{a}}_{3}=\begin{bmatrix}3 \\ 3\end{bmatrix}$. Find a basis of $S=\text{Span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$ by inspection.

Solution: A basis is a linearly independent set that spans the given space. By inspection,

$$
a_3=\begin{bmatrix}3\\3\end{bmatrix}
=\begin{bmatrix}2\\0\end{bmatrix}+\begin{bmatrix}1\\3\end{bmatrix}
=a_1+a_2.
$$

Thus $a_3$ can be removed without changing the span. The vectors $a_1$ and $a_2$ are not parallel, so they are linearly independent. Therefore, a basis is

$$
B=\left\{\begin{bmatrix}2\\0\end{bmatrix},\begin{bmatrix}1\\3\end{bmatrix}\right\}.
$$

Answer selection: \mathcal{B}=\left\{\begin{bmatrix}2 \\ 0\end{bmatrix},\begin{bmatrix}1 \\ 3\end{bmatrix}\right\}

Question 17592186247170 — question.difficulty/moderate

Consider the vectors ${\mathbf{a}}_{1}=\begin{bmatrix}0 \\ -4\end{bmatrix},{\mathbf{a}}_{2}=\begin{bmatrix}4 \\ 4\end{bmatrix},$ and ${\mathbf{a}}_{3}=\begin{bmatrix}-4 \\ -4\end{bmatrix}.$ Find a basis of $S=\text{Span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$  by inspection.

Solution: Remember that a basis of $S$ is a set of linearly independent vectors that spans $S.$

From the given vectors, we can see that ${\mathbf{a}}_{3}$ is a linear combination of vectors ${\mathbf{a}}_{1}$ and ${\mathbf{a}}_{2}:$

$$
{\mathbf{a}}_{3}=0\cdot {\mathbf{a}}_{1}+(-1)\cdot {\mathbf{a}}_{2}
$$

Consequently, the vector ${\mathbf{a}}_{3}$ can be removed from $\text{Span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$ without changing the span. So $S=\text{Span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$ is spanned by just $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2}\}.$ 

Lastly, note that ${\mathbf{a}}_{1}$ and ${\mathbf{a}}_{2}$ are linearly independent since they are not parallel. So the set $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2}\}$ is a linearly independent set that spans $S.$

Therefore, a basis of $S$ is $\{{\mathbf{a}}_{1},{\mathbf{a}}_{2}\},$ that is to say,

$$
\mathcal{B}=\left\{\underbrace{\begin{bmatrix}0 \\ -4\end{bmatrix}}_{{\color{black}{\mathbf{a}}_{1}}},\underbrace{\begin{bmatrix}4 \\ 4\end{bmatrix}}_{{\color{black}{\mathbf{a}}_{2}}}\right\}.
$$

Answer selection: B=\left\{\begin{bmatrix}0 \\ -4\end{bmatrix},\begin{bmatrix}4 \\ 4\end{bmatrix}\right\}

### Finding a Basis of the Space Spanned by a Set of Vectors by Identifying Pivot Columns (28 captured questions)

Question 17592186120338 — question.difficulty/easy

Consider the vectors ${\mathbf{a}}_{1}=\begin{bmatrix}5 \\ 0 \\ 0\end{bmatrix}$, ${\mathbf{a}}_{2}=\begin{bmatrix}-1 \\ 7 \\ 0\end{bmatrix}$, and ${\mathbf{a}}_{3}=\begin{bmatrix}2 \\ -14 \\ 0\end{bmatrix}$. Find a basis $B$ of $\text{Span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$.

Solution: We need a linearly independent subset that has the same span. Place the given vectors in the columns of a matrix:

$$
\begin{bmatrix}5&-1&2\\0&7&-14\\0&0&0\end{bmatrix}.
$$

This matrix is already in row echelon form, with pivots in the first and second columns. The third column is $-2$ times the second, so $a_3=-2a_2$ can be removed without changing the span. Select the first and second columns from the original matrix:

$$
B=\left\{\begin{bmatrix}5\\0\\0\end{bmatrix},\begin{bmatrix}-1\\7\\0\end{bmatrix}\right\}.
$$

Answer selection: \mathcal{B}=\left\{\begin{bmatrix}5 \\ 0 \\ 0\end{bmatrix},\begin{bmatrix}-1 \\ 7 \\ 0\end{bmatrix}\right\}

Question 17592186120399 — question.difficulty/moderate

Consider the vectors ${\mathbf{a}}_{1}=\begin{bmatrix}-2 \\ 3\end{bmatrix},$ ${\mathbf{a}}_{2}=\begin{bmatrix}4 \\ -6\end{bmatrix},$ and ${\mathbf{a}}_{3}=\begin{bmatrix}-2 \\ -3\end{bmatrix}.$ Find a basis $B$ of $\text{Span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}.$

Solution: We need to find a subset of linearly independent vectors. So, we start by creating a matrix whose columns are made up of our vectors, and then we reduce the matrix to row echelon form:

$$
\begin{aligned} & \begin{bmatrix}-2 & 4 & -2 \\ 3 & -6 & -3\end{bmatrix} & {R}_{2} & :={R}_{2}+\frac{3}{2}{R}_{1} \\  & ∼\begin{bmatrix}-2 & 4 & -2 \\ 0 & 0 & -6\end{bmatrix}\end{aligned}
$$

The pivot columns correspond to linearly independent vectors, while the non-pivot columns correspond to linearly dependent vectors that can be removed. Here, the $1$st and $3$rd columns are pivot columns, while the $2$nd column is a non-pivot column.

Remember that we need to pick the pivot columns from the *original matrix*, not from the reduced one.

The $1$st and $3$rd columns from the original matrix are ${\mathbf{a}}_{1}$ and ${\mathbf{a}}_{3}.$ So, a basis of $S$ is $\{{\mathbf{a}}_{1},{\mathbf{a}}_{3}\},$ that is to say, 

$$
\mathcal{B}=\left\{\begin{bmatrix}-2 \\ 3\end{bmatrix},\begin{bmatrix}-2 \\ -3\end{bmatrix}\right\}.
$$

Answer selection: \mathcal{B}=\left\{\begin{bmatrix}-2 \\ 3\end{bmatrix},\begin{bmatrix}-2 \\ -3\end{bmatrix}\right\}

Question 17592186247171 — question.difficulty/easy

Consider the vectors ${\mathbf{a}}_{1}=\begin{bmatrix}1 \\ 0 \\ 0\end{bmatrix},{\mathbf{a}}_{2}=\begin{bmatrix}5 \\ 0 \\ 0\end{bmatrix},$ and ${\mathbf{a}}_{3}=\begin{bmatrix}6 \\ 2 \\ 0\end{bmatrix}.$ Find a basis $B$ of $\text{span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}.$

Solution: We need to find a subset of linearly independent vectors. So, we start by creating a matrix whose columns are made up of our vectors, and then we reduce the matrix to row echelon form:

$$
\begin{aligned} & \begin{bmatrix}1 & 5 & 6 \\ 0 & 0 & 2 \\ 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

In this case, our matrix is already in a row echelon form.

The pivot columns correspond to linearly independent vectors, while the non-pivot columns correspond to linearly dependent vectors that can be removed. Here, the $1$st and $3$rd columns are pivot columns, while the $2$nd column is a non-pivot column.

The $1$st and $3$rd columns from the original matrix are ${\mathbf{a}}_{1}$ and ${\mathbf{a}}_{3}.$ So, a basis of $S$ is $\{{\mathbf{a}}_{1},{\mathbf{a}}_{3}\},$ that is to say, 

$$
B=\left\{\begin{bmatrix}1 \\ 0 \\ 0\end{bmatrix},\begin{bmatrix}6 \\ 2 \\ 0\end{bmatrix}\right\}.
$$

Answer selection: B=\left\{\begin{bmatrix}1 \\ 0 \\ 0\end{bmatrix},\begin{bmatrix}6 \\ 2 \\ 0\end{bmatrix}\right\}

### Determining Whether a Given Set Is a Basis of a Span (27 captured questions)

Question 17592186120523 — question.difficulty/moderate

The vectors ${\mathbf{a}}_{1}$, ${\mathbf{a}}_{2}$, and ${\mathbf{a}}_{3}$ are given below. Determine whether $\mathcal{B}=\{{\mathbf{a}}_{1},{\mathbf{a}}_{2}\}$ is a basis of $\text{Span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$. If that is the case, find $x_{1} \cdot x_{2}$, where ${\mathbf{a}}_{3}={x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}$.
$$
{\mathbf{a}}_{1}=\begin{bmatrix}1 \\ -2\end{bmatrix},\hspace{2em}{\mathbf{a}}_{2}=\begin{bmatrix}-1 \\ 4\end{bmatrix},\hspace{2em}{\mathbf{a}}_{3}=\begin{bmatrix}2 \\ -2\end{bmatrix}
$$

Solution: We want to find coefficients $x_1,x_2$ such that $a_3=x_1a_1+x_2a_2$. Equating coordinates gives

$$
\left\{\begin{aligned}x_1-x_2&=2\\-2x_1+4x_2&=-2.\end{aligned}\right.
$$

Add twice the first equation to the second to obtain $2x_2=2$, so $x_2=1$. The first equation then gives $x_1=3$.

The coefficient matrix has a pivot in both columns, so $a_1$ and $a_2$ are linearly independent. Also $a_3=3a_1+a_2$, so they span the same space as the three given vectors. Thus $B$ is a basis, and

$$
x_1x_2=3\cdot1=3.
$$

Answer selection: 3

Question 17592186120524 — question.difficulty/hard

The vectors ${\mathbf{a}}_{1},$ ${\mathbf{a}}_{2},$ ${\mathbf{a}}_{3},$ and ${\mathbf{a}}_{4}$ are given below. Determine whether $\mathcal{B}=\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$ is a basis of $\text{Span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3},{\mathbf{a}}_{4}\}.$ If that is the case, find ${x}_{1}+{x}_{2}+{x}_{3},$ where ${\mathbf{a}}_{4}={x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}.$

$$
{\mathbf{a}}_{1}=\begin{bmatrix}1 \\ -2 \\ 5\end{bmatrix},\hspace{2em}{\mathbf{a}}_{2}=\begin{bmatrix}-1 \\ 3 \\ -5\end{bmatrix},\hspace{2em}{\mathbf{a}}_{3}=\begin{bmatrix}1 \\ -2 \\ 6\end{bmatrix},\hspace{2em}{\mathbf{a}}_{4}=\begin{bmatrix}-1 \\ 2 \\ 2\end{bmatrix}
$$

Solution: We want to determine if $B$ is indeed a basis of $\text{Span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3},{\mathbf{a}}_{4}\}.$ So, we want to find ${x}_{1},{x}_{2},{x}_{3}\in \mathbb{R}$ such that 

$$
{\color{black}{x}_{1}}\underbrace{\begin{bmatrix}1 \\ -2 \\ 5\end{bmatrix}}_{{\mathbf{a}}_{1}}+{\color{rblack}{x}_{2}}\underbrace{\begin{bmatrix}-1 \\ 3 \\ -5\end{bmatrix}}_{{\mathbf{a}}_{2}}+{\color{rblack}{x}_{3}}\underbrace{\begin{bmatrix}1 \\ -2 \\ 6\end{bmatrix}}_{{\mathbf{a}}_{3}}=\underbrace{\begin{bmatrix}-1 \\ 2 \\ 2\end{bmatrix}}_{{\mathbf{a}}_{4}}.
$$

This equation is equivalent to the system

$$
\left\{\begin{aligned}{x}_{1}-{x}_{2}+{x}_{3} &=-1 \\ -2{x}_{1}+3{x}_{2}-2{x}_{3} &=2 \\ 5{x}_{1}-5{x}_{2}+6{x}_{3} &=2\end{aligned}\right.
$$

Now, we reduce the augmented matrix of the system to reduced row echelon form (RREF):

$$
\begin{aligned} & \,\,\left[\begin{array}{ccc|c}1 & -1 & 1 & -1 \\ -2 & 3 & -2 & 2 \\ 5 & -5 & 6 & 2\end{array}\right] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & -1 \\ 0 & 1 & 0 & 0 \\ 5 & -5 & 6 & 2\end{array}\right] & {R}_{3} & :={R}_{3}+(-5){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 1 & -1 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 7\end{array}\right] & {R}_{1} & :={R}_{1}+(-1){R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & -1 & 0 & -8 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 7\end{array}\right] & {R}_{1} & :={R}_{1}+{R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 0 & -8 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 7\end{array}\right]\end{aligned}
$$

From the reduced matrix above, we see that the pivot columns are the $1$st, $2$nd, and $3$rd columns. So,  $B$ is indeed a basis of $\text{Span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3},{\mathbf{a}}_{4}\}.$
Also, the matrix tells us that ${x}_{1}=-8,$ ${x}_{2}=0,$ and ${x}_{3}=7,$ meaning that

$$
(-8)\cdot \underbrace{\begin{bmatrix}1 \\ -2 \\ 5\end{bmatrix}}_{{\mathbf{a}}_{1}}+0\cdot \underbrace{\begin{bmatrix}-1 \\ 3 \\ -5\end{bmatrix}}_{{\mathbf{a}}_{2}}+7\cdot \underbrace{\begin{bmatrix}1 \\ -2 \\ 6\end{bmatrix}}_{{\mathbf{a}}_{3}}=\underbrace{\begin{bmatrix}-1 \\ 2 \\ 2\end{bmatrix}}_{{\mathbf{a}}_{4}}.
$$

Therefore, ${x}_{1}+{x}_{2}+{x}_{3}=-8+0+7=-1.$

Answer selection: -1

Question 17592186247186 — question.difficulty/hard

The vectors ${\mathbf{a}}_{1},$ ${\mathbf{a}}_{2},$ ${\mathbf{a}}_{3},$ and ${\mathbf{a}}_{4}$ are given below. Determine whether $\mathcal{B}=\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3}\}$ is a basis of $\text{Span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3},{\mathbf{a}}_{4}\}.$ If that is the case, find ${x}_{1}+{x}_{2}+{x}_{3},$ where ${\mathbf{a}}_{4}={x}_{1}{\mathbf{a}}_{1}+{x}_{2}{\mathbf{a}}_{2}+{x}_{3}{\mathbf{a}}_{3}.$

$$
{\mathbf{a}}_{1}=\begin{bmatrix}1 \\ 3 \\ -1\end{bmatrix},\hspace{2em}{\mathbf{a}}_{2}=\begin{bmatrix}1 \\ 4 \\ -1\end{bmatrix},\hspace{2em}{\mathbf{a}}_{3}=\begin{bmatrix}2 \\ 6 \\ -1\end{bmatrix},\hspace{2em}{\mathbf{a}}_{4}=\begin{bmatrix}-9 \\ -29 \\ 6\end{bmatrix}
$$

Solution: We want to determine if $B$ is indeed a basis of $\text{Span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3},{\mathbf{a}}_{4}\}.$ So, we want to find ${x}_{1},{x}_{2},{x}_{3}\in \mathbb{R}$ such that 

$$
{\color{black}{x}_{1}}\underbrace{\begin{bmatrix}1 \\ 3 \\ -1\end{bmatrix}}_{{\mathbf{a}}_{1}}+{\color{rblack}{x}_{2}}\underbrace{\begin{bmatrix}1 \\ 4 \\ -1\end{bmatrix}}_{{\mathbf{a}}_{2}}+{\color{rblack}{x}_{3}}\underbrace{\begin{bmatrix}2 \\ 6 \\ -1\end{bmatrix}}_{{\mathbf{a}}_{3}}=\underbrace{\begin{bmatrix}-9 \\ -29 \\ 6\end{bmatrix}}_{{\mathbf{a}}_{4}}.
$$

This equation is equivalent to the system

$$
\left\{\begin{aligned}{x}_{1}+{x}_{2}+2{x}_{3} &=-9 \\ 3{x}_{1}+4{x}_{2}+6{x}_{3} &=-29 \\ -{x}_{1}-{x}_{2}-{x}_{3} &=6\end{aligned}\right.
$$

Now, we reduce the augmented matrix of the system to reduced row echelon form (RREF):

$$
\begin{aligned} & \,\,\left[\begin{array}{ccc|c}1 & 1 & 2 & -9 \\ 3 & 4 & 6 & -29 \\ -1 & -1 & -1 & 6\end{array}\right] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 2 & -9 \\ 0 & 1 & 0 & -2 \\ -1 & -1 & -1 & 6\end{array}\right] & {R}_{3} & :={R}_{3}+{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 2 & -9 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & -3\end{array}\right] & {R}_{1} & :={R}_{1}+(-2){R}_{3} \\  & ∼\left[\begin{array}{ccc|c}1 & 1 & 0 & -3 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & -3\end{array}\right] & {R}_{1} & :={R}_{1}+(-1){R}_{2} \\  & ∼\left[\begin{array}{ccc|c}1 & 0 & 0 & -1 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & -3\end{array}\right]\end{aligned}
$$

From the reduced matrix above, we see that the pivot columns are the $1$st, $2$nd, and $3$rd columns. So,  $B$ is indeed a basis of $\text{Span}\{{\mathbf{a}}_{1},{\mathbf{a}}_{2},{\mathbf{a}}_{3},{\mathbf{a}}_{4}\}.$
Also, the matrix tells us that ${x}_{1}=-1,$ ${x}_{2}=-2,$ and ${x}_{3}=-3,$ meaning that

$$
(-1)\cdot \underbrace{\begin{bmatrix}1 \\ 3 \\ -1\end{bmatrix}}_{{\mathbf{a}}_{1}}+(-2)\cdot \underbrace{\begin{bmatrix}1 \\ 4 \\ -1\end{bmatrix}}_{{\mathbf{a}}_{2}}+(-3)\cdot \underbrace{\begin{bmatrix}2 \\ 6 \\ -1\end{bmatrix}}_{{\mathbf{a}}_{3}}=\underbrace{\begin{bmatrix}-9 \\ -29 \\ 6\end{bmatrix}}_{{\mathbf{a}}_{4}}.
$$

Therefore, ${x}_{1}+{x}_{2}+{x}_{3}=(-1)+(-2)+(-3)=-6.$

Answer selection: -6
