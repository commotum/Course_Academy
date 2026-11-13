# 17592186049159 Basic Properties of Determinants

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186121130 — Introduction

There are some special matrices for which we can compute the determinants without doing so many computations. This is the case for triangular or diagonal matrices. 

For example, let's consider the following matrices:

$$
I =
\begin{bmatrix}1 & {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{0}} \\ {\color{blue}{0}} & 1 & {\color{blue}{0}} & {\color{blue}{0}} \\ {\color{blue}{0}} & {\color{blue}{0}} & 1 & {\color{blue}{0}} \\ {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{0}} & 1\end{bmatrix}\!,\quad
	A =
\begin{bmatrix}4 & 195 & \sqrt{2} & -14 \\ {\color{blue}{0}} & 2 & -98 & 12 \\ {\color{blue}{0}} & {\color{blue}{0}} & -3 & 9 \\ {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{0}} & -1\end{bmatrix}\!,\quad
	B =
\begin{bmatrix}3 & {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{0}} \\ {\color{blue}{0}} & 2 & {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{0}} \\ {\color{blue}{0}} & {\color{blue}{0}} & 4 & {\color{blue}{0}} & {\color{blue}{0}} \\ {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{0}} & 1 & {\color{blue}{0}} \\ {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{0}} & -2\end{bmatrix}\!.
$$

To quickly compute the determinants of the matrices above, we can use the following three basic properties of determinants:

I. - The determinant of an $n\!\times\!n$ identity matrix is equal to $1$. So, 

$$
\det(I) = 1.
$$
II. - The determinant of a triangular or diagonal matrix is equal to the product of the entries on the main diagonal. So, 

$$
\begin{aligned}\det (A) & =4\cdot 2\cdot (-3)\cdot (-1)=24, \\ \det (B) & =3\cdot 2\cdot 4\cdot 1\cdot (-2)=-48.\end{aligned}
$$
III. - The determinant of $A^T$, the transpose of $A$, is the same as the determinant of $A$: 

$$
\det(A^T)=\det(A)
$$



### example 17592186119503 — Finding the Determinant of a Triangular Matrix

Calculate 
$$
{\left| \begin{array}{cccc}- 2 & 0 & 0 & 0 \\ - 4 & 1 & 0 & 0 \\ 1 & 10 & \sqrt{3} & 0 \\ - 3 & 0 & 6 & - 2\end{array} \right|}.
$$

The determinant of a triangular matrix is equal to the product of the entries on the main diagonal. Therefore, we have

$$
\begin{aligned}\begin{vmatrix}-2 & {\color{blue}{0}} & {\color{blue}{0}} & {\color{blue}{0}} \\ -4 & 1 & {\color{blue}{0}} & {\color{blue}{0}} \\ 1 & 10 & \sqrt{3} & {\color{blue}{0}} \\ -3 & 0 & 6 & -2\end{vmatrix} & =(-2)\cdot 1\cdot \sqrt{3}\cdot (-2)=4\sqrt{3}.\end{aligned}
$$

### example 17592186119504 — Calculating the Determinant of a Matrix With Many Zeros

Find the determinant of the matrix 
$$
A=
{\left[ \begin{array}{cccc}2 & 5 & 5 & 4 \\ 0 & 1 & 0 & 0 \\ 0 & 8 & 2 & 0 \\ 0 & 13 & 19 & - 3\end{array} \right]}.
$$

Notice that the $1$st column contains three zeros. So, using Laplace expansion along the $1$st column, we have

$$
\begin{aligned}\det (A) & =\begin{vmatrix}2 & {\color{lightgray}{5}} & {\color{lightgray}{5}} & {\color{lightgray}{4}} \\ {\color{lightgray}{0}} & 1 & 0 & 0 \\ {\color{lightgray}{0}} & 8 & 2 & 0 \\ {\color{lightgray}{0}} & 13 & 19 & -3\end{vmatrix} \\  & =2\cdot (-1)^{1+1}\begin{vmatrix}1 & 0 & 0 \\ 8 & 2 & 0 \\ 13 & 19 & -3\end{vmatrix} \\  & =2\begin{vmatrix}1 & 0 & 0 \\ 8 & 2 & 0 \\ 13 & 19 & -3\end{vmatrix}.\end{aligned}
$$

The determinant of a triangular matrix is equal to the product of the entries on the main diagonal. Therefore, we have

$$
\begin{aligned}\begin{vmatrix}1 & 0 & 0 \\ 8 & 2 & 0 \\ 13 & 19 & -3\end{vmatrix} & =1\cdot 2\cdot (-3)=-6.\end{aligned}
$$

Finally, we obtain

$$
\det(A) = 2 \cdot (-6) = -12.
$$

### tutorial 17592186121131 — Determinants as Volumes

Geometrically, the absolute value of an $n \times n$ determinant can be interpreted as the volume of the $n$-dimensional parallelepiped spanned by the columns of the matrix. For example:

- The parallelogram (a.k.a. $2$-dimensional parallelepiped) spanned by the two-dimensional vectors $\mathbf{p}$ and $\mathbf{q}$ is depicted below:

![](images/c5/c538736c09cab15b58d7318c9c2361b2ae08e03b0f15231736d4b7b47f08ec59.png)

The volume of this parallelogram is 

$$
V = \left| \:\:
\det
\begin{bmatrix}\hspace{0.222em}\hspace{0.222em}| & |\hspace{0.222em}\hspace{0.222em} \\ \hspace{0.222em}\hspace{0.222em}\mathbf{p} & \mathbf{q}\hspace{0.222em}\hspace{0.222em} \\ \hspace{0.222em}\hspace{0.222em}| & |\hspace{0.222em}\hspace{0.222em}\end{bmatrix} 
\:\: \right|.
$$

- The $3$-dimensional parallelepiped spanned by the three-dimensional vectors $\mathbf{a},$ $\mathbf{b},$ and $\mathbf{c}$ is depicted below:

![](images/7a/7ae38eb9a0d8e7a68b23dc40513f0c813cebf72c2bf839b196fd251d619b702b.png)

The volume of this parallelepiped is

$$
V = \left| \:\:
\det
\begin{bmatrix}\hspace{0.222em}\hspace{0.222em}| & | & |\hspace{0.222em}\hspace{0.222em} \\ \hspace{0.222em}\hspace{0.222em}\mathbf{a} & \mathbf{b} & \mathbf{c}\hspace{0.222em}\hspace{0.222em} \\ \hspace{0.222em}\hspace{0.222em}| & | & |\hspace{0.222em}\hspace{0.222em}\end{bmatrix} 
\:\: \right|.
$$

It's much harder to draw a $4$-dimesional parallelepiped that is spanned by the four-dimensional vectors $\mathbf{a}_1,$ $\mathbf{a}_2,$ $\mathbf{a}_3,$ and $\mathbf{a}_4.$ However, we can define its volume similar to the ones above. It will be equal to the absolute value of the corresponding determinant:

$$
V = \left| \:\:
\det
\begin{bmatrix}\hspace{0.222em}\hspace{0.222em}| & | & | & |\hspace{0.222em}\hspace{0.222em} \\ \hspace{0.222em}\hspace{0.222em}{\mathbf{a}}_{1} & {\mathbf{a}}_{2} & {\mathbf{a}}_{3} & {\mathbf{a}}_{4}\hspace{0.222em}\hspace{0.222em} \\ \hspace{0.222em}\hspace{0.222em}| & | & | & |\hspace{0.222em}\hspace{0.222em}\end{bmatrix} 
\:\: \right|
$$

Volumes for parallelepipeds of higher dimensions are defined analogously.



### example 17592186119506 — Computing the Volume of an N-Dimensional Parallelepiped

Calculate the volume of the $4$-dimensional parallelepiped spanned by the vectors

$$
\mathbf{a}=
{\left[ \begin{array}{c}2 \\ 3 \\ - 4 \\ 5\end{array} \right]}, \quad
\mathbf{b}=
{\left[ \begin{array}{c}3 \\ 0 \\ 0 \\ - 4\end{array} \right]}, \quad
\mathbf{c}=
{\left[ \begin{array}{c}- 2 \\ 0 \\ 1 \\ 2\end{array} \right]}, \quad
\mathbf{d}=
{\left[ \begin{array}{c}1 \\ 0 \\ 0 \\ 5\end{array} \right]}.
$$

First, let's construct the matrix $M,$ whose columns are the coordinates of our vectors $\mathbf{a},$ $\mathbf{b},$ $\mathbf{c},$ and  $\mathbf{d}{:}$

$$
M =
{\left[ \begin{array}{cccc}2 & 3 & - 2 & 1 \\ 3 & 0 & 0 & 0 \\ - 4 & 0 & 1 & 0 \\ 5 & - 4 & 2 & 5\end{array} \right]}
$$

The volume of the parallelepiped spanned by these vectors equals the absolute value of the determinant of $M{:}$

$$
V = | \det(M) |
$$

Notice that the $2$nd row of the determinant contains three zeros. So, using Laplace expansion along the $2$nd row, we have

$$
\begin{aligned}\det (M) & =\begin{vmatrix}{\color{lightgray}{2}} & 3 & -2 & 1 \\ 3 & {\color{lightgray}{0}} & {\color{lightgray}{0}} & {\color{lightgray}{0}} \\ {\color{lightgray}{-4}} & 0 & 1 & 0 \\ {\color{lightgray}{5}} & -4 & 2 & 5\end{vmatrix} \\  & =3\cdot (-1)^{2+1}\begin{vmatrix}3 & -2 & 1 \\ 0 & 1 & 0 \\ -4 & 2 & 5\end{vmatrix} \\  & =-3\begin{vmatrix}3 & -2 & 1 \\ 0 & 1 & 0 \\ -4 & 2 & 5\end{vmatrix}.\end{aligned}
$$

Now, notice that the $2$nd row of the $3 \times 3$ determinant contains two zeros. So, using Laplace expansion along the $2$nd row, we have

$$
\begin{aligned}\det (M) & =-3\begin{vmatrix}3 & {\color{lightgray}{-2}} & 1 \\ {\color{lightgray}{0}} & 1 & {\color{lightgray}{0}} \\ -4 & {\color{lightgray}{2}} & 5\end{vmatrix} \\  & =-3\cdot 1\cdot (-1)^{2+2}\begin{vmatrix}3 & 1 \\ -4 & 5\end{vmatrix} \\  & =-3\begin{vmatrix}3 & 1 \\ -4 & 5\end{vmatrix} \\  & =-3(15+4) \\  & =-57.\end{aligned}
$$

Therefore, the volume is

$$
V = | \det(M) | = |-57| = 57.
$$

### example 17592186119505 — Calculating an Expression Involving Given Determinants and Matrix Types

Given that $\det(A)=4,$ which of the following statements are true?

- $\textrm{det}(A^T)=16$

- $3\textrm{det}(A^T)=12$

- $\textrm{det}(A^T)+\textrm{det}(I)=17$

From the properties of determinants, we know that 

$$
\textrm{det}(A^T)=\textrm{det}(A)=4
$$

and

$$
\textrm{det}(I)=1.
$$

With that in mind, let's analyze each statement in turn.

- Statement I is false. Rather, 

$$
\textrm{det}(A^T)=4 \neq 16.
$$

- Statement II is true. Indeed,

$$
3\textrm{det}(A^T)= 3 \cdot 4 = 12.
$$

- Statement III is false. We have

$$
\textrm{det}(A^T)+\textrm{det}(I)= 4 + 1 = 5 \neq 17.
$$

In conclusion, the correct answer is "II only".

## Representative practice (first three per skill; full bank in practice.json)

### Finding the Determinant of a Triangular Matrix (26 captured questions)

Question 17592186120428 — None

Given that $A =-3I$, where $I$ is the $3 \times 3$ identity matrix, what is the value of $\det (A)$?

Solution: The matrix $A=-3I_3$ is diagonal. The determinant of a triangular matrix is the product of its diagonal entries, so $\det(A)=(-3)(-3)(-3)=-27$.

Answer selection: -27

Question 17592186120444 — None

What is $$
\displaystyle \begin{vmatrix}2 & -4 & \sqrt{2} & 0.5 \\ 0 & 5 & -2 & \sqrt{3} \\ 0 & 0 & -1 & 10 \\ 0 & 0 & 0 & 5\end{vmatrix}
$$?

Solution: The determinant of a triangular matrix is the product of its diagonal entries. Therefore, the determinant is $2\cdot5\cdot(-1)\cdot5=-50$.

Answer selection: -50

Question 17592186265827 — question.difficulty/easy

Given that $E=5I$, where $I$ is the $3\times 3$ identity matrix, what is the value of $\det (E)?$

Solution: First, notice that

$$
\begin{aligned}5I & =5\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}=\begin{bmatrix}5 & 0 & 0 \\ 0 & 5 & 0 \\ 0 & 0 & 5\end{bmatrix}.\end{aligned}
$$

The determinant of a diagonal matrix is equal to the product of the entries on the main diagonal. Therefore, we have

$$
\begin{aligned}\begin{vmatrix}5 & 0 & 0 \\ 0 & 5 & 0 \\ 0 & 0 & 5\end{vmatrix} & =5\cdot 5\cdot 5=125.\end{aligned}
$$

Answer selection: 125

### Calculating the Determinant of a Matrix With Many Zeros (31 captured questions)

Question 17592186120429 — question.difficulty/moderate

Find the determinant of the matrix 
$$
\displaystyle B=\begin{bmatrix}3 & 0 & 0 & 0 \\ 3 & 1 & 0 & 0 \\ 5 & 11 & 1 & 19 \\ 4 & 0 & 0 & -3\end{bmatrix}.
$$

Solution: Notice that the $3$rd column contains three zeros. So, using Laplace expansion along the $3$rd column, we have

$$
\begin{aligned}\det (B) & =\begin{vmatrix}3 & 0 & {\color{lightgray}{0}} & 0 \\ 3 & 1 & {\color{lightgray}{0}} & 0 \\ {\color{lightgray}{5}} & {\color{lightgray}{11}} & 1 & {\color{lightgray}{19}} \\ 4 & 0 & {\color{lightgray}{0}} & -3\end{vmatrix} \\  & =1\cdot (-1)^{3+3}\begin{vmatrix}3 & 0 & 0 \\ 3 & 1 & 0 \\ 4 & 0 & -3\end{vmatrix} \\  & =\begin{vmatrix}3 & 0 & 0 \\ 3 & 1 & 0 \\ 4 & 0 & -3\end{vmatrix}\end{aligned}
$$

The determinant of a triangular matrix is equal to the product of the entries on the main diagonal. Therefore, we have

$$
\begin{aligned}\begin{vmatrix}3 & 0 & 0 \\ 3 & 1 & 0 \\ 4 & 0 & -3\end{vmatrix} & =3\cdot 1\cdot (-3)=-9.\end{aligned}
$$

Finally, we obtain

$$
\det (B)=-9.
$$

Answer selection: -9

Question 17592186120445 — None

Find the determinant of the matrix
$$
\displaystyle A = \begin{bmatrix}1 & 1 & 1 & 2 \\ 2 & -1 & 4 & 2 \\ 0 & 2 & 0 & 0 \\ 1 & 5 & 0 & 0\end{bmatrix}.
$$

Solution: The third row contains three zeros, so expand along that row:

$$
\det(A)=2(-1)^{3+2}\begin{vmatrix}1&1&2\\2&4&2\\1&0&0\end{vmatrix}
=-2\begin{vmatrix}1&2\\4&2\end{vmatrix}
=-2(2-8)=12.
$$

Answer selection: 12

Question 17592186265875 — question.difficulty/moderate

Find the determinant of the matrix 
$$
\displaystyle B=\begin{bmatrix}5 & 0 & 0 & 0 \\ 2 & 6 & 0 & 0 \\ -4 & 1 & 2 & 8 \\ 9 & 0 & 0 & -1\end{bmatrix}.
$$

Solution: Notice that the $3$rd column contains three zeros. So, using Laplace expansion along the $3$rd column, we have

$$
\begin{aligned}\det (B) & =\begin{vmatrix}5 & 0 & {\color{lightgray}{0}} & 0 \\ 2 & 6 & {\color{lightgray}{0}} & 0 \\ {\color{lightgray}{-4}} & {\color{lightgray}{1}} & 2 & {\color{lightgray}{8}} \\ 9 & 0 & {\color{lightgray}{0}} & -1\end{vmatrix} \\  & =2\cdot (-1)^{3+3}\begin{vmatrix}5 & 0 & 0 \\ 2 & 6 & 0 \\ 9 & 0 & -1\end{vmatrix} \\  & =2\cdot \begin{vmatrix}5 & 0 & 0 \\ 2 & 6 & 0 \\ 9 & 0 & -1\end{vmatrix}\end{aligned}
$$

The determinant of a triangular matrix is equal to the product of the entries on the main diagonal. Therefore, we have

$$
\begin{aligned}2\cdot \begin{vmatrix}5 & 0 & 0 \\ 2 & 6 & 0 \\ 9 & 0 & -1\end{vmatrix} & =2\cdot 5\cdot 6\cdot (-1)=-60.\end{aligned}
$$

Finally, we obtain

$$
\det (B)=-60.
$$

Answer selection: -60

### Computing the Volume of an N-Dimensional Parallelepiped (27 captured questions)

Question 17592186120154 — None

Calculate the volume of the $4$-dimensional parallelepiped spanned by the vectors

$$
\mathbf{a}=\begin{bmatrix}2 \\ 0 \\ -1 \\ 3\end{bmatrix},\hspace{1em}\mathbf{b}=\begin{bmatrix}1 \\ -1 \\ 1 \\ 2\end{bmatrix},\hspace{1em}\mathbf{c}=\begin{bmatrix}-2 \\ 0 \\ 3 \\ 0\end{bmatrix},\hspace{1em}\mathbf{d}=\begin{bmatrix}1 \\ 0 \\ -2 \\ 0\end{bmatrix}.
$$

Solution: Construct the matrix $M$ whose columns are $a,b,c,d$. The volume equals $|\det(M)|$.

$$
\det(M)=\begin{vmatrix}2&1&-2&1\\0&-1&0&0\\-1&1&3&-2\\3&2&0&0\end{vmatrix}
=-\begin{vmatrix}2&-2&1\\-1&3&-2\\3&0&0\end{vmatrix}
=-3\begin{vmatrix}-2&1\\3&-2\end{vmatrix}=-3(4-3)=-3.
$$

Therefore, the volume is $|-3|=3$.

Answer selection: 3

Question 17592186120155 — question.difficulty/easy

Calculate the volume of the $4$-dimensional parallelepiped spanned by the vectors

$$
\mathbf{a}=\begin{bmatrix}5 \\ -1 \\ 3 \\ 1\end{bmatrix},\hspace{1em}\mathbf{b}=\begin{bmatrix}0 \\ 2 \\ -3 \\ 1\end{bmatrix},\hspace{1em}\mathbf{c}=\begin{bmatrix}0 \\ 0 \\ 3 \\ -1\end{bmatrix},\hspace{1em}\mathbf{d}=\begin{bmatrix}0 \\ 0 \\ 0 \\ -1\end{bmatrix}.
$$

Solution: First, let's construct the matrix $M,$ whose columns are the coordinates of our vectors $\mathbf{a},$ $\mathbf{b},$ $\mathbf{c},$ and  $\mathbf{d}:$

$$
M=\begin{bmatrix}5 & 0 & 0 & 0 \\ -1 & 2 & 0 & 0 \\ 3 & -3 & 3 & 0 \\ 1 & 1 & -1 & -1\end{bmatrix}
$$

The volume of the parallelepiped spanned by these vectors equals the absolute value of the determinant of $M:$

$$
V=|\det (M)|
$$

The determinant of a triangular matrix is equal to the product of the entries on the main diagonal. So, we have

$$
\det (M)=\begin{bmatrix}5 & 0 & 0 & 0 \\ -1 & 2 & 0 & 0 \\ 3 & -3 & 3 & 0 \\ 1 & 1 & -1 & -1\end{bmatrix}=5\cdot 2\cdot 3\cdot (-1)=-30.
$$

Therefore, the volume is

$$
V=|\det (M)|=|-30|=30.
$$

Answer selection: 30

Question 17592186275444 — question.difficulty/easy

Calculate the volume of the $4$-dimensional parallelepiped spanned by the vectors

$$
\mathbf{a}=\begin{bmatrix}4 \\ 0 \\ 0 \\ 0\end{bmatrix},\hspace{1em}\mathbf{b}=\begin{bmatrix}3 \\ -1 \\ 0 \\ 0\end{bmatrix},\hspace{1em}\mathbf{c}=\begin{bmatrix}7 \\ 2 \\ -3 \\ 0\end{bmatrix},\hspace{1em}\mathbf{d}=\begin{bmatrix}13 \\ -9 \\ 4 \\ 2\end{bmatrix}.
$$

Solution: First, let's construct the matrix $M,$ whose columns are the coordinates of our vectors $\mathbf{a},$ $\mathbf{b},$ $\mathbf{c},$ and  $\mathbf{d}:$

$$
M=\begin{bmatrix}4 & 3 & 7 & 13 \\ 0 & -1 & 2 & -9 \\ 0 & 0 & -3 & 4 \\ 0 & 0 & 0 & 2\end{bmatrix}
$$

The volume of the parallelepiped spanned by these vectors equals the absolute value of the determinant of $M:$

$$
V=|\det (M)|
$$

The determinant of a triangular matrix is equal to the product of the entries on the main diagonal. So, we have

$$
\det (M)=\begin{bmatrix}4 & 3 & 7 & 13 \\ 0 & -1 & 2 & -9 \\ 0 & 0 & -3 & 4 \\ 0 & 0 & 0 & 2\end{bmatrix}=4\cdot (-1)\cdot (-3)\cdot 2=24.
$$

Therefore, the volume is

$$
V=|\det (M)|=|24|=24.
$$

Answer selection: 24

### Calculating an Expression Involving Given Determinants and Matrix Types (26 captured questions)

Question 17592186120427 — question.difficulty/moderate

Given that $\det ({A}^{T})=5$, which of the following statements are true?

Select all that apply.

Solution: From the properties of determinants, we know that 

$$
\text{det}(A)=\text{det}({A}^{T})=5
$$

and

$$
\det (I)=1.
$$

With that in mind, let's analyze each statement in turn.

- Statement $4\text{det}(A)=20$ is true. Indeed,

$$
4\text{det}(A)=4\cdot 5=20.
$$

- Statement $2\text{det}({A}^{T})=25$ is false. We have

$$
2\text{det}({A}^{T})=2\cdot 5=10\ne 25.
$$

- Statement $\text{det}(A)-3\text{det}(I)=8$ is false. We have

$$
\text{det}(A)-3\text{det}(I)=5-3\cdot 1=2\ne 8.
$$

In conclusion, the correct answer is $4\text{det}(A)=20$ only.

Answer $2\text{det}({A}^{T})=25$: false

Answer $4\text{det}(A)=20$: true

Answer $\text{det}(A)-3\text{det}(I)=8$: false

Answer None of the above: false

Question 17592186120430 — question.difficulty/hard

Given that $A=-2I$, where $I$ is the $4\times 4$ identity matrix, which of the following statements are true?

Select all that apply.

Solution: First, notice that

$$
\begin{aligned}-2I & =-2\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix}=\begin{bmatrix}-2 & 0 & 0 & 0 \\ 0 & -2 & 0 & 0 \\ 0 & 0 & -2 & 0 \\ 0 & 0 & 0 & -2\end{bmatrix}.\end{aligned}
$$

The determinant of a diagonal matrix is equal to the product of the entries on the main diagonal. Therefore, we have

$$
\begin{aligned}\begin{vmatrix}-2 & 0 & 0 & 0 \\ 0 & -2 & 0 & 0 \\ 0 & 0 & -2 & 0 \\ 0 & 0 & 0 & -2\end{vmatrix} & =(-2)^{4}=16.\end{aligned}
$$

From the properties of determinants, we know that 

$$
\text{det}({A}^{T})=\text{det}(A)=16
$$

and

$$
\text{det}(I)=1.
$$

With that in mind, let's analyze each statement in turn.

- Statement $\text{det}(A)+16\text{det}(I)=0$ is false. We have

$$
\text{det}(A)+16\text{det}(I)=16+16=32\ne 0.
$$

- Statement $\text{det}(I)=-8$ is false. Rather,

$$
\text{det}(I)=1.
$$

- Statement $\text{det}({A}^{T})=-16$ is false. We have

$$
\text{det}({A}^{T})=\text{det}(A)=16\ne -16.
$$

In conclusion, none of the statements is true.

Answer $\text{det}(A)+16\text{det}(I)=0$: false

Answer $\text{det}(I)=-8$: false

Answer $\text{det}({A}^{T})=-16$: false

Answer None of the above: true

Question 17592186265885 — question.difficulty/hard

Given that $K=-3I$, where $I$ is the $4\times 4$ identity matrix, which of the following statements are true?

Select all that apply.

Solution: First, notice that

$$
\begin{aligned}-3I & =\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix}=\begin{bmatrix}-3 & 0 & 0 & 0 \\ 0 & -3 & 0 & 0 \\ 0 & 0 & -3 & 0 \\ 0 & 0 & 0 & -3\end{bmatrix}.\end{aligned}
$$

The determinant of a diagonal matrix is equal to the product of the entries on the main diagonal. Therefore, we have

$$
\begin{aligned}\begin{vmatrix}-3 & 0 & 0 & 0 \\ 0 & -3 & 0 & 0 \\ 0 & 0 & -3 & 0 \\ 0 & 0 & 0 & -3\end{vmatrix} & =(-3)^{4}=81.\end{aligned}
$$

From the properties of determinants, we know that 

$$
\text{det}({K}^{T})=\text{det}(K)=81
$$

and

$$
\text{det}(I)=1.
$$

With that in mind, let's analyze each statement in turn.

- Statement $\text{det}(K)-9\text{det}(I)=0$ is false. We have

$$
\text{det}(K)-9\text{det}(I)=81-9=72\ne 0.
$$

- Statement $\text{det}(I)=81$ is false. Rather,

$$
\text{det}(I)=1.
$$

- Statement $\text{det}({K}^{T})=-3$ is false. We have

$$
\text{det}({K}^{T})=\text{det}(K)=81\ne -3.
$$

In conclusion, none of the statements is true.

Answer $\text{det}(I)=81$: false

Answer $\text{det}(K)-9\text{det}(I)=0$: false

Answer $\text{det}({K}^{T})=-3$: false

Answer None of the above: true
