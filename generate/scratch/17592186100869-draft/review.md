# Original MA practice replays

### easy / q-22063 / raw-q-22063

$$
A=\begin{bmatrix}1 & 2 & 6 \\ 0 & 7 & 7 \\ 8 & 8 & 8\end{bmatrix},\,B=\begin{bmatrix}1 & 0 \\ -1 & 0 \\ 0 & 0\end{bmatrix},\,C=\begin{bmatrix}1 \\ -3 \\ 2\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $A,B,$ and $C?$

Select all that apply.

- **I.** The product $AB$ is well defined
- **II.** The product $BA$ is well defined
- **III.** The product $AC$ is well defined

Field I (:answer-field.type/checkbox)

- false

- true **correct**

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $A$ is a $3\times 3$ matrix, $B$ is a $3\times 2$ matrix, and $C$ is a $3\times 1$ column vector

There are $3$ columns in $A$ and $3$ rows in $B.$ Since the number of columns in $A$ equals the number of rows in $B,$ the matrices $A$ and $B$ are conformable for multiplication:

$$
{A}_{3\times \boxed{\text{3}}}{\times }_{✓}{B}_{\boxed{\text{3}}\times 2}=\text{well defined}
$$

On the other hand, there are $2$ columns in $B$ and $3$ rows in $A.$ Since the number of columns in $B$ does **not** equal the number of rows in $A,$ the matrices $B$ and $A$ are **not** conformable for multiplication:

$$
{B}_{3\times 2}{\times }_{\ne }{A}_{3\times 3}=\text{undefined}
$$

Finally, there are $3$ columns in $A$ and $3$ rows in $C.$ Since the number of columns in $A$ equals the number of rows in $C,$ the matrices $A$ and $C$ are conformable for multiplication:

$$
{A}_{3\times \boxed{\text{3}}}{\times }_{✓}{C}_{\boxed{\text{3}}\times 1}=\text{well defined}
$$

Therefore, statements I and III are true, while statement II is false.

### easy / q-42374 / raw-q-42374

$$
A=\begin{bmatrix}1 & -1 \\ 1 & 2 \\ 5 & 3 \\ -2 & 1\end{bmatrix},\,B=\begin{bmatrix}5 & -2 & 1 & 7 \\ -1 & 3 & 3 & 0\end{bmatrix},\,C=\begin{bmatrix}2 & 5 \\ -0 & 6\end{bmatrix},
$$

Which of the following statement are true regarding the matrices $A,B,$ and $C?$

I. The product $AB$ is well defined
II. The product $BA$ is well defined
III. The product $AC$ is well defined

Select all that apply.

Field I (:answer-field.type/checkbox)

- false

- true **correct**

Field II (:answer-field.type/checkbox)

- false

- true **correct**

Field III (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $A$ is a $4\times 2$ matrix, $B$ is a $2\times 4$ matrix, and $C$ is a $2\times 2$ matrix.

There are $2$ columns in $A$ and $2$ rows in $B.$ Since the number of columns in $A$ equals the number of rows in $B,$ the matrices $A$ and $B$ are conformable for multiplication:

$$
{A}_{4\times \boxed{\text{2}}}{\times }_{✓}{B}_{\boxed{\text{2}}\times 4}=\text{well defined}
$$

On the other hand, there are $4$ columns in $B$ and $4$ rows in $A.$ Since the number of columns in $B$ equals the number of rows in $A,$ the matrices $B$ and $A$ are conformable for multiplication:

$$
{B}_{2\times \boxed{\text{4}}}{\times }_{✓}{A}_{\boxed{\text{4}}\times 2}=\text{well defined}
$$

Finally, there are $2$ columns in $A$ and $2$ rows in $C.$ Since the number of columns in $A$ equals the number of rows in $C,$ the matrices $A$ and $C$ are conformable for multiplication:

$$
{A}_{4\times \boxed{\text{2}}}{\times }_{✓}{C}_{\boxed{\text{2}}\times 2}=\text{well defined}
$$

We conclude that all three statements are true.

### moderate / q-129437 / raw-q-129437

$$
P=\begin{bmatrix}1 & 0 & 0 \\ 0 & 2 & 0 \\ 3 & 0 & 0 \\ 0 & 4 & 0 \\ 5 & 0 & 0\end{bmatrix},\,R=\begin{bmatrix}1 & 2 & 3\end{bmatrix},\,S=\begin{bmatrix}1 & 2 & 3 & 4 & 5\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $P,R,$ and $S?$

Select all that apply.

- **I.** The product $RS$ is well defined
- **II.** The product $RP$ is well defined
- **III.** The product $SP$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $P$ is a $5\times 3$ matrix, $R$ is a $1\times 3$ row vector, and $S$ is a $1\times 5$ row vector. 

There are $3$ columns in $R$ and $1$ row in $S.$ Since the number of columns in $R$ does **not** equal the number of rows in $S,$ the matrices $R$ and $S$ are **not** conformable for multiplication:

$$
{R}_{1\times 3}{\times }_{\ne }{S}_{1\times 5}=\text{undefined}
$$

On the other hand, there are $3$ columns in $R$ and $5$ rows in $P.$ Since the number of columns in $R$ does **not** equal the number of rows in $P,$ the matrices $R$ and $P$ are **not** conformable for multiplication:

$$
{R}_{1\times 3}{\times }_{\ne }{P}_{5\times 3}=\text{undefined}
$$

Finally, there are $5$ columns in $S$ and $5$ rows in $P.$ Since the number of columns in $S$ equals the number of rows in $P,$ the matrices $S$ and $P$ are conformable for multiplication:

$$
{S}_{1\times \boxed{\text{5}}}{\times }_{✓}{P}_{\boxed{\text{5}}\times 3}=\text{well defined}
$$

Therefore, statement III is true, while statements I and II are false.

### easy / q-22055 / raw-q-22055

$$
X=\begin{bmatrix}1 & 2 \\ 0 & 7\end{bmatrix},\,Y=\begin{bmatrix}1 & 0 & -1 \\ -1 & 0 & 1\end{bmatrix},\,Z=\begin{bmatrix}1 & 0 & -1 \\ -1 & 0 & 1 \\ 1 & 0 & 1\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $X,Y,$ and $Z?$

Select all that apply.

- **I.** The product $XY$ is well defined

- **II.** The product $YX$ is well defined

- **III.** The product $YZ$ is well defined

Field I (:answer-field.type/checkbox)

- false

- true **correct**

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $X$ is a $2\times 2$ matrix, $Y$ is a $2\times 3$ matrix, and $Z$ is a $3\times 3$ matrix.

There are $2$ columns in $X$ and $2$ rows in $Y.$ Since the number of columns in $X$ equals the number of rows in $Y,$ the matrices $X$ and $Y$ are conformable for multiplication:

$$
{X}_{2\times \boxed{\text{2}}}{\times }_{✓}{Y}_{\boxed{\text{2}}\times 3}=\text{well defined}
$$

On the other hand, there are $3$ columns in $Y$ and $2$ rows in $X.$ Since the number of columns in $Y$ does **not** equal the number of rows in $X,$ the matrices $Y$ and $X$ are **not** conformable for multiplication:

$$
{Y}_{2\times 3}{\times }_{\ne }{X}_{2\times 2}=\text{undefined}
$$

Finally, there are $3$ columns in $Y$ and $3$ rows in $Z.$ Since the number of columns in $Y$ equals the number of rows in $Z,$ the matrices $Y$ and $Z$ are conformable for multiplication:

$$
{Y}_{2\times \boxed{\text{3}}}{\times }_{✓}{Z}_{\boxed{\text{3}}\times 3}=\text{well defined}
$$

Therefore, statements I and III are true, while statement II is false.

### easy / q-22056 / raw-q-22056

$$
R=\begin{bmatrix}0 & 0 \\ 0 & 0 \\ 0 & 0 \\ 0 & 0\end{bmatrix},\,S=\begin{bmatrix}1 & 0 & -1 & 0 \\ -1 & 0 & 1 & 8\end{bmatrix},\,T=\begin{bmatrix}1 & 0 \\ 0 & 1 \\ 0 & -1\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $R,S,$ and $T?$

Select all that apply.

- **I.** The product $SR$ is well defined
- **II.** The product $RS$ is well defined
- **III.** The product $ST$ is well defined

Field I (:answer-field.type/checkbox)

- false

- true **correct**

Field II (:answer-field.type/checkbox)

- false

- true **correct**

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $R$ is a $4\times 2$ matrix, $S$ is a $2\times 4$ matrix, and $T$ is a $3\times 2$ matrix.

There are $4$ columns in $S$ and $4$ rows in $R.$ Since the number of columns in $S$ equals the number of rows in $R,$ the matrices $S$ and $R$ are conformable for multiplication:

$$
{S}_{2\times \boxed{\text{4}}}{\times }_{✓}{R}_{\boxed{\text{4}}\times 2}=\text{well defined}
$$

On the other hand, there are $2$ columns in $R$ and $2$ rows in $S.$ Since the number of columns in $R$ equals the number of rows in $S,$ the matrices $R$ and $S$ are conformable for multiplication:

$$
{R}_{4\times \boxed{\text{2}}}{\times }_{✓}{S}_{\boxed{\text{2}}\times 4}=\text{well defined}
$$

Finally, there are $4$ columns in $S$ and $3$ rows in $T.$ Since the number of columns in $S$ does **not** equal the number of rows in $T,$ the matrices $S$ and $T$ are **not** conformable for multiplication:

$$
{S}_{2\times 4}{\times }_{\ne }{T}_{3\times 2}=\text{undefined}
$$

Therefore, statements I and II are true, while statement III is false.

### moderate / q-22062 / raw-q-22062

$$
P=\begin{bmatrix}1 & 2 & 3 & 4 & 5\end{bmatrix},\,R=\begin{bmatrix}1 & 0\end{bmatrix},\,S=\begin{bmatrix}1 & 0 \\ -1 & 0 \\ 1 & 0 \\ -1 & 0 \\ 1 & 0\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $P,R,$ and $S?$

Select all that apply.

- **I.** The product $RS$ is well defined
- **II.** The product $RP$ is well defined
- **III.** The product $PS$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $P$ is a $1\times 5$ row vector, $R$ is a $1\times 2$ row vector, and $S$ is a $5\times 2$ matrix.

There are $2$ columns in $R$ and $5$ rows in $S.$ Since the number of columns in $R$ does **not** equal the number of rows in $S,$ the matrices $R$ and $S$ are **not** conformable for multiplication:

$$
{R}_{1\times 2}{\times }_{\ne }{S}_{5\times 2}=\text{undefined}
$$

On the other hand, there are $2$ columns in $R$ and $1$ row in $P.$ Since the number of columns in $R$ does **not** equal the number of rows in $P,$ the matrices $R$ and $P$ are **not** conformable for multiplication:

$$
{R}_{1\times 2}{\times }_{\ne }{P}_{1\times 5}=\text{undefined}
$$

Finally, there are $5$ columns in $P$ and $5$ rows in $S.$ Since the number of columns in $P$ equals the number of rows in $S,$ the matrices $P$ and $S$ are conformable for multiplication:

$$
{P}_{1\times \boxed{\text{5}}}{\times }_{✓}{S}_{\boxed{\text{5}}\times 2}=\text{well defined}
$$

Therefore, statement III is true, while statements I and II are false.

### easy / q-42375 / raw-q-42375

$$
J=\begin{bmatrix}2 & 0 & 3 & 1 \\ 1 & 2 & -3 & 1 \\ 0 & 0 & 2 & 7\end{bmatrix},\,K=\begin{bmatrix}3 & -5 \\ 8 & 7 \\ 0 & -2\end{bmatrix},\,L=\begin{bmatrix}3 & 0 & 1 & 4 \\ 2 & 1 & -9 & 0\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $J,K,$ and $L?$

Select all that apply.

- **I.** The product $JK$ is well defined
- **II.** The product $KL$ is well defined
- **III.** The product $JL$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false

- true **correct**

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $J$ is a $3\times 4$ matrix, $K$ is a $3\times 2$ matrix, and $L$ is a $2\times 4$ matrix.

There are $4$ columns in $J$ and $3$ rows in $K.$ Since the number of columns in $J$ does **not** equal the number of rows in $K,$ the matrices $J$ and $K$ are **not** conformable for multiplication:

$$
{J}_{3\times 4}{\times }_{\ne }{K}_{3\times 2}=\text{undefined}
$$

On the other hand, there are $2$ columns in $K$ and $2$ rows in $L.$ Since the number of columns in $K$ equals the number of rows in $L$, the matrices $K$ and $L$ are conformable for multiplication:

$$
{K}_{3\times \boxed{\text{2}}}{\times }_{✓}{L}_{\boxed{\text{2}}\times 4}=\text{well defined}
$$

Finally, there are $4$ columns in $J$ and $2$ rows in $L.$ Since the number of columns in $J$ does **not** equal the number of rows in $L$, the matrices $J$ and $L$ are **not** conformable for multiplication:

$$
{J}_{3\times 4}{\times }_{\ne }{L}_{2\times 4}=\text{undefined}
$$

Therefore, statement II is true, while statements I and III are false.

### easy / q-42376 / raw-q-42376

$$
D=\begin{bmatrix}-2 & 3 \\ 1 & 0\end{bmatrix},\,E=\begin{bmatrix}2 & 0 \\ -3 & 5 \\ 2 & 1\end{bmatrix},\,F=\begin{bmatrix}3 & 1 & 4 \\ -2 & 3 & 2\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $D,E,$ and $F?$

Select all that apply.

- **I.** The product $ED$ is well defined
- **II.** The product $FD$ is well defined
- **III.** The product $EF$ is well defined

Field I (:answer-field.type/checkbox)

- false

- true **correct**

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $D$ is a $2\times 2$ matrix, $E$ is a $3\times 2$ matrix, and $F$ is a $2\times 3$ matrix.

There are $2$ columns in $E$ and $2$ rows in $D.$ Since the number of columns in $E$ equals the number of rows in $D,$ the matrices $E$ and $D$ are conformable for multiplication:

$$
{E}_{3\times \boxed{\text{2}}}{\times }_{✓}{D}_{\boxed{\text{2}}\times 2}=\text{well defined}
$$

On the other hand, there are $3$ columns in $F$ and $2$ rows in $D.$ Since the number of columns in $F$ does **not** equal the number of rows in $D,$ the matrices $F$ and $D$ are **not** conformable for multiplication:

$$
{F}_{2\times 3}{\times }_{\ne }{D}_{2\times 2}=\text{undefined}
$$

Finally, there are $2$ columns in $E$ and $2$ rows in $F.$ Since the number of columns in $E$ equals the number of rows in $F,$ the matrices $E$ and $F$ are conformable for multiplication:

$$
{E}_{3\times \boxed{\text{2}}}{\times }_{✓}{F}_{\boxed{\text{2}}\times 3}=\text{well defined}
$$

Therefore, statements I and III are true, while statement II is false.

### easy / q-42377 / raw-q-42377

$$
L=\begin{bmatrix}1 & 4 & 0 \\ 0 & 5 & 0\end{bmatrix},\,M=\begin{bmatrix}5 & 0 & 0 \\ -4 & 5 & 1\end{bmatrix},\,N=\begin{bmatrix}2 & 0 \\ -3 & 5 \\ 2 & 1\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $L,M,$ and $N?$

Select all that apply.

- **I.** The product $ML$ is well defined
- **II.** The product $MN$ is well defined
- **III.** The product $LN$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false

- true **correct**

Field III (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $L$ is a $2\times 3$ matrix, $M$ is a $2\times 3$ matrix, and $N$ is a $3\times 2$ matrix.

There are $3$ columns in $M$ and $2$ rows in $L.$ Since the number of columns in $M$ does **not** equal the number of rows in $L,$ the matrices $M$ and $L$ are **not** conformable for multiplication:

$$
{M}_{2\times 3}{\times }_{\ne }{L}_{2\times 3}=\text{undefined}
$$

On the other hand, there are $3$ columns in $M$ and $3$ rows in $N.$ Since the number of columns in $M$ equals the number of rows in $N,$ the matrices $M$ and $N$ are conformable for multiplication:

$$
{M}_{2\times \boxed{\text{3}}}{\times }_{✓}{N}_{\boxed{\text{3}}\times 2}=\text{well defined}
$$

Finally, there are $3$ columns in $L$ and $3$ rows in $N.$ Since the number of columns in $L$ equals the number of rows in $N,$ the matrices $L$ and $N$ are conformable for multiplication:

$$
{L}_{2\times \boxed{\text{3}}}{\times }_{✓}{N}_{\boxed{\text{3}}\times 2}=\text{well defined}
$$

Therefore, statements II and III are true, while statement I is false.

### moderate / q-42381 / raw-q-42381

$$
O=\begin{bmatrix}1 & 2 \\ -4 & 3 \\ 0 & 4\end{bmatrix},\,P=\begin{bmatrix}5 & 0 & 0 \\ -4 & 5 & 1\end{bmatrix},\,R=\begin{bmatrix}2 & 0 & 5\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $O,P,$ and $R?$

Select all that apply.

- **I.** The product $OP$ is well defined

- **II.** The product $OR$ is well defined

- **III.** The product $PR$ is well defined

Field I (:answer-field.type/checkbox)

- false

- true **correct**

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $O$ is a $3\times 2$ matrix, $P$ is a $2\times 3$ matrix, and $R$ is a $1\times 3$ row vector.

There are $2$ columns in $O$ and $2$ rows in $P.$ Since the number of columns in $O$ equals the number of rows in $P,$ the matrices $O$ and $P$ are conformable for multiplication:

$$
{O}_{3\times \boxed{\text{2}}}{\times }_{✓}{P}_{\boxed{\text{2}}\times 3}=\text{well defined}
$$

On the other hand, there are $2$ columns in $O$ and $1$ rows in $R.$ Since the number of columns in $O$ does **not** equal the number of rows in $R,$ the matrices $O$ and $R$ are **not** conformable for multiplication:

$$
{O}_{3\times 2}{\times }_{\ne }{R}_{1\times 3}=\text{undefined}
$$

Finally, there are $3$ columns in $P$ and $1$ rows in $R.$ Since the number of columns in $P$ does **not** equal the number of rows in $R,$ the matrices $P$ and $R$ are **not** conformable for multiplication:

$$
{P}_{2\times 3}{\times }_{\ne }{R}_{1\times 3}=\text{undefined}
$$

Therefore, statement I is true, while statements II and III are false.

# Generated variants (authored parameter and target slots)

### easy / q-22063 / boolean-pairs

$$
A=\begin{bmatrix}-5 & -5 & -8 \\ -8 & -5 & -2\end{bmatrix},\,B=\begin{bmatrix}8 & 5 & 7 \\ 4 & -3 & 9\end{bmatrix},\,C=\begin{bmatrix}-7 \\ -6\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $A,B,$ and $C?$

Select all that apply.

- **I.** The product $AC$ is well defined
- **II.** The product $AB$ is well defined
- **III.** The product $CB$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $A$ is a $2\times 3$ matrix, $B$ is a $2\times 3$ matrix, and $C$ is a $2\times 1$ column vector

There are $3$ columns in $A$ and $2$ rows in $C.$ Since the number of columns in $A$ does **not** equal the number of rows in $C,$ the matrices $A$ and $C$ are **not** conformable for multiplication:

$$
{A}_{2\times 3}{\times }_{\ne }{C}_{2\times 1}=\text{undefined}
$$

On the other hand, there are $3$ columns in $A$ and $2$ rows in $B.$ Since the number of columns in $A$ does **not** equal the number of rows in $B,$ the matrices $A$ and $B$ are **not** conformable for multiplication:

$$
{A}_{2\times 3}{\times }_{\ne }{B}_{2\times 3}=\text{undefined}
$$

Finally, there is $1$ column in $C$ and $2$ rows in $B.$ Since the number of columns in $C$ does **not** equal the number of rows in $B,$ the matrices $C$ and $B$ are **not** conformable for multiplication:

$$
{C}_{2\times 1}{\times }_{\ne }{B}_{2\times 3}=\text{undefined}
$$

We conclude that all three statements are false.

### easy / q-22063 / boolean-pairs

$$
A=\begin{bmatrix}6 & 3 \\ 7 & 7 \\ -3 & 5\end{bmatrix},\,B=\begin{bmatrix}-6 & -9 & -1 \\ 4 & -9 & 4 \\ 2 & 8 & 4 \\ 6 & 8 & 4\end{bmatrix},\,C=\begin{bmatrix}-4 \\ -8 \\ -1\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $A,B,$ and $C?$

Select all that apply.

- **I.** The product $BA$ is well defined
- **II.** The product $CA$ is well defined
- **III.** The product $AB$ is well defined

Field I (:answer-field.type/checkbox)

- false

- true **correct**

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $A$ is a $3\times 2$ matrix, $B$ is a $4\times 3$ matrix, and $C$ is a $3\times 1$ column vector

There are $3$ columns in $B$ and $3$ rows in $A.$ Since the number of columns in $B$ equals the number of rows in $A,$ the matrices $B$ and $A$ are conformable for multiplication:

$$
{B}_{4\times \boxed{\text{3}}}{\times }_{✓}{A}_{\boxed{\text{3}}\times 2}=\text{well defined}
$$

On the other hand, there is $1$ column in $C$ and $3$ rows in $A.$ Since the number of columns in $C$ does **not** equal the number of rows in $A,$ the matrices $C$ and $A$ are **not** conformable for multiplication:

$$
{C}_{3\times 1}{\times }_{\ne }{A}_{3\times 2}=\text{undefined}
$$

Finally, there are $2$ columns in $A$ and $4$ rows in $B.$ Since the number of columns in $A$ does **not** equal the number of rows in $B,$ the matrices $A$ and $B$ are **not** conformable for multiplication:

$$
{A}_{3\times 2}{\times }_{\ne }{B}_{4\times 3}=\text{undefined}
$$

Therefore, statement I is true, while statements II and III are false.

### easy / q-42374 / boolean-pairs

$$
A=\begin{bmatrix}8 & -2 & -5 \\ -5 & -8 & -8\end{bmatrix},\,B=\begin{bmatrix}-5 & -2 & 8 \\ 5 & 7 & 4\end{bmatrix},\,C=\begin{bmatrix}-3 & 9 & -7 & -6 \\ -9 & 3 & 1 & -3\end{bmatrix},
$$

Which of the following statements are true regarding the matrices $A,B,$ and $C?$

- **I.** The product $AB$ is well defined
- **II.** The product $AC$ is well defined
- **III.** The product $CB$ is well defined

Select all that apply.

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $A$ is a $2\times 3$ matrix, $B$ is a $2\times 3$ matrix, and $C$ is a $2\times 4$ matrix.

There are $3$ columns in $A$ and $2$ rows in $B.$ Since the number of columns in $A$ does **not** equal the number of rows in $B,$ the matrices $A$ and $B$ are **not** conformable for multiplication:

$$
{A}_{2\times 3}{\times }_{\ne }{B}_{2\times 3}=\text{undefined}
$$

On the other hand, there are $3$ columns in $A$ and $2$ rows in $C.$ Since the number of columns in $A$ does **not** equal the number of rows in $C,$ the matrices $A$ and $C$ are **not** conformable for multiplication:

$$
{A}_{2\times 3}{\times }_{\ne }{C}_{2\times 4}=\text{undefined}
$$

Finally, there are $4$ columns in $C$ and $2$ rows in $B.$ Since the number of columns in $C$ does **not** equal the number of rows in $B,$ the matrices $C$ and $B$ are **not** conformable for multiplication:

$$
{C}_{2\times 4}{\times }_{\ne }{B}_{2\times 3}=\text{undefined}
$$

We conclude that all three statements are false.

### easy / q-42374 / boolean-pairs

$$
A=\begin{bmatrix}6 & 3 \\ 7 & 7 \\ -3 & 5\end{bmatrix},\,B=\begin{bmatrix}-6 & -9 & -1 \\ 4 & -9 & 4 \\ 2 & 8 & 4 \\ 6 & 8 & 4\end{bmatrix},\,C=\begin{bmatrix}-4 & -8 \\ -1 & 9 \\ -3 & -7 \\ 5 & 2\end{bmatrix},
$$

Which of the following statements are true regarding the matrices $A,B,$ and $C?$

- **I.** The product $BC$ is well defined
- **II.** The product $BA$ is well defined
- **III.** The product $AB$ is well defined

Select all that apply.

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false

- true **correct**

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $A$ is a $3\times 2$ matrix, $B$ is a $4\times 3$ matrix, and $C$ is a $4\times 2$ matrix.

There are $3$ columns in $B$ and $4$ rows in $C.$ Since the number of columns in $B$ does **not** equal the number of rows in $C,$ the matrices $B$ and $C$ are **not** conformable for multiplication:

$$
{B}_{4\times 3}{\times }_{\ne }{C}_{4\times 2}=\text{undefined}
$$

On the other hand, there are $3$ columns in $B$ and $3$ rows in $A.$ Since the number of columns in $B$ equals the number of rows in $A,$ the matrices $B$ and $A$ are conformable for multiplication:

$$
{B}_{4\times \boxed{\text{3}}}{\times }_{✓}{A}_{\boxed{\text{3}}\times 2}=\text{well defined}
$$

Finally, there are $2$ columns in $A$ and $4$ rows in $B.$ Since the number of columns in $A$ does **not** equal the number of rows in $B,$ the matrices $A$ and $B$ are **not** conformable for multiplication:

$$
{A}_{3\times 2}{\times }_{\ne }{B}_{4\times 3}=\text{undefined}
$$

Therefore, statement II is true, while statements I and III are false.

### moderate / q-129437 / boolean-pairs

$$
P=\begin{bmatrix}-5 & -6 \\ 8 & -2\end{bmatrix},\,R=\begin{bmatrix}-5 & -5 & -8 & -8 & -5\end{bmatrix},\,S=\begin{bmatrix}-2 & 8\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $P,R,$ and $S?$

Select all that apply.

- **I.** The product $RS$ is well defined
- **II.** The product $PS$ is well defined
- **III.** The product $PR$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $P$ is a $2\times 2$ matrix, $R$ is a $1\times 5$ row vector, and $S$ is a $1\times 2$ row vector. 

There are $5$ columns in $R$ and $1$ row in $S.$ Since the number of columns in $R$ does **not** equal the number of rows in $S,$ the matrices $R$ and $S$ are **not** conformable for multiplication:

$$
{R}_{1\times 5}{\times }_{\ne }{S}_{1\times 2}=\text{undefined}
$$

On the other hand, there are $2$ columns in $P$ and $1$ row in $S.$ Since the number of columns in $P$ does **not** equal the number of rows in $S,$ the matrices $P$ and $S$ are **not** conformable for multiplication:

$$
{P}_{2\times 2}{\times }_{\ne }{S}_{1\times 2}=\text{undefined}
$$

Finally, there are $2$ columns in $P$ and $1$ row in $R.$ Since the number of columns in $P$ does **not** equal the number of rows in $R,$ the matrices $P$ and $R$ are **not** conformable for multiplication:

$$
{P}_{2\times 2}{\times }_{\ne }{R}_{1\times 5}=\text{undefined}
$$

We conclude that all three statements are false.

### moderate / q-129437 / boolean-pairs

$$
P=\begin{bmatrix}0 & 9 \\ -7 & 6 \\ 3 & 7\end{bmatrix},\,R=\begin{bmatrix}7 & -3\end{bmatrix},\,S=\begin{bmatrix}5 & -6 & -9 & -1 & 4\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $P,R,$ and $S?$

Select all that apply.

- **I.** The product $SP$ is well defined
- **II.** The product $PS$ is well defined
- **III.** The product $RS$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $P$ is a $3\times 2$ matrix, $R$ is a $1\times 2$ row vector, and $S$ is a $1\times 5$ row vector. 

There are $5$ columns in $S$ and $3$ rows in $P.$ Since the number of columns in $S$ does **not** equal the number of rows in $P,$ the matrices $S$ and $P$ are **not** conformable for multiplication:

$$
{S}_{1\times 5}{\times }_{\ne }{P}_{3\times 2}=\text{undefined}
$$

On the other hand, there are $2$ columns in $P$ and $1$ row in $S.$ Since the number of columns in $P$ does **not** equal the number of rows in $S,$ the matrices $P$ and $S$ are **not** conformable for multiplication:

$$
{P}_{3\times 2}{\times }_{\ne }{S}_{1\times 5}=\text{undefined}
$$

Finally, there are $2$ columns in $R$ and $1$ row in $S.$ Since the number of columns in $R$ does **not** equal the number of rows in $S,$ the matrices $R$ and $S$ are **not** conformable for multiplication:

$$
{R}_{1\times 2}{\times }_{\ne }{S}_{1\times 5}=\text{undefined}
$$

We conclude that all three statements are false.

### easy / q-22055 / boolean-pairs

$$
X=\begin{bmatrix}8 & -2 & -5 \\ -5 & -8 & -8\end{bmatrix},\,Y=\begin{bmatrix}-5 & -2 & 8 \\ 5 & 7 & 4\end{bmatrix},\,Z=\begin{bmatrix}-3 & 9 & -7 & -6 \\ -9 & 3 & 1 & -3\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $X,Y,$ and $Z?$

Select all that apply.

- **I.** The product $XY$ is well defined

- **II.** The product $XZ$ is well defined

- **III.** The product $ZY$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $X$ is a $2\times 3$ matrix, $Y$ is a $2\times 3$ matrix, and $Z$ is a $2\times 4$ matrix.

There are $3$ columns in $X$ and $2$ rows in $Y.$ Since the number of columns in $X$ does **not** equal the number of rows in $Y,$ the matrices $X$ and $Y$ are **not** conformable for multiplication:

$$
{X}_{2\times 3}{\times }_{\ne }{Y}_{2\times 3}=\text{undefined}
$$

On the other hand, there are $3$ columns in $X$ and $2$ rows in $Z.$ Since the number of columns in $X$ does **not** equal the number of rows in $Z,$ the matrices $X$ and $Z$ are **not** conformable for multiplication:

$$
{X}_{2\times 3}{\times }_{\ne }{Z}_{2\times 4}=\text{undefined}
$$

Finally, there are $4$ columns in $Z$ and $2$ rows in $Y.$ Since the number of columns in $Z$ does **not** equal the number of rows in $Y,$ the matrices $Z$ and $Y$ are **not** conformable for multiplication:

$$
{Z}_{2\times 4}{\times }_{\ne }{Y}_{2\times 3}=\text{undefined}
$$

We conclude that all three statements are false.

### easy / q-22055 / boolean-pairs

$$
X=\begin{bmatrix}6 & 3 \\ 7 & 7 \\ -3 & 5\end{bmatrix},\,Y=\begin{bmatrix}-6 & -9 & -1 \\ 4 & -9 & 4 \\ 2 & 8 & 4 \\ 6 & 8 & 4\end{bmatrix},\,Z=\begin{bmatrix}-4 & -8 \\ -1 & 9 \\ -3 & -7 \\ 5 & 2\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $X,Y,$ and $Z?$

Select all that apply.

- **I.** The product $YZ$ is well defined

- **II.** The product $YX$ is well defined

- **III.** The product $XY$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false

- true **correct**

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $X$ is a $3\times 2$ matrix, $Y$ is a $4\times 3$ matrix, and $Z$ is a $4\times 2$ matrix.

There are $3$ columns in $Y$ and $4$ rows in $Z.$ Since the number of columns in $Y$ does **not** equal the number of rows in $Z,$ the matrices $Y$ and $Z$ are **not** conformable for multiplication:

$$
{Y}_{4\times 3}{\times }_{\ne }{Z}_{4\times 2}=\text{undefined}
$$

On the other hand, there are $3$ columns in $Y$ and $3$ rows in $X.$ Since the number of columns in $Y$ equals the number of rows in $X,$ the matrices $Y$ and $X$ are conformable for multiplication:

$$
{Y}_{4\times \boxed{\text{3}}}{\times }_{✓}{X}_{\boxed{\text{3}}\times 2}=\text{well defined}
$$

Finally, there are $2$ columns in $X$ and $4$ rows in $Y.$ Since the number of columns in $X$ does **not** equal the number of rows in $Y,$ the matrices $X$ and $Y$ are **not** conformable for multiplication:

$$
{X}_{3\times 2}{\times }_{\ne }{Y}_{4\times 3}=\text{undefined}
$$

Therefore, statement II is true, while statements I and III are false.

### easy / q-22056 / boolean-pairs

$$
R=\begin{bmatrix}8 & -2 & -5 \\ -5 & -8 & -8\end{bmatrix},\,S=\begin{bmatrix}-5 & -2 & 8 \\ 5 & 7 & 4\end{bmatrix},\,T=\begin{bmatrix}-3 & 9 & -7 & -6 \\ -9 & 3 & 1 & -3\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $R,S,$ and $T?$

Select all that apply.

- **I.** The product $RS$ is well defined
- **II.** The product $RT$ is well defined
- **III.** The product $TS$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $R$ is a $2\times 3$ matrix, $S$ is a $2\times 3$ matrix, and $T$ is a $2\times 4$ matrix.

There are $3$ columns in $R$ and $2$ rows in $S.$ Since the number of columns in $R$ does **not** equal the number of rows in $S,$ the matrices $R$ and $S$ are **not** conformable for multiplication:

$$
{R}_{2\times 3}{\times }_{\ne }{S}_{2\times 3}=\text{undefined}
$$

On the other hand, there are $3$ columns in $R$ and $2$ rows in $T.$ Since the number of columns in $R$ does **not** equal the number of rows in $T,$ the matrices $R$ and $T$ are **not** conformable for multiplication:

$$
{R}_{2\times 3}{\times }_{\ne }{T}_{2\times 4}=\text{undefined}
$$

Finally, there are $4$ columns in $T$ and $2$ rows in $S.$ Since the number of columns in $T$ does **not** equal the number of rows in $S,$ the matrices $T$ and $S$ are **not** conformable for multiplication:

$$
{T}_{2\times 4}{\times }_{\ne }{S}_{2\times 3}=\text{undefined}
$$

We conclude that all three statements are false.

### easy / q-22056 / boolean-pairs

$$
R=\begin{bmatrix}6 & 3 \\ 7 & 7 \\ -3 & 5\end{bmatrix},\,S=\begin{bmatrix}-6 & -9 & -1 \\ 4 & -9 & 4 \\ 2 & 8 & 4 \\ 6 & 8 & 4\end{bmatrix},\,T=\begin{bmatrix}-4 & -8 \\ -1 & 9 \\ -3 & -7 \\ 5 & 2\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $R,S,$ and $T?$

Select all that apply.

- **I.** The product $ST$ is well defined
- **II.** The product $SR$ is well defined
- **III.** The product $RS$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false

- true **correct**

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $R$ is a $3\times 2$ matrix, $S$ is a $4\times 3$ matrix, and $T$ is a $4\times 2$ matrix.

There are $3$ columns in $S$ and $4$ rows in $T.$ Since the number of columns in $S$ does **not** equal the number of rows in $T,$ the matrices $S$ and $T$ are **not** conformable for multiplication:

$$
{S}_{4\times 3}{\times }_{\ne }{T}_{4\times 2}=\text{undefined}
$$

On the other hand, there are $3$ columns in $S$ and $3$ rows in $R.$ Since the number of columns in $S$ equals the number of rows in $R,$ the matrices $S$ and $R$ are conformable for multiplication:

$$
{S}_{4\times \boxed{\text{3}}}{\times }_{✓}{R}_{\boxed{\text{3}}\times 2}=\text{well defined}
$$

Finally, there are $2$ columns in $R$ and $4$ rows in $S.$ Since the number of columns in $R$ does **not** equal the number of rows in $S,$ the matrices $R$ and $S$ are **not** conformable for multiplication:

$$
{R}_{3\times 2}{\times }_{\ne }{S}_{4\times 3}=\text{undefined}
$$

Therefore, statement II is true, while statements I and III are false.

### moderate / q-22062 / boolean-pairs

$$
P=\begin{bmatrix}-5 & -6\end{bmatrix},\,R=\begin{bmatrix}8 & -2 & -5 & -5 & -8\end{bmatrix},\,S=\begin{bmatrix}-8 & -5 & -2 \\ 8 & 5 & 7\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $P,R,$ and $S?$

Select all that apply.

- **I.** The product $RS$ is well defined
- **II.** The product $PS$ is well defined
- **III.** The product $PR$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false

- true **correct**

Field III (:answer-field.type/checkbox)

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

Therefore, statement II is true, while statements I and III are false.

### moderate / q-22062 / boolean-pairs

$$
P=\begin{bmatrix}5 & 0 & 9 & -7\end{bmatrix},\,R=\begin{bmatrix}6 & 3\end{bmatrix},\,S=\begin{bmatrix}7 & 7 \\ -3 & 5 \\ -6 & -9 \\ -1 & 4\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $P,R,$ and $S?$

Select all that apply.

- **I.** The product $RS$ is well defined
- **II.** The product $SP$ is well defined
- **III.** The product $PS$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $P$ is a $1\times 4$ row vector, $R$ is a $1\times 2$ row vector, and $S$ is a $4\times 2$ matrix.

There are $2$ columns in $R$ and $4$ rows in $S.$ Since the number of columns in $R$ does **not** equal the number of rows in $S,$ the matrices $R$ and $S$ are **not** conformable for multiplication:

$$
{R}_{1\times 2}{\times }_{\ne }{S}_{4\times 2}=\text{undefined}
$$

On the other hand, there are $2$ columns in $S$ and $1$ row in $P.$ Since the number of columns in $S$ does **not** equal the number of rows in $P,$ the matrices $S$ and $P$ are **not** conformable for multiplication:

$$
{S}_{4\times 2}{\times }_{\ne }{P}_{1\times 4}=\text{undefined}
$$

Finally, there are $4$ columns in $P$ and $4$ rows in $S.$ Since the number of columns in $P$ equals the number of rows in $S,$ the matrices $P$ and $S$ are conformable for multiplication:

$$
{P}_{1\times \boxed{\text{4}}}{\times }_{✓}{S}_{\boxed{\text{4}}\times 2}=\text{well defined}
$$

Therefore, statement III is true, while statements I and II are false.

### easy / q-42375 / boolean-pairs

$$
J=\begin{bmatrix}8 & -2 & -5 \\ -5 & -8 & -8\end{bmatrix},\,K=\begin{bmatrix}-5 & -2 & 8 \\ 5 & 7 & 4\end{bmatrix},\,L=\begin{bmatrix}-3 & 9 & -7 & -6 \\ -9 & 3 & 1 & -3\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $J,K,$ and $L?$

Select all that apply.

- **I.** The product $JK$ is well defined
- **II.** The product $JL$ is well defined
- **III.** The product $LK$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $J$ is a $2\times 3$ matrix, $K$ is a $2\times 3$ matrix, and $L$ is a $2\times 4$ matrix.

There are $3$ columns in $J$ and $2$ rows in $K.$ Since the number of columns in $J$ does **not** equal the number of rows in $K,$ the matrices $J$ and $K$ are **not** conformable for multiplication:

$$
{J}_{2\times 3}{\times }_{\ne }{K}_{2\times 3}=\text{undefined}
$$

On the other hand, there are $3$ columns in $J$ and $2$ rows in $L.$ Since the number of columns in $J$ does **not** equal the number of rows in $L$, the matrices $J$ and $L$ are **not** conformable for multiplication:

$$
{J}_{2\times 3}{\times }_{\ne }{L}_{2\times 4}=\text{undefined}
$$

Finally, there are $4$ columns in $L$ and $2$ rows in $K.$ Since the number of columns in $L$ does **not** equal the number of rows in $K$, the matrices $L$ and $K$ are **not** conformable for multiplication:

$$
{L}_{2\times 4}{\times }_{\ne }{K}_{2\times 3}=\text{undefined}
$$

We conclude that all three statements are false.

### easy / q-42375 / boolean-pairs

$$
J=\begin{bmatrix}6 & 3 \\ 7 & 7 \\ -3 & 5\end{bmatrix},\,K=\begin{bmatrix}-6 & -9 & -1 \\ 4 & -9 & 4 \\ 2 & 8 & 4 \\ 6 & 8 & 4\end{bmatrix},\,L=\begin{bmatrix}-4 & -8 \\ -1 & 9 \\ -3 & -7 \\ 5 & 2\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $J,K,$ and $L?$

Select all that apply.

- **I.** The product $KL$ is well defined
- **II.** The product $KJ$ is well defined
- **III.** The product $JK$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false

- true **correct**

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $J$ is a $3\times 2$ matrix, $K$ is a $4\times 3$ matrix, and $L$ is a $4\times 2$ matrix.

There are $3$ columns in $K$ and $4$ rows in $L.$ Since the number of columns in $K$ does **not** equal the number of rows in $L,$ the matrices $K$ and $L$ are **not** conformable for multiplication:

$$
{K}_{4\times 3}{\times }_{\ne }{L}_{4\times 2}=\text{undefined}
$$

On the other hand, there are $3$ columns in $K$ and $3$ rows in $J.$ Since the number of columns in $K$ equals the number of rows in $J$, the matrices $K$ and $J$ are conformable for multiplication:

$$
{K}_{4\times \boxed{\text{3}}}{\times }_{✓}{J}_{\boxed{\text{3}}\times 2}=\text{well defined}
$$

Finally, there are $2$ columns in $J$ and $4$ rows in $K.$ Since the number of columns in $J$ does **not** equal the number of rows in $K$, the matrices $J$ and $K$ are **not** conformable for multiplication:

$$
{J}_{3\times 2}{\times }_{\ne }{K}_{4\times 3}=\text{undefined}
$$

Therefore, statement II is true, while statements I and III are false.

### easy / q-42376 / boolean-pairs

$$
D=\begin{bmatrix}8 & -2 & -5 \\ -5 & -8 & -8\end{bmatrix},\,E=\begin{bmatrix}-5 & -2 & 8 \\ 5 & 7 & 4\end{bmatrix},\,F=\begin{bmatrix}-3 & 9 & -7 & -6 \\ -9 & 3 & 1 & -3\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $D,E,$ and $F?$

Select all that apply.

- **I.** The product $DE$ is well defined
- **II.** The product $DF$ is well defined
- **III.** The product $FE$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $D$ is a $2\times 3$ matrix, $E$ is a $2\times 3$ matrix, and $F$ is a $2\times 4$ matrix.

There are $3$ columns in $D$ and $2$ rows in $E.$ Since the number of columns in $D$ does **not** equal the number of rows in $E,$ the matrices $D$ and $E$ are **not** conformable for multiplication:

$$
{D}_{2\times 3}{\times }_{\ne }{E}_{2\times 3}=\text{undefined}
$$

On the other hand, there are $3$ columns in $D$ and $2$ rows in $F.$ Since the number of columns in $D$ does **not** equal the number of rows in $F,$ the matrices $D$ and $F$ are **not** conformable for multiplication:

$$
{D}_{2\times 3}{\times }_{\ne }{F}_{2\times 4}=\text{undefined}
$$

Finally, there are $4$ columns in $F$ and $2$ rows in $E.$ Since the number of columns in $F$ does **not** equal the number of rows in $E,$ the matrices $F$ and $E$ are **not** conformable for multiplication:

$$
{F}_{2\times 4}{\times }_{\ne }{E}_{2\times 3}=\text{undefined}
$$

We conclude that all three statements are false.

### easy / q-42376 / boolean-pairs

$$
D=\begin{bmatrix}6 & 3 \\ 7 & 7 \\ -3 & 5\end{bmatrix},\,E=\begin{bmatrix}-6 & -9 & -1 \\ 4 & -9 & 4 \\ 2 & 8 & 4 \\ 6 & 8 & 4\end{bmatrix},\,F=\begin{bmatrix}-4 & -8 \\ -1 & 9 \\ -3 & -7 \\ 5 & 2\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $D,E,$ and $F?$

Select all that apply.

- **I.** The product $EF$ is well defined
- **II.** The product $ED$ is well defined
- **III.** The product $DE$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false

- true **correct**

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $D$ is a $3\times 2$ matrix, $E$ is a $4\times 3$ matrix, and $F$ is a $4\times 2$ matrix.

There are $3$ columns in $E$ and $4$ rows in $F.$ Since the number of columns in $E$ does **not** equal the number of rows in $F,$ the matrices $E$ and $F$ are **not** conformable for multiplication:

$$
{E}_{4\times 3}{\times }_{\ne }{F}_{4\times 2}=\text{undefined}
$$

On the other hand, there are $3$ columns in $E$ and $3$ rows in $D.$ Since the number of columns in $E$ equals the number of rows in $D,$ the matrices $E$ and $D$ are conformable for multiplication:

$$
{E}_{4\times \boxed{\text{3}}}{\times }_{✓}{D}_{\boxed{\text{3}}\times 2}=\text{well defined}
$$

Finally, there are $2$ columns in $D$ and $4$ rows in $E.$ Since the number of columns in $D$ does **not** equal the number of rows in $E,$ the matrices $D$ and $E$ are **not** conformable for multiplication:

$$
{D}_{3\times 2}{\times }_{\ne }{E}_{4\times 3}=\text{undefined}
$$

Therefore, statement II is true, while statements I and III are false.

### easy / q-42377 / boolean-pairs

$$
L=\begin{bmatrix}8 & -2 & -5 \\ -5 & -8 & -8\end{bmatrix},\,M=\begin{bmatrix}-5 & -2 & 8 \\ 5 & 7 & 4\end{bmatrix},\,N=\begin{bmatrix}-3 & 9 & -7 & -6 \\ -9 & 3 & 1 & -3\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $L,M,$ and $N?$

Select all that apply.

- **I.** The product $LM$ is well defined
- **II.** The product $LN$ is well defined
- **III.** The product $NM$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $L$ is a $2\times 3$ matrix, $M$ is a $2\times 3$ matrix, and $N$ is a $2\times 4$ matrix.

There are $3$ columns in $L$ and $2$ rows in $M.$ Since the number of columns in $L$ does **not** equal the number of rows in $M,$ the matrices $L$ and $M$ are **not** conformable for multiplication:

$$
{L}_{2\times 3}{\times }_{\ne }{M}_{2\times 3}=\text{undefined}
$$

On the other hand, there are $3$ columns in $L$ and $2$ rows in $N.$ Since the number of columns in $L$ does **not** equal the number of rows in $N,$ the matrices $L$ and $N$ are **not** conformable for multiplication:

$$
{L}_{2\times 3}{\times }_{\ne }{N}_{2\times 4}=\text{undefined}
$$

Finally, there are $4$ columns in $N$ and $2$ rows in $M.$ Since the number of columns in $N$ does **not** equal the number of rows in $M,$ the matrices $N$ and $M$ are **not** conformable for multiplication:

$$
{N}_{2\times 4}{\times }_{\ne }{M}_{2\times 3}=\text{undefined}
$$

We conclude that all three statements are false.

### easy / q-42377 / boolean-pairs

$$
L=\begin{bmatrix}6 & 3 \\ 7 & 7 \\ -3 & 5\end{bmatrix},\,M=\begin{bmatrix}-6 & -9 & -1 \\ 4 & -9 & 4 \\ 2 & 8 & 4 \\ 6 & 8 & 4\end{bmatrix},\,N=\begin{bmatrix}-4 & -8 \\ -1 & 9 \\ -3 & -7 \\ 5 & 2\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $L,M,$ and $N?$

Select all that apply.

- **I.** The product $MN$ is well defined
- **II.** The product $ML$ is well defined
- **III.** The product $LM$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false

- true **correct**

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $L$ is a $3\times 2$ matrix, $M$ is a $4\times 3$ matrix, and $N$ is a $4\times 2$ matrix.

There are $3$ columns in $M$ and $4$ rows in $N.$ Since the number of columns in $M$ does **not** equal the number of rows in $N,$ the matrices $M$ and $N$ are **not** conformable for multiplication:

$$
{M}_{4\times 3}{\times }_{\ne }{N}_{4\times 2}=\text{undefined}
$$

On the other hand, there are $3$ columns in $M$ and $3$ rows in $L.$ Since the number of columns in $M$ equals the number of rows in $L,$ the matrices $M$ and $L$ are conformable for multiplication:

$$
{M}_{4\times \boxed{\text{3}}}{\times }_{✓}{L}_{\boxed{\text{3}}\times 2}=\text{well defined}
$$

Finally, there are $2$ columns in $L$ and $4$ rows in $M.$ Since the number of columns in $L$ does **not** equal the number of rows in $M,$ the matrices $L$ and $M$ are **not** conformable for multiplication:

$$
{L}_{3\times 2}{\times }_{\ne }{M}_{4\times 3}=\text{undefined}
$$

Therefore, statement II is true, while statements I and III are false.

### moderate / q-42381 / boolean-pairs

$$
O=\begin{bmatrix}-5 & -6 \\ 8 & -2\end{bmatrix},\,P=\begin{bmatrix}-5 & -5 & -8 & -8 & -5 \\ -2 & 8 & 5 & 7 & 4 \\ -3 & 9 & -7 & -6 & -9\end{bmatrix},\,R=\begin{bmatrix}3 & 1\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $O,P,$ and $R?$

Select all that apply.

- **I.** The product $PR$ is well defined

- **II.** The product $OR$ is well defined

- **III.** The product $OP$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $O$ is a $2\times 2$ matrix, $P$ is a $3\times 5$ matrix, and $R$ is a $1\times 2$ row vector.

There are $5$ columns in $P$ and $1$ row in $R.$ Since the number of columns in $P$ does **not** equal the number of rows in $R,$ the matrices $P$ and $R$ are **not** conformable for multiplication:

$$
{P}_{3\times 5}{\times }_{\ne }{R}_{1\times 2}=\text{undefined}
$$

On the other hand, there are $2$ columns in $O$ and $1$ row in $R.$ Since the number of columns in $O$ does **not** equal the number of rows in $R,$ the matrices $O$ and $R$ are **not** conformable for multiplication:

$$
{O}_{2\times 2}{\times }_{\ne }{R}_{1\times 2}=\text{undefined}
$$

Finally, there are $2$ columns in $O$ and $3$ rows in $P.$ Since the number of columns in $O$ does **not** equal the number of rows in $P,$ the matrices $O$ and $P$ are **not** conformable for multiplication:

$$
{O}_{2\times 2}{\times }_{\ne }{P}_{3\times 5}=\text{undefined}
$$

We conclude that all three statements are false.

### moderate / q-42381 / boolean-pairs

$$
O=\begin{bmatrix}0 & 9 \\ -7 & 6 \\ 3 & 7\end{bmatrix},\,P=\begin{bmatrix}7 & -3 & 5 \\ -6 & -9 & -1\end{bmatrix},\,R=\begin{bmatrix}4 & -9 & 4 & 2 & 8\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $O,P,$ and $R?$

Select all that apply.

- **I.** The product $RO$ is well defined

- **II.** The product $OR$ is well defined

- **III.** The product $PR$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false **correct**

- true

Worked solution

Notice that $O$ is a $3\times 2$ matrix, $P$ is a $2\times 3$ matrix, and $R$ is a $1\times 5$ row vector.

There are $5$ columns in $R$ and $3$ rows in $O.$ Since the number of columns in $R$ does **not** equal the number of rows in $O,$ the matrices $R$ and $O$ are **not** conformable for multiplication:

$$
{R}_{1\times 5}{\times }_{\ne }{O}_{3\times 2}=\text{undefined}
$$

On the other hand, there are $2$ columns in $O$ and $1$ row in $R.$ Since the number of columns in $O$ does **not** equal the number of rows in $R,$ the matrices $O$ and $R$ are **not** conformable for multiplication:

$$
{O}_{3\times 2}{\times }_{\ne }{R}_{1\times 5}=\text{undefined}
$$

Finally, there are $3$ columns in $P$ and $1$ row in $R.$ Since the number of columns in $P$ does **not** equal the number of rows in $R,$ the matrices $P$ and $R$ are **not** conformable for multiplication:

$$
{P}_{2\times 3}{\times }_{\ne }{R}_{1\times 5}=\text{undefined}
$$

We conclude that all three statements are false.

### hard / mixed-orientations / boolean-pairs

$$
O=\begin{bmatrix}-5 & -5 & -8 & -8 \\ -5 & -2 & 8 & 5\end{bmatrix},\,P=\begin{bmatrix}7 & 4\end{bmatrix},\,R=\begin{bmatrix}-3 \\ 9 \\ -7\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $O,P,$ and $R?$

Select all that apply.

- **I.** The product $RP$ is well defined

- **II.** The product $PR$ is well defined

- **III.** The product $OP$ is well defined

Field I (:answer-field.type/checkbox)

- false

- true **correct**

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

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

Therefore, statement I is true, while statements II and III are false.

### hard / mixed-orientations / boolean-pairs

$$
O=\begin{bmatrix}5 & -6 & -9 & -1 & 4 \\ -9 & 4 & 2 & 8 & 4 \\ 6 & 8 & 4 & -4 & -8 \\ -1 & 9 & -3 & -7 & 5\end{bmatrix},\,P=\begin{bmatrix}2 & 0 & -5 & -2\end{bmatrix},\,R=\begin{bmatrix}-9 \\ -3\end{bmatrix}
$$

Which of the following statements are true regarding the matrices $O,P,$ and $R?$

Select all that apply.

- **I.** The product $RO$ is well defined

- **II.** The product $PR$ is well defined

- **III.** The product $RP$ is well defined

Field I (:answer-field.type/checkbox)

- false **correct**

- true

Field II (:answer-field.type/checkbox)

- false **correct**

- true

Field III (:answer-field.type/checkbox)

- false

- true **correct**

Worked solution

Notice that $O$ is a $4\times 5$ matrix, $P$ is a $1\times 4$ row vector, and $R$ is a $2\times 1$ column vector.

There is $1$ column in $R$ and $4$ rows in $O.$ Since the number of columns in $R$ does **not** equal the number of rows in $O,$ the matrices $R$ and $O$ are **not** conformable for multiplication:

$$
{R}_{2\times 1}{\times }_{\ne }{O}_{4\times 5}=\text{undefined}
$$

On the other hand, there are $4$ columns in $P$ and $2$ rows in $R.$ Since the number of columns in $P$ does **not** equal the number of rows in $R,$ the matrices $P$ and $R$ are **not** conformable for multiplication:

$$
{P}_{1\times 4}{\times }_{\ne }{R}_{2\times 1}=\text{undefined}
$$

Finally, there is $1$ column in $R$ and $1$ row in $P.$ Since the number of columns in $R$ equals the number of rows in $P,$ the matrices $R$ and $P$ are conformable for multiplication:

$$
{R}_{2\times \boxed{\text{1}}}{\times }_{✓}{P}_{\boxed{\text{1}}\times 4}=\text{well defined}
$$

Therefore, statement III is true, while statements I and II are false.