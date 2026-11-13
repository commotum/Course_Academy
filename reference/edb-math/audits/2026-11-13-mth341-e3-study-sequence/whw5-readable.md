# MTH 341 — WHW-5

Captured basis: 14416

## 17592186754435 Assignment information

**MTH 341 — Written Homework 5**

Due: 2026-11-04
Due time: 23:59:00 America/Los_Angeles (PST).
Date imported: 2026-11-06
Source: [341-WHW-5.pdf](/api/source?path=%2Fhome%2Fjake%2FDeveloper%2Fstudy%2Fvault%2FF26%2Fsource%2F341%2FWHW-5%2F341-WHW-5.pdf)
Deadline source: [Canvas](https://canvas.oregonstate.edu/courses/2064363/assignments/10695098), verified 2026-11-06.

Question source: [Kuttler, *Linear Algebra: A First Course*, 2017A](/api/source?path=%2Fhome%2Fjake%2FDeveloper%2Fstudy%2Fvault%2FF26%2Fsource%2F341%2FKuttler-LinearAlgebra-AFirstCourse-2017A.pdf). Exercise and printed-page numbers were checked against this edition; PDF page positions are recorded below.

Study answers, explanations, and graphics labeled “Authored reference” are additions, not publisher-provided solutions.

## Instructions

Write solutions on separate letter-size (8.5 × 11 in.) or A4 paper and use the assignment sheet as the cover. Show all work and write neatly. Submit a single PDF through Canvas by the posted deadline; late homework is not accepted. Technology such as WolframAlpha may be used for row reduction unless an exercise says otherwise. The current Canvas assignment is worth 10 points: 8 for completeness and 2 for correctness of local Problem 2 (Kuttler 4.10.33). The old dates retained in the reused handout do not set the current deadline.



## 17592186754683 Practice

Source question: Assignment item (1); Kuttler 2017A, Exercise 4.10.21, printed p. 224 (PDF p. 236).

The following five vectors lie in $\mathbb R^4$, in the listed order $v_1,\ldots,v_5$: $$\left\{\begin{pmatrix}1\\1\\-1\\1\end{pmatrix},\begin{pmatrix}1\\2\\-1\\1\end{pmatrix},\begin{pmatrix}1\\-2\\-1\\1\end{pmatrix},\begin{pmatrix}1\\2\\0\\1\end{pmatrix},\begin{pmatrix}1\\-1\\-1\\1\end{pmatrix}\right\}.$$ Explain why they cannot be linearly independent. Then find a linearly independent subset with the same span, that is, a basis for their span.

Use the number of vectors versus the ambient dimension for the first claim. To extract a basis, choose pivot columns from the original matrix, not the reduced matrix.

REFERENCE ANSWER
Five vectors in $\mathbb R^4$ are dependent because a homogeneous system with four equations and five unknowns has a free variable. Put the listed vectors in the columns of $A$. Row reduction gives $$\operatorname{rref}(A)=\begin{pmatrix}1&0&4&0&3\\0&1&-3&0&-2\\0&0&0&1&0\\0&0&0&0&0\end{pmatrix}.$$ The original columns $1,2,4$ form a basis: $\mathcal B=\left\{\begin{pmatrix}1\\1\\-1\\1\end{pmatrix},\begin{pmatrix}1\\2\\-1\\1\end{pmatrix},\begin{pmatrix}1\\2\\0\\1\end{pmatrix}\right\}$. As a span check, $v_3=4v_1-3v_2$ and $v_5=3v_1-2v_2$.

## 17592186754503 Practice

Source question: Assignment item (2); Kuttler 2017A, Exercise 4.10.33, printed p. 227 (PDF p. 239).

Let $H=\operatorname{span}\left\{\begin{pmatrix}0\\1\\1\\-1\end{pmatrix},\begin{pmatrix}-1\\-1\\-2\\2\end{pmatrix},\begin{pmatrix}2\\3\\5\\-5\end{pmatrix},\begin{pmatrix}0\\1\\2\\-2\end{pmatrix}\right\}$. Find its dimension and determine a basis. Show supporting work.

$\dim H=$ {{dimension}}. Give a basis and its justification in the written response.

Row-reduce the spanning columns, count pivots, and retain the corresponding original vectors. This is the Canvas rubric’s selected correctness problem.

REFERENCE ANSWER
3

REFERENCE ANSWER
The RREF of the matrix of listed columns is $$\begin{pmatrix}1&0&1&0\\0&1&-2&0\\0&0&0&1\\0&0&0&0\end{pmatrix}.$$ Pivot columns $1,2,4$ of the original matrix give the basis $\left\{\begin{pmatrix}0\\1\\1\\-1\end{pmatrix},\begin{pmatrix}-1\\-1\\-2\\2\end{pmatrix},\begin{pmatrix}0\\1\\2\\-2\end{pmatrix}\right\}$. The third vector equals $v_1-2v_2$, so no span is lost. The three pivots prove independence and dimension $3$.

## 17592186754728 Practice

Source question: Assignment item (3); Kuttler 2017A, Exercise 4.10.35, printed p. 227 (PDF p. 239).

Let $H=\operatorname{span}\left\{\begin{pmatrix}-1\\1\\-1\\-2\end{pmatrix},\begin{pmatrix}-4\\3\\-2\\-4\end{pmatrix},\begin{pmatrix}-3\\2\\-1\\-2\end{pmatrix},\begin{pmatrix}-1\\1\\-2\\-4\end{pmatrix},\begin{pmatrix}-7\\5\\-3\\-6\end{pmatrix}\right\}$. Find its dimension and determine a basis. Show supporting work.

$\dim H=$ {{dimension}}. Give a basis and its justification in the written response.

Redundant spanning columns can be deleted without changing the span; the remaining original pivot columns form a basis.

REFERENCE ANSWER
3

REFERENCE ANSWER
The RREF of the spanning-column matrix is $$\begin{pmatrix}1&0&-1&0&-1\\0&1&1&0&2\\0&0&0&1&0\\0&0&0&0&0\end{pmatrix}.$$ A basis is formed by original columns $1,2,4$: $\left\{\begin{pmatrix}-1\\1\\-1\\-2\end{pmatrix},\begin{pmatrix}-4\\3\\-2\\-4\end{pmatrix},\begin{pmatrix}-1\\1\\-2\\-4\end{pmatrix}\right\}$. The other columns satisfy $v_3=-v_1+v_2$ and $v_5=-v_1+2v_2$. There are three pivots, so $\dim H=3$.

## 17592186754622 Practice

Source question: Assignment item (4); Kuttler 2017A, Exercise 4.10.44, printed p. 228 (PDF p. 240).

For a fixed $w\in\mathbb R^4$, let $M=\{u\in\mathbb R^4:w\cdot u=0\}$. Is $M$ a subspace? Explain.

Use the subspace test and the dot product’s linearity; do not assume $w$ is nonzero.

REFERENCE ANSWER
Yes, including when $w=0$. First $w\cdot0=0$, so $0\in M$. For $u,v\in M$ and scalars $\alpha,\beta$, $$w\cdot(\alpha u+\beta v)=\alpha(w\cdot u)+\beta(w\cdot v)=0.$$ Hence $M$ is closed under all linear combinations and is a subspace of $\mathbb R^4$. Equivalently $M=\operatorname{Null}(w^T)$.

## 17592186754460 Practice

Source question: Assignment item (5); Kuttler 2017A, Exercise 4.10.47, printed p. 229 (PDF p. 241).

Consider $$S=\left\{\begin{pmatrix}4u+v-5w\\12u+6v-6w\\4u+4v+4w\end{pmatrix}:u,v,w\in\mathbb R\right\}.$$ Is $S$ a subspace of $\mathbb R^3$? If so, explain why, give a basis, and find its dimension.

Dimension (if a subspace): {{dimension}}. Give the subspace argument and a basis in the written response.

Collect the coefficients of $u,v,w$ as generating vectors. Expressing the set as their span establishes the subspace claim before extracting a basis.

REFERENCE ANSWER
2

REFERENCE ANSWER
Yes. Write $$S=\operatorname{span}\left\{\begin{pmatrix}4\\12\\4\end{pmatrix},\begin{pmatrix}1\\6\\4\end{pmatrix},\begin{pmatrix}-5\\-6\\4\end{pmatrix}\right\}.$$ A span is closed under addition and scalar multiplication, hence is a subspace. The third generator equals $-2$ times the first plus $3$ times the second. The first two are not scalar multiples; they are independent. Thus a basis is $\{(4,12,4)^T,(1,6,4)^T\}$ and $\dim S=2$. The generator-matrix RREF is $\begin{pmatrix}1&0&-2\\0&1&3\\0&0&0\end{pmatrix}$.

## 17592186754449 Practice

Source question: Assignment item (6); Kuttler 2017A, Exercise 4.10.55, printed p. 230 (PDF p. 242).

If five vectors in $\mathbb R^5$ are linearly independent, must they span $\mathbb R^5$? Explain.

Explain the link between a square matrix’s independent columns, full rank, and its column space being the whole ambient space.

REFERENCE ANSWER
Yes. Form the $5\times5$ matrix $A$ with those vectors as columns. Independence means $Ax=0$ has only the zero solution, so every one of the five columns is a pivot column. There are therefore five pivot rows as well. For every $b\in\mathbb R^5$, the equation $Ax=b$ has a solution, so the columns span $\mathbb R^5$. Equivalently, an independent set with exactly the dimension of the ambient space is a basis.

## 17592186754518 Practice

Source question: Assignment item (7); Kuttler 2017A, Exercise 4.10.56, printed p. 230 (PDF p. 242).

Can six vectors in $\mathbb R^5$ be linearly independent? Explain.

Use the number of possible pivots to prove a nontrivial dependence relation exists, rather than merely asserting there are too many vectors.

REFERENCE ANSWER
No. Put them in a $5\times6$ matrix $A$. It has at most five pivots, so the homogeneous system $Ax=0$ has at least one free variable and therefore a nonzero solution. This gives a nontrivial linear relation among the six vectors. An independent set in a five-dimensional space has at most five vectors.

## 17592186754599 Practice

Source question: Assignment item (8); Kuttler 2017A, Exercise 4.10.63, printed p. 231 (PDF p. 243).

Find the rank of $$A=\begin{pmatrix}1&3&0&-2&0&3\\3&9&1&-7&0&8\\1&3&1&-3&1&-1\\1&3&-1&-1&-2&10\end{pmatrix}.$$ Also give a basis for its row space and a basis for its column space. Show supporting work.

$\operatorname{rank}(A)=$ {{rank}}. Give both bases and your row reduction in the written response.

Count pivots for rank. Use reduced nonzero rows for a row basis and original pivot columns for a column basis.

REFERENCE ANSWER
3

REFERENCE ANSWER
The RREF is $$R=\begin{pmatrix}1&3&0&-2&0&3\\0&0&1&-1&0&-1\\0&0&0&0&1&-3\\0&0&0&0&0&0\end{pmatrix}.$$ It has three pivots, so $\operatorname{rank}(A)=3$. Its nonzero rows give the row-space basis $$\{(1,3,0,-2,0,3),(0,0,1,-1,0,-1),(0,0,0,0,1,-3)\}.$$ Pivot columns $1,3,5$ must be taken from the original $A$ to give the column-space basis $$\left\{\begin{pmatrix}1\\3\\1\\1\end{pmatrix},\begin{pmatrix}0\\1\\1\\-1\end{pmatrix},\begin{pmatrix}0\\0\\1\\-2\end{pmatrix}\right\}.$$ Row operations preserve row space but generally change column space; this explains the different extraction rules.