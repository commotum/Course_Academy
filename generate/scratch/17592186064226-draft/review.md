# Source and variant review

All original source fields and prose remain in source.json and independent-inventory.json. Below, each original-ID fixture is paired with a normal scale -3 instance. Authored hard examples then vary independent coefficients with endpoints held fixed.

## q-49273

Original

$\int \frac{{cos}^{3}⁡x+{cot}^{2}⁡x}{{cos}^{2}⁡x}\,\text{d}x=$

- $-\operatorname{sin}⁡x-\operatorname{tan}⁡x+C$
- $\operatorname{sin}⁡x-\operatorname{cot}⁡x+C$ (correct)
- $\operatorname{sin}⁡x+\operatorname{cot}⁡x+C$
- $\operatorname{sin}⁡x+\operatorname{tan}⁡x+C$
- $\operatorname{sin}⁡x-\operatorname{tan}⁡x+C$

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

Normal variant

$-3\left(\int \frac{{cos}^{3}⁡x+{cot}^{2}⁡x}{{cos}^{2}⁡x}\,\text{d}x\right)=$

{{selection}}

- $C + 3 \sin{\left(x \right)} + 3 \tan{\left(x \right)}$
- $C - 3 \sin{\left(x \right)} + 3 \cot{\left(x \right)}$ (correct)
- $C - 3 \sin{\left(x \right)} - 3 \cot{\left(x \right)}$
- $C - 3 \sin{\left(x \right)} - 3 \tan{\left(x \right)}$
- $C - 3 \sin{\left(x \right)} + 3 \tan{\left(x \right)}$

We can write the integral as

$$
-3\left(\int \frac{{cos}^{3}⁡x+{cot}^{2}⁡x}{{cos}^{2}⁡x}\,\text{d}x\right)=-3\left(\int \frac{1}{{cos}^{2}⁡x}({cos}^{3}⁡x+{cot}^{2}⁡x)\text{d}x\right)
$$

We then use the fact that ${cot}^{2}⁡x=\frac{{cos}^{2}⁡x}{{sin}^{2}⁡x}$ to express this as

$$
-3\left(\int \frac{1}{{cos}^{2}⁡x}({cos}^{3}⁡x+\frac{{cos}^{2}⁡x}{{sin}^{2}⁡x})\text{d}x\right)
$$

Therefore,

$$
\begin{aligned}-3\left(\int \frac{{cos}^{3}⁡x+{cot}^{2}⁡x}{{cos}^{2}⁡x}\,\text{d}x\right)& =-3\left(\int \frac{1}{{cos}^{2}⁡x}({cos}^{3}⁡x+\frac{{cos}^{2}⁡x}{{sin}^{2}⁡x})\text{d}x\right)\\  & =-3\left(\int (\frac{1}{{cos}^{2}⁡x}\cdot {cos}^{3}⁡x+\frac{1}{{cos}^{2}⁡x}\cdot \frac{{cos}^{2}⁡x}{{sin}^{2}⁡x})\text{d}x\right)\\  & =-3\left(\int (\operatorname{cos}⁡x+\frac{1}{{sin}^{2}⁡x})\text{d}x\right)\\  & =-3\left(\int (\operatorname{cos}⁡x+{csc}^{2}⁡x)\text{d}x\right)\\  & =-3\left(\operatorname{sin}⁡x-\operatorname{cot}⁡x\right)+C\end{aligned}
$$

## q-49275

Original

Calculate $\int \frac{{tan}^{2}⁡x}{8{sin}^{2}⁡x}\,\text{d}x.$

- $\frac{1}{8}\operatorname{tan}⁡x\operatorname{sec}⁡x+C$
- $\frac{1}{8}{tan}^{2}⁡x{sec}^{2}⁡x+C$
- $\frac{1}{8}{tan}^{2}⁡x+C$
- $\frac{1}{8}{csc}^{2}⁡x+C$
- $\frac{1}{8}\operatorname{tan}⁡x+C$ (correct)

We can write the integral as

$$
\int \frac{{tan}^{2}⁡x}{8{sin}^{2}⁡x}\,\text{d}x=\frac{1}{8}\int {tan}^{2}⁡x\cdot \frac{1}{{sin}^{2}⁡x}\,\text{d}x.
$$

We then use the fact that $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}$ and $\operatorname{sec}⁡x=\frac{1}{\operatorname{cos}⁡x}.$ Therefore,

$$
\begin{aligned}\begin{aligned}\int \frac{{tan}^{2}⁡x}{8{sin}^{2}⁡x}\,\text{d}x & =\frac{1}{8}\int {tan}^{2}⁡x\cdot \frac{1}{{sin}^{2}⁡x}\,\text{d}x \\  & =\frac{1}{8}\int {(\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x})}^{2}\cdot \frac{1}{{sin}^{2}⁡x}\,\text{d}x \\  & =\frac{1}{8}\int \frac{{sin}^{2}⁡x}{{cos}^{2}⁡x}\cdot \frac{1}{{sin}^{2}⁡x}\,\text{d}x \\  & =\frac{1}{8}\int \frac{1}{{cos}^{2}⁡x}\,\text{d}x \\  & =\frac{1}{8}\int {(\frac{1}{\operatorname{cos}⁡x})}^{2}\text{d}x \\  & =\frac{1}{8}\int {sec}^{2}⁡x\,\text{d}x \\  & =\frac{1}{8}\operatorname{tan}⁡x+C.\end{aligned}\end{aligned}
$$

Normal variant

Calculate $-3\left(\int \frac{{tan}^{2}⁡x}{8{sin}^{2}⁡x}\,\text{d}x\right).$

{{selection}}

- $C - \frac{3 \tan{\left(x \right)} \sec{\left(x \right)}}{8}$
- $C - \frac{3 \tan^{2}{\left(x \right)} \sec^{2}{\left(x \right)}}{8}$
- $C - \frac{3 \tan^{2}{\left(x \right)}}{8}$
- $C - \frac{3 \csc^{2}{\left(x \right)}}{8}$
- $C - \frac{3 \tan{\left(x \right)}}{8}$ (correct)

We can write the integral as

$$
-3\left(\int \frac{{tan}^{2}⁡x}{8{sin}^{2}⁡x}\,\text{d}x\right)=-3\left(\frac{1}{8}\int {tan}^{2}⁡x\cdot \frac{1}{{sin}^{2}⁡x}\,\text{d}x\right)
$$

We then use the fact that $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}$ and $\operatorname{sec}⁡x=\frac{1}{\operatorname{cos}⁡x}.$ Therefore,

$$
\begin{aligned}-3\left(\int \frac{{tan}^{2}⁡x}{8{sin}^{2}⁡x}\,\text{d}x\right)& =-3\left(\frac{1}{8}\int {tan}^{2}⁡x\cdot \frac{1}{{sin}^{2}⁡x}\,\text{d}x\right)\\  & =-3\left(\frac{1}{8}\int {(\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x})}^{2}\cdot \frac{1}{{sin}^{2}⁡x}\,\text{d}x\right)\\  & =-3\left(\frac{1}{8}\int \frac{{sin}^{2}⁡x}{{cos}^{2}⁡x}\cdot \frac{1}{{sin}^{2}⁡x}\,\text{d}x\right)\\  & =-3\left(\frac{1}{8}\int \frac{1}{{cos}^{2}⁡x}\,\text{d}x\right)\\  & =-3\left(\frac{1}{8}\int {(\frac{1}{\operatorname{cos}⁡x})}^{2}\text{d}x\right)\\  & =-3\left(\frac{1}{8}\int {sec}^{2}⁡x\,\text{d}x\right)\\  & =-3\left(\frac{1}{8}\operatorname{tan}⁡x\right)+C\end{aligned}
$$

## q-114306

Original

${\int }_{0}^{\pi /4}\frac{3\operatorname{sec}⁡x\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x=$

- $3(\sqrt{2}-1)$ (correct)
- $3(\sqrt{2}-2)$
- $\sqrt{2}-3$
- $3(\sqrt{2}+1)$
- $\sqrt{2}+1$

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

Normal variant

$-3\left({\int }_{0}^{\pi /4}\frac{3\operatorname{sec}⁡x\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x\right)=$

{{selection}}

- $9 - 9 \sqrt{2}$ (correct)
- $18 - 9 \sqrt{2}$
- $9 - 3 \sqrt{2}$
- $- 9 \sqrt{2} - 9$
- $- 3 \sqrt{2} - 3$

We can write the integral as

$$
-3\left({\int }_{0}^{\pi /4}\frac{3\operatorname{sec}⁡x\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x\right)=-3\left(3{\int }_{0}^{\pi /4}\operatorname{sec}⁡x\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x\right)
$$

Then, we use the fact that $\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}=\operatorname{tan}⁡x,$ as follows:

$$
\begin{aligned}-3\left(3{\int }_{0}^{\pi /4}\operatorname{sec}⁡x\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x\right)& =-3\left(3{\int }_{0}^{\pi /4}\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x\right)\end{aligned}
$$

Therefore,

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /4}\frac{3\operatorname{sec}⁡x\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x\right)& =-3\left(3{\int }_{0}^{\pi /4}\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x\right)\\  & =-3\left(3\operatorname{sec}⁡x\,{|}_{0}^{\pi /4}\right)\\  & =-3\left(3[\operatorname{sec}⁡(\frac{\pi }{4})-\operatorname{sec}⁡0]\right)\\  & =-3\left(3(\sqrt{2}-1)\right)\end{aligned}
$$

## q-114313

Original

$\int \frac{\operatorname{sin}⁡x-\operatorname{csc}⁡x}{\operatorname{tan}⁡x}\,\text{d}x=$

- $\operatorname{cos}⁡x-\operatorname{csc}⁡x+C$
- $\operatorname{sin}⁡x+\operatorname{csc}⁡x+C$ (correct)
- $\operatorname{csc}⁡x+\operatorname{sec}⁡x+C$
- $\operatorname{sin}⁡x-\operatorname{cot}⁡x+C$
- $\operatorname{csc}⁡x-\operatorname{cot}⁡x+C$

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

Normal variant

$-3\left(\int \frac{\operatorname{sin}⁡x-\operatorname{csc}⁡x}{\operatorname{tan}⁡x}\,\text{d}x\right)=$

{{selection}}

- $C - 3 \cos{\left(x \right)} + 3 \csc{\left(x \right)}$
- $C - 3 \sin{\left(x \right)} - 3 \csc{\left(x \right)}$ (correct)
- $C - 3 \csc{\left(x \right)} - 3 \sec{\left(x \right)}$
- $C - 3 \sin{\left(x \right)} + 3 \cot{\left(x \right)}$
- $C + 3 \cot{\left(x \right)} - 3 \csc{\left(x \right)}$

We can write the integral as

$$
-3\left(\int \frac{\operatorname{sin}⁡x-\operatorname{csc}⁡x}{\operatorname{tan}⁡x}\,\text{d}x\right)=-3\left(\int \frac{1}{\operatorname{tan}⁡x}(\operatorname{sin}⁡x-\operatorname{csc}⁡x)\text{d}x\right)
$$

We then use the fact that $\frac{1}{\operatorname{tan}⁡x}=\operatorname{cot}⁡x=\frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}$ to express this as

$$
\begin{aligned}-3\left(\int \operatorname{cot}⁡x(\operatorname{sin}⁡x-\operatorname{csc}⁡x)\text{d}x\right)& =-3\left(\int (\operatorname{cot}⁡x\operatorname{sin}⁡x-\operatorname{cot}⁡x\cdot \operatorname{csc}⁡x)\text{d}x\right)\\  & =-3\left(\int (\frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}\cdot \operatorname{sin}⁡x-\operatorname{cot}⁡x\cdot \operatorname{csc}⁡x)\text{d}x\right)\\  & =-3\left(\int (\operatorname{cos}⁡x-\operatorname{csc}⁡x\operatorname{cot}⁡x)\text{d}x\right)\end{aligned}
$$

Therefore,

$$
\begin{aligned}-3\left(\int \frac{\operatorname{sin}⁡x-\operatorname{csc}⁡x}{\operatorname{tan}⁡x}\,\text{d}x\right)& =-3\left(\int (\operatorname{cos}⁡x-\operatorname{csc}⁡x\operatorname{cot}⁡x)\text{d}x\right)\\  & =-3\left(\operatorname{sin}⁡x-(-\operatorname{csc}⁡x)\right)+C\\  & =-3\left(\operatorname{sin}⁡x+\operatorname{csc}⁡x\right)+C\end{aligned}
$$

## q-114318

Original

${\int }_{\pi /4}^{\pi /2}\frac{\operatorname{cos}⁡x}{{sin}^{2}⁡x}\,\text{d}x=$

- $\sqrt{2}-1$ (correct)
- $3\sqrt{2}-2$
- $2\sqrt{2}$
- $\frac{\sqrt{2}+1}{2}$
- $\frac{\sqrt{2}-2}{3}$

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

Normal variant

$-3\left({\int }_{\pi /4}^{\pi /2}\frac{\operatorname{cos}⁡x}{{sin}^{2}⁡x}\,\text{d}x\right)=$

{{selection}}

- $3 - 3 \sqrt{2}$ (correct)
- $6 - 9 \sqrt{2}$
- $- 6 \sqrt{2}$
- $- \frac{3 \sqrt{2}}{2} - \frac{3}{2}$
- $2 - \sqrt{2}$

We can write the integral as

$$
-3\left({\int }_{\pi /4}^{\pi /2}\frac{\operatorname{cos}⁡x}{{sin}^{2}⁡x}\,\text{d}x\right)=-3\left({\int }_{\pi /4}^{\pi /2}\frac{1}{\operatorname{sin}⁡x}\cdot \frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}\,\text{d}x\right)
$$

We then use the fact that $\frac{1}{\operatorname{sin}⁡x}=\operatorname{csc}⁡x$ and $\frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}=\operatorname{cot}⁡x$ to express this as

$$
-3\left({\int }_{\pi /4}^{\pi /2}\operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x\right)
$$

Therefore,

$$
\begin{aligned}-3\left({\int }_{\pi /4}^{\pi /2}\frac{1}{\operatorname{sin}⁡x}\cdot \frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}\,\text{d}x\right)& =-3\left({\int }_{\pi /4}^{\pi /2}\operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x\right)\\  & =-3\left(-\operatorname{csc}⁡x\,{|}_{\pi /4}^{\pi /2}\right)\\  & =-3\left(-[\operatorname{csc}⁡(\frac{\pi }{2})-\operatorname{csc}⁡(\frac{\pi }{4})]\right)\\  & =-3\left(-[1-\sqrt{2}]\right)\\  & =-3\left(\sqrt{2}-1\right)\end{aligned}
$$

## q-352848

Original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x=$
{{field-1}}

- $\frac{\sqrt{3}}{3}$ (correct)

We use the identities $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}$  and  $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x,$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\text{d}x & ={\int }_{0}^{\pi /6}(1-{tan}^{2}⁡x)\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x \\  & ={\int }_{0}^{\pi /6}(1-\frac{{sin}^{2}⁡x}{{cos}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x \\  & ={\int }_{0}^{\pi /6}(\frac{{cos}^{2}⁡x-{sin}^{2}⁡x}{{cos}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x \\  & ={\int }_{0}^{\pi /6}\frac{1}{{cos}^{2}⁡x}\,\text{d}x \\  & ={\int }_{0}^{\pi /6}{sec}^{2}⁡x\,\text{d}x \\  & =\operatorname{tan}⁡x{|}_{0}^{\pi /6} \\  & =\operatorname{tan}⁡(\frac{\pi }{6})-\operatorname{tan}⁡0 \\  & =\frac{\sqrt{3}}{3}-0 \\  & =\frac{\sqrt{3}}{3}\end{aligned}
$$

Normal variant

Evaluate the following integral. Do not round the answer.

$-3\left({\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)=$
{{field-1}}

- $- \sqrt{3}$ (correct)

We use the identities $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}$  and  $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x,$ as follows:

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\text{d}x\right)& =-3\left({\int }_{0}^{\pi /6}(1-{tan}^{2}⁡x)\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)\\  & =-3\left({\int }_{0}^{\pi /6}(1-\frac{{sin}^{2}⁡x}{{cos}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)\\  & =-3\left({\int }_{0}^{\pi /6}(\frac{{cos}^{2}⁡x-{sin}^{2}⁡x}{{cos}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)\\  & =-3\left({\int }_{0}^{\pi /6}\frac{1}{{cos}^{2}⁡x}\,\text{d}x\right)\\  & =-3\left({\int }_{0}^{\pi /6}{sec}^{2}⁡x\,\text{d}x\right)\\  & =-3\left(\operatorname{tan}⁡x{|}_{0}^{\pi /6}\right)\\  & =-3\left(\operatorname{tan}⁡(\frac{\pi }{6})-\operatorname{tan}⁡0\right)\\  & =-3\left(\frac{\sqrt{3}}{3}-0\right)\\  & =-3\left(\frac{\sqrt{3}}{3}\right)\end{aligned}
$$

## q-352853

Original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /3}\frac{1+\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\,\text{d}x=$
{{field-1}}

- $\frac{1}{2}+\frac{\sqrt{3}}{2}$ (correct)

We use the identities $\frac{1}{\operatorname{sec}⁡x}=\operatorname{cos}⁡x$  and  $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x},$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /3}\frac{1+\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\text{d}x & ={\int }_{0}^{\pi /3}\frac{1}{\operatorname{sec}⁡x}\cdot (1+\operatorname{tan}⁡x)\,\text{d}x \\  & ={\int }_{0}^{\pi /3}\operatorname{cos}⁡x(1+\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x})\,\text{d}x \\  & ={\int }_{0}^{\pi /3}(\operatorname{cos}⁡x+\operatorname{sin}⁡x)\,\text{d}x \\  & =(\operatorname{sin}⁡x-\operatorname{cos}⁡x){|}_{0}^{\pi /3} \\  & =(\frac{\sqrt{3}}{2}-\frac{1}{2})-(0-1) \\  & =\frac{1}{2}+\frac{\sqrt{3}}{2}\end{aligned}
$$

Normal variant

Evaluate the following integral. Do not round the answer.

$-3\left({\int }_{0}^{\pi /3}\frac{1+\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\,\text{d}x\right)=$
{{field-1}}

- $- \frac{3 \sqrt{3}}{2} - \frac{3}{2}$ (correct)

We use the identities $\frac{1}{\operatorname{sec}⁡x}=\operatorname{cos}⁡x$  and  $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x},$ as follows:

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /3}\frac{1+\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\text{d}x\right)& =-3\left({\int }_{0}^{\pi /3}\frac{1}{\operatorname{sec}⁡x}\cdot (1+\operatorname{tan}⁡x)\,\text{d}x\right)\\  & =-3\left({\int }_{0}^{\pi /3}\operatorname{cos}⁡x(1+\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x})\,\text{d}x\right)\\  & =-3\left({\int }_{0}^{\pi /3}(\operatorname{cos}⁡x+\operatorname{sin}⁡x)\,\text{d}x\right)\\  & =-3\left((\operatorname{sin}⁡x-\operatorname{cos}⁡x){|}_{0}^{\pi /3}\right)\\  & =-3\left((\frac{\sqrt{3}}{2}-\frac{1}{2})-(0-1)\right)\\  & =-3\left(\frac{1}{2}+\frac{\sqrt{3}}{2}\right)\end{aligned}
$$

## q-352858

Original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /8}\frac{\operatorname{cot}⁡4x}{\operatorname{csc}⁡4x}\,\text{d}x=$
{{field-1}}

- $\frac{1}{4}$ (correct)

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

Normal variant

Evaluate the following integral. Do not round the answer.

$-3\left({\int }_{0}^{\pi /8}\frac{\operatorname{cot}⁡4x}{\operatorname{csc}⁡4x}\,\text{d}x\right)=$
{{field-1}}

- $- \frac{3}{4}$ (correct)

We can write the integral as

$$
-3\left({\int }_{0}^{\pi /8}\frac{\operatorname{cot}⁡4x}{\operatorname{csc}⁡4x}\,\text{d}x\right)=-3\left({\int }_{0}^{\pi /8}\operatorname{cot}⁡4x\cdot \frac{1}{\operatorname{csc}⁡4x}\,\text{d}x\right)
$$

Then, we use the fact that $\operatorname{cot}⁡4x=\frac{\operatorname{cos}⁡4x}{\operatorname{sin}⁡4x}$ and $\frac{1}{\operatorname{csc}⁡4x}=\operatorname{sin}⁡4x$ as follows:

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /8}\frac{\operatorname{cos}⁡4x}{\operatorname{sin}⁡4x}\cdot \operatorname{sin}⁡4x\,\text{d}x\right)& =-3\left({\int }_{0}^{\pi /8}\operatorname{cos}⁡4x\,\text{d}x\right)\end{aligned}
$$

We can solve this by substitution. Let $u=4x.$ Then $\text{d}x=\frac{1}{4}\text{d}u.$ 

Now, we fill the table for the limits of integration, according to the rule $u=4x.$

| $x$ | $0$ | $\frac{\pi }{8}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi }{2}$ |

Therefore, the integral in terms of the new variable is

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /8}\operatorname{cos}⁡4x\,\text{d}x\right)& =-3\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡u\cdot \frac{1}{4}\text{d}u\right)\\  & =-3\left(\frac{1}{4}{\int }_{0}^{\pi /2}\operatorname{cos}⁡u\text{d}u\right)\\  & =-3\left(\frac{1}{4}\operatorname{sin}⁡u{|}_{0}^{\pi /2}\right)\\  & =-3\left(\frac{1}{4}(sin\,(\frac{\pi }{2})-sin\,(0))\right)\\  & =-3\left(\frac{1}{4}(1-0)\right)\\  & =-3\left(\frac{1}{4}\right)\end{aligned}
$$

The original quotient is undefined at $x=0$. This is an improper integral; the simplified integrand has a finite right limit there.

## q-352867

Original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /10}\frac{\operatorname{cot}⁡5x}{\operatorname{csc}⁡5x}\,\text{d}x=$
{{field-1}}

- $\frac{1}{5}$ (correct)

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

Normal variant

Evaluate the following integral. Do not round the answer.

$-3\left({\int }_{0}^{\pi /10}\frac{\operatorname{cot}⁡5x}{\operatorname{csc}⁡5x}\,\text{d}x\right)=$
{{field-1}}

- $- \frac{3}{5}$ (correct)

We can rewrite the integral as

$$
-3\left({\int }_{0}^{\pi /10}\frac{\operatorname{cot}⁡5x}{\operatorname{csc}⁡5x}\,\text{d}x\right)=-3\left({\int }_{0}^{\pi /10}\operatorname{cot}⁡5x\cdot \frac{1}{\operatorname{csc}⁡5x}\,\text{d}x\right)
$$

Then, we use the fact that $\operatorname{cot}⁡5x=\frac{\operatorname{cos}⁡5x}{\operatorname{sin}⁡5x}$ and $\frac{1}{\operatorname{csc}⁡5x}=\operatorname{sin}⁡5x$ as follows:

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /10}\frac{\operatorname{cos}⁡5x}{\operatorname{sin}⁡5x}\cdot \operatorname{sin}⁡5x\,\text{d}x\right)& =-3\left({\int }_{0}^{\pi /10}\operatorname{cos}⁡5x\,\text{d}x\right)\end{aligned}
$$

We can solve this by substitution. Let $u=5x.$ Then $\text{d}x=\frac{1}{5}\text{d}u.$

Now, we fill the table for the limits of integration, according to the rule $u=5x.$

| $x$ | $0$ | $\frac{\pi }{10}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi }{2}$ |

Therefore, the integral in terms of the new variable is

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /10}\operatorname{cos}⁡5x\,\text{d}x\right)& =-3\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡u\cdot \frac{1}{5}\,\text{d}u\right)\\  & =-3\left(\frac{1}{5}{\int }_{0}^{\pi /2}\operatorname{cos}⁡u\,\text{d}u\right)\\  & =-3\left(\frac{1}{5}\operatorname{sin}⁡u{|}_{0}^{\pi /2}\right)\\  & =-3\left(\frac{1}{5}(sin\,(\frac{\pi }{2})-\operatorname{sin}⁡(0))\right)\\  & =-3\left(\frac{1}{5}(1-0)\right)\\  & =-3\left(\frac{1}{5}\right)\end{aligned}
$$

The original quotient is undefined at $x=0$. This is an improper integral; the simplified integrand has a finite right limit there.

## q-352868

Original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /12}\frac{\operatorname{tan}⁡4x}{\operatorname{sec}⁡4x}\,\text{d}x=$
{{field-1}}

- $\frac{1}{8}$ (correct)

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

Normal variant

Evaluate the following integral. Do not round the answer.

$-3\left({\int }_{0}^{\pi /12}\frac{\operatorname{tan}⁡4x}{\operatorname{sec}⁡4x}\,\text{d}x\right)=$
{{field-1}}

- $- \frac{3}{8}$ (correct)

We can rewrite the integral as

$$
-3\left({\int }_{0}^{\pi /12}\frac{\operatorname{tan}⁡4x}{\operatorname{sec}⁡4x}\,\text{d}x\right)=-3\left({\int }_{0}^{\pi /12}\operatorname{tan}⁡4x\cdot \frac{1}{\operatorname{sec}⁡4x}\,\text{d}x\right)
$$

Then, we use the fact that $\operatorname{tan}⁡4x=\frac{\operatorname{sin}⁡4x}{\operatorname{cos}⁡4x}$ and $\frac{1}{\operatorname{sec}⁡4x}=\operatorname{cos}⁡4x$ as follows:

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /12}\frac{\operatorname{sin}⁡4x}{\operatorname{cos}⁡4x}\cdot \operatorname{cos}⁡4x\,\text{d}x\right)& =-3\left({\int }_{0}^{\pi /12}\operatorname{sin}⁡4x\,\text{d}x\right)\end{aligned}
$$

We can solve this by substitution. Let $u=4x.$ Then $\text{d}x=\frac{1}{4}\text{d}u.$

Now, we fill the table for the limits of integration, according to the rule $u=4x.$

| $x$ | $0$ | $\frac{\pi }{12}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi }{3}$ |

Therefore, the integral in terms of the new variable is

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /12}\operatorname{sin}⁡4x\,\text{d}x\right)& =-3\left({\int }_{0}^{\pi /3}\operatorname{sin}⁡u\cdot \frac{1}{4}\,\text{d}u\right)\\  & =-3\left(\frac{1}{4}{\int }_{0}^{\pi /3}\operatorname{sin}⁡u\,\text{d}u\right)\\  & =-3\left(-\frac{1}{4}\operatorname{cos}⁡u{|}_{0}^{\pi /3}\right)\\  & =-3\left(-\frac{1}{4}(cos\,(\frac{\pi }{3})-\operatorname{cos}⁡(0))\right)\\  & =-3\left(-\frac{1}{4}(\frac{1}{2}-1)\right)\\  & =-3\left(\frac{1}{8}\right)\end{aligned}
$$

## q-49284

Original

Evaluate ${\int }_{0}^{\pi /4}\frac{\operatorname{sin}⁡x}{{cos}^{2}⁡x}\,\text{d}x.$

- $\sqrt{2}-1$ (correct)
- $\frac{\sqrt{2}}{2}-1$
- $2\sqrt{2}-1$
- $\frac{\sqrt{2}}{2}$
- $\sqrt{2}$

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

Normal variant

Evaluate $-3\left({\int }_{0}^{\pi /4}\frac{\operatorname{sin}⁡x}{{cos}^{2}⁡x}\,\text{d}x\right).$

{{selection}}

- $3 - 3 \sqrt{2}$ (correct)
- $3 - \frac{3 \sqrt{2}}{2}$
- $3 - 6 \sqrt{2}$
- $- \frac{3 \sqrt{2}}{2}$
- $- 3 \sqrt{2}$

We can write the integral as

$$
-3\left({\int }_{0}^{\pi /4}\frac{\operatorname{sin}⁡x}{{cos}^{2}⁡x}\text{d}x\right)=-3\left({\int }_{0}^{\pi /4}\frac{1}{\operatorname{cos}⁡x}\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x\right)
$$

We use the fact that $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x$ and $\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}=\operatorname{tan}⁡x$ to express this as

$$
-3\left({\int }_{0}^{\pi /4}\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x\right)
$$

Therefore,

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /4}\frac{\operatorname{sin}⁡x}{{cos}^{2}⁡x}\text{d}x\right)& =-3\left({\int }_{0}^{\pi /4}\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x\right)\\  & =-3\left(\operatorname{sec}⁡x{|}_{0}^{\pi /4}\right)\\  & =-3\left((\operatorname{sec}⁡(\frac{\pi }{4})-\operatorname{sec}⁡(0))\right)\\  & =-3\left(\sqrt{2}-1\right)\end{aligned}
$$

## q-73361

Original

Evaluate ${\int }_{0}^{\pi /4}\frac{1+\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\,\text{d}x.$

- $\sqrt{2}-2$
- $1$ (correct)
- $0$
- $\frac{1}{2}$
- $\sqrt{2}$

We can write the integral as

$$
{\int }_{0}^{\pi /4}\frac{1+\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\text{d}x={\int }_{0}^{\pi /4}\frac{1}{\operatorname{sec}⁡x}\cdot (1+\operatorname{tan}⁡x)\,\text{d}x
$$

We then use the fact that $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x$ and $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}.$ Therefore,

$$
\begin{aligned}{\int }_{0}^{\pi /4}\frac{1}{\operatorname{sec}⁡x}\cdot (1+\operatorname{tan}⁡x)\,\text{d}x & ={\int }_{0}^{\pi /4}\operatorname{cos}⁡x\cdot (1+\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x})\,\text{d}x \\  & ={\int }_{0}^{\pi /4}(\operatorname{cos}⁡x+\operatorname{cos}⁡x\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x})\,\text{d}x \\  & ={\int }_{0}^{\pi /4}(\operatorname{cos}⁡x+\operatorname{sin}⁡x)\,\text{d}x \\  & =(\operatorname{sin}⁡x-\operatorname{cos}⁡x){|}_{0}^{\pi /4} \\  & (\operatorname{sin}⁡(\frac{\pi }{4})-\operatorname{cos}⁡(\frac{\pi }{4}))-(\operatorname{sin}⁡(0)-\operatorname{cos}⁡(0)) \\  & =(\frac{\sqrt{2}}{2}-\frac{\sqrt{2}}{2})-(0-1) \\  & =1.\end{aligned}
$$

Normal variant

Evaluate $-3\left({\int }_{0}^{\pi /4}\frac{1+\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\,\text{d}x\right).$

{{selection}}

- $6 - 3 \sqrt{2}$
- $-3$ (correct)
- $0$
- $- \frac{3}{2}$
- $- 3 \sqrt{2}$

We can write the integral as

$$
-3\left({\int }_{0}^{\pi /4}\frac{1+\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\text{d}x\right)=-3\left({\int }_{0}^{\pi /4}\frac{1}{\operatorname{sec}⁡x}\cdot (1+\operatorname{tan}⁡x)\,\text{d}x\right)
$$

We then use the fact that $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x$ and $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}.$ Therefore,

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /4}\frac{1}{\operatorname{sec}⁡x}\cdot (1+\operatorname{tan}⁡x)\,\text{d}x\right)& =-3\left({\int }_{0}^{\pi /4}\operatorname{cos}⁡x\cdot (1+\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x})\,\text{d}x\right)\\  & =-3\left({\int }_{0}^{\pi /4}(\operatorname{cos}⁡x+\operatorname{cos}⁡x\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x})\,\text{d}x\right)\\  & =-3\left({\int }_{0}^{\pi /4}(\operatorname{cos}⁡x+\operatorname{sin}⁡x)\,\text{d}x\right)\\  & =-3\left((\operatorname{sin}⁡x-\operatorname{cos}⁡x){|}_{0}^{\pi /4}\right)\\  & =-3\left((\operatorname{sin}⁡(\frac{\pi }{4})-\operatorname{cos}⁡(\frac{\pi }{4}))-(\operatorname{sin}⁡(0)-\operatorname{cos}⁡(0))\right)\\  & =-3\left((\frac{\sqrt{2}}{2}-\frac{\sqrt{2}}{2})-(0-1)\right)\\  & =-3\left(1\right)\end{aligned}
$$

## q-74279

Original

Calculate $\int \frac{\operatorname{cos}⁡4x}{{sin}^{2}⁡4x}\,\text{d}x.$

- $\frac{1}{2}{cot}^{2}⁡4x+C$
- $-\frac{1}{4}{sin}^{2}⁡4x+C$
- $-\frac{1}{4}\operatorname{csc}⁡4x+C$ (correct)
- $\frac{1}{2}{csc}^{2}⁡4x+C$
- $-\frac{1}{4}\operatorname{cot}⁡4x+C$

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

Normal variant

Calculate $-3\left(\int \frac{\operatorname{cos}⁡4x}{{sin}^{2}⁡4x}\,\text{d}x\right).$

{{selection}}

- $C - \frac{3 \cot^{2}{\left(4 x \right)}}{2}$
- $C + \frac{3 \sin^{2}{\left(4 x \right)}}{4}$
- $C + \frac{3 \csc{\left(4 x \right)}}{4}$ (correct)
- $C - \frac{3 \csc^{2}{\left(4 x \right)}}{2}$
- $C + \frac{3 \cot{\left(4 x \right)}}{4}$

We can write the integral as

$$
-3\left(\int \frac{\operatorname{cos}⁡4x}{{sin}^{2}⁡4x}\,\text{d}x\right)=-3\left(\int \frac{1}{\operatorname{sin}⁡4x}\cdot \frac{\operatorname{cos}⁡4x}{\operatorname{sin}⁡4x}\,\text{d}x\right)
$$

We then use the fact that $\frac{\operatorname{cos}⁡4x}{\operatorname{sin}⁡4x}=\operatorname{cot}⁡4x$ and $\frac{1}{\operatorname{sin}⁡4x}=\operatorname{csc}⁡4x$ to express this as

$$
-3\left(\int \operatorname{csc}⁡4x\operatorname{cot}⁡4x\,\text{d}x\right)
$$

We can solve this by substitution. Let $u=4x.$ Then $\text{d}x=\frac{1}{4}\text{d}u.$ Therefore,

$$
\begin{aligned}-3\left(\int \operatorname{csc}⁡4x\operatorname{cot}⁡4x\,\text{d}x\right)& =-3\left(\int \operatorname{csc}⁡u\operatorname{cot}⁡u\,\cdot \frac{1}{4}\text{d}u\right)\\  & =-3\left(\frac{1}{4}\int \operatorname{csc}⁡u\operatorname{cot}⁡u\,\text{d}u\right)\\  & =-3\left(-\frac{1}{4}\operatorname{csc}⁡u\right)+C\\  & =-3\left(-\frac{1}{4}\operatorname{csc}⁡4x\right)+C\end{aligned}
$$

## q-74281

Original

Calculate $\int \frac{1-{cot}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x.$

- $\operatorname{cot}⁡x+C$ (correct)
- ${csc}^{2}⁡x+C$
- $-\operatorname{cot}⁡x+C$
- $-\operatorname{csc}⁡x\operatorname{cot}⁡x+C$
- $\operatorname{csc}⁡x+C$

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

Normal variant

Calculate $-3\left(\int \frac{1-{cot}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right).$

{{selection}}

- $C - 3 \cot{\left(x \right)}$ (correct)
- $C - 3 \csc^{2}{\left(x \right)}$
- $C + 3 \cot{\left(x \right)}$
- $C + 3 \cot{\left(x \right)} \csc{\left(x \right)}$
- $C - 3 \csc{\left(x \right)}$

We can write the integral as

$$
-3\left(\int \frac{1-{cot}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)=-3\left(\int (1-{cot}^{2}⁡x)\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)
$$

Then, we use the fact that $\operatorname{cot}⁡x=\frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}$ as follows:

$$
\begin{aligned}-3\left(\int \frac{1-{cot}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)& =-3\left(\int (1-{cot}^{2}⁡x)\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)\\  & =-3\left(\int (1-\frac{{cos}^{2}⁡x}{{sin}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)\\  & =-3\left(\int (\frac{{sin}^{2}⁡x-{cos}^{2}⁡x}{{sin}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)\\  & =-3\left(-\int (\frac{{cos}^{2}⁡x-{sin}^{2}⁡x}{{sin}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)\\  & =-3\left(-\int \frac{1}{{sin}^{2}⁡x}\,\text{d}x\right)\end{aligned}
$$

Now we use the fact that $\frac{1}{\operatorname{sin}⁡x}=\operatorname{csc}⁡x$ to express this as

$$
-3\left(-\int {csc}^{2}⁡x\,\text{d}x\right)
$$

Therefore,

$$
\begin{aligned}-3\left(-\int {csc}^{2}⁡x\,\text{d}x\right)& =-3\left(-(-\operatorname{cot}⁡x)\right)+C\\  & =-3\left(\operatorname{cot}⁡x\right)+C\end{aligned}
$$

## q-114308

Original

$\int \frac{{tan}^{2}⁡x-{sin}^{3}⁡x}{{sin}^{2}⁡x}\,\text{d}x=$

- $\operatorname{cot}⁡x+\operatorname{sin}⁡x+C$
- $-\operatorname{tan}⁡x+\operatorname{cos}⁡x+C$
- $-\operatorname{cot}⁡x-\operatorname{sin}⁡x+C$
- $\operatorname{tan}⁡x+\operatorname{cos}⁡x+C$ (correct)
- $\operatorname{cot}⁡x-\operatorname{cos}⁡x+C$

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

Normal variant

$-3\left(\int \frac{{tan}^{2}⁡x-{sin}^{3}⁡x}{{sin}^{2}⁡x}\,\text{d}x\right)=$

{{selection}}

- $C - 3 \sin{\left(x \right)} - 3 \cot{\left(x \right)}$
- $C - 3 \cos{\left(x \right)} + 3 \tan{\left(x \right)}$
- $C + 3 \sin{\left(x \right)} + 3 \cot{\left(x \right)}$
- $C - 3 \cos{\left(x \right)} - 3 \tan{\left(x \right)}$ (correct)
- $C + 3 \cos{\left(x \right)} - 3 \cot{\left(x \right)}$

We can write the integral as

$$
-3\left(\int \frac{{tan}^{2}⁡x-{sin}^{3}⁡x}{{sin}^{2}⁡x}\,\text{d}x\right)=-3\left(\int \frac{1}{{sin}^{2}⁡x}({tan}^{2}⁡x-{sin}^{3}⁡x)\text{d}x\right)
$$

We then use the fact that ${tan}^{2}⁡x=\frac{{sin}^{2}⁡x}{{cos}^{2}⁡x}$ to express this as

$$
-3\left(\int \frac{1}{{sin}^{2}⁡x}(\frac{{sin}^{2}⁡x}{{cos}^{2}⁡x}-{sin}^{3}⁡x)\text{d}x\right)
$$

Therefore,

$$
\begin{aligned}-3\left(\int \frac{{tan}^{2}⁡x-{sin}^{3}⁡x}{{sin}^{2}⁡x}\,\text{d}x\right)& =-3\left(\int \frac{1}{{sin}^{2}⁡x}(\frac{{sin}^{2}⁡x}{{cos}^{2}⁡x}-{sin}^{3}⁡x)\text{d}x\right)\\  & =-3\left(\int (\frac{1}{{sin}^{2}⁡x}\cdot \frac{{sin}^{2}⁡x}{{cos}^{2}⁡x}-\frac{1}{{sin}^{2}⁡x}\cdot {sin}^{3}⁡x)\text{d}x\right)\\  & =-3\left(\int (\frac{1}{{cos}^{2}⁡x}-\operatorname{sin}⁡x)\text{d}x\right)\\  & =-3\left(\int ({sec}^{2}⁡x-\operatorname{sin}⁡x)\text{d}x\right)\\  & =-3\left(\operatorname{tan}⁡x-(-\operatorname{cos}⁡x)\right)+C\\  & =-3\left(\operatorname{tan}⁡x+\operatorname{cos}⁡x\right)+C\end{aligned}
$$

## q-73365

Original

Calculate ${\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x.$

- $\frac{\sqrt{2}-1}{2}$
- $\frac{\sqrt{3}}{3}$ (correct)
- $\frac{2\sqrt{3}}{3}$
- $\frac{\sqrt{2}}{2}$
- $\frac{\sqrt{3}-1}{3}$

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

Normal variant

Calculate $-3\left({\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right).$

{{selection}}

- $\frac{3}{2} - \frac{3 \sqrt{2}}{2}$
- $- \sqrt{3}$ (correct)
- $- 2 \sqrt{3}$
- $- \frac{3 \sqrt{2}}{2}$
- $1 - \sqrt{3}$

We can write the integral as

$$
-3\left({\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)=-3\left({\int }_{0}^{\pi /6}(1-{tan}^{2}⁡x)\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)
$$

Then, we use the fact that $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}$ as follows:

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /6}(1-{tan}^{2}⁡x)\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)& =-3\left({\int }_{0}^{\pi /6}(1-\frac{{sin}^{2}⁡x}{{cos}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)\\  & =-3\left({\int }_{0}^{\pi /6}(\frac{{cos}^{2}⁡x-{sin}^{2}⁡x}{{cos}^{2}⁡x})\cdot \frac{1}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)\\  & =-3\left({\int }_{0}^{\pi /6}\frac{1}{{cos}^{2}⁡x}\,\text{d}x\right)\end{aligned}
$$

Now we use the fact that $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x$ to express this as

$$
-3\left({\int }_{0}^{\pi /6}{sec}^{2}⁡x\text{d}x\right)
$$

Hence,

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /6}\frac{1-{tan}^{2}⁡x}{{cos}^{2}⁡x-{sin}^{2}⁡x}\,\text{d}x\right)& =-3\left({\int }_{0}^{\pi /6}{sec}^{2}⁡x\text{d}x\right)\\  & =-3\left(\operatorname{tan}⁡x{|}_{0}^{\pi /6}\right)\\  & =-3\left(\operatorname{tan}⁡(\frac{\pi }{6})-\operatorname{tan}⁡0\right)\\  & =-3\left(\frac{\sqrt{3}}{3}-0\right)\\  & =-3\left(\frac{\sqrt{3}}{3}\right)\end{aligned}
$$

## q-352711

Original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /6}\frac{\operatorname{sin}⁡x}{{cos}^{2}⁡x}\,\text{d}x=$
{{field-1}}

- $\frac{2\sqrt{3}}{3}-1$ (correct)

We use the identities $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x$ and $\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}=\operatorname{tan}⁡x,$ as follows:

$$
\begin{aligned}{\int }_{0}^{\pi /6}\frac{\operatorname{sin}⁡x}{{cos}^{2}⁡x}\text{d}x & ={\int }_{0}^{\pi /6}\frac{1}{\operatorname{cos}⁡x}\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x \\  & ={\int }_{0}^{\pi /6}\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x \\  & =\operatorname{sec}⁡x{|}_{0}^{\pi /6} \\  & =(\operatorname{sec}⁡(\frac{\pi }{6})-\operatorname{sec}⁡(0)) \\  & =\frac{2}{\sqrt{3}}-1\end{aligned}
$$

Normal variant

Evaluate the following integral. Do not round the answer.

$-3\left({\int }_{0}^{\pi /6}\frac{\operatorname{sin}⁡x}{{cos}^{2}⁡x}\,\text{d}x\right)=$
{{field-1}}

- $3 - 2 \sqrt{3}$ (correct)

We use the identities $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x$ and $\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}=\operatorname{tan}⁡x,$ as follows:

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /6}\frac{\operatorname{sin}⁡x}{{cos}^{2}⁡x}\text{d}x\right)& =-3\left({\int }_{0}^{\pi /6}\frac{1}{\operatorname{cos}⁡x}\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x\right)\\  & =-3\left({\int }_{0}^{\pi /6}\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x\right)\\  & =-3\left(\operatorname{sec}⁡x{|}_{0}^{\pi /6}\right)\\  & =-3\left((\operatorname{sec}⁡(\frac{\pi }{6})-\operatorname{sec}⁡(0))\right)\\  & =-3\left(\frac{2}{\sqrt{3}}-1\right)\end{aligned}
$$

## q-114319

Original

${\int }_{0}^{\pi /3}\frac{\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\,\text{d}x=$

- $0$
- $1$
- $\frac{1}{4}$
- $\frac{3}{4}$
- $\frac{1}{2}$ (correct)

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

Normal variant

$-3\left({\int }_{0}^{\pi /3}\frac{\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\,\text{d}x\right)=$

{{selection}}

- $0$
- $-3$
- $- \frac{3}{4}$
- $- \frac{9}{4}$
- $- \frac{3}{2}$ (correct)

We can write the integral as

$$
-3\left({\int }_{0}^{\pi /3}\frac{\operatorname{tan}⁡x}{\operatorname{sec}⁡x}\,\text{d}x\right)=-3\left({\int }_{0}^{\pi /3}\frac{1}{\operatorname{sec}⁡x}\cdot \operatorname{tan}⁡x\,\text{d}x\right)
$$

We then use the fact that $\operatorname{sec}⁡x=\frac{1}{\operatorname{cos}⁡x}$ and $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}$ to express this as

$$
-3\left({\int }_{0}^{\pi /3}\operatorname{cos}⁡x\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x\right)
$$

Therefore,

$$
\begin{aligned}-3\left({\int }_{0}^{\pi /3}\frac{1}{\operatorname{sec}⁡x}\cdot \operatorname{tan}⁡x\,\text{d}x\right)& =-3\left({\int }_{0}^{\pi /3}\operatorname{cos}⁡x\cdot \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x\right)\\  & =-3\left({\int }_{0}^{\pi /3}\operatorname{sin}⁡x\,\text{d}x\right)\\  & =-3\left(-\operatorname{cos}⁡x\,{|}_{0}^{\pi /3}\right)\\  & =-3\left(-[\operatorname{cos}⁡(\frac{\pi }{3})-\operatorname{cos}⁡0]\right)\\  & =-3\left(-[\frac{1}{2}-1]\right)\\  & =-3\left(\frac{1}{2}\right)\end{aligned}
$$

## q-73357

Original

Calculate ${\int }_{\pi /12}^{\pi /4}\frac{\operatorname{cot}⁡3x}{\operatorname{csc}⁡3x}\,\text{d}x.$

- $2\frac{\sqrt{2}}{3}$
- $\frac{\sqrt{3}}{3}$
- $\frac{\sqrt{3}}{2}$
- $\frac{\sqrt{2}}{3}$
- $0$ (correct)

We can write the integral as

$$
{\int }_{\pi /12}^{\pi /4}\frac{\operatorname{cot}⁡3x}{\operatorname{csc}⁡3x}\,\text{d}x={\int }_{\pi /12}^{\pi /4}\operatorname{cot}⁡3x\cdot \frac{1}{\operatorname{csc}⁡3x}\,\text{d}x
$$

Then, we use the fact that $\operatorname{cot}⁡3x=\frac{\operatorname{cos}⁡3x}{\operatorname{sin}⁡3x}$ and $\frac{1}{\operatorname{sin}⁡3x}=\operatorname{csc}⁡3x$ as follows:

$$
\begin{aligned}{\int }_{\pi /12}^{\pi /4}\frac{\operatorname{cos}⁡3x}{\operatorname{sin}⁡3x}\cdot \operatorname{sin}⁡3x\,\text{d}x={\int }_{\pi /12}^{\pi /4}\operatorname{cos}⁡3x\,\text{d}x\end{aligned}
$$

We can solve this by substitution. Let $u=3x.$ Then $\text{d}x=\frac{1}{3}\text{d}u.$ 

Now, we fill the table for the limits of integration, according to the rule $u=3x.$

| $x$ | $\frac{\pi }{12}$ | $\frac{\pi }{4}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi }{4}$ | $\frac{3\pi }{4}$ |

Therefore, the integral in terms of the new variable is

$$
\begin{aligned}\begin{aligned}{\int }_{\pi /12}^{\pi /4}\operatorname{cos}⁡3x\,\text{d}x & ={\int }_{\pi /4}^{3\pi /4}\operatorname{cos}⁡u\,\cdot \frac{1}{3}\text{d}u \\  & =\frac{1}{3}{\int }_{\pi /4}^{3\pi /4}\operatorname{cos}⁡u\,\text{d}u \\  & =\frac{1}{3}\operatorname{sin}⁡u{|}_{\pi /4}^{3\pi /4} \\  & =\frac{1}{3}(\operatorname{sin}⁡(\frac{3\pi }{4})-\operatorname{sin}⁡(\frac{\pi }{4})) \\  & =\frac{1}{3}(\frac{\sqrt{2}}{2}-\frac{\sqrt{2}}{2}) \\  & =0.\end{aligned}\end{aligned}
$$

Normal variant

Calculate $-3\left({\int }_{\pi /12}^{\pi /4}\frac{\operatorname{cot}⁡3x}{\operatorname{csc}⁡3x}\,\text{d}x\right).$

{{selection}}

- $- 2 \sqrt{2}$
- $- \sqrt{3}$
- $- \frac{3 \sqrt{3}}{2}$
- $- \sqrt{2}$
- $0$ (correct)

We can write the integral as

$$
-3\left({\int }_{\pi /12}^{\pi /4}\frac{\operatorname{cot}⁡3x}{\operatorname{csc}⁡3x}\,\text{d}x\right)=-3\left({\int }_{\pi /12}^{\pi /4}\operatorname{cot}⁡3x\cdot \frac{1}{\operatorname{csc}⁡3x}\,\text{d}x\right)
$$

Then, we use the fact that $\operatorname{cot}⁡3x=\frac{\operatorname{cos}⁡3x}{\operatorname{sin}⁡3x}$ and $\frac{1}{\operatorname{sin}⁡3x}=\operatorname{csc}⁡3x$ as follows:

$$
\begin{aligned}-3\left({\int }_{\pi /12}^{\pi /4}\frac{\operatorname{cos}⁡3x}{\operatorname{sin}⁡3x}\cdot \operatorname{sin}⁡3x\,\text{d}x\right)&=-3\left({\int }_{\pi /12}^{\pi /4}\operatorname{cos}⁡3x\,\text{d}x\right)\end{aligned}
$$

We can solve this by substitution. Let $u=3x.$ Then $\text{d}x=\frac{1}{3}\text{d}u.$ 

Now, we fill the table for the limits of integration, according to the rule $u=3x.$

| $x$ | $\frac{\pi }{12}$ | $\frac{\pi }{4}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi }{4}$ | $\frac{3\pi }{4}$ |

Therefore, the integral in terms of the new variable is

$$
\begin{aligned}-3\left({\int }_{\pi /12}^{\pi /4}\operatorname{cos}⁡3x\,\text{d}x\right)& =-3\left({\int }_{\pi /4}^{3\pi /4}\operatorname{cos}⁡u\,\cdot \frac{1}{3}\text{d}u\right)\\  & =-3\left(\frac{1}{3}{\int }_{\pi /4}^{3\pi /4}\operatorname{cos}⁡u\,\text{d}u\right)\\  & =-3\left(\frac{1}{3}\operatorname{sin}⁡u{|}_{\pi /4}^{3\pi /4}\right)\\  & =-3\left(\frac{1}{3}(\operatorname{sin}⁡(\frac{3\pi }{4})-\operatorname{sin}⁡(\frac{\pi }{4}))\right)\\  & =-3\left(\frac{1}{3}(\frac{\sqrt{2}}{2}-\frac{\sqrt{2}}{2})\right)\\  & =-3\left(0\right)\end{aligned}
$$

## authored-h-cos-cot a=1, b=1

Evaluate the following integral. Do not round the answer.

$\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{\cos^{3}{\left(x \right)} + \cot^{2}{\left(x \right)}}{\cos^{2}{\left(x \right)}}\,\text{d}x=$
{{field-1}}

- $- \frac{3}{2} + \frac{\sqrt{2}}{2} + \sqrt{3}$ (correct)

We use the identity $\cot^2x=\frac{\cos^2x}{\sin^2x}$ to rewrite the quotient, distribute, and recognize standard trigonometric integrals. Therefore,

$$
\begin{aligned}\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{\cos^{3}{\left(x \right)} + \cot^{2}{\left(x \right)}}{\cos^{2}{\left(x \right)}}\,\text{d}x &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{\cos^{3}{\left(x \right)} + \frac{\cos^{2}{\left(x \right)}}{\sin^{2}{\left(x \right)}}}{\cos^{2}{\left(x \right)}}\,\text{d}x \\ &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \cos{\left(x \right)} + \frac{1}{\sin^{2}{\left(x \right)}}\,\text{d}x \\ &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \cos{\left(x \right)} + \csc^{2}{\left(x \right)}\,\text{d}x \\ &=\left(\sin{\left(x \right)} - \cot{\left(x \right)}\right)|_{\frac{\pi}{6}}^{\frac{\pi}{4}} \\ &=\left(-1 + \frac{\sqrt{2}}{2}\right)-\left(\frac{1}{2} - \sqrt{3}\right) \\ &=- \frac{3}{2} + \frac{\sqrt{2}}{2} + \sqrt{3}\end{aligned}
$$

## authored-h-cos-cot a=1, b=-3

Evaluate the following integral. Do not round the answer.

$\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{\cos^{3}{\left(x \right)} - 3 \cot^{2}{\left(x \right)}}{\cos^{2}{\left(x \right)}}\,\text{d}x=$
{{field-1}}

- $- 3 \sqrt{3} + \frac{\sqrt{2}}{2} + \frac{5}{2}$ (correct)

We use the identity $\cot^2x=\frac{\cos^2x}{\sin^2x}$ to rewrite the quotient, distribute, and recognize standard trigonometric integrals. Therefore,

$$
\begin{aligned}\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{\cos^{3}{\left(x \right)} - 3 \cot^{2}{\left(x \right)}}{\cos^{2}{\left(x \right)}}\,\text{d}x &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{\cos^{3}{\left(x \right)} - \frac{3 \cos^{2}{\left(x \right)}}{\sin^{2}{\left(x \right)}}}{\cos^{2}{\left(x \right)}}\,\text{d}x \\ &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \cos{\left(x \right)} - \frac{3}{\sin^{2}{\left(x \right)}}\,\text{d}x \\ &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \cos{\left(x \right)} - 3 \csc^{2}{\left(x \right)}\,\text{d}x \\ &=\left(\sin{\left(x \right)} + 3 \cot{\left(x \right)}\right)|_{\frac{\pi}{6}}^{\frac{\pi}{4}} \\ &=\left(\frac{\sqrt{2}}{2} + 3\right)-\left(\frac{1}{2} + 3 \sqrt{3}\right) \\ &=- 3 \sqrt{3} + \frac{\sqrt{2}}{2} + \frac{5}{2}\end{aligned}
$$

## authored-h-cos-cot a=-4, b=1

Evaluate the following integral. Do not round the answer.

$\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{- 4 \cos^{3}{\left(x \right)} + \cot^{2}{\left(x \right)}}{\cos^{2}{\left(x \right)}}\,\text{d}x=$
{{field-1}}

- $- 2 \sqrt{2} + 1 + \sqrt{3}$ (correct)

We use the identity $\cot^2x=\frac{\cos^2x}{\sin^2x}$ to rewrite the quotient, distribute, and recognize standard trigonometric integrals. Therefore,

$$
\begin{aligned}\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{- 4 \cos^{3}{\left(x \right)} + \cot^{2}{\left(x \right)}}{\cos^{2}{\left(x \right)}}\,\text{d}x &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{- 4 \cos^{3}{\left(x \right)} + \frac{\cos^{2}{\left(x \right)}}{\sin^{2}{\left(x \right)}}}{\cos^{2}{\left(x \right)}}\,\text{d}x \\ &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} - 4 \cos{\left(x \right)} + \frac{1}{\sin^{2}{\left(x \right)}}\,\text{d}x \\ &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} - 4 \cos{\left(x \right)} + \csc^{2}{\left(x \right)}\,\text{d}x \\ &=\left(- 4 \sin{\left(x \right)} - \cot{\left(x \right)}\right)|_{\frac{\pi}{6}}^{\frac{\pi}{4}} \\ &=\left(- 2 \sqrt{2} - 1\right)-\left(-2 - \sqrt{3}\right) \\ &=- 2 \sqrt{2} + 1 + \sqrt{3}\end{aligned}
$$

## authored-h-tan-sin a=1, b=1

Evaluate the following integral. Do not round the answer.

$\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{- \sin^{3}{\left(x \right)} + \tan^{2}{\left(x \right)}}{\sin^{2}{\left(x \right)}}\,\text{d}x=$
{{field-1}}

- $- \frac{5 \sqrt{3}}{6} + \frac{\sqrt{2}}{2} + 1$ (correct)

We use the identity $\tan^2x=\frac{\sin^2x}{\cos^2x}$ to rewrite the quotient, distribute, and recognize standard trigonometric integrals. Therefore,

$$
\begin{aligned}\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{- \sin^{3}{\left(x \right)} + \tan^{2}{\left(x \right)}}{\sin^{2}{\left(x \right)}}\,\text{d}x &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{- \sin^{3}{\left(x \right)} + \frac{\sin^{2}{\left(x \right)}}{\cos^{2}{\left(x \right)}}}{\sin^{2}{\left(x \right)}}\,\text{d}x \\ &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} - \sin{\left(x \right)} + \frac{1}{\cos^{2}{\left(x \right)}}\,\text{d}x \\ &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} - \sin{\left(x \right)} + \sec^{2}{\left(x \right)}\,\text{d}x \\ &=\left(\cos{\left(x \right)} + \tan{\left(x \right)}\right)|_{\frac{\pi}{6}}^{\frac{\pi}{4}} \\ &=\left(\frac{\sqrt{2}}{2} + 1\right)-\left(\frac{5 \sqrt{3}}{6}\right) \\ &=- \frac{5 \sqrt{3}}{6} + \frac{\sqrt{2}}{2} + 1\end{aligned}
$$

## authored-h-tan-sin a=1, b=-3

Evaluate the following integral. Do not round the answer.

$\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{3 \sin^{3}{\left(x \right)} + \tan^{2}{\left(x \right)}}{\sin^{2}{\left(x \right)}}\,\text{d}x=$
{{field-1}}

- $- \frac{3 \sqrt{2}}{2} + 1 + \frac{7 \sqrt{3}}{6}$ (correct)

We use the identity $\tan^2x=\frac{\sin^2x}{\cos^2x}$ to rewrite the quotient, distribute, and recognize standard trigonometric integrals. Therefore,

$$
\begin{aligned}\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{3 \sin^{3}{\left(x \right)} + \tan^{2}{\left(x \right)}}{\sin^{2}{\left(x \right)}}\,\text{d}x &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{3 \sin^{3}{\left(x \right)} + \frac{\sin^{2}{\left(x \right)}}{\cos^{2}{\left(x \right)}}}{\sin^{2}{\left(x \right)}}\,\text{d}x \\ &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} 3 \sin{\left(x \right)} + \frac{1}{\cos^{2}{\left(x \right)}}\,\text{d}x \\ &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} 3 \sin{\left(x \right)} + \sec^{2}{\left(x \right)}\,\text{d}x \\ &=\left(- 3 \cos{\left(x \right)} + \tan{\left(x \right)}\right)|_{\frac{\pi}{6}}^{\frac{\pi}{4}} \\ &=\left(1 - \frac{3 \sqrt{2}}{2}\right)-\left(- \frac{7 \sqrt{3}}{6}\right) \\ &=- \frac{3 \sqrt{2}}{2} + 1 + \frac{7 \sqrt{3}}{6}\end{aligned}
$$

## authored-h-tan-sin a=-4, b=1

Evaluate the following integral. Do not round the answer.

$\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{- \sin^{3}{\left(x \right)} - 4 \tan^{2}{\left(x \right)}}{\sin^{2}{\left(x \right)}}\,\text{d}x=$
{{field-1}}

- $-4 + \frac{\sqrt{2}}{2} + \frac{5 \sqrt{3}}{6}$ (correct)

We use the identity $\tan^2x=\frac{\sin^2x}{\cos^2x}$ to rewrite the quotient, distribute, and recognize standard trigonometric integrals. Therefore,

$$
\begin{aligned}\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{- \sin^{3}{\left(x \right)} - 4 \tan^{2}{\left(x \right)}}{\sin^{2}{\left(x \right)}}\,\text{d}x &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} \frac{- \sin^{3}{\left(x \right)} - \frac{4 \sin^{2}{\left(x \right)}}{\cos^{2}{\left(x \right)}}}{\sin^{2}{\left(x \right)}}\,\text{d}x \\ &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} - \sin{\left(x \right)} - \frac{4}{\cos^{2}{\left(x \right)}}\,\text{d}x \\ &=\int_{\frac{\pi}{6}}^{\frac{\pi}{4}} - \sin{\left(x \right)} - 4 \sec^{2}{\left(x \right)}\,\text{d}x \\ &=\left(\cos{\left(x \right)} - 4 \tan{\left(x \right)}\right)|_{\frac{\pi}{6}}^{\frac{\pi}{4}} \\ &=\left(-4 + \frac{\sqrt{2}}{2}\right)-\left(- \frac{5 \sqrt{3}}{6}\right) \\ &=-4 + \frac{\sqrt{2}}{2} + \frac{5 \sqrt{3}}{6}\end{aligned}
$$
