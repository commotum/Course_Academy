# 17592186049653 Calculating a Scalar Projection

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186107174 — Introduction

The **scalar projection** of a vector $\mathbf{a}$ onto another vector $\mathbf{b}$ is the distance that the vector $\mathbf{a}$ extends in the direction of $\mathbf{b}.$

For example, consider two vectors $\mathbf{a}$ and $\mathbf{b}$ shown below. Suppose we know that $|\,\mathbf{a}\,|=2$ and that the angle between the vectors is $\theta = \dfrac{\pi}{4}.$

![](images/a2/a28278cf12885ab7f845407ac2fa7f4ffa00dbe30849a3f8ff41f02e134ed3a0.png)

To illustrate the projection of $\mathbf{a}$ along $\mathbf{b},$ consider the point $P$ on the line that contains $\mathbf{b}$ with $AP \perp \mathbf{b},$ as shown below.

![](images/fd/fd37bdb2a97b4125fb360990d3c4a36b48bcb50433de033a154799db00e474dd.png)

The length $OP$ is called the **scalar projection** of $\mathbf{a}$ onto $\mathbf{b}$ (or the **component** of $\mathbf{a}$ along $\mathbf{b}$). It is denoted as $\text{comp}_{\mathbf{b}}\,\mathbf{a},$ and we can compute it using cosine in $\triangle OPA$ as follows:

$$
\begin{aligned}{\text{comp}}_{\mathbf{b}}\hspace{0.167em}\mathbf{a} & =OP \\  & =|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\operatorname{cos}\theta  \\  & =2\operatorname{cos}\left(\frac{\pi }{4}\right) \\  & =2\cdot \frac{\sqrt{2}}{2} \\  & =\sqrt{2}\end{aligned}
$$

This formula is the general definition of the scalar projection:

$$
\text{comp}_{\mathbf{b}}\,\mathbf{a}= |\,\mathbf{a}\,| \cos\theta
$$



### tutorial 17592186107177 — Negative Scalar Projections

The scalar projection of $\mathbf{a}$ onto $\mathbf{b}$ can be negative. This happens when the vector $\mathbf{a}$ extends in the direction opposite to that of $\mathbf{b}.$

![](images/c1/c19648ea2df1935e89e10df2f7f5ab33ad537a5fdb52bb97c3555c9a0365701e.png)

For example, consider two vectors $\mathbf{a}$ and $\mathbf{b},$ where it is known that 

$$
|\,\mathbf{a}\,|=2, \qquad \theta = 135^\circ.
$$

Notice that the angle $\theta$ between the vectors is obtuse. 

Computing the scalar projection of $\mathbf a$ onto $\mathbf b$ using the formula, we obtain 

$$
\begin{aligned}{\text{comp}}_{\mathbf{b}}\hspace{0.167em}\mathbf{a} & =|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\operatorname{cos}\theta  \\  & =2\operatorname{cos}({135}^{∘}) \\  & =2\cdot \left(-\frac{\sqrt{2}}{2}\right) \\  & =-\sqrt{2}.\end{aligned}
$$

In general, if $90^\circ < \theta \leq 180^\circ,$ then $\cos\theta <0$ and the scalar projection will be negative.



### example 17592186105488 — Calculating a Scalar Projection Using Angles and Magnitudes

Suppose $|\,\mathbf{a}\,|=13$ and the angle between vectors $\mathbf{a}$ and $\mathbf{b}$ is $\theta = \dfrac{2\pi}{3}.$ Find the scalar projection of $\mathbf{a}$ onto $\mathbf{b}.$

Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{\mathbf{b}}\hspace{0.167em}\mathbf{a} & =|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\operatorname{cos}\theta  \\  & =13\operatorname{cos}\left(\frac{2\pi }{3}\right) \\  & =13\cdot \left(-\frac{1}{2}\right) \\  & =-\frac{13}{2}.\end{aligned}
$$

### tutorial 17592186107175 — Deriving a General Formula

We have been using the following formula for the scalar projection of $\mathbf{a}$ onto $\mathbf{b}\mathbin{:}$

$$
\text{comp}_{\mathbf{b}}\,\mathbf{a}= |\,\mathbf{a}\,| \cos\theta
$$

However, sometimes we are not given the angle between two vectors. In such cases, we can solve for $\cos \theta$ in terms of the dot product:

$$
\begin{aligned}\mathbf{a}\cdot \mathbf{b} & =|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\hspace{0.167em}|\hspace{0.167em}\mathbf{b}\hspace{0.167em}|\operatorname{cos}\theta  \\ \operatorname{cos}\theta  & =\frac{\mathbf{a}\cdot \mathbf{b}}{|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\hspace{0.167em}|\hspace{0.167em}\mathbf{b}\hspace{0.167em}|}\end{aligned}
$$

Substituting this into our original formula, we get

$$
\begin{aligned}{\text{comp}}_{\mathbf{b}}\hspace{0.167em}\mathbf{a} & =|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\operatorname{cos}\theta  \\  & =|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\cdot \frac{\mathbf{a}\cdot \mathbf{b}}{|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\hspace{0.167em}|\hspace{0.167em}\mathbf{b}\hspace{0.167em}|} \\  & =\frac{\mathbf{a}\cdot \mathbf{b}}{|\hspace{0.167em}\mathbf{b}\hspace{0.167em}|}.\end{aligned}
$$

Therefore, another general formula for the scalar projection of $\mathbf{a}$ onto $\mathbf{b}$ is

$$
\begin{aligned}{\text{comp}}_{\mathbf{b}}\hspace{0.167em}\mathbf{a} & =\frac{\mathbf{a}\cdot \mathbf{b}}{|\hspace{0.167em}\mathbf{b}\hspace{0.167em}|}.\end{aligned}
$$



### example 17592186105489 — Calculating a Scalar Projection Using Components

Let $\mathbf{a}=\langle 3,3,-1 \rangle$ and $\mathbf{b}=\langle 2,-7,0 \rangle.$ Find the scalar projection of $\mathbf{a}$ onto $\mathbf{b}.$

Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{\mathbf{b}}\hspace{0.167em}\mathbf{a} & =\frac{\mathbf{a}\cdot \mathbf{b}}{|\hspace{0.167em}\mathbf{b}\hspace{0.167em}|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{3\cdot 2+3\cdot (-7)+(-1)\cdot 0}{\sqrt{{2}^{2}+(-7)^{2}+{0}^{2}}} \\  & =-\frac{15}{\sqrt{53}}.\end{aligned}
$$

### tutorial 17592186107176 — Projecting Perpendicular Vectors

Notice that if two vectors $\mathbf{a}$ and $\mathbf{b}$ are perpendicular, then the scalar projection of $\mathbf{a}$ onto $\mathbf{b}$ (or $\mathbf{b}$ onto $\mathbf{a}$) is equal to $0.$

For example, consider the following illustration. Notice that, since $\mathbf{a} \perp \mathbf{b},$ the vector $\mathbf{a}$ doesn't extend in the direction of $\mathbf{b}$ at all. So, the scalar projection of $\mathbf{a}$ onto $\mathbf{b}$ is $0.$

![](images/ef/efb79d8645a5df54d76c0199335aad61b258e400a98dc485ccd8b3abc8e0ba8d.png)

Furthermore, we have the following fact:

*If $\mathbf{a}$ is a nonzero vector, its scalar projection onto another nonzero vector $\mathbf{b}$ equals $0$ if and only if the vectors are perpendicular.*



### example 17592186105490 — Projecting a Vector Onto a Perpendicular Vector

Let $\mathbf{a}={\left[ \begin{array}{c}0 \\ 0 \\ 1\end{array} \right]}$ and $\mathbf{b}={\left[ \begin{array}{c}2 \\ - 4 \\ 0\end{array} \right]}.$ Find the scalar projection of $\mathbf{a}$ onto $\mathbf{b}.$

Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{\mathbf{b}}\hspace{0.167em}\mathbf{a} & =\frac{\mathbf{a}\cdot \mathbf{b}}{|\hspace{0.167em}\mathbf{b}\hspace{0.167em}|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{c}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{0\cdot 2+0\cdot (-4)+1\cdot 0}{\sqrt{{2}^{2}+(-4)^{2}+{0}^{2}}} \\  & =\frac{0}{\sqrt{{2}^{2}+(-4)^{2}+{0}^{2}}} \\  & =0.\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Calculating a Scalar Projection Using Angles and Magnitudes (37 captured questions)

Question 17592186106110 — None

Suppose $\mid c|= 14$ and the angle between vectors $c$ and $d$ is $θ = 60^{∘}$. Find the scalar projection of $c$ onto $d$.

Solution: Use the scalar-projection formula:

$$
\operatorname{comp}_{d}c=|c|\cos\theta=14\cos60^\circ=14\left(\frac12\right)=7.
$$

Answer selection: 7

Question 17592186106478 — question.difficulty/easy

Suppose $|\hspace{0.167em}\mathbf{c}\hspace{0.167em}|=18$ and the angle between vectors $\mathbf{c}$ and $\mathbf{d}$ is $\theta =\frac{3\pi }{4}.$ Find the scalar projection of $\mathbf{c}$ onto $\mathbf{d}.$

Solution: Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{\mathbf{d}}\hspace{0.167em}\mathbf{c} & =|\hspace{0.167em}\mathbf{c}\hspace{0.167em}|\operatorname{cos}\theta  \\  & =18\operatorname{cos}\left(\frac{3\pi }{4}\right) \\  & =18\cdot \left(-\frac{\sqrt{2}}{2}\right) \\  & =-9\sqrt{2}.\end{aligned}
$$

Answer selection: -9\sqrt{2}

Question 17592186237842 — question.difficulty/easy

Suppose $|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|=14$ and the angle between vectors $\mathbf{a}$ and $\mathbf{b}$ is $\theta =\frac{2\pi }{3}.$ Find the scalar projection of $\mathbf{a}$ onto $\mathbf{b}.$

Solution: Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{\mathbf{b}}\hspace{0.167em}\mathbf{a} & =|\hspace{0.167em}\mathbf{a}\hspace{0.167em}|\operatorname{cos}\theta  \\  & =14\operatorname{cos}\left(\frac{2\pi }{3}\right) \\  & =14\cdot \left(-\frac{1}{2}\right) \\  & =-7.\end{aligned}
$$

Answer selection: -7

### Calculating a Scalar Projection Using Components (38 captured questions)

Question 17592186106038 — None

Let $c = ⟨2, 1, 2⟩$ and $d = ⟨ - 1, 2, 2⟩$. Find $comp_{d}c + comp_{c}d$.

Solution: The scalar projections are

$$
\operatorname{comp}_{d}c=\frac{c\cdot d}{|d|},
\qquad \operatorname{comp}_{c}d=\frac{d\cdot c}{|c|}.
$$

Here $c\cdot d=-2+2+4=4$, while $|c|=|d|=3$. Therefore

$$
\operatorname{comp}_{d}c+\operatorname{comp}_{c}d=\frac43+\frac43=\frac83.
$$

Answer selection: \frac{8}{3}

Question 17592186106098 — question.difficulty/easy

Let $\mathbf{p}=⟨\sqrt{2},1,-1⟩$ and $\mathbf{q}=⟨\sqrt{8},-\sqrt{3},1⟩.$ Find the scalar projection of $\mathbf{p}$ onto $\mathbf{q}.$

Solution: Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{\mathbf{q}}\hspace{0.167em}\mathbf{p} & =\frac{\mathbf{p}\cdot \mathbf{q}}{|\hspace{0.167em}\mathbf{q}\hspace{0.167em}|} \\  & =\frac{{p}_{x}{q}_{x}+{p}_{y}{q}_{y}+{p}_{z}{q}_{z}}{\sqrt{{q}_{x}^{2}+{q}_{y}^{2}+{q}_{z}^{2}}} \\  & =\frac{\sqrt{2}\cdot \sqrt{8}+1\cdot (-\sqrt{3})+(-1)\cdot 1}{\sqrt{(\sqrt{8})^{2}+(-\sqrt{3})^{2}+{1}^{2}}} \\  & =\frac{3-\sqrt{3}}{\sqrt{12}} \\  & =\frac{3-\sqrt{3}}{2\sqrt{3}} \\  & =\frac{\sqrt{3}-1}{2}.\end{aligned}
$$

Answer selection: \frac{\sqrt{3}-1}{2}

Question 17592186237844 — question.difficulty/easy

Let $\mathbf{a}=⟨3,-1,-1⟩$ and $\mathbf{b}=⟨4,4,2⟩.$ Find the scalar projection of $\mathbf{a}$ onto $\mathbf{b}.$

Solution: Using the formula for the scalar projection, we obtain

$$
\begin{aligned}{\text{comp}}_{\mathbf{b}}\hspace{0.167em}\mathbf{a} & =\frac{\mathbf{a}\cdot \mathbf{b}}{|\hspace{0.167em}\mathbf{b}\hspace{0.167em}|} \\  & =\frac{{a}_{x}{b}_{x}+{a}_{y}{b}_{y}+{a}_{z}{b}_{z}}{\sqrt{{b}_{x}^{2}+{b}_{y}^{2}+{b}_{z}^{2}}} \\  & =\frac{3\cdot 4+(-1)\cdot 4+(-1)\cdot 2}{\sqrt{{4}^{2}+{4}^{2}+{2}^{2}}} \\  & =\frac{6}{\sqrt{36}} \\  & =1.\end{aligned}
$$

Answer selection: 1

### Projecting a Vector Onto a Perpendicular Vector (27 captured questions)

Question 17592186106213 — question.difficulty/moderate

Let $\mathbf{p}=⟨-1,1,2⟩$ and $\mathbf{q}=⟨4,x,1⟩.$ Given that the scalar projection of $\mathbf{p}$ onto $\mathbf{q}$ is zero, find the value of $x.$

Solution: Since $\mathbf{p}$ is a nonzero vector, its scalar projection onto another nonzero vector $\mathbf{q}$ equals zero only when the vectors are perpendicular. 

So, we must have

$$
\mathbf{p}⊥\mathbf{q}\hspace{2em}⟹\hspace{2em}\mathbf{p}\cdot \mathbf{q}=0.
$$

Computing the dot product, we obtain

$$
\begin{aligned}\mathbf{p}\cdot \mathbf{q} & ={p}_{x}\cdot {q}_{x}+{p}_{y}\cdot {q}_{y}+{p}_{z}\cdot {q}_{z} \\  & =(-1)\cdot 4+1\cdot x+2\cdot 1 \\  & =x-2.\end{aligned}
$$

Setting the dot product equal to $0,$ we get

$$
\begin{aligned}\mathbf{p}\cdot \mathbf{q} & =0 \\ x-2 & =0 \\ x & =2.\end{aligned}
$$

Answer selection: 2

Question 17592186106214 — question.difficulty/moderate

Let $\mathbf{p}=\begin{bmatrix}6 \\ 1 \\ 4\end{bmatrix}$ and $\mathbf{q}=\begin{bmatrix}x \\ 4 \\ -4\end{bmatrix}.$ Given that the scalar projection of $\mathbf{p}$ onto $\mathbf{q}$ is $0,$ find the value of $x.$

Solution: Since $\mathbf{p}$ is a nonzero vector, its scalar projection onto another nonzero vector $\mathbf{q}$ equals zero only when the vectors are perpendicular. 

So, we must have

$$
\mathbf{p}⊥\mathbf{q}\hspace{2em}⟹\hspace{2em}\mathbf{p}\cdot \mathbf{q}=0.
$$

Computing the dot product, we obtain

$$
\begin{aligned}\mathbf{p}\cdot \mathbf{q} & ={p}_{x}\cdot {q}_{x}+{p}_{y}\cdot {q}_{y}+{p}_{z}\cdot {q}_{z} \\  & =6\cdot x+1\cdot 4+4\cdot (-4) \\  & =6x-12.\end{aligned}
$$

Setting the dot product equal to $0,$ we get

$$
\begin{aligned}\mathbf{p}\cdot \mathbf{q} & =0 \\ 6x-12 & =0 \\ 6x & =12 \\ x & =2.\end{aligned}
$$

Answer selection: 2

Question 17592186290486 — question.difficulty/moderate

Let $\mathbf{p}=\begin{bmatrix}-2 \\ 0 \\ 5\end{bmatrix}$ and $\mathbf{q}=\begin{bmatrix}15 \\ \sqrt{2} \\ x\end{bmatrix}.$ Given that the scalar projection of $\mathbf{p}$ onto $\mathbf{q}$ is $0,$ find the value of $x.$

Solution: Since $\mathbf{p}$ is a nonzero vector, its scalar projection onto another nonzero vector $\mathbf{q}$ equals zero only when the vectors are perpendicular. 

So, we must have

$$
\mathbf{p}⊥\mathbf{q}\hspace{2em}⟹\hspace{2em}\mathbf{p}\cdot \mathbf{q}=0.
$$

Computing the dot product, we obtain

$$
\begin{aligned}\mathbf{p}\cdot \mathbf{q} & ={p}_{x}\cdot {q}_{x}+{p}_{y}\cdot {q}_{y}+{p}_{z}\cdot {q}_{z} \\  & =(-2)\cdot 15+0\cdot \sqrt{2}+5\cdot x \\  & =5x-30.\end{aligned}
$$

Setting the dot product equal to $0,$ we get

$$
\begin{aligned}\mathbf{p}\cdot \mathbf{q} & =0 \\ 5x-30 & =0 \\ 5x & =30 \\ x & =6.\end{aligned}
$$

Answer selection: 6
