# 17592186048203 The Standard Matrix of a Linear Transformation

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186125781 — Introduction

Every linear transformation $\mathbf{T}$ that acts on 2D-vectors has a $2 \times 2$ matrix $T$ associated with it. The matrix is called the **standard matrix** of the linear transformation. 
For any vector $\mathbf{v},$ the standard matrix $T$ of a linear transformation $\mathbf{T}$ must have the property

$$
\mathbf{T}(\mathbf{v}) = T \cdot \mathbf{v}
$$

where $T \cdot \mathbf{v}$ is the matrix product of the standard matrix $T$ and the vector $\mathbf{v}.$

To illustrate, consider the following linear transformation:

$$
\mathbf{S}: \begin{bmatrix}x \\ y\end{bmatrix} \longrightarrow \begin{bmatrix}-3x+7y \\ x-5y\end{bmatrix}
$$

The standard matrix for the linear transformation $\mathbf{S}$ is <div class="matrix-operands matrix-operands-stacked">
<div>$S=\begin{bmatrix}-3 & 7 \\ 1 & -5\end{bmatrix}$</div>
</div> since it has the following property:

$$
\begin{aligned}\overbrace{\begin{bmatrix}-3 & 7 \\ 1 & -5\end{bmatrix}}^{S}\cdot \begin{bmatrix}x \\ y\end{bmatrix} & =\begin{bmatrix}-3\cdot x+7\cdot y \\ 1\cdot x+(-5)\cdot y\end{bmatrix} \\  & =\begin{bmatrix}-3x+7y \\ x-5y\end{bmatrix} \\  & =S\begin{bmatrix}x \\ y\end{bmatrix}.\end{aligned}
$$

Notice here that $\mathbf{S}$ (using a **bold** letter) denotes the transformation (function) itself, while $S$ (big *italic* letter) is a $2 \times 2$ matrix that corresponds to the linear transformation.

In general, the standard matrix of the linear transformation $\mathbf{T}: \begin{bmatrix}x \\ y\end{bmatrix} \longrightarrow \begin{bmatrix}{\color{blue}{a}}x+{\color{blue}{b}}y \\ {\color{blue}{c}}x+{\color{blue}{d}}y\end{bmatrix}$ is

$$
T=\begin{bmatrix}{\color{blue}{a}} & {\color{blue}{b}} \\ {\color{blue}{c}} & {\color{blue}{d}}\end{bmatrix}.
$$

We can learn a lot about linear transformations by looking at their standard matrices.



### example 17592186124321 — Identifying the Standard Matrix of a Linear Transformation

Find the standard matrix that represents  the  linear  transformation $\mathbf{T},$ where
$$
\mathbf{T}:
{\left[ \begin{array}{c}x \\ y\end{array} \right]}
\longrightarrow 
{\left[ \begin{array}{c}x + 3 y \\ 2 x - y\end{array} \right]}.
$$

We require a $2\times 2$ matrix ${T}$ such that
$$
{T} \cdot
    {\left[ \begin{array}{c}x \\ y\end{array} \right]}
    =
    {\left[ \begin{array}{c}{\color{blue}1} \cdot  x + {\color{blue}3} \cdot  y \\ {\color{blue}2} \cdot  x + {\color{blue}( - 1 )} \cdot  y\end{array} \right]}.
$$
    Notice that
$$
{\left[ \begin{array}{cc}{\color{blue}1} & {\color{blue}3} \\ {\color{blue}2} & {\color{blue}- 1}\end{array} \right]}
	\cdot
    {\left[ \begin{array}{c}x \\ y\end{array} \right]}
    =
    {\left[ \begin{array}{c}x + 3 y \\ 2 x - y\end{array} \right]}.
$$

Therefore, the matrix which represents the linear transformation $\mathbf{T}$ is
$$
T=
    {\left[ \begin{array}{cc}1 & 3 \\ 2 & - 1\end{array} \right]}.
$$

### example 17592186124323 — Determining a Linear Transformation Given its Standard Matrix

What is the linear transformation $\mathbf{T}$ whose standard matrix is $T={\left[ \begin{array}{cc}8 & - 1 \\ - 5 & - 2\end{array} \right]}?$

Consider a general vector $\,{\left[ \begin{array}{c}x \\ y\end{array} \right]}.$ Multiplying by the matrix $T,$ we have

$$
\begin{aligned}T\cdot \begin{bmatrix}x \\ y\end{bmatrix} & =\begin{bmatrix}8 & -1 \\ -5 & -2\end{bmatrix}\cdot \begin{bmatrix}x \\ y\end{bmatrix} \\  & =\begin{bmatrix}8x-y \\ -5x-2y\end{bmatrix}.\end{aligned}
$$

Therefore, the linear transformation $\,\mathbf{T}\,$ is given by

$$
\mathbf{T}: {\left[ \begin{array}{c}x \\ y\end{array} \right]} \longrightarrow {\left[ \begin{array}{c}8 x - y \\ - 5 x - 2 y\end{array} \right]}.
$$

### example 17592186124324 — Finding the Image of a Vector Under a Linear Transformation Given its Standard Matrix

Consider the matrix $T$ and the vector $\mathbf{v}$ given below. If $T$ is the standard matrix of the linear transformation $\mathbf{T},$ find $\mathbf{T}(\mathbf{v}).$

$$
T={\left[ \begin{array}{cc}4 & 7 \\ - 6 & - 2\end{array} \right]}, \qquad
\mathbf{v}={\left[ \begin{array}{c}- 2 \\ 5\end{array} \right]}.
$$

Using the fact that $\,\mathbf{T}(\mathbf{v})=T\cdot \mathbf{v},$ we get

$$
\begin{aligned}T(v) & =T\cdot v \\  & =\begin{bmatrix}4 & 7 \\ -6 & -2\end{bmatrix}\cdot \begin{bmatrix}-2 \\ 5\end{bmatrix} \\  & =\begin{bmatrix}27 \\ 2\end{bmatrix}.\end{aligned}
$$

### example 17592186124322 — Identifying the Standard Matrix of a Linear Transformation With Rearranging

Find the standard matrix that represents  the  linear  transformation $\mathbf{T},$ where
$$
\mathbf{T}:
{\left[ \begin{array}{c}x \\ y\end{array} \right]}
\longrightarrow 
{\left[ \begin{array}{c}4 y - 5 x \\ y + 3 x\end{array} \right]}.
$$

First, rewrite the order of the variables in the usual way:

$$
\mathbf{T}:
{\left[ \begin{array}{c}x \\ y\end{array} \right]}
\longrightarrow 
{\left[ \begin{array}{c}- 5 x + 4 y \\ 3 x + y\end{array} \right]}
$$

We require a $2\times 2$ matrix ${T}$ such that
$$
{T}\cdot
    {\left[ \begin{array}{c}x \\ y\end{array} \right]}
    =
{\left[ \begin{array}{c}- 5 x + 4 y \\ 3 x + y\end{array} \right]}.
$$

Notice that
$$
{\left[ \begin{array}{cc}- 5 & 4 \\ 3 & 1\end{array} \right]}
	\cdot
    {\left[ \begin{array}{c}x \\ y\end{array} \right]}
    =
    {\left[ \begin{array}{c}- 5 x + 4 y \\ 3 x + y\end{array} \right]}.
$$

Therefore, the matrix which represents the linear transformation $\mathbf{T}$ is
$$
T=
    {\left[ \begin{array}{cc}- 5 & 4 \\ 3 & 1\end{array} \right]}.
$$

## Representative practice (first three per skill; full bank in practice.json)

### Identifying the Standard Matrix of a Linear Transformation (14 captured questions)

Question 17592186124777 — None

Find the standard matrix that represents the linear transformation $T$, where$T: \begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}x - 5y \\ 2x + y\end{bmatrix}$.

Solution: 

Question 17592186124778 — question.difficulty/easy

Find the standard matrix that represents  the  linear  transformation $T$, where

$$
T:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}y \\ x\end{bmatrix}.
$$

Solution: We require a $2\times 2$ matrix $T$ such that
    

$$
T\cdot \begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}0\cdot x+1\cdot y \\ 1\cdot x+0\cdot y\end{bmatrix}.
$$

Notice that
    

$$
\begin{bmatrix}0 & 1 \\ 1 & 0\end{bmatrix}\cdot \begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}y \\ x\end{bmatrix}.
$$

Therefore, the matrix which represents the linear transformation $T$ is
    

$$
\begin{bmatrix}0 & 1 \\ 1 & 0\end{bmatrix}.
$$

Answer selection: \begin{bmatrix}0 & 1 \\ 1 & 0\end{bmatrix}

Question 17592186253579 — question.difficulty/easy

Find the standard matrix that  represents  the  linear  transformation $T$, where

$$
T:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}2x+3y \\ y\end{bmatrix}.
$$

Solution: We require a $2\times 2$ matrix $T$ such that
    

$$
T\cdot \begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}2\cdot x+3\cdot y \\ 0\cdot x+1\cdot y\end{bmatrix}.
$$

Notice that
    

$$
\begin{bmatrix}2 & 3 \\ 0 & 1\end{bmatrix}\cdot \begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}2x+3y \\ y\end{bmatrix}.
$$

Therefore, the matrix which represents the linear transformation $T$ is
    

$$
\begin{bmatrix}2 & 3 \\ 0 & 1\end{bmatrix}.
$$

Answer selection: \begin{bmatrix}2 & 3 \\ 0 & 1\end{bmatrix}

### Determining a Linear Transformation Given its Standard Matrix (13 captured questions)

Question 17592186125113 — None

What is the linear transformation $T$ whose standard matrix is
$T = \begin{bmatrix}0 & -2 & 4 \\ 2 & -3 & 0 \\ 1 & -1 & 1\end{bmatrix}$?

Solution: 

Question 17592186125114 — question.difficulty/easy

What is the linear transformation $T$ whose standard matrix is $T=\begin{bmatrix}-4 & 8 \\ -3 & 2\end{bmatrix}?$

Solution: Consider a general vector $\,\begin{bmatrix}x \\ y\end{bmatrix}.$ Multiplying by the matrix $T,$ we have

$$
\begin{aligned}T\cdot \begin{bmatrix}x \\ y\end{bmatrix} & =\begin{bmatrix}-4 & 8 \\ -3 & 2\end{bmatrix}\cdot \begin{bmatrix}x \\ y\end{bmatrix} \\  & =\begin{bmatrix}-4x+8y \\ -3x+2y\end{bmatrix}.\end{aligned}
$$

Therefore, the linear transformation $\,T\,$ is given by

$$
T:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}-4x+8y \\ -3x+2y\end{bmatrix}.
$$

Answer selection: T:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}-4x+8y \\ -3x+2y\end{bmatrix}

Question 17592186284601 — question.difficulty/moderate

What is the linear transformation $T$ whose standard matrix is 
$$
\displaystyle T=\begin{bmatrix}1 & 0 & 1 \\ 0 & -1 & 1 \\ 1 & -1 & 0\end{bmatrix}?
$$

Solution: Consider a general vector $\,\begin{bmatrix}x \\ y \\ z\end{bmatrix}.$ Multiplying by the matrix $T,$ we have

$$
\begin{aligned}T\cdot \begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}1 & 0 & 1 \\ 0 & -1 & 1 \\ 1 & -1 & 0\end{bmatrix}\cdot \begin{bmatrix}x \\ y \\ z\end{bmatrix} \\  & =\begin{bmatrix}x+z \\ -y+z \\ x-y\end{bmatrix}.\end{aligned}
$$

Therefore, the linear transformation $\,T\,$ is given by

$$
T:\begin{bmatrix}x \\ y \\ z\end{bmatrix}⟶\begin{bmatrix}x+z \\ -y+z \\ x-y\end{bmatrix}.
$$

Answer selection: T:\begin{bmatrix}x \\ y \\ z\end{bmatrix}⟶\begin{bmatrix}x+z \\ -y+z \\ x-y\end{bmatrix}

### Finding the Image of a Vector Under a Linear Transformation Given its Standard Matrix (14 captured questions)

Question 17592186125110 — None

Consider the matrix $T$ and the vector $v$ given below. If $T$ is the standard matrix of the linear transformation $T$, find $T(v)$.

$$
\displaystyle T = \begin{bmatrix}-2 & 3 \\ 5 & 1\end{bmatrix}, v = \begin{bmatrix}-3 \\ 2\end{bmatrix}
$$

Solution: 

Question 17592186125111 — question.difficulty/moderate

Consider the matrix $T$ and the vector $v$ given below. If $T$ is the standard matrix of the linear transformation $T,$ find $T(v).$

$$
T=\begin{bmatrix}-2 & 4 & -1 \\ 5 & 1 & 3 \\ -1 & 3 & 4\end{bmatrix},\,v=\begin{bmatrix}1 \\ 4 \\ -2\end{bmatrix}
$$

Solution: Using the fact that $\,T(v)=T\cdot v,$ we get

$$
\begin{aligned}T(v) & =T\cdot v \\  & =\begin{bmatrix}-2 & 4 & -1 \\ 5 & 1 & 3 \\ -1 & 3 & 4\end{bmatrix}\cdot \begin{bmatrix}1 \\ 4 \\ -2\end{bmatrix} \\  & =\begin{bmatrix}16 \\ 3 \\ 3\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}16 \\ 3 \\ 3\end{bmatrix}

Question 17592186284602 — question.difficulty/moderate

Consider the matrix $T$ and the vector $v$ given below. If $T$ is the standard matrix of the linear transformation $T,$ find $T(v).$

$$
T=\begin{bmatrix}3 & -1 & 1 \\ 6 & 2 & 0 \\ -1 & 0 & 1\end{bmatrix},\,v=\begin{bmatrix}1 \\ 3 \\ 2\end{bmatrix}
$$

Solution: Using the fact that $\,T(v)=T\cdot v,$ we get

$$
\begin{aligned}T(v) & =T\cdot v \\  & =\begin{bmatrix}3 & -1 & 1 \\ 6 & 2 & 0 \\ -1 & 0 & 1\end{bmatrix}\cdot \begin{bmatrix}1 \\ 3 \\ 2\end{bmatrix} \\  & =\begin{bmatrix}2 \\ 12 \\ 1\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}2 \\ 12 \\ 1\end{bmatrix}

### Identifying the Standard Matrix of a Linear Transformation With Rearranging (13 captured questions)

Question 17592186125112 — question.difficulty/hard

Find the standard matrix that represents the linear transformation $T$, where
$$
\displaystyle T: \begin{bmatrix}x \\ y \\ z\end{bmatrix}⟶\begin{bmatrix}2z + 3y - x \\ 2y - 3z + x \\ z - x + 3y\end{bmatrix}.
$$

Solution: 

Question 17592186125232 — None

Find the standard matrix that represents the linear transformation $T$, where
$$
\displaystyle T: \begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}y - x \\ y + x\end{bmatrix}.
$$

Solution: 

Question 17592186253647 — question.difficulty/moderate

Find the standard matrix that represents  the  linear  transformation  $T$, where

$$
T:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}y-3x \\ y\end{bmatrix}.
$$

Solution: First, rewrite the order of the variables in the usual way:

$$
T:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}-3x+y \\ y\end{bmatrix}
$$

We require a $2\times 2$ matrix $T$ such that
    

$$
T\cdot \begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}-3x+y \\ y\end{bmatrix}.
$$

Notice that
    

$$
\begin{bmatrix}-3 & 1 \\ 0 & 1\end{bmatrix}\cdot \begin{bmatrix}x \\ y\end{bmatrix}=\begin{bmatrix}-3x+y \\ y\end{bmatrix}.
$$

Therefore, the matrix which represents the linear transformation  $T$ is
    

$$
\begin{bmatrix}-3 & 1 \\ 0 & 1\end{bmatrix}.
$$

Answer selection: \begin{bmatrix}-3 & 1 \\ 0 & 1\end{bmatrix}
