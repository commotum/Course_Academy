# Determinant unknown review

All answers and fixed worked solutions are included for author review. Originals are immutable capture text. Generated variants are labeled with evidence replay versus authored default banks.

## Original q-9657 (unrated)

Given that the determinant of
$\begin{bmatrix}2 & -1 & 3 \\ x & 2 & 4 \\ -2 & 1 & x + 3\end{bmatrix}$
is $8$, find all the possible values of $x$.

Field `selection`
- $5$ and $6$ only
- $2$ and $8$ only
- $8$ only
- $-8$ and $-2$ only
- $5$ only

**Original worked solution**

No source worked solution or correct designation is present. See independently verified repair in template-extraction.md.

### Generated evidence-profile variant q-9657 seed 101

Given that the determinant of
$\begin{bmatrix}2 & -1 & 3 \\ x & 4 & 4 \\ -5 & 1 & x + 3\end{bmatrix}$
is $72$, find all the possible values of $x$.

Field `selection` (radio)
- $5$ and $12$ only
- $-12$ and $-2$ only **correct**
- $72$ only
- $2$ and $72$ only
- $5$ only

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}2 & -1 & 3 \\ x & 4 & 4 \\ -5 & 1 & x + 3\end{aligned}| & =2|\begin{aligned}4 & 4 \\ 1 & x + 3\end{aligned}|-(-1)|\begin{aligned}x & 4 \\ -5 & x + 3\end{aligned}|+3|\begin{aligned}x & 4 \\ -5 & 1\end{aligned}| \\  & =2\big(4 x + 12-(4)\big)-(-1)\big(x (x + 3)-(-20)\big)+3\big(x-(-20)\big) \\  & =2(4 x + 8)-(-1)(x^{2} + 3 x + 20)+3(x + 20) \\  & =x^{2} + 14 x + 96\end{aligned}
$$

Since the determinant of the matrix is $72,$ we have:

$$
\begin{aligned}x^{2} + 14 x + 96 & =72 \\ x^{2} + 14 x + 24 & =0 \\ x & =\frac{-(14)\pm\sqrt{(14)^2-4\cdot 1\cdot (24)}}{2\cdot 1} \\  & =\frac{-14\pm\sqrt{100}}{2} \\  & =\frac{-14\pm 10}{2} \\  & =-12,-2\end{aligned}
$$

Therefore, the solutions are $x=-12$ and $x=-2.$

### Generated evidence-profile variant q-9657 seed 202

Given that the determinant of
$\begin{bmatrix}2 & -1 & 3 \\ x & -2 & 4 \\ -2 & 1 & x - 2\end{bmatrix}$
is $0$, find all the possible values of $x$.

Field `selection` (radio)
- $0$ only
- $5$ and $-6$ only
- $2$ and $0$ only
- $5$ only
- $-1$ and $4$ only **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}2 & -1 & 3 \\ x & -2 & 4 \\ -2 & 1 & x - 2\end{aligned}| & =2|\begin{aligned}-2 & 4 \\ 1 & x - 2\end{aligned}|-(-1)|\begin{aligned}x & 4 \\ -2 & x - 2\end{aligned}|+3|\begin{aligned}x & -2 \\ -2 & 1\end{aligned}| \\  & =2\big(4 - 2 x-(4)\big)-(-1)\big(x (x - 2)-(-8)\big)+3\big(x-(4)\big) \\  & =2(- 2 x)-(-1)(x^{2} - 2 x + 8)+3(x - 4) \\  & =x^{2} - 3 x - 4\end{aligned}
$$

Since the determinant of the matrix is $0,$ we have:

$$
\begin{aligned}x^{2} - 3 x - 4 & =0 \\ x^{2} - 3 x - 4 & =0 \\ x & =\frac{-(-3)\pm\sqrt{(-3)^2-4\cdot 1\cdot (-4)}}{2\cdot 1} \\  & =\frac{3\pm\sqrt{25}}{2} \\  & =\frac{3\pm 5}{2} \\  & =-1,4\end{aligned}
$$

Therefore, the solutions are $x=-1$ and $x=4.$

### Generated authored default bank q-9657 seed 303

Given that the determinant of
$\begin{bmatrix}2 & 3 & 3 \\ x & 2 & 4 \\ -2 & 2 & x + 3\end{bmatrix}$
is $-130$, find all the possible values of $x$.

Field `selection` (radio)
- $\frac{19}{3}$ only
- $0$ and $\frac{1}{3}$ only
- $-6$ only
- $6$ and $- \frac{19}{3}$ only
- $-6$ and $\frac{19}{3}$ only **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}2 & 3 & 3 \\ x & 2 & 4 \\ -2 & 2 & x + 3\end{aligned}| & =2|\begin{aligned}2 & 4 \\ 2 & x + 3\end{aligned}|-3|\begin{aligned}x & 4 \\ -2 & x + 3\end{aligned}|+3|\begin{aligned}x & 2 \\ -2 & 2\end{aligned}| \\  & =2\big(2 x + 6-(8)\big)-3\big(x (x + 3)-(-8)\big)+3\big(2 x-(-4)\big) \\  & =2(2 x - 2)-3(x^{2} + 3 x + 8)+3(2 x + 4) \\  & =- 3 x^{2} + x - 16\end{aligned}
$$

Since the determinant of the matrix is $-130,$ we have:

$$
\begin{aligned}- 3 x^{2} + x - 16 & =-130 \\ 3 x^{2} - x - 114 & =0 \\ x & =\frac{-(-1)\pm\sqrt{(-1)^2-4\cdot 3\cdot (-114)}}{2\cdot 3} \\  & =\frac{1\pm\sqrt{1369}}{6} \\  & =\frac{1\pm 37}{6} \\  & =-6,\frac{19}{3}\end{aligned}
$$

Therefore, the solutions are $x=-6$ and $x=\frac{19}{3}.$

## Original q-9669 (:question.difficulty/easy)

Find the possible values of the constant $k$ given that the matrix $[\begin{aligned}2 & 1 & -4 \\ 2k+1 & 3 & k \\ 1 & 0 & 1\end{aligned}]$ is singular.

Field `selection`
- 17 **original correct**
- -6
- -1
- 5
- 6

**Original worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$ 

$$
\begin{aligned}|\begin{aligned}2 & 1 & -4 \\ 2k+1 & 3 & k \\ 1 & 0 & 1\end{aligned}| & =2|\begin{aligned}3 & k \\ 0 & 1\end{aligned}|-1|\begin{aligned}2k+1 & k \\ 1 & 1\end{aligned}|-4|\begin{aligned}2k+1 & 3 \\ 1 & 0\end{aligned}| \\  & =2(3-0)-(2k+1-k)-4(0-3) \\  & =2\cdot 3-(k+1)-4\cdot (-3) \\  & =6-k-1+12 \\  & =17-k\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}17-k & =0 \\ k & =17\end{aligned}
$$

Therefore, the solution is $k=17.$

### Generated evidence-profile variant q-9669 seed 101

Find the possible values of the constant $k$ given that the matrix $[\begin{aligned}2 & 1 & -4 \\ 2 k + 1 & 5 & k \\ -2 & 0 & 1\end{aligned}]$ is singular.

Field `selection` (radio)
- - \frac{31}{4} **correct**
- 5
- -1
- -10
- 10

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}2 & 1 & -4 \\ 2 k + 1 & 5 & k \\ -2 & 0 & 1\end{aligned}| & =2|\begin{aligned}5 & k \\ 0 & 1\end{aligned}|-1|\begin{aligned}2 k + 1 & k \\ -2 & 1\end{aligned}|+(-4)|\begin{aligned}2 k + 1 & 5 \\ -2 & 0\end{aligned}| \\  & =2\big(5-(0)\big)-1\big(2 k + 1-(- 2 k)\big)+(-4)\big(0-(-10)\big) \\  & =2(5)-1(4 k + 1)+(-4)(10) \\  & =10- 4 k - 1-40 \\  & =- 4 k - 31\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}- 4 k - 31 & =0 \\ k & =- \frac{31}{4}\end{aligned}
$$

Therefore, the solution is $k=- \frac{31}{4}.$

### Generated evidence-profile variant q-9669 seed 202

Find the possible values of the constant $k$ given that the matrix $[\begin{aligned}2 & 2 & -4 \\ 2 k + 1 & 3 & k \\ -5 & 0 & 1\end{aligned}]$ is singular.

Field `selection` (radio)
- -1
- -4 **correct**
- -6
- 6
- 5

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}2 & 2 & -4 \\ 2 k + 1 & 3 & k \\ -5 & 0 & 1\end{aligned}| & =2|\begin{aligned}3 & k \\ 0 & 1\end{aligned}|-2|\begin{aligned}2 k + 1 & k \\ -5 & 1\end{aligned}|+(-4)|\begin{aligned}2 k + 1 & 3 \\ -5 & 0\end{aligned}| \\  & =2\big(3-(0)\big)-2\big(2 k + 1-(- 5 k)\big)+(-4)\big(0-(-15)\big) \\  & =2(3)-2(7 k + 1)+(-4)(15) \\  & =6- 14 k - 2-60 \\  & =- 14 k - 56\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}- 14 k - 56 & =0 \\ k & =-4\end{aligned}
$$

Therefore, the solution is $k=-4.$

### Generated authored default bank q-9669 seed 303

Find the possible values of the constant $k$ given that the matrix $[\begin{aligned}2 & -2 & -4 \\ 2 k + 1 & 3 & k \\ -4 & 0 & 1\end{aligned}]$ is singular.

Field `selection` (radio)
- 12
- -40
- 40
- - \frac{10}{3}
- \frac{10}{3} **correct**

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}2 & -2 & -4 \\ 2 k + 1 & 3 & k \\ -4 & 0 & 1\end{aligned}| & =2|\begin{aligned}3 & k \\ 0 & 1\end{aligned}|-(-2)|\begin{aligned}2 k + 1 & k \\ -4 & 1\end{aligned}|+(-4)|\begin{aligned}2 k + 1 & 3 \\ -4 & 0\end{aligned}| \\  & =2\big(3-(0)\big)-(-2)\big(2 k + 1-(- 4 k)\big)+(-4)\big(0-(-12)\big) \\  & =2(3)-(-2)(6 k + 1)+(-4)(12) \\  & =6+12 k + 2-48 \\  & =12 k - 40\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}12 k - 40 & =0 \\ k & =\frac{10}{3}\end{aligned}
$$

Therefore, the solution is $k=\frac{10}{3}.$

## Original q-9852 (unrated)

Find the possible values of the constant $k$ given that the matrix
$\begin{bmatrix}0 & 7 & 4k \\ 0 & 9 & 5k \\ 0 & 11 & 6k\end{bmatrix}$ is singular.

Field `selection`
- Any value of $k$
- $10$ only
- $0$ only
- $2$ only
- $3$ and $-3$ only

**Original worked solution**

No source worked solution or correct designation is present. See independently verified repair in template-extraction.md.

### Generated evidence-profile variant q-9852 seed 101

Find the possible values of the constant $k$ given that the matrix
$\begin{bmatrix}0 & 10 & 4 k \\ 0 & 7 & 5 k \\ 0 & 9 & 6 k\end{bmatrix}$ is singular.

Field `selection` (radio)
- Any value of $k$ **correct**
- $2$ only
- $0$ only
- $8$ only
- $3$ and $-3$ only

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}0 & 10 & 4 k \\ 0 & 7 & 5 k \\ 0 & 9 & 6 k\end{aligned}| & =0|\begin{aligned}7 & 5 k \\ 9 & 6 k\end{aligned}|-10|\begin{aligned}0 & 5 k \\ 0 & 6 k\end{aligned}|+4 k|\begin{aligned}0 & 7 \\ 0 & 9\end{aligned}| \\  & =0\big(42 k-(45 k)\big)-10\big(0-(0)\big)+4 k\big(0-(0)\big) \\  & =0(- 3 k)-10(0)+4 k(0) \\  & =0\end{aligned}
$$

Therefore, this matrix is singular for all values of $k.$

### Generated evidence-profile variant q-9852 seed 202

Find the possible values of the constant $k$ given that the matrix
$\begin{bmatrix}0 & 12 & 4 k \\ 0 & 9 & 5 k \\ 0 & 8 & 6 k\end{bmatrix}$ is singular.

Field `selection` (radio)
- $0$ only
- Any value of $k$ **correct**
- $\frac{17}{2}$ only
- $3$ and $-3$ only
- $2$ only

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}0 & 12 & 4 k \\ 0 & 9 & 5 k \\ 0 & 8 & 6 k\end{aligned}| & =0|\begin{aligned}9 & 5 k \\ 8 & 6 k\end{aligned}|-12|\begin{aligned}0 & 5 k \\ 0 & 6 k\end{aligned}|+4 k|\begin{aligned}0 & 9 \\ 0 & 8\end{aligned}| \\  & =0\big(54 k-(40 k)\big)-12\big(0-(0)\big)+4 k\big(0-(0)\big) \\  & =0(14 k)-12(0)+4 k(0) \\  & =0\end{aligned}
$$

Therefore, this matrix is singular for all values of $k.$

### Generated authored default bank q-9852 seed 303

Find the possible values of the constant $k$ given that the matrix
$\begin{bmatrix}0 & 5 & 4 k \\ 0 & 5 & 5 k \\ 0 & 3 & 6 k\end{bmatrix}$ is singular.

Field `selection` (radio)
- $1$ only
- $\frac{1}{2}$ only
- $\frac{5}{4}$ only
- $0$ only
- Any value of $k$ **correct**

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}0 & 5 & 4 k \\ 0 & 5 & 5 k \\ 0 & 3 & 6 k\end{aligned}| & =0|\begin{aligned}5 & 5 k \\ 3 & 6 k\end{aligned}|-5|\begin{aligned}0 & 5 k \\ 0 & 6 k\end{aligned}|+4 k|\begin{aligned}0 & 5 \\ 0 & 3\end{aligned}| \\  & =0\big(30 k-(15 k)\big)-5\big(0-(0)\big)+4 k\big(0-(0)\big) \\  & =0(15 k)-5(0)+4 k(0) \\  & =0\end{aligned}
$$

Therefore, this matrix is singular for all values of $k.$

## Original q-128500 (:question.difficulty/easy)

Given that
$B=[\begin{aligned}1 & 2 & -5 \\ 1 & 2 & 1 \\ y & 2 & 1\end{aligned}]$
and $det(B)=12,$ find the value of $y.$

Field `selection`
- -8
- 10
- 13
- 2 **original correct**
- -5

**Original worked solution**

Let's use our formula to find an expression for the determinant in terms of $y:$

$$
\begin{aligned}\text{det}(B) & =|\begin{aligned}1 & 2 & -5 \\ 1 & 2 & 1 \\ y & 2 & 1\end{aligned}| \\  & =1|\begin{aligned}2 & 1 \\ 2 & 1\end{aligned}|-2|\begin{aligned}1 & 1 \\ y & 1\end{aligned}|-5|\begin{aligned}1 & 2 \\ y & 2\end{aligned}| \\  & =0-2\cdot (1-y)-5\cdot (2-2y) \\  & =12y-12\end{aligned}
$$

Since the determinant of the matrix is $12,$ we have:

$$
\begin{aligned}12y-12 & =12 \\ 12y & =24 \\ y & =2\end{aligned}
$$

### Generated evidence-profile variant q-128500 seed 101

Given that
$B=[\begin{aligned}-2 & 2 & -5 \\ 1 & 2 & 1 \\ y & 2 & -1\end{aligned}]$
and $det(B)=-9,$ find the value of $y.$

Field `selection` (radio)
- -8
- - \frac{3}{4} **correct**
- -11
- 10
- -5

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $y:$

$$
\begin{aligned}\text{det}(B) & =|\begin{aligned}-2 & 2 & -5 \\ 1 & 2 & 1 \\ y & 2 & -1\end{aligned}| \\  & =(-2)|\begin{aligned}2 & 1 \\ 2 & -1\end{aligned}|-2|\begin{aligned}1 & 1 \\ y & -1\end{aligned}|+(-5)|\begin{aligned}1 & 2 \\ y & 2\end{aligned}| \\  & =(-2)(-4)-2(- y - 1)+(-5)(2 - 2 y) \\  & =12 y\end{aligned}
$$

Since the determinant of the matrix is $-9,$ we have:

$$
\begin{aligned}12 y & =-9 \\ 12 y & =-9 \\ y & =- \frac{3}{4}\end{aligned}
$$

### Generated evidence-profile variant q-128500 seed 202

Given that
$B=[\begin{aligned}1 & 2 & -5 \\ -2 & 2 & 1 \\ y & 2 & -2\end{aligned}]$
and $det(B)=51,$ find the value of $y.$

Field `selection` (radio)
- 52
- -8
- 10
- -5
- \frac{15}{4} **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $y:$

$$
\begin{aligned}\text{det}(B) & =|\begin{aligned}1 & 2 & -5 \\ -2 & 2 & 1 \\ y & 2 & -2\end{aligned}| \\  & =1|\begin{aligned}2 & 1 \\ 2 & -2\end{aligned}|-2|\begin{aligned}-2 & 1 \\ y & -2\end{aligned}|+(-5)|\begin{aligned}-2 & 2 \\ y & 2\end{aligned}| \\  & =1(-6)-2(4 - y)+(-5)(- 2 y - 4) \\  & =12 y + 6\end{aligned}
$$

Since the determinant of the matrix is $51,$ we have:

$$
\begin{aligned}12 y + 6 & =51 \\ 12 y & =45 \\ y & =\frac{15}{4}\end{aligned}
$$

### Generated authored default bank q-128500 seed 303

Given that
$B=[\begin{aligned}1 & 2 & -5 \\ -2 & 2 & -4 \\ y & 2 & 1\end{aligned}]$
and $det(B)=16,$ find the value of $y.$

Field `selection` (radio)
- 2
- 18
- -18
- 9
- -9 **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $y:$

$$
\begin{aligned}\text{det}(B) & =|\begin{aligned}1 & 2 & -5 \\ -2 & 2 & -4 \\ y & 2 & 1\end{aligned}| \\  & =1|\begin{aligned}2 & -4 \\ 2 & 1\end{aligned}|-2|\begin{aligned}-2 & -4 \\ y & 1\end{aligned}|+(-5)|\begin{aligned}-2 & 2 \\ y & 2\end{aligned}| \\  & =1(10)-2(4 y - 2)+(-5)(- 2 y - 4) \\  & =2 y + 34\end{aligned}
$$

Since the determinant of the matrix is $16,$ we have:

$$
\begin{aligned}2 y + 34 & =16 \\ 2 y & =-18 \\ y & =-9\end{aligned}
$$

## Original q-128502 (:question.difficulty/easy)

Given that 
$C=[\begin{aligned}2 & 3 & 1 \\ -1 & q & 5 \\ 0 & -5 & 1\end{aligned}]$ 
and $det(C)=28,$ find the value of $q.$

Field `selection`
- -10
- 20
- 2
- 12
- -15 **original correct**

**Original worked solution**

Let's use our formula to find an expression for the determinant in terms of $q:$

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}2 & 3 & 1 \\ -1 & q & 5 \\ 0 & -5 & 1\end{aligned}| \\  & =2|\begin{aligned}q & 5 \\ -5 & 1\end{aligned}|-3|\begin{aligned}-1 & 5 \\ 0 & 1\end{aligned}|+1|\begin{aligned}-1 & q \\ 0 & -5\end{aligned}| \\  & =2\cdot (q+25)-3\cdot (-1)+5 \\  & =2q+58\end{aligned}
$$

Since the determinant of the matrix is $28,$ we have:

$$
\begin{aligned}2q+58 & =28 \\ 2q & =-30 \\ q & =-15\end{aligned}
$$

### Generated evidence-profile variant q-128502 seed 101

Given that 
$C=[\begin{aligned}2 & 3 & -5 \\ -1 & q & 3 \\ 0 & -5 & 1\end{aligned}]$ 
and $det(C)=78,$ find the value of $q.$

Field `selection` (radio)
- -6
- 12
- 2
- 20
- 35 **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $q:$

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}2 & 3 & -5 \\ -1 & q & 3 \\ 0 & -5 & 1\end{aligned}| \\  & =2|\begin{aligned}q & 3 \\ -5 & 1\end{aligned}|-3|\begin{aligned}-1 & 3 \\ 0 & 1\end{aligned}|+(-5)|\begin{aligned}-1 & q \\ 0 & -5\end{aligned}| \\  & =2(q + 15)-3(-1)+(-5)(5) \\  & =2 q + 8\end{aligned}
$$

Since the determinant of the matrix is $78,$ we have:

$$
\begin{aligned}2 q + 8 & =78 \\ 2 q & =70 \\ q & =35\end{aligned}
$$

### Generated evidence-profile variant q-128502 seed 202

Given that 
$C=[\begin{aligned}2 & 3 & 1 \\ -2 & q & 5 \\ 0 & 2 & 1\end{aligned}]$ 
and $det(C)=0,$ find the value of $q.$

Field `selection` (radio)
- 2
- -20
- -8
- 9 **correct**
- 12

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $q:$

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}2 & 3 & 1 \\ -2 & q & 5 \\ 0 & 2 & 1\end{aligned}| \\  & =2|\begin{aligned}q & 5 \\ 2 & 1\end{aligned}|-3|\begin{aligned}-2 & 5 \\ 0 & 1\end{aligned}|+1|\begin{aligned}-2 & q \\ 0 & 2\end{aligned}| \\  & =2(q - 10)-3(-2)+1(-4) \\  & =2 q - 18\end{aligned}
$$

Since the determinant of the matrix is $0,$ we have:

$$
\begin{aligned}2 q - 18 & =0 \\ 2 q & =18 \\ q & =9\end{aligned}
$$

### Generated authored default bank q-128502 seed 303

Given that 
$C=[\begin{aligned}2 & -2 & 1 \\ -1 & q & 5 \\ 0 & -4 & 1\end{aligned}]$ 
and $det(C)=16,$ find the value of $q.$

Field `selection` (radio)
- 2
- 26
- -26
- 13
- -13 **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $q:$

$$
\begin{aligned}\text{det}(C) & =|\begin{aligned}2 & -2 & 1 \\ -1 & q & 5 \\ 0 & -4 & 1\end{aligned}| \\  & =2|\begin{aligned}q & 5 \\ -4 & 1\end{aligned}|-(-2)|\begin{aligned}-1 & 5 \\ 0 & 1\end{aligned}|+1|\begin{aligned}-1 & q \\ 0 & -4\end{aligned}| \\  & =2(q + 20)-(-2)(-1)+1(4) \\  & =2 q + 42\end{aligned}
$$

Since the determinant of the matrix is $16,$ we have:

$$
\begin{aligned}2 q + 42 & =16 \\ 2 q & =-26 \\ q & =-13\end{aligned}
$$

## Original q-130575 (:question.difficulty/moderate)

Given that the determinant of
$[\begin{aligned}2 & 1 & 5 \\ 2 & 3 & z \\ z & -1 & 1\end{aligned}]$
is $-48$, find all the possible values of $z.$

Field `selection`
- $6$ and $7$ only **original correct**
- $3$  only
- $-2$ and $3$ only
- $5$ and $-5$ only
- $5$ and $6$ only

**Original worked solution**

Let's use our formula to find an expression for the determinant in terms of $z:$

$$
\begin{aligned}|\begin{aligned}2 & 1 & 5 \\ 2 & 3 & z \\ z & -1 & 1\end{aligned}| & =2|\begin{aligned}3 & z \\ -1 & 1\end{aligned}|-1|\begin{aligned}2 & z \\ z & 1\end{aligned}|+5|\begin{aligned}2 & 3 \\ z & -1\end{aligned}| \\  & =2(3+z)-(2-{z}^{2})+5(-2-3z) \\  & =6+2z-2+{z}^{2}-10-15z \\  & ={z}^{2}-13z-6\end{aligned}
$$

Since the determinant of the matrix is $-48,$ we have:

$$
\begin{aligned}{z}^{2}-13z-6 & =-48 \\ {z}^{2}-13z+42 & =0 \\ z & =\frac{-(-13)\pm \sqrt{{13}^{2}-4\cdot 1\cdot 42}}{2\cdot 1} \\  & =\frac{13\pm \sqrt{1}}{2} \\  & =\frac{13\pm 1}{2} \\  & =6,7\end{aligned}
$$

Therefore, the solutions are $z=6$ and $z=7.$

### Generated evidence-profile variant q-130575 seed 101

Given that the determinant of
$[\begin{aligned}2 & 1 & -5 \\ 2 & 3 & z \\ z & -1 & 1\end{aligned}]$
is $214$, find all the possible values of $z.$

Field `selection` (radio)
- $-25$ and $8$ only **correct**
- $-5$ and $5$ only
- $-2$ and $3$ only
- $3$  only
- $-5$ and $6$ only

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $z:$

$$
\begin{aligned}|\begin{aligned}2 & 1 & -5 \\ 2 & 3 & z \\ z & -1 & 1\end{aligned}| & =2|\begin{aligned}3 & z \\ -1 & 1\end{aligned}|-1|\begin{aligned}2 & z \\ z & 1\end{aligned}|+(-5)|\begin{aligned}2 & 3 \\ z & -1\end{aligned}| \\  & =2(z + 3)-1(2 - z^{2})+(-5)(- 3 z - 2) \\  & =2 z + 6+z^{2} - 2+15 z + 10 \\  & =z^{2} + 17 z + 14\end{aligned}
$$

Since the determinant of the matrix is $214,$ we have:

$$
\begin{aligned}z^{2} + 17 z + 14 & =214 \\ z^{2} + 17 z - 200 & =0 \\ z & =\frac{-(17)\pm\sqrt{(17)^2-4\cdot 1\cdot (-200)}}{2\cdot 1} \\  & =\frac{-17\pm\sqrt{1089}}{2} \\  & =\frac{-17\pm 33}{2} \\  & =-25,8\end{aligned}
$$

Therefore, the solutions are $z=-25$ and $z=8.$

### Generated evidence-profile variant q-130575 seed 202

Given that the determinant of
$[\begin{aligned}2 & 1 & 5 \\ -2 & 3 & z \\ z & 2 & 1\end{aligned}]$
is $30$, find all the possible values of $z.$

Field `selection` (radio)
- $1$ and $3$ only
- $-2$ and $21$ only **correct**
- $3$  only
- $5$ and $6$ only
- $5$ and $-5$ only

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $z:$

$$
\begin{aligned}|\begin{aligned}2 & 1 & 5 \\ -2 & 3 & z \\ z & 2 & 1\end{aligned}| & =2|\begin{aligned}3 & z \\ 2 & 1\end{aligned}|-1|\begin{aligned}-2 & z \\ z & 1\end{aligned}|+5|\begin{aligned}-2 & 3 \\ z & 2\end{aligned}| \\  & =2(3 - 2 z)-1(- z^{2} - 2)+5(- 3 z - 4) \\  & =6 - 4 z+z^{2} + 2- 15 z - 20 \\  & =z^{2} - 19 z - 12\end{aligned}
$$

Since the determinant of the matrix is $30,$ we have:

$$
\begin{aligned}z^{2} - 19 z - 12 & =30 \\ z^{2} - 19 z - 42 & =0 \\ z & =\frac{-(-19)\pm\sqrt{(-19)^2-4\cdot 1\cdot (-42)}}{2\cdot 1} \\  & =\frac{19\pm\sqrt{529}}{2} \\  & =\frac{19\pm 23}{2} \\  & =-2,21\end{aligned}
$$

Therefore, the solutions are $z=-2$ and $z=21.$

### Generated authored default bank q-130575 seed 303

Given that the determinant of
$[\begin{aligned}2 & 1 & 5 \\ 2 & 2 & z \\ z & -1 & -3\end{aligned}]$
is $-31$, find all the possible values of $z.$

Field `selection` (radio)
- $5$ only
- $0$ and $8$ only
- $3$ only
- $-3$ and $-5$ only
- $3$ and $5$ only **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $z:$

$$
\begin{aligned}|\begin{aligned}2 & 1 & 5 \\ 2 & 2 & z \\ z & -1 & -3\end{aligned}| & =2|\begin{aligned}2 & z \\ -1 & -3\end{aligned}|-1|\begin{aligned}2 & z \\ z & -3\end{aligned}|+5|\begin{aligned}2 & 2 \\ z & -1\end{aligned}| \\  & =2(z - 6)-1(- z^{2} - 6)+5(- 2 z - 2) \\  & =2 z - 12+z^{2} + 6- 10 z - 10 \\  & =z^{2} - 8 z - 16\end{aligned}
$$

Since the determinant of the matrix is $-31,$ we have:

$$
\begin{aligned}z^{2} - 8 z - 16 & =-31 \\ z^{2} - 8 z + 15 & =0 \\ z & =\frac{-(-8)\pm\sqrt{(-8)^2-4\cdot 1\cdot (15)}}{2\cdot 1} \\  & =\frac{8\pm\sqrt{4}}{2} \\  & =\frac{8\pm 2}{2} \\  & =3,5\end{aligned}
$$

Therefore, the solutions are $z=3$ and $z=5.$

## Original q-130580 (:question.difficulty/moderate)

Given that the determinant of
$[\begin{aligned}x & 2x & 3 \\ 5 & x & 7 \\ 3 & 2 & 1\end{aligned}]$
is $22$, find all the possible values of $x.$

Field `selection`
- $8$ and $3$ only
- $7$ only
- $5$ and $3$ only
- $-8$ and $-1$ only **original correct**
- $-5$ and $-3$ only

**Original worked solution**

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}x & 2x & 3 \\ 5 & x & 7 \\ 3 & 2 & 1\end{aligned}| & =x|\begin{aligned}x & 7 \\ 2 & 1\end{aligned}|-2x|\begin{aligned}5 & 7 \\ 3 & 1\end{aligned}|+3|\begin{aligned}5 & x \\ 3 & 2\end{aligned}| \\  & =x(x-14)-2x(5-21)+3(10-3x) \\  & ={x}^{2}-14x+32x+30-9x \\  & ={x}^{2}+9x+30\end{aligned}
$$

Since the determinant of the matrix is $22,$ we have:

$$
\begin{aligned}{x}^{2}+9x+30 & =22 \\ {x}^{2}+9x+8 & =0 \\ x & =\frac{-9\pm \sqrt{{9}^{2}-4\cdot 1\cdot 8}}{2\cdot 1} \\  & =\frac{-9\pm \sqrt{49}}{2} \\  & =\frac{-9\pm 7}{2} \\  & =-8,-1\end{aligned}
$$

Therefore, the solutions are $x=-8$ and $x=-1.$

### Generated evidence-profile variant q-130580 seed 101

Given that the determinant of
$[\begin{aligned}x & 2 x & 3 \\ 5 & x & -5 \\ 3 & 3 & 1\end{aligned}]$
is $-163$, find all the possible values of $x.$

Field `selection` (radio)
- $-8$ and $3$ only
- $8$ and $26$ only **correct**
- $5$ and $3$ only
- $-5$ only
- $-5$ and $-3$ only

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}x & 2 x & 3 \\ 5 & x & -5 \\ 3 & 3 & 1\end{aligned}| & =x|\begin{aligned}x & -5 \\ 3 & 1\end{aligned}|-2 x|\begin{aligned}5 & -5 \\ 3 & 1\end{aligned}|+3|\begin{aligned}5 & x \\ 3 & 3\end{aligned}| \\  & =x(x + 15)-2 x(20)+3(15 - 3 x) \\  & =x^{2} + 15 x- 40 x+45 - 9 x \\  & =x^{2} - 34 x + 45\end{aligned}
$$

Since the determinant of the matrix is $-163,$ we have:

$$
\begin{aligned}x^{2} - 34 x + 45 & =-163 \\ x^{2} - 34 x + 208 & =0 \\ x & =\frac{-(-34)\pm\sqrt{(-34)^2-4\cdot 1\cdot (208)}}{2\cdot 1} \\  & =\frac{34\pm\sqrt{324}}{2} \\  & =\frac{34\pm 18}{2} \\  & =8,26\end{aligned}
$$

Therefore, the solutions are $x=8$ and $x=26.$

### Generated evidence-profile variant q-130580 seed 202

Given that the determinant of
$[\begin{aligned}x & 2 x & 3 \\ 5 & x & 7 \\ -2 & 2 & 2\end{aligned}]$
is $150$, find all the possible values of $x.$

Field `selection` (radio)
- $5$ and $3$ only
- $2$ and $3$ only
- $7$ only
- $-5$ and $-3$ only
- $-2$ and $30$ only **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}x & 2 x & 3 \\ 5 & x & 7 \\ -2 & 2 & 2\end{aligned}| & =x|\begin{aligned}x & 7 \\ 2 & 2\end{aligned}|-2 x|\begin{aligned}5 & 7 \\ -2 & 2\end{aligned}|+3|\begin{aligned}5 & x \\ -2 & 2\end{aligned}| \\  & =x(2 x - 14)-2 x(24)+3(2 x + 10) \\  & =2 x^{2} - 14 x- 48 x+6 x + 30 \\  & =2 x^{2} - 56 x + 30\end{aligned}
$$

Since the determinant of the matrix is $150,$ we have:

$$
\begin{aligned}2 x^{2} - 56 x + 30 & =150 \\ 2 x^{2} - 56 x - 120 & =0 \\ x & =\frac{-(-56)\pm\sqrt{(-56)^2-4\cdot 2\cdot (-120)}}{2\cdot 2} \\  & =\frac{56\pm\sqrt{4096}}{4} \\  & =\frac{56\pm 64}{4} \\  & =-2,30\end{aligned}
$$

Therefore, the solutions are $x=-2$ and $x=30.$

### Generated authored default bank q-130580 seed 303

Given that the determinant of
$[\begin{aligned}x & 2 x & 3 \\ 5 & x & 7 \\ 3 & 2 & -3\end{aligned}]$
is $200$, find all the possible values of $x.$

Field `selection` (radio)
- $\frac{34}{3}$ only
- $0$ and $\frac{49}{3}$ only
- $5$ only
- $-5$ and $- \frac{34}{3}$ only
- $5$ and $\frac{34}{3}$ only **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}x & 2 x & 3 \\ 5 & x & 7 \\ 3 & 2 & -3\end{aligned}| & =x|\begin{aligned}x & 7 \\ 2 & -3\end{aligned}|-2 x|\begin{aligned}5 & 7 \\ 3 & -3\end{aligned}|+3|\begin{aligned}5 & x \\ 3 & 2\end{aligned}| \\  & =x(- 3 x - 14)-2 x(-36)+3(10 - 3 x) \\  & =- 3 x^{2} - 14 x+72 x+30 - 9 x \\  & =- 3 x^{2} + 49 x + 30\end{aligned}
$$

Since the determinant of the matrix is $200,$ we have:

$$
\begin{aligned}- 3 x^{2} + 49 x + 30 & =200 \\ 3 x^{2} - 49 x + 170 & =0 \\ x & =\frac{-(-49)\pm\sqrt{(-49)^2-4\cdot 3\cdot (170)}}{2\cdot 3} \\  & =\frac{49\pm\sqrt{361}}{6} \\  & =\frac{49\pm 19}{6} \\  & =5,\frac{34}{3}\end{aligned}
$$

Therefore, the solutions are $x=5$ and $x=\frac{34}{3}.$

## Original q-130620 (:question.difficulty/easy)

Find the possible values of the constant $x$ given that the matrix $[\begin{aligned}3 & 5 & 8 \\ 1 & 1 & 2 \\ x & -1 & -x\end{aligned}]$ is singular.

Field `selection`
- \frac{1}{2} **original correct**
- \frac{7}{4}
- 8
- 5
- -9

**Original worked solution**

First, let's use our formula to find an expression for the determinant in terms of $x:$ 

$$
\begin{aligned}|\begin{aligned}3 & 5 & 8 \\ 1 & 1 & 2 \\ x & -1 & -x\end{aligned}| & =3|\begin{aligned}1 & 2 \\ -1 & -x\end{aligned}|-5|\begin{aligned}1 & 2 \\ x & -x\end{aligned}|+8|\begin{aligned}1 & 1 \\ x & -1\end{aligned}| \\  & =3(-x+2)-5(-x-2x)+8(-1-x) \\  & =-3x+6+15x-8-8x \\  & =4x-2\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}4x-2 & =0 \\ x & =\frac{1}{2}\end{aligned}
$$

Therefore, the solution is $x=\frac{1}{2}.$

### Generated evidence-profile variant q-130620 seed 101

Find the possible values of the constant $x$ given that the matrix $[\begin{aligned}3 & 5 & -5 \\ 1 & 3 & 2 \\ x & -1 & - x\end{aligned}]$ is singular.

Field `selection` (radio)
- - \frac{11}{21} **correct**
- 5
- -5
- - \frac{2}{7}
- 4

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}3 & 5 & -5 \\ 1 & 3 & 2 \\ x & -1 & - x\end{aligned}| & =3|\begin{aligned}3 & 2 \\ -1 & - x\end{aligned}|-5|\begin{aligned}1 & 2 \\ x & - x\end{aligned}|+(-5)|\begin{aligned}1 & 3 \\ x & -1\end{aligned}| \\  & =3(2 - 3 x)-5(- 3 x)+(-5)(- 3 x - 1) \\  & =6 - 9 x+15 x+15 x + 5 \\  & =21 x + 11\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}21 x + 11 & =0 \\ x & =- \frac{11}{21}\end{aligned}
$$

Therefore, the solution is $x=- \frac{11}{21}.$

### Generated evidence-profile variant q-130620 seed 202

Find the possible values of the constant $x$ given that the matrix $[\begin{aligned}3 & 5 & 8 \\ -2 & 1 & 2 \\ x & -1 & - x\end{aligned}]$ is singular.

Field `selection` (radio)
- 8
- 2 **correct**
- - \frac{10}{11}
- -6
- 5

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}3 & 5 & 8 \\ -2 & 1 & 2 \\ x & -1 & - x\end{aligned}| & =3|\begin{aligned}1 & 2 \\ -1 & - x\end{aligned}|-5|\begin{aligned}-2 & 2 \\ x & - x\end{aligned}|+8|\begin{aligned}-2 & 1 \\ x & -1\end{aligned}| \\  & =3(2 - x)-5(0)+8(2 - x) \\  & =6 - 3 x+0+16 - 8 x \\  & =22 - 11 x\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}22 - 11 x & =0 \\ x & =2\end{aligned}
$$

Therefore, the solution is $x=2.$

### Generated authored default bank q-130620 seed 303

Find the possible values of the constant $x$ given that the matrix $[\begin{aligned}3 & -2 & 8 \\ 1 & 1 & -4 \\ x & -1 & - x\end{aligned}]$ is singular.

Field `selection` (radio)
- -5
- -20
- 20
- 4
- -4 **correct**

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}3 & -2 & 8 \\ 1 & 1 & -4 \\ x & -1 & - x\end{aligned}| & =3|\begin{aligned}1 & -4 \\ -1 & - x\end{aligned}|-(-2)|\begin{aligned}1 & -4 \\ x & - x\end{aligned}|+8|\begin{aligned}1 & 1 \\ x & -1\end{aligned}| \\  & =3(- x - 4)-(-2)(3 x)+8(- x - 1) \\  & =- 3 x - 12+6 x- 8 x - 8 \\  & =- 5 x - 20\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}- 5 x - 20 & =0 \\ x & =-4\end{aligned}
$$

Therefore, the solution is $x=-4.$

## Original q-130626 (:question.difficulty/hard)

Find the possible values of the constant $p$ given that the matrix
$[\begin{aligned}1 & -3p & 4 \\ -2 & 6p & -8 \\ 1 & -1 & 1\end{aligned}]$ is singular.

Field `selection`
- $\frac{5}{2}$ only
- Any value of $p$ **original correct**
- $-3$ and $3$ only
- $-3$ only
- $-10$ only

**Original worked solution**

First, let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}|\begin{aligned}1 & -3p & 4 \\ -2 & 6p & -8 \\ 1 & -1 & 1\end{aligned}| & =1|\begin{aligned}6p & -8 \\ -1 & 1\end{aligned}|-(-3p)|\begin{aligned}-2 & -8 \\ 1 & 1\end{aligned}|+4|\begin{aligned}-2 & 6p \\ 1 & -1\end{aligned}| \\  & =(6p-8)+3p(-2+8)+4(2-6p) \\  & =6p-8+18p+8-24p \\  & =0.\end{aligned}
$$

Therefore, this matrix is singular for all values of $p.$

### Generated evidence-profile variant q-130626 seed 101

Find the possible values of the constant $p$ given that the matrix
$[\begin{aligned}5 & - 3 p & 3 \\ -10 & 6 p & -6 \\ 1 & -3 & 2\end{aligned}]$ is singular.

Field `selection` (radio)
- $\frac{4}{5}$ only
- $-3$ only
- $-3$ and $3$ only
- Any value of $p$ **correct**
- $-16$ only

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}|\begin{aligned}5 & - 3 p & 3 \\ -10 & 6 p & -6 \\ 1 & -3 & 2\end{aligned}| & =5|\begin{aligned}6 p & -6 \\ -3 & 2\end{aligned}|-(- 3 p)|\begin{aligned}-10 & -6 \\ 1 & 2\end{aligned}|+3|\begin{aligned}-10 & 6 p \\ 1 & -3\end{aligned}| \\  & =5(12 p - 18)-(- 3 p)(-14)+3(30 - 6 p) \\  & =60 p - 90- 42 p+90 - 18 p \\  & =0\end{aligned}
$$

Therefore, this matrix is singular for all values of $p.$

### Generated evidence-profile variant q-130626 seed 202

Find the possible values of the constant $p$ given that the matrix
$[\begin{aligned}4 & - 3 p & 4 \\ -8 & 6 p & -8 \\ -2 & -2 & 4\end{aligned}]$ is singular.

Field `selection` (radio)
- $-3$ and $3$ only
- $1$ only
- Any value of $p$ **correct**
- $-16$ only
- $-3$ only

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}|\begin{aligned}4 & - 3 p & 4 \\ -8 & 6 p & -8 \\ -2 & -2 & 4\end{aligned}| & =4|\begin{aligned}6 p & -8 \\ -2 & 4\end{aligned}|-(- 3 p)|\begin{aligned}-8 & -8 \\ -2 & 4\end{aligned}|+4|\begin{aligned}-8 & 6 p \\ -2 & -2\end{aligned}| \\  & =4(24 p - 16)-(- 3 p)(-48)+4(12 p + 16) \\  & =96 p - 64- 144 p+48 p + 64 \\  & =0\end{aligned}
$$

Therefore, this matrix is singular for all values of $p.$

### Generated authored default bank q-130626 seed 303

Find the possible values of the constant $p$ given that the matrix
$[\begin{aligned}2 & - 3 p & 6 \\ -4 & 6 p & -12 \\ -2 & -3 & 3\end{aligned}]$ is singular.

Field `selection` (radio)
- $-1$ only
- $2$ and $-1$ only
- $2$ only
- $0$ only
- Any value of $p$ **correct**

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}|\begin{aligned}2 & - 3 p & 6 \\ -4 & 6 p & -12 \\ -2 & -3 & 3\end{aligned}| & =2|\begin{aligned}6 p & -12 \\ -3 & 3\end{aligned}|-(- 3 p)|\begin{aligned}-4 & -12 \\ -2 & 3\end{aligned}|+6|\begin{aligned}-4 & 6 p \\ -2 & -3\end{aligned}| \\  & =2(18 p - 36)-(- 3 p)(-36)+6(12 p + 12) \\  & =36 p - 72- 108 p+72 p + 72 \\  & =0\end{aligned}
$$

Therefore, this matrix is singular for all values of $p.$

## Original q-18252 (:question.difficulty/easy)

Find the possible values of the constant $p$ given that the matrix $[\begin{aligned}1 & 0 & 1 \\ 2 & 1 & 2 \\ 6 & -5 & 2p-4\end{aligned}]$ is singular.

Field `selection`
- -3
- 5 **original correct**
- 3
- -5
- 2

**Original worked solution**

First, let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}|\begin{aligned}1 & 0 & 1 \\ 2 & 1 & 2 \\ 6 & -5 & 2p-4\end{aligned}| & =1|\begin{aligned}1 & 2 \\ -5 & 2p-4\end{aligned}|-0|\begin{aligned}2 & 2 \\ 6 & 2p-4\end{aligned}|+1|\begin{aligned}2 & 1 \\ 6 & -5\end{aligned}| \\  & =(2p-4+10)-0+(-10-6) \\  & =2p-4+10-10-6 \\  & =2p-10\end{aligned}
$$

Since the matrix is singular, the determinant is $0.$ So,  we have:

 

$$
\begin{aligned}2p-10 & =0 \\ 2p & =10 \\ p & =\frac{10}{2} \\  & =5\end{aligned}
$$

Therefore, the solution is $p=5.$

### Generated evidence-profile variant q-18252 seed 101

Find the possible values of the constant $p$ given that the matrix $[\begin{aligned}1 & 0 & 1 \\ 2 & 4 & 2 \\ -5 & -5 & 2 p - 4\end{aligned}]$ is singular.

Field `selection` (radio)
- -3
- \frac{1}{2}
- 3
- - \frac{1}{2} **correct**
- 2

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}|\begin{aligned}1 & 0 & 1 \\ 2 & 4 & 2 \\ -5 & -5 & 2 p - 4\end{aligned}| & =1|\begin{aligned}4 & 2 \\ -5 & 2 p - 4\end{aligned}|-0|\begin{aligned}2 & 2 \\ -5 & 2 p - 4\end{aligned}|+1|\begin{aligned}2 & 4 \\ -5 & -5\end{aligned}| \\  & =1(8 p - 6)-0(4 p + 2)+1(10) \\  & =8 p - 6+0+10 \\  & =8 p + 4\end{aligned}
$$

Since the matrix is singular, the determinant is $0.$ So,  we have:

$$
\begin{aligned}8 p + 4 & =0 \\ 8 p & =-4 \\ p & =\frac{-4}{8} \\ p & =- \frac{1}{2}\end{aligned}
$$

Therefore, the solution is $p=- \frac{1}{2}.$

### Generated evidence-profile variant q-18252 seed 202

Find the possible values of the constant $p$ given that the matrix $[\begin{aligned}1 & 0 & 1 \\ 2 & -2 & 2 \\ 6 & -5 & 2 p - 2\end{aligned}]$ is singular.

Field `selection` (radio)
- 3
- -3
- 4 **correct**
- 2
- -4

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}|\begin{aligned}1 & 0 & 1 \\ 2 & -2 & 2 \\ 6 & -5 & 2 p - 2\end{aligned}| & =1|\begin{aligned}-2 & 2 \\ -5 & 2 p - 2\end{aligned}|-0|\begin{aligned}2 & 2 \\ 6 & 2 p - 2\end{aligned}|+1|\begin{aligned}2 & -2 \\ 6 & -5\end{aligned}| \\  & =1(14 - 4 p)-0(4 p - 16)+1(2) \\  & =14 - 4 p+0+2 \\  & =16 - 4 p\end{aligned}
$$

Since the matrix is singular, the determinant is $0.$ So,  we have:

$$
\begin{aligned}16 - 4 p & =0 \\ - 4 p & =-16 \\ p & =\frac{-16}{-4} \\ p & =4\end{aligned}
$$

Therefore, the solution is $p=4.$

### Generated authored default bank q-18252 seed 303

Find the possible values of the constant $p$ given that the matrix $[\begin{aligned}1 & 0 & 1 \\ 2 & 1 & 4 \\ 6 & -5 & 2 p + 2\end{aligned}]$ is singular.

Field `selection` (radio)
- 2
- 6
- -6
- 3
- -3 **correct**

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}|\begin{aligned}1 & 0 & 1 \\ 2 & 1 & 4 \\ 6 & -5 & 2 p + 2\end{aligned}| & =1|\begin{aligned}1 & 4 \\ -5 & 2 p + 2\end{aligned}|-0|\begin{aligned}2 & 4 \\ 6 & 2 p + 2\end{aligned}|+1|\begin{aligned}2 & 1 \\ 6 & -5\end{aligned}| \\  & =1(2 p + 22)-0(4 p - 20)+1(-16) \\  & =2 p + 22+0-16 \\  & =2 p + 6\end{aligned}
$$

Since the matrix is singular, the determinant is $0.$ So,  we have:

$$
\begin{aligned}2 p + 6 & =0 \\ 2 p & =-6 \\ p & =\frac{-6}{2} \\ p & =-3\end{aligned}
$$

Therefore, the solution is $p=-3.$

## Original q-18256 (:question.difficulty/moderate)

Given that the determinant of 
$[\begin{aligned}4 & 2 & 3 \\ -3y & -2 & 1 \\ 2 & y & -5\end{aligned}]$
 is $81,$ find all the possible values of $y.$

Field `selection`
- $-\frac{5}{3}$ and $1$ only
- $-\frac{25}{9}$ and $1$ only
- $-\frac{5}{3}$ and $-1$ only
- $-\frac{25}{9}$ and $-1$ only **original correct**
- $-1$ only

**Original worked solution**

Let's use our formula to find an expression for the determinant in terms of $y:$

$$
\begin{aligned}|\begin{aligned}4 & 2 & 3 \\ -3y & -2 & 1 \\ 2 & y & -5\end{aligned}| & =4|\begin{aligned}-2 & 1 \\ y & -5\end{aligned}|-2|\begin{aligned}-3y & 1 \\ 2 & -5\end{aligned}|+3|\begin{aligned}-3y & -2 \\ 2 & y\end{aligned}| \\  & =4\cdot (10-y)-2\cdot (15y-2)+3\cdot (-3{y}^{2}+4) \\  & =40-4y-30y+4-9{y}^{2}+12 \\  & =-9{y}^{2}-34y+56\end{aligned}
$$

Since the determinant of the matrix is $81,$ we have:

$$
\begin{aligned}-9{y}^{2}-34y+56 & =81 \\ -9{y}^{2}-34y-25 & =0 \\ 9{y}^{2}+34y+25 & =0 \\ y & =\frac{-34\pm \sqrt{{34}^{2}-4\cdot 9\cdot 25}}{2\cdot 9} \\  & =\frac{-34\pm \sqrt{256}}{18} \\  & =\frac{-34\pm 16}{18} \\  & =\frac{-17\pm 8}{9}\end{aligned}
$$

Therefore, the solutions are $y=-\frac{25}{9}$ and $y=-1.$

### Generated evidence-profile variant q-18256 seed 101

Given that the determinant of 
$[\begin{aligned}4 & 2 & -5 \\ - 3 y & -2 & 3 \\ 2 & y & -5\end{aligned}]$
 is $656,$ find all the possible values of $y.$

Field `selection` (radio)
- $1$ and $3$ only
- $- \frac{26}{5}$ and $8$ only **correct**
- $1$ and $-3$ only
- $- \frac{26}{5}$ and $3$ only
- $8$ only

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $y:$

$$
\begin{aligned}|\begin{aligned}4 & 2 & -5 \\ - 3 y & -2 & 3 \\ 2 & y & -5\end{aligned}| & =4|\begin{aligned}-2 & 3 \\ y & -5\end{aligned}|-2|\begin{aligned}- 3 y & 3 \\ 2 & -5\end{aligned}|+(-5)|\begin{aligned}- 3 y & -2 \\ 2 & y\end{aligned}| \\  & =4(10 - 3 y)-2(15 y - 6)+(-5)(4 - 3 y^{2}) \\  & =40 - 12 y+12 - 30 y+15 y^{2} - 20 \\  & =15 y^{2} - 42 y + 32\end{aligned}
$$

Since the determinant of the matrix is $656,$ we have:

$$
\begin{aligned}15 y^{2} - 42 y + 32 & =656 \\ 15 y^{2} - 42 y - 624 & =0 \\ y & =\frac{-(-42)\pm\sqrt{(-42)^2-4\cdot 15\cdot (-624)}}{2\cdot 15} \\  & =\frac{42\pm\sqrt{39204}}{30} \\  & =\frac{42\pm 198}{30} \\  & =- \frac{26}{5},8\end{aligned}
$$

Therefore, the solutions are $y=- \frac{26}{5}$ and $y=8.$

### Generated evidence-profile variant q-18256 seed 202

Given that the determinant of 
$[\begin{aligned}4 & 2 & 3 \\ - 3 y & -2 & 1 \\ 2 & y & -5\end{aligned}]$
 is $88,$ find all the possible values of $y.$

Field `selection` (radio)
- $- \frac{5}{3}$ and $-1$ only
- $- \frac{5}{3}$ and $1$ only
- $-2$ and $1$ only
- $- \frac{16}{9}$ only
- $-2$ and $- \frac{16}{9}$ only **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $y:$

$$
\begin{aligned}|\begin{aligned}4 & 2 & 3 \\ - 3 y & -2 & 1 \\ 2 & y & -5\end{aligned}| & =4|\begin{aligned}-2 & 1 \\ y & -5\end{aligned}|-2|\begin{aligned}- 3 y & 1 \\ 2 & -5\end{aligned}|+3|\begin{aligned}- 3 y & -2 \\ 2 & y\end{aligned}| \\  & =4(10 - y)-2(15 y - 2)+3(4 - 3 y^{2}) \\  & =40 - 4 y+4 - 30 y+12 - 9 y^{2} \\  & =- 9 y^{2} - 34 y + 56\end{aligned}
$$

Since the determinant of the matrix is $88,$ we have:

$$
\begin{aligned}- 9 y^{2} - 34 y + 56 & =88 \\ - 9 y^{2} - 34 y - 32 & =0 \\ 9 y^{2} + 34 y + 32 & =0 \\ y & =\frac{-(34)\pm\sqrt{(34)^2-4\cdot 9\cdot (32)}}{2\cdot 9} \\  & =\frac{-34\pm\sqrt{4}}{18} \\  & =\frac{-34\pm 2}{18} \\  & =-2,- \frac{16}{9}\end{aligned}
$$

Therefore, the solutions are $y=-2$ and $y=- \frac{16}{9}.$

### Generated authored default bank q-18256 seed 303

Given that the determinant of 
$[\begin{aligned}4 & 2 & 3 \\ - 3 y & -2 & 2 \\ 2 & y & -3\end{aligned}]$
 is $-311,$ find all the possible values of $y.$

Field `selection` (radio)
- $5$ only
- $0$ and $- \frac{26}{9}$ only
- $- \frac{71}{9}$ only
- $\frac{71}{9}$ and $-5$ only
- $- \frac{71}{9}$ and $5$ only **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $y:$

$$
\begin{aligned}|\begin{aligned}4 & 2 & 3 \\ - 3 y & -2 & 2 \\ 2 & y & -3\end{aligned}| & =4|\begin{aligned}-2 & 2 \\ y & -3\end{aligned}|-2|\begin{aligned}- 3 y & 2 \\ 2 & -3\end{aligned}|+3|\begin{aligned}- 3 y & -2 \\ 2 & y\end{aligned}| \\  & =4(6 - 2 y)-2(9 y - 4)+3(4 - 3 y^{2}) \\  & =24 - 8 y+8 - 18 y+12 - 9 y^{2} \\  & =- 9 y^{2} - 26 y + 44\end{aligned}
$$

Since the determinant of the matrix is $-311,$ we have:

$$
\begin{aligned}- 9 y^{2} - 26 y + 44 & =-311 \\ - 9 y^{2} - 26 y + 355 & =0 \\ 9 y^{2} + 26 y - 355 & =0 \\ y & =\frac{-(26)\pm\sqrt{(26)^2-4\cdot 9\cdot (-355)}}{2\cdot 9} \\  & =\frac{-26\pm\sqrt{13456}}{18} \\  & =\frac{-26\pm 116}{18} \\  & =- \frac{71}{9},5\end{aligned}
$$

Therefore, the solutions are $y=- \frac{71}{9}$ and $y=5.$

## Original q-18271 (:question.difficulty/easy)

Given that
$A=[\begin{aligned}-k & 0 & -3 \\ 1 & 3 & -1 \\ 2k & 0 & 1\end{aligned}]$
and $det(A)=-30,$ find the value of $k.$

Field `selection`
- 3
- 1
- 2
- -3
- -2 **original correct**

**Original worked solution**

Let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}\text{det}(A) & =|\begin{aligned}-k & 0 & -3 \\ 1 & 3 & -1 \\ 2k & 0 & 1\end{aligned}| \\  & =-k|\begin{aligned}3 & -1 \\ 0 & 1\end{aligned}|-0|\begin{aligned}1 & -1 \\ 2k & 1\end{aligned}|-3|\begin{aligned}1 & 3 \\ 2k & 0\end{aligned}| \\  & =-k\cdot 3+0-3\cdot (-6k) \\  & =-3k+18k \\  & =15k\end{aligned}
$$

Since the determinant of the matrix is $-30,$ we have:

$$
\begin{aligned}15k & =-30 \\ k & =-2\end{aligned}
$$

### Generated evidence-profile variant q-18271 seed 101

Given that
$A=[\begin{aligned}- k & 0 & -3 \\ 1 & -5 & -1 \\ 2 k & 0 & 3\end{aligned}]$
and $det(A)=78,$ find the value of $k.$

Field `selection` (radio)
- -5
- 5
- \frac{26}{5}
- 1
- - \frac{26}{5} **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}\text{det}(A) & =|\begin{aligned}- k & 0 & -3 \\ 1 & -5 & -1 \\ 2 k & 0 & 3\end{aligned}| \\  & =(- k)|\begin{aligned}-5 & -1 \\ 0 & 3\end{aligned}|-0|\begin{aligned}1 & -1 \\ 2 k & 3\end{aligned}|+(-3)|\begin{aligned}1 & -5 \\ 2 k & 0\end{aligned}| \\  & =(- k)(-15)-0(2 k + 3)+(-3)(10 k) \\  & =15 k+0- 30 k \\  & =- 15 k\end{aligned}
$$

Since the determinant of the matrix is $78,$ we have:

$$
\begin{aligned}- 15 k & =78 \\ k & =- \frac{26}{5}\end{aligned}
$$

### Generated evidence-profile variant q-18271 seed 202

Given that
$A=[\begin{aligned}- k & 0 & -3 \\ 1 & 3 & -2 \\ 2 k & 0 & -2\end{aligned}]$
and $det(A)=51,$ find the value of $k.$

Field `selection` (radio)
- - \frac{17}{8}
- 3
- 1
- \frac{17}{8} **correct**
- -3

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}\text{det}(A) & =|\begin{aligned}- k & 0 & -3 \\ 1 & 3 & -2 \\ 2 k & 0 & -2\end{aligned}| \\  & =(- k)|\begin{aligned}3 & -2 \\ 0 & -2\end{aligned}|-0|\begin{aligned}1 & -2 \\ 2 k & -2\end{aligned}|+(-3)|\begin{aligned}1 & 3 \\ 2 k & 0\end{aligned}| \\  & =(- k)(-6)-0(4 k - 2)+(-3)(- 6 k) \\  & =6 k+0+18 k \\  & =24 k\end{aligned}
$$

Since the determinant of the matrix is $51,$ we have:

$$
\begin{aligned}24 k & =51 \\ k & =\frac{17}{8}\end{aligned}
$$

### Generated authored default bank q-18271 seed 303

Given that
$A=[\begin{aligned}- k & 0 & -3 \\ -4 & 3 & -1 \\ 2 k & 0 & 5\end{aligned}]$
and $det(A)=16,$ find the value of $k.$

Field `selection` (radio)
- 3
- -16
- 16
- - \frac{16}{3}
- \frac{16}{3} **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}\text{det}(A) & =|\begin{aligned}- k & 0 & -3 \\ -4 & 3 & -1 \\ 2 k & 0 & 5\end{aligned}| \\  & =(- k)|\begin{aligned}3 & -1 \\ 0 & 5\end{aligned}|-0|\begin{aligned}-4 & -1 \\ 2 k & 5\end{aligned}|+(-3)|\begin{aligned}-4 & 3 \\ 2 k & 0\end{aligned}| \\  & =(- k)(15)-0(2 k - 20)+(-3)(- 6 k) \\  & =- 15 k+0+18 k \\  & =3 k\end{aligned}
$$

Since the determinant of the matrix is $16,$ we have:

$$
\begin{aligned}3 k & =16 \\ k & =\frac{16}{3}\end{aligned}
$$

## Original q-18272 (:question.difficulty/moderate)

Given that $M=[\begin{aligned}0 & -3 & 2 \\ 1 & p & 0 \\ p-3 & 0 & -1\end{aligned}]$ and $det(M)=-23,$ find all the possible values of $p.$

Field `selection`
- $2$ and $4$ only
- $-2$ and $5$ only **original correct**
- $4$ and $5$ only
- $4$ only
- $5$ only

**Original worked solution**

Let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}\text{det}(M) & =|\begin{aligned}0 & -3 & 2 \\ 1 & p & 0 \\ p-3 & 0 & -1\end{aligned}| \\  & =0|\begin{aligned}p & 0 \\ 0 & -1\end{aligned}|-(-3)|\begin{aligned}1 & 0 \\ p-3 & -1\end{aligned}|+2|\begin{aligned}1 & p \\ p-3 & 0\end{aligned}| \\  & =0+3\cdot (-1)+2\cdot (3p-{p}^{2}) \\  & =-3-2{p}^{2}+6p \\  & =-2{p}^{2}+6p-3\end{aligned}
$$

Since the determinant of the matrix is $-23,$ we have:

$$
\begin{aligned}-2{p}^{2}+6p-3 & =-23 \\ 2{p}^{2}-6p-20 & =0 \\ {p}^{2}-3p-10 & =0 \\ p & =\frac{-(-3)\pm \sqrt{(-3)^{2}-4\cdot 1\cdot (-10)}}{2\cdot 1} \\  & =\frac{3\pm \sqrt{49}}{2} \\  & =\frac{3\pm 7}{2}\end{aligned}
$$

Therefore,  the solutions are $p=-2$ and $p=5.$

### Generated evidence-profile variant q-18272 seed 101

Given that $M=[\begin{aligned}0 & -3 & 2 \\ -5 & p & 0 \\ p - 3 & 0 & 3\end{aligned}]$ and $det(M)=-125,$ find all the possible values of $p.$

Field `selection` (radio)
- $5$ and $4$ only
- $4$ only
- $4$ and $8$ only
- $-5$ and $8$ only **correct**
- $8$ only

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}\text{det}(M) & =|\begin{aligned}0 & -3 & 2 \\ -5 & p & 0 \\ p - 3 & 0 & 3\end{aligned}| \\  & =0|\begin{aligned}p & 0 \\ 0 & 3\end{aligned}|-(-3)|\begin{aligned}-5 & 0 \\ p - 3 & 3\end{aligned}|+2|\begin{aligned}-5 & p \\ p - 3 & 0\end{aligned}| \\  & =0(3 p)-(-3)(-15)+2(- p^{2} + 3 p) \\  & =0-45- 2 p^{2} + 6 p \\  & =- 2 p^{2} + 6 p - 45\end{aligned}
$$

Since the determinant of the matrix is $-125,$ we have:

$$
\begin{aligned}- 2 p^{2} + 6 p - 45 & =-125 \\ 2 p^{2} - 6 p - 80 & =0 \\ p^{2} - 3 p - 40 & =0 \\ p & =\frac{-(-3)\pm\sqrt{(-3)^2-4\cdot 1\cdot (-40)}}{2\cdot 1} \\  & =\frac{3\pm\sqrt{169}}{2} \\  & =\frac{3\pm 13}{2}\end{aligned}
$$

Therefore, the solutions are $p=-5$ and $p=8.$

### Generated evidence-profile variant q-18272 seed 202

Given that $M=[\begin{aligned}0 & -3 & 2 \\ -2 & p & 0 \\ p - 3 & 0 & -2\end{aligned}]$ and $det(M)=-44,$ find all the possible values of $p.$

Field `selection` (radio)
- $4$ and $7$ only
- $4$ and $4$ only
- $-4$ and $7$ only **correct**
- $7$ only
- $4$ only

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}\text{det}(M) & =|\begin{aligned}0 & -3 & 2 \\ -2 & p & 0 \\ p - 3 & 0 & -2\end{aligned}| \\  & =0|\begin{aligned}p & 0 \\ 0 & -2\end{aligned}|-(-3)|\begin{aligned}-2 & 0 \\ p - 3 & -2\end{aligned}|+2|\begin{aligned}-2 & p \\ p - 3 & 0\end{aligned}| \\  & =0(- 2 p)-(-3)(4)+2(- p^{2} + 3 p) \\  & =0+12- 2 p^{2} + 6 p \\  & =- 2 p^{2} + 6 p + 12\end{aligned}
$$

Since the determinant of the matrix is $-44,$ we have:

$$
\begin{aligned}- 2 p^{2} + 6 p + 12 & =-44 \\ 2 p^{2} - 6 p - 56 & =0 \\ p^{2} - 3 p - 28 & =0 \\ p & =\frac{-(-3)\pm\sqrt{(-3)^2-4\cdot 1\cdot (-28)}}{2\cdot 1} \\  & =\frac{3\pm\sqrt{121}}{2} \\  & =\frac{3\pm 11}{2}\end{aligned}
$$

Therefore, the solutions are $p=-4$ and $p=7.$

### Generated authored default bank q-18272 seed 303

Given that $M=[\begin{aligned}0 & -3 & 2 \\ 1 & p & 0 \\ p + 2 & 0 & -3\end{aligned}]$ and $det(M)=-135,$ find all the possible values of $p.$

Field `selection` (radio)
- $7$ only
- $0$ and $-2$ only
- $-9$ only
- $9$ and $-7$ only
- $-9$ and $7$ only **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $p:$

$$
\begin{aligned}\text{det}(M) & =|\begin{aligned}0 & -3 & 2 \\ 1 & p & 0 \\ p + 2 & 0 & -3\end{aligned}| \\  & =0|\begin{aligned}p & 0 \\ 0 & -3\end{aligned}|-(-3)|\begin{aligned}1 & 0 \\ p + 2 & -3\end{aligned}|+2|\begin{aligned}1 & p \\ p + 2 & 0\end{aligned}| \\  & =0(- 3 p)-(-3)(-3)+2(- p^{2} - 2 p) \\  & =0-9- 2 p^{2} - 4 p \\  & =- 2 p^{2} - 4 p - 9\end{aligned}
$$

Since the determinant of the matrix is $-135,$ we have:

$$
\begin{aligned}- 2 p^{2} - 4 p - 9 & =-135 \\ 2 p^{2} + 4 p - 126 & =0 \\ p^{2} + 2 p - 63 & =0 \\ p & =\frac{-(2)\pm\sqrt{(2)^2-4\cdot 1\cdot (-63)}}{2\cdot 1} \\  & =\frac{-2\pm\sqrt{256}}{2} \\  & =\frac{-2\pm 16}{2}\end{aligned}
$$

Therefore, the solutions are $p=-9$ and $p=7.$

## Original q-280403 (:question.difficulty/easy)

Given that $A=[\begin{aligned}2 & 1 & 0 \\ 3 & x & 4 \\ -2 & 5 & 1\end{aligned}]$ and $det(A)=37$, find the value of $x.$

$x=$
{{field-1}}

Field `field-1`
- 44 **original correct**

**Original worked solution**

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}\text{det}(F) & =|\begin{aligned}2 & 1 & 0 \\ 3 & x & 4 \\ -2 & 5 & 1\end{aligned}| \\  & =2|\begin{aligned}x & 4 \\ 5 & 1\end{aligned}|-1|\begin{aligned}3 & 4 \\ -2 & 1\end{aligned}|+0|\begin{aligned}3 & x \\ -2 & 5\end{aligned}| \\  & =2(x\cdot 1-4\cdot 5)-(3\cdot 1-4\cdot (-2)) \\  & =2(x-20)-(3+8) \\  & =2x-40-11 \\  & =2x-51\end{aligned}
$$

Since the determinant of the matrix is $37,$ we have

$$
\begin{aligned}2x-51 & =37 \\ 2x & =88 \\ x & =44.\end{aligned}
$$

### Generated evidence-profile variant q-280403 seed 101

Given that $A=[\begin{aligned}2 & 1 & 0 \\ -5 & x & 4 \\ 3 & 5 & 1\end{aligned}]$ and $det(A)=78$, find the value of $x.$

$x=$
{{field-1}}

Field `field-1` (blank)
- \frac{101}{2} **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}\text{det}(A) & =|\begin{aligned}2 & 1 & 0 \\ -5 & x & 4 \\ 3 & 5 & 1\end{aligned}| \\  & =2|\begin{aligned}x & 4 \\ 5 & 1\end{aligned}|-1|\begin{aligned}-5 & 4 \\ 3 & 1\end{aligned}|+0|\begin{aligned}-5 & x \\ 3 & 5\end{aligned}| \\  & =2\big(x-(20)\big)-1\big(-5-(12)\big)+0\big(-25-(3 x)\big) \\  & =2(x - 20)-1(-17)+0(- 3 x - 25) \\  & =2 x - 40+17+0 \\  & =2 x - 23\end{aligned}
$$

Since the determinant of the matrix is $78,$ we have

$$
\begin{aligned}2 x - 23 & =78 \\ 2 x & =101 \\ x & =\frac{101}{2}.\end{aligned}
$$

### Generated evidence-profile variant q-280403 seed 202

Given that $A=[\begin{aligned}2 & 1 & 0 \\ 3 & x & -2 \\ -2 & 2 & 1\end{aligned}]$ and $det(A)=0$, find the value of $x.$

$x=$
{{field-1}}

Field `field-1` (blank)
- - \frac{9}{2} **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}\text{det}(A) & =|\begin{aligned}2 & 1 & 0 \\ 3 & x & -2 \\ -2 & 2 & 1\end{aligned}| \\  & =2|\begin{aligned}x & -2 \\ 2 & 1\end{aligned}|-1|\begin{aligned}3 & -2 \\ -2 & 1\end{aligned}|+0|\begin{aligned}3 & x \\ -2 & 2\end{aligned}| \\  & =2\big(x-(-4)\big)-1\big(3-(4)\big)+0\big(6-(- 2 x)\big) \\  & =2(x + 4)-1(-1)+0(2 x + 6) \\  & =2 x + 8+1+0 \\  & =2 x + 9\end{aligned}
$$

Since the determinant of the matrix is $0,$ we have

$$
\begin{aligned}2 x + 9 & =0 \\ 2 x & =-9 \\ x & =- \frac{9}{2}.\end{aligned}
$$

## Original q-280404 (:question.difficulty/easy)

Find the possible values of the constant $k$ given that the matrix $[\begin{aligned}k+1 & 2k & 3 \\ 0 & 5 & 0 \\ -2 & k & 1\end{aligned}]$ is singular.

$k=$
{{field-1}}

Field `field-1`
- -7 **original correct**

**Original worked solution**

Let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}det & =|\begin{aligned}k+1 & 2k & 3 \\ 0 & 5 & 0 \\ -2 & k & 1\end{aligned}| \\  & =(k+1)|\begin{aligned}5 & 0 \\ k & 1\end{aligned}|-2k|\begin{aligned}0 & 0 \\ -2 & 1\end{aligned}|+3|\begin{aligned}0 & 5 \\ -2 & k\end{aligned}| \\  & =(k+1)(5\cdot 1-0\cdot k)-2k(0\cdot 1-0\cdot -2)+3(0\cdot k-5\cdot (-2)) \\  & =(k+1)(5)-2k(0)+3(10) \\  & =5k+5+30 \\  & =5k+35\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have

$$
\begin{aligned}5k+35 & =0 \\ 5k & =-35 \\ k & =-7.\end{aligned}
$$

### Generated evidence-profile variant q-280404 seed 101

Find the possible values of the constant $k$ given that the matrix $[\begin{aligned}k + 1 & 2 k & 3 \\ 0 & -5 & 0 \\ -2 & k & 3\end{aligned}]$ is singular.

$k=$
{{field-1}}

Field `field-1` (blank)
- -3 **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}det & =|\begin{aligned}k + 1 & 2 k & 3 \\ 0 & -5 & 0 \\ -2 & k & 3\end{aligned}| \\  & =(k + 1)|\begin{aligned}-5 & 0 \\ k & 3\end{aligned}|-2 k|\begin{aligned}0 & 0 \\ -2 & 3\end{aligned}|+3|\begin{aligned}0 & -5 \\ -2 & k\end{aligned}| \\  & =(k + 1)\big(-15-(0)\big)-2 k\big(0-(0)\big)+3\big(0-(10)\big) \\  & =(k + 1)(-15)-2 k(0)+3(-10) \\  & =- 15 k - 15+0-30 \\  & =- 15 k - 45\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have

$$
\begin{aligned}- 15 k - 45 & =0 \\ - 15 k & =45 \\ k & =-3.\end{aligned}
$$

### Generated evidence-profile variant q-280404 seed 202

Find the possible values of the constant $k$ given that the matrix $[\begin{aligned}k + 1 & 2 k & 3 \\ 0 & 5 & 0 \\ -2 & k & -2\end{aligned}]$ is singular.

$k=$
{{field-1}}

Field `field-1` (blank)
- 2 **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}det & =|\begin{aligned}k + 1 & 2 k & 3 \\ 0 & 5 & 0 \\ -2 & k & -2\end{aligned}| \\  & =(k + 1)|\begin{aligned}5 & 0 \\ k & -2\end{aligned}|-2 k|\begin{aligned}0 & 0 \\ -2 & -2\end{aligned}|+3|\begin{aligned}0 & 5 \\ -2 & k\end{aligned}| \\  & =(k + 1)\big(-10-(0)\big)-2 k\big(0-(0)\big)+3\big(0-(-10)\big) \\  & =(k + 1)(-10)-2 k(0)+3(10) \\  & =- 10 k - 10+0+30 \\  & =20 - 10 k\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have

$$
\begin{aligned}20 - 10 k & =0 \\ - 10 k & =-20 \\ k & =2.\end{aligned}
$$

## Original q-280519 (:question.difficulty/easy)

Given that $G=[\begin{aligned}x & 2x-1 & 6 \\ 0 & 3 & 0 \\ -1 & x+1 & -4\end{aligned}]$ is singular, find the value of $x.$

$x=$
{{field-1}}

Field `field-1`
- \frac{3}{2} **original correct**

**Original worked solution**

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}det & =|\begin{aligned}x & 2x-1 & 6 \\ 0 & 3 & 0 \\ -1 & x+1 & -4\end{aligned}| \\  & =x|\begin{aligned}3 & 0 \\ x+1 & -4\end{aligned}|-(2x-1)|\begin{aligned}0 & 0 \\ -1 & -4\end{aligned}|+6|\begin{aligned}0 & 3 \\ -1 & x+1\end{aligned}| \\  & =x(3\cdot (-4)-0\cdot (x+1))-(2x-1)(0)+6(0\cdot (x+1)-3\cdot (-1)) \\  & =x(-12)+0+6(3) \\  & =-12x+18\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have

$$
\begin{aligned}-12x+18 & =0 \\ -12x & =-18 \\ x & =\frac{3}{2}.\end{aligned}
$$

### Generated evidence-profile variant q-280519 seed 101

Given that $G=[\begin{aligned}x & 2 x - 1 & 6 \\ 0 & -5 & 0 \\ -1 & x + 3 & -4\end{aligned}]$ is singular, find the value of $x.$

$x=$
{{field-1}}

Field `field-1` (blank)
- \frac{3}{2} **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}\text{det}(G) & =|\begin{aligned}x & 2 x - 1 & 6 \\ 0 & -5 & 0 \\ -1 & x + 3 & -4\end{aligned}| \\  & =x|\begin{aligned}-5 & 0 \\ x + 3 & -4\end{aligned}|-(2 x - 1)|\begin{aligned}0 & 0 \\ -1 & -4\end{aligned}|+6|\begin{aligned}0 & -5 \\ -1 & x + 3\end{aligned}| \\  & =x(20)-(2 x - 1)(0)+6(-5) \\  & =20 x+0-30 \\  & =20 x - 30\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have

$$
\begin{aligned}20 x - 30 & =0 \\ 20 x & =30 \\ x & =\frac{3}{2}.\end{aligned}
$$

### Generated evidence-profile variant q-280519 seed 202

Given that $G=[\begin{aligned}x & 2 x - 1 & 6 \\ 0 & 3 & 0 \\ -2 & x + 1 & 2\end{aligned}]$ is singular, find the value of $x.$

$x=$
{{field-1}}

Field `field-1` (blank)
- -6 **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}\text{det}(G) & =|\begin{aligned}x & 2 x - 1 & 6 \\ 0 & 3 & 0 \\ -2 & x + 1 & 2\end{aligned}| \\  & =x|\begin{aligned}3 & 0 \\ x + 1 & 2\end{aligned}|-(2 x - 1)|\begin{aligned}0 & 0 \\ -2 & 2\end{aligned}|+6|\begin{aligned}0 & 3 \\ -2 & x + 1\end{aligned}| \\  & =x(6)-(2 x - 1)(0)+6(6) \\  & =6 x+0+36 \\  & =6 x + 36\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have

$$
\begin{aligned}6 x + 36 & =0 \\ 6 x & =-36 \\ x & =-6.\end{aligned}
$$

## Original q-280540 (:question.difficulty/moderate)

Given that the determinant of $[\begin{aligned}{x}^{2}-2 & 3 & 0 \\ x & -2 & -1 \\ 1 & 4 & 0\end{aligned}]$ is $32$, find all the possible values of $x$ **in ascending order**.

In ascending order, $x=$
{{field-1}} and $x=$
{{field-2}}.

Field `field-2`
- \frac{\sqrt{43}}{2} **original correct**
Field `field-1`
- -\frac{\sqrt{43}}{2} **original correct**

**Original worked solution**

Let’s use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}det(A) & =|\begin{aligned}{x}^{2}-2 & 3 & 0 \\ x & -2 & -1 \\ 1 & 4 & 0\end{aligned}| \\  & =({x}^{2}-2)|\begin{aligned}-2 & -1 \\ 4 & 0\end{aligned}|-3|\begin{aligned}x & -1 \\ 1 & 0\end{aligned}|+0 \\  & =({x}^{2}-2)(-2\cdot 0-(-1)(4))-3(x\cdot 0-(-1)(1)) \\  & =({x}^{2}-2)(4)-3(1) \\  & =4{x}^{2}-8-3 \\  & =4{x}^{2}-11\end{aligned}
$$

Since the determinant of the matrix is $32$, we have

$$
\begin{aligned}4{x}^{2}-11 & =32 \\ 4{x}^{2} & =43 \\ {x}^{2} & =\frac{43}{4} \\ x & =\pm \sqrt{\frac{43}{4}} \\  & =\pm \frac{\sqrt{43}}{2}\end{aligned}
$$

Therefore, **in ascending order**, the solutions are $x=-\frac{\sqrt{43}}{2}$ and $x=\frac{\sqrt{43}}{2}.$

### Generated evidence-profile variant q-280540 seed 101

Given that the determinant of $[\begin{aligned}x^{2} - 2 & 3 & 0 \\ x & -5 & -1 \\ 3 & 4 & 0\end{aligned}]$ is $44$, find all the possible values of $x$ **in ascending order**.

In ascending order, $x=$
{{field-1}} and $x=$
{{field-2}}.

Field `field-1` (blank)
- - \frac{\sqrt{61}}{2} **correct**
Field `field-2` (blank)
- \frac{\sqrt{61}}{2} **correct**

**Worked solution**

Let’s use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}det(A) & =|\begin{aligned}x^{2} - 2 & 3 & 0 \\ x & -5 & -1 \\ 3 & 4 & 0\end{aligned}| \\  & =(x^{2} - 2)|\begin{aligned}-5 & -1 \\ 4 & 0\end{aligned}|-3|\begin{aligned}x & -1 \\ 3 & 0\end{aligned}|+0|\begin{aligned}x & -5 \\ 3 & 4\end{aligned}| \\  & =(x^{2} - 2)\big(0-(-4)\big)-3\big(0-(-3)\big)+0\big(4 x-(-15)\big) \\  & =(x^{2} - 2)(4)-3(3)+0(4 x + 15) \\  & =4 x^{2} - 8-9+0 \\  & =4 x^{2} - 17\end{aligned}
$$

Since the determinant of the matrix is $44$, we have

$$
\begin{aligned}4 x^{2} - 17 & =44 \\ 4 x^{2} & =61 \\ x^2 & =\frac{61}{4} \\ x & =\pm\sqrt{\frac{61}{4}} \\  & =\pm \frac{\sqrt{61}}{2}\end{aligned}
$$

Therefore, **in ascending order**, the solutions are $x=- \frac{\sqrt{61}}{2}$ and $x=\frac{\sqrt{61}}{2}.$

### Generated evidence-profile variant q-280540 seed 202

Given that the determinant of $[\begin{aligned}x^{2} - 2 & 3 & 0 \\ x & -2 & -2 \\ 1 & 2 & 0\end{aligned}]$ is $14$, find all the possible values of $x$ **in ascending order**.

In ascending order, $x=$
{{field-1}} and $x=$
{{field-2}}.

Field `field-1` (blank)
- - \sqrt{7} **correct**
Field `field-2` (blank)
- \sqrt{7} **correct**

**Worked solution**

Let’s use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}det(A) & =|\begin{aligned}x^{2} - 2 & 3 & 0 \\ x & -2 & -2 \\ 1 & 2 & 0\end{aligned}| \\  & =(x^{2} - 2)|\begin{aligned}-2 & -2 \\ 2 & 0\end{aligned}|-3|\begin{aligned}x & -2 \\ 1 & 0\end{aligned}|+0|\begin{aligned}x & -2 \\ 1 & 2\end{aligned}| \\  & =(x^{2} - 2)\big(0-(-4)\big)-3\big(0-(-2)\big)+0\big(2 x-(-2)\big) \\  & =(x^{2} - 2)(4)-3(2)+0(2 x + 2) \\  & =4 x^{2} - 8-6+0 \\  & =4 x^{2} - 14\end{aligned}
$$

Since the determinant of the matrix is $14$, we have

$$
\begin{aligned}4 x^{2} - 14 & =14 \\ 4 x^{2} & =28 \\ x^2 & =7 \\ x & =\pm\sqrt{7} \\  & =\pm \sqrt{7}\end{aligned}
$$

Therefore, **in ascending order**, the solutions are $x=- \sqrt{7}$ and $x=\sqrt{7}.$

## Original q-280541 (:question.difficulty/moderate)

Given that the determinant of $[\begin{aligned}x & 2x & 5 \\ 3 & x & 4 \\ 7 & 1 & 2\end{aligned}]$ is $40$, find all the possible values of $x$ **in ascending order**.

In ascending order, $x=$
{{field-1}} and $x=$
{{field-2}}.

Field `field-2`
- \frac{5}{2} **original correct**
Field `field-1`
- -5 **original correct**

**Original worked solution**

Let’s use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}det(A) & =|\begin{aligned}x & 2x & 5 \\ 3 & x & 4 \\ 7 & 1 & 2\end{aligned}| \\  & =x|\begin{aligned}x & 4 \\ 1 & 2\end{aligned}|-2x|\begin{aligned}3 & 4 \\ 7 & 2\end{aligned}|+5|\begin{aligned}3 & x \\ 7 & 1\end{aligned}| \\  & =x(2x-4)-2x(3\cdot 2-4\cdot 7)+5(3-7x) \\  & =x(2x-4)-2x(-22)+15-35x \\  & =2{x}^{2}-4x+44x+15-35x \\  & =2{x}^{2}+5x+15\end{aligned}
$$

Since the determinant of the matrix is $40$, we have

$$
\begin{aligned}2{x}^{2}+5x+15 & =40 \\ 2{x}^{2}+5x-25 & =0 \\ x & =\frac{-5\pm \sqrt{{5}^{2}-4(2)(-25)}}{2(2)} \\ x & =\frac{-5+\sqrt{225}}{4} \\  & =\frac{-5\pm 15}{4}.\end{aligned}
$$

Therefore, **in ascending order**, the solutions are $x=-5$ and $x=\frac{5}{2}.$

### Generated evidence-profile variant q-280541 seed 101

Given that the determinant of $[\begin{aligned}x & 2 x & 5 \\ 3 & x & -5 \\ 7 & 3 & 2\end{aligned}]$ is $-643$, find all the possible values of $x$ **in ascending order**.

In ascending order, $x=$
{{field-1}} and $x=$
{{field-2}}.

Field `field-1` (blank)
- 8 **correct**
Field `field-2` (blank)
- 43 **correct**

**Worked solution**

Let’s use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}det(A) & =|\begin{aligned}x & 2 x & 5 \\ 3 & x & -5 \\ 7 & 3 & 2\end{aligned}| \\  & =x|\begin{aligned}x & -5 \\ 3 & 2\end{aligned}|-2 x|\begin{aligned}3 & -5 \\ 7 & 2\end{aligned}|+5|\begin{aligned}3 & x \\ 7 & 3\end{aligned}| \\  & =x\big(2 x-(-15)\big)-2 x\big(6-(-35)\big)+5\big(9-(7 x)\big) \\  & =x(2 x + 15)-2 x(41)+5(9 - 7 x) \\  & =2 x^{2} + 15 x- 82 x+45 - 35 x \\  & =2 x^{2} - 102 x + 45\end{aligned}
$$

Since the determinant of the matrix is $-643$, we have

$$
\begin{aligned}2 x^{2} - 102 x + 45 & =-643 \\ 2 x^{2} - 102 x + 688 & =0 \\ x & =\frac{-(-102)\pm\sqrt{(-102)^2-4\cdot 2\cdot (688)}}{2\cdot 2} \\  & =\frac{102\pm\sqrt{4900}}{4} \\  & =\frac{102\pm 70}{4}\end{aligned}
$$

Therefore, **in ascending order**, the solutions are $x=8$ and $x=43.$

### Generated evidence-profile variant q-280541 seed 202

Given that the determinant of $[\begin{aligned}x & 2 x & 5 \\ 3 & x & 4 \\ -2 & 1 & 2\end{aligned}]$ is $67$, find all the possible values of $x$ **in ascending order**.

In ascending order, $x=$
{{field-1}} and $x=$
{{field-2}}.

Field `field-1` (blank)
- -2 **correct**
Field `field-2` (blank)
- 13 **correct**

**Worked solution**

Let’s use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}det(A) & =|\begin{aligned}x & 2 x & 5 \\ 3 & x & 4 \\ -2 & 1 & 2\end{aligned}| \\  & =x|\begin{aligned}x & 4 \\ 1 & 2\end{aligned}|-2 x|\begin{aligned}3 & 4 \\ -2 & 2\end{aligned}|+5|\begin{aligned}3 & x \\ -2 & 1\end{aligned}| \\  & =x\big(2 x-(4)\big)-2 x\big(6-(-8)\big)+5\big(3-(- 2 x)\big) \\  & =x(2 x - 4)-2 x(14)+5(2 x + 3) \\  & =2 x^{2} - 4 x- 28 x+10 x + 15 \\  & =2 x^{2} - 22 x + 15\end{aligned}
$$

Since the determinant of the matrix is $67$, we have

$$
\begin{aligned}2 x^{2} - 22 x + 15 & =67 \\ 2 x^{2} - 22 x - 52 & =0 \\ x & =\frac{-(-22)\pm\sqrt{(-22)^2-4\cdot 2\cdot (-52)}}{2\cdot 2} \\  & =\frac{22\pm\sqrt{900}}{4} \\  & =\frac{22\pm 30}{4}\end{aligned}
$$

Therefore, **in ascending order**, the solutions are $x=-2$ and $x=13.$

## Original q-9911 (:question.difficulty/moderate)

Find the possible values of the constant $k$ given that the matrix
$[\begin{aligned}1 & -1 & k \\ 1 & k & -k \\ 5 & k & k\end{aligned}]$ is singular.

Field `selection`
- $0$ and $3$ only **original correct**
- $-3$ only
- $0$ only
- $0$ and $-3$ only
- $3$ only

**Original worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}1 & -1 & k \\ 1 & k & -k \\ 5 & k & k\end{aligned}| & =1|\begin{aligned}k & -k \\ k & k\end{aligned}|-(-1)|\begin{aligned}1 & -k \\ 5 & k\end{aligned}|+k|\begin{aligned}1 & k \\ 5 & k\end{aligned}| \\  & =({k}^{2}+{k}^{2})+(k+5k)+k(k-5k) \\  & =2{k}^{2}+6k+k\cdot (-4k) \\  & =2{k}^{2}+6k-4{k}^{2} \\  & =-2{k}^{2}+6k\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}-2{k}^{2}+6k & =0 \\ k(-2k+6) & =0\end{aligned}
$$

Therefore, the solutions are $k=0$ and $k=3.$

### Generated evidence-profile variant q-9911 seed 101

Find the possible values of the constant $k$ given that the matrix
$[\begin{aligned}1 & -2 & k \\ -1 & k & - k \\ 5 & k & k\end{aligned}]$ is singular.

Field `selection` (radio)
- $0$ and $2$ only **correct**
- $0$ and $-2$ only
- $0$ only
- $-2$ only
- $2$ only

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}1 & -2 & k \\ -1 & k & - k \\ 5 & k & k\end{aligned}| & =1|\begin{aligned}k & - k \\ k & k\end{aligned}|-(-2)|\begin{aligned}-1 & - k \\ 5 & k\end{aligned}|+k|\begin{aligned}-1 & k \\ 5 & k\end{aligned}| \\  & =1\big(k^{2}-(- k^{2})\big)-(-2)\big(- k-(- 5 k)\big)+k\big(- k-(5 k)\big) \\  & =1(2 k^{2})-(-2)(4 k)+k(- 6 k) \\  & =2 k^{2}+8 k- 6 k^{2} \\  & =- 4 k^{2} + 8 k\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}- 4 k^{2} + 8 k & =0 \\ - 4 k (k - 2) & =0\end{aligned}
$$

Therefore, the solutions are $k=0$ and $k=2.$

### Generated evidence-profile variant q-9911 seed 202

Find the possible values of the constant $k$ given that the matrix
$[\begin{aligned}1 & -2 & k \\ 1 & k & - k \\ -2 & k & k\end{aligned}]$ is singular.

Field `selection` (radio)
- $0$ only
- $0$ and $\frac{2}{5}$ only **correct**
- $- \frac{2}{5}$ only
- $\frac{2}{5}$ only
- $0$ and $- \frac{2}{5}$ only

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}1 & -2 & k \\ 1 & k & - k \\ -2 & k & k\end{aligned}| & =1|\begin{aligned}k & - k \\ k & k\end{aligned}|-(-2)|\begin{aligned}1 & - k \\ -2 & k\end{aligned}|+k|\begin{aligned}1 & k \\ -2 & k\end{aligned}| \\  & =1\big(k^{2}-(- k^{2})\big)-(-2)\big(k-(2 k)\big)+k\big(k-(- 2 k)\big) \\  & =1(2 k^{2})-(-2)(- k)+k(3 k) \\  & =2 k^{2}- 2 k+3 k^{2} \\  & =5 k^{2} - 2 k\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}5 k^{2} - 2 k & =0 \\ k (5 k - 2) & =0\end{aligned}
$$

Therefore, the solutions are $k=0$ and $k=\frac{2}{5}.$

### Generated authored default bank q-9911 seed 303

Find the possible values of the constant $k$ given that the matrix
$[\begin{aligned}1 & -2 & k \\ -4 & k & - k \\ 5 & k & k\end{aligned}]$ is singular.

Field `selection` (radio)
- $- \frac{2}{7}$ only
- $0$ and $- \frac{2}{7}$ only
- $\frac{2}{7}$ only
- $0$ only
- $0$ and $\frac{2}{7}$ only **correct**

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}1 & -2 & k \\ -4 & k & - k \\ 5 & k & k\end{aligned}| & =1|\begin{aligned}k & - k \\ k & k\end{aligned}|-(-2)|\begin{aligned}-4 & - k \\ 5 & k\end{aligned}|+k|\begin{aligned}-4 & k \\ 5 & k\end{aligned}| \\  & =1\big(k^{2}-(- k^{2})\big)-(-2)\big(- 4 k-(- 5 k)\big)+k\big(- 4 k-(5 k)\big) \\  & =1(2 k^{2})-(-2)(k)+k(- 9 k) \\  & =2 k^{2}+2 k- 9 k^{2} \\  & =- 7 k^{2} + 2 k\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have:

$$
\begin{aligned}- 7 k^{2} + 2 k & =0 \\ - k (7 k - 2) & =0\end{aligned}
$$

Therefore, the solutions are $k=0$ and $k=\frac{2}{7}.$

## Original q-9961 (:question.difficulty/easy)

Given that the determinant of  $[\begin{aligned}1 & n & 0 \\ 1 & 2 & 0 \\ -1 & 1 & 2\end{aligned}]$ is $-6$, find the value of $n.$

Field `selection`
- 1
- Any real number
- 5 **original correct**
- -1
- 0

**Original worked solution**

Let's use our formula to find an expression for the determinant in terms of $n:$

$$
\begin{aligned}|\begin{aligned}1 & n & 0 \\ 1 & 2 & 0 \\ -1 & 1 & 2\end{aligned}| & =1|\begin{aligned}2 & 0 \\ 1 & 2\end{aligned}|-n|\begin{aligned}1 & 0 \\ -1 & 2\end{aligned}|+0|\begin{aligned}1 & 2 \\ -1 & 1\end{aligned}| \\  & =4-n\cdot 2+0 \\  & =4-2n\end{aligned}
$$

Since the determinant of the matrix is $-6,$ we have:

$$
\begin{aligned}4-2n & =-6 \\ -2n & =-10 \\ n & =5\end{aligned}
$$

### Generated evidence-profile variant q-9961 seed 101

Given that the determinant of  $[\begin{aligned}1 & n & 0 \\ 1 & -5 & 0 \\ -1 & 3 & 2\end{aligned}]$ is $78$, find the value of $n.$

Field `selection` (radio)
- 1
- -1
- -44 **correct**
- Any real number
- 0

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $n:$

$$
\begin{aligned}|\begin{aligned}1 & n & 0 \\ 1 & -5 & 0 \\ -1 & 3 & 2\end{aligned}| & =1|\begin{aligned}-5 & 0 \\ 3 & 2\end{aligned}|-n|\begin{aligned}1 & 0 \\ -1 & 2\end{aligned}|+0|\begin{aligned}1 & -5 \\ -1 & 3\end{aligned}| \\  & =1(-10)-n(2)+0(-2) \\  & =- 2 n - 10\end{aligned}
$$

Since the determinant of the matrix is $78,$ we have:

$$
\begin{aligned}- 2 n - 10 & =78 \\ - 2 n & =88 \\ n & =-44\end{aligned}
$$

### Generated evidence-profile variant q-9961 seed 202

Given that the determinant of  $[\begin{aligned}1 & n & 0 \\ 1 & 2 & 0 \\ -2 & 1 & 2\end{aligned}]$ is $0$, find the value of $n.$

Field `selection` (radio)
- 2 **correct**
- 1
- Any real number
- 0
- -2

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $n:$

$$
\begin{aligned}|\begin{aligned}1 & n & 0 \\ 1 & 2 & 0 \\ -2 & 1 & 2\end{aligned}| & =1|\begin{aligned}2 & 0 \\ 1 & 2\end{aligned}|-n|\begin{aligned}1 & 0 \\ -2 & 2\end{aligned}|+0|\begin{aligned}1 & 2 \\ -2 & 1\end{aligned}| \\  & =1(4)-n(2)+0(5) \\  & =4 - 2 n\end{aligned}
$$

Since the determinant of the matrix is $0,$ we have:

$$
\begin{aligned}4 - 2 n & =0 \\ - 2 n & =-4 \\ n & =2\end{aligned}
$$

### Generated authored default bank q-9961 seed 303

Given that the determinant of  $[\begin{aligned}1 & n & 0 \\ -4 & 2 & 0 \\ -1 & 1 & 5\end{aligned}]$ is $16$, find the value of $n.$

Field `selection` (radio)
- 20
- -6
- 6
- - \frac{3}{10}
- \frac{3}{10} **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $n:$

$$
\begin{aligned}|\begin{aligned}1 & n & 0 \\ -4 & 2 & 0 \\ -1 & 1 & 5\end{aligned}| & =1|\begin{aligned}2 & 0 \\ 1 & 5\end{aligned}|-n|\begin{aligned}-4 & 0 \\ -1 & 5\end{aligned}|+0|\begin{aligned}-4 & 2 \\ -1 & 1\end{aligned}| \\  & =1(10)-n(-20)+0(-2) \\  & =20 n + 10\end{aligned}
$$

Since the determinant of the matrix is $16,$ we have:

$$
\begin{aligned}20 n + 10 & =16 \\ 20 n & =6 \\ n & =\frac{3}{10}\end{aligned}
$$

## Original q-280402 (:question.difficulty/easy)

Given that $B=[\begin{aligned}3 & 0 & 2 \\ 1 & k+2 & -5 \\ 4 & -1 & 6\end{aligned}]$ and $det(B)=70$, find the value of $k.$

$k=$
{{field-1}}

Field `field-1`
- \frac{67}{10} **original correct**

**Original worked solution**

Let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}\text{det}(B) & =|\begin{aligned}3 & 0 & 2 \\ 1 & k+2 & -5 \\ 4 & -1 & 6\end{aligned}| \\  & =3|\begin{aligned}k+2 & -5 \\ -1 & 6\end{aligned}|-0|\begin{aligned}1 & -5 \\ 4 & 6\end{aligned}|+2|\begin{aligned}1 & k+2 \\ 4 & -1\end{aligned}| \\  & =3(6\cdot (k+2)-(-5)(-1))+2(1\cdot (-1)-4\cdot (k+2)) \\  & =3(6k+12-5)+2(-1-4k-8) \\  & =3(6k+7)+2(-4k-9) \\  & =18k+21-8k-18 \\  & =10k+3\end{aligned}
$$

Since the determinant of the matrix is $70,$ we have

$$
\begin{aligned}10k+3 & =70 \\ 10k & =67 \\ k & =\frac{67}{10}.\end{aligned}
$$

### Generated evidence-profile variant q-280402 seed 101

Given that $B=[\begin{aligned}3 & 0 & 2 \\ 1 & k + 4 & -5 \\ -5 & -1 & 6\end{aligned}]$ and $det(B)=4$, find the value of $k.$

$k=$
{{field-1}}

Field `field-1` (blank)
- - \frac{13}{4} **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}\text{det}(B) & =|\begin{aligned}3 & 0 & 2 \\ 1 & k + 4 & -5 \\ -5 & -1 & 6\end{aligned}| \\  & =3|\begin{aligned}k + 4 & -5 \\ -1 & 6\end{aligned}|-0|\begin{aligned}1 & -5 \\ -5 & 6\end{aligned}|+2|\begin{aligned}1 & k + 4 \\ -5 & -1\end{aligned}| \\  & =3\big(6 k + 24-(5)\big)-0\big(6-(25)\big)+2\big(-1-(- 5 k - 20)\big) \\  & =3\big(6 k + 19\big)+0\big(-19\big)+2\big(5 k + 19\big) \\  & =3(6 k + 19)-0(-19)+2(5 k + 19) \\  & =18 k + 57+0+10 k + 38 \\  & =28 k + 95\end{aligned}
$$

Since the determinant of the matrix is $4,$ we have

$$
\begin{aligned}28 k + 95 & =4 \\ 28 k & =-91 \\ k & =- \frac{13}{4}.\end{aligned}
$$

### Generated evidence-profile variant q-280402 seed 202

Given that $B=[\begin{aligned}3 & 0 & 2 \\ 1 & k - 2 & -5 \\ 4 & -1 & -2\end{aligned}]$ and $det(B)=51$, find the value of $k.$

$k=$
{{field-1}}

Field `field-1` (blank)
- - \frac{20}{7} **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}\text{det}(B) & =|\begin{aligned}3 & 0 & 2 \\ 1 & k - 2 & -5 \\ 4 & -1 & -2\end{aligned}| \\  & =3|\begin{aligned}k - 2 & -5 \\ -1 & -2\end{aligned}|-0|\begin{aligned}1 & -5 \\ 4 & -2\end{aligned}|+2|\begin{aligned}1 & k - 2 \\ 4 & -1\end{aligned}| \\  & =3\big(4 - 2 k-(5)\big)-0\big(-2-(-20)\big)+2\big(-1-(4 k - 8)\big) \\  & =3\big(- 2 k - 1\big)+0\big(18\big)+2\big(7 - 4 k\big) \\  & =3(- 2 k - 1)-0(18)+2(7 - 4 k) \\  & =- 6 k - 3+0+14 - 8 k \\  & =11 - 14 k\end{aligned}
$$

Since the determinant of the matrix is $51,$ we have

$$
\begin{aligned}11 - 14 k & =51 \\ - 14 k & =40 \\ k & =- \frac{20}{7}.\end{aligned}
$$

## Original q-280543 (:question.difficulty/moderate)

Find, in **ascending order**, the values ​​of $x$ for which the following matrix is singular.

$$
A=[\begin{aligned}x+2 & 2x & 4 \\ 3 & x & x+1 \\ 1 & 0 & 3\end{aligned}]
$$

In ascending order, $x=$
{{field-1}} and $x=$
{{field-2}}.

Field `field-1`
- 0 **original correct**
Field `field-2`
- \frac{14}{5} **original correct**

**Original worked solution**

First, let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}x+2 & 2x & 4 \\ 3 & x & x+1 \\ 1 & 0 & 3\end{aligned}| & =(x+2)|\begin{aligned}x & x+1 \\ 0 & 3\end{aligned}|-2x|\begin{aligned}3 & x+1 \\ 1 & 3\end{aligned}|+4|\begin{aligned}3 & x \\ 1 & 0\end{aligned}| \\  & =(x+2)(3x)-2x(8-x)+4(-x) \\  & =3x(x+2)-2x(8-x)-4x \\  & =3{x}^{2}+6x-16x+2{x}^{2}-4x \\  & =5{x}^{2}-14x\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have
 

$$
\begin{aligned}5{x}^{2}-14x & =0 \\ x(5x-14) & =0 \\ x & =0\,\text{or}\,x=\frac{14}{5}.\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=0$ and $x=\frac{14}{5}.$

### Generated evidence-profile variant q-280543 seed 101

Find, in **ascending order**, the values ​​of $x$ for which the following matrix is singular.

$$
A=[\begin{aligned}x + 2 & 2 x & 4 \\ -5 & x & x + 1 \\ 3 & 0 & 3\end{aligned}]
$$

In ascending order, $x=$
{{field-1}} and $x=$
{{field-2}}.

Field `field-1` (blank)
- - \frac{10}{3} **correct**
Field `field-2` (blank)
- 0 **correct**

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}x + 2 & 2 x & 4 \\ -5 & x & x + 1 \\ 3 & 0 & 3\end{aligned}| & =(x + 2)|\begin{aligned}x & x + 1 \\ 0 & 3\end{aligned}|-2 x|\begin{aligned}-5 & x + 1 \\ 3 & 3\end{aligned}|+4|\begin{aligned}-5 & x \\ 3 & 0\end{aligned}| \\  & =(x + 2)(3 x)-2 x(- 3 x - 18)+4(- 3 x) \\  & =(x + 2)\big(3 x\big)- 2 x\big(- 3 x - 18\big)+4\big(- 3 x\big) \\  & =3 x^{2} + 6 x+6 x^{2} + 36 x- 12 x \\  & =9 x^{2} + 30 x\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have

$$
\begin{aligned}9 x^{2} + 30 x & =0 \\ 3 x (3 x + 10) & =0 \\ x & =- \frac{10}{3},\,0\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=- \frac{10}{3}$ and $x=0.$

### Generated evidence-profile variant q-280543 seed 202

Find, in **ascending order**, the values ​​of $x$ for which the following matrix is singular.

$$
A=[\begin{aligned}x + 2 & 2 x & 4 \\ 3 & x & x - 2 \\ 1 & 0 & 2\end{aligned}]
$$

In ascending order, $x=$
{{field-1}} and $x=$
{{field-2}}.

Field `field-1` (blank)
- 0 **correct**
Field `field-2` (blank)
- 4 **correct**

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $x:$

$$
\begin{aligned}|\begin{aligned}x + 2 & 2 x & 4 \\ 3 & x & x - 2 \\ 1 & 0 & 2\end{aligned}| & =(x + 2)|\begin{aligned}x & x - 2 \\ 0 & 2\end{aligned}|-2 x|\begin{aligned}3 & x - 2 \\ 1 & 2\end{aligned}|+4|\begin{aligned}3 & x \\ 1 & 0\end{aligned}| \\  & =(x + 2)(2 x)-2 x(8 - x)+4(- x) \\  & =(x + 2)\big(2 x\big)- 2 x\big(8 - x\big)+4\big(- x\big) \\  & =2 x^{2} + 4 x+2 x^{2} - 16 x- 4 x \\  & =4 x^{2} - 16 x\end{aligned}
$$

Since the matrix is singular, the determinant is $0,$ and we have

$$
\begin{aligned}4 x^{2} - 16 x & =0 \\ 4 x (x - 4) & =0 \\ x & =0,\,4\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=0$ and $x=4.$

## Original q-9913 (:question.difficulty/moderate)

Find the possible values of the constant $k$ given that the matrix  $[\begin{aligned}k & 0 & 0 \\ 0 & 3 & 1 \\ 0 & 6 & k\end{aligned}]$ is singular.

Field `selection`
- $-2$ and $2$ only
- $0$ only
- $-2$ and $0$ only
- $0$ and $2$ only **original correct**
- $-2$ only

**Original worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}k & 0 & 0 \\ 0 & 3 & 1 \\ 0 & 6 & k\end{aligned}| & =k|\begin{aligned}3 & 1 \\ 6 & k\end{aligned}|+0|\begin{aligned}0 & 1 \\ 0 & k\end{aligned}|+0|\begin{aligned}0 & 3 \\ 0 & 6\end{aligned}| \\  & =k(3k-6)+0+0 \\  & =k(3k-6)\end{aligned}
$$

Since the matrix is singular, the determinant is $0.$ So,  we have:

 

$$
\begin{aligned}k(3k-6) & =0 \\ 3k(k-2) & =0 \\ k & =0,2\end{aligned}
$$

Therefore, the solutions are $k=0$ and $k=2.$

### Generated evidence-profile variant q-9913 seed 101

Find the possible values of the constant $k$ given that the matrix  $[\begin{aligned}k & 0 & 0 \\ 0 & -2 & -1 \\ 0 & 6 & k\end{aligned}]$ is singular.

Field `selection` (radio)
- $-3$ and $3$ only
- $0$ and $3$ only **correct**
- $-3$ and $0$ only
- $0$ only
- $-3$ only

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}k & 0 & 0 \\ 0 & -2 & -1 \\ 0 & 6 & k\end{aligned}| & =k|\begin{aligned}-2 & -1 \\ 6 & k\end{aligned}|-0|\begin{aligned}0 & -1 \\ 0 & k\end{aligned}|+0|\begin{aligned}0 & -2 \\ 0 & 6\end{aligned}| \\  & =k(6 - 2 k)-0(0)+0(0) \\  & =k(6 - 2 k)\end{aligned}
$$

Since the matrix is singular, the determinant is $0.$ So,  we have:

$$
\begin{aligned}k(6 - 2 k) & =0 \\ - 2 k (k - 3) & =0 \\ k & =0,\,3\end{aligned}
$$

Therefore, the solutions are $k=0$ and $k=3.$

### Generated evidence-profile variant q-9913 seed 202

Find the possible values of the constant $k$ given that the matrix  $[\begin{aligned}k & 0 & 0 \\ 0 & 1 & 1 \\ 0 & 2 & k\end{aligned}]$ is singular.

Field `selection` (radio)
- $-2$ and $0$ only
- $-2$ and $2$ only
- $0$ only
- $-2$ only
- $0$ and $2$ only **correct**

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}k & 0 & 0 \\ 0 & 1 & 1 \\ 0 & 2 & k\end{aligned}| & =k|\begin{aligned}1 & 1 \\ 2 & k\end{aligned}|-0|\begin{aligned}0 & 1 \\ 0 & k\end{aligned}|+0|\begin{aligned}0 & 1 \\ 0 & 2\end{aligned}| \\  & =k(k - 2)-0(0)+0(0) \\  & =k(k - 2)\end{aligned}
$$

Since the matrix is singular, the determinant is $0.$ So,  we have:

$$
\begin{aligned}k(k - 2) & =0 \\ k (k - 2) & =0 \\ k & =0,\,2\end{aligned}
$$

Therefore, the solutions are $k=0$ and $k=2.$

### Generated authored default bank q-9913 seed 303

Find the possible values of the constant $k$ given that the matrix  $[\begin{aligned}k & 0 & 0 \\ 0 & 3 & 4 \\ 0 & 5 & k\end{aligned}]$ is singular.

Field `selection` (radio)
- $- \frac{20}{3}$ only
- $0$ and $- \frac{20}{3}$ only
- $\frac{20}{3}$ only
- $0$ only
- $0$ and $\frac{20}{3}$ only **correct**

**Worked solution**

First, let's use our formula to find an expression for the determinant in terms of $k:$

$$
\begin{aligned}|\begin{aligned}k & 0 & 0 \\ 0 & 3 & 4 \\ 0 & 5 & k\end{aligned}| & =k|\begin{aligned}3 & 4 \\ 5 & k\end{aligned}|-0|\begin{aligned}0 & 4 \\ 0 & k\end{aligned}|+0|\begin{aligned}0 & 3 \\ 0 & 5\end{aligned}| \\  & =k(3 k - 20)-0(0)+0(0) \\  & =k(3 k - 20)\end{aligned}
$$

Since the matrix is singular, the determinant is $0.$ So,  we have:

$$
\begin{aligned}k(3 k - 20) & =0 \\ k (3 k - 20) & =0 \\ k & =0,\,\frac{20}{3}\end{aligned}
$$

Therefore, the solutions are $k=0$ and $k=\frac{20}{3}.$

## Original q-128506 (:question.difficulty/moderate)

Given that the determinant of
$[\begin{aligned}1 & 6 & m \\ m & 3 & 0 \\ 2 & 1 & 1\end{aligned}]$
is $-29$, find all the possible values of $m.$

Field `selection`
- $1$ only
- $4$ and $8$ only **original correct**
- $-5$ and $1$ only
- $8$ only
- $-6$ and $3$ only

**Original worked solution**

Let's use our formula to find an expression for the determinant in terms of $m:$

$$
\begin{aligned}|\begin{aligned}1 & 6 & m \\ m & 3 & 0 \\ 2 & 1 & 1\end{aligned}| & =1|\begin{aligned}3 & 0 \\ 1 & 1\end{aligned}|-6|\begin{aligned}m & 0 \\ 2 & 1\end{aligned}|+m|\begin{aligned}m & 3 \\ 2 & 1\end{aligned}| \\  & =(3-0)-6(m-0)+m(m-6) \\  & =3-6m+{m}^{2}-6m \\  & ={m}^{2}-12m+3\end{aligned}
$$

Since the determinant of the matrix is $-29,$ we have:

$$
\begin{aligned}{m}^{2}-12m+3 & =-29 \\ {m}^{2}-12m+32 & =0 \\ m & =\frac{-(-12)\pm \sqrt{{12}^{2}-4\cdot 1\cdot 32}}{2\cdot 1} \\  & =\frac{12\pm \sqrt{16}}{2} \\  & =\frac{12\pm 4}{2} \\  & =6\pm 2\end{aligned}
$$

Therefore, the solutions are $m=4$ and $m=8.$

### Generated evidence-profile variant q-128506 seed 101

Given that the determinant of
$[\begin{aligned}1 & 6 & m \\ m & -5 & 0 \\ 2 & 3 & 1\end{aligned}]$
is $219$, find all the possible values of $m.$

Field `selection` (radio)
- $1$ only
- $8$ only
- $-5$ and $1$ only
- $- \frac{28}{3}$ and $8$ only **correct**
- $-6$ and $-5$ only

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $m:$

$$
\begin{aligned}|\begin{aligned}1 & 6 & m \\ m & -5 & 0 \\ 2 & 3 & 1\end{aligned}| & =1|\begin{aligned}-5 & 0 \\ 3 & 1\end{aligned}|-6|\begin{aligned}m & 0 \\ 2 & 1\end{aligned}|+m|\begin{aligned}m & -5 \\ 2 & 3\end{aligned}| \\  & =1(-5)-6(m)+m(3 m + 10) \\  & =-5- 6 m+3 m^{2} + 10 m \\  & =3 m^{2} + 4 m - 5\end{aligned}
$$

Since the determinant of the matrix is $219,$ we have:

$$
\begin{aligned}3 m^{2} + 4 m - 5 & =219 \\ 3 m^{2} + 4 m - 224 & =0 \\ m & =\frac{-(4)\pm\sqrt{(4)^2-4\cdot 3\cdot (-224)}}{2\cdot 3} \\  & =\frac{-4\pm\sqrt{2704}}{6} \\  & =\frac{-4\pm 52}{6} \\  & =- \frac{28}{3},8\end{aligned}
$$

Therefore, the solutions are $m=- \frac{28}{3}$ and $m=8.$

### Generated evidence-profile variant q-128506 seed 202

Given that the determinant of
$[\begin{aligned}1 & 6 & m \\ m & 3 & 0 \\ -2 & 1 & 2\end{aligned}]$
is $22$, find all the possible values of $m.$

Field `selection` (radio)
- $-5$ and $1$ only
- $1$ only
- $-2$ and $8$ only **correct**
- $-6$ and $3$ only
- $8$ only

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $m:$

$$
\begin{aligned}|\begin{aligned}1 & 6 & m \\ m & 3 & 0 \\ -2 & 1 & 2\end{aligned}| & =1|\begin{aligned}3 & 0 \\ 1 & 2\end{aligned}|-6|\begin{aligned}m & 0 \\ -2 & 2\end{aligned}|+m|\begin{aligned}m & 3 \\ -2 & 1\end{aligned}| \\  & =1(6)-6(2 m)+m(m + 6) \\  & =6- 12 m+m^{2} + 6 m \\  & =m^{2} - 6 m + 6\end{aligned}
$$

Since the determinant of the matrix is $22,$ we have:

$$
\begin{aligned}m^{2} - 6 m + 6 & =22 \\ m^{2} - 6 m - 16 & =0 \\ m & =\frac{-(-6)\pm\sqrt{(-6)^2-4\cdot 1\cdot (-16)}}{2\cdot 1} \\  & =\frac{6\pm\sqrt{100}}{2} \\  & =\frac{6\pm 10}{2} \\  & =-2,8\end{aligned}
$$

Therefore, the solutions are $m=-2$ and $m=8.$

### Generated authored default bank q-128506 seed 303

Given that the determinant of
$[\begin{aligned}1 & 6 & m \\ m & 3 & 0 \\ 2 & 2 & -3\end{aligned}]$
is $101$, find all the possible values of $m.$

Field `selection` (radio)
- $5$ only
- $0$ and $-6$ only
- $-11$ only
- $11$ and $-5$ only
- $-11$ and $5$ only **correct**

**Worked solution**

Let's use our formula to find an expression for the determinant in terms of $m:$

$$
\begin{aligned}|\begin{aligned}1 & 6 & m \\ m & 3 & 0 \\ 2 & 2 & -3\end{aligned}| & =1|\begin{aligned}3 & 0 \\ 2 & -3\end{aligned}|-6|\begin{aligned}m & 0 \\ 2 & -3\end{aligned}|+m|\begin{aligned}m & 3 \\ 2 & 2\end{aligned}| \\  & =1(-9)-6(- 3 m)+m(2 m - 6) \\  & =-9+18 m+2 m^{2} - 6 m \\  & =2 m^{2} + 12 m - 9\end{aligned}
$$

Since the determinant of the matrix is $101,$ we have:

$$
\begin{aligned}2 m^{2} + 12 m - 9 & =101 \\ 2 m^{2} + 12 m - 110 & =0 \\ m & =\frac{-(12)\pm\sqrt{(12)^2-4\cdot 2\cdot (-110)}}{2\cdot 2} \\  & =\frac{-12\pm\sqrt{1024}}{4} \\  & =\frac{-12\pm 32}{4} \\  & =-11,5\end{aligned}
$$

Therefore, the solutions are $m=-11$ and $m=5.$
