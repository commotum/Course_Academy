# 17592186050001 Calculating the Eigenvalues of a 2x2 Matrix

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186093438 — Introduction

Consider the matrix $A= {\left[ \begin{array}{cc}2 & 5 \\ - 1 & - 4\end{array} \right]}.$ How can we find its eigenvalues?

By definition, we need to find the value(s) of $\,\lambda\,$ such that $\,A\mathbf{\color{blue}v} = \lambda \mathbf{\color{blue}v}\,$ is true for some *non-zero* vector $\mathbf{\color{blue}v}.$ Let's re-write this equation as follows:

$$
\begin{aligned}Av & =\lambda v \\ Av-\lambda v & =0 \\ Av-\lambda Iv & =0 \\ (A-\lambda I)v & =0\end{aligned}
$$

The final equation above tells us that there should be at least one non-zero vector $\mathbf{\color{blue}v}$ that lies in $\textrm{Null}(A-\lambda I)$, the null space of the matrix $A-\lambda I.$ As a result, the invertible matrix theorem tells us that the matrix $\, A-\lambda I \,$ must be singular, meaning $\det(A-\lambda I) = 0.$

We've reduced the problem to finding the values of $\lambda$ that satisfy the equation

$$
\det(A-\lambda I) = 0,
$$

which is called the **characteristic equation** of the matrix $A$. So, let's solve it!

First, we write down the matrix $A-\lambda I\mathbin{:}$

$$
\begin{aligned}A\,-\,\lambda I & =\begin{bmatrix}2 & 5 \\ -1 & -4\end{bmatrix}\,-\,\lambda \begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}2\,-\,\lambda  & 5 \\ -1 & -4\,-\,\lambda \end{bmatrix}\end{aligned}
$$

Then, we solve the characteristic equation $\det(A-\lambda I) = 0\mathbin{:}$

$$
\begin{aligned}\det (A-\lambda I) & =0 \\ \begin{vmatrix}2-\lambda  & 5 \\ -1 & -4-\lambda \end{vmatrix} & =0 \\ (2-\lambda )(-4-\lambda )-5\cdot (-1) & =0 \\ -8-2\lambda +4\lambda +{\lambda }^{2}+5 & =0 \\ {\lambda }^{2}+2\lambda -3 & =0 \\ (\lambda +3)(\lambda -1) & =0\end{aligned}
$$

Therefore, the eigenvalues of $A$ are $\lambda=-3$ and $\lambda=1.$



### example 17592186092074 — Finding the Characteristic Equation of a Matrix

Find the characteristic equation of the matrix 
$$
A=
{\left[ \begin{array}{cc}2 & 4 \\ 3 & 2\end{array} \right]}.
$$

First, we find the matrix $\, A-\lambda I\mathbin{:}$
﻿﻿﻿$A - \lambda I = 
{\left[ \begin{array}{cc}2 - \lambda  & 4 \\ 3 & 2 - \lambda \end{array} \right]}.$

Then, the characteristic equation is

$$
\begin{aligned}\det (A-\lambda I) & =0 \\ \begin{vmatrix}2-\lambda  & 4 \\ 3 & 2-\lambda \end{vmatrix} & =0 \\ (2-\lambda )(2-\lambda )-4\cdot 3 & =0 \\ 4-4\lambda +{\lambda }^{2}-12 & =0 \\ {\lambda }^{2}-4\lambda -8 & =0.\end{aligned}
$$

### tutorial 17592186093439 — The Number of Real Eigenvalues of a 2x2 Matrix

The characteristic equation of any $2 \!\times\! 2$ matrix $A$ is always a quadratic equation, which implies that $A$ has at most $2$ eigenvalues. Here are the all possible cases:

- Two distinct real eigenvalues

- One repeated real eigenvalue (or, equivalently, two real eigenvalues that are the same)

- No real eigenvalues (or, equivalently, two complex eigenvalues)



### example 17592186092076 — Computing the Eigenvalues of a Matrix With Two Distinct Eigenvalues

Find all real eigenvalues of the matrix $A={\left[ \begin{array}{cc}10 & 3 \\ 6 & 7\end{array} \right]}.$

Let's start by writing the matrix $A - \lambda I\mathbin{:}$
﻿﻿$A - \lambda I = 
{\left[ \begin{array}{cc}10 - \lambda  & 3 \\ 6 & 7 - \lambda \end{array} \right]}$

Now, let's find and solve the characteristic equation $\det(A-\lambda I) = 0\mathbin{:}$

$$
\begin{aligned}\det (A-\lambda I) & =0 \\ \begin{vmatrix}10-\lambda  & 3 \\ 6 & 7-\lambda \end{vmatrix} & =0 \\ (10-\lambda )(7-\lambda )-3\cdot 6 & =0 \\ 70-7\lambda -10\lambda +{\lambda }^{2}-18 & =0 \\ {\lambda }^{2}-17\lambda +52 & =0\end{aligned}
$$

Using the quadratic formula, we obtain

$$
\begin{aligned}\lambda  & =\frac{17\pm \sqrt{(-17)^{2}-4\cdot 1\cdot 52}}{2\cdot 1} \\  & =\frac{17\pm \sqrt{81}}{2} \\  & =\frac{17\pm 9}{2} \\  & =13,4.\end{aligned}
$$

Therefore, the eigenvalues are $\lambda=13$ and $\lambda=4.$

### example 17592186092075 — Computing the Eigenvalues of a Matrix With At Most One Distinct Eigenvalue

Find all real eigenvalues of the matrix
$$
B= {\left[ \begin{array}{cc}4 & 0 \\ 0 & 4\end{array} \right]}.
$$

Let's start by writing the matrix $B-\lambda I\mathbin{:}$
$$
B - \lambda I = 
{\left[ \begin{array}{cc}4 - \lambda  & 0 \\ 0 & 4 - \lambda \end{array} \right]}
$$

Now, let's find and solve the characteristic equation $\det(B-\lambda I) = 0\mathbin{:}$

$$
\begin{aligned}\det (B-\lambda I) & =0 \\ \begin{vmatrix}4-\lambda  & 0 \\ 0 & 4-\lambda \end{vmatrix} & =0 \\ (4-\lambda )(4-\lambda )-0\cdot 0 & =0 \\ (\lambda -4)^{2} & =0\end{aligned}
$$

Therefore, the matrix $B$ has only one eigenvalue $\lambda=4,$ which is a double root of the characteristic equation. 

**Note:** We also say that $\lambda=4$ has an **algebraic multiplicity** of $2.$

### example 17592186092077 — Calculating the Eigenvalues of a Triangular/Diagonal Matrix

Find all real eigenvalues of the matrix $A={\left[ \begin{array}{cc}3 & 0 \\ 9 & - 2 \sqrt{3}\end{array} \right]}.$

Let's start by writing the matrix $A - \lambda I \mathbin{:}$
﻿﻿﻿$A - \lambda I = 
{\left[ \begin{array}{cc}3 - \lambda  & 0 \\ 9 & - 2 \sqrt{3} - \lambda \end{array} \right]}$

Now, let's find and solve the characteristic equation $\det (A - \lambda I) = 0\mathbin{:}$

$$
\begin{aligned}\det (A-\lambda I) & =0 \\ \begin{vmatrix}3-\lambda  & 0 \\ 9 & -2\sqrt{3}-\lambda \end{vmatrix} & =0 \\ (3-\lambda )(-2\sqrt{3}-\lambda )-9\cdot 0 & =0 \\ (\lambda -3)(\lambda +2\sqrt{3}) & =0\end{aligned}
$$

So, we get the eigenvalues $\lambda={\color{red}3}$ and $\lambda={\color{blue}-2\sqrt{3}}.$

If we look again at the matrix $\,A={\left[ \begin{array}{cc}{\color{red}3} & 0 \\ 9 & {\color{blue}- 2 \sqrt{3}}\end{array} \right]},$
we see that the eigenvalues are the entries on the main diagonal. This is true in general: the eigenvalues of a *triangular* or *diagonal* matrix are *always* given by the entries on the main diagonal!

**Watch out!** For a general matrix (which is neither triangular nor diagonal), this might not be the case!

## Representative practice (first three per skill; full bank in practice.json)

### Finding the Characteristic Equation of a Matrix (15 captured questions)

Question 17592186092689 — question.difficulty/easy

Find the characteristic equation of the matrix $A=\begin{bmatrix}2 & 2 \\ -8 & -6\end{bmatrix}.$

Solution: First, we find the matrix $\,A-\lambda I:$
﻿﻿﻿

$$
A-\lambda I=\begin{bmatrix}2-\lambda  & 2 \\ -8 & -6-\lambda \end{bmatrix}.
$$

Then, the characteristic equation is

$$
\begin{aligned}\det (A-\lambda I) & =0 \\ \begin{vmatrix}2-\lambda  & 2 \\ -8 & -6-\lambda \end{vmatrix} & =0 \\ (2-\lambda )(-6-\lambda )-(-8)\cdot 2 & =0 \\ -12-2\lambda +6\lambda +{\lambda }^{2}+16 & =0 \\ {\lambda }^{2}+4\lambda +4 & =0.\end{aligned}
$$

Answer selection: {\lambda }^{2}+4\lambda +4=0

Question 17592186092690 — None

Find the characteristic equation of the matrix
$$
\displaystyle B = \begin{bmatrix}5 & 3 \\ 0 & 5\end{bmatrix}.
$$

Solution: 

Question 17592186243988 — question.difficulty/easy

Find the characteristic equation of the matrix 
$$
\displaystyle B=\begin{bmatrix}5 & -1 \\ 0 & 1\end{bmatrix}.
$$

Solution: First, we find the matrix $\,B-\lambda I:$
﻿﻿﻿

$$
B-\lambda I=\begin{bmatrix}5-\lambda  & -1 \\ 0 & 1-\lambda \end{bmatrix}.
$$

Then, the characteristic equation is

$$
\begin{aligned}\det (B-\lambda I) & =0 \\ \begin{vmatrix}5-\lambda  & -1 \\ 0 & 1-\lambda \end{vmatrix} & =0 \\ (5-\lambda )(1-\lambda )-0\cdot (-1) & =0 \\ 5-5\lambda -\lambda +{\lambda }^{2}+0 & =0 \\ {\lambda }^{2}-6\lambda +5 & =0.\end{aligned}
$$

Answer selection: {\lambda }^{2}-6\lambda +5=0

### Computing the Eigenvalues of a Matrix With Two Distinct Eigenvalues (13 captured questions)

Question 17592186092529 — None

Find all real eigenvalues of the matrix
$$
\displaystyle P = \begin{bmatrix}-6 & 3 \\ 3 & 2\end{bmatrix}.
$$

Solution: 

Question 17592186092902 — question.difficulty/easy

Find all real eigenvalues of the matrix 
$$
\displaystyle A=\begin{bmatrix}-4 & 2 \\ 6 & 7\end{bmatrix}.
$$

Solution: Let's start by writing the matrix $A-\lambda I:$
﻿﻿﻿

$$
A-\lambda I=\begin{bmatrix}-4-\lambda  & 2 \\ 6 & 7-\lambda \end{bmatrix}
$$

Now, let's find and solve the characteristic equation $\det (A-\lambda I)=0:$

$$
\begin{aligned}\det (A-\lambda I) & =0 \\ \begin{vmatrix}-4-\lambda  & 2 \\ 6 & 7-\lambda \end{vmatrix} & =0 \\ (-4-\lambda )(7-\lambda )-2\cdot 6 & =0 \\ -28-7\lambda +4\lambda +{\lambda }^{2}-12 & =0 \\ {\lambda }^{2}-3\lambda -40 & =0\end{aligned}
$$

Using the quadratic formula, we obtain

$$
\begin{aligned}\lambda  & =\frac{3\pm \sqrt{(-3)^{2}+4\cdot 1\cdot 40}}{2} \\  & =\frac{3\pm \sqrt{169}}{2} \\  & =\frac{3\pm 13}{2} \\  & =8,-5.\end{aligned}
$$

Therefore, the eigenvalues are $\lambda =8$ and $\lambda =-5.$

Answer selection: $\lambda =8$ and $\lambda =-5$

Question 17592186253608 — question.difficulty/easy

Find all real eigenvalues of the matrix
$$
\displaystyle M=\begin{bmatrix}-4 & 5 \\ 5 & -4\end{bmatrix}.
$$

Solution: Let's start by writing the matrix $M-\lambda I:$
﻿﻿﻿

$$
M-\lambda I=\begin{bmatrix}-4-\lambda  & 5 \\ 5 & -4-\lambda \end{bmatrix}.
$$

Now, let's find and solve the characteristic equation $\det (M-\lambda I)=0:$

$$
\begin{aligned}\det (M-\lambda I) & =0 \\ \begin{vmatrix}-4-\lambda  & 5 \\ 5 & -4-\lambda \end{vmatrix} & =0 \\ (-4-\lambda )(-4-\lambda )-5\cdot 5 & =0 \\ 16+4\lambda +4\lambda +{\lambda }^{2}-25 & =0 \\ {\lambda }^{2}+8\lambda -9 & =0\end{aligned}
$$

Using the quadratic formula, we obtain

$$
\begin{aligned}\lambda  & =\frac{-8\pm \sqrt{{8}^{2}+4\cdot 1\cdot 9}}{2} \\  & =\frac{-8\pm \sqrt{100}}{2} \\  & =\frac{-8\pm 10}{2} \\  & =1,-9.\end{aligned}
$$

Therefore, the eigenvalues are $\lambda =1$ and $\lambda =-9.$

Answer selection: $\lambda =1$ and $\lambda =-9$

### Computing the Eigenvalues of a Matrix With At Most One Distinct Eigenvalue (13 captured questions)

Question 17592186092691 — question.difficulty/moderate

Find all real eigenvalues of the matrix
$$
\displaystyle Q=\begin{bmatrix}-6 & -3 \\ 2 & -10\end{bmatrix}.
$$

Solution: Let's start by writing the matrix $Q-\lambda I:$
﻿﻿﻿

$$
Q-\lambda I=\begin{bmatrix}-6-\lambda  & -3 \\ 2 & -10-\lambda \end{bmatrix}
$$

Now, let's find and solve the characteristic equation $\det (Q-\lambda I)=0:$

$$
\begin{aligned}\det (Q-\lambda I) & =0 \\ \begin{vmatrix}-6-\lambda  & -3 \\ 2 & -10-\lambda \end{vmatrix} & =0 \\ (-6-\lambda )(-10-\lambda )-(-3)\cdot 2 & =0 \\ 60+6\lambda +10\lambda +{\lambda }^{2}+6 & =0 \\ {\lambda }^{2}+16\lambda +66 & =0\end{aligned}
$$

Computing the discriminant of the quadratic equation above, we obtain 

$$
\begin{aligned}D & ={16}^{2}-4\cdot 1\cdot 66 \\  & =256-264 \\  & =-8 \\  & <0.\end{aligned}
$$

Therefore, we conclude that the characteristic equation does not have real solutions, and therefore, $Q$ does not have real eigenvalues.

Answer selection: There are no real eigenvalues

Question 17592186092903 — question.difficulty/easy

Find all real eigenvalues of the matrix
$$
\displaystyle A=\begin{bmatrix}3 & 1 \\ -1 & 1\end{bmatrix}.
$$

Solution: Let's start by writing the matrix $A-\lambda I:$
﻿﻿﻿

$$
A-\lambda I=\begin{bmatrix}3-\lambda  & 1 \\ -1 & 1-\lambda \end{bmatrix}
$$

Now, let's find and solve the characteristic equation $\det (A-\lambda I)=0:$

$$
\begin{aligned}\det (A-\lambda I) & =0 \\ \begin{vmatrix}3-\lambda  & 1 \\ -1 & 1-\lambda \end{vmatrix} & =0 \\ (3-\lambda )(1-\lambda )+1\cdot 1 & =0 \\ 3-3\lambda -\lambda +{\lambda }^{2}+1 & =0 \\ {\lambda }^{2}-4\lambda +4 & =0 \\ (\lambda -2)^{2} & =0.\end{aligned}
$$

Therefore, the matrix $A$ has only one eigenvalue $\lambda =2,$ which is a double root of the characteristic equation.

Answer selection: $\lambda =2$  (double root)

Question 17592186244110 — question.difficulty/moderate

Find all real eigenvalues of the matrix
$$
\displaystyle Q=\begin{bmatrix}5 & 1 \\ -3 & 8\end{bmatrix}.
$$

Solution: Let's start by writing the matrix $Q-\lambda I:$
﻿﻿﻿

$$
Q-\lambda I=\begin{bmatrix}5-\lambda  & 1 \\ -3 & 8-\lambda \end{bmatrix}
$$

Now, let's find and solve the characteristic equation $\det (Q-\lambda I)=0:$

$$
\begin{aligned}\det (Q-\lambda I) & =0 \\ \begin{vmatrix}5-\lambda  & 1 \\ -3 & 8-\lambda \end{vmatrix} & =0 \\ (5-\lambda )(8-\lambda )-(-3)\cdot 1 & =0 \\ 40-5\lambda -8\lambda +{\lambda }^{2}+3 & =0 \\ {\lambda }^{2}-13\lambda +43 & =0.\end{aligned}
$$

Computing the discriminant of the quadratic equation above, we obtain 

$$
\begin{aligned}D & =(-13)^{2}-4\cdot 1\cdot 43 \\  & =169-172 \\  & =-3 \\  & <0.\end{aligned}
$$

Therefore, we conclude that the characteristic equation does not have real solutions and therefore $Q$ does not have real eigenvalues.

Answer selection: There are no real eigenvalues

### Calculating the Eigenvalues of a Triangular/Diagonal Matrix (15 captured questions)

Question 17592186092516 — question.difficulty/easy

Find all real eigenvalues of the matrix
$$
\displaystyle A=\begin{bmatrix}\sqrt{3} & 0 \\ 4 & 2\end{bmatrix}.
$$

Solution: Let's start by writing the matrix $A-\lambda I:$
﻿﻿﻿

$$
A-\lambda I=\begin{bmatrix}\sqrt{3}-\lambda  & 0 \\ 4 & 2-\lambda \end{bmatrix}
$$

Now, let's find and solve the characteristic equation $\det (A-\lambda I)=0:$

$$
\begin{aligned}\det (A-\lambda I) & =0 \\ \begin{vmatrix}\sqrt{3}-\lambda  & 0 \\ 4 & 2-\lambda \end{vmatrix} & =0 \\ (\sqrt{3}-\lambda )(2-\lambda )-0\cdot 4 & =0 \\ (\lambda -\sqrt{3})(\lambda -2) & =0\end{aligned}
$$

Therefore, the eigenvalues are $\lambda =\sqrt{3}$ and $\lambda =2.$

**Note:** The eigenvalues of a triangular (or diagonal) matrix are the entries on the main diagonal.

Answer selection: $\lambda =\sqrt{3}$ and $\lambda =2$

Question 17592186092688 — None

Find all real eigenvalues of the matrix
$$
\displaystyle C = \begin{bmatrix}\sqrt{2} & 0 \\ 0 & -\sqrt{3}\end{bmatrix}.
$$

Solution: 

Question 17592186243993 — question.difficulty/easy

Find all real eigenvalues of the matrix
$$
\displaystyle A=\begin{bmatrix}5 & 0 \\ 2 & 3\end{bmatrix}.
$$

Solution: Let's start by writing the matrix $A-\lambda I:$
﻿﻿﻿

$$
A-\lambda I=\begin{bmatrix}5-\lambda  & 0 \\ 2 & 3-\lambda \end{bmatrix}
$$

Now, let's find and solve the characteristic equation $\det (A-\lambda I)=0:$

$$
\begin{aligned}\det (A-\lambda I) & =0 \\ \begin{vmatrix}5-\lambda  & 0 \\ 2 & 3-\lambda \end{vmatrix} & =0 \\ (5-\lambda )(3-\lambda )-0\cdot 2 & =0 \\ (\lambda -5)(\lambda -3) & =0\end{aligned}
$$

Therefore, the eigenvalues are $\lambda =5$ and $\lambda =3.$

**Note:** The eigenvalues of a triangular (or diagonal) matrix are the entries on the main diagonal.

Answer selection: $\lambda =5$ and $\lambda =3$
