# Determinant review

All raw sources are retained in source.json. q-1088 has authored easy assignment/solution and inferred correct choice; observed intent is not claimed. All hard questions are authored numerical arithmetic extensions.

## Original q-1088

What is $\begin{vmatrix}\sqrt{2} & 5 \\ 1 & 3\end{vmatrix}$?

Raw bank: ["1", "\\sqrt{6} + 5", "3\\sqrt{2} - 5", "-2", "\\sqrt{6} - 5"]

(No original worked solution)

### Generator replay

What is $\begin{vmatrix}\sqrt{2} & 5 \\ 1 & 3\end{vmatrix}$?

- $3\sqrt{2}-5$
- $\sqrt{6}+5$
- $1$
- $-5+\sqrt{6}$
- $-2$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(A) & =|\begin{aligned}\sqrt{2} & 5 \\ 1 & 3\end{aligned}| \\  & =\sqrt{2}\cdot 3-5\cdot 1 \\  & =3\sqrt{2}-5\end{aligned}
$$

## Original q-1089

Calculate $det(Z)$, if
 $Z=[\begin{aligned}\sqrt{x} & y \\ {y}^{2} & \sqrt{x}\end{aligned}].$

Raw bank: ["x-2{y}^{2}", "2\\sqrt{x}-{y}^{3}", "x-{y}^{3}", "\\sqrt{x}-2{y}^{3}", "x-{y}^{2}"]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(Z) & =|\begin{aligned}\sqrt{x} & y \\ {y}^{2} & \sqrt{x}\end{aligned}| \\  & =\sqrt{x}\cdot \sqrt{x}-y\cdot {y}^{2} \\  & =x-{y}^{3}\end{aligned}
$$

### Generator replay

Calculate $det(Z)$, if
 $Z=[\begin{aligned}\sqrt{x} & y \\ {y}^{2} & \sqrt{x}\end{aligned}].$

- $x-{y}^{3}$
- $2\sqrt{x}-{y}^{3}$
- $x-2{y}^{2}$
- $x-{y}^{2}$
- $\sqrt{x}-2{y}^{3}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(Z) & =|\begin{aligned}\sqrt{x} & y \\ {y}^{2} & \sqrt{x}\end{aligned}| \\  & =\sqrt{x}\cdot \sqrt{x}-y\cdot {y}^{2} \\  & =x-{y}^{3}\end{aligned}
$$

## Original q-1083

$|\begin{aligned}2x & {y}^{2} \\ z & -3\end{aligned}|=$

Raw bank: ["5", "1", "6x-{y}^{2}", "6x-{y}^{2}z", "-6x-{y}^{2}z"]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}2x & {y}^{2} \\ z & -3\end{aligned}| & =2x\cdot (-3)-{y}^{2}\cdot z \\  & =-6x-{y}^{2}z\end{aligned}
$$

### Generator replay

$|\begin{aligned}2x & {y}^{2} \\ z & -3\end{aligned}|=$

- $6x-{y}^{2}$
- $1$
- $5$
- $-6x-{y}^{2}z$
- $6x-{y}^{2}z$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}2x & {y}^{2} \\ z & -3\end{aligned}| & =2x\cdot (-3)-{y}^{2}\cdot z \\  & =-6x-{y}^{2}z\end{aligned}
$$

## Original q-1087

Calculate $det(T)$, if
    $T=[\begin{aligned}\frac{1}{2} & 17 \\ 1 & 10\end{aligned}].$

Raw bank: ["3", "7", "-17", "-12", "22"]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(T) & =|\begin{aligned}\frac{1}{2} & 17 \\ 1 & 10\end{aligned}| \\  & =\frac{1}{2}\cdot 10-17\cdot 1 \\  & =5-17 \\  & =-12\end{aligned}
$$

### Generator replay

Calculate $det(T)$, if
    $T=[\begin{aligned}\frac{1}{2} & 17 \\ 1 & 10\end{aligned}].$

- $-17$
- $7$
- $3$
- $22$
- $-12$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(T) & =|\begin{aligned}\frac{1}{2} & 17 \\ 1 & 10\end{aligned}| \\  & =\frac{1}{2}\cdot 10-17\cdot 1 \\  & =5-17 \\  & =-12\end{aligned}
$$

## Original q-127601

Calculate $det(C)$, if
    $C=[\begin{aligned}-x & -2y \\ \frac{x}{2} & 5y\end{aligned}].$

Raw bank: ["5xy", "-\\frac{3xy}{2}", "-4xy", "\\frac{5xy}{2}", "-5xy"]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}-x & -2y \\ \frac{x}{2} & 5y\end{aligned}| \\  & =-x\cdot 5y-(-2y)\cdot \frac{x}{2} \\  & =-5xy+xy \\  & =-4xy\end{aligned}
$$

### Generator replay

Calculate $det(C)$, if
    $C=[\begin{aligned}-x & -2y \\ \frac{x}{2} & 5y\end{aligned}].$

- $-4xy$
- $-\frac{3xy}{2}$
- $5xy$
- $-5xy$
- $\frac{5xy}{2}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}-x & -2y \\ \frac{x}{2} & 5y\end{aligned}| \\  & =-x\cdot 5y-(-2y)\cdot \frac{x}{2} \\  & =-5xy+xy \\  & =-4xy\end{aligned}
$$

## Original q-127603

Calculate $det(D)$, if
    $D=[\begin{aligned}2x & y \\ -5 & xy\end{aligned}].$

Raw bank: ["3{y}^{2}x-5", "y(2{x}^{2}+5)", "3{x}^{2}y+3", "4{x}^{2}{y}^{2}", "y(2{x}^{2}-3)"]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}2x & y \\ -5 & xy\end{aligned}| \\  & =2x\cdot xy-y\cdot (-5) \\  & =2{x}^{2}y+5y \\  & =y(2{x}^{2}+5)\end{aligned}
$$

### Generator replay

Calculate $det(D)$, if
    $D=[\begin{aligned}2x & y \\ -5 & xy\end{aligned}].$

- $3{x}^{2}y+3$
- $y(2{x}^{2}+5)$
- $3{y}^{2}x-5$
- $y(2{x}^{2}-3)$
- $4{x}^{2}{y}^{2}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}2x & y \\ -5 & xy\end{aligned}| \\  & =2x\cdot xy-y\cdot (-5) \\  & =2{x}^{2}y+5y \\  & =y(2{x}^{2}+5)\end{aligned}
$$

## Original q-275595

Evaluate the determinant:

$|\begin{aligned}\sqrt{3} & y \\ 2 & \sqrt{3}\end{aligned}|=$
 {{field-1}}

Raw bank: ["3-2y"]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}|\begin{aligned}\sqrt{3} & y \\ 2 & \sqrt{3}\end{aligned}| & =\sqrt{3}\cdot \sqrt{3}-y\cdot 2 \\  & =3-2y.\end{aligned}
$$

### Generator replay

Evaluate the determinant:

$|\begin{aligned}\sqrt{3} & y \\ 2 & \sqrt{3}\end{aligned}|=$
 {{field-1}}

- $3-2y$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}|\begin{aligned}\sqrt{3} & y \\ 2 & \sqrt{3}\end{aligned}| & =\sqrt{3}\cdot \sqrt{3}-y\cdot 2 \\  & =3-2y.\end{aligned}
$$

## Original q-317367

Calculate $det(D)$ given that
$D=[\begin{aligned}\frac{2}{5} & -3 \\ -\frac{1}{2} & 2\end{aligned}].$

$det(D)=$
{{field-1}}

Raw bank: ["-\\frac{7}{10}"]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}\frac{2}{5} & -3 \\ -\frac{1}{2} & 2\end{aligned}| \\  & =\frac{2}{5}\cdot 2-(-3)\cdot (-\frac{1}{2}) \\  & =\frac{4}{5}-\frac{3}{2} \\  & =-\frac{7}{10}.\end{aligned}
$$

### Generator replay

Calculate $det(D)$ given that
$D=[\begin{aligned}\frac{2}{5} & -3 \\ -\frac{1}{2} & 2\end{aligned}].$

$det(D)=$
{{field-1}}

- $-\frac{7}{10}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}\frac{2}{5} & -3 \\ -\frac{1}{2} & 2\end{aligned}| \\  & =\frac{2}{5}\cdot 2-(-3)\cdot (-\frac{1}{2}) \\  & =\frac{4}{5}-\frac{3}{2} \\  & =-\frac{7}{10}.\end{aligned}
$$

## Original q-317368

Calculate $det(E)$ given that
$E=[\begin{aligned}-\frac{3}{4} & 5 \\ 2 & -1\end{aligned}].$

$det(E)=$
{{field-1}}

Raw bank: ["-\\frac{37}{4}"]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(E) & =|\begin{aligned}-\frac{3}{4} & 5 \\ 2 & -1\end{aligned}| \\  & =-\frac{3}{4}\cdot (-1)-5\cdot 2 \\  & =\frac{3}{4}-10 \\  & =-\frac{37}{4}.\end{aligned}
$$

### Generator replay

Calculate $det(E)$ given that
$E=[\begin{aligned}-\frac{3}{4} & 5 \\ 2 & -1\end{aligned}].$

$det(E)=$
{{field-1}}

- $-\frac{37}{4}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(E) & =|\begin{aligned}-\frac{3}{4} & 5 \\ 2 & -1\end{aligned}| \\  & =-\frac{3}{4}\cdot (-1)-5\cdot 2 \\  & =\frac{3}{4}-10 \\  & =-\frac{37}{4}.\end{aligned}
$$

## Original q-317372

Calculate $det(D)$ given that
$D=[\begin{aligned}3x & 2y \\ -5 & x\end{aligned}].$

$det(D)=$
{{field-1}}

Raw bank: ["3{x}^{2}+10y"]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}3x & 2y \\ -5 & x\end{aligned}| \\  & =3x\cdot x-2y\cdot (-5) \\  & =3{x}^{2}+10y.\end{aligned}
$$

### Generator replay

Calculate $det(D)$ given that
$D=[\begin{aligned}3x & 2y \\ -5 & x\end{aligned}].$

$det(D)=$
{{field-1}}

- $3{x}^{2}+10y$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}3x & 2y \\ -5 & x\end{aligned}| \\  & =3x\cdot x-2y\cdot (-5) \\  & =3{x}^{2}+10y.\end{aligned}
$$

## Original q-317374

Evaluate the determinant:

$|\begin{aligned}\sqrt{6} & y \\ 4 & \sqrt{6}\end{aligned}|=$
{{field-1}}

Raw bank: ["6-4y"]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}|\begin{aligned}\sqrt{6} & y \\ 4 & \sqrt{6}\end{aligned}| & =\sqrt{6}\cdot \sqrt{6}-y\cdot 4 \\  & =6-4y.\end{aligned}
$$

### Generator replay

Evaluate the determinant:

$|\begin{aligned}\sqrt{6} & y \\ 4 & \sqrt{6}\end{aligned}|=$
{{field-1}}

- $6-4y$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}|\begin{aligned}\sqrt{6} & y \\ 4 & \sqrt{6}\end{aligned}| & =\sqrt{6}\cdot \sqrt{6}-y\cdot 4 \\  & =6-4y.\end{aligned}
$$

## Original q-69649

$|\begin{aligned}3\sqrt{x} & {z}^{2} \\ 2y & -\sqrt{x}\end{aligned}|=$

Raw bank: ["-3x-2y{z}^{2}", "3x-2{z}^{2}y", "-2x-3y{z}^{2}", "-3x-2{y}^{2}z", "2x+3y{z}^{2}"]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}3\sqrt{x} & {z}^{2} \\ 2y & -\sqrt{x}\end{aligned}| & =3\sqrt{x}\cdot (-\sqrt{x})-{z}^{2}\cdot 2y \\  & =-3x-2y{z}^{2}\end{aligned}
$$

### Generator replay

$|\begin{aligned}3\sqrt{x} & {z}^{2} \\ 2y & -\sqrt{x}\end{aligned}|=$

- $-2x-3y{z}^{2}$
- $3x-2{z}^{2}y$
- $-3x-2y{z}^{2}$
- $2x+3y{z}^{2}$
- $-3x-2{y}^{2}z$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}3\sqrt{x} & {z}^{2} \\ 2y & -\sqrt{x}\end{aligned}| & =3\sqrt{x}\cdot (-\sqrt{x})-{z}^{2}\cdot 2y \\  & =-3x-2y{z}^{2}\end{aligned}
$$

## Original q-69650

Calculate $det(H)$, if
    $H=[\begin{aligned}-2r & 3s \\ -2t & 3u\end{aligned}].$

Raw bank: ["6(ru-st)", "6ru-3st", "6(st-ru)", "-6ru+3st", "3(2st-ru)"]

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(H) & =|\begin{aligned}-2r & 3s \\ -2t & 3u\end{aligned}| \\  & =-2r\cdot 3u-3s\cdot (-2t) \\  & =-6ru-(-6st) \\  & =-6ru+6st \\  & =6(st-ru)\end{aligned}
$$

### Generator replay

Calculate $det(H)$, if
    $H=[\begin{aligned}-2r & 3s \\ -2t & 3u\end{aligned}].$

- $6(st-ru)$
- $6ru-3st$
- $6(ru-st)$
- $3(2st-ru)$
- $-6ru+3st$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(H) & =|\begin{aligned}-2r & 3s \\ -2t & 3u\end{aligned}| \\  & =-2r\cdot 3u-3s\cdot (-2t) \\  & =-6ru-(-6st) \\  & =-6ru+6st \\  & =6(st-ru)\end{aligned}
$$

## Generated variant / numeric_radical / authored-operations

What is $\begin{vmatrix}\sqrt{3} & 5 \\ 3 & 6\end{vmatrix}$?

- $-15$
- $-6\sqrt{3}+15$
- $6\sqrt{3}-15$
- $6\sqrt{3}+15$
- $6\sqrt{3}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(A) & =|\begin{aligned}\sqrt{3} & 5 \\ 3 & 6\end{aligned}| \\  & =\sqrt{3}\cdot 6-5\cdot 3 \\  & =6\sqrt{3}-15\end{aligned}
$$

## Generated variant / numeric_radical / authored-operations

What is $\begin{vmatrix}\sqrt{2} & 3 \\ 2 & 6\end{vmatrix}$?

- $6\sqrt{2}-6$
- $-6\sqrt{2}+6$
- $-6$
- $6+6\sqrt{2}$
- $6\sqrt{2}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(A) & =|\begin{aligned}\sqrt{2} & 3 \\ 2 & 6\end{aligned}| \\  & =\sqrt{2}\cdot 6-3\cdot 2 \\  & =6\sqrt{2}-6\end{aligned}
$$

## Generated variant / symbolic_radical / authored-operations

Calculate $det(Z)$, if
 $Z=[\begin{aligned}\sqrt{x} & y \\ {y}^{3} & \sqrt{x}\end{aligned}].$

- $-x+{y}^{4}$
- $-{y}^{4}$
- $x+{y}^{4}$
- $x$
- $x-{y}^{4}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(Z) & =|\begin{aligned}\sqrt{x} & y \\ {y}^{3} & \sqrt{x}\end{aligned}| \\  & =\sqrt{x}\cdot \sqrt{x}-y\cdot {y}^{3} \\  & =x-{y}^{4}\end{aligned}
$$

## Generated variant / symbolic_radical / authored-operations

Calculate $det(Z)$, if
 $Z=[\begin{aligned}\sqrt{x} & y \\ {y}^{2} & \sqrt{x}\end{aligned}].$

- $x$
- $-{y}^{3}$
- $-x+{y}^{3}$
- $x-{y}^{3}$
- $x+{y}^{3}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(Z) & =|\begin{aligned}\sqrt{x} & y \\ {y}^{2} & \sqrt{x}\end{aligned}| \\  & =\sqrt{x}\cdot \sqrt{x}-y\cdot {y}^{2} \\  & =x-{y}^{3}\end{aligned}
$$

## Generated variant / linear_power / authored-operations

$|\begin{aligned}5x & {y}^{3} \\ z & -2\end{aligned}|=$

- $-{y}^{3}z$
- $-10x$
- $-10x+{y}^{3}z$
- $-10x-{y}^{3}z$
- $10x+{y}^{3}z$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}5x & {y}^{3} \\ z & -2\end{aligned}| & =5x\cdot (-2)-{y}^{3}\cdot z \\  & =-10x-{y}^{3}z\end{aligned}
$$

## Generated variant / linear_power / authored-operations

$|\begin{aligned}2x & {y}^{2} \\ z & -3\end{aligned}|=$

- $6x+{y}^{2}z$
- $-6x+{y}^{2}z$
- $-6x-{y}^{2}z$
- $-6x$
- $-{y}^{2}z$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}2x & {y}^{2} \\ z & -3\end{aligned}| & =2x\cdot (-3)-{y}^{2}\cdot z \\  & =-6x-{y}^{2}z\end{aligned}
$$

## Generated variant / easy_fraction / authored-operations

Calculate $det(T)$, if
    $T=[\begin{aligned}\frac{1}{5} & 23 \\ 1 & 10\end{aligned}].$

- $-23$
- $2$
- $25$
- $-21$
- $21$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(T) & =|\begin{aligned}\frac{1}{5} & 23 \\ 1 & 10\end{aligned}| \\  & =\frac{1}{5}\cdot 10-23\cdot 1 \\  & =2-23 \\  & =-21\end{aligned}
$$

## Generated variant / easy_fraction / authored-operations

Calculate $det(T)$, if
    $T=[\begin{aligned}\frac{1}{2} & 8 \\ 1 & 6\end{aligned}].$

- $-5$
- $5$
- $-8$
- $11$
- $3$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(T) & =|\begin{aligned}\frac{1}{2} & 8 \\ 1 & 6\end{aligned}| \\  & =\frac{1}{2}\cdot 6-8\cdot 1 \\  & =3-8 \\  & =-5\end{aligned}
$$

## Generated variant / shared_monomial / authored-operations

Calculate $det(C)$, if
    $C=[\begin{aligned}-4x & -3y \\ \frac{x}{3} & 7y\end{aligned}].$

- $-27xy$
- $xy$
- $-28xy$
- $27xy$
- $-29xy$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}-4x & -3y \\ \frac{x}{3} & 7y\end{aligned}| \\  & =-4x\cdot 7y-(-3y)\cdot \frac{x}{3} \\  & =-28xy+xy \\  & =-27xy\end{aligned}
$$

## Generated variant / shared_monomial / authored-operations

Calculate $det(C)$, if
    $C=[\begin{aligned}-2x & -6y \\ \frac{x}{6} & 3y\end{aligned}].$

- $-6xy$
- $-7xy$
- $5xy$
- $xy$
- $-5xy$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}-2x & -6y \\ \frac{x}{6} & 3y\end{aligned}| \\  & =-2x\cdot 3y-(-6y)\cdot \frac{x}{6} \\  & =-6xy+xy \\  & =-5xy\end{aligned}
$$

## Generated variant / factored_polynomial / authored-operations

Calculate $det(D)$, if
    $D=[\begin{aligned}5x & y \\ -2 & xy\end{aligned}].$

- $2y$
- $5{x}^{2}y-2y$
- $y(5{x}^{2}+2)$
- $-y\left(5{x}^{2}+2\right)$
- $5{x}^{2}y$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}5x & y \\ -2 & xy\end{aligned}| \\  & =5x\cdot xy-y\cdot (-2) \\  & =5{x}^{2}y+2y \\  & =y(5{x}^{2}+2)\end{aligned}
$$

## Generated variant / factored_polynomial / authored-operations

Calculate $det(D)$, if
    $D=[\begin{aligned}2x & y \\ -3 & xy\end{aligned}].$

- $-y\left(2{x}^{2}+3\right)$
- $2{x}^{2}y-3y$
- $3y$
- $2{x}^{2}y$
- $y(2{x}^{2}+3)$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}2x & y \\ -3 & xy\end{aligned}| \\  & =2x\cdot xy-y\cdot (-3) \\  & =2{x}^{2}y+3y \\  & =y(2{x}^{2}+3)\end{aligned}
$$

## Generated variant / radical_blank / blank

Evaluate the determinant:

$|\begin{aligned}\sqrt{11} & y \\ 2 & \sqrt{11}\end{aligned}|=$
{{field-1}}

- $11-2y$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}|\begin{aligned}\sqrt{11} & y \\ 2 & \sqrt{11}\end{aligned}| & =\sqrt{11}\cdot \sqrt{11}-y\cdot 2 \\  & =11-2y.\end{aligned}
$$

## Generated variant / radical_blank / blank

Evaluate the determinant:

$|\begin{aligned}\sqrt{2} & y \\ 3 & \sqrt{2}\end{aligned}|=$
{{field-1}}

- $2-3y$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}|\begin{aligned}\sqrt{2} & y \\ 3 & \sqrt{2}\end{aligned}| & =\sqrt{2}\cdot \sqrt{2}-y\cdot 3 \\  & =2-3y.\end{aligned}
$$

## Generated variant / two_fractions / blank

Calculate $det(D)$ given that
$D=[\begin{aligned}\frac{2}{5} & -7 \\ -\frac{2}{3} & 4\end{aligned}].$

$det(D)=$
{{field-1}}

- $-\frac{46}{15}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}\frac{2}{5} & -7 \\ -\frac{2}{3} & 4\end{aligned}| \\  & =\frac{2}{5}\cdot 4-(-7)\cdot (-\frac{2}{3}) \\  & =\frac{8}{5}-\frac{14}{3} \\  & =-\frac{46}{15}.\end{aligned}
$$

## Generated variant / two_fractions / blank

Calculate $det(D)$ given that
$D=[\begin{aligned}\frac{1}{8} & -4 \\ -\frac{1}{6} & 7\end{aligned}].$

$det(D)=$
{{field-1}}

- $\frac{5}{24}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}\frac{1}{8} & -4 \\ -\frac{1}{6} & 7\end{aligned}| \\  & =\frac{1}{8}\cdot 7-(-4)\cdot (-\frac{1}{6}) \\  & =\frac{7}{8}-\frac{2}{3} \\  & =\frac{5}{24}.\end{aligned}
$$

## Generated variant / one_fraction / blank

Calculate $det(E)$ given that
$E=[\begin{aligned}-\frac{1}{3} & 4 \\ 3 & -4\end{aligned}].$

$det(E)=$
{{field-1}}

- $-\frac{32}{3}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(E) & =|\begin{aligned}-\frac{1}{3} & 4 \\ 3 & -4\end{aligned}| \\  & =-\frac{1}{3}\cdot (-4)-4\cdot 3 \\  & =\frac{4}{3}-12 \\  & =-\frac{32}{3}.\end{aligned}
$$

## Generated variant / one_fraction / blank

Calculate $det(E)$ given that
$E=[\begin{aligned}-\frac{1}{8} & 4 \\ 1 & -5\end{aligned}].$

$det(E)=$
{{field-1}}

- $-\frac{27}{8}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(E) & =|\begin{aligned}-\frac{1}{8} & 4 \\ 1 & -5\end{aligned}| \\  & =-\frac{1}{8}\cdot (-5)-4\cdot 1 \\  & =\frac{5}{8}-4 \\  & =-\frac{27}{8}.\end{aligned}
$$

## Generated variant / polynomial_blank / blank

Calculate $det(D)$ given that
$D=[\begin{aligned}5x & 2y \\ -5 & x\end{aligned}].$

$det(D)=$
{{field-1}}

- $5{x}^{2}+10y$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}5x & 2y \\ -5 & x\end{aligned}| \\  & =5x\cdot x-2y\cdot (-5) \\  & =5{x}^{2}+10y.\end{aligned}
$$

## Generated variant / polynomial_blank / blank

Calculate $det(D)$ given that
$D=[\begin{aligned}2x & 3y \\ -2 & x\end{aligned}].$

$det(D)=$
{{field-1}}

- $2{x}^{2}+6y$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}2x & 3y \\ -2 & x\end{aligned}| \\  & =2x\cdot x-3y\cdot (-2) \\  & =2{x}^{2}+6y.\end{aligned}
$$

## Generated variant / radical_power / authored-operations

$|\begin{aligned}5\sqrt{x} & {z}^{3} \\ 2y & -\sqrt{x}\end{aligned}|=$

- $-2y{z}^{3}$
- $-5x$
- $-5x+2y{z}^{3}$
- $-5x-2y{z}^{3}$
- $5x+2y{z}^{3}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}5\sqrt{x} & {z}^{3} \\ 2y & -\sqrt{x}\end{aligned}| & =5\sqrt{x}\cdot (-\sqrt{x})-{z}^{3}\cdot 2y \\  & =-5x-2y{z}^{3}\end{aligned}
$$

## Generated variant / radical_power / authored-operations

$|\begin{aligned}2\sqrt{x} & {z}^{2} \\ 3y & -\sqrt{x}\end{aligned}|=$

- $2x+3y{z}^{2}$
- $-2x+3y{z}^{2}$
- $-2x-3y{z}^{2}$
- $-2x$
- $-3y{z}^{2}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}2\sqrt{x} & {z}^{2} \\ 3y & -\sqrt{x}\end{aligned}| & =2\sqrt{x}\cdot (-\sqrt{x})-{z}^{2}\cdot 3y \\  & =-2x-3y{z}^{2}\end{aligned}
$$

## Generated variant / factored_bilinear / authored-operations

Calculate $det(H)$, if
    $H=[\begin{aligned}-8r & 5s \\ -8t & 5u\end{aligned}].$

- $40ru-40st$
- $40st$
- $-40ru-40st$
- $-40ru$
- $40(st-ru)$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(H) & =|\begin{aligned}-8r & 5s \\ -8t & 5u\end{aligned}| \\  & =-8r\cdot 5u-5s\cdot (-8t) \\  & =-40ru-(-40st) \\  & =-40ru+40st \\  & =40(st-ru)\end{aligned}
$$

## Generated variant / factored_bilinear / authored-operations

Calculate $det(H)$, if
    $H=[\begin{aligned}-8r & 2s \\ -8t & 2u\end{aligned}].$

- $-16ru$
- $16st$
- $16ru-16st$
- $16(st-ru)$
- $-16ru-16st$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(H) & =|\begin{aligned}-8r & 2s \\ -8t & 2u\end{aligned}| \\  & =-8r\cdot 2u-2s\cdot (-8t) \\  & =-16ru-(-16st) \\  & =-16ru+16st \\  & =16(st-ru)\end{aligned}
$$

## Generated variant / four_fractions / blank

Calculate $det(A)$ given that
$A=[\begin{aligned}\frac{5}{7} & -\frac{9}{4} \\ -\frac{9}{4} & \frac{8}{5}\end{aligned}].$

$det(A)=$
{{field-1}}

- $-\frac{439}{112}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(A) & =|\begin{aligned}\frac{5}{7} & -\frac{9}{4} \\ -\frac{9}{4} & \frac{8}{5}\end{aligned}| \\  & =\frac{5}{7}\cdot \frac{8}{5}-(-\frac{9}{4})\cdot (-\frac{9}{4}) \\  & =\frac{8}{7}-\frac{81}{16} \\  & =-\frac{439}{112}.\end{aligned}
$$

## Generated variant / four_fractions / blank

Calculate $det(A)$ given that
$A=[\begin{aligned}-\frac{9}{5} & -\frac{2}{7} \\ \frac{4}{3} & \frac{5}{2}\end{aligned}].$

$det(A)=$
{{field-1}}

- $-\frac{173}{42}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have

$$
\begin{aligned}\text{det}(A) & =|\begin{aligned}-\frac{9}{5} & -\frac{2}{7} \\ \frac{4}{3} & \frac{5}{2}\end{aligned}| \\  & =-\frac{9}{5}\cdot \frac{5}{2}-(-\frac{2}{7})\cdot \frac{4}{3} \\  & =-\frac{9}{2}-(-\frac{8}{21}) \\  & =-\frac{173}{42}.\end{aligned}
$$

## Generated variant / numeric_radical / observed-q-1088

What is $\begin{vmatrix}\sqrt{5} & 6 \\ 3 & 5\end{vmatrix}$?

- $3$
- $-5$
- $5\sqrt{5}-18$
- $-13$
- $23$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(A) & =|\begin{aligned}\sqrt{5} & 6 \\ 3 & 5\end{aligned}| \\  & =\sqrt{5}\cdot 5-6\cdot 3 \\  & =5\sqrt{5}-18\end{aligned}
$$

## Generated variant / numeric_radical / observed-q-1088

What is $\begin{vmatrix}\sqrt{2} & 4 \\ 2 & 2\end{vmatrix}$?

- $10$
- $-2$
- $2\sqrt{2}-8$
- $2$
- $-6$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(A) & =|\begin{aligned}\sqrt{2} & 4 \\ 2 & 2\end{aligned}| \\  & =\sqrt{2}\cdot 2-4\cdot 2 \\  & =2\sqrt{2}-8\end{aligned}
$$

## Generated variant / symbolic_radical / observed-q-1089

Calculate $det(Z)$, if
 $Z=[\begin{aligned}\sqrt{x} & y \\ {y}^{3} & \sqrt{x}\end{aligned}].$

- $x-{y}^{4}$
- $x-{y}^{3}$
- $2\sqrt{x}-{y}^{4}$
- $\sqrt{x}-2{y}^{4}$
- $x-2{y}^{3}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(Z) & =|\begin{aligned}\sqrt{x} & y \\ {y}^{3} & \sqrt{x}\end{aligned}| \\  & =\sqrt{x}\cdot \sqrt{x}-y\cdot {y}^{3} \\  & =x-{y}^{4}\end{aligned}
$$

## Generated variant / symbolic_radical / observed-q-1089

Calculate $det(Z)$, if
 $Z=[\begin{aligned}\sqrt{x} & y \\ {y}^{4} & \sqrt{x}\end{aligned}].$

- $2\sqrt{x}-{y}^{5}$
- $\sqrt{x}-2{y}^{5}$
- $x-{y}^{4}$
- $x-{y}^{5}$
- $x-2{y}^{4}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(Z) & =|\begin{aligned}\sqrt{x} & y \\ {y}^{4} & \sqrt{x}\end{aligned}| \\  & =\sqrt{x}\cdot \sqrt{x}-y\cdot {y}^{4} \\  & =x-{y}^{5}\end{aligned}
$$

## Generated variant / linear_power / observed-q-1083

$|\begin{aligned}5x & {y}^{3} \\ z & -2\end{aligned}|=$

- $10x-{y}^{3}z$
- $7$
- $-10x-{y}^{3}z$
- $-3$
- $10x-{y}^{3}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}5x & {y}^{3} \\ z & -2\end{aligned}| & =5x\cdot (-2)-{y}^{3}\cdot z \\  & =-10x-{y}^{3}z\end{aligned}
$$

## Generated variant / linear_power / observed-q-1083

$|\begin{aligned}6x & {y}^{3} \\ z & -2\end{aligned}|=$

- $-4$
- $12x-{y}^{3}z$
- $12x-{y}^{3}$
- $-12x-{y}^{3}z$
- $8$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}6x & {y}^{3} \\ z & -2\end{aligned}| & =6x\cdot (-2)-{y}^{3}\cdot z \\  & =-12x-{y}^{3}z\end{aligned}
$$

## Generated variant / easy_fraction / observed-q-1087

Calculate $det(T)$, if
    $T=[\begin{aligned}\frac{1}{5} & 3 \\ 4 & 10\end{aligned}].$

- $-12$
- $\frac{6}{5}$
- $-10$
- $14$
- $\frac{14}{5}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(T) & =|\begin{aligned}\frac{1}{5} & 3 \\ 4 & 10\end{aligned}| \\  & =\frac{1}{5}\cdot 10-3\cdot 4 \\  & =2-12 \\  & =-10\end{aligned}
$$

## Generated variant / easy_fraction / observed-q-1087

Calculate $det(T)$, if
    $T=[\begin{aligned}\frac{1}{6} & 2 \\ 3 & 6\end{aligned}].$

- $\frac{7}{5}$
- $-5$
- $-6$
- $7$
- $\frac{3}{5}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(T) & =|\begin{aligned}\frac{1}{6} & 2 \\ 3 & 6\end{aligned}| \\  & =\frac{1}{6}\cdot 6-2\cdot 3 \\  & =1-6 \\  & =-5\end{aligned}
$$

## Generated variant / shared_monomial / observed-q-127601

Calculate $det(C)$, if
    $C=[\begin{aligned}-2x & -6y \\ \frac{x}{6} & 7y\end{aligned}].$

- $14xy$
- $-\frac{3xy}{2}$
- $7xy$
- $-14xy$
- $-13xy$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}-2x & -6y \\ \frac{x}{6} & 7y\end{aligned}| \\  & =-2x\cdot 7y-(-6y)\cdot \frac{x}{6} \\  & =-14xy+xy \\  & =-13xy\end{aligned}
$$

## Generated variant / shared_monomial / observed-q-127601

Calculate $det(C)$, if
    $C=[\begin{aligned}-x & -6y \\ \frac{x}{3} & 6y\end{aligned}].$

- $3xy$
- $-6xy$
- $-3xy$
- $-4xy$
- $6xy$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}-x & -6y \\ \frac{x}{3} & 6y\end{aligned}| \\  & =-x\cdot 6y-(-6y)\cdot \frac{x}{3} \\  & =-6xy+2xy \\  & =-4xy\end{aligned}
$$

## Generated variant / factored_polynomial / observed-q-127603

Calculate $det(D)$, if
    $D=[\begin{aligned}5x & y \\ -2 & xy\end{aligned}].$

- $y(5{x}^{2}+2)$
- $6{y}^{2}x-2$
- $y(5{x}^{2}-6)$
- $6{x}^{2}y+6$
- $25{x}^{2}{y}^{2}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}5x & y \\ -2 & xy\end{aligned}| \\  & =5x\cdot xy-y\cdot (-2) \\  & =5{x}^{2}y+2y \\  & =y(5{x}^{2}+2)\end{aligned}
$$

## Generated variant / factored_polynomial / observed-q-127603

Calculate $det(D)$, if
    $D=[\begin{aligned}6x & y \\ -2 & xy\end{aligned}].$

- $y(6{x}^{2}+2)$
- $y(6{x}^{2}-7)$
- $36{x}^{2}{y}^{2}$
- $7{y}^{2}x-2$
- $7{x}^{2}y+7$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(D) & =|\begin{aligned}6x & y \\ -2 & xy\end{aligned}| \\  & =6x\cdot xy-y\cdot (-2) \\  & =6{x}^{2}y+2y \\  & =y(6{x}^{2}+2)\end{aligned}
$$

## Generated variant / radical_power / observed-q-69649

$|\begin{aligned}5\sqrt{x} & {z}^{3} \\ 2y & -\sqrt{x}\end{aligned}|=$

- $-5x-2{y}^{3}z$
- $-5x-2y{z}^{3}$
- $2x+5y{z}^{3}$
- $5x-2{z}^{3}y$
- $-2x-5y{z}^{3}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}5\sqrt{x} & {z}^{3} \\ 2y & -\sqrt{x}\end{aligned}| & =5\sqrt{x}\cdot (-\sqrt{x})-{z}^{3}\cdot 2y \\  & =-5x-2y{z}^{3}\end{aligned}
$$

## Generated variant / radical_power / observed-q-69649

$|\begin{aligned}6\sqrt{x} & {z}^{3} \\ 2y & -\sqrt{x}\end{aligned}|=$

- $6x-2{z}^{3}y$
- $-6x-2{y}^{3}z$
- $-2x-6y{z}^{3}$
- $2x+6y{z}^{3}$
- $-6x-2y{z}^{3}$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}|\begin{aligned}6\sqrt{x} & {z}^{3} \\ 2y & -\sqrt{x}\end{aligned}| & =6\sqrt{x}\cdot (-\sqrt{x})-{z}^{3}\cdot 2y \\  & =-6x-2y{z}^{3}\end{aligned}
$$

## Generated variant / factored_bilinear / observed-q-69650

Calculate $det(H)$, if
    $H=[\begin{aligned}-5r & 2s \\ -5t & 2u\end{aligned}].$

- $10ru-5st$
- $10(ru-st)$
- $2(5st-ru)$
- $10(st-ru)$
- $-10ru+5st$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(H) & =|\begin{aligned}-5r & 2s \\ -5t & 2u\end{aligned}| \\  & =-5r\cdot 2u-2s\cdot (-5t) \\  & =-10ru-(-10st) \\  & =-10ru+10st \\  & =10(st-ru)\end{aligned}
$$

## Generated variant / factored_bilinear / observed-q-69650

Calculate $det(H)$, if
    $H=[\begin{aligned}-6r & 2s \\ -6t & 2u\end{aligned}].$

- $12ru-6st$
- $2(6st-ru)$
- $-12ru+6st$
- $12(ru-st)$
- $12(st-ru)$

For a $2\times 2$ matrix, the determinant is given by the formula

$$
|\begin{aligned}a & b \\ c & d\end{aligned}|=ad-bc.
$$

Using the formula, we have:

$$
\begin{aligned}\text{det}(H) & =|\begin{aligned}-6r & 2s \\ -6t & 2u\end{aligned}| \\  & =-6r\cdot 2u-2s\cdot (-6t) \\  & =-12ru-(-12st) \\  & =-12ru+12st \\  & =12(st-ru)\end{aligned}
$$
