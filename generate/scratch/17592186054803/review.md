# Originals and generated variants

The complete source records are preserved in source.json. The following comparison checks source method, field layout, sign changes, every synthetic row and concrete solution targets. Generator version quartic-two-factors-v1 is frozen after exhaustive domain checks and native grading. No figures are required.

## q-112626

### Original

Find the polynomial $P(x)$ given that 

$$
{x}^{4}+2{x}^{3}-36{x}^{2}-2x+35=(x-5)(x+1)P(x).
$$

Let $f(x)={x}^{4}+2{x}^{3}-36{x}^{2}-2x+35.$ We know that $(x-5)$ and $(x+1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x-5)$ is a factor of $f(x),$ we know that $(x-5)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-5)$ using synthetic division:

\

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $5$ | $1$ | $2$ | $-36$ | $-2$ | $35$ |
|  | $↓$ | $5$ | $35$ | $-5$ | $-35$ |
|  | $1$ | $7$ | $-1$ | $-7$ | $0$ |

Therefore,

$$
\frac{{x}^{4}+2{x}^{3}-36{x}^{2}-2x+35}{x-5}={x}^{3}+7{x}^{2}-x-7,
$$

which means that

$$
{x}^{4}+2{x}^{3}-36{x}^{2}-2x+35=(x-5)({x}^{3}+7{x}^{2}-x-7).
$$

Now, because $(x+1)$ is also a factor of $f(x),$ it must be a factor of the quotient $({x}^{3}+7{x}^{2}-x-7).$ So, we divide this quotient by $(x+1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-1$ | $1$ | $7$ | $-1$ | $-7$ |
|  | $↓$ | $-1$ | $-6$ | $7$ |
|  | $1$ | $6$ | $-7$ | $0$ |

Therefore,

$$
\frac{{x}^{3}+7{x}^{2}-x-7}{x+1}={x}^{2}+6x-7,
$$

which means that

$$
{x}^{4}+2{x}^{3}-36{x}^{2}-2x+35=(x-5)(x+1)({x}^{2}+6x-7).
$$

We can factor the quadratic factor even further, and get

$$
{x}^{4}+2{x}^{3}-36{x}^{2}-2x+35=(x-5)(x+1){{(x-1)(x+7)}_{⏟}}_{P(x)}.
$$

Therefore, $P(x)=(x-1)(x+7).$

### Variant

Find the polynomial $P(x)$ given that

$$
x^{4} + 7 x^{3} - 3 x^{2} - 19 x + 14=(x + 2)(x - 1)P(x).
$$

Let $f(x)=x^{4} + 7 x^{3} - 3 x^{2} - 19 x + 14.$ We know that $(x + 2)$ and $(x - 1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x + 2)$ is a factor of $f(x),$ we know that $(x + 2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x + 2)$ using synthetic division:

|  | $x^{4}$ | $x^{3}$ | $x^{2}$ | $x^{1}$ | $x^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-2$ | $1$ | $7$ | $-3$ | $-19$ | $14$ |
|  | $\downarrow$ | $-2$ | $-10$ | $26$ | $-14$ |
|  | $1$ | $5$ | $-13$ | $7$ | $0$ |

Therefore,

$$
\frac{x^{4} + 7 x^{3} - 3 x^{2} - 19 x + 14}{x + 2}=x^{3} + 5 x^{2} - 13 x + 7,
$$

which means that

$$
x^{4} + 7 x^{3} - 3 x^{2} - 19 x + 14=(x + 2)(x^{3} + 5 x^{2} - 13 x + 7).
$$

Now, because $(x - 1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(x^{3} + 5 x^{2} - 13 x + 7).$ So, we divide this quotient by $(x - 1)$ using synthetic division once more:

|  | $x^{3}$ | $x^{2}$ | $x^{1}$ | $x^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $1$ | $5$ | $-13$ | $7$ |
|  | $\downarrow$ | $1$ | $6$ | $-7$ |
|  | $1$ | $6$ | $-7$ | $0$ |

Therefore,

$$
\frac{x^{3} + 5 x^{2} - 13 x + 7}{x - 1}=x^{2} + 6 x - 7,
$$

which means that

$$
x^{4} + 7 x^{3} - 3 x^{2} - 19 x + 14=(x + 2)(x - 1)(x^{2} + 6 x - 7).
$$

We can factor the quadratic factor even further, and get

$$
x^{4} + 7 x^{3} - 3 x^{2} - 19 x + 14=(x + 2)(x - 1)\underbrace{(x - 1)(x + 7)}_{P(x)}.
$$

Therefore, $P(x)=(x - 1)(x + 7).$

### Review

Pass: the two supplied factors, two synthetic-division stages, requested P(x), complete field shape and source bank pattern agree. Changes are within the extracted numerical slots. q-18862 retains its reversed division order. Symbolic verification independently reads every rendered identity; native grading accepts the key and rejects every distractor, including equivalent expanded/factored blank entries.

## q-18862

### Original

Find the polynomial $P(x)$ given that 

$$
{x}^{4}-{x}^{3}-11{x}^{2}+9x+18=(x-2)(x-3)P(x).
$$

Let $f(x)={x}^{4}-{x}^{3}-11{x}^{2}+9x+18.$ We know that $(x-2)$ and $(x-3)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x-3)$ is a factor of $f(x),$ we know that $(x-3)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-3)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $3$ | $1$ | $-1$ | $-11$ | $9$ | $18$ |
|  | $↓$ | $3$ | $6$ | $-15$ | $-18$ |
|  | $1$ | $2$ | $-5$ | $-6$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-{x}^{3}-11{x}^{2}+9x+18}{x-3}={x}^{3}+2{x}^{2}-5x-6,
$$

which means that

$$
{x}^{4}-{x}^{3}-11{x}^{2}+9x+18=(x-3)({x}^{3}+2{x}^{2}-5x-6).
$$

Now, because $(x-2)$ is also a factor of $f(x),$ it must be a factor of the quotient $({x}^{3}+2{x}^{2}-5x-6).$ So, we divide this quotient by $(x-2)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $2$ | $1$ | $2$ | $-5$ | $-6$ |
|  | $↓$ | $2$ | $8$ | $6$ |
|  | $1$ | $4$ | $3$ | $0$ |

Therefore,

$$
\frac{{x}^{3}+2{x}^{2}-5x-6}{x-2}={x}^{2}+4x+3,
$$

which means that

$$
{x}^{4}-{x}^{3}-11{x}^{2}+9x+18=(x-2)(x-3)({x}^{2}+4x+3).
$$

We can factor the quadratic factor even further, and get

$$
{x}^{4}-{x}^{3}-11{x}^{2}+9x+18=(x-2)(x-3){{(x+1)(x+3)}_{⏟}}_{P(x)}.
$$

Therefore, $P(x)=(x+1)(x+3).$

### Variant

Find the polynomial $P(x)$ given that

$$
x^{4} + 5 x^{3} + 5 x^{2} - 5 x - 6=(x + 2)(x - 1)P(x).
$$

Let $f(x)=x^{4} + 5 x^{3} + 5 x^{2} - 5 x - 6.$ We know that $(x + 2)$ and $(x - 1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x - 1)$ is a factor of $f(x),$ we know that $(x - 1)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x - 1)$ using synthetic division:

|  | $x^{4}$ | $x^{3}$ | $x^{2}$ | $x^{1}$ | $x^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $1$ | $1$ | $5$ | $5$ | $-5$ | $-6$ |
|  | $\downarrow$ | $1$ | $6$ | $11$ | $6$ |
|  | $1$ | $6$ | $11$ | $6$ | $0$ |

Therefore,

$$
\frac{x^{4} + 5 x^{3} + 5 x^{2} - 5 x - 6}{x - 1}=x^{3} + 6 x^{2} + 11 x + 6,
$$

which means that

$$
x^{4} + 5 x^{3} + 5 x^{2} - 5 x - 6=(x - 1)(x^{3} + 6 x^{2} + 11 x + 6).
$$

Now, because $(x + 2)$ is also a factor of $f(x),$ it must be a factor of the quotient $(x^{3} + 6 x^{2} + 11 x + 6).$ So, we divide this quotient by $(x + 2)$ using synthetic division once more:

|  | $x^{3}$ | $x^{2}$ | $x^{1}$ | $x^{0}$ |
| --- | --- | --- | --- | --- |
| $-2$ | $1$ | $6$ | $11$ | $6$ |
|  | $\downarrow$ | $-2$ | $-8$ | $-6$ |
|  | $1$ | $4$ | $3$ | $0$ |

Therefore,

$$
\frac{x^{3} + 6 x^{2} + 11 x + 6}{x + 2}=x^{2} + 4 x + 3,
$$

which means that

$$
x^{4} + 5 x^{3} + 5 x^{2} - 5 x - 6=(x + 2)(x - 1)(x^{2} + 4 x + 3).
$$

We can factor the quadratic factor even further, and get

$$
x^{4} + 5 x^{3} + 5 x^{2} - 5 x - 6=(x + 2)(x - 1)\underbrace{(x + 1)(x + 3)}_{P(x)}.
$$

Therefore, $P(x)=(x + 1)(x + 3).$

### Review

Pass: the two supplied factors, two synthetic-division stages, requested P(x), complete field shape and source bank pattern agree. Changes are within the extracted numerical slots. q-18862 retains its reversed division order. Symbolic verification independently reads every rendered identity; native grading accepts the key and rejects every distractor, including equivalent expanded/factored blank entries.

## q-328505

### Original

The polynomial 

$$
{x}^{4}-4{x}^{3}-{x}^{2}+16x-12
$$

 
can be expressed as

$$
(x-2)(x-3)\cdot P(x).
$$

Find the polynomial $P(x).$

$P(x)=$
{{field-1}}

Let $f(x)={x}^{4}-4{x}^{3}-{x}^{2}+16x-12.$ We know that $(x-2)$ and $(x-3)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x-2)$ is a factor of $f(x),$ we know that $(x-2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-2)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $2$ | $1$ | $-4$ | $-1$ | $16$ | $-12$ |
|  | $↓$ | $2$ | $-4$ | $-10$ | $12$ |
|  | $1$ | $-2$ | $-5$ | $6$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-4{x}^{3}-{x}^{2}+16x-12}{x-2}={x}^{3}-2{x}^{2}-5x+6,
$$

which means that

$$
{x}^{4}-4{x}^{3}-{x}^{2}+16x-12=(x-2)({x}^{3}-2{x}^{2}-5x+6).
$$

Now, because $(x-3)$ is also a factor of $f(x),$ it must be a factor of the quotient $({x}^{3}-2{x}^{2}-5x+6).$ So, we divide this quotient by $(x-3)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $3$ | $1$ | $-2$ | $-5$ | $6$ |
|  | $↓$ | $3$ | $3$ | $-6$ |
|  | $1$ | $1$ | $-2$ | $0$ |

Therefore,

$$
\frac{{x}^{3}-2{x}^{2}-5x+6}{x-3}={x}^{2}+x-2,
$$

which means that

$$
{x}^{4}-4{x}^{3}-{x}^{2}+16x-12=(x-2)(x-3)({x}^{2}+x-2).
$$

Therefore,

$$
P(x)={x}^{2}+x-2=(x+2)(x-1).
$$

### Variant

The polynomial

$$
x^{4} + 2 x^{3} - 3 x^{2} - 4 x + 4
$$

can be expressed as

$$
(x + 2)(x - 1)\cdot P(x).
$$

Find the polynomial $P(x).$

$P(x)=$
{{field-1}}

Let $f(x)=x^{4} + 2 x^{3} - 3 x^{2} - 4 x + 4.$ We know that $(x + 2)$ and $(x - 1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x + 2)$ is a factor of $f(x),$ we know that $(x + 2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x + 2)$ using synthetic division:

|  | $x^{4}$ | $x^{3}$ | $x^{2}$ | $x^{1}$ | $x^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-2$ | $1$ | $2$ | $-3$ | $-4$ | $4$ |
|  | $\downarrow$ | $-2$ | $0$ | $6$ | $-4$ |
|  | $1$ | $0$ | $-3$ | $2$ | $0$ |

Therefore,

$$
\frac{x^{4} + 2 x^{3} - 3 x^{2} - 4 x + 4}{x + 2}=x^{3} - 3 x + 2,
$$

which means that

$$
x^{4} + 2 x^{3} - 3 x^{2} - 4 x + 4=(x + 2)(x^{3} - 3 x + 2).
$$

Now, because $(x - 1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(x^{3} - 3 x + 2).$ So, we divide this quotient by $(x - 1)$ using synthetic division once more:

|  | $x^{3}$ | $x^{2}$ | $x^{1}$ | $x^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $1$ | $0$ | $-3$ | $2$ |
|  | $\downarrow$ | $1$ | $1$ | $-2$ |
|  | $1$ | $1$ | $-2$ | $0$ |

Therefore,

$$
\frac{x^{3} - 3 x + 2}{x - 1}=x^{2} + x - 2,
$$

which means that

$$
x^{4} + 2 x^{3} - 3 x^{2} - 4 x + 4=(x + 2)(x - 1)(x^{2} + x - 2).
$$

Therefore,

$$
P(x)=x^{2} + x - 2=(x + 2)(x - 1).
$$

### Review

Pass: the two supplied factors, two synthetic-division stages, requested P(x), complete field shape and source bank pattern agree. Changes are within the extracted numerical slots. q-18862 retains its reversed division order. Symbolic verification independently reads every rendered identity; native grading accepts the key and rejects every distractor, including equivalent expanded/factored blank entries.

## q-112615

### Original

Find the polynomial $P(x)$ given that

$$
3{x}^{4}-13{x}^{3}+7{x}^{2}+17x-6=(x-3)(x+1)P(x).
$$

Let $f(x)=3{x}^{4}-13{x}^{3}+7{x}^{2}+17x-6.$ We know that $(x-3)$ and $(x+1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x-3)$ is a factor of $f(x),$ we know that $(x-3)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-3)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $3$ | $3$ | $-13$ | $7$ | $17$ | $-6$ |
|  | $↓$ | $9$ | $-12$ | $-15$ | $6$ |
|  | $3$ | $-4$ | $-5$ | $2$ | $0$ |

Therefore,

$$
\frac{3{x}^{4}-13{x}^{3}+7{x}^{2}+17x-6}{x-3}=3{x}^{3}-4{x}^{2}-5x+2,
$$

which means that

$$
3{x}^{4}-13{x}^{3}+7{x}^{2}+17x-6=(x-3)(3{x}^{3}-4{x}^{2}-5x+2).
$$

Now, because $(x+1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(3{x}^{3}-4{x}^{2}-5x+2).$ So, we divide this quotient by $(x+1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-1$ | $3$ | $-4$ | $-5$ | $2$ |
|  | $↓$ | $-3$ | $7$ | $-2$ |
|  | $3$ | $-7$ | $2$ | $0$ |

Therefore,

$$
\frac{3{x}^{3}-4{x}^{2}-5x+2}{x+1}=3{x}^{2}-7x+2,
$$

which means that

$$
3{x}^{4}-13{x}^{3}+7{x}^{2}+17x-6=(x-3)(x+1)(3{x}^{2}-7x+2).
$$

We can factor the quadratic factor even further, and get

$$
3{x}^{4}-13{x}^{3}+7{x}^{2}+17x-6=(x-3)(x+1){{(3x-1)(x-2)}_{⏟}}_{P(x)}.
$$

Therefore, $P(x)=(3x-1)(x-2).$

### Variant

Find the polynomial $P(x)$ given that

$$
3 x^{4} - 4 x^{3} - 11 x^{2} + 16 x - 4=(x + 2)(x - 1)P(x).
$$

Let $f(x)=3 x^{4} - 4 x^{3} - 11 x^{2} + 16 x - 4.$ We know that $(x + 2)$ and $(x - 1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x + 2)$ is a factor of $f(x),$ we know that $(x + 2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x + 2)$ using synthetic division:

|  | $x^{4}$ | $x^{3}$ | $x^{2}$ | $x^{1}$ | $x^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-2$ | $3$ | $-4$ | $-11$ | $16$ | $-4$ |
|  | $\downarrow$ | $-6$ | $20$ | $-18$ | $4$ |
|  | $3$ | $-10$ | $9$ | $-2$ | $0$ |

Therefore,

$$
\frac{3 x^{4} - 4 x^{3} - 11 x^{2} + 16 x - 4}{x + 2}=3 x^{3} - 10 x^{2} + 9 x - 2,
$$

which means that

$$
3 x^{4} - 4 x^{3} - 11 x^{2} + 16 x - 4=(x + 2)(3 x^{3} - 10 x^{2} + 9 x - 2).
$$

Now, because $(x - 1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(3 x^{3} - 10 x^{2} + 9 x - 2).$ So, we divide this quotient by $(x - 1)$ using synthetic division once more:

|  | $x^{3}$ | $x^{2}$ | $x^{1}$ | $x^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $3$ | $-10$ | $9$ | $-2$ |
|  | $\downarrow$ | $3$ | $-7$ | $2$ |
|  | $3$ | $-7$ | $2$ | $0$ |

Therefore,

$$
\frac{3 x^{3} - 10 x^{2} + 9 x - 2}{x - 1}=3 x^{2} - 7 x + 2,
$$

which means that

$$
3 x^{4} - 4 x^{3} - 11 x^{2} + 16 x - 4=(x + 2)(x - 1)(3 x^{2} - 7 x + 2).
$$

We can factor the quadratic factor even further, and get

$$
3 x^{4} - 4 x^{3} - 11 x^{2} + 16 x - 4=(x + 2)(x - 1)\underbrace{(3 x - 1)(x - 2)}_{P(x)}.
$$

Therefore, $P(x)=(3 x - 1)(x - 2).$

### Review

Pass: the two supplied factors, two synthetic-division stages, requested P(x), complete field shape and source bank pattern agree. Changes are within the extracted numerical slots. q-18862 retains its reversed division order. Symbolic verification independently reads every rendered identity; native grading accepts the key and rejects every distractor, including equivalent expanded/factored blank entries.

## q-112617

### Original

Find the polynomial $P(x)$ given that

$$
3{x}^{4}+4{x}^{3}-37{x}^{2}-14x+24=(x-3)(x+4)P(x).
$$

Let $f(x)=3{x}^{4}+4{x}^{3}-37{x}^{2}-14x+24.$ We know that $(x-3)$ and $(x+4)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x-3)$ is a factor of $f(x),$ we know that $(x-3)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-3)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $3$ | $3$ | $4$ | $-37$ | $-14$ | $24$ |
|  | $↓$ | $9$ | $39$ | $6$ | $-24$ |
|  | $3$ | $13$ | $2$ | $-8$ | $0$ |

Therefore,

$$
\frac{3{x}^{4}+4{x}^{3}-37{x}^{2}-14x+24}{x-3}=3{x}^{3}+13{x}^{2}+2x-8,
$$

which means that

$$
3{x}^{4}+4{x}^{3}-37{x}^{2}-14x+24=(x-3)(3{x}^{3}+13{x}^{2}+2x-8).
$$

Now, because $(x+4)$ is also a factor of $f(x),$ it must be a factor of the quotient $(3{x}^{3}+13{x}^{2}+2x-8).$ So, we divide this quotient by $(x+4)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-4$ | $3$ | $13$ | $2$ | $-8$ |
|  | $↓$ | $-12$ | $-4$ | $8$ |
|  | $3$ | $1$ | $-2$ | $0$ |

Therefore,

$$
\frac{3{x}^{3}+13{x}^{2}+2x-8}{x+4}=3{x}^{2}+x-2,
$$

which means that

$$
3{x}^{4}+4{x}^{3}-37{x}^{2}-14x+24=(x-3)(x+4)(3{x}^{2}+x-2).
$$

We can factor the quadratic factor even further, and get

$$
3{x}^{4}+4{x}^{3}-37{x}^{2}-14x+24=(x-3)(x+4){{(3x-2)(x+1)}_{⏟}}_{P(x)}.
$$

Therefore, $P(x)=(3x-2)(x+1).$

### Variant

Find the polynomial $P(x)$ given that

$$
3 x^{4} + 4 x^{3} - 7 x^{2} - 4 x + 4=(x + 2)(x - 1)P(x).
$$

Let $f(x)=3 x^{4} + 4 x^{3} - 7 x^{2} - 4 x + 4.$ We know that $(x + 2)$ and $(x - 1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x + 2)$ is a factor of $f(x),$ we know that $(x + 2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x + 2)$ using synthetic division:

|  | $x^{4}$ | $x^{3}$ | $x^{2}$ | $x^{1}$ | $x^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-2$ | $3$ | $4$ | $-7$ | $-4$ | $4$ |
|  | $\downarrow$ | $-6$ | $4$ | $6$ | $-4$ |
|  | $3$ | $-2$ | $-3$ | $2$ | $0$ |

Therefore,

$$
\frac{3 x^{4} + 4 x^{3} - 7 x^{2} - 4 x + 4}{x + 2}=3 x^{3} - 2 x^{2} - 3 x + 2,
$$

which means that

$$
3 x^{4} + 4 x^{3} - 7 x^{2} - 4 x + 4=(x + 2)(3 x^{3} - 2 x^{2} - 3 x + 2).
$$

Now, because $(x - 1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(3 x^{3} - 2 x^{2} - 3 x + 2).$ So, we divide this quotient by $(x - 1)$ using synthetic division once more:

|  | $x^{3}$ | $x^{2}$ | $x^{1}$ | $x^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $3$ | $-2$ | $-3$ | $2$ |
|  | $\downarrow$ | $3$ | $1$ | $-2$ |
|  | $3$ | $1$ | $-2$ | $0$ |

Therefore,

$$
\frac{3 x^{3} - 2 x^{2} - 3 x + 2}{x - 1}=3 x^{2} + x - 2,
$$

which means that

$$
3 x^{4} + 4 x^{3} - 7 x^{2} - 4 x + 4=(x + 2)(x - 1)(3 x^{2} + x - 2).
$$

We can factor the quadratic factor even further, and get

$$
3 x^{4} + 4 x^{3} - 7 x^{2} - 4 x + 4=(x + 2)(x - 1)\underbrace{(3 x - 2)(x + 1)}_{P(x)}.
$$

Therefore, $P(x)=(3 x - 2)(x + 1).$

### Review

Pass: the two supplied factors, two synthetic-division stages, requested P(x), complete field shape and source bank pattern agree. Changes are within the extracted numerical slots. q-18862 retains its reversed division order. Symbolic verification independently reads every rendered identity; native grading accepts the key and rejects every distractor, including equivalent expanded/factored blank entries.
