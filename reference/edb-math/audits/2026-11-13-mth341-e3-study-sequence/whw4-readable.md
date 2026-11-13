# MTH 341 — WHW-4

Captured basis: 14416

## 17592186702497 Assignment information

**MTH 341 — Written Homework 4**

Due: 2026-10-28
Due time: 11:59 p.m. PDT
Deadline source: [Fall 2026 Canvas assignment](https://canvas.oregonstate.edu/courses/2064363/assignments/10695097), checked 2026-10-25 (Wednesday, October 28).
Date imported: 2026-10-25
Source: [341-WHW-4.pdf](/api/source?path=%2Fhome%2Fjake%2FDeveloper%2Fstudy%2Fvault%2FF26%2Fsource%2F341%2FWHW-4%2F341-WHW-4.pdf)
Textbook: [A First Course in Linear Algebra, Version 2017 — Revision A](/api/source?path=%2Fhome%2Fjake%2FDeveloper%2Fstudy%2Fvault%2FF26%2Fsource%2F341%2FKuttler-LinearAlgebra-AFirstCourse-2017A.pdf), Lyryx Learning, based on K. Kuttler (CC BY).

Study answers and worked explanations are independently authored additions. The current deadline comes from Fall 2026 Canvas; historical Spring dates extracted from the assignment PDF do not determine this deadline. Textbook exercise identifiers resolve two inaccurate page references on the assignment sheet.

## Instructions

- Complete all 13 assigned exercises, including all parts of Exercise 3.1.1 and only part (b) of Exercise 3.1.3.
- Calculate Problems 1 and 2 **by hand, without technology**. Technology may be used to row reduce matrices elsewhere unless the problem specifies a method. Problem 8 specifically requires row operations to simplify the determinant first.
- Show all work and write neatly. Put solutions on separate 8.5-by-11-inch or A4 sheets, using the assignment sheet as the cover. Canvas also allows handwritten work scanned to PDF or typeset work. Submit one PDF to Canvas by the deadline; late homework is not accepted.
- The assignment points to the definition of a linear combination on textbook pages 30 and 151, and to Week 2 lecture Problems 6–7 for §§1.2.3–1.2.4. A linear combination of vectors is a sum of scalar multiples of those vectors.
- The Canvas rubric assigns 8 points for completion and 2 points for correctly solving Problem 4 (Exercise 3.1.12).



## 17592186702688 Practice

Source exercise: 3.1.1(a–c), textbook printed page 126 (PDF page 138).

**(a)** Find the determinant of $\begin{bmatrix}1&3\\0&2\end{bmatrix}$ **by hand, without technology**. Show your calculation.

Determinant: {{answer}}.

$1(2)-3(0)=2$. For a $2\times2$ matrix, $\det\begin{bmatrix}a&b\\c&d\end{bmatrix}=ad-bc$. Apply the subtraction in that order.

REFERENCE ANSWER
2

## 17592186702532 Practice

Source exercise: 3.1.1(a–c), textbook printed page 126 (PDF page 138).

**(b)** Find the determinant of $\begin{bmatrix}0&3\\0&2\end{bmatrix}$ **by hand, without technology**. Show your calculation.

Determinant: {{answer}}.

$0(2)-3(0)=0$. For a $2\times2$ matrix, $\det\begin{bmatrix}a&b\\c&d\end{bmatrix}=ad-bc$. Apply the subtraction in that order.

REFERENCE ANSWER
0

## 17592186702677 Practice

Source exercise: 3.1.1(a–c), textbook printed page 126 (PDF page 138).

**(c)** Find the determinant of $\begin{bmatrix}4&3\\6&2\end{bmatrix}$ **by hand, without technology**. Show your calculation.

Determinant: {{answer}}.

$4(2)-3(6)=8-18=-10$. For a $2\times2$ matrix, $\det\begin{bmatrix}a&b\\c&d\end{bmatrix}=ad-bc$. Apply the subtraction in that order.

REFERENCE ANSWER
-10

## 17592186702658 Practice

Source exercise: 3.1.3(b) only, printed page 126 (PDF page 138).

Find the determinant of $\begin{bmatrix}4&3&2\\1&7&8\\3&-9&3\end{bmatrix}$ **by hand, without technology**. Show your calculation.

Determinant: {{answer}}.

Expand along the first row, using signs $+,-,+$:

$$4\begin{vmatrix}7&8\\-9&3\end{vmatrix}-3\begin{vmatrix}1&8\\3&3\end{vmatrix}+2\begin{vmatrix}1&7\\3&-9\end{vmatrix}
=4(21+72)-3(3-24)+2(-9-21)=372+63-60=375.$$

The negative cofactor sign on the middle term is essential. A separate elimination check gives the same determinant.

REFERENCE ANSWER
375

## 17592186702577 Practice

Source exercise: 3.1.9, printed page **127** (PDF page 139); the assignment sheet lists page 128.

Identify the operation that changes the first matrix to the second, and explain its effect on the determinant:

$$\begin{bmatrix}a&b\\c&d\end{bmatrix}\longrightarrow\cdots\longrightarrow\begin{bmatrix}a&c\\b&d\end{bmatrix}.$$

The second matrix has the old rows as columns. Directly, the first determinant is $ad-bc$, and the second is $ad-cb=ad-bc$. This is transposition, rather than swapping two rows.

REFERENCE ANSWER
The matrix is transposed. Transposing a square matrix preserves its determinant: $\det(A^T)=\det(A)$.

## 17592186702512 Practice

Source exercise: 3.1.12, printed page 128 (PDF page 140).

Identify the operation that changes the first matrix to the second, and explain its effect on the determinant:

$$\begin{bmatrix}a&b\\c&d\end{bmatrix}\longrightarrow\cdots\longrightarrow\begin{bmatrix}a&b\\2c&2d\end{bmatrix}.$$

Scaling one row by $2$ scales the determinant by $2$. Directly, $a(2d)-b(2c)=2(ad-bc)$. Only one row is scaled, so the factor is $2$, rather than $2^2$.

REFERENCE ANSWER
The second row is multiplied by $2$: $R_2\leftarrow2R_2$. The new determinant is $2$ times the old determinant.

## 17592186702564 Practice

Source exercise: 3.1.17, printed page 128 (PDF page 140).

Is it true that $\det(A+B)=\det(A)+\det(B)$? If true, explain why; if false, give a counterexample.

A single pair of square matrices for which the two sides differ disproves the assertion. Here $A+B=\begin{bmatrix}2&0\\0&2\end{bmatrix}$, whose determinant is $2\cdot2=4$. The determinant is linear in one row at a time with the other rows fixed, not additive in the whole matrix.

REFERENCE ANSWER
It is false in general. Take $A=B=I_2$. Then $\det(A)+\det(B)=1+1=2$, while $\det(A+B)=\det(2I_2)=4$.

## 17592186702540 Practice

Source exercise: 3.1.19, printed page 128 (PDF page 140).

A real matrix is **orthogonal** if $A^T A=I$, so its inverse is its transpose. What are the possible values of $\det(A)$?

Enter the set of possible values: {{answer}}.

Taking determinants gives $\det(A^T)\det(A)=\det(I)=1$. Since $\det(A^T)=\det(A)$, we have $(\det A)^2=1$, hence $\det A\in\{-1,1\}$. Both occur: $I_n$ has determinant $1$, and $\operatorname{diag}(-1,1,\ldots,1)$ has determinant $-1$.

REFERENCE ANSWER
\{-1,1\}

## 17592186702514 Practice

Source exercise: 3.1.20, printed page 129 (PDF page 141).

Let $A,B$ be $n\times n$ matrices. The notation $A\sim B$ (**$A$ is similar to $B$**) means that some invertible matrix $P$ satisfies $A=P^{-1}BP$.

Show that $A\sim B$ implies $\det(A)=\det(B)$.

Use $\det(XY)=\det(X)\det(Y)$ and $\det(P^{-1})=1/\det(P)$. Similarity uses the same invertible $P$ on the two sides of $B$ with opposite powers. The notation $\sim$ here means similarity, as defined in this exercise.

REFERENCE ANSWER
By multiplicativity,

$$\det(A)=\det(P^{-1}BP)=\det(P^{-1})\det(B)\det(P)
=\frac{1}{\det(P)}\det(B)\det(P)=\det(B).$$

The cancellation is valid because $P$ is invertible, so $\det(P)\ne0$.

## 17592186702490 Practice

Source exercise: 3.1.24, printed page **129** (PDF page 141); the assignment sheet lists page 128.

Find the determinant, **using row operations to simplify first**. Show your row operations and track their effects on the determinant.

$$A=\begin{bmatrix}1&2&1&2\\3&1&-2&3\\-1&0&3&1\\2&3&2&-2\end{bmatrix}.$$

$\det(A)=$ {{answer}}.

First use $R_2\leftarrow R_2-3R_1$, $R_3\leftarrow R_3+R_1$, and $R_4\leftarrow R_4-2R_1$. These row replacements preserve the determinant:

$$\begin{bmatrix}1&2&1&2\\0&-5&-5&-3\\0&2&4&3\\0&-1&0&-6\end{bmatrix}.$$

Swap $R_2$ and $R_4$ once, changing the determinant's sign. Then apply $R_3\leftarrow R_3+2R_2$ and $R_4\leftarrow R_4-5R_2$:

$$\begin{bmatrix}1&2&1&2\\0&-1&0&-6\\0&0&4&-9\\0&0&-5&27\end{bmatrix}.$$

Finally, $R_4\leftarrow R_4+\tfrac54R_3$ gives upper triangular diagonal entries $1,-1,4,63/4$. Its determinant is $-63$. There was one row swap, so $\det(A)=63$.

REFERENCE ANSWER
63

## 17592186702627 Practice

Source exercise: 4.2.3, printed page 151 (PDF page 163).

Decide whether

$$\vec v=\begin{bmatrix}4\\4\\-3\end{bmatrix}$$

is a linear combination of

$$\vec u_1=\begin{bmatrix}3\\1\\-1\end{bmatrix},\qquad\vec u_2=\begin{bmatrix}2\\-2\\1\end{bmatrix}.$$

Set $a\vec u_1+b\vec u_2=\vec v$. The first two equations are $3a+2b=4$ and $a-2b=4$, giving $a=2$, $b=-1$. Check the third equation: $-a+b=-2-1=-3$. All three coordinates must agree.

REFERENCE ANSWER
Yes. The combination is $\vec v=2\vec u_1-\vec u_2$:

$$2\begin{bmatrix}3\\1\\-1\end{bmatrix}-\begin{bmatrix}2\\-2\\1\end{bmatrix}=\begin{bmatrix}4\\4\\-3\end{bmatrix}.$$

## 17592186702626 Practice

Source exercise: 4.10.4, printed page 221 (PDF page 233).

Consider

$$\vec v_1=\begin{bmatrix}1\\1\\-2\end{bmatrix},\quad\vec v_2=\begin{bmatrix}1\\2\\-2\end{bmatrix},\quad\vec v_3=\begin{bmatrix}1\\-3\\-2\end{bmatrix},\quad\vec v_4=\begin{bmatrix}-1\\1\\2\end{bmatrix}.$$

Is $\vec w=\begin{bmatrix}1\\2\\-1\end{bmatrix}$ in their span? If so, exhibit a linear combination equal to $\vec w$, using as few of the four vectors as possible.

If $\sum c_j\vec v_j=\vec w$, the first-coordinate equation would give $c_1+c_2+c_3-c_4=1$, while the third would give $-2(c_1+c_2+c_3-c_4)=-1$. The first equation makes the third left side $-2$, a contradiction. The requested minimal combination is conditional on membership.

REFERENCE ANSWER
No. Each generating vector satisfies $z=-2x$, so every linear combination also satisfies $z=-2x$. The target has $x=1$ and $z=-1$, which fails that relation. It is outside the span, so no such linear combination exists.

## 17592186702580 Practice

Source exercise: 4.10.10, printed page 222 (PDF page 234).

Suppose $\{\vec x_1,\ldots,\vec x_k\}$ is a set of vectors in $\mathbb R^n$. Show that $\vec0$ is in $\operatorname{span}\{\vec x_1,\ldots,\vec x_k\}$.

A span allows arbitrary real coefficients, including all zeros. The argument does not require the vectors to be nonzero or independent. Producing zero with all-zero coefficients does not demonstrate dependence; dependence requires a nontrivial zero combination.

REFERENCE ANSWER
Choose every coefficient to be zero. Then $0\vec x_1+\cdots+0\vec x_k=\vec0$, which is a linear combination of the given vectors. Therefore $\vec0$ belongs to their span.

## 17592186702562 Practice

Source exercise: 4.10.11, printed page 222 (PDF page 234).

Are the following vectors linearly independent? If they are, explain why. If they are not, exhibit one as a linear combination of the others. Also give a linearly independent set with the same span.

$$\vec v_1=\begin{bmatrix}1\\3\\-1\\1\end{bmatrix},\quad\vec v_2=\begin{bmatrix}1\\4\\-1\\1\end{bmatrix},\quad\vec v_3=\begin{bmatrix}1\\4\\0\\1\end{bmatrix},\quad\vec v_4=\begin{bmatrix}1\\10\\2\\1\end{bmatrix}.$$

The displayed combination checks in every coordinate: $-6+4+3=1$, $-18+16+12=10$, $6-4=2$, and $-6+4+3=1$. The first three rows of the matrix with columns $\vec v_1,\vec v_2,\vec v_3$ form a $3\times3$ minor with determinant $1$, so these three columns are independent. Removing $\vec v_4$, which is generated by them, preserves the span.

REFERENCE ANSWER
They are dependent because $\vec v_4=-6\vec v_1+4\vec v_2+3\vec v_3$. An independent set with the same span is $\{\vec v_1,\vec v_2,\vec v_3\}$.

## 17592186702602 Practice

Source exercise: 4.10.18, printed page 224 (PDF page 236).

Are the following vectors linearly independent? If they are, explain why. If they are not, exhibit one as a linear combination of the others. Also give a linearly independent set with the same span.

$$\vec v_1=\begin{bmatrix}1\\4\\-2\\1\end{bmatrix},\quad\vec v_2=\begin{bmatrix}1\\5\\-3\\1\end{bmatrix},\quad\vec v_3=\begin{bmatrix}1\\7\\-5\\1\end{bmatrix},\quad\vec v_4=\begin{bmatrix}1\\5\\-2\\1\end{bmatrix}.$$

The combination checks as $-2(1,4,-2,1)+3(1,5,-3,1)=(1,7,-5,1)$. For the proposed independent set, use the first three coordinate rows. The determinant of $\begin{bmatrix}1&1&1\\4&5&5\\-2&-3&-2\end{bmatrix}$ is $1$, proving independence. The removed vector $\vec v_3$ is generated by the retained ones, so their spans agree.

REFERENCE ANSWER
They are dependent because $\vec v_3=-2\vec v_1+3\vec v_2$. An independent set with the same span is $\{\vec v_1,\vec v_2,\vec v_4\}$.