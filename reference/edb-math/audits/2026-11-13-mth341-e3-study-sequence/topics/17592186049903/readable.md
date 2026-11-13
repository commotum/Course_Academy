# 17592186049903 The Kernel of a Linear Transformation

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186125782 — Introduction

The **kernel** of a linear transformation is the set of vectors that map to the zero vector. We define it formally as follows:

*For a linear transformation $\mathbf{T}$, the **kernel** of $\mathbf{T}$ is the set of all the vectors $\mathbf{u}$ such that $\mathbf{T}(\mathbf{u})=\mathbf{0}.$ We can write this as*

$$
\textrm{Ker}(\mathbf{T}) = \left\{ \;\mathbf{u} \;| \; \mathbf{T}(\mathbf{u}) = \mathbf{0} \right\}.
$$

The diagram below shows the kernel of a linear transformation $\mathbf{T}: V \rightarrow V$ in a vector space $V$.

![](images/05/05f8c544d55c6bb07e4063150e586f8b4a7c51a352c2ff8ddda8c4cd5047dd93.png)

Notice that, because of linearity, the zero vector is always in the kernel of a linear transformation: 

$$
\mathbf{T}(\mathbf{0})=\mathbf{T}(0\cdot\mathbf{v})=0\cdot\mathbf{T}(\mathbf{v})= \mathbf 0
$$

for any vector $\mathbf{v}$.



### example 17592186124355 — Determining Whether Given Vectors Belong to the Kernel of a Linear Transformation

Consider the linear transformation 
$$
\mathbf{T}:
{\left[ \begin{array}{c}x \\ y\end{array} \right]}
\longrightarrow 
{\left[ \begin{array}{c}2 x - 4 y \\ - 3 x + 6 y\end{array} \right]}
$$ 
and the vectors 
$$
\mathbf{v}_1={\left[ \begin{array}{c}2 \\ 1\end{array} \right]}, 
\mathbf{v}_2={\left[ \begin{array}{c}3 \\ 1\end{array} \right]}, 
\mathbf{v}_3={\left[ \begin{array}{c}2 \\ 3\end{array} \right]}.
$$
Which of the given vectors belong to the kernel of $\mathbf{T}?$

A vector $\mathbf{u}$ belongs to the kernel of a linear transformation $\mathbf{T}$ if $\mathbf{T}(\mathbf{u})=\mathbf{0}.$ 

Therefore, we need to compute $\mathbf{T}(\mathbf{v}_i)$ for each vector $\mathbf v_i\mathbin{:}$

$$
\begin{aligned}T({v}_{1}) & =T\left(\begin{bmatrix}2 \\ 1\end{bmatrix}\right)=\begin{bmatrix}0 \\ 0\end{bmatrix} \\ T({v}_{2}) & =T\left(\begin{bmatrix}3 \\ 1\end{bmatrix}\right)=\begin{bmatrix}2 \\ -3\end{bmatrix} \\ T({v}_{3}) & =T\left(\begin{bmatrix}2 \\ 3\end{bmatrix}\right)=\begin{bmatrix}-8 \\ 12\end{bmatrix}\end{aligned}
$$

Since $\,\mathbf{T}(\mathbf{v}_1)=\mathbf{0},$ we conclude that, of the given vectors, the only vector that belongs to the kernel of $\,\mathbf{T}$ is $\,\mathbf{v}_1.$

### example 17592186124327 — Calculating a Component of a Vector in the Kernel of a Linear Transformation

Consider the linear transformation $$
\displaystyle \mathbf{T}:
{\left[ \begin{array}{c}x \\ y \\ z\end{array} \right]}
\longrightarrow 
{\left[ \begin{array}{c}3 x + 12 y - 3 z \\ - 2 x + 4 y - 2 z \\ 6 x - 3 y + 3 z\end{array} \right]}
$$ and the vector $\,\mathbf{u}={\left[ \begin{array}{c}k \\ 2 \\ 6\end{array} \right]}.$ Find the value of $\,k\,$ such that $\,\mathbf{u}\in\textrm{Ker}(\mathbf{T}).$

A vector $\mathbf{u}$ belongs to the kernel of a linear transformation $\mathbf{T}$ if $\mathbf{T}(\mathbf{u})=\mathbf{0}.$ 

So, we need to solve the following equation:

$$
\begin{aligned}T(u) & =0 \\ \begin{bmatrix}3\cdot k+12\cdot 2-3\cdot 6 \\ -2\cdot k+4\cdot 2-2\cdot 6 \\ 6\cdot k-3\cdot 2+3\cdot 6\end{bmatrix} & =\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix} \\ \begin{bmatrix}3k+6 \\ -2k-4 \\ 6k+12\end{bmatrix} & =\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}\end{aligned}
$$

Therefore, we get the system

$$
\left\{\begin{aligned}3k+6 &=0 \\ -2k-4 &=0 \\ 6k+12 &=0.\end{aligned}\right.
$$

The solution to all three of these equations is $k=-2.$

### tutorial 17592186125818 — Finding the Kernel of a Linear Transformation

We know how to determine whether a given vector is in the kernel of a linear transformation. But how do we find the kernel of a linear transformation?

First, remember that if $T$ is the standard matrix of $\mathbf{T},$ then 

$$
\textrm{Ker}(\mathbf{T}) = \textrm{Null}(T) = \left\{ \;\mathbf{x} \;|\; T\mathbf{x}=\mathbf{0} \right\}.
$$

Therefore, to find all the vectors in the kernel of a linear transformation, we just need to find the null space of the corresponding standard matrix. We can do this by solving the matrix equation $T\mathbf{x}=\mathbf{0}.$



### example 17592186124325 — Finding the Kernel of a Linear Transformation

Consider the linear transformation $$
\displaystyle \mathbf{T}:
{\left[ \begin{array}{c}x \\ y\end{array} \right]}\longrightarrow
{\left[ \begin{array}{c}2 x + 4 y \\ 3 x + 6 y\end{array} \right]}.
$$ Find $\textrm{Ker}(\mathbf{T}).$

Finding the kernel of $\mathbf{T}$ is equivalent to finding the null space of the standard matrix of $\mathbf{T}.$

For the given linear transformation, the standard matrix is $T={\left[ \begin{array}{cc}2 & 4 \\ 3 & 6\end{array} \right]}.$

Setting $\mathbf{x}={\left[ \begin{array}{c}x \\ y\end{array} \right]},$ we then need to solve the equation $T\mathbf{x}=\mathbf{0}.$ First, we reduce $T$ to row echelon form, as follows:

$$
\begin{aligned}T & =\begin{bmatrix}2 & 4 \\ 3 & 6\end{bmatrix} & {R}_{2} & :={R}_{2}+\left(-\frac{3}{2}\right){R}_{1} \\  & ∼\begin{bmatrix}2 & 4 \\ 0 & 0\end{bmatrix}\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is $x,$ and we have one free variable, $y.$ That means we need to find $x$ in terms of $y.$

From the first equation, we get 

$$
x=-2y.
$$

 

Therefore, the kernel of the linear transformation $\,\mathbf{T}$ is $\left\{ {\left[ \begin{array}{c}- 2 y \\ y\end{array} \right]} \: : \: y\in\mathbb{R} \right\}.$

### tutorial 17592186125820 — The Nullity of a Linear Transformation

The **nullity** of a linear transformation $\mathbf{T}$ is the dimension of its kernel. This means that

$$
\text{nullity}(\mathbf{T}) = \dim(\textrm{Ker}(\mathbf{T})) = \text{nullity}(T).
$$

To compute the dimension of the kernel of $\mathbf{T},$ we just have to reduce the matrix $T$ to row echelon form and count the number of  non-pivot columns.



### example 17592186124326 — Finding the Nullity of a Linear Transformation

Given the linear transformation $$
\displaystyle \mathbf{T}:
{\left[ \begin{array}{c}x \\ y \\ z\end{array} \right]}\longrightarrow
{\left[ \begin{array}{c}2 x + 4 y \\ 4 x + 10 y - z \\ z - 6 x - 12 y\end{array} \right]},
$$ find $\,\textrm{nullity}(\mathbf{T}).$

First, we write down the standard matrix of $\mathbf{T}\mathbin{:}$

$$
T={\left[ \begin{array}{ccc}2 & 4 & 0 \\ 4 & 10 & - 1 \\ - 6 & - 12 & 1\end{array} \right]}
$$

Recall that $\textrm{nullity}(\mathbf{T}) = \textrm{nullity}(T) = \textrm{dim}(\textrm{Null}(T)).$

In order to find $\textrm{dim}(\textrm{Null}(T)),$ we reduce $T$ to row echelon form, as follows:

$$
\begin{aligned}T & =\begin{bmatrix}2 & 4 & 0 \\ 4 & 10 & -1 \\ -6 & -12 & 1\end{bmatrix} & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼\begin{bmatrix}2 & 4 & 0 \\ 0 & 2 & -1 \\ -6 & -12 & 1\end{bmatrix} & {R}_{3} & :={R}_{3}+3{R}_{1} \\  & ∼\begin{bmatrix}2 & 4 & 0 \\ 0 & 2 & -1 \\ 0 & 0 & 1\end{bmatrix}\end{aligned}
$$

The reduced matrix above has no non-pivot columns. Therefore, 

$$
\textrm{nullity}(\mathbf{T})=\textrm{dim}(\textrm{Null}(T))=0.
$$

## Representative practice (first three per skill; full bank in practice.json)

### Determining Whether Given Vectors Belong to the Kernel of a Linear Transformation (10 captured questions)

Question 17592186125103 — question.difficulty/easy

Consider the linear transformation
$$
\displaystyle T: \begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}4x - y \\ -8x + 2y\end{bmatrix}
$$
and the vectors
$$
\displaystyle v_{1} = \begin{bmatrix}1 \\ 4\end{bmatrix}, v_{2} = \begin{bmatrix}2 \\ 8\end{bmatrix}, v_{3} = \begin{bmatrix}2 \\ 6\end{bmatrix}.
$$
Which of the given vectors belong to the kernel of $T$?

Solution: 

Question 17592186125136 — question.difficulty/moderate

Consider the linear transformation
$$
\displaystyle T: \begin{bmatrix}x \\ y \\ z\end{bmatrix}⟶\begin{bmatrix}x - 2y + 3z \\ 4x + y + z \\ 0\end{bmatrix}
$$
and the vectors
$$
\displaystyle v_{1} = \begin{bmatrix}1 \\ 1 \\ 1\end{bmatrix}, v_{2} = \begin{bmatrix}5 \\ -11 \\ -9\end{bmatrix}, v_{3} = \begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}.
$$
Which of the given vectors belong to $Ker(T)$?

Solution: 

Question 17592186272001 — question.difficulty/easy

Consider the linear transformation 
$$
\displaystyle T:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}4x+2y \\ 6x+3y\end{bmatrix}
$$ 
and the vectors 
$$
\displaystyle {v}_{1}=\begin{bmatrix}1 \\ 2\end{bmatrix},{v}_{2}=\begin{bmatrix}-3 \\ 6\end{bmatrix},{v}_{3}=\begin{bmatrix}-2 \\ 6\end{bmatrix}.
$$
Which of the given vectors belong to the kernel of $T?$

Solution: A vector $u$ belongs to the kernel of a linear transformation $T$ if $T(u)=0.$ 

Therefore, we need to compute $T({v}_{i})$ for each vector ${v}_{i}:$

$$
\begin{aligned}T({v}_{1}) & =T\left(\begin{bmatrix}1 \\ 2\end{bmatrix}\right)=\begin{bmatrix}8 \\ 12\end{bmatrix} \\ T({v}_{2}) & =T\left(\begin{bmatrix}-3 \\ 6\end{bmatrix}\right)=\begin{bmatrix}0 \\ 0\end{bmatrix} \\ T({v}_{3}) & =T\left(\begin{bmatrix}-2 \\ 6\end{bmatrix}\right)=\begin{bmatrix}4 \\ 6\end{bmatrix}\end{aligned}
$$

Since $\,T({v}_{2})=0,$ we conclude that the only vector that belongs to the kernel of $\,T$ is ${v}_{2}.$

Answer selection: ${v}_{2}$  only

### Calculating a Component of a Vector in the Kernel of a Linear Transformation (12 captured questions)

Question 17592186125104 — question.difficulty/easy

Consider the linear transformation $T:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}4x-2y \\ -10x+5y\end{bmatrix}$ and the vector $\,u=\begin{bmatrix}k \\ 6\end{bmatrix}.$ Find the value of $\,k\,$ such that $\,u\in \text{Ker}(T).$

Solution: A vector $u$ belongs to the kernel of a linear transformation $T$ if $T(u)=0.$ 

So, we need to solve the following equation:

$$
\begin{aligned}T(u) & =0 \\ \begin{bmatrix}4\cdot k-2\cdot 6 \\ -10\cdot k+5\cdot 6\end{bmatrix} & =\begin{bmatrix}0 \\ 0\end{bmatrix} \\ \begin{bmatrix}4k-12 \\ -10k+30\end{bmatrix} & =\begin{bmatrix}0 \\ 0\end{bmatrix}\end{aligned}
$$

Therefore, we get the system

$$
\left\{\begin{aligned}4k-12 &=0 \\ -10k+30 &=0.\end{aligned}\right.
$$

The solution to both of these equations is $k=3.$

Answer selection: 3

Question 17592186125107 — question.difficulty/moderate

Consider the linear transformation $T:\begin{bmatrix}x \\ y \\ z\end{bmatrix}⟶\begin{bmatrix}-8x+4y \\ 6x-3y \\ 2x-y\end{bmatrix}$ and the vector $\,u=\begin{bmatrix}3 \\ k \\ 1\end{bmatrix}.$ Find the value of $\,k\,$ such that $\,u\in \text{Ker}(T).$

Solution: A vector $u$ belongs to the kernel of a linear transformation $T$ if $T(u)=0.$ 

So, we need to solve the following equation:

$$
\begin{aligned}T(u) & =0 \\ \begin{bmatrix}-8\cdot 3+4\cdot k \\ 6\cdot 3-3\cdot k \\ 2\cdot 3-k\end{bmatrix} & =\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix} \\ \begin{bmatrix}-24+4k \\ 18-3k \\ 6-k\end{bmatrix} & =\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}\end{aligned}
$$

Therefore, we get the system

$$
\left\{\begin{aligned}-24+4k &=0 \\ 18-3k &=0 \\ 6-k &=0.\end{aligned}\right.
$$

The solution to all three of these equations is $k=6.$

Answer selection: 6

Question 17592186272002 — question.difficulty/easy

Consider the linear transformation $T:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}2x+4y \\ 5x+10y\end{bmatrix}$ and the vector $\,u=\begin{bmatrix}k \\ 3\end{bmatrix}.$ Find the value of $\,k\,$ such that $\,u\in \text{Ker}(T).$

Solution: A vector $u$ belongs to the kernel of a linear transformation $T$ if $T(u)=0.$ 

So, we need to solve the following equation:

$$
\begin{aligned}T(u) & =0 \\ \begin{bmatrix}2\cdot k+4\cdot 3 \\ 5\cdot k+10\cdot 3\end{bmatrix} & =\begin{bmatrix}0 \\ 0\end{bmatrix} \\ \begin{bmatrix}2k+12 \\ 5k+30\end{bmatrix} & =\begin{bmatrix}0 \\ 0\end{bmatrix}\end{aligned}
$$

Therefore, we get the system

$$
\left\{\begin{aligned}2k+12 &=0 \\ 5k+30 &=0.\end{aligned}\right.
$$

The solution to both of these equations is $k=-6.$

Answer selection: -6

### Finding the Kernel of a Linear Transformation (11 captured questions)

Question 17592186125105 — question.difficulty/easy

Find a basis of $\,\text{Ker}(T)$ given that $T:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}-9x-3y \\ -12x-4y\end{bmatrix}.$

Solution: Finding the kernel of $\,T\,$ is equivalent to finding the null space of the standard matrix of $\,T.$

For the given linear transformation, the standard matrix is $T=\begin{bmatrix}-9 & -3 \\ -12 & -4\end{bmatrix}.$

Setting $x=\begin{bmatrix}x \\ y\end{bmatrix},$ we then need to solve the equation $Tx=0.$ First, we reduce $T$ to row echelon form, as follows:

$$
\begin{aligned}T & =\begin{bmatrix}-9 & -3 \\ -12 & -4\end{bmatrix} & {R}_{2} & :={R}_{2}+\left(-\frac{4}{3}\right){R}_{1} \\  & ∼\begin{bmatrix}-9 & -3 \\ 0 & 0\end{bmatrix}\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is $x$, and we have one free variable, $y.$ That means we need to find $x$ in terms of $y.$

From the first equation, we get 

$$
x=-\frac{1}{3}y.
$$

 

Therefore, if $x\in \text{Ker}(T),$ then 

$$
x=\begin{bmatrix}-\frac{1}{3}y \\ y\end{bmatrix}=\begin{bmatrix}-\frac{1}{3} \\ 1\end{bmatrix}y,\,y\in R.
$$

This implies that $B={\begin{bmatrix}-\frac{1}{3} \\ 1\end{bmatrix}}$ is a basis of $\text{Ker}(T).$

Answer selection: {\begin{bmatrix}-\frac{1}{3} \\ 1\end{bmatrix}}

Question 17592186125138 — question.difficulty/moderate

Consider the linear transformation $$
\displaystyle T:\begin{bmatrix}x \\ y \\ z\end{bmatrix}⟶\begin{bmatrix}2x-4y+2z \\ x-3y+z \\ 4x-4y+z\end{bmatrix}.
$$ Find $\,\text{Ker}(T).$

Solution: Finding the kernel of $T$ is equivalent to finding the null space of the standard matrix of $T.$

Fror the given linear transformation, the standard matrix is $T=\begin{bmatrix}2 & -4 & 2 \\ 1 & -3 & 1 \\ 4 & -4 & 1\end{bmatrix}.$

Setting $x=\begin{bmatrix}x \\ y \\ z\end{bmatrix},$ we then need to solve the equation $Tx=0.$ First, we find reduce $T$ to row echelon form, as follows:

$$
\begin{aligned}T & =\begin{bmatrix}2 & -4 & 2 \\ 1 & -3 & 1 \\ 4 & -4 & 1\end{bmatrix} &  & \begin{aligned}{R}_{1}↔{R}_{2}\end{aligned} \\  & ∼\begin{bmatrix}1 & -3 & 1 \\ 2 & -4 & 2 \\ 4 & -4 & 1\end{bmatrix} &  & \begin{aligned}{R}_{2}:={R}_{2}+(-2){R}_{1} \\ {R}_{3}:={R}_{3}+(-4){R}_{1}\end{aligned} \\  & ∼\begin{bmatrix}1 & -3 & 1 \\ 0 & 2 & 0 \\ 0 & 8 & -3\end{bmatrix} &  & \begin{aligned}{R}_{3}:={R}_{3}+(-4){R}_{2}\end{aligned} \\  & ∼\begin{bmatrix}1 & -3 & 1 \\ 0 & 2 & 0 \\ 0 & 0 & -3\end{bmatrix}\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are $x,$ $y,$ and $z.$ From the third equation, we obtain $z=0$ and from the second equation, we get $y=0.$ Substituting these into the first equation, we have $x=0.$ 

Therefore, the kernel of the linear transformation $\,T$ is ${\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}}.$

Answer selection: {\begin{bmatrix}0 \\ 0 \\ 0\end{bmatrix}}

Question 17592186272014 — question.difficulty/easy

Find a basis of $\,\text{Ker}(T)$ given that $T:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}4x-2y \\ -6x+3y\end{bmatrix}.$

Solution: Finding the kernel of $\,T\,$ is equivalent to finding the null space of the standard matrix of $\,T.$

For the given linear transformation, the standard matrix is $T=\begin{bmatrix}4 & -2 \\ -6 & 3\end{bmatrix}.$ 

Setting $x=\begin{bmatrix}x \\ y\end{bmatrix},$ we then need to solve the equation $Tx=0.$ First, we reduce $T$ to row echelon form, as follows:

$$
\begin{aligned}T & =\begin{bmatrix}4 & -2 \\ -6 & 3\end{bmatrix} & {R}_{2} & :={R}_{2}+\frac{6}{4}{R}_{1} \\  & ∼\begin{bmatrix}4 & -2 \\ 0 & 0\end{bmatrix}\end{aligned}
$$

The basic variables are the variables whose coefficients are pivots. In this case, the basic variable is $x$, and we have one free variable, $y.$ That means we need to find $x$ in terms of $y.$

From the first equation, we get 

$$
x=\frac{1}{2}y.
$$

  

Therefore, if $x\in \text{Ker}(T),$ then 

$$
x=\begin{bmatrix}\frac{1}{2}y \\ y\end{bmatrix}=y\begin{bmatrix}\frac{1}{2} \\ 1\end{bmatrix},\,y\in R.
$$

This implies that $B={\begin{bmatrix}\frac{1}{2} \\ 1\end{bmatrix}}$ is a basis of $\text{Ker}(T).$

Answer selection: {\begin{bmatrix}\frac{1}{2} \\ 1\end{bmatrix}}

### Finding the Nullity of a Linear Transformation (11 captured questions)

Question 17592186125134 — None

Given the linear transformation $$
\displaystyle T: \begin{bmatrix}x \\ y \\ z\end{bmatrix}⟶\begin{bmatrix}-3y - 2z \\ x - 2z - 4y \\ z - 3x + 4y\end{bmatrix},
$$ find $nullity(T)$.

Solution: 

Question 17592186125135 — question.difficulty/easy

Given the linear transformation $T:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}5x-7y \\ 14y-10x\end{bmatrix},$
find  $3\cdot \text{nullity}(T)+1.$

Solution: First, we write down the standard matrix of $T:$

$$
T=\begin{bmatrix}5 & -7 \\ -10 & 14\end{bmatrix}
$$

Recall that $\text{nullity}(T)=\text{nullity}(T)=\text{dim}(\text{Null}(T)).$

In order to find $\text{dim}(\text{Null}(T)),$ we reduce $T$ to row echelon form, as follows:

$$
\begin{aligned}T & =\begin{bmatrix}5 & -7 \\ -10 & 14\end{bmatrix} & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼\begin{bmatrix}5 & -7 \\ 0 & 0\end{bmatrix}\end{aligned}
$$

The reduced matrix above has $1$ non-pivot column (the $2$nd one). 

Therefore, $\text{nullity}(T)=\text{dim}(\text{Null}(T))=1.$

Finally, we obtain

$$
3\cdot \text{nullity}(T)+1=3\cdot 1+1=4.
$$

Answer selection: 4

Question 17592186326813 — question.difficulty/easy

Given the linear transformation $T:\begin{bmatrix}x \\ y\end{bmatrix}⟶\begin{bmatrix}-3x-6y \\ 2x-4y\end{bmatrix},$ find $9\cdot \text{nullity}(T)+4.$

Solution: First, we write down the standard matrix of $T:$

$$
T=\begin{bmatrix}-3 & -6 \\ 2 & -4\end{bmatrix}
$$

Recall that $\text{nullity}(T)=\text{nullity}(T)=\text{dim}(\text{Null}(T)).$

In order to find $\text{dim}(\text{Null}(T)),$ we reduce $T$ to row echelon form, as follows:

$$
\begin{aligned}T & =\begin{bmatrix}-3 & -6 \\ 2 & -4\end{bmatrix} & {R}_{2} & :={R}_{2}+\frac{2}{3}{R}_{1} \\  & ∼\begin{bmatrix}-3 & -6 \\ 0 & -8\end{bmatrix}\end{aligned}
$$

The reduced matrix above has no non-pivot column. 

Therefore, $\text{nullity}(T)=\text{dim}(\text{Null}(T))=0.$

Finally, we obtain

$$
9\cdot \text{nullity}(T)+4=9\cdot 0+4=4.
$$

Answer selection: 4
