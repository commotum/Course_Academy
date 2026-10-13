# Arc-length integral setup review

All records are author previews with answers. Original snapshots follow, then parameterized replays and generated variants.

## Original q-33728

![](/media/jake/SSD/EDB/math/images/d1/d162245ac19c3ef9ae63d602fb4e188ddfd241a1a604304f6c272c3902ce1e93.png)

Which integral expression gives the arc length of the curve $g(t)=⟨\operatorname{sin}⁡2t,\,\operatorname{cos}⁡3t⟩$ from $t=0$ to $t=\pi ?$

First, we find ${g}^{′}(t)$ and $‖{g}^{′}(t)‖:$

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡2t),\,\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡3t)⟩ \\  & =⟨2\operatorname{cos}⁡2t,\,-3\operatorname{sin}⁡3t⟩ \\ ‖{g}^{′}(t)‖ & =\sqrt{(2\operatorname{cos}⁡2t)^{2}+(-3\operatorname{sin}⁡3t)^{2}} \\  & =\sqrt{4{cos}^{2}⁡2t+9{sin}^{2}⁡3t}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & ={\int }_{0}^{\pi }‖{g}^{′}(t)‖\,\text{d}t \\  & ={\int }_{0}^{\pi }\sqrt{4{cos}^{2}⁡2t+9{sin}^{2}⁡3t}\,\text{d}t.\end{aligned}
$$

Field 17592186117771; correct UNAVAILABLE

- $\displaystyle \int_{0}^{1}\sqrt{2\cos^{2} 2t + 3\sin^{2} 3t}dt$
- $\displaystyle \int_{0}^{π}\sqrt{4\cos^{2} 2t + 9\sin^{2} 3t}dt$
- $\displaystyle \int_{0}^{π}\sqrt{4\sin^{2} 2t + 9\cos^{2} 3t}dt$
- $\displaystyle \int_{0}^{1}\sqrt{2\sin^{2} 2t + 9\cos^{2} 3t}dt$
- $\displaystyle \int_{0}^{π}\sqrt{2\cos^{2} 2t + 9\sin^{2} 3t}dt$
Field 17592186391648; correct {\int }_{0}^{\pi }\sqrt{4{cos}^{2}⁡2t+9{sin}^{2}⁡3t}\,\text{d}t

- ${\int }_{0}^{\pi }\sqrt{2{cos}^{2}⁡2t+9{sin}^{2}⁡3t}\,\text{d}t$
- ${\int }_{0}^{\pi }\sqrt{4{sin}^{2}⁡2t+9{cos}^{2}⁡3t}\,\text{d}t$
- ${\int }_{0}^{\pi }\sqrt{4{cos}^{2}⁡2t+9{sin}^{2}⁡3t}\,\text{d}t$
- ${\int }_{0}^{1}\sqrt{2{cos}^{2}⁡2t+3{sin}^{2}⁡3t}\,\text{d}t$
- ${\int }_{0}^{1}\sqrt{2{sin}^{2}⁡2t+9{cos}^{2}⁡3t}\,\text{d}t$

## Original q-33862

Which integral  expression gives the arc length of the curve $f(t)={e}^{t}(\,i+2\,j+t\,k)$ from  $t=1$ to $t=2?$

First, we find ${f}^{′}(t)$ and $‖{f}^{′}(t)‖:$

$$
\begin{aligned}{f}^{′}(t) & =\frac{\text{d}}{\text{d}t}({e}^{t})\,i+\frac{\text{d}}{\text{d}t}(2{e}^{t})\,j+\frac{\text{d}}{\text{d}t}(t{e}^{t})\,k \\  & ={e}^{t}\,i+2{e}^{t}\,j+(t{e}^{t}+{e}^{t})\,k \\ ‖{f}^{′}(t)‖ & =\sqrt{({e}^{t})^{2}+(2{e}^{t})^{2}+({e}^{t}(t+1))^{2}} \\  & =\sqrt{{e}^{2t}+4{e}^{2t}+{e}^{2t}({t}^{2}+2t+1)} \\  & =\sqrt{{e}^{2t}(1+4+{t}^{2}+2t+1)} \\  & ={e}^{t}\sqrt{{t}^{2}+2t+6}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & ={\int }_{1}^{2}‖{f}^{′}(t)‖\,\text{d}t \\  & ={\int }_{1}^{2}{e}^{t}\sqrt{{t}^{2}+2t+6}\,\text{d}t.\end{aligned}
$$

Field 17592186314526; correct {\int }_{1}^{2}{e}^{t}\sqrt{{t}^{2}+2t+6}\,\text{d}t

- ${\int }_{1}^{2}{e}^{t}\sqrt{{t}^{2}+2t+5}\,\text{d}t$
- ${\int }_{0}^{1}{e}^{t}\sqrt{{t}^{2}+2t+2}\,\text{d}t$
- ${\int }_{1}^{2}{e}^{t}\sqrt{{t}^{2}+2t+4}\,\text{d}t$
- ${\int }_{1}^{2}{e}^{t}\sqrt{{t}^{2}+2t+6}\,\text{d}t$
- ${\int }_{0}^{1}{e}^{t}(t+2)\,\text{d}t$

## Original q-127419

Which integral expression gives the arc length of the curve $f(t)=⟨4\operatorname{cos}⁡t,\,3\operatorname{sin}⁡t,\,4\operatorname{sin}⁡t⟩$ from $t=\frac{\pi }{6}$ to $t=\frac{\pi }{4}?$

First, we find ${f}^{′}(t)$ and $‖{f}^{′}(t)‖:$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(4\operatorname{cos}⁡t),\,\frac{\text{d}}{\text{d}t}(3\operatorname{sin}⁡t),\,\frac{\text{d}}{\text{d}t}(4\operatorname{sin}⁡t)⟩ \\  & =⟨-4\operatorname{sin}⁡t,\,3\operatorname{cos}⁡t,\,4\operatorname{cos}⁡t⟩ \\ ‖{f}^{′}(t)‖ & =\sqrt{(-4\operatorname{sin}⁡t)^{2}+(3\operatorname{cos}⁡t)^{2}+(4\operatorname{cos}⁡t)^{2}} \\  & =\sqrt{16{sin}^{2}⁡t+9{cos}^{2}⁡t+16{cos}^{2}⁡t} \\  & =\sqrt{16({sin}^{2}⁡t+{cos}^{2}⁡t)+9{cos}^{2}⁡t} \\  & =\sqrt{9{cos}^{2}⁡t+16}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & ={\int }_{\pi /6}^{\pi /4}‖{f}^{′}(t)‖\,\text{d}t \\  & ={\int }_{\pi /6}^{\pi /4}\sqrt{9{cos}^{2}⁡t+16}\,\text{d}t.\end{aligned}
$$

Field 17592186262549; correct {\int }_{\pi /6}^{\pi /4}\sqrt{9{cos}^{2}⁡t+16}\,\text{d}t

- ${\int }_{\pi /6}^{\pi /4}\sqrt{16{cos}^{2}⁡t+9}\,\text{d}t$
- ${\int }_{\pi /6}^{\pi /4}\sqrt{3{cos}^{2}⁡t+4}\,\text{d}t$
- ${\int }_{\pi /6}^{\pi /4}\sqrt{9{sin}^{2}⁡t+16}\,\text{d}t$
- ${\int }_{\pi /6}^{\pi /4}\sqrt{4{sin}^{2}⁡t+3}\,\text{d}t$
- ${\int }_{\pi /6}^{\pi /4}\sqrt{9{cos}^{2}⁡t+16}\,\text{d}t$

## Original q-127427

Which integral expression gives the arc length of the curve $f(t)=⟨\operatorname{cos}⁡t+\operatorname{sin}⁡t,\,{e}^{t},\,\operatorname{sin}⁡t-\operatorname{cos}⁡t⟩$ from $t=-1$ to $t=1?$

First, we find ${f}^{′}(t)$ and $‖{f}^{′}(t)‖:$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t+\operatorname{sin}⁡t),\,\frac{\text{d}}{\text{d}t}({e}^{t}),\,\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t-\operatorname{cos}⁡t)⟩ \\  & =⟨\operatorname{cos}⁡t-\operatorname{sin}⁡t,\,{e}^{t},\,\operatorname{cos}⁡t+\operatorname{sin}⁡t⟩ \\ ‖{f}^{′}(t)‖ & =\sqrt{{(\operatorname{cos}⁡t-\operatorname{sin}⁡t)}^{2}+({e}^{t})^{2}+{(\operatorname{cos}⁡t+\operatorname{sin}⁡t)}^{2}} \\  & =\sqrt{{cos}^{2}⁡t-2\operatorname{cos}⁡t\operatorname{sin}⁡t+{sin}^{2}⁡t+{e}^{2t}+{cos}^{2}⁡t+2\operatorname{cos}⁡t\operatorname{sin}⁡t+{sin}^{2}⁡t} \\  & =\sqrt{{e}^{2t}+2({cos}^{2}⁡t+{sin}^{2}⁡t)} \\  & =\sqrt{{e}^{2t}+2}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & ={\int }_{-1}^{1}‖{f}^{′}(t)‖\,\text{d}t \\  & ={\int }_{-1}^{1}\sqrt{{e}^{2t}+2}\,\text{d}t.\end{aligned}
$$

Field 17592186262347; correct {\int }_{-1}^{1}\sqrt{{e}^{2t}+2}\,\text{d}t

- ${\int }_{-1}^{1}\sqrt{{e}^{2t}+2}\,\text{d}t$
- ${\int }_{-1}^{1}\sqrt{2{e}^{t}+1}\,\text{d}t$
- $2{\int }_{-1}^{1}\sqrt{{e}^{t}+2}\,\text{d}t$
- $2{\int }_{-1}^{1}\sqrt{2{e}^{2t}+1}\,\text{d}t$
- ${\int }_{-1}^{1}\sqrt{{e}^{2t}+1}\,\text{d}t$

## Original q-33857

Which integral  expression gives the arc length of the curve $f(t)=⟨\operatorname{sin}⁡2t,\operatorname{cos}⁡2t,{t}^{2}⟩$
from  $t=0$ to $t=1?$

First, we find ${f}^{′}(t)$ and $‖{f}^{′}(t)‖:$

$$
\begin{aligned}{f}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡2t),\,\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡2t),\,\frac{\text{d}}{\text{d}t}({t}^{2})⟩ \\  & =⟨2\operatorname{cos}⁡2t,\,-2\operatorname{sin}⁡2t,\,2t⟩ \\ ‖{f}^{′}(t)‖ & =\sqrt{(2\operatorname{cos}⁡2t)^{2}+(-2\operatorname{sin}⁡2t)^{2}+(2t)^{2}} \\  & =\sqrt{4{cos}^{2}⁡2t+4{sin}^{2}⁡2t+4{t}^{2}} \\  & =\sqrt{4({cos}^{2}⁡2t+{sin}^{2}⁡2t+{t}^{2})} \\  & =2\sqrt{1+{t}^{2}}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & ={\int }_{1}^{2}‖{f}^{′}(t)‖\,\text{d}t={\int }_{0}^{1}2\sqrt{1+{t}^{2}}\,\text{d}t\end{aligned}
$$

Field 17592186314419; correct 2{\int }_{0}^{1}\sqrt{1+{t}^{2}}\,\text{d}t

- ${\int }_{0}^{1}\sqrt{1+4{t}^{2}}\,\text{d}t$
- $\sqrt{2}{\int }_{0}^{1}\sqrt{1+{t}^{2}}\,\text{d}t$
- ${\int }_{0}^{1}\sqrt{1+{t}^{2}}\,\text{d}t$
- $2{\int }_{0}^{1}\sqrt{1+{t}^{2}}\,\text{d}t$
- $2{\int }_{0}^{1}\sqrt{{cos}^{2}⁡2t-{sin}^{2}⁡2t+{t}^{2}}\,\text{d}t$

## Original q-33706

![](/media/jake/SSD/EDB/math/images/10/10ee30ddf508bf985e1c3a41491818723b57301412a5514e4a39c3bc13518acd.png)

Which integral  expression gives the arc length of the curve $g(t)=⟨t\operatorname{sin}⁡t,2-t\operatorname{cos}⁡t⟩$
from  $t=0$ to $t=\pi ?$

First, we find ${g}^{′}(t)$ and $‖{g}^{′}(t)‖:$

$$
\begin{aligned}{g}^{′}(t) & =⟨\frac{\text{d}}{\text{d}t}(t\operatorname{sin}⁡t),\,\frac{\text{d}}{\text{d}t}(2-t\operatorname{cos}⁡t)⟩ \\  & =⟨\operatorname{sin}⁡t+t\operatorname{cos}⁡t,\,t\operatorname{sin}⁡t-\operatorname{cos}⁡t⟩ \\ ‖{g}^{′}(t)‖ & =\sqrt{(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)^{2}+(t\operatorname{sin}⁡t-\operatorname{cos}⁡t)^{2}} \\  & =\sqrt{{sin}^{2}⁡t+2t\operatorname{sin}⁡t\operatorname{cos}⁡t+{t}^{2}{cos}^{2}⁡t+{t}^{2}{sin}^{2}⁡t-2t\operatorname{sin}⁡t\operatorname{cos}⁡t+{cos}^{2}⁡t} \\  & =\sqrt{1+{t}^{2}}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L={\int }_{0}^{\pi }‖{g}^{′}(t)‖\,\text{d}t={\int }_{0}^{\pi }\sqrt{1+{t}^{2}}\,\text{d}t\end{aligned}
$$

Field 17592186391632; correct {\int }_{0}^{\pi }\sqrt{1+{t}^{2}}\,\text{d}t

- ${\int }_{0}^{\pi }\sqrt{1+{t}^{2}}\,\text{d}t$
- ${\int }_{0}^{\pi }\sqrt{2}(\operatorname{sin}⁡t+t\operatorname{cos}⁡t)\,\text{d}t$
- ${\int }_{0}^{\pi }\sqrt{{t}^{2}+2t\operatorname{sin}⁡2t}\,\text{d}t$
- ${\int }_{0}^{\pi }\sqrt{1+2{t}^{2}}\,\text{d}t$
- ${\int }_{0}^{\pi }\sqrt{2+{t}^{2}}\,\text{d}t$

## Original q-64723

![](/media/jake/SSD/EDB/math/images/d4/d42e9c6ed71f06c2dec273a91d3a4cfbdf5c58095be9370285d7987d38f7b5a6.png)

Which integral  expression gives the arc length of the curve $h(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j+t\,k$ from  $t=0$ to $t=2\pi ?$

First, we find ${h}^{′}(t)$ and $‖{h}^{′}(t)‖:$

$$
\begin{aligned}{h}^{′}(t) & =\frac{\text{d}}{\text{d}t}(\operatorname{cos}⁡t)\,i+\frac{\text{d}}{\text{d}t}(\operatorname{sin}⁡t)\,j+\frac{\text{d}}{\text{d}t}(t)\,k \\  & =-\operatorname{sin}⁡t\,i+\operatorname{cos}⁡t\,j+1\,k \\ ‖{h}^{′}(t)‖ & =\sqrt{(-\operatorname{sin}⁡t)^{2}+(\operatorname{cos}⁡t)^{2}+(1)^{2}} \\  & =\sqrt{{sin}^{2}⁡t+{cos}^{2}⁡t+1} \\  & =\sqrt{2}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & ={\int }_{0}^{2\pi }‖{h}^{′}(t)‖\,\text{d}t={\int }_{0}^{2\pi }\sqrt{2}\,\text{d}t\end{aligned}
$$

Field 17592186392885; correct {\int }_{0}^{2\pi }\sqrt{2}\,\text{d}t

- ${\int }_{0}^{2\pi }\sqrt{2{sin}^{2}⁡t+{cos}^{2}⁡t}\,\text{d}t$
- ${\int }_{0}^{\pi }\sqrt{3-{sin}^{2}⁡t}\,\text{d}t$
- ${\int }_{0}^{2\pi }\sqrt{2+{sin}^{2}⁡t}\,\text{d}t$
- ${\int }_{0}^{2\pi }\sqrt{2+{cos}^{2}⁡t}\,\text{d}t$
- ${\int }_{0}^{2\pi }\sqrt{2}\,\text{d}t$

## Original q-64724

Which integral expression gives the arc length of the curve $r(t)={t}^{3}\,i+3t\,j+{t}^{4}\,k$ from  $t=2$ to $t=5?$

First, we find ${r}^{′}(t)$ and $‖{r}^{′}(t)‖:$

$$
\begin{aligned}{r}^{′}(t) & =\frac{\text{d}}{\text{d}t}({t}^{3})\,i+\frac{\text{d}}{\text{d}t}(3t)\,j+\frac{\text{d}}{\text{d}t}({t}^{4})\,k \\  & =3{t}^{2}\,i+3\,j+4{t}^{3}\,k \\ ‖{r}^{′}(t)‖ & =\sqrt{(3{t}^{2})^{2}+(3)^{2}+(4{t}^{3})^{2}} \\  & =\sqrt{9{t}^{4}+9+16{t}^{6}}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & ={\int }_{2}^{5}‖{r}^{′}(t)‖\,\text{d}t={\int }_{2}^{5}\sqrt{16{t}^{6}+9{t}^{4}+9}\,\text{d}t\end{aligned}
$$

Field 17592186392892; correct {\int }_{2}^{5}\sqrt{16{t}^{6}+9{t}^{4}+9}\,\text{d}t

- ${\int }_{2}^{5}\sqrt{16{t}^{6}+9{t}^{4}+9}\,\text{d}t$
- ${\int }_{2}^{5}\sqrt{{t}^{6}+{t}^{4}+9}\,\text{d}t$
- ${\int }_{2}^{5}\sqrt{8{t}^{5}+9{t}^{3}+6}\,\text{d}t$
- ${\int }_{0}^{5}\sqrt{16{t}^{6}+9}\,\text{d}t$
- ${\int }_{2}^{5}\sqrt{16{t}^{6}+9{t}^{4}}\,\text{d}t$

## original-parameter replay — trig2 / observed:trig2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/bc7f3fd745b6a51bb1abd54c4a1d9c2ff7cab9314e0d2ce3f2ae55477e83ea7e.png)

Which integral expression gives the arc length of the curve $g(t)=\langle \sin{\left(2 t \right)},\,\cos{\left(3 t \right)}\rangle$ from $t=0$ to $t=\pi?$

- $\int_{0}^{\pi}\sqrt{9 \sin^{2}{\left(3 t \right)} + 2 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{9 \sin^{2}{\left(3 t \right)} + 4 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$ **correct**
- $\int_{0}^{\pi}\sqrt{4 \sin^{2}{\left(2 t \right)} + 9 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{3 \sin^{2}{\left(3 t \right)} + 2 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{2 \sin^{2}{\left(2 t \right)} + 9 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$

First, we find $g'(t)$ and $\|g'(t)\|:$

$$
\begin{aligned}g'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(\cos{\left(3 t \right)})\rangle \\  & =\langle 2 \cos{\left(2 t \right)},\,- 3 \sin{\left(3 t \right)}\rangle \\ \|g'(t)\| & =\sqrt{\left(- 3 \sin{\left(3 t \right)}\right)^{2} + \left(2 \cos{\left(2 t \right)}\right)^{2}} \\  & =\sqrt{9 \sin^{2}{\left(3 t \right)} + 4 \cos^{2}{\left(2 t \right)}}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{0}^{\pi}\|g'(t)\|\,\mathrm{d}t \\  & =\int_{0}^{\pi}\sqrt{9 \sin^{2}{\left(3 t \right)} + 4 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t.\end{aligned}
$$

## generated observed-bank variant — trig2 / observed:trig2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/d86eff07dc415c90d53b48c6b2eadd48f819f81dea20f23bd7180784b7e9167d.png)

Which integral expression gives the arc length of the curve $g(t)=\langle 4 \sin{\left(3 t \right)},\,3 \cos{\left(2 t \right)}\rangle$ from $t=0$ to $t=\pi?$

- $\int_{0}^{\pi}\sqrt{144 \sin^{2}{\left(3 t \right)} + 36 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}6 \sqrt{\sin^{2}{\left(2 t \right)} + 4 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$ **correct**
- $\int_{0}^{1}\sqrt{48 \sin^{2}{\left(3 t \right)} + 36 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{36 \sin^{2}{\left(2 t \right)} + 48 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{18 \sin^{2}{\left(2 t \right)} + 48 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$

First, we find $g'(t)$ and $\|g'(t)\|:$

$$
\begin{aligned}g'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(3 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(3 \cos{\left(2 t \right)})\rangle \\  & =\langle 12 \cos{\left(3 t \right)},\,- 6 \sin{\left(2 t \right)}\rangle \\ \|g'(t)\| & =\sqrt{\left(- 6 \sin{\left(2 t \right)}\right)^{2} + \left(12 \cos{\left(3 t \right)}\right)^{2}} \\  & =\sqrt{36 \sin^{2}{\left(2 t \right)} + 144 \cos^{2}{\left(3 t \right)}}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{0}^{\pi}\|g'(t)\|\,\mathrm{d}t \\  & =\int_{0}^{\pi}6 \sqrt{\sin^{2}{\left(2 t \right)} + 4 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t.\end{aligned}
$$

## generated observed-bank variant — trig2 / observed:trig2

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/6b0b7e765fb34366247525e153bbd81c97f941fff9f29b81f68474086a16795a.png)

Which integral expression gives the arc length of the curve $g(t)=\langle \sin{\left(3 t \right)},\,\cos{\left(2 t \right)}\rangle$ from $t=0$ to $t=\pi?$

- $\int_{0}^{1}\sqrt{2 \sin^{2}{\left(2 t \right)} + 3 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{4 \sin^{2}{\left(2 t \right)} + 9 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$ **correct**
- $\int_{0}^{\pi}\sqrt{4 \sin^{2}{\left(2 t \right)} + 3 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{3 \sin^{2}{\left(3 t \right)} + 4 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{9 \sin^{2}{\left(3 t \right)} + 4 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$

First, we find $g'(t)$ and $\|g'(t)\|:$

$$
\begin{aligned}g'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(3 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(\cos{\left(2 t \right)})\rangle \\  & =\langle 3 \cos{\left(3 t \right)},\,- 2 \sin{\left(2 t \right)}\rangle \\ \|g'(t)\| & =\sqrt{\left(- 2 \sin{\left(2 t \right)}\right)^{2} + \left(3 \cos{\left(3 t \right)}\right)^{2}} \\  & =\sqrt{4 \sin^{2}{\left(2 t \right)} + 9 \cos^{2}{\left(3 t \right)}}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{0}^{\pi}\|g'(t)\|\,\mathrm{d}t \\  & =\int_{0}^{\pi}\sqrt{4 \sin^{2}{\left(2 t \right)} + 9 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t.\end{aligned}
$$

## original-parameter replay — trig2 / observed:trig2:legacy

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/bc7f3fd745b6a51bb1abd54c4a1d9c2ff7cab9314e0d2ce3f2ae55477e83ea7e.png)

Which integral expression gives the arc length of the curve $g(t)=\langle \sin{\left(2 t \right)},\,\cos{\left(3 t \right)}\rangle$ from $t=0$ to $t=\pi?$

- $\int_{0}^{\pi}\sqrt{9 \sin^{2}{\left(3 t \right)} + 2 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{9 \sin^{2}{\left(3 t \right)} + 4 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$ **correct**
- $\int_{0}^{\pi}\sqrt{4 \sin^{2}{\left(2 t \right)} + 9 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{3 \sin^{2}{\left(3 t \right)} + 2 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{2 \sin^{2}{\left(2 t \right)} + 9 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$

First, we find $g'(t)$ and $\|g'(t)\|:$

$$
\begin{aligned}g'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(\cos{\left(3 t \right)})\rangle \\  & =\langle 2 \cos{\left(2 t \right)},\,- 3 \sin{\left(3 t \right)}\rangle \\ \|g'(t)\| & =\sqrt{\left(- 3 \sin{\left(3 t \right)}\right)^{2} + \left(2 \cos{\left(2 t \right)}\right)^{2}} \\  & =\sqrt{9 \sin^{2}{\left(3 t \right)} + 4 \cos^{2}{\left(2 t \right)}}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{0}^{\pi}\|g'(t)\|\,\mathrm{d}t \\  & =\int_{0}^{\pi}\sqrt{9 \sin^{2}{\left(3 t \right)} + 4 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t.\end{aligned}
$$

## generated observed-bank variant — trig2 / observed:trig2:legacy

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/d86eff07dc415c90d53b48c6b2eadd48f819f81dea20f23bd7180784b7e9167d.png)

Which integral expression gives the arc length of the curve $g(t)=\langle 4 \sin{\left(3 t \right)},\,3 \cos{\left(2 t \right)}\rangle$ from $t=0$ to $t=\pi?$

- $\int_{0}^{\pi}\sqrt{144 \sin^{2}{\left(3 t \right)} + 36 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}6 \sqrt{\sin^{2}{\left(2 t \right)} + 4 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$ **correct**
- $\int_{0}^{1}\sqrt{48 \sin^{2}{\left(3 t \right)} + 36 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{36 \sin^{2}{\left(2 t \right)} + 48 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{18 \sin^{2}{\left(2 t \right)} + 48 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$

First, we find $g'(t)$ and $\|g'(t)\|:$

$$
\begin{aligned}g'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(3 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(3 \cos{\left(2 t \right)})\rangle \\  & =\langle 12 \cos{\left(3 t \right)},\,- 6 \sin{\left(2 t \right)}\rangle \\ \|g'(t)\| & =\sqrt{\left(- 6 \sin{\left(2 t \right)}\right)^{2} + \left(12 \cos{\left(3 t \right)}\right)^{2}} \\  & =\sqrt{36 \sin^{2}{\left(2 t \right)} + 144 \cos^{2}{\left(3 t \right)}}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{0}^{\pi}\|g'(t)\|\,\mathrm{d}t \\  & =\int_{0}^{\pi}6 \sqrt{\sin^{2}{\left(2 t \right)} + 4 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t.\end{aligned}
$$

## generated observed-bank variant — trig2 / observed:trig2:legacy

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/6b0b7e765fb34366247525e153bbd81c97f941fff9f29b81f68474086a16795a.png)

Which integral expression gives the arc length of the curve $g(t)=\langle \sin{\left(3 t \right)},\,\cos{\left(2 t \right)}\rangle$ from $t=0$ to $t=\pi?$

- $\int_{0}^{1}\sqrt{2 \sin^{2}{\left(2 t \right)} + 3 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{4 \sin^{2}{\left(2 t \right)} + 9 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$ **correct**
- $\int_{0}^{\pi}\sqrt{4 \sin^{2}{\left(2 t \right)} + 3 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{3 \sin^{2}{\left(3 t \right)} + 4 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{9 \sin^{2}{\left(3 t \right)} + 4 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$

First, we find $g'(t)$ and $\|g'(t)\|:$

$$
\begin{aligned}g'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(3 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(\cos{\left(2 t \right)})\rangle \\  & =\langle 3 \cos{\left(3 t \right)},\,- 2 \sin{\left(2 t \right)}\rangle \\ \|g'(t)\| & =\sqrt{\left(- 2 \sin{\left(2 t \right)}\right)^{2} + \left(3 \cos{\left(3 t \right)}\right)^{2}} \\  & =\sqrt{4 \sin^{2}{\left(2 t \right)} + 9 \cos^{2}{\left(3 t \right)}}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{0}^{\pi}\|g'(t)\|\,\mathrm{d}t \\  & =\int_{0}^{\pi}\sqrt{4 \sin^{2}{\left(2 t \right)} + 9 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t.\end{aligned}
$$

## original-parameter replay — exp_basis / observed:exp_basis

Which integral  expression gives the arc length of the curve $f(t)=e^{t}\big((1)\,i+(2)\,j+(t)\,k\big)$ from $t=1$ to $t=2?$

- $\int_{1}^{2}\sqrt{t^{2} + 2 t + 5} e^{t}\,\mathrm{d}t$
- $\int_{1}^{2}\sqrt{t^{2} + 2 t + 4} e^{t}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{t^{2} + 2 t + 2} e^{t}\,\mathrm{d}t$
- $\int_{1}^{2}\sqrt{t^{2} + 2 t + 6} e^{t}\,\mathrm{d}t$ **correct**
- $\int_{0}^{1}\left(t + 2\right) e^{t}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(e^{t}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(2 e^{t}))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(t e^{t}))\,k \\  & =(e^{t})\,i+(2 e^{t})\,j+(t e^{t} + e^{t})\,k \\ \|f'(t)\| & =\sqrt{\left(t e^{t} + e^{t}\right)^{2} + \left(e^{t}\right)^{2} + \left(2 e^{t}\right)^{2}} \\  & =\sqrt{\left(t^{2} + 2 t + 1\right) e^{2 t} + e^{2 t} + 4 e^{2 t}} \\  & =\sqrt{\left(t^{2} + 2 t + 1 + 1 + 4\right) e^{2 t}} \\  & =\sqrt{t^{2} + 2 t + 6} e^{t}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{1}^{2}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{1}^{2}\sqrt{t^{2} + 2 t + 6} e^{t}\,\mathrm{d}t.\end{aligned}
$$

## generated observed-bank variant — exp_basis / observed:exp_basis

Which integral  expression gives the arc length of the curve $f(t)=e^{t}\big((4)\,i+(3)\,j+(2 t)\,k\big)$ from $t=1$ to $t=2?$

- $\int_{1}^{2}\sqrt{4 t^{2} + 8 t + 25} e^{t}\,\mathrm{d}t$
- $\int_{0}^{1}\left(2 t + 3\right) e^{t}\,\mathrm{d}t$
- $\int_{1}^{2}\sqrt{4 t^{2} + 8 t + 9} e^{t}\,\mathrm{d}t$
- $\int_{1}^{2}\sqrt{4 t^{2} + 8 t + 29} e^{t}\,\mathrm{d}t$ **correct**
- $\int_{0}^{1}\sqrt{4 t^{2} + 8 t + 8} e^{t}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(4 e^{t}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(3 e^{t}))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(2 t e^{t}))\,k \\  & =(4 e^{t})\,i+(3 e^{t})\,j+(2 t e^{t} + 2 e^{t})\,k \\ \|f'(t)\| & =\sqrt{\left(2 t e^{t} + 2 e^{t}\right)^{2} + \left(3 e^{t}\right)^{2} + \left(4 e^{t}\right)^{2}} \\  & =\sqrt{\left(t^{2} + 2 t + 1\right) 4 e^{2 t} + 9 e^{2 t} + 16 e^{2 t}} \\  & =\sqrt{\left(4 t^{2} + 8 t + 4 + 9 + 16\right) e^{2 t}} \\  & =\sqrt{4 t^{2} + 8 t + 29} e^{t}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{1}^{2}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{1}^{2}\sqrt{4 t^{2} + 8 t + 29} e^{t}\,\mathrm{d}t.\end{aligned}
$$

## generated observed-bank variant — exp_basis / observed:exp_basis

Which integral  expression gives the arc length of the curve $f(t)=e^{t}\big((1)\,i+(1)\,j+(3 t)\,k\big)$ from $t=1$ to $t=2?$

- $\int_{1}^{2}\sqrt{9 t^{2} + 18 t + 11} e^{t}\,\mathrm{d}t$ **correct**
- $\int_{1}^{2}\sqrt{9 t^{2} + 18 t + 1} e^{t}\,\mathrm{d}t$
- $\int_{1}^{2}\sqrt{9 t^{2} + 18 t + 2} e^{t}\,\mathrm{d}t$
- $\int_{0}^{1}\left(3 t + 1\right) e^{t}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{9 t^{2} + 18 t + 18} e^{t}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(e^{t}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(e^{t}))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(3 t e^{t}))\,k \\  & =(e^{t})\,i+(e^{t})\,j+(3 t e^{t} + 3 e^{t})\,k \\ \|f'(t)\| & =\sqrt{\left(3 t e^{t} + 3 e^{t}\right)^{2} + \left(e^{t}\right)^{2} + \left(e^{t}\right)^{2}} \\  & =\sqrt{\left(t^{2} + 2 t + 1\right) 9 e^{2 t} + e^{2 t} + e^{2 t}} \\  & =\sqrt{\left(9 t^{2} + 18 t + 1 + 1 + 9\right) e^{2 t}} \\  & =\sqrt{9 t^{2} + 18 t + 11} e^{t}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{1}^{2}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{1}^{2}\sqrt{9 t^{2} + 18 t + 11} e^{t}\,\mathrm{d}t.\end{aligned}
$$

## original-parameter replay — trig3 / observed:trig3

Which integral expression gives the arc length of the curve $f(t)=\langle 4 \cos{\left(t \right)},\,3 \sin{\left(t \right)},\,4 \sin{\left(t \right)}\rangle$ from $t=\frac{\pi}{6}$ to $t=\frac{\pi}{4}?$

- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{16 \cos^{2}{\left(t \right)} + 9}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{9 \sin^{2}{\left(t \right)} + 16}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{3 \cos^{2}{\left(t \right)} + 4}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{4 \sin^{2}{\left(t \right)} + 3}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{9 \cos^{2}{\left(t \right)} + 16}\,\mathrm{d}t$ **correct**

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(4 \cos{\left(t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(3 \sin{\left(t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(t \right)})\rangle \\  & =\langle - 4 \sin{\left(t \right)},\,3 \cos{\left(t \right)},\,4 \cos{\left(t \right)}\rangle \\ \|f'(t)\| & =\sqrt{\left(- 4 \sin{\left(t \right)}\right)^{2} + \left(3 \cos{\left(t \right)}\right)^{2} + \left(4 \cos{\left(t \right)}\right)^{2}} \\  & =\sqrt{16 \sin^{2}{\left(t \right)} + 9 \cos^{2}{\left(t \right)} + 16 \cos^{2}{\left(t \right)}} \\  & =\sqrt{16 \left(\sin^{2}{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + 9 \cos^{2}{\left(t \right)}} \\  & =\sqrt{9 \cos^{2}{\left(t \right)} + 16}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{9 \cos^{2}{\left(t \right)} + 16}\,\mathrm{d}t.\end{aligned}
$$

## generated observed-bank variant — trig3 / observed:trig3

Which integral expression gives the arc length of the curve $f(t)=\langle 4 \cos{\left(t \right)},\,3 \sin{\left(t \right)},\,4 \sin{\left(t \right)}\rangle$ from $t=\frac{\pi}{6}$ to $t=\frac{\pi}{4}?$

- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{16 \cos^{2}{\left(t \right)} + 9}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{9 \sin^{2}{\left(t \right)} + 16}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{4 \sin^{2}{\left(t \right)} + 3}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{9 \cos^{2}{\left(t \right)} + 16}\,\mathrm{d}t$ **correct**
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{3 \cos^{2}{\left(t \right)} + 4}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(4 \cos{\left(t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(3 \sin{\left(t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(t \right)})\rangle \\  & =\langle - 4 \sin{\left(t \right)},\,3 \cos{\left(t \right)},\,4 \cos{\left(t \right)}\rangle \\ \|f'(t)\| & =\sqrt{\left(- 4 \sin{\left(t \right)}\right)^{2} + \left(3 \cos{\left(t \right)}\right)^{2} + \left(4 \cos{\left(t \right)}\right)^{2}} \\  & =\sqrt{16 \sin^{2}{\left(t \right)} + 9 \cos^{2}{\left(t \right)} + 16 \cos^{2}{\left(t \right)}} \\  & =\sqrt{16 \left(\sin^{2}{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + 9 \cos^{2}{\left(t \right)}} \\  & =\sqrt{9 \cos^{2}{\left(t \right)} + 16}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{9 \cos^{2}{\left(t \right)} + 16}\,\mathrm{d}t.\end{aligned}
$$

## generated observed-bank variant — trig3 / observed:trig3

Which integral expression gives the arc length of the curve $f(t)=\langle \cos{\left(t \right)},\,2 \sin{\left(t \right)},\,\sin{\left(t \right)}\rangle$ from $t=\frac{\pi}{6}$ to $t=\frac{\pi}{4}?$

- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{\sin^{2}{\left(t \right)} + 2}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{4 \cos^{2}{\left(t \right)} + 1}\,\mathrm{d}t$ **correct**
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{\cos^{2}{\left(t \right)} + 4}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{2 \cos^{2}{\left(t \right)} + 1}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{4 \sin^{2}{\left(t \right)} + 1}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(\cos{\left(t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(2 \sin{\left(t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(t \right)})\rangle \\  & =\langle - \sin{\left(t \right)},\,2 \cos{\left(t \right)},\,\cos{\left(t \right)}\rangle \\ \|f'(t)\| & =\sqrt{\left(- \sin{\left(t \right)}\right)^{2} + \cos^{2}{\left(t \right)} + \left(2 \cos{\left(t \right)}\right)^{2}} \\  & =\sqrt{\sin^{2}{\left(t \right)} + \cos^{2}{\left(t \right)} + 4 \cos^{2}{\left(t \right)}} \\  & =\sqrt{1 \left(\sin^{2}{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + 4 \cos^{2}{\left(t \right)}} \\  & =\sqrt{4 \cos^{2}{\left(t \right)} + 1}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{4 \cos^{2}{\left(t \right)} + 1}\,\mathrm{d}t.\end{aligned}
$$

## original-parameter replay — paired_exp / observed:paired_exp

Which integral expression gives the arc length of the curve $f(t)=\langle \sin{\left(t \right)} + \cos{\left(t \right)},\,e^{t},\,\sin{\left(t \right)} - \cos{\left(t \right)}\rangle$ from $t=-1$ to $t=1?$

- $\int_{-1}^{1}\sqrt{e^{2 t} + 2}\,\mathrm{d}t$ **correct**
- $\int_{-1}^{1}2 \sqrt{e^{t} + 2}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{2 e^{t} + 1}\,\mathrm{d}t$
- $\int_{-1}^{1}2 \sqrt{2 e^{2 t} + 1}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{e^{2 t} + 1}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(t \right)} + \cos{\left(t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(e^{t}),\,\frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(t \right)} - \cos{\left(t \right)})\rangle \\  & =\langle - \sin{\left(t \right)} + \cos{\left(t \right)},\,e^{t},\,\sin{\left(t \right)} + \cos{\left(t \right)}\rangle \\ \|f'(t)\| & =\sqrt{\left(- \sin{\left(t \right)} + \cos{\left(t \right)}\right)^{2} + \left(\sin{\left(t \right)} + \cos{\left(t \right)}\right)^{2} + \left(e^{t}\right)^{2}} \\  & =\sqrt{\left(\sin^{2}{\left(t \right)} - 2 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + \left(\sin^{2}{\left(t \right)} + 2 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + e^{2 t}} \\  & =\sqrt{2 \left(\sin^{2}{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + e^{2 t}} \\  & =\sqrt{e^{2 t} + 2}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{-1}^{1}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{-1}^{1}\sqrt{e^{2 t} + 2}\,\mathrm{d}t.\end{aligned}
$$

## generated observed-bank variant — paired_exp / observed:paired_exp

Which integral expression gives the arc length of the curve $f(t)=\langle 4 \sin{\left(2 t \right)} + 4 \cos{\left(2 t \right)},\,2 e^{t},\,4 \sin{\left(2 t \right)} - 4 \cos{\left(2 t \right)}\rangle$ from $t=-1$ to $t=1?$

- $\int_{-1}^{1}2 \sqrt{e^{2 t} + 32}\,\mathrm{d}t$ **correct**
- $\int_{-1}^{1}\sqrt{4 e^{t} + 64}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{4 e^{2 t} + 64}\,\mathrm{d}t$
- $\int_{-1}^{1}2 \sqrt{2 e^{t} + 128}\,\mathrm{d}t$
- $\int_{-1}^{1}2 \sqrt{8 e^{2 t} + 64}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(2 t \right)} + 4 \cos{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(2 e^{t}),\,\frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(2 t \right)} - 4 \cos{\left(2 t \right)})\rangle \\  & =\langle - 8 \sin{\left(2 t \right)} + 8 \cos{\left(2 t \right)},\,2 e^{t},\,8 \sin{\left(2 t \right)} + 8 \cos{\left(2 t \right)}\rangle \\ \|f'(t)\| & =\sqrt{\left(- 8 \sin{\left(2 t \right)} + 8 \cos{\left(2 t \right)}\right)^{2} + \left(8 \sin{\left(2 t \right)} + 8 \cos{\left(2 t \right)}\right)^{2} + \left(2 e^{t}\right)^{2}} \\  & =\sqrt{\left(64 \sin^{2}{\left(2 t \right)} - 128 \sin{\left(2 t \right)} \cos{\left(2 t \right)} + 64 \cos^{2}{\left(2 t \right)}\right) + \left(64 \sin^{2}{\left(2 t \right)} + 128 \sin{\left(2 t \right)} \cos{\left(2 t \right)} + 64 \cos^{2}{\left(2 t \right)}\right) + 4 e^{2 t}} \\  & =\sqrt{128 \left(\sin^{2}{\left(2 t \right)} + \cos^{2}{\left(2 t \right)}\right) + 4 e^{2 t}} \\  & =\sqrt{4 e^{2 t} + 128}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{-1}^{1}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{-1}^{1}2 \sqrt{e^{2 t} + 32}\,\mathrm{d}t.\end{aligned}
$$

## generated observed-bank variant — paired_exp / observed:paired_exp

Which integral expression gives the arc length of the curve $f(t)=\langle \sin{\left(t \right)} + \cos{\left(t \right)},\,3 e^{t},\,\sin{\left(t \right)} - \cos{\left(t \right)}\rangle$ from $t=-1$ to $t=1?$

- $\int_{-1}^{1}2 \sqrt{18 e^{2 t} + 1}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{9 e^{2 t} + 2}\,\mathrm{d}t$ **correct**
- $\int_{-1}^{1}2 \sqrt{3 e^{t} + 2}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{9 e^{2 t} + 1}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{6 e^{t} + 1}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(t \right)} + \cos{\left(t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(3 e^{t}),\,\frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(t \right)} - \cos{\left(t \right)})\rangle \\  & =\langle - \sin{\left(t \right)} + \cos{\left(t \right)},\,3 e^{t},\,\sin{\left(t \right)} + \cos{\left(t \right)}\rangle \\ \|f'(t)\| & =\sqrt{\left(- \sin{\left(t \right)} + \cos{\left(t \right)}\right)^{2} + \left(\sin{\left(t \right)} + \cos{\left(t \right)}\right)^{2} + \left(3 e^{t}\right)^{2}} \\  & =\sqrt{\left(\sin^{2}{\left(t \right)} - 2 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + \left(\sin^{2}{\left(t \right)} + 2 \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + 9 e^{2 t}} \\  & =\sqrt{2 \left(\sin^{2}{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + 9 e^{2 t}} \\  & =\sqrt{9 e^{2 t} + 2}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{-1}^{1}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{-1}^{1}\sqrt{9 e^{2 t} + 2}\,\mathrm{d}t.\end{aligned}
$$

## original-parameter replay — quad_helix / observed:quad_helix

Which integral  expression gives the arc length of the curve $f(t)=\langle \sin{\left(2 t \right)},\,\cos{\left(2 t \right)},\,t^{2}\rangle$
from  $t=0$ to $t=1?$

- $\int_{0}^{1}\sqrt{4 t^{2} + 1}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{t^{2} + 1}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{2} \sqrt{t^{2} + 1}\,\mathrm{d}t$
- $\int_{0}^{1}2 \sqrt{t^{2} + 1}\,\mathrm{d}t$ **correct**
- $\int_{0}^{1}2 \sqrt{t^{2} - \sin^{2}{\left(2 t \right)} + \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(\cos{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(t^{2})\rangle \\  & =\langle 2 \cos{\left(2 t \right)},\,- 2 \sin{\left(2 t \right)},\,2 t\rangle \\ \|f'(t)\| & =\sqrt{\left(2 t\right)^{2} + \left(- 2 \sin{\left(2 t \right)}\right)^{2} + \left(2 \cos{\left(2 t \right)}\right)^{2}} \\  & =\sqrt{4 t^{2} + 4 \sin^{2}{\left(2 t \right)} + 4 \cos^{2}{\left(2 t \right)}} \\  & =\sqrt{4 \left(t^{2} + \sin^{2}{\left(2 t \right)} + \cos^{2}{\left(2 t \right)}\right)} \\  & =\sqrt{4 t^{2} + 4}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{1}\|f'(t)\|\,\mathrm{d}t=\int_{0}^{1}2 \sqrt{t^{2} + 1}\,\mathrm{d}t\end{aligned}
$$

## generated observed-bank variant — quad_helix / observed:quad_helix

Which integral  expression gives the arc length of the curve $f(t)=\langle 4 \sin{\left(2 t \right)},\,4 \cos{\left(2 t \right)},\,2 t^{2}\rangle$
from  $t=0$ to $t=1?$

- $\int_{0}^{1}\sqrt{16 t^{2} + 16}\,\mathrm{d}t$
- $\int_{0}^{1}2 \sqrt{4 t^{2} - 16 \sin^{2}{\left(2 t \right)} + 16 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{4 t^{2} + 16}\,\mathrm{d}t$
- $\int_{0}^{1}4 \sqrt{t^{2} + 4}\,\mathrm{d}t$ **correct**
- $\int_{0}^{1}\sqrt{2} \sqrt{4 t^{2} + 16}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(4 \cos{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(2 t^{2})\rangle \\  & =\langle 8 \cos{\left(2 t \right)},\,- 8 \sin{\left(2 t \right)},\,4 t\rangle \\ \|f'(t)\| & =\sqrt{\left(4 t\right)^{2} + \left(- 8 \sin{\left(2 t \right)}\right)^{2} + \left(8 \cos{\left(2 t \right)}\right)^{2}} \\  & =\sqrt{16 t^{2} + 64 \sin^{2}{\left(2 t \right)} + 64 \cos^{2}{\left(2 t \right)}} \\  & =\sqrt{64 \left(\frac{t^{2}}{4} + \sin^{2}{\left(2 t \right)} + \cos^{2}{\left(2 t \right)}\right)} \\  & =\sqrt{16 t^{2} + 64}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{1}\|f'(t)\|\,\mathrm{d}t=\int_{0}^{1}4 \sqrt{t^{2} + 4}\,\mathrm{d}t\end{aligned}
$$

## generated observed-bank variant — quad_helix / observed:quad_helix

Which integral  expression gives the arc length of the curve $f(t)=\langle \sin{\left(3 t \right)},\,\cos{\left(3 t \right)},\,t^{2}\rangle$
from  $t=0$ to $t=1?$

- $\int_{0}^{1}\sqrt{3} \sqrt{t^{2} + 1}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{t^{2} + 1}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{4 t^{2} + 1}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{4 t^{2} + 9}\,\mathrm{d}t$ **correct**
- $\int_{0}^{1}3 \sqrt{t^{2} - \sin^{2}{\left(3 t \right)} + \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(3 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(\cos{\left(3 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(t^{2})\rangle \\  & =\langle 3 \cos{\left(3 t \right)},\,- 3 \sin{\left(3 t \right)},\,2 t\rangle \\ \|f'(t)\| & =\sqrt{\left(2 t\right)^{2} + \left(- 3 \sin{\left(3 t \right)}\right)^{2} + \left(3 \cos{\left(3 t \right)}\right)^{2}} \\  & =\sqrt{4 t^{2} + 9 \sin^{2}{\left(3 t \right)} + 9 \cos^{2}{\left(3 t \right)}} \\  & =\sqrt{9 \left(\frac{4 t^{2}}{9} + \sin^{2}{\left(3 t \right)} + \cos^{2}{\left(3 t \right)}\right)} \\  & =\sqrt{4 t^{2} + 9}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{1}\|f'(t)\|\,\mathrm{d}t=\int_{0}^{1}\sqrt{4 t^{2} + 9}\,\mathrm{d}t\end{aligned}
$$

## original-parameter replay — spiral / observed:spiral

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/b282ef57d9b8e5c61b0a112bd12a6af2a80b0cfd5f9f5ede2f96f44decf714b3.png)

Which integral  expression gives the arc length of the curve $g(t)=\langle t \sin{\left(t \right)},\,- t \cos{\left(t \right)} + 2\rangle$
from  $t=0$ to $t=\pi?$

- $\int_{0}^{\pi}\sqrt{t^{2} + 1}\,\mathrm{d}t$ **correct**
- $\int_{0}^{\pi}\sqrt{t^{2} + 2 t \sin{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{2} \left(t \cos{\left(t \right)} + \sin{\left(t \right)}\right)\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{2 t^{2} + 1}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{t^{2} + 2}\,\mathrm{d}t$

First, we find $g'(t)$ and $\|g'(t)\|:$

$$
\begin{aligned}g'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(t \sin{\left(t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(- t \cos{\left(t \right)} + 2)\rangle \\  & =\langle t \cos{\left(t \right)} + \sin{\left(t \right)},\,t \sin{\left(t \right)} - \cos{\left(t \right)}\rangle \\ \|g'(t)\| & =\sqrt{\left(t \sin{\left(t \right)} - \cos{\left(t \right)}\right)^{2} + \left(t \cos{\left(t \right)} + \sin{\left(t \right)}\right)^{2}} \\  & =\sqrt{\left(t^{2} \sin^{2}{\left(t \right)} - 2 t \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + \left(t^{2} \cos^{2}{\left(t \right)} + 2 t \sin{\left(t \right)} \cos{\left(t \right)} + \sin^{2}{\left(t \right)}\right)} \\  & =\sqrt{t^{2} + 1}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{\pi}\|g'(t)\|\,\mathrm{d}t=\int_{0}^{\pi}\sqrt{t^{2} + 1}\,\mathrm{d}t\end{aligned}
$$

## generated observed-bank variant — spiral / observed:spiral

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/f365a2a7ad443c37febb69d409ec4c9d6cbc24ab76cab27cee751eda79243567.png)

Which integral  expression gives the arc length of the curve $g(t)=\langle 4 t \sin{\left(2 t \right)},\,- 4 t \cos{\left(2 t \right)} - 2\rangle$
from  $t=0$ to $t=\pi?$

- $\int_{0}^{\pi}4 \sqrt{4 t^{2} + 1}\,\mathrm{d}t$ **correct**
- $\int_{0}^{\pi}\sqrt{64 t^{2} + 32}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{64 t^{2} + 64 t \sin{\left(4 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{128 t^{2} + 16}\,\mathrm{d}t$
- $\int_{0}^{\pi}4 \sqrt{2} \left(2 t \cos{\left(2 t \right)} + \sin{\left(2 t \right)}\right)\,\mathrm{d}t$

First, we find $g'(t)$ and $\|g'(t)\|:$

$$
\begin{aligned}g'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(4 t \sin{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(- 4 t \cos{\left(2 t \right)} - 2)\rangle \\  & =\langle 8 t \cos{\left(2 t \right)} + 4 \sin{\left(2 t \right)},\,8 t \sin{\left(2 t \right)} - 4 \cos{\left(2 t \right)}\rangle \\ \|g'(t)\| & =\sqrt{\left(8 t \sin{\left(2 t \right)} - 4 \cos{\left(2 t \right)}\right)^{2} + \left(8 t \cos{\left(2 t \right)} + 4 \sin{\left(2 t \right)}\right)^{2}} \\  & =\sqrt{\left(64 t^{2} \sin^{2}{\left(2 t \right)} - 64 t \sin{\left(2 t \right)} \cos{\left(2 t \right)} + 16 \cos^{2}{\left(2 t \right)}\right) + \left(64 t^{2} \cos^{2}{\left(2 t \right)} + 64 t \sin{\left(2 t \right)} \cos{\left(2 t \right)} + 16 \sin^{2}{\left(2 t \right)}\right)} \\  & =\sqrt{64 t^{2} + 16}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{\pi}\|g'(t)\|\,\mathrm{d}t=\int_{0}^{\pi}4 \sqrt{4 t^{2} + 1}\,\mathrm{d}t\end{aligned}
$$

## generated observed-bank variant — spiral / observed:spiral

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/b282ef57d9b8e5c61b0a112bd12a6af2a80b0cfd5f9f5ede2f96f44decf714b3.png)

Which integral  expression gives the arc length of the curve $g(t)=\langle t \sin{\left(t \right)},\,- t \cos{\left(t \right)} + 2\rangle$
from  $t=0$ to $t=\pi?$

- $\int_{0}^{\pi}\sqrt{2 t^{2} + 1}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{t^{2} + 2}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{t^{2} + 1}\,\mathrm{d}t$ **correct**
- $\int_{0}^{\pi}\sqrt{2} \left(t \cos{\left(t \right)} + \sin{\left(t \right)}\right)\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{t^{2} + 2 t \sin{\left(2 t \right)}}\,\mathrm{d}t$

First, we find $g'(t)$ and $\|g'(t)\|:$

$$
\begin{aligned}g'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(t \sin{\left(t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(- t \cos{\left(t \right)} + 2)\rangle \\  & =\langle t \cos{\left(t \right)} + \sin{\left(t \right)},\,t \sin{\left(t \right)} - \cos{\left(t \right)}\rangle \\ \|g'(t)\| & =\sqrt{\left(t \sin{\left(t \right)} - \cos{\left(t \right)}\right)^{2} + \left(t \cos{\left(t \right)} + \sin{\left(t \right)}\right)^{2}} \\  & =\sqrt{\left(t^{2} \sin^{2}{\left(t \right)} - 2 t \sin{\left(t \right)} \cos{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + \left(t^{2} \cos^{2}{\left(t \right)} + 2 t \sin{\left(t \right)} \cos{\left(t \right)} + \sin^{2}{\left(t \right)}\right)} \\  & =\sqrt{t^{2} + 1}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{\pi}\|g'(t)\|\,\mathrm{d}t=\int_{0}^{\pi}\sqrt{t^{2} + 1}\,\mathrm{d}t\end{aligned}
$$

## original-parameter replay — helix_basis / observed:helix_basis

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/79b01fb4013ede4fe89cb9240b557d0e05d1cf38ca038a1285ae18d4799ab881.png)

Which integral  expression gives the arc length of the curve $h(t)=(\cos{\left(t \right)})\,i+(\sin{\left(t \right)})\,j+(t)\,k$ from $t=0$ to $t=2 \pi?$

- $\int_{0}^{2 \pi}\sqrt{2 \sin^{2}{\left(t \right)} + \cos^{2}{\left(t \right)}}\,\mathrm{d}t$
- $\int_{0}^{2 \pi}\sqrt{\sin^{2}{\left(t \right)} + 2}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{3 - \sin^{2}{\left(t \right)}}\,\mathrm{d}t$
- $\int_{0}^{2 \pi}\sqrt{\cos^{2}{\left(t \right)} + 2}\,\mathrm{d}t$
- $\int_{0}^{2 \pi}\sqrt{2}\,\mathrm{d}t$ **correct**

First, we find $h'(t)$ and $\|h'(t)\|:$

$$
\begin{aligned}h'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(\cos{\left(t \right)}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(t \right)}))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(t))\,k \\  & =(- \sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j+(1)\,k \\ \|h'(t)\| & =\sqrt{\left(- \sin{\left(t \right)}\right)^{2} + \cos^{2}{\left(t \right)} + 1^{2}} \\  & =\sqrt{\sin^{2}{\left(t \right)} + \cos^{2}{\left(t \right)} + 1} \\  & =\sqrt{2}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{2 \pi}\|h'(t)\|\,\mathrm{d}t=\int_{0}^{2 \pi}\sqrt{2}\,\mathrm{d}t\end{aligned}
$$

## generated observed-bank variant — helix_basis / observed:helix_basis

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/90313df445a432e84bda39f12b0740937b9dcc73f2d4e2dbc2673dca7f598af3.png)

Which integral  expression gives the arc length of the curve $h(t)=(4 \cos{\left(2 t \right)})\,i+(4 \sin{\left(2 t \right)})\,j+(2 t)\,k$ from $t=0$ to $t=2 \pi?$

- $\int_{0}^{2 \pi}\sqrt{128 \sin^{2}{\left(2 t \right)} + 64 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{2 \pi}\sqrt{68}\,\mathrm{d}t$ **correct**
- $\int_{0}^{2 \pi}\sqrt{64 \sin^{2}{\left(2 t \right)} + 68}\,\mathrm{d}t$
- $\int_{0}^{2 \pi}\sqrt{64 \cos^{2}{\left(2 t \right)} + 68}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{192 - 64 \sin^{2}{\left(2 t \right)}}\,\mathrm{d}t$

First, we find $h'(t)$ and $\|h'(t)\|:$

$$
\begin{aligned}h'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(4 \cos{\left(2 t \right)}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(2 t \right)}))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(2 t))\,k \\  & =(- 8 \sin{\left(2 t \right)})\,i+(8 \cos{\left(2 t \right)})\,j+(2)\,k \\ \|h'(t)\| & =\sqrt{\left(- 8 \sin{\left(2 t \right)}\right)^{2} + \left(8 \cos{\left(2 t \right)}\right)^{2} + 2^{2}} \\  & =\sqrt{64 \sin^{2}{\left(2 t \right)} + 64 \cos^{2}{\left(2 t \right)} + 4} \\  & =\sqrt{68}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{2 \pi}\|h'(t)\|\,\mathrm{d}t=\int_{0}^{2 \pi}\sqrt{68}\,\mathrm{d}t\end{aligned}
$$

## generated observed-bank variant — helix_basis / observed:helix_basis

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/d3f74486caccd085144475863f44de572916af36947eb1c6ce02e43ea86d8563.png)

Which integral  expression gives the arc length of the curve $h(t)=(\cos{\left(t \right)})\,i+(\sin{\left(t \right)})\,j+(3 t)\,k$ from $t=0$ to $t=2 \pi?$

- $\int_{0}^{2 \pi}\sqrt{\cos^{2}{\left(t \right)} + 10}\,\mathrm{d}t$
- $\int_{0}^{2 \pi}\sqrt{\sin^{2}{\left(t \right)} + 10}\,\mathrm{d}t$
- $\int_{0}^{2 \pi}\sqrt{2 \sin^{2}{\left(t \right)} + \cos^{2}{\left(t \right)}}\,\mathrm{d}t$
- $\int_{0}^{2 \pi}\sqrt{10}\,\mathrm{d}t$ **correct**
- $\int_{0}^{\pi}\sqrt{3 - \sin^{2}{\left(t \right)}}\,\mathrm{d}t$

First, we find $h'(t)$ and $\|h'(t)\|:$

$$
\begin{aligned}h'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(\cos{\left(t \right)}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(\sin{\left(t \right)}))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(3 t))\,k \\  & =(- \sin{\left(t \right)})\,i+(\cos{\left(t \right)})\,j+(3)\,k \\ \|h'(t)\| & =\sqrt{\left(- \sin{\left(t \right)}\right)^{2} + \cos^{2}{\left(t \right)} + 3^{2}} \\  & =\sqrt{\sin^{2}{\left(t \right)} + \cos^{2}{\left(t \right)} + 9} \\  & =\sqrt{10}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{2 \pi}\|h'(t)\|\,\mathrm{d}t=\int_{0}^{2 \pi}\sqrt{10}\,\mathrm{d}t\end{aligned}
$$

## original-parameter replay — power_basis / observed:power_basis

Which integral expression gives the arc length of the curve $r(t)=(t^{3})\,i+(3 t)\,j+(t^{4})\,k$ from $t=2$ to $t=5?$

- $\int_{2}^{5}\sqrt{16 t^{6} + 9 t^{4} + 9}\,\mathrm{d}t$ **correct**
- $\int_{2}^{5}\sqrt{8 t^{5} + 9 t^{3} + 6}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{t^{6} + t^{4} + 9}\,\mathrm{d}t$
- $\int_{0}^{5}\sqrt{16 t^{6} + 9}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{16 t^{6} + 9 t^{4}}\,\mathrm{d}t$

First, we find $r'(t)$ and $\|r'(t)\|:$

$$
\begin{aligned}r'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(t^{3}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(3 t))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(t^{4}))\,k \\  & =(3 t^{2})\,i+(3)\,j+(4 t^{3})\,k \\ \|r'(t)\| & =\sqrt{\left(3 t^{2}\right)^{2} + \left(4 t^{3}\right)^{2} + 3^{2}} \\  & =\sqrt{16 t^{6} + 9 t^{4} + 9}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{2}^{5}\|r'(t)\|\,\mathrm{d}t=\int_{2}^{5}\sqrt{16 t^{6} + 9 t^{4} + 9}\,\mathrm{d}t\end{aligned}
$$

## generated observed-bank variant — power_basis / observed:power_basis

Which integral expression gives the arc length of the curve $r(t)=(4 t^{2})\,i+(3 t)\,j+(2 t^{3})\,k$ from $t=2$ to $t=5?$

- $\int_{2}^{5}\sqrt{36 t^{4} + 64 t^{2} + 9}\,\mathrm{d}t$ **correct**
- $\int_{2}^{5}\sqrt{4 t^{4} + 16 t^{2} + 9}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{36 t^{4} + 64 t^{2}}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{12 t^{3} + 16 t + 6}\,\mathrm{d}t$
- $\int_{0}^{5}\sqrt{36 t^{4} + 9}\,\mathrm{d}t$

First, we find $r'(t)$ and $\|r'(t)\|:$

$$
\begin{aligned}r'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(4 t^{2}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(3 t))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(2 t^{3}))\,k \\  & =(8 t)\,i+(3)\,j+(6 t^{2})\,k \\ \|r'(t)\| & =\sqrt{\left(8 t\right)^{2} + \left(6 t^{2}\right)^{2} + 3^{2}} \\  & =\sqrt{36 t^{4} + 64 t^{2} + 9}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{2}^{5}\|r'(t)\|\,\mathrm{d}t=\int_{2}^{5}\sqrt{36 t^{4} + 64 t^{2} + 9}\,\mathrm{d}t\end{aligned}
$$

## generated observed-bank variant — power_basis / observed:power_basis

Which integral expression gives the arc length of the curve $r(t)=(t^{2})\,i+(t)\,j+(3 t^{3})\,k$ from $t=2$ to $t=5?$

- $\int_{0}^{5}\sqrt{81 t^{4} + 1}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{81 t^{4} + 4 t^{2} + 1}\,\mathrm{d}t$ **correct**
- $\int_{2}^{5}\sqrt{18 t^{3} + 4 t + 2}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{81 t^{4} + 4 t^{2}}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{9 t^{4} + t^{2} + 1}\,\mathrm{d}t$

First, we find $r'(t)$ and $\|r'(t)\|:$

$$
\begin{aligned}r'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(t^{2}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(t))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(3 t^{3}))\,k \\  & =(2 t)\,i+(1)\,j+(9 t^{2})\,k \\ \|r'(t)\| & =\sqrt{\left(2 t\right)^{2} + \left(9 t^{2}\right)^{2} + 1^{2}} \\  & =\sqrt{81 t^{4} + 4 t^{2} + 1}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{2}^{5}\|r'(t)\|\,\mathrm{d}t=\int_{2}^{5}\sqrt{81 t^{4} + 4 t^{2} + 1}\,\mathrm{d}t\end{aligned}
$$

## authored method bank variant — trig2 / authored_method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/22d3647f8a7d0f1c1b6961108c56f12f50e2bad57145c91471379946bbfe8d7c.png)

Which integral expression gives the arc length of the curve $g(t)=\langle 4 \sin{\left(3 t \right)},\,3 \cos{\left(t \right)}\rangle$ from $t=0$ to $t=\pi?$

- $\int_{0}^{\pi}\sqrt{16 \sin^{2}{\left(3 t \right)} + 9 \cos^{2}{\left(t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{144 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}3 \sqrt{\sin^{2}{\left(t \right)} + 16 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$ **correct**
- $\int_{0}^{1 + \pi}3 \sqrt{\sin^{2}{\left(t \right)} + 16 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}9 \sin^{2}{\left(t \right)} + 144 \cos^{2}{\left(3 t \right)}\,\mathrm{d}t$

First, we find $g'(t)$ and $\|g'(t)\|:$

$$
\begin{aligned}g'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(3 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(3 \cos{\left(t \right)})\rangle \\  & =\langle 12 \cos{\left(3 t \right)},\,- 3 \sin{\left(t \right)}\rangle \\ \|g'(t)\| & =\sqrt{\left(- 3 \sin{\left(t \right)}\right)^{2} + \left(12 \cos{\left(3 t \right)}\right)^{2}} \\  & =\sqrt{9 \sin^{2}{\left(t \right)} + 144 \cos^{2}{\left(3 t \right)}}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{0}^{\pi}\|g'(t)\|\,\mathrm{d}t \\  & =\int_{0}^{\pi}3 \sqrt{\sin^{2}{\left(t \right)} + 16 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t.\end{aligned}
$$

## authored method bank variant — trig2 / authored_method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/1eb6b22656f8c2cefccf7b3a4d0ef61aa1f3f13a2c7d21b135b4b379fc14103d.png)

Which integral expression gives the arc length of the curve $g(t)=\langle 2 \sin{\left(3 t \right)},\,4 \cos{\left(2 t \right)}\rangle$ from $t=0$ to $t=\pi?$

- $\int_{0}^{\pi}2 \sqrt{16 \sin^{2}{\left(2 t \right)} + 9 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$ **correct**
- $\int_{0}^{\pi}64 \sin^{2}{\left(2 t \right)} + 36 \cos^{2}{\left(3 t \right)}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{36 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{1 + \pi}2 \sqrt{16 \sin^{2}{\left(2 t \right)} + 9 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{4 \sin^{2}{\left(3 t \right)} + 16 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$

First, we find $g'(t)$ and $\|g'(t)\|:$

$$
\begin{aligned}g'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(2 \sin{\left(3 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(4 \cos{\left(2 t \right)})\rangle \\  & =\langle 6 \cos{\left(3 t \right)},\,- 8 \sin{\left(2 t \right)}\rangle \\ \|g'(t)\| & =\sqrt{\left(- 8 \sin{\left(2 t \right)}\right)^{2} + \left(6 \cos{\left(3 t \right)}\right)^{2}} \\  & =\sqrt{64 \sin^{2}{\left(2 t \right)} + 36 \cos^{2}{\left(3 t \right)}}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{0}^{\pi}\|g'(t)\|\,\mathrm{d}t \\  & =\int_{0}^{\pi}2 \sqrt{16 \sin^{2}{\left(2 t \right)} + 9 \cos^{2}{\left(3 t \right)}}\,\mathrm{d}t.\end{aligned}
$$

## authored method bank variant — exp_basis / authored_method

Which integral  expression gives the arc length of the curve $f(t)=e^{t}\big((4)\,i+(3)\,j+(4 t)\,k\big)$ from $t=1$ to $t=2?$

- $\int_{1}^{2}\sqrt{16 t^{2} e^{2 t} + 25 e^{2 t}}\,\mathrm{d}t$
- $\int_{1}^{2}\sqrt{25 e^{2 t}}\,\mathrm{d}t$
- $\int_{1}^{3}\sqrt{16 t^{2} + 32 t + 41} e^{t}\,\mathrm{d}t$
- $\int_{1}^{2}\sqrt{16 t^{2} + 32 t + 41} e^{t}\,\mathrm{d}t$ **correct**
- $\int_{1}^{2}16 t^{2} e^{2 t} + 32 t e^{2 t} + 41 e^{2 t}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(4 e^{t}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(3 e^{t}))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(4 t e^{t}))\,k \\  & =(4 e^{t})\,i+(3 e^{t})\,j+(4 t e^{t} + 4 e^{t})\,k \\ \|f'(t)\| & =\sqrt{\left(4 t e^{t} + 4 e^{t}\right)^{2} + \left(3 e^{t}\right)^{2} + \left(4 e^{t}\right)^{2}} \\  & =\sqrt{\left(t^{2} + 2 t + 1\right) 16 e^{2 t} + 9 e^{2 t} + 16 e^{2 t}} \\  & =\sqrt{\left(16 t^{2} + 32 t + 9 + 16 + 16\right) e^{2 t}} \\  & =\sqrt{16 t^{2} + 32 t + 41} e^{t}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{1}^{2}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{1}^{2}\sqrt{16 t^{2} + 32 t + 41} e^{t}\,\mathrm{d}t.\end{aligned}
$$

## authored method bank variant — exp_basis / authored_method

Which integral  expression gives the arc length of the curve $f(t)=e^{t}\big((2)\,i+(4)\,j+(3 t)\,k\big)$ from $t=1$ to $t=2?$

- $\int_{1}^{2}\sqrt{9 t^{2} + 18 t + 29} e^{t}\,\mathrm{d}t$ **correct**
- $\int_{1}^{2}9 t^{2} e^{2 t} + 18 t e^{2 t} + 29 e^{2 t}\,\mathrm{d}t$
- $\int_{1}^{2}\sqrt{20 e^{2 t}}\,\mathrm{d}t$
- $\int_{1}^{3}\sqrt{9 t^{2} + 18 t + 29} e^{t}\,\mathrm{d}t$
- $\int_{1}^{2}\sqrt{9 t^{2} e^{2 t} + 20 e^{2 t}}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(2 e^{t}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(4 e^{t}))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(3 t e^{t}))\,k \\  & =(2 e^{t})\,i+(4 e^{t})\,j+(3 t e^{t} + 3 e^{t})\,k \\ \|f'(t)\| & =\sqrt{\left(3 t e^{t} + 3 e^{t}\right)^{2} + \left(2 e^{t}\right)^{2} + \left(4 e^{t}\right)^{2}} \\  & =\sqrt{\left(t^{2} + 2 t + 1\right) 9 e^{2 t} + 4 e^{2 t} + 16 e^{2 t}} \\  & =\sqrt{\left(9 t^{2} + 18 t + 4 + 9 + 16\right) e^{2 t}} \\  & =\sqrt{9 t^{2} + 18 t + 29} e^{t}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{1}^{2}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{1}^{2}\sqrt{9 t^{2} + 18 t + 29} e^{t}\,\mathrm{d}t.\end{aligned}
$$

## authored method bank variant — trig3 / authored_method

Which integral expression gives the arc length of the curve $f(t)=\langle 4 \cos{\left(t \right)},\,3 \sin{\left(t \right)},\,4 \sin{\left(t \right)}\rangle$ from $t=\frac{\pi}{6}$ to $t=\frac{\pi}{4}?$

- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{16 \sin^{2}{\left(t \right)} + 9 \cos^{2}{\left(t \right)}}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{9 \cos^{2}{\left(t \right)} + 16}\,\mathrm{d}t$ **correct**
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{25 \sin^{2}{\left(t \right)} + 16 \cos^{2}{\left(t \right)}}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}16 \sin^{2}{\left(t \right)} + 25 \cos^{2}{\left(t \right)}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4} + 1}\sqrt{9 \cos^{2}{\left(t \right)} + 16}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(4 \cos{\left(t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(3 \sin{\left(t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(t \right)})\rangle \\  & =\langle - 4 \sin{\left(t \right)},\,3 \cos{\left(t \right)},\,4 \cos{\left(t \right)}\rangle \\ \|f'(t)\| & =\sqrt{\left(- 4 \sin{\left(t \right)}\right)^{2} + \left(3 \cos{\left(t \right)}\right)^{2} + \left(4 \cos{\left(t \right)}\right)^{2}} \\  & =\sqrt{16 \sin^{2}{\left(t \right)} + 9 \cos^{2}{\left(t \right)} + 16 \cos^{2}{\left(t \right)}} \\  & =\sqrt{16 \left(\sin^{2}{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + 9 \cos^{2}{\left(t \right)}} \\  & =\sqrt{9 \cos^{2}{\left(t \right)} + 16}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{9 \cos^{2}{\left(t \right)} + 16}\,\mathrm{d}t.\end{aligned}
$$

## authored method bank variant — trig3 / authored_method

Which integral expression gives the arc length of the curve $f(t)=\langle 2 \cos{\left(t \right)},\,4 \sin{\left(t \right)},\,2 \sin{\left(t \right)}\rangle$ from $t=\frac{\pi}{6}$ to $t=\frac{\pi}{4}?$

- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{20 \sin^{2}{\left(t \right)} + 4 \cos^{2}{\left(t \right)}}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}4 \sin^{2}{\left(t \right)} + 20 \cos^{2}{\left(t \right)}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}2 \sqrt{4 \cos^{2}{\left(t \right)} + 1}\,\mathrm{d}t$ **correct**
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\sqrt{4 \sin^{2}{\left(t \right)} + 16 \cos^{2}{\left(t \right)}}\,\mathrm{d}t$
- $\int_{\frac{\pi}{6}}^{\frac{\pi}{4} + 1}2 \sqrt{4 \cos^{2}{\left(t \right)} + 1}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(2 \cos{\left(t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(2 \sin{\left(t \right)})\rangle \\  & =\langle - 2 \sin{\left(t \right)},\,4 \cos{\left(t \right)},\,2 \cos{\left(t \right)}\rangle \\ \|f'(t)\| & =\sqrt{\left(- 2 \sin{\left(t \right)}\right)^{2} + \left(2 \cos{\left(t \right)}\right)^{2} + \left(4 \cos{\left(t \right)}\right)^{2}} \\  & =\sqrt{4 \sin^{2}{\left(t \right)} + 4 \cos^{2}{\left(t \right)} + 16 \cos^{2}{\left(t \right)}} \\  & =\sqrt{4 \left(\sin^{2}{\left(t \right)} + \cos^{2}{\left(t \right)}\right) + 16 \cos^{2}{\left(t \right)}} \\  & =\sqrt{16 \cos^{2}{\left(t \right)} + 4}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{\frac{\pi}{6}}^{\frac{\pi}{4}}2 \sqrt{4 \cos^{2}{\left(t \right)} + 1}\,\mathrm{d}t.\end{aligned}
$$

## authored method bank variant — paired_exp / authored_method

Which integral expression gives the arc length of the curve $f(t)=\langle 4 \sin{\left(2 t \right)} + 4 \cos{\left(2 t \right)},\,4 e^{2 t},\,4 \sin{\left(2 t \right)} - 4 \cos{\left(2 t \right)}\rangle$ from $t=-1$ to $t=1?$

- $\int_{-1}^{1}\sqrt{\left(- 8 \sin{\left(2 t \right)} + 8 \cos{\left(2 t \right)}\right)^{2} + 64 e^{4 t}}\,\mathrm{d}t$
- $\int_{-1}^{1}64 e^{4 t} + 128 \sin^{2}{\left(2 t \right)} + 128 \cos^{2}{\left(2 t \right)}\,\mathrm{d}t$
- $\int_{-1}^{2}8 \sqrt{e^{4 t} + 2}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{\left(4 \sin{\left(2 t \right)} - 4 \cos{\left(2 t \right)}\right)^{2} + \left(4 \sin{\left(2 t \right)} + 4 \cos{\left(2 t \right)}\right)^{2} + 16 e^{4 t}}\,\mathrm{d}t$
- $\int_{-1}^{1}8 \sqrt{e^{4 t} + 2}\,\mathrm{d}t$ **correct**

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(2 t \right)} + 4 \cos{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(4 e^{2 t}),\,\frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(2 t \right)} - 4 \cos{\left(2 t \right)})\rangle \\  & =\langle - 8 \sin{\left(2 t \right)} + 8 \cos{\left(2 t \right)},\,8 e^{2 t},\,8 \sin{\left(2 t \right)} + 8 \cos{\left(2 t \right)}\rangle \\ \|f'(t)\| & =\sqrt{\left(- 8 \sin{\left(2 t \right)} + 8 \cos{\left(2 t \right)}\right)^{2} + \left(8 \sin{\left(2 t \right)} + 8 \cos{\left(2 t \right)}\right)^{2} + \left(8 e^{2 t}\right)^{2}} \\  & =\sqrt{\left(64 \sin^{2}{\left(2 t \right)} - 128 \sin{\left(2 t \right)} \cos{\left(2 t \right)} + 64 \cos^{2}{\left(2 t \right)}\right) + \left(64 \sin^{2}{\left(2 t \right)} + 128 \sin{\left(2 t \right)} \cos{\left(2 t \right)} + 64 \cos^{2}{\left(2 t \right)}\right) + 64 e^{4 t}} \\  & =\sqrt{128 \left(\sin^{2}{\left(2 t \right)} + \cos^{2}{\left(2 t \right)}\right) + 64 e^{4 t}} \\  & =\sqrt{64 e^{4 t} + 128}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{-1}^{1}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{-1}^{1}8 \sqrt{e^{4 t} + 2}\,\mathrm{d}t.\end{aligned}
$$

## authored method bank variant — paired_exp / authored_method

Which integral expression gives the arc length of the curve $f(t)=\langle 2 \sin{\left(2 t \right)} + 2 \cos{\left(2 t \right)},\,3 e^{t},\,2 \sin{\left(2 t \right)} - 2 \cos{\left(2 t \right)}\rangle$ from $t=-1$ to $t=1?$

- $\int_{-1}^{2}\sqrt{9 e^{2 t} + 32}\,\mathrm{d}t$
- $\int_{-1}^{1}9 e^{2 t} + 32 \sin^{2}{\left(2 t \right)} + 32 \cos^{2}{\left(2 t \right)}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{9 e^{2 t} + 32}\,\mathrm{d}t$ **correct**
- $\int_{-1}^{1}\sqrt{\left(- 4 \sin{\left(2 t \right)} + 4 \cos{\left(2 t \right)}\right)^{2} + 9 e^{2 t}}\,\mathrm{d}t$
- $\int_{-1}^{1}\sqrt{\left(2 \sin{\left(2 t \right)} - 2 \cos{\left(2 t \right)}\right)^{2} + \left(2 \sin{\left(2 t \right)} + 2 \cos{\left(2 t \right)}\right)^{2} + 9 e^{2 t}}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(2 \sin{\left(2 t \right)} + 2 \cos{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(3 e^{t}),\,\frac{\mathrm{d}}{\mathrm{d}t}(2 \sin{\left(2 t \right)} - 2 \cos{\left(2 t \right)})\rangle \\  & =\langle - 4 \sin{\left(2 t \right)} + 4 \cos{\left(2 t \right)},\,3 e^{t},\,4 \sin{\left(2 t \right)} + 4 \cos{\left(2 t \right)}\rangle \\ \|f'(t)\| & =\sqrt{\left(- 4 \sin{\left(2 t \right)} + 4 \cos{\left(2 t \right)}\right)^{2} + \left(4 \sin{\left(2 t \right)} + 4 \cos{\left(2 t \right)}\right)^{2} + \left(3 e^{t}\right)^{2}} \\  & =\sqrt{\left(16 \sin^{2}{\left(2 t \right)} - 32 \sin{\left(2 t \right)} \cos{\left(2 t \right)} + 16 \cos^{2}{\left(2 t \right)}\right) + \left(16 \sin^{2}{\left(2 t \right)} + 32 \sin{\left(2 t \right)} \cos{\left(2 t \right)} + 16 \cos^{2}{\left(2 t \right)}\right) + 9 e^{2 t}} \\  & =\sqrt{32 \left(\sin^{2}{\left(2 t \right)} + \cos^{2}{\left(2 t \right)}\right) + 9 e^{2 t}} \\  & =\sqrt{9 e^{2 t} + 32}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{-1}^{1}\|f'(t)\|\,\mathrm{d}t \\  & =\int_{-1}^{1}\sqrt{9 e^{2 t} + 32}\,\mathrm{d}t.\end{aligned}
$$

## authored method bank variant — quad_helix / authored_method

Which integral  expression gives the arc length of the curve $f(t)=\langle 4 \sin{\left(2 t \right)},\,4 \cos{\left(2 t \right)},\,4 t^{2}\rangle$
from  $t=0$ to $t=1?$

- $\int_{0}^{1}\sqrt{16 t^{4} + 16 \sin^{2}{\left(2 t \right)} + 16 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{64 \sin^{2}{\left(2 t \right)} + 64 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{2}8 \sqrt{t^{2} + 1}\,\mathrm{d}t$
- $\int_{0}^{1}8 \sqrt{t^{2} + 1}\,\mathrm{d}t$ **correct**
- $\int_{0}^{1}64 t^{2} + 64 \sin^{2}{\left(2 t \right)} + 64 \cos^{2}{\left(2 t \right)}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(4 \cos{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(4 t^{2})\rangle \\  & =\langle 8 \cos{\left(2 t \right)},\,- 8 \sin{\left(2 t \right)},\,8 t\rangle \\ \|f'(t)\| & =\sqrt{\left(8 t\right)^{2} + \left(- 8 \sin{\left(2 t \right)}\right)^{2} + \left(8 \cos{\left(2 t \right)}\right)^{2}} \\  & =\sqrt{64 t^{2} + 64 \sin^{2}{\left(2 t \right)} + 64 \cos^{2}{\left(2 t \right)}} \\  & =\sqrt{64 \left(t^{2} + \sin^{2}{\left(2 t \right)} + \cos^{2}{\left(2 t \right)}\right)} \\  & =\sqrt{64 t^{2} + 64}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{1}\|f'(t)\|\,\mathrm{d}t=\int_{0}^{1}8 \sqrt{t^{2} + 1}\,\mathrm{d}t\end{aligned}
$$

## authored method bank variant — quad_helix / authored_method

Which integral  expression gives the arc length of the curve $f(t)=\langle 2 \sin{\left(2 t \right)},\,2 \cos{\left(2 t \right)},\,3 t^{2}\rangle$
from  $t=0$ to $t=1?$

- $\int_{0}^{1}2 \sqrt{9 t^{2} + 4}\,\mathrm{d}t$ **correct**
- $\int_{0}^{1}36 t^{2} + 16 \sin^{2}{\left(2 t \right)} + 16 \cos^{2}{\left(2 t \right)}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{16 \sin^{2}{\left(2 t \right)} + 16 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{2}2 \sqrt{9 t^{2} + 4}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{9 t^{4} + 4 \sin^{2}{\left(2 t \right)} + 4 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$

First, we find $f'(t)$ and $\|f'(t)\|:$

$$
\begin{aligned}f'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(2 \sin{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(2 \cos{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(3 t^{2})\rangle \\  & =\langle 4 \cos{\left(2 t \right)},\,- 4 \sin{\left(2 t \right)},\,6 t\rangle \\ \|f'(t)\| & =\sqrt{\left(6 t\right)^{2} + \left(- 4 \sin{\left(2 t \right)}\right)^{2} + \left(4 \cos{\left(2 t \right)}\right)^{2}} \\  & =\sqrt{36 t^{2} + 16 \sin^{2}{\left(2 t \right)} + 16 \cos^{2}{\left(2 t \right)}} \\  & =\sqrt{16 \left(\frac{9 t^{2}}{4} + \sin^{2}{\left(2 t \right)} + \cos^{2}{\left(2 t \right)}\right)} \\  & =\sqrt{36 t^{2} + 16}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{1}\|f'(t)\|\,\mathrm{d}t=\int_{0}^{1}2 \sqrt{9 t^{2} + 4}\,\mathrm{d}t\end{aligned}
$$

## authored method bank variant — spiral / authored_method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/7794ce8b25bfd38cc9f02f11fb4607a43673f5cfb0ecf98ad25fc061831fe298.png)

Which integral  expression gives the arc length of the curve $g(t)=\langle 4 t \sin{\left(2 t \right)},\,- 4 t \cos{\left(2 t \right)} + 1\rangle$
from  $t=0$ to $t=\pi?$

- $\int_{0}^{\pi}\sqrt{\left(8 t \cos{\left(2 t \right)} + 4 \sin{\left(2 t \right)}\right)^{2}}\,\mathrm{d}t$
- $\int_{0}^{\pi}4 \sqrt{4 t^{2} + 1}\,\mathrm{d}t$ **correct**
- $\int_{0}^{\pi}\sqrt{16 t^{2} \sin^{2}{\left(2 t \right)} + \left(- 4 t \cos{\left(2 t \right)} + 1\right)^{2}}\,\mathrm{d}t$
- $\int_{0}^{\pi}64 t^{2} \sin^{2}{\left(2 t \right)} + 64 t^{2} \cos^{2}{\left(2 t \right)} + 16 \sin^{2}{\left(2 t \right)} + 16 \cos^{2}{\left(2 t \right)}\,\mathrm{d}t$
- $\int_{0}^{1 + \pi}4 \sqrt{4 t^{2} + 1}\,\mathrm{d}t$

First, we find $g'(t)$ and $\|g'(t)\|:$

$$
\begin{aligned}g'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(4 t \sin{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(- 4 t \cos{\left(2 t \right)} + 1)\rangle \\  & =\langle 8 t \cos{\left(2 t \right)} + 4 \sin{\left(2 t \right)},\,8 t \sin{\left(2 t \right)} - 4 \cos{\left(2 t \right)}\rangle \\ \|g'(t)\| & =\sqrt{\left(8 t \sin{\left(2 t \right)} - 4 \cos{\left(2 t \right)}\right)^{2} + \left(8 t \cos{\left(2 t \right)} + 4 \sin{\left(2 t \right)}\right)^{2}} \\  & =\sqrt{\left(64 t^{2} \sin^{2}{\left(2 t \right)} - 64 t \sin{\left(2 t \right)} \cos{\left(2 t \right)} + 16 \cos^{2}{\left(2 t \right)}\right) + \left(64 t^{2} \cos^{2}{\left(2 t \right)} + 64 t \sin{\left(2 t \right)} \cos{\left(2 t \right)} + 16 \sin^{2}{\left(2 t \right)}\right)} \\  & =\sqrt{64 t^{2} + 16}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{\pi}\|g'(t)\|\,\mathrm{d}t=\int_{0}^{\pi}4 \sqrt{4 t^{2} + 1}\,\mathrm{d}t\end{aligned}
$$

## authored method bank variant — spiral / authored_method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/f7077578c9f215f7e5499624ca3b11c32ab220bdec7c04f171b010b4a5af343c.png)

Which integral  expression gives the arc length of the curve $g(t)=\langle 2 t \sin{\left(2 t \right)},\,- 2 t \cos{\left(2 t \right)} + 1\rangle$
from  $t=0$ to $t=\pi?$

- $\int_{0}^{1 + \pi}2 \sqrt{4 t^{2} + 1}\,\mathrm{d}t$
- $\int_{0}^{\pi}16 t^{2} \sin^{2}{\left(2 t \right)} + 16 t^{2} \cos^{2}{\left(2 t \right)} + 4 \sin^{2}{\left(2 t \right)} + 4 \cos^{2}{\left(2 t \right)}\,\mathrm{d}t$
- $\int_{0}^{\pi}2 \sqrt{4 t^{2} + 1}\,\mathrm{d}t$ **correct**
- $\int_{0}^{\pi}\sqrt{4 t^{2} \sin^{2}{\left(2 t \right)} + \left(- 2 t \cos{\left(2 t \right)} + 1\right)^{2}}\,\mathrm{d}t$
- $\int_{0}^{\pi}\sqrt{\left(4 t \cos{\left(2 t \right)} + 2 \sin{\left(2 t \right)}\right)^{2}}\,\mathrm{d}t$

First, we find $g'(t)$ and $\|g'(t)\|:$

$$
\begin{aligned}g'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(2 t \sin{\left(2 t \right)}),\,\frac{\mathrm{d}}{\mathrm{d}t}(- 2 t \cos{\left(2 t \right)} + 1)\rangle \\  & =\langle 4 t \cos{\left(2 t \right)} + 2 \sin{\left(2 t \right)},\,4 t \sin{\left(2 t \right)} - 2 \cos{\left(2 t \right)}\rangle \\ \|g'(t)\| & =\sqrt{\left(4 t \sin{\left(2 t \right)} - 2 \cos{\left(2 t \right)}\right)^{2} + \left(4 t \cos{\left(2 t \right)} + 2 \sin{\left(2 t \right)}\right)^{2}} \\  & =\sqrt{\left(16 t^{2} \sin^{2}{\left(2 t \right)} - 16 t \sin{\left(2 t \right)} \cos{\left(2 t \right)} + 4 \cos^{2}{\left(2 t \right)}\right) + \left(16 t^{2} \cos^{2}{\left(2 t \right)} + 16 t \sin{\left(2 t \right)} \cos{\left(2 t \right)} + 4 \sin^{2}{\left(2 t \right)}\right)} \\  & =\sqrt{16 t^{2} + 4}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{\pi}\|g'(t)\|\,\mathrm{d}t=\int_{0}^{\pi}2 \sqrt{4 t^{2} + 1}\,\mathrm{d}t\end{aligned}
$$

## authored method bank variant — helix_basis / authored_method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/9e09ecef4a667916fcb367bfaad295ea69f132dd1f9548da63c77c81cdf8cae8.png)

Which integral  expression gives the arc length of the curve $h(t)=(4 \cos{\left(2 t \right)})\,i+(4 \sin{\left(2 t \right)})\,j+(4 t)\,k$ from $t=0$ to $t=2 \pi?$

- $\int_{0}^{2 \pi}\sqrt{16 t^{2} + 16 \sin^{2}{\left(2 t \right)} + 16 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{2 \pi}\sqrt{64 \sin^{2}{\left(2 t \right)} + 64 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{1 + 2 \pi}\sqrt{80}\,\mathrm{d}t$
- $\int_{0}^{2 \pi}\sqrt{80}\,\mathrm{d}t$ **correct**
- $\int_{0}^{2 \pi}64 \sin^{2}{\left(2 t \right)} + 64 \cos^{2}{\left(2 t \right)} + 16\,\mathrm{d}t$

First, we find $h'(t)$ and $\|h'(t)\|:$

$$
\begin{aligned}h'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(4 \cos{\left(2 t \right)}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(4 \sin{\left(2 t \right)}))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(4 t))\,k \\  & =(- 8 \sin{\left(2 t \right)})\,i+(8 \cos{\left(2 t \right)})\,j+(4)\,k \\ \|h'(t)\| & =\sqrt{\left(- 8 \sin{\left(2 t \right)}\right)^{2} + \left(8 \cos{\left(2 t \right)}\right)^{2} + 4^{2}} \\  & =\sqrt{64 \sin^{2}{\left(2 t \right)} + 64 \cos^{2}{\left(2 t \right)} + 16} \\  & =\sqrt{80}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{2 \pi}\|h'(t)\|\,\mathrm{d}t=\int_{0}^{2 \pi}\sqrt{80}\,\mathrm{d}t\end{aligned}
$$

## authored method bank variant — helix_basis / authored_method

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186119743/plots/f2f3e33e9041fcfc7beae068ae99f45592d847cbeedafa309416599ba4830dab.png)

Which integral  expression gives the arc length of the curve $h(t)=(2 \cos{\left(2 t \right)})\,i+(2 \sin{\left(2 t \right)})\,j+(3 t)\,k$ from $t=0$ to $t=2 \pi?$

- $\int_{0}^{2 \pi}\sqrt{25}\,\mathrm{d}t$ **correct**
- $\int_{0}^{2 \pi}16 \sin^{2}{\left(2 t \right)} + 16 \cos^{2}{\left(2 t \right)} + 9\,\mathrm{d}t$
- $\int_{0}^{2 \pi}\sqrt{16 \sin^{2}{\left(2 t \right)} + 16 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$
- $\int_{0}^{1 + 2 \pi}\sqrt{25}\,\mathrm{d}t$
- $\int_{0}^{2 \pi}\sqrt{9 t^{2} + 4 \sin^{2}{\left(2 t \right)} + 4 \cos^{2}{\left(2 t \right)}}\,\mathrm{d}t$

First, we find $h'(t)$ and $\|h'(t)\|:$

$$
\begin{aligned}h'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(2 \cos{\left(2 t \right)}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(2 \sin{\left(2 t \right)}))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(3 t))\,k \\  & =(- 4 \sin{\left(2 t \right)})\,i+(4 \cos{\left(2 t \right)})\,j+(3)\,k \\ \|h'(t)\| & =\sqrt{\left(- 4 \sin{\left(2 t \right)}\right)^{2} + \left(4 \cos{\left(2 t \right)}\right)^{2} + 3^{2}} \\  & =\sqrt{16 \sin^{2}{\left(2 t \right)} + 16 \cos^{2}{\left(2 t \right)} + 9} \\  & =\sqrt{25}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{0}^{2 \pi}\|h'(t)\|\,\mathrm{d}t=\int_{0}^{2 \pi}\sqrt{25}\,\mathrm{d}t\end{aligned}
$$

## authored method bank variant — power_basis / authored_method

Which integral expression gives the arc length of the curve $r(t)=(4 t^{3})\,i+(3 t)\,j+(4 t^{4})\,k$ from $t=2$ to $t=5?$

- $\int_{2}^{5}\sqrt{144 t^{4} + 9}\,\mathrm{d}t$
- $\int_{2}^{5}256 t^{6} + 144 t^{4} + 9\,\mathrm{d}t$
- $\int_{2}^{6}\sqrt{256 t^{6} + 144 t^{4} + 9}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{16 t^{8} + 16 t^{6} + 9 t^{2}}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{256 t^{6} + 144 t^{4} + 9}\,\mathrm{d}t$ **correct**

First, we find $r'(t)$ and $\|r'(t)\|:$

$$
\begin{aligned}r'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(4 t^{3}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(3 t))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(4 t^{4}))\,k \\  & =(12 t^{2})\,i+(3)\,j+(16 t^{3})\,k \\ \|r'(t)\| & =\sqrt{\left(12 t^{2}\right)^{2} + \left(16 t^{3}\right)^{2} + 3^{2}} \\  & =\sqrt{256 t^{6} + 144 t^{4} + 9}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{2}^{5}\|r'(t)\|\,\mathrm{d}t=\int_{2}^{5}\sqrt{256 t^{6} + 144 t^{4} + 9}\,\mathrm{d}t\end{aligned}
$$

## authored method bank variant — power_basis / authored_method

Which integral expression gives the arc length of the curve $r(t)=(2 t^{2})\,i+(4 t)\,j+(3 t^{3})\,k$ from $t=2$ to $t=5?$

- $\int_{2}^{6}\sqrt{81 t^{4} + 16 t^{2} + 16}\,\mathrm{d}t$
- $\int_{2}^{5}81 t^{4} + 16 t^{2} + 16\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{81 t^{4} + 16 t^{2} + 16}\,\mathrm{d}t$ **correct**
- $\int_{2}^{5}\sqrt{16 t^{2} + 16}\,\mathrm{d}t$
- $\int_{2}^{5}\sqrt{9 t^{6} + 4 t^{4} + 16 t^{2}}\,\mathrm{d}t$

First, we find $r'(t)$ and $\|r'(t)\|:$

$$
\begin{aligned}r'(t) & =(\frac{\mathrm{d}}{\mathrm{d}t}(2 t^{2}))\,i+(\frac{\mathrm{d}}{\mathrm{d}t}(4 t))\,j+(\frac{\mathrm{d}}{\mathrm{d}t}(3 t^{3}))\,k \\  & =(4 t)\,i+(4)\,j+(9 t^{2})\,k \\ \|r'(t)\| & =\sqrt{\left(4 t\right)^{2} + \left(9 t^{2}\right)^{2} + 4^{2}} \\  & =\sqrt{81 t^{4} + 16 t^{2} + 16}\end{aligned}
$$

Therefore, the arc length of the curve is:

$$
\begin{aligned}L & =\int_{2}^{5}\|r'(t)\|\,\mathrm{d}t=\int_{2}^{5}\sqrt{81 t^{4} + 16 t^{2} + 16}\,\mathrm{d}t\end{aligned}
$$

## authored default variant; hard level authored — exp_rotating / authored_method

Which integral expression gives the arc length of the curve $r(t)=\langle \left(2 \sin{\left(3 t \right)} + 3 \cos{\left(3 t \right)}\right) e^{3 t},\,2 t e^{3 t},\,\left(3 \sin{\left(3 t \right)} - 2 \cos{\left(3 t \right)}\right) e^{3 t}\rangle$ from $t=0$ to $t=1?$

- $\int_{0}^{1}\sqrt{4 t^{2} e^{6 t} + \left(2 \sin{\left(3 t \right)} + 3 \cos{\left(3 t \right)}\right)^{2} e^{6 t} + \left(3 \sin{\left(3 t \right)} - 2 \cos{\left(3 t \right)}\right)^{2} e^{6 t}}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{\left(6 t e^{3 t} + 2 e^{3 t}\right)^{2} + \left(\left(- 9 \sin{\left(3 t \right)} + 6 \cos{\left(3 t \right)}\right) e^{3 t} + 3 \left(2 \sin{\left(3 t \right)} + 3 \cos{\left(3 t \right)}\right) e^{3 t}\right)^{2}}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{2} \sqrt{2 \left(3 t + 1\right)^{2} + 117} e^{3 t}\,\mathrm{d}t$ **correct**
- $\int_{0}^{2}\sqrt{2} \sqrt{2 \left(3 t + 1\right)^{2} + 117} e^{3 t}\,\mathrm{d}t$
- $\int_{0}^{1}36 t^{2} e^{6 t} + 24 t e^{6 t} + 234 e^{6 t} \sin^{2}{\left(3 t \right)} + 234 e^{6 t} \cos^{2}{\left(3 t \right)} + 4 e^{6 t}\,\mathrm{d}t$

First, we find $r'(t)$ and $\|r'(t)\|:$

$$
\begin{aligned}r'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(\left(2 \sin{\left(3 t \right)} + 3 \cos{\left(3 t \right)}\right) e^{3 t}),\,\frac{\mathrm{d}}{\mathrm{d}t}(2 t e^{3 t}),\,\frac{\mathrm{d}}{\mathrm{d}t}(\left(3 \sin{\left(3 t \right)} - 2 \cos{\left(3 t \right)}\right) e^{3 t})\rangle \\  & =\langle \left(- 9 \sin{\left(3 t \right)} + 6 \cos{\left(3 t \right)}\right) e^{3 t} + 3 \left(2 \sin{\left(3 t \right)} + 3 \cos{\left(3 t \right)}\right) e^{3 t},\,6 t e^{3 t} + 2 e^{3 t},\,3 \left(3 \sin{\left(3 t \right)} - 2 \cos{\left(3 t \right)}\right) e^{3 t} + \left(6 \sin{\left(3 t \right)} + 9 \cos{\left(3 t \right)}\right) e^{3 t}\rangle \\ \|r'(t)\| & =\sqrt{\left(6 t e^{3 t} + 2 e^{3 t}\right)^{2} + \left(\left(- 9 \sin{\left(3 t \right)} + 6 \cos{\left(3 t \right)}\right) e^{3 t} + 3 \left(2 \sin{\left(3 t \right)} + 3 \cos{\left(3 t \right)}\right) e^{3 t}\right)^{2} + \left(3 \left(3 \sin{\left(3 t \right)} - 2 \cos{\left(3 t \right)}\right) e^{3 t} + \left(6 \sin{\left(3 t \right)} + 9 \cos{\left(3 t \right)}\right) e^{3 t}\right)^{2}} \\  & =\sqrt{\left(36 t^{2} e^{6 t} + 24 t e^{6 t} + 4 e^{6 t}\right) + \left(9 e^{6 t} \sin^{2}{\left(3 t \right)} - 90 e^{6 t} \sin{\left(3 t \right)} \cos{\left(3 t \right)} + 225 e^{6 t} \cos^{2}{\left(3 t \right)}\right) + \left(225 e^{6 t} \sin^{2}{\left(3 t \right)} + 90 e^{6 t} \sin{\left(3 t \right)} \cos{\left(3 t \right)} + 9 e^{6 t} \cos^{2}{\left(3 t \right)}\right)} \\  & =\sqrt{\left(4 \left(3 t + 1\right)^{2} + 234\right) e^{6 t}} \\  & =\sqrt{4 \left(3 t + 1\right)^{2} + 234} e^{3 t}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{0}^{1}\|r'(t)\|\,\mathrm{d}t \\  & =\int_{0}^{1}\sqrt{2} \sqrt{2 \left(3 t + 1\right)^{2} + 117} e^{3 t}\,\mathrm{d}t.\end{aligned}
$$

## authored default variant; hard level authored — exp_rotating / authored_method

Which integral expression gives the arc length of the curve $r(t)=\langle \left(2 \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{2 t},\,3 t e^{2 t},\,\left(\sin{\left(t \right)} - 2 \cos{\left(t \right)}\right) e^{2 t}\rangle$ from $t=0$ to $t=1?$

- $\int_{0}^{2}\sqrt{9 \left(2 t + 1\right)^{2} + 25} e^{2 t}\,\mathrm{d}t$
- $\int_{0}^{1}36 t^{2} e^{4 t} + 36 t e^{4 t} + 25 e^{4 t} \sin^{2}{\left(t \right)} + 25 e^{4 t} \cos^{2}{\left(t \right)} + 9 e^{4 t}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{9 \left(2 t + 1\right)^{2} + 25} e^{2 t}\,\mathrm{d}t$ **correct**
- $\int_{0}^{1}\sqrt{\left(6 t e^{2 t} + 3 e^{2 t}\right)^{2} + \left(\left(- \sin{\left(t \right)} + 2 \cos{\left(t \right)}\right) e^{2 t} + 2 \left(2 \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{2 t}\right)^{2}}\,\mathrm{d}t$
- $\int_{0}^{1}\sqrt{9 t^{2} e^{4 t} + \left(\sin{\left(t \right)} - 2 \cos{\left(t \right)}\right)^{2} e^{4 t} + \left(2 \sin{\left(t \right)} + \cos{\left(t \right)}\right)^{2} e^{4 t}}\,\mathrm{d}t$

First, we find $r'(t)$ and $\|r'(t)\|:$

$$
\begin{aligned}r'(t) & =\langle \frac{\mathrm{d}}{\mathrm{d}t}(\left(2 \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{2 t}),\,\frac{\mathrm{d}}{\mathrm{d}t}(3 t e^{2 t}),\,\frac{\mathrm{d}}{\mathrm{d}t}(\left(\sin{\left(t \right)} - 2 \cos{\left(t \right)}\right) e^{2 t})\rangle \\  & =\langle \left(- \sin{\left(t \right)} + 2 \cos{\left(t \right)}\right) e^{2 t} + 2 \left(2 \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{2 t},\,6 t e^{2 t} + 3 e^{2 t},\,2 \left(\sin{\left(t \right)} - 2 \cos{\left(t \right)}\right) e^{2 t} + \left(2 \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{2 t}\rangle \\ \|r'(t)\| & =\sqrt{\left(6 t e^{2 t} + 3 e^{2 t}\right)^{2} + \left(\left(- \sin{\left(t \right)} + 2 \cos{\left(t \right)}\right) e^{2 t} + 2 \left(2 \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{2 t}\right)^{2} + \left(2 \left(\sin{\left(t \right)} - 2 \cos{\left(t \right)}\right) e^{2 t} + \left(2 \sin{\left(t \right)} + \cos{\left(t \right)}\right) e^{2 t}\right)^{2}} \\  & =\sqrt{\left(36 t^{2} e^{4 t} + 36 t e^{4 t} + 9 e^{4 t}\right) + \left(9 e^{4 t} \sin^{2}{\left(t \right)} + 24 e^{4 t} \sin{\left(t \right)} \cos{\left(t \right)} + 16 e^{4 t} \cos^{2}{\left(t \right)}\right) + \left(16 e^{4 t} \sin^{2}{\left(t \right)} - 24 e^{4 t} \sin{\left(t \right)} \cos{\left(t \right)} + 9 e^{4 t} \cos^{2}{\left(t \right)}\right)} \\  & =\sqrt{\left(9 \left(2 t + 1\right)^{2} + 25\right) e^{4 t}} \\  & =\sqrt{9 \left(2 t + 1\right)^{2} + 25} e^{2 t}\end{aligned}
$$

Therefore, the arc length of the curve is

$$
\begin{aligned}L & =\int_{0}^{1}\|r'(t)\|\,\mathrm{d}t \\  & =\int_{0}^{1}\sqrt{9 \left(2 t + 1\right)^{2} + 25} e^{2 t}\,\mathrm{d}t.\end{aligned}
$$
