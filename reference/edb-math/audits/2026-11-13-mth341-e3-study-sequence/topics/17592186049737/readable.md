# 17592186049737 Introduction to Abstract Vector Spaces

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186125833 — Introduction

The structure $\mathbb{R}^n$ is called a **vector space**. However, many other structures possess properties similar to $\mathbb{R}^n.$ These other structures can be called vector spaces too. 

In this lesson, we'll learn about some important properties used to construct vector spaces. We begin by discussing what it means for a set to be **closed** under addition and scalar multiplication.

As an example, consider the set $\mathrm{M}_2(\mathbb{R})$ of all $2 \times 2$ matrices with real entries:

$$
\mathrm{M}_2(\mathbb{R}) = 
	\left\{
		{\left[ \begin{array}{cc}a & b \\ c & d\end{array} \right]} \: : \: a,b,c,d \in \mathbb{R}
	\right\}
$$

For this set of matrices, we can define two operations:

- the addition of two matrices, and

- the multiplication of a matrix by a real number (called a scalar).

Now, notice the following:

- $\mathrm{M}_2(\mathbb{R})$ is **closed under addition**. This means that the sum of *any* two matrices from $\mathrm{M}_2(\mathbb{R})$ is also a matrix in $\mathrm{M}_2(\mathbb{R}).$

- $\mathrm{M}_2(\mathbb{R})$ is **closed under scalar multiplication**. This means that the product of *any* scalar and *any* matrix from $\mathrm{M}_2(\mathbb{R})$ is also a matrix in $\mathrm{M}_2(\mathbb{R}).$

Identifying that a set is closed under addition and scalar multiplication is an essential first step in determining whether a set can form a vector space.



### tutorial 17592186125860 — Sets That Are Not Closed

It's important to realize that not all sets are closed under addition and scalar multiplication. Sets not closed under addition and scalar multiplication *cannot* be vector spaces. 

For instance, let $S$ be the set of all polynomials with real coefficients whose degree is greater than or equal to $5.$  

We note that $S$ is not closed under addition. To see why this is the case, let's define the polynomials $p(x),q(x)\in S$ as 

$$
p(x) = x^5, \qquad q(x) = 1-x^5.
$$

Adding the two polynomials using regular polynomial addition, we get

$$
p(x) + q(x) = x^5 + (1-x^5) = 1\notin S
$$

The sum $p(x) + q(x)$ is not in $S$ because it is a polynomial of degree zero, which is less than $5.$

Therefore, we conclude that our set $S$ is *not* closed under addition.



### example 17592186124432 — Identifying Sets Closed Under Addition and Scalar Multiplication

Let $M$ be the set of all $2\times2$ real matrices whose entries are non-negative. Then, which of the following statements are true?

I. $I_2 \in M$

II. For any $A \in M$ and $\alpha \in \mathbb{R}$, we have $\alpha \cdot A \in M.$

III. The set is closed under scalar multiplication.

Let's verify the statements one by one.

- Statement I is true. Indeed, $I_2 = {\left[ \begin{array}{cc}1 & 0 \\ 0 & 1\end{array} \right]} \in M$ because all its entries are non-negative.

- Statement II is false. There exists a $2\times2$ real matrix in $M$ that has a scalar multiple not in $M.$ 

For example, let $A = {\left[ \begin{array}{cc}1 & 0 \\ 0 & 1\end{array} \right]}$ and $\alpha=-1\in\mathbb{R}.$ Notice that $A$ belongs to $M$ since statement I is true. However,
$$
\alpha \cdot A
=
-1 \cdot {\left[ \begin{array}{cc}1 & 0 \\ 0 & 1\end{array} \right]}


=
{\left[ \begin{array}{cc}- 1 & 0 \\ 0 & - 1\end{array} \right]} \notin M
$$
Since the entries on the main diagonal are negative, we conclude that $-1 \cdot A \notin M.$

- Statement III is false. Since statement II is false, the set is *not* closed under scalar multiplication.

Therefore, the correct answer is "I only."

### tutorial 17592186125759 — Addition of Vectors

Let's now compare some properties of addition in $\mathbb{R}^2$ and $\text{M}_2(\mathbb{R}).$ 
It turns out that the addition of two matrices in $\mathrm{M}_2(\mathbb{R})$ is *very* similar to the addition of two vectors in $\mathbb{R}^n.$ See the table below.



<div class="source-table-scroll"><table class="source-table" data-rules="all" data-table-align="center" data-frame="true">
<tbody><tr data-next-row="true">
<td data-cell-align="center"><b></b></td>
<td data-cell-align="center" data-fill="#D6EAF8"><b>$\mathbb{R}^2$</b></td>
<td data-cell-align="center" data-fill="#D6EAF8"><b>$\text{M}_2(\mathbb{R})$</b></td>
</tr>
<tr data-next-row="true">
<td colspan="3" data-cell-align="center"><strong>Addition is Commutative:</strong></td>
</tr>
<tr data-next-row="true">
<td data-cell-align="center" data-fill="#D6EAF8">A1</td>
<td data-cell-align="center">For any vectors $\mathbf{u}, \mathbf{v} \in \mathbb{R}^2,$ we have $\color{blue}\mathbf{u}+\mathbf{v} = \mathbf{v}+\mathbf{u}$</td>
<td data-cell-align="center">For any matrices $A, B \in \text{M}_2(\mathbb{R}),$ we have $\color{blue}A+B = B+A$</td>
</tr>
<tr data-next-row="true">
<td colspan="3" data-cell-align="center"><strong>Addition is Associative:</strong></td>
</tr>
<tr data-next-row="true">
<td data-cell-align="center" data-fill="#D6EAF8">A2</td>
<td data-cell-align="center">For any vectors $\mathbf{u}, \mathbf{v}, \mathbf{w} \in \mathbb{R}^2,$ we have $\color{blue}(\mathbf{u}+\mathbf{v})+\mathbf{w} = \mathbf{u}+(\mathbf{v}+\mathbf{w})$</td>
<td data-cell-align="center">For any matrices $A, B, C \in \text{M}_2(\mathbb{R}),$ we have $\color{blue}(A+B) + C = A + (B+C)$</td>
</tr>
<tr data-next-row="true">
<td colspan="3" data-cell-align="center"><strong>Existence of a Unique Zero Element:</strong></td>
</tr>
<tr data-next-row="true">
<td data-cell-align="center" data-fill="#D6EAF8">A3</td>
<td data-cell-align="center">For the zero-vector $\mathbf{0}$ and any $\mathbf{u} \in \mathbb{R}^2,$ we have $\color{blue} \mathbf{u} + \mathbf{0} = \mathbf{u}$</td>
<td data-cell-align="center">For the zero-matrix $O$ and any $A \in \text{M}_2(\mathbb{R}),$ we have $\color{blue} A + O = A$</td>
</tr>
<tr data-next-row="true">
<td colspan="3" data-cell-align="center"><strong>Existence of a Unique Opposite Element:</strong></td>
</tr>
<tr><td data-cell-align="center" data-fill="#D6EAF8">A4</td>
<td data-cell-align="center">For any vector $\mathbf{u} \in \mathbb{R}^2$ we can find the corresponding negative vector $-\mathbf{u} \in \mathbb{R}$ such that $\color{blue} \mathbf{u} + (-\mathbf{u}) = \mathbf{0}$</td>
<td data-cell-align="center">For any matrix $A \in \text{M}_2(\mathbb{R})$ we can find the corresponding negative matrix $-A \in \text{M}_2(\mathbb{R})$ such that $\color{blue} A + (-A) = O$</td>
</tr>
</tbody></table></div>



And it's not just matrices that have additive properties similar to those of $\mathbb R^n.$ Many mathematical structures do. Let's see some more examples.



### example 17592186124297 — Verifying Properties Involving Vector Addition

Let $L$ be the set of all polynomials with real coefficients whose degree is less than or equal to $2.$  Which of the following statements are true? 

I. For any $p(x),q(x) \in L,$ we have $p(x)+q(x) = q(x)+p(x).$

II. For any $p(x),q(x),r(x) \in L,$ we have $[p(x)+q(x)]+r(x) = p(x)+[q(x)+r(x)].$

III. For each $p(x) \in L,$ we have $-p(x) \in L$ such that $p(x)+(-p(x))=0.$

Let's examine our statements one at a time.

- Statement I is true. Indeed, for any polynomials $p(x), q(x) \in L,$ we obtain that 

$$
p(x) + q(x)= q(x) +p(x)
$$

since polynomial addition is commutative.

- Statement II is true. Indeed, for any polynomials $p(x),q(x),r(x) \in L,$ we obtain that

$$
[p(x) + q(x)] + r(x) = p(x) + [q(x) + r(x)]
$$

since polynomial addition is associative.

- Statement III is true. Indeed, for any polynomial $p(x) \in L,$ there is a corresponding negative polynomial $-p(x)$ such that

$$
p(x) + (-p(x))= p(x) - p(x) = 0.
$$

Notice that

$$
\deg(-p(x)) = \deg(p(x)) \leq 2,
$$

hence $-p(x) \in L.$

Therefore, the correct answer is "I, II, and III."

### tutorial 17592186125832 — Scalar Multiplication and the Distributive Laws

Let's also compare some properties of scalar multiplication in $\mathbb{R}^2$ and $\text{M}_2(\mathbb{R}).$ It turns out that the multiplication of a matrix in $\mathrm{M}_2(\mathbb{R})$ by a scalar is *very* similar to the multiplication of a vector in $\mathbb{R}^n$ by a real number. See the table below.



<div class="source-table-scroll"><table class="source-table" data-rules="all" data-table-align="center" data-frame="true">
<tbody><tr data-next-row="true">
<td data-cell-align="center"><b></b></td>
<td data-cell-align="center" data-fill="#D6EAF8"><b>$\mathbb{R}^2$</b></td>
<td data-cell-align="center" data-fill="#D6EAF8"><b>$\text{M}_2(\mathbb{R})$</b></td>
</tr>
<tr data-next-row="true">
<td colspan="3" data-cell-align="center"><strong>Invariance Under Multiplication by $1$:</strong></td>
</tr>
<tr data-next-row="true"><td data-cell-align="center" data-fill="#D6EAF8">A5</td>
<td data-cell-align="center">For any vector $\mathbf{u} \in \mathbb{R}^2$, we have $\color{blue} 1 \cdot \mathbf{u} = \mathbf{u}$</td>
<td data-cell-align="center">For any matrix $A \in \text{M}_2(\mathbb{R})$, we have $\color{blue} 1 \cdot A = A$</td>
</tr>
<tr data-next-row="true">
<td colspan="3" data-cell-align="center"><strong>Scalar Multiplication is Associative:</strong></td>
</tr>
<tr data-next-row="true"><td data-cell-align="center" data-fill="#D6EAF8">A6</td>
<td data-cell-align="center">For any numbers $\alpha, \beta$ and any vector $\mathbf{u} \in \mathbb{R}^2$, we have $\color{blue} \alpha (\beta \mathbf{u}) = (\alpha\beta) \mathbf{u}$</td>
<td data-cell-align="center">For any numbers $\alpha, \beta$ and any matrix $A \in \text{M}_2(\mathbb{R})$, we have $\color{blue} \alpha (\beta A) = (\alpha\beta) A$</td>
</tr>
<tr data-next-row="true">
<td colspan="3" data-cell-align="center"><strong>Distributive Laws:</strong></td>
</tr>
<tr data-next-row="true"><td data-cell-align="center" data-fill="#D6EAF8">A7</td>
<td data-cell-align="center">For any numbers $\alpha, \beta$ and any vector $\mathbf{u} \in \mathbb{R}^2$, we have $\color{blue} (\alpha + \beta)\mathbf{u} = \alpha \mathbf{u} + \beta \mathbf{u}$</td>
<td data-cell-align="center">For any numbers $\alpha, \beta$ and any matrix $A \in \text{M}_2(\mathbb{R})$, we have $\color{blue} (\alpha + \beta)A = \alpha A + \beta A$</td>
</tr>
<tr><td data-cell-align="center" data-fill="#D6EAF8">A8</td>
<td data-cell-align="center">For any number $\alpha$ and any vectors $\mathbf{u}, \mathbf{v} \in \mathbb{R}^2$, we have $\color{blue} \alpha (\mathbf{u} + \mathbf{v}) = \alpha \mathbf{u} + \alpha \mathbf{v}$</td>
<td data-cell-align="center">For any number $\alpha$ and any matrices $A, B \in \text{M}_2(\mathbb{R})$, we have $\color{blue} \alpha (A + B) = \alpha A + \alpha B$</td>
</tr>
</tbody></table></div>





### example 17592186124400 — Verifying Properties Involving Scalar Multiplication and the Distributive Laws

Let $P$ be the set of all $2\times 2$ real matrices $A= (a_{ij})$ such that $a_{11} + a_{22} > 0.$ Which of the following properties are true?

I. For any $A \in P,$ we have $1 \cdot A = A.$

II. For any $A \in P$ and $\alpha,\beta \in \mathbb{R},$ we have $\alpha(\beta A) = (\alpha\beta) A.$

III. For any $A \in P$ and $\alpha,\beta \in \mathbb{R},$ we have $(\alpha+\beta) A= \alpha A + \beta A.$

Let's verify the statements one by one.

- Statement I is true. Indeed, for any $2\times 2$ matrix $A = (a_{ij}) \in P,$ the entries are just real numbers. Thus, we have

$$
1 \cdot a_{ij} = a_{ij},
$$

and hence,

$$
1\cdot A=A.
$$

- Statements II is true. Indeed, for any $2\times 2$ matrix $A = (a_{ij}) \in P,$ the entries are just real numbers. Thus, for any $\alpha, \beta \in \mathbb{R},$ we obtain that

$$
\alpha(\beta a_{ij}) = (\alpha\beta) a_{ij},
$$

and hence,

$$
\alpha(\beta A) = (\alpha\beta) A.
$$

- Statements III is true. Indeed, for any $2\times 2$ matrix $A = (a_{ij}) \in P,$ the entries are just real numbers. Thus, for any $\alpha, \beta \in \mathbb{R},$ we obtain that

$$
(\alpha+\beta) a_{ij} = \alpha a_{ij} + \beta a_{ij},
$$

and hence,

$$
(\alpha+\beta) A= \alpha A + \beta A.
$$

Therefore, the correct answer is "I, II, and III."

### tutorial 17592186125861 — A Summary of the Addition and Scalar Multiplication Properties of Euclidian Space

In this lesson, we discussed several properties exhibited by vectors in $\mathbb R^n$ and other sets.
Let's consolidate these properties into a single list.



<div class="source-table-scroll"><table class="source-table" data-rules="all" data-table-align="center" data-frame="true">
<tbody><tr data-next-row="true">
<td data-cell-align="center" data-fill="#D6EAF8"><strong>Label</strong></td>
<td data-cell-align="center" data-fill="#D6EAF8"><strong>Name</strong></td>
<td data-cell-align="center" data-fill="#D6EAF8"><strong>Description</strong></td>
</tr>
<tr data-next-row="true">
<td data-cell-align="center" data-fill="#D6EAF8">A1</td>
<td data-cell-align="left"><strong>Addition is Commutative</strong></td>
<td data-cell-align="left">For any vectors $\mathbf{u}, \mathbf{v} \in \mathbb{R}^2,$ we have $\color{blue}\mathbf{u}+\mathbf{v} = \mathbf{v}+\mathbf{u}$</td>
</tr>
<tr data-next-row="true">
<td data-cell-align="center" data-fill="#D6EAF8">A2</td>
<td data-cell-align="left"><strong>Addition is Associative</strong></td>
<td data-cell-align="left">For any vectors $\mathbf{u}, \mathbf{v}, \mathbf{w} \in \mathbb{R}^2,$ we have $\color{blue}(\mathbf{u}+\mathbf{v})+\mathbf{w} = \mathbf{u}+(\mathbf{v}+\mathbf{w})$</td>
</tr>
<tr data-next-row="true">
<td data-cell-align="center" data-fill="#D6EAF8">A3</td>
<td data-cell-align="left"><strong>Existence of a Unique Zero Element</strong></td>
<td data-cell-align="left">For the zero-vector $\mathbf{0}$ and any $\mathbf{u} \in \mathbb{R}^2,$ we have $\color{blue} \mathbf{u} + \mathbf{0} = \mathbf{u}$</td>
</tr>
<tr data-next-row="true"><td data-cell-align="center" data-fill="#D6EAF8">A4</td>
<td data-cell-align="left"><strong>Existence of a Unique Opposite Element</strong></td>
<td data-cell-align="left">For any vector $\mathbf{u} \in \mathbb{R}^2$ we can find the corresponding negative vector $-\mathbf{u} \in \mathbb{R}$ such that $\color{blue} \mathbf{u} + (-\mathbf{u}) = \mathbf{0}$</td>
</tr>
<tr data-next-row="true"><td data-cell-align="center" data-fill="#D6EAF8">A5</td>
<td data-cell-align="left"><strong>Invariance Under Multiplication by $1$</strong></td>
<td data-cell-align="left">For any vector $\mathbf{u} \in \mathbb{R}^2$, we have $\color{blue} 1 \cdot \mathbf{u} = \mathbf{u}$</td></tr>
<tr data-next-row="true"><td data-cell-align="center" data-fill="#D6EAF8">A6</td>
<td data-cell-align="left"><strong>Scalar Multiplication is Associative</strong></td>
<td data-cell-align="left">For any numbers $\alpha, \beta$ and any vector $\mathbf{u} \in \mathbb{R}^2$, we have $\color{blue} \alpha (\beta \mathbf{u}) = (\alpha\beta) \mathbf{u}$</td>
</tr>
<tr data-next-row="true"><td data-cell-align="center" data-fill="#D6EAF8">A7</td>
<td data-cell-align="left"><strong>Distributive Laws:</strong></td>
<td data-cell-align="left">For any numbers $\alpha, \beta$ and any vector $\mathbf{u} \in \mathbb{R}^2$, we have $\color{blue} (\alpha + \beta)\mathbf{u} = \alpha \mathbf{u} + \beta \mathbf{u}$</td>
</tr>
<tr><td data-cell-align="center" data-fill="#D6EAF8">A8</td>
<td data-cell-align="left"><strong>Distributive Laws:</strong></td>
<td data-cell-align="left">For any number $\alpha$ and any vectors $\mathbf{u}, \mathbf{v} \in \mathbb{R}^2$, we have $\color{blue} \alpha (\mathbf{u} + \mathbf{v}) = \alpha \mathbf{u} + \alpha \mathbf{v}$</td>
</tr>
</tbody></table></div>


We'll meet these properties again in a future lesson, where we'll formally define what we mean by a vector space.



## Representative practice (first three per skill; full bank in practice.json)

### Identifying Sets Closed Under Addition and Scalar Multiplication (16 captured questions)

Question 17592186125240 — question.difficulty/easy

Let $K$ be the set of all functions $f: R → R$ such that $f(0) = 1$. Which of the following statements are true?

1. $p(x) ∈ K$, where $p(x) = x^{2} + 1$.
2. For any $f(x), g(x) ∈ K$, we have $f(x) + g(x) ∈ K$.
3. The set is closed under addition.

Solution: 

Question 17592186125241 — question.difficulty/easy

Let $U$ be the set of polynomials of the form $a{x}^{3},$ where $a\in R.$ Which of the following statements are true?

Select all that apply.

Solution: Let's examine each of our statements in turn.

- Statement “$h(x)\in U,$ where $h(x)=3x.$” is false. The set $U$ contains only polynomials of the form $a{x}^{3},$ where $a$ is a real coefficient. However, $h(x)=3x$ is *not* a polynomial of this form. So, $h(x)\notin U.$

- Statement “For any $p(x)\in U$ and $k\in R,$ we have $k\cdot p(x)\in U.$” is true. Indeed, suppose $p(x)=a{x}^{3}\in U,$ where $a$ is a real coefficient, and $k\in R.$ Then,

$$
k\cdot p(x)=k(a{x}^{3})=(ka){x}^{3}.
$$

Since $(ka)$ is a real coefficient, we conclude that $(ka){x}^{3}\in U,$ i.e., $k\cdot p(x)\in U.$

- Statement “The set is closed under scalar multiplication” is true. Since statement “For any $p(x)\in U$ and $k\in R,$ we have $k\cdot p(x)\in U.$” is true, the set is closed scalar multiplication.

Therefore, the correct answer is “For any $p(x)\in U$ and $k\in R,$ we have $k\cdot p(x)\in U.$”; “The set is closed under scalar multiplication” only.

Answer $h(x)\in U,$ where $h(x)=3x.$: false

Answer For any $p(x)\in U$ and $k\in R,$ we have $k\cdot p(x)\in U.$: true

Answer The set is closed under scalar multiplication.: true

Question 17592186278339 — question.difficulty/easy

Let $K$ be the set of all functions $f:R\to R$ such that $f(0)=-1.$  Which of the following statements are true?

Select all that apply.

Solution: Let's verify the statements one by one.

- Statement “$p(x)\in K,$ where $p(x)=(x-1)^{3}.$” is true. Indeed, $p(x)=(x-1)^{3}\in K$ because 

$$
p(0)=(0-1)^{3}=(-1)^{3}=-1.
$$

- Statement “For any $f(x),g(x)\in K$, we have $f(x)+g(x)\in K.$” is false. There exist functions in $K$ such that their sum is *not* in $K.$ For example, let $f(x)=-1$ and $g(x)=(x-1)^{3}.$ Notice that both these functions belong to $K$ since $f(0)=g(0)=-1.$ However,

$$
f(0)+g(0)=-1+(0-1)^{3}=-2\ne -1.
$$

Hence, $f(x)+g(x)\notin K.$

- Statement “The set is closed under addition” is false. Since statement “For any $f(x),g(x)\in K$, we have $f(x)+g(x)\in K.$” is false, the set is *not* closed under addition.

Therefore, the correct answer is “$p(x)\in K,$ where $p(x)=(x-1)^{3}.$” only.

Answer $p(x)\in K,$ where $p(x)=(x-1)^{3}.$: true

Answer For any $f(x),g(x)\in K$, we have $f(x)+g(x)\in K.$: false

Answer The set is closed under addition.: false

### Verifying Properties Involving Vector Addition (17 captured questions)

Question 17592186124765 — question.difficulty/moderate

Let $D$ be the set of all $2\times 2$ matrices of the form $$
\displaystyle \begin{bmatrix}a & 0 \\ 0 & a\end{bmatrix},
$$ where $a\in R.$ Which of the following statements are true?  

I. The identity matrix $$
\displaystyle {I}_{2}=\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}
$$ belongs to $D.$

II. For the zero matrix $O$ and any $A,B\in D,$ we have $A+O=O.$

III. For any $A,B\in D,$ we have $A+B=B+A.$

Solution: Let's examine each statement in turn.

- Statement I is true. Indeed, every element $A$ in $D$ satisfies ${a}_{12}={a}_{21}=0$ and ${a}_{11}={a}_{22}.$ So, $$
\displaystyle {I}_{2}=\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\in D.
$$

- Statement II is false. For example, consider the identity matrix $$
\displaystyle {I}_{2}=\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\in D.
$$ Then

$$
{I}_{2}+O=\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}+\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}=\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}\ne O.
$$

- Statement III is true. Indeed, For any matrices $A,B\in D,$ we obtain that 

$$
A+B=B+A
$$

since matrix addition is commutative.

Therefore, the correct answer is "I and III only."

Answer selection: I and III only

Question 17592186125219 — question.difficulty/moderate

Let $U$ be the set of polynomials of the form $a{x}^{3},$ where $a\in R.$ Which of the following statements are true?

Select all that apply.

Solution: Let's examine each statement in turn.

- Statement “The zero-polynomial belongs to $U.$” is true. Indeed, the zero-polynomial can be represented as 

$$
0=0\cdot {x}^{3}.
$$

 
Hence, $0\in U.$

- Statement “For any $p(x),q(x)\in U,$ we have $p(x)+q(x)=q(x)+p(x).$” is true. Indeed, for any polynomials $p(x),q(x)\in U,$ we obtain that 

$$
p(x)+q(x)=q(x)+p(x)
$$

since polynomial addition is commutative.

- Statement “For any $p(x),q(x),r(x)\in U,$ we have $[p(x)-q(x)]-r(x)=p(x)-[q(x)-r(x)].$” is false. For example, consider polynomials $p(x)={x}^{3},$ $q(x)=2{x}^{3},$ and $r(x)=3{x}^{3}$ from $U.$ Then: 

$$
\begin{aligned}[p(x)-q(x)]-r(x) & =[{x}^{3}-2{x}^{3}]-3{x}^{3} \\  & =-{x}^{3}-3{x}^{3} \\  & =-4{x}^{3} \\ p(x)-[q(x)-r(x)] & ={x}^{3}-[2{x}^{3}-3{x}^{3}] \\  & ={x}^{3}-[-{x}^{3}] \\  & =2{x}^{3}\end{aligned}
$$

Hence, $[p(x)-q(x)]-r(x)\ne p(x)-[q(x)-r(x)].$

Therefore, the correct answer is “The zero-polynomial belongs to $U.$”; “For any $p(x),q(x)\in U,$ we have $p(x)+q(x)=q(x)+p(x).$” only.

Answer For any $p(x),q(x),r(x)\in U,$ we have $[p(x)-q(x)]-r(x)=p(x)-[q(x)-r(x)].$: false

Answer For any $p(x),q(x)\in U,$ we have $p(x)+q(x)=q(x)+p(x).$: true

Answer The zero-polynomial belongs to $U.$: true

Question 17592186243917 — question.difficulty/moderate

Let $L$ be the set of all $2\times 2$ matrices with real entries and determinant $0.$ Which of the following statements are true?

Select all that apply.

Solution: Let's examine each statement in turn.

- Statement “The  zero-matrix $\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}$ belongs to $L.$” is true. Indeed, $\begin{vmatrix}0 & 0 \\ 0 & 0\end{vmatrix}=0.$ Hence, $\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}\in L.$

- Statement “For any $A\in L,$ we can find the corresponding negative matrix $-A\in L$ such that $A+(-A)=O.$” is true. Indeed, for any matrix $A\in L,$ there is a corresponding negative matrix $-A$ such that

$$
A+(-A)=A-A=O.
$$

Notice that

$$
|-A|=|-1\cdot A|=(-1)^{2}\cdot |A|=1\cdot 0=0,
$$

hence $-A\in L.$

- Statement “For any $A,B,C\in L,$ we have $(A+B)-C=A+(B-C).$” is true. Indeed, for any matrices $A,B\in L,$ we obtain that 

$$
(A+B)-C=(A+B)+(-C)=A+(B+(-C))=A+(B-C).
$$

since matrix addition is associative.

Therefore, the correct answer is “The  zero-matrix $\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}$ belongs to $L.$”; “For any $A\in L,$ we can find the corresponding negative matrix $-A\in L$ such that $A+(-A)=O.$”; “For any $A,B,C\in L,$ we have $(A+B)-C=A+(B-C).$”.

Answer For any $A,B,C\in L,$ we have $(A+B)-C=A+(B-C).$: true

Answer For any $A\in L,$ we can find the corresponding negative matrix $-A\in L$ such that $A+(-A)=O.$: true

Answer The  zero-matrix $\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}$ belongs to $L.$: true

### Verifying Properties Involving Scalar Multiplication and the Distributive Laws (17 captured questions)

Question 17592186124767 — question.difficulty/moderate

Let $S$ be the set of all $2\times 2$ real matrices with determinant $1.$ Which of the following statements are true?

Select all that apply.

Solution: Let's examine each of our statements in turn.

- Statement “For any $A\in S,$ we have $1\cdot A=A.$” is true. Indeed, for any $2\times 2$ matrix $A=({a}_{ij})\in S,$ the entries are just real numbers. Thus, we have

$$
1\cdot {a}_{ij}={a}_{ij},
$$

and hence,

$$
1\cdot A=A.
$$

- Statements “For any $A\in S$ and $\alpha ,\beta \in R,$ we have $(\alpha +\beta )A=\alpha A+\beta A.$” is true. Indeed, for any $2\times 2$ matrix $A=({a}_{ij})\in S,$ the entries are just real numbers. Thus, for any $\alpha ,\beta \in R,$ we obtain that

$$
(\alpha +\beta ){a}_{ij}=\alpha {a}_{ij}+\beta {a}_{ij},
$$

and hence,

$$
(\alpha +\beta )A=\alpha A+\beta A.
$$

- Statement “There is a matrix $A\in S$ such that $\frac{1}{2}(2A)\ne A.$” is false. For a matrix in $A\in S,$ we have that

$$
\frac{1}{2}(2A)=\left(\frac{1}{2}\cdot 2\right)A=1\cdot A=A
$$

since the scalar multiplication of matrices is associative.

Therefore, the correct answer is “For any $A\in S,$ we have $1\cdot A=A.$”; “For any $A\in S$ and $\alpha ,\beta \in R,$ we have $(\alpha +\beta )A=\alpha A+\beta A.$” only.

Answer For any $A\in S$ and $\alpha ,\beta \in R,$ we have $(\alpha +\beta )A=\alpha A+\beta A.$: true

Answer For any $A\in S,$ we have $1\cdot A=A.$: true

Answer There is a matrix $A\in S$ such that $\frac{1}{2}(2A)\ne A.$: false

Question 17592186125242 — question.difficulty/moderate

Let $L$ be the set of all functions from $(0,\infty )$ to $R$ of the form $f(x)=a{\log }_{2}⁡(x),$ where $a\in R.$ Which of the following statements are true?

Select all that apply.

Solution: Let's examine each of our statements in turn.

- Statement “The scalar multiplication of functions in $L$ is associative” is true. Indeed, for any $f(x)\in L$ and for any fixed $x\in (0,\infty ),$ the result of $f(x)$ is just a real number. Thus, for any $\alpha ,\beta \in R,$ we obtain that

$$
\alpha (\beta f(x))=(\alpha \beta )f(x).
$$

- Statement “For any $\alpha ,\beta \in R$ and $f(x)\in L,$ we have $(\alpha +\beta )f(x)=\alpha f(x)+\beta f(x).$” is true. Indeed, for any $f(x)\in L$ and for any fixed $x\in (0,\infty ),$ the result of $f(x)$ is just a real number. Thus, for any $\alpha ,\beta \in R,$ we obtain that

$$
(\alpha +\beta )f(x)=\alpha f(x)+\beta f(x).
$$

- Statement “For any $\alpha \in R$ and any $f(x),g(x)\in L,$ we have $\alpha (f(x)+g(x))=\alpha f(x)+\alpha g(x).$” is true. Indeed, for any $f(x)\in L$ and for any fixed $x\in (0,\infty ),$ the result of $f(x)$ is just a real number. Thus, for any $\alpha \in R,$ we obtain that 

$$
\alpha (f(x)+g(x))=\alpha f(x)+\alpha g(x).
$$

Therefore, the correct answer is “The scalar multiplication of functions in $L$ is associative”; “For any $\alpha ,\beta \in R$ and $f(x)\in L,$ we have $(\alpha +\beta )f(x)=\alpha f(x)+\beta f(x).$”; “For any $\alpha \in R$ and any $f(x),g(x)\in L,$ we have $\alpha (f(x)+g(x))=\alpha f(x)+\alpha g(x).$”.

Answer For any $\alpha ,\beta \in R$ and $f(x)\in L,$ we have $(\alpha +\beta )f(x)=\alpha f(x)+\beta f(x).$: true

Answer For any $\alpha \in R$ and any $f(x),g(x)\in L,$ we have $\alpha (f(x)+g(x))$ $=\alpha f(x)+\alpha g(x).$: true

Answer The scalar multiplication of functions in $L$ is associative.: true

Question 17592186243955 — question.difficulty/moderate

Let $N$ be the set of all functions of the form $f(x)=a|x|,$ where $a\in R.$ Which of the following statements are true?

Select all that apply.

Solution: Let's examine each of our statements in turn.

- Statement “For any $f(x)\in N,$ we have $(-1)\cdot f(x)=f(x).$” is false. As a counterexample, consider $f(x)=|x|\in N.$ Then,

$$
(-1)\cdot f(x)=(-1)\cdot |x|=-|x|\ne |x|.
$$

Hence, $(-1)\cdot f(x)\ne f(x).$

- Statement “For any $f(x)\in N$ and $\alpha ,\beta \in R,$ we have $(\alpha +\beta )f(x)=\alpha f(x)+\beta f(x).$” is true. Indeed, for any function $f(x)\in N$ and any fixed $x\in R,$ the result of $f(x)$ is just a real number. Thus, for any $\alpha ,\beta \in R,$ we obtain that

$$
(\alpha +\beta )f(x)=\alpha f(x)+\beta f(x).
$$

- Statement “For any $f(x),g(x)\in N$ and $\alpha \in R,$ we have $\alpha (f(x)+g(x))$ $=\alpha f(x)$ $+\alpha g(x).$” is true. Indeed, for any functions $f(x),g(x)\in N$ and any fixed $x\in R,$ the results of $f(x)$ and $g(x)$ are just real numbers. Thus, for any $\alpha \in R,$ we obtain that

$$
\alpha (f(x)+g(x))=\alpha f(x)+\alpha g(x).
$$

Therefore, the correct answer is “For any $f(x)\in N$ and $\alpha ,\beta \in R,$ we have $(\alpha +\beta )f(x)=\alpha f(x)+\beta f(x).$”; “For any $f(x),g(x)\in N$ and $\alpha \in R,$ we have $\alpha (f(x)+g(x))$ $=\alpha f(x)$ $+\alpha g(x).$” only.

Answer For any $f(x),g(x)\in N$ and $\alpha \in R,$ we have $\alpha (f(x)+g(x))$ $=\alpha f(x)$ $+\alpha g(x).$: true

Answer For any $f(x)\in N$ and $\alpha ,\beta \in R,$ we have $(\alpha +\beta )f(x)=\alpha f(x)+\beta f(x).$: true

Answer For any $f(x)\in N,$ we have $(-1)\cdot f(x)=f(x).$: false
