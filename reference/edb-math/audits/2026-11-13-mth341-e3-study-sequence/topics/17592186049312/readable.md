# 17592186049312 Conditions When a Determinant Equals Zero

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186135151 — Introduction

If an $n\!\times \!n$ matrix $A$ has an entire row or column of zeros, then its determinant is equal to zero.

For example, consider the matrix $A$ given below:

$$
A=
{\left[ \begin{array}{ccc}∗ & ∗ & ∗ \\ 0 & 0 & 0 \\ ∗ & ∗ & ∗\end{array} \right]}
$$

The second row consists of all zeros, and the asterisks ($\ast$) may represent any number.

Let's compute the determinant using the Laplace expansion across the second row:

$$
\begin{aligned}\det (A) & =\begin{vmatrix}∗ & ∗ & ∗ \\ {\color{red}0} & {\color{red}0} & {\color{red}0} \\ ∗ & ∗ & ∗\end{vmatrix} \\  & =(-1)^{2+1}({\color{red}0})\begin{vmatrix}∗ & ∗ \\ ∗ & ∗\end{vmatrix}+(-1)^{2+2}({\color{red}0})\begin{vmatrix}∗ & ∗ \\ ∗ & ∗\end{vmatrix}+(-1)^{2+3}({\color{red}0})\begin{vmatrix}∗ & ∗ \\ ∗ & ∗\end{vmatrix} \\  & =0+0+0 \\  & =0\end{aligned}
$$

Notice that it doesn't matter what numbers are represented by the asterisks ($\ast$). Each cofactor is multiplied by zero, so the final result must be zero.



### tutorial 17592186135152 — Determinants with Identical Rows or Identical Columns

Now, suppose a matrix has no zero rows but it has two identical rows:

$$
A  = {\left[ \begin{array}{ccc}{\color{blue}1} & {\color{blue}2} & {\color{blue}1} \\ 1 & 2 & 3 \\ {\color{blue}1} & {\color{blue}2} & {\color{blue}1}\end{array} \right]}.
$$

We can subtract the $1$st row from the $3$rd row, as follows:

$$
\begin{aligned}A & =\begin{bmatrix}{\color{blue}1} & {\color{blue}2} & {\color{blue}1} \\ 1 & 2 & 3 \\ {\color{blue}1} & {\color{blue}2} & {\color{blue}1}\end{bmatrix} & {R}_{3} & :={R}_{3}+(-1){R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 1 \\ 1 & 2 & 3 \\ {\color{red}0} & {\color{red}0} & {\color{red}0}\end{bmatrix} \\  & =B\end{aligned}
$$

Since this operation does not change the determinant, we get $\det(A) = \det(B).$ Furthermore, as $B$ contains a zero row, we obtain

$$
\det(A) = \det(B) = 0.
$$

Notice that we can use this method with columns too. Therefore, we have the following property:

*If a square matrix has at least two identical rows/columns, its determinant equals zero.*



### example 17592186133466 — Calculating the Determinant of a Matrix With A Zero Row/Column or Two Identical Rows/Columns

Find $5\det(A)-\det(B),$ where 
$$
A={\left[ \begin{array}{ccc}4 & \sqrt{13} & 4 \\ 4 & 11 & 4 \\ \sqrt{3} & 9 & \sqrt{3}\end{array} \right]}, \qquad 
B=
	{\left[ \begin{array}{ccc}3 & 0 & 0 \\ 0 & - 4 & 0 \\ 0 & 0 & - 2\end{array} \right]}.
$$

Let's examine each matrix in turn.

- Since $A$ has two identical columns, we obtain
$$
A=
{\left[ \begin{array}{ccc}{\color{blue}4} & \sqrt{13} & {\color{blue}4} \\ {\color{blue}4} & 11 & {\color{blue}4} \\ {\color{blue}\sqrt{3}} & 9 & {\color{blue}\sqrt{3}}\end{array} \right]}
\qquad\Longrightarrow\qquad 
\det(A) = 0.
$$

- Since $B$ is a diagonal matrix, its determinant is given by the product of the elements of the main diagonal: 

$$
\det(B) = 3 \cdot (-4) \cdot (-2) = 24
$$

Therefore, $5\det(A)-\det(B) = 5 \cdot 0 - 24 = -24.$

### tutorial 17592186135153 — Determinants with Proportional Rows/Columns

Now, suppose a matrix has no zero rows and no identical rows but it has two proportional rows:

$$
A  = {\left[ \begin{array}{ccc}{\color{blue}1} & {\color{blue}2} & {\color{blue}1} \\ 1 & 2 & 3 \\ {\color{blue}- 3} & {\color{blue}- 6} & {\color{blue}- 3}\end{array} \right]}
$$

We can add three times the $1$st row to the $3$rd row, as follows:

$$
\begin{aligned}A & =\begin{bmatrix}{\color{blue}1} & {\color{blue}2} & {\color{blue}1} \\ 1 & 2 & 3 \\ {\color{blue}-3} & {\color{blue}-6} & {\color{blue}-3}\end{bmatrix} & {R}_{3} & :={R}_{3}+3{R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 1 \\ 1 & 2 & 3 \\ {\color{red}0} & {\color{red}0} & {\color{red}0}\end{bmatrix} \\  & =B\end{aligned}
$$

Since this operation does not change the determinant, we get $\det(A) = \det(B).$ Furthermore, as $B$ contains a zero row, we obtain

$$
\det(A) = \det(B) = 0.
$$

Notice that we can use this method with columns too. Therefore, we have the following property:

*If a square matrix has at least two proportional rows/columns, its determinant equals zero.*



### example 17592186133467 — Calculating the Determinant of a Matrix With Two Proportional Rows/Columns

Which of the following determinants are equal to $0?$

$$
|A|=
\left|{\begin{array}{ccc}2 & \sqrt{3} & 1 \\ 1 & 1 & 2 \\ 3 & 3 & 6\end{array}}\right|,\qquad
|B|=
\left|{\begin{array}{ccc}- 1 & 0 & 0 \\ 2 & 4 & 0 \\ 1 & \sqrt{3} & - 3\end{array}}\right|, \qquad
|C|=
\left|{\begin{array}{ccc}- 1 & \sqrt{2} & \sqrt{3} \\ 0 & 0 & 0 \\ 1 & 0 & - 1\end{array}}\right|
$$

Let's examine each of the given determinants in turn.

- The matrix $A$ has proportional rows: 
$$
A = {\left[ \begin{array}{ccc}2 & \sqrt{3} & 1 \\ {\color{blue}1} & {\color{blue}1} & {\color{blue}2} \\ {\color{blue}3} & {\color{blue}3} & {\color{blue}6}\end{array} \right]}
$$
As a result, $|A| = 0.$

- The matrix $B$ is a triangular matrix, so 

$$
|B| = (-1) \cdot 4 \cdot (-3) = 12 \neq 0.
$$

- The matrix $C$ has a zero row: 
$$
C={\left[ \begin{array}{ccc}- 1 & \sqrt{2} & \sqrt{3} \\ {\color{blue}0} & {\color{blue}0} & {\color{blue}0} \\ 1 & 0 & - 1\end{array} \right]}
$$
As a result, $|C| = 0.$

Therefore, only $|A|$ and $|C|$ are equal to $0.$

### tutorial 17592186135154 — Conditions When a Determinant Equals Zero

In conclusion, if an $n\!\times \!n$ matrix $A$ satisfies any one of the following conditions, then $\det(A)=0.$

I. $A$ has a zero row/column

II. $A$ has two identical rows/columns

III. $A$ has two proportional rows/columns

IV. $A$ has a row/column that is a linear combination of other rows/columns

Notice that condition IV encompasses each of the conditions I, II, and III. If we have a zero row/column, two identical rows/columns, or proportional rows/columns, then the rows/columns form a linearly dependent set of vectors. 
In turn, this means that one of the rows/columns is a linear combination of other rows/columns.

**Watch out!** While all of the above conditions are *sufficient* to conclude that $\det(A)=0,$ only condition IV is *necessary* to conclude that $\det(A)=0.$ 
In other words, if we have a matrix $A$ with $\det(A)=0,$ then conditions I, II, and III may or may not be satisfied, while condition IV *must* be satisfied. 

So, we have the following theorem:

*$\det(A)=0$ if and only if one of the rows/columns of $A$ is a linear combination of other rows/columns of $A.$*

Finally, note also that in the case of a $2\times 2$ matrix *only*, statements III and IV mean the same thing.



### tutorial 17592186135155 — Geometric Interpretation of a Zero Determinant

Geometrically, the absolute value of an $n \times n$ determinant can be interpreted as the volume of the $n$-dimensional parallelepiped spanned by the columns of the determinant. 

For example:

- Suppose the columns of a $3\times 3$ matrix $A$ are ${\color{black}\mathbf{a}}, {\color{black}\mathbf{b}},$ and ${\color{black}\mathbf{c}}.$
$$
A = {\left[ \begin{array}{ccc}{\color{black}|} & {\color{black}|} & {\color{black}|} \\ {\color{black}\mathbf{a}} & {\color{black}\mathbf{b}} & {\color{black}\mathbf{c}} \\ {\color{black}|} & {\color{black}|} & {\color{black}|}\end{array} \right]}
$$
The $3$-dimensional parallelepiped spanned by the columns of $A$ is depicted below:

![](images/25/2597b48a010607fca71c551dbce8e9e2bbeda47d0892a582347ae1cdf19f1bf6.png)

The volume $V$ of this parallelepiped equals the absolute value of the determinant of $A{:}$

$$
V = \left|\det(A)\right|
$$

- Now suppose the columns of a $2\times 2$ matrix $B$ are ${\color{black}\mathbf{p}}$ and ${\color{black}\mathbf{q}}.$
$$
B = {\left[ \begin{array}{cc}{\color{black}|} & {\color{black}|} \\ {\color{black}\mathbf{p}} & {\color{black}\mathbf{q}} \\ {\color{black}|} & {\color{black}|}\end{array} \right]}
$$
The $2$-dimensional parallelepiped (i.e., the parallelogram) spanned by vectors $\mathbf{p}$ and $\mathbf{q}$ is shown below:

![](images/4a/4af1971404b188df75bb3d62d47ac95340c5e1791066e5358370d743230baa45.png)

The two-dimensional volume $V$ (i.e., the area) of this parallelepiped equals the absolute value of the determinant of $B{:}$

$$
V = \left|\det(B)\right|
$$

- In general, the absolute value of the determinant of an $n\times n$ matrix $M$ gives the $n$-dimensional volume of the parallelepiped spanned by the columns of $M.$

In this lesson, we studied the following property:

*$\det(A) = 0$ if and only if one of the columns of $A$ is a linear combination of other columns of $A$.*

What does this property mean in geometric terms?

The component $\det(A) = 0$ implies that the $n$-dimensional parallelepiped formed by the columns of $A$ has zero volume. Conversely, when one of the columns of $A$ is a linear combination of other columns, it indicates that the corresponding parallelepiped possesses at most $n-1$ distinct dimensions. 

Consider the following examples:

- In the case of a $3$-dimensional parallelepiped, if the vector $\mathbf{c}$ is a linear combination of the vectors $\mathbf{a}$ and $\mathbf{b}$, then $\mathbf{c}$ lies within the plane containing $\mathbf{a}$ and $\mathbf{b}$. In other words, the vectors $\mathbf{a}$, $\mathbf{b}$, and $\mathbf{c}$ are coplanar. Consequently, we obtain a "flat" ($2$-dimensional) figure with a volume of $0$.

- For the parallelogram example, if the vector $\mathbf{q}$ is a linear combination of the vector $\mathbf{p}$ (i.e., $\mathbf{p}$ and $\mathbf{q}$ are proportional), then $\mathbf{q}$ resides on the line containing vector $\mathbf{p}$. In other words, the vectors $\mathbf{p}$ and $\mathbf{q}$ are collinear. This results in a $1$-dimensional object with a $2$-dimensional volume (i.e., area) of $0$.



### example 17592186133468 — Identifying the Reasons Why a Determinant Equals Zero

$$
A={\left[ \begin{array}{cccc}1 & 2 & 0 & - 1 \\ 3 & 6 & 0 & 1 \\ 2 & 4 & 0 & - 2 \\ 6 & 8 & 0 & 2\end{array} \right]}
$$

Consider the matrix given above. Identify **all** of the reasons why one can conclude that $|A|=0.$

I. $A$ has a zero column

II. $A$ has proportional rows

III. $A$ has identical columns

Let's examine each of the statements in turn.

- $A$ has a zero column: 
$$
A={\left[ \begin{array}{cccc}1 & 2 & {\color{blue}0} & - 1 \\ 3 & 6 & {\color{blue}0} & 1 \\ 2 & 4 & {\color{blue}0} & - 2 \\ 6 & 8 & {\color{blue}0} & 2\end{array} \right]}
$$

- $A$ has proportional rows: 
$$
A={\left[ \begin{array}{cccc}{\color{blue}1} & {\color{blue}2} & {\color{blue}0} & {\color{blue}- 1} \\ 3 & 6 & 0 & 1 \\ {\color{blue}2} & {\color{blue}4} & {\color{blue}0} & {\color{blue}- 2} \\ 6 & 8 & 0 & 2\end{array} \right]}
$$

- $A$ does *not* have identical columns.

Therefore, the correct answer is "I and II only."

## Representative practice (first three per skill; full bank in practice.json)

### Calculating the Determinant of a Matrix With A Zero Row/Column or Two Identical Rows/Columns (12 captured questions)

Question 17592186134395 — question.difficulty/easy

Find $2\det (A)+4\det (B)$, where 

$$
A=\begin{bmatrix}1 & 0 & \sqrt{3} & 1 \\ 0 & 2 & 4 & 2 \\ 0 & 0 & 2 & -4 \\ 0 & 0 & 0 & 1\end{bmatrix},\,B=\begin{bmatrix}3 & \sqrt{2} & 2 & 3 \\ 1 & 2 & 1 & 3 \\ 3 & 1 & 0 & \sqrt{2} \\ 1 & 2 & 1 & 3\end{bmatrix}.
$$

Solution: Let's examine each matrix in turn.

- Since $A$ is a triangular matrix, its determinant is given by the product of the elements of the main diagonal: 

$$
\det (A)=1\cdot 2\cdot 2\cdot 1=4
$$

- Since $B$ has two identical rows, we obtain

$$
B=\begin{bmatrix}3 & \sqrt{2} & 2 & 3 \\ 1 & 2 & 1 & 3 \\ 3 & 1 & 0 & \sqrt{2} \\ 1 & 2 & 1 & 3\end{bmatrix}\,⟹\,\det (B)=0.
$$

Therefore, $2\det (A)+4\det (B)=2\cdot 4+4\cdot 0=8.$

Answer selection: 8

Question 17592186134408 — question.difficulty/moderate

Which of the following determinants are equal to $0?$

$$
|A|=\begin{vmatrix}2 & 0 & 1 \\ \sqrt{5} & 0 & 4 \\ -1 & 0 & 0\end{vmatrix},\,|B|=\begin{vmatrix}3 & 0 & 0 \\ 0 & -1 & 0 \\ 0 & 0 & 5\end{vmatrix},\,|C|=\begin{vmatrix}4 & \sqrt{3} & 4 \\ 2 & 4 & 2 \\ 1 & \sqrt{5} & 1\end{vmatrix}
$$

Solution: Let's examine each of the given determinants in turn.

- The matrix $A$ has a zero column: 

$$
A=\begin{bmatrix}2 & {\color{blue}0} & 1 \\ \sqrt{5} & {\color{blue}0} & 4 \\ -1 & {\color{blue}0} & 0\end{bmatrix}
$$

As a result, $|A|=0.$

- Since $B$ is a diagonal matrix, we obtain 

$$
|B|=3\cdot (-1)\cdot 5=-15\ne 0.
$$

- The matrix $C$ has identical columns: 

$$
C=\begin{bmatrix}{\color{blue}4} & \sqrt{3} & {\color{blue}4} \\ {\color{blue}2} & 4 & {\color{blue}2} \\ {\color{blue}1} & \sqrt{5} & {\color{blue}1}\end{bmatrix}
$$

As a result, $|C|=0.$

Therefore, only $|A|$ and $|C|$ are equal to $0.$

Answer selection: $|A|$ and $|C|$ only

Question 17592186272009 — question.difficulty/easy

Find $\det (A)-3\det (B)$, where 

$$
A=\begin{bmatrix}2 & -2 & 2 & 2 \\ -1 & 1 & 0 & -1 \\ 1 & 1 & 1 & 1 \\ 3 & -3 & -3 & 3\end{bmatrix},\,B=\begin{bmatrix}3 & 4 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 2 & 3 & 1 & 0 \\ 1 & 2 & -3 & 1\end{bmatrix}.
$$

Solution: Let's examine each matrix in turn.

- Since $A$ has two identical columns, we obtain

$$
A=\begin{bmatrix}{\color{blue}2} & -2 & 2 & {\color{blue}2} \\ {\color{blue}-1} & 1 & 0 & {\color{blue}-1} \\ {\color{blue}1} & 1 & 1 & {\color{blue}1} \\ {\color{blue}3} & -3 & -3 & {\color{blue}3}\end{bmatrix}\hspace{2em}⟹\hspace{2em}\det (A)=0.
$$

- Since $B$ has a zero row, we obtain:

$$
B=\begin{bmatrix}3 & 4 & 0 & 0 \\ {\color{blue}0} & {\color{blue}0} & {\color{blue}0} & {\color{blue}0} \\ 2 & 3 & 1 & 0 \\ 1 & 2 & -3 & 1\end{bmatrix}\hspace{2em}⟹\hspace{2em}\det (B)=0.
$$

Therefore, $\det (A)-3\det (B)=0-3\cdot 0=0.$

Answer selection: 0

### Calculating the Determinant of a Matrix With Two Proportional Rows/Columns (12 captured questions)

Question 17592186134394 — question.difficulty/easy

Find $4\det (A)+4\det (B)$, where 

$$
A=\begin{bmatrix}2\sqrt{2} & 1 \\ 1 & \sqrt{2}\end{bmatrix},\,B=\begin{bmatrix}1 & \sqrt{2} & 2 \\ 2 & 1 & 4 \\ 3 & 6 & 6\end{bmatrix}.
$$

Solution: Let's examine each matrix in turn.

- For the matrix $A,$ we have

$$
\det (A)=2\sqrt{2}\cdot \sqrt{2}-1\cdot 1=3.
$$

- Since $B$ has proportional columns, we obtain

$$
B=\begin{bmatrix}{\color{blue}1} & \sqrt{2} & {\color{blue}2} \\ {\color{blue}2} & 1 & {\color{blue}4} \\ {\color{blue}3} & 6 & {\color{blue}6}\end{bmatrix}\hspace{2em}⟹\hspace{2em}\det (B)=0.
$$

Therefore, $4\det (A)+4\det (B)=4\cdot 3+4\cdot 0=12.$

Answer selection: 12

Question 17592186134407 — question.difficulty/moderate

Which of the following determinants are equal to $0?$

$$
|A|=\begin{vmatrix}2 & -1 & \sqrt{3} \\ \sqrt[5]{2} & 1 & 4 \\ 0 & 0 & 0\end{vmatrix},\,|B|=\begin{vmatrix}1 & \sqrt{2} & 4 \\ 0 & 3 & 6 \\ 0 & 0 & 4\end{vmatrix},\,|C|=\begin{vmatrix}1 & \sqrt{2} & 4 \\ 2 & 3 & 8 \\ 1 & 0 & 4\end{vmatrix}
$$

Solution: Let's examine each of the given determinants in turn.

- The matrix $A$ has a zero row: 

$$
A=\begin{bmatrix}2 & -1 & \sqrt{3} \\ \sqrt[5]{2} & 1 & 4 \\ {\color{blue}0} & {\color{blue}0} & {\color{blue}0}\end{bmatrix}
$$

As a result, $|A|=0.$

- The matrix $B$ is a triangular matrix, hence 

$$
|B|=1\cdot 3\cdot 4=12\ne 0.
$$

- The matrix $C$ has proportional columns: 

$$
C=\begin{bmatrix}{\color{blue}1} & \sqrt{2} & {\color{blue}4} \\ {\color{blue}2} & 3 & {\color{blue}8} \\ {\color{blue}1} & 0 & {\color{blue}4}\end{bmatrix}
$$

As a result, $|C|=0.$

Therefore, only $|A|$ and $|C|$ are equal to $0.$

Answer selection: $|A|$ and $|C|$ only

Question 17592186272011 — question.difficulty/easy

Find $\det (A)-2\det (B)$, where 

$$
A=\begin{bmatrix}1 & 0 & 1 & -1 \\ 0 & 2 & 1 & 3 \\ -2 & 0 & -2 & 2 \\ 2 & 1 & 0 & 1\end{bmatrix},\,B=\begin{bmatrix}-1 & 0 & 0 \\ 2 & 1 & 0 \\ 4 & -1 & 3\end{bmatrix}.
$$

Solution: Let's examine each matrix in turn.

- Since $A$ has proportional rows, we obtain

$$
A=\begin{bmatrix}{\color{blue}1} & {\color{blue}0} & {\color{blue}1} & {\color{blue}-1} \\ 0 & 2 & 1 & 3 \\ {\color{blue}-2} & {\color{blue}0} & {\color{blue}-2} & {\color{blue}2} \\ 2 & 1 & 0 & 1\end{bmatrix}\hspace{2em}⟹\hspace{2em}\det (A)=0.
$$

- Since $B$ is a triangular matrix, we obtain

$$
|B|=-1\cdot 1\cdot 3=-3
$$

Therefore, $\det (A)-2\det (B)=0-2\cdot (-3)=6.$

Answer selection: 6

### Identifying the Reasons Why a Determinant Equals Zero (12 captured questions)

Question 17592186134393 — question.difficulty/moderate

$$
A=\begin{bmatrix}2 & 0 & 4 \\ 1 & 0 & 3 \\ 2 & 0 & 4\end{bmatrix}
$$

Consider the matrix given above. Identify **all** of the reasons why one can conclude that $|A|=0?$

Select all that apply.

Solution: Let's examine each of the statements in turn.

- $A$ has a zero column: 

$$
A=\begin{bmatrix}2 & 0 & 4 \\ 1 & 0 & 3 \\ 2 & 0 & 4\end{bmatrix}\,✓
$$

- $A$ does *not* have identical columns.

- $A$ has identical rows: 

$$
A=\begin{bmatrix}2 & 0 & 4 \\ 1 & 0 & 3 \\ 2 & 0 & 4\end{bmatrix}.\,✓
$$

Therefore, the correct answer is “$A$ has a zero column”; “$A$ has identical rows” only.

Answer $A$ has a zero column: true

Answer $A$ has identical columns: false

Answer $A$ has identical rows: true

Question 17592186134414 — question.difficulty/hard

Let $A$ be a $2\times 2$ matrix such that $|A|=0.$ Which of the following statements must be true?

Select all that apply.

Solution: Let's consider our statements in turn.

- Statements “$A$ has two identical rows” and “$A$ has two identical columns” are false. For example, consider the matrix 

$$
A=\begin{bmatrix}1 & 4 \\ 2 & 8\end{bmatrix}.
$$

We have that 

$$
|A|=1\cdot 8-4\cdot 2=0
$$

but $A$ has neither two identical rows nor two identical columns.

- Statement “One of the rows/columns of $A$ is proportional to another row/column of $A$” is true. Indeed, we can make use of the following fact:

$|A|=0$ *if and only if one of the rows/columns of $A$ is a linear combination of other rows/columns of $A.$*

In the case of a $2\times 2$ matrix, this means that one of the rows/columns must be proportional to another row/column.

Therefore, the correct answer is “One of the rows/columns of $A$ is proportional to another row/column of $A$” only.

Answer $A$ has two identical columns: false

Answer $A$ has two identical rows: false

Answer One of the rows/columns of $A$ is proportional to another row/column of $A$: true

Question 17592186272012 — question.difficulty/hard

Let $A$ be a $2\times 2$ matrix such that $|A|\ne 0.$ Which of the following statements must be true?

Select all that apply.

Solution: Let's consider our statements in turn.

- Statement “$A$ is a triangular matrix” is false. For example, consider the matrix 

$$
A=\begin{bmatrix}1 & -2 \\ 2 & 1\end{bmatrix}.
$$

We have that 

$$
|A|=1\cdot 1-(-2)\cdot 2=5\ne 0
$$

but $A$ is not a triangular matrix.

- Statements “$A$ does not have identical rows” and “$A$ does not have proportional columns” are true. Indeed, we can make use of the following fact:

$|A|=0$ *if and only if one of the rows/columns of $A$ is a linear combination of other rows/columns of $A.$*

In the case of a $2\times 2$ matrix, this means that one of the rows/columns must be proportional to another row/column.
Hence, if $|A|\ne 0$ then $A$ doesn't have proportional nor identical rows/columns.

Therefore, the correct answer is “$A$ does not have identical rows”; “$A$ does not have proportional columns” only.

Answer $A$ does not have identical rows: true

Answer $A$ does not have proportional columns: true

Answer $A$ is a triangular matrix: false

Answer None of the above: false
