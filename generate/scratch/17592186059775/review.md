## q-10329

Original replay

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}2 & 3 & 7 \\ 3 & -2 & 4\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & -5 & -3 \\ 0 & 1 & 5\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{3}{2} & \frac{7}{2} \\ 0 & 1 & 2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{3}{2} & \frac{7}{2} \\ 0 & 1 & 1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 5 & -3 \\ 0 & 1 & 1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{7}{2} & \frac{3}{2} \\ 0 & 1 & 1\end{array}\right]$

Reducing $M$ to row echelon form using the standard algorithm for Gaussian elimination, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}2 & 3 & 7 \\ 3 & -2 & 4\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{3}{2} & \frac{7}{2} \\ 3 & -2 & 4\end{array}\right] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{3}{2} & \frac{7}{2} \\ 0 & -\frac{13}{2} & -\frac{13}{2}\end{array}\right] & {R}_{2} & :=-\frac{2}{13}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{3}{2} & \frac{7}{2} \\ 0 & 1 & 1\end{array}\right].\end{aligned}
$$

Changed RHS, fixed coefficients and stages

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}2 & 3 & 21 \\  3 & -2 & 12\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & -5 & -9 \\  0 & 1 & 15\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{3}{2} & \frac{21}{2} \\  0 & 1 & 6\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{3}{2} & \frac{21}{2} \\  0 & 1 & 3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 5 & -9 \\  0 & 1 & 3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{7}{2} & \frac{9}{2} \\  0 & 1 & 3\end{array}\right]$

Reducing $M$ to row echelon form using the standard algorithm for Gaussian elimination, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}2 & 3 & 21 \\  3 & -2 & 12\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{3}{2} & \frac{21}{2} \\  3 & -2 & 12\end{array}\right] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{3}{2} & \frac{21}{2} \\  0 & -\frac{13}{2} & -\frac{39}{2}\end{array}\right] & {R}_{2} & :=-\frac{2}{13}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{3}{2} & \frac{21}{2} \\  0 & 1 & 3\end{array}\right].\end{aligned}
$$

## q-1059

Original replay

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}1 & 1 & 8 \\ -1 & -2 & 3\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then solve the linear system represented by the matrix.

- $M∼\left[\begin{array}{cc|c}1 & 1 & 8 \\ 0 & 1 & 14\end{array}\right],$
$\,x=13$ and $y=14$
- $M∼\left[\begin{array}{cc|c}1 & 1 & 8 \\ 0 & 1 & 13\end{array}\right],$
$\,x=11$ and $y=13$
- $M∼\left[\begin{array}{cc|c}1 & 1 & 8 \\ 0 & 1 & -11\end{array}\right],$
$\,x=19$ and $y=-11$
- $M∼\left[\begin{array}{cc|c}1 & 1 & 8 \\ 0 & 1 & -16\end{array}\right],$
$\,x=17$ and $y=-16$
- $M∼\left[\begin{array}{cc|c}1 & 1 & 8 \\ 0 & 1 & 11\end{array}\right],$
$\,x=10$ and $y=11$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}1 & 1 & 8 \\ -1 & -2 & 3\end{array}\right] & {R}_{2} & :={R}_{2}+1\cdot {R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 1 & 8 \\ 0 & -1 & 11\end{array}\right] & {R}_{2} & :=-1\cdot {R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & 1 & 8 \\ 0 & 1 & -11\end{array}\right].\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x+y &=8 \\ y &=-11,\end{aligned}\right.
$$

and we can apply back substitution. The final equation $y=-11$ tells us the value of $y.$ Substituting this value into the first equation, we get

$$
x+(-11)=8\,⇒\,x=8+11=19.
$$

Therefore, the solution is $x=19$ and $y=-11.$

Changed RHS, fixed coefficients and stages

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}1 & 1 & 16 \\  -1 & -2 & 6\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then solve the linear system represented by the matrix.

- $M∼\left[\begin{array}{cc|c}1 & 1 & 16 \\  0 & 1 & 28\end{array}\right],$
$\,x=26$ and $y=28$
- $M∼\left[\begin{array}{cc|c}1 & 1 & 16 \\  0 & 1 & 26\end{array}\right],$
$\,x=22$ and $y=26$
- $M∼\left[\begin{array}{cc|c}1 & 1 & 16 \\  0 & 1 & -22\end{array}\right],$
$\,x=38$ and $y=-22$
- $M∼\left[\begin{array}{cc|c}1 & 1 & 16 \\  0 & 1 & -32\end{array}\right],$
$\,x=34$ and $y=-32$
- $M∼\left[\begin{array}{cc|c}1 & 1 & 16 \\  0 & 1 & 22\end{array}\right],$
$\,x=20$ and $y=22$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}1 & 1 & 16 \\  -1 & -2 & 6\end{array}\right] & {R}_{2} & :={R}_{2}+1\cdot {R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 1 & 16 \\  0 & -1 & 22\end{array}\right] & {R}_{2} & :=-1\cdot {R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & 1 & 16 \\  0 & 1 & -22\end{array}\right].\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x+y &=16 \\ y &=-22,\end{aligned}\right.
$$

and we can apply back substitution. The final equation $y=-22$ tells us the value of $y.$ Substituting this value into the first equation, we get

$$
x+(-22)=16\,⇒\,x=16+22=38.
$$

Therefore, the solution is $x=38$ and $y=-22.$

## q-1060

Original replay

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}-1 & 2 & 1 \\ 5 & 6 & 8\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & -2 & -1 \\ 0 & 1 & \frac{11}{16}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -2 & -1 \\ 0 & 1 & \frac{13}{16}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -2 & -1 \\ 0 & 1 & \frac{15}{16}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -2 & -1 \\ 0 & 1 & \frac{17}{16}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -2 & -1 \\ 0 & 1 & \frac{9}{16}\end{array}\right]$

Reducing $M$ to row echelon form using the standard algorithm for Gaussian elimination, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}-1 & 2 & 1 \\ 5 & 6 & 8\end{array}\right] & {R}_{1} & :=-1\cdot {R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & -1 \\ 5 & 6 & 8\end{array}\right] & {R}_{2} & :={R}_{2}-5\cdot {R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & -1 \\ 0 & 16 & 13\end{array}\right] & {R}_{2} & :=\frac{1}{16}\cdot {R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & -1 \\ 0 & 1 & \frac{13}{16}\end{array}\right].\end{aligned}
$$

Changed RHS, fixed coefficients and stages

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}-1 & 2 & 3 \\  5 & 6 & 24\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & -2 & -3 \\  0 & 1 & \frac{33}{16}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -2 & -3 \\  0 & 1 & \frac{39}{16}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -2 & -3 \\  0 & 1 & \frac{45}{16}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -2 & -3 \\  0 & 1 & \frac{51}{16}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -2 & -3 \\  0 & 1 & \frac{27}{16}\end{array}\right]$

Reducing $M$ to row echelon form using the standard algorithm for Gaussian elimination, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}-1 & 2 & 3 \\  5 & 6 & 24\end{array}\right] & {R}_{1} & :=-1\cdot {R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & -3 \\  5 & 6 & 24\end{array}\right] & {R}_{2} & :={R}_{2}-5\cdot {R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & -3 \\  0 & 16 & 39\end{array}\right] & {R}_{2} & :=\frac{1}{16}\cdot {R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & -3 \\  0 & 1 & \frac{39}{16}\end{array}\right].\end{aligned}
$$

## q-130910

Original replay

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}1 & 7 & -2 \\ 2 & 10 & 0\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then solve the linear system represented by the matrix.

- $M∼\left[\begin{array}{cc|c}1 & 7 & -1 \\ 0 & 1 & -2\end{array}\right],$ $\,x=12$ and $y=-2$
- $M∼\left[\begin{array}{cc|c}1 & 7 & -2 \\ 0 & 1 & -1\end{array}\right],$ $\,x=13$ and $y=-1$
- $M∼\left[\begin{array}{cc|c}1 & 7 & -1 \\ 0 & 1 & 1\end{array}\right],$ $\,x=15$ and $y=1$
- $M∼\left[\begin{array}{cc|c}1 & 7 & -2 \\ 0 & 1 & -1\end{array}\right],$ $\,x=5$ and $y=-1$
- $M∼\left[\begin{array}{cc|c}1 & 7 & -1 \\ 0 & 1 & 2\end{array}\right],$ $\,x=12$ and $y=2$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}1 & 7 & -2 \\ 2 & 10 & 0\end{array}\right] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 7 & -2 \\ 0 & -4 & 4\end{array}\right] & {R}_{2} & :=-\frac{1}{4}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & 7 & -2 \\ 0 & 1 & -1\end{array}\right].\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x+7y &=-2 \\ y &=-1,\end{aligned}\right.
$$

and we can apply back substitution. The final equation $y=-1$ tells us the value of $y.$ Substituting this value into the first equation, we get

$$
x+7(-1)=-2\,⇒\,x=-2+7=5.
$$

Therefore, the solution is $x=5$ and $y=-1.$

Changed RHS, fixed coefficients and stages

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}1 & 7 & -6 \\  2 & 10 & 0\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then solve the linear system represented by the matrix.

- $M∼\left[\begin{array}{cc|c}1 & 7 & -3 \\  0 & 1 & -6\end{array}\right],$ $\,x=36$ and $y=-6$
- $M∼\left[\begin{array}{cc|c}1 & 7 & -6 \\  0 & 1 & -3\end{array}\right],$ $\,x=39$ and $y=-3$
- $M∼\left[\begin{array}{cc|c}1 & 7 & -3 \\  0 & 1 & 3\end{array}\right],$ $\,x=45$ and $y=3$
- $M∼\left[\begin{array}{cc|c}1 & 7 & -6 \\  0 & 1 & -3\end{array}\right],$ $\,x=15$ and $y=-3$
- $M∼\left[\begin{array}{cc|c}1 & 7 & -3 \\  0 & 1 & 6\end{array}\right],$ $\,x=36$ and $y=6$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}1 & 7 & -6 \\  2 & 10 & 0\end{array}\right] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 7 & -6 \\  0 & -4 & 12\end{array}\right] & {R}_{2} & :=-\frac{1}{4}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & 7 & -6 \\  0 & 1 & -3\end{array}\right].\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x+7y &=-6 \\ y &=-3,\end{aligned}\right.
$$

and we can apply back substitution. The final equation $y=-3$ tells us the value of $y.$ Substituting this value into the first equation, we get

$$
x+7(-3)=-6\,⇒\,x=-6+21=15.
$$

Therefore, the solution is $x=15$ and $y=-3.$

## q-20459

Original replay

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}3 & -6 & 10 \\ 2 & -3 & 5\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then solve the linear system represented by the matrix.

- $M∼\left[\begin{array}{cc|c}1 & 2 & 4 \\ 0 & 1 & -3\end{array}\right],$
$\,x=0$ and $y=\frac{5}{3}$
- $M∼\left[\begin{array}{cc|c}1 & -2 & -4 \\ 0 & 1 & \frac{1}{3}\end{array}\right],$
$\,x=-\frac{5}{3}$ and $y=\frac{1}{3}$
- $M∼\left[\begin{array}{cc|c}1 & -2 & \frac{10}{3} \\ 0 & 1 & -3\end{array}\right],$
$\,x=-\frac{8}{3}$ and $y=-3$
- $M∼\left[\begin{array}{cc|c}1 & -2 & \frac{10}{3} \\ 0 & 1 & -\frac{5}{3}\end{array}\right],$
$\,x=0$ and $y=-\frac{5}{3}$
- $M∼\left[\begin{array}{cc|c}1 & -2 & \frac{10}{3} \\ 0 & 1 & \frac{5}{3}\end{array}\right],$
$\,x=\frac{20}{3}$ and $y=\frac{5}{3}$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}3 & -6 & 10 \\ 2 & -3 & 5\end{array}\right] & {R}_{1} & :=\frac{1}{3}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & \frac{10}{3} \\ 2 & -3 & 5\end{array}\right] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & \frac{10}{3} \\ 0 & 1 & -\frac{5}{3}\end{array}\right].\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x-2y &=\frac{10}{3} \\ y &=-\frac{5}{3},\end{aligned}\right.
$$

and we can apply back substitution. The final equation $y=-\frac{5}{3}$ tells us the value of $y.$ Substituting this value into the first equation, we get

$$
x-2(-\frac{5}{3})=\frac{10}{3}\,⇒\,x=\frac{10}{3}-\frac{10}{3}=0.
$$

Thus, the solution is $x=0$ and $y=-\frac{5}{3}.$

Changed RHS, fixed coefficients and stages

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}3 & -6 & 20 \\  2 & -3 & 10\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then solve the linear system represented by the matrix.

- $M∼\left[\begin{array}{cc|c}1 & 2 & 8 \\  0 & 1 & -6\end{array}\right],$
$\,x=0$ and $y=\frac{10}{3}$
- $M∼\left[\begin{array}{cc|c}1 & -2 & -8 \\  0 & 1 & \frac{2}{3}\end{array}\right],$
$\,x=-\frac{10}{3}$ and $y=\frac{2}{3}$
- $M∼\left[\begin{array}{cc|c}1 & -2 & \frac{20}{3} \\  0 & 1 & -6\end{array}\right],$
$\,x=-\frac{16}{3}$ and $y=-6$
- $M∼\left[\begin{array}{cc|c}1 & -2 & \frac{20}{3} \\  0 & 1 & -\frac{10}{3}\end{array}\right],$
$\,x=0$ and $y=-\frac{10}{3}$
- $M∼\left[\begin{array}{cc|c}1 & -2 & \frac{20}{3} \\  0 & 1 & \frac{10}{3}\end{array}\right],$
$\,x=\frac{40}{3}$ and $y=\frac{10}{3}$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}3 & -6 & 20 \\  2 & -3 & 10\end{array}\right] & {R}_{1} & :=\frac{1}{3}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & \frac{20}{3} \\  2 & -3 & 10\end{array}\right] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & \frac{20}{3} \\  0 & 1 & -\frac{10}{3}\end{array}\right].\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x-2y &=\frac{20}{3} \\ y &=-\frac{10}{3},\end{aligned}\right.
$$

and we can apply back substitution. The final equation $y=-\frac{10}{3}$ tells us the value of $y.$ Substituting this value into the first equation, we get

$$
x-2(-\frac{10}{3})=\frac{20}{3}\,⇒\,x=\frac{20}{3}-\frac{20}{3}=0.
$$

Thus, the solution is $x=0$ and $y=-\frac{10}{3}.$

## q-20461

Original replay

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}2 & -6 & -9 \\ 1 & -2 & -4\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then solve the linear system represented by the matrix.

- $M∼\left[\begin{array}{cc|c}1 & 3 & -\frac{9}{2} \\ 0 & 1 & -\frac{17}{2}\end{array}\right],$
$\,x=-1$ and $y=-\frac{17}{2}$
- $M∼\left[\begin{array}{cc|c}1 & -3 & -\frac{9}{2} \\ 0 & 1 & \frac{1}{2}\end{array}\right],$
$\,x=-3$ and $y=\frac{1}{2}$
- $M∼\left[\begin{array}{cc|c}1 & -3 & \frac{9}{2} \\ 0 & 1 & -\frac{1}{2}\end{array}\right],$
$\,x=3$ and $y=-\frac{1}{2}$
- $M∼\left[\begin{array}{cc|c}1 & -2 & -5 \\ 0 & 1 & \frac{17}{2}\end{array}\right],$
$\,x=\frac{4}{2}$ and $y=\frac{15}{2}$
- $M∼\left[\begin{array}{cc|c}1 & -3 & -3 \\ 0 & 1 & \frac{9}{2}\end{array}\right],$
$\,x=\frac{1}{2}$ and $y=-\frac{9}{2}$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}2 & -6 & -9 \\ 1 & -2 & -4\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & -\frac{9}{2} \\ 1 & -2 & -4\end{array}\right] & {R}_{2} & :={R}_{2}-{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & -\frac{9}{2} \\ 0 & 1 & \frac{1}{2}\end{array}\right].\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x-3y &=-\frac{9}{2} \\ y &=\frac{1}{2}\end{aligned}\right.
$$

and we can apply back substitution. The final equation $y=\frac{1}{2}$ tells us the value of $y.$ Substituting this value into the first equation, we get

$$
x-3(\frac{1}{2})=-\frac{9}{2}\,⇒\,x=-\frac{9}{2}+\frac{3}{2}=-3.
$$

Thus, the solution is $x=-3$ and $y=\frac{1}{2}.$

Changed RHS, fixed coefficients and stages

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}2 & -6 & -27 \\  1 & -2 & -12\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form, and then solve the linear system represented by the matrix.

- $M∼\left[\begin{array}{cc|c}1 & 3 & -\frac{27}{2} \\  0 & 1 & -\frac{51}{2}\end{array}\right],$
$\,x=-3$ and $y=-\frac{51}{2}$
- $M∼\left[\begin{array}{cc|c}1 & -3 & -\frac{27}{2} \\  0 & 1 & \frac{3}{2}\end{array}\right],$
$\,x=-9$ and $y=\frac{3}{2}$
- $M∼\left[\begin{array}{cc|c}1 & -3 & \frac{27}{2} \\  0 & 1 & -\frac{3}{2}\end{array}\right],$
$\,x=9$ and $y=-\frac{3}{2}$
- $M∼\left[\begin{array}{cc|c}1 & -2 & -15 \\  0 & 1 & \frac{51}{2}\end{array}\right],$
$\,x=6$ and $y=\frac{45}{2}$
- $M∼\left[\begin{array}{cc|c}1 & -3 & -9 \\  0 & 1 & \frac{27}{2}\end{array}\right],$
$\,x=\frac{3}{2}$ and $y=-\frac{27}{2}$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}2 & -6 & -27 \\  1 & -2 & -12\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & -\frac{27}{2} \\  1 & -2 & -12\end{array}\right] & {R}_{2} & :={R}_{2}-{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & -\frac{27}{2} \\  0 & 1 & \frac{3}{2}\end{array}\right].\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x-3y &=-\frac{27}{2} \\ y &=\frac{3}{2}\end{aligned}\right.
$$

and we can apply back substitution. The final equation $y=\frac{3}{2}$ tells us the value of $y.$ Substituting this value into the first equation, we get

$$
x-3(\frac{3}{2})=-\frac{27}{2}\,⇒\,x=-\frac{27}{2}+\frac{9}{2}=-9.
$$

Thus, the solution is $x=-9$ and $y=\frac{3}{2}.$

## q-10512

Excluded source bank: both the keyed REF and another offered RREF represent the same system.

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}3 & -2 & 4 \\ 6 & 4 & -8\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & \frac{4}{3} \\ 0 & 1 & -2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & \frac{4}{3} \\ 0 & 1 & 2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 0 & 0 \\ 0 & 1 & -2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -\frac{4}{3} & \frac{4}{3} \\ 0 & 1 & -2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -\frac{4}{3} & \frac{4}{3} \\ 0 & 1 & -1\end{array}\right]$

Reducing $M$ to row echelon form using the standard algorithm for Gaussian elimination, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}3 & -2 & 4 \\ 6 & 4 & -8\end{array}\right] & {R}_{1} & :=\frac{1}{3}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & \frac{4}{3} \\ 6 & 4 & -8\end{array}\right] & {R}_{2} & :={R}_{2}-6{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & \frac{4}{3} \\ 0 & 8 & -16\end{array}\right] & {R}_{2} & :=\frac{1}{8}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & \frac{4}{3} \\ 0 & 1 & -2\end{array}\right].\end{aligned}
$$

## q-130909

Original replay

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}2 & -8 & 6 \\ 3 & -7 & 4\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & -4 & 3 \\ 0 & 1 & 1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -8 & 6 \\ 0 & 1 & -1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 8 & -6 \\ 0 & 1 & 1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -4 & 3 \\ 0 & 1 & -1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 4 & -3 \\ 0 & 1 & -1\end{array}\right]$

Reducing $M$ to row echelon form using the standard algorithm for Gaussian elimination, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}2 & -8 & 6 \\ 3 & -7 & 4\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -4 & 3 \\ 3 & -7 & 4\end{array}\right] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -4 & 3 \\ 0 & 5 & -5\end{array}\right] & {R}_{2} & :=\frac{1}{5}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -4 & 3 \\ 0 & 1 & -1\end{array}\right].\end{aligned}
$$

Changed RHS, fixed coefficients and stages

Consider the augmented matrix $M$ given by

$$
M=\left[\begin{array}{cc|c}2 & -8 & 18 \\  3 & -7 & 12\end{array}\right].
$$

Use the standard method of Gaussian elimination to reduce $M$ to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & -4 & 9 \\  0 & 1 & 3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -8 & 18 \\  0 & 1 & -3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 8 & -18 \\  0 & 1 & 3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -4 & 9 \\  0 & 1 & -3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 4 & -9 \\  0 & 1 & -3\end{array}\right]$

Reducing $M$ to row echelon form using the standard algorithm for Gaussian elimination, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}2 & -8 & 18 \\  3 & -7 & 12\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -4 & 9 \\  3 & -7 & 12\end{array}\right] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -4 & 9 \\  0 & 5 & -15\end{array}\right] & {R}_{2} & :=\frac{1}{5}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -4 & 9 \\  0 & 1 & -3\end{array}\right].\end{aligned}
$$
