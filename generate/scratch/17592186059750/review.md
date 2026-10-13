# Determinant unknowns review

Original capture: math basis 1356. Original strings below remain evidence. Replays normalize mathematical notation and repair missing fields/ref designations explicitly.


## q-11651 — original

If
$C = \begin{bmatrix}2 & 3 \\ 5 & k\end{bmatrix}$
and
$det(C) = 3$, what is the value of $k$?

Original choices: [["k = 9", "k =-4", "k =-9", "k = 4", "k = 0"]]

Observed correct designations: [null]

No captured solution.


### Parameterized replay

If
$C = \begin{bmatrix}2 & 3 \\ 5 & k\end{bmatrix}$
and
$det(C) = 3$, what is the value of $k$?

- $k =-9$
- $k =-4$
- $k = 9$
- $k = 0$
- $k = 4$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(C) & =|\begin{aligned}2 & 3 \\ 5 & k\end{aligned}| \\  & =2\cdot k-3\cdot 5 \\  & =2k-15\end{aligned}
$$

Since $det(C)=3$, we obtain:

$$
\begin{aligned}det(C) & =3 \\ 2k-15 & =3 \\ 2k & =18 \\ k & =9\end{aligned}
$$


### Generated variant (observed:q-11651)

If
$C = \begin{bmatrix}5 & 3 \\ -1 & k\end{bmatrix}$
and
$det(C) = -22$, what is the value of $k$?

- $k = -5$
- $k =\frac{20}{9}$
- $k = 0$
- $k =5$
- $k = -\frac{20}{9}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(C) & =|\begin{aligned}5 & 3 \\ -1 & k\end{aligned}| \\  & =5\cdot k-3\cdot (-1) \\  & =5k+3\end{aligned}
$$

Since $det(C)=-22$, we obtain:

$$
\begin{aligned}det(C) & =-22 \\ 5k+3 & =-22 \\ 5k & =-25 \\ k & =-5\end{aligned}
$$


### Generated variant (authored:operations)

If
$C = \begin{bmatrix}-3 & 7 \\ 2 & k\end{bmatrix}$
and
$det(C) = -41$, what is the value of $k$?

- $k=-9$
- $k=-27$
- $k=\frac{55}{3}$
- $k=\frac{41}{3}$
- $k=9$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(C) & =|\begin{aligned}-3 & 7 \\ 2 & k\end{aligned}| \\  & =(-3)\cdot k-7\cdot 2 \\  & =-3k-14\end{aligned}
$$

Since $det(C)=-41$, we obtain:

$$
\begin{aligned}det(C) & =-41 \\ -3k-14 & =-41 \\ -3k & =-27 \\ k & =9\end{aligned}
$$


## q-19801 — original

If
$A = \begin{bmatrix}1 + t & 2t \\ -3 & 1 - t\end{bmatrix}$
and $det(A) = 10$, what is the value of $t$?

Original choices: [["-3", "1", "3", "-1", "2"]]

Observed correct designations: [null]

No captured solution.


### Parameterized replay

If
$A = \begin{bmatrix}1 + t & 2t \\ -3 & 1 - t\end{bmatrix}$
and $det(A) = 10$, what is the value of $t$?

- $3$
- $1$
- $-3$
- $2$
- $-1$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(A) & =|\begin{aligned}1+t & 2t \\ -3 & 1-t\end{aligned}| \\  & =(1+t)(1-t)-2t\cdot (-3) \\  & =1-{t}^{2}+6t \\  & =-{t}^{2}+6t+1\end{aligned}
$$

Since $det(A)=10$, we obtain:

$$
\begin{aligned}det(A) & =10 \\ -{t}^{2}+6t+1 & =10 \\ -{t}^{2}+6t-9 & =0 \\ {t}^{2}-6t+9 & =0 \\ (t-3)^{2} & =0 \\ t & =3\end{aligned}
$$


### Generated variant (observed:q-19801)

If
$A = \begin{bmatrix}4 + t & 3t \\ -4 & 4 - t\end{bmatrix}$
and $det(A) = 52$, what is the value of $t$?

- $-6$
- $4$
- $6$
- $-2$
- $2$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(A) & =|\begin{aligned}4+t & 3t \\ -4 & 4-t\end{aligned}| \\  & =(4+t)(4-t)-3t\cdot (-4) \\  & =16-{t}^{2}+12t \\  & =-{t}^{2}+12t+16\end{aligned}
$$

Since $det(A)=52$, we obtain:

$$
\begin{aligned}det(A) & =52 \\ -{t}^{2}+12t+16 & =52 \\ -{t}^{2}+12t-36 & =0 \\ {t}^{2}-12t+36 & =0 \\ (t-6)^{2} & =0 \\ t & =6\end{aligned}
$$


### Generated variant (authored:operations)

If
$A = \begin{bmatrix}3 + t & t \\ 4 & 3 - t\end{bmatrix}$
and $det(A) = 13$, what is the value of $t$?

- $-2$
- $-4$
- $-1$
- $2$
- $4$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(A) & =|\begin{aligned}3+t & t \\ 4 & 3-t\end{aligned}| \\  & =(3+t)(3-t)-t\cdot 4 \\  & =9-{t}^{2}-4t \\  & =-{t}^{2}-4t+9\end{aligned}
$$

Since $det(A)=13$, we obtain:

$$
\begin{aligned}det(A) & =13 \\ -{t}^{2}-4t+9 & =13 \\ -{t}^{2}-4t-4 & =0 \\ {t}^{2}+4t+4 & =0 \\ (t+2)^{2} & =0 \\ t & =-2\end{aligned}
$$


## q-127614 — original

If
$D=[\begin{aligned}2x & 6 \\ 2x & x-2\end{aligned}]$
and $det(D)=-32$, what is the value of $x?$

Original choices: []

Observed correct designations: []

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(D) & =|\begin{aligned}2x & 6 \\ 2x & x-2\end{aligned}| \\  & =2x\cdot (x-2)-6\cdot 2x \\  & =2{x}^{2}-16x\end{aligned}
$$

Since $det(D)=-32$, we obtain:

$$
\begin{aligned}det(D) & =-32 \\ 2{x}^{2}-16x & =-32 \\ 2{x}^{2}-16x+32 & =0 \\ {x}^{2}-8x+16 & =0 \\ (x-4)^{2} & =0 \\ x & =4\end{aligned}
$$


### Parameterized replay

If
$D=[\begin{aligned}2x & 6 \\ 2x & x-2\end{aligned}]$
and $det(D)=-32$, what is the value of $x?$

$x=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(D) & =|\begin{aligned}2x & 6 \\ 2x & x-2\end{aligned}| \\  & =2x\cdot (x-2)-6\cdot 2x \\  & =2{x}^{2}-16x\end{aligned}
$$

Since $det(D)=-32$, we obtain:

$$
\begin{aligned}det(D) & =-32 \\ 2{x}^{2}-16x & =-32 \\ 2{x}^{2}-16x+32 & =0 \\ {x}^{2}-8x+16 & =0 \\ (x-4)^{2} & =0 \\ x & =4\end{aligned}
$$


### Generated variant (authored:blank_repair)

If
$D=[\begin{aligned}2x & 2 \\ 2x & x+8\end{aligned}]$
and $det(D)=-18$, what is the value of $x?$

$x=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(D) & =|\begin{aligned}2x & 2 \\ 2x & x+8\end{aligned}| \\  & =2x\cdot (x+8)-2\cdot 2x \\  & =2{x}^{2}+12x\end{aligned}
$$

Since $det(D)=-18$, we obtain:

$$
\begin{aligned}det(D) & =-18 \\ 2{x}^{2}+12x & =-18 \\ 2{x}^{2}+12x+18 & =0 \\ {x}^{2}+6x+9 & =0 \\ (x+3)^{2} & =0 \\ x & =-3\end{aligned}
$$


### Generated variant (authored:blank_repair)

If
$D=[\begin{aligned}3x & 3 \\ 2x & x-4\end{aligned}]$
and $det(D)=-27$, what is the value of $x?$

$x=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(D) & =|\begin{aligned}3x & 3 \\ 2x & x-4\end{aligned}| \\  & =3x\cdot (x-4)-3\cdot 2x \\  & =3{x}^{2}-18x\end{aligned}
$$

Since $det(D)=-27$, we obtain:

$$
\begin{aligned}det(D) & =-27 \\ 3{x}^{2}-18x & =-27 \\ 3{x}^{2}-18x+27 & =0 \\ {x}^{2}-6x+9 & =0 \\ (x-3)^{2} & =0 \\ x & =3\end{aligned}
$$


## q-11653 — original

If
    $M=[\begin{aligned}2 & w \\ 4 & 3\end{aligned}]$
and
$\text{det}(M)=2$, what is the value of $w?$

Original choices: [["-4", "-1", "0", "1", "4"]]

Observed correct designations: [{":answer/id": "dd8e6d11-24ab-54f4-9302-a197b45ae78f", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "1", ":db/id": 17592186252504}]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(M) & =|\begin{aligned}2 & w \\ 4 & 3\end{aligned}| \\  & =2\cdot 3-w\cdot 4 \\  & =6-4w.\end{aligned}
$$

    

Since $det(M)=2$, we get:

$$
\begin{aligned}det(M) & =2 \\ 6-4w & =2 \\ -4w & =2-6 \\ -4w & =-4 \\ w & =1\end{aligned}
$$


### Parameterized replay

If
    $M=[\begin{aligned}2 & w \\ 4 & 3\end{aligned}]$
and
$\text{det}(M)=2$, what is the value of $w?$

- $0$
- $-1$
- $-4$
- $4$
- $1$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(M) & =|\begin{aligned}2 & w \\ 4 & 3\end{aligned}| \\  & =2\cdot 3-w\cdot 4 \\  & =6-4w.\end{aligned}
$$

    

Since $det(M)=2$, we get:

$$
\begin{aligned}det(M) & =2 \\ 6-4w & =2 \\ -4w & =2-6 \\ -4w & =-4 \\ w & =1\end{aligned}
$$


### Generated variant (observed:q-11653)

If
    $M=[\begin{aligned}5 & w \\ 3 & -1\end{aligned}]$
and
$\text{det}(M)=10$, what is the value of $w?$

- $20$
- $5$
- $-20$
- $0$
- $-5$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(M) & =|\begin{aligned}5 & w \\ 3 & -1\end{aligned}| \\  & =5\cdot (-1)-w\cdot 3 \\  & =-5-3w.\end{aligned}
$$

    

Since $det(M)=10$, we get:

$$
\begin{aligned}det(M) & =10 \\ -5-3w & =10 \\ -3w & =10-(-5) \\ -3w & =15 \\ w & =-5\end{aligned}
$$


### Generated variant (authored:operations)

If
    $M=[\begin{aligned}1 & w \\ -5 & 8\end{aligned}]$
and
$\text{det}(M)=53$, what is the value of $w?$

- $-9$
- $9$
- $45$
- $\frac{53}{5}$
- $\frac{61}{5}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(M) & =|\begin{aligned}1 & w \\ -5 & 8\end{aligned}| \\  & =1\cdot 8-w\cdot (-5) \\  & =8+5w.\end{aligned}
$$

    

Since $det(M)=53$, we get:

$$
\begin{aligned}det(M) & =53 \\ 8+5w & =53 \\ 5w & =53-8 \\ 5w & =45 \\ w & =9\end{aligned}
$$


## q-127604 — original

If
    $U=[\begin{aligned}3 & -5 \\ 2k & -k+2\end{aligned}]$
and
$\text{det}(U)=-1$, what is the value of $k?$

Original choices: [["k=7", "k=-1", "k=-\\frac{3}{2}", "k=-7", "k=-\\frac{1}{4}"]]

Observed correct designations: [{":answer/id": "2cde1f0f-ce43-5b48-8b5f-a4207965af8f", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "k=-1", ":db/id": 17592186260279}]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(U) & =|\begin{aligned}3 & -5 \\ 2k & -k+2\end{aligned}| \\  & =3\cdot (-k+2)-(-5)\cdot 2k \\  & =7k+6\end{aligned}
$$

Since $det(U)=-1$, we get:

$$
\begin{aligned}det(U) & =-1 \\ 7k+6 & =-1 \\ 7k & =-1-6 \\ 7k & =-7 \\ k & =-1\end{aligned}
$$


### Parameterized replay

If
    $U=[\begin{aligned}3 & -5 \\ 2k & -k+2\end{aligned}]$
and
$\text{det}(U)=-1$, what is the value of $k?$

- $k=-\frac{3}{2}$
- $k=-1$
- $k=7$
- $k=-\frac{1}{4}$
- $k=-7$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(U) & =|\begin{aligned}3 & -5 \\ 2k & -k+2\end{aligned}| \\  & =3\cdot (-k+2)-(-5)\cdot 2k \\  & =7k+6\end{aligned}
$$

Since $det(U)=-1$, we get:

$$
\begin{aligned}det(U) & =-1 \\ 7k+6 & =-1 \\ 7k & =-1-6 \\ 7k & =-7 \\ k & =-1\end{aligned}
$$


### Generated variant (observed:q-127604)

If
    $U=[\begin{aligned}5 & 3 \\ -k & -3k+5\end{aligned}]$
and
$\text{det}(U)=-83$, what is the value of $k?$

- $k=63$
- $k=-63$
- $k=9$
- $k=\frac{9}{4}$
- $k=\frac{27}{2}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(U) & =|\begin{aligned}5 & 3 \\ -k & -3k+5\end{aligned}| \\  & =5\cdot (-3k+5)-3\cdot (-k) \\  & =-12k+25\end{aligned}
$$

Since $det(U)=-83$, we get:

$$
\begin{aligned}det(U) & =-83 \\ -12k+25 & =-83 \\ -12k & =-83-25 \\ -12k & =-108 \\ k & =9\end{aligned}
$$


### Generated variant (authored:operations)

If
    $U=[\begin{aligned}1 & -5 \\ 8k & -3k+7\end{aligned}]$
and
$\text{det}(U)=-30$, what is the value of $k?$

- $k=-\frac{30}{37}$
- $k=1$
- $k=-\frac{23}{37}$
- $k=-1$
- $k=-37$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(U) & =|\begin{aligned}1 & -5 \\ 8k & -3k+7\end{aligned}| \\  & =1\cdot (-3k+7)-(-5)\cdot 8k \\  & =37k+7\end{aligned}
$$

Since $det(U)=-30$, we get:

$$
\begin{aligned}det(U) & =-30 \\ 37k+7 & =-30 \\ 37k & =-30-7 \\ 37k & =-37 \\ k & =-1\end{aligned}
$$


## q-127606 — original

If
$T=[\begin{aligned}v & 2v \\ 2 & v+8\end{aligned}]$
and $det(T)=-4$, what is the value of $v?$

Original choices: [["v=4", "v=-2", "v=\\frac{3}{4}", "v=-3", "v=\\frac{7}{3}"]]

Observed correct designations: [{":answer/id": "6c66b584-1346-57a8-91c6-b84e73a70782", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "v=-2", ":db/id": 17592186260826}]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(T) & =|\begin{aligned}v & 2v \\ 2 & v+8\end{aligned}| \\  & =v\cdot (v+8)-2v\cdot 2 \\  & ={v}^{2}+4v\end{aligned}
$$

Since $det(T)=-4$, we obtain:

$$
\begin{aligned}det(T) & =-4 \\ {v}^{2}+4v & =-4 \\ {v}^{2}+4v+4 & =0 \\ (v+2)^{2} & =0 \\ v & =-2\end{aligned}
$$


### Parameterized replay

If
$T=[\begin{aligned}v & 2v \\ 2 & v+8\end{aligned}]$
and $det(T)=-4$, what is the value of $v?$

- $v=\frac{3}{4}$
- $v=-2$
- $v=4$
- $v=\frac{7}{3}$
- $v=-3$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(T) & =|\begin{aligned}v & 2v \\ 2 & v+8\end{aligned}| \\  & =v\cdot (v+8)-2v\cdot 2 \\  & ={v}^{2}+4v\end{aligned}
$$

Since $det(T)=-4$, we obtain:

$$
\begin{aligned}det(T) & =-4 \\ {v}^{2}+4v & =-4 \\ {v}^{2}+4v+4 & =0 \\ (v+2)^{2} & =0 \\ v & =-2\end{aligned}
$$


### Generated variant (observed:q-127606)

If
$T=[\begin{aligned}2v & 2v \\ 2 & v+8\end{aligned}]$
and $det(T)=-18$, what is the value of $v?$

- $v=6$
- $v=-3$
- $v=\frac{7}{2}$
- $v=\frac{9}{8}$
- $v=-\frac{9}{2}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(T) & =|\begin{aligned}2v & 2v \\ 2 & v+8\end{aligned}| \\  & =2v\cdot (v+8)-2v\cdot 2 \\  & =2{v}^{2}+12v\end{aligned}
$$

Since $det(T)=-18$, we obtain:

$$
\begin{aligned}det(T) & =-18 \\ 2{v}^{2}+12v & =-18 \\ 2{v}^{2}+12v+18 & =0 \\ {v}^{2}+6v+9 & =0 \\ (v+3)^{2} & =0 \\ v & =-3\end{aligned}
$$


### Generated variant (authored:operations)

If
$T=[\begin{aligned}3v & 3v \\ 2 & v-4\end{aligned}]$
and $det(T)=-27$, what is the value of $v?$

- $v=9$
- $v=6$
- $v=-3$
- $v=\frac{3}{2}$
- $v=3$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(T) & =|\begin{aligned}3v & 3v \\ 2 & v-4\end{aligned}| \\  & =3v\cdot (v-4)-3v\cdot 2 \\  & =3{v}^{2}-18v\end{aligned}
$$

Since $det(T)=-27$, we obtain:

$$
\begin{aligned}det(T) & =-27 \\ 3{v}^{2}-18v & =-27 \\ 3{v}^{2}-18v+27 & =0 \\ {v}^{2}-6v+9 & =0 \\ (v-3)^{2} & =0 \\ v & =3\end{aligned}
$$


## q-127607 — original

If
$P=[\begin{aligned}r-3 & r \\ 3 & r\end{aligned}]$
and $det(P)=-9$, what is the value of $r?$

Original choices: [["2", "-\\frac{5}{2}", "3", "\\frac{3}{4}", "9"]]

Observed correct designations: [{":answer/id": "77bbba7e-5eef-5fde-bf0b-27cf27e274ce", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "3", ":db/id": 17592186260919}]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(P) & =|\begin{aligned}r-3 & r \\ 3 & r\end{aligned}| \\  & =(r-3)\cdot r-r\cdot 3 \\  & ={r}^{2}-6r\end{aligned}
$$

Since $det(P)=-9$, we obtain:

$$
\begin{aligned}det(P) & =-9 \\ {r}^{2}-6r & =-9 \\ {r}^{2}-6r+9 & =0 \\ (r-3)^{2} & =0 \\ r & =3\end{aligned}
$$


### Parameterized replay

If
$P=[\begin{aligned}r-3 & r \\ 3 & r\end{aligned}]$
and $det(P)=-9$, what is the value of $r?$

- $3$
- $-\frac{5}{2}$
- $2$
- $9$
- $\frac{3}{4}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(P) & =|\begin{aligned}r-3 & r \\ 3 & r\end{aligned}| \\  & =(r-3)\cdot r-r\cdot 3 \\  & ={r}^{2}-6r\end{aligned}
$$

Since $det(P)=-9$, we obtain:

$$
\begin{aligned}det(P) & =-9 \\ {r}^{2}-6r & =-9 \\ {r}^{2}-6r+9 & =0 \\ (r-3)^{2} & =0 \\ r & =3\end{aligned}
$$


### Generated variant (observed:q-127607)

If
$P=[\begin{aligned}r+8 & 2r \\ 2 & 2r\end{aligned}]$
and $det(P)=-18$, what is the value of $r?$

- $-2$
- $\frac{5}{2}$
- $-9$
- $-3$
- $-\frac{3}{4}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(P) & =|\begin{aligned}r+8 & 2r \\ 2 & 2r\end{aligned}| \\  & =(r+8)\cdot 2r-2r\cdot 2 \\  & =2{r}^{2}+12r\end{aligned}
$$

Since $det(P)=-18$, we obtain:

$$
\begin{aligned}det(P) & =-18 \\ 2{r}^{2}+12r & =-18 \\ 2{r}^{2}+12r+18 & =0 \\ {r}^{2}+6r+9 & =0 \\ (r+3)^{2} & =0 \\ r & =-3\end{aligned}
$$


### Generated variant (authored:operations)

If
$P=[\begin{aligned}r-4 & 3r \\ 2 & 3r\end{aligned}]$
and $det(P)=-27$, what is the value of $r?$

- $9$
- $6$
- $-3$
- $\frac{3}{2}$
- $3$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(P) & =|\begin{aligned}r-4 & 3r \\ 2 & 3r\end{aligned}| \\  & =(r-4)\cdot 3r-3r\cdot 2 \\  & =3{r}^{2}-18r\end{aligned}
$$

Since $det(P)=-27$, we obtain:

$$
\begin{aligned}det(P) & =-27 \\ 3{r}^{2}-18r & =-27 \\ 3{r}^{2}-18r+27 & =0 \\ {r}^{2}-6r+9 & =0 \\ (r-3)^{2} & =0 \\ r & =3\end{aligned}
$$


## q-127608 — original

If
$B=[\begin{aligned}5-p & p \\ 3 & p\end{aligned}]$
and $det(B)=1$, what is the value of $p?$

Original choices: [["p=1", "p=\\frac{2}{5}", "p=\\frac{1}{3}", "p=3", "p=-5"]]

Observed correct designations: [{":answer/id": "0d8c86ed-6d17-58e5-80b8-58959792fbea", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "p=1", ":db/id": 17592186260000}]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(B) & =|\begin{aligned}5-p & p \\ 3 & p\end{aligned}| \\  & =(5-p)\cdot p-p\cdot 3 \\  & =-{p}^{2}+2p\end{aligned}
$$

Since $det(B)=1$, we obtain:

$$
\begin{aligned}det(B) & =1 \\ -{p}^{2}+2p & =1 \\ -{p}^{2}+2p-1 & =0 \\ {p}^{2}-2p+1 & =0 \\ (p-1)^{2} & =0 \\ p & =1\end{aligned}
$$


### Parameterized replay

If
$B=[\begin{aligned}5-p & p \\ 3 & p\end{aligned}]$
and $det(B)=1$, what is the value of $p?$

- $p=\frac{1}{3}$
- $p=\frac{2}{5}$
- $p=1$
- $p=-5$
- $p=3$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(B) & =|\begin{aligned}5-p & p \\ 3 & p\end{aligned}| \\  & =(5-p)\cdot p-p\cdot 3 \\  & =-{p}^{2}+2p\end{aligned}
$$

Since $det(B)=1$, we obtain:

$$
\begin{aligned}det(B) & =1 \\ -{p}^{2}+2p & =1 \\ -{p}^{2}+2p-1 & =0 \\ {p}^{2}-2p+1 & =0 \\ (p-1)^{2} & =0 \\ p & =1\end{aligned}
$$


### Generated variant (observed:q-127608)

If
$B=[\begin{aligned}-4-p & 2p \\ 2 & 2p\end{aligned}]$
and $det(B)=18$, what is the value of $p?$

- $p=-3$
- $p=-\frac{6}{5}$
- $p=15$
- $p=-\frac{3}{3}$
- $p=-9$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(B) & =|\begin{aligned}-4-p & 2p \\ 2 & 2p\end{aligned}| \\  & =(-4-p)\cdot 2p-2p\cdot 2 \\  & =-2{p}^{2}-12p\end{aligned}
$$

Since $det(B)=18$, we obtain:

$$
\begin{aligned}det(B) & =18 \\ -2{p}^{2}-12p & =18 \\ -2{p}^{2}-12p-18 & =0 \\ {p}^{2}+6p+9 & =0 \\ (p+3)^{2} & =0 \\ p & =-3\end{aligned}
$$


### Generated variant (authored:operations)

If
$B=[\begin{aligned}8-p & 3p \\ 2 & 3p\end{aligned}]$
and $det(B)=27$, what is the value of $p?$

- $p=9$
- $p=6$
- $p=-3$
- $p=\frac{3}{2}$
- $p=3$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(B) & =|\begin{aligned}8-p & 3p \\ 2 & 3p\end{aligned}| \\  & =(8-p)\cdot 3p-3p\cdot 2 \\  & =-3{p}^{2}+18p\end{aligned}
$$

Since $det(B)=27$, we obtain:

$$
\begin{aligned}det(B) & =27 \\ -3{p}^{2}+18p & =27 \\ -3{p}^{2}+18p-27 & =0 \\ {p}^{2}-6p+9 & =0 \\ (p-3)^{2} & =0 \\ p & =3\end{aligned}
$$


## q-127609 — original

If
$A=[\begin{aligned}3y & y \\ 3 & y-5\end{aligned}]$
and $det(A)=-27$, what is the value of $y?$

Original choices: [["y=3", "y=18", "y=-9", "y=\\frac{9}{2}", "y=\\frac{18}{2}"]]

Observed correct designations: [{":answer/id": "1a37c432-ec3a-54fa-a265-be8a73e5b042", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "y=3", ":db/id": 17592186260101}]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(A) & =|\begin{aligned}3y & y \\ 3 & y-5\end{aligned}| \\  & =3y\cdot (y-5)-y\cdot 3 \\  & =3{y}^{2}-18y\end{aligned}
$$

Since $det(A)=-27$, we obtain:

$$
\begin{aligned}det(A) & =-27 \\ 3{y}^{2}-18y & =-27 \\ 3{y}^{2}-18y+27 & =0 \\ {y}^{2}-6y+9 & =0 \\ (y-3)^{2} & =0 \\ y & =3\end{aligned}
$$


### Parameterized replay

If
$A=[\begin{aligned}3y & y \\ 3 & y-5\end{aligned}]$
and $det(A)=-27$, what is the value of $y?$

- $y=-9$
- $y=18$
- $y=3$
- $y=\frac{18}{2}$
- $y=\frac{9}{2}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(A) & =|\begin{aligned}3y & y \\ 3 & y-5\end{aligned}| \\  & =3y\cdot (y-5)-y\cdot 3 \\  & =3{y}^{2}-18y\end{aligned}
$$

Since $det(A)=-27$, we obtain:

$$
\begin{aligned}det(A) & =-27 \\ 3{y}^{2}-18y & =-27 \\ 3{y}^{2}-18y+27 & =0 \\ {y}^{2}-6y+9 & =0 \\ (y-3)^{2} & =0 \\ y & =3\end{aligned}
$$


### Generated variant (observed:q-127609)

If
$A=[\begin{aligned}2y & 2y \\ 2 & y+8\end{aligned}]$
and $det(A)=-18$, what is the value of $y?$

- $y=-3$
- $y=-18$
- $y=-\frac{18}{2}$
- $y=9$
- $y=-\frac{9}{2}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(A) & =|\begin{aligned}2y & 2y \\ 2 & y+8\end{aligned}| \\  & =2y\cdot (y+8)-2y\cdot 2 \\  & =2{y}^{2}+12y\end{aligned}
$$

Since $det(A)=-18$, we obtain:

$$
\begin{aligned}det(A) & =-18 \\ 2{y}^{2}+12y & =-18 \\ 2{y}^{2}+12y+18 & =0 \\ {y}^{2}+6y+9 & =0 \\ (y+3)^{2} & =0 \\ y & =-3\end{aligned}
$$


### Generated variant (authored:operations)

If
$A=[\begin{aligned}3y & 3y \\ 2 & y-4\end{aligned}]$
and $det(A)=-27$, what is the value of $y?$

- $y=9$
- $y=6$
- $y=-3$
- $y=\frac{3}{2}$
- $y=3$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(A) & =|\begin{aligned}3y & 3y \\ 2 & y-4\end{aligned}| \\  & =3y\cdot (y-4)-3y\cdot 2 \\  & =3{y}^{2}-18y\end{aligned}
$$

Since $det(A)=-27$, we obtain:

$$
\begin{aligned}det(A) & =-27 \\ 3{y}^{2}-18y & =-27 \\ 3{y}^{2}-18y+27 & =0 \\ {y}^{2}-6y+9 & =0 \\ (y-3)^{2} & =0 \\ y & =3\end{aligned}
$$


## q-275598 — original

If
    $C=[\begin{aligned}1 & k \\ 4 & 6\end{aligned}]$
and
$\text{det}(C)=-14,$ determine the value of $k.$

$k=$
{{field-1}}

Original choices: [["5"]]

Observed correct designations: [{":answer/id": "637424aa-e375-5ca5-bc92-9b93538da967", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "5", ":db/id": 17592186291058}]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}1 & k \\ 4 & 6\end{aligned}| \\  & =1\cdot 6-k\cdot 4 \\  & =6-4k.\end{aligned}
$$

Since $det(C)=-14$, we get

$$
\begin{aligned}det(C) & =-14 \\ 6-4k & =-14 \\ -4k & =-14-6 \\ -4k & =-20 \\ k & =5.\end{aligned}
$$


### Parameterized replay

If
    $C=[\begin{aligned}1 & k \\ 4 & 6\end{aligned}]$
and
$\text{det}(C)=-14,$ determine the value of $k.$

$k=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}1 & k \\ 4 & 6\end{aligned}| \\  & =1\cdot 6-k\cdot 4 \\  & =6-4k.\end{aligned}
$$

Since $det(C)=-14$, we get

$$
\begin{aligned}det(C) & =-14 \\ 6-4k & =-14 \\ -4k & =-14-6 \\ -4k & =-20 \\ k & =5.\end{aligned}
$$


### Generated variant (none)

If
    $C=[\begin{aligned}5 & k \\ 3 & -1\end{aligned}]$
and
$\text{det}(C)=10,$ determine the value of $k.$

$k=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}5 & k \\ 3 & -1\end{aligned}| \\  & =5\cdot (-1)-k\cdot 3 \\  & =-5-3k.\end{aligned}
$$

Since $det(C)=10$, we get

$$
\begin{aligned}det(C) & =10 \\ -5-3k & =10 \\ -3k & =10-(-5) \\ -3k & =15 \\ k & =-5.\end{aligned}
$$


### Generated variant (none)

If
    $C=[\begin{aligned}1 & k \\ -5 & 8\end{aligned}]$
and
$\text{det}(C)=53,$ determine the value of $k.$

$k=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}1 & k \\ -5 & 8\end{aligned}| \\  & =1\cdot 8-k\cdot (-5) \\  & =8+5k.\end{aligned}
$$

Since $det(C)=53$, we get

$$
\begin{aligned}det(C) & =53 \\ 8+5k & =53 \\ 5k & =53-8 \\ 5k & =45 \\ k & =9.\end{aligned}
$$


## q-275601 — original

If
$A=[\begin{aligned}3+p & 4p-{p}^{2} \\ 1 & 5-p\end{aligned}]$
and $det(A)=7,$ what is the value of $p?$

$p=$
{{field-1}}

Original choices: [["4"]]

Observed correct designations: [{":answer/id": "93399e4d-4d85-580e-9e08-c041fa5d5800", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "4", ":db/id": 17592186291266}]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}det(A) & =|\begin{aligned}3+p & 4p-{p}^{2} \\ 1 & 5-p\end{aligned}| \\  & =(3+p)(5-p)-(4p-{p}^{2})\cdot 1 \\  & =15-3p+5p-{p}^{2}-4p+{p}^{2} \\  & =15-2p-\cancel{{p}^{2}}+\cancel{{p}^{2}} \\  & =15-2p.\end{aligned}
$$

Finally, since $det(A)=7$, we obtain

$$
\begin{aligned}det(A) & =7 \\ 15-2p & =7 \\ -2p & =-8 \\ p & =4.\end{aligned}
$$


### Parameterized replay

If
$A=[\begin{aligned}3+p & 4p-{p}^{2} \\ 1 & 5-p\end{aligned}]$
and $det(A)=7,$ what is the value of $p?$

$p=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}det(A) & =|\begin{aligned}3+p & 4p-{p}^{2} \\ 1 & 5-p\end{aligned}| \\  & =(3+p)(5-p)-(4p-{p}^{2})\cdot 1 \\  & =15-3p+5p-{p}^{2}-4p+{p}^{2} \\  & =15-2p-\cancel{{p}^{2}}+\cancel{{p}^{2}} \\  & =15-2p.\end{aligned}
$$

Finally, since $det(A)=7$, we obtain

$$
\begin{aligned}det(A) & =7 \\ 15-2p & =7 \\ -2p & =-8 \\ p & =4.\end{aligned}
$$


### Generated variant (none)

If
$A=[\begin{aligned}5+p & 3p-{p}^{2} \\ 1 & -1-p\end{aligned}]$
and $det(A)=40,$ what is the value of $p?$

$p=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}det(A) & =|\begin{aligned}5+p & 3p-{p}^{2} \\ 1 & -1-p\end{aligned}| \\  & =(5+p)(-1-p)-(3p-{p}^{2})\cdot 1 \\  & =-5-5p-p-{p}^{2}-3p+{p}^{2} \\  & =-5-9p-\cancel{{p}^{2}}+\cancel{{p}^{2}} \\  & =-5-9p.\end{aligned}
$$

Finally, since $det(A)=40$, we obtain

$$
\begin{aligned}det(A) & =40 \\ -5-9p & =40 \\ -9p & =45 \\ p & =-5.\end{aligned}
$$


### Generated variant (none)

If
$A=[\begin{aligned}1+p & -5p-{p}^{2} \\ 1 & 8-p\end{aligned}]$
and $det(A)=116,$ what is the value of $p?$

$p=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}det(A) & =|\begin{aligned}1+p & -5p-{p}^{2} \\ 1 & 8-p\end{aligned}| \\  & =(1+p)(8-p)-(-5p-{p}^{2})\cdot 1 \\  & =8-p+8p-{p}^{2}+5p+{p}^{2} \\  & =8+12p-\cancel{{p}^{2}}+\cancel{{p}^{2}} \\  & =8+12p.\end{aligned}
$$

Finally, since $det(A)=116$, we obtain

$$
\begin{aligned}det(A) & =116 \\ 8+12p & =116 \\ 12p & =108 \\ p & =9.\end{aligned}
$$


## q-317377 — original

If
    $D=[\begin{aligned}2 & m \\ 3 & 5\end{aligned}]$
and
$\text{det}(D)=-11,$ determine the value of $m.$

$m=$
{{field-1}}

Original choices: [["7"]]

Observed correct designations: [{":answer/id": "d7fa1ff0-7dcd-55bd-a8fb-9db3d54aaf17", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "7", ":db/id": 17592186298479}]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}2 & m \\ 3 & 5\end{aligned}| \\  & =2\cdot 5-m\cdot 3 \\  & =10-3m.\end{aligned}
$$

Since $det(D)=-11,$ we get

$$
\begin{aligned}det(D) & =-11 \\ 10-3m & =-11 \\ -3m & =-21 \\ m & =7.\end{aligned}
$$


### Parameterized replay

If
    $D=[\begin{aligned}2 & m \\ 3 & 5\end{aligned}]$
and
$\text{det}(D)=-11,$ determine the value of $m.$

$m=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}2 & m \\ 3 & 5\end{aligned}| \\  & =2\cdot 5-m\cdot 3 \\  & =10-3m.\end{aligned}
$$

Since $det(D)=-11,$ we get

$$
\begin{aligned}det(D) & =-11 \\ 10-3m & =-11 \\ -3m & =-21 \\ m & =7.\end{aligned}
$$


### Generated variant (none)

If
    $D=[\begin{aligned}5 & m \\ 3 & -1\end{aligned}]$
and
$\text{det}(D)=10,$ determine the value of $m.$

$m=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}5 & m \\ 3 & -1\end{aligned}| \\  & =5\cdot (-1)-m\cdot 3 \\  & =-5-3m.\end{aligned}
$$

Since $det(D)=10,$ we get

$$
\begin{aligned}det(D) & =10 \\ -5-3m & =10 \\ -3m & =15 \\ m & =-5.\end{aligned}
$$


### Generated variant (none)

If
    $D=[\begin{aligned}1 & m \\ -5 & 8\end{aligned}]$
and
$\text{det}(D)=53,$ determine the value of $m.$

$m=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}1 & m \\ -5 & 8\end{aligned}| \\  & =1\cdot 8-m\cdot (-5) \\  & =8+5m.\end{aligned}
$$

Since $det(D)=53,$ we get

$$
\begin{aligned}det(D) & =53 \\ 8+5m & =53 \\ 5m & =45 \\ m & =9.\end{aligned}
$$


## q-317382 — original

If
$U=[\begin{aligned}1+r & 2-r \\ -5 & 4\end{aligned}]$
and $det(U)=-6$, what is the value of $r?$

$r=$
{{field-1}}

Original choices: [["20"]]

Observed correct designations: [{":answer/id": "e2846b11-7ae8-5649-abfa-db38bcffb861", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "20", ":db/id": 17592186298524}]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}det(U) & =|\begin{aligned}1+r & 2-r \\ -5 & 4\end{aligned}| \\  & =(1+r)\cdot 4-(2-r)\cdot (-5) \\  & =4+4r+10-5r \\  & =14-r.\end{aligned}
$$

Since $det(U)=-6,$ we get

$$
\begin{aligned}det(U) & =-6 \\ 14-r & =-6 \\ -r & =-20 \\ r & =20.\end{aligned}
$$


### Parameterized replay

If
$U=[\begin{aligned}1+r & 2-r \\ -5 & 4\end{aligned}]$
and $det(U)=-6$, what is the value of $r?$

$r=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}det(U) & =|\begin{aligned}1+r & 2-r \\ -5 & 4\end{aligned}| \\  & =(1+r)\cdot 4-(2-r)\cdot (-5) \\  & =4+4r+10-5r \\  & =14-r.\end{aligned}
$$

Since $det(U)=-6,$ we get

$$
\begin{aligned}det(U) & =-6 \\ 14-r & =-6 \\ -r & =-20 \\ r & =20.\end{aligned}
$$


### Generated variant (none)

If
$U=[\begin{aligned}5+3r & -1-3r \\ 5 & 2\end{aligned}]$
and $det(U)=183$, what is the value of $r?$

$r=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}det(U) & =|\begin{aligned}5+3r & -1-3r \\ 5 & 2\end{aligned}| \\  & =(5+3r)\cdot 2-(-1-3r)\cdot 5 \\  & =10+6r+5+15r \\  & =15+21r.\end{aligned}
$$

Since $det(U)=183,$ we get

$$
\begin{aligned}det(U) & =183 \\ 15+21r & =183 \\ 21r & =168 \\ r & =8.\end{aligned}
$$


### Generated variant (none)

If
$U=[\begin{aligned}1-5r & 8-3r \\ 7 & 2\end{aligned}]$
and $det(U)=45$, what is the value of $r?$

$r=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}det(U) & =|\begin{aligned}1-5r & 8-3r \\ 7 & 2\end{aligned}| \\  & =(1-5r)\cdot 2-(8-3r)\cdot 7 \\  & =2-10r-56+21r \\  & =-54+11r.\end{aligned}
$$

Since $det(U)=45,$ we get

$$
\begin{aligned}det(U) & =45 \\ -54+11r & =45 \\ 11r & =99 \\ r & =9.\end{aligned}
$$


## q-317385 — original

If
$S=[\begin{aligned}3+s & 2s \\ -4 & 3-s\end{aligned}]$
and $det(S)=25,$ what is the value of $s?$

$s=$
{{field-1}}

Original choices: [["4"]]

Observed correct designations: [{":answer/id": "8cb2781e-f836-5ab8-a7a5-4a709b95dddb", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "4", ":db/id": 17592186298164}]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}det(S) & =|\begin{aligned}3+s & 2s \\ -4 & 3-s\end{aligned}| \\  & =(3+s)(3-s)-2s(-4) \\  & =9-{s}^{2}+8s \\  & =-{s}^{2}+8s+9.\end{aligned}
$$

Since $det(S)=25,$ we get

$$
\begin{aligned}det(S) & =25 \\ -{s}^{2}+8s+9 & =25 \\ -{s}^{2}+8s-16 & =0 \\ {s}^{2}-8s+16 & =0 \\ (s-4)^{2} & =0 \\ s & =4.\end{aligned}
$$


### Parameterized replay

If
$S=[\begin{aligned}3+s & 2s \\ -4 & 3-s\end{aligned}]$
and $det(S)=25,$ what is the value of $s?$

$s=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}det(S) & =|\begin{aligned}3+s & 2s \\ -4 & 3-s\end{aligned}| \\  & =(3+s)(3-s)-2s(-4) \\  & =9-{s}^{2}+8s \\  & =-{s}^{2}+8s+9.\end{aligned}
$$

Since $det(S)=25,$ we get

$$
\begin{aligned}det(S) & =25 \\ -{s}^{2}+8s+9 & =25 \\ -{s}^{2}+8s-16 & =0 \\ {s}^{2}-8s+16 & =0 \\ (s-4)^{2} & =0 \\ s & =4.\end{aligned}
$$


### Generated variant (none)

If
$S=[\begin{aligned}4+s & 3s \\ -4 & 4-s\end{aligned}]$
and $det(S)=52,$ what is the value of $s?$

$s=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}det(S) & =|\begin{aligned}4+s & 3s \\ -4 & 4-s\end{aligned}| \\  & =(4+s)(4-s)-3s(-4) \\  & =16-{s}^{2}+12s \\  & =-{s}^{2}+12s+16.\end{aligned}
$$

Since $det(S)=52,$ we get

$$
\begin{aligned}det(S) & =52 \\ -{s}^{2}+12s+16 & =52 \\ -{s}^{2}+12s-36 & =0 \\ {s}^{2}-12s+36 & =0 \\ (s-6)^{2} & =0 \\ s & =6.\end{aligned}
$$


### Generated variant (none)

If
$S=[\begin{aligned}3+s & s \\ 4 & 3-s\end{aligned}]$
and $det(S)=13,$ what is the value of $s?$

$s=$
{{field-1}}



For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}det(S) & =|\begin{aligned}3+s & s \\ 4 & 3-s\end{aligned}| \\  & =(3+s)(3-s)-s(4) \\  & =9-{s}^{2}-4s \\  & =-{s}^{2}-4s+9.\end{aligned}
$$

Since $det(S)=13,$ we get

$$
\begin{aligned}det(S) & =13 \\ -{s}^{2}-4s+9 & =13 \\ -{s}^{2}-4s-4 & =0 \\ {s}^{2}+4s+4 & =0 \\ (s+2)^{2} & =0 \\ s & =-2.\end{aligned}
$$


## q-69661 — original

If
$S=[\begin{aligned}1-p & 1+p \\ -3 & 2\end{aligned}]$
and $det(S)=2$, what is the value of $p?$

Original choices: [["2", "-6", "-2", "-3", "3"]]

Observed correct designations: [{":answer/id": "9e476a33-a9f4-5b54-ad86-0d592acad0c2", ":answer/type": {":db/ident": ":answer.type/math"}, ":answer/value": "-3", ":db/id": 17592186334384}]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(S) & =|\begin{aligned}1-p & 1+p \\ -3 & 2\end{aligned}| \\  & =(1-p)\cdot 2-(1+p)\cdot (-3) \\  & =2-2p+3+3p \\  & =5+p\end{aligned}
$$

Since $det(S)=2$, we obtain:

$$
\begin{aligned}det(S) & =2 \\ 5+p & =2 \\ p & =2-5 \\ p & =-3\end{aligned}
$$


### Parameterized replay

If
$S=[\begin{aligned}1-p & 1+p \\ -3 & 2\end{aligned}]$
and $det(S)=2$, what is the value of $p?$

- $-2$
- $-6$
- $2$
- $3$
- $-3$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(S) & =|\begin{aligned}1-p & 1+p \\ -3 & 2\end{aligned}| \\  & =(1-p)\cdot 2-(1+p)\cdot (-3) \\  & =2-2p+3+3p \\  & =5+p\end{aligned}
$$

Since $det(S)=2$, we obtain:

$$
\begin{aligned}det(S) & =2 \\ 5+p & =2 \\ p & =2-5 \\ p & =-3\end{aligned}
$$


### Generated variant (observed:q-69661)

If
$S=[\begin{aligned}5+3p & -1-3p \\ 5 & 2\end{aligned}]$
and $det(S)=183$, what is the value of $p?$

- $16$
- $-\frac{16}{3}$
- $-8$
- $8$
- $\frac{16}{3}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(S) & =|\begin{aligned}5+3p & -1-3p \\ 5 & 2\end{aligned}| \\  & =(5+3p)\cdot 2-(-1-3p)\cdot 5 \\  & =10+6p+5+15p \\  & =15+21p\end{aligned}
$$

Since $det(S)=183$, we obtain:

$$
\begin{aligned}det(S) & =183 \\ 15+21p & =183 \\ 21p & =183-15 \\ 21p & =168 \\ p & =8\end{aligned}
$$


### Generated variant (authored:operations)

If
$S=[\begin{aligned}1-5p & 8-3p \\ 7 & 2\end{aligned}]$
and $det(S)=45$, what is the value of $p?$

- $-9$
- $99$
- $-\frac{9}{11}$
- $\frac{45}{11}$
- $9$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}det(S) & =|\begin{aligned}1-5p & 8-3p \\ 7 & 2\end{aligned}| \\  & =(1-5p)\cdot 2-(8-3p)\cdot 7 \\  & =2-10p-56+21p \\  & =-54+11p\end{aligned}
$$

Since $det(S)=45$, we obtain:

$$
\begin{aligned}det(S) & =45 \\ -54+11p & =45 \\ 11p & =45-(-54) \\ 11p & =99 \\ p & =9\end{aligned}
$$
