## q-2622 exact original

Calculate $\int \operatorname{tan}⁡x\sqrt{\operatorname{cos}⁡x}\,\text{d}x.$

Field selection (radio)

- $\frac{1}{2\sqrt{\operatorname{cos}⁡x}}+C$
- $2\sqrt{\operatorname{sin}⁡x}+C$
- $-2\sqrt{\operatorname{tan}⁡x}+C$
- $-\frac{1}{2\sqrt{\operatorname{cos}⁡x}}+C$
- $-2\sqrt{\operatorname{cos}⁡x}+C$ (correct)

We use the identity $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}$ and rewrite the integral as

$$
\int \operatorname{tan}⁡x\,\sqrt{\operatorname{cos}⁡x}\,\text{d}x=\int \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\sqrt{\operatorname{cos}⁡x}\,\text{d}x.
$$

We can solve this by substitution. Let $u=\operatorname{cos}⁡x.$ Then

$$
\frac{\text{d}u}{\text{d}x}=-\operatorname{sin}⁡x\,⟹\,-\text{d}u=\operatorname{sin}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \operatorname{tan}⁡x\,\sqrt{\operatorname{cos}⁡x}\,\text{d}x & =\int \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\sqrt{\operatorname{cos}⁡x}\,\text{d}x \\  & =\int \frac{\sqrt{\operatorname{cos}⁡x}}{\operatorname{cos}⁡x}\cdot \operatorname{sin}⁡x\,\text{d}x \\  & =\int \frac{1}{\sqrt{\operatorname{cos}⁡x}}\cdot \operatorname{sin}⁡x\,\text{d}x \\  & =\int \frac{1}{\sqrt{u}}\cdot (-\text{d}u) \\  & =-\int \frac{1}{\sqrt{u}}\cdot \text{d}u \\  & =-2\sqrt{u}+C \\  & =-2\sqrt{\operatorname{cos}⁡x}+C\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

Calculate $3\cdot \int \operatorname{tan}⁡{2x}\sqrt{\operatorname{cos}⁡{2x}}\,\text{d}x.$

Field selection (radio)

- $\frac{3}{4 \sqrt{\cos{\left(2 x \right)}}}+C$
- $3 \sqrt{\sin{\left(2 x \right)}}+C$
- $- 3 \sqrt{\tan{\left(2 x \right)}}+C$
- $- \frac{3}{4 \sqrt{\cos{\left(2 x \right)}}}+C$
- $- 3 \sqrt{\cos{\left(2 x \right)}}+C$ (correct)

We use the identity $\operatorname{tan}⁡{2x}=\frac{\operatorname{sin}⁡{2x}}{\operatorname{cos}⁡{2x}}$ and rewrite the integral as

$$
3\cdot \int \operatorname{tan}⁡{2x}\,\sqrt{\operatorname{cos}⁡{2x}}\,\text{d}x = 3\cdot \int \frac{\operatorname{sin}⁡{2x}}{\operatorname{cos}⁡{2x}}\,\sqrt{\operatorname{cos}⁡{2x}}\,\text{d}x.
$$

We can solve this by substitution. Let $u=\operatorname{cos}⁡{2x}.$ Then

$$
\frac{\text{d}u}{\text{d}x}=2\left(-\operatorname{sin}⁡{2x}\right)\,⟹\,\frac{1}{2}\left(-\text{d}u\right)=\operatorname{sin}⁡{2x}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}3\cdot \int \operatorname{tan}⁡{2x}\,\sqrt{\operatorname{cos}⁡{2x}}\,\text{d}x &=3\cdot \int \frac{\operatorname{sin}⁡{2x}}{\operatorname{cos}⁡{2x}}\,\sqrt{\operatorname{cos}⁡{2x}}\,\text{d}x \\  &=3\cdot \int \frac{\sqrt{\operatorname{cos}⁡{2x}}}{\operatorname{cos}⁡{2x}}\cdot \operatorname{sin}⁡{2x}\,\text{d}x \\  &=3\cdot \int \frac{1}{\sqrt{\operatorname{cos}⁡{2x}}}\cdot \operatorname{sin}⁡{2x}\,\text{d}x \\  &=\frac{3}{2}\cdot \int \frac{1}{\sqrt{u}}\cdot (-\text{d}u) \\  &=\frac{3}{2}\cdot -\int \frac{1}{\sqrt{u}}\cdot \text{d}u \\  &=\frac{3}{2}\left(-2\sqrt{u}\right)+C \\  &=\frac{3}{2}\left(-2\sqrt{\operatorname{cos}⁡{2x}}\right)+C\end{aligned}
$$

## q-49259 exact original

$\int \operatorname{cot}⁡x\,\text{d}x=$

Field selection (radio)

- $\operatorname{ln}⁡|x|+C$
- $\operatorname{csc}⁡(\operatorname{ln}⁡|x|)+C$
- $\operatorname{ln}⁡|\operatorname{csc}⁡x|+C$
- $\operatorname{sin}⁡(\operatorname{ln}⁡|x|)+C$
- $\operatorname{ln}⁡|\operatorname{sin}⁡x|+C$ (correct)

We use the identity $\operatorname{cot}⁡x=\frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}$ and rewrite the integral as

$$
\int \operatorname{cot}⁡x\,\text{d}x=\int \frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}\,\text{d}x.
$$

We can solve this by substitution. Let $u=\operatorname{sin}⁡x.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=\operatorname{cos}⁡x\,⟹\,\text{d}u=\operatorname{cos}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{\operatorname{cos}⁡x}{\operatorname{sin}⁡x}\,\text{d}x & =\int \frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|+C \\  & =\operatorname{ln}⁡|\operatorname{sin}⁡x|+C.\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

$3\cdot \int \operatorname{cot}⁡{2x}\,\text{d}x=$

Field selection (radio)

- $\frac{3 \log{\left(2 \left|{x}\right| \right)}}{2}+C$
- $\frac{3 \csc{\left(\log{\left(2 \left|{x}\right| \right)} \right)}}{2}+C$
- $\frac{3 \log{\left(\left|{\csc{\left(2 x \right)}}\right| \right)}}{2}+C$
- $\frac{3 \sin{\left(\log{\left(2 \left|{x}\right| \right)} \right)}}{2}+C$
- $\frac{3 \log{\left(\left|{\sin{\left(2 x \right)}}\right| \right)}}{2}+C$ (correct)

We use the identity $\operatorname{cot}⁡{2x}=\frac{\operatorname{cos}⁡{2x}}{\operatorname{sin}⁡{2x}}$ and rewrite the integral as

$$
3\cdot \int \operatorname{cot}⁡{2x}\,\text{d}x = 3\cdot \int \frac{\operatorname{cos}⁡{2x}}{\operatorname{sin}⁡{2x}}\,\text{d}x.
$$

We can solve this by substitution. Let $u=\operatorname{sin}⁡{2x}.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(\operatorname{cos}⁡{2x}\right)\,⟹\,\frac{1}{2}\left(\text{d}u\right)=\operatorname{cos}⁡{2x}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}3\cdot \int \frac{\operatorname{cos}⁡{2x}}{\operatorname{sin}⁡{2x}}\,\text{d}x &=\frac{3}{2}\cdot \int \frac{1}{u}\,\text{d}u \\  &=\frac{3}{2}\left(\operatorname{ln}⁡|u|\right)+C \\  &=\frac{3}{2}\left(\operatorname{ln}⁡|\operatorname{sin}⁡{2x}|\right)+C.\end{aligned}
$$

## q-114294 exact original (ineligible raw operator capture)

$\int \operatorname{tan}⁡x{sec}^{3}⁡x\,\text{d}x=$

Field selection (radio)

- $\frac{1}{3}{sec}^{3}⁡x+C$ (correct)
- ${sec}^{2}⁡x+C$
- $3{sec}^{3}⁡x+C$
- $-3{csc}^{3}⁡x+C$
- $\frac{1}{3}{csc}^{3}⁡x+C$

We use the identities $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}$ and $\operatorname{sec}⁡x=\frac{1}{\operatorname{cos}⁡x}$ and rewrite the integral as

$$
\begin{aligned}\int \operatorname{tan}⁡x{sec}^{3}⁡x\,\text{d}x & =\int \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\cdot {(\frac{1}{\operatorname{cos}⁡x})}^{3}\,\text{d}x \\  & =\int \frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\cdot \frac{1}{{cos}^{3}⁡x}\,\text{d}x \\  & =\int \frac{\operatorname{sin}⁡x}{{cos}^{4}⁡x}\,\text{d}x.\end{aligned}
$$

We can solve this by substitution. Let $u=\operatorname{cos}⁡x.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=-\operatorname{sin}⁡x\,⟹\,-\text{d}u=\operatorname{sin}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{\operatorname{sin}⁡x}{{cos}^{4}⁡x}\,\text{d}x & =\int \frac{1}{{u}^{4}}\,(-\text{d}u) \\  & =-\int \frac{1}{{u}^{4}}\,\text{d}u \\  & =\frac{1}{3{u}^{3}}+C \\  & =\frac{1}{3{cos}^{3}⁡x}+C \\  & =\frac{1}{3}{sec}^{3}⁡x+C\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

$3\cdot \int \operatorname{tan}⁡{2x}\operatorname{sec}^{3}⁡{2x}\,\text{d}x=$

Field selection (radio)

- $\frac{\sec^{3}{\left(2 x \right)}}{2}+C$ (correct)
- $\frac{3 \sec^{2}{\left(2 x \right)}}{2}+C$
- $\frac{9 \sec^{3}{\left(2 x \right)}}{2}+C$
- $- \frac{9 \csc^{3}{\left(2 x \right)}}{2}+C$
- $\frac{\csc^{3}{\left(2 x \right)}}{2}+C$

We use the identities $\operatorname{tan}⁡{2x}=\frac{\operatorname{sin}⁡{2x}}{\operatorname{cos}⁡{2x}}$ and $\operatorname{sec}⁡{2x}=\frac{1}{\operatorname{cos}⁡{2x}}$ and rewrite the integral as

$$
\begin{aligned}3\cdot \int \operatorname{tan}⁡{2x}\operatorname{sec}^{3}⁡{2x}\,\text{d}x &=3\cdot \int \frac{\operatorname{sin}⁡{2x}}{\operatorname{cos}⁡{2x}}\cdot {(\frac{1}{\operatorname{cos}⁡{2x}})}^{3}\,\text{d}x \\  &=3\cdot \int \frac{\operatorname{sin}⁡{2x}}{\operatorname{cos}⁡{2x}}\cdot \frac{1}{\operatorname{cos}^{3}⁡{2x}}\,\text{d}x \\  &=3\cdot \int \frac{\operatorname{sin}⁡{2x}}{\operatorname{cos}^{4}⁡{2x}}\,\text{d}x.\end{aligned}
$$

We can solve this by substitution. Let $u=\operatorname{cos}⁡{2x}.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(-\operatorname{sin}⁡{2x}\right)\,⟹\,\frac{1}{2}\left(-\text{d}u\right)=\operatorname{sin}⁡{2x}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}3\cdot \int \frac{\operatorname{sin}⁡{2x}}{\operatorname{cos}^{4}⁡{2x}}\,\text{d}x &=\frac{3}{2}\cdot \int \frac{1}{{u}^{4}}\,(-\text{d}u) \\  &=\frac{3}{2}\cdot -\int \frac{1}{{u}^{4}}\,\text{d}u \\  &=\frac{3}{2}\left(\frac{1}{3{u}^{3}}\right)+C \\  &=\frac{3}{2}\left(\frac{1}{3\operatorname{cos}^{3}⁡{2x}}\right)+C \\  &=\frac{3}{2}\left(\frac{1}{3}\operatorname{sec}^{3}⁡{2x}\right)+C\end{aligned}
$$

## q-347941 exact original (ineligible raw operator capture)

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /9}^{\pi /6}\frac{3\operatorname{cos}⁡(3x)}{{sin}^{2}⁡(3x)}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{2\sqrt{3}}{3}-1$ (correct)

We can solve this by substitution. Let $u=\operatorname{sin}⁡3x.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=3\operatorname{cos}⁡3x\,⟹\,\text{d}u=3\operatorname{cos}⁡3x\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{sin}⁡3x.$

| $x$ | $\frac{\pi }{9}$ | $\frac{\pi }{6}$ |
| --- | --- | --- |
| $u$ | $\frac{\sqrt{3}}{2}$ | $1$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{\pi /9}^{\pi /6}\frac{3\operatorname{cos}⁡(3x)}{{sin}^{2}⁡(3x)}\,\text{d}x & ={\int }_{\sqrt{3}/2}^{1}\frac{1}{{u}^{2}}\,\text{d}u \\  & =-\frac{1}{u}{|}_{\sqrt{3}/2}^{1} \\  & =-(\frac{1}{1}-\frac{2}{\sqrt{3}}) \\  & =\frac{2\sqrt{3}}{3}-1\end{aligned}\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

Evaluate the following integral. Do not round the answer.

$3\cdot \int_{\frac{\pi}{18}}^{\frac{\pi}{12}}\frac{3\operatorname{cos}⁡({6x})}{\operatorname{sin}^{2}⁡({6x})}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $- \frac{3}{2} + \sqrt{3}$ (correct)

We can solve this by substitution. Let $u=\operatorname{sin}⁡{6x}.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(3\operatorname{cos}⁡{6x}\right)\,⟹\,\frac{1}{2}\left(\text{d}u\right)=3\operatorname{cos}⁡{6x}\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{sin}⁡{6x}.$

| $x$ | $\frac{\pi}{18}$ | $\frac{\pi}{12}$ |
| --- | --- | --- |
| $u$ | $\frac{\sqrt{3}}{2}$ | $1$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}3\cdot \int_{\frac{\pi}{18}}^{\frac{\pi}{12}}\frac{3\operatorname{cos}⁡({6x})}{\operatorname{sin}^{2}⁡({6x})}\,\text{d}x &=\frac{3}{2}\cdot {\int }_{\sqrt{3}/2}^{1}\frac{1}{{u}^{2}}\,\text{d}u \\  &=\frac{3}{2}\left(-\frac{1}{u}{|}_{\sqrt{3}/2}^{1}\right) \\  &=\frac{3}{2}\left(-(\frac{1}{1}-\frac{2}{\sqrt{3}})\right) \\  &=\frac{3}{2}\left(\frac{2\sqrt{3}}{3}-1\right)\end{aligned}\end{aligned}
$$

## q-352786 exact original (ineligible raw operator capture)

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /3}{sec}^{3}\,x\,\operatorname{tan}⁡x\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{7}{3}$ (correct)

We can solve this by substitution. Let $u=\operatorname{sec}⁡x.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=\operatorname{sec}⁡x\,\operatorname{tan}⁡x\,⟹\,\text{d}u=\operatorname{sec}⁡x\,\operatorname{tan}⁡x\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{sec}⁡x.$

| $x$ | $0$ | $\frac{\pi }{3}$ |
| --- | --- | --- |
| $u$ | $1$ | $2$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{0}^{\pi /3}{sec}^{3}\,x\,\operatorname{tan}⁡x\,\text{d}x & ={\int }_{0}^{\pi /3}{sec}^{2}\,x\cdot \operatorname{sec}⁡x\,\operatorname{tan}⁡x\,\text{d}x \\  & ={\int }_{1}^{2}{u}^{2}\,\text{d}u \\  & =\frac{{u}^{3}}{3}{|}_{1}^{2} \\  & =\frac{1}{3}({2}^{3}-{1}^{3}) \\  & =\frac{1}{3}(8-1) \\  & =\frac{7}{3}\end{aligned}\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

Evaluate the following integral. Do not round the answer.

$3\cdot \int_{0}^{\frac{\pi}{6}}\operatorname{sec}^{3}\,{2x}\,\operatorname{tan}⁡{2x}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{7}{2}$ (correct)

We can solve this by substitution. Let $u=\operatorname{sec}⁡{2x}.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(\operatorname{sec}⁡{2x}\operatorname{tan}⁡{2x}\right)\,⟹\,\frac{1}{2}\left(\text{d}u\right)=\operatorname{sec}⁡{2x}\,\operatorname{tan}⁡{2x}\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{sec}⁡{2x}.$

| $x$ | $0$ | $\frac{\pi}{6}$ |
| --- | --- | --- |
| $u$ | $1$ | $2$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}3\cdot \int_{0}^{\frac{\pi}{6}}\operatorname{sec}^{3}\,{2x}\,\operatorname{tan}⁡{2x}\,\text{d}x &=3\cdot \int_{0}^{\frac{\pi}{6}}\operatorname{sec}^{2}\,{2x}\cdot \operatorname{sec}⁡{2x}\,\operatorname{tan}⁡{2x}\,\text{d}x \\  &=\frac{3}{2}\cdot {\int }_{1}^{2}{u}^{2}\,\text{d}u \\  &=\frac{3}{2}\left(\frac{{u}^{3}}{3}{|}_{1}^{2}\right) \\  &=\frac{3}{2}\left(\frac{1}{3}({2}^{3}-{1}^{3})\right) \\  &=\frac{3}{2}\left(\frac{1}{3}(8-1)\right) \\  &=\frac{3}{2}\left(\frac{7}{3}\right)\end{aligned}\end{aligned}
$$

## q-352797 exact original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /12}\frac{2\operatorname{cos}⁡(2x)}{1+\operatorname{sin}⁡(2x)}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\operatorname{ln}(\frac{3}{2})$
- $\operatorname{ln}⁡(\frac{3}{2})$ (correct)

We can solve this by substitution. Let $u=1+\operatorname{sin}⁡2x.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\operatorname{cos}⁡2x\,⟹\,\text{d}u=2\operatorname{cos}⁡2x\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=1+\operatorname{sin}⁡2x.$

| $x$ | $0$ | $\frac{\pi }{12}$ |
| --- | --- | --- |
| $u$ | $1$ | $\frac{3}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{0}^{\pi /12}\frac{2\operatorname{cos}⁡(2x)}{1+\operatorname{sin}⁡(2x)}\,\text{d}x & ={\int }_{1}^{3/2}\frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|{|}_{1}^{3/2} \\  & =\operatorname{ln}⁡(\frac{3}{2})-\operatorname{ln}⁡(1) \\  & =\operatorname{ln}⁡(\frac{3}{2})\end{aligned}\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

Evaluate the following integral. Do not round the answer.

$3\cdot \int_{0}^{\frac{\pi}{24}}\frac{2\operatorname{cos}⁡({4x})}{1+\operatorname{sin}⁡({4x})}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{3 \log{\left(\frac{3}{2} \right)}}{2}$
- $\frac{3 \log{\left(\frac{3}{2} \right)}}{2}$ (correct)

We can solve this by substitution. Let $u=1+\operatorname{sin}⁡{4x}.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(2\operatorname{cos}⁡{4x}\right)\,⟹\,\frac{1}{2}\left(\text{d}u\right)=2\operatorname{cos}⁡{4x}\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=1+\operatorname{sin}⁡{4x}.$

| $x$ | $0$ | $\frac{\pi}{24}$ |
| --- | --- | --- |
| $u$ | $1$ | $\frac{3}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}3\cdot \int_{0}^{\frac{\pi}{24}}\frac{2\operatorname{cos}⁡({4x})}{1+\operatorname{sin}⁡({4x})}\,\text{d}x &=\frac{3}{2}\cdot {\int }_{1}^{3/2}\frac{1}{u}\,\text{d}u \\  &=\frac{3}{2}\left(\operatorname{ln}⁡|u|{|}_{1}^{3/2}\right) \\  &=\frac{3}{2}\left(\operatorname{ln}⁡(\frac{3}{2})-\operatorname{ln}⁡(1)\right) \\  &=\frac{3}{2}\left(\operatorname{ln}⁡(\frac{3}{2})\right)\end{aligned}\end{aligned}
$$

## q-352798 exact original

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /12}^{\pi /6}\frac{2\operatorname{cos}⁡(2x)}{\operatorname{sin}⁡(2x)}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{\operatorname{ln}(3)}{2}$ (correct)

We can solve this by substitution. Let $u=\operatorname{sin}⁡2x.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\operatorname{cos}⁡2x\,⟹\,\text{d}u=2\operatorname{cos}⁡2x\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{sin}⁡2x.$

| $x$ | $\frac{\pi }{12}$ | $\frac{\pi }{6}$ |
| --- | --- | --- |
| $u$ | $\frac{1}{2}$ | $\frac{\sqrt{3}}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{\pi /12}^{\pi /6}\frac{2\operatorname{cos}⁡(2x)}{\operatorname{sin}⁡(2x)}\,\text{d}x & ={\int }_{1/2}^{\sqrt{3}/2}\frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|{|}_{1/2}^{\sqrt{3}/2} \\  & =\operatorname{ln}⁡(\frac{\sqrt{3}}{2})-\operatorname{ln}⁡(\frac{1}{2}) \\  & =\operatorname{ln}⁡(\frac{(\frac{\sqrt{3}}{2})}{(\frac{1}{2})}) \\  & =\operatorname{ln}⁡(\sqrt{3}) \\  & =\frac{\operatorname{ln}⁡(3)}{2}\end{aligned}\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

Evaluate the following integral. Do not round the answer.

$3\cdot \int_{\frac{\pi}{24}}^{\frac{\pi}{12}}\frac{2\operatorname{cos}⁡({4x})}{\operatorname{sin}⁡({4x})}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{3 \log{\left(3 \right)}}{4}$ (correct)

We can solve this by substitution. Let $u=\operatorname{sin}⁡{4x}.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(2\operatorname{cos}⁡{4x}\right)\,⟹\,\frac{1}{2}\left(\text{d}u\right)=2\operatorname{cos}⁡{4x}\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{sin}⁡{4x}.$

| $x$ | $\frac{\pi}{24}$ | $\frac{\pi}{12}$ |
| --- | --- | --- |
| $u$ | $\frac{1}{2}$ | $\frac{\sqrt{3}}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}3\cdot \int_{\frac{\pi}{24}}^{\frac{\pi}{12}}\frac{2\operatorname{cos}⁡({4x})}{\operatorname{sin}⁡({4x})}\,\text{d}x &=\frac{3}{2}\cdot {\int }_{1/2}^{\sqrt{3}/2}\frac{1}{u}\,\text{d}u \\  &=\frac{3}{2}\left(\operatorname{ln}⁡|u|{|}_{1/2}^{\sqrt{3}/2}\right) \\  &=\frac{3}{2}\left(\operatorname{ln}⁡(\frac{\sqrt{3}}{2})-\operatorname{ln}⁡(\frac{1}{2})\right) \\  &=\frac{3}{2}\left(\operatorname{ln}⁡(\frac{(\frac{\sqrt{3}}{2})}{(\frac{1}{2})})\right) \\  &=\frac{3}{2}\left(\operatorname{ln}⁡(\sqrt{3})\right) \\  &=\frac{3}{2}\left(\frac{\operatorname{ln}⁡(3)}{2}\right)\end{aligned}\end{aligned}
$$

## q-362157 exact original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /3}\operatorname{tan}⁡(x)\sqrt{\operatorname{cos}⁡(x)}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $2-\sqrt{2}$ (correct)

We can solve this by substitution. Let $u=\operatorname{cos}⁡x.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=-\operatorname{sin}⁡x\,⟹\,\text{d}u=-\operatorname{sin}⁡x\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{cos}⁡x.$

| $x$ | $0$ | $\frac{\pi }{3}$ |
| --- | --- | --- |
| $u$ | $1$ | $\frac{1}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\pi /3}\operatorname{tan}⁡(x)\sqrt{\operatorname{cos}⁡(x)}\,\text{d}x & ={\int }_{0}^{\pi /3}\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\sqrt{\operatorname{cos}⁡x}\,\text{d}x \\  & ={\int }_{0}^{\pi /3}\frac{\sqrt{\operatorname{cos}⁡x}}{\operatorname{cos}⁡x}\cdot \operatorname{sin}⁡x\,\text{d}x \\  & ={\int }_{0}^{\pi /3}\frac{1}{\sqrt{\operatorname{cos}⁡x}}\cdot \operatorname{sin}⁡x\,\text{d}x \\  & ={\int }_{1}^{1/2}\frac{1}{\sqrt{u}}\cdot (-\text{d}u) \\  & ={\int }_{1}^{1/2}-\frac{1}{\sqrt{u}}\,\text{d}u \\  & =-2\sqrt{u}{|}_{1}^{1/2} \\  & =-2(\frac{\sqrt{2}}{2}-1) \\  & =2-\sqrt{2}\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

Evaluate the following integral. Do not round the answer.

$3\cdot \int_{0}^{\frac{\pi}{6}}\operatorname{tan}⁡({2x})\sqrt{\operatorname{cos}⁡({2x})}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $3 - \frac{3 \sqrt{2}}{2}$ (correct)

We can solve this by substitution. Let $u=\operatorname{cos}⁡{2x}.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(-\operatorname{sin}⁡{2x}\right)\,⟹\,\frac{1}{2}\left(\text{d}u\right)=-\operatorname{sin}⁡{2x}\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{cos}⁡{2x}.$

| $x$ | $0$ | $\frac{\pi}{6}$ |
| --- | --- | --- |
| $u$ | $1$ | $\frac{1}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}3\cdot \int_{0}^{\frac{\pi}{6}}\operatorname{tan}⁡({2x})\sqrt{\operatorname{cos}⁡({2x})}\,\text{d}x &=3\cdot \int_{0}^{\frac{\pi}{6}}\frac{\operatorname{sin}⁡{2x}}{\operatorname{cos}⁡{2x}}\,\sqrt{\operatorname{cos}⁡{2x}}\,\text{d}x \\  &=3\cdot \int_{0}^{\frac{\pi}{6}}\frac{\sqrt{\operatorname{cos}⁡{2x}}}{\operatorname{cos}⁡{2x}}\cdot \operatorname{sin}⁡{2x}\,\text{d}x \\  &=3\cdot \int_{0}^{\frac{\pi}{6}}\frac{1}{\sqrt{\operatorname{cos}⁡{2x}}}\cdot \operatorname{sin}⁡{2x}\,\text{d}x \\  &=\frac{3}{2}\cdot {\int }_{1}^{1/2}\frac{1}{\sqrt{u}}\cdot (-\text{d}u) \\  &=\frac{3}{2}\cdot {\int }_{1}^{1/2}-\frac{1}{\sqrt{u}}\,\text{d}u \\  &=\frac{3}{2}\left(-2\sqrt{u}{|}_{1}^{1/2}\right) \\  &=\frac{3}{2}\left(-2(\frac{\sqrt{2}}{2}-1)\right) \\  &=\frac{3}{2}\left(2-\sqrt{2}\right)\end{aligned}
$$

## q-49256 exact original (ineligible raw operator capture)

Calculate $\int \frac{\operatorname{sec}⁡3x}{\operatorname{cos}⁡3x}\,\text{d}x.$

Field selection (radio)

- $\frac{1}{3}\operatorname{cot}⁡x+C$
- $\frac{1}{3}{sec}^{2}⁡3x+C$
- $\operatorname{tan}⁡x+C$
- $\operatorname{cot}⁡(\frac{x}{3})+C$
- $\frac{1}{3}\operatorname{tan}⁡3x+C$ (correct)

We can write the integral as

$$
\int \frac{\operatorname{sec}⁡3x}{\operatorname{cos}⁡3x}\,\text{d}x=\int \operatorname{sec}⁡3x\cdot \frac{1}{\operatorname{cos}⁡3x}\,\text{d}x.
$$

We then use the fact that $\frac{1}{\operatorname{cos}⁡3x}=\operatorname{sec}⁡3x$ to express this as

$$
\int {sec}^{2}⁡3x\,\text{d}x.
$$

We can solve this by substitution. Let $u=3x.$ Then $\text{d}x=\frac{1}{3}\text{d}u.$ Therefore,

$$
\begin{aligned}\begin{aligned}\int {sec}^{2}⁡3x\,\text{d}x & =\int {sec}^{2}⁡u\cdot \,\frac{1}{3}\text{d}u \\  & =\frac{1}{3}\int {sec}^{2}⁡u\,\text{d}u \\  & =\frac{1}{3}\operatorname{tan}⁡u+C \\  & =\frac{1}{3}\operatorname{tan}⁡3x+C.\end{aligned}\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

Calculate $3\cdot \int \frac{\operatorname{sec}⁡{6x}}{\operatorname{cos}⁡{6x}}\,\text{d}x.$

Field selection (radio)

- $\frac{\cot{\left(2 x \right)}}{2}+C$
- $\frac{\sec^{2}{\left(6 x \right)}}{2}+C$
- $\frac{3 \tan{\left(2 x \right)}}{2}+C$
- $\frac{3 \cot{\left(\frac{2 x}{3} \right)}}{2}+C$
- $\frac{\tan{\left(6 x \right)}}{2}+C$ (correct)

We can write the integral as

$$
3\cdot \int \frac{\operatorname{sec}⁡{6x}}{\operatorname{cos}⁡{6x}}\,\text{d}x = 3\cdot \int \operatorname{sec}⁡{6x}\cdot \frac{1}{\operatorname{cos}⁡{6x}}\,\text{d}x.
$$

We then use the fact that $\frac{1}{\operatorname{cos}⁡{6x}}=\operatorname{sec}⁡{6x}$ to express this as

$$
3\cdot \int \operatorname{sec}^{2}⁡{6x}\,\text{d}x.
$$

We can solve this by substitution. Let $u={6x}.$ Then $\text{d}x=\frac{1}{2}\left(\frac{1}{3}\text{d}u\right).$ Therefore,

$$
\begin{aligned}\begin{aligned}3\cdot \int \operatorname{sec}^{2}⁡{6x}\,\text{d}x &=\frac{3}{2}\cdot \int \operatorname{sec}^{2}⁡u\cdot \,\frac{1}{3}\text{d}u \\  &=\frac{3}{2}\cdot \frac{1}{3}\int \operatorname{sec}^{2}⁡u\,\text{d}u \\  &=\frac{3}{2}\left(\frac{1}{3}\operatorname{tan}⁡u\right)+C \\  &=\frac{3}{2}\left(\frac{1}{3}\operatorname{tan}⁡{6x}\right)+C.\end{aligned}\end{aligned}
$$

## q-49257 exact original (ineligible raw operator capture)

Evaluate ${\int }_{\pi /8}^{\pi /4}\frac{2\operatorname{cos}⁡(2x)}{{sin}^{2}⁡(2x)}\,\text{d}x.$

Field selection (radio)

- $1$
- $\sqrt{2}-1$ (correct)
- $\sqrt{2}$
- $\frac{\sqrt{2}-1}{2}$
- $2-\sqrt{2}$

We can solve this by substitution. Let $u=\operatorname{sin}⁡2x.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\operatorname{cos}⁡2x\,⟹\,\text{d}u=2\operatorname{cos}⁡2x\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{sin}⁡2x.$

| $x$ | $\frac{\pi }{8}$ | $\frac{\pi }{4}$ |
| --- | --- | --- |
| $u$ | $\frac{\sqrt{2}}{2}$ | $1$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{\pi /8}^{\pi /4}\frac{2\operatorname{cos}⁡(2x)}{{sin}^{2}⁡(2x)}\,\text{d}x & ={\int }_{\sqrt{2}/2}^{1}\frac{1}{{u}^{2}}\,\text{d}u \\  & =-\frac{1}{u}{|}_{\sqrt{2}/2}^{1} \\  & =-\frac{1}{1}+\frac{2}{\sqrt{2}} \\  & =\sqrt{2}-1.\end{aligned}\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

Evaluate $3\cdot \int_{\frac{\pi}{16}}^{\frac{\pi}{8}}\frac{2\operatorname{cos}⁡({4x})}{\operatorname{sin}^{2}⁡({4x})}\,\text{d}x.$

Field selection (radio)

- $\frac{3}{2}$
- $- \frac{3}{2} + \frac{3 \sqrt{2}}{2}$ (correct)
- $\frac{3 \sqrt{2}}{2}$
- $- \frac{3}{4} + \frac{3 \sqrt{2}}{4}$
- $3 - \frac{3 \sqrt{2}}{2}$

We can solve this by substitution. Let $u=\operatorname{sin}⁡{4x}.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(2\operatorname{cos}⁡{4x}\right)\,⟹\,\frac{1}{2}\left(\text{d}u\right)=2\operatorname{cos}⁡{4x}\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{sin}⁡{4x}.$

| $x$ | $\frac{\pi}{16}$ | $\frac{\pi}{8}$ |
| --- | --- | --- |
| $u$ | $\frac{\sqrt{2}}{2}$ | $1$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}3\cdot \int_{\frac{\pi}{16}}^{\frac{\pi}{8}}\frac{2\operatorname{cos}⁡({4x})}{\operatorname{sin}^{2}⁡({4x})}\,\text{d}x &=\frac{3}{2}\cdot {\int }_{\sqrt{2}/2}^{1}\frac{1}{{u}^{2}}\,\text{d}u \\  &=\frac{3}{2}\left(-\frac{1}{u}{|}_{\sqrt{2}/2}^{1}\right) \\  &=\frac{3}{2}\left(-\frac{1}{1}+\frac{2}{\sqrt{2}}\right) \\  &=\frac{3}{2}\left(\sqrt{2}-1\right).\end{aligned}\end{aligned}
$$

## q-49277 exact original (ineligible raw operator capture)

$\int \operatorname{sin}⁡x{sec}^{2}⁡x\,\text{d}x=$

Field selection (radio)

- $-\operatorname{csc}⁡x+C$
- $\operatorname{sec}⁡x+C$ (correct)
- $-\operatorname{sec}⁡x+C$
- $\operatorname{csc}⁡x+C$
- $\operatorname{cos}⁡x+C$

We use the identity $\operatorname{sec}⁡x=\frac{1}{\operatorname{cos}⁡x}$ and rewrite the integral as

$$
\int \operatorname{sin}⁡x{sec}^{2}⁡x\,\text{d}x=\int \frac{1}{{cos}^{2}⁡x}\cdot \operatorname{sin}⁡x\,\text{d}x.
$$

We can solve this by substitution. Let $u=\operatorname{cos}⁡x.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=-\operatorname{sin}⁡x\,⟹\,\text{d}u=-\operatorname{sin}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{1}{{cos}^{2}⁡x}\cdot \operatorname{sin}⁡x\,\text{d}x & =-\int \frac{1}{{u}^{2}}\,\text{d}u \\  & =\frac{1}{u}+C \\  & =(\operatorname{cos}⁡x)^{-1}+C \\  & =\operatorname{sec}⁡x+C.\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

$3\cdot \int \operatorname{sin}⁡{2x}\operatorname{sec}^{2}⁡{2x}\,\text{d}x=$

Field selection (radio)

- $- \frac{3 \csc{\left(2 x \right)}}{2}+C$
- $\frac{3 \sec{\left(2 x \right)}}{2}+C$ (correct)
- $- \frac{3 \sec{\left(2 x \right)}}{2}+C$
- $\frac{3 \csc{\left(2 x \right)}}{2}+C$
- $\frac{3 \cos{\left(2 x \right)}}{2}+C$

We use the identity $\operatorname{sec}⁡{2x}=\frac{1}{\operatorname{cos}⁡{2x}}$ and rewrite the integral as

$$
3\cdot \int \operatorname{sin}⁡{2x}\operatorname{sec}^{2}⁡{2x}\,\text{d}x = 3\cdot \int \frac{1}{\operatorname{cos}^{2}⁡{2x}}\cdot \operatorname{sin}⁡{2x}\,\text{d}x.
$$

We can solve this by substitution. Let $u=\operatorname{cos}⁡{2x}.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(-\operatorname{sin}⁡{2x}\right)\,⟹\,\frac{1}{2}\left(\text{d}u\right)=-\operatorname{sin}⁡{2x}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}3\cdot \int \frac{1}{\operatorname{cos}^{2}⁡{2x}}\cdot \operatorname{sin}⁡{2x}\,\text{d}x &=\frac{3}{2}\cdot -\int \frac{1}{{u}^{2}}\,\text{d}u \\  &=\frac{3}{2}\left(\frac{1}{u}\right)+C \\  &=\frac{3}{2}\left((\operatorname{cos}⁡{2x})^{-1}\right)+C \\  &=\frac{3}{2}\left(\operatorname{sec}⁡{2x}\right)+C.\end{aligned}
$$

## q-49278 exact original

$\int \operatorname{sin}⁡3x\operatorname{sec}⁡3x\,\text{d}x=$

Field selection (radio)

- $\frac{1}{3}\operatorname{ln}⁡|\operatorname{csc}⁡3x|+C$
- $3\operatorname{ln}⁡|\operatorname{cos}⁡3x|+C$
- $\frac{1}{3}\operatorname{ln}⁡|\operatorname{cos}⁡3x|+C$
- $\frac{1}{3}\operatorname{ln}⁡|\operatorname{sec}⁡3x|+C$ (correct)
- $3\operatorname{ln}⁡|\operatorname{sin}⁡3x|+C$

We use the identity $\operatorname{sec}⁡3x=\frac{1}{\operatorname{cos}⁡3x}$ and rewrite the integral as

$$
\int \operatorname{sin}⁡3x\operatorname{sec}⁡3x\,\text{d}x=\int \frac{1}{\operatorname{cos}⁡3x}\cdot \operatorname{sin}⁡3x\,\text{d}x.
$$

We can solve this by substitution. Let $u=\operatorname{cos}⁡3x.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=-3\operatorname{sin}⁡3x\,⟹\,-\frac{1}{3}\text{d}u=\operatorname{sin}⁡3x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{1}{\operatorname{cos}⁡3x}\cdot \operatorname{sin}⁡3x\,\text{d}x & =-\frac{1}{3}\int \frac{1}{u}\,\text{d}u \\  & =-\frac{1}{3}\operatorname{ln}⁡|u|+C \\  & =-\frac{1}{3}\operatorname{ln}⁡|\operatorname{cos}⁡3x|+C \\  & =\frac{1}{3}\operatorname{ln}⁡|(\operatorname{cos}⁡3x)^{-1}|+C \\  & =\frac{1}{3}\operatorname{ln}⁡|\operatorname{sec}⁡3x|+C.\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

$3\cdot \int \operatorname{sin}⁡{6x}\operatorname{sec}⁡{6x}\,\text{d}x=$

Field selection (radio)

- $\frac{\log{\left(\left|{\csc{\left(6 x \right)}}\right| \right)}}{2}+C$
- $\frac{9 \log{\left(\left|{\cos{\left(6 x \right)}}\right| \right)}}{2}+C$
- $\frac{\log{\left(\left|{\cos{\left(6 x \right)}}\right| \right)}}{2}+C$
- $\frac{\log{\left(\left|{\sec{\left(6 x \right)}}\right| \right)}}{2}+C$ (correct)
- $\frac{9 \log{\left(\left|{\sin{\left(6 x \right)}}\right| \right)}}{2}+C$

We use the identity $\operatorname{sec}⁡{6x}=\frac{1}{\operatorname{cos}⁡{6x}}$ and rewrite the integral as

$$
3\cdot \int \operatorname{sin}⁡{6x}\operatorname{sec}⁡{6x}\,\text{d}x = 3\cdot \int \frac{1}{\operatorname{cos}⁡{6x}}\cdot \operatorname{sin}⁡{6x}\,\text{d}x.
$$

We can solve this by substitution. Let $u=\operatorname{cos}⁡{6x}.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(-3\operatorname{sin}⁡{6x}\right)\,⟹\,\frac{1}{2}\left(-\frac{1}{3}\text{d}u\right)=\operatorname{sin}⁡{6x}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}3\cdot \int \frac{1}{\operatorname{cos}⁡{6x}}\cdot \operatorname{sin}⁡{6x}\,\text{d}x &=\frac{3}{2}\cdot -\frac{1}{3}\int \frac{1}{u}\,\text{d}u \\  &=\frac{3}{2}\left(-\frac{1}{3}\operatorname{ln}⁡|u|\right)+C \\  &=\frac{3}{2}\left(-\frac{1}{3}\operatorname{ln}⁡|\operatorname{cos}⁡{6x}|\right)+C \\  &=\frac{3}{2}\left(\frac{1}{3}\operatorname{ln}⁡|(\operatorname{cos}⁡{6x})^{-1}|\right)+C \\  &=\frac{3}{2}\left(\frac{1}{3}\operatorname{ln}⁡|\operatorname{sec}⁡{6x}|\right)+C.\end{aligned}
$$

## q-49280 exact original (ineligible raw operator capture)

Calculate $\int \frac{\operatorname{tan}⁡4x}{\operatorname{cos}⁡4x\operatorname{sin}⁡4x}\,\text{d}x.$

Field selection (radio)

- $4\operatorname{tan}⁡4x+C$
- $4\operatorname{tan}⁡4x\operatorname{sec}⁡4x+C$
- $\frac{1}{4}\operatorname{tan}⁡4x+C$ (correct)
- $\frac{1}{4}\operatorname{tan}⁡4x\operatorname{sec}⁡4x+C$
- $\frac{1}{4}{tan}^{2}⁡4x+C$

We can write the integral as

$$
\int \frac{\operatorname{tan}⁡4x}{\operatorname{cos}⁡4x\operatorname{sin}⁡4x}\,\text{d}x=\int \operatorname{tan}⁡4x\cdot \frac{1}{\operatorname{cos}⁡4x\operatorname{sin}⁡4x}\,\text{d}x.
$$

We then use the fact that $\operatorname{tan}⁡4x=\frac{\operatorname{sin}⁡4x}{\operatorname{cos}⁡4x}$ to express this as

$$
\int \frac{\operatorname{sin}⁡4x}{\operatorname{cos}⁡4x}\cdot \frac{1}{\operatorname{cos}⁡4x\operatorname{sin}⁡4x}\,\text{d}x.
$$

Therefore, using the identity $\frac{1}{\operatorname{cos}⁡4x}=\operatorname{sec}⁡4x$, we get

$$
\begin{aligned}\int \frac{\operatorname{tan}⁡4x}{\operatorname{cos}⁡4x\operatorname{sin}⁡4x}\,\text{d}x & =\int \frac{\operatorname{sin}⁡4x}{\operatorname{cos}⁡4x}\cdot \frac{1}{\operatorname{cos}⁡4x\operatorname{sin}⁡4x}\,\text{d}x \\  & =\int \frac{1}{\operatorname{cos}⁡4x}\cdot \frac{1}{\operatorname{cos}⁡4x}\,\text{d}x \\  & =\int {sec}^{2}⁡4x\,\text{d}x.\end{aligned}
$$

We can solve this by substitution. Let $u=4x.$ Then $\text{d}x=\frac{1}{4}\text{d}u.$ Hence,

$$
\begin{aligned}\begin{aligned}\int \frac{\operatorname{tan}⁡4x}{\operatorname{cos}⁡4x\operatorname{sin}⁡4x}\,\text{d}x & =\int {sec}^{2}⁡4x\,\text{d}x \\  & =\int {sec}^{2}⁡u\cdot \frac{1}{4}\,\text{d}u \\  & =\frac{1}{4}\int {sec}^{2}⁡u\,\text{d}u \\  & =\frac{1}{4}\operatorname{tan}⁡u+C \\  & =\frac{1}{4}\operatorname{tan}⁡4x+C.\end{aligned}\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

Calculate $3\cdot \int \frac{\operatorname{tan}⁡{8x}}{\operatorname{cos}⁡{8x}\operatorname{sin}⁡{8x}}\,\text{d}x.$

Field selection (radio)

- $6 \tan{\left(8 x \right)}+C$
- $6 \tan{\left(8 x \right)} \sec{\left(8 x \right)}+C$
- $\frac{3 \tan{\left(8 x \right)}}{8}+C$ (correct)
- $\frac{3 \tan{\left(8 x \right)} \sec{\left(8 x \right)}}{8}+C$
- $\frac{3 \tan^{2}{\left(8 x \right)}}{8}+C$

We can write the integral as

$$
3\cdot \int \frac{\operatorname{tan}⁡{8x}}{\operatorname{cos}⁡{8x}\operatorname{sin}⁡{8x}}\,\text{d}x = 3\cdot \int \operatorname{tan}⁡{8x}\cdot \frac{1}{\operatorname{cos}⁡{8x}\operatorname{sin}⁡{8x}}\,\text{d}x.
$$

We then use the fact that $\operatorname{tan}⁡{8x}=\frac{\operatorname{sin}⁡{8x}}{\operatorname{cos}⁡{8x}}$ to express this as

$$
3\cdot \int \frac{\operatorname{sin}⁡{8x}}{\operatorname{cos}⁡{8x}}\cdot \frac{1}{\operatorname{cos}⁡{8x}\operatorname{sin}⁡{8x}}\,\text{d}x.
$$

Therefore, using the identity $\frac{1}{\operatorname{cos}⁡{8x}}=\operatorname{sec}⁡{8x}$, we get

$$
\begin{aligned}3\cdot \int \frac{\operatorname{tan}⁡{8x}}{\operatorname{cos}⁡{8x}\operatorname{sin}⁡{8x}}\,\text{d}x &=3\cdot \int \frac{\operatorname{sin}⁡{8x}}{\operatorname{cos}⁡{8x}}\cdot \frac{1}{\operatorname{cos}⁡{8x}\operatorname{sin}⁡{8x}}\,\text{d}x \\  &=3\cdot \int \frac{1}{\operatorname{cos}⁡{8x}}\cdot \frac{1}{\operatorname{cos}⁡{8x}}\,\text{d}x \\  &=3\cdot \int \operatorname{sec}^{2}⁡{8x}\,\text{d}x.\end{aligned}
$$

We can solve this by substitution. Let $u={8x}.$ Then $\text{d}x=\frac{1}{2}\left(\frac{1}{4}\text{d}u\right).$ Hence,

$$
\begin{aligned}\begin{aligned}3\cdot \int \frac{\operatorname{tan}⁡{8x}}{\operatorname{cos}⁡{8x}\operatorname{sin}⁡{8x}}\,\text{d}x &=3\cdot \int \operatorname{sec}^{2}⁡{8x}\,\text{d}x \\  &=\frac{3}{2}\cdot \int \operatorname{sec}^{2}⁡u\cdot \frac{1}{4}\,\text{d}u \\  &=\frac{3}{2}\cdot \frac{1}{4}\int \operatorname{sec}^{2}⁡u\,\text{d}u \\  &=\frac{3}{2}\left(\frac{1}{4}\operatorname{tan}⁡u\right)+C \\  &=\frac{3}{2}\left(\frac{1}{4}\operatorname{tan}⁡{8x}\right)+C.\end{aligned}\end{aligned}
$$

## q-49281 exact original (ineligible raw operator capture)

Calculate $\int \frac{1}{{sec}^{2}⁡2x\operatorname{cos}⁡2x}\,\text{d}x.$

Field selection (radio)

- $2\operatorname{cos}⁡2x+C$
- $2\operatorname{sin}⁡2x+C$
- $\frac{1}{2}\operatorname{sin}⁡2x+C$ (correct)
- $-\frac{1}{2}\operatorname{cos}⁡2x+C$
- $-2\operatorname{sin}⁡2x+C$

We can write the integral as

$$
\int \frac{1}{{sec}^{2}⁡2x\operatorname{cos}⁡2x}\,\text{d}x=\int \frac{1}{{sec}^{2}⁡2x}\cdot \frac{1}{\operatorname{cos}⁡2x}\,\text{d}x.
$$

Then, we use the identity $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x$ as follows:

$$
\int \frac{1}{{sec}^{2}⁡2x}\cdot \operatorname{sec}⁡2x\,\text{d}x=\int \frac{1}{\operatorname{sec}⁡2x}\,\text{d}x=\int \operatorname{cos}⁡2x\,\text{d}x
$$

We can solve this by substitution. Let  $u=2x.$ Then $\text{d}x=\frac{1}{2}\text{d}u.$ Hence

$$
\begin{aligned}\int \frac{1}{{sec}^{2}⁡2x\operatorname{cos}⁡2x}\,\text{d}x & =\int \operatorname{cos}⁡2x\,\text{d}x \\  & =\int \operatorname{cos}⁡u\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int \operatorname{cos}⁡u\,\text{d}u \\  & =\frac{1}{2}\operatorname{sin}⁡u+C \\  & =\frac{1}{2}\operatorname{sin}⁡2x+C.\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

Calculate $3\cdot \int \frac{1}{\operatorname{sec}^{2}⁡{4x}\operatorname{cos}⁡{4x}}\,\text{d}x.$

Field selection (radio)

- $3 \cos{\left(4 x \right)}+C$
- $3 \sin{\left(4 x \right)}+C$
- $\frac{3 \sin{\left(4 x \right)}}{4}+C$ (correct)
- $- \frac{3 \cos{\left(4 x \right)}}{4}+C$
- $- 3 \sin{\left(4 x \right)}+C$

We can write the integral as

$$
3\cdot \int \frac{1}{\operatorname{sec}^{2}⁡{4x}\operatorname{cos}⁡{4x}}\,\text{d}x = 3\cdot \int \frac{1}{\operatorname{sec}^{2}⁡{4x}}\cdot \frac{1}{\operatorname{cos}⁡{4x}}\,\text{d}x.
$$

Then, we use the identity $\frac{1}{\operatorname{cos}⁡{2x}}=\operatorname{sec}⁡{2x}$ as follows:

$$
3\cdot \int \frac{1}{\operatorname{sec}^{2}⁡{4x}}\cdot \operatorname{sec}⁡{4x}\,\text{d}x = 3\cdot \int \frac{1}{\operatorname{sec}⁡{4x}}\,\text{d}x = 3\cdot \int \operatorname{cos}⁡{4x}\,\text{d}x
$$

We can solve this by substitution. Let  $u={4x}.$ Then $\text{d}x=\frac{1}{2}\left(\frac{1}{2}\text{d}u\right).$ Hence

$$
\begin{aligned}3\cdot \int \frac{1}{\operatorname{sec}^{2}⁡{4x}\operatorname{cos}⁡{4x}}\,\text{d}x &=3\cdot \int \operatorname{cos}⁡{4x}\,\text{d}x \\  &=\frac{3}{2}\cdot \int \operatorname{cos}⁡u\cdot \frac{1}{2}\,\text{d}u \\  &=\frac{3}{2}\cdot \frac{1}{2}\int \operatorname{cos}⁡u\,\text{d}u \\  &=\frac{3}{2}\left(\frac{1}{2}\operatorname{sin}⁡u\right)+C \\  &=\frac{3}{2}\left(\frac{1}{2}\operatorname{sin}⁡{4x}\right)+C.\end{aligned}
$$

## q-10040 exact original

${\int }_{0}^{1}\operatorname{tan}⁡x\,\text{d}x=$

Field selection (radio)

- $\operatorname{ln}⁡|\operatorname{cos}⁡(1)|$
- $\frac{1}{2}\operatorname{ln}⁡|\operatorname{cos}⁡(1)|$
- $-\operatorname{ln}⁡|\operatorname{sin}⁡(1)|$
- $-\operatorname{ln}⁡|\operatorname{cos}⁡(1)|$ (correct)
- $\operatorname{ln}⁡|\operatorname{sin}⁡(1)|$

We use the identity $\operatorname{tan}⁡x=\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}$ and rewrite the integral as

$$
{\int }_{0}^{1}\operatorname{tan}⁡x\,\text{d}x={\int }_{0}^{1}\frac{\operatorname{sin}⁡x}{\operatorname{cos}⁡x}\,\text{d}x.
$$

We can solve this by substitution. Let $u=\operatorname{cos}⁡x.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=-\operatorname{sin}⁡x\,⟹\,\text{d}u=-\operatorname{sin}⁡x\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{cos}⁡x.$

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $1$ | $\operatorname{cos}⁡(1)$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

Hence

$$
\begin{aligned}{\int }_{0}^{1}\operatorname{tan}⁡x\,\text{d}x & =-{\int }_{1}^{\operatorname{cos}⁡(1)}\frac{1}{u}\text{d}u \\  & =-\operatorname{ln}⁡|u|{|}_{1}^{\operatorname{cos}⁡(1)} \\  & =-\operatorname{ln}⁡|\operatorname{cos}⁡(1)|+\operatorname{ln}⁡|1| \\  & =-\operatorname{ln}⁡|\operatorname{cos}⁡(1)|.\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

$3\cdot \int_{0}^{\frac{1}{2}}\operatorname{tan}⁡{2x}\,\text{d}x=$

Field selection (radio)

- $\frac{3 \log{\left(\cos{\left(1 \right)} \right)}}{2}$
- $\frac{3 \log{\left(\cos{\left(1 \right)} \right)}}{4}$
- $- \frac{3 \log{\left(\sin{\left(1 \right)} \right)}}{2}$
- $- \frac{3 \log{\left(\cos{\left(1 \right)} \right)}}{2}$ (correct)
- $\frac{3 \log{\left(\sin{\left(1 \right)} \right)}}{2}$

We use the identity $\operatorname{tan}⁡{2x}=\frac{\operatorname{sin}⁡{2x}}{\operatorname{cos}⁡{2x}}$ and rewrite the integral as

$$
3\cdot \int_{0}^{\frac{1}{2}}\operatorname{tan}⁡{2x}\,\text{d}x = 3\cdot \int_{0}^{\frac{1}{2}}\frac{\operatorname{sin}⁡{2x}}{\operatorname{cos}⁡{2x}}\,\text{d}x.
$$

We can solve this by substitution. Let $u=\operatorname{cos}⁡{2x}.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(-\operatorname{sin}⁡{2x}\right)\,⟹\,\frac{1}{2}\left(\text{d}u\right)=-\operatorname{sin}⁡{2x}\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{cos}⁡{2x}.$

| $x$ | $0$ | $\frac{1}{2}$ |
| --- | --- | --- |
| $u$ | $1$ | $\operatorname{cos}⁡(1)$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

Hence

$$
\begin{aligned}3\cdot \int_{0}^{\frac{1}{2}}\operatorname{tan}⁡{2x}\,\text{d}x &=\frac{3}{2}\cdot -{\int }_{1}^{\operatorname{cos}⁡(1)}\frac{1}{u}\text{d}u \\  &=\frac{3}{2}\left(-\operatorname{ln}⁡|u|{|}_{1}^{\operatorname{cos}⁡(1)}\right) \\  &=\frac{3}{2}\left(-\operatorname{ln}⁡|\operatorname{cos}⁡(1)|+\operatorname{ln}⁡|1|\right) \\  &=\frac{3}{2}\left(-\operatorname{ln}⁡|\operatorname{cos}⁡(1)|\right).\end{aligned}
$$

## q-49279 exact original (ineligible raw operator capture)

${\int }_{\pi /6}^{\pi /3}\frac{{tan}^{2}⁡x}{{cos}^{2}⁡x}\,\text{d}x=$

Field selection (radio)

- $\frac{2\sqrt{3}}{9}$
- $\frac{26\sqrt{3}}{27}$ (correct)
- $\frac{9\sqrt{3}}{20}$
- $\frac{14\sqrt{3}}{27}$
- $\frac{3\sqrt{3}}{8}$

We use the identity $\frac{1}{\operatorname{cos}⁡x}=\operatorname{sec}⁡x$ and rewrite the integral as

$$
{\int }_{\pi /6}^{\pi /3}\frac{{tan}^{2}⁡x}{{cos}^{2}⁡x}\,\text{d}x={\int }_{\pi /6}^{\pi /3}{tan}^{2}⁡x\cdot {sec}^{2}⁡x\,\text{d}x.
$$

We can solve this by substitution. Let $u=\operatorname{tan}⁡x.$ Then,

$$
\frac{\text{d}u}{\text{d}x}={sec}^{2}⁡x\,⟹\,du={sec}^{2}⁡x\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{tan}⁡x.$

| $x$ | $\frac{\pi }{6}$ | $\frac{\pi }{3}$ |
| --- | --- | --- |
| $u$ | $\frac{\sqrt{3}}{3}$ | $\sqrt{3}$ |

Therefore, the integral in terms of the new variable is

$$
\begin{aligned}\begin{aligned}{\int }_{\pi /6}^{\pi /3}{tan}^{2}⁡x\cdot {sec}^{2}⁡x\,\text{d}x & ={\int }_{\sqrt{3}/3}^{\sqrt{3}}{u}^{2}\,\cdot \text{d}u \\  & =\frac{{u}^{3}}{3}{|}_{\sqrt{3}/3}^{\sqrt{3}} \\  & =\frac{1}{3}({(\sqrt{3})}^{3}-{(\frac{\sqrt{3}}{3})}^{3}) \\  & =\frac{1}{3}(3\sqrt{3}-\frac{\sqrt{3}}{9}) \\  & =\frac{\sqrt{3}}{3}(3-\frac{1}{9}) \\  & =\frac{26\sqrt{3}}{27}.\end{aligned}\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

$3\cdot \int_{\frac{\pi}{12}}^{\frac{\pi}{6}}\frac{\operatorname{tan}^{2}⁡{2x}}{\operatorname{cos}^{2}⁡{2x}}\,\text{d}x=$

Field selection (radio)

- $\frac{\sqrt{3}}{3}$
- $\frac{13 \sqrt{3}}{9}$ (correct)
- $\frac{27 \sqrt{3}}{40}$
- $\frac{7 \sqrt{3}}{9}$
- $\frac{9 \sqrt{3}}{16}$

We use the identity $\frac{1}{\operatorname{cos}⁡{2x}}=\operatorname{sec}⁡{2x}$ and rewrite the integral as

$$
3\cdot \int_{\frac{\pi}{12}}^{\frac{\pi}{6}}\frac{\operatorname{tan}^{2}⁡{2x}}{\operatorname{cos}^{2}⁡{2x}}\,\text{d}x = 3\cdot \int_{\frac{\pi}{12}}^{\frac{\pi}{6}}\operatorname{tan}^{2}⁡{2x}\cdot \operatorname{sec}^{2}⁡{2x}\,\text{d}x.
$$

We can solve this by substitution. Let $u=\operatorname{tan}⁡{2x}.$ Then,

$$
\frac{\text{d}u}{\text{d}x}=2\left(\operatorname{sec}^{2}⁡{2x}\right)\,⟹\,\frac{1}{2}\left(du\right)=\operatorname{sec}^{2}⁡{2x}\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{tan}⁡{2x}.$

| $x$ | $\frac{\pi}{12}$ | $\frac{\pi}{6}$ |
| --- | --- | --- |
| $u$ | $\frac{\sqrt{3}}{3}$ | $\sqrt{3}$ |

Therefore, the integral in terms of the new variable is

$$
\begin{aligned}\begin{aligned}3\cdot \int_{\frac{\pi}{12}}^{\frac{\pi}{6}}\operatorname{tan}^{2}⁡{2x}\cdot \operatorname{sec}^{2}⁡{2x}\,\text{d}x &=\frac{3}{2}\cdot {\int }_{\sqrt{3}/3}^{\sqrt{3}}{u}^{2}\,\cdot \text{d}u \\  &=\frac{3}{2}\left(\frac{{u}^{3}}{3}{|}_{\sqrt{3}/3}^{\sqrt{3}}\right) \\  &=\frac{3}{2}\left(\frac{1}{3}({(\sqrt{3})}^{3}-{(\frac{\sqrt{3}}{3})}^{3})\right) \\  &=\frac{3}{2}\left(\frac{1}{3}(3\sqrt{3}-\frac{\sqrt{3}}{9})\right) \\  &=\frac{3}{2}\left(\frac{\sqrt{3}}{3}(3-\frac{1}{9})\right) \\  &=\frac{3}{2}\left(\frac{26\sqrt{3}}{27}\right).\end{aligned}\end{aligned}
$$

## q-362158 exact original

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /24}^{\pi /8}\operatorname{cot}⁡(4x)\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{\operatorname{ln}⁡2}{4}$ (correct)

We can solve this by substitution. Let $u=\operatorname{sin}⁡4x.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=4\operatorname{cos}⁡4x\,⟹\,\frac{1}{4}\text{d}u=\operatorname{cos}⁡4x\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{sin}⁡4x.$

| $x$ | $\frac{\pi }{24}$ | $\frac{\pi }{8}$ |
| --- | --- | --- |
| $u$ | $\frac{1}{2}$ | $1$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{\pi /24}^{\pi /8}\operatorname{cot}⁡(4x)\,\text{d}x & ={\int }_{\pi /24}^{\pi /8}\frac{\operatorname{cos}⁡(4x)}{\operatorname{sin}⁡(4x)}\,\text{d}x \\  & =\frac{1}{4}{\int }_{1/2}^{1}\frac{1}{u}\,\text{d}u \\  & =\frac{1}{4}\operatorname{ln}⁡|u|{|}_{1/2}^{1} \\  & =\frac{1}{4}(\operatorname{ln}⁡(1)-\operatorname{ln}⁡(\frac{1}{2})) \\  & =\frac{\operatorname{ln}⁡2}{4}\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

Evaluate the following integral. Do not round the answer.

$3\cdot \int_{\frac{\pi}{48}}^{\frac{\pi}{16}}\operatorname{cot}⁡({8x})\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{3 \log{\left(2 \right)}}{8}$ (correct)

We can solve this by substitution. Let $u=\operatorname{sin}⁡{8x}.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(4\operatorname{cos}⁡{8x}\right)\,⟹\,\frac{1}{2}\left(\frac{1}{4}\text{d}u\right)=\operatorname{cos}⁡{8x}\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{sin}⁡{8x}.$

| $x$ | $\frac{\pi}{48}$ | $\frac{\pi}{16}$ |
| --- | --- | --- |
| $u$ | $\frac{1}{2}$ | $1$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}3\cdot \int_{\frac{\pi}{48}}^{\frac{\pi}{16}}\operatorname{cot}⁡({8x})\,\text{d}x &=3\cdot \int_{\frac{\pi}{48}}^{\frac{\pi}{16}}\frac{\operatorname{cos}⁡({8x})}{\operatorname{sin}⁡({8x})}\,\text{d}x \\  &=\frac{3}{2}\cdot \frac{1}{4}{\int }_{1/2}^{1}\frac{1}{u}\,\text{d}u \\  &=\frac{3}{2}\left(\frac{1}{4}\operatorname{ln}⁡|u|{|}_{1/2}^{1}\right) \\  &=\frac{3}{2}\left(\frac{1}{4}(\operatorname{ln}⁡(1)-\operatorname{ln}⁡(\frac{1}{2}))\right) \\  &=\frac{3}{2}\left(\frac{\operatorname{ln}⁡2}{4}\right)\end{aligned}
$$

## q-114295 exact original

$\int \operatorname{tan}⁡(\frac{x}{2})\text{d}x=$

Field selection (radio)

- $-2\operatorname{ln}⁡|\operatorname{cos}⁡(\frac{x}{2})|+C$ (correct)
- $\operatorname{ln}⁡|\operatorname{cos}⁡(\frac{x}{2})|+C$
- $-2\operatorname{ln}⁡|\operatorname{sin}⁡(\frac{x}{2})|+C$
- $\frac{1}{2}\operatorname{ln}⁡|\operatorname{csc}⁡(\frac{x}{2})|+C$
- $\frac{1}{2}\operatorname{ln}⁡|\operatorname{sec}⁡(\frac{x}{2})|+C$

We use the identity $\operatorname{tan}⁡(\frac{x}{2})=\frac{\operatorname{sin}⁡(\frac{x}{2})}{\operatorname{cos}⁡(\frac{x}{2})}$ and rewrite the integral as

$$
\int \operatorname{tan}⁡(\frac{x}{2})\text{d}x=\int \frac{\operatorname{sin}⁡(\frac{x}{2})}{\operatorname{cos}⁡(\frac{x}{2})}\,\text{d}x.
$$

We can solve this by substitution. Let $u=\operatorname{cos}⁡(\frac{x}{2}).$ Then 

$$
\frac{\text{d}u}{\text{d}x}=-\frac{1}{2}\operatorname{sin}⁡(\frac{x}{2})\,⟹\,-2\text{d}u=\operatorname{sin}⁡(\frac{x}{2})\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{\operatorname{sin}⁡(\frac{x}{2})}{\operatorname{cos}⁡(\frac{x}{2})}\,\text{d}x & =-2\int \frac{1}{u}\,\text{d}u \\  & =-2\operatorname{ln}⁡|u|+C \\  & =-2\operatorname{ln}⁡|\operatorname{cos}⁡(\frac{x}{2})|+C\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

$3\cdot \int \operatorname{tan}⁡(\frac{{2x}}{2})\text{d}x=$

Field selection (radio)

- $- 3 \log{\left(\left|{\cos{\left(x \right)}}\right| \right)}+C$ (correct)
- $\frac{3 \log{\left(\left|{\cos{\left(x \right)}}\right| \right)}}{2}+C$
- $- 3 \log{\left(\left|{\sin{\left(x \right)}}\right| \right)}+C$
- $\frac{3 \log{\left(\left|{\csc{\left(x \right)}}\right| \right)}}{4}+C$
- $\frac{3 \log{\left(\left|{\sec{\left(x \right)}}\right| \right)}}{4}+C$

We use the identity $\operatorname{tan}⁡(\frac{{2x}}{2})=\frac{\operatorname{sin}⁡(\frac{{2x}}{2})}{\operatorname{cos}⁡(\frac{{2x}}{2})}$ and rewrite the integral as

$$
3\cdot \int \operatorname{tan}⁡(\frac{{2x}}{2})\text{d}x = 3\cdot \int \frac{\operatorname{sin}⁡(\frac{{2x}}{2})}{\operatorname{cos}⁡(\frac{{2x}}{2})}\,\text{d}x.
$$

We can solve this by substitution. Let $u=\operatorname{cos}⁡(\frac{{2x}}{2}).$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(-\frac{1}{2}\operatorname{sin}⁡(\frac{{2x}}{2})\right)\,⟹\,\frac{1}{2}\left(-2\text{d}u\right)=\operatorname{sin}⁡(\frac{{2x}}{2})\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}3\cdot \int \frac{\operatorname{sin}⁡(\frac{{2x}}{2})}{\operatorname{cos}⁡(\frac{{2x}}{2})}\,\text{d}x &=\frac{3}{2}\cdot -2\int \frac{1}{u}\,\text{d}u \\  &=\frac{3}{2}\left(-2\operatorname{ln}⁡|u|\right)+C \\  &=\frac{3}{2}\left(-2\operatorname{ln}⁡|\operatorname{cos}⁡(\frac{{2x}}{2})|\right)+C\end{aligned}
$$

## q-73371 exact original (ineligible raw operator capture)

${\int }_{\pi /12}^{\pi /4}\frac{\operatorname{cot}⁡(2x)}{{sin}^{4}⁡(2x)}\,\text{d}x=$

Field selection (radio)

- $\frac{3}{4}$
- $\frac{15}{4}$
- $\frac{15}{8}$ (correct)
- $\frac{3}{8}$
- $\frac{1}{8}$

We use the identity $\operatorname{cot}⁡2x=\frac{\operatorname{cos}⁡2x}{\operatorname{sin}⁡2x}$ and rewrite the integral as

$$
\begin{aligned}{\int }_{\pi /12}^{\pi /4}\frac{\operatorname{cot}⁡(2x)}{{sin}^{4}⁡(2x)}\,\text{d}x & ={\int }_{\pi /12}^{\pi /4}\frac{1}{{sin}^{4}⁡(2x)}\cdot \frac{\operatorname{cos}⁡2x}{\operatorname{sin}⁡2x}\,\text{d}x \\  & ={\int }_{\pi /12}^{\pi /4}\frac{1}{{sin}^{5}⁡(2x)}\cdot \operatorname{cos}⁡2x\,\text{d}x.\end{aligned}
$$

We can solve this by substitution. Let $u=\operatorname{sin}⁡2x.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\operatorname{cos}⁡2x\,⟹\,\frac{1}{2}\text{d}u=\operatorname{cos}⁡2x\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{sin}⁡2x.$

| $x$ | $\frac{\pi }{12}$ | $\frac{\pi }{4}$ |
| --- | --- | --- |
| $u$ | $\frac{1}{2}$ | $1$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{\pi /12}^{\pi /4}\frac{1}{{sin}^{5}⁡(2x)}\cdot \operatorname{cos}⁡2x\,\text{d}x & ={\int }_{1/2}^{1}\frac{1}{{u}^{5}}\,\cdot \frac{1}{2}\text{d}u \\  & =\frac{1}{2}{\int }_{1/2}^{1}\frac{1}{{u}^{5}}\,\text{d}u \\  & =\frac{1}{2}(\frac{{u}^{-4}}{-4}){|}_{1/2}^{1} \\  & =-\frac{1}{8}(\frac{1}{{u}^{4}}){|}_{1/2}^{1} \\  & =-\frac{1}{8}(\frac{1}{{1}^{4}}-{(\frac{2}{1})}^{4}) \\  & =-\frac{1}{8}(1-16) \\  & =\frac{15}{8}.\end{aligned}\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

$3\cdot \int_{\frac{\pi}{24}}^{\frac{\pi}{8}}\frac{\operatorname{cot}⁡({4x})}{\operatorname{sin}^{4}⁡({4x})}\,\text{d}x=$

Field selection (radio)

- $\frac{9}{8}$
- $\frac{45}{8}$
- $\frac{45}{16}$ (correct)
- $\frac{9}{16}$
- $\frac{3}{16}$

We use the identity $\operatorname{cot}⁡{4x}=\frac{\operatorname{cos}⁡{4x}}{\operatorname{sin}⁡{4x}}$ and rewrite the integral as

$$
\begin{aligned}3\cdot \int_{\frac{\pi}{24}}^{\frac{\pi}{8}}\frac{\operatorname{cot}⁡({4x})}{\operatorname{sin}^{4}⁡({4x})}\,\text{d}x &=3\cdot \int_{\frac{\pi}{24}}^{\frac{\pi}{8}}\frac{1}{\operatorname{sin}^{4}⁡({4x})}\cdot \frac{\operatorname{cos}⁡{4x}}{\operatorname{sin}⁡{4x}}\,\text{d}x \\  &=3\cdot \int_{\frac{\pi}{24}}^{\frac{\pi}{8}}\frac{1}{\operatorname{sin}^{5}⁡({4x})}\cdot \operatorname{cos}⁡{4x}\,\text{d}x.\end{aligned}
$$

We can solve this by substitution. Let $u=\operatorname{sin}⁡{4x}.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(2\operatorname{cos}⁡{4x}\right)\,⟹\,\frac{1}{2}\left(\frac{1}{2}\text{d}u\right)=\operatorname{cos}⁡{4x}\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{sin}⁡{4x}.$

| $x$ | $\frac{\pi}{24}$ | $\frac{\pi}{8}$ |
| --- | --- | --- |
| $u$ | $\frac{1}{2}$ | $1$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}3\cdot \int_{\frac{\pi}{24}}^{\frac{\pi}{8}}\frac{1}{\operatorname{sin}^{5}⁡({4x})}\cdot \operatorname{cos}⁡{4x}\,\text{d}x &=\frac{3}{2}\cdot {\int }_{1/2}^{1}\frac{1}{{u}^{5}}\,\cdot \frac{1}{2}\text{d}u \\  &=\frac{3}{2}\cdot \frac{1}{2}{\int }_{1/2}^{1}\frac{1}{{u}^{5}}\,\text{d}u \\  &=\frac{3}{2}\left(\frac{1}{2}(\frac{{u}^{-4}}{-4}){|}_{1/2}^{1}\right) \\  &=\frac{3}{2}\left(-\frac{1}{8}(\frac{1}{{u}^{4}}){|}_{1/2}^{1}\right) \\  &=\frac{3}{2}\left(-\frac{1}{8}(\frac{1}{{1}^{4}}-{(\frac{2}{1})}^{4})\right) \\  &=\frac{3}{2}\left(-\frac{1}{8}(1-16)\right) \\  &=\frac{3}{2}\left(\frac{15}{8}\right).\end{aligned}\end{aligned}
$$

## q-347942 exact original (ineligible raw operator capture)

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /18}^{\pi /6}\frac{\operatorname{cot}⁡(3x)}{{sin}^{4}⁡(3x)}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{5}{4}$ (correct)

We use the identity $\operatorname{cot}⁡3x=\frac{\operatorname{cos}⁡3x}{\operatorname{sin}⁡3x}$ and rewrite the integral as

$$
\begin{aligned}{\int }_{\pi /18}^{\pi /6}\frac{\operatorname{cot}⁡(3x)}{{sin}^{4}⁡(3x)}\,\text{d}x & ={\int }_{\pi /18}^{\pi /6}\frac{1}{{sin}^{4}⁡(3x)}\cdot \frac{\operatorname{cos}⁡3x}{\operatorname{sin}⁡3x}\,\text{d}x \\  & ={\int }_{\pi /18}^{\pi /6}\frac{1}{{sin}^{5}⁡(3x)}\cdot \operatorname{cos}⁡3x\,\text{d}x.\end{aligned}
$$

We can solve this by substitution. Let $u=\operatorname{sin}⁡3x.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=3\operatorname{cos}⁡3x\,⟹\,\frac{1}{3}\text{d}u=\operatorname{cos}⁡3x\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{sin}⁡3x.$

| $x$ | $\frac{\pi }{18}$ | $\frac{\pi }{6}$ |
| --- | --- | --- |
| $u$ | $\frac{1}{2}$ | $1$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{\pi /18}^{\pi /6}\frac{1}{{sin}^{5}⁡(3x)}\cdot \operatorname{cos}⁡3x\,\text{d}x & ={\int }_{1/2}^{1}\frac{1}{{u}^{5}}\,\cdot \frac{1}{3}\text{d}u \\  & =\frac{1}{3}{\int }_{1/2}^{1}{u}^{-5}\,\text{d}u \\  & =\frac{1}{3}(\frac{{u}^{-4}}{-4}){|}_{1/2}^{1} \\  & =-\frac{1}{12}(\frac{1}{{u}^{4}}){|}_{1/2}^{1} \\  & =-\frac{1}{12}(\frac{1}{{1}^{4}}-{(\frac{2}{1})}^{4}) \\  & =-\frac{1}{12}(1-16) \\  & =\frac{5}{4}.\end{aligned}\end{aligned}
$$

### Changed a=2,k=3 (normal notation repair where needed)

Evaluate the following integral. Do not round the answer.

$3\cdot \int_{\frac{\pi}{36}}^{\frac{\pi}{12}}\frac{\operatorname{cot}⁡({6x})}{\operatorname{sin}^{4}⁡({6x})}\,\text{d}x=$
{{field-1}}

Field field-1 (blank)

- $\frac{15}{8}$ (correct)

We use the identity $\operatorname{cot}⁡{6x}=\frac{\operatorname{cos}⁡{6x}}{\operatorname{sin}⁡{6x}}$ and rewrite the integral as

$$
\begin{aligned}3\cdot \int_{\frac{\pi}{36}}^{\frac{\pi}{12}}\frac{\operatorname{cot}⁡({6x})}{\operatorname{sin}^{4}⁡({6x})}\,\text{d}x &=3\cdot \int_{\frac{\pi}{36}}^{\frac{\pi}{12}}\frac{1}{\operatorname{sin}^{4}⁡({6x})}\cdot \frac{\operatorname{cos}⁡{6x}}{\operatorname{sin}⁡{6x}}\,\text{d}x \\  &=3\cdot \int_{\frac{\pi}{36}}^{\frac{\pi}{12}}\frac{1}{\operatorname{sin}^{5}⁡({6x})}\cdot \operatorname{cos}⁡{6x}\,\text{d}x.\end{aligned}
$$

We can solve this by substitution. Let $u=\operatorname{sin}⁡{6x}.$ Then 

$$
\frac{\text{d}u}{\text{d}x}=2\left(3\operatorname{cos}⁡{6x}\right)\,⟹\,\frac{1}{2}\left(\frac{1}{3}\text{d}u\right)=\operatorname{cos}⁡{6x}\,\text{d}x.
$$

Now, we fill the table for the limits of integration, according to the rule $u=\operatorname{sin}⁡{6x}.$

| $x$ | $\frac{\pi}{36}$ | $\frac{\pi}{12}$ |
| --- | --- | --- |
| $u$ | $\frac{1}{2}$ | $1$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}3\cdot \int_{\frac{\pi}{36}}^{\frac{\pi}{12}}\frac{1}{\operatorname{sin}^{5}⁡({6x})}\cdot \operatorname{cos}⁡{6x}\,\text{d}x &=\frac{3}{2}\cdot {\int }_{1/2}^{1}\frac{1}{{u}^{5}}\,\cdot \frac{1}{3}\text{d}u \\  &=\frac{3}{2}\cdot \frac{1}{3}{\int }_{1/2}^{1}{u}^{-5}\,\text{d}u \\  &=\frac{3}{2}\left(\frac{1}{3}(\frac{{u}^{-4}}{-4}){|}_{1/2}^{1}\right) \\  &=\frac{3}{2}\left(-\frac{1}{12}(\frac{1}{{u}^{4}}){|}_{1/2}^{1}\right) \\  &=\frac{3}{2}\left(-\frac{1}{12}(\frac{1}{{1}^{4}}-{(\frac{2}{1})}^{4})\right) \\  &=\frac{3}{2}\left(-\frac{1}{12}(1-16)\right) \\  &=\frac{3}{2}\left(\frac{5}{4}\right).\end{aligned}\end{aligned}
$$
