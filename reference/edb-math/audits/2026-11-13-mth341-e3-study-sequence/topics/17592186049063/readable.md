# 17592186049063 Linear Transformations of Points and Lines in the Plane

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186153365 — Introduction

Consider the linear transformation $\mathbf T$ with matrix representation $T,$ given by

<div class="matrix-operands matrix-operands-stacked">
<div>$T =\begin{bmatrix}-2 & 1 \\ 0 & -2\end{bmatrix}$</div>
</div>

Given a point $A(1,1),$ let $A'$ be the image of $A$ under the action of $\mathbf T.$ How can we find the coordinates of $A'?$

First, we create a column vector $\mathbf{x}$ containing the coordinates of $A{:}$

$$
\mathbf{x} = 
\begin{bmatrix}1 \\ 1\end{bmatrix}
$$

Now, we compute the image of $\mathbf{x}$ under the action of $\mathbf T$ by calculating the matrix product $T\mathbf{x}\mathbin{:}$

$$
\begin{aligned}Tx & =\begin{bmatrix}-2 & 1 \\ 0 & -2\end{bmatrix}\begin{bmatrix}1 \\ 1\end{bmatrix} \\  & =\begin{bmatrix}-1 \\ -2\end{bmatrix}\end{aligned}
$$

The result, $T \mathbf{x},$ contains the coordinates of $A'.$ Therefore, $A'(-1,-2).$



### example 17592186151974 — Computing the Image of a Point Under a Linear Transformation of a Plane

Consider the linear transformation $\mathbf T$ with matrix representation $T,$ given by

$$
T = {\left[ \begin{array}{cc}3 & 1 \\ - 4 & - 1\end{array} \right]}.
$$

What are the coordinates of the point $B',$ the image of $B(2,-3)$ under the action of $\mathbf T?$

To find the image of $B$ under the action of $\mathbf T,$ we first create a column vector $\mathbf{x}$ containing the coordinates of $B{:}$

$$
\mathbf{x} = 
{\left[ \begin{array}{c}2 \\ - 3\end{array} \right]}.
$$

Now, we compute the image of $\mathbf{x}$ under the action of $\mathbf T$ by calculating the matrix product $T\mathbf{x}\mathbin{:}$

$$
\begin{aligned}Tx & =\begin{bmatrix}3 & 1 \\ -4 & -1\end{bmatrix}\begin{bmatrix}2 \\ -3\end{bmatrix} \\  & =\begin{bmatrix}3 \\ -5\end{bmatrix}.\end{aligned}
$$

The result, $T \mathbf{x},$ contains the coordinates of $B'.$ Therefore, $B'(3,-5).$

### tutorial 17592186153373 — The Image of a Line Under the Action of a Linear Transformation

Linear transformations of a plane have the following important property: 

*A non-singular linear transformation in the plane maps a straight line into a straight line.* 

Therefore, to find the image of a line $l$ under the action of a linear transformation $\mathbf{T}$ (represented by its standard matrix $T$), we do the following:

1\. Find two distinct points $A$ and $B$ that lie on the line $l.$

2\. Compute the images $A'$ and $B'$ of the points $A$ and $B$ under the action of $\mathbf{T}.$

3\. Write down the equation of the line that passes through $A'$ and $B'.$



### example 17592186151976 — Computing the Image of a Line Given by an Equation in Slope-Intercept Form

Consider the line $y=3x-2$ and linear transformation $\mathbf T$ with matrix representation $T,$ given by

$$
T = {\left[ \begin{array}{cc}- 1 & 0 \\ 3 & 1\end{array} \right]}.
$$

What is the equation of the image of the line under the action of $\mathbf T?$

First, let's find two points on the given line. Substituting $x=0$ and $x=1,$ we get

$$
\begin{aligned}x=0\, & \to \,y=3(0)-2=-2, \\ x=1\, & \to \,y=3(1)-2=1.\end{aligned}
$$

So we have two points on the line, $P(0,-2)$ and $Q(1,1).$

To find the images of $P$ and $Q$ under the action of $\mathbf T,$ we first create a matrix $X$ containing the coordinates of $P$ and $Q$ in its columns:

$$
X = 
{\left[ \begin{array}{cc}0 & 1 \\ - 2 & 1\end{array} \right]}
$$

Now, we compute the image of $X$ under the action of $\mathbf T$ by calculating the matrix product $TX\mathbin{:}$

$$
\begin{aligned}TX & =\begin{bmatrix}-1 & 0 \\ 3 & 1\end{bmatrix}\begin{bmatrix}0 & 1 \\ -2 & 1\end{bmatrix} \\  & =\begin{bmatrix}0 & -1 \\ -2 & 4\end{bmatrix}\end{aligned}
$$

Therefore, the coordinates of the respective image points are $P'(0,-2)$ and $Q'(-1,4).$

Finally, we write the equation of the line that passes through $P'$ and $Q'\mathbin{:}$

$$
\begin{aligned}y-{y}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}}(x-{x}_{1}) \\ y-(-2) & =\frac{4-(-2)}{-1-0}(x-0) \\ y+2 & =-6x \\ 6x+y+2 & =0\end{aligned}
$$

### example 17592186151975 — Computing the Image of a Line Given by an Equation in Standard Form

Consider the line $5x-y-3=0$ and linear transformation $\mathbf T$ with matrix representation $T,$ given by

$$
T = {\left[ \begin{array}{cc}- 3 & 1 \\ - 1 & 2\end{array} \right]}.
$$

What is the equation of the image of the line under the action of $\mathbf T?$

First, let's find two points on the given line. Solving for $y,$ we get $y=5x-3,$ and substituting $x=0$ and $x=1,$ we get

$$
\begin{aligned}x=0\, & \to \,y=5(0)-3=-3, \\ x=1\, & \to \,y=5(1)-3=2.\end{aligned}
$$

So we have two points on the line, $P(0,-3)$ and $Q(1,2).$

To find the images of $P$ and $Q$ under the action of $\mathbf T,$ we first create a matrix $X$ containing the coordinates of $P$ and $Q$ in its columns:

$$
X = 
{\left[ \begin{array}{cc}0 & 1 \\ - 3 & 2\end{array} \right]}
$$

Now, we compute the image of $X$ under the action of $\mathbf T$ by calculating the matrix product $TX\mathbin{:}$

$$
\begin{aligned}TX & =\begin{bmatrix}-3 & 1 \\ -1 & 2\end{bmatrix}\begin{bmatrix}0 & 1 \\ -3 & 2\end{bmatrix} \\  & =\begin{bmatrix}-3 & -1 \\ -6 & 3\end{bmatrix}\end{aligned}
$$

Therefore, the coordinates of the respective image points are $P'(-3,-6)$ and $Q'(-1,3).$

Finally, we write the equation of the line that passes through $P'$ and $Q'\mathbin{:}$

$$
\begin{aligned}y-{y}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}}(x-{x}_{1}) \\ y-(-6) & =\frac{3-(-6)}{-1-(-3)}(x-(-3)) \\ y+6 & =\frac{9}{2}(x+3) \\ 2y+12 & =9x+27 \\ 9x-2y+15 & =0\end{aligned}
$$

### tutorial 17592186153366 — The Proof That a Linear Transformation Maps a Straight Line Onto a Straight Line

Consider a non-singular linear transformation $\mathbf{T}$ and a line that is given by the vector equation 

$$
\mathbf{r} = \mathbf{p}+\mathbf{d}t, \qquad
	t \in (-\infty,\infty).
$$

Note that, for the above equation to represent a line (and not just a point), we must have $\mathbf{d} \neq \mathbf{0}.$

Now, using the linearity of the transformation, we obtain

$$
\begin{aligned}T(r) & =T(p+dt) \\  & =T(p)+T(td) \\  & =T(p)+tT(d) \\  & ={p}^{′}+t{d}^{′},\end{aligned}
$$

where $\mathbf{T}(\mathbf{p})=\mathbf{p}'$ and $\mathbf{T}(\mathbf{d})=\mathbf{d}'.$

Because $\mathbf{T}$ is non-singular and $\mathbf{d} \neq \mathbf{0},$ we know that $\mathbf{T}(\mathbf{d}) \neq \mathbf{0},$ which means $\mathbf{d}' \neq \mathbf{0}.$

Therefore, the equation $\mathbf{p}'+t\mathbf{d}'$ represents a straight line, and we can make the following conclusion:

*A non-singular linear transformation maps a straight line onto a straight line.*



## Representative practice (first three per skill; full bank in practice.json)

### Computing the Image of a Point Under a Linear Transformation of a Plane (10 captured questions)

Question 17592186152771 — question.difficulty/easy

Consider the linear transformation $T$ with matrix representation $T,$ given by

$$
T=\begin{bmatrix}-2 & 0 \\ 1 & 2\end{bmatrix}.
$$

What are the coordinates of the point ${A}^{′}$, the image of $A(-1,1)$ under the action of $T?$

Solution: To find the image of $A$ under the action of $T$, we first create a column-vector $x$ containing the coordinates of $A:$

$$
x=\begin{bmatrix}-1 \\ 1\end{bmatrix}.
$$

Now, we compute the image of $x$ under the action of $T$ by calculating the matrix product $Tx:$

$$
\begin{aligned}Tx & =\begin{bmatrix}-2 & 0 \\ 1 & 2\end{bmatrix}\begin{bmatrix}-1 \\ 1\end{bmatrix} \\  & =\begin{bmatrix}2 \\ 1\end{bmatrix}.\end{aligned}
$$

The result, $Tx,$ contains the coordinates of ${A}^{′}.$ Therefore, ${A}^{′}(2,1).$

Answer selection: (2,1)

Question 17592186152775 — question.difficulty/easy

Consider the linear transformation $T$ with matrix representation $T,$ given by

$$
T=\begin{bmatrix}-3 & \sqrt{3} \\ 1 & \sqrt{3}\end{bmatrix}.
$$

What are the coordinates of the point ${S}^{′}$, the image of $S(-4,\sqrt{3})$ under the action of $T?$

Solution: To find the image of $S$ under the action of $T$, we first create a column-vector $x$ containing the coordinates of $S:$

$$
x=\begin{bmatrix}-4 \\ \sqrt{3}\end{bmatrix}.
$$

Now, we compute the image of $x$ under the action of $T$ by calculating the matrix product $Tx:$

$$
\begin{aligned}Tx & =\begin{bmatrix}-3 & \sqrt{3} \\ 1 & \sqrt{3}\end{bmatrix}\begin{bmatrix}-4 \\ \sqrt{3}\end{bmatrix} \\  & =\begin{bmatrix}15 \\ -1\end{bmatrix}.\end{aligned}
$$

The result, $Tx,$ contains the coordinates of ${S}^{′}.$ Therefore, ${S}^{′}(15,-1).$

Answer selection: (15,-1)

Question 17592186292879 — question.difficulty/easy

Consider the linear transformation $T$ with matrix representation $T,$ given by

$$
T=\begin{bmatrix}7 & 0 \\ 2 & -4\end{bmatrix}.
$$

What are the coordinates of the point ${C}^{′}$, the image of $C(0,3)$ under the action of $T?$

${C}^{′}($ 
{{field-1}},
{{field-2}}$)$

Solution: To find the image of $C$ under the action of $T$, we first create a column-vector $x$ containing the coordinates of $C:$

$$
x=\begin{bmatrix}0 \\ 3\end{bmatrix}.
$$

Now, we compute the image of $x$ under the action of $T$ by calculating the matrix product $Tx:$

$$
\begin{aligned}Tx & =\begin{bmatrix}7 & 0 \\ 2 & -4\end{bmatrix}\begin{bmatrix}0 \\ 3\end{bmatrix} \\  & =\begin{bmatrix}0 \\ -12\end{bmatrix}.\end{aligned}
$$

The result, $Tx,$ contains the coordinates of ${C}^{′}.$ Therefore, ${C}^{′}(0,-12).$

Answer field-1: 0

Answer field-2: -12

### Computing the Image of a Line Given by an Equation in Slope-Intercept Form (17 captured questions)

Question 17592186152773 — question.difficulty/moderate

Consider the line $y=2x-5$ and linear transformation $T$ with matrix representation $T,$ given by

$$
T=\begin{bmatrix}1 & -1 \\ 2 & 0\end{bmatrix}.
$$

What is the equation of the image of the line under the action of $T?$

Solution: First, notice that the line $y=2x-5$ passes through the points $A(0,-5)$ and $B(1,-3)$ since the coordinates of both points satisfy the equation.

To find the image of $A$ and $B$ under the action of $T$, we first create a matrix $X$ containing the coordinates of the points:

$$
X=\begin{bmatrix}0 & 1 \\ -5 & -3\end{bmatrix}.
$$

Now, we compute the image of $X$ under the action of $T$ by calculating the matrix product $TX:$

$$
\begin{aligned}TX & =\begin{bmatrix}1 & -1 \\ 2 & 0\end{bmatrix}\begin{bmatrix}0 & 1 \\ -5 & -3\end{bmatrix} \\  & =\begin{bmatrix}5 & 4 \\ 0 & 2\end{bmatrix}.\end{aligned}
$$

Therefore, the coordinates of the respective image points are ${A}^{′}(5,0)$ and ${B}^{′}(4,2).$

Finally, we write the equation of the line that passes through ${A}^{′}$ and ${B}^{′}:$

$$
\begin{aligned}y-{y}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}}(x-{x}_{1}) \\ y-0 & =\frac{2-0}{4-5}(x-5) \\ y & =-2(x-5) \\ y & =-2x+10 \\ 2x+y-10 & =0\end{aligned}
$$

Answer selection: 2x+y-10=0

Question 17592186152776 — None

Consider the line $y = 2x + 3$ and linear transformation $T$ with matrix representation $T$, given by

$$
\displaystyle T = \begin{bmatrix}-2 & -1 \\ 1 & -3\end{bmatrix}.
$$

What is the equation of the image of the line under the action of $T$?

Solution: 

Question 17592186295032 — question.difficulty/moderate

Consider the line $y=3x+5$ and linear transformation $T$ with matrix representation $T,$ given by

$$
T=\begin{bmatrix}0 & -2 \\ 4 & 1\end{bmatrix}.
$$

In **standard form**, the equation of the image of the line under the action of $T$ is

{{field-1}}$=-40.$

Solution: First, notice that the line $y=3x+5$ passes through the points $A(0,5)$ and $B(1,8)$ since the coordinates of both points satisfy the equation.

To find the image of $A$ and $B$ under the action of $T$, we first create a matrix $X$ containing the coordinates of the points:

$$
X=\begin{bmatrix}0 & -2 \\ 4 & 1\end{bmatrix}.
$$

Now, we compute the image of $X$ under the action of $T$ by calculating the matrix product $TX:$

$$
\begin{aligned}TX & =\begin{bmatrix}0 & -2 \\ 4 & 1\end{bmatrix}\begin{bmatrix}0 & 1 \\ 5 & 8\end{bmatrix} \\  & =\begin{bmatrix}-10 & -16 \\ 5 & 12\end{bmatrix}.\end{aligned}
$$

Therefore, the coordinates of the respective image points are ${A}^{′}(-10,5)$ and ${B}^{′}(-16,12).$

Now, we write the equation of the line that passes through ${A}^{′}$ and ${B}^{′}$ in point-slope form:

$$
\begin{aligned}y-{y}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}}(x-{x}_{1}) \\ y-5 & =\frac{12-5}{-16-(-10)}(x-(-10)) \\ y-5 & =-\frac{7}{6}(x+10)\end{aligned}
$$

Finally, we transform the equation of the line to standard form:

$$
\begin{aligned}y-5 & =-\frac{7}{6}(x+10) \\ 6y-30 & =-7x-70 \\ 7x+6y & =-40\end{aligned}
$$

Answer field-1: 7x+6y

### Computing the Image of a Line Given by an Equation in Standard Form (16 captured questions)

Question 17592186152772 — question.difficulty/hard

Consider the line $2x+y-3=0$ and linear transformation $T$ with matrix representation $T,$ given by

$$
T=\begin{bmatrix}-2 & 0 \\ 1 & 2\end{bmatrix}.
$$

What is the equation of the image of the line under the action of $T?$

Solution: First, notice that the line $2x+y-3=0$ passes through the points $A(0,3)$ and $B(1,1)$ since the coordinates of both points satisfy the equation.

To find the image of $A$ and $B$ under the action of $T$, we first create a matrix $X$ containing the coordinates of the points:

$$
X=\begin{bmatrix}0 & 1 \\ 3 & 1\end{bmatrix}.
$$

Now, we compute the image of $X$ under the action of $T$ by calculating the matrix product $TX:$

$$
\begin{aligned}TX & =\begin{bmatrix}-2 & 0 \\ 1 & 2\end{bmatrix}\begin{bmatrix}0 & 1 \\ 3 & 1\end{bmatrix} \\  & =\begin{bmatrix}0 & -2 \\ 6 & 3\end{bmatrix}.\end{aligned}
$$

Therefore, the coordinates of the respective image points are ${A}^{′}(0,6)$ and ${B}^{′}(-2,3).$

Finally, we write the equation of the line that passes through ${A}^{′}$ and ${B}^{′}:$

$$
\begin{aligned}y-{y}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}}(x-{x}_{1}) \\ y-6 & =\frac{3-6}{-2-0}(x-0) \\ y-6 & =\frac{3}{2}x \\ 2y-12 & =3x \\ 3x-2y+12 & =0\end{aligned}
$$

Answer selection: 3x-2y+12=0

Question 17592186152774 — question.difficulty/moderate

Consider the line $x=5$ and linear transformation $T$ with matrix representation $T,$ given by

$$
T=\begin{bmatrix}-1 & 1 \\ 0 & 1\end{bmatrix}.
$$

What is the equation of the image of the line under the action of $T?$

Solution: First, notice that the line $x=5$ passes through the points $A(5,0)$ and $B(5,1)$ since the coordinates of both points satisfy the equation.

To find the image of $A$ and $B$ under the action of $T$, we first create a matrix $X$ containing the coordinates of the points:

$$
X=\begin{bmatrix}5 & 5 \\ 0 & 1\end{bmatrix}.
$$

Now, we compute the image of $X$ under the action of $T$ by calculating the matrix product $TX:$

$$
\begin{aligned}TX & =\begin{bmatrix}-1 & 1 \\ 0 & 1\end{bmatrix}\begin{bmatrix}5 & 5 \\ 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}-5 & -4 \\ 0 & 1\end{bmatrix}.\end{aligned}
$$

Therefore, the coordinates of the respective image points are ${A}^{′}(-5,0)$ and ${B}^{′}(-4,1).$

Finally, we write the equation of the line that passes through ${A}^{′}$ and ${B}^{′}:$

$$
\begin{aligned}y-{y}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}}(x-{x}_{1}) \\ y-0 & =\frac{1-0}{-4-(-5)}(x-(-5)) \\ y & =x+5 \\ x-y+5 & =0\end{aligned}
$$

Answer selection: x-y+5=0

Question 17592186235396 — question.difficulty/hard

![](images/c1/c1d9f53c6aed4acd378f8554df5c8beaaea81e169b5284e51f87204a87b3d53d.png)

A housing complex designed by an architect is shown in the coordinate plane as the region $R$ with vertices $ABCD.$ A highway lies on the line $l$ with equation $2x+y+1=0.$ The area of the complex is $16$ hectares.

The architect finds the image of the line $l$ under the action of $T$ and places another highway on the plan from this image. The equation of the line on which the new highway lies, in **standard form**, is

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$x\,+\,$

                                    
                                
                                    
                            
                                        {{field-2}}                
                                    
                                
                                    
                                        
                                        
$y\,=\,3.$

Solution: In part 1, we found that the matrix representation of $T$ is

$$
T=\begin{bmatrix}-3 & 0 \\ 2 & -1\end{bmatrix}.
$$

First, notice that the line $2x+y+1=0$ passes through the points $U(-1,1)$ and $V(0,-1)$ since the coordinates of both points satisfy the equation.

To find the image of $U$ and $V$ under the action of $T,$ we first create a matrix $X$ containing the coordinates of the points:

$$
X=\begin{bmatrix}-1 & 0 \\ 1 & -1\end{bmatrix}
$$

Now, we compute the image of $X$ under the action of $T$ by calculating the matrix product $TX:$

$$
\begin{aligned}TX & =\begin{bmatrix}-3 & 0 \\ 2 & -1\end{bmatrix}\begin{bmatrix}-1 & 0 \\ 1 & -1\end{bmatrix} \\  & =\begin{bmatrix}3 & 0 \\ -3 & 1\end{bmatrix}.\end{aligned}
$$

Therefore, the coordinates of the respective image points are ${U}^{′}(3,-3)$ and ${V}^{′}(0,1).$

Finally, we write the equation of the line that passes through ${U}^{′}$ and ${V}^{′}:$

$$
\begin{aligned}y-{y}_{1} & =\frac{{y}_{2}-{y}_{1}}{{x}_{2}-{x}_{1}}(x-{x}_{1}) \\ y-(-3) & =\frac{1-(-3)}{0-3}(x-3) \\ y+3 & =-\frac{4}{3}(x-3) \\ 3y+9 & =-4x+12 \\ 4x+3y+9 & =12 \\ 4x+3y & =3\end{aligned}
$$

Answer field-1: 4

Answer field-2: 3
