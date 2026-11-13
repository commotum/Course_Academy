# 17592186049606 Orthogonal Matrices

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186135177 — Introduction

Suppose we have a square $n\times n$ matrix $Q$ with columns $\mathbf{q}_1, \mathbf{q}_2, \ldots, \mathbf{q}_n{:}$

$$
Q = {\left[ \begin{array}{cccc}| & | &  & | \\ {\mathbf{q}}_{1} & {\mathbf{q}}_{2} & \cdots  & {\mathbf{q}}_{n} \\ | & | &  & |\end{array} \right]}
$$

The matrix $Q$ is said to be **orthogonal** if its columns $\mathbf{q}_1, \mathbf{q}_2, \dots, \mathbf{q}_n$ form an *orthonormal* set. In other words, 

- the columns of $Q$ must be *mutually orthogonal*, and

- they must all be *unit* vectors.

For instance, the matrix 
$$
Q={\left[ \begin{array}{cc}{\color{black}{\displaystyle \frac{\sqrt{3}}{2}}} & {\color{black}- {\displaystyle \frac{1}{2}}} \\ {\color{black}{\displaystyle \frac{1}{2}}} & {\color{black}{\displaystyle \frac{\sqrt{3}}{2}}}\end{array} \right]}
$$ 
is orthogonal since its columns 

$$
{\color{black}\mathbf{q}_1}={\color{black}{\left[ \begin{array}{c}{\displaystyle \frac{\sqrt{3}}{2}} \\ {\displaystyle \frac{1}{2}}\end{array} \right]}}, 
\qquad
{\color{black}\mathbf{q}_2}={\color{black}{\left[ \begin{array}{c}- {\displaystyle \frac{1}{2}} \\ {\displaystyle \frac{\sqrt{3}}{2}}\end{array} \right]}}
$$

form an orthonormal set $\left\{ {\color{black}\mathbf{q}_1}, {\color{black}\mathbf{q}_2} \right\}.$ To see this, note the following:

- The vectors $\mathbf q_1$ and $\mathbf q_2$ are orthogonal, since

$$
\begin{aligned}{\color{black}{{\mathbf{q}}_{1}}}\cdot {\color{black}{{\mathbf{q}}_{2}}} & =\begin{bmatrix}\frac{\sqrt{3}}{2} \\ \frac{1}{2}\end{bmatrix}\cdot \begin{bmatrix}-\frac{1}{2} \\ \frac{\sqrt{3}}{2}\end{bmatrix} \\  & =\left(\frac{\sqrt{3}}{2}\right)\cdot \left(-\frac{1}{2}\right)+\left(\frac{1}{2}\right)\cdot \left(\frac{\sqrt{3}}{2}\right) \\  & =-\frac{\sqrt{3}}{4}+\frac{\sqrt{3}}{4} \\  & =0.\end{aligned}
$$

- Both $\mathbf q_1$ and $\mathbf q_2$ are unit vectors, since

$$
\begin{aligned}||{\mathbf{q}}_{1}|{|}^{2} & ={\mathbf{q}}_{1}\cdot {\mathbf{q}}_{1} \\  & =\begin{bmatrix}\frac{\sqrt{3}}{2} \\ \frac{1}{2}\end{bmatrix}\cdot \begin{bmatrix}\frac{\sqrt{3}}{2} \\ \frac{1}{2}\end{bmatrix} \\  & ={\left(\frac{\sqrt{3}}{2}\right)}^{2}+{\left(\frac{1}{2}\right)}^{2} \\  & =\frac{3}{4}+\frac{1}{4} \\  & =1,\end{aligned}
$$

and

$$
\begin{aligned}||{\mathbf{q}}_{2}|{|}^{2} & ={\mathbf{q}}_{2}\cdot {\mathbf{q}}_{2} \\  & =\begin{bmatrix}-\frac{1}{2} \\ \frac{\sqrt{3}}{2}\end{bmatrix}\cdot \begin{bmatrix}-\frac{1}{2} \\ \frac{\sqrt{3}}{2}\end{bmatrix} \\  & ={\left(-\frac{1}{2}\right)}^{2}+{\left(\frac{\sqrt{3}}{2}\right)}^{2} \\  & =\frac{1}{4}+\frac{3}{4} \\  & =1.\end{aligned}
$$



### tutorial 17592186135182 — A Straightforward Test of Orthogonality

Checking that the columns of $Q$ form an orthonormal set is a fair amount of work. Thankfully, we have the following theorem to make our lives easier: 

*A matrix $Q$ is orthogonal if and only if*

$$
Q \cdot Q^T = Q^T \cdot Q = I
$$

Note the following:

- $Q^T$ denotes the transpose of $Q.$  It's the matrix we get when we interchange the rows and columns of $Q.$

- To verify that a matrix is orthogonal in practice, we only need to check that $Q \, Q^T = I.$

Let's see an example of applying this theorem.



### example 17592186133503 — Identifying Orthogonal Matrices

$$
A={\left[ \begin{array}{cc}{\displaystyle \frac{1}{\sqrt{2}}} & - {\displaystyle \frac{1}{\sqrt{2}}} \\ {\displaystyle \frac{1}{\sqrt{2}}} & {\displaystyle \frac{1}{\sqrt{2}}}\end{array} \right]}
$$

Consider the matrix $A$ above. Which of the following statements are true?

I. $A$ is a square matrix

II. $A \cdot A^T = I$

III. $A$ is an orthogonal matrix

Recall that a square matrix $A$ is **orthogonal** if and only if

$$
A \cdot A^T = A^T\cdot A = I
$$

where $I$ is the identity matrix.

With that in mind, let's examine the given statements. 

- Statement I is true. The number of rows in $A$ is the same as the number of columns. So, it's a square matrix.

- Statement II is true. Indeed,
$$
A \cdot A^T = {\left[ \begin{array}{cc}{\displaystyle \frac{1}{\sqrt{2}}} & - {\displaystyle \frac{1}{\sqrt{2}}} \\ {\displaystyle \frac{1}{\sqrt{2}}} & {\displaystyle \frac{1}{\sqrt{2}}}\end{array} \right]} {\left[ \begin{array}{cc}{\displaystyle \frac{1}{\sqrt{2}}} & {\displaystyle \frac{1}{\sqrt{2}}} \\ - {\displaystyle \frac{1}{\sqrt{2}}} & {\displaystyle \frac{1}{\sqrt{2}}}\end{array} \right]} = {\left[ \begin{array}{cc}1 & 0 \\ 0 & 1\end{array} \right]} = I.
$$

- Statement III is true. Since $A\cdot A^T = I,$ our matrix is orthogonal.

Therefore, the correct answer is "I, II, and III."

### tutorial 17592186135179 — The Inverse of an Orthogonal Matrix

Recall the following theorem:

*A matrix $Q$ is orthogonal if and only if*

$$
Q \cdot {\color{blue}{Q^T}} = {\color{blue}{Q^T}} \cdot Q = I.
$$

Now, recall that for $Q$ to be invertible, there must exist a matrix $Q^{-1}$ such that

$$
Q \cdot {\color{blue}{Q^{-1}}} = {\color{blue}{Q^{-1}}} \cdot Q = I.
$$

By comparing the two equations above, we can deduce the following:

- Every orthogonal matrix $Q$ is invertible, and

- the inverse of an orthogonal matrix $Q$ is ${\color{blue}{Q^T}},$ that is

$$
Q^{-1} = Q^T.
$$

These properties explain why orthogonal matrices are desirable. We can always find the inverse of an orthogonal matrix, and we can quickly compute the inverse by simply transposing the original matrix.



### example 17592186133505 — Calculating the Inverse of an Orthogonal Matrix

Find the inverse of the orthogonal matrix $D={\left[ \begin{array}{cc}{\displaystyle \frac{1}{\sqrt{2}}} & {\displaystyle \frac{1}{\sqrt{2}}} \\ - {\displaystyle \frac{1}{\sqrt{2}}} & {\displaystyle \frac{1}{\sqrt{2}}}\end{array} \right]}.$

The inverse of an orthogonal matrix is equal to its transpose.

Therefore, since $D$ is orthogonal, we have 

$$
\begin{aligned}{D}^{-1} & ={D}^{T}=\begin{bmatrix}\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}}\end{bmatrix}.\end{aligned}
$$

### tutorial 17592186135178 — Properties of Orthogonal Matrices

Orthogonal matrices also have the following important properties:

- $\det(Q)=\pm1$ (the determinant of an orthogonal matrix is either $1$ or $-1$)

- If $\lambda$ is an eigenvalue of an orthogonal matrix $Q,$ then $| \lambda |= 1 .$

**Watch out!** These properties are necessary *but not sufficient* conditions:

- Every orthogonal matrix has determinant equal to $\pm 1$, but not every matrix with determinant $\pm 1$ is orthogonal!

- Similarly, every orthogonal matrix has eigenvalues $1$ or $-1$ only, but not every matrix with eigenvalues $1$ or $-1$ is orthogonal.



### example 17592186133504 — Calculating the Determinant of a Product of Matrices

$$
P={\left[ \begin{array}{cc}{\displaystyle \frac{2}{\sqrt{13}}} & - {\displaystyle \frac{3}{\sqrt{13}}} \\ {\displaystyle \frac{3}{\sqrt{13}}} & {\displaystyle \frac{2}{\sqrt{13}}}\end{array} \right]}, \qquad
Q={\left[ \begin{array}{cc}- 2 \sqrt{3} & 1 \\ 2 & 3 \sqrt{3}\end{array} \right]}
$$

Find $|\textrm{det}(PQ)|$ given that $P$ is an orthogonal matrix.

We use the following facts: 

- The determinant of a product is equal to the product of the determinants.

- The determinant of an orthogonal matrix $P$ is equal to $\pm1.$

Applying these ideas, we get the following:

$$
\begin{aligned}|\text{det}(PQ)| & =|\text{det}(P)\cdot \text{det}(Q)| \\  & =|(\pm 1)\cdot \text{det}(Q)| \\  & =|\pm 1|\cdot |\text{det}(Q)| \\  & =|\text{det}(Q)| \\  & =|(-2\sqrt{3})\cdot 3\sqrt{3}-2\cdot 1| \\  & =|-18-2| \\  & =|-20| \\  & =20\end{aligned}
$$

### example 17592186133506 — Identifying True Statements About Orthogonal Matrices

Which of the following statements are true regarding the $n\times n$ orthogonal matrices $P$ and $Q?$

I. $2Q$ is orthogonal

II. $P^{-1}Q$ is orthogonal

III. $PQ^T$ is orthogonal

Recall that a matrix $Q$ is orthogonal if and only if

$$
Q Q^T = Q^T Q = I.
$$

To check that a matrix is orthogonal, it is sufficient to check that the above equation is satisfied.

Moreover, we have the following properties:

- For any orthogonal matrix $Q,$ we have $Q^{-1} = Q^T.$

- $(AB)^T = B^TA^T$ for conformable matrices $A$ and $B.$

With that in mind, let's inspect each statement in turn.

- Statement I is false. Computing the product $2Q \cdot (2Q)^T,$ we obtain

$$
\begin{aligned}2Q\cdot (2Q)^{T} & =2Q\cdot 2{Q}^{T} \\  & =4Q{Q}^{T} \\  & =4I \\  & \ne I.\end{aligned}
$$

- Statement II is true. Computing the product $(P^{-1}Q)\cdot (P^{-1}Q)^T,$ we obtain

$$
\begin{aligned}({P}^{-1}Q)\cdot ({P}^{-1}Q)^{T} & =({P}^{T}Q)\cdot ({P}^{T}Q)^{T} \\  & ={P}^{T}Q\cdot {Q}^{T}({P}^{T})^{T} \\  & ={P}^{T}(Q{Q}^{T})P \\  & ={P}^{T}(I)P \\  & ={P}^{T}P \\  & =I.\end{aligned}
$$

- Statement III is true. Computing the product $(PQ^T)\cdot(PQ^T)^T ,$ we obtain

$$
\begin{aligned}(P{Q}^{T})\cdot (P{Q}^{T})^{T} & =P{Q}^{T}\cdot ({Q}^{T})^{T}{P}^{T} \\  & =P{Q}^{T}Q{P}^{T} \\  & =P({Q}^{T}Q){P}^{T} \\  & =P(I){P}^{T} \\  & =P{P}^{T} \\  & =I.\end{aligned}
$$

Therefore, the correct answer is "II and III only."

## Representative practice (first three per skill; full bank in practice.json)

### Identifying Orthogonal Matrices (17 captured questions)

Question 17592186134145 — question.difficulty/easy

$$
\displaystyle A = \begin{bmatrix}-1 & 0 \\ 0 & 1\end{bmatrix}
$$

Consider the matrix $A$ above. Which of the following statements are true?

1. $A$ is a square matrix
2. $A \cdot A^{T} = I$
3. $A$ is an orthogonal matrix

Solution: Statement I is true because $A$ is $2\times2$. Also,

$$
AA^T=\begin{bmatrix}-1&0\\0&1\end{bmatrix}\begin{bmatrix}-1&0\\0&1\end{bmatrix}=I_2.
$$

Thus statement II is true. A square matrix with $AA^T=I$ is orthogonal, so statement III is true. The correct answer is "I, II, and III."

Answer selection: I, II, and III

Question 17592186134146 — question.difficulty/moderate

$$
\displaystyle A = \begin{bmatrix}\frac{1}{2} & 0 & 1 \\ 0 & 1 & 0 \\ 1 & 0 & -\frac{1}{2}\end{bmatrix}
$$

Consider the matrix $A$ above. Which of the following statements are true?

1. $A$ is a square matrix
2. $A \cdot A^{T} = I$
3. $A$ is an orthogonal matrix

Solution: Statement I is true because $A$ is $3\times3$. However,

$$
AA^T=\begin{bmatrix}\frac54&0&0\\0&1&0\\0&0&\frac54\end{bmatrix}\ne I_3.
$$

Therefore, statement II is false and $A$ is not orthogonal, so statement III is false. The correct answer is "I only."

Answer selection: I only

Question 17592186284752 — question.difficulty/easy

$$
A=\begin{bmatrix}2 & 3 \\ -3 & 2\end{bmatrix}
$$

Consider the matrix $A$ above. Which of the following statements are true?

Select all that apply.

Solution: Recall that a square matrix $A$ is **orthogonal** if and only if

$$
A\cdot {A}^{T}={A}^{T}\cdot A=I
$$

where $I$ is the identity matrix.

With that in mind, let's examine the given statements. 

- Statement “$A$ is a square matrix” is true. The number of rows in $A$ is the same as the number of columns. So, it's a square matrix.

- Statement $A\cdot {A}^{T}=I$ is false. Note that

$$
A\cdot {A}^{T}=\begin{bmatrix}2 & 3 \\ -3 & 2\end{bmatrix}\begin{bmatrix}2 & -3 \\ 3 & 2\end{bmatrix}=\begin{bmatrix}13 & 0 \\ 0 & 13\end{bmatrix}\ne I.
$$

- Statement “$A$ is an orthogonal matrix” is false. Since $A\cdot {A}^{T}\ne I,$ our matrix is **not** orthogonal.

Therefore, the correct answer is “$A$ is a square matrix” only.

Answer $A$ is a square matrix: true

Answer $A$ is an orthogonal matrix: false

Answer $A\cdot {A}^{T}=I$: false

### Calculating the Inverse of an Orthogonal Matrix (12 captured questions)

Question 17592186134241 — question.difficulty/easy

Find the inverse of the orthogonal matrix $D = \begin{bmatrix}-\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{bmatrix}$.

Solution: The inverse of an orthogonal matrix equals its transpose. Therefore,

$$
D^{-1}=D^T=\begin{bmatrix}-\frac{1}{\sqrt2}&\frac{1}{\sqrt2}\\-\frac{1}{\sqrt2}&-\frac{1}{\sqrt2}\end{bmatrix}.
$$

Answer selection: \begin{bmatrix}-\frac{1}{\sqrt{2}} & \frac{1}{\sqrt{2}} \\ -\frac{1}{\sqrt{2}} & -\frac{1}{\sqrt{2}}\end{bmatrix}

Question 17592186134242 — question.difficulty/moderate

Solve for $\mathbf{x}$ in $A\mathbf{x}=\mathbf{b}$ given that the matrix $A$ is orthogonal, and 

$$
A=\begin{bmatrix}-\frac{1}{\sqrt{2}} & 0 & -\frac{1}{\sqrt{2}} \\ 0 & -1 & 0 \\ \frac{1}{\sqrt{2}} & 0 & -\frac{1}{\sqrt{2}}\end{bmatrix},\hspace{2em}\mathbf{b}=\begin{bmatrix}2\sqrt{2} \\ 0 \\ -2\sqrt{2}\end{bmatrix}.
$$

Solution: The inverse of an orthogonal matrix is equal to its transpose.

Hence, since $A$ is orthogonal, we have ${A}^{-1}={A}^{T}.$ Therefore,

$$
\begin{aligned}Ax & =b \\ {A}^{-1}Ax & ={A}^{-1}b \\ x & ={A}^{-1}b \\ x & ={A}^{T}b \\ x & =\begin{bmatrix}-\frac{1}{\sqrt{2}} & 0 & \frac{1}{\sqrt{2}} \\ 0 & -1 & 0 \\ -\frac{1}{\sqrt{2}} & 0 & -\frac{1}{\sqrt{2}}\end{bmatrix}\begin{bmatrix}2\sqrt{2} \\ 0 \\ -2\sqrt{2}\end{bmatrix} \\  & =\begin{bmatrix}-4 \\ 0 \\ 0\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}-4 \\ 0 \\ 0\end{bmatrix}

Question 17592186272133 — question.difficulty/moderate

Solve for $\mathbf{x}$ in $A\mathbf{x}=\mathbf{b}$ given that the matrix $A$ is orthogonal, and 

$$
A=\begin{bmatrix}\frac{1}{3} & \frac{2}{3} & -\frac{2}{3} \\ \frac{2}{\sqrt{5}} & 0 & \frac{1}{\sqrt{5}} \\ -\frac{2\sqrt{5}}{15} & \frac{\sqrt{5}}{3} & \frac{4\sqrt{5}}{15}\end{bmatrix},\hspace{2em}\mathbf{b}=\begin{bmatrix}1 \\ \sqrt{5} \\ 0\end{bmatrix}.
$$

Solution: The inverse of an orthogonal matrix is equal to its transpose.

Hence, since $A$ is orthogonal, we have ${A}^{-1}={A}^{T}.$ Therefore,

$$
\begin{aligned}A\mathbf{x} & =\mathbf{b} \\ {A}^{-1}A\mathbf{x} & ={A}^{-1}\mathbf{b} \\ \mathbf{x} & ={A}^{-1}\mathbf{b} \\ \mathbf{x} & ={A}^{T}\mathbf{b} \\ \mathbf{x} & =\begin{bmatrix}\frac{1}{3} & \frac{2}{\sqrt{5}} & -\frac{2\sqrt{5}}{15} \\ \frac{2}{3} & 0 & \frac{\sqrt{5}}{3} \\ -\frac{2}{3} & \frac{1}{\sqrt{5}} & \frac{4\sqrt{5}}{15}\end{bmatrix}\begin{bmatrix}1 \\ \sqrt{5} \\ 0\end{bmatrix} \\  & =\begin{bmatrix}\frac{7}{3} \\ \frac{2}{3} \\ \frac{1}{3}\end{bmatrix}.\end{aligned}
$$

Answer selection: \begin{bmatrix}\frac{7}{3} \\ \frac{2}{3} \\ \frac{1}{3}\end{bmatrix}

### Calculating the Determinant of a Product of Matrices (12 captured questions)

Question 17592186134244 — question.difficulty/easy

$$
P=\begin{bmatrix}-\frac{2}{\sqrt{5}} & \frac{1}{\sqrt{5}} \\ \frac{1}{\sqrt{5}} & \frac{2}{\sqrt{5}}\end{bmatrix},\,Q=\begin{bmatrix}\sqrt{7} & \sqrt{3} \\ 3\sqrt{3} & \sqrt{7}\end{bmatrix}
$$

Find $|\text{det}(PQ)|$ given that $P$ is an orthogonal matrix.

Solution: We use the following facts: 

- The determinant of a product is equal to the product of the determinants.

- The determinant of an orthogonal matrix $P$ is equal to $\pm 1.$

Applying these ideas, we get the following:

$$
\begin{aligned}|\text{det}(PQ)| & =|\text{det}(P)\cdot \text{det}(Q)| \\  & =|(\pm 1)\cdot \text{det}(Q)| \\  & =|\pm 1|\cdot |\text{det}(Q)| \\  & =|\text{det}(Q)| \\  & =|\sqrt{7}\cdot \sqrt{7}-\sqrt{3}\cdot 3\sqrt{3}| \\  & =2\end{aligned}
$$

Answer selection: 2

Question 17592186134245 — question.difficulty/easy

$$
P=\begin{bmatrix}-\frac{3}{\sqrt{10}} & \frac{1}{\sqrt{10}} \\ \frac{1}{\sqrt{10}} & \frac{3}{\sqrt{10}}\end{bmatrix},\,Q=\begin{bmatrix}\sqrt{2} & 8 \\ -4 & \sqrt{2}\end{bmatrix}
$$

Find $|\text{det}(PQ)|$ given that $P$ is an orthogonal matrix.

Solution: We use the following facts: 

- The determinant of a product is equal to the product of the determinants.

- The determinant of an orthogonal matrix $P$ is equal to $\pm 1.$

Applying these ideas, we get the following:

$$
\begin{aligned}|\text{det}(PQ)| & =|\text{det}(P)\cdot \text{det}(Q)| \\  & =|(\pm 1)\cdot \text{det}(Q)| \\  & =|\pm 1|\cdot |\text{det}(Q)| \\  & =|\text{det}(Q)| \\  & =|\sqrt{2}\cdot \sqrt{2}-8\cdot (-4)| \\  & =34\end{aligned}
$$

Answer selection: 34

Question 17592186354294 — question.difficulty/easy

$$
P=\begin{bmatrix}\frac{1}{\sqrt{17}} & \frac{4}{\sqrt{17}} \\ -\frac{4}{\sqrt{17}} & \frac{1}{\sqrt{17}}\end{bmatrix},\,Q=\begin{bmatrix}5 & \sqrt{2} \\ 4\sqrt{2} & 5\end{bmatrix}
$$

Find $|\text{det}(PQ)|$ given that $P$ is an orthogonal matrix.

Solution: We use the following facts: 

- The determinant of a product is equal to the product of the determinants.

- The determinant of an orthogonal matrix $P$ is equal to $\pm 1.$

Applying these ideas, we get the following:

$$
\begin{aligned}|\text{det}(PQ)| & =|\text{det}(P)\cdot \text{det}(Q)| \\  & =|(\pm 1)\cdot \text{det}(Q)| \\  & =|\pm 1|\cdot |\text{det}(Q)| \\  & =|\text{det}(Q)| \\  & =|5\cdot 5-\sqrt{2}\cdot 4\sqrt{2}| \\  & =17\end{aligned}
$$

Answer selection: 17

### Identifying True Statements About Orthogonal Matrices (12 captured questions)

Question 17592186134226 — question.difficulty/hard

Which of the following statements are true regarding the $n\times n$ orthogonal matrices $P$ and $Q?$

I. $Q$ is invertible

II. $PQ$ is always orthogonal

III. $P+Q$ is always orthogonal

Solution: Recall that a matrix $Q$ is orthogonal if and only if

$$
Q{Q}^{T}={Q}^{T}Q=I.
$$

To check that a matrix is orthogonal, it is sufficient to check that the above equation is satisfied.

Moreover, we have the following properties:

- For any orthogonal matrix $Q,$ we have ${Q}^{-1}={Q}^{T}.$

- $(AB)^{T}={B}^{T}{A}^{T}$ for conformable matrices $A$ and $B.$

With that in mind, let's inspect each of the statements in turn.

- Statement I is true. The inverse of an orthogonal matrix $Q$ is given by ${Q}^{-1}={Q}^{T}.$

- Statement II is true. Computing the product $(PQ)\cdot (PQ)^{T},$ we obtain

$$
\begin{aligned}(PQ)\cdot (PQ)^{T} & =PQ\cdot {Q}^{T}{P}^{T} \\  & =P(Q{Q}^{T}){P}^{T} \\  & =P(I){P}^{T} \\  & =P{P}^{T} \\  & =I.\end{aligned}
$$

- Statement III is false. As a counterexample, consider the following sum of two orthogonal matrices:

$$
\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}+\begin{bmatrix}0 & 1 \\ 1 & 0\end{bmatrix}=\begin{bmatrix}1 & 1 \\ 1 & 1\end{bmatrix}
$$

The resulting matrix is not orthogonal since, for example,it is not invertible.

Therefore, the correct answer is "I and II only."

Answer selection: I and II only

Question 17592186134475 — question.difficulty/moderate

Which of the following statements are true regarding the orthogonal matrix $Q?$

Select all that apply.

Solution: Recall that a matrix $Q$ is orthogonal if and only if

$$
Q{Q}^{T}={Q}^{T}Q=I.
$$

To check that a matrix is orthogonal, it is sufficient to check that the above equation is satisfied.

Moreover, we have the following properties:

- For any orthogonal matrix $Q,$ we have ${Q}^{-1}={Q}^{T}.$

- $(AB)^{T}={B}^{T}{A}^{T}$ for conformable matrices $A$ and $B.$

With that in mind, let's inspect each of the statements in turn.

- Statement “${Q}^{T}$ is orthogonal” is true. Computing the product ${Q}^{T}\cdot ({Q}^{T})^{T},$ we obtain

$$
\begin{aligned}{Q}^{T}\cdot ({Q}^{T})^{T} & ={Q}^{T}Q \\  & =I.\end{aligned}
$$

- Statement “The identity matrix $I$ is orthogonal” is true. The columns of the identity matrix are orthonormal. Therefore, $I$ is an orthogonal matrix.

- Statement “$2Q$ is orthogonal” is false. Computing the product $2Q\cdot (2Q)^{T},$ we obtain

$$
\begin{aligned}2Q\cdot (2Q)^{T} & =2Q\cdot 2{Q}^{T} \\  & =4Q{Q}^{T} \\  & =4I \\  & \ne I.\end{aligned}
$$

Therefore, the correct answer is “${Q}^{T}$ is orthogonal”; “The identity matrix $I$ is orthogonal” only.

Answer $2Q$ is orthogonal: false

Answer ${Q}^{T}$ is orthogonal: true

Answer The identity matrix $I$ is orthogonal: true

Question 17592186272134 — question.difficulty/hard

Which of the following statements are true regarding the $n\times n$ orthogonal matrix $Q$ and the $n\times n$ matrix $P?$

Select all that apply.

Solution: Recall that a matrix $Q$ is orthogonal if and only if

$$
Q{Q}^{T}={Q}^{T}Q=I.
$$

To check that a matrix is orthogonal, it is sufficient to check that the above equation is satisfied.

Moreover, we have the following properties:

- For any orthogonal matrix $Q,$ we have ${Q}^{-1}={Q}^{T}.$

- $(AB)^{T}={B}^{T}{A}^{T}$ for conformable matrices $A$ and $B.$

With that in mind, let's inspect each of the statements in turn.

- Statement “If $\lambda $ is a real eigenvalue of $Q,$ then $\lambda =\pm 1$” is true. If $\lambda $ is an eigenvalue of an orthogonal matrix $Q$ then $\lambda =\pm 1$

- Statement “If the determinant of $P$ is either $1$ or $-1,$ then $P$ is orthogonal” is false. Every orthogonal matrix has the determinant equal to $\pm 1$, but not every matrix with the determinant equal to $\pm 1$ is orthogonal. As a counterexample, consider the following matrix:

$$
P=\begin{bmatrix}2 & 1 \\ 1 & 1\end{bmatrix}
$$

The determinant of $P$ is

$$
\begin{aligned}\det (P)=2\cdot 1-1\cdot 1=1,\end{aligned}
$$

 however, $P$ is not orthogonal since, for example, the first column is not normalized.

- Statement “$Q-I$ is singular” is false. As a counterexample, consider the following orthogonal matrix:

$$
Q=\begin{bmatrix}\frac{3}{5} & -\frac{4}{5} \\ \frac{4}{5} & \frac{3}{5}\end{bmatrix}
$$

We have that

$$
Q-I=\begin{bmatrix}\frac{3}{5} & -\frac{4}{5} \\ \frac{4}{5} & \frac{3}{5}\end{bmatrix}-\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}=\begin{bmatrix}-\frac{2}{5} & -\frac{4}{5} \\ \frac{4}{5} & -\frac{2}{5}\end{bmatrix}
$$

and $Q-I$ is not singular since, for example, it doesn't have proportional rows or columns.

Therefore, the correct answer is “If $\lambda $ is a real eigenvalue of $Q,$ then $\lambda =\pm 1$” only.

Answer $Q-I$ is singular: false

Answer If $\lambda $ is a real eigenvalue of $Q,$ then $\lambda =\pm 1$: true

Answer If the determinant of $P$ is either $1$ or $-1,$ then $P$ is orthogonal: false

Answer None of the above: false
