# 17592186048978 The Rank-Nullity Theorem

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186185320 — Introduction

When we reduce a matrix to row echelon form, the number of *pivot* columns plus the number of *non-pivot* columns always equals the total number of columns of the matrix. 

By translating this into the language of vector spaces, we get the **rank-nullity theorem**. The rank-nullity theorem relates the rank of a matrix to the dimension of its null space:

*Let $A$ be a matrix (not necessarily square) with $n$ columns. Then,*

$$
\textrm{dim(Col}(A)) + \textrm{dim(Null}(A)) = \textrm{dim}(\mathbb{R}^n),
$$

*or, equivalently,*

$$
\textrm{rank}(A) + \textrm{nullity}(A) = n.
$$

For example, suppose that for some matrix $A,$ we have



$$
\textrm{Null}(A)= \left\{ \left. \begin{bmatrix}-2{x}_{2} \\ {x}_{2} \\ 2{x}_{3} \\ {x}_{2}-{x}_{3}\end{bmatrix} \:\right|\: \, x_2,x_3\in\mathbb{R} \right\}.
$$



We can use the rank-nullity theorem to calculate $\textrm{rank}(A).$

In this case, we must have $n=4,$ since this is the number of components in each of the vectors of the null space. 

Also, we must have $\textrm{nullity}(A)=2,$ since 


$$
\textrm{Null}(A)= \left\{ \left. x_2 \begin{bmatrix}-2 \\ 1 \\ 0 \\ 1\end{bmatrix} + x_3 \begin{bmatrix}0 \\ 0 \\ 2 \\ -1\end{bmatrix} \:\right|\: \, x_2,x_3\in\mathbb{R} \right\}.
$$



Therefore, using the rank-nullity theorem, we have

$$
\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ \text{rank}(A)+2 & =4 \\ \text{rank}(A) & =4-2 \\  & =2.\end{aligned}
$$



### example 17592186184124 — Finding the Rank or Nullity of a Matrix Using the Rank-Nullity Theorem

Consider a $8 \times 6$ matrix $A.$ If $\textrm{rank}(A)=5$ then what is $\textrm{nullity}(A)?$

According to the rank-nullity theorem, if $A$ is a matrix with $n$ columns, then  

$$
\textrm{rank}(A) + \textrm{nullity}(A) = n.
$$

For the given matrix, we have $n=6.$ Therefore,

$$
\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ 5+\text{nullity}(A) & =6 \\ \text{nullity}(A) & =6-5 \\  & =1.\end{aligned}
$$

### example 17592186184070 — Finding the Rank or Nullity of a Matrix Given a Description of the Column or Null Space

Let $A$ be a $3\times 5$ matrix. If $\mathcal{B}= \{\mathbf{b_1}, \mathbf{b_2}, \mathbf{b_3}\}$ is a basis of $\textrm{Col}(A)$, find $\textrm{dim(Null}(A)).$

According to the rank-nullity theorem, if $A$ is a matrix with $n$ columns, then 

$$
\textrm{rank}(A) + \textrm{nullity}(A) = n.
$$

For the given matrix, we have $n=5,$ and since $\mathcal{B}$ is formed by $3$ vectors, $\textrm{rank}(A) = 3.$ Therefore,

$$
\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ 3+\text{nullity}(A) & =5 \\ \text{nullity}(A) & =5-3 \\ \text{dim(Null}(A)) & =2.\end{aligned}
$$

### example 17592186184071 — Identifying True Statements Using the Invertible Matrix Theorem and the Rank-Nullity Theorem

Which of the following statements are true given that $A$ is a $3 \times 3$ matrix, and  

$$
\textrm{Null}(A) = \left\{ \left. \begin{bmatrix}{x}_{1} \\ 0 \\ -2{x}_{3}\end{bmatrix}\;\right| \;x_1, x_3 \in\mathbb{R} \right\}?
$$

 

I. $\textrm{rank}(A)=1$

II. $A$ is invertible

III. $\textrm{Col}(A)$ is a $2$-dimensional subspace of $\Bbb R^3$

Since $A$ is a $3 \times 3$ matrix, the invertible matrix theorem states the following:



$$
A \textrm{ is invertible} \qquad \Leftrightarrow \qquad \left\{\; \begin{aligned} & \text{Col}(A)={\mathbb{R}}^{3} \\ & \text{dim(Col}(A))=3=\text{rank}(A) \\ & \text{Null}(A)=\{\mathbf{0}\} \\ & \text{dim(Null}(A))=0=\text{nullity}(A)\end{aligned} \right.
$$



Also, according to the rank-nullity theorem, if $A$ is a matrix with $n$ columns, then 

$$
\textrm{rank}(A) + \textrm{nullity}(A) = n.
$$

With that in mind, let's examine each statement in turn.

- Statement I is true. Indeed, we have that 


$$
\textrm{Null}(A) = \textrm{Span}\left\{ {\begin{bmatrix}1 \\ 0 \\ 0\end{bmatrix}, \;\begin{bmatrix}0 \\ 0 \\ -2\end{bmatrix} }\right\}
$$

 
which means that $\textrm{nullity}(A) =2.$

Now,  for the matrix $A,$ the number of columns is $n = 3,$ so according to the rank-nullity theorem, we obtain

$$
\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ \text{rank}(A)+2 & =3 \\ \text{rank}(A) & =3-2 \\  & =1.\end{aligned}
$$

- Statement II is false. Since $\textrm{nullity}(A) = 2 \neq 0,$ then by the invertible matrix theorem, $A$ cannot be an invertible matrix.

- Statement III is false. Since $\textrm{rank}(A) = 1,$ we have that $\textrm{Col}(A)$ is a $1$-dimensional subspace of $\Bbb R^3.$

Therefore, the correct answer is "I only."

## Representative practice (first three per skill; full bank in practice.json)

### Finding the Rank or Nullity of a Matrix Using the Rank-Nullity Theorem (19 captured questions)

Question 17592186184754 — question.difficulty/easy

Consider a $5\times 8$ matrix $A.$ If $\text{dim(Null(}A))=3,$ then $\text{rank}(A)=$

Solution: According to the rank-nullity theorem, if $A$ is a matrix with $n$ columns, then 

$$
\text{rank}(A)+\text{nullity}(A)=n.
$$

For the given matrix, we have $n=8.$ Therefore,

$$
\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ \text{rank}(A)+3 & =8 \\ \text{rank}(A) & =8-3 \\  & =5.\end{aligned}
$$

Answer selection: 5

Question 17592186184756 — question.difficulty/easy

Consider a $6\times 7$ matrix $A.$ If $\text{rank}(A)=5$ then $\text{nullity}(A)=$

Solution: According to the rank-nullity theorem, if $A$ is a matrix with $n$ columns, then 

$$
\text{rank}(A)+\text{nullity}(A)=n.
$$

For the given matrix, we have $n=7.$ Therefore,

$$
\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ 5+\text{nullity}(A) & =7 \\ \text{nullity}(A) & =7-5 \\  & =2.\end{aligned}
$$

Answer selection: 2

Question 17592186272243 — question.difficulty/easy

Consider a $8\times 7$ matrix $A.$ If $\text{dim(Null(}A))=2,$ then $\text{rank}(A)=$

Solution: According to the rank-nullity theorem, if $A$ is a matrix with $n$ columns, then 

$$
\text{rank}(A)+\text{nullity}(A)=n.
$$

For the given matrix, we have $n=7.$ Therefore,

$$
\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =7 \\ \text{rank}(A)+2 & =7 \\ \text{rank}(A) & =7-2 \\  & =5.\end{aligned}
$$

Answer selection: 5

### Finding the Rank or Nullity of a Matrix Given a Description of the Column or Null Space (20 captured questions)

Question 17592186184759 — question.difficulty/moderate

Find $\text{rank}(A)$ given that $$
\displaystyle \text{Null}(A)=\left\{\begin{bmatrix}2{x}_{2} \\ {x}_{2} \\ {x}_{3} \\ {x}_{2}+{x}_{3}\end{bmatrix}\right.\,|\,\,{x}_{2},{x}_{3}\in R\}.
$$

Solution: According to the rank-nullity theorem, if $A$ is a matrix with $n$ columns, then 

$$
\text{rank}(A)+\text{nullity}(A)=n.
$$

For the given matrix, we have $n=4,$ since this is the number of components in each of the vectors of the null space. 

Also, since 

$$
\text{Null}(A)=\{{x}_{2}\begin{bmatrix}2 \\ 1 \\ 0 \\ 1\end{bmatrix}+{x}_{3}\begin{bmatrix}0 \\ 0 \\ 1 \\ 1\end{bmatrix}\,|\,\,{x}_{2},{x}_{3}\in R\}
$$

we conclude that $\text{nullity}(A)=2.$

Therefore,

$$
\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ \text{rank}(A)+2 & =4 \\ \text{rank}(A) & =4-2 \\  & =2.\end{aligned}
$$

Answer selection: 2

Question 17592186184760 — question.difficulty/easy

Let $A$ be a $3\times 6$ matrix. If $B=\{{b}_{1},{b}_{2},{b}_{3}\}$ is a basis of $\text{Col}(A)$, find $\text{dim(Null}(A)).$

Solution: According to the rank-nullity theorem, if $A$ is a matrix with $n$ columns, then 

$$
\text{rank}(A)+\text{nullity}(A)=n.
$$

For the given matrix, we have $n=6,$ and since $B$ is formed by $3$ vectors, $\text{rank}(A)=3.$ Therefore,

$$
\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ 3+\text{nullity}(A) & =6 \\ \text{nullity}(A) & =6-3 \\ \text{dim(Null}(A)) & =3.\end{aligned}
$$

Answer selection: 3

Question 17592186272246 — question.difficulty/easy

Let $A$ be a $5\times 7$ matrix. If $B=\{{b}_{1},{b}_{2},{b}_{3},{b}_{4}\}$ is a basis of $\text{Col}(A)$, find $\text{dim(Null}(A)).$

Solution: According to the rank-nullity theorem, if $A$ is a matrix with $n$ columns, then 

$$
\text{rank}(A)+\text{nullity}(A)=n.
$$

For the given matrix, we have $n=7,$ and since $B$ is formed by $4$ vectors, $\text{rank}(A)=4.$ Therefore,

$$
\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ 4+\text{nullity}(A) & =7 \\ \text{nullity}(A) & =7-4 \\ \text{dim(Null}(A)) & =3.\end{aligned}
$$

Answer selection: 3

### Identifying True Statements Using the Invertible Matrix Theorem and the Rank-Nullity Theorem (20 captured questions)

Question 17592186184755 — question.difficulty/hard

Which of the following statements are true, given that $A$ is a $4\times 4$ matrix and 

$$
\text{Null}(A)=\text{Span}\left\{\begin{bmatrix}5 \\ -2 \\ 0 \\ 0\end{bmatrix},\,\begin{bmatrix}3 \\ 0 \\ 0 \\ -1\end{bmatrix}\right\}?
$$

I. The number of non-pivot columns in $A$ is equal to $3$

II. $\text{Col}(A)={R}^{4}$

III. $\text{rank}(A)=2$

Solution: Since $A$ is a $4\times 4$ matrix, the invertible matrix theorem states the following:

$A$ is invertible $$
\displaystyle \,⇔\,\left\{\begin{aligned}\text{Col}(A) &={R}^{4} \\ \text{dim(Col}(A)) &=4=\text{rank}(A) \\ \text{Null}(A) &=\{0\} \\ \text{dim(Null}(A)) &=0=\text{nullity}(A)\end{aligned}\right.
$$

Also, according to the rank-nullity theorem, if $A$ is a matrix with $n$ columns, then 

$$
\text{rank}(A)+\text{nullity}(A)=n.
$$

With that in mind, let's examine each statement in turn.

- Statement I is false. Since the generating vectors in 

$$
\text{Null}(A)=\text{Span}\left\{\begin{bmatrix}5 \\ -2 \\ 0 \\ 0\end{bmatrix},\,\begin{bmatrix}3 \\ 0 \\ 0 \\ -1\end{bmatrix}\right\}
$$

are linearly independent, we conclude that the number of non-pivot columns in $A$ is equal to $2.$

- Statement II is false. Since $\text{nullity}(A)=2\ne 0,$ then by the invertible matrix theorem, we have $\text{Col}(A)\ne {R}^{4}.$

- Statement III is true. Indeed, for the matrix $A,$ the number of columns is $n=4.$ Now, according to the rank-nullity theorem, we obtain

$$
\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ \text{rank}(A)+2 & =4 \\ \text{rank}(A) & =4-2 \\  & =2.\end{aligned}
$$

Therefore, the correct answer is "III only."

Answer selection: III only

Question 17592186184757 — question.difficulty/moderate

Which of the following statements are true given that $A$ is a $4\times 4$ matrix with $3$ pivot columns?

I. $\text{rank}(A)=3$

II. $A$ is invertible

III. $\text{nullity}(A)=1$

Solution: Since $A$ is a $4\times 4$ matrix, the invertible matrix theorem states the following:

$A$ is invertible $$
\displaystyle \,⇔\,\left\{\begin{aligned}\text{Col}(A) &={R}^{4} \\ \text{dim(Col}(A)) &=4=\text{rank}(A) \\ \text{Null}(A) &=\{0\} \\ \text{dim(Null}(A)) &=0=\text{nullity}(A)\end{aligned}\right.
$$

Also, according to the rank-nullity theorem, if $A$ is a matrix with $n$ columns, then 

$$
\text{rank}(A)+\text{nullity}(A)=n.
$$

With that in mind, let's examine each statement in turn.

- Statement I is true. Indeed, since $A$ has $3$ pivot columns, we have $\text{rank}(A)=3.$

- Statement II is false. For the matrix $A,$ the number of the columns is $n=4.$ Now, since $\text{rank}(A)\ne 4,$ then by the invertible matrix theorem, we have that $A$ is not invertible.

- Statement III is true. According to  the rank-nullity theorem, we obtain

$$
\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ 3+\text{nullity}(A) & =4 \\ \text{nullity}(A) & =4-3 \\  & =1.\end{aligned}
$$

Therefore, the correct answer is "I and III only."

Answer selection: I and III only

Question 17592186272354 — question.difficulty/moderate

Which of the following statements are true given that $A$ is a $7\times 7$ matrix which has only $3$ non-pivot column?

Select all that apply.

Solution: Since $A$ is a $7\times 7$ matrix, the invertible matrix theorem states the following:

$$
A\text{ is }\text{invertible}\quad\Longleftrightarrow\quad\left\{\begin{aligned}\operatorname{Col}(A) &=\mathbb{R}^{7} \\ \dim(\operatorname{Col}(A)) &=7=\operatorname{rank}(A) \\ \operatorname{Null}(A) &=\{0\} \\ \dim(\operatorname{Null}(A)) &=0=\operatorname{nullity}(A)\end{aligned}\right.
$$

Also, according to the rank-nullity theorem, if $A$ is a matrix with $n$ columns, then 

$$
\text{rank}(A)+\text{nullity}(A)=n.
$$

With that in mind, let's examine each statement in turn.

- Statement “$A$ is  **not** invertible” is true. Since $A$ has $n=7$ columns and $3$ of them is a non-pivot one, it follows that    

$$
\text{dim(Col}(A))=7-3=4\ne 7.
$$

 Thus,  according to the invertible matrix theorem $A$ is  **not** an invertible matrix.

- Statement “$\text{Col}(A)$ is a $4$-dimensional subspace of ${R}^{7}.$” is true.  Indeed, since $\text{dim(Col}(A))=\text{rank}(A)=4$,  then $\text{Col}(A)$ is a $4$-dimensional subspace of ${R}^{7}.$

- Statement $\text{nullity}(A)=1$ is false. Since $n=7$, according to  the rank-nullity theorem, we obtain

$$
\begin{aligned}\text{rank}(A)+\text{nullity}(A) & =n \\ 4+\text{nullity}(A) & =7 \\ \text{nullity}(A) & =7-4 \\  & =3.\end{aligned}
$$

Therefore, the correct answer is “$A$ is  **not** invertible”; “$\text{Col}(A)$ is a $4$-dimensional subspace of ${R}^{7}.$” only.

Answer $A$ is  **not** invertible: true

Answer $\text{Col}(A)$ is a $4$-dimensional subspace of ${\mathbb{R}}^{7}.$: true

Answer $\text{nullity}(A)=1$: false
