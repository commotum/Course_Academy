## q-10522 (easy)

Source

Consider the system of linear equations

$$
\left\{\begin{aligned}x-3y &=-8 \\ 2x+4y &=4.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then solve the linear system.

- $M∼\left[\begin{array}{cc|c}1 & -3 & -8 \\ 0 & 1 & -2\end{array}\right],$
$\,x=-4$ and $y=1$
- $M∼\left[\begin{array}{cc|c}1 & 0 & -8 \\ 0 & 1 & 2\end{array}\right],$
$\,x=-8$ and $y=2$
- $M∼\left[\begin{array}{cc|c}1 & -3 & -8 \\ 0 & 1 & 2\end{array}\right],$
$\,x=-2$ and $y=2$
- $M∼\left[\begin{array}{cc|c}1 & -3 & -8 \\ 0 & 1 & 1\end{array}\right],$
$\,x=-4$ and $y=1$
- $M∼\left[\begin{array}{cc|c}1 & -3 & -8 \\ 0 & 1 & 5\end{array}\right],$
$\,x=-2$ and $y=2$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}1 & -3 & -8 \\ 2 & 4 & 4\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}1 & -3 & -8 \\ 2 & 4 & 4\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & -8 \\ 0 & 10 & 20\end{array}\right] & {R}_{2} & :=\frac{1}{10}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & -8 \\ 0 & 1 & 2\end{array}\right].\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}x-3y &=-8 \\ y &=2,\end{aligned}\right.
$$

and we can apply back substitution. The final equation $y=2$ tells us the value of $y.$ Substituting this value into the first equation, we get

$$
x-3(2)=-8\,⇒\,x=-2.
$$

Therefore, the solution is $x=-2$ and $y=2.$

Offsets h=2, k=-1

Consider the system of linear equations

$$
\left\{\begin{aligned}x-3y &=-3 \\ 2x+4y &=4.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then solve the linear system.

- $M∼\left[\begin{array}{cc|c}1 & -3 & -3 \\ 0 & 1 & -3\end{array}\right],$
$\,x=-2$ and $y=0$
- $M∼\left[\begin{array}{cc|c}1 & 0 & -6 \\ 0 & 1 & 1\end{array}\right],$
$\,x=-6$ and $y=1$
- $M∼\left[\begin{array}{cc|c}1 & -3 & -3 \\ 0 & 1 & 1\end{array}\right],$
$\,x=0$ and $y=1$
- $M∼\left[\begin{array}{cc|c}1 & -3 & -3 \\ 0 & 1 & 0\end{array}\right],$
$\,x=-2$ and $y=0$
- $M∼\left[\begin{array}{cc|c}1 & -3 & -3 \\ 0 & 1 & 4\end{array}\right],$
$\,x=0$ and $y=1$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}1 & -3 & -3 \\ 2 & 4 & 4\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}1 & -3 & -3 \\ 2 & 4 & 4\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & -3 \\ 0 & 10 & 10\end{array}\right] & {R}_{2} & :=\frac{1}{10}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & -3 \\ 0 & 1 & 1\end{array}\right].\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}x-3y &=-3 \\ y &=1,\end{aligned}\right.
$$

and we can apply back substitution. The final equation $y=1$ tells us the value of $y.$ Substituting this value into the first equation, we get

$$
x-3(1)=-3\,⇒\,x=0.
$$

Therefore, the solution is $x=0$ and $y=1.$

## q-20496 (moderate)

Source

Consider the system of linear equations

$$
\left\{\begin{aligned}2x+7y &=-5 \\ 7x+11y &=-4.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & \frac{7}{2} & -\frac{5}{2} \\ 0 & 1 & -3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 7 & -5 \\ 0 & 1 & -2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{7}{2} & -\frac{5}{2} \\ 0 & 1 & -1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 7 & -5 \\ 0 & 1 & 0\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{7}{2} & -\frac{5}{2} \\ 0 & 1 & 1\end{array}\right]$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}2 & 7 & -5 \\ 7 & 11 & -4\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}2 & 7 & -5 \\ 7 & 11 & -4\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{7}{2} & -\frac{5}{2} \\ 7 & 11 & -4\end{array}\right] & {R}_{2} & :={R}_{2}-7{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{7}{2} & -\frac{5}{2} \\ 0 & -\frac{27}{2} & \frac{27}{2}\end{array}\right] & {R}_{2} & :=-\frac{2}{27}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{7}{2} & -\frac{5}{2} \\ 0 & 1 & -1\end{array}\right].\end{aligned}
$$

Offsets h=2, k=-1

Consider the system of linear equations

$$
\left\{\begin{aligned}2x+7y &=-8 \\ 7x+11y &=-1.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & \frac{7}{2} & -4 \\ 0 & 1 & -4\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 7 & -10 \\ 0 & 1 & -3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{7}{2} & -4 \\ 0 & 1 & -2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 7 & -10 \\ 0 & 1 & -1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{7}{2} & -4 \\ 0 & 1 & 0\end{array}\right]$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}2 & 7 & -8 \\ 7 & 11 & -1\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}2 & 7 & -8 \\ 7 & 11 & -1\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{7}{2} & -4 \\ 7 & 11 & -1\end{array}\right] & {R}_{2} & :={R}_{2}-7{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{7}{2} & -4 \\ 0 & -\frac{27}{2} & 27\end{array}\right] & {R}_{2} & :=-\frac{2}{27}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{7}{2} & -4 \\ 0 & 1 & -2\end{array}\right].\end{aligned}
$$

## q-20497 (moderate)

Source

Consider the system of linear equations

$$
\left\{\begin{aligned}3x+8y &=22 \\ 7x-5y &=4.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{22}{3} \\ 0 & 1 & 0\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{22}{3} \\ 0 & 1 & -1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{22}{3} \\ 0 & 1 & 3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{22}{3} \\ 0 & 1 & 2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{22}{3} \\ 0 & 1 & 1\end{array}\right]$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}3 & 8 & 22 \\ 7 & -5 & 4\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}3 & 8 & 22 \\ 7 & -5 & 4\end{array}\right] & {R}_{1} & :=\frac{1}{3}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{22}{3} \\ 7 & -5 & 4\end{array}\right] & {R}_{2} & :={R}_{2}-7{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{22}{3} \\ 0 & -\frac{71}{3} & -\frac{142}{3}\end{array}\right] & {R}_{2} & :=-\frac{3}{71}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{22}{3} \\ 0 & 1 & 2\end{array}\right].\end{aligned}
$$

Offsets h=2, k=-1

Consider the system of linear equations

$$
\left\{\begin{aligned}3x+8y &=20 \\ 7x-5y &=23.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{20}{3} \\ 0 & 1 & -1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{20}{3} \\ 0 & 1 & -2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{20}{3} \\ 0 & 1 & 2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{20}{3} \\ 0 & 1 & 1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{20}{3} \\ 0 & 1 & 0\end{array}\right]$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}3 & 8 & 20 \\ 7 & -5 & 23\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}3 & 8 & 20 \\ 7 & -5 & 23\end{array}\right] & {R}_{1} & :=\frac{1}{3}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{20}{3} \\ 7 & -5 & 23\end{array}\right] & {R}_{2} & :={R}_{2}-7{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{20}{3} \\ 0 & -\frac{71}{3} & -\frac{71}{3}\end{array}\right] & {R}_{2} & :=-\frac{3}{71}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{8}{3} & \frac{20}{3} \\ 0 & 1 & 1\end{array}\right].\end{aligned}
$$

## q-20500 (moderate)

Source

Consider the system of linear equations

$$
\left\{\begin{aligned}x+\frac{1}{3}y &=11 \\ 3x+\frac{1}{5}y &=9.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then solve the linear system.

- $M∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & 11 \\ 0 & 1 & -3\end{array}\right],$
$\,x=12$ and $y=-3$
- $M∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & 11 \\ 0 & 1 & 6\end{array}\right],$
$\,x=9$ and $y=6$
- $M∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & 11 \\ 0 & 1 & 3\end{array}\right],$
$\,x=10$ and $y=3$
- $M∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & 11 \\ 0 & 1 & 30\end{array}\right],$
$\,x=1$ and $y=30$
- $M∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & 11 \\ 0 & 1 & 0\end{array}\right],$
$\,x=11$ and $y=0$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}1 & \frac{1}{3} & 11 \\ 3 & \frac{1}{5} & 9\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & 11 \\ 3 & \frac{1}{5} & 9\end{array}\right] & {R}_{2} & :={R}_{2}-3{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & 11 \\ 0 & -\frac{4}{5} & -24\end{array}\right] & {R}_{2} & :=-\frac{5}{4}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & 11 \\ 0 & 1 & 30\end{array}\right].\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}x+\frac{1}{3}y &=11 \\ y &=30,\end{aligned}\right.
$$

and we can apply back substitution. The final equation $y=30$ tells us the value of $y.$ Substituting this value into the first equation, we get

$$
x+\frac{1}{3}(30)=11\,⇒\,x=11-10=1.
$$

Therefore, the solution is $x=1$ and $y=30.$

Offsets h=2, k=-1

Consider the system of linear equations

$$
\left\{\begin{aligned}x+\frac{1}{3}y &=\frac{38}{3} \\ 3x+\frac{1}{5}y &=\frac{74}{5}.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then solve the linear system.

- $M∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & \frac{38}{3} \\ 0 & 1 & -4\end{array}\right],$
$\,x=14$ and $y=-4$
- $M∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & \frac{38}{3} \\ 0 & 1 & 5\end{array}\right],$
$\,x=11$ and $y=5$
- $M∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & \frac{38}{3} \\ 0 & 1 & 2\end{array}\right],$
$\,x=12$ and $y=2$
- $M∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & \frac{38}{3} \\ 0 & 1 & 29\end{array}\right],$
$\,x=3$ and $y=29$
- $M∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & \frac{38}{3} \\ 0 & 1 & -1\end{array}\right],$
$\,x=13$ and $y=-1$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}1 & \frac{1}{3} & \frac{38}{3} \\ 3 & \frac{1}{5} & \frac{74}{5}\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & \frac{38}{3} \\ 3 & \frac{1}{5} & \frac{74}{5}\end{array}\right] & {R}_{2} & :={R}_{2}-3{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & \frac{38}{3} \\ 0 & -\frac{4}{5} & -\frac{116}{5}\end{array}\right] & {R}_{2} & :=-\frac{5}{4}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{1}{3} & \frac{38}{3} \\ 0 & 1 & 29\end{array}\right].\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}x+\frac{1}{3}y &=\frac{38}{3} \\ y &=29,\end{aligned}\right.
$$

and we can apply back substitution. The final equation $y=29$ tells us the value of $y.$ Substituting this value into the first equation, we get

$$
x+\frac{1}{3}(29)=\frac{38}{3}\,⇒\,x=\frac{38}{3}-\frac{29}{3}=3.
$$

Therefore, the solution is $x=3$ and $y=29.$

## q-73555 (easy)

Source

Consider the system of linear equations

$$
\left\{\begin{aligned}4x+12y &=-4 \\ 5x+11y &=3.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & 3 & -1 \\ 0 & 1 & -2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 3 & -1 \\ 0 & 1 & 1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 3 & -1 \\ 0 & 1 & 2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 3 & -1 \\ 0 & 1 & -1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 3 & -1 \\ 0 & 1 & -4\end{array}\right]$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}4 & 12 & -4 \\ 5 & 11 & 3\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}4 & 12 & -4 \\ 5 & 11 & 3\end{array}\right] & {R}_{1} & :=\frac{1}{4}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 3 & -1 \\ 5 & 11 & 3\end{array}\right] & {R}_{2} & :={R}_{2}-5{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 3 & -1 \\ 0 & -4 & 8\end{array}\right] & {R}_{2} & :=-\frac{1}{4}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & 3 & -1 \\ 0 & 1 & -2\end{array}\right].\end{aligned}
$$

Offsets h=2, k=-1

Consider the system of linear equations

$$
\left\{\begin{aligned}4x+12y &=-8 \\ 5x+11y &=2.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & 3 & -2 \\ 0 & 1 & -3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 3 & -2 \\ 0 & 1 & 0\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 3 & -2 \\ 0 & 1 & 1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 3 & -2 \\ 0 & 1 & -2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 3 & -2 \\ 0 & 1 & -5\end{array}\right]$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}4 & 12 & -8 \\ 5 & 11 & 2\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}4 & 12 & -8 \\ 5 & 11 & 2\end{array}\right] & {R}_{1} & :=\frac{1}{4}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 3 & -2 \\ 5 & 11 & 2\end{array}\right] & {R}_{2} & :={R}_{2}-5{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & 3 & -2 \\ 0 & -4 & 12\end{array}\right] & {R}_{2} & :=-\frac{1}{4}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & 3 & -2 \\ 0 & 1 & -3\end{array}\right].\end{aligned}
$$

## q-130912 (moderate)

Source

Consider the system of linear equations

$$
\left\{\begin{aligned}3x+5y &=-6 \\ -6x-6y &=10.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & \frac{5}{3} & 2 \\ 0 & 1 & \frac{1}{2}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 5 & -2 \\ 0 & 1 & -1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{5}{3} & -1 \\ 0 & 1 & \frac{1}{2}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{5}{3} & -2 \\ 0 & 1 & -\frac{1}{2}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 3 & -2 \\ 0 & 1 & -2\end{array}\right]$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}3 & 5 & -6 \\ -6 & -6 & 10\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}3 & 5 & -6 \\ -6 & -6 & 10\end{array}\right] & {R}_{1} & :=\frac{1}{3}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{5}{3} & -2 \\ -6 & -6 & 10\end{array}\right] & {R}_{2} & :={R}_{2}+6{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{5}{3} & -2 \\ 0 & 4 & -2\end{array}\right] & {R}_{2} & :=\frac{1}{4}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{5}{3} & -2 \\ 0 & 1 & -\frac{1}{2}\end{array}\right].\end{aligned}
$$

Offsets h=2, k=-1

Consider the system of linear equations

$$
\left\{\begin{aligned}3x+5y &=-5 \\ -6x-6y &=4.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & \frac{5}{3} & \frac{7}{3} \\ 0 & 1 & -\frac{1}{2}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 5 & -5 \\ 0 & 1 & -2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{5}{3} & -\frac{2}{3} \\ 0 & 1 & -\frac{1}{2}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & \frac{5}{3} & -\frac{5}{3} \\ 0 & 1 & -\frac{3}{2}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & 3 & -3 \\ 0 & 1 & -3\end{array}\right]$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}3 & 5 & -5 \\ -6 & -6 & 4\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}3 & 5 & -5 \\ -6 & -6 & 4\end{array}\right] & {R}_{1} & :=\frac{1}{3}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{5}{3} & -\frac{5}{3} \\ -6 & -6 & 4\end{array}\right] & {R}_{2} & :={R}_{2}+6{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{5}{3} & -\frac{5}{3} \\ 0 & 4 & -6\end{array}\right] & {R}_{2} & :=\frac{1}{4}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & \frac{5}{3} & -\frac{5}{3} \\ 0 & 1 & -\frac{3}{2}\end{array}\right].\end{aligned}
$$

## q-73538 (moderate)

Source

Consider the system of linear equations

$$
\left\{\begin{aligned}3x-2y &=4 \\ 2x-y &=2.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & \frac{4}{3} \\ 0 & 1 & -2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & \frac{4}{3} \\ 0 & 1 & -\frac{3}{2}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & \frac{4}{3} \\ 0 & 1 & 2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & \frac{4}{3} \\ 0 & 1 & \frac{3}{2}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & \frac{4}{3} \\ 0 & 1 & -3\end{array}\right]$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}3 & -2 & 4 \\ 2 & -1 & 2\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}3 & -2 & 4 \\ 2 & -1 & 2\end{array}\right] & {R}_{1} & :=\frac{1}{3}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & \frac{4}{3} \\ 2 & -1 & 2\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & \frac{4}{3} \\ 0 & \frac{1}{3} & -\frac{2}{3}\end{array}\right] & {R}_{2} & :=3{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & \frac{4}{3} \\ 0 & 1 & -2\end{array}\right].\end{aligned}
$$

Offsets h=2, k=-1

Consider the system of linear equations

$$
\left\{\begin{aligned}3x-2y &=12 \\ 2x-y &=7.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & 4 \\ 0 & 1 & -3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & 4 \\ 0 & 1 & -\frac{5}{2}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & 4 \\ 0 & 1 & 1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & 4 \\ 0 & 1 & \frac{1}{2}\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & 4 \\ 0 & 1 & -4\end{array}\right]$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}3 & -2 & 12 \\ 2 & -1 & 7\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}3 & -2 & 12 \\ 2 & -1 & 7\end{array}\right] & {R}_{1} & :=\frac{1}{3}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & 4 \\ 2 & -1 & 7\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & 4 \\ 0 & \frac{1}{3} & -1\end{array}\right] & {R}_{2} & :=3{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -\frac{2}{3} & 4 \\ 0 & 1 & -3\end{array}\right].\end{aligned}
$$

## q-73544 (easy)

Source

Consider the system of linear equations

$$
\left\{\begin{aligned}2x-4y &=6 \\ 4x-7y &=10.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then solve the linear system.

- $M∼\left[\begin{array}{cc|c}1 & -2 & 3 \\ 0 & 1 & -1\end{array}\right],$
$\,x=1$ and $y=-1$
- $M∼\left[\begin{array}{cc|c}1 & -2 & 3 \\ 0 & 1 & -2\end{array}\right],$
$\,x=-1$ and $y=-2$
- $M∼\left[\begin{array}{cc|c}1 & -2 & 3 \\ 0 & 1 & -4\end{array}\right],$
$\,x=-5$ and $y=-4$
- $M∼\left[\begin{array}{cc|c}1 & -2 & 3 \\ 0 & 1 & 2\end{array}\right],$
$\,x=7$ and $y=2$
- $M∼\left[\begin{array}{cc|c}1 & -2 & 3 \\ 0 & 1 & 4\end{array}\right],$
$\,x=11$ and $y=4$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}2 & -4 & 6 \\ 4 & -7 & 10\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}2 & -4 & 6 \\ 4 & -7 & 10\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & 3 \\ 4 & -7 & 10\end{array}\right] & {R}_{2} & :={R}_{2}-4{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & 3 \\ 0 & 1 & -2\end{array}\right].\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}x-2y &=3 \\ y &=-2,\end{aligned}\right.
$$

and we can apply back substitution. The final equation $y=-2$ tells us the value of $y.$ Substituting this value into the first equation, we get

$$
x-2(-2)=3\,⇒\,x=-1.
$$

Thus, the solution is $x=-1$ and $y=-2.$

Offsets h=2, k=-1

Consider the system of linear equations

$$
\left\{\begin{aligned}2x-4y &=14 \\ 4x-7y &=25.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form, and then solve the linear system.

- $M∼\left[\begin{array}{cc|c}1 & -2 & 7 \\ 0 & 1 & -2\end{array}\right],$
$\,x=3$ and $y=-2$
- $M∼\left[\begin{array}{cc|c}1 & -2 & 7 \\ 0 & 1 & -3\end{array}\right],$
$\,x=1$ and $y=-3$
- $M∼\left[\begin{array}{cc|c}1 & -2 & 7 \\ 0 & 1 & -5\end{array}\right],$
$\,x=-3$ and $y=-5$
- $M∼\left[\begin{array}{cc|c}1 & -2 & 7 \\ 0 & 1 & 1\end{array}\right],$
$\,x=9$ and $y=1$
- $M∼\left[\begin{array}{cc|c}1 & -2 & 7 \\ 0 & 1 & 3\end{array}\right],$
$\,x=13$ and $y=3$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}2 & -4 & 14 \\ 4 & -7 & 25\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}2 & -4 & 14 \\ 4 & -7 & 25\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & 7 \\ 4 & -7 & 25\end{array}\right] & {R}_{2} & :={R}_{2}-4{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -2 & 7 \\ 0 & 1 & -3\end{array}\right].\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}x-2y &=7 \\ y &=-3,\end{aligned}\right.
$$

and we can apply back substitution. The final equation $y=-3$ tells us the value of $y.$ Substituting this value into the first equation, we get

$$
x-2(-3)=7\,⇒\,x=1.
$$

Thus, the solution is $x=1$ and $y=-3.$

## q-73551 (easy)

Source

Consider the system of linear equations

$$
\left\{\begin{aligned}5x-15y &=10 \\ 2x-4y &=4.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & 3 & 2 \\ 0 & 1 & 4\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -3 & 2 \\ 0 & 1 & 0\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -3 & 2 \\ 0 & 1 & 4\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -3 & 2 \\ 0 & 1 & -1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -3 & -2 \\ 0 & 1 & 1\end{array}\right]$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}5 & -15 & 10 \\ 2 & -4 & 4\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}5 & -15 & 10 \\ 2 & -4 & 4\end{array}\right] & {R}_{1} & :=\frac{1}{5}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & 2 \\ 2 & -4 & 4\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & 2 \\ 0 & 2 & 0\end{array}\right] & {R}_{2} & :=\frac{1}{2}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & 2 \\ 0 & 1 & 0\end{array}\right].\end{aligned}
$$

Offsets h=2, k=-1

Consider the system of linear equations

$$
\left\{\begin{aligned}5x-15y &=35 \\ 2x-4y &=12.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & 3 & 1 \\ 0 & 1 & 3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -3 & 7 \\ 0 & 1 & -1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -3 & 7 \\ 0 & 1 & 3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -3 & 7 \\ 0 & 1 & -2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -3 & 3 \\ 0 & 1 & 0\end{array}\right]$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}5 & -15 & 35 \\ 2 & -4 & 12\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}5 & -15 & 35 \\ 2 & -4 & 12\end{array}\right] & {R}_{1} & :=\frac{1}{5}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & 7 \\ 2 & -4 & 12\end{array}\right] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & 7 \\ 0 & 2 & -2\end{array}\right] & {R}_{2} & :=\frac{1}{2}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -3 & 7 \\ 0 & 1 & -1\end{array}\right].\end{aligned}
$$

## q-73554 (easy)

Source

Consider the system of linear equations

$$
\left\{\begin{aligned}2x-8y &=10 \\ 3x-7y &=5.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & -4 & 5 \\ 0 & 1 & 4\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -4 & 5 \\ 0 & 1 & -2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -4 & 5 \\ 0 & 1 & 2\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -4 & 5 \\ 0 & 1 & -4\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -4 & 5 \\ 0 & 1 & 1\end{array}\right]$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}2 & -8 & 10 \\ 3 & -7 & 5\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}2 & -8 & 10 \\ 3 & -7 & 5\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -4 & 5 \\ 3 & -7 & 5\end{array}\right] & {R}_{2} & :={R}_{2}-3{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -4 & 5 \\ 0 & 5 & -10\end{array}\right] & {R}_{2} & :=\frac{1}{5}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -4 & 5 \\ 0 & 1 & -2\end{array}\right].\end{aligned}
$$

Offsets h=2, k=-1

Consider the system of linear equations

$$
\left\{\begin{aligned}2x-8y &=22 \\ 3x-7y &=18.\end{aligned}\right.
$$

Use the standard method of Gaussian elimination to reduce the augmented matrix $M$ of the system to row echelon form.

- $M∼\left[\begin{array}{cc|c}1 & -4 & 11 \\ 0 & 1 & 3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -4 & 11 \\ 0 & 1 & -3\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -4 & 11 \\ 0 & 1 & 1\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -4 & 11 \\ 0 & 1 & -5\end{array}\right]$
- $M∼\left[\begin{array}{cc|c}1 & -4 & 11 \\ 0 & 1 & 0\end{array}\right]$

The augmented matrix for this system is

$$
M=\left[\begin{array}{cc|c}2 & -8 & 22 \\ 3 & -7 & 18\end{array}\right].
$$

Reducing $M$ to row echelon form, we have

$$
\begin{aligned}M & ∼\left[\begin{array}{cc|c}2 & -8 & 22 \\ 3 & -7 & 18\end{array}\right] & {R}_{1} & :=\frac{1}{2}{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -4 & 11 \\ 3 & -7 & 18\end{array}\right] & {R}_{2} & :={R}_{2}-3{R}_{1} \\  & ∼\left[\begin{array}{cc|c}1 & -4 & 11 \\ 0 & 5 & -15\end{array}\right] & {R}_{2} & :=\frac{1}{5}{R}_{2} \\  & ∼\left[\begin{array}{cc|c}1 & -4 & 11 \\ 0 & 1 & -3\end{array}\right].\end{aligned}
$$
