# 17592186050312 Sets and Functions

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186173158 — Introduction

A function relates an input to an output.
The set of all inputs is called the **domain** of the function, while the set of all *possible* outputs is the **codomain** of the function.

To say "*the function $f$ maps the set $X$ to the set $Y,$*" we can use the following notation:

$$
f : X \to Y
$$

In this case, 

- the domain of $f$ is $X,$ and

- the codomain of $f$ is $Y.$

You might be used to calling the set of outputs of a function as the *range* of the function. However, there is a subtle difference between codomain and range, which we'll learn about during this lesson.



### example 17592186171837 — Interpreting the Arrow Function Notation

Which of the following functions has the codomain $[0,1]?$

I. $p: \{ 0, 1 \} \to \mathbb{R}$

II. $q: \mathbb{R} \to [ 0, 1 ]$

III. $r: [0,1] \to [ 0, 1 )$

The notation $f: X \to Y$ means that the function $f$ maps the set $X$ to the set $Y.$ In this case,

- the domain of $f$ is $X,$

- the codomain of $f$ is $Y.$

With that in mind, let's examine our functions.

- The codomain of $p$ is $\mathbb{R},$ the set of real numbers.

- The codomain of $q$ is $[ 0, 1 ],$ the interval from $0$ and $1$ (including $0$ and $1$).

- The codomain of $r$ is $[ 0, 1),$ the interval from $0$ to $1$ (including $0$ but not including $1$).

Therefore, the correct answer is "II only."

### example 17592186171838 — Writing a Function Using Arrow Notation

Which of the following is the correct symbolic notation for the sentence given below?

$\qquad$ *"The function $g$ maps the set of rational numbers to the set $Y$."*

I. $g:\mathbb{Q} \to Y$

II. $g: Y \to \mathbb{Q}$

III. $g:\mathbb{R} \to Y$

The sentence *"The function $g$ maps the set of rational numbers to the set $Y$"* is equivalent to the following symbolic notation:

$\qquad$ $g:\mathbb{Q} \to Y$

Here, the domain of $g$ is $\mathbb Q,$ and the codomain of $g$ is $Y.$

Therefore, the correct answer is "I only".

### tutorial 17592186173159 — An Alternative Arrow Notation

The alternative arrow notation for a function "$\mapsto$" describes to which element of the codomain each element in the domain is mapped.

Consider the following function $f,$ defined by the alternative arrow notation:

$$
f : x \mapsto |x|
$$

This means that the function $f$ maps the element $x$ in the domain to $|x|$ in the codomain. Notice that this can also be written as

$$
f(x) = |x|.
$$



### example 17592186171839 — Using the Alternative Arrow Notations

Which of the following is equivalent to $g(x)=x-x^3?$

I. $g:x \mapsto x-x^3$

II. $g:x \mapsto -x^3$

III. $g:-x \mapsto x^3$

The notation $g(x)=x-x^3$ means that the function $g$ maps the element $x$ in the domain to $x-x^3$ in the codomain. This can also be written as

$$
g:x \mapsto x-x^3.
$$

Therefore, the correct answer is "I only."

### tutorial 17592186173160 — Codomain vs. Range

How do the codomain and range differ? Recall that in the notation $f : X \to Y$ the codomain of the function is $Y.$

On the other hand, the range of $f$ is the subset of the codomain that contains all values $y \in Y$ that are mapped to by at least one element $x \in X.$

Consider the function $f(x)=|x|$ shown in the mapping diagram below.

![](images/28/28fc79adea3f40c735cc0015069b4dc30433b7a3d372cc00148d6412a8ba27af.png)

Inspecting the diagram, we see that:

- the domain of $f$ is $X = \{ -2,-1,1,2,3 \},$

- the codomain of $f$ is $Y = \{ 0,1,2,3,4 \},$

- the range of $f$ is $\{ 1,2,3 \},$ the subset of elements of $Y$ that have at least one incoming arrow.

The range depends on the domain we choose. If we remove the element $3$ from the domain in the diagram above, then the element $3$ in the codomain will not have any incoming arrows. Therefore, the range of the function will be $\{ 1,2 \}.$



### example 17592186171840 — Identifying Codomains and Ranges

Which of the following is the correct interpretation of $g: \{ -1,0,1 \} \to \mathbb{R}?$

I. The domain of $g$ is $\{ -1,0,1 \}$

II. The codomain of $g$ is $\mathbb{R}$

III. The range of $g$ is $\mathbb{R}$

The notation 

$$
g: \{ -1,0,1 \} \to \mathbb{R}
$$

means that the function $g$ maps the set $\{ -1,0,1 \}$ to the set $\mathbb{R}.$ In this case,

- the domain of $g$ is $\{ -1,0,1 \},$ and

- the codomain of $g$ is $\mathbb{R}.$ Note that this is *not* necessarily the range.

As a result, statements I and II are true, while statement III is false.

Therefore, the correct answer is "I and II only."

## Representative practice (first three per skill; full bank in practice.json)

### Interpreting the Arrow Function Notation (12 captured questions)

Question 17592186172627 — question.difficulty/easy

Which of the following functions has the codomain $[0,3)?$

I. $p:\{0,3\}\to R$

II. $q:R\to [0,3)$

III. $r:[0,3)\to \{0,3\}$

Solution: The notation $f:X\to Y$ means that the function $f$ maps the set $X$ to the set $Y.$ In this case,

- the domain of $f$ is $X,$

- the codomain of $f$ is $Y.$

With that in mind, let's examine our functions.

- The codomain of $p$ is $R,$ the set of real numbers.

- The codomain of $q$ is $[0,3),$ the interval from $0$ to $3$ (including $0$ but not including $3$).

- The codomain of $r$ is $\{0,3\},$ the set containing the two numbers $0$ and $3$ only.

Therefore, the correct answer is "II only."

Answer selection: II only

Question 17592186172643 — None

Which of the following functions has the domain $R$?

1. $p: R → [- 5, 5]$
2. $q: R → R$
3. $r: [- 5, 5] → R$

Solution: 

Question 17592186240931 — question.difficulty/easy

Which of the following functions has the codomain ${0,1}?$

Select all that apply.

Solution: The notation $f:X\to Y$ means that the function $f$ maps the set $X$ to the set $Y.$ In this case,

- the domain of $f$ is $X,$

- the codomain of $f$ is $Y.$

With that in mind, let's examine our functions.

- The codomain of $p$ is $Z,$ the set of integers.

- The codomain of $q$ is ${0,1},$ the set containing the two numbers $0$ and $1$ only.

- The codomain of $r$ is $(0,1),$ the interval from $0$ to $1$ (excluding both $0$ and $1$).

Therefore, the correct answer is $q:[0,1]\to {0,1}$ only.

Answer $p:{0,1}\to Z$: false

Answer $q:[0,1]\to {0,1}$: true

Answer $r:{0,1}\to (0,1)$: false

### Writing a Function Using Arrow Notation (11 captured questions)

Question 17592186172628 — question.difficulty/easy

Which of the following is the correct symbolic notation for the sentence given below?

*"The function $g$ maps the set $X$ to the set of real numbers."*

Solution: The sentence *"The function $g$ maps the set $X$ to the set of real numbers"* is equivalent to the following symbolic notation:

$\,$ $g:X\to R$

Here, the domain of $g$ is $X,$ and the codomain of $g$ is $R.$

Answer selection: g:X\to R

Question 17592186172644 — question.difficulty/easy

Which of the following is the correct symbolic notation for the sentence given below?

*"The function $f$ maps the interval from $-1$ to $1$ exclusive to the set $Y.$"*

Solution: The sentence *"The function $f$ maps the interval from $-1$ to $1$ exclusive to the set $Y$"* is equivalent to the following symbolic notation:

$\,$ $f:(-1,1)\to Y$

Here, the domain of $f$ is $(-1,1),$ and the codomain of $f$ is $Y.$

Answer selection: f:(-1,1)\to Y

Question 17592186240944 — question.difficulty/easy

Which of the following is the correct symbolic notation for the sentence given below?

*"The function $g$ maps the set $X$ to the set containing the two numbers $-1$ and $1$ only."*

Solution: The sentence *"The function $g$ maps the set $X$ to the set containing the two numbers $-1$ and $1$ only"* is equivalent to the following symbolic notation:

$\,$ $g:X\to {-1,1}$

Here, the domain of $g$ is $X,$ and the codomain of $g$ is ${-1,1}.$

Answer selection: g:X\to {-1,1}

### Using the Alternative Arrow Notations (14 captured questions)

Question 17592186172629 — question.difficulty/easy

Which of the following is equivalent to $f:x↦{x}^{2}-3?$

Solution: The notation $f:x↦{x}^{2}-3$ means that the function $f$ maps the element $x$ in the domain to ${x}^{2}-3$ in the codomain. This can also be written as

$$
f(x)={x}^{2}-3.
$$

Answer selection: f(x)={x}^{2}-3

Question 17592186172630 — question.difficulty/easy

Which of the following is equivalent to $h(x)=5x+{x}^{2}?$

Solution: The notation $h(x)=5x+{x}^{2}$ means that the function $h$ maps the element $x$ in the domain to $5x+{x}^{2}$ in the codomain. This can also be written as

$$
h:x↦5x+{x}^{2}.
$$

Answer selection: h:x↦5x+{x}^{2}

Question 17592186240963 — question.difficulty/easy

Which of the following is equivalent to $f:x↦2x-{x}^{3}?$

Solution: The notation $f:x↦2x-{x}^{3}$ means that the function $f$ maps the element $x$ in the domain to $2x-{x}^{3}$ in the codomain. This can also be written as

$$
f(x)=2x-{x}^{3}.
$$

Answer selection: f(x)=2x-{x}^{3}

### Identifying Codomains and Ranges (12 captured questions)

Question 17592186172626 — None

Which of the following is the correct interpretation of $f: R → {0, 1, 3}$?

1. The domain of $f$ is $R$
2. The codomain of $f$ is $R$
3. The range of $f$ is ${0, 1, 3}$

Solution: 

Question 17592186172633 — question.difficulty/easy

![](images/dc/dcee145044fe79dc7f4d07c3c4c1248df358cd8eda7a173cd8d4641f13404122.png)

Consider the function $f:X\to Y$ given by the mapping diagram shown above. Which of the following statements are true?

Select all that apply.

Solution: The notation $f:X\to Y$ means that the function $f$ maps the set $X$ to the set $Y.$ In this case,

- the domain of $f$ is $X,$

- the codomain of $f$ is $Y.$

The range of $f$ is the subset of the codomain that contains all values $y\in Y$ that are mapped to by at least one element $x\in X.$

With that in mind, let's inspect our diagram:

- the domain of $f$ is $X={0,1,2,3},$

- the codomain of $f$ is $Y={0,-1,-2},$

- the range of $f$ is ${0,-1},$ the subset of elements of $Y$ that have at least one incoming arrow.

As a result, statements “The domain of $f$ is ${0,1,2,3}$” and “The range of $f$ is ${0,-1}$” are true, while statement “The codomain of $f$ is ${0,-1}$” is false.

Therefore, the correct answer “The domain of $f$ is ${0,1,2,3}$”; “The range of $f$ is ${0,-1}$” only.

Answer The codomain of $f$ is ${0,-1}$: false

Answer The domain of $f$ is ${0,1,2,3}$: true

Answer The range of $f$ is ${0,-1}$: true

Question 17592186240965 — question.difficulty/moderate

Which of the following is the correct interpretation of $g:{0,1}\to Z?$

Select all that apply.

Solution: The notation 

$$
g:{0,1}\to Z
$$

means that the function $g$ maps the set ${0,1}$ to the set $Z.$ In this case,

- the domain of $g$ is ${0,1},$ and

- the codomain of $g$ is $Z.$ Note that ${0,1}⊆Z$ is *not* necessarily the range.

As a result, statements “The domain of $g$ is ${0,1}$” and “The codomain of $g$ is $Z$” are true, while statement “The range of $g$ is ${0,1}$” is false.

Therefore, the correct answer is “The domain of $g$ is ${0,1}$”; “The codomain of $g$ is $Z$” only.

Answer The codomain of $g$ is $Z$: true

Answer The domain of $g$ is ${0,1}$: true

Answer The range of $g$ is ${0,1}$: false
