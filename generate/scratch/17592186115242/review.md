# Source originals and generated review

Raw source solutions below include errors; repaired replays are labeled.


## Raw original q-32246

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 3x+4y=12 \\  & x+ky=4\end{aligned}
$$


- $k=0$
- $k=\frac{4}{3}$
- $k=\frac{3}{4}$
- $k=-4$
- $k=-\frac{4}{3}$

The augmented matrix for this system is

$$
M=[\begin{aligned}3 & 4 & 12 \\ 1 & k & 4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}3 & 4 & 12 \\ 1 & k & 4\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & k & 4 \\ 3 & 4 & 12\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}1 & k & 4 \\ 0 & 4-3k & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x+ky=4 \\  & (4-3k)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=\frac{4}{3},$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=4.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=\frac{4}{3}.$


## Raw original q-42059

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & 2x+3y=1 \\  & 6x+(k+3)y=-5\end{aligned}
$$


- $k=9$
- $k=6$
- $k=4$
- $k=-2$
- $k=7$

The augmented matrix for this system is

$$
M=[\begin{aligned}2 & 3 & 1 \\ 6 & k+3 & -5\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & 3 & 1 \\ 6 & k+3 & -5\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}2 & 3 & 1 \\ 0 & k-6 & -8\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}2x+3y=1 \\ (k-6)y=-8.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=6,$ then the second equation is $0=-8,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=6.$


## Raw original q-131726

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
{\begin{aligned} & -3x+2y=1 \\  & 6x+(k+9)y=5\end{aligned}
$$


- $k=-13$
- $k=8$
- $k=-12$
- $k=7$
- $k=-14$

The augmented matrix for this system is

$$
M=[\begin{aligned}-3 & 2 & 1 \\ 6 & k+9 & 5\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-3 & 2 & 1 \\ 6 & k+9 & 5\end{aligned}] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼[\begin{aligned}-3 & 2 & 1 \\ 0 & k+13 & 7\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
{\begin{aligned}-3x+2y=1 \\ (k+13)y=7.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-13,$ then the second equation is $0=7,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-13.$


## Raw original q-131727

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
{\begin{aligned} & x-3y=-1 \\  & 4x+3ky=3\end{aligned}
$$


- $k=-13$
- $k=7$
- $k=-3$
- $k=-12$
- $k=-4$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -3 & -1 \\ 4 & 3k & 3\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -3 & -1 \\ 4 & 3k & 3\end{aligned}] & {R}_{2} & :={R}_{2}-4{R}_{1} \\  & ∼[\begin{aligned}1 & -3 & -1 \\ 0 & 3k+12 & 7\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
{\begin{aligned}x-3y=-1 \\ (3k+12)y=7.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-4,$ then the second equation is $0=7,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-4.$


## Raw original q-131728

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
{\begin{aligned} & -x+4y=-2 \\  & -3x+(3k+15)y=-4\end{aligned}
$$


- $k=1$
- $k=-1$
- $k=-2$
- $k=0$
- $k=2$

The augmented matrix for this system is

$$
M=[\begin{aligned}-1 & 4 & -2 \\ -3 & 3k+15 & -4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-1 & 4 & -2 \\ -3 & 3k+15 & -4\end{aligned}] & {R}_{2} & :={R}_{2}-3{R}_{1} \\  & ∼[\begin{aligned}-1 & 4 & -2 \\ 0 & 3k+3 & 2\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
{\begin{aligned}-x+4y=-2 \\ (3k+3)y=2.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-1,$ then the second equation is $0=2,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-1.$


## Raw original q-131729

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
{\begin{aligned} & -2x+7y=6 \\  & x+ky=-3\end{aligned}
$$


- $k=-\frac{2}{7}$
- $k=-7$
- $k=\frac{7}{2}$
- $k=-\frac{7}{2}$
- $k=0$

The augmented matrix for this system is

$$
M=[\begin{aligned}-2 & 7 & 6 \\ 1 & k & -3\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-2 & 7 & 6 \\ 1 & k & -3\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & k & -3 \\ -2 & 7 & 6\end{aligned}] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼[\begin{aligned}1 & k & -3 \\ 0 & 2k+7 & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
{\begin{aligned} & x+ky=-3 \\  & (2k+7)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=-\frac{7}{2},$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=-3.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=-\frac{7}{2}.$


## Raw original q-131731

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
{\begin{aligned} & -2x+6y=-4 \\  & 5x+(k-6)y=10\end{aligned}
$$


- $k=-9$
- $k=-6$
- $k=0$
- $k=9$
- $k=-12$

The augmented matrix for this system is 

$$
M=[\begin{aligned}-2 & 6 & -4 \\ 5 & k-6 & 10\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-2 & 6 & -4 \\ 5 & k-6 & 10\end{aligned}] & {R}_{2} & :={R}_{2}+\frac{5}{2}{R}_{1} \\  & ∼[\begin{aligned}-2 & 6 & -4 \\ 0 & k+9 & 0\end{aligned}]\end{aligned}
$$

 

The corresponding system is now 

$$
{\begin{aligned} & -2x+6y=-4 \\  & (k+9)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=-9,$ then the second equation is $0=0,$ which is true for any value of $y.$ So, we can remove this equation from the system. As a result, the system will contain only one equation, $-2x+6y=-4.$  

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=-9.$


## Raw original q-32245

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & 2x-y=3 \\  & 4x+ky=4\end{aligned}
$$


- $k=0$
- $k=-4$
- $k=2$
- $k=-2$
- $k=4$

The augmented matrix for this system is

$$
M=[\begin{aligned}2 & -1 & 3 \\ 4 & k & 4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & -1 & 3 \\ 4 & k & 4\end{aligned}] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼[\begin{aligned}2 & -1 & 3 \\ 0 & k+2 & -2\end{aligned}]\end{aligned}
$$

The corresponding system is now

$$
\{\begin{aligned} & 2x-y=3 \\  & (k+2)y=-2.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

Now if $k=-2$, then the second equation is $0=-2,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when  $k=-2.$


## Raw original q-32331

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
{\begin{aligned}-4x-y=2 \\ 8x+ky=5\end{aligned}
$$


- $k=2$
- $k=0$
- $k=-5$
- $k=-8$
- $k=-2$

The augmented matrix for this system is

$$
M=[\begin{aligned}-4 & -1 & 2 \\ 8 & k & 5\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-4 & -1 & 2 \\ 8 & k & 5\end{aligned}] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼[\begin{aligned}-4 & -1 & 2 \\ 0 & k-2 & 9\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
{\begin{aligned}-4x-y=2 \\ (k-2)y=9.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=2,$ then the second equation is $0=9,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=2.$


## Raw original q-74646

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
{\begin{aligned} & x+4y=2 \\  & 2x+(k+1)y=3\end{aligned}
$$


- $k=5$
- $k=3$
- $k=1$
- $k=9$
- $k=7$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 4 & 2 \\ 2 & k+1 & 3\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 4 & 2 \\ 2 & k+1 & 3\end{aligned}] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼[\begin{aligned}1 & 4 & 2 \\ 0 & k-7 & -1\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
{\begin{aligned}x+4y=2 \\ (k-7)y=-1.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=7,$ then the second equation is $0=-1,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=7.$


## Raw original q-74688

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
{\begin{aligned} & x+2y=-4 \\  & 3x+2ky=-2\end{aligned}
$$


- $k=-2$
- $k=-1$
- $k=-3$
- $k=3$
- $k=2$

The augmented matrix for this system is 

$$
M=[\begin{aligned}1 & 2 & -4 \\ 3 & 2k & -2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 2 & -4 \\ 3 & 2k & -2\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}1 & 2 & -4 \\ 0 & 2k-6 & 10\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
{\begin{aligned}x+2y=-4 \\ (2k-6)y=10.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=3,$ then the second equation is $0=10,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=3.$


## Raw original q-74695

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
{\begin{aligned} & 4x+2y=-8 \\  & x+ky=-2\end{aligned}
$$


- $k=\frac{1}{4}$
- $k=-\frac{1}{4}$
- $k=\frac{1}{2}$
- $k=2$
- $k=\frac{1}{8}$

The augmented matrix for this system is

$$
M=[\begin{aligned}4 & 2 & -8 \\ 1 & k & -2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}4 & 2 & -8 \\ 1 & k & -2\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & k & -2 \\ 4 & 2 & -8\end{aligned}] & {R}_{2} & :={R}_{2}+(-4){R}_{1} \\  & ∼[\begin{aligned}1 & k & -2 \\ 0 & 2-4k & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
{\begin{aligned} & x+ky=2 \\  & (2-4k)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=\frac{1}{2},$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=2.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=\frac{1}{2}.$


## Raw original q-74650

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
{\begin{aligned} & 2x+6y=4 \\  & x+(k+1)y=2\end{aligned}
$$


- $k=\frac{1}{2}$
- $k=-\frac{1}{2}$
- $k=-2$
- $k=2$
- $k=-4$

The augmented matrix for this system is 

$$
M=[\begin{aligned}2 & 6 & 4 \\ 1 & k+1 & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & 6 & 4 \\ 1 & k+1 & 2\end{aligned}] & {R}_{2} & :={R}_{2}+(-\frac{1}{2}){R}_{1} \\  & ∼[\begin{aligned}2 & 6 & 4 \\ 0 & k-2 & 0\end{aligned}]\end{aligned}
$$

 

The corresponding system is now 

$$
{\begin{aligned} & 2x+6y=4 \\  & (k-2)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=2,$ then the second equation is $0=0,$ which is true for any value of $y.$ So, we can remove this equation from the system. As a result, the system will contain only one equation, $2x+6y=4.$  

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=2.$


## Raw original q-131730

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
{\begin{aligned} & 3x+2y=12 \\  & x+ky=4\end{aligned}
$$


- $k=2$
- $k=0$
- $k=\frac{2}{3}$
- $k=-\frac{2}{3}$
- $k=\frac{3}{2}$

The augmented matrix for this system is

$$
M=[\begin{aligned}3 & 2 & 12 \\ 1 & k & 4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}3 & 2 & 12 \\ 1 & k & 4\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & k & 4 \\ 3 & 2 & 12\end{aligned}] & {R}_{2} & :={R}_{2}-3{R}_{1} \\  & ∼[\begin{aligned}1 & k & 4 \\ 0 & 2-3k & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
{\begin{aligned} & x+ky=4 \\  & (2-3k)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=\frac{2}{3},$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=4.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=\frac{2}{3}.$


## Raw original q-42021

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned}x+2y=3 \\ -3x-(k+1)y=-9\end{aligned}
$$


- $k=1$
- $k=-3$
- $k=-5$
- $k=2$
- $k=5$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 2 & -3 \\ -3 & -(k+1) & -9\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 2 & 3 \\ -3 & -(k+1) & -9\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}1 & 2 & 3 \\ 0 & -k+5 & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}1-2y=3 \\ -(k-5)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=5,$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+2y=3.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=5.$


## Observed replay q-32246

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 3x+4y=12 \\  & x+ky=4\end{aligned}
$$

- $k=-4$
- $k=0$
- $k=\frac{3}{4}$
- $k=\frac{4}{3}$
- $k=-\frac{4}{3}$

The augmented matrix for this system is

$$
M=[\begin{aligned}3 & 4 & 12 \\ 1 & k & 4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}3 & 4 & 12 \\ 1 & k & 4\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & k & 4 \\ 3 & 4 & 12\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}1 & k & 4 \\ 0 & 4-3k & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x+ky=4 \\  & (4-3k)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=\frac{4}{3},$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=4.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=\frac{4}{3}.$


## Generated variant of observed profile q-32246

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 2x-6y=8 \\  & x+ky=4\end{aligned}
$$

- $k=3$
- $k=-3$
- $k=0$
- $k=-\frac{1}{3}$
- $k=6$

The augmented matrix for this system is

$$
M=[\begin{aligned}2 & -6 & 8 \\ 1 & k & 4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & -6 & 8 \\ 1 & k & 4\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & k & 4 \\ 2 & -6 & 8\end{aligned}] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼[\begin{aligned}1 & k & 4 \\ 0 & -6-2k & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x+ky=4 \\  & (-6-2k)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=-3,$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=4.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=-3.$


## Observed replay q-42059

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & 2x+3y=1 \\  & 6x+(k+3)y=-5\end{aligned}
$$

- $k=-2$
- $k=9$
- $k=4$
- $k=6$
- $k=7$

The augmented matrix for this system is

$$
M=[\begin{aligned}2 & 3 & 1 \\ 6 & k+3 & -5\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & 3 & 1 \\ 6 & k+3 & -5\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}2 & 3 & 1 \\ 0 & k-6 & -8\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}2x+3y=1 \\ (k-6)y=-8.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=6,$ then the second equation is $0=-8,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=6.$


## Generated variant of observed profile q-42059

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & x+3y=1 \\  & -3x+(k-6)y=2\end{aligned}
$$

- $k=-2$
- $k=-5$
- $k=-9$
- $k=-1$
- $k=-3$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 3 & 1 \\ -3 & k-6 & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 3 & 1 \\ -3 & k-6 & 2\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}1 & 3 & 1 \\ 0 & k+3 & 5\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}x+3y=1 \\ (k+3)y=5.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-3,$ then the second equation is $0=5,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-3.$


## Observed replay q-131726

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & -3x+2y=1 \\  & 6x+(k+9)y=5\end{aligned}
$$

- $k=7$
- $k=-13$
- $k=-12$
- $k=8$
- $k=-14$

The augmented matrix for this system is

$$
M=[\begin{aligned}-3 & 2 & 1 \\ 6 & k+9 & 5\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-3 & 2 & 1 \\ 6 & k+9 & 5\end{aligned}] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼[\begin{aligned}-3 & 2 & 1 \\ 0 & k+13 & 7\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}-3x+2y=1 \\ (k+13)y=7.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-13,$ then the second equation is $0=7,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-13.$


## Generated variant of observed profile q-131726

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & x+3y=1 \\  & -3x+(k-6)y=2\end{aligned}
$$

- $k=-4$
- $k=-2$
- $k=-3$
- $k=5$
- $k=6$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 3 & 1 \\ -3 & k-6 & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 3 & 1 \\ -3 & k-6 & 2\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}1 & 3 & 1 \\ 0 & k+3 & 5\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}x+3y=1 \\ (k+3)y=5.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-3,$ then the second equation is $0=5,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-3.$


## Observed replay q-131727

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & x-3y=-1 \\  & 4x+3ky=3\end{aligned}
$$

- $k=-12$
- $k=-13$
- $k=-3$
- $k=7$
- $k=-4$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -3 & -1 \\ 4 & 3k & 3\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -3 & -1 \\ 4 & 3k & 3\end{aligned}] & {R}_{2} & :={R}_{2}-4{R}_{1} \\  & ∼[\begin{aligned}1 & -3 & -1 \\ 0 & 3k+12 & 7\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}x-3y=-1 \\ (3k+12)y=7.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-4,$ then the second equation is $0=7,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-4.$


## Generated variant of observed profile q-131727

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & x+3y=1 \\  & -3x+2ky=2\end{aligned}
$$

- $k=-\frac{9}{2}$
- $k=-\frac{7}{2}$
- $k=-\frac{27}{2}$
- $k=-9$
- $k=5$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 3 & 1 \\ -3 & 2k & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 3 & 1 \\ -3 & 2k & 2\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}1 & 3 & 1 \\ 0 & 2k+9 & 5\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}x+3y=1 \\ (2k+9)y=5.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-\frac{9}{2},$ then the second equation is $0=5,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-\frac{9}{2}.$


## Observed replay q-131728

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & -x+4y=-2 \\  & -3x+(3k+15)y=-4\end{aligned}
$$

- $k=0$
- $k=1$
- $k=-2$
- $k=-1$
- $k=2$

The augmented matrix for this system is

$$
M=[\begin{aligned}-1 & 4 & -2 \\ -3 & 3k+15 & -4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-1 & 4 & -2 \\ -3 & 3k+15 & -4\end{aligned}] & {R}_{2} & :={R}_{2}-3{R}_{1} \\  & ∼[\begin{aligned}-1 & 4 & -2 \\ 0 & 3k+3 & 2\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}-x+4y=-2 \\ (3k+3)y=2.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-1,$ then the second equation is $0=2,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-1.$


## Generated variant of observed profile q-131728

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & 2x-2y=-1 \\  & 6x+(2k+3)y=5\end{aligned}
$$

- $k=\frac{9}{2}$
- $k=9$
- $k=-\frac{11}{2}$
- $k=-\frac{9}{2}$
- $k=0$

The augmented matrix for this system is

$$
M=[\begin{aligned}2 & -2 & -1 \\ 6 & 2k+3 & 5\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & -2 & -1 \\ 6 & 2k+3 & 5\end{aligned}] & {R}_{2} & :={R}_{2}-3{R}_{1} \\  & ∼[\begin{aligned}2 & -2 & -1 \\ 0 & 2k+9 & 8\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}2x-2y=-1 \\ (2k+9)y=8.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-\frac{9}{2},$ then the second equation is $0=8,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-\frac{9}{2}.$


## Observed replay q-131729

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & -2x+7y=6 \\  & x+ky=-3\end{aligned}
$$

- $k=-\frac{7}{2}$
- $k=-\frac{2}{7}$
- $k=\frac{7}{2}$
- $k=-7$
- $k=0$

The augmented matrix for this system is

$$
M=[\begin{aligned}-2 & 7 & 6 \\ 1 & k & -3\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-2 & 7 & 6 \\ 1 & k & -3\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & k & -3 \\ -2 & 7 & 6\end{aligned}] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼[\begin{aligned}1 & k & -3 \\ 0 & 2k+7 & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x+ky=-3 \\  & (2k+7)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=-\frac{7}{2},$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=-3.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=-\frac{7}{2}.$


## Generated variant of observed profile q-131729

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 2x-6y=8 \\  & x+ky=4\end{aligned}
$$

- $k=0$
- $k=6$
- $k=-\frac{1}{3}$
- $k=3$
- $k=-3$

The augmented matrix for this system is

$$
M=[\begin{aligned}2 & -6 & 8 \\ 1 & k & 4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & -6 & 8 \\ 1 & k & 4\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & k & 4 \\ 2 & -6 & 8\end{aligned}] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼[\begin{aligned}1 & k & 4 \\ 0 & -6-2k & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x+ky=4 \\  & (-6-2k)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=-3,$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=4.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=-3.$


## Observed replay q-131731

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & -2x+6y=-4 \\  & 5x+(k-6)y=10\end{aligned}
$$

- $k=9$
- $k=-9$
- $k=0$
- $k=-6$
- $k=-12$

The augmented matrix for this system is 

$$
M=[\begin{aligned}-2 & 6 & -4 \\ 5 & k-6 & 10\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-2 & 6 & -4 \\ 5 & k-6 & 10\end{aligned}] & {R}_{2} & :={R}_{2}+\frac{5}{2}{R}_{1} \\  & ∼[\begin{aligned}-2 & 6 & -4 \\ 0 & k+9 & 0\end{aligned}]\end{aligned}
$$

 

The corresponding system is now 

$$
\{\begin{aligned} & -2x+6y=-4 \\  & (k+9)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=-9,$ then the second equation is $0=0,$ which is true for any value of $y.$ So, we can remove this equation from the system. As a result, the system will contain only one equation, $-2x+6y=-4.$  

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=-9.$


## Generated variant of observed profile q-131731

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 2x+2y=-6 \\  & 5x+(k-1)y=-15\end{aligned}
$$

- $k=0$
- $k=-1$
- $k=3$
- $k=-6$
- $k=6$

The augmented matrix for this system is 

$$
M=[\begin{aligned}2 & 2 & -6 \\ 5 & k-1 & -15\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & 2 & -6 \\ 5 & k-1 & -15\end{aligned}] & {R}_{2} & :={R}_{2}-\frac{5}{2}{R}_{1} \\  & ∼[\begin{aligned}2 & 2 & -6 \\ 0 & k-6 & 0\end{aligned}]\end{aligned}
$$

 

The corresponding system is now 

$$
\{\begin{aligned} & 2x+2y=-6 \\  & (k-6)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=6,$ then the second equation is $0=0,$ which is true for any value of $y.$ So, we can remove this equation from the system. As a result, the system will contain only one equation, $2x+2y=-6.$  

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=6.$


## Observed replay q-32245

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & 2x-y=3 \\  & 4x+ky=4\end{aligned}
$$

- $k=-2$
- $k=0$
- $k=2$
- $k=-4$
- $k=4$

The augmented matrix for this system is

$$
M=[\begin{aligned}2 & -1 & 3 \\ 4 & k & 4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & -1 & 3 \\ 4 & k & 4\end{aligned}] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼[\begin{aligned}2 & -1 & 3 \\ 0 & k+2 & -2\end{aligned}]\end{aligned}
$$

The corresponding system is now

$$
\{\begin{aligned} & 2x-y=3 \\  & (k+2)y=-2.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

Now if $k=-2$, then the second equation is $0=-2,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when  $k=-2.$


## Generated variant of observed profile q-32245

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & 3x+3y=1 \\  & -9x+ky=-4\end{aligned}
$$

- $k=0$
- $k=18$
- $k=9$
- $k=-18$
- $k=-9$

The augmented matrix for this system is

$$
M=[\begin{aligned}3 & 3 & 1 \\ -9 & k & -4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}3 & 3 & 1 \\ -9 & k & -4\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}3 & 3 & 1 \\ 0 & k+9 & -1\end{aligned}]\end{aligned}
$$

The corresponding system is now

$$
\{\begin{aligned} & 3x+3y=1 \\  & (k+9)y=-1.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

Now if $k=-9$, then the second equation is $0=-1,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when  $k=-9.$


## Observed replay q-32331

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned}-4x-y=2 \\ 8x+ky=5\end{aligned}
$$

- $k=-8$
- $k=2$
- $k=-5$
- $k=0$
- $k=-2$

The augmented matrix for this system is

$$
M=[\begin{aligned}-4 & -1 & 2 \\ 8 & k & 5\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-4 & -1 & 2 \\ 8 & k & 5\end{aligned}] & {R}_{2} & :={R}_{2}+2{R}_{1} \\  & ∼[\begin{aligned}-4 & -1 & 2 \\ 0 & k-2 & 9\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}-4x-y=2 \\ (k-2)y=9.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=2,$ then the second equation is $0=9,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=2.$


## Generated variant of observed profile q-32331

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned}-2x+4y=-1 \\ -4x+ky=5\end{aligned}
$$

- $k=-8$
- $k=8$
- $k=4$
- $k=0$
- $k=-5$

The augmented matrix for this system is

$$
M=[\begin{aligned}-2 & 4 & -1 \\ -4 & k & 5\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-2 & 4 & -1 \\ -4 & k & 5\end{aligned}] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼[\begin{aligned}-2 & 4 & -1 \\ 0 & k-8 & 7\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}-2x+4y=-1 \\ (k-8)y=7.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=8,$ then the second equation is $0=7,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=8.$


## Observed replay q-74646

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & x+4y=2 \\  & 2x+(k+1)y=3\end{aligned}
$$

- $k=9$
- $k=5$
- $k=1$
- $k=3$
- $k=7$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 4 & 2 \\ 2 & k+1 & 3\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 4 & 2 \\ 2 & k+1 & 3\end{aligned}] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼[\begin{aligned}1 & 4 & 2 \\ 0 & k-7 & -1\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}x+4y=2 \\ (k-7)y=-1.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=7,$ then the second equation is $0=-1,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=7.$


## Generated variant of observed profile q-74646

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & x+3y=1 \\  & -3x+(k-6)y=2\end{aligned}
$$

- $k=-3$
- $k=-6$
- $k=-5$
- $k=-1$
- $k=2$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 3 & 1 \\ -3 & k-6 & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 3 & 1 \\ -3 & k-6 & 2\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}1 & 3 & 1 \\ 0 & k+3 & 5\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}x+3y=1 \\ (k+3)y=5.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-3,$ then the second equation is $0=5,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-3.$


## Observed replay q-74688

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & x+2y=-4 \\  & 3x+2ky=-2\end{aligned}
$$

- $k=3$
- $k=-2$
- $k=-3$
- $k=-1$
- $k=2$

The augmented matrix for this system is 

$$
M=[\begin{aligned}1 & 2 & -4 \\ 3 & 2k & -2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 2 & -4 \\ 3 & 2k & -2\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}1 & 2 & -4 \\ 0 & 2k-6 & 10\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}x+2y=-4 \\ (2k-6)y=10.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=3,$ then the second equation is $0=10,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=3.$


## Generated variant of observed profile q-74688

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & x+3y=1 \\  & -3x+2ky=2\end{aligned}
$$

- $k=2$
- $k=\frac{9}{2}$
- $k=-2$
- $k=-\frac{9}{2}$
- $k=-1$

The augmented matrix for this system is 

$$
M=[\begin{aligned}1 & 3 & 1 \\ -3 & 2k & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 3 & 1 \\ -3 & 2k & 2\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}1 & 3 & 1 \\ 0 & 2k+9 & 5\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}x+3y=1 \\ (2k+9)y=5.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-\frac{9}{2},$ then the second equation is $0=5,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-\frac{9}{2}.$


## Observed replay q-74695

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 4x+2y=-8 \\  & x+ky=-2\end{aligned}
$$

- $k=2$
- $k=\frac{1}{4}$
- $k=\frac{1}{2}$
- $k=-\frac{1}{4}$
- $k=\frac{1}{8}$

The augmented matrix for this system is

$$
M=[\begin{aligned}4 & 2 & -8 \\ 1 & k & -2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}4 & 2 & -8 \\ 1 & k & -2\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & k & -2 \\ 4 & 2 & -8\end{aligned}] & {R}_{2} & :={R}_{2}+(-4){R}_{1} \\  & ∼[\begin{aligned}1 & k & -2 \\ 0 & 2-4k & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x+ky=-2 \\  & (2-4k)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=\frac{1}{2},$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=-2.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=\frac{1}{2}.$


## Generated variant of observed profile q-74695

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 2x-6y=8 \\  & x+ky=4\end{aligned}
$$

- $k=-\frac{3}{4}$
- $k=\frac{3}{2}$
- $k=-\frac{3}{2}$
- $k=-3$
- $k=-\frac{1}{3}$

The augmented matrix for this system is

$$
M=[\begin{aligned}2 & -6 & 8 \\ 1 & k & 4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & -6 & 8 \\ 1 & k & 4\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & k & 4 \\ 2 & -6 & 8\end{aligned}] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼[\begin{aligned}1 & k & 4 \\ 0 & -6-2k & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x+ky=4 \\  & (-6-2k)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=-3,$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=4.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=-3.$


## Observed replay q-74650

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 2x+6y=4 \\  & x+(k+1)y=2\end{aligned}
$$

- $k=2$
- $k=\frac{1}{2}$
- $k=-2$
- $k=-\frac{1}{2}$
- $k=-4$

The augmented matrix for this system is 

$$
M=[\begin{aligned}2 & 6 & 4 \\ 1 & k+1 & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & 6 & 4 \\ 1 & k+1 & 2\end{aligned}] & {R}_{2} & :={R}_{2}+(-\frac{1}{2}){R}_{1} \\  & ∼[\begin{aligned}2 & 6 & 4 \\ 0 & k-2 & 0\end{aligned}]\end{aligned}
$$

 

The corresponding system is now 

$$
\{\begin{aligned} & 2x+6y=4 \\  & (k-2)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=2,$ then the second equation is $0=0,$ which is true for any value of $y.$ So, we can remove this equation from the system. As a result, the system will contain only one equation, $2x+6y=4.$  

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=2.$


## Generated variant of observed profile q-74650

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 2x+2y=-6 \\  & 5x+(k-1)y=-15\end{aligned}
$$

- $k=-6$
- $k=-\frac{1}{6}$
- $k=-12$
- $k=6$
- $k=\frac{1}{6}$

The augmented matrix for this system is 

$$
M=[\begin{aligned}2 & 2 & -6 \\ 5 & k-1 & -15\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & 2 & -6 \\ 5 & k-1 & -15\end{aligned}] & {R}_{2} & :={R}_{2}+(-\frac{5}{2}){R}_{1} \\  & ∼[\begin{aligned}2 & 2 & -6 \\ 0 & k-6 & 0\end{aligned}]\end{aligned}
$$

 

The corresponding system is now 

$$
\{\begin{aligned} & 2x+2y=-6 \\  & (k-6)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=6,$ then the second equation is $0=0,$ which is true for any value of $y.$ So, we can remove this equation from the system. As a result, the system will contain only one equation, $2x+2y=-6.$  

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=6.$


## Observed replay q-131730

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 3x+2y=12 \\  & x+ky=4\end{aligned}
$$

- $k=-\frac{2}{3}$
- $k=2$
- $k=\frac{2}{3}$
- $k=0$
- $k=\frac{3}{2}$

The augmented matrix for this system is

$$
M=[\begin{aligned}3 & 2 & 12 \\ 1 & k & 4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}3 & 2 & 12 \\ 1 & k & 4\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & k & 4 \\ 3 & 2 & 12\end{aligned}] & {R}_{2} & :={R}_{2}-3{R}_{1} \\  & ∼[\begin{aligned}1 & k & 4 \\ 0 & 2-3k & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x+ky=4 \\  & (2-3k)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=\frac{2}{3},$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=4.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=\frac{2}{3}.$


## Generated variant of observed profile q-131730

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 2x-6y=8 \\  & x+ky=4\end{aligned}
$$

- $k=-\frac{1}{3}$
- $k=0$
- $k=-6$
- $k=-3$
- $k=3$

The augmented matrix for this system is

$$
M=[\begin{aligned}2 & -6 & 8 \\ 1 & k & 4\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & -6 & 8 \\ 1 & k & 4\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & k & 4 \\ 2 & -6 & 8\end{aligned}] & {R}_{2} & :={R}_{2}-2{R}_{1} \\  & ∼[\begin{aligned}1 & k & 4 \\ 0 & -6-2k & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x+ky=4 \\  & (-6-2k)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=-3,$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=4.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=-3.$


## Observed replay q-42021

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned}x+2y=3 \\ -3x-(k+1)y=-9\end{aligned}
$$

- $k=2$
- $k=1$
- $k=-5$
- $k=-3$
- $k=5$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 2 & 3 \\ -3 & -(k+1) & -9\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 2 & 3 \\ -3 & -(k+1) & -9\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}1 & 2 & 3 \\ 0 & -k+5 & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}x+2y=3 \\ -(k-5)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=5,$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+2y=3.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=5.$


## Generated variant of observed profile q-42021

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned}x-3y=3 \\ -4x-(k+1)y=-12\end{aligned}
$$

- $k=-3$
- $k=1$
- $k=13$
- $k=-13$
- $k=-4$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -3 & 3 \\ -4 & -(k+1) & -12\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -3 & 3 \\ -4 & -(k+1) & -12\end{aligned}] & {R}_{2} & :={R}_{2}+4{R}_{1} \\  & ∼[\begin{aligned}1 & -3 & 3 \\ 0 & -k-13 & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned}x-3y=3 \\ -(k+13)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=-13,$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x-3y=3.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=-13.$


## Authored default easy inconsistent_easy

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & x+2y=1 \\  & -3x+ky=0\end{aligned}
$$

- $k=-6$
- $k=2$
- $k=6$
- $k=-2$
- $k=0$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & 2 & 1 \\ -3 & k & 0\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & 2 & 1 \\ -3 & k & 0\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}1 & 2 & 1 \\ 0 & k+6 & 3\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x+2y=1 \\  & (k+6)y=3.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-6,$ then the second equation is $0=3,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-6.$


## Authored default easy inconsistent_easy

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & x-3y=4 \\  & -3x+ky=0\end{aligned}
$$

- $k=0$
- $k=-3$
- $k=-9$
- $k=3$
- $k=9$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -3 & 4 \\ -3 & k & 0\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -3 & 4 \\ -3 & k & 0\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}1 & -3 & 4 \\ 0 & k-9 & 12\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x-3y=4 \\  & (k-9)y=12.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=9,$ then the second equation is $0=12,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=9.$


## Authored default moderate inconsistent_bare

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & 3x-4y=0 \\  & 9x+ky=3\end{aligned}
$$

- $k=-12$
- $k=-4$
- $k=12$
- $k=0$
- $k=4$

The augmented matrix for this system is

$$
M=[\begin{aligned}3 & -4 & 0 \\ 9 & k & 3\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}3 & -4 & 0 \\ 9 & k & 3\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}3 & -4 & 0 \\ 0 & k+12 & 3\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & 3x-4y=0 \\  & (k+12)y=3.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-12,$ then the second equation is $0=3,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-12.$


## Authored default moderate inconsistent_bare

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & -2x+y=-3 \\  & 6x+ky=2\end{aligned}
$$

- $k=-3$
- $k=3$
- $k=1$
- $k=0$
- $k=-1$

The augmented matrix for this system is

$$
M=[\begin{aligned}-2 & 1 & -3 \\ 6 & k & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-2 & 1 & -3 \\ 6 & k & 2\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}-2 & 1 & -3 \\ 0 & k+3 & -7\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & -2x+y=-3 \\  & (k+3)y=-7.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-3,$ then the second equation is $0=-7,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-3.$


## Authored default moderate inconsistent_shift

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & x-4y=0 \\  & 3x+(k+9)y=1\end{aligned}
$$

- $k=-3$
- $k=-21$
- $k=21$
- $k=-9$
- $k=-12$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -4 & 0 \\ 3 & k+9 & 1\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -4 & 0 \\ 3 & k+9 & 1\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}1 & -4 & 0 \\ 0 & k+21 & 1\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x-4y=0 \\  & (k+21)y=1.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-21,$ then the second equation is $0=1,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-21.$


## Authored default moderate inconsistent_shift

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & -2x+y=-3 \\  & 6x+(k+9)y=2\end{aligned}
$$

- $k=12$
- $k=-3$
- $k=-12$
- $k=6$
- $k=-9$

The augmented matrix for this system is

$$
M=[\begin{aligned}-2 & 1 & -3 \\ 6 & k+9 & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-2 & 1 & -3 \\ 6 & k+9 & 2\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}-2 & 1 & -3 \\ 0 & k+12 & -7\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & -2x+y=-3 \\  & (k+12)y=-7.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-12,$ then the second equation is $0=-7,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-12.$


## Authored default moderate inconsistent_scaled

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & x-4y=0 \\  & 3x+3ky=1\end{aligned}
$$

- $k=0$
- $k=-4$
- $k=4$
- $k=\frac{4}{3}$
- $k=-\frac{4}{3}$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -4 & 0 \\ 3 & 3k & 1\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -4 & 0 \\ 3 & 3k & 1\end{aligned}] & {R}_{2} & :={R}_{2}+(-3){R}_{1} \\  & ∼[\begin{aligned}1 & -4 & 0 \\ 0 & 3k+12 & 1\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x-4y=0 \\  & (3k+12)y=1.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-4,$ then the second equation is $0=1,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-4.$


## Authored default moderate inconsistent_scaled

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & -2x+y=-3 \\  & 6x+3ky=2\end{aligned}
$$

- $k=1$
- $k=\frac{1}{3}$
- $k=-1$
- $k=0$
- $k=-\frac{1}{3}$

The augmented matrix for this system is

$$
M=[\begin{aligned}-2 & 1 & -3 \\ 6 & 3k & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-2 & 1 & -3 \\ 6 & 3k & 2\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}-2 & 1 & -3 \\ 0 & 3k+3 & -7\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & -2x+y=-3 \\  & (3k+3)y=-7.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-1,$ then the second equation is $0=-7,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-1.$


## Authored default moderate inconsistent_scaled_shift

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & -3x-2y=0 \\  & -6x+(2k-6)y=5\end{aligned}
$$

- $k=-1$
- $k=1$
- $k=-5$
- $k=3$
- $k=-2$

The augmented matrix for this system is

$$
M=[\begin{aligned}-3 & -2 & 0 \\ -6 & 2k-6 & 5\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-3 & -2 & 0 \\ -6 & 2k-6 & 5\end{aligned}] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼[\begin{aligned}-3 & -2 & 0 \\ 0 & 2k-2 & 5\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & -3x-2y=0 \\  & (2k-2)y=5.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=1,$ then the second equation is $0=5,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=1.$


## Authored default moderate inconsistent_scaled_shift

Determine the value of $k$ for which the following system of linear equations is inconsistent:

$$
\{\begin{aligned} & -2x+y=-3 \\  & 6x+(3k+9)y=2\end{aligned}
$$

- $k=-1$
- $k=2$
- $k=-4$
- $k=4$
- $k=-3$

The augmented matrix for this system is

$$
M=[\begin{aligned}-2 & 1 & -3 \\ 6 & 3k+9 & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-2 & 1 & -3 \\ 6 & 3k+9 & 2\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}-2 & 1 & -3 \\ 0 & 3k+12 & -7\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & -2x+y=-3 \\  & (3k+12)y=-7.\end{aligned}
$$

The system is inconsistent if it has no solutions. For the system to have no solutions, one of the equations above must be false.

If $k=-4,$ then the second equation is $0=-7,$ which is false, and the system will have no solution.

Therefore, our system is inconsistent when $k=-4.$


## Authored default hard dependent_swap

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 2x-7y=4 \\  & x+ky=2\end{aligned}
$$

- $k=-\frac{7}{2}$
- $k=0$
- $k=\frac{7}{2}$
- $k=-7$
- $k=-\frac{2}{7}$

The augmented matrix for this system is

$$
M=[\begin{aligned}2 & -7 & 4 \\ 1 & k & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & -7 & 4 \\ 1 & k & 2\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & k & 2 \\ 2 & -7 & 4\end{aligned}] & {R}_{2} & :={R}_{2}+(-2){R}_{1} \\  & ∼[\begin{aligned}1 & k & 2 \\ 0 & -7-2k & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x+ky=2 \\  & (-7-2k)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=-\frac{7}{2},$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=2.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=-\frac{7}{2}.$


## Authored default hard dependent_swap

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & -3x-6y=-9 \\  & x+ky=3\end{aligned}
$$

- $k=-6$
- $k=0$
- $k=-2$
- $k=2$
- $k=\frac{1}{2}$

The augmented matrix for this system is

$$
M=[\begin{aligned}-3 & -6 & -9 \\ 1 & k & 3\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}-3 & -6 & -9 \\ 1 & k & 3\end{aligned}] & {R}_{1} & ↔{R}_{2} \\  & ∼[\begin{aligned}1 & k & 3 \\ -3 & -6 & -9\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}1 & k & 3 \\ 0 & 3k-6 & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x+ky=3 \\  & (3k-6)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=2,$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x+ky=3.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=2.$


## Authored default hard dependent_fractional

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 2x-2y=-6 \\  & x+(k+3)y=-3\end{aligned}
$$

- $k=-4$
- $k=-3$
- $k=4$
- $k=0$
- $k=-5$

The augmented matrix for this system is

$$
M=[\begin{aligned}2 & -2 & -6 \\ 1 & k+3 & -3\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & -2 & -6 \\ 1 & k+3 & -3\end{aligned}] & {R}_{2} & :={R}_{2}+(-\frac{1}{2}){R}_{1} \\  & ∼[\begin{aligned}2 & -2 & -6 \\ 0 & k+4 & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & 2x-2y=-6 \\  & (k+4)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=-4,$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $2x-2y=-6.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=-4.$


## Authored default hard dependent_fractional

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & 2x+6y=4 \\  & x+(k+1)y=2\end{aligned}
$$

- $k=-1$
- $k=5$
- $k=0$
- $k=2$
- $k=-2$

The augmented matrix for this system is

$$
M=[\begin{aligned}2 & 6 & 4 \\ 1 & k+1 & 2\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}2 & 6 & 4 \\ 1 & k+1 & 2\end{aligned}] & {R}_{2} & :={R}_{2}+(-\frac{1}{2}){R}_{1} \\  & ∼[\begin{aligned}2 & 6 & 4 \\ 0 & k-2 & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & 2x+6y=4 \\  & (k-2)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=2,$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $2x+6y=4.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=2.$


## Authored default hard dependent_negative

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & x-4y=3 \\  & -3x-(k+2)y=-9\end{aligned}
$$

- $k=-14$
- $k=-2$
- $k=14$
- $k=2$
- $k=0$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -4 & 3 \\ -3 & -(k+2) & -9\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -4 & 3 \\ -3 & -(k+2) & -9\end{aligned}] & {R}_{2} & :={R}_{2}+3{R}_{1} \\  & ∼[\begin{aligned}1 & -4 & 3 \\ 0 & -k-14 & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x-4y=3 \\  & -(k+14)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=-14,$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x-4y=3.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=-14.$


## Authored default hard dependent_negative

Determine the value of $k$ for which the following system of linear equations is consistent dependent:

$$
\{\begin{aligned} & x-4y=4 \\  & -4x-(k+2)y=-16\end{aligned}
$$

- $k=0$
- $k=-2$
- $k=18$
- $k=2$
- $k=-18$

The augmented matrix for this system is

$$
M=[\begin{aligned}1 & -4 & 4 \\ -4 & -(k+2) & -16\end{aligned}].
$$

Using the method of Gaussian elimination, we can reduce this matrix to row echelon form, as follows:

$$
\begin{aligned}M & =[\begin{aligned}1 & -4 & 4 \\ -4 & -(k+2) & -16\end{aligned}] & {R}_{2} & :={R}_{2}+4{R}_{1} \\  & ∼[\begin{aligned}1 & -4 & 4 \\ 0 & -k-18 & 0\end{aligned}]\end{aligned}
$$

The corresponding system is now 

$$
\{\begin{aligned} & x-4y=4 \\  & -(k+18)y=0.\end{aligned}
$$

The system is consistent dependent if it has infinitely many solutions. For the system to have infinitely many solutions, it must have at least one free variable.

If $k=-18,$ then the second equation is $0=0,$ which is true for any value of $y$, and we can remove this equation from the system. As a result, the system will contain only one equation, $x-4y=4.$ 

Then, the basic variable will be $x,$ and we will have a free variable $y.$ That means the system will have infinitely many solutions.

Therefore, our system is consistent dependent when $k=-18.$
