# 17592186049360 Unit Vectors

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186097833 — Introduction

A **unit vector** is a vector whose magnitude is equal to $1.$ 

Given any vector $\mathbf a$, we can create a unit vector $\mathbf u$ by dividing $\mathbf a$ by its magnitude $|\, \mathbf{a} \,|,$ as follows:

$$
\mathbf{u} = \dfrac{ \mathbf{a} }{ |\,\mathbf{a}\,| }
$$

For example, if $|\,\mathbf{a}\,|=2,$ then the unit vector is

$$
\mathbf{u} = \dfrac{\mathbf{a}}{2} = \dfrac{1}{2} \mathbf{a}.
$$

![](images/c7/c78d5b75c1d5928e7b269a4a67229487b3d3324e9815b11c5fd1f47f63437d82.png)



### example 17592186096447 — Finding a Unit Vector Parallel to a Given Vector

The vector $\mathbf{a}$ has magnitude $3$. Find a unit vector that is parallel to $\mathbf{a}$.

To obtain the unit vector that is parallel to $\mathbf{a}$, we divide $\mathbf{a}$ by its length:

$$
\mathbf{u}=\dfrac{\mathbf{a}}{\mid \,\mathbf{a}\, \mid}=\dfrac{1}{3}\mathbf{a}
$$

### example 17592186096493 — Finding a Unit Vector Parallel to a Given Vector in a Diagram

![](images/d3/d3042242136b82b867b8bd7911761ee38318924df0c9979488d20f04117c45d9.png)

Consider the picture shown above. Find a unit vector that is parallel to $\mathbf a$.

![](images/b3/b316448c885a20a7ed60871ce0f1a4dc4f77bd4658dc6eda3407fb3c89a088cb.png)

In $\bigtriangleup AHB$ we have

$$
\angle AHB = 90^\circ
$$

, $AH=3$ and $BH=2$. So, the Pythagorean theorem gives

$$
\begin{aligned}
AB &= \sqrt{AH^{2} + BH^{2}} \\
&= \sqrt{3^{2} + 2^{2}} \\
&= \sqrt{9 + 4} \\
&= \sqrt{13}
\end{aligned}
$$

Hence, the magnitude of $\mathbf{a}$ is $\sqrt{13}$. Consequently, the unit vector is

$$
\begin{aligned}
u &= \frac{1}{\mid a \mid} \cdot a \\
&= \frac{1}{\sqrt{13}}a
\end{aligned}
$$

### example 17592186096448 — Finding a Unit Vector Parallel to a Vector Sum

The vector $\mathbf{a}$ is directed horizontally to the right and has magnitude $10$, while the vector $\mathbf{b}$ is directed vertically down and has magnitude $20$. Find a unit vector that is parallel to $\mathbf{a+b}$.

First, we have to find $\mathbf{a+b}$. According to the triangle law of addition, the resultant $\mathbf{a}+\mathbf{b}$ goes from the tail of $\mathbf{a}$ to the head of $\mathbf{b}$:

![](images/32/32c48d8c19fc68fbc172b240ded922f3e2ebc12804411c318ff63fe999aaedcc.png)

To find the unit vector corresponding to $\mathbf{a+b}$, we have to divide by the magnitude:

$$
\begin{aligned}
u &= \frac{a + b}{\mid a + b \mid}
\end{aligned}
$$

To find the magnitude, first notice that we obtain a right triangle. So, we can use the Pythagorean theorem:

$$
\begin{aligned}{|\mathbf{a}\mathbf{+}\mathbf{b}|}^{2} & ={|\mathbf{a}|}^{2}+{|\mathbf{b}|}^{2} \\  & ={10}^{2}+{20}^{2} \\  & =100+400 \\  & =500\end{aligned}
$$

Therefore, the magnitude is

$$
\begin{aligned}
\mid \mathbf{a+b} &= \sqrt{500}=10\sqrt{5}
\end{aligned}
$$

and the corresponding unit vector is

$$
\begin{aligned}
u &= \frac{a + b}{\mid a + b \mid} \\
&= \frac{1}{10\sqrt{5}}(a + b)
\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Finding a Unit Vector Parallel to a Given Vector (26 captured questions)

Question 17592186096969 — None

The vector $a$ has magnitude $5$. Find a unit vector that is parallel to $a$.

Solution: Divide the vector by its magnitude:

$$
\widehat a=\frac{a}{|a|}=\frac15a.
$$

Its magnitude is $\frac15|a|=1$, and the positive scalar multiple has the same direction as $a$.

Answer selection: \frac{1}{5}a

Question 17592186097045 — None

The vector $\overrightarrow{AB}$ has magnitude $7$. Which of the following is a unit vector that is parallel to $\overrightarrow{AB}$?

Solution: A unit vector in the direction of $\overrightarrow{AB}$ is obtained by dividing by its magnitude:

$$
\frac{\overrightarrow{AB}}{|\overrightarrow{AB}|}=\frac17\overrightarrow{AB}.
$$

Its magnitude is $\frac17(7)=1$.

Answer selection: \frac{1}{7}\overrightarrow{AB}

Question 17592186502222 — question.difficulty/easy

The vector $\overrightarrow{AB}$ has magnitude $30$. Which of the following is a unit vector that is parallel to $\overrightarrow{AB}$?

Solution: To obtain the unit vector that is parallel to $\overrightarrow{AB}$, we divide $\overrightarrow{AB}$ by its length:

$$
\mathbf{u}=\dfrac{\overrightarrow{AB}}{\mid \,\overrightarrow{AB}\, \mid}=\dfrac{1}{30}\overrightarrow{AB}
$$

Answer selection: \frac{1}{30}\overrightarrow{AB}

### Finding a Unit Vector Parallel to a Given Vector in a Diagram (24 captured questions)

Question 17592186097161 — question.difficulty/hard

![](images/9d/9dfaf74a497a2fd22428e09a4c26d573e184c9728ccf67f11ebb9d6a2a44f4c6.png)

Consider the picture above. Which of the following is a unit vector that is parallel to $q + r$?

Solution: The scale shows that two grid squares represent one unit. Reading the displacements from the diagram gives

$$
q=\left\langle\frac52,-\frac32\right\rangle,
\qquad r=\left\langle\frac32,3\right\rangle.
$$

Thus $q+r=\left\langle4,\frac32\right\rangle$ and

$$
|q+r|=\sqrt{4^2+\left(\frac32\right)^2}=\frac{\sqrt{73}}2.
$$

The required unit vector is

$$
\frac{q+r}{|q+r|}=\frac{2(q+r)}{\sqrt{73}}.
$$

Answer selection: (2(q + r))/(\sqrt{73})

Question 17592186097177 — question.difficulty/moderate

![](images/13/1319298a994d5daf26853baf7d255490827ada4123debdf0b4374db1ed03f7af.png)

Consider the picture shown above. Find a unit vector that is parallel to $c$.

Solution: The scale shows that two grid squares represent one unit. The vector moves four grid squares right and seven down, so

$$
c=\left\langle2,-\frac72\right\rangle,
\qquad |c|=\sqrt{2^2+\left(-\frac72\right)^2}=\frac{\sqrt{65}}2.
$$

Dividing by the magnitude gives

$$
\frac{c}{|c|}=\frac{2c}{\sqrt{65}}.
$$

Answer selection: \frac{2}{\sqrt{65}}c

Question 17592186233276 — question.difficulty/hard

![](images/95/95c30eab094a24beb6976262167401efa973dbac12781c69d074eb14e12e2743.png)

Consider the picture above. Which of the following is a unit vector that is parallel to $\mathbf{m}+\mathbf{n}?$

Solution: First, we have to find $m+n.$ According to the triangle law of addition, the resultant $m+n$ goes from the tail of $m$ to the head of $n:$ 

![](images/87/87647211f77776c5f5f740c205fafb150eef1b9d3ebefb82df73a9fdcd953bdb.png)

In $△AHB$, we have $∠AHB={90}^{∘}$, $AH=0.5=\frac{1}{2}$ and $BH=2.$ So, the Pythagorean theorem gives

$$
\begin{aligned}|m+n| & =AB \\  & =\sqrt{A{H}^{2}+B{H}^{2}} \\  & =\sqrt{{\left(\frac{1}{2}\right)}^{2}+{2}^{2}} \\  & =\sqrt{\frac{1}{4}+4} \\  & =\frac{\sqrt{17}}{2}.\end{aligned}
$$

Hence, the magnitude of $m+n$ is $\frac{\sqrt{17}}{2}.$ Consequently, the unit vector is

$$
\begin{aligned}u & =\frac{1}{|m+n|}\cdot (m+n) \\  & =\frac{2}{\sqrt{17}}(m+n).\end{aligned}
$$

Answer selection: \frac{2}{\sqrt{17}}(m+n)

### Finding a Unit Vector Parallel to a Vector Sum (27 captured questions)

Question 17592186097042 — question.difficulty/moderate

The vector $\mathbf{a}$ is directed horizontally to the right and has magnitude $3$, while the vector $\mathbf{b}$ is directed vertically down and has magnitude $4$. Which of the following is a unit vector that is parallel to $a + b$?

> A scientific calculator is required to answer this question.

Solution: The horizontal and vertical vectors are perpendicular, so

$$
|a+b|=\sqrt{3^2+4^2}=5.
$$

Dividing by this magnitude gives the required unit vector:

$$
\frac{a+b}{|a+b|}=\frac15(a+b).
$$

Answer selection: \frac{1}{5}(a + b)

Question 17592186097043 — None

The vector $a$ is directed due north-east and $\mid a|= 20$, while the vector $b$ is directed due south-east and $\mid b|= 13$. Which of the following is a unit vector that is parallel to $a + b$?

> A scientific calculator is required to answer this question.

Solution: North-east and south-east directions are perpendicular. Hence

$$
|a+b|=\sqrt{20^2+13^2}=\sqrt{569}.
$$

The unit vector in the direction of $a+b$ is

$$
\frac{a+b}{\sqrt{569}}.
$$

Answer selection: \frac{1}{\sqrt{569}}(a + b)

Question 17592186502430 — question.difficulty/easy

The vector $a$ is directed horizontally to the right and has magnitude $6$, while the vector $b$ is directed vertically down and has magnitude $8$. Which of the following is a unit vector that is parallel to $a + b$?

> A scientific calculator is required to answer this question.

Solution: First, we have to find $a+b$. The given directions are perpendicular, so the triangle law of addition gives a right triangle.

To find the unit vector corresponding to $a+b$, we have to divide by the magnitude:

$$
u=\frac{a+b}{|a+b|}
$$

To find the magnitude, we can use the Pythagorean theorem:

$$
\begin{aligned}|a+b|^2&=|a|^2+|b|^2\\
&=6^2+8^2\\
&=36+64\\
&=100\end{aligned}
$$

Therefore, the magnitude is

$$
|a+b|=\sqrt{100}=10
$$

and the corresponding unit vector is

$$
\begin{aligned}u&=\frac{a+b}{|a+b|}\\
&=\frac{1}{10}(a+b)\end{aligned}
$$

Answer selection: \frac{1}{10}(a + b)
