# 17592186049891 Rotations as Linear Transformations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186093433 — Introduction

Consider the standard basis $\big\{ \mathbf{i},\mathbf{j} \big\}$ of the Euclidean plane $\mathbb{R}^2$ and the unit square spanned by these two vectors. 

Let's define a linear transformation $\mathbf R$ by its standard matrix $R,$ given by 

$$
{R}=\begin{bmatrix}\operatorname{cos}{30}^{∘} & -\operatorname{sin}{30}^{∘} \\ \operatorname{sin}{30}^{∘} & \operatorname{cos}{30}^{∘}\end{bmatrix}.
$$

We can find the images of $\{ \mathbf{i},\mathbf{j} \}$ under $\mathbf{R}$ by computing the matrix products, as follows:

$$
\begin{aligned}{i}^{'} & =R(i)=\begin{bmatrix}\operatorname{cos}{30}^{∘} & -\operatorname{sin}{30}^{∘} \\ \operatorname{sin}{30}^{∘} & \operatorname{cos}{30}^{∘}\end{bmatrix}\begin{bmatrix}1 \\ 0\end{bmatrix}=\begin{bmatrix}\operatorname{cos}{30}^{∘} \\ \operatorname{sin}{30}^{∘}\end{bmatrix} \\ {j}^{'} & =R(j)=\begin{bmatrix}\operatorname{cos}{30}^{∘} & -\operatorname{sin}{30}^{∘} \\ \operatorname{sin}{30}^{∘} & \operatorname{cos}{30}^{∘}\end{bmatrix}\begin{bmatrix}0 \\ 1\end{bmatrix}=\begin{bmatrix}-\operatorname{sin}{30}^{∘} \\ \operatorname{cos}{30}^{∘}\end{bmatrix}\end{aligned}
$$

Plotting the vectors $\mathbf i$ and $\mathbf j$ and their images $\mathbf i'$ and $\mathbf j',$ we obtain the following:

![](images/35/3516ba56a842adb78f1acae9190b65eb1574629e9f3d6bca25854f547f69385f.png)

We see that the transformation $\mathbf R$ represented by the matrix $R$ defines a **counterclockwise rotation of $30^\circ$ about the origin.**

As usual, we typically refer to rotations in the counterclockwise sense. However, in this case, the transformation $\mathbf R$ can also be considered a rotation of $360^\circ-30^\circ=330^\circ$ *clockwise* about the origin.



### tutorial 17592186093435 — General Rotation Matrix

The matrix $R_\theta,$ given by

$$
R_\theta = \begin{bmatrix}\operatorname{cos}\theta  & -\operatorname{sin}\theta  \\ \operatorname{sin}\theta  & \operatorname{cos}\theta \end{bmatrix},
$$

represents a **rotation by an angle $\theta$ counterclockwise about the origin.**

To find the matrix representing a rotation by an angle $\theta$ *clockwise* about the origin, we replace $\theta$ with $-\theta$ in the above. This gives

$$
R_{(-\theta)} = \begin{bmatrix}\operatorname{cos}(-\theta ) & -\operatorname{sin}(-\theta ) \\ \operatorname{sin}(-\theta ) & \operatorname{cos}(-\theta )\end{bmatrix} = \begin{bmatrix}\operatorname{cos}\theta  & \operatorname{sin}\theta  \\ -\operatorname{sin}\theta  & \operatorname{cos}\theta \end{bmatrix}.
$$



### example 17592186092067 — Rotating a Vector About the Origin

The vector $\mathbf{v}=\langle -5,4 \rangle$ is rotated $135^{\circ}$ counterclockwise about the origin. Find the image of $\mathbf{v}$ under this rotation.

A rotation of $135^{\circ}$ counterclockwise about the origin is represented by the matrix 
$$
R_{135^\circ} = {\left[ \begin{array}{cc}\cos   ( {135}^{\circ } ) & - \sin   ( {135}^{\circ } ) \\ \sin   ( {135}^{\circ } ) & \cos   ( {135}^{\circ } )\end{array} \right]} = {\left[ \begin{array}{cc}- {\displaystyle \frac{1}{\sqrt{2}}} & - {\displaystyle \frac{1}{\sqrt{2}}} \\ {\displaystyle \frac{1}{\sqrt{2}}} & - {\displaystyle \frac{1}{\sqrt{2}}}\end{array} \right]}.
$$

To find the image $\mathbf{v}'$ under the action of the matrix $R_{135^{\circ}}$, we compute the matrix product, as follows:

$$
\begin{aligned}{v}^{′} & ={R}_{{135}^{∘}}\cdot v \\  & =\begin{bmatrix}-\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{bmatrix}\begin{bmatrix}-5 \\ 4\end{bmatrix} \\  & =\begin{bmatrix}\frac{1}{\sqrt{2}} \\ -\frac{9}{\sqrt{2}}\end{bmatrix}\end{aligned}
$$

Therefore, the image is $$
\displaystyle \mathbf{v}'=\left\langle \dfrac{1}{\sqrt{2}}, -\dfrac{9}{\sqrt{2}} \right\rangle.
$$

### example 17592186092068 — Interpreting a Given Matrix as a Rotation

What is the geometrical interpretation of the transformation represented by the matrix $A$ given below? 

 $$
A=
 {\left[ \begin{array}{cc}- {\displaystyle \frac{1}{\sqrt{2}}} & - {\displaystyle \frac{1}{\sqrt{2}}} \\ {\displaystyle \frac{1}{\sqrt{2}}} & - {\displaystyle \frac{1}{\sqrt{2}}}\end{array} \right]}.
$$

The rotation matrix $R_\theta$ represents a rotation of angle $\theta$ counterclockwise about the origin and is given by

$$
R = {\left[ \begin{array}{cc}\cos   \theta  & - \sin   \theta  \\ \sin   \theta  & \cos   \theta \end{array} \right]}.
$$

Comparing $A$ with the rotation matrix, we have 

$$
\left\{\begin{aligned}\operatorname{sin}⁡\theta &=\frac{1}{\sqrt{2}} \\ \operatorname{cos}⁡\theta &=-\frac{1}{\sqrt{2}}.\end{aligned}\right.
$$

Since $\sin \theta$ is positive and $\cos \theta$ is negative, we must have $\dfrac{\pi}{2} \leq \theta \leq \pi.$

Dividing the first equation by the second gives

$$
\tan \theta = -1.
$$

 

The principal value $\theta_1$ is

$$
\theta_1 = \arctan (-1) = -\dfrac{\pi}{4},
$$

but this is outside the range $\dfrac{\pi}{2} \leq \theta \leq \pi.$ To find a value in the required range, we add $\pi{:}$

$$
\theta = \theta_1 + \pi = \dfrac{3\pi}{4}
$$

Therefore, $A$ represents a rotation of $\dfrac{3\pi}{4}$ radians counterclockwise about the origin.

Note that this is also equivalent to a *clockwise* rotation with an angle of rotation given by

$$
2\pi - \dfrac{3\pi}{4} = \dfrac{5\pi}{4}.
$$

### example 17592186092069 — Rotating an Object About the Origin

A triangle $S$ has vertices at $(1,1), (3,4), (5,8).$ Which of the following are coordinates of the vertices of $S',$ the image of $S$ under a counterclockwise rotation of $\dfrac{\pi}{3}$ radians about the origin?

- $\left(1,-3\right)$

- $\big(0,\sqrt{3}\big)$

- $$
\displaystyle \left(\dfrac{5-8\sqrt{3}}{2},\dfrac{8+5\sqrt{3}}{2}\right)
$$

The rotation matrix $R_\theta$ represents a rotation of angle $\theta$ counterclockwise about the origin and is given by

$$
R = {\left[ \begin{array}{cc}\cos   \theta  & - \sin   \theta  \\ \sin   \theta  & \cos   \theta \end{array} \right]}.
$$

Substituting $\theta = \dfrac{\pi}{3}$ into the above, we have

$$
\begin{aligned}R & =\begin{bmatrix}\operatorname{cos}⁡\left(\frac{\pi }{3}\right) & -\operatorname{sin}⁡\left(\frac{\pi }{3}\right) \\ \operatorname{sin}⁡\left(\frac{\pi }{3}\right) & \operatorname{cos}⁡\left(\frac{\pi }{3}\right)\end{bmatrix} \\  & =\begin{bmatrix}\frac{1}{2} & -\frac{\sqrt{3}}{2} \\ \frac{\sqrt{3}}{2} & \frac{1}{2}\end{bmatrix} \\  & =\frac{1}{2}\begin{bmatrix}1 & -\sqrt{3} \\ \sqrt{3} & 1\end{bmatrix}.\end{aligned}
$$

To find the image of $S$ under the transformation, we first create a matrix $X$ containing all of the vertices of $S\mathbin{:}$

$$
X = 
	{\left[ \begin{array}{ccc}1 & 3 & 5 \\ 1 & 4 & 8\end{array} \right]}
$$

Now, we compute the image of $X$ under the rotation $\mathbf{R}$ by calculating the matrix product $RX\mathbin{:}$

$$
\begin{aligned}RX & =\frac{1}{2}\begin{bmatrix}1 & -\sqrt{3} \\ \sqrt{3} & 1\end{bmatrix}\begin{bmatrix}1 & 3 & 5 \\ 1 & 4 & 8\end{bmatrix} \\  & =\frac{1}{2}\begin{bmatrix}1-\sqrt{3} & 3-4\sqrt{3} & 5-8\sqrt{3} \\ 1+\sqrt{3} & 4+3\sqrt{3} & 8+5\sqrt{3}\end{bmatrix} \\  & =\begin{bmatrix}\frac{1-\sqrt{3}}{2} & \frac{3-4\sqrt{3}}{2} & \frac{5-8\sqrt{3}}{2} \\ \frac{1+\sqrt{3}}{2} & \frac{4+3\sqrt{3}}{2} & \frac{8+5\sqrt{3}}{2}\end{bmatrix}\end{aligned}
$$

Therefore, the coordinates of the respective vertices of $S'$ are 

$$
\left(\dfrac{1-\sqrt{3}}{2},\dfrac{1+\sqrt{3}}{2}\right), \quad
\left(\dfrac{3-4\sqrt{3}}{2},\dfrac{4+3\sqrt{3}}{2}\right),\quad
\left(\dfrac{5-8\sqrt{3}}{2},\dfrac{8+5\sqrt{3}}{2}\right).
$$

So, the correct answer is "III only."

## Representative practice (first three per skill; full bank in practice.json)

### Rotating a Vector About the Origin (13 captured questions)

Question 17592186092805 — question.difficulty/easy

The vector $v=⟨2,-1⟩$ is rotated $\frac{\pi }{3}$ radians counterclockwise about the origin. Find the image of $v$ under this rotation.

Solution: A rotation of $\frac{\pi }{3}$ counterclockwise about the origin is represented by the matrix 

$$
{R}_{\pi /3}=\begin{bmatrix}\operatorname{cos}⁡\left(\frac{\pi }{3}\right) & -\operatorname{sin}⁡\left(\frac{\pi }{3}\right) \\ \operatorname{sin}⁡\left(\frac{\pi }{3}\right) & \operatorname{cos}⁡\left(\frac{\pi }{3}\right)\end{bmatrix}=\begin{bmatrix}\frac{1}{2} & -\frac{\sqrt{3}}{2} \\ \frac{\sqrt{3}}{2} & \frac{1}{2}\end{bmatrix}.
$$

To find the image ${v}^{′}$ under the action of the matrix ${R}_{\pi /3}$, we compute the matrix product, as follows:

$$
\begin{aligned}{v}^{′} & ={R}_{\pi /3}\cdot v \\  & =\begin{bmatrix}\frac{1}{2} & -\frac{\sqrt{3}}{2} \\ \frac{\sqrt{3}}{2} & \frac{1}{2}\end{bmatrix}\begin{bmatrix}2 \\ -1\end{bmatrix} \\  & =\begin{bmatrix}1+\frac{\sqrt{3}}{2} \\ \sqrt{3}-\frac{1}{2}\end{bmatrix}\end{aligned}
$$

Therefore, the image is $$
\displaystyle {v}^{′}=\left\langle 1+\frac{\sqrt{3}}{2},\sqrt{3}-\frac{1}{2}\right\rangle .
$$

Answer selection: \left\langle 1+\frac{\sqrt{3}}{2},\sqrt{3}-\frac{1}{2}\right\rangle 

Question 17592186092806 — None

The vector $v = ⟨ - 1,-1⟩$ is rotated $45^{∘}$ **clockwise** about the origin. Find the image of $v$ under this rotation.

Solution: 

Question 17592186284643 — question.difficulty/easy

The vector $v=⟨4,2⟩$ is rotated ${45}^{∘}$ counterclockwise about the origin. Find the image of $v$ under this rotation.

Solution: A rotation of ${45}^{∘}$ counterclockwise about the origin is represented by the matrix 

$$
{R}_{{45}^{∘}}=\begin{bmatrix}\operatorname{cos}⁡({45}^{∘}) & -\operatorname{sin}⁡({45}^{∘}) \\ \operatorname{sin}⁡({45}^{∘}) & \operatorname{cos}⁡({45}^{∘})\end{bmatrix}=\begin{bmatrix}\frac{\sqrt{2}}{2} & -\frac{\sqrt{2}}{2} \\ \frac{\sqrt{2}}{2} & \frac{\sqrt{2}}{2}\end{bmatrix}.
$$

To find the image ${v}^{′}$ under the action of the matrix ${R}_{{45}^{∘}}$, we compute the matrix product, as follows:

$$
\begin{aligned}{v}^{′} & ={R}_{{45}^{∘}}\cdot v \\  & =\begin{bmatrix}\frac{\sqrt{2}}{2} & -\frac{\sqrt{2}}{2} \\ \frac{\sqrt{2}}{2} & \frac{\sqrt{2}}{2}\end{bmatrix}\begin{bmatrix}4 \\ 2\end{bmatrix} \\  & =\begin{bmatrix}\sqrt{2} \\ 3\sqrt{2}\end{bmatrix}\end{aligned}
$$

Therefore, the image is ${v}^{′}=⟨\sqrt{2},3\sqrt{2}⟩.$

Answer selection: ⟨\sqrt{2},3\sqrt{2}⟩

### Interpreting a Given Matrix as a Rotation (18 captured questions)

Question 17592186092829 — question.difficulty/hard

![](images/60/6086bfbba3b3b63d8f8bd728d5401481e5cd5e7b7fee5cd2bd773d808f4b44de.png)

Consider the vector $v$ shown above. Find the vector $Av$ given that 

 

$$
A=\begin{bmatrix}\frac{1}{2} & -\frac{\sqrt{3}}{2} \\ \frac{\sqrt{3}}{2} & \frac{1}{2}\end{bmatrix}.
$$

Solution: The rotation matrix ${R}_{\theta }$ represents a rotation of angle $\theta $ counterclockwise about the origin and is given by

$$
{R}_{\theta }=\begin{bmatrix}\operatorname{cos}⁡\theta  & -\operatorname{sin}⁡\theta  \\ \operatorname{sin}⁡\theta  & \operatorname{cos}⁡\theta \end{bmatrix}.
$$

Comparing $A$ with the rotation matrix, we have 

$$
\left\{\begin{aligned}\operatorname{sin}⁡\theta &=\frac{\sqrt{3}}{2} \\ \operatorname{cos}⁡\theta &=\frac{1}{2}.\end{aligned}\right.
$$

Since both $\operatorname{sin}⁡\theta $ and $\operatorname{cos}⁡\theta $ are positive we must have that $\theta $ lies in $1$st quadrant. 

Dividing the first equation by the second gives

$$
\operatorname{tan}⁡\theta =\sqrt{3}.
$$

The principal value of $\theta $ is

$$
\theta =\operatorname{arctan}⁡(\sqrt{3})=\frac{\pi }{3}.
$$

Therefore, the transformation represents a rotation of $\frac{\pi }{3}$ radians counterclockwise about the origin.

Finally, to find $Av$, we need to rotate $v$ counterclockwise by an angle of $\frac{\pi }{3}$ radians, as shown below.

![](images/87/87620581d28a4a3fd832785947ec6fc043d51841bcedd414b264121d7bf1c458.png)

Answer selection: images/6c/6c8c0257920650dcf9d92096f32cd32ea1901bb5fa0077d0d6ddc7a2f214eb24.png

Question 17592186092845 — None

What is the geometrical interpretation of the transformation represented by the matrix $A$ given below?

$$
\displaystyle A = \begin{bmatrix}-\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} \\ -\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{bmatrix}
$$

Solution: 

Question 17592186092846 — None

What is the geometrical interpretation of the transformation represented by the matrix $A$ given below?

$$
\displaystyle A = \begin{bmatrix}\frac{1}{2} & -\frac{\sqrt{3}}{2} \\ \frac{\sqrt{3}}{2} & \frac{1}{2}\end{bmatrix}
$$

Solution: 

### Rotating an Object About the Origin (12 captured questions)

Question 17592186092515 — question.difficulty/moderate

A triangle $S$ has vertices at $(-2,-2),(0,4),(2,-2).$ Which of the following are coordinates of the vertices of ${S}^{′},$ the image of $S$ under a counterclockwise rotation of ${45}^{∘}$ about the origin?

Select all that apply.

Solution: The rotation matrix ${R}_{\theta }$ represents a rotation of angle $\theta $ counterclockwise about the origin and is given by

$$
{R}_{\theta }=\begin{bmatrix}\operatorname{cos}⁡\theta  & -\operatorname{sin}⁡\theta  \\ \operatorname{sin}⁡\theta  & \operatorname{cos}⁡\theta \end{bmatrix}.
$$

Substituting $\theta ={45}^{∘}$ into the above, we have

$$
\begin{aligned}R & =\begin{bmatrix}\operatorname{cos}⁡({45}^{∘}) & -\operatorname{sin}⁡({45}^{∘}) \\ \operatorname{sin}⁡({45}^{∘}) & \operatorname{cos}⁡({45}^{∘})\end{bmatrix} \\  & =\begin{bmatrix}\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\end{bmatrix} \\  & =\frac{1}{\sqrt{2}}\begin{bmatrix}1 & -1 \\ 1 & 1\end{bmatrix}.\end{aligned}
$$

To find the image of $S$ under the transformation, we first create a matrix $X$ containing all of the vertices of $S:$

$$
\begin{aligned}X & =\begin{bmatrix}-2 & 0 & 2 \\ -2 & 4 & -2\end{bmatrix}\end{aligned}
$$

Now, we compute the image of $X$ under the rotation $R$ by calculating the matrix product $RX:$

$$
\begin{aligned}RX & =\frac{1}{\sqrt{2}}\begin{bmatrix}1 & -1 \\ 1 & 1\end{bmatrix}\begin{bmatrix}-2 & 0 & 2 \\ -2 & 4 & -2\end{bmatrix} \\  & =\frac{1}{\sqrt{2}}\begin{bmatrix}0 & -4 & 4 \\ -4 & 4 & 0\end{bmatrix} \\  & =\begin{bmatrix}0 & -2\sqrt{2} & 2\sqrt{2} \\ -2\sqrt{2} & 2\sqrt{2} & 0\end{bmatrix}\end{aligned}
$$

Therefore, the coordinates of the respective vertices of ${S}^{′}$ are 

$$
(0,-2\sqrt{2}),\,(-2\sqrt{2},2\sqrt{2}),\,(2\sqrt{2},0).
$$

So, the correct answer is “The point $(0,-2\sqrt{2})$”; “The point $(2\sqrt{2},0)$” only.

Answer The point $(0,-2\sqrt{2})$: true

Answer The point $(1,-\sqrt{3})$: false

Answer The point $(2\sqrt{2},0)$: true

Question 17592186092850 — question.difficulty/hard

A triangle $S$ has vertices at $(0,0),(2,0),(2,2).$ Which of the following are coordinates of the vertices of ${S}^{′},$ the image of $S$ under a **clockwise** rotation of $\frac{2\pi }{3}$ radians about the origin?

Select all that apply.

Solution: The rotation matrix ${R}_{\theta }$ represents a rotation of angle $\theta $ counterclockwise about the origin and is given by

$$
{R}_{\theta }=\begin{bmatrix}\operatorname{cos}⁡\theta  & -\operatorname{sin}⁡\theta  \\ \operatorname{sin}⁡\theta  & \operatorname{cos}⁡\theta \end{bmatrix}.
$$

Substituting $\theta =-\frac{2\pi }{3}$ into the above, we have

$$
\begin{aligned}R & =\begin{bmatrix}\operatorname{cos}⁡\left(-\frac{2\pi }{3}\right) & -\operatorname{sin}⁡\left(-\frac{2\pi }{3}\right) \\ \operatorname{sin}⁡\left(-\frac{2\pi }{3}\right) & \operatorname{cos}⁡\left(-\frac{2\pi }{3}\right)\end{bmatrix} \\  & =\begin{bmatrix}-\frac{1}{2} & \frac{\sqrt{3}}{2} \\ -\frac{\sqrt{3}}{2} & -\frac{1}{2}\end{bmatrix} \\  & =\frac{1}{2}\begin{bmatrix}-1 & \sqrt{3} \\ -\sqrt{3} & -1\end{bmatrix}.\end{aligned}
$$

To find the image of $S$ under the transformation, we first create a matrix $X$ containing all of the vertices of $S:$

$$
\begin{aligned}X & =\begin{bmatrix}0 & 2 & 2 \\ 0 & 0 & 2\end{bmatrix}\end{aligned}
$$

Now, we compute the image of $X$ under the rotation $R$ by calculating the matrix product $RX:$

$$
\begin{aligned}RX & =\frac{1}{2}\begin{bmatrix}-1 & \sqrt{3} \\ -\sqrt{3} & -1\end{bmatrix}\begin{bmatrix}0 & 2 & 2 \\ 0 & 0 & 2\end{bmatrix} \\  & =\frac{1}{2}\begin{bmatrix}0 & -2 & (2\sqrt{3}-2) \\ 0 & -2\sqrt{3} & (-2\sqrt{3}-2)\end{bmatrix} \\  & =\begin{bmatrix}0 & -1 & (\sqrt{3}-1) \\ 0 & -\sqrt{3} & (-\sqrt{3}-1)\end{bmatrix}\end{aligned}
$$

Therefore, the coordinates of the respective vertices of ${S}^{′}$ are 

$$
(0,0),\,(-1,-\sqrt{3}),\,(\sqrt{3}-1,-\sqrt{3}-1).
$$

So, the correct answer is “The point $(-1,-\sqrt{3})$” only.

Answer The point $(-1,-\sqrt{3})$: true

Answer The point $(2,-2)$: false

Answer The point $(\sqrt{3},0)$: false

Question 17592186253588 — question.difficulty/hard

A triangle $S$ has vertices at $(-1,-1),(-1,2),(2,-3).$ Which of the following are coordinates of the vertices of ${S}^{′},$ the image of $S$ under a **clockwise** rotation of $\frac{3\pi }{4}$ radians about the origin?

Select all that apply.

Solution: The rotation matrix ${R}_{\theta }$ represents a rotation of angle $\theta $ counterclockwise about the origin and is given by

$$
R=\begin{bmatrix}\operatorname{cos}⁡\theta  & -\operatorname{sin}⁡\theta  \\ \operatorname{sin}⁡\theta  & \operatorname{cos}⁡\theta \end{bmatrix}.
$$

Substituting $\theta =-\frac{3\pi }{4}$ into the above, we have

$$
\begin{aligned}R & =\begin{bmatrix}\operatorname{cos}⁡\left(-\frac{3\pi }{4}\right) & -\operatorname{sin}⁡\left(-\frac{3\pi }{4}\right) \\ \operatorname{sin}⁡\left(-\frac{3\pi }{4}\right) & \operatorname{cos}⁡\left(-\frac{3\pi }{4}\right)\end{bmatrix} \\  & =\begin{bmatrix}-\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} \\ -\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{bmatrix} \\  & =\frac{1}{\sqrt{2}}\begin{bmatrix}-1 & 1 \\ -1 & -1\end{bmatrix}.\end{aligned}
$$

To find the image of $S$ under the transformation, we first create a matrix $X$ containing all of the vertices of $S:$

$$
\begin{aligned}X & =\begin{bmatrix}-1 & -1 & 2 \\ -1 & 2 & -3\end{bmatrix}\end{aligned}
$$

Now, we compute the image of $X$ under the rotation $R$ by calculating the matrix product $RX:$

$$
\begin{aligned}RX & =\frac{1}{\sqrt{2}}\begin{bmatrix}-1 & 1 \\ -1 & -1\end{bmatrix}\begin{bmatrix}-1 & -1 & 2 \\ -1 & 2 & -3\end{bmatrix} \\  & =\frac{1}{\sqrt{2}}\text{ }\begin{bmatrix}0 & 3 & -5 \\ 2 & -1 & 1\end{bmatrix} \\  & =\begin{bmatrix}0 & \frac{3}{\sqrt{2}} & -\frac{5}{\sqrt{2}} \\ \sqrt{2} & -\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\end{bmatrix}\end{aligned}
$$

Therefore, the coordinates of the respective vertices of ${S}^{′}$ are 

$$
(0,\sqrt{2}),\,\left(\frac{3}{\sqrt{2}},-\frac{1}{\sqrt{2}}\right),\,\left(-\frac{5}{\sqrt{2}},\frac{1}{\sqrt{2}}\right).
$$

So, the correct answer is “The point $(0,\sqrt{2})$” only.

Answer The point $(-5,1)$: false

Answer The point $(0,\sqrt{2})$: true

Answer The point $(3,-1)$: false
