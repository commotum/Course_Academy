## q-105168

### Source

Consider the vectors

$$
{a}_{1}=\begin{bmatrix}1 \\ 3 \\ -2\end{bmatrix},\,{a}_{2}=\begin{bmatrix}-3 \\ -8 \\ 6\end{bmatrix},\,{a}_{3}=\begin{bmatrix}2 \\ 5 \\ -3\end{bmatrix},\,b=\begin{bmatrix}2 \\ 1 \\ 2\end{bmatrix}.
$$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b,$ then what is ${x}_{1}+{x}_{2}+{x}_{3}?$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b$, then we have  

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ 3 \\ -2\end{bmatrix}+{x}_{2}\begin{bmatrix}-3 \\ -8 \\ 6\end{bmatrix}+{x}_{3}\begin{bmatrix}2 \\ 5 \\ -3\end{bmatrix} & =\begin{bmatrix}2 \\ 1 \\ 2\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ 3{x}_{1} \\ -2{x}_{1}\end{bmatrix}+\begin{bmatrix}-3{x}_{2} \\ -8{x}_{2} \\ 6{x}_{2}\end{bmatrix}+\begin{bmatrix}2{x}_{3} \\ 5{x}_{3} \\ -3{x}_{3}\end{bmatrix} & =\begin{bmatrix}2 \\ 1 \\ 2\end{bmatrix} \\ \begin{bmatrix}{x}_{1}-3{x}_{2}+2{x}_{3} \\ 3{x}_{1}-8{x}_{2}+5{x}_{3} \\ -2{x}_{1}+6{x}_{2}-3{x}_{3}\end{bmatrix} & =\begin{bmatrix}2 \\ 1 \\ 2\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}-3{x}_{2}+2{x}_{3} &=2 \\ 3{x}_{1}-8{x}_{2}+5{x}_{3} &=1 \\ -2{x}_{1}+6{x}_{2}-3{x}_{3} &=2\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\begin{bmatrix}1 & -3 & 2 & 2 \\ 3 & -8 & 5 & 1 \\ -2 & 6 & -3 & 2\end{bmatrix}
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\begin{bmatrix}1 & -3 & 2 & 2 \\ 3 & -8 & 5 & 1 \\ -2 & 6 & -3 & 2\end{bmatrix} & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 2 & 2 \\ 0 & 1 & -1 & -5 \\ -2 & 6 & -3 & 2\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & -3 & 2 & 2 \\ 0 & 1 & -1 & -5 \\ 0 & 0 & 1 & 6\end{bmatrix}.\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}-3{x}_{2}+2{x}_{3} &=2 \\ {x}_{2}-{x}_{3} &=-5 \\ {x}_{3} &=6.\end{aligned}\right.
$$

From the third equation, we get ${x}_{3}=6.$ Substituting ${x}_{3}=6$ into the second equation, we obtain

$$
{x}_{2}-6=-5\,⟹\,{x}_{2}=1.
$$

Now, substituting ${x}_{2}=1$ and ${x}_{3}=6$ into the first equation, we obtain

$$
{x}_{1}-3(1)+2(6)=2\,⟹\,{x}_{1}=-7.
$$

So, the solution of the system is ${x}_{1}=-7$, ${x}_{2}=1$, and ${x}_{3}=6,$ which means 

$$
-7{a}_{1}+{a}_{2}+6{a}_{3}=b.
$$

Consequently, 

$$
{x}_{1}+{x}_{2}+{x}_{3}=-7+1+6=0.
$$

### Replay

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 3 \\ -2\end{bmatrix},\quad a_2=\begin{bmatrix}-3 \\ -8 \\ 6\end{bmatrix},\quad a_3=\begin{bmatrix}2 \\ 5 \\ -3\end{bmatrix},\quad b=\begin{bmatrix}2 \\ 1 \\ 2\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 3 \\ -2\end{bmatrix}+x_2\begin{bmatrix}-3 \\ -8 \\ 6\end{bmatrix}+x_3\begin{bmatrix}2 \\ 5 \\ -3\end{bmatrix}&=\begin{bmatrix}2 \\ 1 \\ 2\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 3 x_{1} \\ - 2 x_{1}\end{bmatrix}+\begin{bmatrix}- 3 x_{2} \\ - 8 x_{2} \\ 6 x_{2}\end{bmatrix}+\begin{bmatrix}2 x_{3} \\ 5 x_{3} \\ - 3 x_{3}\end{bmatrix}&=\begin{bmatrix}2 \\ 1 \\ 2\end{bmatrix} \\ \begin{bmatrix}x_{1} - 3 x_{2} + 2 x_{3} \\ 3 x_{1} - 8 x_{2} + 5 x_{3} \\ - 2 x_{1} + 6 x_{2} - 3 x_{3}\end{bmatrix}&=\begin{bmatrix}2 \\ 1 \\ 2\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} - 3 x_{2} + 2 x_{3} &=2 \\ 3 x_{1} - 8 x_{2} + 5 x_{3} &=1 \\ - 2 x_{1} + 6 x_{2} - 3 x_{3} &=2\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & -3 & 2 & 2 \\ 3 & -8 & 5 & 1 \\ -2 & 6 & -3 & 2\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & -3 & 2 & 2 \\ 3 & -8 & 5 & 1 \\ -2 & 6 & -3 & 2\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & -3 & 2 & 2 \\ 0 & 1 & -1 & -5 \\ -2 & 6 & -3 & 2\end{array}\right] && R_{2}:=R_{2}+(-3)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & -3 & 2 & 2 \\ 0 & 1 & -1 & -5 \\ 0 & 0 & 1 & 6\end{array}\right] && R_{3}:=R_{3}+(2)R_{1}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} - 3 x_{2} + 2 x_{3} &=2 \\ x_{2} - x_{3} &=-5 \\ x_{3} &=6\end{aligned}\right.
$$

From the third equation, we get $x_3=6.$ Substituting this value into the second equation, we get

$$
1x_2+(-1)(6)=-5\quad\Rightarrow\quad x_2=1
$$

Finally, substituting these values into the first equation, we obtain

$$
x_1+(-3)(1)+(2)(6)=2\quad\Rightarrow\quad x_1=-7
$$

So, the solution of the system is $x_1=-7$, $x_2=1$, $x_3=6$, which means

$$
-7a_1+(1)a_2+(6)a_3=b.
$$

Consequently,

$$
x_{1} + x_{2} + x_{3}=(-7)+(1)+(6)=0.
$$



### Changed RHS

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 3 \\ -2\end{bmatrix},\quad a_2=\begin{bmatrix}-3 \\ -8 \\ 6\end{bmatrix},\quad a_3=\begin{bmatrix}2 \\ 5 \\ -3\end{bmatrix},\quad b=\begin{bmatrix}42 \\ 112 \\ -77\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 3 \\ -2\end{bmatrix}+x_2\begin{bmatrix}-3 \\ -8 \\ 6\end{bmatrix}+x_3\begin{bmatrix}2 \\ 5 \\ -3\end{bmatrix}&=\begin{bmatrix}42 \\ 112 \\ -77\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 3 x_{1} \\ - 2 x_{1}\end{bmatrix}+\begin{bmatrix}- 3 x_{2} \\ - 8 x_{2} \\ 6 x_{2}\end{bmatrix}+\begin{bmatrix}2 x_{3} \\ 5 x_{3} \\ - 3 x_{3}\end{bmatrix}&=\begin{bmatrix}42 \\ 112 \\ -77\end{bmatrix} \\ \begin{bmatrix}x_{1} - 3 x_{2} + 2 x_{3} \\ 3 x_{1} - 8 x_{2} + 5 x_{3} \\ - 2 x_{1} + 6 x_{2} - 3 x_{3}\end{bmatrix}&=\begin{bmatrix}42 \\ 112 \\ -77\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} - 3 x_{2} + 2 x_{3} &=42 \\ 3 x_{1} - 8 x_{2} + 5 x_{3} &=112 \\ - 2 x_{1} + 6 x_{2} - 3 x_{3} &=-77\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & -3 & 2 & 42 \\ 3 & -8 & 5 & 112 \\ -2 & 6 & -3 & -77\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & -3 & 2 & 42 \\ 3 & -8 & 5 & 112 \\ -2 & 6 & -3 & -77\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & -3 & 2 & 42 \\ 0 & 1 & -1 & -14 \\ -2 & 6 & -3 & -77\end{array}\right] && R_{2}:=R_{2}+(-3)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & -3 & 2 & 42 \\ 0 & 1 & -1 & -14 \\ 0 & 0 & 1 & 7\end{array}\right] && R_{3}:=R_{3}+(2)R_{1}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} - 3 x_{2} + 2 x_{3} &=42 \\ x_{2} - x_{3} &=-14 \\ x_{3} &=7\end{aligned}\right.
$$

From the third equation, we get $x_3=7.$ Substituting this value into the second equation, we get

$$
1x_2+(-1)(7)=-14\quad\Rightarrow\quad x_2=-7
$$

Finally, substituting these values into the first equation, we obtain

$$
x_1+(-3)(-7)+(2)(7)=42\quad\Rightarrow\quad x_1=7
$$

So, the solution of the system is $x_1=7$, $x_2=-7$, $x_3=7$, which means

$$
7a_1+(-7)a_2+(7)a_3=b.
$$

Consequently,

$$
x_{1} + x_{2} + x_{3}=(7)+(-7)+(7)=7.
$$



## q-105169

### Source

Consider the vectors

$$
{a}_{1}=\begin{bmatrix}1 \\ 5 \\ -2\end{bmatrix},\,{a}_{2}=\begin{bmatrix}1 \\ 6 \\ -2\end{bmatrix},\,{a}_{3}=\begin{bmatrix}-1 \\ -8 \\ 2\end{bmatrix},\,b=\begin{bmatrix}2 \\ -3 \\ 4\end{bmatrix}.
$$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b,$ then what is ${x}_{1}+{x}_{2}+{x}_{3}?$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b$, then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ 5 \\ -2\end{bmatrix}+{x}_{2}\begin{bmatrix}1 \\ 6 \\ -2\end{bmatrix}+{x}_{3}\begin{bmatrix}-1 \\ -8 \\ 2\end{bmatrix} & =\begin{bmatrix}2 \\ -3 \\ 4\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ 5{x}_{1} \\ -2{x}_{1}\end{bmatrix}+\begin{bmatrix}{x}_{2} \\ 6{x}_{2} \\ -2{x}_{2}\end{bmatrix}+\begin{bmatrix}-{x}_{3} \\ -8{x}_{3} \\ 2{x}_{3}\end{bmatrix} & =\begin{bmatrix}2 \\ -3 \\ 4\end{bmatrix} \\ \begin{bmatrix}{x}_{1}+{x}_{2}-{x}_{3} \\ 5{x}_{1}+6{x}_{2}-8{x}_{3} \\ -2{x}_{1}-2{x}_{2}+2{x}_{3}\end{bmatrix} & =\begin{bmatrix}2 \\ -3 \\ 4\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}+{x}_{2}-{x}_{3} &=2 \\ 5{x}_{1}+6{x}_{2}-8{x}_{3} &=-3 \\ -2{x}_{1}-2{x}_{2}+2{x}_{3} &=4\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\begin{bmatrix}1 & 1 & -1 & 2 \\ 5 & 6 & -8 & -3 \\ -2 & -2 & 2 & 4\end{bmatrix}.
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\begin{bmatrix}1 & 1 & -1 & 2 \\ 5 & 6 & -8 & -3 \\ -2 & -2 & 2 & 4\end{bmatrix} & {R}_{2} & :={R}_{2}+(-5){R}_{1} \\  & ∼\begin{bmatrix}1 & 1 & -1 & 2 \\ 0 & 1 & -3 & -13 \\ -2 & -2 & 2 & 4\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{1} \\  & ∼\begin{bmatrix}1 & 1 & -1 & 2 \\ 0 & 1 & -3 & -13 \\ 0 & 0 & 0 & 8\end{bmatrix}.\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}+{x}_{2}-{x}_{3} &=2 \\ {x}_{2}-3{x}_{3} &=-13 \\ 0 &=8.\end{aligned}\right.
$$

However, the final equation $0=8$  gives a false statement. So the system has no solution.

### Replay

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 5 \\ -2\end{bmatrix},\quad a_2=\begin{bmatrix}1 \\ 6 \\ -2\end{bmatrix},\quad a_3=\begin{bmatrix}-1 \\ -8 \\ 2\end{bmatrix},\quad b=\begin{bmatrix}2 \\ -3 \\ 4\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 5 \\ -2\end{bmatrix}+x_2\begin{bmatrix}1 \\ 6 \\ -2\end{bmatrix}+x_3\begin{bmatrix}-1 \\ -8 \\ 2\end{bmatrix}&=\begin{bmatrix}2 \\ -3 \\ 4\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 5 x_{1} \\ - 2 x_{1}\end{bmatrix}+\begin{bmatrix}x_{2} \\ 6 x_{2} \\ - 2 x_{2}\end{bmatrix}+\begin{bmatrix}- x_{3} \\ - 8 x_{3} \\ 2 x_{3}\end{bmatrix}&=\begin{bmatrix}2 \\ -3 \\ 4\end{bmatrix} \\ \begin{bmatrix}x_{1} + x_{2} - x_{3} \\ 5 x_{1} + 6 x_{2} - 8 x_{3} \\ - 2 x_{1} - 2 x_{2} + 2 x_{3}\end{bmatrix}&=\begin{bmatrix}2 \\ -3 \\ 4\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + x_{2} - x_{3} &=2 \\ 5 x_{1} + 6 x_{2} - 8 x_{3} &=-3 \\ - 2 x_{1} - 2 x_{2} + 2 x_{3} &=4\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 1 & -1 & 2 \\ 5 & 6 & -8 & -3 \\ -2 & -2 & 2 & 4\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 1 & -1 & 2 \\ 5 & 6 & -8 & -3 \\ -2 & -2 & 2 & 4\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & -1 & 2 \\ 0 & 1 & -3 & -13 \\ -2 & -2 & 2 & 4\end{array}\right] && R_{2}:=R_{2}+(-5)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & -1 & 2 \\ 0 & 1 & -3 & -13 \\ 0 & 0 & 0 & 8\end{array}\right] && R_{3}:=R_{3}+(2)R_{1}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + x_{2} - x_{3} &=2 \\ x_{2} - 3 x_{3} &=-13 \\ 0 &=8\end{aligned}\right.
$$

However, the final equation $0=8$ gives a false statement. So the system has no solution.

### Changed RHS

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 5 \\ -2\end{bmatrix},\quad a_2=\begin{bmatrix}1 \\ 6 \\ -2\end{bmatrix},\quad a_3=\begin{bmatrix}-1 \\ -8 \\ 2\end{bmatrix},\quad b=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 5 \\ -2\end{bmatrix}+x_2\begin{bmatrix}1 \\ 6 \\ -2\end{bmatrix}+x_3\begin{bmatrix}-1 \\ -8 \\ 2\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 5 x_{1} \\ - 2 x_{1}\end{bmatrix}+\begin{bmatrix}x_{2} \\ 6 x_{2} \\ - 2 x_{2}\end{bmatrix}+\begin{bmatrix}- x_{3} \\ - 8 x_{3} \\ 2 x_{3}\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix} \\ \begin{bmatrix}x_{1} + x_{2} - x_{3} \\ 5 x_{1} + 6 x_{2} - 8 x_{3} \\ - 2 x_{1} - 2 x_{2} + 2 x_{3}\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + x_{2} - x_{3} &=0 \\ 5 x_{1} + 6 x_{2} - 8 x_{3} &=-7 \\ - 2 x_{1} - 2 x_{2} + 2 x_{3} &=-9\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 1 & -1 & 0 \\ 5 & 6 & -8 & -7 \\ -2 & -2 & 2 & -9\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 1 & -1 & 0 \\ 5 & 6 & -8 & -7 \\ -2 & -2 & 2 & -9\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & -1 & 0 \\ 0 & 1 & -3 & -7 \\ -2 & -2 & 2 & -9\end{array}\right] && R_{2}:=R_{2}+(-5)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & -1 & 0 \\ 0 & 1 & -3 & -7 \\ 0 & 0 & 0 & -9\end{array}\right] && R_{3}:=R_{3}+(2)R_{1}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + x_{2} - x_{3} &=0 \\ x_{2} - 3 x_{3} &=-7 \\ 0 &=-9\end{aligned}\right.
$$

However, the final equation $0=-9$ gives a false statement. So the system has no solution.

## q-105170

### Source

Consider the vectors

$$
{a}_{1}=\begin{bmatrix}1 \\ -1 \\ 2\end{bmatrix},\,{a}_{2}=\begin{bmatrix}4 \\ -3 \\ 8\end{bmatrix},\,{a}_{3}=\begin{bmatrix}7 \\ -7 \\ 14\end{bmatrix},\,b=\begin{bmatrix}5 \\ -3 \\ 7\end{bmatrix}.
$$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b,$ then what is ${x}_{1}+{x}_{2}+{x}_{3}?$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b$, then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ -1 \\ 2\end{bmatrix}+{x}_{2}\begin{bmatrix}4 \\ -3 \\ 8\end{bmatrix}+{x}_{3}\begin{bmatrix}7 \\ -7 \\ 14\end{bmatrix} & =\begin{bmatrix}5 \\ -3 \\ 7\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ -{x}_{1} \\ 2{x}_{1}\end{bmatrix}+\begin{bmatrix}4{x}_{2} \\ -3{x}_{2} \\ 8{x}_{2}\end{bmatrix}+\begin{bmatrix}7{x}_{3} \\ -7{x}_{3} \\ 14{x}_{3}\end{bmatrix} & =\begin{bmatrix}5 \\ -3 \\ 7\end{bmatrix} \\ \begin{bmatrix}{x}_{1}+4{x}_{2}+7{x}_{3} \\ -{x}_{1}-3{x}_{2}-7{x}_{3} \\ 2{x}_{1}+8{x}_{2}+14{x}_{3}\end{bmatrix} & =\begin{bmatrix}5 \\ -3 \\ 7\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}+4{x}_{2}+7{x}_{3} &=5 \\ -{x}_{1}-3{x}_{2}-7{x}_{3} &=-3 \\ 2{x}_{1}+8{x}_{2}+14{x}_{3} &=7\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\begin{bmatrix}1 & 4 & 7 & 5 \\ -1 & -3 & -7 & -3 \\ 2 & 8 & 14 & 7\end{bmatrix}.
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\begin{bmatrix}1 & 4 & 7 & 5 \\ -1 & -3 & -7 & -3 \\ 2 & 8 & 14 & 7\end{bmatrix} & {R}_{2} & :={R}_{2}+{R}_{1} \\  & ∼\begin{bmatrix}1 & 4 & 7 & 5 \\ 0 & 1 & 0 & 2 \\ 2 & 8 & 14 & 7\end{bmatrix} & {R}_{3} & :={R}_{3}+(-2){R}_{1} \\  & ∼\begin{bmatrix}1 & 4 & 7 & 5 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 0 & -3\end{bmatrix}.\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}+4{x}_{2}+7{x}_{3} &=5 \\ {x}_{2} &=2 \\ 0 &=-3.\end{aligned}\right.
$$

However, the final equation $0=-3$  gives a false statement. So the system has no solution.

### Replay

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ -1 \\ 2\end{bmatrix},\quad a_2=\begin{bmatrix}4 \\ -3 \\ 8\end{bmatrix},\quad a_3=\begin{bmatrix}7 \\ -7 \\ 14\end{bmatrix},\quad b=\begin{bmatrix}5 \\ -3 \\ 7\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ -1 \\ 2\end{bmatrix}+x_2\begin{bmatrix}4 \\ -3 \\ 8\end{bmatrix}+x_3\begin{bmatrix}7 \\ -7 \\ 14\end{bmatrix}&=\begin{bmatrix}5 \\ -3 \\ 7\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ - x_{1} \\ 2 x_{1}\end{bmatrix}+\begin{bmatrix}4 x_{2} \\ - 3 x_{2} \\ 8 x_{2}\end{bmatrix}+\begin{bmatrix}7 x_{3} \\ - 7 x_{3} \\ 14 x_{3}\end{bmatrix}&=\begin{bmatrix}5 \\ -3 \\ 7\end{bmatrix} \\ \begin{bmatrix}x_{1} + 4 x_{2} + 7 x_{3} \\ - x_{1} - 3 x_{2} - 7 x_{3} \\ 2 x_{1} + 8 x_{2} + 14 x_{3}\end{bmatrix}&=\begin{bmatrix}5 \\ -3 \\ 7\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + 4 x_{2} + 7 x_{3} &=5 \\ - x_{1} - 3 x_{2} - 7 x_{3} &=-3 \\ 2 x_{1} + 8 x_{2} + 14 x_{3} &=7\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 4 & 7 & 5 \\ -1 & -3 & -7 & -3 \\ 2 & 8 & 14 & 7\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 4 & 7 & 5 \\ -1 & -3 & -7 & -3 \\ 2 & 8 & 14 & 7\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 4 & 7 & 5 \\ 0 & 1 & 0 & 2 \\ 2 & 8 & 14 & 7\end{array}\right] && R_{2}:=R_{2}+(1)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 4 & 7 & 5 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & 0 & -3\end{array}\right] && R_{3}:=R_{3}+(-2)R_{1}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + 4 x_{2} + 7 x_{3} &=5 \\ x_{2} &=2 \\ 0 &=-3\end{aligned}\right.
$$

However, the final equation $0=-3$ gives a false statement. So the system has no solution.

### Changed RHS

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ -1 \\ 2\end{bmatrix},\quad a_2=\begin{bmatrix}4 \\ -3 \\ 8\end{bmatrix},\quad a_3=\begin{bmatrix}7 \\ -7 \\ 14\end{bmatrix},\quad b=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ -1 \\ 2\end{bmatrix}+x_2\begin{bmatrix}4 \\ -3 \\ 8\end{bmatrix}+x_3\begin{bmatrix}7 \\ -7 \\ 14\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ - x_{1} \\ 2 x_{1}\end{bmatrix}+\begin{bmatrix}4 x_{2} \\ - 3 x_{2} \\ 8 x_{2}\end{bmatrix}+\begin{bmatrix}7 x_{3} \\ - 7 x_{3} \\ 14 x_{3}\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix} \\ \begin{bmatrix}x_{1} + 4 x_{2} + 7 x_{3} \\ - x_{1} - 3 x_{2} - 7 x_{3} \\ 2 x_{1} + 8 x_{2} + 14 x_{3}\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + 4 x_{2} + 7 x_{3} &=0 \\ - x_{1} - 3 x_{2} - 7 x_{3} &=-7 \\ 2 x_{1} + 8 x_{2} + 14 x_{3} &=-9\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 4 & 7 & 0 \\ -1 & -3 & -7 & -7 \\ 2 & 8 & 14 & -9\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 4 & 7 & 0 \\ -1 & -3 & -7 & -7 \\ 2 & 8 & 14 & -9\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 4 & 7 & 0 \\ 0 & 1 & 0 & -7 \\ 2 & 8 & 14 & -9\end{array}\right] && R_{2}:=R_{2}+(1)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 4 & 7 & 0 \\ 0 & 1 & 0 & -7 \\ 0 & 0 & 0 & -9\end{array}\right] && R_{3}:=R_{3}+(-2)R_{1}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + 4 x_{2} + 7 x_{3} &=0 \\ x_{2} &=-7 \\ 0 &=-9\end{aligned}\right.
$$

However, the final equation $0=-9$ gives a false statement. So the system has no solution.

## q-105171

### Source

Consider the vectors

$$
{a}_{1}=\begin{bmatrix}1 \\ 2 \\ -1\end{bmatrix},\,{a}_{2}=\begin{bmatrix}-5 \\ -8 \\ 5\end{bmatrix},\,{a}_{3}=\begin{bmatrix}-1 \\ 2 \\ 1\end{bmatrix},\,b=\begin{bmatrix}1 \\ 9 \\ 1\end{bmatrix}.
$$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b,$ then what is ${x}_{1}+{x}_{2}+{x}_{3}?$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b$, then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ 2 \\ -1\end{bmatrix}+{x}_{2}\begin{bmatrix}-5 \\ -8 \\ 5\end{bmatrix}+{x}_{3}\begin{bmatrix}-1 \\ 2 \\ 1\end{bmatrix} & =\begin{bmatrix}1 \\ 9 \\ 1\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ 2{x}_{1} \\ -{x}_{1}\end{bmatrix}+\begin{bmatrix}-5{x}_{2} \\ -8{x}_{2} \\ 5{x}_{2}\end{bmatrix}+\begin{bmatrix}-{x}_{3} \\ 2{x}_{3} \\ {x}_{3}\end{bmatrix} & =\begin{bmatrix}1 \\ 9 \\ 1\end{bmatrix} \\ \begin{bmatrix}{x}_{1}-5{x}_{2}-{x}_{3} \\ 2{x}_{1}-8{x}_{2}+2{x}_{3} \\ -{x}_{1}+5{x}_{2}+{x}_{3}\end{bmatrix} & =\begin{bmatrix}1 \\ 9 \\ 1\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}-5{x}_{2}-{x}_{3} &=1 \\ 2{x}_{1}-8{x}_{2}+2{x}_{3} &=9 \\ -{x}_{1}+5{x}_{2}+{x}_{3} &=1\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\begin{bmatrix}1 & -5 & -1 & 1 \\ 2 & -8 & 2 & 9 \\ -1 & 5 & 1 & 1\end{bmatrix}.
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\begin{bmatrix}1 & -5 & -1 & 1 \\ 2 & -8 & 2 & 9 \\ -1 & 5 & 1 & 1\end{bmatrix} & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼\begin{bmatrix}1 & -5 & -1 & 1 \\ 0 & 2 & 4 & 7 \\ -1 & 5 & 1 & 1\end{bmatrix} & {R}_{3} & :={R}_{3}+{R}_{1} \\  & ∼\begin{bmatrix}1 & -5 & -1 & 1 \\ 0 & 2 & 4 & 7 \\ 0 & 0 & 0 & 2\end{bmatrix}.\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}-5{x}_{2}-{x}_{3} &=1 \\ 2{x}_{2}+4{x}_{3} &=7 \\ 0 &=2.\end{aligned}\right.
$$

However, the final equation $0=2$  gives a false statement. So the system has no solution.

### Replay

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 2 \\ -1\end{bmatrix},\quad a_2=\begin{bmatrix}-5 \\ -8 \\ 5\end{bmatrix},\quad a_3=\begin{bmatrix}-1 \\ 2 \\ 1\end{bmatrix},\quad b=\begin{bmatrix}1 \\ 9 \\ 1\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 2 \\ -1\end{bmatrix}+x_2\begin{bmatrix}-5 \\ -8 \\ 5\end{bmatrix}+x_3\begin{bmatrix}-1 \\ 2 \\ 1\end{bmatrix}&=\begin{bmatrix}1 \\ 9 \\ 1\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 2 x_{1} \\ - x_{1}\end{bmatrix}+\begin{bmatrix}- 5 x_{2} \\ - 8 x_{2} \\ 5 x_{2}\end{bmatrix}+\begin{bmatrix}- x_{3} \\ 2 x_{3} \\ x_{3}\end{bmatrix}&=\begin{bmatrix}1 \\ 9 \\ 1\end{bmatrix} \\ \begin{bmatrix}x_{1} - 5 x_{2} - x_{3} \\ 2 x_{1} - 8 x_{2} + 2 x_{3} \\ - x_{1} + 5 x_{2} + x_{3}\end{bmatrix}&=\begin{bmatrix}1 \\ 9 \\ 1\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} - 5 x_{2} - x_{3} &=1 \\ 2 x_{1} - 8 x_{2} + 2 x_{3} &=9 \\ - x_{1} + 5 x_{2} + x_{3} &=1\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & -5 & -1 & 1 \\ 2 & -8 & 2 & 9 \\ -1 & 5 & 1 & 1\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & -5 & -1 & 1 \\ 2 & -8 & 2 & 9 \\ -1 & 5 & 1 & 1\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & -5 & -1 & 1 \\ 0 & 2 & 4 & 7 \\ -1 & 5 & 1 & 1\end{array}\right] && R_{2}:=R_{2}+(-2)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & -5 & -1 & 1 \\ 0 & 2 & 4 & 7 \\ 0 & 0 & 0 & 2\end{array}\right] && R_{3}:=R_{3}+(1)R_{1}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} - 5 x_{2} - x_{3} &=1 \\ 2 x_{2} + 4 x_{3} &=7 \\ 0 &=2\end{aligned}\right.
$$

However, the final equation $0=2$ gives a false statement. So the system has no solution.

### Changed RHS

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 2 \\ -1\end{bmatrix},\quad a_2=\begin{bmatrix}-5 \\ -8 \\ 5\end{bmatrix},\quad a_3=\begin{bmatrix}-1 \\ 2 \\ 1\end{bmatrix},\quad b=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 2 \\ -1\end{bmatrix}+x_2\begin{bmatrix}-5 \\ -8 \\ 5\end{bmatrix}+x_3\begin{bmatrix}-1 \\ 2 \\ 1\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 2 x_{1} \\ - x_{1}\end{bmatrix}+\begin{bmatrix}- 5 x_{2} \\ - 8 x_{2} \\ 5 x_{2}\end{bmatrix}+\begin{bmatrix}- x_{3} \\ 2 x_{3} \\ x_{3}\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix} \\ \begin{bmatrix}x_{1} - 5 x_{2} - x_{3} \\ 2 x_{1} - 8 x_{2} + 2 x_{3} \\ - x_{1} + 5 x_{2} + x_{3}\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} - 5 x_{2} - x_{3} &=0 \\ 2 x_{1} - 8 x_{2} + 2 x_{3} &=-7 \\ - x_{1} + 5 x_{2} + x_{3} &=-9\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & -5 & -1 & 0 \\ 2 & -8 & 2 & -7 \\ -1 & 5 & 1 & -9\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & -5 & -1 & 0 \\ 2 & -8 & 2 & -7 \\ -1 & 5 & 1 & -9\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & -5 & -1 & 0 \\ 0 & 2 & 4 & -7 \\ -1 & 5 & 1 & -9\end{array}\right] && R_{2}:=R_{2}+(-2)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & -5 & -1 & 0 \\ 0 & 2 & 4 & -7 \\ 0 & 0 & 0 & -9\end{array}\right] && R_{3}:=R_{3}+(1)R_{1}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} - 5 x_{2} - x_{3} &=0 \\ 2 x_{2} + 4 x_{3} &=-7 \\ 0 &=-9\end{aligned}\right.
$$

However, the final equation $0=-9$ gives a false statement. So the system has no solution.

## q-105172

### Source

Consider the vectors

$$
{a}_{1}=\begin{bmatrix}1 \\ -5 \\ -3\end{bmatrix},\,{a}_{2}=\begin{bmatrix}4 \\ -21 \\ -12\end{bmatrix},\,{a}_{3}=\begin{bmatrix}-3 \\ 14 \\ 9\end{bmatrix},\,b=\begin{bmatrix}2 \\ 8 \\ -7\end{bmatrix}.
$$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b,$ then what is ${x}_{1}+{x}_{2}+{x}_{3}?$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b$, then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ -5 \\ -3\end{bmatrix}+{x}_{2}\begin{bmatrix}4 \\ -21 \\ -12\end{bmatrix}+{x}_{3}\begin{bmatrix}-3 \\ 14 \\ 9\end{bmatrix} & =\begin{bmatrix}2 \\ 8 \\ -7\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ -5{x}_{1} \\ -3{x}_{1}\end{bmatrix}+\begin{bmatrix}4{x}_{2} \\ -21{x}_{2} \\ -12{x}_{2}\end{bmatrix}+\begin{bmatrix}-3{x}_{3} \\ 14{x}_{3} \\ 9{x}_{3}\end{bmatrix} & =\begin{bmatrix}2 \\ 8 \\ -7\end{bmatrix} \\ \begin{bmatrix}{x}_{1}+4{x}_{2}-3{x}_{3} \\ -5{x}_{1}-21{x}_{2}+14{x}_{3} \\ -3{x}_{1}-12{x}_{2}+9{x}_{3}\end{bmatrix} & =\begin{bmatrix}2 \\ 8 \\ -7\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}+4{x}_{2}-3{x}_{3} &=2 \\ -5{x}_{1}-21{x}_{2}+14{x}_{3} &=8 \\ -3{x}_{1}-12{x}_{2}+9{x}_{3} &=-7\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\begin{bmatrix}1 & 4 & -3 & 2 \\ -5 & -21 & 14 & 8 \\ -3 & -12 & 9 & -7\end{bmatrix}.
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\begin{bmatrix}1 & 4 & -3 & 2 \\ -5 & -21 & 14 & 8 \\ -3 & -12 & 9 & -7\end{bmatrix} & {R}_{2} & :={R}_{2}+5{R}_{1} \\  & ∼\begin{bmatrix}1 & 4 & -3 & 2 \\ 0 & -1 & -1 & 18 \\ -3 & -12 & 9 & -7\end{bmatrix} & {R}_{3} & :={R}_{3}+3{R}_{1} \\  & ∼\begin{bmatrix}1 & 4 & -3 & 2 \\ 0 & -1 & -1 & 18 \\ 0 & 0 & 0 & -1\end{bmatrix}.\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}+4{x}_{2}-3{x}_{3} &=2 \\ -{x}_{2}-{x}_{3} &=18 \\ 0 &=-1.\end{aligned}\right.
$$

However, the final equation $0=-1$  gives a false statement. So the system has no solution.

### Replay

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ -5 \\ -3\end{bmatrix},\quad a_2=\begin{bmatrix}4 \\ -21 \\ -12\end{bmatrix},\quad a_3=\begin{bmatrix}-3 \\ 14 \\ 9\end{bmatrix},\quad b=\begin{bmatrix}2 \\ 8 \\ -7\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ -5 \\ -3\end{bmatrix}+x_2\begin{bmatrix}4 \\ -21 \\ -12\end{bmatrix}+x_3\begin{bmatrix}-3 \\ 14 \\ 9\end{bmatrix}&=\begin{bmatrix}2 \\ 8 \\ -7\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ - 5 x_{1} \\ - 3 x_{1}\end{bmatrix}+\begin{bmatrix}4 x_{2} \\ - 21 x_{2} \\ - 12 x_{2}\end{bmatrix}+\begin{bmatrix}- 3 x_{3} \\ 14 x_{3} \\ 9 x_{3}\end{bmatrix}&=\begin{bmatrix}2 \\ 8 \\ -7\end{bmatrix} \\ \begin{bmatrix}x_{1} + 4 x_{2} - 3 x_{3} \\ - 5 x_{1} - 21 x_{2} + 14 x_{3} \\ - 3 x_{1} - 12 x_{2} + 9 x_{3}\end{bmatrix}&=\begin{bmatrix}2 \\ 8 \\ -7\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + 4 x_{2} - 3 x_{3} &=2 \\ - 5 x_{1} - 21 x_{2} + 14 x_{3} &=8 \\ - 3 x_{1} - 12 x_{2} + 9 x_{3} &=-7\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 4 & -3 & 2 \\ -5 & -21 & 14 & 8 \\ -3 & -12 & 9 & -7\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 4 & -3 & 2 \\ -5 & -21 & 14 & 8 \\ -3 & -12 & 9 & -7\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 4 & -3 & 2 \\ 0 & -1 & -1 & 18 \\ -3 & -12 & 9 & -7\end{array}\right] && R_{2}:=R_{2}+(5)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 4 & -3 & 2 \\ 0 & -1 & -1 & 18 \\ 0 & 0 & 0 & -1\end{array}\right] && R_{3}:=R_{3}+(3)R_{1}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + 4 x_{2} - 3 x_{3} &=2 \\ - x_{2} - x_{3} &=18 \\ 0 &=-1\end{aligned}\right.
$$

However, the final equation $0=-1$ gives a false statement. So the system has no solution.

### Changed RHS

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ -5 \\ -3\end{bmatrix},\quad a_2=\begin{bmatrix}4 \\ -21 \\ -12\end{bmatrix},\quad a_3=\begin{bmatrix}-3 \\ 14 \\ 9\end{bmatrix},\quad b=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ -5 \\ -3\end{bmatrix}+x_2\begin{bmatrix}4 \\ -21 \\ -12\end{bmatrix}+x_3\begin{bmatrix}-3 \\ 14 \\ 9\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ - 5 x_{1} \\ - 3 x_{1}\end{bmatrix}+\begin{bmatrix}4 x_{2} \\ - 21 x_{2} \\ - 12 x_{2}\end{bmatrix}+\begin{bmatrix}- 3 x_{3} \\ 14 x_{3} \\ 9 x_{3}\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix} \\ \begin{bmatrix}x_{1} + 4 x_{2} - 3 x_{3} \\ - 5 x_{1} - 21 x_{2} + 14 x_{3} \\ - 3 x_{1} - 12 x_{2} + 9 x_{3}\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + 4 x_{2} - 3 x_{3} &=0 \\ - 5 x_{1} - 21 x_{2} + 14 x_{3} &=-7 \\ - 3 x_{1} - 12 x_{2} + 9 x_{3} &=-9\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 4 & -3 & 0 \\ -5 & -21 & 14 & -7 \\ -3 & -12 & 9 & -9\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 4 & -3 & 0 \\ -5 & -21 & 14 & -7 \\ -3 & -12 & 9 & -9\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 4 & -3 & 0 \\ 0 & -1 & -1 & -7 \\ -3 & -12 & 9 & -9\end{array}\right] && R_{2}:=R_{2}+(5)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 4 & -3 & 0 \\ 0 & -1 & -1 & -7 \\ 0 & 0 & 0 & -9\end{array}\right] && R_{3}:=R_{3}+(3)R_{1}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + 4 x_{2} - 3 x_{3} &=0 \\ - x_{2} - x_{3} &=-7 \\ 0 &=-9\end{aligned}\right.
$$

However, the final equation $0=-9$ gives a false statement. So the system has no solution.

## q-34566

### Source

Consider the vectors

$$
{a}_{1}=\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix},\,{a}_{2}=\begin{bmatrix}2 \\ 5 \\ 6\end{bmatrix},\,{a}_{3}=\begin{bmatrix}3 \\ 2 \\ 9\end{bmatrix},\,b=\begin{bmatrix}-2 \\ -6 \\ 7\end{bmatrix}.
$$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b,$ then what is ${x}_{1}+{x}_{2}+{x}_{3}?$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b$, then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix}+{x}_{2}\begin{bmatrix}2 \\ 5 \\ 6\end{bmatrix}+{x}_{3}\begin{bmatrix}3 \\ 2 \\ 9\end{bmatrix} & =\begin{bmatrix}-2 \\ -6 \\ 7\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ 2{x}_{1} \\ 3{x}_{1}\end{bmatrix}+\begin{bmatrix}2{x}_{2} \\ 5{x}_{2} \\ 6{x}_{2}\end{bmatrix}+\begin{bmatrix}3{x}_{3} \\ 2{x}_{3} \\ 9{x}_{3}\end{bmatrix} & =\begin{bmatrix}-2 \\ -6 \\ 7\end{bmatrix} \\ \begin{bmatrix}{x}_{1}+2{x}_{2}+3{x}_{3} \\ 2{x}_{1}+5{x}_{2}+2{x}_{3} \\ 3{x}_{1}+6{x}_{2}+9{x}_{3}\end{bmatrix} & =\begin{bmatrix}-2 \\ -6 \\ 7\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}+2{x}_{2}+3{x}_{3} &=-2 \\ 2{x}_{1}+5{x}_{2}+2{x}_{3} &=-6 \\ 3{x}_{1}+6{x}_{2}+9{x}_{3} &=7\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\begin{bmatrix}1 & 2 & 3 & -2 \\ 2 & 5 & 2 & -6 \\ 3 & 6 & 9 & 7\end{bmatrix}.
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\begin{bmatrix}1 & 2 & 3 & -2 \\ 2 & 5 & 2 & -6 \\ 3 & 6 & 9 & 7\end{bmatrix} & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 3 & -2 \\ 0 & 1 & -4 & -2 \\ 3 & 6 & 9 & 7\end{bmatrix} & {R}_{3} & :={R}_{3}+(-3){R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 3 & -2 \\ 0 & 1 & -4 & -2 \\ 0 & 0 & 0 & 13\end{bmatrix}.\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}+2{x}_{2}+3{x}_{3} &=-2 \\ {x}_{2}-4{x}_{3} &=-2 \\ 0 &=13.\end{aligned}\right.
$$

However, the final equation $0=13$  gives a false statement. So the system has no solution.

### Replay

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix},\quad a_2=\begin{bmatrix}2 \\ 5 \\ 6\end{bmatrix},\quad a_3=\begin{bmatrix}3 \\ 2 \\ 9\end{bmatrix},\quad b=\begin{bmatrix}-2 \\ -6 \\ 7\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix}+x_2\begin{bmatrix}2 \\ 5 \\ 6\end{bmatrix}+x_3\begin{bmatrix}3 \\ 2 \\ 9\end{bmatrix}&=\begin{bmatrix}-2 \\ -6 \\ 7\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 2 x_{1} \\ 3 x_{1}\end{bmatrix}+\begin{bmatrix}2 x_{2} \\ 5 x_{2} \\ 6 x_{2}\end{bmatrix}+\begin{bmatrix}3 x_{3} \\ 2 x_{3} \\ 9 x_{3}\end{bmatrix}&=\begin{bmatrix}-2 \\ -6 \\ 7\end{bmatrix} \\ \begin{bmatrix}x_{1} + 2 x_{2} + 3 x_{3} \\ 2 x_{1} + 5 x_{2} + 2 x_{3} \\ 3 x_{1} + 6 x_{2} + 9 x_{3}\end{bmatrix}&=\begin{bmatrix}-2 \\ -6 \\ 7\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + 2 x_{2} + 3 x_{3} &=-2 \\ 2 x_{1} + 5 x_{2} + 2 x_{3} &=-6 \\ 3 x_{1} + 6 x_{2} + 9 x_{3} &=7\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 2 & 3 & -2 \\ 2 & 5 & 2 & -6 \\ 3 & 6 & 9 & 7\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 2 & 3 & -2 \\ 2 & 5 & 2 & -6 \\ 3 & 6 & 9 & 7\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 2 & 3 & -2 \\ 0 & 1 & -4 & -2 \\ 3 & 6 & 9 & 7\end{array}\right] && R_{2}:=R_{2}+(-2)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 2 & 3 & -2 \\ 0 & 1 & -4 & -2 \\ 0 & 0 & 0 & 13\end{array}\right] && R_{3}:=R_{3}+(-3)R_{1}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + 2 x_{2} + 3 x_{3} &=-2 \\ x_{2} - 4 x_{3} &=-2 \\ 0 &=13\end{aligned}\right.
$$

However, the final equation $0=13$ gives a false statement. So the system has no solution.

### Changed RHS

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix},\quad a_2=\begin{bmatrix}2 \\ 5 \\ 6\end{bmatrix},\quad a_3=\begin{bmatrix}3 \\ 2 \\ 9\end{bmatrix},\quad b=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix}+x_2\begin{bmatrix}2 \\ 5 \\ 6\end{bmatrix}+x_3\begin{bmatrix}3 \\ 2 \\ 9\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 2 x_{1} \\ 3 x_{1}\end{bmatrix}+\begin{bmatrix}2 x_{2} \\ 5 x_{2} \\ 6 x_{2}\end{bmatrix}+\begin{bmatrix}3 x_{3} \\ 2 x_{3} \\ 9 x_{3}\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix} \\ \begin{bmatrix}x_{1} + 2 x_{2} + 3 x_{3} \\ 2 x_{1} + 5 x_{2} + 2 x_{3} \\ 3 x_{1} + 6 x_{2} + 9 x_{3}\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + 2 x_{2} + 3 x_{3} &=0 \\ 2 x_{1} + 5 x_{2} + 2 x_{3} &=-7 \\ 3 x_{1} + 6 x_{2} + 9 x_{3} &=-9\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 2 & 3 & 0 \\ 2 & 5 & 2 & -7 \\ 3 & 6 & 9 & -9\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 2 & 3 & 0 \\ 2 & 5 & 2 & -7 \\ 3 & 6 & 9 & -9\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 2 & 3 & 0 \\ 0 & 1 & -4 & -7 \\ 3 & 6 & 9 & -9\end{array}\right] && R_{2}:=R_{2}+(-2)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 2 & 3 & 0 \\ 0 & 1 & -4 & -7 \\ 0 & 0 & 0 & -9\end{array}\right] && R_{3}:=R_{3}+(-3)R_{1}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + 2 x_{2} + 3 x_{3} &=0 \\ x_{2} - 4 x_{3} &=-7 \\ 0 &=-9\end{aligned}\right.
$$

However, the final equation $0=-9$ gives a false statement. So the system has no solution.

## q-73992

### Source

Consider the vectors

$$
{a}_{1}=\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix},\,{a}_{2}=\begin{bmatrix}-1 \\ 0 \\ -1\end{bmatrix},\,{a}_{3}=\begin{bmatrix}2 \\ 5 \\ 1\end{bmatrix},\,b=\begin{bmatrix}-5 \\ -10 \\ 1\end{bmatrix}.
$$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b,$ then what is ${x}_{1}+{x}_{2}+{x}_{3}?$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b$, then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix}+{x}_{2}\begin{bmatrix}-1 \\ 0 \\ -1\end{bmatrix}+{x}_{3}\begin{bmatrix}2 \\ 5 \\ 1\end{bmatrix} & =\begin{bmatrix}-5 \\ -10 \\ 1\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ 0 \\ 3{x}_{1}\end{bmatrix}+\begin{bmatrix}-{x}_{2} \\ 0 \\ -{x}_{2}\end{bmatrix}+\begin{bmatrix}2{x}_{3} \\ 5{x}_{3} \\ {x}_{3}\end{bmatrix} & =\begin{bmatrix}-5 \\ -10 \\ 1\end{bmatrix} \\ \begin{bmatrix}{x}_{1}-{x}_{2}+2{x}_{3} \\ 5{x}_{3} \\ 3{x}_{1}-{x}_{2}+{x}_{3}\end{bmatrix} & =\begin{bmatrix}-5 \\ -10 \\ 1\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}-{x}_{2}+2{x}_{3} &=-5 \\ 5{x}_{3} &=-10 \\ 3{x}_{1}-{x}_{2}+{x}_{3} &=1\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\begin{bmatrix}1 & -1 & 2 & -5 \\ 0 & 0 & 5 & -10 \\ 3 & -1 & 1 & 1\end{bmatrix}
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\begin{bmatrix}1 & -1 & 2 & -5 \\ 0 & 0 & 5 & -10 \\ 3 & -1 & 1 & 1\end{bmatrix} & {R}_{3} & :={R}_{3}-3{R}_{1} \\  & ∼\begin{bmatrix}1 & -1 & 2 & -5 \\ 0 & 0 & 5 & -10 \\ 0 & 2 & -5 & 16\end{bmatrix} & {R}_{2} & ↔{R}_{3} \\  & ∼\begin{bmatrix}1 & -1 & 2 & -5 \\ 0 & 2 & -5 & 16 \\ 0 & 0 & 5 & -10\end{bmatrix} & {R}_{2} & :=\frac{1}{2}{R}_{2} \\  & ∼\begin{bmatrix}1 & -1 & 2 & -5 \\ 0 & 1 & -2.5 & 8 \\ 0 & 0 & 5 & -10\end{bmatrix} & {R}_{3} & :=\frac{1}{5}{R}_{3} \\  & ∼\begin{bmatrix}1 & -1 & 2 & -5 \\ 0 & 1 & -2.5 & 8 \\ 0 & 0 & 1 & -2\end{bmatrix}.\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}-{x}_{2}+2{x}_{3} &=-5 \\ {x}_{2}-2.5\,{x}_{3} &=8 \\ {x}_{3} &=-2.\end{aligned}\right.
$$

From the third equation, we get ${x}_{3}=-2.$ Substituting this value into the second equation, we get 

$$
{x}_{2}-2.5(-2)=8\,⟹\,{x}_{2}=8-5=3.
$$

Finally,  substituting ${x}_{2}=3$ and ${x}_{3}=-2$  into the first equation, we obtain

$$
{x}_{1}-(3)+2(-2)=-5\,⟹\,{x}_{1}=2.
$$

So, the solution of the system is ${x}_{1}=2$, ${x}_{2}=3$, and ${x}_{3}=-2,$ which means 

$$
2{a}_{1}+3{a}_{2}-2{a}_{3}=b.
$$

Consequently, 

$$
{x}_{1}+{x}_{2}+{x}_{3}=2+3-2=3.
$$

### Replay

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix},\quad a_2=\begin{bmatrix}-1 \\ 0 \\ -1\end{bmatrix},\quad a_3=\begin{bmatrix}2 \\ 5 \\ 1\end{bmatrix},\quad b=\begin{bmatrix}-5 \\ -10 \\ 1\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix}+x_2\begin{bmatrix}-1 \\ 0 \\ -1\end{bmatrix}+x_3\begin{bmatrix}2 \\ 5 \\ 1\end{bmatrix}&=\begin{bmatrix}-5 \\ -10 \\ 1\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 0 \\ 3 x_{1}\end{bmatrix}+\begin{bmatrix}- x_{2} \\ 0 \\ - x_{2}\end{bmatrix}+\begin{bmatrix}2 x_{3} \\ 5 x_{3} \\ x_{3}\end{bmatrix}&=\begin{bmatrix}-5 \\ -10 \\ 1\end{bmatrix} \\ \begin{bmatrix}x_{1} - x_{2} + 2 x_{3} \\ 5 x_{3} \\ 3 x_{1} - x_{2} + x_{3}\end{bmatrix}&=\begin{bmatrix}-5 \\ -10 \\ 1\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} - x_{2} + 2 x_{3} &=-5 \\ 5 x_{3} &=-10 \\ 3 x_{1} - x_{2} + x_{3} &=1\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & -1 & 2 & -5 \\ 0 & 0 & 5 & -10 \\ 3 & -1 & 1 & 1\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & -1 & 2 & -5 \\ 0 & 0 & 5 & -10 \\ 3 & -1 & 1 & 1\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 2 & -5 \\ 0 & 0 & 5 & -10 \\ 0 & 2 & -5 & 16\end{array}\right] && R_{3}:=R_{3}+(-3)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 2 & -5 \\ 0 & 2 & -5 & 16 \\ 0 & 0 & 5 & -10\end{array}\right] && R_{2}\leftrightarrow R_{3} \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 2 & -5 \\ 0 & 1 & - \frac{5}{2} & 8 \\ 0 & 0 & 5 & -10\end{array}\right] && R_{2}:=(\frac{1}{2})R_{2} \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 2 & -5 \\ 0 & 1 & - \frac{5}{2} & 8 \\ 0 & 0 & 1 & -2\end{array}\right] && R_{3}:=(\frac{1}{5})R_{3}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} - x_{2} + 2 x_{3} &=-5 \\ x_{2} - \frac{5 x_{3}}{2} &=8 \\ x_{3} &=-2\end{aligned}\right.
$$

From the third equation, we get $x_3=-2.$ Substituting this value into the second equation, we get

$$
1x_2+(- \frac{5}{2})(-2)=8\quad\Rightarrow\quad x_2=3
$$

Finally, substituting these values into the first equation, we obtain

$$
x_1+(-1)(3)+(2)(-2)=-5\quad\Rightarrow\quad x_1=2
$$

So, the solution of the system is $x_1=2$, $x_2=3$, $x_3=-2$, which means

$$
2a_1+(3)a_2+(-2)a_3=b.
$$

Consequently,

$$
x_{1} + x_{2} + x_{3}=(2)+(3)+(-2)=3.
$$



### Changed RHS

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix},\quad a_2=\begin{bmatrix}-1 \\ 0 \\ -1\end{bmatrix},\quad a_3=\begin{bmatrix}2 \\ 5 \\ 1\end{bmatrix},\quad b=\begin{bmatrix}28 \\ 35 \\ 35\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix}+x_2\begin{bmatrix}-1 \\ 0 \\ -1\end{bmatrix}+x_3\begin{bmatrix}2 \\ 5 \\ 1\end{bmatrix}&=\begin{bmatrix}28 \\ 35 \\ 35\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 0 \\ 3 x_{1}\end{bmatrix}+\begin{bmatrix}- x_{2} \\ 0 \\ - x_{2}\end{bmatrix}+\begin{bmatrix}2 x_{3} \\ 5 x_{3} \\ x_{3}\end{bmatrix}&=\begin{bmatrix}28 \\ 35 \\ 35\end{bmatrix} \\ \begin{bmatrix}x_{1} - x_{2} + 2 x_{3} \\ 5 x_{3} \\ 3 x_{1} - x_{2} + x_{3}\end{bmatrix}&=\begin{bmatrix}28 \\ 35 \\ 35\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} - x_{2} + 2 x_{3} &=28 \\ 5 x_{3} &=35 \\ 3 x_{1} - x_{2} + x_{3} &=35\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & -1 & 2 & 28 \\ 0 & 0 & 5 & 35 \\ 3 & -1 & 1 & 35\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & -1 & 2 & 28 \\ 0 & 0 & 5 & 35 \\ 3 & -1 & 1 & 35\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 2 & 28 \\ 0 & 0 & 5 & 35 \\ 0 & 2 & -5 & -49\end{array}\right] && R_{3}:=R_{3}+(-3)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 2 & 28 \\ 0 & 2 & -5 & -49 \\ 0 & 0 & 5 & 35\end{array}\right] && R_{2}\leftrightarrow R_{3} \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 2 & 28 \\ 0 & 1 & - \frac{5}{2} & - \frac{49}{2} \\ 0 & 0 & 5 & 35\end{array}\right] && R_{2}:=(\frac{1}{2})R_{2} \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 2 & 28 \\ 0 & 1 & - \frac{5}{2} & - \frac{49}{2} \\ 0 & 0 & 1 & 7\end{array}\right] && R_{3}:=(\frac{1}{5})R_{3}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} - x_{2} + 2 x_{3} &=28 \\ x_{2} - \frac{5 x_{3}}{2} &=- \frac{49}{2} \\ x_{3} &=7\end{aligned}\right.
$$

From the third equation, we get $x_3=7.$ Substituting this value into the second equation, we get

$$
1x_2+(- \frac{5}{2})(7)=- \frac{49}{2}\quad\Rightarrow\quad x_2=-7
$$

Finally, substituting these values into the first equation, we obtain

$$
x_1+(-1)(-7)+(2)(7)=28\quad\Rightarrow\quad x_1=7
$$

So, the solution of the system is $x_1=7$, $x_2=-7$, $x_3=7$, which means

$$
7a_1+(-7)a_2+(7)a_3=b.
$$

Consequently,

$$
x_{1} + x_{2} + x_{3}=(7)+(-7)+(7)=7.
$$



## q-74006

### Source

Consider the vectors

$$
{a}_{1}=\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix},\,{a}_{2}=\begin{bmatrix}2 \\ -1 \\ -1\end{bmatrix},\,{a}_{3}=\begin{bmatrix}0 \\ -1 \\ -3\end{bmatrix},\,b=\begin{bmatrix}-2 \\ 5 \\ 1\end{bmatrix}.
$$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b,$ then what is ${x}_{1}+{x}_{2}+{x}_{3}?$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b,$ then   we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix}+{x}_{2}\begin{bmatrix}2 \\ -1 \\ -1\end{bmatrix}+{x}_{3}\begin{bmatrix}0 \\ -1 \\ -3\end{bmatrix} & =\begin{bmatrix}-2 \\ 5 \\ 1\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ 0 \\ {x}_{1}\end{bmatrix}+\begin{bmatrix}2{x}_{2} \\ -{x}_{2} \\ -{x}_{2}\end{bmatrix}+\begin{bmatrix}0 \\ -{x}_{3} \\ -3{x}_{3}\end{bmatrix} & =\begin{bmatrix}-2 \\ 5 \\ 1\end{bmatrix} \\ \begin{bmatrix}{x}_{1}+2{x}_{2} \\ -{x}_{2}-{x}_{3} \\ {x}_{1}-{x}_{2}-3{x}_{3}\end{bmatrix} & =\begin{bmatrix}-2 \\ 5 \\ 1\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}+2{x}_{2} &=-2 \\ -{x}_{2}-{x}_{3} &=5 \\ {x}_{1}-{x}_{2}-3{x}_{3} &=1\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\begin{bmatrix}1 & 2 & 0 & -2 \\ 0 & -1 & -1 & 5 \\ 1 & -1 & -3 & 1\end{bmatrix}.
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\begin{bmatrix}1 & 2 & 0 & -2 \\ 0 & -1 & -1 & 5 \\ 1 & -1 & -3 & 1\end{bmatrix} & {R}_{3} & :={R}_{3}+(-1){R}_{1} \\  & ∼\begin{bmatrix}1 & 2 & 0 & -2 \\ 0 & -1 & -1 & 5 \\ 0 & -3 & -3 & 3\end{bmatrix} & {R}_{2} & :=(-1){R}_{2} \\  & ∼\begin{bmatrix}1 & 2 & 0 & -2 \\ 0 & 1 & 1 & -5 \\ 0 & -3 & -3 & 3\end{bmatrix} & {R}_{3} & :={R}_{3}+3{R}_{2} \\  & ∼\begin{bmatrix}1 & 2 & 0 & -2 \\ 0 & 1 & 1 & -5 \\ 0 & 0 & 0 & -12\end{bmatrix}.\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}+2{x}_{2} &=-2 \\ {x}_{2}+{x}_{3} &=-5 \\ 0 &=-12.\end{aligned}\right.
$$

However, the final equation $0=-12$  gives a false statement. So the system has no solution.

### Replay

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix},\quad a_2=\begin{bmatrix}2 \\ -1 \\ -1\end{bmatrix},\quad a_3=\begin{bmatrix}0 \\ -1 \\ -3\end{bmatrix},\quad b=\begin{bmatrix}-2 \\ 5 \\ 1\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix}+x_2\begin{bmatrix}2 \\ -1 \\ -1\end{bmatrix}+x_3\begin{bmatrix}0 \\ -1 \\ -3\end{bmatrix}&=\begin{bmatrix}-2 \\ 5 \\ 1\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 0 \\ x_{1}\end{bmatrix}+\begin{bmatrix}2 x_{2} \\ - x_{2} \\ - x_{2}\end{bmatrix}+\begin{bmatrix}0 \\ - x_{3} \\ - 3 x_{3}\end{bmatrix}&=\begin{bmatrix}-2 \\ 5 \\ 1\end{bmatrix} \\ \begin{bmatrix}x_{1} + 2 x_{2} \\ - x_{2} - x_{3} \\ x_{1} - x_{2} - 3 x_{3}\end{bmatrix}&=\begin{bmatrix}-2 \\ 5 \\ 1\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + 2 x_{2} &=-2 \\ - x_{2} - x_{3} &=5 \\ x_{1} - x_{2} - 3 x_{3} &=1\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 2 & 0 & -2 \\ 0 & -1 & -1 & 5 \\ 1 & -1 & -3 & 1\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 2 & 0 & -2 \\ 0 & -1 & -1 & 5 \\ 1 & -1 & -3 & 1\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 2 & 0 & -2 \\ 0 & -1 & -1 & 5 \\ 0 & -3 & -3 & 3\end{array}\right] && R_{3}:=R_{3}+(-1)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 2 & 0 & -2 \\ 0 & 1 & 1 & -5 \\ 0 & -3 & -3 & 3\end{array}\right] && R_{2}:=(-1)R_{2} \\ &\sim \left[\begin{array}{ccc|c}1 & 2 & 0 & -2 \\ 0 & 1 & 1 & -5 \\ 0 & 0 & 0 & -12\end{array}\right] && R_{3}:=R_{3}+(3)R_{2}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + 2 x_{2} &=-2 \\ x_{2} + x_{3} &=-5 \\ 0 &=-12\end{aligned}\right.
$$

However, the final equation $0=-12$ gives a false statement. So the system has no solution.

### Changed RHS

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix},\quad a_2=\begin{bmatrix}2 \\ -1 \\ -1\end{bmatrix},\quad a_3=\begin{bmatrix}0 \\ -1 \\ -3\end{bmatrix},\quad b=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix}+x_2\begin{bmatrix}2 \\ -1 \\ -1\end{bmatrix}+x_3\begin{bmatrix}0 \\ -1 \\ -3\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 0 \\ x_{1}\end{bmatrix}+\begin{bmatrix}2 x_{2} \\ - x_{2} \\ - x_{2}\end{bmatrix}+\begin{bmatrix}0 \\ - x_{3} \\ - 3 x_{3}\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix} \\ \begin{bmatrix}x_{1} + 2 x_{2} \\ - x_{2} - x_{3} \\ x_{1} - x_{2} - 3 x_{3}\end{bmatrix}&=\begin{bmatrix}0 \\ -7 \\ -9\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + 2 x_{2} &=0 \\ - x_{2} - x_{3} &=-7 \\ x_{1} - x_{2} - 3 x_{3} &=-9\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 2 & 0 & 0 \\ 0 & -1 & -1 & -7 \\ 1 & -1 & -3 & -9\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 2 & 0 & 0 \\ 0 & -1 & -1 & -7 \\ 1 & -1 & -3 & -9\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 2 & 0 & 0 \\ 0 & -1 & -1 & -7 \\ 0 & -3 & -3 & -9\end{array}\right] && R_{3}:=R_{3}+(-1)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 2 & 0 & 0 \\ 0 & 1 & 1 & 7 \\ 0 & -3 & -3 & -9\end{array}\right] && R_{2}:=(-1)R_{2} \\ &\sim \left[\begin{array}{ccc|c}1 & 2 & 0 & 0 \\ 0 & 1 & 1 & 7 \\ 0 & 0 & 0 & 12\end{array}\right] && R_{3}:=R_{3}+(3)R_{2}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + 2 x_{2} &=0 \\ x_{2} + x_{3} &=7 \\ 0 &=12\end{aligned}\right.
$$

However, the final equation $0=12$ gives a false statement. So the system has no solution.

## q-74028

### Source

Consider the vectors

$$
{a}_{1}=\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix},\,{a}_{2}=\begin{bmatrix}1 \\ 3 \\ 1\end{bmatrix},\,{a}_{3}=\begin{bmatrix}3 \\ 3 \\ 1\end{bmatrix},\,b=\begin{bmatrix}-1 \\ -9 \\ 1\end{bmatrix}.
$$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b,$ then what is ${x}_{1}+{x}_{2}-{x}_{3}?$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b$, then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix}+{x}_{2}\begin{bmatrix}1 \\ 3 \\ 1\end{bmatrix}+{x}_{3}\begin{bmatrix}3 \\ 3 \\ 1\end{bmatrix} & =\begin{bmatrix}-1 \\ -9 \\ 1\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ 0 \\ {x}_{1}\end{bmatrix}+\begin{bmatrix}{x}_{2} \\ 3{x}_{2} \\ {x}_{2}\end{bmatrix}+\begin{bmatrix}3{x}_{3} \\ 3{x}_{3} \\ {x}_{3}\end{bmatrix} & =\begin{bmatrix}-1 \\ -9 \\ 1\end{bmatrix} \\ \begin{bmatrix}{x}_{1}+{x}_{2}+3{x}_{3} \\ 3{x}_{2}+3{x}_{3} \\ {x}_{1}+{x}_{2}+{x}_{3}\end{bmatrix} & =\begin{bmatrix}-1 \\ -9 \\ 1\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}+{x}_{2}+3{x}_{3} &=-1 \\ 3{x}_{2}+3{x}_{3} &=-9 \\ {x}_{1}+{x}_{2}+{x}_{3} &=1\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\begin{bmatrix}1 & 1 & 3 & -1 \\ 0 & 3 & 3 & -9 \\ 1 & 1 & 1 & 1\end{bmatrix}.
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\begin{bmatrix}1 & 1 & 3 & -1 \\ 0 & 3 & 3 & -9 \\ 1 & 1 & 1 & 1\end{bmatrix} & {R}_{3} & :={R}_{3}+(-1){R}_{1} \\  & ∼\begin{bmatrix}1 & 1 & 3 & -1 \\ 0 & 3 & 3 & -9 \\ 0 & 0 & -2 & 2\end{bmatrix} & {R}_{2} & :=\frac{1}{3}{R}_{2} \\  & ∼\begin{bmatrix}1 & 1 & 3 & -1 \\ 0 & 1 & 1 & -3 \\ 0 & 0 & -2 & 2\end{bmatrix} & {R}_{3} & :=-\frac{1}{2}{R}_{3} \\  & ∼\begin{bmatrix}1 & 1 & 3 & -1 \\ 0 & 1 & 1 & -3 \\ 0 & 0 & 1 & -1\end{bmatrix}.\end{aligned}
$$

 

The system is now 

$$
\left\{\begin{aligned}{x}_{1}+{x}_{2}+3{x}_{3} &=-1 \\ {x}_{2}+{x}_{3} &=-3 \\ {x}_{3} &=-1.\end{aligned}\right.
$$

 

From the third equation, we get ${x}_{3}=-1.$ Substituting this value into the second equation, we get

$$
{x}_{2}+(-1)=-3\,⟹\,{x}_{2}=-2.
$$

Finally, by substituting ${x}_{2}=-2,{x}_{3}=-1$ into the first equation, we obtain

$$
\begin{aligned}{x}_{1}+{x}_{2}+3{x}_{3} & =-1 \\ {x}_{1}+(-2)+3(-1) & =-1 \\ {x}_{1}-5 & =-1 \\ {x}_{1} & =4.\end{aligned}
$$

So, the solution of the system is ${x}_{1}=4$, ${x}_{2}=-2$, and ${x}_{3}=-1,$ which means 

$$
4{a}_{1}-2{a}_{2}-{a}_{3}=b.
$$

Consequently, 

$$
{x}_{1}+{x}_{2}-{x}_{3}=4+(-2)-(-1)=3.
$$

### Replay

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix},\quad a_2=\begin{bmatrix}1 \\ 3 \\ 1\end{bmatrix},\quad a_3=\begin{bmatrix}3 \\ 3 \\ 1\end{bmatrix},\quad b=\begin{bmatrix}-1 \\ -9 \\ 1\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} - x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix}+x_2\begin{bmatrix}1 \\ 3 \\ 1\end{bmatrix}+x_3\begin{bmatrix}3 \\ 3 \\ 1\end{bmatrix}&=\begin{bmatrix}-1 \\ -9 \\ 1\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 0 \\ x_{1}\end{bmatrix}+\begin{bmatrix}x_{2} \\ 3 x_{2} \\ x_{2}\end{bmatrix}+\begin{bmatrix}3 x_{3} \\ 3 x_{3} \\ x_{3}\end{bmatrix}&=\begin{bmatrix}-1 \\ -9 \\ 1\end{bmatrix} \\ \begin{bmatrix}x_{1} + x_{2} + 3 x_{3} \\ 3 x_{2} + 3 x_{3} \\ x_{1} + x_{2} + x_{3}\end{bmatrix}&=\begin{bmatrix}-1 \\ -9 \\ 1\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + x_{2} + 3 x_{3} &=-1 \\ 3 x_{2} + 3 x_{3} &=-9 \\ x_{1} + x_{2} + x_{3} &=1\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 1 & 3 & -1 \\ 0 & 3 & 3 & -9 \\ 1 & 1 & 1 & 1\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 1 & 3 & -1 \\ 0 & 3 & 3 & -9 \\ 1 & 1 & 1 & 1\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & 3 & -1 \\ 0 & 3 & 3 & -9 \\ 0 & 0 & -2 & 2\end{array}\right] && R_{3}:=R_{3}+(-1)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & 3 & -1 \\ 0 & 1 & 1 & -3 \\ 0 & 0 & -2 & 2\end{array}\right] && R_{2}:=(\frac{1}{3})R_{2} \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & 3 & -1 \\ 0 & 1 & 1 & -3 \\ 0 & 0 & 1 & -1\end{array}\right] && R_{3}:=(- \frac{1}{2})R_{3}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + x_{2} + 3 x_{3} &=-1 \\ x_{2} + x_{3} &=-3 \\ x_{3} &=-1\end{aligned}\right.
$$

From the third equation, we get $x_3=-1.$ Substituting this value into the second equation, we get

$$
1x_2+(1)(-1)=-3\quad\Rightarrow\quad x_2=-2
$$

Finally, substituting these values into the first equation, we obtain

$$
x_1+(1)(-2)+(3)(-1)=-1\quad\Rightarrow\quad x_1=4
$$

So, the solution of the system is $x_1=4$, $x_2=-2$, $x_3=-1$, which means

$$
4a_1+(-2)a_2+(-1)a_3=b.
$$

Consequently,

$$
x_{1} + x_{2} - x_{3}=(4)+(-2)+(1)=3.
$$



### Changed RHS

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix},\quad a_2=\begin{bmatrix}1 \\ 3 \\ 1\end{bmatrix},\quad a_3=\begin{bmatrix}3 \\ 3 \\ 1\end{bmatrix},\quad b=\begin{bmatrix}21 \\ 0 \\ 7\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} - x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix}+x_2\begin{bmatrix}1 \\ 3 \\ 1\end{bmatrix}+x_3\begin{bmatrix}3 \\ 3 \\ 1\end{bmatrix}&=\begin{bmatrix}21 \\ 0 \\ 7\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 0 \\ x_{1}\end{bmatrix}+\begin{bmatrix}x_{2} \\ 3 x_{2} \\ x_{2}\end{bmatrix}+\begin{bmatrix}3 x_{3} \\ 3 x_{3} \\ x_{3}\end{bmatrix}&=\begin{bmatrix}21 \\ 0 \\ 7\end{bmatrix} \\ \begin{bmatrix}x_{1} + x_{2} + 3 x_{3} \\ 3 x_{2} + 3 x_{3} \\ x_{1} + x_{2} + x_{3}\end{bmatrix}&=\begin{bmatrix}21 \\ 0 \\ 7\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + x_{2} + 3 x_{3} &=21 \\ 3 x_{2} + 3 x_{3} &=0 \\ x_{1} + x_{2} + x_{3} &=7\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 1 & 3 & 21 \\ 0 & 3 & 3 & 0 \\ 1 & 1 & 1 & 7\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 1 & 3 & 21 \\ 0 & 3 & 3 & 0 \\ 1 & 1 & 1 & 7\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & 3 & 21 \\ 0 & 3 & 3 & 0 \\ 0 & 0 & -2 & -14\end{array}\right] && R_{3}:=R_{3}+(-1)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & 3 & 21 \\ 0 & 1 & 1 & 0 \\ 0 & 0 & -2 & -14\end{array}\right] && R_{2}:=(\frac{1}{3})R_{2} \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & 3 & 21 \\ 0 & 1 & 1 & 0 \\ 0 & 0 & 1 & 7\end{array}\right] && R_{3}:=(- \frac{1}{2})R_{3}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + x_{2} + 3 x_{3} &=21 \\ x_{2} + x_{3} &=0 \\ x_{3} &=7\end{aligned}\right.
$$

From the third equation, we get $x_3=7.$ Substituting this value into the second equation, we get

$$
1x_2+(1)(7)=0\quad\Rightarrow\quad x_2=-7
$$

Finally, substituting these values into the first equation, we obtain

$$
x_1+(1)(-7)+(3)(7)=21\quad\Rightarrow\quad x_1=7
$$

So, the solution of the system is $x_1=7$, $x_2=-7$, $x_3=7$, which means

$$
7a_1+(-7)a_2+(7)a_3=b.
$$

Consequently,

$$
x_{1} + x_{2} - x_{3}=(7)+(-7)+(-7)=-7.
$$



## q-74032

### Source

Consider the vectors

$$
{a}_{1}=\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix},\,{a}_{2}=\begin{bmatrix}1 \\ -2 \\ 2\end{bmatrix},\,{a}_{3}=\begin{bmatrix}3 \\ -11 \\ 1\end{bmatrix},\,b=\begin{bmatrix}5 \\ -18 \\ -1\end{bmatrix}.
$$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b,$ then what is ${x}_{1}+{x}_{2}+{x}_{3}?$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b$, then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix}+{x}_{2}\begin{bmatrix}1 \\ -2 \\ 2\end{bmatrix}+{x}_{3}\begin{bmatrix}3 \\ -11 \\ 1\end{bmatrix} & =\begin{bmatrix}5 \\ -18 \\ -1\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ 0 \\ {x}_{1}\end{bmatrix}+\begin{bmatrix}{x}_{2} \\ -2{x}_{2} \\ 2{x}_{2}\end{bmatrix}+\begin{bmatrix}3{x}_{3} \\ -11{x}_{3} \\ {x}_{3}\end{bmatrix} & =\begin{bmatrix}5 \\ -18 \\ -1\end{bmatrix} \\ \begin{bmatrix}{x}_{1}+{x}_{2}+3{x}_{3} \\ -2{x}_{2}-11{x}_{3} \\ {x}_{1}+2{x}_{2}+{x}_{3}\end{bmatrix} & =\begin{bmatrix}5 \\ -18 \\ -1\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}+{x}_{2}+3{x}_{3} &=5 \\ -2{x}_{2}-11{x}_{3} &=-18 \\ {x}_{1}+2{x}_{2}+{x}_{3} &=-1\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\begin{bmatrix}1 & 1 & 3 & 5 \\ 0 & -2 & -11 & -18 \\ 1 & 2 & 1 & -1\end{bmatrix}.
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\begin{bmatrix}1 & 1 & 3 & 5 \\ 0 & -2 & -11 & -18 \\ 1 & 2 & 1 & -1\end{bmatrix} & {R}_{3} & :={R}_{3}+(-1){R}_{1} \\  & ∼\begin{bmatrix}1 & 1 & 3 & 5 \\ 0 & -2 & -11 & -18 \\ 0 & 1 & -2 & -6\end{bmatrix} & {R}_{2} & ↔{R}_{3} \\  & ∼\begin{bmatrix}1 & 1 & 3 & -1 \\ 0 & 1 & -2 & -6 \\ 0 & -2 & -11 & -18\end{bmatrix} & {R}_{3} & :={R}_{3}+2{R}_{2} \\  & ∼\begin{bmatrix}1 & 1 & 3 & 5 \\ 0 & 1 & -2 & -6 \\ 0 & 0 & -15 & -30\end{bmatrix} & {R}_{3} & :=-\frac{1}{15}{R}_{3} \\  & ∼\begin{bmatrix}1 & 1 & 3 & 5 \\ 0 & 1 & -2 & -6 \\ 0 & 0 & 1 & 2\end{bmatrix}.\end{aligned}
$$

 

The system is now 

$$
\left\{\begin{aligned}{x}_{1}+{x}_{2}+3{x}_{3} &=5 \\ {x}_{2}-2{x}_{3} &=-6 \\ {x}_{3} &=2.\end{aligned}\right.
$$

 

From the third equation, we get ${x}_{3}=2.$ Substituting this value into  the second equation, we get

$$
{x}_{2}-2(2)=-6\,⟹\,{x}_{2}=-2.
$$

 

Finally, by substituting ${x}_{2}=-2$ and ${x}_{3}=2$ into the first equation, we obtain 

$$
\begin{aligned}{x}_{1}+{x}_{2}+3{x}_{3} & =5 \\ {x}_{1}+(-2)+3(2) & =5 \\ {x}_{1}+4 & =5 \\ {x}_{1} & =1.\end{aligned}
$$

So, the solution of the system is ${x}_{1}=1$, ${x}_{2}=-2$, and ${x}_{3}=2,$ which means 

$$
{a}_{1}-2{a}_{2}+2{a}_{3}=b.
$$

Consequently, 

$$
{x}_{1}+{x}_{2}+{x}_{3}=1+(-2)+2=1.
$$

### Replay

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix},\quad a_2=\begin{bmatrix}1 \\ -2 \\ 2\end{bmatrix},\quad a_3=\begin{bmatrix}3 \\ -11 \\ 1\end{bmatrix},\quad b=\begin{bmatrix}5 \\ -18 \\ -1\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix}+x_2\begin{bmatrix}1 \\ -2 \\ 2\end{bmatrix}+x_3\begin{bmatrix}3 \\ -11 \\ 1\end{bmatrix}&=\begin{bmatrix}5 \\ -18 \\ -1\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 0 \\ x_{1}\end{bmatrix}+\begin{bmatrix}x_{2} \\ - 2 x_{2} \\ 2 x_{2}\end{bmatrix}+\begin{bmatrix}3 x_{3} \\ - 11 x_{3} \\ x_{3}\end{bmatrix}&=\begin{bmatrix}5 \\ -18 \\ -1\end{bmatrix} \\ \begin{bmatrix}x_{1} + x_{2} + 3 x_{3} \\ - 2 x_{2} - 11 x_{3} \\ x_{1} + 2 x_{2} + x_{3}\end{bmatrix}&=\begin{bmatrix}5 \\ -18 \\ -1\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + x_{2} + 3 x_{3} &=5 \\ - 2 x_{2} - 11 x_{3} &=-18 \\ x_{1} + 2 x_{2} + x_{3} &=-1\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 1 & 3 & 5 \\ 0 & -2 & -11 & -18 \\ 1 & 2 & 1 & -1\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 1 & 3 & 5 \\ 0 & -2 & -11 & -18 \\ 1 & 2 & 1 & -1\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & 3 & 5 \\ 0 & -2 & -11 & -18 \\ 0 & 1 & -2 & -6\end{array}\right] && R_{3}:=R_{3}+(-1)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & 3 & 5 \\ 0 & 1 & -2 & -6 \\ 0 & -2 & -11 & -18\end{array}\right] && R_{2}\leftrightarrow R_{3} \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & 3 & 5 \\ 0 & 1 & -2 & -6 \\ 0 & 0 & -15 & -30\end{array}\right] && R_{3}:=R_{3}+(2)R_{2} \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & 3 & 5 \\ 0 & 1 & -2 & -6 \\ 0 & 0 & 1 & 2\end{array}\right] && R_{3}:=(- \frac{1}{15})R_{3}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + x_{2} + 3 x_{3} &=5 \\ x_{2} - 2 x_{3} &=-6 \\ x_{3} &=2\end{aligned}\right.
$$

From the third equation, we get $x_3=2.$ Substituting this value into the second equation, we get

$$
1x_2+(-2)(2)=-6\quad\Rightarrow\quad x_2=-2
$$

Finally, substituting these values into the first equation, we obtain

$$
x_1+(1)(-2)+(3)(2)=5\quad\Rightarrow\quad x_1=1
$$

So, the solution of the system is $x_1=1$, $x_2=-2$, $x_3=2$, which means

$$
1a_1+(-2)a_2+(2)a_3=b.
$$

Consequently,

$$
x_{1} + x_{2} + x_{3}=(1)+(-2)+(2)=1.
$$



### Changed RHS

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix},\quad a_2=\begin{bmatrix}1 \\ -2 \\ 2\end{bmatrix},\quad a_3=\begin{bmatrix}3 \\ -11 \\ 1\end{bmatrix},\quad b=\begin{bmatrix}21 \\ -63 \\ 0\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 0 \\ 1\end{bmatrix}+x_2\begin{bmatrix}1 \\ -2 \\ 2\end{bmatrix}+x_3\begin{bmatrix}3 \\ -11 \\ 1\end{bmatrix}&=\begin{bmatrix}21 \\ -63 \\ 0\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 0 \\ x_{1}\end{bmatrix}+\begin{bmatrix}x_{2} \\ - 2 x_{2} \\ 2 x_{2}\end{bmatrix}+\begin{bmatrix}3 x_{3} \\ - 11 x_{3} \\ x_{3}\end{bmatrix}&=\begin{bmatrix}21 \\ -63 \\ 0\end{bmatrix} \\ \begin{bmatrix}x_{1} + x_{2} + 3 x_{3} \\ - 2 x_{2} - 11 x_{3} \\ x_{1} + 2 x_{2} + x_{3}\end{bmatrix}&=\begin{bmatrix}21 \\ -63 \\ 0\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + x_{2} + 3 x_{3} &=21 \\ - 2 x_{2} - 11 x_{3} &=-63 \\ x_{1} + 2 x_{2} + x_{3} &=0\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 1 & 3 & 21 \\ 0 & -2 & -11 & -63 \\ 1 & 2 & 1 & 0\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 1 & 3 & 21 \\ 0 & -2 & -11 & -63 \\ 1 & 2 & 1 & 0\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & 3 & 21 \\ 0 & -2 & -11 & -63 \\ 0 & 1 & -2 & -21\end{array}\right] && R_{3}:=R_{3}+(-1)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & 3 & 21 \\ 0 & 1 & -2 & -21 \\ 0 & -2 & -11 & -63\end{array}\right] && R_{2}\leftrightarrow R_{3} \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & 3 & 21 \\ 0 & 1 & -2 & -21 \\ 0 & 0 & -15 & -105\end{array}\right] && R_{3}:=R_{3}+(2)R_{2} \\ &\sim \left[\begin{array}{ccc|c}1 & 1 & 3 & 21 \\ 0 & 1 & -2 & -21 \\ 0 & 0 & 1 & 7\end{array}\right] && R_{3}:=(- \frac{1}{15})R_{3}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + x_{2} + 3 x_{3} &=21 \\ x_{2} - 2 x_{3} &=-21 \\ x_{3} &=7\end{aligned}\right.
$$

From the third equation, we get $x_3=7.$ Substituting this value into the second equation, we get

$$
1x_2+(-2)(7)=-21\quad\Rightarrow\quad x_2=-7
$$

Finally, substituting these values into the first equation, we obtain

$$
x_1+(1)(-7)+(3)(7)=21\quad\Rightarrow\quad x_1=7
$$

So, the solution of the system is $x_1=7$, $x_2=-7$, $x_3=7$, which means

$$
7a_1+(-7)a_2+(7)a_3=b.
$$

Consequently,

$$
x_{1} + x_{2} + x_{3}=(7)+(-7)+(7)=7.
$$



## q-74035

### Source

Consider the vectors

$$
{a}_{1}=\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix},\,{a}_{2}=\begin{bmatrix}-1 \\ 5 \\ 2\end{bmatrix},\,{a}_{3}=\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix},\,b=\begin{bmatrix}-3 \\ 4 \\ -4\end{bmatrix}.
$$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b,$ then what is ${x}_{1}+{x}_{2}+{x}_{3}?$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b$, then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix}+{x}_{2}\begin{bmatrix}-1 \\ 5 \\ 2\end{bmatrix}+{x}_{3}\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix} & =\begin{bmatrix}-3 \\ 4 \\ -4\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ 0 \\ 3{x}_{1}\end{bmatrix}+\begin{bmatrix}-{x}_{2} \\ 5{x}_{2} \\ 2{x}_{2}\end{bmatrix}+\begin{bmatrix}0 \\ {x}_{3} \\ 0\end{bmatrix} & =\begin{bmatrix}-3 \\ 4 \\ -4\end{bmatrix} \\ \begin{bmatrix}{x}_{1}-{x}_{2} \\ 5{x}_{2}+{x}_{3} \\ 3{x}_{1}+2{x}_{2}\end{bmatrix} & =\begin{bmatrix}-3 \\ 4 \\ -4\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}-{x}_{2} &=-3 \\ 5{x}_{2}+{x}_{3} &=4 \\ 3{x}_{1}+2{x}_{2} &=-4\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\begin{bmatrix}1 & -1 & 0 & -3 \\ 0 & 5 & 1 & 4 \\ 3 & 2 & 0 & -4\end{bmatrix}
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\begin{bmatrix}1 & -1 & 0 & -3 \\ 0 & 5 & 1 & 4 \\ 3 & 2 & 0 & -4\end{bmatrix} & {R}_{3} & :={R}_{3}+(-3){R}_{1} \\  & ∼\begin{bmatrix}1 & -1 & 0 & -3 \\ 0 & 5 & 1 & 4 \\ 0 & 5 & 0 & 5\end{bmatrix} & {R}_{3} & :={R}_{3}+(-1){R}_{2} \\  & ∼\begin{bmatrix}1 & -1 & 0 & -3 \\ 0 & 5 & 1 & 4 \\ 0 & 0 & -1 & 1\end{bmatrix} & {R}_{2} & :=\frac{1}{5}{R}_{2} \\  & ∼\begin{bmatrix}1 & -1 & 0 & -3 \\ 0 & 1 & 0.2 & 0.8 \\ 0 & 0 & -1 & 1\end{bmatrix} & {R}_{3} & :=-{R}_{3} \\  & ∼\begin{bmatrix}1 & -1 & 0 & -3 \\ 0 & 1 & 0.2 & 0.8 \\ 0 & 0 & 1 & -1\end{bmatrix}.\end{aligned}
$$

The system is now 

$$
\left\{\begin{aligned}{x}_{1}-{x}_{2} &=-3 \\ {x}_{2}+\,0.2{x}_{3} &=0.8 \\ {x}_{3} &=-1.\end{aligned}\right.
$$

From the third equation, we get ${x}_{3}=-1.$ Substituting this value into the second equation, we get 

$$
{x}_{2}+0.2(-1)=0.8\,⟹\,{x}_{2}=1.
$$

   

Finally,  substituting ${x}_{2}=1$ into the first equation, we obtain

$$
{x}_{1}-(1)=-3\,⟹\,{x}_{1}=-2.
$$

So, the solution of the system is ${x}_{1}=-2$, ${x}_{2}=1$, and ${x}_{3}=-1,$ which means  

$$
-2{a}_{1}+{a}_{2}-{a}_{3}=b.
$$

Consequently, 

$$
{x}_{1}+{x}_{2}+{x}_{3}=-2+1-1=-2.
$$

### Replay

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix},\quad a_2=\begin{bmatrix}-1 \\ 5 \\ 2\end{bmatrix},\quad a_3=\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix},\quad b=\begin{bmatrix}-3 \\ 4 \\ -4\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix}+x_2\begin{bmatrix}-1 \\ 5 \\ 2\end{bmatrix}+x_3\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix}&=\begin{bmatrix}-3 \\ 4 \\ -4\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 0 \\ 3 x_{1}\end{bmatrix}+\begin{bmatrix}- x_{2} \\ 5 x_{2} \\ 2 x_{2}\end{bmatrix}+\begin{bmatrix}0 \\ x_{3} \\ 0\end{bmatrix}&=\begin{bmatrix}-3 \\ 4 \\ -4\end{bmatrix} \\ \begin{bmatrix}x_{1} - x_{2} \\ 5 x_{2} + x_{3} \\ 3 x_{1} + 2 x_{2}\end{bmatrix}&=\begin{bmatrix}-3 \\ 4 \\ -4\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} - x_{2} &=-3 \\ 5 x_{2} + x_{3} &=4 \\ 3 x_{1} + 2 x_{2} &=-4\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & -1 & 0 & -3 \\ 0 & 5 & 1 & 4 \\ 3 & 2 & 0 & -4\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & -1 & 0 & -3 \\ 0 & 5 & 1 & 4 \\ 3 & 2 & 0 & -4\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 0 & -3 \\ 0 & 5 & 1 & 4 \\ 0 & 5 & 0 & 5\end{array}\right] && R_{3}:=R_{3}+(-3)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 0 & -3 \\ 0 & 5 & 1 & 4 \\ 0 & 0 & -1 & 1\end{array}\right] && R_{3}:=R_{3}+(-1)R_{2} \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 0 & -3 \\ 0 & 1 & \frac{1}{5} & \frac{4}{5} \\ 0 & 0 & -1 & 1\end{array}\right] && R_{2}:=(\frac{1}{5})R_{2} \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 0 & -3 \\ 0 & 1 & \frac{1}{5} & \frac{4}{5} \\ 0 & 0 & 1 & -1\end{array}\right] && R_{3}:=(-1)R_{3}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} - x_{2} &=-3 \\ x_{2} + \frac{x_{3}}{5} &=\frac{4}{5} \\ x_{3} &=-1\end{aligned}\right.
$$

From the third equation, we get $x_3=-1.$ Substituting this value into the second equation, we get

$$
1x_2+(\frac{1}{5})(-1)=\frac{4}{5}\quad\Rightarrow\quad x_2=1
$$

Finally, substituting these values into the first equation, we obtain

$$
x_1+(-1)(1)+(0)(-1)=-3\quad\Rightarrow\quad x_1=-2
$$

So, the solution of the system is $x_1=-2$, $x_2=1$, $x_3=-1$, which means

$$
-2a_1+(1)a_2+(-1)a_3=b.
$$

Consequently,

$$
x_{1} + x_{2} + x_{3}=(-2)+(1)+(-1)=-2.
$$



### Changed RHS

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix},\quad a_2=\begin{bmatrix}-1 \\ 5 \\ 2\end{bmatrix},\quad a_3=\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix},\quad b=\begin{bmatrix}14 \\ -28 \\ 7\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 0 \\ 3\end{bmatrix}+x_2\begin{bmatrix}-1 \\ 5 \\ 2\end{bmatrix}+x_3\begin{bmatrix}0 \\ 1 \\ 0\end{bmatrix}&=\begin{bmatrix}14 \\ -28 \\ 7\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 0 \\ 3 x_{1}\end{bmatrix}+\begin{bmatrix}- x_{2} \\ 5 x_{2} \\ 2 x_{2}\end{bmatrix}+\begin{bmatrix}0 \\ x_{3} \\ 0\end{bmatrix}&=\begin{bmatrix}14 \\ -28 \\ 7\end{bmatrix} \\ \begin{bmatrix}x_{1} - x_{2} \\ 5 x_{2} + x_{3} \\ 3 x_{1} + 2 x_{2}\end{bmatrix}&=\begin{bmatrix}14 \\ -28 \\ 7\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} - x_{2} &=14 \\ 5 x_{2} + x_{3} &=-28 \\ 3 x_{1} + 2 x_{2} &=7\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & -1 & 0 & 14 \\ 0 & 5 & 1 & -28 \\ 3 & 2 & 0 & 7\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & -1 & 0 & 14 \\ 0 & 5 & 1 & -28 \\ 3 & 2 & 0 & 7\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 0 & 14 \\ 0 & 5 & 1 & -28 \\ 0 & 5 & 0 & -35\end{array}\right] && R_{3}:=R_{3}+(-3)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 0 & 14 \\ 0 & 5 & 1 & -28 \\ 0 & 0 & -1 & -7\end{array}\right] && R_{3}:=R_{3}+(-1)R_{2} \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 0 & 14 \\ 0 & 1 & \frac{1}{5} & - \frac{28}{5} \\ 0 & 0 & -1 & -7\end{array}\right] && R_{2}:=(\frac{1}{5})R_{2} \\ &\sim \left[\begin{array}{ccc|c}1 & -1 & 0 & 14 \\ 0 & 1 & \frac{1}{5} & - \frac{28}{5} \\ 0 & 0 & 1 & 7\end{array}\right] && R_{3}:=(-1)R_{3}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} - x_{2} &=14 \\ x_{2} + \frac{x_{3}}{5} &=- \frac{28}{5} \\ x_{3} &=7\end{aligned}\right.
$$

From the third equation, we get $x_3=7.$ Substituting this value into the second equation, we get

$$
1x_2+(\frac{1}{5})(7)=- \frac{28}{5}\quad\Rightarrow\quad x_2=-7
$$

Finally, substituting these values into the first equation, we obtain

$$
x_1+(-1)(-7)+(0)(7)=14\quad\Rightarrow\quad x_1=7
$$

So, the solution of the system is $x_1=7$, $x_2=-7$, $x_3=7$, which means

$$
7a_1+(-7)a_2+(7)a_3=b.
$$

Consequently,

$$
x_{1} + x_{2} + x_{3}=(7)+(-7)+(7)=7.
$$



## q-74046

### Source

Consider the vectors

$$
{a}_{1}=\begin{bmatrix}1 \\ 0 \\ 2\end{bmatrix},\,{a}_{2}=\begin{bmatrix}0 \\ 1 \\ -1\end{bmatrix},\,{a}_{3}=\begin{bmatrix}1 \\ -2 \\ 0\end{bmatrix},\,b=\begin{bmatrix}8 \\ -6 \\ 2\end{bmatrix}.
$$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b,$ then what is ${x}_{1}+{x}_{2}+{x}_{3}?$

If ${x}_{1}{a}_{1}+{x}_{2}{a}_{2}+{x}_{3}{a}_{3}=b$, then we have

$$
\begin{aligned}{x}_{1}\begin{bmatrix}1 \\ 0 \\ 2\end{bmatrix}+{x}_{2}\begin{bmatrix}0 \\ 1 \\ -1\end{bmatrix}+{x}_{3}\begin{bmatrix}1 \\ -2 \\ 0\end{bmatrix} & =\begin{bmatrix}8 \\ -6 \\ 2\end{bmatrix} \\ \begin{bmatrix}{x}_{1} \\ 0 \\ 2{x}_{1}\end{bmatrix}+\begin{bmatrix}0 \\ {x}_{2} \\ -{x}_{2}\end{bmatrix}+\begin{bmatrix}{x}_{3} \\ -2{x}_{3} \\ 0\end{bmatrix} & =\begin{bmatrix}8 \\ -6 \\ 2\end{bmatrix} \\ \begin{bmatrix}{x}_{1}+{x}_{3} \\ {x}_{2}-2{x}_{3} \\ 2{x}_{1}-{x}_{2}\end{bmatrix} & =\begin{bmatrix}8 \\ -6 \\ 2\end{bmatrix}.\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}{x}_{1}+{x}_{3} &=8 \\ {x}_{2}-2{x}_{3} &=-6 \\ 2{x}_{1}-{x}_{2} &=2\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\begin{bmatrix}1 & 0 & 1 & 8 \\ 0 & 1 & -2 & -6 \\ 2 & -1 & 0 & 2\end{bmatrix}
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M & =\begin{bmatrix}1 & 0 & 1 & 8 \\ 0 & 1 & -2 & -6 \\ 2 & -1 & 0 & 2\end{bmatrix} & {R}_{3} & :={R}_{3}-2{R}_{1} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 8 \\ 0 & 1 & -2 & -6 \\ 0 & -1 & -2 & -14\end{bmatrix} & {R}_{3} & :={R}_{3}+{R}_{2} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 8 \\ 0 & 1 & -2 & -6 \\ 0 & 0 & -4 & -20\end{bmatrix} & {R}_{3} & :=-\frac{1}{4}{R}_{3} \\  & ∼\begin{bmatrix}1 & 0 & 1 & 8 \\ 0 & 1 & -2 & -6 \\ 0 & 0 & 1 & 5\end{bmatrix}.\end{aligned}
$$

So, the system is now 

$$
\left\{\begin{aligned}{x}_{1}+{x}_{3} &=8 \\ {x}_{2}-2{x}_{3} &=-6 \\ {x}_{3} &=5.\end{aligned}\right.
$$

From the third equation, we get ${x}_{3}=5.$ Substituting this value in the second and first equations, we obtain

$$
\begin{aligned} & {x}_{2}-2(5)=-6\,⟹\,{x}_{2}=4 \\  & {x}_{1}+5=8\,⟹\,{x}_{1}=3.\end{aligned}
$$

So, the solution of the system is ${x}_{1}=3$, ${x}_{2}=4$, and ${x}_{3}=5,$ which means 

$$
3{a}_{1}+4{a}_{2}+5{a}_{3}=b.
$$

Consequently, 

$$
{x}_{1}+{x}_{2}+{x}_{3}=3+4+5=12.
$$

### Replay

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 0 \\ 2\end{bmatrix},\quad a_2=\begin{bmatrix}0 \\ 1 \\ -1\end{bmatrix},\quad a_3=\begin{bmatrix}1 \\ -2 \\ 0\end{bmatrix},\quad b=\begin{bmatrix}8 \\ -6 \\ 2\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 0 \\ 2\end{bmatrix}+x_2\begin{bmatrix}0 \\ 1 \\ -1\end{bmatrix}+x_3\begin{bmatrix}1 \\ -2 \\ 0\end{bmatrix}&=\begin{bmatrix}8 \\ -6 \\ 2\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 0 \\ 2 x_{1}\end{bmatrix}+\begin{bmatrix}0 \\ x_{2} \\ - x_{2}\end{bmatrix}+\begin{bmatrix}x_{3} \\ - 2 x_{3} \\ 0\end{bmatrix}&=\begin{bmatrix}8 \\ -6 \\ 2\end{bmatrix} \\ \begin{bmatrix}x_{1} + x_{3} \\ x_{2} - 2 x_{3} \\ 2 x_{1} - x_{2}\end{bmatrix}&=\begin{bmatrix}8 \\ -6 \\ 2\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + x_{3} &=8 \\ x_{2} - 2 x_{3} &=-6 \\ 2 x_{1} - x_{2} &=2\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 0 & 1 & 8 \\ 0 & 1 & -2 & -6 \\ 2 & -1 & 0 & 2\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 0 & 1 & 8 \\ 0 & 1 & -2 & -6 \\ 2 & -1 & 0 & 2\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 0 & 1 & 8 \\ 0 & 1 & -2 & -6 \\ 0 & -1 & -2 & -14\end{array}\right] && R_{3}:=R_{3}+(-2)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 0 & 1 & 8 \\ 0 & 1 & -2 & -6 \\ 0 & 0 & -4 & -20\end{array}\right] && R_{3}:=R_{3}+(1)R_{2} \\ &\sim \left[\begin{array}{ccc|c}1 & 0 & 1 & 8 \\ 0 & 1 & -2 & -6 \\ 0 & 0 & 1 & 5\end{array}\right] && R_{3}:=(- \frac{1}{4})R_{3}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + x_{3} &=8 \\ x_{2} - 2 x_{3} &=-6 \\ x_{3} &=5\end{aligned}\right.
$$

From the third equation, we get $x_3=5.$ Substituting this value into the second equation, we get

$$
1x_2+(-2)(5)=-6\quad\Rightarrow\quad x_2=4
$$

Finally, substituting these values into the first equation, we obtain

$$
x_1+(0)(4)+(1)(5)=8\quad\Rightarrow\quad x_1=3
$$

So, the solution of the system is $x_1=3$, $x_2=4$, $x_3=5$, which means

$$
3a_1+(4)a_2+(5)a_3=b.
$$

Consequently,

$$
x_{1} + x_{2} + x_{3}=(3)+(4)+(5)=12.
$$



### Changed RHS

Consider the vectors

$$
a_1=\begin{bmatrix}1 \\ 0 \\ 2\end{bmatrix},\quad a_2=\begin{bmatrix}0 \\ 1 \\ -1\end{bmatrix},\quad a_3=\begin{bmatrix}1 \\ -2 \\ 0\end{bmatrix},\quad b=\begin{bmatrix}14 \\ -21 \\ 21\end{bmatrix}
$$

If $x_1a_1+x_2a_2+x_3a_3=b,$ then what is $x_{1} + x_{2} + x_{3}?$

If $x_1a_1+x_2a_2+x_3a_3=b$, then we have

$$
\begin{aligned}x_1\begin{bmatrix}1 \\ 0 \\ 2\end{bmatrix}+x_2\begin{bmatrix}0 \\ 1 \\ -1\end{bmatrix}+x_3\begin{bmatrix}1 \\ -2 \\ 0\end{bmatrix}&=\begin{bmatrix}14 \\ -21 \\ 21\end{bmatrix} \\ \begin{bmatrix}x_{1} \\ 0 \\ 2 x_{1}\end{bmatrix}+\begin{bmatrix}0 \\ x_{2} \\ - x_{2}\end{bmatrix}+\begin{bmatrix}x_{3} \\ - 2 x_{3} \\ 0\end{bmatrix}&=\begin{bmatrix}14 \\ -21 \\ 21\end{bmatrix} \\ \begin{bmatrix}x_{1} + x_{3} \\ x_{2} - 2 x_{3} \\ 2 x_{1} - x_{2}\end{bmatrix}&=\begin{bmatrix}14 \\ -21 \\ 21\end{bmatrix}\end{aligned}
$$

Equating the corresponding components, we get the following system:

$$
\left\{\begin{aligned}x_{1} + x_{3} &=14 \\ x_{2} - 2 x_{3} &=-21 \\ 2 x_{1} - x_{2} &=21\end{aligned}\right.
$$

We will solve this system using Gaussian elimination. First, we write the augmented matrix for this system:

$$
M=\left[\begin{array}{ccc|c}1 & 0 & 1 & 14 \\ 0 & 1 & -2 & -21 \\ 2 & -1 & 0 & 21\end{array}\right]
$$

Row-reducing the augmented matrix, we get

$$
\begin{aligned}M&=\left[\begin{array}{ccc|c}1 & 0 & 1 & 14 \\ 0 & 1 & -2 & -21 \\ 2 & -1 & 0 & 21\end{array}\right] \\ &\sim \left[\begin{array}{ccc|c}1 & 0 & 1 & 14 \\ 0 & 1 & -2 & -21 \\ 0 & -1 & -2 & -7\end{array}\right] && R_{3}:=R_{3}+(-2)R_{1} \\ &\sim \left[\begin{array}{ccc|c}1 & 0 & 1 & 14 \\ 0 & 1 & -2 & -21 \\ 0 & 0 & -4 & -28\end{array}\right] && R_{3}:=R_{3}+(1)R_{2} \\ &\sim \left[\begin{array}{ccc|c}1 & 0 & 1 & 14 \\ 0 & 1 & -2 & -21 \\ 0 & 0 & 1 & 7\end{array}\right] && R_{3}:=(- \frac{1}{4})R_{3}\end{aligned}
$$

The system is now

$$
\left\{\begin{aligned}x_{1} + x_{3} &=14 \\ x_{2} - 2 x_{3} &=-21 \\ x_{3} &=7\end{aligned}\right.
$$

From the third equation, we get $x_3=7.$ Substituting this value into the second equation, we get

$$
1x_2+(-2)(7)=-21\quad\Rightarrow\quad x_2=-7
$$

Finally, substituting these values into the first equation, we obtain

$$
x_1+(0)(-7)+(1)(7)=14\quad\Rightarrow\quad x_1=7
$$

So, the solution of the system is $x_1=7$, $x_2=-7$, $x_3=7$, which means

$$
7a_1+(-7)a_2+(7)a_3=b.
$$

Consequently,

$$
x_{1} + x_{2} + x_{3}=(7)+(-7)+(7)=7.
$$

