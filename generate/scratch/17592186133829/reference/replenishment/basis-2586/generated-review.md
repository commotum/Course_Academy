# Committed scalar line-integral setup batch

## easy / parabola / a17cfaab-14e7-5c09-ade5-3176e170f53b

Which of the following is equivalent to the integral ${\int }_{C}5\left(\frac{x}{4y+1}\right)\text{d}s,$ where the curve $C$ is parametrized by $r(t)=t\,i+{t}^{2}\,j\,$ for $\frac{1}{2}\le t\le \frac{7}{3}?$

1. $\int_{\frac{1}{2}}^{\frac{7}{3}}\frac{5 t}{\sqrt{4 t^{2} + 1}}\,\mathrm{d}t$
2. $\int_{\frac{1}{2}}^{\frac{7}{3}}\frac{5 t}{4 t^{2} + 1}\,\mathrm{d}t$
3. $\int_{\frac{1}{2}}^{\frac{7}{3}}5 t\,\mathrm{d}t$
4. $\int_{\frac{1}{2}}^{\frac{7}{3}}\frac{5 t^{2}}{\sqrt{4 t^{2} + 1}}\,\mathrm{d}t$
5. $\int_{\frac{1}{2}}^{\frac{7}{3}}\frac{5 t}{\left(4 t^{2} + 1\right)^{\frac{3}{2}}}\,\mathrm{d}t$

Since $r(t)=t\,i+{t}^{2}\,j,$ then along the curve we have $x=t$ and $y={t}^{2}.$ 

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{2})j \\  & =i+2tj \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(2t)^{2}} \\  & =\sqrt{1+4{t}^{2}}\end{aligned}
$$

 

Now, if  $f(x,y)=5\left(\frac{x}{4y+1}\right)$, then we obtain 

$$
\begin{aligned}f(r(t)) & =5\left(\frac{t}{4{t}^{2}+1}\right).\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}5\left(\frac{x}{4y+1}\right)\text{d}s & ={\int }_{\frac{1}{2}}^{\frac{7}{3}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t  \\    & =5\left({\int }_{\frac{1}{2}}^{\frac{7}{3}}(\frac{t}{4{t}^{2}+1})\cdot \sqrt{4{t}^{2}+1}\cdot \text{d}t\right) \\    & =5\left({\int }_{\frac{1}{2}}^{\frac{7}{3}}\frac{t}{\sqrt{4{t}^{2}+1}}\text{d}t\right).\end{aligned}
$$

---

## easy / parabola / 86c6a686-849e-56ac-8cd5-66fc10eebbef

Which of the following is equivalent to the integral ${\int }_{C}2\left(\frac{x}{4y+1}\right)\text{d}s,$ where the curve $C$ is parametrized by $r(t)=t\,i+{t}^{2}\,j\,$ for $2\le t\le \frac{11}{2}?$

1. $\int_{2}^{\frac{11}{2}}\frac{2 t^{2}}{\sqrt{4 t^{2} + 1}}\,\mathrm{d}t$
2. $\int_{2}^{\frac{11}{2}}\frac{2 t}{\sqrt{4 t^{2} + 1}}\,\mathrm{d}t$
3. $\int_{2}^{\frac{11}{2}}2 t\,\mathrm{d}t$
4. $\int_{2}^{\frac{11}{2}}\frac{2 t}{\left(4 t^{2} + 1\right)^{\frac{3}{2}}}\,\mathrm{d}t$
5. $\int_{2}^{\frac{11}{2}}\frac{2 t}{4 t^{2} + 1}\,\mathrm{d}t$

Since $r(t)=t\,i+{t}^{2}\,j,$ then along the curve we have $x=t$ and $y={t}^{2}.$ 

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{2})j \\  & =i+2tj \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(2t)^{2}} \\  & =\sqrt{1+4{t}^{2}}\end{aligned}
$$

 

Now, if  $f(x,y)=2\left(\frac{x}{4y+1}\right)$, then we obtain 

$$
\begin{aligned}f(r(t)) & =2\left(\frac{t}{4{t}^{2}+1}\right).\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}2\left(\frac{x}{4y+1}\right)\text{d}s & ={\int }_{2}^{\frac{11}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t  \\    & =2\left({\int }_{2}^{\frac{11}{2}}(\frac{t}{4{t}^{2}+1})\cdot \sqrt{4{t}^{2}+1}\cdot \text{d}t\right) \\    & =2\left({\int }_{2}^{\frac{11}{2}}\frac{t}{\sqrt{4{t}^{2}+1}}\text{d}t\right).\end{aligned}
$$

---

## easy / parabola / f04c0a98-4a6c-5873-883f-948e18d8b72b

Which of the following is equivalent to the integral ${\int }_{C}\frac{x}{4y+1}\text{d}s,$ where the curve $C$ is parametrized by $r(t)=t\,i+{t}^{2}\,j\,$ for $1\le t\le \frac{4}{3}?$

1. $\int_{1}^{\frac{4}{3}}\frac{t}{4 t^{2} + 1}\,\mathrm{d}t$
2. $\int_{1}^{\frac{4}{3}}t\,\mathrm{d}t$
3. $\int_{1}^{\frac{4}{3}}\frac{t^{2}}{\sqrt{4 t^{2} + 1}}\,\mathrm{d}t$
4. $\int_{1}^{\frac{4}{3}}\frac{t}{\left(4 t^{2} + 1\right)^{\frac{3}{2}}}\,\mathrm{d}t$
5. $\int_{1}^{\frac{4}{3}}\frac{t}{\sqrt{4 t^{2} + 1}}\,\mathrm{d}t$

Since $r(t)=t\,i+{t}^{2}\,j,$ then along the curve we have $x=t$ and $y={t}^{2}.$ 

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{2})j \\  & =i+2tj \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(2t)^{2}} \\  & =\sqrt{1+4{t}^{2}}\end{aligned}
$$

 

Now, if  $f(x,y)=\frac{x}{4y+1}$, then we obtain 

$$
\begin{aligned}f(r(t)) & =\frac{t}{4{t}^{2}+1}.\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}\frac{x}{4y+1}\text{d}s & ={\int }_{1}^{\frac{4}{3}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{\frac{4}{3}}(\frac{t}{4{t}^{2}+1})\cdot \sqrt{4{t}^{2}+1}\cdot \text{d}t \\  & ={\int }_{1}^{\frac{4}{3}}\frac{t}{\sqrt{4{t}^{2}+1}}\text{d}t.\end{aligned}
$$

---

## easy / parabola / 629bb41a-481a-5fce-89d8-1176b4e371da

Which of the following is equivalent to the integral ${\int }_{C}2\left(\frac{x}{4y+1}\right)\text{d}s,$ where the curve $C$ is parametrized by $r(t)=t\,i+{t}^{2}\,j\,$ for $0\le t\le 5?$

1. $\int_{0}^{5}2 t\,\mathrm{d}t$
2. $\int_{0}^{5}\frac{2 t}{\left(4 t^{2} + 1\right)^{\frac{3}{2}}}\,\mathrm{d}t$
3. $\int_{0}^{5}\frac{2 t}{\sqrt{4 t^{2} + 1}}\,\mathrm{d}t$
4. $\int_{0}^{5}\frac{2 t}{4 t^{2} + 1}\,\mathrm{d}t$
5. $\int_{0}^{5}\frac{2 t^{2}}{\sqrt{4 t^{2} + 1}}\,\mathrm{d}t$

Since $r(t)=t\,i+{t}^{2}\,j,$ then along the curve we have $x=t$ and $y={t}^{2}.$ 

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j \\  & =\frac{\text{d}}{\text{d}t}(t)i+\frac{\text{d}}{\text{d}t}({t}^{2})j \\  & =i+2tj \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}} \\  & =\sqrt{{1}^{2}+(2t)^{2}} \\  & =\sqrt{1+4{t}^{2}}\end{aligned}
$$

 

Now, if  $f(x,y)=2\left(\frac{x}{4y+1}\right)$, then we obtain 

$$
\begin{aligned}f(r(t)) & =2\left(\frac{t}{4{t}^{2}+1}\right).\end{aligned}
$$

Therefore, we can write the integral as 

$$
\begin{aligned}{\int }_{C}2\left(\frac{x}{4y+1}\right)\text{d}s & ={\int }_{0}^{5}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t  \\    & =2\left({\int }_{0}^{5}(\frac{t}{4{t}^{2}+1})\cdot \sqrt{4{t}^{2}+1}\cdot \text{d}t\right) \\    & =2\left({\int }_{0}^{5}\frac{t}{\sqrt{4{t}^{2}+1}}\text{d}t\right).\end{aligned}
$$

---

## moderate / helix / 88d1c090-6bb7-523f-a9f3-d7ec7807cd7a

Which of the following is equivalent to the integral ${\int }_{C}5\left(z({x}^{2}-{y}^{2})\right)\,\text{d}s,$ where the curve $C$ is parametrized by $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j\,+t\,k$ for $\,0\le t\le \frac{\pi}{6}?$

1. $\int_{0}^{\frac{\pi}{6}}5 \sqrt{2} t \cos{\left(2 t \right)}\,\mathrm{d}t$
2. $\int_{0}^{\frac{\pi}{6}}5 t \cos{\left(2 t \right)}\,\mathrm{d}t$
3. $\int_{0}^{\frac{\pi}{6}}10 t \cos{\left(2 t \right)}\,\mathrm{d}t$
4. $\int_{0}^{\frac{\pi}{6}}5 \sqrt{2} t\,\mathrm{d}t$
5. $\int_{0}^{\frac{\pi}{6}}\frac{5 \sqrt{2} t \cos{\left(2 t \right)}}{2}\,\mathrm{d}t$

Since $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j\,+t\,k,$ then along the curve we have $x=\operatorname{cos}⁡t,$ $y=\operatorname{sin}⁡t,$ and $z=t.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)j+\frac{\text{d}}{\text{d}t}(t)k \\  & =-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{(-\operatorname{sin}⁡t)^{2}+(\operatorname{cos}⁡t)^{2}+{1}^{2}} \\  & =\sqrt{{sin}^{2}⁡t+{cos}^{2}⁡t+1} \\  & =\sqrt{1+1} \\  & =\sqrt{2}\end{aligned}
$$

  

Now, if $f(x,y,z)=5\left(z({x}^{2}-{y}^{2})\right)$, then we obtain

$$
\begin{aligned}f(r(t)) & =5\left(t((\operatorname{cos}⁡t)^{2}-(\operatorname{sin}⁡t)^{2})\right) \\    & =5\left(t({cos}^{2}⁡t-{sin}^{2}⁡t)\right) \\    & =5\left(t\operatorname{cos}⁡2t\right).\end{aligned}
$$

Therefore, we can write the integral as  

$$
\begin{aligned}{\int }_{C}5\left(z({x}^{2}-{y}^{2})\right)\,\text{d}s & ={\int }_{0}^{\frac{\pi}{6}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t  \\    & =5\left({\int }_{0}^{\frac{\pi}{6}}t\operatorname{cos}⁡2t\cdot \sqrt{2}\cdot \text{d}t\right) \\    & =5\left(\sqrt{2}{\int }_{0}^{\frac{\pi}{6}}t\operatorname{cos}⁡2t\,\text{d}t\right).\end{aligned}
$$

---

## moderate / linear_cubic / f515b153-b2d5-5f07-b698-2b223e35049e

Which of the following is equivalent to the integral $\displaystyle \int_C2\left((x^{3} - y)\right)ds$, where the curve $C$ is parametrized by $r(t) = 2ti + (2 - t)j$ for $- \frac{3}{2}\le t\le 2$?

1. $\int_{- \frac{3}{2}}^{2}2 \sqrt{5} \left(8 t^{3} - t + 2\right)\,\mathrm{d}t$
2. $\int_{- \frac{3}{2}}^{2}2 \sqrt{5} \left(8 t^{3} + t - 2\right)\,\mathrm{d}t$.
3. $\int_{- \frac{3}{2}}^{2}80 t^{3} + 10 t - 20\,\mathrm{d}t$
4. $\int_{- \frac{3}{2}}^{2}\frac{2 \sqrt{5} \left(8 t^{3} + t - 2\right)}{5}\,\mathrm{d}t$
5. $\int_{- \frac{3}{2}}^{2}16 t^{3} + 2 t - 4\,\mathrm{d}t$

Since $r(t)=\langle 2 t, 2 - t\rangle,$ then along the curve we have $x=2 t$, $y=2 - t$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j \\ &= \frac{\mathrm{d}}{\mathrm{d}t}(2 t)i+\frac{\mathrm{d}}{\mathrm{d}t}(2 - t)j \\ &= (2)\,i+(-1)\,j \\ \|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2} \\ &= \sqrt{(2)^2+(-1)^2} \\ &= \sqrt{5}\end{aligned}
$$

Now, since $f(x,y)=2 x^{3} - 2 y$, we obtain

$$
\begin{aligned}f(r(t))&=2\left((2 t)^3-(2 - t)\right) \\ &= 2\left(8t^3-2+t\right) \\ &= 16 t^{3} + 2 t - 4.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y)\,\mathrm{d}s&=\int_{- \frac{3}{2}}^{2} f(r(t))\,\|r'(t)\|\,\mathrm{d}t \\ &= \int_{- \frac{3}{2}}^{2}(16 t^{3} + 2 t - 4)(\sqrt{5})\,\mathrm{d}t \\ &= \int_{- \frac{3}{2}}^{2}2 \sqrt{5} \left(8 t^{3} + t - 2\right)\,\mathrm{d}t.\end{aligned}
$$

---

## moderate / helix / 77c0932d-edde-5a3d-a95b-c9e88ef0198f

Which of the following is equivalent to the integral ${\int }_{C}z({x}^{2}-{y}^{2})\,\text{d}s,$ where the curve $C$ is parametrized by $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j\,+t\,k$ for $\,\frac{\pi}{12}\le t\le \frac{\pi}{2}?$

1. $\int_{\frac{\pi}{12}}^{\frac{\pi}{2}}t \cos{\left(2 t \right)}\,\mathrm{d}t$
2. $\int_{\frac{\pi}{12}}^{\frac{\pi}{2}}2 t \cos{\left(2 t \right)}\,\mathrm{d}t$
3. $\int_{\frac{\pi}{12}}^{\frac{\pi}{2}}\sqrt{2} t\,\mathrm{d}t$
4. $\int_{\frac{\pi}{12}}^{\frac{\pi}{2}}\frac{\sqrt{2} t \cos{\left(2 t \right)}}{2}\,\mathrm{d}t$
5. $\int_{\frac{\pi}{12}}^{\frac{\pi}{2}}\sqrt{2} t \cos{\left(2 t \right)}\,\mathrm{d}t$

Since $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j\,+t\,k,$ then along the curve we have $x=\operatorname{cos}⁡t,$ $y=\operatorname{sin}⁡t,$ and $z=t.$

Computing ${r}^{′}(t)$ and $‖{r}^{′}(t)‖,$ we get the following:

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}x}{\text{d}t}\,i+\frac{\text{d}y}{\text{d}t}\,j+\frac{\text{d}z}{\text{d}t}\,k \\  & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)j+\frac{\text{d}}{\text{d}t}(t)k \\  & =-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+k \\ ‖{r}^{′}(t)‖ & =\sqrt{{(\frac{\text{d}x}{\text{d}t})}^{2}+{(\frac{\text{d}y}{\text{d}t})}^{2}+{(\frac{\text{d}z}{\text{d}t})}^{2}} \\  & =\sqrt{(-\operatorname{sin}⁡t)^{2}+(\operatorname{cos}⁡t)^{2}+{1}^{2}} \\  & =\sqrt{{sin}^{2}⁡t+{cos}^{2}⁡t+1} \\  & =\sqrt{1+1} \\  & =\sqrt{2}\end{aligned}
$$

  

Now, if $f(x,y,z)=z({x}^{2}-{y}^{2})$, then we obtain

$$
\begin{aligned}f(r(t)) & =t((\operatorname{cos}⁡t)^{2}-(\operatorname{sin}⁡t)^{2}) \\  & =t({cos}^{2}⁡t-{sin}^{2}⁡t) \\  & =t\operatorname{cos}⁡2t.\end{aligned}
$$

Therefore, we can write the integral as  

$$
\begin{aligned}{\int }_{C}z({x}^{2}-{y}^{2})\,\text{d}s & ={\int }_{\frac{\pi}{12}}^{\frac{\pi}{2}}f(r(t))\,‖{r}^{′}(t)‖\,\text{d}t \\  & ={\int }_{\frac{\pi}{12}}^{\frac{\pi}{2}}t\operatorname{cos}⁡2t\cdot \sqrt{2}\cdot \text{d}t \\  & =\sqrt{2}{\int }_{\frac{\pi}{12}}^{\frac{\pi}{2}}t\operatorname{cos}⁡2t\,\text{d}t.\end{aligned}
$$

---

## hard / hard_product_square / 021666da-2b39-563b-b7fb-5efa8b86fda8

Which of the following is equivalent to $\int_C 3 x y - 3 z^{2}\,\mathrm{d}s,$ where the curve $C$ is parametrized by $r(t)=\langle t^{2}, 2 t + 1, 3 t + 1\rangle$ for $\frac{1}{2}\le t\le \frac{3}{2}$?

1. $\int_{\frac{1}{2}}^{\frac{3}{2}}\frac{3 \left(2 t^{3} - 8 t^{2} - 6 t - 1\right)}{\sqrt{4 t^{2} + 13}}\,\mathrm{d}t$
2. $\int_{\frac{1}{2}}^{\frac{3}{2}}3 \sqrt{4 t^{2} + 13} \left(t^{2} \left(2 t + 1\right) + \left(3 t + 1\right)^{2}\right)\,\mathrm{d}t$
3. $\int_{\frac{1}{2}}^{\frac{3}{2}}6 t^{3} - 24 t^{2} - 18 t - 3\,\mathrm{d}t$
4. $\int_{\frac{1}{2}}^{\frac{3}{2}}- 3 \left(4 t^{2} + 13\right) \left(- 2 t^{3} + 8 t^{2} + 6 t + 1\right)\,\mathrm{d}t$
5. $\int_{\frac{1}{2}}^{\frac{3}{2}}\sqrt{4 t^{2} + 13} \left(6 t^{3} - 24 t^{2} - 18 t - 3\right)\,\mathrm{d}t$

Since $r(t)=\langle t^{2}, 2 t + 1, 3 t + 1\rangle,$ then along the curve we have $x=t^{2}$, $y=2 t + 1$, $z=3 t + 1$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ &= \frac{\mathrm{d}}{\mathrm{d}t}(t^{2})i+\frac{\mathrm{d}}{\mathrm{d}t}(2 t + 1)j+\frac{\mathrm{d}}{\mathrm{d}t}(3 t + 1)k \\ &= (2 t)\,i+(2)\,j+(3)\,k \\ \|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2+(\frac{\mathrm{d}z}{\mathrm{d}t})^2} \\ &= \sqrt{(2 t)^2+(2)^2+(3)^2} \\ &= \sqrt{4 t^{2} + 13}\end{aligned}
$$

Now, since $f(x,y,z)=3 x y - 3 z^{2}$, we obtain

$$
\begin{aligned}f(r(t))&=3\left((t^{2})(2 t + 1)-(3 t + 1)^2\right) \\ &= 3\left(2t^3+(1)t^2-\left(9t^2+(6)t+1\right)\right) \\ &= 6 t^{3} - 24 t^{2} - 18 t - 3.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y,z)\,\mathrm{d}s&=\int_{\frac{1}{2}}^{\frac{3}{2}} f(r(t))\,\|r'(t)\|\,\mathrm{d}t \\ &= \int_{\frac{1}{2}}^{\frac{3}{2}}(6 t^{3} - 24 t^{2} - 18 t - 3)(\sqrt{4 t^{2} + 13})\,\mathrm{d}t \\ &= \int_{\frac{1}{2}}^{\frac{3}{2}}\sqrt{4 t^{2} + 13} \left(6 t^{3} - 24 t^{2} - 18 t - 3\right)\,\mathrm{d}t.\end{aligned}
$$

---

## hard / hard_product_square / fcd80b68-90ad-5381-82bb-4a395bb5f45b

Which of the following is equivalent to $\int_C 3 x y - 3 z^{2}\,\mathrm{d}s,$ where the curve $C$ is parametrized by $r(t)=\langle 2 t^{2}, 2 t + 1, t + 3\rangle$ for $1\le t\le \frac{3}{2}$?

1. $\int_{1}^{\frac{3}{2}}3 \sqrt{16 t^{2} + 5} \left(4 t^{3} + t^{2} - 6 t - 9\right)\,\mathrm{d}t$
2. $\int_{1}^{\frac{3}{2}}12 t^{3} + 3 t^{2} - 18 t - 27\,\mathrm{d}t$
3. $\int_{1}^{\frac{3}{2}}\frac{3 \left(4 t^{3} + t^{2} - 6 t - 9\right)}{\sqrt{16 t^{2} + 5}}\,\mathrm{d}t$
4. $\int_{1}^{\frac{3}{2}}3 \sqrt{16 t^{2} + 5} \left(2 t^{2} \left(2 t + 1\right) + \left(t + 3\right)^{2}\right)\,\mathrm{d}t$
5. $\int_{1}^{\frac{3}{2}}3 \left(16 t^{2} + 5\right) \left(4 t^{3} + t^{2} - 6 t - 9\right)\,\mathrm{d}t$

Since $r(t)=\langle 2 t^{2}, 2 t + 1, t + 3\rangle,$ then along the curve we have $x=2 t^{2}$, $y=2 t + 1$, $z=t + 3$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ &= \frac{\mathrm{d}}{\mathrm{d}t}(2 t^{2})i+\frac{\mathrm{d}}{\mathrm{d}t}(2 t + 1)j+\frac{\mathrm{d}}{\mathrm{d}t}(t + 3)k \\ &= (4 t)\,i+(2)\,j+(1)\,k \\ \|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2+(\frac{\mathrm{d}z}{\mathrm{d}t})^2} \\ &= \sqrt{(4 t)^2+(2)^2+(1)^2} \\ &= \sqrt{16 t^{2} + 5}\end{aligned}
$$

Now, since $f(x,y,z)=3 x y - 3 z^{2}$, we obtain

$$
\begin{aligned}f(r(t))&=3\left((2 t^{2})(2 t + 1)-(t + 3)^2\right) \\ &= 3\left(4t^3+(2)t^2-\left(1t^2+(6)t+9\right)\right) \\ &= 12 t^{3} + 3 t^{2} - 18 t - 27.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y,z)\,\mathrm{d}s&=\int_{1}^{\frac{3}{2}} f(r(t))\,\|r'(t)\|\,\mathrm{d}t \\ &= \int_{1}^{\frac{3}{2}}(12 t^{3} + 3 t^{2} - 18 t - 27)(\sqrt{16 t^{2} + 5})\,\mathrm{d}t \\ &= \int_{1}^{\frac{3}{2}}3 \sqrt{16 t^{2} + 5} \left(4 t^{3} + t^{2} - 6 t - 9\right)\,\mathrm{d}t.\end{aligned}
$$

---

## hard / hard_product_square / 19471cdf-9ea5-5c33-ad36-e0767c3ac883

Which of the following is equivalent to $\int_C - 2 x y + 2 z^{2}\,\mathrm{d}s,$ where the curve $C$ is parametrized by $r(t)=\langle t^{2}, t - 3, 2 t + 1\rangle$ for $1\le t\le \frac{3}{2}$?

1. $\int_{1}^{\frac{3}{2}}2 \sqrt{4 t^{2} + 5} \left(- t^{3} + 7 t^{2} + 4 t + 1\right)\,\mathrm{d}t$
2. $\int_{1}^{\frac{3}{2}}2 \left(4 t^{2} + 5\right) \left(- t^{3} + 7 t^{2} + 4 t + 1\right)\,\mathrm{d}t$
3. $\int_{1}^{\frac{3}{2}}2 \sqrt{4 t^{2} + 5} \left(- t^{3} - t^{2} - 4 t - 1\right)\,\mathrm{d}t$
4. $\int_{1}^{\frac{3}{2}}- 2 t^{3} + 14 t^{2} + 8 t + 2\,\mathrm{d}t$
5. $\int_{1}^{\frac{3}{2}}\frac{2 \left(- t^{3} + 7 t^{2} + 4 t + 1\right)}{\sqrt{4 t^{2} + 5}}\,\mathrm{d}t$

Since $r(t)=\langle t^{2}, t - 3, 2 t + 1\rangle,$ then along the curve we have $x=t^{2}$, $y=t - 3$, $z=2 t + 1$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ &= \frac{\mathrm{d}}{\mathrm{d}t}(t^{2})i+\frac{\mathrm{d}}{\mathrm{d}t}(t - 3)j+\frac{\mathrm{d}}{\mathrm{d}t}(2 t + 1)k \\ &= (2 t)\,i+(1)\,j+(2)\,k \\ \|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2+(\frac{\mathrm{d}z}{\mathrm{d}t})^2} \\ &= \sqrt{(2 t)^2+(1)^2+(2)^2} \\ &= \sqrt{4 t^{2} + 5}\end{aligned}
$$

Now, since $f(x,y,z)=- 2 x y + 2 z^{2}$, we obtain

$$
\begin{aligned}f(r(t))&=-2\left((t^{2})(t - 3)-(2 t + 1)^2\right) \\ &= -2\left(1t^3+(-3)t^2-\left(4t^2+(4)t+1\right)\right) \\ &= - 2 t^{3} + 14 t^{2} + 8 t + 2.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y,z)\,\mathrm{d}s&=\int_{1}^{\frac{3}{2}} f(r(t))\,\|r'(t)\|\,\mathrm{d}t \\ &= \int_{1}^{\frac{3}{2}}(- 2 t^{3} + 14 t^{2} + 8 t + 2)(\sqrt{4 t^{2} + 5})\,\mathrm{d}t \\ &= \int_{1}^{\frac{3}{2}}2 \sqrt{4 t^{2} + 5} \left(- t^{3} + 7 t^{2} + 4 t + 1\right)\,\mathrm{d}t.\end{aligned}
$$

---

## hard / hard_product_square / a908ad08-fd2d-5338-a3b2-fa3636e47ff4

Which of the following is equivalent to $\int_C - 2 x y + 2 z^{2}\,\mathrm{d}s,$ where the curve $C$ is parametrized by $r(t)=\langle 3 t^{2}, t + 3, 2 t + 2\rangle$ for $0\le t\le \frac{5}{2}$?

1. $\int_{0}^{\frac{5}{2}}- 6 t^{3} - 10 t^{2} + 16 t + 8\,\mathrm{d}t$
2. $\int_{0}^{\frac{5}{2}}\frac{2 \left(- 3 t^{3} - 5 t^{2} + 8 t + 4\right)}{\sqrt{36 t^{2} + 5}}\,\mathrm{d}t$
3. $\int_{0}^{\frac{5}{2}}- 2 \left(36 t^{2} + 5\right) \left(3 t^{3} + 5 t^{2} - 8 t - 4\right)\,\mathrm{d}t$
4. $\int_{0}^{\frac{5}{2}}\sqrt{36 t^{2} + 5} \left(- 6 t^{3} - 10 t^{2} + 16 t + 8\right)\,\mathrm{d}t$
5. $\int_{0}^{\frac{5}{2}}2 \sqrt{36 t^{2} + 5} \left(- 3 t^{2} \left(t + 3\right) - 4 \left(t + 1\right)^{2}\right)\,\mathrm{d}t$

Since $r(t)=\langle 3 t^{2}, t + 3, 2 t + 2\rangle,$ then along the curve we have $x=3 t^{2}$, $y=t + 3$, $z=2 t + 2$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ &= \frac{\mathrm{d}}{\mathrm{d}t}(3 t^{2})i+\frac{\mathrm{d}}{\mathrm{d}t}(t + 3)j+\frac{\mathrm{d}}{\mathrm{d}t}(2 t + 2)k \\ &= (6 t)\,i+(1)\,j+(2)\,k \\ \|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2+(\frac{\mathrm{d}z}{\mathrm{d}t})^2} \\ &= \sqrt{(6 t)^2+(1)^2+(2)^2} \\ &= \sqrt{36 t^{2} + 5}\end{aligned}
$$

Now, since $f(x,y,z)=- 2 x y + 2 z^{2}$, we obtain

$$
\begin{aligned}f(r(t))&=-2\left((3 t^{2})(t + 3)-(2 t + 2)^2\right) \\ &= -2\left(3t^3+(9)t^2-\left(4t^2+(8)t+4\right)\right) \\ &= - 6 t^{3} - 10 t^{2} + 16 t + 8.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y,z)\,\mathrm{d}s&=\int_{0}^{\frac{5}{2}} f(r(t))\,\|r'(t)\|\,\mathrm{d}t \\ &= \int_{0}^{\frac{5}{2}}(- 6 t^{3} - 10 t^{2} + 16 t + 8)(\sqrt{36 t^{2} + 5})\,\mathrm{d}t \\ &= \int_{0}^{\frac{5}{2}}\sqrt{36 t^{2} + 5} \left(- 6 t^{3} - 10 t^{2} + 16 t + 8\right)\,\mathrm{d}t.\end{aligned}
$$

---

## hard / hard_product_square / 1b6b1bd1-88e4-5d2e-9dfb-33372f16d858

Which of the following is equivalent to $\int_C x y - z^{2}\,\mathrm{d}s,$ where the curve $C$ is parametrized by $r(t)=\langle 2 t^{2}, 2 t + 2, 3 t + 1\rangle$ for $0\le t\le 2$?

1. $\int_{0}^{2}\sqrt{16 t^{2} + 13} \left(4 t^{3} - 5 t^{2} - 6 t - 1\right)\,\mathrm{d}t$
2. $\int_{0}^{2}\frac{4 t^{3} - 5 t^{2} - 6 t - 1}{\sqrt{16 t^{2} + 13}}\,\mathrm{d}t$
3. $\int_{0}^{2}4 t^{3} - 5 t^{2} - 6 t - 1\,\mathrm{d}t$
4. $\int_{0}^{2}\sqrt{16 t^{2} + 13} \left(4 t^{2} \left(t + 1\right) + \left(3 t + 1\right)^{2}\right)\,\mathrm{d}t$
5. $\int_{0}^{2}- \left(16 t^{2} + 13\right) \left(- 4 t^{3} + 5 t^{2} + 6 t + 1\right)\,\mathrm{d}t$

Since $r(t)=\langle 2 t^{2}, 2 t + 2, 3 t + 1\rangle,$ then along the curve we have $x=2 t^{2}$, $y=2 t + 2$, $z=3 t + 1$.

Computing $r'(t)$ and $\|r'(t)\|,$ we get the following:

$$
\begin{aligned}r'(t)&=\frac{\mathrm{d}x}{\mathrm{d}t}\,i+\frac{\mathrm{d}y}{\mathrm{d}t}\,j+\frac{\mathrm{d}z}{\mathrm{d}t}\,k \\ &= \frac{\mathrm{d}}{\mathrm{d}t}(2 t^{2})i+\frac{\mathrm{d}}{\mathrm{d}t}(2 t + 2)j+\frac{\mathrm{d}}{\mathrm{d}t}(3 t + 1)k \\ &= (4 t)\,i+(2)\,j+(3)\,k \\ \|r'(t)\|&=\sqrt{(\frac{\mathrm{d}x}{\mathrm{d}t})^2+(\frac{\mathrm{d}y}{\mathrm{d}t})^2+(\frac{\mathrm{d}z}{\mathrm{d}t})^2} \\ &= \sqrt{(4 t)^2+(2)^2+(3)^2} \\ &= \sqrt{16 t^{2} + 13}\end{aligned}
$$

Now, since $f(x,y,z)=x y - z^{2}$, we obtain

$$
\begin{aligned}f(r(t))&=(2 t^{2})(2 t + 2)-(3 t + 1)^2 \\ &= 4t^3+(4)t^2-\left(9t^2+(6)t+1\right) \\ &= 4 t^{3} - 5 t^{2} - 6 t - 1.\end{aligned}
$$

Therefore, we can write the integral as

$$
\begin{aligned}\int_C f(x,y,z)\,\mathrm{d}s&=\int_{0}^{2} f(r(t))\,\|r'(t)\|\,\mathrm{d}t \\ &= \int_{0}^{2}(4 t^{3} - 5 t^{2} - 6 t - 1)(\sqrt{16 t^{2} + 13})\,\mathrm{d}t \\ &= \int_{0}^{2}\sqrt{16 t^{2} + 13} \left(4 t^{3} - 5 t^{2} - 6 t - 1\right)\,\mathrm{d}t.\end{aligned}
$$
