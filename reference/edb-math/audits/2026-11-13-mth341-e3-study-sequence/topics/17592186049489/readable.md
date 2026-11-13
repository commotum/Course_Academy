# 17592186049489 Projection Matrices, Linear Transformations and Their Properties

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186135052 — Introduction

As we know, if $A$ is the matrix whose columns are the linearly independent vectors $\mathbf{a}_1, \mathbf{a}_2, \ldots, \mathbf{a}_n$ then the projection of a vector $\mathbf{x}$ onto $S=\textrm{Span}\{ \mathbf{a}_1, \mathbf{a}_2, \ldots, \mathbf{a}_n \}$ is given by

$$
\textrm{proj}_{S} \: \mathbf{x} = {\color{blue}A(A^T\!A)^{-1}\!A^T}\,\mathbf{x}.
$$

 
Now, if we denote $P_S = A(A^T\!A)^{-1}\!A^T$, then 

$$
\textrm{proj}_{S} \: \mathbf{x} = {\color{blue}P_S}\,\mathbf{x}.
$$

The matrix $P_S$ is called the **orthogonal projection matrix**. In other words, an orthogonal projection matrix 

$$
P_S=A(A^T\!A)^{-1}\!A^T
$$

is a matrix that transforms any vector of the vector space into its projection to subspace $S$ spanned by the columns of $A$.

Knowing this, we can define the **orthogonal projection transformation** $\mathbf{P}_{\!S}$ as

$$
\mathbf{P}_{\!S}:	\mathbb{R}^n \to \mathbb{R}^n
$$

such that

$$
\mathbf{x} \,\,\, \mapsto \textrm{proj}_S\,\mathbf{x}.
$$

It maps each vector from $\mathbb{R}^n$ into its orthogonal projection on $S$. 

**Note:** The matrix $P_S$ is the standard matrix of the orthogonal projection transformation, that is, the matrix relative to the standard basis of $\mathbb{R}^n.$



### example 17592186133599 — Finding a Matrix that Defines an Orthogonal Projection Onto the Subspace Spanned by a Vector

Find a matrix that defines the orthogonal projection of $\mathbb{R}^3$ onto the subspace spanned by $\mathbf{a}={\left[ \begin{array}{c}1 \\ 2 \\ - 3\end{array} \right]}.$

Recall that the matrix $P_S = A(A^T\!A)^{-1}\!A^T$ maps any vector $\mathbf x\in \mathbb{R}^n$ onto its orthogonal projection in the subspace $S$ spanned by the columns of the matrix $A.$ 

In our case, $A={\left[ \begin{array}{c}1 \\ 2 \\ - 3\end{array} \right]}.$ Therefore,

$$
\begin{aligned}{P}_{S} & =A({A}^{T}\,A)^{-1}\,{A}^{T} \\  & =\begin{bmatrix}1 \\ 2 \\ -3\end{bmatrix}{\left(\begin{bmatrix}1 & 2 & -3\end{bmatrix}\begin{bmatrix}1 \\ 2 \\ -3\end{bmatrix}\right)}^{-1}\begin{bmatrix}1 & 2 & -3\end{bmatrix} \\  & =\begin{bmatrix}1 \\ 2 \\ -3\end{bmatrix}\cdot (14)^{-1}\begin{bmatrix}1 & 2 & -3\end{bmatrix} \\  & =\frac{1}{14}\begin{bmatrix}1 \\ 2 \\ -3\end{bmatrix}\begin{bmatrix}1 & 2 & -3\end{bmatrix} \\  & =\frac{1}{14}\begin{bmatrix}1 & 2 & -3 \\ 2 & 4 & -6 \\ -3 & -6 & 9\end{bmatrix}.\end{aligned}
$$

### example 17592186133676 — Finding a Matrix That Defines an Orthogonal Projection Onto the Subspace Spanned by a Plane

Find a matrix that defines the orthogonal projection of $\mathbb{R}^3$ onto the plane whose parametric equation is $\mathbf{r}=s\mathbf{v} + t\mathbf{w}$, where
$$
\mathbf{v}={\left[ \begin{array}{c}1 \\ 2 \\ 1\end{array} \right]},\quad \mathbf{w}={\left[ \begin{array}{c}1 \\ - 1 \\ 1\end{array} \right]}.
$$

Recall that the matrix $P_S = A(A^T\!A)^{-1}\!A^T$ maps any vector $\mathbf x\in \mathbb{R}^n$ onto its orthogonal projection in the subspace $S$ spanned by the columns of the matrix $A.$ 

Notice that the plane $\mathbf{r}=s\mathbf{v}+t\mathbf{w}$ is actually the subspace $\text{Span}\{\mathbf{v}, \mathbf{w}\}.$ 
Hence, we have 
$$
A={\left[ \begin{array}{cc}1 & 1 \\ 2 & - 1 \\ 1 & 1\end{array} \right]}.
$$

Therefore,

$$
\begin{aligned}{P}_{S} & =A({A}^{T}\,A)^{-1}\,{A}^{T} \\  & =\begin{bmatrix}1 & 1 \\ 2 & -1 \\ 1 & 1\end{bmatrix}{\left(\begin{bmatrix}1 & 2 & 1 \\ 1 & -1 & 1\end{bmatrix}\begin{bmatrix}1 & 1 \\ 2 & -1 \\ 1 & 1\end{bmatrix}\right)}^{-1}\begin{bmatrix}1 & 2 & 1 \\ 1 & -1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 1 \\ 2 & -1 \\ 1 & 1\end{bmatrix}{\begin{bmatrix}6 & 0 \\ 0 & 3\end{bmatrix}}^{-1}\begin{bmatrix}1 & 2 & 1 \\ 1 & -1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 1 \\ 2 & -1 \\ 1 & 1\end{bmatrix}\cdot \frac{1}{6}\begin{bmatrix}1 & 0 \\ 0 & 2\end{bmatrix}\cdot \begin{bmatrix}1 & 2 & 1 \\ 1 & -1 & 1\end{bmatrix} \\  & =\frac{1}{6}\begin{bmatrix}1 & 1 \\ 2 & -1 \\ 1 & 1\end{bmatrix}\begin{bmatrix}1 & 2 & 1 \\ 2 & -2 & 2\end{bmatrix} \\  & =\frac{1}{2}\begin{bmatrix}1 & 0 & 1 \\ 0 & 2 & 0 \\ 1 & 0 & 1\end{bmatrix}.\end{aligned}
$$

### tutorial 17592186135096 — A Criterion of an Orthogonal Projection Matrix

A matrix $P$ is an orthogonal projection matrix if and only if the following two conditions hold:

- $P^2 = P$ (the matrix is idempotent), and

- $P^T = P$ (the matrix is symmetric with respect to the main diagonal).

Let's check whether $A={\left[ \begin{array}{cc}{\displaystyle \frac{1}{2}} & {\displaystyle \frac{1}{2}} \\ {\displaystyle \frac{1}{2}} & {\displaystyle \frac{1}{2}}\end{array} \right]}$ is an orthogonal  projection matrix:

$$
\begin{aligned}{A}^{T} & =\begin{bmatrix}\frac{1}{2} & \frac{1}{2} \\ \frac{1}{2} & \frac{1}{2}\end{bmatrix} \\  & =A.\,✓ \\ {A}^{2} & =A\cdot A \\  & =\begin{bmatrix}\frac{1}{2} & \frac{1}{2} \\ \frac{1}{2} & \frac{1}{2}\end{bmatrix}\begin{bmatrix}\frac{1}{2} & \frac{1}{2} \\ \frac{1}{2} & \frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}\frac{1}{2} & \frac{1}{2} \\ \frac{1}{2} & \frac{1}{2}\end{bmatrix} \\  & =A.\,✓\end{aligned}
$$

Therefore, $A$ is an orthogonal projection matrix.



### example 17592186133600 — Identifying an Orthogonal Projection Matrix

Which of the following are orthogonal projection matrices?

$$
A ={\left[ \begin{array}{cc}2 & 1 \\ 1 & 3\end{array} \right]}, \quad 
B= {\left[ \begin{array}{cc}{\displaystyle \frac{1}{4}} & {\displaystyle \frac{2}{3}} \\ - {\displaystyle \frac{2}{3}} & {\displaystyle \frac{1}{4}}\end{array} \right]}, \quad 
C={\left[ \begin{array}{cc}{\displaystyle \frac{4}{5}} & {\displaystyle \frac{2}{5}} \\ {\displaystyle \frac{2}{5}} & {\displaystyle \frac{1}{5}}\end{array} \right]}.
$$

Recall that $Q$ is an orthogonal projection matrix if and only if $Q^2=Q$ and $Q^T=Q.$ 

With that in mind, let's examine our matrices.

- $A$ is *not* an orthogonal projection matrix. We have
$A^T = A$
but 

$$
\begin{aligned}{A}^{2} & =A\cdot A \\  & =\begin{bmatrix}2 & 1 \\ 1 & 3\end{bmatrix}\begin{bmatrix}2 & 1 \\ 1 & 3\end{bmatrix} \\  & =\begin{bmatrix}5 & 5 \\ 5 & 10\end{bmatrix} \\  & \ne A.\end{aligned}
$$

- $B$ is *not* an orthogonal projection matrix. We have

$$
\begin{aligned}{B}^{T}\ne B.\end{aligned}
$$

- $C$ is an orthogonal projection matrix. Indeed,
$C^T = C$
and

$$
\begin{aligned}{C}^{2} & =C\cdot C \\  & =\begin{bmatrix}\frac{4}{5} & \frac{2}{5} \\ \frac{2}{5} & \frac{1}{5}\end{bmatrix}\begin{bmatrix}\frac{4}{5} & \frac{2}{5} \\ \frac{2}{5} & \frac{1}{5}\end{bmatrix} \\  & =\frac{1}{5}\begin{bmatrix}4 & 2 \\ 2 & 1\end{bmatrix}\cdot \frac{1}{5}\begin{bmatrix}4 & 2 \\ 2 & 1\end{bmatrix} \\  & =\frac{1}{25}\begin{bmatrix}4 & 2 \\ 2 & 1\end{bmatrix}\begin{bmatrix}4 & 2 \\ 2 & 1\end{bmatrix} \\  & =\frac{1}{25}\begin{bmatrix}20 & 10 \\ 10 & 5\end{bmatrix} \\  & =\begin{bmatrix}\frac{4}{5} & \frac{2}{5} \\ \frac{2}{5} & \frac{1}{5}\end{bmatrix} \\  & =C.\end{aligned}
$$

Therefore, the correct answer is "$C$ only."

### tutorial 17592186135053 — Projection Onto the Orthogonal Complement

As we know, any vector $\mathbf{x} \in \mathbb{R}^n$ can be expressed as a sum of its projections onto the subspace $S$ and the corresponding orthogonal complement $S^\perp.$

If $\mathbf{P}_S$ and $\mathbf{P}_{S^\perp}$ are the orthogonal projections onto the subspace $S$ and its orthogonal complement $S^\perp,$ respectively, then

$$
\mathbf{P}_S (\mathbf{x}) + \mathbf{P}_{S^\perp} (\mathbf{x}) = \mathbf{x}.
$$

 

In $\mathbb{R}^3,$ this can be illustrated as follows:

![](images/41/4144ec8cf2ab12d7d915855acca282c665803bb5402b5b76c08372f8fc5ccc42.png)

In particular, this means that the sum of the corresponding projection matrices equals the identity matrix:

$$
P_S + P_{S^\perp} = I
$$



### example 17592186133601 — Finding an Orthogonal Projection Matrix Given Vectors That Span the Orthogonal Complement

$$
\mathbf{a}={\left[ \begin{array}{c}1 \\ 1 \\ 2\end{array} \right]}, \qquad
P=\dfrac16{\left[ \begin{array}{ccc}{p}_{11} & {p}_{12} & \bbox[2pt,Gainsboro]{ {p}_{13}} \\ {p}_{21} & {p}_{22} & {p}_{23} \\ {p}_{31} & \bbox[2pt,Gainsboro]{ {p}_{32}} & {p}_{33}\end{array} \right]}
$$
Given that the vector $\mathbf{a}$ above spans $S^\perp,$ and that $P$ is the orthogonal projection matrix of $\mathbb{R}^3$ onto the subspace $S$, what is the value of $p_{13} + p_{32}?$

First, we find the orthogonal projection matrix onto $S^\perp = \textrm{Span}\{\mathbf{a}\}.$

Using the formula for the orthogonal projection matrix

$$
P_{S^\perp} = \mathbf{a} (\mathbf{a}^T\!\mathbf{a})^{-1} \mathbf{a}^T,
$$

we obtain the following:

$$
\begin{aligned}{P}_{{S}^{⊥}} & =\begin{bmatrix}1 \\ 1 \\ 2\end{bmatrix}{\left(\begin{bmatrix}1 & 1 & 2\end{bmatrix}\begin{bmatrix}1 \\ 1 \\ 2\end{bmatrix}\right)}^{-1}\begin{bmatrix}1 & 1 & 2\end{bmatrix} \\  & ={6}^{-1}\begin{bmatrix}1 \\ 1 \\ 2\end{bmatrix}\begin{bmatrix}1 & 1 & 2\end{bmatrix} \\  & =\frac{1}{6}\begin{bmatrix}1 & 1 & 2 \\ 1 & 1 & 2 \\ 2 & 2 & 4\end{bmatrix}\end{aligned}
$$

Recall that $P_S  + P_{S^\perp} = I.$ Therefore, 

$$
\begin{aligned}{P}_{S} & =I-{P}_{{S}^{⊥}} \\  & =I-\frac{1}{6}\begin{bmatrix}1 & 1 & 2 \\ 1 & 1 & 2 \\ 2 & 2 & 4\end{bmatrix} \\  & =\frac{1}{6}\begin{bmatrix}5 & -1 & -2 \\ -1 & 5 & -2 \\ -2 & -2 & 2\end{bmatrix}.\end{aligned}
$$

Finally, $p_{13} + p_{32} = (-2) + (-2) = -4.$

## Representative practice (first three per skill; full bank in practice.json)

### Finding a Matrix that Defines an Orthogonal Projection Onto the Subspace Spanned by a Vector (10 captured questions)

Question 17592186134253 — question.difficulty/easy

Find a matrix that defines the orthogonal projection of ${R}^{3}$ onto the subspace spanned by $a=\begin{bmatrix}3 \\ -2 \\ 1\end{bmatrix}.$

Solution: Recall that the matrix ${P}_{S}=A({A}^{T}\,A)^{-1}\,{A}^{T}$ maps any vector $x\in {R}^{n}$ onto its orthogonal projection in the subspace $S$ spanned by the columns of the matrix $A.$ 

In our case, $A=\begin{bmatrix}3 \\ -2 \\ 1\end{bmatrix}.$ Therefore,

$$
\begin{aligned}{P}_{S} & =A({A}^{T}\,A)^{-1}\,{A}^{T} \\  & =\begin{bmatrix}3 \\ -2 \\ 1\end{bmatrix}{\left(\begin{bmatrix}3 & -2 & 1\end{bmatrix}\begin{bmatrix}3 \\ -2 \\ 1\end{bmatrix}\right)}^{-1}\begin{bmatrix}3 & -2 & 1\end{bmatrix} \\  & =(14)^{-1}\begin{bmatrix}3 \\ -2 \\ 1\end{bmatrix}\begin{bmatrix}3 & -2 & 1\end{bmatrix} \\  & =\frac{1}{14}\begin{bmatrix}9 & -6 & 3 \\ -6 & 4 & -2 \\ 3 & -2 & 1\end{bmatrix}.\end{aligned}
$$

Answer selection: \frac{1}{14}\begin{bmatrix}9 & -6 & 3 \\ -6 & 4 & -2 \\ 3 & -2 & 1\end{bmatrix}

Question 17592186134545 — question.difficulty/easy

Find a matrix that defines the orthogonal projection of ${R}^{3}$ onto the subspace spanned by $$
\displaystyle a=\begin{bmatrix}2 \\ -1 \\ 1\end{bmatrix}.
$$

Solution: Recall that the matrix ${P}_{S}=A({A}^{T}\,A)^{-1}\,{A}^{T}$ maps any vector $x\in {R}^{n}$ onto its orthogonal projection in the subspace $S$ spanned by the columns of the matrix $A.$ 

In our case, $$
\displaystyle A=\begin{bmatrix}2 \\ -1 \\ 1\end{bmatrix}.
$$ Therefore,

$$
\begin{aligned}{P}_{S} & =A({A}^{T}\,A)^{-1}\,{A}^{T} \\  & =\begin{bmatrix}2 \\ -1 \\ 1\end{bmatrix}{\left(\begin{bmatrix}2 & -1 & 1\end{bmatrix}\begin{bmatrix}2 \\ -1 \\ 1\end{bmatrix}\right)}^{-1}\begin{bmatrix}2 & -1 & 1\end{bmatrix} \\  & =(6)^{-1}\begin{bmatrix}2 \\ -1 \\ 1\end{bmatrix}\begin{bmatrix}2 & -1 & 1\end{bmatrix} \\  & =\frac{1}{6}\begin{bmatrix}4 & -2 & 2 \\ -2 & 1 & -1 \\ 2 & -1 & 1\end{bmatrix}.\end{aligned}
$$

Answer selection: \frac{1}{6}\begin{bmatrix}4 & -2 & 2 \\ -2 & 1 & -1 \\ 2 & -1 & 1\end{bmatrix}

Question 17592186272115 — question.difficulty/easy

Find a matrix that defines the orthogonal projection of ${R}^{3}$ onto the subspace spanned by $a=\begin{bmatrix}2 \\ 0 \\ -1\end{bmatrix}.$

Solution: Recall that the matrix ${P}_{S}=A({A}^{T}\,A)^{-1}\,{A}^{T}$ maps any vector $x\in {R}^{n}$ onto its orthogonal projection in the subspace $S$ spanned by the columns of the matrix $A.$ 

In our case, $A=\begin{bmatrix}2 \\ 0 \\ -1\end{bmatrix}.$ Therefore,

$$
\begin{aligned}{P}_{S} & =A({A}^{T}\,A)^{-1}\,{A}^{T} \\  & =\begin{bmatrix}2 \\ 0 \\ -1\end{bmatrix}{\left(\begin{bmatrix}2 & 0 & -1\end{bmatrix}\begin{bmatrix}2 \\ 0 \\ -1\end{bmatrix}\right)}^{-1}\begin{bmatrix}2 & 0 & -1\end{bmatrix} \\  & =(5)^{-1}\begin{bmatrix}2 \\ 0 \\ -1\end{bmatrix}\begin{bmatrix}2 & 0 & -1\end{bmatrix} \\  & =\frac{1}{5}\begin{bmatrix}4 & 0 & -2 \\ 0 & 0 & 0 \\ -2 & 0 & 1\end{bmatrix}.\end{aligned}
$$

Answer selection: \frac{1}{5}\begin{bmatrix}4 & 0 & -2 \\ 0 & 0 & 0 \\ -2 & 0 & 1\end{bmatrix}

### Finding a Matrix That Defines an Orthogonal Projection Onto the Subspace Spanned by a Plane (12 captured questions)

Question 17592186134304 — question.difficulty/moderate

Find a matrix that defines the orthogonal projection of ${R}^{3}$ onto the plane whose parametric equation is $r=sv+tw$, where

$$
v=\begin{bmatrix}2 \\ 1 \\ 2\end{bmatrix},\,w=\begin{bmatrix}-1 \\ 2 \\ -1\end{bmatrix}.
$$

Solution: Recall that the matrix ${P}_{S}=A({A}^{T}\,A)^{-1}\,{A}^{T}$ maps any vector $x\in {R}^{n}$ onto its orthogonal projection in the subspace $S$ spanned by the columns of the matrix $A.$ 

Notice that the plane $r=sv+tw$ is actually the subspace $\text{Span}\{v,w\}.$ 
Hence, we have 

$$
A=\begin{bmatrix}2 & -1 \\ 1 & 2 \\ 2 & -1\end{bmatrix}.
$$

Therefore,

$$
\begin{aligned}{P}_{S} & =A({A}^{T}\,A)^{-1}\,{A}^{T} \\  & =\begin{bmatrix}2 & -1 \\ 1 & 2 \\ 2 & -1\end{bmatrix}{\left(\begin{bmatrix}2 & 1 & 2 \\ -1 & 2 & -1\end{bmatrix}\begin{bmatrix}2 & -1 \\ 1 & 2 \\ 2 & -1\end{bmatrix}\right)}^{-1}\begin{bmatrix}2 & 1 & 2 \\ -1 & 2 & -1\end{bmatrix} \\  & =\begin{bmatrix}2 & -1 \\ 1 & 2 \\ 2 & -1\end{bmatrix}{\begin{bmatrix}9 & -2 \\ -2 & 6\end{bmatrix}}^{-1}\begin{bmatrix}2 & 1 & 2 \\ -1 & 2 & -1\end{bmatrix} \\  & =\begin{bmatrix}2 & -1 \\ 1 & 2 \\ 2 & -1\end{bmatrix}\cdot \frac{1}{50}\begin{bmatrix}6 & 2 \\ 2 & 9\end{bmatrix}\cdot \begin{bmatrix}2 & 1 & 2 \\ -1 & 2 & -1\end{bmatrix} \\  & =\frac{1}{50}\begin{bmatrix}2 & -1 \\ 1 & 2 \\ 2 & -1\end{bmatrix}\begin{bmatrix}10 & 10 & 10 \\ -5 & 20 & -5\end{bmatrix} \\  & =\frac{1}{2}\begin{bmatrix}1 & 0 & 1 \\ 0 & 2 & 0 \\ 1 & 0 & 1\end{bmatrix}.\end{aligned}
$$

Answer selection: \frac{1}{2}\begin{bmatrix}1 & 0 & 1 \\ 0 & 2 & 0 \\ 1 & 0 & 1\end{bmatrix}

Question 17592186134547 — question.difficulty/moderate

Find a matrix that defines the orthogonal projection of ${R}^{3}$ onto the plane whose parametric equation is $r=sv+tw$, where

$$
v=\begin{bmatrix}0 \\ 1 \\ 2\end{bmatrix},\,w=\begin{bmatrix}-1 \\ 2 \\ 0\end{bmatrix}.
$$

Solution: Recall that the matrix ${P}_{S}=A({A}^{T}\,A)^{-1}\,{A}^{T}$ maps any vector $x\in {R}^{n}$ onto its orthogonal projection in the subspace $S$ spanned by the columns of the matrix $A.$ 

Notice that the plane $r=sv+tw$ is actually the subspace $\text{Span}{v,w}.$ 
Hence, we have 

$$
A=\begin{bmatrix}0 & -1 \\ 1 & 2 \\ 2 & 0\end{bmatrix}.
$$

Therefore,

$$
\begin{aligned}{P}_{S} & =A({A}^{T}\,A)^{-1}\,{A}^{T} \\  & =\begin{bmatrix}0 & -1 \\ 1 & 2 \\ 2 & 0\end{bmatrix}{\left(\begin{bmatrix}0 & 1 & 2 \\ -1 & 2 & 0\end{bmatrix}\begin{bmatrix}0 & -1 \\ 1 & 2 \\ 2 & 0\end{bmatrix}\right)}^{-1}\begin{bmatrix}0 & 1 & 2 \\ -1 & 2 & 0\end{bmatrix} \\  & =\begin{bmatrix}0 & -1 \\ 1 & 2 \\ 2 & 0\end{bmatrix}{\begin{bmatrix}5 & 2 \\ 2 & 5\end{bmatrix}}^{-1}\begin{bmatrix}0 & 1 & 2 \\ -1 & 2 & 0\end{bmatrix} \\  & =\begin{bmatrix}0 & -1 \\ 1 & 2 \\ 2 & 0\end{bmatrix}\cdot \frac{1}{21}\begin{bmatrix}5 & -2 \\ -2 & 5\end{bmatrix}\cdot \begin{bmatrix}0 & 1 & 2 \\ -1 & 2 & 0\end{bmatrix} \\  & =\frac{1}{21}\begin{bmatrix}0 & -1 \\ 1 & 2 \\ 2 & 0\end{bmatrix}\begin{bmatrix}2 & 1 & 10 \\ -5 & 8 & -4\end{bmatrix} \\  & =\frac{1}{21}\begin{bmatrix}5 & -8 & 4 \\ -8 & 17 & 2 \\ 4 & 2 & 20\end{bmatrix}.\end{aligned}
$$

Answer selection: \frac{1}{21}\begin{bmatrix}5 & -8 & 4 \\ -8 & 17 & 2 \\ 4 & 2 & 20\end{bmatrix}

Question 17592186326867 — question.difficulty/moderate

Find a matrix that defines the orthogonal projection of ${R}^{3}$ onto the plane whose parametric equation is $r=sv+tw$, where

$$
v=\begin{bmatrix}1 \\ 1 \\ 1\end{bmatrix},\,w=\begin{bmatrix}-1 \\ 1 \\ -1\end{bmatrix}.
$$

Solution: Recall that the matrix ${P}_{S}=A({A}^{T}\,A)^{-1}\,{A}^{T}$ maps any vector $x\in {R}^{n}$ onto its orthogonal projection in the subspace $S$ spanned by the columns of the matrix $A.$ 

Notice that the plane $r=sv+tw$ is actually the subspace $\text{Span}{v,w}.$ 
Hence, we have 

$$
A=\begin{bmatrix}1 & -1 \\ 1 & 1 \\ 1 & -1\end{bmatrix}.
$$

Therefore,

$$
\begin{aligned}{P}_{S} & =A({A}^{T}\,A)^{-1}\,{A}^{T} \\  & =\begin{bmatrix}1 & -1 \\ 1 & 1 \\ 1 & -1\end{bmatrix}{\left(\begin{bmatrix}1 & 1 & 1 \\ -1 & 1 & -1\end{bmatrix}\begin{bmatrix}1 & -1 \\ 1 & 1 \\ 1 & -1\end{bmatrix}\right)}^{-1}\begin{bmatrix}1 & 1 & 1 \\ -1 & 1 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & -1 \\ 1 & 1 \\ 1 & -1\end{bmatrix}{\begin{bmatrix}3 & -1 \\ -1 & 3\end{bmatrix}}^{-1}\begin{bmatrix}1 & 1 & 1 \\ -1 & 1 & -1\end{bmatrix} \\  & =\frac{1}{8}\begin{bmatrix}1 & -1 \\ 1 & 1 \\ 1 & -1\end{bmatrix}\begin{bmatrix}3 & 1 \\ 1 & 3\end{bmatrix}\begin{bmatrix}1 & 1 & 1 \\ -1 & 1 & -1\end{bmatrix} \\  & =\frac{1}{8}\begin{bmatrix}1 & -1 \\ 1 & 1 \\ 1 & -1\end{bmatrix}\begin{bmatrix}2 & 4 & 2 \\ -2 & 4 & -2\end{bmatrix} \\  & =\frac{1}{2}\begin{bmatrix}1 & 0 & 1 \\ 0 & 2 & 0 \\ 1 & 0 & 1\end{bmatrix}.\end{aligned}
$$

Answer selection: \frac{1}{2}\begin{bmatrix}1 & 0 & 1 \\ 0 & 2 & 0 \\ 1 & 0 & 1\end{bmatrix}

### Identifying an Orthogonal Projection Matrix (12 captured questions)

Question 17592186134302 — question.difficulty/moderate

Which of the following are orthogonal projection matrices?

Select all that apply.

Solution: Recall that $Q$ is an orthogonal projection matrix if and only if ${Q}^{2}=Q$ and ${Q}^{T}=Q.$ 

With that in mind, let's examine our matrices.

- $A$ is *not* an orthogonal projection matrix. We have
${A}^{T}=A$
but 

$$
\begin{aligned}{A}^{2} & =A\cdot A \\  & =\begin{bmatrix}1 & -1 \\ -1 & 1\end{bmatrix}\begin{bmatrix}1 & -1 \\ -1 & 1\end{bmatrix} \\  & =\begin{bmatrix}2 & -2 \\ -2 & 2\end{bmatrix} \\  & \ne A.\end{aligned}
$$

- $B$ is *not* an orthogonal projection matrix. We have

$$
\begin{aligned}{B}^{T}\ne B.\end{aligned}
$$

- $C$ is an orthogonal projection matrix. Indeed,
${C}^{T}=C$
and

$$
\begin{aligned}{C}^{2} & =C\cdot C \\  & =\begin{bmatrix}\frac{1}{17} & \frac{4}{17} \\ \frac{4}{17} & \frac{16}{17}\end{bmatrix}\begin{bmatrix}\frac{1}{17} & \frac{4}{17} \\ \frac{4}{17} & \frac{16}{17}\end{bmatrix} \\  & =\frac{1}{17}\begin{bmatrix}1 & 4 \\ 4 & 16\end{bmatrix}\cdot \frac{1}{17}\begin{bmatrix}1 & 4 \\ 4 & 16\end{bmatrix} \\  & =\frac{1}{289}\begin{bmatrix}1 & 4 \\ 4 & 16\end{bmatrix}\begin{bmatrix}1 & 4 \\ 4 & 16\end{bmatrix} \\  & =\frac{1}{289}\begin{bmatrix}17 & 68 \\ 68 & 272\end{bmatrix} \\  & =\begin{bmatrix}\frac{1}{17} & \frac{4}{17} \\ \frac{4}{17} & \frac{16}{17}\end{bmatrix} \\  & =C.\end{aligned}
$$

Therefore, the correct answer is "$C$ only."

Answer $A=\begin{bmatrix}1 & -1 \\ -1 & 1\end{bmatrix}$: false

Answer $B=\begin{bmatrix}-\frac{1}{2} & \frac{1}{2} \\ -\frac{1}{2} & -\frac{1}{2}\end{bmatrix}$: false

Answer $C=\begin{bmatrix}\frac{1}{17} & \frac{4}{17} \\ \frac{4}{17} & \frac{16}{17}\end{bmatrix}$: true

Question 17592186134303 — question.difficulty/easy

$$
A=\begin{bmatrix}\frac{4}{5} & \frac{2}{5} \\ \frac{2}{5} & \frac{1}{5}\end{bmatrix}
$$

Consider the matrix $A$ given above. Which of the following statements are true?

Select all that apply.

Solution: Recall that $Q$ is an orthogonal projection matrix if and only if ${Q}^{2}=Q$ and ${Q}^{T}=Q.$ 

With that in mind, let's examine each of the statements in turn.

- Statement ${A}^{T}=A$ is true. Indeed, ${A}^{T}=A.$

- Statement ${A}^{2}=A$ is true. Indeed, 

$$
\begin{aligned}{A}^{2} & =A\cdot A \\  & =\begin{bmatrix}\frac{4}{5} & \frac{2}{5} \\ \frac{2}{5} & \frac{1}{5}\end{bmatrix}\begin{bmatrix}\frac{4}{5} & \frac{2}{5} \\ \frac{2}{5} & \frac{1}{5}\end{bmatrix} \\  & =\frac{1}{5}\begin{bmatrix}4 & 2 \\ 2 & 1\end{bmatrix}\cdot \frac{1}{5}\begin{bmatrix}4 & 2 \\ 2 & 1\end{bmatrix} \\  & =\frac{1}{25}\begin{bmatrix}4 & 2 \\ 2 & 1\end{bmatrix}\begin{bmatrix}4 & 2 \\ 2 & 1\end{bmatrix} \\  & =\frac{1}{25}\begin{bmatrix}20 & 10 \\ 10 & 5\end{bmatrix} \\  & =\begin{bmatrix}\frac{4}{5} & \frac{2}{5} \\ \frac{2}{5} & \frac{1}{5}\end{bmatrix} \\  & =A.\end{aligned}
$$

- Statement “$A$ is an orthogonal projection matrix” is true since both statements ${A}^{T}=A$ and ${A}^{2}=A$ are true.

Therefore, the correct answer is ${A}^{T}=A$; ${A}^{2}=A$; “$A$ is an orthogonal projection matrix”.

Answer $A$ is an orthogonal projection matrix: true

Answer ${A}^{2}=A$: true

Answer ${A}^{T}=A$: true

Question 17592186272117 — question.difficulty/easy

$$
A=\begin{bmatrix}2 & -2 \\ 1 & -1\end{bmatrix}
$$

Consider the matrix $A$ given above. Which of the following statements are true?

Select all that apply.

Solution: Recall that $Q$ is an orthogonal projection matrix if and only if ${Q}^{2}=Q$ and ${Q}^{T}=Q.$ 

With that in mind, let's examine each of the statements in turn.

- Statement ${A}^{T}=A$ is false since ${A}^{T}\ne A.$

- Statement ${A}^{2}=A$ is true. Indeed, 

$$
\begin{aligned}{A}^{2} & =A\cdot A \\  & =\begin{bmatrix}2 & -2 \\ 1 & -1\end{bmatrix}\begin{bmatrix}2 & -2 \\ 1 & -1\end{bmatrix} \\  & =\begin{bmatrix}2 & -2 \\ 1 & -1\end{bmatrix} \\  & =A.\end{aligned}
$$

- Statement “$A$ is an orthogonal projection matrix” is false since not both statements ${A}^{T}=A$ and ${A}^{2}=A$ are true.

Therefore, the correct answer is " ${A}^{2}=A$ only."

Answer $A$ is an orthogonal projection matrix: false

Answer ${A}^{2}=A$: true

Answer ${A}^{T}=A$: false

### Finding an Orthogonal Projection Matrix Given Vectors That Span the Orthogonal Complement (12 captured questions)

Question 17592186134254 — question.difficulty/moderate

$$
a=\begin{bmatrix}2 \\ -1 \\ -2\end{bmatrix},\,P=\frac{1}{9}\begin{bmatrix}{p}_{11} & {p}_{12} & {p}_{13} \\ {p}_{21} & {p}_{22} & {p}_{23} \\ {p}_{31} & {p}_{32} & {p}_{33}\end{bmatrix}
$$

Given that the vector $a$ above spans ${S}^{⊥},$ and that $P$ is the orthogonal projection matrix of ${R}^{3}$ onto the subspace $S$, what is the value of ${p}_{22}+{p}_{31}?$

Solution: First, we find the orthogonal projection matrix onto ${S}^{⊥}=\text{Span}{a}.$

Using the formula for the orthogonal projection matrix

$$
{P}_{{S}^{⊥}}=a({a}^{T}\,a)^{-1}{a}^{T},
$$

we obtain the following:

$$
\begin{aligned}{P}_{{S}^{⊥}} & =\begin{bmatrix}2 \\ -1 \\ -2\end{bmatrix}{\left(\begin{bmatrix}2 & -1 & -2\end{bmatrix}\begin{bmatrix}2 \\ -1 \\ -2\end{bmatrix}\right)}^{-1}\begin{bmatrix}2 & -1 & -2\end{bmatrix} \\  & ={9}^{-1}\begin{bmatrix}2 \\ -1 \\ -2\end{bmatrix}\begin{bmatrix}2 & -1 & -2\end{bmatrix} \\  & =\frac{1}{9}\begin{bmatrix}4 & -2 & -4 \\ -2 & 1 & 2 \\ -4 & 2 & 4\end{bmatrix}\end{aligned}
$$

Recall that ${P}_{S}+{P}_{{S}^{⊥}}=I.$ Therefore, 

$$
\begin{aligned}{P}_{S} & =I-{P}_{{S}^{⊥}} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}-\frac{1}{9}\begin{bmatrix}4 & -2 & -4 \\ -2 & 1 & 2 \\ -4 & 2 & 4\end{bmatrix} \\  & =\frac{1}{9}\begin{bmatrix}5 & 2 & 4 \\ 2 & 8 & -2 \\ 4 & -2 & 5\end{bmatrix}.\end{aligned}
$$

Finally, ${p}_{22}+{p}_{31}=8+4=12.$

Answer selection: 12

Question 17592186134255 — question.difficulty/hard

$$
{a}_{1}=\begin{bmatrix}1 \\ 0 \\ -1 \\ 0\end{bmatrix},\,{a}_{2}=\begin{bmatrix}0 \\ -1 \\ 0 \\ 2\end{bmatrix},\,P=\frac{1}{10}\begin{bmatrix}{p}_{11} & {p}_{12} & {p}_{13} & {p}_{14} \\ {p}_{21} & {p}_{22} & {p}_{23} & {p}_{24} \\ {p}_{31} & {p}_{32} & {p}_{33} & {p}_{34} \\ {p}_{41} & {p}_{42} & {p}_{43} & {p}_{44}\end{bmatrix}
$$

Given that the vectors ${a}_{1}$ and ${a}_{2}$ above span ${S}^{⊥}$, and that $P$ is the orthogonal projection matrix of ${R}^{4}$ onto the subspace $S$, what is the value of ${p}_{22}+{p}_{42}?$

Solution: First, we find the orthogonal projection matrix onto ${S}^{⊥}=\text{Span}\{{a}_{1},{a}_{2}\}.$

Using the formula for the orthogonal projection matrix

$$
{P}_{{S}^{⊥}}=A({A}^{T}\,A)^{-1}{A}^{T},
$$

we obtain the following:

$$
\begin{aligned}{P}_{{S}^{⊥}} & =\begin{bmatrix}1 & 0 \\ 0 & -1 \\ -1 & 0 \\ 0 & 2\end{bmatrix}{\left(\begin{bmatrix}1 & 0 & -1 & 0 \\ 0 & -1 & 0 & 2\end{bmatrix}\begin{bmatrix}1 & 0 \\ 0 & -1 \\ -1 & 0 \\ 0 & 2\end{bmatrix}\right)}^{-1}\begin{bmatrix}1 & 0 & -1 & 0 \\ 0 & -1 & 0 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & -1 \\ -1 & 0 \\ 0 & 2\end{bmatrix}{\begin{bmatrix}2 & 0 \\ 0 & 5\end{bmatrix}}^{-1}\begin{bmatrix}1 & 0 & -1 & 0 \\ 0 & -1 & 0 & 2\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & -1 \\ -1 & 0 \\ 0 & 2\end{bmatrix}\cdot \frac{1}{10}\begin{bmatrix}5 & 0 \\ 0 & 2\end{bmatrix}\cdot \begin{bmatrix}1 & 0 & -1 & 0 \\ 0 & -1 & 0 & 2\end{bmatrix} \\  & =\frac{1}{10}\begin{bmatrix}1 & 0 \\ 0 & -1 \\ -1 & 0 \\ 0 & 2\end{bmatrix}\begin{bmatrix}5 & 0 & -5 & 0 \\ 0 & -2 & 0 & 4\end{bmatrix} \\  & =\frac{1}{10}\begin{bmatrix}5 & 0 & -5 & 0 \\ 0 & 2 & 0 & -4 \\ -5 & 0 & 5 & 0 \\ 0 & -4 & 0 & 8\end{bmatrix}\end{aligned}
$$

Since ${P}_{S}+{P}_{{S}^{⊥}}=I$, we have

$$
\begin{aligned}{P}_{S} & =I-{P}_{{S}^{⊥}} \\  & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix}-\frac{1}{10}\begin{bmatrix}5 & 0 & -5 & 0 \\ 0 & 2 & 0 & -4 \\ -5 & 0 & 5 & 0 \\ 0 & -4 & 0 & 8\end{bmatrix} \\  & =\frac{1}{10}\begin{bmatrix}5 & 0 & 5 & 0 \\ 0 & 8 & 0 & 4 \\ 5 & 0 & 5 & 0 \\ 0 & 4 & 0 & 2\end{bmatrix}.\end{aligned}
$$

Finally, ${p}_{22}+{p}_{42}=8+4=12.$

Answer selection: 12

Question 17592186272118 — question.difficulty/moderate

$$
a=\begin{bmatrix}1 \\ -1 \\ 1\end{bmatrix},\,P=\frac{1}{3}\begin{bmatrix}{p}_{11} & {p}_{12} & {p}_{13} \\ {p}_{21} & {p}_{22} & {p}_{23} \\ {p}_{31} & {p}_{32} & {p}_{33}\end{bmatrix}
$$

Given that the vector $a$ above spans ${S}^{⊥},$ and that $P$ is the orthogonal projection matrix of ${R}^{3}$ onto the subspace $S$, what is the value of ${p}_{11}+{p}_{22}?$

Solution: First, we find the orthogonal projection matrix onto ${S}^{⊥}=\text{Span}\{a\}.$

Using the formula for the orthogonal projection matrix

$$
{P}_{{S}^{⊥}}=a({a}^{T}\,a)^{-1}{a}^{T},
$$

we obtain the following:

$$
\begin{aligned}{P}_{{S}^{⊥}} & =\begin{bmatrix}1 \\ -1 \\ 1\end{bmatrix}{\left(\begin{bmatrix}1 & -1 & 1\end{bmatrix}\begin{bmatrix}1 \\ -1 \\ 1\end{bmatrix}\right)}^{-1}\begin{bmatrix}1 & -1 & 1\end{bmatrix} \\  & ={3}^{-1}\begin{bmatrix}1 \\ -1 \\ 1\end{bmatrix}\begin{bmatrix}1 & -1 & 1\end{bmatrix} \\  & =\frac{1}{3}\begin{bmatrix}1 & -1 & 1 \\ -1 & 1 & -1 \\ 1 & -1 & 1\end{bmatrix}\end{aligned}
$$

Recall that ${P}_{S}+{P}_{{S}^{⊥}}=I.$ Therefore, 

$$
\begin{aligned}{P}_{S} & =I-{P}_{{S}^{⊥}} \\  & =\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}-\frac{1}{3}\begin{bmatrix}1 & -1 & 1 \\ -1 & 1 & -1 \\ 1 & -1 & 1\end{bmatrix} \\  & =\frac{1}{3}\begin{bmatrix}2 & 1 & -1 \\ 1 & 2 & 1 \\ -1 & 1 & 2\end{bmatrix}.\end{aligned}
$$

Finally, ${p}_{11}+{p}_{22}=2+2=4.$

Answer selection: 4
