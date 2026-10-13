# Source replay and bounded variants

## Source q-100642

${\int }_{0}^{\infty }\frac{2}{\sqrt[3]{2z+1}}\,\text{d}z=$

selection: \frac{4}{3}, 3, The integral is divergent [correct], 6, \frac{2}{3}

We proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{2}{\sqrt[3]{2z+1}}\,\text{d}z & ={lim}_{a\to \infty }{\int }_{0}^{a}\frac{2}{\sqrt[3]{2z+1}}\,\text{d}z \\  & ={lim}_{a\to \infty }{[\frac{3}{2}(2z+1)^{2/3}]}_{0}^{a} \\  & =\frac{3}{2}\cdot {lim}_{a\to \infty }{[(2z+1)^{2/3}]}_{0}^{a} \\  & =\frac{3}{2}\cdot {lim}_{a\to \infty }((2a+1)^{2/3}-1) \\  & =\frac{3}{2}\cdot \infty  \\  & =\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Boundary variant q-100642

${\int }_{0}^{\infty }\frac{2}{\sqrt[21]{2z+1}}\,\text{d}z=$

selection: The integral is divergent [correct], 21, \frac{22}{21}, \frac{20}{21}, 42

We proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{2}{\sqrt[21]{2z+1}}\,\text{d}z & ={lim}_{a\to \infty }{\int }_{0}^{a}\frac{2}{\sqrt[21]{2z+1}}\,\text{d}z \\  & ={lim}_{a\to \infty }{[\frac{21}{20}(2z+1)^{20/21}]}_{0}^{a} \\  & =\frac{21}{20}\cdot {lim}_{a\to \infty }{[(2z+1)^{20/21}]}_{0}^{a} \\  & =\frac{21}{20}\cdot {lim}_{a\to \infty }((2a+1)^{20/21}-1) \\  & =\frac{21}{20}\cdot \infty  \\  & =\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Source q-5964

${\int }_{1}^{\infty }-\frac{6}{\sqrt[5]{x}}\,\text{d}x=$

selection: The integral is divergent [correct], -\frac{1}{2}, -\frac{15}{8}, -\frac{15}{2}, -\frac{3}{2}

We proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{1}^{\infty }-\frac{6}{\sqrt[5]{x}}\,\text{d}x & =-6\cdot {lim}_{a\to \infty }{\int }_{1}^{a}\frac{1}{\sqrt[5]{x}}\,\text{d}x \\  & =-6\cdot {lim}_{a\to \infty }{[\frac{5}{4}{x}^{4/5}]}_{1}^{a} \\  & =-\frac{15}{2}\cdot {lim}_{a\to \infty }{[{x}^{4/5}]}_{1}^{a} \\  & =-\frac{15}{2}\cdot {lim}_{a\to \infty }({a}^{4/5}-1) \\  & =-\frac{15}{2}\cdot \infty  \\  & =-\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Boundary variant q-5964

${\int }_{1}^{\infty }-\frac{6}{\sqrt[21]{x}}\,\text{d}x=$

selection: - \frac{63}{40}, - \frac{21}{50}, The integral is divergent [correct], - \frac{63}{50}, - \frac{63}{10}

We proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{1}^{\infty }-\frac{6}{\sqrt[21]{x}}\,\text{d}x & =-6\cdot {lim}_{a\to \infty }{\int }_{1}^{a}\frac{1}{\sqrt[21]{x}}\,\text{d}x \\  & =-6\cdot {lim}_{a\to \infty }{[\frac{21}{20}{x}^{20/21}]}_{1}^{a} \\  & =-\frac{63}{10}\cdot {lim}_{a\to \infty }{[{x}^{20/21}]}_{1}^{a} \\  & =-\frac{63}{10}\cdot {lim}_{a\to \infty }({a}^{20/21}-1) \\  & =-\frac{63}{10}\cdot \infty  \\  & =-\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Source q-100643

Evaluate ${\int }_{-\infty }^{-1}\frac{\text{d}t}{\sqrt{2-3t}}.$

selection: The integral is divergent [correct], \frac{3}{2}, -\frac{2}{3}, \frac{2\sqrt{5}}{3}, -2\sqrt{5}

We proceed by setting the lower bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to -\infty .$

$$
\begin{aligned}{\int }_{-\infty }^{-1}\frac{\text{d}t}{\sqrt{2-3t}} & ={lim}_{a\to -\infty }{\int }_{a}^{-1}\frac{\text{d}t}{\sqrt{2-3t}} \\  & ={lim}_{a\to -\infty }{[-\frac{2}{3}\sqrt{2-3t}]}_{a}^{-1} \\  & =-\frac{2}{3}\cdot {lim}_{a\to -\infty }(\sqrt{2+3}-\sqrt{2-3a}) \\  & =-\frac{2\sqrt{5}}{3}+\frac{2}{3}{lim}_{a\to -\infty }\sqrt{2-3a} \\  & =-\frac{2\sqrt{5}}{3}+\infty  \\  & =\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Boundary variant q-100643

Evaluate ${\int }_{-\infty }^{-1}\frac{\text{d}t}{\sqrt{2-20t}}.$

selection: - \frac{1}{10}, 10, The integral is divergent [correct], - 2\sqrt{22}, \frac{\sqrt{22}}{10}

We proceed by setting the lower bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to -\infty .$

$$
\begin{aligned}{\int }_{-\infty }^{-1}\frac{\text{d}t}{\sqrt{2-20t}} & ={lim}_{a\to -\infty }{\int }_{a}^{-1}\frac{\text{d}t}{\sqrt{2-20t}} \\  & ={lim}_{a\to -\infty }{[-\frac{1}{10}\sqrt{2-20t}]}_{a}^{-1} \\  & =-\frac{1}{10}\cdot {lim}_{a\to -\infty }(\sqrt{2+20}-\sqrt{2-20a}) \\  & =-\frac{\sqrt{22}}{10}+\frac{1}{10}{lim}_{a\to -\infty }\sqrt{2-20a} \\  & =-\frac{\sqrt{22}}{10}+\infty  \\  & =\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Source q-80342

Evaluate ${\int }_{-\infty }^{0}\frac{\text{d}z}{\sqrt{1-z}}.$

selection: -1, -\frac{1}{2}, The integral is divergent [correct], -2, -4

We proceed by setting the lower bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to -\infty .$

$$
\begin{aligned}{\int }_{-\infty }^{0}\frac{\text{d}z}{\sqrt{1-z}} & ={lim}_{a\to -\infty }{\int }_{a}^{0}\frac{\text{d}z}{\sqrt{1-z}} \\  & ={lim}_{a\to -\infty }{[-2\sqrt{1-z}]}_{a}^{0} \\  & =-2\cdot {lim}_{a\to -\infty }(\sqrt{1-0}-\sqrt{1-a}) \\  & =-2+2\cdot {lim}_{a\to -\infty }\sqrt{1-a} \\  & =-2+2\cdot \infty  \\  & =\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Boundary variant q-80342

Evaluate ${\int }_{-\infty }^{0}\frac{\text{d}z}{\sqrt{20-z}}.$

selection: The integral is divergent [correct], -\sqrt{5}, - 2\sqrt{5}, - 8\sqrt{5}, - 4\sqrt{5}

We proceed by setting the lower bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to -\infty .$

$$
\begin{aligned}{\int }_{-\infty }^{0}\frac{\text{d}z}{\sqrt{20-z}} & ={lim}_{a\to -\infty }{\int }_{a}^{0}\frac{\text{d}z}{\sqrt{20-z}} \\  & ={lim}_{a\to -\infty }{[-2\sqrt{20-z}]}_{a}^{0} \\  & =-2\cdot {lim}_{a\to -\infty }(\sqrt{20-0}-\sqrt{20-a}) \\  & =-4\sqrt{5}+2\cdot {lim}_{a\to -\infty }\sqrt{20-a} \\  & =-4\sqrt{5}+2\cdot \infty  \\  & =\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Source q-80347

Evaluate ${\int }_{-\infty }^{-1}\frac{{x}^{2}}{\sqrt{8-{x}^{3}}}\,\text{d}x.$

selection: \frac{1}{3}, -2, 2, -\frac{2}{3}, The integral is divergent [correct]

First, we substitute $u=8-{x}^{3}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=-3{x}^{2}\,⟹\,-\frac{1}{3}\,\text{d}u={x}^{2}\text{d}x.
$$

Since $u\to \infty $ when $x\to -\infty ,$ the table for the limits of integration using the rule $u=8-{x}^{3}$ is as follows:

$$
\begin{aligned}x & -1 & -\infty  \\ u & 9 & \infty \end{aligned}
$$

So, the integral in terms of the new variable $u$ is

$$
{\int }_{-\infty }^{-1}\frac{{x}^{2}}{\sqrt{8-{x}^{3}}}\,\text{d}x={\int }_{\infty }^{9}(-\frac{1}{3\sqrt{u}})\,\text{d}u=\frac{1}{3}{\int }_{9}^{\infty }\frac{1}{\sqrt{u}}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{-\infty }^{-1}\frac{{x}^{2}}{\sqrt{8-{x}^{3}}}\,\text{d}x & =\frac{1}{3}\cdot {lim}_{a\to \infty }{\int }_{9}^{a}\frac{1}{\sqrt{u}}\,\text{d}u \\  & =\frac{1}{3}\cdot {lim}_{a\to \infty }{[2\sqrt{u}]}_{9}^{a} \\  & =\frac{2}{3}\cdot {lim}_{a\to \infty }[\sqrt{a}-\sqrt{9}] \\  & =\frac{2}{3}\cdot \infty  \\  & =\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Boundary variant q-80347

Evaluate ${\int }_{-\infty }^{-1}\frac{{x}^{2}}{\sqrt{30-{x}^{3}}}\,\text{d}x.$

selection: 2, -2, \frac{1}{3}, The integral is divergent [correct], -\frac{2}{3}

First, we substitute $u=30-{x}^{3}.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=-3{x}^{2}\,⟹\,-\frac{1}{3}\,\text{d}u={x}^{2}\text{d}x.
$$

Since $u\to \infty $ when $x\to -\infty ,$ the table for the limits of integration using the rule $u=30-{x}^{3}$ is as follows:

$$
\begin{aligned}x & -1 & -\infty  \\ u & 31 & \infty \end{aligned}
$$

So, the integral in terms of the new variable $u$ is

$$
{\int }_{-\infty }^{-1}\frac{{x}^{2}}{\sqrt{30-{x}^{3}}}\,\text{d}x={\int }_{\infty }^{31}(-\frac{1}{3\sqrt{u}})\,\text{d}u=\frac{1}{3}{\int }_{31}^{\infty }\frac{1}{\sqrt{u}}\,\text{d}u.
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{-\infty }^{-1}\frac{{x}^{2}}{\sqrt{30-{x}^{3}}}\,\text{d}x & =\frac{1}{3}\cdot {lim}_{a\to \infty }{\int }_{31}^{a}\frac{1}{\sqrt{u}}\,\text{d}u \\  & =\frac{1}{3}\cdot {lim}_{a\to \infty }{[2\sqrt{u}]}_{31}^{a} \\  & =\frac{2}{3}\cdot {lim}_{a\to \infty }[\sqrt{a}-\sqrt{31}] \\  & =\frac{2}{3}\cdot \infty  \\  & =\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Source q-6034

Evaluate ${\int }_{6}^{\infty }\frac{\text{d}z}{z}.$

selection: \frac{1}{\operatorname{ln}⁡(6)}, \operatorname{ln}⁡(6), 6\operatorname{ln}⁡(6), The integral diverges [correct], {e}^{6}

We proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{6}^{\infty }\frac{\text{d}z}{z} & ={lim}_{a\to \infty }{\int }_{6}^{a}\frac{\text{d}z}{z} \\  & ={lim}_{a\to \infty }{[\operatorname{ln}⁡z]}_{6}^{a} \\  & ={lim}_{a\to \infty }(\operatorname{ln}⁡a-\operatorname{ln}⁡6) \\  & =\infty -\operatorname{ln}⁡6 \\  & =\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Boundary variant q-6034

Evaluate ${\int }_{30}^{\infty }\frac{\text{d}z}{z}.$

selection: 30 \operatorname{ln}{\left(30 \right)}, \operatorname{ln}{\left(30 \right)}, \frac{1}{\operatorname{ln}{\left(30 \right)}}, e^{30}, The integral diverges [correct]

We proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{30}^{\infty }\frac{\text{d}z}{z} & ={lim}_{a\to \infty }{\int }_{30}^{a}\frac{\text{d}z}{z} \\  & ={lim}_{a\to \infty }{[\operatorname{ln}⁡z]}_{30}^{a} \\  & ={lim}_{a\to \infty }(\operatorname{ln}⁡a-\operatorname{ln}⁡30) \\  & =\infty -\operatorname{ln}⁡30 \\  & =\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Source q-20700

Evaluate the integral ${\int }_{2}^{\infty }\frac{1}{x\operatorname{ln}⁡x}\,\text{d}x.$

selection: The integral is divergent [correct], 2\operatorname{ln}⁡(2), {e}^{2}, \operatorname{ln}⁡(2), \frac{1}{\operatorname{ln}⁡(2)}

First, we substitute $u=\operatorname{ln}⁡x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\,⟹\,\text{d}u=\frac{1}{x}\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u=\operatorname{ln}⁡x$ is as follows:

$$
\begin{aligned}x & 2 & \infty  \\ u & \operatorname{ln}⁡2 & \infty \end{aligned}
$$

So, the integral in terms of the new variable $u$ is

$$
\begin{aligned}{\int }_{2}^{\infty }\frac{1}{x\operatorname{ln}⁡(x)}\,\text{d}x & ={\int }_{\operatorname{ln}⁡2}^{\infty }\frac{1}{u}\,\text{d}u.\end{aligned}
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{2}^{\infty }\frac{1}{x\operatorname{ln}⁡x}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{\operatorname{ln}⁡2}^{a}\frac{1}{u}\,\text{d}u \\  & ={lim}_{a\to \infty }{[\operatorname{ln}⁡u]}_{\operatorname{ln}⁡2}^{a} \\  & ={lim}_{a\to \infty }[\operatorname{ln}⁡a-\operatorname{ln}⁡(\operatorname{ln}⁡2)] \\  & =\infty -\operatorname{ln}⁡(\operatorname{ln}⁡2) \\  & =\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Boundary variant q-20700

Evaluate the integral ${\int }_{30}^{\infty }\frac{1}{x\operatorname{ln}⁡x}\,\text{d}x.$

selection: e^{30}, 30 \operatorname{ln}{\left(30 \right)}, The integral is divergent [correct], \frac{1}{\operatorname{ln}{\left(30 \right)}}, \operatorname{ln}{\left(30 \right)}

First, we substitute $u=\operatorname{ln}⁡x.$ Differentiating, we get

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{x}\,⟹\,\text{d}u=\frac{1}{x}\text{d}x.
$$

Since $u\to \infty $ when $x\to \infty ,$ the table for the limits of integration using the rule $u=\operatorname{ln}⁡x$ is as follows:

$$
\begin{aligned}x & 30 & \infty  \\ u & \operatorname{ln}⁡30 & \infty \end{aligned}
$$

So, the integral in terms of the new variable $u$ is

$$
\begin{aligned}{\int }_{30}^{\infty }\frac{1}{x\operatorname{ln}⁡(x)}\,\text{d}x & ={\int }_{\operatorname{ln}⁡30}^{\infty }\frac{1}{u}\,\text{d}u.\end{aligned}
$$

Finally, we proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{30}^{\infty }\frac{1}{x\operatorname{ln}⁡x}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{\operatorname{ln}⁡30}^{a}\frac{1}{u}\,\text{d}u \\  & ={lim}_{a\to \infty }{[\operatorname{ln}⁡u]}_{\operatorname{ln}⁡30}^{a} \\  & ={lim}_{a\to \infty }[\operatorname{ln}⁡a-\operatorname{ln}⁡(\operatorname{ln}⁡30)] \\  & =\infty -\operatorname{ln}⁡(\operatorname{ln}⁡30) \\  & =\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Source q-20698

Evaluate the integral ${\int }_{0}^{\infty }\frac{1}{3x+1}\,\text{d}x.$

selection: The integral is divergent [correct], \frac{1}{3}, \operatorname{ln}⁡(3), \frac{1}{3\operatorname{ln}⁡(3)}, 3\operatorname{ln}⁡(3)

We proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{1}{3x+1}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{0}^{a}\frac{1}{3x+1}\,\text{d}x \\  & ={lim}_{a\to \infty }{[\frac{1}{3}\cdot \operatorname{ln}⁡|3x+1|]}_{0}^{a} \\  & =\frac{1}{3}\cdot {lim}_{a\to \infty }{[\operatorname{ln}⁡|3x+1|]}_{0}^{a} \\  & =\frac{1}{3}\cdot {lim}_{a\to \infty }(\operatorname{ln}⁡|3a+1|-\operatorname{ln}⁡(1)) \\  & =\frac{1}{3}\cdot {lim}_{a\to \infty }(\operatorname{ln}⁡|3a+1|) \\  & =\frac{1}{3}\cdot (\infty ) \\  & =\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Boundary variant q-20698

Evaluate the integral ${\int }_{0}^{\infty }\frac{1}{30x+1}\,\text{d}x.$

selection: \operatorname{ln}{\left(30 \right)}, \frac{1}{30}, The integral is divergent [correct], 30 \operatorname{ln}{\left(30 \right)}, \frac{1}{30 \operatorname{ln}{\left(30 \right)}}

We proceed by setting the upper bound equal to some parameter $a,$ integrating as usual, and then taking the limit as $a\to \infty .$

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{1}{30x+1}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{0}^{a}\frac{1}{30x+1}\,\text{d}x \\  & ={lim}_{a\to \infty }{[\frac{1}{30}\cdot \operatorname{ln}⁡|30x+1|]}_{0}^{a} \\  & =\frac{1}{30}\cdot {lim}_{a\to \infty }{[\operatorname{ln}⁡|30x+1|]}_{0}^{a} \\  & =\frac{1}{30}\cdot {lim}_{a\to \infty }(\operatorname{ln}⁡|30a+1|-\operatorname{ln}⁡(1)) \\  & =\frac{1}{30}\cdot {lim}_{a\to \infty }(\operatorname{ln}⁡|30a+1|) \\  & =\frac{1}{30}\cdot (\infty ) \\  & =\infty .\end{aligned}
$$

Therefore, the integral is divergent.

---

## Source q-6032

Which of the following improper integrals are divergent?
- **I.** ${\int }_{10}^{\infty }\frac{1}{\sqrt{x-1}}\,\text{d}x$
- **II.** ${\int }_{-\infty }^{-1}\frac{1}{x}\,\text{d}x$
- **III.** ${\int }_{1}^{\infty }\frac{1}{{x}^{2}}\,\text{d}x$

Select all that apply.

I: false, true [correct]
II: false, true [correct]
III: false [correct], true

Let's work out each integral.

For the first integral, we have

$$
\begin{aligned}{\int }_{10}^{\infty }\frac{1}{\sqrt{x-1}}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{10}^{a}\frac{1}{\sqrt{x-1}}\,\text{d}x \\  & ={lim}_{a\to \infty }{[2\sqrt{x-1}]}_{10}^{a} \\  & ={lim}_{a\to \infty }(2\sqrt{a-1}-2\sqrt{10-1}) \\  & ={lim}_{a\to \infty }(2\sqrt{a-1}-6) \\  & =\infty ,\end{aligned}
$$

so the integral diverges.

For the second integral, we have

$$
\begin{aligned}{\int }_{-\infty }^{-1}\frac{1}{x}\,\text{d}x & ={lim}_{a\to -\infty }{\int }_{a}^{-1}\frac{1}{x}\,\text{d}x \\  & ={lim}_{a\to -\infty }{[\operatorname{ln}⁡|x|]}_{a}^{-1} \\  & ={lim}_{a\to -\infty }(\operatorname{ln}⁡|-1|-\operatorname{ln}⁡|a|) \\  & =-\infty ,\end{aligned}
$$

so the integral diverges.

For the third integral, we have

$$
\begin{aligned}{\int }_{1}^{\infty }\frac{1}{{x}^{2}}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{1}^{a}\frac{1}{{x}^{2}}\,\text{d}x \\  & ={lim}_{a\to \infty }{[-\frac{1}{x}]}_{1}^{a} \\  & ={lim}_{a\to \infty }(-\frac{1}{a}+\frac{1}{1}) \\  & =1,\end{aligned}
$$

so the integral is convergent.

In conclusion, only integrals I and II are divergent.

---

## Boundary variant q-6032

Which of the following improper integrals are divergent?
- **I.** ${\int }_{401}^{\infty }\frac{1}{\sqrt{x-1}}\,\text{d}x$
- **II.** ${\int }_{-\infty }^{-1}\frac{1}{x}\,\text{d}x$
- **III.** ${\int }_{1}^{\infty }\frac{1}{{x}^{2}}\,\text{d}x$

Select all that apply.

I: false, true [correct]
II: false, true [correct]
III: true, false [correct]

Let's work out each integral.

For the first integral, we have

$$
\begin{aligned}{\int }_{401}^{\infty }\frac{1}{\sqrt{x-1}}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{401}^{a}\frac{1}{\sqrt{x-1}}\,\text{d}x \\  & ={lim}_{a\to \infty }{[2\sqrt{x-1}]}_{401}^{a} \\  & ={lim}_{a\to \infty }(2\sqrt{a-1}-2\sqrt{401-1}) \\  & ={lim}_{a\to \infty }(2\sqrt{a-1}-40) \\  & =\infty ,\end{aligned}
$$

so the integral diverges.

For the second integral, we have

$$
\begin{aligned}{\int }_{-\infty }^{-1}\frac{1}{x}\,\text{d}x & ={lim}_{a\to -\infty }{\int }_{a}^{-1}\frac{1}{x}\,\text{d}x \\  & ={lim}_{a\to -\infty }{[\operatorname{ln}⁡|x|]}_{a}^{-1} \\  & ={lim}_{a\to -\infty }(\operatorname{ln}⁡|-1|-\operatorname{ln}⁡|a|) \\  & =-\infty ,\end{aligned}
$$

so the integral diverges.

For the third integral, we have

$$
\begin{aligned}{\int }_{1}^{\infty }\frac{1}{{x}^{2}}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{1}^{a}\frac{1}{{x}^{2}}\,\text{d}x \\  & ={lim}_{a\to \infty }{[-\frac{1}{x}]}_{1}^{a} \\  & ={lim}_{a\to \infty }(-\frac{1}{a}+\frac{1}{1}) \\  & =1,\end{aligned}
$$

so the integral is convergent.

In conclusion, only integrals I and II are divergent.

---

## Source q-101735

Which of the following improper integrals are divergent?
- **I.** ${\int }_{-\infty }^{-2}\frac{1}{{u}^{3}}\,\text{d}u$
- **II.** ${\int }_{0}^{\infty }\frac{1}{(z+3)^{2}}\,\text{d}z$
- **III.** ${\int }_{2}^{\infty }\frac{1}{x}\,\text{d}x$

Select all that apply.

I: false [correct], true
II: false [correct], true
III: false, true [correct]

Let's work out each integral.

For the first integral, we have

$$
\begin{aligned}{\int }_{-\infty }^{-2}\frac{1}{{u}^{3}}\,\text{d}u & ={lim}_{a\to -\infty }{\int }_{a}^{-2}\frac{1}{{u}^{3}}\,\text{d}u \\  & ={lim}_{a\to -\infty }{[-\frac{1}{2{u}^{2}}]}_{a}^{-2} \\  & ={lim}_{a\to -\infty }(-\frac{1}{2(-2)^{2}}+\frac{1}{2{a}^{2}}) \\  & ={lim}_{a\to -\infty }(\frac{1}{2{a}^{2}}-\frac{1}{8}) \\  & =-\frac{1}{8},\end{aligned}
$$

so the integral is convergent.

For the second integral, we have

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{1}{(z+3)^{2}}\,\text{d}z & ={lim}_{a\to \infty }{\int }_{0}^{a}\frac{1}{(z+3)^{2}}\,\text{d}z \\  & ={lim}_{a\to \infty }{[-\frac{1}{z+3}]}_{0}^{a} \\  & ={lim}_{a\to \infty }(-\frac{1}{a+3}+\frac{1}{0+3}) \\  & =\frac{1}{3},\end{aligned}
$$

so the integral is convergent.

For the third integral, we have

$$
\begin{aligned}{\int }_{2}^{\infty }\frac{1}{x}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{2}^{a}\frac{1}{x}\,\text{d}x \\  & ={lim}_{a\to \infty }[\operatorname{ln}⁡|x|]_{2}^{a} \\  & ={lim}_{a\to \infty }(\operatorname{ln}⁡a-\operatorname{ln}⁡2) \\  & =\infty ,\end{aligned}
$$

so the integral diverges.

In conclusion, only integrals III is divergent.

---

## Boundary variant q-101735

Which of the following improper integrals are divergent?
- **I.** ${\int }_{-\infty }^{-2}\frac{1}{{u}^{3}}\,\text{d}u$
- **II.** ${\int }_{0}^{\infty }\frac{1}{(z+3)^{2}}\,\text{d}z$
- **III.** ${\int }_{20}^{\infty }\frac{1}{x}\,\text{d}x$

Select all that apply.

I: false [correct], true
II: false [correct], true
III: true [correct], false

Let's work out each integral.

For the first integral, we have

$$
\begin{aligned}{\int }_{-\infty }^{-2}\frac{1}{{u}^{3}}\,\text{d}u & ={lim}_{a\to -\infty }{\int }_{a}^{-2}\frac{1}{{u}^{3}}\,\text{d}u \\  & ={lim}_{a\to -\infty }{[-\frac{1}{2{u}^{2}}]}_{a}^{-2} \\  & ={lim}_{a\to -\infty }(-\frac{1}{2(-2)^{2}}+\frac{1}{2{a}^{2}}) \\  & ={lim}_{a\to -\infty }(\frac{1}{2{a}^{2}}-\frac{1}{8}) \\  & =-\frac{1}{8},\end{aligned}
$$

so the integral is convergent.

For the second integral, we have

$$
\begin{aligned}{\int }_{0}^{\infty }\frac{1}{(z+3)^{2}}\,\text{d}z & ={lim}_{a\to \infty }{\int }_{0}^{a}\frac{1}{(z+3)^{2}}\,\text{d}z \\  & ={lim}_{a\to \infty }{[-\frac{1}{z+3}]}_{0}^{a} \\  & ={lim}_{a\to \infty }(-\frac{1}{a+3}+\frac{1}{0+3}) \\  & =\frac{1}{3},\end{aligned}
$$

so the integral is convergent.

For the third integral, we have

$$
\begin{aligned}{\int }_{20}^{\infty }\frac{1}{x}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{20}^{a}\frac{1}{x}\,\text{d}x \\  & ={lim}_{a\to \infty }[\operatorname{ln}⁡|x|]_{20}^{a} \\  & ={lim}_{a\to \infty }(\operatorname{ln}⁡a-\operatorname{ln}⁡20) \\  & =\infty ,\end{aligned}
$$

so the integral diverges.

In conclusion, only integrals III is divergent.

---

## Source q-101738

Which of the following improper integrals are divergent?
- **I.** ${\int }_{-\infty }^{0}\frac{1}{(u-1)^{2}}\,\text{d}u$
- **II.** ${\int }_{-\infty }^{0}t\,\text{d}t$
- **III.** ${\int }_{3}^{\infty }\frac{2}{\sqrt{x-2}}\,\text{d}x$

Select all that apply.

I: false [correct], true
II: false, true [correct]
III: false, true [correct]

Let's work out each integral.

For the first integral, we have

$$
\begin{aligned}{\int }_{-\infty }^{0}\frac{1}{(u-1)^{2}}\,\text{d}u & ={lim}_{a\to -\infty }{\int }_{a}^{0}\frac{1}{(u-1)^{2}}\,\text{d}u \\  & ={lim}_{a\to -\infty }{[-\frac{1}{u-1}]}_{a}^{0} \\  & ={lim}_{a\to -\infty }(1+\frac{1}{a-1}) \\  & =1,\end{aligned}
$$

so the integral is convergent.

For the second integral, we have

$$
\begin{aligned}{\int }_{-\infty }^{0}t\,\text{d}t & ={lim}_{a\to -\infty }{\int }_{a}^{0}t\,\text{d}t \\  & ={lim}_{a\to -\infty }{[\frac{1}{2}{t}^{2}]}_{a}^{0} \\  & =\frac{1}{2}{lim}_{a\to -\infty }(0-{a}^{2}) \\  & =-\frac{1}{2}{lim}_{a\to -\infty }{a}^{2} \\  & =-\infty ,\end{aligned}
$$

so the integral diverges.

For the third integral, we have

$$
\begin{aligned}{\int }_{3}^{\infty }\frac{2}{\sqrt{x-2}}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{3}^{a}\frac{2}{\sqrt{x-2}}\,\text{d}x \\  & ={lim}_{a\to \infty }{[4\sqrt{x-2}]}_{3}^{a} \\  & =4{lim}_{a\to \infty }(\sqrt{a-2}-\sqrt{3-2}) \\  & =4{lim}_{a\to \infty }(\sqrt{a-2}-1) \\  & =\infty ,\end{aligned}
$$

so the integral diverges.
In conclusion, only integrals II and III are divergent.

---

## Boundary variant q-101738

Which of the following improper integrals are divergent?
- **I.** ${\int }_{-\infty }^{0}\frac{1}{(u-1)^{2}}\,\text{d}u$
- **II.** ${\int }_{-\infty }^{0}t\,\text{d}t$
- **III.** ${\int }_{402}^{\infty }\frac{2}{\sqrt{x-2}}\,\text{d}x$

Select all that apply.

I: false [correct], true
II: false, true [correct]
III: true [correct], false

Let's work out each integral.

For the first integral, we have

$$
\begin{aligned}{\int }_{-\infty }^{0}\frac{1}{(u-1)^{2}}\,\text{d}u & ={lim}_{a\to -\infty }{\int }_{a}^{0}\frac{1}{(u-1)^{2}}\,\text{d}u \\  & ={lim}_{a\to -\infty }{[-\frac{1}{u-1}]}_{a}^{0} \\  & ={lim}_{a\to -\infty }(1+\frac{1}{a-1}) \\  & =1,\end{aligned}
$$

so the integral is convergent.

For the second integral, we have

$$
\begin{aligned}{\int }_{-\infty }^{0}t\,\text{d}t & ={lim}_{a\to -\infty }{\int }_{a}^{0}t\,\text{d}t \\  & ={lim}_{a\to -\infty }{[\frac{1}{2}{t}^{2}]}_{a}^{0} \\  & =\frac{1}{2}{lim}_{a\to -\infty }(0-{a}^{2}) \\  & =-\frac{1}{2}{lim}_{a\to -\infty }{a}^{2} \\  & =-\infty ,\end{aligned}
$$

so the integral diverges.

For the third integral, we have

$$
\begin{aligned}{\int }_{402}^{\infty }\frac{2}{\sqrt{x-2}}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{402}^{a}\frac{2}{\sqrt{x-2}}\,\text{d}x \\  & ={lim}_{a\to \infty }{[4\sqrt{x-2}]}_{402}^{a} \\  & =4{lim}_{a\to \infty }(\sqrt{a-2}-\sqrt{402-2}) \\  & =4{lim}_{a\to \infty }(\sqrt{a-2}-20) \\  & =\infty ,\end{aligned}
$$

so the integral diverges.
In conclusion, only integrals II and III are divergent.

---

## Source q-101734

Which of the following improper integrals are divergent?
- **I.** ${\int }_{6}^{\infty }\frac{1}{\sqrt{x-5}}\,\text{d}x$
- **II.** ${\int }_{1}^{\infty }\frac{1}{3\sqrt[3]{{x}^{2}}}\,\text{d}x$
- **III.** ${\int }_{-\infty }^{-1}\frac{1}{{x}^{2}}\,\text{d}x$

Select all that apply.

I: false, true [correct]
II: false, true [correct]
III: false [correct], true

Let's work out each integral.

For the first integral, we have

$$
\begin{aligned}{\int }_{6}^{\infty }\frac{1}{\sqrt{x-5}}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{6}^{a}\frac{1}{\sqrt{x-5}}\,\text{d}x \\  & ={lim}_{a\to \infty }{[2\sqrt{x-5}]}_{6}^{a} \\  & ={lim}_{a\to \infty }(2\sqrt{a-5}-2\sqrt{6-5}) \\  & ={lim}_{a\to \infty }(2\sqrt{a-5}-2) \\  & =\infty ,\end{aligned}
$$

so the integral diverges.

For the second integral, we have

$$
\begin{aligned}{\int }_{1}^{\infty }\frac{1}{3\sqrt[3]{{x}^{2}}}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{1}^{a}\frac{1}{3}\,{x}^{-2/3}\,\text{d}x \\  & ={lim}_{a\to \infty }{[{x}^{1/3}]}_{1}^{a} \\  & ={lim}_{a\to \infty }(\sqrt[3]{a}-1) \\  & =\infty ,\end{aligned}
$$

so the integral diverges.

For the third integral, we have

$$
\begin{aligned}{\int }_{-\infty }^{-1}\frac{1}{{x}^{2}}\,\text{d}x & ={lim}_{a\to -\infty }{\int }_{a}^{-1}\frac{1}{{x}^{2}}\,\text{d}x \\  & ={lim}_{a\to -\infty }{[-\frac{1}{x}]}_{a}^{-1} \\  & ={lim}_{a\to -\infty }(1+\frac{1}{a}) \\  & =1,\end{aligned}
$$

so the integral is convergent.

In conclusion, only integrals I and II are divergent.

---

## Boundary variant q-101734

Which of the following improper integrals are divergent?
- **I.** ${\int }_{405}^{\infty }\frac{1}{\sqrt{x-5}}\,\text{d}x$
- **II.** ${\int }_{1}^{\infty }\frac{1}{3\sqrt[3]{{x}^{2}}}\,\text{d}x$
- **III.** ${\int }_{-\infty }^{-1}\frac{1}{{x}^{2}}\,\text{d}x$

Select all that apply.

I: false, true [correct]
II: false, true [correct]
III: true, false [correct]

Let's work out each integral.

For the first integral, we have

$$
\begin{aligned}{\int }_{405}^{\infty }\frac{1}{\sqrt{x-5}}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{405}^{a}\frac{1}{\sqrt{x-5}}\,\text{d}x \\  & ={lim}_{a\to \infty }{[2\sqrt{x-5}]}_{405}^{a} \\  & ={lim}_{a\to \infty }(2\sqrt{a-5}-2\sqrt{405-5}) \\  & ={lim}_{a\to \infty }(2\sqrt{a-5}-40) \\  & =\infty ,\end{aligned}
$$

so the integral diverges.

For the second integral, we have

$$
\begin{aligned}{\int }_{1}^{\infty }\frac{1}{3\sqrt[3]{{x}^{2}}}\,\text{d}x & ={lim}_{a\to \infty }{\int }_{1}^{a}\frac{1}{3}\,{x}^{-2/3}\,\text{d}x \\  & ={lim}_{a\to \infty }{[{x}^{1/3}]}_{1}^{a} \\  & ={lim}_{a\to \infty }(\sqrt[3]{a}-1) \\  & =\infty ,\end{aligned}
$$

so the integral diverges.

For the third integral, we have

$$
\begin{aligned}{\int }_{-\infty }^{-1}\frac{1}{{x}^{2}}\,\text{d}x & ={lim}_{a\to -\infty }{\int }_{a}^{-1}\frac{1}{{x}^{2}}\,\text{d}x \\  & ={lim}_{a\to -\infty }{[-\frac{1}{x}]}_{a}^{-1} \\  & ={lim}_{a\to -\infty }(1+\frac{1}{a}) \\  & =1,\end{aligned}
$$

so the integral is convergent.

In conclusion, only integrals I and II are divergent.

---

## Source q-101736

Which of the following improper integrals are divergent?

I. ${\int }_{2}^{\infty }\frac{1}{(u-1)^{3}}\,\text{d}u$
II. ${\int }_{-\infty }^{1}3{z}^{2}\,\text{d}z$
III. ${\int }_{-\infty }^{-2}\frac{1}{{x}^{2}}\,\text{d}x$

Select all that apply.

I: false [correct], true
II: false, true [correct]
III: false [correct], true

Let's work out each integral.

For the first integral, we have

$$
\begin{aligned}{\int }_{2}^{\infty }\frac{1}{(u-1)^{3}}\,\text{d}u & ={lim}_{a\to \infty }{\int }_{2}^{a}\frac{1}{(u-1)^{3}}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-\frac{1}{2(u-1)^{2}}]}_{2}^{a} \\  & ={lim}_{a\to \infty }(-\frac{1}{2(a-1)^{2}}+\frac{1}{2(2-1)^{2}}) \\  & ={lim}_{a\to \infty }(\frac{1}{2}-\frac{1}{2(a-1)^{2}}) \\  & =\frac{1}{2},\end{aligned}
$$

so the integral is convergent.

For the second integral, we have

$$
\begin{aligned}{\int }_{-\infty }^{1}3{z}^{2}\,\text{d}z & ={lim}_{a\to -\infty }{\int }_{a}^{1}3{z}^{2}\,\text{d}z \\  & ={lim}_{a\to -\infty }{[{z}^{3}]}_{a}^{1} \\  & ={lim}_{a\to -\infty }(1-{a}^{3}) \\  & =\infty ,\end{aligned}
$$

so the integral diverges.

For the third integral, we have

$$
\begin{aligned}{\int }_{-\infty }^{-2}\frac{1}{{x}^{2}}\,\text{d}x & ={lim}_{a\to -\infty }{\int }_{a}^{-2}\frac{1}{{x}^{2}}\,\text{d}x \\  & ={lim}_{a\to -\infty }{[-\frac{1}{x}]}_{a}^{-2} \\  & ={lim}_{a\to -\infty }(\frac{1}{2}+\frac{1}{a}) \\  & =\frac{1}{2},\end{aligned}
$$

so the integral is convergent.

In conclusion, only integral II is divergent.

---

## Boundary variant q-101736

Which of the following improper integrals are divergent?

I. ${\int }_{2}^{\infty }\frac{1}{(u-1)^{3}}\,\text{d}u$
II. ${\int }_{-\infty }^{1}3{z}^{2}\,\text{d}z$
III. ${\int }_{-\infty }^{-20}\frac{1}{{x}^{2}}\,\text{d}x$

Select all that apply.

I: false [correct], true
II: false, true [correct]
III: true, false [correct]

Let's work out each integral.

For the first integral, we have

$$
\begin{aligned}{\int }_{2}^{\infty }\frac{1}{(u-1)^{3}}\,\text{d}u & ={lim}_{a\to \infty }{\int }_{2}^{a}\frac{1}{(u-1)^{3}}\,\text{d}u \\  & ={lim}_{a\to \infty }{[-\frac{1}{2(u-1)^{2}}]}_{2}^{a} \\  & ={lim}_{a\to \infty }(-\frac{1}{2(a-1)^{2}}+\frac{1}{2(2-1)^{2}}) \\  & ={lim}_{a\to \infty }(\frac{1}{2}-\frac{1}{2(a-1)^{2}}) \\  & =\frac{1}{2},\end{aligned}
$$

so the integral is convergent.

For the second integral, we have

$$
\begin{aligned}{\int }_{-\infty }^{1}3{z}^{2}\,\text{d}z & ={lim}_{a\to -\infty }{\int }_{a}^{1}3{z}^{2}\,\text{d}z \\  & ={lim}_{a\to -\infty }{[{z}^{3}]}_{a}^{1} \\  & ={lim}_{a\to -\infty }(1-{a}^{3}) \\  & =\infty ,\end{aligned}
$$

so the integral diverges.

For the third integral, we have

$$
\begin{aligned}{\int }_{-\infty }^{-20}\frac{1}{{x}^{2}}\,\text{d}x & ={lim}_{a\to -\infty }{\int }_{a}^{-20}\frac{1}{{x}^{2}}\,\text{d}x \\  & ={lim}_{a\to -\infty }{[-\frac{1}{x}]}_{a}^{-20} \\  & ={lim}_{a\to -\infty }(\frac{1}{20}+\frac{1}{a}) \\  & =\frac{1}{20},\end{aligned}
$$

so the integral is convergent.

In conclusion, only integral II is divergent.
