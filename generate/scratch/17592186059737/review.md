# Original and generated review

## Public raw evidence replay q-19783

Let $a = ⟨1, 2, 3x⟩$, $b = ⟨4, 3, x⟩$ and $\mid a \cdot b|= \sqrt{705}$. Find $x$.

> A calculator is required to answer this question.

- $x = ± 2$
- $x =-2, 4$
- $x = 2, 4$
- $x = ± 4$
- $x =-4, 2$

[No captured worked solution.]

## Public changed raw evidence replay q-19783

Let $a = ⟨1, 2, 6x⟩$, $b = ⟨4, 3, 2x⟩$ and $\mid a \cdot b|= \sqrt{705}$. Find $2x$.

> A calculator is required to answer this question.

- $x=1,\,2$
- $x=-1,\,2$
- $x=\pm 1$
- $x=-2,\,1$
- $x=\pm 2$

[No captured worked solution.]

## Original repaired replay q-19783

### Captured raw original

Let $a = ⟨1, 2, 3x⟩$, $b = ⟨4, 3, x⟩$ and $\mid a \cdot b|= \sqrt{705}$. Find $x$.

> A calculator is required to answer this question.

No captured solution.

Let $a = ⟨1, 2, 3x⟩$, $b = ⟨4, 3, x⟩$ and $|\,a\times b\,|= \sqrt{705}$. Find $x$.

> A calculator is required to answer this question.

- $x = \pm 2$
- $x =-2, 4$
- $x = 2, 4$
- $x = \pm 4$
- $x =-4, 2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 1 & 2 & 3x \\ 4 & 3 & x\end{aligned}| \\  & =|\begin{aligned}2 & 3x \\ 3 & x\end{aligned}|i-|\begin{aligned}1 & 3x \\ 4 & x\end{aligned}|j+|\begin{aligned}1 & 2 \\ 4 & 3\end{aligned}|k \\  & =(2\cdot (x)-3x\cdot (3))i-(1\cdot (x)-3x\cdot (4))j+(1\cdot (3)-2\cdot (4))k \\  & =(2x-(9x))i-(x-(12x))j+(3-(8))k \\  & =⟨- 7x,11x,-5⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(- 7x)^{2}+(11x)^{2}+(-5)^{2}} \\  & =\sqrt{(49x^{2})+(121x^{2})+(25)} \\  & =\sqrt{170x^{2} + 25}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{705} \\ \sqrt{170x^{2} + 25} & =\sqrt{705} \\ 170x^{2} + 25 & =705 \\ 170x^{2} - 680 & =0 \\ 170 \left(x - 2\right) \left(x + 2\right) & =0 \\ x & =-2,\,2.\end{aligned}
$$

Therefore, the solutions are $x=\pm 2.$

Checking in the original magnitude equation: $|\,a\times b\,|_{x=-2}=\sqrt{705}=\sqrt{705}$ $|\,a\times b\,|_{x=2}=\sqrt{705}=\sqrt{705}$.

## Generated changed observed recipe q-19783

Let $a = ⟨1, 2, 6x⟩$, $b = ⟨4, 3, 2x⟩$ and $|\,a\times b\,|= \sqrt{705}$. Find $2x$.

> A calculator is required to answer this question.

- $x=1,\,2$
- $x=-1,\,2$
- $x=\pm 1$
- $x=-2,\,1$
- $x=\pm 2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 1 & 2 & 6x \\ 4 & 3 & 2x\end{aligned}| \\  & =|\begin{aligned}2 & 6x \\ 3 & 2x\end{aligned}|i-|\begin{aligned}1 & 6x \\ 4 & 2x\end{aligned}|j+|\begin{aligned}1 & 2 \\ 4 & 3\end{aligned}|k \\  & =(2\cdot (2x)-6x\cdot (3))i-(1\cdot (2x)-6x\cdot (4))j+(1\cdot (3)-2\cdot (4))k \\  & =(4x-(18x))i-(2x-(24x))j+(3-(8))k \\  & =⟨- 14x,22x,-5⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(- 14x)^{2}+(22x)^{2}+(-5)^{2}} \\  & =\sqrt{(196x^{2})+(484x^{2})+(25)} \\  & =\sqrt{680x^{2} + 25}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{705} \\ \sqrt{680x^{2} + 25} & =\sqrt{705} \\ 680x^{2} + 25 & =705 \\ 680x^{2} - 680 & =0 \\ 680 \left(x - 1\right) \left(x + 1\right) & =0 \\ x & =-1,\,1.\end{aligned}
$$

Therefore, the solutions are $x=\pm 1.$

Checking in the original magnitude equation: $|\,a\times b\,|_{x=-1}=\sqrt{705}=\sqrt{705}$ $|\,a\times b\,|_{x=1}=\sqrt{705}=\sqrt{705}$.

## Public raw evidence replay q-19786

Let $a=⟨2x,1,4⟩,$ $b=⟨2,0,3⟩$ and $|\,a\times b\,|=\sqrt{13}.$ Find $x.$

- $x=\frac{4}{3}$
- $x=\pm \frac{3}{4}$
- $x=\frac{3}{4}$
- $x=\pm \frac{4}{3}$
- $x=-\frac{4}{3}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 1 & 4 \\ 2 & 0 & 3\end{aligned}| \\  & =|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|i-|\begin{aligned}2x & 4 \\ 2 & 3\end{aligned}|j+|\begin{aligned}2x & 1 \\ 2 & 0\end{aligned}|k \\  & =(3-0)i-(6x-8)j+(0-2)k \\  & =⟨3,-(6x-8),-2⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(-(6x-8))^{2}+(-2)^{2}} \\  & =\sqrt{9+36{x}^{2}-96x+64+4} \\  & =\sqrt{36{x}^{2}-96x+77}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{13} \\ \sqrt{36{x}^{2}-96x+77} & =\sqrt{13} \\ 36{x}^{2}-96x+77 & =13 \\ 36{x}^{2}-96x+64 & =0 \\ 9{x}^{2}-24x+16 & =0 \\ (3x-4)^{2} & =0 \\ 3x-4 & =0 \\ x & =\frac{4}{3}.\end{aligned}
$$

Therefore, the solution is $x=\frac{4}{3}.$

## Public changed raw evidence replay q-19786

Let $a=⟨4x,1,4⟩,$ $b=⟨2,0,3⟩$ and $|\,a\times b\,|=\sqrt{13}.$ Find $2x.$

- $x=\frac{3}{8}$
- $x=\pm \frac{3}{8}$
- $x=\frac{2}{3}$
- $x=- \frac{2}{3}$
- $x=\pm \frac{2}{3}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4x & 1 & 4 \\ 2 & 0 & 3\end{aligned}| \\  & =|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|i-|\begin{aligned}4x & 4 \\ 2 & 3\end{aligned}|j+|\begin{aligned}4x & 1 \\ 2 & 0\end{aligned}|k \\  & =(3-0)i-(12x-8)j+(0-2)k \\  & =⟨3,-(12x-8),-2⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(-(12x-8))^{2}+(-2)^{2}} \\  & =\sqrt{9+144{x}^{2}-192x+64+4} \\  & =\sqrt{144{x}^{2}-192x+77}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{13} \\ \sqrt{144{x}^{2}-192x+77} & =\sqrt{13} \\ 144{x}^{2}-192x+77 & =13 \\ 144{x}^{2}-192x+64 & =0 \\ 36{x}^{2}-48x+16 & =0 \\ (6x-4)^{2} & =0 \\ 6x-4 & =0 \\ 2x & =\frac{4}{3}.\end{aligned}
$$

Therefore, the solution is $x=\frac{2}{3}.$

## Original repaired replay q-19786

### Captured raw original

Let $a=⟨2x,1,4⟩,$ $b=⟨2,0,3⟩$ and $|\,a\times b\,|=\sqrt{13}.$ Find $x.$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 1 & 4 \\ 2 & 0 & 3\end{aligned}| \\  & =|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|i-|\begin{aligned}2x & 4 \\ 2 & 3\end{aligned}|j+|\begin{aligned}2x & 1 \\ 2 & 0\end{aligned}|k \\  & =(3-0)i-(6x-8)j+(0-2)k \\  & =⟨3,-(6x-8),-2⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(-(6x-8))^{2}+(-2)^{2}} \\  & =\sqrt{9+36{x}^{2}-96x+64+4} \\  & =\sqrt{36{x}^{2}-96x+77}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{13} \\ \sqrt{36{x}^{2}-96x+77} & =\sqrt{13} \\ 36{x}^{2}-96x+77 & =13 \\ 36{x}^{2}-96x+64 & =0 \\ 9{x}^{2}-24x+16 & =0 \\ (3x-4)^{2} & =0 \\ 3x-4 & =0 \\ x & =\frac{4}{3}.\end{aligned}
$$

Therefore, the solution is $x=\frac{4}{3}.$

Let $a=⟨2x,1,4⟩,$ $b=⟨2,0,3⟩$ and $|\,a\times b\,|=\sqrt{13}.$ Find $x.$

- $x=\frac{4}{3}$
- $x=\pm \frac{3}{4}$
- $x=\frac{3}{4}$
- $x=\pm \frac{4}{3}$
- $x=-\frac{4}{3}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 1 & 4 \\ 2 & 0 & 3\end{aligned}| \\  & =|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|i-|\begin{aligned}2x & 4 \\ 2 & 3\end{aligned}|j+|\begin{aligned}2x & 1 \\ 2 & 0\end{aligned}|k \\  & =(3-0)i-(6x-8)j+(0-2)k \\  & =⟨3,-(6x-8),-2⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(-(6x-8))^{2}+(-2)^{2}} \\  & =\sqrt{9+36{x}^{2}-96x+64+4} \\  & =\sqrt{36{x}^{2}-96x+77}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{13} \\ \sqrt{36{x}^{2}-96x+77} & =\sqrt{13} \\ 36{x}^{2}-96x+77 & =13 \\ 36{x}^{2}-96x+64 & =0 \\ 9{x}^{2}-24x+16 & =0 \\ (3x-4)^{2} & =0 \\ 3x-4 & =0 \\ x & =\frac{4}{3}.\end{aligned}
$$

Therefore, the solution is $x=\frac{4}{3}.$

## Generated changed observed recipe q-19786

Let $a=⟨4x,1,4⟩,$ $b=⟨2,0,3⟩$ and $|\,a\times b\,|=\sqrt{13}.$ Find $2x.$

- $x=\frac{3}{8}$
- $x=\pm \frac{3}{8}$
- $x=\frac{2}{3}$
- $x=- \frac{2}{3}$
- $x=\pm \frac{2}{3}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4x & 1 & 4 \\ 2 & 0 & 3\end{aligned}| \\  & =|\begin{aligned}1 & 4 \\ 0 & 3\end{aligned}|i-|\begin{aligned}4x & 4 \\ 2 & 3\end{aligned}|j+|\begin{aligned}4x & 1 \\ 2 & 0\end{aligned}|k \\  & =(3-0)i-(12x-8)j+(0-2)k \\  & =⟨3,-(12x-8),-2⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(-(12x-8))^{2}+(-2)^{2}} \\  & =\sqrt{9+144{x}^{2}-192x+64+4} \\  & =\sqrt{144{x}^{2}-192x+77}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{13} \\ \sqrt{144{x}^{2}-192x+77} & =\sqrt{13} \\ 144{x}^{2}-192x+77 & =13 \\ 144{x}^{2}-192x+64 & =0 \\ 36{x}^{2}-48x+16 & =0 \\ (6x-4)^{2} & =0 \\ 6x-4 & =0 \\ 2x & =\frac{4}{3}.\end{aligned}
$$

Therefore, the solution is $x=\frac{2}{3}.$

## Public raw evidence replay q-103540

Let $a=⟨2x,3,2⟩$, $b=⟨x,1,-1⟩$ and $|\,a\times b\,|=\sqrt{93}.$ Find $x.$

- $x=\pm 4$
- $x=4$
- $x=-2,4$
- $x=\pm 2$
- $x=-4,2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 3 & 2 \\ x & 1 & -1\end{aligned}| \\  & =|\begin{aligned}3 & 2 \\ 1 & -1\end{aligned}|i-|\begin{aligned}2x & 2 \\ x & -1\end{aligned}|j+|\begin{aligned}2x & 3 \\ x & 1\end{aligned}|k \\  & =(-3-2)i-(-2x-2x)j+(2x-3x)k \\  & =⟨-5,-4x,x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-5)^{2}+(-4x)^{2}+{x}^{2}} \\  & =\sqrt{25+16{x}^{2}+{x}^{2}} \\  & =\sqrt{17{x}^{2}+25}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{93} \\ \sqrt{17{x}^{2}+25} & =\sqrt{93} \\ 17{x}^{2}+25 & =93 \\ 17{x}^{2} & =68 \\ {x}^{2} & =4.\end{aligned}
$$

Therefore, the solutions are $x=\pm 2.$

## Public changed raw evidence replay q-103540

Let $a=⟨4x,3,2⟩$, $b=⟨2x,1,-1⟩$ and $|\,a\times b\,|=\sqrt{93}.$ Find $2x.$

- $x=-1,\,2$
- $x=2$
- $x=\pm 2$
- $x=-2,\,1$
- $x=\pm 1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4x & 3 & 2 \\ 2x & 1 & -1\end{aligned}| \\  & =|\begin{aligned}3 & 2 \\ 1 & -1\end{aligned}|i-|\begin{aligned}4x & 2 \\ 2x & -1\end{aligned}|j+|\begin{aligned}4x & 3 \\ 2x & 1\end{aligned}|k \\  & =(-3-2)i-(-4x-4x)j+(4x-6x)k \\  & =⟨-5,-8x,2x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-5)^{2}+(-8x)^{2}+4{x}^{2}} \\  & =\sqrt{25+64{x}^{2}+4{x}^{2}} \\  & =\sqrt{68{x}^{2}+25}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{93} \\ \sqrt{68{x}^{2}+25} & =\sqrt{93} \\ 68{x}^{2}+25 & =93 \\ 68{x}^{2} & =68 \\ 4{x}^{2} & =4.\end{aligned}
$$

Therefore, the solutions are $x=\pm 1.$

## Original repaired replay q-103540

### Captured raw original

Let $a=⟨2x,3,2⟩$, $b=⟨x,1,-1⟩$ and $|\,a\times b\,|=\sqrt{93}.$ Find $x.$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 3 & 2 \\ x & 1 & -1\end{aligned}| \\  & =|\begin{aligned}3 & 2 \\ 1 & -1\end{aligned}|i-|\begin{aligned}2x & 2 \\ x & -1\end{aligned}|j+|\begin{aligned}2x & 3 \\ x & 1\end{aligned}|k \\  & =(-3-2)i-(-2x-2x)j+(2x-3x)k \\  & =⟨-5,-4x,x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-5)^{2}+(-4x)^{2}+{x}^{2}} \\  & =\sqrt{25+16{x}^{2}+{x}^{2}} \\  & =\sqrt{17{x}^{2}+25}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{93} \\ \sqrt{17{x}^{2}+25} & =\sqrt{93} \\ 17{x}^{2}+25 & =93 \\ 17{x}^{2} & =68 \\ {x}^{2} & =4.\end{aligned}
$$

Therefore, the solutions are $x=\pm 2.$

Let $a=⟨2x,3,2⟩$, $b=⟨x,1,-1⟩$ and $|\,a\times b\,|=\sqrt{93}.$ Find $x.$

- $x=\pm 4$
- $x=4$
- $x=-2,4$
- $x=\pm 2$
- $x=-4,2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 3 & 2 \\ x & 1 & -1\end{aligned}| \\  & =|\begin{aligned}3 & 2 \\ 1 & -1\end{aligned}|i-|\begin{aligned}2x & 2 \\ x & -1\end{aligned}|j+|\begin{aligned}2x & 3 \\ x & 1\end{aligned}|k \\  & =(-3-2)i-(-2x-2x)j+(2x-3x)k \\  & =⟨-5,4x,-x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-5)^{2}+(4x)^{2}+(-x)^{2}} \\  & =\sqrt{25+16{x}^{2}+{x}^{2}} \\  & =\sqrt{17{x}^{2}+25}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{93} \\ \sqrt{17{x}^{2}+25} & =\sqrt{93} \\ 17{x}^{2}+25 & =93 \\ 17{x}^{2} & =68 \\ {x}^{2} & =4.\end{aligned}
$$

Therefore, the solutions are $x=\pm 2.$

## Generated changed observed recipe q-103540

Let $a=⟨4x,3,2⟩$, $b=⟨2x,1,-1⟩$ and $|\,a\times b\,|=\sqrt{93}.$ Find $2x.$

- $x=-1,\,2$
- $x=2$
- $x=\pm 2$
- $x=-2,\,1$
- $x=\pm 1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4x & 3 & 2 \\ 2x & 1 & -1\end{aligned}| \\  & =|\begin{aligned}3 & 2 \\ 1 & -1\end{aligned}|i-|\begin{aligned}4x & 2 \\ 2x & -1\end{aligned}|j+|\begin{aligned}4x & 3 \\ 2x & 1\end{aligned}|k \\  & =(-3-2)i-(-4x-4x)j+(4x-6x)k \\  & =⟨-5,8x,-2x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-5)^{2}+(8x)^{2}+(-2x)^{2}} \\  & =\sqrt{25+64{x}^{2}+4{x}^{2}} \\  & =\sqrt{68{x}^{2}+25}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{93} \\ \sqrt{68{x}^{2}+25} & =\sqrt{93} \\ 68{x}^{2}+25 & =93 \\ 68{x}^{2} & =68 \\ 4{x}^{2} & =4.\end{aligned}
$$

Therefore, the solutions are $x=\pm 1.$

## Public raw evidence replay q-103541

Let $a=⟨-3,2,0⟩,$ $b=⟨2,-4,2x⟩$ and $|\,a\times b\,|=\sqrt{77}.$ Find $x.$

- $x=\pm 2$
- $x=\pm \frac{1}{4}$
- $x=2,4$
- $x=\pm \frac{1}{2}$
- $x=\pm 4$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -3 & 2 & 0 \\ 2 & -4 & 2x\end{aligned}| \\  & =|\begin{aligned}2 & 0 \\ -4 & 2x\end{aligned}|i-|\begin{aligned}-3 & 0 \\ 2 & 2x\end{aligned}|j+|\begin{aligned}-3 & 2 \\ 2 & -4\end{aligned}|k \\  & =(4x-0)i-(-6x-0)j+(12-4)k \\  & =⟨4x,6x,8⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(4x)^{2}+(6x)^{2}+(8)^{2}} \\  & =\sqrt{16{x}^{2}+36{x}^{2}+64} \\  & =\sqrt{52{x}^{2}+64}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{77} \\ \sqrt{52{x}^{2}+64} & =\sqrt{77} \\ 52{x}^{2}+64 & =77 \\ 52{x}^{2} & =13 \\ {x}^{2} & =\frac{1}{4}.\end{aligned}
$$

Therefore, the solutions are $x=\pm \frac{1}{2}.$

## Public changed raw evidence replay q-103541

Let $a=⟨-3,2,0⟩,$ $b=⟨2,-4,4x⟩$ and $|\,a\times b\,|=\sqrt{77}.$ Find $2x.$

- $x=1,\,2$
- $x=\pm \frac{1}{8}$
- $x=\pm 1$
- $x=\pm 2$
- $x=\pm \frac{1}{4}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -3 & 2 & 0 \\ 2 & -4 & 4x\end{aligned}| \\  & =|\begin{aligned}2 & 0 \\ -4 & 4x\end{aligned}|i-|\begin{aligned}-3 & 0 \\ 2 & 4x\end{aligned}|j+|\begin{aligned}-3 & 2 \\ 2 & -4\end{aligned}|k \\  & =(8x-0)i-(-12x-0)j+(12-4)k \\  & =⟨8x,12x,8⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(8x)^{2}+(12x)^{2}+(8)^{2}} \\  & =\sqrt{64{x}^{2}+144{x}^{2}+64} \\  & =\sqrt{208{x}^{2}+64}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{77} \\ \sqrt{208{x}^{2}+64} & =\sqrt{77} \\ 208{x}^{2}+64 & =77 \\ 208{x}^{2} & =13 \\ 4{x}^{2} & =\frac{1}{4}.\end{aligned}
$$

Therefore, the solutions are $x=\pm \frac{1}{4}.$

## Original repaired replay q-103541

### Captured raw original

Let $a=⟨-3,2,0⟩,$ $b=⟨2,-4,2x⟩$ and $|\,a\times b\,|=\sqrt{77}.$ Find $x.$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -3 & 2 & 0 \\ 2 & -4 & 2x\end{aligned}| \\  & =|\begin{aligned}2 & 0 \\ -4 & 2x\end{aligned}|i-|\begin{aligned}-3 & 0 \\ 2 & 2x\end{aligned}|j+|\begin{aligned}-3 & 2 \\ 2 & -4\end{aligned}|k \\  & =(4x-0)i-(-6x-0)j+(12-4)k \\  & =⟨4x,6x,8⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(4x)^{2}+(6x)^{2}+(8)^{2}} \\  & =\sqrt{16{x}^{2}+36{x}^{2}+64} \\  & =\sqrt{52{x}^{2}+64}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{77} \\ \sqrt{52{x}^{2}+64} & =\sqrt{77} \\ 52{x}^{2}+64 & =77 \\ 52{x}^{2} & =13 \\ {x}^{2} & =\frac{1}{4}.\end{aligned}
$$

Therefore, the solutions are $x=\pm \frac{1}{2}.$

Let $a=⟨-3,2,0⟩,$ $b=⟨2,-4,2x⟩$ and $|\,a\times b\,|=\sqrt{77}.$ Find $x.$

- $x=\pm 2$
- $x=\pm \frac{1}{4}$
- $x=2,4$
- $x=\pm \frac{1}{2}$
- $x=\pm 4$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -3 & 2 & 0 \\ 2 & -4 & 2x\end{aligned}| \\  & =|\begin{aligned}2 & 0 \\ -4 & 2x\end{aligned}|i-|\begin{aligned}-3 & 0 \\ 2 & 2x\end{aligned}|j+|\begin{aligned}-3 & 2 \\ 2 & -4\end{aligned}|k \\  & =(4x-0)i-(-6x-0)j+(12-4)k \\  & =⟨4x,6x,8⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(4x)^{2}+(6x)^{2}+(8)^{2}} \\  & =\sqrt{16{x}^{2}+36{x}^{2}+64} \\  & =\sqrt{52{x}^{2}+64}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{77} \\ \sqrt{52{x}^{2}+64} & =\sqrt{77} \\ 52{x}^{2}+64 & =77 \\ 52{x}^{2} & =13 \\ {x}^{2} & =\frac{1}{4}.\end{aligned}
$$

Therefore, the solutions are $x=\pm \frac{1}{2}.$

## Generated changed observed recipe q-103541

Let $a=⟨-3,2,0⟩,$ $b=⟨2,-4,4x⟩$ and $|\,a\times b\,|=\sqrt{77}.$ Find $2x.$

- $x=1,\,2$
- $x=\pm \frac{1}{8}$
- $x=\pm 1$
- $x=\pm 2$
- $x=\pm \frac{1}{4}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -3 & 2 & 0 \\ 2 & -4 & 4x\end{aligned}| \\  & =|\begin{aligned}2 & 0 \\ -4 & 4x\end{aligned}|i-|\begin{aligned}-3 & 0 \\ 2 & 4x\end{aligned}|j+|\begin{aligned}-3 & 2 \\ 2 & -4\end{aligned}|k \\  & =(8x-0)i-(-12x-0)j+(12-4)k \\  & =⟨8x,12x,8⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(8x)^{2}+(12x)^{2}+(8)^{2}} \\  & =\sqrt{64{x}^{2}+144{x}^{2}+64} \\  & =\sqrt{208{x}^{2}+64}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{77} \\ \sqrt{208{x}^{2}+64} & =\sqrt{77} \\ 208{x}^{2}+64 & =77 \\ 208{x}^{2} & =13 \\ 4{x}^{2} & =\frac{1}{4}.\end{aligned}
$$

Therefore, the solutions are $x=\pm \frac{1}{4}.$

## Public raw evidence replay q-103542

Let $a=⟨-1,2x,3⟩,$ $b=⟨2,-x,1⟩$ and $|\,a\times b\,|=\sqrt{355}.$ Find $x.$

- $x=\pm 9$
- $x=\pm 3$
- $x=-3,9$
- $x=\pm \frac{1}{3}$
- $x=-\frac{1}{3},3$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -1 & 2x & 3 \\ 2 & -x & 1\end{aligned}| \\  & =|\begin{aligned}2x & 3 \\ -x & 1\end{aligned}|i-|\begin{aligned}-1 & 3 \\ 2 & 1\end{aligned}|j+|\begin{aligned}-1 & 2x \\ 2 & -x\end{aligned}|k \\  & =(2x+3x)i-(-1-6)j+(x-4x)k \\  & =⟨5x,7,-3x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(5x)^{2}+(7)^{2}+(-3x)^{2}} \\  & =\sqrt{25{x}^{2}+49+9{x}^{2}} \\  & =\sqrt{34{x}^{2}+49}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{355} \\ \sqrt{34{x}^{2}+49} & =\sqrt{355} \\ 34{x}^{2}+49 & =355 \\ 34{x}^{2} & =306 \\ {x}^{2} & =9.\end{aligned}
$$

Therefore, the solutions are $x=\pm 3.$

## Public changed raw evidence replay q-103542

Let $a=⟨-1,4x,3⟩,$ $b=⟨2,-2x,1⟩$ and $|\,a\times b\,|=\sqrt{355}.$ Find $2x.$

- $x=- \frac{3}{2},\,\frac{9}{2}$
- $x=\pm \frac{3}{2}$
- $x=\pm \frac{9}{2}$
- $x=- \frac{1}{6},\,\frac{3}{2}$
- $x=\pm \frac{1}{6}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -1 & 4x & 3 \\ 2 & -2x & 1\end{aligned}| \\  & =|\begin{aligned}4x & 3 \\ -2x & 1\end{aligned}|i-|\begin{aligned}-1 & 3 \\ 2 & 1\end{aligned}|j+|\begin{aligned}-1 & 4x \\ 2 & -2x\end{aligned}|k \\  & =(4x+6x)i-(-1-6)j+(2x-8x)k \\  & =⟨10x,7,-6x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(10x)^{2}+(7)^{2}+(-6x)^{2}} \\  & =\sqrt{100{x}^{2}+49+36{x}^{2}} \\  & =\sqrt{136{x}^{2}+49}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{355} \\ \sqrt{136{x}^{2}+49} & =\sqrt{355} \\ 136{x}^{2}+49 & =355 \\ 136{x}^{2} & =306 \\ 4{x}^{2} & =9.\end{aligned}
$$

Therefore, the solutions are $x=\pm \frac{3}{2}.$

## Original repaired replay q-103542

### Captured raw original

Let $a=⟨-1,2x,3⟩,$ $b=⟨2,-x,1⟩$ and $|\,a\times b\,|=\sqrt{355}.$ Find $x.$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -1 & 2x & 3 \\ 2 & -x & 1\end{aligned}| \\  & =|\begin{aligned}2x & 3 \\ -x & 1\end{aligned}|i-|\begin{aligned}-1 & 3 \\ 2 & 1\end{aligned}|j+|\begin{aligned}-1 & 2x \\ 2 & -x\end{aligned}|k \\  & =(2x+3x)i-(-1-6)j+(x-4x)k \\  & =⟨5x,7,-3x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(5x)^{2}+(7)^{2}+(-3x)^{2}} \\  & =\sqrt{25{x}^{2}+49+9{x}^{2}} \\  & =\sqrt{34{x}^{2}+49}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{355} \\ \sqrt{34{x}^{2}+49} & =\sqrt{355} \\ 34{x}^{2}+49 & =355 \\ 34{x}^{2} & =306 \\ {x}^{2} & =9.\end{aligned}
$$

Therefore, the solutions are $x=\pm 3.$

Let $a=⟨-1,2x,3⟩,$ $b=⟨2,-x,1⟩$ and $|\,a\times b\,|=\sqrt{355}.$ Find $x.$

- $x=\pm 9$
- $x=\pm 3$
- $x=-3,9$
- $x=\pm \frac{1}{3}$
- $x=-\frac{1}{3},3$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -1 & 2x & 3 \\ 2 & -x & 1\end{aligned}| \\  & =|\begin{aligned}2x & 3 \\ -x & 1\end{aligned}|i-|\begin{aligned}-1 & 3 \\ 2 & 1\end{aligned}|j+|\begin{aligned}-1 & 2x \\ 2 & -x\end{aligned}|k \\  & =(2x+3x)i-(-1-6)j+(x-4x)k \\  & =⟨5x,7,-3x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(5x)^{2}+(7)^{2}+(-3x)^{2}} \\  & =\sqrt{25{x}^{2}+49+9{x}^{2}} \\  & =\sqrt{34{x}^{2}+49}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{355} \\ \sqrt{34{x}^{2}+49} & =\sqrt{355} \\ 34{x}^{2}+49 & =355 \\ 34{x}^{2} & =306 \\ {x}^{2} & =9.\end{aligned}
$$

Therefore, the solutions are $x=\pm 3.$

## Generated changed observed recipe q-103542

Let $a=⟨-1,4x,3⟩,$ $b=⟨2,-2x,1⟩$ and $|\,a\times b\,|=\sqrt{355}.$ Find $2x.$

- $x=- \frac{3}{2},\,\frac{9}{2}$
- $x=\pm \frac{3}{2}$
- $x=\pm \frac{9}{2}$
- $x=- \frac{1}{6},\,\frac{3}{2}$
- $x=\pm \frac{1}{6}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -1 & 4x & 3 \\ 2 & -2x & 1\end{aligned}| \\  & =|\begin{aligned}4x & 3 \\ -2x & 1\end{aligned}|i-|\begin{aligned}-1 & 3 \\ 2 & 1\end{aligned}|j+|\begin{aligned}-1 & 4x \\ 2 & -2x\end{aligned}|k \\  & =(4x+6x)i-(-1-6)j+(2x-8x)k \\  & =⟨10x,7,-6x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(10x)^{2}+(7)^{2}+(-6x)^{2}} \\  & =\sqrt{100{x}^{2}+49+36{x}^{2}} \\  & =\sqrt{136{x}^{2}+49}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{355} \\ \sqrt{136{x}^{2}+49} & =\sqrt{355} \\ 136{x}^{2}+49 & =355 \\ 136{x}^{2} & =306 \\ 4{x}^{2} & =9.\end{aligned}
$$

Therefore, the solutions are $x=\pm \frac{3}{2}.$

## Public raw evidence replay q-103547

Let $a=⟨4,x,3⟩,$ $b=⟨-2,3,0⟩$ and $|\,a\times b\,|=\sqrt{181}.$ Find $x.$

- $x=\pm 2$
- $x=-4,\,5$
- $x=-5,\,4$
- $x=-10,\,-2$
- $x=4,\,10$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4 & x & 3 \\ -2 & 3 & 0\end{aligned}| \\  & =|\begin{aligned}x & 3 \\ 3 & 0\end{aligned}|i-|\begin{aligned}4 & 3 \\ -2 & 0\end{aligned}|j+|\begin{aligned}4 & x \\ -2 & 3\end{aligned}|k \\  & =(0-9)i-(0+6)j+(12+2x)k \\  & =⟨-9,-6,12+2x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-9)^{2}+(-6)^{2}+(12+2x)^{2}} \\  & =\sqrt{81+36+144+48x+4{x}^{2}} \\  & =\sqrt{261+48x+4{x}^{2}}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{181} \\ \sqrt{261+48x+4{x}^{2}} & =\sqrt{181} \\ 261+48x+4{x}^{2} & =181 \\ 4{x}^{2}+48x+80 & =0 \\ {x}^{2}+12x+20 & =0 \\ (x+10)(x+2) & =0.\end{aligned}
$$

Therefore, the solutions are $x=-10,\,-2.$

## Public changed raw evidence replay q-103547

Let $a=⟨4,2x,3⟩,$ $b=⟨-2,3,0⟩$ and $|\,a\times b\,|=\sqrt{181}.$ Find $2x.$

- $x=- \frac{5}{2},\,2$
- $x=-2,\,\frac{5}{2}$
- $x=\pm 1$
- $x=2,\,5$
- $x=-5,\,-1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4 & 2x & 3 \\ -2 & 3 & 0\end{aligned}| \\  & =|\begin{aligned}2x & 3 \\ 3 & 0\end{aligned}|i-|\begin{aligned}4 & 3 \\ -2 & 0\end{aligned}|j+|\begin{aligned}4 & 2x \\ -2 & 3\end{aligned}|k \\  & =(0-9)i-(0+6)j+(12+4x)k \\  & =⟨-9,-6,12+4x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-9)^{2}+(-6)^{2}+(12+4x)^{2}} \\  & =\sqrt{81+36+144+96x+16{x}^{2}} \\  & =\sqrt{261+96x+16{x}^{2}}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{181} \\ \sqrt{261+96x+16{x}^{2}} & =\sqrt{181} \\ 261+96x+16{x}^{2} & =181 \\ 16{x}^{2}+96x+80 & =0 \\ 4{x}^{2}+24x+20 & =0 \\ (2x+10)(2x+2) & =0.\end{aligned}
$$

Therefore, the solutions are $x=-5,\,-1.$

## Original repaired replay q-103547

### Captured raw original

Let $a=⟨4,x,3⟩,$ $b=⟨-2,3,0⟩$ and $|\,a\times b\,|=\sqrt{181}.$ Find $x.$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4 & x & 3 \\ -2 & 3 & 0\end{aligned}| \\  & =|\begin{aligned}x & 3 \\ 3 & 0\end{aligned}|i-|\begin{aligned}4 & 3 \\ -2 & 0\end{aligned}|j+|\begin{aligned}4 & x \\ -2 & 3\end{aligned}|k \\  & =(0-9)i-(0+6)j+(12+2x)k \\  & =⟨-9,-6,12+2x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-9)^{2}+(-6)^{2}+(12+2x)^{2}} \\  & =\sqrt{81+36+144+48x+4{x}^{2}} \\  & =\sqrt{261+48x+4{x}^{2}}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{181} \\ \sqrt{261+48x+4{x}^{2}} & =\sqrt{181} \\ 261+48x+4{x}^{2} & =181 \\ 4{x}^{2}+48x+80 & =0 \\ {x}^{2}+12x+20 & =0 \\ (x+10)(x+2) & =0.\end{aligned}
$$

Therefore, the solutions are $x=-10,\,-2.$

Let $a=⟨4,x,3⟩,$ $b=⟨-2,3,0⟩$ and $|\,a\times b\,|=\sqrt{181}.$ Find $x.$

- $x=\pm 2$
- $x=-4,\,5$
- $x=-5,\,4$
- $x=-10,\,-2$
- $x=4,\,10$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4 & x & 3 \\ -2 & 3 & 0\end{aligned}| \\  & =|\begin{aligned}x & 3 \\ 3 & 0\end{aligned}|i-|\begin{aligned}4 & 3 \\ -2 & 0\end{aligned}|j+|\begin{aligned}4 & x \\ -2 & 3\end{aligned}|k \\  & =(0-9)i-(0+6)j+(12+2x)k \\  & =⟨-9,-6,12+2x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-9)^{2}+(-6)^{2}+(12+2x)^{2}} \\  & =\sqrt{81+36+144+48x+4{x}^{2}} \\  & =\sqrt{261+48x+4{x}^{2}}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{181} \\ \sqrt{261+48x+4{x}^{2}} & =\sqrt{181} \\ 261+48x+4{x}^{2} & =181 \\ 4{x}^{2}+48x+80 & =0 \\ {x}^{2}+12x+20 & =0 \\ (x+10)(x+2) & =0.\end{aligned}
$$

Therefore, the solutions are $x=-10,\,-2.$

## Generated changed observed recipe q-103547

Let $a=⟨4,2x,3⟩,$ $b=⟨-2,3,0⟩$ and $|\,a\times b\,|=\sqrt{181}.$ Find $2x.$

- $x=- \frac{5}{2},\,2$
- $x=-2,\,\frac{5}{2}$
- $x=\pm 1$
- $x=2,\,5$
- $x=-5,\,-1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4 & 2x & 3 \\ -2 & 3 & 0\end{aligned}| \\  & =|\begin{aligned}2x & 3 \\ 3 & 0\end{aligned}|i-|\begin{aligned}4 & 3 \\ -2 & 0\end{aligned}|j+|\begin{aligned}4 & 2x \\ -2 & 3\end{aligned}|k \\  & =(0-9)i-(0+6)j+(12+4x)k \\  & =⟨-9,-6,12+4x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-9)^{2}+(-6)^{2}+(12+4x)^{2}} \\  & =\sqrt{81+36+144+96x+16{x}^{2}} \\  & =\sqrt{261+96x+16{x}^{2}}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{181} \\ \sqrt{261+96x+16{x}^{2}} & =\sqrt{181} \\ 261+96x+16{x}^{2} & =181 \\ 16{x}^{2}+96x+80 & =0 \\ 4{x}^{2}+24x+20 & =0 \\ (2x+10)(2x+2) & =0.\end{aligned}
$$

Therefore, the solutions are $x=-5,\,-1.$

## Public raw evidence replay q-103549

Let $a=⟨0,3,4⟩,$ $b=⟨-1,-x,2⟩$ and $|\,a\times b\,|=\sqrt{221}.$ Find $x.$

- $x=-2,\,1$
- $x=-1,\,10$
- $x=\pm 10$
- $x=\pm 1$
- $x=-5,\,2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 0 & 3 & 4 \\ -1 & -x & 2\end{aligned}| \\  & =|\begin{aligned}3 & 4 \\ -x & 2\end{aligned}|i-|\begin{aligned}0 & 4 \\ -1 & 2\end{aligned}|j+|\begin{aligned}0 & 3 \\ -1 & -x\end{aligned}|k \\  & =(6+4x)i-(0+4)j+(0+3)k \\  & =⟨6+4x,-4,3⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(6+4x)^{2}+(-4)^{2}+(3)^{2}} \\  & =\sqrt{36+48x+16{x}^{2}+16+9} \\  & =\sqrt{61+48x+16{x}^{2}}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{221} \\ \sqrt{61+48x+16{x}^{2}} & =\sqrt{221} \\ 61+48x+16{x}^{2} & =221 \\ 16{x}^{2}+48x-160 & =0 \\ {x}^{2}+3x-10 & =0 \\ (x+5)(x-2) & =0.\end{aligned}
$$

Therefore, the solutions are $x=-5,\,2.$

## Public changed raw evidence replay q-103549

Let $a=⟨0,3,4⟩,$ $b=⟨-1,-2x,2⟩$ and $|\,a\times b\,|=\sqrt{221}.$ Find $2x.$

- $x=\pm 5$
- $x=- \frac{1}{2},\,5$
- $x=-1,\,\frac{1}{2}$
- $x=- \frac{5}{2},\,1$
- $x=\pm \frac{1}{2}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 0 & 3 & 4 \\ -1 & -2x & 2\end{aligned}| \\  & =|\begin{aligned}3 & 4 \\ -2x & 2\end{aligned}|i-|\begin{aligned}0 & 4 \\ -1 & 2\end{aligned}|j+|\begin{aligned}0 & 3 \\ -1 & -2x\end{aligned}|k \\  & =(6+8x)i-(0+4)j+(0+3)k \\  & =⟨6+8x,-4,3⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(6+8x)^{2}+(-4)^{2}+(3)^{2}} \\  & =\sqrt{36+96x+64{x}^{2}+16+9} \\  & =\sqrt{61+96x+64{x}^{2}}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{221} \\ \sqrt{61+96x+64{x}^{2}} & =\sqrt{221} \\ 61+96x+64{x}^{2} & =221 \\ 64{x}^{2}+96x-160 & =0 \\ 4{x}^{2}+6x-10 & =0 \\ (2x+5)(2x-2) & =0.\end{aligned}
$$

Therefore, the solutions are $x=- \frac{5}{2},\,1.$

## Original repaired replay q-103549

### Captured raw original

Let $a=⟨0,3,4⟩,$ $b=⟨-1,-x,2⟩$ and $|\,a\times b\,|=\sqrt{221}.$ Find $x.$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 0 & 3 & 4 \\ -1 & -x & 2\end{aligned}| \\  & =|\begin{aligned}3 & 4 \\ -x & 2\end{aligned}|i-|\begin{aligned}0 & 4 \\ -1 & 2\end{aligned}|j+|\begin{aligned}0 & 3 \\ -1 & -x\end{aligned}|k \\  & =(6+4x)i-(0+4)j+(0+3)k \\  & =⟨6+4x,-4,3⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(6+4x)^{2}+(-4)^{2}+(3)^{2}} \\  & =\sqrt{36+48x+16{x}^{2}+16+9} \\  & =\sqrt{61+48x+16{x}^{2}}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{221} \\ \sqrt{61+48x+16{x}^{2}} & =\sqrt{221} \\ 61+48x+16{x}^{2} & =221 \\ 16{x}^{2}+48x-160 & =0 \\ {x}^{2}+3x-10 & =0 \\ (x+5)(x-2) & =0.\end{aligned}
$$

Therefore, the solutions are $x=-5,\,2.$

Let $a=⟨0,3,4⟩,$ $b=⟨-1,-x,2⟩$ and $|\,a\times b\,|=\sqrt{221}.$ Find $x.$

- $x=-2,\,1$
- $x=-1,\,10$
- $x=\pm 10$
- $x=\pm 1$
- $x=-5,\,2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 0 & 3 & 4 \\ -1 & -x & 2\end{aligned}| \\  & =|\begin{aligned}3 & 4 \\ -x & 2\end{aligned}|i-|\begin{aligned}0 & 4 \\ -1 & 2\end{aligned}|j+|\begin{aligned}0 & 3 \\ -1 & -x\end{aligned}|k \\  & =(6+4x)i-(0+4)j+(0+3)k \\  & =⟨6+4x,-4,3⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(6+4x)^{2}+(-4)^{2}+(3)^{2}} \\  & =\sqrt{36+48x+16{x}^{2}+16+9} \\  & =\sqrt{61+48x+16{x}^{2}}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{221} \\ \sqrt{61+48x+16{x}^{2}} & =\sqrt{221} \\ 61+48x+16{x}^{2} & =221 \\ 16{x}^{2}+48x-160 & =0 \\ {x}^{2}+3x-10 & =0 \\ (x+5)(x-2) & =0.\end{aligned}
$$

Therefore, the solutions are $x=-5,\,2.$

## Generated changed observed recipe q-103549

Let $a=⟨0,3,4⟩,$ $b=⟨-1,-2x,2⟩$ and $|\,a\times b\,|=\sqrt{221}.$ Find $2x.$

- $x=\pm 5$
- $x=- \frac{1}{2},\,5$
- $x=-1,\,\frac{1}{2}$
- $x=- \frac{5}{2},\,1$
- $x=\pm \frac{1}{2}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 0 & 3 & 4 \\ -1 & -2x & 2\end{aligned}| \\  & =|\begin{aligned}3 & 4 \\ -2x & 2\end{aligned}|i-|\begin{aligned}0 & 4 \\ -1 & 2\end{aligned}|j+|\begin{aligned}0 & 3 \\ -1 & -2x\end{aligned}|k \\  & =(6+8x)i-(0+4)j+(0+3)k \\  & =⟨6+8x,-4,3⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(6+8x)^{2}+(-4)^{2}+(3)^{2}} \\  & =\sqrt{36+96x+64{x}^{2}+16+9} \\  & =\sqrt{61+96x+64{x}^{2}}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{221} \\ \sqrt{61+96x+64{x}^{2}} & =\sqrt{221} \\ 61+96x+64{x}^{2} & =221 \\ 64{x}^{2}+96x-160 & =0 \\ 4{x}^{2}+6x-10 & =0 \\ (2x+5)(2x-2) & =0.\end{aligned}
$$

Therefore, the solutions are $x=- \frac{5}{2},\,1.$

## Public raw evidence replay q-103552

Let $a=⟨0,-2,3⟩,$ $b=⟨-2,1,-2x⟩$ and $|\,a\times b\,|=\sqrt{53}.$ Find $x.$

- $x=\frac{1}{2},\,2$
- $x=1$
- $x=\frac{1}{2},\,1$
- $x=-2$
- $x=-1,\,2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 0 & -2 & 3 \\ -2 & 1 & -2x\end{aligned}| \\  & =|\begin{aligned}-2 & 3 \\ 1 & -2x\end{aligned}|i-|\begin{aligned}0 & 3 \\ -2 & -2x\end{aligned}|j+|\begin{aligned}0 & -2 \\ -2 & 1\end{aligned}|k \\  & =(4x-3)i-(0+6)j+(0-4)k \\  & =⟨4x-3,-6,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(4x-3)^{2}+(-6)^{2}+(-4)^{2}} \\  & =\sqrt{16{x}^{2}-24x+9+36+16} \\  & =\sqrt{16{x}^{2}-24x+61}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{53} \\ \sqrt{16{x}^{2}-24x+61} & =\sqrt{53} \\ 16{x}^{2}-24x+61 & =53 \\ 16{x}^{2}-24x+8 & =0 \\ 2{x}^{2}-3x+1 & =0 \\ (2x-1)(x-1) & =0 \\ x & =\frac{1}{2},\,1.\end{aligned}
$$

Therefore, the solutions are $x=\frac{1}{2},\,1.$

## Public changed raw evidence replay q-103552

Let $a=⟨0,-2,3⟩,$ $b=⟨-2,1,-4x⟩$ and $|\,a\times b\,|=\sqrt{53}.$ Find $2x.$

- $x=\frac{1}{4},\,\frac{1}{2}$
- $x=\frac{1}{2}$
- $x=\frac{1}{4},\,1$
- $x=- \frac{1}{2},\,1$
- $x=-1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 0 & -2 & 3 \\ -2 & 1 & -4x\end{aligned}| \\  & =|\begin{aligned}-2 & 3 \\ 1 & -4x\end{aligned}|i-|\begin{aligned}0 & 3 \\ -2 & -4x\end{aligned}|j+|\begin{aligned}0 & -2 \\ -2 & 1\end{aligned}|k \\  & =(8x-3)i-(0+6)j+(0-4)k \\  & =⟨8x-3,-6,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(8x-3)^{2}+(-6)^{2}+(-4)^{2}} \\  & =\sqrt{64{x}^{2}-48x+9+36+16} \\  & =\sqrt{64{x}^{2}-48x+61}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{53} \\ \sqrt{64{x}^{2}-48x+61} & =\sqrt{53} \\ 64{x}^{2}-48x+61 & =53 \\ 64{x}^{2}-48x+8 & =0 \\ 8{x}^{2}-6x+1 & =0 \\ (4x-1)(2x-1) & =0 \\ 2x & =\frac{1}{2},\,1.\end{aligned}
$$

Therefore, the solutions are $x=\frac{1}{4},\,\frac{1}{2}.$

## Original repaired replay q-103552

### Captured raw original

Let $a=⟨0,-2,3⟩,$ $b=⟨-2,1,-2x⟩$ and $|\,a\times b\,|=\sqrt{53}.$ Find $x.$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 0 & -2 & 3 \\ -2 & 1 & -2x\end{aligned}| \\  & =|\begin{aligned}-2 & 3 \\ 1 & -2x\end{aligned}|i-|\begin{aligned}0 & 3 \\ -2 & -2x\end{aligned}|j+|\begin{aligned}0 & -2 \\ -2 & 1\end{aligned}|k \\  & =(4x-3)i-(0+6)j+(0-4)k \\  & =⟨4x-3,-6,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(4x-3)^{2}+(-6)^{2}+(-4)^{2}} \\  & =\sqrt{16{x}^{2}-24x+9+36+16} \\  & =\sqrt{16{x}^{2}-24x+61}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{53} \\ \sqrt{16{x}^{2}-24x+61} & =\sqrt{53} \\ 16{x}^{2}-24x+61 & =53 \\ 16{x}^{2}-24x+8 & =0 \\ 2{x}^{2}-3x+1 & =0 \\ (2x-1)(x-1) & =0 \\ x & =\frac{1}{2},\,1.\end{aligned}
$$

Therefore, the solutions are $x=\frac{1}{2},\,1.$

Let $a=⟨0,-2,3⟩,$ $b=⟨-2,1,-2x⟩$ and $|\,a\times b\,|=\sqrt{53}.$ Find $x.$

- $x=\frac{1}{2},\,2$
- $x=1$
- $x=\frac{1}{2},\,1$
- $x=-2$
- $x=-1,\,2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 0 & -2 & 3 \\ -2 & 1 & -2x\end{aligned}| \\  & =|\begin{aligned}-2 & 3 \\ 1 & -2x\end{aligned}|i-|\begin{aligned}0 & 3 \\ -2 & -2x\end{aligned}|j+|\begin{aligned}0 & -2 \\ -2 & 1\end{aligned}|k \\  & =(4x-3)i-(0+6)j+(0-4)k \\  & =⟨4x-3,-6,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(4x-3)^{2}+(-6)^{2}+(-4)^{2}} \\  & =\sqrt{16{x}^{2}-24x+9+36+16} \\  & =\sqrt{16{x}^{2}-24x+61}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{53} \\ \sqrt{16{x}^{2}-24x+61} & =\sqrt{53} \\ 16{x}^{2}-24x+61 & =53 \\ 16{x}^{2}-24x+8 & =0 \\ 2{x}^{2}-3x+1 & =0 \\ (2x-1)(x-1) & =0 \\ x & =\frac{1}{2},\,1.\end{aligned}
$$

Therefore, the solutions are $x=\frac{1}{2},\,1.$

## Generated changed observed recipe q-103552

Let $a=⟨0,-2,3⟩,$ $b=⟨-2,1,-4x⟩$ and $|\,a\times b\,|=\sqrt{53}.$ Find $2x.$

- $x=\frac{1}{4},\,\frac{1}{2}$
- $x=\frac{1}{2}$
- $x=\frac{1}{4},\,1$
- $x=- \frac{1}{2},\,1$
- $x=-1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 0 & -2 & 3 \\ -2 & 1 & -4x\end{aligned}| \\  & =|\begin{aligned}-2 & 3 \\ 1 & -4x\end{aligned}|i-|\begin{aligned}0 & 3 \\ -2 & -4x\end{aligned}|j+|\begin{aligned}0 & -2 \\ -2 & 1\end{aligned}|k \\  & =(8x-3)i-(0+6)j+(0-4)k \\  & =⟨8x-3,-6,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(8x-3)^{2}+(-6)^{2}+(-4)^{2}} \\  & =\sqrt{64{x}^{2}-48x+9+36+16} \\  & =\sqrt{64{x}^{2}-48x+61}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{53} \\ \sqrt{64{x}^{2}-48x+61} & =\sqrt{53} \\ 64{x}^{2}-48x+61 & =53 \\ 64{x}^{2}-48x+8 & =0 \\ 8{x}^{2}-6x+1 & =0 \\ (4x-1)(2x-1) & =0 \\ 2x & =\frac{1}{2},\,1.\end{aligned}
$$

Therefore, the solutions are $x=\frac{1}{4},\,\frac{1}{2}.$

## Public raw evidence replay q-19785

Let $a=⟨x,2,3⟩$, $b=⟨2x,5,2⟩$ and $|\,a\times b\,|=\sqrt{393}.$ Find $x.$

- $x=4,5$
- $x=-5,-4$
- $x=\pm 5$
- $x=-5$
- $x=\pm 4$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 2 & 3 \\ 2x & 5 & 2\end{aligned}| \\  & =|\begin{aligned}2 & 3 \\ 5 & 2\end{aligned}|i-|\begin{aligned}x & 3 \\ 2x & 2\end{aligned}|j+|\begin{aligned}x & 2 \\ 2x & 5\end{aligned}|k \\  & =(4-15)i-(2x-6x)j+(5x-4x)k \\  & =⟨-11,4x,x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-11)^{2}+(4x)^{2}+{x}^{2}} \\  & =\sqrt{121+16{x}^{2}+{x}^{2}} \\  & =\sqrt{17{x}^{2}+121}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{393} \\ \sqrt{17{x}^{2}+121} & =\sqrt{393} \\ 17{x}^{2}+121 & =393 \\ 17{x}^{2} & =272 \\ {x}^{2} & =16.\end{aligned}
$$

Therefore, the solutions are $x=\pm 4.$

## Public changed raw evidence replay q-19785

Let $a=⟨2x,2,3⟩$, $b=⟨4x,5,2⟩$ and $|\,a\times b\,|=\sqrt{393}.$ Find $2x.$

- $x=\pm \frac{5}{2}$
- $x=- \frac{5}{2},\,-2$
- $x=2,\,\frac{5}{2}$
- $x=\pm 2$
- $x=- \frac{5}{2}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 2 & 3 \\ 4x & 5 & 2\end{aligned}| \\  & =|\begin{aligned}2 & 3 \\ 5 & 2\end{aligned}|i-|\begin{aligned}2x & 3 \\ 4x & 2\end{aligned}|j+|\begin{aligned}2x & 2 \\ 4x & 5\end{aligned}|k \\  & =(4-15)i-(4x-12x)j+(10x-8x)k \\  & =⟨-11,8x,2x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-11)^{2}+(8x)^{2}+4{x}^{2}} \\  & =\sqrt{121+64{x}^{2}+4{x}^{2}} \\  & =\sqrt{68{x}^{2}+121}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{393} \\ \sqrt{68{x}^{2}+121} & =\sqrt{393} \\ 68{x}^{2}+121 & =393 \\ 68{x}^{2} & =272 \\ 4{x}^{2} & =16.\end{aligned}
$$

Therefore, the solutions are $x=\pm 2.$

## Original repaired replay q-19785

### Captured raw original

Let $a=⟨x,2,3⟩$, $b=⟨2x,5,2⟩$ and $|\,a\times b\,|=\sqrt{393}.$ Find $x.$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 2 & 3 \\ 2x & 5 & 2\end{aligned}| \\  & =|\begin{aligned}2 & 3 \\ 5 & 2\end{aligned}|i-|\begin{aligned}x & 3 \\ 2x & 2\end{aligned}|j+|\begin{aligned}x & 2 \\ 2x & 5\end{aligned}|k \\  & =(4-15)i-(2x-6x)j+(5x-4x)k \\  & =⟨-11,4x,x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-11)^{2}+(4x)^{2}+{x}^{2}} \\  & =\sqrt{121+16{x}^{2}+{x}^{2}} \\  & =\sqrt{17{x}^{2}+121}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{393} \\ \sqrt{17{x}^{2}+121} & =\sqrt{393} \\ 17{x}^{2}+121 & =393 \\ 17{x}^{2} & =272 \\ {x}^{2} & =16.\end{aligned}
$$

Therefore, the solutions are $x=\pm 4.$

Let $a=⟨x,2,3⟩$, $b=⟨2x,5,2⟩$ and $|\,a\times b\,|=\sqrt{393}.$ Find $x.$

- $x=4,5$
- $x=-5,-4$
- $x=\pm 5$
- $x=-5$
- $x=\pm 4$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 2 & 3 \\ 2x & 5 & 2\end{aligned}| \\  & =|\begin{aligned}2 & 3 \\ 5 & 2\end{aligned}|i-|\begin{aligned}x & 3 \\ 2x & 2\end{aligned}|j+|\begin{aligned}x & 2 \\ 2x & 5\end{aligned}|k \\  & =(4-15)i-(2x-6x)j+(5x-4x)k \\  & =⟨-11,4x,x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-11)^{2}+(4x)^{2}+{x}^{2}} \\  & =\sqrt{121+16{x}^{2}+{x}^{2}} \\  & =\sqrt{17{x}^{2}+121}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{393} \\ \sqrt{17{x}^{2}+121} & =\sqrt{393} \\ 17{x}^{2}+121 & =393 \\ 17{x}^{2} & =272 \\ {x}^{2} & =16.\end{aligned}
$$

Therefore, the solutions are $x=\pm 4.$

## Generated changed observed recipe q-19785

Let $a=⟨2x,2,3⟩$, $b=⟨4x,5,2⟩$ and $|\,a\times b\,|=\sqrt{393}.$ Find $2x.$

- $x=\pm \frac{5}{2}$
- $x=- \frac{5}{2},\,-2$
- $x=2,\,\frac{5}{2}$
- $x=\pm 2$
- $x=- \frac{5}{2}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 2 & 3 \\ 4x & 5 & 2\end{aligned}| \\  & =|\begin{aligned}2 & 3 \\ 5 & 2\end{aligned}|i-|\begin{aligned}2x & 3 \\ 4x & 2\end{aligned}|j+|\begin{aligned}2x & 2 \\ 4x & 5\end{aligned}|k \\  & =(4-15)i-(4x-12x)j+(10x-8x)k \\  & =⟨-11,8x,2x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-11)^{2}+(8x)^{2}+4{x}^{2}} \\  & =\sqrt{121+64{x}^{2}+4{x}^{2}} \\  & =\sqrt{68{x}^{2}+121}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{393} \\ \sqrt{68{x}^{2}+121} & =\sqrt{393} \\ 68{x}^{2}+121 & =393 \\ 68{x}^{2} & =272 \\ 4{x}^{2} & =16.\end{aligned}
$$

Therefore, the solutions are $x=\pm 2.$

## Public raw evidence replay q-275278

Let $a=⟨-2x,3,5⟩,$ $b=⟨2x,0,1⟩$ and $|\,a\times b\,|=\sqrt{909}.$ Then, in **ascending order**,  the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

- $-\sqrt{5}$
- $\sqrt{5}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -2x & 3 & 5 \\ 2x & 0 & 1\end{aligned}| \\  & =|\begin{aligned}3 & 5 \\ 0 & 1\end{aligned}|i-|\begin{aligned}-2x & 5 \\ 2x & 1\end{aligned}|j+|\begin{aligned}-2x & 3 \\ 2x & 0\end{aligned}|k \\  & =(3-0)i-(-2x-10x)j+(0-6x)k \\  & =⟨3,12x,-6x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(12x)^{2}+(-6x)^{2}} \\  & =\sqrt{9+144{x}^{2}+36{x}^{2}} \\  & =\sqrt{180{x}^{2}+9}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{909} \\ \sqrt{180{x}^{2}+9} & =\sqrt{909} \\ 180{x}^{2}+9 & =909 \\ 180{x}^{2} & =900 \\ {x}^{2} & =5\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=-\sqrt{5},$ $x=\sqrt{5}.$

## Public changed raw evidence replay q-275278

Let $a=⟨-4x,3,5⟩,$ $b=⟨4x,0,1⟩$ and $|\,a\times b\,|=\sqrt{909}.$ Then, in **ascending order**,  the possible values of $2x$ are

$\,2x=$
{{field-1}}$\,$ and $\,2x=$
{{field-2}}.

- $- \frac{\sqrt{5}}{2}$
- $\frac{\sqrt{5}}{2}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -4x & 3 & 5 \\ 4x & 0 & 1\end{aligned}| \\  & =|\begin{aligned}3 & 5 \\ 0 & 1\end{aligned}|i-|\begin{aligned}-4x & 5 \\ 4x & 1\end{aligned}|j+|\begin{aligned}-4x & 3 \\ 4x & 0\end{aligned}|k \\  & =(3-0)i-(-4x-20x)j+(0-12x)k \\  & =⟨3,24x,-12x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(24x)^{2}+(-12x)^{2}} \\  & =\sqrt{9+576{x}^{2}+144{x}^{2}} \\  & =\sqrt{720{x}^{2}+9}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{909} \\ \sqrt{720{x}^{2}+9} & =\sqrt{909} \\ 720{x}^{2}+9 & =909 \\ 720{x}^{2} & =900 \\ 4{x}^{2} & =5\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=- \frac{\sqrt{5}}{2}$ $x=\frac{\sqrt{5}}{2}.$

## Original repaired replay q-275278

### Captured raw original

Let $a=⟨-2x,3,5⟩,$ $b=⟨2x,0,1⟩$ and $|\,a\times b\,|=\sqrt{909}.$ Then, in **ascending order**,  the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -2x & 3 & 5 \\ 2x & 0 & 1\end{aligned}| \\  & =|\begin{aligned}3 & 5 \\ 0 & 1\end{aligned}|i-|\begin{aligned}-2x & 5 \\ 2x & 1\end{aligned}|j+|\begin{aligned}-2x & 3 \\ 2x & 0\end{aligned}|k \\  & =(3-0)i-(-2x-10x)j+(0-6x)k \\  & =⟨3,12x,-6x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(12x)^{2}+(-6x)^{2}} \\  & =\sqrt{9+144{x}^{2}+36{x}^{2}} \\  & =\sqrt{180{x}^{2}+9}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{909} \\ \sqrt{180{x}^{2}+9} & =\sqrt{909} \\ 180{x}^{2}+9 & =909 \\ 180{x}^{2} & =900 \\ {x}^{2} & =5\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=-\sqrt{5},$ $x=\sqrt{5}.$

Let $a=⟨-2x,3,5⟩,$ $b=⟨2x,0,1⟩$ and $|\,a\times b\,|=\sqrt{909}.$ Then, in **ascending order**,  the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

- $-\sqrt{5}$
- $\sqrt{5}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -2x & 3 & 5 \\ 2x & 0 & 1\end{aligned}| \\  & =|\begin{aligned}3 & 5 \\ 0 & 1\end{aligned}|i-|\begin{aligned}-2x & 5 \\ 2x & 1\end{aligned}|j+|\begin{aligned}-2x & 3 \\ 2x & 0\end{aligned}|k \\  & =(3-0)i-(-2x-10x)j+(0-6x)k \\  & =⟨3,12x,-6x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(12x)^{2}+(-6x)^{2}} \\  & =\sqrt{9+144{x}^{2}+36{x}^{2}} \\  & =\sqrt{180{x}^{2}+9}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{909} \\ \sqrt{180{x}^{2}+9} & =\sqrt{909} \\ 180{x}^{2}+9 & =909 \\ 180{x}^{2} & =900 \\ {x}^{2} & =5\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=-\sqrt{5},$ $x=\sqrt{5}.$

## Generated changed observed recipe q-275278

Let $a=⟨-4x,3,5⟩,$ $b=⟨4x,0,1⟩$ and $|\,a\times b\,|=\sqrt{909}.$ Then, in **ascending order**,  the possible values of $2x$ are

$\,2x=$
{{field-1}}$\,$ and $\,2x=$
{{field-2}}.

- $- \frac{\sqrt{5}}{2}$
- $\frac{\sqrt{5}}{2}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ -4x & 3 & 5 \\ 4x & 0 & 1\end{aligned}| \\  & =|\begin{aligned}3 & 5 \\ 0 & 1\end{aligned}|i-|\begin{aligned}-4x & 5 \\ 4x & 1\end{aligned}|j+|\begin{aligned}-4x & 3 \\ 4x & 0\end{aligned}|k \\  & =(3-0)i-(-4x-20x)j+(0-12x)k \\  & =⟨3,24x,-12x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(24x)^{2}+(-12x)^{2}} \\  & =\sqrt{9+576{x}^{2}+144{x}^{2}} \\  & =\sqrt{720{x}^{2}+9}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{909} \\ \sqrt{720{x}^{2}+9} & =\sqrt{909} \\ 720{x}^{2}+9 & =909 \\ 720{x}^{2} & =900 \\ 4{x}^{2} & =5\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=- \frac{\sqrt{5}}{2}$ $x=\frac{\sqrt{5}}{2}.$

## Public raw evidence replay q-278839

Let $a=⟨x,2,1⟩,$ $b=⟨2,0,1⟩$ and $|\,a\times b\,|=\sqrt{20}.$ Find $x.$

$\,x=$
{{field-1}}

- $2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 2 & 1 \\ 2 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ 0 & 1\end{aligned}|i-|\begin{aligned}x & 1 \\ 2 & 1\end{aligned}|j+|\begin{aligned}x & 2 \\ 2 & 0\end{aligned}|k \\  & =(2-0)i-(x-2)j+(0-4)k \\  & =⟨2,2-x,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(2-x)^{2}+(-4)^{2}} \\  & =\sqrt{4+4-4x+{x}^{2}+16} \\  & =\sqrt{{x}^{2}-4x+24}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{20} \\ \sqrt{{x}^{2}-4x+24} & =\sqrt{20} \\ {x}^{2}-4x+24 & =20 \\ {x}^{2}-4x+4 & =0 \\ (x-2)^{2} & =0 \\ x-2 & =0 \\ x & =2\end{aligned}
$$

Therefore, the solution is $x=2.$

## Public changed raw evidence replay q-278839

Let $a=⟨2x,2,1⟩,$ $b=⟨2,0,1⟩$ and $|\,a\times b\,|=\sqrt{20}.$ Find $2x.$

$\,2x=$
{{field-1}}

- $1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 2 & 1 \\ 2 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ 0 & 1\end{aligned}|i-|\begin{aligned}2x & 1 \\ 2 & 1\end{aligned}|j+|\begin{aligned}2x & 2 \\ 2 & 0\end{aligned}|k \\  & =(2-0)i-(2x-2)j+(0-4)k \\  & =⟨2,2-2x,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(2-2x)^{2}+(-4)^{2}} \\  & =\sqrt{4+4-8x+4{x}^{2}+16} \\  & =\sqrt{4{x}^{2}-8x+24}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{20} \\ \sqrt{4{x}^{2}-8x+24} & =\sqrt{20} \\ 4{x}^{2}-8x+24 & =20 \\ 4{x}^{2}-8x+4 & =0 \\ (2x-2)^{2} & =0 \\ 2x-2 & =0 \\ 2x & =2\end{aligned}
$$

Therefore, the solution is $x=1.$

## Original repaired replay q-278839

### Captured raw original

Let $a=⟨x,2,1⟩,$ $b=⟨2,0,1⟩$ and $|\,a\times b\,|=\sqrt{20}.$ Find $x.$

$\,x=$
{{field-1}}

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 2 & 1 \\ 2 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ 0 & 1\end{aligned}|i-|\begin{aligned}x & 1 \\ 2 & 1\end{aligned}|j+|\begin{aligned}x & 2 \\ 2 & 0\end{aligned}|k \\  & =(2-0)i-(x-2)j+(0-4)k \\  & =⟨2,2-x,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(2-x)^{2}+(-4)^{2}} \\  & =\sqrt{4+4-4x+{x}^{2}+16} \\  & =\sqrt{{x}^{2}-4x+24}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{20} \\ \sqrt{{x}^{2}-4x+24} & =\sqrt{20} \\ {x}^{2}-4x+24 & =20 \\ {x}^{2}-4x+4 & =0 \\ (x-2)^{2} & =0 \\ x-2 & =0 \\ x & =2\end{aligned}
$$

Therefore, the solution is $x=2.$

Let $a=⟨x,2,1⟩,$ $b=⟨2,0,1⟩$ and $|\,a\times b\,|=\sqrt{20}.$ Find $x.$

$\,x=$
{{field-1}}

- $2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 2 & 1 \\ 2 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ 0 & 1\end{aligned}|i-|\begin{aligned}x & 1 \\ 2 & 1\end{aligned}|j+|\begin{aligned}x & 2 \\ 2 & 0\end{aligned}|k \\  & =(2-0)i-(x-2)j+(0-4)k \\  & =⟨2,2-x,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(2-x)^{2}+(-4)^{2}} \\  & =\sqrt{4+4-4x+{x}^{2}+16} \\  & =\sqrt{{x}^{2}-4x+24}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{20} \\ \sqrt{{x}^{2}-4x+24} & =\sqrt{20} \\ {x}^{2}-4x+24 & =20 \\ {x}^{2}-4x+4 & =0 \\ (x-2)^{2} & =0 \\ x-2 & =0 \\ x & =2\end{aligned}
$$

Therefore, the solution is $x=2.$

## Generated changed observed recipe q-278839

Let $a=⟨2x,2,1⟩,$ $b=⟨2,0,1⟩$ and $|\,a\times b\,|=\sqrt{20}.$ Find $2x.$

$\,2x=$
{{field-1}}

- $1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 2 & 1 \\ 2 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ 0 & 1\end{aligned}|i-|\begin{aligned}2x & 1 \\ 2 & 1\end{aligned}|j+|\begin{aligned}2x & 2 \\ 2 & 0\end{aligned}|k \\  & =(2-0)i-(2x-2)j+(0-4)k \\  & =⟨2,2-2x,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(2-2x)^{2}+(-4)^{2}} \\  & =\sqrt{4+4-8x+4{x}^{2}+16} \\  & =\sqrt{4{x}^{2}-8x+24}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{20} \\ \sqrt{4{x}^{2}-8x+24} & =\sqrt{20} \\ 4{x}^{2}-8x+24 & =20 \\ 4{x}^{2}-8x+4 & =0 \\ (2x-2)^{2} & =0 \\ 2x-2 & =0 \\ 2x & =2\end{aligned}
$$

Therefore, the solution is $x=1.$

## Public raw evidence replay q-282260

Let $a=⟨2x,3,1⟩,$ $b=⟨-2x,0,4⟩$ and $|\,a\times b\,|=\sqrt{280}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

- $-1$
- $1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 3 & 1 \\ -2x & 0 & 4\end{aligned}| \\  & =|\begin{aligned}3 & 1 \\ 0 & 4\end{aligned}|i-|\begin{aligned}2x & 1 \\ -2x & 4\end{aligned}|j+|\begin{aligned}2x & 3 \\ -2x & 0\end{aligned}|k \\  & =(12-0)i-(8x+2x)j+(0+6x)k \\  & =⟨12,-10x,6x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{12}^{2}+(-10x)^{2}+(6x)^{2}} \\  & =\sqrt{144+100{x}^{2}+36{x}^{2}} \\  & =\sqrt{136{x}^{2}+144}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{280} \\ \sqrt{136{x}^{2}+144} & =\sqrt{280} \\ 136{x}^{2}+144 & =280 \\ 136{x}^{2} & =136 \\ {x}^{2} & =1\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=-1,$ $x=1.$

## Public changed raw evidence replay q-282260

Let $a=⟨4x,3,1⟩,$ $b=⟨-4x,0,4⟩$ and $|\,a\times b\,|=\sqrt{280}.$ Then, in **ascending order**, the possible values of $2x$ are

$\,2x=$
{{field-1}}$\,$ and $\,2x=$
{{field-2}}.

- $- \frac{1}{2}$
- $\frac{1}{2}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4x & 3 & 1 \\ -4x & 0 & 4\end{aligned}| \\  & =|\begin{aligned}3 & 1 \\ 0 & 4\end{aligned}|i-|\begin{aligned}4x & 1 \\ -4x & 4\end{aligned}|j+|\begin{aligned}4x & 3 \\ -4x & 0\end{aligned}|k \\  & =(12-0)i-(16x+4x)j+(0+12x)k \\  & =⟨12,-20x,12x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{12}^{2}+(-20x)^{2}+(12x)^{2}} \\  & =\sqrt{144+400{x}^{2}+144{x}^{2}} \\  & =\sqrt{544{x}^{2}+144}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{280} \\ \sqrt{544{x}^{2}+144} & =\sqrt{280} \\ 544{x}^{2}+144 & =280 \\ 544{x}^{2} & =136 \\ 4{x}^{2} & =1\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=- \frac{1}{2}$ $x=\frac{1}{2}.$

## Original repaired replay q-282260

### Captured raw original

Let $a=⟨2x,3,1⟩,$ $b=⟨-2x,0,4⟩$ and $|\,a\times b\,|=\sqrt{280}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 3 & 1 \\ -2x & 0 & 4\end{aligned}| \\  & =|\begin{aligned}3 & 1 \\ 0 & 4\end{aligned}|i-|\begin{aligned}2x & 1 \\ -2x & 4\end{aligned}|j+|\begin{aligned}2x & 3 \\ -2x & 0\end{aligned}|k \\  & =(12-0)i-(8x+2x)j+(0+6x)k \\  & =⟨12,-10x,6x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{12}^{2}+(-10x)^{2}+(6x)^{2}} \\  & =\sqrt{144+100{x}^{2}+36{x}^{2}} \\  & =\sqrt{136{x}^{2}+144}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{280} \\ \sqrt{136{x}^{2}+144} & =\sqrt{280} \\ 136{x}^{2}+144 & =280 \\ 136{x}^{2} & =136 \\ {x}^{2} & =1\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=-1,$ $x=1.$

Let $a=⟨2x,3,1⟩,$ $b=⟨-2x,0,4⟩$ and $|\,a\times b\,|=\sqrt{280}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

- $-1$
- $1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 3 & 1 \\ -2x & 0 & 4\end{aligned}| \\  & =|\begin{aligned}3 & 1 \\ 0 & 4\end{aligned}|i-|\begin{aligned}2x & 1 \\ -2x & 4\end{aligned}|j+|\begin{aligned}2x & 3 \\ -2x & 0\end{aligned}|k \\  & =(12-0)i-(8x+2x)j+(0+6x)k \\  & =⟨12,-10x,6x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{12}^{2}+(-10x)^{2}+(6x)^{2}} \\  & =\sqrt{144+100{x}^{2}+36{x}^{2}} \\  & =\sqrt{136{x}^{2}+144}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{280} \\ \sqrt{136{x}^{2}+144} & =\sqrt{280} \\ 136{x}^{2}+144 & =280 \\ 136{x}^{2} & =136 \\ {x}^{2} & =1\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=-1,$ $x=1.$

## Generated changed observed recipe q-282260

Let $a=⟨4x,3,1⟩,$ $b=⟨-4x,0,4⟩$ and $|\,a\times b\,|=\sqrt{280}.$ Then, in **ascending order**, the possible values of $2x$ are

$\,2x=$
{{field-1}}$\,$ and $\,2x=$
{{field-2}}.

- $- \frac{1}{2}$
- $\frac{1}{2}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4x & 3 & 1 \\ -4x & 0 & 4\end{aligned}| \\  & =|\begin{aligned}3 & 1 \\ 0 & 4\end{aligned}|i-|\begin{aligned}4x & 1 \\ -4x & 4\end{aligned}|j+|\begin{aligned}4x & 3 \\ -4x & 0\end{aligned}|k \\  & =(12-0)i-(16x+4x)j+(0+12x)k \\  & =⟨12,-20x,12x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{12}^{2}+(-20x)^{2}+(12x)^{2}} \\  & =\sqrt{144+400{x}^{2}+144{x}^{2}} \\  & =\sqrt{544{x}^{2}+144}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{280} \\ \sqrt{544{x}^{2}+144} & =\sqrt{280} \\ 544{x}^{2}+144 & =280 \\ 544{x}^{2} & =136 \\ 4{x}^{2} & =1\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=- \frac{1}{2}$ $x=\frac{1}{2}.$

## Public raw evidence replay q-282261

Let $a=⟨x,0,1⟩,$ $b=⟨-x,2,0⟩$ and $|\,a\times b\,|=\sqrt{29}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

- $-\sqrt{5}$
- $\sqrt{5}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 0 & 1 \\ -x & 2 & 0\end{aligned}| \\  & =|\begin{aligned}0 & 1 \\ 2 & 0\end{aligned}|i-|\begin{aligned}x & 1 \\ -x & 0\end{aligned}|j+|\begin{aligned}x & 0 \\ -x & 2\end{aligned}|k \\  & =(0-2)i-(0+x)j+(2x+0)k \\  & =⟨-2,-x,2x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-2)^{2}+(-x)^{2}+(2x)^{2}} \\  & =\sqrt{4+{x}^{2}+4{x}^{2}} \\  & =\sqrt{5{x}^{2}+4}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{29} \\ \sqrt{5{x}^{2}+4} & =\sqrt{29} \\ 5{x}^{2}+4 & =29 \\ 5{x}^{2} & =25 \\ {x}^{2} & =5\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=-\sqrt{5},$ $x=\sqrt{5}.$

## Public changed raw evidence replay q-282261

Let $a=⟨2x,0,1⟩,$ $b=⟨-2x,2,0⟩$ and $|\,a\times b\,|=\sqrt{29}.$ Then, in **ascending order**, the possible values of $2x$ are

$\,2x=$
{{field-1}}$\,$ and $\,2x=$
{{field-2}}.

- $- \frac{\sqrt{5}}{2}$
- $\frac{\sqrt{5}}{2}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 0 & 1 \\ -2x & 2 & 0\end{aligned}| \\  & =|\begin{aligned}0 & 1 \\ 2 & 0\end{aligned}|i-|\begin{aligned}2x & 1 \\ -2x & 0\end{aligned}|j+|\begin{aligned}2x & 0 \\ -2x & 2\end{aligned}|k \\  & =(0-2)i-(0+2x)j+(4x+0)k \\  & =⟨-2,-2x,4x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-2)^{2}+(-2x)^{2}+(4x)^{2}} \\  & =\sqrt{4+4{x}^{2}+16{x}^{2}} \\  & =\sqrt{20{x}^{2}+4}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{29} \\ \sqrt{20{x}^{2}+4} & =\sqrt{29} \\ 20{x}^{2}+4 & =29 \\ 20{x}^{2} & =25 \\ 4{x}^{2} & =5\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=- \frac{\sqrt{5}}{2}$ $x=\frac{\sqrt{5}}{2}.$

## Original repaired replay q-282261

### Captured raw original

Let $a=⟨x,0,1⟩,$ $b=⟨-x,2,0⟩$ and $|\,a\times b\,|=\sqrt{29}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 0 & 1 \\ -x & 2 & 0\end{aligned}| \\  & =|\begin{aligned}0 & 1 \\ 2 & 0\end{aligned}|i-|\begin{aligned}x & 1 \\ -x & 0\end{aligned}|j+|\begin{aligned}x & 0 \\ -x & 2\end{aligned}|k \\  & =(0-2)i-(0+x)j+(2x+0)k \\  & =⟨-2,-x,2x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-2)^{2}+(-x)^{2}+(2x)^{2}} \\  & =\sqrt{4+{x}^{2}+4{x}^{2}} \\  & =\sqrt{5{x}^{2}+4}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{29} \\ \sqrt{5{x}^{2}+4} & =\sqrt{29} \\ 5{x}^{2}+4 & =29 \\ 5{x}^{2} & =25 \\ {x}^{2} & =5\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=-\sqrt{5},$ $x=\sqrt{5}.$

Let $a=⟨x,0,1⟩,$ $b=⟨-x,2,0⟩$ and $|\,a\times b\,|=\sqrt{29}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

- $-\sqrt{5}$
- $\sqrt{5}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 0 & 1 \\ -x & 2 & 0\end{aligned}| \\  & =|\begin{aligned}0 & 1 \\ 2 & 0\end{aligned}|i-|\begin{aligned}x & 1 \\ -x & 0\end{aligned}|j+|\begin{aligned}x & 0 \\ -x & 2\end{aligned}|k \\  & =(0-2)i-(0+x)j+(2x+0)k \\  & =⟨-2,-x,2x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-2)^{2}+(-x)^{2}+(2x)^{2}} \\  & =\sqrt{4+{x}^{2}+4{x}^{2}} \\  & =\sqrt{5{x}^{2}+4}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{29} \\ \sqrt{5{x}^{2}+4} & =\sqrt{29} \\ 5{x}^{2}+4 & =29 \\ 5{x}^{2} & =25 \\ {x}^{2} & =5\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=-\sqrt{5},$ $x=\sqrt{5}.$

## Generated changed observed recipe q-282261

Let $a=⟨2x,0,1⟩,$ $b=⟨-2x,2,0⟩$ and $|\,a\times b\,|=\sqrt{29}.$ Then, in **ascending order**, the possible values of $2x$ are

$\,2x=$
{{field-1}}$\,$ and $\,2x=$
{{field-2}}.

- $- \frac{\sqrt{5}}{2}$
- $\frac{\sqrt{5}}{2}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 0 & 1 \\ -2x & 2 & 0\end{aligned}| \\  & =|\begin{aligned}0 & 1 \\ 2 & 0\end{aligned}|i-|\begin{aligned}2x & 1 \\ -2x & 0\end{aligned}|j+|\begin{aligned}2x & 0 \\ -2x & 2\end{aligned}|k \\  & =(0-2)i-(0+2x)j+(4x+0)k \\  & =⟨-2,-2x,4x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-2)^{2}+(-2x)^{2}+(4x)^{2}} \\  & =\sqrt{4+4{x}^{2}+16{x}^{2}} \\  & =\sqrt{20{x}^{2}+4}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{29} \\ \sqrt{20{x}^{2}+4} & =\sqrt{29} \\ 20{x}^{2}+4 & =29 \\ 20{x}^{2} & =25 \\ 4{x}^{2} & =5\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=- \frac{\sqrt{5}}{2}$ $x=\frac{\sqrt{5}}{2}.$

## Public raw evidence replay q-282262

Let $a=⟨x,3,0⟩,$ $b=⟨-x,0,1⟩$ and $|\,a\times b\,|=\sqrt{49}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

- $2$
- $-2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 3 & 0 \\ -x & 0 & 1\end{aligned}| \\  & =|\begin{aligned}3 & 0 \\ 0 & 1\end{aligned}|i-|\begin{aligned}x & 0 \\ -x & 1\end{aligned}|j+|\begin{aligned}x & 3 \\ -x & 0\end{aligned}|k \\  & =(3-0)i-(x+0)j+(0+3x)k \\  & =⟨3,-x,3x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(-x)^{2}+(3x)^{2}} \\  & =\sqrt{9+{x}^{2}+9{x}^{2}} \\  & =\sqrt{10{x}^{2}+9}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{49} \\ \sqrt{10{x}^{2}+9} & =\sqrt{49} \\ 10{x}^{2}+9 & =49 \\ 10{x}^{2} & =40 \\ {x}^{2} & =4\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=-2,$ $x=2.$

## Public changed raw evidence replay q-282262

Let $a=⟨2x,3,0⟩,$ $b=⟨-2x,0,1⟩$ and $|\,a\times b\,|=\sqrt{49}.$ Then, in **ascending order**, the possible values of $2x$ are

$\,2x=$
{{field-1}}$\,$ and $\,2x=$
{{field-2}}.

- $1$
- $-1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 3 & 0 \\ -2x & 0 & 1\end{aligned}| \\  & =|\begin{aligned}3 & 0 \\ 0 & 1\end{aligned}|i-|\begin{aligned}2x & 0 \\ -2x & 1\end{aligned}|j+|\begin{aligned}2x & 3 \\ -2x & 0\end{aligned}|k \\  & =(3-0)i-(2x+0)j+(0+6x)k \\  & =⟨3,-2x,6x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(-2x)^{2}+(6x)^{2}} \\  & =\sqrt{9+4{x}^{2}+36{x}^{2}} \\  & =\sqrt{40{x}^{2}+9}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{49} \\ \sqrt{40{x}^{2}+9} & =\sqrt{49} \\ 40{x}^{2}+9 & =49 \\ 40{x}^{2} & =40 \\ 4{x}^{2} & =4\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=-1$ $x=1.$

## Original repaired replay q-282262

### Captured raw original

Let $a=⟨x,3,0⟩,$ $b=⟨-x,0,1⟩$ and $|\,a\times b\,|=\sqrt{49}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 3 & 0 \\ -x & 0 & 1\end{aligned}| \\  & =|\begin{aligned}3 & 0 \\ 0 & 1\end{aligned}|i-|\begin{aligned}x & 0 \\ -x & 1\end{aligned}|j+|\begin{aligned}x & 3 \\ -x & 0\end{aligned}|k \\  & =(3-0)i-(x+0)j+(0+3x)k \\  & =⟨3,-x,3x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(-x)^{2}+(3x)^{2}} \\  & =\sqrt{9+{x}^{2}+9{x}^{2}} \\  & =\sqrt{10{x}^{2}+9}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{49} \\ \sqrt{10{x}^{2}+9} & =\sqrt{49} \\ 10{x}^{2}+9 & =49 \\ 10{x}^{2} & =40 \\ {x}^{2} & =4\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=-2,$ $x=2.$

Let $a=⟨x,3,0⟩,$ $b=⟨-x,0,1⟩$ and $|\,a\times b\,|=\sqrt{49}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

- $2$
- $-2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 3 & 0 \\ -x & 0 & 1\end{aligned}| \\  & =|\begin{aligned}3 & 0 \\ 0 & 1\end{aligned}|i-|\begin{aligned}x & 0 \\ -x & 1\end{aligned}|j+|\begin{aligned}x & 3 \\ -x & 0\end{aligned}|k \\  & =(3-0)i-(x+0)j+(0+3x)k \\  & =⟨3,-x,3x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(-x)^{2}+(3x)^{2}} \\  & =\sqrt{9+{x}^{2}+9{x}^{2}} \\  & =\sqrt{10{x}^{2}+9}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{49} \\ \sqrt{10{x}^{2}+9} & =\sqrt{49} \\ 10{x}^{2}+9 & =49 \\ 10{x}^{2} & =40 \\ {x}^{2} & =4\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=-2,$ $x=2.$

## Generated changed observed recipe q-282262

Let $a=⟨2x,3,0⟩,$ $b=⟨-2x,0,1⟩$ and $|\,a\times b\,|=\sqrt{49}.$ Then, in **ascending order**, the possible values of $2x$ are

$\,2x=$
{{field-1}}$\,$ and $\,2x=$
{{field-2}}.

- $1$
- $-1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 3 & 0 \\ -2x & 0 & 1\end{aligned}| \\  & =|\begin{aligned}3 & 0 \\ 0 & 1\end{aligned}|i-|\begin{aligned}2x & 0 \\ -2x & 1\end{aligned}|j+|\begin{aligned}2x & 3 \\ -2x & 0\end{aligned}|k \\  & =(3-0)i-(2x+0)j+(0+6x)k \\  & =⟨3,-2x,6x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(-2x)^{2}+(6x)^{2}} \\  & =\sqrt{9+4{x}^{2}+36{x}^{2}} \\  & =\sqrt{40{x}^{2}+9}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{49} \\ \sqrt{40{x}^{2}+9} & =\sqrt{49} \\ 40{x}^{2}+9 & =49 \\ 40{x}^{2} & =40 \\ 4{x}^{2} & =4\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=-1$ $x=1.$

## Public raw evidence replay q-282269

Let $a=⟨x,1,1⟩,$ $b=⟨1,0,3⟩$ and $|\,a\times b\,|=\sqrt{10}.$ Find $x.$

$\,x=$
{{field-1}}

- $\frac{1}{3}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 1 & 1 \\ 1 & 0 & 3\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ 0 & 3\end{aligned}|i-|\begin{aligned}x & 1 \\ 1 & 3\end{aligned}|j+|\begin{aligned}x & 1 \\ 1 & 0\end{aligned}|k \\  & =(3-0)i-(3x-1)j+(0-1)k \\  & =⟨3,1-3x,-1⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(1-3x)^{2}+(-1)^{2}} \\  & =\sqrt{9+(9{x}^{2}-6x+1)+1} \\  & =\sqrt{9{x}^{2}-6x+11}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{10} \\ \sqrt{9{x}^{2}-6x+11} & =\sqrt{10} \\ 9{x}^{2}-6x+11 & =10 \\ (3x-1)^{2} & =0 \\ 3x-1 & =0 \\ x & =\frac{1}{3}\end{aligned}
$$

Therefore, the solution is $x=\frac{1}{3}.$

## Public changed raw evidence replay q-282269

Let $a=⟨2x,1,1⟩,$ $b=⟨1,0,3⟩$ and $|\,a\times b\,|=\sqrt{10}.$ Find $2x.$

$\,2x=$
{{field-1}}

- $\frac{1}{6}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 1 & 1 \\ 1 & 0 & 3\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ 0 & 3\end{aligned}|i-|\begin{aligned}2x & 1 \\ 1 & 3\end{aligned}|j+|\begin{aligned}2x & 1 \\ 1 & 0\end{aligned}|k \\  & =(3-0)i-(6x-1)j+(0-1)k \\  & =⟨3,1-6x,-1⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(1-6x)^{2}+(-1)^{2}} \\  & =\sqrt{9+(36{x}^{2}-12x+1)+1} \\  & =\sqrt{36{x}^{2}-12x+11}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{10} \\ \sqrt{36{x}^{2}-12x+11} & =\sqrt{10} \\ 36{x}^{2}-12x+11 & =10 \\ (6x-1)^{2} & =0 \\ 6x-1 & =0 \\ 2x & =\frac{1}{3}\end{aligned}
$$

Therefore, the solution is $x=\frac{1}{6}.$

## Original repaired replay q-282269

### Captured raw original

Let $a=⟨x,1,1⟩,$ $b=⟨1,0,3⟩$ and $|\,a\times b\,|=\sqrt{10}.$ Find $x.$

$\,x=$
{{field-1}}

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 1 & 1 \\ 1 & 0 & 3\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ 0 & 3\end{aligned}|i-|\begin{aligned}x & 1 \\ 1 & 3\end{aligned}|j+|\begin{aligned}x & 1 \\ 1 & 0\end{aligned}|k \\  & =(3-0)i-(3x-1)j+(0-1)k \\  & =⟨3,1-3x,-1⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(1-3x)^{2}+(-1)^{2}} \\  & =\sqrt{9+(9{x}^{2}-6x+1)+1} \\  & =\sqrt{9{x}^{2}-6x+11}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{10} \\ \sqrt{9{x}^{2}-6x+11} & =\sqrt{10} \\ 9{x}^{2}-6x+11 & =10 \\ (3x-1)^{2} & =0 \\ 3x-1 & =0 \\ x & =\frac{1}{3}\end{aligned}
$$

Therefore, the solution is $x=\frac{1}{3}.$

Let $a=⟨x,1,1⟩,$ $b=⟨1,0,3⟩$ and $|\,a\times b\,|=\sqrt{10}.$ Find $x.$

$\,x=$
{{field-1}}

- $\frac{1}{3}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 1 & 1 \\ 1 & 0 & 3\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ 0 & 3\end{aligned}|i-|\begin{aligned}x & 1 \\ 1 & 3\end{aligned}|j+|\begin{aligned}x & 1 \\ 1 & 0\end{aligned}|k \\  & =(3-0)i-(3x-1)j+(0-1)k \\  & =⟨3,1-3x,-1⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(1-3x)^{2}+(-1)^{2}} \\  & =\sqrt{9+(9{x}^{2}-6x+1)+1} \\  & =\sqrt{9{x}^{2}-6x+11}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{10} \\ \sqrt{9{x}^{2}-6x+11} & =\sqrt{10} \\ 9{x}^{2}-6x+11 & =10 \\ (3x-1)^{2} & =0 \\ 3x-1 & =0 \\ x & =\frac{1}{3}\end{aligned}
$$

Therefore, the solution is $x=\frac{1}{3}.$

## Generated changed observed recipe q-282269

Let $a=⟨2x,1,1⟩,$ $b=⟨1,0,3⟩$ and $|\,a\times b\,|=\sqrt{10}.$ Find $2x.$

$\,2x=$
{{field-1}}

- $\frac{1}{6}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 1 & 1 \\ 1 & 0 & 3\end{aligned}| \\  & =|\begin{aligned}1 & 1 \\ 0 & 3\end{aligned}|i-|\begin{aligned}2x & 1 \\ 1 & 3\end{aligned}|j+|\begin{aligned}2x & 1 \\ 1 & 0\end{aligned}|k \\  & =(3-0)i-(6x-1)j+(0-1)k \\  & =⟨3,1-6x,-1⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{3}^{2}+(1-6x)^{2}+(-1)^{2}} \\  & =\sqrt{9+(36{x}^{2}-12x+1)+1} \\  & =\sqrt{36{x}^{2}-12x+11}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{10} \\ \sqrt{36{x}^{2}-12x+11} & =\sqrt{10} \\ 36{x}^{2}-12x+11 & =10 \\ (6x-1)^{2} & =0 \\ 6x-1 & =0 \\ 2x & =\frac{1}{3}\end{aligned}
$$

Therefore, the solution is $x=\frac{1}{6}.$

## Public raw evidence replay q-282270

Let $a=⟨x,1,2⟩,$ $b=⟨1,0,2⟩$ and $|\,a\times b\,|=\sqrt{5}.$ Find $x.$

$\,x=$
{{field-1}}

- $1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 1 & 2 \\ 1 & 0 & 2\end{aligned}| \\  & =|\begin{aligned}1 & 2 \\ 0 & 2\end{aligned}|i-|\begin{aligned}x & 2 \\ 1 & 2\end{aligned}|j+|\begin{aligned}x & 1 \\ 1 & 0\end{aligned}|k \\  & =(2-0)i-(2x-2)j+(0-1)k \\  & =⟨2,2-2x,-1⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(2-2x)^{2}+(-1)^{2}} \\  & =\sqrt{4+(4{x}^{2}-8x+4)+1} \\  & =\sqrt{4{x}^{2}-8x+9}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{5} \\ \sqrt{4{x}^{2}-8x+9} & =\sqrt{5} \\ 4{x}^{2}-8x+9 & =5 \\ 4{x}^{2}-8x+4 & =0 \\ (2x-2)^{2} & =0 \\ 2x-2 & =0 \\ x & =1\end{aligned}
$$

Therefore, the solution is $x=1.$

## Public changed raw evidence replay q-282270

Let $a=⟨2x,1,2⟩,$ $b=⟨1,0,2⟩$ and $|\,a\times b\,|=\sqrt{5}.$ Find $2x.$

$\,2x=$
{{field-1}}

- $\frac{1}{2}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 1 & 2 \\ 1 & 0 & 2\end{aligned}| \\  & =|\begin{aligned}1 & 2 \\ 0 & 2\end{aligned}|i-|\begin{aligned}2x & 2 \\ 1 & 2\end{aligned}|j+|\begin{aligned}2x & 1 \\ 1 & 0\end{aligned}|k \\  & =(2-0)i-(4x-2)j+(0-1)k \\  & =⟨2,2-4x,-1⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(2-4x)^{2}+(-1)^{2}} \\  & =\sqrt{4+(16{x}^{2}-16x+4)+1} \\  & =\sqrt{16{x}^{2}-16x+9}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{5} \\ \sqrt{16{x}^{2}-16x+9} & =\sqrt{5} \\ 16{x}^{2}-16x+9 & =5 \\ 16{x}^{2}-16x+4 & =0 \\ (4x-2)^{2} & =0 \\ 4x-2 & =0 \\ 2x & =1\end{aligned}
$$

Therefore, the solution is $x=\frac{1}{2}.$

## Original repaired replay q-282270

### Captured raw original

Let $a=⟨x,1,2⟩,$ $b=⟨1,0,2⟩$ and $|\,a\times b\,|=\sqrt{5}.$ Find $x.$

$\,x=$
{{field-1}}

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 1 & 2 \\ 1 & 0 & 2\end{aligned}| \\  & =|\begin{aligned}1 & 2 \\ 0 & 2\end{aligned}|i-|\begin{aligned}x & 2 \\ 1 & 2\end{aligned}|j+|\begin{aligned}x & 1 \\ 1 & 0\end{aligned}|k \\  & =(2-0)i-(2x-2)j+(0-1)k \\  & =⟨2,2-2x,-1⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(2-2x)^{2}+(-1)^{2}} \\  & =\sqrt{4+(4{x}^{2}-8x+4)+1} \\  & =\sqrt{4{x}^{2}-8x+9}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{5} \\ \sqrt{4{x}^{2}-8x+9} & =\sqrt{5} \\ 4{x}^{2}-8x+9 & =5 \\ 4{x}^{2}-8x+4 & =0 \\ (2x-2)^{2} & =0 \\ 2x-2 & =0 \\ x & =1\end{aligned}
$$

Therefore, the solution is $x=1.$

Let $a=⟨x,1,2⟩,$ $b=⟨1,0,2⟩$ and $|\,a\times b\,|=\sqrt{5}.$ Find $x.$

$\,x=$
{{field-1}}

- $1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 1 & 2 \\ 1 & 0 & 2\end{aligned}| \\  & =|\begin{aligned}1 & 2 \\ 0 & 2\end{aligned}|i-|\begin{aligned}x & 2 \\ 1 & 2\end{aligned}|j+|\begin{aligned}x & 1 \\ 1 & 0\end{aligned}|k \\  & =(2-0)i-(2x-2)j+(0-1)k \\  & =⟨2,2-2x,-1⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(2-2x)^{2}+(-1)^{2}} \\  & =\sqrt{4+(4{x}^{2}-8x+4)+1} \\  & =\sqrt{4{x}^{2}-8x+9}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{5} \\ \sqrt{4{x}^{2}-8x+9} & =\sqrt{5} \\ 4{x}^{2}-8x+9 & =5 \\ 4{x}^{2}-8x+4 & =0 \\ (2x-2)^{2} & =0 \\ 2x-2 & =0 \\ x & =1\end{aligned}
$$

Therefore, the solution is $x=1.$

## Generated changed observed recipe q-282270

Let $a=⟨2x,1,2⟩,$ $b=⟨1,0,2⟩$ and $|\,a\times b\,|=\sqrt{5}.$ Find $2x.$

$\,2x=$
{{field-1}}

- $\frac{1}{2}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 1 & 2 \\ 1 & 0 & 2\end{aligned}| \\  & =|\begin{aligned}1 & 2 \\ 0 & 2\end{aligned}|i-|\begin{aligned}2x & 2 \\ 1 & 2\end{aligned}|j+|\begin{aligned}2x & 1 \\ 1 & 0\end{aligned}|k \\  & =(2-0)i-(4x-2)j+(0-1)k \\  & =⟨2,2-4x,-1⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(2-4x)^{2}+(-1)^{2}} \\  & =\sqrt{4+(16{x}^{2}-16x+4)+1} \\  & =\sqrt{16{x}^{2}-16x+9}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{5} \\ \sqrt{16{x}^{2}-16x+9} & =\sqrt{5} \\ 16{x}^{2}-16x+9 & =5 \\ 16{x}^{2}-16x+4 & =0 \\ (4x-2)^{2} & =0 \\ 4x-2 & =0 \\ 2x & =1\end{aligned}
$$

Therefore, the solution is $x=\frac{1}{2}.$

## Public raw evidence replay q-282276

Let $a=⟨x,4,5⟩,$ $b=⟨1,0,1⟩$ and $|\,a\times b\,|=\sqrt{33}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

- $6$
- $4$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 4 & 5 \\ 1 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}4 & 5 \\ 0 & 1\end{aligned}|i-|\begin{aligned}x & 5 \\ 1 & 1\end{aligned}|j+|\begin{aligned}x & 4 \\ 1 & 0\end{aligned}|k \\  & =(4-0)i-(x-5)j+(0-4)k \\  & =⟨4,5-x,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{4}^{2}+(5-x)^{2}+(-4)^{2}} \\  & =\sqrt{16+(25-10x+{x}^{2})+16} \\  & =\sqrt{{x}^{2}-10x+57}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{33} \\ \sqrt{{x}^{2}-10x+57} & =\sqrt{33} \\ {x}^{2}-10x+57 & =33 \\ {x}^{2}-10x+24 & =0 \\ (x-4)(x-6) & =0 \\ x & =4,\,x=6\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=4,$ $x=6.$

## Public changed raw evidence replay q-282276

Let $a=⟨2x,4,5⟩,$ $b=⟨1,0,1⟩$ and $|\,a\times b\,|=\sqrt{33}.$ Then, in **ascending order**, the possible values of $2x$ are

$\,2x=$
{{field-1}}$\,$ and $\,2x=$
{{field-2}}.

- $3$
- $2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 4 & 5 \\ 1 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}4 & 5 \\ 0 & 1\end{aligned}|i-|\begin{aligned}2x & 5 \\ 1 & 1\end{aligned}|j+|\begin{aligned}2x & 4 \\ 1 & 0\end{aligned}|k \\  & =(4-0)i-(2x-5)j+(0-4)k \\  & =⟨4,5-2x,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{4}^{2}+(5-2x)^{2}+(-4)^{2}} \\  & =\sqrt{16+(25-20x+4{x}^{2})+16} \\  & =\sqrt{4{x}^{2}-20x+57}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{33} \\ \sqrt{4{x}^{2}-20x+57} & =\sqrt{33} \\ 4{x}^{2}-20x+57 & =33 \\ 4{x}^{2}-20x+24 & =0 \\ (2x-4)(2x-6) & =0 \\ 2x & =4,\,2x=6\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=2$ $x=3.$

## Original repaired replay q-282276

### Captured raw original

Let $a=⟨x,4,5⟩,$ $b=⟨1,0,1⟩$ and $|\,a\times b\,|=\sqrt{33}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 4 & 5 \\ 1 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}4 & 5 \\ 0 & 1\end{aligned}|i-|\begin{aligned}x & 5 \\ 1 & 1\end{aligned}|j+|\begin{aligned}x & 4 \\ 1 & 0\end{aligned}|k \\  & =(4-0)i-(x-5)j+(0-4)k \\  & =⟨4,5-x,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{4}^{2}+(5-x)^{2}+(-4)^{2}} \\  & =\sqrt{16+(25-10x+{x}^{2})+16} \\  & =\sqrt{{x}^{2}-10x+57}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{33} \\ \sqrt{{x}^{2}-10x+57} & =\sqrt{33} \\ {x}^{2}-10x+57 & =33 \\ {x}^{2}-10x+24 & =0 \\ (x-4)(x-6) & =0 \\ x & =4,\,x=6\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=4,$ $x=6.$

Let $a=⟨x,4,5⟩,$ $b=⟨1,0,1⟩$ and $|\,a\times b\,|=\sqrt{33}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

- $6$
- $4$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 4 & 5 \\ 1 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}4 & 5 \\ 0 & 1\end{aligned}|i-|\begin{aligned}x & 5 \\ 1 & 1\end{aligned}|j+|\begin{aligned}x & 4 \\ 1 & 0\end{aligned}|k \\  & =(4-0)i-(x-5)j+(0-4)k \\  & =⟨4,5-x,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{4}^{2}+(5-x)^{2}+(-4)^{2}} \\  & =\sqrt{16+(25-10x+{x}^{2})+16} \\  & =\sqrt{{x}^{2}-10x+57}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{33} \\ \sqrt{{x}^{2}-10x+57} & =\sqrt{33} \\ {x}^{2}-10x+57 & =33 \\ {x}^{2}-10x+24 & =0 \\ (x-4)(x-6) & =0 \\ x & =4,\,x=6\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=4,$ $x=6.$

## Generated changed observed recipe q-282276

Let $a=⟨2x,4,5⟩,$ $b=⟨1,0,1⟩$ and $|\,a\times b\,|=\sqrt{33}.$ Then, in **ascending order**, the possible values of $2x$ are

$\,2x=$
{{field-1}}$\,$ and $\,2x=$
{{field-2}}.

- $3$
- $2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 4 & 5 \\ 1 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}4 & 5 \\ 0 & 1\end{aligned}|i-|\begin{aligned}2x & 5 \\ 1 & 1\end{aligned}|j+|\begin{aligned}2x & 4 \\ 1 & 0\end{aligned}|k \\  & =(4-0)i-(2x-5)j+(0-4)k \\  & =⟨4,5-2x,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{4}^{2}+(5-2x)^{2}+(-4)^{2}} \\  & =\sqrt{16+(25-20x+4{x}^{2})+16} \\  & =\sqrt{4{x}^{2}-20x+57}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{33} \\ \sqrt{4{x}^{2}-20x+57} & =\sqrt{33} \\ 4{x}^{2}-20x+57 & =33 \\ 4{x}^{2}-20x+24 & =0 \\ (2x-4)(2x-6) & =0 \\ 2x & =4,\,2x=6\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=2$ $x=3.$

## Public raw evidence replay q-282278

Let $a=⟨2x,1,4⟩,$ $b=⟨3,0,2⟩$ and $|\,a\times b\,|=\sqrt{157}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

- $6$
- $0$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 1 & 4 \\ 3 & 0 & 2\end{aligned}| \\  & =|\begin{aligned}1 & 4 \\ 0 & 2\end{aligned}|i-|\begin{aligned}2x & 4 \\ 3 & 2\end{aligned}|j+|\begin{aligned}2x & 1 \\ 3 & 0\end{aligned}|k \\  & =(2-0)i-(4x-12)j+(0-3)k \\  & =⟨2,12-4x,-3⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(12-4x)^{2}+(-3)^{2}} \\  & =\sqrt{4+(144-96x+16{x}^{2})+9} \\  & =\sqrt{16{x}^{2}-96x+157}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{157} \\ \sqrt{16{x}^{2}-96x+157} & =\sqrt{157} \\ 16{x}^{2}-96x+157 & =157 \\ 16{x}^{2}-96x & =0 \\ 16x(x-6) & =0 \\ x & =0,\,x=6\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=0,$ $x=6.$

## Public changed raw evidence replay q-282278

Let $a=⟨4x,1,4⟩,$ $b=⟨3,0,2⟩$ and $|\,a\times b\,|=\sqrt{157}.$ Then, in **ascending order**, the possible values of $2x$ are

$\,2x=$
{{field-1}}$\,$ and $\,2x=$
{{field-2}}.

- $3$
- $0$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4x & 1 & 4 \\ 3 & 0 & 2\end{aligned}| \\  & =|\begin{aligned}1 & 4 \\ 0 & 2\end{aligned}|i-|\begin{aligned}4x & 4 \\ 3 & 2\end{aligned}|j+|\begin{aligned}4x & 1 \\ 3 & 0\end{aligned}|k \\  & =(2-0)i-(8x-12)j+(0-3)k \\  & =⟨2,12-8x,-3⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(12-8x)^{2}+(-3)^{2}} \\  & =\sqrt{4+(144-192x+64{x}^{2})+9} \\  & =\sqrt{64{x}^{2}-192x+157}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{157} \\ \sqrt{64{x}^{2}-192x+157} & =\sqrt{157} \\ 64{x}^{2}-192x+157 & =157 \\ 64{x}^{2}-192x & =0 \\ 32x(2x-6) & =0 \\ 2x & =0,\,2x=6\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=0$ $x=3.$

## Original repaired replay q-282278

### Captured raw original

Let $a=⟨2x,1,4⟩,$ $b=⟨3,0,2⟩$ and $|\,a\times b\,|=\sqrt{157}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 1 & 4 \\ 3 & 0 & 2\end{aligned}| \\  & =|\begin{aligned}1 & 4 \\ 0 & 2\end{aligned}|i-|\begin{aligned}2x & 4 \\ 3 & 2\end{aligned}|j+|\begin{aligned}2x & 1 \\ 3 & 0\end{aligned}|k \\  & =(2-0)i-(4x-12)j+(0-3)k \\  & =⟨2,12-4x,-3⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(12-4x)^{2}+(-3)^{2}} \\  & =\sqrt{4+(144-96x+16{x}^{2})+9} \\  & =\sqrt{16{x}^{2}-96x+157}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{157} \\ \sqrt{16{x}^{2}-96x+157} & =\sqrt{157} \\ 16{x}^{2}-96x+157 & =157 \\ 16{x}^{2}-96x & =0 \\ 16x(x-6) & =0 \\ x & =0,\,x=6\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=0,$ $x=6.$

Let $a=⟨2x,1,4⟩,$ $b=⟨3,0,2⟩$ and $|\,a\times b\,|=\sqrt{157}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

- $6$
- $0$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 1 & 4 \\ 3 & 0 & 2\end{aligned}| \\  & =|\begin{aligned}1 & 4 \\ 0 & 2\end{aligned}|i-|\begin{aligned}2x & 4 \\ 3 & 2\end{aligned}|j+|\begin{aligned}2x & 1 \\ 3 & 0\end{aligned}|k \\  & =(2-0)i-(4x-12)j+(0-3)k \\  & =⟨2,12-4x,-3⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(12-4x)^{2}+(-3)^{2}} \\  & =\sqrt{4+(144-96x+16{x}^{2})+9} \\  & =\sqrt{16{x}^{2}-96x+157}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{157} \\ \sqrt{16{x}^{2}-96x+157} & =\sqrt{157} \\ 16{x}^{2}-96x+157 & =157 \\ 16{x}^{2}-96x & =0 \\ 16x(x-6) & =0 \\ x & =0,\,x=6\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=0,$ $x=6.$

## Generated changed observed recipe q-282278

Let $a=⟨4x,1,4⟩,$ $b=⟨3,0,2⟩$ and $|\,a\times b\,|=\sqrt{157}.$ Then, in **ascending order**, the possible values of $2x$ are

$\,2x=$
{{field-1}}$\,$ and $\,2x=$
{{field-2}}.

- $3$
- $0$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4x & 1 & 4 \\ 3 & 0 & 2\end{aligned}| \\  & =|\begin{aligned}1 & 4 \\ 0 & 2\end{aligned}|i-|\begin{aligned}4x & 4 \\ 3 & 2\end{aligned}|j+|\begin{aligned}4x & 1 \\ 3 & 0\end{aligned}|k \\  & =(2-0)i-(8x-12)j+(0-3)k \\  & =⟨2,12-8x,-3⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{2}^{2}+(12-8x)^{2}+(-3)^{2}} \\  & =\sqrt{4+(144-192x+64{x}^{2})+9} \\  & =\sqrt{64{x}^{2}-192x+157}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{157} \\ \sqrt{64{x}^{2}-192x+157} & =\sqrt{157} \\ 64{x}^{2}-192x+157 & =157 \\ 64{x}^{2}-192x & =0 \\ 32x(2x-6) & =0 \\ 2x & =0,\,2x=6\end{aligned}
$$

Therefore, in ascending order, the solutions are $x=0$ $x=3.$

## Public raw evidence replay q-77427

Let $a=⟨2,x,1⟩,$ $b=⟨1,-x,3⟩$ and $|\,a\times b\,|=10.$ Find $x.$

- $x=\pm \sqrt{2}$
- $x=\pm 4$
- $x=\pm 2$
- $x=\pm \sqrt{3}$
- $x=\pm 3$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2 & x & 1 \\ 1 & -x & 3\end{aligned}| \\  & =|\begin{aligned}x & 1 \\ -x & 3\end{aligned}|i-|\begin{aligned}2 & 1 \\ 1 & 3\end{aligned}|j+|\begin{aligned}2 & x \\ 1 & -x\end{aligned}|k \\  & =(3x+x)i-(6-1)j+(-2x-x)k \\  & =⟨4x,-5,-3x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(4x)^{2}+(-5)^{2}+(-3x)^{2}} \\  & =\sqrt{16{x}^{2}+25+9{x}^{2}} \\  & =\sqrt{25({x}^{2}+1)}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =10 \\ \sqrt{25({x}^{2}+1)} & =10 \\ 25({x}^{2}+1) & =100 \\ {x}^{2}+1 & =4 \\ {x}^{2} & =3.\end{aligned}
$$

Therefore, the solutions are $x=\pm \sqrt{3}.$

## Public changed raw evidence replay q-77427

Let $a=⟨2,2x,1⟩,$ $b=⟨1,-2x,3⟩$ and $|\,a\times b\,|=10.$ Find $2x.$

- $x=\pm 1$
- $x=\pm 2$
- $x=\pm \frac{\sqrt{2}}{2}$
- $x=\pm \frac{3}{2}$
- $x=\pm \frac{\sqrt{3}}{2}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2 & 2x & 1 \\ 1 & -2x & 3\end{aligned}| \\  & =|\begin{aligned}2x & 1 \\ -2x & 3\end{aligned}|i-|\begin{aligned}2 & 1 \\ 1 & 3\end{aligned}|j+|\begin{aligned}2 & 2x \\ 1 & -2x\end{aligned}|k \\  & =(6x+2x)i-(6-1)j+(-4x-2x)k \\  & =⟨8x,-5,-6x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(8x)^{2}+(-5)^{2}+(-6x)^{2}} \\  & =\sqrt{64{x}^{2}+25+36{x}^{2}} \\  & =\sqrt{25(4{x}^{2}+1)}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =10 \\ \sqrt{25(4{x}^{2}+1)} & =10 \\ 25(4{x}^{2}+1) & =100 \\ 4{x}^{2}+1 & =4 \\ 4{x}^{2} & =3.\end{aligned}
$$

Therefore, the solutions are $x=\pm \frac{\sqrt{3}}{2}.$

## Original repaired replay q-77427

### Captured raw original

Let $a=⟨2,x,1⟩,$ $b=⟨1,-x,3⟩$ and $|\,a\times b\,|=10.$ Find $x.$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2 & x & 1 \\ 1 & -x & 3\end{aligned}| \\  & =|\begin{aligned}x & 1 \\ -x & 3\end{aligned}|i-|\begin{aligned}2 & 1 \\ 1 & 3\end{aligned}|j+|\begin{aligned}2 & x \\ 1 & -x\end{aligned}|k \\  & =(3x+x)i-(6-1)j+(-2x-x)k \\  & =⟨4x,-5,-3x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(4x)^{2}+(-5)^{2}+(-3x)^{2}} \\  & =\sqrt{16{x}^{2}+25+9{x}^{2}} \\  & =\sqrt{25({x}^{2}+1)}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =10 \\ \sqrt{25({x}^{2}+1)} & =10 \\ 25({x}^{2}+1) & =100 \\ {x}^{2}+1 & =4 \\ {x}^{2} & =3.\end{aligned}
$$

Therefore, the solutions are $x=\pm \sqrt{3}.$

Let $a=⟨2,x,1⟩,$ $b=⟨1,-x,3⟩$ and $|\,a\times b\,|=10.$ Find $x.$

- $x=\pm \sqrt{2}$
- $x=\pm 4$
- $x=\pm 2$
- $x=\pm \sqrt{3}$
- $x=\pm 3$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2 & x & 1 \\ 1 & -x & 3\end{aligned}| \\  & =|\begin{aligned}x & 1 \\ -x & 3\end{aligned}|i-|\begin{aligned}2 & 1 \\ 1 & 3\end{aligned}|j+|\begin{aligned}2 & x \\ 1 & -x\end{aligned}|k \\  & =(3x+x)i-(6-1)j+(-2x-x)k \\  & =⟨4x,-5,-3x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(4x)^{2}+(-5)^{2}+(-3x)^{2}} \\  & =\sqrt{16{x}^{2}+25+9{x}^{2}} \\  & =\sqrt{25({x}^{2}+1)}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =10 \\ \sqrt{25({x}^{2}+1)} & =10 \\ 25({x}^{2}+1) & =100 \\ {x}^{2}+1 & =4 \\ {x}^{2} & =3.\end{aligned}
$$

Therefore, the solutions are $x=\pm \sqrt{3}.$

## Generated changed observed recipe q-77427

Let $a=⟨2,2x,1⟩,$ $b=⟨1,-2x,3⟩$ and $|\,a\times b\,|=10.$ Find $2x.$

- $x=\pm 1$
- $x=\pm 2$
- $x=\pm \frac{\sqrt{2}}{2}$
- $x=\pm \frac{3}{2}$
- $x=\pm \frac{\sqrt{3}}{2}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2 & 2x & 1 \\ 1 & -2x & 3\end{aligned}| \\  & =|\begin{aligned}2x & 1 \\ -2x & 3\end{aligned}|i-|\begin{aligned}2 & 1 \\ 1 & 3\end{aligned}|j+|\begin{aligned}2 & 2x \\ 1 & -2x\end{aligned}|k \\  & =(6x+2x)i-(6-1)j+(-4x-2x)k \\  & =⟨8x,-5,-6x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(8x)^{2}+(-5)^{2}+(-6x)^{2}} \\  & =\sqrt{64{x}^{2}+25+36{x}^{2}} \\  & =\sqrt{25(4{x}^{2}+1)}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =10 \\ \sqrt{25(4{x}^{2}+1)} & =10 \\ 25(4{x}^{2}+1) & =100 \\ 4{x}^{2}+1 & =4 \\ 4{x}^{2} & =3.\end{aligned}
$$

Therefore, the solutions are $x=\pm \frac{\sqrt{3}}{2}.$

## Public raw evidence replay q-77429

Let $a=⟨2,0,-4⟩,$ $b=⟨-1,1,2x⟩$ and $|\,a\times b\,|=2\sqrt{5}.$ Find $x.$

- $x=2$
- $x=\pm 1$
- $x=-1,\,2$
- $x=-1,4$
- $x=1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2 & 0 & -4 \\ -1 & 1 & 2x\end{aligned}| \\  & =|\begin{aligned}0 & -4 \\ 1 & 2x\end{aligned}|i-|\begin{aligned}2 & -4 \\ -1 & 2x\end{aligned}|j+|\begin{aligned}2 & 0 \\ -1 & 1\end{aligned}|k \\  & =(0+4)i-(4x-4)j+(2-0)k \\  & =⟨4,-4x+4,2⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{4}^{2}+(-4x+4)^{2}+{2}^{2}} \\  & =\sqrt{16+16{x}^{2}-32x+16+4} \\  & =\sqrt{16{x}^{2}-32x+36}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =2\sqrt{5} \\ \sqrt{16{x}^{2}-32x+36} & =2\sqrt{5} \\ 16{x}^{2}-32x+36 & =20 \\ 16{x}^{2}-32x+16 & =0 \\ 16({x}^{2}-2x+1) & =0 \\ {x}^{2}-2x+1 & =0 \\ (x-1)^{2} & =0 \\ x-1 & =0 \\ x & =1.\end{aligned}
$$

Therefore, the solution is $x=1.$

## Public changed raw evidence replay q-77429

Let $a=⟨2,0,-4⟩,$ $b=⟨-1,1,4x⟩$ and $|\,a\times b\,|=2\sqrt{5}.$ Find $2x.$

- $x=- \frac{1}{2},\,1$
- $x=\pm \frac{1}{2}$
- $x=1$
- $x=\frac{1}{2}$
- $x=- \frac{1}{2},\,2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2 & 0 & -4 \\ -1 & 1 & 4x\end{aligned}| \\  & =|\begin{aligned}0 & -4 \\ 1 & 4x\end{aligned}|i-|\begin{aligned}2 & -4 \\ -1 & 4x\end{aligned}|j+|\begin{aligned}2 & 0 \\ -1 & 1\end{aligned}|k \\  & =(0+4)i-(8x-4)j+(2-0)k \\  & =⟨4,-8x+4,2⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{4}^{2}+(-8x+4)^{2}+{2}^{2}} \\  & =\sqrt{16+64{x}^{2}-64x+16+4} \\  & =\sqrt{64{x}^{2}-64x+36}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =2\sqrt{5} \\ \sqrt{64{x}^{2}-64x+36} & =2\sqrt{5} \\ 64{x}^{2}-64x+36 & =20 \\ 64{x}^{2}-64x+16 & =0 \\ 16(4{x}^{2}-4x+1) & =0 \\ 4{x}^{2}-4x+1 & =0 \\ (2x-1)^{2} & =0 \\ 2x-1 & =0 \\ 2x & =1.\end{aligned}
$$

Therefore, the solution is $x=\frac{1}{2}.$

## Original repaired replay q-77429

### Captured raw original

Let $a=⟨2,0,-4⟩,$ $b=⟨-1,1,2x⟩$ and $|\,a\times b\,|=2\sqrt{5}.$ Find $x.$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2 & 0 & -4 \\ -1 & 1 & 2x\end{aligned}| \\  & =|\begin{aligned}0 & -4 \\ 1 & 2x\end{aligned}|i-|\begin{aligned}2 & -4 \\ -1 & 2x\end{aligned}|j+|\begin{aligned}2 & 0 \\ -1 & 1\end{aligned}|k \\  & =(0+4)i-(4x-4)j+(2-0)k \\  & =⟨4,-4x+4,2⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{4}^{2}+(-4x+4)^{2}+{2}^{2}} \\  & =\sqrt{16+16{x}^{2}-32x+16+4} \\  & =\sqrt{16{x}^{2}-32x+36}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =2\sqrt{5} \\ \sqrt{16{x}^{2}-32x+36} & =2\sqrt{5} \\ 16{x}^{2}-32x+36 & =20 \\ 16{x}^{2}-32x+16 & =0 \\ 16({x}^{2}-2x+1) & =0 \\ {x}^{2}-2x+1 & =0 \\ (x-1)^{2} & =0 \\ x-1 & =0 \\ x & =1.\end{aligned}
$$

Therefore, the solution is $x=1.$

Let $a=⟨2,0,-4⟩,$ $b=⟨-1,1,2x⟩$ and $|\,a\times b\,|=2\sqrt{5}.$ Find $x.$

- $x=2$
- $x=\pm 1$
- $x=-1,\,2$
- $x=-1,4$
- $x=1$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2 & 0 & -4 \\ -1 & 1 & 2x\end{aligned}| \\  & =|\begin{aligned}0 & -4 \\ 1 & 2x\end{aligned}|i-|\begin{aligned}2 & -4 \\ -1 & 2x\end{aligned}|j+|\begin{aligned}2 & 0 \\ -1 & 1\end{aligned}|k \\  & =(0+4)i-(4x-4)j+(2-0)k \\  & =⟨4,-4x+4,2⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{4}^{2}+(-4x+4)^{2}+{2}^{2}} \\  & =\sqrt{16+16{x}^{2}-32x+16+4} \\  & =\sqrt{16{x}^{2}-32x+36}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =2\sqrt{5} \\ \sqrt{16{x}^{2}-32x+36} & =2\sqrt{5} \\ 16{x}^{2}-32x+36 & =20 \\ 16{x}^{2}-32x+16 & =0 \\ 16({x}^{2}-2x+1) & =0 \\ {x}^{2}-2x+1 & =0 \\ (x-1)^{2} & =0 \\ x-1 & =0 \\ x & =1.\end{aligned}
$$

Therefore, the solution is $x=1.$

## Generated changed observed recipe q-77429

Let $a=⟨2,0,-4⟩,$ $b=⟨-1,1,4x⟩$ and $|\,a\times b\,|=2\sqrt{5}.$ Find $2x.$

- $x=- \frac{1}{2},\,1$
- $x=\pm \frac{1}{2}$
- $x=1$
- $x=\frac{1}{2}$
- $x=- \frac{1}{2},\,2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2 & 0 & -4 \\ -1 & 1 & 4x\end{aligned}| \\  & =|\begin{aligned}0 & -4 \\ 1 & 4x\end{aligned}|i-|\begin{aligned}2 & -4 \\ -1 & 4x\end{aligned}|j+|\begin{aligned}2 & 0 \\ -1 & 1\end{aligned}|k \\  & =(0+4)i-(8x-4)j+(2-0)k \\  & =⟨4,-8x+4,2⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{4}^{2}+(-8x+4)^{2}+{2}^{2}} \\  & =\sqrt{16+64{x}^{2}-64x+16+4} \\  & =\sqrt{64{x}^{2}-64x+36}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =2\sqrt{5} \\ \sqrt{64{x}^{2}-64x+36} & =2\sqrt{5} \\ 64{x}^{2}-64x+36 & =20 \\ 64{x}^{2}-64x+16 & =0 \\ 16(4{x}^{2}-4x+1) & =0 \\ 4{x}^{2}-4x+1 & =0 \\ (2x-1)^{2} & =0 \\ 2x-1 & =0 \\ 2x & =1.\end{aligned}
$$

Therefore, the solution is $x=\frac{1}{2}.$

## Public raw evidence replay q-69776

Let $a=⟨4,2,-1⟩$, $b=⟨x,2,-1⟩$ and $|\,a\times b\,|=\sqrt{20}.$ Find $x.$

- $x=2,\,6$
- $x=-3,\,2$
- $x=-3,\,6$
- $x=\pm 6$
- $x=\pm 3$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4 & 2 & -1 \\ x & 2 & -1\end{aligned}| \\  & =|\begin{aligned}2 & -1 \\ 2 & -1\end{aligned}|i-|\begin{aligned}4 & -1 \\ x & -1\end{aligned}|j+|\begin{aligned}4 & 2 \\ x & 2\end{aligned}|k \\  & =(-2+2)i-(-4+x)j+(8-2x)k \\  & =⟨0,4-x,8-2x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{0}^{2}+(4-x)^{2}+(8-2x)^{2}} \\  & =\sqrt{16-8x+{x}^{2}+64-32x+4{x}^{2}} \\  & =\sqrt{5{x}^{2}-40x+80}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{20} \\ \sqrt{5{x}^{2}-40x+80} & =\sqrt{20} \\ 5{x}^{2}-40x+80 & =20 \\ 5{x}^{2}-40x+60 & =0 \\ {x}^{2}-8x+12 & =0 \\ (x-2)(x-6) & =0.\end{aligned}
$$

Therefore, the solutions are $x=2,\,6.$

## Public changed raw evidence replay q-69776

Let $a=⟨4,2,-1⟩$, $b=⟨2x,2,-1⟩$ and $|\,a\times b\,|=\sqrt{20}.$ Find $2x.$

- $x=- \frac{3}{2},\,3$
- $x=- \frac{3}{2},\,1$
- $x=1,\,3$
- $x=\pm \frac{3}{2}$
- $x=\pm 3$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4 & 2 & -1 \\ 2x & 2 & -1\end{aligned}| \\  & =|\begin{aligned}2 & -1 \\ 2 & -1\end{aligned}|i-|\begin{aligned}4 & -1 \\ 2x & -1\end{aligned}|j+|\begin{aligned}4 & 2 \\ 2x & 2\end{aligned}|k \\  & =(-2+2)i-(-4+2x)j+(8-4x)k \\  & =⟨0,4-2x,8-4x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{0}^{2}+(4-2x)^{2}+(8-4x)^{2}} \\  & =\sqrt{16-16x+4{x}^{2}+64-64x+16{x}^{2}} \\  & =\sqrt{20{x}^{2}-80x+80}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{20} \\ \sqrt{20{x}^{2}-80x+80} & =\sqrt{20} \\ 20{x}^{2}-80x+80 & =20 \\ 20{x}^{2}-80x+60 & =0 \\ 4{x}^{2}-16x+12 & =0 \\ (2x-2)(2x-6) & =0.\end{aligned}
$$

Therefore, the solutions are $x=1,\,3.$

## Original repaired replay q-69776

### Captured raw original

Let $a=⟨4,2,-1⟩$, $b=⟨x,2,-1⟩$ and $|\,a\times b\,|=\sqrt{20}.$ Find $x.$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4 & 2 & -1 \\ x & 2 & -1\end{aligned}| \\  & =|\begin{aligned}2 & -1 \\ 2 & -1\end{aligned}|i-|\begin{aligned}4 & -1 \\ x & -1\end{aligned}|j+|\begin{aligned}4 & 2 \\ x & 2\end{aligned}|k \\  & =(-2+2)i-(-4+x)j+(8-2x)k \\  & =⟨0,4-x,8-2x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{0}^{2}+(4-x)^{2}+(8-2x)^{2}} \\  & =\sqrt{16-8x+{x}^{2}+64-32x+4{x}^{2}} \\  & =\sqrt{5{x}^{2}-40x+80}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{20} \\ \sqrt{5{x}^{2}-40x+80} & =\sqrt{20} \\ 5{x}^{2}-40x+80 & =20 \\ 5{x}^{2}-40x+60 & =0 \\ {x}^{2}-8x+12 & =0 \\ (x-2)(x-6) & =0.\end{aligned}
$$

Therefore, the solutions are $x=2,\,6.$

Let $a=⟨4,2,-1⟩$, $b=⟨x,2,-1⟩$ and $|\,a\times b\,|=\sqrt{20}.$ Find $x.$

- $x=2,\,6$
- $x=-3,\,2$
- $x=-3,\,6$
- $x=\pm 6$
- $x=\pm 3$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4 & 2 & -1 \\ x & 2 & -1\end{aligned}| \\  & =|\begin{aligned}2 & -1 \\ 2 & -1\end{aligned}|i-|\begin{aligned}4 & -1 \\ x & -1\end{aligned}|j+|\begin{aligned}4 & 2 \\ x & 2\end{aligned}|k \\  & =(-2+2)i-(-4+x)j+(8-2x)k \\  & =⟨0,4-x,8-2x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{0}^{2}+(4-x)^{2}+(8-2x)^{2}} \\  & =\sqrt{16-8x+{x}^{2}+64-32x+4{x}^{2}} \\  & =\sqrt{5{x}^{2}-40x+80}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{20} \\ \sqrt{5{x}^{2}-40x+80} & =\sqrt{20} \\ 5{x}^{2}-40x+80 & =20 \\ 5{x}^{2}-40x+60 & =0 \\ {x}^{2}-8x+12 & =0 \\ (x-2)(x-6) & =0.\end{aligned}
$$

Therefore, the solutions are $x=2,\,6.$

## Generated changed observed recipe q-69776

Let $a=⟨4,2,-1⟩$, $b=⟨2x,2,-1⟩$ and $|\,a\times b\,|=\sqrt{20}.$ Find $2x.$

- $x=- \frac{3}{2},\,3$
- $x=- \frac{3}{2},\,1$
- $x=1,\,3$
- $x=\pm \frac{3}{2}$
- $x=\pm 3$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 4 & 2 & -1 \\ 2x & 2 & -1\end{aligned}| \\  & =|\begin{aligned}2 & -1 \\ 2 & -1\end{aligned}|i-|\begin{aligned}4 & -1 \\ 2x & -1\end{aligned}|j+|\begin{aligned}4 & 2 \\ 2x & 2\end{aligned}|k \\  & =(-2+2)i-(-4+2x)j+(8-4x)k \\  & =⟨0,4-2x,8-4x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{{0}^{2}+(4-2x)^{2}+(8-4x)^{2}} \\  & =\sqrt{16-16x+4{x}^{2}+64-64x+16{x}^{2}} \\  & =\sqrt{20{x}^{2}-80x+80}.\end{aligned}
$$

Lastly, we solve for $2x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{20} \\ \sqrt{20{x}^{2}-80x+80} & =\sqrt{20} \\ 20{x}^{2}-80x+80 & =20 \\ 20{x}^{2}-80x+60 & =0 \\ 4{x}^{2}-16x+12 & =0 \\ (2x-2)(2x-6) & =0.\end{aligned}
$$

Therefore, the solutions are $x=1,\,3.$

## Authored easy seed 0

Let $a=⟨2,1,2x⟩,$ $b=⟨0,1,x⟩$ and $|\,a\times b\,|=7.$ Find $x.$

- $x=-3$
- $x=3$
- $x=\pm 3$
- $x=\pm \sqrt{3}$
- $x=\pm 9$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2 & 1 & 2x \\ 0 & 1 & x\end{aligned}| \\  & =|\begin{aligned}1 & 2x \\ 1 & x\end{aligned}|i-|\begin{aligned}2 & 2x \\ 0 & x\end{aligned}|j+|\begin{aligned}2 & 1 \\ 0 & 1\end{aligned}|k \\  & =(1\cdot (x)-2x\cdot (1))i-(2\cdot (x)-2x\cdot (0))j+(2\cdot (1)-1\cdot (0))k \\  & =(x-(2x))i-(2x-(0))j+(2-(0))k \\  & =⟨-x,- 2x,2⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-x)^{2}+(- 2x)^{2}+(2)^{2}} \\  & =\sqrt{(x^{2})+(4x^{2})+(4)} \\  & =\sqrt{5x^{2} + 4}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =7 \\ \sqrt{5x^{2} + 4} & =7 \\ 5x^{2} + 4 & =49 \\ 5x^{2} - 45 & =0 \\ 5 \left(x - 3\right) \left(x + 3\right) & =0 \\ x & =-3,\,3.\end{aligned}
$$

Therefore, the solutions are $x=\pm 3.$

Checking in the original magnitude equation: $|\,a\times b\,|_{x=-3}=7=7$ $|\,a\times b\,|_{x=3}=7=7$.

## Authored easy seed 1

Let $a=⟨1,1,3x⟩,$ $b=⟨0,1,x⟩$ and $|\,a\times b\,|=\sqrt{46}.$ Find $x.$

- $x=-3$
- $x=\pm 9$
- $x=\pm \sqrt{3}$
- $x=\pm 3$
- $x=3$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 1 & 1 & 3x \\ 0 & 1 & x\end{aligned}| \\  & =|\begin{aligned}1 & 3x \\ 1 & x\end{aligned}|i-|\begin{aligned}1 & 3x \\ 0 & x\end{aligned}|j+|\begin{aligned}1 & 1 \\ 0 & 1\end{aligned}|k \\  & =(1\cdot (x)-3x\cdot (1))i-(1\cdot (x)-3x\cdot (0))j+(1\cdot (1)-1\cdot (0))k \\  & =(x-(3x))i-(x-(0))j+(1-(0))k \\  & =⟨- 2x,-x,1⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(- 2x)^{2}+(-x)^{2}+(1)^{2}} \\  & =\sqrt{(4x^{2})+(x^{2})+(1)} \\  & =\sqrt{5x^{2} + 1}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{46} \\ \sqrt{5x^{2} + 1} & =\sqrt{46} \\ 5x^{2} + 1 & =46 \\ 5x^{2} - 45 & =0 \\ 5 \left(x - 3\right) \left(x + 3\right) & =0 \\ x & =-3,\,3.\end{aligned}
$$

Therefore, the solutions are $x=\pm 3.$

Checking in the original magnitude equation: $|\,a\times b\,|_{x=-3}=\sqrt{46}=\sqrt{46}$ $|\,a\times b\,|_{x=3}=\sqrt{46}=\sqrt{46}$.

## Authored moderate seed 0

Let $a=⟨- 2x,3,1⟩,$ $b=⟨-x,2,2⟩$ and $|\,a\times b\,|=\sqrt{66}.$ Find $x.$

- $x=- \sqrt{5}$
- $x=\sqrt{5}$
- $x=\pm \sqrt{5}$
- $x=\pm \sqrt[4]{5}$
- $x=\pm 5$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ - 2x & 3 & 1 \\ -x & 2 & 2\end{aligned}| \\  & =|\begin{aligned}3 & 1 \\ 2 & 2\end{aligned}|i-|\begin{aligned}- 2x & 1 \\ -x & 2\end{aligned}|j+|\begin{aligned}- 2x & 3 \\ -x & 2\end{aligned}|k \\  & =(3\cdot (2)-1\cdot (2))i-(- 2x\cdot (2)-1\cdot (-x))j+(- 2x\cdot (2)-3\cdot (-x))k \\  & =(6-(2))i-(- 4x-(-x))j+(- 4x-(- 3x))k \\  & =⟨4,3x,-x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(4)^{2}+(3x)^{2}+(-x)^{2}} \\  & =\sqrt{(16)+(9x^{2})+(x^{2})} \\  & =\sqrt{10x^{2} + 16}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{66} \\ \sqrt{10x^{2} + 16} & =\sqrt{66} \\ 10x^{2} + 16 & =66 \\ 10x^{2} - 50 & =0 \\ 10 \left(x^{2} - 5\right) & =0 \\ x & =- \sqrt{5},\,\sqrt{5}.\end{aligned}
$$

Therefore, the solutions are $x=\pm \sqrt{5}.$

Checking in the original magnitude equation: $|\,a\times b\,|_{x=- \sqrt{5}}=\sqrt{66}=\sqrt{66}$ $|\,a\times b\,|_{x=\sqrt{5}}=\sqrt{66}=\sqrt{66}$.

## Authored moderate seed 1

Let $a=⟨3x,3,1⟩,$ $b=⟨x,2,-2⟩$ and $|\,a\times b\,|=2 \sqrt{74}.$ Find $x.$

- $x=-2$
- $x=\pm 4$
- $x=\pm \sqrt{2}$
- $x=\pm 2$
- $x=2$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 3x & 3 & 1 \\ x & 2 & -2\end{aligned}| \\  & =|\begin{aligned}3 & 1 \\ 2 & -2\end{aligned}|i-|\begin{aligned}3x & 1 \\ x & -2\end{aligned}|j+|\begin{aligned}3x & 3 \\ x & 2\end{aligned}|k \\  & =(3\cdot (-2)-1\cdot (2))i-(3x\cdot (-2)-1\cdot (x))j+(3x\cdot (2)-3\cdot (x))k \\  & =(-6-(2))i-(- 6x-(x))j+(6x-(3x))k \\  & =⟨-8,7x,3x⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(-8)^{2}+(7x)^{2}+(3x)^{2}} \\  & =\sqrt{(64)+(49x^{2})+(9x^{2})} \\  & =\sqrt{58x^{2} + 64}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =2 \sqrt{74} \\ \sqrt{58x^{2} + 64} & =2 \sqrt{74} \\ 58x^{2} + 64 & =296 \\ 58x^{2} - 232 & =0 \\ 58 \left(x - 2\right) \left(x + 2\right) & =0 \\ x & =-2,\,2.\end{aligned}
$$

Therefore, the solutions are $x=\pm 2.$

Checking in the original magnitude equation: $|\,a\times b\,|_{x=-2}=2 \sqrt{74}=2 \sqrt{74}$ $|\,a\times b\,|_{x=2}=2 \sqrt{74}=2 \sqrt{74}$.

## Authored hard seed 0

Let $a=⟨2x,2,1⟩,$ $b=⟨2,0,3⟩$ and $|\,a\times b\,|=2 \sqrt{22}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

- $- \frac{2}{3}$
- $\frac{4}{3}$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ 2x & 2 & 1 \\ 2 & 0 & 3\end{aligned}| \\  & =|\begin{aligned}2 & 1 \\ 0 & 3\end{aligned}|i-|\begin{aligned}2x & 1 \\ 2 & 3\end{aligned}|j+|\begin{aligned}2x & 2 \\ 2 & 0\end{aligned}|k \\  & =(2\cdot (3)-1\cdot (0))i-(2x\cdot (3)-1\cdot (2))j+(2x\cdot (0)-2\cdot (2))k \\  & =(6-(0))i-(6x-(2))j+(0-(4))k \\  & =⟨6,- 6x + 2,-4⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(6)^{2}+(- 6x + 2)^{2}+(-4)^{2}} \\  & =\sqrt{(36)+(36x^{2} - 24x + 4)+(16)} \\  & =\sqrt{36x^{2} - 24x + 56}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =2 \sqrt{22} \\ \sqrt{36x^{2} - 24x + 56} & =2 \sqrt{22} \\ 36x^{2} - 24x + 56 & =88 \\ 36x^{2} - 24x - 32 & =0 \\ 4 \left(3x - 4\right) \left(3x + 2\right) & =0 \\ x & =- \frac{2}{3},\,\frac{4}{3}.\end{aligned}
$$

Therefore, the solutions are $x=- \frac{2}{3},\,\frac{4}{3}.$

Checking in the original magnitude equation: $|\,a\times b\,|_{x=- \frac{2}{3}}=2 \sqrt{22}=2 \sqrt{22}$ $|\,a\times b\,|_{x=\frac{4}{3}}=2 \sqrt{22}=2 \sqrt{22}$.

## Authored hard seed 1

Let $a=⟨x,3,1⟩,$ $b=⟨2,0,1⟩$ and $|\,a\times b\,|=\sqrt{46}.$ Then, in **ascending order**, the possible values of $x$ are

$\,x=$
{{field-1}}$\,$ and $\,x=$
{{field-2}}.

- $1$
- $3$

Using the determinant formula, we get

$$
\begin{aligned}a\times b & =|\begin{aligned}i & j & k \\ x & 3 & 1 \\ 2 & 0 & 1\end{aligned}| \\  & =|\begin{aligned}3 & 1 \\ 0 & 1\end{aligned}|i-|\begin{aligned}x & 1 \\ 2 & 1\end{aligned}|j+|\begin{aligned}x & 3 \\ 2 & 0\end{aligned}|k \\  & =(3\cdot (1)-1\cdot (0))i-(x\cdot (1)-1\cdot (2))j+(x\cdot (0)-3\cdot (2))k \\  & =(3-(0))i-(x-(2))j+(0-(6))k \\  & =⟨3,-x + 2,-6⟩.\end{aligned}
$$

Now, computing the magnitude, we get

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{(3)^{2}+(-x + 2)^{2}+(-6)^{2}} \\  & =\sqrt{(9)+(x^{2} - 4x + 4)+(36)} \\  & =\sqrt{x^{2} - 4x + 49}.\end{aligned}
$$

Lastly, we solve for $x$ the following equation:

$$
\begin{aligned}|\,a\times b\,| & =\sqrt{46} \\ \sqrt{x^{2} - 4x + 49} & =\sqrt{46} \\ x^{2} - 4x + 49 & =46 \\ x^{2} - 4x + 3 & =0 \\ \left(x - 3\right) \left(x - 1\right) & =0 \\ x & =1,\,3.\end{aligned}
$$

Therefore, the solutions are $x=1,\,3.$

Checking in the original magnitude equation: $|\,a\times b\,|_{x=1}=\sqrt{46}=\sqrt{46}$ $|\,a\times b\,|_{x=3}=\sqrt{46}=\sqrt{46}$.