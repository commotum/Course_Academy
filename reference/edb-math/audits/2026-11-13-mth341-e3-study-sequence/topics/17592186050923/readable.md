# 17592186050923 Subsets

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186056044 — Introduction

Given two sets $A$ and $B,$ if every element of $A$ is an element of $B,$ we say that $A$ is a **subset** of $B,$ and we write 

$$
A \subseteq B.
$$

For example, consider the following sets:

$$
A = \{ {\color{blue}{1}},{\color{blue}{3}} \}, \qquad B = \{ 1,2,3\}, \qquad C=\{1,2,{\color{red}4}\}
$$

 

Notice that *every* element of $A$ is also an element of $B{:}$

$$
{\color{blue}{1}}\in B, \qquad {\color{blue}{3}}\in B
$$

Therefore, $A$ is a subset of $B,$ and we write $A \subseteq B.$

We can visualize the sets $A$ and $B$ as shown below. Notice that $A$ is contained entirely within $B$ (here, $U$ is the universal set).

![](images/91/911dbbe9a638810f3a245fdcd004e10aee4dbd49fd8a99741c1bdd5c48cc2319.png)

On the other hand, not every element of $C$ is an element of $B{:}$ 

$$
1 \in B, \qquad 2\in B, \qquad {\color{red}4}\notin B
$$

Since $4 \notin B,$ we have that $C$ is *not* a subset of $B,$ and we write $C \not\subseteq B.$

We can visualize the sets $B$ and $C$ as follows. Notice that $C$ is *not* contained entirely within $B$ (here, $U$ is the universal set).

![](images/45/454c28bacb8d5117bb11f76988b70344b4521d260adf2b690a11e7dfd2964385.png)

Another way of thinking about the statement $C \not\subseteq B$ is that $C$ contains *at least one* element that is not an element of $B.$ In this case, that element is $4.$



### tutorial 17592186056055 — Some Remarks

We note the following points regarding subsets:

- Every set $A$ is a subset of itself:

$$
A\subseteq A
$$

This is because $A$ contains the same elements as $A,$ and therefore $A$ is a subset of $A.$

- The empty set is a subset of *every* set. So, for all sets $A,$ we have

$$
\emptyset \subseteq A.
$$

To understand this, remember that $\emptyset \not\subseteq A$ means that $\emptyset$ contains *at least one* element that is not an element of $A.$ However, this cannot be true since $\emptyset$ contains no elements! Thus, we must have $\emptyset\subseteq A.$

It's worth pointing out that the empty set is a subset of itself:

$$
\emptyset \subseteq \emptyset
$$

Finally, note that a set $A$ is a **proper subset** of a set $B$ if $A \subseteq B$ and $A \neq B.$ In this case, we can write 

$$
A \subset B.
$$

To explain this concretely, consider the following sets:

$$
A = \{ 1,3 \}, \qquad B = \{ 1, 2, 3 \}, \qquad C = \{ 3,2,1 \}
$$

Notice that $A$ is a proper subset of $B,$ but $C$ is *not* a proper subset of $B{:}$

- Since every element of $A$ is an element of $B,$ we have that $A\subseteq B.$ Also, $A\neq B.$ Therefore, $A$ is a *proper* subset of $B{:}$

$$
A\subset B
$$

- On the other hand, $C\subseteq B$ because every element of $C$ is an element of $B.$ However, $C$ is *not* a proper subset of $B$ because $C=B.$ Therefore, we write 

$$
C \not\subset B.
$$



### example 17592186054442 — Identifying Subsets of a Given Set

Which of the following sets is a subset of $S=\{n \in \mathbb{Z}: {-3} \leq 2n+1 \leq 7 \}?$

I. $\{ -2, 0, 4 \}$

II. $\{ 0, 3 \}$

III. $\{ -3, 1, 3 \}$

First, we must find the elements of the set $S.$ Solving the given inequality, we have

$$
\begin{aligned}-3\le 2n+1 & \le 7 \\ -4\le 2n & \le 6 \\ -2\le n & \le 3.\end{aligned}
$$

So, $S$ contains all integers between $-2$ and $3$ (including $-2$ and $3$):

$$
S = \{ -2, -1, 0, 1, 2, 3 \}
$$

A set is a subset of $S$ if all its elements are elements of $S.$ With that in mind, let's inspect each option.

- $\{ -2,0,4 \}$ is *not* a subset of $S$ because it contains the element $4 \notin S. \quad \color{red}\times$

- $\{ 0,3 \}$ is a subset of $S. \quad \color{green}\checkmark$

- $\{ -3,1,3 \}$ is *not* a subset of $S$ because it contains the element $-3 \notin S. \quad \color{red}\times$

Therefore, the correct answer is "II only".

### tutorial 17592186056047 — Listing All the Subsets of a Set

We can systematically list all the subsets of a given set using a tree diagram.

To demonstrate, let's find all the subsets of the set $A=\{ 0,1 \}.$

We list every possible combination of elements within the set using a tree diagram like the one below.

![](images/dd/dd51f5e02c9f280b8478e11497602dd7ae886b84d1d5994d8af73dff9719d20e.png)

We start with the empty set as the root $\bbox[2pt,Gainsboro]{\{ \}}.$ 

Next, we consider the element $0\in A.$ We can either include it or not include it in a new subset.

- If we don't include $0$ in $\bbox[2pt,Gainsboro]{\{ \}},$ we are left with the empty set $\bbox[2pt,LightBlue]{\{\}}.$ Next, we consider the element $1\in A.$ We can either include it or not include it in a new subset:

- If we don't include $1$ in $\bbox[2pt,LightBlue]{\{\}},$ we are left with $\bbox[2pt,Thistle]{\{\}}.$

- If we include $1$ in $\bbox[2pt,LightBlue]{\{\}},$ we get $\bbox[2pt,Thistle]{\{1\}}.$

- If we include $0$ in $\bbox[2pt,Gainsboro]{\{ \}},$ we get the set $\bbox[2pt,LightBlue]{\{0\}}.$ Next, we consider the element $1\in A.$ We can either include it or not include it in a new subset:

- If we don't include $1$ in $\bbox[2pt,LightBlue]{\{0\}},$ we are left with $\bbox[2pt,Thistle]{\{0\}}.$

- If we include $1$ in $\bbox[2pt,LightBlue]{\{0\}},$ we get $\bbox[2pt,Thistle]{\{0,1\}}.$

Finally, the list of all subsets is shown in the last column:

$$
\bbox[2pt,Thistle]{\{\}},\quad \: \bbox[2pt,Thistle]{\{0\}},\quad \: \bbox[2pt,Thistle]{\{1\}},\quad \: \bbox[2pt,Thistle]{\{0,1\}}
$$



### example 17592186054443 — Finding All Subsets of a Given Set

Find all of the subsets of $A = \{ a, b, c \}.$

To find every subset of $A,$ we list out every combination of elements within $A.$ 

We can use the following diagram to visualize the process:

![](images/83/8323a4292a4f06d66d456bfce1906cbc7e9933a3fac41dd5fb643e13d25f6a6e.png)

Note that we must include the empty set since it is a subset of every set.

By doing this, we get

$$
\emptyset, \{a\}, \{b\}, \{c\}, \{a, b\}, \{a, c\}, \{b, c\}, \{a, b, c\}.
$$

### tutorial 17592186056056 — Subsets of Special Sets

Recall that the natural numbers, integers, rational numbers, and real and complex numbers can be arranged in the following hierarchical diagram.

![](images/66/66260e4c239137cd30453d9335256fd7d84e93a197612d670c19d97e417bd2f0.png)

In other words, $\mathbb{N}$ is a (proper) subset of $\mathbb{Z},$ which is a (proper) subset of $\mathbb{Q},$ which is a (proper) subset of $\mathbb{R},$ which is a (proper) subset of $\mathbb{C}.$ We can write this symbolically as follows:

$$
\mathbb{N} \subseteq \mathbb{Z} \subseteq \mathbb{Q} \subseteq \mathbb{R} \subseteq \mathbb{C}
$$

Since none of these sets are equivalent, we can also write

$$
\mathbb{N} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R} \subset \mathbb{C}.
$$

Some restricted or extended special sets are subsets of others. For example:

- $\mathbb N$ is the set of natural numbers, and $\mathbb N_0$ is the set of natural numbers *and* zero. Therefore, 

$$
\mathbb N\subset \mathbb N_0.
$$

- $\mathbb Z$ is the set of integers, $\mathbb Z^+$ is the set of positive integers (equivalent to $\mathbb N$), and $\mathbb Z^+_0$ is the set of positive integers and zero (equivalent to $\mathbb N_0$). Therefore,

$$
\mathbb Z^+\subset  \mathbb Z_0^+ \subset \mathbb Z.
$$

- $\mathbb Q^+$ is the set of positive rational numbers, $\mathbb R^+$ is the set of positive real numbers, and $\mathbb R$ is the set of real numbers. Therefore,

$$
\mathbb Q^+\subset  \mathbb R^+ \subset \mathbb R.
$$

However, note that, for example, $\mathbb Q \not\subset  \mathbb R^+,$ since $0\in\mathbb Q$ yet $0\notin \mathbb R^+.$



### example 17592186054444 — Identifying Subsets of Special Sets

Which of the following are subsets of $\mathbb{Z}_0^+$ (the set of non-negative integers)?

I. $\mathbb{Z}$

II. $\mathbb{Z}^-$ (the set of negative integers)

III. $\mathbb{N}$

$A$ is a subset of $B$ if every element of $A$ is an element of $B.$

With that in mind, let's inspect the given choices.

- $\mathbb{Z}$ is *not* a subset of $\mathbb{Z}_0^+.$ For example, $-1 \in \mathbb{Z}$ but $-1 \notin \mathbb{Z}_0^+.$

- $\mathbb{Z}^-$ is *not* a subset of $\mathbb{Z}_0^+.$ For example, $-1 \in \mathbb{Z}^-$ but $-1 \notin \mathbb{Z}_0^+.$

- $\mathbb{N}$ is a subset of $\mathbb{Z}_0^+.$ Every natural number is a positive integer.

Therefore, the correct answer is "III only."

### tutorial 17592186056073 — Superset Notation

The notation 

$$
A \supseteq B
$$

reads "$A$ is a **superset** of $B$", and is equivalent to $B \subseteq A.$ This is similar to how we can write either $x \leq y$ or $y \geq x$. The two notations mean the same thing. 

Similarly, $A \supset B$ reads "$A$ is a **proper superset** of $B$," and is equivalent to $B \subset A.$



### example 17592186054445 — Identifying True Statements About Subsets

Which of the following statements are true for the sets $A =\{ n \in \mathbb{N} \mid 2n \geq 10 \}$ and $B= \{ n\in \mathbb{Z} \mid n+2 \geq 5 \}?$

I. $A\subseteq B$

II. $B\subseteq A$

III. $B\nsubseteq A$

IV. $B\supseteq A$

First, we must find the elements of the sets $A$ and $B.$

- The elements of the set $A$ are all the natural numbers that satisfy the inequality $2n\geq 10,$ that is, $n\geq 5.$ So, we have

$$
A= \{5,6,7,8,9,\ldots \}.
$$

- On the other hand, the elements of the set $B$ are all integers that satisfy the inequality $n+2\geq 5,$ that is, $n\geq 3.$ So, we have

$$
B= \{3,4,5,6,7,\ldots\}.
$$

Now, let's inspect the given statements.

- $A\subseteq B$ is true. Every element of $A$ is an element of the set $B.$

- $B\subseteq A$ is false, while $B\nsubseteq A$ is true. For example, $3 \in B$ but $3 \notin A.$

- $B\supseteq A$ is equivalent to $A \subseteq B,$ which is true.

Therefore, the correct answer is "I, III, and IV only".

### tutorial 17592186056075 — Russell's Paradox: Why We Need a Universal Set

You might wonder why we need to define a universal set. Can't we just let the universal set be the set of everything?

The answer is no. If we don't specify a well-defined universal set, we encounter a nonsensical situation called **Russell's paradox.**

First, suppose there exists a set $\Omega$ that contains absolutely everything, including every mathematical object, every thought, every book, every person, animal, cell, and star in the universe, past, present, or future. 

Russell's paradox originates from the following idea:

*Define $S$ as the set that contains all sets that are not elements of themselves.* 

$$
S = \{A\in \Omega\,:\, A\notin A\}
$$

Most sets you can think of are elements of $S.$ For example, the set $\{ 1,2,3 \}$ is in $S$ because $\{ 1,2,3 \}\notin \{ 1,2,3 \}.$ 

It takes a bit of thought to find sets that *aren't* members of $S.$ Such sets do exist, although typical examples are somewhat abstract: 

- The set containing all possible sets.

- The set containing all possible thoughts.

- The set $X,$ given by

$$
X = \Big\{\underbrace{\big\{ \left\{\{\ldots \}\right\}\big\}}_{X}\Big\}.
$$

However, what about $S$ itself? Is $S$ an element of $S?$ There are only two possibilities:

- If $S\in S,$ then by the definition of $S,$ we have that $S\notin S.$ But this is a contradiction because we cannot have $S\in S$ *and* $S\notin S.$

- If $S\notin S,$ then by the definition of $S,$ we must have that $S\in S.$ But this leads to the same contradiction as before!

The only way to resolve this is to conclude that $S\notin \Omega,$ but this is also a contradiction since $\Omega$ contains absolutely everything!  So, there is no consistent answer to the question of whether $S$ itself is an element of $S.$ This is Russell's paradox, and when it was discovered, it shook the foundations of mathematics to its very core.

Later, it was realized that if a set is defined using a predicate, we should ensure that all sets involved are subsets of some larger set $U$ (i.e., a universal set) where we can always determine which elements are members of $U$ and which are not, at least in principle.

To see how this resolves Russell's paradox, suppose $U$ is a universal set. Let's refine our definition of $S$ as follows:

$$
S = \{A\subseteq U\,:\,A\notin A\}
$$

We'll assume $S$ is a set, so $S\subseteq U$ for some well-defined $U.$ Once again, we'll ask the question of whether $S\in S{:}$

- If $S\in S,$ then by the definition of $S,$ we have that $S\notin S.$ But this is a contradiction.

- If $S\notin S,$ then by the definition of $S,$ we have that $S\in S.$ But this is also a contradiction.

Thus, to resolve the paradox, we're left with no choice but to conclude that $S\not\subseteq U.$ This indicates that something is fundamentally wrong with our definition of $S,$ and no such set can exist because if it were a set, it would belong to a universal set.



## Representative practice (first three per skill; full bank in practice.json)

### Identifying Subsets of a Given Set (13 captured questions)

Question 17592186055137 — None

Which set is a subset of $B = {1, 2, 4, 6, 8, 10}$?

Solution: 

Question 17592186055242 — question.difficulty/hard

Which of the following sets is a subset of $A={{1},{2,3},{1,3,6}}?$

Select all that apply.

Solution: A set is a subset of $A$ if all its elements are elements of $A.$ 

With that in mind, let's inspect each option.

- ${2,{1}}$ is *not* a subset of $A$ because it contains the element $2\notin A.\,\times $

- ${{2,3}}$ is a subset of $A.\,✓$

- ${{-1},{1,3,6}}$ is *not* a subset of $A$ because it contains the element ${-1}\notin A.\,\times $

Therefore, the correct answer is ${{2,3}}$ only.

Answer ${2,{1}}$: false

Answer ${{-1},{1,3,6}}$: false

Answer ${{2,3}}$: true

Question 17592186055243 — None

Which of the following sets is a subset of $A = {n^{2}∣n ∈ {1, 2, 3}}$?

Solution: 

### Finding All Subsets of a Given Set (15 captured questions)

Question 17592186054975 — question.difficulty/easy

Find all of the subsets of $S = {p, q}$.

Solution: 

Question 17592186054976 — question.difficulty/moderate

Find all of the subsets of $T={1,2,3}.$

Solution: To find every subset of $T,$ we list out every combination of elements within $T.$ 

We can use the following diagram to visualize the process:

![](images/12/127ee1187ebf3a2cc498c88326285d5adf5d609cf3276885e8c9d525435133eb.png)

Note that we must include the empty set since it is a subset of every set.

By doing this, we get

$$
∅,\,{1},\,{2},\,{3},\,{1,2},\,{1,3},\,{2,3},\,{1,2,3}.
$$

Answer selection: ∅,{1},{2},{3},{1,2},{1,3},{2,3},{1,2,3}

Question 17592186240959 — question.difficulty/easy

Find all of the subsets of $S={r,t}.$

Solution: To find every subset of $S,$ we list out every combination of elements within $S.$

We can use the following diagram to visualize the process:

![](images/02/022399e6a7a5e1f79b58e856aa8e9e5e9f3561e8e4bcb5b80a95237d30d06002.png)

Note that we must include the empty set since it is a subset of every set.

By doing this, we get

$$
∅,{r},{t},{r,t}.
$$

Answer selection: ∅,{r},{t},{r,t}

### Identifying Subsets of Special Sets (16 captured questions)

Question 17592186055142 — None

Which statement is **not** true?

Solution: 

Question 17592186055352 — question.difficulty/moderate

Which of the following are subsets of ${Q}_{0}^{+}$ (the set of non-negative rational numbers)?

I. $Z$

II. ${Z}^{+}$ (the set of positive integers)

III. $N$

Solution: $A$ is a subset of $B$ if every element of $A$ is an element of $B.$

With that in mind, let's inspect the given choices.

- $Z$ is *not* a subset of ${Q}_{0}^{+}.$ For example, $-1\in Z$ but $-1\notin {Q}_{0}^{+}.$

- ${Z}^{+}$ is  a subset of ${Q}_{0}^{+}.$ Every positive integer is a positive rational number.

- $N$ a subset of ${Q}_{0}^{+}.$ Every natural number is a positive rational number.

Therefore, the correct answer is "II and III only".

Answer selection: II and III only

Question 17592186240972 — question.difficulty/moderate

Which of the following are subsets of ${Q}_{0}^{-}$ (the set of non-positive rational numbers)?

Select all that apply.

Solution: $A$ is a subset of $B$ if every element of $A$ is an element of $B.$

With that in mind, let's inspect the given choices.

- $Z$ is *not* a subset of ${Q}_{0}^{-}.$ For example, $1\in Z$ but $1\notin {Q}_{0}^{-}.$

- ${Z}^{-}$ is  a subset of ${Q}_{0}^{-}.$ Every negative integer is a non-positive rational number.

- $N$ is *not* a subset of ${Q}_{0}^{-}.$ For example, $1\in N$ but $1\notin {Q}_{0}^{-}.$

Therefore, the correct answer is “${Z}^{-}$ (the set of negative integers)” only.

Answer $N$ (natural numbers): false

Answer $Z$ (integers): false

Answer ${Z}^{-}$ (the set of negative integers): true

Answer None of the above: false

### Identifying True Statements About Subsets (15 captured questions)

Question 17592186054987 — question.difficulty/easy

Which of the following statements are true for the sets $A={x\in Z:-2\le x<6}$ and $B={x\in N:x+1<6}?$

Select all that apply.

Solution: First, we must find the elements of the sets $A$ and $B.$

- The elements of the set $A$ are all integer numbers greater than or equal to $-2$ but less than $6.$ So,

$$
A={-2,-1,0,1,2,3,4,5}.
$$

- On the other hand, the elements of the set $B$ are natural numbers that satisfy the inequality $x+1<6.$ So,

$$
B={1,2,3,4}.
$$

Now, let's inspect the given statements.

- $∅⊆B$ is true. The null set $∅={}$ is a subset of *every* set.

- $B⊆A$ is true. Every element in the set $B$ is an element of the set $A.$

- $A⊈B$ is true. For example, $-1\in A$ but $-1\notin B.$

Therefore, the correct answer is $∅⊆B$; $B⊆A$; $A⊈B$.

Answer $A⊈B$: true

Answer $B⊆A$: true

Answer $∅⊆B$: true

Question 17592186054988 — None

Which of the following statements are true for the sets $A = {x ∈ Z∣x \le 3}$ and $B = {x ∈ Z∣ - 5 \le x < 0}$?

1. $A⊆B$
2. $B⊆A$
3. $B⊈A$
4. $A⊇B$

Solution: 

Question 17592186240975 — question.difficulty/moderate

Which of the following statements are true for the sets $A={n\in N∣n-2\ge 4}$ and $B={n\in Z∣n+2\ge 5}?$

Select all that apply.

Solution: First, we must find the elements of the sets $A$ and $B.$

- The elements of the set $A$ are all the natural numbers that satisfy the inequality $n-2\ge 4,$ that is to say, $n\ge 6.$ So, we have

$$
A={6,7,8,9,10,11,…}.
$$

- On the other hand, the elements of the set $B$ are all integers that satisfy the inequality $n+2\ge 5,$ That is to say, $n\ge 3.$ So, we have

$$
B={3,4,5,6,7,8,…}.
$$

Now, let's inspect the given statements.

- $A⊆B$ is true. Every element in the set $A$ is an element of the set $B.$

- $B⊆A$ is false. For example, $3\in B$ but $3\notin A.$

- $∅⊆A$ is true. The null set $∅={}$ is a subset of *every* set.

- $B⊇A$ is equivalent to $A⊆B,$ which is true.

Therefore, the correct answer is $A⊆B$; $∅⊆A$; $B⊇A$ only.

Answer $A⊆B$: true

Answer $B⊆A$: false

Answer $B⊇A$: true

Answer $∅⊆A$: true
