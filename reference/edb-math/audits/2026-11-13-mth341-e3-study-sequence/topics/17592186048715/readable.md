# 17592186048715 Proving Elementary Properties of Set Operations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186158572 — Introduction

In this lesson, we'll learn how to prove some elementary results from set theory.

For example, suppose $A$ is a set and $A\subseteq U$, where $U$ is a universal set. Let's prove the following set identity:

$$
A\cap U = A
$$

One way to prove this identity is to show that $A\cap U \subseteq A$ and $A\subseteq A\cap U$. Let's go through this argument.

We start by considering the first inclusion, $A \cap U \subseteq A$.

> *First, we'll prove that $A \cap U \subseteq A$.*

We take a fixed but arbitrary element of $A\cap U$ and apply the definition of intersection:

> *Let $x \in A \cap U$. Then $x \in A$ and $x \in U$.*

Therefore, $x\in A\cap U$ implies $x\in A$, which means that $A\cap U\subseteq A$.

> *Since $x \in A$ for all $x \in A \cap U$, we have $A \cap U \subseteq A$.*

This proves the first inclusion.

Next, we need to show that $A \subseteq A\cap U$. This time, we take an element $x$ in $A$ and apply the definition of the universal set:

> *Next, we prove that $A\subseteq A \cap U$. Let $x \in A$. Since $U$ is the universal set containing $A$, we also have $x \in U$.*

Then, we apply the definition of intersection.

> *So, by the definition of the intersection, $x \in A \cap U$, and we conclude that $A \subseteq A \cap U$.*

This proves the second inclusion.

The proof is completed, and we can write our conclusion.

> *Combining the two inclusions, we obtain that*
> $A \cap U = A$.

Let's now state the full proof.



### tutorial 17592186158600 — Stating the Full Proof

Theorem:

> *Suppose $A$ is a set and $A\subseteq U$, where $U$ is a universal set. Then, $A\cap U = A$.*

Proof:

> *First, we'll prove that $A \cap U \subseteq A$. Let $x \in A \cap U$. Then $x \in A$ and $x \in U$. Since $x \in A$ for all $x \in A \cap U$, we have $A \cap U \subseteq A$. Next, we prove that $A\subseteq A \cap U$. Let $x \in A$. Since $U$ is the universal set containing $A$, we also have $x \in U$. So, by the definition of the intersection, $x \in A \cap U$, and we conclude that $A \subseteq A \cap U$. Combining the two inclusions, we obtain that $A \cap U = A$.*

Notice that we wrote our proof as a single paragraph. You'll often see this format for short proofs, so getting used to reading them in that format is a good idea.



### example 17592186157018 — Proving Statements Using Two Inclusions

Consider the following statement:

> Given that $U$ is a universal set and $A \subseteq U$, we have $A \cup \overline{A} = U$.

A proof that $U \subseteq A \cup \overline{A}$ is given below.

> $\textrm{L1}{:}\:$ Let $x \in U$. So, we have two cases:
> $\textrm{L2}{:}\:$ **Case 1:** $x \in A$. Then $x \in A \cup \overline{A}$.
> $\textrm{L3}{:}\:$ **Case 2:** $x \not\in A$. This implies that $x \in \overline{A}$.
> $\textrm{L4}{:}\:$ Therefore, $x \in A \cup \overline{A}$.
> $\textrm{L5}{:}\:$ In both cases, $x \in A \cup \overline{A}$.
> $\textrm{L6}{:}\:$ Thus, $U \subseteq A \cup \overline{A}$.

Complete the missing entries in the following reasoning.

- Line $\textrm{L2}$ is true due to the properties of the $\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\,$.
- Line $\textrm{L3}$ is true by the the definition of the $\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\,$.
- Line $\textrm{L6}$ follows from $\textrm{L1}$ and $\textrm{L5}$ by the definition of the $\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\,$.

Let's examine each statement in turn. Assume $X$ and $Y$ are subsets of a universal set $U$.

- First, we consider line $\textrm{L2}$. According to the properties of the union of sets, we have the following implication:
$a \in X \quad \Rightarrow \quad a \in X \cup Y$
Therefore, line $\textrm{L2}$ is true due to the properties of the $\bbox[3pt,Gainsboro]{\color{blue}\text{union of sets}}$.
- Next, we consider line $\textrm{L3}$. According to the definition of the set complement, we have the following equivalence:
$a \not\in X \quad \Leftrightarrow \quad a \in \overline{X}$
Therefore, line $\textrm{L3}$ is true by the definition of the $\bbox[3pt,Gainsboro]{\color{blue}\text{set complement}}$.
- Finally, we consider lines $\textrm{L1}$, $\textrm{L5}$, and $\textrm{L6}$. According to the definition of the subset, we have the following equivalence:
$X \subseteq Y \quad\Leftrightarrow\quad \forall a \in U, \: a \in X \Rightarrow a \in Y$
Therefore, $\textrm{L6}$ follows from $\textrm{L1}$ and $\textrm{L5}$ by the definition of the $\bbox[3pt,Gainsboro]{\color{blue}\textrm{subset}}$.

### tutorial 17592186158599 — Proof Using Chains of Biconditional Statements

Another way to prove some set identities is by forming a chain of equivalent statements.

Let's use this concept to prove the commutative law for intersections:

$$
A\cap B = B\cap A
$$

First, we use logical operations to rewrite the predicates $x \in A \cap B$ and $x \in B \cap A$.

> *Given any element $x\in U$ for some universal set $U$, we have the following equivalent statements:*
> $x ∈ A∩B \mid ⇔(x ∈ A)∧(x ∈ B)$
> *and*
> $x ∈ B∩A \mid ⇔(x ∈ B)∧(x ∈ A)$

Now, we use the commutative law for conjunctions.

> *By the commutative law for conjunctions, $(x \in A) \land (x \in B)$ is equivalent to $(x \in B) \land (x \in A)$.*
> *Hence, we have the following chain of equivalent statements:*
> $x ∈ A∩B⇔(x ∈ A)∧(x ∈ B)⇔(x ∈ B)∧(x ∈ A)⇔x ∈ B∩A$

This chain of statements is valid from left to right and from right to left, and it tells us that $x\in A\cap B$ is equivalent to $x\in B\cap A$.

Therefore, our proof is complete, and we write our conclusion.

> *Therefore, we conclude that $A \cap B = B\cap A$.*

Let's state the full proof.



### tutorial 17592186158602 — Stating the Full Proof

Theorem:

> *Given $A\subseteq U$ and $B\subseteq U$, where $U$ is a universal set, we have $A\cap B = B\cap A$.*

Proof:

> *Given any element $x\in U$, we have the following equivalent statements:*
> $x ∈ A∩B \mid ⇔(x ∈ A)∧(x ∈ B)$
> *and*
> $x ∈ B∩A \mid ⇔(x ∈ B)∧(x ∈ A)$
> *By the commutative law for conjunctions, $(x \in A) \land (x \in B)$ is equivalent to $(x \in B) \land (x \in A)$. Hence, we have the following chain of equivalent statements:*
> $x ∈ A∩B⇔(x ∈ A)∧(x ∈ B)⇔(x ∈ B)∧(x ∈ A)⇔x ∈ B∩A$
> *Therefore, we conclude that $A \cap B = B\cap A$.*



### example 17592186157024 — Proving Statements Using Chains of Biconditionals

Consider the following statement:

> Given that $U$ is a universal set and $A \subseteq U$, we have $(A \cap B) \cap C = A \cap (B \cap C)$.

A proof of this statement is given below.

> $\textrm{L1}{:}\:$ $x \in (A \cap B) \cap C$
> $\textrm{L2}{:}\:$ $\Leftrightarrow (x\in A \cap B) \land (x \in C)$
> $\textrm{L3}{:}\:$ $\Leftrightarrow ((x \in A) \land (x\in B))\land (x\in C)$
> $\textrm{L4}{:}\:$ $\Leftrightarrow (x\in A) \land ((x \in B) \land (x\in C))$
> $\textrm{L5}{:}\:$ $\Leftrightarrow (x\in A)\land(x \in (B \cap C))$
> $\textrm{L6}{:}\:$ $\Leftrightarrow x \in A \cap (B \cap C)$

Complete the missing entries in the following reasoning.

- Line $\textrm{L2}$ is equivalent to line $\textrm{L1}$ by $\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\,$.
- Line $\textrm{L4}$ is equivalent to line $\textrm{L3}$ by the law of
$\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\,$.
- Line $\textrm{L6}$ is equivalent to line $\textrm{L5}$ by the definition of $\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\,$.

Let's examine each statement in turn. Assume $X$, $Y$ and $Z$ are subsets of a universal set $U$, and $P$ is a statement.

- First, we consider lines $\textrm{L1}$ and $\textrm{L2}$. According to the definition of the intersection of sets, we have the following equivalence:
$a \in X \cap Y \quad \Leftrightarrow \quad (a \in X) \land (a \in Y)$
Therefore, line $\textrm{L2}$ is equivalent to line $\textrm{L1}$ by the $\bbox[3pt,Gainsboro]{\color{blue}\text{definition of the intersection of sets}}$.
- Next, we consider lines $\textrm{L3}$ and $\textrm{L4}$. According to the law of associativity for conjunctions, we have the following equivalence:
$((a \in X) \land (a\in Y)) \land (a\in Z)\quad \Leftrightarrow \quad (a \in X)\land ((a\in Y) \land (a\in Z))$
Therefore, line $\textrm{L4}$ is equivalent to line $\textrm{L3}$ by the law of $\bbox[3pt,Gainsboro]{\color{blue}\text{associativity for conjunctions}}$.
- Finally, we consider lines $\textrm{L5}$ and $\textrm{L6}$. According to the definition of the intersection of sets, we have the following equivalence:
$(a \in X) \land (a \in Y) \quad \Leftrightarrow \quad a \in X \cap Y$
Therefore, line $\textrm{L6}$ is equivalent to line $\textrm{L5}$ by the definition of $\bbox[3pt,Gainsboro]{\color{blue}\text{the intersection of sets}}$.

### tutorial 17592186158601 — Proof by Contradiction

Proof by contradiction is often a handy technique when proving set identities involving the empty set $\emptyset$.

Suppose we have a universal set $U$ that contains at least one element. Then, the statement

$x\in\emptyset$
is a contradiction for all $x\in U$ because the empty set contains no elements! This simple idea is the key to unlocking many proofs involving the empty set.

For example, suppose we wish to prove the following statement:

$$
\phantom{\lnot}P: \quad \emptyset \times A = \emptyset
$$

Note that the symbol $\times$ denotes the Cartesian product.

We'll proceed by contradiction. So, to prove that $P$ is true, we assume that $\lnot P$ is true and show this leads to a contradiction.

$$
\lnot P: \quad \emptyset \times A \neq \emptyset
$$

Since we're assuming that $\emptyset \times A$ is not empty, it must contain at least one element. So, we begin our proof as follows:

> *Assume, for a contradiction, that $\emptyset \times A \neq \emptyset$. Then, there exists at least one element $(x,y) \in \emptyset \times A$.*

We can now use the definition of the Cartesian product of two sets.

> *As a result, by the definition of the Cartesian product, we have*
> $x \in \emptyset \quad \textrm{and} \quad y \in A$.

But, by definition, the empty set contains no elements, so there cannot be a pair $(x,y)$ such that $x \in \emptyset$ and $y \in A$. Hence, we have a contradiction.

> *But $x \in \emptyset$ is a contradiction since the empty set contains no elements.*

Since we have a contradiction, our original assumption must be false. Hence, our proof is complete, and we write our conclusion as follows:

> *Therefore, we conclude that $\emptyset \times A = \emptyset$.*



### tutorial 17592186158603 — Stating the Full Proof

Theorem:

> *If $A$ is any set, then $\emptyset \times A = \emptyset$.*

Proof:

> *Assume, for a contradiction, that $\emptyset \times A \neq \emptyset$. Then, there exists at least one element $(x,y) \in \emptyset \times A$. As a result, by the definition of the Cartesian product, we have*
> $x \in \emptyset \quad \textrm{and} \quad y \in A$.
> *But $x \in \emptyset$ is a contradiction since the empty set contains no elements. Therefore, we conclude that $\emptyset \times A = \emptyset$.*



### example 17592186157023 — Proving Statements About the Empty Set

Prove by contradiction that $\emptyset \cap \emptyset = \emptyset$.

Let's write down the formal statement $P$ that we wish to prove:

$$
\phantom{\lnot}P: \quad \emptyset \cap \emptyset = \emptyset
$$

To prove that $P$ is true, we assume that $\lnot P$ is true and show this leads to a contradiction.

$$
\lnot P: \quad \emptyset \cap \emptyset \neq \emptyset
$$

Assuming $\emptyset \cap \emptyset$ is not empty, it must contain at least one element. So, we begin our proof as follows:

> Assume, for a contradiction, that $\emptyset \cap \emptyset \neq \emptyset$. Then, there exists at least one element $x \in \emptyset \cap \emptyset$.

We can now use the definition of the intersection of sets.

> As a result, by the definition of the intersection of sets, we have
> $x \in \emptyset \quad \textrm{and}\quad x \in \emptyset$,
> which is equivalent to $x \in \emptyset$. But this is a contradiction since the empty set contains no elements.

Since we have a contradiction, our original assumption must be false. Hence, we write our conclusion as follows:

> Therefore, we conclude that $\emptyset \cap \emptyset = \emptyset$.

## Representative practice (first three per skill; full bank in practice.json)

### Proving Statements Using Two Inclusions (2 captured questions)

Question 17592186157661 — None

Let $A$ be a set and $A⊆U$, where $U$ is a universal set. Prove that

$A∪A = A$.

First, we prove that $A∪A⊆A$. Let {{field-1}}. Then, by the definition of the {{field-2}}, $x ∈ A$ {{field-3}} $x ∈ A$. In any of these two cases, we obtain that {{field-4}} Therefore, $A∪A$ {{field-5}} $A$.

Solution: 

Question 17592186157678 — None

Consider the following statement:

> Given that $U$ is a universal set and $A⊆U$, we have $A∪∅ = A$.

A proof of the part that $A∪∅⊆A$ is given below.

> $L1$: Let $x ∈ A∪∅$.
> $L2$: Then, $x ∈ A$ or $x ∈ ∅$. So, we have two cases:
> $L3$: **Case 1:** $x ∈ A$.
> $L4$: **Case 2:** $x ∈ ∅$. But this is always false.
> $L5$: Therefore, $x ∈ A$.
> $L6$: Thus, $A∪∅⊆A$.

Select the correct options in the following reasoning.

Line $L2$ is equivalent to line $L1$ by the {{field-1}} of {{field-2}}.

Line $L5$ follows from $L3$ and $L4$ since in $L4$ we have a {{field-3}}.

Line $L6$ follows from $L1$ and $L5$ by the definition of the {{field-4}}.

Solution: 

### Proving Statements Using Chains of Biconditionals (2 captured questions)

Question 17592186157677 — None

Let $A$ be a set and $A⊆U$, where $U$ is a universal set. Prove that

$A∩A = A$.

Given any element $x ∈ U$, we have the following equivalent statements:

$∨$ {{field-1}} {{field-2}}

Solution: 

Question 17592186157679 — None

Consider the following statement:

> Given that $U$ is a universal set and $A⊆U$, we have $A∪A = A$.

A proof of this statement is given below.

> $L1$: $x ∈ A∪A$
> $L2$: $⇔(x ∈ A)∨(x ∈ A)$
> $L3$: $⇔x ∈ A$

Select the correct options in the following reasoning.

Line $L2$ is equivalent to line $L1$ by the {{field-1}} of
{{field-2}}.

Line $L3$ is equivalent to line $L2$ since a {{field-3}} of a statement with itself gives {{field-4}}.

Solution: 

### Proving Statements About the Empty Set (2 captured questions)

Question 17592186157675 — None

Prove by contradiction that $A∩A^(―) = ∅$ for any set $A$.

Assume, for a contradiction, that $A∩A^(―)$ {{field-1}} $∅$. Then, there exists at least one element $x$ {{field-2}} $A∩A^(―)$.

Solution: 

Question 17592186157676 — None

Prove by contradiction that if $B⊆A^(―)$, then $A∩B = ∅$ for all sets $A$ and $B$.

Assume, for a contradiction, that $B⊆A^(―)$ and $A∩B$ {{field-1}} $∅$. Then, there exists at least one element $x$ {{field-2}} $A∩B$.

Solution: 
