# Quartic given two roots: originals and generated variants

All originals below are raw evidence only. Generated variants use repaired/shared operative stages.


## Original q-40091

Let $p(x) = 12x^{4} + 17x^{3} - 6x^{2} - 17x - 6$. Given that $p(1) = p(-1) = 0$, find the sum of all distinct real roots of $p(x)$.

selection: -\frac{17}{12}, -\frac{2}{5}, -\frac{1}{6}, -\frac{11}{9}, -\frac{1}{3}


## Original q-75795

Let $p(x) =-4x^{4} + 15x^{2} + 5x - 6$. Given that $p(2) = p(-1) = 0$, find the sum of all distinct real roots of $p(x)$.

selection: -2, 2, 1, -1, 0


## Original q-112638

Let $p(x)={x}^{4}+{x}^{3}-35{x}^{2}-57x+90.$ Given that $p(-3)=p(1)=0,$ find the sum of all distinct real roots of $p(x).$

selection: -2, -3, 5, -1, 6

Worked solution

Since $p(-3)=p(1)=0,$ by factor theorem $(x+3)$ and $(x-1)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x-1)$ is a factor of $p(x),$ we know that $(x-1)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x-1)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $1$ | $1$ | $1$ | $-35$ | $-57$ | $90$ |
|  | $↓$ | $1$ | $2$ | $-33$ | $-90$ |
|  | $1$ | $2$ | $-33$ | $-90$ | $0$ |

Therefore,

$$
\frac{{x}^{4}+{x}^{3}-35{x}^{2}-57x+90}{x-1}={x}^{3}+2{x}^{2}-33x-90,
$$

which means that

$$
{x}^{4}+{x}^{3}-35{x}^{2}-57x+90=(x-1)({x}^{3}+2{x}^{2}-33x-90).
$$

Now, because $(x+3)$ is also a factor of $p(x),$ it must be a factor of the quotient $({x}^{3}+2{x}^{2}-33x-90).$ So, we divide this quotient by $(x+3)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-3$ | $1$ | $2$ | $-33$ | $-90$ |
|  | $↓$ | $-3$ | $3$ | $90$ |
|  | $1$ | $-1$ | $-30$ | $0$ |

Therefore,

$$
\frac{{x}^{3}+2{x}^{2}-33x-90}{x+3}={x}^{2}-x-30,
$$

which means that

$$
{x}^{4}+{x}^{3}-35{x}^{2}-57x+90=(x-1)(x+3)({x}^{2}-x-30).
$$

We can factor the quadratic factor even further, and get

$$
{x}^{4}+{x}^{3}-35{x}^{2}-57x+90=(x-1)(x+3)(x-6)(x+5).
$$

We can now equate each factor to zero and solve for $x$ to find the three roots:

$$
\begin{aligned}x & =1\,,\,x=-3\,,\,x=6\,,\,x=-5\end{aligned}
$$

Finally, the sum of the roots of the polynomial is

$$
1-3+6-5=-1.
$$


## Original q-270967

Let $p(x)={x}^{4}-5{x}^{2}+4,$ and $p(1)=p(-1)=0.$ In **ascending order**, the distinct real roots of $p(x)$ are

$x=$
{{field-1}}, 

$\,x=$

{{field-2}}, 

$\,x=$
{{field-3}}, 

$\,x=$
{{field-4}}.

field-1: -2

field-2: -1

field-3: 1

field-4: 2

Worked solution

Since $p(1)=p(-1)=0,$ by factor theorem $(x-1)$ and $(x+1)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x-1)$ is a factor of $p(x),$ we know that $(x-1)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x-1)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $1$ | $1$ | $0$ | $-5$ | $0$ | $4$ |
|  | $↓$ | $1$ | $1$ | $-4$ | $-4$ |
|  | $1$ | $1$ | $-4$ | $-4$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-5{x}^{2}+4}{x-1}={x}^{3}+{x}^{2}-4x-4,
$$

which means that

$$
{x}^{4}-5{x}^{2}+4=(x-1)({x}^{3}+{x}^{2}-4x-4).
$$

Now, because $(x+1)$ is also a factor of $p(x),$ it must be a factor of the quotient $({x}^{3}+{x}^{2}-4x-4).$ So, we divide this quotient by $(x+1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-1$ | $1$ | $1$ | $-4$ | $-4$ |
|  | $↓$ | $-1$ | $0$ | $4$ |
|  | $1$ | $0$ | $-4$ | $0$ |

Therefore,

$$
\frac{{x}^{3}+{x}^{2}-4x-4}{x+1}={x}^{2}-4,
$$

which means that

$$
{x}^{4}-5{x}^{2}+4=(x-1)(x+1)({x}^{2}-4).
$$

We can factor the quadratic factor even further, and get

$$
{x}^{4}-5{x}^{2}+4=(x-1)(x+1)(x-2)(x+2).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots. In ascending order, the roots are

$$
\begin{aligned}x & =-2\,,\,x=-1\,,\,x=1\,,\,x=2.\end{aligned}
$$


## Original q-270970

Let $p(x)=-30{x}^{4}-127{x}^{3}-68{x}^{2}+123x-18,$ and $p(-3)=p(-2)=0.$ In **ascending order**, the distinct real roots of $p(x)$ are

$x=$
{{field-1}}, 

$\,x=$
{{field-2}}, 

$\,x=$
{{field-3}}, 

$\,x=$
{{field-4}}.

field-1: -3

field-2: -2

field-3: \frac{1}{6}

field-4: \frac{3}{5}

Worked solution

Since $p(-3)=p(-2)=0,$ by factor theorem $(x+3)$ and $(x+2)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x+3)$ is a factor of $p(x),$ we know that $(x+3)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x+3)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-3$ | $-30$ | $-127$ | $-68$ | $123$ | $-18$ |
|  | $↓$ | $90$ | $111$ | $-129$ | $18$ |
|  | $-30$ | $-37$ | $43$ | $-6$ | $0$ |

Therefore,

$$
\frac{-30{x}^{4}-127{x}^{3}-68{x}^{2}+123x-18}{x+3}=-30{x}^{3}-37{x}^{2}+43x-6,
$$

which means that

$$
-30{x}^{4}-127{x}^{3}-68{x}^{2}+123x-18=(x+3)(-30{x}^{3}-37{x}^{2}+43x-6).
$$

Now, because $(x+2)$ is also a factor of $p(x),$ it must be a factor of the quotient $(-30{x}^{3}-37{x}^{2}+43x-6).$ So, we divide this quotient by $(x+2)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-2$ | $-30$ | $-37$ | $43$ | $-6$ |
|  | $↓$ | $60$ | $-46$ | $6$ |
|  | $-30$ | $23$ | $-3$ | $0$ |

Therefore,

$$
\frac{-30{x}^{3}-37{x}^{2}+43x-6}{x+2}=-30{x}^{2}+23x-3,
$$

which means that

$$
-30{x}^{4}-127{x}^{3}-68{x}^{2}+123x-18=(x+2)(x+3)(-30{x}^{2}+23x-3).
$$

We can factor the quadratic factor even further, and get

$$
8{x}^{4}+26{x}^{3}+{x}^{2}-14x+3=-(x+2)(x+3)(6x-1)(5x-3).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots. In ascending order, the roots are

$$
\begin{aligned}x & =-3\,,\,x=-2\,,\,x=\frac{1}{6}\,,\,x=\frac{3}{5}.\end{aligned}
$$


## Original q-328522

Let $p(x)={x}^{4}+{x}^{3}-11{x}^{2}-9x+18,$ and $p(3)=p(-3)=0.$ In **ascending order**, the distinct real roots of $p(x)$ are

$x=$
{{field-1}}, 

$\,x=$
{{field-2}}, 

$\,x=$
{{field-3}}, 

$\,x=$
{{field-4}}.

field-1: -3

field-2: -2

field-3: 1

field-4: 3

Worked solution

Since $p(3)=p(-3)=0,$ by factor theorem $(x-3)$ and $(x+3)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x-3)$ is a factor of $p(x),$ we know that $(x-3)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x-3)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $3$ | $1$ | $1$ | $-11$ | $-9$ | $18$ |
|  | $↓$ | $3$ | $12$ | $3$ | $-18$ |
|  | $1$ | $4$ | $1$ | $-6$ | $0$ |

Therefore,

$$
\frac{{x}^{4}+{x}^{3}-11{x}^{2}-9x+18}{x-3}={x}^{3}+4{x}^{2}+x-6,
$$

which means that

$$
{x}^{4}+{x}^{3}-11{x}^{2}-9x+18=(x-3)({x}^{3}+4{x}^{2}+x-6).
$$

Now, because $(x+3)$ is also a factor of $p(x),$ it must be a factor of the quotient $({x}^{3}+4{x}^{2}+x-6).$ So, we divide this quotient by $(x+3)$ using synthetic division once more.

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-3$ | $1$ | $4$ | $1$ | $-6$ |
|  | $↓$ | $-3$ | $-3$ | $6$ |
|  | $1$ | $1$ | $-2$ | $0$ |

Therefore,

$$
\frac{{x}^{3}+4{x}^{2}+x-6}{x+3}={x}^{2}+x-2,
$$

which means that

$$
{x}^{4}+{x}^{3}-11{x}^{2}-9x+18=(x-3)(x+3)({x}^{2}+x-2).
$$

We can factor the quadratic factor even further, and get

$$
{x}^{4}+{x}^{3}-11{x}^{2}-9x+18=(x-3)(x+3)(x-1)(x+2).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots. In ascending order, the roots are

$$
\begin{aligned}x & =-3\,,\,x=-2\,,\,x=1\,,\,x=3.\end{aligned}
$$


## Original q-337081

Let $p(x)=9{x}^{4}+42{x}^{3}+37{x}^{2}-28x-12,$ and $p(-2)=p(-3)=0.$ In **ascending order**, the distinct real roots of $p(x)$ are

$x=$
{{field-1}}, 

$\,x=$
{{field-2}}, 

$\,x=$
{{field-3}}, 

$\,x=$
{{field-4}}.

field-1: -3

field-2: -2

field-3: -\frac{1}{3}

field-4: \frac{2}{3}

Worked solution

Since $p(-2)=p(-3)=0,$ by factor theorem $(x+2)$ and $(x+3)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x+2)$ is a factor of $p(x),$ we know that $(x+2)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x+2)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-2$ | $9$ | $42$ | $37$ | $-28$ | $-12$ |
|  | $↓$ | $-18$ | $-48$ | $22$ | $12$ |
|  | $9$ | $24$ | $-11$ | $-6$ | $0$ |

Therefore,

$$
\frac{9{x}^{4}+42{x}^{3}+37{x}^{2}-28x-12}{x+2}=9{x}^{3}+24{x}^{2}-11x-6,
$$

which means that

$$
9{x}^{4}+42{x}^{3}+37{x}^{2}-28x-12=(x+2)(9{x}^{3}+24{x}^{2}-11x-6).
$$

Now, because $(x+3)$ is also a factor of $p(x),$ it must be a factor of the quotient $(9{x}^{3}+24{x}^{2}-11x-6).$ So, we divide this quotient by $(x+3)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-3$ | $9$ | $24$ | $-11$ | $-6$ |
|  | $↓$ | $-27$ | $9$ | $6$ |
|  | $9$ | $-3$ | $-2$ | $0$ |

Therefore,

$$
\frac{9{x}^{3}+24{x}^{2}-11x-6}{x+3}=9{x}^{2}-3x-2,
$$

which means that

$$
9{x}^{4}+42{x}^{3}+37{x}^{2}-28x-12=(x+2)(x+3)(9{x}^{2}-3x-2).
$$

We can factor the quadratic factor even further, and get

$$
9{x}^{4}+42{x}^{3}+37{x}^{2}-28x-12=(x+2)(x+3)(3x+1)(3x-2).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots. In ascending order, the roots are

$$
\begin{aligned}x & =-3\,,\,x=-2\,,\,x=-\frac{1}{3}\,,\,x=\frac{2}{3}.\end{aligned}
$$


## Generated sum_integer (easy)

Let $p(x)={x}^{4}-{x}^{3}-13{x}^{2}+x+12.$ Given that $p(1)=p(-1)=0,$ find the sum of all distinct real roots of $p(x).$

selection: -1, 0, 1, -3, 4

Worked solution

Since $p(1)=p(-1)=0,$ by factor theorem $(x-1)$ and $(x+1)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x+1)$ is a factor of $p(x),$ we know that $(x+1)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x+1)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-1$ | $1$ | $-1$ | $-13$ | $1$ | $12$ |
|  | $↓$ | $-1$ | $2$ | $11$ | $-12$ |
|  | $1$ | $-2$ | $-11$ | $12$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-{x}^{3}-13{x}^{2}+x+12}{x+1}={x}^{3}-2{x}^{2}-11x+12,
$$

which means that

$$
{x}^{4}-{x}^{3}-13{x}^{2}+x+12=(x+1)({x}^{3}-2{x}^{2}-11x+12).
$$

Now, because $(x-1)$ is also a factor of $p(x),$ it must be a factor of the quotient $({x}^{3}-2{x}^{2}-11x+12).$ So, we divide this quotient by $(x-1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $1$ | $-2$ | $-11$ | $12$ |
|  | $↓$ | $1$ | $-1$ | $-12$ |
|  | $1$ | $-1$ | $-12$ | $0$ |

Therefore,

$$
\frac{{x}^{3}-2{x}^{2}-11x+12}{x-1}={x}^{2}-x-12,
$$

which means that

$$
{x}^{4}-{x}^{3}-13{x}^{2}+x+12=(x+1)(x-1)({x}^{2}-x-12).
$$

We can factor the quadratic factor even further, and get

$$
{x}^{4}-{x}^{3}-13{x}^{2}+x+12=(x+1)(x-1)(x-4)(x+3).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots:

$$
\begin{aligned}x & =-1\,,\,x=1\,,\,x=4\,,\,x=-3\end{aligned}
$$

Finally, the sum of the roots of the polynomial is

$$
-1+1+4-3=1.
$$


## Generated sum_integer (easy)

Let $p(x)={x}^{4}-14{x}^{3}+65{x}^{2}-112x+60.$ Given that $p(2)=p(6)=0,$ find the sum of all distinct real roots of $p(x).$

selection: 6, 2, 13, 14, 8

Worked solution

Since $p(2)=p(6)=0,$ by factor theorem $(x-2)$ and $(x-6)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x-6)$ is a factor of $p(x),$ we know that $(x-6)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x-6)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $6$ | $1$ | $-14$ | $65$ | $-112$ | $60$ |
|  | $↓$ | $6$ | $-48$ | $102$ | $-60$ |
|  | $1$ | $-8$ | $17$ | $-10$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-14{x}^{3}+65{x}^{2}-112x+60}{x-6}={x}^{3}-8{x}^{2}+17x-10,
$$

which means that

$$
{x}^{4}-14{x}^{3}+65{x}^{2}-112x+60=(x-6)({x}^{3}-8{x}^{2}+17x-10).
$$

Now, because $(x-2)$ is also a factor of $p(x),$ it must be a factor of the quotient $({x}^{3}-8{x}^{2}+17x-10).$ So, we divide this quotient by $(x-2)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $2$ | $1$ | $-8$ | $17$ | $-10$ |
|  | $↓$ | $2$ | $-12$ | $10$ |
|  | $1$ | $-6$ | $5$ | $0$ |

Therefore,

$$
\frac{{x}^{3}-8{x}^{2}+17x-10}{x-2}={x}^{2}-6x+5,
$$

which means that

$$
{x}^{4}-14{x}^{3}+65{x}^{2}-112x+60=(x-6)(x-2)({x}^{2}-6x+5).
$$

We can factor the quadratic factor even further, and get

$$
{x}^{4}-14{x}^{3}+65{x}^{2}-112x+60=(x-6)(x-2)(x-5)(x-1).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots:

$$
\begin{aligned}x & =6\,,\,x=2\,,\,x=5\,,\,x=1\end{aligned}
$$

Finally, the sum of the roots of the polynomial is

$$
6+2+5+1=14.
$$


## Generated roots_integer (easy)

Let $p(x)={x}^{4}-10{x}^{2}+9,$ and $p(1)=p(-1)=0.$ In **ascending order**, the distinct real roots of $p(x)$ are

$x=$
{{field-1}}, 

$\,x=$

{{field-2}}, 

$\,x=$
{{field-3}}, 

$\,x=$
{{field-4}}.

field-1: -3

field-2: -1

field-3: 1

field-4: 3

Worked solution

Since $p(1)=p(-1)=0,$ by factor theorem $(x-1)$ and $(x+1)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x-1)$ is a factor of $p(x),$ we know that $(x-1)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x-1)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $1$ | $1$ | $0$ | $-10$ | $0$ | $9$ |
|  | $↓$ | $1$ | $1$ | $-9$ | $-9$ |
|  | $1$ | $1$ | $-9$ | $-9$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-10{x}^{2}+9}{x-1}={x}^{3}+{x}^{2}-9x-9,
$$

which means that

$$
{x}^{4}-10{x}^{2}+9=(x-1)({x}^{3}+{x}^{2}-9x-9).
$$

Now, because $(x+1)$ is also a factor of $p(x),$ it must be a factor of the quotient $({x}^{3}+{x}^{2}-9x-9).$ So, we divide this quotient by $(x+1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-1$ | $1$ | $1$ | $-9$ | $-9$ |
|  | $↓$ | $-1$ | $0$ | $9$ |
|  | $1$ | $0$ | $-9$ | $0$ |

Therefore,

$$
\frac{{x}^{3}+{x}^{2}-9x-9}{x+1}={x}^{2}-9,
$$

which means that

$$
{x}^{4}-10{x}^{2}+9=(x-1)(x+1)({x}^{2}-9).
$$

We can factor the quadratic factor even further, and get

$$
{x}^{4}-10{x}^{2}+9=(x-1)(x+1)(x-3)(x+3).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots. In ascending order, the roots are

$$
\begin{aligned}x & =-3\,,\,x=-1\,,\,x=1\,,\,x=3.\end{aligned}
$$


## Generated roots_integer (easy)

Let $p(x)={x}^{4}-29{x}^{2}+100,$ and $p(2)=p(-2)=0.$ In **ascending order**, the distinct real roots of $p(x)$ are

$x=$
{{field-1}}, 

$\,x=$

{{field-2}}, 

$\,x=$
{{field-3}}, 

$\,x=$
{{field-4}}.

field-1: -5

field-2: -2

field-3: 2

field-4: 5

Worked solution

Since $p(2)=p(-2)=0,$ by factor theorem $(x-2)$ and $(x+2)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x-2)$ is a factor of $p(x),$ we know that $(x-2)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x-2)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $2$ | $1$ | $0$ | $-29$ | $0$ | $100$ |
|  | $↓$ | $2$ | $4$ | $-50$ | $-100$ |
|  | $1$ | $2$ | $-25$ | $-50$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-29{x}^{2}+100}{x-2}={x}^{3}+2{x}^{2}-25x-50,
$$

which means that

$$
{x}^{4}-29{x}^{2}+100=(x-2)({x}^{3}+2{x}^{2}-25x-50).
$$

Now, because $(x+2)$ is also a factor of $p(x),$ it must be a factor of the quotient $({x}^{3}+2{x}^{2}-25x-50).$ So, we divide this quotient by $(x+2)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-2$ | $1$ | $2$ | $-25$ | $-50$ |
|  | $↓$ | $-2$ | $0$ | $50$ |
|  | $1$ | $0$ | $-25$ | $0$ |

Therefore,

$$
\frac{{x}^{3}+2{x}^{2}-25x-50}{x+2}={x}^{2}-25,
$$

which means that

$$
{x}^{4}-29{x}^{2}+100=(x-2)(x+2)({x}^{2}-25).
$$

We can factor the quadratic factor even further, and get

$$
{x}^{4}-29{x}^{2}+100=(x-2)(x+2)(x-5)(x+5).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots. In ascending order, the roots are

$$
\begin{aligned}x & =-5\,,\,x=-2\,,\,x=2\,,\,x=5.\end{aligned}
$$


## Generated roots_integer_general (easy)

Let $p(x)={x}^{4}+{x}^{3}-38{x}^{2}-36x+72,$ and $p(1)=p(6)=0.$ In **ascending order**, the distinct real roots of $p(x)$ are

$x=$
{{field-1}}, 

$\,x=$
{{field-2}}, 

$\,x=$
{{field-3}}, 

$\,x=$
{{field-4}}.

field-1: -6

field-2: -2

field-3: 1

field-4: 6

Worked solution

Since $p(1)=p(6)=0,$ by factor theorem $(x-1)$ and $(x-6)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x-1)$ is a factor of $p(x),$ we know that $(x-1)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x-1)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $1$ | $1$ | $1$ | $-38$ | $-36$ | $72$ |
|  | $↓$ | $1$ | $2$ | $-36$ | $-72$ |
|  | $1$ | $2$ | $-36$ | $-72$ | $0$ |

Therefore,

$$
\frac{{x}^{4}+{x}^{3}-38{x}^{2}-36x+72}{x-1}={x}^{3}+2{x}^{2}-36x-72,
$$

which means that

$$
{x}^{4}+{x}^{3}-38{x}^{2}-36x+72=(x-1)({x}^{3}+2{x}^{2}-36x-72).
$$

Now, because $(x-6)$ is also a factor of $p(x),$ it must be a factor of the quotient $({x}^{3}+2{x}^{2}-36x-72).$ So, we divide this quotient by $(x-6)$ using synthetic division once more.

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $6$ | $1$ | $2$ | $-36$ | $-72$ |
|  | $↓$ | $6$ | $48$ | $72$ |
|  | $1$ | $8$ | $12$ | $0$ |

Therefore,

$$
\frac{{x}^{3}+2{x}^{2}-36x-72}{x-6}={x}^{2}+8x+12,
$$

which means that

$$
{x}^{4}+{x}^{3}-38{x}^{2}-36x+72=(x-1)(x-6)({x}^{2}+8x+12).
$$

We can factor the quadratic factor even further, and get

$$
{x}^{4}+{x}^{3}-38{x}^{2}-36x+72=(x-1)(x-6)(x+6)(x+2).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots. In ascending order, the roots are

$$
\begin{aligned}x & =-6\,,\,x=-2\,,\,x=1\,,\,x=6.\end{aligned}
$$


## Generated roots_integer_general (easy)

Let $p(x)={x}^{4}+2{x}^{3}-28{x}^{2}-50x+75,$ and $p(5)=p(1)=0.$ In **ascending order**, the distinct real roots of $p(x)$ are

$x=$
{{field-1}}, 

$\,x=$
{{field-2}}, 

$\,x=$
{{field-3}}, 

$\,x=$
{{field-4}}.

field-1: -5

field-2: -3

field-3: 1

field-4: 5

Worked solution

Since $p(5)=p(1)=0,$ by factor theorem $(x-5)$ and $(x-1)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x-5)$ is a factor of $p(x),$ we know that $(x-5)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x-5)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $5$ | $1$ | $2$ | $-28$ | $-50$ | $75$ |
|  | $↓$ | $5$ | $35$ | $35$ | $-75$ |
|  | $1$ | $7$ | $7$ | $-15$ | $0$ |

Therefore,

$$
\frac{{x}^{4}+2{x}^{3}-28{x}^{2}-50x+75}{x-5}={x}^{3}+7{x}^{2}+7x-15,
$$

which means that

$$
{x}^{4}+2{x}^{3}-28{x}^{2}-50x+75=(x-5)({x}^{3}+7{x}^{2}+7x-15).
$$

Now, because $(x-1)$ is also a factor of $p(x),$ it must be a factor of the quotient $({x}^{3}+7{x}^{2}+7x-15).$ So, we divide this quotient by $(x-1)$ using synthetic division once more.

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $1$ | $7$ | $7$ | $-15$ |
|  | $↓$ | $1$ | $8$ | $15$ |
|  | $1$ | $8$ | $15$ | $0$ |

Therefore,

$$
\frac{{x}^{3}+7{x}^{2}+7x-15}{x-1}={x}^{2}+8x+15,
$$

which means that

$$
{x}^{4}+2{x}^{3}-28{x}^{2}-50x+75=(x-5)(x-1)({x}^{2}+8x+15).
$$

We can factor the quadratic factor even further, and get

$$
{x}^{4}+2{x}^{3}-28{x}^{2}-50x+75=(x-5)(x-1)(x+3)(x+5).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots. In ascending order, the roots are

$$
\begin{aligned}x & =-5\,,\,x=-3\,,\,x=1\,,\,x=5.\end{aligned}
$$


## Generated roots_common_denominator (moderate)

Let $p(x)=4{x}^{4}-32{x}^{3}+49{x}^{2}-3x-18,$ and $p(1)=p(6)=0.$ In **ascending order**, the distinct real roots of $p(x)$ are

$x=$
{{field-1}}, 

$\,x=$
{{field-2}}, 

$\,x=$
{{field-3}}, 

$\,x=$
{{field-4}}.

field-1: -\frac{1}{2}

field-2: 1

field-3: \frac{3}{2}

field-4: 6

Worked solution

Since $p(1)=p(6)=0,$ by factor theorem $(x-1)$ and $(x-6)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x-1)$ is a factor of $p(x),$ we know that $(x-1)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x-1)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $1$ | $4$ | $-32$ | $49$ | $-3$ | $-18$ |
|  | $↓$ | $4$ | $-28$ | $21$ | $18$ |
|  | $4$ | $-28$ | $21$ | $18$ | $0$ |

Therefore,

$$
\frac{4{x}^{4}-32{x}^{3}+49{x}^{2}-3x-18}{x-1}=4{x}^{3}-28{x}^{2}+21x+18,
$$

which means that

$$
4{x}^{4}-32{x}^{3}+49{x}^{2}-3x-18=(x-1)(4{x}^{3}-28{x}^{2}+21x+18).
$$

Now, because $(x-6)$ is also a factor of $p(x),$ it must be a factor of the quotient $(4{x}^{3}-28{x}^{2}+21x+18).$ So, we divide this quotient by $(x-6)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $6$ | $4$ | $-28$ | $21$ | $18$ |
|  | $↓$ | $24$ | $-24$ | $-18$ |
|  | $4$ | $-4$ | $-3$ | $0$ |

Therefore,

$$
\frac{4{x}^{3}-28{x}^{2}+21x+18}{x-6}=4{x}^{2}-4x-3,
$$

which means that

$$
4{x}^{4}-32{x}^{3}+49{x}^{2}-3x-18=(x-1)(x-6)(4{x}^{2}-4x-3).
$$

We can factor the quadratic factor even further, and get

$$
4{x}^{4}-32{x}^{3}+49{x}^{2}-3x-18=(x-1)(x-6)(2x+1)(2x-3).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots. In ascending order, the roots are

$$
\begin{aligned}x & =-\frac{1}{2}\,,\,x=1\,,\,x=\frac{3}{2}\,,\,x=6.\end{aligned}
$$


## Generated roots_common_denominator (moderate)

Let $p(x)=4{x}^{4}+12{x}^{3}-59{x}^{2}-192x-80,$ and $p(-4)=p(4)=0.$ In **ascending order**, the distinct real roots of $p(x)$ are

$x=$
{{field-1}}, 

$\,x=$
{{field-2}}, 

$\,x=$
{{field-3}}, 

$\,x=$
{{field-4}}.

field-1: -4

field-2: -\frac{5}{2}

field-3: -\frac{1}{2}

field-4: 4

Worked solution

Since $p(-4)=p(4)=0,$ by factor theorem $(x+4)$ and $(x-4)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x+4)$ is a factor of $p(x),$ we know that $(x+4)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x+4)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-4$ | $4$ | $12$ | $-59$ | $-192$ | $-80$ |
|  | $↓$ | $-16$ | $16$ | $172$ | $80$ |
|  | $4$ | $-4$ | $-43$ | $-20$ | $0$ |

Therefore,

$$
\frac{4{x}^{4}+12{x}^{3}-59{x}^{2}-192x-80}{x+4}=4{x}^{3}-4{x}^{2}-43x-20,
$$

which means that

$$
4{x}^{4}+12{x}^{3}-59{x}^{2}-192x-80=(x+4)(4{x}^{3}-4{x}^{2}-43x-20).
$$

Now, because $(x-4)$ is also a factor of $p(x),$ it must be a factor of the quotient $(4{x}^{3}-4{x}^{2}-43x-20).$ So, we divide this quotient by $(x-4)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $4$ | $4$ | $-4$ | $-43$ | $-20$ |
|  | $↓$ | $16$ | $48$ | $20$ |
|  | $4$ | $12$ | $5$ | $0$ |

Therefore,

$$
\frac{4{x}^{3}-4{x}^{2}-43x-20}{x-4}=4{x}^{2}+12x+5,
$$

which means that

$$
4{x}^{4}+12{x}^{3}-59{x}^{2}-192x-80=(x+4)(x-4)(4{x}^{2}+12x+5).
$$

We can factor the quadratic factor even further, and get

$$
4{x}^{4}+12{x}^{3}-59{x}^{2}-192x-80=(x+4)(x-4)(2x+1)(2x+5).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots. In ascending order, the roots are

$$
\begin{aligned}x & =-4\,,\,x=-\frac{5}{2}\,,\,x=-\frac{1}{2}\,,\,x=4.\end{aligned}
$$


## Generated roots_distinct_denominators (hard)

Let $p(x)=10{x}^{4}-93{x}^{3}+233{x}^{2}-222x+72,$ and $p(1)=p(6)=0.$ In **ascending order**, the distinct real roots of $p(x)$ are

$x=$
{{field-1}}, 

$\,x=$
{{field-2}}, 

$\,x=$
{{field-3}}, 

$\,x=$
{{field-4}}.

field-1: \frac{4}{5}

field-2: 1

field-3: \frac{3}{2}

field-4: 6

Worked solution

Since $p(1)=p(6)=0,$ by factor theorem $(x-1)$ and $(x-6)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x-1)$ is a factor of $p(x),$ we know that $(x-1)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x-1)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $1$ | $10$ | $-93$ | $233$ | $-222$ | $72$ |
|  | $↓$ | $10$ | $-83$ | $150$ | $-72$ |
|  | $10$ | $-83$ | $150$ | $-72$ | $0$ |

Therefore,

$$
\frac{10{x}^{4}-93{x}^{3}+233{x}^{2}-222x+72}{x-1}=10{x}^{3}-83{x}^{2}+150x-72,
$$

which means that

$$
10{x}^{4}-93{x}^{3}+233{x}^{2}-222x+72=(x-1)(10{x}^{3}-83{x}^{2}+150x-72).
$$

Now, because $(x-6)$ is also a factor of $p(x),$ it must be a factor of the quotient $(10{x}^{3}-83{x}^{2}+150x-72).$ So, we divide this quotient by $(x-6)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $6$ | $10$ | $-83$ | $150$ | $-72$ |
|  | $↓$ | $60$ | $-138$ | $72$ |
|  | $10$ | $-23$ | $12$ | $0$ |

Therefore,

$$
\frac{10{x}^{3}-83{x}^{2}+150x-72}{x-6}=10{x}^{2}-23x+12,
$$

which means that

$$
10{x}^{4}-93{x}^{3}+233{x}^{2}-222x+72=(x-6)(x-1)(10{x}^{2}-23x+12).
$$

We can factor the quadratic factor even further, and get

$$
10{x}^{4}-93{x}^{3}+233{x}^{2}-222x+72=(x-6)(x-1)(2x-3)(5x-4).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots. In ascending order, the roots are

$$
\begin{aligned}x & =\frac{4}{5}\,,\,x=1\,,\,x=\frac{3}{2}\,,\,x=6.\end{aligned}
$$


## Generated roots_distinct_denominators (hard)

Let $p(x)=10{x}^{4}+17{x}^{3}-180{x}^{2}-272x+320,$ and $p(-4)=p(4)=0.$ In **ascending order**, the distinct real roots of $p(x)$ are

$x=$
{{field-1}}, 

$\,x=$
{{field-2}}, 

$\,x=$
{{field-3}}, 

$\,x=$
{{field-4}}.

field-1: -4

field-2: -\frac{5}{2}

field-3: \frac{4}{5}

field-4: 4

Worked solution

Since $p(-4)=p(4)=0,$ by factor theorem $(x+4)$ and $(x-4)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x+4)$ is a factor of $p(x),$ we know that $(x+4)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x+4)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-4$ | $10$ | $17$ | $-180$ | $-272$ | $320$ |
|  | $↓$ | $-40$ | $92$ | $352$ | $-320$ |
|  | $10$ | $-23$ | $-88$ | $80$ | $0$ |

Therefore,

$$
\frac{10{x}^{4}+17{x}^{3}-180{x}^{2}-272x+320}{x+4}=10{x}^{3}-23{x}^{2}-88x+80,
$$

which means that

$$
10{x}^{4}+17{x}^{3}-180{x}^{2}-272x+320=(x+4)(10{x}^{3}-23{x}^{2}-88x+80).
$$

Now, because $(x-4)$ is also a factor of $p(x),$ it must be a factor of the quotient $(10{x}^{3}-23{x}^{2}-88x+80).$ So, we divide this quotient by $(x-4)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $4$ | $10$ | $-23$ | $-88$ | $80$ |
|  | $↓$ | $40$ | $68$ | $-80$ |
|  | $10$ | $17$ | $-20$ | $0$ |

Therefore,

$$
\frac{10{x}^{3}-23{x}^{2}-88x+80}{x-4}=10{x}^{2}+17x-20,
$$

which means that

$$
10{x}^{4}+17{x}^{3}-180{x}^{2}-272x+320=(x-4)(x+4)(10{x}^{2}+17x-20).
$$

We can factor the quadratic factor even further, and get

$$
10{x}^{4}+17{x}^{3}-180{x}^{2}-272x+320=(x-4)(x+4)(2x+5)(5x-4).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots. In ascending order, the roots are

$$
\begin{aligned}x & =-4\,,\,x=-\frac{5}{2}\,,\,x=\frac{4}{5}\,,\,x=4.\end{aligned}
$$


## Generated historical_sum_fractional (hard)

Let $p(x) = -8x^{4} + 18x^{3} + 205x^{2} - 450x - 125$. Given that $p(5) = p(-5) = 0$, find the sum of all distinct real roots of $p(x)$.

selection: -\frac{9}{4}, 0, \frac{9}{4}, -\frac{1}{4}, \frac{5}{2}

Worked solution

Since $p(5)=p(-5)=0,$ by factor theorem $(x-5)$ and $(x+5)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x-5)$ is a factor of $p(x),$ we know that $(x-5)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x-5)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $5$ | $-8$ | $18$ | $205$ | $-450$ | $-125$ |
|  | $↓$ | $-40$ | $-110$ | $475$ | $125$ |
|  | $-8$ | $-22$ | $95$ | $25$ | $0$ |

Therefore,

$$
\frac{-8{x}^{4}+18{x}^{3}+205{x}^{2}-450x-125}{x-5}=-8{x}^{3}-22{x}^{2}+95x+25,
$$

which means that

$$
-8{x}^{4}+18{x}^{3}+205{x}^{2}-450x-125=(x-5)(-8{x}^{3}-22{x}^{2}+95x+25).
$$

Now, because $(x+5)$ is also a factor of $p(x),$ it must be a factor of the quotient $(-8{x}^{3}-22{x}^{2}+95x+25).$ So, we divide this quotient by $(x+5)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-5$ | $-8$ | $-22$ | $95$ | $25$ |
|  | $↓$ | $40$ | $-90$ | $-25$ |
|  | $-8$ | $18$ | $5$ | $0$ |

Therefore,

$$
\frac{-8{x}^{3}-22{x}^{2}+95x+25}{x+5}=-8{x}^{2}+18x+5,
$$

which means that

$$
-8{x}^{4}+18{x}^{3}+205{x}^{2}-450x-125=(x-5)(x+5)(-8{x}^{2}+18x+5).
$$

We can factor the quadratic factor even further, and get

$$
-8{x}^{4}+18{x}^{3}+205{x}^{2}-450x-125=-(x-5)(x+5)(2x-5)(4x+1).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots:

$$
\begin{aligned}x & =5\,,\,x=-5\,,\,x=\frac{5}{2}\,,\,x=-\frac{1}{4}\end{aligned}
$$

Finally, the sum of the roots of the polynomial is

$$
5-5+\frac{5}{2}-\frac{1}{4}=\frac{9}{4}.
$$


## Generated historical_sum_fractional (hard)

Let $p(x) = 8x^{4} + 2x^{3} - 165x^{2} + 121x - 20$. Given that $p(4) = p(-5) = 0$, find the sum of all distinct real roots of $p(x)$.

selection: \frac{3}{4}, -\frac{7}{4}, -\frac{3}{4}, -\frac{1}{4}, -1

Worked solution

Since $p(4)=p(-5)=0,$ by factor theorem $(x-4)$ and $(x+5)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x-4)$ is a factor of $p(x),$ we know that $(x-4)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x-4)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $4$ | $8$ | $2$ | $-165$ | $121$ | $-20$ |
|  | $↓$ | $32$ | $136$ | $-116$ | $20$ |
|  | $8$ | $34$ | $-29$ | $5$ | $0$ |

Therefore,

$$
\frac{8{x}^{4}+2{x}^{3}-165{x}^{2}+121x-20}{x-4}=8{x}^{3}+34{x}^{2}-29x+5,
$$

which means that

$$
8{x}^{4}+2{x}^{3}-165{x}^{2}+121x-20=(x-4)(8{x}^{3}+34{x}^{2}-29x+5).
$$

Now, because $(x+5)$ is also a factor of $p(x),$ it must be a factor of the quotient $(8{x}^{3}+34{x}^{2}-29x+5).$ So, we divide this quotient by $(x+5)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-5$ | $8$ | $34$ | $-29$ | $5$ |
|  | $↓$ | $-40$ | $30$ | $-5$ |
|  | $8$ | $-6$ | $1$ | $0$ |

Therefore,

$$
\frac{8{x}^{3}+34{x}^{2}-29x+5}{x+5}=8{x}^{2}-6x+1,
$$

which means that

$$
8{x}^{4}+2{x}^{3}-165{x}^{2}+121x-20=(x-4)(x+5)(8{x}^{2}-6x+1).
$$

We can factor the quadratic factor even further, and get

$$
8{x}^{4}+2{x}^{3}-165{x}^{2}+121x-20=(x-4)(x+5)(4x-1)(2x-1).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots:

$$
\begin{aligned}x & =4\,,\,x=-5\,,\,x=\frac{1}{4}\,,\,x=\frac{1}{2}\end{aligned}
$$

Finally, the sum of the roots of the polynomial is

$$
4-5+\frac{1}{4}+\frac{1}{2}=-\frac{1}{4}.
$$


## Generated historical_sum_halves (moderate)

Let $p(x) =16x^{4} + 8x^{3} - 591x^{2} - 288x + 540$. Given that $p(6) = p(-6) = 0$, find the sum of all distinct real roots of $p(x)$.

selection: \frac{1}{2}, 0, -\frac{1}{2}, \frac{3}{4}, -\frac{5}{4}

Worked solution

Since $p(6)=p(-6)=0,$ by factor theorem $(x-6)$ and $(x+6)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x-6)$ is a factor of $p(x),$ we know that $(x-6)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x-6)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $6$ | $16$ | $8$ | $-591$ | $-288$ | $540$ |
|  | $↓$ | $96$ | $624$ | $198$ | $-540$ |
|  | $16$ | $104$ | $33$ | $-90$ | $0$ |

Therefore,

$$
\frac{16{x}^{4}+8{x}^{3}-591{x}^{2}-288x+540}{x-6}=16{x}^{3}+104{x}^{2}+33x-90,
$$

which means that

$$
16{x}^{4}+8{x}^{3}-591{x}^{2}-288x+540=(x-6)(16{x}^{3}+104{x}^{2}+33x-90).
$$

Now, because $(x+6)$ is also a factor of $p(x),$ it must be a factor of the quotient $(16{x}^{3}+104{x}^{2}+33x-90).$ So, we divide this quotient by $(x+6)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-6$ | $16$ | $104$ | $33$ | $-90$ |
|  | $↓$ | $-96$ | $-48$ | $90$ |
|  | $16$ | $8$ | $-15$ | $0$ |

Therefore,

$$
\frac{16{x}^{3}+104{x}^{2}+33x-90}{x+6}=16{x}^{2}+8x-15,
$$

which means that

$$
16{x}^{4}+8{x}^{3}-591{x}^{2}-288x+540=(x-6)(x+6)(16{x}^{2}+8x-15).
$$

We can factor the quadratic factor even further, and get

$$
16{x}^{4}+8{x}^{3}-591{x}^{2}-288x+540=(x-6)(x+6)(4x+5)(4x-3).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots:

$$
\begin{aligned}x & =6\,,\,x=-6\,,\,x=-\frac{5}{4}\,,\,x=\frac{3}{4}\end{aligned}
$$

Finally, the sum of the roots of the polynomial is

$$
6-6-\frac{5}{4}+\frac{3}{4}=-\frac{1}{2}.
$$


## Generated historical_sum_halves (moderate)

Let $p(x) =9x^{4} + 6x^{3} - 203x^{2} + 40x + 400$. Given that $p(4) = p(-5) = 0$, find the sum of all distinct real roots of $p(x)$.

selection: \frac{1}{3}, -\frac{4}{3}, -\frac{7}{3}, -\frac{2}{3}, -1

Worked solution

Since $p(4)=p(-5)=0,$ by factor theorem $(x-4)$ and $(x+5)$ are both factors of $p(x).$
To factor $p(x)$ completely we need to find its other factors.

Since $(x-4)$ is a factor of $p(x),$ we know that $(x-4)$ divides $p(x)$ with no remainder. So, to begin factoring $p(x),$ we can divide it by $(x-4)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $4$ | $9$ | $6$ | $-203$ | $40$ | $400$ |
|  | $↓$ | $36$ | $168$ | $-140$ | $-400$ |
|  | $9$ | $42$ | $-35$ | $-100$ | $0$ |

Therefore,

$$
\frac{9{x}^{4}+6{x}^{3}-203{x}^{2}+40x+400}{x-4}=9{x}^{3}+42{x}^{2}-35x-100,
$$

which means that

$$
9{x}^{4}+6{x}^{3}-203{x}^{2}+40x+400=(x-4)(9{x}^{3}+42{x}^{2}-35x-100).
$$

Now, because $(x+5)$ is also a factor of $p(x),$ it must be a factor of the quotient $(9{x}^{3}+42{x}^{2}-35x-100).$ So, we divide this quotient by $(x+5)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-5$ | $9$ | $42$ | $-35$ | $-100$ |
|  | $↓$ | $-45$ | $15$ | $100$ |
|  | $9$ | $-3$ | $-20$ | $0$ |

Therefore,

$$
\frac{9{x}^{3}+42{x}^{2}-35x-100}{x+5}=9{x}^{2}-3x-20,
$$

which means that

$$
9{x}^{4}+6{x}^{3}-203{x}^{2}+40x+400=(x-4)(x+5)(9{x}^{2}-3x-20).
$$

We can factor the quadratic factor even further, and get

$$
9{x}^{4}+6{x}^{3}-203{x}^{2}+40x+400=(x-4)(x+5)(3x+4)(3x-5).
$$

We can now equate each factor to zero and solve for $x$ to find the four roots:

$$
\begin{aligned}x & =4\,,\,x=-5\,,\,x=-\frac{4}{3}\,,\,x=\frac{5}{3}\end{aligned}
$$

Finally, the sum of the roots of the polynomial is

$$
4-5-\frac{4}{3}+\frac{5}{3}=-\frac{2}{3}.
$$
