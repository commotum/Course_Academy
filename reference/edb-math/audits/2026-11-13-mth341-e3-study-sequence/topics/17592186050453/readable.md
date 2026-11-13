# 17592186050453 Subspaces of Abstract Vector Spaces

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186125762 — Introduction

Given a vector space $V$, any subset $H$ of $V,$ which is itself a vector space, is called a **subspace** of $V$. 

Fortunately, we do not need to check all vector space axioms to determine whether a subset of some vector space is a subspace. Instead, we only need to check the **subspace criterion**, which states the following:

*A subset $H$ of a vector space $V$ is a subspace of $V$ if and only if $H$ is closed under vector addition and scalar multiplication. That is to say, both of the following conditions hold:*

- *If $\mathbf{u}$ and $\mathbf{v}$ lie in $H$, then their sum $\mathbf{u}+\mathbf{v}$ also lies in $H$. Formally,*

$$
\mathbf{u},\mathbf{v} \in H \quad\Rightarrow\quad  \mathbf{u}+\mathbf{v} \in H.
$$

- *If $\mathbf{u}$ lies in $H$, then $k \cdot \mathbf{u}$ also lies in $H$ for any scalar  $k$. Formally,* 

$$
k \in \mathbb{R}, \,\mathbf{u} \in H \quad\Rightarrow\quad  k\cdot\mathbf{u} \in H.
$$

For example, consider the vector space $\mathbb{R}_3[t]$ containing all polynomials of degree at most $3,$ along with the subset 

$$
A = \{ at^2 \:|\: a \in \mathbb{R} \}.
$$

Is $A$ a subspace? Let's check the two subspace criterion conditions: 

- Suppose $p_1(t)=a_1 t^2$ and $p_2(t)=a_2 t^2$ are two polynomials from $A$. Summing the two polynomials, we get

$$
\begin{aligned}{p}_{1}(t)+{p}_{2}(t) & =({a}_{1}{t}^{2})+({a}_{2}{t}^{2}) \\  & =\underbrace{({a}_{1}+{a}_{2})}_{a\in R}{t}^{2}.\end{aligned}
$$

 
Thus, $p_1(t)+p_2(t)$ is a polynomial of the form $at^2,$ which belongs to $A$.

- If $p_1(t)=a_1 t^2 \in A$ and $k \in \mathbb{R},$ then 

$$
\begin{aligned}k{p}_{1}(t) & =k({a}_{1}{t}^{2}) \\  & =\underbrace{(k{a}_{1})}_{a\in R}{t}^{2}.\end{aligned}
$$

 
Thus, $kp_1(t)$ is a polynomial of the form $at^2,$ which belongs to $A$.

Since both conditions hold, we conclude that $A$ is a subspace $\mathbb{R}_3[t].$



### tutorial 17592186125858 — Example of a Subset That Is Not a Subspace

Let's now look at an example of a subset of a vector space that is not a subspace.

Consider the vector space $\mathbb R_2[t]$ of all polynomials in the variable $t$ of degree at most $2,$ and its subset 

$$
B = \big\{ at+b \: | \: a,b  \in\mathbb{Z} \big\}.
$$

Recall that a subset of a vector space is a subspace if it's closed under addition and scalar multiplication.

- $B$ is closed under polynomial addition. Indeed, suppose that $f(t)=a_1t+b_1$ and $g(t)=a_2t+b_2$ are two polynomials from $B.$ Then,

$$
\begin{aligned}f(t)+g(t) & =({a}_{1}t+{b}_{1})+({a}_{2}t+{b}_{2}) \\  & =({a}_{1}+{a}_{2})t+({b}_{1}+{b}_{2}),\end{aligned}
$$

which is a polynomial from $B$ since $a_1+a_2$ and $b_1+b_2$ are in $\Bbb Z.$

- $B$ is *not* closed under scalar multiplication. As a counterexample, consider $f(t)=t$ and $k=0.5,$ then 

$$
\begin{aligned}kf(t) & =0.5t,\end{aligned}
$$

which is *not* a polynomial from $B,$ because $0.5 \notin \Bbb Z.$

Therefore, $B$ is not a subspace of $\mathbb R_2[t].$



### example 17592186124402 — Identifying Subspaces of Polynomial Vector Spaces

Consider the vector space $\mathbb R_3[t]$ of all polynomials in the variable $t$ of degree at most $3,$ and its subset $A = \big\{ at^3-bt \: | \: a,b \in\mathbb{R} \big\}.$

Which of the following statements are true?

I. $A$ is closed under polynomial addition

II. $A$ is closed under scalar multiplication

III. $A$ is a subspace of $\mathbb R_3[t]$

IV. $A$ is **not** a subspace of $\mathbb R_3[t]$

Recall that a subset of a vector space is a subspace if it's closed under addition and scalar multiplication.

With that in mind, let's examine each statement in turn.

- Statement I is true. If $f(t)=a_1t^3-b_1t$ and $g(t)=a_2t^3-b_2t$ are two polynomials from $A,$ then

$$
\begin{aligned}f(t)+g(t) & =({a}_{1}{t}^{3}-{b}_{1}t)+({a}_{2}{t}^{3}-{b}_{2}t) \\  & =({a}_{1}+{a}_{2}){t}^{3}-({b}_{1}+{b}_{2})t,\end{aligned}
$$

which is a polynomial from $A.$ So, $A$ is closed under addition.

- Statement II is true. If $f(t)=at^3-bt \in A$ and $k \in \mathbb{R},$ then 

$$
\begin{aligned}kf(t) & =k(a{t}^{3}-bt) \\  & =(ka){t}^{3}-(kb)t,\end{aligned}
$$

which is a polynomial from $A.$ So, $A$ is closed under scalar multiplication.

- Statement III is true. $A$ is a subspace because it's closed under addition and scalar multiplication.

Therefore, the correct answer is "I, II, and III only."

### example 17592186124401 — Identifying Subspaces of Matrix Vector Spaces

Consider the vector space $\text{M}_2(\mathbb{R})$ of all $2\times 2$ matrices over $\mathbb{R},$ and its subset $N$ containing all $2\times 2$ matrices such that the sum of the elements on the main diagonal is greater or equal to $0.$

Which of the following statements are true?

I. $N$ is closed under matrix addition

II. $N$ is closed under scalar multiplication

III. $N$ is a subspace of $\text{M}_2(\mathbb{R})$

IV. $N$ is **not** a subspace of $\text{M}_2(\mathbb{R})$

Recall that a subset of a vector space is a subspace if it's closed under addition and scalar multiplication.

With that in mind, let's examine each statement in turn.

- Statement I is true. If $A_1$ and $A_2$ are two matrices from $N,$ then the sum of the elements on the main diagonal for each matrix is greater or equal to $0.$ Therefore, $A_1+A_2$ is a matrix where the sum of the elements on the main diagonal is greater or equal to $0.$ This matrix belongs to $N,$  and so $N$ is closed under addition.

- Statement II is false. If $A$ is an element of $N,$ then the sum of the elements on the main diagonal is greater than or equal to $0.$ If we let $k=-1 \in \mathbb{R},$ then $kA$ is a matrix where the sum of the elements on the main diagonal is less than or equal to $0.$ This matrix does not belong to $N,$  and so $N$ is *not* closed under scalar multiplication.

- Statement III is false, while statement IV is true. $N$ is a *not* subspace because it's not closed under scalar multiplication.

Therefore, the correct answer is "I and IV only."

### example 17592186124301 — Identifying Subspaces of Function Vector Spaces

Consider the vector space $\mathcal{C}[-1,3]$ of all continuous functions $f:[-1,3] \to \mathbb{R}$ and its subset $A = \big\{ f \in \mathcal{C}[-1,3] \: | \: f(0)=-f(2) \big\}.$ 

Which of the following statements are true?

I. $A$ is closed under function addition

II. $A$ is closed under scalar multiplication

III. $A$ is a subspace of $\mathcal{C}[-1,3]$

IV. $A$ is **not** a subspace of $\mathcal{C}[-1,3]$

Recall that a subset of a vector space is a subspace if it's closed under addition and scalar multiplication.

With that in mind, let's examine each statement in turn.

- Statement I is true. If $f(x),g(x) \in A,$ then

$$
\begin{aligned}(f+g)(0) & =f(0)+g(0) \\  & =-f(2)-g(2) \\  & =-(f(2)+g(2)) \\  & =-(f+g)(2),\end{aligned}
$$

which means $f+g \in A.$ So, $A$ is closed under addition.

- Statement II is true. If $f(x) \in A$ and $k \in \mathbb{R},$ then 

$$
\begin{aligned}(kf)(0) & =kf(0) \\  & =k\cdot (-f(2)) \\  & =-kf(2) \\  & =-(kf)(2),\end{aligned}
$$

which means $kf \in A.$ So, $A$ is closed under scalar multiplication.

- Statement III is true. $A$ is a subspace because it's closed under addition and scalar multiplication.

Therefore, the correct answer is "I, II, and III only."

## Representative practice (first three per skill; full bank in practice.json)

### Identifying Subspaces of Polynomial Vector Spaces (13 captured questions)

Question 17592186125152 — None

Consider the vector space $R_{3}[t]$ of all polynomials in the variable $t$ of degree at most $3$, and its subset $A$ containing all polynomials of the form $at^{3}$, where $a ∈ R$.

Which of the following statements are true?

1. $A$ is closed under polynomial addition
2. $A$ is closed under scalar multiplication
3. $A$ is a subspace of $R_{3}[t]$
4. $A$ is **not** a subspace of $R_{3}[t]$

Solution: 

Question 17592186125153 — question.difficulty/moderate

Consider the vector space ${R}_{2}[t]$ of all polynomials in the variable $t$ of degree at most $2,$ and its subset $B={{t}^{2}+at+b\,|\,a,b\in R}.$

Which of the following statements are true?

Select all that apply.

Solution: Recall that a subset of a vector space is a subspace if it's closed under addition and scalar multiplication.

With that in mind, let's examine each statement in turn.

- Statement “$B$ is closed under polynomial addition” is false. For example, if $f(t)=g(t)={t}^{2},$ then

$$
\begin{aligned}f(t)+g(t) & ={t}^{2}+{t}^{2} \\  & =2{t}^{2},\end{aligned}
$$

which is not a polynomial from $B.$ So, $B$ is *not* closed under addition.

- Statement “$B$ is closed under scalar multiplication” is false. For example, if $f(t)={t}^{2}$ and $k=2,$ then 

$$
\begin{aligned}kf(t) & =2{t}^{2},\end{aligned}
$$

which is not a polynomial from $B.$ So, $B$ is *not* closed under scalar multiplication.

- Statement “$B$ is a subspace of ${R}_{2}[t]$” is false, while statement “$B$ is a **not** a subspace of ${R}_{2}[t]$” is true. $B$ is *not* a subspace because it's not closed under addition and scalar multiplication.

Therefore, the correct answer is “$B$ is a **not** a subspace of ${R}_{2}[t]$” only.

Answer $B$ is a **not** a subspace of ${R}_{2}[t]$: true

Answer $B$ is a subspace of ${R}_{2}[t]$: false

Answer $B$ is closed under polynomial addition: false

Answer $B$ is closed under scalar multiplication: false

Question 17592186244019 — question.difficulty/easy

Consider the vector space ${R}_{5}[t]$ of all polynomials in the variable $t$ of degree at most $5,$ and its subset $A$ containing all polynomials of the form $a{t}^{5}+b,$ where $a,b\in R.$

Which of the following statements are true?

Select all that apply.

Solution: Recall that a subset of a vector space is a subspace if it's closed under addition and scalar multiplication.

With that in mind, let's examine each statement in turn.

- Statement “$A$ is closed under polynomial addition” is true. If $f(t)={a}_{1}{t}^{5}+{b}_{1}$ and $g(t)={a}_{2}{t}^{5}+{b}_{2},$ then

$$
\begin{aligned}f(t)+g(t) & =({a}_{1}{t}^{5}+{b}_{1})+({a}_{2}{t}^{5}+{b}_{2}) \\  & =({a}_{1}+{a}_{2}){t}^{5}+({b}_{1}+{b}_{2}),\end{aligned}
$$

which is a polynomial from $A.$ So, $A$ is closed under addition.

- Statement “$A$ is closed under scalar multiplication” is true. If $f(t)=a{t}^{5}+b$ and $k\in R,$ then 

$$
\begin{aligned}kf(t) & =k(a{t}^{5}+b) \\  & =(ka){t}^{5}+(kb),\end{aligned}
$$

which is a polynomial from $A.$ So, $A$ is closed under scalar multiplication.

- Statement “$A$ is a subspace of ${R}_{5}[t]$” is true while statement “$A$ is **not** a subspace of ${R}_{5}[t]$” is false. $A$ is a subspace because it's closed under addition and scalar multiplication.

Therefore, the correct answer is “$A$ is closed under polynomial addition”; “$A$ is closed under scalar multiplication”; “$A$ is a subspace of ${R}_{5}[t]$” only.

Answer $A$ is **not** a subspace of ${R}_{5}[t]$: false

Answer $A$ is a subspace of ${R}_{5}[t]$: true

Answer $A$ is closed under polynomial addition: true

Answer $A$ is closed under scalar multiplication: true

### Identifying Subspaces of Matrix Vector Spaces (16 captured questions)

Question 17592186125154 — question.difficulty/easy

Consider the vector space ${\text{M}}_{2}(R)$ of all $2\times 2$ matrices over $R$ and its subset $C=\left\{\begin{bmatrix}a & 0 \\ 0 & 0\end{bmatrix}\right.\,|\,a\in R\}.$

Which of the following statements are true?

I. $C$ is closed under matrix addition

II. $C$ is closed under scalar multiplication

III. $C$ is a subspace of ${\text{M}}_{2}(R)$

IV. $C$ is **not** a subspace of ${\text{M}}_{2}(R)$

Solution: Recall that a subset of a vector space is a subspace if it's closed under addition and scalar multiplication.

With that in mind, let's examine each statement in turn.

- Statement I is true. If ${A}_{1}=\begin{bmatrix}{a}_{1} & 0 \\ 0 & 0\end{bmatrix}$ and ${A}_{2}=\begin{bmatrix}{a}_{2} & 0 \\ 0 & 0\end{bmatrix}$ are two matrices from $C,$ then

$$
\begin{aligned}{A}_{1}+{A}_{2} & =\begin{bmatrix}{a}_{1} & 0 \\ 0 & 0\end{bmatrix}+\begin{bmatrix}{a}_{2} & 0 \\ 0 & 0\end{bmatrix} \\  & =\begin{bmatrix}{a}_{1}+{a}_{2} & 0 \\ 0 & 0\end{bmatrix},\end{aligned}
$$

which is a matrix from $C.$ So, $C$ is closed under addition.

- Statement II is true. If $A=\begin{bmatrix}a & 0 \\ 0 & 0\end{bmatrix}$ is an element of $C$ and $k\in R,$ then 

$$
\begin{aligned}kA & =k\begin{bmatrix}a & 0 \\ 0 & 0\end{bmatrix} \\  & =\begin{bmatrix}ka & 0 \\ 0 & 0\end{bmatrix},\end{aligned}
$$

which is a matrix from $C.$ So, $C$ is closed under scalar multiplication.

- Statement III is true, while statement IV is false. $C$ is a subspace because it's closed under addition and scalar multiplication.

Therefore, the correct answer is "I, II, and III only."

Answer selection: I, II, and III only

Question 17592186125155 — question.difficulty/moderate

Consider the vector space ${\text{M}}_{2}(R)$ of all $2\times 2$ matrices over $R,$ and its subset $D$ containing all $2\times 2$ matrices such that the sum of the elements on the main diagonal is equal to $1.$

Which of the following statements are true?

Select all that apply.

Solution: Recall that a subset of a vector space is a subspace if it's closed under addition and scalar multiplication.

With that in mind, let's examine each statement in turn.

- Statement “$D$ is closed under matrix addition” is false. If ${A}_{1}$ and ${A}_{2}$ are two matrices from $D$ such that the sum of the elements on the main diagonal is equal to $1,$ then 

$$
{A}_{1}+{A}_{2}
$$

 is a matrix where the sum of the elements on the main diagonal is equal to 

$$
1+1=2.
$$

 This matrix does not belong to $D.$ So, $D$ is *not* closed under addition.

- Statement “$D$ is closed under scalar multiplication” is false. If $A$ is an element of $D$ such that the sum of the elements on the main diagonal is equal to $1,$ and $k=5\in R,$ then 

$$
kA
$$

 is a matrix such that the sum of the elements on the main diagonal is equal to 

$$
5\cdot 1=5.
$$

 This matrix does not belong to $D.$ So, $D$ is *not* closed under scalar multiplication.

- Statement “$D$ is a subspace of ${\text{M}}_{2}(R)$” is false, while statement “$D$ is **not** a subspace of ${\text{M}}_{2}(R)$” is true. $D$ is a *not* subspace because it's not closed under addition and scalar multiplication.

Therefore, the correct answer is “$D$ is **not** a subspace of ${\text{M}}_{2}(R)$” only.

Answer $D$ is **not** a subspace of ${\text{M}}_{2}(R)$: true

Answer $D$ is a subspace of ${\text{M}}_{2}(R)$: false

Answer $D$ is closed under matrix addition: false

Answer $D$ is closed under scalar multiplication: false

Question 17592186244021 — question.difficulty/easy

Consider the vector space ${\text{M}}_{2}(R)$ of all $2\times 2$ matrices over $R$ and its subset $C=\left\{\begin{bmatrix}a & 0 \\ 0 & -a\end{bmatrix}\right.\,|\,a\in R\}.$ 

Which of the following statements are true?

Select all that apply.

Solution: Recall that a subset of a vector space is a subspace if it's closed under addition and scalar multiplication.

With that in mind, let's examine each statement in turn.

- Statement “$C$ is closed under matrix addition” is true. If ${A}_{1}=\begin{bmatrix}{a}_{1} & 0 \\ 0 & -{a}_{1}\end{bmatrix}$ and ${A}_{2}=\begin{bmatrix}{a}_{2} & 0 \\ 0 & -{a}_{2}\end{bmatrix}$ are two matrices from $C,$ then

$$
\begin{aligned}{A}_{1}+{A}_{2} & =\begin{bmatrix}{a}_{1} & 0 \\ 0 & -{a}_{1}\end{bmatrix}+\begin{bmatrix}{a}_{2} & 0 \\ 0 & -{a}_{2}\end{bmatrix} \\  & =\begin{bmatrix}{a}_{1}+{a}_{2} & 0 \\ 0 & -({a}_{1}+{a}_{2})\end{bmatrix},\end{aligned}
$$

 
which is a matrix from $C.$ So, $C$ is closed under addition.

- Statement “$C$ is closed under scalar multiplication” is true. If $A=\begin{bmatrix}a & 0 \\ 0 & -a\end{bmatrix}$ is an element of $C$ and $k\in R,$ then 

$$
\begin{aligned}kA & =k\begin{bmatrix}a & 0 \\ 0 & -a\end{bmatrix} \\  & =\begin{bmatrix}ka & 0 \\ 0 & -ka\end{bmatrix},\end{aligned}
$$

which is a matrix from $C.$ So, $C$ is closed under scalar multiplication.

- Statement “$C$ is a subspace of ${\text{M}}_{2}(R)$” is true, while statement “$C$ is **not** a subspace of ${\text{M}}_{2}(R)$” is false. $C$ is a subspace because it's closed under addition and scalar multiplication.

Therefore, the correct answer is “$C$ is closed under matrix addition”; “$C$ is closed under scalar multiplication”; “$C$ is a subspace of ${\text{M}}_{2}(R)$” only.

Answer $C$ is **not** a subspace of ${\text{M}}_{2}(R)$: false

Answer $C$ is a subspace of ${\text{M}}_{2}(R)$: true

Answer $C$ is closed under matrix addition: true

Answer $C$ is closed under scalar multiplication: true

### Identifying Subspaces of Function Vector Spaces (17 captured questions)

Question 17592186125156 — question.difficulty/moderate

Consider the vector space $C[0,1]$ of all continuous functions $f:[0,1]\to R$ and its subset $K$ containing all constant functions.

Which of the following statements are true?

Select all that apply.

*Hint: $f$ is a constant function if $f(x)=\text{const}$ for all $x\in [0,1].$*

Solution: Recall that a subset of a vector space is a subspace if it's closed under addition and scalar multiplication.

With that in mind, let's examine each statement in turn.

- Statement “$K$ is closed under function addition” is true. The sum of two constant functions is a constant function. So, $K$ is closed under addition.

- Statement “$K$ is closed under scalar multiplication” is true. The product of a constant function by a scalar is again a constant function. So, $K$ is closed under scalar multiplication.

- Statement “$K$ is a subspace of $C[0,1]$” is true, while statement “$K$ is **not** a subspace of $C[0,1]$” is false. $K$ is a subspace because it's closed under addition and scalar multiplication.

Therefore, the correct answer is “$K$ is closed under function addition”; “$K$ is closed under scalar multiplication”; “$K$ is a subspace of $C[0,1]$” only.

Answer $K$ is **not** a subspace of $C[0,1]$: false

Answer $K$ is a subspace of $C[0,1]$: true

Answer $K$ is closed under function addition: true

Answer $K$ is closed under scalar multiplication: true

Question 17592186125157 — question.difficulty/hard

Consider the vector space $C[0,1]$ of all continuous functions $f:[0,1]\to R$ and its subset $D=\{f\in C[0,1]\,|\,f(0)=3\}.$ 

Which of the following statements are true?

Select all that apply.

Solution: Recall that a subset of a vector space is a subspace if it's closed under addition and scalar multiplication.

With that in mind, let's examine each statement in turn.

- Statement “$D$ is closed under function addition” is false. For example, if $f(x),g(x)\in D,$ then

$$
\begin{aligned}(f+g)(0) & =f(0)+g(0) \\  & =3+3 \\  & =6 \\  & \ne 3\end{aligned}
$$

So, $D$ is *not* closed under addition.

- Statement “$D$ is closed under scalar multiplication” is false. For example, if $f(x)\in D$ and $k=5\in R,$ then 

$$
\begin{aligned}(kf)(0) & =(5f)(0) \\  & =5\cdot 3 \\  & =15 \\  & \ne 3\end{aligned}
$$

So, $D$ is *not* closed under scalar multiplication.

- Statement “$D$ is a subspace of $C[0,1]$” is false, while statement “$D$ is **not** a subspace of $C[0,1]$” is true. $D$ is *not* a subspace because it's not closed under addition and scalar multiplication.

Therefore, the correct answer is “$D$ is **not** a subspace of $C[0,1]$” only.

Answer $D$ is **not** a subspace of $C[0,1]$: true

Answer $D$ is a subspace of $C[0,1]$: false

Answer $D$ is closed under function addition: false

Answer $D$ is closed under scalar multiplication: false

Question 17592186244032 — question.difficulty/moderate

Consider the vector space $C[0,1]$ of all continuous functions $f:[0,1]\to R$ and its subset $N$ containing all functions such that $f(0)=0.$

Which of the following statements are true?

Select all that apply.

Solution: Recall that a subset of a vector space is a subspace if it's closed under addition and scalar multiplication.

With that in mind, let's examine each statement in turn.

- Statement “$N$ is closed under function addition” is true. Indeed, suppose $f(x)$ and $g(x)$ are functions from $N.$ Then $f(x)=g(x)=0$ and 

$$
\begin{aligned}(f+g)(0) & =f(0)+g(0) \\  & =0+0 \\  & =0.\end{aligned}
$$

So, $N$ is closed under function addition.

- Statement “$N$ is closed under scalar multiplication” is true.  Indeed, suppose $f(x)\in N$  and let $\alpha \in R.$ Then we have

$$
\begin{aligned}(\alpha f)(0) & =\alpha \cdot f(0) \\  & =\alpha \cdot 0 \\  & =0.\end{aligned}
$$

So, $N$ is closed under scalar multiplication.

- Statement “$N$ is a subspace of $C[0,1]$” is true, while statement “$N$ is **not** a subspace of $C[0,1]$” is false. $N$ is a subspace because it's closed under addition and scalar multiplication.

Therefore, the correct answer is “$N$ is closed under function addition”; “$N$ is closed under scalar multiplication”; “$N$ is a subspace of $C[0,1]$” only.

Answer $N$ is **not** a subspace of $C[0,1]$: false

Answer $N$ is a subspace of $C[0,1]$: true

Answer $N$ is closed under function addition: true

Answer $N$ is closed under scalar multiplication: true
