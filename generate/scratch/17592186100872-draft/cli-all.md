Level: easy; template: q-1034; profile: method-sign-omission

Find $AB$, if
$A = \begin{bmatrix}1 & 2 & -5 \\ 0 & -1 & 1\end{bmatrix}$
and
$B = \begin{bmatrix}3 & 5 \\ -1 & 3 \\ 3 & 4\end{bmatrix}$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}-10 & -21 \\ 2 & 7\end{bmatrix}$

• $\begin{bmatrix}14 & 9 \\ -4 & -1\end{bmatrix}$

• $\begin{bmatrix}-14 & 4 \\ -9 & 1\end{bmatrix}$

• $\begin{bmatrix}1 & 11 \\ 1 & -3\end{bmatrix}$

✓ $\begin{bmatrix}-14 & -9 \\ 4 & 1\end{bmatrix}$

Here, $A$ is a $2\times 3$ matrix and $B$ is a $3\times 2$ matrix. 

There are $3$ columns in $A$ and $3$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{2\times \boxed{\text{3}}}{\cdot }_{✓}{B}_{\boxed{\text{3}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}1 & 2 & -5 \\ 0 & -1 & 1\end{bmatrix}\begin{bmatrix}3 & 5 \\ -1 & 3 \\ 3 & 4\end{bmatrix}=\begin{bmatrix}-14 & ∗ \\ ∗ & ∗\end{bmatrix}, \\ & \,-14=1\cdot 3+2\cdot (-1)+(-5)\cdot 3 \\  & \begin{bmatrix}1 & 2 & -5 \\ 0 & -1 & 1\end{bmatrix}\begin{bmatrix}3 & 5 \\ -1 & 3 \\ 3 & 4\end{bmatrix}=\begin{bmatrix}-14 & -9 \\ ∗ & ∗\end{bmatrix}, \\ & \,-9=1\cdot 5+2\cdot 3+(-5)\cdot 4 \\  & \begin{bmatrix}1 & 2 & -5 \\ 0 & -1 & 1\end{bmatrix}\begin{bmatrix}3 & 5 \\ -1 & 3 \\ 3 & 4\end{bmatrix}=\begin{bmatrix}-14 & -9 \\ 4 & ∗\end{bmatrix}, \\ & \,4=0\cdot 3+(-1)\cdot (-1)+1\cdot 3 \\  & \begin{bmatrix}1 & 2 & -5 \\ 0 & -1 & 1\end{bmatrix}\begin{bmatrix}3 & 5 \\ -1 & 3 \\ 3 & 4\end{bmatrix}=\begin{bmatrix}-14 & -9 \\ 4 & 1\end{bmatrix}, \\ & \,1=0\cdot 5+(-1)\cdot 3+1\cdot 4\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}-14 & -9 \\ 4 & 1\end{bmatrix}.$

---

Level: easy; template: q-317844; profile: method-sign-omission

Determine $AB$ given that 
$A=\begin{bmatrix}2 & 1 \\ 0 & 3 \\ -3 & 2 \\ 3 & -5\end{bmatrix}$
and
$B=\begin{bmatrix}4 & -2 \\ 0 & -1\end{bmatrix}.$

| $AB=$ | {{field-1}} | $-5$ |
| --- | --- | --- |
|  | {{field-2}} | {{field-3}} |
|  | $-12$ | $4$ |
|  | {{field-4}} | {{field-5}} |

Field field-2 (:answer-field.type/blank):

✓ $0$

Field field-5 (:answer-field.type/blank):

✓ $-1$

Field field-4 (:answer-field.type/blank):

✓ $12$

Field field-1 (:answer-field.type/blank):

✓ $8$

Field field-3 (:answer-field.type/blank):

✓ $-3$

Here, $A$ is a $4\times 2$ matrix and $B$ is a $2\times 2$ matrix. 

There are $2$ columns in $A$ and $2$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{4\times \boxed{\text{2}}}{\cdot }_{✓}{B}_{\boxed{\text{2}}\times 2}={AB}_{4\times 2}
$$

Let's compute the unknown elements of $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}2 & 1 \\ 0 & 3 \\ -3 & 2 \\ 3 & -5\end{bmatrix}\begin{bmatrix}4 & -2 \\ 0 & -1\end{bmatrix}=\begin{bmatrix}8 & -5 \\ ∗ & ∗ \\ -12 & 4 \\ ∗ & ∗\end{bmatrix}, \\ & \,8=2\cdot 4+1\cdot 0 \\  & \begin{bmatrix}2 & 1 \\ 0 & 3 \\ -3 & 2 \\ 3 & -5\end{bmatrix}\begin{bmatrix}4 & -2 \\ 0 & -1\end{bmatrix}=\begin{bmatrix}8 & -5 \\ 0 & ∗ \\ -12 & 4 \\ ∗ & ∗\end{bmatrix}, \\ & \,0=0\cdot 4+3\cdot 0 \\  & \begin{bmatrix}2 & 1 \\ 0 & 3 \\ -3 & 2 \\ 3 & -5\end{bmatrix}\begin{bmatrix}4 & -2 \\ 0 & -1\end{bmatrix}=\begin{bmatrix}8 & -5 \\ 0 & -3 \\ -12 & 4 \\ ∗ & ∗\end{bmatrix}, \\ & \,-3=0\cdot (-2)+3\cdot (-1) \\  & \begin{bmatrix}2 & 1 \\ 0 & 3 \\ -3 & 2 \\ 3 & -5\end{bmatrix}\begin{bmatrix}4 & -2 \\ 0 & -1\end{bmatrix}=\begin{bmatrix}8 & -5 \\ 0 & -3 \\ -12 & 4 \\ 12 & ∗\end{bmatrix}, \\ & \,12=3\cdot 4+(-5)\cdot 0 \\  & \begin{bmatrix}2 & 1 \\ 0 & 3 \\ -3 & 2 \\ 3 & -5\end{bmatrix}\begin{bmatrix}4 & -2 \\ 0 & -1\end{bmatrix}=\begin{bmatrix}8 & -5 \\ 0 & -3 \\ -12 & 4 \\ 12 & -1\end{bmatrix}, \\ & \,-1=3\cdot (-2)+(-5)\cdot (-1)\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}8 & -5 \\ 0 & -3 \\ -12 & 4 \\ 12 & -1\end{bmatrix}.$

---

Level: moderate; template: authored-moderate; profile: method-sign-omission

Find $AB$, if
$A=\begin{bmatrix}-2 & 1 & -1 \\ 1 & -1 & -1\end{bmatrix}$
and 
$B=\begin{bmatrix}-4 & 3 \\ -5 & -1 \\ 5 & -2\end{bmatrix}$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}8 & -3 \\ -14 & 4\end{bmatrix}$

• $\begin{bmatrix}2 & 5 \\ 4 & -6\end{bmatrix}$

• $\begin{bmatrix}-2 & -4 \\ -5 & 6\end{bmatrix}$

• $\begin{bmatrix}3 & -7 \\ 1 & 4\end{bmatrix}$

✓ $\begin{bmatrix}-2 & -5 \\ -4 & 6\end{bmatrix}$

Here, $A$ is a $2\times 3$ matrix and $B$ is a $3\times 2$ matrix. 

There are $3$ columns in $A$ and $3$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{2\times \boxed{\text{3}}}{\cdot }_{✓}{B}_{\boxed{\text{3}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}-2 & 1 & -1 \\ 1 & -1 & -1\end{bmatrix}\begin{bmatrix}-4 & 3 \\ -5 & -1 \\ 5 & -2\end{bmatrix}=\begin{bmatrix}-2 & ∗ \\ ∗ & ∗\end{bmatrix}, \\ & \,-2=(-2)\cdot (-4)+1\cdot (-5)+(-1)\cdot 5 \\  & \begin{bmatrix}-2 & 1 & -1 \\ 1 & -1 & -1\end{bmatrix}\begin{bmatrix}-4 & 3 \\ -5 & -1 \\ 5 & -2\end{bmatrix}=\begin{bmatrix}-2 & -5 \\ ∗ & ∗\end{bmatrix}, \\ & \,-5=(-2)\cdot 3+1\cdot (-1)+(-1)\cdot (-2) \\  & \begin{bmatrix}-2 & 1 & -1 \\ 1 & -1 & -1\end{bmatrix}\begin{bmatrix}-4 & 3 \\ -5 & -1 \\ 5 & -2\end{bmatrix}=\begin{bmatrix}-2 & -5 \\ -4 & ∗\end{bmatrix}, \\ & \,-4=1\cdot (-4)+(-1)\cdot (-5)+(-1)\cdot 5 \\  & \begin{bmatrix}-2 & 1 & -1 \\ 1 & -1 & -1\end{bmatrix}\begin{bmatrix}-4 & 3 \\ -5 & -1 \\ 5 & -2\end{bmatrix}=\begin{bmatrix}-2 & -5 \\ -4 & 6\end{bmatrix}, \\ & \,6=1\cdot 3+(-1)\cdot (-1)+(-1)\cdot (-2)\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}-2 & -5 \\ -4 & 6\end{bmatrix}.$

---

Level: moderate; template: authored-moderate; profile: method-sign-omission

Find $AB$, if
$A=\begin{bmatrix}2 & -2 & -1 \\ 1 & -2 & -1\end{bmatrix}$
and 
$B=\begin{bmatrix}-1 & 1 \\ 3 & -2 \\ 1 & -5\end{bmatrix}$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}9 & -11 \\ 8 & -10\end{bmatrix}$

✓ $\begin{bmatrix}-9 & 11 \\ -8 & 10\end{bmatrix}$

• $\begin{bmatrix}3 & 3 \\ 4 & 2\end{bmatrix}$

• $\begin{bmatrix}-8 & 6 \\ -7 & 5\end{bmatrix}$

• $\begin{bmatrix}-9 & -8 \\ 11 & 10\end{bmatrix}$

Here, $A$ is a $2\times 3$ matrix and $B$ is a $3\times 2$ matrix. 

There are $3$ columns in $A$ and $3$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{2\times \boxed{\text{3}}}{\cdot }_{✓}{B}_{\boxed{\text{3}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}2 & -2 & -1 \\ 1 & -2 & -1\end{bmatrix}\begin{bmatrix}-1 & 1 \\ 3 & -2 \\ 1 & -5\end{bmatrix}=\begin{bmatrix}-9 & ∗ \\ ∗ & ∗\end{bmatrix}, \\ & \,-9=2\cdot (-1)+(-2)\cdot 3+(-1)\cdot 1 \\  & \begin{bmatrix}2 & -2 & -1 \\ 1 & -2 & -1\end{bmatrix}\begin{bmatrix}-1 & 1 \\ 3 & -2 \\ 1 & -5\end{bmatrix}=\begin{bmatrix}-9 & 11 \\ ∗ & ∗\end{bmatrix}, \\ & \,11=2\cdot 1+(-2)\cdot (-2)+(-1)\cdot (-5) \\  & \begin{bmatrix}2 & -2 & -1 \\ 1 & -2 & -1\end{bmatrix}\begin{bmatrix}-1 & 1 \\ 3 & -2 \\ 1 & -5\end{bmatrix}=\begin{bmatrix}-9 & 11 \\ -8 & ∗\end{bmatrix}, \\ & \,-8=1\cdot (-1)+(-2)\cdot 3+(-1)\cdot 1 \\  & \begin{bmatrix}2 & -2 & -1 \\ 1 & -2 & -1\end{bmatrix}\begin{bmatrix}-1 & 1 \\ 3 & -2 \\ 1 & -5\end{bmatrix}=\begin{bmatrix}-9 & 11 \\ -8 & 10\end{bmatrix}, \\ & \,10=1\cdot 1+(-2)\cdot (-2)+(-1)\cdot (-5)\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}-9 & 11 \\ -8 & 10\end{bmatrix}.$

---

Level: hard; template: authored-hard; profile: method-sign-omission

If
$E=\begin{bmatrix}-1 & 2 & -4 & 4 \\ -2 & 1 & 3 & -3\end{bmatrix}$
and
$F=\begin{bmatrix}2 & 1 \\ -2 & -3 \\ 1 & -2 \\ -1 & 1\end{bmatrix}$
then $EF=$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}2 & 9 \\ -2 & -2\end{bmatrix}$

• $\begin{bmatrix}14 & -5 \\ 0 & 14\end{bmatrix}$

• $\begin{bmatrix}-14 & 0 \\ 5 & -14\end{bmatrix}$

• $\begin{bmatrix}-10 & 1 \\ -3 & -11\end{bmatrix}$

✓ $\begin{bmatrix}-14 & 5 \\ 0 & -14\end{bmatrix}$

Here, $E$ is a $2\times 4$ matrix and $F$ is a $4\times 2$ matrix. 

There are $4$ columns in $E$ and $4$ rows in $F,$ so $E$ and $F$ are conformable for multiplication:

$$
{E}_{2\times \boxed{\text{4}}}{\cdot }_{✓}{F}_{\boxed{\text{4}}\times 2}={EF}_{2\times 2}
$$

Let's compute $EF,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}-1 & 2 & -4 & 4 \\ -2 & 1 & 3 & -3\end{bmatrix}\begin{bmatrix}2 & 1 \\ -2 & -3 \\ 1 & -2 \\ -1 & 1\end{bmatrix}=\begin{bmatrix}-14 & ∗ \\ ∗ & ∗\end{bmatrix}, \\ & \,-14=(-1)\cdot 2+2\cdot (-2)+(-4)\cdot 1+4\cdot (-1) \\  & \begin{bmatrix}-1 & 2 & -4 & 4 \\ -2 & 1 & 3 & -3\end{bmatrix}\begin{bmatrix}2 & 1 \\ -2 & -3 \\ 1 & -2 \\ -1 & 1\end{bmatrix}=\begin{bmatrix}-14 & 5 \\ ∗ & ∗\end{bmatrix}, \\ & \,5=(-1)\cdot 1+2\cdot (-3)+(-4)\cdot (-2)+4\cdot 1 \\  & \begin{bmatrix}-1 & 2 & -4 & 4 \\ -2 & 1 & 3 & -3\end{bmatrix}\begin{bmatrix}2 & 1 \\ -2 & -3 \\ 1 & -2 \\ -1 & 1\end{bmatrix}=\begin{bmatrix}-14 & 5 \\ 0 & ∗\end{bmatrix}, \\ & \,0=(-2)\cdot 2+1\cdot (-2)+3\cdot 1+(-3)\cdot (-1) \\  & \begin{bmatrix}-1 & 2 & -4 & 4 \\ -2 & 1 & 3 & -3\end{bmatrix}\begin{bmatrix}2 & 1 \\ -2 & -3 \\ 1 & -2 \\ -1 & 1\end{bmatrix}=\begin{bmatrix}-14 & 5 \\ 0 & -14\end{bmatrix}, \\ & \,-14=(-2)\cdot 1+1\cdot (-3)+3\cdot (-2)+(-3)\cdot 1\end{aligned}
$$

Therefore, 
$EF=\begin{bmatrix}-14 & 5 \\ 0 & -14\end{bmatrix}.$

---

Level: hard; template: authored-hard; profile: method-sign-omission

If
$E=\begin{bmatrix}2 & -2 & -1 & 1 \\ -2 & -1 & -1 & 1\end{bmatrix}$
and
$F=\begin{bmatrix}3 & -2 \\ 1 & -5 \\ 5 & -2 \\ 2 & 2\end{bmatrix}$
then $EF=$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}-1 & -10 \\ 10 & -13\end{bmatrix}$

✓ $\begin{bmatrix}1 & 10 \\ -10 & 13\end{bmatrix}$

• $\begin{bmatrix}1 & -14 \\ -12 & -1\end{bmatrix}$

• $\begin{bmatrix}-1 & 8 \\ -12 & 11\end{bmatrix}$

• $\begin{bmatrix}1 & -10 \\ 10 & 13\end{bmatrix}$

Here, $E$ is a $2\times 4$ matrix and $F$ is a $4\times 2$ matrix. 

There are $4$ columns in $E$ and $4$ rows in $F,$ so $E$ and $F$ are conformable for multiplication:

$$
{E}_{2\times \boxed{\text{4}}}{\cdot }_{✓}{F}_{\boxed{\text{4}}\times 2}={EF}_{2\times 2}
$$

Let's compute $EF,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}2 & -2 & -1 & 1 \\ -2 & -1 & -1 & 1\end{bmatrix}\begin{bmatrix}3 & -2 \\ 1 & -5 \\ 5 & -2 \\ 2 & 2\end{bmatrix}=\begin{bmatrix}1 & ∗ \\ ∗ & ∗\end{bmatrix}, \\ & \,1=2\cdot 3+(-2)\cdot 1+(-1)\cdot 5+1\cdot 2 \\  & \begin{bmatrix}2 & -2 & -1 & 1 \\ -2 & -1 & -1 & 1\end{bmatrix}\begin{bmatrix}3 & -2 \\ 1 & -5 \\ 5 & -2 \\ 2 & 2\end{bmatrix}=\begin{bmatrix}1 & 10 \\ ∗ & ∗\end{bmatrix}, \\ & \,10=2\cdot (-2)+(-2)\cdot (-5)+(-1)\cdot (-2)+1\cdot 2 \\  & \begin{bmatrix}2 & -2 & -1 & 1 \\ -2 & -1 & -1 & 1\end{bmatrix}\begin{bmatrix}3 & -2 \\ 1 & -5 \\ 5 & -2 \\ 2 & 2\end{bmatrix}=\begin{bmatrix}1 & 10 \\ -10 & ∗\end{bmatrix}, \\ & \,-10=(-2)\cdot 3+(-1)\cdot 1+(-1)\cdot 5+1\cdot 2 \\  & \begin{bmatrix}2 & -2 & -1 & 1 \\ -2 & -1 & -1 & 1\end{bmatrix}\begin{bmatrix}3 & -2 \\ 1 & -5 \\ 5 & -2 \\ 2 & 2\end{bmatrix}=\begin{bmatrix}1 & 10 \\ -10 & 13\end{bmatrix}, \\ & \,13=(-2)\cdot (-2)+(-1)\cdot (-5)+(-1)\cdot (-2)+1\cdot 2\end{aligned}
$$

Therefore, 
$EF=\begin{bmatrix}1 & 10 \\ -10 & 13\end{bmatrix}.$
