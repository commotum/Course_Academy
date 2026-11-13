# 17592186048729 The Parametric Equations of a Line

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186125899 — Introduction

Suppose that we have a straight line passing through the point $P(3,-1,7)$ and that's parallel to the direction vector $\mathbf{v}={\left[ \begin{array}{c}0 \\ 5 \\ - 3\end{array} \right]}.$ As we know, we can write the vector equation of the line as follows:

$$
\begin{aligned}r & =p+tv \\ r & =\begin{bmatrix}3 \\ -1 \\ 7\end{bmatrix}+t\begin{bmatrix}0 \\ 5 \\ -3\end{bmatrix},\end{aligned}
$$

where $t \in (-\infty,\infty).$

Using the vector equation above, we can create a set of **parametric equations** where we express a general point $(x,y,z)$ in terms of  the parameter $t.$

If we let $\mathbf{r}={\left[ \begin{array}{c}x \\ y \\ z\end{array} \right]}$ be the position vector of the general point $(x,y,z),$ then the above equation can be written as

$$
\begin{aligned}r & =\begin{bmatrix}3 \\ -1 \\ 7\end{bmatrix}+t\begin{bmatrix}0 \\ 5 \\ -3\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}3 \\ -1 \\ 7\end{bmatrix}+t\begin{bmatrix}0 \\ 5 \\ -3\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}3 \\ -1+5t \\ 7-3t\end{bmatrix}.\end{aligned}
$$

So, we have the following system of equations:
$$
\left\{
	{\begin{array}{l}x = 3 \\ y = - 1 + 5 t \\ z = 7 - 3 t\end{array}}
	\right.
$$

The equations in the above system are called the **parametric equations** of the straight line.
Geometrically, the equation states that a point belongs to the line if and only if its coordinates have the form

$$
(3, \: -1+5t, \: 7-3t),
$$

where $t \in (-\infty, \infty).$

![](images/e2/e29ce95cdccb47b97578f6431a96e608f7af9f6709410b221ff517b436896608.png)



### example 17592186124227 — Finding the Vector Equation of a Straight Line Given Parametrically

Consider the straight line given by the following parametric equations: 
$$
\left\{
	{\begin{array}{l}x = 2 + 2 t \\ y = 5 t \\ z = 1 - t\end{array}}
	\right.
$$
What would be the vector equation of the line?

These parametric equations are equivalent to

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}2+2t \\ 5t \\ 1-t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}2 \\ 0 \\ 1\end{bmatrix}+\begin{bmatrix}2t \\ 5t \\ -t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}2 \\ 0 \\ 1\end{bmatrix}+t\begin{bmatrix}2 \\ 5 \\ -1\end{bmatrix} \\ r & =\begin{bmatrix}2 \\ 0 \\ 1\end{bmatrix}+t\begin{bmatrix}2 \\ 5 \\ -1\end{bmatrix},\end{aligned}
$$

where $t \in (-\infty,\infty).$

### example 17592186124228 — Finding a Vector Parallel To a Straight Line Given Parametrically

Consider the straight line given by the following parametric equations:
$$
\left\{
	{\begin{array}{l}x = 5 - t \\ y = 3 \\ z = 1\end{array}}
\right.
$$
Find a vector that is parallel to the line.

First, let's find the corresponding vector equation:

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}5-t \\ 3 \\ 1\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}5 \\ 3 \\ 1\end{bmatrix}+\begin{bmatrix}-t \\ 0 \\ 0\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}5 \\ 3 \\ 1\end{bmatrix}+t\begin{bmatrix}-1 \\ 0 \\ 0\end{bmatrix} \\ r & =\begin{bmatrix}5 \\ 3 \\ 1\end{bmatrix}+t\begin{bmatrix}-1 \\ 0 \\ 0\end{bmatrix},\end{aligned}
$$

where $t \in (-\infty,\infty).$

This implies that the line passes through the point $(5,3,1)$ and is parallel to the vector $\mathbf{v}={\left[ \begin{array}{c}- 1 \\ 0 \\ 0\end{array} \right]}.$

### example 17592186124229 — Finding the Parametric Equations of a Line

Find the parametric equations of the line shown in the figure below.

![](images/53/53386f04f4025fda6ab579113a8ecb53a19f4dc0a77903adc05bac3a71429717.png)

We know that the line passes through the points $P(3,3,-5)$ and $Q(1,0,-1)$. Now, we need to find a direction vector that is parallel to the given line. We can use the vector $\overrightarrow{PQ}$ as follows:

$$
\begin{aligned}v & =\overset{\to }{PQ} \\  & =\overset{\to }{OQ}-\overset{\to }{OP} \\  & =\begin{bmatrix}1 \\ 0 \\ -1\end{bmatrix}-\begin{bmatrix}3 \\ 3 \\ -5\end{bmatrix} \\  & =\begin{bmatrix}-2 \\ -3 \\ 4\end{bmatrix}.\end{aligned}
$$

So, the vector equation of the line is

$$
\begin{aligned}r & =p+tv \\ r & =\begin{bmatrix}3 \\ 3 \\ -5\end{bmatrix}+t\begin{bmatrix}-2 \\ -3 \\ 4\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}3 \\ 3 \\ -5\end{bmatrix}+\begin{bmatrix}-2t \\ -3t \\ 4t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}3-2t \\ 3-3t \\ -5+4t\end{bmatrix}\end{aligned}
$$

where $t \in (-\infty,\infty).$ And finally, the parametric equations:

$$
\left\{\begin{aligned}x &=3-2t \\ y &=3-3t \\ z &=-5+4t\end{aligned}\right.
$$

### example 17592186124230 — Finding the Parametric Equations of a Segment

Find the parametric equations that describe all the points on the line segment $\overline{PQ},$ where $P(1,-5,3)$ and $Q(0, 4, -4).$

First, we need to find a direction vector that is parallel to the line passing through the given points. We can use the vector $\overrightarrow{PQ}$ as follows:

$$
\begin{aligned}v & =\overset{\to }{PQ} \\  & =\overset{\to }{OQ}-\overset{\to }{OP} \\  & =\begin{bmatrix}0 \\ 4 \\ -4\end{bmatrix}-\begin{bmatrix}1 \\ -5 \\ 3\end{bmatrix} \\  & =\begin{bmatrix}-1 \\ 9 \\ -7\end{bmatrix}\end{aligned}
$$

So, the vector equation of the line is

$$
\begin{aligned}r & =p+tv \\ r & =\begin{bmatrix}1 \\ -5 \\ 3\end{bmatrix}+t\begin{bmatrix}-1 \\ 9 \\ -7\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}1 \\ -5 \\ 3\end{bmatrix}+\begin{bmatrix}-t \\ 9t \\ -7t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}1-t \\ -5+9t \\ 3-7t\end{bmatrix}\end{aligned}
$$

where $t \in (-\infty,\infty).$ 

To get the equations for the line segment, we take only $t \in [0,1].$ Notice that substitution of $t=0$ in the above equation gives the coordinates of $P$ and substitution of $t=1$ gives the coordinates of $Q.$

Therefore, the parametric equations of the line segment $\overline{PQ}$ are the following:
$$
{\left\{  \begin{array}{l}x = 1 - t \\ y = - 5 + 9 t \\ z = 3 - 7 t\end{array} \right. }
\qquad\qquad
t \in \big[0, 1 \big]
$$

## Representative practice (first three per skill; full bank in practice.json)

### Finding the Vector Equation of a Straight Line Given Parametrically (11 captured questions)

Question 17592186124854 — None

Consider the straight line given by the following parametric equations:
$$
\displaystyle \left\{  \begin{array}{l}x = 3 - 5 t \\ y = {\displaystyle \frac{1}{2}} + 4 t \\ z = 1 - 2 t\end{array} \right.
$$
What would be the vector equation of the line?

Solution: 

Question 17592186124949 — question.difficulty/easy

Consider the straight line given by the following parametric equations:

$$
\left\{\begin{aligned}x &=5 \\ y &=4t \\ z &=7\end{aligned}\right.
$$

What would be the vector equation of the line?

Solution: These parametric equations are equivalent to

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}5 \\ 4t \\ 7\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}5 \\ 0 \\ 7\end{bmatrix}+\begin{bmatrix}0 \\ 4t \\ 0\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}5 \\ 0 \\ 7\end{bmatrix}+t\begin{bmatrix}0 \\ 4 \\ 0\end{bmatrix} \\ r & =\begin{bmatrix}5 \\ 0 \\ 7\end{bmatrix}+t\begin{bmatrix}0 \\ 4 \\ 0\end{bmatrix},\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

Answer selection: r=\begin{bmatrix}5 \\ 0 \\ 7\end{bmatrix}+t\begin{bmatrix}0 \\ 4 \\ 0\end{bmatrix},\,t\in (-\infty ,\infty )

Question 17592186262682 — question.difficulty/easy

Consider the straight line given by the following parametric equations:

$$
\left\{\begin{aligned}x &=2+4t \\ y &=\frac{3}{4}-2t \\ z &=3+t\end{aligned}\right.
$$

What would be the vector equation of the line?

Solution: These parametric equations are equivalent to

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}2+4t \\ \frac{3}{4}-2t \\ 3+t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}2 \\ \frac{3}{4} \\ 3\end{bmatrix}+\begin{bmatrix}4t \\ -2t \\ t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}2 \\ \frac{3}{4} \\ 3\end{bmatrix}+t\begin{bmatrix}4 \\ -2 \\ 1\end{bmatrix} \\ r & =\begin{bmatrix}2 \\ \frac{3}{4} \\ 3\end{bmatrix}+t\begin{bmatrix}4 \\ -2 \\ 1\end{bmatrix},\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

Answer selection: r=\begin{bmatrix}2 \\ \frac{3}{4} \\ 3\end{bmatrix}+t\begin{bmatrix}4 \\ -2 \\ 1\end{bmatrix},\,t\in (-\infty ,\infty )

### Finding a Vector Parallel To a Straight Line Given Parametrically (14 captured questions)

Question 17592186124779 — question.difficulty/moderate

Consider the straight line given by the following parametric equations:

$$
\left\{\begin{aligned}x &=3t-12 \\ y &=-5-7t \\ z &=\frac{3}{4}t+\frac{1}{5}\end{aligned}\right.
$$

Find a vector that is parallel to the line.

Solution: First, let's find the corresponding vector equation:

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}3t-12 \\ -5-7t \\ \frac{3}{4}t+\frac{1}{5}\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}-12 \\ -5 \\ \frac{1}{5}\end{bmatrix}+\begin{bmatrix}3t \\ -7t \\ \frac{3}{4}t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}-12 \\ -5 \\ \frac{1}{5}\end{bmatrix}+t\begin{bmatrix}3 \\ -7 \\ \frac{3}{4}\end{bmatrix} \\ r & =\begin{bmatrix}-12 \\ -5 \\ \frac{1}{5}\end{bmatrix}+t\begin{bmatrix}3 \\ -7 \\ \frac{3}{4}\end{bmatrix},\end{aligned}
$$

where $t\in (-\infty ,\infty ).$ 

This implies that the straight line passes through the point $\left(-12,-5,\frac{1}{5}\right)$ and is parallel to the vector $v=\begin{bmatrix}3 \\ -7 \\ \frac{3}{4}\end{bmatrix}.$

Answer selection: \begin{bmatrix}3 \\ -7 \\ \frac{3}{4}\end{bmatrix}

Question 17592186124855 — None

Consider the straight line given by the following parametric equations:
$$
\displaystyle \left\{  \begin{array}{l}x = - 2 + 6 t \\ y = 4 t \\ z = 3 - t\end{array} \right.
$$
Find a vector that is parallel to the line.

Solution: 

Question 17592186262694 — question.difficulty/moderate

Consider the straight line given by the following parametric equations:

$$
\left\{\begin{aligned}x &=\frac{1}{3}t-2 \\ y &=5-4t \\ z &=2t+\frac{1}{7}\end{aligned}\right.
$$

Find a vector that is parallel to the line.

Solution: First, let's find the corresponding vector equation:

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}\frac{1}{3}t-2 \\ 5-4t \\ 2t+\frac{1}{7}\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}-2 \\ 5 \\ \frac{1}{7}\end{bmatrix}+\begin{bmatrix}\frac{1}{3}t \\ -4t \\ 2t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}-2 \\ 5 \\ \frac{1}{7}\end{bmatrix}+t\begin{bmatrix}\frac{1}{3} \\ -4 \\ 2\end{bmatrix} \\ r & =\begin{bmatrix}-2 \\ 5 \\ \frac{1}{7}\end{bmatrix}+t\begin{bmatrix}\frac{1}{3} \\ -4 \\ 2\end{bmatrix},\end{aligned}
$$

where $t\in (-\infty ,\infty ).$  

This implies that the straight line passes through the point $\left(-2,5,\frac{1}{7}\right)$  and is parallel to the vector $v=\begin{bmatrix}\frac{1}{3} \\ -4 \\ 2\end{bmatrix}.$

Answer selection: \begin{bmatrix}\frac{1}{3} \\ -4 \\ 2\end{bmatrix}

### Finding the Parametric Equations of a Line (15 captured questions)

Question 17592186124845 — question.difficulty/easy

Find the parametric equations of the straight line that passes through $P(5,-10,2)$ and is parallel to $v=⟨-6,-2,1⟩.$

Solution: First, the vector equation of the line is 

$$
\begin{aligned}r & =p+tv \\ r & =\begin{bmatrix}5 \\ -10 \\ 2\end{bmatrix}+t\begin{bmatrix}-6 \\ -2 \\ 1\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}5 \\ -10 \\ 2\end{bmatrix}+\begin{bmatrix}-6t \\ -2t \\ t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}5-6t \\ -10-2t \\ 2+t\end{bmatrix},\end{aligned}
$$

where $t\in (-\infty ,\infty ).$ Therefore, the parametric equations are:

$$
\left\{\begin{aligned}x &=5-6t \\ y &=-10-2t \\ z &=2+t\end{aligned}\right.
$$

Answer selection: \left\{\begin{aligned}x &=5-6t \\ y &=-10-2t \\ z &=2+t\end{aligned}\right.

Question 17592186124950 — question.difficulty/moderate

Find the parametric equations of the line that passes through the points $P(1,4,-2)$ and $Q(5,3,0).$

Solution: We know that the line passes through the points $P(1,4,-2)$ and $Q(5,3,0).$ Now, we need to find a direction vector that is parallel to the given line. We can use the vector $\overset{\to }{PQ}$ as follows:

$$
\begin{aligned}v & =\overset{\to }{PQ} \\  & =\overset{\to }{OQ}-\overset{\to }{OP} \\  & =\begin{bmatrix}5 \\ 3 \\ 0\end{bmatrix}-\begin{bmatrix}1 \\ 4 \\ -2\end{bmatrix} \\  & =\begin{bmatrix}4 \\ -1 \\ 2\end{bmatrix}\end{aligned}
$$

So, the vector equation of the line is

$$
\begin{aligned}r & =p+tv \\ r & =\begin{bmatrix}1 \\ 4 \\ -2\end{bmatrix}+t\begin{bmatrix}4 \\ -1 \\ 2\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}1 \\ 4 \\ -2\end{bmatrix}+\begin{bmatrix}4t \\ -t \\ 2t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}1+4t \\ 4-t \\ -2+2t\end{bmatrix}\end{aligned}
$$

where $t\in (-\infty ,\infty ).$ And finally, the parametric equations:

$$
\left\{\begin{aligned}x &=1+4t \\ y &=4-t \\ z &=-2+2t\end{aligned}\right.
$$

Answer selection: \left\{\begin{aligned}x &=1+4t \\ y &=4-t \\ z &=-2+2t\end{aligned}\right.

Question 17592186262695 — question.difficulty/moderate

Find the parametric equations of the line that passes through the points $P(2,-5,4)$ and $Q(3,-2,2).$

Solution: We need to find a direction vector that is parallel to the given line. We can use the vector $\overset{\to }{PQ}$ as follows:

$$
\begin{aligned}v & =\overset{\to }{PQ} \\  & =\overset{\to }{OQ}-\overset{\to }{OP} \\  & =\begin{bmatrix}3 \\ -2 \\ 2\end{bmatrix}-\begin{bmatrix}2 \\ -5 \\ 4\end{bmatrix} \\  & =\begin{bmatrix}1 \\ 3 \\ -2\end{bmatrix}\end{aligned}
$$

So, the vector equation of the line is

$$
\begin{aligned}r & =p+tv \\ r & =\begin{bmatrix}2 \\ -5 \\ 4\end{bmatrix}+t\begin{bmatrix}1 \\ 3 \\ -2\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}2 \\ -5 \\ 4\end{bmatrix}+\begin{bmatrix}t \\ 3t \\ -2t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}2+t \\ -5+3t \\ 4-2t\end{bmatrix}\end{aligned}
$$

where $t\in (-\infty ,\infty ).$ And finally, the parametric equations:

$$
\left\{\begin{aligned}x &=2+t \\ y &=-5+3t \\ z &=4-2t\end{aligned}\right.
$$

Answer selection: \left\{\begin{aligned}x &=2+t \\ y &=-5+3t \\ z &=4-2t\end{aligned}\right.

### Finding the Parametric Equations of a Segment (11 captured questions)

Question 17592186124846 — question.difficulty/moderate

Fill in the missing parts in the parametric equations below that describe all the points on the line segment $\overset{―}{PQ},$ where $P(1,4,-2)$ and $Q(-2,3,1).$

| $x=$ | {{field-1}} | $t\in [0,$ {{field-2}} $]$ |
| --- | --- | --- |
| $y=$ | $4-t$ |  |
| $z=$ | {{field-3}} |  |

Solution: First, we need to find a direction vector that is parallel to the line passing through the given points. We can use the vector $\overset{\to }{PQ}$ as follows:

$$
\begin{aligned}v & =\overset{\to }{PQ} \\  & =\overset{\to }{OQ}-\overset{\to }{OP} \\  & =\begin{bmatrix}-2 \\ 3 \\ 1\end{bmatrix}-\begin{bmatrix}1 \\ 4 \\ -2\end{bmatrix} \\  & =\begin{bmatrix}-3 \\ -1 \\ 3\end{bmatrix}\end{aligned}
$$

So, the vector equation of the line is

$$
\begin{aligned}r & =p+tv \\ r & =\begin{bmatrix}1 \\ 4 \\ -2\end{bmatrix}+t\begin{bmatrix}-3 \\ -1 \\ 3\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}1 \\ 4 \\ -2\end{bmatrix}+\begin{bmatrix}-3t \\ -t \\ 3t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}1-3t \\ 4-t \\ -2+3t\end{bmatrix}\end{aligned}
$$

where $t\in (-\infty ,\infty ).$ 

To get the equations for the line segment, we take only $t\in [0,1].$ Notice that substitution of $t=0$ in the above equation gives the coordinates of $P$ and substitution of $t=1$ gives the coordinates of $Q.$

Therefore, the parametric equations of the line segment $\overset{―}{PQ}$ are the following:

$$
\left\{\begin{aligned}x &=1-3t \\ y &=4-t \\ z &=-2+3t\end{aligned}\right.\,\,t\in [0,1]
$$

Answer field-1: 1-3t

Answer field-2: 1

Answer field-3: -2+3t

Question 17592186124847 — question.difficulty/easy

Fill in the missing parts in the parametric equations below that describe all the points on the line segment $\overset{―}{PQ},$ where $P(-5,7,1)$ and $Q(-4,-1,6).$

| $x=$ | {{field-1}} | $t\in [$ {{field-2}} $,1]$ |
| --- | --- | --- |
| $y=$ | $7-8t$ |  |
| $z=$ | $1+5t$ |  |

Solution: First, we need to find a direction vector that is parallel to the line passing through the given points. We can use the vector $\overset{\to }{PQ}$ as follows:

$$
\begin{aligned}v & =\overset{\to }{PQ} \\  & =\overset{\to }{OQ}-\overset{\to }{OP} \\  & =\begin{bmatrix}-4 \\ -1 \\ 6\end{bmatrix}-\begin{bmatrix}-5 \\ 7 \\ 1\end{bmatrix} \\  & =\begin{bmatrix}1 \\ -8 \\ 5\end{bmatrix}\end{aligned}
$$

So, the vector equation of the line is

$$
\begin{aligned}r & =p+tv \\ r & =\begin{bmatrix}-5 \\ 7 \\ 1\end{bmatrix}+t\begin{bmatrix}1 \\ -8 \\ 5\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}-5 \\ 7 \\ 1\end{bmatrix}+\begin{bmatrix}t \\ -8t \\ 5t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}-5+t \\ 7-8t \\ 1+5t\end{bmatrix}\end{aligned}
$$

where $t\in (-\infty ,\infty ).$ 

To get the equations for the line segment, we take only $t\in [0,1].$ Notice that substitution of $t=0$ in the above equation gives the coordinates of $P$ and substitution of $t=1$ gives the coordinates of $Q.$

Therefore, the parametric equations of the line segment $\overset{―}{PQ}$ are the following:

$$
\left\{\begin{aligned}x &=-5+t \\ y &=7-8t \\ z &=1+5t\end{aligned}\right.\,\,t\in [0,1]
$$

Answer field-1: -5+t

Answer field-2: 0

Question 17592186290479 — question.difficulty/moderate

Fill in the missing parts in the parametric equations below that describe all the points on the line segment $\overset{―}{PQ},$ where $P(5,0,-1)$ and $Q(7,2,2).$

| $x=$ | {{field-1}} | $t\in [$ {{field-2}} $,1]$ |
| --- | --- | --- |
| $y=$ | {{field-3}} |  |
| $z=$ | $-1+3t$ |  |

Solution: First, we need to find a direction vector that is parallel to the line passing through the given points. We can use the vector $\overset{\to }{PQ}$ as follows:

$$
\begin{aligned}v & =\overset{\to }{PQ} \\  & =\overset{\to }{OQ}-\overset{\to }{OP} \\  & =\begin{bmatrix}7 \\ 2 \\ 2\end{bmatrix}-\begin{bmatrix}5 \\ 0 \\ -1\end{bmatrix} \\  & =\begin{bmatrix}2 \\ 2 \\ 3\end{bmatrix}\end{aligned}
$$

So, the vector equation of the line is

$$
\begin{aligned}r & =p+tv \\ r & =\begin{bmatrix}5 \\ 0 \\ -1\end{bmatrix}+t\begin{bmatrix}2 \\ 2 \\ 3\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}5 \\ 0 \\ -1\end{bmatrix}+\begin{bmatrix}2t \\ 2t \\ 3t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}5+2t \\ 2t \\ -1+3t\end{bmatrix}\end{aligned}
$$

where $t\in (-\infty ,\infty ).$ 

To get the equations for the line segment, we take only $t\in [0,1].$ Notice that substitution of $t=0$ in the above equation gives the coordinates of $P$ and substitution of $t=1$ gives the coordinates of $Q.$

Therefore, the parametric equations of the line segment $\overset{―}{PQ}$ are the following:

$$
\left\{\begin{aligned}x &=5+2t \\ y &=2t \\ z &=-1+3t\end{aligned}\right.\,\,t\in [0,1]
$$

Answer field-1: 5+2t

Answer field-2: 0

Answer field-3: 2t
