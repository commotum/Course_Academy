# 17592186049539 The Image and Rank of a Linear Transformation

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186125783 — Introduction

The **image** (or **range**) of a linear transformation $\mathbf{T}$ is the set of all vectors $\mathbf{b}$ that the transformation maps to. That is to say
$$
\textrm{Im}(\mathbf{T}) = 
		\left\{ 
			\mathbf{b} \:|\: 
			{ {\mathbf{T} ( \mathbf{u} ) = \mathbf{b}} \text{ for some } {\mathbf{u}}}
		\right\}
$$

The diagram below gives a schematic representation of the image of a linear transformation $\mathbf{T}: V \rightarrow V$ for a vector space $V.$

![](images/b8/b859250756eb3870f9c1d4d7e6e78f044adf2b0c4cd94a87d01011879d668afc.png)

Notice that $\mathbf{0}$ is always in the image of a linear transformation since $\mathbf{T}(\mathbf{0})=\mathbf{0}.$

As an example, let's consider the linear transformation
$$
\mathbf{S}: {\left[ \begin{array}{c}x \\ y\end{array} \right]} \longrightarrow {\left[ \begin{array}{c}2 x + 4 y \\ 3 x + 6 y\end{array} \right]}.
$$

Notice that, for example, the vector $\mathbf b = [6,9]^T$ is in the image of the transformation $\mathbf{S}$ since there is another vector $\mathbf{u} = [1,1]^T$ such that $\mathbf{S}(\mathbf{u})=\mathbf{b}{:}$

$$
\mathbf{S} \bigg( \underbrace{ {\left[ \begin{array}{c}1 \\ 1\end{array} \right]} }_{\mathbf{u}} \bigg) = {\left[ \begin{array}{c}2 \cdot  1 + 4 \cdot  1 \\ 3 \cdot  1 + 6 \cdot  1\end{array} \right]}
	=\underbrace{ {\left[ \begin{array}{c}6 \\ 9\end{array} \right]}}_{\mathbf{b}}
$$



### example 17592186124356 — Determining a Component of a Vector in the Image of a Linear Transformation

Let $$
\displaystyle \mathbf{T}: {\left[ \begin{array}{c}x \\ y \\ z\end{array} \right]} \longrightarrow {\left[ \begin{array}{c}x + y \\ - x + y \\ 2 y\end{array} \right]}
$$ be a linear transformation. Determine the value of $k$ for which the vector $\mathbf{v}={\left[ \begin{array}{c}4 \\ k \\ 8\end{array} \right]}$ belongs to $\textrm{Im}(\mathbf{T}).$

The vector $\mathbf{v}$ belongs to $\textrm{Im}(\mathbf{T})$ if there exists a vector $\mathbf{u}={\left[ \begin{array}{c}x \\ y \\ z\end{array} \right]}$ such that $\mathbf{T}(\mathbf{u}) = \mathbf{v}.$ 

Therefore, we must have

$$
\begin{aligned}\begin{bmatrix}x+y \\ -x+y \\ 2y\end{bmatrix} & =\begin{bmatrix}4 \\ k \\ 8\end{bmatrix}.\end{aligned}
$$

This gives the following system of equations:

$$
\left\{\begin{aligned}x+y &=4 \\ -x+y &=k \\ 2y &=8.\end{aligned}\right.
$$

From the third equation, we get $y=4,$ which we substitute into the first equation to get 

$$
\begin{aligned}x+y & =4 \\ x+4 & =4 \\ x & =0.\end{aligned}
$$

Finally, we substitute $x=0$ and $y=4$ into the third equation and obtain

$$
\begin{aligned}-x+y & =k \\ 0+4 & =k \\ k & =4.\end{aligned}
$$

Therefore, $\mathbf{v}\in\textrm{Im}(\mathbf{T})$ when $k=4.$

### tutorial 17592186125819 — Determining If a Vector Lies in the Image

In general, the image of a linear transformation $$
\textrm{Im}(\mathbf{T}) = \textrm{Col}(T) = \textrm{Span}\{ \text{columns of T} \}.
$$ is equivalent to the column space of its standard matrix $T.$ That is,
$$
\textrm{Im}(\mathbf{T}) = \textrm{Col}(T) = \textrm{Span}\{ {\text{columns of } {T}} \}.
$$

So to find out if a vector $\mathbf{b}$ is in the image of the linear transformation $\mathbf{T},$ we just need to check if the matrix equation $T\mathbf{x}=\mathbf{b}$ is consistent.



### example 17592186124328 — Determining Whether a Vector Is in the Image of a Linear Transformation

The standard matrix $T$ of a linear transformation $\mathbf{T}$ and the vector $\mathbf{b} \in \mathbb{R}^3$ are given below. Determine if there exists a vector $\mathbf{x} \in \mathbb{R}^3$ such that $\mathbf{T}(\mathbf{x})=\mathbf{b}.$ In the affirmative case, find such a vector.

$$
T={\left[ \begin{array}{ccc}2 & 4 & 2 \\ 6 & 4 & - 10 \\ 0 & 4 & 8\end{array} \right]},
\qquad
\mathbf{b}={\left[ \begin{array}{c}6 \\ 26 \\ - 4\end{array} \right]}
$$

Since $T$ is the standard matix of $\mathbf{T},$ we have $\textrm{Im}(\mathbf{T}) = \textrm{Col}(T).$ In order to determine whether $\mathbf{b}$ lies in $\textrm{Im}(\mathbf{T}),$ we need to check if the equation $T\mathbf{x}=\mathbf{b}$ is consistent. 

So, we find the row echelon form of the augmented matrix $[T \,|\, \mathbf{b}],$ as follows: 

$$
\begin{aligned}[T\,|\,b] & =\left[\begin{array}{ccc|c}2 & 4 & 2 & 6 \\ 6 & 4 & -10 & 26 \\ 0 & 4 & 8 & -4\end{array}\right] &  & \begin{aligned}{R}_{2}:={R}_{2}+(-3){R}_{1}\end{aligned} \\  & ∼\left[\begin{array}{ccc|c}2 & 4 & 2 & 6 \\ 0 & -8 & -16 & 8 \\ 0 & 4 & 8 & -4\end{array}\right] &  & \begin{aligned}{R}_{3}:={R}_{3}+\frac{1}{2}{R}_{2}\end{aligned} \\  & ∼\left[\begin{array}{ccc|c}2 & 4 & 2 & 6 \\ 0 & -8 & -16 & 8 \\ 0 & 0 & 0 & 0\end{array}\right]\end{aligned}
$$

The reduced matrix above has a zero row, and so the system is consistent. We have two pivot columns (the $1$st and the $2$nd). So, $x_3$ is a free variable. 
Now, from the second equation, we get 

$$
-8x_2-16x_3 = 8
\qquad\Longrightarrow\qquad
x_2=-1-2x_3.
$$

Substituting this into the first equation gives 

$$
2x_1+4(-1-2x_3)+2x_3 = 6
\qquad\Longrightarrow\qquad
x_1=5+3x_3.
$$

As a result, the general solution is given by 
$$
{\left[ \begin{array}{c}5 + 3 {x}_{3} \\ - 1 - 2 {x}_{3} \\ {x}_{3}\end{array} \right]}, \qquad x_3 \in \mathbb{R}.
$$

Setting $x_3=0,$ we have
$$
\mathbf{x}={\left[ \begin{array}{c}5 \\ - 1 \\ 0\end{array} \right]}.
$$

### tutorial 17592186125821 — The Rank of a Linear Transformation

In general, the rank of a linear transformation $\mathbf{T}$ is equal to the dimension of its image:

$$
\text{rank}(\mathbf{T}) = \text{dim}(\text{Im}(\mathbf{T}))
$$

If the linear transformation $\mathbf{T}$ has the standard matrix $T,$ then the dimension of the image is equal to the rank of $T{:}$

$$
\text{dim}(\text{Im}(\mathbf{T})) = \text{rank}(T)
$$

So, in general, we have

$$
\text{rank}(\mathbf{T}) = \text{rank}(T).
$$



### example 17592186124329 — Calculating the Rank of a Linear Transformation

If $$
\displaystyle T={\left[ \begin{array}{cccc}2 & - 3 & - 1 & - 2 \\ - 6 & 5 & - 1 & 2 \\ 4 & 1 & 5 & 3 \\ 0 & 0 & 0 & 0\end{array} \right]}
$$ is the standard matrix of the linear transformation $\mathbf{T},$ then what is $\text{rank}(\mathbf{T})?$

In general, $\text{rank}(\mathbf{T}) = \text{dim}(\text{Im}(\mathbf{T})) = \text{rank}(T).$ 

So, we need to find the rank of the matrix $T.$ We reduce $T$ to row echelon form, as follows:

$$
\begin{aligned}T & =\begin{bmatrix}2 & -3 & -1 & -2 \\ -6 & 5 & -1 & 2 \\ 4 & 1 & 5 & 3 \\ 0 & 0 & 0 & 0\end{bmatrix} &  & \begin{aligned}{R}_{2}:={R}_{2}+3{R}_{1} \\ {R}_{3}:={R}_{3}+(-2){R}_{1}\end{aligned} \\  & ∼\begin{bmatrix}2 & -3 & -1 & -2 \\ 0 & -4 & -4 & -4 \\ 0 & 7 & 7 & 7 \\ 0 & 0 & 0 & 0\end{bmatrix} &  & \begin{aligned}{R}_{3}:={R}_{3}+\frac{7}{4}{R}_{2}\end{aligned} \\  & ∼\begin{bmatrix}2 & -3 & -1 & -2 \\ 0 & -4 & -4 & -4 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

Therefore, since $T$ has $2$ pivot columns, we have that 

$$
\textrm{rank}(\mathbf{T})=\textrm{rank}(T)=2.
$$

## Representative practice (first three per skill; full bank in practice.json)

### Determining a Component of a Vector in the Image of a Linear Transformation (9 captured questions)

Question 17592186125132 — question.difficulty/easy

Let $T:\begin{bmatrix}x \\ y \\ z\end{bmatrix}⟶\begin{bmatrix}-2x+y \\ -x+4y \\ -3x-5y\end{bmatrix}$ be a linear transformation. Determine the value of $k$ for which the vector $v=\begin{bmatrix}6 \\ -4 \\ k\end{bmatrix}$ belongs to $\text{Im}(T).$

Solution: The vector $v$ belongs to $\text{Im}(T)$ if there exists a vector $u=\begin{bmatrix}x \\ y \\ z\end{bmatrix}$ such that $T(u)=v.$ 

Therefore, we must have

$$
\begin{aligned}\begin{bmatrix}-2x+y \\ -x+4y \\ -3x-5y\end{bmatrix} & =\begin{bmatrix}6 \\ -4 \\ k\end{bmatrix}.\end{aligned}
$$

This gives the following system of equations:

$$
\left\{\begin{aligned}-2x+y &=6 \\ -x+4y &=-4 \\ -3x-5y &=k.\end{aligned}\right.
$$

From the second equation, we get $x=4+4y$, which we substitute into the first equation to get 

$$
\begin{aligned}-2x+y & =6 \\ -2(4+4y)+y & =6 \\ -7y & =14 \\ y & =-2.\end{aligned}
$$

Hence, 

$$
\begin{aligned}x & =4+4y \\  & =4+4(-2) \\  & =-4.\end{aligned}
$$

Finally, we substitute $x=-4$ and $y=-2$ into the third equation and obtain 

$$
\begin{aligned}-3x-5y & =k \\ -3(-4)-5(-2) & =k \\ k & =22.\end{aligned}
$$

Therefore, $v\in \text{Im}(T)$ when $k=22.$

Answer selection: 22

Question 17592186125133 — question.difficulty/moderate

Let $T=\begin{bmatrix}3 & -8 & 0 \\ 2 & -4 & 0 \\ -2 & 10 & 0\end{bmatrix}$ be the standard matrix of the linear transformation $T.$ Determine the value of $k$ for which the vector $v=\begin{bmatrix}6 \\ 8 \\ k\end{bmatrix}$ belongs to $\text{Im}(T).$

Solution: The vector $v$ belongs to $\text{Im}(T)$ if there exists a vector $u=\begin{bmatrix}x \\ y \\ z\end{bmatrix}$ such that $T(u)=v.$

Therefore, we must have

$$
\begin{aligned}T\cdot u & =v \\ \begin{bmatrix}3 & -8 & 0 \\ 2 & -4 & 0 \\ -2 & 10 & 0\end{bmatrix}\begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}6 \\ 8 \\ k\end{bmatrix} \\ \begin{bmatrix}3x-8y \\ 2x-4y \\ -2x+10y\end{bmatrix} & =\begin{bmatrix}6 \\ 8 \\ k\end{bmatrix}\end{aligned}
$$

This gives the following system of equations:

$$
\left\{\begin{aligned}3x-8y &=6 \\ 2x-4y &=8 \\ -2x+10y &=k.\end{aligned}\right.
$$

From the second equation, we get $x=4+2y$, which we substitute into the first equation to get 

$$
\begin{aligned}3x-8y & =6 \\ 3(4+2y)-8y & =6 \\ -2y & =-6 \\ y & =3.\end{aligned}
$$

Hence, 

$$
\begin{aligned}x & =4+2y \\  & =4+2(3) \\  & =10.\end{aligned}
$$

Finally, we substitute $x=10$ and $y=3$ into the third equation and obtain

$$
\begin{aligned}-2x+10y & =k \\ -2(10)+10(3) & =k \\ k & =10.\end{aligned}
$$

Therefore, $v\in \text{Im}(T)$ when $k=10.$

Answer selection: 10

Question 17592186272018 — question.difficulty/moderate

Let $T=\begin{bmatrix}2 & -4 & 0 \\ 1 & -3 & 0 \\ -1 & 4 & 0\end{bmatrix}$ be the standard matrix of the linear transformation $T.$ Determine the value of $k$ for which the vector $v=\begin{bmatrix}2 \\ 7 \\ k\end{bmatrix}$  belongs to $\text{Im}(T).$

Solution: The vector $v$ belongs to $\text{Im}(T)$ if there exists a vector $u=\begin{bmatrix}x \\ y \\ z\end{bmatrix}$ such that $T(u)=v.$

Therefore, we must have

$$
\begin{aligned}T\cdot u & =v \\ \begin{bmatrix}2 & -4 & 0 \\ 1 & -3 & 0 \\ -1 & 4 & 0\end{bmatrix}\begin{bmatrix}x \\ y \\ z\end{bmatrix} & =\begin{bmatrix}2 \\ 7 \\ k\end{bmatrix} \\ \begin{bmatrix}2x-4y \\ x-3y \\ -x+4y\end{bmatrix} & =\begin{bmatrix}2 \\ 7 \\ k\end{bmatrix}\end{aligned}
$$

This gives the following system of equations:

$$
\left\{\begin{aligned}2x-4y &=2 \\ x-3y &=7 \\ -x+4y &=k.\end{aligned}\right.
$$

From the second equation, we get $x=7+3y$, which we substitute into the first equation to get 

$$
\begin{aligned}2x-4y & =2 \\ 2(7+3y)-4y & =2 \\ 2y & =-12 \\ y & =-6.\end{aligned}
$$

Hence, 

$$
\begin{aligned}x & =7+3y \\  & =7+3(-6) \\  & =-11.\end{aligned}
$$

Finally, we substitute $x=-11$ and $y=-6$ into the third equation and obtain

$$
\begin{aligned}-x+4y & =k \\ -(-11)+4(-6) & =k \\ k & =-13.\end{aligned}
$$

Therefore, $v\in \text{Im}(T)$ when $k=-13.$

Answer selection: -13

### Determining Whether a Vector Is in the Image of a Linear Transformation (12 captured questions)

Question 17592186125115 — question.difficulty/moderate

The standard matrix $T$ of a linear transformation $T$ and the vector $b\in {R}^{3}$ are given below. Determine if there exists a vector $x\in {R}^{3}$ such that $T(x)=b.$
In the affirmative case, find the value of ${x}_{1}+{x}_{2},$ where ${x}_{1},{x}_{2},{x}_{3}$ are the components of $x.$  

$$
T=\begin{bmatrix}-2 & -5 & 3 \\ 4 & -1 & 5 \\ 0 & 3 & -3\end{bmatrix},\,b=\begin{bmatrix}9 \\ -7 \\ -3\end{bmatrix}
$$

Solution: Since $T$ is the standard matix of $T,$ we have $\text{Im}(T)=\text{Col}(T).$ In order to determine whether $b$ lies in $\text{Im}(T),$ we need to check if the equation $Tx=b$ is consistent. 

So, we find the row echelon form of the augmented matrix $[T\,|\,b],$ as follows: 

$$
\begin{aligned}[T\,|\,b] & =\left[\begin{array}{ccc|c}-2 & -5 & 3 & 9 \\ 4 & -1 & 5 & -7 \\ 0 & 3 & -3 & -3\end{array}\right] &  & \begin{aligned}{R}_{2}:={R}_{2}+2{R}_{1}\end{aligned} \\  & ∼\left[\begin{array}{ccc|c}-2 & -5 & 3 & 9 \\ 0 & -11 & 11 & 11 \\ 0 & 3 & -3 & -3\end{array}\right] &  & \begin{aligned}{R}_{3}:={R}_{3}+\frac{3}{11}{R}_{2}\end{aligned} \\  & ∼\left[\begin{array}{ccc|c}-2 & -5 & 3 & 9 \\ 0 & -11 & 11 & 11 \\ 0 & 0 & 0 & 0\end{array}\right]\end{aligned}
$$

The reduced matrix above has two pivot columns (the $1$st and the $2$nd). Hence, ${x}_{3}$ is a free variable. 
Now, from the second equation, we get 

$$
-11{x}_{2}+11{x}_{3}=11\,⟹\,{x}_{2}=-1+{x}_{3}.
$$

Substituting this into the first equation gives 

$$
-2{x}_{1}-5(-1+{x}_{3})+3{x}_{3}=9\,⟹\,{x}_{1}=-2-{x}_{3}.
$$

As a result, the general solution is given by 

$$
\begin{bmatrix}-2-{x}_{3} \\ -1+{x}_{3} \\ {x}_{3}\end{bmatrix},\,{x}_{3}\in R.
$$

Setting ${x}_{3}=0,$ we have

$$
x=\begin{bmatrix}-2 \\ -1 \\ 0\end{bmatrix},
$$

where $T(x)=b.$

Finally, ${x}_{1}+{x}_{2}=-2-1=-3.$

Answer selection: -3

Question 17592186125117 — question.difficulty/hard

The linear transformation $T$ and the vector $b\in {R}^{4}$ are given below. Determine if there exists a vector $x\in {R}^{4}$ such that $T(x)=b.$
In the affirmative case, find the value of ${x}_{1}-{x}_{3},$ where ${x}_{1},{x}_{2},{x}_{3},{x}_{4}$ are the components of $x.$  

$$
T:\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3} \\ {x}_{4}\end{bmatrix}⟶\begin{bmatrix}{x}_{1}+{x}_{2}-{x}_{4} \\ 2{x}_{2}-{x}_{1}+3{x}_{3}+4{x}_{4} \\ 2{x}_{1}+{x}_{2}-{x}_{3}-3{x}_{4} \\ 0\end{bmatrix},\,b=\begin{bmatrix}3 \\ 6 \\ -3 \\ 0\end{bmatrix}
$$

Solution: First, we write down the standard matrix of $T:$

$$
T=\begin{bmatrix}1 & 1 & 0 & -1 \\ -1 & 2 & 3 & 4 \\ 2 & 1 & -1 & -3 \\ 0 & 0 & 0 & 0\end{bmatrix}
$$

Since $T$ is the standard matix of $T,$ we have $\text{Im}(T)=\text{Col}(T).$ In order to determine whether $b$ lies in $\text{Im}(T),$ we need to check if the equation $Tx=b$ is consistent. 

So, let's find the row echelon form of the augmented matrix $[T\,|\,b]$ as follows: 

$$
\begin{aligned}[T\,|\,b] & =\left[\begin{array}{cccc|c}1 & 1 & 0 & -1 & 3 \\ -1 & 2 & 3 & 4 & 6 \\ 2 & 1 & -1 & -3 & -3 \\ 0 & 0 & 0 & 0 & 0\end{array}\right] &  & \begin{aligned}{R}_{2}:={R}_{2}+{R}_{1} \\ {R}_{3}:={R}_{3}+(-2){R}_{1}\end{aligned} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & 0 & -1 & 3 \\ 0 & 3 & 3 & 3 & 9 \\ 0 & -1 & -1 & -1 & -9 \\ 0 & 0 & 0 & 0 & 0\end{array}\right] &  & \begin{aligned}{R}_{3}={R}_{3}+\frac{1}{3}{R}_{2}\end{aligned} \\  & ∼\left[\begin{array}{cccc|c}1 & 1 & 0 & -1 & 3 \\ 0 & 3 & 3 & 3 & 9 \\ 0 & 0 & 0 & 0 & -6 \\ 0 & 0 & 0 & 0 & 0\end{array}\right]\end{aligned}
$$

From the third equation, we get the false statement $0=-6.$ Therefore, the system is inconsistent, and we conclude that  $b\notin \text{Im}(T).$

Answer selection: b\notin \text{Im}(T)

Question 17592186272019 — question.difficulty/hard

The linear transformation $T$ and the vector $b\in {R}^{4}$ are given below. Determine if there exists a vector $x\in {R}^{4}$ such that $T(x)=b.$
In the affirmative case, find the value of ${x}_{1}-{x}_{3},$ where ${x}_{1},{x}_{2},{x}_{3},{x}_{4}$ are the components of $x.$  

$$
T:\begin{bmatrix}{x}_{1} \\ {x}_{2} \\ {x}_{3} \\ {x}_{4}\end{bmatrix}⟶\begin{bmatrix}{x}_{1}+2{x}_{2}+{x}_{3}-{x}_{4} \\ -{x}_{2}+2{x}_{3}+{x}_{4} \\ 2{x}_{1}-{x}_{2}+{x}_{3}+{x}_{4} \\ -11{x}_{3}-2{x}_{4}\end{bmatrix},\,b=\begin{bmatrix}1 \\ -2 \\ 3 \\ 5\end{bmatrix}
$$

Solution: First, we write down the standard matrix of $T:$

$$
T=\begin{bmatrix}1 & 2 & 1 & -1 \\ 0 & -1 & 2 & 1 \\ 2 & -1 & 1 & 1 \\ 0 & 0 & -11 & -2\end{bmatrix}
$$

Since $T$ is the standard matix of $T,$ we have $\text{Im}(T)=\text{Col}(T).$ In order to determine whether $b$ lies in $\text{Im}(T),$ we need to check if the equation $Tx=b$ is consistent. 

So, let's find the row echelon form of the augmented matrix $[T\,|\,b]$ as follows: 

$$
\begin{aligned}[T\,|\,b] & =\left[\begin{array}{cccc|c}1 & 2 & 1 & -1 & 1 \\ 0 & -1 & 2 & 1 & -2 \\ 2 & -1 & 1 & 1 & 3 \\ 0 & 0 & -11 & -2 & 5\end{array}\right] &  & \begin{aligned}{R}_{3}:={R}_{3}+(-2){R}_{1}\end{aligned} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & 1 & -1 & 1 \\ 0 & -1 & 2 & 1 & -2 \\ 0 & -5 & -1 & 3 & 1 \\ 0 & 0 & -11 & -2 & 5\end{array}\right] &  & \begin{aligned}{R}_{3}:={R}_{3}+(-5){R}_{1}\end{aligned} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & 1 & -1 & 1 \\ 0 & -1 & 2 & 1 & -2 \\ 0 & 0 & -11 & -2 & 11 \\ 0 & 0 & -11 & -2 & 5\end{array}\right] &  & \begin{aligned}{R}_{4}:={R}_{4}+(-1){R}_{3}\end{aligned} \\  & ∼\left[\begin{array}{cccc|c}1 & 2 & 1 & -1 & 1 \\ 0 & -1 & 2 & 1 & -2 \\ 0 & 0 & -11 & -2 & 11 \\ 0 & 0 & 0 & 0 & -6\end{array}\right]\end{aligned}
$$

From the third equation, we get the false statement $0=-6.$ Therefore, the system is inconsistent, and we conclude that  $b\notin \text{Im}(T).$

Answer selection: b\notin \text{Im}(T)

### Calculating the Rank of a Linear Transformation (11 captured questions)

Question 17592186125116 — question.difficulty/easy

If $T=\begin{bmatrix}2 & -1 & 1 \\ -4 & 2 & -2 \\ 6 & -3 & 3\end{bmatrix}$ is the standard matrix of the linear transformation $T$, then $\text{rank}(T)=$

Solution: Recall that $\text{rank}(T)=\text{dim}(\text{Im}(T))=\text{rank}(T).$ 

So, we need to find the rank of the matrix $T.$ We reduce $T$ to row echelon form, as follows:

$$
\begin{aligned}T & =\begin{bmatrix}2 & -1 & 1 \\ -4 & 2 & -2 \\ 6 & -3 & 3\end{bmatrix} &  & \begin{aligned}{R}_{2}:={R}_{2}+2{R}_{1} \\ {R}_{3}:={R}_{3}+(-3){R}_{1}\end{aligned} \\  & ∼\begin{bmatrix}2 & -1 & 1 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

Therefore, since $T$ has $1$ pivot column, we have that 

$$
\text{rank}(T)=\text{rank}(T)=1.
$$

Answer selection: 1

Question 17592186125150 — question.difficulty/moderate

Given the transformation $T:\begin{bmatrix}x \\ y \\ z\end{bmatrix}⟶\begin{bmatrix}x+2y \\ y-x+6z \\ 8z-x+3y\end{bmatrix},$ find its rank.

Solution: First, the standard matrix of $T$ is given by

$$
T=\begin{bmatrix}1 & 2 & 0 \\ -1 & 1 & 6 \\ -1 & 3 & 8\end{bmatrix}.
$$

Recall that $\text{rank}(T)=\text{dim}(\text{Im}(T))=\text{rank}(T).$ 

So, we need to find the rank of the matrix $T.$ We reduce $T$ to row echelon form, as follows:

$$
\begin{aligned}T & =\begin{bmatrix}1 & 2 & 0 \\ -1 & 1 & 6 \\ -1 & 3 & 8\end{bmatrix} &  & \begin{aligned}{R}_{2}:={R}_{2}+{R}_{1} \\ {R}_{3}:={R}_{3}+{R}_{1}\end{aligned} \\  & ∼\begin{bmatrix}1 & 2 & 0 \\ 0 & 3 & 6 \\ 0 & 5 & 8\end{bmatrix} &  & \begin{aligned}{R}_{3}:={R}_{3}+\left(-\frac{5}{3}\right){R}_{2}\end{aligned} \\  & ∼\begin{bmatrix}1 & 2 & 0 \\ 0 & 3 & 6 \\ 0 & 0 & -2\end{bmatrix}\end{aligned}
$$

Therefore, since $T$ has $3$ pivot columns, we have that 

$$
\text{rank}(T)=\text{rank}(T)=3.
$$

Answer selection: 3

Question 17592186323958 — question.difficulty/easy

If $T=\begin{bmatrix}1 & 3 & -4 \\ 0 & 14 & -14 \\ 2 & 3 & -5\end{bmatrix}$ is the standard matrix of the linear transformation $T$, then $\text{rank}(T)=$

Solution: Recall that $\text{rank}(T)=\text{dim}(\text{Im}(T))=\text{rank}(T).$ 

So, we need to find the rank of the matrix $T.$ We reduce $T$ to row echelon form, as follows:

$$
\begin{aligned}T & =\begin{bmatrix}1 & 3 & -4 \\ 0 & 14 & -14 \\ 2 & 3 & -5\end{bmatrix} &  & \begin{aligned}{R}_{3}:={R}_{3}+(-2){R}_{1}\end{aligned} \\  & ∼\begin{bmatrix}1 & 3 & -4 \\ 0 & 14 & -14 \\ 0 & -3 & 3\end{bmatrix} &  & \begin{aligned}{R}_{3}:={R}_{3}+\frac{3}{14}{R}_{2}\end{aligned} \\  & ∼\begin{bmatrix}1 & 3 & -4 \\ 0 & 14 & -14 \\ 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

Therefore, since $T$ has $2$ pivot columns, we have that 

$$
\text{rank}(T)=\text{rank}(T)=2.
$$

Answer selection: 2
