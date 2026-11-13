# 17592186050910 Orthogonal Linear Transformations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186199537 — Introduction

A linear transformation $\mathbf{Q}:\mathbb{R}^n \to \mathbb{R}^n$ is an **orthogonal linear transformation** if for any $\mathbf{x}, \mathbf{y} \in \mathbb{R}^n,$ we have that

$$
\mathbf{Q}(\mathbf{x}) \cdot \mathbf{Q}(\mathbf{y}) = \mathbf{x} \cdot \mathbf{y}.
$$

In this case, we say that $\mathbf{Q}$ *preserves the dot product*.

The linear transformation $\mathbf{Q}$ being orthogonal is equivalent to the following:

- The matrix $Q$ of transformation $\mathbf{Q}$ relative to any orthonormal basis (including the standard basis) of $\mathbb{R}^n$ is orthogonal.

- $\| \mathbf{Q}(\mathbf{x}) \| = \| \mathbf{x} \|$. In other words, $\mathbf{Q}$ preserves vector norms.

- If $\mathbf{x} \perp \mathbf{y}$ then $\mathbf{Q}(\mathbf{x}) \perp \mathbf{Q}(\mathbf{y})$ for any $\mathbf{x}, \mathbf{y} \in \mathbb{R}^n.$ In general, $\mathbf{Q}$ preserves the angle between any two vectors.

- $\mathbf{Q}$ maps any orthogonal (orthonormal) set into an orthogonal (orthonormal) set.



### example 17592186198131 — Applying the Angle Preserving Property of Orthogonal Linear Transformations

Let $\mathbf{Q}$ be an orthogonal linear transformation. If $\mathbf{x}={\left[ \begin{array}{c}- 1 \\ - 2 \\ 2\end{array} \right]}$ and $\mathbf{y}={\left[ \begin{array}{c}3 \\ 0 \\ 5\end{array} \right]}$, find

I. $\Vert \mathbf{Q}(\mathbf{x}) \Vert.$

II. $\mathbf{Q}(\mathbf{x}) \cdot \mathbf{Q}(\mathbf{y}).$

Since $\mathbf{Q}$ is orthogonal, we have that $\mathbf{Q}(\mathbf{x}) \cdot \mathbf{Q}(\mathbf{y}) = \mathbf{x} \cdot \mathbf{y}$ for any vectors $\mathbf{x}$ and $\mathbf{y}.$

The linear transformation $\mathbf{Q}$ being orthogonal is equivalent to the following:

- The matrix $Q$ of transformation $\mathbf{Q}$ relative to any orthonormal basis (including the standard basis) of $\mathbb{R}^n$ is orthogonal.

- $|| \mathbf{Q}(\mathbf{x}) || = || \mathbf{x} ||.$

- If $\mathbf{x} \perp \mathbf{y}$ then $\mathbf{Q}(\mathbf{x}) \perp \mathbf{Q}(\mathbf{y})$ for any $\mathbf{x}, \mathbf{y} \in \mathbb{R}^n.$ In general, $\mathbf{Q}$ preserves the angle between any two vectors.

- $\mathbf{Q}$ maps any orthogonal (orthonormal) set into an orthogonal (orthonormal) set.

In this case, since $\mathbf{Q}$ is orthogonal, we have 

$$
\begin{aligned}‖Q(x)‖ & =‖x‖ \\  & =\sqrt{{x}_{1}^{2}+{x}_{2}^{2}+{x}_{3}^{2}} \\  & =\sqrt{(-1)^{2}+(-2)^{2}+{2}^{2}} \\  & =3.\end{aligned}
$$

Also, $\mathbf{Q}(\mathbf{x}) \cdot \mathbf{Q}(\mathbf{y}) = \mathbf{x} \cdot \mathbf{y}.$ As a result,

$$
\begin{aligned}Q(x)\cdot Q(y) & =x\cdot y \\  & =(-1)\cdot 3+(-2)\cdot 0+2\cdot 5 \\  & =7.\end{aligned}
$$

### example 17592186198130 — Identifying the Orthogonality of a Two-Vector Set

$$
\mathbf{u}_1 = {\left[ \begin{array}{c}{\displaystyle \frac{2 \sqrt{2}}{3}} \\ {\displaystyle \frac{1}{3}}\end{array} \right]}, \qquad 
\mathbf{u}_2 = {\left[ \begin{array}{c}- {\displaystyle \frac{1}{3}} \\ {\displaystyle \frac{2 \sqrt{2}}{3}}\end{array} \right]}
$$

Consider the vectors above, and let $\mathbf{Q}$ be an orthogonal linear transformation. Which of the following statements are true?

I. $\mathbf{u}_1 \cdot \mathbf{u}_2 = 0$

II. $\{\mathbf{Q}(\mathbf{u}_1),\mathbf{Q}(\mathbf{u}_2)\}$ is orthogonal

III. $\{\mathbf{Q}(\mathbf{u}_1),\mathbf{Q}(\mathbf{u}_2)\}$ is orthonormal

Since $\mathbf{Q}$ is orthogonal, we have that $\mathbf{Q}(\mathbf{x}) \cdot \mathbf{Q}(\mathbf{y}) = \mathbf{x} \cdot \mathbf{y}$ for any vectors $\mathbf{x}$ and $\mathbf{y}.$

The linear transformation $\mathbf{Q}$ being orthogonal is equivalent to the following:

- The matrix $Q$ of transformation $\mathbf{Q}$ relative to any orthonormal basis (including the standard basis) of $\mathbb{R}^n$ is orthogonal.

- $|| \mathbf{Q}(\mathbf{x}) || = || \mathbf{x} ||.$

- If $\mathbf{x} \perp \mathbf{y}$ then $\mathbf{Q}(\mathbf{x}) \perp \mathbf{Q}(\mathbf{y})$ for any $\mathbf{x}, \mathbf{y} \in \mathbb{R}^n.$ In general, $\mathbf{Q}$ preserves the angle between any two vectors.

- $\mathbf{Q}$ maps any orthogonal (orthonormal) set into an orthogonal (orthonormal) set.

With that in mind, let's examine our statements.

- Statement I is true. Indeed,
$$
\mathbf{u}_1\cdot\mathbf{u}_2 = {\left[ \begin{array}{c}{\displaystyle \frac{2 \sqrt{2}}{3}} \\ {\displaystyle \frac{1}{3}}\end{array} \right]} \cdot {\left[ \begin{array}{c}- {\displaystyle \frac{1}{3}} \\ {\displaystyle \frac{2 \sqrt{2}}{3}}\end{array} \right]} = -\dfrac{2\sqrt{2}}{9}+\dfrac{2\sqrt{2}}{9} = 0.
$$

- Statement II is true. Indeed, $\mathbf{Q}(\mathbf{u}_1) \perp \mathbf{Q}(\mathbf{u}_2)$ since

$$
\mathbf{Q}(\mathbf{u}_1)\cdot\mathbf{Q}(\mathbf{u}_2) = \mathbf{u}_1\cdot\mathbf{u}_2 = 0.
$$

- Statement III is true. Indeed, both $\mathbf{Q}(\mathbf{u}_1)$ and $\mathbf{Q}(\mathbf{u}_2)$ are unit vectors:

$$
\begin{aligned}‖Q({u}_{1})‖ & =‖{u}_{1}‖=\sqrt{\left(\frac{2\sqrt{2}}{3}\right)^{2}+\left(\frac{1}{3}\right)^{2}}=1 \\ ‖Q({u}_{2})‖ & =‖{u}_{2}‖=\sqrt{\left(-\frac{1}{3}\right)^{2}+\left(\frac{2\sqrt{2}}{3}\right)^{2}}=1\end{aligned}
$$

Therefore, the correct answer is "I, II, and III."

## Representative practice (first three per skill; full bank in practice.json)

### Applying the Angle Preserving Property of Orthogonal Linear Transformations (12 captured questions)

Question 17592186198978 — question.difficulty/easy

Let $Q$ be an orthogonal linear transformation. Find $‖Q(x)‖$, where $x=\begin{bmatrix}2 \\ 4 \\ \sqrt{5}\end{bmatrix}.$

Solution: Since $Q$ is orthogonal, we have that $Q(x)\cdot Q(y)=x\cdot y$ for any vectors $x$ and $y.$

The linear transformation $Q$ being orthogonal is equivalent to the following:

- The matrix $Q$ of transformation $Q$ relative to any orthonormal basis (including the standard basis) of ${R}^{n}$ is orthogonal.

- $||Q(x)||=||x||.$

- If $x⊥y$ then $Q(x)⊥Q(y)$ for any $x,y\in {R}^{n}.$ In general, $Q$ preserves the angle between any two vectors.

- $Q$ maps any orthogonal (orthonormal) set into an orthogonal (orthonormal) set.

In this case, since $Q$ is orthogonal, we have 

$$
\begin{aligned}‖Q(x)‖ & =‖x‖ \\  & =\sqrt{{x}_{1}^{2}+{x}_{2}^{2}+{x}_{3}^{2}} \\  & =\sqrt{{2}^{2}+{4}^{2}+{(\sqrt{5})}^{2}} \\  & =5.\end{aligned}
$$

Answer selection: 5

Question 17592186198979 — question.difficulty/easy

Let $Q$ be an orthogonal linear transformation. Find $Q(x)\cdot Q(y)$, where $x=\begin{bmatrix}1 \\ -1 \\ 1\end{bmatrix}$ and $y=\begin{bmatrix}-2 \\ 1 \\ -2\end{bmatrix}.$

Solution: Since $Q$ is orthogonal, we have that $Q(x)\cdot Q(y)=x\cdot y$ for any vectors $x$ and $y.$

The linear transformation $Q$ being orthogonal is equivalent to the following:

- The matrix $Q$ of transformation $Q$ relative to any orthonormal basis (including the standard basis) of ${R}^{n}$ is orthogonal.

- $||Q(x)||=||x||.$

- If $x⊥y$ then $Q(x)⊥Q(y)$ for any $x,y\in {R}^{n}.$ In general, $Q$ preserves the angle between any two vectors.

- $Q$ maps any orthogonal (orthonormal) set into an orthogonal (orthonormal) set.

In this case, since $Q$ is orthogonal, we have 

$$
\begin{aligned}Q(x)\cdot Q(y) & =x\cdot y \\  & =1\cdot (-2)+(-1)\cdot 1+1\cdot (-2) \\  & =-5.\end{aligned}
$$

Answer selection: -5

Question 17592186284757 — question.difficulty/easy

Let $Q$ be an orthogonal linear transformation. Find $‖Q(x)‖$, where $x=\begin{bmatrix}-1 \\ 3 \\ \sqrt{6}\end{bmatrix}.$

Solution: Since $Q$ is orthogonal, we have that $Q(x)\cdot Q(y)=x\cdot y$ for any vectors $x$ and $y.$

The linear transformation $Q$ being orthogonal is equivalent to the following:

- The matrix $Q$ of transformation $Q$ relative to any orthonormal basis (including the standard basis) of ${R}^{n}$ is orthogonal.

- $||Q(x)||=||x||.$

- If $x⊥y$ then $Q(x)⊥Q(y)$ for any $x,y\in {R}^{n}.$ In general, $Q$ preserves the angle between any two vectors.

- $Q$ maps any orthogonal (orthonormal) set into an orthogonal (orthonormal) set.

In this case, since $Q$ is orthogonal, we have 

$$
\begin{aligned}‖Q(x)‖ & =‖x‖ \\  & =\sqrt{{x}_{1}^{2}+{x}_{2}^{2}+{x}_{3}^{2}} \\  & =\sqrt{(-1)^{2}+{3}^{2}+{(\sqrt{6})}^{2}} \\  & =4.\end{aligned}
$$

Answer selection: 4

### Identifying the Orthogonality of a Two-Vector Set (15 captured questions)

Question 17592186198749 — question.difficulty/easy

$$
{u}_{1}=\begin{bmatrix}9 \\ 6\end{bmatrix},\,{u}_{2}=\begin{bmatrix}2 \\ -3\end{bmatrix}
$$

Consider the vectors above, and let $Q$ be an orthogonal linear transformation. Which of the following statements are true?

Select all that apply.

Solution: Since $Q$ is orthogonal, we have that $Q(x)\cdot Q(y)=x\cdot y$ for any vectors $x$ and $y.$

The linear transformation $Q$ being orthogonal is equivalent to the following:

- The matrix $Q$ of transformation $Q$ relative to any orthonormal basis (including the standard basis) of ${R}^{n}$ is orthogonal.

- $||Q(x)||=||x||.$

- If $x⊥y$ then $Q(x)⊥Q(y)$ for any $x,y\in {R}^{n}.$ In general, $Q$ preserves the angle between any two vectors.

- $Q$ maps any orthogonal (orthonormal) set into an orthogonal (orthonormal) set.

With that in mind, let's examine our statements.

- Statement ${u}_{1}\cdot {u}_{2}=0$ is true. Indeed,

$$
{u}_{1}\cdot {u}_{2}=\begin{bmatrix}9 \\ 6\end{bmatrix}\cdot \begin{bmatrix}2 \\ -3\end{bmatrix}=18-18=0.
$$

- Statement “${Q({u}_{1}),Q({u}_{2})}$ is orthogonal” is true. Indeed, $Q({u}_{1})⊥Q({u}_{2})$ since

$$
Q({u}_{1})\cdot Q({u}_{2})={u}_{1}\cdot {u}_{2}=0.
$$

- Statement “${Q({u}_{1}),Q({u}_{2})}$ is orthonormal” is false. Notice that, for example, $Q({u}_{1})$ is not a unit vector since

$$
‖Q({u}_{1})‖=‖{u}_{1}‖=\sqrt{{9}^{2}+{6}^{2}}\ne 1.
$$

Therefore, the correct answer is ${u}_{1}\cdot {u}_{2}=0$; “${Q({u}_{1}),Q({u}_{2})}$ is orthogonal” only.

Answer ${Q({u}_{1}),Q({u}_{2})}$ is orthogonal: true

Answer ${Q({u}_{1}),Q({u}_{2})}$ is orthonormal: false

Answer ${u}_{1}\cdot {u}_{2}=0$: true

Answer None of the above: false

Question 17592186198750 — question.difficulty/easy

$$
{u}_{1}=\begin{bmatrix}-\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}}\end{bmatrix},\,{u}_{2}=\begin{bmatrix}\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}}\end{bmatrix}
$$

Consider the vectors above, and let $Q$ be an orthogonal linear transformation. Which of the following statements are true?

Select all that apply.

Solution: Since $Q$ is orthogonal, we have that $Q(x)\cdot Q(y)=x\cdot y$ for any vectors $x$ and $y.$

The linear transformation $Q$ being orthogonal is equivalent to the following:

- The matrix $Q$ of transformation $Q$ relative to any orthonormal basis (including the standard basis) of ${R}^{n}$ is orthogonal.

- $||Q(x)||=||x||.$

- If $x⊥y$ then $Q(x)⊥Q(y)$ for any $x,y\in {R}^{n}.$ In general, $Q$ preserves the angle between any two vectors.

- $Q$ maps any orthogonal (orthonormal) set into an orthogonal (orthonormal) set.

With that in mind, let's examine our statements.

- Statement ${u}_{1}\cdot {u}_{2}=0$ is true. Indeed,

$$
{u}_{1}\cdot {u}_{2}=\begin{bmatrix}-\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}}\end{bmatrix}\cdot \begin{bmatrix}\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}}\end{bmatrix}=-\frac{1}{2}+\frac{1}{2}=0.
$$

- Statement “${Q({u}_{1}),Q({u}_{2})}$ is orthogonal” is true. Indeed, $Q({u}_{1})⊥Q({u}_{2})$ since

$$
Q({u}_{1})\cdot Q({u}_{2})={u}_{1}\cdot {u}_{2}=0.
$$

- Statement “${Q({u}_{1}),Q({u}_{2})}$ is orthonormal” is true. Indeed, both $Q({u}_{1})$ and $Q({u}_{2})$ are unit vectors:

$$
\begin{aligned}‖Q({u}_{1})‖ & =‖{u}_{1}‖=\sqrt{\left(-\frac{1}{\sqrt{2}}\right)^{2}+\left(\frac{1}{\sqrt{2}}\right)^{2}}=1 \\ ‖Q({u}_{2})‖ & =‖{u}_{2}‖=\sqrt{\left(\frac{1}{\sqrt{2}}\right)^{2}+\left(\frac{1}{\sqrt{2}}\right)^{2}}=1\end{aligned}
$$

Therefore, the correct answer is ${u}_{1}\cdot {u}_{2}=0$; “${Q({u}_{1}),Q({u}_{2})}$ is orthogonal”; “${Q({u}_{1}),Q({u}_{2})}$ is orthonormal”.

Answer ${Q({u}_{1}),Q({u}_{2})}$ is orthogonal: true

Answer ${Q({u}_{1}),Q({u}_{2})}$ is orthonormal: true

Answer ${u}_{1}\cdot {u}_{2}=0$: true

Answer None of the above: false

Question 17592186284748 — question.difficulty/moderate

$$
{u}_{1}=\begin{bmatrix}2 \\ 3 \\ 5\end{bmatrix},\,{u}_{2}=\begin{bmatrix}1 \\ 4 \\ -1\end{bmatrix},\,{u}_{3}=\begin{bmatrix}3 \\ 3 \\ -3\end{bmatrix}
$$

Consider the vectors above, and let $Q$ be an orthogonal linear transformation. Which of the following statements are true?

Select all that apply.

Solution: Since $Q$ is orthogonal, we have that $Q(x)\cdot Q(y)=x\cdot y$ for any vectors $x$ and $y.$

With that in mind, let's examine our statements.

- Statement ${u}_{1}\cdot {u}_{2}=0$ is false since

$$
{u}_{1}\cdot {u}_{2}=\begin{bmatrix}2 \\ 3 \\ 5\end{bmatrix}\cdot \begin{bmatrix}1 \\ 4 \\ -1\end{bmatrix}=2+12-5=9\ne 0.
$$

- Statement “${Q({u}_{1}),Q({u}_{2}),Q({u}_{3})}$ is orthogonal” is false. Notice that, for example, $Q({u}_{1})⊥̸Q({u}_{2})$ since

$$
Q({u}_{1})\cdot Q({u}_{2})={u}_{1}\cdot {u}_{2}\ne 0.
$$

- Statement “${Q({u}_{1}),Q({u}_{2}),Q({u}_{3})}$ is orthonormal” is false since the set is not even orthogonal.

Therefore, the correct answer is "None of the statements are true."

Answer ${Q({u}_{1}),Q({u}_{2}),Q({u}_{3})}$ is orthogonal: false

Answer ${Q({u}_{1}),Q({u}_{2}),Q({u}_{3})}$ is orthonormal: false

Answer ${u}_{1}\cdot {u}_{2}=0$: false

Answer None of the above: true
