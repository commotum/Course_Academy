$\int 9(75-2x)^{8}\,\text{d}x=$

- $\frac{1}{2}(75-2x)^{9}+C$
- $-\frac{9}{2}(75-2x)^{9}+C$
- $9(75-2x)^{9}+C$
- $\frac{9}{2}(75-2x)^{9}+C$
- $-\frac{1}{2}(75-2x)^{9}+C$

Let $u=75-2x.$ Then differentiating with respect to $x$ gives

$$
\frac{\text{d}u}{\text{d}x}=-2\,⟹\,\text{d}x=-\frac{1}{2}\text{d}u.
$$

We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $x$ at the very end:

$$
\begin{aligned}\int 9(75-2x)^{8}\,\text{d}x & =\int 9{u}^{8}\cdot (-\frac{1}{2})\text{d}u \\  & =9\cdot (-\frac{1}{2})\int {u}^{8}\cdot \,\text{d}u \\  & =-\frac{9}{2}\int {u}^{8}\,\text{d}u \\  & =-\frac{9}{2}\cdot \frac{{u}^{9}}{9}+C \\  & =-\frac{1}{2}{u}^{9}+C \\  & =-\frac{1}{2}(75-2x)^{9}+C\end{aligned}
$$

Let's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}[-\frac{1}{2}(75-2x)^{9}+C] & =-\frac{\text{d}}{\text{d}x}[\frac{1}{2}(75-2x)^{9}]+\frac{\text{d}}{\text{d}x}(C) \\  & =-\frac{9}{2}(75-2x)^{8}\cdot \frac{\text{d}}{\text{d}x}(75-2x)+0 \\  & =-\frac{9}{2}(75-2x)^{8}\cdot (-2) \\  & =9(75-2x)^{8}\,✓\end{aligned}
$$

---

$\int 16(56-2x)^{7}\,\text{d}x=$

- $-(56-2x)^{8}+C$
- $-\frac{1}{2}(56-2x)^{8}+C$
- $(56-2x)^{8}+C$
- $\frac{1}{8}(56-2x)^{8}+C$
- $\frac{1}{2}(56-2x)^{8}+C$

Let $u=56-2x.$ Then differentiating with respect to $x$ gives

$$
\frac{\text{d}u}{\text{d}x}=-2\,⟹\,\text{d}x=-\frac{1}{2}\text{d}u.
$$

We now write our integral in terms of $u,$ calculate the integral as normal, and write the final answer in terms of $x$ at the very end:

$$
\begin{aligned}\int 16(56-2x)^{7}\,\text{d}x & =\int 16{u}^{7}\cdot (-\frac{1}{2})\,\text{d}u \\  & =16\int {u}^{7}\cdot (-\frac{1}{2})\,\text{d}u \\  & =16\cdot (-\frac{1}{2})\int {u}^{7}\,\text{d}u \\  & =-8\cdot \frac{{u}^{8}}{8}+C \\  & =-{u}^{8}+C \\  & =-(56-2x)^{8}+C\end{aligned}
$$

Let's double-check that our result is correct. If we differentiate the result, then it should come out to the original integrand:

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}[-(56-2x)^{8}+C] & =-\frac{\text{d}}{\text{d}x}[(56-2x)^{8}]+\frac{\text{d}}{\text{d}x}(C) \\  & =-8(56-2x)^{7}\cdot \frac{\text{d}}{\text{d}x}(56-2x)+0 \\  & =-8(56-2x)^{7}\cdot (-2) \\  & =16(56-2x)^{7}\,✓\end{aligned}
$$
