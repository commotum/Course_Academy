## source q-103989

$\int \frac{2x-4}{x(x-4)}\,\text{d}x=$

selection: \operatorname{ln}⁡|x|-\operatorname{ln}⁡|x-4|+C, 2\operatorname{ln}⁡|x|+2\operatorname{ln}⁡|x-4|+C, \operatorname{ln}⁡|x|+2\operatorname{ln}⁡|x-4|+C, 2\operatorname{ln}⁡|x|-2\operatorname{ln}⁡|x-4|+C, \operatorname{ln}⁡|x|+\operatorname{ln}⁡|x-4|+C

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{2x-4}{x(x-4)} & =\frac{A}{x}+\frac{B}{x-4},\end{aligned}
$$

which gives

$$
2x-4=A(x-4)+Bx.
$$

Plugging in $x=4,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}2(4)-4 & =A(4-4)+B(4) \\ 4 & =4B \\ 1 & =B\end{aligned}
$$

On the other hand, plugging in $x=0,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}2(0)-4 & =A(0-4)+B(0) \\ -4 & =-4A \\ A & =1\end{aligned}
$$

Therefore,

$$
\begin{aligned}\frac{2x-4}{x(x-4)} & =\frac{1}{x}+\frac{1}{x-4}.\end{aligned}
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{2x-4}{x(x-4)}\,\text{d}x & =\int (\frac{1}{x}+\frac{1}{x-4})\text{d}x \\  & =\int \frac{1}{x}\,\text{d}x+\int \frac{1}{x-4}\,\text{d}x \\  & =\operatorname{ln}⁡|x|+\operatorname{ln}⁡|x-4|+C.\end{aligned}
$$

## source q-49903

$\int \frac{6x+12}{x(x+3)}\,\text{d}x=$

selection: 4\operatorname{ln}⁡|x|+2\operatorname{ln}⁡|x+3|+C, \frac{1}{4}\operatorname{ln}⁡|x|+2\operatorname{ln}⁡|x+3|+C, \frac{1}{4}\operatorname{ln}⁡|x|+\frac{1}{2}\operatorname{ln}⁡|x+3|+C, \operatorname{ln}⁡|x|+2\operatorname{ln}⁡|x+3|+C, 4\operatorname{ln}⁡|x|+\frac{1}{2}\operatorname{ln}⁡|x+3|+C

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{6x+12}{x(x+3)} & =\frac{A}{x}+\frac{B}{x+3},\end{aligned}
$$

which gives

$$
6x+12=A(x+3)+Bx.
$$

Plugging in $x=-3,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}6(-3)+12 & =A(-3+3)+B(-3) \\ -6 & =-3B \\ B & =2\end{aligned}
$$

On the other hand, plugging in $x=0,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}6(0)+12 & =A(0+3)+B(0) \\ 12 & =3A \\ A & =4\end{aligned}
$$

Therefore,

$$
\begin{aligned}\frac{6x+12}{x(x+3)}=\frac{4}{x}+\frac{2}{x+3}.\end{aligned}
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{6x+12}{x(x+3)}\,\text{d}x & =\int (\frac{4}{x}+\frac{2}{x+3})\text{d}x \\  & =4\int \frac{1}{x}\,\text{d}x+2\int \frac{1}{x+3}\,\text{d}x \\  & =4\operatorname{ln}⁡|x|+2\operatorname{ln}⁡|x+3|+C\end{aligned}
$$

## source q-103991

Given that

$$
\int \frac{7}{(x-1)(x+6)}\,\text{d}x=a\operatorname{ln}⁡|x-1|+b\operatorname{ln}⁡|x+6|+C,
$$

find the value of $a+b.$

selection: 2, 1, 0, -1, -2

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{7}{(x-1)(x+6)} & =\frac{A}{x-1}+\frac{B}{x+6},\end{aligned}
$$

which gives

$$
7=A(x+6)+B(x-1).
$$

Plugging in $x=-6,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}7 & =A(-6+6)+B(-6-1) \\ 7 & =-7B \\ B & =-1\end{aligned}
$$

On the other hand, plugging in $x=1,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}7 & =A(1+6)+B(1-1) \\ 7 & =7A \\ A & =1\end{aligned}
$$

Therefore,

$$
\begin{aligned}\frac{7}{(x-1)(x+6)} & =\frac{1}{x-1}-\frac{1}{x+6}.\end{aligned}
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{7}{(x-1)(x+6)}\,\text{d}x & =\int (\frac{1}{x-1}-\frac{1}{x+6})\text{d}x \\  & =\int \frac{1}{x-1}\,\text{d}x-\int \frac{1}{x+6}\,\text{d}x \\  & =\operatorname{ln}⁡|x-1|-\operatorname{ln}⁡|x+6|+C.\end{aligned}
$$

Finally, $a=1,b=-1,$ and $a+b=1-1=0.$

## source q-49604

Given that

$$
\int \frac{13}{(3x+2)(2x-3)}\,\text{d}x=a\operatorname{ln}⁡|2x-3|+b\operatorname{ln}⁡|3x+2|+C,
$$

find the value of $a+b.$

selection: 0, -2, 2, 1, -1

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{13}{(3x+2)(2x-3)} & =\frac{A}{3x+2}+\frac{B}{2x-3},\end{aligned}
$$

which gives

$$
13=A(2x-3)+B(3x+2).
$$

Plugging in $x=\frac{3}{2},$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}13 & =A(2(\frac{3}{2})-3)+B(3(\frac{3}{2})+2) \\ 13 & =\frac{13}{2}B \\ B & =2\end{aligned}
$$

On the other hand, plugging in $x=-\frac{2}{3},$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}13 & =A(2(-\frac{2}{3})-3)+B(3(-\frac{2}{3})+2) \\ 13 & =-\frac{13}{3}A \\ A & =-3\end{aligned}
$$

Therefore,

$$
\begin{aligned}\frac{13}{(3x+2)(2x-3)}=-\frac{3}{3x+2}+\frac{2}{2x-3}.\end{aligned}
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{13}{(3x+2)(2x-3)}\,\text{d}x & =\int (-\frac{3}{3x+2}+\frac{2}{2x-3})\text{d}x \\  & =-\int \frac{3}{3x+2}\,\text{d}x+\int \frac{2}{2x-3}\,\text{d}x \\  & =\operatorname{ln}⁡|2x-3|-\operatorname{ln}⁡|3x+2|+C.\end{aligned}
$$

Finally, $a=1,b=-1,$ and $a+b=1-1=0.$

## source q-49905

Given that

$$
\int \frac{5x-1}{(x-3)(2x+1)}\,\text{d}x=a\operatorname{ln}⁡|x-3|+b\operatorname{ln}⁡|2x+1|+C,
$$

find the value of $a+b.$

selection: \frac{1}{2}, \frac{3}{2}, 2, \frac{5}{2}, \frac{7}{2}

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{5x-1}{(x-3)(2x+1)} & =\frac{A}{x-3}+\frac{B}{2x+1},\end{aligned}
$$

which gives

$$
5x-1=A(2x+1)+B(x-3).
$$

Plugging in $x=-\frac{1}{2},$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}5(-\frac{1}{2})-1 & =A(2(-\frac{1}{2})+1)+B(-\frac{1}{2}-3) \\ -\frac{7}{2} & =-\frac{7}{2}B \\ B & =1\end{aligned}
$$

On the other hand, plugging in $x=3,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}5(3)-1 & =A(2(3)+1)+B(3-3) \\ 14 & =7A \\ A & =2\end{aligned}
$$

Therefore,

$$
\begin{aligned}\frac{5x-1}{(x-3)(2x+1)}=\frac{2}{x-3}+\frac{1}{2x+1}.\end{aligned}
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{5x-1}{(x-3)(2x+1)}\,\text{d}x & =\int (\frac{2}{x-3}+\frac{1}{2x+1})\text{d}x \\  & =2\int \frac{1}{x-3}\,\text{d}x+\frac{1}{2}\int \frac{2}{2x+1}\,\text{d}x \\  & =2\operatorname{ln}⁡|x-3|+\frac{1}{2}\operatorname{ln}⁡|2x+1|+C\end{aligned}
$$

Finally, $a=2,b=\frac{1}{2},$ and $a+b=2+\frac{1}{2}=\frac{5}{2}.$

## source q-103988

$\int \frac{2x+7}{(2x+1)(x+2)}\,\text{d}x=$

selection: 2\operatorname{ln}⁡|2x+1|+2\operatorname{ln}⁡|x+2|+C, 4\operatorname{ln}⁡|2x+1|+\operatorname{ln}⁡|x+2|+C, 4\operatorname{ln}⁡|2x+1|-\operatorname{ln}⁡|x+2|+C, 4\operatorname{ln}⁡|2x+1|-2\operatorname{ln}⁡|x+2|+C, 2\operatorname{ln}⁡|2x+1|-\operatorname{ln}⁡|x+2|+C

First, we convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{2x+7}{(2x+1)(x+2)} & =\frac{A}{2x+1}+\frac{B}{x+2},\end{aligned}
$$

which gives

$$
2x+7=A(x+2)+B(2x+1).
$$

Plugging in $x=-2,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}2(-2)+7 & =A((-2)+2)+B(2(-2)+1) \\ 3 & =-3B \\ B & =-1\end{aligned}
$$

On the other hand, plugging in $x=-\frac{1}{2},$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}2(-\frac{1}{2})+7 & =A(-\frac{1}{2}+2)+B(2(-\frac{1}{2})+1) \\ 6 & =A(\frac{3}{2}) \\ A & =4\end{aligned}
$$

Therefore,

$$
\begin{aligned}\frac{2x+7}{(2x+1)(x+2)} & =\frac{4}{2x+1}-\frac{1}{x+2}.\end{aligned}
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{2x+7}{(2x+1)(x+2)}\,\text{d}x & =\int (\frac{4}{2x+1}-\frac{1}{x+2})\text{d}x \\  & =4\int \frac{1}{2x+1}\,\text{d}x-\int \frac{1}{x+2}\,\text{d}x \\  & =2\operatorname{ln}⁡|2x+1|-\operatorname{ln}⁡|x+2|+C.\end{aligned}
$$

## source q-49908

$\int \frac{2}{3{x}^{2}+x}\,\text{d}x=$

selection: 2\operatorname{ln}⁡|x|+\operatorname{ln}⁡|3x+1|+C, \frac{1}{2}\operatorname{ln}⁡|x|-\operatorname{ln}⁡|3x+1|+C, \frac{1}{2}\operatorname{ln}⁡|x|+\frac{1}{2}\operatorname{ln}⁡|3x+1|+C, 2\operatorname{ln}⁡|x|-2\operatorname{ln}⁡|3x+1|+C, 2\operatorname{ln}⁡|x|-3\operatorname{ln}⁡|3x+1|+C

First, we note that the denominator of the integrand can be factored as

$$
3{x}^{2}+x=x(3x+1).
$$

We convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{2}{x(3x+1)} & =\frac{A}{x}+\frac{B}{(3x+1)},\end{aligned}
$$

which gives

$$
2=A(3x+1)+Bx.
$$

Plugging in $x=-\frac{1}{3},$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}2 & =A(3(-\frac{1}{3})+1)+B(-\frac{1}{3}) \\ 2 & =-\frac{1}{3}B \\ 6 & =-B \\ B & =-6\end{aligned}
$$

On the other hand, plugging in $x=0,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}2 & =A(3(0)+1)+B(0) \\ 2 & =A\end{aligned}
$$

Therefore

$$
\begin{aligned}\frac{2}{x(3x+1)}=\frac{2}{x}-\frac{6}{3x+1}.\end{aligned}
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{2}{x(3x+1)}\,\text{d}x & =\int (\frac{2}{x}-\frac{6}{3x+1})\,\text{d}x \\  & =2\int \frac{1}{x}\,\text{d}x-2\int \frac{3}{3x+1}\,\text{d}x \\  & =2\operatorname{ln}⁡|x|-2\operatorname{ln}⁡|3x+1|+C\end{aligned}
$$

## source q-348896

Evaluate the following indefinite integral and fill in the missing coefficients.

$\int \frac{7x+7}{(x+3)(x-4)}\,\text{d}x=$
{{field-1}}$\,\operatorname{ln}⁡|x+3|\,+\,$
{{field-2}}$\,\operatorname{ln}⁡|x-4|+C$

field-1: 2
field-2: 5

First, we note that the denominator of the integrand can be factored as

$$
(x+3)(x-4).
$$

We convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{7x+7}{(x+3)(x-4)} & =\frac{A}{x+3}+\frac{B}{x-4},\end{aligned}
$$

which gives

$$
7x+7=A(x-4)+B(x+3).
$$

Plugging in $x=4,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}7(4)+7 & =A(4-4)+B(4+3) \\ 35 & =7B \\ B & =5.\end{aligned}
$$

On the other hand, plugging in $x=-3,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}7(-3)+7 & =A(-3-4)+B(-3+3) \\ -14 & =-7A \\ A & =2.\end{aligned}
$$

Therefore,

$$
\frac{7x+7}{(x+3)(x-4)}=\frac{2}{x+3}+\frac{5}{x-4}.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{7x+7}{(x+3)(x-4)}\,\text{d}x & =2\int \frac{1}{x+3}\,\text{d}x+5\int \frac{1}{x-4}\,\text{d}x \\  & =2\,\operatorname{ln}⁡|x+3|+5\,\operatorname{ln}⁡|x-4|+C.\end{aligned}
$$

## source q-348898

Evaluate the following indefinite integral and fill in the missing coefficients.

$\int \frac{7x-11}{(x-8)(x+1)}\,\text{d}x=$
{{field-1}}$\,\operatorname{ln}⁡|x-8|\,+\,$
{{field-2}}$\,\operatorname{ln}⁡|x+1|+C$

field-1: 5
field-2: 2

First, we note that the denominator of the integrand can be factored as

$$
(x-8)(x+1).
$$

We convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{7x-11}{(x-8)(x+1)} & =\frac{A}{x-8}+\frac{B}{x+1},\end{aligned}
$$

which gives

$$
7x-11=A(x+1)+B(x-8).
$$

Plugging in $x=8,$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}7(8)-11 & =A(8+1)+B(8-8) \\ 45 & =9A \\ A & =5.\end{aligned}
$$

On the other hand, plugging in $x=-1,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}7(-1)-11 & =A(-1+1)+B(-1-8) \\ -18 & =-9B \\ B & =2.\end{aligned}
$$

Therefore,

$$
\frac{7x-11}{(x-8)(x+1)}=\frac{5}{x-8}+\frac{2}{x+1}.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{7x-11}{(x-8)(x+1)}\,\text{d}x & =5\int \frac{1}{x-8}\,\text{d}x+2\int \frac{1}{x+1}\,\text{d}x \\  & =5\,\operatorname{ln}⁡|x-8|+2\,\operatorname{ln}⁡|x+1|+C.\end{aligned}
$$

## source q-348933

Evaluate the following indefinite integral and fill in the missing coefficients.

$\int \frac{11}{(2x+5)(x-2)}\,\text{d}x=$
{{field-1}}$\,\operatorname{ln}⁡|2x+5|\,+\,$
{{field-2}}$\,\operatorname{ln}⁡|x-2|+C$

field-1: -\frac{11}{9}
field-2: \frac{11}{9}

First, we note that the denominator of the integrand can be factored as

$$
(2x+5)(x-2).
$$

We convert the integrand into a sum of partial fractions:

$$
\begin{aligned}\frac{11}{(2x+5)(x-2)} & =\frac{A}{2x+5}+\frac{B}{x-2},\end{aligned}
$$

which gives

$$
11=A(x-2)+B(2x+5).
$$

Plugging in $x=2,$ we can eliminate $A$ and solve for $B:$

$$
\begin{aligned}11 & =9B \\ B & =\frac{11}{9}.\end{aligned}
$$

On the other hand, plugging in $x=-\frac{5}{2},$ we can eliminate $B$ and solve for $A:$

$$
\begin{aligned}11 & =-\frac{9}{2}A \\ A & =-\frac{22}{9}.\end{aligned}
$$

Therefore,

$$
\frac{11}{(2x+5)(x-2)}=-\frac{22}{9(2x+5)}+\frac{11}{9(x-2)}.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{11}{(2x+5)(x-2)}\,\text{d}x & =-\frac{22}{9}\int \frac{1}{2x+5}\,\text{d}x+\frac{11}{9}\int \frac{1}{x-2}\,\text{d}x \\  & =-\frac{11}{9}\,\operatorname{ln}⁡|2x+5|+\frac{11}{9}\,\operatorname{ln}⁡|x-2|+C.\end{aligned}
$$

## variant q-103989

$\int \frac{4 x - 8}{(x)(x - 4)}\,\text{d}x=$

selection: 2\operatorname{ln}⁡|x|-2\operatorname{ln}⁡|x - 4|+C, 4\operatorname{ln}⁡|x|+4\operatorname{ln}⁡|x - 4|+C, 2\operatorname{ln}⁡|x|+4\operatorname{ln}⁡|x - 4|+C, 4\operatorname{ln}⁡|x|-4\operatorname{ln}⁡|x - 4|+C, 2\operatorname{ln}⁡|x|+2\operatorname{ln}⁡|x - 4|+C

First, we note that the denominator of the integrand can be factored as

$$
x^{2} - 4 x=(x)(x - 4).
$$

We convert the integrand into a sum of partial fractions:

$$
\frac{4 x - 8}{(x)(x - 4)}=\frac{A}{x}+\frac{B}{x - 4}.
$$

Multiplying by the denominator gives

$$
4 x - 8=A(x - 4)+B(x).
$$

Plugging in $x=4,$ we can eliminate $A$ and solve for $B$:

$$
8=4B,\qquad B=2.
$$

Plugging in $x=0,$ we can eliminate $B$ and solve for $A$:

$$
-8=-4A,\qquad A=2.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{4 x - 8}{(x)(x - 4)}\,\text{d}x&=2\int \frac{1}{x}\,\text{d}x+2\int \frac{1}{x - 4}\,\text{d}x\\&=2\operatorname{ln}⁡|x|+2\operatorname{ln}⁡|x - 4|+C\end{aligned}
$$

## variant q-49903

$\int \frac{12 x + 24}{(x)(x + 3)}\,\text{d}x=$

selection: 8\operatorname{ln}⁡|x|+4\operatorname{ln}⁡|x + 3|+C, \frac{1}{2}\operatorname{ln}⁡|x|+4\operatorname{ln}⁡|x + 3|+C, \frac{1}{2}\operatorname{ln}⁡|x|+\operatorname{ln}⁡|x + 3|+C, 2\operatorname{ln}⁡|x|+4\operatorname{ln}⁡|x + 3|+C, 8\operatorname{ln}⁡|x|+\operatorname{ln}⁡|x + 3|+C

First, we note that the denominator of the integrand can be factored as

$$
x^{2} + 3 x=(x)(x + 3).
$$

We convert the integrand into a sum of partial fractions:

$$
\frac{12 x + 24}{(x)(x + 3)}=\frac{A}{x}+\frac{B}{x + 3}.
$$

Multiplying by the denominator gives

$$
12 x + 24=A(x + 3)+B(x).
$$

Plugging in $x=-3,$ we can eliminate $A$ and solve for $B$:

$$
-12=-3B,\qquad B=4.
$$

Plugging in $x=0,$ we can eliminate $B$ and solve for $A$:

$$
24=3A,\qquad A=8.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{12 x + 24}{(x)(x + 3)}\,\text{d}x&=8\int \frac{1}{x}\,\text{d}x+4\int \frac{1}{x + 3}\,\text{d}x\\&=8\operatorname{ln}⁡|x|+4\operatorname{ln}⁡|x + 3|+C\end{aligned}
$$

## variant q-103991

Given that

$$
\int \frac{14}{(x - 1)(x + 6)}\,\text{d}x=a\operatorname{ln}⁡|x - 1|+b\operatorname{ln}⁡|x + 6|+C,
$$

find the value of $a+b.$

selection: 4, 2, 0, -2, -4

First, we note that the denominator of the integrand can be factored as

$$
x^{2} + 5 x - 6=(x - 1)(x + 6).
$$

We convert the integrand into a sum of partial fractions:

$$
\frac{14}{(x - 1)(x + 6)}=\frac{A}{x - 1}+\frac{B}{x + 6}.
$$

Multiplying by the denominator gives

$$
14=A(x + 6)+B(x - 1).
$$

Plugging in $x=-6,$ we can eliminate $A$ and solve for $B$:

$$
14=-7B,\qquad B=-2.
$$

Plugging in $x=1,$ we can eliminate $B$ and solve for $A$:

$$
14=7A,\qquad A=2.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{14}{(x - 1)(x + 6)}\,\text{d}x&=2\int \frac{1}{x - 1}\,\text{d}x-2\int \frac{1}{x + 6}\,\text{d}x\\&=2\operatorname{ln}⁡|x - 1|-2\operatorname{ln}⁡|x + 6|+C\end{aligned}
$$

Finally, $a=2,b=-2,$ and $a+b=0.$

## variant q-49604

Given that

$$
\int \frac{26}{(2 x - 3)(3 x + 2)}\,\text{d}x=a\operatorname{ln}⁡|2 x - 3|+b\operatorname{ln}⁡|3 x + 2|+C,
$$

find the value of $a+b.$

selection: 0, -4, 4, 2, -2

First, we note that the denominator of the integrand can be factored as

$$
6 x^{2} - 5 x - 6=(2 x - 3)(3 x + 2).
$$

We convert the integrand into a sum of partial fractions:

$$
\frac{26}{(2 x - 3)(3 x + 2)}=\frac{A}{2 x - 3}+\frac{B}{3 x + 2}.
$$

Multiplying by the denominator gives

$$
26=A(3 x + 2)+B(2 x - 3).
$$

Plugging in $x=- \frac{2}{3},$ we can eliminate $A$ and solve for $B$:

$$
26=- \frac{13}{3}B,\qquad B=-6.
$$

Plugging in $x=\frac{3}{2},$ we can eliminate $B$ and solve for $A$:

$$
26=\frac{13}{2}A,\qquad A=4.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{26}{(2 x - 3)(3 x + 2)}\,\text{d}x&=4\int \frac{1}{2 x - 3}\,\text{d}x-6\int \frac{1}{3 x + 2}\,\text{d}x\\&=2\operatorname{ln}⁡|2 x - 3|-2\operatorname{ln}⁡|3 x + 2|+C\end{aligned}
$$

Finally, $a=2,b=-2,$ and $a+b=0.$

## variant q-49905

Given that

$$
\int \frac{10 x - 2}{(x - 3)(2 x + 1)}\,\text{d}x=a\operatorname{ln}⁡|x - 3|+b\operatorname{ln}⁡|2 x + 1|+C,
$$

find the value of $a+b.$

selection: 1, 3, 4, 5, 7

First, we note that the denominator of the integrand can be factored as

$$
2 x^{2} - 5 x - 3=(x - 3)(2 x + 1).
$$

We convert the integrand into a sum of partial fractions:

$$
\frac{10 x - 2}{(x - 3)(2 x + 1)}=\frac{A}{x - 3}+\frac{B}{2 x + 1}.
$$

Multiplying by the denominator gives

$$
10 x - 2=A(2 x + 1)+B(x - 3).
$$

Plugging in $x=- \frac{1}{2},$ we can eliminate $A$ and solve for $B$:

$$
-7=- \frac{7}{2}B,\qquad B=2.
$$

Plugging in $x=3,$ we can eliminate $B$ and solve for $A$:

$$
28=7A,\qquad A=4.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{10 x - 2}{(x - 3)(2 x + 1)}\,\text{d}x&=4\int \frac{1}{x - 3}\,\text{d}x+2\int \frac{1}{2 x + 1}\,\text{d}x\\&=4\operatorname{ln}⁡|x - 3|+\operatorname{ln}⁡|2 x + 1|+C\end{aligned}
$$

Finally, $a=4,b=1,$ and $a+b=5.$

## variant q-103988

$\int \frac{4 x + 14}{(2 x + 1)(x + 2)}\,\text{d}x=$

selection: 4\operatorname{ln}⁡|2 x + 1|+4\operatorname{ln}⁡|x + 2|+C, 8\operatorname{ln}⁡|2 x + 1|+2\operatorname{ln}⁡|x + 2|+C, 8\operatorname{ln}⁡|2 x + 1|-2\operatorname{ln}⁡|x + 2|+C, 8\operatorname{ln}⁡|2 x + 1|-4\operatorname{ln}⁡|x + 2|+C, 4\operatorname{ln}⁡|2 x + 1|-2\operatorname{ln}⁡|x + 2|+C

First, we note that the denominator of the integrand can be factored as

$$
2 x^{2} + 5 x + 2=(2 x + 1)(x + 2).
$$

We convert the integrand into a sum of partial fractions:

$$
\frac{4 x + 14}{(2 x + 1)(x + 2)}=\frac{A}{2 x + 1}+\frac{B}{x + 2}.
$$

Multiplying by the denominator gives

$$
4 x + 14=A(x + 2)+B(2 x + 1).
$$

Plugging in $x=-2,$ we can eliminate $A$ and solve for $B$:

$$
6=-3B,\qquad B=-2.
$$

Plugging in $x=- \frac{1}{2},$ we can eliminate $B$ and solve for $A$:

$$
12=\frac{3}{2}A,\qquad A=8.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{4 x + 14}{(2 x + 1)(x + 2)}\,\text{d}x&=8\int \frac{1}{2 x + 1}\,\text{d}x-2\int \frac{1}{x + 2}\,\text{d}x\\&=4\operatorname{ln}⁡|2 x + 1|-2\operatorname{ln}⁡|x + 2|+C\end{aligned}
$$

## variant q-49908

$\int \frac{4}{3 x^{2} + x}\,\text{d}x=$

selection: 4\operatorname{ln}⁡|x|+2\operatorname{ln}⁡|3 x + 1|+C, \operatorname{ln}⁡|x|-2\operatorname{ln}⁡|3 x + 1|+C, \operatorname{ln}⁡|x|+\operatorname{ln}⁡|3 x + 1|+C, 4\operatorname{ln}⁡|x|-4\operatorname{ln}⁡|3 x + 1|+C, 4\operatorname{ln}⁡|x|-6\operatorname{ln}⁡|3 x + 1|+C

First, we note that the denominator of the integrand can be factored as

$$
3 x^{2} + x=(x)(3 x + 1).
$$

We convert the integrand into a sum of partial fractions:

$$
\frac{4}{(x)(3 x + 1)}=\frac{A}{x}+\frac{B}{3 x + 1}.
$$

Multiplying by the denominator gives

$$
4=A(3 x + 1)+B(x).
$$

Plugging in $x=- \frac{1}{3},$ we can eliminate $A$ and solve for $B$:

$$
4=- \frac{1}{3}B,\qquad B=-12.
$$

Plugging in $x=0,$ we can eliminate $B$ and solve for $A$:

$$
4=1A,\qquad A=4.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{4}{3 x^{2} + x}\,\text{d}x&=4\int \frac{1}{x}\,\text{d}x-12\int \frac{1}{3 x + 1}\,\text{d}x\\&=4\operatorname{ln}⁡|x|-4\operatorname{ln}⁡|3 x + 1|+C\end{aligned}
$$

## variant q-348896

Evaluate the following indefinite integral and fill in the missing coefficients.

$\int \frac{14 x + 14}{(x + 3)(x - 4)}\,\text{d}x=$
{{field-1}}$\,\operatorname{ln}⁡|x + 3|\,+\,$
{{field-2}}$\,\operatorname{ln}⁡|x - 4|+C$

field-1: 4
field-2: 10

First, we note that the denominator of the integrand can be factored as

$$
x^{2} - x - 12=(x + 3)(x - 4).
$$

We convert the integrand into a sum of partial fractions:

$$
\frac{14 x + 14}{(x + 3)(x - 4)}=\frac{A}{x + 3}+\frac{B}{x - 4}.
$$

Multiplying by the denominator gives

$$
14 x + 14=A(x - 4)+B(x + 3).
$$

Plugging in $x=4,$ we can eliminate $A$ and solve for $B$:

$$
70=7B,\qquad B=10.
$$

Plugging in $x=-3,$ we can eliminate $B$ and solve for $A$:

$$
-28=-7A,\qquad A=4.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{14 x + 14}{(x + 3)(x - 4)}\,\text{d}x&=4\int \frac{1}{x + 3}\,\text{d}x+10\int \frac{1}{x - 4}\,\text{d}x\\&=4\operatorname{ln}⁡|x + 3|+10\operatorname{ln}⁡|x - 4|+C\end{aligned}
$$

## variant q-348898

Evaluate the following indefinite integral and fill in the missing coefficients.

$\int \frac{14 x - 22}{(x - 8)(x + 1)}\,\text{d}x=$
{{field-1}}$\,\operatorname{ln}⁡|x - 8|\,+\,$
{{field-2}}$\,\operatorname{ln}⁡|x + 1|+C$

field-1: 10
field-2: 4

First, we note that the denominator of the integrand can be factored as

$$
x^{2} - 7 x - 8=(x - 8)(x + 1).
$$

We convert the integrand into a sum of partial fractions:

$$
\frac{14 x - 22}{(x - 8)(x + 1)}=\frac{A}{x - 8}+\frac{B}{x + 1}.
$$

Multiplying by the denominator gives

$$
14 x - 22=A(x + 1)+B(x - 8).
$$

Plugging in $x=-1,$ we can eliminate $A$ and solve for $B$:

$$
-36=-9B,\qquad B=4.
$$

Plugging in $x=8,$ we can eliminate $B$ and solve for $A$:

$$
90=9A,\qquad A=10.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{14 x - 22}{(x - 8)(x + 1)}\,\text{d}x&=10\int \frac{1}{x - 8}\,\text{d}x+4\int \frac{1}{x + 1}\,\text{d}x\\&=10\operatorname{ln}⁡|x - 8|+4\operatorname{ln}⁡|x + 1|+C\end{aligned}
$$

## variant q-348933

Evaluate the following indefinite integral and fill in the missing coefficients.

$\int \frac{22}{(2 x + 5)(x - 2)}\,\text{d}x=$
{{field-1}}$\,\operatorname{ln}⁡|2 x + 5|\,+\,$
{{field-2}}$\,\operatorname{ln}⁡|x - 2|+C$

field-1: - \frac{22}{9}
field-2: \frac{22}{9}

First, we note that the denominator of the integrand can be factored as

$$
2 x^{2} + x - 10=(2 x + 5)(x - 2).
$$

We convert the integrand into a sum of partial fractions:

$$
\frac{22}{(2 x + 5)(x - 2)}=\frac{A}{2 x + 5}+\frac{B}{x - 2}.
$$

Multiplying by the denominator gives

$$
22=A(x - 2)+B(2 x + 5).
$$

Plugging in $x=2,$ we can eliminate $A$ and solve for $B$:

$$
22=9B,\qquad B=\frac{22}{9}.
$$

Plugging in $x=- \frac{5}{2},$ we can eliminate $B$ and solve for $A$:

$$
22=- \frac{9}{2}A,\qquad A=- \frac{44}{9}.
$$

Finally, we integrate, and we get

$$
\begin{aligned}\int \frac{22}{(2 x + 5)(x - 2)}\,\text{d}x&=- \frac{44}{9}\int \frac{1}{2 x + 5}\,\text{d}x+\frac{22}{9}\int \frac{1}{x - 2}\,\text{d}x\\&=-\frac{22}{9}\operatorname{ln}⁡|2 x + 5|+\frac{22}{9}\operatorname{ln}⁡|x - 2|+C\end{aligned}
$$
