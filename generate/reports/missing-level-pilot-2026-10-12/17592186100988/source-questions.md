# Complete source practice questions

EDB math basis 1522; KP 17592186100988. Original prompts, every choice, and one original worked solution are retained. Missing source attributes remain explicitly missing.

## q-13488 — unrated

**Specific components:** {"matrix": [[1, 1, 2], [-1, 1, 3]], "rows": 2, "columns": 3, "row": 1, "column": 3, "domains": "One-based integer indices; allow absent entry only for the observed out-of-bounds family.", "expected_answer": "2"}

**Template:** `unrated-inline-in-bounds-radio`

Find the entry $a_{13}$ of the matrix $A$, where
$A = \begin{bmatrix}1 & 1 & 2 \\ -1 & 1 & 3\end{bmatrix}$.

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| selection | radio | bank-q-13488 | 17592186098074 | $-1$ | unrecorded | `A[r-1][c-1]`; {"candidate_positions": [[2, 1]]} |
| selection | radio | bank-q-13488 | 17592186098075 | $0$ | unrecorded | `k`; {"k": "0"} |
| selection | radio | bank-q-13488 | 17592186098076 | $3$ | unrecorded | `A[r-1][c-1]`; {"candidate_positions": [[2, 3]]} |
| selection | radio | bank-q-13488 | 17592186098077 | No such entry | unrecorded | `No such entry`; {} |
| selection | radio | bank-q-13488 | 17592186098078 | $2$ | unrecorded | `A[r-1][c-1]`; {"candidate_positions": [[1, 3]]} |

**Original worked solution:**

**Missing in database. No source solution was invented.**

## q-13496 — unrated

**Specific components:** {"matrix": [[0, 1, 2, 4], [-1, 2, -3, 5], [2, 1, -3, 4]], "rows": 3, "columns": 4, "row": 4, "column": 3, "domains": "One-based integer indices; allow absent entry only for the observed out-of-bounds family.", "expected_answer": "No such entry"}

**Template:** `unrated-out-of-bounds-radio`

Find the entry $d_{43}$ of the matrix $D$, where
$D = \begin{bmatrix}0 & 1 & 2 & 4 \\ -1 & 2 & -3 & 5 \\ 2 & 1 & -3 & 4\end{bmatrix}$.

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| selection | radio | bank-q-13496 | 17592186098086 | $5$ | unrecorded | `A[r-1][c-1]`; {"candidate_positions": [[2, 4]]} |
| selection | radio | bank-q-13496 | 17592186098087 | $-3$ | unrecorded | `A[r-1][c-1]`; {"candidate_positions": [[2, 3], [3, 3]]} |
| selection | radio | bank-q-13496 | 17592186098088 | $-1$ | unrecorded | `A[r-1][c-1]`; {"candidate_positions": [[2, 1]]} |
| selection | radio | bank-q-13496 | 17592186098089 | $4$ | unrecorded | `A[r-1][c-1]`; {"candidate_positions": [[1, 4], [3, 4]]} |
| selection | radio | bank-q-13496 | 17592186098090 | No such entry | unrecorded | `No such entry`; {} |

**Original worked solution:**

**Missing in database. No source solution was invented.**

## q-279260 — easy

**Specific components:** {"matrix": [[1, -2, 6], [-2, -1, 7]], "rows": 2, "columns": 3, "row": 2, "column": 2, "domains": "One-based integer indices; allow absent entry only for the observed out-of-bounds family.", "expected_answer": "-1"}

**Template:** `E1-lookup-radio`

Find the entry ${y}_{22}$ of the matrix $Y$, where 

$$
Y=[\begin{aligned}1 & -2 & 6 \\ -2 & -1 & 7\end{aligned}].
$$

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| selection | radio | bank-q-279260 | 17592186292984 | $1$ | False | `A[r-1][c-1]`; {"candidate_positions": [[1, 1]]} |
| selection | radio | bank-q-279260 | 17592186293106 | $2$ | False | `k`; {"k": "2"} |
| selection | radio | bank-q-279260 | 17592186293342 | $-1$ | True | `A[i-1][j-1]`; {"A": "[[1, -2, 6], [-2, -1, 7]]", "i": "2", "j": "2"} |
| selection | radio | bank-q-279260 | 17592186293453 | $-2$ | False | `A[r-1][c-1]`; {"candidate_positions": [[1, 2], [2, 1]]} |
| selection | radio | bank-q-279260 | 17592186293923 | $7$ | False | `A[r-1][c-1]`; {"candidate_positions": [[2, 3]]} |

**Original worked solution:**

The entry ${y}_{22}$ lies at the intersection of the $2$nd row and $2$nd column. Therefore, ${y}_{22}=-1.$

$$
Y=[\begin{aligned}1 & -2 & 6 \\ -2 & -1 & 7\end{aligned}].
$$

## q-279539 — easy

**Specific components:** {"matrix": [[-5, -2, 0, 9], [3, -8, -2, 5], [-2, 2, 5, -8], [6, 6, -6, 0], [-6, 4, 2, 5]], "rows": 5, "columns": 4, "row": 5, "column": 3, "domains": "One-based integer indices; allow absent entry only for the observed out-of-bounds family.", "expected_answer": "2"}

**Template:** `E2-lookup-blank`

Find the entry ${e}_{53}$ of the matrix $E$, where 

$$
E=[\begin{aligned}-5 & -2 & 0 & 9 \\ 3 & -8 & -2 & 5 \\ -2 & 2 & 5 & -8 \\ 6 & 6 & -6 & 0 \\ -6 & 4 & 2 & 5\end{aligned}].
$$

${e}_{53}=$
{{field-1}}

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| field-1 | blank | none | 17592186293527 | $2$ | True | `A[i-1][j-1]`; {"A": "[[-5, -2, 0, 9], [3, -8, -2, 5], [-2, 2, 5, -8], [6, 6, -6, 0], [-6, 4, 2, 5]]", "i": "5", "j": "3"} |

**Original worked solution:**

The entry ${e}_{53}$ lies at the intersection of the $5$th row and $3$rd column. Therefore, ${e}_{53}=2.$

$$
E=[\begin{aligned}-5 & -2 & 0 & 9 \\ 3 & -8 & -2 & 5 \\ -2 & 2 & 5 & -8 \\ 6 & 6 & -6 & 0 \\ -6 & 4 & 2 & 5\end{aligned}].
$$

## q-279540 — easy

**Specific components:** {"matrix": [[4, 5, -2, 0], [-2, -1, 2, 5], [3, 4, 0, -3]], "rows": 3, "columns": 4, "row": 3, "column": 2, "domains": "One-based integer indices; allow absent entry only for the observed out-of-bounds family.", "expected_answer": "4"}

**Template:** `E2-lookup-blank`

Find the entry ${f}_{32}$ of the matrix $F$, where 

$$
F=[\begin{aligned}4 & 5 & -2 & 0 \\ -2 & -1 & 2 & 5 \\ 3 & 4 & 0 & -3\end{aligned}].
$$

${f}_{32}=$
{{field-1}}

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| field-1 | blank | none | 17592186292968 | $4$ | True | `A[i-1][j-1]`; {"A": "[[4, 5, -2, 0], [-2, -1, 2, 5], [3, 4, 0, -3]]", "i": "3", "j": "2"} |

**Original worked solution:**

The entry ${f}_{32}$ lies at the intersection of the $3$rd row and $2$nd column. Therefore, ${f}_{32}=4.$

$$
F=[\begin{aligned}4 & 5 & -2 & 0 \\ -2 & -1 & 2 & 5 \\ 3 & 4 & 0 & -3\end{aligned}].
$$

## q-13497 — easy

**Specific components:** {"matrix": [[0, 1, 2, 4], [-1, 2, -3, 5], [2, 1, -3, 4]], "rows": 3, "columns": 4, "row": 2, "column": 4, "domains": "One-based integer indices; allow absent entry only for the observed out-of-bounds family.", "expected_answer": "5"}

**Template:** `E1-lookup-radio`

Find the entry ${c}_{24}$ of the matrix $C$, where 

$$
C=[\begin{aligned}0 & 1 & 2 & 4 \\ -1 & 2 & -3 & 5 \\ 2 & 1 & -3 & 4\end{aligned}].
$$

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| selection | radio | bank-q-13497 | 17592186395750 | No such entry | False | `No such entry`; {} |
| selection | radio | bank-q-13497 | 17592186395751 | $-3$ | False | `A[r-1][c-1]`; {"candidate_positions": [[2, 3], [3, 3]]} |
| selection | radio | bank-q-13497 | 17592186395752 | $4$ | False | `A[r-1][c-1]`; {"candidate_positions": [[1, 4], [3, 4]]} |
| selection | radio | bank-q-13497 | 17592186395753 | $-1$ | False | `A[r-1][c-1]`; {"candidate_positions": [[2, 1]]} |
| selection | radio | bank-q-13497 | 17592186395754 | $5$ | True | `A[i-1][j-1]`; {"A": "[[0, 1, 2, 4], [-1, 2, -3, 5], [2, 1, -3, 4]]", "i": "2", "j": "4"} |

**Original worked solution:**

The entry ${c}_{24}$ should lie at the intersection of the $2$nd row and $4$th column. Therefore, ${c}_{24}=5.$

$$
C=[\begin{aligned}0 & 1 & 2 & 4 \\ -1 & 2 & -3 & 5 \\ 2 & 1 & -3 & 4\end{aligned}]
$$

## q-125561 — easy

**Specific components:** {"matrix": [[1, 2], [-1, 5], [-3, 4]], "rows": 3, "columns": 2, "row": 3, "column": 1, "domains": "One-based integer indices; allow absent entry only for the observed out-of-bounds family.", "expected_answer": "-3"}

**Template:** `E1-lookup-radio`

Find the entry ${e}_{31}$ of the matrix $E$, where 

$$
E=[\begin{aligned}1 & 2 \\ -1 & 5 \\ -3 & 4\end{aligned}].
$$

| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |
|---|---|---|---:|---|---|---|
| selection | radio | bank-q-125561 | 17592186398265 | $1$ | False | `A[r-1][c-1]`; {"candidate_positions": [[1, 1]]} |
| selection | radio | bank-q-125561 | 17592186398266 | $-3$ | True | `A[i-1][j-1]`; {"A": "[[1, 2], [-1, 5], [-3, 4]]", "i": "3", "j": "1"} |
| selection | radio | bank-q-125561 | 17592186398267 | $4$ | False | `A[r-1][c-1]`; {"candidate_positions": [[3, 2]]} |
| selection | radio | bank-q-125561 | 17592186398268 | $-1$ | False | `A[r-1][c-1]`; {"candidate_positions": [[2, 1]]} |
| selection | radio | bank-q-125561 | 17592186398269 | $5$ | False | `A[r-1][c-1]`; {"candidate_positions": [[2, 2]]} |

**Original worked solution:**

The entry ${e}_{31}$ lies at the intersection of the $3$rd row and $1$st column. Therefore, ${e}_{31}=-3.$

$$
E=[\begin{aligned}1 & 2 \\ -1 & 5 \\ -3 & 4\end{aligned}]
$$
