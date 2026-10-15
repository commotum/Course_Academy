# Original sources and generated variants

Raw profiles are ineligible evidence. Normal examples use authored method banks; easy is an authored level. All examples use the public generate API.


## q-13461 — captured original


Calculate $\intx\sin (x^{2})dx$.



Original complete bank:


- $\cos (x^{2}) + C$

- $-\cos (x^{2}) + C$

- $\frac{1}{2}\cos (x^{2}) + C$

- $-\frac{1}{2}\cos (x^{2}) + C$

- $-2\cos (x^{2}) + C$


[No captured solution, difficulty or correct designation.]


### Changed evidence-bank variant (ineligible)


Calculate $\int 2 x \sin{\left(x^{2} \right)}\,\text{d}x$.

- $- 2 \cos{\left(x^{2} \right)}+C$
- $- \cos{\left(x^{2} \right)}+C$
- $\cos{\left(x^{2} \right)}+C$
- $- 4 \cos{\left(x^{2} \right)}+C$
- $2 \cos{\left(x^{2} \right)}+C$

[No captured worked solution.]


### Generated normal variant 1


Calculate $\int 9 x \sin{\left(2 x^{2} \right)}\,\text{d}x.$

- $- \frac{9 \cos{\left(2 x^{2} \right)}}{4}+C$
- $- 9 \cos{\left(2 x^{2} \right)}+C$
- $\frac{9 \cos{\left(2 x^{2} \right)}}{4}+C$
- $- \frac{9 \cos{\left(2 x^{2} \right)}}{16}+C$
- $\frac{9 \sin{\left(2 x^{2} \right)}}{4}+C$

Let $u=2 x^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=4 x\,⟹\,\frac{1}{4}\text{d}u=x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 9 x \sin{\left(2 x^{2} \right)}\,\text{d}x &=\int 9 \sin{\left(2 x^{2} \right)}\cdot x\,\text{d}x \\ &=9\int \sin{\left(u \right)}\cdot \left(\frac{1}{4}\right)\,\text{d}u \\ &=\frac{9}{4}\int \sin{\left(u \right)}\,\text{d}u \\ &=- \frac{9 \cos{\left(u \right)}}{4}+C \\ &=- \frac{9 \cos{\left(2 x^{2} \right)}}{4}+C\end{aligned}
$$


### Generated normal variant 2


Calculate $\int 8 x \sin{\left(6 x^{2} \right)}\,\text{d}x.$

- $\frac{2 \sin{\left(6 x^{2} \right)}}{3}+C$
- $- \frac{\cos{\left(6 x^{2} \right)}}{18}+C$
- $- \frac{2 \cos{\left(6 x^{2} \right)}}{3}+C$
- $\frac{2 \cos{\left(6 x^{2} \right)}}{3}+C$
- $- 8 \cos{\left(6 x^{2} \right)}+C$

Let $u=6 x^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=12 x\,⟹\,\frac{1}{12}\text{d}u=x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 8 x \sin{\left(6 x^{2} \right)}\,\text{d}x &=\int 8 \sin{\left(6 x^{2} \right)}\cdot x\,\text{d}x \\ &=8\int \sin{\left(u \right)}\cdot \left(\frac{1}{12}\right)\,\text{d}u \\ &=\frac{2}{3}\int \sin{\left(u \right)}\,\text{d}u \\ &=- \frac{2 \cos{\left(u \right)}}{3}+C \\ &=- \frac{2 \cos{\left(6 x^{2} \right)}}{3}+C\end{aligned}
$$


## q-13474 — captured original


$\int 4{x}^{2}{sec}^{2}⁡({x}^{3})\,\text{d}x=$



Original complete bank:


- $\frac{3}{4}\operatorname{tan}⁡({x}^{3})+C$

- $\frac{4}{3}\operatorname{sec}⁡({x}^{3})+C$

- $3\operatorname{tan}⁡({x}^{3})+C$

- $\operatorname{tan}⁡({x}^{3})+C$

- $\frac{4}{3}\operatorname{tan}⁡({x}^{3})+C$


Let $u={x}^{3}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=3{x}^{2}\,⟹\,\frac{1}{3}\text{d}u={x}^{2}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 4{x}^{2}{sec}^{2}⁡({x}^{3})\,\text{d}x & =4\int {sec}^{2}⁡({x}^{3})\cdot {x}^{2}\,\text{d}x \\  & =4\int {sec}^{2}⁡(u)\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{4}{3}\int {sec}^{2}⁡u\,\text{d}u \\  & =\frac{4}{3}\operatorname{tan}⁡u+C \\  & =\frac{4}{3}\operatorname{tan}⁡({x}^{3})+C\end{aligned}
$$


### Changed evidence-bank variant (ineligible)


$\int 5 x^{2} \sec^{2}{\left(x^{3} \right)}\,\text{d}x=$

- $\frac{5 \sec{\left(x^{3} \right)}}{3}+C$
- $\frac{5 \tan{\left(x^{3} \right)}}{4}+C$
- $\frac{15 \tan{\left(x^{3} \right)}}{4}+C$
- $\frac{5 \tan{\left(x^{3} \right)}}{3}+C$
- $\frac{15 \tan{\left(x^{3} \right)}}{16}+C$

Let $u={x}^{3}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=3{x}^{2}\,⟹\,\frac{1}{3}\text{d}u={x}^{2}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 5 x^{2} \sec^{2}{\left(x^{3} \right)}\,\text{d}x & =\int 5 \sec^{2}{\left(x^{3} \right)}\cdot x^{2}\,\text{d}x \\  & =5\int \sec^{2}{\left(u \right)}\cdot \left(\frac{1}{3}\right)\,\text{d}u \\  & =\frac{5}{3}\int \sec^{2}{\left(u \right)}\,\text{d}u \\  & =\frac{5 \tan{\left(u \right)}}{3}+C \\  & =\frac{5 \tan{\left(x^{3} \right)}}{3}+C\end{aligned}
$$


### Generated normal variant 1


Calculate $\int 8 x^{2} \sec^{2}{\left(6 x^{3} \right)}\,\text{d}x.$

- $\frac{4 \tan{\left(6 x^{3} \right)}}{9}+C$
- $8 \tan{\left(6 x^{3} \right)}+C$
- $- \frac{4 \tan{\left(6 x^{3} \right)}}{9}+C$
- $\frac{2 \tan{\left(6 x^{3} \right)}}{81}+C$
- $\frac{4 \sec{\left(6 x^{3} \right)}}{9}+C$

Let $u=6 x^{3}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=18 x^{2}\,⟹\,\frac{1}{18}\text{d}u=x^{2}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 8 x^{2} \sec^{2}{\left(6 x^{3} \right)}\,\text{d}x & =\int 8 \sec^{2}{\left(6 x^{3} \right)}\cdot x^{2}\,\text{d}x \\  & =8\int \sec^{2}{\left(u \right)}\cdot \left(\frac{1}{18}\right)\,\text{d}u \\  & =\frac{4}{9}\int \sec^{2}{\left(u \right)}\,\text{d}u \\  & =\frac{4 \tan{\left(u \right)}}{9}+C \\  & =\frac{4 \tan{\left(6 x^{3} \right)}}{9}+C\end{aligned}
$$


### Generated normal variant 2


Calculate $\int 8 x^{2} \sec^{2}{\left(2 x^{3} \right)}\,\text{d}x.$

- $\frac{4 \sec{\left(2 x^{3} \right)}}{3}+C$
- $8 \tan{\left(2 x^{3} \right)}+C$
- $\frac{4 \tan{\left(2 x^{3} \right)}}{3}+C$
- $- \frac{4 \tan{\left(2 x^{3} \right)}}{3}+C$
- $\frac{2 \tan{\left(2 x^{3} \right)}}{9}+C$

Let $u=2 x^{3}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=6 x^{2}\,⟹\,\frac{1}{6}\text{d}u=x^{2}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 8 x^{2} \sec^{2}{\left(2 x^{3} \right)}\,\text{d}x & =\int 8 \sec^{2}{\left(2 x^{3} \right)}\cdot x^{2}\,\text{d}x \\  & =8\int \sec^{2}{\left(u \right)}\cdot \left(\frac{1}{6}\right)\,\text{d}u \\  & =\frac{4}{3}\int {sec}^{2}⁡u\,\text{d}u \\  & =\frac{4}{3}\operatorname{tan}⁡u+C \\  & =\frac{4 \tan{\left(2 x^{3} \right)}}{3}+C\end{aligned}
$$


## q-13464 — captured original


Calculate $\int x{csc}^{2}⁡({x}^{2})\,\text{d}x.$



Original complete bank:


- $\frac{1}{2}\operatorname{cot}⁡({x}^{2})+C$

- $-\frac{1}{2}\operatorname{csc}⁡({x}^{2})+C$

- $\frac{1}{4}\operatorname{cot}⁡({x}^{2})+C$

- $-\frac{1}{4}\operatorname{cot}⁡({x}^{2})+C$

- $-\frac{1}{2}\operatorname{cot}⁡({x}^{2})+C$


Let $u={x}^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int x{csc}^{2}⁡({x}^{2})\,\text{d}x & =\int {csc}^{2}⁡({x}^{2})\cdot x\,\text{d}x \\  & =\int {csc}^{2}⁡u\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int {csc}^{2}⁡u\,\text{d}u \\  & =-\frac{1}{2}\operatorname{cot}⁡u+C \\  & =-\frac{1}{2}\operatorname{cot}⁡({x}^{2})+C\end{aligned}
$$


### Changed evidence-bank variant (ineligible)


Calculate $\int 2 x \csc^{2}{\left(x^{2} \right)}\,\text{d}x.$

- $- \csc{\left(x^{2} \right)}+C$
- $- \frac{\cot{\left(x^{2} \right)}}{2}+C$
- $\frac{\cot{\left(x^{2} \right)}}{2}+C$
- $- \cot{\left(x^{2} \right)}+C$
- $\cot{\left(x^{2} \right)}+C$

Let $u={x}^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=2x\,⟹\,\frac{1}{2}\text{d}u=x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 2 x \csc^{2}{\left(x^{2} \right)}\,\text{d}x & =\int 2 \csc^{2}{\left(x^{2} \right)}\cdot x\,\text{d}x \\  & =2\int \csc^{2}{\left(u \right)}\cdot \left(\frac{1}{2}\right)\,\text{d}u \\  & =1\int \csc^{2}{\left(u \right)}\,\text{d}u \\  & =- \cot{\left(u \right)}+C \\  & =- \cot{\left(x^{2} \right)}+C\end{aligned}
$$


### Generated normal variant 1


Calculate $\int 9 x \csc^{2}{\left(2 x^{2} \right)}\,\text{d}x.$

- $- \frac{9 \cot{\left(2 x^{2} \right)}}{4}+C$
- $- 9 \cot{\left(2 x^{2} \right)}+C$
- $\frac{9 \cot{\left(2 x^{2} \right)}}{4}+C$
- $- \frac{9 \cot{\left(2 x^{2} \right)}}{16}+C$
- $- \frac{9 \csc{\left(2 x^{2} \right)}}{4}+C$

Let $u=2 x^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=4 x\,⟹\,\frac{1}{4}\text{d}u=x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 9 x \csc^{2}{\left(2 x^{2} \right)}\,\text{d}x & =\int 9 \csc^{2}{\left(2 x^{2} \right)}\cdot x\,\text{d}x \\  & =9\int \csc^{2}{\left(u \right)}\cdot \left(\frac{1}{4}\right)\,\text{d}u \\  & =\frac{9}{4}\int \csc^{2}{\left(u \right)}\,\text{d}u \\  & =- \frac{9 \cot{\left(u \right)}}{4}+C \\  & =- \frac{9 \cot{\left(2 x^{2} \right)}}{4}+C\end{aligned}
$$


### Generated normal variant 2


Calculate $\int 8 x \csc^{2}{\left(6 x^{2} \right)}\,\text{d}x.$

- $- \frac{2 \csc{\left(6 x^{2} \right)}}{3}+C$
- $- \frac{\cot{\left(6 x^{2} \right)}}{18}+C$
- $- \frac{2 \cot{\left(6 x^{2} \right)}}{3}+C$
- $\frac{2 \cot{\left(6 x^{2} \right)}}{3}+C$
- $- 8 \cot{\left(6 x^{2} \right)}+C$

Let $u=6 x^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=12 x\,⟹\,\frac{1}{12}\text{d}u=x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 8 x \csc^{2}{\left(6 x^{2} \right)}\,\text{d}x & =\int 8 \csc^{2}{\left(6 x^{2} \right)}\cdot x\,\text{d}x \\  & =8\int \csc^{2}{\left(u \right)}\cdot \left(\frac{1}{12}\right)\,\text{d}u \\  & =\frac{2}{3}\int \csc^{2}{\left(u \right)}\,\text{d}u \\  & =- \frac{2 \cot{\left(u \right)}}{3}+C \\  & =- \frac{2 \cot{\left(6 x^{2} \right)}}{3}+C\end{aligned}
$$


## q-13533 — captured original


${\int }_{0}^{\sqrt{\pi /2}}5x\operatorname{cos}⁡(2{x}^{2})\,\text{d}x=$



Original complete bank:


- $0$

- $\frac{1}{2}$

- $\frac{5}{4}$

- $\frac{1}{4}$

- $-1$


Let $u=2{x}^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=4x\,⟹\,\frac{1}{4}\text{d}u=x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\sqrt{\pi /2}$ |
| --- | --- | --- |
| $u$ | $0$ | $\pi $ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\sqrt{\pi /2}}5x\operatorname{cos}⁡(2{x}^{2})\,\text{d}x & ={\int }_{0}^{\sqrt{\pi /2}}5\operatorname{cos}⁡(2{x}^{2})\cdot x\,\text{d}x \\  & ={\int }_{0}^{\pi }5\operatorname{cos}⁡u\cdot \frac{1}{4}\,\text{d}u \\  & =\frac{5}{4}{\int }_{0}^{\pi }\operatorname{cos}⁡u\,\text{d}u \\  & =\frac{5}{4}\operatorname{sin}⁡u{|}_{0}^{\pi } \\  & =\frac{5}{4}(\operatorname{sin}⁡(\pi )-\operatorname{sin}⁡(0)) \\  & =\frac{5}{4}(0) \\  & =0\end{aligned}
$$


### Changed evidence-bank variant (ineligible)


$\int_{0}^{\frac{\sqrt{2} \sqrt{\pi}}{2}} 6 x \cos{\left(2 x^{2} \right)}\,\text{d}x=$

- $\frac{3}{5}$
- $\frac{3}{10}$
- $\frac{3}{2}$
- $- \frac{6}{5}$
- $0$

Let $u=2{x}^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=4x\,⟹\,\frac{1}{4}\text{d}u=x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\sqrt{\pi /2}$ |
| --- | --- | --- |
| $u$ | $0$ | $\pi $ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\sqrt{2} \sqrt{\pi}}{2}} 6 x \cos{\left(2 x^{2} \right)}\,\text{d}x & =\int_{0}^{\frac{\sqrt{2} \sqrt{\pi}}{2}} 6 \cos{\left(2 x^{2} \right)}\cdot x\,\text{d}x \\  & =\int_{0}^{\pi} 6 \cos{\left(u \right)}\cdot \left(\frac{1}{4}\right)\,\text{d}u \\  & =\frac{3}{2}\int_{0}^{\pi} \cos{\left(u \right)}\,\text{d}u \\  & =\frac{3 \sin{\left(u \right)}}{2}\big|_{0}^{\pi} \\  & =\frac{3}{2}\left(\sin{\left(\left(\pi\right) \right)}-\left(\sin{\left(\left(0\right) \right)}\right)\right) \\  & =\frac{3}{2}\left(0\right) \\  & =0\end{aligned}
$$


### Generated normal variant 1


Calculate $\int_{\frac{\sqrt{\pi}}{6}}^{\frac{\sqrt{3} \sqrt{\pi}}{6}} 12 x \cos{\left(6 x^{2} \right)}\,\text{d}x.$

- $\frac{1}{24}$
- $6$
- $- \frac{\sqrt{3}}{2}$
- $- \frac{1}{2}$
- $\frac{1}{2}$

Let $u=6 x^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=12 x\,⟹\,\frac{1}{12}\text{d}u=x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{\sqrt{\pi}}{6}$ | $\frac{\sqrt{3} \sqrt{\pi}}{6}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{6}$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{\sqrt{\pi}}{6}}^{\frac{\sqrt{3} \sqrt{\pi}}{6}} 12 x \cos{\left(6 x^{2} \right)}\,\text{d}x & =\int_{\frac{\sqrt{\pi}}{6}}^{\frac{\sqrt{3} \sqrt{\pi}}{6}} 12 \cos{\left(6 x^{2} \right)}\cdot x\,\text{d}x \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} 12 \cos{\left(u \right)}\cdot \left(\frac{1}{12}\right)\,\text{d}u \\  & =1\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \cos{\left(u \right)}\,\text{d}u \\  & =\sin{\left(u \right)}\big|_{\frac{\pi}{6}}^{\frac{\pi}{2}} \\  & =1\left(\sin{\left(\left(\frac{\pi}{2}\right) \right)}-\left(\sin{\left(\left(\frac{\pi}{6}\right) \right)}\right)\right) \\  & =1\left(\frac{1}{2}\right) \\  & =\frac{1}{2}\end{aligned}
$$


### Generated normal variant 2


Calculate $\int_{\frac{\sqrt{\pi}}{6}}^{\frac{\sqrt{3} \sqrt{\pi}}{6}} 6 x \cos{\left(6 x^{2} \right)}\,\text{d}x.$

- $\frac{1}{4}$
- $\frac{1}{48}$
- $3$
- $- \frac{\sqrt{3}}{4}$
- $- \frac{1}{4}$

Let $u=6 x^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=12 x\,⟹\,\frac{1}{12}\text{d}u=x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{\sqrt{\pi}}{6}$ | $\frac{\sqrt{3} \sqrt{\pi}}{6}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{6}$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{\sqrt{\pi}}{6}}^{\frac{\sqrt{3} \sqrt{\pi}}{6}} 6 x \cos{\left(6 x^{2} \right)}\,\text{d}x & =\int_{\frac{\sqrt{\pi}}{6}}^{\frac{\sqrt{3} \sqrt{\pi}}{6}} 6 \cos{\left(6 x^{2} \right)}\cdot x\,\text{d}x \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} 6 \cos{\left(u \right)}\cdot \left(\frac{1}{12}\right)\,\text{d}u \\  & =\frac{1}{2}\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \cos{\left(u \right)}\,\text{d}u \\  & =\frac{\sin{\left(u \right)}}{2}\big|_{\frac{\pi}{6}}^{\frac{\pi}{2}} \\  & =\frac{1}{2}\left(\sin{\left(\left(\frac{\pi}{2}\right) \right)}-\left(\sin{\left(\left(\frac{\pi}{6}\right) \right)}\right)\right) \\  & =\frac{1}{2}\left(\frac{1}{2}\right) \\  & =\frac{1}{4}\end{aligned}
$$


## q-13537 — captured original


Evaluate the integral ${\int }_{0}^{\sqrt{\pi }}3x\operatorname{sin}⁡(2{x}^{2})\,\text{d}x.$



Original complete bank:


- $\frac{3}{4}$

- $1$

- $-1$

- $-\frac{3}{4}$

- $0$


Let $u=2{x}^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=4x\,⟹\,\frac{1}{4}\text{d}u=x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\sqrt{\pi }$ |
| --- | --- | --- |
| $u$ | $0$ | $2\pi $ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\sqrt{\pi }}3x\operatorname{sin}⁡(2{x}^{2})\,\text{d}x & ={\int }_{0}^{\sqrt{\pi }}3\operatorname{sin}⁡(2{x}^{2})\cdot x\,\text{d}x \\  & ={\int }_{0}^{2\pi }3\operatorname{sin}⁡u\cdot \frac{1}{4}\,\text{d}u \\  & =\frac{3}{4}{\int }_{0}^{2\pi }\operatorname{sin}⁡u\,\text{d}u \\  & =-\frac{3}{4}\operatorname{cos}⁡u{|}_{0}^{2\pi } \\  & =-\frac{3}{4}(\operatorname{cos}⁡(2\pi )-\operatorname{cos}⁡(0)) \\  & =-\frac{3}{4}(1-1) \\  & =-\frac{3}{4}\cdot 0 \\  & =0\end{aligned}
$$


### Changed evidence-bank variant (ineligible)


Evaluate the integral $\int_{0}^{\sqrt{\pi}} 4 x \sin{\left(2 x^{2} \right)}\,\text{d}x.$

- $\frac{4}{3}$
- $-1$
- $- \frac{4}{3}$
- $0$
- $1$

Let $u=2{x}^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=4x\,⟹\,\frac{1}{4}\text{d}u=x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\sqrt{\pi }$ |
| --- | --- | --- |
| $u$ | $0$ | $2\pi $ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\sqrt{\pi}} 4 x \sin{\left(2 x^{2} \right)}\,\text{d}x & =\int_{0}^{\sqrt{\pi}} 4 \sin{\left(2 x^{2} \right)}\cdot x\,\text{d}x \\  & =\int_{0}^{2 \pi} 4 \sin{\left(u \right)}\cdot \left(\frac{1}{4}\right)\,\text{d}u \\  & =1\int_{0}^{2 \pi} \sin{\left(u \right)}\,\text{d}u \\  & =- \cos{\left(u \right)}\big|_{0}^{2 \pi} \\  & =1\left(- \cos{\left(\left(2 \pi\right) \right)}-\left(- \cos{\left(\left(0\right) \right)}\right)\right) \\  & =1\left(-1-\left(-1\right)\right) \\  & =1\cdot \left(0\right) \\  & =0\end{aligned}
$$


### Generated normal variant 1


Calculate $\int_{0}^{\frac{\sqrt{6} \sqrt{\pi}}{6}} 12 x \sin{\left(6 x^{2} \right)}\,\text{d}x.$

- $\frac{1}{6}$
- $24$
- $0$
- $-2$
- $2$

Let $u=6 x^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=12 x\,⟹\,\frac{1}{12}\text{d}u=x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{\sqrt{6} \sqrt{\pi}}{6}$ |
| --- | --- | --- |
| $u$ | $0$ | $\pi$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\sqrt{6} \sqrt{\pi}}{6}} 12 x \sin{\left(6 x^{2} \right)}\,\text{d}x & =\int_{0}^{\frac{\sqrt{6} \sqrt{\pi}}{6}} 12 \sin{\left(6 x^{2} \right)}\cdot x\,\text{d}x \\  & =\int_{0}^{\pi} 12 \sin{\left(u \right)}\cdot \left(\frac{1}{12}\right)\,\text{d}u \\  & =1\int_{0}^{\pi} \sin{\left(u \right)}\,\text{d}u \\  & =- \cos{\left(u \right)}\big|_{0}^{\pi} \\  & =1\left(- \cos{\left(\left(\pi\right) \right)}-\left(- \cos{\left(\left(0\right) \right)}\right)\right) \\  & =1\left(1-\left(-1\right)\right) \\  & =1\cdot \left(2\right) \\  & =2\end{aligned}
$$


### Generated normal variant 2


Calculate $\int_{0}^{\frac{\sqrt{6} \sqrt{\pi}}{6}} 6 x \sin{\left(6 x^{2} \right)}\,\text{d}x.$

- $1$
- $\frac{1}{12}$
- $12$
- $0$
- $-1$

Let $u=6 x^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=12 x\,⟹\,\frac{1}{12}\text{d}u=x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{\sqrt{6} \sqrt{\pi}}{6}$ |
| --- | --- | --- |
| $u$ | $0$ | $\pi$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\sqrt{6} \sqrt{\pi}}{6}} 6 x \sin{\left(6 x^{2} \right)}\,\text{d}x & =\int_{0}^{\frac{\sqrt{6} \sqrt{\pi}}{6}} 6 \sin{\left(6 x^{2} \right)}\cdot x\,\text{d}x \\  & =\int_{0}^{\pi} 6 \sin{\left(u \right)}\cdot \left(\frac{1}{12}\right)\,\text{d}u \\  & =\frac{1}{2}\int_{0}^{\pi} \sin{\left(u \right)}\,\text{d}u \\  & =- \frac{\cos{\left(u \right)}}{2}\big|_{0}^{\pi} \\  & =\frac{1}{2}\left(- \cos{\left(\left(\pi\right) \right)}-\left(- \cos{\left(\left(0\right) \right)}\right)\right) \\  & =\frac{1}{2}\left(1-\left(-1\right)\right) \\  & =\frac{1}{2}\cdot \left(2\right) \\  & =1\end{aligned}
$$


## q-3038 — captured original


Calculate the integral $\int \frac{{sec}^{2}⁡(1/x)}{{x}^{2}}\,\text{d}x.$



Original complete bank:


- $-\operatorname{tan}⁡(\frac{1}{x})+C$

- $\operatorname{cot}⁡(\frac{1}{x})+C$

- $-\operatorname{csc}⁡(\frac{1}{x})+C$

- $-\operatorname{sec}⁡(\frac{1}{x})+C$

- $2\operatorname{tan}⁡(\frac{1}{x})+C$


Let $u=\frac{1}{x}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=-\frac{1}{{x}^{2}}\,⟹\,-\text{d}u=\frac{1}{{x}^{2}}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{{sec}^{2}⁡(1/x)}{{x}^{2}}\,\text{d}x & =\int {sec}^{2}⁡(\frac{1}{x})\cdot \frac{1}{{x}^{2}}\,\text{d}x \\  & =\int {sec}^{2}⁡u\cdot (-\text{d}u) \\  & =-\int {sec}^{2}⁡u\,\text{d}u \\  & =-\operatorname{tan}⁡u+C \\  & =-\operatorname{tan}⁡(\frac{1}{x})+C\end{aligned}\end{aligned}
$$


### Changed evidence-bank variant (ineligible)


Calculate the integral $\int \frac{2 \sec^{2}{\left(\frac{1}{x} \right)}}{x^{2}}\,\text{d}x.$

- $2 \cot{\left(\frac{1}{x} \right)}+C$
- $- 2 \sec{\left(\frac{1}{x} \right)}+C$
- $- 2 \csc{\left(\frac{1}{x} \right)}+C$
- $4 \tan{\left(\frac{1}{x} \right)}+C$
- $- 2 \tan{\left(\frac{1}{x} \right)}+C$

Let $u=\frac{1}{x}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=-\frac{1}{{x}^{2}}\,⟹\,-\text{d}u=\frac{1}{{x}^{2}}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{2 \sec^{2}{\left(\frac{1}{x} \right)}}{x^{2}}\,\text{d}x & =\int 2 \sec^{2}{\left(\frac{1}{x} \right)}\cdot \frac{1}{x^{2}}\,\text{d}x \\  & =2\int \sec^{2}{\left(u \right)}\cdot \left(-1\right)\,\text{d}u \\  & =-2\int \sec^{2}{\left(u \right)}\,\text{d}u \\  & =- 2 \tan{\left(u \right)}+C \\  & =- 2 \tan{\left(\frac{1}{x} \right)}+C\end{aligned}\end{aligned}
$$


### Generated normal variant 1


Calculate $\int \frac{12 \sec^{2}{\left(\frac{6}{x} \right)}}{x^{2}}\,\text{d}x.$

- $- \frac{\tan{\left(\frac{6}{x} \right)}}{3}+C$
- $12 \tan{\left(\frac{6}{x} \right)}+C$
- $- 2 \sec{\left(\frac{6}{x} \right)}+C$
- $2 \tan{\left(\frac{6}{x} \right)}+C$
- $- 2 \tan{\left(\frac{6}{x} \right)}+C$

Let $u=\frac{6}{x}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=- \frac{6}{x^{2}}\,⟹\,- \frac{1}{6}\text{d}u=\frac{1}{x^{2}}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{12 \sec^{2}{\left(\frac{6}{x} \right)}}{x^{2}}\,\text{d}x & =\int 12 \sec^{2}{\left(\frac{6}{x} \right)}\cdot \frac{1}{x^{2}}\,\text{d}x \\  & =12\int \sec^{2}{\left(u \right)}\cdot \left(- \frac{1}{6}\right)\,\text{d}u \\  & =-2\int \sec^{2}{\left(u \right)}\,\text{d}u \\  & =- 2 \tan{\left(u \right)}+C \\  & =- 2 \tan{\left(\frac{6}{x} \right)}+C\end{aligned}\end{aligned}
$$


### Generated normal variant 2


Calculate $\int \frac{6 \sec^{2}{\left(\frac{6}{x} \right)}}{x^{2}}\,\text{d}x.$

- $- \tan{\left(\frac{6}{x} \right)}+C$
- $- \frac{\tan{\left(\frac{6}{x} \right)}}{6}+C$
- $6 \tan{\left(\frac{6}{x} \right)}+C$
- $- \sec{\left(\frac{6}{x} \right)}+C$
- $\tan{\left(\frac{6}{x} \right)}+C$

Let $u=\frac{6}{x}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=- \frac{6}{x^{2}}\,⟹\,- \frac{1}{6}\text{d}u=\frac{1}{x^{2}}\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \frac{6 \sec^{2}{\left(\frac{6}{x} \right)}}{x^{2}}\,\text{d}x & =\int 6 \sec^{2}{\left(\frac{6}{x} \right)}\cdot \frac{1}{x^{2}}\,\text{d}x \\  & =6\int \sec^{2}{\left(u \right)}\cdot \left(- \frac{1}{6}\right)\,\text{d}u \\  & =-\int {sec}^{2}⁡u\,\text{d}u \\  & =-\operatorname{tan}⁡u+C \\  & =- \tan{\left(\frac{6}{x} \right)}+C\end{aligned}\end{aligned}
$$


## q-350202 — captured original


Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\sqrt{\pi /12}}8xsec\,(4{x}^{2})tan\,(4{x}^{2})\,\text{d}x=$
{{field-1}}



Original complete bank:


- $1$


If we let $u=4{x}^{2},$ then

$$
\frac{\text{d}u}{\text{d}x}=8x\,⟹\,\text{d}u=8x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\sqrt{\pi /12}$ |
| --- | --- | --- |
| $u$ | $0$ | $\pi /3$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\sqrt{\pi /12}}8xsec\,(4{x}^{2})tan\,(4{x}^{2})\,\text{d}x & ={\int }_{0}^{\sqrt{\pi /12}}sec\,(4{x}^{2})tan\,(4{x}^{2})\cdot 8x\,\text{d}x \\  & ={\int }_{0}^{\pi /3}\operatorname{sec}⁡(u)\operatorname{tan}⁡(u)\,\text{d}u \\  & =\operatorname{sec}⁡(u)\,{|}_{0}^{\pi /3} \\  & =\operatorname{sec}⁡(\frac{\pi }{3})-\operatorname{sec}⁡(0) \\  & =2-1 \\  & =1\end{aligned}
$$


### Changed evidence-bank variant (ineligible)


Evaluate the following integral. Do not round the answer.

$\int_{0}^{\frac{\sqrt{3} \sqrt{\pi}}{6}} 9 x \tan{\left(4 x^{2} \right)} \sec{\left(4 x^{2} \right)}\,\text{d}x=$
{{field-1}}

- $\frac{9}{8}$

If we let $u=4{x}^{2},$ then

$$
\frac{\text{d}u}{\text{d}x}=8x\,⟹\,\text{d}u=8x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\sqrt{\pi /12}$ |
| --- | --- | --- |
| $u$ | $0$ | $\pi /3$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\sqrt{3} \sqrt{\pi}}{6}} 9 x \tan{\left(4 x^{2} \right)} \sec{\left(4 x^{2} \right)}\,\text{d}x & =\int_{0}^{\frac{\sqrt{3} \sqrt{\pi}}{6}} 9 \tan{\left(4 x^{2} \right)} \sec{\left(4 x^{2} \right)}\cdot x\,\text{d}x \\  & =\frac{9}{8}\int_{0}^{\frac{\pi}{3}} \tan{\left(u \right)} \sec{\left(u \right)}\,\text{d}u \\  & =\frac{9 \sec{\left(u \right)}}{8}\big|_{0}^{\frac{\pi}{3}} \\  & =\frac{9}{8}\left(\sec{\left(\left(\frac{\pi}{3}\right) \right)}-\left(\sec{\left(\left(0\right) \right)}\right)\right) \\  & =\frac{9}{8}\left(2-\left(1\right)\right) \\  & =\frac{9}{8}\end{aligned}
$$


### Generated normal variant 1


Evaluate the following integral. Give an exact answer.

$\int_{0}^{\frac{\sqrt{2} \sqrt{\pi}}{6}} 12 x \tan{\left(6 x^{2} \right)} \sec{\left(6 x^{2} \right)}\,\text{d}x=$
{{field-1}}

- $1$

If we let $u=6 x^{2},$ then

$$
\frac{\text{d}u}{\text{d}x}=12 x\,⟹\,\frac{1}{12}\text{d}u=x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{\sqrt{2} \sqrt{\pi}}{6}$ |
| --- | --- | --- |
| $u$ | $0$ | $\pi /3$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\sqrt{2} \sqrt{\pi}}{6}} 12 x \tan{\left(6 x^{2} \right)} \sec{\left(6 x^{2} \right)}\,\text{d}x & =\int_{0}^{\frac{\sqrt{2} \sqrt{\pi}}{6}} 12 \tan{\left(6 x^{2} \right)} \sec{\left(6 x^{2} \right)}\cdot x\,\text{d}x \\  & ={\int }_{0}^{\pi /3}\operatorname{sec}⁡(u)\operatorname{tan}⁡(u)\,\text{d}u \\  & =\operatorname{sec}⁡(u)\,{|}_{0}^{\pi /3} \\  & =\operatorname{sec}⁡(\frac{\pi }{3})-\operatorname{sec}⁡(0) \\  & =2-1 \\  & =1\end{aligned}
$$


### Generated normal variant 2


Evaluate the following integral. Give an exact answer.

$\int_{0}^{\frac{\sqrt{2} \sqrt{\pi}}{6}} 6 x \tan{\left(6 x^{2} \right)} \sec{\left(6 x^{2} \right)}\,\text{d}x=$
{{field-1}}

- $\frac{1}{2}$

If we let $u=6 x^{2},$ then

$$
\frac{\text{d}u}{\text{d}x}=12 x\,⟹\,\frac{1}{12}\text{d}u=x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{\sqrt{2} \sqrt{\pi}}{6}$ |
| --- | --- | --- |
| $u$ | $0$ | $\pi /3$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\sqrt{2} \sqrt{\pi}}{6}} 6 x \tan{\left(6 x^{2} \right)} \sec{\left(6 x^{2} \right)}\,\text{d}x & =\int_{0}^{\frac{\sqrt{2} \sqrt{\pi}}{6}} 6 \tan{\left(6 x^{2} \right)} \sec{\left(6 x^{2} \right)}\cdot x\,\text{d}x \\  & =\frac{1}{2}\int_{0}^{\frac{\pi}{3}} \tan{\left(u \right)} \sec{\left(u \right)}\,\text{d}u \\  & =\frac{\sec{\left(u \right)}}{2}\big|_{0}^{\frac{\pi}{3}} \\  & =\frac{1}{2}\left(\sec{\left(\left(\frac{\pi}{3}\right) \right)}-\left(\sec{\left(\left(0\right) \right)}\right)\right) \\  & =\frac{1}{2}\left(2-\left(1\right)\right) \\  & =\frac{1}{2}\end{aligned}
$$


## q-350203 — captured original


Evaluate the following integral. Do not round the answer.

${\int }_{\sqrt{\pi /12}}^{\sqrt{\pi /6}}12x\operatorname{cos}⁡(6{x}^{2})\,\text{d}x=$
{{field-1}}



Original complete bank:


- $-1$


If we let $u=6{x}^{2},$ then

$$
\frac{\text{d}u}{\text{d}x}=12x\,⟹\,\text{d}u=12x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $\sqrt{\pi /12}$ | $\sqrt{\pi /6}$ |
| --- | --- | --- |
| $u$ | $\pi /2$ | $\pi $ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{\sqrt{\pi /12}}^{\sqrt{\pi /6}}12x\operatorname{cos}⁡(6{x}^{2})\,\text{d}x & ={\int }_{\sqrt{\pi /12}}^{\sqrt{\pi /6}}\operatorname{cos}⁡(6{x}^{2})\cdot 12x\,\text{d}x \\  & ={\int }_{\pi /2}^{\pi }\operatorname{cos}⁡(u)\,\text{d}u \\  & =\operatorname{sin}⁡(u)\,{|}_{\pi /2}^{\pi } \\  & =\operatorname{sin}⁡(\pi )-\operatorname{sin}⁡(\frac{\pi }{2}) \\  & =0-1 \\  & =-1\end{aligned}
$$


### Changed evidence-bank variant (ineligible)


Evaluate the following integral. Do not round the answer.

$\int_{\frac{\sqrt{3} \sqrt{\pi}}{6}}^{\frac{\sqrt{6} \sqrt{\pi}}{6}} x \cos{\left(6 x^{2} \right)}\,\text{d}x=$
{{field-1}}

- $- \frac{1}{12}$

If we let $u=6{x}^{2},$ then

$$
\frac{\text{d}u}{\text{d}x}=12x\,⟹\,\text{d}u=12x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $\sqrt{\pi /12}$ | $\sqrt{\pi /6}$ |
| --- | --- | --- |
| $u$ | $\pi /2$ | $\pi $ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{\sqrt{3} \sqrt{\pi}}{6}}^{\frac{\sqrt{6} \sqrt{\pi}}{6}} x \cos{\left(6 x^{2} \right)}\,\text{d}x & =\int_{\frac{\sqrt{3} \sqrt{\pi}}{6}}^{\frac{\sqrt{6} \sqrt{\pi}}{6}} \cos{\left(6 x^{2} \right)}\cdot x\,\text{d}x \\  & =\frac{1}{12}\int_{\frac{\pi}{2}}^{\pi} \cos{\left(u \right)}\,\text{d}u \\  & =\frac{\sin{\left(u \right)}}{12}\big|_{\frac{\pi}{2}}^{\pi} \\  & =\frac{1}{12}\left(\sin{\left(\left(\pi\right) \right)}-\left(\sin{\left(\left(\frac{\pi}{2}\right) \right)}\right)\right) \\  & =\frac{1}{12}\left(0-\left(1\right)\right) \\  & =- \frac{1}{12}\end{aligned}
$$


### Generated normal variant 1


Evaluate the following integral. Give an exact answer.

$\int_{\frac{\sqrt{3} \sqrt{\pi}}{6}}^{\frac{\sqrt{6} \sqrt{\pi}}{6}} 12 x \cos{\left(6 x^{2} \right)}\,\text{d}x=$
{{field-1}}

- $-1$

If we let $u=6{x}^{2},$ then

$$
\frac{\text{d}u}{\text{d}x}=12x\,⟹\,\text{d}u=12x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $\sqrt{\pi /12}$ | $\sqrt{\pi /6}$ |
| --- | --- | --- |
| $u$ | $\pi /2$ | $\pi$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{\sqrt{\pi /12}}^{\sqrt{\pi /6}}12x\operatorname{cos}⁡(6{x}^{2})\,\text{d}x & ={\int }_{\sqrt{\pi /12}}^{\sqrt{\pi /6}}\operatorname{cos}⁡(6{x}^{2})\cdot 12x\,\text{d}x \\  & ={\int }_{\pi /2}^{\pi }\operatorname{cos}⁡(u)\,\text{d}u \\  & =\operatorname{sin}⁡(u)\,{|}_{\pi /2}^{\pi } \\  & =\operatorname{sin}⁡(\pi )-\operatorname{sin}⁡(\frac{\pi }{2}) \\  & =0-1 \\  & =-1\end{aligned}
$$


### Generated normal variant 2


Evaluate the following integral. Give an exact answer.

$\int_{\frac{\sqrt{3} \sqrt{\pi}}{6}}^{\frac{\sqrt{6} \sqrt{\pi}}{6}} 6 x \cos{\left(6 x^{2} \right)}\,\text{d}x=$
{{field-1}}

- $- \frac{1}{2}$

If we let $u=6{x}^{2},$ then

$$
\frac{\text{d}u}{\text{d}x}=12x\,⟹\,\text{d}u=12x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $\sqrt{\pi /12}$ | $\sqrt{\pi /6}$ |
| --- | --- | --- |
| $u$ | $\pi /2$ | $\pi$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{\sqrt{3} \sqrt{\pi}}{6}}^{\frac{\sqrt{6} \sqrt{\pi}}{6}} 6 x \cos{\left(6 x^{2} \right)}\,\text{d}x & =\int_{\frac{\sqrt{3} \sqrt{\pi}}{6}}^{\frac{\sqrt{6} \sqrt{\pi}}{6}} 6 \cos{\left(6 x^{2} \right)}\cdot x\,\text{d}x \\  & =\frac{1}{2}\int_{\frac{\pi}{2}}^{\pi} \cos{\left(u \right)}\,\text{d}u \\  & =\frac{\sin{\left(u \right)}}{2}\big|_{\frac{\pi}{2}}^{\pi} \\  & =\frac{1}{2}\left(\sin{\left(\left(\pi\right) \right)}-\left(\sin{\left(\left(\frac{\pi}{2}\right) \right)}\right)\right) \\  & =\frac{1}{2}\left(0-\left(1\right)\right) \\  & =- \frac{1}{2}\end{aligned}
$$


## Authored easy from the preceding nonlinear-product tutorial



### Generated easy cos


Calculate $\int 4 x \cos{\left(2 x^{2} \right)}\,\text{d}x.$

- $4 \sin{\left(2 x^{2} \right)}+C$
- $- \sin{\left(2 x^{2} \right)}+C$
- $\sin{\left(2 x^{2} \right)}+C$
- $\cos{\left(2 x^{2} \right)}+C$
- $\frac{\sin{\left(2 x^{2} \right)}}{4}+C$

Let $u=2 x^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=4 x\,⟹\,\frac{1}{4}\text{d}u=x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 4 x \cos{\left(2 x^{2} \right)}\,\text{d}x &=\int 4 \cos{\left(2 x^{2} \right)}\cdot x\,\text{d}x \\ &=4\int \cos{\left(u \right)}\cdot \left(\frac{1}{4}\right)\,\text{d}u \\ &=1\int \cos{\left(u \right)}\,\text{d}u \\ &=\sin{\left(u \right)}+C \\ &=\sin{\left(2 x^{2} \right)}+C\end{aligned}
$$


### Generated easy sin


Calculate $\int 10 x \sin{\left(5 x^{2} \right)}\,\text{d}x.$

- $- 10 \cos{\left(5 x^{2} \right)}+C$
- $\cos{\left(5 x^{2} \right)}+C$
- $- \cos{\left(5 x^{2} \right)}+C$
- $\sin{\left(5 x^{2} \right)}+C$
- $- \frac{\cos{\left(5 x^{2} \right)}}{10}+C$

Let $u=5 x^{2}.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=10 x\,⟹\,\frac{1}{10}\text{d}u=x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 10 x \sin{\left(5 x^{2} \right)}\,\text{d}x &=\int 10 \sin{\left(5 x^{2} \right)}\cdot x\,\text{d}x \\ &=10\int \sin{\left(u \right)}\cdot \left(\frac{1}{10}\right)\,\text{d}u \\ &=1\int \sin{\left(u \right)}\,\text{d}u \\ &=- \cos{\left(u \right)}+C \\ &=- \cos{\left(5 x^{2} \right)}+C\end{aligned}
$$
