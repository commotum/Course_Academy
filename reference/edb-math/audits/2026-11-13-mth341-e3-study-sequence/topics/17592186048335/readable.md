# 17592186048335 Elementary Properties of Set Operations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186199538 — Introduction

Suppose that $U$ is a universal set and $A\subseteq U$. Then, we have the following basic properties:

- The intersection of a set and its complement gives the empty set:
$A\cap \overline{A}= \emptyset$
- The union of a set and its complement gives the universal set:
$A \cup \overline{A} = U$
- The complement of the complement of a set gives the original set:
$\overline{\overline{A}}=A$
- The complement of the universal set is the empty set:
$\overline{U}= \emptyset$
- The complement of the empty set is the universal set:
$\overline{\emptyset}= U$

We'll prove these properties in future lessons. For now, let's get some practice at applying them.



### example 17592186198134 — Identifying Elementary Properties of Union, Intersection, and Complement

Given that $R$ is a subset of a universal set $U$, simplify the following expression:
$\overline{R} \cap R$

The intersection of a set and its complement gives the empty set.

Therefore,

$$
\overline{R} \cap R = \emptyset
$$

### tutorial 17592186199589 — Unions and Intersections With the Universal and Empty Sets

Given that $U$ is a universal set and $A \subseteq U$, we have the following additional properties:

- The intersection of $A$ with the empty set equals the empty set:
$A\cap \emptyset = \emptyset$
- The union of $A$ with the empty set equals $A{:}$
$A \cup \emptyset = A$
- The union of $A$ with the universal set equals the universal set.
$A\cup U = U$
- The intersection of $A$ with the universal set equals $A{:}$
$A \cap U = A$



### tutorial 17592186199591 — Idempotent Properties of Union and Intersection

We also have two **idempotent** properties of union and intersection.

- The union of the set with itself gives the original set:
$A \cup A = A$
- The intersection of the set with itself gives the original set:
$A \cap A = A$



### example 17592186198133 — Applying the Properties of Union and Intersection

Simplify the expression $((A \cup A) \cap A) \cup B$.

First, the expression $A \cup A$ simplifies to just $A$. So, the given expression can be simplified to

$$
(A \cap A) \cup B
$$

Then, the expression $A \cap A$ simplifies to just $A$. So, the expression can be further simplified to

$$
A \cup B
$$

Therefore,

$$
((A \cup A) \cap A) \cup B = A \cup B
$$

### tutorial 17592186199590 — Associative and Commutative Properties of Union and Intersection

Let $A$, $B$, and $C$ be subsets of a universal set $U$.

- The **associative** properties of union and intersection state the following:
$$
\begin{aligned}(A\cup B)\cup C & =A\cup (B\cup C) \\ (A\cap B)\cap C & =A\cap (B\cap C)\end{aligned}
$$
- The **commutative** properties of union and intersection state the following:
$$
\begin{aligned}A\cup B & =B\cup A \\ A\cap B & =B\cap A\end{aligned}
$$



### example 17592186198132 — Applying the Associative and Commutative Properties of Union and Intersection

Simplify the expression $A \cap (\overline{B} \cap A)$.

Using the commutative, associative, and idempotent properties of intersection, we get

$$
\begin{aligned}
A∩(B^(―)∩A) &= A∩(A∩B^(―)) \\
&= (A∩A)∩B^(―) \\
&= A∩B^(―)
\end{aligned}
$$

## Representative practice (first three per skill; full bank in practice.json)

### Identifying Elementary Properties of Union, Intersection, and Complement (2 captured questions)

Question 17592186198754 — None

Given that $A$ and $B$ are subsets of a universal set $U$, simplify the following expression:

$(A∩B^(―))∪(A∩B) =$ {{field-1}}

Solution: 

Question 17592186198879 — None

Given that $U$ is a universal set and $A⊆U$, simplify the following expression:

$∅^(―) =$ {{field-1}}

Solution: 

### Applying the Properties of Union and Intersection (2 captured questions)

Question 17592186198751 — None

Simplify the expression $A∪(B∩B)$.

Solution: 

Question 17592186198880 — None

Given that $U$ is a universal set and $A⊆U$, simplify the following expression:

$A∩∅ =$ {{field-1}}

Solution: 

### Applying the Associative and Commutative Properties of Union and Intersection (2 captured questions)

Question 17592186198752 — None

Simplify the expression $(M∪N)∪N$.

Solution: 

Question 17592186198753 — None

Simplify the expression $A∩(B∩A)$.

Solution: 
