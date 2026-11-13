# 17592186048468 Proving Subset Relations

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186205286 — Intro

Suppose $A$ and $B$ are sets, and $U$ is a universal set. Then, $A$ is a subset of $B$ if every element of $A$ is also an element of $B$. We can express this using the following formal notation:

$$
A\subseteq B \quad \Leftrightarrow \quad \forall x \in U,\: x\in A \Rightarrow x\in B
$$

To *prove* that $A$ is a subset of $B$, the standard method is to take a fixed but arbitrary element of $A$ and show that it is also an element of $B$.

Consider the following sets:

$$
A = \{6m-4 \:: \: m \in \mathbb{N} \}, \qquad B = \{2n \:: \: n \in \mathbb{N} \}
$$

To get a feel for these sets, let's write down the first few elements of each set:

$$
A = \{{\color{blue}{2}}, {\color{blue}{8}}, {\color{blue}{14}}, {\color{blue}{20}} \ldots\}
$$

$$
B = \{{\color{blue}{2}}, 4, 6, {\color{blue}{8}}, 10, 12, {\color{blue}{14}}, 16,18, {\color{blue}{20}}, \ldots\}
$$

So intuitively, it certainly looks as though $A\subseteq B$. Let's now prove this result.



### tutorial 17592186205271 — Proving That a Given Set Is a Subset

We wish to prove that $A \subseteq B$, where the sets $A$ and $B$ are given by

$$
A = \{6m-4 \:: \: m \in \mathbb{Z} \}, \qquad B = \{2n \:: \: n \in \mathbb{Z} \}
$$

We begin our proof as follows.

> *To prove that $A \subseteq B$, we take an arbitrary element of $A$ and show that it is an element of $B$.*

Now, we denote an arbitrary element of $A$ by $x$ and use the definition of $A$.

> *So, let $x \in A$. Then, according to the definition of $A$, there exists $m \in \mathbb{Z}$ such that*
> $x = 6m-4$.

The key to unlocking the proof is to rewrite $x$ to match the definition of $B$. In other words, we need to write $x=2n$, where $n$ is an integer.

> *Note that*
> $\begin{aligned}x & =6m-4 \\  & =2(3m-2).\end{aligned}$.
> *Denote $n=3m-2$. Since $m$ is an integer, $n$ is also an integer. Thus,*
> $x=2n$,
> *where $n \in \mathbb{Z}$. So, by the definition of $B$, we have $x \in B$.*

So, we have shown that $x\in A$ implies $x \in B$, and we can state our conclusion.

> *Therefore, $A \subseteq B$.*



### tutorial 17592186205278 — Stating the Full Proof

Proposition:

> *Given that $A = \{6m-4 \:: \: m \in \mathbb{N} \}$ and $B = \{2n \:: \: n \in \mathbb{N} \}$, prove that $A \subseteq B$.*

Proof:

> *To prove that $A \subseteq B$, we take an arbitrary element of $A$ and show that it is an element of $B$.*
> *So, let $x \in A$. Then, according to the definition of $A$, there exists $m \in \mathbb{N}$ such that*
> $x = 6m-4$.
> *Note that*
> $\begin{aligned}x & =6m-4 \\  & =2(3m-2).\end{aligned}$.
> *Denote $n=3m-2$. Since $m$ is an integer, $n$ is also an integer. Thus,*
> $x=2n$,
> *where $n \in \mathbb{N}$. So, by the definition of $B$, we have $x \in B$.*
> *Therefore, $A \subseteq B$.*



### example 17592186203726 — Proving Subset Relations Using Constructive Definitions

Consider the following sets.

$$
\displaystyle A = \{9^{m+2}\:: \: m \in \mathbb{Z} \}, \qquad B = \{3^n \:: \: n \in \mathbb{Z} \}
$$
Prove that $A \subseteq B$.

To show that $A\subseteq B$, we need to show that every element of $A$ is also an element of $B$.

So, we begin our proof as follows.

> To prove that $A \subseteq B$, we take an arbitrary element of $A$ and show that its is an element of $B$.

Now, we denote an arbitrary element of $A$ by $x$ and use the definition of $A$.

> So, let $x \in A$. Then, according to the definition of $A$, there exists $m \in \mathbb{Z}$ such that
> $x = 9^{m+2}$.

The key to unlocking the proof is to rewrite $x$ to match the definition of $B$. In other words, we need to write $x=3^n$, where $n$ is an integer.

> Note that
> $\begin{aligned}x & ={9}^{m+2} \\  & ={({3}^{2})}^{m+2} \\  & ={3}^{2(m+2)}.\end{aligned}$.
> Denote $n=2(m+2)$. Since $m$ is an integer, $n$ is also an integer. Thus,
> $x=3^n$,
> where $n \in \mathbb{Z}$. So, by the definition of $B$, we have $x \in B$.

So, we have shown that $x\in B$, and we can state our conclusion.

> Therefore, $A \subseteq B$.

### example 17592186203731 — Proving Subset Relations Using Conditional Definitions

Consider the following sets.

$$
\displaystyle A = \{x \in \Bbb Z: x \equiv 3 \: \: (\textrm{mod 4})\}, \qquad B = \{x \in \Bbb Z: x \equiv 1 \: \: (\textrm{mod 2})\}
$$
Prove that $A \subseteq B$.

To show that $A\subseteq B$, we need to show that every element of $A$ is also an element of $B$.

So, we begin our proof as follows.

> To prove that $A \subseteq B$, we take an arbitrary element of $A$ and show that its is an element of $B$.

Now, we denote an arbitrary element of $A$ by $x$ and use the definition of $A$.

> So, let $x \in A$. Then, according to the definition of $A$, there exists $m \in \mathbb{Z}$ such that
> $\begin{aligned}x-3 & =4m \\ x & =3+4m.\end{aligned}$.

The key to unlocking the proof is to rewrite $x$ to match the definition of $B$. In other words, we need to write

$$
x = 1+2n
$$

where $n$ is an integer.

> Note that
> $\begin{aligned}x & =3+4m \\  & =1+2+4m \\  & =1+2(1+2m)\end{aligned}$
> Denote $n=1+2m$. Since $m$ is an integer, $n$ is also an integer. Thus,
> $x=1+2n\qquad\Leftrightarrow \qquad x\equiv 1\:(\textrm{mod} 2)$.
> Therefore, by the definition of $B$, we have $x \in B$.

So, we have shown that $x\in B$, and we can state our conclusion.

> So, we conclude that $A \subseteq B$.

### tutorial 17592186205287 — Disproving a Subset Relation

According to the definition, $A$ is a subset of $B$ if and only if $x\in A$ implies $x\in B$.

$A\subseteq B \quad \Leftrightarrow\quad \forall \: x \in U, \: x \in A \Rightarrow x \in B$
where $U$ is a universal set.

Now, suppose we want to show that $A$ is *not* a subset of $B$. To do this, we need to show that the above statement is false or, equivalently, that its negation is true.

We negate our conditional statement as follows:

$$
¬(∀x ∈ U, x ∈ A⇒x ∈ B) \mid ≡∃x ∈ U, ¬(x ∈ A⇒x ∈ B); ≡∃x ∈ U, ¬(¬(x ∈ A)∨(x ∈ B)); ≡∃x ∈ U, ¬¬(x ∈ A)∧¬(x ∈ B); ≡∃x ∈ U, x ∈ A∧x ∉ B
$$

To summarize:
$A\not\subseteq B \quad \Leftrightarrow\quad \exists x \in U, \: x \in A \land x \notin B$

So, to show that $A$ is *not* a subset of $B$, we need to show that there exists a single element of $A$ that does not lie in $B$.



### example 17592186203727 — Proving X Is Not a Subset of Y

Consider the following sets.

$$
\displaystyle A = \{x \in \Bbb R: \cos x = 1 \}, \qquad B = \{x \in \Bbb R: \sin x = 0\}
$$
Disprove that $B \subseteq A$.

Recall that $B \subseteq A$ if, for any $x \in B$, we have $x \in A$. More formally,
$\forall \: x \in U, \: x \in B \Rightarrow x \in A$,
where $U$ is the universal set. To disprove the statement means to show that it's false or, equivalently, that the negation is true.

By negating the above expression, we obtain

$$
¬(∀x ∈ U, x ∈ B⇒x ∈ A) \mid ≡∃x ∈ U, ¬(x ∈ B⇒x ∈ A); ≡∃x ∈ U, ¬(¬(x ∈ B)∨(x ∈ A)); ≡∃x ∈ U, ¬¬(x ∈ B)∧¬(x ∈ A); ≡∃x ∈ U, x ∈ B∧x ∉ A
$$

So, we proceed as follows:

> We need to show that there exists an element $x$ such that $x \in B$ and $x \notin A$.

Any suitable element $x$ will do, so we will try to find the most obvious one.

> Consider $x=\pi$.

First, we show that this element lies in $B$.

> Note that $\pi \in B\,$ since $\sin \pi = 0$, which is consistent with the definition of $B$.

We now explain why $x=\pi$ cannot be an element of $A$.

> Now, $\cos \pi= -1 \neq 1$. Hence, $\pi \notin A$.

So, we have shown that $\pi\in B$ and $\pi\notin A$, and we can state our conclusion.

> Therefore, $B \not\subseteq A$.

### tutorial 17592186205285 — Set Equality

Recall that two sets $A$ and $B$ are **equal** (or **equivalent**) if they have the same elements. In other words, if every element of $A$ is an element of $B$ *and* vice-versa.

This means that $A=B$ if and only if $A\subseteq B$ *and* $B\subseteq A$. We can write this using the following formal notation:

$$
A = B \quad\Leftrightarrow\quad (A\subseteq B) \land (B\subseteq A)
$$

We'll present a formal proof of this result at the end of the lesson.

This result means we can prove that two sets are equivalent using the following method:

- First, we prove that $x\in A\Rightarrow x\in B$
- Then, we prove that $x\in B\Rightarrow x\in A$

The two proofs in conjunction give a valid proof that $A=B$.

Let's see an example.



### example 17592186203728 — Proving Set Equality

Consider the following sets.
$$
\displaystyle A = \{3m+1 \:: \: m \in \mathbb{Z} \}, \qquad B = \{3n+7 \:: \: n \in \mathbb{Z} \}
$$
Prove that $A = B$.

Recall that $A = B$ if and only if $A\subseteq B$ and $B\subseteq A$.

So, we begin our proof as follows:

> To prove that $A=B$, we must show that $A \subseteq B$ and $B \subseteq A$.

First, let's prove that $A \subseteq B$. We denote an arbitrary element of $A$ by $x$ and use the definition of $A$.

> **Part 1.** Proving that $A \subseteq B$.
> Let $x \in A$. Then, there exists $m \in \mathbb{Z}$ such that $x = 3m+1$.

Next, we rewrite $x$ to match the definition of $B$. In other words, we need to write

$$
x=3n+7
$$

where $n$ is an integer.

> Note that
> $\begin{aligned}x & =3m+1 \\  & =3m+(7-6) \\  & =3m-6+7 \\  & =3(m-2)+7.\end{aligned}$.
> Denoting $n=m-2$, we get that
> $x=3n+7$,
> where $n \in \mathbb{Z}$. So, by the definition of $B$, we have $x \in B$. Thus, $A \subseteq B$.

Next, let's prove that $B \subseteq A$.

> **Part 2.** Proving that $B \subseteq A$.
> Let $x \in B$. Then, there exists $n \in \mathbb{Z}$ such that $x = 3n+7$.

Next, we rewrite $x$ to match the definition of $A$. In other words, we need to write

$$
x=3m+1
$$

where $m$ is an integer.

> Note that
> $\begin{aligned}x & =3n+7 \\  & =3n+(6+1) \\  & =3(n+2)+1.\end{aligned}$.
> Denoting $m=n+2$, we get that
> $x=3m+1$,
> where $m \in \mathbb{Z}$. So, by the definition of $A$, we have $x \in A$. Thus, $B \subseteq A$.

Finally, we've shown that $A\subseteq B$ and $B\subseteq A$. Therefore, $A=B$, and we state our conclusion.

> Therefore, $A = B$.

### tutorial 17592186205288 — Proving Set Equality Using Subsets

In this lesson, we used the fact that $A=B$ if and only if $A\subseteq B$ *and* $B\subseteq A{:}$

$$
A = B \quad\Leftrightarrow\quad (A\subseteq B) \land (B\subseteq A)
$$

A proof of this result is given below.

Proof:

> *We need to show the following:*
> $A = B \quad\Leftrightarrow\quad (A\subseteq B) \land (B\subseteq A)$
> *This is the same as proving two implications.*
> ***Case $\Rightarrow{:}$*** *We need to show that*
> $A=B \quad\Rightarrow\quad (A\subseteq B) \land (B\subseteq A)$.
> *Suppose $x \in A$. Then, by the definition of equal sets, $x \in B$. Thus, $A \subseteq B$ by the definition of a subset. Similarly, if $x \in B$, then $x \in A$. Thus, $B \subseteq A$.*
> ***Case $\Leftarrow{:}$*** *We need to show that*
> $(A\subseteq B) \land (B\subseteq A) \quad\Rightarrow\quad A=B$.
> *Suppose $A \subseteq B$ and $B \subseteq A$. Now, since $A \subseteq B$, then for any $x \in A$, we have $x \in B$ by the definition of a subset. Similarly, since $B \subseteq A$, then for any $x \in B$, we have $x \in A$. Thus, by the definition of equal sets, $A=B$.*
> *Therefore, $A=B$ if and only if $A \subseteq B$ and $B \subseteq A$.*



## Representative practice (first three per skill; full bank in practice.json)

### Proving Subset Relations Using Constructive Definitions (2 captured questions)

Question 17592186204304 — None

Consider the following sets.

$$
\displaystyle A = {12m + 36: m ∈ Z}, B = {4n: n ∈ Z}
$$
Prove that $A⊆B$.

To prove that $A⊆B$, we take an arbitrary element of {{field-1}} and show that it lies in {{field-2}}.

Solution: 

Question 17592186204308 — None

Consider the following sets.

$$
\displaystyle A = {4^{m}: m ∈ Z}, B = {2^{n}: n ∈ Z}
$$
Prove that $A⊆B$.

To prove that $A⊆B$, we take an arbitrary element of {{field-1}} and show that it lies in {{field-2}}.

Solution: 

### Proving Subset Relations Using Conditional Definitions (2 captured questions)

Question 17592186204309 — None

Consider the following sets.

$$
\displaystyle A = {x ∈ Z: x≡2(mod 9)}, B = {x ∈ Z: x≡2(mod 3)}
$$
Prove that $A⊆B$.

To prove that $A⊆B$, we take an arbitrary element of {{field-1}} and show that it lies in {{field-2}}.

Solution: 

Question 17592186204318 — None

Consider the following sets.

$$
\displaystyle A = {x ∈ R: \tan x = 1}, B = {x ∈ R: 2\sin^{2} x = 1}
$$
Prove that $A⊆B$.

To prove that $A⊆B$, we take an arbitrary element of {{field-1}} and show that it lies in {{field-2}}.

Solution: 

### Proving X Is Not a Subset of Y (2 captured questions)

Question 17592186204305 — None

Consider the following sets.

$$
\displaystyle A = {12m + 36: m ∈ Z}, B = {4n: n ∈ Z}
$$
Disprove that $B⊆A$.

We need to show that {{field-1}}.

Solution: 

Question 17592186204310 — None

Consider the following sets.

$$
\displaystyle A = {x ∈ Z: x≡2(mod 9)}, B = {x ∈ Z: x≡2(mod 3)}
$$
Disprove that $B⊆A$.

We need to show that {{field-1}}.

Solution: 

### Proving Set Equality (2 captured questions)

Question 17592186204315 — None

Consider the following sets.
$$
\displaystyle A = {2 \cdot 4^{m}: m ∈ Z}, B = {2^{n}: n = 2k + 1, k ∈ Z}
$$
Prove that $A = B$.

To prove that $A = B$, we must show that $A⊆$ {{field-1}}
and
{{field-2}}
{{field-3}}
{{field-4}}.

Solution: 

Question 17592186204316 — None

Consider the following sets.
$$
\displaystyle A = {x ∈ R: \sin (x + 2π) =-1}, B = {x ∈ R: \sin x =-1}
$$
Prove that $A = B$.

To prove that $A = B$, we must show that $A⊆$ {{field-1}}
and
{{field-2}}
{{field-3}}
{{field-4}}.

Solution: 
