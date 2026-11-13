# 17592186050231 Shear and Stretch as Linear Transformations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186107088 — Introduction

Consider the standard basis $\big\{ \mathbf{i},\mathbf{j} \big\}$ of the Euclidean plane $\mathbb{R}^2$ and the unit square spanned by the vectors.

Let $$
{T}=\begin{bmatrix}2 & 0 \\ 0 & 1\end{bmatrix}
$$ be a matrix of a linear transformation $\mathbf T.$ We can find the images of $\{ \mathbf{i},\mathbf{j} \}$ under $\mathbf{T}$ as follows:

$$
\begin{aligned}{i}^{'} & =T(i)=\begin{bmatrix}2 & 0 \\ 0 & 1\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}2 \\ 0\end{bmatrix}=2i \\ {j}^{'} & =T(j)=\begin{bmatrix}2 & 0 \\ 0 & 1\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}0 \\ 1\end{bmatrix}=j\end{aligned}
$$

Applying this transformation, we obtain the following image:

![](images/61/61fc1f3f1e76ff49b9967399d1b3a3a63bbe9845a59f2b2841af6e14510b2a7a.png)

We see that the transformation represented by the matrix $T$ multiplies the vector $\mathbf{i}$ by a factor of $2$ and leaves the vector $\mathbf j$ unchanged. This type of transformation is called a **stretch in the $\mathbf x$-direction.** We can also call it a **horizontal stretch.** In this case, we have a **horizontal stretch of scale factor** $\mathbf 2.$

In general, a stretch in the $x$-direction of scale factor $k$ with its center at the origin is represented by the matrix

$$
\begin{bmatrix}k & 0 \\ 0 & 1\end{bmatrix}
$$



### tutorial 17592186107101 — Vertical Stretch

Now, let <div class="matrix-operands matrix-operands-stacked">
<div>$T=\begin{bmatrix}1 & 0 \\ 0 & 2\end{bmatrix}$</div>
</div> be a matrix of a linear transformation $\mathbf T.$ We can find the images of $\{ \mathbf{i},\mathbf{j} \}$ under $\mathbf T$ as follows:

$$
\begin{aligned}{i}^{'} & =T(i)=\begin{bmatrix}1 & 0 \\ 0 & 2\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}1 \\ 0\end{bmatrix}=i \\ {j}^{'} & =T(j)=\begin{bmatrix}1 & 0 \\ 0 & 2\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}0 \\ 2\end{bmatrix}=2j\end{aligned}
$$

Applying this transformation, we obtain the following image:

![](images/19/19b1f75508ae7fc0255edcf2821bb26df352f46544add7740957291d9cb8e117.png)

The transformation represented by the matrix $T$ multiplies the vector $\mathbf{j}$ by $2$ and leaves the vector $\mathbf i$ unchanged. This type of transformation is called a **stretch in the $\mathbf y$-direction.** We can also call this a **vertical stretch**. In this case, we have a **vertical stretch of scale factor** $\mathbf 2$. 

In general, a stretch in the $y$-direction of scale factor $k$ with its center at the origin is represented by the matrix

$$
\begin{bmatrix}1 & 0 \\ 0 & k\end{bmatrix}
$$



### example 17592186105616 — Finding the Standard Matrix of a Stretch Transformation Given a Vector and its Image

A linear transformation $\mathbf{T}$ represents a stretch along the $x$-axis or $y$-axis. Given that $\mathbf{v}={\left[ \begin{array}{c}- 4 \\ 3\end{array} \right]}$ and $\mathbf{T}(\mathbf{v})={\left[ \begin{array}{c}- 16 \\ 3\end{array} \right]},$ what is the standard matrix of $\mathbf{T}?$

First, we are told that $\mathbf{T}$ represents a stretch along the $x$-axis or $y$-axis.

Comparing the $x$- and $y$-components of $\mathbf{v}$ and $\mathbf{T}(\mathbf{v}),$ we note the following:

- the $x$-component of $\mathbf{T}(\mathbf{v})$ is $4$ times the $x$-component of $\mathbf{v},$ while

- the $y$-components of $\mathbf{v}$ and $\mathbf{T}(\mathbf{v})$ are the same.

So, we conclude that $\mathbf{T}$ represents a stretch of scale factor $4$ in the $x$-direction. 

Therefore, the standard matrix of $\mathbf{T}$ is
$$
T = {\left[ \begin{array}{cc}4 & 0 \\ 0 & 1\end{array} \right]}.
$$

### tutorial 17592186107089 — Horizontal Shear

Consider the standard basis $\big\{ \mathbf{i},\mathbf{j} \big\}$ of the Euclidean plane $\mathbb{R}^2$ and the unit square spanned by the vectors.

Let $$
{T}=\begin{bmatrix}1 & 0.5 \\ 0 & 1\end{bmatrix}
$$ be a matrix of a linear transformation $\mathbf T.$ We can find the images of $\{ \mathbf{i},\mathbf{j} \}$ under $\mathbf{T}$ as follows:

$$
\begin{aligned}{i}^{'} & =T(i)=\begin{bmatrix}1 & 0.5 \\ 0 & 1\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}1 \\ 0\end{bmatrix}=i \\ {j}^{'} & =T(j)=\begin{bmatrix}1 & 0.5 \\ 0 & 1\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}0.5 \\ 1\end{bmatrix}=0.5i+j\end{aligned}
$$

Applying this transformation, we obtain the following image:

![](images/aa/aa646019f6af73e795661060a1a678b5b3be7961d7e60e3ae601d911033382d2.png)

The transformation represented by the matrix $T$ adds $0.5\mathbf{i}$ to $\mathbf j,$ while the vector $\mathbf i$ remains unchanged. This type of transformation is called a **horizontal shear.** In this case, we have a **horizontal shear with a shear factor of** $\mathbf{0.5}.$

In general, a horizontal shear of scale factor $k$ with its center at the origin is represented by the matrix

$$
\begin{bmatrix}1 & k \\ 0 & 1\end{bmatrix}
$$



### tutorial 17592186107102 — Vertical Shear

Now, let $$
{T}=\begin{bmatrix}1 & 0 \\ 0.5 & 1\end{bmatrix}
$$ be a matrix of a linear transformation $\mathbf T.$ We can find the images of $\{ \mathbf{i},\mathbf{j} \}$ under $\mathbf{T}$ as follows:

$$
\begin{aligned}{i}^{'} & =T(i)=\begin{bmatrix}1 & 0 \\ 0.5 & 1\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}1 \\ 0.5\end{bmatrix}=i+0.5j \\ {j}^{'} & =T(j)=\begin{bmatrix}1 & 0 \\ 0.5 & 1\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}0 \\ 1\end{bmatrix}=j\end{aligned}
$$

This gives the following image:

![](images/66/6626afefeea861f7a4d20e251021ed8db264f365051b85b619770293ac638b37.png)

The transformation represented by the matrix $T$ adds $0.5\mathbf{j}$ to $\mathbf i,$ while the vector $\mathbf j$ remains unchanged. This type of transformation is called a **vertical shear.** In this case, we have a **vertical shear with a shear factor of** $\mathbf{0.5}.$

In general, a vertical shear of scale factor $k$ with its center at the origin is represented by the matrix

$$
\begin{bmatrix}1 & 0 \\ k & 1\end{bmatrix}
$$



### example 17592186105617 — Identifying a Shear or Stretch Transformation Given the Images of the Standard Basis Vectors

Consider the standard basis $\{ \mathbf{i}, \mathbf{j} \}$ of $\,\mathbb{R}^2.$ If $\mathbf{T}$ is a linear transformation such that $\mathbf{T}(\mathbf{i})=\mathbf{i}+2\mathbf{j}$ and $\mathbf{T}(\mathbf{j})=\mathbf{j}$ then, what is the geometric interpretation of the transformation $\mathbf{T}?$

First, let's consider the unit square spanned by the vectors $\mathbf{i}$ and $\mathbf{j}.$

![](images/db/db15a65fd944c24ea2545baea08e6a0789b749295f623d8d4fdc2f07a37d4b73.png)

Now, using the fact that $\mathbf{T}(\mathbf{i})=\mathbf{i}+2\mathbf{j}$ and $\mathbf{T}(\mathbf{j})=\mathbf{j},$ we can draw the image of the square under the transformation $\mathbf{T}\mathbin{:}$

![](images/1e/1e5310f50dab35bc25447af9b37d972e11eda0afee98ac99b87a819ba62f56a1.png)

Therefore, the linear transformation $\mathbf{T}$ represents a vertical shear with a shear factor of $2.$

### example 17592186105618 — Identifying a Shear or Stretch Transformation Represented by a Matrix

What linear transformation is represented by the following matrix
$$
{\left[ \begin{array}{cc}1 & 2 \\ 0 & 1\end{array} \right]}?
$$

We can find the images of the standard basis vectors $\mathbf i$ and $\mathbf j$ under the action of  $\mathbf T,$ as follows:

$$
\begin{aligned}T(i) & =\begin{bmatrix}1 & 2 \\ 0 & 1\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}1 \\ 0\end{bmatrix}=i \\ T(j) & =\begin{bmatrix}1 & 2 \\ 0 & 1\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}2 \\ 1\end{bmatrix}=2i+j\end{aligned}
$$

Therefore, the matrix represents a *horizontal* shear with a shear factor of $2.$

### example 17592186105619 — Finding the Image of a Square Under a Shear or Stretch Transformation

![](images/61/611f958a7bd7475e37f743ef86affde7754195fe2c9ad414e628c17a09d47e38.png)

Let $T={\left[ \begin{array}{cc}1 & 0 \\ - 1 & 1\end{array} \right]}$ be the standard matrix of the linear transformation $\mathbf{T}.$ What is the image of the square $R$ (shown above) under the action of $\mathbf{T}?$

Looking at the matrix $T,$ we can see that $\mathbf{T}$ represents a vertical shear of shear factor $-1.$ Therefore, the image of the square $R$ under $\mathbf{T}$ is as follows:

![](images/2d/2d3d15c4d6b6f9e08c6fbcc35236b50dcd6cf4d09e9204e0aa255706461c3dd8.png)

**Alternative method:**

We can check that the vertices of $R$ are mapped to the vertices of the parallelogram shown above as follows:

$$
\begin{aligned}T\left(\begin{bmatrix}0 \\ 0\end{bmatrix}\right) & =\begin{bmatrix}1 & 0 \\ -1 & 1\end{bmatrix}\begin{bmatrix}0 \\ 0\end{bmatrix}=\begin{bmatrix}0 \\ 0\end{bmatrix} \\ T\left(\begin{bmatrix}2 \\ 0\end{bmatrix}\right) & =\begin{bmatrix}1 & 0 \\ -1 & 1\end{bmatrix}\begin{bmatrix}2 \\ 0\end{bmatrix}=\begin{bmatrix}2 \\ -2\end{bmatrix} \\ T\left(\begin{bmatrix}2 \\ 2\end{bmatrix}\right) & =\begin{bmatrix}1 & 0 \\ -1 & 1\end{bmatrix}\begin{bmatrix}2 \\ 2\end{bmatrix}=\begin{bmatrix}2 \\ 0\end{bmatrix} \\ T\left(\begin{bmatrix}0 \\ 2\end{bmatrix}\right) & =\begin{bmatrix}1 & 0 \\ -1 & 1\end{bmatrix}\begin{bmatrix}0 \\ 2\end{bmatrix}=\begin{bmatrix}0 \\ 2\end{bmatrix}\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Finding the Standard Matrix of a Stretch Transformation Given a Vector and its Image (6 captured questions)

Question 17592186106489 — question.difficulty/moderate

A linear transformation $T$ represents a stretch along the $x$-axis or $y$-axis. Given that $v=\begin{bmatrix}2 \\ -6\end{bmatrix}$ and $T(v)=\begin{bmatrix}2 \\ -2\end{bmatrix},$ what is the standard matrix of $T?$

Solution: First, we are told that $T$ represents a stretch along the $x$-axis or $y$-axis.

Comparing the $x$- and $y$-components of $v$ and $T(v),$ we note the following:

- the $x$-components of $v$ and $T(v)$ are the same, while

- the $y$-component of $T(v)$ is $\frac{1}{3}$ times the $y$-component of $v.$

So, we conclude that $T$ represents a stretch of scale factor $\frac{1}{3}$ in the $y$-direction.

Therefore, the standard matrix of $T$ is

$$
T=\begin{bmatrix}1 & 0 \\ 0 & \frac{1}{3}\end{bmatrix}.
$$

Answer selection: \begin{bmatrix}1 & 0 \\ 0 & \frac{1}{3}\end{bmatrix}

Question 17592186106490 — question.difficulty/easy

A linear transformation $T$ represents a stretch along the $x$-axis or $y$-axis. Given that $v=\begin{bmatrix}3 \\ -2\end{bmatrix}$ and $T(v)=\begin{bmatrix}6 \\ -2\end{bmatrix},$ what is the standard matrix of $T?$

Solution: First, we are told that $T$ represents a stretch along the $x$-axis or $y$-axis.

Comparing the $x$- and $y$-components of $v$ and $T(v),$ we note the following:

- the $x$-component of $T(v)$ is $2$ times the $x$-component of $v,$ while

- the $y$-components of $v$ and $T(v)$ are the same.

So, we conclude that $T$ represents a stretch of scale factor $2$ in the $x$-direction. 

Therefore, the standard matrix of $T$ is

$$
T=\begin{bmatrix}2 & 0 \\ 0 & 1\end{bmatrix}.
$$

Answer selection: \begin{bmatrix}2 & 0 \\ 0 & 1\end{bmatrix}

Question 17592186299626 — question.difficulty/easy

A linear transformation $T$ represents a stretch along the $x$-axis or $y$-axis. Given that $u=\begin{bmatrix}4 \\ -3\end{bmatrix}$ and $T(u)=\begin{bmatrix}12 \\ -3\end{bmatrix},$ what is the standard matrix of $T?$

<div class="matrix-answer">
<span class="matrix-answer-label">$T=\,\,$</span>
<div class="matrix-answer-brackets">
<table aria-label="Answer matrix"><tbody>
<tr><td>{{field-1}}</td><td>{{field-2}}</td></tr>
<tr><td>$0$</td><td>{{field-3}}</td></tr>
</tbody></table>
</div>
</div>

Solution: First, we are told that $T$ represents a stretch along the $x$-axis or $y$-axis.

Comparing the $x$- and $y$-components of $u$ and $T(u),$ we note the following:

- the $y$-components of $u$ and $T(u)$ are the same, while

- the $x$-component of $T(u)$ is $3$ times the $x$-component of $u.$

So, we conclude that $T$ represents a stretch of scale factor $3$ in the $x$-direction. 

Therefore, the standard matrix of $T$ is

$$
T=\begin{bmatrix}3 & 0 \\ 0 & 1\end{bmatrix}.
$$

Answer field-1: 3

Answer field-2: 0

Answer field-3: 1

### Identifying a Shear or Stretch Transformation Given the Images of the Standard Basis Vectors (7 captured questions)

Question 17592186106305 — None

Consider the standard basis ${i, j}$ of $R^{2}$. If $T$ is a linear transformation such that $T(i) = 4i$ and $T(j) = j$, then what is the geometric interpretation of the transformation $T$?

Solution: 

Question 17592186106306 — question.difficulty/hard

Consider the standard basis ${i,j}$ of ${R}^{2}.$ If $T$ is a linear transformation such that $T(i)=i$ and $T(j)=1.5i+j,$ then what is the geometric interpretation of the transformation $T?$

Solution: First, let's consider the unit square spanned by the vectors $i$ and $j.$

![](images/db/db15a65fd944c24ea2545baea08e6a0789b749295f623d8d4fdc2f07a37d4b73.png)

Now, using the fact that $T(i)=i$ and $T(j)=1.5i+j,$ we can draw the image of the square under the transformation $T:$

![](images/f5/f5ebbff856529ad8cd3da41bf2f7d373294af3e0153c5e8da7da4c7b069b8b25.png)

Therefore, the linear transformation $T$ represents a horizontal shear with a shear factor of $1.5.$

Answer selection: A horizontal shear with a shear factor of $1.5$

Question 17592186284561 — question.difficulty/moderate

Consider the standard basis ${i,j}$ of $\,{R}^{2}.$ If $T$ is a linear transformation such that $T(i)=i$ and $T(j)=2j,$ then what is the geometric interpretation of the transformation $T?$

Solution: First, let's consider the unit square spanned by the vectors $\,i\,$ and  $\,j.$ 

![](images/34/34c82826da26290fc890671734c354fbfd9c253f1cfaca38de1ea615434e6766.png)

Now, using the fact that $T(i)=i$ and $T(j)=2j,$ we can draw the image of the square under the transformation $T:$

![](images/56/56a5f95d469cb63e20936a6c07971d9e80611d966282cb37d7ddf17fdc761bab.png)

Therefore, the linear transformation $T$ represents a stretch with a scale factor $2$ in the $y$-direction.

Answer selection: A stretch with a scale factor $2$ in the $y$-direction

### Identifying a Shear or Stretch Transformation Represented by a Matrix (7 captured questions)

Question 17592186106035 — question.difficulty/moderate

What linear transformation is represented by the following matrix
$$
\displaystyle \begin{bmatrix}1 & 10 \\ 0 & 1\end{bmatrix}?
$$

Solution: We can find the images of the standard basis vectors $i$ and $j$ under the action of  $T,$ as follows:

$$
\begin{aligned}T(i) & =\begin{bmatrix}1 & 10 \\ 0 & 1\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}1 \\ 0\end{bmatrix}=i \\ T(j) & =\begin{bmatrix}1 & 10 \\ 0 & 1\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}10 \\ 1\end{bmatrix}=10i+j\end{aligned}
$$

Therefore, the matrix represents a *horizontal* shear with a shear factor of $10.$

Answer selection: A horizontal shear with a shear factor of $10$

Question 17592186106491 — question.difficulty/moderate

What linear transformation is represented by the following matrix
$$
\displaystyle \begin{bmatrix}1 & 0 \\ 12 & 1\end{bmatrix}?
$$

Solution: We can find the images of the standard basis vectors $i$ and $j$ under the action of  $T,$ as follows:

$$
\begin{aligned}T(i) & =\begin{bmatrix}1 & 0 \\ 12 & 1\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}1 \\ 12\end{bmatrix}=i+12j \\ T(j) & =\begin{bmatrix}1 & 0 \\ 12 & 1\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}0 \\ 1\end{bmatrix}=j\end{aligned}
$$

Therefore, the matrix represents a *vertical* shear with a shear factor of $12.$

Answer selection: A vertical shear with a shear factor of $12$

Question 17592186256406 — question.difficulty/moderate

What linear transformation is represented by the following matrix
$$
\displaystyle \begin{bmatrix}1 & 4 \\ 0 & 1\end{bmatrix}?
$$

Solution: We can find the images of the standard basis vectors $i$ and $j$ under the action of  $T,$ as follows:

$$
\begin{aligned}T(i) & =\begin{bmatrix}1 & 4 \\ 0 & 1\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}1 \\ 0\end{bmatrix}=i \\ T(j) & =\begin{bmatrix}1 & 4 \\ 0 & 1\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}4 \\ 1\end{bmatrix}=4i+j\end{aligned}
$$

Therefore, the matrix represents a *horizontal* shear with a shear factor of $4.$

Answer selection: A horizontal shear with a shear factor of $4$

### Finding the Image of a Square Under a Shear or Stretch Transformation (7 captured questions)

Question 17592186106304 — None

![](images/61/611f958a7bd7475e37f743ef86affde7754195fe2c9ad414e628c17a09d47e38.png)

Let $T = \begin{bmatrix}\frac{1}{2} & 0 \\ 0 & 1\end{bmatrix}$ be the standard matrix of the linear transformation $T$. What is the image of the square $R$ (shown above) under the action of $T$?

Solution: 

Question 17592186106307 — question.difficulty/hard

![](images/61/611f958a7bd7475e37f743ef86affde7754195fe2c9ad414e628c17a09d47e38.png)

Let $T=\begin{bmatrix}1 & \frac{1}{2} \\ 0 & 1\end{bmatrix}$ be the standard matrix of the linear transformation $T.$ What is the image of the square $R$ (shown above) above under the action of $T?$

Solution: Looking at the matrix $T$, we can see that $T$ represents a horizontal shear of shear factor $\frac{1}{2}.$ Therefore, the image of the square $R$ under $T$ is

![](images/85/85ff90a404a22310659fadd3a00c58490c9745d443b180d6b509b40a5497376b.png)

**Alternative method:**

We can check that the vertices of $R$ are mapped to the vertices of the parallelogram shown above as follows:

$$
\begin{aligned}T\left(\begin{bmatrix}0 \\ 0\end{bmatrix}\right) & =\begin{bmatrix}1 & \frac{1}{2} \\ 0 & 1\end{bmatrix}\begin{bmatrix}0 \\ 0\end{bmatrix}=\begin{bmatrix}0 \\ 0\end{bmatrix} \\ T\left(\begin{bmatrix}2 \\ 0\end{bmatrix}\right) & =\begin{bmatrix}1 & \frac{1}{2} \\ 0 & 1\end{bmatrix}\begin{bmatrix}2 \\ 0\end{bmatrix}=\begin{bmatrix}2 \\ 0\end{bmatrix} \\ T\left(\begin{bmatrix}2 \\ 2\end{bmatrix}\right) & =\begin{bmatrix}1 & \frac{1}{2} \\ 0 & 1\end{bmatrix}\begin{bmatrix}2 \\ 2\end{bmatrix}=\begin{bmatrix}3 \\ 2\end{bmatrix} \\ T\left(\begin{bmatrix}0 \\ 2\end{bmatrix}\right) & =\begin{bmatrix}1 & \frac{1}{2} \\ 0 & 1\end{bmatrix}\begin{bmatrix}0 \\ 2\end{bmatrix}=\begin{bmatrix}1 \\ 2\end{bmatrix}\end{aligned}
$$

Answer selection: images/10/104eeafc851528b17a22a683b44a9e74c83d851976c65d39c697d550f79270c3.png

Question 17592186323972 — question.difficulty/hard

![](images/61/611f958a7bd7475e37f743ef86affde7754195fe2c9ad414e628c17a09d47e38.png)

Let $T=\begin{bmatrix}1 & -\frac{1}{2} \\ 0 & 1\end{bmatrix}$ be the standard matrix of the linear transformation $T.$ What is the image of the square $R$ (shown above) under the linear transformation $T?$

Solution: Looking at the matrix $T$, we can see that $T$ represents a horizontal shear of shear factor $-\frac{1}{2}.$ Therefore, the image of the square $R$ under $T$ is

![](images/4b/4b6cfc485ffa74f141e3dc4b8fad61b48103808a4f4c29b2dc5180f634902c4f.png)

**Alternative method:**

We can check that the vertices of $R$ are mapped to the vertices of the parallelogram shown above as follows:

$$
\begin{aligned}T\left(\begin{bmatrix}0 \\ 0\end{bmatrix}\right) & =\begin{bmatrix}1 & -\frac{1}{2} \\ 0 & 1\end{bmatrix}\begin{bmatrix}0 \\ 0\end{bmatrix}=\begin{bmatrix}0 \\ 0\end{bmatrix} \\ T\left(\begin{bmatrix}2 \\ 0\end{bmatrix}\right) & =\begin{bmatrix}1 & -\frac{1}{2} \\ 0 & 1\end{bmatrix}\begin{bmatrix}2 \\ 0\end{bmatrix}=\begin{bmatrix}2 \\ 0\end{bmatrix} \\ T\left(\begin{bmatrix}2 \\ 2\end{bmatrix}\right) & =\begin{bmatrix}1 & -\frac{1}{2} \\ 0 & 1\end{bmatrix}\begin{bmatrix}2 \\ 2\end{bmatrix}=\begin{bmatrix}1 \\ 2\end{bmatrix} \\ T\left(\begin{bmatrix}0 \\ 2\end{bmatrix}\right) & =\begin{bmatrix}1 & -\frac{1}{2} \\ 0 & 1\end{bmatrix}\begin{bmatrix}0 \\ 2\end{bmatrix}=\begin{bmatrix}-1 \\ 2\end{bmatrix}\end{aligned}
$$

Answer selection: images/5b/5b8e80ca6209eeb01ddad113b796d65fc7a60e9036594759780489321091bc42.png
