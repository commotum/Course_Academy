## Original evidence q-10046

Evaluate the integral
$\displaystyle \int_{0}^{π/4}\frac{\sec x\tan x}{1 + \sec x}dx$.

- $\ln (1 + \sqrt{2}) + \ln 2$
- $\ln (1 + \sqrt{2}) - \ln 2$
- $1 + \sqrt{2} - \ln 2$
- $\ln (1 - \sqrt{2}) - \ln 2$
- $\ln (1 - \sqrt{2}) + \ln 2$

[Source has no worked solution.]

## Changed evidence q-10046

Evaluate the integral
$\displaystyle \int_{0}^{π/4}2\cdot \frac{\sec x\tan x}{1 + \sec x}dx$.

- $2\left(\ln (1 + \sqrt{2}) + \ln 2\right)$
- $2\left(\ln (1 + \sqrt{2}) - \ln 2\right)$
- $2\left(1 + \sqrt{2} - \ln 2\right)$
- $2\left(\ln (1 - \sqrt{2}) - \ln 2\right)$
- $2\left(\ln (1 - \sqrt{2}) + \ln 2\right)$

[Source has no worked solution.]

## Normal authored bank q-10046

Evaluate the integral
$\displaystyle \int_{0}^{π/4}2\cdot \frac{\sec x\tan x}{1 + \sec x}dx$.

- $2 \ln{\left(2 \right)} + 2 \ln{\left(1 + \sqrt{2} \right)}$
- $- 2 \ln{\left(1 + \sqrt{2} \right)} + 2 \ln{\left(2 \right)}$
- $- 2 \ln{\left(2 \right)} + 2 \ln{\left(1 + \sqrt{2} \right)}$ (correct)
- $- 2 \ln{\left(2 \right)}$
- $2 \ln{\left(1 + \sqrt{2} \right)}$

Let $u=\sec{\left(x \right)} + 1.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=\tan{\left(x \right)} \sec{\left(x \right)}\,⟹\,\text{d}u=\tan{\left(x \right)} \sec{\left(x \right)}\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{\pi}{4}$ |
| --- | --- | --- |
| $u$ | $2$ | $1 + \sqrt{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\pi}{4}} \frac{2 \tan{\left(x \right)} \sec{\left(x \right)}}{\sec{\left(x \right)} + 1}\,\text{d}x &= \int_{0}^{\frac{\pi}{4}} \frac{1}{\sec{\left(x \right)} + 1}\cdot (2 \tan{\left(x \right)} \sec{\left(x \right)})\,\text{d}x \\ &= \int_{2}^{1 + \sqrt{2}}\frac{1}{u}\cdot 2\,\text{d}u \\ &= 2\ln|u|\big|_{2}^{1 + \sqrt{2}} \\ &= 2\left(\ln(1 + \sqrt{2})-\ln(2)\right) \\ &= 2\left(- \ln{\left(2 \right)} + \ln{\left(1 + \sqrt{2} \right)}\right)\end{aligned}
$$

## Original evidence q-49557

What is $\displaystyle \int\frac{2\cos y}{\sin y}dy$?

- $2\ln \mid \cos y \mid + C$
- $\ln \mid \sin y \mid + C$
- $\ln \mid \cos y \mid + C$
- $2\ln \mid \sin y \mid + C$
- $\ln \mid \cos 2y \mid + C$

[Source has no worked solution.]

## Changed evidence q-49557

What is $\displaystyle \int2\cdot \frac{2\cos y}{\sin y}dy$?

- $2\left(2\ln \mid \cos y \mid + C\right)$
- $2\left(\ln \mid \sin y \mid + C\right)$
- $2\left(\ln \mid \cos y \mid + C\right)$
- $2\left(2\ln \mid \sin y \mid + C\right)$
- $2\left(\ln \mid \cos 2y \mid + C\right)$

[Source has no worked solution.]

## Normal authored bank q-49557

What is $\displaystyle \int2\cdot \frac{2\cos y}{\sin y}dy$?

- $- 4 \ln|\sin{\left(y \right)}|+C$
- $4 \ln|\cos{\left(y \right)}|+C$
- $4 \ln|\sin{\left(y \right)}|+C$ (correct)
- $- \frac{4}{\sin{\left(y \right)}}+C$
- $4 \sin{\left(y \right)}+C$

Let $u=\sin{\left(y \right)}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}y}=\cos{\left(y \right)}\,⟹\,\text{d}u=\cos{\left(y \right)}\,\text{d}y.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{4 \cos{\left(y \right)}}{\sin{\left(y \right)}}\,\text{d}y &= \int \frac{1}{\sin{\left(y \right)}}\cdot (4 \cos{\left(y \right)})\,\text{d}y \\ &= \int \frac{1}{u}\cdot 4\,\text{d}u \\ &= 4\int \frac{1}{u}\,\text{d}u \\ &= 4 \ln|u|+C \\ &= 4 \ln|\sin{\left(y \right)}|+C\end{aligned}
$$

## Original evidence q-10045

${\int }_{-1}^{1}\frac{\operatorname{cos}⁡x}{1+\operatorname{sin}⁡x}\,\text{d}x=$

- $\operatorname{ln}⁡(2-\operatorname{sin}⁡(1))+\operatorname{ln}⁡(2+\operatorname{sin}⁡(1))$
- $\operatorname{ln}⁡(1-\operatorname{sin}⁡(2))-\operatorname{ln}⁡(1+\operatorname{sin}⁡(2))$
- $\operatorname{ln}⁡(2+\operatorname{sin}⁡(1))+\operatorname{ln}⁡(2-\operatorname{sin}⁡(1))$
- $-\operatorname{ln}⁡(1+\operatorname{sin}⁡(2))-\operatorname{ln}⁡(1-\operatorname{sin}⁡(2))$
- $\operatorname{ln}⁡(1+\operatorname{sin}⁡(1))-\operatorname{ln}⁡(1-\operatorname{sin}⁡(1))$ (correct)

Notice that the numerator is proportional to the derivative of the denominator, because

$$
\frac{\text{d}}{\text{d}x}(1+\operatorname{sin}⁡x)=\operatorname{cos}⁡x.
$$

So, let $u=1+\operatorname{sin}⁡x.$ Differentiating, we have 

$$
\frac{\text{d}u}{\text{d}x}=\operatorname{cos}⁡x\,⟹\,\text{d}u=\operatorname{cos}⁡x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $-1$ | $1$ |
| --- | --- | --- |
| $u$ | $1-\operatorname{sin}⁡(1)$ | $1+\operatorname{sin}⁡(1)$ |

We now substitute and evaluate, as follows:

$$
\begin{aligned}{\int }_{-1}^{1}\frac{\operatorname{cos}⁡x}{1+\operatorname{sin}⁡x}\,\text{d}x & ={\int }_{-1}^{1}\frac{1}{1+\operatorname{sin}⁡x}\cdot \operatorname{cos}⁡x\,\text{d}x \\  & ={\int }_{1-\operatorname{sin}⁡(1)}^{1+\operatorname{sin}⁡(1)}\frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|{|}_{1-\operatorname{sin}⁡(1)}^{1+\operatorname{sin}⁡(1)} \\  & =\operatorname{ln}⁡(1+\operatorname{sin}⁡(1))-\operatorname{ln}⁡(1-\operatorname{sin}⁡(1))\end{aligned}
$$

## Changed evidence q-10045

${\int }_{-1}^{1}2\cdot \frac{\operatorname{cos}⁡x}{1+\operatorname{sin}⁡x}\,\text{d}x=$

- $2\left(\operatorname{ln}⁡(2-\operatorname{sin}⁡(1))+\operatorname{ln}⁡(2+\operatorname{sin}⁡(1))\right)$
- $2\left(\operatorname{ln}⁡(1-\operatorname{sin}⁡(2))-\operatorname{ln}⁡(1+\operatorname{sin}⁡(2))\right)$
- $2\left(\operatorname{ln}⁡(2+\operatorname{sin}⁡(1))+\operatorname{ln}⁡(2-\operatorname{sin}⁡(1))\right)$
- $2\left(-\operatorname{ln}⁡(1+\operatorname{sin}⁡(2))-\operatorname{ln}⁡(1-\operatorname{sin}⁡(2))\right)$
- $2\left(\operatorname{ln}⁡(1+\operatorname{sin}⁡(1))-\operatorname{ln}⁡(1-\operatorname{sin}⁡(1))\right)$ (correct)

Notice that the numerator is proportional to the derivative of the denominator, because

$$
\frac{\text{d}}{\text{d}x}(1+\operatorname{sin}⁡x)=\operatorname{cos}⁡x.
$$

So, let $u=1+\operatorname{sin}⁡x.$ Differentiating, we have 

$$
\frac{\text{d}u}{\text{d}x}=\operatorname{cos}⁡x\,⟹\,\text{d}u=\operatorname{cos}⁡x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $-1$ | $1$ |
| --- | --- | --- |
| $u$ | $1-\operatorname{sin}⁡(1)$ | $1+\operatorname{sin}⁡(1)$ |

We now substitute and evaluate, as follows:

$$
\begin{aligned}{\int }_{-1}^{1}2\cdot \frac{\operatorname{cos}⁡x}{1+\operatorname{sin}⁡x}\,\text{d}x & ={\int }_{-1}^{1}2\cdot \frac{1}{1+\operatorname{sin}⁡x}\cdot \operatorname{cos}⁡x\,\text{d}x \\  & ={\int }_{1-\operatorname{sin}⁡(1)}^{1+\operatorname{sin}⁡(1)}2\cdot \frac{1}{u}\,\text{d}u \\  & =2\left(\operatorname{ln}⁡|u|{|}_{1-\operatorname{sin}⁡(1)}^{1+\operatorname{sin}⁡(1)}\right) \\  & =2\left(\operatorname{ln}⁡(1+\operatorname{sin}⁡(1))-\operatorname{ln}⁡(1-\operatorname{sin}⁡(1))\right)\end{aligned}
$$

## Normal authored bank q-10045

${\int }_{-1}^{1}2\cdot \frac{\operatorname{cos}⁡x}{1+\operatorname{sin}⁡x}\,\text{d}x=$

- $2 \ln{\left(1 - \sin{\left(1 \right)} \right)} + 2 \ln{\left(\sin{\left(1 \right)} + 1 \right)}$
- $2 \ln{\left(1 - \sin{\left(1 \right)} \right)} - 2 \ln{\left(\sin{\left(1 \right)} + 1 \right)}$
- $2 \ln{\left(\sin{\left(1 \right)} + 1 \right)} - 2 \ln{\left(1 - \sin{\left(1 \right)} \right)}$ (correct)
- $- 2 \ln{\left(1 - \sin{\left(1 \right)} \right)}$
- $2 \ln{\left(\sin{\left(1 \right)} + 1 \right)}$

Notice that the numerator is proportional to the derivative of the denominator, because

$$
\frac{\text{d}}{\text{d}x}(1+\operatorname{sin}⁡x)=\operatorname{cos}⁡x.
$$

So, let $u=1+\operatorname{sin}⁡x.$ Differentiating, we have 

$$
\frac{\text{d}u}{\text{d}x}=\operatorname{cos}⁡x\,⟹\,\text{d}u=\operatorname{cos}⁡x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $-1$ | $1$ |
| --- | --- | --- |
| $u$ | $1-\operatorname{sin}⁡(1)$ | $1+\operatorname{sin}⁡(1)$ |

We now substitute and evaluate, as follows:

$$
\begin{aligned}{\int }_{-1}^{1}2\cdot \frac{\operatorname{cos}⁡x}{1+\operatorname{sin}⁡x}\,\text{d}x & ={\int }_{-1}^{1}2\cdot \frac{1}{1+\operatorname{sin}⁡x}\cdot \operatorname{cos}⁡x\,\text{d}x \\  & ={\int }_{1-\operatorname{sin}⁡(1)}^{1+\operatorname{sin}⁡(1)}2\cdot \frac{1}{u}\,\text{d}u \\  & =2\left(\operatorname{ln}⁡|u|{|}_{1-\operatorname{sin}⁡(1)}^{1+\operatorname{sin}⁡(1)}\right) \\  & =2\left(\operatorname{ln}⁡(1+\operatorname{sin}⁡(1))-\operatorname{ln}⁡(1-\operatorname{sin}⁡(1))\right)\end{aligned}
$$

## Original evidence q-113998

Calculate $\int \frac{2\operatorname{csc}⁡x\operatorname{cot}⁡x}{\operatorname{csc}⁡x+2}\,\text{d}x.$

- $2\operatorname{ln}⁡|\operatorname{csc}⁡x+2|+C$
- $-2\operatorname{ln}⁡|\operatorname{csc}⁡x|+C$
- $\operatorname{ln}⁡|\operatorname{csc}⁡x|+C$
- $-2\operatorname{ln}⁡|\operatorname{csc}⁡x+2|+C$ (correct)
- $\operatorname{ln}⁡|\operatorname{csc}⁡x+2|+C$

Let $u=\operatorname{csc}⁡x+2.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=-\operatorname{csc}⁡x\operatorname{cot}⁡x\,⟹\,-\text{d}u=\operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{2\operatorname{csc}⁡x\operatorname{cot}⁡x}{\operatorname{csc}⁡x+2}\,\text{d}x & =2\int \frac{1}{\operatorname{csc}⁡x+2}\cdot \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & =2\int \frac{1}{u}\cdot (-\text{d}u) \\  & =-2\int \frac{1}{u}\,\text{d}u \\  & =-2\operatorname{ln}⁡|u|+C \\  & =-2\operatorname{ln}⁡|\operatorname{csc}⁡x+2|+C\end{aligned}
$$

## Changed evidence q-113998

Calculate $\int2\cdot  \frac{2\operatorname{csc}⁡x\operatorname{cot}⁡x}{\operatorname{csc}⁡x+2}\,\text{d}x.$

- $2\left(2\operatorname{ln}⁡|\operatorname{csc}⁡x+2|\right)+C$
- $2\left(-2\operatorname{ln}⁡|\operatorname{csc}⁡x|\right)+C$
- $2\left(\operatorname{ln}⁡|\operatorname{csc}⁡x|\right)+C$
- $2\left(-2\operatorname{ln}⁡|\operatorname{csc}⁡x+2|\right)+C$ (correct)
- $2\left(\operatorname{ln}⁡|\operatorname{csc}⁡x+2|\right)+C$

Let $u=\operatorname{csc}⁡x+2.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=-\operatorname{csc}⁡x\operatorname{cot}⁡x\,⟹\,-\text{d}u=\operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int2\cdot  \frac{2\operatorname{csc}⁡x\operatorname{cot}⁡x}{\operatorname{csc}⁡x+2}\,\text{d}x & =2\int2\cdot  \frac{1}{\operatorname{csc}⁡x+2}\cdot \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & =2\int2\cdot  \frac{1}{u}\cdot (-\text{d}u) \\  & =-2\int2\cdot  \frac{1}{u}\,\text{d}u \\  & =2\left(-2\operatorname{ln}⁡|u|\right)+C \\  & =2\left(-2\operatorname{ln}⁡|\operatorname{csc}⁡x+2|\right)+C\end{aligned}
$$

## Normal authored bank q-113998

Calculate $\int2\cdot  \frac{2\operatorname{csc}⁡x\operatorname{cot}⁡x}{\operatorname{csc}⁡x+2}\,\text{d}x.$

- $- 2 \ln|\csc{\left(x \right)} + 2|+C$
- $4 \ln|\csc{\left(x \right)} + 2|+C$
- $- 4 \ln|\csc{\left(x \right)} + 2|+C$ (correct)
- $\frac{4}{\csc{\left(x \right)} + 2}+C$
- $- 4 \ln|\csc{\left(x \right)}|+C$

Let $u=\operatorname{csc}⁡x+2.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=-\operatorname{csc}⁡x\operatorname{cot}⁡x\,⟹\,-\text{d}u=\operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int2\cdot  \frac{2\operatorname{csc}⁡x\operatorname{cot}⁡x}{\operatorname{csc}⁡x+2}\,\text{d}x & =2\int2\cdot  \frac{1}{\operatorname{csc}⁡x+2}\cdot \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & =2\int2\cdot  \frac{1}{u}\cdot (-\text{d}u) \\  & =-2\int2\cdot  \frac{1}{u}\,\text{d}u \\  & =2\left(-2\operatorname{ln}⁡|u|\right)+C \\  & =2\left(-2\operatorname{ln}⁡|\operatorname{csc}⁡x+2|\right)+C\end{aligned}
$$

## Original evidence q-350887

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /2}\frac{2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)}{{sin}^{2}⁡(x)+3}\,\text{d}x=$
{{field-1}}

- $\operatorname{ln}(\frac{4}{3})$ (correct)

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

## Changed evidence q-350887

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /2}2\cdot \frac{2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)}{{sin}^{2}⁡(x)+3}\,\text{d}x=$
{{field-1}}

- $2\left(\operatorname{ln}(\frac{4}{3})\right)$ (correct)

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
\begin{aligned}{\int }_{0}^{\pi /2}2\cdot \frac{2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)}{{sin}^{2}⁡(x)+3}\,\text{d}x & ={\int }_{0}^{\pi /2}2\cdot \frac{1}{{sin}^{2}⁡(x)+3}\cdot 2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)\,\text{d}x \\  & ={\int }_{3}^{4}2\cdot \frac{1}{u}\,\text{d}u \\  & =2\left(\operatorname{ln}⁡|u|\,{|}_{3}^{4}\right) \\  & =2\left(\operatorname{ln}⁡4-\operatorname{ln}⁡3\right) \\  & =2\left(\operatorname{ln}⁡(\frac{4}{3})\right)\end{aligned}
$$

## Normal authored bank q-350887

Evaluate the following integral. Give an exact answer.

${\int }_{0}^{\pi /2}2\cdot \frac{2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)}{{sin}^{2}⁡(x)+3}\,\text{d}x=$
{{field-1}}

- $2\left(\operatorname{ln}(\frac{4}{3})\right)$ (correct)

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
\begin{aligned}{\int }_{0}^{\pi /2}2\cdot \frac{2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)}{{sin}^{2}⁡(x)+3}\,\text{d}x & ={\int }_{0}^{\pi /2}2\cdot \frac{1}{{sin}^{2}⁡(x)+3}\cdot 2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)\,\text{d}x \\  & ={\int }_{3}^{4}2\cdot \frac{1}{u}\,\text{d}u \\  & =2\left(\operatorname{ln}⁡|u|\,{|}_{3}^{4}\right) \\  & =2\left(\operatorname{ln}⁡4-\operatorname{ln}⁡3\right) \\  & =2\left(\operatorname{ln}⁡(\frac{4}{3})\right)\end{aligned}
$$

## Original evidence q-350901

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /3}^{\pi /2}\frac{24\operatorname{sin}⁡(x){cos}^{2}⁡(x)}{8{cos}^{3}⁡(x)+5}\,\text{d}x=$
{{field-1}}

- $\operatorname{ln}(\frac{6}{5})$ (correct)

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

## Changed evidence q-350901

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /3}^{\pi /2}2\cdot \frac{24\operatorname{sin}⁡(x){cos}^{2}⁡(x)}{8{cos}^{3}⁡(x)+5}\,\text{d}x=$
{{field-1}}

- $2\left(\operatorname{ln}(\frac{6}{5})\right)$ (correct)

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
\begin{aligned}{\int }_{\pi /3}^{\pi /2}2\cdot \frac{24\operatorname{sin}⁡(x){cos}^{2}⁡(x)}{8{cos}^{3}⁡(x)+5}\,\text{d}x & ={\int }_{\pi /3}^{\pi /2}2\cdot \frac{1}{8{cos}^{3}⁡(x)+5}\cdot 24\operatorname{sin}⁡(x){cos}^{2}⁡(x)\,\text{d}x \\  & ={\int }_{6}^{5}2\cdot \frac{1}{u}\cdot (-\text{d}u) \\  & =-{\int }_{6}^{5}2\cdot \frac{1}{u}\,\text{d}u \\  & =2\left(-\operatorname{ln}⁡|u|{|}_{6}^{5}\right) \\  & =2\left(-(\operatorname{ln}⁡5-\operatorname{ln}⁡6)\right) \\  & =2\left(\operatorname{ln}⁡(\frac{6}{5})\right)\end{aligned}
$$

## Normal authored bank q-350901

Evaluate the following integral. Give an exact answer.

${\int }_{\pi /3}^{\pi /2}2\cdot \frac{24\operatorname{sin}⁡(x){cos}^{2}⁡(x)}{8{cos}^{3}⁡(x)+5}\,\text{d}x=$
{{field-1}}

- $2\left(\operatorname{ln}(\frac{6}{5})\right)$ (correct)

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
\begin{aligned}{\int }_{\pi /3}^{\pi /2}2\cdot \frac{24\operatorname{sin}⁡(x){cos}^{2}⁡(x)}{8{cos}^{3}⁡(x)+5}\,\text{d}x & ={\int }_{\pi /3}^{\pi /2}2\cdot \frac{1}{8{cos}^{3}⁡(x)+5}\cdot 24\operatorname{sin}⁡(x){cos}^{2}⁡(x)\,\text{d}x \\  & ={\int }_{6}^{5}2\cdot \frac{1}{u}\cdot (-\text{d}u) \\  & =-{\int }_{6}^{5}2\cdot \frac{1}{u}\,\text{d}u \\  & =2\left(-\operatorname{ln}⁡|u|{|}_{6}^{5}\right) \\  & =2\left(-(\operatorname{ln}⁡5-\operatorname{ln}⁡6)\right) \\  & =2\left(\operatorname{ln}⁡(\frac{6}{5})\right)\end{aligned}
$$

## Original evidence q-350904

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /6}^{\pi /2}\frac{\operatorname{csc}⁡(x)\operatorname{cot}⁡(x)}{2+\operatorname{csc}⁡(x)}\,\text{d}x=$
{{field-1}}

- $\operatorname{ln}(\frac{4}{3})$
- $\ln\left(\frac{4}{3}\right)$ (correct)

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

## Changed evidence q-350904

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /6}^{\pi /2}2\cdot \frac{\operatorname{csc}⁡(x)\operatorname{cot}⁡(x)}{2+\operatorname{csc}⁡(x)}\,\text{d}x=$
{{field-1}}

- $2\left(\operatorname{ln}(\frac{4}{3})\right)$
- $2\left(\ln\left(\frac{4}{3}\right)\right)$ (correct)

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
\begin{aligned}{\int }_{\pi /6}^{\pi /2}2\cdot \frac{\operatorname{csc}⁡(x)\operatorname{cot}⁡(x)}{2+\operatorname{csc}⁡(x)}\,\text{d}x & ={\int }_{\pi /6}^{\pi /2}2\cdot \frac{1}{2+\operatorname{csc}⁡(x)}\cdot (\operatorname{csc}⁡(x)\operatorname{cot}⁡(x))\,\text{d}x \\  & ={\int }_{4}^{3}2\cdot \frac{1}{u}\,(-\text{d}u) \\  & =-{\int }_{4}^{3}2\cdot \frac{1}{u}\,\text{d}u \\  & =2\left(-\operatorname{ln}⁡|u|{|}_{4}^{3}\right) \\  & =2\left(-(\operatorname{ln}⁡3-\operatorname{ln}⁡4)\right) \\  & =2\left(\operatorname{ln}⁡(\frac{4}{3})\right)\end{aligned}
$$

## Normal authored bank q-350904

Evaluate the following integral. Give an exact answer.

${\int }_{\pi /6}^{\pi /2}2\cdot \frac{\operatorname{csc}⁡(x)\operatorname{cot}⁡(x)}{2+\operatorname{csc}⁡(x)}\,\text{d}x=$
{{field-1}}

- $2\left(\ln\left(\frac{4}{3}\right)\right)$ (correct)

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
\begin{aligned}{\int }_{\pi /6}^{\pi /2}2\cdot \frac{\operatorname{csc}⁡(x)\operatorname{cot}⁡(x)}{2+\operatorname{csc}⁡(x)}\,\text{d}x & ={\int }_{\pi /6}^{\pi /2}2\cdot \frac{1}{2+\operatorname{csc}⁡(x)}\cdot (\operatorname{csc}⁡(x)\operatorname{cot}⁡(x))\,\text{d}x \\  & ={\int }_{4}^{3}2\cdot \frac{1}{u}\,(-\text{d}u) \\  & =-{\int }_{4}^{3}2\cdot \frac{1}{u}\,\text{d}u \\  & =2\left(-\operatorname{ln}⁡|u|{|}_{4}^{3}\right) \\  & =2\left(-(\operatorname{ln}⁡3-\operatorname{ln}⁡4)\right) \\  & =2\left(\operatorname{ln}⁡(\frac{4}{3})\right)\end{aligned}
$$

## Original evidence q-73674

Calculate the integral $\int \frac{y\operatorname{cos}⁡({y}^{2})}{\operatorname{sin}⁡({y}^{2})}\,\text{d}y.$

- $\operatorname{ln}⁡|\operatorname{sin}⁡({y}^{2})|+C$
- $\frac{1}{2}\operatorname{ln}⁡|\operatorname{cos}⁡({y}^{2})|+C$
- $\operatorname{ln}⁡|\operatorname{cos}⁡({y}^{2})|+C$
- $\frac{1}{2}\operatorname{ln}⁡|\operatorname{sin}⁡({y}^{2})|+C$ (correct)
- $2\operatorname{ln}⁡|\operatorname{cos}⁡({y}^{2})|+C$

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

## Changed evidence q-73674

Calculate the integral $\int2\cdot  \frac{y\operatorname{cos}⁡({y}^{2})}{\operatorname{sin}⁡({y}^{2})}\,\text{d}y.$

- $2\left(\operatorname{ln}⁡|\operatorname{sin}⁡({y}^{2})|\right)+C$
- $2\left(\frac{1}{2}\operatorname{ln}⁡|\operatorname{cos}⁡({y}^{2})|\right)+C$
- $2\left(\operatorname{ln}⁡|\operatorname{cos}⁡({y}^{2})|\right)+C$
- $2\left(\frac{1}{2}\operatorname{ln}⁡|\operatorname{sin}⁡({y}^{2})|\right)+C$ (correct)
- $2\left(2\operatorname{ln}⁡|\operatorname{cos}⁡({y}^{2})|\right)+C$

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
\begin{aligned}\int2\cdot  \frac{y\operatorname{cos}⁡({y}^{2})}{\operatorname{sin}⁡({y}^{2})}\,\text{d}y & =\int2\cdot  \frac{1}{\operatorname{sin}⁡({y}^{2})}\cdot (y\operatorname{cos}⁡({y}^{2}))\,\text{d}y \\  & =\int2\cdot  \frac{1}{u}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int2\cdot  \frac{1}{u}\,\text{d}u \\  & =2\left(\frac{1}{2}\operatorname{ln}⁡|u|\right)+C \\  & =2\left(\frac{1}{2}\operatorname{ln}⁡|\operatorname{sin}⁡({y}^{2})|\right)+C\end{aligned}
$$

## Normal authored bank q-73674

Calculate the integral $\int2\cdot  \frac{y\operatorname{cos}⁡({y}^{2})}{\operatorname{sin}⁡({y}^{2})}\,\text{d}y.$

- $- \ln|\sin{\left(y^{2} \right)}|+C$
- $2 \ln|\sin{\left(y^{2} \right)}|+C$
- $\ln|\sin{\left(y^{2} \right)}|+C$ (correct)
- $- \frac{1}{\sin{\left(y^{2} \right)}}+C$
- $\ln|\cos{\left(y^{2} \right)}|+C$

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
\begin{aligned}\int2\cdot  \frac{y\operatorname{cos}⁡({y}^{2})}{\operatorname{sin}⁡({y}^{2})}\,\text{d}y & =\int2\cdot  \frac{1}{\operatorname{sin}⁡({y}^{2})}\cdot (y\operatorname{cos}⁡({y}^{2}))\,\text{d}y \\  & =\int2\cdot  \frac{1}{u}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int2\cdot  \frac{1}{u}\,\text{d}u \\  & =2\left(\frac{1}{2}\operatorname{ln}⁡|u|\right)+C \\  & =2\left(\frac{1}{2}\operatorname{ln}⁡|\operatorname{sin}⁡({y}^{2})|\right)+C\end{aligned}
$$

## Original evidence q-113997

Calculate $\int \frac{{sec}^{2}⁡x\operatorname{tan}⁡x}{\operatorname{tan}⁡x+1}\,\text{d}x.$

- $\operatorname{tan}⁡(x-1)-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|+K$
- $\operatorname{tan}⁡x-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|+K$ (correct)
- $\frac{{tan}^{2}⁡x}{2}-\operatorname{tan}⁡x+K$
- $\operatorname{tan}⁡x-\operatorname{ln}⁡|\operatorname{tan}⁡x|+K$
- $\operatorname{tan}⁡(x+1)-\operatorname{ln}⁡|\operatorname{tan}⁡x|+K$

Let $u=\operatorname{tan}⁡x+1.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}={sec}^{2}⁡x\,⟹\,\text{d}u={sec}^{2}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{{sec}^{2}⁡x\operatorname{tan}⁡x}{\operatorname{tan}⁡x+1}\,\text{d}x & =\int \frac{1}{\operatorname{tan}⁡x+1}\cdot {sec}^{2}⁡x\operatorname{tan}⁡x\,\text{d}x \\  & =\int \frac{1}{\operatorname{tan}⁡x+1}\cdot \operatorname{tan}⁡x\cdot {sec}^{2}⁡x\,\text{d}x \\  & =\int \frac{1}{u}(u-1)\text{d}u \\  & =\int (1-\frac{1}{u})\,\text{d}u \\  & =u-\operatorname{ln}⁡|u|+C \\  & =(\operatorname{tan}⁡x+1)-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|+C \\  & =\operatorname{tan}⁡x-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|+K\end{aligned}
$$

where $K=C+1.$

## Changed evidence q-113997

Calculate $\int2\cdot  \frac{{sec}^{2}⁡x\operatorname{tan}⁡x}{\operatorname{tan}⁡x+1}\,\text{d}x.$

- $2\left(\operatorname{tan}⁡(x-1)-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|\right)+K$
- $2\left(\operatorname{tan}⁡x-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|\right)+K$ (correct)
- $2\left(\frac{{tan}^{2}⁡x}{2}-\operatorname{tan}⁡x\right)+K$
- $2\left(\operatorname{tan}⁡x-\operatorname{ln}⁡|\operatorname{tan}⁡x|\right)+K$
- $2\left(\operatorname{tan}⁡(x+1)-\operatorname{ln}⁡|\operatorname{tan}⁡x|\right)+K$

Let $u=\operatorname{tan}⁡x+1.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}={sec}^{2}⁡x\,⟹\,\text{d}u={sec}^{2}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int2\cdot  \frac{{sec}^{2}⁡x\operatorname{tan}⁡x}{\operatorname{tan}⁡x+1}\,\text{d}x & =\int2\cdot  \frac{1}{\operatorname{tan}⁡x+1}\cdot {sec}^{2}⁡x\operatorname{tan}⁡x\,\text{d}x \\  & =\int2\cdot  \frac{1}{\operatorname{tan}⁡x+1}\cdot \operatorname{tan}⁡x\cdot {sec}^{2}⁡x\,\text{d}x \\  & =\int2\cdot  \frac{1}{u}(u-1)\text{d}u \\  & =\int2\cdot  (1-\frac{1}{u})\,\text{d}u \\  & =2\left(u-\operatorname{ln}⁡|u|\right)+C \\  & =2\left((\operatorname{tan}⁡x+1)-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|\right)+C \\  & =2\left(\operatorname{tan}⁡x-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|\right)+K\end{aligned}
$$

where $K=C+2.$

## Normal authored bank q-113997

Calculate $\int2\cdot  \frac{{sec}^{2}⁡x\operatorname{tan}⁡x}{\operatorname{tan}⁡x+1}\,\text{d}x.$

- $2 \ln|\tan{\left(x \right)} + 1|+C$
- $2 \ln|\tan{\left(x \right)} + 1| + 2 \tan{\left(x \right)}+C$
- $- 2 \ln|\tan{\left(x \right)} + 1| + 2 \tan{\left(x \right)}+C$ (correct)
- $\left(\tan{\left(x \right)} + 1\right)^{2} - 2 \tan{\left(x \right)} - 2+C$
- $- 2 \ln|\tan{\left(x \right)}| + 2 \tan{\left(x \right)}+C$

Let $u=\operatorname{tan}⁡x+1.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}={sec}^{2}⁡x\,⟹\,\text{d}u={sec}^{2}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int2\cdot  \frac{{sec}^{2}⁡x\operatorname{tan}⁡x}{\operatorname{tan}⁡x+1}\,\text{d}x & =\int2\cdot  \frac{1}{\operatorname{tan}⁡x+1}\cdot {sec}^{2}⁡x\operatorname{tan}⁡x\,\text{d}x \\  & =\int2\cdot  \frac{1}{\operatorname{tan}⁡x+1}\cdot \operatorname{tan}⁡x\cdot {sec}^{2}⁡x\,\text{d}x \\  & =\int2\cdot  \frac{1}{u}(u-1)\text{d}u \\  & =\int2\cdot  (1-\frac{1}{u})\,\text{d}u \\  & =2\left(u-\operatorname{ln}⁡|u|\right)+C \\  & =2\left((\operatorname{tan}⁡x+1)-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|\right)+C \\  & =2\left(\operatorname{tan}⁡x-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|\right)+K\end{aligned}
$$

where $K=C+2.$

## Generated easy 1

What is $\displaystyle \int5\cdot \frac{2\cos y}{\sin y}dy$?

- $10 \ln|\cos{\left(y \right)}|+C$
- $- \frac{10}{\sin{\left(y \right)}}+C$
- $10 \ln|\sin{\left(y \right)}|+C$ (correct)
- $- 10 \ln|\sin{\left(y \right)}|+C$
- $10 \sin{\left(y \right)}+C$

Let $u=\sin{\left(y \right)}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}y}=\cos{\left(y \right)}\,⟹\,\text{d}u=\cos{\left(y \right)}\,\text{d}y.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{10 \cos{\left(y \right)}}{\sin{\left(y \right)}}\,\text{d}y &= \int \frac{1}{\sin{\left(y \right)}}\cdot (10 \cos{\left(y \right)})\,\text{d}y \\ &= \int \frac{1}{u}\cdot 10\,\text{d}u \\ &= 10\int \frac{1}{u}\,\text{d}u \\ &= 10 \ln|u|+C \\ &= 10 \ln|\sin{\left(y \right)}|+C\end{aligned}
$$

## Generated easy 2

What is $\displaystyle \int3\cdot \frac{2\cos y}{\sin y}dy$?

- $6 \ln|\cos{\left(y \right)}|+C$
- $- \frac{6}{\sin{\left(y \right)}}+C$
- $6 \ln|\sin{\left(y \right)}|+C$ (correct)
- $- 6 \ln|\sin{\left(y \right)}|+C$
- $6 \sin{\left(y \right)}+C$

Let $u=\sin{\left(y \right)}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}y}=\cos{\left(y \right)}\,⟹\,\text{d}u=\cos{\left(y \right)}\,\text{d}y.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{6 \cos{\left(y \right)}}{\sin{\left(y \right)}}\,\text{d}y &= \int \frac{1}{\sin{\left(y \right)}}\cdot (6 \cos{\left(y \right)})\,\text{d}y \\ &= \int \frac{1}{u}\cdot 6\,\text{d}u \\ &= 6\int \frac{1}{u}\,\text{d}u \\ &= 6 \ln|u|+C \\ &= 6 \ln|\sin{\left(y \right)}|+C\end{aligned}
$$

## Generated moderate 1

Calculate $\int \frac{3 \cos{\left(x \right)}}{\sin{\left(x \right)} + 6}\,\text{d}x.$

- $3 \ln|\sin{\left(x \right)}|+C$
- $- \frac{3}{\sin{\left(x \right)} + 6}+C$
- $3 \ln|\sin{\left(x \right)} + 6|+C$ (correct)
- $- 3 \ln|\sin{\left(x \right)} + 6|+C$
- $3 \sin{\left(x \right)} + 18+C$

Let $u=\sin{\left(x \right)} + 6.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=\cos{\left(x \right)}\,⟹\,\text{d}u=\cos{\left(x \right)}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{3 \cos{\left(x \right)}}{\sin{\left(x \right)} + 6}\,\text{d}x &= \int \frac{1}{\sin{\left(x \right)} + 6}\cdot (3 \cos{\left(x \right)})\,\text{d}x \\ &= \int \frac{1}{u}\cdot 3\,\text{d}u \\ &= 3\int \frac{1}{u}\,\text{d}u \\ &= 3 \ln|u|+C \\ &= 3 \ln|\sin{\left(x \right)} + 6|+C\end{aligned}
$$

## Generated moderate 2

Calculate $\int \frac{6 \cos{\left(x \right)}}{\sin{\left(x \right)} + 3}\,\text{d}x.$

- $6 \ln|\sin{\left(x \right)}|+C$
- $- \frac{6}{\sin{\left(x \right)} + 3}+C$
- $6 \ln|\sin{\left(x \right)} + 3|+C$ (correct)
- $- 6 \ln|\sin{\left(x \right)} + 3|+C$
- $6 \sin{\left(x \right)} + 18+C$

Let $u=\sin{\left(x \right)} + 3.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=\cos{\left(x \right)}\,⟹\,\text{d}u=\cos{\left(x \right)}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{6 \cos{\left(x \right)}}{\sin{\left(x \right)} + 3}\,\text{d}x &= \int \frac{1}{\sin{\left(x \right)} + 3}\cdot (6 \cos{\left(x \right)})\,\text{d}x \\ &= \int \frac{1}{u}\cdot 6\,\text{d}u \\ &= 6\int \frac{1}{u}\,\text{d}u \\ &= 6 \ln|u|+C \\ &= 6 \ln|\sin{\left(x \right)} + 3|+C\end{aligned}
$$

## Generated hard 1

Calculate $\int9\cdot  \frac{2\operatorname{csc}⁡x\operatorname{cot}⁡x}{\operatorname{csc}⁡x+2}\,\text{d}x.$

- $18 \ln|\csc{\left(x \right)} + 2|+C$
- $\frac{18}{\csc{\left(x \right)} + 2}+C$
- $- 18 \ln|\csc{\left(x \right)} + 2|+C$ (correct)
- $- 9 \ln|\csc{\left(x \right)} + 2|+C$
- $- 18 \ln|\csc{\left(x \right)}|+C$

Let $u=\operatorname{csc}⁡x+2.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=-\operatorname{csc}⁡x\operatorname{cot}⁡x\,⟹\,-\text{d}u=\operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int9\cdot  \frac{2\operatorname{csc}⁡x\operatorname{cot}⁡x}{\operatorname{csc}⁡x+2}\,\text{d}x & =2\int9\cdot  \frac{1}{\operatorname{csc}⁡x+2}\cdot \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & =2\int9\cdot  \frac{1}{u}\cdot (-\text{d}u) \\  & =-2\int9\cdot  \frac{1}{u}\,\text{d}u \\  & =9\left(-2\operatorname{ln}⁡|u|\right)+C \\  & =9\left(-2\operatorname{ln}⁡|\operatorname{csc}⁡x+2|\right)+C\end{aligned}
$$

## Generated hard 2

Calculate $\int3\cdot  \frac{{sec}^{2}⁡x\operatorname{tan}⁡x}{\operatorname{tan}⁡x+1}\,\text{d}x.$

- $3 \ln|\tan{\left(x \right)} + 1| + 3 \tan{\left(x \right)}+C$
- $\frac{3 \left(\tan{\left(x \right)} + 1\right)^{2}}{2} - 3 \tan{\left(x \right)} - 3+C$
- $- 3 \ln|\tan{\left(x \right)} + 1| + 3 \tan{\left(x \right)}+C$ (correct)
- $3 \ln|\tan{\left(x \right)} + 1|+C$
- $- 3 \ln|\tan{\left(x \right)}| + 3 \tan{\left(x \right)}+C$

Let $u=\operatorname{tan}⁡x+1.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}={sec}^{2}⁡x\,⟹\,\text{d}u={sec}^{2}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int3\cdot  \frac{{sec}^{2}⁡x\operatorname{tan}⁡x}{\operatorname{tan}⁡x+1}\,\text{d}x & =\int3\cdot  \frac{1}{\operatorname{tan}⁡x+1}\cdot {sec}^{2}⁡x\operatorname{tan}⁡x\,\text{d}x \\  & =\int3\cdot  \frac{1}{\operatorname{tan}⁡x+1}\cdot \operatorname{tan}⁡x\cdot {sec}^{2}⁡x\,\text{d}x \\  & =\int3\cdot  \frac{1}{u}(u-1)\text{d}u \\  & =\int3\cdot  (1-\frac{1}{u})\,\text{d}u \\  & =3\left(u-\operatorname{ln}⁡|u|\right)+C \\  & =3\left((\operatorname{tan}⁡x+1)-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|\right)+C \\  & =3\left(\operatorname{tan}⁡x-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|\right)+K\end{aligned}
$$

where $K=C+3.$