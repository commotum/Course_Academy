# Identifying a Triangular Matrix

Basis1356; originals are publicly parameterized raw recipes. Generated variants use complete source banks or labeled authored hard profiles.

## Original q-42090 (raw captured layout)

Which of the following matrices are upper triangular matrices?

$A=[\begin{aligned}8 & 0 & -1 & 0 \\ 0 & 0 & 0 & 7 \\ 0 & 0 & -4 & 5 \\ 0 & 0 & 0 & 1\end{aligned}],\,B=[\begin{aligned}1 & 0 & 6 \\ 0 & -1 & 3 \\ 5 & 7 & 11\end{aligned}],\,C=[\begin{aligned}2 & 0 & 1 \\ 0 & 1 & 0 \\ 0 & 3 & 0\end{aligned}].$

selection:
- $B$ only
- $B$ and $C$ only
- $C$ only
- $A$ only
- $A$ and $B$ only

selection:
- $A$ only
- $A$ and $B$ only
- $B$ and $C$ only
- $C$ only
- $B$ only

Worked solution:

The matrix $A$ is an upper triangular matrix since all the entries below the main diagonal are zeros.

The matrices $B$ and $C$ are *not* upper triangular matrices since they each have a non-zero element below the main diagonal: 

$$
\begin{aligned}{b}_{31} & =5\ne 0 \\ {c}_{32} & =3\ne 0\end{aligned}
$$

Legacy first field has no correct ref. Normal output removes that duplicate: the original MA widget is one five-choice radio. No checkbox migration.

### Generated variants of q-42090

Which of the following matrices are lower triangular matrices?

$A=[\begin{aligned}1 & 0 & 0 & 0 \\ 7 & 11 & 0 & 0 \\ 0 & 0 & 2 & 0 \\ 1 & 1 & 0 & 6\end{aligned}],\,B=[\begin{aligned}1 & 1 & -11 \\ 7 & 1 & 0 \\ 0 & -4 & 8\end{aligned}],\,C=[\begin{aligned}-10 & 0 & 0 \\ 0 & 1 & -4 \\ -6 & 0 & 5\end{aligned}].$

selection:
- $A$ and $B$ only
- $B$ and $C$ only
- $C$ only
- $A$ only
- $B$ only

Worked solution:

The matrix $A$ is an lower triangular matrix since all the entries above the main diagonal are zeros.

The matrices $B$ and $C$ are *not* lower triangular matrices since they each have a non-zero element above the main diagonal: 

$$
\begin{aligned}{b}_{12} & =1\ne 0 \\ {c}_{23} & =-4\ne 0\end{aligned}
$$

---

Which of the following matrices are upper triangular matrices?

$A=[\begin{aligned}3 & 0 & -1 & 0 \\ 0 & 6 & 0 & 7 \\ 0 & 0 & 1 & 5 \\ 0 & 0 & 0 & -11\end{aligned}],\,B=[\begin{aligned}-6 & -7 & 0 \\ 0 & 3 & 11 \\ 9 & -11 & -1\end{aligned}],\,C=[\begin{aligned}-2 & 1 & 0 \\ 0 & -4 & 0 \\ 0 & -2 & 10\end{aligned}].$

selection:
- $A$ and $B$ only
- $B$ only
- $C$ only
- $A$ only
- $B$ and $C$ only

Worked solution:

The matrix $A$ is an upper triangular matrix since all the entries below the main diagonal are zeros.

The matrices $B$ and $C$ are *not* upper triangular matrices since they each have a non-zero element below the main diagonal: 

$$
\begin{aligned}{b}_{31} & =9\ne 0 \\ {c}_{32} & =-2\ne 0\end{aligned}
$$

## Original q-68740 (raw captured layout)

Which of the following is an upper triangular matrix?

selection:
- $D=[\begin{aligned}0 & 1 \\ 1 & 0\end{aligned}]$
- $A=[\begin{aligned}1 & 0 \\ 2 & 3\end{aligned}]$
- $C=[\begin{aligned}3 & 0 & 0 \\ 0 & -5 & 1 \\ 0 & 0 & 2\end{aligned}]$
- $E=[\begin{aligned}2 & 4 & 0 \\ 4 & 0 & 4 \\ 0 & 4 & 2\end{aligned}]$
- $B=[\begin{aligned}2 & 0 & 0 \\ 0 & 5 & 0 \\ 0 & 1 & -3\end{aligned}]$

Worked solution:

Notice that $C$ is a matrix for which all entries *below* the diagonal are $0$'s:

$$
C=[\begin{aligned}3 & 0 & 0 \\ 0 & -5 & 1 \\ 0 & 0 & 2\end{aligned}]
$$

Hence, it is an upper triangular matrix. 

By contrast, matrices $A$, $B$, $D$, and $E$ each have at least one non-zero entry below the diagonal:

$$
A=[\begin{aligned}1 & 0 \\ 2 & 3\end{aligned}],\,B=[\begin{aligned}2 & 0 & 0 \\ 0 & 5 & 0 \\ 0 & 1 & -3\end{aligned}],\,D=[\begin{aligned}0 & 1 \\ 1 & 0\end{aligned}],\,E=[\begin{aligned}2 & 4 & 0 \\ 4 & 0 & 4 \\ 0 & 4 & 2\end{aligned}].
$$

So, they are not upper triangular matrices.

### Generated variants of q-68740

Which of the following is an lower triangular matrix?

selection:
- $E=[\begin{aligned}1 & 0 & -4 \\ -6 & 5 & 8 \\ -11 & 0 & -7\end{aligned}]$
- $D=[\begin{aligned}1 & -4 \\ 9 & -10\end{aligned}]$
- $C=[\begin{aligned}1 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & -11 & 6\end{aligned}]$
- $A=[\begin{aligned}1 & 7 \\ 0 & 11\end{aligned}]$
- $B=[\begin{aligned}2 & 0 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 6\end{aligned}]$

Worked solution:

Notice that $C$ is a matrix for which all entries *above* the diagonal are $0$'s:

$$
C=[\begin{aligned}1 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & -11 & 6\end{aligned}]
$$

Hence, it is an lower triangular matrix. 

By contrast, matrices $A$, $B$, $D$, and $E$ each have at least one non-zero entry above the diagonal:

$$
A=[\begin{aligned}1 & 7 \\ 0 & 11\end{aligned}],\,B=[\begin{aligned}2 & 0 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 6\end{aligned}],\,D=[\begin{aligned}1 & -4 \\ 9 & -10\end{aligned}],\,E=[\begin{aligned}1 & 0 & -4 \\ -6 & 5 & 8 \\ -11 & 0 & -7\end{aligned}].
$$

So, they are not lower triangular matrices.

---

Which of the following is an lower triangular matrix?

selection:
- $E=[\begin{aligned}0 & -4 & 0 \\ -2 & 10 & -7 \\ 0 & 9 & -9\end{aligned}]$
- $C=[\begin{aligned}-6 & 0 & 0 \\ 0 & -7 & 0 \\ 0 & 4 & 10\end{aligned}]$
- $B=[\begin{aligned}6 & 2 & 0 \\ 0 & 4 & 0 \\ 0 & 0 & -11\end{aligned}]$
- $D=[\begin{aligned}8 & -11 \\ -1 & -2\end{aligned}]$
- $A=[\begin{aligned}3 & -1 \\ 0 & 6\end{aligned}]$

Worked solution:

Notice that $C$ is a matrix for which all entries *above* the diagonal are $0$'s:

$$
C=[\begin{aligned}-6 & 0 & 0 \\ 0 & -7 & 0 \\ 0 & 4 & 10\end{aligned}]
$$

Hence, it is an lower triangular matrix. 

By contrast, matrices $A$, $B$, $D$, and $E$ each have at least one non-zero entry above the diagonal:

$$
A=[\begin{aligned}3 & -1 \\ 0 & 6\end{aligned}],\,B=[\begin{aligned}6 & 2 & 0 \\ 0 & 4 & 0 \\ 0 & 0 & -11\end{aligned}],\,D=[\begin{aligned}8 & -11 \\ -1 & -2\end{aligned}],\,E=[\begin{aligned}0 & -4 & 0 \\ -2 & 10 & -7 \\ 0 & 9 & -9\end{aligned}].
$$

So, they are not lower triangular matrices.

## Original q-126351 (raw captured layout)

Which of the following matrices are lower triangular matrices?

$A=[\begin{aligned}1 & 0 \\ 0 & 1\end{aligned}],\,B=[\begin{aligned}5 & 0 \\ -1 & 2\end{aligned}],\,C=[\begin{aligned}1 & -2 \\ 0 & 5\end{aligned}].$

selection:
- $C$ only
- $A$ and $C$ only
- $B$ only
- $A$ and $B$ only
- $A$, $B$, and $C$

Worked solution:

The matrices $A$ and $B$ are lower triangular matrices since all the entries above the main diagonal are zeros.

The matrix $C$ is *not* a lower triangular matrix since it has a non-zero element above the main diagonal: 

$$
\begin{aligned}{c}_{12} & =-2\ne 0\end{aligned}
$$

### Generated variants of q-126351

Which of the following matrices are upper triangular matrices?

$A=[\begin{aligned}1 & 0 \\ 0 & 6\end{aligned}],\,B=[\begin{aligned}11 & 3 \\ 0 & 0\end{aligned}],\,C=[\begin{aligned}0 & 0 \\ 7 & 1\end{aligned}].$

selection:
- $A$, $B$, and $C$
- $A$ and $C$ only
- $A$ and $B$ only
- $B$ only
- $C$ only

Worked solution:

The matrices $A$ and $B$ are upper triangular matrices since all the entries below the main diagonal are zeros.

The matrix $C$ is *not* a upper triangular matrix since it has a non-zero element below the main diagonal: 

$$
\begin{aligned}{c}_{21} & =7\ne 0\end{aligned}
$$

---

Which of the following matrices are upper triangular matrices?

$A=[\begin{aligned}-1 & 0 \\ 0 & 6\end{aligned}],\,B=[\begin{aligned}6 & 2 \\ 0 & 4\end{aligned}],\,C=[\begin{aligned}-11 & 0 \\ -6 & -7\end{aligned}].$

selection:
- $A$ and $B$ only
- $C$ only
- $A$ and $C$ only
- $B$ only
- $A$, $B$, and $C$

Worked solution:

The matrices $A$ and $B$ are upper triangular matrices since all the entries below the main diagonal are zeros.

The matrix $C$ is *not* a upper triangular matrix since it has a non-zero element below the main diagonal: 

$$
\begin{aligned}{c}_{21} & =-6\ne 0\end{aligned}
$$

## Original q-126352 (raw captured layout)

Which of the following is an upper triangular matrix?

selection:
- $B=[\begin{aligned}-1 & 0 & 0 \\ 0 & 5 & 0 \\ 2 & 0 & 1\end{aligned}]$
- $C=[\begin{aligned}0 & -1 \\ 5 & 1\end{aligned}]$
- $D=[\begin{aligned}-2 & 6 & 0 \\ 0 & 1 & -1 \\ 0 & 0 & 2\end{aligned}]$
- $E=[\begin{aligned}-1 & 4 & 0 \\ 3 & 0 & 2 \\ 4 & 0 & 2\end{aligned}]$
- $A=[\begin{aligned}4 & 0 \\ 1 & 1\end{aligned}]$

Worked solution:

Notice that $D$ is a matrix for which all entries *below* the diagonal are $0$'s:

$$
D=[\begin{aligned}-2 & 6 & 0 \\ 0 & 1 & -1 \\ 0 & 0 & 2\end{aligned}]
$$

Hence, it is an upper triangular matrix. 

By contrast, matrices $A$, $B$, $C$, and $E$ each have at least one non-zero entry below the diagonal:

$$
A=[\begin{aligned}4 & 0 \\ 1 & 1\end{aligned}],\,B=[\begin{aligned}-1 & 0 & 0 \\ 0 & 5 & 0 \\ 2 & 0 & 1\end{aligned}],\,C=[\begin{aligned}0 & -1 \\ 5 & 1\end{aligned}],\,E=[\begin{aligned}-1 & 4 & 0 \\ 3 & 0 & 2 \\ 4 & 0 & 2\end{aligned}].
$$

So, they are not upper triangular matrices.

### Generated variants of q-126352

Which of the following is an upper triangular matrix?

selection:
- $A=[\begin{aligned}1 & 0 \\ 7 & 11\end{aligned}]$
- $B=[\begin{aligned}2 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 1 & 6\end{aligned}]$
- $D=[\begin{aligned}1 & -4 & 0 \\ 0 & 8 & -10 \\ 0 & 0 & 1\end{aligned}]$
- $C=[\begin{aligned}1 & 1 \\ -11 & 6\end{aligned}]$
- $E=[\begin{aligned}-4 & -6 & 0 \\ 0 & 5 & 8 \\ -11 & -7 & 3\end{aligned}]$

Worked solution:

Notice that $D$ is a matrix for which all entries *below* the diagonal are $0$'s:

$$
D=[\begin{aligned}1 & -4 & 0 \\ 0 & 8 & -10 \\ 0 & 0 & 1\end{aligned}]
$$

Hence, it is an upper triangular matrix. 

By contrast, matrices $A$, $B$, $C$, and $E$ each have at least one non-zero entry below the diagonal:

$$
A=[\begin{aligned}1 & 0 \\ 7 & 11\end{aligned}],\,B=[\begin{aligned}2 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 1 & 6\end{aligned}],\,C=[\begin{aligned}1 & 1 \\ -11 & 6\end{aligned}],\,E=[\begin{aligned}-4 & -6 & 0 \\ 0 & 5 & 8 \\ -11 & -7 & 3\end{aligned}].
$$

So, they are not upper triangular matrices.

---

Which of the following is an lower triangular matrix?

selection:
- $C=[\begin{aligned}-6 & -7 \\ 4 & 10\end{aligned}]$
- $D=[\begin{aligned}8 & 0 & 0 \\ -11 & -1 & 0 \\ -2 & 0 & 0\end{aligned}]$
- $A=[\begin{aligned}3 & -1 \\ 0 & 6\end{aligned}]$
- $B=[\begin{aligned}6 & 0 & 0 \\ 0 & 1 & 5 \\ 0 & 0 & -11\end{aligned}]$
- $E=[\begin{aligned}-4 & -2 & 11 \\ 0 & -7 & 0 \\ 9 & -9 & -5\end{aligned}]$

Worked solution:

Notice that $D$ is a matrix for which all entries *above* the diagonal are $0$'s:

$$
D=[\begin{aligned}8 & 0 & 0 \\ -11 & -1 & 0 \\ -2 & 0 & 0\end{aligned}]
$$

Hence, it is an lower triangular matrix. 

By contrast, matrices $A$, $B$, $C$, and $E$ each have at least one non-zero entry above the diagonal:

$$
A=[\begin{aligned}3 & -1 \\ 0 & 6\end{aligned}],\,B=[\begin{aligned}6 & 0 & 0 \\ 0 & 1 & 5 \\ 0 & 0 & -11\end{aligned}],\,C=[\begin{aligned}-6 & -7 \\ 4 & 10\end{aligned}],\,E=[\begin{aligned}-4 & -2 & 11 \\ 0 & -7 & 0 \\ 9 & -9 & -5\end{aligned}].
$$

So, they are not lower triangular matrices.

## Original q-126354 (raw captured layout)

Which of the following is an upper triangular matrix?

selection:
- $D=[\begin{aligned}2 & 1 \\ 1 & 2\end{aligned}]$
- $B=[\begin{aligned}2 & 0 \\ 1 & 1\end{aligned}]$
- $C=[\begin{aligned}6 & 7 \\ -2 & 1\end{aligned}]$
- $A=[\begin{aligned}9 & 0 \\ -1 & 1\end{aligned}]$
- $E=[\begin{aligned}1 & -3 \\ 0 & 5\end{aligned}]$

Worked solution:

Notice that $E$ is a matrix for which all entries *below* the diagonal are $0$'s:

$$
E=[\begin{aligned}1 & -3 \\ 0 & 5\end{aligned}]
$$

Hence, it is an upper triangular matrix. 

By contrast, matrices $A$, $B$, $C$, and $D$ each have at least one non-zero entry below the diagonal:

$$
A=[\begin{aligned}9 & 0 \\ -1 & 1\end{aligned}],\,B=[\begin{aligned}2 & 0 \\ 1 & 1\end{aligned}],\,C=[\begin{aligned}6 & 7 \\ -2 & 1\end{aligned}],\,D=[\begin{aligned}2 & 1 \\ 1 & 2\end{aligned}].
$$

So, they are not upper triangular matrices.

### Generated variants of q-126354

Which of the following is an upper triangular matrix?

selection:
- $D=[\begin{aligned}6 & 2 \\ -4 & 8\end{aligned}]$
- $A=[\begin{aligned}1 & 0 \\ 7 & 11\end{aligned}]$
- $E=[\begin{aligned}-10 & 2 \\ 0 & -4\end{aligned}]$
- $C=[\begin{aligned}6 & 2 \\ 1 & -11\end{aligned}]$
- $B=[\begin{aligned}2 & 0 \\ 1 & 0\end{aligned}]$

Worked solution:

Notice that $E$ is a matrix for which all entries *below* the diagonal are $0$'s:

$$
E=[\begin{aligned}-10 & 2 \\ 0 & -4\end{aligned}]
$$

Hence, it is an upper triangular matrix. 

By contrast, matrices $A$, $B$, $C$, and $D$ each have at least one non-zero entry below the diagonal:

$$
A=[\begin{aligned}1 & 0 \\ 7 & 11\end{aligned}],\,B=[\begin{aligned}2 & 0 \\ 1 & 0\end{aligned}],\,C=[\begin{aligned}6 & 2 \\ 1 & -11\end{aligned}],\,D=[\begin{aligned}6 & 2 \\ -4 & 8\end{aligned}].
$$

So, they are not upper triangular matrices.

---

Which of the following is an upper triangular matrix?

selection:
- $D=[\begin{aligned}8 & -11 \\ -1 & -2\end{aligned}]$
- $A=[\begin{aligned}-1 & 0 \\ 7 & 6\end{aligned}]$
- $E=[\begin{aligned}0 & -4 \\ 0 & -2\end{aligned}]$
- $C=[\begin{aligned}-6 & -7 \\ 4 & 10\end{aligned}]$
- $B=[\begin{aligned}1 & 0 \\ 5 & -11\end{aligned}]$

Worked solution:

Notice that $E$ is a matrix for which all entries *below* the diagonal are $0$'s:

$$
E=[\begin{aligned}0 & -4 \\ 0 & -2\end{aligned}]
$$

Hence, it is an upper triangular matrix. 

By contrast, matrices $A$, $B$, $C$, and $D$ each have at least one non-zero entry below the diagonal:

$$
A=[\begin{aligned}-1 & 0 \\ 7 & 6\end{aligned}],\,B=[\begin{aligned}1 & 0 \\ 5 & -11\end{aligned}],\,C=[\begin{aligned}-6 & -7 \\ 4 & 10\end{aligned}],\,D=[\begin{aligned}8 & -11 \\ -1 & -2\end{aligned}].
$$

So, they are not upper triangular matrices.

## Original q-13760 (raw captured layout)

Which of the following is an upper triangular matrix?

selection:
- $C=[\begin{aligned}0 & 1 & 0 \\ -1 & 2 & 3 \\ 0 & -3 & 0\end{aligned}]$
- $A=[\begin{aligned}0 & 1 & 0 \\ 0 & 2 & 3 \\ 0 & 0 & 0\end{aligned}]$
- $E=[\begin{aligned}1 & 0 \\ 1 & 1\end{aligned}]$
- $B=[\begin{aligned}2 & 0 & 0 \\ 0 & 2 & 0 \\ -5 & 0 & 0\end{aligned}]$
- $D=[\begin{aligned}1 & 1 \\ 1 & 1\end{aligned}]$

Worked solution:

Notice that $A$ is a matrix for which all entries *below* the diagonal are $0$'s:

$$
A=[\begin{aligned}0 & 1 & 0 \\ 0 & 2 & 3 \\ 0 & 0 & 0\end{aligned}]
$$

Hence, it is an upper triangular matrix. 

By contrast, matrices $B$, $C$, $D$, and $E$ each have at least one non-zero entry below the diagonal:

$$
B=[\begin{aligned}2 & 0 & 0 \\ 0 & 2 & 0 \\ -5 & 0 & 0\end{aligned}],\,C=[\begin{aligned}0 & 1 & 0 \\ -1 & 2 & 3 \\ 0 & -3 & 0\end{aligned}],\,D=[\begin{aligned}1 & 1 \\ 1 & 1\end{aligned}],\,E=[\begin{aligned}1 & 0 \\ 1 & 1\end{aligned}].
$$

So, they are not upper triangular matrices.

### Generated variants of q-13760

Which of the following is an upper triangular matrix?

selection:
- $C=[\begin{aligned}6 & 2 & -4 \\ 9 & -10 & 0 \\ 2 & 0 & -4\end{aligned}]$
- $D=[\begin{aligned}-6 & 6 \\ 8 & -11\end{aligned}]$
- $E=[\begin{aligned}-7 & 0 \\ 4 & 8\end{aligned}]$
- $B=[\begin{aligned}6 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 1 & -11\end{aligned}]$
- $A=[\begin{aligned}1 & 7 & 3 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{aligned}]$

Worked solution:

Notice that $A$ is a matrix for which all entries *below* the diagonal are $0$'s:

$$
A=[\begin{aligned}1 & 7 & 3 \\ 0 & 0 & 0 \\ 0 & 0 & 0\end{aligned}]
$$

Hence, it is an upper triangular matrix. 

By contrast, matrices $B$, $C$, $D$, and $E$ each have at least one non-zero entry below the diagonal:

$$
B=[\begin{aligned}6 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 1 & -11\end{aligned}],\,C=[\begin{aligned}6 & 2 & -4 \\ 9 & -10 & 0 \\ 2 & 0 & -4\end{aligned}],\,D=[\begin{aligned}-6 & 6 \\ 8 & -11\end{aligned}],\,E=[\begin{aligned}-7 & 0 \\ 4 & 8\end{aligned}].
$$

So, they are not upper triangular matrices.

---

Which of the following is an lower triangular matrix?

selection:
- $A=[\begin{aligned}3 & 0 & 0 \\ 0 & -1 & 0 \\ 7 & 7 & 1\end{aligned}]$
- $E=[\begin{aligned}8 & -9 \\ 0 & -5\end{aligned}]$
- $D=[\begin{aligned}-4 & -2 \\ 11 & -7\end{aligned}]$
- $C=[\begin{aligned}3 & 11 & 9 \\ -11 & -1 & 0 \\ 0 & -2 & 0\end{aligned}]$
- $B=[\begin{aligned}4 & -11 & 0 \\ 0 & -6 & 0 \\ 0 & 0 & -7\end{aligned}]$

Worked solution:

Notice that $A$ is a matrix for which all entries *above* the diagonal are $0$'s:

$$
A=[\begin{aligned}3 & 0 & 0 \\ 0 & -1 & 0 \\ 7 & 7 & 1\end{aligned}]
$$

Hence, it is an lower triangular matrix. 

By contrast, matrices $B$, $C$, $D$, and $E$ each have at least one non-zero entry above the diagonal:

$$
B=[\begin{aligned}4 & -11 & 0 \\ 0 & -6 & 0 \\ 0 & 0 & -7\end{aligned}],\,C=[\begin{aligned}3 & 11 & 9 \\ -11 & -1 & 0 \\ 0 & -2 & 0\end{aligned}],\,D=[\begin{aligned}-4 & -2 \\ 11 & -7\end{aligned}],\,E=[\begin{aligned}8 & -9 \\ 0 & -5\end{aligned}].
$$

So, they are not lower triangular matrices.

## Original q-126353 (raw captured layout)

Which of the following is an upper triangular matrix?

selection:
- $E=[\begin{aligned}4 & 1 & 0 \\ -1 & 0 & 2 \\ 1 & 0 & 2\end{aligned}]$
- $C=[\begin{aligned}3 & 0 & 0 \\ 2 & 5 & 0 \\ 1 & 0 & -5\end{aligned}]$
- $B=[\begin{aligned}-2 & 0 \\ -3 & 5\end{aligned}]$
- $D=[\begin{aligned}0 & -2 \\ 7 & 2\end{aligned}]$
- $A=[\begin{aligned}1 & -3 \\ 0 & 5\end{aligned}]$

Worked solution:

Notice that $A$ is a matrix for which all entries *below* the diagonal are $0$'s:

$$
A=[\begin{aligned}1 & -3 \\ 0 & 5\end{aligned}]
$$

Hence, it is an upper triangular matrix. 

By contrast, matrices $B$, $C$, $D$, and $E$ each have at least one non-zero entry below the diagonal:

$$
B=[\begin{aligned}-2 & 0 \\ -3 & 5\end{aligned}],\,C=[\begin{aligned}3 & 0 & 0 \\ 2 & 5 & 0 \\ 1 & 0 & -5\end{aligned}],\,D=[\begin{aligned}0 & -2 \\ 7 & 2\end{aligned}],\,E=[\begin{aligned}4 & 1 & 0 \\ -1 & 0 & 2 \\ 1 & 0 & 2\end{aligned}].
$$

So, they are not upper triangular matrices.

### Generated variants of q-126353

Which of the following is an upper triangular matrix?

selection:
- $D=[\begin{aligned}1 & -4 \\ 9 & -10\end{aligned}]$
- $E=[\begin{aligned}1 & -4 & -6 \\ 0 & 5 & 0 \\ 8 & -11 & -7\end{aligned}]$
- $B=[\begin{aligned}2 & 0 \\ 1 & 0\end{aligned}]$
- $C=[\begin{aligned}6 & 0 & 0 \\ 0 & 1 & 0 \\ 1 & -11 & 6\end{aligned}]$
- $A=[\begin{aligned}1 & 7 \\ 0 & 11\end{aligned}]$

Worked solution:

Notice that $A$ is a matrix for which all entries *below* the diagonal are $0$'s:

$$
A=[\begin{aligned}1 & 7 \\ 0 & 11\end{aligned}]
$$

Hence, it is an upper triangular matrix. 

By contrast, matrices $B$, $C$, $D$, and $E$ each have at least one non-zero entry below the diagonal:

$$
B=[\begin{aligned}2 & 0 \\ 1 & 0\end{aligned}],\,C=[\begin{aligned}6 & 0 & 0 \\ 0 & 1 & 0 \\ 1 & -11 & 6\end{aligned}],\,D=[\begin{aligned}1 & -4 \\ 9 & -10\end{aligned}],\,E=[\begin{aligned}1 & -4 & -6 \\ 0 & 5 & 0 \\ 8 & -11 & -7\end{aligned}].
$$

So, they are not upper triangular matrices.

---

Which of the following is an lower triangular matrix?

selection:
- $D=[\begin{aligned}8 & -11 \\ -1 & -2\end{aligned}]$
- $B=[\begin{aligned}6 & 2 \\ 0 & 4\end{aligned}]$
- $A=[\begin{aligned}3 & 0 \\ -1 & 6\end{aligned}]$
- $E=[\begin{aligned}0 & 0 & -4 \\ -2 & 10 & -7 \\ 0 & 9 & -9\end{aligned}]$
- $C=[\begin{aligned}-11 & 0 & -6 \\ 0 & -7 & 4 \\ 0 & 0 & 10\end{aligned}]$

Worked solution:

Notice that $A$ is a matrix for which all entries *above* the diagonal are $0$'s:

$$
A=[\begin{aligned}3 & 0 \\ -1 & 6\end{aligned}]
$$

Hence, it is an lower triangular matrix. 

By contrast, matrices $B$, $C$, $D$, and $E$ each have at least one non-zero entry above the diagonal:

$$
B=[\begin{aligned}6 & 2 \\ 0 & 4\end{aligned}],\,C=[\begin{aligned}-11 & 0 & -6 \\ 0 & -7 & 4 \\ 0 & 0 & 10\end{aligned}],\,D=[\begin{aligned}8 & -11 \\ -1 & -2\end{aligned}],\,E=[\begin{aligned}0 & 0 & -4 \\ -2 & 10 & -7 \\ 0 & 9 & -9\end{aligned}].
$$

So, they are not lower triangular matrices.

## Original q-74316 (raw captured layout)

Which of the following is a lower triangular matrix?

selection:
- $A=[\begin{aligned}0 & 0 & 1 \\ 0 & 4 & 0 \\ 0 & 0 & 3\end{aligned}]$
- $D=[\begin{aligned}2 & -3 \\ 0 & 3\end{aligned}]$
- $C=[\begin{aligned}0 & 1 \\ 0 & 0\end{aligned}]$
- $B=[\begin{aligned}0 & 0 & 0 \\ 2 & 5 & 0 \\ 1 & 4 & 3\end{aligned}]$
- $E=[\begin{aligned}0 & -4 & 0 \\ 5 & 0 & -7 \\ 1 & 2 & 0\end{aligned}]$

Worked solution:

Notice that $B$ is a matrix for which all entries *above* the diagonal are $0$'s:

$$
B=[\begin{aligned}0 & 0 & 0 \\ 2 & 5 & 0 \\ 1 & 4 & 3\end{aligned}]
$$

Hence, it is a lower triangular matrix. 

By contrast, matrices $A$, $C$, $D$, and $E$ each have at least one non-zero entry above the diagonal:

$$
A=[\begin{aligned}0 & 0 & 1 \\ 0 & 4 & 0 \\ 0 & 0 & 3\end{aligned}],\,C=[\begin{aligned}0 & 1 \\ 0 & 0\end{aligned}],\,D=[\begin{aligned}2 & -3 \\ 0 & 3\end{aligned}],\,E=[\begin{aligned}0 & -4 & 0 \\ 5 & 0 & -7 \\ 1 & 2 & 0\end{aligned}].
$$

So, they are not lower triangular matrices.

### Generated variants of q-74316

Which of the following is a lower triangular matrix?

selection:
- $A=[\begin{aligned}1 & 7 & 0 \\ 0 & 11 & 0 \\ 0 & 0 & 2\end{aligned}]$
- $E=[\begin{aligned}-4 & -6 & 0 \\ 6 & 7 & -11 \\ -7 & 4 & 8\end{aligned}]$
- $C=[\begin{aligned}6 & 2 \\ 0 & -4\end{aligned}]$
- $B=[\begin{aligned}0 & 0 & 0 \\ 1 & 6 & 0 \\ 2 & 1 & -11\end{aligned}]$
- $D=[\begin{aligned}8 & -10 \\ 0 & 1\end{aligned}]$

Worked solution:

Notice that $B$ is a matrix for which all entries *above* the diagonal are $0$'s:

$$
B=[\begin{aligned}0 & 0 & 0 \\ 1 & 6 & 0 \\ 2 & 1 & -11\end{aligned}]
$$

Hence, it is a lower triangular matrix. 

By contrast, matrices $A$, $C$, $D$, and $E$ each have at least one non-zero entry above the diagonal:

$$
A=[\begin{aligned}1 & 7 & 0 \\ 0 & 11 & 0 \\ 0 & 0 & 2\end{aligned}],\,C=[\begin{aligned}6 & 2 \\ 0 & -4\end{aligned}],\,D=[\begin{aligned}8 & -10 \\ 0 & 1\end{aligned}],\,E=[\begin{aligned}-4 & -6 & 0 \\ 6 & 7 & -11 \\ -7 & 4 & 8\end{aligned}].
$$

So, they are not lower triangular matrices.

---

Which of the following is a upper triangular matrix?

selection:
- $C=[\begin{aligned}10 & 0 \\ 9 & -11\end{aligned}]$
- $E=[\begin{aligned}-4 & -2 & 11 \\ 0 & -7 & 9 \\ -9 & -5 & 5\end{aligned}]$
- $B=[\begin{aligned}1 & 5 & -11 \\ 0 & -6 & -7 \\ 0 & 0 & 3\end{aligned}]$
- $D=[\begin{aligned}-1 & 0 \\ -2 & 0\end{aligned}]$
- $A=[\begin{aligned}3 & 0 & 0 \\ -1 & 6 & 0 \\ 0 & 0 & 6\end{aligned}]$

Worked solution:

Notice that $B$ is a matrix for which all entries *below* the diagonal are $0$'s:

$$
B=[\begin{aligned}1 & 5 & -11 \\ 0 & -6 & -7 \\ 0 & 0 & 3\end{aligned}]
$$

Hence, it is a upper triangular matrix. 

By contrast, matrices $A$, $C$, $D$, and $E$ each have at least one non-zero entry below the diagonal:

$$
A=[\begin{aligned}3 & 0 & 0 \\ -1 & 6 & 0 \\ 0 & 0 & 6\end{aligned}],\,C=[\begin{aligned}10 & 0 \\ 9 & -11\end{aligned}],\,D=[\begin{aligned}-1 & 0 \\ -2 & 0\end{aligned}],\,E=[\begin{aligned}-4 & -2 & 11 \\ 0 & -7 & 9 \\ -9 & -5 & 5\end{aligned}].
$$

So, they are not upper triangular matrices.

## Authored hard extension: hard_two

Which of the following matrices are lower triangular matrices?

$A=[\begin{aligned}1 & 0 & 0 & 0 \\ 0 & 6 & 0 & 0 \\ 0 & 0 & 11 & 0 \\ 0 & 0 & 0 & 2\end{aligned}],\,B=[\begin{aligned}0 & 0 & 0 & 0 \\ 1 & 6 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & -11 & 6\end{aligned}],\,C=[\begin{aligned}1 & -4 & 0 & 0 \\ 0 & 8 & 0 & 0 \\ -10 & 2 & -4 & 0 \\ -6 & 0 & 0 & 5\end{aligned}],\,D=[\begin{aligned}7 & 0 & 0 & 0 \\ 0 & -11 & 0 & 0 \\ -7 & 4 & 8 & -7 \\ 0 & -6 & 0 & -4\end{aligned}],\,E=[\begin{aligned}0 & 0 & 0 & 0 \\ 1 & 7 & -6 & 0 \\ 10 & -5 & -3 & 0 \\ 0 & 0 & 0 & -3\end{aligned}].$

selection:
- $A$ only
- $A$, $B$, and $C$ only
- $A$ and $C$ only
- $B$ only
- $A$ and $B$ only

Worked solution:

The matrices $A$ and $B$ are lower triangular matrices since all the entries above the main diagonal are zeros.

The matrices $C$ and $D$ and $E$ are *not* lower triangular matrices since they each have a non-zero element above the main diagonal: 

$$
\begin{aligned}{c}_{12} & =-4\ne 0 \\ {d}_{34} & =-7\ne 0 \\ {e}_{23} & =-6\ne 0\end{aligned}
$$

---

Which of the following matrices are upper triangular matrices?

$A=[\begin{aligned}3 & 0 & 0 & 0 \\ 0 & -1 & 0 & 0 \\ 0 & 0 & 6 & 0 \\ 0 & 0 & 0 & 6\end{aligned}],\,B=[\begin{aligned}1 & 0 & 5 & 0 \\ 0 & -11 & -6 & -7 \\ 0 & 0 & 3 & 0 \\ 0 & 0 & 0 & 10\end{aligned}],\,C=[\begin{aligned}8 & 0 & -11 & -1 \\ 0 & -2 & 1 & 0 \\ 0 & 0 & -4 & 0 \\ -2 & 0 & 0 & 10\end{aligned}],\,D=[\begin{aligned}-7 & 9 & 0 & -9 \\ 0 & -5 & 0 & 6 \\ -2 & 0 & 7 & 0 \\ 0 & 0 & 0 & 6\end{aligned}],\,E=[\begin{aligned}-6 & 0 & 0 & -1 \\ 0 & -6 & 2 & -4 \\ 0 & 0 & 9 & 0 \\ 0 & 0 & 4 & -4\end{aligned}].$

selection:
- $A$ and $C$ only
- $A$ only
- $B$ only
- $A$ and $B$ only
- $A$, $B$, and $C$ only

Worked solution:

The matrices $A$ and $B$ are upper triangular matrices since all the entries below the main diagonal are zeros.

The matrices $C$ and $D$ and $E$ are *not* upper triangular matrices since they each have a non-zero element below the main diagonal: 

$$
\begin{aligned}{c}_{41} & =-2\ne 0 \\ {d}_{31} & =-2\ne 0 \\ {e}_{43} & =4\ne 0\end{aligned}
$$

## Authored hard extension: hard_three

Which of the following matrices are lower triangular matrices?

$A=[\begin{aligned}1 & 0 & 0 & 0 \\ 0 & 6 & 0 & 0 \\ 0 & 0 & 11 & 0 \\ 0 & 0 & 0 & 2\end{aligned}],\,B=[\begin{aligned}0 & 0 & 0 & 0 \\ 1 & 6 & 0 & 0 \\ 2 & 0 & 0 & 0 \\ -11 & 0 & 0 & 6\end{aligned}],\,C=[\begin{aligned}1 & 0 & 0 & 0 \\ -4 & 8 & 0 & 0 \\ -10 & 0 & 1 & 0 \\ 0 & -4 & 0 & -6\end{aligned}],\,D=[\begin{aligned}5 & 0 & 0 & 0 \\ 0 & 7 & 0 & 0 \\ 0 & -11 & -7 & 4 \\ 9 & 0 & -7 & -6\end{aligned}],\,E=[\begin{aligned}-4 & 0 & 0 & 0 \\ 1 & 0 & 0 & 8 \\ -6 & 0 & 9 & 0 \\ 0 & 0 & -5 & -3\end{aligned}].$

selection:
- $A$, $C$, and $E$ only
- $A$, $B$, $C$, and $D$ only
- $A$ and $B$ only
- $A$, $B$, and $C$ only
- $B$ and $C$ only

Worked solution:

The matrices $A$, $B$ and $C$ are lower triangular matrices since all the entries above the main diagonal are zeros.

The matrices $D$ and $E$ are *not* lower triangular matrices since they each have a non-zero element above the main diagonal: 

$$
\begin{aligned}{d}_{34} & =4\ne 0 \\ {e}_{24} & =8\ne 0\end{aligned}
$$

---

Which of the following matrices are lower triangular matrices?

$A=[\begin{aligned}3 & 0 & 0 & 0 \\ 0 & -1 & 0 & 0 \\ 0 & 0 & 6 & 0 \\ 0 & 0 & 0 & 6\end{aligned}],\,B=[\begin{aligned}1 & 0 & 0 & 0 \\ 0 & 4 & 0 & 0 \\ -11 & 0 & -6 & 0 \\ -7 & 4 & 0 & 10\end{aligned}],\,C=[\begin{aligned}8 & 0 & 0 & 0 \\ -11 & -1 & 0 & 0 \\ 0 & -2 & 0 & 0 \\ 0 & -4 & 0 & -2\end{aligned}],\,D=[\begin{aligned}10 & 0 & 0 & 0 \\ 0 & -7 & 9 & 0 \\ 0 & -9 & -5 & 0 \\ 6 & 0 & -2 & 7\end{aligned}],\,E=[\begin{aligned}6 & -6 & 0 & 0 \\ 0 & 11 & 0 & 0 \\ 0 & 0 & -1 & 0 \\ -6 & 2 & -4 & 9\end{aligned}].$

selection:
- $A$, $B$, and $C$ only
- $A$, $C$, and $E$ only
- $B$ and $C$ only
- $A$ and $B$ only
- $A$, $B$, $C$, and $D$ only

Worked solution:

The matrices $A$, $B$ and $C$ are lower triangular matrices since all the entries above the main diagonal are zeros.

The matrices $D$ and $E$ are *not* lower triangular matrices since they each have a non-zero element above the main diagonal: 

$$
\begin{aligned}{d}_{23} & =9\ne 0 \\ {e}_{12} & =-6\ne 0\end{aligned}
$$
