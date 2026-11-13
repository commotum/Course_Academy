# 17592186049880 The Rank-Nullity Theorem in Terms of Linear Transformations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186189365 — Introduction

The **rank-nullity theorem in terms of linear transformations** states the following:

*If $\mathbf{T}:\mathbb{R}^n \to \mathbb{R}^n$ is a linear transformation, then*

$$
\textrm{dim(Im}(\mathbf{T})) + \textrm{dim(Ker}(\mathbf{T})) = \textrm{dim}(\mathbb{R}^n),
$$

*or equivalently,*

$$
\textrm{rank}(\mathbf{T}) + \textrm{nullity}(\mathbf{T}) = n.
$$

For example, suppose that $\mathbf{T}:\mathbb{R}^3\to\mathbb{R}^3$ is a linear transformation such that

$$
\textrm{Im}(\mathbf{T})=\{ [ x, y, z ]^T \, : \, y+2z=0\}.
$$

Let's use the rank-nullity theorem to compute $\textrm{rank}(\mathbf{T})$ and $\text{nullity}(\mathbf{T}).$ 

First, solving $y+2z=0$ for $y,$ we get $y = -2z.$ Therefore, any vector from $\textrm{Im}(\mathbf{T})$ can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ -2z \\ z\end{bmatrix}=x\underbrace{\begin{bmatrix}1 \\ 0 \\ 0\end{bmatrix}}_{{v}_{1}}+z\underbrace{\begin{bmatrix}0 \\ -2 \\ 1\end{bmatrix}}_{{v}_{2}}.\end{aligned}
$$

This means that $\textrm{Im}(\mathbf{T})=\textrm{Span}\{\mathbf{v}_1,\mathbf{v}_2\}.$ And since $\mathbf v_1$ and $\mathbf v_2$ are linearly independent, we have $\textrm{rank}(\mathbf{T})=2.$ 

Finally, using the rank-nullity theorem, we obtain

$$
\begin{aligned}\text{nullity}(T) & =3-\text{rank}(T) \\  & =3-2 \\  & =1.\end{aligned}
$$



### example 17592186188204 — Finding the Rank or Nullity of a Linear Transformation Using the Rank-Nullity Theorem

Consider a linear transformation $\mathbf{T}:\mathbb{R}^3 \to \mathbb{R}^3.$ If $\textrm{nullity}(\mathbf{T})=1,$ then what is $\textrm{rank}(\mathbf{T})?$

According to the rank-nullity theorem, if $\mathbf{T}:\mathbb{R}^n \to \mathbb{R}^n,$ then

$$
\textrm{rank}(\mathbf{T}) + \textrm{nullity}(\mathbf{T}) = n.
$$

For the given transformation, we have $n=3.$ Therefore,

$$
\begin{aligned}\text{rank}(T)+\text{nullity}(T) & =n \\ \text{rank}(T)+1 & =3 \\ \text{rank}(T) & =3-1 \\  & =2.\end{aligned}
$$

### example 17592186188216 — Finding the Rank or Nullity of a Linear Transformation Given a Description of the Image or Kernel

Find $\text{nullity}(\mathbf{T})$ given that $\mathbf{T}:\mathbb{R}^3\to\mathbb{R}^3$ and $\textrm{Im}(\mathbf{T})=\{ [ x, y, z ]^T \, : \, x=y=z\}.$

Any vector from $\textrm{Im}(\mathbf{T})$ can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ x \\ x\end{bmatrix}=x\underbrace{\begin{bmatrix}1 \\ 1 \\ 1\end{bmatrix}}_{{v}_{1}}.\end{aligned}
$$

This means that $\textrm{Im}(\mathbf{T})=\textrm{Span}\{\mathbf{v}_1\}.$ Therefore, $\textrm{rank}(\mathbf{T})=1.$ 

Finally, according the rank-nullity theorem, we obtain

$$
\begin{aligned}\text{nullity}(T) & =3-\text{rank}(T) \\  & =3-1 \\  & =2.\end{aligned}
$$

### example 17592186188207 — Identifying True Statements Using the Rank-Nullity Theorem

Let $\mathbf{T}: \mathbb{R}^4 \rightarrow \mathbb{R}^4$ be a linear transformation whose standard matrix is $T,$ and let $\{ \mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3 \}$ be a set of linearly independent vectors in $\mathbb{R}^4.$ Consider the following statement:

*If  $\textrm{Im}(\mathbf{T})=\textrm{Span}\{ \mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}$, then $\underline{\phantom{xxxxxx}}.$* 

Which of the following can be placed into the blank space to make a true statement?

I. $\textrm{rank}(T)=3$

II. $\textrm{nullity}(\mathbf{T})=3$

III. $\mathbf{T}$ is a bijection

Since $\mathbf{T}$ is a linear transformation from $\mathbb{R}^4$ into $\mathbb{R}^4,$ the invertible matrix theorem states the following:

 $\mathbf{T}$ is a bijection (an invertible transformation) $$
\displaystyle \qquad \Longleftrightarrow \qquad
\left\{\;
{\begin{array}{rl}\displaystyle  & \displaystyle \text{Im} ( \mathbf{T} ) = {\mathbb{R}}^{4} \\ \displaystyle  & \displaystyle \text{rank} ( \mathbf{T} ) = 4 \\ \displaystyle  & \displaystyle \text{Ker} ( \mathbf{T} ) = \{  \mathbf{0} \}  \\ \displaystyle  & \displaystyle \text{nullity} ( \mathbf{T} ) = 0\end{array}} \right.
$$ 

Also, according to the rank-nullity theorem, 

$$
\textrm{rank}(\mathbf{T}) + \textrm{nullity}(\mathbf{T}) = 4.
$$

With that in mind, let's examine each statement in turn.

- Statement I is true. Since $\textrm{Im}(\mathbf{T})=\textrm{Span}\{ \mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3\}$ and the set $\{ \mathbf{v}_1, \mathbf{v}_2, \mathbf{v}_3 \}$ is linearly independent, we get that $\textrm{rank}(T)=\textrm{rank}(\mathbf{T})=3.$

- Statement II is false. According to the rank-nullity theorem, we obtain 

$$
\begin{aligned}\text{nullity}(T) & =4-\text{rank}(T) \\  & =4-3 \\  & =1.\end{aligned}
$$

- Statement III is false. Since $\textrm{rank}(\mathbf{T}) \neq 4$ (or since $\textrm{nullity}(\mathbf{T}) \neq 0$), the linear transformation $\mathbf{T}$ cannot be a bijection according to the invertible matrix theorem.

Therefore, the correct option is "I only."

## Representative practice (first three per skill; full bank in practice.json)

### Finding the Rank or Nullity of a Linear Transformation Using the Rank-Nullity Theorem (8 captured questions)

Question 17592186188917 — question.difficulty/easy

Consider a linear transformation $T:{R}^{5}\to {R}^{5}.$ If $\text{nullity}(T)=3$ then $\text{rank}(T)=$

Solution: According to the rank-nullity theorem, if $T:{R}^{n}\to {R}^{n},$ then

$$
\text{rank}(T)+\text{nullity}(T)=n.
$$

For the given transformation, we have $n=5.$ Therefore,

$$
\begin{aligned}\text{rank}(T)+\text{nullity}(T) & =n \\ \text{rank}(T)+3 & =5 \\ \text{rank}(T) & =5-3 \\  & =2.\end{aligned}
$$

Answer selection: 2

Question 17592186188981 — question.difficulty/easy

Consider a linear transformation $T:{R}^{7}\to {R}^{7}.$ If $\text{rank}(T)=3$ then $\text{nullity}(T)=$

Solution: According to the rank-nullity theorem, if $T:{R}^{n}\to {R}^{n},$ then

$$
\text{rank}(T)+\text{nullity}(T)=n.
$$

For the given transformation, we have $n=7.$ Therefore,

$$
\begin{aligned}\text{rank}(T)+\text{nullity}(T) & =n \\ 3+\text{nullity}(T) & =7 \\ \text{nullity}(T) & =7-3 \\  & =4.\end{aligned}
$$

Answer selection: 4

Question 17592186364975 — question.difficulty/easy

Consider a linear transformation $T:{R}^{6}\to {R}^{6}.$ If $\text{nullity}(T)=2$ then $\text{rank}(T)=$

Solution: According to the rank-nullity theorem, if $T:{R}^{n}\to {R}^{n},$ then

$$
\text{rank}(T)+\text{nullity}(T)=n.
$$

For the given transformation, we have $n=6.$ Therefore,

$$
\begin{aligned}\text{rank}(T)+\text{nullity}(T) & =n \\ \text{rank}(T)+2 & =6 \\ \text{rank}(T) & =6-2 \\  & =4.\end{aligned}
$$

Answer selection: 4

### Finding the Rank or Nullity of a Linear Transformation Given a Description of the Image or Kernel (11 captured questions)

Question 17592186188924 — question.difficulty/moderate

Find $\text{nullity}(T)$ given that $T:{R}^{3}\to {R}^{3}$ and 

$$
\text{Im}(T)=\{[x,y,z]^{T}\,:\,-x+z=0\}.
$$

Solution: Solving $-x+z=0$ for $z,$ we get $z=x.$ Therefore, any vector from $\text{Im}(T)$ can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ x\end{bmatrix}=x\underbrace{\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix}}_{{v}_{1}}+y\underbrace{\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix}}_{{v}_{2}}.\end{aligned}
$$

This means that $\text{Im}(T)=\text{Span}\{{v}_{1},{v}_{2}\}.$ Therefore, $\text{rank}(T)=2.$ 

Finally, according the rank-nullity theorem, we obtain

$$
\begin{aligned}\text{nullity}(T) & =3-\text{rank}(T) \\  & =3-2 \\  & =1.\end{aligned}
$$

Answer selection: 1

Question 17592186188982 — question.difficulty/moderate

Find $\text{rank}(T)$ given that $T:{R}^{4}\to {R}^{4}$ and 

$$
\text{Ker}(T)=\{[x,y,z,w]^{T}\,:\,x+y+z=0,\,2x-y-w=0\}.
$$

Solution: Solving $x+y+z=0$ for $z,$ we get $z=-x-y.$ Solving $2x-y-w=0$ for $w,$ we get $w=2x-y.$  Therefore, any vector from $\text{Ker}(T)$ can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ 2x-y \\ -x-y\end{bmatrix}=x\underbrace{\begin{bmatrix}1 \\ 0 \\ 2 \\ -1\end{bmatrix}}_{{v}_{1}}+y\underbrace{\begin{bmatrix}0 \\ 1 \\ -1 \\ -1\end{bmatrix}}_{{v}_{2}}.\end{aligned}
$$

This means that $\text{Ker}(T)=\text{Span}\{{v}_{1},{v}_{2}\}.$ Therefore, $\text{nullity}(T)=2.$ 

Finally, according the rank-nullity theorem, we obtain

$$
\begin{aligned}\text{rank}(T) & =4-\text{nullity}(T) \\  & =4-2 \\  & =2.\end{aligned}
$$

Answer selection: 2

Question 17592186365087 — question.difficulty/moderate

Find $\text{nullity}(T)$ given that $T:{R}^{3}\to {R}^{3}$ and $\text{Im}(T)=\{[x,y,z]^{T}\,:\,x-y+2z=0\}.$

Solution: Solving $x-y+2z=0$ for $y,$ we get $y=x+2z.$ Therefore, any vector from $\text{Im}(T)$ can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ x+2z \\ z\end{bmatrix}=x\underbrace{\begin{bmatrix}1 \\ 1 \\ 0\end{bmatrix}}_{{v}_{1}}+z\underbrace{\begin{bmatrix}0 \\ 2 \\ 1\end{bmatrix}}_{{v}_{2}}\end{aligned}
$$

This means that $\text{Im}(T)=\text{Span}\{{v}_{1},{v}_{2}\}.$ Therefore, $\text{rank}(T)=2.$ 

Finally, according the rank-nullity theorem, we obtain

$$
\begin{aligned}\text{nullity}(T) & =3-\text{rank}(T) \\  & =3-2 \\  & =1.\end{aligned}
$$

Answer selection: 1

### Identifying True Statements Using the Rank-Nullity Theorem (11 captured questions)

Question 17592186188911 — question.difficulty/moderate

Let $T:{R}^{5}\to {R}^{5}$ be a linear transformation whose standard matrix is $T,$ and let ${{v}_{1},{v}_{2},{v}_{3}}$ be a set of linearly independent vectors in ${R}^{5}.$ Consider the following statement:

*If  $\text{Im}(T)=\text{Span}{{v}_{1},{v}_{2},{v}_{3}}$, then $\underline{\phantom{xxxxxx}}.$* 

Which of the following can be placed into the blank space to make a true statement?

Select all that apply.

Solution: Since $T$ is a linear transformation from ${R}^{5}$ into ${R}^{5},$ the invertible matrix theorem states the following:

 $T$ is a bijection (an invertible transformation) $$
\displaystyle \,⟺\,\left\{\,\begin{aligned} & \text{Im}(T)={R}^{5} \\  & \text{rank}(T)=5 \\  & \text{Ker}(T)={0} \\  & \text{nullity}(T)=0\end{aligned}\right.
$$ 

Also, according to the rank-nullity theorem, 

$$
\text{rank}(T)+\text{nullity}(T)=5.
$$

With that in mind, let's examine each statement in turn.

- Statement $\text{rank}(T)=1$ is false. Since $\text{Im}(T)=\text{Span}{{v}_{1},{v}_{2},{v}_{3}}$ and the set ${{v}_{1},{v}_{2},{v}_{3}}$ is linearly independent, we get that $\text{rank}(T)=\text{rank}(T)=3.$

- Statement $\text{nullity}(T)=2$ is true. According to the rank-nullity theorem, we obtain 

$$
\begin{aligned}\text{nullity}(T) & =5-\text{rank}(T) \\  & =5-3 \\  & =2.\end{aligned}
$$

- Statement “$T$ is a bijection” is false. Since $\text{rank}(T)\ne 5$ (or since $\text{nullity}(T)\ne 0$), the linear transformation $T$ cannot be a bijection according to the invertible matrix theorem.

Therefore, the correct option is $\text{nullity}(T)=2$ only.

Answer $T$ is a bijection: false

Answer $\text{nullity}(T)=2$: true

Answer $\text{rank}(T)=1$: false

Answer None of the above: false

Question 17592186188925 — question.difficulty/hard

Let $T:{R}^{3}\to {R}^{3}$ be a linear transformation whose standard matrix is $T.$ Which of the following statements are true?

Select all that apply.

Solution: Since $T$ is a linear transformation from ${R}^{3}$ into ${R}^{3},$ the invertible matrix theorem states the following:

 $T$ is a bijection (an invertible transformation) $$
\displaystyle \,⟺\,\left\{\,\begin{aligned} & \text{Im}(T)={R}^{3} \\  & \text{rank}(T)=3 \\  & \text{Ker}(T)={0} \\  & \text{nullity}(T)=0\end{aligned}\right.
$$ 

Also, according to the rank-nullity theorem, 

$$
\text{rank}(T)+\text{nullity}(T)=3.
$$

With that in mind, let's examine each statement in turn.

- Statement “If $$
\displaystyle \begin{gathered}\text{Im}(T)=\left\{\begin{gathered}\,[x,y,z]^{T}\,:\\\,3x+2y-z=0\end{gathered}\right\}\end{gathered}
$$ then $\text{nullity}(T)=1$” is true. Solving $3x+2y-z=0$ for $z,$ we get $z=3x+2y.$ Therefore, any vector from $\text{Im}(T)$ can be written as

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}x \\ y \\ 3x+2y\end{bmatrix}=x\underbrace{\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix}}_{{v}_{1}}+y\underbrace{\begin{bmatrix}0 \\ 1 \\ 2\end{bmatrix}}_{{v}_{2}}.\end{aligned}
$$

This means that $\text{Im}(T)=\text{Span}{{v}_{1},{v}_{2}}.$ Therefore, $\text{rank}(T)=2.$ Finally, according the rank-nullity theorem, we obtain

$$
\begin{aligned}\text{nullity}(T) & =3-\text{rank}(T) \\  & =3-2 \\  & =1.\end{aligned}
$$

- Statement “If ${v}_{1}$ and ${v}_{2}$ are two different solutions to $Tx=[1,-2,1]^{T}$ then $T$ is invertible” is false. If ${v}_{1}$ and ${v}_{2}$ are two different solutions to $Tx=[1,-2,1]^{T},$ then 

$$
T{v}_{1}=T{v}_{2}\,⟹\,T({v}_{1}-{v}_{2})=0,
$$

where ${v}_{1}-{v}_{2}$ is a non-zero vector. This means that $\text{Ker}(T)=\text{Null}(T)\ne {0}$ and, according to the invertible matrix theorem, $T$ can't be invertible.

- Statement “If ${v}_{1},$ ${v}_{2},$ and ${v}_{3}$ are the columns of $T$ and ${v}_{3}={v}_{1}+2{v}_{2}$, then $\text{Ker}(T)={0}$” is false. If the columns of $T$ are such that ${v}_{3}={v}_{1}+2{v}_{2},$ then the set of vectors ${{v}_{1},{v}_{2},{v}_{3}}$ is linearly dependent and therefore $\text{Im}(T)=\text{Col}(T)\ne {R}^{3}.$ Now, according to the matrix invertible theorem, we obtain that $\text{Ker}(T)\ne {0}.$

Therefore, the correct answer is “If $$
\displaystyle \begin{gathered}\text{Im}(T)=\left\{\begin{gathered}\,[x,y,z]^{T}\,:\\\,3x+2y-z=0\end{gathered}\right\}\end{gathered}
$$ then $\text{nullity}(T)=1$” only.

Answer If $\begin{gathered}\text{Im}(T)=\left\{\begin{gathered}\,[x,y,z]^{T}\,:\\\,3x+2y-z=0\end{gathered}\right\}\end{gathered}$ then $\text{nullity}(T)=1$: true

Answer If ${v}_{1}$ and ${v}_{2}$ are two different solutions to $Tx=[1,-2,1]^{T}$ then $T$ is invertible: false

Answer If ${v}_{1},$ ${v}_{2},$ and ${v}_{3}$ are the columns of $T$ and ${v}_{3}={v}_{1}+2{v}_{2}$, then $\text{Ker}(T)={0}$: false

Question 17592186366039 — question.difficulty/hard

Let $T:{R}^{3}\to {R}^{3}$ be a linear transformation whose standard matrix is $T.$ Which of the following statements are true?

Select all that apply.

Solution: Since $T$ is a linear transformation from ${R}^{3}$ into ${R}^{3},$ the invertible matrix theorem states the following:

 $T$ is a bijection (an invertible transformation) $$
\displaystyle \,⟺\,\left\{\,\begin{aligned} & \text{Im}(T)={R}^{3} \\  & \text{rank}(T)=3 \\  & \text{Ker}(T)={0} \\  & \text{nullity}(T)=0\end{aligned}\right.
$$ 

Also, according to the rank-nullity theorem, 

$$
\text{rank}(T)+\text{nullity}(T)=3.
$$

With that in mind, let's examine each statement in turn.

- Statement “If $\text{rank}(T)=2,$ then $\text{Ker}(T)={0}$” is false. According to the rank-nullity theorem, we obtain 

$$
\begin{aligned}\text{nullity}(T) & =3-\text{rank}(T) \\  & =3-2 \\  & =1.\end{aligned}
$$

Therefore, $\text{Ker}(T)\ne {0}.$

- Statement “If $[-2,0,0]^{T}$ is a solution of $T(x)=0$ then $\text{nullity}(T)\ne 0$” is true. Since $\begin{bmatrix}-2 \\ 0 \\ 0\end{bmatrix}$ is a solution of $Tx=0$, we have that $\begin{bmatrix}-2 \\ 0 \\ 0\end{bmatrix}\in \text{Ker}(T)$ and therefore $\text{nullity}(T)\ne 0.$

- Statement “If $T(x)=[1,0,0]^{T}$ has no solution then $\text{rank}(T)=3$” is false. Since $T(x)=\begin{bmatrix}1 \\ 0 \\ 0\end{bmatrix}$ has no solution, we have that $\text{Im}(T)\ne {R}^{3}.$ Hence, $\text{rank}(T)\ne 3.$

Therefore, the correct option is “If $[-2,0,0]^{T}$ is a solution of $T(x)=0$ then $\text{nullity}(T)\ne 0$” only.

Answer If $T(x)=[1,0,0]^{T}$ has no solution then $\text{rank}(T)=3$: false

Answer If $[-2,0,0]^{T}$ is a solution of $T(x)=0$ then $\text{nullity}(T)\ne 0$: true

Answer If $\text{rank}(T)=2,$ then $\text{Ker}(T)={0}$: false

Answer None of the above: false
