# 17592186048816 Two-Dimensional Vectors Expressed in Component Form

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186101946 — Introduction

We can use Cartesian coordinates to define vectors in the plane. For example, consider the diagram shown below.

![](images/b7/b7fad622207f396145e930cf74f7905104bf12fa394a9f2f4f5d7ce761cc8e36.png)

The point $A$ has coordinates $(2,3).$ We also have the point $O(0,0)$ that is called the **origin**. 

The vector $\overrightarrow{OA}=\mathbf{a}$ is called the **position vector** of $A.$ A position vector always has its tail at the origin. 

Now let's define two special unit vectors $\mathbf{i}$ and $\mathbf{j},$ where $|\, \mathbf{i} \,| = |\, \mathbf{j} \,| = 1,$ as follows:

- $\mathbf{i}$ is a horizontal unit vector that points to the right along the positive direction of the $x$-axis, while

- $\mathbf{j}$ is a vertical unit vector that points upwards along the positive direction of the $y$-axis.

These vectors are shown in the picture below. 

![](images/cb/cb5694945b6f76f14a4e66b854f5daa56f3e607bd5b24c4f361ed844dbf8ff7e.png)

We have 

$$
\begin{aligned} & \overset{\to }{OX}=2i, \\  & \overset{\to }{XA}=\overset{\to }{OY}=3j.\end{aligned}
$$

Now, from $\triangle OXA,$ we have

$$
\begin{aligned}\overset{\to }{OA} & =\overset{\to }{OX}+\overset{\to }{XA} \\  & =2i+3j.\end{aligned}
$$

So, the point $A$ with coordinates $(2,3)$ has a position vector

$$
\begin{aligned}\overset{\to }{OA} & =2i+3j.\end{aligned}
$$

In general, if a point $A$ has coordinates $(a_x,a_y),$ then its position vector is given by

$$
\overrightarrow{OA} = \mathbf{a} = a_x\mathbf{i}+a_y\mathbf{j}.
$$



### example 17592186100672 — Expressing a Position Vector in Component Form

Find the position vector of $A(-1,2)$ in terms of $\mathbf{i}$ and $\mathbf{j}$.

Our vector is shown in the diagram below.

![](images/26/269326f4375dfad6d05e4468f4831012bde4a57bc85fbdfc7082cc466d3522dd.png)

Remember that in general, if a point $A$ has coordinates $(a_x,a_y)$, then its position vector is given by

$$
\overrightarrow{OA} = a_x\mathbf{i}+a_y\mathbf{j}
$$

Here, the point $A$ has coordinates $(-1,2)$, so its position vector is given by

$$
\begin{aligned}
OA^(→) &= (-1) \cdot i + 2 \cdot j \\
&=-i + 2j
\end{aligned}
$$

### tutorial 17592186101947 — Alternatives to i,j Notation

The $\mathbf{i,j}$ notation can sometimes be cumbersome. An alternative is to use **angle bracket** notation. For example, using angle bracket notation, the vector $2\mathbf{i}+3\mathbf{j}$ can be expressed as

$$
2\mathbf{i}+3\mathbf{j}=\langle 2,3 \rangle.
$$

Note that, using angle bracket notation, the special unit vectors can be expressed as

$$
\begin{aligned}i &=1i+0j=⟨1,0⟩, \\ j &=0i+1j=⟨0,1⟩.\end{aligned}
$$

We can also use **column vector** notation, which is similar to angle bracket notation but expresses the vector as a column rather than a row. For example, using column vector notation, the vector $2\mathbf{i}+3\mathbf{j}$ can be expressed as

$$
2\mathbf{i}+3\mathbf{j}={\left[ \begin{array}{c}2 \\ 3\end{array} \right]}.
$$

Using column vector notation, the special unit vectors can be expressed as $\displaystyle \mathbf{i} = {\left[ \begin{array}{c}1 \\ 0\end{array} \right]}$ and $\displaystyle \mathbf{j} = {\left[ \begin{array}{c}0 \\ 1\end{array} \right]}.$

**Note:** Sometimes, the round bracket notation $(\ldots)$ is used to denote vectors. However, we will avoid using that notation here, because it also looks like the coordinates of a point. A point and its position vector are two separate objects!



### example 17592186100674 — Expressing a Position Vector in Angle Bracket Notation

The points $A, B, C$, and $O$ are shown in the picture below. Find the corresponding position vectors, using angle bracket notation.

![](images/92/92eb1531e0e5e308edb85da62149a220166c8bd37fc0f66d600e9a9599731195.png)

For a point with coordinates $(a_x, a_y)$, the position vector is

$$
\left< a_x, a_y \right>
$$

- The point $A$ has coordinates $(-1,2)$, so the position vector is
$\overrightarrow{OA} = \langle -1,2 \rangle$.
- The point $B$ has coordinates $(3, 1.5)$, so the position vector is
$\overrightarrow{OB} = \langle 3, 1.5 \rangle$.
- The point $C$ has coordinates $(1,-2)$, so the position vector is
$\overrightarrow{OC} = \langle 1,-2 \rangle$.
- The point $O$ has coordinates $(0,0)$, so the position vector is
$$
\displaystyle \overrightarrow{OO} = \langle 0,0 \rangle = \mathbf{0}.
$$

### example 17592186100675 — Expressing a Vector in Component Form

Let $A(-2,1)$ and $B(2,3)$. Find $\overrightarrow{AB}$ in terms of $\mathbf{i}$ and $\mathbf{j}$.

Our vector is shown in the diagram below.

![](images/76/76c98067c9780e9c903dda8657b67a2db473ecd8ef24e53e2262ba2f46a4293a.png)

We have

$$
OA^(→) = a =-2i + j,; OB^(→) = b = 2i + 3j
$$

Now, from $\triangle OAB$, we have

$$
\begin{aligned}
AB^(→) &= AO^(→) + OB^(→) \\
&=-OA^(→) + OB^(→) \\
&= b - a \\
&= (2i + 3j) - (-2i + j) \\
&= 4i + 2j
\end{aligned}
$$

### tutorial 17592186101948 — Expressing Vectors as Differences of Position Vectors

If $A$ and $B$ are points in the Cartesian plane with position vectors $\mathbf{a}$ and $\mathbf{b}$ respectively, then

$$
\overrightarrow{AB} = \mathbf{b}-\mathbf{a}.
$$

To understand why the equation above is true, remember that $\overrightarrow{OA} = \mathbf{a}$ and $\overrightarrow{OB} = \mathbf{b}.$ Then, we have

$$
\begin{aligned}\overset{\to }{AB} & =\overset{\to }{AO}+\overset{\to }{OB} \\  & =-\overset{\to }{OA}+\overset{\to }{OB} \\  & =-a+b \\  & =b-a.\end{aligned}
$$

For example, given $A(5,13)$ and $B(-2,-35)$, we have

$$
\begin{aligned} & \overset{\to }{OA}=a=5i+13j, \\  & \overset{\to }{OB}=b=-2i-35j.\end{aligned}
$$

Now, using the formula, we obtain

$$
\begin{aligned}\overset{\to }{AB} & =b-a \\  & =(-2i-35j)-(5i+13j) \\  & =-7i-48j.\end{aligned}
$$



## Representative practice (first three per skill; full bank in practice.json)

### Expressing a Position Vector in Component Form (4 captured questions)

Question 17592186101253 — None

![](images/ae/ae198a23a6f97db16c791fe685bda99dff489b50dc87552afcbe5bbbb458a8c6.png)

Given the diagram above, find the position vector of $A$ in terms of $i$ and $j$.

Solution: 

Question 17592186101261 — None

Find the position vector of $A(0,-4)$ in terms of $i$ and $j$.

Solution: 

Question 17592186573291 — question.difficulty/easy

Find the position vector of $R(-4,5)$ in terms of $i$ and $j.$

The position vector of $R$ is
{{field-1}}
$i\,\,+$
{{field-2}}
$j.$

Solution: Our vector is shown in the diagram below.

![](images/e1/e132f8e20ffb38c70ef435a560a584b25a6509486cc148636d873a9e0e94ea52.png)

Remember that in general, if a point $R$ has coordinates $({r}_{x},{r}_{y}),$ then its position vector is given by

$$
\overset{\to }{OR}={r}_{x}i+{r}_{y}\,j.
$$

Here, the point $R$ has coordinates $(-4,5),$ so its position vector is given by

$$
\begin{aligned}\overset{\to }{OR} & =(-4)\cdot i+5\cdot j \\  & =-4\,i+5\,j.\end{aligned}
$$

Answer field-1: -4

Answer field-2: 5

### Expressing a Position Vector in Angle Bracket Notation (5 captured questions)

Question 17592186101262 — None

![](images/12/12dc0a80a64f0d9ed9ea319a14435eef1597484bcfc2af59d9cf7c760bbd095c.png)

The points $A, B$ and $C$ are shown in the picture above. Which of the following statements are true?

1. $OA^(→) = ⟨0, 1⟩$
2. $OB^(→) = ⟨3, 2⟩$
3. $OC^(→) = ⟨2, 1⟩$

Solution: 

Question 17592186101263 — None

![](images/d0/d01c92b786d5612faa3c2e0e128b517b740744e5b636831a13a192ee1e3f9f4a.png)

The point $P$ is shown in the picture above. Find the coordinates of the corresponding position vector.

Solution: 

Question 17592186573269 — question.difficulty/easy

![](images/a8/a86e5e973e15230943beaa3f8afdeed139690ba4e5cf3fed4c35895e5f4bd2d4.png)

The point $W$ is shown in the picture above. Find the coordinates of the corresponding position vector.

Solution: For a point with coordinates $({a}_{x},{a}_{y}),$ the position vector is $⟨{a}_{x},{a}_{y}⟩.$

The point $W$ has coordinates $(1.5,-2.5),$ so the position vector is

$$
\overset{\to }{OW}=⟨1.5,-2.5⟩.
$$

Answer selection: \overset{\to }{OW}=⟨1.5,-2.5⟩

### Expressing a Vector in Component Form (7 captured questions)

Question 17592186101254 — None

![](images/cf/cfbe4db887133923440cb848161424aa385c0e60c86376e371455cef7084e7ed.png)

Let $A(1, 3)$ and $B(4,-1)$. Find $AB^(→)$ in terms of $i$ and $j$.

Solution: 

Question 17592186101265 — None

Let $A(3, 3)$ and $B(0,-3)$. Find $BA^(→)$ in terms of $i$ and $j$.

Solution: 

Question 17592186234391 — question.difficulty/moderate

Let $A(-2,1)$ and $B(1,-5).$ Find $\overset{\to }{AB}$ in terms of $i$ and $j.$

Solution: Our vector is shown in the diagram below.

![](images/9b/9b2d2c2a56e095f5bed1d5b128196cf2e959e6a75559e08c9956be5fbc507dfd.png)

We have 

$$
\begin{aligned} & \overset{\to }{OA}=a=-2i+j, \\  & \overset{\to }{OB}=b=i-5j.\end{aligned}
$$

Now, from $△OAB,$ we have

$$
\begin{aligned}\overset{\to }{AB} & =\overset{\to }{AO}+\overset{\to }{OB} \\  & =-\overset{\to }{OA}+\overset{\to }{OB} \\  & =b-a \\  & =(i-5j)-(-2i+j) \\  & =3i-6j.\end{aligned}
$$
