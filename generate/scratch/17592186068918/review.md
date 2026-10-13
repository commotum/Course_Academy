## original q-49557

What is $\displaystyle \int\frac{2\cos y}{\sin y}dy$?

Missing source solution

## variant q-49557

What is $\int \frac{4 \cos{\left(x \right)}}{\sin{\left(x \right)}}\,\text{d}x$?

- $2\ln|\cos{\left(x \right)}|+C$
- $2\ln|\sin{\left(x \right)}|+C$
- $4\ln|\cos{\left(x \right)}|+C$
- $2\ln|\cos{\left(2 x \right)}|+C$
- $4\ln|\sin{\left(x \right)}|+C$ (correct)

Let $u=\sin{\left(x \right)},$ then

$$
\frac{\text{d}u}{\text{d}x}=\cos{\left(x \right)}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{4 \cos{\left(x \right)}}{\sin{\left(x \right)}}\,\text{d}x &= 4\int \frac{1}{u}\,\text{d}u \\ &= 4\ln|u|+C \\ &= 4\ln|\sin{\left(x \right)}|+C\end{aligned}
$$

## original q-113998

Calculate $\int \frac{2\operatorname{csc}⁡x\operatorname{cot}⁡x}{\operatorname{csc}⁡x+2}\,\text{d}x.$

Let $u=\operatorname{csc}⁡x+2.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=-\operatorname{csc}⁡x\operatorname{cot}⁡x\,⟹\,-\text{d}u=\operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{2\operatorname{csc}⁡x\operatorname{cot}⁡x}{\operatorname{csc}⁡x+2}\,\text{d}x & =2\int \frac{1}{\operatorname{csc}⁡x+2}\cdot \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & =2\int \frac{1}{u}\cdot (-\text{d}u) \\  & =-2\int \frac{1}{u}\,\text{d}u \\  & =-2\operatorname{ln}⁡|u|+C \\  & =-2\operatorname{ln}⁡|\operatorname{csc}⁡x+2|+C\end{aligned}
$$

## variant q-113998

Calculate $\int \frac{4 \cot{\left(x \right)} \csc{\left(x \right)}}{\csc{\left(x \right)} + 2}\,\text{d}x.$

- $2\ln|\csc{\left(x \right)}|+C$
- $-4\ln|\csc{\left(x \right)}|+C$
- $4\ln|\csc{\left(x \right)} + 2|+C$
- $2\ln|\csc{\left(x \right)} + 2|+C$
- $-4\ln|\csc{\left(x \right)} + 2|+C$ (correct)

Let $u=\csc{\left(x \right)} + 2,$ then

$$
\frac{\text{d}u}{\text{d}x}=- \cot{\left(x \right)} \csc{\left(x \right)}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{4 \cot{\left(x \right)} \csc{\left(x \right)}}{\csc{\left(x \right)} + 2}\,\text{d}x &= -4\int \frac{1}{u}\,\text{d}u \\ &= -4\ln|u|+C \\ &= -4\ln|\csc{\left(x \right)} + 2|+C\end{aligned}
$$

## original q-350887

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /2}\frac{2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)}{{sin}^{2}⁡(x)+3}\,\text{d}x=$
{{field-1}}

If we let $u={sin}^{2}⁡(x)+3,$ then

$$
\frac{\text{d}u}{\text{d}x}=2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)\,⟹\,\text{d}u=2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\pi /2$ |
| --- | --- | --- |
| $u$ | $3$ | $4$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\pi /2}\frac{2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)}{{sin}^{2}⁡(x)+3}\,\text{d}x & ={\int }_{0}^{\pi /2}\frac{1}{{sin}^{2}⁡(x)+3}\cdot 2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)\,\text{d}x \\  & ={\int }_{3}^{4}\frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|\,{|}_{3}^{4} \\  & =\operatorname{ln}⁡4-\operatorname{ln}⁡3 \\  & =\operatorname{ln}⁡(\frac{4}{3})\end{aligned}
$$

## variant q-350887

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\frac{\pi}{2}}\frac{4 \sin{\left(x \right)} \cos{\left(x \right)}}{\sin^{2}{\left(x \right)} + 3}\,\text{d}x=$
{{field-1}}

- $2 \ln{\left(\frac{4}{3} \right)}$ (correct)

Let $u=\sin^{2}{\left(x \right)} + 3,$ then

$$
\frac{\text{d}u}{\text{d}x}=2 \sin{\left(x \right)} \cos{\left(x \right)}.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{\pi}{2}$ |
| --- | --- | --- |
| $u$ | $3$ | $4$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\frac{\pi}{2}}\frac{4 \sin{\left(x \right)} \cos{\left(x \right)}}{\sin^{2}{\left(x \right)} + 3}\,\text{d}x &= 2{\int }_{3}^{4}\frac{1}{u}\,\text{d}u \\ &= 2 \ln{\left(u \right)}\big|_{3}^{4} \\ &= 2 \ln{\left(4 \right)}-(2 \ln{\left(3 \right)}) \\ &= \ln{\left(\frac{16}{9} \right)}\end{aligned}
$$

## original q-350901

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /3}^{\pi /2}\frac{24\operatorname{sin}⁡(x){cos}^{2}⁡(x)}{8{cos}^{3}⁡(x)+5}\,\text{d}x=$
{{field-1}}

If we let $u=8{cos}^{3}⁡(x)+5,$ then

$$
\frac{\text{d}}{\text{d}x}(8{cos}^{3}⁡(x)+5)=-24{cos}^{2}⁡(x)\operatorname{sin}⁡(x).
$$

So, differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=-24{cos}^{2}⁡(x)\operatorname{sin}⁡(x)\,⟹\,-\text{d}u=24\operatorname{sin}⁡(x){cos}^{2}⁡(x)\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $\pi /3$ | $\pi /2$ |
| --- | --- | --- |
| $u$ | $6$ | $5$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{\pi /3}^{\pi /2}\frac{24\operatorname{sin}⁡(x){cos}^{2}⁡(x)}{8{cos}^{3}⁡(x)+5}\,\text{d}x & ={\int }_{\pi /3}^{\pi /2}\frac{1}{8{cos}^{3}⁡(x)+5}\cdot 24\operatorname{sin}⁡(x){cos}^{2}⁡(x)\,\text{d}x \\  & ={\int }_{6}^{5}\frac{1}{u}\cdot (-\text{d}u) \\  & =-{\int }_{6}^{5}\frac{1}{u}\,\text{d}u \\  & =-\operatorname{ln}⁡|u|{|}_{6}^{5} \\  & =-(\operatorname{ln}⁡5-\operatorname{ln}⁡6) \\  & =\operatorname{ln}⁡(\frac{6}{5})\end{aligned}
$$

## variant q-350901

Evaluate the following integral. Do not round the answer.

${\int }_{\frac{\pi}{3}}^{\frac{\pi}{2}}\frac{48 \sin{\left(x \right)} \cos^{2}{\left(x \right)}}{8 \cos^{3}{\left(x \right)} + 5}\,\text{d}x=$
{{field-1}}

- $2 \ln{\left(\frac{6}{5} \right)}$ (correct)

Let $u=8 \cos^{3}{\left(x \right)} + 5,$ then

$$
\frac{\text{d}u}{\text{d}x}=- 24 \sin{\left(x \right)} \cos^{2}{\left(x \right)}.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{\pi}{3}$ | $\frac{\pi}{2}$ |
| --- | --- | --- |
| $u$ | $6$ | $5$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{\frac{\pi}{3}}^{\frac{\pi}{2}}\frac{48 \sin{\left(x \right)} \cos^{2}{\left(x \right)}}{8 \cos^{3}{\left(x \right)} + 5}\,\text{d}x &= -2{\int }_{6}^{5}\frac{1}{u}\,\text{d}u \\ &= - 2 \ln{\left(u \right)}\big|_{6}^{5} \\ &= - 2 \ln{\left(5 \right)}-(- 2 \ln{\left(6 \right)}) \\ &= \ln{\left(\frac{36}{25} \right)}\end{aligned}
$$

## original q-350904

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /6}^{\pi /2}\frac{\operatorname{csc}⁡(x)\operatorname{cot}⁡(x)}{2+\operatorname{csc}⁡(x)}\,\text{d}x=$
{{field-1}}

If we let $u=2+\operatorname{csc}⁡(x),$ then

$$
\frac{\text{d}u}{\text{d}x}=-\operatorname{csc}⁡(x)\operatorname{cot}⁡(x)\,⟹\,-\text{d}u=\operatorname{csc}⁡(x)\operatorname{cot}⁡(x)\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $\pi /6$ | $\pi /2$ |
| --- | --- | --- |
| $u$ | $4$ | $3$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{\pi /6}^{\pi /2}\frac{\operatorname{csc}⁡(x)\operatorname{cot}⁡(x)}{2+\operatorname{csc}⁡(x)}\,\text{d}x & ={\int }_{\pi /6}^{\pi /2}\frac{1}{2+\operatorname{csc}⁡(x)}\cdot (\operatorname{csc}⁡(x)\operatorname{cot}⁡(x))\,\text{d}x \\  & ={\int }_{4}^{3}\frac{1}{u}\,(-\text{d}u) \\  & =-{\int }_{4}^{3}\frac{1}{u}\,\text{d}u \\  & =-\operatorname{ln}⁡|u|{|}_{4}^{3} \\  & =-(\operatorname{ln}⁡3-\operatorname{ln}⁡4) \\  & =\operatorname{ln}⁡(\frac{4}{3})\end{aligned}
$$

## variant q-350904

Evaluate the following integral. Do not round the answer.

${\int }_{\frac{\pi}{6}}^{\frac{\pi}{2}}\frac{2 \cot{\left(x \right)} \csc{\left(x \right)}}{\csc{\left(x \right)} + 2}\,\text{d}x=$
{{field-1}}

- $2 \ln{\left(\frac{4}{3} \right)}$
- $2 \ln{\left(\frac{4}{3} \right)}$ (correct)

Let $u=\csc{\left(x \right)} + 2,$ then

$$
\frac{\text{d}u}{\text{d}x}=- \cot{\left(x \right)} \csc{\left(x \right)}.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{\pi}{6}$ | $\frac{\pi}{2}$ |
| --- | --- | --- |
| $u$ | $4$ | $3$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{\frac{\pi}{6}}^{\frac{\pi}{2}}\frac{2 \cot{\left(x \right)} \csc{\left(x \right)}}{\csc{\left(x \right)} + 2}\,\text{d}x &= -2{\int }_{4}^{3}\frac{1}{u}\,\text{d}u \\ &= - 2 \ln{\left(u \right)}\big|_{4}^{3} \\ &= - 2 \ln{\left(3 \right)}-(- 2 \ln{\left(4 \right)}) \\ &= \ln{\left(\frac{16}{9} \right)}\end{aligned}
$$

## original q-73674

Calculate the integral $\int \frac{y\operatorname{cos}⁡({y}^{2})}{\operatorname{sin}⁡({y}^{2})}\,\text{d}y.$

Notice that the numerator is proportional to the derivative of the denominator, because

$$
\frac{\text{d}}{\text{d}y}(\operatorname{sin}⁡({y}^{2}))=2y\operatorname{cos}⁡({y}^{2}).
$$

So, let $u=\operatorname{sin}⁡({y}^{2}).$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}y}=2y\operatorname{cos}⁡({y}^{2})\,⟹\,\frac{1}{2}\,\text{d}u=y\operatorname{cos}⁡({y}^{2})\,\text{d}y.
$$

We now substitute and evaluate, as follows:

$$
\begin{aligned}\int \frac{y\operatorname{cos}⁡({y}^{2})}{\operatorname{sin}⁡({y}^{2})}\,\text{d}y & =\int \frac{1}{\operatorname{sin}⁡({y}^{2})}\cdot (y\operatorname{cos}⁡({y}^{2}))\,\text{d}y \\  & =\int \frac{1}{u}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int \frac{1}{u}\,\text{d}u \\  & =\frac{1}{2}\operatorname{ln}⁡|u|+C \\  & =\frac{1}{2}\operatorname{ln}⁡|\operatorname{sin}⁡({y}^{2})|+C\end{aligned}
$$

## variant q-73674

Calculate $\int \frac{2 x \cos{\left(x^{2} \right)}}{\sin{\left(x^{2} \right)}}\,\text{d}x.$

- $2\ln|\cos{\left(x^{2} \right)}|+C$
- $\ln|\cos{\left(x^{2} \right)}|+C$
- $2\ln|\sin{\left(x^{2} \right)}|+C$
- $4\ln|\cos{\left(x^{2} \right)}|+C$
- $\ln|\sin{\left(x^{2} \right)}|+C$ (correct)

Let $u=\sin{\left(x^{2} \right)},$ then

$$
\frac{\text{d}u}{\text{d}x}=2 x \cos{\left(x^{2} \right)}.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{2 x \cos{\left(x^{2} \right)}}{\sin{\left(x^{2} \right)}}\,\text{d}x &= 1\int \frac{1}{u}\,\text{d}u \\ &= \ln|u|+C \\ &= \ln|\sin{\left(x^{2} \right)}|+C\end{aligned}
$$

## original q-113997

Calculate $\int \frac{{sec}^{2}⁡x\operatorname{tan}⁡x}{\operatorname{tan}⁡x+1}\,\text{d}x.$

Let $u=\operatorname{tan}⁡x+1.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}={sec}^{2}⁡x\,⟹\,\text{d}u={sec}^{2}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{{sec}^{2}⁡x\operatorname{tan}⁡x}{\operatorname{tan}⁡x+1}\,\text{d}x & =\int \frac{1}{\operatorname{tan}⁡x+1}\cdot {sec}^{2}⁡x\operatorname{tan}⁡x\,\text{d}x \\  & =\int \frac{1}{\operatorname{tan}⁡x+1}\cdot \operatorname{tan}⁡x\cdot {sec}^{2}⁡x\,\text{d}x \\  & =\int \frac{1}{u}(u-1)\text{d}u \\  & =\int (1-\frac{1}{u})\,\text{d}u \\  & =u-\operatorname{ln}⁡|u|+C \\  & =(\operatorname{tan}⁡x+1)-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|+C \\  & =\operatorname{tan}⁡x-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|+K\end{aligned}
$$

where $K=C+1.$

## variant q-113997

Calculate $\int \left(1 - \frac{1}{\tan{\left(x \right)} + 1}\right) \left(2 \tan^{2}{\left(x \right)} + 2\right)\,\text{d}x.$

- $\tan^{2}{\left(x \right)}- 2 \tan{\left(x \right)}+C$
- $-2\ln|\tan{\left(x \right)} + 1|+2 \tan{\left(x \right)}+C$ (correct)
- $-2\ln|\tan{\left(x \right)} + 1|+2 \tan{\left(x - 1 \right)}+C$
- $-2\ln|\tan{\left(x \right)}|+2 \tan{\left(x + 1 \right)}+C$
- $-2\ln|\tan{\left(x \right)}|+2 \tan{\left(x \right)}+C$

Let $u=\tan{\left(x \right)} + 1,$ then

$$
\frac{\text{d}u}{\text{d}x}=\tan^{2}{\left(x \right)} + 1.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \left(1 - \frac{1}{\tan{\left(x \right)} + 1}\right) \left(2 \tan^{2}{\left(x \right)} + 2\right)\,\text{d}x &= 2\int 1 - \frac{1}{u}\,\text{d}u \\ &= -2\ln|u|+2 u+C \\ &= 2-2\ln|\tan{\left(x \right)} + 1|+2 \tan{\left(x \right)}+C\end{aligned}
$$