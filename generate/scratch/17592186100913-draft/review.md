# Source evidence and generated variants

Original replay (evidence-only)

### easy / outer-3x2 / q-1031

What is $\begin{bmatrix}3 \\ 0 \\ 1\end{bmatrix}\begin{bmatrix}2 & 4\end{bmatrix}$?

Field selection: :answer-field.type/radio

Raw source missing correct designation.

* \begin{bmatrix}6 & 12 \\ 2 & 4 \\ 2 & 4\end{bmatrix}

* [6]

* Undefined

* \begin{bmatrix}6 & 12 \\ 0 & 0 \\ 2 & 4\end{bmatrix}

* \begin{bmatrix}6 & 12 \\ 5 & 4\end{bmatrix}

Worked solution:

Raw source missing worked solution.

Original replay (evidence-only)

### easy / undefined-evidence / q-13636

Find $CD$, if
$C = \begin{bmatrix}1 & 2\end{bmatrix}$
and
$D = \begin{bmatrix}0 \\ -2 \\ -3\end{bmatrix}$.

Field selection: :answer-field.type/radio

Raw source missing correct designation.

* [4]

* \begin{bmatrix}1 & 0 \\ -2 & -4 \\ -3 & -6\end{bmatrix}

* Undefined

* \begin{bmatrix}0 & 0 \\ -2 & -4 \\ -3 & -6\end{bmatrix}

* \begin{bmatrix}0 & 0 \\ -2 & -4 \\ 3 & -6\end{bmatrix}

Worked solution:

Raw source missing worked solution.

Original replay (evidence-only)

### easy / outer-4x3 / q-1038

$\begin{bmatrix}-10 \\ 6 \\ 0 \\ 8\end{bmatrix}\begin{bmatrix}1 & -5 & -1\end{bmatrix}=$

Field selection: :answer-field.type/radio

* Undefined

* \begin{bmatrix}-10 & 50 & 10 \\ 6 & -30 & -6 \\ 0 & 0 & 0\end{bmatrix}

* \begin{bmatrix}-10 & -30 & 0 & -8\end{bmatrix}

* \begin{bmatrix}-10 & -50 & -10 \\ 6 & -30 & -6 \\ 0 & 0 & 0 \\ 8 & -40 & -8\end{bmatrix}

* correct: \begin{bmatrix}-10 & 50 & 10 \\ 6 & -30 & -6 \\ 0 & 0 & 0 \\ 8 & -40 & -8\end{bmatrix}

Worked solution:

Here, the first factor is $4\times 1$ matrix and the second factor is a $1\times 3$ matrix. 

There is $1$ column in the first matrix and $1$ row in the second matrix, so the product is well defined:

$$
4\times \boxed{\text{1}}✓\boxed{\text{1}}\times 3=4\times 3
$$

Computing the product, we have:

$$
\begin{aligned}\begin{bmatrix}-10 \\ 6 \\ 0 \\ 8\end{bmatrix}\begin{bmatrix}1 & -5 & -1\end{bmatrix} & =\begin{bmatrix}-10\cdot 1 & -10\cdot (-5) & -10\cdot (-1) \\ 6\cdot 1 & 6\cdot (-5) & 6\cdot (-1) \\ 0\cdot 1 & 0\cdot (-5) & 0\cdot (-1) \\ 8\cdot 1 & 8\cdot (-5) & 8\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}-10 & 50 & 10 \\ 6 & -30 & -6 \\ 0 & 0 & 0 \\ 8 & -40 & -8\end{bmatrix}\end{aligned}
$$

Original replay (evidence-only)

### easy / outer-2x2 / q-129961

If
$A=\begin{bmatrix}-1 \\ -3\end{bmatrix}$
and
$B=\begin{bmatrix}3 & -1\end{bmatrix}$
then $AB=$

Field selection: :answer-field.type/radio

* \begin{bmatrix}3 & -1 \\ -9 & 3\end{bmatrix}

* correct: \begin{bmatrix}-3 & 1 \\ -9 & 3\end{bmatrix}

* \begin{bmatrix}-3 \\ -1\end{bmatrix}

* \begin{bmatrix}-1 \\ -9\end{bmatrix}

* \begin{bmatrix}-3 & 9\end{bmatrix}

Worked solution:

Here, $A$ is a $2\times 1$ matrix and $B$ is a $1\times 2$ matrix. 

There is $1$ column in $A$ and $1$ row in $B,$ so $A$ and $B$ are conformable for multiplication: 

$$
{A}_{2\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}-1 \\ -3\end{bmatrix}\begin{bmatrix}3 & -1\end{bmatrix}=\begin{bmatrix}-3 & ∗ \\ ∗ & ∗\end{bmatrix}, &  & \,-3=-1\cdot 3 \\  & \begin{bmatrix}-1 \\ -3\end{bmatrix}\begin{bmatrix}3 & -1\end{bmatrix}=\begin{bmatrix}-3 & 1 \\ ∗ & ∗\end{bmatrix}, &  & \,1=(-1)\cdot (-1) \\  & \begin{bmatrix}-1 \\ -3\end{bmatrix}\begin{bmatrix}3 & -1\end{bmatrix}=\begin{bmatrix}-3 & 1 \\ -9 & ∗\end{bmatrix}, &  & \,-9=(-3)\cdot 3 \\  & \begin{bmatrix}-1 \\ -3\end{bmatrix}\begin{bmatrix}3 & -1\end{bmatrix}=\begin{bmatrix}-3 & 1 \\ -9 & 3\end{bmatrix}, &  & \,3=(-3)\cdot (-1)\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}-3 & 1 \\ -9 & 3\end{bmatrix}.$

Original replay (evidence-only)

### easy / outer-4x3 / q-130136

$\begin{bmatrix}4 \\ 2 \\ 1 \\ 1\end{bmatrix}\begin{bmatrix}1 & 0 & 4\end{bmatrix}=$

Field selection: :answer-field.type/radio

* \begin{bmatrix}4 & 1 & 16 & 1 \\ 2 & -1 & 8 & 2 \\ 0 & 0 & 0 & 0 \\ 1 & 0 & 4 & 3\end{bmatrix}

* \begin{bmatrix}4 & 1 & 16 & 1 \\ 0 & 0 & 0 & 0 \\ 2 & -1 & 8 & 2 \\ 1 & 0 & 4 & 3\end{bmatrix}

* correct: \begin{bmatrix}4 & 0 & 16 \\ 2 & 0 & 8 \\ 1 & 0 & 4 \\ 1 & 0 & 4\end{bmatrix}

* Undefined

* \begin{bmatrix}4 & 1 & 16 \\ 2 & -1 & 8 \\ 1 & 0 & 4 \\ 0 & 4 & 0\end{bmatrix}

Worked solution:

Here, the first factor is $4\times 1$ matrix and the second factor is a $1\times 3$ matrix. 

There is $1$ column in the first matrix and $1$ row in the second matrix, so the product is well defined:

$$
4\times \boxed{\text{1}}✓\boxed{\text{1}}\times 3=4\times 3
$$

Computing the product, we have

$$
\begin{aligned}\begin{bmatrix}4 \\ 2 \\ 1 \\ 1\end{bmatrix}\begin{bmatrix}1 & 0 & 4\end{bmatrix} & =\begin{bmatrix}4\cdot 1 & 4\cdot 0 & 4\cdot 4 \\ 2\cdot 1 & 2\cdot 0 & 2\cdot 4 \\ 1\cdot 1 & 1\cdot 0 & 1\cdot 4 \\ 1\cdot 1 & 1\cdot 0 & 1\cdot 4\end{bmatrix} \\  & =\begin{bmatrix}4 & 0 & 16 \\ 2 & 0 & 8 \\ 1 & 0 & 4 \\ 1 & 0 & 4\end{bmatrix}\end{aligned}
$$

Original replay (evidence-only)

### moderate / undefined-evidence / q-130230

Find $ST$, if 
$S=\begin{bmatrix}3 \\ -4 \\ 2\end{bmatrix}$
and 
$T=\begin{bmatrix}4 \\ -3\end{bmatrix}.$

Field selection: :answer-field.type/radio

* correct: Undefined

* \begin{bmatrix}12 & -15 \\ -16 & 20 \\ 8 & -10\end{bmatrix}

* \begin{bmatrix}24\end{bmatrix}

* \begin{bmatrix}12 & -15 \\ 8 & -10\end{bmatrix}

* \begin{bmatrix}-1\end{bmatrix}

Worked solution:

Here, $S$ is $3\times 1$ matrix and $T$ is a $2\times 1$ matrix. 

There is $1$ column in $S$ and $2$ rows in $T$, so the product is undefined:

$$
{S}_{3\times 1}{\times }_{\ne }{T}_{2\times 1}=\text{undefined}
$$

Original replay (evidence-only)

### easy / outer-2x2 / q-275545

If
$A=\begin{bmatrix}2 \\ -1\end{bmatrix}$
and
$B=\begin{bmatrix}-2 & 3\end{bmatrix},$
find $AB.$

| $AB=\,\,$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
|  | {{field-3}} | {{field-4}} |  |  |

Field field-4: :answer-field.type/blank

* correct: -3

Field field-2: :answer-field.type/blank

* correct: 6

Field field-1: :answer-field.type/blank

* correct: -4

Field field-3: :answer-field.type/blank

* correct: 2

Worked solution:

Here, $A$ is a $2\times 1$ matrix and $B$ is a $1\times 2$ matrix. 

There is $1$ column in $A$ and $1$ row in $B,$ so $A$ and $B$ are conformable for multiplication: 

$$
{A}_{2\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}2 \\ -1\end{bmatrix}\begin{bmatrix}-2 & 3\end{bmatrix}=\begin{bmatrix}-4 & ∗ \\ ∗ & ∗\end{bmatrix}, &  & \,-4=2\cdot -2 \\  & \begin{bmatrix}2 \\ -1\end{bmatrix}\begin{bmatrix}-2 & 3\end{bmatrix}=\begin{bmatrix}-4 & 6 \\ ∗ & ∗\end{bmatrix}, &  & \,6=2\cdot 3 \\  & \begin{bmatrix}2 \\ -1\end{bmatrix}\begin{bmatrix}-2 & 3\end{bmatrix}=\begin{bmatrix}-4 & 6 \\ 2 & ∗\end{bmatrix}, &  & \,2=-1\cdot -2 \\  & \begin{bmatrix}2 \\ -1\end{bmatrix}\begin{bmatrix}-2 & 3\end{bmatrix}=\begin{bmatrix}-4 & 6 \\ 2 & -3\end{bmatrix}, &  & \,-3=-1\cdot 3\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}-4 & 6 \\ 2 & -3\end{bmatrix}.$

Original replay (evidence-only)

### easy / outer-3x2 / q-275548

Find $AB,$ if $A=\begin{bmatrix}1 \\ 2 \\ -2\end{bmatrix}$
and 
$B=\begin{bmatrix}1 & -2\end{bmatrix}.$

|  |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
| $AB=\,\,$ |  | {{field-3}} | {{field-4}} |  |
|  |  | {{field-5}} | {{field-6}} |  |

Field field-6: :answer-field.type/blank

* correct: 4

Field field-3: :answer-field.type/blank

* correct: 2

Field field-2: :answer-field.type/blank

* correct: -2

Field field-5: :answer-field.type/blank

* correct: -2

Field field-4: :answer-field.type/blank

* correct: -4

Field field-1: :answer-field.type/blank

* correct: 1

Worked solution:

Here, $A$ is $3\times 1$ matrix and $B$ is a $1\times 2$ matrix.  

There is $1$ column in matrix $A$ and $1$ row in matrix $B$, so the product is well defined:

$$
{A}_{3\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{3\times 2}
$$

Computing the product, we have

$$
\begin{aligned}AB & =\begin{bmatrix}1 \\ 2 \\ -2\end{bmatrix}\begin{bmatrix}1 & -2\end{bmatrix} \\  & =\begin{bmatrix}1\cdot 1 & 1\cdot (-2) \\ 2\cdot 1 & 2\cdot (-2) \\ (-2)\cdot 1 & (-2)\cdot (-2)\end{bmatrix} \\  & =\begin{bmatrix}1 & -2 \\ 2 & -4 \\ -2 & 4\end{bmatrix}.\end{aligned}
$$

Original replay (evidence-only)

### easy / outer-2x2 / q-318484

If
$A=\begin{bmatrix}5 \\ -2\end{bmatrix}$
and
$B=\begin{bmatrix}1 & -3\end{bmatrix},$
find $AB.$

| $AB=\,\,$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
|  | {{field-3}} | {{field-4}} |  |  |

Field field-2: :answer-field.type/blank

* correct: -15

Field field-1: :answer-field.type/blank

* correct: 5

Field field-4: :answer-field.type/blank

* correct: 6

Field field-3: :answer-field.type/blank

* correct: -2

Worked solution:

Here, $A$ is a $2\times 1$ matrix and $B$ is a $1\times 2$ matrix. 

There is $1$ column in $A$ and $1$ row in $B,$ so $A$ and $B$ are conformable for multiplication: 

$$
{A}_{2\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}5 \\ -2\end{bmatrix}\begin{bmatrix}1 & -3\end{bmatrix}=\begin{bmatrix}5 & ∗ \\ ∗ & ∗\end{bmatrix}, &  & \,5=5\cdot 1 \\  & \begin{bmatrix}5 \\ -2\end{bmatrix}\begin{bmatrix}1 & -3\end{bmatrix}=\begin{bmatrix}5 & -15 \\ ∗ & ∗\end{bmatrix}, &  & \,-15=5\cdot (-3) \\  & \begin{bmatrix}5 \\ -2\end{bmatrix}\begin{bmatrix}1 & -3\end{bmatrix}=\begin{bmatrix}5 & -15 \\ -2 & ∗\end{bmatrix}, &  & \,-2=-2\cdot 1 \\  & \begin{bmatrix}5 \\ -2\end{bmatrix}\begin{bmatrix}1 & -3\end{bmatrix}=\begin{bmatrix}5 & -15 \\ -2 & 6\end{bmatrix}, &  & \,6=-2\cdot (-3)\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}5 & -15 \\ -2 & 6\end{bmatrix}.$

Original replay (evidence-only)

### easy / outer-3x2 / q-318588

Find $PQ,$ if
$P=\begin{bmatrix}0 \\ 3 \\ -1\end{bmatrix}$
and
$Q=\begin{bmatrix}-4 & 2\end{bmatrix}.$

|  |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
| $PQ=\,\,$ |  | {{field-3}} | {{field-4}} |  |
|  |  | {{field-5}} | {{field-6}} |  |

Field field-4: :answer-field.type/blank

* correct: 6

Field field-6: :answer-field.type/blank

* correct: -2

Field field-2: :answer-field.type/blank

* correct: 0

Field field-5: :answer-field.type/blank

* correct: 4

Field field-3: :answer-field.type/blank

* correct: -12

Field field-1: :answer-field.type/blank

* correct: 0

Worked solution:

Here, $P$ is a $3\times 1$ matrix and $Q$ is a $1\times 2$ matrix.  

There is $1$ column in matrix $P$ and $1$ row in matrix $Q$, so the product is well defined:

$$
{P}_{3\times \boxed{\text{1}}}{\cdot }_{✓}{Q}_{\boxed{\text{1}}\times 2}={PQ}_{3\times 2}
$$

Computing the product, we have:

$$
\begin{aligned}PQ & =\begin{bmatrix}0 \\ 3 \\ -1\end{bmatrix}\begin{bmatrix}-4 & 2\end{bmatrix} \\  & =\begin{bmatrix}0\cdot (-4) & 0\cdot 2 \\ 3\cdot (-4) & 3\cdot 2 \\ (-1)\cdot (-4) & (-1)\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}0 & 0 \\ -12 & 6 \\ 4 & -2\end{bmatrix}.\end{aligned}
$$

Original replay (evidence-only)

### easy / outer-3x2 / q-13635

Find $AB$, if 
$A=\begin{bmatrix}0 \\ -2 \\ -3\end{bmatrix}$
and 
$B=\begin{bmatrix}1 & 2\end{bmatrix}.$

Field selection: :answer-field.type/radio

* $$
\begin{bmatrix}1 & 0 \\ -2 & -4 \\ -3 & -6\end{bmatrix}
$$

* $$
\begin{bmatrix}1 & 2 \\ -2 & -4 \\ -3 & -6\end{bmatrix}
$$

* correct: $$
\begin{bmatrix}0 & 0 \\ -2 & -4 \\ -3 & -6\end{bmatrix}
$$

* $$
\begin{bmatrix}0 & 0 \\ -2 & -4 \\ 3 & -6\end{bmatrix}
$$

* Undefined

Worked solution:

Here, $A$ is $3\times 1$ matrix and $B$ is a $1\times 2$ matrix. 

There is $1$ column in matrix $A$ and $1$ row in matrix $B$, so the product is well defined:

$$
{A}_{3\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{3\times 2}
$$

Computing the product, we have:

$$
\begin{aligned}AB & =\begin{bmatrix}0 \\ -2 \\ -3\end{bmatrix}\begin{bmatrix}1 & 2\end{bmatrix} \\  & =\begin{bmatrix}0\cdot 1 & 0\cdot 2 \\ (-2)\cdot 1 & (-2)\cdot 2 \\ (-3)\cdot 1 & (-3)\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}0 & 0 \\ -2 & -4 \\ -3 & -6\end{bmatrix}\end{aligned}
$$

Authored generated variant

### easy / outer-3x2 / authored-method/q-13635

Find $AB,$ if $A=\begin{bmatrix}0 \\ 1 \\ -1\end{bmatrix}$
and 
$B=\begin{bmatrix}3 & -3\end{bmatrix}.$

|  |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
| $AB=\,\,$ |  | {{field-3}} | {{field-4}} |  |
|  |  | {{field-5}} | {{field-6}} |  |

Field field-1: :answer-field.type/blank

* correct: 0

Field field-2: :answer-field.type/blank

* correct: 0

Field field-3: :answer-field.type/blank

* correct: 3

Field field-4: :answer-field.type/blank

* correct: -3

Field field-5: :answer-field.type/blank

* correct: -3

Field field-6: :answer-field.type/blank

* correct: 3

Worked solution:

Here, $A$ is $3\times 1$ matrix and $B$ is a $1\times 2$ matrix.  

There is $1$ column in matrix $A$ and $1$ row in matrix $B$, so the product is well defined:

$$
{A}_{3\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{3\times 2}
$$

Computing the product, we have

$$
\begin{aligned}AB & =\begin{bmatrix}0 \\ 1 \\ -1\end{bmatrix}\begin{bmatrix}3 & -3\end{bmatrix} \\  & =\begin{bmatrix}0\cdot 3 & 0\cdot (-3) \\ 1\cdot 3 & 1\cdot (-3) \\ (-1)\cdot 3 & (-1)\cdot (-3)\end{bmatrix} \\  & =\begin{bmatrix}0 & 0 \\ 3 & -3 \\ -3 & 3\end{bmatrix}.\end{aligned}
$$

Authored generated variant

### easy / outer-2x2 / authored-method/q-275545

If
$A=\begin{bmatrix}-1 \\ -1\end{bmatrix}$
and
$B=\begin{bmatrix}2 & -5\end{bmatrix},$
find $AB.$

Field selection: :answer-field.type/radio

* \begin{bmatrix}-2 & -2 \\ 5 & 5\end{bmatrix}

* correct: \begin{bmatrix}-2 & 5 \\ -2 & 5\end{bmatrix}

* \begin{bmatrix}1 & -6 \\ 1 & -6\end{bmatrix}

* Undefined

* \begin{bmatrix}2 & -5 \\ 2 & -5\end{bmatrix}

Worked solution:

Here, $A$ is a $2\times 1$ matrix and $B$ is a $1\times 2$ matrix. 

There is $1$ column in $A$ and $1$ row in $B,$ so $A$ and $B$ are conformable for multiplication: 

$$
{A}_{2\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}-1 \\ -1\end{bmatrix}\begin{bmatrix}2 & -5\end{bmatrix}=\begin{bmatrix}-2 & ∗ \\ ∗ & ∗\end{bmatrix}, &  & \,-2=(-1)\cdot 2 \\  & \begin{bmatrix}-1 \\ -1\end{bmatrix}\begin{bmatrix}2 & -5\end{bmatrix}=\begin{bmatrix}-2 & 5 \\ ∗ & ∗\end{bmatrix}, &  & \,5=(-1)\cdot (-5) \\  & \begin{bmatrix}-1 \\ -1\end{bmatrix}\begin{bmatrix}2 & -5\end{bmatrix}=\begin{bmatrix}-2 & 5 \\ -2 & ∗\end{bmatrix}, &  & \,-2=(-1)\cdot 2 \\  & \begin{bmatrix}-1 \\ -1\end{bmatrix}\begin{bmatrix}2 & -5\end{bmatrix}=\begin{bmatrix}-2 & 5 \\ -2 & 5\end{bmatrix}, &  & \,5=(-1)\cdot (-5)\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}-2 & 5 \\ -2 & 5\end{bmatrix}.$

Authored generated variant

### easy / outer-2x2 / authored-method/q-129961

If
$A=\begin{bmatrix}0 \\ 1\end{bmatrix}$
and
$B=\begin{bmatrix}-2 & 4\end{bmatrix}$
then $AB=$

Field selection: :answer-field.type/radio

* Undefined

* \begin{bmatrix}-2 & 4 \\ -1 & 5\end{bmatrix}

* \begin{bmatrix}0 & 0 \\ 2 & -4\end{bmatrix}

* \begin{bmatrix}0 & -2 \\ 0 & 4\end{bmatrix}

* correct: \begin{bmatrix}0 & 0 \\ -2 & 4\end{bmatrix}

Worked solution:

Here, $A$ is a $2\times 1$ matrix and $B$ is a $1\times 2$ matrix. 

There is $1$ column in $A$ and $1$ row in $B,$ so $A$ and $B$ are conformable for multiplication: 

$$
{A}_{2\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}0 \\ 1\end{bmatrix}\begin{bmatrix}-2 & 4\end{bmatrix}=\begin{bmatrix}0 & ∗ \\ ∗ & ∗\end{bmatrix}, &  & \,0=0\cdot (-2) \\  & \begin{bmatrix}0 \\ 1\end{bmatrix}\begin{bmatrix}-2 & 4\end{bmatrix}=\begin{bmatrix}0 & 0 \\ ∗ & ∗\end{bmatrix}, &  & \,0=0\cdot 4 \\  & \begin{bmatrix}0 \\ 1\end{bmatrix}\begin{bmatrix}-2 & 4\end{bmatrix}=\begin{bmatrix}0 & 0 \\ -2 & ∗\end{bmatrix}, &  & \,-2=1\cdot (-2) \\  & \begin{bmatrix}0 \\ 1\end{bmatrix}\begin{bmatrix}-2 & 4\end{bmatrix}=\begin{bmatrix}0 & 0 \\ -2 & 4\end{bmatrix}, &  & \,4=1\cdot 4\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}0 & 0 \\ -2 & 4\end{bmatrix}.$

Authored generated variant

### easy / outer-4x3 / authored-method/q-130136

$\begin{bmatrix}10 \\ 6 \\ -10 \\ 4\end{bmatrix}\begin{bmatrix}-1 & 1 & -1\end{bmatrix}=$

| {{field-1}} | {{field-2}} | {{field-3}} |
| --- | --- | --- |
| {{field-4}} | {{field-5}} | {{field-6}} |
| {{field-7}} | {{field-8}} | {{field-9}} |
| {{field-10}} | {{field-11}} | {{field-12}} |

Field field-1: :answer-field.type/blank

* correct: -10

Field field-2: :answer-field.type/blank

* correct: 10

Field field-3: :answer-field.type/blank

* correct: -10

Field field-4: :answer-field.type/blank

* correct: -6

Field field-5: :answer-field.type/blank

* correct: 6

Field field-6: :answer-field.type/blank

* correct: -6

Field field-7: :answer-field.type/blank

* correct: 10

Field field-8: :answer-field.type/blank

* correct: -10

Field field-9: :answer-field.type/blank

* correct: 10

Field field-10: :answer-field.type/blank

* correct: -4

Field field-11: :answer-field.type/blank

* correct: 4

Field field-12: :answer-field.type/blank

* correct: -4

Worked solution:

Here, the first factor is $4\times 1$ matrix and the second factor is a $1\times 3$ matrix. 

There is $1$ column in the first matrix and $1$ row in the second matrix, so the product is well defined:

$$
4\times \boxed{\text{1}}✓\boxed{\text{1}}\times 3=4\times 3
$$

Computing the product, we have

$$
\begin{aligned}\begin{bmatrix}10 \\ 6 \\ -10 \\ 4\end{bmatrix}\begin{bmatrix}-1 & 1 & -1\end{bmatrix} & =\begin{bmatrix}10\cdot (-1) & 10\cdot 1 & 10\cdot (-1) \\ 6\cdot (-1) & 6\cdot 1 & 6\cdot (-1) \\ (-10)\cdot (-1) & (-10)\cdot 1 & (-10)\cdot (-1) \\ 4\cdot (-1) & 4\cdot 1 & 4\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}-10 & 10 & -10 \\ -6 & 6 & -6 \\ 10 & -10 & 10 \\ -4 & 4 & -4\end{bmatrix}\end{aligned}
$$

Authored generated variant

### easy / outer-3x2 / authored-method/q-275548

Find $AB,$ if $A=\begin{bmatrix}1 \\ -1 \\ 1\end{bmatrix}$
and 
$B=\begin{bmatrix}-2 & -5\end{bmatrix}.$

Field selection: :answer-field.type/radio

* \begin{bmatrix}-1 & -4 \\ -3 & -6 \\ -1 & -4\end{bmatrix}

* Undefined

* \begin{bmatrix}-2 & 2 & -2 \\ -5 & 5 & -5\end{bmatrix}

* \begin{bmatrix}2 & 5 \\ -2 & -5 \\ 2 & 5\end{bmatrix}

* correct: \begin{bmatrix}-2 & -5 \\ 2 & 5 \\ -2 & -5\end{bmatrix}

Worked solution:

Here, $A$ is $3\times 1$ matrix and $B$ is a $1\times 2$ matrix.  

There is $1$ column in matrix $A$ and $1$ row in matrix $B$, so the product is well defined:

$$
{A}_{3\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{3\times 2}
$$

Computing the product, we have

$$
\begin{aligned}AB & =\begin{bmatrix}1 \\ -1 \\ 1\end{bmatrix}\begin{bmatrix}-2 & -5\end{bmatrix} \\  & =\begin{bmatrix}1\cdot (-2) & 1\cdot (-5) \\ (-1)\cdot (-2) & (-1)\cdot (-5) \\ 1\cdot (-2) & 1\cdot (-5)\end{bmatrix} \\  & =\begin{bmatrix}-2 & -5 \\ 2 & 5 \\ -2 & -5\end{bmatrix}.\end{aligned}
$$

Authored generated variant

### easy / outer-3x2 / authored-method/q-318588

Find $AB,$ if $A=\begin{bmatrix}0 \\ 0 \\ 1\end{bmatrix}$
and 
$B=\begin{bmatrix}2 & 4\end{bmatrix}.$

|  |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
| $AB=\,\,$ |  | {{field-3}} | {{field-4}} |  |
|  |  | {{field-5}} | {{field-6}} |  |

Field field-1: :answer-field.type/blank

* correct: 0

Field field-2: :answer-field.type/blank

* correct: 0

Field field-3: :answer-field.type/blank

* correct: 0

Field field-4: :answer-field.type/blank

* correct: 0

Field field-5: :answer-field.type/blank

* correct: 2

Field field-6: :answer-field.type/blank

* correct: 4

Worked solution:

Here, $A$ is $3\times 1$ matrix and $B$ is a $1\times 2$ matrix.  

There is $1$ column in matrix $A$ and $1$ row in matrix $B$, so the product is well defined:

$$
{A}_{3\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{3\times 2}
$$

Computing the product, we have

$$
\begin{aligned}AB & =\begin{bmatrix}0 \\ 0 \\ 1\end{bmatrix}\begin{bmatrix}2 & 4\end{bmatrix} \\  & =\begin{bmatrix}0\cdot 2 & 0\cdot 4 \\ 0\cdot 2 & 0\cdot 4 \\ 1\cdot 2 & 1\cdot 4\end{bmatrix} \\  & =\begin{bmatrix}0 & 0 \\ 0 & 0 \\ 2 & 4\end{bmatrix}.\end{aligned}
$$

Authored generated variant

### easy / outer-2x2 / authored-method/q-318484

If
$A=\begin{bmatrix}-9 \\ -5\end{bmatrix}$
and
$B=\begin{bmatrix}-1 & -1\end{bmatrix},$
find $AB.$

Field selection: :answer-field.type/radio

* Undefined

* \begin{bmatrix}-9 & -9 \\ -5 & -5\end{bmatrix}

* correct: \begin{bmatrix}9 & 9 \\ 5 & 5\end{bmatrix}

* \begin{bmatrix}-10 & -10 \\ -6 & -6\end{bmatrix}

* \begin{bmatrix}9 & 5 \\ 9 & 5\end{bmatrix}

Worked solution:

Here, $A$ is a $2\times 1$ matrix and $B$ is a $1\times 2$ matrix. 

There is $1$ column in $A$ and $1$ row in $B,$ so $A$ and $B$ are conformable for multiplication: 

$$
{A}_{2\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}-9 \\ -5\end{bmatrix}\begin{bmatrix}-1 & -1\end{bmatrix}=\begin{bmatrix}9 & ∗ \\ ∗ & ∗\end{bmatrix}, &  & \,9=(-9)\cdot (-1) \\  & \begin{bmatrix}-9 \\ -5\end{bmatrix}\begin{bmatrix}-1 & -1\end{bmatrix}=\begin{bmatrix}9 & 9 \\ ∗ & ∗\end{bmatrix}, &  & \,9=(-9)\cdot (-1) \\  & \begin{bmatrix}-9 \\ -5\end{bmatrix}\begin{bmatrix}-1 & -1\end{bmatrix}=\begin{bmatrix}9 & 9 \\ 5 & ∗\end{bmatrix}, &  & \,5=(-5)\cdot (-1) \\  & \begin{bmatrix}-9 \\ -5\end{bmatrix}\begin{bmatrix}-1 & -1\end{bmatrix}=\begin{bmatrix}9 & 9 \\ 5 & 5\end{bmatrix}, &  & \,5=(-5)\cdot (-1)\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}9 & 9 \\ 5 & 5\end{bmatrix}.$

Authored generated variant

### easy / outer-4x3 / authored-method/q-1038

$\begin{bmatrix}6 \\ -4 \\ 2 \\ 1\end{bmatrix}\begin{bmatrix}1 & 0 & 1\end{bmatrix}=$

Field selection: :answer-field.type/radio

* \begin{bmatrix}-6 & 0 & -6 \\ 4 & 0 & 4 \\ -2 & 0 & -2 \\ -1 & 0 & -1\end{bmatrix}

* \begin{bmatrix}6 & -4 & 2 & 1 \\ 0 & 0 & 0 & 0 \\ 6 & -4 & 2 & 1\end{bmatrix}

* correct: \begin{bmatrix}6 & 0 & 6 \\ -4 & 0 & -4 \\ 2 & 0 & 2 \\ 1 & 0 & 1\end{bmatrix}

* \begin{bmatrix}7 & 6 & 7 \\ -3 & -4 & -3 \\ 3 & 2 & 3 \\ 2 & 1 & 2\end{bmatrix}

* Undefined

Worked solution:

Here, the first factor is $4\times 1$ matrix and the second factor is a $1\times 3$ matrix. 

There is $1$ column in the first matrix and $1$ row in the second matrix, so the product is well defined:

$$
4\times \boxed{\text{1}}✓\boxed{\text{1}}\times 3=4\times 3
$$

Computing the product, we have:

$$
\begin{aligned}\begin{bmatrix}6 \\ -4 \\ 2 \\ 1\end{bmatrix}\begin{bmatrix}1 & 0 & 1\end{bmatrix} & =\begin{bmatrix}6\cdot 1 & 6\cdot 0 & 6\cdot 1 \\ (-4)\cdot 1 & (-4)\cdot 0 & (-4)\cdot 1 \\ 2\cdot 1 & 2\cdot 0 & 2\cdot 1 \\ 1\cdot 1 & 1\cdot 0 & 1\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}6 & 0 & 6 \\ -4 & 0 & -4 \\ 2 & 0 & 2 \\ 1 & 0 & 1\end{bmatrix}\end{aligned}
$$

Authored generated variant

### moderate / outer-3x2 / authored-method/q-13635

Find $AB,$ if $A=\begin{bmatrix}3 \\ -2 \\ -3\end{bmatrix}$
and 
$B=\begin{bmatrix}2 & -3\end{bmatrix}.$

|  |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
| $AB=\,\,$ |  | {{field-3}} | {{field-4}} |  |
|  |  | {{field-5}} | {{field-6}} |  |

Field field-1: :answer-field.type/blank

* correct: 6

Field field-2: :answer-field.type/blank

* correct: -9

Field field-3: :answer-field.type/blank

* correct: -4

Field field-4: :answer-field.type/blank

* correct: 6

Field field-5: :answer-field.type/blank

* correct: -6

Field field-6: :answer-field.type/blank

* correct: 9

Worked solution:

Here, $A$ is $3\times 1$ matrix and $B$ is a $1\times 2$ matrix.  

There is $1$ column in matrix $A$ and $1$ row in matrix $B$, so the product is well defined:

$$
{A}_{3\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{3\times 2}
$$

Computing the product, we have

$$
\begin{aligned}AB & =\begin{bmatrix}3 \\ -2 \\ -3\end{bmatrix}\begin{bmatrix}2 & -3\end{bmatrix} \\  & =\begin{bmatrix}3\cdot 2 & 3\cdot (-3) \\ (-2)\cdot 2 & (-2)\cdot (-3) \\ (-3)\cdot 2 & (-3)\cdot (-3)\end{bmatrix} \\  & =\begin{bmatrix}6 & -9 \\ -4 & 6 \\ -6 & 9\end{bmatrix}.\end{aligned}
$$

Authored generated variant

### moderate / outer-3x2 / authored-method/q-275548

Find $AB,$ if $A=\begin{bmatrix}4 \\ -5 \\ 5\end{bmatrix}$
and 
$B=\begin{bmatrix}2 & -2\end{bmatrix}.$

Field selection: :answer-field.type/radio

* \begin{bmatrix}6 & 2 \\ -3 & -7 \\ 7 & 3\end{bmatrix}

* \begin{bmatrix}-8 & 8 \\ 10 & -10 \\ -10 & 10\end{bmatrix}

* \begin{bmatrix}8 & -10 & 10 \\ -8 & 10 & -10\end{bmatrix}

* correct: \begin{bmatrix}8 & -8 \\ -10 & 10 \\ 10 & -10\end{bmatrix}

* Undefined

Worked solution:

Here, $A$ is $3\times 1$ matrix and $B$ is a $1\times 2$ matrix.  

There is $1$ column in matrix $A$ and $1$ row in matrix $B$, so the product is well defined:

$$
{A}_{3\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{3\times 2}
$$

Computing the product, we have

$$
\begin{aligned}AB & =\begin{bmatrix}4 \\ -5 \\ 5\end{bmatrix}\begin{bmatrix}2 & -2\end{bmatrix} \\  & =\begin{bmatrix}4\cdot 2 & 4\cdot (-2) \\ (-5)\cdot 2 & (-5)\cdot (-2) \\ 5\cdot 2 & 5\cdot (-2)\end{bmatrix} \\  & =\begin{bmatrix}8 & -8 \\ -10 & 10 \\ 10 & -10\end{bmatrix}.\end{aligned}
$$

Authored generated variant

### moderate / outer-3x2 / authored-method/q-318588

Find $AB,$ if $A=\begin{bmatrix}-5 \\ -2 \\ -2\end{bmatrix}$
and 
$B=\begin{bmatrix}-3 & -3\end{bmatrix}.$

|  |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
| $AB=\,\,$ |  | {{field-3}} | {{field-4}} |  |
|  |  | {{field-5}} | {{field-6}} |  |

Field field-1: :answer-field.type/blank

* correct: 15

Field field-2: :answer-field.type/blank

* correct: 15

Field field-3: :answer-field.type/blank

* correct: 6

Field field-4: :answer-field.type/blank

* correct: 6

Field field-5: :answer-field.type/blank

* correct: 6

Field field-6: :answer-field.type/blank

* correct: 6

Worked solution:

Here, $A$ is $3\times 1$ matrix and $B$ is a $1\times 2$ matrix.  

There is $1$ column in matrix $A$ and $1$ row in matrix $B$, so the product is well defined:

$$
{A}_{3\times \boxed{\text{1}}}{\cdot }_{✓}{B}_{\boxed{\text{1}}\times 2}={AB}_{3\times 2}
$$

Computing the product, we have

$$
\begin{aligned}AB & =\begin{bmatrix}-5 \\ -2 \\ -2\end{bmatrix}\begin{bmatrix}-3 & -3\end{bmatrix} \\  & =\begin{bmatrix}(-5)\cdot (-3) & (-5)\cdot (-3) \\ (-2)\cdot (-3) & (-2)\cdot (-3) \\ (-2)\cdot (-3) & (-2)\cdot (-3)\end{bmatrix} \\  & =\begin{bmatrix}15 & 15 \\ 6 & 6 \\ 6 & 6\end{bmatrix}.\end{aligned}
$$

Authored generated variant

### hard / outer-4x3 / authored-method/q-1038

$\begin{bmatrix}2 \\ -3 \\ 4 \\ -5\end{bmatrix}\begin{bmatrix}3 & -6 & -4\end{bmatrix}=$

| {{field-1}} | {{field-2}} | {{field-3}} |
| --- | --- | --- |
| {{field-4}} | {{field-5}} | {{field-6}} |
| {{field-7}} | {{field-8}} | {{field-9}} |
| {{field-10}} | {{field-11}} | {{field-12}} |

Field field-1: :answer-field.type/blank

* correct: 6

Field field-2: :answer-field.type/blank

* correct: -12

Field field-3: :answer-field.type/blank

* correct: -8

Field field-4: :answer-field.type/blank

* correct: -9

Field field-5: :answer-field.type/blank

* correct: 18

Field field-6: :answer-field.type/blank

* correct: 12

Field field-7: :answer-field.type/blank

* correct: 12

Field field-8: :answer-field.type/blank

* correct: -24

Field field-9: :answer-field.type/blank

* correct: -16

Field field-10: :answer-field.type/blank

* correct: -15

Field field-11: :answer-field.type/blank

* correct: 30

Field field-12: :answer-field.type/blank

* correct: 20

Worked solution:

Here, the first factor is $4\times 1$ matrix and the second factor is a $1\times 3$ matrix. 

There is $1$ column in the first matrix and $1$ row in the second matrix, so the product is well defined:

$$
4\times \boxed{\text{1}}✓\boxed{\text{1}}\times 3=4\times 3
$$

Computing the product, we have:

$$
\begin{aligned}\begin{bmatrix}2 \\ -3 \\ 4 \\ -5\end{bmatrix}\begin{bmatrix}3 & -6 & -4\end{bmatrix} & =\begin{bmatrix}2\cdot 3 & 2\cdot (-6) & 2\cdot (-4) \\ (-3)\cdot 3 & (-3)\cdot (-6) & (-3)\cdot (-4) \\ 4\cdot 3 & 4\cdot (-6) & 4\cdot (-4) \\ (-5)\cdot 3 & (-5)\cdot (-6) & (-5)\cdot (-4)\end{bmatrix} \\  & =\begin{bmatrix}6 & -12 & -8 \\ -9 & 18 & 12 \\ 12 & -24 & -16 \\ -15 & 30 & 20\end{bmatrix}\end{aligned}
$$

Authored generated variant

### hard / outer-4x3 / authored-method/q-130136

$\begin{bmatrix}4 \\ -3 \\ 2 \\ -4\end{bmatrix}\begin{bmatrix}5 & 3 & 4\end{bmatrix}=$

Field selection: :answer-field.type/radio

* \begin{bmatrix}20 & -15 & 10 & -20 \\ 12 & -9 & 6 & -12 \\ 16 & -12 & 8 & -16\end{bmatrix}

* Undefined

* \begin{bmatrix}9 & 7 & 8 \\ 2 & 0 & 1 \\ 7 & 5 & 6 \\ 1 & -1 & 0\end{bmatrix}

* \begin{bmatrix}-20 & -12 & -16 \\ 15 & 9 & 12 \\ -10 & -6 & -8 \\ 20 & 12 & 16\end{bmatrix}

* correct: \begin{bmatrix}20 & 12 & 16 \\ -15 & -9 & -12 \\ 10 & 6 & 8 \\ -20 & -12 & -16\end{bmatrix}

Worked solution:

Here, the first factor is $4\times 1$ matrix and the second factor is a $1\times 3$ matrix. 

There is $1$ column in the first matrix and $1$ row in the second matrix, so the product is well defined:

$$
4\times \boxed{\text{1}}✓\boxed{\text{1}}\times 3=4\times 3
$$

Computing the product, we have

$$
\begin{aligned}\begin{bmatrix}4 \\ -3 \\ 2 \\ -4\end{bmatrix}\begin{bmatrix}5 & 3 & 4\end{bmatrix} & =\begin{bmatrix}4\cdot 5 & 4\cdot 3 & 4\cdot 4 \\ (-3)\cdot 5 & (-3)\cdot 3 & (-3)\cdot 4 \\ 2\cdot 5 & 2\cdot 3 & 2\cdot 4 \\ (-4)\cdot 5 & (-4)\cdot 3 & (-4)\cdot 4\end{bmatrix} \\  & =\begin{bmatrix}20 & 12 & 16 \\ -15 & -9 & -12 \\ 10 & 6 & 8 \\ -20 & -12 & -16\end{bmatrix}\end{aligned}
$$
