# Original and generated definite-integral review

Originals are preserved evidence; all anchors and changed variants below come from the same parameterized generator. source_bank retains the complete empirical bank; authored_method_bank labels the normal bank extension.

## q-13751 — faithful parameterized anchor

Original prompt:

Evaluate the integral ${\int }_{0}^{\sqrt{\operatorname{ln}⁡3}}5x{e}^{{x}^{2}}\,\text{d}x.$

Original complete bank:

- $\frac{15}{2}$
- $3$
- $2\operatorname{ln}⁡3$
- $5$
- $\operatorname{ln}⁡3$

Original solution:

Let's introduce the new variable $u={x}^{2}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $\sqrt{\operatorname{ln}⁡3}$ |
| --- | --- | --- |
| $u$ | $0$ | $\operatorname{ln}⁡3$ |

Therefore, we get

$$
\begin{aligned}{\int }_{0}^{\sqrt{\operatorname{ln}⁡3}}5x{e}^{{x}^{2}}\,\text{d}x & ={\int }_{0}^{\sqrt{\operatorname{ln}⁡3}}5{e}^{{x}^{2}}\cdot x\,\text{d}x \\  & ={\int }_{0}^{\operatorname{ln}⁡3}5{e}^{u}\cdot \frac{1}{2}\text{d}u \\  & =\frac{5}{2}{\int }_{0}^{\operatorname{ln}⁡3}{e}^{u}\,\text{d}u \\  & =\frac{5}{2}{e}^{u}\,{|}_{0}^{\operatorname{ln}⁡3} \\  & =\frac{5}{2}({e}^{\operatorname{ln}⁡3}-{e}^{0}) \\  & =\frac{5}{2}(3-1) \\  & =\frac{5}{2}(2) \\  & =5.\end{aligned}
$$

Profile: `source_bank`; parameters: `{'c': 5, 'b': 3}`.

Evaluate the integral $\int_{0}^{\sqrt{\ln(3)}}5xe^{x^{2}}\,\mathrm{d}x.$

- $2 \ln{\left(3 \right)}$
- $3$
- $\frac{15}{2}$
- $\ln{\left(3 \right)}$
- $5$

Let's introduce the new variable $u=x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=2x\quad\Longrightarrow\quad \frac{1}{2}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $\sqrt{\ln(3)}$ |
| --- | --- | --- |
| $u$ | $0$ | $\ln(3)$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{\sqrt{\ln(3)}}5xe^{x^{2}}\,\mathrm{d}x &= \int_{0}^{\sqrt{\ln(3)}}5e^{x^{2}}\cdot x\,\mathrm{d}x \\ & = \int_{0}^{\ln(3)}5e^{u}\cdot \frac{1}{2}\,\mathrm{d}u \\ & = \frac{5}{2}\int_{0}^{\ln(3)}e^{u}\,\mathrm{d}u \\ & = \frac{5}{2}e^{u}\big|_{0}^{\ln(3)} \\ & = \frac{5}{2}(e^{\ln(3)}-e^{0}) \\ & = \frac{5}{2}(3-1) \\ & = \frac{5}{2}(2) \\ & = 5.\end{aligned}
$$

## q-30953 — faithful parameterized anchor

Original prompt:

Evaluate the integral ${\int }_{0}^{\sqrt{\operatorname{ln}⁡5}}\frac{1}{5}x{e}^{2{x}^{2}}\,\text{d}x.$

Original complete bank:

- $\frac{1}{20}$
- $\frac{6}{5}$
- $\frac{1}{5}$
- $6$
- $\frac{3}{20}$

Original solution:

Let's introduce the new variable $u=2{x}^{2}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=4x\,⟹\,\frac{1}{4}\,\text{d}u=x\,\text{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $\sqrt{\operatorname{ln}⁡5}$ |
| --- | --- | --- |
| $u$ | $0$ | $2\operatorname{ln}⁡5$ |

Therefore, we get

$$
\begin{aligned}{\int }_{0}^{\sqrt{\operatorname{ln}⁡5}}\frac{1}{5}x{e}^{2{x}^{2}}\,\text{d}x & =\frac{1}{5}{\int }_{0}^{\sqrt{\operatorname{ln}⁡5}}{e}^{2{x}^{2}}\cdot x\,\text{d}x \\  & =\frac{1}{5}{\int }_{0}^{2\operatorname{ln}⁡5}{e}^{u}\cdot \frac{1}{4}\,\text{d}u \\  & =\frac{1}{20}{\int }_{0}^{2\operatorname{ln}⁡5}{e}^{u}\,\text{d}u \\  & =\frac{1}{20}{e}^{u}\,{|}_{0}^{2\operatorname{ln}⁡5} \\  & =\frac{1}{20}({e}^{2\operatorname{ln}⁡5}-{e}^{0}) \\  & =\frac{1}{20}(25-1) \\  & =\frac{24}{20} \\  & =\frac{6}{5}.\end{aligned}
$$

Profile: `source_bank`; parameters: `{'d': 5, 'b': 5}`.

Evaluate the integral $\int_{0}^{\sqrt{\ln(5)}}\frac{1}{5}xe^{2x^{2}}\,\mathrm{d}x.$

- $\frac{1}{5}$
- $\frac{6}{5}$
- $\frac{1}{20}$
- $\frac{3}{20}$
- $6$

Let's introduce the new variable $u=2x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=4x\quad\Longrightarrow\quad \frac{1}{4}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $\sqrt{\ln(5)}$ |
| --- | --- | --- |
| $u$ | $0$ | $2\ln(5)$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{\sqrt{\ln(5)}}\frac{1}{5}xe^{2x^{2}}\,\mathrm{d}x &= \frac{1}{5}\int_{0}^{\sqrt{\ln(5)}}e^{2x^{2}}\cdot x\,\mathrm{d}x \\ & = \frac{1}{5}\int_{0}^{2\ln(5)}e^{u}\cdot \frac{1}{4}\,\mathrm{d}u \\ & = \frac{1}{20}\int_{0}^{2\ln(5)}e^{u}\,\mathrm{d}u \\ & = \frac{1}{20}e^{u}\big|_{0}^{2\ln(5)} \\ & = \frac{1}{20}(e^{2\ln(5)}-e^{0}) \\ & = \frac{1}{20}(25-1) \\ & = \frac{24}{20} \\ & = \frac{6}{5}.\end{aligned}
$$

## q-350740 — faithful parameterized anchor

Original prompt:

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\sqrt{\operatorname{ln}⁡2}}x{e}^{3{x}^{2}+\operatorname{ln}⁡2}\,\text{d}x=$
{{field-1}}

Original complete bank:

- $\frac{7}{3}$

Original solution:

Let's introduce the new variable $u=3{x}^{2}+\operatorname{ln}⁡2.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=6x\,⟹\,\frac{1}{6}\text{d}u=x\,\text{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $\sqrt{\operatorname{ln}⁡2}$ |
| --- | --- | --- |
| $u$ | $\operatorname{ln}⁡2$ | $4\operatorname{ln}⁡2$ |

Therefore, we get

$$
\begin{aligned}{\int }_{0}^{\sqrt{\operatorname{ln}⁡2}}x{e}^{3{x}^{2}+\operatorname{ln}⁡2}\,\text{d}x & ={\int }_{\operatorname{ln}⁡2}^{4\operatorname{ln}⁡2}{e}^{u}\cdot \frac{1}{6}\text{d}u \\  & =\frac{1}{6}{\int }_{\operatorname{ln}⁡2}^{4\operatorname{ln}⁡2}{e}^{u}\,\text{d}u \\  & =\frac{1}{6}{e}^{u}\,{|}_{\operatorname{ln}⁡2}^{4\operatorname{ln}⁡2} \\  & =\frac{1}{6}({e}^{4\operatorname{ln}⁡2}-{e}^{\operatorname{ln}⁡2}) \\  & =\frac{1}{6}(16-2) \\  & =\frac{7}{3}.\end{aligned}
$$

Profile: `source_presentation`; parameters: `{'b': 2, 'k': 3}`.

Evaluate the following integral. Do not round the answer.

$\int_{0}^{\sqrt{\ln(2)}}xe^{3x^{2}+\ln(2)}\,\mathrm{d}x=$
{{field-1}}

- $\frac{7}{3}$

Let's introduce the new variable $u=3x^{2}+\ln(2).$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=6x\quad\Longrightarrow\quad \frac{1}{6}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $\sqrt{\ln(2)}$ |
| --- | --- | --- |
| $u$ | $\ln(2)$ | $4\ln(2)$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{\sqrt{\ln(2)}}xe^{3x^{2}+\ln(2)}\,\mathrm{d}x &= \int_{\ln(2)}^{4\ln(2)}e^{u}\cdot \frac{1}{6}\,\mathrm{d}u \\ & = \frac{1}{6}\int_{\ln(2)}^{4\ln(2)}e^{u}\,\mathrm{d}u \\ & = \frac{1}{6}e^{u}\big|_{\ln(2)}^{4\ln(2)} \\ & = \frac{1}{6}(e^{4\ln(2)}-e^{\ln(2)}) \\ & = \frac{1}{6}(16-2) \\ & = \frac{7}{3}.\end{aligned}
$$

## q-30977 — faithful parameterized anchor

Original prompt:

Evaluate the integral $\displaystyle \int_{0}^{1}x2^{3x^{2}}dx$.

Original complete bank:

- $\frac{7}{3\ln 2}$
- $\frac{7}{6\ln 2}$
- $\frac{1}{6\ln 2}$
- $\frac{7}{2\ln 2}$
- $\frac{1}{8\ln 2}$

Original solution:

Missing in captured original. The full served solution below is independently authored.

Profile: `source_bank`; parameters: `{'b': 2, 'k': 3}`.

Evaluate the integral $\int_{0}^{1}x2^{3x^{2}}\,\mathrm{d}x.$

- $\frac{1}{6 \ln{\left(2 \right)}}$
- $\frac{7}{6 \ln{\left(2 \right)}}$
- $\frac{7}{3 \ln{\left(2 \right)}}$
- $\frac{1}{8 \ln{\left(2 \right)}}$
- $\frac{7}{2 \ln{\left(2 \right)}}$

Let's introduce the new variable $u=3x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=6x\quad\Longrightarrow\quad \frac{1}{6}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $3$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{1}x2^{3x^{2}}\,\mathrm{d}x &= \int_{0}^{1}2^{3x^{2}}\cdot x\,\mathrm{d}x \\ & = \int_{0}^{3}2^{u}\cdot \frac{1}{6}\,\mathrm{d}u \\ & = \frac{1}{6}\int_{0}^{3}2^{u}\,\mathrm{d}u \\ & = \frac{1}{6}\frac{2^{u}}{\ln(2)}\big|_{0}^{3} \\ & = \frac{1}{6}\frac{1}{\ln(2)}(8-1) \\ & = \frac{7}{6 \ln{\left(2 \right)}}.\end{aligned}
$$

## q-30978 — faithful parameterized anchor

Original prompt:

Evaluate the integral ${\int }_{0}^{1}x{4}^{{x}^{2}}\,\text{d}x.$

Original complete bank:

- $\frac{4}{3\operatorname{ln}⁡2}$
- $\frac{4\operatorname{ln}⁡2}{3}$
- $\frac{3\operatorname{ln}⁡2}{4}$
- $\frac{3}{4\operatorname{ln}⁡2}$
- $\frac{3}{\operatorname{ln}⁡2}$

Original solution:

Let's introduce the new variable $u={x}^{2}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\,\text{d}u=x\,\text{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Therefore, we get

$$
\begin{aligned}{\int }_{0}^{1}x{4}^{{x}^{2}}\,\text{d}x & ={\int }_{0}^{1}{4}^{{x}^{2}}\cdot x\,\text{d}x \\  & ={\int }_{0}^{1}{4}^{u}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}{\int }_{0}^{1}{4}^{u}\,\text{d}u \\  & =\frac{1}{2}\frac{{4}^{u}}{\operatorname{ln}⁡4}\,{|}_{0}^{1} \\  & =\frac{1}{2\operatorname{ln}⁡4}(4-1) \\  & =\frac{3}{2\operatorname{ln}⁡4} \\  & =\frac{3}{4\operatorname{ln}⁡2}.\end{aligned}
$$

Profile: `source_bank`; parameters: `{'b': 2}`.

Evaluate the integral $\int_{0}^{1}x4^{x^{2}}\,\mathrm{d}x.$

- $\frac{3 \ln{\left(2 \right)}}{4}$
- $\frac{4 \ln{\left(2 \right)}}{3}$
- $\frac{4}{3 \ln{\left(2 \right)}}$
- $\frac{3}{\ln{\left(2 \right)}}$
- $\frac{3}{2 \ln{\left(4 \right)}}$

Let's introduce the new variable $u=x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=2x\quad\Longrightarrow\quad \frac{1}{2}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{1}x4^{x^{2}}\,\mathrm{d}x &= \int_{0}^{1}4^{x^{2}}\cdot x\,\mathrm{d}x \\ & = \int_{0}^{1}4^{u}\cdot \frac{1}{2}\,\mathrm{d}u \\ & = \frac{1}{2}\int_{0}^{1}4^{u}\,\mathrm{d}u \\ & = \frac{1}{2}\frac{4^{u}}{\ln(4)}\big|_{0}^{1} \\ & = \frac{1}{2}\frac{1}{\ln(4)}(4-1) \\ & = \frac{3}{2\ln(4)} \\ & = \frac{3}{4 \ln{\left(2 \right)}}.\end{aligned}
$$

## q-346400 — faithful parameterized anchor

Original prompt:

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{1}2x\cdot {3}^{{x}^{2}}\,\text{d}x=$  
{{field-1}}

Original complete bank:

- $\frac{2}{\operatorname{ln}(3)}$

Original solution:

Let's introduce the new variable $u={x}^{2}.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\text{d}u=2x\,\text{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Therefore, we get

$$
\begin{aligned}{\int }_{0}^{1}2x\cdot {3}^{{x}^{2}}\,\text{d}x & ={\int }_{0}^{1}{3}^{u}\,\text{d}u \\  & ={\frac{{3}^{u}}{\operatorname{ln}⁡(3)}\,|}_{0}^{1} \\  & =\frac{1}{\operatorname{ln}⁡(3)}({3}^{1}-{3}^{0}) \\  & =\frac{1}{\operatorname{ln}⁡(3)}(3-1) \\  & =\frac{2}{\operatorname{ln}⁡(3)}.\end{aligned}
$$

Profile: `source_presentation`; parameters: `{'b': 3}`.

Evaluate the following integral. Do not round the answer.

$\int_{0}^{1}2x\cdot 3^{x^{2}}\,\mathrm{d}x=$
{{field-1}}

- $\frac{2}{\ln{\left(3 \right)}}$

Let's introduce the new variable $u=x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=2x\quad\Longrightarrow\quad \mathrm{d}u=2x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{1}2x\cdot 3^{x^{2}}\,\mathrm{d}x &= \int_{0}^{1}3^{u}\,\mathrm{d}u \\ & = \frac{3^{u}}{\ln(3)}\big|_{0}^{1} \\ & = \frac{1}{\ln(3)}(3^{1}-3^{0}) \\ & = \frac{1}{\ln(3)}(3-1) \\ & = \frac{2}{\ln{\left(3 \right)}}.\end{aligned}
$$

## q-350743 — faithful parameterized anchor

Original prompt:

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{1}2\cdot {3}^{2x+1}\,\text{d}x=$  
{{field-1}}

Original complete bank:

- $\frac{24}{\operatorname{ln}(3)}$

Original solution:

Let's introduce the new variable $u=2x+1.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=2\,⟹\,\text{d}u=2\,\text{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $1$ | $3$ |

Therefore, we get

$$
\begin{aligned}{\int }_{0}^{1}2\cdot {3}^{2x+1}\,\text{d}x & ={\int }_{1}^{3}{3}^{u}\,\text{d}u \\  & ={\frac{{3}^{u}}{\operatorname{ln}⁡(3)}\,|}_{1}^{3} \\  & =\frac{1}{\operatorname{ln}⁡(3)}({3}^{3}-{3}^{1}) \\  & =\frac{1}{\operatorname{ln}⁡(3)}(27-3) \\  & =\frac{24}{\operatorname{ln}⁡(3)}.\end{aligned}
$$

Profile: `source_presentation`; parameters: `{'b': 3, 'k': 2, 'h': 1}`.

Evaluate the following integral. Do not round the answer.

$\int_{0}^{1}2\cdot 3^{2x+1}\,\mathrm{d}x=$
{{field-1}}

- $\frac{24}{\ln{\left(3 \right)}}$

Let's introduce the new variable $u=2x+1.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=2\quad\Longrightarrow\quad \mathrm{d}u=2\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $1$ | $3$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{1}2\cdot 3^{2x+1}\,\mathrm{d}x &= \int_{1}^{3}3^{u}\,\mathrm{d}u \\ & = \frac{3^{u}}{\ln(3)}\big|_{1}^{3} \\ & = \frac{1}{\ln(3)}(3^{3}-3^{1}) \\ & = \frac{1}{\ln(3)}(27-3) \\ & = \frac{24}{\ln{\left(3 \right)}}.\end{aligned}
$$

## q-350751 — faithful parameterized anchor

Original prompt:

Evaluate the following integral. Do not round the answer.

${\int }_{\operatorname{ln}⁡2}^{\operatorname{ln}⁡5}\frac{12{e}^{x}}{3{e}^{x}+1}\,\text{d}x=$  
{{field-1}}

Original complete bank:

- $4\operatorname{ln}(\frac{16}{7})$

Original solution:

Let's introduce the new variable $u=3{e}^{x}+1.$ Differentiating gives

$$
\frac{\text{d}u}{\text{d}x}=3{e}^{x}\,⟹\,\text{d}u=3{e}^{x}\,\text{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $\operatorname{ln}⁡2$ | $\operatorname{ln}⁡5$ |
| --- | --- | --- |
| $u$ | $7$ | $16$ |

Therefore, we get

$$
\begin{aligned}{\int }_{\operatorname{ln}⁡2}^{\operatorname{ln}⁡5}\frac{12{e}^{x}}{3{e}^{x}+1}\,\text{d}x & ={\int }_{\operatorname{ln}⁡2}^{\operatorname{ln}⁡5}\frac{4}{3{e}^{x}+1}\cdot 3{e}^{x}\,\text{d}x \\  & ={\int }_{7}^{16}\frac{4}{u}\cdot \,\text{d}u \\  & =4{\int }_{7}^{16}\frac{1}{u}\,\text{d}u \\  & =4\operatorname{ln}⁡|u|\,{|}_{7}^{16} \\  & =4(\operatorname{ln}⁡(16)-\operatorname{ln}⁡(7)) \\  & =4\operatorname{ln}⁡(\frac{16}{7}).\end{aligned}
$$

Profile: `source_presentation`; parameters: `{'a': 3, 'c': 4, 'h': 1, 'l': 2, 'r': 5}`.

Evaluate the following integral. Do not round the answer.

$\int_{\ln(2)}^{\ln(5)}\frac{12e^{x}}{3e^{x}+1}\,\mathrm{d}x=$
{{field-1}}

- $4 \ln{\left(\frac{16}{7} \right)}$

Let's introduce the new variable $u=3e^{x}+1.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=3e^{x}\quad\Longrightarrow\quad \mathrm{d}u=3e^{x}\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $\ln(2)$ | $\ln(5)$ |
| --- | --- | --- |
| $u$ | $7$ | $16$ |

Therefore, we get

$$
\begin{aligned}\int_{\ln(2)}^{\ln(5)}\frac{12e^{x}}{3e^{x}+1}\,\mathrm{d}x &= \int_{\ln(2)}^{\ln(5)}\frac{4}{3e^{x}+1}\cdot 3e^{x}\,\mathrm{d}x \\ & = \int_{7}^{16}\frac{4}{u}\,\mathrm{d}u \\ & = 4\int_{7}^{16}\frac{1}{u}\,\mathrm{d}u \\ & = 4\ln|u|\big|_{7}^{16} \\ & = 4(\ln(16)-\ln(7)) \\ & = 4 \ln{\left(\frac{16}{7} \right)}.\end{aligned}
$$

## q-13751 — changed variant

Profile: `authored_method_bank`; parameters: `{'c': 2, 'b': 3}`.

Evaluate the integral $\int_{0}^{\sqrt{\ln(3)}}2xe^{x^{2}}\,\mathrm{d}x.$

- $4$
- $3$
- $2$
- $1$
- $-2$

Let's introduce the new variable $u=x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=2x\quad\Longrightarrow\quad \frac{1}{2}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $\sqrt{\ln(3)}$ |
| --- | --- | --- |
| $u$ | $0$ | $\ln(3)$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{\sqrt{\ln(3)}}2xe^{x^{2}}\,\mathrm{d}x &= \int_{0}^{\sqrt{\ln(3)}}2e^{x^{2}}\cdot x\,\mathrm{d}x \\ & = \int_{0}^{\ln(3)}2e^{u}\cdot \frac{1}{2}\,\mathrm{d}u \\ & = 1\int_{0}^{\ln(3)}e^{u}\,\mathrm{d}u \\ & = 1e^{u}\big|_{0}^{\ln(3)} \\ & = 1(e^{\ln(3)}-e^{0}) \\ & = 1(3-1) \\ & = 1(2) \\ & = 2.\end{aligned}
$$

## q-13751 — changed variant

Profile: `authored_method_bank`; parameters: `{'c': 2, 'b': 4}`.

Evaluate the integral $\int_{0}^{\sqrt{\ln(4)}}2xe^{x^{2}}\,\mathrm{d}x.$

- $6$
- $4$
- $3$
- $\frac{3}{2}$
- $-3$

Let's introduce the new variable $u=x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=2x\quad\Longrightarrow\quad \frac{1}{2}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $\sqrt{\ln(4)}$ |
| --- | --- | --- |
| $u$ | $0$ | $\ln(4)$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{\sqrt{\ln(4)}}2xe^{x^{2}}\,\mathrm{d}x &= \int_{0}^{\sqrt{\ln(4)}}2e^{x^{2}}\cdot x\,\mathrm{d}x \\ & = \int_{0}^{\ln(4)}2e^{u}\cdot \frac{1}{2}\,\mathrm{d}u \\ & = 1\int_{0}^{\ln(4)}e^{u}\,\mathrm{d}u \\ & = 1e^{u}\big|_{0}^{\ln(4)} \\ & = 1(e^{\ln(4)}-e^{0}) \\ & = 1(4-1) \\ & = 1(3) \\ & = 3.\end{aligned}
$$

## q-30953 — changed variant

Profile: `authored_method_bank`; parameters: `{'d': 2, 'b': 2}`.

Evaluate the integral $\int_{0}^{\sqrt{\ln(2)}}\frac{1}{2}xe^{2x^{2}}\,\mathrm{d}x.$

- $\frac{3}{2}$
- $\frac{1}{2}$
- $\frac{3}{8}$
- $\frac{3}{16}$
- $- \frac{3}{8}$

Let's introduce the new variable $u=2x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=4x\quad\Longrightarrow\quad \frac{1}{4}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $\sqrt{\ln(2)}$ |
| --- | --- | --- |
| $u$ | $0$ | $2\ln(2)$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{\sqrt{\ln(2)}}\frac{1}{2}xe^{2x^{2}}\,\mathrm{d}x &= \frac{1}{2}\int_{0}^{\sqrt{\ln(2)}}e^{2x^{2}}\cdot x\,\mathrm{d}x \\ & = \frac{1}{2}\int_{0}^{2\ln(2)}e^{u}\cdot \frac{1}{4}\,\mathrm{d}u \\ & = \frac{1}{8}\int_{0}^{2\ln(2)}e^{u}\,\mathrm{d}u \\ & = \frac{1}{8}e^{u}\big|_{0}^{2\ln(2)} \\ & = \frac{1}{8}(e^{2\ln(2)}-e^{0}) \\ & = \frac{1}{8}(4-1) \\ & = \frac{3}{8} \\ & = \frac{3}{8}.\end{aligned}
$$

## q-30953 — changed variant

Profile: `authored_method_bank`; parameters: `{'d': 2, 'b': 3}`.

Evaluate the integral $\int_{0}^{\sqrt{\ln(3)}}\frac{1}{2}xe^{2x^{2}}\,\mathrm{d}x.$

- $4$
- $\frac{9}{8}$
- $1$
- $\frac{1}{2}$
- $-1$

Let's introduce the new variable $u=2x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=4x\quad\Longrightarrow\quad \frac{1}{4}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $\sqrt{\ln(3)}$ |
| --- | --- | --- |
| $u$ | $0$ | $2\ln(3)$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{\sqrt{\ln(3)}}\frac{1}{2}xe^{2x^{2}}\,\mathrm{d}x &= \frac{1}{2}\int_{0}^{\sqrt{\ln(3)}}e^{2x^{2}}\cdot x\,\mathrm{d}x \\ & = \frac{1}{2}\int_{0}^{2\ln(3)}e^{u}\cdot \frac{1}{4}\,\mathrm{d}u \\ & = \frac{1}{8}\int_{0}^{2\ln(3)}e^{u}\,\mathrm{d}u \\ & = \frac{1}{8}e^{u}\big|_{0}^{2\ln(3)} \\ & = \frac{1}{8}(e^{2\ln(3)}-e^{0}) \\ & = \frac{1}{8}(9-1) \\ & = \frac{8}{8} \\ & = 1.\end{aligned}
$$

## q-350740 — changed variant

Profile: `source_blank`; parameters: `{'b': 2, 'k': 2}`.

Evaluate the following integral. Give an exact answer.

$\int_{0}^{\sqrt{\ln(2)}}xe^{2x^{2}+\ln(2)}\,\mathrm{d}x=$
{{field-1}}

- $\frac{3}{2}$

Let's introduce the new variable $u=2x^{2}+\ln(2).$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=4x\quad\Longrightarrow\quad \frac{1}{4}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $\sqrt{\ln(2)}$ |
| --- | --- | --- |
| $u$ | $\ln(2)$ | $3\ln(2)$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{\sqrt{\ln(2)}}xe^{2x^{2}+\ln(2)}\,\mathrm{d}x &= \int_{\ln(2)}^{3\ln(2)}e^{u}\cdot \frac{1}{4}\,\mathrm{d}u \\ & = \frac{1}{4}\int_{\ln(2)}^{3\ln(2)}e^{u}\,\mathrm{d}u \\ & = \frac{1}{4}e^{u}\big|_{\ln(2)}^{3\ln(2)} \\ & = \frac{1}{4}(e^{3\ln(2)}-e^{\ln(2)}) \\ & = \frac{1}{4}(8-2) \\ & = \frac{3}{2}.\end{aligned}
$$

## q-350740 — changed variant

Profile: `source_blank`; parameters: `{'b': 2, 'k': 4}`.

Evaluate the following integral. Give an exact answer.

$\int_{0}^{\sqrt{\ln(2)}}xe^{4x^{2}+\ln(2)}\,\mathrm{d}x=$
{{field-1}}

- $\frac{15}{4}$

Let's introduce the new variable $u=4x^{2}+\ln(2).$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=8x\quad\Longrightarrow\quad \frac{1}{8}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $\sqrt{\ln(2)}$ |
| --- | --- | --- |
| $u$ | $\ln(2)$ | $5\ln(2)$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{\sqrt{\ln(2)}}xe^{4x^{2}+\ln(2)}\,\mathrm{d}x &= \int_{\ln(2)}^{5\ln(2)}e^{u}\cdot \frac{1}{8}\,\mathrm{d}u \\ & = \frac{1}{8}\int_{\ln(2)}^{5\ln(2)}e^{u}\,\mathrm{d}u \\ & = \frac{1}{8}e^{u}\big|_{\ln(2)}^{5\ln(2)} \\ & = \frac{1}{8}(e^{5\ln(2)}-e^{\ln(2)}) \\ & = \frac{1}{8}(32-2) \\ & = \frac{15}{4}.\end{aligned}
$$

## q-30977 — changed variant

Profile: `authored_method_bank`; parameters: `{'b': 2, 'k': 2}`.

Evaluate the integral $\int_{0}^{1}x2^{2x^{2}}\,\mathrm{d}x.$

- $\frac{3}{\ln{\left(2 \right)}}$
- $\frac{1}{\ln{\left(2 \right)}}$
- $\frac{3}{4 \ln{\left(2 \right)}}$
- $\frac{3}{8 \ln{\left(2 \right)}}$
- $- \frac{3}{4 \ln{\left(2 \right)}}$

Let's introduce the new variable $u=2x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=4x\quad\Longrightarrow\quad \frac{1}{4}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $2$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{1}x2^{2x^{2}}\,\mathrm{d}x &= \int_{0}^{1}2^{2x^{2}}\cdot x\,\mathrm{d}x \\ & = \int_{0}^{2}2^{u}\cdot \frac{1}{4}\,\mathrm{d}u \\ & = \frac{1}{4}\int_{0}^{2}2^{u}\,\mathrm{d}u \\ & = \frac{1}{4}\frac{2^{u}}{\ln(2)}\big|_{0}^{2} \\ & = \frac{1}{4}\frac{1}{\ln(2)}(4-1) \\ & = \frac{3}{4 \ln{\left(2 \right)}}.\end{aligned}
$$

## q-30977 — changed variant

Profile: `authored_method_bank`; parameters: `{'b': 2, 'k': 4}`.

Evaluate the integral $\int_{0}^{1}x2^{4x^{2}}\,\mathrm{d}x.$

- $\frac{15}{\ln{\left(2 \right)}}$
- $\frac{2}{\ln{\left(2 \right)}}$
- $\frac{15}{8 \ln{\left(2 \right)}}$
- $\frac{15}{16 \ln{\left(2 \right)}}$
- $- \frac{15}{8 \ln{\left(2 \right)}}$

Let's introduce the new variable $u=4x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=8x\quad\Longrightarrow\quad \frac{1}{8}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $4$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{1}x2^{4x^{2}}\,\mathrm{d}x &= \int_{0}^{1}2^{4x^{2}}\cdot x\,\mathrm{d}x \\ & = \int_{0}^{4}2^{u}\cdot \frac{1}{8}\,\mathrm{d}u \\ & = \frac{1}{8}\int_{0}^{4}2^{u}\,\mathrm{d}u \\ & = \frac{1}{8}\frac{2^{u}}{\ln(2)}\big|_{0}^{4} \\ & = \frac{1}{8}\frac{1}{\ln(2)}(16-1) \\ & = \frac{15}{8 \ln{\left(2 \right)}}.\end{aligned}
$$

## q-30978 — changed variant

Profile: `authored_method_bank`; parameters: `{'b': 3}`.

Evaluate the integral $\int_{0}^{1}x9^{x^{2}}\,\mathrm{d}x.$

- $\frac{8}{\ln{\left(9 \right)}}$
- $\frac{9}{2 \ln{\left(9 \right)}}$
- $\frac{4}{\ln{\left(9 \right)}}$
- $\frac{2}{\ln{\left(9 \right)}}$
- $- \frac{4}{\ln{\left(9 \right)}}$

Let's introduce the new variable $u=x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=2x\quad\Longrightarrow\quad \frac{1}{2}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{1}x9^{x^{2}}\,\mathrm{d}x &= \int_{0}^{1}9^{x^{2}}\cdot x\,\mathrm{d}x \\ & = \int_{0}^{1}9^{u}\cdot \frac{1}{2}\,\mathrm{d}u \\ & = \frac{1}{2}\int_{0}^{1}9^{u}\,\mathrm{d}u \\ & = \frac{1}{2}\frac{9^{u}}{\ln(9)}\big|_{0}^{1} \\ & = \frac{1}{2}\frac{1}{\ln(9)}(9-1) \\ & = \frac{8}{2\ln(9)} \\ & = \frac{2}{\ln{\left(3 \right)}}.\end{aligned}
$$

## q-30978 — changed variant

Profile: `authored_method_bank`; parameters: `{'b': 4}`.

Evaluate the integral $\int_{0}^{1}x16^{x^{2}}\,\mathrm{d}x.$

- $\frac{15}{\ln{\left(16 \right)}}$
- $\frac{8}{\ln{\left(16 \right)}}$
- $\frac{15}{2 \ln{\left(16 \right)}}$
- $\frac{15}{4 \ln{\left(16 \right)}}$
- $- \frac{15}{2 \ln{\left(16 \right)}}$

Let's introduce the new variable $u=x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=2x\quad\Longrightarrow\quad \frac{1}{2}\,\mathrm{d}u=x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{1}x16^{x^{2}}\,\mathrm{d}x &= \int_{0}^{1}16^{x^{2}}\cdot x\,\mathrm{d}x \\ & = \int_{0}^{1}16^{u}\cdot \frac{1}{2}\,\mathrm{d}u \\ & = \frac{1}{2}\int_{0}^{1}16^{u}\,\mathrm{d}u \\ & = \frac{1}{2}\frac{16^{u}}{\ln(16)}\big|_{0}^{1} \\ & = \frac{1}{2}\frac{1}{\ln(16)}(16-1) \\ & = \frac{15}{2\ln(16)} \\ & = \frac{15}{8 \ln{\left(2 \right)}}.\end{aligned}
$$

## q-346400 — changed variant

Profile: `source_blank`; parameters: `{'b': 2}`.

Evaluate the following integral. Give an exact answer.

$\int_{0}^{1}2x\cdot 2^{x^{2}}\,\mathrm{d}x=$
{{field-1}}

- $\frac{1}{\ln{\left(2 \right)}}$

Let's introduce the new variable $u=x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=2x\quad\Longrightarrow\quad \mathrm{d}u=2x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{1}2x\cdot 2^{x^{2}}\,\mathrm{d}x &= \int_{0}^{1}2^{u}\,\mathrm{d}u \\ & = \frac{2^{u}}{\ln(2)}\big|_{0}^{1} \\ & = \frac{1}{\ln(2)}(2^{1}-2^{0}) \\ & = \frac{1}{\ln(2)}(2-1) \\ & = \frac{1}{\ln{\left(2 \right)}}.\end{aligned}
$$

## q-346400 — changed variant

Profile: `source_blank`; parameters: `{'b': 4}`.

Evaluate the following integral. Give an exact answer.

$\int_{0}^{1}2x\cdot 4^{x^{2}}\,\mathrm{d}x=$
{{field-1}}

- $\frac{3}{\ln{\left(4 \right)}}$

Let's introduce the new variable $u=x^{2}.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=2x\quad\Longrightarrow\quad \mathrm{d}u=2x\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $1$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{1}2x\cdot 4^{x^{2}}\,\mathrm{d}x &= \int_{0}^{1}4^{u}\,\mathrm{d}u \\ & = \frac{4^{u}}{\ln(4)}\big|_{0}^{1} \\ & = \frac{1}{\ln(4)}(4^{1}-4^{0}) \\ & = \frac{1}{\ln(4)}(4-1) \\ & = \frac{3}{\ln{\left(4 \right)}}.\end{aligned}
$$

## q-350743 — changed variant

Profile: `source_blank`; parameters: `{'b': 2, 'k': 2, 'h': 1}`.

Evaluate the following integral. Give an exact answer.

$\int_{0}^{1}2\cdot 2^{2x+1}\,\mathrm{d}x=$
{{field-1}}

- $\frac{6}{\ln{\left(2 \right)}}$

Let's introduce the new variable $u=2x+1.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=2\quad\Longrightarrow\quad \mathrm{d}u=2\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $1$ | $3$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{1}2\cdot 2^{2x+1}\,\mathrm{d}x &= \int_{1}^{3}2^{u}\,\mathrm{d}u \\ & = \frac{2^{u}}{\ln(2)}\big|_{1}^{3} \\ & = \frac{1}{\ln(2)}(2^{3}-2^{1}) \\ & = \frac{1}{\ln(2)}(8-2) \\ & = \frac{6}{\ln{\left(2 \right)}}.\end{aligned}
$$

## q-350743 — changed variant

Profile: `source_blank`; parameters: `{'b': 2, 'k': 2, 'h': 2}`.

Evaluate the following integral. Give an exact answer.

$\int_{0}^{1}2\cdot 2^{2x+2}\,\mathrm{d}x=$
{{field-1}}

- $\frac{12}{\ln{\left(2 \right)}}$

Let's introduce the new variable $u=2x+2.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=2\quad\Longrightarrow\quad \mathrm{d}u=2\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $2$ | $4$ |

Therefore, we get

$$
\begin{aligned}\int_{0}^{1}2\cdot 2^{2x+2}\,\mathrm{d}x &= \int_{2}^{4}2^{u}\,\mathrm{d}u \\ & = \frac{2^{u}}{\ln(2)}\big|_{2}^{4} \\ & = \frac{1}{\ln(2)}(2^{4}-2^{2}) \\ & = \frac{1}{\ln(2)}(16-4) \\ & = \frac{12}{\ln{\left(2 \right)}}.\end{aligned}
$$

## q-350751 — changed variant

Profile: `source_blank`; parameters: `{'a': 2, 'c': 2, 'h': 1, 'l': 2, 'r': 5}`.

Evaluate the following integral. Give an exact answer.

$\int_{\ln(2)}^{\ln(5)}\frac{4e^{x}}{2e^{x}+1}\,\mathrm{d}x=$
{{field-1}}

- $2 \ln{\left(\frac{11}{5} \right)}$

Let's introduce the new variable $u=2e^{x}+1.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=2e^{x}\quad\Longrightarrow\quad \mathrm{d}u=2e^{x}\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $\ln(2)$ | $\ln(5)$ |
| --- | --- | --- |
| $u$ | $5$ | $11$ |

Therefore, we get

$$
\begin{aligned}\int_{\ln(2)}^{\ln(5)}\frac{4e^{x}}{2e^{x}+1}\,\mathrm{d}x &= \int_{\ln(2)}^{\ln(5)}\frac{2}{2e^{x}+1}\cdot 2e^{x}\,\mathrm{d}x \\ & = \int_{5}^{11}\frac{2}{u}\,\mathrm{d}u \\ & = 2\int_{5}^{11}\frac{1}{u}\,\mathrm{d}u \\ & = 2\ln|u|\big|_{5}^{11} \\ & = 2(\ln(11)-\ln(5)) \\ & = 2 \ln{\left(\frac{11}{5} \right)}.\end{aligned}
$$

## q-350751 — changed variant

Profile: `source_blank`; parameters: `{'a': 2, 'c': 2, 'h': 1, 'l': 2, 'r': 6}`.

Evaluate the following integral. Give an exact answer.

$\int_{\ln(2)}^{\ln(6)}\frac{4e^{x}}{2e^{x}+1}\,\mathrm{d}x=$
{{field-1}}

- $2 \ln{\left(\frac{13}{5} \right)}$

Let's introduce the new variable $u=2e^{x}+1.$ Differentiating gives

$$
\frac{\mathrm{d}u}{\mathrm{d}x}=2e^{x}\quad\Longrightarrow\quad \mathrm{d}u=2e^{x}\,\mathrm{d}x.
$$

Next, we determine the new limits of integration:

| $x$ | $\ln(2)$ | $\ln(6)$ |
| --- | --- | --- |
| $u$ | $5$ | $13$ |

Therefore, we get

$$
\begin{aligned}\int_{\ln(2)}^{\ln(6)}\frac{4e^{x}}{2e^{x}+1}\,\mathrm{d}x &= \int_{\ln(2)}^{\ln(6)}\frac{2}{2e^{x}+1}\cdot 2e^{x}\,\mathrm{d}x \\ & = \int_{5}^{13}\frac{2}{u}\,\mathrm{d}u \\ & = 2\int_{5}^{13}\frac{1}{u}\,\mathrm{d}u \\ & = 2\ln|u|\big|_{5}^{13} \\ & = 2(\ln(13)-\ln(5)) \\ & = 2 \ln{\left(\frac{13}{5} \right)}.\end{aligned}
$$
