# Source and variant review

Frequency transport preserves the entire source identity-reduction sequence using substitution t=r*x. Source bank values are transported as complete mathematical objects. Prompt rendering uses standard SymPy TeX. The blank and radio versions of a mathematical task share one novelty fingerprint. All original banks and correct designations replay exactly.

## q-49273

Source

$\int \frac{{cos}^{3}⁡x+{cot}^{2}⁡x}{{cos}^{2}⁡x}\,\text{d}x=$

['-\\operatorname{sin}\u2061x-\\operatorname{tan}\u2061x+C', '\\operatorname{sin}\u2061x-\\operatorname{cot}\u2061x+C', '\\operatorname{sin}\u2061x+\\operatorname{cot}\u2061x+C', '\\operatorname{sin}\u2061x+\\operatorname{tan}\u2061x+C', '\\operatorname{sin}\u2061x-\\operatorname{tan}\u2061x+C']

We can write the integral as

$$
\int \frac{{cos}^{3}⁡x+{cot}^{2}⁡x}{{cos}^{2}⁡x}\,\text{d}x=\int \frac{1}{{cos}^{2}⁡x}({cos}^{3}⁡x+{cot}^{2}⁡x)\text{d}x.
$$

We then use the fact that ${cot}^{2}⁡x=\frac{{cos}^{2}⁡x}{{sin}^{2}⁡x}$ to express this as

$$
\int \frac{1}{{cos}^{2}⁡x}({cos}^{3}⁡x+\frac{{cos}^{2}⁡x}{{sin}^{2}⁡x})\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int \frac{{cos}^{3}⁡x+{cot}^{2}⁡x}{{cos}^{2}⁡x}\,\text{d}x & =\int \frac{1}{{cos}^{2}⁡x}({cos}^{3}⁡x+\frac{{cos}^{2}⁡x}{{sin}^{2}⁡x})\text{d}x \\  & =\int (\frac{1}{{cos}^{2}⁡x}\cdot {cos}^{3}⁡x+\frac{1}{{cos}^{2}⁡x}\cdot \frac{{cos}^{2}⁡x}{{sin}^{2}⁡x})\text{d}x \\  & =\int (\operatorname{cos}⁡x+\frac{1}{{sin}^{2}⁡x})\text{d}x \\  & =\int (\operatorname{cos}⁡x+{csc}^{2}⁡x)\text{d}x \\  & =\operatorname{sin}⁡x-\operatorname{cot}⁡x+C.\end{aligned}
$$

Variant

$\int \frac{\cos^{3}{\left(2 x \right)} + \cot^{2}{\left(2 x \right)}}{\cos^{2}{\left(2 x \right)}}\,\text{d}x=$

['C - \\frac{\\sin{\\left(2 x \\right)}}{2} - \\frac{\\tan{\\left(2 x \\right)}}{2}', 'C + \\frac{\\sin{\\left(2 x \\right)}}{2} - \\frac{\\cot{\\left(2 x \\right)}}{2}', 'C + \\frac{\\sin{\\left(2 x \\right)}}{2} + \\frac{\\cot{\\left(2 x \\right)}}{2}', 'C + \\frac{\\sin{\\left(2 x \\right)}}{2} + \\frac{\\tan{\\left(2 x \\right)}}{2}', 'C + \\frac{\\sin{\\left(2 x \\right)}}{2} - \\frac{\\tan{\\left(2 x \\right)}}{2}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can write the integral as

$$
\int \frac{{cos}^{3}⁡t+{cot}^{2}⁡t}{{cos}^{2}⁡t}\,\text{d}t=\int \frac{1}{{cos}^{2}⁡t}({cos}^{3}⁡t+{cot}^{2}⁡t)\text{d}t.
$$

We then use the fact that ${cot}^{2}⁡t=\frac{{cos}^{2}⁡t}{{sin}^{2}⁡t}$ to express this as

$$
\int \frac{1}{{cos}^{2}⁡t}({cos}^{3}⁡t+\frac{{cos}^{2}⁡t}{{sin}^{2}⁡t})\text{d}t.
$$

Therefore,

$$
\begin{aligned}\int \frac{{cos}^{3}⁡t+{cot}^{2}⁡t}{{cos}^{2}⁡t}\,\text{d}t & =\int \frac{1}{{cos}^{2}⁡t}({cos}^{3}⁡t+\frac{{cos}^{2}⁡t}{{sin}^{2}⁡t})\text{d}t \\  & =\int (\frac{1}{{cos}^{2}⁡t}\cdot {cos}^{3}⁡t+\frac{1}{{cos}^{2}⁡t}\cdot \frac{{cos}^{2}⁡t}{{sin}^{2}⁡t})\text{d}t \\  & =\int (\operatorname{cos}⁡t+\frac{1}{{sin}^{2}⁡t})\text{d}t \\  & =\int (\operatorname{cos}⁡t+{csc}^{2}⁡t)\text{d}t \\  & =\operatorname{sin}⁡t-\operatorname{cot}⁡t+C.\end{aligned}
$$

Multiplying this result by $1/2$ and substituting back $t=2x$, we obtain

$$
\int \frac{\cos^{3}{\left(2 x \right)} + \cot^{2}{\left(2 x \right)}}{\cos^{2}{\left(2 x \right)}}\,\text{d}x=C + \frac{\sin{\left(2 x \right)}}{2} - \frac{\cot{\left(2 x \right)}}{2}.
$$

## q-49275

Source

Calculate $\int \frac{{tan}^{2}⁡x}{8{sin}^{2}⁡x}\,\text{d}x.$

['\\frac{1}{8}\\operatorname{tan}\u2061x\\operatorname{sec}\u2061x+C', '\\frac{1}{8}{tan}^{2}\u2061x{sec}^{2}\u2061x+C', '\\frac{1}{8}{tan}^{2}\u2061x+C', '\\frac{1}{8}{csc}^{2}\u2061x+C', '\\frac{1}{8}\\operatorname{tan}\u2061x+C']

We can write the integral as

$$
\int \frac{{tan}^{2}⁡x}{8{sin}^{2}⁡x}\,\text{d}x=\frac{1}{8}\int {tan}^{2}⁡x\cdot \frac{1}{{sin}^{2}⁡x}\,\text{d}x.
$$

We then use the fact that $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}$ and $\operatorname{sec}⁡x=\frac{1}{\operatorname{cos}⁡x}.$ Therefore,

$$
\begin{aligned}\begin{aligned}\int \frac{{tan}^{2}⁡x}{8{sin}^{2}⁡x}\,\text{d}x & =\frac{1}{8}\int {tan}^{2}⁡x\cdot \frac{1}{{sin}^{2}⁡x}\,\text{d}x \\  & =\frac{1}{8}\int {(\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x})}^{2}\cdot \frac{1}{{sin}^{2}⁡x}\,\text{d}x \\  & =\frac{1}{8}\int \frac{{sin}^{2}⁡x}{{cos}^{2}⁡x}\cdot \frac{1}{{sin}^{2}⁡x}\,\text{d}x \\  & =\frac{1}{8}\int \frac{1}{{cos}^{2}⁡x}\,\text{d}x \\  & =\frac{1}{8}\int {(\frac{1}{\operatorname{cos}⁡x})}^{2}\text{d}x \\  & =\frac{1}{8}\int {sec}^{2}⁡x\,\text{d}x \\  & =\frac{1}{8}\operatorname{tan}⁡x+C.\end{aligned}\end{aligned}
$$

Variant

Calculate $\int \frac{\tan^{2}{\left(2 x \right)}}{8 \sin^{2}{\left(2 x \right)}}\,\text{d}x.$

['C + \\frac{\\tan{\\left(2 x \\right)} \\sec{\\left(2 x \\right)}}{16}', 'C + \\frac{\\tan^{2}{\\left(2 x \\right)} \\sec^{2}{\\left(2 x \\right)}}{16}', 'C + \\frac{\\tan^{2}{\\left(2 x \\right)}}{16}', 'C + \\frac{\\csc^{2}{\\left(2 x \\right)}}{16}', 'C + \\frac{\\tan{\\left(2 x \\right)}}{16}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can write the integral as

$$
\int \frac{{tan}^{2}⁡t}{8{sin}^{2}⁡t}\,\text{d}t=\frac{1}{8}\int {tan}^{2}⁡t\cdot \frac{1}{{sin}^{2}⁡t}\,\text{d}t.
$$

We then use the fact that $\operatorname{tan}⁡t=\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}$ and $\operatorname{sec}⁡t=\frac{1}{\operatorname{cos}⁡t}.$ Therefore,

$$
\begin{aligned}\begin{aligned}\int \frac{{tan}^{2}⁡t}{8{sin}^{2}⁡t}\,\text{d}t & =\frac{1}{8}\int {tan}^{2}⁡t\cdot \frac{1}{{sin}^{2}⁡t}\,\text{d}t \\  & =\frac{1}{8}\int {(\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t})}^{2}\cdot \frac{1}{{sin}^{2}⁡t}\,\text{d}t \\  & =\frac{1}{8}\int \frac{{sin}^{2}⁡t}{{cos}^{2}⁡t}\cdot \frac{1}{{sin}^{2}⁡t}\,\text{d}t \\  & =\frac{1}{8}\int \frac{1}{{cos}^{2}⁡t}\,\text{d}t \\  & =\frac{1}{8}\int {(\frac{1}{\operatorname{cos}⁡t})}^{2}\text{d}t \\  & =\frac{1}{8}\int {sec}^{2}⁡t\,\text{d}t \\  & =\frac{1}{8}\operatorname{tan}⁡t+C.\end{aligned}\end{aligned}
$$

Multiplying this result by $1/2$ and substituting back $t=2x$, we obtain

$$
\int \frac{\tan^{2}{\left(2 x \right)}}{8 \sin^{2}{\left(2 x \right)}}\,\text{d}x=C + \frac{\tan{\left(2 x \right)}}{16}.
$$

## q-114306

Source

${\int }_{0}^{\pi /4}\frac{3\operatorname{sec}⁡x\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x=$

['3(\\sqrt{2}-1)', '3(\\sqrt{2}-2)', '\\sqrt{2}-3', '3(\\sqrt{2}+1)', '\\sqrt{2}+1']

We can write the integral as

$$
{\int }_{0}^{\pi /4}\frac{3\operatorname{sec}⁡x\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x=3{\int }_{0}^{\pi /4}\operatorname{sec}⁡x\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x
$$

Then, we use the fact that $\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}=\operatorname{tan}⁡x,$ as follows:

$$
\begin{aligned}3{\int }_{0}^{\pi /4}\operatorname{sec}⁡x\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x & =3{\int }_{0}^{\pi /4}\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x\end{aligned}
$$

Therefore,

$$
\begin{aligned}{\int }_{0}^{\pi /4}\frac{3\operatorname{sec}⁡x\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x & =3{\int }_{0}^{\pi /4}\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x \\  & =3\operatorname{sec}⁡x\,{|}_{0}^{\pi /4} \\  & =3[\operatorname{sec}⁡(\frac{\pi }{4})-\operatorname{sec}⁡0] \\  & =3(\sqrt{2}-1)\end{aligned}
$$

Variant

$\int_{0}^{\frac{\pi}{8}} \frac{3 \sin{\left(2 x \right)} \sec{\left(2 x \right)}}{\cos{\left(2 x \right)}}\,\text{d}x=$

['- \\frac{3}{2} + \\frac{3 \\sqrt{2}}{2}', '-3 + \\frac{3 \\sqrt{2}}{2}', '- \\frac{3}{2} + \\frac{\\sqrt{2}}{2}', '\\frac{3}{2} + \\frac{3 \\sqrt{2}}{2}', '\\frac{1}{2} + \\frac{\\sqrt{2}}{2}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. The limits become $t=0$ and $t=\frac{\pi}{4}$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can write the integral as

$$
{\int }_{0}^{\pi /4}\frac{3\operatorname{sec}⁡t\operatorname{sin}⁡t}{\operatorname{cos}⁡t}\,\text{d}t=3{\int }_{0}^{\pi /4}\operatorname{sec}⁡t\cdot \frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}\,\text{d}t
$$

Then, we use the fact that $\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}=\operatorname{tan}⁡t,$ as follows:

$$
\begin{aligned}3{\int }_{0}^{\pi /4}\operatorname{sec}⁡t\cdot \frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}\,\text{d}t & =3{\int }_{0}^{\pi /4}\operatorname{sec}⁡t\operatorname{tan}⁡t\,\text{d}t\end{aligned}
$$

Therefore,

$$
\begin{aligned}{\int }_{0}^{\pi /4}\frac{3\operatorname{sec}⁡t\operatorname{sin}⁡t}{\operatorname{cos}⁡t}\,\text{d}t & =3{\int }_{0}^{\pi /4}\operatorname{sec}⁡t\operatorname{tan}⁡t\,\text{d}t \\  & =3\operatorname{sec}⁡t\,{|}_{0}^{\pi /4} \\  & =3[\operatorname{sec}⁡(\frac{\pi }{4})-\operatorname{sec}⁡0] \\  & =3(\sqrt{2}-1)\end{aligned}
$$

Multiplying this result by $1/2$, we obtain

$$
\int_{0}^{\frac{\pi}{8}} \frac{3 \sin{\left(2 x \right)} \sec{\left(2 x \right)}}{\cos{\left(2 x \right)}}\,\text{d}x=- \frac{3}{2} + \frac{3 \sqrt{2}}{2}.
$$

## q-114313

Source

$\int \frac{\operatorname{sin}⁡x-\operatorname{csc}⁡x}{\operatorname{tan}⁡x}\,\text{d}x=$

['\\operatorname{cos}\u2061x-\\operatorname{csc}\u2061x+C', '\\operatorname{sin}\u2061x+\\operatorname{csc}\u2061x+C', '\\operatorname{csc}\u2061x+\\operatorname{sec}\u2061x+C', '\\operatorname{sin}\u2061x-\\operatorname{cot}\u2061x+C', '\\operatorname{csc}\u2061x-\\operatorname{cot}\u2061x+C']

We can write the integral as

$$
\int \frac{\operatorname{sin}⁡x-\operatorname{csc}⁡x}{\operatorname{tan}⁡x}\,\text{d}x=\int \frac{1}{\operatorname{tan}⁡x}(\operatorname{sin}⁡x-\operatorname{csc}⁡x)\text{d}x.
$$

We then use the fact that $\frac{1}{\operatorname{tan}⁡x}=\operatorname{cot}⁡x=\frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}$ to express this as

$$
\begin{aligned}\int \operatorname{cot}⁡x(\operatorname{sin}⁡x-\operatorname{csc}⁡x)\text{d}x & =\int (\operatorname{cot}⁡x\operatorname{sin}⁡x-\operatorname{cot}⁡x\cdot \operatorname{csc}⁡x)\text{d}x \\  & =\int (\frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}\cdot \operatorname{sin}⁡x-\operatorname{cot}⁡x\cdot \operatorname{csc}⁡x)\text{d}x \\  & =\int (\operatorname{cos}⁡x-\operatorname{csc}⁡x\operatorname{cot}⁡x)\text{d}x.\end{aligned}
$$

Therefore,

$$
\begin{aligned}\int \frac{\operatorname{sin}⁡x-\operatorname{csc}⁡x}{\operatorname{tan}⁡x}\,\text{d}x & =\int (\operatorname{cos}⁡x-\operatorname{csc}⁡x\operatorname{cot}⁡x)\text{d}x \\  & =\operatorname{sin}⁡x-(-\operatorname{csc}⁡x)+C \\  & =\operatorname{sin}⁡x+\operatorname{csc}⁡x+C.\end{aligned}
$$

Variant

$\int \frac{\sin{\left(2 x \right)} - \csc{\left(2 x \right)}}{\tan{\left(2 x \right)}}\,\text{d}x=$

['C + \\frac{\\cos{\\left(2 x \\right)}}{2} - \\frac{\\csc{\\left(2 x \\right)}}{2}', 'C + \\frac{\\sin{\\left(2 x \\right)}}{2} + \\frac{\\csc{\\left(2 x \\right)}}{2}', 'C + \\frac{\\csc{\\left(2 x \\right)}}{2} + \\frac{\\sec{\\left(2 x \\right)}}{2}', 'C + \\frac{\\sin{\\left(2 x \\right)}}{2} - \\frac{\\cot{\\left(2 x \\right)}}{2}', 'C - \\frac{\\cot{\\left(2 x \\right)}}{2} + \\frac{\\csc{\\left(2 x \\right)}}{2}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can write the integral as

$$
\int \frac{\operatorname{sin}⁡t-\operatorname{csc}⁡t}{\operatorname{tan}⁡t}\,\text{d}t=\int \frac{1}{\operatorname{tan}⁡t}(\operatorname{sin}⁡t-\operatorname{csc}⁡t)\text{d}t.
$$

We then use the fact that $\frac{1}{\operatorname{tan}⁡t}=\operatorname{cot}⁡t=\frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t}$ to express this as

$$
\begin{aligned}\int \operatorname{cot}⁡t(\operatorname{sin}⁡t-\operatorname{csc}⁡t)\text{d}t & =\int (\operatorname{cot}⁡t\operatorname{sin}⁡t-\operatorname{cot}⁡t\cdot \operatorname{csc}⁡t)\text{d}t \\  & =\int (\frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t}\cdot \operatorname{sin}⁡t-\operatorname{cot}⁡t\cdot \operatorname{csc}⁡t)\text{d}t \\  & =\int (\operatorname{cos}⁡t-\operatorname{csc}⁡t\operatorname{cot}⁡t)\text{d}t.\end{aligned}
$$

Therefore,

$$
\begin{aligned}\int \frac{\operatorname{sin}⁡t-\operatorname{csc}⁡t}{\operatorname{tan}⁡t}\,\text{d}t & =\int (\operatorname{cos}⁡t-\operatorname{csc}⁡t\operatorname{cot}⁡t)\text{d}t \\  & =\operatorname{sin}⁡t-(-\operatorname{csc}⁡t)+C \\  & =\operatorname{sin}⁡t+\operatorname{csc}⁡t+C.\end{aligned}
$$

Multiplying this result by $1/2$ and substituting back $t=2x$, we obtain

$$
\int \frac{\sin{\left(2 x \right)} - \csc{\left(2 x \right)}}{\tan{\left(2 x \right)}}\,\text{d}x=C + \frac{\sin{\left(2 x \right)}}{2} + \frac{\csc{\left(2 x \right)}}{2}.
$$

## q-114318

Source

${\int }_{\pi /4}^{\pi /2}\frac{\operatorname{cos}⁡x}{{sin}^{2}⁡x}\,\text{d}x=$

['\\sqrt{2}-1', '3\\sqrt{2}-2', '2\\sqrt{2}', '\\frac{\\sqrt{2}+1}{2}', '\\frac{\\sqrt{2}-2}{3}']

We can write the integral as

$$
{\int }_{\pi /4}^{\pi /2}\frac{\operatorname{cos}⁡x}{{sin}^{2}⁡x}\,\text{d}x={\int }_{\pi /4}^{\pi /2}\frac{1}{\operatorname{sin}⁡x}\cdot \frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}\,\text{d}x.
$$

We then use the fact that $\frac{1}{\operatorname{sin}⁡x}=\operatorname{csc}⁡x$ and $\frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}=\operatorname{cot}⁡x$ to express this as

$$
{\int }_{\pi /4}^{\pi /2}\operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}{\int }_{\pi /4}^{\pi /2}\frac{1}{\operatorname{sin}⁡x}\cdot \frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}\,\text{d}x & ={\int }_{\pi /4}^{\pi /2}\operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & =-\operatorname{csc}⁡x\,{|}_{\pi /4}^{\pi /2} \\  & =-[\operatorname{csc}⁡(\frac{\pi }{2})-\operatorname{csc}⁡(\frac{\pi }{4})] \\  & =-[1-\sqrt{2}] \\  & =\sqrt{2}-1.\end{aligned}
$$

Variant

$\int_{\frac{\pi}{8}}^{\frac{\pi}{4}} \frac{\cos{\left(2 x \right)}}{\sin^{2}{\left(2 x \right)}}\,\text{d}x=$

['- \\frac{1}{2} + \\frac{\\sqrt{2}}{2}', '-1 + \\frac{3 \\sqrt{2}}{2}', '\\sqrt{2}', '\\frac{1}{4} + \\frac{\\sqrt{2}}{4}', '- \\frac{1}{3} + \\frac{\\sqrt{2}}{6}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. The limits become $t=\frac{\pi}{4}$ and $t=\frac{\pi}{2}$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can write the integral as

$$
{\int }_{\pi /4}^{\pi /2}\frac{\operatorname{cos}⁡t}{{sin}^{2}⁡t}\,\text{d}t={\int }_{\pi /4}^{\pi /2}\frac{1}{\operatorname{sin}⁡t}\cdot \frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t}\,\text{d}t.
$$

We then use the fact that $\frac{1}{\operatorname{sin}⁡t}=\operatorname{csc}⁡t$ and $\frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t}=\operatorname{cot}⁡t$ to express this as

$$
{\int }_{\pi /4}^{\pi /2}\operatorname{csc}⁡t\operatorname{cot}⁡t\,\text{d}t.
$$

Therefore,

$$
\begin{aligned}{\int }_{\pi /4}^{\pi /2}\frac{1}{\operatorname{sin}⁡t}\cdot \frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t}\,\text{d}t & ={\int }_{\pi /4}^{\pi /2}\operatorname{csc}⁡t\operatorname{cot}⁡t\,\text{d}t \\  & =-\operatorname{csc}⁡t\,{|}_{\pi /4}^{\pi /2} \\  & =-[\operatorname{csc}⁡(\frac{\pi }{2})-\operatorname{csc}⁡(\frac{\pi }{4})] \\  & =-[1-\sqrt{2}] \\  & =\sqrt{2}-1.\end{aligned}
$$

Multiplying this result by $1/2$, we obtain

$$
\int_{\frac{\pi}{8}}^{\frac{\pi}{4}} \frac{\cos{\left(2 x \right)}}{\sin^{2}{\left(2 x \right)}}\,\text{d}x=- \frac{1}{2} + \frac{\sqrt{2}}{2}.
$$

## q-352848

Source

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x=$
{{field-1}}

['\\frac{\\sqrt{3}}{3}']

We use the identities $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}$  and  $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x,$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\text{d}x & ={\int }_{0}^{\pi /6}(1-{tan}^{2}⁡x)\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x \\  & ={\int }_{0}^{\pi /6}(1-\frac{{sin}^{2}⁡x}{{cos}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x \\  & ={\int }_{0}^{\pi /6}(\frac{{cos}^{2}⁡x-{sin}^{2}⁡x}{{cos}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x \\  & ={\int }_{0}^{\pi /6}\frac{1}{{cos}^{2}⁡x}\,\text{d}x \\  & ={\int }_{0}^{\pi /6}{sec}^{2}⁡x\,\text{d}x \\  & =\operatorname{tan}⁡x{|}_{0}^{\pi /6} \\  & =\operatorname{tan}⁡(\frac{\pi }{6})-\operatorname{tan}⁡0 \\  & =\frac{\sqrt{3}}{3}-0 \\  & =\frac{\sqrt{3}}{3}\end{aligned}
$$

Variant

Evaluate the following integral. Do not round the answer.

$\int_{0}^{\frac{\pi}{12}} \frac{1 - \tan^{2}{\left(2 x \right)}}{- \sin^{2}{\left(2 x \right)} + \cos^{2}{\left(2 x \right)}}\,\text{d}x=$
{{field-1}}

['\\frac{\\sqrt{3}}{6}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. The limits become $t=0$ and $t=\frac{\pi}{6}$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We use the identities $\operatorname{tan}⁡t=\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}$  and  $\frac{1}{\operatorname{cos}⁡t}=\operatorname{sec}⁡t,$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡t}{{cos}^{2}⁡t-{sin}^{2}⁡t}\text{d}t & ={\int }_{0}^{\pi /6}(1-{tan}^{2}⁡t)\cdot \frac{1}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi /6}(1-\frac{{sin}^{2}⁡t}{{cos}^{2}⁡t})\cdot \frac{1}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi /6}(\frac{{cos}^{2}⁡t-{sin}^{2}⁡t}{{cos}^{2}⁡t})\cdot \frac{1}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi /6}\frac{1}{{cos}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi /6}{sec}^{2}⁡t\,\text{d}t \\  & =\operatorname{tan}⁡t{|}_{0}^{\pi /6} \\  & =\operatorname{tan}⁡(\frac{\pi }{6})-\operatorname{tan}⁡0 \\  & =\frac{\sqrt{3}}{3}-0 \\  & =\frac{\sqrt{3}}{3}\end{aligned}
$$

Multiplying this result by $1/2$, we obtain

$$
\int_{0}^{\frac{\pi}{12}} \frac{1 - \tan^{2}{\left(2 x \right)}}{- \sin^{2}{\left(2 x \right)} + \cos^{2}{\left(2 x \right)}}\,\text{d}x=\frac{\sqrt{3}}{6}.
$$

## q-352853

Source

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /3}\frac{1+\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\,\text{d}x=$
{{field-1}}

['\\frac{1}{2}+\\frac{\\sqrt{3}}{2}']

We use the identities $\frac{1}{\operatorname{sec}⁡x}=\operatorname{cos}⁡x$  and  $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x},$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /3}\frac{1+\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\text{d}x & ={\int }_{0}^{\pi /3}\frac{1}{\operatorname{sec}⁡x}\cdot (1+\operatorname{tan}⁡x)\,\text{d}x \\  & ={\int }_{0}^{\pi /3}\operatorname{cos}⁡x(1+\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x})\,\text{d}x \\  & ={\int }_{0}^{\pi /3}(\operatorname{cos}⁡x+\operatorname{sin}⁡x)\,\text{d}x \\  & =(\operatorname{sin}⁡x-\operatorname{cos}⁡x){|}_{0}^{\pi /3} \\  & =(\frac{\sqrt{3}}{2}-\frac{1}{2})-(0-1) \\  & =\frac{1}{2}+\frac{\sqrt{3}}{2}\end{aligned}
$$

Variant

Evaluate the following integral. Do not round the answer.

$\int_{0}^{\frac{\pi}{6}} \frac{\tan{\left(2 x \right)} + 1}{\sec{\left(2 x \right)}}\,\text{d}x=$
{{field-1}}

['\\frac{1}{4} + \\frac{\\sqrt{3}}{4}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. The limits become $t=0$ and $t=\frac{\pi}{3}$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We use the identities $\frac{1}{\operatorname{sec}⁡t}=\operatorname{cos}⁡t$  and  $\operatorname{tan}⁡t=\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t},$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /3}\frac{1+\operatorname{tan}⁡t}{\operatorname{sec}⁡t}\text{d}t & ={\int }_{0}^{\pi /3}\frac{1}{\operatorname{sec}⁡t}\cdot (1+\operatorname{tan}⁡t)\,\text{d}t \\  & ={\int }_{0}^{\pi /3}\operatorname{cos}⁡t(1+\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t})\,\text{d}t \\  & ={\int }_{0}^{\pi /3}(\operatorname{cos}⁡t+\operatorname{sin}⁡t)\,\text{d}t \\  & =(\operatorname{sin}⁡t-\operatorname{cos}⁡t){|}_{0}^{\pi /3} \\  & =(\frac{\sqrt{3}}{2}-\frac{1}{2})-(0-1) \\  & =\frac{1}{2}+\frac{\sqrt{3}}{2}\end{aligned}
$$

Multiplying this result by $1/2$, we obtain

$$
\int_{0}^{\frac{\pi}{6}} \frac{\tan{\left(2 x \right)} + 1}{\sec{\left(2 x \right)}}\,\text{d}x=\frac{1}{4} + \frac{\sqrt{3}}{4}.
$$

## q-352858

Source

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /8}\frac{\operatorname{cot}⁡4x}{\operatorname{csc}⁡4x}\,\text{d}x=$
{{field-1}}

['\\frac{1}{4}']

We can write the integral as

$$
{\int }_{0}^{\pi /8}\frac{\operatorname{cot}⁡4x}{\operatorname{csc}⁡4x}\,\text{d}x={\int }_{0}^{\pi /8}\operatorname{cot}⁡4x\cdot \frac{1}{\operatorname{csc}⁡4x}\,\text{d}x.
$$

Then, we use the fact that $\operatorname{cot}⁡4x=\frac{\operatorname{cos}⁡4x}{\operatorname{sin}⁡4x}$ and $\frac{1}{\operatorname{csc}⁡4x}=\operatorname{sin}⁡4x$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /8}\frac{\operatorname{cos}⁡4x}{\operatorname{sin}⁡4x}\cdot \operatorname{sin}⁡4x\,\text{d}x & ={\int }_{0}^{\pi /8}\operatorname{cos}⁡4x\,\text{d}x\end{aligned}
$$

We can solve this by substitution. Let $u=4x.$ Then $\text{d}x=\frac{1}{4}\text{d}u.$ 

Now, we fill the table for the limits of integration, according to the rule $u=4x.$

| $x$ | $0$ | $\frac{\pi }{8}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi }{2}$ |

Therefore, the integral in terms of the new variable is

$$
\begin{aligned}\begin{aligned}{\int }_{0}^{\pi /8}\operatorname{cos}⁡4x\,\text{d}x & ={\int }_{0}^{\pi /2}\operatorname{cos}⁡u\cdot \frac{1}{4}\text{d}u \\  & =\frac{1}{4}{\int }_{0}^{\pi /2}\operatorname{cos}⁡u\text{d}u \\  & =\frac{1}{4}\operatorname{sin}⁡u{|}_{0}^{\pi /2} \\  & =\frac{1}{4}(sin\,(\frac{\pi }{2})-sin\,(0)) \\  & =\frac{1}{4}(1-0) \\  & =\frac{1}{4}.\end{aligned}\end{aligned}
$$

Variant

Evaluate the following integral. Do not round the answer.

$\int_{0}^{\frac{\pi}{16}} \frac{\cot{\left(8 x \right)}}{\csc{\left(8 x \right)}}\,\text{d}x=$
{{field-1}}

['\\frac{1}{8}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. The limits become $t=0$ and $t=\frac{\pi}{8}$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can write the integral as

$$
{\int }_{0}^{\pi /8}\frac{\operatorname{cot}⁡4t}{\operatorname{csc}⁡4t}\,\text{d}t={\int }_{0}^{\pi /8}\operatorname{cot}⁡4t\cdot \frac{1}{\operatorname{csc}⁡4t}\,\text{d}t.
$$

Then, we use the fact that $\operatorname{cot}⁡4t=\frac{\operatorname{cos}⁡4t}{\operatorname{sin}⁡4t}$ and $\frac{1}{\operatorname{csc}⁡4t}=\operatorname{sin}⁡4t$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /8}\frac{\operatorname{cos}⁡4t}{\operatorname{sin}⁡4t}\cdot \operatorname{sin}⁡4t\,\text{d}t & ={\int }_{0}^{\pi /8}\operatorname{cos}⁡4t\,\text{d}t\end{aligned}
$$

We can solve this by substitution. Let $u=4t.$ Then $\text{d}t=\frac{1}{4}\text{d}u.$ 

Now, we fill the table for the limits of integration, according to the rule $u=4t.$

| $t$ | $0$ | $\frac{\pi }{8}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi }{2}$ |

Therefore, the integral in terms of the new variable is

$$
\begin{aligned}\begin{aligned}{\int }_{0}^{\pi /8}\operatorname{cos}⁡4t\,\text{d}t & ={\int }_{0}^{\pi /2}\operatorname{cos}⁡u\cdot \frac{1}{4}\text{d}u \\  & =\frac{1}{4}{\int }_{0}^{\pi /2}\operatorname{cos}⁡u\text{d}u \\  & =\frac{1}{4}\operatorname{sin}⁡u{|}_{0}^{\pi /2} \\  & =\frac{1}{4}(sin\,(\frac{\pi }{2})-sin\,(0)) \\  & =\frac{1}{4}(1-0) \\  & =\frac{1}{4}.\end{aligned}\end{aligned}
$$

Multiplying this result by $1/2$, we obtain

$$
\int_{0}^{\frac{\pi}{16}} \frac{\cot{\left(8 x \right)}}{\csc{\left(8 x \right)}}\,\text{d}x=\frac{1}{8}.
$$

At the lower endpoint the quotient is interpreted by its continuous limit.

## q-352867

Source

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /10}\frac{\operatorname{cot}⁡5x}{\operatorname{csc}⁡5x}\,\text{d}x=$
{{field-1}}

['\\frac{1}{5}']

We can rewrite the integral as

$$
{\int }_{0}^{\pi /10}\frac{\operatorname{cot}⁡5x}{\operatorname{csc}⁡5x}\,\text{d}x={\int }_{0}^{\pi /10}\operatorname{cot}⁡5x\cdot \frac{1}{\operatorname{csc}⁡5x}\,\text{d}x.
$$

Then, we use the fact that $\operatorname{cot}⁡5x=\frac{\operatorname{cos}⁡5x}{\operatorname{sin}⁡5x}$ and $\frac{1}{\operatorname{csc}⁡5x}=\operatorname{sin}⁡5x$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /10}\frac{\operatorname{cos}⁡5x}{\operatorname{sin}⁡5x}\cdot \operatorname{sin}⁡5x\,\text{d}x & ={\int }_{0}^{\pi /10}\operatorname{cos}⁡5x\,\text{d}x\end{aligned}
$$

We can solve this by substitution. Let $u=5x.$ Then $\text{d}x=\frac{1}{5}\text{d}u.$

Now, we fill the table for the limits of integration, according to the rule $u=5x.$

| $x$ | $0$ | $\frac{\pi }{10}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi }{2}$ |

Therefore, the integral in terms of the new variable is

$$
\begin{aligned}{\int }_{0}^{\pi /10}\operatorname{cos}⁡5x\,\text{d}x & ={\int }_{0}^{\pi /2}\operatorname{cos}⁡u\cdot \frac{1}{5}\,\text{d}u \\  & =\frac{1}{5}{\int }_{0}^{\pi /2}\operatorname{cos}⁡u\,\text{d}u \\  & =\frac{1}{5}\operatorname{sin}⁡u{|}_{0}^{\pi /2} \\  & =\frac{1}{5}(sin\,(\frac{\pi }{2})-\operatorname{sin}⁡(0)) \\  & =\frac{1}{5}(1-0) \\  & =\frac{1}{5}.\end{aligned}
$$

Variant

Evaluate the following integral. Do not round the answer.

$\int_{0}^{\frac{\pi}{20}} \frac{\cot{\left(10 x \right)}}{\csc{\left(10 x \right)}}\,\text{d}x=$
{{field-1}}

['\\frac{1}{10}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. The limits become $t=0$ and $t=\frac{\pi}{10}$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can rewrite the integral as

$$
{\int }_{0}^{\pi /10}\frac{\operatorname{cot}⁡5t}{\operatorname{csc}⁡5t}\,\text{d}t={\int }_{0}^{\pi /10}\operatorname{cot}⁡5t\cdot \frac{1}{\operatorname{csc}⁡5t}\,\text{d}t.
$$

Then, we use the fact that $\operatorname{cot}⁡5t=\frac{\operatorname{cos}⁡5t}{\operatorname{sin}⁡5t}$ and $\frac{1}{\operatorname{csc}⁡5t}=\operatorname{sin}⁡5t$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /10}\frac{\operatorname{cos}⁡5t}{\operatorname{sin}⁡5t}\cdot \operatorname{sin}⁡5t\,\text{d}t & ={\int }_{0}^{\pi /10}\operatorname{cos}⁡5t\,\text{d}t\end{aligned}
$$

We can solve this by substitution. Let $u=5t.$ Then $\text{d}t=\frac{1}{5}\text{d}u.$

Now, we fill the table for the limits of integration, according to the rule $u=5t.$

| $t$ | $0$ | $\frac{\pi }{10}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi }{2}$ |

Therefore, the integral in terms of the new variable is

$$
\begin{aligned}{\int }_{0}^{\pi /10}\operatorname{cos}⁡5t\,\text{d}t & ={\int }_{0}^{\pi /2}\operatorname{cos}⁡u\cdot \frac{1}{5}\,\text{d}u \\  & =\frac{1}{5}{\int }_{0}^{\pi /2}\operatorname{cos}⁡u\,\text{d}u \\  & =\frac{1}{5}\operatorname{sin}⁡u{|}_{0}^{\pi /2} \\  & =\frac{1}{5}(sin\,(\frac{\pi }{2})-\operatorname{sin}⁡(0)) \\  & =\frac{1}{5}(1-0) \\  & =\frac{1}{5}.\end{aligned}
$$

Multiplying this result by $1/2$, we obtain

$$
\int_{0}^{\frac{\pi}{20}} \frac{\cot{\left(10 x \right)}}{\csc{\left(10 x \right)}}\,\text{d}x=\frac{1}{10}.
$$

At the lower endpoint the quotient is interpreted by its continuous limit.

## q-352868

Source

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /12}\frac{\operatorname{tan}⁡4x}{\operatorname{sec}⁡4x}\,\text{d}x=$
{{field-1}}

['\\frac{1}{8}']

We can rewrite the integral as

$$
{\int }_{0}^{\pi /12}\frac{\operatorname{tan}⁡4x}{\operatorname{sec}⁡4x}\,\text{d}x={\int }_{0}^{\pi /12}\operatorname{tan}⁡4x\cdot \frac{1}{\operatorname{sec}⁡4x}\,\text{d}x.
$$

Then, we use the fact that $\operatorname{tan}⁡4x=\frac{\operatorname{sin}⁡4x}{\operatorname{cos}⁡4x}$ and $\frac{1}{\operatorname{sec}⁡4x}=\operatorname{cos}⁡4x$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /12}\frac{\operatorname{sin}⁡4x}{\operatorname{cos}⁡4x}\cdot \operatorname{cos}⁡4x\,\text{d}x & ={\int }_{0}^{\pi /12}\operatorname{sin}⁡4x\,\text{d}x\end{aligned}
$$

We can solve this by substitution. Let $u=4x.$ Then $\text{d}x=\frac{1}{4}\text{d}u.$

Now, we fill the table for the limits of integration, according to the rule $u=4x.$

| $x$ | $0$ | $\frac{\pi }{12}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi }{3}$ |

Therefore, the integral in terms of the new variable is

$$
\begin{aligned}{\int }_{0}^{\pi /12}\operatorname{sin}⁡4x\,\text{d}x & ={\int }_{0}^{\pi /3}\operatorname{sin}⁡u\cdot \frac{1}{4}\,\text{d}u \\  & =\frac{1}{4}{\int }_{0}^{\pi /3}\operatorname{sin}⁡u\,\text{d}u \\  & =-\frac{1}{4}\operatorname{cos}⁡u{|}_{0}^{\pi /3} \\  & =-\frac{1}{4}(cos\,(\frac{\pi }{3})-\operatorname{cos}⁡(0)) \\  & =-\frac{1}{4}(\frac{1}{2}-1) \\  & =\frac{1}{8}.\end{aligned}
$$

Variant

Evaluate the following integral. Do not round the answer.

$\int_{0}^{\frac{\pi}{24}} \frac{\tan{\left(8 x \right)}}{\sec{\left(8 x \right)}}\,\text{d}x=$
{{field-1}}

['\\frac{1}{16}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. The limits become $t=0$ and $t=\frac{\pi}{12}$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can rewrite the integral as

$$
{\int }_{0}^{\pi /12}\frac{\operatorname{tan}⁡4t}{\operatorname{sec}⁡4t}\,\text{d}t={\int }_{0}^{\pi /12}\operatorname{tan}⁡4t\cdot \frac{1}{\operatorname{sec}⁡4t}\,\text{d}t.
$$

Then, we use the fact that $\operatorname{tan}⁡4t=\frac{\operatorname{sin}⁡4t}{\operatorname{cos}⁡4t}$ and $\frac{1}{\operatorname{sec}⁡4t}=\operatorname{cos}⁡4t$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /12}\frac{\operatorname{sin}⁡4t}{\operatorname{cos}⁡4t}\cdot \operatorname{cos}⁡4t\,\text{d}t & ={\int }_{0}^{\pi /12}\operatorname{sin}⁡4t\,\text{d}t\end{aligned}
$$

We can solve this by substitution. Let $u=4t.$ Then $\text{d}t=\frac{1}{4}\text{d}u.$

Now, we fill the table for the limits of integration, according to the rule $u=4t.$

| $t$ | $0$ | $\frac{\pi }{12}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi }{3}$ |

Therefore, the integral in terms of the new variable is

$$
\begin{aligned}{\int }_{0}^{\pi /12}\operatorname{sin}⁡4t\,\text{d}t & ={\int }_{0}^{\pi /3}\operatorname{sin}⁡u\cdot \frac{1}{4}\,\text{d}u \\  & =\frac{1}{4}{\int }_{0}^{\pi /3}\operatorname{sin}⁡u\,\text{d}u \\  & =-\frac{1}{4}\operatorname{cos}⁡u{|}_{0}^{\pi /3} \\  & =-\frac{1}{4}(cos\,(\frac{\pi }{3})-\operatorname{cos}⁡(0)) \\  & =-\frac{1}{4}(\frac{1}{2}-1) \\  & =\frac{1}{8}.\end{aligned}
$$

Multiplying this result by $1/2$, we obtain

$$
\int_{0}^{\frac{\pi}{24}} \frac{\tan{\left(8 x \right)}}{\sec{\left(8 x \right)}}\,\text{d}x=\frac{1}{16}.
$$

## q-49284

Source

Evaluate ${\int }_{0}^{\pi /4}\frac{\operatorname{sin}⁡x}{{cos}^{2}⁡x}\,\text{d}x.$

['\\sqrt{2}-1', '\\frac{\\sqrt{2}}{2}-1', '2\\sqrt{2}-1', '\\frac{\\sqrt{2}}{2}', '\\sqrt{2}']

We can write the integral as

$$
{\int }_{0}^{\pi /4}\frac{\operatorname{sin}⁡x}{{cos}^{2}⁡x}\text{d}x={\int }_{0}^{\pi /4}\frac{1}{\operatorname{cos}⁡x}\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x
$$

We use the fact that $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x$ and $\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}=\operatorname{tan}⁡x$ to express this as

$$
{\int }_{0}^{\pi /4}\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\begin{aligned}{\int }_{0}^{\pi /4}\frac{\operatorname{sin}⁡x}{{cos}^{2}⁡x}\text{d}x & ={\int }_{0}^{\pi /4}\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x \\  & =\operatorname{sec}⁡x{|}_{0}^{\pi /4} \\  & =(\operatorname{sec}⁡(\frac{\pi }{4})-\operatorname{sec}⁡(0)) \\  & =\sqrt{2}-1.\end{aligned}\end{aligned}
$$

Variant

Evaluate $\int_{0}^{\frac{\pi}{8}} \frac{\sin{\left(2 x \right)}}{\cos^{2}{\left(2 x \right)}}\,\text{d}x.$

['- \\frac{1}{2} + \\frac{\\sqrt{2}}{2}', '- \\frac{1}{2} + \\frac{\\sqrt{2}}{4}', '- \\frac{1}{2} + \\sqrt{2}', '\\frac{\\sqrt{2}}{4}', '\\frac{\\sqrt{2}}{2}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. The limits become $t=0$ and $t=\frac{\pi}{4}$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can write the integral as

$$
{\int }_{0}^{\pi /4}\frac{\operatorname{sin}⁡t}{{cos}^{2}⁡t}\text{d}t={\int }_{0}^{\pi /4}\frac{1}{\operatorname{cos}⁡t}\cdot \frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}\,\text{d}t
$$

We use the fact that $\frac{1}{\operatorname{cos}⁡t}=\operatorname{sec}⁡t$ and $\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}=\operatorname{tan}⁡t$ to express this as

$$
{\int }_{0}^{\pi /4}\operatorname{sec}⁡t\operatorname{tan}⁡t\,\text{d}t.
$$

Therefore,

$$
\begin{aligned}\begin{aligned}{\int }_{0}^{\pi /4}\frac{\operatorname{sin}⁡t}{{cos}^{2}⁡t}\text{d}t & ={\int }_{0}^{\pi /4}\operatorname{sec}⁡t\operatorname{tan}⁡t\,\text{d}t \\  & =\operatorname{sec}⁡t{|}_{0}^{\pi /4} \\  & =(\operatorname{sec}⁡(\frac{\pi }{4})-\operatorname{sec}⁡(0)) \\  & =\sqrt{2}-1.\end{aligned}\end{aligned}
$$

Multiplying this result by $1/2$, we obtain

$$
\int_{0}^{\frac{\pi}{8}} \frac{\sin{\left(2 x \right)}}{\cos^{2}{\left(2 x \right)}}\,\text{d}x=- \frac{1}{2} + \frac{\sqrt{2}}{2}.
$$

## q-73361

Source

Evaluate ${\int }_{0}^{\pi /4}\frac{1+\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\,\text{d}x.$

['\\sqrt{2}-2', '1', '0', '\\frac{1}{2}', '\\sqrt{2}']

We can write the integral as

$$
{\int }_{0}^{\pi /4}\frac{1+\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\text{d}x={\int }_{0}^{\pi /4}\frac{1}{\operatorname{sec}⁡x}\cdot (1+\operatorname{tan}⁡x)\,\text{d}x
$$

We then use the fact that $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x$ and $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}.$ Therefore,

$$
\begin{aligned}{\int }_{0}^{\pi /4}\frac{1}{\operatorname{sec}⁡x}\cdot (1+\operatorname{tan}⁡x)\,\text{d}x & ={\int }_{0}^{\pi /4}\operatorname{cos}⁡x\cdot (1+\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x})\,\text{d}x \\  & ={\int }_{0}^{\pi /4}(\operatorname{cos}⁡x+\operatorname{cos}⁡x\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x})\,\text{d}x \\  & ={\int }_{0}^{\pi /4}(\operatorname{cos}⁡x+\operatorname{sin}⁡x)\,\text{d}x \\  & =(\operatorname{sin}⁡x-\operatorname{cos}⁡x){|}_{0}^{\pi /4} \\  & (\operatorname{sin}⁡(\frac{\pi }{4})-\operatorname{cos}⁡(\frac{\pi }{4}))-(\operatorname{sin}⁡(0)-\operatorname{cos}⁡(0)) \\  & =(\frac{\sqrt{2}}{2}-\frac{\sqrt{2}}{2})-(0-1) \\  & =1.\end{aligned}
$$

Variant

Evaluate $\int_{0}^{\frac{\pi}{8}} \frac{\tan{\left(2 x \right)} + 1}{\sec{\left(2 x \right)}}\,\text{d}x.$

['-1 + \\frac{\\sqrt{2}}{2}', '\\frac{1}{2}', '0', '\\frac{1}{4}', '\\frac{\\sqrt{2}}{2}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. The limits become $t=0$ and $t=\frac{\pi}{4}$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can write the integral as

$$
{\int }_{0}^{\pi /4}\frac{1+\operatorname{tan}⁡t}{\operatorname{sec}⁡t}\text{d}t={\int }_{0}^{\pi /4}\frac{1}{\operatorname{sec}⁡t}\cdot (1+\operatorname{tan}⁡t)\,\text{d}t
$$

We then use the fact that $\frac{1}{\operatorname{cos}⁡t}=\operatorname{sec}⁡t$ and $\operatorname{tan}⁡t=\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}.$ Therefore,

$$
\begin{aligned}{\int }_{0}^{\pi /4}\frac{1}{\operatorname{sec}⁡t}\cdot (1+\operatorname{tan}⁡t)\,\text{d}t & ={\int }_{0}^{\pi /4}\operatorname{cos}⁡t\cdot (1+\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t})\,\text{d}t \\  & ={\int }_{0}^{\pi /4}(\operatorname{cos}⁡t+\operatorname{cos}⁡t\cdot \frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t})\,\text{d}t \\  & ={\int }_{0}^{\pi /4}(\operatorname{cos}⁡t+\operatorname{sin}⁡t)\,\text{d}t \\  & =(\operatorname{sin}⁡t-\operatorname{cos}⁡t){|}_{0}^{\pi /4} \\  & (\operatorname{sin}⁡(\frac{\pi }{4})-\operatorname{cos}⁡(\frac{\pi }{4}))-(\operatorname{sin}⁡(0)-\operatorname{cos}⁡(0)) \\  & =(\frac{\sqrt{2}}{2}-\frac{\sqrt{2}}{2})-(0-1) \\  & =1.\end{aligned}
$$

Multiplying this result by $1/2$, we obtain

$$
\int_{0}^{\frac{\pi}{8}} \frac{\tan{\left(2 x \right)} + 1}{\sec{\left(2 x \right)}}\,\text{d}x=\frac{1}{2}.
$$

## q-74279

Source

Calculate $\int \frac{\operatorname{cos}⁡4x}{{sin}^{2}⁡4x}\,\text{d}x.$

['\\frac{1}{2}{cot}^{2}\u20614x+C', '-\\frac{1}{4}{sin}^{2}\u20614x+C', '-\\frac{1}{4}\\operatorname{csc}\u20614x+C', '\\frac{1}{2}{csc}^{2}\u20614x+C', '-\\frac{1}{4}\\operatorname{cot}\u20614x+C']

We can write the integral as

$$
\int \frac{\operatorname{cos}⁡4x}{{sin}^{2}⁡4x}\,\text{d}x=\int \frac{1}{\operatorname{sin}⁡4x}\cdot \frac{\operatorname{cos}⁡4x}{\operatorname{sin}⁡4x}\,\text{d}x.
$$

We then use the fact that $\frac{\operatorname{cos}⁡4x}{\operatorname{sin}⁡4x}=\operatorname{cot}⁡4x$ and $\frac{1}{\operatorname{sin}⁡4x}=\operatorname{csc}⁡4x$ to express this as

$$
\int \operatorname{csc}⁡4x\operatorname{cot}⁡4x\,\text{d}x.
$$

We can solve this by substitution. Let $u=4x.$ Then $\text{d}x=\frac{1}{4}\text{d}u.$ Therefore,

$$
\begin{aligned}\begin{aligned}\int \operatorname{csc}⁡4x\operatorname{cot}⁡4x\,\text{d}x & =\int \operatorname{csc}⁡u\operatorname{cot}⁡u\,\cdot \frac{1}{4}\text{d}u \\  & =\frac{1}{4}\int \operatorname{csc}⁡u\operatorname{cot}⁡u\,\text{d}u \\  & =-\frac{1}{4}\operatorname{csc}⁡u+C \\  & =-\frac{1}{4}\operatorname{csc}⁡4x+C.\end{aligned}\end{aligned}
$$

Variant

Calculate $\int \frac{\cos{\left(8 x \right)}}{\sin^{2}{\left(8 x \right)}}\,\text{d}x.$

['C + \\frac{\\cot^{2}{\\left(8 x \\right)}}{4}', 'C - \\frac{\\sin^{2}{\\left(8 x \\right)}}{8}', 'C - \\frac{\\csc{\\left(8 x \\right)}}{8}', 'C + \\frac{\\csc^{2}{\\left(8 x \\right)}}{4}', 'C - \\frac{\\cot{\\left(8 x \\right)}}{8}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can write the integral as

$$
\int \frac{\operatorname{cos}⁡4t}{{sin}^{2}⁡4t}\,\text{d}t=\int \frac{1}{\operatorname{sin}⁡4t}\cdot \frac{\operatorname{cos}⁡4t}{\operatorname{sin}⁡4t}\,\text{d}t.
$$

We then use the fact that $\frac{\operatorname{cos}⁡4t}{\operatorname{sin}⁡4t}=\operatorname{cot}⁡4t$ and $\frac{1}{\operatorname{sin}⁡4t}=\operatorname{csc}⁡4t$ to express this as

$$
\int \operatorname{csc}⁡4t\operatorname{cot}⁡4t\,\text{d}t.
$$

We can solve this by substitution. Let $u=4t.$ Then $\text{d}t=\frac{1}{4}\text{d}u.$ Therefore,

$$
\begin{aligned}\begin{aligned}\int \operatorname{csc}⁡4t\operatorname{cot}⁡4t\,\text{d}t & =\int \operatorname{csc}⁡u\operatorname{cot}⁡u\,\cdot \frac{1}{4}\text{d}u \\  & =\frac{1}{4}\int \operatorname{csc}⁡u\operatorname{cot}⁡u\,\text{d}u \\  & =-\frac{1}{4}\operatorname{csc}⁡u+C \\  & =-\frac{1}{4}\operatorname{csc}⁡4t+C.\end{aligned}\end{aligned}
$$

Multiplying this result by $1/2$ and substituting back $t=2x$, we obtain

$$
\int \frac{\cos{\left(8 x \right)}}{\sin^{2}{\left(8 x \right)}}\,\text{d}x=C - \frac{\csc{\left(8 x \right)}}{8}.
$$

## q-74281

Source

Calculate $\int \frac{1-{cot}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x.$

['\\operatorname{cot}\u2061x+C', '{csc}^{2}\u2061x+C', '-\\operatorname{cot}\u2061x+C', '-\\operatorname{csc}\u2061x\\operatorname{cot}\u2061x+C', '\\operatorname{csc}\u2061x+C']

We can write the integral as

$$
\int \frac{1-{cot}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x=\int (1-{cot}^{2}⁡x)\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x
$$

Then, we use the fact that $\operatorname{cot}⁡x=\frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}$ as follows:

$$
\begin{aligned}\int \frac{1-{cot}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x & =\int (1-{cot}^{2}⁡x)\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x \\  & =\int (1-\frac{{cos}^{2}⁡x}{{sin}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x \\  & =\int (\frac{{sin}^{2}⁡x-{cos}^{2}⁡x}{{sin}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x \\  & =-\int (\frac{{cos}^{2}⁡x-{sin}^{2}⁡x}{{sin}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x \\  & =-\int \frac{1}{{sin}^{2}⁡x}\,\text{d}x\end{aligned}
$$

Now we use the fact that $\frac{1}{\operatorname{sin}⁡x}=\operatorname{csc}⁡x$ to express this as

$$
-\int {csc}^{2}⁡x\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}\begin{aligned}-\int {csc}^{2}⁡x\,\text{d}x & =-(-\operatorname{cot}⁡x)+C \\  & =\operatorname{cot}⁡x+C.\end{aligned}\end{aligned}
$$

Variant

Calculate $\int \frac{1 - \cot^{2}{\left(2 x \right)}}{- \sin^{2}{\left(2 x \right)} + \cos^{2}{\left(2 x \right)}}\,\text{d}x.$

['C + \\frac{\\cot{\\left(2 x \\right)}}{2}', 'C + \\frac{\\csc^{2}{\\left(2 x \\right)}}{2}', 'C - \\frac{\\cot{\\left(2 x \\right)}}{2}', 'C - \\frac{\\cot{\\left(2 x \\right)} \\csc{\\left(2 x \\right)}}{2}', 'C + \\frac{\\csc{\\left(2 x \\right)}}{2}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can write the integral as

$$
\int \frac{1-{cot}^{2}⁡t}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t=\int (1-{cot}^{2}⁡t)\cdot \frac{1}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t
$$

Then, we use the fact that $\operatorname{cot}⁡t=\frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t}$ as follows:

$$
\begin{aligned}\int \frac{1-{cot}^{2}⁡t}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t & =\int (1-{cot}^{2}⁡t)\cdot \frac{1}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t \\  & =\int (1-\frac{{cos}^{2}⁡t}{{sin}^{2}⁡t})\cdot \frac{1}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t \\  & =\int (\frac{{sin}^{2}⁡t-{cos}^{2}⁡t}{{sin}^{2}⁡t})\cdot \frac{1}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t \\  & =-\int (\frac{{cos}^{2}⁡t-{sin}^{2}⁡t}{{sin}^{2}⁡t})\cdot \frac{1}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t \\  & =-\int \frac{1}{{sin}^{2}⁡t}\,\text{d}t\end{aligned}
$$

Now we use the fact that $\frac{1}{\operatorname{sin}⁡t}=\operatorname{csc}⁡t$ to express this as

$$
-\int {csc}^{2}⁡t\,\text{d}t.
$$

Therefore,

$$
\begin{aligned}\begin{aligned}-\int {csc}^{2}⁡t\,\text{d}t & =-(-\operatorname{cot}⁡t)+C \\  & =\operatorname{cot}⁡t+C.\end{aligned}\end{aligned}
$$

Multiplying this result by $1/2$ and substituting back $t=2x$, we obtain

$$
\int \frac{1 - \cot^{2}{\left(2 x \right)}}{- \sin^{2}{\left(2 x \right)} + \cos^{2}{\left(2 x \right)}}\,\text{d}x=C + \frac{\cot{\left(2 x \right)}}{2}.
$$

## q-114308

Source

$\int \frac{{tan}^{2}⁡x-{sin}^{3}⁡x}{{sin}^{2}⁡x}\,\text{d}x=$

['\\operatorname{cot}\u2061x+\\operatorname{sin}\u2061x+C', '-\\operatorname{tan}\u2061x+\\operatorname{cos}\u2061x+C', '-\\operatorname{cot}\u2061x-\\operatorname{sin}\u2061x+C', '\\operatorname{tan}\u2061x+\\operatorname{cos}\u2061x+C', '\\operatorname{cot}\u2061x-\\operatorname{cos}\u2061x+C']

We can write the integral as

$$
\int \frac{{tan}^{2}⁡x-{sin}^{3}⁡x}{{sin}^{2}⁡x}\,\text{d}x=\int \frac{1}{{sin}^{2}⁡x}({tan}^{2}⁡x-{sin}^{3}⁡x)\text{d}x.
$$

We then use the fact that ${tan}^{2}⁡x=\frac{{sin}^{2}⁡x}{{cos}^{2}⁡x}$ to express this as

$$
\int \frac{1}{{sin}^{2}⁡x}(\frac{{sin}^{2}⁡x}{{cos}^{2}⁡x}-{sin}^{3}⁡x)\text{d}x.
$$

Therefore,

$$
\begin{aligned}\int \frac{{tan}^{2}⁡x-{sin}^{3}⁡x}{{sin}^{2}⁡x}\,\text{d}x & =\int \frac{1}{{sin}^{2}⁡x}(\frac{{sin}^{2}⁡x}{{cos}^{2}⁡x}-{sin}^{3}⁡x)\text{d}x \\  & =\int (\frac{1}{{sin}^{2}⁡x}\cdot \frac{{sin}^{2}⁡x}{{cos}^{2}⁡x}-\frac{1}{{sin}^{2}⁡x}\cdot {sin}^{3}⁡x)\text{d}x \\  & =\int (\frac{1}{{cos}^{2}⁡x}-\operatorname{sin}⁡x)\text{d}x \\  & =\int ({sec}^{2}⁡x-\operatorname{sin}⁡x)\text{d}x \\  & =\operatorname{tan}⁡x-(-\operatorname{cos}⁡x)+C \\  & =\operatorname{tan}⁡x+\operatorname{cos}⁡x+C.\end{aligned}
$$

Variant

$\int \frac{- \sin^{3}{\left(2 x \right)} + \tan^{2}{\left(2 x \right)}}{\sin^{2}{\left(2 x \right)}}\,\text{d}x=$

['C + \\frac{\\sin{\\left(2 x \\right)}}{2} + \\frac{\\cot{\\left(2 x \\right)}}{2}', 'C + \\frac{\\cos{\\left(2 x \\right)}}{2} - \\frac{\\tan{\\left(2 x \\right)}}{2}', 'C - \\frac{\\sin{\\left(2 x \\right)}}{2} - \\frac{\\cot{\\left(2 x \\right)}}{2}', 'C + \\frac{\\cos{\\left(2 x \\right)}}{2} + \\frac{\\tan{\\left(2 x \\right)}}{2}', 'C - \\frac{\\cos{\\left(2 x \\right)}}{2} + \\frac{\\cot{\\left(2 x \\right)}}{2}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can write the integral as

$$
\int \frac{{tan}^{2}⁡t-{sin}^{3}⁡t}{{sin}^{2}⁡t}\,\text{d}t=\int \frac{1}{{sin}^{2}⁡t}({tan}^{2}⁡t-{sin}^{3}⁡t)\text{d}t.
$$

We then use the fact that ${tan}^{2}⁡t=\frac{{sin}^{2}⁡t}{{cos}^{2}⁡t}$ to express this as

$$
\int \frac{1}{{sin}^{2}⁡t}(\frac{{sin}^{2}⁡t}{{cos}^{2}⁡t}-{sin}^{3}⁡t)\text{d}t.
$$

Therefore,

$$
\begin{aligned}\int \frac{{tan}^{2}⁡t-{sin}^{3}⁡t}{{sin}^{2}⁡t}\,\text{d}t & =\int \frac{1}{{sin}^{2}⁡t}(\frac{{sin}^{2}⁡t}{{cos}^{2}⁡t}-{sin}^{3}⁡t)\text{d}t \\  & =\int (\frac{1}{{sin}^{2}⁡t}\cdot \frac{{sin}^{2}⁡t}{{cos}^{2}⁡t}-\frac{1}{{sin}^{2}⁡t}\cdot {sin}^{3}⁡t)\text{d}t \\  & =\int (\frac{1}{{cos}^{2}⁡t}-\operatorname{sin}⁡t)\text{d}t \\  & =\int ({sec}^{2}⁡t-\operatorname{sin}⁡t)\text{d}t \\  & =\operatorname{tan}⁡t-(-\operatorname{cos}⁡t)+C \\  & =\operatorname{tan}⁡t+\operatorname{cos}⁡t+C.\end{aligned}
$$

Multiplying this result by $1/2$ and substituting back $t=2x$, we obtain

$$
\int \frac{- \sin^{3}{\left(2 x \right)} + \tan^{2}{\left(2 x \right)}}{\sin^{2}{\left(2 x \right)}}\,\text{d}x=C + \frac{\cos{\left(2 x \right)}}{2} + \frac{\tan{\left(2 x \right)}}{2}.
$$

## q-73365

Source

Calculate ${\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x.$

['\\frac{\\sqrt{2}-1}{2}', '\\frac{\\sqrt{3}}{3}', '\\frac{2\\sqrt{3}}{3}', '\\frac{\\sqrt{2}}{2}', '\\frac{\\sqrt{3}-1}{3}']

We can write the integral as

$$
{\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x={\int }_{0}^{\pi /6}(1-{tan}^{2}⁡x)\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x
$$

Then, we use the fact that $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /6}(1-{tan}^{2}⁡x)\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x & ={\int }_{0}^{\pi /6}(1-\frac{{sin}^{2}⁡x}{{cos}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x \\  & ={\int }_{0}^{\pi /6}(\frac{{cos}^{2}⁡x-{sin}^{2}⁡x}{{cos}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x \\  & ={\int }_{0}^{\pi /6}\frac{1}{{cos}^{2}⁡x}\,\text{d}x\end{aligned}
$$

Now we use the fact that $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x$ to express this as

$$
{\int }_{0}^{\pi /6}{sec}^{2}⁡x\text{d}x.
$$

Hence,

$$
\begin{aligned}{\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x & ={\int }_{0}^{\pi /6}{sec}^{2}⁡x\text{d}x \\  & =\operatorname{tan}⁡x{|}_{0}^{\pi /6} \\  & =\operatorname{tan}⁡(\frac{\pi }{6})-\operatorname{tan}⁡0 \\  & =\frac{\sqrt{3}}{3}-0 \\  & =\frac{\sqrt{3}}{3}.\end{aligned}
$$

Variant

Calculate $\int_{0}^{\frac{\pi}{12}} \frac{1 - \tan^{2}{\left(2 x \right)}}{- \sin^{2}{\left(2 x \right)} + \cos^{2}{\left(2 x \right)}}\,\text{d}x.$

['- \\frac{1}{4} + \\frac{\\sqrt{2}}{4}', '\\frac{\\sqrt{3}}{6}', '\\frac{\\sqrt{3}}{3}', '\\frac{\\sqrt{2}}{4}', '- \\frac{1}{6} + \\frac{\\sqrt{3}}{6}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. The limits become $t=0$ and $t=\frac{\pi}{6}$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can write the integral as

$$
{\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡t}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t={\int }_{0}^{\pi /6}(1-{tan}^{2}⁡t)\cdot \frac{1}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t
$$

Then, we use the fact that $\operatorname{tan}⁡t=\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /6}(1-{tan}^{2}⁡t)\cdot \frac{1}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t & ={\int }_{0}^{\pi /6}(1-\frac{{sin}^{2}⁡t}{{cos}^{2}⁡t})\cdot \frac{1}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi /6}(\frac{{cos}^{2}⁡t-{sin}^{2}⁡t}{{cos}^{2}⁡t})\cdot \frac{1}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi /6}\frac{1}{{cos}^{2}⁡t}\,\text{d}t\end{aligned}
$$

Now we use the fact that $\frac{1}{\operatorname{cos}⁡t}=\operatorname{sec}⁡t$ to express this as

$$
{\int }_{0}^{\pi /6}{sec}^{2}⁡t\text{d}t.
$$

Hence,

$$
\begin{aligned}{\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡t}{{cos}^{2}⁡t-{sin}^{2}⁡t}\,\text{d}t & ={\int }_{0}^{\pi /6}{sec}^{2}⁡t\text{d}t \\  & =\operatorname{tan}⁡t{|}_{0}^{\pi /6} \\  & =\operatorname{tan}⁡(\frac{\pi }{6})-\operatorname{tan}⁡0 \\  & =\frac{\sqrt{3}}{3}-0 \\  & =\frac{\sqrt{3}}{3}.\end{aligned}
$$

Multiplying this result by $1/2$, we obtain

$$
\int_{0}^{\frac{\pi}{12}} \frac{1 - \tan^{2}{\left(2 x \right)}}{- \sin^{2}{\left(2 x \right)} + \cos^{2}{\left(2 x \right)}}\,\text{d}x=\frac{\sqrt{3}}{6}.
$$

## q-352711

Source

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /6}\frac{\operatorname{sin}⁡x}{{cos}^{2}⁡x}\,\text{d}x=$
{{field-1}}

['\\frac{2\\sqrt{3}}{3}-1']

We use the identities $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x$ and $\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}=\operatorname{tan}⁡x,$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /6}\frac{\operatorname{sin}⁡x}{{cos}^{2}⁡x}\text{d}x & ={\int }_{0}^{\pi /6}\frac{1}{\operatorname{cos}⁡x}\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x \\  & ={\int }_{0}^{\pi /6}\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x \\  & =\operatorname{sec}⁡x{|}_{0}^{\pi /6} \\  & =(\operatorname{sec}⁡(\frac{\pi }{6})-\operatorname{sec}⁡(0)) \\  & =\frac{2}{\sqrt{3}}-1\end{aligned}
$$

Variant

Evaluate the following integral. Do not round the answer.

$\int_{0}^{\frac{\pi}{12}} \frac{\sin{\left(2 x \right)}}{\cos^{2}{\left(2 x \right)}}\,\text{d}x=$
{{field-1}}

['- \\frac{1}{2} + \\frac{\\sqrt{3}}{3}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. The limits become $t=0$ and $t=\frac{\pi}{6}$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We use the identities $\frac{1}{\operatorname{cos}⁡t}=\operatorname{sec}⁡t$ and $\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}=\operatorname{tan}⁡t,$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /6}\frac{\operatorname{sin}⁡t}{{cos}^{2}⁡t}\text{d}t & ={\int }_{0}^{\pi /6}\frac{1}{\operatorname{cos}⁡t}\cdot \frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi /6}\operatorname{sec}⁡t\operatorname{tan}⁡t\,\text{d}t \\  & =\operatorname{sec}⁡t{|}_{0}^{\pi /6} \\  & =(\operatorname{sec}⁡(\frac{\pi }{6})-\operatorname{sec}⁡(0)) \\  & =\frac{2}{\sqrt{3}}-1\end{aligned}
$$

Multiplying this result by $1/2$, we obtain

$$
\int_{0}^{\frac{\pi}{12}} \frac{\sin{\left(2 x \right)}}{\cos^{2}{\left(2 x \right)}}\,\text{d}x=- \frac{1}{2} + \frac{\sqrt{3}}{3}.
$$

## q-114319

Source

${\int }_{0}^{\pi /3}\frac{\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\,\text{d}x=$

['0', '1', '\\frac{1}{4}', '\\frac{3}{4}', '\\frac{1}{2}']

We can write the integral as

$$
{\int }_{0}^{\pi /3}\frac{\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\,\text{d}x={\int }_{0}^{\pi /3}\frac{1}{\operatorname{sec}⁡x}\cdot \operatorname{tan}⁡x\,\text{d}x.
$$

We then use the fact that $\operatorname{sec}⁡x=\frac{1}{\operatorname{cos}⁡x}$ and $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}$ to express this as

$$
{\int }_{0}^{\pi /3}\operatorname{cos}⁡x\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x.
$$

Therefore,

$$
\begin{aligned}{\int }_{0}^{\pi /3}\frac{1}{\operatorname{sec}⁡x}\cdot \operatorname{tan}⁡x\,\text{d}x & ={\int }_{0}^{\pi /3}\operatorname{cos}⁡x\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x \\  & ={\int }_{0}^{\pi /3}\operatorname{sin}⁡x\,\text{d}x \\  & =-\operatorname{cos}⁡x\,{|}_{0}^{\pi /3} \\  & =-[\operatorname{cos}⁡(\frac{\pi }{3})-\operatorname{cos}⁡0] \\  & =-[\frac{1}{2}-1] \\  & =\frac{1}{2}.\end{aligned}
$$

Variant

$\int_{0}^{\frac{\pi}{6}} \frac{\tan{\left(2 x \right)}}{\sec{\left(2 x \right)}}\,\text{d}x=$

['0', '\\frac{1}{2}', '\\frac{1}{8}', '\\frac{3}{8}', '\\frac{1}{4}']

Let $t=2x$, so $\text{d}x=\frac{1}{2}\text{d}t$. The limits become $t=0$ and $t=\frac{\pi}{3}$. Apply the constant multiple rule to take $1/2$ outside the integral. For the remaining integral, we have:

We can write the integral as

$$
{\int }_{0}^{\pi /3}\frac{\operatorname{tan}⁡t}{\operatorname{sec}⁡t}\,\text{d}t={\int }_{0}^{\pi /3}\frac{1}{\operatorname{sec}⁡t}\cdot \operatorname{tan}⁡t\,\text{d}t.
$$

We then use the fact that $\operatorname{sec}⁡t=\frac{1}{\operatorname{cos}⁡t}$ and $\operatorname{tan}⁡t=\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}$ to express this as

$$
{\int }_{0}^{\pi /3}\operatorname{cos}⁡t\cdot \frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}\,\text{d}t.
$$

Therefore,

$$
\begin{aligned}{\int }_{0}^{\pi /3}\frac{1}{\operatorname{sec}⁡t}\cdot \operatorname{tan}⁡t\,\text{d}t & ={\int }_{0}^{\pi /3}\operatorname{cos}⁡t\cdot \frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}\,\text{d}t \\  & ={\int }_{0}^{\pi /3}\operatorname{sin}⁡t\,\text{d}t \\  & =-\operatorname{cos}⁡t\,{|}_{0}^{\pi /3} \\  & =-[\operatorname{cos}⁡(\frac{\pi }{3})-\operatorname{cos}⁡0] \\  & =-[\frac{1}{2}-1] \\  & =\frac{1}{2}.\end{aligned}
$$

Multiplying this result by $1/2$, we obtain

$$
\int_{0}^{\frac{\pi}{6}} \frac{\tan{\left(2 x \right)}}{\sec{\left(2 x \right)}}\,\text{d}x=\frac{1}{4}.
$$