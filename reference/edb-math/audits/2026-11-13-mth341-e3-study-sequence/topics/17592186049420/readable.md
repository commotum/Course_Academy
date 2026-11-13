# 17592186049420 Linear Transformations of Objects in the Plane

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186088929 — Introduction

Consider a line segment $\overline{AB}$ whose endpoints are located at $A(1,1)$ and $B(2,-1).$ Let's denote $\mathbf{a}$ and $\mathbf{b}$ as the position vectors of the points $A$ and $B$ respectively, as shown below.

![](images/a4/a41c830f1372e8e2763b36770fa5263557af2b36cc1e5780b9da0be1d24c171b.png)

In the plane, we know that a non-singular linear transformation maps a straight line onto a straight line. Similarly, a linear transformation maps a line segment onto another line segment.

Suppose that $\overline{A'B'}$ is the image of $\overline{AB}$ under the action of the linear transformation $\mathbf{T}$ represented by the matrix

$$
T = 
	\begin{bmatrix}2 & 1 \\ 1 & -2\end{bmatrix}.
$$

How do we compute $\overline{A'B'}?$

To find the coordinates of $A'$ and $B'$ simultaneously, we first create a matrix $X$ containing the coordinates of both ends  $A({\color{red}1},{\color{red}1})$ and $B({\color{blue}2},{\color{blue}-1})\mathbin{:}$

$$
X = 
\begin{bmatrix}{\color{red}{1}} & {\color{blue}{2}} \\ {\color{red}{1}} & {\color{blue}{-1}}\end{bmatrix}
$$

Next, we compute the product $TX\mathbin{:}$

$$
TX = 
	\begin{bmatrix}2 & 1 \\ 1 & -2\end{bmatrix}
\begin{bmatrix}{\color{red}{1}} & {\color{blue}{2}} \\ {\color{red}{1}} & {\color{blue}{-1}}\end{bmatrix}
	=
	\begin{bmatrix}{\color{red}{3}} & {\color{blue}{3}} \\ {\color{red}{-1}} & {\color{blue}{4}}\end{bmatrix}
$$

Therefore, $A'({\color{red}3},{\color{red}-1})$ and $B'({\color{blue}3},{\color{blue}4})$. Our result is shown below.

![](images/07/071e41286987da93608fa602fcccd3a63fc861985e6ff96e338b51b92c8c2e6a.png)



### example 17592186087608 — Computing the Image of a Line Segment Under the Action of a Linear Transformation

Consider the linear transformation $\mathbf T$ with matrix representation $T,$ given by

$$
T = {\left[ \begin{array}{cc}2 & 3 \\ 1 & - 1\end{array} \right]}.
$$

The line segment $\overline{AB}$ is shown below. Find $\overline{A'B'},$ the image of $\overline{AB}$ under the action of $\mathbf T.$

![](images/2e/2e22400d15abc81150d6d18de591549e81a46bd16ab9e95f10f86bae2125b490.png)

To find the image of $\overline{AB}$ under the action of $\mathbf T$, we first create a matrix $X$ containing the coordinates of the endpoints of $\overline{AB}\mathbin{:}$

$$
X = 
{\left[ \begin{array}{cc}2 & - 1 \\ - 1 & 1\end{array} \right]}
$$

Now, we compute the image of $X$ under the action of $\mathbf T$ by calculating the matrix product $TX\mathbin{:}$

$$
\begin{aligned}TX & =\begin{bmatrix}2 & 3 \\ 1 & -1\end{bmatrix}\begin{bmatrix}2 & -1 \\ -1 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 1 \\ 3 & -2\end{bmatrix}\end{aligned}
$$

Therefore, the coordinates of the respective endpoints of the image are $A'(1,3)$ and $B'(1,-2),$ as shown below.

![](images/47/472f8e712f7d695d5ab3593dafbcc0309feb1a6ac80e9e29c4893dc651d20cf7.png)

### example 17592186087566 — Computing the Image of a Polygon Under the Action of a Linear Transformation

Consider the linear transformation $\mathbf T$ with matrix representation $T,$ given by
$$
T = {\left[ \begin{array}{cc}1 & - 1 \\ 0 & - 2\end{array} \right]}.
$$

The triangle $\triangle ABC$ is shown below. Find $\triangle A'B'C',$ the image of $\triangle ABC$ under the action of $\mathbf T.$

![](images/49/4986bd2dab6b455c0d5e41909377c433d761bf7270364d3e2596e6db7f23981b.png)

To find the image of $T$ under the action of $\mathbf T,$ we first create a matrix $X$ containing all of the vertices of $\triangle ABC\mathbin{:}$
$$
X = 
	{\left[ \begin{array}{ccc}- 1 & 0 & 2 \\ 2 & 0 & 1\end{array} \right]}
$$

Now, we compute the image of $X$ under the action of $\mathbf T$ by calculating the matrix product $TX\mathbin{:}$

$$
\begin{aligned}TX & =\begin{bmatrix}1 & -1 \\ 0 & -2\end{bmatrix}\begin{bmatrix}-1 & 0 & 2 \\ 2 & 0 & 1\end{bmatrix} \\  & =\begin{bmatrix}-3 & 0 & 1 \\ -4 & 0 & -2\end{bmatrix}.\end{aligned}
$$

Therefore, the coordinates of the respective vertices of $\triangle A'B'C'$ are $(-3,-4), (0,0), (1,-2),$ as shown below.

![](images/e8/e8a14ffbaab4597a2a4a7c9a6bad61dabbc4970fc22c3ed2eb28b2594a670938.png)

## Representative practice (first three per skill; full bank in practice.json)

### Computing the Image of a Line Segment Under the Action of a Linear Transformation (16 captured questions)

Question 17592186087994 — None

Consider the linear transformation $T$ with matrix representation $T$, given by

$$
\displaystyle T = \begin{bmatrix}3 & 1 \\ 0 & 2\end{bmatrix}.
$$

A line segment $\overline{AB}$ has endpoints at $A(-1,-2)$ and $B(1, 3)$. What are the coordinates of the corresponding endpoints of $\overline{A^{\prime}B^{\prime}}$, the image of $\overline{AB}$ under the action of $T$?

Solution: 

Question 17592186087997 — None

![](images/f0/f07ad116d33d08e93b157f70bffc6036765e1b983ca1edbe23eea3316e1863a3.png)

Consider the linear transformation $T$ with matrix representation $T$, given by

$$
\displaystyle T = \begin{bmatrix}1 & 1 \\ 2 & 1\end{bmatrix}.
$$

The line segment $\overline{AB}$ is shown above. Which of the following is $\overline{A^{\prime}B^{\prime}}$, the image of $\overline{AB}$ under the action of $T$?

Solution: 

Question 17592186292882 — question.difficulty/easy

Consider the linear transformation $T$ with matrix representation $T,$ given by

$$
T=\begin{bmatrix}2 & 0 \\ 1 & 1\end{bmatrix}.
$$

A line segment $\overset{―}{AB}$ has endpoints at $A(1,2)$ and $B(-1,0).$ What are the coordinates of the corresponding endpoints of $\overset{―}{{A}^{′}{B}^{′}}$, the image of $\overset{―}{AB}$ under the action of $T?$

${A}^{′}($ 
{{field-1}}, 
{{field-2}}
$)\,$ and $\,{B}^{′}($ 
{{field-3}}, 
{{field-4}}
$)$

Solution: To find the image of $\overset{―}{AB}$ under the action of $T$, we first create a matrix $X$ containing the coordinates of the endpoints of $\overset{―}{AB}:$

$$
X=\begin{bmatrix}1 & -1 \\ 2 & 0\end{bmatrix}.
$$

Now, we compute the image of $X$ under the action of $T$ by calculating the matrix product $TX:$

$$
\begin{aligned}TX & =\begin{bmatrix}2 & 0 \\ 1 & 1\end{bmatrix}\begin{bmatrix}1 & -1 \\ 2 & 0\end{bmatrix} \\  & =\begin{bmatrix}2 & -2 \\ 3 & -1\end{bmatrix}.\end{aligned}
$$

Therefore, the coordinates of the respective endpoints of the image are ${A}^{′}(2,3)$ and ${B}^{′}(-2,-1).$

Answer field-1: 2

Answer field-2: 3

Answer field-3: -2

Answer field-4: -1

### Computing the Image of a Polygon Under the Action of a Linear Transformation (16 captured questions)

Question 17592186087996 — question.difficulty/moderate

![](images/20/205badcabf4c2444f7ca8b38e189b1a0f8957e324ba7fb1a28909dc4afdd8c75.png)

Consider the linear transformation $T$ with matrix representation $T,$ given by

$$
T=\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}.
$$

The triangle $△ABC$ is shown above. Which of the following is $△{A}^{′}{B}^{′}{C}^{′},$ the image of $△ABC$ under the action of $T?$

Solution: To find the image of $T$ under the action of $T$, we first create a matrix $X$ containing all of the vertices of $△ABC:$

$$
X=\begin{bmatrix}-3 & 1 & 3 \\ -2 & 2 & -2\end{bmatrix}
$$

Now, we compute the image of $X$ under the action of $T$ by calculating the matrix product $TX:$

$$
\begin{aligned}TX & =\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}\begin{bmatrix}-3 & 1 & 3 \\ -2 & 2 & -2\end{bmatrix} \\  & =\begin{bmatrix}2 & -2 & 2 \\ -3 & 1 & 3\end{bmatrix}.\end{aligned}
$$

 

Therefore, the coordinates of the respective vertices of $△{A}^{′}{B}^{′}{C}^{′}$ are $(2,-3),(-2,1),(2,3)$, as shown below.

![](images/4e/4e456209fc818f606bfe83324b05843b0122840161a84a8d729927f4050f2397.png)

Answer selection: images/4e/4e456209fc818f606bfe83324b05843b0122840161a84a8d729927f4050f2397.png

Question 17592186088388 — question.difficulty/easy

Consider the linear transformation $T$ with matrix representation $T,$ given by

$$
T=\begin{bmatrix}1 & 5 \\ 0 & -1\end{bmatrix}.
$$

A triangle $S$ has vertices at $(-1,1),(2,3),$ and $(5,1).$ Which of the following are coordinates of a vertex of ${S}^{′}$, the image of $S$ under the action of $T?$

Select all that apply.

Solution: To find the image of $S$ under the action of $T$, we first create a matrix $X$ containing all of the vertices of $S:$

$$
X=\begin{bmatrix}-1 & 2 & 5 \\ 1 & 3 & 1\end{bmatrix}
$$

Now, we compute the image of $X$ under $T$ by calculating the matrix product $TX:$

$$
\begin{aligned}TX & =\begin{bmatrix}1 & 5 \\ 0 & -1\end{bmatrix}\begin{bmatrix}-1 & 2 & 5 \\ 1 & 3 & 1\end{bmatrix} \\  & =\begin{bmatrix}4 & 17 & 10 \\ -1 & -3 & -1\end{bmatrix}.\end{aligned}
$$

Therefore, the coordinates of the respective vertices of ${S}^{′}$ are $(4,-1),(17,-3),(10,-1).$ 

So, the correct answer is “The point $(4,-1)$”; “The point $(17,-3)$”; “The point $(10,-1)$”.

Answer The point $(10,-1)$: true

Answer The point $(17,-3)$: true

Answer The point $(4,-1)$: true

Question 17592186235393 — question.difficulty/hard

![](images/c1/c1d9f53c6aed4acd378f8554df5c8beaaea81e169b5284e51f87204a87b3d53d.png)

A housing complex designed by an architect is shown in the coordinate plane as the region $R$ with vertices $ABCD.$ A highway lies on the line $l$ with equation $2x+y+1=0.$ The area of the complex is $16$ hectares.

The architect is expanding the plan of the housing complex. The transformation $T$ from part 1 maps the current plan of the housing complex $ABCD$ to the new plan ${A}^{′}{B}^{′}{C}^{′}{D}^{′}.$ Find the vertices of the new housing complex.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
${A}^{′}(-9,$

                                    
                                
                                    
                            
{{field-1}}                
                                    
                                
                                    
                                        
                                        
$)$
$\,$
${B}^{′}($

                                    
                                
                                    
                            
{{field-2}}                
                                    
                                
                                    
                                        
                                        
$,14)$

                                    
                                
                                    
                                        
                                                

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
${C}^{′}(-21,$

                                    
                                
                                    
                            
{{field-3}}                
                                    
                                
                                    
                                        
                                        
$)$
$\,$
${D}^{′}($

                                    
                                
                                    
                            
{{field-4}}                
                                    
                                
                                    
                                        
                                        
$,0)$

Solution: In part 1, we found that the matrix representation of $T$ is

$$
T=\begin{bmatrix}-3 & 0 \\ 2 & -1\end{bmatrix}.
$$

To find the image of the field under the action of $T,$ we first create a matrix $X$ containing all of the vertices of $ABCD:$

$$
X=\begin{bmatrix}3 & 7 & 7 & 3 \\ 2 & 0 & 4 & 6\end{bmatrix}
$$

Now, we compute the image of $X$ under the action of $T$ by calculating the matrix product $TX:$

$$
\begin{aligned}TX & =\begin{bmatrix}-3 & 0 \\ 2 & -1\end{bmatrix}\begin{bmatrix}3 & 7 & 7 & 3 \\ 2 & 0 & 4 & 6\end{bmatrix} \\  & =\begin{bmatrix}-9 & -21 & -21 & -9 \\ 4 & 14 & 10 & 0\end{bmatrix}.\end{aligned}
$$

Therefore, the coordinates of the respective vertices ${A}^{′}{B}^{′}{C}^{′}{D}^{′}$ are $(-9,4),$ $(-21,14),$ $(-21,10),$ and $(-9,0),$ as shown below.

![](images/74/7430fd0c1e3a4c94e951eb1cf133e5c155f7a7b605a46b4b2272bf30fbb688e2.png)

Answer field-1: 4

Answer field-2: -21

Answer field-3: 10

Answer field-4: -9
