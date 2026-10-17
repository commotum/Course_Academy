### easy / q-22063 / boolean-pairs

<div class="matrix-operands">
<div>$A=\begin{bmatrix}7 & 4 \\ -3 & 9 \\ -7 & -6 \\ -9 & 3\end{bmatrix}$</div>
<div>$B=\begin{bmatrix}1 & -3 & -3 & 1 \\ 3 & 2 & -2 & -3\end{bmatrix}$</div>
<div>$C=\begin{bmatrix}-3 \\ 4\end{bmatrix}$</div>
</div>

Which of the following statements are true regarding the matrices $A,B,$ and $C?$

Select all that apply.

Field The product $AC$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Field The product $CB$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Field The product $BC$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $A$ is a $4\times 2$ matrix, $B$ is a $2\times 4$ matrix, and $C$ is a $2\times 1$ column vector

There are $2$ columns in $A$ and $2$ rows in $C.$ Since the number of columns in $A$ equals the number of rows in $C,$ the matrices $A$ and $C$ are conformable for multiplication:

$$
{A}_{4\times \boxed{\text{2}}}{\times }_{✓}{C}_{\boxed{\text{2}}\times 1}=\text{well defined}
$$

On the other hand, there is $1$ column in $C$ and $2$ rows in $B.$ Since the number of columns in $C$ does **not** equal the number of rows in $B,$ the matrices $C$ and $B$ are **not** conformable for multiplication:

$$
{C}_{2\times 1}{\times }_{\ne }{B}_{2\times 4}=\text{undefined}
$$

Finally, there are $4$ columns in $B$ and $2$ rows in $C.$ Since the number of columns in $B$ does **not** equal the number of rows in $C,$ the matrices $B$ and $C$ are **not** conformable for multiplication:

$$
{B}_{2\times 4}{\times }_{\ne }{C}_{2\times 1}=\text{undefined}
$$

The product $AC$ is well defined. The products $CB$ and $BC$ are undefined.

### easy / q-42374 / boolean-pairs

<div class="matrix-operands">
<div>$A=\begin{bmatrix}-2 & 8 \\ 5 & 7 \\ 4 & -3 \\ 9 & -7\end{bmatrix}$</div>
<div>$B=\begin{bmatrix}-6 & -9 \\ 3 & 1 \\ -3 & -3 \\ 1 & 3\end{bmatrix}$</div>
<div>$C=\begin{bmatrix}2 & -2 & -3 & -3 \\ 4 & 9 & 8 & -8\end{bmatrix}$</div>
</div>

Which of the following statements are true regarding the matrices $A,B,$ and $C?$

Select all that apply.

Field The product $AB$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Field The product $CB$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Field The product $AC$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $A$ is a $4\times 2$ matrix, $B$ is a $4\times 2$ matrix, and $C$ is a $2\times 4$ matrix.

There are $2$ columns in $A$ and $4$ rows in $B.$ Since the number of columns in $A$ does **not** equal the number of rows in $B,$ the matrices $A$ and $B$ are **not** conformable for multiplication:

$$
{A}_{4\times 2}{\times }_{\ne }{B}_{4\times 2}=\text{undefined}
$$

On the other hand, there are $4$ columns in $C$ and $4$ rows in $B.$ Since the number of columns in $C$ equals the number of rows in $B,$ the matrices $C$ and $B$ are conformable for multiplication:

$$
{C}_{2\times \boxed{\text{4}}}{\times }_{✓}{B}_{\boxed{\text{4}}\times 2}=\text{well defined}
$$

Finally, there are $2$ columns in $A$ and $2$ rows in $C.$ Since the number of columns in $A$ equals the number of rows in $C,$ the matrices $A$ and $C$ are conformable for multiplication:

$$
{A}_{4\times \boxed{\text{2}}}{\times }_{✓}{C}_{\boxed{\text{2}}\times 4}=\text{well defined}
$$

The products $CB$ and $AC$ are well defined. The product $AB$ is undefined.

### moderate / q-129437 / boolean-pairs

<div class="matrix-operands">
<div>$P=\begin{bmatrix}0 & 1 & 9 \\ 3 & 6 & 1 \\ -3 & -6 & 0\end{bmatrix}$</div>
<div>$R=\begin{bmatrix}-4 & 8 & 8\end{bmatrix}$</div>
<div>$S=\begin{bmatrix}0 & -7 & -4 & -3 & -9\end{bmatrix}$</div>
</div>

Which of the following statements are true regarding the matrices $P,R,$ and $S?$

Select all that apply.

Field The product $PR$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Field The product $RP$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Field The product $SP$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $P$ is a $3\times 3$ matrix, $R$ is a $1\times 3$ row vector, and $S$ is a $1\times 5$ row vector. 

There are $3$ columns in $P$ and $1$ row in $R.$ Since the number of columns in $P$ does **not** equal the number of rows in $R,$ the matrices $P$ and $R$ are **not** conformable for multiplication:

$$
{P}_{3\times 3}{\times }_{\ne }{R}_{1\times 3}=\text{undefined}
$$

On the other hand, there are $3$ columns in $R$ and $3$ rows in $P.$ Since the number of columns in $R$ equals the number of rows in $P,$ the matrices $R$ and $P$ are conformable for multiplication:

$$
{R}_{1\times \boxed{\text{3}}}{\times }_{✓}{P}_{\boxed{\text{3}}\times 3}=\text{well defined}
$$

Finally, there are $5$ columns in $S$ and $3$ rows in $P.$ Since the number of columns in $S$ does **not** equal the number of rows in $P,$ the matrices $S$ and $P$ are **not** conformable for multiplication:

$$
{S}_{1\times 5}{\times }_{\ne }{P}_{3\times 3}=\text{undefined}
$$

The product $RP$ is well defined. The products $PR$ and $SP$ are undefined.

### easy / q-22055 / boolean-pairs

<div class="matrix-operands">
<div>$X=\begin{bmatrix}-2 & 8 \\ 5 & 7 \\ 4 & -3 \\ 9 & -7\end{bmatrix}$</div>
<div>$Y=\begin{bmatrix}-6 & -9 \\ 3 & 1 \\ -3 & -3 \\ 1 & 3\end{bmatrix}$</div>
<div>$Z=\begin{bmatrix}2 & -2 & -3 & -3 \\ 4 & 9 & 8 & -8\end{bmatrix}$</div>
</div>

Which of the following statements are true regarding the matrices $X,Y,$ and $Z?$

Select all that apply.

Field The product $XY$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Field The product $ZY$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Field The product $XZ$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $X$ is a $4\times 2$ matrix, $Y$ is a $4\times 2$ matrix, and $Z$ is a $2\times 4$ matrix.

There are $2$ columns in $X$ and $4$ rows in $Y.$ Since the number of columns in $X$ does **not** equal the number of rows in $Y,$ the matrices $X$ and $Y$ are **not** conformable for multiplication:

$$
{X}_{4\times 2}{\times }_{\ne }{Y}_{4\times 2}=\text{undefined}
$$

On the other hand, there are $4$ columns in $Z$ and $4$ rows in $Y.$ Since the number of columns in $Z$ equals the number of rows in $Y,$ the matrices $Z$ and $Y$ are conformable for multiplication:

$$
{Z}_{2\times \boxed{\text{4}}}{\times }_{✓}{Y}_{\boxed{\text{4}}\times 2}=\text{well defined}
$$

Finally, there are $2$ columns in $X$ and $2$ rows in $Z.$ Since the number of columns in $X$ equals the number of rows in $Z,$ the matrices $X$ and $Z$ are conformable for multiplication:

$$
{X}_{4\times \boxed{\text{2}}}{\times }_{✓}{Z}_{\boxed{\text{2}}\times 4}=\text{well defined}
$$

The products $ZY$ and $XZ$ are well defined. The product $XY$ is undefined.

### easy / q-22056 / boolean-pairs

<div class="matrix-operands">
<div>$R=\begin{bmatrix}-2 & 8 \\ 5 & 7 \\ 4 & -3 \\ 9 & -7\end{bmatrix}$</div>
<div>$S=\begin{bmatrix}-6 & -9 \\ 3 & 1 \\ -3 & -3 \\ 1 & 3\end{bmatrix}$</div>
<div>$T=\begin{bmatrix}2 & -2 & -3 & -3 \\ 4 & 9 & 8 & -8\end{bmatrix}$</div>
</div>

Which of the following statements are true regarding the matrices $R,S,$ and $T?$

Select all that apply.

Field The product $RS$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Field The product $TS$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Field The product $RT$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $R$ is a $4\times 2$ matrix, $S$ is a $4\times 2$ matrix, and $T$ is a $2\times 4$ matrix.

There are $2$ columns in $R$ and $4$ rows in $S.$ Since the number of columns in $R$ does **not** equal the number of rows in $S,$ the matrices $R$ and $S$ are **not** conformable for multiplication:

$$
{R}_{4\times 2}{\times }_{\ne }{S}_{4\times 2}=\text{undefined}
$$

On the other hand, there are $4$ columns in $T$ and $4$ rows in $S.$ Since the number of columns in $T$ equals the number of rows in $S,$ the matrices $T$ and $S$ are conformable for multiplication:

$$
{T}_{2\times \boxed{\text{4}}}{\times }_{✓}{S}_{\boxed{\text{4}}\times 2}=\text{well defined}
$$

Finally, there are $2$ columns in $R$ and $2$ rows in $T.$ Since the number of columns in $R$ equals the number of rows in $T,$ the matrices $R$ and $T$ are conformable for multiplication:

$$
{R}_{4\times \boxed{\text{2}}}{\times }_{✓}{T}_{\boxed{\text{2}}\times 4}=\text{well defined}
$$

The products $TS$ and $RT$ are well defined. The product $RS$ is undefined.

### moderate / q-22062 / boolean-pairs

<div class="matrix-operands">
<div>$P=\begin{bmatrix}-5 & -6\end{bmatrix}$</div>
<div>$R=\begin{bmatrix}8 & -2 & -5 & -5 & -8\end{bmatrix}$</div>
<div>$S=\begin{bmatrix}-8 & -5 & -2 \\ 8 & 5 & 7\end{bmatrix}$</div>
</div>

Which of the following statements are true regarding the matrices $P,R,$ and $S?$

Select all that apply.

Field The product $RS$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Field The product $PS$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Field The product $PR$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $P$ is a $1\times 2$ row vector, $R$ is a $1\times 5$ row vector, and $S$ is a $2\times 3$ matrix.

There are $5$ columns in $R$ and $2$ rows in $S.$ Since the number of columns in $R$ does **not** equal the number of rows in $S,$ the matrices $R$ and $S$ are **not** conformable for multiplication:

$$
{R}_{1\times 5}{\times }_{\ne }{S}_{2\times 3}=\text{undefined}
$$

On the other hand, there are $2$ columns in $P$ and $2$ rows in $S.$ Since the number of columns in $P$ equals the number of rows in $S,$ the matrices $P$ and $S$ are conformable for multiplication:

$$
{P}_{1\times \boxed{\text{2}}}{\times }_{✓}{S}_{\boxed{\text{2}}\times 3}=\text{well defined}
$$

Finally, there are $2$ columns in $P$ and $1$ row in $R.$ Since the number of columns in $P$ does **not** equal the number of rows in $R,$ the matrices $P$ and $R$ are **not** conformable for multiplication:

$$
{P}_{1\times 2}{\times }_{\ne }{R}_{1\times 5}=\text{undefined}
$$

The product $PS$ is well defined. The products $RS$ and $PR$ are undefined.

### easy / q-42375 / boolean-pairs

<div class="matrix-operands">
<div>$J=\begin{bmatrix}-2 & 8 \\ 5 & 7 \\ 4 & -3 \\ 9 & -7\end{bmatrix}$</div>
<div>$K=\begin{bmatrix}-6 & -9 \\ 3 & 1 \\ -3 & -3 \\ 1 & 3\end{bmatrix}$</div>
<div>$L=\begin{bmatrix}2 & -2 & -3 & -3 \\ 4 & 9 & 8 & -8\end{bmatrix}$</div>
</div>

Which of the following statements are true regarding the matrices $J,K,$ and $L?$

Select all that apply.

Field The product $JK$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Field The product $LK$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Field The product $JL$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $J$ is a $4\times 2$ matrix, $K$ is a $4\times 2$ matrix, and $L$ is a $2\times 4$ matrix.

There are $2$ columns in $J$ and $4$ rows in $K.$ Since the number of columns in $J$ does **not** equal the number of rows in $K,$ the matrices $J$ and $K$ are **not** conformable for multiplication:

$$
{J}_{4\times 2}{\times }_{\ne }{K}_{4\times 2}=\text{undefined}
$$

On the other hand, there are $4$ columns in $L$ and $4$ rows in $K.$ Since the number of columns in $L$ equals the number of rows in $K$, the matrices $L$ and $K$ are conformable for multiplication:

$$
{L}_{2\times \boxed{\text{4}}}{\times }_{✓}{K}_{\boxed{\text{4}}\times 2}=\text{well defined}
$$

Finally, there are $2$ columns in $J$ and $2$ rows in $L.$ Since the number of columns in $J$ equals the number of rows in $L$, the matrices $J$ and $L$ are conformable for multiplication:

$$
{J}_{4\times \boxed{\text{2}}}{\times }_{✓}{L}_{\boxed{\text{2}}\times 4}=\text{well defined}
$$

The products $LK$ and $JL$ are well defined. The product $JK$ is undefined.

### easy / q-42376 / boolean-pairs

<div class="matrix-operands">
<div>$D=\begin{bmatrix}-2 & 8 \\ 5 & 7 \\ 4 & -3 \\ 9 & -7\end{bmatrix}$</div>
<div>$E=\begin{bmatrix}-6 & -9 \\ 3 & 1 \\ -3 & -3 \\ 1 & 3\end{bmatrix}$</div>
<div>$F=\begin{bmatrix}2 & -2 & -3 & -3 \\ 4 & 9 & 8 & -8\end{bmatrix}$</div>
</div>

Which of the following statements are true regarding the matrices $D,E,$ and $F?$

Select all that apply.

Field The product $DE$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Field The product $FE$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Field The product $DF$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $D$ is a $4\times 2$ matrix, $E$ is a $4\times 2$ matrix, and $F$ is a $2\times 4$ matrix.

There are $2$ columns in $D$ and $4$ rows in $E.$ Since the number of columns in $D$ does **not** equal the number of rows in $E,$ the matrices $D$ and $E$ are **not** conformable for multiplication:

$$
{D}_{4\times 2}{\times }_{\ne }{E}_{4\times 2}=\text{undefined}
$$

On the other hand, there are $4$ columns in $F$ and $4$ rows in $E.$ Since the number of columns in $F$ equals the number of rows in $E,$ the matrices $F$ and $E$ are conformable for multiplication:

$$
{F}_{2\times \boxed{\text{4}}}{\times }_{✓}{E}_{\boxed{\text{4}}\times 2}=\text{well defined}
$$

Finally, there are $2$ columns in $D$ and $2$ rows in $F.$ Since the number of columns in $D$ equals the number of rows in $F,$ the matrices $D$ and $F$ are conformable for multiplication:

$$
{D}_{4\times \boxed{\text{2}}}{\times }_{✓}{F}_{\boxed{\text{2}}\times 4}=\text{well defined}
$$

The products $FE$ and $DF$ are well defined. The product $DE$ is undefined.

### easy / q-42377 / boolean-pairs

<div class="matrix-operands">
<div>$L=\begin{bmatrix}-2 & 8 \\ 5 & 7 \\ 4 & -3 \\ 9 & -7\end{bmatrix}$</div>
<div>$M=\begin{bmatrix}-6 & -9 \\ 3 & 1 \\ -3 & -3 \\ 1 & 3\end{bmatrix}$</div>
<div>$N=\begin{bmatrix}2 & -2 & -3 & -3 \\ 4 & 9 & 8 & -8\end{bmatrix}$</div>
</div>

Which of the following statements are true regarding the matrices $L,M,$ and $N?$

Select all that apply.

Field The product $LM$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Field The product $NM$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Field The product $LN$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $L$ is a $4\times 2$ matrix, $M$ is a $4\times 2$ matrix, and $N$ is a $2\times 4$ matrix.

There are $2$ columns in $L$ and $4$ rows in $M.$ Since the number of columns in $L$ does **not** equal the number of rows in $M,$ the matrices $L$ and $M$ are **not** conformable for multiplication:

$$
{L}_{4\times 2}{\times }_{\ne }{M}_{4\times 2}=\text{undefined}
$$

On the other hand, there are $4$ columns in $N$ and $4$ rows in $M.$ Since the number of columns in $N$ equals the number of rows in $M,$ the matrices $N$ and $M$ are conformable for multiplication:

$$
{N}_{2\times \boxed{\text{4}}}{\times }_{✓}{M}_{\boxed{\text{4}}\times 2}=\text{well defined}
$$

Finally, there are $2$ columns in $L$ and $2$ rows in $N.$ Since the number of columns in $L$ equals the number of rows in $N,$ the matrices $L$ and $N$ are conformable for multiplication:

$$
{L}_{4\times \boxed{\text{2}}}{\times }_{✓}{N}_{\boxed{\text{2}}\times 4}=\text{well defined}
$$

The products $NM$ and $LN$ are well defined. The product $LM$ is undefined.

### moderate / q-42381 / boolean-pairs

<div class="matrix-operands">
<div>$O=\begin{bmatrix}7 & 4 & -3 & 9 & -7 \\ -6 & -9 & 3 & 1 & -3 \\ -3 & 1 & 3 & 2 & -2 \\ -3 & -3 & 4 & 9 & 8\end{bmatrix}$</div>
<div>$P=\begin{bmatrix}-8 & -8 \\ -4 & 2\end{bmatrix}$</div>
<div>$R=\begin{bmatrix}-5 & -3\end{bmatrix}$</div>
</div>

Which of the following statements are true regarding the matrices $O,P,$ and $R?$

Select all that apply.

Field The product $OR$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Field The product $RP$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Field The product $PR$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $O$ is a $4\times 5$ matrix, $P$ is a $2\times 2$ matrix, and $R$ is a $1\times 2$ row vector.

There are $5$ columns in $O$ and $1$ row in $R.$ Since the number of columns in $O$ does **not** equal the number of rows in $R,$ the matrices $O$ and $R$ are **not** conformable for multiplication:

$$
{O}_{4\times 5}{\times }_{\ne }{R}_{1\times 2}=\text{undefined}
$$

On the other hand, there are $2$ columns in $R$ and $2$ rows in $P.$ Since the number of columns in $R$ equals the number of rows in $P,$ the matrices $R$ and $P$ are conformable for multiplication:

$$
{R}_{1\times \boxed{\text{2}}}{\times }_{✓}{P}_{\boxed{\text{2}}\times 2}=\text{well defined}
$$

Finally, there are $2$ columns in $P$ and $1$ row in $R.$ Since the number of columns in $P$ does **not** equal the number of rows in $R,$ the matrices $P$ and $R$ are **not** conformable for multiplication:

$$
{P}_{2\times 2}{\times }_{\ne }{R}_{1\times 2}=\text{undefined}
$$

The product $RP$ is well defined. The products $OR$ and $PR$ are undefined.

### hard / mixed-orientations / boolean-pairs

<div class="matrix-operands">
<div>$O=\begin{bmatrix}-5 & -5 & -8 & -8 \\ -5 & -2 & 8 & 5\end{bmatrix}$</div>
<div>$P=\begin{bmatrix}7 & 4\end{bmatrix}$</div>
<div>$R=\begin{bmatrix}-3 \\ 9 \\ -7\end{bmatrix}$</div>
</div>

Which of the following statements are true regarding the matrices $O,P,$ and $R?$

Select all that apply.

Field The product $RP$ is well defined. (:answer-field.type/checkbox)

- false

- true **correct**

Field The product $PR$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Field The product $OP$ is well defined. (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $O$ is a $2\times 4$ matrix, $P$ is a $1\times 2$ row vector, and $R$ is a $3\times 1$ column vector.

There is $1$ column in $R$ and $1$ row in $P.$ Since the number of columns in $R$ equals the number of rows in $P,$ the matrices $R$ and $P$ are conformable for multiplication:

$$
{R}_{3\times \boxed{\text{1}}}{\times }_{✓}{P}_{\boxed{\text{1}}\times 2}=\text{well defined}
$$

On the other hand, there are $2$ columns in $P$ and $3$ rows in $R.$ Since the number of columns in $P$ does **not** equal the number of rows in $R,$ the matrices $P$ and $R$ are **not** conformable for multiplication:

$$
{P}_{1\times 2}{\times }_{\ne }{R}_{3\times 1}=\text{undefined}
$$

Finally, there are $4$ columns in $O$ and $1$ row in $P.$ Since the number of columns in $O$ does **not** equal the number of rows in $P,$ the matrices $O$ and $P$ are **not** conformable for multiplication:

$$
{O}_{2\times 4}{\times }_{\ne }{P}_{1\times 2}=\text{undefined}
$$

The product $RP$ is well defined. The products $PR$ and $OP$ are undefined.