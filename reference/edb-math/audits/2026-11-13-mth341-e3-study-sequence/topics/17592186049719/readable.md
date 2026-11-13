# 17592186049719 Dilations and Reflections as Linear Transformations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186088930 — Introduction

A **dilation** of scale factor $k$ with the center at the origin is a linear transformation that multiplies the standard basis vectors by $k.$ It is represented by the matrix
$$
{\left[ \begin{array}{cc}k & 0 \\ 0 & k\end{array} \right]}.
$$

For example, let $T={\left[ \begin{array}{cc}2 & 0 \\ 0 & 2\end{array} \right]}$ be the matrix of a linear transformation $\mathbf{T}.$ This transformation is a dilation of scale factor $2.$

To visualize the dilation $\mathbf{T},$ consider the standard basis $\{ \mathbf{i},\mathbf{j} \}$ of the Euclidean plane $\mathbb{R}^2$ and the unit square $\mathrm{R}$ spanned by the vectors, as shown below. 

![](images/6e/6e38185922e9cad6d3961e7c5e755eabf4c52eafd1cc81a1e81a383b4df5ae82.png)

We can find the images of $\{ \mathbf{i},\mathbf{j} \}$ under $T,$ as follows:

$$
\begin{aligned}{i}^{′} & =Ti=\begin{bmatrix}2 & 0 \\ 0 & 2\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}2 \\ 0\end{bmatrix}=2i, \\ {j}^{′} & =Tj=\begin{bmatrix}2 & 0 \\ 0 & 2\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}0 \\ 2\end{bmatrix}=2j.\end{aligned}
$$

The transformation $\mathbf{T}$ multiplies vectors $\mathbf{i}$ and $\mathbf{j}$ by $2.$ The resulting vectors span a larger region, shown below.

![](images/cc/cc6677c641a2a713e0324db90edfdd86a5ca1c096c0ffd70f1216119f36da645.png)



### example 17592186087568 — Finding the Standard Matrix of a Dilation Given a Vector and its Image

A linear transformation $\mathbf{T}$ represents a dilation. Given that $\mathbf{v}={\left[ \begin{array}{c}24 \\ 16\end{array} \right]}$ and $\mathbf{T}(\mathbf{v})={\left[ \begin{array}{c}6 \\ 4\end{array} \right]},$ what is the standard matrix of $\mathbf{T}?$

We can write $\mathbf{T}(\mathbf{v})$ as follows:

$$
\begin{aligned}T(v) & =\begin{bmatrix}6 \\ 4\end{bmatrix} \\  & =\frac{1}{4}\cdot \begin{bmatrix}24 \\ 16\end{bmatrix} \\  & =\frac{1}{4}v\end{aligned}
$$

Since we have $\mathbf{T}(\mathbf{v}) = \dfrac{1}{4}\mathbf{v},$ we conclude that the linear transformation $\mathbf T$ is a dilation with scale factor $k = \dfrac{1}{4}.$

Remember that the matrix representing a dilation of scale factor $k$ is given by
$$
{\left[ \begin{array}{cc}k & 0 \\ 0 & k\end{array} \right]}.
$$

Therefore, the standard matrix of $\mathbf{T}$ is
$$
T = {\left[ \begin{array}{cc}{\displaystyle \frac{1}{4}} & 0 \\ 0 & {\displaystyle \frac{1}{4}}\end{array} \right]}.
$$

### tutorial 17592186088931 — Reflection in the X and Y Axes

A **reflection in the $x$-axis** is represented by the matrix
$$
T={\left[ \begin{array}{cc}1 & 0 \\ 0 & - 1\end{array} \right]}.
$$

To visualize a reflection in the $x$-axis, consider the standard basis $\{ \mathbf{i},\mathbf{j} \}$ of the Euclidean plane $\mathbb{R}^2$ and the unit square $\mathrm{R}$ spanned by the vectors, as shown below. 

![](images/9e/9e322e6ed1ddb8f1d094633e931cd179b7eb9d6f47acd7c7d0809f113df91b22.png)

We can find the images of $\{ \mathbf{i},\mathbf{j} \}$ under $T,$ as follows:

$$
\begin{aligned}{i}^{′} & =T(i)=\begin{bmatrix}1 & 0 \\ 0 & -1\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}1 \\ 0\end{bmatrix}=i \\ {j}^{′} & =T(j)=\begin{bmatrix}1 & 0 \\ 0 & -1\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}0 \\ -1\end{bmatrix}=-j\end{aligned}
$$

Then, we obtain the following image:

![](images/b9/b93bb91dae85a3e3b40a8d0ade3d4f420064aaa6926431fa7f664c977bb8fd59.png)

Similarly, a **reflection in the $y$-axis** is represented by the matrix
$$
T = {\left[ \begin{array}{cc}- 1 & 0 \\ 0 & 1\end{array} \right]}.
$$

Again, we can find the images of $\{ \mathbf{i},\mathbf{j} \}$ under $T,$ as follows:

$$
\begin{aligned}{i}^{′} & =T(i)=\begin{bmatrix}-1 & 0 \\ 0 & 1\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}-1 \\ 0\end{bmatrix}=-i \\ {j}^{′} & =T(j)=\begin{bmatrix}-1 & 0 \\ 0 & 1\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}0 \\ 1\end{bmatrix}=j\end{aligned}
$$

We obtain the following image:

![](images/49/4993d8586a84e4a40a54edddd8011cd3d516264bfffc7e3c33d27a10edf1e7d7.png)



### tutorial 17592186088956 — Reflection in the Lines y=x and y=-x

A **reflection in line $y=x$** is represented by the matrix
$$
T = {\left[ \begin{array}{cc}0 & 1 \\ 1 & 0\end{array} \right]}.
$$

We can find the images of $\{ \mathbf{i},\mathbf{j} \}$ under $T$, as follows:

$$
\begin{aligned}{i}^{′} & =T(i)=\begin{bmatrix}0 & 1 \\ 1 & 0\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}0 \\ 1\end{bmatrix}=j \\ {j}^{′} & =T(j)=\begin{bmatrix}0 & 1 \\ 1 & 0\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}1 \\ 0\end{bmatrix}=i\end{aligned}
$$

Then, we obtain the following image:

![](images/0e/0e37a258ea833a2d490fc34a34af40a5c7a18f7589f107c6d0ed631b331c8f2a.png)

Similarly, a **reflection in line $y=-x$** is represented by the matrix
$$
T = {\left[ \begin{array}{cc}0 & - 1 \\ - 1 & 0\end{array} \right]}.
$$

We can find the images of $\{ \mathbf{i},\mathbf{j} \}$ under $T,$ as follows:

$$
\begin{aligned}{i}^{′} & =T(i)=\begin{bmatrix}0 & -1 \\ -1 & 0\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}0 \\ -1\end{bmatrix}=-j \\ {j}^{′} & =T(j)=\begin{bmatrix}0 & -1 \\ -1 & 0\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}-1 \\ 0\end{bmatrix}=-i\end{aligned}
$$

Then, we obtain the following image:

![](images/4a/4a83673a409fd2e5d33b0b5f743f57af08cfb27c38e312a636179102c2172b04.png)



### example 17592186087567 — Identifying the Linear Transformation Represented by a Matrix

What linear transformation is represented by the matrix
$$
{\left[ \begin{array}{cc}1 & 0 \\ 0 & - 1\end{array} \right]}?
$$

Consider the standard basis $\{ \mathbf{i},\mathbf{j} \}$ of the Euclidean plane $\mathbb{R}^2$ and the unit square spanned by the vectors, as depicted below. 

![](images/9e/9e322e6ed1ddb8f1d094633e931cd179b7eb9d6f47acd7c7d0809f113df91b22.png)

We can find the images of $\{ \mathbf{i},\mathbf{j} \}$ under $T,$ as follows:

$$
\begin{aligned}{i}^{′} & =T(i)=\begin{bmatrix}1 & 0 \\ 0 & -1\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}1 \\ 0\end{bmatrix}=i \\ {j}^{′} & =T(j)=\begin{bmatrix}1 & 0 \\ 0 & -1\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}0 \\ -1\end{bmatrix}=-j\end{aligned}
$$

Then, we obtain the following image:

![](images/b9/b93bb91dae85a3e3b40a8d0ade3d4f420064aaa6926431fa7f664c977bb8fd59.png)

Therefore, the matrix represents the reflection across the $x$-axis.

## Representative practice (first three per skill; full bank in practice.json)

### Finding the Standard Matrix of a Dilation Given a Vector and its Image (21 captured questions)

Question 17592186088154 — None

A linear transformation $T$ represents a dilation. Given that $v = \begin{bmatrix}2 \\ -6\end{bmatrix}$ and $T(v) = \begin{bmatrix}30 \\ -90\end{bmatrix}$, what is the standard matrix of $T$?

Solution: 

Question 17592186088155 — question.difficulty/easy

A  linear transformation $T$ represents a dilation. Given that $v=\begin{bmatrix}8 \\ -1\end{bmatrix}$ and $T(v)=\begin{bmatrix}48 \\ -6\end{bmatrix},$ what is the standard matrix of $T?$

Solution: We can write $T(v)$ as follows:

$$
\begin{aligned}T(v) & =\begin{bmatrix}48 \\ -6\end{bmatrix} \\  & =6\cdot \begin{bmatrix}8 \\ -1\end{bmatrix} \\  & =6v\end{aligned}
$$

So we have $T(v)=6v,$ and so the linear transformation $T$ is a dilation with scale factor $k=6.$

The matrix that represents a dilation of scale factor $k$ is given by

$$
\begin{bmatrix}k & 0 \\ 0 & k\end{bmatrix}.
$$

Therefore, the standard matrix of $T$ is

$$
T=\begin{bmatrix}6 & 0 \\ 0 & 6\end{bmatrix}.
$$

Answer selection: \begin{bmatrix}6 & 0 \\ 0 & 6\end{bmatrix}

Question 17592186278257 — question.difficulty/easy

A linear transformation $T$ represents a dilation.  Given that $v=\begin{bmatrix}16 \\ -20\end{bmatrix}$ and $T(v)=\begin{bmatrix}4 \\ -5\end{bmatrix},$ what is the standard matrix of $T?$

Solution: We can write $T(v)$ as follows:

$$
\begin{aligned}T(v) & =\begin{bmatrix}4 \\ -5\end{bmatrix} \\  & =\frac{1}{4}\cdot \begin{bmatrix}16 \\ -20\end{bmatrix} \\  & =\frac{1}{4}v\end{aligned}
$$

So we have $T(v)=\frac{1}{4}v,$ and so the linear transformation $T$ is a dilation with scale factor $k=\frac{1}{4}.$

The matrix that represents a dilation of scale factor $k$ is given by

$$
\begin{bmatrix}k & 0 \\ 0 & k\end{bmatrix}.
$$

Therefore, the standard matrix of $T$ is

$$
T=\begin{bmatrix}\frac{1}{4} & 0 \\ 0 & \frac{1}{4}\end{bmatrix}.
$$

Answer selection: \begin{bmatrix}\frac{1}{4} & 0 \\ 0 & \frac{1}{4}\end{bmatrix}

### Identifying the Linear Transformation Represented by a Matrix (17 captured questions)

Question 17592186088359 — question.difficulty/hard

Which of the following represents a reflection across the $y$-axis?

Solution: The correct answer is $T=\begin{bmatrix}-1 & 0 \\ 0 & 1\end{bmatrix}.$ Indeed, consider the standard basis ${i,j}$ of the Euclidean plane ${R}^{2}$ and the unit square spanned by the vectors, as shown below. 

![](images/9e/9e322e6ed1ddb8f1d094633e931cd179b7eb9d6f47acd7c7d0809f113df91b22.png)

Now, we can find the images of ${i,j}$ under $T$, as follows:

$$
\begin{aligned}{i}^{′} & =T(i)=\begin{bmatrix}-1 & 0 \\ 0 & 1\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}-1 \\ 0\end{bmatrix}=-i \\ {j}^{′} & =T(j)=\begin{bmatrix}-1 & 0 \\ 0 & 1\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}0 \\ 1\end{bmatrix}=j\end{aligned}
$$

Therefore, we obtain the following image:

![](images/49/4993d8586a84e4a40a54edddd8011cd3d516264bfffc7e3c33d27a10edf1e7d7.png)

Answer selection: \begin{bmatrix}-1 & 0 \\ 0 & 1\end{bmatrix}

Question 17592186088383 — None

What linear transformation $T$ is represented by the matrix $T = \begin{bmatrix}0 & 1 \\ 1 & 0\end{bmatrix}$?

Solution: 

Question 17592186253584 — question.difficulty/easy

What linear transformation $T$ is represented by the matrix $T=\begin{bmatrix}2 & 0 \\ 0 & 2\end{bmatrix}?$

Solution: Recall that a dilation of scale factor $k$ is represented by the matrix

$$
\begin{bmatrix}k & 0 \\ 0 & k\end{bmatrix}.
$$

Here, we have $k=2.$ Therefore, the matrix represents a dilation with a scale factor of $2.$

Answer selection: Dilation with scale factor $2$
