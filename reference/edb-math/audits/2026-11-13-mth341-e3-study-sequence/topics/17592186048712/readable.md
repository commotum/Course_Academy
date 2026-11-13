# 17592186048712 Right-Angle Rotations as Linear Transformations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186093432 — Introduction

Consider the standard basis $\{\mathbf{i},\mathbf{j} \}$ of the Euclidean plane $\Bbb R^2$ and the unit square spanned by these two vectors. 

Let's define a linear transformation $\mathbf A$ by its standard matrix $A,$ given by 

$$
A = \left[ \begin{array}{cc}- 1 & 0 \\ 0 & - 1\end{array} \right] .
$$

We can find the images of $\{\mathbf{i},\mathbf{j} \}$ under $\mathbf A$ by computing the matrix products, as follows:
$$
\begin{array}{cc}{\mathbf{i}}^{\prime } &  = \mathbf{A} ( \mathbf{i} ) = \left[ \begin{array}{cc}{\color{blue}- 1} & 0 \\ {\color{blue}0} & - 1\end{array} \right] \left[ \begin{array}{c}1 \\ 0\end{array} \right] = \left[ \begin{array}{c}{\color{blue}- 1} \\ {\color{blue}0}\end{array} \right] = - \mathbf{i} \\ {\mathbf{j}}^{\prime } &  = \mathbf{A} ( \mathbf{j} ) = \left[ \begin{array}{cc}- 1 & {\color{red}0} \\ 0 & {\color{red}- 1}\end{array} \right] \left[ \begin{array}{c}0 \\ 1\end{array} \right] = \left[ \begin{array}{c}{\color{red}0} \\ {\color{red}- 1}\end{array} \right] = - \mathbf{j}\end{array}
$$

Plotting the vectors $\mathbf i$ and $\mathbf j$ and their images $\mathbf i'$ and $\mathbf j',$ we obtain the following:

![](images/c2/c2dc9f76bb23225cec0a4f62541d8a74c4c4b16d2e2f7c37e8d36922d97c59f0.png)

We see that the transformation $\mathbf A$ represented by the matrix $A$ defines a **counterclockwise rotation of $180^\circ$ (or $\pi$ radians) about the origin.**

Note that we typically refer to rotations in the counterclockwise sense. However, in this case, the transformation $\mathbf A$ can also be considered a rotation of $180^\circ$ (or $\pi$ radians) *clockwise* about the origin.



### example 17592186092066 — Using a Matrix That Represents a Rotation of 180 Degrees

A triangle $S$ has vertices at $(2,-1), (-3,5),$ and $(4,-3).$  Which of the following are coordinates of the vertices of $S',$ the image of $S$ under the counterclockwise rotation $\mathbf{R}_{\pi}$ by an angle of $\pi$ radians about the origin?

- $(-2,1)$

- $(-4,3)$

- $(-5,3)$

The counterclockwise rotation $\mathbf{R}_{\pi}$ by an angle of $\pi$ radians is given by the matrix

$$
R=
{\left[ \begin{array}{cc}- 1 & 0 \\ 0 & - 1\end{array} \right]}.
$$

To find the image of $S$ under the action of $\mathbf{R}_{\pi},$ we first create a matrix $X$ containing all of the vertices of $S$ as columns:

$$
\begin{aligned}X & =\begin{bmatrix}2 & -3 & 4 \\ -1 & 5 & -3\end{bmatrix}\end{aligned}
$$

Now, we compute the image of $X$ under $\mathbf{R}_{\pi}$ by calculating the matrix product $RX\mathbin{:}$

$$
\begin{aligned}RX & =\begin{bmatrix}-1 & 0 \\ 0 & -1\end{bmatrix}\begin{bmatrix}2 & -3 & 4 \\ -1 & 5 & -3\end{bmatrix} \\  & =\begin{bmatrix}-2 & 3 & -4 \\ 1 & -5 & 3\end{bmatrix}\end{aligned}
$$

Therefore, the coordinates of the respective vertices of $S'$ are $(-2,1), (3,-5), (-4,3).$

So, the correct answer is "I and II only."

### tutorial 17592186093431 — Rotations of 90 Degrees

Consider once again the standard basis $\{\mathbf{i},\mathbf{j} \}$ of the Euclidean plane $\Bbb R^2$ and the unit square that is spanned by these vectors.

Let's define a linear transformation $\mathbf A$ by its standard matrix $A,$ given by 

$$
A={\left[ \begin{array}{cc}0 & - 1 \\ 1 & 0\end{array} \right]}.
$$ 

As before, we can find the images of $\{\mathbf{i},\mathbf{j} \}$ under $\mathbf A$ as follows:
$$
\begin{array}{cc}{\mathbf{i}}^{\prime } &  = \mathbf{A} ( \mathbf{i} ) = \left[ \begin{array}{cc}{\color{blue}0} & - 1 \\ {\color{blue}1} & 0\end{array} \right] \left[ \begin{array}{c}1 \\ 0\end{array} \right] = \left[ \begin{array}{c}{\color{blue}0} \\ {\color{blue}1}\end{array} \right] = \mathbf{j} \\ {\mathbf{j}}^{\prime } &  = \mathbf{A} ( \mathbf{j} ) = \left[ \begin{array}{cc}0 & {\color{red}- 1} \\ 1 & {\color{red}0}\end{array} \right] \left[ \begin{array}{c}0 \\ 1\end{array} \right] = \left[ \begin{array}{c}{\color{red}- 1} \\ {\color{red}0}\end{array} \right] = - \mathbf{i}\end{array}
$$

Plotting the vectors $\mathbf i$ and $\mathbf j$ and their images $\mathbf i'$ and $\mathbf j',$ we obtain the following:

![](images/41/4195c8cd2f22fb0f84056226fb7b28c5f9944f747ca3230bf187752829b2a04e.png)

We see that the transformation $\mathbf A$ represented by the matrix $A$ defines a **counterclockwise rotation of $90^\circ,$ or $\dfrac \pi 2$ radians, about the origin.**

The transformation $\mathbf A$ can also be considered a rotation of $270^\circ,$ or $\dfrac{3\pi}{2}$ radians, *clockwise* about the origin.



### tutorial 17592186093434 — Rotations of 270 Degrees

Finally, let 

$$
{R}={\left[ \begin{array}{cc}0 & 1 \\ - 1 & 0\end{array} \right]}
$$

be a matrix of a linear transformation $\mathbf A.$ As usual, we can find the images of $\{\mathbf{i},\mathbf{j} \}$ under $\mathbf A$ as follows:
$$
\begin{array}{cc}{\mathbf{i}}^{\prime } &  = \mathbf{A} ( \mathbf{i} ) = \left[ \begin{array}{cc}{\color{blue}0} & 1 \\ {\color{blue}- 1} & 0\end{array} \right] \left[ \begin{array}{c}1 \\ 0\end{array} \right] = \left[ \begin{array}{c}{\color{blue}0} \\ {\color{blue}- 1}\end{array} \right] = - \mathbf{j} \\ {\mathbf{j}}^{\prime } &  = \mathbf{A} ( \mathbf{j} ) = \left[ \begin{array}{cc}0 & {\color{red}1} \\ - 1 & {\color{red}0}\end{array} \right] \left[ \begin{array}{c}0 \\ 1\end{array} \right] = \left[ \begin{array}{c}{\color{red}1} \\ {\color{red}0}\end{array} \right] = \mathbf{i}\end{array}
$$

Plotting the vectors $\mathbf i$ and $\mathbf j$ and their images $\mathbf i'$ and $\mathbf j',$ we obtain the following:

![](images/0f/0fc5f33d0bd7047ab02bd9bc3ea3b00c083ab214f3bc8a51e9cbb6e54dc6b51b.png)

We see that the transformation $\mathbf A$ represented by the matrix $A$ defines a **counterclockwise rotation of $270^\circ,$ or $\dfrac{3\pi}{2}$ radians, about the origin.**

The transformation $\mathbf A$ can also be considered a rotation of $90^\circ,$ or $\dfrac \pi 2$ radians *clockwise* about the origin.



### example 17592186092114 — Identifying Rotation Matrices

![](images/a4/a43a1658a16151c0306702959c50e8d0288077983ad50a084b39703e206469c0.png)

Consider the vector $\mathbf{v}$ shown above. Find the vector $A\mathbf{v}$ given that 
$$
A={\left[ \begin{array}{cc}0 & - 1 \\ 1 & 0\end{array} \right]}.
$$

Consider the standard basis $\{ \mathbf{i},\mathbf{j} \}$ of the Euclidean plane $\mathbb{R}^2$ and the unit square spanned by the vectors. Computing the images of $\{ \mathbf{i},\mathbf{j} \}$ under $A,$ we get the following:

$$
\begin{aligned}{i}^{′} & =Ai=\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}0 \\ 1\end{bmatrix}=j \\ {j}^{′} & =Aj=\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}-1 \\ 0\end{bmatrix}=-i\end{aligned}
$$

As a result, we obtain the following diagram:

![](images/41/414cb72ff004fe4c5898a0e2c7b60b4b3651473e776388fad21efd8fc9ae6165.png)

So, the matrix represents a rotation of $\dfrac{\pi}{2}$ radians counterclockwise about the origin.

Therefore, in order to find $A\mathbf{v},$ we need to rotate $\mathbf{v}$ counterclockwise by an angle of $\dfrac{\pi}{2}$ radians, as shown below.

![](images/b2/b24d8d460b7833a49f2bd7183f0f4b5d22d94a7d3b1d3bb9eb51beff9eeb7ef6.png)

### example 17592186092065 — Using a Matrix That Represents a Rotation of 90 Degrees

A triangle $S$ has vertices at  $(-5,-1), (1,4), (3,-5).$ Which of the following are coordinates of the vertices of $S',$ the image of $S$ under the **clockwise** rotation $\mathbf{R}_{-90^\circ}$ by an angle of $90^\circ$ about the origin?

- $(1,-5)$

- $(4,-1)$

- $(-5,-3)$

The clockwise rotation $\mathbf{R}_{-90^\circ}$ by an angle of $90^\circ$ is the same as counterclockwise rotation by an angle of $270^\circ.$ It's given by the matrix

$$
R=
{\left[ \begin{array}{cc}0 & 1 \\ - 1 & 0\end{array} \right]}.
$$

To find the image of $S$ under the action of $\mathbf{R}_{-90^\circ},$ we first create a matrix $X$ containing all of the vertices of $S$ as columns:

$$
\begin{aligned}X & =\begin{bmatrix}-5 & 1 & 3 \\ -1 & 4 & -5\end{bmatrix}\end{aligned}
$$

Now, we compute the image of $X$ under $\mathbf{R}_{-90^\circ}$ by calculating the matrix product $RX\mathbin{:}$

$$
\begin{aligned}RX & =\begin{bmatrix}0 & 1 \\ -1 & 0\end{bmatrix}\begin{bmatrix}-5 & 1 & 3 \\ -1 & 4 & -5\end{bmatrix} \\  & =\begin{bmatrix}-1 & 4 & -5 \\ 5 & -1 & -3\end{bmatrix}\end{aligned}
$$

Therefore, the coordinates of the respective vertices of $S'$ are $(-1,5), (4,-1), (-5,-3).$

So, the correct answer is "II and III only."

## Representative practice (first three per skill; full bank in practice.json)

### Using a Matrix That Represents a Rotation of 180 Degrees (14 captured questions)

Question 17592186092519 — question.difficulty/moderate

A triangle $S$ has vertices at $(-1,-2),(-1,2),(1,1).$  Which of the following are coordinates of the vertices of ${S}^{′},$ the image of $S$ under the **clockwise** rotation ${R}_{-\pi }$ by an angle of $\pi $ radians about the origin?

Select all that apply.

Solution: The clockwise rotation ${R}_{-\pi }$ by an angle of $\pi $ radians is the same as counterclockwise rotation by the same angle. It's given by the matrix

$$
R=\begin{bmatrix}-1 & 0 \\ 0 & -1\end{bmatrix}.
$$

To find the image of $S$ under the action of ${R}_{-\pi },$ we first create a matrix $X$ containing all of the vertices of $S:$

$$
\begin{aligned}X & =\begin{bmatrix}-1 & -1 & 1 \\ -2 & 2 & 1\end{bmatrix}\end{aligned}
$$

Now, we compute the image of $X$ under ${R}_{-\pi }$ by calculating the matrix product $RX:$

$$
\begin{aligned}RX & =\begin{bmatrix}-1 & 0 \\ 0 & -1\end{bmatrix}\begin{bmatrix}-1 & -1 & 1 \\ -2 & 2 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 1 & -1 \\ 2 & -2 & -1\end{bmatrix}\end{aligned}
$$

Therefore, the coordinates of the respective vertices of ${S}^{′}$ are $(1,2),(1,-2),(-1,-1).$

So, the correct answer is “The point $(1,2)$”; “The point $(1,-2)$”; “The point $(-1,-1)$”.

Answer The point $(-1,-1)$: true

Answer The point $(1,-2)$: true

Answer The point $(1,2)$: true

Question 17592186092844 — question.difficulty/easy

A triangle $S$ has vertices at $(-1, 1), (2, 3), (5, 1)$. Which of the following are coordinates of the vertices of $S^{′}$, the image of $S$ under the counterclockwise rotation $R_{180^{∘}}$ by an angle of $180^{∘}$ about the origin?

1. $(-5,-1)$
2. $(3, 2)$
3. $(1, 1)$

Solution: 

Question 17592186278283 — question.difficulty/moderate

A triangle $S$ has vertices at $(1,0),(-1,0),(2,1).$ Which of the following are coordinates of the vertices of ${S}^{′},$ the image of $S$ under the **clockwise** rotation ${R}_{-\pi }$ by an angle of $\pi $ radians about the origin?

Select all that apply.

Solution: The clockwise rotation ${R}_{-\pi }$ by an angle of $\pi $ radians is the same as counterclockwise rotation by the same angle. It's given by the matrix

$$
R=\begin{bmatrix}-1 & 0 \\ 0 & -1\end{bmatrix}.
$$

To find the image of $S$ under the action of ${R}_{-\pi },$ we first create a matrix $X$ containing all of the vertices of $S:$

$$
\begin{aligned}X & =\begin{bmatrix}1 & -1 & 2 \\ 0 & 0 & 1\end{bmatrix}\end{aligned}
$$

Now, we compute the image of $X$ under ${R}_{-\pi }$ by calculating the matrix product $RX:$

$$
\begin{aligned}RX & =\begin{bmatrix}-1 & 0 \\ 0 & -1\end{bmatrix}\begin{bmatrix}1 & -1 & 2 \\ 0 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}-1 & 1 & -2 \\ 0 & 0 & -1\end{bmatrix}\end{aligned}
$$

Therefore, the coordinates of the respective vertices of ${S}^{′}$ are $(1,0),(-1,0),(-2,-1).$

So, the correct answer is “The point $(1,0)$”; “The point $(-1,0)$” only.

Answer The point $(-1,0)$: true

Answer The point $(1,0)$: true

Answer The point $(2,1)$: false

### Identifying Rotation Matrices (17 captured questions)

Question 17592186092827 — question.difficulty/moderate

![](images/d1/d111b1df75cfaa0d86d17c06584c57b19ca4711ae3e6720e68d1704fd72d86ae.png)

Consider the vector $v$ shown above. Find the vector $Av$ given that 

$$
A=\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}.
$$

Solution: Consider the standard basis ${i,j}$ of the Euclidean plane ${R}^{2}$ and the unit square spanned by the vectors. Computing the images of ${i,j}$ under $A$, we get the following:

$$
\begin{aligned}{i}^{′} & =Ai=\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}0 \\ 1\end{bmatrix}=j \\ {j}^{′} & =Aj=\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}-1 \\ 0\end{bmatrix}=-i\end{aligned}
$$

As a result, we obtain the following diagram:

![](images/f1/f154267ed0a528b1e9fbec40064b090560410fe76dab00070e13fb3d1978b59c.png)

So, the matrix represents a rotation of $\frac{\pi }{2}$ radians counterclockwise about the origin.

Therefore, in order to find $Av$, we need to rotate $v$ counterclockwise by an angle of $\frac{\pi }{2}$ radians, as shown below.

![](images/dd/dd0496914b35f969896c6a54907fbfa5ea6c139c878d8682b933a8757bde7524.png)

Answer selection: images/0d/0d1ea82168dc6a122d1b20ad568b8958af496fc963edfb5e789bf57fc9108624.png

Question 17592186092828 — question.difficulty/easy

![](images/76/76e074486c71f2e53a9ff66528731ac6a6c1db43729032edd4423985ac25dbeb.png)

Consider the vector $v$ shown above. Find the vector $Av$ given that
$$
\displaystyle A = \begin{bmatrix}-1 & 0 \\ 0 & -1\end{bmatrix}.
$$

Solution: 

Question 17592186278322 — question.difficulty/easy

![](images/f3/f3e31d1c15a97adea32790eafe75ad1bc9f70c854b516b98de6648ec8d7bcb87.png)

Consider the vector $v$ shown above. Find the vector $Av$ given that 

$$
A=\begin{bmatrix}-1 & 0 \\ 0 & -1\end{bmatrix}.
$$

Solution: Consider the standard basis $\{i,j\}$ of the Euclidean plane ${R}^{2}$ and the unit square spanned by the vectors. Computing the images of $\{i,j\}$ under $A$, we get the following:

$$
\begin{aligned}{i}^{′} & =A(i)=\begin{bmatrix}-1 & 0 \\ 0 & -1\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}-1 \\ 0\end{bmatrix}=-i \\ {j}^{′} & =A(j)=\begin{bmatrix}-1 & 0 \\ 0 & -1\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}0 \\ -1\end{bmatrix}=-j\end{aligned}
$$

As a result, we obtain the following diagram:

![](images/9f/9fae3ec0ada3008937d88e4e76374a56da4369b1821cfee072c90d88b562df46.png)

So, the matrix represents a rotation of $\pi $ radians (counterclockwise or clockwise) about the origin.

Therefore, in order to find $Av$, we need to rotate $v$ (counterclockwise or clockwise) by an angle of $\pi $ radians, as shown below.

![](images/ae/ae800b271848948b5f60f5cd7c1cecd163c2aa7399e9a87e2a52d158857c6a42.png)

Answer selection: images/ba/ba328088ca187ea28b241a302a486da1145a51c7e134d8d4f529f5f4a916ddc1.png

### Using a Matrix That Represents a Rotation of 90 Degrees (15 captured questions)

Question 17592186092520 — question.difficulty/hard

A triangle $S$ has vertices at  $(-2,-3),(-3,2),(2,4).$ Which of the following are coordinates of the vertices of ${S}^{′},$ the image of $S$ under the **clockwise** rotation ${R}_{-{90}^{∘}}$ by an angle of ${90}^{∘}$ about the origin?

Select all that apply.

Solution: The clockwise rotation ${R}_{-{90}^{∘}}$ by an angle of ${90}^{∘}$ is the same as counterclockwise rotation by an angle of ${270}^{∘}.$ It's given by the matrix

$$
R=\begin{bmatrix}0 & 1 \\ -1 & 0\end{bmatrix}.
$$

To find the image of $S$ under the action of ${R}_{-{90}^{∘}},$ we first create a matrix $X$ containing all of the vertices of $S:$

$$
\begin{aligned}X & =\begin{bmatrix}-2 & -3 & 2 \\ -3 & 2 & 4\end{bmatrix}\end{aligned}
$$

Now, we compute the image of $X$ under ${R}_{-{90}^{∘}}$ by calculating the matrix product $RX:$

$$
\begin{aligned}RX & =\begin{bmatrix}0 & 1 \\ -1 & 0\end{bmatrix}\begin{bmatrix}-2 & -3 & 2 \\ -3 & 2 & 4\end{bmatrix} \\  & =\begin{bmatrix}-3 & 2 & 4 \\ 2 & 3 & -2\end{bmatrix}\end{aligned}
$$

Therefore, the coordinates of the respective vertices of ${S}^{′}$ are $(-3,2),(2,3),(4,-2).$

So, the correct answer is “The point $(-3,2)$”; “The point $(4,-2)$” only.

Answer The point $(-3,2)$: true

Answer The point $(-4,2)$: false

Answer The point $(4,-2)$: true

Question 17592186092521 — question.difficulty/moderate

A triangle $S$ has vertices at $(-2,-1),(1,4),(1,-1).$ Which of the following are coordinates of the vertices of ${S}^{′},$ the image of $S$ under the counterclockwise rotation ${R}_{\pi /2}$ by an angle of $\frac{\pi }{2}$ radians about the origin?

Select all that apply.

Solution: The counterclockwise rotation ${R}_{\pi /2}$ by an angle of $\frac{\pi }{2}$ radians is given by the matrix

$$
R=\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}.
$$

To find the image of $S$ under the action of ${R}_{\pi /2},$ we first create a matrix $X$ containing all of the vertices of $S:$

$$
\begin{aligned}X & =\begin{bmatrix}-2 & 1 & 1 \\ -1 & 4 & -1\end{bmatrix}\end{aligned}
$$

Now, we compute the image of $X$ under ${R}_{\pi /2}$ by calculating the matrix product $RX:$

$$
\begin{aligned}RX & =\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}\begin{bmatrix}-2 & 1 & 1 \\ -1 & 4 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & -4 & 1 \\ -2 & 1 & 1\end{bmatrix}\end{aligned}
$$

Therefore, the coordinates of the respective vertices of ${S}^{′}$ are $(1,-2),(-4,1),(1,1).$

So, the correct answer is “The point $(1,-2)$”; “The point $(1,1)$” only.

Answer The point $(1,-2)$: true

Answer The point $(1,1)$: true

Answer The point $(4,-2)$: false

Question 17592186253586 — question.difficulty/moderate

A triangle $S$ has vertices at $(-2,-3),(0,5),(2,-5).$ Which of the following are coordinates of the vertices of ${S}^{′},$ the image of $S$ under the counterclockwise rotation ${R}_{\pi /2}$ by an angle of $\frac{\pi }{2}$ radians about the origin?

Select all that apply.

Solution: The counterclockwise rotation ${R}_{\pi /2}$ by an angle of $\frac{\pi }{2}$ radians is given by the matrix

$$
R=\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}.
$$

To find the image of $S$ under the action of ${R}_{\pi /2},$ we first create a matrix $X$ containing all of the vertices of $S:$

$$
\begin{aligned}X & =\begin{bmatrix}-2 & 0 & 2 \\ -3 & 5 & -5\end{bmatrix}\end{aligned}
$$

Now, we compute the image of $X$ under ${R}_{\pi /2}$ by calculating the matrix product $RX:$

$$
\begin{aligned}RX & =\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}\begin{bmatrix}-2 & 0 & 2 \\ -3 & 5 & -5\end{bmatrix} \\  & =\begin{bmatrix}3 & -5 & 5 \\ -2 & 0 & 2\end{bmatrix}\end{aligned}
$$

Therefore, the coordinates of the respective vertices of ${S}^{′}$ are $(3,-2),(-5,0),(5,2).$

So, the correct answer is “The point $(3,-2)$”; “The point $(-5,0)$”; “The point $(5,2)$”.

Answer The point $(-5,0)$: true

Answer The point $(3,-2)$: true

Answer The point $(5,2)$: true
