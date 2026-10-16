
# Zero, Square, Diagonal and Identity Matrices

## Tutorial 17592186088890 Introduction
Some important types of matrices have special names.

- An $m \times n$ matrix in which all entries are zeros is called a **zero matrix**. For example, the following matrices are both zero matrices:

<div class="matrix-operands matrix-operands-stacked">
<div>$\begin{bmatrix}0 & 0 \\ 0 & 0 \\ 0 & 0\end{bmatrix}$</div>
<div>$\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}$</div>
</div>

We use the notation $O_{m \times n}$ to represent the zero-matrix with $m$ rows and $n$ columns. So, the zero matrices shown above are $O_{3 \times 2}$ and $O_{2 \times 2},$ respectively.

- A $n \times n$ matrix (meaning the number of rows equals the number of columns) is called a **square matrix**. For example, the following matrices are square matrices of dimensions $2\times 2$ and $3\times 3,$ respectively:

<div class="matrix-operands matrix-operands-stacked">
<div>$\begin{bmatrix}a & b \\ c & d\end{bmatrix}$</div>
<div>$\begin{bmatrix}-1 & \pi & -2 \\ 0 & 0 & \pi \\ 2 & -1 & 4\end{bmatrix}$</div>
</div>

## Tutorial 17592186088892 Diagonal, Identity, and Other Matrices
There are some special types of square matrices.

- A square matrix is called **diagonal**, if all entries that do not lie on the main diagonal (from top-left to bottom-right) are zeros. For example, the following matrices are all diagonal matrices:

$$
\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix}
$$

Note that we can have any number (including $0$) on the diagonal.

- An **identity matrix** is a diagonal matrix where the entries on the diagonal are all $1$'s (and all other entries are $0$'s). For example, the following matrices are all identity matrices:

$$
\begin{bmatrix}\,1\,\end{bmatrix}
$$

We use the notation $I_n$ for the $n \times n$ identity matrix.

Finally, as we've seen before:

- If a matrix has only one row, then it's called a **row vector**. An example of a row vector is shown below.

$$
\begin{bmatrix}-3 & 0 & 1\end{bmatrix}
$$

- If a matrix has only one column, then it's called a **column vector**. An example of a column vector is shown below.

$$
\begin{bmatrix}1 \\ 5 \\ -2\end{bmatrix}
$$

## Identifying a Zero Matrix

### 17592186087502 e-4390
Which of the following are zero matrices?

$$
\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix}
$$

Solution: - $P$ is a zero matrix since *all* its entries are zeros.

- $Q$ is *not* a zero matrix since some of its entries are not zeros (for instance, $q_{12}=0.1\neq0$).

- $R$ is a zero matrix since *all* its entries are zeros.

Therefore, only $P$ and $R$ are zero matrices.


### 17592186087983 q-11553
Which of the following are zero matrices?
$H = \begin{bmatrix}0 & 0 \\ 0 & 0 \\ 0 & 0\end{bmatrix}, G = \begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}, K = \begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}$

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186088357 q-7827
Which of the following are zero matrices?
$A = \begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}, B = \begin{bmatrix}0 & 0 \\ 0 & 1\end{bmatrix}, C = \begin{bmatrix}10 & 0\end{bmatrix}$

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186262598 q-126201
Which of the following are zero matrices?

$$
H=\begin{bmatrix}0 & 0 \\ 0 & 0 \\ 0 & 0\end{bmatrix},\,I=\begin{bmatrix}0 & 0 \\ 0.1 & 0.1 \\ 0 & 0\end{bmatrix},\,G=\begin{bmatrix}0\end{bmatrix}
$$

Select all that apply.

Solution: - $H$ is a zero matrix since *all* its entries are zeros.

- $I$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${i}_{12}=0.1\ne 0$).

- $G$ is a zero matrix since *all* its entries are zeros.

Therefore, only $H$ and $G$ are zero matrices.

G {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186463569} 
H {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186463571} 
I {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186463572} 

### 17592186262599 q-126204
Which of the following are zero matrices?

$$
R=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,S=\begin{bmatrix}0 & 0 \\ 0 & 0\end{bmatrix},\,T=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

Solution: - $R$ is a zero matrix since *all* its entries are zeros.

- $S$ is a zero matrix since *all* its entries are zeros.

- $T$ is a zero matrix since *all* its entries are zeros.

Therefore, $R$, $S$, and $T$ are zero matrices.

R {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186463575} 
S {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186463577} 
T {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186463579} 

### 17592186335966 q-68729
Which of the following are zero matrices?

$$
T=\begin{bmatrix}0 & 1 \\ 0 & 0\end{bmatrix},\,U=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 1 & 0\end{bmatrix},\,V=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

Solution: - $T$ is *not* a zero matrix since one of its entries is not zero (${t}_{12}=1\ne 0$).

- $U$ is *not* a zero matrix since one of its entries is not zero (${u}_{32}=1\ne 0$).

- $V$ is a zero matrix since *all* its entries are zeros.

Therefore, only $V$ is a zero matrix.

T {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186467764} 
U {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186467766} 
V {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186467769} 

### 17592186403286 q-68725
Which of the following are zero matrices?

$$
P=\begin{bmatrix}0 & 1 \\ 1 & 0 \\ 0 & 1\end{bmatrix},\,Q=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix},\,R=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

Solution: - $P$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${p}_{21}=1\ne 0$).

- $Q$ is a zero matrix since *all* its entries are zeros.

- $R$ is a zero matrix since *all* its entries are zeros.

Therefore, only $Q$ and $R$ are zero matrices.

P {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186473218} 
Q {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186473221} 
R {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186473223} 

### 17592186403293 q-68727
Which of the following are zero matrices?

<div class="matrix-operands matrix-operands-stacked">
<div>$W=\begin{bmatrix}0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 1 & 0 & 0 & 0\end{bmatrix}$</div>
<div>$X=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}$</div>
<div>$Y=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 1 \\ 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 3 & 0 & 0 & 0\end{bmatrix}$</div>
</div>

Select all that apply.

Solution: - $W$ is not a zero matrix since some of its entries are not zeros (for instance, ${w}_{22}=1\ne 0$).

- $X$ is a zero matrix since *all* its entries are zeros.

- $Y$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${y}_{33}=3\ne 0$).

Therefore, only $X$ is a zero matrix.

W {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186473224} 
X {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186473227} 
Y {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186473228} 

### 17592186509668 authored
Which of the following are zero matrices?

$$
A=\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix},\,B=\begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 3 & 0 & 3 & 0 & 0\end{bmatrix},\,C=\begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

Solution: - $A$ is a zero matrix since *all* its entries are zeros.

- $B$ is *not* a zero matrix since some of its entries are not zeros (for instance, ${b}_{43}=3\ne 0$).

- $C$ is a zero matrix since *all* its entries are zeros.

Therefore, only $A$ and $C$ are zero matrices.

B {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186509671} 
C {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186509667} 
A {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186509673} 

## Identifying a Square Matrix

### 17592186087503 e-4391
Which of the following are square matrices?

<div class="matrix-operands matrix-operands-stacked">
<div>$U=\begin{bmatrix}1 & 0 & 1 \\ 2 & 3 & 1\end{bmatrix}$</div>
<div>$W=\begin{bmatrix}1 & -1 & 0 \\ 1 & 0 & -4 \\ 5 & 0 & 1\end{bmatrix}$</div>
<div>$Z=\begin{bmatrix}\sqrt{3} & 0 \\ 1 & -\sqrt{2}\end{bmatrix}$</div>
</div>

Solution: - $U$ is *not* a square matrix since the numbers of rows and columns are not the same. It has $2$ rows and $3$ columns, so it's a $2 \times 3$ matrix.

- $W$ is a square matrix since it has the same number of rows and columns. It has $3$ rows and $3$ columns, so it is a $3 \times 3$ matrix.

- $Z$ is a square matrix since it has the same number of rows and columns. It has $2$ rows and $2$ columns, so it is a $2 \times 2$ matrix.

Therefore, $W$ and $Z$ are square matrices.


### 17592186087984 q-11557
Which of the following are square matrices?

$$
C=\begin{bmatrix}0 & -2 & 0 \\ -10 & 0 & 0 \\ 0 & 0 & 0.5\end{bmatrix},\,D=\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix},\,E=\begin{bmatrix}-\sqrt{2} & \sqrt{3} \\ \sqrt{3} & -\sqrt{2}\end{bmatrix}\,
$$

Select all that apply.

Solution: - $C$ is a square matrix since it has the same number of rows and columns. It has $3$ rows and $3$ columns, so it is a $3\times 3$ matrix.

- $D$ is a square matrix since it has the same number of rows and columns. It has $4$ rows and $4$ columns, so it is a $4\times 4$ matrix.

- $E$ is a square matrix since it has the same number of rows and columns. It has $2$ rows and $2$ columns, so it is a $2\times 2$ matrix.

Therefore, $C$, $D$, and $E$ are square matrices.

C {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186459408} 
D {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186459410} 
E {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186459412} 

### 17592186088356 q-7826
Which of the following are square matrices?
$A = \begin{bmatrix}0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0\end{bmatrix}, B = \begin{bmatrix}1 & 0 \\ 1 & 0 \\ 1 & 0\end{bmatrix}, C = \begin{bmatrix}0 & 0 & 0\end{bmatrix}$

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186250432 q-11556
Which of the following are square matrices?

$$
P=\begin{bmatrix}0 & 0 \\ -10 & 0.5 \\ -2 & 0\end{bmatrix},\,S=\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix},\,T=\begin{bmatrix}1.5 & -3 & 0 & 1 & 9 \\ 0 & 0.2 & 1 & 0 & 0 \\ 0 & \sqrt{3} & 0 & 0 & 1 \\ -2 & 0 & 0 & 6 & 0 \\ 2 & 1 & 0 & 5 & 8\end{bmatrix}\,
$$

Select all that apply.

Solution: - $P$ is *not* a square matrix since the numbers of rows and columns are not the same. It has $3$ rows and $2$ columns, so it's a $3\times 2$ matrix.

- $S$ is a square matrix since it has the same number of rows and columns. It has $2$ rows and $2$ columns, so it is a $2\times 2$ matrix.

- $T$ is a square matrix since it has the same number of rows and columns. It has $5$ rows and $5$ columns, so it is a $5\times 5$ matrix.

Therefore, only $S$ and $T$ are square matrices.

P {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186461737} 
S {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186461740} 
T {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186461742} 

### 17592186262600 q-126275
Which of the following are square matrices?

$$
K=\begin{bmatrix}3 & 1 \\ 0 & \sqrt{2}\end{bmatrix},\,L=\begin{bmatrix}1 & 0\end{bmatrix},\,M=\begin{bmatrix}-1 & 3 & -3 \\ 0 & 0 & 0 \\ -2 & 5 & -1 \\ 0 & 0 & 0\end{bmatrix}
$$

Select all that apply. If none apply, leave all boxes unchecked.

Solution: - $K$ is a square matrix since it has the same number of rows and columns. It has $2$ rows and $2$ columns, so it is a $2\times 2$ matrix.

- $L$ is *not* a square matrix since the numbers of rows and columns are not the same. It has $1$ rows and $2$ columns, so it's a $1\times 2$ matrix.

- $M$ is *not* a square matrix since the numbers of rows and columns are not the same. It has $4$ rows and $3$ columns, so it's a $4\times 3$ matrix.

Therefore, only $K$ is a square matrix.

K {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186463581} 
L {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186463582} 
M {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186463584} 

### 17592186396162 q-7835
Which of the following are square matrices?

$$
K=\begin{bmatrix}3 & 1 & 1 \\ 0 & 0 & 0\end{bmatrix},\,L=\begin{bmatrix}1 & 0 \\ 0 & -1\end{bmatrix},\,M=\begin{bmatrix}2 & 3 & 0 & 1 \\ 0 & 0 & 0 & 0 \\ 7 & 1 & 1 & 4 \\ 0 & 0 & 0 & 8\end{bmatrix}
$$

Select all that apply.

Solution: - $K$ is *not* a square matrix since the numbers of rows and columns are not the same. It has $2$ rows and $3$ columns, so it's a $2\times 3$ matrix.

- $L$ is a square matrix since it has the same number of rows and columns. It has $2$ rows and $2$ columns, so it is a $2\times 2$ matrix.

- $M$ is a square matrix since it has the same number of rows and columns. It has $4$ rows and $4$ columns, so it is a $4\times 4$ matrix.

Therefore, only $L$ and $M$ are square matrices.

K {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186471549} 
L {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186471552} 
M {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186471554} 

### 17592186400212 q-126278
Which of the following are square matrices?

$$
A=\begin{bmatrix}-1\end{bmatrix},\,B=\begin{bmatrix}1 & 1 & 1 \\ 2 & 4 & 2 \\ -2 & 2 & 1\end{bmatrix},\,C=\begin{bmatrix}2 & 1\end{bmatrix}
$$

Select all that apply. If none apply, leave all boxes unchecked.

Solution: - $A$ is a square matrix since it has the same number of rows and columns. It has $1$ row and $1$ column, so it is a $1\times 1$ matrix.

- $B$ is a square matrix since it has the same number of rows and columns. It has $3$ rows and $3$ columns, so it is a $3\times 3$ matrix.

- $C$ is *not* a square matrix since the numbers of rows and columns are not the same. It has $1$ row and $2$ columns, so it's a $1\times 2$ matrix.

Therefore, only $A$ and $B$ are square matrices.

A {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186472557} 
B {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186472559} 
C {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186472560} 

## Identifying a Special Square Matrix

### 17592186087504 e-4392
Which of the following are diagonal matrices?

$$
\begin{bmatrix}3 & 0 \\ 0 & 3\end{bmatrix}
$$

Solution: - $Q$ is a diagonal matrix. It's a square matrix since it has the same number of rows and columns. Also, all the entries that do not lie on the main diagonal are zeros.

Notice that $Q$ is not an identity matrix since the diagonal entries are not all ones.

- $R$ is *not* a diagonal matrix. It's a square matrix since it has the same number of rows and columns. But some of the entries that do not lie on the main diagonal are not zeros (for instance, $r_{13}=1 \neq 0$).

- $S$ is a diagonal matrix. It's a square matrix since it has the same number of rows and columns. Also, all the entries that do not lie on the main diagonal are zeros.

Notice that $S$ is not an identity matrix since the diagonal entries are not all ones.

Therefore, only $Q$ and $S$ are diagonal matrices.


### 17592186087985 q-11562
Which of the following are diagonal matrices?

$$
H=\begin{bmatrix}0 & 1 \\ 0 & 0\end{bmatrix},\,J=\begin{bmatrix}5 & 0 & 0 \\ 0 & 5 & 0 \\ 0 & 0 & 5\end{bmatrix},\,L=\begin{bmatrix}3 & 0 & 0 & 1 \\ 0 & 3 & 0 & 0 \\ 0 & 0 & 3 & 0 \\ 1 & 0 & 0 & 3\end{bmatrix}
$$

Select all that apply.

Solution: - $H$ is *not* a diagonal matrix. It's a square matrix since it has the same number of rows and columns. But some of the entries that do not lie on the main diagonal are not zeros (for instance, ${h}_{12}=1\ne 0$).

- $J$ is a diagonal matrix. It's a square matrix since it has the same number of rows and columns. Also, all the entries that do not lie on the main diagonal are zeros.

Notice that $J$ is not an identity matrix since the diagonal entries are not all ones.

- $L$ is *not* a diagonal matrix. It's a square matrix since it has the same number of rows and columns. But some of the entries that do not lie on the main diagonal are not zeros (for instance, ${l}_{14}=1\ne 0$).

Therefore, only $J$ is a diagonal matrix.

H {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186459413} 
J {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186459416} 
L {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186459417} 

### 17592186088358 q-7829
Which of the following are identity matrices?
$B = \begin{bmatrix}0 & 0 \\ 0 & 1\end{bmatrix}, C = \begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0\end{bmatrix}, D = \begin{bmatrix}1 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 1\end{bmatrix}$

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186335967 q-68741
Which of the following are identity matrices?

$$
M=\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1\end{bmatrix},\,N=\begin{bmatrix}1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1\end{bmatrix},\,P=\begin{bmatrix}1 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 1\end{bmatrix}
$$

Select all that apply.

Solution: - $M$ is an identity matrix. First, it's a square matrix since it has the same number of rows and columns. Also, its entries on the main diagonal are all ones, and the rest of the entries are zeros.

- $N$ is *not* an identity matrix since it's not a square matrix.

- $P$ is *not* an identity matrix. Although it's a diagonal matrix, its diagonal entries are not all ones.

Therefore, only $M$ is an identity matrix.

M {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186467771} 
N {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186467772} 
P {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186467774} 

### 17592186335968 q-68744
Which of the following are diagonal matrices?

$$
F=\begin{bmatrix}4 & 0 & 1 & 0 \\ 0 & 3 & 0 & 0 \\ 0 & 0 & 4 & 0 \\ 0 & 2 & 0 & 3\end{bmatrix},\,H=\begin{bmatrix}0 & 0 \\ 0 & 1\end{bmatrix},\,M=\begin{bmatrix}2 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 3\end{bmatrix}
$$

Select all that apply.

Solution: - $F$ is *not* a diagonal matrix. It's a square matrix since it has the same number of rows and columns. But some of the entries that do not lie on the main diagonal are not zeros (for instance, ${f}_{13}=1\ne 0$).

- $H$ is a diagonal matrix.  It's a square matrix since it has the same number of rows and columns. Also, all the entries that do not lie on the main diagonal are zeros.

Notice that $H$ is not an identity matrix since the diagonal entries are not all ones.

- $M$ is a diagonal matrix. It's a square matrix since it has the same number of rows and columns. Also, all the entries that do not lie on the main diagonal are zeros.

Notice that $M$ is not an identity matrix since the diagonal entries are not all ones.

Therefore, only $H$ and $M$ are diagonal matrices.

F {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186467776} 
H {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186467779} 
M {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186467781} 

### 17592186400205 q-126222
Which of the following are diagonal matrices?

$$
P=\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0\text{ }\end{bmatrix},\,Q=\begin{bmatrix}1 & 2 \\ 1 & 2 \\ 1 & 2 \\ 2 & 1\end{bmatrix},\,R=\begin{bmatrix}1 & 0 & 5 \\ 0 & -2 & 0 \\ 7 & 0 & -3\end{bmatrix}
$$

Select all that apply.

Solution: - $P$ is *not* a diagonal matrix since it's not a square matrix.

- $Q$ is *not* a diagonal matrix since it's not a square matrix.

- $R$ is *not* a diagonal matrix. It's a square matrix since it has the same number of rows and columns. But some of the entries that do not lie on the main diagonal are not zeros (for instance, ${r}_{31}=7\ne 0$).

Therefore, none of the given are diagonal matrices.

P {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186472550} 
Q {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186472552} 
R {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186472554} 

### 17592186403300 q-68745
Which of the following are diagonal matrices?

$$
S=\begin{bmatrix}4 & 0 & 0 & 0 \\ 0 & 3 & 0 & 0 \\ 0 & 0 & 4 & 0 \\ 0 & 0 & 0 & 3\end{bmatrix},\,R=\begin{bmatrix}1 & 0 \\ 0 & 1 \\ 1 & 0 \\ 0 & 1\end{bmatrix},\,Y=\begin{bmatrix}2 & 0 & -1 \\ 0 & 2 & 0 \\ 1 & 0 & 3\end{bmatrix}
$$

Select all that apply.

Solution: - $S$ is a diagonal matrix. It's a square matrix since it has the same number of rows and columns. Also, all the entries that do not lie on the main diagonal are zeros.

Notice that $S$ is not an identity matrix since the diagonal entries are not all ones.

- $R$ is *not* a diagonal matrix since it's not a square matrix.

- $Y$ is *not* a diagonal matrix. It's a square matrix since it has the same number of rows and columns. But some of the entries that do not lie on the main diagonal are not zeros (for instance, ${y}_{31}=1\ne 0$).

Therefore, only $S$ is a diagonal matrix.

R {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186473230} 
S {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186473233} 
Y {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186473234} 

## Identifying Other Matrices

### 17592186087505 e-4393
How can we best describe the following matrix?
 

$$
\begin{bmatrix}5 \\ -9 \\ 2\end{bmatrix}
$$

Solution: Notice that $F$ is a matrix that has a single column. Therefore, it is a column vector.


### 17592186088360 q-7831
Which of the following are row vectors?
$E = \begin{bmatrix}-1 \\ 0 \\ 0 \\ -3 \\ \sqrt{2}\end{bmatrix}, F = \begin{bmatrix}2 & 5 & 6 & -2 & 0\end{bmatrix}, G = \begin{bmatrix}2 & 5 \\ 2 & 5\end{bmatrix}$

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186088361 q-7836
Which of the following best describes the following matrix $M$?
$M = \begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 1\end{bmatrix}$

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186250441 q-11563
Which of the following best describes the following matrix $A?$

$$
A=\begin{bmatrix}1 & 2 & 3\end{bmatrix}
$$

Solution: The matrix has only one row. Hence, it is a row vector.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'A row vector', ':db/id': 17592186247735} 

### 17592186262601 q-126293
Which of the following best describes the following matrix $P?$

$$
P=\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & -1 & 0 \\ 0 & 0 & 0 & -1\end{bmatrix}
$$

Solution: The matrix is square, all the entries that do not lie on the main diagonal are zeros, and the diagonal entries are not all ones. 

Hence it's a diagonal matrix.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'A diagonal matrix', ':db/id': 17592186260289} 

### 17592186335969 q-68751
Which of the following are row vectors?

$$
A=\begin{bmatrix}0 & 1 & 3 & -2 & 9 \\ 1 & 2 & 0 & 4 & 1\end{bmatrix},\,B=\begin{bmatrix}3 \\ -2 \\ 0 \\ 6\end{bmatrix},\,C=\begin{bmatrix}3 & 10\end{bmatrix}
$$

Select all that apply.

Solution: - $A$ is *not* a row vector, since it has more than $1$ row (it has $2$ rows).

- $B$ is *not* a row vector. It has only one column (and $4$ rows), so it's a column vector.

- $C$ is a row vector since it has only one row.

Therefore, only $C$ is a row vector.

A {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186467782} 
B {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186467784} 
C {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186467787} 

### 17592186396155 q-7830
Which of the following best describes the following matrix $E?$

$$
E=\begin{bmatrix}1 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0\end{bmatrix}
$$

Solution: The matrix has no special name.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'Other', ':db/id': 17592186396158} 

### 17592186400219 q-126287
Which of the following are column vectors?

$$
A=\begin{bmatrix}-2 & 0\end{bmatrix},\,B=\begin{bmatrix}2 \\ 0 \\ 0\end{bmatrix},\,C=\begin{bmatrix}1 & -3 \\ -2 & 1\end{bmatrix}
$$

Select all that apply. If none apply, leave all boxes unchecked.

Solution: - $A$ is *not* a column vector. It has only one row (and $2$ columns), so it's a row vector.

- $B$ is a column vector since it has only one column.

- $C$ is *not* a column vector, since it has more than $1$ column (it has $2$ columns).

Therefore, only $B$ is a column vector.

A {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186472562} 
B {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'true', ':db/id': 17592186472565} 
C {':db/ident': ':answer-field.type/checkbox'} => {':answer/type': {':db/ident': ':answer.type/text'}, ':answer/value': 'false', ':db/id': 17592186472566} 

# The Transpose of a Matrix

## Tutorial 17592186060928 Introduction
To take the **transpose of a matrix**, we interchange each of its columns with the corresponding row. That is, row $1$ becomes column $1,$ row $2$ becomes column $2,$ and so on. A superscript ${}^{T}$ is used to denote the transpose operation.

For example, the transpose of the $2 \times 3$ matrix ${X}$ is the following $3 \times 2$ matrix $X^T\mathbin{:}$

$$
{X} = 
    		\left\lbrack
    		\begin{matrix}
        		{\color{red}7} & {\color{red}2} & {\color{red}-4}  \\
        		{\color{blue}-3} & {\color{blue}1} & {\color{blue}0}
    		\end{matrix}
    		\right\rbrack

        \qquad\implies\qquad

	{X}^T = 
    		\left\lbrack
    		\begin{matrix}
        		{\color{red}7} & {\color{blue}-3}  \\
        		{\color{red}2} & {\color{blue}1}  \\
        		{\color{red}-4} & {\color{blue}0}
    		\end{matrix}
    		\right\rbrack
$$

The first row of $X$ becomes the first column of $X^T,$ and the second row of $X$ becomes the second column of $X^T.$

Note that transposing a matrix swaps its dimensions. In general, we have the following property:

> *When a matrix is transposed, its dimensions switch from $m \times n$ to $n \times m.$*

Also, notice that the transpose of a column vector is a row vector:

$$
{A} = 
    		\left\lbrack
    		\begin{matrix}
        		5  \\
        		4  \\
                        2 
    		\end{matrix}
    		\right\rbrack

       \qquad \implies\qquad

	{A}^T = 
    		\left\lbrack
    		\begin{matrix}
        		5 & 4 & 2
    		\end{matrix}
    		\right\rbrack
$$

Similarly, the transpose of a row vector is a column vector:

$$
{B} = 
    		\left\lbrack
    		\begin{matrix}
        		8 & -10 & 0 & 6
    		\end{matrix}
    		\right\rbrack

        \qquad\implies\qquad

	{B}^T = 
    		\left\lbrack
    		\begin{matrix}
        		8  \\
                        -10  \\
                        0  \\
                        6
    		\end{matrix}
    		\right\rbrack
$$

## Tutorial 17592186060929 Properties of the Transpose of a Matrix
Remember that transposing a matrix swaps the rows and columns. So, if $B=A^T,$ then $b_{ij}=a_{ji}$ for all values of $i$ and $j.$ 

Geometrically, when a matrix is transposed, the diagonal elements (those with $i=j$) remain the same while all other elements are reflected across the diagonal.  For example,

$$
{A} = 
    		\left\lbrack
    		\begin{matrix}
        		\color{red}{3} & \color{blue}{7}  \\
        		1 & \color{red}{6}
    		\end{matrix}
    		\right\rbrack

      \qquad  \implies\qquad

	{A}^T = 
    		\left\lbrack
    		\begin{matrix}
        		\color{red}{3} & 1  \\
        		\color{blue}{7} & \color{red}{6} 
    		\end{matrix}
    		\right\rbrack.
$$

Also,  transposing a matrix twice results in the original matrix. More precisely, for any matrix $A,$ we have

$$
\left( A^T\right)^T = A.
$$

This happens because, in the first transpose, we swap the rows of $A$ for the columns, and then in the second transpose, we swap them back again. For example,

$$
{A} = 
    		\left\lbrack
    		\begin{matrix}
        		\color{red}{3} & \color{blue}{7}  \\
        		1 & \color{red}{6}
    		\end{matrix}
    		\right\rbrack

      \quad  \implies\quad

	{A}^T = 
    		\left\lbrack
    		\begin{matrix}
        		\color{red}{3} & 1  \\
        		\color{blue}{7} & \color{red}{6} 
    		\end{matrix}
    		\right\rbrack

      \quad  \implies\quad

	\left( {A}^T\right)^T = 
    		\left\lbrack
    		\begin{matrix}
        		\color{red}{3} & \color{blue}{7}  \\
        		1 & \color{red}{6} 
    		\end{matrix}
    		\right\rbrack =A.
$$

Finally, for any numbers $c_1,c_2$ and any $m \times n$ matrices $A,B$ we have the following rule:

$$
(c_1 A \pm c_2 B)^T = c_1 A^T \pm c_2 B^T
$$

## Finding the Transpose of a Matrix

### 17592186059552 e-4386
Find $C^T,$ if 
![](images/d5/d5e344ac147321b0440d313274626b1a00527214467cbc85bac199c10fee00bd.png)

Solution: To find the transpose, we interchange the rows and columns:
![](images/d6/d64f16633ed91692b0cd22daa4c739a6e4347ec6c0596c992d28088880ea2862.png)


### 17592186059967 q-1046
If
    $Y=\begin{bmatrix}-2 & 9 & 7 \\ 1 & 6 & 0 \\ -8 & 2 & 1\end{bmatrix},$
then ${Y}^{T}=$

Solution: To find the transpose, we interchange the rows and columns:

$$
{Y}^{T}=\begin{bmatrix}-2 & 1 & -8 \\ 9 & 6 & 2 \\ 7 & 0 & 1\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => None 
selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}-2 & 1 & -8 \\\\ 9 & 6 & 2 \\\\ 7 & 0 & 1\\end{bmatrix}', ':db/id': 17592186386111} 

### 17592186059993 q-11438
Find $A^{T}$, given that
$A = \begin{bmatrix}5 & 4 \\ 3 & 2\end{bmatrix}$.

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186240846 q-1043
Find ${Y}^{T}$, given that 
    $Y=\begin{bmatrix}-20 & 0 & 15 \\ 9 & 6 & 0.5\end{bmatrix}.$

Solution: To find the transpose, we interchange the rows and columns:

$$
{Y}^{T}=\begin{bmatrix}-20 & 9 \\ 0 & 6 \\ 15 & 0.5\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}-20 & 9 \\\\ 0 & 6 \\\\ 15 & 0.5\\end{bmatrix}', ':db/id': 17592186238949} 

### 17592186262587 q-126126
Find ${G}^{T}$, given that 
    $G=\begin{bmatrix}-2 & -1 \\ 3 & 1 \\ 0 & 2\end{bmatrix}.$

Solution: To find the transpose, we interchange the rows and columns:

$$
{G}^{T}=\begin{bmatrix}-2 & 3 & 0 \\ -1 & 1 & 2\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}-2 & 3 & 0 \\\\ -1 & 1 & 2\\end{bmatrix}', ':db/id': 17592186260955} 

### 17592186262588 q-126128
Find ${Q}^{T}$, given that 
    $Q=\begin{bmatrix}0 & 2 \\ -1 & 5 \\ 0 & 7\end{bmatrix}.$

Solution: To find the transpose, we interchange the rows and columns:

$$
{Q}^{T}=\begin{bmatrix}0 & -1 & 0 \\ 2 & 5 & 7\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}0 & -1 & 0 \\\\ 2 & 5 & 7\\end{bmatrix}', ':db/id': 17592186261092} 

### 17592186262589 q-126129
If
    $H=\begin{bmatrix}-2 & 0 & 1 \\ 0 & -1 & 0 \\ 1 & 0 & 0\end{bmatrix}$,
then ${H}^{T}=$

Solution: To find the transpose, we interchange the rows and columns:

$$
{H}^{T}=\begin{bmatrix}-2 & 0 & 1 \\ 0 & -1 & 0 \\ 1 & 0 & 0\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}-2 & 0 & 1 \\\\ 0 & -1 & 0 \\\\ 1 & 0 & 0\\end{bmatrix}', ':db/id': 17592186261027} 

### 17592186262590 q-126130
If
    $B=\begin{bmatrix}3 & 1 \\ 2 & -4\end{bmatrix}$,
then ${B}^{T}=$

Solution: To find the transpose, we interchange the rows and columns:

$$
{B}^{T}=\begin{bmatrix}3 & 2 \\ 1 & -4\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}3 & 2 \\\\ 1 & -4\\end{bmatrix}', ':db/id': 17592186261213} 

### 17592186295249 q-282739
If
    $C=\begin{bmatrix}6 & -1 & 0 \\ 4 & 3 & 8\end{bmatrix}$,
then find the transpose of $C.$

|  |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
| ${C}^{T}=\,\,$ |  | {{field-3}} | {{field-4}} |  |
|  |  | {{field-5}} | {{field-6}} |  |

Solution: To find the transpose, we interchange the rows and columns:

$$
{C}^{T}=\begin{bmatrix}6 & 4 \\ -1 & 3 \\ 0 & 8\end{bmatrix}
$$

field-6 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '8', ':db/id': 17592186293696} 
field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-1', ':db/id': 17592186293177} 
field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '3', ':db/id': 17592186293587} 
field-5 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '0', ':db/id': 17592186293003} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '6', ':db/id': 17592186293768} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '4', ':db/id': 17592186293675} 

### 17592186295250 q-282740
If
    $E=\begin{bmatrix}1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9\end{bmatrix}$,
then find the transpose of $E.$

|  |  | {{field-1}} | {{field-2}} | {{field-3}} |  |
| --- | --- | --- | --- | --- | --- |
| ${E}^{T}=\,\,$ |  | {{field-4}} | {{field-5}} | {{field-6}} |  |
|  |  | {{field-7}} | {{field-8}} | {{field-9}} |  |

Solution: To find the transpose, we interchange the rows and columns:

$$
{E}^{T}=\begin{bmatrix}1 & 4 & 7 \\ 2 & 5 & 8 \\ 3 & 6 & 9\end{bmatrix}
$$

field-8 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '6', ':db/id': 17592186293055} 
field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '7', ':db/id': 17592186293735} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '4', ':db/id': 17592186293427} 
field-9 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '9', ':db/id': 17592186292941} 
field-7 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '3', ':db/id': 17592186293223} 
field-5 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '5', ':db/id': 17592186293244} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '1', ':db/id': 17592186293598} 
field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '2', ':db/id': 17592186293908} 
field-6 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '8', ':db/id': 17592186293069} 

### 17592186295251 q-282742
If
    $G=\begin{bmatrix}9 & 3 & 1 \\ 0 & 6 & -2 \\ 4 & 7 & 5\end{bmatrix}$,
then find the transpose of $G.$

|  |  | {{field-1}} | {{field-2}} | {{field-3}} |  |
| --- | --- | --- | --- | --- | --- |
| ${G}^{T}=\,\,$ |  | {{field-4}} | {{field-5}} | {{field-6}} |  |
|  |  | {{field-7}} | {{field-8}} | {{field-9}} |  |

Solution: To find the transpose, we interchange the rows and columns:

$$
{G}^{T}=\begin{bmatrix}9 & 0 & 4 \\ 3 & 6 & 7 \\ 1 & -2 & 5\end{bmatrix}
$$

field-8 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-2', ':db/id': 17592186293893} 
field-7 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '1', ':db/id': 17592186293119} 
field-5 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '6', ':db/id': 17592186293719} 
field-9 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '5', ':db/id': 17592186293623} 
field-6 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '7', ':db/id': 17592186293741} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '9', ':db/id': 17592186293135} 
field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '3', ':db/id': 17592186293532} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '0', ':db/id': 17592186292996} 
field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '4', ':db/id': 17592186293085} 

### 17592186295252 q-282744
If
    $P=\begin{bmatrix}2 & 7 \\ -1 & 0\end{bmatrix}$,
then find the transpose of $P.$

  

| ${P}^{T}=$ |  | {{field-1}} | {{field-2}} |
| --- | --- | --- | --- |
|  | {{field-3}} | {{field-4}} |  |

Solution: To find the transpose, we interchange the rows and columns:

$$
{P}^{T}=\begin{bmatrix}2 & -1 \\ 7 & 0\end{bmatrix}
$$

field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '7', ':db/id': 17592186293360} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-1', ':db/id': 17592186293501} 
field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '0', ':db/id': 17592186293413} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '2', ':db/id': 17592186293506} 

### 17592186295253 q-282747
If
    $S=\begin{bmatrix}2 & 7 \\ -1 & 0 \\ 4 & 5\end{bmatrix}$,
then find the transpose of $S.$

  

| ${S}^{T}=$ |  | {{field-1}} | {{field-2}} | {{field-3}} |
| --- | --- | --- | --- | --- |
|  | {{field-4}} | {{field-5}} | {{field-6}} |  |

Solution: To find the transpose, we interchange the rows and columns:

$$
{S}^{T}=\begin{bmatrix}2 & -1 & 4 \\ 7 & 0 & 5\end{bmatrix}
$$

field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-1', ':db/id': 17592186293861} 
field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '4', ':db/id': 17592186293473} 
field-6 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '5', ':db/id': 17592186293500} 
field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '7', ':db/id': 17592186293184} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '2', ':db/id': 17592186293297} 
field-5 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '0', ':db/id': 17592186292952} 

### 17592186295254 q-282748
If
    $T=\begin{bmatrix}6 & -2 \\ 0 & 3 \\ -5 & 4\end{bmatrix}$,
then find the transpose of $T.$

  

| ${T}^{T}=$ |  | {{field-1}} | {{field-2}} | {{field-3}} |
| --- | --- | --- | --- | --- |
|  | {{field-4}} | {{field-5}} | {{field-6}} |  |

Solution: To find the transpose, we interchange the rows and columns:

$$
{T}^{T}=\begin{bmatrix}6 & 0 & -5 \\ -2 & 3 & 4\end{bmatrix}
$$

field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '0', ':db/id': 17592186293910} 
field-6 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '4', ':db/id': 17592186292971} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '6', ':db/id': 17592186292993} 
field-5 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '3', ':db/id': 17592186292946} 
field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-5', ':db/id': 17592186293584} 
field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-2', ':db/id': 17592186293583} 

### 17592186386113 q-1047
If
    $A=\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}$,
then ${A}^{T}=$

Solution: To find the transpose, we interchange the rows and columns:

$$
{A}^{T}=\begin{bmatrix}1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}1 & 0 & 0 \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 1\\end{bmatrix}', ':db/id': 17592186386119} 

### 17592186386743 q-11463
If
    $D=\begin{bmatrix}3 & 1 & 2 \\ 3 & 4 & 2\end{bmatrix}$,
then ${D}^{T}=$

Solution: To find the transpose, we interchange the rows and columns:

$$
{D}^{T}=\begin{bmatrix}3 & 3 \\ 1 & 4 \\ 2 & 2\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}3 & 3 \\\\ 1 & 4 \\\\ 2 & 2\\end{bmatrix}', ':db/id': 17592186386748} 

### 17592186387657 q-126125
If
    $A=\begin{bmatrix}\sqrt{2} & 1 \\ 1 & -5\end{bmatrix}$,
then ${A}^{T}=$

Solution: To find the transpose, we interchange the rows and columns:

$$
{A}^{T}=\begin{bmatrix}\sqrt{2} & 1 \\ 1 & -5\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}\\sqrt{2} & 1 \\\\ 1 & -5\\end{bmatrix}', ':db/id': 17592186387663} 

## Finding the Transpose of a Row Vector or Column Vector

### 17592186059553 e-4387
If
    ${A} = 
    \left\lbrack
    \begin{matrix}
        5 & -1 & 0  \end{matrix}
    \right\rbrack,$
then what is ${A^T} ?$

Solution: To find the transpose, we interchange the rows and columns. 

Here, there is just a single row, so it becomes a single column:

$$
{A}^T = 
    		\left\lbrack
    		\begin{matrix}
    5  \\
    -1  \\
    0  \end{matrix}
    		\right\rbrack
$$


### 17592186059966 q-1045
Find ${Z}^{T}$ given that 
$Z=\begin{bmatrix}-4 & 4 & 5 & 1\end{bmatrix}.$

Solution: To find the transpose, we interchange the rows and columns. 

Here, there is just a single row, so it becomes a single column:

$$
{Z}^{T}=\begin{bmatrix}-4 \\ 4 \\ 5 \\ 1\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => None 
selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}-4 \\\\ 4 \\\\ 5 \\\\ 1\\end{bmatrix}', ':db/id': 17592186386093} 

### 17592186059968 q-1048
If
$G = \begin{bmatrix}-4 \\ 15 \\ -1 \\ 8\end{bmatrix}$,
then $G^{T} =$

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186250296 q-11468
Find ${F}^{T}$ given that 
    $F=\begin{bmatrix}3 \\ 3 \\ 2 \\ 1\end{bmatrix}.$

Solution: To find the transpose, we interchange the rows and columns. 

Here, there is just a single column, so it becomes a single row:

$$
{F}^{T}=\begin{bmatrix}3 & 3 & 2 & 1\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}3 & 3 & 2 & 1\\end{bmatrix}', ':db/id': 17592186247424} 

### 17592186262591 q-126136
Find ${L}^{T}$ given that 
    $L=\begin{bmatrix}-a \\ b \\ -c \\ d\end{bmatrix}.$

Solution: To find the transpose, we interchange the rows and columns. 

Here, there is just a single column, so it becomes a single row:

$$
{L}^{T}=\begin{bmatrix}-a & b & -c & d\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}-a & b & -c & d\\end{bmatrix}', ':db/id': 17592186260144} 

### 17592186262592 q-126137
If
    $C=\begin{bmatrix}p \\ q \\ 2r\end{bmatrix},$  then ${C}^{T}=$

Solution: To find the transpose, we interchange the rows and columns. 

Here, there is just a single column, so it becomes a single row:

$$
{C}^{T}=\begin{bmatrix}p & q & 2r\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}p & q & 2r\\end{bmatrix}', ':db/id': 17592186261692} 

### 17592186292842 q-275365
If
    $D=\begin{bmatrix}5 & 2 & 7 & 4\end{bmatrix}$,
then find the transpose of $D.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| ${D}^{T}=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |
|  |  | {{field-4}} |  |

Solution: To find the transpose, we interchange the rows and columns:

$$
{D}^{T}=\begin{bmatrix}5 \\ 2 \\ 7 \\ 4\end{bmatrix}
$$

field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '7', ':db/id': 17592186290771} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '5', ':db/id': 17592186291252} 
field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '4', ':db/id': 17592186291056} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '2', ':db/id': 17592186291369} 

### 17592186292843 q-275366
If
    $H=\begin{bmatrix}u & -v & -x & y\end{bmatrix}$,
then find the transpose of $H.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| ${H}^{T}=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |
|  |  | {{field-4}} |  |

Solution: To find the transpose, we interchange the rows and columns:

$$
{H}^{T}=\begin{bmatrix}u \\ -v \\ -x \\ y\end{bmatrix}
$$

field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': 'y', ':db/id': 17592186291268} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-v', ':db/id': 17592186291672} 
field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-x', ':db/id': 17592186291194} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': 'u', ':db/id': 17592186290827} 

### 17592186295255 q-282761
If
    $Z=\begin{bmatrix}-8 & 2 & 10\end{bmatrix}$,
then find the transpose of $Z.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| ${Z}^{T}=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |

Solution: To find the transpose, we interchange the rows and columns:

$$
{Z}^{T}=\begin{bmatrix}-8 \\ 2 \\ 10\end{bmatrix}
$$

field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '10', ':db/id': 17592186293077} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-8', ':db/id': 17592186293525} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '2', ':db/id': 17592186293330} 

### 17592186295256 q-282766
If
    $R=\begin{bmatrix}-2 & 11\end{bmatrix}$,
then find the transpose of $R.$

  

| ${R}^{T}=$ |  | {{field-1}} |
| --- | --- | --- |
|  | {{field-2}} |  |

Solution: To find the transpose, we interchange the rows and columns:

$$
{R}^{T}=\begin{bmatrix}-2 \\ 11\end{bmatrix}
$$

field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '11', ':db/id': 17592186293382} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-2', ':db/id': 17592186293027} 

### 17592186295257 q-282769
If
    $T=\begin{bmatrix}-5\end{bmatrix}$,
then find the transpose of $T.$

  

| ${T}^{T}=$ |  | {{field-1}} |  |
| --- | --- | --- | --- |

Solution: To find the transpose, we interchange the rows and columns:

$$
{T}^{T}=\begin{bmatrix}-5\end{bmatrix}
$$

field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-5', ':db/id': 17592186293493} 

### 17592186295258 q-282775
If
    $K=\begin{bmatrix}a-b & 3c\end{bmatrix}$,
then find the transpose of $K.$
  

| ${K}^{T}=$ |  | {{field-1}} |
| --- | --- | --- |
|  | {{field-2}} |  |

Solution: To find the transpose, we interchange the rows and columns:

$$
{K}^{T}=\begin{bmatrix}a-b \\ 3c\end{bmatrix}
$$

field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '3c', ':db/id': 17592186293924} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': 'a-b', ':db/id': 17592186293398} 

### 17592186295259 q-282779
If
    $M=\begin{bmatrix}-x \\ 3y\end{bmatrix}$,
then find the transpose of $M.$
  

| ${M}^{T}=$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |

Solution: To find the transpose, we interchange the rows and columns:

$$
{M}^{T}=\begin{bmatrix}-x & 3y\end{bmatrix}
$$

field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-x', ':db/id': 17592186293270} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '3y', ':db/id': 17592186293073} 

### 17592186295260 q-282780
If
    $A=\begin{bmatrix}4 \\ -5\end{bmatrix}$,
then find the transpose of $A.$

  

| ${A}^{T}=$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |

Solution: To find the transpose, we interchange the rows and columns:

$$
{A}^{T}=\begin{bmatrix}4 & -5\end{bmatrix}
$$

field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '4', ':db/id': 17592186293308} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-5', ':db/id': 17592186293806} 

### 17592186295261 q-282781
If
    $Q=\begin{bmatrix}-6 \\ 1 \\ 5\end{bmatrix}$,
then find the transpose of $Q.$

  

| ${Q}^{T}=$ |  | {{field-1}} | {{field-2}} | {{field-3}} |  |
| --- | --- | --- | --- | --- | --- |

Solution: To find the transpose, we interchange the rows and columns:

$$
{Q}^{T}=\begin{bmatrix}-6 & 1 & 5\end{bmatrix}
$$

field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-6', ':db/id': 17592186293349} 
field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '5', ':db/id': 17592186293029} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '1', ':db/id': 17592186293460} 

### 17592186338742 q-70063
If
    $S=\begin{bmatrix}1 \\ -10 \\ 100\end{bmatrix},$  then ${S}^{T}=$

Solution: To find the transpose, we interchange the rows and columns. 

Here, there is just a single column, so it becomes a single row:

$$
{S}^{T}=\begin{bmatrix}1 & -10 & 100\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}1 & -10 & 100\\end{bmatrix}', ':db/id': 17592186337491} 

### 17592186338746 q-70070
Find ${D}^{T}$ given that 
    $D=\begin{bmatrix}x \\ y \\ z\end{bmatrix}.$

Solution: To find the transpose, we interchange the rows and columns. 

Here, there is just a single column, so it becomes a single row:

$$
{D}^{T}=\begin{bmatrix}x & y & z\end{bmatrix}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}x & y & z\\end{bmatrix}', ':db/id': 17592186337944} 

## Determining the Dimensions of the Transpose of a Matrix

### 17592186059554 e-4388
Consider the matrix
    ${B} = 
    \left\lbrack
    \begin{matrix}
        1 & 2 & 4 & 2 \\
        4 & 4 & 1 & 1 \\
        3 & -3 & 0 & -1
    \end{matrix}
    \right\rbrack.$
What are the dimensions of ${B}^T?$

Solution: When a matrix is transposed, its dimensions switch from $N \times M$ to $M \times N.$

So, since $B$ is a $3 \times 4$ matrix, the transpose ${B}^T$ is a $4\times3$ matrix.


### 17592186059994 q-11439
Consider the matrix
$B = \begin{bmatrix}2 & 3 \\ 2 & 3 \\ 3 & 2\end{bmatrix}$.
What are the dimensions of $B^{T}$?

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186059996 q-11465
Consider the matrix
$C = \begin{bmatrix}5 & 3 \\ 4 & 3 \\ 3 & -2 \\ 4 & 1\end{bmatrix}$.
What are the dimensions of $C^{T}$?

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186250292 q-11462
Consider the matrix
    $C=\begin{bmatrix}1 & 3 \\ 2 & 4\end{bmatrix}.$
What are the dimensions of ${C}^{T}?$

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$

So, since $C$ is a $2\times 2$ matrix, the transpose ${C}^{T}$ is a $2\times 2$ matrix too.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '2\\times 2', ':db/id': 17592186247926} 

### 17592186250293 q-11467
Consider the matrix
    $C=\begin{bmatrix}6 & 3 & 2 \\ 4 & 4 & 1 \\ 3 & -2 & 0 \\ 4 & 1 & 7\end{bmatrix}.$
What are the dimensions of ${C}^{T}?$

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$

So, since $C$ is a $4\times 3$ matrix, the transpose ${C}^{T}$ is a $3\times 4$ matrix.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '3\\times 4', ':db/id': 17592186248596} 

### 17592186262593 q-126141
Consider  the matrix
    $X=\begin{bmatrix}-2 \\ 3\end{bmatrix}.$
What are the dimensions of ${X}^{T}?$

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$

So, since $X$ is a $2\times 1$ matrix, the transpose ${X}^{T}$ is a $1\times 2$ matrix.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '1\\times 2', ':db/id': 17592186261531} 

### 17592186262594 q-126142
Consider the matrix
    $Y=\begin{bmatrix}1 & -2\end{bmatrix}.$
What are the dimensions of ${Y}^{T}?$

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$

So, since $Y$ is a $1\times 2$ matrix, the transpose ${Y}^{T}$ is a $2\times 1$ matrix.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '2\\times 1', ':db/id': 17592186260041} 

### 17592186262595 q-126145
Consider  the matrix
    $R=\begin{bmatrix}2\end{bmatrix}.$
What are the dimensions of ${R}^{T}?$

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$

So, since $R$ is a $1\times 1$ matrix, the transpose ${R}^{T}$ is a $1\times 1$ matrix too.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '1\\times 1', ':db/id': 17592186262097} 

### 17592186292844 q-275367
Consider the matrix
  

$$
M=\begin{bmatrix}3 & 4 & 6 & 0 \\ 10 & 17 & 0 & -1 \\ 6 & 0 & 5 & 8\end{bmatrix}.
$$

What are the dimensions of ${M}^{T}?$

${M}^{T}$ is a 

{{field-1}}
$\times $
{{field-2}}
 matrix.

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$

So, since $M$ is a $3\times 4$ matrix, the transpose ${M}^{T}$ is a $4\times 3$ matrix.

field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '4', ':db/id': 17592186291615} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '3', ':db/id': 17592186291187} 

### 17592186295262 q-282783
Consider the matrix
  

$$
R=\begin{bmatrix}2 & 1 \\ 4 & 6 \\ 0 & -3 \\ 5 & 8 \\ 7 & 9\end{bmatrix}.
$$

What are the dimensions of ${R}^{T}?$

${R}^{T}$ is a 

{{field-1}}
$\times $
{{field-2}}
 matrix.

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$

So, since $R$ is a $5\times 2$ matrix, the transpose ${R}^{T}$ is a $2\times 5$ matrix.

field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '5', ':db/id': 17592186293357} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '2', ':db/id': 17592186293253} 

### 17592186295263 q-282784
Consider the matrix
  

$$
Z=\begin{bmatrix}3 & 6 & 1 & 4 & 9 & 0 & 2 \\ -5 & 8 & 3 & 7 & -2 & 6 & 1 \\ 0 & 4 & 5 & 3 & 8 & 1 & 2 \\ 1 & 7 & 6 & -3 & 0 & 2 & 9 \\ 4 & 1 & 8 & 5 & 3 & -1 & 0 \\ 2 & 9 & 7 & 4 & 1 & 3 & 6\end{bmatrix}.
$$

What are the dimensions of ${Z}^{T}?$

${Z}^{T}$ is a 

{{field-1}}
$\times $
{{field-2}}
 matrix.

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$

So, since $Z$ is a $6\times 7$ matrix, the transpose ${Z}^{T}$ is a $7\times 6$ matrix.

field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '6', ':db/id': 17592186293570} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '7', ':db/id': 17592186293885} 

### 17592186295264 q-282786
Consider the matrix
  

$$
P=\begin{bmatrix}-2 & 0 & 5 \\ 7 & 3 & 1 \\ 8 & -4 & 9 \\ 6 & 6 & 6 \\ -1 & 2 & -3 \\ 0 & 0 & 0\end{bmatrix}.
$$

What are the dimensions of ${P}^{T}?$

${P}^{T}$ is a 

{{field-1}}
$\times $
{{field-2}}
 matrix.

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$

So, since $P$ is a $6\times 3$ matrix, the transpose ${P}^{T}$ is a $3\times 6$ matrix.

field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '6', ':db/id': 17592186293750} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '3', ':db/id': 17592186293370} 

### 17592186295265 q-282793
Consider the matrix

$$
F=\begin{bmatrix}6 \\ -4 \\ 1 \\ 9 \\ 0 \\ 2\end{bmatrix}.
$$

What are the dimensions of ${F}^{T}?$

${F}^{T}$ is a 

{{field-1}}
$\times $
{{field-2}}
 matrix.

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$  

So, since $F$ is a $6\times 1$ matrix, the transpose ${F}^{T}$ is a $1\times 6$ matrix.

field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '6', ':db/id': 17592186293063} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '1', ':db/id': 17592186293540} 

### 17592186338741 q-70061
Consider the matrix
    $D=\begin{bmatrix}0 & 1 \\ 0 & 1 \\ 0 & 1 \\ 0 & 1\end{bmatrix}.$
What are the dimensions of ${D}^{T}?$

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$

So, since $D$ is a $4\times 2$ matrix, the transpose ${D}^{T}$ is a $2\times 4$ matrix.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '2\\times 4', ':db/id': 17592186337225} 

### 17592186338743 q-70064
Consider the matrix
    $L=\begin{bmatrix}3 & -4 & 5 & -1 & 2 \\ -2 & -1 & 0 & -1 & 2 \\ 8 & 0 & 1 & -4 & 6\end{bmatrix}.$
What are the dimensions of ${L}^{T}?$

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$

So, since $L$ is a $3\times 5$ matrix, the transpose ${L}^{T}$ is a $5\times 3$ matrix.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '5\\times 3', ':db/id': 17592186337335} 

### 17592186338744 q-70065
Consider the matrix
    $F=\begin{bmatrix}1 & 0 & 1 \\ 0 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 0\end{bmatrix}.$
What are the dimensions of ${F}^{T}?$

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$

So, since $F$ is a $6\times 3$ matrix, the transpose ${F}^{T}$ is a $3\times 6$ matrix.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '3\\times 6', ':db/id': 17592186337455} 

### 17592186338745 q-70068
Consider the matrix
    $Q=\begin{bmatrix}1 & 2 & 3 & 0 \\ 6 & 5 & 4 & 1 \\ 7 & 8 & 9 & 2\end{bmatrix}.$
What are the dimensions of ${Q}^{T}?$

Solution: When a matrix is transposed, its dimensions switch from $m\times n$ to $n\times m.$

So, since $Q$ is a $3\times 4$ matrix, the transpose ${Q}^{T}$ is a $4\times 3$ matrix too.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '4\\times 3', ':db/id': 17592186337983} 

# Scalar Multiplication of Matrices

## Tutorial 17592186060926 Introduction
We can multiply matrices by numbers. This type of multiplication is known as **scalar multiplication**. Here, a **scalar** is just a number.

For example, consider the matrix

$$
\begin{bmatrix}1 & 3 \\ 2 & 4\end{bmatrix}
$$

To multiply ${A}$ by the scalar $2,$ we just multiply each entry of ${A}$ by $2\mathbin{:}$

$$
\begin{aligned}2A & =2\begin{bmatrix}1 & 3 \\ 2 & 4\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 1 & 2\cdot 3 \\ 2\cdot 2 & 2\cdot 4\end{bmatrix} \\  & =\begin{bmatrix}2 & 6 \\ 4 & 8\end{bmatrix}\end{aligned}
$$

In general, to multiply a $m \times n$ matrix $A$ by a scalar $c,$ we multiply each entry of $A$ by $c$ as follows:

$$
\begin{bmatrix}{a}_{11} & {a}_{12} & … & {a}_{1n} \\ {a}_{21} & {a}_{22} & … & {a}_{2n} \\ ⋮ & ⋮ & ⋱ & ⋮ \\ {a}_{m1} & {a}_{m2} & … & {a}_{mn}\end{bmatrix}
$$

## Tutorial 17592186060927 Properties of Scalar Multiplication of Matrices
Since scalar multiplication is done entry-wise, it obeys the same kind of rules as multiplication of real numbers.

For example, for any numbers $c_1, c_2$ and any matrix $A,$ we can perform scalar multiplication in any order: 

$$
c_1 (c_2 A) = (c_1 c_2) A = c_2 (c_1 A)
$$

Moreover, we can distribute a matrix over the sum or difference of scalars:

$$
(c_1 \pm c_2)A = c_1A \pm c_2A
$$

We can also distribute scalar multiplication over the sum or difference of two matrices:

$$
c (A \pm B) = c A \pm c B
$$

## Multiplying a Matrix by a Scalar

### 17592186059549 e-4380
Calculate $-2A$, if 
$A=\left\lbrack
    	\begin{matrix}
        	2 & -1  \\
        	4 & 7
    	\end{matrix}
    	\right\rbrack.$

Solution: We multiply each entry of $A$ by $-2,$ as follows:

$$
\begin{aligned}-2A & =-2\begin{bmatrix}2 & -1 \\ 4 & 7\end{bmatrix} \\  & =\begin{bmatrix}-2\cdot 2 & -2\cdot (-1) \\ -2\cdot 4 & -2\cdot 7\end{bmatrix} \\  & =\begin{bmatrix}-4 & 2 \\ -8 & -14\end{bmatrix}\end{aligned}
$$


### 17592186060452 q-979
What is $5\begin{bmatrix}1 & 0 \\ 2 & 6\end{bmatrix}$?

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186060457 q-986
Calculate $6D$, if
$D = \begin{bmatrix}-1 & 2 \\ 1 & 0 \\ \frac{1}{3} & 4\end{bmatrix}$.

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186259867 q-125885
Calculate $0W$, if 
$W=\begin{bmatrix}1 & -1 & -3 \\ -5 & 0 & 2\end{bmatrix}.$

Solution: We multiply each entry of $W$ by $0,$ as follows:

$$
\begin{aligned}0W & =0\begin{bmatrix}1 & -1 & -3 \\ -5 & 0 & 2\end{bmatrix} \\  & =\begin{bmatrix}0\cdot 1 & 0\cdot (-1) & 0\cdot (-3) \\ 0\cdot (-5) & 0\cdot 0 & 0\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}0 & 0 & 0 \\ 0 & 0 & 0\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}0 & 0 & 0 \\\\ 0 & 0 & 0\\end{bmatrix}', ':db/id': 17592186257499} 

### 17592186299816 q-320045
Calculate $3A$, where
$A=\begin{bmatrix}2 & 1 \\ 4 & 3\end{bmatrix}.$

| $3A=\,\,$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
|  | {{field-3}} | {{field-4}} |  |  |

Solution: We multiply each entry of $A$ by $3,$ as follows:

$$
\begin{aligned}3A & =3\begin{bmatrix}2 & 1 \\ 4 & 3\end{bmatrix} \\  & =\begin{bmatrix}3\cdot 2 & 3\cdot 1 \\ 3\cdot 4 & 3\cdot 3\end{bmatrix} \\  & =\begin{bmatrix}6 & 3 \\ 12 & 9\end{bmatrix}\end{aligned}
$$

field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '9', ':db/id': 17592186298539} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '6', ':db/id': 17592186298096} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '3', ':db/id': 17592186297695} 
field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '12', ':db/id': 17592186297884} 

### 17592186299819 q-320075
Calculate $-7A$, where
$A=\begin{bmatrix}5 & 4 \\ -6 & 2\end{bmatrix}.$

| $-7A=\,\,$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
|  | {{field-3}} | {{field-4}} |  |  |

Solution: We multiply each entry of $A$ by $3,$ as follows:

$$
\begin{aligned}-7A & =-7\begin{bmatrix}5 & 4 \\ -6 & 2\end{bmatrix} \\  & =\begin{bmatrix}(-7)\cdot 5 & (-7)\cdot 4 \\ (-7)\cdot (-6) & (-7)\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}-35 & -28 \\ 42 & -14\end{bmatrix}\end{aligned}
$$

field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-35', ':db/id': 17592186297714} 
field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-14', ':db/id': 17592186297753} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-28', ':db/id': 17592186297946} 
field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '42', ':db/id': 17592186298640} 

### 17592186299820 q-320082
Calculate $2C$, where
$C=\begin{bmatrix}1 & 2 \\ -2 & 4\end{bmatrix}.$

| $2C=\,\,$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
|  | {{field-3}} | {{field-4}} |  |  |

Solution: We multiply each entry of $C$ by $2,$ as follows:

$$
\begin{aligned}2C & =2\begin{bmatrix}1 & 2 \\ -2 & 4\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 1 & 2\cdot 2 \\ 2\cdot (-2) & 2\cdot 4\end{bmatrix} \\  & =\begin{bmatrix}2 & 4 \\ -4 & 8\end{bmatrix}\end{aligned}
$$

field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-4', ':db/id': 17592186297806} 
field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '8', ':db/id': 17592186297752} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '2', ':db/id': 17592186297583} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '4', ':db/id': 17592186297941} 

### 17592186362261 q-980
$3\begin{bmatrix}4 & -5 \\ -2 & \frac{1}{3}\end{bmatrix}=$

Solution: We multiply each entry of the matrix by $3$, as follows:

$$
\begin{aligned}3\begin{bmatrix}4 & -5 \\ -2 & \frac{1}{3}\end{bmatrix} & =\begin{bmatrix}3\cdot 4 & 3\cdot (-5) \\ 3\cdot (-2) & 3\cdot \frac{1}{3}\end{bmatrix} \\  & =\begin{bmatrix}12 & -15 \\ -6 & 1\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}12 & -15 \\\\ -6 & 1\\end{bmatrix}', ':db/id': 17592186361706} 

### 17592186539208 authored
Calculate $- \frac{3}{5}A$, if 
$A=\begin{bmatrix}\frac{3}{5} & \frac{5}{4} & - \frac{1}{2} \\ - \frac{1}{4} & \frac{5}{4} & - \frac{2}{3}\end{bmatrix}.$

Solution: We multiply each entry of $A$ by $- \frac{3}{5},$ as follows:

$$
\begin{aligned}- \frac{3}{5}A & =- \frac{3}{5}\begin{bmatrix}\frac{3}{5} & \frac{5}{4} & - \frac{1}{2} \\ - \frac{1}{4} & \frac{5}{4} & - \frac{2}{3}\end{bmatrix} \\  & =\begin{bmatrix}(- \frac{3}{5})\cdot \frac{3}{5} & (- \frac{3}{5})\cdot \frac{5}{4} & (- \frac{3}{5})\cdot (- \frac{1}{2}) \\ (- \frac{3}{5})\cdot (- \frac{1}{4}) & (- \frac{3}{5})\cdot \frac{5}{4} & (- \frac{3}{5})\cdot (- \frac{2}{3})\end{bmatrix} \\  & =\begin{bmatrix}- \frac{9}{25} & - \frac{3}{4} & \frac{3}{10} \\ \frac{3}{20} & - \frac{3}{4} & \frac{2}{5}\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}- \\frac{9}{25} & - \\frac{3}{4} & \\frac{3}{10} \\\\ \\frac{3}{20} & - \\frac{3}{4} & \\frac{2}{5}\\end{bmatrix}', ':db/id': 17592186539254} 

### 17592186539210 authored
$- \frac{3}{4}\begin{bmatrix}- \frac{1}{4} & - \frac{4}{5} \\ \frac{5}{2} & \frac{1}{5} \\ \frac{4}{3} & - \frac{4}{5}\end{bmatrix}=$

Solution: We multiply each entry of the matrix by $- \frac{3}{4}$, as follows:

$$
\begin{aligned}- \frac{3}{4}\begin{bmatrix}- \frac{1}{4} & - \frac{4}{5} \\ \frac{5}{2} & \frac{1}{5} \\ \frac{4}{3} & - \frac{4}{5}\end{bmatrix} & =\begin{bmatrix}(- \frac{3}{4})\cdot (- \frac{1}{4}) & (- \frac{3}{4})\cdot (- \frac{4}{5}) \\ (- \frac{3}{4})\cdot \frac{5}{2} & (- \frac{3}{4})\cdot \frac{1}{5} \\ (- \frac{3}{4})\cdot \frac{4}{3} & (- \frac{3}{4})\cdot (- \frac{4}{5})\end{bmatrix} \\  & =\begin{bmatrix}\frac{3}{16} & \frac{3}{5} \\ - \frac{15}{8} & - \frac{3}{20} \\ -1 & \frac{3}{5}\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}\\frac{3}{16} & \\frac{3}{5} \\\\ - \\frac{15}{8} & - \\frac{3}{20} \\\\ -1 & \\frac{3}{5}\\end{bmatrix}', ':db/id': 17592186539264} 

### 17592186539222 authored
$-4\begin{bmatrix}-4 & -1 \\ -3 & \frac{1}{4}\end{bmatrix}=$

Solution: We multiply each entry of the matrix by $-4$, as follows:

$$
\begin{aligned}-4\begin{bmatrix}-4 & -1 \\ -3 & \frac{1}{4}\end{bmatrix} & =\begin{bmatrix}(-4)\cdot (-4) & (-4)\cdot (-1) \\ (-4)\cdot (-3) & (-4)\cdot \frac{1}{4}\end{bmatrix} \\  & =\begin{bmatrix}16 & 4 \\ 12 & -1\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}16 & 4 \\\\ 12 & -1\\end{bmatrix}', ':db/id': 17592186539250} 

### 17592186539223 authored
Calculate $\frac{2}{5}D$, if 
$D=\begin{bmatrix}- \frac{4}{5} & \frac{5}{2} & - \frac{2}{3} \\ - \frac{1}{5} & - \frac{3}{4} & - \frac{1}{2}\end{bmatrix}.$

Solution: We multiply each entry of $D$ by $\frac{2}{5},$ as follows:

$$
\begin{aligned}\frac{2}{5}D & =\frac{2}{5}\begin{bmatrix}- \frac{4}{5} & \frac{5}{2} & - \frac{2}{3} \\ - \frac{1}{5} & - \frac{3}{4} & - \frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}\frac{2}{5}\cdot (- \frac{4}{5}) & \frac{2}{5}\cdot \frac{5}{2} & \frac{2}{5}\cdot (- \frac{2}{3}) \\ \frac{2}{5}\cdot (- \frac{1}{5}) & \frac{2}{5}\cdot (- \frac{3}{4}) & \frac{2}{5}\cdot (- \frac{1}{2})\end{bmatrix} \\  & =\begin{bmatrix}- \frac{8}{25} & 1 & - \frac{4}{15} \\ - \frac{2}{25} & - \frac{3}{10} & - \frac{1}{5}\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}- \\frac{8}{25} & 1 & - \\frac{4}{15} \\\\ - \\frac{2}{25} & - \\frac{3}{10} & - \\frac{1}{5}\\end{bmatrix}', ':db/id': 17592186539280} 

### 17592186539227 authored
Calculate $- \frac{1}{2}D$, if 
$D=\begin{bmatrix}-4 & 3 & -7 \\ 8 & 6 & 3\end{bmatrix}.$

Solution: We multiply each entry of $D$ by $- \frac{1}{2},$ as follows:

$$
\begin{aligned}- \frac{1}{2}D & =- \frac{1}{2}\begin{bmatrix}-4 & 3 & -7 \\ 8 & 6 & 3\end{bmatrix} \\  & =\begin{bmatrix}(- \frac{1}{2})\cdot (-4) & (- \frac{1}{2})\cdot 3 & (- \frac{1}{2})\cdot (-7) \\ (- \frac{1}{2})\cdot 8 & (- \frac{1}{2})\cdot 6 & (- \frac{1}{2})\cdot 3\end{bmatrix} \\  & =\begin{bmatrix}2 & - \frac{3}{2} & \frac{7}{2} \\ -4 & -3 & - \frac{3}{2}\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}2 & - \\frac{3}{2} & \\frac{7}{2} \\\\ -4 & -3 & - \\frac{3}{2}\\end{bmatrix}', ':db/id': 17592186539281} 

### 17592186539229 authored
Calculate $\frac{1}{2}W$, if 
$W=\begin{bmatrix}6 & 7 & -4 \\ -2 & -1 & -3\end{bmatrix}.$

Solution: We multiply each entry of $W$ by $\frac{1}{2},$ as follows:

$$
\begin{aligned}\frac{1}{2}W & =\frac{1}{2}\begin{bmatrix}6 & 7 & -4 \\ -2 & -1 & -3\end{bmatrix} \\  & =\begin{bmatrix}\frac{1}{2}\cdot 6 & \frac{1}{2}\cdot 7 & \frac{1}{2}\cdot (-4) \\ \frac{1}{2}\cdot (-2) & \frac{1}{2}\cdot (-1) & \frac{1}{2}\cdot (-3)\end{bmatrix} \\  & =\begin{bmatrix}3 & \frac{7}{2} & -2 \\ -1 & - \frac{1}{2} & - \frac{3}{2}\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}3 & \\frac{7}{2} & -2 \\\\ -1 & - \\frac{1}{2} & - \\frac{3}{2}\\end{bmatrix}', ':db/id': 17592186539230} 

### 17592186539235 authored
Calculate $- \frac{1}{2}D$, if 
$D=\begin{bmatrix}-6 & 3 & -4 \\ 6 & -1 & 1\end{bmatrix}.$

Solution: We multiply each entry of $D$ by $- \frac{1}{2},$ as follows:

$$
\begin{aligned}- \frac{1}{2}D & =- \frac{1}{2}\begin{bmatrix}-6 & 3 & -4 \\ 6 & -1 & 1\end{bmatrix} \\  & =\begin{bmatrix}(- \frac{1}{2})\cdot (-6) & (- \frac{1}{2})\cdot 3 & (- \frac{1}{2})\cdot (-4) \\ (- \frac{1}{2})\cdot 6 & (- \frac{1}{2})\cdot (-1) & (- \frac{1}{2})\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}3 & - \frac{3}{2} & 2 \\ -3 & \frac{1}{2} & - \frac{1}{2}\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}3 & - \\frac{3}{2} & 2 \\\\ -3 & \\frac{1}{2} & - \\frac{1}{2}\\end{bmatrix}', ':db/id': 17592186539267} 

### 17592186539239 authored
$\frac{3}{5}\begin{bmatrix}- \frac{1}{3} & - \frac{2}{5} \\ \frac{5}{3} & \frac{1}{2} \\ - \frac{2}{5} & \frac{5}{4}\end{bmatrix}=$

Solution: We multiply each entry of the matrix by $\frac{3}{5}$, as follows:

$$
\begin{aligned}\frac{3}{5}\begin{bmatrix}- \frac{1}{3} & - \frac{2}{5} \\ \frac{5}{3} & \frac{1}{2} \\ - \frac{2}{5} & \frac{5}{4}\end{bmatrix} & =\begin{bmatrix}\frac{3}{5}\cdot (- \frac{1}{3}) & \frac{3}{5}\cdot (- \frac{2}{5}) \\ \frac{3}{5}\cdot \frac{5}{3} & \frac{3}{5}\cdot \frac{1}{2} \\ \frac{3}{5}\cdot (- \frac{2}{5}) & \frac{3}{5}\cdot \frac{5}{4}\end{bmatrix} \\  & =\begin{bmatrix}- \frac{1}{5} & - \frac{6}{25} \\ 1 & \frac{3}{10} \\ - \frac{6}{25} & \frac{3}{4}\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}- \\frac{1}{5} & - \\frac{6}{25} \\\\ 1 & \\frac{3}{10} \\\\ - \\frac{6}{25} & \\frac{3}{4}\\end{bmatrix}', ':db/id': 17592186539252} 

### 17592186539270 authored
$- \frac{1}{2}\begin{bmatrix}-2 & -5 \\ 8 & 2 \\ -7 & -5\end{bmatrix}=$

Solution: We multiply each entry of the matrix by $- \frac{1}{2}$, as follows:

$$
\begin{aligned}- \frac{1}{2}\begin{bmatrix}-2 & -5 \\ 8 & 2 \\ -7 & -5\end{bmatrix} & =\begin{bmatrix}(- \frac{1}{2})\cdot (-2) & (- \frac{1}{2})\cdot (-5) \\ (- \frac{1}{2})\cdot 8 & (- \frac{1}{2})\cdot 2 \\ (- \frac{1}{2})\cdot (-7) & (- \frac{1}{2})\cdot (-5)\end{bmatrix} \\  & =\begin{bmatrix}1 & \frac{5}{2} \\ -4 & -1 \\ \frac{7}{2} & \frac{5}{2}\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}1 & \\frac{5}{2} \\\\ -4 & -1 \\\\ \\frac{7}{2} & \\frac{5}{2}\\end{bmatrix}', ':db/id': 17592186539273} 

### 17592186539272 authored
$- \frac{1}{2}\begin{bmatrix}7 & -4 \\ 5 & 4 \\ -4 & 1\end{bmatrix}=$

Solution: We multiply each entry of the matrix by $- \frac{1}{2}$, as follows:

$$
\begin{aligned}- \frac{1}{2}\begin{bmatrix}7 & -4 \\ 5 & 4 \\ -4 & 1\end{bmatrix} & =\begin{bmatrix}(- \frac{1}{2})\cdot 7 & (- \frac{1}{2})\cdot (-4) \\ (- \frac{1}{2})\cdot 5 & (- \frac{1}{2})\cdot 4 \\ (- \frac{1}{2})\cdot (-4) & (- \frac{1}{2})\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}- \frac{7}{2} & 2 \\ - \frac{5}{2} & -2 \\ 2 & - \frac{1}{2}\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}- \\frac{7}{2} & 2 \\\\ - \\frac{5}{2} & -2 \\\\ 2 & - \\frac{1}{2}\\end{bmatrix}', ':db/id': 17592186539258} 

### 17592186539282 authored
Calculate $\frac{2}{5}W$, if 
$W=\begin{bmatrix}\frac{4}{5} & - \frac{1}{4} & - \frac{5}{3} \\ - \frac{2}{3} & \frac{5}{4} & \frac{1}{5}\end{bmatrix}.$

Solution: We multiply each entry of $W$ by $\frac{2}{5},$ as follows:

$$
\begin{aligned}\frac{2}{5}W & =\frac{2}{5}\begin{bmatrix}\frac{4}{5} & - \frac{1}{4} & - \frac{5}{3} \\ - \frac{2}{3} & \frac{5}{4} & \frac{1}{5}\end{bmatrix} \\  & =\begin{bmatrix}\frac{2}{5}\cdot \frac{4}{5} & \frac{2}{5}\cdot (- \frac{1}{4}) & \frac{2}{5}\cdot (- \frac{5}{3}) \\ \frac{2}{5}\cdot (- \frac{2}{3}) & \frac{2}{5}\cdot \frac{5}{4} & \frac{2}{5}\cdot \frac{1}{5}\end{bmatrix} \\  & =\begin{bmatrix}\frac{8}{25} & - \frac{1}{10} & - \frac{2}{3} \\ - \frac{4}{15} & \frac{1}{2} & \frac{2}{25}\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}\\frac{8}{25} & - \\frac{1}{10} & - \\frac{2}{3} \\\\ - \\frac{4}{15} & \\frac{1}{2} & \\frac{2}{25}\\end{bmatrix}', ':db/id': 17592186539249} 

## Calculating the Value of a Scalar

### 17592186059550 e-4381
If $k {A} =
\left\lbrack
    	\begin{matrix}
        	1 & 3 & 4  \\
        	6 & 0 & -2
    	\end{matrix}
    	\right\rbrack,$
where ${A} =
\left\lbrack
    	\begin{matrix}
        	2 & 6 & 8  \\
        	12 & 0 & -4
    	\end{matrix}
    	\right\rbrack$
and $k$ is a scalar, calculate the value of $k.$

Solution: To express $kA,$ we multiply each entry of $A$ by $k,$ as follows:

$$
\begin{aligned}kA & =k\cdot \begin{bmatrix}2 & 6 & 8 \\ 12 & 0 & -4\end{bmatrix} \\  & =\begin{bmatrix}2k & 6k & 8k \\ 12k & 0 & -4k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kA$ in the problem statement:

$$
\left\lbrack
    	\begin{matrix}
        	2k & 6k & 8k  \\
        	12k & 0 & -4k
    	\end{matrix}
    	\right\rbrack
=
\left\lbrack
    	\begin{matrix}
        	1 & 3 & 4  \\
        	6 & 0 & -2
    	\end{matrix}
    	\right\rbrack
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the top-left elements, $2k$ and $1.$ Equating these elements, we get

$$
\begin{aligned}2k & =1 \\ k & =\frac{1}{2}.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.


### 17592186059995 q-11442
If $kG = \begin{bmatrix}5 & 0 \\ 10 & 30\end{bmatrix}$,
where $G = \begin{bmatrix}1 & 0 \\ 2 & 6\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k$.

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186060453 q-981
If $kA=\begin{bmatrix}-7 & -21 & 56\end{bmatrix}$,
where $A=\begin{bmatrix}-1 & -3 & 8\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

Solution: To express $kA,$ we multiply each entry of $A$ by $k,$ as follows:

$$
\begin{aligned}kA & =k\cdot \begin{bmatrix}-1 & -3 & 8\end{bmatrix} \\  & =\begin{bmatrix}-k & -3k & 8k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kA$ in the problem statement:

$$
\begin{bmatrix}-k & -3k & 8k\end{bmatrix}=\begin{bmatrix}-7 & -21 & 56\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the leftmost elements, $-k$ and $-7.$ Equating these elements, we get

$$
\begin{aligned}-k & =-7 \\ k & =7.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': 'k=7', ':db/id': 17592186361174} 

### 17592186235400 q-139431
Maria and John agreed to increase the bet. After increasing, Maria's payoff matrix became

$$
\begin{bmatrix}0 & -6 & 6 \\ 6 & 0 & -6 \\ -6 & 6 & 0\end{bmatrix}.
$$

This new matrix is obtained from matrix $P$ using the scalar multiplication $kP$, where

                            
                                    
                                        
                                        $\,k=$

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        .

Solution: To express $kP,$ we multiply each entry of $P$ by $k,$ as follows:

$$
\begin{aligned}kP & =k\begin{bmatrix}0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0\end{bmatrix} \\  & =\begin{bmatrix}0 & -2k & 2k \\ 2k & 0 & -2k \\ -2k & 2k & 0\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the value given for $kP$ in the problem statement:

$$
\begin{bmatrix}0 & -2k & 2k \\ 2k & 0 & -2k \\ -2k & 2k & 0\end{bmatrix}=\begin{bmatrix}0 & -6 & 6 \\ 6 & 0 & -6 \\ -6 & 6 & 0\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the top-right elements, $2k$ and $6.$ Equating these elements, we get

$$
\begin{aligned}2k & =6 \\ k & =3.\end{aligned}
$$

**Note:** We would get the same result by equating any two corresponding (nonzero) elements.

field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '3', ':db/id': 17592186234581} 

### 17592186299853 q-320536
If $kB=\begin{bmatrix}33 & 36 \\ -12 & -24\end{bmatrix}$,
where $B=\begin{bmatrix}11 & 12 \\ -4 & -8\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

Solution: To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}11 & 12 \\ 4 & -8\end{bmatrix} \\  & =\begin{bmatrix}11k & 12k \\ 4k & -8k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}11k & 12k \\ -4k & -8k\end{bmatrix}=\begin{bmatrix}33 & 36 \\ -12 & -24\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the bottom-left elements, $-4k$ and $-12.$ Equating these elements, we get

$$
\begin{aligned}-4k & =-12 \\ k & =3.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '3', ':db/id': 17592186298457} 

### 17592186299855 q-320551
If $kW=\begin{bmatrix}5 & 0 & 0 \\ 0 & 20 & -15 \\ 10 & -10 & 25\end{bmatrix}$,
where $W=\begin{bmatrix}1 & 0 & 0 \\ 0 & 4 & -3 \\ 2 & -2 & 5\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

Solution: To express $kW,$ we multiply each entry of $W$ by $k,$ as follows:

$$
\begin{aligned}kW & =k\begin{bmatrix}1 & 0 & 0 \\ 0 & 4 & -3 \\ 2 & -2 & 5\end{bmatrix} \\  & =\begin{bmatrix}k & 0 & 0 \\ 0 & 4k & -3k \\ 2k & -2k & 5k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kW$ in the problem statement:

$$
\begin{bmatrix}k & 0 & 0 \\ 0 & 4k & -3k \\ 2k & -2k & 5k\end{bmatrix}=\begin{bmatrix}5 & 0 & 0 \\ 0 & 20 & -15 \\ 10 & -10 & 25\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the  leftmost elements of the third row, $2k$ and $10.$ Equating these elements, we get

$$
\begin{aligned}2k & =10 \\ k & =5.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '5', ':db/id': 17592186298115} 

### 17592186299860 q-320563
If $kB=\begin{bmatrix}8 & -4 & 2\end{bmatrix}$,
where $B=\begin{bmatrix}24 & -12 & 6\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

Solution: To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}24 & -12 & 6\end{bmatrix} \\  & =\begin{bmatrix}24k & -12k & 6k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}24k & -12k & 6k\end{bmatrix}=\begin{bmatrix}8 & -4 & 2\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the rightmost elements, $6k$ and $2.$ Equating these elements, we get

$$
\begin{aligned}6k & =2 \\ k & =\frac{1}{3}.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\frac{1}{3}', ':db/id': 17592186298082} 

### 17592186335993 q-69670
If $kS=\begin{bmatrix}63 & -28 \\ 0 & -56\end{bmatrix}$,
where $S=\begin{bmatrix}-9 & 4 \\ 0 & 8\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

Solution: To express $kS,$ we multiply each entry of $S$ by $k,$ as follows:

$$
\begin{aligned}kS & =k\begin{bmatrix}-9 & 4 \\ 0 & 8\end{bmatrix} \\  & =\begin{bmatrix}-9k & 4k \\ 0 & 8k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kS$ in the problem statement:

$$
\begin{bmatrix}-9k & 4k \\ 0 & 8k\end{bmatrix}=\begin{bmatrix}63 & -28 \\ 0 & -56\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the top-left elements, $-9k$ and $63.$ Equating these elements, we get

$$
\begin{aligned}-9k & =63 \\ k & =-7.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': 'k=-7', ':db/id': 17592186334372} 

### 17592186530579 authored
If $kA=\begin{bmatrix}-12 & -54 & 60\end{bmatrix}$,
where $A=\begin{bmatrix}-2 & -9 & 10\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

Solution: To express $kA,$ we multiply each entry of $A$ by $k,$ as follows:

$$
\begin{aligned}kA & =k\cdot \begin{bmatrix}-2 & -9 & 10\end{bmatrix} \\  & =\begin{bmatrix}- 2 k & - 9 k & 10 k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kA$ in the problem statement:

$$
\begin{bmatrix}- 2 k & - 9 k & 10 k\end{bmatrix}=\begin{bmatrix}-12 & -54 & 60\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $2$, $- 9 k$ and $-54.$ Equating these elements, we get

$$
\begin{aligned}- 9 k & =-54 \\ k & =6.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': 'k=6', ':db/id': 17592186530577} 

## Calculating a Linear Combination of Two Matrices

### 17592186059551 e-4382
Calculate $2 {A} + \dfrac{1}{2} {B}$, where
$\begin{bmatrix}1 & 5 \\ 1 & 2\end{bmatrix}$ and ${B}=
    \left\lbrack
    \begin{matrix}
        0 & 2  \\
        4 & 2
    \end{matrix}
    \right\rbrack
.$

Solution: We multiply each entry of $A$ by $2$ and each entry of $B$ by $\dfrac{1}{2},$ and then add the resulting matrices, as follows:

$$
\begin{aligned}2A+\frac{1}{2}B & =2\begin{bmatrix}1 & 5 \\ 1 & 2\end{bmatrix}+\frac{1}{2}\begin{bmatrix}0 & 2 \\ 4 & 2\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 1 & 2\cdot 5 \\ 2\cdot 1 & 2\cdot 2\end{bmatrix}+\begin{bmatrix}\frac{1}{2}\cdot 0 & \frac{1}{2}\cdot 2 \\ \frac{1}{2}\cdot 4 & \frac{1}{2}\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}2 & 10 \\ 2 & 4\end{bmatrix}+\begin{bmatrix}0 & 1 \\ 2 & 1\end{bmatrix} \\  & =\begin{bmatrix}2+0 & 10+1 \\ 2+2 & 4+1\end{bmatrix} \\  & =\begin{bmatrix}2 & 11 \\ 4 & 5\end{bmatrix}\end{aligned}
$$


### 17592186059997 q-11534
Calculate $4A + 6B$, where
$A = \begin{bmatrix}-1 & 1 \\ 1 & -1\end{bmatrix}$
and
$B = \begin{bmatrix}2 & -2 \\ -2 & 2\end{bmatrix}$.

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186059998 q-11536
Calculate $2P - 3Q$, where
$P = \begin{bmatrix}2 & 1 \\ -2 & -1\end{bmatrix}$
and
$Q = \begin{bmatrix}2 & 1 \\ 1 & -1\end{bmatrix}$.

Solution: MISSING

selection {':db/ident': ':answer-field.type/radio'} => None 

### 17592186233218 q-11532
Calculate $2H-3L$, where
$H=\begin{bmatrix}3 & -2 \\ 2 & -1\end{bmatrix}$
and
$L=\begin{bmatrix}0 & 1 \\ 2 & 1\end{bmatrix}.$

Solution: We multiply each entry of $H$ by $2$ and each entry of $L$ by $3,$ and then subtract the resulting matrices, as follows:

$$
\begin{aligned}2H-3L & =2\begin{bmatrix}3 & -2 \\ 2 & -1\end{bmatrix}-3\begin{bmatrix}0 & 1 \\ 2 & 1\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 3 & 2\cdot (-2) \\ 2\cdot 2 & 2\cdot (-1)\end{bmatrix}-\begin{bmatrix}3\cdot 0 & 3\cdot 1 \\ 3\cdot 2 & 3\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}6 & -4 \\ 4 & -2\end{bmatrix}-\begin{bmatrix}0 & 3 \\ 6 & 3\end{bmatrix} \\  & =\begin{bmatrix}6-0 & -4-3 \\ 4-6 & -2-3\end{bmatrix} \\  & =\begin{bmatrix}6 & -7 \\ -2 & -5\end{bmatrix}\end{aligned}
$$


### 17592186250392 q-11531
Calculate $3F+\frac{1}{2}G$, where
$F=\begin{bmatrix}1 & 3 \\ -2 & 2\end{bmatrix}$
and
$G=\begin{bmatrix}2 & 0 \\ 4 & 6\end{bmatrix}.$

Solution: We multiply each entry of $F$ by $3$ and each entry of $G$ by $\frac{1}{2},$ and then add the resulting matrices, as follows:

$$
\begin{aligned}3F+\frac{1}{2}G & =3\begin{bmatrix}1 & 3 \\ -2 & 2\end{bmatrix}+\frac{1}{2}\begin{bmatrix}2 & 0 \\ 4 & 6\end{bmatrix} \\  & =\begin{bmatrix}3\cdot 1 & 3\cdot 3 \\ 3\cdot (-2) & 3\cdot 2\end{bmatrix}+\begin{bmatrix}\frac{1}{2}\cdot 2 & \frac{1}{2}\cdot 0 \\ \frac{1}{2}\cdot 4 & \frac{1}{2}\cdot 6\end{bmatrix} \\  & =\begin{bmatrix}3 & 9 \\ -6 & 6\end{bmatrix}+\begin{bmatrix}1 & 0 \\ 2 & 3\end{bmatrix} \\  & =\begin{bmatrix}3+1 & 9+0 \\ -6+2 & 6+3\end{bmatrix} \\  & =\begin{bmatrix}4 & 9 \\ -4 & 9\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}4 & 9 \\\\ -4 & 9\\end{bmatrix}', ':db/id': 17592186249560} 

### 17592186262575 q-126009
Calculate $-A+2B$, where
$A=\begin{bmatrix}3 & 1 \\ 1 & 0\end{bmatrix}$
and
$B=\begin{bmatrix}0 & -2 \\ -2 & 2\end{bmatrix}.$

Solution: We multiply each entry of $A$ by $-1$ and each entry of $B$ by $2,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}-A+2B & =(-1)\begin{bmatrix}3 & 1 \\ 1 & 0\end{bmatrix}+2\begin{bmatrix}0 & -2 \\ -2 & 2\end{bmatrix} \\  & =\begin{bmatrix}(-1)\cdot 3 & (-1)\cdot 1 \\ (-1)\cdot 1 & (-1)\cdot 0\end{bmatrix}+\begin{bmatrix}2\cdot 0 & 2\cdot (-2) \\ 2\cdot (-2) & 2\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}-3 & -1 \\ -1 & 0\end{bmatrix}+\begin{bmatrix}0 & -4 \\ -4 & 4\end{bmatrix} \\  & =\begin{bmatrix}-3+0 & -1+(-4) \\ -1+(-4) & 0+4\end{bmatrix} \\  & =\begin{bmatrix}-3 & -5 \\ -5 & 4\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}-3 & -5 \\\\ -5 & 4\\end{bmatrix}', ':db/id': 17592186261489} 

### 17592186299869 q-320656
Calculate $4F-\frac{1}{2}G$, where
$F=\begin{bmatrix}4 & -1 & 0 & 2\end{bmatrix}$
and
$G=\begin{bmatrix}2 & 0 & 4 & -6\end{bmatrix}.$

| $4F-\frac{1}{2}G=\,\,$ |  | {{field-1}} | {{field-2}} | {{field-3}} | {{field-4}} |  |
| --- | --- | --- | --- | --- | --- | --- |

Solution: We multiply each entry of $F$ by $4$ and each entry of $G$ by $\frac{1}{2},$ and then subtract the resulting matrices, as follows:

$$
\begin{aligned}4F-\frac{1}{2}G & =4\begin{bmatrix}4 & -1 & 0 & 2\end{bmatrix}-\frac{1}{2}\begin{bmatrix}2 & 0 & 4 & -6\end{bmatrix} \\  & =\begin{bmatrix}4\cdot 4 & 4\cdot (-1) & 4\cdot 0 & 4\cdot 2\end{bmatrix}-\begin{bmatrix}\frac{1}{2}\cdot 2 & \frac{1}{2}\cdot 0 & \frac{1}{2}\cdot 4 & \frac{1}{2}\cdot (-6)\end{bmatrix} \\  & =\begin{bmatrix}16 & -4 & 0 & 8\end{bmatrix}-\begin{bmatrix}1 & 0 & 2 & -3\end{bmatrix} \\  & =\begin{bmatrix}16-1 & -4-0 & 0-2 & 8-(-3)\end{bmatrix} \\  & =\begin{bmatrix}15 & -4 & -2 & 11\end{bmatrix}\end{aligned}
$$

field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '15', ':db/id': 17592186298010} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-4', ':db/id': 17592186298007} 
field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-2', ':db/id': 17592186297835} 
field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '11', ':db/id': 17592186297601} 

### 17592186299873 q-320671
Calculate $\frac{2}{3}M+2N$, where
$M=\begin{bmatrix}6 & 0 & 15 \\ -12 & 6 & 0\end{bmatrix}$
and
$N=\begin{bmatrix}3 & -1 & 0 \\ -2 & \frac{1}{2} & -1\end{bmatrix}.$

| $\frac{2}{3}M+2N=\,\,$ |  | {{field-1}} | $-2$ | {{field-2}} |  |
| --- | --- | --- | --- | --- | --- |
|  | $-12$ | {{field-3}} | {{field-4}} |  |  |

Solution: We multiply each entry of $M$ by $\frac{2}{3}$ and each entry of $N$ by $2,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}\frac{2}{3}M+2N & =\frac{2}{3}\begin{bmatrix}6 & 0 & 15 \\ -12 & 6 & 0\end{bmatrix}+2\begin{bmatrix}3 & -1 & 0 \\ -2 & \frac{1}{2} & -1\end{bmatrix} \\  & =\begin{bmatrix}\frac{2}{3}\cdot 6 & \frac{2}{3}\cdot 0 & \frac{2}{3}\cdot 15 \\ \frac{2}{3}\cdot (-12) & \frac{2}{3}\cdot 6 & \frac{2}{3}\cdot 0\end{bmatrix}+\begin{bmatrix}2\cdot 3 & 2\cdot (-1) & 2\cdot 0 \\ 2\cdot (-2) & 2\cdot \frac{1}{2} & 2\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}4 & 0 & 10 \\ -8 & 4 & 0\end{bmatrix}+\begin{bmatrix}6 & -2 & 0 \\ -4 & 1 & -2\end{bmatrix} \\  & =\begin{bmatrix}4+6 & 0-2 & 10+0 \\ -8-4 & 4+1 & 0-2\end{bmatrix} \\  & =\begin{bmatrix}10 & -2 & 10 \\ -12 & 5 & -2\end{bmatrix}\end{aligned}
$$

field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '5', ':db/id': 17592186297786} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '10', ':db/id': 17592186297756} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '10', ':db/id': 17592186298509} 
field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-2', ':db/id': 17592186298633} 

### 17592186392959 q-69642
Calculate $\frac{1}{3}G+2H$, where
$G=\begin{bmatrix}3 & 6 & 15 \\ -12 & 9 & 6\end{bmatrix}$
and
$H=\begin{bmatrix}1 & 2 & 5 \\ 3 & 4 & 6\end{bmatrix}.$

Solution: We multiply each entry of $G$ by $\frac{1}{3}$ and each entry of $H$ by $2,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}\frac{1}{3}G+2H & =\frac{1}{3}\begin{bmatrix}3 & 6 & 15 \\ -12 & 9 & 6\end{bmatrix}+2\begin{bmatrix}1 & 2 & 5 \\ 3 & 4 & 6\end{bmatrix} \\  & =\begin{bmatrix}\frac{1}{3}\cdot 3 & \frac{1}{3}\cdot 6 & \frac{1}{3}\cdot 15 \\ \frac{1}{3}\cdot (-12) & \frac{1}{3}\cdot 9 & \frac{1}{3}\cdot 6\end{bmatrix}+\begin{bmatrix}2\cdot 1 & 2\cdot 2 & 2\cdot 5 \\ 2\cdot 3 & 2\cdot 4 & 2\cdot 6\end{bmatrix} \\  & =\begin{bmatrix}1 & 2 & 5 \\ -4 & 3 & 2\end{bmatrix}+\begin{bmatrix}2 & 4 & 10 \\ 6 & 8 & 12\end{bmatrix} \\  & =\begin{bmatrix}1+2 & 2+4 & 5+10 \\ -4+6 & 3+8 & 2+12\end{bmatrix} \\  & =\begin{bmatrix}3 & 6 & 15 \\ 2 & 11 & 14\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}3 & 6 & 15 \\\\ 2 & 11 & 14\\end{bmatrix}', ':db/id': 17592186392962} 

### 17592186547198 authored
Calculate $2F+2B$, where
$F=\begin{bmatrix}2 & 4 \\ 4 & 4\end{bmatrix}$
and
$B=\begin{bmatrix}3 & 2 \\ 4 & 1\end{bmatrix}.$

Solution: We multiply each entry of $F$ by $2$ and each entry of $B$ by $2,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}2F+2B & =2\begin{bmatrix}2 & 4 \\ 4 & 4\end{bmatrix}+2\begin{bmatrix}3 & 2 \\ 4 & 1\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 2 & 2\cdot 4 \\ 2\cdot 4 & 2\cdot 4\end{bmatrix}+\begin{bmatrix}2\cdot 3 & 2\cdot 2 \\ 2\cdot 4 & 2\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}4 & 8 \\ 8 & 8\end{bmatrix}+\begin{bmatrix}6 & 4 \\ 8 & 2\end{bmatrix} \\  & =\begin{bmatrix}4+6 & 8+4 \\ 8+8 & 8+2\end{bmatrix} \\  & =\begin{bmatrix}10 & 12 \\ 16 & 10\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}10 & 12 \\\\ 16 & 10\\end{bmatrix}', ':db/id': 17592186547211} 

### 17592186547205 authored
Calculate $6L+\frac{1}{2}A$, where
$L=\begin{bmatrix}3 & 2 \\ 5 & 2\end{bmatrix}$
and
$A=\begin{bmatrix}6 & 0 \\ -2 & -2\end{bmatrix}.$

Solution: We multiply each entry of $L$ by $6$ and each entry of $A$ by $\frac{1}{2},$ and then add the resulting matrices, as follows:

$$
\begin{aligned}6L+\frac{1}{2}A & =6\begin{bmatrix}3 & 2 \\ 5 & 2\end{bmatrix}+\frac{1}{2}\begin{bmatrix}6 & 0 \\ -2 & -2\end{bmatrix} \\  & =\begin{bmatrix}6\cdot 3 & 6\cdot 2 \\ 6\cdot 5 & 6\cdot 2\end{bmatrix}+\begin{bmatrix}\frac{1}{2}\cdot 6 & \frac{1}{2}\cdot 0 \\ \frac{1}{2}\cdot (-2) & \frac{1}{2}\cdot (-2)\end{bmatrix} \\  & =\begin{bmatrix}18 & 12 \\ 30 & 12\end{bmatrix}+\begin{bmatrix}3 & 0 \\ -1 & -1\end{bmatrix} \\  & =\begin{bmatrix}18+3 & 12+0 \\ 30+(-1) & 12+(-1)\end{bmatrix} \\  & =\begin{bmatrix}21 & 12 \\ 29 & 11\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}21 & 12 \\\\ 29 & 11\\end{bmatrix}', ':db/id': 17592186547241} 

### 17592186547210 authored
Calculate $2M+2F$, where
$M=\begin{bmatrix}4 & 3 \\ 4 & 4\end{bmatrix}$
and
$F=\begin{bmatrix}4 & 1 \\ 3 & 1\end{bmatrix}.$

Solution: We multiply each entry of $M$ by $2$ and each entry of $F$ by $2,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}2M+2F & =2\begin{bmatrix}4 & 3 \\ 4 & 4\end{bmatrix}+2\begin{bmatrix}4 & 1 \\ 3 & 1\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 4 & 2\cdot 3 \\ 2\cdot 4 & 2\cdot 4\end{bmatrix}+\begin{bmatrix}2\cdot 4 & 2\cdot 1 \\ 2\cdot 3 & 2\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}8 & 6 \\ 8 & 8\end{bmatrix}+\begin{bmatrix}8 & 2 \\ 6 & 2\end{bmatrix} \\  & =\begin{bmatrix}8+8 & 6+2 \\ 8+6 & 8+2\end{bmatrix} \\  & =\begin{bmatrix}16 & 8 \\ 14 & 10\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}16 & 8 \\\\ 14 & 10\\end{bmatrix}', ':db/id': 17592186547254} 

### 17592186547215 authored
Calculate $3A+2B$, where
$A=\begin{bmatrix}3 & 3 \\ 4 & 3\end{bmatrix}$
and
$B=\begin{bmatrix}0 & 3 \\ 2 & 2\end{bmatrix}.$

Solution: We multiply each entry of $A$ by $3$ and each entry of $B$ by $2,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}3A+2B & =3\begin{bmatrix}3 & 3 \\ 4 & 3\end{bmatrix}+2\begin{bmatrix}0 & 3 \\ 2 & 2\end{bmatrix} \\  & =\begin{bmatrix}3\cdot 3 & 3\cdot 3 \\ 3\cdot 4 & 3\cdot 3\end{bmatrix}+\begin{bmatrix}2\cdot 0 & 2\cdot 3 \\ 2\cdot 2 & 2\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}9 & 9 \\ 12 & 9\end{bmatrix}+\begin{bmatrix}0 & 6 \\ 4 & 4\end{bmatrix} \\  & =\begin{bmatrix}9+0 & 9+6 \\ 12+4 & 9+4\end{bmatrix} \\  & =\begin{bmatrix}9 & 15 \\ 16 & 13\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}9 & 15 \\\\ 16 & 13\\end{bmatrix}', ':db/id': 17592186547265} 

### 17592186547216 authored
Calculate $\frac{2}{3}L+2A$, where
$L=\begin{bmatrix}-3 & -3 & -9 \\ 18 & -3 & 0\end{bmatrix}$
and
$A=\begin{bmatrix}- \frac{3}{2} & 3 & - \frac{3}{2} \\ -3 & 2 & 1\end{bmatrix}.$

| $\frac{2}{3}L+2A=\,\,$ |  | {{field-1}} | {{field-2}} | $-9$ |  |
| --- | --- | --- | --- | --- | --- |
|  |  | {{field-3}} | $2$ | {{field-4}} |  |

Solution: We multiply each entry of $L$ by $\frac{2}{3}$ and each entry of $A$ by $2,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}\frac{2}{3}L+2A & =\frac{2}{3}\begin{bmatrix}-3 & -3 & -9 \\ 18 & -3 & 0\end{bmatrix}+2\begin{bmatrix}- \frac{3}{2} & 3 & - \frac{3}{2} \\ -3 & 2 & 1\end{bmatrix} \\  & =\begin{bmatrix}\frac{2}{3}\cdot (-3) & \frac{2}{3}\cdot (-3) & \frac{2}{3}\cdot (-9) \\ \frac{2}{3}\cdot 18 & \frac{2}{3}\cdot (-3) & \frac{2}{3}\cdot 0\end{bmatrix}+\begin{bmatrix}2\cdot (- \frac{3}{2}) & 2\cdot 3 & 2\cdot (- \frac{3}{2}) \\ 2\cdot (-3) & 2\cdot 2 & 2\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}-2 & -2 & -6 \\ 12 & -2 & 0\end{bmatrix}+\begin{bmatrix}-3 & 6 & -3 \\ -6 & 4 & 2\end{bmatrix} \\  & =\begin{bmatrix}-2-3 & -2+6 & -6-3 \\ 12-6 & -2+4 & 0+2\end{bmatrix} \\  & =\begin{bmatrix}-5 & 4 & -9 \\ 6 & 2 & 2\end{bmatrix}\end{aligned}
$$

field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '6', ':db/id': 17592186547260} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-5', ':db/id': 17592186547209} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '4', ':db/id': 17592186547259} 
field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '2', ':db/id': 17592186547230} 

### 17592186547223 authored
Calculate $6P + 3H$, where
$P = \begin{bmatrix}1 & 0 \\ 4 & 4\end{bmatrix}$
and
$H = \begin{bmatrix}1 & 0 \\ -3 & 0\end{bmatrix}$.

Solution: We multiply each entry of $P$ by $6$ and each entry of $H$ by $3,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}6P+3H & =6\begin{bmatrix}1 & 0 \\ 4 & 4\end{bmatrix}+3\begin{bmatrix}1 & 0 \\ -3 & 0\end{bmatrix} \\  & =\begin{bmatrix}6\cdot 1 & 6\cdot 0 \\ 6\cdot 4 & 6\cdot 4\end{bmatrix}+\begin{bmatrix}3\cdot 1 & 3\cdot 0 \\ 3\cdot (-3) & 3\cdot 0\end{bmatrix} \\  & =\begin{bmatrix}6 & 0 \\ 24 & 24\end{bmatrix}+\begin{bmatrix}3 & 0 \\ -9 & 0\end{bmatrix} \\  & =\begin{bmatrix}6+3 & 0+0 \\ 24+(-9) & 24+0\end{bmatrix} \\  & =\begin{bmatrix}9 & 0 \\ 15 & 24\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}9 & 0 \\\\ 15 & 24\\end{bmatrix}', ':db/id': 17592186547235} 

### 17592186547224 authored
Calculate $\frac{2}{3}Q+2G$, where
$Q=\begin{bmatrix}-3 & -6 & 9 \\ -9 & 6 & -6\end{bmatrix}$
and
$G=\begin{bmatrix}3 & -3 & 0 \\ 0 & \frac{5}{2} & \frac{5}{2}\end{bmatrix}.$

Solution: We multiply each entry of $Q$ by $\frac{2}{3}$ and each entry of $G$ by $2,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}\frac{2}{3}Q+2G & =\frac{2}{3}\begin{bmatrix}-3 & -6 & 9 \\ -9 & 6 & -6\end{bmatrix}+2\begin{bmatrix}3 & -3 & 0 \\ 0 & \frac{5}{2} & \frac{5}{2}\end{bmatrix} \\  & =\begin{bmatrix}\frac{2}{3}\cdot (-3) & \frac{2}{3}\cdot (-6) & \frac{2}{3}\cdot 9 \\ \frac{2}{3}\cdot (-9) & \frac{2}{3}\cdot 6 & \frac{2}{3}\cdot (-6)\end{bmatrix}+\begin{bmatrix}2\cdot 3 & 2\cdot (-3) & 2\cdot 0 \\ 2\cdot 0 & 2\cdot \frac{5}{2} & 2\cdot \frac{5}{2}\end{bmatrix} \\  & =\begin{bmatrix}-2 & -4 & 6 \\ -6 & 4 & -4\end{bmatrix}+\begin{bmatrix}6 & -6 & 0 \\ 0 & 5 & 5\end{bmatrix} \\  & =\begin{bmatrix}-2+6 & -4+(-6) & 6+0 \\ -6+0 & 4+5 & -4+5\end{bmatrix} \\  & =\begin{bmatrix}4 & -10 & 6 \\ -6 & 9 & 1\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}4 & -10 & 6 \\\\ -6 & 9 & 1\\end{bmatrix}', ':db/id': 17592186547269} 

### 17592186547229 authored
Calculate $3B+3M$, where
$B=\begin{bmatrix}2 & 4 \\ 1 & 4\end{bmatrix}$
and
$M=\begin{bmatrix}2 & 0 \\ 3 & 3\end{bmatrix}.$

Solution: We multiply each entry of $B$ by $3$ and each entry of $M$ by $3,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}3B+3M & =3\begin{bmatrix}2 & 4 \\ 1 & 4\end{bmatrix}+3\begin{bmatrix}2 & 0 \\ 3 & 3\end{bmatrix} \\  & =\begin{bmatrix}3\cdot 2 & 3\cdot 4 \\ 3\cdot 1 & 3\cdot 4\end{bmatrix}+\begin{bmatrix}3\cdot 2 & 3\cdot 0 \\ 3\cdot 3 & 3\cdot 3\end{bmatrix} \\  & =\begin{bmatrix}6 & 12 \\ 3 & 12\end{bmatrix}+\begin{bmatrix}6 & 0 \\ 9 & 9\end{bmatrix} \\  & =\begin{bmatrix}6+6 & 12+0 \\ 3+9 & 12+9\end{bmatrix} \\  & =\begin{bmatrix}12 & 12 \\ 12 & 21\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}12 & 12 \\\\ 12 & 21\\end{bmatrix}', ':db/id': 17592186547208} 

### 17592186547244 authored
Calculate $-2Q+4G$, where
$Q=\begin{bmatrix}-2 & 3 \\ -3 & 2\end{bmatrix}$
and
$G=\begin{bmatrix}-1 & 3 \\ -3 & 0\end{bmatrix}.$

Solution: We multiply each entry of $Q$ by $-2$ and each entry of $G$ by $4,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}-2Q+4G & =(-2)\begin{bmatrix}-2 & 3 \\ -3 & 2\end{bmatrix}+4\begin{bmatrix}-1 & 3 \\ -3 & 0\end{bmatrix} \\  & =\begin{bmatrix}(-2)\cdot (-2) & (-2)\cdot 3 \\ (-2)\cdot (-3) & (-2)\cdot 2\end{bmatrix}+\begin{bmatrix}4\cdot (-1) & 4\cdot 3 \\ 4\cdot (-3) & 4\cdot 0\end{bmatrix} \\  & =\begin{bmatrix}4 & -6 \\ 6 & -4\end{bmatrix}+\begin{bmatrix}-4 & 12 \\ -12 & 0\end{bmatrix} \\  & =\begin{bmatrix}4+(-4) & -6+12 \\ 6+(-12) & -4+0\end{bmatrix} \\  & =\begin{bmatrix}0 & 6 \\ -6 & -4\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}0 & 6 \\\\ -6 & -4\\end{bmatrix}', ':db/id': 17592186547249} 

### 17592186547248 authored
Calculate $3L+2M$, where
$L=\begin{bmatrix}4 & 4 \\ 4 & 4\end{bmatrix}$
and
$M=\begin{bmatrix}3 & 2 \\ 2 & 1\end{bmatrix}.$

Solution: We multiply each entry of $L$ by $3$ and each entry of $M$ by $2,$ and then add the resulting matrices, as follows:

$$
\begin{aligned}3L+2M & =3\begin{bmatrix}4 & 4 \\ 4 & 4\end{bmatrix}+2\begin{bmatrix}3 & 2 \\ 2 & 1\end{bmatrix} \\  & =\begin{bmatrix}3\cdot 4 & 3\cdot 4 \\ 3\cdot 4 & 3\cdot 4\end{bmatrix}+\begin{bmatrix}2\cdot 3 & 2\cdot 2 \\ 2\cdot 2 & 2\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}12 & 12 \\ 12 & 12\end{bmatrix}+\begin{bmatrix}6 & 4 \\ 4 & 2\end{bmatrix} \\  & =\begin{bmatrix}12+6 & 12+4 \\ 12+4 & 12+2\end{bmatrix} \\  & =\begin{bmatrix}18 & 16 \\ 16 & 14\end{bmatrix}\end{aligned}
$$

selection {':db/ident': ':answer-field.type/radio'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '\\begin{bmatrix}18 & 16 \\\\ 16 & 14\\end{bmatrix}', ':db/id': 17592186547251} 

### 17592186547255 authored
Calculate $4P-\frac{1}{2}H$, where
$P=\begin{bmatrix}4 & -3 & 1 & 0\end{bmatrix}$
and
$H=\begin{bmatrix}4 & 4 & 2 & 0\end{bmatrix}.$

| $4P-\frac{1}{2}H=\,\,$ |  | {{field-1}} | {{field-2}} | {{field-3}} | {{field-4}} |  |
| --- | --- | --- | --- | --- | --- | --- |

Solution: We multiply each entry of $P$ by $4$ and each entry of $H$ by $\frac{1}{2},$ and then subtract the resulting matrices, as follows:

$$
\begin{aligned}4P-\frac{1}{2}H & =4\begin{bmatrix}4 & -3 & 1 & 0\end{bmatrix}-\frac{1}{2}\begin{bmatrix}4 & 4 & 2 & 0\end{bmatrix} \\  & =\begin{bmatrix}4\cdot 4 & 4\cdot (-3) & 4\cdot 1 & 4\cdot 0\end{bmatrix}-\begin{bmatrix}\frac{1}{2}\cdot 4 & \frac{1}{2}\cdot 4 & \frac{1}{2}\cdot 2 & \frac{1}{2}\cdot 0\end{bmatrix} \\  & =\begin{bmatrix}16 & -12 & 4 & 0\end{bmatrix}-\begin{bmatrix}2 & 2 & 1 & 0\end{bmatrix} \\  & =\begin{bmatrix}16-2 & -12-2 & 4-1 & 0-0\end{bmatrix} \\  & =\begin{bmatrix}14 & -14 & 3 & 0\end{bmatrix}\end{aligned}
$$

field-4 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '0', ':db/id': 17592186547270} 
field-3 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '3', ':db/id': 17592186547250} 
field-2 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '-14', ':db/id': 17592186547274} 
field-1 {':db/ident': ':answer-field.type/blank'} => {':answer/type': {':db/ident': ':answer.type/math'}, ':answer/value': '14', ':db/id': 17592186547234} 