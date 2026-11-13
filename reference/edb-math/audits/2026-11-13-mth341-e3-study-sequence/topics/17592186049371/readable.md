# 17592186049371 The Invertible Matrix Theorem in Terms of Linear Transformations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186125784 — Introduction

A linear transformation $\mathbf{T}:\mathbb{R}^n \to \mathbb{R}^n$ is **invertible** if there is another linear transformation $\mathbf T^{-1}$ such that 

$$
\mathbf{T}^{-1}(\mathbf{T}(\mathbf{v}))=\mathbf{T}(\mathbf{T}^{-1}(\mathbf{v}))=\mathbf{v}
$$

for every vector $\mathbf{v}\in \mathbb R^n.$ The transformation $\mathbf T^{-1}$ is called the **inverse** of $\mathbf T.$ An invertible linear transformation is also called a **bijection**. 

We have the following theorem regarding invertible linear transformations: 

*If $T$ is the standard matrix of $\mathbf T$, then $\mathbf T$ is invertible if and only if $T$ is invertible*.

Recall that the invertible matrix theorem in terms of dimension, rank, and nullity states that if $T$ is an $n\times n$ matrix, then 

$T$ is invertible $\qquad \Longleftrightarrow \qquad$
$$
\left\{\;
{\begin{array}{rl}\displaystyle  & \displaystyle \text{Col} ( T ) = {\mathbb{R}}^{n} \\ \displaystyle  & \displaystyle \text{dim(Col} ( T ) ) = n = \text{rank} ( T ) \\ \displaystyle  & \displaystyle \text{Null} ( T ) = \{  \mathbf{0} \}  \\ \displaystyle  & \displaystyle \text{dim(Null} ( T ) ) = 0 = \text{nullity} ( T ) .\end{array}} \right.
$$

In the theorem above, we can make the following swaps, where $\mathbf T$ is a linear transformation with the standard matrix $T{:}$
$$
\begin{array}{rl}\displaystyle \text{Col} ( T ) & \displaystyle  = \text{Im} ( \mathbf{T} ) \\ \displaystyle \text{rank} ( T ) & \displaystyle  = \text{rank} ( \mathbf{T} ) \\ \displaystyle \text{Null} ( T ) & \displaystyle  = \text{Ker} ( \mathbf{T} ) \\ \displaystyle \text{nullity} ( T ) & \displaystyle  = \text{nullity} ( \mathbf{T} )\end{array}
$$

As a result, we obtain the **invertible matrix theorem in terms of linear transformations:**

 $\mathbf T$ is a bijection (invertible) $$
\displaystyle \qquad \Longleftrightarrow \qquad
\left\{\;
{\begin{array}{rl}\displaystyle  & \displaystyle \text{Im} ( \mathbf{T} ) = {\mathbb{R}}^{n} \\ \displaystyle  & \displaystyle \text{rank} ( \mathbf{T} ) = n \\ \displaystyle  & \displaystyle \text{Ker} ( \mathbf{T} ) = \{  \mathbf{0} \}  \\ \displaystyle  & \displaystyle \text{nullity} ( \mathbf{T} ) = 0\end{array}} \right.
$$ 
$\qquad \Longleftrightarrow \qquad$  $T$ is invertible



### example 17592186124436 — Recognizing Parts of the Invertible Matrix Theorem

$\mathbf{T}$ is a bijection $$
\displaystyle \qquad \Longleftrightarrow \qquad
\left\{\;
{\begin{array}{rl}\displaystyle  & \displaystyle \bbox[3pt,white,border:2px solid Silver]{\phantom{W W}} = {\mathbb{R}}^{n} \\ \displaystyle  & \displaystyle \text{rank} ( \mathbf{T} ) = n \\ \displaystyle  & \displaystyle \text{Ker} ( \mathbf{T} ) = \{  \mathbf{0} \}  \\ \displaystyle  & \displaystyle \text{nullity} ( \mathbf{T} ) = 0\end{array}} \right.
$$ 
$\qquad \Longleftrightarrow \qquad$  $T$ is invertible

Consider the equivalence above, where $\mathbf{T}:\mathbb{R}^n \to \mathbb{R}^n$ is a linear transformation whose standard matrix is $T.$ What should be placed into the blank space to make a true statement?

Recall that the *invertible matrix theorem* (in terms of linear transformations) states the following: 

 $\mathbf{T}$ is a bijection $$
\displaystyle \qquad \Longleftrightarrow \qquad
\left\{\;
{\begin{array}{rl}\displaystyle  & \displaystyle \bbox[3pt,white,border:2px solid Silver]{ {\color{blue}\text{Im} ( \mathbf{T} )}} = {\mathbb{R}}^{n} \\ \displaystyle  & \displaystyle \text{rank} ( \mathbf{T} ) = n \\ \displaystyle  & \displaystyle \text{Ker} ( \mathbf{T} ) = \{  \mathbf{0} \}  \\ \displaystyle  & \displaystyle \text{nullity} ( \mathbf{T} ) = 0\end{array}} \right.
$$ 
$\qquad \Longleftrightarrow \qquad$  $T$ is invertible

Therefore, the missing expression is $\textrm{Im}(\mathbf{T}).$

### example 17592186124330 — Identifying True Statements Using the Invertible Matrix Theorem

Which of the following statements are true given that $\mathbf{T}:\mathbb{R}^3 \to \mathbb{R}^3$ is a linear transformation whose standard matrix is $T,$ and $T$ is invertible? 

I. $\textrm{Ker}(\mathbf{T}) \neq \{\mathbf{0}\}$

II. $\textrm{nullity}(\mathbf{T})=0$

III. $\textrm{rank}(\mathbf{T}) = 3$

Since $\mathbf{T}$ is a linear transformation from $\mathbb{R}^3$ into $\mathbb{R}^3,$ the invertible matrix theorem states the following:

 $\mathbf{T}$ is a bijection (an invertible transformation) $$
\displaystyle \qquad \Longleftrightarrow \qquad
\left\{\;
{\begin{array}{rl}\displaystyle  & \displaystyle \text{Im} ( \mathbf{T} ) = {\mathbb{R}}^{3} \\ \displaystyle  & \displaystyle \text{rank} ( \mathbf{T} ) = 3 \\ \displaystyle  & \displaystyle \text{Ker} ( \mathbf{T} ) = \{  \mathbf{0} \}  \\ \displaystyle  & \displaystyle \text{nullity} ( \mathbf{T} ) = 0\end{array}} \right.
$$ 

With that in mind, let's examine each statement in turn.

- Statement I is false. Since $T$ is invertible, the invertible matrix theorem implies that $\textrm{Ker}(\mathbf{T}) = \{\mathbf{0}\}.$

- Statement II is true. Since $T$ is invertible, the invertible matrix theorem implies that $\textrm{nullity}(\mathbf{T}) = 0.$

- Statement III is true. Since $T$ is invertible, the invertible matrix theorem implies that $\textrm{rank}(\mathbf{T}) = 3.$

Therefore, the correct answer is "II and III only."

### example 17592186124435 — Сompleting a Sentence Using the Invertible Matrix Theorem

Let $\mathbf{T}:\mathbb{R}^3\rightarrow \mathbb{R}^3$ be a linear transformation whose standard matrix is $T.$ Consider the following statement:

*If $[1, 2, 1]^T \not\in  \textrm{Im}(\mathbf{T}),$ then $\underline{\phantom{xxxxxx}}.$*

Which of the following can be placed into the blank space to make a true statement?

I. $\textrm{Im}(\mathbf{T})=\mathbb{R}^3$

II. $\textrm{Ker}(\mathbf{T})\ne\{\mathbf{0}\}$

III. $\mathbf{T}$ is invertible

Since $\mathbf{T}$ is a linear transformation from $\mathbb{R}^3$ into $\mathbb{R}^3,$ the invertible matrix theorem states the following:

 $\mathbf{T}$ is a bijection (an invertible transformation) $$
\displaystyle \qquad \Longleftrightarrow \qquad
\left\{\;
{\begin{array}{rl}\displaystyle  & \displaystyle \text{Im} ( \mathbf{T} ) = {\mathbb{R}}^{3} \\ \displaystyle  & \displaystyle \text{rank} ( \mathbf{T} ) = 3 \\ \displaystyle  & \displaystyle \text{Ker} ( \mathbf{T} ) = \{  \mathbf{0} \}  \\ \displaystyle  & \displaystyle \text{nullity} ( \mathbf{T} ) = 0\end{array}} \right.
$$ 

With that in mind, let's examine each statement in turn.

- Statement I is false. Since $[1, 2, 1]^T \not\in  \textrm{Im}(\mathbf{T}),$ we must have that $\textrm{Im}(\mathbf{T}) \neq \mathbb{R}^3.$

- Statement II is true. Since the vector $[1, 2, 1]^T$ does not lie in $\textrm{Im}(\mathbf{T})$, then $\textrm{Im}(\mathbf{T}) \neq \mathbb{R}^3.$ Therefore, according to the invertible matrix theorem, we must have $\textrm{Ker}(\mathbf{T}) \neq \{\mathbf{0}\}.$

- Statement III is false. According to the invertible matrix theorem, since $\textrm{Im}(\mathbf{T}) \neq \mathbb{R}^3,$ the transformation $\mathbf T$ can't be invertible.

Therefore, the correct answer is "II only."

## Representative practice (first three per skill; full bank in practice.json)

### Recognizing Parts of the Invertible Matrix Theorem (11 captured questions)

Question 17592186124790 — None

> $T$ is a bijection $$
\displaystyle \hspace{2em} \Longleftrightarrow  \hspace{2em} \left\{  \hspace{0.278em} \begin{array}{rl}\displaystyle  & \displaystyle \text{Im} ( \mathbf{T} ) = {\mathbb{R}}^{n} \\ \displaystyle  & \displaystyle \text{rank} ( \mathbf{T} ) = n \\ \displaystyle  & \displaystyle \text{Ker} ( \mathbf{T} ) = \bbox[3pt,white,border:2px solid Gainsboro]{\phantom{W}} \\ \displaystyle  & \displaystyle \text{nullity} ( \mathbf{T} ) = 0\end{array}\right.
$$
> $⟺$ $T$ is invertible

Consider the equivalence above, where $T: R^{n} → R^{n}$ is a linear transformation whose standard matrix is $T$. Which of the following should be placed into the blank space to make a true statement?

Solution: 

Question 17592186124792 — question.difficulty/easy

$T$ is a ? $\,⟺\,{\,\begin{aligned} & \text{Im}(T)={R}^{n} \\  & \text{rank}(T)=n \\  & \text{Ker}(T)={0} \\  & \text{nullity}(T)=0\end{aligned}}$ 
$\,⟺\,$  $T$ is invertible

Consider the equivalence above, where $T:{R}^{n}\to {R}^{n}$ is a linear transformation whose standard matrix is $T.$ Which of the following should be placed into the blank space to make a true statement?

Solution: Recall that the *invertible matrix theorem* (in terms of linear transformations) states the following: 

 $T$ is a $\text{bijection}$ $\,⟺\,{\,\begin{aligned} & \text{Im}(T)={R}^{n} \\  & \text{rank}(T)=n \\  & \text{Ker}(T)={0} \\  & \text{nullity}(T)=0\end{aligned}$ 
$\,⟺\,$  $T$ is invertible

Therefore, the missing expression is "bijection".

Answer selection: bijection

Question 17592186272282 — question.difficulty/easy

$T$ is a bijection $\,⟺\,{\,\begin{aligned} & \text{Im}(T)= \\  & \text{rank}(T)=n \\  & \text{Ker}(T)={0} \\  & \text{nullity}(T)=0\end{aligned}$ 
$\,⟺\,$  $T$ is invertible

Consider the equivalence above, where $T:{R}^{n}\to {R}^{n}$ is a linear transformation whose standard matrix is $T.$ Which of the following should be placed into the blank space to make a true statement?

Solution: Recall that the *invertible matrix theorem* (in terms of linear transformations) states the following: 

 $T$ is a bijection $\,⟺\,{\,\begin{aligned} & \text{Im}(T)={R}^{n} \\  & \text{rank}(T)=n \\  & \text{Ker}(T)={0} \\  & \text{nullity}(T)=0\end{aligned}$ 
$\,⟺\,$  $T$ is invertible

Therefore, the missing expression is ${R}^{n}.$

Answer selection: {R}^{n}

### Identifying True Statements Using the Invertible Matrix Theorem (11 captured questions)

Question 17592186124793 — None

Which of the following statements are true given that $T: R^{5} → R^{5}$ is a linear transformation whose standard matrix is $T$, and $T(v_{1}) = T(v_{2})$ is true if and only if $v_{1} = v_{2}$?

1. $Ker(T) = {0}$
2. $T$ is invertible
3. $\Im (T) = R^{5}$

Solution: 

Question 17592186125118 — question.difficulty/moderate

Which of the following statements are true given that $T:{R}^{8}\to {R}^{8}$ is a linear transformation whose standard matrix is $T,$ and $T({v}_{1})=T({v}_{2})$ for some distinct vectors  ${v}_{1}$ and ${v}_{2}?$ 

Select all that apply.

Solution: Since $T$ is a linear transformation from ${R}^{8}$ into ${R}^{8},$ the invertible matrix theorem states the following:

 $T$ is a bijection (an invertible transformation) $$
\displaystyle \,⟺\,\left\{\,\begin{aligned} & \text{Im}(T)={R}^{8} \\  & \text{rank}(T)=8 \\  & \text{Ker}(T)=\{0\} \\  & \text{nullity}(T)=0\end{aligned}\right.
$$ 

Since $T$ is a linear transformation, we have that

$$
T({v}_{1})=T({v}_{2})\,⟹\,T({v}_{1}-{v}_{2})=0.
$$

With that in mind, let's examine each statement in turn.

- Statement $\text{Ker}(T)=\{0\}$ is false. Since ${v}_{1}-{v}_{2}\in \text{Ker}(T)$ and ${v}_{1}\ne {v}_{2},$ we must have that $\text{Ker}(T)\ne \{0\}.$

- Statement “$T$ is invertible” is false. According to the invertible matrix theorem, since $\text{Ker}(T)\ne \{0\},$ the transformation $T$ and the matrix $T$ are not invertible.

- Statement $\text{rank}(T)<8$ is true. Since $T$ is not invertible, the invertible matrix theorem implies that $\text{rank}(T)\ne 8.$ In turn, this means that $\text{rank}(T)<8.$

Therefore, the correct answer is $\text{rank}(T)<8$ only.

Answer $T$ is invertible: false

Answer $\text{Ker}(T)=\{0\}$: false

Answer $\text{rank}(T)<8$: true

Answer None of the above: false

Question 17592186272020 — question.difficulty/moderate

Which of the following statements are true given that $T:{R}^{7}\to {R}^{7}$ is a linear transformation whose standard matrix is $T,$ and $T({v}_{1})=T({v}_{2})$ for some distinct vectors  ${v}_{1}$ and ${v}_{2}?$

Select all that apply.

Solution: Since $T$ is a linear transformation from ${R}^{7}$ into ${R}^{7},$ the invertible matrix theorem states the following:

 $T$ is a bijection (an invertible transformation) $$
\displaystyle \,⟺\,\left\{\,\begin{aligned} & \text{Im}(T)={R}^{7} \\  & \text{rank}(T)=7 \\  & \text{Ker}(T)={0} \\  & \text{nullity}(T)=0\end{aligned}\right.
$$ 

Since $T$ is a linear transformation, we have that

$$
T({v}_{1})=T({v}_{2})\,⟹\,T({v}_{1}-{v}_{2})=0.
$$

With that in mind, let's examine each statement in turn.

- Statement $\text{Ker}(T)\ne {0}$ is true. Indeed, since ${v}_{1}-{v}_{2}\in \text{Ker}(T)$ and ${v}_{1}\ne {v}_{2},$ we must have that $\text{Ker}(T)\ne {0}.$

- Statement “$T$ is invertible” is false. According to the invertible matrix theorem, since $\text{Ker}(T)\ne {0},$ the transformation $T$ and the matrix $T$ are not invertible.

- Statement $\text{rank}(T)=7$ is false. Since $T$ is not invertible, the invertible matrix theorem implies that $\text{rank}(T)\ne 7.$

Therefore, the correct answer is $\text{Ker}(T)\ne {0}$ only.

Answer $T$ is invertible: false

Answer $\text{Ker}(T)\ne {0}$: true

Answer $\text{rank}(T)=7$: false

### Сompleting a Sentence Using the Invertible Matrix Theorem (12 captured questions)

Question 17592186125144 — question.difficulty/hard

Let $T:{R}^{4}\to {R}^{4}$ be a linear transformation whose standard matrix is $T.$ Consider the following statement:

*If $T$ is invertible, then $\underline{\phantom{xxxxxx}}.$*

Which of the following can be placed into the blank space to make a true statement?

Select all that apply.

Solution: Since $T$ is a linear transformation from ${R}^{4}$ into ${R}^{4},$ the invertible matrix theorem states the following:

 $T$ is a bijection (an invertible transformation) $$
\displaystyle \,⟺\,\left\{\,\begin{aligned} & \text{Im}(T)={R}^{4} \\  & \text{rank}(T)=4 \\  & \text{Ker}(T)={0} \\  & \text{nullity}(T)=0\end{aligned}\right.
$$ 

With that in mind, let's examine each statement in turn.

- Statement $\text{Ker}(T)={0}$ is true. Since $T$ is invertible, the invertible matrix theorem implies that $\text{Ker}(T)={0}.$

- Statement $\text{rank}(T)\ne 4$ is false. Since $T$ is invertible, the invertible matrix theorem implies that $\text{rank}(T)=4.$

- Statement $\text{nullity}(T)\ne 0$ is false. Since $T$ is invertible, the invertible matrix theorem implies that $\text{nullity}(T)=0.$

Therefore, the correct answer is $\text{Ker}(T)={0}$ only.

Answer $\text{Ker}(T)={0}$: true

Answer $\text{nullity}(T)\ne 0$: false

Answer $\text{rank}(T)\ne 4$: false

Question 17592186125164 — question.difficulty/hard

Let $T:{R}^{2}\to {R}^{2}$ be a linear transformation whose standard matrix is $T.$ Consider the following statement:

*If $[1,-1]^{T}\notin \text{Im}(T)$, then $\underline{\phantom{xxxxxx}}.$*

Which of the following can be placed into the blank space to make a true statement?

Select all that apply.

Solution: Since $T$ is a linear transformation from ${R}^{2}$ into ${R}^{2},$ the invertible matrix theorem states the following:

 $T$ is a bijection (an invertible transformation) $$
\displaystyle \,⟺\,\left\{\,\begin{aligned} & \text{Im}(T)={R}^{2} \\  & \text{rank}(T)=2 \\  & \text{Ker}(T)=\{0\} \\  & \text{nullity}(T)=0\end{aligned}\right.
$$ 

With that in mind, let's examine each statement in turn.

- Statement $\text{Ker}(T)=\{0\}$ is false. Since the vector $\begin{bmatrix}1 \\ -1\end{bmatrix}$ does not lie in $\text{Im}(T)$, then $\text{Im}(T)\ne {R}^{2}.$ Therefore, according to the invertible matrix theorem, we must have $\text{Ker}(T)\ne \{0\}.$

- Statement $\text{rank}(T)\ne 2$ is true. Since $\text{Im}(T)\ne {R}^{2}$, then $\text{rank}(T)=\text{rank}(T)\ne 2.$

- Statement “$T$ is invertible” is false. According to the invertible matrix theorem, since $\text{Im}(T)\ne {R}^{2},$ the transformation $T$ can't be invertible.

Therefore, the correct answer is $\text{rank}(T)\ne 2$ only.

Answer $T$ is invertible: false

Answer $\text{Ker}(T)=\{0\}$: false

Answer $\text{rank}(T)\ne 2$: true

Question 17592186272021 — question.difficulty/hard

Let $T:{R}^{5}\to {R}^{5}$ be a linear transformation whose standard matrix is $T.$ Consider the following statement:

*If $\text{rank}(T)=5,$ then $\underline{\phantom{xxxxxx}}.$*

Which of the following can be placed into the blank space to make a true statement?

Select all that apply.

Solution: Since $T$ is a linear transformation from ${R}^{5}$ into ${R}^{5},$ the invertible matrix theorem states the following:

 $T$ is a bijection (an invertible transformation) $$
\displaystyle \,⟺\,\left\{\,\begin{aligned} & \text{Im}(T)={R}^{5} \\  & \text{rank}(T)=5 \\  & \text{Ker}(T)=\{0\} \\  & \text{nullity}(T)=0\end{aligned}\right.
$$ 

With that in mind, let's examine each statement in turn.

- Statement $\text{Ker}(T)\ne \{0\}$ is false. Since $\text{rank}(T)=5,$ the invertible matrix theorem implies that $\text{Ker}(T)=\{0\}.$

- Statement “$T$ is invertible” is true. Indeed, since $\text{rank}(T)=5,$ the invertible matrix theorem implies that $T$ is invertible.

- Statement $\text{nullity}(T)=0$ is true. Indeed, since $T$ is invertible, the invertible matrix theorem implies that $\text{nullity}(T)=0.$

Therefore, the correct answer is “$T$ is invertible”; $\text{nullity}(T)=0$ only.

Answer $T$ is invertible: true

Answer $\text{Ker}(T)\ne \{0\}$: false

Answer $\text{nullity}(T)=0$: true
