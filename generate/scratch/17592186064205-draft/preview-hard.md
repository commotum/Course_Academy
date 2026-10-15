$\int \frac{1}{\sqrt[3]{(23-5s)^{2}}}\,\text{d}s=$

- $\frac{1}{\sqrt[3]{23-5s}}+C$
- $\sqrt{23-5s}+C$
- $\frac{5}{3\sqrt[4]{21-5s}}+C$
- $-\frac{5}{7}\sqrt[3]{23-5s}+C$
- $-\frac{3}{5}\sqrt[3]{23-5s}+C$

First, we rewrite the integral as

$$
\int (23-5s)^{-2/3}\,\text{d}s.
$$

Now, we let  $u=23-5s.$ Then differentiating with respect to $s$ gives

$$
\frac{\text{d}u}{\text{d}s}=-5\,⟹\,\text{d}s=-\frac{1}{5}\text{d}u.
$$

We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $s$ at the very end:

$$
\begin{aligned}\int (23-5s)^{-2/3}\,\text{d}s & =\int {u}^{-2/3}\cdot (-\frac{1}{5}\text{d}u) \\  & =-\frac{1}{5}\int {u}^{-2/3}\,\text{d}u \\  & =-\frac{1}{5}\cdot \frac{1}{1/3}{u}^{1/3}+C \\  & =-\frac{3}{5}{u}^{1/3}+C \\  & =-\frac{3}{5}(23-5s)^{1/3}+C \\  & =-\frac{3}{5}\sqrt[3]{23-5s}+C\end{aligned}
$$

Let's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:

$$
\begin{aligned}\frac{\text{d}}{\text{d}s}[-\frac{3}{5}\sqrt[3]{23-5s}+C] & =-\frac{3}{5}\cdot \frac{\text{d}}{\text{d}s}[\sqrt[3]{23-5s}]+\frac{\text{d}}{\text{d}s}(C) \\  & =-\frac{3}{5}\cdot \frac{\text{d}}{\text{d}s}[(23-5s)^{1/3}]+\frac{\text{d}}{\text{d}s}(C) \\  & =-\frac{3}{5}\cdot \frac{1}{3}(23-5s)^{-2/3}\cdot \frac{\text{d}}{\text{d}s}(23-5s)+0 \\  & =-\frac{1}{5}(23-5s)^{-2/3}\cdot (-5) \\  & =(23-5s)^{-2/3} \\  & =\frac{1}{\sqrt[3]{(23-5s)^{2}}}\,✓\end{aligned}
$$

---

Calculate the integral $\int \sqrt[3]{(y-87)^{5}}\,\text{d}y.$

- $8\sqrt[3]{(y-87)^{5}}+C$
- $3\sqrt[3]{(y-87)^{8}}+C$
- $\frac{8}{3}\sqrt[3]{(y-87)^{2}}+C$
- $\sqrt[3]{(y-87)^{8}}+C$
- $\frac{3}{8}\sqrt[3]{(y-87)^{8}}+C$

First, we rewrite the integral as

$$
\int (y-87)^{5/3}\,\text{d}y.
$$

Now, we let $u=y-87.$ Then differentiating with respect to $y$ gives

$$
\frac{\text{d}u}{\text{d}y}=1\,⟹\,\text{d}y=\text{d}u.
$$

We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $y$ at the very end:

$$
\begin{aligned}\int (y-87)^{5/3}\,\text{d}y & =\int {u}^{5/3}\,\text{d}u \\  & =\frac{{u}^{8/3}}{8/3}+C \\  & =\frac{3}{8}(y-87)^{8/3}+C \\  & =\frac{3}{8}\sqrt[3]{(y-87)^{8}}+C\end{aligned}
$$

Let's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:

$$
\begin{aligned}\frac{\text{d}}{\text{d}y}[\frac{3}{8}\sqrt[3]{(y-87)^{8}}] & =\frac{3}{8}\cdot \frac{\text{d}}{\text{d}y}[\sqrt[3]{(y-87)^{8}}]+\frac{\text{d}}{\text{d}y}(C) \\  & =\frac{3}{8}\cdot \frac{\text{d}}{\text{d}y}[(y-87)^{8/3}]+\frac{\text{d}}{\text{d}y}(C) \\  & =\frac{3}{8}\cdot \frac{8}{3}(y-87)^{5/3}\cdot \frac{\text{d}}{\text{d}y}(y-87)+0 \\  & =(y-87)^{5/3}\cdot 1 \\  & =\sqrt[3]{(y-87)^{5}}\,✓\end{aligned}
$$