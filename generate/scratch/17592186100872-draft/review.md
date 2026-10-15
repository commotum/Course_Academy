### original evidence raw

Level: easy; template: q-1029; profile: observed-raw

If
$X = \begin{bmatrix}1 & 3 \\ 0 & -1\end{bmatrix}$
and
$Y = \begin{bmatrix}3 & 1 & 2 \\ -1 & 0 & 4\end{bmatrix}$
then $XY =$

Field selection (:answer-field.type/radio): [source correct designation absent]

• $\begin{bmatrix}1 & 0 & 14 \\ 14 & -4 & 4\end{bmatrix}$

• $\begin{bmatrix}0 & 1 & 14 \\ 1 & 0 & -4\end{bmatrix}$

• $\begin{bmatrix}0 & 1 \\ 1 & 0 \\ 14 & -4\end{bmatrix}$

• $\begin{bmatrix}14 & 0 & 0 \\ 14 & 2 & -1\end{bmatrix}$

• $\begin{bmatrix}14 & 14 \\ 0 & 2 \\ 0 & -1\end{bmatrix}$

[Source worked solution absent]

---

### generated variant

Level: easy; template: q-1029; profile: method-sign-omission

If
$X = \begin{bmatrix}-1 & 2 \\ 0 & 4\end{bmatrix}$
and
$Y = \begin{bmatrix}-3 & 1 & -1 \\ -2 & 0 & -3\end{bmatrix}$
then $XY =$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}-1 & -8 \\ -1 & 0 \\ -5 & -12\end{bmatrix}$

✓ $\begin{bmatrix}-1 & -1 & -5 \\ -8 & 0 & -12\end{bmatrix}$

• $\begin{bmatrix}7 & -1 & 7 \\ 8 & 0 & 12\end{bmatrix}$

• $\begin{bmatrix}1 & 1 & 5 \\ 8 & 0 & 12\end{bmatrix}$

• $\begin{bmatrix}3 & -1 & 1 \\ 0 & 0 & 0\end{bmatrix}$

Here, $X$ is a $2\times 2$ matrix and $Y$ is a $2\times 3$ matrix. 

There are $2$ columns in $X$ and $2$ rows in $Y,$ so $X$ and $Y$ are conformable for multiplication:

$$
{X}_{2\times \boxed{\text{2}}}{\cdot }_{✓}{Y}_{\boxed{\text{2}}\times 3}={XY}_{2\times 3}
$$

Let's compute $XY,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}-1 & 2 \\ 0 & 4\end{bmatrix}\begin{bmatrix}-3 & 1 & -1 \\ -2 & 0 & -3\end{bmatrix}=\begin{bmatrix}-1 & ∗ & ∗ \\ ∗ & ∗ & ∗\end{bmatrix}, \\ & \,-1=(-1)\cdot (-3)+2\cdot (-2) \\  & \begin{bmatrix}-1 & 2 \\ 0 & 4\end{bmatrix}\begin{bmatrix}-3 & 1 & -1 \\ -2 & 0 & -3\end{bmatrix}=\begin{bmatrix}-1 & -1 & ∗ \\ ∗ & ∗ & ∗\end{bmatrix}, \\ & \,-1=(-1)\cdot 1+2\cdot 0 \\  & \begin{bmatrix}-1 & 2 \\ 0 & 4\end{bmatrix}\begin{bmatrix}-3 & 1 & -1 \\ -2 & 0 & -3\end{bmatrix}=\begin{bmatrix}-1 & -1 & -5 \\ ∗ & ∗ & ∗\end{bmatrix}, \\ & \,-5=(-1)\cdot (-1)+2\cdot (-3) \\  & \begin{bmatrix}-1 & 2 \\ 0 & 4\end{bmatrix}\begin{bmatrix}-3 & 1 & -1 \\ -2 & 0 & -3\end{bmatrix}=\begin{bmatrix}-1 & -1 & -5 \\ -8 & ∗ & ∗\end{bmatrix}, \\ & \,-8=0\cdot (-3)+4\cdot (-2) \\  & \begin{bmatrix}-1 & 2 \\ 0 & 4\end{bmatrix}\begin{bmatrix}-3 & 1 & -1 \\ -2 & 0 & -3\end{bmatrix}=\begin{bmatrix}-1 & -1 & -5 \\ -8 & 0 & ∗\end{bmatrix}, \\ & \,0=0\cdot 1+4\cdot 0 \\  & \begin{bmatrix}-1 & 2 \\ 0 & 4\end{bmatrix}\begin{bmatrix}-3 & 1 & -1 \\ -2 & 0 & -3\end{bmatrix}=\begin{bmatrix}-1 & -1 & -5 \\ -8 & 0 & -12\end{bmatrix}, \\ & \,-12=0\cdot (-1)+4\cdot (-3)\end{aligned}
$$

Therefore, 
$XY=\begin{bmatrix}-1 & -1 & -5 \\ -8 & 0 & -12\end{bmatrix}.$

---

### original evidence raw

Level: easy; template: q-1034; profile: observed-raw

Find $AB$, if
$A = \begin{bmatrix}5 & 1 & 3 \\ 0 & 1 & -2\end{bmatrix}$
and
$B = \begin{bmatrix}6 & 5 \\ 9 & 8 \\ 3 & 7\end{bmatrix}$

Field selection (:answer-field.type/radio): [source correct designation absent]

• $\begin{bmatrix}48 & 54 \\ 3 & -6\end{bmatrix}$

• $\begin{bmatrix}48 & 3 \\ 54 & -6\end{bmatrix}$

• $\begin{bmatrix}12 & 4 \\ 3 & -3\end{bmatrix}$

• $\begin{bmatrix}48 & 5 \\ 3 & 4\end{bmatrix}$

• $\begin{bmatrix}5 & 54 \\ -3 & 6\end{bmatrix}$

[Source worked solution absent]

---

### generated variant

Level: easy; template: q-1034; profile: method-sign-omission

Find $AB$, if
$A = \begin{bmatrix}5 & -2 & 4 \\ 0 & 1 & 3\end{bmatrix}$
and
$B = \begin{bmatrix}-5 & 4 \\ -2 & 5 \\ -2 & -1\end{bmatrix}$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}-29 & -8 \\ 6 & 2\end{bmatrix}$

✓ $\begin{bmatrix}-29 & 6 \\ -8 & 2\end{bmatrix}$

• $\begin{bmatrix}-37 & 26 \\ -4 & -8\end{bmatrix}$

• $\begin{bmatrix}29 & -6 \\ 8 & -2\end{bmatrix}$

• $\begin{bmatrix}-21 & 10 \\ -2 & 5\end{bmatrix}$

Here, $A$ is a $2\times 3$ matrix and $B$ is a $3\times 2$ matrix. 

There are $3$ columns in $A$ and $3$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{2\times \boxed{\text{3}}}{\cdot }_{✓}{B}_{\boxed{\text{3}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}5 & -2 & 4 \\ 0 & 1 & 3\end{bmatrix}\begin{bmatrix}-5 & 4 \\ -2 & 5 \\ -2 & -1\end{bmatrix}=\begin{bmatrix}-29 & ∗ \\ ∗ & ∗\end{bmatrix}, \\ & \,-29=5\cdot (-5)+(-2)\cdot (-2)+4\cdot (-2) \\  & \begin{bmatrix}5 & -2 & 4 \\ 0 & 1 & 3\end{bmatrix}\begin{bmatrix}-5 & 4 \\ -2 & 5 \\ -2 & -1\end{bmatrix}=\begin{bmatrix}-29 & 6 \\ ∗ & ∗\end{bmatrix}, \\ & \,6=5\cdot 4+(-2)\cdot 5+4\cdot (-1) \\  & \begin{bmatrix}5 & -2 & 4 \\ 0 & 1 & 3\end{bmatrix}\begin{bmatrix}-5 & 4 \\ -2 & 5 \\ -2 & -1\end{bmatrix}=\begin{bmatrix}-29 & 6 \\ -8 & ∗\end{bmatrix}, \\ & \,-8=0\cdot (-5)+1\cdot (-2)+3\cdot (-2) \\  & \begin{bmatrix}5 & -2 & 4 \\ 0 & 1 & 3\end{bmatrix}\begin{bmatrix}-5 & 4 \\ -2 & 5 \\ -2 & -1\end{bmatrix}=\begin{bmatrix}-29 & 6 \\ -8 & 2\end{bmatrix}, \\ & \,2=0\cdot 4+1\cdot 5+3\cdot (-1)\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}-29 & 6 \\ -8 & 2\end{bmatrix}.$

---

### original evidence raw

Level: easy; template: q-1033; profile: observed-raw

If
$E=\begin{bmatrix}1 & -2 & 4 & 5 \\ 3 & -1 & 0 & 1\end{bmatrix}$
and
$F=\begin{bmatrix}4 & 2 \\ -3 & -1 \\ -2 & 1 \\ 0 & 2\end{bmatrix}$
then $EF=$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}18 & -2 \\ 9 & 15\end{bmatrix}$

✓ $\begin{bmatrix}2 & 18 \\ 15 & 9\end{bmatrix}$

• $\begin{bmatrix}18 & -2 \\ -15 & 9\end{bmatrix}$

• $\begin{bmatrix}18 & -2 \\ 15 & 9\end{bmatrix}$

• $\begin{bmatrix}2 & 9 \\ -15 & 18\end{bmatrix}$

Here, $E$ is a $2\times 4$ matrix and $F$ is a $4\times 2$ matrix. 

There are $4$ columns in $E$ and $4$ rows in $F,$ so $E$ and $F$ are conformable for multiplication:

$$
{E}_{2\times \boxed{\text{4}}}{\cdot }_{✓}{F}_{\boxed{\text{4}}\times 2}={EF}_{2\times 2}
$$

Let's compute $EF,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}1 & -2 & 4 & 5 \\ 3 & -1 & 0 & 1\end{bmatrix}\begin{bmatrix}4 & 2 \\ -3 & -1 \\ -2 & 1 \\ 0 & 2\end{bmatrix}=\begin{bmatrix}2 & ∗ \\ ∗ & ∗\end{bmatrix}, &  & \,2=1\cdot 4+(-2)\cdot (-3)+4\cdot (-2)+5\cdot 0 \\  & \begin{bmatrix}1 & -2 & 4 & 5 \\ 3 & -1 & 0 & 1\end{bmatrix}\begin{bmatrix}4 & 2 \\ -3 & -1 \\ -2 & 1 \\ 0 & 2\end{bmatrix}=\begin{bmatrix}2 & 18 \\ ∗ & ∗\end{bmatrix}, &  & \,18=1\cdot 2+(-2)\cdot (-1)+4\cdot 1+5\cdot 2 \\  & \begin{bmatrix}1 & -2 & 4 & 5 \\ 3 & -1 & 0 & 1\end{bmatrix}\begin{bmatrix}4 & 2 \\ -3 & -1 \\ -2 & 1 \\ 0 & 2\end{bmatrix}=\begin{bmatrix}2 & 18 \\ 15 & ∗\end{bmatrix}, &  & \,15=3\cdot 4+(-1)\cdot (-3)+0\cdot (-2)+1\cdot 0 \\  & \begin{bmatrix}1 & -2 & 4 & 5 \\ 3 & -1 & 0 & 1\end{bmatrix}\begin{bmatrix}4 & 2 \\ -3 & -1 \\ -2 & 1 \\ 0 & 2\end{bmatrix}=\begin{bmatrix}2 & 18 \\ 15 & 9\end{bmatrix}, &  & \,9=3\cdot 2+(-1)\cdot (-1)+0\cdot 1+1\cdot 2\end{aligned}
$$

Therefore, 
$EF=\begin{bmatrix}2 & 18 \\ 15 & 9\end{bmatrix}.$

---

### generated variant

Level: easy; template: q-1033; profile: method-sign-omission

If
$E=\begin{bmatrix}1 & -1 & -1 & -1 \\ -2 & 2 & 0 & -2\end{bmatrix}$
and
$F=\begin{bmatrix}3 & -1 \\ -5 & -2 \\ -5 & 5 \\ 0 & 1\end{bmatrix}$
then $EF=$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}13 & -16 \\ -5 & -4\end{bmatrix}$

✓ $\begin{bmatrix}13 & -5 \\ -16 & -4\end{bmatrix}$

• $\begin{bmatrix}3 & -7 \\ 4 & 8\end{bmatrix}$

• $\begin{bmatrix}-13 & 5 \\ 16 & 4\end{bmatrix}$

• $\begin{bmatrix}13 & -4 \\ -16 & -2\end{bmatrix}$

Here, $E$ is a $2\times 4$ matrix and $F$ is a $4\times 2$ matrix. 

There are $4$ columns in $E$ and $4$ rows in $F,$ so $E$ and $F$ are conformable for multiplication:

$$
{E}_{2\times \boxed{\text{4}}}{\cdot }_{✓}{F}_{\boxed{\text{4}}\times 2}={EF}_{2\times 2}
$$

Let's compute $EF,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}1 & -1 & -1 & -1 \\ -2 & 2 & 0 & -2\end{bmatrix}\begin{bmatrix}3 & -1 \\ -5 & -2 \\ -5 & 5 \\ 0 & 1\end{bmatrix}=\begin{bmatrix}13 & ∗ \\ ∗ & ∗\end{bmatrix}, \\ & \,13=1\cdot 3+(-1)\cdot (-5)+(-1)\cdot (-5)+(-1)\cdot 0 \\  & \begin{bmatrix}1 & -1 & -1 & -1 \\ -2 & 2 & 0 & -2\end{bmatrix}\begin{bmatrix}3 & -1 \\ -5 & -2 \\ -5 & 5 \\ 0 & 1\end{bmatrix}=\begin{bmatrix}13 & -5 \\ ∗ & ∗\end{bmatrix}, \\ & \,-5=1\cdot (-1)+(-1)\cdot (-2)+(-1)\cdot 5+(-1)\cdot 1 \\  & \begin{bmatrix}1 & -1 & -1 & -1 \\ -2 & 2 & 0 & -2\end{bmatrix}\begin{bmatrix}3 & -1 \\ -5 & -2 \\ -5 & 5 \\ 0 & 1\end{bmatrix}=\begin{bmatrix}13 & -5 \\ -16 & ∗\end{bmatrix}, \\ & \,-16=(-2)\cdot 3+2\cdot (-5)+0\cdot (-5)+(-2)\cdot 0 \\  & \begin{bmatrix}1 & -1 & -1 & -1 \\ -2 & 2 & 0 & -2\end{bmatrix}\begin{bmatrix}3 & -1 \\ -5 & -2 \\ -5 & 5 \\ 0 & 1\end{bmatrix}=\begin{bmatrix}13 & -5 \\ -16 & -4\end{bmatrix}, \\ & \,-4=(-2)\cdot (-1)+2\cdot (-2)+0\cdot 5+(-2)\cdot 1\end{aligned}
$$

Therefore, 
$EF=\begin{bmatrix}13 & -5 \\ -16 & -4\end{bmatrix}.$

---

### original evidence raw

Level: easy; template: q-1035; profile: observed-raw

Find $ST$,  if  $S=\begin{bmatrix}2 & -3 & 1 & 4\end{bmatrix}$ and $T=\begin{bmatrix}1 & -2 \\ 0 & 4 \\ -2 & 1 \\ 6 & 4\end{bmatrix}.$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}12 & -24\end{bmatrix}$

✓ $\begin{bmatrix}24 & 1\end{bmatrix}$

• $\begin{bmatrix}20 \\ 4\end{bmatrix}$

• $\begin{bmatrix}-20 \\ -4\end{bmatrix}$

• $\begin{bmatrix}20 & 24 \\ 4 & 1\end{bmatrix}$

Here, $S$ is a $1\times 4$ matrix and $T$ is a $4\times 2$ matrix. 

There are $4$ columns in $S$ and $4$ rows in $T,$ so $S$ and $T$ are conformable for multiplication:

$$
{S}_{1\times \boxed{\text{4}}}{\cdot }_{✓}{T}_{\boxed{\text{4}}\times 2}={ST}_{1\times 2}
$$

Let's compute $ST,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}2 & -3 & 1 & 4\end{bmatrix}\begin{bmatrix}1 & -2 \\ 0 & 4 \\ -2 & 1 \\ 6 & 4\end{bmatrix}=\begin{bmatrix}24 & ∗\end{bmatrix}, &  & \,24=2\cdot 1+(-3)\cdot 0+1\cdot (-2)+4\cdot 6 \\  & \begin{bmatrix}2 & -3 & 1 & 4\end{bmatrix}\begin{bmatrix}1 & -2 \\ 0 & 4 \\ -2 & 1 \\ 6 & 4\end{bmatrix}=\begin{bmatrix}24 & 1\end{bmatrix}, &  & \,1=2\cdot (-2)+(-3)\cdot 4+1\cdot 1+4\cdot 4\end{aligned}
$$

Therefore, 
$ST=\begin{bmatrix}24 & 1\end{bmatrix}.$

---

### generated variant

Level: easy; template: q-1035; profile: method-sign-omission

Find $ST$,  if  $S=\begin{bmatrix}3 & -2 & 1 & 3\end{bmatrix}$ and $T=\begin{bmatrix}-4 & -1 \\ 0 & -2 \\ -3 & -4 \\ 3 & 4\end{bmatrix}.$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}-6 \\ 9\end{bmatrix}$

✓ $\begin{bmatrix}-6 & 9\end{bmatrix}$

• $\begin{bmatrix}-24 & -23\end{bmatrix}$

• $\begin{bmatrix}6 & -9\end{bmatrix}$

• $\begin{bmatrix}-15 & -3\end{bmatrix}$

Here, $S$ is a $1\times 4$ matrix and $T$ is a $4\times 2$ matrix. 

There are $4$ columns in $S$ and $4$ rows in $T,$ so $S$ and $T$ are conformable for multiplication:

$$
{S}_{1\times \boxed{\text{4}}}{\cdot }_{✓}{T}_{\boxed{\text{4}}\times 2}={ST}_{1\times 2}
$$

Let's compute $ST,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}3 & -2 & 1 & 3\end{bmatrix}\begin{bmatrix}-4 & -1 \\ 0 & -2 \\ -3 & -4 \\ 3 & 4\end{bmatrix}=\begin{bmatrix}-6 & ∗\end{bmatrix}, \\ & \,-6=3\cdot (-4)+(-2)\cdot 0+1\cdot (-3)+3\cdot 3 \\  & \begin{bmatrix}3 & -2 & 1 & 3\end{bmatrix}\begin{bmatrix}-4 & -1 \\ 0 & -2 \\ -3 & -4 \\ 3 & 4\end{bmatrix}=\begin{bmatrix}-6 & 9\end{bmatrix}, \\ & \,9=3\cdot (-1)+(-2)\cdot (-2)+1\cdot (-4)+3\cdot 4\end{aligned}
$$

Therefore, 
$ST=\begin{bmatrix}-6 & 9\end{bmatrix}.$

---

### original evidence raw

Level: easy; template: q-129495; profile: observed-raw

Find $AB$, if
$A=\begin{bmatrix}2 & -1 & 1 \\ 1 & 0 & 2\end{bmatrix}$
and 
$B=\begin{bmatrix}-3 & 2 \\ 6 & 5 \\ -3 & 4\end{bmatrix}$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}-9 & 10 \\ -5 & 3\end{bmatrix}$

• $\begin{bmatrix}-15 & 10 \\ -2 & -3\end{bmatrix}$

• $\begin{bmatrix}-5 & 6 \\ -3 & 10\end{bmatrix}$

• $\begin{bmatrix}3 & 10 \\ -6 & 5\end{bmatrix}$

✓ $\begin{bmatrix}-15 & 3 \\ -9 & 10\end{bmatrix}$

Here, $A$ is a $2\times 3$ matrix and $B$ is a $3\times 2$ matrix. 

There are $3$ columns in $A$ and $3$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{2\times \boxed{\text{3}}}{\cdot }_{✓}{B}_{\boxed{\text{3}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}2 & -1 & 1 \\ 1 & 0 & 2\end{bmatrix}\begin{bmatrix}-3 & 2 \\ 6 & 5 \\ -3 & 4\end{bmatrix}=\begin{bmatrix}-15 & ∗ \\ ∗ & ∗\end{bmatrix}, &  & \,-15=2\cdot (-3)+(-1)\cdot 6+1\cdot (-3) \\  & \begin{bmatrix}2 & -1 & 1 \\ 1 & 0 & 2\end{bmatrix}\begin{bmatrix}-3 & 2 \\ 6 & 5 \\ -3 & 4\end{bmatrix}=\begin{bmatrix}-15 & 3 \\ ∗ & ∗\end{bmatrix}, &  & \,3=2\cdot 2+(-1)\cdot 5+1\cdot 4 \\  & \begin{bmatrix}2 & -1 & 1 \\ 1 & 0 & 2\end{bmatrix}\begin{bmatrix}-3 & 2 \\ 6 & 5 \\ -3 & 4\end{bmatrix}=\begin{bmatrix}-15 & 3 \\ -9 & ∗\end{bmatrix}, &  & \,-9=1\cdot (-3)+0\cdot 6+2\cdot (-3) \\  & \begin{bmatrix}-2 & 1 & 1 \\ 1 & 0 & 2\end{bmatrix}\begin{bmatrix}-3 & 2 \\ 6 & 5 \\ -3 & 4\end{bmatrix}=\begin{bmatrix}-15 & 3 \\ -9 & 10\end{bmatrix}, &  & \,10=1\cdot 2+0\cdot 5+2\cdot 4\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}-15 & 3 \\ -9 & 10\end{bmatrix}.$

---

### generated variant

Level: easy; template: q-129495; profile: method-sign-omission

Find $AB$, if
$A=\begin{bmatrix}1 & 1 & 2 \\ 1 & 0 & -2\end{bmatrix}$
and 
$B=\begin{bmatrix}5 & -1 \\ -1 & -1 \\ 4 & 2\end{bmatrix}$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}12 & -3 \\ 2 & -5\end{bmatrix}$

✓ $\begin{bmatrix}12 & 2 \\ -3 & -5\end{bmatrix}$

• $\begin{bmatrix}14 & 4 \\ -3 & -5\end{bmatrix}$

• $\begin{bmatrix}-12 & -2 \\ 3 & 5\end{bmatrix}$

• $\begin{bmatrix}4 & -2 \\ 5 & -1\end{bmatrix}$

Here, $A$ is a $2\times 3$ matrix and $B$ is a $3\times 2$ matrix. 

There are $3$ columns in $A$ and $3$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{2\times \boxed{\text{3}}}{\cdot }_{✓}{B}_{\boxed{\text{3}}\times 2}={AB}_{2\times 2}
$$

Let's compute $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}1 & 1 & 2 \\ 1 & 0 & -2\end{bmatrix}\begin{bmatrix}5 & -1 \\ -1 & -1 \\ 4 & 2\end{bmatrix}=\begin{bmatrix}12 & ∗ \\ ∗ & ∗\end{bmatrix}, \\ & \,12=1\cdot 5+1\cdot (-1)+2\cdot 4 \\  & \begin{bmatrix}1 & 1 & 2 \\ 1 & 0 & -2\end{bmatrix}\begin{bmatrix}5 & -1 \\ -1 & -1 \\ 4 & 2\end{bmatrix}=\begin{bmatrix}12 & 2 \\ ∗ & ∗\end{bmatrix}, \\ & \,2=1\cdot (-1)+1\cdot (-1)+2\cdot 2 \\  & \begin{bmatrix}1 & 1 & 2 \\ 1 & 0 & -2\end{bmatrix}\begin{bmatrix}5 & -1 \\ -1 & -1 \\ 4 & 2\end{bmatrix}=\begin{bmatrix}12 & 2 \\ -3 & ∗\end{bmatrix}, \\ & \,-3=1\cdot 5+0\cdot (-1)+(-2)\cdot 4 \\  & \begin{bmatrix}1 & 1 & 2 \\ 1 & 0 & -2\end{bmatrix}\begin{bmatrix}5 & -1 \\ -1 & -1 \\ 4 & 2\end{bmatrix}=\begin{bmatrix}12 & 2 \\ -3 & -5\end{bmatrix}, \\ & \,-5=1\cdot (-1)+0\cdot (-1)+(-2)\cdot 2\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}12 & 2 \\ -3 & -5\end{bmatrix}.$

---

### original evidence raw

Level: easy; template: q-129496; profile: observed-raw

Find $XY$,  if  $X=\begin{bmatrix}5 & -2 & 4\end{bmatrix}$ and $Y=\begin{bmatrix}2 & 3 \\ -2 & 1 \\ 2 & -1\end{bmatrix}.$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}15 & 9\end{bmatrix}$

• $\begin{bmatrix}12 & 6\end{bmatrix}$

✓ $\begin{bmatrix}22 & 9\end{bmatrix}$

• $\begin{bmatrix}10 \\ -4 \\ 8\end{bmatrix}$

• $\begin{bmatrix}-6 & 12\end{bmatrix}$

Here, $X$ is a $1\times 3$ matrix and $Y$ is a $3\times 2$ matrix. 

There are $3$ columns in $X$ and $3$ rows in $Y,$ so $X$ and $Y$ are conformable for multiplication:

$$
{X}_{1\times \boxed{\text{3}}}{\cdot }_{✓}{Y}_{\boxed{\text{3}}\times 2}={XY}_{1\times 2}
$$

Let's compute $XY,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}5 & -2 & 4\end{bmatrix}\begin{bmatrix}2 & 3 \\ -2 & 1 \\ 2 & -1\end{bmatrix}=\begin{bmatrix}22 & ∗\end{bmatrix}, &  & \,22=5\cdot 2+(-2)\cdot (-2)+4\cdot 2 \\  & \begin{bmatrix}5 & -2 & 4\end{bmatrix}\begin{bmatrix}2 & 3 \\ -2 & 1 \\ 2 & -1\end{bmatrix}=\begin{bmatrix}22 & 9\end{bmatrix}, &  & \,9=5\cdot 3+(-2)\cdot 1+4\cdot (-1)\end{aligned}
$$

Therefore, 
$XY=\begin{bmatrix}22 & 9\end{bmatrix}.$

---

### generated variant

Level: easy; template: q-129496; profile: method-sign-omission

Find $XY$,  if  $X=\begin{bmatrix}-2 & -1 & 3\end{bmatrix}$ and $Y=\begin{bmatrix}-2 & 1 \\ 3 & -4 \\ -1 & -2\end{bmatrix}.$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}-2 \\ -4\end{bmatrix}$

✓ $\begin{bmatrix}-2 & -4\end{bmatrix}$

• $\begin{bmatrix}4 & -12\end{bmatrix}$

• $\begin{bmatrix}2 & 4\end{bmatrix}$

• $\begin{bmatrix}1 & 2\end{bmatrix}$

Here, $X$ is a $1\times 3$ matrix and $Y$ is a $3\times 2$ matrix. 

There are $3$ columns in $X$ and $3$ rows in $Y,$ so $X$ and $Y$ are conformable for multiplication:

$$
{X}_{1\times \boxed{\text{3}}}{\cdot }_{✓}{Y}_{\boxed{\text{3}}\times 2}={XY}_{1\times 2}
$$

Let's compute $XY,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}-2 & -1 & 3\end{bmatrix}\begin{bmatrix}-2 & 1 \\ 3 & -4 \\ -1 & -2\end{bmatrix}=\begin{bmatrix}-2 & ∗\end{bmatrix}, \\ & \,-2=(-2)\cdot (-2)+(-1)\cdot 3+3\cdot (-1) \\  & \begin{bmatrix}-2 & -1 & 3\end{bmatrix}\begin{bmatrix}-2 & 1 \\ 3 & -4 \\ -1 & -2\end{bmatrix}=\begin{bmatrix}-2 & -4\end{bmatrix}, \\ & \,-4=(-2)\cdot 1+(-1)\cdot (-4)+3\cdot (-2)\end{aligned}
$$

Therefore, 
$XY=\begin{bmatrix}-2 & -4\end{bmatrix}.$

---

### original evidence raw

Level: easy; template: q-317844; profile: observed-raw

Determine $AB$ given that 
$A=\begin{bmatrix}2 & 1 \\ 0 & 3 \\ -1 & 4 \\ 5 & 2\end{bmatrix}$
and
$B=\begin{bmatrix}1 & -2 \\ 0 & 3\end{bmatrix}.$

| $AB=\,\,$ |  | {{field-1}} | {{field-2}} |  |
| --- | --- | --- | --- | --- |
|  | {{field-3}} | $9$ |  |  |
|  | {{field-4}} | $14$ |  |  |
|  | $5$ | {{field-5}} |  |  |

Field field-2 (:answer-field.type/blank):

✓ $-1$

Field field-5 (:answer-field.type/blank):

✓ $-4$

Field field-4 (:answer-field.type/blank):

✓ $-1$

Field field-1 (:answer-field.type/blank):

✓ $2$

Field field-3 (:answer-field.type/blank):

✓ $0$

Here, $A$ is a $4\times 2$ matrix and $B$ is a $2\times 2$ matrix. 

There are $2$ columns in $A$ and $2$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{4\times \boxed{\text{2}}}{\cdot }_{✓}{B}_{\boxed{\text{2}}\times 2}={AB}_{4\times 2}
$$

Let's compute the unknown elements of $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}2 & 1 \\ 0 & 3 \\ -1 & 4 \\ 5 & 2\end{bmatrix}\begin{bmatrix}1 & -2 \\ 0 & 3\end{bmatrix}=\begin{bmatrix}2 & ∗ \\ ∗ & 9 \\ ∗ & 14 \\ 5 & ∗\end{bmatrix}, &  & \,2=2\cdot 1+1\cdot 0 \\  & \begin{bmatrix}2 & 1 \\ 0 & 3 \\ -1 & 4 \\ 5 & 2\end{bmatrix}\begin{bmatrix}1 & -2 \\ 0 & 3\end{bmatrix}=\begin{bmatrix}2 & -1 \\ ∗ & 9 \\ ∗ & 14 \\ 5 & ∗\end{bmatrix}, &  & \,-1=2\cdot (-2)+1\cdot 3 \\  & \begin{bmatrix}2 & 1 \\ 0 & 3 \\ -1 & 4 \\ 5 & 2\end{bmatrix}\begin{bmatrix}1 & -2 \\ 0 & 3\end{bmatrix}=\begin{bmatrix}2 & -1 \\ 0 & 9 \\ ∗ & 14 \\ 5 & ∗\end{bmatrix}, &  & \,0=0\cdot 1+3\cdot 0 \\  & \begin{bmatrix}2 & 1 \\ 0 & 3 \\ -1 & 4 \\ 5 & 2\end{bmatrix}\begin{bmatrix}1 & -2 \\ 0 & 3\end{bmatrix}=\begin{bmatrix}2 & -1 \\ 0 & 9 \\ -1 & 14 \\ 5 & ∗\end{bmatrix}, &  & \,-1=(-1)\cdot 1+4\cdot 0 \\  & \begin{bmatrix}2 & 1 \\ 0 & 3 \\ -1 & 4 \\ 5 & 2\end{bmatrix}\begin{bmatrix}1 & -2 \\ 0 & 3\end{bmatrix}=\begin{bmatrix}2 & -1 \\ 0 & 9 \\ -1 & 14 \\ 5 & -4\end{bmatrix}, &  & \,-4=5\cdot (-2)+2\cdot 3\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}2 & -1 \\ 0 & 9 \\ -1 & 14 \\ 5 & -4\end{bmatrix}.$

---

### generated variant

Level: easy; template: q-317844; profile: method-sign-omission

Determine $AB$ given that 
$A=\begin{bmatrix}2 & -2 \\ 0 & -4 \\ 2 & 3 \\ -1 & -2\end{bmatrix}$
and
$B=\begin{bmatrix}-4 & 5 \\ 0 & 1\end{bmatrix}.$

| $AB=$ | $-8$ | {{field-1}} |
| --- | --- | --- |
|  | $0$ | {{field-2}} |
|  | {{field-3}} | {{field-4}} |
|  | {{field-5}} | $-7$ |

Field field-2 (:answer-field.type/blank):

✓ $-4$

Field field-5 (:answer-field.type/blank):

✓ $4$

Field field-4 (:answer-field.type/blank):

✓ $13$

Field field-1 (:answer-field.type/blank):

✓ $8$

Field field-3 (:answer-field.type/blank):

✓ $-8$

Here, $A$ is a $4\times 2$ matrix and $B$ is a $2\times 2$ matrix. 

There are $2$ columns in $A$ and $2$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{4\times \boxed{\text{2}}}{\cdot }_{✓}{B}_{\boxed{\text{2}}\times 2}={AB}_{4\times 2}
$$

Let's compute the unknown elements of $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}2 & -2 \\ 0 & -4 \\ 2 & 3 \\ -1 & -2\end{bmatrix}\begin{bmatrix}-4 & 5 \\ 0 & 1\end{bmatrix}=\begin{bmatrix}-8 & 8 \\ 0 & ∗ \\ ∗ & ∗ \\ ∗ & -7\end{bmatrix}, \\ & \,8=2\cdot 5+(-2)\cdot 1 \\  & \begin{bmatrix}2 & -2 \\ 0 & -4 \\ 2 & 3 \\ -1 & -2\end{bmatrix}\begin{bmatrix}-4 & 5 \\ 0 & 1\end{bmatrix}=\begin{bmatrix}-8 & 8 \\ 0 & -4 \\ ∗ & ∗ \\ ∗ & -7\end{bmatrix}, \\ & \,-4=0\cdot 5+(-4)\cdot 1 \\  & \begin{bmatrix}2 & -2 \\ 0 & -4 \\ 2 & 3 \\ -1 & -2\end{bmatrix}\begin{bmatrix}-4 & 5 \\ 0 & 1\end{bmatrix}=\begin{bmatrix}-8 & 8 \\ 0 & -4 \\ -8 & ∗ \\ ∗ & -7\end{bmatrix}, \\ & \,-8=2\cdot (-4)+3\cdot 0 \\  & \begin{bmatrix}2 & -2 \\ 0 & -4 \\ 2 & 3 \\ -1 & -2\end{bmatrix}\begin{bmatrix}-4 & 5 \\ 0 & 1\end{bmatrix}=\begin{bmatrix}-8 & 8 \\ 0 & -4 \\ -8 & 13 \\ ∗ & -7\end{bmatrix}, \\ & \,13=2\cdot 5+3\cdot 1 \\  & \begin{bmatrix}2 & -2 \\ 0 & -4 \\ 2 & 3 \\ -1 & -2\end{bmatrix}\begin{bmatrix}-4 & 5 \\ 0 & 1\end{bmatrix}=\begin{bmatrix}-8 & 8 \\ 0 & -4 \\ -8 & 13 \\ 4 & -7\end{bmatrix}, \\ & \,4=(-1)\cdot (-4)+(-2)\cdot 0\end{aligned}
$$

Therefore, 
$AB=\begin{bmatrix}-8 & 8 \\ 0 & -4 \\ -8 & 13 \\ 4 & -7\end{bmatrix}.$

---

### original evidence raw

Level: easy; template: q-317846; profile: observed-raw

Determine $AB$ given that 
$A=\begin{bmatrix}1 & 2 & -1 \\ 0 & 3 & 4\end{bmatrix}$
and
$B=\begin{bmatrix}2 & 1 \\ -1 & 0 \\ 3 & -2\end{bmatrix}.$

| $AB=\,\,$ |  | {{field-1}} | $3$ |  |
| --- | --- | --- | --- | --- |
|  | $9$ | {{field-2}} |  |  |

Field field-2 (:answer-field.type/blank):

✓ $-8$

Field field-1 (:answer-field.type/blank):

✓ $-3$

Here, $A$ is a $2\times 3$ matrix and $B$ is a $3\times 2$ matrix. 

There are $3$ columns in $A$ and $3$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{2\times \boxed{\text{3}}}{\cdot }_{✓}{B}_{\boxed{\text{3}}\times 2}={AB}_{2\times 2}
$$

Let's compute the unknown elements of $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}1 & 2 & -1 \\ 0 & 3 & 4\end{bmatrix}\begin{bmatrix}2 & 1 \\ -1 & 0 \\ 3 & -2\end{bmatrix}=\begin{bmatrix}-3 & ∗ \\ ∗ & -8\end{bmatrix}, &  & \,-3=1\cdot 2+2\cdot (-1)+(-1)\cdot 3 \\  & \begin{bmatrix}1 & 2 & -1 \\ 0 & 3 & 4\end{bmatrix}\begin{bmatrix}2 & 1 \\ -1 & 0 \\ 3 & -2\end{bmatrix}=\begin{bmatrix}-3 & 3 \\ 9 & -8\end{bmatrix}, &  & \,-8=0\cdot 1+3\cdot 0+4\cdot (-2)\end{aligned}
$$

Therefore,

$$
AB=\begin{bmatrix}-3 & 3 \\ 9 & -8\end{bmatrix}.
$$

---

### generated variant

Level: easy; template: q-317846; profile: method-sign-omission

Determine $AB$ given that 
$A=\begin{bmatrix}2 & -4 & -1 \\ 0 & 1 & 3\end{bmatrix}$
and
$B=\begin{bmatrix}-1 & 4 \\ -1 & 0 \\ -1 & 3\end{bmatrix}.$

| $AB=$ | $3$ | {{field-1}} |
| --- | --- | --- |
|  | {{field-2}} | $9$ |

Field field-2 (:answer-field.type/blank):

✓ $-4$

Field field-1 (:answer-field.type/blank):

✓ $5$

Here, $A$ is a $2\times 3$ matrix and $B$ is a $3\times 2$ matrix. 

There are $3$ columns in $A$ and $3$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{2\times \boxed{\text{3}}}{\cdot }_{✓}{B}_{\boxed{\text{3}}\times 2}={AB}_{2\times 2}
$$

Let's compute the unknown elements of $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}2 & -4 & -1 \\ 0 & 1 & 3\end{bmatrix}\begin{bmatrix}-1 & 4 \\ -1 & 0 \\ -1 & 3\end{bmatrix}=\begin{bmatrix}3 & 5 \\ ∗ & 9\end{bmatrix}, \\ & \,5=2\cdot 4+(-4)\cdot 0+(-1)\cdot 3 \\  & \begin{bmatrix}2 & -4 & -1 \\ 0 & 1 & 3\end{bmatrix}\begin{bmatrix}-1 & 4 \\ -1 & 0 \\ -1 & 3\end{bmatrix}=\begin{bmatrix}3 & 5 \\ -4 & 9\end{bmatrix}, \\ & \,-4=0\cdot (-1)+1\cdot (-1)+3\cdot (-1)\end{aligned}
$$

Therefore,

$$
AB=\begin{bmatrix}3 & 5 \\ -4 & 9\end{bmatrix}.
$$

---

### original evidence raw

Level: easy; template: q-317847; profile: observed-raw

Determine $AB$ given that 
$A=\begin{bmatrix}2 & -1 & 0 \\ 4 & 3 & 1\end{bmatrix}$
and
$B=\begin{bmatrix}1 & 2 \\ -3 & 0 \\ 5 & -1\end{bmatrix}.$

| $AB=\,\,$ |  | {{field-1}} | $4$ |  |
| --- | --- | --- | --- | --- |
|  | $0$ | {{field-2}} |  |  |

Field field-1 (:answer-field.type/blank):

✓ $5$

Field field-2 (:answer-field.type/blank):

✓ $7$

Here, $A$ is a $2\times 3$ matrix and $B$ is a $3\times 2$ matrix. 

There are $3$ columns in $A$ and $3$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{2\times \boxed{\text{3}}}{\cdot }_{✓}{B}_{\boxed{\text{3}}\times 2}={AB}_{2\times 2}
$$

Let's compute the unknown elements of $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}2 & -1 & 0 \\ 4 & 3 & 1\end{bmatrix}\begin{bmatrix}1 & 2 \\ -3 & 0 \\ 5 & -1\end{bmatrix}=\begin{bmatrix}5 & 4 \\ 0 & ∗\end{bmatrix}, &  & \,5=2\cdot 1+(-1)\cdot (-3)+0\cdot 5 \\  & \begin{bmatrix}2 & -1 & 0 \\ 4 & 3 & 1\end{bmatrix}\begin{bmatrix}1 & 2 \\ -3 & 0 \\ 5 & -1\end{bmatrix}=\begin{bmatrix}5 & 4 \\ 0 & 7\end{bmatrix}, &  & \,7=4\cdot 2+3\cdot 0+1\cdot (-1)\end{aligned}
$$

Therefore,

$$
AB=\begin{bmatrix}5 & 4 \\ 0 & 7\end{bmatrix}.
$$

---

### generated variant

Level: easy; template: q-317847; profile: method-sign-omission

Determine $AB$ given that 
$A=\begin{bmatrix}1 & -4 & 0 \\ -1 & -3 & -1\end{bmatrix}$
and
$B=\begin{bmatrix}3 & -2 \\ 2 & 0 \\ -4 & 4\end{bmatrix}.$

| $AB=$ | {{field-1}} | $-2$ |
| --- | --- | --- |
|  | {{field-2}} | $-2$ |

Field field-1 (:answer-field.type/blank):

✓ $-5$

Field field-2 (:answer-field.type/blank):

✓ $-5$

Here, $A$ is a $2\times 3$ matrix and $B$ is a $3\times 2$ matrix. 

There are $3$ columns in $A$ and $3$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{2\times \boxed{\text{3}}}{\cdot }_{✓}{B}_{\boxed{\text{3}}\times 2}={AB}_{2\times 2}
$$

Let's compute the unknown elements of $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}1 & -4 & 0 \\ -1 & -3 & -1\end{bmatrix}\begin{bmatrix}3 & -2 \\ 2 & 0 \\ -4 & 4\end{bmatrix}=\begin{bmatrix}-5 & -2 \\ ∗ & -2\end{bmatrix}, \\ & \,-5=1\cdot 3+(-4)\cdot 2+0\cdot (-4) \\  & \begin{bmatrix}1 & -4 & 0 \\ -1 & -3 & -1\end{bmatrix}\begin{bmatrix}3 & -2 \\ 2 & 0 \\ -4 & 4\end{bmatrix}=\begin{bmatrix}-5 & -2 \\ -5 & -2\end{bmatrix}, \\ & \,-5=(-1)\cdot 3+(-3)\cdot 2+(-1)\cdot (-4)\end{aligned}
$$

Therefore,

$$
AB=\begin{bmatrix}-5 & -2 \\ -5 & -2\end{bmatrix}.
$$

---

### original evidence raw

Level: easy; template: q-317848; profile: observed-raw

Determine $AB$ given that 
$A=\begin{bmatrix}1 & 0 & -2 & 3 \\ 4 & 1 & 0 & -1\end{bmatrix}$
and
$B=\begin{bmatrix}2 & -1 \\ 1 & 3 \\ 0 & 4 \\ -2 & 1\end{bmatrix}.$

| $AB=\,\,$ |  | {{field-1}} | $-6$ |  |
| --- | --- | --- | --- | --- |
|  | $11$ | {{field-2}} |  |  |

Field field-2 (:answer-field.type/blank):

✓ $-2$

Field field-1 (:answer-field.type/blank):

✓ $-4$

Here, $A$ is a $2\times 4$ matrix and $B$ is a $4\times 2$ matrix. 

There are $4$ columns in $A$ and $4$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{2\times \boxed{\text{4}}}{\cdot }_{✓}{B}_{\boxed{\text{4}}\times 2}={AB}_{2\times 2}
$$

Let's compute the unknown elements of $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}1 & 0 & -2 & 3 \\ 4 & 1 & 0 & -1\end{bmatrix}\begin{bmatrix}2 & -1 \\ 1 & 3 \\ 0 & 4 \\ -2 & 1\end{bmatrix}=\begin{bmatrix}-4 & -6 \\ 11 & ∗\end{bmatrix}, &  & \,-4=1\cdot 2+0\cdot 1+(-2)\cdot 0+3\cdot (-2) \\  & \begin{bmatrix}1 & 0 & -2 & 3 \\ 4 & 1 & 0 & -1\end{bmatrix}\begin{bmatrix}2 & -1 \\ 1 & 3 \\ 0 & 4 \\ -2 & 1\end{bmatrix}=\begin{bmatrix}-4 & -6 \\ 11 & -2\end{bmatrix}, &  & \,-2=4\cdot (-1)+1\cdot 3+0\cdot 4+(-1)\cdot 1\end{aligned}
$$

Therefore,

$$
AB=\begin{bmatrix}-4 & -6 \\ 11 & -2\end{bmatrix}.
$$

---

### generated variant

Level: easy; template: q-317848; profile: method-sign-omission

Determine $AB$ given that 
$A=\begin{bmatrix}-2 & 0 & 1 & -1 \\ -2 & 3 & 0 & -1\end{bmatrix}$
and
$B=\begin{bmatrix}-1 & 2 \\ -2 & 2 \\ 0 & 2 \\ 3 & 2\end{bmatrix}.$

| $AB=$ | $-1$ | {{field-1}} |
| --- | --- | --- |
|  | {{field-2}} | $0$ |

Field field-2 (:answer-field.type/blank):

✓ $-7$

Field field-1 (:answer-field.type/blank):

✓ $-4$

Here, $A$ is a $2\times 4$ matrix and $B$ is a $4\times 2$ matrix. 

There are $4$ columns in $A$ and $4$ rows in $B,$ so $A$ and $B$ are conformable for multiplication:

$$
{A}_{2\times \boxed{\text{4}}}{\cdot }_{✓}{B}_{\boxed{\text{4}}\times 2}={AB}_{2\times 2}
$$

Let's compute the unknown elements of $AB,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}-2 & 0 & 1 & -1 \\ -2 & 3 & 0 & -1\end{bmatrix}\begin{bmatrix}-1 & 2 \\ -2 & 2 \\ 0 & 2 \\ 3 & 2\end{bmatrix}=\begin{bmatrix}-1 & -4 \\ ∗ & 0\end{bmatrix}, \\ & \,-4=(-2)\cdot 2+0\cdot 2+1\cdot 2+(-1)\cdot 2 \\  & \begin{bmatrix}-2 & 0 & 1 & -1 \\ -2 & 3 & 0 & -1\end{bmatrix}\begin{bmatrix}-1 & 2 \\ -2 & 2 \\ 0 & 2 \\ 3 & 2\end{bmatrix}=\begin{bmatrix}-1 & -4 \\ -7 & 0\end{bmatrix}, \\ & \,-7=(-2)\cdot (-1)+3\cdot (-2)+0\cdot 0+(-1)\cdot 3\end{aligned}
$$

Therefore,

$$
AB=\begin{bmatrix}-1 & -4 \\ -7 & 0\end{bmatrix}.
$$

---

### original evidence raw

Level: easy; template: q-70928; profile: observed-raw

Find $BC$,  if  $B=\begin{bmatrix}-3 & 1 & -2\end{bmatrix}$ and $C=\begin{bmatrix}1 & 2 \\ 3 & 4 \\ 5 & 6\end{bmatrix}.$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}-1 & -7\end{bmatrix}$

• $\begin{bmatrix}5 & 14\end{bmatrix}$

• $\begin{bmatrix}-1 & 14\end{bmatrix}$

✓ $\begin{bmatrix}-10 & -14\end{bmatrix}$

• $\begin{bmatrix}10 & -1\end{bmatrix}$

Here, $B$ is a $1\times 3$ matrix and $C$ is a $3\times 2$ matrix. 

There are $3$ columns in $B$ and $3$ rows in $C,$ so $B$ and $C$ are conformable for multiplication:

$$
{B}_{1\times \boxed{\text{3}}}{\cdot }_{✓}{C}_{\boxed{\text{3}}\times 2}={BC}_{1\times 2}
$$

Let's compute $BC,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}-3 & 1 & -2\end{bmatrix}\begin{bmatrix}1 & 2 \\ 3 & 4 \\ 5 & 6\end{bmatrix}=\begin{bmatrix}-10 & ∗\end{bmatrix}, &  & \,-10=(-3)\cdot 1+1\cdot 3+(-2)\cdot 5 \\  & \begin{bmatrix}-3 & 1 & -2\end{bmatrix}\begin{bmatrix}1 & 2 \\ 3 & 4 \\ 5 & 6\end{bmatrix}=\begin{bmatrix}-10 & -14\end{bmatrix}, &  & \,-14=(-3)\cdot 2+1\cdot 4+(-2)\cdot 6\end{aligned}
$$

Therefore, 
$BC=\begin{bmatrix}-10 & -14\end{bmatrix}.$

---

### generated variant

Level: easy; template: q-70928; profile: method-sign-omission

Find $BC$,  if  $B=\begin{bmatrix}-2 & -1 & 3\end{bmatrix}$ and $C=\begin{bmatrix}-2 & 1 \\ 3 & -4 \\ -1 & -2\end{bmatrix}.$

Field selection (:answer-field.type/radio):

• $\begin{bmatrix}-2 \\ -4\end{bmatrix}$

✓ $\begin{bmatrix}-2 & -4\end{bmatrix}$

• $\begin{bmatrix}4 & -12\end{bmatrix}$

• $\begin{bmatrix}2 & 4\end{bmatrix}$

• $\begin{bmatrix}1 & 2\end{bmatrix}$

Here, $B$ is a $1\times 3$ matrix and $C$ is a $3\times 2$ matrix. 

There are $3$ columns in $B$ and $3$ rows in $C,$ so $B$ and $C$ are conformable for multiplication:

$$
{B}_{1\times \boxed{\text{3}}}{\cdot }_{✓}{C}_{\boxed{\text{3}}\times 2}={BC}_{1\times 2}
$$

Let's compute $BC,$ one element at a time:

$$
\begin{aligned} & \begin{bmatrix}-2 & -1 & 3\end{bmatrix}\begin{bmatrix}-2 & 1 \\ 3 & -4 \\ -1 & -2\end{bmatrix}=\begin{bmatrix}-2 & ∗\end{bmatrix}, \\ & \,-2=(-2)\cdot (-2)+(-1)\cdot 3+3\cdot (-1) \\  & \begin{bmatrix}-2 & -1 & 3\end{bmatrix}\begin{bmatrix}-2 & 1 \\ 3 & -4 \\ -1 & -2\end{bmatrix}=\begin{bmatrix}-2 & -4\end{bmatrix}, \\ & \,-4=(-2)\cdot 1+(-1)\cdot (-4)+3\cdot (-2)\end{aligned}
$$

Therefore, 
$BC=\begin{bmatrix}-2 & -4\end{bmatrix}.$

---

### generated easy variant

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

### generated easy variant

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

### authored missing-level variant

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

### authored missing-level variant

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

### authored missing-level variant

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

### authored missing-level variant

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
