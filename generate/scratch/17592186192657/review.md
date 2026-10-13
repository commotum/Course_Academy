# Review: second-variable one-transformation solve

Raw historical evidence preserves missing attributes and malformed presentation. All difficulty labels below are authored. Historical distractor offsets are opaque and ineligible for normal learning.


## raw source q-170145

Find the solution $(x, y)$ to the following system of equations using the elimination method:
${3x - 2y =-1; 4x + y =-5$

*Hint: Eliminate the variable $y$.*

selection: $(-3, 5)$, $(5, 3)$, $(-3,-4)$, $(-1, 2)$, $(-1,-1)$


## changed raw evidence q-170145

Find the solution $(x, y)$ to the following system of equations using the elimination method:
${3x - 2y = 2; 4x + y =-1$

*Hint: Eliminate the variable $y$.*

selection: $(-2, 5)$, $(6, 3)$, $(-2,-4)$, $(0, 2)$, $(0,-1)$


## raw source q-238087

Consider the following system of equations:

${-5x + 2y = 11; 7x + 4y = 5$

Find the solution $(x, y)$ to this system by eliminating the variable $y$.

The solution is $($
{{field-1}} $$,
{{field-2}}
$)$.


## changed raw evidence q-238087

Consider the following system of equations:

${-5x + 2y = 6; 7x + 4y = 12$

Find the solution $(x, y)$ to this system by eliminating the variable $y$.

The solution is $($
{{field-1}} $$,
{{field-2}}
$)$.


## authored easy/radio_hint/signed_substitution seed14

Find the solution $(x, y)$ to the following system of equations using the elimination method:
$$
\left\{\begin{aligned}-3x+y&=2\\5x-6y&=1\end{aligned}\right.
$$

*Hint: Eliminate the variable $y$.*

selection: $(-1,1)$, $(\frac{11}{13},\frac{59}{13})$, $(- \frac{3}{13},\frac{17}{13})$, $(-1,5)$, $(-1,-1)$

Notice that the $y$-coefficient in the first equation is $1$, while in the second equation it is $-6$.

If we multiply the first equation by $6$, then the $y$-coefficient will become $6$, which will cancel with the coefficient of $-6$ in the second equation.

$$
\{ \left(-3x+y=2\right)\cdot (6); 5x-6y=1
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
-18x+6y&=12 \\
5x-6y&=1 \\
(-18x+5x)&=(12+1) \\
-13x&=13 \\
x&=-1
\end{aligned}
$$

So, the solution must have $x = -1$. However, we still need to find $y$. To do this, we substitute $x = -1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-3x+y&=2 \\
-3(-1)+y&=2 \\
3+y&=2 \\
y&=-1
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -1, \,y = -1
$$

which can be expressed as $(-1,-1)$.


## authored easy/radio_hint/signed_substitution seed27

Find the solution $(x, y)$ to the following system of equations using the elimination method:
$$
\left\{\begin{aligned}-3x+7y&=-16\\-4x+y&=12\end{aligned}\right.
$$

*Hint: Eliminate the variable $y$.*

selection: $(-4,-4)$, $(-4,28)$, $(- \frac{4}{25},\frac{284}{25})$, $(-4,4)$, $(\frac{68}{25},\frac{572}{25})$

Notice that the $y$-coefficient in the first equation is $7$, while in the second equation it is $1$.

If we multiply the second equation by $-7$, then the $y$-coefficient will become $-7$, which will cancel with the coefficient of $7$ in the first equation.

$$
\{ -3x+7y=-16; \left(-4x+y=12\right)\cdot (-7)
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
-3x+7y&=-16 \\
28x-7y&=-84 \\
(-3x+28x)&=(-16-84) \\
25x&=-100 \\
x&=-4
\end{aligned}
$$

So, the solution must have $x = -4$. However, we still need to find $y$. To do this, we substitute $x = -4$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}
-4x+y&=12 \\
-4(-4)+y&=12 \\
16+y&=12 \\
y&=-4
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -4, \,y = -4
$$

which can be expressed as $(-4,-4)$.


## authored easy/pair_blank/signed_substitution seed14

Consider the following system of equations:

$$
\left\{\begin{aligned}-3x+y&=2\\5x-6y&=1\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $y$.

The solution is $($ {{field-1}} $,$ {{field-2}} $)$.

field-1: $-1$

field-2: $-1$

Notice that the $y$-coefficient in the first equation is $1$, while in the second equation it is $-6$.

If we multiply the first equation by $6$, then the $y$-coefficient will become $6$, which will cancel with the coefficient of $-6$ in the second equation.

$$
\{ \left(-3x+y=2\right)\cdot (6); 5x-6y=1
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
-18x+6y&=12 \\
5x-6y&=1 \\
(-18x+5x)&=(12+1) \\
-13x&=13 \\
x&=-1
\end{aligned}
$$

So, the solution must have $x = -1$. However, we still need to find $y$. To do this, we substitute $x = -1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-3x+y&=2 \\
-3(-1)+y&=2 \\
3+y&=2 \\
y&=-1
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -1, \,y = -1
$$

which can be expressed as $(-1,-1)$.


## authored easy/pair_blank/signed_substitution seed27

Consider the following system of equations:

$$
\left\{\begin{aligned}-3x+7y&=-16\\-4x+y&=12\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $y$.

The solution is $($ {{field-1}} $,$ {{field-2}} $)$.

field-1: $-4$

field-2: $-4$

Notice that the $y$-coefficient in the first equation is $7$, while in the second equation it is $1$.

If we multiply the second equation by $-7$, then the $y$-coefficient will become $-7$, which will cancel with the coefficient of $7$ in the first equation.

$$
\{ -3x+7y=-16; \left(-4x+y=12\right)\cdot (-7)
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
-3x+7y&=-16 \\
28x-7y&=-84 \\
(-3x+28x)&=(-16-84) \\
25x&=-100 \\
x&=-4
\end{aligned}
$$

So, the solution must have $x = -4$. However, we still need to find $y$. To do this, we substitute $x = -4$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}
-4x+y&=12 \\
-4(-4)+y&=12 \\
16+y&=12 \\
y&=-4
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -4, \,y = -4
$$

which can be expressed as $(-4,-4)$.


## authored moderate/radio_hint/signed_substitution seed14

Find the solution $(x, y)$ to the following system of equations using the elimination method:
$$
\left\{\begin{aligned}-3x+2y&=18\\5x+8y&=4\end{aligned}\right.
$$

*Hint: Eliminate the variable $y$.*

selection: $(-4,3)$, $(\frac{22}{17},\frac{186}{17})$, $(-4,-3)$, $(-4,15)$, $(\frac{76}{17},\frac{267}{17})$

Notice that the $y$-coefficient in the first equation is $2$, while in the second equation it is $8$.

If we multiply the first equation by $-4$, then the $y$-coefficient will become $-8$, which will cancel with the coefficient of $8$ in the second equation.

$$
\{ \left(-3x+2y=18\right)\cdot (-4); 5x+8y=4
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
12x-8y&=-72 \\
5x+8y&=4 \\
(12x+5x)&=(-72+4) \\
17x&=-68 \\
x&=-4
\end{aligned}
$$

So, the solution must have $x = -4$. However, we still need to find $y$. To do this, we substitute $x = -4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-3x+2y&=18 \\
-3(-4)+2y&=18 \\
12+2y&=18 \\
2y&=6 \\
y&=3
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -4, \,y = 3
$$

which can be expressed as $(-4,3)$.


## authored moderate/radio_hint/signed_substitution seed27

Find the solution $(x, y)$ to the following system of equations using the elimination method:
$$
\left\{\begin{aligned}-5x-3y&=16\\4x+9y&=7\end{aligned}\right.
$$

*Hint: Eliminate the variable $y$.*

selection: $(-5,3)$, $(-5,-3)$, $(-5,- \frac{41}{3})$, $(\frac{41}{11},- \frac{127}{11})$, $(- \frac{23}{11},- \frac{61}{33})$

Notice that the $y$-coefficient in the first equation is $-3$, while in the second equation it is $9$.

If we multiply the first equation by $3$, then the $y$-coefficient will become $-9$, which will cancel with the coefficient of $9$ in the second equation.

$$
\{ \left(-5x-3y=16\right)\cdot (3); 4x+9y=7
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
-15x-9y&=48 \\
4x+9y&=7 \\
(-15x+4x)&=(48+7) \\
-11x&=55 \\
x&=-5
\end{aligned}
$$

So, the solution must have $x = -5$. However, we still need to find $y$. To do this, we substitute $x = -5$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-5x-3y&=16 \\
-5(-5)-3y&=16 \\
25-3y&=16 \\
-3y&=-9 \\
y&=3
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -5, \,y = 3
$$

which can be expressed as $(-5,3)$.


## authored moderate/radio_hint/distribution_division seed14

Find the solution $(x, y)$ to the following system of equations using the elimination method:
$$
\left\{\begin{aligned}-3x+2y&=18\\5x+8y&=4\end{aligned}\right.
$$

*Hint: Eliminate the variable $y$.*

selection: $(-4,3)$, $(-34,-42)$, $(-4,6)$, $(-4,15)$, $(\frac{22}{17},\frac{186}{17})$

Notice that the $y$-coefficient in the first equation is $2$, while in the second equation it is $8$.

If we multiply the first equation by $-4$, then the $y$-coefficient will become $-8$, which will cancel with the coefficient of $8$ in the second equation.

$$
\{ \left(-3x+2y=18\right)\cdot (-4); 5x+8y=4
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
12x-8y&=-72 \\
5x+8y&=4 \\
(12x+5x)&=(-72+4) \\
17x&=-68 \\
x&=-4
\end{aligned}
$$

So, the solution must have $x = -4$. However, we still need to find $y$. To do this, we substitute $x = -4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-3x+2y&=18 \\
-3(-4)+2y&=18 \\
12+2y&=18 \\
2y&=6 \\
y&=3
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -4, \,y = 3
$$

which can be expressed as $(-4,3)$.


## authored moderate/radio_hint/distribution_division seed27

Find the solution $(x, y)$ to the following system of equations using the elimination method:
$$
\left\{\begin{aligned}-5x-3y&=16\\4x+9y&=7\end{aligned}\right.
$$

*Hint: Eliminate the variable $y$.*

selection: $(-5,3)$, $(-5,-9)$, $(-5,- \frac{41}{3})$, $(- \frac{23}{11},- \frac{61}{33})$, $(-55,\frac{259}{3})$

Notice that the $y$-coefficient in the first equation is $-3$, while in the second equation it is $9$.

If we multiply the first equation by $3$, then the $y$-coefficient will become $-9$, which will cancel with the coefficient of $9$ in the second equation.

$$
\{ \left(-5x-3y=16\right)\cdot (3); 4x+9y=7
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
-15x-9y&=48 \\
4x+9y&=7 \\
(-15x+4x)&=(48+7) \\
-11x&=55 \\
x&=-5
\end{aligned}
$$

So, the solution must have $x = -5$. However, we still need to find $y$. To do this, we substitute $x = -5$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-5x-3y&=16 \\
-5(-5)-3y&=16 \\
25-3y&=16 \\
-3y&=-9 \\
y&=3
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -5, \,y = 3
$$

which can be expressed as $(-5,3)$.


## authored moderate/pair_blank/signed_substitution seed14

Consider the following system of equations:

$$
\left\{\begin{aligned}-3x+2y&=18\\5x+8y&=4\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $y$.

The solution is $($ {{field-1}} $,$ {{field-2}} $)$.

field-1: $-4$

field-2: $3$

Notice that the $y$-coefficient in the first equation is $2$, while in the second equation it is $8$.

If we multiply the first equation by $-4$, then the $y$-coefficient will become $-8$, which will cancel with the coefficient of $8$ in the second equation.

$$
\{ \left(-3x+2y=18\right)\cdot (-4); 5x+8y=4
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
12x-8y&=-72 \\
5x+8y&=4 \\
(12x+5x)&=(-72+4) \\
17x&=-68 \\
x&=-4
\end{aligned}
$$

So, the solution must have $x = -4$. However, we still need to find $y$. To do this, we substitute $x = -4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-3x+2y&=18 \\
-3(-4)+2y&=18 \\
12+2y&=18 \\
2y&=6 \\
y&=3
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -4, \,y = 3
$$

which can be expressed as $(-4,3)$.


## authored moderate/pair_blank/signed_substitution seed27

Consider the following system of equations:

$$
\left\{\begin{aligned}-5x-3y&=16\\4x+9y&=7\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $y$.

The solution is $($ {{field-1}} $,$ {{field-2}} $)$.

field-1: $-5$

field-2: $3$

Notice that the $y$-coefficient in the first equation is $-3$, while in the second equation it is $9$.

If we multiply the first equation by $3$, then the $y$-coefficient will become $-9$, which will cancel with the coefficient of $9$ in the second equation.

$$
\{ \left(-5x-3y=16\right)\cdot (3); 4x+9y=7
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
-15x-9y&=48 \\
4x+9y&=7 \\
(-15x+4x)&=(48+7) \\
-11x&=55 \\
x&=-5
\end{aligned}
$$

So, the solution must have $x = -5$. However, we still need to find $y$. To do this, we substitute $x = -5$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-5x-3y&=16 \\
-5(-5)-3y&=16 \\
25-3y&=16 \\
-3y&=-9 \\
y&=3
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -5, \,y = 3
$$

which can be expressed as $(-5,3)$.


## authored moderate/pair_blank/distribution_division seed14

Consider the following system of equations:

$$
\left\{\begin{aligned}-3x+2y&=18\\5x+8y&=4\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $y$.

The solution is $($ {{field-1}} $,$ {{field-2}} $)$.

field-1: $-4$

field-2: $3$

Notice that the $y$-coefficient in the first equation is $2$, while in the second equation it is $8$.

If we multiply the first equation by $-4$, then the $y$-coefficient will become $-8$, which will cancel with the coefficient of $8$ in the second equation.

$$
\{ \left(-3x+2y=18\right)\cdot (-4); 5x+8y=4
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
12x-8y&=-72 \\
5x+8y&=4 \\
(12x+5x)&=(-72+4) \\
17x&=-68 \\
x&=-4
\end{aligned}
$$

So, the solution must have $x = -4$. However, we still need to find $y$. To do this, we substitute $x = -4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-3x+2y&=18 \\
-3(-4)+2y&=18 \\
12+2y&=18 \\
2y&=6 \\
y&=3
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -4, \,y = 3
$$

which can be expressed as $(-4,3)$.


## authored moderate/pair_blank/distribution_division seed27

Consider the following system of equations:

$$
\left\{\begin{aligned}-5x-3y&=16\\4x+9y&=7\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $y$.

The solution is $($ {{field-1}} $,$ {{field-2}} $)$.

field-1: $-5$

field-2: $3$

Notice that the $y$-coefficient in the first equation is $-3$, while in the second equation it is $9$.

If we multiply the first equation by $3$, then the $y$-coefficient will become $-9$, which will cancel with the coefficient of $9$ in the second equation.

$$
\{ \left(-5x-3y=16\right)\cdot (3); 4x+9y=7
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
-15x-9y&=48 \\
4x+9y&=7 \\
(-15x+4x)&=(48+7) \\
-11x&=55 \\
x&=-5
\end{aligned}
$$

So, the solution must have $x = -5$. However, we still need to find $y$. To do this, we substitute $x = -5$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-5x-3y&=16 \\
-5(-5)-3y&=16 \\
25-3y&=16 \\
-3y&=-9 \\
y&=3
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -5, \,y = 3
$$

which can be expressed as $(-5,3)$.


## authored hard/radio_hint/signed_substitution seed14

Find the solution $(x, y)$ to the following system of equations using the elimination method:
$$
\left\{\begin{aligned}-3x+2y&=18\\5x+14y&=22\end{aligned}\right.
$$

*Hint: Eliminate the variable $y$.*

selection: $(-4,3)$, $(\frac{20}{13},\frac{147}{13})$, $(-4,-3)$, $(-4,15)$, $(\frac{74}{13},\frac{228}{13})$

Notice that the $y$-coefficient in the first equation is $2$, while in the second equation it is $14$.

If we multiply the first equation by $-7$, then the $y$-coefficient will become $-14$, which will cancel with the coefficient of $14$ in the second equation.

$$
\{ \left(-3x+2y=18\right)\cdot (-7); 5x+14y=22
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
21x-14y&=-126 \\
5x+14y&=22 \\
(21x+5x)&=(-126+22) \\
26x&=-104 \\
x&=-4
\end{aligned}
$$

So, the solution must have $x = -4$. However, we still need to find $y$. To do this, we substitute $x = -4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-3x+2y&=18 \\
-3(-4)+2y&=18 \\
12+2y&=18 \\
2y&=6 \\
y&=3
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -4, \,y = 3
$$

which can be expressed as $(-4,3)$.


## authored hard/radio_hint/signed_substitution seed27

Find the solution $(x, y)$ to the following system of equations using the elimination method:
$$
\left\{\begin{aligned}x+3y&=6\\7x+15y&=36\end{aligned}\right.
$$

*Hint: Eliminate the variable $y$.*

selection: $(3,3)$, $(21,-5)$, $(3,-1)$, $(33,-9)$, $(3,1)$

Notice that the $y$-coefficient in the first equation is $3$, while in the second equation it is $15$.

If we multiply the first equation by $-5$, then the $y$-coefficient will become $-15$, which will cancel with the coefficient of $15$ in the second equation.

$$
\{ \left(x+3y=6\right)\cdot (-5); 7x+15y=36
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
-5x-15y&=-30 \\
7x+15y&=36 \\
(-5x+7x)&=(-30+36) \\
2x&=6 \\
x&=3
\end{aligned}
$$

So, the solution must have $x = 3$. However, we still need to find $y$. To do this, we substitute $x = 3$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
x+3y&=6 \\
1(3)+3y&=6 \\
3+3y&=6 \\
3y&=3 \\
y&=1
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = 3, \,y = 1
$$

which can be expressed as $(3,1)$.


## authored hard/radio_hint/distribution_division seed14

Find the solution $(x, y)$ to the following system of equations using the elimination method:
$$
\left\{\begin{aligned}-3x+2y&=18\\5x+14y&=22\end{aligned}\right.
$$

*Hint: Eliminate the variable $y$.*

selection: $(-4,3)$, $(-52,-69)$, $(-4,6)$, $(-4,15)$, $(\frac{20}{13},\frac{147}{13})$

Notice that the $y$-coefficient in the first equation is $2$, while in the second equation it is $14$.

If we multiply the first equation by $-7$, then the $y$-coefficient will become $-14$, which will cancel with the coefficient of $14$ in the second equation.

$$
\{ \left(-3x+2y=18\right)\cdot (-7); 5x+14y=22
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
21x-14y&=-126 \\
5x+14y&=22 \\
(21x+5x)&=(-126+22) \\
26x&=-104 \\
x&=-4
\end{aligned}
$$

So, the solution must have $x = -4$. However, we still need to find $y$. To do this, we substitute $x = -4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-3x+2y&=18 \\
-3(-4)+2y&=18 \\
12+2y&=18 \\
2y&=6 \\
y&=3
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -4, \,y = 3
$$

which can be expressed as $(-4,3)$.


## authored hard/radio_hint/distribution_division seed27

Find the solution $(x, y)$ to the following system of equations using the elimination method:
$$
\left\{\begin{aligned}5x+2y&=-13\\-7x+12y&=33\end{aligned}\right.
$$

*Hint: Eliminate the variable $y$.*

selection: $(- \frac{20}{37},- \frac{381}{74})$, $(-3,-14)$, $(-3,2)$, $(- \frac{111}{2},\frac{529}{4})$, $(-3,1)$

Notice that the $y$-coefficient in the first equation is $2$, while in the second equation it is $12$.

If we multiply the first equation by $-6$, then the $y$-coefficient will become $-12$, which will cancel with the coefficient of $12$ in the second equation.

$$
\{ \left(5x+2y=-13\right)\cdot (-6); -7x+12y=33
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
-30x-12y&=78 \\
-7x+12y&=33 \\
(-30x-7x)&=(78+33) \\
-37x&=111 \\
x&=-3
\end{aligned}
$$

So, the solution must have $x = -3$. However, we still need to find $y$. To do this, we substitute $x = -3$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
5x+2y&=-13 \\
5(-3)+2y&=-13 \\
-15+2y&=-13 \\
2y&=2 \\
y&=1
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -3, \,y = 1
$$

which can be expressed as $(-3,1)$.


## authored hard/pair_blank/signed_substitution seed14

Consider the following system of equations:

$$
\left\{\begin{aligned}-3x+2y&=18\\5x+14y&=22\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $y$.

The solution is $($ {{field-1}} $,$ {{field-2}} $)$.

field-1: $-4$

field-2: $3$

Notice that the $y$-coefficient in the first equation is $2$, while in the second equation it is $14$.

If we multiply the first equation by $-7$, then the $y$-coefficient will become $-14$, which will cancel with the coefficient of $14$ in the second equation.

$$
\{ \left(-3x+2y=18\right)\cdot (-7); 5x+14y=22
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
21x-14y&=-126 \\
5x+14y&=22 \\
(21x+5x)&=(-126+22) \\
26x&=-104 \\
x&=-4
\end{aligned}
$$

So, the solution must have $x = -4$. However, we still need to find $y$. To do this, we substitute $x = -4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-3x+2y&=18 \\
-3(-4)+2y&=18 \\
12+2y&=18 \\
2y&=6 \\
y&=3
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -4, \,y = 3
$$

which can be expressed as $(-4,3)$.


## authored hard/pair_blank/signed_substitution seed27

Consider the following system of equations:

$$
\left\{\begin{aligned}x+3y&=6\\7x+15y&=36\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $y$.

The solution is $($ {{field-1}} $,$ {{field-2}} $)$.

field-1: $3$

field-2: $1$

Notice that the $y$-coefficient in the first equation is $3$, while in the second equation it is $15$.

If we multiply the first equation by $-5$, then the $y$-coefficient will become $-15$, which will cancel with the coefficient of $15$ in the second equation.

$$
\{ \left(x+3y=6\right)\cdot (-5); 7x+15y=36
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
-5x-15y&=-30 \\
7x+15y&=36 \\
(-5x+7x)&=(-30+36) \\
2x&=6 \\
x&=3
\end{aligned}
$$

So, the solution must have $x = 3$. However, we still need to find $y$. To do this, we substitute $x = 3$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
x+3y&=6 \\
1(3)+3y&=6 \\
3+3y&=6 \\
3y&=3 \\
y&=1
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = 3, \,y = 1
$$

which can be expressed as $(3,1)$.


## authored hard/pair_blank/distribution_division seed14

Consider the following system of equations:

$$
\left\{\begin{aligned}-3x+2y&=18\\5x+14y&=22\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $y$.

The solution is $($ {{field-1}} $,$ {{field-2}} $)$.

field-1: $-4$

field-2: $3$

Notice that the $y$-coefficient in the first equation is $2$, while in the second equation it is $14$.

If we multiply the first equation by $-7$, then the $y$-coefficient will become $-14$, which will cancel with the coefficient of $14$ in the second equation.

$$
\{ \left(-3x+2y=18\right)\cdot (-7); 5x+14y=22
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
21x-14y&=-126 \\
5x+14y&=22 \\
(21x+5x)&=(-126+22) \\
26x&=-104 \\
x&=-4
\end{aligned}
$$

So, the solution must have $x = -4$. However, we still need to find $y$. To do this, we substitute $x = -4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-3x+2y&=18 \\
-3(-4)+2y&=18 \\
12+2y&=18 \\
2y&=6 \\
y&=3
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -4, \,y = 3
$$

which can be expressed as $(-4,3)$.


## authored hard/pair_blank/distribution_division seed27

Consider the following system of equations:

$$
\left\{\begin{aligned}5x+2y&=-13\\-7x+12y&=33\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $y$.

The solution is $($ {{field-1}} $,$ {{field-2}} $)$.

field-1: $-3$

field-2: $1$

Notice that the $y$-coefficient in the first equation is $2$, while in the second equation it is $12$.

If we multiply the first equation by $-6$, then the $y$-coefficient will become $-12$, which will cancel with the coefficient of $12$ in the second equation.

$$
\{ \left(5x+2y=-13\right)\cdot (-6); -7x+12y=33
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
-30x-12y&=78 \\
-7x+12y&=33 \\
(-30x-7x)&=(78+33) \\
-37x&=111 \\
x&=-3
\end{aligned}
$$

So, the solution must have $x = -3$. However, we still need to find $y$. To do this, we substitute $x = -3$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
5x+2y&=-13 \\
5(-3)+2y&=-13 \\
-15+2y&=-13 \\
2y&=2 \\
y&=1
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -3, \,y = 1
$$

which can be expressed as $(-3,1)$.


## authored completion at original parameters q-170145

Find the solution $(x, y)$ to the following system of equations using the elimination method:
$$
\left\{\begin{aligned}3x-2y&=-1\\4x+y&=-5\end{aligned}\right.
$$

*Hint: Eliminate the variable $y$.*

selection: $(\frac{9}{11},- \frac{91}{11})$, $(- \frac{6}{11},- \frac{31}{11})$, $(-1,-1)$, $(-1,1)$, $(-1,-9)$

Notice that the $y$-coefficient in the first equation is $-2$, while in the second equation it is $1$.

If we multiply the second equation by $2$, then the $y$-coefficient will become $2$, which will cancel with the coefficient of $-2$ in the first equation.

$$
\{ 3x-2y=-1; \left(4x+y=-5\right)\cdot (2)
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
3x-2y&=-1 \\
8x+2y&=-10 \\
(3x+8x)&=(-1-10) \\
11x&=-11 \\
x&=-1
\end{aligned}
$$

So, the solution must have $x = -1$. However, we still need to find $y$. To do this, we substitute $x = -1$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}
4x+y&=-5 \\
4(-1)+y&=-5 \\
-4+y&=-5 \\
y&=-1
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -1, \,y = -1
$$

which can be expressed as $(-1,-1)$.


## authored completion at original parameters q-238087

Consider the following system of equations:

$$
\left\{\begin{aligned}-5x+2y&=11\\7x+4y&=5\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $y$.

The solution is $($ {{field-1}} $,$ {{field-2}} $)$.

field-1: $-1$

field-2: $3$

Notice that the $y$-coefficient in the first equation is $2$, while in the second equation it is $4$.

If we multiply the first equation by $-2$, then the $y$-coefficient will become $-4$, which will cancel with the coefficient of $4$ in the second equation.

$$
\{ \left(-5x+2y=11\right)\cdot (-2); 7x+4y=5
$$

Now, when we add the two equations, the variable $y$ will be eliminated:

$$
\begin{aligned}
10x-4y&=-22 \\
7x+4y&=5 \\
(10x+7x)&=(-22+5) \\
17x&=-17 \\
x&=-1
\end{aligned}
$$

So, the solution must have $x = -1$. However, we still need to find $y$. To do this, we substitute $x = -1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-5x+2y&=11 \\
-5(-1)+2y&=11 \\
5+2y&=11 \\
2y&=6 \\
y&=3
\end{aligned}
$$

Therefore, the solution to the system of equations is

$$
x = -1, \,y = 3
$$

which can be expressed as $(-1,3)$.
