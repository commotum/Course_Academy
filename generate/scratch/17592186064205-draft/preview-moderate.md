$\int \sqrt{5x-84}\,\text{d}x=$

- $\frac{2}{15}\sqrt{(5x-84)^{3}}+C$
- $\frac{1}{5}\sqrt{5x-84}+C$
- $\frac{1}{5}\sqrt{(5x-84)^{3}}+C$
- $\frac{2}{3}\sqrt{(5x-84)^{3}}+C$
- $\frac{2}{3}\sqrt{5x-84}+C$

First, we rewrite the integral as

$$
\int (5x-84)^{1/2}\,\text{d}x.
$$

Now, we let $u=5x-84.$ Then differentiating with respect to $x$ gives

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\text{d}x=\frac{1}{5}\text{d}u.
$$

We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $x$ at the very end:

$$
\begin{aligned}\int (5x-84)^{1/2}\,\text{d}x & =\int {u}^{1/2}\cdot (\frac{1}{5})\,\text{d}u \\  & =\frac{1}{5}\int {u}^{1/2}\,\text{d}u \\  & =\frac{1}{5}\cdot \frac{2}{3}{u}^{3/2}+C \\  & =\frac{2}{15}{u}^{3/2}+C \\  & =\frac{2}{15}(5x-84)^{3/2}+C \\  & =\frac{2}{15}\sqrt{(5x-84)^{3}}+C\end{aligned}
$$

Let's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}[\frac{2}{15}\sqrt{(5x-84)^{3}}+C] & =\frac{2}{15}\cdot \frac{\text{d}}{\text{d}x}[\sqrt{(5x-84)^{3}}]+\frac{\text{d}}{\text{d}x}(C) \\  & =\frac{2}{15}\cdot \frac{\text{d}}{\text{d}x}[(5x-84)^{3/2}]+\frac{\text{d}}{\text{d}x}(C) \\  & =\frac{2}{15}\cdot \frac{3}{2}(5x-84)^{1/2}\cdot \frac{\text{d}}{\text{d}x}(5x-84)+0 \\  & =\frac{1}{5}(5x-84)^{1/2}\cdot 5 \\  & =(5x-84)^{1/2} \\  & =\sqrt{5x-84}\,✓\end{aligned}
$$

---

$\int \frac{1}{\sqrt{4y+95}}\,\text{d}y=$

- $\sqrt{4y+95}+C$
- $\frac{\sqrt{4y+95}}{3}+C$
- $\frac{3\sqrt{4y+95}}{2}+C$
- $\frac{\sqrt{4y+95}}{4}+C$
- $\frac{\sqrt{4y+95}}{2}+C$

First, we rewrite the integral as

$$
\int (4y+95)^{-1/2}\,\text{d}y.
$$

Now, we let $u=4y+95.$ Then differentiating with respect to $y$ gives

$$
\frac{\text{d}u}{\text{d}y}=4\,⟹\,\text{d}y=\frac{1}{4}\text{d}u.
$$

We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $y$ at the very end:

$$
\begin{aligned}\int (4y+95)^{-1/2}\,\text{d}y & =\int {u}^{-1/2}\cdot \frac{1}{4}\,\text{d}u \\  & =\frac{1}{4}\int {u}^{-1/2}\,\text{d}u \\  & =\frac{1}{4}\cdot \frac{1}{(1/2)}{u}^{1/2}+C \\  & =\frac{2}{4}\cdot {u}^{1/2}+C \\  & =\frac{1}{2}(4y+95)^{1/2}+C \\  & =\frac{\sqrt{4y+95}}{2}+C\end{aligned}
$$

Let's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:

$$
\begin{aligned}\frac{\text{d}}{\text{d}y}[\frac{\sqrt{4y+95}}{2}+C] & =\frac{1}{2}\cdot \frac{\text{d}}{\text{d}y}[\sqrt{4y+95}]+\frac{\text{d}}{\text{d}y}(C) \\  & =\frac{1}{2}\cdot \frac{\text{d}}{\text{d}y}[(4y+95)^{1/2}]+\frac{\text{d}}{\text{d}y}(C) \\  & =\frac{1}{2}\cdot \frac{1}{2}(4y+95)^{-1/2}\cdot \frac{\text{d}}{\text{d}y}(4y+95)+0 \\  & =\frac{1}{4}(4y+95)^{-1/2}\cdot 4 \\  & =\frac{1}{\sqrt{4y+95}}\,✓\end{aligned}
$$