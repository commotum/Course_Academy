# 17592186049064 Defining Abstract Vector Spaces

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186185317 — Introduction

In previous lessons, we've seen how some sets equipped with addition and scalar multiplication operations exhibit properties similar to $\mathbb R^n.$ 

In this lesson, we will formally define what we mean by a **vector space.**

First, let $V$ be a set equipped with the following two operations:

Vector addition: 

For any two elements $\mathbf{x}, \mathbf{y} \in V,$ there is a unique element $\mathbf{x}+\mathbf{y}$ that also lies in $V.$ We say that $V$ is **closed under vector addition.**

Scalar multiplication: 

For any element $\mathbf{x} \in V$ and any number $\alpha \in \mathbb{R},$ there is a unique element $\alpha \mathbf{x}$ that also lies in $V.$ We say that $V$ is **closed under scalar multiplication.**

A set $V$ equipped with vector addition and scalar multiplication forms a **vector space** if it satisfies the following **vector space axioms**. 

Axioms of Vector Addition ($+$)

- $\color{black}\textrm{[A1]}$: $\color{blue}\mathbf{x}+\mathbf{y} =  \mathbf{y}+\mathbf{x}$ for any $\mathbf{x}, \mathbf{y} \in V$; vector addition is **commutative**.

- $\color{black}\textrm{[A2]}$: $\color{blue}(\mathbf{x}+\mathbf{y})+\mathbf{z} =  \mathbf{x}+(\mathbf{y}+\mathbf{z})$ for any $\mathbf{x}, \mathbf{y}, \mathbf{z} \in V$; vectors addition is **associative**.

- $\color{black}\textrm{[A3]}$: There exists a **zero-vector** $\mathbf{0}$ such that $\color{blue}\mathbf{x} + \mathbf{0} = \mathbf{x}$.

- $\color{black}\textrm{[A4]}$: For every $\mathbf{x} \in V,$ there exists $-\mathbf{x} \in V$ such that $\color{blue}\mathbf{x} + (-\mathbf{x}) = \mathbf{0}$; $-\mathbf{x}$ is called the **negative** of $\mathbf{x}$.

Axioms of Scalar Multiplication ($\cdot$)

- $\color{black}\textrm{[A5]}$: $\color{blue}1 \cdot \mathbf{x} = \mathbf{x}$ for any $\mathbf{x} \in V$; multiplying by $1$ does not change a vector.

- $\color{black}\textrm{[A6]}$: $\color{blue}\alpha (\beta \mathbf{x}) = (\alpha\beta) \mathbf{x}$ for any numbers $\alpha,\beta \in \mathbb{R}$ and any vector $\mathbf{x} \in V$.

Axioms Connecting Vector Addition and Scalar Multiplication (the Distributive Laws)

- $\color{black}\textrm{[A7]}$: $\color{blue}(\alpha + \beta)\mathbf{x} = \alpha \mathbf{x} + \beta \mathbf{x}$ for any numbers $\alpha,\beta \in \mathbb{R}$ and any vector $\mathbf{x} \in V$.

- $\color{black}\textrm{[A8]}$: $\color{blue}\alpha (\mathbf{x} + \mathbf{y}) = \alpha \mathbf{x} + \alpha \mathbf{y}$ for any number $\alpha \in \mathbb{R}$ and any vectors $\mathbf{x}, \mathbf{y} \in V$.

So, a vector space is simply a collective term for all kinds of sets equipped with addition and scalar multiplication, where these operations satisfy this particular list of axioms (which are similar to the properties of these operations in $\mathbb{R}^n$). 

The elements of any vector space are called **vectors**.



### tutorial 17592186185345 — Important Vector Spaces

There are many different vector spaces. Some of the most important are listed below.

- $\mathbb{R}^n$, the set of all column vectors of height $n$ with elements from $\mathbb{R}$

- $\text{M}_n(\mathbb{R})$, the set of all $n \times n$ matrices with elements from $\mathbb{R}$

- $\mathbb{R}[t]$, the set of all polynomials in the variable $t$ and with coefficients from $\mathbb{R}$

- $\mathbb{R}_n[t]$, the set of all polynomials of degree less than or equal to $n$ in the variable $t$ and with coefficients from $\mathbb{R}$

- The set of all real-valued functions of one variable.



### example 17592186184094 — Identifying Sets That Are Not Vector Spaces

Let $V$ be the set of all real polynomials of degree exactly $3$, equipped with the usual addition and scalar multiplication operations. Complete the following sentence:

*$V$ is **not** a vector space because $\textrm{_________}\,.$*

I. the sum of two polynomials of degree $3$ may not be a polynomial of degree $3$

II. $V$ does not contain the polynomial $-p(x)$ for every $p(x) \in V$

III. addition of polynomials is not commutative

The correct answer  is as follows:

*$V$ is **not** a vector space because **the sum of two polynomials of degree $3$ may not be a polynomial of degree $3$.*** 

For instance, if $p(x) = 1 +x^3$ and $q(x) = 1-x^3$, then $p(x)$ and $q(x)$ are in $V.$ However  

$$
\begin{aligned}p(x)+q(x) & =(1+{x}^{3})+(1-{x}^{3}) \\  & =2\notin V.\end{aligned}
$$

On the other hand:

- Addition of polynomials is commutative.

- For any polynomial $p(x)$ of degree $3$, the corresponding negative polynomial $-p(x)$ also has degree $3.$

### example 17592186184065 — Proving Statements Using the Vector Space Axioms

From top to bottom, fill in the blanks and hence complete the proof of the following statement using the axioms $[\textrm A1] - [\textrm A8]$ given below.

*Statement:* 

*If $\mathbf{w}$ is a vector such that $\mathbf{w}+\mathbf{w} = \mathbf{w}$, then $\mathbf{w}=\mathbf{0}.$* 

*Proof:*

$$
\begin{aligned}\mathbf{w}+\mathbf{w} & =\mathbf{w} &  & [\hspace{0.222em}\text{given}\hspace{0.222em}] \\ (\mathbf{w}+\mathbf{w})+(-\mathbf{w}) & =\mathbf{w}+(-\mathbf{w}) &  & [\hspace{0.222em}\text{add }-\mathbf{w}\text{ to both sides}\hspace{0.222em}] \\ \mathbf{w}+(\mathbf{w}+(-\mathbf{w})) & =\mathbf{w}+(-\mathbf{w}) &  & [\hspace{0.222em}\text{axiom __}\hspace{0.222em}\hspace{0.222em}] \\ \mathbf{w}+\mathbf{0} & =\mathbf{0} &  & [\hspace{0.222em}\text{axiom A4}\hspace{0.222em}] \\ \mathbf{w} & =\mathbf{0} &  & [\hspace{0.222em}\text{axiom __}\hspace{0.222em}\hspace{0.222em}]\end{aligned}
$$

The axioms:

$$
\begin{array}{ll}{\color{black}\text{[A1]}}:{\color{blue}\mathbf{x}+\mathbf{y}=\mathbf{y}+\mathbf{x}} & {\color{black}\text{[A5]}}:{\color{blue}1\cdot \mathbf{x}=\mathbf{x}} \\ {\color{black}\text{[A2]}}:{\color{blue}(\mathbf{x}+\mathbf{y})+\mathbf{z}=\mathbf{x}+(\mathbf{y}+\mathbf{z})} & {\color{black}\text{[A6]}}:{\color{blue}\alpha (\beta \mathbf{x})=(\alpha \beta )\mathbf{x}} \\ {\color{black}\text{[A3]}}:{\color{blue}\mathbf{x}+\mathbf{0}=\mathbf{x}} & {\color{black}\text{[A7]}}:{\color{blue}(\alpha +\beta )\mathbf{x}=\alpha \mathbf{x}+\beta \mathbf{x}} \\ {\color{black}\text{[A4]}}:{\color{blue}\mathbf{x}+(-\mathbf{x})=\mathbf{0}} & {\color{black}\text{[A8]}}:{\color{blue}\alpha (\mathbf{x}+\mathbf{y})=\alpha \mathbf{x}+\alpha \mathbf{y}}\end{array}
$$

Using the axioms of a vector space, we obtain the following:

$$
\begin{aligned}\mathbf{w}+\mathbf{w} & =\mathbf{w} &  & [\hspace{0.222em}\text{given}\hspace{0.222em}] \\ (\mathbf{w}+\mathbf{w})+(-\mathbf{w}) & =\mathbf{w}+(-\mathbf{w}) &  & [\hspace{0.222em}\text{add }-\mathbf{w}\text{ to both sides}\hspace{0.222em}] \\ \mathbf{w}+(\mathbf{w}+(-\mathbf{w})) & =\mathbf{w}+(-\mathbf{w}) &  & [\hspace{0.222em}\text{axiom }{\color{blue}\text{A2}}\hspace{0.222em}] \\ \mathbf{w}+\mathbf{0} & =\mathbf{0} &  & [\hspace{0.222em}\text{axiom A4}\hspace{0.222em}] \\ \mathbf{w} & =\mathbf{0} &  & [\hspace{0.222em}\text{axiom }{\color{blue}\text{A3}}\hspace{0.222em}]\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Identifying Sets That Are Not Vector Spaces (17 captured questions)

Question 17592186184761 — question.difficulty/easy

Let $W$ be the set of all polynomials in the variable $x\in \mathbb{R}$ with coefficients in $\mathbb{R}$ of degree $5$ or greater. Complete the following sentence:

*$W$ is **not** a vector space (with respect to polynomials addition and multiplication of a polynomial by a real number) because $\text{_________}\,.$*

Solution: The correct answer is as follows:

*$W$ is **not** a vector space (with respect to polynomials addition and multiplication of a polynomial by a real number) because **$W$ does not contain the zero element.*** 

Indeed, the zero polynomial is not a polynomial of degree $5$ or greater. Its degree is undefined (or is assigned $-\infty$ by convention).

On the other hand: 

- Addition of polynomials is associative. $\hspace{0.222em}{\color{green}✓}$

- Addition of polynomials is commutative. $\hspace{0.222em}{\color{green}✓}$

- Addition and scalar multiplication of polynomials satisfy the distributive laws. $\hspace{0.222em}{\color{green}✓}$

- For any polynomial $p(x)$ of degree $5$ (or greater), the corresponding negative polynomial $-p(x)$ has the same degree. $\hspace{0.222em}{\color{green}✓}$

Answer selection: $W$ does not contain the zero element

Question 17592186184763 — question.difficulty/moderate

Let $C$ be the set of functions $f:\mathbb{R}\to \mathbb{R}$ such that $f(x)\ge 0$ for all $x\in \mathbb{R}.$ Complete the following sentence:

*$C$ is **not** a vector space (with respect to function addition and scalar multiplication of a function by a real number) because $\text{_________}\,.$*

Solution: The correct answer is as follows:

*$C$ is **not** a vector space (with respect to function addition and scalar multiplication of a function by a real number) because **multiplication of $f\in C$ by a scalar is not closed.*** 

For example, if $\alpha =-1$ and $f(x)={x}^{2}+1,$ then $\alpha f(x)=-f(x)<0$ for all $x\in \mathbb{R}.$

On the other hand:

- Addition of $f,g\in C$ is associative. $\hspace{0.222em}{\color{green}✓}$

- $C$ contains the zero element. Indeed, the function $e(x),$ such that $e(x)=0$ for all $x\in \mathbb{R},$ belongs to $C.$ This function is the zero element of $C$ since $e(x)+f(x)=f(x)+e(x)=f(x)$ for any $f(x)\in C.$ $\hspace{0.222em}{\color{green}✓}$

- $1\cdot f=f$ for all $f\in C.$ $\hspace{0.222em}{\color{green}✓}$

- Addition of $f,g\in C$ is commutative. $\hspace{0.222em}{\color{green}✓}$

Answer selection: multiplication of $f\in C$ by a scalar is not closed

Question 17592186243958 — question.difficulty/moderate

Let $F$ be the set of functions $f:\mathbb{R}\to \mathbb{R}$ such that $f(0)=\frac{1}{2}.$ Complete the following sentence:

*$F$ is **not** a vector space (with respect to function addition and scalar multiplication of a function by a real number) because $\text{_________}\,.$*

Solution: The correct answer is as follows:

*$F$ is **not** a vector space (with respect to function addition and scalar multiplication of a function by a real number) because **$F$ does not contain the zero element.*** 

Indeed, evaluating the zero function $f(x)=0$ at $x=0,$ we have $f(0)=0\ne \frac{1}{2}.$

On the other hand:

- Addition of $f,g\in F$ is associative. $\hspace{0.222em}{\color{green}✓}$

- Addition of $f,g\in F$ is commutative. $\hspace{0.222em}{\color{green}✓}$

- $1\cdot f=f$ for all $f\in F.$ $\hspace{0.222em}{\color{green}✓}$

- Addition and scalar multiplication of functions satisfy the distributive laws. $\hspace{0.222em}{\color{green}✓}$

Answer selection: $F$ does not contain the zero element

### Proving Statements Using the Vector Space Axioms (17 captured questions)

Question 17592186184762 — question.difficulty/hard

From top to bottom, fill in the blanks and hence complete the proof of the following statement using the axioms $[\text{A}1]-[\text{A}8]$ given below.

*Statement:* 

*$\alpha \mathbf{0}=\mathbf{0}$ for any $\alpha \in \mathbb{R}$*

*Proof:*

$$
\begin{aligned}\alpha \mathbf{0} & =\alpha \mathbf{0} &  & [\hspace{0.222em}\text{given}\hspace{0.222em}] \\ \alpha \mathbf{0} & =\alpha (\mathbf{0}+\mathbf{0}) &  & [\hspace{0.222em}\text{axiom A3}\hspace{0.222em}] \\ \alpha \mathbf{0} & =\alpha \mathbf{0}+\alpha \mathbf{0} &  & [\hspace{0.222em}\text{axiom __}\hspace{0.222em}\hspace{0.222em}] \\ \alpha \mathbf{0}+(-\alpha \mathbf{0}) & =(\alpha \mathbf{0}+\alpha \mathbf{0})+(-\alpha \mathbf{0}) &  & [\hspace{0.222em}\text{add }-\alpha \mathbf{0}\text{ to both sides}\hspace{0.222em}] \\ \alpha \mathbf{0}+(-\alpha \mathbf{0}) & =\alpha \mathbf{0}+(\alpha \mathbf{0}+(-\alpha \mathbf{0})) &  & [\hspace{0.222em}\text{axiom A2}\hspace{0.222em}] \\ \mathbf{0} & =\alpha \mathbf{0}+\mathbf{0} &  & [\hspace{0.222em}\text{axiom A4}\hspace{0.222em}] \\ \mathbf{0} & =\alpha \mathbf{0} &  & [\hspace{0.222em}\text{axiom __}\hspace{0.222em}\hspace{0.222em}]\end{aligned}
$$

The axioms:

$$
\begin{array}{ll}{\color{black}\text{[A1]}}:{\color{blue}\mathbf{x}+\mathbf{y}=\mathbf{y}+\mathbf{x}} & {\color{black}\text{[A5]}}:{\color{blue}1\cdot \mathbf{x}=\mathbf{x}} \\ {\color{black}\text{[A2]}}:{\color{blue}(\mathbf{x}+\mathbf{y})+\mathbf{z}=\mathbf{x}+(\mathbf{y}+\mathbf{z})} & {\color{black}\text{[A6]}}:{\color{blue}\alpha (\beta \mathbf{x})=(\alpha \beta )\mathbf{x}} \\ {\color{black}\text{[A3]}}:{\color{blue}\mathbf{x}+\mathbf{0}=\mathbf{x}} & {\color{black}\text{[A7]}}:{\color{blue}(\alpha +\beta )\mathbf{x}=\alpha \mathbf{x}+\beta \mathbf{x}} \\ {\color{black}\text{[A4]}}:{\color{blue}\mathbf{x}+(-\mathbf{x})=\mathbf{0}} & {\color{black}\text{[A8]}}:{\color{blue}\alpha (\mathbf{x}+\mathbf{y})=\alpha \mathbf{x}+\alpha \mathbf{y}}\end{array}
$$

Solution: Using the vector space axioms, we obtain the following:

$$
\begin{aligned}\alpha \mathbf{0} & =\alpha \mathbf{0} &  & [\hspace{0.222em}\text{given}\hspace{0.222em}] \\ \alpha \mathbf{0} & =\alpha (\mathbf{0}+\mathbf{0}) &  & [\hspace{0.222em}\text{axiom A3}\hspace{0.222em}] \\ \alpha \mathbf{0} & =\alpha \mathbf{0}+\alpha \mathbf{0} &  & [\hspace{0.222em}\text{axiom }{\color{blue}\text{A8}}\hspace{0.222em}] \\ \alpha \mathbf{0}+(-\alpha \mathbf{0}) & =(\alpha \mathbf{0}+\alpha \mathbf{0})+(-\alpha \mathbf{0}) &  & [\hspace{0.222em}\text{add }-\alpha \mathbf{0}\text{ to both sides}\hspace{0.222em}] \\ \alpha \mathbf{0}+(-\alpha \mathbf{0}) & =\alpha \mathbf{0}+(\alpha \mathbf{0}+(-\alpha \mathbf{0})) &  & [\hspace{0.222em}\text{axiom A2}\hspace{0.222em}] \\ \mathbf{0} & =\alpha \mathbf{0}+\mathbf{0} &  & [\hspace{0.222em}\text{axiom A4}\hspace{0.222em}] \\ \mathbf{0} & =\alpha \mathbf{0} &  & [\hspace{0.222em}\text{axiom }{\color{blue}\text{A3}}\hspace{0.222em}]\end{aligned}
$$

Answer selection: $\text{A8}$, $\text{A3}$

Question 17592186184764 — question.difficulty/hard

From top to bottom, fill in the blanks and hence complete the proof of the following statement using the axioms $[\text{A}1]-[\text{A}8]$ given below.

*Statement:*

*If $\mathbf{w}$ is a vector such that $\mathbf{x}+\mathbf{w}=\mathbf{x}$ for some $\mathbf{x}\in V$, then $\mathbf{w}=\mathbf{0}.$*

*Proof:*

$$
\begin{aligned}\mathbf{x}+\mathbf{w} & =\mathbf{x} &  & [\hspace{0.222em}\text{given}\hspace{0.222em}] \\ (\mathbf{x}+\mathbf{w})+(-\mathbf{x}) & =\mathbf{x}+(-\mathbf{x}) &  & [\hspace{0.222em}\text{add }-\mathbf{x}\text{ to both sides}\hspace{0.222em}] \\ (\mathbf{w}+\mathbf{x})+(-\mathbf{x}) & =\mathbf{x}+(-\mathbf{x}) &  & [\hspace{0.222em}\text{axiom __}\hspace{0.222em}\hspace{0.222em}] \\ \mathbf{w}+(\mathbf{x}+(-\mathbf{x})) & =\mathbf{x}+(-\mathbf{x}) &  & [\hspace{0.222em}\text{axiom A2}\hspace{0.222em}] \\ \mathbf{w}+\mathbf{0} & =\mathbf{0} &  & [\hspace{0.222em}\text{axiom A4}\hspace{0.222em}] \\ \mathbf{w} & =\mathbf{0} &  & [\hspace{0.222em}\text{axiom __}\hspace{0.222em}\hspace{0.222em}]\end{aligned}
$$

The axioms:

$$
\begin{array}{ll}{\color{black}\text{[A1]}}:{\color{blue}\mathbf{x}+\mathbf{y}=\mathbf{y}+\mathbf{x}} & {\color{black}\text{[A5]}}:{\color{blue}1\cdot \mathbf{x}=\mathbf{x}} \\ {\color{black}\text{[A2]}}:{\color{blue}(\mathbf{x}+\mathbf{y})+\mathbf{z}=\mathbf{x}+(\mathbf{y}+\mathbf{z})} & {\color{black}\text{[A6]}}:{\color{blue}\alpha (\beta \mathbf{x})=(\alpha \beta )\mathbf{x}} \\ {\color{black}\text{[A3]}}:{\color{blue}\mathbf{x}+\mathbf{0}=\mathbf{x}} & {\color{black}\text{[A7]}}:{\color{blue}(\alpha +\beta )\mathbf{x}=\alpha \mathbf{x}+\beta \mathbf{x}} \\ {\color{black}\text{[A4]}}:{\color{blue}\mathbf{x}+(-\mathbf{x})=\mathbf{0}} & {\color{black}\text{[A8]}}:{\color{blue}\alpha (\mathbf{x}+\mathbf{y})=\alpha \mathbf{x}+\alpha \mathbf{y}}\end{array}
$$

Solution: Using the vector space axioms, we obtain the following:

$$
\begin{aligned}x+w & =x &  & [\,\text{given}\,] \\ (x+w)+(-x) & =x+(-x) &  & [\,\text{add }-x\text{ to both sides}\,] \\ (w+x)+(-x) & =x+(-x) &  & [\,\text{axiom }\text{A1}\,] \\ w+(x+(-x)) & =x+(-x) &  & [\,\text{axiom A2}\,] \\ w+0 & =0 &  & [\,\text{axiom A4}\,] \\ w & =0 &  & [\,\text{axiom }\text{A3}\,]\end{aligned}
$$

Answer selection: $\text{A1}$, $\text{A3}$

Question 17592186243984 — question.difficulty/hard

From top to bottom, fill in the blanks and hence complete the proof of the following statement using the axioms $[\text{A}1]-[\text{A}8]$ given below.

*Statement:*

*Given any $\mathbf{x}\in V$, if $\mathbf{y}$ is a vector such that $\mathbf{x}+\mathbf{y}=\mathbf{0}$, then $\mathbf{y}=-\mathbf{x}.$* 

*Proof:*

$$
\begin{aligned}\mathbf{x}+\mathbf{y} & =\mathbf{0} &  & [\hspace{0.222em}\text{given}\hspace{0.222em}] \\ (\mathbf{x}+\mathbf{y})+(-\mathbf{x}) & =\mathbf{0}+(-\mathbf{x}) &  & [\hspace{0.222em}\text{add }-\mathbf{x}\text{ to both sides}\hspace{0.222em}] \\ (\mathbf{y}+\mathbf{x})+(-\mathbf{x}) & =(-\mathbf{x})+\mathbf{0} &  & [\hspace{0.222em}\text{axiom A1}\hspace{0.222em}] \\ (\mathbf{y}+\mathbf{x})+(-\mathbf{x}) & =-\mathbf{x} &  & [\hspace{0.222em}\text{axiom __}\hspace{0.222em}\hspace{0.222em}] \\ \mathbf{y}+(\mathbf{x}+(-\mathbf{x})) & =-\mathbf{x} &  & [\hspace{0.222em}\text{axiom __}\hspace{0.222em}\hspace{0.222em}] \\ \mathbf{y}+\mathbf{0} & =-\mathbf{x} &  & [\hspace{0.222em}\text{axiom A4}\hspace{0.222em}] \\ \mathbf{y} & =-\mathbf{x} &  & [\hspace{0.222em}\text{axiom A3}\hspace{0.222em}]\end{aligned}
$$

The axioms:

$$
\begin{array}{ll}{\color{black}\text{[A1]}}:{\color{blue}\mathbf{x}+\mathbf{y}=\mathbf{y}+\mathbf{x}} & {\color{black}\text{[A5]}}:{\color{blue}1\cdot \mathbf{x}=\mathbf{x}} \\ {\color{black}\text{[A2]}}:{\color{blue}(\mathbf{x}+\mathbf{y})+\mathbf{z}=\mathbf{x}+(\mathbf{y}+\mathbf{z})} & {\color{black}\text{[A6]}}:{\color{blue}\alpha (\beta \mathbf{x})=(\alpha \beta )\mathbf{x}} \\ {\color{black}\text{[A3]}}:{\color{blue}\mathbf{x}+\mathbf{0}=\mathbf{x}} & {\color{black}\text{[A7]}}:{\color{blue}(\alpha +\beta )\mathbf{x}=\alpha \mathbf{x}+\beta \mathbf{x}} \\ {\color{black}\text{[A4]}}:{\color{blue}\mathbf{x}+(-\mathbf{x})=\mathbf{0}} & {\color{black}\text{[A8]}}:{\color{blue}\alpha (\mathbf{x}+\mathbf{y})=\alpha \mathbf{x}+\alpha \mathbf{y}}\end{array}
$$

Solution: Using the vector space axioms, we obtain the following:

$$
\begin{aligned}\mathbf{x}+\mathbf{y} & =\mathbf{0} &  & [\hspace{0.222em}\text{given}\hspace{0.222em}] \\ (\mathbf{x}+\mathbf{y})+(-\mathbf{x}) & =\mathbf{0}+(-\mathbf{x}) &  & [\hspace{0.222em}\text{add }-\mathbf{x}\text{ to both sides}\hspace{0.222em}] \\ (\mathbf{y}+\mathbf{x})+(-\mathbf{x}) & =(-\mathbf{x})+\mathbf{0} &  & [\hspace{0.222em}\text{axiom A1}\hspace{0.222em}] \\ (\mathbf{y}+\mathbf{x})+(-\mathbf{x}) & =-\mathbf{x} &  & [\hspace{0.222em}\text{axiom }{\color{blue}\text{A3}}\hspace{0.222em}\hspace{0.222em}] \\ \mathbf{y}+(\mathbf{x}+(-\mathbf{x})) & =-\mathbf{x} &  & [\hspace{0.222em}\text{axiom }{\color{blue}\text{A2}}\hspace{0.222em}\hspace{0.222em}] \\ \mathbf{y}+\mathbf{0} & =-\mathbf{x} &  & [\hspace{0.222em}\text{axiom A4}\hspace{0.222em}] \\ \mathbf{y} & =-\mathbf{x} &  & [\hspace{0.222em}\text{axiom A3}\hspace{0.222em}]\end{aligned}
$$

Answer selection: $\text{A3}$, $\text{A2}$
