# 17592186048850 The Cartesian Equation of a Line

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121048 — Introduction

Suppose we know that the vector equation of the line $l$ is given by
$$
\mathbf{r} = {\left[ \begin{array}{c}3 \\ - 2 \\ 5\end{array} \right]} + t {\left[ \begin{array}{c}6 \\ 5 \\ - 1\end{array} \right]}, \qquad  t \in (-\infty,\infty)
$$

and we want to rewrite it using Cartesian coordinates. In other words, we want to create an equation that relates $x,$ $y,$ and $z$ to each other.

We can do this using the following $3$ steps.

**Step 1:** Find the parametric equations for the line.

Substituting $\mathbf{r}={\left[ \begin{array}{c}x \\ y \\ z\end{array} \right]}$ into the equation of $l,$ we get

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}3 \\ -2 \\ 5\end{bmatrix}+t\begin{bmatrix}6 \\ 5 \\ -1\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}3+6t \\ -2+5t \\ 5-t\end{bmatrix}.\end{aligned}
$$

So, we have the following system:

$$
\left\{\begin{aligned}x &=3+6t \\ y &=-2+5t \\ z &=5-t\end{aligned}\right.
\qquad \Rightarrow \qquad
\left\{\begin{aligned}\frac{x-3}{6} &=t \\ \frac{y+2}{5} &=t \\ \frac{z-5}{-1} &=t\end{aligned}\right.
$$

**Step 2:** Solve for $t$ in each of the parametric equations.

$$
{\left\{  \begin{array}{l}x = 3 + 6 t \\ y = - 2 + 5 t \\ z = 5 - t\end{array} \right. }
\qquad \Rightarrow \qquad
{\left\{  \begin{array}{l}{\displaystyle \frac{x - 3}{6}} = t \\ {\displaystyle \frac{y + 2}{5}} = t \\ {\displaystyle \frac{z - 5}{- 1}} = t\end{array} \right. }
$$

**Step 3:** Equate the resulting expressions. Because the right-hand side of each equation is equal to $t,$ we can write this system as follows:

$$
\dfrac{x-3}{6}=\dfrac{y+2}{5}=\dfrac{z-5}{-1} = t
$$

We can simplify further by omitting the "$=t$" on the right-hand side, which gives

$$
\dfrac{x-3}{6}=\dfrac{y+2}{5}=\dfrac{z-5}{-1} \,.
$$

And we are done! 

This way of writing the equation of a line is called the **Cartesian equation** or **Cartesian canonical equation** (or simply **canonical equation**).

In general, the Cartesian equation of the straight line that passes through the point $P(x_0,y_0,z_0)$ and is parallel to the vector $\mathbf{v}=\langle v_x, v_y, v_z \rangle$ is given by

$$
\dfrac{x-x_0}{v_x}=\dfrac{y-y_0}{v_y}=\dfrac{z-z_0}{v_z} = t, \qquad t \in (-\infty,\infty).
$$



### example 17592186119637 — Finding the Vector Equation of a Line Given in Canonical Form

Consider the straight line with the canonical equation $$
\displaystyle \dfrac{x}{5}=\dfrac{y+3}{3}=\dfrac{z-2}{1}.
$$ Find the vector equation of the line.

Remember that the Cartesian (canonical) equation of the straight line that passes through the point $P(x_0,y_0,z_0)$ and is parallel to the vector $\mathbf{v}=\langle v_x, v_y, v_z \rangle$ is given by

$$
\dfrac{x-x_0}{v_x}=\dfrac{y-y_0}{v_y}=\dfrac{z-z_0}{v_z} = t, \qquad t \in (-\infty,\infty).
$$

Comparing the above to our given equation

$$
\dfrac{x}{5}=\dfrac{y-(-3)}{3}=\dfrac{z-2}{1},
$$

we find that our line passes through the point $P(0,-3,2)$ and is parallel to $\mathbf{v}=\langle 5,3,1 \rangle.$ Therefore, its vector equation is

$$
\begin{aligned}r & =p+tv \\ r & =\begin{bmatrix}0 \\ -3 \\ 2\end{bmatrix}+t\begin{bmatrix}5 \\ 3 \\ 1\end{bmatrix},\,t\in (-\infty ,\infty ).\end{aligned}
$$

### example 17592186119638 — Finding the Cartesian Equation of a Line Given in Parametric or Vector Form

Consider the straight line with the parametric equations

$$
\left\{\begin{aligned}x &=1-2t \\ y &=4t \\ z &=-2+3t\end{aligned}\right.
$$

for $t \in (-\infty,\infty).$ Find the Cartesian equation of this line.

First, let's find the corresponding vector equation as follows:

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}1-2t \\ 4t \\ -2+3t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}1 \\ 0 \\ -2\end{bmatrix}+\begin{bmatrix}-2t \\ 4t \\ 3t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}1 \\ 0 \\ -2\end{bmatrix}+t\begin{bmatrix}-2 \\ 4 \\ 3\end{bmatrix} \\ r & =\begin{bmatrix}1 \\ 0 \\ -2\end{bmatrix}+t\begin{bmatrix}-2 \\ 4 \\ 3\end{bmatrix},\end{aligned}
$$

where $t \in (-\infty,\infty).$

This implies that the given line passes through the point $P(1,0,-2)$ and is parallel to the vector $\mathbf{v}=\langle -2, 4, 3 \rangle.$ So, its Cartesian (canonical) equation is given by

$$
\dfrac{x-1}{-2}=\dfrac{y}{4}=\dfrac{z-(-2)}{3} = t, 	\qquad t \in (-\infty,\infty).
$$

Simplifying, we reach

$$
\dfrac{x-1}{-2}=\dfrac{y}{4}=\dfrac{z+2}{3}.
$$

### tutorial 17592186121055 — Finding the Cartesian Equation of a Line When a Component of the Direction Vector is Zero

Suppose we want to write the Cartesian equation for the line with the following vector equation:
$$
\mathbf{r} = {\left[ \begin{array}{c}1 \\ 2 \\ 3\end{array} \right]} + t {\left[ \begin{array}{c}4 \\ 5 \\ 0\end{array} \right]}, \qquad  t \in (-\infty,\infty)
$$

Using the usual formula, we get

$$
\dfrac{x-1}{4}=\dfrac{y-2}{5}=\dfrac{z-3}{0} = t,	\qquad t \in (-\infty,\infty),
$$

or equivalently,

$$
\dfrac{x-1}{4}=\dfrac{y-2}{5}=\dfrac{z-3}{0}.
$$

But the above equation is problematic because $\dfrac{z-3}{0}$ involves division by zero.

However, notice that in our line, the $z$ component always maintains the constant value of $z=3\mathbin{:}$

$$
\mathbf{r} = {\left[ \begin{array}{c}1 + 4 t \\ 2 + 5 t \\ 3\end{array} \right]}, \qquad  t \in (-\infty,\infty)
$$

If we solve for $t$ in the parametric equations of the line, we get

$$
{\left\{  \begin{array}{l}x = 1 + 4 t \\ y = 2 + 5 t \\ z = 3\end{array} \right. }
\qquad \Longrightarrow \qquad
{\left\{  \begin{array}{l}{\displaystyle \frac{x - 1}{4}} = t \\ {\displaystyle \frac{y - 2}{5}} = t \\ z = 3 ,\end{array} \right. }
$$

Only the first two equations have right-hand sides equal to $t,$ so we combine them but keep the third equation separate:

$$
\dfrac{x-1}{4}=\dfrac{y-2}{5}, \; z=3
$$

So, it's as if we removed the $\dfrac{z-3}{0}$ part in the original formula and replaced it with $z=3.$



### example 17592186119656 — Finding the Cartesian Equation of a Line When a Component of the Direction Vector is Zero

Find the Cartesian equation for the line with the following vector equation:

$$
\mathbf{r} = {\left[ \begin{array}{c}1 \\ 2 \\ 3\end{array} \right]} + t {\left[ \begin{array}{c}4 \\ 0 \\ 5\end{array} \right]}, \qquad  t \in (-\infty,\infty)
$$

Using the usual formula, we get

$$
\dfrac{x-1}{4}=\dfrac{y-2}{0}=\dfrac{z-3}{5} = t,	\qquad t \in (-\infty,\infty),
$$

or equivalently

$$
\dfrac{x-1}{4}=\dfrac{y-2}{0}=\dfrac{z-3}{5},
$$

which is problematic because $\dfrac{y-2}{0}$ involves division by zero.

However, notice that in our line, the $y$ component always maintains the constant value of $y=2\mathbin{:}$

$$
\mathbf{r} = {\left[ \begin{array}{c}1 + 4 t \\ 2 \\ 3 + 5 t\end{array} \right]}, \qquad  t \in (-\infty,\infty)
$$

So, in the Cartesian equation, we remove the $\dfrac{y-2}{0}$ part and instead write $y=2,$ as follows:

$$
\dfrac{x-1}{4}=\dfrac{z-3}{5}, \; y=2
$$

### example 17592186119639 — Finding the Cartesian Equation of a Line Given Two Points on the Line

Find a Cartesian equation of the line shown in the figure below.

![](images/79/792bf09ff2546903b863a879a2518c42bbd30fdfce652bd4e22b1ad19aefc7c9.png)

We know that the line passes through the points $P\left(-1,1,0\right)$ and $Q\left(5,-1, 0\right).$ Now, we need to find a vector parallel to the given line. Let's consider the vector $\overrightarrow{PQ}$ which is given by
$$
\begin{array}{cc}\overrightarrow{P Q} &  = \langle  5 , - 1 , 0 \rangle  - \langle  - 1 , 1 , 0 \rangle  \\  &  = \langle  6 , - 2 , 0 \rangle  .\end{array}
$$

Using the point $P$ and the vector $\overrightarrow{PQ}$, we have that the Cartesian (canonical) equation of the given line is given by
$$
\dfrac{x-(-1)}{6}=\dfrac{y-1}{-2}=\dfrac{z-0}{0} = t,	\qquad t \in (-\infty,\infty),
$$
or equivalently
$$
\dfrac{x+1}{6}=\dfrac{y-1}{-2}=\dfrac{z}{0}.
$$

But the above equation is problematic because $\dfrac{z}{0}$ involves division by zero.

However, in our line, the $z$ component always maintains the constant value $z=0.$ For example, our two points $P\left(-1,1,0\right)$ and $Q\left(5,-1,0\right)$ both have $z$-coordinates of $z=0.$

So, in the Cartesian equation, we remove the $\dfrac{z}{0}$ part and instead write $z=0,$ as follows:

$$
\dfrac{x+1}{6}=\dfrac{y-1}{-2},\; z=0 .
$$

## Representative practice (first three per skill; full bank in practice.json)

### Finding the Vector Equation of a Line Given in Canonical Form (13 captured questions)

Question 17592186120220 — question.difficulty/easy

Consider the straight line with the canonical equation $\frac{x}{1}=\frac{y+1}{2}=\frac{z}{3}.$ Find the vector equation of the line.

Solution: Remember that the Cartesian (canonical) equation of the straight line that passes through the point $P({x}_{0},{y}_{0},{z}_{0})$ and is parallel to the vector $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$, is given by

$$
\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}}=t,\,t\in (-\infty ,\infty ).
$$

Comparing the above to our given equation

$$
\frac{x}{1}=\frac{y-(-1)}{2}=\frac{z}{3},
$$

we find that our line passes through the point $P(0,-1,0)$ and is parallel to $v=⟨1,2,3⟩.$ Therefore, its vector equation is

$$
\begin{aligned}r & =p+tv \\ r & =\begin{bmatrix}0 \\ -1 \\ 0\end{bmatrix}+t\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix},\,t\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: r=\begin{bmatrix}0 \\ -1 \\ 0\end{bmatrix}+t\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix},\,t\in (-\infty ,\infty )

Question 17592186120245 — None

Find the vector equation of the line $$
\displaystyle \frac{x - 4}{2} = \frac{y - 2}{-3} = \frac{z + 6}{8}.
$$

Solution: 

Question 17592186262705 — question.difficulty/easy

Consider the straight line with the canonical equation $$
\displaystyle \frac{x-4}{3}=\frac{y-7}{-1}=\frac{z+6}{-7}.
$$ Find the vector equation of the line.

Solution: Remember that the Cartesian (canonical) equation of the straight line that passes through the point $P({x}_{0},{y}_{0},{z}_{0})$ and is parallel to the vector $v=⟨{v}_{x},{v}_{y},{v}_{z}⟩$, is given by

$$
\frac{x-{x}_{0}}{{v}_{x}}=\frac{y-{y}_{0}}{{v}_{y}}=\frac{z-{z}_{0}}{{v}_{z}}=t,\,t\in (-\infty ,\infty ).
$$

Comparing the above to our given equation

$$
\frac{x-4}{3}=\frac{y-7}{-1}=\frac{z-(-6)}{-7},
$$

we find that our line passes through the point $P(4,7,-6)$ and is parallel to $v=⟨3,-1,-7⟩.$ Therefore, its vector equation is

$$
\begin{aligned}r & =p+tv \\ r & =\begin{bmatrix}4 \\ 7 \\ -6\end{bmatrix}+t\begin{bmatrix}3 \\ -1 \\ -7\end{bmatrix},\,t\in (-\infty ,\infty ).\end{aligned}
$$

Answer selection: r=\begin{bmatrix}4 \\ 7 \\ -6\end{bmatrix}+t\begin{bmatrix}3 \\ -1 \\ -7\end{bmatrix},\,t\in (-\infty ,\infty )

### Finding the Cartesian Equation of a Line Given in Parametric or Vector Form (16 captured questions)

Question 17592186120221 — question.difficulty/easy

Consider the straight line with the vector equation

$$
r=\begin{bmatrix}0 \\ -5 \\ 5\end{bmatrix}+t\begin{bmatrix}6 \\ 1 \\ -6\end{bmatrix}
$$

for $t\in (-\infty ,\infty ).$ Find the Cartesian equation of this line.

Solution: We have the vector equation 

$$
r=\begin{bmatrix}0 \\ -5 \\ 5\end{bmatrix}+t\begin{bmatrix}6 \\ 1 \\ -6\end{bmatrix},\,t\in (-\infty ,\infty ).
$$

 

This implies that the straight line passes through the point $P(0,-5,5)$ and is parallel to the vector $v=⟨6,1,-6⟩.$ So, its Cartesian (canonical) equation is given by

$$
\frac{x-0}{6}=\frac{y-(-5)}{1}=\frac{z-5}{-6}=t,\,t\in (-\infty ,\infty ).
$$

Simplifying, we reach

$$
\frac{x}{6}=\frac{y+5}{1}=\frac{z-5}{-6}.
$$

Answer selection: \frac{x}{6}=\frac{y+5}{1}=\frac{z-5}{-6}

Question 17592186120244 — question.difficulty/easy

Consider the straight line with the parametric equations

$$
\left\{\begin{aligned}x &=-1+2t \\ y &=2+4t \\ z &=-5+3t\end{aligned}\right.
$$

for $t\in (-\infty ,\infty ).$ Find the Cartesian equation of this line.

Solution: First, let's find the corresponding vector equation as follows:

$$
\begin{aligned}\begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}-1+2t \\ 2+4t \\ -5+3t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}-1 \\ 2 \\ -5\end{bmatrix}+\begin{bmatrix}2t \\ 4t \\ 3t\end{bmatrix} \\ \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}-1 \\ 2 \\ -5\end{bmatrix}+t\begin{bmatrix}2 \\ 4 \\ 3\end{bmatrix} \\ r & =\begin{bmatrix}-1 \\ 2 \\ -5\end{bmatrix}+t\begin{bmatrix}2 \\ 4 \\ 3\end{bmatrix},\end{aligned}
$$

where $t\in (-\infty ,\infty ).$

This implies that the given line passes through the point $P(-1,2,-5)$ and is parallel to the vector $v=⟨2,4,3⟩.$ So, its Cartesian (canonical) equation is given by

$$
\frac{x-(-1)}{2}=\frac{y-2}{4}=\frac{z-(-5)}{3}=t,\,t\in (-\infty ,\infty ).
$$

Simplifying, we reach

$$
\frac{x+1}{2}=\frac{y-2}{4}=\frac{z+5}{3}.
$$

Answer selection: \frac{x+1}{2}=\frac{y-2}{4}=\frac{z+5}{3}

Question 17592186262766 — question.difficulty/easy

Consider the straight line with the vector equation

$$
r=\begin{bmatrix}-2 \\ 3 \\ 3\end{bmatrix}+t\begin{bmatrix}2 \\ -5 \\ 3\end{bmatrix}
$$

for $t\in (-\infty ,\infty ).$ Find the Cartesian equation of this line.

Solution: We have the vector equation 

$$
r=\begin{bmatrix}-2 \\ 3 \\ 3\end{bmatrix}+t\begin{bmatrix}2 \\ -5 \\ 3\end{bmatrix},\,t\in (-\infty ,\infty ).
$$

 

This implies that the straight line passes through the point $P(-2,3,3)$ and is parallel to the vector $v=⟨2,-5,3⟩.$ So, its Cartesian (canonical) equation is given by

$$
\frac{x-(-2)}{2}=\frac{y-3}{-5}=\frac{z-3}{3}=t,\,t\in (-\infty ,\infty ).
$$

Simplifying, we reach

$$
\frac{x+2}{2}=\frac{y-3}{-5}=\frac{z-3}{3}.
$$

Answer selection: \frac{x+2}{2}=\frac{y-3}{-5}=\frac{z-3}{3}

### Finding the Cartesian Equation of a Line When a Component of the Direction Vector is Zero (16 captured questions)

Question 17592186120506 — question.difficulty/moderate

Find the Cartesian equation for the line with the following vector equation:

$$
r=\begin{bmatrix}-1 \\ 1 \\ 0\end{bmatrix}+t\begin{bmatrix}0 \\ 2 \\ -1\end{bmatrix},\,t\in (-\infty ,\infty )
$$

Solution: Using the usual formula, we get

$$
\frac{x-(-1)}{0}=\frac{y-1}{2}=\frac{z-0}{-1}=t,\,t\in (-\infty ,\infty ),
$$

or equivalently

$$
\frac{x+1}{0}=\frac{y-1}{2}=-z,
$$

which is problematic because $\frac{x+1}{0}$ involves division by zero.

However, notice that in our line, the $x$ component always maintains the constant value of $x=-1:$

$$
r=\begin{bmatrix}-1 \\ 1+2t \\ -t\end{bmatrix},\,t\in (-\infty ,\infty )
$$

So, in the Cartesian equation, we remove the $\frac{x+1}{0}$ part and instead write $x=-1,$ as follows:

$$
\frac{y-1}{2}=-z,\,x=-1
$$

Answer selection: \frac{y-1}{2}=-z,\,x=-1

Question 17592186120507 — question.difficulty/moderate

Find the Cartesian equation for the line with the following vector equation:

$$
r=\begin{bmatrix}2 \\ 7 \\ 1\end{bmatrix}+t\begin{bmatrix}5 \\ 0 \\ -1\end{bmatrix},\,t\in (-\infty ,\infty )
$$

Solution: Using the usual formula, we get

$$
\frac{x-2}{5}=\frac{y-7}{0}=\frac{z-1}{-1}=t,\,t\in (-\infty ,\infty ),
$$

or equivalently

$$
\frac{x-2}{5}=\frac{y-7}{0}=1-z,
$$

which is problematic because $\frac{y-7}{0}$ involves division by zero.

However, notice that in our line, the $y$ component always maintains the constant value of $y=7:$

$$
r=\begin{bmatrix}2+5t \\ 7 \\ 1-t\end{bmatrix},\,t\in (-\infty ,\infty )
$$

So, in the Cartesian equation, we remove the $\frac{y-7}{0}$ part and instead write $y=7$, as follows:

$$
\frac{x-2}{5}=1-z,\,y=7
$$

Answer selection: \frac{x-2}{5}=1-z,\,y=7

Question 17592186262771 — question.difficulty/moderate

Find the Cartesian equation for the line with the following vector equation:

$$
r=\begin{bmatrix}-3 \\ 2 \\ 1\end{bmatrix}+t\begin{bmatrix}3 \\ 0 \\ -2\end{bmatrix},\,t\in (-\infty ,\infty )
$$

Solution: Using the usual formula, we get

$$
\frac{x-(-3)}{3}=\frac{y-2}{0}=\frac{z-1}{-2}=t,\,t\in (-\infty ,\infty ),
$$

or equivalently

$$
\frac{x+3}{3}=\frac{y-2}{0}=\frac{z-1}{-2},
$$

which is problematic because $\frac{y-2}{0}$ involves division by zero.

However, notice that in our line, the $y$ component always maintains the constant value of $y=2:$

$$
r=\begin{bmatrix}-3+3t \\ 2 \\ 1-2t\end{bmatrix},\,t\in (-\infty ,\infty )
$$

So, in the Cartesian equation, we remove the $\frac{y-2}{0}$ part and instead write $y=2,$ as follows:

$$
\frac{x+3}{3}=\frac{z-1}{-2},\,y=2
$$

Answer selection: \frac{x+3}{3}=\frac{z-1}{-2},\,y=2

### Finding the Cartesian Equation of a Line Given Two Points on the Line (15 captured questions)

Question 17592186120243 — question.difficulty/moderate

![](images/1f/1f9599192c1979f40fc519458019ed3296d9a5ef9048aaed41aab973c62e0be8.png)

Find a Cartesian equation of the line shown in the figure above.

Solution: We know that the line passes through the points $P(-2,3,1)$ and $Q(5,-1,4).$ Now, we need to find a vector parallel to the given line. Let's consider the vector $\overset{\to }{PQ}$ which is given by

$$
\begin{aligned}\overset{\to }{PQ} & =⟨5,-1,4⟩-⟨-2,3,1⟩ \\  & =⟨7,-4,3⟩.\end{aligned}
$$

Using the point $P$ and the vector $\overset{\to }{PQ}$, we have that the Cartesian (canonical) equation of the given line is given by

$$
\frac{x-(-2)}{7}=\frac{y-3}{-4}=\frac{z-1}{3}=t,\,t\in (-\infty ,\infty ),
$$

or equivalently

$$
\frac{x+2}{7}=\frac{y-3}{-4}=\frac{z-1}{3}.
$$

Answer selection: \frac{x+2}{7}=\frac{y-3}{-4}=\frac{z-1}{3}

Question 17592186120246 — None

![](images/c9/c98485de8f94d4f00c0a1dd6eae30db51ee65cd8997d6dcb13aa590abafb816a.png)

Find a Cartesian equation of the line shown in the figure above.

Solution: 

Question 17592186262776 — question.difficulty/moderate

![](images/16/1647eb5cca32c6fdc99e23507db151a8299b29bfa70ebfbaa941e17fe4638586.png)

Find a Cartesian equation of the line shown in the figure above.

Solution: We know that the line passes through the points $P(-1,4,5)$ and $Q(7,-1,2).$ Now, we need to find a vector parallel to the given line. Let's consider the vector $\overset{\to }{PQ}$ which is given by

$$
\begin{aligned}\overset{\to }{PQ} & =⟨7,-1,2⟩-⟨-1,4,5⟩ \\  & =⟨8,-5,-3⟩.\end{aligned}
$$

Using the point $P$ and the vector $\overset{\to }{PQ}$, we have that the Cartesian (canonical) equation of the given line is given by

$$
\frac{x-(-1)}{8}=\frac{y-4}{-5}=\frac{z-5}{-3}=t,\,t\in (-\infty ,\infty ),
$$

or equivalently

$$
\frac{x+1}{8}=\frac{y-4}{-5}=\frac{z-5}{-3}.
$$

Answer selection: \frac{x+1}{8}=\frac{y-4}{-5}=\frac{z-5}{-3}
