# Quartic factoring review

---

Raw evidence preserves missing labels/fields/keys and the known easy divisor typo. Normal anchor/variants use repaired solutions and authored method banks.

---

### q-75798 — raw evidence

Find the polynomial $P(x)$ given that

$x^{4} + x^{3} - x^{2} + x - 2 = (x + 2)(x - 1)P(x)$.

- $x^{2} - 2x + 1$

- $x^{2} - x + 1$

- $x^{2} + x + 1$

- $(x + 1)^{2}$

- $x^{2} + 1$

---

### q-75798 — generated moderate

Find the polynomial $P(x)$ given that

$x^{4} + x^{3} - x^{2} + x - 2 = (x + 2)(x - 1)P(x)$.

- ${x}^{2}+4x+1$

- ${x}^{2}-3$

- ${x}^{2}-x+1$

- ${x}^{2}-1$

- ${x}^{2}+1$ **correct**

**Worked solution**

Let $f(x)={x}^{4}+{x}^{3}-{x}^{2}+x-2.$ We know that $(x+2)$ and $(x-1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x+2)$ is a factor of $f(x),$ we know that $(x+2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+2)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-2$ | $1$ | $1$ | $-1$ | $1$ | $-2$ |
|  | $↓$ | $-2$ | $2$ | $-2$ | $2$ |
|  | $1$ | $-1$ | $1$ | $-1$ | $0$ |

Therefore,

$$
\frac{{x}^{4}+{x}^{3}-{x}^{2}+x-2}{x+2}={x}^{3}-{x}^{2}+x-1,
$$

which means that

$$
{x}^{4}+{x}^{3}-{x}^{2}+x-2=(x+2)({x}^{3}-{x}^{2}+x-1).
$$

Now, because $(x-1)$ is also a factor of $f(x),$ it must be a factor of the quotient $({x}^{3}-{x}^{2}+x-1).$ So, we divide this quotient by $(x-1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $1$ | $-1$ | $1$ | $-1$ |
|  | $↓$ | $1$ | $0$ | $1$ |
|  | $1$ | $0$ | $1$ | $0$ |

Therefore,

$$
\frac{{x}^{3}-{x}^{2}+x-1}{x-1}={x}^{2}+1,
$$

which means that

$$
{x}^{4}+{x}^{3}-{x}^{2}+x-2=(x+2)(x-1)({x}^{2}+1).
$$

To see whether the quadratic polynomial ${x}^{2}+1$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={0}^{2}-4(1)(1)=-4<0
$$

So, the quadratic polynomial ${x}^{2}+1$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
{x}^{4}+{x}^{3}-{x}^{2}+x-2=(x+2)(x-1)\underbrace{({x}^{2}+1)}_{P(x)}.
$$

Finally, $P(x)={x}^{2}+1.$

---

### q-75798 — generated moderate

Find the polynomial $P(x)$ given that

$2x^{4} - 3x^{3} + x^{2} - 12x + 12 = (x - 2)(x - 1)P(x)$.

- $2{x}^{2}+x+6$

- $2{x}^{2}-5x+6$

- $2{x}^{2}+3x+6$ **correct**

- $2{x}^{2}+3x-6$

- $2{x}^{2}+3x+2$

**Worked solution**

Let $f(x)=2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12.$ We know that $(x-2)$ and $(x-1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x-2)$ is a factor of $f(x),$ we know that $(x-2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-2)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $2$ | $2$ | $-3$ | $1$ | $-12$ | $12$ |
|  | $↓$ | $4$ | $2$ | $6$ | $-12$ |
|  | $2$ | $1$ | $3$ | $-6$ | $0$ |

Therefore,

$$
\frac{2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12}{x-2}=2{x}^{3}+{x}^{2}+3x-6,
$$

which means that

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-2)(2{x}^{3}+{x}^{2}+3x-6).
$$

Now, because $(x-1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(2{x}^{3}+{x}^{2}+3x-6).$ So, we divide this quotient by $(x-1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $2$ | $1$ | $3$ | $-6$ |
|  | $↓$ | $2$ | $3$ | $6$ |
|  | $2$ | $3$ | $6$ | $0$ |

Therefore,

$$
\frac{2{x}^{3}+{x}^{2}+3x-6}{x-1}=2{x}^{2}+3x+6,
$$

which means that

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-2)(x-1)(2{x}^{2}+3x+6).
$$

To see whether the quadratic polynomial $2{x}^{2}+3x+6$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={3}^{2}-4(2)(6)=-39<0
$$

So, the quadratic polynomial $2{x}^{2}+3x+6$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-2)(x-1)\underbrace{(2{x}^{2}+3x+6)}_{P(x)}.
$$

Finally, $P(x)=2{x}^{2}+3x+6.$

---

### q-75798 — generated moderate

Find the polynomial $P(x)$ given that

$x^{4} - 14x^{2} - 32 = (x + 4)(x - 4)P(x)$.

- ${x}^{2}-4x+2$

- ${x}^{2}-30$

- ${x}^{2}-2$

- ${x}^{2}+2$ **correct**

- ${x}^{2}+8x+2$

**Worked solution**

Let $f(x)={x}^{4}-14{x}^{2}-32.$ We know that $(x+4)$ and $(x-4)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x+4)$ is a factor of $f(x),$ we know that $(x+4)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+4)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-4$ | $1$ | $0$ | $-14$ | $0$ | $-32$ |
|  | $↓$ | $-4$ | $16$ | $-8$ | $32$ |
|  | $1$ | $-4$ | $2$ | $-8$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-14{x}^{2}-32}{x+4}={x}^{3}-4{x}^{2}+2x-8,
$$

which means that

$$
{x}^{4}-14{x}^{2}-32=(x+4)({x}^{3}-4{x}^{2}+2x-8).
$$

Now, because $(x-4)$ is also a factor of $f(x),$ it must be a factor of the quotient $({x}^{3}-4{x}^{2}+2x-8).$ So, we divide this quotient by $(x-4)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $4$ | $1$ | $-4$ | $2$ | $-8$ |
|  | $↓$ | $4$ | $0$ | $8$ |
|  | $1$ | $0$ | $2$ | $0$ |

Therefore,

$$
\frac{{x}^{3}-4{x}^{2}+2x-8}{x-4}={x}^{2}+2,
$$

which means that

$$
{x}^{4}-14{x}^{2}-32=(x+4)(x-4)({x}^{2}+2).
$$

To see whether the quadratic polynomial ${x}^{2}+2$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={0}^{2}-4(1)(2)=-8<0
$$

So, the quadratic polynomial ${x}^{2}+2$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
{x}^{4}-14{x}^{2}-32=(x+4)(x-4)\underbrace{({x}^{2}+2)}_{P(x)}.
$$

Finally, $P(x)={x}^{2}+2.$

---

### q-75803 — raw evidence

Find the polynomial $P(x)$ given that

$-3x^{4} + 16x^{3} - 4x^{2} - 4x - 5 = - (x - 5)(x - 1)P(x)$.

- $3x^{2} - 3x + 1$

- $3x^{2} + 1$

- $3x^{2} + 2x + 1$

- $3x^{2} - 4x + 1$

- $3x^{2} - 1$

---

### q-75803 — generated hard

Find the polynomial $P(x)$ given that

$-3x^{4} + 16x^{3} - 4x^{2} - 4x - 5 = - (x - 5)(x - 1)P(x)$.

- $3{x}^{2}-28x+1$

- $3{x}^{2}+2x+11$

- $3{x}^{2}-x+1$

- $3{x}^{2}+2x-1$

- $3{x}^{2}+2x+1$ **correct**

**Worked solution**

Let $f(x)=-3{x}^{4}+16{x}^{3}-4{x}^{2}-4x-5.$ We know that $(x-5)$ and $(x-1)$ are factors of $f(x),$ and we need to find its other factors.  

Because $(x-5)$ is a factor of $f(x),$ we know that $(x-5)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-5)$ using synthetic division:  

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $5$ | $-3$ | $16$ | $-4$ | $-4$ | $-5$ |
|  | $↓$ | $-15$ | $5$ | $5$ | $5$ |
|  | $-3$ | $1$ | $1$ | $1$ | $0$ |

Therefore,  

$$
\frac{-3{x}^{4}+16{x}^{3}-4{x}^{2}-4x-5}{x-5}=-3{x}^{3}+{x}^{2}+x+1,
$$

which means that  

$$
-3{x}^{4}+16{x}^{3}-4{x}^{2}-4x-5=(x-5)(-3{x}^{3}+{x}^{2}+x+1).
$$

Now, because $(x-1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(-3{x}^{3}+{x}^{2}+x+1).$ So, we divide this quotient by $(x-1)$ using synthetic division once more:  

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $-3$ | $1$ | $1$ | $1$ |
|  | $↓$ | $-3$ | $-2$ | $-1$ |
|  | $-3$ | $-2$ | $-1$ | $0$ |

Therefore,  

$$
\frac{-3{x}^{3}+{x}^{2}+x+1}{x-1}=-3{x}^{2}-2x-1,
$$

which means that  

$$
\begin{aligned}-3{x}^{4}+16{x}^{3}-4{x}^{2}-4x-5 & =(x-5)(x-1)(-3{x}^{2}-2x-1) \\  & =-(x-5)(x-1)(3{x}^{2}+2x+1).\end{aligned}
$$

To see whether the quadratic polynomial $3{x}^{2}+2x+1$ can be factored any further, we calculate its discriminant:  

$$
{b}^{2}-4ac={2}^{2}-4(3)(1)=-8<0.
$$

So, the quadratic polynomial $3{x}^{2}+2x+1$ cannot be factored over the real numbers since its discriminant is negative.  

Therefore, the full factorization of $f(x)$ over the real numbers is given by  

$$
-3{x}^{4}+16{x}^{3}-4{x}^{2}-4x-5=-(x-5)(x-1)\underbrace{(3{x}^{2}+2x+1)}_{P(x)}.
$$

Finally, $P(x)=3{x}^{2}+2x+1.$

---

### q-75803 — generated hard

Find the polynomial $P(x)$ given that

$-2x^{4} + 3x^{3} - x^{2} + 12x - 12 = - (x - 2)(x - 1)P(x)$.

- $2{x}^{2}+x+6$

- $2{x}^{2}-5x+6$

- $2{x}^{2}+3x+6$ **correct**

- $2{x}^{2}+3x-6$

- $2{x}^{2}+3x+2$

**Worked solution**

Let $f(x)=-2{x}^{4}+3{x}^{3}-{x}^{2}+12x-12.$ We know that $(x-2)$ and $(x-1)$ are factors of $f(x),$ and we need to find its other factors.  

Because $(x-2)$ is a factor of $f(x),$ we know that $(x-2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-2)$ using synthetic division:  

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $2$ | $-2$ | $3$ | $-1$ | $12$ | $-12$ |
|  | $↓$ | $-4$ | $-2$ | $-6$ | $12$ |
|  | $-2$ | $-1$ | $-3$ | $6$ | $0$ |

Therefore,  

$$
\frac{-2{x}^{4}+3{x}^{3}-{x}^{2}+12x-12}{x-2}=-2{x}^{3}-{x}^{2}-3x+6,
$$

which means that  

$$
-2{x}^{4}+3{x}^{3}-{x}^{2}+12x-12=(x-2)(-2{x}^{3}-{x}^{2}-3x+6).
$$

Now, because $(x-1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(-2{x}^{3}-{x}^{2}-3x+6).$ So, we divide this quotient by $(x-1)$ using synthetic division once more:  

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $-2$ | $-1$ | $-3$ | $6$ |
|  | $↓$ | $-2$ | $-3$ | $-6$ |
|  | $-2$ | $-3$ | $-6$ | $0$ |

Therefore,  

$$
\frac{-2{x}^{3}-{x}^{2}-3x+6}{x-1}=-2{x}^{2}-3x-6,
$$

which means that  

$$
\begin{aligned}-2{x}^{4}+3{x}^{3}-{x}^{2}+12x-12 & =(x-2)(x-1)(-2{x}^{2}-3x-6) \\  & =-(x-2)(x-1)(2{x}^{2}+3x+6).\end{aligned}
$$

To see whether the quadratic polynomial $2{x}^{2}+3x+6$ can be factored any further, we calculate its discriminant:  

$$
{b}^{2}-4ac={3}^{2}-4(2)(6)=-39<0.
$$

So, the quadratic polynomial $2{x}^{2}+3x+6$ cannot be factored over the real numbers since its discriminant is negative.  

Therefore, the full factorization of $f(x)$ over the real numbers is given by  

$$
-2{x}^{4}+3{x}^{3}-{x}^{2}+12x-12=-(x-2)(x-1)\underbrace{(2{x}^{2}+3x+6)}_{P(x)}.
$$

Finally, $P(x)=2{x}^{2}+3x+6.$

---

### q-75803 — generated hard

Find the polynomial $P(x)$ given that

$-x^{4} + 14x^{2} + 32 = - (x + 4)(x - 4)P(x)$.

- ${x}^{2}-4x+2$

- ${x}^{2}-30$

- ${x}^{2}-2$

- ${x}^{2}+2$ **correct**

- ${x}^{2}+8x+2$

**Worked solution**

Let $f(x)=-{x}^{4}+14{x}^{2}+32.$ We know that $(x+4)$ and $(x-4)$ are factors of $f(x),$ and we need to find its other factors.  

Because $(x+4)$ is a factor of $f(x),$ we know that $(x+4)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+4)$ using synthetic division:  

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-4$ | $-1$ | $0$ | $14$ | $0$ | $32$ |
|  | $↓$ | $4$ | $-16$ | $8$ | $-32$ |
|  | $-1$ | $4$ | $-2$ | $8$ | $0$ |

Therefore,  

$$
\frac{-{x}^{4}+14{x}^{2}+32}{x+4}=-{x}^{3}+4{x}^{2}-2x+8,
$$

which means that  

$$
-{x}^{4}+14{x}^{2}+32=(x+4)(-{x}^{3}+4{x}^{2}-2x+8).
$$

Now, because $(x-4)$ is also a factor of $f(x),$ it must be a factor of the quotient $(-{x}^{3}+4{x}^{2}-2x+8).$ So, we divide this quotient by $(x-4)$ using synthetic division once more:  

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $4$ | $-1$ | $4$ | $-2$ | $8$ |
|  | $↓$ | $-4$ | $0$ | $-8$ |
|  | $-1$ | $0$ | $-2$ | $0$ |

Therefore,  

$$
\frac{-{x}^{3}+4{x}^{2}-2x+8}{x-4}=-{x}^{2}-2,
$$

which means that  

$$
\begin{aligned}-{x}^{4}+14{x}^{2}+32 & =(x+4)(x-4)(-{x}^{2}-2) \\  & =-(x+4)(x-4)({x}^{2}+2).\end{aligned}
$$

To see whether the quadratic polynomial ${x}^{2}+2$ can be factored any further, we calculate its discriminant:  

$$
{b}^{2}-4ac={0}^{2}-4(1)(2)=-8<0.
$$

So, the quadratic polynomial ${x}^{2}+2$ cannot be factored over the real numbers since its discriminant is negative.  

Therefore, the full factorization of $f(x)$ over the real numbers is given by  

$$
-{x}^{4}+14{x}^{2}+32=-(x+4)(x-4)\underbrace{({x}^{2}+2)}_{P(x)}.
$$

Finally, $P(x)={x}^{2}+2.$

---

### q-76184 — raw evidence

Find the polynomial $P(x)$ given that 

$$
2{x}^{4}-10{x}^{3}-{x}^{2}+6x-5=(x-5)(x+1)P(x).
$$

**Worked solution**

Let $f(x)=2{x}^{4}-10{x}^{3}-{x}^{2}+6x-5.$ We know that $(x+1)$ and $(x-5)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x+1)$ is a factor of $f(x),$ we know that $(x+1)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+1)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-1$ | $2$ | $-10$ | $-1$ | $6$ | $-5$ |
|  | $↓$ | $-2$ | $12$ | $-11$ | $5$ |
|  | $2$ | $-12$ | $11$ | $-5$ | $0$ |

Therefore,

$$
\frac{2{x}^{4}-10{x}^{3}-{x}^{2}+6x-5}{x+1}=2{x}^{3}-12{x}^{2}+11x-5,
$$

which means that

$$
2{x}^{4}-10{x}^{3}-{x}^{2}+6x-5=(x+1)(2{x}^{3}-12{x}^{2}+11x-5).
$$

Now, because $(x-5)$ is also a factor of $f(x),$ it must be a factor of the quotient $(2{x}^{3}-12{x}^{2}+11x-5).$ So, we divide this quotient by $(x-5)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $5$ | $2$ | $-12$ | $11$ | $-5$ |
|  | $↓$ | $10$ | $-10$ | $5$ |
|  | $2$ | $-2$ | $1$ | $0$ |

Therefore,

$$
\frac{2{x}^{3}-12{x}^{2}+11x-5}{x-5}=2{x}^{2}-2x+1,
$$

which means that

$$
2{x}^{4}-10{x}^{3}-{x}^{2}+6x-5=(x-5)(x+1)(2{x}^{2}-2x+1).
$$

To see whether the quadratic polynomial $2{x}^{2}-2x+1$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac=(-2)^{2}-4(2)(1)=-4<0
$$

So, the quadratic polynomial $2{x}^{2}-2x+1$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
2{x}^{4}-10{x}^{3}-{x}^{2}+6x-5=(x-5)(x+1){{(2{x}^{2}-2x+1)}_{⏟}}_{P(x)}.
$$

Finally, $P(x)=2{x}^{2}-2x+1.$

---

### q-76184 — generated moderate

Find the polynomial $P(x)$ given that 

$$
2{x}^{4}-10{x}^{3}-{x}^{2}+6x-5=(x-5)(x+1)P(x).
$$

$P(x)=$
{{field-1}}

- $2{x}^{2}-2x+1$ **correct**

**Worked solution**

Let $f(x)=2{x}^{4}-10{x}^{3}-{x}^{2}+6x-5.$ We know that $(x+1)$ and $(x-5)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x+1)$ is a factor of $f(x),$ we know that $(x+1)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+1)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-1$ | $2$ | $-10$ | $-1$ | $6$ | $-5$ |
|  | $↓$ | $-2$ | $12$ | $-11$ | $5$ |
|  | $2$ | $-12$ | $11$ | $-5$ | $0$ |

Therefore,

$$
\frac{2{x}^{4}-10{x}^{3}-{x}^{2}+6x-5}{x+1}=2{x}^{3}-12{x}^{2}+11x-5,
$$

which means that

$$
2{x}^{4}-10{x}^{3}-{x}^{2}+6x-5=(x+1)(2{x}^{3}-12{x}^{2}+11x-5).
$$

Now, because $(x-5)$ is also a factor of $f(x),$ it must be a factor of the quotient $(2{x}^{3}-12{x}^{2}+11x-5).$ So, we divide this quotient by $(x-5)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $5$ | $2$ | $-12$ | $11$ | $-5$ |
|  | $↓$ | $10$ | $-10$ | $5$ |
|  | $2$ | $-2$ | $1$ | $0$ |

Therefore,

$$
\frac{2{x}^{3}-12{x}^{2}+11x-5}{x-5}=2{x}^{2}-2x+1,
$$

which means that

$$
2{x}^{4}-10{x}^{3}-{x}^{2}+6x-5=(x-5)(x+1)(2{x}^{2}-2x+1).
$$

To see whether the quadratic polynomial $2{x}^{2}-2x+1$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac=(-2)^{2}-4(2)(1)=-4<0
$$

So, the quadratic polynomial $2{x}^{2}-2x+1$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
2{x}^{4}-10{x}^{3}-{x}^{2}+6x-5=(x-5)(x+1)\underbrace{(2{x}^{2}-2x+1)}_{P(x)}.
$$

Finally, $P(x)=2{x}^{2}-2x+1.$

---

### q-76184 — generated moderate

Find the polynomial $P(x)$ given that 

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-1)(x-2)P(x).
$$

$P(x)=$
{{field-1}}

- $2{x}^{2}+3x+6$ **correct**

**Worked solution**

Let $f(x)=2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12.$ We know that $(x-2)$ and $(x-1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x-2)$ is a factor of $f(x),$ we know that $(x-2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-2)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $2$ | $2$ | $-3$ | $1$ | $-12$ | $12$ |
|  | $↓$ | $4$ | $2$ | $6$ | $-12$ |
|  | $2$ | $1$ | $3$ | $-6$ | $0$ |

Therefore,

$$
\frac{2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12}{x-2}=2{x}^{3}+{x}^{2}+3x-6,
$$

which means that

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-2)(2{x}^{3}+{x}^{2}+3x-6).
$$

Now, because $(x-1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(2{x}^{3}+{x}^{2}+3x-6).$ So, we divide this quotient by $(x-1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $2$ | $1$ | $3$ | $-6$ |
|  | $↓$ | $2$ | $3$ | $6$ |
|  | $2$ | $3$ | $6$ | $0$ |

Therefore,

$$
\frac{2{x}^{3}+{x}^{2}+3x-6}{x-1}=2{x}^{2}+3x+6,
$$

which means that

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-1)(x-2)(2{x}^{2}+3x+6).
$$

To see whether the quadratic polynomial $2{x}^{2}+3x+6$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={3}^{2}-4(2)(6)=-39<0
$$

So, the quadratic polynomial $2{x}^{2}+3x+6$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-1)(x-2)\underbrace{(2{x}^{2}+3x+6)}_{P(x)}.
$$

Finally, $P(x)=2{x}^{2}+3x+6.$

---

### q-76184 — generated moderate

Find the polynomial $P(x)$ given that 

$$
{x}^{4}-14{x}^{2}-32=(x-4)(x+4)P(x).
$$

$P(x)=$
{{field-1}}

- ${x}^{2}+2$ **correct**

**Worked solution**

Let $f(x)={x}^{4}-14{x}^{2}-32.$ We know that $(x+4)$ and $(x-4)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x+4)$ is a factor of $f(x),$ we know that $(x+4)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+4)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-4$ | $1$ | $0$ | $-14$ | $0$ | $-32$ |
|  | $↓$ | $-4$ | $16$ | $-8$ | $32$ |
|  | $1$ | $-4$ | $2$ | $-8$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-14{x}^{2}-32}{x+4}={x}^{3}-4{x}^{2}+2x-8,
$$

which means that

$$
{x}^{4}-14{x}^{2}-32=(x+4)({x}^{3}-4{x}^{2}+2x-8).
$$

Now, because $(x-4)$ is also a factor of $f(x),$ it must be a factor of the quotient $({x}^{3}-4{x}^{2}+2x-8).$ So, we divide this quotient by $(x-4)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $4$ | $1$ | $-4$ | $2$ | $-8$ |
|  | $↓$ | $4$ | $0$ | $8$ |
|  | $1$ | $0$ | $2$ | $0$ |

Therefore,

$$
\frac{{x}^{3}-4{x}^{2}+2x-8}{x-4}={x}^{2}+2,
$$

which means that

$$
{x}^{4}-14{x}^{2}-32=(x-4)(x+4)({x}^{2}+2).
$$

To see whether the quadratic polynomial ${x}^{2}+2$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={0}^{2}-4(1)(2)=-8<0
$$

So, the quadratic polynomial ${x}^{2}+2$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
{x}^{4}-14{x}^{2}-32=(x-4)(x+4)\underbrace{({x}^{2}+2)}_{P(x)}.
$$

Finally, $P(x)={x}^{2}+2.$

---

### q-112651 — raw evidence

Find the polynomial $P(x)$ given that 

$$
{x}^{4}-10{x}^{3}+34{x}^{2}-90x+225=(x-5)^{2}P(x).
$$

- ${x}^{2}-3x+9$

- ${x}^{2}+9$ **correct**

- ${x}^{2}+2$

- ${x}^{2}-4x+6$

- ${x}^{2}+3$

**Worked solution**

Let $f(x)={x}^{4}-10{x}^{3}+34{x}^{2}-90x+225.$ We know that $(x-5)^{2}$ is a factor of $f(x),$ and we need to find its other factors.

Because $(x-5)$ is a factor of $f(x),$ we know that $(x-5)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-5)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $5$ | $1$ | $-10$ | $34$ | $-90$ | $225$ |
|  | $↓$ | $5$ | $-25$ | $45$ | $-225$ |
|  | $1$ | $-5$ | $9$ | $-45$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-10{x}^{3}+34{x}^{2}-90x+225}{x-5}={x}^{3}-5{x}^{2}+9x-45,
$$

which means that

$$
{x}^{4}-10{x}^{3}+34{x}^{2}-90x+225=(x-5)({x}^{3}-5{x}^{2}+9x-45).
$$

Now, because $(x-5)^{2}$ is a factor of $f(x),$ $(x-5)$ must be also a factor of the quotient $({x}^{3}-5{x}^{2}+9x-45).$ So, we divide this quotient by $(x-5)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $5$ | $1$ | $-5$ | $9$ | $-45$ |
|  | $↓$ | $5$ | $0$ | $45$ |
|  | $1$ | $0$ | $9$ | $0$ |

Therefore,

$$
\frac{{x}^{3}-5{x}^{2}+9x-45}{x-2}={x}^{2}+9,
$$

which means that

$$
{x}^{4}-10{x}^{3}+34{x}^{2}-90x+225=(x-5)^{2}({x}^{2}+9).
$$

To see whether the quadratic polynomial ${x}^{2}+9$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={0}^{2}-4(1)(9)=-36<0
$$

So, the quadratic polynomial ${x}^{2}+9$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
{x}^{4}-10{x}^{3}+34{x}^{2}-90x+225=(x-5)^{2}{{({x}^{2}+9)}_{⏟}}_{P(x)}.
$$

Finally, $P(x)={x}^{2}+9.$

---

### q-112651 — generated easy

Find the polynomial $P(x)$ given that 

$$
{x}^{4}-10{x}^{3}+34{x}^{2}-90x+225=(x-5)^{2}P(x).
$$

- ${x}^{2}-10x+9$

- ${x}^{2}+59$

- ${x}^{2}-5x+9$

- ${x}^{2}-9$

- ${x}^{2}+9$ **correct**

**Worked solution**

Let $f(x)={x}^{4}-10{x}^{3}+34{x}^{2}-90x+225.$ We know that $(x-5)^{2}$ is a factor of $f(x),$ and we need to find its other factors.

Because $(x-5)$ is a factor of $f(x),$ we know that $(x-5)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-5)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $5$ | $1$ | $-10$ | $34$ | $-90$ | $225$ |
|  | $↓$ | $5$ | $-25$ | $45$ | $-225$ |
|  | $1$ | $-5$ | $9$ | $-45$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-10{x}^{3}+34{x}^{2}-90x+225}{x-5}={x}^{3}-5{x}^{2}+9x-45,
$$

which means that

$$
{x}^{4}-10{x}^{3}+34{x}^{2}-90x+225=(x-5)({x}^{3}-5{x}^{2}+9x-45).
$$

Now, because $(x-5)^{2}$ is a factor of $f(x),$ $(x-5)$ must be also a factor of the quotient $({x}^{3}-5{x}^{2}+9x-45).$ So, we divide this quotient by $(x-5)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $5$ | $1$ | $-5$ | $9$ | $-45$ |
|  | $↓$ | $5$ | $0$ | $45$ |
|  | $1$ | $0$ | $9$ | $0$ |

Therefore,

$$
\frac{{x}^{3}-5{x}^{2}+9x-45}{x-5}={x}^{2}+9,
$$

which means that

$$
{x}^{4}-10{x}^{3}+34{x}^{2}-90x+225=(x-5)^{2}({x}^{2}+9).
$$

To see whether the quadratic polynomial ${x}^{2}+9$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={0}^{2}-4(1)(9)=-36<0
$$

So, the quadratic polynomial ${x}^{2}+9$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
{x}^{4}-10{x}^{3}+34{x}^{2}-90x+225=(x-5)^{2}\underbrace{({x}^{2}+9)}_{P(x)}.
$$

Finally, $P(x)={x}^{2}+9.$

---

### q-112651 — generated easy

Find the polynomial $P(x)$ given that 

$$
{x}^{4}-2{x}^{3}+8{x}^{2}-14x+7=(x-1)^{2}P(x).
$$

- ${x}^{2}-x+7$

- ${x}^{2}-2x+7$

- ${x}^{2}+7$ **correct**

- ${x}^{2}-7$

- ${x}^{2}+9$

**Worked solution**

Let $f(x)={x}^{4}-2{x}^{3}+8{x}^{2}-14x+7.$ We know that $(x-1)^{2}$ is a factor of $f(x),$ and we need to find its other factors.

Because $(x-1)$ is a factor of $f(x),$ we know that $(x-1)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-1)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $1$ | $1$ | $-2$ | $8$ | $-14$ | $7$ |
|  | $↓$ | $1$ | $-1$ | $7$ | $-7$ |
|  | $1$ | $-1$ | $7$ | $-7$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-2{x}^{3}+8{x}^{2}-14x+7}{x-1}={x}^{3}-{x}^{2}+7x-7,
$$

which means that

$$
{x}^{4}-2{x}^{3}+8{x}^{2}-14x+7=(x-1)({x}^{3}-{x}^{2}+7x-7).
$$

Now, because $(x-1)^{2}$ is a factor of $f(x),$ $(x-1)$ must be also a factor of the quotient $({x}^{3}-{x}^{2}+7x-7).$ So, we divide this quotient by $(x-1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $1$ | $-1$ | $7$ | $-7$ |
|  | $↓$ | $1$ | $0$ | $7$ |
|  | $1$ | $0$ | $7$ | $0$ |

Therefore,

$$
\frac{{x}^{3}-{x}^{2}+7x-7}{x-1}={x}^{2}+7,
$$

which means that

$$
{x}^{4}-2{x}^{3}+8{x}^{2}-14x+7=(x-1)^{2}({x}^{2}+7).
$$

To see whether the quadratic polynomial ${x}^{2}+7$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={0}^{2}-4(1)(7)=-28<0
$$

So, the quadratic polynomial ${x}^{2}+7$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
{x}^{4}-2{x}^{3}+8{x}^{2}-14x+7=(x-1)^{2}\underbrace{({x}^{2}+7)}_{P(x)}.
$$

Finally, $P(x)={x}^{2}+7.$

---

### q-112651 — generated easy

Find the polynomial $P(x)$ given that 

$$
{x}^{4}+8{x}^{3}+18{x}^{2}+16x+32=(x+4)^{2}P(x).
$$

- ${x}^{2}+4x+2$

- ${x}^{2}+34$

- ${x}^{2}-2$

- ${x}^{2}+2$ **correct**

- ${x}^{2}+8x+2$

**Worked solution**

Let $f(x)={x}^{4}+8{x}^{3}+18{x}^{2}+16x+32.$ We know that $(x+4)^{2}$ is a factor of $f(x),$ and we need to find its other factors.

Because $(x+4)$ is a factor of $f(x),$ we know that $(x+4)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+4)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-4$ | $1$ | $8$ | $18$ | $16$ | $32$ |
|  | $↓$ | $-4$ | $-16$ | $-8$ | $-32$ |
|  | $1$ | $4$ | $2$ | $8$ | $0$ |

Therefore,

$$
\frac{{x}^{4}+8{x}^{3}+18{x}^{2}+16x+32}{x+4}={x}^{3}+4{x}^{2}+2x+8,
$$

which means that

$$
{x}^{4}+8{x}^{3}+18{x}^{2}+16x+32=(x+4)({x}^{3}+4{x}^{2}+2x+8).
$$

Now, because $(x+4)^{2}$ is a factor of $f(x),$ $(x+4)$ must be also a factor of the quotient $({x}^{3}+4{x}^{2}+2x+8).$ So, we divide this quotient by $(x+4)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-4$ | $1$ | $4$ | $2$ | $8$ |
|  | $↓$ | $-4$ | $0$ | $-8$ |
|  | $1$ | $0$ | $2$ | $0$ |

Therefore,

$$
\frac{{x}^{3}+4{x}^{2}+2x+8}{x+4}={x}^{2}+2,
$$

which means that

$$
{x}^{4}+8{x}^{3}+18{x}^{2}+16x+32=(x+4)^{2}({x}^{2}+2).
$$

To see whether the quadratic polynomial ${x}^{2}+2$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={0}^{2}-4(1)(2)=-8<0
$$

So, the quadratic polynomial ${x}^{2}+2$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
{x}^{4}+8{x}^{3}+18{x}^{2}+16x+32=(x+4)^{2}\underbrace{({x}^{2}+2)}_{P(x)}.
$$

Finally, $P(x)={x}^{2}+2.$

---

### q-18852 — raw evidence

Find the polynomial $P(x)$ given that 

$$
{x}^{4}-2{x}^{3}-2{x}^{2}-2x-3=(x-3)(x+1)P(x).
$$

- ${x}^{2}-x+1$

- ${x}^{2}-1$

- ${x}^{2}+1$ **correct**

- ${x}^{2}-2x+1$

- ${x}^{2}+x+1$

**Worked solution**

Let $f(x)={x}^{4}-2{x}^{3}-2{x}^{2}-2x-3.$ We know that $(x-3)$ and $(x+1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x-3)$ is a factor of $f(x),$ we know that $(x-3)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-3)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $3$ | $1$ | $-2$ | $-2$ | $-2$ | $-3$ |
|  | $↓$ | $3$ | $3$ | $3$ | $3$ |
|  | $1$ | $1$ | $1$ | $1$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-2{x}^{3}-2{x}^{2}-2x-3}{x-3}={x}^{3}+{x}^{2}+x+1,
$$

which means that

$$
{x}^{4}-2{x}^{3}-2{x}^{2}-2x-3=(x-3)({x}^{3}+{x}^{2}+x+1).
$$

So we obtain 

$$
f(x)=(x-3)({x}^{3}+{x}^{2}+x+1).\,
$$

Now, because $(x+1)$ is also a factor of $f(x),$ it must be a factor of the quotient $({x}^{3}+{x}^{2}+x+1).$ So, we divide this quotient by $(x+1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-1$ | $1$ | $1$ | $1$ | $1$ |
|  | $↓$ | $-1$ | $0$ | $-1$ |
|  | $1$ | $0$ | $1$ | $0$ |

Therefore,

$$
\frac{{x}^{3}+{x}^{2}+x+1}{x+1}={x}^{2}+1,
$$

which means that

$$
{x}^{4}-2{x}^{3}-2{x}^{2}-2x-3=(x-3)(x+1)({x}^{2}+1).
$$

To see whether the quadratic polynomial ${x}^{2}+1$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={0}^{2}-4(1)(1)=-4<0
$$

So, the quadratic polynomial ${x}^{2}+1$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $p(x)$ over the real numbers is given by 

$$
{x}^{4}-2{x}^{3}-2{x}^{2}-2x-3=(x-3)(x+1){{({x}^{2}+1)}_{⏟}}_{P(x)}.
$$

Finally, $P(x)={x}^{2}+1.$

---

### q-18852 — generated moderate

Find the polynomial $P(x)$ given that 

$$
{x}^{4}-2{x}^{3}-2{x}^{2}-2x-3=(x-3)(x+1)P(x).
$$

- ${x}^{2}-6x+1$

- ${x}^{2}-5$

- ${x}^{2}+x+1$

- ${x}^{2}-1$

- ${x}^{2}+1$ **correct**

**Worked solution**

Let $f(x)={x}^{4}-2{x}^{3}-2{x}^{2}-2x-3.$ We know that $(x-3)$ and $(x+1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x-3)$ is a factor of $f(x),$ we know that $(x-3)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-3)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $3$ | $1$ | $-2$ | $-2$ | $-2$ | $-3$ |
|  | $↓$ | $3$ | $3$ | $3$ | $3$ |
|  | $1$ | $1$ | $1$ | $1$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-2{x}^{3}-2{x}^{2}-2x-3}{x-3}={x}^{3}+{x}^{2}+x+1,
$$

which means that

$$
{x}^{4}-2{x}^{3}-2{x}^{2}-2x-3=(x-3)({x}^{3}+{x}^{2}+x+1).
$$

So we obtain 

$$
f(x)=(x-3)({x}^{3}+{x}^{2}+x+1).\,
$$

Now, because $(x+1)$ is also a factor of $f(x),$ it must be a factor of the quotient $({x}^{3}+{x}^{2}+x+1).$ So, we divide this quotient by $(x+1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-1$ | $1$ | $1$ | $1$ | $1$ |
|  | $↓$ | $-1$ | $0$ | $-1$ |
|  | $1$ | $0$ | $1$ | $0$ |

Therefore,

$$
\frac{{x}^{3}+{x}^{2}+x+1}{x+1}={x}^{2}+1,
$$

which means that

$$
{x}^{4}-2{x}^{3}-2{x}^{2}-2x-3=(x-3)(x+1)({x}^{2}+1).
$$

To see whether the quadratic polynomial ${x}^{2}+1$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={0}^{2}-4(1)(1)=-4<0
$$

So, the quadratic polynomial ${x}^{2}+1$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
{x}^{4}-2{x}^{3}-2{x}^{2}-2x-3=(x-3)(x+1)\underbrace{({x}^{2}+1)}_{P(x)}.
$$

Finally, $P(x)={x}^{2}+1.$

---

### q-18852 — generated moderate

Find the polynomial $P(x)$ given that 

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-2)(x-1)P(x).
$$

- $2{x}^{2}+x+6$

- $2{x}^{2}-5x+6$

- $2{x}^{2}+3x+6$ **correct**

- $2{x}^{2}+3x-6$

- $2{x}^{2}+3x+2$

**Worked solution**

Let $f(x)=2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12.$ We know that $(x-2)$ and $(x-1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x-2)$ is a factor of $f(x),$ we know that $(x-2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-2)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $2$ | $2$ | $-3$ | $1$ | $-12$ | $12$ |
|  | $↓$ | $4$ | $2$ | $6$ | $-12$ |
|  | $2$ | $1$ | $3$ | $-6$ | $0$ |

Therefore,

$$
\frac{2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12}{x-2}=2{x}^{3}+{x}^{2}+3x-6,
$$

which means that

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-2)(2{x}^{3}+{x}^{2}+3x-6).
$$

So we obtain 

$$
f(x)=(x-2)(2{x}^{3}+{x}^{2}+3x-6).\,
$$

Now, because $(x-1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(2{x}^{3}+{x}^{2}+3x-6).$ So, we divide this quotient by $(x-1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $2$ | $1$ | $3$ | $-6$ |
|  | $↓$ | $2$ | $3$ | $6$ |
|  | $2$ | $3$ | $6$ | $0$ |

Therefore,

$$
\frac{2{x}^{3}+{x}^{2}+3x-6}{x-1}=2{x}^{2}+3x+6,
$$

which means that

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-2)(x-1)(2{x}^{2}+3x+6).
$$

To see whether the quadratic polynomial $2{x}^{2}+3x+6$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={3}^{2}-4(2)(6)=-39<0
$$

So, the quadratic polynomial $2{x}^{2}+3x+6$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-2)(x-1)\underbrace{(2{x}^{2}+3x+6)}_{P(x)}.
$$

Finally, $P(x)=2{x}^{2}+3x+6.$

---

### q-18852 — generated moderate

Find the polynomial $P(x)$ given that 

$$
{x}^{4}-14{x}^{2}-32=(x+4)(x-4)P(x).
$$

- ${x}^{2}-4x+2$

- ${x}^{2}-30$

- ${x}^{2}-2$

- ${x}^{2}+2$ **correct**

- ${x}^{2}+8x+2$

**Worked solution**

Let $f(x)={x}^{4}-14{x}^{2}-32.$ We know that $(x+4)$ and $(x-4)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x+4)$ is a factor of $f(x),$ we know that $(x+4)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+4)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-4$ | $1$ | $0$ | $-14$ | $0$ | $-32$ |
|  | $↓$ | $-4$ | $16$ | $-8$ | $32$ |
|  | $1$ | $-4$ | $2$ | $-8$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-14{x}^{2}-32}{x+4}={x}^{3}-4{x}^{2}+2x-8,
$$

which means that

$$
{x}^{4}-14{x}^{2}-32=(x+4)({x}^{3}-4{x}^{2}+2x-8).
$$

So we obtain 

$$
f(x)=(x+4)({x}^{3}-4{x}^{2}+2x-8).\,
$$

Now, because $(x-4)$ is also a factor of $f(x),$ it must be a factor of the quotient $({x}^{3}-4{x}^{2}+2x-8).$ So, we divide this quotient by $(x-4)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $4$ | $1$ | $-4$ | $2$ | $-8$ |
|  | $↓$ | $4$ | $0$ | $8$ |
|  | $1$ | $0$ | $2$ | $0$ |

Therefore,

$$
\frac{{x}^{3}-4{x}^{2}+2x-8}{x-4}={x}^{2}+2,
$$

which means that

$$
{x}^{4}-14{x}^{2}-32=(x+4)(x-4)({x}^{2}+2).
$$

To see whether the quadratic polynomial ${x}^{2}+2$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={0}^{2}-4(1)(2)=-8<0
$$

So, the quadratic polynomial ${x}^{2}+2$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
{x}^{4}-14{x}^{2}-32=(x+4)(x-4)\underbrace{({x}^{2}+2)}_{P(x)}.
$$

Finally, $P(x)={x}^{2}+2.$

---

### q-75800 — raw evidence

Find the polynomial $P(x)$ given that 

$$
2{x}^{4}-3{x}^{3}-2{x}^{2}+x-2=(x+1)(x-2)P(x).
$$

- $2{x}^{2}-x+1$ **correct**

- $2{x}^{2}-6x+1$

- $2{x}^{2}-2x+1$

- $2{x}^{2}-4x+1$

- $2{x}^{2}+3x+1$

**Worked solution**

Let $f(x)=2{x}^{4}-3{x}^{3}-2{x}^{2}+x-2.$ We know that $(x-2)$ and $(x+1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x-2)$ is a factor of $f(x),$ we know that $(x-2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-2)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $2$ | $2$ | $-3$ | $-2$ | $1$ | $-2$ |
|  | $↓$ | $4$ | $2$ | $0$ | $2$ |
|  | $2$ | $1$ | $0$ | $1$ | $0$ |

Therefore,

$$
\frac{2{x}^{4}-3{x}^{3}-2{x}^{2}+x-2}{x-2}=2{x}^{3}+{x}^{2}+1,
$$

which means that

$$
2{x}^{4}-3{x}^{3}-2{x}^{2}+x-2=(x-2)(2{x}^{3}+{x}^{2}+1).
$$

Now, because $(x+1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(2{x}^{3}+{x}^{2}+1).$ So, we divide this quotient by $(x+1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-1$ | $2$ | $1$ | $0$ | $1$ |
|  | $↓$ | $-2$ | $1$ | $-1$ |
|  | $2$ | $-1$ | $1$ | $0$ |

Therefore,

$$
\frac{2{x}^{3}+{x}^{2}+1}{x+1}=2{x}^{2}-x+1,
$$

which means that

$$
2{x}^{4}-3{x}^{3}-2{x}^{2}+x-2=(x-2)(x+1)(2{x}^{2}-x+1).
$$

To see whether the quadratic polynomial $2{x}^{2}-x+1$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac=(-1)^{2}-4(2)(1)=-7<0
$$

So, the quadratic polynomial $2{x}^{2}-x+1$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
2{x}^{4}-3{x}^{3}-2{x}^{2}+x-2=(x-2)(x+1){{(2{x}^{2}-x+1)}_{⏟}}_{P(x)}.
$$

Finally, $P(x)=2{x}^{2}-x+1.$

---

### q-75800 — generated moderate

Find the polynomial $P(x)$ given that 

$$
2{x}^{4}-3{x}^{3}-2{x}^{2}+x-2=(x+1)(x-2)P(x).
$$

- $2{x}^{2}-9x+1$

- $2{x}^{2}-x-3$

- $2{x}^{2}+x+1$

- $2{x}^{2}-x-1$

- $2{x}^{2}-x+1$ **correct**

**Worked solution**

Let $f(x)=2{x}^{4}-3{x}^{3}-2{x}^{2}+x-2.$ We know that $(x-2)$ and $(x+1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x-2)$ is a factor of $f(x),$ we know that $(x-2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-2)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $2$ | $2$ | $-3$ | $-2$ | $1$ | $-2$ |
|  | $↓$ | $4$ | $2$ | $0$ | $2$ |
|  | $2$ | $1$ | $0$ | $1$ | $0$ |

Therefore,

$$
\frac{2{x}^{4}-3{x}^{3}-2{x}^{2}+x-2}{x-2}=2{x}^{3}+{x}^{2}+1,
$$

which means that

$$
2{x}^{4}-3{x}^{3}-2{x}^{2}+x-2=(x-2)(2{x}^{3}+{x}^{2}+1).
$$

Now, because $(x+1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(2{x}^{3}+{x}^{2}+1).$ So, we divide this quotient by $(x+1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $-1$ | $2$ | $1$ | $0$ | $1$ |
|  | $↓$ | $-2$ | $1$ | $-1$ |
|  | $2$ | $-1$ | $1$ | $0$ |

Therefore,

$$
\frac{2{x}^{3}+{x}^{2}+1}{x+1}=2{x}^{2}-x+1,
$$

which means that

$$
2{x}^{4}-3{x}^{3}-2{x}^{2}+x-2=(x-2)(x+1)(2{x}^{2}-x+1).
$$

To see whether the quadratic polynomial $2{x}^{2}-x+1$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac=(-1)^{2}-4(2)(1)=-7<0
$$

So, the quadratic polynomial $2{x}^{2}-x+1$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
2{x}^{4}-3{x}^{3}-2{x}^{2}+x-2=(x-2)(x+1)\underbrace{(2{x}^{2}-x+1)}_{P(x)}.
$$

Finally, $P(x)=2{x}^{2}-x+1.$

---

### q-75800 — generated moderate

Find the polynomial $P(x)$ given that 

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-1)(x-2)P(x).
$$

- $2{x}^{2}+x+6$

- $2{x}^{2}-5x+6$

- $2{x}^{2}+3x+6$ **correct**

- $2{x}^{2}+3x-6$

- $2{x}^{2}+3x+2$

**Worked solution**

Let $f(x)=2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12.$ We know that $(x-2)$ and $(x-1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x-2)$ is a factor of $f(x),$ we know that $(x-2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-2)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $2$ | $2$ | $-3$ | $1$ | $-12$ | $12$ |
|  | $↓$ | $4$ | $2$ | $6$ | $-12$ |
|  | $2$ | $1$ | $3$ | $-6$ | $0$ |

Therefore,

$$
\frac{2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12}{x-2}=2{x}^{3}+{x}^{2}+3x-6,
$$

which means that

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-2)(2{x}^{3}+{x}^{2}+3x-6).
$$

Now, because $(x-1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(2{x}^{3}+{x}^{2}+3x-6).$ So, we divide this quotient by $(x-1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $2$ | $1$ | $3$ | $-6$ |
|  | $↓$ | $2$ | $3$ | $6$ |
|  | $2$ | $3$ | $6$ | $0$ |

Therefore,

$$
\frac{2{x}^{3}+{x}^{2}+3x-6}{x-1}=2{x}^{2}+3x+6,
$$

which means that

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-2)(x-1)(2{x}^{2}+3x+6).
$$

To see whether the quadratic polynomial $2{x}^{2}+3x+6$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={3}^{2}-4(2)(6)=-39<0
$$

So, the quadratic polynomial $2{x}^{2}+3x+6$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-2)(x-1)\underbrace{(2{x}^{2}+3x+6)}_{P(x)}.
$$

Finally, $P(x)=2{x}^{2}+3x+6.$

---

### q-75800 — generated moderate

Find the polynomial $P(x)$ given that 

$$
{x}^{4}-14{x}^{2}-32=(x-4)(x+4)P(x).
$$

- ${x}^{2}-4x+2$

- ${x}^{2}-30$

- ${x}^{2}-2$

- ${x}^{2}+2$ **correct**

- ${x}^{2}+8x+2$

**Worked solution**

Let $f(x)={x}^{4}-14{x}^{2}-32.$ We know that $(x+4)$ and $(x-4)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x+4)$ is a factor of $f(x),$ we know that $(x+4)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+4)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-4$ | $1$ | $0$ | $-14$ | $0$ | $-32$ |
|  | $↓$ | $-4$ | $16$ | $-8$ | $32$ |
|  | $1$ | $-4$ | $2$ | $-8$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-14{x}^{2}-32}{x+4}={x}^{3}-4{x}^{2}+2x-8,
$$

which means that

$$
{x}^{4}-14{x}^{2}-32=(x+4)({x}^{3}-4{x}^{2}+2x-8).
$$

Now, because $(x-4)$ is also a factor of $f(x),$ it must be a factor of the quotient $({x}^{3}-4{x}^{2}+2x-8).$ So, we divide this quotient by $(x-4)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $4$ | $1$ | $-4$ | $2$ | $-8$ |
|  | $↓$ | $4$ | $0$ | $8$ |
|  | $1$ | $0$ | $2$ | $0$ |

Therefore,

$$
\frac{{x}^{3}-4{x}^{2}+2x-8}{x-4}={x}^{2}+2,
$$

which means that

$$
{x}^{4}-14{x}^{2}-32=(x+4)(x-4)({x}^{2}+2).
$$

To see whether the quadratic polynomial ${x}^{2}+2$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={0}^{2}-4(1)(2)=-8<0
$$

So, the quadratic polynomial ${x}^{2}+2$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
{x}^{4}-14{x}^{2}-32=(x+4)(x-4)\underbrace{({x}^{2}+2)}_{P(x)}.
$$

Finally, $P(x)={x}^{2}+2.$

---

### q-270972 — raw evidence

Find the polynomial $P(x)$ given that $2{x}^{4}-7{x}^{3}-34{x}^{2}+56x-192=(x+4)(x-6)P(x).$

$P(x)=$
{{field-1}}

- $2{x}^{2}-3x+8$ **correct**

**Worked solution**

Let $f(x)=2{x}^{4}-7{x}^{3}-34{x}^{2}+56x-192.$ We know that $(x+4)$ and $(x-6)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x+4)$ is a factor of $f(x),$ we know that $(x+4)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+4)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-4$ | $2$ | $-7$ | $-34$ | $56$ | $-192$ |
|  | $↓$ | $-8$ | $60$ | $-104$ | $192$ |
|  | $2$ | $-15$ | $26$ | $-48$ | $0$ |

Therefore,

$$
\frac{2{x}^{4}-7{x}^{3}-34{x}^{2}+56x-192}{x+4}=2{x}^{3}-15{x}^{2}+26x-48,
$$

which means that

$$
2{x}^{4}-7{x}^{3}-34{x}^{2}+56x-192=(x+4)(2{x}^{3}-15{x}^{2}+26x-48).
$$

Now, because $(x-6)$ is also a factor of $f(x),$ it must be a factor of the quotient $(2{x}^{3}-15{x}^{2}+26x-48).$ So, we divide this quotient by $(x-6)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $6$ | $2$ | $-15$ | $26$ | $-48$ |
|  | $↓$ | $12$ | $-18$ | $48$ |
|  | $2$ | $-3$ | $8$ | $0$ |

Therefore,

$$
\frac{2{x}^{3}-15{x}^{2}+26x-48}{x-6}=2{x}^{2}-3x+8,
$$

which means that

$$
\begin{aligned}2{x}^{4}-7{x}^{3}-34{x}^{2}+56x-192 & =(x+4)(x-6)(2{x}^{2}-3x+8)\end{aligned}
$$

To see whether the quadratic polynomial $2{x}^{2}-3x+8$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac=(-3)^{2}-4(2)(8)=-55<0
$$

So, the quadratic polynomial $2{x}^{2}-3x+8$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
2{x}^{4}-7{x}^{3}-34{x}^{2}+56x-192=(x+4)(x-6){{(2{x}^{2}-3x+8)}_{⏟}}_{P(x)}.
$$

Finally, $P(x)=2{x}^{2}-3x+8.$

---

### q-270972 — generated moderate

Find the polynomial $P(x)$ given that $2{x}^{4}-7{x}^{3}-34{x}^{2}+56x-192=(x+4)(x-6)P(x).$

$P(x)=$
{{field-1}}

- $2{x}^{2}-3x+8$ **correct**

**Worked solution**

Let $f(x)=2{x}^{4}-7{x}^{3}-34{x}^{2}+56x-192.$ We know that $(x+4)$ and $(x-6)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x+4)$ is a factor of $f(x),$ we know that $(x+4)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+4)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-4$ | $2$ | $-7$ | $-34$ | $56$ | $-192$ |
|  | $↓$ | $-8$ | $60$ | $-104$ | $192$ |
|  | $2$ | $-15$ | $26$ | $-48$ | $0$ |

Therefore,

$$
\frac{2{x}^{4}-7{x}^{3}-34{x}^{2}+56x-192}{x+4}=2{x}^{3}-15{x}^{2}+26x-48,
$$

which means that

$$
2{x}^{4}-7{x}^{3}-34{x}^{2}+56x-192=(x+4)(2{x}^{3}-15{x}^{2}+26x-48).
$$

Now, because $(x-6)$ is also a factor of $f(x),$ it must be a factor of the quotient $(2{x}^{3}-15{x}^{2}+26x-48).$ So, we divide this quotient by $(x-6)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $6$ | $2$ | $-15$ | $26$ | $-48$ |
|  | $↓$ | $12$ | $-18$ | $48$ |
|  | $2$ | $-3$ | $8$ | $0$ |

Therefore,

$$
\frac{2{x}^{3}-15{x}^{2}+26x-48}{x-6}=2{x}^{2}-3x+8,
$$

which means that

$$
\begin{aligned}2{x}^{4}-7{x}^{3}-34{x}^{2}+56x-192 & =(x+4)(x-6)(2{x}^{2}-3x+8)\end{aligned}
$$

To see whether the quadratic polynomial $2{x}^{2}-3x+8$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac=(-3)^{2}-4(2)(8)=-55<0
$$

So, the quadratic polynomial $2{x}^{2}-3x+8$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
2{x}^{4}-7{x}^{3}-34{x}^{2}+56x-192=(x+4)(x-6)\underbrace{(2{x}^{2}-3x+8)}_{P(x)}.
$$

Finally, $P(x)=2{x}^{2}-3x+8.$

---

### q-270972 — generated moderate

Find the polynomial $P(x)$ given that $2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-2)(x-1)P(x).$

$P(x)=$
{{field-1}}

- $2{x}^{2}+3x+6$ **correct**

**Worked solution**

Let $f(x)=2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12.$ We know that $(x-2)$ and $(x-1)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x-2)$ is a factor of $f(x),$ we know that $(x-2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-2)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $2$ | $2$ | $-3$ | $1$ | $-12$ | $12$ |
|  | $↓$ | $4$ | $2$ | $6$ | $-12$ |
|  | $2$ | $1$ | $3$ | $-6$ | $0$ |

Therefore,

$$
\frac{2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12}{x-2}=2{x}^{3}+{x}^{2}+3x-6,
$$

which means that

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-2)(2{x}^{3}+{x}^{2}+3x-6).
$$

Now, because $(x-1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(2{x}^{3}+{x}^{2}+3x-6).$ So, we divide this quotient by $(x-1)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $2$ | $1$ | $3$ | $-6$ |
|  | $↓$ | $2$ | $3$ | $6$ |
|  | $2$ | $3$ | $6$ | $0$ |

Therefore,

$$
\frac{2{x}^{3}+{x}^{2}+3x-6}{x-1}=2{x}^{2}+3x+6,
$$

which means that

$$
\begin{aligned}2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12 & =(x-2)(x-1)(2{x}^{2}+3x+6)\end{aligned}
$$

To see whether the quadratic polynomial $2{x}^{2}+3x+6$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={3}^{2}-4(2)(6)=-39<0
$$

So, the quadratic polynomial $2{x}^{2}+3x+6$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
2{x}^{4}-3{x}^{3}+{x}^{2}-12x+12=(x-2)(x-1)\underbrace{(2{x}^{2}+3x+6)}_{P(x)}.
$$

Finally, $P(x)=2{x}^{2}+3x+6.$

---

### q-270972 — generated moderate

Find the polynomial $P(x)$ given that ${x}^{4}-14{x}^{2}-32=(x+4)(x-4)P(x).$

$P(x)=$
{{field-1}}

- ${x}^{2}+2$ **correct**

**Worked solution**

Let $f(x)={x}^{4}-14{x}^{2}-32.$ We know that $(x+4)$ and $(x-4)$ are factors of $f(x),$ and we need to find its other factors.

Because $(x+4)$ is a factor of $f(x),$ we know that $(x+4)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+4)$ using synthetic division:

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-4$ | $1$ | $0$ | $-14$ | $0$ | $-32$ |
|  | $↓$ | $-4$ | $16$ | $-8$ | $32$ |
|  | $1$ | $-4$ | $2$ | $-8$ | $0$ |

Therefore,

$$
\frac{{x}^{4}-14{x}^{2}-32}{x+4}={x}^{3}-4{x}^{2}+2x-8,
$$

which means that

$$
{x}^{4}-14{x}^{2}-32=(x+4)({x}^{3}-4{x}^{2}+2x-8).
$$

Now, because $(x-4)$ is also a factor of $f(x),$ it must be a factor of the quotient $({x}^{3}-4{x}^{2}+2x-8).$ So, we divide this quotient by $(x-4)$ using synthetic division once more:

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $4$ | $1$ | $-4$ | $2$ | $-8$ |
|  | $↓$ | $4$ | $0$ | $8$ |
|  | $1$ | $0$ | $2$ | $0$ |

Therefore,

$$
\frac{{x}^{3}-4{x}^{2}+2x-8}{x-4}={x}^{2}+2,
$$

which means that

$$
\begin{aligned}{x}^{4}-14{x}^{2}-32 & =(x+4)(x-4)({x}^{2}+2)\end{aligned}
$$

To see whether the quadratic polynomial ${x}^{2}+2$ can be factored any further, we calculate its discriminant:

$$
{b}^{2}-4ac={0}^{2}-4(1)(2)=-8<0
$$

So, the quadratic polynomial ${x}^{2}+2$ cannot be factored over the real numbers since its discriminant is negative. 

Therefore, the full factorization of $f(x)$ over the real numbers is given by 

$$
{x}^{4}-14{x}^{2}-32=(x+4)(x-4)\underbrace{({x}^{2}+2)}_{P(x)}.
$$

Finally, $P(x)={x}^{2}+2.$

---

### q-328607 — raw evidence

Find the polynomial $P(x)$ given that $-3{x}^{4}+4{x}^{3}+30{x}^{2}-7x+60=-(x+3)(x-4)P(x).$

$P(x)=$
{{field-1}}

- $3{x}^{2}-x+5$ **correct**

**Worked solution**

Let $f(x)=-3{x}^{4}+4{x}^{3}+30{x}^{2}-7x+60.$ We know that $(x+3)$ and $(x-4)$ are factors of $f(x),$ and we need to find its other factors.  

Because $(x+3)$ is a factor of $f(x),$ we know that $(x+3)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+3)$ using synthetic division:  

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-3$ | $-3$ | $4$ | $30$ | $-7$ | $60$ |
|  | $↓$ | $9$ | $-39$ | $27$ | $-60$ |
|  | $-3$ | $13$ | $-9$ | $20$ | $0$ |

Therefore,  

$$
\frac{-3{x}^{4}+4{x}^{3}+30{x}^{2}-7x+60}{x+3}=-3{x}^{3}+13{x}^{2}-9x+20,
$$

which means that  

$$
-3{x}^{4}+4{x}^{3}+30{x}^{2}-7x+60=(x+3)(-3{x}^{3}+13{x}^{2}-9x+20).
$$

Now, because $(x-4)$ is also a factor of $f(x),$ it must be a factor of the quotient $(-3{x}^{3}+13{x}^{2}-9x+20).$ So, we divide this quotient by $(x-4)$ using synthetic division once more:  

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $4$ | $-3$ | $13$ | $-9$ | $20$ |
|  | $↓$ | $-12$ | $4$ | $-20$ |
|  | $-3$ | $1$ | $-5$ | $0$ |

Therefore,  

$$
\frac{-3{x}^{3}+13{x}^{2}-9x+20}{x-4}=-3{x}^{2}+x-5,
$$

which means that  

$$
\begin{aligned}-3{x}^{4}+4{x}^{3}+30{x}^{2}-7x+60 & =(x+3)(x-4)(-3{x}^{2}+x-5) \\  & =-(x+3)(x-4)(3{x}^{2}-x+5).\end{aligned}
$$

To see whether the quadratic polynomial $3{x}^{2}-x+5$ can be factored any further, we calculate its discriminant:  

$$
{b}^{2}-4ac=(-1)^{2}-4(3)(5)=-59<0.
$$

So, the quadratic polynomial $3{x}^{2}-x+5$ cannot be factored over the real numbers since its discriminant is negative.  

Therefore, the full factorization of $f(x)$ over the real numbers is given by  

$$
-3{x}^{4}+4{x}^{3}+30{x}^{2}-7x+60=-(x+3)(x-4){{(3{x}^{2}-x+5)}_{⏟}}_{P(x)}.
$$

Finally, $P(x)=3{x}^{2}-x+5.$

---

### q-328607 — generated hard

Find the polynomial $P(x)$ given that $-3{x}^{4}+4{x}^{3}+30{x}^{2}-7x+60=-(x+3)(x-4)P(x).$

$P(x)=$
{{field-1}}

- $3{x}^{2}-x+5$ **correct**

**Worked solution**

Let $f(x)=-3{x}^{4}+4{x}^{3}+30{x}^{2}-7x+60.$ We know that $(x+3)$ and $(x-4)$ are factors of $f(x),$ and we need to find its other factors.  

Because $(x+3)$ is a factor of $f(x),$ we know that $(x+3)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+3)$ using synthetic division:  

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-3$ | $-3$ | $4$ | $30$ | $-7$ | $60$ |
|  | $↓$ | $9$ | $-39$ | $27$ | $-60$ |
|  | $-3$ | $13$ | $-9$ | $20$ | $0$ |

Therefore,  

$$
\frac{-3{x}^{4}+4{x}^{3}+30{x}^{2}-7x+60}{x+3}=-3{x}^{3}+13{x}^{2}-9x+20,
$$

which means that  

$$
-3{x}^{4}+4{x}^{3}+30{x}^{2}-7x+60=(x+3)(-3{x}^{3}+13{x}^{2}-9x+20).
$$

Now, because $(x-4)$ is also a factor of $f(x),$ it must be a factor of the quotient $(-3{x}^{3}+13{x}^{2}-9x+20).$ So, we divide this quotient by $(x-4)$ using synthetic division once more:  

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $4$ | $-3$ | $13$ | $-9$ | $20$ |
|  | $↓$ | $-12$ | $4$ | $-20$ |
|  | $-3$ | $1$ | $-5$ | $0$ |

Therefore,  

$$
\frac{-3{x}^{3}+13{x}^{2}-9x+20}{x-4}=-3{x}^{2}+x-5,
$$

which means that  

$$
\begin{aligned}-3{x}^{4}+4{x}^{3}+30{x}^{2}-7x+60 & =(x+3)(x-4)(-3{x}^{2}+x-5) \\  & =-(x+3)(x-4)(3{x}^{2}-x+5).\end{aligned}
$$

To see whether the quadratic polynomial $3{x}^{2}-x+5$ can be factored any further, we calculate its discriminant:  

$$
{b}^{2}-4ac=(-1)^{2}-4(3)(5)=-59<0.
$$

So, the quadratic polynomial $3{x}^{2}-x+5$ cannot be factored over the real numbers since its discriminant is negative.  

Therefore, the full factorization of $f(x)$ over the real numbers is given by  

$$
-3{x}^{4}+4{x}^{3}+30{x}^{2}-7x+60=-(x+3)(x-4)\underbrace{(3{x}^{2}-x+5)}_{P(x)}.
$$

Finally, $P(x)=3{x}^{2}-x+5.$

---

### q-328607 — generated hard

Find the polynomial $P(x)$ given that $-2{x}^{4}+3{x}^{3}-{x}^{2}+12x-12=-(x-2)(x-1)P(x).$

$P(x)=$
{{field-1}}

- $2{x}^{2}+3x+6$ **correct**

**Worked solution**

Let $f(x)=-2{x}^{4}+3{x}^{3}-{x}^{2}+12x-12.$ We know that $(x-2)$ and $(x-1)$ are factors of $f(x),$ and we need to find its other factors.  

Because $(x-2)$ is a factor of $f(x),$ we know that $(x-2)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x-2)$ using synthetic division:  

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $2$ | $-2$ | $3$ | $-1$ | $12$ | $-12$ |
|  | $↓$ | $-4$ | $-2$ | $-6$ | $12$ |
|  | $-2$ | $-1$ | $-3$ | $6$ | $0$ |

Therefore,  

$$
\frac{-2{x}^{4}+3{x}^{3}-{x}^{2}+12x-12}{x-2}=-2{x}^{3}-{x}^{2}-3x+6,
$$

which means that  

$$
-2{x}^{4}+3{x}^{3}-{x}^{2}+12x-12=(x-2)(-2{x}^{3}-{x}^{2}-3x+6).
$$

Now, because $(x-1)$ is also a factor of $f(x),$ it must be a factor of the quotient $(-2{x}^{3}-{x}^{2}-3x+6).$ So, we divide this quotient by $(x-1)$ using synthetic division once more:  

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $1$ | $-2$ | $-1$ | $-3$ | $6$ |
|  | $↓$ | $-2$ | $-3$ | $-6$ |
|  | $-2$ | $-3$ | $-6$ | $0$ |

Therefore,  

$$
\frac{-2{x}^{3}-{x}^{2}-3x+6}{x-1}=-2{x}^{2}-3x-6,
$$

which means that  

$$
\begin{aligned}-2{x}^{4}+3{x}^{3}-{x}^{2}+12x-12 & =(x-2)(x-1)(-2{x}^{2}-3x-6) \\  & =-(x-2)(x-1)(2{x}^{2}+3x+6).\end{aligned}
$$

To see whether the quadratic polynomial $2{x}^{2}+3x+6$ can be factored any further, we calculate its discriminant:  

$$
{b}^{2}-4ac={3}^{2}-4(2)(6)=-39<0.
$$

So, the quadratic polynomial $2{x}^{2}+3x+6$ cannot be factored over the real numbers since its discriminant is negative.  

Therefore, the full factorization of $f(x)$ over the real numbers is given by  

$$
-2{x}^{4}+3{x}^{3}-{x}^{2}+12x-12=-(x-2)(x-1)\underbrace{(2{x}^{2}+3x+6)}_{P(x)}.
$$

Finally, $P(x)=2{x}^{2}+3x+6.$

---

### q-328607 — generated hard

Find the polynomial $P(x)$ given that $-{x}^{4}+14{x}^{2}+32=-(x+4)(x-4)P(x).$

$P(x)=$
{{field-1}}

- ${x}^{2}+2$ **correct**

**Worked solution**

Let $f(x)=-{x}^{4}+14{x}^{2}+32.$ We know that $(x+4)$ and $(x-4)$ are factors of $f(x),$ and we need to find its other factors.  

Because $(x+4)$ is a factor of $f(x),$ we know that $(x+4)$ divides $f(x)$ with no remainder. So, to begin factoring $f(x),$ we can divide it by $(x+4)$ using synthetic division:  

|  | ${x}^{4}$ | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- | --- |
| $-4$ | $-1$ | $0$ | $14$ | $0$ | $32$ |
|  | $↓$ | $4$ | $-16$ | $8$ | $-32$ |
|  | $-1$ | $4$ | $-2$ | $8$ | $0$ |

Therefore,  

$$
\frac{-{x}^{4}+14{x}^{2}+32}{x+4}=-{x}^{3}+4{x}^{2}-2x+8,
$$

which means that  

$$
-{x}^{4}+14{x}^{2}+32=(x+4)(-{x}^{3}+4{x}^{2}-2x+8).
$$

Now, because $(x-4)$ is also a factor of $f(x),$ it must be a factor of the quotient $(-{x}^{3}+4{x}^{2}-2x+8).$ So, we divide this quotient by $(x-4)$ using synthetic division once more:  

|  | ${x}^{3}$ | ${x}^{2}$ | ${x}^{1}$ | ${x}^{0}$ |
| --- | --- | --- | --- | --- |
| $4$ | $-1$ | $4$ | $-2$ | $8$ |
|  | $↓$ | $-4$ | $0$ | $-8$ |
|  | $-1$ | $0$ | $-2$ | $0$ |

Therefore,  

$$
\frac{-{x}^{3}+4{x}^{2}-2x+8}{x-4}=-{x}^{2}-2,
$$

which means that  

$$
\begin{aligned}-{x}^{4}+14{x}^{2}+32 & =(x+4)(x-4)(-{x}^{2}-2) \\  & =-(x+4)(x-4)({x}^{2}+2).\end{aligned}
$$

To see whether the quadratic polynomial ${x}^{2}+2$ can be factored any further, we calculate its discriminant:  

$$
{b}^{2}-4ac={0}^{2}-4(1)(2)=-8<0.
$$

So, the quadratic polynomial ${x}^{2}+2$ cannot be factored over the real numbers since its discriminant is negative.  

Therefore, the full factorization of $f(x)$ over the real numbers is given by  

$$
-{x}^{4}+14{x}^{2}+32=-(x+4)(x-4)\underbrace{({x}^{2}+2)}_{P(x)}.
$$

Finally, $P(x)={x}^{2}+2.$
