# Polar repeated integral review

All records are local author review data. Ten source originals have exact bank/prompt replay; the missing q-38127 solution and level are authored. Generated defaults and scaled observed banks are labeled separately.


## Original source replay

### q-38031 — moderate

Evaluate 
${\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{sin}⁡\theta }2r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta .$

- A. $2$
- B. $1$
- C. $\frac{2}{3}$
- D. $\frac{1}{3}$ **correct**
- E. $2\pi $

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}{\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{sin}⁡\theta }2r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta  & ={\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {\int }_{0}^{\operatorname{sin}⁡\theta }2r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \,[{r}^{2}]_{0}^{\operatorname{sin}⁡\theta }\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}\theta \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}\theta  & =\frac{1}{3}{[{sin}^{3}⁡\theta ]}_{0}^{\pi /2} \\  & =\frac{1}{3}[{1}^{3}-{0}^{3}] \\  & =\frac{1}{3}\end{aligned}
$$


## Original source replay

### q-38127 — easy

What is $\displaystyle \int_{π/3}^{π/2}\displaystyle \int_{1}^{2}r^{2}\sin θdrdθ$?

- A. $\frac{π}{5}$
- B. $\frac{7}{6}$ **correct**
- C. $-\frac{2}{3}$
- D. $4$
- E. $- π$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \int_{1}^{2} r^{2} \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \sin{\left(\theta \right)} \int_{1}^{2} r^{2}\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \sin{\left(\theta \right)} \left[\frac{r^{3}}{3}\right]_{1}^{2}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \sin{\left(\theta \right)} \left(\frac{\left(2\right)^{3}-\left(1\right)^{3}}{3}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \frac{7 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \frac{7 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta & = \left[- \frac{7 \cos{\left(\theta \right)}}{3}\right]_{\frac{\pi}{3}}^{\frac{\pi}{2}} \\
& = \left(\left(- \frac{7 \cos{\left(\left(\frac{\pi}{2}\right) \right)}}{3}\right)\right)-\left(\left(- \frac{7 \cos{\left(\left(\frac{\pi}{3}\right) \right)}}{3}\right)\right) \\
& = \left(\left(0\right)\right)-\left(\left(- \frac{7}{6}\right)\right) \\
& = \frac{7}{6}
\end{aligned}
$$


## Original source replay

### q-161049 — moderate

Evaluate 
${\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{cos}⁡\theta }3r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta .$

- A. $1$ **correct**
- B. $\frac{1}{2}$
- C. $2$
- D. $3$
- E. $\frac{3}{2}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}{\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{cos}⁡\theta }3r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta  & ={\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta {\int }_{0}^{\operatorname{cos}⁡\theta }r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta \,{[\frac{{r}^{2}}{2}]}_{0}^{\operatorname{cos}⁡\theta }\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta \,(\frac{{cos}^{2}⁡\theta }{2}-0)\,\text{d}\theta  \\  & =\frac{3}{2}{\int }_{0}^{\pi /2}{cos}^{3}⁡\theta \,\text{d}\theta \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}\frac{3}{2}{\int }_{0}^{\pi /2}{cos}^{3}⁡\theta \,\text{d}\theta  & =\frac{3}{2}{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta (1-{sin}^{2}⁡\theta )\,\text{d}\theta  \\  & =\frac{3}{2}{[\operatorname{sin}⁡\theta -\frac{{sin}^{3}⁡\theta }{3}]}_{0}^{\pi /2} \\  & =\frac{3}{2}[(\operatorname{sin}⁡\frac{\pi }{2}-\frac{1}{3}{sin}^{3}⁡\frac{\pi }{2})-(\operatorname{sin}⁡0-\frac{1}{3}{sin}^{3}⁡0)] \\  & =\frac{3}{2}[(1-\frac{1}{3})-0] \\  & =1\end{aligned}
$$


## Original source replay

### q-38133 — easy

${\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta =$

- A. $\frac{\sqrt{3}}{2}$
- B. $\pi $ **correct**
- C. $\frac{\pi }{4}$
- D. $\pi +4$
- E. $2\pi $

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}{\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta  & ={\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{-\pi /2}^{\pi /2}{[\frac{{r}^{2}}{2}]}_{0}^{2\operatorname{cos}⁡(2\theta )}\,\text{d}\theta  \\  & ={\int }_{-\pi /2}^{\pi /2}(\frac{(2\operatorname{cos}⁡(2\theta ))^{2}}{2}-0)\,\text{d}\theta  \\  & ={\int }_{-\pi /2}^{\pi /2}2{cos}^{2}⁡(2\theta )\,\text{d}\theta \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}{\int }_{-\pi /2}^{\pi /2}2{cos}^{2}⁡(2\theta )\,\text{d}\theta  & ={\int }_{-\pi /2}^{\pi /2}(1+\operatorname{cos}⁡(4\theta ))\,\text{d}\theta  \\  & ={[\theta +\frac{1}{4}\operatorname{sin}⁡(4\theta )]}_{-\pi /2}^{\pi /2} \\  & =(\frac{\pi }{2}+\frac{\pi }{2})+\frac{1}{4}(\operatorname{sin}⁡(2\pi )-\operatorname{sin}⁡(-2\pi )) \\  & =\pi \end{aligned}
$$


## Original source replay

### q-83511 — easy

Evaluate ${\int }_{0}^{\pi /2}{\int }_{1}^{3}{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta .$

- A. $10$ **correct**
- B. $30$
- C. $5$
- D. $40$
- E. $20$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}{\int }_{0}^{\pi /2}{\int }_{1}^{3}{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta  & ={\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta {\int }_{1}^{3}{r}^{3}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta {[\frac{{r}^{4}}{4}]}_{1}^{3}\,\text{d}\theta  \\  & =\frac{1}{4}{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta ({3}^{4}-{1}^{4})\,\text{d}\theta  \\  & =20{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}\theta \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}20{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}\theta  & =20[\frac{{sin}^{2}⁡\theta }{2}]_{0}^{\pi /2} \\  & =10{[{sin}^{2}⁡\theta ]}_{0}^{\pi /2} \\  & =10({sin}^{2}⁡(\frac{\pi }{2})-{sin}^{2}⁡(0)) \\  & =10(1-0) \\  & =10\end{aligned}
$$


## Original source replay

### q-83957 — easy

${\int }_{\pi /6}^{3\pi /4}{\int }_{2}^{4}r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta =$

- A. $3\sqrt{2}$
- B. $3$
- C. $6(\sqrt{2}-1)$
- D. $3(\sqrt{2}-1)$ **correct**
- E. $\frac{3}{2}(\sqrt{2}-1)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}{\int }_{\pi /6}^{3\pi /4}{\int }_{2}^{4}r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta  & ={\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta {\int }_{2}^{4}r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta {[\frac{{r}^{2}}{2}]}_{2}^{4}\,\text{d}\theta  \\  & =\frac{1}{2}{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta ({4}^{2}-{2}^{2})\,\text{d}\theta  \\  & =6{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta \,\text{d}\theta \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}6{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta \,\text{d}\theta  & =6[\operatorname{sin}⁡\theta ]_{\pi /6}^{3\pi /4} \\  & =6(\operatorname{sin}⁡(\frac{3\pi }{4})-\operatorname{sin}⁡(\frac{\pi }{6})) \\  & =6(\frac{\sqrt{2}}{2}-\frac{1}{2}) \\  & =3(\sqrt{2}-1)\end{aligned}
$$


## Original source replay

### q-83958 — moderate

Evaluate 
${\int }_{0}^{\pi /2}{\int }_{1-\operatorname{cos}⁡\theta }^{1}r\,\text{d}r\,\text{d}\theta .$

- A. $\frac{2-\pi }{2}$
- B. $8-\pi $
- C. $\frac{4-\pi }{4}$
- D. $1-\pi $
- E. $\frac{8-\pi }{8}$ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}{\int }_{0}^{\pi /2}{\int }_{1-\operatorname{cos}⁡\theta }^{1}r\,\text{d}r\,\text{d}\theta  & ={\int }_{0}^{\pi /2}\,[\frac{{r}^{2}}{2}]_{1-\operatorname{cos}⁡\theta }^{1}\,\text{d}\theta  \\  & =\frac{1}{2}{\int }_{0}^{\pi /2}({1}^{2}-(1-\operatorname{cos}⁡\theta )^{2})\,\text{d}\theta  \\  & =\frac{1}{2}{\int }_{0}^{\pi /2}(2\operatorname{cos}⁡\theta -{cos}^{2}⁡\theta )\,\text{d}\theta \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}\frac{1}{2}{\int }_{0}^{\pi /2}(2\operatorname{cos}⁡\theta -{cos}^{2}⁡\theta )\,\text{d}\theta  & ={[\operatorname{sin}⁡\theta -\frac{1}{4}\theta -\frac{1}{8}\operatorname{sin}⁡(2\theta )]}_{0}^{\pi /2} \\  & =(\operatorname{sin}⁡(\frac{\pi }{2})-\frac{1}{4}\cdot \frac{\pi }{2}-\frac{1}{8}\operatorname{sin}⁡\pi )-0 \\  & =1-\frac{\pi }{8}-\frac{1}{8}\cdot 0 \\  & =\frac{8-\pi }{8}\end{aligned}
$$


## Original source replay

### q-83514 — moderate

Evaluate 
${\int }_{\pi /4}^{\pi /2}{\int }_{\operatorname{csc}⁡\theta }^{2}2r\,\text{d}r\,\text{d}\theta .$

- A. $\pi -2$
- B. $\pi +1$
- C. $\pi -1$ **correct**
- D. $\pi $
- E. $\pi +2$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}{\int }_{\pi /4}^{\pi /2}{\int }_{\operatorname{csc}⁡\theta }^{2}2r\,\text{d}r\,\text{d}\theta  & ={\int }_{\pi /4}^{\pi /2}[{r}^{2}]_{\operatorname{csc}⁡\theta }^{2}\,\text{d}\theta  \\  & ={\int }_{\pi /4}^{\pi /2}({2}^{2}-{csc}^{2}⁡\theta )\,\text{d}\theta  \\  & ={\int }_{\pi /4}^{\pi /2}(4-{csc}^{2}⁡\theta )\,\text{d}\theta \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}{\int }_{\pi /4}^{\pi /2}(4-{csc}^{2}⁡\theta )\,\text{d}\theta  & =[4\theta +\operatorname{cot}⁡\theta ]_{\pi /4}^{\pi /2} \\  & =(4\cdot \frac{\pi }{2}+\operatorname{cot}⁡(\frac{\pi }{2}))-(4\cdot \frac{\pi }{4}+\operatorname{cot}⁡(\frac{\pi }{4})) \\  & =(2\pi +0)-(\pi +1) \\  & =\pi -1\end{aligned}
$$


## Original source replay

### q-161048 — easy

${\int }_{0}^{\pi }{\int }_{0}^{1}5{r}^{4}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta =$

- A. $5$
- B. $1$
- C. $0$
- D. $4$
- E. $2$ **correct**

First, we integrate with respect to $r$ treating $\theta $ as a constant:

$$
\begin{aligned}{\int }_{0}^{\pi }{\int }_{0}^{1}5{r}^{4}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta  & ={\int }_{0}^{\pi }\operatorname{sin}⁡\theta {\int }_{0}^{1}5{r}^{4}\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{0}^{\pi }\operatorname{sin}⁡\theta [{r}^{5}]_{0}^{1}\,\text{d}\theta  \\  & ={\int }_{0}^{\pi }\operatorname{sin}⁡\theta (1-0)\,\text{d}\theta  \\  & ={\int }_{0}^{\pi }\operatorname{sin}⁡\theta \,\text{d}\theta \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}{\int }_{0}^{\pi }\operatorname{sin}⁡\theta \,\text{d}\theta  & =[-\operatorname{cos}⁡\theta ]_{0}^{\pi } \\  & =-(\operatorname{cos}⁡\pi -\operatorname{cos}⁡0) \\  & =-(-1-1) \\  & =2\end{aligned}
$$


## Original source replay

### q-83966 — moderate

Evaluate 
${\int }_{5\pi /3}^{2\pi }{\int }_{1}^{2\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta .$

- A. $\frac{1}{12}$
- B. $-\frac{1}{3}$ **correct**
- C. $-\frac{1}{12}$
- D. $-\frac{1}{6}$
- E. $\frac{1}{6}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}{\int }_{5\pi /3}^{2\pi }{\int }_{1}^{2\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta  & ={\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta {\int }_{1}^{2\operatorname{cos}⁡\theta }r\,\text{d}r\,\text{d}\theta  \\  & ={\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta \,[\frac{{r}^{2}}{2}]_{1}^{2\operatorname{cos}⁡\theta }\,\text{d}\theta  \\  & =\frac{1}{2}{\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta ((2\operatorname{cos}⁡\theta )^{2}-{1}^{2})\,\text{d}\theta  \\  & =\frac{1}{2}{\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta (4{cos}^{2}⁡\theta -1)\,\text{d}\theta  \\  & =\frac{1}{2}{\int }_{5\pi /3}^{2\pi }(4\operatorname{sin}⁡\theta {cos}^{2}⁡\theta -\operatorname{sin}⁡\theta )\,\text{d}\theta \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}\frac{1}{2}{\int }_{5\pi /3}^{2\pi }(4\operatorname{sin}⁡\theta {cos}^{2}⁡\theta -\operatorname{sin}⁡\theta )\,\text{d}\theta  & =\frac{1}{2}{[-\frac{4}{3}{cos}^{3}⁡\theta +\operatorname{cos}⁡\theta ]}_{5\pi /3}^{2\pi } \\  & =\frac{1}{2}[(-\frac{4}{3}{cos}^{3}⁡(2\pi )+\operatorname{cos}⁡(2\pi ))-(-\frac{4}{3}{cos}^{3}⁡(\frac{5\pi }{3})+\operatorname{cos}⁡(\frac{5\pi }{3}))] \\  & =\frac{1}{2}[(-\frac{4}{3}+1)-(-\frac{1}{6}+\frac{1}{2})] \\  & =-\frac{1}{3}\end{aligned}
$$


## Generated authored operation bank

### q-38031 — moderate

Evaluate $\int_{0}^{\frac{\pi}{3}} \int_{0}^{3 \sin{\left(\theta \right)}} 4 r \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $\frac{9 \sqrt{3}}{4}$ **correct**
- B. $\frac{9 \sqrt{3}}{2}$
- C. $\frac{9 \sqrt{3}}{8}$
- D. $\frac{81}{16}$
- E. $- \frac{9 \sqrt{3}}{4}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{3}} \int_{0}^{3 \sin{\left(\theta \right)}} 4 r \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{3}} 4 \cos{\left(\theta \right)} \int_{0}^{3 \sin{\left(\theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 4 \cos{\left(\theta \right)} \left[\frac{r^{2}}{2}\right]_{0}^{3 \sin{\left(\theta \right)}}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 4 \cos{\left(\theta \right)} \left(\frac{\left(3 \sin{\left(\theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 18 \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{3}} 18 \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)}\,\mathrm d \theta & = \left[6 \sin^{3}{\left(\theta \right)}\right]_{0}^{\frac{\pi}{3}} \\
& = \left(\left(6 \sin^{3}{\left(\left(\frac{\pi}{3}\right) \right)}\right)\right)-\left(\left(6 \sin^{3}{\left(\left(0\right) \right)}\right)\right) \\
& = \left(\left(\frac{9 \sqrt{3}}{4}\right)\right)-\left(\left(0\right)\right) \\
& = \frac{9 \sqrt{3}}{4}
\end{aligned}
$$


## Generated authored operation bank

### q-38031 — moderate

Evaluate $\int_{0}^{\frac{\pi}{3}} \int_{0}^{4 \sin{\left(\theta \right)}} 4 r \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $8 \sqrt{3}$
- B. $12$
- C. $2 \sqrt{3}$
- D. $4 \sqrt{3}$ **correct**
- E. $- 4 \sqrt{3}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{3}} \int_{0}^{4 \sin{\left(\theta \right)}} 4 r \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{3}} 4 \cos{\left(\theta \right)} \int_{0}^{4 \sin{\left(\theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 4 \cos{\left(\theta \right)} \left[\frac{r^{2}}{2}\right]_{0}^{4 \sin{\left(\theta \right)}}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 4 \cos{\left(\theta \right)} \left(\frac{\left(4 \sin{\left(\theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 32 \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{3}} 32 \sin^{2}{\left(\theta \right)} \cos{\left(\theta \right)}\,\mathrm d \theta & = \left[\frac{32 \sin^{3}{\left(\theta \right)}}{3}\right]_{0}^{\frac{\pi}{3}} \\
& = \left(\left(\frac{32 \sin^{3}{\left(\left(\frac{\pi}{3}\right) \right)}}{3}\right)\right)-\left(\left(\frac{32 \sin^{3}{\left(\left(0\right) \right)}}{3}\right)\right) \\
& = \left(\left(4 \sqrt{3}\right)\right)-\left(\left(0\right)\right) \\
& = 4 \sqrt{3}
\end{aligned}
$$


## Generated authored operation bank

### q-38127 — easy

Evaluate $\int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \int_{1}^{2} 4 r^{2} \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $- \frac{14 \sqrt{2}}{3} - \frac{14}{3}$
- B. $\frac{14}{3} + \frac{14 \sqrt{2}}{3}$ **correct**
- C. $14 + 14 \sqrt{2}$
- D. $\frac{15}{2} + \frac{15 \sqrt{2}}{2}$
- E. $\frac{7 \sqrt{2}}{3} + \frac{14}{3}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \int_{1}^{2} 4 r^{2} \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} 4 \sin{\left(\theta \right)} \int_{1}^{2} r^{2}\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} 4 \sin{\left(\theta \right)} \left[\frac{r^{3}}{3}\right]_{1}^{2}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} 4 \sin{\left(\theta \right)} \left(\frac{\left(2\right)^{3}-\left(1\right)^{3}}{3}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \frac{28 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \frac{28 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta & = \left[- \frac{28 \cos{\left(\theta \right)}}{3}\right]_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \\
& = \left(\left(- \frac{28 \cos{\left(\left(\frac{3 \pi}{4}\right) \right)}}{3}\right)\right)-\left(\left(- \frac{28 \cos{\left(\left(\frac{\pi}{3}\right) \right)}}{3}\right)\right) \\
& = \left(\left(\frac{14 \sqrt{2}}{3}\right)\right)-\left(\left(- \frac{14}{3}\right)\right) \\
& = \frac{14}{3} + \frac{14 \sqrt{2}}{3}
\end{aligned}
$$


## Generated authored operation bank

### q-38127 — easy

Evaluate $\int_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \int_{2}^{3} r^{2} \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $\frac{65 \sqrt{2}}{8} + \frac{65 \sqrt{3}}{8}$
- B. $- \frac{19 \sqrt{3}}{6} - \frac{19 \sqrt{2}}{6}$
- C. $\frac{19 \sqrt{2}}{2} + \frac{19 \sqrt{3}}{2}$
- D. $\frac{19 \sqrt{2}}{12} + \frac{19 \sqrt{3}}{6}$
- E. $\frac{19 \sqrt{2}}{6} + \frac{19 \sqrt{3}}{6}$ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \int_{2}^{3} r^{2} \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \sin{\left(\theta \right)} \int_{2}^{3} r^{2}\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \sin{\left(\theta \right)} \left[\frac{r^{3}}{3}\right]_{2}^{3}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \sin{\left(\theta \right)} \left(\frac{\left(3\right)^{3}-\left(2\right)^{3}}{3}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \frac{19 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \frac{19 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta & = \left[- \frac{19 \cos{\left(\theta \right)}}{3}\right]_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \\
& = \left(\left(- \frac{19 \cos{\left(\left(\frac{3 \pi}{4}\right) \right)}}{3}\right)\right)-\left(\left(- \frac{19 \cos{\left(\left(\frac{\pi}{6}\right) \right)}}{3}\right)\right) \\
& = \left(\left(\frac{19 \sqrt{2}}{6}\right)\right)-\left(\left(- \frac{19 \sqrt{3}}{6}\right)\right) \\
& = \frac{19 \sqrt{2}}{6} + \frac{19 \sqrt{3}}{6}
\end{aligned}
$$


## Generated authored operation bank

### q-161049 — moderate

Evaluate $\int_{0}^{\frac{\pi}{3}} \int_{0}^{3 \cos{\left(\theta \right)}} 4 r \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $\frac{27 \sqrt{3}}{4}$ **correct**
- B. $\frac{27 \sqrt{3}}{2}$
- C. $\frac{27 \sqrt{3}}{8}$
- D. $\frac{63 \sqrt{3}}{16} + \frac{9 \pi}{2}$
- E. $- \frac{27 \sqrt{3}}{4}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{3}} \int_{0}^{3 \cos{\left(\theta \right)}} 4 r \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{3}} 4 \cos{\left(\theta \right)} \int_{0}^{3 \cos{\left(\theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 4 \cos{\left(\theta \right)} \left[\frac{r^{2}}{2}\right]_{0}^{3 \cos{\left(\theta \right)}}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 4 \cos{\left(\theta \right)} \left(\frac{\left(3 \cos{\left(\theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 18 \cos^{3}{\left(\theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{3}} 18 \cos^{3}{\left(\theta \right)}\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{3}} 18\cos\theta\left(1-\sin^2\theta\right)\,\mathrm d \theta \\
& = \left[- 6 \sin^{3}{\left(\theta \right)} + 18 \sin{\left(\theta \right)}\right]_{0}^{\frac{\pi}{3}} \\
& = \left(\left(- 6 \sin^{3}{\left(\left(\frac{\pi}{3}\right) \right)}\right)+\left(18 \sin{\left(\left(\frac{\pi}{3}\right) \right)}\right)\right)-\left(\left(- 6 \sin^{3}{\left(\left(0\right) \right)}\right)+\left(18 \sin{\left(\left(0\right) \right)}\right)\right) \\
& = \left(\left(- \frac{9 \sqrt{3}}{4}\right)+\left(9 \sqrt{3}\right)\right)-\left(\left(0\right)+\left(0\right)\right) \\
& = \frac{27 \sqrt{3}}{4}
\end{aligned}
$$


## Generated authored operation bank

### q-161049 — moderate

Evaluate $\int_{0}^{\frac{\pi}{3}} \int_{0}^{4 \cos{\left(\theta \right)}} 4 r \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $24 \sqrt{3}$
- B. $\frac{28 \sqrt{3}}{3} + \frac{32 \pi}{3}$
- C. $6 \sqrt{3}$
- D. $12 \sqrt{3}$ **correct**
- E. $- 12 \sqrt{3}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{3}} \int_{0}^{4 \cos{\left(\theta \right)}} 4 r \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{3}} 4 \cos{\left(\theta \right)} \int_{0}^{4 \cos{\left(\theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 4 \cos{\left(\theta \right)} \left[\frac{r^{2}}{2}\right]_{0}^{4 \cos{\left(\theta \right)}}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 4 \cos{\left(\theta \right)} \left(\frac{\left(4 \cos{\left(\theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 32 \cos^{3}{\left(\theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{3}} 32 \cos^{3}{\left(\theta \right)}\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{3}} 32\cos\theta\left(1-\sin^2\theta\right)\,\mathrm d \theta \\
& = \left[- \frac{32 \sin^{3}{\left(\theta \right)}}{3} + 32 \sin{\left(\theta \right)}\right]_{0}^{\frac{\pi}{3}} \\
& = \left(\left(32 \sin{\left(\left(\frac{\pi}{3}\right) \right)}\right)+\left(- \frac{32 \sin^{3}{\left(\left(\frac{\pi}{3}\right) \right)}}{3}\right)\right)-\left(\left(32 \sin{\left(\left(0\right) \right)}\right)+\left(- \frac{32 \sin^{3}{\left(\left(0\right) \right)}}{3}\right)\right) \\
& = \left(\left(16 \sqrt{3}\right)+\left(- 4 \sqrt{3}\right)\right)-\left(\left(0\right)+\left(0\right)\right) \\
& = 12 \sqrt{3}
\end{aligned}
$$


## Generated authored operation bank

### q-38133 — easy

Evaluate $\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \int_{0}^{3 \cos{\left(\theta \right)}} 4 r\,\mathrm d r\,\mathrm d \theta.$

- A. $9 \pi$ **correct**
- B. $\frac{27 \pi}{4}$
- C. $48$
- D. $- 9 \pi$
- E. $18 \pi$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \int_{0}^{3 \cos{\left(\theta \right)}} 4 r\,\mathrm d r\,\mathrm d \theta & = \int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} 4 \int_{0}^{3 \cos{\left(\theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} 4 \left[\frac{r^{2}}{2}\right]_{0}^{3 \cos{\left(\theta \right)}}\,\mathrm d \theta \\
& = \int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} 4 \left(\frac{\left(3 \cos{\left(\theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} 18 \cos^{2}{\left(\theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we recall the double-angle formula

$$
\cos(2x)=2\cos^2 x-1.
$$

Substituting $x=1\theta$ and rearranging, we get

$$
\cos^2\left(1\theta\right)=\frac{1}{2}\left(1+\cos\left(2\theta\right)\right).
$$

Finally, we can finish our integral by integrating with respect to $\theta,$ as follows:

$$
\begin{aligned}
\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} 18 \cos^{2}{\left(\theta \right)}\,\mathrm d \theta & = \int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} 9\left(1+\cos\left(2\theta\right)\right)\,\mathrm d \theta \\
& = 9\left[\theta + \frac{\sin{\left(2 \theta \right)}}{2}\right]_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \\
& = 9\left(\left(\frac{\pi}{2}+\frac{1}{2}\sin\left(\pi\right)\right)-\left(- \frac{\pi}{2}+\frac{1}{2}\sin\left(- \pi\right)\right)\right) \\
& = 9\left(\left(\frac{\pi}{2}+\frac{1}{2} \left(0\right)\right)-\left(- \frac{\pi}{2}+\frac{1}{2} \left(0\right)\right)\right) \\
& = 9\left(\left(\pi\right)+\frac{1}{2}\left(0\right)\right) \\
& = 9 \pi
\end{aligned}
$$


## Generated authored operation bank

### q-38133 — easy

Evaluate $\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \int_{0}^{4 \cos{\left(\theta \right)}} 4 r\,\mathrm d r\,\mathrm d \theta.$

- A. $12 \pi$
- B. $\frac{1024}{9}$
- C. $16 \pi$ **correct**
- D. $- 16 \pi$
- E. $32 \pi$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \int_{0}^{4 \cos{\left(\theta \right)}} 4 r\,\mathrm d r\,\mathrm d \theta & = \int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} 4 \int_{0}^{4 \cos{\left(\theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} 4 \left[\frac{r^{2}}{2}\right]_{0}^{4 \cos{\left(\theta \right)}}\,\mathrm d \theta \\
& = \int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} 4 \left(\frac{\left(4 \cos{\left(\theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} 32 \cos^{2}{\left(\theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we recall the double-angle formula

$$
\cos(2x)=2\cos^2 x-1.
$$

Substituting $x=1\theta$ and rearranging, we get

$$
\cos^2\left(1\theta\right)=\frac{1}{2}\left(1+\cos\left(2\theta\right)\right).
$$

Finally, we can finish our integral by integrating with respect to $\theta,$ as follows:

$$
\begin{aligned}
\int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} 32 \cos^{2}{\left(\theta \right)}\,\mathrm d \theta & = \int_{- \frac{\pi}{2}}^{\frac{\pi}{2}} 16\left(1+\cos\left(2\theta\right)\right)\,\mathrm d \theta \\
& = 16\left[\theta + \frac{\sin{\left(2 \theta \right)}}{2}\right]_{- \frac{\pi}{2}}^{\frac{\pi}{2}} \\
& = 16\left(\left(\frac{\pi}{2}+\frac{1}{2}\sin\left(\pi\right)\right)-\left(- \frac{\pi}{2}+\frac{1}{2}\sin\left(- \pi\right)\right)\right) \\
& = 16\left(\left(\frac{\pi}{2}+\frac{1}{2} \left(0\right)\right)-\left(- \frac{\pi}{2}+\frac{1}{2} \left(0\right)\right)\right) \\
& = 16\left(\left(\pi\right)+\frac{1}{2}\left(0\right)\right) \\
& = 16 \pi
\end{aligned}
$$


## Generated authored operation bank

### q-83511 — easy

Evaluate $\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \int_{1}^{2} 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $\frac{7}{2}$ **correct**
- B. $\frac{21}{2}$
- C. $- \frac{7}{2}$
- D. $\frac{45}{8}$
- E. $\frac{7}{6}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \int_{1}^{2} 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{6}}^{\frac{\pi}{2}} 4 \sin{\left(\theta \right)} \cos{\left(\theta \right)} \int_{1}^{2} r^{2}\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{\pi}{2}} 4 \sin{\left(\theta \right)} \cos{\left(\theta \right)} \left[\frac{r^{3}}{3}\right]_{1}^{2}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{\pi}{2}} 4 \sin{\left(\theta \right)} \cos{\left(\theta \right)} \left(\frac{\left(2\right)^{3}-\left(1\right)^{3}}{3}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \frac{28 \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{3}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \frac{28 \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{3}\,\mathrm d \theta & = \left[\frac{14 \sin^{2}{\left(\theta \right)}}{3}\right]_{\frac{\pi}{6}}^{\frac{\pi}{2}} \\
& = \left(\left(\frac{14 \sin^{2}{\left(\left(\frac{\pi}{2}\right) \right)}}{3}\right)\right)-\left(\left(\frac{14 \sin^{2}{\left(\left(\frac{\pi}{6}\right) \right)}}{3}\right)\right) \\
& = \left(\left(\frac{14}{3}\right)\right)-\left(\left(\frac{7}{6}\right)\right) \\
& = \frac{7}{2}
\end{aligned}
$$


## Generated authored operation bank

### q-83511 — easy

Evaluate $\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \int_{1}^{2} 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $\frac{21}{2}$
- B. $- \frac{7}{2}$
- C. $\frac{45}{8}$
- D. $\frac{7}{6}$
- E. $\frac{7}{2}$ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \int_{1}^{2} 4 r^{2} \sin{\left(\theta \right)} \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{6}}^{\frac{\pi}{2}} 4 \sin{\left(\theta \right)} \cos{\left(\theta \right)} \int_{1}^{2} r^{2}\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{\pi}{2}} 4 \sin{\left(\theta \right)} \cos{\left(\theta \right)} \left[\frac{r^{3}}{3}\right]_{1}^{2}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{\pi}{2}} 4 \sin{\left(\theta \right)} \cos{\left(\theta \right)} \left(\frac{\left(2\right)^{3}-\left(1\right)^{3}}{3}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \frac{28 \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{3}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \frac{28 \sin{\left(\theta \right)} \cos{\left(\theta \right)}}{3}\,\mathrm d \theta & = \left[\frac{14 \sin^{2}{\left(\theta \right)}}{3}\right]_{\frac{\pi}{6}}^{\frac{\pi}{2}} \\
& = \left(\left(\frac{14 \sin^{2}{\left(\left(\frac{\pi}{2}\right) \right)}}{3}\right)\right)-\left(\left(\frac{14 \sin^{2}{\left(\left(\frac{\pi}{6}\right) \right)}}{3}\right)\right) \\
& = \left(\left(\frac{14}{3}\right)\right)-\left(\left(\frac{7}{6}\right)\right) \\
& = \frac{7}{2}
\end{aligned}
$$


## Generated authored operation bank

### q-83957 — easy

Evaluate $\int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \int_{1}^{2} 4 r^{2} \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $- \frac{14 \sqrt{2}}{3} + \frac{14 \sqrt{3}}{3}$
- B. $- \frac{14 \sqrt{3}}{3} + \frac{14 \sqrt{2}}{3}$ **correct**
- C. $- 14 \sqrt{3} + 14 \sqrt{2}$
- D. $- \frac{15 \sqrt{3}}{2} + \frac{15 \sqrt{2}}{2}$
- E. $- \frac{14 \sqrt{3}}{3} + \frac{7 \sqrt{2}}{3}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \int_{1}^{2} 4 r^{2} \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} 4 \cos{\left(\theta \right)} \int_{1}^{2} r^{2}\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} 4 \cos{\left(\theta \right)} \left[\frac{r^{3}}{3}\right]_{1}^{2}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} 4 \cos{\left(\theta \right)} \left(\frac{\left(2\right)^{3}-\left(1\right)^{3}}{3}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \frac{28 \cos{\left(\theta \right)}}{3}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \frac{28 \cos{\left(\theta \right)}}{3}\,\mathrm d \theta & = \left[\frac{28 \sin{\left(\theta \right)}}{3}\right]_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \\
& = \left(\left(\frac{28 \sin{\left(\left(\frac{3 \pi}{4}\right) \right)}}{3}\right)\right)-\left(\left(\frac{28 \sin{\left(\left(\frac{\pi}{3}\right) \right)}}{3}\right)\right) \\
& = \left(\left(\frac{14 \sqrt{2}}{3}\right)\right)-\left(\left(\frac{14 \sqrt{3}}{3}\right)\right) \\
& = - \frac{14 \sqrt{3}}{3} + \frac{14 \sqrt{2}}{3}
\end{aligned}
$$


## Generated authored operation bank

### q-83957 — easy

Evaluate $\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \int_{1}^{2} 4 r^{2} \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $- \frac{28}{3} + \frac{14 \sqrt{3}}{3}$
- B. $15 - \frac{15 \sqrt{3}}{2}$
- C. $\frac{14}{3} - \frac{14 \sqrt{3}}{3}$
- D. $28 - 14 \sqrt{3}$
- E. $\frac{28}{3} - \frac{14 \sqrt{3}}{3}$ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \int_{1}^{2} 4 r^{2} \cos{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 4 \cos{\left(\theta \right)} \int_{1}^{2} r^{2}\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 4 \cos{\left(\theta \right)} \left[\frac{r^{3}}{3}\right]_{1}^{2}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 4 \cos{\left(\theta \right)} \left(\frac{\left(2\right)^{3}-\left(1\right)^{3}}{3}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \frac{28 \cos{\left(\theta \right)}}{3}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \frac{28 \cos{\left(\theta \right)}}{3}\,\mathrm d \theta & = \left[\frac{28 \sin{\left(\theta \right)}}{3}\right]_{\frac{\pi}{3}}^{\frac{\pi}{2}} \\
& = \left(\left(\frac{28 \sin{\left(\left(\frac{\pi}{2}\right) \right)}}{3}\right)\right)-\left(\left(\frac{28 \sin{\left(\left(\frac{\pi}{3}\right) \right)}}{3}\right)\right) \\
& = \left(\left(\frac{28}{3}\right)\right)-\left(\left(\frac{14 \sqrt{3}}{3}\right)\right) \\
& = \frac{28}{3} - \frac{14 \sqrt{3}}{3}
\end{aligned}
$$


## Generated authored operation bank

### q-83958 — moderate

Evaluate $\int_{0}^{\frac{\pi}{3}} \int_{3 - 3 \cos{\left(\theta \right)}}^{3} 4 r\,\mathrm d r\,\mathrm d \theta.$

- A. $- 3 \pi + \frac{63 \sqrt{3}}{4}$ **correct**
- B. $- 6 \pi + \frac{63 \sqrt{3}}{2}$
- C. $- \frac{3 \pi}{2} + \frac{63 \sqrt{3}}{8}$
- D. $- 18 \pi + 54 \sqrt{3}$
- E. $- \frac{63 \sqrt{3}}{4} + 3 \pi$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{3}} \int_{3 - 3 \cos{\left(\theta \right)}}^{3} 4 r\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{3}} 4 \int_{3 - 3 \cos{\left(\theta \right)}}^{3} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 4 \left[\frac{r^{2}}{2}\right]_{3 - 3 \cos{\left(\theta \right)}}^{3}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 4 \left(\frac{\left(3\right)^{2}-\left(3 - 3 \cos{\left(\theta \right)}\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} - 18 \cos^{2}{\left(\theta \right)} + 36 \cos{\left(\theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{3}} - 18 \cos^{2}{\left(\theta \right)} + 36 \cos{\left(\theta \right)}\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{3}} 18\left(2\cos\theta-\frac{1+\cos(2\theta)}{2}\right)\,\mathrm d \theta \\
& = \left[- 9 \theta + 36 \sin{\left(\theta \right)} - \frac{9 \sin{\left(2 \theta \right)}}{2}\right]_{0}^{\frac{\pi}{3}} \\
& = \left(\left(- 9 \left(\frac{\pi}{3}\right)\right)+\left(36 \sin{\left(\left(\frac{\pi}{3}\right) \right)}\right)+\left(- \frac{9 \sin{\left(2 \left(\frac{\pi}{3}\right) \right)}}{2}\right)\right)-\left(\left(- 9 \left(0\right)\right)+\left(36 \sin{\left(\left(0\right) \right)}\right)+\left(- \frac{9 \sin{\left(2 \left(0\right) \right)}}{2}\right)\right) \\
& = \left(\left(- 3 \pi\right)+\left(18 \sqrt{3}\right)+\left(- \frac{9 \sqrt{3}}{4}\right)\right)-\left(\left(0\right)+\left(0\right)+\left(0\right)\right) \\
& = - 3 \pi + \frac{63 \sqrt{3}}{4}
\end{aligned}
$$


## Generated authored operation bank

### q-83958 — moderate

Evaluate $\int_{0}^{\frac{\pi}{3}} \int_{4 - 4 \cos{\left(\theta \right)}}^{4} 4 r\,\mathrm d r\,\mathrm d \theta.$

- A. $- \frac{32 \pi}{3} + 56 \sqrt{3}$
- B. $- \frac{128 \pi}{3} + 128 \sqrt{3}$
- C. $- \frac{8 \pi}{3} + 14 \sqrt{3}$
- D. $- \frac{16 \pi}{3} + 28 \sqrt{3}$ **correct**
- E. $- 28 \sqrt{3} + \frac{16 \pi}{3}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{3}} \int_{4 - 4 \cos{\left(\theta \right)}}^{4} 4 r\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{3}} 4 \int_{4 - 4 \cos{\left(\theta \right)}}^{4} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 4 \left[\frac{r^{2}}{2}\right]_{4 - 4 \cos{\left(\theta \right)}}^{4}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} 4 \left(\frac{\left(4\right)^{2}-\left(4 - 4 \cos{\left(\theta \right)}\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{3}} - 32 \cos^{2}{\left(\theta \right)} + 64 \cos{\left(\theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{3}} - 32 \cos^{2}{\left(\theta \right)} + 64 \cos{\left(\theta \right)}\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{3}} 32\left(2\cos\theta-\frac{1+\cos(2\theta)}{2}\right)\,\mathrm d \theta \\
& = \left[- 16 \theta + 64 \sin{\left(\theta \right)} - 8 \sin{\left(2 \theta \right)}\right]_{0}^{\frac{\pi}{3}} \\
& = \left(\left(- 16 \left(\frac{\pi}{3}\right)\right)+\left(- 8 \sin{\left(2 \left(\frac{\pi}{3}\right) \right)}\right)+\left(64 \sin{\left(\left(\frac{\pi}{3}\right) \right)}\right)\right)-\left(\left(- 16 \left(0\right)\right)+\left(- 8 \sin{\left(2 \left(0\right) \right)}\right)+\left(64 \sin{\left(\left(0\right) \right)}\right)\right) \\
& = \left(\left(- \frac{16 \pi}{3}\right)+\left(- 4 \sqrt{3}\right)+\left(32 \sqrt{3}\right)\right)-\left(\left(0\right)+\left(0\right)+\left(0\right)\right) \\
& = - \frac{16 \pi}{3} + 28 \sqrt{3}
\end{aligned}
$$


## Generated authored operation bank

### q-83514 — moderate

Evaluate $\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \int_{\csc{\left(\theta \right)}}^{2} 4 r\,\mathrm d r\,\mathrm d \theta.$

- A. $- \frac{8 \sqrt{3}}{3} + 4 \pi$ **correct**
- B. $- \frac{16 \sqrt{3}}{3} + 8 \pi$
- C. $- 4 \pi + \frac{8 \sqrt{3}}{3}$
- D. $4 \pi$
- E. $- \frac{7 \sqrt{3}}{3} + \frac{4 \pi}{3}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \int_{\csc{\left(\theta \right)}}^{2} 4 r\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} 4 \int_{\csc{\left(\theta \right)}}^{2} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} 4 \left[\frac{r^{2}}{2}\right]_{\csc{\left(\theta \right)}}^{2}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} 4 \left(\frac{\left(2\right)^{2}-\left(\csc{\left(\theta \right)}\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} 8 - 2 \csc^{2}{\left(\theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} 8 - 2 \csc^{2}{\left(\theta \right)}\,\mathrm d \theta & = \left[8 \theta + 2 \cot{\left(\theta \right)}\right]_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \\
& = \left(\left(2 \cot{\left(\left(\frac{2 \pi}{3}\right) \right)}\right)+\left(8 \left(\frac{2 \pi}{3}\right)\right)\right)-\left(\left(2 \cot{\left(\left(\frac{\pi}{6}\right) \right)}\right)+\left(8 \left(\frac{\pi}{6}\right)\right)\right) \\
& = \left(\left(- \frac{2 \sqrt{3}}{3}\right)+\left(\frac{16 \pi}{3}\right)\right)-\left(\left(2 \sqrt{3}\right)+\left(\frac{4 \pi}{3}\right)\right) \\
& = - \frac{8 \sqrt{3}}{3} + 4 \pi
\end{aligned}
$$


## Generated authored operation bank

### q-83514 — moderate

Evaluate $\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \int_{\csc{\left(\theta \right)}}^{2} 4 r\,\mathrm d r\,\mathrm d \theta.$

- A. $- \frac{16 \sqrt{3}}{3} + 8 \pi$
- B. $- 4 \pi + \frac{8 \sqrt{3}}{3}$
- C. $4 \pi$
- D. $- \frac{7 \sqrt{3}}{3} + \frac{4 \pi}{3}$
- E. $- \frac{8 \sqrt{3}}{3} + 4 \pi$ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \int_{\csc{\left(\theta \right)}}^{2} 4 r\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} 4 \int_{\csc{\left(\theta \right)}}^{2} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} 4 \left[\frac{r^{2}}{2}\right]_{\csc{\left(\theta \right)}}^{2}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} 4 \left(\frac{\left(2\right)^{2}-\left(\csc{\left(\theta \right)}\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} 8 - 2 \csc^{2}{\left(\theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} 8 - 2 \csc^{2}{\left(\theta \right)}\,\mathrm d \theta & = \left[8 \theta + 2 \cot{\left(\theta \right)}\right]_{\frac{\pi}{6}}^{\frac{2 \pi}{3}} \\
& = \left(\left(2 \cot{\left(\left(\frac{2 \pi}{3}\right) \right)}\right)+\left(8 \left(\frac{2 \pi}{3}\right)\right)\right)-\left(\left(2 \cot{\left(\left(\frac{\pi}{6}\right) \right)}\right)+\left(8 \left(\frac{\pi}{6}\right)\right)\right) \\
& = \left(\left(- \frac{2 \sqrt{3}}{3}\right)+\left(\frac{16 \pi}{3}\right)\right)-\left(\left(2 \sqrt{3}\right)+\left(\frac{4 \pi}{3}\right)\right) \\
& = - \frac{8 \sqrt{3}}{3} + 4 \pi
\end{aligned}
$$


## Generated authored operation bank

### q-161048 — easy

Evaluate $\int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \int_{1}^{2} 4 r^{2} \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $- \frac{14 \sqrt{2}}{3} - \frac{14}{3}$
- B. $\frac{14}{3} + \frac{14 \sqrt{2}}{3}$ **correct**
- C. $14 + 14 \sqrt{2}$
- D. $\frac{15}{2} + \frac{15 \sqrt{2}}{2}$
- E. $\frac{7 \sqrt{2}}{3} + \frac{14}{3}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \int_{1}^{2} 4 r^{2} \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} 4 \sin{\left(\theta \right)} \int_{1}^{2} r^{2}\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} 4 \sin{\left(\theta \right)} \left[\frac{r^{3}}{3}\right]_{1}^{2}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} 4 \sin{\left(\theta \right)} \left(\frac{\left(2\right)^{3}-\left(1\right)^{3}}{3}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \frac{28 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \frac{28 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta & = \left[- \frac{28 \cos{\left(\theta \right)}}{3}\right]_{\frac{\pi}{3}}^{\frac{3 \pi}{4}} \\
& = \left(\left(- \frac{28 \cos{\left(\left(\frac{3 \pi}{4}\right) \right)}}{3}\right)\right)-\left(\left(- \frac{28 \cos{\left(\left(\frac{\pi}{3}\right) \right)}}{3}\right)\right) \\
& = \left(\left(\frac{14 \sqrt{2}}{3}\right)\right)-\left(\left(- \frac{14}{3}\right)\right) \\
& = \frac{14}{3} + \frac{14 \sqrt{2}}{3}
\end{aligned}
$$


## Generated authored operation bank

### q-161048 — easy

Evaluate $\int_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \int_{2}^{3} r^{2} \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $\frac{65 \sqrt{2}}{8} + \frac{65 \sqrt{3}}{8}$
- B. $- \frac{19 \sqrt{3}}{6} - \frac{19 \sqrt{2}}{6}$
- C. $\frac{19 \sqrt{2}}{2} + \frac{19 \sqrt{3}}{2}$
- D. $\frac{19 \sqrt{2}}{12} + \frac{19 \sqrt{3}}{6}$
- E. $\frac{19 \sqrt{2}}{6} + \frac{19 \sqrt{3}}{6}$ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \int_{2}^{3} r^{2} \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \sin{\left(\theta \right)} \int_{2}^{3} r^{2}\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \sin{\left(\theta \right)} \left[\frac{r^{3}}{3}\right]_{2}^{3}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \sin{\left(\theta \right)} \left(\frac{\left(3\right)^{3}-\left(2\right)^{3}}{3}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \frac{19 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \frac{19 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta & = \left[- \frac{19 \cos{\left(\theta \right)}}{3}\right]_{\frac{\pi}{6}}^{\frac{3 \pi}{4}} \\
& = \left(\left(- \frac{19 \cos{\left(\left(\frac{3 \pi}{4}\right) \right)}}{3}\right)\right)-\left(\left(- \frac{19 \cos{\left(\left(\frac{\pi}{6}\right) \right)}}{3}\right)\right) \\
& = \left(\left(\frac{19 \sqrt{2}}{6}\right)\right)-\left(\left(- \frac{19 \sqrt{3}}{6}\right)\right) \\
& = \frac{19 \sqrt{2}}{6} + \frac{19 \sqrt{3}}{6}
\end{aligned}
$$


## Generated authored operation bank

### q-83966 — moderate

Evaluate $\int_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} \int_{1}^{3 \cos{\left(\theta \right)}} 4 r \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $- \frac{5 \sqrt{3}}{4} - \frac{1}{4}$ **correct**
- B. $- \frac{5 \sqrt{3}}{2} - \frac{1}{2}$
- C. $- \frac{5 \sqrt{3}}{8} - \frac{1}{4}$
- D. $- \frac{31}{6} + \frac{2 \sqrt{3}}{3}$
- E. $\frac{1}{4} + \frac{5 \sqrt{3}}{4}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} \int_{1}^{3 \cos{\left(\theta \right)}} 4 r \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} 4 \sin{\left(\theta \right)} \int_{1}^{3 \cos{\left(\theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} 4 \sin{\left(\theta \right)} \left[\frac{r^{2}}{2}\right]_{1}^{3 \cos{\left(\theta \right)}}\,\mathrm d \theta \\
& = \int_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} 4 \sin{\left(\theta \right)} \left(\frac{\left(3 \cos{\left(\theta \right)}\right)^{2}-\left(1\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} 18 \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 \sin{\left(\theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} 18 \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 \sin{\left(\theta \right)}\,\mathrm d \theta & = \left[- 6 \cos^{3}{\left(\theta \right)} + 2 \cos{\left(\theta \right)}\right]_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} \\
& = \left(\left(- 6 \cos^{3}{\left(\left(\frac{11 \pi}{6}\right) \right)}\right)+\left(2 \cos{\left(\left(\frac{11 \pi}{6}\right) \right)}\right)\right)-\left(\left(- 6 \cos^{3}{\left(\left(\frac{5 \pi}{3}\right) \right)}\right)+\left(2 \cos{\left(\left(\frac{5 \pi}{3}\right) \right)}\right)\right) \\
& = \left(\left(- \frac{9 \sqrt{3}}{4}\right)+\left(\sqrt{3}\right)\right)-\left(\left(- \frac{3}{4}\right)+\left(1\right)\right) \\
& = - \frac{5 \sqrt{3}}{4} - \frac{1}{4}
\end{aligned}
$$


## Generated authored operation bank

### q-83966 — moderate

Evaluate $\int_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} \int_{1}^{4 \cos{\left(\theta \right)}} 4 r \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta.$

- A. $\frac{2}{3} - 6 \sqrt{3}$
- B. $- \frac{34}{3} + \frac{2 \sqrt{3}}{3}$
- C. $\frac{1}{3} - \frac{3 \sqrt{3}}{2}$
- D. $\frac{1}{3} - 3 \sqrt{3}$ **correct**
- E. $- \frac{1}{3} + 3 \sqrt{3}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} \int_{1}^{4 \cos{\left(\theta \right)}} 4 r \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} 4 \sin{\left(\theta \right)} \int_{1}^{4 \cos{\left(\theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} 4 \sin{\left(\theta \right)} \left[\frac{r^{2}}{2}\right]_{1}^{4 \cos{\left(\theta \right)}}\,\mathrm d \theta \\
& = \int_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} 4 \sin{\left(\theta \right)} \left(\frac{\left(4 \cos{\left(\theta \right)}\right)^{2}-\left(1\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} 32 \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 \sin{\left(\theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} 32 \sin{\left(\theta \right)} \cos^{2}{\left(\theta \right)} - 2 \sin{\left(\theta \right)}\,\mathrm d \theta & = \left[- \frac{32 \cos^{3}{\left(\theta \right)}}{3} + 2 \cos{\left(\theta \right)}\right]_{\frac{5 \pi}{3}}^{\frac{11 \pi}{6}} \\
& = \left(\left(2 \cos{\left(\left(\frac{11 \pi}{6}\right) \right)}\right)+\left(- \frac{32 \cos^{3}{\left(\left(\frac{11 \pi}{6}\right) \right)}}{3}\right)\right)-\left(\left(2 \cos{\left(\left(\frac{5 \pi}{3}\right) \right)}\right)+\left(- \frac{32 \cos^{3}{\left(\left(\frac{5 \pi}{3}\right) \right)}}{3}\right)\right) \\
& = \left(\left(\sqrt{3}\right)+\left(- 4 \sqrt{3}\right)\right)-\left(\left(1\right)+\left(- \frac{4}{3}\right)\right) \\
& = \frac{1}{3} - 3 \sqrt{3}
\end{aligned}
$$


## Generated authored operation bank

### sine_double_partial — hard

Evaluate $\int_{0}^{\frac{\pi}{12}} \int_{0}^{3 \sin{\left(2 \theta \right)}} 4 r\,\mathrm d r\,\mathrm d \theta.$

- A. $- \frac{9 \sqrt{3}}{8} + \frac{3 \pi}{4}$ **correct**
- B. $- \frac{9 \sqrt{3}}{16} + \frac{3 \pi}{8}$
- C. $12 - \frac{27 \sqrt{3}}{4}$
- D. $- \frac{3 \pi}{4} + \frac{9 \sqrt{3}}{8}$
- E. $- \frac{9 \sqrt{3}}{4} + \frac{3 \pi}{2}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{12}} \int_{0}^{3 \sin{\left(2 \theta \right)}} 4 r\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{12}} 4 \int_{0}^{3 \sin{\left(2 \theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 4 \left[\frac{r^{2}}{2}\right]_{0}^{3 \sin{\left(2 \theta \right)}}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 4 \left(\frac{\left(3 \sin{\left(2 \theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 18 \sin^{2}{\left(2 \theta \right)}\,\mathrm d \theta
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
\int_{0}^{\frac{\pi}{12}} 18 \sin^{2}{\left(2 \theta \right)}\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{12}} 9\left(1-\cos\left(4\theta\right)\right)\,\mathrm d \theta \\
& = 9\left[\theta - \frac{\sin{\left(4 \theta \right)}}{4}\right]_{0}^{\frac{\pi}{12}} \\
& = 9\left(\left(\frac{\pi}{12}-\frac{1}{4}\sin\left(\frac{\pi}{3}\right)\right)-\left(0-\frac{1}{4}\sin\left(0\right)\right)\right) \\
& = 9\left(\left(\frac{\pi}{12}-\frac{1}{4} \left(\frac{\sqrt{3}}{2}\right)\right)-\left(0-\frac{1}{4} \left(0\right)\right)\right) \\
& = 9\left(\left(\frac{\pi}{12}\right)-\frac{1}{4}\left(\frac{\sqrt{3}}{2}\right)\right) \\
& = - \frac{9 \sqrt{3}}{8} + \frac{3 \pi}{4}
\end{aligned}
$$


## Generated authored operation bank

### sine_double_partial — hard

Evaluate $\int_{0}^{\frac{\pi}{12}} \int_{0}^{4 \sin{\left(2 \theta \right)}} 4 r\,\mathrm d r\,\mathrm d \theta.$

- A. $- \sqrt{3} + \frac{2 \pi}{3}$
- B. $\frac{256}{9} - 16 \sqrt{3}$
- C. $- 2 \sqrt{3} + \frac{4 \pi}{3}$ **correct**
- D. $- \frac{4 \pi}{3} + 2 \sqrt{3}$
- E. $- 4 \sqrt{3} + \frac{8 \pi}{3}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{12}} \int_{0}^{4 \sin{\left(2 \theta \right)}} 4 r\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{12}} 4 \int_{0}^{4 \sin{\left(2 \theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 4 \left[\frac{r^{2}}{2}\right]_{0}^{4 \sin{\left(2 \theta \right)}}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 4 \left(\frac{\left(4 \sin{\left(2 \theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 32 \sin^{2}{\left(2 \theta \right)}\,\mathrm d \theta
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
\int_{0}^{\frac{\pi}{12}} 32 \sin^{2}{\left(2 \theta \right)}\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{12}} 16\left(1-\cos\left(4\theta\right)\right)\,\mathrm d \theta \\
& = 16\left[\theta - \frac{\sin{\left(4 \theta \right)}}{4}\right]_{0}^{\frac{\pi}{12}} \\
& = 16\left(\left(\frac{\pi}{12}-\frac{1}{4}\sin\left(\frac{\pi}{3}\right)\right)-\left(0-\frac{1}{4}\sin\left(0\right)\right)\right) \\
& = 16\left(\left(\frac{\pi}{12}-\frac{1}{4} \left(\frac{\sqrt{3}}{2}\right)\right)-\left(0-\frac{1}{4} \left(0\right)\right)\right) \\
& = 16\left(\left(\frac{\pi}{12}\right)-\frac{1}{4}\left(\frac{\sqrt{3}}{2}\right)\right) \\
& = - 2 \sqrt{3} + \frac{4 \pi}{3}
\end{aligned}
$$


## Generated authored operation bank

### cosine_double_partial — hard

Evaluate $\int_{0}^{\frac{\pi}{12}} \int_{0}^{3 \cos{\left(2 \theta \right)}} 4 r\,\mathrm d r\,\mathrm d \theta.$

- A. $\frac{9 \sqrt{3}}{8} + \frac{3 \pi}{4}$ **correct**
- B. $\frac{9 \sqrt{3}}{16} + \frac{3 \pi}{8}$
- C. $\frac{33}{4}$
- D. $- \frac{3 \pi}{4} - \frac{9 \sqrt{3}}{8}$
- E. $\frac{9 \sqrt{3}}{4} + \frac{3 \pi}{2}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{12}} \int_{0}^{3 \cos{\left(2 \theta \right)}} 4 r\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{12}} 4 \int_{0}^{3 \cos{\left(2 \theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 4 \left[\frac{r^{2}}{2}\right]_{0}^{3 \cos{\left(2 \theta \right)}}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 4 \left(\frac{\left(3 \cos{\left(2 \theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 18 \cos^{2}{\left(2 \theta \right)}\,\mathrm d \theta
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
\int_{0}^{\frac{\pi}{12}} 18 \cos^{2}{\left(2 \theta \right)}\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{12}} 9\left(1+\cos\left(4\theta\right)\right)\,\mathrm d \theta \\
& = 9\left[\theta + \frac{\sin{\left(4 \theta \right)}}{4}\right]_{0}^{\frac{\pi}{12}} \\
& = 9\left(\left(\frac{\pi}{12}+\frac{1}{4}\sin\left(\frac{\pi}{3}\right)\right)-\left(0+\frac{1}{4}\sin\left(0\right)\right)\right) \\
& = 9\left(\left(\frac{\pi}{12}+\frac{1}{4} \left(\frac{\sqrt{3}}{2}\right)\right)-\left(0+\frac{1}{4} \left(0\right)\right)\right) \\
& = 9\left(\left(\frac{\pi}{12}\right)+\frac{1}{4}\left(\frac{\sqrt{3}}{2}\right)\right) \\
& = \frac{9 \sqrt{3}}{8} + \frac{3 \pi}{4}
\end{aligned}
$$


## Generated authored operation bank

### cosine_double_partial — hard

Evaluate $\int_{0}^{\frac{\pi}{12}} \int_{0}^{4 \cos{\left(2 \theta \right)}} 4 r\,\mathrm d r\,\mathrm d \theta.$

- A. $\sqrt{3} + \frac{2 \pi}{3}$
- B. $\frac{176}{9}$
- C. $2 \sqrt{3} + \frac{4 \pi}{3}$ **correct**
- D. $- \frac{4 \pi}{3} - 2 \sqrt{3}$
- E. $4 \sqrt{3} + \frac{8 \pi}{3}$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{0}^{\frac{\pi}{12}} \int_{0}^{4 \cos{\left(2 \theta \right)}} 4 r\,\mathrm d r\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{12}} 4 \int_{0}^{4 \cos{\left(2 \theta \right)}} r\,\mathrm d r\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 4 \left[\frac{r^{2}}{2}\right]_{0}^{4 \cos{\left(2 \theta \right)}}\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 4 \left(\frac{\left(4 \cos{\left(2 \theta \right)}\right)^{2}-\left(0\right)^{2}}{2}\right)\,\mathrm d \theta \\
& = \int_{0}^{\frac{\pi}{12}} 32 \cos^{2}{\left(2 \theta \right)}\,\mathrm d \theta
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
\int_{0}^{\frac{\pi}{12}} 32 \cos^{2}{\left(2 \theta \right)}\,\mathrm d \theta & = \int_{0}^{\frac{\pi}{12}} 16\left(1+\cos\left(4\theta\right)\right)\,\mathrm d \theta \\
& = 16\left[\theta + \frac{\sin{\left(4 \theta \right)}}{4}\right]_{0}^{\frac{\pi}{12}} \\
& = 16\left(\left(\frac{\pi}{12}+\frac{1}{4}\sin\left(\frac{\pi}{3}\right)\right)-\left(0+\frac{1}{4}\sin\left(0\right)\right)\right) \\
& = 16\left(\left(\frac{\pi}{12}+\frac{1}{4} \left(\frac{\sqrt{3}}{2}\right)\right)-\left(0+\frac{1}{4} \left(0\right)\right)\right) \\
& = 16\left(\left(\frac{\pi}{12}\right)+\frac{1}{4}\left(\frac{\sqrt{3}}{2}\right)\right) \\
& = 2 \sqrt{3} + \frac{4 \pi}{3}
\end{aligned}
$$


## Generated observed-profile scalar variant

### q-38031 — moderate

Evaluate 
$2\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{sin}⁡\theta }2r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $2\left(2\right)$
- B. $2\left(1\right)$
- C. $2\left(2\pi\right) $
- D. $2\left(\frac{1}{3}\right)$ **correct**
- E. $2\left(\frac{2}{3}\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}2\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{sin}⁡\theta }2r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =2\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {\int }_{0}^{\operatorname{sin}⁡\theta }2r\,\text{d}r\,\text{d}\theta\right)  \\  & =2\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \,[{r}^{2}]_{0}^{\operatorname{sin}⁡\theta }\,\text{d}\theta\right)  \\  & =2\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}2\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}\theta\right)  & =2\left(\frac{1}{3}{[{sin}^{3}⁡\theta ]}_{0}^{\pi /2}\right) \\  & =2\left(\frac{1}{3}[{1}^{3}-{0}^{3}]\right) \\  & =2\left(\frac{1}{3}\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-38031 — moderate

Evaluate 
$3\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{sin}⁡\theta }2r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $3\left(\frac{2}{3}\right)$
- B. $3\left(2\right)$
- C. $3\left(2\pi\right) $
- D. $3\left(\frac{1}{3}\right)$ **correct**
- E. $3\left(1\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}3\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{sin}⁡\theta }2r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =3\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {\int }_{0}^{\operatorname{sin}⁡\theta }2r\,\text{d}r\,\text{d}\theta\right)  \\  & =3\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \,[{r}^{2}]_{0}^{\operatorname{sin}⁡\theta }\,\text{d}\theta\right)  \\  & =3\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}3\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}\theta\right)  & =3\left(\frac{1}{3}{[{sin}^{3}⁡\theta ]}_{0}^{\pi /2}\right) \\  & =3\left(\frac{1}{3}[{1}^{3}-{0}^{3}]\right) \\  & =3\left(\frac{1}{3}\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-38031 — moderate

Evaluate 
$4\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{sin}⁡\theta }2r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $4\left(2\pi\right) $
- B. $4\left(\frac{1}{3}\right)$ **correct**
- C. $4\left(\frac{2}{3}\right)$
- D. $4\left(2\right)$
- E. $4\left(1\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}4\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{sin}⁡\theta }2r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =4\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {\int }_{0}^{\operatorname{sin}⁡\theta }2r\,\text{d}r\,\text{d}\theta\right)  \\  & =4\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \,[{r}^{2}]_{0}^{\operatorname{sin}⁡\theta }\,\text{d}\theta\right)  \\  & =4\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}4\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}\theta\right)  & =4\left(\frac{1}{3}{[{sin}^{3}⁡\theta ]}_{0}^{\pi /2}\right) \\  & =4\left(\frac{1}{3}[{1}^{3}-{0}^{3}]\right) \\  & =4\left(\frac{1}{3}\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-38031 — moderate

Evaluate 
$5\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{sin}⁡\theta }2r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $5\left(\frac{2}{3}\right)$
- B. $5\left(1\right)$
- C. $5\left(2\pi\right) $
- D. $5\left(2\right)$
- E. $5\left(\frac{1}{3}\right)$ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}5\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{sin}⁡\theta }2r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =5\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {\int }_{0}^{\operatorname{sin}⁡\theta }2r\,\text{d}r\,\text{d}\theta\right)  \\  & =5\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \,[{r}^{2}]_{0}^{\operatorname{sin}⁡\theta }\,\text{d}\theta\right)  \\  & =5\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}5\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta {sin}^{2}⁡\theta \,\text{d}\theta\right)  & =5\left(\frac{1}{3}{[{sin}^{3}⁡\theta ]}_{0}^{\pi /2}\right) \\  & =5\left(\frac{1}{3}[{1}^{3}-{0}^{3}]\right) \\  & =5\left(\frac{1}{3}\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-38127 — easy

What is $2\left(\displaystyle \int_{π/3}^{π/2}\displaystyle \int_{1}^{2}r^{2}\sin θdrdθ\right)$?

- A. $2\left(\frac{π}{5}\right)$
- B. $2\left(\frac{7}{6}\right)$ **correct**
- C. $2\left(- π\right)$
- D. $2\left(4\right)$
- E. $2\left(-\frac{2}{3}\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \int_{1}^{2} 2 r^{2} \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 2 \sin{\left(\theta \right)} \int_{1}^{2} r^{2}\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 2 \sin{\left(\theta \right)} \left[\frac{r^{3}}{3}\right]_{1}^{2}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 2 \sin{\left(\theta \right)} \left(\frac{\left(2\right)^{3}-\left(1\right)^{3}}{3}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \frac{14 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \frac{14 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta & = \left[- \frac{14 \cos{\left(\theta \right)}}{3}\right]_{\frac{\pi}{3}}^{\frac{\pi}{2}} \\
& = \left(\left(- \frac{14 \cos{\left(\left(\frac{\pi}{2}\right) \right)}}{3}\right)\right)-\left(\left(- \frac{14 \cos{\left(\left(\frac{\pi}{3}\right) \right)}}{3}\right)\right) \\
& = \left(\left(0\right)\right)-\left(\left(- \frac{7}{3}\right)\right) \\
& = \frac{7}{3}
\end{aligned}
$$


## Generated observed-profile scalar variant

### q-38127 — easy

What is $3\left(\displaystyle \int_{π/3}^{π/2}\displaystyle \int_{1}^{2}r^{2}\sin θdrdθ\right)$?

- A. $3\left(-\frac{2}{3}\right)$
- B. $3\left(\frac{π}{5}\right)$
- C. $3\left(- π\right)$
- D. $3\left(4\right)$
- E. $3\left(\frac{7}{6}\right)$ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \int_{1}^{2} 3 r^{2} \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 3 \sin{\left(\theta \right)} \int_{1}^{2} r^{2}\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 3 \sin{\left(\theta \right)} \left[\frac{r^{3}}{3}\right]_{1}^{2}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 3 \sin{\left(\theta \right)} \left(\frac{\left(2\right)^{3}-\left(1\right)^{3}}{3}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 7 \sin{\left(\theta \right)}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 7 \sin{\left(\theta \right)}\,\mathrm d \theta & = \left[- 7 \cos{\left(\theta \right)}\right]_{\frac{\pi}{3}}^{\frac{\pi}{2}} \\
& = \left(\left(- 7 \cos{\left(\left(\frac{\pi}{2}\right) \right)}\right)\right)-\left(\left(- 7 \cos{\left(\left(\frac{\pi}{3}\right) \right)}\right)\right) \\
& = \left(\left(0\right)\right)-\left(\left(- \frac{7}{2}\right)\right) \\
& = \frac{7}{2}
\end{aligned}
$$


## Generated observed-profile scalar variant

### q-38127 — easy

What is $4\left(\displaystyle \int_{π/3}^{π/2}\displaystyle \int_{1}^{2}r^{2}\sin θdrdθ\right)$?

- A. $4\left(- π\right)$
- B. $4\left(4\right)$
- C. $4\left(-\frac{2}{3}\right)$
- D. $4\left(\frac{π}{5}\right)$
- E. $4\left(\frac{7}{6}\right)$ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \int_{1}^{2} 4 r^{2} \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 4 \sin{\left(\theta \right)} \int_{1}^{2} r^{2}\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 4 \sin{\left(\theta \right)} \left[\frac{r^{3}}{3}\right]_{1}^{2}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 4 \sin{\left(\theta \right)} \left(\frac{\left(2\right)^{3}-\left(1\right)^{3}}{3}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \frac{28 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \frac{28 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta & = \left[- \frac{28 \cos{\left(\theta \right)}}{3}\right]_{\frac{\pi}{3}}^{\frac{\pi}{2}} \\
& = \left(\left(- \frac{28 \cos{\left(\left(\frac{\pi}{2}\right) \right)}}{3}\right)\right)-\left(\left(- \frac{28 \cos{\left(\left(\frac{\pi}{3}\right) \right)}}{3}\right)\right) \\
& = \left(\left(0\right)\right)-\left(\left(- \frac{14}{3}\right)\right) \\
& = \frac{14}{3}
\end{aligned}
$$


## Generated observed-profile scalar variant

### q-38127 — easy

What is $5\left(\displaystyle \int_{π/3}^{π/2}\displaystyle \int_{1}^{2}r^{2}\sin θdrdθ\right)$?

- A. $5\left(-\frac{2}{3}\right)$
- B. $5\left(\frac{7}{6}\right)$ **correct**
- C. $5\left(- π\right)$
- D. $5\left(\frac{π}{5}\right)$
- E. $5\left(4\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \int_{1}^{2} 5 r^{2} \sin{\left(\theta \right)}\,\mathrm d r\,\mathrm d \theta & = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 5 \sin{\left(\theta \right)} \int_{1}^{2} r^{2}\,\mathrm d r\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 5 \sin{\left(\theta \right)} \left[\frac{r^{3}}{3}\right]_{1}^{2}\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 5 \sin{\left(\theta \right)} \left(\frac{\left(2\right)^{3}-\left(1\right)^{3}}{3}\right)\,\mathrm d \theta \\
& = \int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \frac{35 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta
\end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}
\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \frac{35 \sin{\left(\theta \right)}}{3}\,\mathrm d \theta & = \left[- \frac{35 \cos{\left(\theta \right)}}{3}\right]_{\frac{\pi}{3}}^{\frac{\pi}{2}} \\
& = \left(\left(- \frac{35 \cos{\left(\left(\frac{\pi}{2}\right) \right)}}{3}\right)\right)-\left(\left(- \frac{35 \cos{\left(\left(\frac{\pi}{3}\right) \right)}}{3}\right)\right) \\
& = \left(\left(0\right)\right)-\left(\left(- \frac{35}{6}\right)\right) \\
& = \frac{35}{6}
\end{aligned}
$$


## Generated observed-profile scalar variant

### q-161049 — moderate

Evaluate 
$2\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{cos}⁡\theta }3r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $2\left(1\right)$ **correct**
- B. $2\left(\frac{1}{2}\right)$
- C. $2\left(\frac{3}{2}\right)$
- D. $2\left(3\right)$
- E. $2\left(2\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}2\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{cos}⁡\theta }3r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =2\left({\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta {\int }_{0}^{\operatorname{cos}⁡\theta }r\,\text{d}r\,\text{d}\theta\right)  \\  & =2\left({\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta \,{[\frac{{r}^{2}}{2}]}_{0}^{\operatorname{cos}⁡\theta }\,\text{d}\theta\right)  \\  & =2\left({\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta \,(\frac{{cos}^{2}⁡\theta }{2}-0)\,\text{d}\theta\right)  \\  & =2\left(\frac{3}{2}{\int }_{0}^{\pi /2}{cos}^{3}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}2\left(\frac{3}{2}{\int }_{0}^{\pi /2}{cos}^{3}⁡\theta \,\text{d}\theta\right)  & =2\left(\frac{3}{2}{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta (1-{sin}^{2}⁡\theta )\,\text{d}\theta\right)  \\  & =2\left(\frac{3}{2}{[\operatorname{sin}⁡\theta -\frac{{sin}^{3}⁡\theta }{3}]}_{0}^{\pi /2}\right) \\  & =2\left(\frac{3}{2}[(\operatorname{sin}⁡\frac{\pi }{2}-\frac{1}{3}{sin}^{3}⁡\frac{\pi }{2})-(\operatorname{sin}⁡0-\frac{1}{3}{sin}^{3}⁡0)]\right) \\  & =2\left(\frac{3}{2}[(1-\frac{1}{3})-0]\right) \\  & =2\left(1\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-161049 — moderate

Evaluate 
$3\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{cos}⁡\theta }3r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $3\left(2\right)$
- B. $3\left(1\right)$ **correct**
- C. $3\left(\frac{3}{2}\right)$
- D. $3\left(3\right)$
- E. $3\left(\frac{1}{2}\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}3\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{cos}⁡\theta }3r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =3\left({\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta {\int }_{0}^{\operatorname{cos}⁡\theta }r\,\text{d}r\,\text{d}\theta\right)  \\  & =3\left({\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta \,{[\frac{{r}^{2}}{2}]}_{0}^{\operatorname{cos}⁡\theta }\,\text{d}\theta\right)  \\  & =3\left({\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta \,(\frac{{cos}^{2}⁡\theta }{2}-0)\,\text{d}\theta\right)  \\  & =3\left(\frac{3}{2}{\int }_{0}^{\pi /2}{cos}^{3}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}3\left(\frac{3}{2}{\int }_{0}^{\pi /2}{cos}^{3}⁡\theta \,\text{d}\theta\right)  & =3\left(\frac{3}{2}{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta (1-{sin}^{2}⁡\theta )\,\text{d}\theta\right)  \\  & =3\left(\frac{3}{2}{[\operatorname{sin}⁡\theta -\frac{{sin}^{3}⁡\theta }{3}]}_{0}^{\pi /2}\right) \\  & =3\left(\frac{3}{2}[(\operatorname{sin}⁡\frac{\pi }{2}-\frac{1}{3}{sin}^{3}⁡\frac{\pi }{2})-(\operatorname{sin}⁡0-\frac{1}{3}{sin}^{3}⁡0)]\right) \\  & =3\left(\frac{3}{2}[(1-\frac{1}{3})-0]\right) \\  & =3\left(1\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-161049 — moderate

Evaluate 
$4\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{cos}⁡\theta }3r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $4\left(\frac{3}{2}\right)$
- B. $4\left(3\right)$
- C. $4\left(2\right)$
- D. $4\left(1\right)$ **correct**
- E. $4\left(\frac{1}{2}\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}4\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{cos}⁡\theta }3r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =4\left({\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta {\int }_{0}^{\operatorname{cos}⁡\theta }r\,\text{d}r\,\text{d}\theta\right)  \\  & =4\left({\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta \,{[\frac{{r}^{2}}{2}]}_{0}^{\operatorname{cos}⁡\theta }\,\text{d}\theta\right)  \\  & =4\left({\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta \,(\frac{{cos}^{2}⁡\theta }{2}-0)\,\text{d}\theta\right)  \\  & =4\left(\frac{3}{2}{\int }_{0}^{\pi /2}{cos}^{3}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}4\left(\frac{3}{2}{\int }_{0}^{\pi /2}{cos}^{3}⁡\theta \,\text{d}\theta\right)  & =4\left(\frac{3}{2}{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta (1-{sin}^{2}⁡\theta )\,\text{d}\theta\right)  \\  & =4\left(\frac{3}{2}{[\operatorname{sin}⁡\theta -\frac{{sin}^{3}⁡\theta }{3}]}_{0}^{\pi /2}\right) \\  & =4\left(\frac{3}{2}[(\operatorname{sin}⁡\frac{\pi }{2}-\frac{1}{3}{sin}^{3}⁡\frac{\pi }{2})-(\operatorname{sin}⁡0-\frac{1}{3}{sin}^{3}⁡0)]\right) \\  & =4\left(\frac{3}{2}[(1-\frac{1}{3})-0]\right) \\  & =4\left(1\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-161049 — moderate

Evaluate 
$5\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{cos}⁡\theta }3r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $5\left(2\right)$
- B. $5\left(\frac{1}{2}\right)$
- C. $5\left(\frac{3}{2}\right)$
- D. $5\left(1\right)$ **correct**
- E. $5\left(3\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}5\left({\int }_{0}^{\pi /2}{\int }_{0}^{\operatorname{cos}⁡\theta }3r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =5\left({\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta {\int }_{0}^{\operatorname{cos}⁡\theta }r\,\text{d}r\,\text{d}\theta\right)  \\  & =5\left({\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta \,{[\frac{{r}^{2}}{2}]}_{0}^{\operatorname{cos}⁡\theta }\,\text{d}\theta\right)  \\  & =5\left({\int }_{0}^{\pi /2}3\operatorname{cos}⁡\theta \,(\frac{{cos}^{2}⁡\theta }{2}-0)\,\text{d}\theta\right)  \\  & =5\left(\frac{3}{2}{\int }_{0}^{\pi /2}{cos}^{3}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}5\left(\frac{3}{2}{\int }_{0}^{\pi /2}{cos}^{3}⁡\theta \,\text{d}\theta\right)  & =5\left(\frac{3}{2}{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta (1-{sin}^{2}⁡\theta )\,\text{d}\theta\right)  \\  & =5\left(\frac{3}{2}{[\operatorname{sin}⁡\theta -\frac{{sin}^{3}⁡\theta }{3}]}_{0}^{\pi /2}\right) \\  & =5\left(\frac{3}{2}[(\operatorname{sin}⁡\frac{\pi }{2}-\frac{1}{3}{sin}^{3}⁡\frac{\pi }{2})-(\operatorname{sin}⁡0-\frac{1}{3}{sin}^{3}⁡0)]\right) \\  & =5\left(\frac{3}{2}[(1-\frac{1}{3})-0]\right) \\  & =5\left(1\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-38133 — easy

$2\left({\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta\right) =$

- A. $2\left(\frac{\sqrt{3}}{2}\right)$
- B. $2\left(\pi\right) $ **correct**
- C. $2\left(2\pi\right) $
- D. $2\left(\pi +4\right)$
- E. $2\left(\frac{\pi }{4}\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}2\left({\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta\right)  & =2\left({\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta\right)  \\  & =2\left({\int }_{-\pi /2}^{\pi /2}{[\frac{{r}^{2}}{2}]}_{0}^{2\operatorname{cos}⁡(2\theta )}\,\text{d}\theta\right)  \\  & =2\left({\int }_{-\pi /2}^{\pi /2}(\frac{(2\operatorname{cos}⁡(2\theta ))^{2}}{2}-0)\,\text{d}\theta\right)  \\  & =2\left({\int }_{-\pi /2}^{\pi /2}2{cos}^{2}⁡(2\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}2\left({\int }_{-\pi /2}^{\pi /2}2{cos}^{2}⁡(2\theta )\,\text{d}\theta\right)  & =2\left({\int }_{-\pi /2}^{\pi /2}(1+\operatorname{cos}⁡(4\theta ))\,\text{d}\theta\right)  \\  & =2\left({[\theta +\frac{1}{4}\operatorname{sin}⁡(4\theta )]}_{-\pi /2}^{\pi /2}\right) \\  & =2\left((\frac{\pi }{2}+\frac{\pi }{2})+\frac{1}{4}(\operatorname{sin}⁡(2\pi )-\operatorname{sin}⁡(-2\pi ))\right) \\  & =2\left(\pi\right) \end{aligned}
$$


## Generated observed-profile scalar variant

### q-38133 — easy

$3\left({\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta\right) =$

- A. $3\left(\frac{\pi }{4}\right)$
- B. $3\left(\frac{\sqrt{3}}{2}\right)$
- C. $3\left(2\pi\right) $
- D. $3\left(\pi +4\right)$
- E. $3\left(\pi\right) $ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}3\left({\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta\right)  & =3\left({\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta\right)  \\  & =3\left({\int }_{-\pi /2}^{\pi /2}{[\frac{{r}^{2}}{2}]}_{0}^{2\operatorname{cos}⁡(2\theta )}\,\text{d}\theta\right)  \\  & =3\left({\int }_{-\pi /2}^{\pi /2}(\frac{(2\operatorname{cos}⁡(2\theta ))^{2}}{2}-0)\,\text{d}\theta\right)  \\  & =3\left({\int }_{-\pi /2}^{\pi /2}2{cos}^{2}⁡(2\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}3\left({\int }_{-\pi /2}^{\pi /2}2{cos}^{2}⁡(2\theta )\,\text{d}\theta\right)  & =3\left({\int }_{-\pi /2}^{\pi /2}(1+\operatorname{cos}⁡(4\theta ))\,\text{d}\theta\right)  \\  & =3\left({[\theta +\frac{1}{4}\operatorname{sin}⁡(4\theta )]}_{-\pi /2}^{\pi /2}\right) \\  & =3\left((\frac{\pi }{2}+\frac{\pi }{2})+\frac{1}{4}(\operatorname{sin}⁡(2\pi )-\operatorname{sin}⁡(-2\pi ))\right) \\  & =3\left(\pi\right) \end{aligned}
$$


## Generated observed-profile scalar variant

### q-38133 — easy

$4\left({\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta\right) =$

- A. $4\left(2\pi\right) $
- B. $4\left(\pi +4\right)$
- C. $4\left(\frac{\pi }{4}\right)$
- D. $4\left(\frac{\sqrt{3}}{2}\right)$
- E. $4\left(\pi\right) $ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}4\left({\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta\right)  & =4\left({\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta\right)  \\  & =4\left({\int }_{-\pi /2}^{\pi /2}{[\frac{{r}^{2}}{2}]}_{0}^{2\operatorname{cos}⁡(2\theta )}\,\text{d}\theta\right)  \\  & =4\left({\int }_{-\pi /2}^{\pi /2}(\frac{(2\operatorname{cos}⁡(2\theta ))^{2}}{2}-0)\,\text{d}\theta\right)  \\  & =4\left({\int }_{-\pi /2}^{\pi /2}2{cos}^{2}⁡(2\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}4\left({\int }_{-\pi /2}^{\pi /2}2{cos}^{2}⁡(2\theta )\,\text{d}\theta\right)  & =4\left({\int }_{-\pi /2}^{\pi /2}(1+\operatorname{cos}⁡(4\theta ))\,\text{d}\theta\right)  \\  & =4\left({[\theta +\frac{1}{4}\operatorname{sin}⁡(4\theta )]}_{-\pi /2}^{\pi /2}\right) \\  & =4\left((\frac{\pi }{2}+\frac{\pi }{2})+\frac{1}{4}(\operatorname{sin}⁡(2\pi )-\operatorname{sin}⁡(-2\pi ))\right) \\  & =4\left(\pi\right) \end{aligned}
$$


## Generated observed-profile scalar variant

### q-38133 — easy

$5\left({\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta\right) =$

- A. $5\left(\frac{\pi }{4}\right)$
- B. $5\left(\pi\right) $ **correct**
- C. $5\left(2\pi\right) $
- D. $5\left(\frac{\sqrt{3}}{2}\right)$
- E. $5\left(\pi +4\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}5\left({\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta\right)  & =5\left({\int }_{-\pi /2}^{\pi /2}{\int }_{0}^{2\operatorname{cos}⁡(2\theta )}r\,\text{d}r\,\text{d}\theta\right)  \\  & =5\left({\int }_{-\pi /2}^{\pi /2}{[\frac{{r}^{2}}{2}]}_{0}^{2\operatorname{cos}⁡(2\theta )}\,\text{d}\theta\right)  \\  & =5\left({\int }_{-\pi /2}^{\pi /2}(\frac{(2\operatorname{cos}⁡(2\theta ))^{2}}{2}-0)\,\text{d}\theta\right)  \\  & =5\left({\int }_{-\pi /2}^{\pi /2}2{cos}^{2}⁡(2\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}5\left({\int }_{-\pi /2}^{\pi /2}2{cos}^{2}⁡(2\theta )\,\text{d}\theta\right)  & =5\left({\int }_{-\pi /2}^{\pi /2}(1+\operatorname{cos}⁡(4\theta ))\,\text{d}\theta\right)  \\  & =5\left({[\theta +\frac{1}{4}\operatorname{sin}⁡(4\theta )]}_{-\pi /2}^{\pi /2}\right) \\  & =5\left((\frac{\pi }{2}+\frac{\pi }{2})+\frac{1}{4}(\operatorname{sin}⁡(2\pi )-\operatorname{sin}⁡(-2\pi ))\right) \\  & =5\left(\pi\right) \end{aligned}
$$


## Generated observed-profile scalar variant

### q-83511 — easy

Evaluate $2\left({\int }_{0}^{\pi /2}{\int }_{1}^{3}{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $2\left(10\right)$ **correct**
- B. $2\left(30\right)$
- C. $2\left(20\right)$
- D. $2\left(40\right)$
- E. $2\left(5\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}2\left({\int }_{0}^{\pi /2}{\int }_{1}^{3}{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =2\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta {\int }_{1}^{3}{r}^{3}\,\text{d}r\,\text{d}\theta\right)  \\  & =2\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta {[\frac{{r}^{4}}{4}]}_{1}^{3}\,\text{d}\theta\right)  \\  & =2\left(\frac{1}{4}{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta ({3}^{4}-{1}^{4})\,\text{d}\theta\right)  \\  & =2\left(20{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}2\left(20{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}\theta\right)  & =2\left(20[\frac{{sin}^{2}⁡\theta }{2}]_{0}^{\pi /2}\right) \\  & =2\left(10{[{sin}^{2}⁡\theta ]}_{0}^{\pi /2}\right) \\  & =2\left(10({sin}^{2}⁡(\frac{\pi }{2})-{sin}^{2}⁡(0))\right) \\  & =2\left(10(1-0)\right) \\  & =2\left(10\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83511 — easy

Evaluate $3\left({\int }_{0}^{\pi /2}{\int }_{1}^{3}{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $3\left(5\right)$
- B. $3\left(10\right)$ **correct**
- C. $3\left(20\right)$
- D. $3\left(40\right)$
- E. $3\left(30\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}3\left({\int }_{0}^{\pi /2}{\int }_{1}^{3}{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =3\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta {\int }_{1}^{3}{r}^{3}\,\text{d}r\,\text{d}\theta\right)  \\  & =3\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta {[\frac{{r}^{4}}{4}]}_{1}^{3}\,\text{d}\theta\right)  \\  & =3\left(\frac{1}{4}{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta ({3}^{4}-{1}^{4})\,\text{d}\theta\right)  \\  & =3\left(20{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}3\left(20{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}\theta\right)  & =3\left(20[\frac{{sin}^{2}⁡\theta }{2}]_{0}^{\pi /2}\right) \\  & =3\left(10{[{sin}^{2}⁡\theta ]}_{0}^{\pi /2}\right) \\  & =3\left(10({sin}^{2}⁡(\frac{\pi }{2})-{sin}^{2}⁡(0))\right) \\  & =3\left(10(1-0)\right) \\  & =3\left(10\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83511 — easy

Evaluate $4\left({\int }_{0}^{\pi /2}{\int }_{1}^{3}{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $4\left(20\right)$
- B. $4\left(40\right)$
- C. $4\left(5\right)$
- D. $4\left(10\right)$ **correct**
- E. $4\left(30\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}4\left({\int }_{0}^{\pi /2}{\int }_{1}^{3}{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =4\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta {\int }_{1}^{3}{r}^{3}\,\text{d}r\,\text{d}\theta\right)  \\  & =4\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta {[\frac{{r}^{4}}{4}]}_{1}^{3}\,\text{d}\theta\right)  \\  & =4\left(\frac{1}{4}{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta ({3}^{4}-{1}^{4})\,\text{d}\theta\right)  \\  & =4\left(20{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}4\left(20{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}\theta\right)  & =4\left(20[\frac{{sin}^{2}⁡\theta }{2}]_{0}^{\pi /2}\right) \\  & =4\left(10{[{sin}^{2}⁡\theta ]}_{0}^{\pi /2}\right) \\  & =4\left(10({sin}^{2}⁡(\frac{\pi }{2})-{sin}^{2}⁡(0))\right) \\  & =4\left(10(1-0)\right) \\  & =4\left(10\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83511 — easy

Evaluate $5\left({\int }_{0}^{\pi /2}{\int }_{1}^{3}{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $5\left(5\right)$
- B. $5\left(30\right)$
- C. $5\left(20\right)$
- D. $5\left(10\right)$ **correct**
- E. $5\left(40\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}5\left({\int }_{0}^{\pi /2}{\int }_{1}^{3}{r}^{3}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =5\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta {\int }_{1}^{3}{r}^{3}\,\text{d}r\,\text{d}\theta\right)  \\  & =5\left({\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta {[\frac{{r}^{4}}{4}]}_{1}^{3}\,\text{d}\theta\right)  \\  & =5\left(\frac{1}{4}{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta ({3}^{4}-{1}^{4})\,\text{d}\theta\right)  \\  & =5\left(20{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}5\left(20{\int }_{0}^{\pi /2}\operatorname{cos}⁡\theta \operatorname{sin}⁡\theta \,\text{d}\theta\right)  & =5\left(20[\frac{{sin}^{2}⁡\theta }{2}]_{0}^{\pi /2}\right) \\  & =5\left(10{[{sin}^{2}⁡\theta ]}_{0}^{\pi /2}\right) \\  & =5\left(10({sin}^{2}⁡(\frac{\pi }{2})-{sin}^{2}⁡(0))\right) \\  & =5\left(10(1-0)\right) \\  & =5\left(10\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83957 — easy

$2\left({\int }_{\pi /6}^{3\pi /4}{\int }_{2}^{4}r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right) =$

- A. $2\left(3\sqrt{2}\right)$
- B. $2\left(3\right)$
- C. $2\left(\frac{3}{2}(\sqrt{2}-1)\right)$
- D. $2\left(3(\sqrt{2}-1)\right)$ **correct**
- E. $2\left(6(\sqrt{2}-1)\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}2\left({\int }_{\pi /6}^{3\pi /4}{\int }_{2}^{4}r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =2\left({\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta {\int }_{2}^{4}r\,\text{d}r\,\text{d}\theta\right)  \\  & =2\left({\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta {[\frac{{r}^{2}}{2}]}_{2}^{4}\,\text{d}\theta\right)  \\  & =2\left(\frac{1}{2}{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta ({4}^{2}-{2}^{2})\,\text{d}\theta\right)  \\  & =2\left(6{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}2\left(6{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta \,\text{d}\theta\right)  & =2\left(6[\operatorname{sin}⁡\theta ]_{\pi /6}^{3\pi /4}\right) \\  & =2\left(6(\operatorname{sin}⁡(\frac{3\pi }{4})-\operatorname{sin}⁡(\frac{\pi }{6}))\right) \\  & =2\left(6(\frac{\sqrt{2}}{2}-\frac{1}{2})\right) \\  & =2\left(3(\sqrt{2}-1)\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83957 — easy

$3\left({\int }_{\pi /6}^{3\pi /4}{\int }_{2}^{4}r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right) =$

- A. $3\left(6(\sqrt{2}-1)\right)$
- B. $3\left(3\sqrt{2}\right)$
- C. $3\left(\frac{3}{2}(\sqrt{2}-1)\right)$
- D. $3\left(3(\sqrt{2}-1)\right)$ **correct**
- E. $3\left(3\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}3\left({\int }_{\pi /6}^{3\pi /4}{\int }_{2}^{4}r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =3\left({\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta {\int }_{2}^{4}r\,\text{d}r\,\text{d}\theta\right)  \\  & =3\left({\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta {[\frac{{r}^{2}}{2}]}_{2}^{4}\,\text{d}\theta\right)  \\  & =3\left(\frac{1}{2}{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta ({4}^{2}-{2}^{2})\,\text{d}\theta\right)  \\  & =3\left(6{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}3\left(6{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta \,\text{d}\theta\right)  & =3\left(6[\operatorname{sin}⁡\theta ]_{\pi /6}^{3\pi /4}\right) \\  & =3\left(6(\operatorname{sin}⁡(\frac{3\pi }{4})-\operatorname{sin}⁡(\frac{\pi }{6}))\right) \\  & =3\left(6(\frac{\sqrt{2}}{2}-\frac{1}{2})\right) \\  & =3\left(3(\sqrt{2}-1)\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83957 — easy

$4\left({\int }_{\pi /6}^{3\pi /4}{\int }_{2}^{4}r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right) =$

- A. $4\left(\frac{3}{2}(\sqrt{2}-1)\right)$
- B. $4\left(3(\sqrt{2}-1)\right)$ **correct**
- C. $4\left(6(\sqrt{2}-1)\right)$
- D. $4\left(3\sqrt{2}\right)$
- E. $4\left(3\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}4\left({\int }_{\pi /6}^{3\pi /4}{\int }_{2}^{4}r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =4\left({\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta {\int }_{2}^{4}r\,\text{d}r\,\text{d}\theta\right)  \\  & =4\left({\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta {[\frac{{r}^{2}}{2}]}_{2}^{4}\,\text{d}\theta\right)  \\  & =4\left(\frac{1}{2}{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta ({4}^{2}-{2}^{2})\,\text{d}\theta\right)  \\  & =4\left(6{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}4\left(6{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta \,\text{d}\theta\right)  & =4\left(6[\operatorname{sin}⁡\theta ]_{\pi /6}^{3\pi /4}\right) \\  & =4\left(6(\operatorname{sin}⁡(\frac{3\pi }{4})-\operatorname{sin}⁡(\frac{\pi }{6}))\right) \\  & =4\left(6(\frac{\sqrt{2}}{2}-\frac{1}{2})\right) \\  & =4\left(3(\sqrt{2}-1)\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83957 — easy

$5\left({\int }_{\pi /6}^{3\pi /4}{\int }_{2}^{4}r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right) =$

- A. $5\left(6(\sqrt{2}-1)\right)$
- B. $5\left(3\right)$
- C. $5\left(\frac{3}{2}(\sqrt{2}-1)\right)$
- D. $5\left(3\sqrt{2}\right)$
- E. $5\left(3(\sqrt{2}-1)\right)$ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}5\left({\int }_{\pi /6}^{3\pi /4}{\int }_{2}^{4}r\operatorname{cos}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =5\left({\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta {\int }_{2}^{4}r\,\text{d}r\,\text{d}\theta\right)  \\  & =5\left({\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta {[\frac{{r}^{2}}{2}]}_{2}^{4}\,\text{d}\theta\right)  \\  & =5\left(\frac{1}{2}{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta ({4}^{2}-{2}^{2})\,\text{d}\theta\right)  \\  & =5\left(6{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}5\left(6{\int }_{\pi /6}^{3\pi /4}\operatorname{cos}⁡\theta \,\text{d}\theta\right)  & =5\left(6[\operatorname{sin}⁡\theta ]_{\pi /6}^{3\pi /4}\right) \\  & =5\left(6(\operatorname{sin}⁡(\frac{3\pi }{4})-\operatorname{sin}⁡(\frac{\pi }{6}))\right) \\  & =5\left(6(\frac{\sqrt{2}}{2}-\frac{1}{2})\right) \\  & =5\left(3(\sqrt{2}-1)\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83958 — moderate

Evaluate 
$2\left({\int }_{0}^{\pi /2}{\int }_{1-\operatorname{cos}⁡\theta }^{1}r\,\text{d}r\,\text{d}\theta \right).$

- A. $2\left(\frac{2-\pi }{2}\right)$
- B. $2\left(8-\pi\right) $
- C. $2\left(\frac{8-\pi }{8}\right)$ **correct**
- D. $2\left(1-\pi\right) $
- E. $2\left(\frac{4-\pi }{4}\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}2\left({\int }_{0}^{\pi /2}{\int }_{1-\operatorname{cos}⁡\theta }^{1}r\,\text{d}r\,\text{d}\theta\right)  & =2\left({\int }_{0}^{\pi /2}\,[\frac{{r}^{2}}{2}]_{1-\operatorname{cos}⁡\theta }^{1}\,\text{d}\theta\right)  \\  & =2\left(\frac{1}{2}{\int }_{0}^{\pi /2}({1}^{2}-(1-\operatorname{cos}⁡\theta )^{2})\,\text{d}\theta\right)  \\  & =2\left(\frac{1}{2}{\int }_{0}^{\pi /2}(2\operatorname{cos}⁡\theta -{cos}^{2}⁡\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}2\left(\frac{1}{2}{\int }_{0}^{\pi /2}(2\operatorname{cos}⁡\theta -{cos}^{2}⁡\theta )\,\text{d}\theta\right)  & =2\left({[\operatorname{sin}⁡\theta -\frac{1}{4}\theta -\frac{1}{8}\operatorname{sin}⁡(2\theta )]}_{0}^{\pi /2}\right) \\  & =2\left((\operatorname{sin}⁡(\frac{\pi }{2})-\frac{1}{4}\cdot \frac{\pi }{2}-\frac{1}{8}\operatorname{sin}⁡\pi )-0\right) \\  & =2\left(1-\frac{\pi }{8}-\frac{1}{8}\cdot 0\right) \\  & =2\left(\frac{8-\pi }{8}\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83958 — moderate

Evaluate 
$3\left({\int }_{0}^{\pi /2}{\int }_{1-\operatorname{cos}⁡\theta }^{1}r\,\text{d}r\,\text{d}\theta \right).$

- A. $3\left(\frac{4-\pi }{4}\right)$
- B. $3\left(\frac{2-\pi }{2}\right)$
- C. $3\left(\frac{8-\pi }{8}\right)$ **correct**
- D. $3\left(1-\pi\right) $
- E. $3\left(8-\pi\right) $

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}3\left({\int }_{0}^{\pi /2}{\int }_{1-\operatorname{cos}⁡\theta }^{1}r\,\text{d}r\,\text{d}\theta\right)  & =3\left({\int }_{0}^{\pi /2}\,[\frac{{r}^{2}}{2}]_{1-\operatorname{cos}⁡\theta }^{1}\,\text{d}\theta\right)  \\  & =3\left(\frac{1}{2}{\int }_{0}^{\pi /2}({1}^{2}-(1-\operatorname{cos}⁡\theta )^{2})\,\text{d}\theta\right)  \\  & =3\left(\frac{1}{2}{\int }_{0}^{\pi /2}(2\operatorname{cos}⁡\theta -{cos}^{2}⁡\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}3\left(\frac{1}{2}{\int }_{0}^{\pi /2}(2\operatorname{cos}⁡\theta -{cos}^{2}⁡\theta )\,\text{d}\theta\right)  & =3\left({[\operatorname{sin}⁡\theta -\frac{1}{4}\theta -\frac{1}{8}\operatorname{sin}⁡(2\theta )]}_{0}^{\pi /2}\right) \\  & =3\left((\operatorname{sin}⁡(\frac{\pi }{2})-\frac{1}{4}\cdot \frac{\pi }{2}-\frac{1}{8}\operatorname{sin}⁡\pi )-0\right) \\  & =3\left(1-\frac{\pi }{8}-\frac{1}{8}\cdot 0\right) \\  & =3\left(\frac{8-\pi }{8}\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83958 — moderate

Evaluate 
$4\left({\int }_{0}^{\pi /2}{\int }_{1-\operatorname{cos}⁡\theta }^{1}r\,\text{d}r\,\text{d}\theta \right).$

- A. $4\left(\frac{8-\pi }{8}\right)$ **correct**
- B. $4\left(1-\pi\right) $
- C. $4\left(\frac{4-\pi }{4}\right)$
- D. $4\left(\frac{2-\pi }{2}\right)$
- E. $4\left(8-\pi\right) $

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}4\left({\int }_{0}^{\pi /2}{\int }_{1-\operatorname{cos}⁡\theta }^{1}r\,\text{d}r\,\text{d}\theta\right)  & =4\left({\int }_{0}^{\pi /2}\,[\frac{{r}^{2}}{2}]_{1-\operatorname{cos}⁡\theta }^{1}\,\text{d}\theta\right)  \\  & =4\left(\frac{1}{2}{\int }_{0}^{\pi /2}({1}^{2}-(1-\operatorname{cos}⁡\theta )^{2})\,\text{d}\theta\right)  \\  & =4\left(\frac{1}{2}{\int }_{0}^{\pi /2}(2\operatorname{cos}⁡\theta -{cos}^{2}⁡\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}4\left(\frac{1}{2}{\int }_{0}^{\pi /2}(2\operatorname{cos}⁡\theta -{cos}^{2}⁡\theta )\,\text{d}\theta\right)  & =4\left({[\operatorname{sin}⁡\theta -\frac{1}{4}\theta -\frac{1}{8}\operatorname{sin}⁡(2\theta )]}_{0}^{\pi /2}\right) \\  & =4\left((\operatorname{sin}⁡(\frac{\pi }{2})-\frac{1}{4}\cdot \frac{\pi }{2}-\frac{1}{8}\operatorname{sin}⁡\pi )-0\right) \\  & =4\left(1-\frac{\pi }{8}-\frac{1}{8}\cdot 0\right) \\  & =4\left(\frac{8-\pi }{8}\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83958 — moderate

Evaluate 
$5\left({\int }_{0}^{\pi /2}{\int }_{1-\operatorname{cos}⁡\theta }^{1}r\,\text{d}r\,\text{d}\theta \right).$

- A. $5\left(\frac{4-\pi }{4}\right)$
- B. $5\left(8-\pi\right) $
- C. $5\left(\frac{8-\pi }{8}\right)$ **correct**
- D. $5\left(\frac{2-\pi }{2}\right)$
- E. $5\left(1-\pi\right) $

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}5\left({\int }_{0}^{\pi /2}{\int }_{1-\operatorname{cos}⁡\theta }^{1}r\,\text{d}r\,\text{d}\theta\right)  & =5\left({\int }_{0}^{\pi /2}\,[\frac{{r}^{2}}{2}]_{1-\operatorname{cos}⁡\theta }^{1}\,\text{d}\theta\right)  \\  & =5\left(\frac{1}{2}{\int }_{0}^{\pi /2}({1}^{2}-(1-\operatorname{cos}⁡\theta )^{2})\,\text{d}\theta\right)  \\  & =5\left(\frac{1}{2}{\int }_{0}^{\pi /2}(2\operatorname{cos}⁡\theta -{cos}^{2}⁡\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}5\left(\frac{1}{2}{\int }_{0}^{\pi /2}(2\operatorname{cos}⁡\theta -{cos}^{2}⁡\theta )\,\text{d}\theta\right)  & =5\left({[\operatorname{sin}⁡\theta -\frac{1}{4}\theta -\frac{1}{8}\operatorname{sin}⁡(2\theta )]}_{0}^{\pi /2}\right) \\  & =5\left((\operatorname{sin}⁡(\frac{\pi }{2})-\frac{1}{4}\cdot \frac{\pi }{2}-\frac{1}{8}\operatorname{sin}⁡\pi )-0\right) \\  & =5\left(1-\frac{\pi }{8}-\frac{1}{8}\cdot 0\right) \\  & =5\left(\frac{8-\pi }{8}\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83514 — moderate

Evaluate 
$2\left({\int }_{\pi /4}^{\pi /2}{\int }_{\operatorname{csc}⁡\theta }^{2}2r\,\text{d}r\,\text{d}\theta \right).$

- A. $2\left(\pi -2\right)$
- B. $2\left(\pi +1\right)$
- C. $2\left(\pi +2\right)$
- D. $2\left(\pi\right) $
- E. $2\left(\pi -1\right)$ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}2\left({\int }_{\pi /4}^{\pi /2}{\int }_{\operatorname{csc}⁡\theta }^{2}2r\,\text{d}r\,\text{d}\theta\right)  & =2\left({\int }_{\pi /4}^{\pi /2}[{r}^{2}]_{\operatorname{csc}⁡\theta }^{2}\,\text{d}\theta\right)  \\  & =2\left({\int }_{\pi /4}^{\pi /2}({2}^{2}-{csc}^{2}⁡\theta )\,\text{d}\theta\right)  \\  & =2\left({\int }_{\pi /4}^{\pi /2}(4-{csc}^{2}⁡\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}2\left({\int }_{\pi /4}^{\pi /2}(4-{csc}^{2}⁡\theta )\,\text{d}\theta\right)  & =2\left([4\theta +\operatorname{cot}⁡\theta ]_{\pi /4}^{\pi /2}\right) \\  & =2\left((4\cdot \frac{\pi }{2}+\operatorname{cot}⁡(\frac{\pi }{2}))-(4\cdot \frac{\pi }{4}+\operatorname{cot}⁡(\frac{\pi }{4}))\right) \\  & =2\left((2\pi +0)-(\pi +1)\right) \\  & =2\left(\pi -1\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83514 — moderate

Evaluate 
$3\left({\int }_{\pi /4}^{\pi /2}{\int }_{\operatorname{csc}⁡\theta }^{2}2r\,\text{d}r\,\text{d}\theta \right).$

- A. $3\left(\pi -1\right)$ **correct**
- B. $3\left(\pi -2\right)$
- C. $3\left(\pi +2\right)$
- D. $3\left(\pi\right) $
- E. $3\left(\pi +1\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}3\left({\int }_{\pi /4}^{\pi /2}{\int }_{\operatorname{csc}⁡\theta }^{2}2r\,\text{d}r\,\text{d}\theta\right)  & =3\left({\int }_{\pi /4}^{\pi /2}[{r}^{2}]_{\operatorname{csc}⁡\theta }^{2}\,\text{d}\theta\right)  \\  & =3\left({\int }_{\pi /4}^{\pi /2}({2}^{2}-{csc}^{2}⁡\theta )\,\text{d}\theta\right)  \\  & =3\left({\int }_{\pi /4}^{\pi /2}(4-{csc}^{2}⁡\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}3\left({\int }_{\pi /4}^{\pi /2}(4-{csc}^{2}⁡\theta )\,\text{d}\theta\right)  & =3\left([4\theta +\operatorname{cot}⁡\theta ]_{\pi /4}^{\pi /2}\right) \\  & =3\left((4\cdot \frac{\pi }{2}+\operatorname{cot}⁡(\frac{\pi }{2}))-(4\cdot \frac{\pi }{4}+\operatorname{cot}⁡(\frac{\pi }{4}))\right) \\  & =3\left((2\pi +0)-(\pi +1)\right) \\  & =3\left(\pi -1\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83514 — moderate

Evaluate 
$4\left({\int }_{\pi /4}^{\pi /2}{\int }_{\operatorname{csc}⁡\theta }^{2}2r\,\text{d}r\,\text{d}\theta \right).$

- A. $4\left(\pi +2\right)$
- B. $4\left(\pi\right) $
- C. $4\left(\pi -1\right)$ **correct**
- D. $4\left(\pi -2\right)$
- E. $4\left(\pi +1\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}4\left({\int }_{\pi /4}^{\pi /2}{\int }_{\operatorname{csc}⁡\theta }^{2}2r\,\text{d}r\,\text{d}\theta\right)  & =4\left({\int }_{\pi /4}^{\pi /2}[{r}^{2}]_{\operatorname{csc}⁡\theta }^{2}\,\text{d}\theta\right)  \\  & =4\left({\int }_{\pi /4}^{\pi /2}({2}^{2}-{csc}^{2}⁡\theta )\,\text{d}\theta\right)  \\  & =4\left({\int }_{\pi /4}^{\pi /2}(4-{csc}^{2}⁡\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}4\left({\int }_{\pi /4}^{\pi /2}(4-{csc}^{2}⁡\theta )\,\text{d}\theta\right)  & =4\left([4\theta +\operatorname{cot}⁡\theta ]_{\pi /4}^{\pi /2}\right) \\  & =4\left((4\cdot \frac{\pi }{2}+\operatorname{cot}⁡(\frac{\pi }{2}))-(4\cdot \frac{\pi }{4}+\operatorname{cot}⁡(\frac{\pi }{4}))\right) \\  & =4\left((2\pi +0)-(\pi +1)\right) \\  & =4\left(\pi -1\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83514 — moderate

Evaluate 
$5\left({\int }_{\pi /4}^{\pi /2}{\int }_{\operatorname{csc}⁡\theta }^{2}2r\,\text{d}r\,\text{d}\theta \right).$

- A. $5\left(\pi -1\right)$ **correct**
- B. $5\left(\pi +1\right)$
- C. $5\left(\pi +2\right)$
- D. $5\left(\pi -2\right)$
- E. $5\left(\pi\right) $

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}5\left({\int }_{\pi /4}^{\pi /2}{\int }_{\operatorname{csc}⁡\theta }^{2}2r\,\text{d}r\,\text{d}\theta\right)  & =5\left({\int }_{\pi /4}^{\pi /2}[{r}^{2}]_{\operatorname{csc}⁡\theta }^{2}\,\text{d}\theta\right)  \\  & =5\left({\int }_{\pi /4}^{\pi /2}({2}^{2}-{csc}^{2}⁡\theta )\,\text{d}\theta\right)  \\  & =5\left({\int }_{\pi /4}^{\pi /2}(4-{csc}^{2}⁡\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}5\left({\int }_{\pi /4}^{\pi /2}(4-{csc}^{2}⁡\theta )\,\text{d}\theta\right)  & =5\left([4\theta +\operatorname{cot}⁡\theta ]_{\pi /4}^{\pi /2}\right) \\  & =5\left((4\cdot \frac{\pi }{2}+\operatorname{cot}⁡(\frac{\pi }{2}))-(4\cdot \frac{\pi }{4}+\operatorname{cot}⁡(\frac{\pi }{4}))\right) \\  & =5\left((2\pi +0)-(\pi +1)\right) \\  & =5\left(\pi -1\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-161048 — easy

$2\left({\int }_{0}^{\pi }{\int }_{0}^{1}5{r}^{4}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right) =$

- A. $2\left(5\right)$
- B. $2\left(1\right)$
- C. $2\left(2\right)$ **correct**
- D. $2\left(4\right)$
- E. $2\left(0\right)$

First, we integrate with respect to $r$ treating $\theta $ as a constant:

$$
\begin{aligned}2\left({\int }_{0}^{\pi }{\int }_{0}^{1}5{r}^{4}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =2\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta {\int }_{0}^{1}5{r}^{4}\,\text{d}r\,\text{d}\theta\right)  \\  & =2\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta [{r}^{5}]_{0}^{1}\,\text{d}\theta\right)  \\  & =2\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta (1-0)\,\text{d}\theta\right)  \\  & =2\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}2\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta \,\text{d}\theta\right)  & =2\left([-\operatorname{cos}⁡\theta ]_{0}^{\pi }\right) \\  & =2\left(-(\operatorname{cos}⁡\pi -\operatorname{cos}⁡0)\right) \\  & =2\left(-(-1-1)\right) \\  & =2\left(2\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-161048 — easy

$3\left({\int }_{0}^{\pi }{\int }_{0}^{1}5{r}^{4}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right) =$

- A. $3\left(0\right)$
- B. $3\left(5\right)$
- C. $3\left(2\right)$ **correct**
- D. $3\left(4\right)$
- E. $3\left(1\right)$

First, we integrate with respect to $r$ treating $\theta $ as a constant:

$$
\begin{aligned}3\left({\int }_{0}^{\pi }{\int }_{0}^{1}5{r}^{4}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =3\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta {\int }_{0}^{1}5{r}^{4}\,\text{d}r\,\text{d}\theta\right)  \\  & =3\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta [{r}^{5}]_{0}^{1}\,\text{d}\theta\right)  \\  & =3\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta (1-0)\,\text{d}\theta\right)  \\  & =3\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}3\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta \,\text{d}\theta\right)  & =3\left([-\operatorname{cos}⁡\theta ]_{0}^{\pi }\right) \\  & =3\left(-(\operatorname{cos}⁡\pi -\operatorname{cos}⁡0)\right) \\  & =3\left(-(-1-1)\right) \\  & =3\left(2\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-161048 — easy

$4\left({\int }_{0}^{\pi }{\int }_{0}^{1}5{r}^{4}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right) =$

- A. $4\left(2\right)$ **correct**
- B. $4\left(4\right)$
- C. $4\left(0\right)$
- D. $4\left(5\right)$
- E. $4\left(1\right)$

First, we integrate with respect to $r$ treating $\theta $ as a constant:

$$
\begin{aligned}4\left({\int }_{0}^{\pi }{\int }_{0}^{1}5{r}^{4}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =4\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta {\int }_{0}^{1}5{r}^{4}\,\text{d}r\,\text{d}\theta\right)  \\  & =4\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta [{r}^{5}]_{0}^{1}\,\text{d}\theta\right)  \\  & =4\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta (1-0)\,\text{d}\theta\right)  \\  & =4\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}4\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta \,\text{d}\theta\right)  & =4\left([-\operatorname{cos}⁡\theta ]_{0}^{\pi }\right) \\  & =4\left(-(\operatorname{cos}⁡\pi -\operatorname{cos}⁡0)\right) \\  & =4\left(-(-1-1)\right) \\  & =4\left(2\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-161048 — easy

$5\left({\int }_{0}^{\pi }{\int }_{0}^{1}5{r}^{4}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right) =$

- A. $5\left(0\right)$
- B. $5\left(1\right)$
- C. $5\left(2\right)$ **correct**
- D. $5\left(5\right)$
- E. $5\left(4\right)$

First, we integrate with respect to $r$ treating $\theta $ as a constant:

$$
\begin{aligned}5\left({\int }_{0}^{\pi }{\int }_{0}^{1}5{r}^{4}\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =5\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta {\int }_{0}^{1}5{r}^{4}\,\text{d}r\,\text{d}\theta\right)  \\  & =5\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta [{r}^{5}]_{0}^{1}\,\text{d}\theta\right)  \\  & =5\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta (1-0)\,\text{d}\theta\right)  \\  & =5\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta \,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}5\left({\int }_{0}^{\pi }\operatorname{sin}⁡\theta \,\text{d}\theta\right)  & =5\left([-\operatorname{cos}⁡\theta ]_{0}^{\pi }\right) \\  & =5\left(-(\operatorname{cos}⁡\pi -\operatorname{cos}⁡0)\right) \\  & =5\left(-(-1-1)\right) \\  & =5\left(2\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83966 — moderate

Evaluate 
$2\left({\int }_{5\pi /3}^{2\pi }{\int }_{1}^{2\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $2\left(\frac{1}{12}\right)$
- B. $2\left(-\frac{1}{3}\right)$ **correct**
- C. $2\left(\frac{1}{6}\right)$
- D. $2\left(-\frac{1}{6}\right)$
- E. $2\left(-\frac{1}{12}\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}2\left({\int }_{5\pi /3}^{2\pi }{\int }_{1}^{2\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =2\left({\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta {\int }_{1}^{2\operatorname{cos}⁡\theta }r\,\text{d}r\,\text{d}\theta\right)  \\  & =2\left({\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta \,[\frac{{r}^{2}}{2}]_{1}^{2\operatorname{cos}⁡\theta }\,\text{d}\theta\right)  \\  & =2\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta ((2\operatorname{cos}⁡\theta )^{2}-{1}^{2})\,\text{d}\theta\right)  \\  & =2\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta (4{cos}^{2}⁡\theta -1)\,\text{d}\theta\right)  \\  & =2\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }(4\operatorname{sin}⁡\theta {cos}^{2}⁡\theta -\operatorname{sin}⁡\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}2\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }(4\operatorname{sin}⁡\theta {cos}^{2}⁡\theta -\operatorname{sin}⁡\theta )\,\text{d}\theta\right)  & =2\left(\frac{1}{2}{[-\frac{4}{3}{cos}^{3}⁡\theta +\operatorname{cos}⁡\theta ]}_{5\pi /3}^{2\pi }\right) \\  & =2\left(\frac{1}{2}[(-\frac{4}{3}{cos}^{3}⁡(2\pi )+\operatorname{cos}⁡(2\pi ))-(-\frac{4}{3}{cos}^{3}⁡(\frac{5\pi }{3})+\operatorname{cos}⁡(\frac{5\pi }{3}))]\right) \\  & =2\left(\frac{1}{2}[(-\frac{4}{3}+1)-(-\frac{1}{6}+\frac{1}{2})]\right) \\  & =2\left(-\frac{1}{3}\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83966 — moderate

Evaluate 
$3\left({\int }_{5\pi /3}^{2\pi }{\int }_{1}^{2\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $3\left(-\frac{1}{12}\right)$
- B. $3\left(\frac{1}{12}\right)$
- C. $3\left(\frac{1}{6}\right)$
- D. $3\left(-\frac{1}{6}\right)$
- E. $3\left(-\frac{1}{3}\right)$ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}3\left({\int }_{5\pi /3}^{2\pi }{\int }_{1}^{2\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =3\left({\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta {\int }_{1}^{2\operatorname{cos}⁡\theta }r\,\text{d}r\,\text{d}\theta\right)  \\  & =3\left({\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta \,[\frac{{r}^{2}}{2}]_{1}^{2\operatorname{cos}⁡\theta }\,\text{d}\theta\right)  \\  & =3\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta ((2\operatorname{cos}⁡\theta )^{2}-{1}^{2})\,\text{d}\theta\right)  \\  & =3\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta (4{cos}^{2}⁡\theta -1)\,\text{d}\theta\right)  \\  & =3\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }(4\operatorname{sin}⁡\theta {cos}^{2}⁡\theta -\operatorname{sin}⁡\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}3\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }(4\operatorname{sin}⁡\theta {cos}^{2}⁡\theta -\operatorname{sin}⁡\theta )\,\text{d}\theta\right)  & =3\left(\frac{1}{2}{[-\frac{4}{3}{cos}^{3}⁡\theta +\operatorname{cos}⁡\theta ]}_{5\pi /3}^{2\pi }\right) \\  & =3\left(\frac{1}{2}[(-\frac{4}{3}{cos}^{3}⁡(2\pi )+\operatorname{cos}⁡(2\pi ))-(-\frac{4}{3}{cos}^{3}⁡(\frac{5\pi }{3})+\operatorname{cos}⁡(\frac{5\pi }{3}))]\right) \\  & =3\left(\frac{1}{2}[(-\frac{4}{3}+1)-(-\frac{1}{6}+\frac{1}{2})]\right) \\  & =3\left(-\frac{1}{3}\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83966 — moderate

Evaluate 
$4\left({\int }_{5\pi /3}^{2\pi }{\int }_{1}^{2\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $4\left(\frac{1}{6}\right)$
- B. $4\left(-\frac{1}{6}\right)$
- C. $4\left(-\frac{1}{12}\right)$
- D. $4\left(\frac{1}{12}\right)$
- E. $4\left(-\frac{1}{3}\right)$ **correct**

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}4\left({\int }_{5\pi /3}^{2\pi }{\int }_{1}^{2\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =4\left({\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta {\int }_{1}^{2\operatorname{cos}⁡\theta }r\,\text{d}r\,\text{d}\theta\right)  \\  & =4\left({\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta \,[\frac{{r}^{2}}{2}]_{1}^{2\operatorname{cos}⁡\theta }\,\text{d}\theta\right)  \\  & =4\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta ((2\operatorname{cos}⁡\theta )^{2}-{1}^{2})\,\text{d}\theta\right)  \\  & =4\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta (4{cos}^{2}⁡\theta -1)\,\text{d}\theta\right)  \\  & =4\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }(4\operatorname{sin}⁡\theta {cos}^{2}⁡\theta -\operatorname{sin}⁡\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}4\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }(4\operatorname{sin}⁡\theta {cos}^{2}⁡\theta -\operatorname{sin}⁡\theta )\,\text{d}\theta\right)  & =4\left(\frac{1}{2}{[-\frac{4}{3}{cos}^{3}⁡\theta +\operatorname{cos}⁡\theta ]}_{5\pi /3}^{2\pi }\right) \\  & =4\left(\frac{1}{2}[(-\frac{4}{3}{cos}^{3}⁡(2\pi )+\operatorname{cos}⁡(2\pi ))-(-\frac{4}{3}{cos}^{3}⁡(\frac{5\pi }{3})+\operatorname{cos}⁡(\frac{5\pi }{3}))]\right) \\  & =4\left(\frac{1}{2}[(-\frac{4}{3}+1)-(-\frac{1}{6}+\frac{1}{2})]\right) \\  & =4\left(-\frac{1}{3}\right)\end{aligned}
$$


## Generated observed-profile scalar variant

### q-83966 — moderate

Evaluate 
$5\left({\int }_{5\pi /3}^{2\pi }{\int }_{1}^{2\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta \right).$

- A. $5\left(-\frac{1}{12}\right)$
- B. $5\left(-\frac{1}{3}\right)$ **correct**
- C. $5\left(\frac{1}{6}\right)$
- D. $5\left(\frac{1}{12}\right)$
- E. $5\left(-\frac{1}{6}\right)$

First, we integrate with respect to $r,$ treating $\theta $ as a constant:

$$
\begin{aligned}5\left({\int }_{5\pi /3}^{2\pi }{\int }_{1}^{2\operatorname{cos}⁡\theta }r\operatorname{sin}⁡\theta \,\text{d}r\,\text{d}\theta\right)  & =5\left({\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta {\int }_{1}^{2\operatorname{cos}⁡\theta }r\,\text{d}r\,\text{d}\theta\right)  \\  & =5\left({\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta \,[\frac{{r}^{2}}{2}]_{1}^{2\operatorname{cos}⁡\theta }\,\text{d}\theta\right)  \\  & =5\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta ((2\operatorname{cos}⁡\theta )^{2}-{1}^{2})\,\text{d}\theta\right)  \\  & =5\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }\operatorname{sin}⁡\theta (4{cos}^{2}⁡\theta -1)\,\text{d}\theta\right)  \\  & =5\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }(4\operatorname{sin}⁡\theta {cos}^{2}⁡\theta -\operatorname{sin}⁡\theta )\,\text{d}\theta\right) \end{aligned}
$$

Next, we integrate with respect to $\theta :$ 

$$
\begin{aligned}5\left(\frac{1}{2}{\int }_{5\pi /3}^{2\pi }(4\operatorname{sin}⁡\theta {cos}^{2}⁡\theta -\operatorname{sin}⁡\theta )\,\text{d}\theta\right)  & =5\left(\frac{1}{2}{[-\frac{4}{3}{cos}^{3}⁡\theta +\operatorname{cos}⁡\theta ]}_{5\pi /3}^{2\pi }\right) \\  & =5\left(\frac{1}{2}[(-\frac{4}{3}{cos}^{3}⁡(2\pi )+\operatorname{cos}⁡(2\pi ))-(-\frac{4}{3}{cos}^{3}⁡(\frac{5\pi }{3})+\operatorname{cos}⁡(\frac{5\pi }{3}))]\right) \\  & =5\left(\frac{1}{2}[(-\frac{4}{3}+1)-(-\frac{1}{6}+\frac{1}{2})]\right) \\  & =5\left(-\frac{1}{3}\right)\end{aligned}
$$
