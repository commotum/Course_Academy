# 17592186050394 Calculating a Vector Projection

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186107166 — Introduction

The **vector projection** of a vector $\mathbf{a}$ onto another vector $\mathbf{b}$ is the portion that the vector $\mathbf{a}$ extends along $\mathbf{b}.$

For example, consider two vectors $\mathbf{a}$ and $\mathbf{b}$ shown below. Suppose we know that $|\mathbf{a}|=2,$ $|\mathbf{b}|=3,$ and the angle between the vectors is $\theta = \dfrac{\pi}{4}.$

![](images/a2/a28278cf12885ab7f845407ac2fa7f4ffa00dbe30849a3f8ff41f02e134ed3a0.png)

The starting point of the vector projection is $O,$ and the ending point will be the point $P$ that lies on the line containing $\mathbf{b}$ with $AP \perp \mathbf{b},$ as shown below.

![](images/f0/f0b267fb009e79eb16f86be42edc2c835808b28aa3eaf1c7e857300224ee01ec.png)

The vector $\overrightarrow{OP}$ is called the **vector projection** of $\mathbf{a}$ onto $\mathbf{b}.$ It is denoted as $\text{proj}_{\mathbf{b}}\,\mathbf{a},$ and it is computed as

$$
\begin{aligned}{\text{proj}}_{b}\,a & =OP\cdot u \\  & ={\text{comp}}_{b}\,a\cdot u\end{aligned}
$$

where $\text{comp}_{\mathbf{b}}\,\mathbf{a} = |\,\mathbf{a}\,| \cos\theta$ is the scalar projection of $\mathbf{a}$ onto $\mathbf{b}$ and $\mathbf{u}$ is a unit vector in the direction of $\mathbf{b}.$

First, we compute the scalar projection:

$$
\begin{aligned}{\text{comp}}_{b}\,a & =|\,a\,|\operatorname{cos}⁡\theta  \\  & =2\operatorname{cos}⁡\left(\frac{\pi }{4}\right) \\  & =\sqrt{2}\end{aligned}
$$

Then, we compute the unit vector that is parallel to $\mathbf{b}\mathbin{:}$

$$
\mathbf{u} = \dfrac{\mathbf{b}}{|\,\mathbf{b}\,|} = \dfrac{\mathbf{b}}{3} = \dfrac{1}{3} \mathbf{b}
$$

Therefore, the vector projection of $\mathbf{a}$ onto $\mathbf{b}$ is

$$
\begin{aligned}{\text{proj}}_{b}\,a & ={\text{comp}}_{b}\,a\cdot u \\  & =\sqrt{2}\cdot \frac{1}{3}b \\  & =\frac{\sqrt{2}}{3}b.\end{aligned}
$$



### tutorial 17592186107181 — The Direction of the Projection Vector

When finding the projection of $\mathbf{a}$ onto $\mathbf{b},$ we sometimes find that the resulting projection vector points in the opposite direction to $\mathbf{b}.$ This happens when the vector $\mathbf{a}$ extends in the direction opposite to that of $\mathbf{b}.$

![](images/0e/0e973e6f6484a9aad863ebfe89fc1ea6356d6a50844931306c6aa2b63be18a8a.png)

Consider two vectors $\mathbf{a}$ and $\mathbf{b},$ where it is known that 

$$
|\,\mathbf{a}\,|=2,\qquad |\,\mathbf{b}\,|=3,\qquad \theta = 135^\circ.
$$

Let's calculate $\textrm{proj}_{\mathbf{b}}\,\mathbf{a}.$ 

First, notice that the angle between $\mathbf a$ and $\mathbf b$ is obtuse. This means we expect the projection vector to point in the opposite direction to that of $\mathbf b.$

Next, we compute the scalar projection:

$$
\begin{aligned}{\text{comp}}_{b}\,a & =|\,a\,|\operatorname{cos}⁡\theta  \\  & =2\operatorname{cos}⁡({135}^{∘}) \\  & =2\cdot \left(-\frac{\sqrt{2}}{2}\right) \\  & =-\sqrt{2}\end{aligned}
$$

Notice that the scalar projection is negative. 

Then, we find the unit vector that is parallel to $\mathbf{b}\mathbin{:}$

$$
\mathbf{u} = \dfrac{\mathbf{b}}{|\,\mathbf{b}\,|} = \dfrac{\mathbf{b}}{3} = \dfrac{1}{3} \mathbf{b}
$$

Therefore, the vector projection of $\mathbf{a}$ onto $\mathbf{b}$ is

$$
\begin{aligned}{\text{proj}}_{b}\,a & ={\text{comp}}_{b}\,a\cdot u \\  & =-\sqrt{2}\cdot \frac{1}{3}b \\  & =-\frac{\sqrt{2}}{3}b.\end{aligned}
$$

This vector points in the direction opposite to $\mathbf{b},$ as expected.



### example 17592186105478 — Calculating a Vector Projection Using Angle and Magnitude

Suppose that $|\,\mathbf{a}\,|=8,|\,\mathbf{b}\,|=4$ and that the angle between the vectors is $\theta = \dfrac{5\pi}{6}.$ Find the vector projection of $\mathbf{a}$ onto $\mathbf{b}$ in terms of the vector $\mathbf{b}.$

First, we find the scalar projection as follows:

$$
\begin{aligned}{\text{comp}}_{b}\,a & =|\,a\,|\operatorname{cos}⁡\theta  \\  & =8\operatorname{cos}⁡\left(\frac{5\pi }{6}\right) \\  & =8\cdot \left(-\frac{\sqrt{3}}{2}\right) \\  & =-4\sqrt{3}\end{aligned}
$$

Now, we find the unit vector that is parallel to $\mathbf{b}\mathbin{:}$

$$
\mathbf{u} = \dfrac{\mathbf{b}}{|\,\mathbf{b}\,|} = \dfrac{\mathbf{b}}{4} = \dfrac{1}{4} \mathbf{b}
$$

Finally, we compute the vector projection as follows:

$$
\begin{aligned}{\text{proj}}_{b}\,a & ={\text{comp}}_{b}\,a\cdot u \\  & =-4\sqrt{3}\cdot \frac{1}{4}b \\  & =-\sqrt{3}b\end{aligned}
$$

### tutorial 17592186107167 — A General Formula

We have been using the following formula for the vector projection of $\mathbf{a}$ onto $\mathbf{b}\mathbin{:}$

$$
\text{proj}_{\mathbf{b}}\,\mathbf{a} =\text{comp}_{\mathbf{b}}\,\mathbf{a} \cdot \mathbf{u}
$$

However, we can write an alternative formula using the formula for the scalar projection:

$$
\begin{aligned}{\text{comp}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|}.\end{aligned}
$$

Substituting the above into the original formula for the vector projection, and also substituting $\mathbf{u} = \dfrac{\mathbf{b}}{| \, \mathbf{b} \, |},$ we get

$$
\begin{aligned}{\text{proj}}_{b}\,a & =\frac{a\cdot b}{|\,b\,|}\cdot \frac{b}{|\,b\,|} \\  & =\frac{a\cdot b}{|\,b\,{|}^{2}}b \\  & =\frac{a\cdot b}{b\cdot b}b.\end{aligned}
$$

Therefore, another general formula for the vector projection of $\mathbf{a}$ onto $\mathbf{b}$ is

$$
\begin{aligned}{\text{proj}}_{b}\,a & =\frac{a\cdot b}{b\cdot b}b.\end{aligned}
$$



### example 17592186105479 — Calculating a Vector Projection Using Components

Let $\mathbf{a}=\langle 1,-3,5 \rangle$ and $\mathbf{b}=\langle 5,-4,0 \rangle$. Find the vector projection of $\mathbf{a}$ onto $\mathbf{b}$.

Using the formula for the vector projection, we obtain

$$
\begin{aligned}{\text{proj}}_{b}\,a & =\frac{a\cdot b}{b\cdot b}b \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}b \\  & =\frac{1\cdot 5+(-3)\cdot (-4)+5\cdot 0}{{5}^{2}+(-4)^{2}+{0}^{2}}b \\  & =\frac{17}{41}⟨5,-4,0⟩ \\  & =\left\langle \frac{85}{41},-\frac{68}{41},0\right\rangle .\end{aligned}
$$

### tutorial 17592186107168 — Projecting Perpendicular Vectors

Notice that if two vectors $\mathbf{a}$ and $\mathbf{b}$ are perpendicular, then by projecting $\mathbf{a}$ onto $\mathbf{b}$ (or $\mathbf{b}$ onto $\mathbf{a}$), we obtain the zero vector.

For example, the projection of $\mathbf{a}$ onto a perpendicular vector $\mathbf{b}$ looks as follows:

![](images/91/9163eda36b752f1e36195b8b5a1d40bf545ec21a3988f5480d6ddcbb926c00ea.png)

Furthermore, we have the following fact:

*If $\mathbf{a}$ is a nonzero vector, its projection onto another nonzero vector $\mathbf{b}$ equals the zero vector if and only if the vectors are perpendicular.*



### example 17592186105480 — Perpendicular Vectors

Let $\mathbf{a}={\left[ \begin{array}{c}1 \\ 0 \\ 1\end{array} \right]}$ and $\mathbf{b}={\left[ \begin{array}{c}1 \\ 5 \\ - 1\end{array} \right]}$. Find the vector projection of $\mathbf{a}$ onto $\mathbf{b}$.

Using the formula for the vector projection, we obtain

$$
\begin{aligned}{\text{proj}}_{b}\,a & =\frac{a\cdot b}{b\cdot b}b \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}b \\  & =\frac{1\cdot 1+0\cdot 5+1\cdot (-1)}{{1}^{2}+{5}^{2}+(-1)^{2}}b \\  & =\frac{0}{{1}^{2}+{5}^{2}+(-1)^{2}}b \\  & =⟨0,0,0⟩.\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Calculating a Vector Projection Using Angle and Magnitude (17 captured questions)

Question 17592186106111 — question.difficulty/easy

Suppose that $|\,a\,|=8$, $|\,b\,|=2$ and that the angle between the vectors is $\theta ={120}^{∘}.$ Find the vector projection of $a$ onto $b$ in terms of the vector $b.$

Solution: First, we find the scalar projection as follows:

$$
\begin{aligned}{\text{comp}}_{b}\,a & =|\,a\,|\operatorname{cos}⁡\theta  \\  & =8\operatorname{cos}⁡({120}^{∘}) \\  & =8\cdot \left(-\frac{1}{2}\right) \\  & =-4\end{aligned}
$$

Now, we find the unit vector that is parallel to $b:$

$$
u=\frac{b}{|\,b\,|}=\frac{b}{2}=\frac{1}{2}b
$$

Finally, we compute the vector projection as follows:

$$
\begin{aligned}{\text{proj}}_{b}\,a & ={\text{comp}}_{b}\,a\cdot u \\  & =(-4)\cdot \frac{1}{2}b \\  & =-2b\end{aligned}
$$

Answer selection: -2b

Question 17592186106480 — question.difficulty/moderate

Suppose that $|\,c\,|=12$, $|\,d\,|=6$ and that the angle between the vectors is $\theta =\frac{2\pi }{3}.$ Find the vector projection of $d$ onto $c$ in terms of the vector $c.$

Solution: First, we find the scalar projection as follows:

$$
\begin{aligned}{\text{comp}}_{c}\,d & =|\,d\,|\operatorname{cos}⁡\theta  \\  & =6\operatorname{cos}⁡\left(\frac{2\pi }{3}\right) \\  & =6\cdot \left(-\frac{1}{2}\right) \\  & =-3\end{aligned}
$$

Now, we find the unit vector that is parallel to $c:$

$$
u=\frac{c}{|\,c\,|}=\frac{c}{12}=\frac{1}{12}c
$$

Finally, we compute the vector projection as follows:

$$
\begin{aligned}{\text{proj}}_{c}\,d & ={\text{comp}}_{c}\,d\cdot u \\  & =(-3)\cdot \frac{1}{12}c \\  & =-\frac{1}{4}c\end{aligned}
$$

Answer selection: -\frac{1}{4}c

Question 17592186287856 — question.difficulty/easy

Suppose that $|\,a\,|=6$, $|\,b\,|=2$ and that the angle between the vectors is $\theta =\frac{\pi }{3}.$ Find the vector projection of $a$ onto $b$ in terms of the vector $b.$

Solution: First, we find the scalar projection as follows:

$$
\begin{aligned}{\text{comp}}_{b}\,a & =|\,a\,|\operatorname{cos}⁡\theta  \\  & =6\operatorname{cos}⁡\left(\frac{\pi }{3}\right) \\  & =6\cdot \frac{1}{2} \\  & =3\end{aligned}
$$

Now, we find the unit vector that is parallel to $b:$

$$
u=\frac{b}{|\,b\,|}=\frac{b}{2}=\frac{1}{2}b
$$

Finally, we compute the vector projection as follows:

$$
\begin{aligned}{\text{proj}}_{b}\,a & ={\text{comp}}_{b}\,a\cdot u \\  & =3\cdot \frac{1}{2}b \\  & =\frac{3}{2}b\end{aligned}
$$

Answer selection: \frac{3}{2}b

### Calculating a Vector Projection Using Components (28 captured questions)

Question 17592186106025 — question.difficulty/moderate

Let $a = ⟨2,-4, 0⟩$ and $b = ⟨9, 7, 7⟩$. Find the vector projection of $b$ onto $a$.

Solution: 

Question 17592186106039 — question.difficulty/easy

Let $$
\displaystyle c=\begin{bmatrix}8 \\ -2 \\ -1\end{bmatrix}
$$ and $$
\displaystyle d=\begin{bmatrix}3 \\ -1 \\ -2\end{bmatrix}.
$$ Find the vector projection of $c$ onto $d.$

Solution: Using the formula for the vector projection, we obtain

$$
\begin{aligned}{\text{proj}}_{d}\,c & =\frac{c\cdot d}{d\cdot d}d \\  & =\frac{{c}_{x}{d}_{x}+{c}_{y}{d}_{y}+{c}_{z}{d}_{z}}{{d}_{x}^{2}+{d}_{y}^{2}+{d}_{z}^{2}}d \\  & =\frac{8\cdot 3+(-2)\cdot (-1)+(-1)\cdot (-2)}{{3}^{2}+(-1)^{2}+(-2)^{2}}d \\  & =\frac{28}{14}⟨3,-1,-2⟩ \\  & =2⟨3,-1,-2⟩ \\  & =⟨6,-2,-4⟩.\end{aligned}
$$

Answer selection: ⟨6,-2,-4⟩

Question 17592186237848 — question.difficulty/easy

Let $a=\begin{bmatrix}9 \\ 7 \\ -4\end{bmatrix}$ and $b=\begin{bmatrix}0 \\ 2 \\ 3\end{bmatrix}.$ Find the vector projection of $a$ onto $b.$

Solution: Using the formula for the vector projection, we obtain 

$$
\begin{aligned}{\text{proj}}_{b}\,a & =\frac{a\cdot b}{b\cdot b}b \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}b \\  & =\frac{9\cdot 0+7\cdot 2+(-4)\cdot 3}{{0}^{2}+{2}^{2}+{3}^{2}}b \\  & =\frac{2}{13}⟨0,2,3⟩ \\  & =\left\langle 0,\frac{4}{13},\frac{6}{13}\right\rangle .\end{aligned}
$$

Answer selection: \left\langle 0,\frac{4}{13},\frac{6}{13}\right\rangle 

### Perpendicular Vectors (28 captured questions)

Question 17592186106172 — question.difficulty/moderate

Let $a=\begin{bmatrix}-4 \\ 4 \\ 1\end{bmatrix}$ and $b=\begin{bmatrix}4 \\ -1 \\ x\end{bmatrix}.$ Given that the projection of $a$ onto $b$ is the zero vector, find the value of $x.$

Solution: Since $a$ is a nonzero vector, its projection onto another nonzero vector $b$ equals the zero vector only when the vectors are perpendicular. 

So, we must have

$$
a⊥b\,⟹\,a\cdot b=0.
$$

Computing the dot product, we obtain

$$
\begin{aligned}a\cdot b & ={a}_{x}\cdot {b}_{x}+{a}_{y}\cdot {b}_{y}+{a}_{z}\cdot {b}_{z} \\  & =-4\cdot 4+4\cdot (-1)+1\cdot x \\  & =x-20.\end{aligned}
$$

Setting the dot product equal to $0,$ we get

$$
\begin{aligned}a\cdot b & =0 \\ x-20 & =0 \\ x & =20.\end{aligned}
$$

Answer selection: 20

Question 17592186106479 — question.difficulty/easy

Let $a=⟨1,-2,5⟩$ and $b=⟨3,-1,-1⟩.$ Find the vector projection of $a$ onto $b.$

Solution: Using the formula for the vector projection, we obtain

$$
\begin{aligned}{\text{proj}}_{b}\,a & =\frac{a\cdot b}{b\cdot b}b \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}b \\  & =\frac{1\cdot 3+(-2)\cdot (-1)+5\cdot (-1)}{{3}^{2}+(-1)^{2}+(-1)^{2}}b \\  & =\frac{0}{{3}^{2}+(-1)^{2}+(-1)^{2}}b \\  & =⟨0,0,0⟩.\end{aligned}
$$

Answer selection: ⟨0,0,0⟩

Question 17592186290292 — question.difficulty/moderate

Let $a=⟨1,2,3⟩$ and $b=⟨2,-3,x⟩.$ Given that the projection of $a$ onto $b$ is the zero vector, find the value of $x.$

Solution: Since $a$ is a nonzero vector, its projection onto another nonzero vector $b$ equals the zero vector only when the vectors are perpendicular. 

So, we must have

$$
a⊥b\,⟹\,a\cdot b=0.
$$

Computing the dot product, we obtain

$$
\begin{aligned}a\cdot b & ={a}_{x}\cdot {b}_{x}+{a}_{y}\cdot {b}_{y}+{a}_{z}\cdot {b}_{z} \\  & =1\cdot 2+2\cdot (-3)+3\cdot x \\  & =3x-4.\end{aligned}
$$

Setting the dot product equal to $0,$ we get

$$
\begin{aligned}a\cdot b & =0 \\ 3x-4 & =0 \\ 3x & =4 \\ x & =\frac{4}{3}.\end{aligned}
$$

Answer selection: \frac{4}{3}
