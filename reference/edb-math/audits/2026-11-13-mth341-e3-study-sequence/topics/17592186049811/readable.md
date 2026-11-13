# 17592186049811 Orthogonal Sets in Euclidean Spaces

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186135045 — Introduction

A set of vectors ${U}=\{ \mathbf{u}_1, \cdots, \mathbf{u}_p \}$ in $\mathbb{R}^n$ is an **orthogonal set** if each pair of distinct vectors from the set is orthogonal.

For example, let's consider the following set:

$$
{W}=\left\{ {\left[ \begin{array}{c}3 \\ 1 \\ 1\end{array} \right]}, {\left[ \begin{array}{c}- 1 \\ 2 \\ 1\end{array} \right]}, {\left[ \begin{array}{c}- 1 \\ - 4 \\ 7\end{array} \right]} \right\}
$$

If we denote the vectors in our set ${W}$ as $\{ \mathbf{w}_1, \mathbf{w}_2, \mathbf{w}_3 \},$ we can check that ${W}$ is orthogonal by showing that 

$$
\left\{\begin{aligned}{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{2} &=0 \\ {\mathbf{w}}_{1}\cdot {\mathbf{w}}_{3} &=0 \\ {\mathbf{w}}_{2}\cdot {\mathbf{w}}_{3} &=0.\end{aligned}\right.
$$

Let's compute each dot product:

$$
\begin{aligned}{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{2} & =\begin{bmatrix}3 \\ 1 \\ 1\end{bmatrix}\cdot \begin{bmatrix}-1 \\ 2 \\ 1\end{bmatrix}=3\cdot (-1)+1\cdot 2+1\cdot 1=0 & {\color{green}✓} \\ {\mathbf{w}}_{1}\cdot {\mathbf{w}}_{3} & =\begin{bmatrix}3 \\ 1 \\ 1\end{bmatrix}\cdot \begin{bmatrix}-1 \\ -4 \\ 7\end{bmatrix}=3\cdot (-1)+1\cdot (-4)+1\cdot 7=0 & {\color{green}✓} \\ {\mathbf{w}}_{2}\cdot {\mathbf{w}}_{3} & =\begin{bmatrix}-1 \\ 2 \\ 1\end{bmatrix}\cdot \begin{bmatrix}-1 \\ -4 \\ 7\end{bmatrix}=(-1)\cdot (-1)+2\cdot (-4)+1\cdot 7=0 & {\color{green}✓}\end{aligned}
$$

So indeed, ${W}$ is an orthogonal set.

If an orthogonal set is also a basis, then we call it an **orthogonal basis**. Here, $W$ is an orthogonal basis of $\mathbb{R}^3,$ because it contains three linearly independent (you can check this) orthogonal vectors.



### example 17592186133658 — Determining Whether Sets are Orthogonal

Determine whether the following set is orthogonal:
$$
{X}=\left\{ {\left[ \begin{array}{c}2 \\ 0 \\ 1\end{array} \right]}, {\left[ \begin{array}{c}- 1 \\ 0 \\ 2\end{array} \right]}, {\left[ \begin{array}{c}1 \\ - 2 \\ 0\end{array} \right]} \right\}
$$

If we denote the vectors in our set ${X}$ as $\{ \mathbf{x}_1, \mathbf{x}_2, \mathbf{x}_3 \},$ we can check that ${X}$ is orthogonal by showing that 

$$
\left\{\begin{aligned}{\mathbf{x}}_{1}\cdot {\mathbf{x}}_{2} &=0 \\ {\mathbf{x}}_{1}\cdot {\mathbf{x}}_{3} &=0 \\ {\mathbf{x}}_{2}\cdot {\mathbf{x}}_{3} &=0.\end{aligned}\right.
$$

Let's compute each dot product:

$$
\begin{aligned}{\mathbf{x}}_{1}\cdot {\mathbf{x}}_{2} & =\begin{bmatrix}2 \\ 0 \\ 1\end{bmatrix}\cdot \begin{bmatrix}-1 \\ 0 \\ 2\end{bmatrix}=2\cdot (-1)+0\cdot 0+1\cdot 2=0 & {\color{green}✓} \\ {\mathbf{x}}_{1}\cdot {\mathbf{x}}_{3} & =\begin{bmatrix}2 \\ 0 \\ 1\end{bmatrix}\cdot \begin{bmatrix}1 \\ -2 \\ 0\end{bmatrix}=2\cdot 1+0\cdot (-2)+1\cdot 0=2\ne 0 & {\color{red}\times } \\ {\mathbf{x}}_{2}\cdot {\mathbf{x}}_{3} & =\begin{bmatrix}-1 \\ 0 \\ 2\end{bmatrix}\cdot \begin{bmatrix}1 \\ -2 \\ 0\end{bmatrix}=(-1)\cdot 1+0\cdot (-2)+2\cdot 0=-1\ne 0 & {\color{red}\times }\end{aligned}
$$

So ${X}$ is *not* an orthogonal set.

### tutorial 17592186135090 — Orthonormal Sets and Orthonormal Bases

A set of vectors ${U}=\{\mathbf{u}_1, \cdots, \mathbf{u}_p \}$ is an **orthonormal set** if it is an orthogonal set of *unit* vectors. Remember that $\mathbf u_i$ is a unit vector if $\Vert \mathbf u_i \Vert = 1,$ or equivalently, $\mathbf u_i \cdot \mathbf u_i = 1.$

An orthonormal set that is also a basis, like the standard basis, is called an **orthonormal basis**. For instance, the standard basis $\{\mathbf{e}_1, \mathbf{e}_2, \mathbf{e}_3\}$ of $\mathbb R^3$ is an orthonormal basis because the vectors are orthogonal to each other and each vector in the set is a unit vector.

There are two more things to note about orthogonal sets:

- Any orthogonal set of non-zero vectors is linearly independent.

- An orthogonal set of non-zero vectors in $\Bbb R^n$ cannot contain more than $n$ vectors. More precisely, if $V = \{\mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_p\}$ is an orthogonal set of non-zero vectors and $\mathbf{v}_i\in\mathbb{R}^n,$ then we must have that $p\leq n.$

**Note:** To remember that an orthogonal set of non-zero vectors in $\Bbb R^n$ cannot contain more than $n$ vectors, you can use the following intuitive mnemonic. There are only $n$ dimensions in $\Bbb R^n,$ and each non-zero orthogonal vector has a $1$-dimensional span, meaning that it "takes up" $1$ dimension of $\Bbb R^n.$ So, you can't "fit" more than $n$ orthogonal vectors in $\Bbb R^n.$



### example 17592186133590 — Determining Whether Sets are Orthonormal

Determine whether the following set is orthonormal:
$$
{W}=\left\{ {\left[ \begin{array}{c}{\displaystyle \frac{1}{\sqrt{2}}} \\ - {\displaystyle \frac{1}{\sqrt{2}}}\end{array} \right]}, {\left[ \begin{array}{c}4 \\ 4\end{array} \right]} \right\}
$$

Let's denote the vectors of the given set as $\{\mathbf{w}_1,\mathbf{w}_2\},$ respectively. 

The set $W$ is orthonormal if the following conditions hold:

$$
\mathbf{w}_1\cdot\mathbf{w}_2=0 
\quad \text{and}\quad
{\left\{  \begin{array}{l}{\mathbf{w}}_{1} \cdot  {\mathbf{w}}_{1} = 1 \\ {\mathbf{w}}_{2} \cdot  {\mathbf{w}}_{2} = 1\end{array} \right. }
$$

With that in mind, let's examine our set:

$$
\begin{aligned}{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{2} & =\begin{bmatrix}\frac{1}{\sqrt{2}} \\ -\frac{1}{\sqrt{2}}\end{bmatrix}\cdot \begin{bmatrix}4 \\ 4\end{bmatrix}=\frac{4}{\sqrt{2}}-\frac{4}{\sqrt{2}}=0 & {\color{green}✓} \\ {\mathbf{w}}_{1}\cdot {\mathbf{w}}_{1} & =\begin{bmatrix}\frac{1}{\sqrt{2}} \\ -\frac{1}{\sqrt{2}}\end{bmatrix}\cdot \begin{bmatrix}\frac{1}{\sqrt{2}} \\ -\frac{1}{\sqrt{2}}\end{bmatrix}=\frac{1}{2}+\frac{1}{2}=1 & {\color{green}✓} \\ {\mathbf{w}}_{2}\cdot {\mathbf{w}}_{2} & =\begin{bmatrix}4 \\ 4\end{bmatrix}\cdot \begin{bmatrix}4 \\ 4\end{bmatrix}=16+16=32\ne 1 & {\color{red}\times }\end{aligned}
$$

We see that $\mathbf w_1$ and $\mathbf w_2$ are orthogonal, and $\mathbf w_1$ is a unit vector, but $\mathbf w_2$ is *not* a unit vector.

Therefore, ${W}$ is *not* an orthonormal set.

### example 17592186133591 — Extending a Set to Form an Orthogonal Basis

Consider the orthogonal set $U$ below. By adding a new vector $\mathbf x = [x_1,\,x_2,\,x_3]^T,$ extend the set so that it forms an orthogonal basis of $\mathbb{R}^3.$ 

$$
{U}=\left\{ {\left[ \begin{array}{c}- 1 \\ - 1 \\ 2\end{array} \right]}, {\left[ \begin{array}{c}1 \\ 1 \\ 1\end{array} \right]}\right\}
$$

Let's denote the vectors of ${U}$ as $\mathbf{u}_1,\, \mathbf{u}_2.$ To extend the given set to an orthogonal basis of $\mathbb{R}^3,$ we need to find a third vector $\mathbf{x} = {\left[ \begin{array}{c}{x}_{1} \\ {x}_{2} \\ {x}_{3}\end{array} \right]}$ such that

$$
{\left\{  \begin{array}{l}{\mathbf{u}}_{1} \cdot  \mathbf{x} = 0 \\ {\mathbf{u}}_{2} \cdot  \mathbf{x} = 0\end{array} \right. }
\qquad\Longrightarrow\qquad
{\left\{  \begin{array}{l}- {x}_{1} - {x}_{2} + 2 {x}_{3} = 0 \\ {x}_{1} + {x}_{2} + {x}_{3} = 0.\end{array} \right. }
$$

So, we consider the augmented matrix $M$ of the system above and reduce it to row echelon form, as follows:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}-1 & -1 & 2 & 0 \\ 1 & 1 & 1 & 0\end{array}\right] & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}-1 & -1 & 2 & 0 \\ 0 & 0 & 3 & 0\end{array}\right]\end{aligned}
$$

In the reduced matrix above, there are two pivot columns ($1$st and $3$rd). This means $x_2$ is a free variable. From the second equation, we get $x_3=0.$ Substituting this into the first equation, we obtain

$$
\begin{aligned}-{x}_{1}-{x}_{2}+2(0)=0\,⟹\,{x}_{1}=-{x}_{2}.\end{aligned}
$$

So, the general solution is
$$
{\left[ \begin{array}{c}- {x}_{2} \\ {x}_{2} \\ 0\end{array} \right]},
\qquad x_2 \in\mathbb{R}.
$$

Setting $x_2=1,$ we obtain the vector 

$$
\mathbf{x}={\left[ \begin{array}{c}- 1 \\ 1 \\ 0\end{array} \right]}.
$$

Therefore, an orthogonal basis of $\mathbb{R}^3$ is
$$
\left\{ {\left[ \begin{array}{c}- 1 \\ - 1 \\ 2\end{array} \right]}, {\left[ \begin{array}{c}1 \\ 1 \\ 1\end{array} \right]},{\left[ \begin{array}{c}- 1 \\ 1 \\ 0\end{array} \right]} \right\}.
$$

### example 17592186133652 — Extending a Set to Form an Orthonormal Basis

Consider the **orthonormal** set $U$ below. By adding a new vector $\mathbf x = [x_1,\,x_2,\,x_3]^T,$ extend the set so that it forms an **orthonormal** basis of $\mathbb{R}^3.$ 
$$
{U}=\left\{ {\left[ \begin{array}{c}- {\displaystyle \frac{1}{\sqrt{2}}} \\ 0 \\ {\displaystyle \frac{1}{\sqrt{2}}}\end{array} \right]}, {\left[ \begin{array}{c}{\displaystyle \frac{1}{\sqrt{6}}} \\ {\displaystyle \frac{2}{\sqrt{6}}} \\ {\displaystyle \frac{1}{\sqrt{6}}}\end{array} \right]}\right\}
$$

Let's denote the vectors of ${U}$ as $\mathbf{u}_1,\, \mathbf{u}_2.$ To extend the given set to an orthonormal basis of $\mathbb{R}^3,$ we need to find a third vector $\mathbf{x}$ such that $\| \mathbf{x} \|=1$ and

$$
{\left\{  \begin{array}{l}{\mathbf{u}}_{1} \cdot  \mathbf{x} = 0 \\ {\mathbf{u}}_{2} \cdot  \mathbf{x} = 0\end{array} \right. }
\qquad\Longrightarrow\qquad
{\left\{  \begin{array}{l}- {\displaystyle \frac{1}{\sqrt{2}}} {x}_{1} + {\displaystyle \frac{1}{\sqrt{2}}} {x}_{3} = 0 \\ {\displaystyle \frac{1}{\sqrt{6}}} {x}_{1} + {\displaystyle \frac{2}{\sqrt{6}}} {x}_{2} + {\displaystyle \frac{1}{\sqrt{6}}} {x}_{3} = 0.\end{array} \right. }
$$

So, we consider the augmented matrix $M$ of the system above and reduce it to row echelon form, as follows:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}-\frac{1}{\sqrt{2}} & 0 & \frac{1}{\sqrt{2}} & 0 \\ \frac{1}{\sqrt{6}} & \frac{2}{\sqrt{6}} & \frac{1}{\sqrt{6}} & 0\end{array}\right] &  & \begin{aligned}{R}_{1}:=\sqrt{2}\cdot {R}_{1} \\ {R}_{2}:=\sqrt{6}\cdot {R}_{2}\end{aligned} \\  & ∼\left[\begin{array}{ccc|c}-1 & 0 & 1 & 0 \\ 1 & 2 & 1 & 0\end{array}\right] &  & \begin{aligned}{R}_{2}:={R}_{2}+{R}_{1}\end{aligned} \\  & ∼\left[\begin{array}{ccc|c}-1 & 0 & 1 & 0 \\ 0 & 2 & 2 & 0\end{array}\right]\end{aligned}
$$

In the reduced matrix above, there are two pivot columns ($1$st and $2$nd). This means $x_3$ is a free variable. From the second equation, we get $x_2=-x_3,$ and from the first equation, we obtain $x_1=x_3.$

So, the general solution is

$$
{\left[ \begin{array}{c}{x}_{3} \\ - {x}_{3} \\ {x}_{3}\end{array} \right]},
\qquad x_3 \in\mathbb{R}.
$$

Setting $x_3=1,$ we obtain the vector 
$$
\mathbf{x}={\left[ \begin{array}{c}1 \\ - 1 \\ 1\end{array} \right]}.
$$ 

Now, we need to normalize $\mathbf{x}.$ Notice that $\| \mathbf{x} \| = \sqrt{1^2+(-1)^2+1^2} = \sqrt{3}.$ So, we normalize $\mathbf x$ as follows:

$$
\dfrac{\mathbf{x}}{\|\mathbf{x}\|}={\left[ \begin{array}{c}{\displaystyle \frac{1}{\sqrt{3}}} \\ - {\displaystyle \frac{1}{\sqrt{3}}} \\ {\displaystyle \frac{1}{\sqrt{3}}}\end{array} \right]}
$$

Therefore, an orthonormal basis of $\mathbb{R}^3$ is
$$
\left\{ {\left[ \begin{array}{c}- {\displaystyle \frac{1}{\sqrt{2}}} \\ 0 \\ {\displaystyle \frac{1}{\sqrt{2}}}\end{array} \right]}, {\left[ \begin{array}{c}{\displaystyle \frac{1}{\sqrt{6}}} \\ {\displaystyle \frac{2}{\sqrt{6}}} \\ {\displaystyle \frac{1}{\sqrt{6}}}\end{array} \right]},{\left[ \begin{array}{c}{\displaystyle \frac{1}{\sqrt{3}}} \\ - {\displaystyle \frac{1}{\sqrt{3}}} \\ {\displaystyle \frac{1}{\sqrt{3}}}\end{array} \right]} \right\}.
$$

## Representative practice (first three per skill; full bank in practice.json)

### Determining Whether Sets are Orthogonal (11 captured questions)

Question 17592186134222 — question.difficulty/easy

Which of the following sets are orthogonal?

1. $$
U=\left\{\begin{bmatrix}1 \\ 2 \\ 1 \\ -2\end{bmatrix},\begin{bmatrix}1 \\ 3 \\ -1 \\ 3\end{bmatrix},\begin{bmatrix}2 \\ -1 \\ 2 \\ 1\end{bmatrix}\right\}
$$
2. $$
V=\left\{\begin{bmatrix}2 \\ 2 \\ -2\end{bmatrix},\begin{bmatrix}1 \\ -2 \\ -1\end{bmatrix},\begin{bmatrix}-6 \\ 0 \\ -6\end{bmatrix}\right\}
$$
3. $W=\left\{\begin{bmatrix}4 \\ -1\end{bmatrix},\begin{bmatrix}-2 \\ -2\end{bmatrix}\right\}$

Solution: A set is orthogonal when every pair of distinct vectors has dot product zero. Denoting the vectors in each displayed set by subscripts, we obtain

$$
\begin{aligned}u_1\cdot u_2&=1+6-1-6=0,&u_1\cdot u_3&=2-2+2-2=0,&u_2\cdot u_3&=2-3-2+3=0,\\v_1\cdot v_2&=2-4+2=0,&v_1\cdot v_3&=-12+0+12=0,&v_2\cdot v_3&=-6+0+6=0,\\w_1\cdot w_2&=-8+2=-6.\end{aligned}
$$

Thus $U$ and $V$ are orthogonal, while $W$ is not. The correct answer is $U$ and $V$ only.

Answer selection: $U$ and $V$ only

Question 17592186134286 — question.difficulty/easy

Which of the following sets are orthogonal?

Select all that apply.

Solution: Let's denote the vectors of the given sets as 
$\{{\mathbf{u}}_{1},{\mathbf{u}}_{2}\},$ 
$\{{\mathbf{v}}_{1},{\mathbf{v}}_{2},{\mathbf{v}}_{3}\},$ and 
$\{{\mathbf{w}}_{1},{\mathbf{w}}_{2}\},$ respectively. 

The sets $U,V,$ and $W$ are orthogonal if the following conditions on each set hold:

- ${\mathbf{u}}_{1}\cdot {\mathbf{u}}_{2}=0.$

- $$
{\mathbf{v}}_{1}\cdot {\mathbf{v}}_{2}=0,\hspace{1em}{\mathbf{v}}_{1}\cdot {\mathbf{v}}_{3}=0,\hspace{1em}{\mathbf{v}}_{2}\cdot {\mathbf{v}}_{3}=0.
$$

- ${\mathbf{w}}_{1}\cdot {\mathbf{w}}_{2}=0.$

With that in mind, let's examine our sets in turn.

- For the set $U,$ we get the following:

$$
\begin{aligned}{\mathbf{u}}_{1}\cdot {\mathbf{u}}_{2} & =\begin{bmatrix}5 \\ -1\end{bmatrix}\cdot \begin{bmatrix}1 \\ 5\end{bmatrix}=5-5=0 & {\color{green}✓}\end{aligned}
$$

So, the set $U$ is orthogonal.

- The set $V$ cannot be orthogonal since it contains  $3$ vectors from ${\mathbb{R}}^{2}$ (in which we can have an orthogonal set with at most $2$ non-zero vectors). So, $V$ is not an orthogonal set.

- For the set $W,$ we get the following:

$$
\begin{aligned}{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{2} & =\begin{bmatrix}4 \\ 0 \\ -1\end{bmatrix}\cdot \begin{bmatrix}1 \\ 0 \\ 4\end{bmatrix}=4+0-4=0 & {\color{green}✓}\end{aligned}
$$

So, the set $W$ is orthogonal.

Therefore, we conclude that the correct answer is "$U$ and $W$ only".

Answer $U=\left\{\begin{bmatrix}5 \\ -1\end{bmatrix},\begin{bmatrix}1 \\ 5\end{bmatrix}\right\}$: true

Answer $V=\left\{\begin{bmatrix}1 \\ -1\end{bmatrix},\begin{bmatrix}1 \\ 0\end{bmatrix},\begin{bmatrix}0 \\ 1\end{bmatrix}\right\}$: false

Answer $W=\left\{\begin{bmatrix}4 \\ 0 \\ -1\end{bmatrix},\begin{bmatrix}1 \\ 0 \\ 4\end{bmatrix}\right\}$: true

Answer None of the above: false

Question 17592186272104 — question.difficulty/easy

Which of the following sets are orthogonal?

Select all that apply.

Solution: Let's denote the vectors of the given sets as 
$\{{\mathbf{u}}_{1},{\mathbf{u}}_{2}\},$ 
$\{{\mathbf{v}}_{1},{\mathbf{v}}_{2}\},$ and 
$\{{\mathbf{w}}_{1},{\mathbf{w}}_{2},{\mathbf{w}}_{3}\},$ respectively. 

The sets $U,V,$ and $W$ are orthogonal if the following conditions on each set hold:

- ${\mathbf{u}}_{1}\cdot {\mathbf{u}}_{2}=0.$

- ${\mathbf{v}}_{1}\cdot {\mathbf{v}}_{2}=0.$

- $$
{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{2}=0,\hspace{1em}{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{3}=0,\hspace{1em}{\mathbf{w}}_{2}\cdot {\mathbf{w}}_{3}=0.
$$

With that in mind, let's examine our sets in turn.

- For the set $U,$ notice that

$$
\begin{aligned}{\mathbf{u}}_{1}\cdot {\mathbf{u}}_{2} & =\begin{bmatrix}5 \\ 3 \\ -1\end{bmatrix}\cdot \begin{bmatrix}2 \\ -3 \\ 1\end{bmatrix}=10-9-1=0 & {\color{green}✓}\end{aligned}
$$

So, the set $U$ is orthogonal.

- For the set $V,$ notice that 

$$
\begin{aligned}{\mathbf{v}}_{1}\cdot {\mathbf{v}}_{2} & =\begin{bmatrix}1 \\ 2 \\ 2\end{bmatrix}\cdot \begin{bmatrix}4 \\ -2 \\ 2\end{bmatrix}=4-4+4=4\ne 0 & {\color{red}\times }\end{aligned}
$$

So, $V$ is not an orthogonal set.

- For the set $W,$ notice that

$$
\begin{aligned}{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{2} & =\begin{bmatrix}5 \\ 3 \\ 1\end{bmatrix}\cdot \begin{bmatrix}2 \\ -3 \\ -1\end{bmatrix}=10-9-1=0 & {\color{green}✓} \\ {\mathbf{w}}_{1}\cdot {\mathbf{w}}_{3} & =\begin{bmatrix}5 \\ 3 \\ 1\end{bmatrix}\cdot \begin{bmatrix}0 \\ 1 \\ -3\end{bmatrix}=0+3-3=0 & {\color{green}✓} \\ {\mathbf{w}}_{2}\cdot {\mathbf{w}}_{3} & =\begin{bmatrix}2 \\ -3 \\ -1\end{bmatrix}\cdot \begin{bmatrix}0 \\ 1 \\ -3\end{bmatrix}=0-3+3=0 & {\color{green}✓}\end{aligned}
$$

So, the set $W$ is orthogonal.

Therefore, we conclude that the correct answer is "$U$ and $W$ only".

Answer $U=\left\{\begin{bmatrix}5 \\ 3 \\ -1\end{bmatrix},\begin{bmatrix}2 \\ -3 \\ 1\end{bmatrix}\right\}$: true

Answer $V=\left\{\begin{bmatrix}1 \\ 2 \\ 2\end{bmatrix},\begin{bmatrix}4 \\ -2 \\ 2\end{bmatrix}\right\}$: false

Answer $W=\left\{\begin{bmatrix}5 \\ 3 \\ 1\end{bmatrix},\begin{bmatrix}2 \\ -3 \\ -1\end{bmatrix},\begin{bmatrix}0 \\ 1 \\ -3\end{bmatrix}\right\}$: true

### Determining Whether Sets are Orthonormal (12 captured questions)

Question 17592186134215 — question.difficulty/moderate

Which of the following sets are orthonormal?

Select all that apply.

Solution: Let's denote the vectors of the given sets as 
$\{{\mathbf{u}}_{1},{\mathbf{u}}_{2}\},$ 
$\{{\mathbf{v}}_{1},{\mathbf{v}}_{2},{\mathbf{v}}_{3}\},$ and 
$\{{\mathbf{w}}_{1},{\mathbf{w}}_{2}\},$ respectively. 

The sets $U,V,$ and $W$ are orthonormal if the following conditions on each set hold:

- $$
{\mathbf{u}}_{1}\cdot {\mathbf{u}}_{2}=0\hspace{1em}\text{and}\hspace{1em}\left\{\begin{aligned}{\mathbf{u}}_{1}\cdot {\mathbf{u}}_{1} &=1 \\ {\mathbf{u}}_{2}\cdot {\mathbf{u}}_{2} &=1.\end{aligned}\right.
$$

- $$
\left\{\begin{aligned}{\mathbf{v}}_{1}\cdot {\mathbf{v}}_{2} &=0 \\ {\mathbf{v}}_{1}\cdot {\mathbf{v}}_{3} &=0 \\ {\mathbf{v}}_{2}\cdot {\mathbf{v}}_{3} &=0\end{aligned}\right.\hspace{1em}\text{and}\hspace{1em}\left\{\begin{aligned}{\mathbf{v}}_{1}\cdot {\mathbf{v}}_{1} &=1 \\ {\mathbf{v}}_{2}\cdot {\mathbf{v}}_{2} &=1 \\ {\mathbf{v}}_{3}\cdot {\mathbf{v}}_{3} &=1.\end{aligned}\right.
$$

- $$
{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{2}=0\hspace{1em}\text{and}\hspace{1em}\left\{\begin{aligned}{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{1} &=1 \\ {\mathbf{w}}_{2}\cdot {\mathbf{w}}_{2} &=1.\end{aligned}\right.
$$

With that in mind, let's examine our sets in turn.

- For the set $U,$ we get the following:

$$
\begin{aligned}{\mathbf{u}}_{1}\cdot {\mathbf{u}}_{2} & =\begin{bmatrix}-\frac{3}{\sqrt{10}} \\ \frac{1}{\sqrt{10}}\end{bmatrix}\cdot \begin{bmatrix}\frac{1}{\sqrt{10}} \\ \frac{3}{\sqrt{10}}\end{bmatrix}=-\frac{3}{10}+\frac{3}{10}=0 & {\color{green}✓} \\ {\mathbf{u}}_{1}\cdot {\mathbf{u}}_{1} & =\begin{bmatrix}-\frac{3}{\sqrt{10}} \\ \frac{1}{\sqrt{10}}\end{bmatrix}\cdot \begin{bmatrix}-\frac{3}{\sqrt{10}} \\ \frac{1}{\sqrt{10}}\end{bmatrix}=\frac{9}{10}+\frac{1}{10}=1 & {\color{green}✓} \\ {\mathbf{u}}_{2}\cdot {\mathbf{u}}_{2} & =\begin{bmatrix}\frac{1}{\sqrt{10}} \\ \frac{3}{\sqrt{10}}\end{bmatrix}\cdot \begin{bmatrix}\frac{1}{\sqrt{10}} \\ \frac{3}{\sqrt{10}}\end{bmatrix}=\frac{1}{10}+\frac{9}{10}=1 & {\color{green}✓}\end{aligned}
$$

So, the set $U$ is orthonormal.

- For the set $V,$ notice that

$$
\begin{aligned}{\mathbf{v}}_{1}\cdot {\mathbf{v}}_{1} & =\begin{bmatrix}2 \\ 3 \\ -1\end{bmatrix}\cdot \begin{bmatrix}2 \\ 3 \\ -1\end{bmatrix}=4+9+1=14\ne 1 & {\color{red}\times }\end{aligned}
$$

So, $V$ is not an orthonormal set.

- For the set $W,$ we get the following:

$$
\begin{aligned}{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{2} & =\begin{bmatrix}\frac{3}{5} \\ \frac{4}{5}\end{bmatrix}\cdot \begin{bmatrix}\frac{4}{5} \\ -\frac{3}{5}\end{bmatrix}=\frac{12}{25}-\frac{12}{25}=0 & {\color{green}✓} \\ {\mathbf{w}}_{1}\cdot {\mathbf{w}}_{1} & =\begin{bmatrix}\frac{3}{5} \\ \frac{4}{5}\end{bmatrix}\cdot \begin{bmatrix}\frac{3}{5} \\ \frac{4}{5}\end{bmatrix}=\frac{9}{25}+\frac{16}{25}=1 & {\color{green}✓} \\ {\mathbf{w}}_{2}\cdot {\mathbf{w}}_{2} & =\begin{bmatrix}\frac{4}{5} \\ -\frac{3}{5}\end{bmatrix}\cdot \begin{bmatrix}\frac{4}{5} \\ -\frac{3}{5}\end{bmatrix}=\frac{16}{25}+\frac{9}{25}=1 & {\color{green}✓}\end{aligned}
$$

So, $W$ is an orthonormal set.

Therefore, we conclude that the correct answer is "$U$ and $W$ only".

Answer $U=\left\{\begin{bmatrix}-\frac{3}{\sqrt{10}} \\ \frac{1}{\sqrt{10}}\end{bmatrix},\begin{bmatrix}\frac{1}{\sqrt{10}} \\ \frac{3}{\sqrt{10}}\end{bmatrix}\right\}$: true

Answer $V=\left\{\begin{bmatrix}2 \\ 3 \\ -1\end{bmatrix},\begin{bmatrix}3 \\ 1 \\ 9\end{bmatrix},\begin{bmatrix}28 \\ -21 \\ -7\end{bmatrix}\right\}$: false

Answer $W=\left\{\begin{bmatrix}\frac{3}{5} \\ \frac{4}{5}\end{bmatrix},\begin{bmatrix}\frac{4}{5} \\ -\frac{3}{5}\end{bmatrix}\right\}$: true

Question 17592186134283 — question.difficulty/moderate

Which of the following sets are orthonormal?

- $U=\left\{\begin{bmatrix}1 \\ 0\end{bmatrix},\begin{bmatrix}0 \\ 1\end{bmatrix}\right\}$
- $V=\left\{\begin{bmatrix}0 \\ 0\end{bmatrix},\begin{bmatrix}1 \\ 0\end{bmatrix}\right\}$
- $$
W=\left\{\begin{bmatrix}\frac{1}{\sqrt{2}} \\ -\frac{1}{\sqrt{2}}\end{bmatrix},\begin{bmatrix}0 \\ 1\end{bmatrix}\right\}
$$

Solution: Let's denote the vectors of the given sets as 
$\{{\mathbf{u}}_{1},{\mathbf{u}}_{2}\},$
$\{{\mathbf{v}}_{1},{\mathbf{v}}_{2}\},$ and 
$\{{\mathbf{w}}_{1},{\mathbf{w}}_{2}\}$, respectively. 

The sets $U,V,$ and $W$ are orthonormal if the following conditions on each set hold:

- $$
{\mathbf{u}}_{1}\cdot {\mathbf{u}}_{2}=0\hspace{1em}\text{and}\hspace{1em}\left\{\begin{aligned}{\mathbf{u}}_{1}\cdot {\mathbf{u}}_{1} &=1 \\ {\mathbf{u}}_{2}\cdot {\mathbf{u}}_{2} &=1.\end{aligned}\right.
$$

- $$
{\mathbf{v}}_{1}\cdot {\mathbf{v}}_{2}=0\hspace{1em}\text{and}\hspace{1em}\left\{\begin{aligned}{\mathbf{v}}_{1}\cdot {\mathbf{v}}_{1} &=1 \\ {\mathbf{v}}_{2}\cdot {\mathbf{v}}_{2} &=1.\end{aligned}\right.
$$

- $$
{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{2}=0\hspace{1em}\text{and}\hspace{1em}\left\{\begin{aligned}{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{1} &=1 \\ {\mathbf{w}}_{2}\cdot {\mathbf{w}}_{2} &=1.\end{aligned}\right.
$$

With that in mind, let's examine our sets in turn.

- For the set $U,$ we get the following:

$$
\begin{aligned}{\mathbf{u}}_{1}\cdot {\mathbf{u}}_{2} & =\begin{bmatrix}1 \\ 0\end{bmatrix}\cdot \begin{bmatrix}0 \\ 1\end{bmatrix}=0+0=0 & {\color{green}✓} \\ {\mathbf{u}}_{1}\cdot {\mathbf{u}}_{1} & =\begin{bmatrix}1 \\ 0\end{bmatrix}\cdot \begin{bmatrix}1 \\ 0\end{bmatrix}=1+0=1 & {\color{green}✓} \\ {\mathbf{u}}_{2}\cdot {\mathbf{u}}_{2} & =\begin{bmatrix}0 \\ 1\end{bmatrix}\cdot \begin{bmatrix}0 \\ 1\end{bmatrix}=0+1=1 & {\color{green}✓}\end{aligned}
$$

So, the set $U$ is orthonormal.

- For the set $V,$ notice that

$$
\begin{aligned}{\mathbf{v}}_{1}\cdot {\mathbf{v}}_{1} & =\begin{bmatrix}0 \\ 0\end{bmatrix}\cdot \begin{bmatrix}0 \\ 0\end{bmatrix}=0+0=0\ne 1 & {\color{red}\times }\end{aligned}
$$

So, $V$ is not an orthonormal set.

- For the set $W,$ notice that

$$
\begin{aligned}{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{2} & =\begin{bmatrix}\frac{1}{\sqrt{2}} \\ -\frac{1}{\sqrt{2}}\end{bmatrix}\cdot \begin{bmatrix}0 \\ 1\end{bmatrix}=0-\frac{1}{\sqrt{2}}=-\frac{1}{\sqrt{2}}\ne 0 & {\color{red}\times }\end{aligned}
$$

So, $W$ is not an orthonormal set.

Therefore, we conclude that the correct answer is "$U$ only".

Answer selection: $U$ only

Question 17592186272106 — question.difficulty/moderate

Which of the following sets are orthonormal?

Select all that apply.

Solution: Let's denote the vectors of the given sets as 
$\{{\mathbf{u}}_{1},{\mathbf{u}}_{2}\},$ 
$\{{\mathbf{v}}_{1},{\mathbf{v}}_{2}\},$ and 
$\{{\mathbf{w}}_{1},{\mathbf{w}}_{2}\},$ respectively. 

The sets $U,V,$ and $W$ are orthonormal if the following conditions on each set hold:

- $$
{\mathbf{u}}_{1}\cdot {\mathbf{u}}_{2}=0\hspace{1em}\text{and}\hspace{1em}\left\{\begin{aligned}{\mathbf{u}}_{1}\cdot {\mathbf{u}}_{1} &=1 \\ {\mathbf{u}}_{2}\cdot {\mathbf{u}}_{2} &=1.\end{aligned}\right.
$$

- $$
{\mathbf{v}}_{1}\cdot {\mathbf{u}}_{2}=0\hspace{1em}\text{and}\hspace{1em}\left\{\begin{aligned}{\mathbf{v}}_{1}\cdot {\mathbf{v}}_{1} &=1 \\ {\mathbf{v}}_{2}\cdot {\mathbf{v}}_{2} &=1.\end{aligned}\right.
$$

- $$
{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{2}=0\hspace{1em}\text{and}\hspace{1em}\left\{\begin{aligned}{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{1} &=1 \\ {\mathbf{w}}_{2}\cdot {\mathbf{w}}_{2} &=1.\end{aligned}\right.
$$

With that in mind, let's examine our sets in turn.

- For the set $U,$ we get the following:

$$
\begin{aligned}{\mathbf{u}}_{1}\cdot {\mathbf{u}}_{2} & =\begin{bmatrix}-\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}}\end{bmatrix}\cdot \begin{bmatrix}\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}}\end{bmatrix}=-\frac{1}{2}+\frac{1}{2}=0 & {\color{green}✓} \\ {\mathbf{u}}_{1}\cdot {\mathbf{u}}_{1} & =\begin{bmatrix}-\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}}\end{bmatrix}\cdot \begin{bmatrix}-\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}}\end{bmatrix}=\frac{1}{2}+\frac{1}{2}=1 & {\color{green}✓} \\ {\mathbf{u}}_{2}\cdot {\mathbf{u}}_{2} & =\begin{bmatrix}\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}}\end{bmatrix}\cdot \begin{bmatrix}\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}}\end{bmatrix}=\frac{1}{2}+\frac{1}{2}=1 & {\color{green}✓}\end{aligned}
$$

So, the set $U$ is orthonormal.

- For the set $V,$ we get the following:

$$
\begin{aligned}{\mathbf{v}}_{1}\cdot {\mathbf{v}}_{2} & =\begin{bmatrix}\frac{1}{3} \\ \frac{2}{3} \\ -\frac{2}{3}\end{bmatrix}\cdot \begin{bmatrix}\frac{2}{\sqrt{5}} \\ 0 \\ \frac{1}{\sqrt{5}}\end{bmatrix}=\frac{2}{3\sqrt{5}}+0-\frac{2}{3\sqrt{5}}=0 & {\color{green}✓} \\ {\mathbf{v}}_{1}\cdot {\mathbf{v}}_{1} & =\begin{bmatrix}\frac{1}{3} \\ \frac{2}{3} \\ -\frac{2}{3}\end{bmatrix}\cdot \begin{bmatrix}\frac{1}{3} \\ \frac{2}{3} \\ -\frac{2}{3}\end{bmatrix}=\frac{1}{9}+\frac{4}{9}+\frac{4}{9}=1 & {\color{green}✓} \\ {\mathbf{v}}_{2}\cdot {\mathbf{v}}_{2} & =\begin{bmatrix}\frac{2}{\sqrt{5}} \\ 0 \\ \frac{1}{\sqrt{5}}\end{bmatrix}\cdot \begin{bmatrix}\frac{2}{\sqrt{5}} \\ 0 \\ \frac{1}{\sqrt{5}}\end{bmatrix}=\frac{4}{5}+\frac{1}{5}=1 & {\color{green}✓}\end{aligned}
$$

So, $V$ is an orthonormal set.

- For the set $W,$ notice that

$$
\begin{aligned}{\mathbf{w}}_{1}\cdot {\mathbf{w}}_{2} & =\begin{bmatrix}-\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}}\end{bmatrix}\cdot \begin{bmatrix}\frac{1}{\sqrt{2}} \\ -\frac{1}{\sqrt{2}}\end{bmatrix}=-\frac{1}{2}-\frac{1}{2}=-1 & {\color{red}\times }\end{aligned}
$$

So, $W$ is not an orthonormal set.

Therefore, we conclude that the correct answer is "$U$ and $V$ only".

Answer $U=\left\{\begin{bmatrix}-\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}}\end{bmatrix},\begin{bmatrix}\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}}\end{bmatrix}\right\}$: true

Answer $V=\left\{\begin{bmatrix}\frac{1}{3} \\ \frac{2}{3} \\ -\frac{2}{3}\end{bmatrix},\begin{bmatrix}\frac{2}{\sqrt{5}} \\ 0 \\ \frac{1}{\sqrt{5}}\end{bmatrix}\right\}$: true

Answer $W=\left\{\begin{bmatrix}-\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}}\end{bmatrix},\begin{bmatrix}\frac{1}{\sqrt{2}} \\ -\frac{1}{\sqrt{2}}\end{bmatrix}\right\}$: false

### Extending a Set to Form an Orthogonal Basis (12 captured questions)

Question 17592186134220 — question.difficulty/hard

Consider the orthogonal set $U$ below. By adding a new vector $\mathbf{x}=[{x}_{1},\hspace{0.167em}{x}_{2},\hspace{0.167em}{x}_{3},\hspace{0.167em}{x}_{4}]^{T},$ extend the set so that it forms an orthogonal basis of ${\mathbb{R}}^{4}.$ What is the value of $\frac{{x}_{1}}{{x}_{4}}?$

$$
U=\left\{\begin{bmatrix}1 \\ 1 \\ 1 \\ 1\end{bmatrix},\begin{bmatrix}1 \\ -1 \\ 1 \\ -1\end{bmatrix},\begin{bmatrix}1 \\ 2 \\ -1 \\ -2\end{bmatrix}\right\}
$$

Solution: Let's denote the vectors of $U$ as ${\mathbf{u}}_{1},\hspace{0.167em}{\mathbf{u}}_{2},\hspace{0.167em}{\mathbf{u}}_{3}.$ To extend the given set to an orthogonal basis of ${\mathbb{R}}^{4}$, we need to find a fourth vector $\mathbf{x}$ such that

$$
\left\{\begin{aligned}{\mathbf{u}}_{1}\cdot \mathbf{x} &=0 \\ {\mathbf{u}}_{2}\cdot \mathbf{x} &=0 \\ {\mathbf{u}}_{3}\cdot \mathbf{x} &=0\end{aligned}\right.\hspace{2em}⟹\hspace{2em}\left\{\begin{aligned}{x}_{1}+{x}_{2}+{x}_{3}+{x}_{4} &=0 \\ {x}_{1}-{x}_{2}+{x}_{3}-{x}_{4} &=0 \\ {x}_{1}+2{x}_{2}-{x}_{3}-2{x}_{4} &=0.\end{aligned}\right.
$$

Now, we consider the augmented matrix $M$ of the system above and reduce it to row echelon form, as follows:

$$
\begin{aligned}M & =\left[\begin{array}{cccc|c}1 & 1 & 1 & 1 & 0 \\ 1 & -1 & 1 & -1 & 0 \\ 1 & 2 & -1 & -2 & 0\end{array}\right] &  & \begin{aligned}{R}_{2}:={R}_{2}-{R}_{1} \\ {R}_{3}:={R}_{3}-{R}_{1}\end{aligned} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & 1 & 1 & 0 \\ 0 & -2 & 0 & -2 & 0 \\ 0 & 1 & -2 & -3 & 0\end{array}\right] &  & \begin{aligned}{R}_{3}:={R}_{3}+\frac{1}{2}{R}_{2}\end{aligned} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & 1 & 1 & 0 \\ 0 & -2 & 0 & -2 & 0 \\ 0 & 0 & -2 & -4 & 0\end{array}\right]\end{aligned}
$$

In the reduced matrix above, there are three pivot columns ($1$st, $2$nd and $3$rd). Thus, ${x}_{4}$ is a free variable. From the second and third equations, we get ${x}_{2}=-{x}_{4}$ and ${x}_{3}=-2{x}_{4}$, respectively. Substituting this into the first equation, we obtain

$$
\begin{aligned}{x}_{1}+(-{x}_{4})+(-2{x}_{4})+{x}_{4}=0\,⟹\,{x}_{1}=2{x}_{4}.\end{aligned}
$$

So, the general solution is

$$
\begin{bmatrix}2{x}_{4} \\ -{x}_{4} \\ -2{x}_{4} \\ {x}_{4}\end{bmatrix},\hspace{2em}{x}_{4}\in \mathbb{R}.
$$

Setting ${x}_{4}=1,$ we obtain the vector 

$$
\mathbf{x}=\begin{bmatrix}2 \\ -1 \\ -2 \\ 1\end{bmatrix}.
$$

Therefore, an orthogonal basis of ${\mathbb{R}}^{4}$ is

$$
\left\{\begin{bmatrix}1 \\ 1 \\ 1 \\ 1\end{bmatrix},\begin{bmatrix}1 \\ -1 \\ 1 \\ -1\end{bmatrix},\begin{bmatrix}1 \\ 2 \\ -1 \\ -2\end{bmatrix},\begin{bmatrix}2 \\ -1 \\ -2 \\ 1\end{bmatrix}\right\}.
$$

Finally, $\frac{{x}_{1}}{{x}_{4}}=\frac{2}{1}=2.$

Answer selection: 2

Question 17592186134280 — question.difficulty/moderate

Consider the orthogonal set $U$ below. By adding a new vector $\mathbf{x}=[{x}_{1},\hspace{0.167em}{x}_{2},\hspace{0.167em}{x}_{3}]^{T},$ extend the set so that it forms an orthogonal basis of ${\mathbb{R}}^{3}.$ What is the value of $\frac{{x}_{1}}{{x}_{2}}?$

$$
U=\left\{\begin{bmatrix}1 \\ 2 \\ 1\end{bmatrix},\begin{bmatrix}0 \\ -3 \\ 6\end{bmatrix}\right\}
$$

Solution: Let's denote the vectors of $U$ as ${\mathbf{u}}_{1},\hspace{0.167em}{\mathbf{u}}_{2}.$ To extend the given set to an orthogonal basis of ${\mathbb{R}}^{3}$, we need to find a third vector $\mathbf{x}=\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3}\end{bmatrix}$ such that

$$
\left\{\begin{aligned}{\mathbf{u}}_{1}\cdot \mathbf{x} &=0 \\ {\mathbf{u}}_{2}\cdot \mathbf{x} &=0\end{aligned}\right.\hspace{2em}⟹\hspace{2em}\left\{\begin{aligned}{x}_{1}+2{x}_{2}+{x}_{3} &=0 \\ -3{x}_{2}+6{x}_{3} &=0.\end{aligned}\right.
$$

Now, we consider the augmented matrix $M$ of the system above, which is already in row echelon form:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & 2 & 1 & 0 \\ 0 & -3 & 6 & 0\end{array}\right]\end{aligned}
$$

In the reduced matrix above, there are two pivot columns ($1$st and $2$nd). Thus, ${x}_{3}$ is a free variable. From the second equation, we get ${x}_{2}=2{x}_{3}.$ Substituting this into the first equation, we obtain

$$
\begin{aligned}{x}_{1}+2(2{x}_{3})+{x}_{3}=0\,⟹\,{x}_{1}=-5{x}_{3}.\end{aligned}
$$

So, the general solution is

$$
\begin{bmatrix}-5{x}_{3} \\ 2{x}_{3} \\ {x}_{3}\end{bmatrix},\hspace{2em}{x}_{3}\in \mathbb{R}.
$$

Setting ${x}_{3}=1,$ we obtain the vector 

$$
\mathbf{x}=\begin{bmatrix}-5 \\ 2 \\ 1\end{bmatrix}.
$$

Therefore, an orthogonal basis of ${\mathbb{R}}^{3}$ is

$$
\left\{\begin{bmatrix}1 \\ 2 \\ 1\end{bmatrix},\begin{bmatrix}0 \\ -3 \\ 6\end{bmatrix},\begin{bmatrix}-5 \\ 2 \\ 1\end{bmatrix}\right\}.
$$

Finally, $$
\displaystyle \frac{{x}_{1}}{{x}_{2}}=\frac{-5}{2}=-\frac{5}{2}.
$$

Answer selection: -\frac{5}{2}

Question 17592186272108 — question.difficulty/moderate

Consider the orthogonal set $U$ below. By adding a new vector $\mathbf{x}=[{x}_{1},\hspace{0.167em}{x}_{2},\hspace{0.167em}{x}_{3}]^{T},$ extend the set so that it forms an orthogonal basis of ${\mathbb{R}}^{3}.$ What is the value of $\frac{{x}_{1}}{{x}_{2}}?$

$$
U=\left\{\begin{bmatrix}1 \\ -3 \\ 2\end{bmatrix},\begin{bmatrix}2 \\ 2 \\ 2\end{bmatrix}\right\}
$$

Solution: Let's denote the vectors of $U$ as ${\mathbf{u}}_{1},\hspace{0.167em}{\mathbf{u}}_{2}.$ To extend the given set to an orthogonal basis of ${\mathbb{R}}^{3}$, we need to find a third vector $\mathbf{x}=\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3}\end{bmatrix}$ such that

$$
\left\{\begin{aligned}{\mathbf{u}}_{1}\cdot \mathbf{x} &=0 \\ {\mathbf{u}}_{2}\cdot \mathbf{x} &=0\end{aligned}\right.\hspace{2em}⟹\hspace{2em}\left\{\begin{aligned}{x}_{1}-3{x}_{2}+2{x}_{3} &=0 \\ 2{x}_{1}+2{x}_{2}+2{x}_{3} &=0.\end{aligned}\right.
$$

Now, we consider the augmented matrix $M$ of the system above and reduce it to its row echelon form, as follows:

$$
\begin{aligned}M & =\left[\begin{array}{ccc|c}1 & -3 & 2 & 0 \\ 2 & 2 & 2 & 0\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{ccc|c}1 & -3 & 2 & 0 \\ 0 & 8 & -2 & 0\end{array}\right]\end{aligned}
$$

In the reduced matrix above, there are two pivot columns ($1$st and $2$nd). Thus, ${x}_{3}$ is a free variable. From the second equation, we get ${x}_{2}=\frac{1}{4}{x}_{3}.$ Substituting this into the first equation, we obtain

$$
\begin{aligned}{x}_{1}-3\left(\frac{1}{4}{x}_{3}\right)+2{x}_{3}=0\,⟹\,{x}_{1}=-\frac{5}{4}{x}_{3}.\end{aligned}
$$

So, the general solution is

$$
\begin{bmatrix}-\frac{5}{4}{x}_{3} \\ \frac{1}{4}{x}_{3} \\ {x}_{3}\end{bmatrix},\hspace{2em}{x}_{3}\in \mathbb{R}.
$$

Setting ${x}_{3}=4,$ we obtain the vector 

$$
\mathbf{x}=\begin{bmatrix}-5 \\ 1 \\ 4\end{bmatrix}.
$$

Therefore, an orthogonal basis of ${\mathbb{R}}^{3}$ is

$$
\left\{\begin{bmatrix}1 \\ -3 \\ 2\end{bmatrix},\begin{bmatrix}2 \\ 2 \\ 2\end{bmatrix},\begin{bmatrix}-5 \\ 1 \\ 4\end{bmatrix}\right\}.
$$

Finally, $$
\displaystyle \frac{{x}_{1}}{{x}_{2}}=\frac{-5}{1}=-5.
$$

Answer selection: -5

### Extending a Set to Form an Orthonormal Basis (11 captured questions)

Question 17592186134221 — question.difficulty/hard

Consider the **orthonormal** set $U$ below. By adding a new vector $\mathbf{x}=[{x}_{1},\hspace{0.167em}{x}_{2},\hspace{0.167em}{x}_{3}]^{T}$, extend the set so that it forms an **orthonormal** basis of ${\mathbb{R}}^{3}$. What is the value of $|{x}_{1}|+|{x}_{2}|+|{x}_{3}|?$
$$
U=\left\{\begin{bmatrix}\frac{1}{\sqrt{5}} \\ 0 \\ -\frac{2}{\sqrt{5}}\end{bmatrix},\begin{bmatrix}\frac{2}{3} \\ \frac{2}{3} \\ \frac{1}{3}\end{bmatrix}\right\}
$$

Solution: To extend the orthonormal set, find a unit vector $\mathbf x$ orthogonal to both given vectors. The equations are

$$
\frac{x_1-2x_3}{\sqrt5}=0,\qquad \frac{2x_1+2x_2+x_3}{3}=0.
$$

Hence $x_1=2x_3$ and $x_2=-\frac52x_3$, so $\mathbf x=t\begin{bmatrix}4\\-5\\2\end{bmatrix}$. Its norm is $3\sqrt5|t|$, so the unit-vector condition gives $|t|=\frac1{3\sqrt5}$. Therefore,

$$
|x_1|+|x_2|+|x_3|=\frac{4+5+2}{3\sqrt5}=\frac{11}{3\sqrt5}.
$$

Answer selection: \frac{11}{3\sqrt{5}}

Question 17592186134518 — question.difficulty/moderate

Consider the **orthonormal** set $U$ below. By adding a new vector $\mathbf{x}=[{x}_{1},\hspace{0.167em}{x}_{2}]^{T},$ extend the set so that it forms an **orthonormal** basis of ${\mathbb{R}}^{2}.$ What is the value of $|{x}_{1}|+|{x}_{2}|?$

$$
U=\left\{\begin{bmatrix}\frac{3}{\sqrt{13}} \\ -\frac{2}{\sqrt{13}}\end{bmatrix}\right\}
$$

Solution: Let's denote the vector of $U$ as ${\mathbf{u}}_{1}.$ To extend the given set to an orthonormal basis of ${\mathbb{R}}^{2}$, we need to find a second vector $\mathbf{x}$ such that $‖\mathbf{x}‖=1,$ and

$$
{\mathbf{u}}_{1}\cdot \mathbf{x}=0\hspace{2em}⟹\hspace{2em}\frac{3}{\sqrt{13}}{x}_{1}-\frac{2}{\sqrt{13}}{x}_{2}=0.
$$

From the above equation, we get ${x}_{1}=\frac{2}{3}{x}_{2}.$

So, the general solution is

$$
\begin{bmatrix}\frac{2}{3}{x}_{2} \\ {x}_{2}\end{bmatrix},\hspace{2em}{x}_{2}\in \mathbb{R}.
$$

Setting ${x}_{2}=3,$ we obtain the vector 
$$
\mathbf{x}=\begin{bmatrix}2 \\ 3\end{bmatrix}.
$$ 

Now, we need to normalize $\mathbf{x}.$ Notice that $‖\mathbf{x}‖=\sqrt{{2}^{2}+{3}^{2}}=\sqrt{13}.$ So, we normalize $\mathbf{x}$ as follows:

$$
\frac{\mathbf{x}}{‖\mathbf{x}‖}=\begin{bmatrix}\frac{2}{\sqrt{13}} \\ \frac{3}{\sqrt{13}}\end{bmatrix}.
$$

Therefore, an orthonormal basis of ${\mathbb{R}}^{2}$ is

$$
\left\{\begin{bmatrix}\frac{3}{\sqrt{13}} \\ -\frac{2}{\sqrt{13}}\end{bmatrix},\begin{bmatrix}\frac{2}{\sqrt{13}} \\ \frac{3}{\sqrt{13}}\end{bmatrix}\right\}.
$$

Finally, $$
\displaystyle |{x}_{1}|+|{x}_{2}|=|\frac{2}{\sqrt{13}}|+|\frac{3}{\sqrt{13}}|=\frac{5}{\sqrt{13}}.
$$

Answer selection: \frac{5}{\sqrt{13}}

Question 17592186272109 — question.difficulty/moderate

Consider the **orthonormal** set $U$ below. By adding a new vector $\mathbf{x}=[{x}_{1},\hspace{0.167em}{x}_{2}]^{T},$ extend the set so that it forms an **orthonormal** basis of ${\mathbb{R}}^{2}.$ What is the value of $|{x}_{1}|+|{x}_{2}|?$

$$
U=\left\{\begin{bmatrix}\frac{1}{\sqrt{10}} \\ -\frac{3}{\sqrt{10}}\end{bmatrix}\right\}
$$

Solution: Let's denote the vector of $U$ as ${\mathbf{u}}_{1}.$ To extend the given set to an orthonormal basis of ${\mathbb{R}}^{2}$, we need to find a second vector $\mathbf{x}$ such that $‖\mathbf{x}‖=1,$ and

$$
{\mathbf{u}}_{1}\cdot \mathbf{x}=0\hspace{2em}⟹\hspace{2em}\frac{1}{\sqrt{10}}{x}_{1}-\frac{3}{\sqrt{10}}{x}_{2}=0.
$$

From the above equation, we get ${x}_{1}=3{x}_{2}.$

So, the general solution is

$$
\begin{bmatrix}3{x}_{2} \\ {x}_{2}\end{bmatrix},\hspace{2em}{x}_{2}\in \mathbb{R}.
$$

Setting ${x}_{2}=1,$ we obtain the vector 
$$
\mathbf{x}=\begin{bmatrix}3 \\ 1\end{bmatrix}.
$$ 

Now, we need to normalize $\mathbf{x}.$ Notice that $‖\mathbf{x}‖=\sqrt{{3}^{2}+{1}^{2}}=\sqrt{10}.$ So, we normalize $\mathbf{x}$ as follows:

$$
\frac{\mathbf{x}}{‖\mathbf{x}‖}=\begin{bmatrix}\frac{3}{\sqrt{10}} \\ \frac{1}{\sqrt{10}}\end{bmatrix}.
$$

Therefore, an orthonormal basis of ${\mathbb{R}}^{2}$ is

$$
\left\{\begin{bmatrix}\frac{1}{\sqrt{10}} \\ -\frac{3}{\sqrt{10}}\end{bmatrix},\begin{bmatrix}\frac{3}{\sqrt{10}} \\ \frac{1}{\sqrt{10}}\end{bmatrix}\right\}.
$$

Finally, $$
\displaystyle |{x}_{1}|+|{x}_{2}|=|\frac{3}{\sqrt{10}}|+|\frac{1}{\sqrt{10}}|=\frac{4}{\sqrt{10}}.
$$

Answer selection: \frac{4}{\sqrt{10}}
