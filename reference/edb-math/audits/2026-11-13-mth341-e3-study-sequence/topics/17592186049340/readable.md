# 17592186049340 The Invertible Matrix Theorem in Terms of Dimension, Rank and Nullity

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186125780 — Introduction

Suppose we are given an $n \!\times\! n$ invertible matrix $A.$ Remember that if $A$ is invertible, then the equation $A\mathbf{x}=\mathbf{0}$ has only the trivial solution $\mathbf{x}=\mathbf{0}.$

Let's extract all possible information from this fact using the vector spaces related to the matrix, namely, the *column space* and the *null space*.

- The fact that the unique solution to $A\mathbf{x}=\mathbf{0}$ is $\mathbf{x}=\mathbf{0}$ tells us that 

$$
\textrm{Null}(A)=\{ \mathbf{0} \},
$$

 or alternatively, 

$$
\textrm{dim(Null}(A)) = \textrm{nullity}(A)=0.
$$

- Furthermore, if $\textrm{dim(Null}(A))=0$ then $A$ has no *non-pivot* columns, or equivalently, all the columns of $A$ are *pivot columns*. So 

$$
\textrm{dim(Col}(A))=\textrm{rank}(A)=n.
$$

- Finally, since $\textrm{Col}(A)$ is a subspace of $\mathbb{R}^n$ and its basis has $n$ linearly independent vectors, we can conclude that 

$$
\textrm{Col}(A)=\mathbb{R}^n.
$$

All the results mentioned above can be summarized in the following theorem, called the **invertible matrix theorem**:

*Let $A$ be an $n \!\times\! n$ matrix. Then we have the following equivalence:*


$$
A \textrm{ is invertible} \qquad \Leftrightarrow \qquad \left\{\; \begin{aligned} & \text{Col}(A)={\mathbb{R}}^{n} \\ & \text{dim(Col}(A))=n=\text{rank}(A) \\ & \text{Null}(A)=\{\mathbf{0}\} \\ & \text{dim(Null}(A))=0=\text{nullity}(A)\end{aligned} \right.
$$





### example 17592186124434 — Recognizing Parts of the Invertible Matrix Theorem



$$
A \textrm{ is invertible} \qquad \Leftrightarrow \qquad \left\{\; \begin{aligned} & \text{Col}(A)={\mathbb{R}}^{n} \\ & \text{dim(Col}(A))=n=\text{rank}(A) \\ & \text{Null}(A)=\{\mathbf{0}\} \\ & \bbox[2pt,border:2px solid Silver]{\bbox[white, 2pt]{\phantom{WWW}}}=0=\text{nullity}(A)\end{aligned} \right.
$$



Consider the equivalence above, where $A$ is an $n \!\times\! n$ matrix. What should be placed into the blank space to make a true statement?

Recall that the *invertible matrix theorem* states the following: 

*Let $A$ be an $n \!\times\! n$ matrix. Then we have the following equivalence:*


$$
A \textrm{ is invertible} \qquad \Leftrightarrow \qquad \left\{\; \begin{aligned} & \text{Col}(A)={\mathbb{R}}^{n} \\ & \text{dim(Col}(A))=n=\text{rank}(A) \\ & \text{Null}(A)=\{\mathbf{0}\} \\ & \bbox[2pt,border:2px solid Silver]{\bbox[white, 2pt]{{\color{blue}\text{dim(Null}(A))}}}=0=\text{nullity}(A)\end{aligned} \right.
$$



The missing expression is $\textrm{dim(Null}(A)).$

### example 17592186124320 — Identifying True Statements Using the Invertible Matrix Theorem

Which of the following statements are true, given that $A$ is a $4 \times 4$ matrix, and 


$$
\textrm{Null}(A) = \left\{ \left. \begin{bmatrix}{x}_{1} \\ 2{x}_{1} \\ 0 \\ -{x}_{1}\end{bmatrix} \;\right| \;x_1\in\mathbb{R} \right\}?
$$



I. $A$ is not invertible

II. $\textrm{Col}(A)=\mathbb{R}^4$

III. $\textrm{rank}(A)=4$

Since $A$ is a $4 \times 4$ matrix, the invertible matrix theorem states the following: 



$$
A \textrm{ is invertible} \qquad \Leftrightarrow \qquad \left\{\; \begin{aligned} & \text{Col}(A)={\mathbb{R}}^{4} \\ & \text{dim(Col}(A))=4=\text{rank}(A) \\ & \text{Null}(A)=\{\mathbf{0}\} \\ & \text{dim(Null}(A))=0=\text{nullity}(A)\end{aligned} \right.
$$



With that in mind, let's examine each statement in turn.

- Statement I is true. Since 


$$
\textrm{Null}(A) = \left\{ \left. x_1 \begin{bmatrix}1 \\ 2 \\ 0 \\ -1\end{bmatrix} \;\right| \;x_1\in\mathbb{R} \right\},
$$


we conclude that 

$$
\textrm{dim(Null}(A))=1 \neq 0.
$$

So,  according to the invertible matrix theorem, the matrix $A$ is not invertible.

- Statement II is false. Since the matrix $A$ is not invertible, then by the invertible matrix theorem, we must have $\textrm{Col}(A) \neq \mathbb{R}^4.$

- Statement III is false. Since $A$ is not invertible, then by the invertible matrix theorem, we must have $\textrm{rank}(A) \neq 4.$

Therefore, the correct answer is "I only."

### example 17592186124433 — Сompleting a Sentence Using the Invertible Matrix Theorem

Consider the following sentence:

*If $A$ is a $n\times n$ matrix and $\textrm{Null}(A) = \{\mathbf{ 0}\},$ then $\underline{\phantom{xxxxxx}}\,.$*

Which of the following can be placed into the blank space to make a true statement?

I. $\det(A) = 0$

II. $\textrm{rank}(A) = n$

III. $A$ has $n$ pivot columns

The invertible matrix theorem states the following:

$A$ is invertible 

$$
\qquad \Leftrightarrow \qquad \left\{\; \begin{aligned} & \text{Col}(A)={\mathbb{R}}^{n} \\ & \text{dim(Col}(A))=n=\text{rank}(A) \\ & \text{Null}(A)=\{\mathbf{0}\} \\ & \text{dim(Null}(A))=0=\text{nullity}(A)\end{aligned} \right.
$$



With that in mind, let's examine each of the options separately.

- The following statement is false:

$\qquad$ *If $A$ is a $n\times n$ matrix and $\textrm{Null}(A) = \{\mathbf{ 0}\},$ then $\det(A) = 0.$* $\:{\color{red}\times}$

Since $\textrm{Null}(A) = \{\mathbf{ 0}\},$ then according to the invertible matrix theorem, the matrix $A$ must be invertible, which means $\det(A) \ne 0.$

- The following statement is true:

$\qquad$ *If $A$ is a $n\times n$ matrix and $\textrm{Null}(A) = \{\mathbf{ 0}\},$ then $\textrm{rank}(A) = n.$* $\:{\color{green}\checkmark}$

Indeed, since $A$ is invertible, then according to the invertible matrix theorem, we have $\textrm{rank}(A)=n.$

- The following statement is true:

$\qquad$ *If $A$ is a $n\times n$ matrix and $\textrm{Null}(A) = \{\mathbf{ 0}\},$ then $A$ has $n$ pivot columns.* $\:{\color{green}\checkmark}$ 

Indeed, since $A$ is invertible, then according to the invertible matrix theorem, we have $\textrm{dim(Col}(A))=n,$ which means that $A$ has exactly $n$ pivot columns.

Therefore, the correct answer is "II and III only."

## Representative practice (first three per skill; full bank in practice.json)

### Recognizing Parts of the Invertible Matrix Theorem (21 captured questions)

Question 17592186124789 — question.difficulty/easy

$$
A\text{ is invertible}\,⇔\,\left\{\begin{aligned}\text{Col}(A) &={R}^{n} \\ \text{dim(Col}(A)) &=n=\text{rank}(A) \\ \text{Null}(A) &=\bbox[3pt,white,border: 2px solid Gainsboro]{\phantom{W}} \\ \text{dim(Null}(A)) &=0=\text{nullity}(A)\end{aligned}\right.
$$

Consider the equivalence above, where $A$ is an $n\,\times \,n$ matrix. Which of the following should be placed into the blank space to make a true statement?

Solution: Recall that the *invertible matrix theorem* states the following: 

*Let $A$ be an $n\,\times \,n$ matrix. Then we have the following equivalence:*

$$
A\text{ is invertible}\,⇔\,\left\{\begin{aligned}\text{Col}(A) &={R}^{n} \\ \text{dim(Col}(A)) &=n=\text{rank}(A) \\ \text{Null}(A) &=\{0\} \\ \text{dim(Null}(A)) &=0=\text{nullity}(A)\end{aligned}\right.
$$

Therefore, the missing expression is $\{0\}.$

Answer selection: \{\mathbf{0}\}

Question 17592186124791 — question.difficulty/easy

$$
A\text{ is }\text{invertible}\quad\Longleftrightarrow\quad\left\{\begin{aligned}\operatorname{Col}(A) &=\mathbb{R}^{n} \\ \underline{\phantom{\dim(\operatorname{Col}(A))}} &=n=\operatorname{rank}(A) \\ \operatorname{Null}(A) &=\{0\} \\ \dim(\operatorname{Null}(A)) &=0=\operatorname{nullity}(A)\end{aligned}\right.
$$

Consider the equivalence above, where $A$ is an $n\,\times \,n$ matrix. Which of the following should be placed into the blank space to make a true statement?

Use only expressions that refer directly to $A$; powers and inverses of $A$ are outside the requested form.

Solution: Recall that the *invertible matrix theorem* states the following: 

*Let $A$ be an $n\,\times \,n$ matrix. Then we have the following equivalence:*

$$
A\text{ is }\text{invertible}\quad\Longleftrightarrow\quad\left\{\begin{aligned}\operatorname{Col}(A) &=\mathbb{R}^{n} \\ {\color{blue}\dim(\operatorname{Col}(A))} &=n=\operatorname{rank}(A) \\ \operatorname{Null}(A) &=\{0\} \\ \dim(\operatorname{Null}(A)) &=0=\operatorname{nullity}(A)\end{aligned}\right.
$$

Therefore, the missing expression is $\text{dim(Col}(A)).$

Answer selection: \text{dim(Col}(A))

Question 17592186272237 — question.difficulty/easy

$$
A\text{ is }\text{invertible}\quad\Longleftrightarrow\quad\left\{\begin{aligned}\operatorname{Col}(A) &=\mathbb{R}^{n} \\ \dim(\operatorname{Col}(A)) &=\underline{\phantom{n}}=\operatorname{rank}(A) \\ \operatorname{Null}(A) &=\{0\} \\ \dim(\operatorname{Null}(A)) &=0=\operatorname{nullity}(A)\end{aligned}\right.
$$

Consider the equivalence above, where $A$ is an $n\,\times \,n$ matrix. Which of the following should be placed into the blank space to make a true statement?

Solution: Recall that the *invertible matrix theorem* states the following: 

*Let $A$ be an $n\,\times \,n$ matrix. Then we have the following equivalence:*

$$
A\text{ is }\text{invertible}\quad\Longleftrightarrow\quad\left\{\begin{aligned}\operatorname{Col}(A) &=\mathbb{R}^{n} \\ \dim(\operatorname{Col}(A)) &={\color{blue}n}=\operatorname{rank}(A) \\ \operatorname{Null}(A) &=\{0\} \\ \dim(\operatorname{Null}(A)) &=0=\operatorname{nullity}(A)\end{aligned}\right.
$$

Therefore, the missing expression is $n.$

Answer selection: n

### Identifying True Statements Using the Invertible Matrix Theorem (22 captured questions)

Question 17592186124863 — question.difficulty/moderate

Which of the following statements are true, given that $A$ is a $5\times 5$ matrix and 

$$
\text{Null}(A)=\left\{\begin{bmatrix}{x}_{1} \\ 3{x}_{1} \\ 0 \\ {x}_{1} \\ -2{x}_{1}\end{bmatrix}\right.\,|\,{x}_{1}\in R\}?
$$

Select all that apply.

Solution: Since $A$ is a $5\times 5$ matrix, the invertible matrix theorem states the following:

$A$ is invertible $$
\displaystyle \,⇔\,\left\{\begin{aligned}\text{Col}(A) &={R}^{5} \\ \text{dim(Col}(A)) &=5=\text{rank}(A) \\ \text{Null}(A) &=\{0\} \\ \text{dim(Null}(A)) &=0=\text{nullity}(A)\end{aligned}\right.
$$

With that in mind, let's examine each statement in turn.

- Statement $\text{dim(Null}(A))=0$ is false. Since 

$$
\text{Null}(A)=\{{x}_{1}\begin{bmatrix}1 \\ 3 \\ 0 \\ 1 \\ -2\end{bmatrix}\,|\,{x}_{1}\in R\}
$$

we conclude that 

$$
\text{dim(Null}(A))=1\ne 0.
$$

- Statement “$A$ is not invertible” is true. Since $\text{dim(Null}(A))\ne 0,$ then according to the invertible matrix theorem, the matrix $A$ can't be invertible.

- Statement $\text{rank}(A)=5$ is false. Since $A$ is not invertible, then by the invertible matrix theorem, we must have $\text{rank}(A)\ne 5.$

Therefore, the correct answer is “$A$ is not invertible” only.

Answer $A$ is not invertible: true

Answer $\text{dim(Null}(A))=0$: false

Answer $\text{rank}(A)=5$: false

Answer None of the above: false

Question 17592186124870 — question.difficulty/moderate

Which of the following statements are true, given that $A$ is a $6 \times 6$ matrix and $\text{Col}(A)={\mathbb{R}}^{6}$?

1. $A$ is not invertible
2. $\operatorname{rank} (A) = 6$
3. $\dim (\operatorname{Null}(A)) = 6$

Solution: Since $\operatorname{Col}(A)=\mathbb{R}^6$, the invertible matrix theorem gives $\operatorname{rank}(A)=6$, $A$ invertible, and $\dim(\operatorname{Null}(A))=0$.

Statement I is false, statement II is true, and statement III is false. Therefore, the correct answer is "II only."

Answer selection: II only

Question 17592186272238 — question.difficulty/moderate

Which of the following statements are true, given that $A$ is a $4\times 4$ matrix and $v=\begin{bmatrix}1 \\ 0 \\ -1 \\ 0\end{bmatrix}$ is a solution of the equation $Ax=0?$

Select all that apply.

Solution: Since $A$ is a $4\times 4$ matrix, the invertible matrix theorem states the following:

$$
A\text{ is }\text{invertible}\quad\Longleftrightarrow\quad\left\{\begin{aligned}\operatorname{Col}(A) &=\mathbb{R}^{4} \\ \dim(\operatorname{Col}(A)) &=4=\operatorname{rank}(A) \\ \operatorname{Null}(A) &=\{0\} \\ \dim(\operatorname{Null}(A)) &=0=\operatorname{nullity}(A)\end{aligned}\right.
$$ 

With that in mind, let's examine each statement in turn. 

- Statement $\text{Null}(A)=\{0\}$ is false. Since $v\ne 0$ and $Av=0,$ 
then $v\in \text{Null}(A)$ and, therefore, $\text{Null}(A)\ne \{0\}.$

- Statement “$A$ is not invertible” is true. Since $\text{Null}(A)\ne \{0\},$ then according to the invertible matrix theorem, the matrix $A$ can't be invertible.

- Statement $\text{Col}(A)\ne {R}^{4}$ is true. Since $A$ is not invertible, then by the invertible matrix theorem, we must have $\text{Col}(A)\ne {R}^{4}.$

Therefore, the correct answer is “$A$ is not invertible”; $\text{Col}(A)\ne {R}^{4}$ only.

Answer $A$ is not invertible: true

Answer $\text{Col}(A)\ne {\mathbb{R}}^{4}$: true

Answer $\text{Null}(A)=\{\mathbf{0}\}$: false

### Сompleting a Sentence Using the Invertible Matrix Theorem (21 captured questions)

Question 17592186125167 — None

Consider the following sentence:

> *If $A$ is a $n \times n$ matrix and $\det(A) \ne 0$, then $\underline{\phantom{xxxxxx}}$.*

Which of the following can be placed into the blank space to make a true statement?

1. $A$ has no inverse
2. $\operatorname{Null}(A)$ has the empty set as a basis
3. $A$ has $n$ pivot columns

Solution: Since $\det(A)\ne0$, the matrix $A$ is invertible. Thus statement I is false.

The homogeneous equation $A\mathbf x=\mathbf0$ has only the trivial solution, so $\operatorname{Null}(A)=\{\mathbf0\}$. The empty set is linearly independent and its span is $\{\mathbf0\}$, so it is a basis of this null space. Thus statement II is true.

An invertible $n\times n$ matrix has a pivot in every column, so statement III is true. Therefore, the correct answer is II and III only.

Answer selection: II and III only

Question 17592186125168 — question.difficulty/moderate

Consider the following sentence:

*If $A$ is a $7\times 7$ matrix and $A$ is invertible,  then $\underline{\phantom{xxxxxx}}$ .*

Which of the following can be placed into the blank space to make a true statement?

Select all that apply.

Solution: If $A$ is an $7\times 7$ matrix, the invertible matrix theorem states the following:

$$
A\text{ is }\text{invertible}\quad\Longleftrightarrow\quad\left\{\begin{aligned}\operatorname{Col}(A) &=\mathbb{R}^{7} \\ \dim(\operatorname{Col}(A)) &=7=\operatorname{rank}(A) \\ \operatorname{Null}(A) &=\{0\} \\ \dim(\operatorname{Null}(A)) &=0=\operatorname{nullity}(A)\end{aligned}\right.
$$

With that in mind, let's examine each of the options separately.

- The following statement is false:

*If $A$ is a $7\times 7$ matrix and $A$ is invertible,  then $\det(A)=0$* $\,\times$ 

Since the matrix $A$ is invertible, it must be  $\det(A)\ne 0.$

- The following statement is true:

*If $A$ is a $7\times 7$ matrix and $A$ is invertible,  then  $\text{Col}(A)={R}^{7}.$* $\,✓$

Indeed, since $A$ is invertible, then according to the invertible matrix theorem,  we have $\text{Col}(A)={R}^{7}.$

- The following statement is false:

*If $A$ is a $7\times 7$ matrix and $A$ is invertible,  then $A$ has $5$ pivot columns.* $\,\times$ 

Since $A$ is invertible, then according to the invertible matrix theorem, we have $\text{dim(Col}(A))=7,$ which means that $A$ has exactly $7$ pivot columns.

Therefore, the correct answer is $\text{Col}(A)={R}^{7}$ only.

Answer $A$ has $5$ pivot columns: false

Answer $\det(A)=0$: false

Answer $\text{Col}(A)={\mathbb{R}}^{7}$: true

Question 17592186272348 — question.difficulty/moderate

Consider the following sentence:

*If $A$ is a $n\times n$ matrix and $\text{nullity}(A)=0,$ then  $\underline{\phantom{xxxxxx}}\,.$*

Which of the following can be placed into the blank space to make a true statement?

Select all that apply.

Solution: The invertible matrix theorem states the following:

$$
A\text{ is }\text{invertible}\quad\Longleftrightarrow\quad\left\{\begin{aligned}\operatorname{Col}(A) &=\mathbb{R}^{n} \\ \dim(\operatorname{Col}(A)) &=n=\operatorname{rank}(A) \\ \operatorname{Null}(A) &=\{0\} \\ \dim(\operatorname{Null}(A)) &=0=\operatorname{nullity}(A)\end{aligned}\right.
$$

With that in mind, let's examine each of the options separately.

- The following statement is true:

*If $A$ is a $n\times n$ matrix and $\text{nullity}(A)=0,$ then $A$ is invertible.* $\,✓$ 

Indeed, according to the invertible matrix theorem, 

$A$ is invertible $\,⇔\,\text{dim(Null}(A))=0=\text{nullity}(A).$

- The following statement is false:

*If $A$ is a $n\times n$ matrix and $\text{nullity}(A)=0,$ then $\text{rank}(A)<n.$* $\,\times$ 

Indeed, since $A$ is invertible, then according to the invertible matrix theorem, we have $\text{rank}(A)=n.$

- The following statement is true:

*If $A$ is a $n\times n$ matrix and $\text{nullity}(A)=0,$ then $\text{Col}(A)={R}^{n}.$*  $\,✓$ 

Indeed, since $A$ is invertible, then according to the invertible matrix theorem, we have $\text{Col}(A)={R}^{n}.$

Therefore, the correct answer is “$A$ is invertible”; $\text{Col}(A)={R}^{n}$ only.

Answer $A$ is invertible: true

Answer $\text{Col}(A)={\mathbb{R}}^{n}$: true

Answer $\text{rank}(A)<n$: false
