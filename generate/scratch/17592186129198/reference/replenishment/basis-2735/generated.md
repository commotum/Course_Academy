### q-83957 — easy

Evaluate $\int_{0}^{\frac{2 \pi}{3}} \int_{2}^{4} r^{3} \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $15 \sqrt{3}$
- B. $30 \sqrt{3}$ **correct**
- C. $120 \sqrt{3}$
- D. $- 30 \sqrt{3}$
- E. $\frac{496 \sqrt{3}}{5}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{2 \pi}{3}} \int_{2}^{4} r^{3} \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{2 \pi}{3}} \cos{\left(\theta \right)} \int_{2}^{4} r^{3}\,\mathrm d r\,\mathrm d \theta \\
& = \int_{0}^{\frac{2 \pi}{3}} \cos{\left(\theta \right)} \left[\frac{r^{4}}{4}\right]_{2}^{4}\,\mathrm d \theta \\
& = \int_{0}^{\frac{2 \pi}{3}} \cos{\left(\theta \right)} \left(\frac{\left(4\right)^{4}-\left(2\right)^{4}}{4}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{2 \pi}{3}} 60 \cos{\left(\theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{0}^{\frac{2 \pi}{3}} 60 \cos{\left(\theta \right)}\,\mathrm d \theta & = \left[60 \sin{\left(\theta \right)}\right]_{0}^{\frac{2 \pi}{3}} \\
& = \left(\left(60 \sin{\left(\left(\frac{2 \pi}{3}\right) \right)}\right)\right)-\left(\left(60 \sin{\left(\left(0\right) \right)}\right)\right) \\
& = \left(\left(30 \sqrt{3}\right)\right)-\left(\left(0\right)\right) \\
& = 30 \sqrt{3}
\end{aligned}
$$


---

### cosine_double_partial — hard

Evaluate $\int_{0}^{\frac{\pi}{8}} \int_{0}^{4 \cos{\left(2 \theta \right)}} r\,\mathrm d r\,\mathrm d \theta.$

- A. $\frac{40 \sqrt{2}}{9}$
- B. $2 + \pi$
- C. $\frac{1}{2} + \frac{\pi}{4}$
- D. $- \frac{\pi}{2} - 1$
- E. $1 + \frac{\pi}{2}$ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{8}} \int_{0}^{4 \cos{\left(2 \theta \right)}} r\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{8}} \left[\frac{r^{2}}{2}\right]_{0}^{4 \cos{\left(2 \theta \right)}}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{8}} \left(\frac{\left(4 \cos{\left(2 \theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{8}} 8 \cos^{2}{\left(2 \theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we recall the double-angle formula

$$
\cos(2x)=2\cos^2 x-1.
$$

Substituting $x=2\theta$ and rearranging, we get

$$
\cos^2\left(2\theta\right)=\frac{1}{2}\left(1+\cos\left(4\theta\right)\right).
$$

Finally, we can finish our integral by integrating with respect to $\theta,$ as follows:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{8}} 8 \cos^{2}{\left(2 \theta \right)}\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{8}} 4\left(1+\cos\left(4\theta\right)\right)\,\mathrm d \theta \\
& = 4\left[\theta + \frac{\sin{\left(4 \theta \right)}}{4}\right]_{0}^{\frac{\pi}{8}} \\
& = 4\left(\left(\frac{\pi}{8}+\frac{1}{4}\sin\left(\frac{\pi}{2}\right)\right)-\left(0+\frac{1}{4}\sin\left(0\right)\right)\right) \\
& = 4\left(\left(\frac{\pi}{8}+\frac{1}{4} \left(1\right)\right)-\left(0+\frac{1}{4} \left(0\right)\right)\right) \\
& = 4\left(\left(\frac{\pi}{8}\right)+\frac{1}{4}\left(1\right)\right) \\
& = 1 + \frac{\pi}{2}
\end{aligned}
$$


---

### sine_double_partial — hard

Evaluate $\int_{0}^{\frac{\pi}{6}} \int_{0}^{\sin{\left(2 \theta \right)}} 2 r\,\mathrm d r\,\mathrm d \theta.$

- A. $- \frac{\sqrt{3}}{16} + \frac{\pi}{12}$ **correct**
- B. $\frac{5}{72}$
- C. $- \frac{\sqrt{3}}{32} + \frac{\pi}{24}$
- D. $- \frac{\sqrt{3}}{8} + \frac{\pi}{6}$
- E. $- \frac{\pi}{12} + \frac{\sqrt{3}}{16}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{6}} \int_{0}^{\sin{\left(2 \theta \right)}} 2 r\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{6}} 2 \int_{0}^{\sin{\left(2 \theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{6}} 2 \left[\frac{r^{2}}{2}\right]_{0}^{\sin{\left(2 \theta \right)}}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{6}} 2 \left(\frac{\left(\sin{\left(2 \theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{6}} \sin^{2}{\left(2 \theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we recall the double-angle formula

$$
\cos(2x)=1-2\sin^2 x.
$$

Substituting $x=2\theta$ and rearranging, we get

$$
\sin^2\left(2\theta\right)=\frac{1}{2}\left(1-\cos\left(4\theta\right)\right).
$$

Finally, we can finish our integral by integrating with respect to $\theta,$ as follows:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{6}} \sin^{2}{\left(2 \theta \right)}\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{6}} \frac{1}{2}\left(1-\cos\left(4\theta\right)\right)\,\mathrm d \theta \\
& = \frac{1}{2}\left[\theta - \frac{\sin{\left(4 \theta \right)}}{4}\right]_{0}^{\frac{\pi}{6}} \\
& = \frac{1}{2}\left(\left(\frac{\pi}{6}-\frac{1}{4}\sin\left(\frac{2 \pi}{3}\right)\right)-\left(0-\frac{1}{4}\sin\left(0\right)\right)\right) \\
& = \frac{1}{2}\left(\left(\frac{\pi}{6}-\frac{1}{4} \left(\frac{\sqrt{3}}{2}\right)\right)-\left(0-\frac{1}{4} \left(0\right)\right)\right) \\
& = \frac{1}{2}\left(\left(\frac{\pi}{6}\right)-\frac{1}{4}\left(\frac{\sqrt{3}}{2}\right)\right) \\
& = - \frac{\sqrt{3}}{16} + \frac{\pi}{12}
\end{aligned}
$$


---

### cosine_double_partial — hard

Evaluate $\int_{0}^{\frac{\pi}{12}} \int_{0}^{2 \cos{\left(2 \theta \right)}} 2 r\,\mathrm d r\,\mathrm d \theta.$

- A. $\frac{\sqrt{3}}{2} + \frac{\pi}{3}$
- B. $\frac{\sqrt{3}}{8} + \frac{\pi}{12}$
- C. $\frac{\sqrt{3}}{4} + \frac{\pi}{6}$ **correct**
- D. $- \frac{\pi}{6} - \frac{\sqrt{3}}{4}$
- E. $\frac{11}{9}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{12}} \int_{0}^{2 \cos{\left(2 \theta \right)}} 2 r\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{12}} 2 \int_{0}^{2 \cos{\left(2 \theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 2 \left[\frac{r^{2}}{2}\right]_{0}^{2 \cos{\left(2 \theta \right)}}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 2 \left(\frac{\left(2 \cos{\left(2 \theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 4 \cos^{2}{\left(2 \theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we recall the double-angle formula

$$
\cos(2x)=2\cos^2 x-1.
$$

Substituting $x=2\theta$ and rearranging, we get

$$
\cos^2\left(2\theta\right)=\frac{1}{2}\left(1+\cos\left(4\theta\right)\right).
$$

Finally, we can finish our integral by integrating with respect to $\theta,$ as follows:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{12}} 4 \cos^{2}{\left(2 \theta \right)}\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{12}} 2\left(1+\cos\left(4\theta\right)\right)\,\mathrm d \theta \\
& = 2\left[\theta + \frac{\sin{\left(4 \theta \right)}}{4}\right]_{0}^{\frac{\pi}{12}} \\
& = 2\left(\left(\frac{\pi}{12}+\frac{1}{4}\sin\left(\frac{\pi}{3}\right)\right)-\left(0+\frac{1}{4}\sin\left(0\right)\right)\right) \\
& = 2\left(\left(\frac{\pi}{12}+\frac{1}{4} \left(\frac{\sqrt{3}}{2}\right)\right)-\left(0+\frac{1}{4} \left(0\right)\right)\right) \\
& = 2\left(\left(\frac{\pi}{12}\right)+\frac{1}{4}\left(\frac{\sqrt{3}}{2}\right)\right) \\
& = \frac{\sqrt{3}}{4} + \frac{\pi}{6}
\end{aligned}
$$


---

### cosine_double_partial — hard

Evaluate $\int_{0}^{\frac{\pi}{6}} \int_{0}^{2 \cos{\left(2 \theta \right)}} 3 r\,\mathrm d r\,\mathrm d \theta.$

- A. $\frac{3 \sqrt{3}}{8} + \frac{\pi}{2}$ **correct**
- B. $\frac{3 \sqrt{3}}{4} + \pi$
- C. $\frac{3 \sqrt{3}}{2}$
- D. $\frac{3 \sqrt{3}}{16} + \frac{\pi}{4}$
- E. $- \frac{\pi}{2} - \frac{3 \sqrt{3}}{8}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{6}} \int_{0}^{2 \cos{\left(2 \theta \right)}} 3 r\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{6}} 3 \int_{0}^{2 \cos{\left(2 \theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{6}} 3 \left[\frac{r^{2}}{2}\right]_{0}^{2 \cos{\left(2 \theta \right)}}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{6}} 3 \left(\frac{\left(2 \cos{\left(2 \theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{6}} 6 \cos^{2}{\left(2 \theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we recall the double-angle formula

$$
\cos(2x)=2\cos^2 x-1.
$$

Substituting $x=2\theta$ and rearranging, we get

$$
\cos^2\left(2\theta\right)=\frac{1}{2}\left(1+\cos\left(4\theta\right)\right).
$$

Finally, we can finish our integral by integrating with respect to $\theta,$ as follows:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{6}} 6 \cos^{2}{\left(2 \theta \right)}\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{6}} 3\left(1+\cos\left(4\theta\right)\right)\,\mathrm d \theta \\
& = 3\left[\theta + \frac{\sin{\left(4 \theta \right)}}{4}\right]_{0}^{\frac{\pi}{6}} \\
& = 3\left(\left(\frac{\pi}{6}+\frac{1}{4}\sin\left(\frac{2 \pi}{3}\right)\right)-\left(0+\frac{1}{4}\sin\left(0\right)\right)\right) \\
& = 3\left(\left(\frac{\pi}{6}+\frac{1}{4} \left(\frac{\sqrt{3}}{2}\right)\right)-\left(0+\frac{1}{4} \left(0\right)\right)\right) \\
& = 3\left(\left(\frac{\pi}{6}\right)+\frac{1}{4}\left(\frac{\sqrt{3}}{2}\right)\right) \\
& = \frac{3 \sqrt{3}}{8} + \frac{\pi}{2}
\end{aligned}
$$


---

### cosine_double_partial — hard

Evaluate $\int_{0}^{\frac{\pi}{12}} \int_{0}^{2 \cos{\left(2 \theta \right)}} r\,\mathrm d r\,\mathrm d \theta.$

- A. $\frac{\sqrt{3}}{4} + \frac{\pi}{6}$
- B. $- \frac{\pi}{12} - \frac{\sqrt{3}}{8}$
- C. $\frac{\sqrt{3}}{16} + \frac{\pi}{24}$
- D. $\frac{\sqrt{3}}{8} + \frac{\pi}{12}$ **correct**
- E. $\frac{11}{18}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{12}} \int_{0}^{2 \cos{\left(2 \theta \right)}} r\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{12}} \left[\frac{r^{2}}{2}\right]_{0}^{2 \cos{\left(2 \theta \right)}}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} \left(\frac{\left(2 \cos{\left(2 \theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 2 \cos^{2}{\left(2 \theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we recall the double-angle formula

$$
\cos(2x)=2\cos^2 x-1.
$$

Substituting $x=2\theta$ and rearranging, we get

$$
\cos^2\left(2\theta\right)=\frac{1}{2}\left(1+\cos\left(4\theta\right)\right).
$$

Finally, we can finish our integral by integrating with respect to $\theta,$ as follows:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{12}} 2 \cos^{2}{\left(2 \theta \right)}\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{12}} 1\left(1+\cos\left(4\theta\right)\right)\,\mathrm d \theta \\
& = 1\left[\theta + \frac{\sin{\left(4 \theta \right)}}{4}\right]_{0}^{\frac{\pi}{12}} \\
& = 1\left(\left(\frac{\pi}{12}+\frac{1}{4}\sin\left(\frac{\pi}{3}\right)\right)-\left(0+\frac{1}{4}\sin\left(0\right)\right)\right) \\
& = 1\left(\left(\frac{\pi}{12}+\frac{1}{4} \left(\frac{\sqrt{3}}{2}\right)\right)-\left(0+\frac{1}{4} \left(0\right)\right)\right) \\
& = 1\left(\left(\frac{\pi}{12}\right)+\frac{1}{4}\left(\frac{\sqrt{3}}{2}\right)\right) \\
& = \frac{\sqrt{3}}{8} + \frac{\pi}{12}
\end{aligned}
$$
