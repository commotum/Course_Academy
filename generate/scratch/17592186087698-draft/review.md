# Matrix classification draft review

Source originals are retained in full in review.json. Raw missing-key records are evidence-only. Generated moderate/hard labels are authored inspection bands.

## Original replay q-7831

Which of the following are row vectors?
$E = \begin{bmatrix}-1 \\ 0 \\ 0 \\ -3 \\ \sqrt{2}\end{bmatrix}, F = \begin{bmatrix}2 & 5 & 6 & -2 & 0\end{bmatrix}, G = \begin{bmatrix}2 & 5 \\ 2 & 5\end{bmatrix}$

selection: $E$ only, $E$ and $G$ only, $E$ and $F$ only, $F$ only, $G$ only

Original has no key or worked solution.

## Authored key and solution q-7831

Which of the following are row vectors?
$E = \begin{bmatrix}-1 \\ 0 \\ 0 \\ -3 \\ \sqrt{2}\end{bmatrix}, F = \begin{bmatrix}2 & 5 & 6 & -2 & 0\end{bmatrix}, G = \begin{bmatrix}2 & 5 \\ 2 & 5\end{bmatrix}$

selection: $E$ only, $E$ and $G$ only, $E$ and $F$ only, $F$ only, $G$ only

- $E$ is *not* a row vector. It has only one column (and $5$ rows), so it's a column vector.

- $F$ is a row vector since it has only one row.

- $G$ is *not* a row vector, since it has more than $1$ row (it has $2$ rows).

Therefore, only $F$ is a row vector.

## Original replay q-7836

Which of the following best describes the following matrix $M$?
$M = \begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 1\end{bmatrix}$

selection: An identity matrix, A zero matrix, A row vector, A column vector, Other

Original has no key or worked solution.

## Authored key and solution q-7836

Which of the following best describes the following matrix $M$?
$M = \begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 0 & 1\end{bmatrix}$

selection: An identity matrix, A zero matrix, A row vector, A column vector, Other

The matrix has no special name.

## Original replay q-11563

Which of the following best describes the following matrix $A?$

$$
A=\begin{bmatrix}1 & 2 & 3\end{bmatrix}
$$

selection: An identity matrix, A zero matrix, A row vector, A column vector, A square matrix

The matrix has only one row. Hence, it is a row vector.

## Original replay q-126293

Which of the following best describes the following matrix $P?$

$$
P=\begin{bmatrix}1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & -1 & 0 \\ 0 & 0 & 0 & -1\end{bmatrix}
$$

selection: An identity matrix, A column matrix, A diagonal matrix, A row vector, Other

The matrix is square, all the entries that do not lie on the main diagonal are zeros, and the diagonal entries are not all ones. 

Hence it's a diagonal matrix.

## Original replay q-68751

Which of the following are row vectors?

$$
A=\begin{bmatrix}0 & 1 & 3 & -2 & 9 \\ 1 & 2 & 0 & 4 & 1\end{bmatrix},\,B=\begin{bmatrix}3 \\ -2 \\ 0 \\ 6\end{bmatrix},\,C=\begin{bmatrix}3 & 10\end{bmatrix}
$$

Select all that apply.

A: false, true; B: false, true; C: true, false

- $A$ is *not* a row vector, since it has more than $1$ row (it has $2$ rows).

- $B$ is *not* a row vector. It has only one column (and $4$ rows), so it's a column vector.

- $C$ is a row vector since it has only one row.

Therefore, only $C$ is a row vector.

## Original replay q-7830

Which of the following best describes the following matrix $E?$

$$
E=\begin{bmatrix}1 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0\end{bmatrix}
$$

selection: An identity matrix, Other, A square matrix, A zero matrix, A row vector

The matrix has no special name.

## Original replay q-126287

Which of the following are column vectors?

$$
A=\begin{bmatrix}-2 & 0\end{bmatrix},\,B=\begin{bmatrix}2 \\ 0 \\ 0\end{bmatrix},\,C=\begin{bmatrix}1 & -3 \\ -2 & 1\end{bmatrix}
$$

Select all that apply. If none apply, leave all boxes unchecked.

A: false, true; B: false, true; C: true, false

- $A$ is *not* a column vector. It has only one row (and $2$ columns), so it's a row vector.

- $B$ is a column vector since it has only one column.

- $C$ is *not* a column vector, since it has more than $1$ column (it has $2$ columns).

Therefore, only $B$ is a column vector.

## Generated easy row seed 2

Which of the following best describes the following matrix $A?$

$$
A=\begin{bmatrix}2 & 3\end{bmatrix}
$$

selection: A square matrix, A row vector, A column vector, An identity matrix, A zero matrix

The matrix has only one row. Hence, it is a row vector.

## Generated easy row seed 57

Which of the following best describes the following matrix $F?$

$$
F=\begin{bmatrix}2 & -3 & -2 & 1 & -1 & 0\end{bmatrix}
$$

selection: A row vector, A zero matrix, A column vector, A square matrix, An identity matrix

The matrix has only one row. Hence, it is a row vector.

## Generated easy diagonal seed 2

Which of the following best describes the following matrix $A?$

$$
A=\begin{bmatrix}-1 & 0 \\ 0 & 0\end{bmatrix}
$$

selection: A column matrix, Other, An identity matrix, A diagonal matrix, A row vector

The matrix is square, all the entries that do not lie on the main diagonal are zeros, and the diagonal entries are not all ones. 

Hence it's a diagonal matrix.

## Generated easy diagonal seed 57

Which of the following best describes the following matrix $F?$

$$
F=\begin{bmatrix}2 & 0 & 0 & 0 & 0 & 0 \\ 0 & -1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 2 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & -1 & 0 \\ 0 & 0 & 0 & 0 & 0 & -1\end{bmatrix}
$$

selection: A column matrix, A diagonal matrix, A row vector, An identity matrix, Other

The matrix is square, all the entries that do not lie on the main diagonal are zeros, and the diagonal entries are not all ones. 

Hence it's a diagonal matrix.

## Generated easy other seed 2

Which of the following best describes the following matrix $A?$

$$
A=\begin{bmatrix}2 & 3\end{bmatrix}
$$

selection: A row vector, A square matrix, A zero matrix, An identity matrix, Other

The matrix has only one row. Hence, it is a row vector.

## Generated easy other seed 57

Which of the following best describes the following matrix $F?$

$$
F=\begin{bmatrix}2 & -3 & -2 & 1 & -1 & 0\end{bmatrix}
$$

selection: A square matrix, Other, A zero matrix, A row vector, An identity matrix

The matrix has only one row. Hence, it is a row vector.

## Generated easy rows seed 2

Which of the following are row vectors?

$$
A=\begin{bmatrix}2 & -1\end{bmatrix},\,B=\begin{bmatrix}2 & -2 \\ 1 & -3 \\ 1 & 2 \\ -2 & 0\end{bmatrix},\,C=\begin{bmatrix}1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1\end{bmatrix}
$$

Select all that apply.

A: false, true; B: false, true; C: false, true

- $A$ is a row vector since it has only one row.

- $B$ is *not* a row vector, since it has more than $1$ row (it has $4$ rows).

- $C$ is *not* a row vector, since it has more than $1$ row (it has $6$ rows).

Therefore, only $A$ is a row vector.

## Generated easy rows seed 57

Which of the following are row vectors?

$$
A=\begin{bmatrix}2 & 1 & -3 & -2\end{bmatrix},\,B=\begin{bmatrix}-1 & 0 & 0 & 0 & 0 \\ 0 & 2 & 0 & 0 & 0 \\ 0 & 0 & -1 & 0 & 0 \\ 0 & 0 & 0 & -1 & 0 \\ 0 & 0 & 0 & 0 & -1\end{bmatrix},\,C=\begin{bmatrix}2 & 3 & -2 & 1 & 0 \\ -1 & 1 & 1 & 1 & -2 \\ -2 & 3 & -1 & 0 & 2 \\ -2 & 0 & 0 & -3 & 2 \\ 0 & 0 & -3 & 0 & -3 \\ 1 & -1 & 0 & 1 & 3\end{bmatrix}
$$

Select all that apply.

A: true, false; B: false, true; C: true, false

- $A$ is a row vector since it has only one row.

- $B$ is *not* a row vector, since it has more than $1$ row (it has $5$ rows).

- $C$ is *not* a row vector, since it has more than $1$ row (it has $6$ rows).

Therefore, only $A$ is a row vector.

## Generated easy columns seed 2

Which of the following are column vectors?

$$
A=\begin{bmatrix}2 & -1\end{bmatrix},\,B=\begin{bmatrix}2 & -2 \\ 1 & -3 \\ 1 & 2 \\ -2 & 0\end{bmatrix},\,C=\begin{bmatrix}1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1\end{bmatrix}
$$

Select all that apply. If none apply, leave all boxes unchecked.

A: false, true; B: false, true; C: false, true

- $A$ is *not* a column vector. It has only one row (and $2$ columns), so it's a row vector.

- $B$ is *not* a column vector, since it has more than $1$ column (it has $2$ columns).

- $C$ is *not* a column vector, since it has more than $1$ column (it has $6$ columns).

Therefore, none of the matrices are column vectors.

## Generated easy columns seed 57

Which of the following are column vectors?

$$
A=\begin{bmatrix}2 & 1 & -3 & -2\end{bmatrix},\,B=\begin{bmatrix}-1 & 0 & 0 & 0 & 0 \\ 0 & 2 & 0 & 0 & 0 \\ 0 & 0 & -1 & 0 & 0 \\ 0 & 0 & 0 & -1 & 0 \\ 0 & 0 & 0 & 0 & -1\end{bmatrix},\,C=\begin{bmatrix}2 & 3 & -2 & 1 & 0 \\ -1 & 1 & 1 & 1 & -2 \\ -2 & 3 & -1 & 0 & 2 \\ -2 & 0 & 0 & -3 & 2 \\ 0 & 0 & -3 & 0 & -3 \\ 1 & -1 & 0 & 1 & 3\end{bmatrix}
$$

Select all that apply. If none apply, leave all boxes unchecked.

A: true, false; B: false, true; C: true, false

- $A$ is *not* a column vector. It has only one row (and $4$ columns), so it's a row vector.

- $B$ is *not* a column vector, since it has more than $1$ column (it has $5$ columns).

- $C$ is *not* a column vector, since it has more than $1$ column (it has $5$ columns).

Therefore, none of the matrices are column vectors.

## Generated easy row_sets_repaired seed 2

Which of the following are row vectors?
$E = \begin{bmatrix}2 & 3\end{bmatrix}, F = \begin{bmatrix}2 & 3 & 2\end{bmatrix}, G = \begin{bmatrix}2 \\ 1 \\ -2 \\ 1\end{bmatrix}$

selection: $F$ only, $E$ only, $G$ only, $E$ and $G$ only, $E$ and $F$ only

- $E$ is a row vector since it has only one row.

- $F$ is a row vector since it has only one row.

- $G$ is *not* a row vector. It has only one column (and $4$ rows), so it's a column vector.

Therefore, only $E$ and $F$ are row vectors.

## Generated easy row_sets_repaired seed 57

Which of the following are row vectors?
$E = \begin{bmatrix}2 & -3 & -2 & 1 & -1 & 0\end{bmatrix}, F = \begin{bmatrix}2 & 2 & 3 & 0\end{bmatrix}, G = \begin{bmatrix}2 & 1 & -1 \\ 0 & 0 & -3\end{bmatrix}$

selection: $E$ and $F$ only, $E$ and $G$ only, $E$ only, $G$ only, $F$ only

- $E$ is a row vector since it has only one row.

- $F$ is a row vector since it has only one row.

- $G$ is *not* a row vector, since it has more than $1$ row (it has $2$ rows).

Therefore, only $E$ and $F$ are row vectors.

## Generated easy legacy_other_repaired seed 2

Which of the following best describes the following matrix $A$?
$A = \begin{bmatrix}2 & 3\end{bmatrix}$

selection: Other, A row vector, A column vector, An identity matrix, A zero matrix

The matrix has only one row. Hence, it is a row vector.

## Generated easy legacy_other_repaired seed 57

Which of the following best describes the following matrix $F$?
$F = \begin{bmatrix}2 & -3 & -2 & 1 & -1 & 0\end{bmatrix}$

selection: A row vector, A zero matrix, A column vector, Other, An identity matrix

The matrix has only one row. Hence, it is a row vector.

## Generated moderate row seed 2 (authored level)

Which of the following best describes the following matrix $A?$

$$
A=\begin{bmatrix}2 & 3 & -2 & 2 & 3 & 2 & 3\end{bmatrix}
$$

selection: A zero matrix, A row vector, A square matrix, A column vector, An identity matrix

The matrix has only one row. Hence, it is a row vector.

## Generated moderate row seed 57 (authored level)

Which of the following best describes the following matrix $F?$

$$
F=\begin{bmatrix}2 & 1 & -1 & 0 & -1 & 0 & 2\end{bmatrix}
$$

selection: A zero matrix, A column vector, An identity matrix, A row vector, A square matrix

The matrix has only one row. Hence, it is a row vector.

## Generated moderate diagonal seed 2 (authored level)

Which of the following best describes the following matrix $A?$

$$
A=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 2 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 2 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & -1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & -1\end{bmatrix}
$$

selection: A diagonal matrix, Other, A column matrix, A row vector, An identity matrix

The matrix is square, all the entries that do not lie on the main diagonal are zeros, and the diagonal entries are not all ones. 

Hence it's a diagonal matrix.

## Generated moderate diagonal seed 57 (authored level)

Which of the following best describes the following matrix $F?$

$$
F=\begin{bmatrix}-1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & -1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & -1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & -2\end{bmatrix}
$$

selection: An identity matrix, A column matrix, A diagonal matrix, A row vector, Other

The matrix is square, all the entries that do not lie on the main diagonal are zeros, and the diagonal entries are not all ones. 

Hence it's a diagonal matrix.

## Generated moderate other seed 2 (authored level)

Which of the following best describes the following matrix $A?$

$$
A=\begin{bmatrix}2 & 3 & -2 & 2 & 3 & 2 & 3\end{bmatrix}
$$

selection: Other, A square matrix, A row vector, A zero matrix, An identity matrix

The matrix has only one row. Hence, it is a row vector.

## Generated moderate other seed 57 (authored level)

Which of the following best describes the following matrix $F?$

$$
F=\begin{bmatrix}2 & 1 & -1 & 0 & -1 & 0 & 2\end{bmatrix}
$$

selection: Other, A zero matrix, An identity matrix, A square matrix, A row vector

The matrix has only one row. Hence, it is a row vector.

## Generated moderate rows seed 2 (authored level)

Which of the following are row vectors?

$$
A=\begin{bmatrix}1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1\end{bmatrix},\,B=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix},\,C=\begin{bmatrix}1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1\end{bmatrix}
$$

Select all that apply.

A: true, false; B: true, false; C: true, false

- $A$ is *not* a row vector, since it has more than $1$ row (it has $7$ rows).

- $B$ is *not* a row vector, since it has more than $1$ row (it has $8$ rows).

- $C$ is *not* a row vector, since it has more than $1$ row (it has $7$ rows).

Therefore, none of the matrices are row vectors.

## Generated moderate rows seed 57 (authored level)

Which of the following are row vectors?

$$
A=\begin{bmatrix}2 & 1 & -3 & -2 & 1 & -1 & 0 & -1\end{bmatrix},\,B=\begin{bmatrix}2 & 1 & 2 & -2 & 1 & 1 & -1 & 0 \\ 0 & -3 & 2 & 2 & 1 & 2 & 0 & 1 \\ -1 & 3 & 2 & 1 & -2 & 1 & -2 & -2 \\ 0 & 1 & -2 & 3 & 1 & 0 & 1 & 3 \\ -2 & 1 & 0 & -1 & 1 & 1 & 1 & -2 \\ -2 & 3 & -1 & 0 & 2 & -2 & 0 & 0 \\ -3 & 2 & 0 & 0 & -3 & 0 & -3 & 1 \\ -1 & 0 & 1 & 3 & -3 & 2 & 0 & 1\end{bmatrix},\,C=\begin{bmatrix}0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply.

A: true, false; B: true, false; C: true, false

- $A$ is a row vector since it has only one row.

- $B$ is *not* a row vector, since it has more than $1$ row (it has $8$ rows).

- $C$ is *not* a row vector, since it has more than $1$ row (it has $7$ rows).

Therefore, only $A$ is a row vector.

## Generated moderate columns seed 2 (authored level)

Which of the following are column vectors?

$$
A=\begin{bmatrix}1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1\end{bmatrix},\,B=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix},\,C=\begin{bmatrix}1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1\end{bmatrix}
$$

Select all that apply. If none apply, leave all boxes unchecked.

A: true, false; B: true, false; C: true, false

- $A$ is *not* a column vector, since it has more than $1$ column (it has $7$ columns).

- $B$ is *not* a column vector, since it has more than $1$ column (it has $8$ columns).

- $C$ is *not* a column vector, since it has more than $1$ column (it has $7$ columns).

Therefore, none of the matrices are column vectors.

## Generated moderate columns seed 57 (authored level)

Which of the following are column vectors?

$$
A=\begin{bmatrix}2 & 1 & -3 & -2 & 1 & -1 & 0 & -1\end{bmatrix},\,B=\begin{bmatrix}2 & 1 & 2 & -2 & 1 & 1 & -1 & 0 \\ 0 & -3 & 2 & 2 & 1 & 2 & 0 & 1 \\ -1 & 3 & 2 & 1 & -2 & 1 & -2 & -2 \\ 0 & 1 & -2 & 3 & 1 & 0 & 1 & 3 \\ -2 & 1 & 0 & -1 & 1 & 1 & 1 & -2 \\ -2 & 3 & -1 & 0 & 2 & -2 & 0 & 0 \\ -3 & 2 & 0 & 0 & -3 & 0 & -3 & 1 \\ -1 & 0 & 1 & 3 & -3 & 2 & 0 & 1\end{bmatrix},\,C=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix}
$$

Select all that apply. If none apply, leave all boxes unchecked.

A: true, false; B: true, false; C: true, false

- $A$ is *not* a column vector. It has only one row (and $8$ columns), so it's a row vector.

- $B$ is *not* a column vector, since it has more than $1$ column (it has $8$ columns).

- $C$ is *not* a column vector, since it has more than $1$ column (it has $7$ columns).

Therefore, none of the matrices are column vectors.

## Generated moderate row_sets_repaired seed 2 (authored level)

Which of the following are row vectors?
$E = \begin{bmatrix}2 & 3 & -2 & 2 & 3 & 2 & 3\end{bmatrix}, F = \begin{bmatrix}2 & 1 & -2 & 1 & -3 & 1 & 2 & -2\end{bmatrix}, G = \begin{bmatrix}2 \\ 0 \\ 3 \\ 2 \\ 3 \\ 1 \\ -1 \\ 1\end{bmatrix}$

selection: $E$ and $G$ only, $F$ only, $E$ and $F$ only, $E$ only, $G$ only

- $E$ is a row vector since it has only one row.

- $F$ is a row vector since it has only one row.

- $G$ is *not* a row vector. It has only one column (and $8$ rows), so it's a column vector.

Therefore, only $E$ and $F$ are row vectors.

## Generated moderate row_sets_repaired seed 57 (authored level)

Which of the following are row vectors?
$E = \begin{bmatrix}2 & 1 & -1 & 0 & -1 & 0 & 2\end{bmatrix}, F = \begin{bmatrix}2 & 3 & 2 & -2 & 1 & 1 & -1 & 0\end{bmatrix}, G = \begin{bmatrix}2 & 2 \\ 1 & 2 \\ 0 & 1 \\ -1 & 3 \\ 2 & 1 \\ -2 & 1 \\ -2 & -2 \\ 0 & 1\end{bmatrix}$

selection: $F$ only, $E$ and $F$ only, $E$ only, $G$ only, $E$ and $G$ only

- $E$ is a row vector since it has only one row.

- $F$ is a row vector since it has only one row.

- $G$ is *not* a row vector, since it has more than $1$ row (it has $8$ rows).

Therefore, only $E$ and $F$ are row vectors.

## Generated moderate legacy_other_repaired seed 2 (authored level)

Which of the following best describes the following matrix $A$?
$A = \begin{bmatrix}2 & 3 & -2 & 2 & 3 & 2 & 3\end{bmatrix}$

selection: A zero matrix, A row vector, Other, A column vector, An identity matrix

The matrix has only one row. Hence, it is a row vector.

## Generated moderate legacy_other_repaired seed 57 (authored level)

Which of the following best describes the following matrix $F$?
$F = \begin{bmatrix}2 & 1 & -1 & 0 & -1 & 0 & 2\end{bmatrix}$

selection: A zero matrix, A column vector, An identity matrix, A row vector, Other

The matrix has only one row. Hence, it is a row vector.

## Generated hard row seed 2 (authored level)

Which of the following best describes the following matrix $A?$

$$
A=\begin{bmatrix}2 & 3 & -2 & 2 & 3 & 2 & 3 & -1 & -1\end{bmatrix}
$$

selection: A square matrix, A row vector, An identity matrix, A zero matrix, A column vector

The matrix has only one row. Hence, it is a row vector.

## Generated hard row seed 57 (authored level)

Which of the following best describes the following matrix $F?$

$$
F=\begin{bmatrix}2 & 1 & -1 & 0 & -1 & 0 & 2 & 3 & 0\end{bmatrix}
$$

selection: A column vector, A square matrix, An identity matrix, A zero matrix, A row vector

The matrix has only one row. Hence, it is a row vector.

## Generated hard diagonal seed 2 (authored level)

Which of the following best describes the following matrix $A?$

$$
A=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 2 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & -1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & -1\end{bmatrix}
$$

selection: A diagonal matrix, Other, A row vector, An identity matrix, A column matrix

The matrix is square, all the entries that do not lie on the main diagonal are zeros, and the diagonal entries are not all ones. 

Hence it's a diagonal matrix.

## Generated hard diagonal seed 57 (authored level)

Which of the following best describes the following matrix $F?$

$$
F=\begin{bmatrix}2 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & -1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & -1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & -1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & -2 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix}
$$

selection: A row vector, A column matrix, Other, An identity matrix, A diagonal matrix

The matrix is square, all the entries that do not lie on the main diagonal are zeros, and the diagonal entries are not all ones. 

Hence it's a diagonal matrix.

## Generated hard other seed 2 (authored level)

Which of the following best describes the following matrix $A?$

$$
A=\begin{bmatrix}2 & 3 & -2 & 2 & 3 & 2 & 3 & -1 & -1\end{bmatrix}
$$

selection: A row vector, A square matrix, An identity matrix, Other, A zero matrix

The matrix has only one row. Hence, it is a row vector.

## Generated hard other seed 57 (authored level)

Which of the following best describes the following matrix $F?$

$$
F=\begin{bmatrix}2 & 1 & -1 & 0 & -1 & 0 & 2 & 3 & 0\end{bmatrix}
$$

selection: A zero matrix, A row vector, An identity matrix, Other, A square matrix

The matrix has only one row. Hence, it is a row vector.

## Generated hard rows seed 2 (authored level)

Which of the following are row vectors?

$$
A=\begin{bmatrix}1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1\end{bmatrix},\,B=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix},\,C=\begin{bmatrix}2 \\ 2 \\ -3 \\ 0 \\ 1 \\ -3 \\ 3 \\ -2 \\ -2\end{bmatrix}
$$

Select all that apply.

A: true, false; B: true, false; C: false, true

- $A$ is *not* a row vector, since it has more than $1$ row (it has $9$ rows).

- $B$ is *not* a row vector, since it has more than $1$ row (it has $10$ rows).

- $C$ is *not* a row vector. It has only one column (and $9$ rows), so it's a column vector.

Therefore, none of the matrices are row vectors.

## Generated hard rows seed 57 (authored level)

Which of the following are row vectors?

$$
A=\begin{bmatrix}2 & 1 & -3 & -2 & 1 & -1 & 0 & -1 & 0 & 2\end{bmatrix},\,B=\begin{bmatrix}1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1\end{bmatrix},\,C=\begin{bmatrix}2 & -2 & 2 & -2 & 3 & 1 & -2 & 2 & 3 & 3\end{bmatrix}
$$

Select all that apply.

A: true, false; B: true, false; C: true, false

- $A$ is a row vector since it has only one row.

- $B$ is *not* a row vector, since it has more than $1$ row (it has $10$ rows).

- $C$ is a row vector since it has only one row.

Therefore, only $A$ and $C$ are row vectors.

## Generated hard columns seed 2 (authored level)

Which of the following are column vectors?

$$
A=\begin{bmatrix}1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1\end{bmatrix},\,B=\begin{bmatrix}0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0\end{bmatrix},\,C=\begin{bmatrix}2 \\ 2 \\ -3 \\ 0 \\ 1 \\ -3 \\ 3 \\ -2 \\ -2\end{bmatrix}
$$

Select all that apply. If none apply, leave all boxes unchecked.

A: true, false; B: true, false; C: false, true

- $A$ is *not* a column vector, since it has more than $1$ column (it has $9$ columns).

- $B$ is *not* a column vector, since it has more than $1$ column (it has $9$ columns).

- $C$ is a column vector since it has only one column.

Therefore, only $C$ is a column vector.

## Generated hard columns seed 57 (authored level)

Which of the following are column vectors?

$$
A=\begin{bmatrix}2 & 1 & -3 & -2 & 1 & -1 & 0 & -1 & 0 & 2\end{bmatrix},\,B=\begin{bmatrix}1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 & 1\end{bmatrix},\,C=\begin{bmatrix}2 & -2 & 2 & -2 & 3 & 1 & -2 & 2 & 3 & 3\end{bmatrix}
$$

Select all that apply. If none apply, leave all boxes unchecked.

A: true, false; B: true, false; C: true, false

- $A$ is *not* a column vector. It has only one row (and $10$ columns), so it's a row vector.

- $B$ is *not* a column vector, since it has more than $1$ column (it has $10$ columns).

- $C$ is *not* a column vector. It has only one row (and $10$ columns), so it's a row vector.

Therefore, none of the matrices are column vectors.

## Generated hard row_sets_repaired seed 2 (authored level)

Which of the following are row vectors?
$E = \begin{bmatrix}2 & 3 & -2 & 2 & 3 & 2 & 3 & -1 & -1\end{bmatrix}, F = \begin{bmatrix}2 & -3 & 1 & 2 & -2 & 0 & 2 & 0 & 3\end{bmatrix}, G = \begin{bmatrix}2 \\ 0 \\ 1 \\ -1 \\ -3 \\ 3 \\ -3 \\ -1 \\ 0 \\ -1\end{bmatrix}$

selection: $E$ and $G$ only, $E$ and $F$ only, $E$ only, $F$ only, $G$ only

- $E$ is a row vector since it has only one row.

- $F$ is a row vector since it has only one row.

- $G$ is *not* a row vector. It has only one column (and $10$ rows), so it's a column vector.

Therefore, only $E$ and $F$ are row vectors.

## Generated hard row_sets_repaired seed 57 (authored level)

Which of the following are row vectors?
$E = \begin{bmatrix}2 & 1 & -1 & 0 & -1 & 0 & 2 & 3 & 0\end{bmatrix}, F = \begin{bmatrix}2 & 2 & -2 & 1 & 1 & -1 & 0 & 0 & -3\end{bmatrix}, G = \begin{bmatrix}2 & 3 \\ 2 & 1 \\ -2 & 1 \\ -2 & -2 \\ 0 & 1 \\ -2 & 3 \\ 1 & 0 \\ 1 & 3 \\ -2 & 1 \\ 0 & -1\end{bmatrix}$

selection: $E$ only, $G$ only, $E$ and $F$ only, $E$ and $G$ only, $F$ only

- $E$ is a row vector since it has only one row.

- $F$ is a row vector since it has only one row.

- $G$ is *not* a row vector, since it has more than $1$ row (it has $10$ rows).

Therefore, only $E$ and $F$ are row vectors.

## Generated hard legacy_other_repaired seed 2 (authored level)

Which of the following best describes the following matrix $A$?
$A = \begin{bmatrix}2 & 3 & -2 & 2 & 3 & 2 & 3 & -1 & -1\end{bmatrix}$

selection: Other, A row vector, An identity matrix, A zero matrix, A column vector

The matrix has only one row. Hence, it is a row vector.

## Generated hard legacy_other_repaired seed 57 (authored level)

Which of the following best describes the following matrix $F$?
$F = \begin{bmatrix}2 & 1 & -1 & 0 & -1 & 0 & 2 & 3 & 0\end{bmatrix}$

selection: A column vector, Other, An identity matrix, A zero matrix, A row vector

The matrix has only one row. Hence, it is a row vector.
