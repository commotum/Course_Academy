# 17592186050173 Three-Dimensional Vectors in Component Form

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186101949 — Introduction

We can use Cartesian coordinates to define vectors in three-dimensional space. For example, consider a point $A(2,2,3)$, and define the origin as the point $O(0,0,0)$. The position vector of $A$ is

$$
\overrightarrow{OA} = \mathbf{a}
$$

Let's also define three special unit vectors $\mathbf{i}$, $\mathbf{j}$, and $\mathbf{k}$, where

$$
|\,\mathbf{i}\,| = |\,\mathbf{j}\,| = |\,\mathbf{k}\,| = 1,
$$

as follows:

- $\mathbf{i}$ is a horizontal unit vector that points "outwards" along the positive direction of the $x$-axis,
- $\mathbf{j}$ is a horizontal unit vector that points to the right along the positive direction of the $y$-axis, and
- $\mathbf{k}$ is a vertical unit vector that points upwards along the positive direction of the $z$-axis.

All of these vectors are illustrated in the diagram shown below.

![](images/ee/eee8990fb7bd078cd1788644442f90e4e37f5a232992a5069d53315d18463a9f.png)

Now, we can uniquely describe our position vector using $\mathbf{i}, \mathbf{j}, \mathbf{k}$ as

$$
\begin{aligned}
a &= OA^(→) = 2i + 2j + 3k
\end{aligned}
$$



### example 17592186100678 — Expressing a Position Vector in Component Form Given Its Graph

Given the picture below, find the position vector of the point $A(1,-2,2)$ in terms of $\mathbf{i}$, $\mathbf{j}$, and $\mathbf{k}$.

![](images/59/59c4c67c4ae24a83375e032704b467150e6a2d2cfc1cd51e3848c993847f74ca.png)

Remember that in general, if a point $A$ has coordinates $(a_x,a_y,a_z)$, then its position vector is given by

$$
\overrightarrow{OA} = \mathbf{a} = a_x\mathbf{i}+a_y\mathbf{j} + a_z\mathbf{k}
$$

Here, the point $A$ has the coordinates $(1,-2,2)$, so its position vector is given by

$$
\begin{aligned}
OA^(→) &= i - 2j + 2k
\end{aligned}
$$

### tutorial 17592186101950 — Alternative Notation and the Standard Basis

In general, the position vector of a point $A(a_x,a_y,a_z)$ is the vector
$$
\begin{aligned}
\overrightarrow{OA} &=\mathbf{a} \\
&=\langle a_x, a_y, a_z \rangle \\
&={\left[ \begin{array}{c}{a}_{x} \\ {a}_{y} \\ {a}_{z}\end{array} \right]} \\
&=a_x\,\mathbf{i}+a_y\,\mathbf{j}+a_z\,\mathbf{k}.
\end{aligned}
$$

The unit vectors $\mathbf{i}$, $\mathbf{j}$, and $\mathbf{k}$ are usually called the **standard basis** of the three-dimensional space.

Lastly, note that a vector is defined by its components uniquely. In other words, given

$$
\mathbf{a}=\langle a_x,a_y,a_z \rangle
$$

and

$$
\mathbf{b}=\langle b_x,b_y,b_z \rangle
$$

we have

$$
\mathbf{a} = \mathbf{b}
	\quad\Longleftrightarrow\quad
	\left\{
	{\begin{array}{l}{a}_{x} = {b}_{x} \\ {a}_{y} = {b}_{y} \\ {a}_{z} = {b}_{z} .\end{array}}
	\right.
$$



### example 17592186100677 — Converting Between Alternative Notations

Write the position vector of $A(-1,-2,3)$ using the following notations.

1. The angle bracket notation.
2. The column vector notation.
3. In terms of $\mathbf{i}$, $\mathbf{j}$, and $\mathbf{k}$.

Remember that in general, if a point $A$ has coordinates $(a_x,a_y,a_z)$, then its position vector is given by

$$
\overrightarrow{OA}=\mathbf{a}
		=\langle a_x, a_y, a_z \rangle = 
		{\left[ \begin{array}{c}{a}_{x} \\ {a}_{y} \\ {a}_{z}\end{array} \right]} = 
		a_x\,\mathbf{i}+a_y\,\mathbf{j}+a_z\,\mathbf{k}.
$$

Here, the point $A$ has the coordinates $(-1,-2,3)$, so its position vector is given by

$$
\overrightarrow{OA}=\mathbf{a}
		=\langle -1, -2, 3 \rangle = 
		{\left[ \begin{array}{c}- 1 \\ - 2 \\ 3\end{array} \right]} = 
		-\mathbf{i}-2\mathbf{j}+3\mathbf{k}.
$$

### example 17592186100680 — Expressing a Position Vector in Component Form Given Its Endpoints

Let $A(-1,4, -5)$ and $B(2,3,5)$. Find $\overrightarrow{AB}$ in column vector notation.

We have

$$
OA^(→) = a =-i + 4j - 5k,; OB^(→) = b = 2i + 3j + 5k
$$

Now, we can express $\overrightarrow{AB}$ as the difference of position vectors, as follows:

$$
\begin{aligned}
AB^(→) &= b - a \\
&= (2i + 3j + 5k) - (-i + 4j - 5k) \\
&= 3i - j + 10k \\
&= \begin{bmatrix}3 \\ -1 \\ 10\end{bmatrix}
\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Expressing a Position Vector in Component Form Given Its Graph (7 captured questions)

Question 17592186101287 — None

![](images/69/6980aeb19ad64497366085c6cd092eb28934cd40a1ab5c93d90a18ec284355b2.png)

Given the picture above, find the position vector of the point $A(3,-1,-2)$ in terms of $i$, $j$, and $k$.

Solution: 

Question 17592186101290 — None

![](images/e9/e9cce43fa6175bdc1460c27be05c63ef5eda7cf3bd4a0c66ece5485056b40638.png)

Given the picture above, find the position vector of the point $B(2,-1, 2)$ in terms of $i$, $j$, and $k$.

Solution: 

Question 17592186233602 — question.difficulty/easy

![](images/80/80749f47491522bb42ccca5bce0176b69ca03fa5ac6c33df37350392936857c3.png)

Given the picture above, find the position vector of the point $Q(1,1,2)$ in terms of $i$, $j$, and $k.$

Solution: Remember that in general, if a point $Q$ has coordinates $({q}_{x},{q}_{y},{q}_{z}),$ then its position vector is given by

$$
\overset{\to }{OQ}=q={q}_{x}i+{q}_{y}j+{q}_{z}k.
$$

Here, the point $Q$ has the coordinates $(1,1,2),$ so its position vector is given by

$$
\overset{\to }{OQ}=q=i+j+2k.
$$

### Converting Between Alternative Notations (4 captured questions)

Question 17592186101273 — None

Which of the following represents the vector $a =-4i + k$ in angle bracket notation?

Solution: 

Question 17592186101288 — None

Which of the following represents the position vector of $A(-3, 5, 0)$ in column vector notation?

Solution: 

Question 17592186233827 — question.difficulty/moderate

Write the vector $b=-7i+2j+5k$ in angle bracket notation.

$b=⟨$
{{field-1}},
{{field-2}},
{{field-3}}$⟩$

Solution: Remember that in general, if a point $B$ has coordinates $({b}_{x},{b}_{y},{b}_{z}),$ then its position vector is given by

$$
\overset{\to }{OB}=b=⟨{b}_{x},{b}_{y},{b}_{z}⟩=\begin{bmatrix}{b}_{x} \\ {b}_{y} \\ {b}_{z}\end{bmatrix}={b}_{x}\,i+{b}_{y}\,j+{b}_{z}\,k.
$$

Therefore, we have 

$$
\begin{aligned}b & =-7i+2j+5k \\  & =-7\cdot i+2\cdot j+5\cdot k \\  & =⟨-7,2,5⟩.\end{aligned}
$$

Answer field-1: -7

Answer field-2: 2

Answer field-3: 5

### Expressing a Position Vector in Component Form Given Its Endpoints (4 captured questions)

Question 17592186101274 — None

Let $A(3,-1, 2)$ and $B(1, 1,-3)$. Find $AB^(→)$ in column vector notation.

Solution: 

Question 17592186101289 — None

Let $P(5, 3,-1)$ and $Q(0, 0, 1)$. Find $PQ^(→)$ in terms of $i$, $j$, and $k$.

Solution: 

Question 17592186234387 — question.difficulty/moderate

Let $P(1,0,-2)$ and $Q(3,-4,2).$ Find $\overset{\to }{PQ}$ in terms of $i,$ $j$ and $k.$

Solution: We have 

$$
\begin{aligned} & \overset{\to }{OP}=p=i-2k, \\  & \overset{\to }{OQ}=q=3i-4j+2k.\end{aligned}
$$

Now, we can express $\overset{\to }{PQ}$ as the difference of position vectors, as follows:

$$
\begin{aligned}\overset{\to }{PQ} & =q-p \\  & =(3i-4j+2k)-(i-2k) \\  & =2i-4j+4k\end{aligned}
$$
