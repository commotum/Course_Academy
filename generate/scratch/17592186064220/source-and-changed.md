## q-19394 original

Evaluate the integral ${\int }_{0}^{1}\frac{2}{\sqrt{2-{x}^{2}}}\,\text{d}x.$

Field selection (radio)

- $\frac{3\pi }{2}$
- $\frac{\pi }{2}$ (correct)
- $\frac{\pi }{4}$
- $\frac{\pi }{6}$
- $\frac{\pi }{3}$

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{0}^{1}\frac{2}{\sqrt{2-{x}^{2}}}\,\text{d}x & =2{\int }_{0}^{1}\frac{1}{\sqrt{2\cdot (1-{x}^{2}/2)}}\,\text{d}x \\  & =\frac{2}{\sqrt{2}}{\int }_{0}^{1}\frac{1}{\sqrt{1-{x}^{2}/2}}\,\text{d}x \\  & =\sqrt{2}{\int }_{0}^{1}\frac{1}{\sqrt{1-(x/\sqrt{2})^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-{u}^{2}}}\text{d}u=\operatorname{arcsin}⁡(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(\frac{x}{\sqrt{2}})}^{2}.$

So, let's substitute $u=\frac{x}{\sqrt{2}}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{\sqrt{2}}\,⟹\,\text{d}x=\sqrt{2}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\sqrt{2}}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{1}\frac{2}{\sqrt{2-{x}^{2}}}\,\text{d}x & =\sqrt{2}{\int }_{0}^{1}\frac{1}{\sqrt{1-(x/\sqrt{2})^{2}}}\,\text{d}x \\  & =\sqrt{2}{\int }_{0}^{\sqrt{2}/2}\frac{1}{\sqrt{1-{u}^{2}}}\cdot (\sqrt{2}\,\text{d}u) \\  & =2{\int }_{0}^{\sqrt{2}/2}\frac{\text{d}u}{\sqrt{1-{u}^{2}}} \\  & =2\operatorname{arcsin}⁡u{|}_{0}^{\sqrt{2}/2} \\  & =2\operatorname{arcsin}⁡(\frac{\sqrt{2}}{2})-2\operatorname{arcsin}⁡(0) \\  & =2\cdot \frac{\pi }{4} \\  & =\frac{\pi }{2}\end{aligned}
$$

---

## q-19394 {'h': 2, 'k': 3}

Evaluate the integral $\int_{0}^{2} \frac{6}{\sqrt{8 - x^{2}}}\,\text{d}x.$

Field selection (radio)

- $\frac{9 \pi}{2}$
- $\frac{3 \pi}{2}$ (correct)
- $\frac{3 \pi}{4}$
- $\frac{\pi}{2}$
- $\pi$

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{0}^{2} \frac{6}{\sqrt{8 - x^{2}}}\,\text{d}x &= \int_{0}^{2} \frac{6}{\sqrt{8(1-\frac{x^{2}}{8})}}\,\text{d}x \\ &= \frac{3 \sqrt{2}}{2}\int_{0}^{2} \frac{1}{\sqrt{1-\frac{x^{2}}{8}}}\,\text{d}x \\ &= \frac{3 \sqrt{2}}{2}\int_{0}^{2} \frac{1}{\sqrt{1-(\frac{\sqrt{2} x}{4})^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{\sqrt{2} x}{4})^{2}.$

So, let's substitute $u=\frac{\sqrt{2} x}{4}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{\sqrt{2}}{4}\quad\Longrightarrow\quad\text{d}x=2 \sqrt{2}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $2$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\sqrt{2}}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{2} \frac{6}{\sqrt{8 - x^{2}}}\,\text{d}x &= \frac{3 \sqrt{2}}{2}\int_{0}^{2} \frac{1}{\sqrt{1-(\frac{\sqrt{2} x}{4})^{2}}}\,\text{d}x \\ &= \frac{3 \sqrt{2}}{2}\int_{0}^{\frac{\sqrt{2}}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\cdot (2 \sqrt{2})\,\text{d}u \\ &= 6\int_{0}^{\frac{\sqrt{2}}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u \\ &= \left[6\operatorname{arcsin}(u)\right]_{0}^{\frac{\sqrt{2}}{2}} \\ &= 6\operatorname{arcsin}(\frac{\sqrt{2}}{2})-(6\operatorname{arcsin}(0)) \\ &= \frac{3 \pi}{2}-(0) \\ &= \frac{3 \pi}{2}\end{aligned}
$$

---

## q-19397 original

Evaluate the integral ${\int }_{0}^{7}\frac{9}{2+8{x}^{2}}\,\text{d}x.$

Field selection (radio)

- $\frac{9}{2}\operatorname{arctan}⁡(14)$
- $\frac{9}{4}\operatorname{arctan}⁡(7)$
- $\frac{9}{2}\operatorname{arctan}⁡(7)$
- $\frac{9}{4}\operatorname{arctan}⁡(14)$ (correct)
- $9\operatorname{arctan}⁡(14)$

Note that we can rewrite this integral as

$$
{\int }_{0}^{7}\frac{9}{2+8{x}^{2}}\,\text{d}x=\frac{9}{2}{\int }_{0}^{7}\frac{1}{1+4{x}^{2}}\,\text{d}x.
$$

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+{u}^{2}}\text{d}u=\operatorname{arctan}⁡u+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $4{x}^{2}=(2x)^{2}.$

So, let's substitute $u=2x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=2\,⟹\,\text{d}x=\frac{1}{2}\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $7$ |
| --- | --- | --- |
| $u$ | $0$ | $14$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{7}\frac{9}{2+8{x}^{2}}\,\text{d}x & =\frac{9}{2}{\int }_{0}^{7}\frac{1}{1+(2x)^{2}}\,\text{d}x \\  & =\frac{9}{2}{\int }_{0}^{14}\frac{1}{1+{u}^{2}}\,\cdot (\frac{1}{2}\text{d}u) \\  & =\frac{9}{4}{\int }_{0}^{14}\frac{\text{d}u}{1+{u}^{2}} \\  & =\frac{9}{4}\operatorname{arctan}⁡u{|}_{0}^{14} \\  & =\frac{9}{4}\operatorname{arctan}⁡(14)-\frac{9}{4}\operatorname{arctan}⁡(0) \\  & =\frac{9}{4}\operatorname{arctan}⁡(14)\end{aligned}
$$

---

## q-19397 {'h': 2, 'k': 3}

Evaluate the integral $\int_{0}^{14} \frac{27}{8 x^{2} + 8}\,\text{d}x.$

Field selection (radio)

- $\frac{27 \operatorname{arctan}{\left(14 \right)}}{4}$
- $\frac{27 \operatorname{arctan}{\left(7 \right)}}{8}$
- $\frac{27 \operatorname{arctan}{\left(7 \right)}}{4}$
- $\frac{27 \operatorname{arctan}{\left(14 \right)}}{8}$ (correct)
- $\frac{27 \operatorname{arctan}{\left(14 \right)}}{2}$

Note that we can rewrite this integral as

$$
\begin{aligned}\int_{0}^{14} \frac{27}{8 x^{2} + 8}\,\text{d}x &= \frac{27}{8}\int_{0}^{14} \frac{1}{1+(x)^{2}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+(u)^{2}}\,\text{d}u=\operatorname{arctan}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(x)^{2}.$

So, let's substitute $u=x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=1\quad\Longrightarrow\quad\text{d}x=1\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $14$ |
| --- | --- | --- |
| $u$ | $0$ | $14$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{14} \frac{27}{8 x^{2} + 8}\,\text{d}x &= \frac{27}{8}\int_{0}^{14} \frac{1}{1+(x)^{2}}\,\text{d}x \\ &= \frac{27}{8}\int_{0}^{14} \frac{1}{1+(u)^{2}}\cdot (1)\,\text{d}u \\ &= \frac{27}{8}\int_{0}^{14} \frac{1}{1+(u)^{2}}\,\text{d}u \\ &= \left[\frac{27}{8}\operatorname{arctan}(u)\right]_{0}^{14} \\ &= \frac{27}{8}\operatorname{arctan}(14)-(\frac{27}{8}\operatorname{arctan}(0)) \\ &= \frac{27 \operatorname{arctan}{\left(14 \right)}}{8}-(0) \\ &= \frac{27 \operatorname{arctan}{\left(14 \right)}}{8}\end{aligned}
$$

---

## q-114074 original

Evaluate the integral ${\int }_{0}^{1/8}\frac{2}{\sqrt{1-16{x}^{2}}}\,\text{d}x.$

Field selection (radio)

- $\frac{\pi }{3}$
- $\frac{\pi }{6}$
- $\frac{\pi }{12}$ (correct)
- $3\pi$
- $\frac{\pi }{2}$

Note that we can rewrite this integral as

$$
{\int }_{0}^{1/8}\frac{2}{\sqrt{1-16{x}^{2}}}\,\text{d}x=2{\int }_{0}^{1/8}\frac{1}{\sqrt{1-(4x)^{2}}}\,\text{d}x.
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-{u}^{2}}}\text{d}u=\operatorname{arcsin}⁡(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(4x)^{2}.$

So, let's substitute $u=4x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\text{d}x=\frac{1}{4}\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $\frac{1}{8}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{0}^{1/8}\frac{2}{\sqrt{1-16{x}^{2}}}\,\text{d}x & =2{\int }_{0}^{1/8}\frac{1}{\sqrt{1-(4x)^{2}}}\,\text{d}x \\  & =2{\int }_{0}^{1/2}\frac{1}{\sqrt{1-{u}^{2}}}\,\cdot (\frac{1}{4}\text{d}u) \\  & =\frac{1}{2}{\int }_{0}^{1/2}\frac{\text{d}u}{\sqrt{1-{u}^{2}}} \\  & =\frac{1}{2}\operatorname{arcsin}⁡u{|}_{0}^{1/2} \\  & =\frac{1}{2}(\operatorname{arcsin}⁡(\frac{1}{2})-\operatorname{arcsin}⁡(0)) \\  & =\frac{1}{2}(\frac{\pi }{6}-0) \\  & =\frac{\pi }{12}\end{aligned}\end{aligned}
$$

---

## q-114074 {'h': 2, 'k': 3}

Evaluate the integral $\int_{0}^{\frac{1}{4}} \frac{6}{\sqrt{4 - 16 x^{2}}}\,\text{d}x.$

Field selection (radio)

- $\pi$
- $\frac{\pi}{2}$
- $\frac{\pi}{4}$ (correct)
- $9 \pi$
- $\frac{3 \pi}{2}$

Note that we can rewrite this integral as

$$
\begin{aligned}\int_{0}^{\frac{1}{4}} \frac{6}{\sqrt{4 - 16 x^{2}}}\,\text{d}x &= 3\int_{0}^{\frac{1}{4}} \frac{1}{\sqrt{1-(2 x)^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(2 x)^{2}.$

So, let's substitute $u=2 x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=2\quad\Longrightarrow\quad\text{d}x=\frac{1}{2}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $\frac{1}{4}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{1}{4}} \frac{6}{\sqrt{4 - 16 x^{2}}}\,\text{d}x &= 3\int_{0}^{\frac{1}{4}} \frac{1}{\sqrt{1-(2 x)^{2}}}\,\text{d}x \\ &= 3\int_{0}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\cdot (\frac{1}{2})\,\text{d}u \\ &= \frac{3}{2}\int_{0}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u \\ &= \left[\frac{3}{2}\operatorname{arcsin}(u)\right]_{0}^{\frac{1}{2}} \\ &= \frac{3}{2}\operatorname{arcsin}(\frac{1}{2})-(\frac{3}{2}\operatorname{arcsin}(0)) \\ &= \frac{\pi}{4}-(0) \\ &= \frac{\pi}{4}\end{aligned}
$$

---

## q-114078 original

Evaluate the integral ${\int }_{0}^{2}\frac{1}{\sqrt{8-{x}^{2}}}\,\text{d}x.$

Field selection (radio)

- $\frac{\pi }{8}$
- $\frac{\pi }{2}$
- $2\pi$
- $\frac{\pi }{4}$ (correct)
- $8\pi$

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{0}^{2}\frac{1}{\sqrt{8-{x}^{2}}}\,\text{d}x & ={\int }_{0}^{2}\frac{1}{\sqrt{8\cdot (1-{x}^{2}/8)}}\,\text{d}x \\  & =\frac{1}{\sqrt{8}}{\int }_{0}^{2}\frac{1}{\sqrt{1-{x}^{2}/8}}\,\text{d}x \\  & =\frac{1}{\sqrt{8}}{\int }_{0}^{2}\frac{1}{\sqrt{1-(x/\sqrt{8})^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-{u}^{2}}}\text{d}u=\operatorname{arcsin}⁡(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(\frac{x}{\sqrt{8}})}^{2}.$

So, let's substitute $u=\frac{x}{\sqrt{8}}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{\sqrt{8}}\,⟹\,\text{d}x=\sqrt{8}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $2$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\sqrt{2}}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{2}\frac{1}{\sqrt{8-{x}^{2}}}\,\text{d}x & =\frac{1}{\sqrt{8}}{\int }_{0}^{2}\frac{1}{\sqrt{1-(x/\sqrt{8})^{2}}}\,\text{d}x \\  & =\frac{1}{\sqrt{8}}{\int }_{0}^{\sqrt{2}/2}\frac{1}{\sqrt{1-{u}^{2}}}\cdot (\sqrt{8}\,\text{d}u) \\  & ={\int }_{0}^{\sqrt{2}/2}\frac{\text{d}u}{\sqrt{1-{u}^{2}}} \\  & =\operatorname{arcsin}⁡u{|}_{0}^{\sqrt{2}/2} \\  & =\operatorname{arcsin}⁡(\frac{\sqrt{2}}{2})-\operatorname{arcsin}⁡(0) \\  & =\frac{\pi }{4}\end{aligned}
$$

---

## q-114078 {'h': 2, 'k': 3}

Evaluate the integral $\int_{0}^{4} \frac{3}{\sqrt{32 - x^{2}}}\,\text{d}x.$

Field selection (radio)

- $\frac{3 \pi}{8}$
- $\frac{3 \pi}{2}$
- $6 \pi$
- $\frac{3 \pi}{4}$ (correct)
- $24 \pi$

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{0}^{4} \frac{3}{\sqrt{32 - x^{2}}}\,\text{d}x &= \int_{0}^{4} \frac{3}{\sqrt{32(1-\frac{x^{2}}{32})}}\,\text{d}x \\ &= \frac{3 \sqrt{2}}{8}\int_{0}^{4} \frac{1}{\sqrt{1-\frac{x^{2}}{32}}}\,\text{d}x \\ &= \frac{3 \sqrt{2}}{8}\int_{0}^{4} \frac{1}{\sqrt{1-(\frac{\sqrt{2} x}{8})^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{\sqrt{2} x}{8})^{2}.$

So, let's substitute $u=\frac{\sqrt{2} x}{8}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{\sqrt{2}}{8}\quad\Longrightarrow\quad\text{d}x=4 \sqrt{2}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $4$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\sqrt{2}}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{4} \frac{3}{\sqrt{32 - x^{2}}}\,\text{d}x &= \frac{3 \sqrt{2}}{8}\int_{0}^{4} \frac{1}{\sqrt{1-(\frac{\sqrt{2} x}{8})^{2}}}\,\text{d}x \\ &= \frac{3 \sqrt{2}}{8}\int_{0}^{\frac{\sqrt{2}}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\cdot (4 \sqrt{2})\,\text{d}u \\ &= 3\int_{0}^{\frac{\sqrt{2}}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u \\ &= \left[3\operatorname{arcsin}(u)\right]_{0}^{\frac{\sqrt{2}}{2}} \\ &= 3\operatorname{arcsin}(\frac{\sqrt{2}}{2})-(3\operatorname{arcsin}(0)) \\ &= \frac{3 \pi}{4}-(0) \\ &= \frac{3 \pi}{4}\end{aligned}
$$

---

## q-114080 original

Evaluate the integral ${\int }_{0}^{\sqrt{3}}\frac{8}{\sqrt{4-{x}^{2}}}\,\text{d}x.$

Field selection (radio)

- $\frac{\pi }{3}$
- $\frac{\pi }{8}$
- $\frac{\pi }{24}$
- $\frac{3\pi }{8}$
- $\frac{8\pi }{3}$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{0}^{\sqrt{3}}\frac{8}{\sqrt{4-{x}^{2}}}\,\text{d}x & =8{\int }_{0}^{\sqrt{3}}\frac{1}{\sqrt{4\cdot (1-{x}^{2}/4)}}\,\text{d}x \\  & =\frac{8}{2}{\int }_{0}^{\sqrt{3}}\frac{1}{\sqrt{1-{x}^{2}/4}}\,\text{d}x \\  & =4{\int }_{0}^{\sqrt{3}}\frac{1}{\sqrt{1-(x/2)^{2}}}\,\text{d}x\end{aligned}
$$

 

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-{u}^{2}}}\text{d}u=\operatorname{arcsin}⁡(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(\frac{x}{2})}^{2}.$

So, let's substitute $u=\frac{x}{2}.$ Differentiating, we get 

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{2}\,⟹\,\text{d}x=2\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $\sqrt{3}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\sqrt{3}}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\sqrt{3}}\frac{8}{\sqrt{4-{x}^{2}}}\,\text{d}x & =4{\int }_{0}^{\sqrt{3}}\frac{1}{\sqrt{1-(x/2)^{2}}}\,\text{d}x \\  & =4{\int }_{0}^{\sqrt{3}/2}\frac{1}{\sqrt{1-{u}^{2}}}\cdot (2\,\text{d}u) \\  & =8{\int }_{0}^{\sqrt{3}/2}\frac{\text{d}u}{\sqrt{1-{u}^{2}}} \\  & =8\operatorname{arcsin}⁡u{|}_{0}^{\sqrt{3}/2} \\  & =8(\operatorname{arcsin}⁡(\frac{\sqrt{3}}{2})-\operatorname{arcsin}⁡(0)) \\  & =8(\frac{\pi }{3}-0) \\  & =\frac{8\pi }{3}\end{aligned}
$$

---

## q-114080 {'h': 2, 'k': 3}

Evaluate the integral $\int_{0}^{2 \sqrt{3}} \frac{24}{\sqrt{16 - x^{2}}}\,\text{d}x.$

Field selection (radio)

- $\pi$
- $\frac{3 \pi}{8}$
- $\frac{\pi}{8}$
- $\frac{9 \pi}{8}$
- $8 \pi$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{0}^{2 \sqrt{3}} \frac{24}{\sqrt{16 - x^{2}}}\,\text{d}x &= \int_{0}^{2 \sqrt{3}} \frac{24}{\sqrt{16(1-\frac{x^{2}}{16})}}\,\text{d}x \\ &= 6\int_{0}^{2 \sqrt{3}} \frac{1}{\sqrt{1-\frac{x^{2}}{16}}}\,\text{d}x \\ &= 6\int_{0}^{2 \sqrt{3}} \frac{1}{\sqrt{1-(\frac{x}{4})^{2}}}\,\text{d}x\end{aligned}
$$

 

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{x}{4})^{2}.$

So, let's substitute $u=\frac{x}{4}.$ Differentiating, we get 

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{4}\quad\Longrightarrow\quad\text{d}x=4\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $2 \sqrt{3}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\sqrt{3}}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{2 \sqrt{3}} \frac{24}{\sqrt{16 - x^{2}}}\,\text{d}x &= 6\int_{0}^{2 \sqrt{3}} \frac{1}{\sqrt{1-(\frac{x}{4})^{2}}}\,\text{d}x \\ &= 6\int_{0}^{\frac{\sqrt{3}}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\cdot (4)\,\text{d}u \\ &= 24\int_{0}^{\frac{\sqrt{3}}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u \\ &= \left[24\operatorname{arcsin}(u)\right]_{0}^{\frac{\sqrt{3}}{2}} \\ &= 24\operatorname{arcsin}(\frac{\sqrt{3}}{2})-(24\operatorname{arcsin}(0)) \\ &= 8 \pi-(0) \\ &= 8 \pi\end{aligned}
$$

---

## q-114084 original

Evaluate the integral ${\int }_{0}^{1}\frac{2}{3+{x}^{2}}\,\text{d}x.$

Field selection (radio)

- $\frac{\sqrt{3}\pi }{9}$ (correct)
- $\frac{\sqrt{3}\pi }{3}$
- $\frac{\pi }{3}$
- $\sqrt{3}\pi$
- $\frac{\pi }{9}$

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{0}^{1}\frac{2}{3+{x}^{2}}\,\text{d}x & ={\int }_{0}^{1}\frac{2}{3\cdot (1+{x}^{2}/3)}\,\text{d}x \\  & =\frac{2}{3}{\int }_{0}^{1}\frac{1}{1+{x}^{2}/3}\,\text{d}x \\  & =\frac{2}{3}{\int }_{0}^{1}\frac{1}{1+(x/\sqrt{3})^{2}}\,\text{d}x\end{aligned}
$$

 

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+{u}^{2}}\text{d}u=\operatorname{arctan}⁡u+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(\frac{x}{\sqrt{3}})}^{2}.$

So, let's substitute $u=\frac{x}{\sqrt{3}}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{\sqrt{3}}\,⟹\,\text{d}x=\sqrt{3}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\sqrt{3}}{3}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{1}\frac{2}{3+{x}^{2}}\,\text{d}x & =\frac{2}{3}{\int }_{0}^{1}\frac{1}{1+(x/\sqrt{3})^{2}}\,\text{d}x \\  & =\frac{2}{3}{\int }_{0}^{\sqrt{3}/3}\frac{1}{1+{u}^{2}}\cdot (\sqrt{3}\,\text{d}u) \\  & =\frac{2\sqrt{3}}{3}{\int }_{0}^{\sqrt{3}/3}\frac{\text{d}u}{1+{u}^{2}} \\  & =\frac{2\sqrt{3}}{3}\operatorname{arctan}⁡u{|}_{0}^{\sqrt{3}/3} \\  & =\frac{2\sqrt{3}}{3}(\operatorname{arctan}⁡(\frac{\sqrt{3}}{3})-\operatorname{arctan}⁡(0)) \\  & =\frac{2\sqrt{3}}{3}\cdot \frac{\pi }{6} \\  & =\frac{\sqrt{3}\pi }{9}\end{aligned}
$$

---

## q-114084 {'h': 2, 'k': 3}

Evaluate the integral $\int_{0}^{2} \frac{6}{x^{2} + 12}\,\text{d}x.$

Field selection (radio)

- $\frac{\sqrt{3} \pi}{6}$ (correct)
- $\frac{\sqrt{3} \pi}{2}$
- $\frac{\pi}{2}$
- $\frac{3 \sqrt{3} \pi}{2}$
- $\frac{\pi}{6}$

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{0}^{2} \frac{6}{x^{2} + 12}\,\text{d}x &= \int_{0}^{2} \frac{6}{12(1+\frac{x^{2}}{12})}\,\text{d}x \\ &= \frac{1}{2}\int_{0}^{2} \frac{1}{1+\frac{x^{2}}{12}}\,\text{d}x \\ &= \frac{1}{2}\int_{0}^{2} \frac{1}{1+(\frac{\sqrt{3} x}{6})^{2}}\,\text{d}x\end{aligned}
$$

 

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+(u)^{2}}\,\text{d}u=\operatorname{arctan}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{\sqrt{3} x}{6})^{2}.$

So, let's substitute $u=\frac{\sqrt{3} x}{6}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{\sqrt{3}}{6}\quad\Longrightarrow\quad\text{d}x=2 \sqrt{3}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $2$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\sqrt{3}}{3}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{2} \frac{6}{x^{2} + 12}\,\text{d}x &= \frac{1}{2}\int_{0}^{2} \frac{1}{1+(\frac{\sqrt{3} x}{6})^{2}}\,\text{d}x \\ &= \frac{1}{2}\int_{0}^{\frac{\sqrt{3}}{3}} \frac{1}{1+(u)^{2}}\cdot (2 \sqrt{3})\,\text{d}u \\ &= \sqrt{3}\int_{0}^{\frac{\sqrt{3}}{3}} \frac{1}{1+(u)^{2}}\,\text{d}u \\ &= \left[\sqrt{3}\operatorname{arctan}(u)\right]_{0}^{\frac{\sqrt{3}}{3}} \\ &= \sqrt{3}\operatorname{arctan}(\frac{\sqrt{3}}{3})-(\sqrt{3}\operatorname{arctan}(0)) \\ &= \frac{\sqrt{3} \pi}{6}-(0) \\ &= \frac{\sqrt{3} \pi}{6}\end{aligned}
$$

---

## q-19393 original

Evaluate the integral ${\int }_{0}^{2}\frac{5}{\sqrt{16-{x}^{2}}}\,\text{d}x.$

Field selection (radio)

- $\frac{5\pi }{4}$
- $\pi$
- $\frac{5\pi }{3}$
- $\frac{5\pi }{6}$ (correct)
- $\frac{\pi }{6}$

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{0}^{2}\frac{5}{\sqrt{16-{x}^{2}}}\,\text{d}x & =5{\int }_{0}^{2}\frac{1}{\sqrt{16\cdot (1-{x}^{2}/16)}}\,\text{d}x \\  & =\frac{5}{4}{\int }_{0}^{2}\frac{1}{\sqrt{1-{x}^{2}/16}}\,\text{d}x \\  & =\frac{5}{4}{\int }_{0}^{2}\frac{1}{\sqrt{1-(x/4)^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-{u}^{2}}}\text{d}u=\operatorname{arcsin}⁡(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(\frac{x}{4})}^{2}.$

So, let's substitute $u=\frac{x}{4}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{4}\,⟹\,\text{d}x=4\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $2$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{2}\frac{5}{\sqrt{16-{x}^{2}}}\,\text{d}x & =\frac{5}{4}{\int }_{0}^{2}\frac{1}{\sqrt{1-(x/4)^{2}}}\,\text{d}x \\  & =\frac{5}{4}{\int }_{0}^{1/2}\frac{1}{\sqrt{1-{u}^{2}}}\cdot (4\,\text{d}u) \\  & =5{\int }_{0}^{1/2}\frac{\text{d}u}{\sqrt{1-{u}^{2}}} \\  & =5\operatorname{arcsin}⁡u{|}_{0}^{1/2} \\  & =5\operatorname{arcsin}⁡(\frac{1}{2})-5\operatorname{arcsin}⁡(0) \\  & =\frac{5\pi }{6}\end{aligned}
$$

---

## q-19393 {'h': 2, 'k': 3}

Evaluate the integral $\int_{0}^{4} \frac{15}{\sqrt{64 - x^{2}}}\,\text{d}x.$

Field selection (radio)

- $\frac{15 \pi}{4}$
- $3 \pi$
- $5 \pi$
- $\frac{5 \pi}{2}$ (correct)
- $\frac{\pi}{2}$

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{0}^{4} \frac{15}{\sqrt{64 - x^{2}}}\,\text{d}x &= \int_{0}^{4} \frac{15}{\sqrt{64(1-\frac{x^{2}}{64})}}\,\text{d}x \\ &= \frac{15}{8}\int_{0}^{4} \frac{1}{\sqrt{1-\frac{x^{2}}{64}}}\,\text{d}x \\ &= \frac{15}{8}\int_{0}^{4} \frac{1}{\sqrt{1-(\frac{x}{8})^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{x}{8})^{2}.$

So, let's substitute $u=\frac{x}{8}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{8}\quad\Longrightarrow\quad\text{d}x=8\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $4$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{4} \frac{15}{\sqrt{64 - x^{2}}}\,\text{d}x &= \frac{15}{8}\int_{0}^{4} \frac{1}{\sqrt{1-(\frac{x}{8})^{2}}}\,\text{d}x \\ &= \frac{15}{8}\int_{0}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\cdot (8)\,\text{d}u \\ &= 15\int_{0}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u \\ &= \left[15\operatorname{arcsin}(u)\right]_{0}^{\frac{1}{2}} \\ &= 15\operatorname{arcsin}(\frac{1}{2})-(15\operatorname{arcsin}(0)) \\ &= \frac{5 \pi}{2}-(0) \\ &= \frac{5 \pi}{2}\end{aligned}
$$

---

## q-19395 original

Evaluate the integral ${\int }_{-0.25}^{0.25}\frac{3}{\sqrt{3-12{x}^{2}}}\,\text{d}x.$

Field selection (radio)

- $\sqrt{3}\pi$
- $\frac{\sqrt{3}\pi }{3}$
- $\frac{\pi }{3}$
- $\frac{\sqrt{3}\pi }{6}$ (correct)
- $\frac{\sqrt{2}\pi }{3}$

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{-0.25}^{0.25}\frac{3}{\sqrt{3-12{x}^{2}}}\,\text{d}x & =3{\int }_{-0.25}^{0.25}\frac{1}{\sqrt{3\cdot (1-4{x}^{2})}}\,\text{d}x \\  & =\frac{3}{\sqrt{3}}{\int }_{-0.25}^{0.25}\frac{1}{\sqrt{1-4{x}^{2}}}\,\text{d}x \\  & =\sqrt{3}{\int }_{-0.25}^{0.25}\frac{1}{\sqrt{1-(2x)^{2}}}\,\text{d}x\end{aligned}
$$

  

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-{u}^{2}}}\text{d}u=\operatorname{arcsin}⁡(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(2x)}^{2}.$   

So, let's substitute $u=2x.$ Differentiating, we get 

$$
\frac{\text{d}u}{\text{d}x}=2\,⟹\,\text{d}x=\frac{1}{2}\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $-0.25$ | $0.25$ |
| --- | --- | --- |
| $u$ | $-0.5$ | $0.5$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{-0.25}^{0.25}\frac{3}{\sqrt{3-12{x}^{2}}}\,\text{d}x & =\sqrt{3}{\int }_{-0.25}^{0.25}\frac{1}{\sqrt{1-(2x)^{2}}}\,\text{d}x \\  & =\sqrt{3}{\int }_{-0.5}^{0.5}\frac{1}{\sqrt{1-{u}^{2}}}\cdot (\frac{1}{2}\text{d}u) \\  & =\frac{\sqrt{3}}{2}{\int }_{-0.5}^{0.5}\frac{\text{d}u}{\sqrt{1-{u}^{2}}} \\  & =\frac{\sqrt{3}}{2}\operatorname{arcsin}⁡u{|}_{-0.5}^{0.5} \\  & =\frac{\sqrt{3}}{2}(\operatorname{arcsin}⁡(0.5)-\operatorname{arcsin}⁡(-0.5)) \\  & =\frac{\sqrt{3}}{2}(\frac{\pi }{6}+\frac{\pi }{6}) \\  & =\frac{\sqrt{3}}{2}\cdot \frac{\pi }{3} \\  & =\frac{\sqrt{3}\pi }{6}\end{aligned}
$$

---

## q-19395 {'h': 2, 'k': 3}

Evaluate the integral $\int_{- \frac{1}{2}}^{\frac{1}{2}} \frac{9}{\sqrt{12 - 12 x^{2}}}\,\text{d}x.$

Field selection (radio)

- $3 \sqrt{3} \pi$
- $\sqrt{3} \pi$
- $\pi$
- $\frac{\sqrt{3} \pi}{2}$ (correct)
- $\sqrt{2} \pi$

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{- \frac{1}{2}}^{\frac{1}{2}} \frac{9}{\sqrt{12 - 12 x^{2}}}\,\text{d}x &= \int_{- \frac{1}{2}}^{\frac{1}{2}} \frac{9}{\sqrt{12(1-x^{2})}}\,\text{d}x \\ &= \frac{3 \sqrt{3}}{2}\int_{- \frac{1}{2}}^{\frac{1}{2}} \frac{1}{\sqrt{1-x^{2}}}\,\text{d}x \\ &= \frac{3 \sqrt{3}}{2}\int_{- \frac{1}{2}}^{\frac{1}{2}} \frac{1}{\sqrt{1-(x)^{2}}}\,\text{d}x\end{aligned}
$$

  

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(x)^{2}.$   

So, let's substitute $u=x.$ Differentiating, we get 

$$
\frac{\text{d}u}{\text{d}x}=1\quad\Longrightarrow\quad\text{d}x=1\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $- \frac{1}{2}$ | $\frac{1}{2}$ |
| --- | --- | --- |
| $u$ | $- \frac{1}{2}$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{- \frac{1}{2}}^{\frac{1}{2}} \frac{9}{\sqrt{12 - 12 x^{2}}}\,\text{d}x &= \frac{3 \sqrt{3}}{2}\int_{- \frac{1}{2}}^{\frac{1}{2}} \frac{1}{\sqrt{1-(x)^{2}}}\,\text{d}x \\ &= \frac{3 \sqrt{3}}{2}\int_{- \frac{1}{2}}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\cdot (1)\,\text{d}u \\ &= \frac{3 \sqrt{3}}{2}\int_{- \frac{1}{2}}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u \\ &= \left[\frac{3 \sqrt{3}}{2}\operatorname{arcsin}(u)\right]_{- \frac{1}{2}}^{\frac{1}{2}} \\ &= \frac{3 \sqrt{3}}{2}\operatorname{arcsin}(\frac{1}{2})-(\frac{3 \sqrt{3}}{2}\operatorname{arcsin}(- \frac{1}{2})) \\ &= \frac{\sqrt{3} \pi}{4}-(- \frac{\sqrt{3} \pi}{4}) \\ &= \frac{\sqrt{3} \pi}{2}\end{aligned}
$$

---

## q-19396 original

Evaluate the integral ${\int }_{0}^{1/5}\frac{20}{3+75{x}^{2}}\,\text{d}x.$

Field selection (radio)

- $\frac{\pi }{4}$
- $\frac{4\pi }{3}$
- $\frac{2\pi }{3}$
- $\frac{\pi }{3}$ (correct)
- $\frac{\pi }{2}$

Note that we can write this integral as

$$
{\int }_{0}^{1/5}\frac{20}{3+75{x}^{2}}\,\text{d}x=\frac{20}{3}{\int }_{0}^{1/5}\frac{1}{1+25{x}^{2}}\,\text{d}x.
$$

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+{u}^{2}}\text{d}u=\operatorname{arctan}⁡u+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $25{x}^{2}=(5x)^{2}.$

So, let's substitute $u=5x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\text{d}x=\frac{1}{5}\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $\frac{1}{5}$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{1/5}\frac{20}{3+75{x}^{2}}\,\text{d}x & =\frac{20}{3}{\int }_{0}^{1/5}\frac{1}{1+(5x)^{2}}\,\text{d}x \\  & =\frac{20}{3}{\int }_{0}^{1}\frac{1}{1+{u}^{2}}\,\cdot (\frac{1}{5}\text{d}u) \\  & =\frac{4}{3}{\int }_{0}^{1}\frac{\text{d}u}{1+{u}^{2}} \\  & =\frac{4}{3}\operatorname{arctan}⁡u{|}_{0}^{1} \\  & =\frac{4}{3}\operatorname{arctan}⁡(1)-\frac{4}{3}\operatorname{arctan}⁡(0) \\  & =\frac{4}{3}\cdot \frac{\pi }{4} \\  & =\frac{\pi }{3}\end{aligned}
$$

---

## q-19396 {'h': 2, 'k': 3}

Evaluate the integral $\int_{0}^{\frac{2}{5}} \frac{60}{75 x^{2} + 12}\,\text{d}x.$

Field selection (radio)

- $\frac{3 \pi}{8}$
- $2 \pi$
- $\pi$
- $\frac{\pi}{2}$ (correct)
- $\frac{3 \pi}{4}$

Note that we can write this integral as

$$
\begin{aligned}\int_{0}^{\frac{2}{5}} \frac{60}{75 x^{2} + 12}\,\text{d}x &= 5\int_{0}^{\frac{2}{5}} \frac{1}{1+(\frac{5 x}{2})^{2}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+(u)^{2}}\,\text{d}u=\operatorname{arctan}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{5 x}{2})^{2}.$

So, let's substitute $u=\frac{5 x}{2}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{5}{2}\quad\Longrightarrow\quad\text{d}x=\frac{2}{5}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $\frac{2}{5}$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{2}{5}} \frac{60}{75 x^{2} + 12}\,\text{d}x &= 5\int_{0}^{\frac{2}{5}} \frac{1}{1+(\frac{5 x}{2})^{2}}\,\text{d}x \\ &= 5\int_{0}^{1} \frac{1}{1+(u)^{2}}\cdot (\frac{2}{5})\,\text{d}u \\ &= 2\int_{0}^{1} \frac{1}{1+(u)^{2}}\,\text{d}u \\ &= \left[2\operatorname{arctan}(u)\right]_{0}^{1} \\ &= 2\operatorname{arctan}(1)-(2\operatorname{arctan}(0)) \\ &= \frac{\pi}{2}-(0) \\ &= \frac{\pi}{2}\end{aligned}
$$

---

## q-346451 original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{1/3}\frac{2}{1+9{x}^{2}}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{\pi }{6}$ (correct)

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+{u}^{2}}\,\text{d}u=\operatorname{arctan}⁡u+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $9{x}^{2}=(3x)^{2}.$

So, let's substitute $u=3x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $\frac{1}{3}$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{1/3}\frac{2}{1+9{x}^{2}}\,\text{d}x & =2{\int }_{0}^{1/3}\frac{1}{1+(3x)^{2}}\,\text{d}x \\  & =2{\int }_{0}^{1}\frac{1}{1+{u}^{2}}\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{2}{3}{\int }_{0}^{1}\frac{1}{1+{u}^{2}}\,\text{d}u \\  & =\frac{2}{3}\operatorname{arctan}⁡u\,{|}_{0}^{1} \\  & =\frac{2}{3}(\operatorname{arctan}⁡(1)-\operatorname{arctan}⁡(0)) \\  & =\frac{2}{3}(\frac{\pi }{4}-0) \\  & =\frac{\pi }{6}\end{aligned}
$$

---

## q-346451 {'h': 2, 'k': 3}

Evaluate the following integral. Do not round the answer.

$\int_{0}^{\frac{2}{3}} \frac{6}{9 x^{2} + 4}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{\pi}{4}$ (correct)

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+(u)^{2}}\,\text{d}u=\operatorname{arctan}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{3 x}{2})^{2}.$

So, let's substitute $u=\frac{3 x}{2}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{3}{2}\quad\Longrightarrow\quad\text{d}x=\frac{2}{3}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $\frac{2}{3}$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{2}{3}} \frac{6}{9 x^{2} + 4}\,\text{d}x &= \frac{3}{2}\int_{0}^{\frac{2}{3}} \frac{1}{1+(\frac{3 x}{2})^{2}}\,\text{d}x \\ &= \frac{3}{2}\int_{0}^{1} \frac{1}{1+(u)^{2}}\cdot (\frac{2}{3})\,\text{d}u \\ &= 1\int_{0}^{1} \frac{1}{1+(u)^{2}}\,\text{d}u \\ &= \left[1\operatorname{arctan}(u)\right]_{0}^{1} \\ &= 1\operatorname{arctan}(1)-(1\operatorname{arctan}(0)) \\ &= \frac{\pi}{4}-(0) \\ &= \frac{\pi}{4}\end{aligned}
$$

---

## q-346458 original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{5}\frac{6}{\sqrt{100-{x}^{2}}}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\pi$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{0}^{5}\frac{6}{\sqrt{100-{x}^{2}}}\,\text{d}x & =6{\int }_{0}^{5}\frac{1}{\sqrt{100\cdot (1-{x}^{2}/100)}}\,\text{d}x \\  & =\frac{6}{10}{\int }_{0}^{5}\frac{1}{\sqrt{1-{x}^{2}/100}}\,\text{d}x \\  & =\frac{3}{5}{\int }_{0}^{5}\frac{1}{\sqrt{1-(x/10)^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-{u}^{2}}}\text{d}u=\operatorname{arcsin}⁡u+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(\frac{x}{10})}^{2}.$

So, let's substitute $u=\frac{x}{10}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{10}\,⟹\,\text{d}x=10\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $5$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{5}\frac{6}{\sqrt{100-{x}^{2}}}\,\text{d}x & =\frac{3}{5}{\int }_{0}^{5}\frac{1}{\sqrt{1-(x/10)^{2}}}\,\text{d}x \\  & =\frac{3}{5}{\int }_{0}^{1/2}\frac{1}{\sqrt{1-{u}^{2}}}\cdot 10\,\text{d}u \\  & =6{\int }_{0}^{1/2}\frac{\text{d}u}{\sqrt{1-{u}^{2}}} \\  & =6\operatorname{arcsin}⁡u\,{|}_{0}^{1/2} \\  & =6\operatorname{arcsin}⁡(\frac{1}{2})-6\operatorname{arcsin}⁡(0) \\  & =6\cdot \frac{\pi }{6} \\  & =\pi \end{aligned}
$$

---

## q-346458 {'h': 2, 'k': 3}

Evaluate the following integral. Do not round the answer.

$\int_{0}^{10} \frac{18}{\sqrt{400 - x^{2}}}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $3 \pi$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{0}^{10} \frac{18}{\sqrt{400 - x^{2}}}\,\text{d}x &= \int_{0}^{10} \frac{18}{\sqrt{400(1-\frac{x^{2}}{400})}}\,\text{d}x \\ &= \frac{9}{10}\int_{0}^{10} \frac{1}{\sqrt{1-\frac{x^{2}}{400}}}\,\text{d}x \\ &= \frac{9}{10}\int_{0}^{10} \frac{1}{\sqrt{1-(\frac{x}{20})^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{x}{20})^{2}.$

So, let's substitute $u=\frac{x}{20}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{20}\quad\Longrightarrow\quad\text{d}x=20\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $10$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{10} \frac{18}{\sqrt{400 - x^{2}}}\,\text{d}x &= \frac{9}{10}\int_{0}^{10} \frac{1}{\sqrt{1-(\frac{x}{20})^{2}}}\,\text{d}x \\ &= \frac{9}{10}\int_{0}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\cdot (20)\,\text{d}u \\ &= 18\int_{0}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u \\ &= \left[18\operatorname{arcsin}(u)\right]_{0}^{\frac{1}{2}} \\ &= 18\operatorname{arcsin}(\frac{1}{2})-(18\operatorname{arcsin}(0)) \\ &= 3 \pi-(0) \\ &= 3 \pi\end{aligned}
$$

---

## q-351291 original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{1/8}\frac{10}{\sqrt{5-80{x}^{2}}}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{\pi \sqrt{5}}{12}$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{0}^{1/8}\frac{10}{\sqrt{5-80{x}^{2}}}\,\text{d}x & =10{\int }_{0}^{1/8}\frac{1}{\sqrt{5(1-16{x}^{2})}}\,\text{d}x \\  & =\frac{10}{\sqrt{5}}{\int }_{0}^{1/8}\frac{1}{\sqrt{1-16{x}^{2}}}\,\text{d}x \\  & =2\sqrt{5}{\int }_{0}^{1/8}\frac{1}{\sqrt{1-(4x)^{2}}}\,\text{d}x\end{aligned}
$$

 

This integral resembles the basic integral for inverse sine, 

$$
\int \frac{1}{\sqrt{1-{u}^{2}}}\text{d}u=\operatorname{arcsin}⁡u+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(4x)}^{2}.$

So, let's substitute $u=4x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\text{d}x=\frac{1}{4}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $\frac{1}{8}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{1/8}\frac{10}{\sqrt{5-80{x}^{2}}}\,\text{d}x & =2\sqrt{5}{\int }_{0}^{1/8}\frac{1}{\sqrt{1-(4x)^{2}}}\,\text{d}x \\  & =2\sqrt{5}{\int }_{0}^{1/2}\frac{1}{\sqrt{1-{u}^{2}}}\cdot \frac{1}{4}\,\text{d}u \\  & =\frac{\sqrt{5}}{2}{\int }_{0}^{1/2}\frac{1}{\sqrt{1-{u}^{2}}}\,\text{d}u \\  & =\frac{\sqrt{5}}{2}\operatorname{arcsin}⁡u\,{|}_{0}^{1/2} \\  & =\frac{\sqrt{5}}{2}(\operatorname{arcsin}⁡(\frac{1}{2})-\operatorname{arcsin}⁡(0)) \\  & =\frac{\sqrt{5}}{2}(\frac{\pi }{6}-0) \\  & =\frac{\pi \sqrt{5}}{12}\end{aligned}
$$

---

## q-351291 {'h': 2, 'k': 3}

Evaluate the following integral. Do not round the answer.

$\int_{0}^{\frac{1}{4}} \frac{30}{\sqrt{20 - 80 x^{2}}}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{\sqrt{5} \pi}{4}$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{0}^{\frac{1}{4}} \frac{30}{\sqrt{20 - 80 x^{2}}}\,\text{d}x &= \int_{0}^{\frac{1}{4}} \frac{30}{\sqrt{20(1-4 x^{2})}}\,\text{d}x \\ &= 3 \sqrt{5}\int_{0}^{\frac{1}{4}} \frac{1}{\sqrt{1-4 x^{2}}}\,\text{d}x \\ &= 3 \sqrt{5}\int_{0}^{\frac{1}{4}} \frac{1}{\sqrt{1-(2 x)^{2}}}\,\text{d}x\end{aligned}
$$

 

This integral resembles the basic integral for inverse sine, 

$$
\int \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(2 x)^{2}.$

So, let's substitute $u=2 x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=2\quad\Longrightarrow\quad\text{d}x=\frac{1}{2}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $\frac{1}{4}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{1}{4}} \frac{30}{\sqrt{20 - 80 x^{2}}}\,\text{d}x &= 3 \sqrt{5}\int_{0}^{\frac{1}{4}} \frac{1}{\sqrt{1-(2 x)^{2}}}\,\text{d}x \\ &= 3 \sqrt{5}\int_{0}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\cdot (\frac{1}{2})\,\text{d}u \\ &= \frac{3 \sqrt{5}}{2}\int_{0}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u \\ &= \left[\frac{3 \sqrt{5}}{2}\operatorname{arcsin}(u)\right]_{0}^{\frac{1}{2}} \\ &= \frac{3 \sqrt{5}}{2}\operatorname{arcsin}(\frac{1}{2})-(\frac{3 \sqrt{5}}{2}\operatorname{arcsin}(0)) \\ &= \frac{\sqrt{5} \pi}{4}-(0) \\ &= \frac{\sqrt{5} \pi}{4}\end{aligned}
$$

---

## q-351827 original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{3\sqrt{3}}\frac{15}{\sqrt{36-{x}^{2}}}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $5\pi$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{0}^{3\sqrt{3}}\frac{15}{\sqrt{36-{x}^{2}}}\,\text{d}x & =15{\int }_{0}^{3\sqrt{3}}\frac{1}{\sqrt{36\cdot (1-{x}^{2}/36)}}\,\text{d}x \\  & =\frac{15}{6}{\int }_{0}^{3\sqrt{3}}\frac{1}{\sqrt{1-{x}^{2}/36}}\,\text{d}x \\  & =\frac{5}{2}{\int }_{0}^{3\sqrt{3}}\frac{1}{\sqrt{1-(x/6)^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-{u}^{2}}}\text{d}u=\operatorname{arcsin}⁡u+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(\frac{x}{6})}^{2}.$

So, let's substitute $u=\frac{x}{6}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{6}\,⟹\,\text{d}x=6\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $3\sqrt{3}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\sqrt{3}}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{3\sqrt{3}}\frac{15}{\sqrt{36-{x}^{2}}}\,\text{d}x & =\frac{5}{2}{\int }_{0}^{3\sqrt{3}}\frac{1}{\sqrt{1-(x/6)^{2}}}\,\text{d}x \\  & =\frac{5}{2}{\int }_{0}^{\sqrt{3}/2}\frac{1}{\sqrt{1-{u}^{2}}}\cdot 6\,\text{d}u \\  & =15{\int }_{0}^{\sqrt{3}/2}\frac{\text{d}u}{\sqrt{1-{u}^{2}}} \\  & =15\operatorname{arcsin}⁡u\,{|}_{0}^{\sqrt{3}/2} \\  & =15\operatorname{arcsin}⁡(\frac{\sqrt{3}}{2})-15\operatorname{arcsin}⁡(0) \\  & =15\cdot \frac{\pi }{3} \\  & =5\pi \end{aligned}
$$

---

## q-351827 {'h': 2, 'k': 3}

Evaluate the following integral. Do not round the answer.

$\int_{0}^{6 \sqrt{3}} \frac{45}{\sqrt{144 - x^{2}}}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $15 \pi$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{0}^{6 \sqrt{3}} \frac{45}{\sqrt{144 - x^{2}}}\,\text{d}x &= \int_{0}^{6 \sqrt{3}} \frac{45}{\sqrt{144(1-\frac{x^{2}}{144})}}\,\text{d}x \\ &= \frac{15}{4}\int_{0}^{6 \sqrt{3}} \frac{1}{\sqrt{1-\frac{x^{2}}{144}}}\,\text{d}x \\ &= \frac{15}{4}\int_{0}^{6 \sqrt{3}} \frac{1}{\sqrt{1-(\frac{x}{12})^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{x}{12})^{2}.$

So, let's substitute $u=\frac{x}{12}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{12}\quad\Longrightarrow\quad\text{d}x=12\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $6 \sqrt{3}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\sqrt{3}}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{6 \sqrt{3}} \frac{45}{\sqrt{144 - x^{2}}}\,\text{d}x &= \frac{15}{4}\int_{0}^{6 \sqrt{3}} \frac{1}{\sqrt{1-(\frac{x}{12})^{2}}}\,\text{d}x \\ &= \frac{15}{4}\int_{0}^{\frac{\sqrt{3}}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\cdot (12)\,\text{d}u \\ &= 45\int_{0}^{\frac{\sqrt{3}}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u \\ &= \left[45\operatorname{arcsin}(u)\right]_{0}^{\frac{\sqrt{3}}{2}} \\ &= 45\operatorname{arcsin}(\frac{\sqrt{3}}{2})-(45\operatorname{arcsin}(0)) \\ &= 15 \pi-(0) \\ &= 15 \pi\end{aligned}
$$

---

## q-351834 original

Evaluate the following integral. Do not round the answer.

${\int }_{-0.2}^{0.2}\frac{3}{\sqrt{3-75{x}^{2}}}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{\sqrt{3}\pi }{5}$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{-0.2}^{0.2}\frac{3}{\sqrt{3-75{x}^{2}}}\,\text{d}x & =3{\int }_{-0.2}^{0.2}\frac{1}{\sqrt{3\cdot (1-25{x}^{2})}}\,\text{d}x \\  & =\frac{3}{\sqrt{3}}{\int }_{-0.2}^{0.2}\frac{1}{\sqrt{1-25{x}^{2}}}\,\text{d}x \\  & =\sqrt{3}{\int }_{-0.2}^{0.2}\frac{1}{\sqrt{1-(5x)^{2}}}\,\text{d}x\end{aligned}
$$

  

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-{u}^{2}}}\text{d}u=\operatorname{arcsin}⁡(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(5x)}^{2}.$   

So, let's substitute $u=5x.$ Differentiating, we get 

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\text{d}x=\frac{1}{5}\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $-0.2$ | $0.2$ |
| --- | --- | --- |
| $u$ | $-1$ | $1$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{-0.2}^{0.2}\frac{3}{\sqrt{3-75{x}^{2}}}\,\text{d}x & =\sqrt{3}{\int }_{-0.2}^{0.2}\frac{1}{\sqrt{1-(5x)^{2}}}\,\text{d}x \\  & =\sqrt{3}{\int }_{-1}^{1}\frac{1}{\sqrt{1-{u}^{2}}}\cdot (\frac{1}{5}\text{d}u) \\  & =\frac{\sqrt{3}}{5}{\int }_{-1}^{1}\frac{\text{d}u}{\sqrt{1-{u}^{2}}} \\  & =\frac{\sqrt{3}}{5}\,\operatorname{arcsin}⁡u{|}_{-1}^{1} \\  & =\frac{\sqrt{3}}{5}(\operatorname{arcsin}⁡(1)-\operatorname{arcsin}⁡(-1)) \\  & =\frac{\sqrt{3}}{5}(\frac{\pi }{2}+\frac{\pi }{2}) \\  & =\frac{\sqrt{3}\,\pi }{5}\end{aligned}
$$

---

## q-351834 {'h': 2, 'k': 3}

Evaluate the following integral. Do not round the answer.

$\int_{- \frac{2}{5}}^{\frac{2}{5}} \frac{9}{\sqrt{12 - 75 x^{2}}}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{3 \sqrt{3} \pi}{5}$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{- \frac{2}{5}}^{\frac{2}{5}} \frac{9}{\sqrt{12 - 75 x^{2}}}\,\text{d}x &= \int_{- \frac{2}{5}}^{\frac{2}{5}} \frac{9}{\sqrt{12(1-\frac{25 x^{2}}{4})}}\,\text{d}x \\ &= \frac{3 \sqrt{3}}{2}\int_{- \frac{2}{5}}^{\frac{2}{5}} \frac{1}{\sqrt{1-\frac{25 x^{2}}{4}}}\,\text{d}x \\ &= \frac{3 \sqrt{3}}{2}\int_{- \frac{2}{5}}^{\frac{2}{5}} \frac{1}{\sqrt{1-(\frac{5 x}{2})^{2}}}\,\text{d}x\end{aligned}
$$

  

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{5 x}{2})^{2}.$   

So, let's substitute $u=\frac{5 x}{2}.$ Differentiating, we get 

$$
\frac{\text{d}u}{\text{d}x}=\frac{5}{2}\quad\Longrightarrow\quad\text{d}x=\frac{2}{5}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $- \frac{2}{5}$ | $\frac{2}{5}$ |
| --- | --- | --- |
| $u$ | $-1$ | $1$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{- \frac{2}{5}}^{\frac{2}{5}} \frac{9}{\sqrt{12 - 75 x^{2}}}\,\text{d}x &= \frac{3 \sqrt{3}}{2}\int_{- \frac{2}{5}}^{\frac{2}{5}} \frac{1}{\sqrt{1-(\frac{5 x}{2})^{2}}}\,\text{d}x \\ &= \frac{3 \sqrt{3}}{2}\int_{-1}^{1} \frac{1}{\sqrt{1-(u)^{2}}}\cdot (\frac{2}{5})\,\text{d}u \\ &= \frac{3 \sqrt{3}}{5}\int_{-1}^{1} \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u \\ &= \left[\frac{3 \sqrt{3}}{5}\operatorname{arcsin}(u)\right]_{-1}^{1} \\ &= \frac{3 \sqrt{3}}{5}\operatorname{arcsin}(1)-(\frac{3 \sqrt{3}}{5}\operatorname{arcsin}(-1)) \\ &= \frac{3 \sqrt{3} \pi}{10}-(- \frac{3 \sqrt{3} \pi}{10}) \\ &= \frac{3 \sqrt{3} \pi}{5}\end{aligned}
$$

---

## q-351835 original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{1/12}\frac{2}{\sqrt{1-36{x}^{2}}}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{\pi }{18}$ (correct)

Note that we can rewrite this integral as

$$
{\int }_{0}^{1/12}\frac{2}{\sqrt{1-36{x}^{2}}}\,\text{d}x=2{\int }_{0}^{1/12}\frac{1}{\sqrt{1-(6x)^{2}}}\,\text{d}x.
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-{u}^{2}}}\text{d}u=\operatorname{arcsin}⁡(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(6x)^{2}.$

So, let's substitute $u=6x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=6\,⟹\,\text{d}x=\frac{1}{6}\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $\frac{1}{12}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{0}^{1/12}\frac{2}{\sqrt{1-36{x}^{2}}}\,\text{d}x & =2{\int }_{0}^{1/12}\frac{1}{\sqrt{1-(6x)^{2}}}\,\text{d}x \\  & =2{\int }_{0}^{1/2}\frac{1}{\sqrt{1-{u}^{2}}}\,\cdot (\frac{1}{6}\text{d}u) \\  & =\frac{1}{3}{\int }_{0}^{1/2}\frac{\text{d}u}{\sqrt{1-{u}^{2}}} \\  & =\frac{1}{3}\operatorname{arcsin}⁡u{|}_{0}^{1/2} \\  & =\frac{1}{3}(\operatorname{arcsin}⁡(\frac{1}{2})-\operatorname{arcsin}⁡(0)) \\  & =\frac{1}{3}(\frac{\pi }{6}-0) \\  & =\frac{\pi }{18}\end{aligned}\end{aligned}
$$

---

## q-351835 {'h': 2, 'k': 3}

Evaluate the following integral. Do not round the answer.

$\int_{0}^{\frac{1}{6}} \frac{6}{\sqrt{4 - 36 x^{2}}}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{\pi}{6}$ (correct)

Note that we can rewrite this integral as

$$
\begin{aligned}\int_{0}^{\frac{1}{6}} \frac{6}{\sqrt{4 - 36 x^{2}}}\,\text{d}x &= 3\int_{0}^{\frac{1}{6}} \frac{1}{\sqrt{1-(3 x)^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(3 x)^{2}.$

So, let's substitute $u=3 x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=3\quad\Longrightarrow\quad\text{d}x=\frac{1}{3}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $\frac{1}{6}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{1}{6}} \frac{6}{\sqrt{4 - 36 x^{2}}}\,\text{d}x &= 3\int_{0}^{\frac{1}{6}} \frac{1}{\sqrt{1-(3 x)^{2}}}\,\text{d}x \\ &= 3\int_{0}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\cdot (\frac{1}{3})\,\text{d}u \\ &= 1\int_{0}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u \\ &= \left[1\operatorname{arcsin}(u)\right]_{0}^{\frac{1}{2}} \\ &= 1\operatorname{arcsin}(\frac{1}{2})-(1\operatorname{arcsin}(0)) \\ &= \frac{\pi}{6}-(0) \\ &= \frac{\pi}{6}\end{aligned}
$$

---

## q-351839 original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{4}\frac{12}{3+27{x}^{2}}\,\text{d}x=$
{{field-1}}
$\operatorname{arctan}⁡($
{{field-2}}$)$

Field field-1 (blank)

- $\frac{4}{3}$ (correct)
Field field-2 (blank)

- $12$ (correct)

Note that we can rewrite this integral as

$$
{\int }_{0}^{4}\frac{12}{3+27{x}^{2}}\,\text{d}x=4{\int }_{0}^{4}\frac{1}{1+9{x}^{2}}\,\text{d}x.
$$

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+{u}^{2}}\text{d}u=\operatorname{arctan}⁡u+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $9{x}^{2}=(3x)^{2}.$

So, let's substitute $u=3x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $4$ |
| --- | --- | --- |
| $u$ | $0$ | $12$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{4}\frac{12}{3+27{x}^{2}}\,\text{d}x & =4{\int }_{0}^{4}\frac{1}{1+(3x)^{2}}\,\text{d}x \\  & =4{\int }_{0}^{12}\frac{1}{1+{u}^{2}}\,\cdot (\frac{1}{3}\text{d}u) \\  & =\frac{4}{3}{\int }_{0}^{12}\frac{\text{d}u}{1+{u}^{2}} \\  & =\frac{4}{3}\operatorname{arctan}⁡u{|}_{0}^{12} \\  & =\frac{4}{3}\operatorname{arctan}⁡(12)-\frac{4}{3}\operatorname{arctan}⁡(0) \\  & =\frac{4}{3}\,\operatorname{arctan}\,(12)\end{aligned}
$$

---

## q-351839 {'h': 2, 'k': 3}

Evaluate the following integral. Do not round the answer.

$\int_{0}^{8} \frac{36}{27 x^{2} + 12}\,\text{d}x=$
{{field-1}}
$\operatorname{arctan}⁡($
{{field-2}}$)$

Field field-1 (blank)

- $2$ (correct)
Field field-2 (blank)

- $12$ (correct)

Note that we can rewrite this integral as

$$
\begin{aligned}\int_{0}^{8} \frac{36}{27 x^{2} + 12}\,\text{d}x &= 3\int_{0}^{8} \frac{1}{1+(\frac{3 x}{2})^{2}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+(u)^{2}}\,\text{d}u=\operatorname{arctan}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{3 x}{2})^{2}.$

So, let's substitute $u=\frac{3 x}{2}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{3}{2}\quad\Longrightarrow\quad\text{d}x=\frac{2}{3}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $8$ |
| --- | --- | --- |
| $u$ | $0$ | $12$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{8} \frac{36}{27 x^{2} + 12}\,\text{d}x &= 3\int_{0}^{8} \frac{1}{1+(\frac{3 x}{2})^{2}}\,\text{d}x \\ &= 3\int_{0}^{12} \frac{1}{1+(u)^{2}}\cdot (\frac{2}{3})\,\text{d}u \\ &= 2\int_{0}^{12} \frac{1}{1+(u)^{2}}\,\text{d}u \\ &= \left[2\operatorname{arctan}(u)\right]_{0}^{12} \\ &= 2\operatorname{arctan}(12)-(2\operatorname{arctan}(0)) \\ &= 2 \operatorname{arctan}{\left(12 \right)}-(0) \\ &= 2 \operatorname{arctan}{\left(12 \right)}\end{aligned}
$$

---

## q-351855 original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{2}\frac{1}{\sqrt{12-{x}^{2}}}\,\text{d}x=\operatorname{arcsin}⁡($
{{field-1}}$)$

Field field-1 (blank)

- $\frac{1}{\sqrt{3}}$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{0}^{2}\frac{1}{\sqrt{12-{x}^{2}}}\,\text{d}x & ={\int }_{0}^{2}\frac{1}{\sqrt{12\cdot (1-{x}^{2}/12)}}\,\text{d}x \\  & =\frac{1}{\sqrt{12}}{\int }_{0}^{2}\frac{1}{\sqrt{1-{x}^{2}/12}}\,\text{d}x \\  & =\frac{1}{\sqrt{12}}{\int }_{0}^{2}\frac{1}{\sqrt{1-(x/\sqrt{12})^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-{u}^{2}}}\text{d}u=\operatorname{arcsin}⁡(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(\frac{x}{\sqrt{12}})}^{2}.$

So, let's substitute $u=\frac{x}{\sqrt{12}}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{\sqrt{12}}\,⟹\,\text{d}x=\sqrt{12}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $2$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{1}{\sqrt{3}}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{2}\frac{1}{\sqrt{12-{x}^{2}}}\,\text{d}x & =\frac{1}{\sqrt{12}}{\int }_{0}^{2}\frac{1}{\sqrt{1-(x/\sqrt{12})^{2}}}\,\text{d}x \\  & =\frac{1}{\sqrt{12}}{\int }_{0}^{1/\sqrt{3}}\frac{1}{\sqrt{1-{u}^{2}}}\cdot (\sqrt{12}\,\text{d}u) \\  & ={\int }_{0}^{1/\sqrt{3}}\frac{\text{d}u}{\sqrt{1-{u}^{2}}} \\  & =\operatorname{arcsin}⁡u{|}_{0}^{1/\sqrt{3}} \\  & =\operatorname{arcsin}⁡(\frac{1}{\sqrt{3}})-\operatorname{arcsin}⁡(0) \\  & =\operatorname{arcsin}⁡(\frac{1}{\sqrt{3}})\end{aligned}
$$

---

## q-351855 {'h': 2, 'k': 1}

Evaluate the following integral. Do not round the answer.

$\int_{0}^{4} \frac{1}{\sqrt{48 - x^{2}}}\,\text{d}x=\operatorname{arcsin}⁡($
{{field-1}}$)$

Field field-1 (blank)

- $\frac{\sqrt{3}}{3}$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{0}^{4} \frac{1}{\sqrt{48 - x^{2}}}\,\text{d}x &= \int_{0}^{4} \frac{1}{\sqrt{48(1-\frac{x^{2}}{48})}}\,\text{d}x \\ &= \frac{\sqrt{3}}{12}\int_{0}^{4} \frac{1}{\sqrt{1-\frac{x^{2}}{48}}}\,\text{d}x \\ &= \frac{\sqrt{3}}{12}\int_{0}^{4} \frac{1}{\sqrt{1-(\frac{\sqrt{3} x}{12})^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{\sqrt{3} x}{12})^{2}.$

So, let's substitute $u=\frac{\sqrt{3} x}{12}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{\sqrt{3}}{12}\quad\Longrightarrow\quad\text{d}x=4 \sqrt{3}\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $4$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\sqrt{3}}{3}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{4} \frac{1}{\sqrt{48 - x^{2}}}\,\text{d}x &= \frac{\sqrt{3}}{12}\int_{0}^{4} \frac{1}{\sqrt{1-(\frac{\sqrt{3} x}{12})^{2}}}\,\text{d}x \\ &= \frac{\sqrt{3}}{12}\int_{0}^{\frac{\sqrt{3}}{3}} \frac{1}{\sqrt{1-(u)^{2}}}\cdot (4 \sqrt{3})\,\text{d}u \\ &= 1\int_{0}^{\frac{\sqrt{3}}{3}} \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u \\ &= \left[1\operatorname{arcsin}(u)\right]_{0}^{\frac{\sqrt{3}}{3}} \\ &= 1\operatorname{arcsin}(\frac{\sqrt{3}}{3})-(1\operatorname{arcsin}(0)) \\ &= \operatorname{arcsin}{\left(\frac{\sqrt{3}}{3} \right)}-(0) \\ &= \operatorname{arcsin}{\left(\frac{\sqrt{3}}{3} \right)}\end{aligned}
$$

---

## q-49538 original

What is the value of ${\int }_{0}^{1}\frac{1}{1+4{x}^{2}}\,\text{d}x\,?$

Field selection (radio)

- $\operatorname{arctan}⁡(2)$
- $2\operatorname{arctan}⁡(2)$
- $\frac{1}{2}\operatorname{arctan}⁡(\frac{1}{2})$
- $\frac{1}{2}\operatorname{arctan}⁡(2)$ (correct)
- $\frac{\pi }{4}$

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+{u}^{2}}\text{d}u=\operatorname{arctan}⁡u+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $4{x}^{2}=(2x)^{2}.$

So, let's substitute $u=2x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=2\,⟹\,\text{d}x=\frac{1}{2}\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $2$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{0}^{1}\frac{1}{1+4{x}^{2}}\,\text{d}x & ={\int }_{0}^{1}\frac{\text{d}x}{1+(2x)^{2}} \\  & ={\int }_{0}^{2}\frac{1}{1+{u}^{2}}\cdot (\frac{1}{2}\text{d}u) \\  & =\frac{1}{2}{\int }_{0}^{2}\frac{\text{d}u}{1+{u}^{2}} \\  & =\frac{1}{2}\operatorname{arctan}⁡u{|}_{0}^{2} \\  & =\frac{1}{2}\operatorname{arctan}⁡(2)-\frac{1}{2}\operatorname{arctan}⁡(0) \\  & =\frac{1}{2}\operatorname{arctan}⁡(2)\end{aligned}\end{aligned}
$$

---

## q-49538 {'h': 2, 'k': 3}

What is the value of $\int_{0}^{2} \frac{3}{4 x^{2} + 4}\,\text{d}x\,?$

Field selection (radio)

- $\frac{3 \operatorname{arctan}{\left(2 \right)}}{2}$
- $3 \operatorname{arctan}{\left(2 \right)}$
- $\frac{3 \operatorname{arctan}{\left(\frac{1}{2} \right)}}{4}$
- $\frac{3 \operatorname{arctan}{\left(2 \right)}}{4}$ (correct)
- $\frac{3 \pi}{8}$

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+(u)^{2}}\,\text{d}u=\operatorname{arctan}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(x)^{2}.$

So, let's substitute $u=x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=1\quad\Longrightarrow\quad\text{d}x=1\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $2$ |
| --- | --- | --- |
| $u$ | $0$ | $2$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{2} \frac{3}{4 x^{2} + 4}\,\text{d}x &= \frac{3}{4}\int_{0}^{2} \frac{1}{1+(x)^{2}}\,\text{d}x \\ &= \frac{3}{4}\int_{0}^{2} \frac{1}{1+(u)^{2}}\cdot (1)\,\text{d}u \\ &= \frac{3}{4}\int_{0}^{2} \frac{1}{1+(u)^{2}}\,\text{d}u \\ &= \left[\frac{3}{4}\operatorname{arctan}(u)\right]_{0}^{2} \\ &= \frac{3}{4}\operatorname{arctan}(2)-(\frac{3}{4}\operatorname{arctan}(0)) \\ &= \frac{3 \operatorname{arctan}{\left(2 \right)}}{4}-(0) \\ &= \frac{3 \operatorname{arctan}{\left(2 \right)}}{4}\end{aligned}
$$

---

## q-49546 original

Evaluate the integral ${\int }_{-5/2}^{5/2}\frac{\text{d}x}{\sqrt{25-{x}^{2}}}.$

Field selection (radio)

- $\frac{5\pi }{2}$
- $\frac{\pi }{6}$
- $\frac{\pi }{4}$
- $\frac{2\pi }{3}$
- $\frac{\pi }{3}$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{-5/2}^{5/2}\frac{\text{d}x}{\sqrt{25-{x}^{2}}}\, & ={\int }_{-5/2}^{5/2}\frac{1}{\sqrt{25\cdot (1-{x}^{2}/25)}}\,\text{d}x \\  & =\frac{1}{5}{\int }_{-5/2}^{5/2}\frac{1}{\sqrt{1-{x}^{2}/25}}\,\text{d}x \\  & =\frac{1}{5}{\int }_{-5/2}^{5/2}\frac{1}{\sqrt{1-(x/5)^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-{u}^{2}}}\text{d}u=\operatorname{arcsin}⁡(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(\frac{x}{5})}^{2}.$

So, let's substitute $u=\frac{x}{5}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{5}\,⟹\,\text{d}x=5\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $-\frac{5}{2}$ | $\frac{5}{2}$ |
| --- | --- | --- |
| $u$ | $-\frac{1}{2}$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{-5/2}^{5/2}\frac{\text{d}x}{\sqrt{25-{x}^{2}}} & =\frac{1}{5}{\int }_{-5/2}^{5/2}\frac{1}{\sqrt{1-(x/5)^{2}}}\,\text{d}x \\  & =\frac{1}{5}{\int }_{-1/2}^{1/2}\frac{1}{\sqrt{1-{u}^{2}}}\cdot (5\,\text{d}u) \\  & ={\int }_{-1/2}^{1/2}\frac{\text{d}u}{\sqrt{1-{u}^{2}}} \\  & =\operatorname{arcsin}⁡u{|}_{-1/2}^{1/2} \\  & =\operatorname{arcsin}⁡(\frac{1}{2})-\operatorname{arcsin}⁡(-\frac{1}{2}) \\  & =\frac{\pi }{6}+\frac{\pi }{6} \\  & =\frac{\pi }{3}\end{aligned}\end{aligned}
$$

---

## q-49546 {'h': 2, 'k': 3}

Evaluate the integral $\int_{-5}^{5} \frac{3}{\sqrt{100 - x^{2}}}\,\text{d}x.$

Field selection (radio)

- $\frac{15 \pi}{2}$
- $\frac{\pi}{2}$
- $\frac{3 \pi}{4}$
- $2 \pi$
- $\pi$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{-5}^{5} \frac{3}{\sqrt{100 - x^{2}}}\,\text{d}x &= \int_{-5}^{5} \frac{3}{\sqrt{100(1-\frac{x^{2}}{100})}}\,\text{d}x \\ &= \frac{3}{10}\int_{-5}^{5} \frac{1}{\sqrt{1-\frac{x^{2}}{100}}}\,\text{d}x \\ &= \frac{3}{10}\int_{-5}^{5} \frac{1}{\sqrt{1-(\frac{x}{10})^{2}}}\,\text{d}x\end{aligned}
$$

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{x}{10})^{2}.$

So, let's substitute $u=\frac{x}{10}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{10}\quad\Longrightarrow\quad\text{d}x=10\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $-5$ | $5$ |
| --- | --- | --- |
| $u$ | $- \frac{1}{2}$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{-5}^{5} \frac{3}{\sqrt{100 - x^{2}}}\,\text{d}x &= \frac{3}{10}\int_{-5}^{5} \frac{1}{\sqrt{1-(\frac{x}{10})^{2}}}\,\text{d}x \\ &= \frac{3}{10}\int_{- \frac{1}{2}}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\cdot (10)\,\text{d}u \\ &= 3\int_{- \frac{1}{2}}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u \\ &= \left[3\operatorname{arcsin}(u)\right]_{- \frac{1}{2}}^{\frac{1}{2}} \\ &= 3\operatorname{arcsin}(\frac{1}{2})-(3\operatorname{arcsin}(- \frac{1}{2})) \\ &= \frac{\pi}{2}-(- \frac{\pi}{2}) \\ &= \pi\end{aligned}
$$

---

## q-351850 original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{25}\frac{1}{25+{x}^{2}}\,\text{d}x=$
{{field-1}}
$\operatorname{arctan}⁡($
{{field-2}}$)$

Field field-1 (blank)

- $\frac{1}{5}$ (correct)
Field field-2 (blank)

- $5$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{0}^{25}\frac{1}{25+{x}^{2}}\,\text{d}x & ={\int }_{0}^{25}\frac{1}{25\cdot (1+{x}^{2}/25)}\,\text{d}x \\  & =\frac{1}{25}{\int }_{0}^{25}\frac{1}{1+{x}^{2}/25}\,\text{d}x \\  & =\frac{1}{25}{\int }_{0}^{25}\frac{1}{1+(x/5)^{2}}\,\text{d}x\end{aligned}
$$

 

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+{u}^{2}}\text{d}u=\operatorname{arctan}⁡u+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(\frac{x}{5})}^{2}.$

So, let's substitute $u=\frac{x}{5}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{5}\,⟹\,\text{d}x=5\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $25$ |
| --- | --- | --- |
| $u$ | $0$ | $5$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{0}^{25}\frac{1}{25+{x}^{2}}\,\text{d}x & =\frac{1}{25}{\int }_{0}^{25}\frac{1}{1+(x/5)^{2}}\,\text{d}x \\  & =\frac{1}{25}{\int }_{0}^{5}\frac{1}{1+{u}^{2}}\cdot (5\,\text{d}u) \\  & =\frac{1}{5}{\int }_{0}^{5}\frac{\text{d}u}{1+{u}^{2}} \\  & =\frac{1}{5}\operatorname{arctan}⁡u{|}_{0}^{5} \\  & =\frac{1}{5}(\operatorname{arctan}⁡(5)-\operatorname{arctan}⁡(0)) \\  & =\frac{1}{5}\,\operatorname{arctan}\,(5)\end{aligned}\end{aligned}
$$

---

## q-351850 {'h': 2, 'k': 3}

Evaluate the following integral. Do not round the answer.

$\int_{0}^{50} \frac{3}{x^{2} + 100}\,\text{d}x=$
{{field-1}}
$\operatorname{arctan}⁡($
{{field-2}}$)$

Field field-1 (blank)

- $\frac{3}{10}$ (correct)
Field field-2 (blank)

- $5$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{0}^{50} \frac{3}{x^{2} + 100}\,\text{d}x &= \int_{0}^{50} \frac{3}{100(1+\frac{x^{2}}{100})}\,\text{d}x \\ &= \frac{3}{100}\int_{0}^{50} \frac{1}{1+\frac{x^{2}}{100}}\,\text{d}x \\ &= \frac{3}{100}\int_{0}^{50} \frac{1}{1+(\frac{x}{10})^{2}}\,\text{d}x\end{aligned}
$$

 

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+(u)^{2}}\,\text{d}u=\operatorname{arctan}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{x}{10})^{2}.$

So, let's substitute $u=\frac{x}{10}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{10}\quad\Longrightarrow\quad\text{d}x=10\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $50$ |
| --- | --- | --- |
| $u$ | $0$ | $5$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{50} \frac{3}{x^{2} + 100}\,\text{d}x &= \frac{3}{100}\int_{0}^{50} \frac{1}{1+(\frac{x}{10})^{2}}\,\text{d}x \\ &= \frac{3}{100}\int_{0}^{5} \frac{1}{1+(u)^{2}}\cdot (10)\,\text{d}u \\ &= \frac{3}{10}\int_{0}^{5} \frac{1}{1+(u)^{2}}\,\text{d}u \\ &= \left[\frac{3}{10}\operatorname{arctan}(u)\right]_{0}^{5} \\ &= \frac{3}{10}\operatorname{arctan}(5)-(\frac{3}{10}\operatorname{arctan}(0)) \\ &= \frac{3 \operatorname{arctan}{\left(5 \right)}}{10}-(0) \\ &= \frac{3 \operatorname{arctan}{\left(5 \right)}}{10}\end{aligned}
$$

---

## q-351845 original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{3}\frac{10}{9+{x}^{2}}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{5\pi }{6}$
- $\frac{5\pi}{6}$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{0}^{3}\frac{10}{9+{x}^{2}}\,\text{d}x & ={\int }_{0}^{3}\frac{10}{9\cdot (1+{x}^{2}/9)}\,\text{d}x \\  & =\frac{10}{9}{\int }_{0}^{3}\frac{1}{1+{x}^{2}/9}\,\text{d}x \\  & =\frac{10}{9}{\int }_{0}^{3}\frac{1}{1+(x/3)^{2}}\,\text{d}x\end{aligned}
$$

 

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+{u}^{2}}\text{d}u=\operatorname{arctan}⁡u+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(\frac{x}{3})}^{2}.$

So, let's substitute $u=\frac{x}{3}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{3}\,⟹\,\text{d}x=3\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $3$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{3}\frac{10}{9+{x}^{2}}\,\text{d}x & =\frac{10}{9}{\int }_{0}^{3}\frac{1}{1+(x/3)^{2}}\,\text{d}x \\  & =\frac{10}{9}{\int }_{0}^{1}\frac{1}{1+{u}^{2}}\cdot (3\,\text{d}u) \\  & =\frac{10}{3}{\int }_{0}^{1}\frac{\text{d}u}{1+{u}^{2}} \\  & =\frac{10}{3}\operatorname{arctan}⁡u{|}_{0}^{1} \\  & =\frac{10}{3}\operatorname{arctan}⁡(1)-\frac{10}{3}\operatorname{arctan}⁡(0) \\  & =\frac{10}{3}\cdot \frac{\pi }{4} \\  & =\frac{5\pi }{6}\end{aligned}
$$

---

## q-351845 {'h': 2, 'k': 3}

Evaluate the following integral. Do not round the answer.

$\int_{0}^{6} \frac{30}{x^{2} + 36}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{5 \pi}{4}$
- $\frac{5 \pi}{4}$ (correct)

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{0}^{6} \frac{30}{x^{2} + 36}\,\text{d}x &= \int_{0}^{6} \frac{30}{36(1+\frac{x^{2}}{36})}\,\text{d}x \\ &= \frac{5}{6}\int_{0}^{6} \frac{1}{1+\frac{x^{2}}{36}}\,\text{d}x \\ &= \frac{5}{6}\int_{0}^{6} \frac{1}{1+(\frac{x}{6})^{2}}\,\text{d}x\end{aligned}
$$

 

This integral resembles the basic integral for inverse tangent,

$$
\int \frac{1}{1+(u)^{2}}\,\text{d}u=\operatorname{arctan}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{x}{6})^{2}.$

So, let's substitute $u=\frac{x}{6}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{6}\quad\Longrightarrow\quad\text{d}x=6\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $6$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{6} \frac{30}{x^{2} + 36}\,\text{d}x &= \frac{5}{6}\int_{0}^{6} \frac{1}{1+(\frac{x}{6})^{2}}\,\text{d}x \\ &= \frac{5}{6}\int_{0}^{1} \frac{1}{1+(u)^{2}}\cdot (6)\,\text{d}u \\ &= 5\int_{0}^{1} \frac{1}{1+(u)^{2}}\,\text{d}u \\ &= \left[5\operatorname{arctan}(u)\right]_{0}^{1} \\ &= 5\operatorname{arctan}(1)-(5\operatorname{arctan}(0)) \\ &= \frac{5 \pi}{4}-(0) \\ &= \frac{5 \pi}{4}\end{aligned}
$$

---

## q-114075 original

Evaluate the integral ${\int }_{0}^{3/2}\frac{3}{\sqrt{9-{x}^{2}}}\,\text{d}x.$

Field selection (radio)

- $\frac{\pi }{2}$ (correct)
- $\frac{\pi }{3}$
- $\frac{3\pi }{2}$
- $\frac{\pi }{6}$
- $2\pi$

Let's rewrite our integral as follows:

$$
\begin{aligned}{\int }_{0}^{3/2}\frac{3}{\sqrt{9-{x}^{2}}}\,\text{d}x & =3{\int }_{0}^{3/2}\frac{1}{\sqrt{9\cdot (1-{x}^{2}/9)}}\,\text{d}x \\  & =3\cdot \frac{1}{3}{\int }_{0}^{3/2}\frac{1}{\sqrt{1-{x}^{2}/9}}\,\text{d}x \\  & ={\int }_{0}^{3/2}\frac{1}{\sqrt{1-(x/3)^{2}}}\,\text{d}x\end{aligned}
$$

  

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-{u}^{2}}}\text{d}u=\operatorname{arcsin}⁡(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have ${(\frac{x}{3})}^{2}.$

So, let's substitute $u=\frac{x}{3}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{3}\,⟹\,\text{d}x=3\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $\frac{3}{2}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{3/2}\frac{3}{\sqrt{9-{x}^{2}}}\,\text{d}x & ={\int }_{0}^{3/2}\frac{1}{\sqrt{1-(x/3)^{2}}}\,\text{d}x \\  & ={\int }_{0}^{1/2}\frac{1}{\sqrt{1-{u}^{2}}}\cdot (3\,\text{d}u) \\  & =3{\int }_{0}^{1/2}\frac{\text{d}u}{\sqrt{1-{u}^{2}}} \\  & =3\operatorname{arcsin}⁡u{|}_{0}^{1/2} \\  & =3(\operatorname{arcsin}⁡(\frac{1}{2})-\operatorname{arcsin}⁡(0)) \\  & =3(\frac{\pi }{6}-0) \\  & =\frac{\pi }{2}\end{aligned}
$$

---

## q-114075 {'h': 2, 'k': 3}

Evaluate the integral $\int_{0}^{3} \frac{9}{\sqrt{36 - x^{2}}}\,\text{d}x.$

Field selection (radio)

- $\frac{3 \pi}{2}$ (correct)
- $\pi$
- $\frac{9 \pi}{2}$
- $\frac{\pi}{2}$
- $6 \pi$

Let's rewrite our integral as follows:

$$
\begin{aligned}\int_{0}^{3} \frac{9}{\sqrt{36 - x^{2}}}\,\text{d}x &= \int_{0}^{3} \frac{9}{\sqrt{36(1-\frac{x^{2}}{36})}}\,\text{d}x \\ &= \frac{3}{2}\int_{0}^{3} \frac{1}{\sqrt{1-\frac{x^{2}}{36}}}\,\text{d}x \\ &= \frac{3}{2}\int_{0}^{3} \frac{1}{\sqrt{1-(\frac{x}{6})^{2}}}\,\text{d}x\end{aligned}
$$

  

This integral resembles the basic integral for inverse sine,

$$
\int \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.
$$

The only difference is that instead of ${u}^{2}$ as the variable, we have $(\frac{x}{6})^{2}.$

So, let's substitute $u=\frac{x}{6}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{6}\quad\Longrightarrow\quad\text{d}x=6\,\text{d}u.
$$

Before substituting, we use the table below to change the limits from $x$ to $u.$

| $x$ | $0$ | $3$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{1}{2}$ |

Using the above, we can now write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{3} \frac{9}{\sqrt{36 - x^{2}}}\,\text{d}x &= \frac{3}{2}\int_{0}^{3} \frac{1}{\sqrt{1-(\frac{x}{6})^{2}}}\,\text{d}x \\ &= \frac{3}{2}\int_{0}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\cdot (6)\,\text{d}u \\ &= 9\int_{0}^{\frac{1}{2}} \frac{1}{\sqrt{1-(u)^{2}}}\,\text{d}u \\ &= \left[9\operatorname{arcsin}(u)\right]_{0}^{\frac{1}{2}} \\ &= 9\operatorname{arcsin}(\frac{1}{2})-(9\operatorname{arcsin}(0)) \\ &= \frac{3 \pi}{2}-(0) \\ &= \frac{3 \pi}{2}\end{aligned}
$$
