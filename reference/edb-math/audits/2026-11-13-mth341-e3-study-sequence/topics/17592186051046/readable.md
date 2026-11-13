# 17592186051046 Subspaces of N-Dimensional Space

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121126 — Introduction

A **subspace** of $\mathbb{R}^n$ is a subset of $\mathbb R^n$ that is closed  under vector addition and scalar multiplication. In other words: 

$H\subseteq \mathbb R^n$ is a subspace of $\mathbb{R}^n$ if and only if it satisfies the following properties:

- *Closure under vector addition:* 

$\qquad$ If $\mathbf{u}$ and $\mathbf{v}$ are in $H,$ then their sum $\mathbf{u}+\mathbf{v}$ is also in $H.$

- *Closure under scalar multiplication:* 

$\qquad$ If $\mathbf{u}$ is in $H,$ then $c\cdot \mathbf{u}$ is also in $H$ for any scalar number $c.$

For example, consider the line $L$ with equation $y=3x$ in $\mathbb{R}^2.$ Is $L$ a subspace of $\mathbb{R}^2?$ 

First, notice that we can express the points on $L$ as the following set:

$$
L = \left\{ {\left[ \begin{array}{c}x \\ y\end{array} \right]} \in \mathbb{R}^2 \: : \: y=3x \right\}
$$

In other words, $L$ contains all vectors of the form ${\left[ \begin{array}{c}x \\ 3 x\end{array} \right]},$ where $x$ is a real number.

To determine whether $L$ is a subspace of $\mathbb R^2,$ we need to check the two conditions above. 

- Let's pick two arbitrary vectors in $L,$ namely, $\mathbf{u}={\left[ \begin{array}{c}{u}_{1} \\ 3 {u}_{1}\end{array} \right]}$ and $\mathbf{v}={\left[ \begin{array}{c}{v}_{1} \\ 3 {v}_{1}\end{array} \right]}.$ If we compute their sum, we get

$$
\begin{aligned}\mathbf{u}+\mathbf{v} & =\begin{bmatrix}{u}_{1} \\ 3{u}_{1}\end{bmatrix}+\begin{bmatrix}{v}_{1} \\ 3{v}_{1}\end{bmatrix} \\  & =\begin{bmatrix}{u}_{1}+{v}_{1} \\ 3{u}_{1}+3{v}_{1}\end{bmatrix} \\  & =\begin{bmatrix}{\color{red}{{u}_{1}}}+{\color{red}{{v}_{1}}} \\ {\color{blue}{3}}\cdot ({\color{red}{{u}_{1}}}+{\color{red}{{v}_{1}}})\end{bmatrix},\end{aligned}
$$

which satisfies the condition $y=3x.$ Therefore, $\mathbf{u}+\mathbf{v} \in L. \quad {\color{green}\checkmark}$

- Let's pick an arbitrary vector in $L,$ namely, $\mathbf{u}={\left[ \begin{array}{c}{u}_{1} \\ 3 {u}_{1}\end{array} \right]}.$ Then, for any scalar $c$ we have

$$
\begin{aligned}c\cdot \mathbf{u} & =c\cdot \begin{bmatrix}{u}_{1} \\ 3{u}_{1}\end{bmatrix} \\  & =\begin{bmatrix}{\color{red}{c{u}_{1}}} \\ {\color{blue}{3}}\cdot {\color{red}{c{u}_{1}}}\end{bmatrix},\end{aligned}
$$

which satisfies the condition $y=3x.$ Therefore, $c\cdot \mathbf{u}\in L. \quad {\color{green}\checkmark}$

The set $L$ satisfies both conditions. So, we can conclude that it is a subspace of $\mathbb{R}^2.$

**Note:** Since the second condition must be satisfied for any $c,$ including $c=0,$ we can conclude that every subspace must contain the zero vector $\mathbf{0}.$ So, if a set does not contain $\mathbf{0}$ then it is *not* a subspace of $\mathbb{R}^n.$

For instance, the set 

$$
B=\left\{ {\left[ \begin{array}{c}x \\ y\end{array} \right]} \in \mathbb{R}^2 \: : \: y=x+1 \right\}
$$

does *not* contain the zero vector (since $0 \neq 0 + 1$), and consequently it is *not* a subspace of $\mathbb{R}^2.$



### example 17592186119500 — Determining Whether a Line Is a Subspace of Two-Dimensional Space

Let $L$ be the line with equation $y=5+3x$ in $\mathbb{R}^2.$ Which of the following statements are true?

I. $L$ contains the zero-vector

II. $L$ is closed under vector addition

III. $L$ is closed under scalar multiplication

IV. $L$ is **not** a subspace of $\mathbb{R}^2$

Recall the following two facts about subspaces: 

- A set of vectors in a vector space is a *subspace* if it is closed under vector addition and scalar multiplication.

- If a non-empty set is closed under scalar multiplication, then this set must contain the zero-vector (because $0 \cdot \mathbf{v} = \mathbf{0}$ for any vector $\mathbf{v}$). So, if a set does not contain the zero vector, then this set is not closed under scalar multiplication.

Notice that $L$ contains vectors of the form 

$$
{\left[ \begin{array}{c}x \\ y\end{array} \right]} = {\left[ \begin{array}{c}x \\ 5 + 3 x\end{array} \right]}, \qquad x \in \mathbb{R}.
$$

With that in mind, let's examine our statements. 

- Statement I is false. The coordinates of the zero-vector do not satisfy the equation $y=5+3x{:}$

$$
\begin{aligned}y & =5+3x \\ (0) & =5+3(0) \\ 0 & =5\hspace{1em}{\color{red}{\times }}\end{aligned}
$$

- Statement II is false. Let, for example, $\mathbf{a}={\left[ \begin{array}{c}0 \\ 5\end{array} \right]}$ and $\mathbf{b}={\left[ \begin{array}{c}- 1 \\ 2\end{array} \right]}$ from $L.$ Then,

$$
\begin{aligned}\mathbf{a}+\mathbf{b} & =\begin{bmatrix}0 \\ 5\end{bmatrix}+\begin{bmatrix}-1 \\ 2\end{bmatrix}=\begin{bmatrix}0+(-1) \\ 5+2\end{bmatrix}=\begin{bmatrix}-1 \\ 7\end{bmatrix}.\end{aligned}
$$

 
However, ${\left[ \begin{array}{c}- 1 \\ 7\end{array} \right]} \notin L$ since substituting the coordinates into the equation $y=5+3x$ gives the following: 

$$
\begin{aligned}y & =5+3x \\ 7 & =5+3(-1) \\ 7 & =2\hspace{1em}{\color{red}{\times }}\end{aligned}
$$

- Statement III is false. Since $\mathbf{0} \not\in L,$ this set is not closed under scalar multiplication.

- Statement IV is true. Since statements II and III are false, $L$ is *not* a subspace of $\mathbb{R}^2.$

Therefore, the correct answer is "IV only."

### tutorial 17592186121127 — Lines as Subspaces of Three-Dimensional Space

Recall that $H$ is a subspace of $\mathbb{R}^n$ if and only if it satisfies the following properties:

*Closure under vector addition:* 

 $\qquad$ If $\mathbf{u}$ and $\mathbf{v}$ are in $H,$ then their sum $\mathbf{u}+\mathbf{v}$ is also in $H.$

*Closure under scalar multiplication:* 

 $\qquad$ If $\mathbf{u}$ is in $H,$ then $c\cdot \mathbf{u}$ is also in $H$ for any scalar number $c.$

Let $L$ be the line in $\mathbb{R}^3$ that passes through the points $(0,0,0)$ and $(4,1,-2).$ Is $L$ a subspace of $\mathbb{R}^3?$ 

First, note that the direction vector of the line $L$ is 
$$
\mathbf{d}={\left[ \begin{array}{c}4 \\ 1 \\ - 2\end{array} \right]} -   {\left[ \begin{array}{c}0 \\ 0 \\ 0\end{array} \right]}  = {\left[ \begin{array}{c}4 \\ 1 \\ - 2\end{array} \right]} .
$$
This means that the vector equation of the line is

$$
\begin{aligned}\mathbf{r} & =\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}+t\begin{bmatrix}4 \\ 1 \\ -2\end{bmatrix}=\begin{bmatrix}4t \\ t \\ -2t\end{bmatrix}\end{aligned}
$$

for $t\in\mathbb R,$ and the corresponding Cartesian equation is 

$$
\dfrac x4=y=\dfrac z{-2}.
$$

To determine whether $L$ is a subspace, we need to check the two conditions above:

- Let's pick two arbitrary vectors in $L,$ namely, $\mathbf{u}={\left[ \begin{array}{c}4 {u}_{1} \\ {u}_{1} \\ - 2 {u}_{1}\end{array} \right]}$ and $\mathbf{v}={\left[ \begin{array}{c}4 {v}_{1} \\ {v}_{1} \\ - 2 {v}_{1}\end{array} \right]}.$ If we compute their sum, we get

$$
\begin{aligned}\mathbf{u}+\mathbf{v} & =\begin{bmatrix}4{u}_{1} \\ {u}_{1} \\ -2{u}_{1}\end{bmatrix}+\begin{bmatrix}4{v}_{1} \\ {v}_{1} \\ -2{v}_{1}\end{bmatrix} \\  & =\begin{bmatrix}4{u}_{1}+4{v}_{1} \\ {u}_{1}+{v}_{1} \\ (-2{u}_{1})+(-2{v}_{1})\end{bmatrix} \\  & =\begin{bmatrix}{\color{blue}{4}}\cdot ({\color{red}{{u}_{1}}}+{\color{red}{{v}_{1}}}) \\ {\color{red}{{u}_{1}}}+{\color{red}{{v}_{1}}} \\ ({\color{blue}{-2}})\cdot ({\color{red}{{u}_{1}}}+{\color{red}{{v}_{1}}})\end{bmatrix},\end{aligned}
$$

which satisfies the condition $\dfrac x4=y=\dfrac z{-2}.$ Therefore, $\mathbf{u}+\mathbf{v}\in L. \quad {\color{green}\checkmark}$

- Let's pick an arbitrary vector in $L,$ namely, $\mathbf{u}={\left[ \begin{array}{c}4 {u}_{1} \\ {u}_{1} \\ - 2 {u}_{1}\end{array} \right]}.$ Then, for any scalar $c,$ we have

$$
\begin{aligned}c\cdot \mathbf{u} & =c\cdot \begin{bmatrix}4{u}_{1} \\ {u}_{1} \\ -2{u}_{1}\end{bmatrix} \\  & =\begin{bmatrix}{\color{blue}{4}}\cdot {\color{red}{c{u}_{1}}} \\ {\color{red}{c{u}_{1}}} \\ ({\color{blue}{-2}})\cdot {\color{red}{c{u}_{1}}}\end{bmatrix},\end{aligned}
$$

which satisfies the condition $\dfrac x4=y=\dfrac z{-2}.$ Therefore, $c\cdot \mathbf{u}\in L. \quad {\color{green}\checkmark}$

The set $L$ satisfies both conditions. So, we can conclude that it is a subspace of $\mathbb{R}^3.$



### example 17592186119501 — Determining Whether a Line Is a Subspace of Three-Dimensional Space

Let $L$ be the line in $\mathbb{R}^3$ that passes through the points $(1,2,2)$ and $(2,1,1).$ Which of the following statements are true?

I. $L$ contains the zero-vector

II. $L$ is closed under vector addition

III. $L$ is closed under scalar multiplication

IV. $L$ is **not** a subspace of $\mathbb{R}^3$

Recall the following two facts about subspaces: 

- A set of vectors in a vector space is a *subspace* if it is closed under vector addition and scalar multiplication.

- If a non-empty set is closed under scalar multiplication, then this set must contain the zero-vector (because $0 \cdot \mathbf{v} = \mathbf{0}$ for any vector $\mathbf{v}$). So, if a set does not contain the zero vector, then this set is not closed under scalar multiplication.

With that in mind, let's examine our statements. 

- Statement I is false. The direction vector of the line $L$ is 
$$
\mathbf{d}={\left[ \begin{array}{c}2 \\ 1 \\ 1\end{array} \right]} -   {\left[ \begin{array}{c}1 \\ 2 \\ 2\end{array} \right]}  = {\left[ \begin{array}{c}1 \\ - 1 \\ - 1\end{array} \right]} .
$$
This means that the vector equation of the line is

$$
\begin{aligned}\mathbf{r} & =\begin{bmatrix}1 \\ 2 \\ 2\end{bmatrix}+t\begin{bmatrix}1 \\ -1 \\ -1\end{bmatrix}\end{aligned}
$$

for $t\in\mathbb R,$ and the corresponding Cartesian equation is 

$$
{x-1}=\dfrac{y-2}{-1}=\dfrac{z-2}{-1}.
$$

But this line does not pass through the origin since 

$$
{(0)-1}\neq\dfrac{(0)-2}{-1}=\dfrac{(0)-2}{-1}.  \quad {\color{red}\times}
$$

- Statement II is false. Let's consider the vectors $\begin{bmatrix}1 \\ 2 \\ 2\end{bmatrix}$ and $\begin{bmatrix}2 \\ 1 \\ 1\end{bmatrix}$ from $L$ (the position vectors of the given points). Then,
$$
{\left[ \begin{array}{c}1 \\ 2 \\ 2\end{array} \right]} + {\left[ \begin{array}{c}2 \\ 1 \\ 1\end{array} \right]} = {\left[ \begin{array}{c}3 \\ 3 \\ 3\end{array} \right]}.
$$
However, the point $(3,3,3)$ does not belong to $L$ since

$$
{(3)-1}\neq\dfrac{(3)-2}{-1}=\dfrac{(3)-2}{-1}. \quad {\color{red}\times}
$$

- Statement III is false. Since $\mathbf{0} \not\in L,$ this set is not closed under scalar multiplication.

- Statement IV is true. Since statements II and III are false, $L$ is *not* a subspace of $\mathbb{R}^3.$

Therefore, the correct answer is "IV only."

### tutorial 17592186121128 — Planes as Subspace of Three-Dimensional Space

Again, recall that $H$ is a subspace of $\mathbb{R}^n$ if and only if it satisfies the following properties:

- *Closure under vector addition:* 

$\qquad$ If $\mathbf{u}$ and $\mathbf{v}$ are in $H,$ then their sum $\mathbf{u}+\mathbf{v}$ is also in $H.$

- *Closure under scalar multiplication:* 

$\qquad$ If $\mathbf{u}$ is in $H,$ then $c\cdot \mathbf{u}$ is also in $H$ for any scalar number $c.$

Consider the plane $\Pi$ with equation $z=4x-2y$ in $\mathbb{R}^3.$ 

Notice that $\Pi$ contains vectors of the form 

$$
{\left[ \begin{array}{c}x \\ y \\ z\end{array} \right]} = {\left[ \begin{array}{c}x \\ y \\ 4 x - 2 y\end{array} \right]}, \qquad x,y \in \mathbb{R}.
$$

Is $\Pi$ a subspace of $\mathbb{R}^3?$ To find out, we need to check the two conditions above. 

- Let's pick two arbitrary vectors in $\Pi,$ namely, $\mathbf{u}={\left[ \begin{array}{c}{u}_{1} \\ {u}_{2} \\ 4 {u}_{1} - 2 {u}_{2}\end{array} \right]}$ and $\mathbf{v}={\left[ \begin{array}{c}{v}_{1} \\ {v}_{2} \\ 4 {v}_{1} - 2 {v}_{2}\end{array} \right]}.$ If we compute their sum, we get

$$
\begin{aligned}\mathbf{u}+\mathbf{v} & =\begin{bmatrix}{u}_{1} \\ {u}_{2} \\ 4{u}_{1}-2{u}_{2}\end{bmatrix}+\begin{bmatrix}{v}_{1} \\ {v}_{2} \\ 4{v}_{1}-2{v}_{2}\end{bmatrix} \\  & =\begin{bmatrix}{u}_{1}+{v}_{1} \\ {u}_{2}+{v}_{2} \\ 4{u}_{1}-2{u}_{2}+4{v}_{1}-2{v}_{2}\end{bmatrix} \\  & =\begin{bmatrix}{\color{red}{{u}_{1}}}+{\color{red}{{v}_{1}}} \\ {\color{violet}{{u}_{2}}}+{\color{violet}{{v}_{2}}} \\ {\color{blue}{4}}\cdot ({\color{red}{{u}_{1}}}+{\color{red}{{v}_{1}}})-{\color{blue}{2}}\cdot ({\color{violet}{{u}_{2}}}+{\color{violet}{{v}_{2}}})\end{bmatrix},\end{aligned}
$$

which satisfies the condition $z=4x-2y.$ Therefore, $\mathbf{u}+\mathbf{v}\in \Pi. \quad {\color{green}\checkmark}$

- Let's pick an arbitrary vector in $\Pi,$ say, $\mathbf{u}={\left[ \begin{array}{c}{u}_{1} \\ {u}_{2} \\ 4 {u}_{1} - 2 {u}_{2}\end{array} \right]}.$ Then, for any scalar $c$ we have

$$
\begin{aligned}c\cdot \mathbf{u} & =c\cdot \begin{bmatrix}{u}_{1} \\ {u}_{2} \\ 4{u}_{1}-2{u}_{2}\end{bmatrix} \\  & =\begin{bmatrix}{\color{red}{c{u}_{1}}} \\ {\color{violet}{c{u}_{2}}} \\ {\color{blue}{4}}\cdot {\color{red}{c{u}_{1}}}-{\color{blue}{2}}\cdot {\color{violet}{c{u}_{2}}}\end{bmatrix},\end{aligned}
$$

which satisfies the condition $z=4x-2y.$ Therefore, $c\cdot \mathbf{u}\in \Pi. \quad {\color{green}\checkmark}$

The set $\Pi$ satisfies both conditions. So, we can conclude that it is a subspace of $\mathbb{R}^3.$



### example 17592186119502 — Determining Whether a Plane Is a Subspace of Three-Dimensional Space

Let $\Pi$ be the plane with equation $x+4y-3z=2$ in $\mathbb{R}^3.$ Which of the following statements are true? 

I. $\Pi$ contains the zero-vector

II. $\Pi$ is closed under vector addition

III. $\Pi$ is closed under scalar multiplication

IV. $\Pi$ is **not** a subspace of $\mathbb{R}^3$

Recall the following two facts about subspaces: 

- A set of vectors in a vector space is a *subspace* if it is closed under vector addition and scalar multiplication.

- If a non-empty set is closed under scalar multiplication, then this set must contain the zero-vector (because $0 \cdot \mathbf{v} = \mathbf{0}$ for any vector $\mathbf{v}$). So, if a set does not contain the zero vector, then this set is not closed under scalar multiplication.

Notice that $\Pi$ contains vectors of the form 

$$
{\left[ \begin{array}{c}x \\ y \\ z\end{array} \right]} = {\left[ \begin{array}{c}2 - 4 y + 3 z \\ y \\ z\end{array} \right]}, \qquad y,z \in \mathbb{R}.
$$

With that in mind, let's examine our statements. 

- Statement I is false. The plane does not pass through the origin since

$$
\begin{aligned}x+4y-3z & =2 \\ (0)+4(0)-3(0) & =2 \\ 0 & =2\hspace{1em}{\color{red}{\times }}\end{aligned}
$$

- Statement II is false. Let's consider $\mathbf{a}={\left[ \begin{array}{c}2 \\ 0 \\ 0\end{array} \right]} \in \Pi$ and $\mathbf{b}={\left[ \begin{array}{c}1 \\ 1 \\ 1\end{array} \right]} \in \Pi.$ Then 

$$
\begin{aligned}\mathbf{a}+\mathbf{b} & =\begin{bmatrix}2 \\ 0 \\ 0\end{bmatrix}+\begin{bmatrix}1 \\ 1 \\ 1\end{bmatrix}=\begin{bmatrix}2+1 \\ 0+1 \\ 0+1\end{bmatrix}=\begin{bmatrix}3 \\ 1 \\ 1\end{bmatrix},\end{aligned}
$$

However, $\begin{bmatrix}3 \\ 1 \\ 1\end{bmatrix}$ does not belong to $\Pi$ since 

$$
\begin{aligned}x+4y-3z & =2 \\ (3)+4(1)-3(1) & =2 \\ 4 & =2\hspace{1em}{\color{red}{\times }}\end{aligned}
$$

- Statement III is false. Since $\mathbf{0} \not\in \Pi,$ this set is not closed under scalar multiplication.

- Statement IV is true. Since statements II and III are false, $\Pi$ is *not* a subspace of $\mathbb{R}^3.$

Therefore, the correct answer is "IV only."

## Representative practice (first three per skill; full bank in practice.json)

### Determining Whether a Line Is a Subspace of Two-Dimensional Space (12 captured questions)

Question 17592186120145 — question.difficulty/easy

Let $L$ be the line with equation $x=2y$ in ${R}^{2}.$ Which of the following statements are true?

Select all that apply.

Solution: Recall the following two facts about subspaces: 

- A set of vectors in a vector space is a *subspace* if it is closed under vector addition and scalar multiplication.

- If a non-empty set is closed under scalar multiplication, then this set must contain the zero-vector (because $0\cdot v=0$ for any vector $v$). So, if a set does not contain the zero vector, then this set is not closed under scalar multiplication.

Notice that $L$ contains vectors of the form 

$$
\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}2y \\ y\end{bmatrix},\,y\in R.
$$

With that in mind, let's examine our statements. 

- Statement “$L$ contains the zero-vector” is true. The coordinates of the zero-vector satisfy the equation $x=2y:$

$$
\begin{aligned}x & =2y \\ (0) & =2(0) \\ 0 & =0\,✓\end{aligned}
$$

- Statement “$L$ is closed under vector addition” is true. Let, for example, $a=\begin{bmatrix}2a \\ a\end{bmatrix}\in L$ and $b=\begin{bmatrix}2b \\ b\end{bmatrix}\in L.$ Then,

$$
\begin{aligned}a+b & =\begin{bmatrix}2a \\ a\end{bmatrix}+\begin{bmatrix}2b \\ b\end{bmatrix}=\begin{bmatrix}2a+2b \\ a+b\end{bmatrix}=\begin{bmatrix}2(a+b) \\ a+b\end{bmatrix},\end{aligned}
$$

which satisfies the condition $x=2y.$ Therefore, $a+b\in L.$

- Statement “$L$ is closed under scalar multiplication” is true. Let, for example, $a=\begin{bmatrix}2a \\ a\end{bmatrix}\in L$ and $k\in R.$ Then,

$$
\begin{aligned}k\cdot a & =k\cdot \begin{bmatrix}2a \\ a\end{bmatrix}=\begin{bmatrix}2ka \\ ka\end{bmatrix},\end{aligned}
$$

which satisfies the condition $x=2y.$ Therefore, $k\cdot a\in L.$

- Statement “$L$ is a subspace of ${R}^{2}$” is true. Since statements “$L$ is closed under vector addition” and “$L$ is closed under scalar multiplication” are true, $L$ must be a subspace of ${R}^{2}.$

Therefore, the correct answer is "All the statements are true."

Answer $L$ contains the zero-vector: true

Answer $L$ is a subspace of ${\mathbb{R}}^{2}$: true

Answer $L$ is closed under scalar multiplication: true

Answer $L$ is closed under vector addition: true

Question 17592186120150 — question.difficulty/moderate

Let $L$ be the line with equation $y=1-2x$ in ${R}^{2}.$ Which of the following statements are true?

Select all that apply.

Solution: Recall the following two facts about subspaces: 

- A set of vectors in a vector space is a *subspace* if it is closed under vector addition and scalar multiplication.

- If a non-empty set is closed under scalar multiplication, then this set must contain the zero-vector (because $0\cdot v=0$ for any vector $v$). So, if a set does not contain the zero vector, then this set is not closed under scalar multiplication.

Notice that $L$ contains vectors of the form 

$$
\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}x \\ 1-2x\end{bmatrix},\,x\in R.
$$

With that in mind, let's examine our statements. 

- Statement “$L$ contains the zero-vector” is false. The coordinates of the zero-vector do not satisfy the equation $y=1-2x:$

$$
\begin{aligned}y & =1-2x \\ (0) & =1-2(0) \\ 0 & =1\,\times \end{aligned}
$$

- Statement “$L$ is closed under vector addition” is false. Let, for example, $a=\begin{bmatrix}0 \\ 1\end{bmatrix}$ and $b=\begin{bmatrix}1 \\ -1\end{bmatrix}$ from $L.$ Then,

$$
\begin{aligned}a+b & =\begin{bmatrix}0 \\ 1\end{bmatrix}+\begin{bmatrix}1 \\ -1\end{bmatrix}=\begin{bmatrix}0+1 \\ 1-1\end{bmatrix}=\begin{bmatrix}1 \\ 0\end{bmatrix}.\end{aligned}
$$

 
However, $\begin{bmatrix}1 \\ 0\end{bmatrix}\notin L$ since substituting the coordinates into the equation, we obtain the following: 

$$
\begin{aligned}y & =1-2x \\ (0) & =1-2(1) \\ 0 & =-1\,\times \end{aligned}
$$

- Statement “$L$ is closed under scalar multiplication” is false. Since $0\notin L,$ this set is not closed under scalar multiplication.

- Statement “$L$ is **not** a subspace of ${R}^{2}$” is true. Since statements “$L$ is closed under vector addition” and “$L$ is closed under scalar multiplication” are false, $L$ is *not* a subspace of ${R}^{2}.$

Therefore, the correct answer is “$L$ is **not** a subspace of ${R}^{2}$” only.

Answer $L$ contains the zero-vector: false

Answer $L$ is **not** a subspace of ${\mathbb{R}}^{2}$: true

Answer $L$ is closed under scalar multiplication: false

Answer $L$ is closed under vector addition: false

Question 17592186275357 — question.difficulty/easy

Let $L$ be the line with equation $y=-x$ in ${R}^{2}.$ Which of the following statements are true?

Select all that apply.

Solution: Recall the following two facts about subspaces: 

- A set of vectors in a vector space is a *subspace* if it is closed under vector addition and scalar multiplication.

- If a non-empty set is closed under scalar multiplication, then this set must contain the zero-vector (because $0\cdot v=0$ for any vector $v$). So, if a set does not contain the zero vector, then this set is not closed under scalar multiplication.

Notice that $L$ contains vectors of the form 

$$
\begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}x \\ -x\end{bmatrix},\,x\in R.
$$

With that in mind, let's examine our statements. 

- Statement “$L$ contains the zero-vector” is true. The coordinates of the zero-vector satisfy the equation $y=-x:$

$$
\begin{aligned}y & =-x \\ (0) & =-(0) \\ 0 & =0\,✓\end{aligned}
$$

- Statement “$L$ is closed under vector addition” is true. Let, for example, $a=\begin{bmatrix}a \\ -a\end{bmatrix}\in L$ and $b=\begin{bmatrix}b \\ -b\end{bmatrix}\in L.$ Then,

$$
\begin{aligned}a+b & =\begin{bmatrix}a \\ -a\end{bmatrix}+\begin{bmatrix}b \\ -b\end{bmatrix}=\begin{bmatrix}a+b \\ (-a)+(-b)\end{bmatrix}=\begin{bmatrix}a+b \\ -(a+b)\end{bmatrix},\end{aligned}
$$

which satisfies the condition $y=-x.$ Therefore, $a+b\in L.$

- Statement “$L$ is closed under scalar multiplication” is true. Let, for example, $a=\begin{bmatrix}a \\ -a\end{bmatrix}\in L$ and $k\in R.$ Then,

$$
\begin{aligned}k\cdot a & =k\cdot \begin{bmatrix}a \\ -a\end{bmatrix}=\begin{bmatrix}ka \\ k(-a)\end{bmatrix}=\begin{bmatrix}ka \\ -(ka)\end{bmatrix},\end{aligned}
$$

which satisfies the condition $y=-x.$ Therefore, $k\cdot a\in L.$

- Statement “$L$ is a subspace of ${R}^{2}$” is true. Since statements “$L$ is closed under vector addition” and “$L$ is closed under scalar multiplication” are true, $L$ must be a subspace of ${R}^{2}.$

Therefore, the correct answer is "All the statements are true."

Answer $L$ contains the zero-vector: true

Answer $L$ is a subspace of ${\mathbb{R}}^{2}$: true

Answer $L$ is closed under scalar multiplication: true

Answer $L$ is closed under vector addition: true

### Determining Whether a Line Is a Subspace of Three-Dimensional Space (12 captured questions)

Question 17592186120146 — question.difficulty/moderate

Let $L$ be the line in ${R}^{3}$ that passes through the points $(-2,2,-2)$ and $(3,-4,2).$ Which of the following statements are true?

Select all that apply.

Solution: Recall the following two facts about subspaces: 

- A set of vectors in a vector space is a *subspace* if it is closed under vector addition and scalar multiplication.

- If a non-empty set is closed under scalar multiplication, then this set must contain the zero-vector (because $0\cdot v=0$ for any vector $v$). So, if a set does not contain the zero vector, then this set is not closed under scalar multiplication.

With that in mind, let's examine our statements. 

- Statement “$L$ contains the zero-vector” is false. The direction vector of the line $L$ is 

$$
d=\begin{bmatrix}3 \\ -4 \\ 2\end{bmatrix}-\begin{bmatrix}-2 \\ 2 \\ -2\end{bmatrix}=\begin{bmatrix}5 \\ -6 \\ 4\end{bmatrix}.
$$

This means that the vector equation of the line is

$$
\begin{aligned}r & =\begin{bmatrix}-2 \\ 2 \\ -2\end{bmatrix}+t\begin{bmatrix}5 \\ -6 \\ 4\end{bmatrix}\end{aligned}
$$

for $t\in R,$ and the corresponding Cartesian equation is 

$$
\frac{x+2}{5}=\frac{y-2}{-6}=\frac{z+2}{4}.
$$

But this line does not pass through the origin since 

$$
\frac{(0)+2}{5}\ne \frac{(0)-2}{-6}\ne \frac{(0)+2}{4}.\,\times 
$$

- Statement “$L$ is closed under vector addition” is false. Let's consider the vectors $\begin{bmatrix}-2 \\ 2 \\ -2\end{bmatrix}$ and $\begin{bmatrix}3 \\ -4 \\ 2\end{bmatrix}$ from $L$ (the position vectors of the given points). Then,

$$
\begin{bmatrix}-2 \\ 2 \\ -2\end{bmatrix}+\begin{bmatrix}3 \\ -4 \\ 2\end{bmatrix}=\begin{bmatrix}1 \\ -2 \\ 0\end{bmatrix}.
$$

However, the point $(1,-2,0)$ does not belong to $L$ since

$$
\frac{(1)+2}{5}\ne \frac{(-2)-2}{-6}\ne \frac{(0)+2}{4}.\,\times 
$$

- Statement “$L$ is closed under scalar multiplication” is false. Since $0\notin L,$ this set is not closed under scalar multiplication.

- Statement “$L$ is **not** a subspace of ${R}^{3}$” is true. Since statements “$L$ is closed under vector addition” and “$L$ is closed under scalar multiplication” are false, $L$ is *not* a subspace of ${R}^{3}.$

Therefore, the correct answer is “$L$ is **not** a subspace of ${R}^{3}$” only.

Answer $L$ contains the zero-vector: false

Answer $L$ is **not** a subspace of ${\mathbb{R}}^{3}$: true

Answer $L$ is closed under scalar multiplication: false

Answer $L$ is closed under vector addition: false

Question 17592186120151 — question.difficulty/easy

Let $L$ be the line in ${R}^{3}$ that passes through the points $(0,0,0)$ and $(1,-1,1).$ Which of the following statements are true?

Select all that apply.

Solution: Recall the following two facts about subspaces: 

- A set of vectors in a vector space is a *subspace* if it is closed under vector addition and scalar multiplication.

- If a non-empty set is closed under scalar multiplication, then this set must contain the zero-vector (because $0\cdot v=0$ for any vector $v$). So, if a set does not contain the zero vector, then this set is not closed under scalar multiplication.

First, note that the direction vector of the line $L$ is 

$$
d=\begin{bmatrix}1 \\ -1 \\ 1\end{bmatrix}-\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}=\begin{bmatrix}1 \\ -1 \\ 1\end{bmatrix}.
$$

This means that the vector equation of the line is

$$
\begin{aligned}r & =\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}+t\begin{bmatrix}1 \\ -1 \\ 1\end{bmatrix}=\begin{bmatrix}t \\ -t \\ t\end{bmatrix}\end{aligned}
$$

for $t\in R,$ and the corresponding Cartesian equation is 

$$
x=-y=z.
$$

With that in mind, let's examine our statements. 

- Statement “$L$ contains the zero-vector” is true. Indeed, from the definition of $L$ we have that the point $(0,0,0)$ is in $L.$

- Statement “$L$ is closed under vector addition” is true. Let, for example, $a=\begin{bmatrix}a \\ -a \\ a\end{bmatrix}\in L$ and $b=\begin{bmatrix}b \\ -b \\ b\end{bmatrix}\in L.$ Then,

$$
\begin{aligned}a+b & =\begin{bmatrix}a \\ -a \\ a\end{bmatrix}+\begin{bmatrix}b \\ -b \\ b\end{bmatrix}=\begin{bmatrix}a+b \\ -a+(-b) \\ a+b\end{bmatrix}=\begin{bmatrix}a+b \\ -(a+b) \\ a+b\end{bmatrix},\end{aligned}
$$

which satisfies the conditions $x=-y=z.$ Therefore, $a+b\in L.$

- Statement “$L$ is closed under scalar multiplication” is true. Let, for example, $a=\begin{bmatrix}a \\ -a \\ a\end{bmatrix}\in L$ and $k\in R.$ Then,

$$
\begin{aligned}k\cdot a & =k\cdot \begin{bmatrix}a \\ -a \\ a\end{bmatrix}=\begin{bmatrix}ka \\ k(-a) \\ ka\end{bmatrix}=\begin{bmatrix}ka \\ -(ka) \\ ka\end{bmatrix},\end{aligned}
$$

which satisfies the conditions $x=-y=z.$ Therefore, $k\cdot a\in L.$

- Statement “$L$ is **not** a subspace of ${R}^{3}$” is false. Since statements “$L$ is closed under vector addition” and “$L$ is closed under scalar multiplication” are true, $L$ is a subspace of ${R}^{3}.$

Therefore, the correct answer is “$L$ contains the zero-vector”; “$L$ is closed under vector addition”; “$L$ is closed under scalar multiplication” only.

Answer $L$ contains the zero-vector: true

Answer $L$ is **not** a subspace of ${\mathbb{R}}^{3}$: false

Answer $L$ is closed under scalar multiplication: true

Answer $L$ is closed under vector addition: true

Question 17592186275363 — question.difficulty/moderate

Let $L$ be the line in ${R}^{3}$ that passes through the points $(1,2,3)$ and $(3,2,1).$ Which of the following statements are true?

Select all that apply.

Solution: Recall the following two facts about subspaces: 

- A set of vectors in a vector space is a *subspace* if it is closed under vector addition and scalar multiplication.

- If a non-empty set is closed under scalar multiplication, then this set must contain the zero-vector (because $0\cdot v=0$ for any vector $v$). So, if a set does not contain the zero vector, then this set is not closed under scalar multiplication.

With that in mind, let's examine our statements. 

- Statement “$L$ contains the zero-vector” is false.The direction vector of the line $L$ is 

$$
d=\begin{bmatrix}3 \\ 2 \\ 1\end{bmatrix}-\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix}=\begin{bmatrix}2 \\ 0 \\ -2\end{bmatrix}.
$$

This means that the vector equation of the line is

$$
\begin{aligned}r & =\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix}+t\begin{bmatrix}2 \\ 0 \\ -2\end{bmatrix}\end{aligned}
$$

for $t\in R,$ and the corresponding Cartesian equation is 

$$
\frac{x-1}{2}=\frac{z-3}{-2},\,y=2
$$

But this line does not pass through the origin since the second coordinate of any point on this line satisfies

$$
y=2\ne 0.\,\times 
$$

- Statement “$L$ is closed under vector addition” is false. Let's consider the vectors $\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix}$ and $\begin{bmatrix}3 \\ 2 \\ 1\end{bmatrix}$ from $L$ (the position vectors of the given points). Then,

$$
\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix}+\begin{bmatrix}3 \\ 2 \\ 1\end{bmatrix}=\begin{bmatrix}4 \\ 4 \\ 4\end{bmatrix}.
$$

However, point $(4,4,4)$ does not belong to $L$ since it does not satisfy the equation of the line. Indeed, we have

$$
y=4\ne 2.\,\times 
$$

- Statement “$L$ is closed under scalar multiplication” is false. Since $0\notin L,$ this set is not closed under scalar multiplication.

- Statement “$L$ is **not** a subspace of ${R}^{3}$” is true. Since statements “$L$ is closed under vector addition” and “$L$ is closed under scalar multiplication” are false, $L$ is *not* a subspace of ${R}^{3}.$

Therefore, the correct answer is “$L$ is **not** a subspace of ${R}^{3}$” only.

Answer $L$ contains the zero-vector: false

Answer $L$ is **not** a subspace of ${\mathbb{R}}^{3}$: true

Answer $L$ is closed under scalar multiplication: false

Answer $L$ is closed under vector addition: false

### Determining Whether a Plane Is a Subspace of Three-Dimensional Space (12 captured questions)

Question 17592186120152 — question.difficulty/hard

Let $Π$ be the plane with equation $x-y-z=1$ in ${R}^{3}.$ Which of the following statements are true?

Select all that apply.

Solution: Recall the following two facts about subspaces: 

- A set of vectors in a vector space is a *subspace* if it is closed under vector addition and scalar multiplication.

- If a non-empty set is closed under scalar multiplication, then this set must contain the zero-vector (because $0\cdot v=0$ for any vector $v$). So, if a set does not contain the zero vector, then this set is not closed under scalar multiplication.

Notice that $Π$ contains vectors of the form 

$$
\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}x \\ y \\ x-y-1\end{bmatrix},\,x,y\in R.
$$

With that in mind, let's examine our statements. 

- Statement “$Π$ contains the zero-vector” is false. The line does not pass through the origin since

$$
\begin{aligned}z & =x-y-1 \\ (0) & =(0)-(0)-(1) \\ 0 & =-1\,\times \end{aligned}
$$

- Statement “$Π$ is closed under vector addition” is false. Let's consider $a=\begin{bmatrix}0 \\ 0 \\ -1\end{bmatrix}\in Π$ and $b=\begin{bmatrix}1 \\ 0 \\ 0\end{bmatrix}\in Π.$ Then 

$$
\begin{aligned}a+b & =\begin{bmatrix}0 \\ 0 \\ -1\end{bmatrix}+\begin{bmatrix}1 \\ 0 \\ 0\end{bmatrix}=\begin{bmatrix}0+1 \\ 0+0 \\ -1+0\end{bmatrix}=\begin{bmatrix}1 \\ 0 \\ -1\end{bmatrix},\end{aligned}
$$

However, $\begin{bmatrix}1 \\ 0 \\ -1\end{bmatrix}$ does not belong to $Π$ since 

$$
\begin{aligned}z & =x-y-1 \\ (-1) & =(1)-(0)-1 \\ -1 & =0\,\times \end{aligned}
$$

- Statement “$Π$ is closed under scalar multiplication” is false. Since $0\notin Π,$ this set is not closed under scalar multiplication.

- Statement “$Π$ is **not** a subspace of ${R}^{3}$” is true. Since statements “$Π$ is closed under vector addition” and “$Π$ is closed under scalar multiplication” are false, $L$ is *not* a subspace of ${R}^{3}.$

Therefore, the correct answer is “$Π$ is **not** a subspace of ${R}^{3}$” only.

Answer $Π$ contains the zero-vector: false

Answer $Π$ is **not** a subspace of ${\mathbb{R}}^{3}$: true

Answer $Π$ is closed under scalar multiplication: false

Answer $Π$ is closed under vector addition: false

Question 17592186120153 — question.difficulty/moderate

Let $Π$ be the plane with equation $z=x-y$ in ${R}^{3}.$ Which of the following statements are true?

Select all that apply.

Solution: Recall the following two facts about subspaces: 

- A set of vectors in a vector space is a *subspace* if it is closed under vector addition and scalar multiplication.

- If a non-empty set is closed under scalar multiplication, then this set must contain the zero-vector (because $0\cdot v=0$ for any vector $v$). So, if a set does not contain the zero vector, then this set is not closed under scalar multiplication.

Notice that $Π$ contains vectors of the form 

$$
\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}x \\ y \\ x-y\end{bmatrix},\,x,y\in R.
$$

With that in mind, let's examine our statements. 

- Statement “$Π$ contains the zero-vector” is true. The coordinates of the zero-vector satisfy the equation $z=x-y:$

$$
\begin{aligned}z & =x-y \\ (0) & =(0)-(0) \\ 0 & =0\,✓\end{aligned}
$$

- Statement “$Π$ is closed under vector addition” is true. Let, for example, $a=\begin{bmatrix}{a}_{1} \\ {a}_{2} \\ {a}_{1}-{a}_{2}\end{bmatrix}\in Π$ and $b=\begin{bmatrix}{b}_{1} \\ {b}_{2} \\ {b}_{1}-{b}_{2}\end{bmatrix}\in Π.$ Then,

$$
\begin{aligned}a+b & =\begin{bmatrix}{a}_{1} \\ {a}_{2} \\ {a}_{1}-{a}_{2}\end{bmatrix}+\begin{bmatrix}{b}_{1} \\ {b}_{2} \\ {b}_{1}+{b}_{2}\end{bmatrix}=\begin{bmatrix}{a}_{1}+{b}_{1} \\ {a}_{2}+{b}_{2} \\ ({a}_{1}-{a}_{2})+({b}_{1}-{b}_{2})\end{bmatrix}=\begin{bmatrix}{a}_{1}+{b}_{1} \\ {a}_{2}+{b}_{2} \\ ({a}_{1}+{b}_{1})-({a}_{2}+{b}_{2})\end{bmatrix},\end{aligned}
$$

which satisfies the condition $z=x-y.$ Therefore, $a+b\in Π.$

- Statement “$Π$ is closed under scalar multiplication” is true. Let, for example, $a=\begin{bmatrix}{a}_{1} \\ {a}_{2} \\ {a}_{1}-{a}_{2}\end{bmatrix}\in Π$ and $k\in R.$ Then,

$$
\begin{aligned}k\cdot a & =k\cdot \begin{bmatrix}{a}_{1} \\ {a}_{2} \\ {a}_{1}-{a}_{2}\end{bmatrix}=\begin{bmatrix}k{a}_{1} \\ k{a}_{2} \\ k({a}_{1}-{a}_{2})\end{bmatrix}=\begin{bmatrix}k{a}_{1} \\ k{a}_{2} \\ k{a}_{1}-k{a}_{2}\end{bmatrix},\end{aligned}
$$

which satisfies the condition $z=x-y.$ Therefore, $k\cdot a\in Π.$

- Statement “$Π$ is **not** a subspace of ${R}^{3}$” is false. Since statements “$Π$ is closed under vector addition” and “$Π$ is closed under scalar multiplication” are true, $Π$ must be a subspace of ${R}^{3}.$

Therefore, the correct answer is “$Π$ contains the zero-vector”; “$Π$ is closed under vector addition”; “$Π$ is closed under scalar multiplication” only.

Answer $Π$ contains the zero-vector: true

Answer $Π$ is **not** a subspace of ${\mathbb{R}}^{3}$: false

Answer $Π$ is closed under scalar multiplication: true

Answer $Π$ is closed under vector addition: true

Question 17592186275364 — question.difficulty/moderate

Let $Π$ be the plane with equation $z=2x-5y$ in ${R}^{3}.$ Which of the following statements are true?

Select all that apply.

Solution: Recall the following two facts about subspaces: 

- A set of vectors in a vector space is a *subspace* if it is closed under vector addition and scalar multiplication.

- If a non-empty set is closed under scalar multiplication, then this set must contain the zero-vector (because $0\cdot v=0$ for any vector $v$). So, if a set does not contain the zero vector, then this set is not closed under scalar multiplication.

Notice that $Π$ contains vectors of the form 

$$
\begin{bmatrix}x \\ y \\ z\end{bmatrix}=\begin{bmatrix}x \\ y \\ 2x-5y\end{bmatrix},\,x,y\in R.
$$

With that in mind, let's examine our statements. 

- Statement “$Π$ contains the zero-vector” is true. The coordinates of the zero-vector satisfy the equation $z=2x-5y:$

$$
\begin{aligned}z & =2x-5y \\ (0) & =2(0)-5(0) \\ 0 & =0\,✓\end{aligned}
$$

- Statement “$Π$ is closed under vector addition” is true. Let, for example, $a=\begin{bmatrix}{a}_{1} \\ {a}_{2} \\ 2{a}_{1}-5{a}_{2}\end{bmatrix}\in Π$ and $b=\begin{bmatrix}{b}_{1} \\ {b}_{2} \\ 2{b}_{1}-5{b}_{2}\end{bmatrix}\in Π.$ Then,

$$
\begin{aligned}a+b & =\begin{bmatrix}{a}_{1} \\ {a}_{2} \\ 2{a}_{1}-5{a}_{2}\end{bmatrix}+\begin{bmatrix}{b}_{1} \\ {b}_{2} \\ 2{b}_{1}-5{b}_{2}\end{bmatrix}=\begin{bmatrix}{a}_{1}+{b}_{1} \\ {a}_{2}+{b}_{2} \\ (2{a}_{1}-5{a}_{2})+(2{b}_{1}-5{b}_{2})\end{bmatrix}=\begin{bmatrix}{a}_{1}+{b}_{1} \\ {a}_{2}+{b}_{2} \\ 2({a}_{1}+{b}_{1})-5({a}_{2}+{b}_{2})\end{bmatrix},\end{aligned}
$$

which satisfies the condition $z=2x-5y.$ Therefore, $a+b\in Π.$

- Statement “$Π$ is closed under scalar multiplication” is true. Let, for example, $a=\begin{bmatrix}{a}_{1} \\ {a}_{2} \\ 2{a}_{1}-5{a}_{2}\end{bmatrix}\in Π$ and $k\in R.$ Then,

$$
\begin{aligned}k\cdot a & =k\cdot \begin{bmatrix}{a}_{1} \\ {a}_{2} \\ 2{a}_{1}-5{a}_{2}\end{bmatrix}=\begin{bmatrix}k{a}_{1} \\ k{a}_{2} \\ k(2{a}_{1}-5{a}_{2})\end{bmatrix}=\begin{bmatrix}k{a}_{1} \\ k{a}_{2} \\ 2k{a}_{1}-5k{a}_{2}\end{bmatrix},\end{aligned}
$$

which satisfies the condition $z=2x-5y.$ Therefore, $k\cdot a\in Π.$

- Statement “$Π$ is **not** a subspace of ${R}^{3}$” is false. Since statements “$Π$ is closed under vector addition” and “$Π$ is closed under scalar multiplication” are true, the plane $Π$ must be a subspace of ${R}^{3}.$

Therefore, the correct answer is “$Π$ contains the zero-vector”; “$Π$ is closed under vector addition”; “$Π$ is closed under scalar multiplication” only.

Answer $Π$ contains the zero-vector: true

Answer $Π$ is **not** a subspace of ${\mathbb{R}}^{3}$: false

Answer $Π$ is closed under scalar multiplication: true

Answer $Π$ is closed under vector addition: true
