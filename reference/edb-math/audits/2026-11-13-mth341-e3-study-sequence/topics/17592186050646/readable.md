# 17592186050646 Combining Linear Transformations Using 2x2 Matrices

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186093492 — Introduction

Suppose we are given two linear transformations represented by the matrices

$$
R = \begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}
	\qquad\text{and}\qquad
	S = \begin{bmatrix}1 & 0 \\ 0 & -1\end{bmatrix}.
$$

Here, $R$ represents a rotation of $90^\circ$ counterclockwise about the origin, and $S$ represents a reflection in the $x$-axis. Now, let $\mathbf{v}$ be a vector on the plane. Let's apply $R$ and then $S$ (in this particular order) to $\mathbf{v}.$ We obtain the following:

$$
\begin{aligned}v\overset{R}{⟶}Rv\overset{S}{⟶}S(Rv)\end{aligned}
$$

The above states that $\mathbf{v}$ under the action of $R$ is mapped to $R\mathbf{v},$ and then $R\mathbf{v}$ under the action of $S$ is mapped to $S(R\mathbf{v}).$

Since matrix multiplication is associative, we can write

$$
S(R\mathbf{v}) = (SR)\mathbf{v}.
$$

So, the product $SR$ (in this particular order) represents the combined transformation. 

In our case, the matrix that represents the combined transformation is

$$
\begin{aligned}SR & =\begin{bmatrix}1 & 0 \\ 0 & -1\end{bmatrix}\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix} \\  & =\begin{bmatrix}0 & -1 \\ -1 & 0\end{bmatrix}.\end{aligned}
$$



### tutorial 17592186093493 — The Order in Which Transformations Are Applied

The order in which the multiplication is carried out is extremely important! 

For example, consider the transformations 

$$
R = \begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}
	\qquad\text{and}\qquad
	S = \begin{bmatrix}1 & 0 \\ 0 & -1\end{bmatrix}.
$$

Computing the product $SR,$ we get 

$$
\begin{aligned}SR=\begin{bmatrix}1 & 0 \\ 0 & -1\end{bmatrix}\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}=\begin{bmatrix}0 & -1 \\ -1 & 0\end{bmatrix}.\end{aligned}
$$

Therefore, the transformation $SR$ represents a reflection in line $y=-x.$ 

On the other hand, computing the product $RS,$ we get

$$
\begin{aligned}RS=\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}\begin{bmatrix}1 & 0 \\ 0 & -1\end{bmatrix}=\begin{bmatrix}0 & 1 \\ 1 & 0\end{bmatrix}.\end{aligned}
$$

The product $RS$ represents a reflection in line $y=x,$ which is a completely different transformation than $SR.$ 

In general, the transformations are performed from right-to-left. So, for example, if we have

$$
\mathbf v' = SR\mathbf v,
$$

then we should think of the transformation $R$ as being applied *first*, followed by $S.$

**Note:** The reason why transformations are performed right-to-left is that the rightmost transformation is the first transformation preceding the input. In our case, to compute $SR \mathbf v,$

- we first apply $R$ to $\mathbf v$ to get $R \mathbf v,$

- and then we apply $S$ to $R \mathbf v$ to get $SR \mathbf v.$



### example 17592186091940 — Finding the Image of an Object Under a Combination of Linear Transformations

Consider the linear transformation that acts on vectors in $\mathbb{R}^2$ as follows (in the order given):

- it rotates vectors by $90^\circ$ clockwise about the origin, and then

- stretches the result by a scale factor of $2$ in the $y$-direction.

What is the image of the unit square shown below under the action of this linear transformation?

![](images/e9/e966d34d56ae25deb6bbf5849e813493c51730981031955e6833fd04d9ec1e2a.png)

First, we apply the rotation of $90^\circ$ clockwise:

![](images/4d/4da9df5bb1487aa693d9301c4a4901394da332197328637deef671a2bc59d204.png)

Then, we apply the stretch by a scale factor of $2$ in the $y$-direction:

![](images/f4/f400e267f38f4624d64e3a1899f9bbed3ba69996f1cf846ccc59e06e9eb5f35e.png)

### example 17592186091941 — Finding a Matrix That Represents a Combination of Two Linear Transformations

Construct the matrix of the linear transformation that acts on a vector in $\mathbb{R}^2$ as follows (in the order given):

- it rotates the vector by $\dfrac{\pi}{2}$ radians counterclockwise about the origin, and then

- stretches the result by a stretch factor of $2$ parallel to the $x$-axis.

Let $P$ be the matrix that represents the rotation and let $Q$ be the matrix that represents the stretch. These are given by the following elementary transformation matrices:

$$
\begin{aligned}P & =\begin{bmatrix}\operatorname{cos}⁡\left(\frac{\pi }{2}\right) & -\operatorname{sin}⁡\left(\frac{\pi }{2}\right) \\ \operatorname{sin}⁡\left(\frac{\pi }{2}\right) & \operatorname{cos}⁡\left(\frac{\pi }{2}\right)\end{bmatrix}=\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix} \\ Q & =\begin{bmatrix}2 & 0 \\ 0 & 1\end{bmatrix}\end{aligned}
$$

Therefore, the combined transformation can be represented by the matrix $QP\mathbin{:}$

$$
\begin{aligned}QP & =\begin{bmatrix}2 & 0 \\ 0 & 1\end{bmatrix}\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix} \\  & =\begin{bmatrix}0 & -2 \\ 1 & 0\end{bmatrix}\end{aligned}
$$

### example 17592186091942 — Finding a Matrix That Represents a Combination of Three Linear Transformations

Construct the matrix of the linear transformation that acts on a vector in $\mathbb{R}^2$ as follows (in the order given):

- It rotates the vector by $\dfrac{\pi}{3}$ radians counterclockwise about the origin, then

- scales the result by a scale factor of $5$ with the center of enlargement at the origin, and finally

- reflects the result about the $y$-axis.

Let $P$ be the matrix that represents the rotation, $Q$ be the matrix that represents the scaling, and $R$ be the matrix that represents the reflection. These are given by the following elementary transformation matrices:

$$
\begin{aligned}P & =\begin{bmatrix}\operatorname{cos}⁡\left(\frac{\pi }{3}\right) & -\operatorname{sin}⁡\left(\frac{\pi }{3}\right) \\ \operatorname{sin}⁡\left(\frac{\pi }{3}\right) & \operatorname{cos}⁡\left(\frac{\pi }{3}\right)\end{bmatrix}=\begin{bmatrix}\frac{1}{2} & -\frac{\sqrt{3}}{2} \\ \frac{\sqrt{3}}{2} & \frac{1}{2}\end{bmatrix}=\frac{1}{2}\begin{bmatrix}1 & -\sqrt{3} \\ \sqrt{3} & 1\end{bmatrix} \\ Q & =\begin{bmatrix}5 & 0 \\ 0 & 5\end{bmatrix}=5\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\ R & =\begin{bmatrix}-1 & 0 \\ 0 & 1\end{bmatrix}\end{aligned}
$$

Therefore, the combined transformation can be represented by the matrix $RQP\mathbin{:}$

$$
\begin{aligned}RQP & =\begin{bmatrix}-1 & 0 \\ 0 & 1\end{bmatrix}\left(5\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\right)\left(\frac{1}{2}\begin{bmatrix}1 & -\sqrt{3} \\ \sqrt{3} & 1\end{bmatrix}\right) \\  & =\frac{5}{2}\begin{bmatrix}-1 & 0 \\ 0 & 1\end{bmatrix}\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\begin{bmatrix}1 & -\sqrt{3} \\ \sqrt{3} & 1\end{bmatrix} \\  & =\frac{5}{2}\begin{bmatrix}-1 & 0 \\ 0 & 1\end{bmatrix}\begin{bmatrix}1 & -\sqrt{3} \\ \sqrt{3} & 1\end{bmatrix} \\  & =\frac{5}{2}\begin{bmatrix}-1 & \sqrt{3} \\ \sqrt{3} & 1\end{bmatrix}\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Finding the Image of an Object Under a Combination of Linear Transformations (5 captured questions)

Question 17592186092807 — question.difficulty/easy

![](images/e9/e966d34d56ae25deb6bbf5849e813493c51730981031955e6833fd04d9ec1e2a.png)

Consider the linear transformation that acts on vectors in ${R}^{2}$ as follows (in the order given):

- it rotates vectors by ${90}^{∘}$ counterclockwise about the origin, and then

- stretches the result by a scale factor of $2$ in the $x$-direction.

What is the image of the unit square shown above under the action of the linear transformation?

Solution: First, we apply the rotation of ${90}^{∘}$ counterclockwise:

![](images/de/de2d8506afb72def7df01b5ba60e4c338844f5116212e3b6a5a0e4598d5573fc.png)

Then, we apply the stretch by a scale factor of $2$ in the $x$-direction:

![](images/32/326fd93c3494c23a2ae97297964d94732c36a9aabf6c5b9d2d2647d6626fbf44.png)

Answer selection: images/32/326fd93c3494c23a2ae97297964d94732c36a9aabf6c5b9d2d2647d6626fbf44.png

Question 17592186092830 — question.difficulty/moderate

![](images/42/4229e1e8c92803a4d51043442a8bc65a6560e11a1e7559af7ec4246fe3005e75.png)

Consider the linear transformation that acts on vectors in ${R}^{2}$ as follows (in the order given):

- it shears vectors by a shear factor of $\frac{1}{2}$ in the $x$-direction, and then

- rotates the result by $\frac{\pi }{2}$ radians clockwise about the origin.

What is the image of the unit square shown above under the action of the linear transformation?

Solution: First, we apply the shear by a shear factor of $\frac{1}{2}$ in the $x$-direction:

![](images/c0/c0dfba56ed4c0ceb0b1739304c562040a2a69044117665bba5bf4fc2f506044f.png)

Then, we apply the rotation of $\frac{\pi }{2}$ radians clockwise:

![](images/ff/ff3dca52efc6e985e500f22ce43658855c09901535378081ed6fc07d5bfec115.png)

Answer selection: images/ff/ff3dca52efc6e985e500f22ce43658855c09901535378081ed6fc07d5bfec115.png

Question 17592186281513 — question.difficulty/moderate

![](images/ec/ec31e20140609e972eb1a5878c14d0b656dc5e931cc3deb7cc03ad2b4936bdef.png)

Consider the linear transformation that acts on vectors in ${R}^{2}$ as follows (in the order given):

- it shears vectors by a shear factor of $2$ in the $x$-direction, and then

- reflects the result in the $y$-axis.

What is the image of the unit square shown above under the action of the linear transformation?

Solution: First, we apply the shear by a shear factor of $2$ in the $x$-direction:

![](images/87/87247f5632dc5afb7e57d77227553cb0efd67872cc40a0e8d2804422284f7f64.png)

Then, we apply the reflection in the $y$-axis:

![](images/db/db2c82f441b8edaf821175b130a08f5a5ef3f18ab37282d9bb404e39e2f567d3.png)

Answer selection: images/db/db2c82f441b8edaf821175b130a08f5a5ef3f18ab37282d9bb404e39e2f567d3.png

### Finding a Matrix That Represents a Combination of Two Linear Transformations (9 captured questions)

Question 17592186092524 — question.difficulty/moderate

Construct the matrix of the linear transformation that acts on a vector in ${R}^{2}$ as follows (in the order given):

- it rotates the vector by $\frac{5\pi }{4}$ radians clockwise about the origin, and then

- stretches the result by a stretch factor of $\frac{1}{6}$ parallel to the $x$-axis.

Solution: Let $P$ be the matrix that represents the rotation and let $Q$ be the matrix that represents the stretch. These are given by the following elementary transformation matrices:

$$
\begin{aligned}P & =\begin{bmatrix}\operatorname{cos}⁡\left(-\frac{5\pi }{4}\right) & -\operatorname{sin}⁡\left(-\frac{5\pi }{4}\right) \\ \operatorname{sin}⁡\left(-\frac{5\pi }{4}\right) & \operatorname{cos}⁡\left(-\frac{5\pi }{4}\right)\end{bmatrix}=\begin{bmatrix}-\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{bmatrix}=\frac{1}{\sqrt{2}}\begin{bmatrix}-1 & -1 \\ 1 & -1\end{bmatrix} \\ Q & =\begin{bmatrix}\frac{1}{6} & 0 \\ 0 & 1\end{bmatrix}=\frac{1}{6}\begin{bmatrix}1 & 0 \\ 0 & 6\end{bmatrix}\end{aligned}
$$

Therefore, the combined transformation can be represented by the matrix $QP:$

$$
\begin{aligned}QP & =\left(\frac{1}{6}\begin{bmatrix}1 & 0 \\ 0 & 6\end{bmatrix}\right)\left(\frac{1}{\sqrt{2}}\begin{bmatrix}-1 & -1 \\ 1 & -1\end{bmatrix}\right) \\  & =\frac{1}{6\sqrt{2}}\begin{bmatrix}1 & 0 \\ 0 & 6\end{bmatrix}\begin{bmatrix}-1 & -1 \\ 1 & -1\end{bmatrix} \\  & =\frac{1}{6\sqrt{2}}\begin{bmatrix}-1 & -1 \\ 6 & -6\end{bmatrix}\end{aligned}
$$

Answer selection: \frac{1}{6\sqrt{2}}\begin{bmatrix}-1 & -1 \\ 6 & -6\end{bmatrix}

Question 17592186092525 — None

Construct the matrix of the linear transformation that acts on a vector in $R^{2}$ as follows (in the order given):

- it rotates the vector by $\frac{π}{4}$ radians clockwise about the origin, and then
- applies a shear transformation to the result with a shear factor of $\frac{1}{4}$ parallel to the $y$-axis.

Solution: 

Question 17592186256673 — question.difficulty/moderate

Construct the matrix of the linear transformation that acts on a vector in ${R}^{2}$ as follows (in the order given):

- it rotates the vector by $\frac{\pi }{6}$ radians counterclockwise about the origin, and then

- scales the result by a scale factor of $\sqrt{3}$ with center of enlargement at the origin.

Solution: Let $P$ be the matrix that represents the rotation and let $Q$ be the matrix that represents the scaling. These are given by the following elementary transformation matrices:

$$
\begin{aligned}P & =\begin{bmatrix}\operatorname{cos}⁡\left(\frac{\pi }{6}\right) & -\operatorname{sin}⁡\left(\frac{\pi }{6}\right) \\ \operatorname{sin}⁡\left(\frac{\pi }{6}\right) & \operatorname{cos}⁡\left(\frac{\pi }{6}\right)\end{bmatrix}=\begin{bmatrix}\frac{\sqrt{3}}{2} & -\frac{1}{2} \\ \frac{1}{2} & \frac{\sqrt{3}}{2}\end{bmatrix}=\frac{1}{2}\begin{bmatrix}\sqrt{3} & -1 \\ 1 & \sqrt{3}\end{bmatrix} \\ Q & =\begin{bmatrix}\sqrt{3} & 0 \\ 0 & \sqrt{3}\end{bmatrix}=\sqrt{3}\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\end{aligned}
$$

Therefore, the combined transformation can be represented by the matrix $QP:$

$$
\begin{aligned}QP & =\left(\sqrt{3}\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\right)\left(\frac{1}{2}\begin{bmatrix}\sqrt{3} & -1 \\ 1 & \sqrt{3}\end{bmatrix}\right) \\  & =\frac{\sqrt{3}}{2}\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\begin{bmatrix}\sqrt{3} & -1 \\ 1 & \sqrt{3}\end{bmatrix} \\  & =\frac{\sqrt{3}}{2}\begin{bmatrix}\sqrt{3} & -1 \\ 1 & \sqrt{3}\end{bmatrix}\end{aligned}
$$

Answer selection: \frac{\sqrt{3}}{2}\begin{bmatrix}\sqrt{3} & -1 \\ 1 & \sqrt{3}\end{bmatrix}

### Finding a Matrix That Represents a Combination of Three Linear Transformations (12 captured questions)

Question 17592186092860 — None

The matrix
$$
\displaystyle \frac{1}{\sqrt{2}}\begin{bmatrix}a & 4 \\ b & -1\end{bmatrix}
$$
represents the linear transformation that acts on a vector in $R^{2}$ as follows (in the order given):

- It rotates the vector by $\frac{π}{4}$ radians **clockwise** about the origin, then
- applies a shear transformation to the result with a shear factor of $3$ parallel to the $x$-axis, and finally
- reflects the result about the $x$-axis.

What is the value of $a + b$?

Solution: 

Question 17592186092866 — None

The matrix
$$
\displaystyle \begin{bmatrix}0 & a \\ b & 0\end{bmatrix}
$$
represents the linear transformation that acts on a vector in $R^{2}$ as follows (in the order given):

- It rotates the vector by $\frac{π}{2}$ radians counterclockwise about the origin, then
- stretches the result by a scale factor of $4$ parallel to the $x$-axis, and finally
- reflects the result about the $y$-axis.

What is the value of $a + b$?

Solution: 

Question 17592186281532 — question.difficulty/moderate

The matrix

$$
\begin{bmatrix}a & 0 \\ 0 & b\end{bmatrix}
$$

represents the linear transformation that acts on a vector in ${R}^{2}$ as follows (in the order given):

- It rotates the vector  $\pi $ radians counterclockwise about the origin, then

- stretches the result by a scale factor of $3$ parallel to the $x$-axis, and finally

- reflects the result about the $x$-axis.

What is the value of $a+b?$

Solution: Let $P$ be the matrix that represents the rotation, $Q$ be the matrix that represents the stretching, and $R$ be the matrix that represents the reflection. These are given by the following elementary transformation matrices:

$$
P=\begin{bmatrix}-1 & 0 \\ 0 & -1\end{bmatrix},\,Q=\begin{bmatrix}3 & 0 \\ 0 & 1\end{bmatrix},\,R=\begin{bmatrix}1 & 0 \\ 0 & -1\end{bmatrix}
$$

Hence, the combined transformation can be represented by the matrix $RQP:$

$$
\begin{aligned}RQP & =\begin{bmatrix}1 & 0 \\ 0 & -1\end{bmatrix}\begin{bmatrix}3 & 0 \\ 0 & 1\end{bmatrix}\begin{bmatrix}-1 & 0 \\ 0 & -1\end{bmatrix} \\  & =\begin{bmatrix}3 & 0 \\ 0 & -1\end{bmatrix}\begin{bmatrix}-1 & 0 \\ 0 & -1\end{bmatrix} \\  & =\begin{bmatrix}-3 & 0 \\ 0 & 1\end{bmatrix}\end{aligned}
$$

Therefore,
$$
\displaystyle a+b=(-3)+1=-2.
$$

Answer selection: -2
