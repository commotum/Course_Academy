# Matrix statement review

All raw source replays are evidence-only. Normal records preserve RADIO and their source banks; q42115 hard/solution/correct key are inferred. Easy is authored.


## Original q-42091

Consider the matrix 
$A=[\begin{aligned}4 & 0 & 0 \\ 2 & 1 & 0 \\ 0 & 5 & 3\end{aligned}].$
Which of the following statements are true?

- $A$ is upper triangular
- $A$ is lower triangular
- ${A}^{T}$ is upper triangular

Choices: I only; II and III only; III only; I and III only; II only

Let's analyze each statement in turn.

- Statement I is false, since $A$ has non-zero entries below the main diagonal:

$$
A=[\begin{aligned}4 & 0 & 0 \\ 2 & 1 & 0 \\ 0 & 5 & 3\end{aligned}]
$$

- Statement II is true. All the entries above the main diagonal of $A$ are zeros:

$$
A=[\begin{aligned}4 & 0 & 0 \\ 2 & 1 & 0 \\ 0 & 5 & 3\end{aligned}]
$$

- Statement III is true. All the entries below the main diagonal of ${A}^{T}$ are zeros:

$$
{A}^{T}=[\begin{aligned}4 & 2 & 0 \\ 0 & 1 & 5 \\ 0 & 0 & 3\end{aligned}]
$$

Therefore, the correct answer is "II and III only".


### Generated normal variant

Consider the matrix 
$A=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & -4 & 0\end{aligned}].$
Which of the following statements are true?

- $A$ is upper triangular
- $A$ is lower triangular
- ${A}^{T}$ is upper triangular

Choices: I and III only; II only; II and III only; III only; I only

Let's analyze each statement in turn.

- Statement I is false, since $A$ has non-zero entries below the main diagonal:

$$
A=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & -4 & 0\end{aligned}]
$$

- Statement II is true. All the entries above the main diagonal of $A$ are zeros:

$$
A=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & -4 & 0\end{aligned}]
$$

- Statement III is true. All the entries below the main diagonal of ${A}^{T}$ are zeros:

$$
{A}^{T}=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & -4 \\ 0 & 0 & 0\end{aligned}]
$$

Therefore, the correct answer is "II and III only".


## Original q-42115

Consider the matrix
$A = \begin{bmatrix}-3 & 1 & 0 \\ -1 & 1 & 0 \\ 0 & 0 & 5\end{bmatrix}$.
Which of the following statements are true?

1. $A$ is upper triangular
2. $A^{T} + A$ is upper triangular
3. $A$ is lower triangular

Choices: I and III only; II only; III only; None; I only


### Generated normal variant

Consider the matrix
$A = \begin{bmatrix}8 & 0 & 0 \\ 0 & -8 & -4 \\ 0 & 4 & 0\end{bmatrix}$.
Which of the following statements are true?

1. $A$ is upper triangular
2. $A^{T} + A$ is upper triangular
3. $A$ is lower triangular

Choices: None; I only; II only; III only; I and III only

Let's analyze each statement in turn.

- Statement I is false, since $A$ has non-zero entries below the main diagonal:

$$
A=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & -4 \\ 0 & 4 & 0\end{aligned}]
$$

- Statement II is true, since all the entries below the main diagonal are zeros:

$$
A^{T} + A=[\begin{aligned}16 & 0 & 0 \\ 0 & -16 & 0 \\ 0 & 0 & 0\end{aligned}]
$$

- Statement III is false, since $A$ has non-zero entries above the main diagonal:

$$
A=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & -4 \\ 0 & 4 & 0\end{aligned}]
$$

Therefore, the correct answer is "II only".


## Original q-126477

Consider the matrix 
$B=[\begin{aligned}2 & 0 & 0 & 0 \\ 0 & -3 & -1 & 1 \\ 0 & 0 & 4 & 5 \\ 0 & 0 & 0 & 2\end{aligned}].$
Which of the following statements are true?

- $B$ is upper triangular
- $B$ is lower triangular
- $B-{B}^{T}$ is upper triangular

Choices: I and II only; I only; II only; I and III only; III only

Let's analyze each statement in turn.

- Statement I is true, since all the entries below the main diagonal equal to zero:

$$
B=[\begin{aligned}2 & 0 & 0 & 0 \\ 0 & -3 & -1 & 1 \\ 0 & 0 & 4 & 5 \\ 0 & 0 & 0 & 2\end{aligned}]
$$

- Statement II is false, since $A$ has non-zero entries above the main diagonal:

$$
B=[\begin{aligned}2 & 0 & 0 & 0 \\ 0 & -3 & -1 & 1 \\ 0 & 0 & 4 & 5 \\ 0 & 0 & 0 & 2\end{aligned}]
$$

- Statement III is false, since the result of $B-{B}^{T}$ has non-zero entries below the main diagonal:

$$
B-{B}^{T}=[\begin{aligned}0 & 0 & 0 & 0 \\ 0 & 0 & -1 & 1 \\ 0 & 1 & 0 & 5 \\ 0 & -1 & -5 & 0\end{aligned}]
$$

Therefore, the correct answer is "I only".


### Generated normal variant

Consider the matrix 
$B=[\begin{aligned}8 & 0 & 0 & 0 \\ 0 & -8 & 0 & -2 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & -4\end{aligned}].$
Which of the following statements are true?

- $B$ is upper triangular
- $B$ is lower triangular
- $B-{B}^{T}$ is upper triangular

Choices: I and III only; III only; I only; II only; I and II only

Let's analyze each statement in turn.

- Statement I is true, since all the entries below the main diagonal equal to zero:

$$
B=[\begin{aligned}8 & 0 & 0 & 0 \\ 0 & -8 & 0 & -2 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & -4\end{aligned}]
$$

- Statement II is false, since $B$ has non-zero entries above the main diagonal:

$$
B=[\begin{aligned}8 & 0 & 0 & 0 \\ 0 & -8 & 0 & -2 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & -4\end{aligned}]
$$

- Statement III is false, since the result of $B-{B}^{T}$ has non-zero entries below the main diagonal:

$$
B-{B}^{T}=[\begin{aligned}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & -2 \\ 0 & 0 & 0 & 1 \\ 0 & 2 & -1 & 0\end{aligned}]
$$

Therefore, the correct answer is "I only".


## Original q-126479

Consider the matrix 
$C=[\begin{aligned}5 & 0 & 0 \\ 0 & -2 & 0 \\ 0 & 0 & -5\end{aligned}].$
Which of the following statements are true?

- $C$ is upper triangular
- $C$ is lower triangular
- ${C}^{T}$ is upper triangular

Choices: I, II, and III; III only; I only; I and III only; II and III only

Let's analyze each statement in turn.

- Statement I is true. All the entries below the main diagonal of $C$ are zeros:

$$
C=[\begin{aligned}5 & 0 & 0 \\ 0 & -2 & 0 \\ 0 & 0 & -5\end{aligned}]
$$

- Statement II is true. All the entries above the main diagonal of $C$ are zeros:

$$
C=[\begin{aligned}5 & 0 & 0 \\ 0 & -2 & 0 \\ 0 & 0 & -5\end{aligned}]
$$

- Statement III is true. All the entries below the main diagonal of ${C}^{T}$ are zeros:

$$
{C}^{T}=[\begin{aligned}5 & 0 & 0 \\ 0 & -2 & 0 \\ 0 & 0 & -5\end{aligned}]
$$

Therefore, the correct answer is "I, II, and III".


### Generated normal variant

Consider the matrix 
$C=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & 0 & 0\end{aligned}].$
Which of the following statements are true?

- $C$ is upper triangular
- $C$ is lower triangular
- ${C}^{T}$ is upper triangular

Choices: I and III only; II and III only; III only; I only; I, II, and III

Let's analyze each statement in turn.

- Statement I is true. All the entries below the main diagonal of $C$ are zeros:

$$
C=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & 0 & 0\end{aligned}]
$$

- Statement II is true. All the entries above the main diagonal of $C$ are zeros:

$$
C=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & 0 & 0\end{aligned}]
$$

- Statement III is true. All the entries below the main diagonal of ${C}^{T}$ are zeros:

$$
{C}^{T}=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & 0 & 0\end{aligned}]
$$

Therefore, the correct answer is "I, II, and III".


## Original q-126484

Consider the matrix 
$B=[\begin{aligned}3 & 0 & 0 \\ 0 & -2 & 0 \\ 0 & 4 & 5\end{aligned}].$
Which of the following statements are true?

- $B$ is upper triangular
- $B$ is lower triangular
- ${B}^{T}$ is lower triangular

Choices: III only; I only; I and II only; II only; I and III only

Let's analyze each statement in turn.

- Statement I is false, since $B$ has non-zero entries below the main diagonal:

$$
B=[\begin{aligned}3 & 0 & 0 \\ 0 & -2 & 0 \\ 0 & 4 & 5\end{aligned}]
$$

- Statement II is true. All the entries above the main diagonal of $B$ are zeros:

$$
B=[\begin{aligned}3 & 0 & 0 \\ 0 & -2 & 0 \\ 0 & 4 & 5\end{aligned}]
$$

- Statement III is false, since $B$ has non-zero entries below the main diagonal:

$$
{B}^{T}=[\begin{aligned}3 & 0 & 0 \\ 0 & -2 & 4 \\ 0 & 0 & 5\end{aligned}]
$$

Therefore, the correct answer is "II only".


### Generated normal variant

Consider the matrix 
$B=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & -4 & 0\end{aligned}].$
Which of the following statements are true?

- $B$ is upper triangular
- $B$ is lower triangular
- ${B}^{T}$ is lower triangular

Choices: II only; I and III only; I only; I and II only; III only

Let's analyze each statement in turn.

- Statement I is false, since $B$ has non-zero entries below the main diagonal:

$$
B=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & -4 & 0\end{aligned}]
$$

- Statement II is true. All the entries above the main diagonal of $B$ are zeros:

$$
B=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & -4 & 0\end{aligned}]
$$

- Statement III is false, since ${B}^{T}$ has non-zero entries above the main diagonal:

$$
{B}^{T}=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & -4 \\ 0 & 0 & 0\end{aligned}]
$$

Therefore, the correct answer is "II only".


## Original q-13771

Consider the matrix 
$A=[\begin{aligned}8 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 3\end{aligned}].$
Which of the following statements are true?

I. $A$ is upper triangular

II. $A$ is lower triangular

III. ${A}^{T}+A$ is lower triangular

Choices: I and II only; I, II, and III; II and III only; I and III only; I only

Let's analyze each statement in turn.

- Statement I is true, since all the entries below the main diagonal are zeros:

$$
A=[\begin{aligned}8 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 3\end{aligned}]
$$

- Statement II is true, since all the entries above the main diagonal are zeros:

$$
A=[\begin{aligned}8 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 3\end{aligned}]
$$

- Statement III is true, since the result of $A+{A}^{T}$ has all the entries above the main diagonal equal to zero: 

$$
{A}^{T}+A=[\begin{aligned}16 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 6\end{aligned}]
$$

Therefore, the correct answer is "I, II, and III".


### Generated normal variant

Consider the matrix 
$A=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & 0 & 0\end{aligned}].$
Which of the following statements are true?

I. $A$ is upper triangular

II. $A$ is lower triangular

III. ${A}^{T}+A$ is lower triangular

Choices: I and III only; I only; I, II, and III; II and III only; I and II only

Let's analyze each statement in turn.

- Statement I is true, since all the entries below the main diagonal are zeros:

$$
A=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & 0 & 0\end{aligned}]
$$

- Statement II is true, since all the entries above the main diagonal are zeros:

$$
A=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & 0 & 0\end{aligned}]
$$

- Statement III is true, since the result of $A+{A}^{T}$ has all the entries above the main diagonal equal to zero: 

$$
{A}^{T}+A=[\begin{aligned}16 & 0 & 0 \\ 0 & -16 & 0 \\ 0 & 0 & 0\end{aligned}]
$$

Therefore, the correct answer is "I, II, and III".


## Original q-42116

Consider the matrix 
$A=[\begin{aligned}7 & 0 & 0 \\ -2 & 0 & 0 \\ 0 & 1 & 1\end{aligned}].$
Which of the following statements are true?

- $A$ is lower triangular
- ${A}^{T}-A$ is lower triangular
- $A$ is upper triangular

Choices: I and II only; II only; None; I and III only; I only

Let's analyze each statement in turn.

- Statement I is true, since all the entries above the main diagonal are zeros:

$$
A=[\begin{aligned}7 & 0 & 0 \\ -2 & 0 & 0 \\ 0 & 1 & 1\end{aligned}]
$$

- Statement II is false, since the result of ${A}^{T}-A$ has non-zero entries above the main diagonal:

$$
{A}^{T}-A=[\begin{aligned}0 & -2 & 0 \\ 2 & 0 & 1 \\ 0 & -1 & 0\end{aligned}]
$$

- Statement III is false, since $A$ has non-zero entries below the main diagonal

$$
A=[\begin{aligned}7 & 0 & 0 \\ -2 & 0 & 0 \\ 0 & 1 & 1\end{aligned}]
$$

Therefore, the correct answer is "I only".


### Generated normal variant

Consider the matrix 
$A=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & -4 & 0\end{aligned}].$
Which of the following statements are true?

- $A$ is lower triangular
- ${A}^{T}-A$ is lower triangular
- $A$ is upper triangular

Choices: I and III only; I only; II only; None; I and II only

Let's analyze each statement in turn.

- Statement I is true, since all the entries above the main diagonal are zeros:

$$
A=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & -4 & 0\end{aligned}]
$$

- Statement II is false, since the result of ${A}^{T}-A$ has non-zero entries above the main diagonal:

$$
{A}^{T}-A=[\begin{aligned}0 & 0 & 0 \\ 0 & 0 & -4 \\ 0 & 4 & 0\end{aligned}]
$$

- Statement III is false, since $A$ has non-zero entries below the main diagonal

$$
A=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & -4 & 0\end{aligned}]
$$

Therefore, the correct answer is "I only".


## Original q-68754

Consider the matrix 
$A=[\begin{aligned}0 & -2 & -7 \\ 2 & -1 & 8 \\ 7 & -8 & 1\end{aligned}].$
Which of the following statements are true?

- $A$ is upper triangular
- $A$ is lower triangular
- $A+{A}^{T}$ is upper triangular

Choices: II and III only; II only; I only; III only; I and II only

Let's analyze each statement in turn.

- Statement I is false, since $A$ has non-zero entries below the main diagonal:

$$
A=[\begin{aligned}0 & -2 & -7 \\ 2 & -1 & 8 \\ 7 & -8 & 1\end{aligned}]
$$

- Statement II is false, since $A$ has non-zero entries above the main diagonal:

$$
A=[\begin{aligned}0 & -2 & -7 \\ 2 & -1 & 8 \\ 7 & -8 & 1\end{aligned}]
$$

- Statement III is true, since the result of $A+{A}^{T}$ has all the entries below the main diagonal equal to zero:

$$
A+{A}^{T}=[\begin{aligned}0 & 0 & 0 \\ 0 & -2 & 0 \\ 0 & 0 & 2\end{aligned}]
$$

Therefore, the correct answer is "III only".


### Generated normal variant

Consider the matrix 
$A=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & -4 \\ 0 & 4 & 0\end{aligned}].$
Which of the following statements are true?

- $A$ is upper triangular
- $A$ is lower triangular
- $A+{A}^{T}$ is upper triangular

Choices: III only; I and II only; II only; I only; II and III only

Let's analyze each statement in turn.

- Statement I is false, since $A$ has non-zero entries below the main diagonal:

$$
A=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & -4 \\ 0 & 4 & 0\end{aligned}]
$$

- Statement II is false, since $A$ has non-zero entries above the main diagonal:

$$
A=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & -4 \\ 0 & 4 & 0\end{aligned}]
$$

- Statement III is true, since the result of $A+{A}^{T}$ has all the entries below the main diagonal equal to zero:

$$
A+{A}^{T}=[\begin{aligned}16 & 0 & 0 \\ 0 & -16 & 0 \\ 0 & 0 & 0\end{aligned}]
$$

Therefore, the correct answer is "III only".


## Original q-74318

Consider the matrix 
$C=[\begin{aligned}2 & 0 & 1 & 0 \\ 0 & 4 & 0 & 4 \\ 0 & 0 & 2 & 1 \\ 0 & 0 & 0 & 3\end{aligned}].$
Which of the following statements are true?

- $C$ is upper triangular
- $C$ is lower triangular
- ${C}^{T}$ is upper triangular

Choices: I and II only; I and III only; III only; I only; II only

Let's analyze each statement in turn.

- Statement I is true. All the entries below the main diagonal of $C$ are zeros:

$$
C=[\begin{aligned}2 & 0 & 1 & 0 \\ 0 & 4 & 0 & 4 \\ 0 & 0 & 2 & 1 \\ 0 & 0 & 0 & 3\end{aligned}]
$$

- Statement II is false, since $C$ has non-zero entries above the main diagonal:

$$
C=[\begin{aligned}2 & 0 & 1 & 0 \\ 0 & 4 & 0 & 4 \\ 0 & 0 & 2 & 1 \\ 0 & 0 & 0 & 3\end{aligned}]
$$

- Statement III is false, since ${C}^{T}$ has non-zero entries below the main diagonal:

$$
{C}^{T}=[\begin{aligned}2 & 0 & 0 & 0 \\ 0 & 4 & 0 & 0 \\ 1 & 0 & 2 & 0 \\ 0 & 4 & 1 & 3\end{aligned}]
$$

Therefore, the correct answer is "I only".


### Generated normal variant

Consider the matrix 
$C=[\begin{aligned}8 & 0 & 0 & 0 \\ 0 & -8 & 0 & -2 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & -4\end{aligned}].$
Which of the following statements are true?

- $C$ is upper triangular
- $C$ is lower triangular
- ${C}^{T}$ is upper triangular

Choices: I only; II only; I and III only; III only; I and II only

Let's analyze each statement in turn.

- Statement I is true. All the entries below the main diagonal of $C$ are zeros:

$$
C=[\begin{aligned}8 & 0 & 0 & 0 \\ 0 & -8 & 0 & -2 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & -4\end{aligned}]
$$

- Statement II is false, since $C$ has non-zero entries above the main diagonal:

$$
C=[\begin{aligned}8 & 0 & 0 & 0 \\ 0 & -8 & 0 & -2 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & -4\end{aligned}]
$$

- Statement III is false, since ${C}^{T}$ has non-zero entries below the main diagonal:

$$
{C}^{T}=[\begin{aligned}8 & 0 & 0 & 0 \\ 0 & -8 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & -2 & 1 & -4\end{aligned}]
$$

Therefore, the correct answer is "I only".


## Original q-74319

Consider the matrix 
$D=[\begin{aligned}3 & 0 & 0 \\ 0 & 2 & 0 \\ 1 & 0 & 1\end{aligned}].$
Which of the following statements are true?

I. $D$ is upper triangular

II. $D$ is lower triangular

III. ${D}^{T}$ is upper triangular

Choices: I only; II only; III only; II and III only; I and II only

Let's analyze each statement in turn.

- Statement I is false, since $D$ has non-zero entries below the main diagonal:

$$
D=[\begin{aligned}3 & 0 & 0 \\ 0 & 2 & 0 \\ 1 & 0 & 1\end{aligned}]
$$

- Statement II is true. All the entries above the main diagonal of $D$ are zeros:

$$
D=[\begin{aligned}3 & 0 & 0 \\ 0 & 2 & 0 \\ 1 & 0 & 1\end{aligned}]
$$

- Statement III is true. All the entries below the main diagonal of ${D}^{T}$ are zeros:

$$
{D}^{T}=[\begin{aligned}3 & 0 & 1 \\ 0 & 2 & 0 \\ 0 & 0 & 1\end{aligned}]
$$

Therefore, the correct answer is "II and III only".


### Generated normal variant

Consider the matrix 
$D=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & -4 & 0\end{aligned}].$
Which of the following statements are true?

I. $D$ is upper triangular

II. $D$ is lower triangular

III. ${D}^{T}$ is upper triangular

Choices: II and III only; I and II only; II only; III only; I only

Let's analyze each statement in turn.

- Statement I is false, since $D$ has non-zero entries below the main diagonal:

$$
D=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & -4 & 0\end{aligned}]
$$

- Statement II is true. All the entries above the main diagonal of $D$ are zeros:

$$
D=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & 0 \\ 0 & -4 & 0\end{aligned}]
$$

- Statement III is true. All the entries below the main diagonal of ${D}^{T}$ are zeros:

$$
{D}^{T}=[\begin{aligned}8 & 0 & 0 \\ 0 & -8 & -4 \\ 0 & 0 & 0\end{aligned}]
$$

Therefore, the correct answer is "II and III only".


## Generated easy example

Consider the matrix 
$A=[\begin{aligned}-8 & -5 & 0 \\ 0 & 6 & 0 \\ 8 & 8 & 7\end{aligned}].$
Which of the following statements are true?

- $A$ is upper triangular
- $A$ is lower triangular
- $A$ is diagonal

Choices: I only; I and II only; II only; I, II, and III; None

Let's analyze each statement in turn.

- Statement I is false, since $A$ has non-zero entries below the main diagonal:

$$
A=[\begin{aligned}-8 & -5 & 0 \\ 0 & 6 & 0 \\ 8 & 8 & 7\end{aligned}]
$$

- Statement II is false, since $A$ has non-zero entries above the main diagonal:

$$
A=[\begin{aligned}-8 & -5 & 0 \\ 0 & 6 & 0 \\ 8 & 8 & 7\end{aligned}]
$$

- Statement III is false, since $A$ has non-zero entries off the main diagonal:

$$
A=[\begin{aligned}-8 & -5 & 0 \\ 0 & 6 & 0 \\ 8 & 8 & 7\end{aligned}]
$$

Therefore, the correct answer is "None".


## Generated easy example

Consider the matrix 
$A=[\begin{aligned}3 & -8 & -1 \\ -6 & 5 & 0 \\ 0 & -8 & -3\end{aligned}].$
Which of the following statements are true?

- $A$ is upper triangular
- $A$ is lower triangular
- $A$ is diagonal

Choices: I only; I and II only; II only; I, II, and III; None

Let's analyze each statement in turn.

- Statement I is false, since $A$ has non-zero entries below the main diagonal:

$$
A=[\begin{aligned}3 & -8 & -1 \\ -6 & 5 & 0 \\ 0 & -8 & -3\end{aligned}]
$$

- Statement II is false, since $A$ has non-zero entries above the main diagonal:

$$
A=[\begin{aligned}3 & -8 & -1 \\ -6 & 5 & 0 \\ 0 & -8 & -3\end{aligned}]
$$

- Statement III is false, since $A$ has non-zero entries off the main diagonal:

$$
A=[\begin{aligned}3 & -8 & -1 \\ -6 & 5 & 0 \\ 0 & -8 & -3\end{aligned}]
$$

Therefore, the correct answer is "None".


## Generated moderate example

Consider the matrix 
$C=[\begin{aligned}-4 & 5 & 0 & 2 \\ 0 & 7 & -3 & 7 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 6\end{aligned}].$
Which of the following statements are true?

- $C$ is upper triangular
- $C$ is lower triangular
- ${C}^{T}$ is upper triangular

Choices: I and III only; II only; I and II only; I only; III only

Let's analyze each statement in turn.

- Statement I is true. All the entries below the main diagonal of $C$ are zeros:

$$
C=[\begin{aligned}-4 & 5 & 0 & 2 \\ 0 & 7 & -3 & 7 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 6\end{aligned}]
$$

- Statement II is false, since $C$ has non-zero entries above the main diagonal:

$$
C=[\begin{aligned}-4 & 5 & 0 & 2 \\ 0 & 7 & -3 & 7 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 6\end{aligned}]
$$

- Statement III is false, since ${C}^{T}$ has non-zero entries below the main diagonal:

$$
{C}^{T}=[\begin{aligned}-4 & 0 & 0 & 0 \\ 5 & 7 & 0 & 0 \\ 0 & -3 & 1 & 0 \\ 2 & 7 & 0 & 6\end{aligned}]
$$

Therefore, the correct answer is "I only".


## Generated moderate example

Consider the matrix 
$C=[\begin{aligned}6 & 0 & 0 & -6 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -7\end{aligned}].$
Which of the following statements are true?

- $C$ is upper triangular
- $C$ is lower triangular
- ${C}^{T}$ is upper triangular

Choices: I and III only; II only; I and II only; I only; III only

Let's analyze each statement in turn.

- Statement I is true. All the entries below the main diagonal of $C$ are zeros:

$$
C=[\begin{aligned}6 & 0 & 0 & -6 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -7\end{aligned}]
$$

- Statement II is false, since $C$ has non-zero entries above the main diagonal:

$$
C=[\begin{aligned}6 & 0 & 0 & -6 \\ 0 & 1 & 0 & -2 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -7\end{aligned}]
$$

- Statement III is false, since ${C}^{T}$ has non-zero entries below the main diagonal:

$$
{C}^{T}=[\begin{aligned}6 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ -6 & -2 & 0 & -7\end{aligned}]
$$

Therefore, the correct answer is "I only".


## Generated hard example

Consider the matrix 
$B=[\begin{aligned}-4 & 0 & 0 & 5 \\ 0 & 7 & 2 & -3 \\ 0 & 0 & 1 & 7 \\ 0 & 0 & 0 & 6\end{aligned}].$
Which of the following statements are true?

- $B$ is upper triangular
- $B$ is lower triangular
- $B-{B}^{T}$ is upper triangular

Choices: I only; III only; I and II only; I and III only; II only

Let's analyze each statement in turn.

- Statement I is true, since all the entries below the main diagonal equal to zero:

$$
B=[\begin{aligned}-4 & 0 & 0 & 5 \\ 0 & 7 & 2 & -3 \\ 0 & 0 & 1 & 7 \\ 0 & 0 & 0 & 6\end{aligned}]
$$

- Statement II is false, since $B$ has non-zero entries above the main diagonal:

$$
B=[\begin{aligned}-4 & 0 & 0 & 5 \\ 0 & 7 & 2 & -3 \\ 0 & 0 & 1 & 7 \\ 0 & 0 & 0 & 6\end{aligned}]
$$

- Statement III is false, since the result of $B-{B}^{T}$ has non-zero entries below the main diagonal:

$$
B-{B}^{T}=[\begin{aligned}0 & 0 & 0 & 5 \\ 0 & 0 & 2 & -3 \\ 0 & -2 & 0 & 7 \\ -5 & 3 & -7 & 0\end{aligned}]
$$

Therefore, the correct answer is "I only".


## Generated hard example

Consider the matrix 
$B=[\begin{aligned}6 & -6 & -2 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 2 \\ 0 & 0 & 0 & -7\end{aligned}].$
Which of the following statements are true?

- $B$ is upper triangular
- $B$ is lower triangular
- $B-{B}^{T}$ is upper triangular

Choices: I only; III only; I and II only; I and III only; II only

Let's analyze each statement in turn.

- Statement I is true, since all the entries below the main diagonal equal to zero:

$$
B=[\begin{aligned}6 & -6 & -2 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 2 \\ 0 & 0 & 0 & -7\end{aligned}]
$$

- Statement II is false, since $B$ has non-zero entries above the main diagonal:

$$
B=[\begin{aligned}6 & -6 & -2 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 2 \\ 0 & 0 & 0 & -7\end{aligned}]
$$

- Statement III is false, since the result of $B-{B}^{T}$ has non-zero entries below the main diagonal:

$$
B-{B}^{T}=[\begin{aligned}0 & -6 & -2 & 0 \\ 6 & 0 & 0 & 0 \\ 2 & 0 & 0 & 2 \\ 0 & 0 & -2 & 0\end{aligned}]
$$

Therefore, the correct answer is "I only".
