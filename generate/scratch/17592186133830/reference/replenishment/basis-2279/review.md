Evaluate the line integral of the function $f(x,y)=- 2 x - 2 y$ along the curve $C$ parametrized by $r(t)=⟨- t,\,1 - t⟩$ for $t\in [0,3].$

1. $3 \sqrt{2}$
2. $12 \sqrt{2}$
3. $18 \sqrt{2}$
4. $12$
5. $24$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨- t,\,1 - t⟩,$ then along the curve we have $x=- t$ and $y=1 - t.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(- t)i+\frac{\text{d}}{\text{d}t}(1 - t)j \\ &=(-1)i+(-1)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(-1)^2+(-1)^2} \\ &=\sqrt{2} \\ &=\sqrt{2}\end{aligned}
$$

Now, if $f(x,y)=- 2 x - 2 y$, then we obtain

$$
\begin{aligned}f(r(t))&=(-2)\left(- t+(1 - t)\right) \\ &=4 t - 2\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - 2 x - 2 y\,\text{d}s&=\int_{0}^{3}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{0}^{3}(4 t - 2)\cdot (\sqrt{2})\,\text{d}t \\ &=(\sqrt{2})\int_{0}^{3}4 t - 2\,\text{d}t \\ &=\int_{0}^{3}4 \sqrt{2} t - 2 \sqrt{2}\,\text{d}t \\ &=(- 2 \sqrt{2})\left[- t^{2}+(t)\right]_{0}^{3} \\ &=\left[(2 \sqrt{2} t^{2})+(- 2 \sqrt{2} t)\right]_{0}^{3} \\ &=\left((2 \sqrt{2} (3)^{2})+(- 2 \sqrt{2} (3))\right)-\left((2 \sqrt{2} (0)^{2})+(- 2 \sqrt{2} (0))\right) \\ &=\left((18 \sqrt{2})+(- 6 \sqrt{2})\right)-\left((0)+(0)\right) \\ &=12 \sqrt{2}.\end{aligned}
$$

---

Evaluate the line integral of the function $f(x,y)=- \frac{3}{- x + y}$ along the curve $C$ parametrized by $r(t)=⟨3 t,\,3 t + 6⟩$ for $t\in [-2,2].$

1. $-36$
2. $- 6 \sqrt{2}$
3. $- 216 \sqrt{2}$
4. $6 \sqrt{2}$
5. $-2$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨3 t,\,3 t + 6⟩,$ then along the curve we have $x=3 t$ and $y=3 t + 6.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(3 t)i+\frac{\text{d}}{\text{d}t}(3 t + 6)j \\ &=(3)i+(3)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(3)^2+(3)^2} \\ &=\sqrt{18} \\ &=3 \sqrt{2}\end{aligned}
$$

Now, if $f(x,y)=- \frac{3}{- x + y}$, then we obtain

$$
\begin{aligned}f(r(t))&=\frac{-3}{(3 t + 6)-(3 t)} \\ &=\frac{-3}{6} \\ &=- \frac{1}{2}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - \frac{3}{- x + y}\,\text{d}s&=\int_{-2}^{2}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{-2}^{2}(- \frac{1}{2})\cdot (3 \sqrt{2})\,\text{d}t \\ &=(3 \sqrt{2})\int_{-2}^{2}- \frac{1}{2}\,\text{d}t \\ &=\int_{-2}^{2}- \frac{3 \sqrt{2}}{2}\,\text{d}t \\ &=(- \frac{3 \sqrt{2}}{2})\left[t\right]_{-2}^{2} \\ &=\left[(- \frac{3 \sqrt{2} t}{2})\right]_{-2}^{2} \\ &=\left((- \frac{3 \sqrt{2} (2)}{2})\right)-\left((- \frac{3 \sqrt{2} (-2)}{2})\right) \\ &=\left((- 3 \sqrt{2})\right)-\left((3 \sqrt{2})\right) \\ &=- 6 \sqrt{2}.\end{aligned}
$$

---

Evaluate the line integral of the function $f(x,y)=2 x + 2 y$ along the curve $C$ parametrized by $r(t)=⟨- 2 t,\,- 2 t - 2⟩$ for $t\in [-2,0].$

1. $8$
2. $32 \sqrt{2}$
3. $64$
4. $16 \sqrt{2}$
5. $0$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨- 2 t,\,- 2 t - 2⟩,$ then along the curve we have $x=- 2 t$ and $y=- 2 t - 2.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(- 2 t)i+\frac{\text{d}}{\text{d}t}(- 2 t - 2)j \\ &=(-2)i+(-2)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(-2)^2+(-2)^2} \\ &=\sqrt{8} \\ &=2 \sqrt{2}\end{aligned}
$$

Now, if $f(x,y)=2 x + 2 y$, then we obtain

$$
\begin{aligned}f(r(t))&=(2)\left(- 2 t+(- 2 t - 2)\right) \\ &=- 8 t - 4\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 2 x + 2 y\,\text{d}s&=\int_{-2}^{0}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{-2}^{0}(- 8 t - 4)\cdot (2 \sqrt{2})\,\text{d}t \\ &=(2 \sqrt{2})\int_{-2}^{0}- 8 t - 4\,\text{d}t \\ &=\int_{-2}^{0}- 16 \sqrt{2} t - 8 \sqrt{2}\,\text{d}t \\ &=(4 \sqrt{2})\left[- 2 t^{2}+(- 2 t)\right]_{-2}^{0} \\ &=\left[(- 8 \sqrt{2} t^{2})+(- 8 \sqrt{2} t)\right]_{-2}^{0} \\ &=\left((- 8 \sqrt{2} (0)^{2})+(- 8 \sqrt{2} (0))\right)-\left((- 8 \sqrt{2} (-2)^{2})+(- 8 \sqrt{2} (-2))\right) \\ &=\left((0)+(0)\right)-\left((- 32 \sqrt{2})+(16 \sqrt{2})\right) \\ &=16 \sqrt{2}.\end{aligned}
$$

---

Evaluate the line integral of the function $f(x,y)=9 - 2 x^{2}$ along the curve $C$ parametrized by $r(t)=⟨3 \cos{\left(t \right)},\,- 3 \sin{\left(t \right)}⟩$ for $t\in [- \frac{\pi}{2},- \frac{\pi}{4}].$

1. $\frac{27}{2} - \frac{27 \pi}{4}$
2. $\frac{27}{2}$
3. $27$
4. $\frac{9}{2}$
5. $\frac{81}{2}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨3 \cos{\left(t \right)},\,- 3 \sin{\left(t \right)}⟩,$ then along the curve we have $x=3 \cos{\left(t \right)}$ and $y=- 3 \sin{\left(t \right)}.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(3 \cos{\left(t \right)})i+\frac{\text{d}}{\text{d}t}(- 3 \sin{\left(t \right)})j \\ &=(- 3 \sin{\left(t \right)})i+(- 3 \cos{\left(t \right)})j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(- 3 \sin{\left(t \right)})^2+(- 3 \cos{\left(t \right)})^2} \\ &=\sqrt{9\sin^2t+9\cos^2t} \\ &=\sqrt{9(\sin^2t+\cos^2t)} \\ &=\sqrt{9} \\ &=3\end{aligned}
$$

Now, if $f(x,y)=9 - 2 x^{2}$, then we obtain

$$
\begin{aligned}f(r(t))&=(-1)\left(2(3 \cos{\left(t \right)})^2-9\right) \\ &=(-9)(2\cos^2t-1) \\ &=- 9 \cos{\left(2 t \right)}\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 9 - 2 x^{2}\,\text{d}s&=\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}}(- 9 \cos{\left(2 t \right)})\cdot (3)\,\text{d}t \\ &=\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}}- 27 \cos{\left(2 t \right)}\,\text{d}t \\ &=-27\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}}\cos 2t\,\text{d}t \\ &=(-27)\left[\frac{1}{2}\sin 2t\right]_{- \frac{\pi}{2}}^{- \frac{\pi}{4}} \\ &=\left[(- \frac{27 \sin{\left(2 t \right)}}{2})\right]_{- \frac{\pi}{2}}^{- \frac{\pi}{4}} \\ &=\left((- \frac{27 \sin{\left(2 (- \frac{\pi}{4}) \right)}}{2})\right)-\left((- \frac{27 \sin{\left(2 (- \frac{\pi}{2}) \right)}}{2})\right) \\ &=\left((\frac{27}{2})\right)-\left((0)\right) \\ &=\frac{27}{2}.\end{aligned}
$$

---

Evaluate the line integral of the function $f(x,y)=- y^{2}$ along the curve $C$ parametrized by $r(t)=⟨4 \cos{\left(t \right)},\,- 4 \sin{\left(t \right)}⟩$ for $t\in [- \frac{\pi}{4},0].$

1. $64 - 32 \pi$
2. $16 - 8 \pi$
3. $32 - 8 \pi$
4. $- 8 \pi - 16$
5. $4 - 2 \pi$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨4 \cos{\left(t \right)},\,- 4 \sin{\left(t \right)}⟩,$ then along the curve we have $x=4 \cos{\left(t \right)}$ and $y=- 4 \sin{\left(t \right)}.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(4 \cos{\left(t \right)})i+\frac{\text{d}}{\text{d}t}(- 4 \sin{\left(t \right)})j \\ &=(- 4 \sin{\left(t \right)})i+(- 4 \cos{\left(t \right)})j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(- 4 \sin{\left(t \right)})^2+(- 4 \cos{\left(t \right)})^2} \\ &=\sqrt{16\sin^2t+16\cos^2t} \\ &=\sqrt{16(\sin^2t+\cos^2t)} \\ &=\sqrt{16} \\ &=4\end{aligned}
$$

Now, if $f(x,y)=- y^{2}$, then we obtain

$$
\begin{aligned}f(r(t))&=(-1)(- 4 \sin{\left(t \right)})^2 \\ &=-16\sin^2t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - y^{2}\,\text{d}s&=\int_{- \frac{\pi}{4}}^{0}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{- \frac{\pi}{4}}^{0}(- 16 \sin^{2}{\left(t \right)})\cdot (4)\,\text{d}t \\ &=\int_{- \frac{\pi}{4}}^{0}- 64 \sin^{2}{\left(t \right)}\,\text{d}t \\ &=-64\int_{- \frac{\pi}{4}}^{0}\sin^2t\,\text{d}t \\ &=-64\int_{- \frac{\pi}{4}}^{0}\frac{1-\cos 2t}{2}\,\text{d}t \\ &=-32\int_{- \frac{\pi}{4}}^{0}1-\cos 2t\,\text{d}t \\ &=(-32)\left[t-\frac{\sin 2t}{2}\right]_{- \frac{\pi}{4}}^{0} \\ &=\left[(- 32 t)+(16 \sin{\left(2 t \right)})\right]_{- \frac{\pi}{4}}^{0} \\ &=\left((- 32 (0))+(16 \sin{\left(2 (0) \right)})\right)-\left((- 32 (- \frac{\pi}{4}))+(16 \sin{\left(2 (- \frac{\pi}{4}) \right)})\right) \\ &=\left((0)+(0)\right)-\left((8 \pi)+(-16)\right) \\ &=16 - 8 \pi.\end{aligned}
$$

---

Evaluate the line integral of the function $f(x,y)=x^{2} + y^{2} - 2$ along the curve $C$ parametrized by $r(t)=⟨2 t \sin{\left(t \right)} + 2 \cos{\left(t \right)},\,- 2 t \cos{\left(t \right)} + 2 \sin{\left(t \right)}⟩$ for $t\in [0,\pi].$

1. $2 \pi^{2}$
2. $2 \pi^{2} \left(1 + \pi^{2}\right)$
3. $2 \pi^{2} \left(2 + \pi^{2}\right)$
4. $2 \pi + \frac{4 \pi^{3}}{3}$
5. $\frac{8 \pi^{3} \left(5 + 6 \pi^{2}\right)}{15}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨2 t \sin{\left(t \right)} + 2 \cos{\left(t \right)},\,- 2 t \cos{\left(t \right)} + 2 \sin{\left(t \right)}⟩,$ then along the curve we have $x=2 t \sin{\left(t \right)} + 2 \cos{\left(t \right)}$ and $y=- 2 t \cos{\left(t \right)} + 2 \sin{\left(t \right)}.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(2 t \sin{\left(t \right)} + 2 \cos{\left(t \right)})i+\frac{\text{d}}{\text{d}t}(- 2 t \cos{\left(t \right)} + 2 \sin{\left(t \right)})j \\ &=(2)(-\sin t+\sin t+t\cos t)i+(2)(\cos t-\cos t+t\sin t)j \\ &=(2 t \cos{\left(t \right)})i+(2 t \sin{\left(t \right)})j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(2 t \cos{\left(t \right)})^2+(2 t \sin{\left(t \right)})^2} \\ &=\sqrt{4t^2(\cos^2t+\sin^2t)} \\ &=2|t| \\ &=2 t\end{aligned}
$$

Notice that $|t|=t$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=x^{2} + y^{2} - 2$, then we obtain

$$
\begin{aligned}f(r(t))&=(1)\left((2 t \sin{\left(t \right)} + 2 \cos{\left(t \right)})^2+(- 2 t \cos{\left(t \right)} + 2 \sin{\left(t \right)})^2\right)+(-2) \\ &=(4)\left(\cos^2t+2t\sin t\cos t+t^2\sin^2t+\sin^2t-2t\sin t\cos t+t^2\cos^2t\right)+(-2) \\ &=(4)(1+t^2)+(-2) \\ &=4 t^{2} + 2\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C x^{2} + y^{2} - 2\,\text{d}s&=\int_{0}^{\pi}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{0}^{\pi}(4 t^{2} + 2)\cdot (2 t)\,\text{d}t \\ &=\int_{0}^{\pi}8 t^{3} + 4 t\,\text{d}t \\ &=\left[(2 t^{2})+(2 t^{4})\right]_{0}^{\pi} \\ &=\left((2 (\pi)^{2})+(2 (\pi)^{4})\right)-\left((2 (0)^{2})+(2 (0)^{4})\right) \\ &=\left((2 \pi^{2})+(2 \pi^{4})\right)-\left((0)+(0)\right) \\ &=2 \pi^{2} \left(1 + \pi^{2}\right).\end{aligned}
$$

---

Evaluate the line integral of the function $f(x,y)=- x - 3 y$ along the curve $C$ parametrized by $r(t)=⟨\frac{16 t^{\frac{3}{2}}}{3},\,2 t^{2} - 4 t⟩$ for $t\in [0,2].$

1. $\frac{2688}{5} - \frac{784384 \sqrt{2}}{945}$
2. $64 - \frac{8704 \sqrt{2}}{105}$
3. $64$
4. $- \frac{8704 \sqrt{2}}{105}$
5. $8 - \frac{128 \sqrt{2}}{15}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨\frac{16 t^{\frac{3}{2}}}{3},\,2 t^{2} - 4 t⟩,$ then along the curve we have $x=\frac{16 t^{\frac{3}{2}}}{3}$ and $y=2 t^{2} - 4 t.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(\frac{16 t^{\frac{3}{2}}}{3})i+\frac{\text{d}}{\text{d}t}(2 t^{2} - 4 t)j \\ &=(8 \sqrt{t})i+(4 t - 4)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(8 \sqrt{t})^2+(4 t - 4)^2} \\ &=\sqrt{64t+16(t-1)^2} \\ &=\sqrt{16(t^2+2t+1)} \\ &=4|t+1| \\ &=4 t + 4\end{aligned}
$$

Notice that $|t+1|=t+1$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=- x - 3 y$, then we obtain

$$
\begin{aligned}f(r(t))&=(-1)(\frac{16 t^{\frac{3}{2}}}{3})+(-3)(2 t^{2} - 4 t) \\ &=- \frac{16 t^{\frac{3}{2}}}{3} - 6 t^{2} + 12 t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - x - 3 y\,\text{d}s&=\int_{0}^{2}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{0}^{2}(- \frac{16 t^{\frac{3}{2}}}{3} - 6 t^{2} + 12 t)\cdot (4 t + 4)\,\text{d}t \\ &=\int_{0}^{2}- \frac{64}{3}t^{3/2}(t+1)+(-48)(t^2/2-t)(t+1)\,\text{d}t \\ &=\int_{0}^{2}- \frac{64 t^{\frac{5}{2}}}{3} - \frac{64 t^{\frac{3}{2}}}{3} - 24 t^{3} + 24 t^{2} + 48 t\,\text{d}t \\ &=\left[(- \frac{128 t^{\frac{7}{2}}}{21})+(- \frac{128 t^{\frac{5}{2}}}{15})+(- 6 t^{4})+(8 t^{3})+(24 t^{2})\right]_{0}^{2} \\ &=\left((- \frac{128 (2)^{\frac{7}{2}}}{21})+(- \frac{128 (2)^{\frac{5}{2}}}{15})+(- 6 (2)^{4})+(8 (2)^{3})+(24 (2)^{2})\right)-\left((- \frac{128 (0)^{\frac{7}{2}}}{21})+(- \frac{128 (0)^{\frac{5}{2}}}{15})+(- 6 (0)^{4})+(8 (0)^{3})+(24 (0)^{2})\right) \\ &=\left((- \frac{1024 \sqrt{2}}{21})+(- \frac{512 \sqrt{2}}{15})+(-96)+(64)+(96)\right)-\left((0)+(0)+(0)+(0)+(0)\right) \\ &=64 - \frac{8704 \sqrt{2}}{105}.\end{aligned}
$$

---

Evaluate the line integral of the function $f(x,y)=2 x^{2} + 2 y^{2} - 3$ along the curve $C$ parametrized by $r(t)=⟨5 t \sin{\left(t \right)} + 5 \cos{\left(t \right)},\,- 5 t \cos{\left(t \right)} + 5 \sin{\left(t \right)}⟩$ for $t\in [1,3].$

1. $\frac{1582}{3}$
2. $6000$
3. $\frac{212050}{3}$
4. $5940$
5. $940$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨5 t \sin{\left(t \right)} + 5 \cos{\left(t \right)},\,- 5 t \cos{\left(t \right)} + 5 \sin{\left(t \right)}⟩,$ then along the curve we have $x=5 t \sin{\left(t \right)} + 5 \cos{\left(t \right)}$ and $y=- 5 t \cos{\left(t \right)} + 5 \sin{\left(t \right)}.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(5 t \sin{\left(t \right)} + 5 \cos{\left(t \right)})i+\frac{\text{d}}{\text{d}t}(- 5 t \cos{\left(t \right)} + 5 \sin{\left(t \right)})j \\ &=(5)(-\sin t+\sin t+t\cos t)i+(5)(\cos t-\cos t+t\sin t)j \\ &=(5 t \cos{\left(t \right)})i+(5 t \sin{\left(t \right)})j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(5 t \cos{\left(t \right)})^2+(5 t \sin{\left(t \right)})^2} \\ &=\sqrt{25t^2(\cos^2t+\sin^2t)} \\ &=5|t| \\ &=5 t\end{aligned}
$$

Notice that $|t|=t$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=2 x^{2} + 2 y^{2} - 3$, then we obtain

$$
\begin{aligned}f(r(t))&=(2)\left((5 t \sin{\left(t \right)} + 5 \cos{\left(t \right)})^2+(- 5 t \cos{\left(t \right)} + 5 \sin{\left(t \right)})^2\right)+(-3) \\ &=(50)\left(\cos^2t+2t\sin t\cos t+t^2\sin^2t+\sin^2t-2t\sin t\cos t+t^2\cos^2t\right)+(-3) \\ &=(50)(1+t^2)+(-3) \\ &=50 t^{2} + 47\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C 2 x^{2} + 2 y^{2} - 3\,\text{d}s&=\int_{1}^{3}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{1}^{3}(50 t^{2} + 47)\cdot (5 t)\,\text{d}t \\ &=\int_{1}^{3}250 t^{3} + 235 t\,\text{d}t \\ &=\left[(\frac{235 t^{2}}{2})+(\frac{125 t^{4}}{2})\right]_{1}^{3} \\ &=\left((\frac{235 (3)^{2}}{2})+(\frac{125 (3)^{4}}{2})\right)-\left((\frac{235 (1)^{2}}{2})+(\frac{125 (1)^{4}}{2})\right) \\ &=\left((\frac{2115}{2})+(\frac{10125}{2})\right)-\left((\frac{235}{2})+(\frac{125}{2})\right) \\ &=5940.\end{aligned}
$$

---

Evaluate the line integral of the function $f(x,y)=x + 2 y$ along the curve $C$ parametrized by $r(t)=⟨\frac{20 t^{\frac{3}{2}}}{3},\,\frac{5 t^{2}}{2} - 5 t⟩$ for $t\in [1,2].$

1. $- \frac{5245}{84} + \frac{2720 \sqrt{2}}{21}$
2. $-6 + \frac{32 \sqrt{2}}{3}$
3. $- \frac{475}{12}$
4. $- \frac{160}{7} + \frac{2720 \sqrt{2}}{21}$
5. $- \frac{127375}{189} + \frac{306400 \sqrt{2}}{189}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨\frac{20 t^{\frac{3}{2}}}{3},\,\frac{5 t^{2}}{2} - 5 t⟩,$ then along the curve we have $x=\frac{20 t^{\frac{3}{2}}}{3}$ and $y=\frac{5 t^{2}}{2} - 5 t.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(\frac{20 t^{\frac{3}{2}}}{3})i+\frac{\text{d}}{\text{d}t}(\frac{5 t^{2}}{2} - 5 t)j \\ &=(10 \sqrt{t})i+(5 t - 5)j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(10 \sqrt{t})^2+(5 t - 5)^2} \\ &=\sqrt{100t+25(t-1)^2} \\ &=\sqrt{25(t^2+2t+1)} \\ &=5|t+1| \\ &=5 t + 5\end{aligned}
$$

Notice that $|t+1|=t+1$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=x + 2 y$, then we obtain

$$
\begin{aligned}f(r(t))&=(1)(\frac{20 t^{\frac{3}{2}}}{3})+(2)(\frac{5 t^{2}}{2} - 5 t) \\ &=\frac{20 t^{\frac{3}{2}}}{3} + 5 t^{2} - 10 t\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C x + 2 y\,\text{d}s&=\int_{1}^{2}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{1}^{2}(\frac{20 t^{\frac{3}{2}}}{3} + 5 t^{2} - 10 t)\cdot (5 t + 5)\,\text{d}t \\ &=\int_{1}^{2}\frac{100}{3}t^{3/2}(t+1)+(50)(t^2/2-t)(t+1)\,\text{d}t \\ &=\int_{1}^{2}\frac{100 t^{\frac{5}{2}}}{3} + \frac{100 t^{\frac{3}{2}}}{3} + 25 t^{3} - 25 t^{2} - 50 t\,\text{d}t \\ &=\left[(\frac{200 t^{\frac{7}{2}}}{21})+(\frac{40 t^{\frac{5}{2}}}{3})+(\frac{25 t^{4}}{4})+(- \frac{25 t^{3}}{3})+(- 25 t^{2})\right]_{1}^{2} \\ &=\left((\frac{200 (2)^{\frac{7}{2}}}{21})+(\frac{40 (2)^{\frac{5}{2}}}{3})+(\frac{25 (2)^{4}}{4})+(- \frac{25 (2)^{3}}{3})+(- 25 (2)^{2})\right)-\left((\frac{200 (1)^{\frac{7}{2}}}{21})+(\frac{40 (1)^{\frac{5}{2}}}{3})+(\frac{25 (1)^{4}}{4})+(- \frac{25 (1)^{3}}{3})+(- 25 (1)^{2})\right) \\ &=\left((\frac{1600 \sqrt{2}}{21})+(\frac{160 \sqrt{2}}{3})+(100)+(- \frac{200}{3})+(-100)\right)-\left((\frac{200}{21})+(\frac{40}{3})+(\frac{25}{4})+(- \frac{25}{3})+(-25)\right) \\ &=- \frac{5245}{84} + \frac{2720 \sqrt{2}}{21}.\end{aligned}
$$

---

Evaluate the line integral of the function $f(x,y)=- 2 x^{2} - 2 y^{2} - 2$ along the curve $C$ parametrized by $r(t)=⟨4 t \sin{\left(t \right)} + 4 \cos{\left(t \right)},\,- 4 t \cos{\left(t \right)} + 4 \sin{\left(t \right)}⟩$ for $t\in [0,\pi].$

1. $- \frac{32 \pi^{3}}{3} - 34 \pi$
2. $- 68 \pi^{2}$
3. $\pi^{2} \left(- 32 \pi^{2} - 68\right)$
4. $32 \pi^{2} \left(- \pi^{2} - 2\right)$
5. $\frac{32 \pi^{3} \left(- 48 \pi^{2} - 85\right)}{15}$

To calculate the line integral, we will use the formula

$$
\int_C f(x,y)\,\text{d}s=\int_a^b f(r(t))\,\|r^{\prime}(t)\|\,\text{d}t.
$$

Since $r(t)=⟨4 t \sin{\left(t \right)} + 4 \cos{\left(t \right)},\,- 4 t \cos{\left(t \right)} + 4 \sin{\left(t \right)}⟩,$ then along the curve we have $x=4 t \sin{\left(t \right)} + 4 \cos{\left(t \right)}$ and $y=- 4 t \cos{\left(t \right)} + 4 \sin{\left(t \right)}.$

Computing $r^{\prime}(t)$ and $\|r^{\prime}(t)\|,$ we get the following:

$$
\begin{aligned}r^{\prime}(t)&=\frac{\text{d}x}{\text{d}t}i+\frac{\text{d}y}{\text{d}t}j \\ &=\frac{\text{d}}{\text{d}t}(4 t \sin{\left(t \right)} + 4 \cos{\left(t \right)})i+\frac{\text{d}}{\text{d}t}(- 4 t \cos{\left(t \right)} + 4 \sin{\left(t \right)})j \\ &=(4)(-\sin t+\sin t+t\cos t)i+(4)(\cos t-\cos t+t\sin t)j \\ &=(4 t \cos{\left(t \right)})i+(4 t \sin{\left(t \right)})j \\ \|r^{\prime}(t)\|&=\sqrt{(\frac{\text{d}x}{\text{d}t})^2+(\frac{\text{d}y}{\text{d}t})^2} \\ &=\sqrt{(4 t \cos{\left(t \right)})^2+(4 t \sin{\left(t \right)})^2} \\ &=\sqrt{16t^2(\cos^2t+\sin^2t)} \\ &=4|t| \\ &=4 t\end{aligned}
$$

Notice that $|t|=t$ since $t\geq0$ along the path of $C.$

Now, if $f(x,y)=- 2 x^{2} - 2 y^{2} - 2$, then we obtain

$$
\begin{aligned}f(r(t))&=(-2)\left((4 t \sin{\left(t \right)} + 4 \cos{\left(t \right)})^2+(- 4 t \cos{\left(t \right)} + 4 \sin{\left(t \right)})^2\right)+(-2) \\ &=(-32)\left(\cos^2t+2t\sin t\cos t+t^2\sin^2t+\sin^2t-2t\sin t\cos t+t^2\cos^2t\right)+(-2) \\ &=(-32)(1+t^2)+(-2) \\ &=- 32 t^{2} - 34\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C - 2 x^{2} - 2 y^{2} - 2\,\text{d}s&=\int_{0}^{\pi}f(r(t))\|r^{\prime}(t)\|\,\text{d}t \\ &=\int_{0}^{\pi}(- 32 t^{2} - 34)\cdot (4 t)\,\text{d}t \\ &=\int_{0}^{\pi}- 128 t^{3} - 136 t\,\text{d}t \\ &=\left[(- 68 t^{2})+(- 32 t^{4})\right]_{0}^{\pi} \\ &=\left((- 68 (\pi)^{2})+(- 32 (\pi)^{4})\right)-\left((- 68 (0)^{2})+(- 32 (0)^{4})\right) \\ &=\left((- 68 \pi^{2})+(- 32 \pi^{4})\right)-\left((0)+(0)\right) \\ &=\pi^{2} \left(- 32 \pi^{2} - 68\right).\end{aligned}
$$
