# 17592186049213 Inverting Linear Transformations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186093436 — Introduction

Consider the linear transformation $\mathbf{T}$ whose matrix $T$ is given by

<div class="matrix-operands matrix-operands-stacked">
<div>$T=\begin{bmatrix}2 & 4 \\ 4 & 10\end{bmatrix}$</div>
</div>

Suppose we know that some vector $\mathbf{v}$ in the plane is mapped to the vector $\mathbf w$ under the action of $\mathbf T,$ where the vector $\mathbf w$ is given by

$$
\mathbf{w} = \begin{bmatrix}2 \\ 6\end{bmatrix}.
$$

 

The mapping $\mathbf T(\mathbf v) = \mathbf w$ is shown schematically in the diagram below.

![](images/b5/b53ed555a52830fd0dcc0ba150c618fd8b527a0261c8e3caf09378c47dc6ffae.png)

How can we find the original vector $\mathbf v?$

To find the vector $\mathbf v,$ we compute the inverse of the matrix $T$ and then use it to reverse the action of $\mathbf T.$ Let's see how this works. 

From the given information, we have 

$$
T\cdot \mathbf{v} = \begin{bmatrix}2 \\ 6\end{bmatrix}.
$$

If we pre-multiply the above equation by $T^{-1},$ we get

$$
\begin{aligned}{T}^{-1}\cdot T\cdot v & ={T}^{-1}\cdot \begin{bmatrix}2 \\ 6\end{bmatrix} \\ {I}_{2}\cdot v & ={T}^{-1}\cdot \begin{bmatrix}2 \\ 6\end{bmatrix} \\ v & ={T}^{-1}\cdot \begin{bmatrix}2 \\ 6\end{bmatrix}.\end{aligned}
$$

This equation tells that to find the vector $\mathbf v,$ we need to pre-multiply the vector $\mathbf w$ by the inverse of $T.$

So, we now calculate the inverse of $T\mathbin{:}$

$$
\begin{aligned}{T}^{-1} & =\frac{1}{20-16}\begin{bmatrix}10 & -4 \\ -4 & 2\end{bmatrix} \\  & =\frac{1}{4}\begin{bmatrix}10 & -4 \\ -4 & 2\end{bmatrix}.\end{aligned}
$$

Therefore, we can calculate the original vector $\mathbf v$ as follows:

$$
\begin{aligned}v & ={T}^{-1}\cdot \begin{bmatrix}2 \\ 6\end{bmatrix} \\  & =\frac{1}{4}\begin{bmatrix}10 & -4 \\ -4 & 2\end{bmatrix}\begin{bmatrix}2 \\ 6\end{bmatrix} \\  & =\frac{1}{4}\begin{bmatrix}-4 \\ 4\end{bmatrix} \\  & =\begin{bmatrix}-1 \\ 1\end{bmatrix}\end{aligned}
$$

We can easily check that this is the correct answer by computing $T\cdot \mathbf v\mathbin{:}$

$$
\begin{aligned}T\cdot v & =\begin{bmatrix}2 & 4 \\ 4 & 10\end{bmatrix}\begin{bmatrix}-1 \\ 1\end{bmatrix} \\  & =\begin{bmatrix}2 \\ 6\end{bmatrix}\,✓\end{aligned}
$$

 

We summarize the process we just completed in the following diagram.

![](images/69/6991d3f7be5f29f51512ed927189ea10cbbcdb9dc6a2ce00573759201fb684a6.png)

In general, if $T$ is a $2\times 2$ matrix that represents a linear transformation, then $T^{-1}$ is the inverse linear transformation and, if it exists, it reverses the action of $T.$ So for any vector $\mathbf{v}$ on the plane, we have

$$
T^{-1}\cdot T\cdot \mathbf{v} = I_2 \cdot \mathbf{v} = \mathbf{v}.
$$



### example 17592186092070 — Calculating a Vector Given Its Image Under a Linear Transformation

The vector $\mathbf{v}$ in the plane is mapped to the vector $\begin{bmatrix}1 \\ 4\end{bmatrix}$ under the action of the linear transformation $\mathbf{T}$ whose matrix $T$ is given by
$$
T={\left[ \begin{array}{cc}5 & - 2 \\ 10 & - 3\end{array} \right]}.
$$
What is the original vector $\mathbf{v}?$

From the given information, we have

$$
T\cdot \mathbf{v} = {\left[ \begin{array}{c}1 \\ 4\end{array} \right]}.
$$

We need to reverse the action of the matrix $T.$ So, we multiply the above equation by $T^{-1},$ and we get

$$
\begin{aligned}{T}^{-1}\cdot T\cdot v & ={T}^{-1}\cdot \begin{bmatrix}1 \\ 4\end{bmatrix} \\ v & ={T}^{-1}\cdot \begin{bmatrix}1 \\ 4\end{bmatrix}.\end{aligned}
$$

Now, we need to calculate the inverse of $T$, which is

$$
\begin{aligned}{T}^{-1} & =\frac{1}{-15-(-20)}\begin{bmatrix}-3 & 2 \\ -10 & 5\end{bmatrix} \\  & =\frac{1}{5}\begin{bmatrix}-3 & 2 \\ -10 & 5\end{bmatrix}.\end{aligned}
$$

Therefore, the original vector is

$$
\begin{aligned}v & ={T}^{-1}\cdot \begin{bmatrix}1 \\ 4\end{bmatrix} \\  & =\frac{1}{5}\begin{bmatrix}-3 & 2 \\ -10 & 5\end{bmatrix}\begin{bmatrix}1 \\ 4\end{bmatrix} \\  & =\frac{1}{5}\begin{bmatrix}5 \\ 10\end{bmatrix} \\  & =\begin{bmatrix}1 \\ 2\end{bmatrix}.\end{aligned}
$$

### example 17592186092071 — Calculating the Vertices of a Polygon Given Its Image Under a Linear Transformation

Consider the linear transformation $\mathbf T$ with matrix representation $T,$ given by
$$
T = {\left[ \begin{array}{cc}4 & - 1 \\ 3 & 1\end{array} \right]}.
$$

The triangle $S$ is mapped to the triangle $S'$ under the action of $\mathbf T.$ The triangle $S'$ has vertices $(4,3),(4,10),$ and $(-4,-3).$ Which of the following are vertices of $S?$

- $(1,0)$

- $(4,-3)$

- $(-1,0)$

First, we create a matrix $Y$ containing all of the vertices of $S'\mathbin{:}$ 

$$
Y = 
{\left[ \begin{array}{ccc}4 & 4 & - 4 \\ 3 & 10 & - 3\end{array} \right]}
$$

Now, if $X$ denotes the matrix that contains the corresponding vertices of $S$, we have

$$
\begin{aligned}T\cdot X & =Y \\ T\cdot X & =\begin{bmatrix}4 & 4 & -4 \\ 3 & 10 & -3\end{bmatrix}.\end{aligned}
$$

We need to reverse the action of the matrix $T.$ So, we multiply the above equation by $T^{-1},$ and we get

$$
\begin{aligned}{T}^{-1}\cdot T\cdot X & ={T}^{-1}\cdot \begin{bmatrix}4 & 4 & -4 \\ 3 & 10 & -3\end{bmatrix} \\ X & ={T}^{-1}\cdot \begin{bmatrix}4 & 4 & -4 \\ 3 & 10 & -3\end{bmatrix}.\end{aligned}
$$

The inverse of $T$ is

$$
\begin{aligned}{T}^{-1} & =\frac{1}{4-(-3)}\begin{bmatrix}1 & 1 \\ -3 & 4\end{bmatrix} \\  & =\frac{1}{7}\begin{bmatrix}1 & 1 \\ -3 & 4\end{bmatrix}.\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}X & ={T}^{-1}\cdot \begin{bmatrix}4 & 4 & -4 \\ 3 & 10 & -3\end{bmatrix} \\  & =\frac{1}{7}\begin{bmatrix}1 & 1 \\ -3 & 4\end{bmatrix}\begin{bmatrix}4 & 4 & -4 \\ 3 & 10 & -3\end{bmatrix} \\  & =\frac{1}{7}\begin{bmatrix}7 & 14 & -7 \\ 0 & 28 & 0\end{bmatrix} \\  & =\begin{bmatrix}1 & 2 & -1 \\ 0 & 4 & 0\end{bmatrix}.\end{aligned}
$$

As a result, the coordinates of the vertices of the original triangle are $(1,0),(2,4),(-1,0).$

Therefore, the correct answer is "I and III only."

## Representative practice (first three per skill; full bank in practice.json)

### Calculating a Vector Given Its Image Under a Linear Transformation (20 captured questions)

Question 17592186092808 — question.difficulty/easy

The vector $v$ in the plane is mapped to the vector $\begin{bmatrix}7 \\ 20\end{bmatrix}$ under the action of the linear transformation $T$ whose matrix $T$ is given by
$$
\displaystyle T = \begin{bmatrix}1 & 2 \\ 3 & 5\end{bmatrix}.
$$
What is the original vector $v$?

Solution: 

Question 17592186092809 — None

The vector $v$ in the plane is mapped to the vector $\begin{bmatrix}1 \\ 0\end{bmatrix}$ under the action of the linear transformation $T$ whose matrix $T$ is given by
$$
\displaystyle T = \begin{bmatrix}2 & -1 \\ -2 & 2\end{bmatrix}.
$$
What is the original vector $v$?

Solution: 

Question 17592186253591 — question.difficulty/easy

The vector $v$ in the plane is mapped to the vector $\begin{bmatrix}-2 \\ -3\end{bmatrix}$ under the action of the linear transformation $T$ whose matrix $T$ is given by

$$
T=\begin{bmatrix}1 & 4 \\ -2 & 2\end{bmatrix}.
$$

What is the original vector $v?$

Solution: From the given information, we have 

$$
T\cdot v=\begin{bmatrix}-2 \\ -3\end{bmatrix}.
$$

We need to reverse the action of the matrix $T.$ So, we multiply the above equation by ${T}^{-1},$ and we get

$$
\begin{aligned}{T}^{-1}\cdot T\cdot v & ={T}^{-1}\cdot \begin{bmatrix}-2 \\ -3\end{bmatrix} \\ v & ={T}^{-1}\cdot \begin{bmatrix}-2 \\ -3\end{bmatrix}.\end{aligned}
$$

Now, we need to calculate the inverse of $T$, which is

$$
\begin{aligned}{T}^{-1} & =\frac{1}{2-(-8)}\begin{bmatrix}2 & -4 \\ 2 & 1\end{bmatrix} \\  & =\frac{1}{10}\begin{bmatrix}2 & -4 \\ 2 & 1\end{bmatrix}.\end{aligned}
$$

Therefore, the original vector is

$$
\begin{aligned}v & ={T}^{-1}\cdot \begin{bmatrix}-2 \\ -3\end{bmatrix} \\  & =\frac{1}{10}\begin{bmatrix}2 & -4 \\ 2 & 1\end{bmatrix}\begin{bmatrix}-2 \\ -3\end{bmatrix} \\  & =\frac{1}{10}\begin{bmatrix}8 \\ -7\end{bmatrix} \\  & =\begin{bmatrix}\frac{4}{5} \\ -\frac{7}{10}\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}\frac{4}{5} \\ -\frac{7}{10}\end{bmatrix}

### Calculating the Vertices of a Polygon Given Its Image Under a Linear Transformation (19 captured questions)

Question 17592186092895 — None

Consider the linear transformation $T$ with matrix representation $T$, given by
$$
\displaystyle T = \begin{bmatrix}-1 & 1 \\ 1 & 0\end{bmatrix}.
$$

The triangle $S$ is mapped to the triangle $S^{′}$ under the action of $T$. The triangle $S^{′}$ has vertices $(2, 0), (-3, 3)$, and $(0, 0)$. Which of the following are vertices of $S$?

1. $(0, 2)$
2. $(1, 1)$
3. $(0, 0)$

Solution: 

Question 17592186092896 — question.difficulty/hard

Consider the linear transformation $T$ with matrix representation $T,$ given by

$$
T=\begin{bmatrix}2 & 1 \\ 0 & 1\end{bmatrix}.
$$

The parallelogram $P$ is mapped to the parallelogram ${P}^{′}$ under the action of $T.$ The parallelogram ${P}^{′}$ has vertices $(0,2),(-3,3),(12,4),$ and $(7,3).$ Which of the following are vertices of $P?$

Select all that apply.

Solution: First, we create a matrix $Y$ containing all of the vertices of ${P}^{′}:$ 

$$
Y=\begin{bmatrix}0 & -3 & 12 & 7 \\ 2 & 3 & 4 & 3\end{bmatrix}.
$$

Now, if $X$ denotes the matrix that contains the corresponding vertices of $P$, we have

$$
\begin{aligned}T\cdot X & =Y \\ T\cdot X & =\begin{bmatrix}0 & -3 & 12 & 7 \\ 2 & 3 & 4 & 3\end{bmatrix}.\end{aligned}
$$

We need to reverse the action of the matrix $T.$ So, we multiply the above equation by ${T}^{-1},$ and we get

$$
\begin{aligned}{T}^{-1}\cdot T\cdot X & ={T}^{-1}\cdot \begin{bmatrix}0 & -3 & 12 & 7 \\ 2 & 3 & 4 & 3\end{bmatrix} \\ X & ={T}^{-1}\cdot \begin{bmatrix}0 & -3 & 12 & 7 \\ 2 & 3 & 4 & 3\end{bmatrix}.\end{aligned}
$$

The inverse of $T$ is

$$
\begin{aligned}{T}^{-1} & =\frac{1}{2-0}\begin{bmatrix}1 & -1 \\ 0 & 2\end{bmatrix} \\  & =\frac{1}{2}\begin{bmatrix}1 & -1 \\ 0 & 2\end{bmatrix}.\end{aligned}
$$

Therefore, we obtain 

$$
\begin{aligned}X & ={T}^{-1}\cdot \begin{bmatrix}0 & -3 & 12 & 7 \\ 2 & 3 & 4 & 3\end{bmatrix} \\  & =\frac{1}{2}\begin{bmatrix}1 & -1 \\ 0 & 2\end{bmatrix}\begin{bmatrix}0 & -3 & 12 & 7 \\ 2 & 3 & 4 & 3\end{bmatrix} \\  & =\frac{1}{2}\begin{bmatrix}-2 & -6 & 8 & 4 \\ 4 & 6 & 8 & 6\end{bmatrix} \\  & =\begin{bmatrix}-1 & -3 & 4 & 2 \\ 2 & 3 & 4 & 3\end{bmatrix}.\end{aligned}
$$

As a result, the coordinates of $P$ are $(-1,2),(-3,3),(4,4),(2,3).$

Therefore, the correct answer is “The point $(4,4)$” only.

Answer The point $(-2,2)$: false

Answer The point $(1,-1)$: false

Answer The point $(4,4)$: true

Question 17592186235395 — question.difficulty/moderate

![](images/c1/c1d9f53c6aed4acd378f8554df5c8beaaea81e169b5284e51f87204a87b3d53d.png)

A housing complex designed by an architect is shown in the coordinate plane as the region $R$ with vertices $ABCD.$ A highway lies on the line $l$ with equation $2x+y+1=0.$ The area of the complex is $16$ hectares.

A triangular recreational area next to the housing complex is mapped to a larger recreational area under the action of $T.$ The larger recreational area has vertices ${L}^{′}(-15,4),$ ${M}^{′}(-15,2),$ and ${N}^{′}(-21,6).$ Find the corresponding vertices of the smaller recreational area.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
$L(5,$

                                    
                                
                                    
                            
{{field-1}}                
                                    
                                
                                    
                                        
                                        
$)$
$\,$
$M($

                                    
                                
                                    
                            
{{field-2}}                
                                    
                                
                                    
                                        
                                        
$,8)$
$\,$
$N(7,$

                                    
                                
                                    
                            
{{field-3}}                
                                    
                                
                                    
                                        
                                        
$)$

Solution: In part 1, we found that the matrix representation of $T$ is

$$
T=\begin{bmatrix}-3 & 0 \\ 2 & -1\end{bmatrix}.
$$

First, we create a matrix $Y$ containing all of the vertices of the larger recreational area:

$$
Y=\begin{bmatrix}-15 & -15 & -21 \\ 4 & 2 & 6\end{bmatrix}
$$

Now, if $X$ denotes the matrix that contains the corresponding vertices of the smaller recreational area, we have

$$
\begin{aligned}T\cdot X & =Y \\ T\cdot X & =\begin{bmatrix}-15 & -15 & -21 \\ 4 & 2 & 6\end{bmatrix}.\end{aligned}
$$

We need to reverse the action of the matrix $T.$ So, we multiply the above equation by ${T}^{-1},$ and we get

$$
\begin{aligned}{T}^{-1}\cdot T\cdot X & ={T}^{-1}\cdot \begin{bmatrix}-15 & -15 & -21 \\ 4 & 2 & 6\end{bmatrix} \\ X & ={T}^{-1}\cdot \begin{bmatrix}-15 & -15 & -21 \\ 4 & 2 & 6\end{bmatrix}.\end{aligned}
$$

The inverse of $T$ is

$$
\begin{aligned}{T}^{-1} & =\frac{1}{(-1)(-3)-0}\begin{bmatrix}-1 & 0 \\ -2 & -3\end{bmatrix} \\  & =\frac{1}{3}\begin{bmatrix}-1 & 0 \\ -2 & -3\end{bmatrix}.\end{aligned}
$$

Therefore, we obtain

$$
\begin{aligned}X & ={T}^{-1}\cdot \begin{bmatrix}-15 & -15 & -21 \\ 4 & 2 & 6\end{bmatrix} \\  & =\frac{1}{3}\begin{bmatrix}-1 & 0 \\ -2 & -3\end{bmatrix}\begin{bmatrix}-15 & -15 & -21 \\ 4 & 2 & 6\end{bmatrix} \\  & =\frac{1}{3}\begin{bmatrix}15 & 15 & 21 \\ 18 & 24 & 24\end{bmatrix} \\  & =\begin{bmatrix}5 & 5 & 7 \\ 6 & 8 & 8\end{bmatrix}.\end{aligned}
$$

Therefore, the coordinates of the vertices of the smaller recreational area are $L(5,6),$ $M(5,8),$ and $N(7,8).$

Answer field-1: 6

Answer field-2: 5

Answer field-3: 8
