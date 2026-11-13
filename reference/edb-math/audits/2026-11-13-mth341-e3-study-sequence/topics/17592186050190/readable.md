# 17592186050190 Solving Systems of Linear Equations Using Elimination: One Transformation

Lesson API basis 14416; practice API basis 14416; graph/progress basis 14416.

## Lesson content

### tutorial 17592186193941 — Introduction

Suppose we want to solve the following system of linear equations using the elimination method:

$$
\left\{\begin{aligned}x+2y &=1 \\ x-y &=-2\end{aligned}\right.
$$

As it stands, adding the two equations will not eliminate any of the variables. 

However, suppose we want to eliminate the variable $x$. We begin by multiplying the second equation by $\color{blue}-1$, which gives the following equivalent system:



$$
\left\{\begin{aligned}\phantom{\,(}x+2y &=1 \\ {\color{blue}(\,}x-y &=-2{\color{blue}\,)}{\color{blue}\:\times (-1)}\end{aligned}\right. \qquad\Longrightarrow\qquad \left\{\begin{aligned}x+2y &=1 \\ {\color{blue}-x+y} &{\color{blue}{}=2}\end{aligned}\right.
$$



Then, we add the two resulting equations together. This will eliminate the variable $x,$ allowing us to solve for $y\mathbin{:}$

$$
\begin{aligned}\begin{array}{rl}\cancel{x}+2y & =1 \\ -\cancel{x}+y & =2 \\ \hline (2y+y) & =(1+2) \\ 3y & =3 \\ y & =1\end{array}\end{aligned}
$$

So, the solution must have $y=1.$ However, we still need to find $x.$ To do this, we substitute $y=1$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}\begin{aligned}x-y & =-2 \\ x-(1) & =-2 \\ x & =-1\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-1$ and $y=1,$ which can be expressed as $(-1, 1).$



### example 17592186192585 — Eliminating the First Variable

Consider the following system of equations. 

$$
\left\{\begin{aligned}a+4b &=1 \\ 2a+b &=-5\end{aligned}\right.
$$

Describe the steps needed to eliminate the variable $a$ from this system by filling in the missing information below.

$\qquad$ *To eliminate $a,$ multiply the $\,\textbf{__________}\,$equation by $\,\textbf{______}\,$, 
and add the equations.*

Notice that the coefficient of $a$ in the first equation is $1,$ while in the second equation it is $2.$ 

If we multiply the first equation by ${\color{blue}-2},$ then the coefficient of $a$ will turn into $-2,$ which will cancel with the coefficient of $2$ in the second equation.



$$
\left\{\begin{aligned}{\color{blue}(\,}a+4b &=1{\color{blue}\,)}{\color{blue}\:\times (-2)} \\ 2a+b &=-5\end{aligned}\right. \qquad\Longrightarrow\qquad \left\{\begin{aligned}{\color{blue}-2a-8b} &{\color{blue}{}=-2} \\ 2a+b &=-5\end{aligned}\right.
$$



Now, when we add the two equations, the variable $a$ will be eliminated:

$$
\begin{aligned}\begin{array}{rl}\cancel{-2a}-8b & =-2 \\ \cancel{2a}+b & =-5 \\ \hline (-8b+b) & =(-2-5) \\ -7b & =-7\end{array}\end{aligned}
$$

Therefore, the correct answer is the following:

*To eliminate $a,$ multiply the $\bbox[3pt,Gainsboro]{\color{blue}\text{first}}$ equation by $\bbox[3pt,Gainsboro]{\color{blue}-2},$ and add the equations*.

### example 17592186192586 — Eliminating the Second Variable

Consider the following system of equations.

$$
\left\{\begin{aligned}3x+4y &=2 \\ x-2y &=4\end{aligned}\right.
$$

Describe the steps needed to eliminate the variable $y$ from this system by filling in the missing information below.

$\qquad$ *To eliminate $y,$ multiply the $\,\textbf{__________}\,$equation by $\,\textbf{______}\,$, 
and add the equations.*

Notice that the coefficient of $y$ in the first equation is $4,$ while in the second equation it is $-2.$ 

If we multiply the second equation by ${\color{blue}2},$ then the coefficient of $y$ will turn into $-4,$ which will cancel with the coefficient of $4$ in the first equation.



$$
\left\{\begin{aligned}\phantom{\,(}3x+4y &=2 \\ {\color{blue}(}\,x-2y &=4\,{\color{blue})}\:{\color{blue}\times (2)}\end{aligned}\right. \qquad\Longrightarrow\qquad \left\{\begin{aligned}3x+4y &=2 \\ {\color{blue}2x-4y} &{\color{blue}{}=8}\end{aligned}\right.
$$



Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{array}{rl}3x+\cancel{4y} & =2 \\ 2x-\cancel{4y} & =8 \\ \hline (3x+2x) & =(2+8) \\ 5x & =10\end{array}
$$

Therefore, the correct answer is the following:

*To eliminate $y,$ multiply the $\bbox[3pt,Gainsboro]{\color{blue}\text{second}}$ equation by $\bbox[3pt,Gainsboro]{\color{blue}2},$ and add the equations*.

### example 17592186192587 — Solving a System of Equations by Eliminating the First Variable

Find the solution $(x,y)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}2x+3y &=8 \\ x-2y &=-3\end{aligned}\right.
$$

Notice that the coefficient of $x$ in the first equation is $2,$ while in the second equation it is $1.$

If we multiply the second equation by $-2,$ then the $x$-coefficient will become $-2,$ which will cancel with the coefficient of $2$ in the first equation.


$$
\left\{\begin{aligned}\phantom{\,(}2x+3y &=8 \\ (\,x-2y &=-3\,)\:\times (-2)\end{aligned}\right. \qquad\Longrightarrow\qquad \left\{\begin{aligned}2x+3y &=8 \\ -2x+4y &=6\end{aligned}\right.
$$



Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}\begin{array}{rl}\cancel{2x}+3y & =8 \\ \cancel{-2x}+4y & =6 \\ \hline (3y+4y) & =(8+6) \\ 7y & =14 \\ y & =2\end{array}\end{aligned}
$$

So, the solution must have $y = 2.$ However, we still need to find $x.$ To do this, we substitute $y = 2$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}\begin{aligned}x-2y & =-3 \\ x-2(2) & =-3 \\ x-4 & =-3 \\ x & =1\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $x=1, \,y=2,$ which can be expressed as $(1,2).$

### example 17592186192588 — Solving a System of Equations by Eliminating the Second Variable

Find the solution $(u,v)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}5u-6v &=3 \\ -3u+2v &=-5\end{aligned}\right.
$$

Notice that the $v$-coefficient in the first equation is $-6,$ while in the second equation it is $2.$ 

If we multiply the second equation by $3,$ then the $v$-coefficient will become $6,$ which will cancel with the coefficient of $-6$ in the first equation.


$$
\left\{\begin{aligned}5u-6v &=3 \\ (\,-3u+2v &=-5\,)\:\times (3)\end{aligned}\right. \qquad\Longrightarrow\qquad \left\{\begin{aligned}5u-6v &=3 \\ -9u+6v &=-15\end{aligned}\right.
$$



Now, when we add the two equations, the variable $v$ will be eliminated:

$$
\begin{aligned}\begin{array}{rl}5u-\cancel{6v} & =3 \\ -9u+\cancel{6v} & =-15 \\ \hline (5u-9u) & =(3-15) \\ -4u & =-12 \\ u & =3\end{array}\end{aligned}
$$

So, the solution must have $u = 3.$ However, we still need to find $v.$ To do this, we substitute $u = 3$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}-3u+2v & =-5 \\ -3(3)+2v & =-5 \\ -9+2v & =-5 \\ 2v & =4 \\ v & =2\end{aligned}
$$

Therefore, the solution to the system of equations is $u = 3, \,v = 2,$ which can be expressed as $(3,2).$

## Representative practice (first three per skill; full bank in practice.json)

### Eliminating the First Variable (25 captured questions)

Question 17592186193241 — None

Consider the following system of equations.
$$
\displaystyle \left\{\begin{aligned}x - y &=1 \\ - 7x + 5y &=9\end{aligned}\right.
$$
Describe the steps needed to eliminate the variable $x$ from the system:

To eliminate $x$, multiply the
{{field-1}}
equation by
{{field-2}},
and add the equations.

Solution: 

Question 17592186193242 — question.difficulty/moderate

Consider the following system of equations. 

$$
\left\{\begin{aligned}3s+4t &=8 \\ s+5t &=10\end{aligned}\right.
$$

Describe the steps needed to eliminate the variable $s$ from the system:

To eliminate $s,$ multiply the 
{{field-1}} 
equation by 
{{field-2}}, 
and add the equations.

Solution: Notice that the coefficient of $s$ in the first equation is $3,$ while in the second equation it is $1.$ 

If we multiply the second equation by $-3,$ then the coefficient of $s$ will turn into $-3,$ which will cancel with the coefficient of $3$ in the first equation.

$$
\left\{\begin{aligned}3s+4t &=8 \\ (\,s+5t &=10\,)\,\times (-3)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}3s+4t &=8 \\ -3s-15t &=-30\end{aligned}\right.
$$

Now, when we add the two equations, the variable $s$ will be eliminated:

$$
\begin{aligned}\begin{array}{rl}\cancel{3s}+4t & =8 \\ -\cancel{3s}-15t & =-30 \\ \hline (4t-15t) & =(8-30) \\ -11t & =-22 \\ t & =2\end{array}\end{aligned}
$$

Therefore, the correct answer is the following:

*Multiply the $\text{second}$ equation by $-3,$ and add the equations*.

Answer field-1: second

Answer field-2: -3

Question 17592186508917 — question.difficulty/moderate

Consider the following system of equations. 

$$
\left\{\begin{aligned}10x-3y &=36 \\ 2x+5y &=-4\end{aligned}\right.
$$

Describe the steps needed to eliminate the variable $x$ from the system:

To eliminate $x,$ multiply the 
{{field-1}} 
equation by 
{{field-2}}, 
and add the equations.

Solution: Notice that the coefficient of $x$ in the first equation is $10,$ while in the second equation it is $2.$ 

If we multiply the second equation by $-5,$ then the coefficient of $x$ will turn into $-10,$ which will cancel with the coefficient of $10$ in the first equation.

$$
\left\{\begin{aligned}10x-3y &=36 \\ (\,2x+5y &=-4\,)\,\times (-5)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}10x-3y &=36 \\ -10x-25y &=20\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}\begin{array}{rl}\cancel{10x}-3y & =36 \\ -\cancel{10x}-25y & =20 \\ \hline (-3y-25y) & =(36+20) \\ -28y & =56 \\ y & =-2\end{array}\end{aligned}
$$

Therefore, the correct answer is the following:

*Multiply the $\text{second}$ equation by $-5,$ and add the equations*.

Answer field-1: second

Answer field-2: -5

### Eliminating the Second Variable (28 captured questions)

Question 17592186193243 — None

Consider the following system of equations.
$$
\displaystyle \left\{\begin{aligned}9x + 10y &=3 \\ - 2x - y &=3\end{aligned}\right.
$$
Describe the steps needed to eliminate the variable $y$ from the system:

To eliminate $y$, multiply the
{{field-1}}
equation by
{{field-2}},
and add the equations.

Solution: 

Question 17592186193244 — None

Consider the following system of equations.

$$
\displaystyle \left\{\begin{aligned}3w + 2z &=-1 \\ 7w + 10z &=3\end{aligned}\right.
$$
Describe the steps needed to eliminate the variable $z$ from the system:

To eliminate $z$, multiply the
{{field-1}}
equation by
{{field-2}},
and add the equations.

Solution: 

Question 17592186508249 — question.difficulty/moderate

Consider the following system of equations.
$$
\left\{\begin{aligned}-8a + 4b &=5 \\ -2a - 12b &=5\end{aligned}\right.
$$
Describe the steps needed to eliminate the variable $b$ from the system:
Use an integer multiplier and leave the other equation unchanged.

To eliminate $b$, multiply the
{{field-1}}
equation by
{{field-2}},
and add the equations.

Solution: Notice that the coefficient of $b$ in the first equation is $4$, while in the second equation it is $-12$.

If we multiply the first equation by ${\color{blue}3}$, then the coefficient of $b$ will turn into $12$, which will cancel with the coefficient of $-12$ in the second equation.

$$
\left\{\begin{aligned}&(-8a + 4b = 5)\cdot (3) \\ &-2a - 12b = 5\end{aligned}\right.
$$

Now, when we add the two equations, the variable $b$ will be eliminated:

$$
\begin{aligned}
-24a + 12b &= 15 \\
-2a - 12b &= 5 \\
(-24a - 2a) &= (15 + 5) \\
-26a &= 20
\end{aligned}
$$

Therefore, the correct answer is the following:

> *To eliminate $b$, multiply the $\bbox[3pt,Gainsboro]{\color{blue}\text{first}}$ equation by $\bbox[3pt,Gainsboro]{\color{blue}3}$, and add the equations*.

Answer field-1: first

Answer field-2: 3

### Solving a System of Equations by Eliminating the First Variable (26 captured questions)

Question 17592186193226 — question.difficulty/easy

Find the solution $(x,y)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}4x-5y &=0 \\ 2x-3y &=2\end{aligned}\right.
$$

*Hint: Eliminate the variable $x.$*

Solution: Notice that the $x$-coefficient in the first equation is $4,$ while in the second equation it is $2.$ 

If we multiply the second equation by $-2,$ then the $x$-coefficient will become $-4,$ which will cancel with the coefficient of $4$ in the first equation.

$$
\left\{\begin{aligned}4x-5y &=0 \\ (\,2x-3y &=2\,)\,\times (-2)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}4x-5y &=0 \\ -4x+6y &=-4\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}\begin{array}{rl}\cancel{4x}-5y & =0 \\ -\cancel{4x}+6y & =-4 \\ \hline (-5y+6y) & =(0-4) \\ y & =-4\end{array}\end{aligned}
$$

So, the solution must have $y=-4.$ However, we still need to find $x.$ To do this, we substitute $y=-4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}\begin{aligned}4x-5y & =0 \\ 4x-5(-4) & =0 \\ 4x+20 & =0 \\ 4x & =-20 \\ x & =-5\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-5,\,y=-4,$ which can be expressed as $(-5,-4).$

Answer selection: (-5,-4)

Question 17592186193236 — None

Consider the following system of equations:
$$
\displaystyle \left\{\begin{aligned}4x + 3y &=5 \\ - x + 7y &=-9\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $x$.

The solution is $($ {{field-1}} $,$ {{field-2}} $)$.

Solution: 

Question 17592186508926 — question.difficulty/moderate

Consider the following system of equations:

$$
\left\{\begin{aligned}6x+13y &=21 \\ 2x+6y &=12\end{aligned}\right.
$$

The solution $(x,y)$ to this system is $($
{{field-1}}$\,,$
{{field-2}}
$).$

Solution: Notice that the coefficient of $x$ in the  first  equation is $6,$ while in the second equation it is $2.$ 

If we multiply the second equation by $-3,$ then the $x$-coefficient will become $-6,$ which will cancel with the coefficient of $6$ in the first equation.

$$
\left\{\begin{aligned}6x+13y &=21 \\ (\,2x+6y &=12\,)\,\times (-3)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}6x+13y &=21 \\ -6x-18y &=-36\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{array}{rl}\cancel{6x}+13y & =21 \\ -\cancel{6x}-18y & =-36 \\ \hline (13y-18y) & =(21-36) \\ -5y & =-15 \\ y & =3\end{array}
$$

So, the solution must have $y=3.$ However, we still need to find $x.$ To do this, we substitute $y=3$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}6x+13y & =21 \\ 6x+13(3) & =21 \\ 6x+39 & =21 \\ 6x & =-18 \\ x & =-3\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-3,\,y=3,$ which can be expressed as $(-3,3).$

Answer field-1: -3

Answer field-2: 3

### Solving a System of Equations by Eliminating the Second Variable (24 captured questions)

Question 17592186193212 — None

Find the solution $(x, y)$ to the following system of equations using the elimination method:
$$
\displaystyle \left\{\begin{aligned}3x - 2y &=-1 \\ 4x + y &=-5\end{aligned}\right.
$$

*Hint: Eliminate the variable $y$.*

Solution: 

Question 17592186193285 — question.difficulty/easy

Consider the following system of equations:

$$
\left\{\begin{aligned}-5x+2y &=11 \\ 7x+4y &=5\end{aligned}\right.
$$

Find the solution $(x,y)$ to this system by eliminating the variable $y.$

The solution is $($
{{field-1}}$\,,$
{{field-2}}
$).$

Solution: Notice that the $y$-coefficient in the first equation is $2,$ while in the second equation it is $4.$ 

If we multiply the first equation by $-2,$ then the $y$-coefficient will become $-4,$ which will cancel with the coefficient of $4$ in the second equation.

$$
\left\{\begin{aligned}(\,-5x+2y &=11\,)\,\times (-2) \\ 7x+4y &=5\end{aligned}\right.\,⟹\,\left\{\begin{aligned}10x-4y &=-22 \\ 7x+4y &=5\end{aligned}\right.
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{array}{rl}10x-\cancel{4y} & =-22 \\ 7x+\cancel{4y} & =5 \\ \hline (10x+7x) & =(-22+5) \\ 17x & =-17 \\ x & =-1\end{array}
$$

So, the solution must have $x=-1.$ However, we still need to find $y.$ To do this, we substitute $x=-1$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}7x+4y & =5 \\ 7(-1)+4y & =5 \\ -7+4y & =5 \\ 4y & =12 \\ y & =3\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-1,\,y=3,$ which can be expressed as $(-1,3).$

Answer field-1: -1

Answer field-2: 3

Question 17592186508927 — question.difficulty/easy

Find the solution $(p,q)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}3p+2q &=11 \\ 5p+4q &=19\end{aligned}\right.
$$

*Hint: Eliminate the variable $q.$*

Solution: Notice that the $q$-coefficient in the first equation is $2,$ while in the second equation it is $4.$ 

If we multiply the first equation by $-2,$ then the $q$-coefficient will become $-4,$ which will cancel with the coefficient of $4$ in the second equation.

$$
\left\{\begin{aligned}(\,3p+2q &=11\,)\,\times (-2) \\ 5p+4q &=19\end{aligned}\right.\,⟹\,\left\{\begin{aligned}-6p-4q &=-22 \\ 5p+4q &=19\end{aligned}\right.
$$

Now, when we add the two equations, the variable $q$ will be eliminated:

$$
\begin{aligned}\begin{array}{rl}-6p-\cancel{4q} & =-22 \\ 5p+\cancel{4q} & =19 \\ \hline (-6p+5p) & =(-22+19) \\ -p & =-3 \\ p & =3\end{array}\end{aligned}
$$

So, the solution must have $p=3.$ However, we still need to find $q.$ To do this, we substitute $p=3$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}3p+2q & =11 \\ 3(3)+2q & =11 \\ 9+2q & =11 \\ 2q & =2 \\ q & =1\end{aligned}
$$

Therefore, the solution to the system of equations is $p=3,\,q=1,$ which can be expressed as $(3,1).$

Answer selection: (3,1)
