# Tangent slope generator review

Basis 1356. Original banks are shown in full. Variants are labeled as authored derivative-operation banks or explicit observed expression-pattern profiles. Source domains are repaired where explicitly stated; normal blank wording uses the exact-answer native-grading repair.

## Original q-20991 — exp_root_radio

For the parametric curve 

$$
x=\frac{1}{2\sqrt{t}},\,y=\frac{{e}^{t}}{2t},\,-\infty <t<\infty ,
$$

calculate the slope of the tangent to the curve at the point where $t=5.$

Choices: $\frac{8{e}^{5}}{\sqrt{3}}$, $-\,\frac{5{e}^{4}}{\sqrt{6}}$, $-\,\frac{4{e}^{5}}{\sqrt{2}}$, $\frac{{e}^{3}}{\sqrt{5}}$, $-\,\frac{8{e}^{5}}{\sqrt{5}}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=-\frac{1}{4}{t}^{-3/2},\,{y}^{′}(t)=\frac{2t{e}^{t}-2{e}^{t}}{4{t}^{2}}=\frac{{e}^{t}(t-1)}{2{t}^{2}}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{e}^{t}(t-1)}{2{t}^{2}}\cdot (-4{t}^{3/2}) \\  & =-\frac{2{e}^{t}(t-1)}{\sqrt{t}}.\end{aligned}
$$

Therefore, when $t=5,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =-\,\frac{2{e}^{5}(5-1)}{\sqrt{5}} \\  & =-\,\frac{2{e}^{5}\cdot 4}{\sqrt{5}} \\  & =-\,\frac{8{e}^{5}}{\sqrt{5}}\,.\end{aligned}
$$

### Parameterized replay

For the parametric curve 

$$
x=\frac{1}{2 \sqrt{t}},\,y=\frac{e^{t}}{2 t},\,0<t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=5.$

- $- 2 \sqrt{2} e^{5}$
- $- \frac{5 \sqrt{6} e^{4}}{6}$
- $\frac{8 \sqrt{3} e^{5}}{3}$
- $- \frac{8 \sqrt{5} e^{5}}{5}$
- $\frac{\sqrt{5} e^{3}}{5}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{1}{4 t^{\frac{3}{2}}},\,y'(t)=\frac{2 t e^{t} - 2 e^{t}}{4 t^{2}}=\frac{\left(t - 1\right) e^{t}}{2 t^{2}}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(t - 1\right) e^{t}}{2 t^{2}}\cdot \left(- 4 t^{\frac{3}{2}}\right) \\  & =- \frac{2 \left(t - 1\right) e^{t}}{\sqrt{t}}.\end{aligned}
$$

Therefore, when $t=5,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{2 \left(\left(5\right) - 1\right) e^{\left(5\right)}}{\sqrt{\left(5\right)}} \\  & =\frac{- 8 e^{5}}{\sqrt{5}} \\  & =- \frac{8 \sqrt{5} e^{5}}{5}.\end{aligned}
$$

## Original q-6808 — harmonic_radio

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/source-q-6808.png)

For the parametric curve 

$$
x=4\operatorname{cos}⁡t,\,y=3\operatorname{sin}⁡2t,\,0\le t<2\pi ,
$$

shown above, calculate the slope of the tangent to the curve at the point where $t=\frac{\pi }{6}.$

Choices: $-\,\frac{1}{\sqrt{2}}$, $-\,\frac{2}{3}$, $-\,\frac{1}{2}$, $-\,\frac{3}{\sqrt{2}}$, $-\,\frac{3}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=-4\operatorname{sin}⁡t,\,{y}^{′}(t)=6\operatorname{cos}⁡2t.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{6\operatorname{cos}⁡2t}{-4\operatorname{sin}⁡t} \\  & =-\frac{3}{2}\frac{\operatorname{cos}⁡2t}{\operatorname{sin}⁡t}.\end{aligned}
$$

Therefore, when $t=\frac{\pi }{6},$ the slope of the tangent to the curve is

$$
\begin{aligned}{\frac{dy}{dx}|}_{t=\pi /6} & =-\frac{3}{2}\frac{\operatorname{cos}⁡(2\cdot \frac{\pi }{6})}{\operatorname{sin}⁡(\frac{\pi }{6})} \\  & =-\frac{3}{2}\frac{\operatorname{cos}⁡(\frac{\pi }{3})}{\operatorname{sin}⁡(\frac{\pi }{6})} \\  & =-\frac{3}{2}\frac{(\frac{1}{2})}{(\frac{1}{2})} \\  & =-\frac{3}{2}.\end{aligned}
$$

### Parameterized replay

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/source-q-6808.png)

For the parametric curve 

$$
x=4 \cos {t},\,y=3 \sin {2 t},\,0\le t<2\pi,
$$

shown above, calculate the slope of the tangent to the curve at the point where $t=\frac{\pi}{6}.$

- $- \frac{1}{2}$
- $- \frac{2}{3}$
- $- \frac{\sqrt{2}}{2}$
- $- \frac{3}{2}$
- $- \frac{3 \sqrt{2}}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- 4 \sin {t},\,y'(t)=6 \cos {2 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(6 \cos {2 t}\right)}{\left(- 4 \sin {t}\right)} \\  & =- \frac{3 \cos {2 t}}{2 \sin {t}}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{6},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{3 \cos {2 \left(\frac{\pi}{6}\right)}}{2 \sin {\left(\frac{\pi}{6}\right)}} \\  & =- \frac{3 \left(\frac{1}{2}\right)}{2 \left(\frac{1}{2}\right)} \\  & =- \frac{3}{2}.\end{aligned}
$$

## Original q-102922 — double_sin_radio

For the parametric curve 

$$
x=\operatorname{sin}⁡2t,\,y={sin}^{2}⁡t,\,0\le t<2\pi ,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi }{12}.$

Choices: $\frac{\sqrt{3}}{6}$, $-\frac{\sqrt{3}}{2}$, $\sqrt{3}$, $-\frac{\sqrt{3}}{6}$, $\frac{\sqrt{3}}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=2\operatorname{cos}⁡2t,\,{y}^{′}(t)=2\operatorname{sin}⁡t\operatorname{cos}⁡t=\operatorname{sin}⁡2t.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\operatorname{sin}⁡2t}{2\operatorname{cos}⁡2t} \\  & =\frac{1}{2}\operatorname{tan}⁡2t.\end{aligned}
$$

Therefore, when $t=\frac{\pi }{12},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{1}{2}\operatorname{tan}⁡(2\cdot \frac{\pi }{12}) \\  & =\frac{1}{2}\operatorname{tan}⁡(\frac{\pi }{6}) \\  & =\frac{1}{2}\cdot \frac{\sqrt{3}}{3} \\  & =\frac{\sqrt{3}}{6}.\end{aligned}
$$

### Parameterized replay

For the parametric curve 

$$
x=\sin {2 t},\,y=\sin^{2} {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi}{12}.$

- $\sqrt{3}$
- $- \frac{\sqrt{3}}{2}$
- $\frac{\sqrt{3}}{6}$
- $\frac{\sqrt{3}}{2}$
- $- \frac{\sqrt{3}}{6}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=2 \cos {2 t},\,y'(t)=2 \sin {t} \cos {t}=\sin {2 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(\sin {2 t}\right)}{\left(2 \cos {2 t}\right)} \\  & =\frac{\tan {2 t}}{2}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{12},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\tan {2 \left(\frac{\pi}{12}\right)}}{2} \\  & =\frac{\left(\frac{\sqrt{3}}{3}\right)}{2} \\  & =\frac{\sqrt{3}}{6}.\end{aligned}
$$

## Original q-102940 — poly5_radio

For the parametric curve 

$$
x=2{t}^{2}+3,\,y=3{t}^{5}+{t}^{3},\,0\le t<\infty ,
$$

calculate the slope of the tangent to the curve at the point where $t=1.$

Choices: $\frac{11}{4}$, $\frac{15}{4}$, $\frac{11}{2}$, $\frac{9}{2}$, $\frac{3}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=4t,\,{y}^{′}(t)=3{t}^{2}(5{t}^{2}+1).
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{3{t}^{2}(5{t}^{2}+1)}{4t}=\frac{3t(5{t}^{2}+1)}{4}.\end{aligned}
$$

Therefore, when $t=1,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{3(1)(5(1)^{2}+1)}{4} \\  & =\frac{18}{4} \\  & =\frac{9}{2}.\end{aligned}
$$

### Parameterized replay

For the parametric curve 

$$
x=2 t^{2} + 3,\,y=3 t^{5} + t^{3},\,0\le t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=1.$

- $\frac{11}{2}$
- $\frac{15}{4}$
- $\frac{11}{4}$
- $\frac{3}{2}$
- $\frac{9}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=4 t,\,y'(t)=3 t^{2} \left(5 t^{2} + 1\right).
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(3 t^{2} \left(5 t^{2} + 1\right)\right)}{\left(4 t\right)} \\  & =\frac{3 t \left(5 t^{2} + 1\right)}{4}.\end{aligned}
$$

Therefore, when $t=1,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{3 \left(1\right) \left(5 \left(1\right)^{2} + 1\right)}{4} \\  & =\frac{18}{4} \\  & =\frac{9}{2}.\end{aligned}
$$

## Original q-102941 — trig_poly_radio

For the parametric curve 

$$
x=4\operatorname{sin}⁡t,\,y=\frac{4}{\pi }{t}^{2},\,0\le t<2\pi ,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi }{4}.$

Choices: $\frac{\sqrt{2}}{2}$, $2\sqrt{2}$, $\sqrt{2}$, $\frac{1}{2}$, $2$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=4\operatorname{cos}⁡t,\,{y}^{′}(t)=\frac{8}{\pi }t.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{(\frac{8}{\pi }t)}{4\operatorname{cos}⁡t} \\  & =\frac{2t\operatorname{sec}⁡t}{\pi }.\end{aligned}
$$

Therefore, when $t=\frac{\pi }{4},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{2(\frac{\pi }{4})\operatorname{sec}⁡(\frac{\pi }{4})}{\pi } \\  & =\frac{(\frac{\pi }{2}\cdot \sqrt{2})}{\pi } \\  & =\frac{\sqrt{2}}{2}.\end{aligned}
$$

### Parameterized replay

For the parametric curve 

$$
x=4 \sin {t},\,y=\frac{4 t^{2}}{\pi},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi}{4}.$

- $\sqrt{2}$
- $2 \sqrt{2}$
- $\frac{\sqrt{2}}{2}$
- $2$
- $\frac{1}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=4 \cos {t},\,y'(t)=\frac{8 t}{\pi}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(\frac{8 t}{\pi}\right)}{\left(4 \cos {t}\right)} \\  & =\frac{2 t \sec {t}}{\pi}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{4},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{2 \left(\frac{\pi}{4}\right) \sec {\left(\frac{\pi}{4}\right)}}{\pi} \\  & =\frac{2 \left(\frac{\pi}{4}\right) \left(\sqrt{2}\right)}{\pi} \\  & =\frac{\sqrt{2}}{2}.\end{aligned}
$$

## Original q-15457 — double_cos_radio

For the parametric curve 

$$
x=\operatorname{sin}⁡(2t),\,y={cos}^{2}⁡(t),\,0\le t<2\pi ,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi }{6}.$

Choices: $\sqrt{3}$, $-\,\frac{1}{2}$, $-\,\frac{\sqrt{3}}{2}$, $-\,\sqrt{3}$, $\frac{1}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=2\operatorname{cos}⁡(2t),\,{y}^{′}(t)=-2\operatorname{sin}⁡t\operatorname{cos}⁡t=-\operatorname{sin}⁡(2t).
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{-\operatorname{sin}⁡(2t)}{2\operatorname{cos}⁡(2t)} \\  & =-\frac{1}{2}\operatorname{tan}⁡(2t).\end{aligned}
$$

Therefore, when $t=\frac{\pi }{6},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =-\,\frac{1}{2}\,\operatorname{tan}⁡(\frac{2\pi }{6}) \\  & =-\,\frac{1}{2}\,\operatorname{tan}⁡(\frac{\pi }{3}) \\  & =-\,\frac{\sqrt{3}}{2}\,.\end{aligned}
$$

### Parameterized replay

For the parametric curve 

$$
x=\sin {2 t},\,y=\cos^{2} {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi}{6}.$

- $- \frac{\sqrt{3}}{2}$
- $- \frac{1}{2}$
- $\sqrt{3}$
- $\frac{1}{2}$
- $- \sqrt{3}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=2 \cos {2 t},\,y'(t)=- 2 \sin {t} \cos {t}=- \sin {2 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- \sin {2 t}\right)}{\left(2 \cos {2 t}\right)} \\  & =- \frac{\tan {2 t}}{2}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{6},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{\tan {2 \left(\frac{\pi}{6}\right)}}{2} \\  & =- \frac{\left(\sqrt{3}\right)}{2} \\  & =- \frac{\sqrt{3}}{2}.\end{aligned}
$$

## Original q-15475 — reciprocal_exp_root_radio

For the parametric curve 

$$
x={e}^{1/t},\,y=\frac{1}{\sqrt{{t}^{2}-1}},\,1<t<\infty ,
$$

calculate the slope of the tangent to the curve at the point where $t=2.$

Choices: $\frac{8}{\sqrt{27e}}$, $\sqrt{\frac{8e}{27}}$, $\frac{\sqrt{9e}}{4}$, $\frac{4}{\sqrt{9e}}$, $\sqrt{\frac{9}{8e}}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=-\frac{1}{{t}^{2}}{e}^{1/t},\,{y}^{′}(t)=-\frac{t}{({t}^{2}-1)^{3/2}}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{(-\frac{t}{({t}^{2}-1)^{3/2}})}{(-\frac{1}{{t}^{2}}{e}^{1/t})} \\  & =\frac{{t}^{3}{e}^{-1/t}}{({t}^{2}-1)^{3/2}}.\end{aligned}
$$

Therefore, when $t=2,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{2}^{3}{e}^{-1/2}}{({2}^{2}-1)^{3/2}} \\  & =\frac{8}{{3}^{3/2}\sqrt{e}} \\  & =\frac{8}{\sqrt{27e}}\,.\end{aligned}
$$

### Parameterized replay

For the parametric curve 

$$
x=e^{\frac{1}{t}},\,y=\frac{1}{\sqrt{t^{2} - 1}},\,1<t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=2.$

- $\frac{3 e^{\frac{1}{2}}}{4}$
- $\frac{2 \sqrt{6} e^{\frac{1}{2}}}{9}$
- $\frac{8 \sqrt{3}}{9 e^{\frac{1}{2}}}$
- $\frac{3 \sqrt{2}}{4 e^{\frac{1}{2}}}$
- $\frac{4}{3 e^{\frac{1}{2}}}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{e^{\frac{1}{t}}}{t^{2}},\,y'(t)=- \frac{t}{\left(t^{2} - 1\right)^{\frac{3}{2}}}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- \frac{t}{\left(t^{2} - 1\right)^{\frac{3}{2}}}\right)}{\left(- \frac{e^{\frac{1}{t}}}{t^{2}}\right)} \\  & =\frac{t^{3} e^{- \frac{1}{t}}}{\left(t^{2} - 1\right)^{\frac{3}{2}}}.\end{aligned}
$$

Therefore, when $t=2,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(2\right)^{3} e^{- \frac{1}{\left(2\right)}}}{\left(\left(2\right)^{2} - 1\right)^{\frac{3}{2}}} \\  & =\frac{8}{3 \sqrt{3} e^{\frac{1}{2}}} \\  & =\frac{8 \sqrt{3}}{9 e^{\frac{1}{2}}}.\end{aligned}
$$

## Original q-15476 — nested_trig_radio

For the parametric curve 

$$
x=\sqrt{\operatorname{sin}⁡({e}^{t})},\,y=\operatorname{cot}⁡({e}^{t}),\,-\infty <t<1,
$$

calculate the slope of the tangent to the curve at the point where $t=\operatorname{ln}⁡(\frac{\pi }{6}).$

Choices: $-8\sqrt{\frac{2}{3}}$, $-2\sqrt{\frac{2}{3}}$, $-\,\frac{1}{\sqrt{6}}$, $-4\sqrt{\frac{3}{2}}$, $-2\sqrt{\frac{3}{2}}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
\begin{aligned}{x}^{′}(t) & =\frac{1}{2\sqrt{\operatorname{sin}⁡({e}^{t})}}\cdot \operatorname{cos}⁡({e}^{t})\cdot {e}^{t} \\  & =\frac{{e}^{t}\operatorname{cos}⁡({e}^{t})}{2\sqrt{\operatorname{sin}⁡({e}^{t})}}, \\ {y}^{′}(t) & =-{e}^{t}{csc}^{2}⁡({e}^{t}).\end{aligned}
$$

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{-{e}^{t}{csc}^{2}⁡({e}^{t})}{(\frac{{e}^{t}\operatorname{cos}⁡({e}^{t})}{2\sqrt{\operatorname{sin}⁡({e}^{t})}})} \\  & =-\,\frac{2\sqrt{\operatorname{sin}⁡({e}^{t})}}{{sin}^{2}⁡({e}^{t})\operatorname{cos}⁡({e}^{t})} \\  & =-\,\frac{2}{{sin}^{3/2}⁡({e}^{t})\operatorname{cos}⁡({e}^{t})}\,.\end{aligned}
$$

Therefore, when $t=\operatorname{ln}⁡(\frac{\pi }{6}),$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =-\,\frac{2}{{sin}^{3/2}⁡(\frac{\pi }{6})\operatorname{cos}⁡(\frac{\pi }{6})} \\  & =-\,\frac{2}{{(\frac{1}{2})}^{3/2}(\frac{\sqrt{3}}{2})} \\  & =-2\cdot {2}^{3/2}\,\frac{2}{\sqrt{3}} \\  & =-8\sqrt{\frac{2}{3}}\,.\end{aligned}
$$

### Parameterized replay

For the parametric curve 

$$
x=\sqrt{\sin{\left(e^{t} \right)}},\,y=\cot{\left(e^{t} \right)},\,-\infty<t<1,
$$

calculate the slope of the tangent to the curve at the point where $t=\ln{\left(\frac{\pi}{6} \right)}.$

- $- \frac{\sqrt{6}}{6}$
- $- \frac{2 \sqrt{6}}{3}$
- $- \frac{8 \sqrt{6}}{3}$
- $- \sqrt{6}$
- $- 2 \sqrt{6}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
\begin{aligned}x'(t)&=\frac{1}{2 \sqrt{\sin{\left(e^{t} \right)}}}\cdot \cos{\left(e^{t} \right)}\cdot e^{t}\\ &= \frac{e^{t} \cos{\left(e^{t} \right)}}{2 \sqrt{\sin{\left(e^{t} \right)}}},\\ y'(t)&=- e^{t} \csc^{2}{\left(e^{t} \right)}.\end{aligned}
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- e^{t} \csc^{2}{\left(e^{t} \right)}\right)}{\left(\frac{e^{t} \cos{\left(e^{t} \right)}}{2 \sqrt{\sin{\left(e^{t} \right)}}}\right)} \\  & =\frac{- 2 \sqrt{\sin{\left(e^{t} \right)}}}{\sin^{2}{\left(e^{t} \right)} \cos{\left(e^{t} \right)}} \\  & =- \frac{2}{\sin^{\frac{3}{2}}{\left(e^{t} \right)} \cos{\left(e^{t} \right)}}.\end{aligned}
$$

Therefore, when $t=\ln{\left(\frac{\pi}{6} \right)},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{2}{\sin^{\frac{3}{2}}{\left(e^{\left(\ln{\left(\frac{\pi}{6} \right)}\right)} \right)} \cos{\left(e^{\left(\ln{\left(\frac{\pi}{6} \right)}\right)} \right)}} \\  & =- \frac{2}{\sin^{\frac{3}{2}}{\left(e^{\left(\ln{\left(\frac{\pi}{6} \right)}\right)} \right)} \left(\frac{\sqrt{3}}{2}\right)} \\  & =- \frac{8 \sqrt{6}}{3}.\end{aligned}
$$

## Original q-348303 — cubic_blank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/source-q-348303.png)

For the parametric curve 

$$
x={t}^{3}+2{t}^{2},\,y={t}^{2},\,-\infty <t<\infty ,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=2.$ Do not round the answer.

$m=$
{{field-1}}

Choices: $\frac{1}{5}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=3{t}^{2}+4t,\,{y}^{′}(t)=2t.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{2t}{3{t}^{2}+4t} \\  & =\frac{2}{3t+4}.\end{aligned}
$$

Therefore, when $t=2,$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t\,=\,2} & =\frac{2}{3(2)+4} \\  & =\frac{2}{6+4} \\  & =\frac{2}{10} \\  & =\frac{1}{5}.\end{aligned}
$$

### Parameterized replay

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/source-q-348303.png)

For the parametric curve 

$$
x=t^{3} + 2 t^{2},\,y=t^{2},\,-\infty<t<\infty,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=2.$ Do not round the answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=3 t^{2} + 4 t,\,y'(t)=2 t.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(2 t\right)}{\left(3 t^{2} + 4 t\right)} \\  & =\frac{2}{3 t + 4}.\end{aligned}
$$

Therefore, when $t=2,$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=2} & =\frac{2}{3 \left(2\right) + 4} \\  & =\frac{2}{10} \\  & =\frac{1}{5}.\end{aligned}
$$

## Original q-348304 — harmonic_blank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/source-q-348304.png)

For the parametric curve 

$$
x=6\operatorname{cos}⁡t,\,y=2\operatorname{sin}⁡3t,\,0\le t<2\pi ,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=\frac{\pi }{4}.$ Do not round the answer.

$m=$
{{field-1}}

Choices: $1$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=-6\operatorname{sin}⁡t,\,{y}^{′}(t)=6\operatorname{cos}⁡3t.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{6\operatorname{cos}⁡3t}{(-6\operatorname{sin}⁡t)} \\  & =-\frac{\operatorname{cos}⁡3t}{\operatorname{sin}⁡t}.\end{aligned}
$$

Therefore, when $t=\frac{\pi }{4},$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t\,=\,\pi /4} & =-\frac{\operatorname{cos}⁡(3\cdot \frac{\pi }{4})}{\operatorname{sin}⁡(\frac{\pi }{4})} \\  & =-\frac{\operatorname{cos}⁡(\frac{3\pi }{4})}{\operatorname{sin}⁡(\frac{\pi }{4})} \\  & =-\frac{(-\frac{\sqrt{2}}{2})}{(\frac{\sqrt{2}}{2})} \\  & =1.\end{aligned}
$$

### Parameterized replay

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/source-q-348304.png)

For the parametric curve 

$$
x=6 \cos {t},\,y=2 \sin {3 t},\,0\le t<2\pi,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=\frac{\pi}{4}.$ Do not round the answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- 6 \sin {t},\,y'(t)=6 \cos {3 t}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(6 \cos {3 t}\right)}{\left(- 6 \sin {t}\right)} \\  & =- \frac{\cos {3 t}}{\sin {t}}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{4},$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=\frac{\pi}{4}} & =- \frac{\cos {3 \left(\frac{\pi}{4}\right)}}{\sin {\left(\frac{\pi}{4}\right)}} \\  & =- \frac{\left(- \frac{\sqrt{2}}{2}\right)}{\left(\frac{\sqrt{2}}{2}\right)} \\  & =1.\end{aligned}
$$

## Original q-353350 — ellipse_blank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/source-q-353350.png)

For the parametric curve 

$$
x=2\operatorname{sin}⁡t,\,y=3\operatorname{cos}⁡t,\,0\le t<2\pi ,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=\frac{\pi }{4}.$ Do not round the answer.

$m=$ 
{{field-1}}

Choices: $-\frac{3}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=2\operatorname{cos}⁡t,\,{y}^{′}(t)=-3\operatorname{sin}⁡t.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{(-3\operatorname{sin}⁡t)}{2\operatorname{cos}⁡t} \\  & =-\frac{3}{2}\operatorname{tan}⁡t.\end{aligned}
$$

Therefore, when $t=\frac{\pi }{4},$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t\,=\,\pi /4} & =-\frac{3}{2}\operatorname{tan}⁡(\frac{\pi }{4}) \\  & =-\frac{3}{2}(1) \\  & =-\frac{3}{2}.\end{aligned}
$$

### Parameterized replay

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/source-q-353350.png)

For the parametric curve 

$$
x=2 \sin {t},\,y=3 \cos {t},\,0\le t<2\pi,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=\frac{\pi}{4}.$ Do not round the answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=2 \cos {t},\,y'(t)=- 3 \sin {t}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- 3 \sin {t}\right)}{\left(2 \cos {t}\right)} \\  & =- \frac{3 \tan {t}}{2}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{4},$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=\frac{\pi}{4}} & =- \frac{3 \tan {\left(\frac{\pi}{4}\right)}}{2} \\  & =- \frac{3 \left(1\right)}{2} \\  & =- \frac{3}{2}.\end{aligned}
$$

## Original q-353351 — harmonic_blank

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/source-q-353351.png)

For the parametric curve 

$$
x=3\operatorname{cos}⁡t,\,y=4\operatorname{sin}⁡2t,\,0\le t<2\pi ,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=\frac{\pi }{3}.$ Do not round the answer.

$m=$ 
{{field-1}}

Choices: $\frac{8\sqrt{3}}{9}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=-3\operatorname{sin}⁡t,\,{y}^{′}(t)=8\operatorname{cos}⁡2t.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{8\operatorname{cos}⁡2t}{(-3\operatorname{sin}⁡t)} \\  & =-\frac{8}{3}\frac{\operatorname{cos}⁡2t}{\operatorname{sin}⁡t}.\end{aligned}
$$

Therefore, when $t=\frac{\pi }{3},$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t\,=\,\pi /3} & =-\frac{8}{3}\frac{\operatorname{cos}⁡(2\cdot \frac{\pi }{3})}{\operatorname{sin}⁡(\frac{\pi }{3})} \\  & =-\frac{8}{3}\frac{\operatorname{cos}⁡(\frac{2\pi }{3})}{\operatorname{sin}⁡(\frac{\pi }{3})} \\  & =-\frac{8}{3}\frac{(-\frac{1}{2})}{(\frac{\sqrt{3}}{2})} \\  & =\frac{8\sqrt{3}}{9}.\end{aligned}
$$

### Parameterized replay

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/source-q-353351.png)

For the parametric curve 

$$
x=3 \cos {t},\,y=4 \sin {2 t},\,0\le t<2\pi,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=\frac{\pi}{3}.$ Do not round the answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- 3 \sin {t},\,y'(t)=8 \cos {2 t}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(8 \cos {2 t}\right)}{\left(- 3 \sin {t}\right)} \\  & =- \frac{8 \cos {2 t}}{3 \sin {t}}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{3},$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=\frac{\pi}{3}} & =- \frac{8 \cos {2 \left(\frac{\pi}{3}\right)}}{3 \sin {\left(\frac{\pi}{3}\right)}} \\  & =- \frac{8 \left(- \frac{1}{2}\right)}{3 \left(\frac{\sqrt{3}}{2}\right)} \\  & =\frac{8 \sqrt{3}}{9}.\end{aligned}
$$

## Original q-363490 — reciprocal_exp_root_blank

For the parametric curve 

$$
x={e}^{3/t},\,y=\frac{1}{\sqrt{{t}^{2}+4}},\,0<t<\infty ,
$$

calculate the slope $m$ of the tangent to the curve at the point where $t=1.$ Do not round the answer.

$m=$ 
{{field-1}}

Choices: $\frac{\sqrt{5}}{75{e}^{3}}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=-\frac{3}{{t}^{2}}{e}^{3/t},\,{y}^{′}(t)=-\frac{t}{({t}^{2}+4)^{3/2}}.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{(-\frac{t}{({t}^{2}+4)^{3/2}})}{(-\frac{3}{{t}^{2}}{e}^{3/t})} \\  & =\frac{{t}^{3}}{3({t}^{2}+4)^{3/2}\,{e}^{3/t}}.\end{aligned}
$$

Therefore, when $t=1,$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t\,=\,1} & =\frac{{1}^{3}}{3({1}^{2}+4)^{3/2}\,{e}^{3}} \\  & =\frac{1}{3(5)^{3/2}\,{e}^{3}} \\  & =\frac{1}{15\sqrt{5}\,{e}^{3}} \\  & =\frac{\sqrt{5}}{75{e}^{3}}.\end{aligned}
$$

### Parameterized replay

For the parametric curve 

$$
x=e^{\frac{3}{t}},\,y=\frac{1}{\sqrt{t^{2} + 4}},\,0<t<\infty,
$$

calculate the slope $m$ of the tangent to the curve at the point where $t=1.$ Do not round the answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{3 e^{\frac{3}{t}}}{t^{2}},\,y'(t)=- \frac{t}{\left(t^{2} + 4\right)^{\frac{3}{2}}}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- \frac{t}{\left(t^{2} + 4\right)^{\frac{3}{2}}}\right)}{\left(- \frac{3 e^{\frac{3}{t}}}{t^{2}}\right)} \\  & =\frac{t^{3} e^{- \frac{3}{t}}}{3 \left(t^{2} + 4\right)^{\frac{3}{2}}}.\end{aligned}
$$

Therefore, when $t=1,$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=1} & =\frac{\left(1\right)^{3} e^{- \frac{3}{\left(1\right)}}}{3 \left(\left(1\right)^{2} + 4\right)^{\frac{3}{2}}} \\  & =\frac{1}{15 \sqrt{5} e^{3}} \\  & =\frac{\sqrt{5}}{75 e^{3}}.\end{aligned}
$$

## Original q-348305 — exp_root_blank

For the parametric curve 

$$
x=\frac{1}{3\sqrt{t}},\,y=\frac{{e}^{t}}{3t},\,-\infty <t<\infty ,
$$

calculate the slope $m$ of the tangent to the curve at the point where $t=4.$ Do not round the answer.

$m=$
{{field-1}}

Choices: $-3{e}^{4}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=-\frac{1}{6}{t}^{-3/2},\,{y}^{′}(t)=\frac{3t{e}^{t}-3{e}^{t}}{9{t}^{2}}=\frac{{e}^{t}(t-1)}{3{t}^{2}}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{{e}^{t}(t-1)}{3{t}^{2}}\cdot (-6{t}^{3/2}) \\  & =-\frac{2{e}^{t}(t-1)}{\sqrt{t}}.\end{aligned}
$$

Therefore, when $t=4,$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t\,=\,4} & =-\frac{2{e}^{4}(4-1)}{\sqrt{4}} \\  & =-\frac{2{e}^{4}\cdot 3}{2} \\  & =-3{e}^{4}.\end{aligned}
$$

### Parameterized replay

For the parametric curve 

$$
x=\frac{1}{3 \sqrt{t}},\,y=\frac{e^{t}}{3 t},\,0<t<\infty,
$$

calculate the slope $m$ of the tangent to the curve at the point where $t=4.$ Do not round the answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{1}{6 t^{\frac{3}{2}}},\,y'(t)=\frac{3 t e^{t} - 3 e^{t}}{9 t^{2}}=\frac{\left(t - 1\right) e^{t}}{3 t^{2}}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(t - 1\right) e^{t}}{3 t^{2}}\cdot \left(- 6 t^{\frac{3}{2}}\right) \\  & =- \frac{2 \left(t - 1\right) e^{t}}{\sqrt{t}}.\end{aligned}
$$

Therefore, when $t=4,$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=4} & =- \frac{2 \left(\left(4\right) - 1\right) e^{\left(4\right)}}{\sqrt{\left(4\right)}} \\  & =\frac{- 6 e^{4}}{2} \\  & =- 3 e^{4}.\end{aligned}
$$

## Original q-353363 — reciprocal_exp_root_blank

For the parametric curve 

$$
x={e}^{2/t},\,y=\frac{1}{\sqrt{{t}^{2}+1}},\,0<t<\infty ,
$$

calculate the slope $m$ of the tangent to the curve at the point where $t=1.$ Do not round the answer.

$m=$ 
{{field-1}}

Choices: $\frac{\sqrt{2}}{8{e}^{2}}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=-\frac{2}{{t}^{2}}{e}^{2/t},\,{y}^{′}(t)=-\frac{t}{({t}^{2}+1)^{3/2}}.
$$

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{(-\frac{t}{({t}^{2}+1)^{3/2}})}{(-\frac{2}{{t}^{2}}{e}^{2/t})} \\  & =\frac{{t}^{3}}{2({t}^{2}+1)^{3/2}\,{e}^{2/t}}.\end{aligned}
$$

Therefore, when $t=1,$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t\,=\,1} & =\frac{{1}^{3}}{2({1}^{2}+1)^{3/2}\,{e}^{2}} \\  & =\frac{1}{2(2)^{3/2}\,{e}^{2}} \\  & =\frac{1}{4\sqrt{2}\,{e}^{2}} \\  & =\frac{\sqrt{2}}{8{e}^{2}}.\end{aligned}
$$

### Parameterized replay

For the parametric curve 

$$
x=e^{\frac{2}{t}},\,y=\frac{1}{\sqrt{t^{2} + 1}},\,0<t<\infty,
$$

calculate the slope $m$ of the tangent to the curve at the point where $t=1.$ Do not round the answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{2 e^{\frac{2}{t}}}{t^{2}},\,y'(t)=- \frac{t}{\left(t^{2} + 1\right)^{\frac{3}{2}}}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- \frac{t}{\left(t^{2} + 1\right)^{\frac{3}{2}}}\right)}{\left(- \frac{2 e^{\frac{2}{t}}}{t^{2}}\right)} \\  & =\frac{t^{3} e^{- \frac{2}{t}}}{2 \left(t^{2} + 1\right)^{\frac{3}{2}}}.\end{aligned}
$$

Therefore, when $t=1,$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=1} & =\frac{\left(1\right)^{3} e^{- \frac{2}{\left(1\right)}}}{2 \left(\left(1\right)^{2} + 1\right)^{\frac{3}{2}}} \\  & =\frac{1}{4 \sqrt{2} e^{2}} \\  & =\frac{\sqrt{2}}{8 e^{2}}.\end{aligned}
$$

## Original q-6730 — cubic_radio

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/source-q-6730.png)

For the parametric curve 

$$
x={t}^{3}+{t}^{2},\,y={t}^{2},\,-\infty <t<\infty ,
$$

shown above, calculate the slope of the tangent to the curve at the point where $t=2.$

Choices: $\frac{1}{2}$, $\frac{1}{4}$, $\frac{1}{6}$, $\frac{1}{5}$, $\frac{1}{3}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=3{t}^{2}+2t,\,{y}^{′}(t)=2t.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{2t}{3{t}^{2}+2t} \\  & =\frac{2}{3t+2}.\end{aligned}
$$

Therefore, when $t=2,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{2}{3(2)+2} \\  & =\frac{2}{6+2} \\  & =\frac{1}{4}.\end{aligned}
$$

### Parameterized replay

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/source-q-6730.png)

For the parametric curve 

$$
x=t^{3} + t^{2},\,y=t^{2},\,-\infty<t<\infty,
$$

shown above, calculate the slope of the tangent to the curve at the point where $t=2.$

- $\frac{1}{6}$
- $\frac{1}{4}$
- $\frac{1}{2}$
- $\frac{1}{3}$
- $\frac{1}{5}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=3 t^{2} + 2 t,\,y'(t)=2 t.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(2 t\right)}{\left(3 t^{2} + 2 t\right)} \\  & =\frac{2}{3 t + 2}.\end{aligned}
$$

Therefore, when $t=2,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{2}{3 \left(2\right) + 2} \\  & =\frac{2}{8} \\  & =\frac{1}{4}.\end{aligned}
$$

## Original q-15465 — linear_trig_radio

For the parametric curve 

$$
x=t+\operatorname{sin}⁡t,\,y=t+\operatorname{cos}⁡t,\,0\le t<2\pi ,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi }{2}.$

Choices: $\sqrt{2}$, $\frac{1}{2}$, $1$, $\frac{1}{\sqrt{2}}$, $0$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=1+\operatorname{cos}⁡t,\,{y}^{′}(t)=1-\operatorname{sin}⁡t.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{1-\operatorname{sin}⁡t}{1+\operatorname{cos}⁡t}.\end{aligned}
$$

Therefore, when $t=\frac{\pi }{2},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{1-\operatorname{sin}⁡(\frac{\pi }{2})}{1+\operatorname{cos}⁡(\frac{\pi }{2})} \\  & =\frac{1-1}{1+0} \\  & =0\,.\end{aligned}
$$

### Parameterized replay

For the parametric curve 

$$
x=t + \sin {t},\,y=t + \cos {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi}{2}.$

- $1$
- $\frac{1}{2}$
- $\sqrt{2}$
- $0$
- $\frac{\sqrt{2}}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=\cos {t} + 1,\,y'(t)=1 - \sin {t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(1 - \sin {t}\right)}{\left(\cos {t} + 1\right)} \\  & =\frac{1 - \sin {t}}{\cos {t} + 1}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{2},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{1 - \sin {\left(\frac{\pi}{2}\right)}}{\cos {\left(\frac{\pi}{2}\right)} + 1} \\  & =\frac{1 - \left(1\right)}{\left(0\right) + 1} \\  & =0.\end{aligned}
$$

## Original q-15469 — poly4_radio

For the parametric curve 

$$
x=2{t}^{3}+1,\,y={t}^{4}+2{t}^{2},\,0\le t<\infty ,
$$

calculate the slope of the tangent to the curve at the point where $t=1.$

Choices: $\frac{2}{3}$, $\frac{8}{3}$, $\frac{4}{3}$, $\frac{3}{4}$, $\frac{3}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
{x}^{′}(t)=6{t}^{2},\,{y}^{′}(t)=4t({t}^{2}+1).
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{4t({t}^{2}+1)}{6{t}^{2}} \\  & =\frac{2({t}^{2}+1)}{3t}.\end{aligned}
$$

Therefore, when $t=1,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{2((1)^{2}+1)}{3\cdot 1} \\  & =\frac{4}{3}\,.\end{aligned}
$$

### Parameterized replay

For the parametric curve 

$$
x=2 t^{3} + 1,\,y=t^{4} + 2 t^{2},\,0\le t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=1.$

- $\frac{4}{3}$
- $\frac{8}{3}$
- $\frac{2}{3}$
- $\frac{3}{2}$
- $\frac{3}{4}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=6 t^{2},\,y'(t)=4 t \left(t^{2} + 1\right).
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(4 t \left(t^{2} + 1\right)\right)}{\left(6 t^{2}\right)} \\  & =\frac{2 \left(t^{2} + 1\right)}{3 t}.\end{aligned}
$$

Therefore, when $t=1,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{2 \left(\left(1\right)^{2} + 1\right)}{3 \left(1\right)} \\  & =\frac{4}{3} \\  & =\frac{4}{3}.\end{aligned}
$$

## Generated variant — double_sin_radio / authored-operations / authored_double_sin / observed / seed 11

For the parametric curve 

$$
x=4 \sin {2 t},\,y=5 \sin^{2} {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{11 \pi}{12}.$

- $- \frac{8 \sqrt{3}}{5}$
- $- \frac{5}{4} + \frac{5 \sqrt{3}}{8}$
- $- \frac{5 \sqrt{3}}{24}$
- $\frac{5 \sqrt{3}}{24}$
- $- \frac{5}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=8 \cos {2 t},\,y'(t)=10 \sin {t} \cos {t}=5 \sin {2 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(5 \sin {2 t}\right)}{\left(8 \cos {2 t}\right)} \\  & =\frac{5 \tan {2 t}}{8}.\end{aligned}
$$

Therefore, when $t=\frac{11 \pi}{12},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{5 \tan {2 \left(\frac{11 \pi}{12}\right)}}{8} \\  & =\frac{5 \left(- \frac{\sqrt{3}}{3}\right)}{8} \\  & =- \frac{5 \sqrt{3}}{24}.\end{aligned}
$$

## Generated variant — double_sin_radio / authored-operations / authored_double_sin / observed / seed 23

For the parametric curve 

$$
x=3 \sin {2 t},\,y=\sin^{2} {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi}{12}.$

- $\frac{\sqrt{3}}{18}$
- $\frac{1}{2}$
- $- \frac{\sqrt{3}}{18}$
- $6 \sqrt{3}$
- $\frac{1}{3} - \frac{\sqrt{3}}{6}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=6 \cos {2 t},\,y'(t)=2 \sin {t} \cos {t}=\sin {2 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(\sin {2 t}\right)}{\left(6 \cos {2 t}\right)} \\  & =\frac{\tan {2 t}}{6}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{12},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\tan {2 \left(\frac{\pi}{12}\right)}}{6} \\  & =\frac{\left(\frac{\sqrt{3}}{3}\right)}{6} \\  & =\frac{\sqrt{3}}{18}.\end{aligned}
$$

## Generated variant — double_cos_radio / authored-operations / authored_double_cos / observed / seed 11

For the parametric curve 

$$
x=4 \sin {2 t},\,y=5 \cos^{2} {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{11 \pi}{12}.$

- $\frac{8 \sqrt{3}}{5}$
- $- \frac{5}{4} - \frac{5 \sqrt{3}}{8}$
- $\frac{5 \sqrt{3}}{24}$
- $- \frac{5 \sqrt{3}}{24}$
- $\frac{5}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=8 \cos {2 t},\,y'(t)=- 10 \sin {t} \cos {t}=- 5 \sin {2 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- 5 \sin {2 t}\right)}{\left(8 \cos {2 t}\right)} \\  & =- \frac{5 \tan {2 t}}{8}.\end{aligned}
$$

Therefore, when $t=\frac{11 \pi}{12},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{5 \tan {2 \left(\frac{11 \pi}{12}\right)}}{8} \\  & =- \frac{5 \left(- \frac{\sqrt{3}}{3}\right)}{8} \\  & =\frac{5 \sqrt{3}}{24}.\end{aligned}
$$

## Generated variant — double_cos_radio / authored-operations / authored_double_cos / observed / seed 23

For the parametric curve 

$$
x=3 \sin {2 t},\,y=\cos^{2} {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi}{12}.$

- $- \frac{\sqrt{3}}{18}$
- $- \frac{1}{2}$
- $\frac{\sqrt{3}}{18}$
- $- 6 \sqrt{3}$
- $\frac{\sqrt{3}}{6} + \frac{1}{3}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=6 \cos {2 t},\,y'(t)=- 2 \sin {t} \cos {t}=- \sin {2 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- \sin {2 t}\right)}{\left(6 \cos {2 t}\right)} \\  & =- \frac{\tan {2 t}}{6}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{12},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{\tan {2 \left(\frac{\pi}{12}\right)}}{6} \\  & =- \frac{\left(\frac{\sqrt{3}}{3}\right)}{6} \\  & =- \frac{\sqrt{3}}{18}.\end{aligned}
$$

## Generated variant — poly5_radio / authored-operations / authored_poly5 / observed / seed 11

For the parametric curve 

$$
x=4 t^{2} + 3,\,y=5 t^{5} + t^{3},\,0\le t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=2.$

- $\frac{4}{103}$
- $412$
- $\frac{103}{4}$
- $- \frac{103}{4}$
- $\frac{168}{19}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=8 t,\,y'(t)=t^{2} \left(25 t^{2} + 3\right).
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(t^{2} \left(25 t^{2} + 3\right)\right)}{\left(8 t\right)} \\  & =\frac{t \left(25 t^{2} + 3\right)}{8}.\end{aligned}
$$

Therefore, when $t=2,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(2\right) \left(25 \left(2\right)^{2} + 3\right)}{8} \\  & =\frac{206}{8} \\  & =\frac{103}{4}.\end{aligned}
$$

## Generated variant — poly5_radio / authored-operations / authored_poly5 / observed / seed 23

For the parametric curve 

$$
x=3 t^{2} - 4,\,y=t^{5} + t^{3},\,0\le t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=3.$

- $24$
- $\frac{270}{23}$
- $-24$
- $432$
- $\frac{1}{24}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=6 t,\,y'(t)=t^{2} \left(5 t^{2} + 3\right).
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(t^{2} \left(5 t^{2} + 3\right)\right)}{\left(6 t\right)} \\  & =\frac{t \left(5 t^{2} + 3\right)}{6}.\end{aligned}
$$

Therefore, when $t=3,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(3\right) \left(5 \left(3\right)^{2} + 3\right)}{6} \\  & =\frac{144}{6} \\  & =24.\end{aligned}
$$

## Generated variant — trig_poly_radio / authored-operations / authored_trig_poly / observed / seed 11

For the parametric curve 

$$
x=4 \sin {t},\,y=\frac{5 t^{2}}{\pi},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{7 \pi}{4}.$

- $\frac{4 \sqrt{2}}{35}$
- $- \frac{245 \sqrt{2} \pi}{64}$
- $\frac{35 \sqrt{2}}{8}$
- $- \frac{35 \sqrt{2}}{8}$
- $\frac{35}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=4 \cos {t},\,y'(t)=\frac{10 t}{\pi}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(\frac{10 t}{\pi}\right)}{\left(4 \cos {t}\right)} \\  & =\frac{5 t \sec {t}}{2 \pi}.\end{aligned}
$$

Therefore, when $t=\frac{7 \pi}{4},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{5 \left(\frac{7 \pi}{4}\right) \sec {\left(\frac{7 \pi}{4}\right)}}{2 \pi} \\  & =\frac{5 \left(\frac{7 \pi}{4}\right) \left(\sqrt{2}\right)}{2 \pi} \\  & =\frac{35 \sqrt{2}}{8}.\end{aligned}
$$

## Generated variant — trig_poly_radio / authored-operations / authored_trig_poly / observed / seed 23

For the parametric curve 

$$
x=3 \sin {t},\,y=\frac{t^{2}}{\pi},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi}{4}.$

- $\frac{\sqrt{2}}{6}$
- $\frac{1}{2}$
- $- \frac{\sqrt{2}}{6}$
- $3 \sqrt{2}$
- $\frac{\sqrt{2} \pi}{48}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=3 \cos {t},\,y'(t)=\frac{2 t}{\pi}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(\frac{2 t}{\pi}\right)}{\left(3 \cos {t}\right)} \\  & =\frac{2 t \sec {t}}{3 \pi}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{4},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{2 \left(\frac{\pi}{4}\right) \sec {\left(\frac{\pi}{4}\right)}}{3 \pi} \\  & =\frac{2 \left(\frac{\pi}{4}\right) \left(\sqrt{2}\right)}{3 \pi} \\  & =\frac{\sqrt{2}}{6}.\end{aligned}
$$

## Generated variant — cubic_radio / authored-operations / authored_cubic / observed / seed 11

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/curve-bce2618698b1cc516783.png)

For the parametric curve 

$$
x=t^{3} + 4 t^{2},\,y=5 t^{2},\,-\infty<t<\infty,
$$

shown above, calculate the slope of the tangent to the curve at the point where $t=1.$

- $\frac{11}{10}$
- $1$
- $\frac{10}{11}$
- $- \frac{10}{11}$
- $10$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=3 t^{2} + 8 t,\,y'(t)=10 t.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(10 t\right)}{\left(3 t^{2} + 8 t\right)} \\  & =\frac{10}{3 t + 8}.\end{aligned}
$$

Therefore, when $t=1,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{10}{3 \left(1\right) + 8} \\  & =\frac{10}{11} \\  & =\frac{10}{11}.\end{aligned}
$$

## Generated variant — cubic_radio / authored-operations / authored_cubic / observed / seed 23

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/curve-d5ee25e8dc0e3282818d.png)

For the parametric curve 

$$
x=t^{3} + 5 t^{2},\,y=3 t^{2},\,-\infty<t<\infty,
$$

shown above, calculate the slope of the tangent to the curve at the point where $t=1.$

- $- \frac{6}{13}$
- $\frac{1}{2}$
- $\frac{6}{13}$
- $\frac{13}{6}$
- $6$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=3 t^{2} + 10 t,\,y'(t)=6 t.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(6 t\right)}{\left(3 t^{2} + 10 t\right)} \\  & =\frac{6}{3 t + 10}.\end{aligned}
$$

Therefore, when $t=1,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{6}{3 \left(1\right) + 10} \\  & =\frac{6}{13} \\  & =\frac{6}{13}.\end{aligned}
$$

## Generated variant — cubic_blank / observed-blank / None / compatible-exact / seed 11

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/curve-bce2618698b1cc516783.png)

For the parametric curve 

$$
x=t^{3} + 4 t^{2},\,y=5 t^{2},\,-\infty<t<\infty,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=1.$ Give an exact answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=3 t^{2} + 8 t,\,y'(t)=10 t.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(10 t\right)}{\left(3 t^{2} + 8 t\right)} \\  & =\frac{10}{3 t + 8}.\end{aligned}
$$

Therefore, when $t=1,$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=1} & =\frac{10}{3 \left(1\right) + 8} \\  & =\frac{10}{11} \\  & =\frac{10}{11}.\end{aligned}
$$

## Generated variant — cubic_blank / observed-blank / None / compatible-exact / seed 23

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/curve-c3b85b289d20c3b5209f.png)

For the parametric curve 

$$
x=t^{3} + 3 t^{2},\,y=t^{2},\,-\infty<t<\infty,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=-3.$ Give an exact answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=3 t^{2} + 6 t,\,y'(t)=2 t.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(2 t\right)}{\left(3 t^{2} + 6 t\right)} \\  & =\frac{2}{3 t + 6}.\end{aligned}
$$

Therefore, when $t=-3,$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=-3} & =\frac{2}{3 \left(-3\right) + 6} \\  & =\frac{2}{-3} \\  & =- \frac{2}{3}.\end{aligned}
$$

## Generated variant — linear_trig_radio / authored-operations / authored_linear_trig / observed / seed 11

For the parametric curve 

$$
x=4 t + \sin {t},\,y=5 t + \cos {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{3 \pi}{2}.$

- $\frac{5}{4}$
- $\frac{\sqrt{2}}{31} + \frac{39}{31}$
- $\frac{3}{2}$
- $1$
- $\frac{15 \pi}{8}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=\cos {t} + 4,\,y'(t)=5 - \sin {t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(5 - \sin {t}\right)}{\left(\cos {t} + 4\right)} \\  & =\frac{5 - \sin {t}}{\cos {t} + 4}.\end{aligned}
$$

Therefore, when $t=\frac{3 \pi}{2},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{5 - \sin {\left(\frac{3 \pi}{2}\right)}}{\cos {\left(\frac{3 \pi}{2}\right)} + 4} \\  & =\frac{5 - \left(-1\right)}{\left(0\right) + 4} \\  & =\frac{3}{2}.\end{aligned}
$$

## Generated variant — linear_trig_radio / authored-operations / authored_linear_trig / observed / seed 23

For the parametric curve 

$$
x=3 t + \sin {t},\,y=t + \cos {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi}{2}.$

- $0$
- $\frac{\pi}{6}$
- $\frac{2}{3}$
- $\frac{1}{3}$
- $\frac{7}{17} - \frac{4 \sqrt{2}}{17}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=\cos {t} + 3,\,y'(t)=1 - \sin {t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(1 - \sin {t}\right)}{\left(\cos {t} + 3\right)} \\  & =\frac{1 - \sin {t}}{\cos {t} + 3}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{2},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{1 - \sin {\left(\frac{\pi}{2}\right)}}{\cos {\left(\frac{\pi}{2}\right)} + 3} \\  & =\frac{1 - \left(1\right)}{\left(0\right) + 3} \\  & =0.\end{aligned}
$$

## Generated variant — poly4_radio / authored-operations / authored_poly4 / observed / seed 11

For the parametric curve 

$$
x=4 t^{3} + 1,\,y=5 t^{4} + 4 t^{2},\,0\le t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=2.$

- $\frac{3}{11}$
- $176$
- $\frac{11}{3}$
- $- \frac{11}{3}$
- $\frac{32}{11}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=12 t^{2},\,y'(t)=4 t \left(5 t^{2} + 2\right).
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(4 t \left(5 t^{2} + 2\right)\right)}{\left(12 t^{2}\right)} \\  & =\frac{5 t^{2} + 2}{3 t}.\end{aligned}
$$

Therefore, when $t=2,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{5 \left(2\right)^{2} + 2}{3 \left(2\right)} \\  & =\frac{22}{6} \\  & =\frac{11}{3}.\end{aligned}
$$

## Generated variant — poly4_radio / authored-operations / authored_poly4 / observed / seed 23

For the parametric curve 

$$
x=3 t^{3} + 1,\,y=t^{4} + t^{2},\,0\le t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=3.$

- $\frac{38}{27}$
- $\frac{45}{41}$
- $- \frac{38}{27}$
- $114$
- $\frac{27}{38}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=9 t^{2},\,y'(t)=2 t \left(2 t^{2} + 1\right).
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(2 t \left(2 t^{2} + 1\right)\right)}{\left(9 t^{2}\right)} \\  & =\frac{2 \left(2 t^{2} + 1\right)}{9 t}.\end{aligned}
$$

Therefore, when $t=3,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{2 \left(2 \left(3\right)^{2} + 1\right)}{9 \left(3\right)} \\  & =\frac{38}{27} \\  & =\frac{38}{27}.\end{aligned}
$$

## Generated variant — harmonic_radio / authored-operations / authored_harmonic / observed / seed 11

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/curve-8376daa745d6d658e17b.png)

For the parametric curve 

$$
x=4 \cos {t},\,y=5 \sin {3 t},\,0\le t<2\pi,
$$

shown above, calculate the slope of the tangent to the curve at the point where $t=\frac{5 \pi}{4}.$

- $\frac{4}{15}$
- $\frac{15 \sqrt{2}}{2}$
- $\frac{15}{4}$
- $- \frac{15}{4}$
- $\frac{5}{4}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- 4 \sin {t},\,y'(t)=15 \cos {3 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(15 \cos {3 t}\right)}{\left(- 4 \sin {t}\right)} \\  & =- \frac{15 \cos {3 t}}{4 \sin {t}}.\end{aligned}
$$

Therefore, when $t=\frac{5 \pi}{4},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{15 \cos {3 \left(\frac{5 \pi}{4}\right)}}{4 \sin {\left(\frac{5 \pi}{4}\right)}} \\  & =- \frac{15 \left(\frac{\sqrt{2}}{2}\right)}{4 \left(- \frac{\sqrt{2}}{2}\right)} \\  & =\frac{15}{4}.\end{aligned}
$$

## Generated variant — harmonic_radio / authored-operations / authored_harmonic / observed / seed 23

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/curve-4ec0b6f5134ba57327b1.png)

For the parametric curve 

$$
x=3 \cos {t},\,y=\sin {2 t},\,0\le t<2\pi,
$$

shown above, calculate the slope of the tangent to the curve at the point where $t=\frac{5 \pi}{3}.$

- $- \frac{2 \sqrt{3}}{9}$
- $- \frac{\sqrt{3}}{3}$
- $\frac{2 \sqrt{3}}{9}$
- $-1$
- $- \frac{3 \sqrt{3}}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- 3 \sin {t},\,y'(t)=2 \cos {2 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(2 \cos {2 t}\right)}{\left(- 3 \sin {t}\right)} \\  & =- \frac{2 \cos {2 t}}{3 \sin {t}}.\end{aligned}
$$

Therefore, when $t=\frac{5 \pi}{3},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{2 \cos {2 \left(\frac{5 \pi}{3}\right)}}{3 \sin {\left(\frac{5 \pi}{3}\right)}} \\  & =- \frac{2 \left(- \frac{1}{2}\right)}{3 \left(- \frac{\sqrt{3}}{2}\right)} \\  & =- \frac{2 \sqrt{3}}{9}.\end{aligned}
$$

## Generated variant — harmonic_blank / observed-blank / None / compatible-exact / seed 11

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/curve-8376daa745d6d658e17b.png)

For the parametric curve 

$$
x=4 \cos {t},\,y=5 \sin {3 t},\,0\le t<2\pi,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=\frac{5 \pi}{4}.$ Give an exact answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- 4 \sin {t},\,y'(t)=15 \cos {3 t}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(15 \cos {3 t}\right)}{\left(- 4 \sin {t}\right)} \\  & =- \frac{15 \cos {3 t}}{4 \sin {t}}.\end{aligned}
$$

Therefore, when $t=\frac{5 \pi}{4},$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=\frac{5 \pi}{4}} & =- \frac{15 \cos {3 \left(\frac{5 \pi}{4}\right)}}{4 \sin {\left(\frac{5 \pi}{4}\right)}} \\  & =- \frac{15 \left(\frac{\sqrt{2}}{2}\right)}{4 \left(- \frac{\sqrt{2}}{2}\right)} \\  & =\frac{15}{4}.\end{aligned}
$$

## Generated variant — harmonic_blank / observed-blank / None / compatible-exact / seed 23

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/curve-4ec0b6f5134ba57327b1.png)

For the parametric curve 

$$
x=3 \cos {t},\,y=\sin {2 t},\,0\le t<2\pi,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=\frac{5 \pi}{3}.$ Give an exact answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- 3 \sin {t},\,y'(t)=2 \cos {2 t}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(2 \cos {2 t}\right)}{\left(- 3 \sin {t}\right)} \\  & =- \frac{2 \cos {2 t}}{3 \sin {t}}.\end{aligned}
$$

Therefore, when $t=\frac{5 \pi}{3},$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=\frac{5 \pi}{3}} & =- \frac{2 \cos {2 \left(\frac{5 \pi}{3}\right)}}{3 \sin {\left(\frac{5 \pi}{3}\right)}} \\  & =- \frac{2 \left(- \frac{1}{2}\right)}{3 \left(- \frac{\sqrt{3}}{2}\right)} \\  & =- \frac{2 \sqrt{3}}{9}.\end{aligned}
$$

## Generated variant — ellipse_blank / observed-blank / None / compatible-exact / seed 11

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/curve-384efb26f996cc74e473.png)

For the parametric curve 

$$
x=4 \sin {t},\,y=5 \cos {t},\,0\le t<2\pi,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=\frac{5 \pi}{4}.$ Give an exact answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=4 \cos {t},\,y'(t)=- 5 \sin {t}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- 5 \sin {t}\right)}{\left(4 \cos {t}\right)} \\  & =- \frac{5 \tan {t}}{4}.\end{aligned}
$$

Therefore, when $t=\frac{5 \pi}{4},$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=\frac{5 \pi}{4}} & =- \frac{5 \tan {\left(\frac{5 \pi}{4}\right)}}{4} \\  & =- \frac{5 \left(1\right)}{4} \\  & =- \frac{5}{4}.\end{aligned}
$$

## Generated variant — ellipse_blank / observed-blank / None / compatible-exact / seed 23

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/curve-a27eaa39b11c0e33083e.png)

For the parametric curve 

$$
x=3 \sin {t},\,y=\cos {t},\,0\le t<2\pi,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=\frac{\pi}{6}.$ Give an exact answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=3 \cos {t},\,y'(t)=- \sin {t}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- \sin {t}\right)}{\left(3 \cos {t}\right)} \\  & =- \frac{\tan {t}}{3}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{6},$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=\frac{\pi}{6}} & =- \frac{\tan {\left(\frac{\pi}{6}\right)}}{3} \\  & =- \frac{\left(\frac{\sqrt{3}}{3}\right)}{3} \\  & =- \frac{\sqrt{3}}{9}.\end{aligned}
$$

## Generated variant — exp_root_radio / authored-operations / authored_exp_root / observed / seed 11

For the parametric curve 

$$
x=\frac{1}{4 \sqrt{t}},\,y=\frac{e^{t}}{5 t},\,0<t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=5.$

- $- \frac{5 \sqrt{5}}{32 e^{5}}$
- $\frac{4 \sqrt{5} e^{5}}{25}$
- $- \frac{32 \sqrt{5} e^{5}}{25}$
- $\frac{32 \sqrt{5} e^{5}}{25}$
- $\frac{4 e^{5}}{125}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{1}{8 t^{\frac{3}{2}}},\,y'(t)=\frac{5 t e^{t} - 5 e^{t}}{25 t^{2}}=\frac{\left(t - 1\right) e^{t}}{5 t^{2}}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(t - 1\right) e^{t}}{5 t^{2}}\cdot \left(- 8 t^{\frac{3}{2}}\right) \\  & =- \frac{8 \left(t - 1\right) e^{t}}{5 \sqrt{t}}.\end{aligned}
$$

Therefore, when $t=5,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{8 \left(\left(5\right) - 1\right) e^{\left(5\right)}}{5 \sqrt{\left(5\right)}} \\  & =\frac{- 32 e^{5}}{5 \sqrt{5}} \\  & =- \frac{32 \sqrt{5} e^{5}}{25}.\end{aligned}
$$

## Generated variant — exp_root_radio / authored-operations / authored_exp_root / observed / seed 23

For the parametric curve 

$$
x=\frac{1}{3 \sqrt{t}},\,y=\frac{e^{t}}{t},\,0<t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=2.$

- $- 3 \sqrt{2} e^{2}$
- $\frac{e^{2}}{4}$
- $3 \sqrt{2} e^{2}$
- $- \frac{\sqrt{2}}{6 e^{2}}$
- $\frac{3 \sqrt{2} e^{2}}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{1}{6 t^{\frac{3}{2}}},\,y'(t)=\frac{t e^{t} - e^{t}}{t^{2}}=\frac{\left(t - 1\right) e^{t}}{t^{2}}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(t - 1\right) e^{t}}{t^{2}}\cdot \left(- 6 t^{\frac{3}{2}}\right) \\  & =- \frac{6 \left(t - 1\right) e^{t}}{\sqrt{t}}.\end{aligned}
$$

Therefore, when $t=2,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{6 \left(\left(2\right) - 1\right) e^{\left(2\right)}}{\sqrt{\left(2\right)}} \\  & =\frac{- 6 e^{2}}{\sqrt{2}} \\  & =- 3 \sqrt{2} e^{2}.\end{aligned}
$$

## Generated variant — exp_root_blank / observed-blank / None / compatible-exact / seed 11

For the parametric curve 

$$
x=\frac{1}{4 \sqrt{t}},\,y=\frac{e^{t}}{5 t},\,0<t<\infty,
$$

calculate the slope $m$ of the tangent to the curve at the point where $t=5.$ Give an exact answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{1}{8 t^{\frac{3}{2}}},\,y'(t)=\frac{5 t e^{t} - 5 e^{t}}{25 t^{2}}=\frac{\left(t - 1\right) e^{t}}{5 t^{2}}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(t - 1\right) e^{t}}{5 t^{2}}\cdot \left(- 8 t^{\frac{3}{2}}\right) \\  & =- \frac{8 \left(t - 1\right) e^{t}}{5 \sqrt{t}}.\end{aligned}
$$

Therefore, when $t=5,$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=5} & =- \frac{8 \left(\left(5\right) - 1\right) e^{\left(5\right)}}{5 \sqrt{\left(5\right)}} \\  & =\frac{- 32 e^{5}}{5 \sqrt{5}} \\  & =- \frac{32 \sqrt{5} e^{5}}{25}.\end{aligned}
$$

## Generated variant — exp_root_blank / observed-blank / None / compatible-exact / seed 23

For the parametric curve 

$$
x=\frac{1}{3 \sqrt{t}},\,y=\frac{e^{t}}{t},\,0<t<\infty,
$$

calculate the slope $m$ of the tangent to the curve at the point where $t=2.$ Give an exact answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{1}{6 t^{\frac{3}{2}}},\,y'(t)=\frac{t e^{t} - e^{t}}{t^{2}}=\frac{\left(t - 1\right) e^{t}}{t^{2}}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(t - 1\right) e^{t}}{t^{2}}\cdot \left(- 6 t^{\frac{3}{2}}\right) \\  & =- \frac{6 \left(t - 1\right) e^{t}}{\sqrt{t}}.\end{aligned}
$$

Therefore, when $t=2,$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=2} & =- \frac{6 \left(\left(2\right) - 1\right) e^{\left(2\right)}}{\sqrt{\left(2\right)}} \\  & =\frac{- 6 e^{2}}{\sqrt{2}} \\  & =- 3 \sqrt{2} e^{2}.\end{aligned}
$$

## Generated variant — reciprocal_exp_root_radio / authored-operations / authored_reciprocal_exp_root / observed / seed 11

For the parametric curve 

$$
x=e^{\frac{4}{t}},\,y=\frac{5}{\sqrt{t^{2} + 3}},\,0<t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=3.$

- $\frac{32 \sqrt{3} e^{\frac{4}{3}}}{45}$
- $- \frac{5 \sqrt{3}}{24}$
- $\frac{15 \sqrt{3}}{32 e^{\frac{4}{3}}}$
- $- \frac{15 \sqrt{3}}{32 e^{\frac{4}{3}}}$
- $\frac{5 \sqrt{3}}{6 e^{\frac{4}{3}}}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{4 e^{\frac{4}{t}}}{t^{2}},\,y'(t)=- \frac{5 t}{\left(t^{2} + 3\right)^{\frac{3}{2}}}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- \frac{5 t}{\left(t^{2} + 3\right)^{\frac{3}{2}}}\right)}{\left(- \frac{4 e^{\frac{4}{t}}}{t^{2}}\right)} \\  & =\frac{5 t^{3} e^{- \frac{4}{t}}}{4 \left(t^{2} + 3\right)^{\frac{3}{2}}}.\end{aligned}
$$

Therefore, when $t=3,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{5 \left(3\right)^{3} e^{- \frac{4}{\left(3\right)}}}{4 \left(\left(3\right)^{2} + 3\right)^{\frac{3}{2}}} \\  & =\frac{135}{96 \sqrt{3} e^{\frac{4}{3}}} \\  & =\frac{15 \sqrt{3}}{32 e^{\frac{4}{3}}}.\end{aligned}
$$

## Generated variant — reciprocal_exp_root_radio / authored-operations / authored_reciprocal_exp_root / observed / seed 23

For the parametric curve 

$$
x=e^{\frac{3}{t}},\,y=\frac{1}{\sqrt{t^{2} - 1}},\,1<t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=4.$

- $\frac{64 \sqrt{15}}{675 e^{\frac{3}{4}}}$
- $\frac{\sqrt{15}}{15 e^{\frac{3}{4}}}$
- $- \frac{64 \sqrt{15}}{675 e^{\frac{3}{4}}}$
- $- \frac{4 \sqrt{15}}{225}$
- $\frac{45 \sqrt{15} e^{\frac{3}{4}}}{64}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{3 e^{\frac{3}{t}}}{t^{2}},\,y'(t)=- \frac{t}{\left(t^{2} - 1\right)^{\frac{3}{2}}}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- \frac{t}{\left(t^{2} - 1\right)^{\frac{3}{2}}}\right)}{\left(- \frac{3 e^{\frac{3}{t}}}{t^{2}}\right)} \\  & =\frac{t^{3} e^{- \frac{3}{t}}}{3 \left(t^{2} - 1\right)^{\frac{3}{2}}}.\end{aligned}
$$

Therefore, when $t=4,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(4\right)^{3} e^{- \frac{3}{\left(4\right)}}}{3 \left(\left(4\right)^{2} - 1\right)^{\frac{3}{2}}} \\  & =\frac{64}{45 \sqrt{15} e^{\frac{3}{4}}} \\  & =\frac{64 \sqrt{15}}{675 e^{\frac{3}{4}}}.\end{aligned}
$$

## Generated variant — reciprocal_exp_root_blank / observed-blank / None / compatible-exact / seed 11

For the parametric curve 

$$
x=e^{\frac{4}{t}},\,y=\frac{5}{\sqrt{t^{2} + 3}},\,0<t<\infty,
$$

calculate the slope $m$ of the tangent to the curve at the point where $t=3.$ Give an exact answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{4 e^{\frac{4}{t}}}{t^{2}},\,y'(t)=- \frac{5 t}{\left(t^{2} + 3\right)^{\frac{3}{2}}}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- \frac{5 t}{\left(t^{2} + 3\right)^{\frac{3}{2}}}\right)}{\left(- \frac{4 e^{\frac{4}{t}}}{t^{2}}\right)} \\  & =\frac{5 t^{3} e^{- \frac{4}{t}}}{4 \left(t^{2} + 3\right)^{\frac{3}{2}}}.\end{aligned}
$$

Therefore, when $t=3,$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=3} & =\frac{5 \left(3\right)^{3} e^{- \frac{4}{\left(3\right)}}}{4 \left(\left(3\right)^{2} + 3\right)^{\frac{3}{2}}} \\  & =\frac{135}{96 \sqrt{3} e^{\frac{4}{3}}} \\  & =\frac{15 \sqrt{3}}{32 e^{\frac{4}{3}}}.\end{aligned}
$$

## Generated variant — reciprocal_exp_root_blank / observed-blank / None / compatible-exact / seed 23

For the parametric curve 

$$
x=e^{\frac{3}{t}},\,y=\frac{1}{\sqrt{t^{2} - 1}},\,1<t<\infty,
$$

calculate the slope $m$ of the tangent to the curve at the point where $t=4.$ Give an exact answer.

$m=$
{{field-1}}



We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{3 e^{\frac{3}{t}}}{t^{2}},\,y'(t)=- \frac{t}{\left(t^{2} - 1\right)^{\frac{3}{2}}}.
$$

 

So, we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- \frac{t}{\left(t^{2} - 1\right)^{\frac{3}{2}}}\right)}{\left(- \frac{3 e^{\frac{3}{t}}}{t^{2}}\right)} \\  & =\frac{t^{3} e^{- \frac{3}{t}}}{3 \left(t^{2} - 1\right)^{\frac{3}{2}}}.\end{aligned}
$$

Therefore, when $t=4,$ the slope $m$ of the tangent to the curve is

$$
\begin{aligned}m=\frac{dy}{dx}\,{|}_{t=4} & =\frac{\left(4\right)^{3} e^{- \frac{3}{\left(4\right)}}}{3 \left(\left(4\right)^{2} - 1\right)^{\frac{3}{2}}} \\  & =\frac{64}{45 \sqrt{15} e^{\frac{3}{4}}} \\  & =\frac{64 \sqrt{15}}{675 e^{\frac{3}{4}}}.\end{aligned}
$$

## Generated variant — nested_trig_radio / authored-operations / authored_nested_trig / observed / seed 11

For the parametric curve 

$$
x=4 \sqrt{\sin{\left(e^{t} \right)}},\,y=5 \cot{\left(e^{t} \right)},\,-\infty<t<1,
$$

calculate the slope of the tangent to the curve at the point where $t=\ln{\left(\frac{5 \pi}{6} \right)}.$

- $\frac{\sqrt{6}}{20}$
- $- \frac{5 \sqrt{6}}{4}$
- $\frac{10 \sqrt{6}}{3}$
- $- \frac{10 \sqrt{6}}{3}$
- $- \frac{50 \pi}{3}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
\begin{aligned}x'(t)&=\frac{4}{2 \sqrt{\sin{\left(e^{t} \right)}}}\cdot \cos{\left(e^{t} \right)}\cdot e^{t}\\ &= \frac{2 e^{t} \cos{\left(e^{t} \right)}}{\sqrt{\sin{\left(e^{t} \right)}}},\\ y'(t)&=- 5 e^{t} \csc^{2}{\left(e^{t} \right)}.\end{aligned}
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- 5 e^{t} \csc^{2}{\left(e^{t} \right)}\right)}{\left(\frac{2 e^{t} \cos{\left(e^{t} \right)}}{\sqrt{\sin{\left(e^{t} \right)}}}\right)} \\  & =\frac{- 10 \sqrt{\sin{\left(e^{t} \right)}}}{4 \sin^{2}{\left(e^{t} \right)} \cos{\left(e^{t} \right)}} \\  & =- \frac{5}{2 \sin^{\frac{3}{2}}{\left(e^{t} \right)} \cos{\left(e^{t} \right)}}.\end{aligned}
$$

Therefore, when $t=\ln{\left(\frac{5 \pi}{6} \right)},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{5}{2 \sin^{\frac{3}{2}}{\left(e^{\left(\ln{\left(\frac{5 \pi}{6} \right)}\right)} \right)} \cos{\left(e^{\left(\ln{\left(\frac{5 \pi}{6} \right)}\right)} \right)}} \\  & =- \frac{5}{2 \sin^{\frac{3}{2}}{\left(e^{\left(\ln{\left(\frac{5 \pi}{6} \right)}\right)} \right)} \left(- \frac{\sqrt{3}}{2}\right)} \\  & =\frac{10 \sqrt{6}}{3}.\end{aligned}
$$

## Generated variant — nested_trig_radio / authored-operations / authored_nested_trig / observed / seed 23

For the parametric curve 

$$
x=3 \sqrt{\sin{\left(e^{t} \right)}},\,y=\cot{\left(e^{t} \right)},\,-\infty<t<1,
$$

calculate the slope of the tangent to the curve at the point where $t=\ln{\left(\frac{\pi}{6} \right)}.$

- $- \frac{8 \sqrt{6}}{9}$
- $- \frac{2 \pi}{3}$
- $\frac{8 \sqrt{6}}{9}$
- $- \frac{3 \sqrt{6}}{16}$
- $\frac{\sqrt{6}}{3}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
\begin{aligned}x'(t)&=\frac{3}{2 \sqrt{\sin{\left(e^{t} \right)}}}\cdot \cos{\left(e^{t} \right)}\cdot e^{t}\\ &= \frac{3 e^{t} \cos{\left(e^{t} \right)}}{2 \sqrt{\sin{\left(e^{t} \right)}}},\\ y'(t)&=- e^{t} \csc^{2}{\left(e^{t} \right)}.\end{aligned}
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- e^{t} \csc^{2}{\left(e^{t} \right)}\right)}{\left(\frac{3 e^{t} \cos{\left(e^{t} \right)}}{2 \sqrt{\sin{\left(e^{t} \right)}}}\right)} \\  & =\frac{- 2 \sqrt{\sin{\left(e^{t} \right)}}}{3 \sin^{2}{\left(e^{t} \right)} \cos{\left(e^{t} \right)}} \\  & =- \frac{2}{3 \sin^{\frac{3}{2}}{\left(e^{t} \right)} \cos{\left(e^{t} \right)}}.\end{aligned}
$$

Therefore, when $t=\ln{\left(\frac{\pi}{6} \right)},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{2}{3 \sin^{\frac{3}{2}}{\left(e^{\left(\ln{\left(\frac{\pi}{6} \right)}\right)} \right)} \cos{\left(e^{\left(\ln{\left(\frac{\pi}{6} \right)}\right)} \right)}} \\  & =- \frac{2}{3 \sin^{\frac{3}{2}}{\left(e^{\left(\ln{\left(\frac{\pi}{6} \right)}\right)} \right)} \left(\frac{\sqrt{3}}{2}\right)} \\  & =- \frac{8 \sqrt{6}}{9}.\end{aligned}
$$

## Generated variant — double_sin_radio / observed-expression-pattern / observed_q-102922 / observed / seed 37

For the parametric curve 

$$
x=6 \sin {2 t},\,y=5 \sin^{2} {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi}{6}.$

- $- \frac{5 \sqrt{3}}{12}$
- $- \frac{5 \sqrt{3}}{4}$
- $\frac{5 \sqrt{3}}{2}$
- $\frac{5 \sqrt{3}}{12}$
- $\frac{5 \sqrt{3}}{4}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=12 \cos {2 t},\,y'(t)=10 \sin {t} \cos {t}=5 \sin {2 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(5 \sin {2 t}\right)}{\left(12 \cos {2 t}\right)} \\  & =\frac{5 \tan {2 t}}{12}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{6},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{5 \tan {2 \left(\frac{\pi}{6}\right)}}{12} \\  & =\frac{5 \left(\sqrt{3}\right)}{12} \\  & =\frac{5 \sqrt{3}}{12}.\end{aligned}
$$

## Generated variant — double_sin_radio / observed-expression-pattern / observed_q-102922 / observed / seed 49

For the parametric curve 

$$
x=\sin {2 t},\,y=3 \sin^{2} {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{5 \pi}{6}.$

- $\frac{9 \sqrt{3}}{2}$
- $- \frac{9 \sqrt{3}}{2}$
- $\frac{3 \sqrt{3}}{2}$
- $- 9 \sqrt{3}$
- $- \frac{3 \sqrt{3}}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=2 \cos {2 t},\,y'(t)=6 \sin {t} \cos {t}=3 \sin {2 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(3 \sin {2 t}\right)}{\left(2 \cos {2 t}\right)} \\  & =\frac{3 \tan {2 t}}{2}.\end{aligned}
$$

Therefore, when $t=\frac{5 \pi}{6},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{3 \tan {2 \left(\frac{5 \pi}{6}\right)}}{2} \\  & =\frac{3 \left(- \sqrt{3}\right)}{2} \\  & =- \frac{3 \sqrt{3}}{2}.\end{aligned}
$$

## Generated variant — double_cos_radio / observed-expression-pattern / observed_q-15457 / observed / seed 37

For the parametric curve 

$$
x=6 \sin {2 t},\,y=5 \cos^{2} {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi}{6}.$

- $- \frac{5 \sqrt{3}}{6}$
- $- \frac{5}{12}$
- $- \frac{5 \sqrt{3}}{12}$
- $\frac{5 \sqrt{3}}{6}$
- $\frac{5}{12}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=12 \cos {2 t},\,y'(t)=- 10 \sin {t} \cos {t}=- 5 \sin {2 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- 5 \sin {2 t}\right)}{\left(12 \cos {2 t}\right)} \\  & =- \frac{5 \tan {2 t}}{12}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{6},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{5 \tan {2 \left(\frac{\pi}{6}\right)}}{12} \\  & =- \frac{5 \left(\sqrt{3}\right)}{12} \\  & =- \frac{5 \sqrt{3}}{12}.\end{aligned}
$$

## Generated variant — double_cos_radio / observed-expression-pattern / observed_q-15457 / observed / seed 49

For the parametric curve 

$$
x=\sin {2 t},\,y=3 \cos^{2} {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{5 \pi}{6}.$

- $- \frac{3}{2}$
- $\frac{3}{2}$
- $3 \sqrt{3}$
- $\frac{3 \sqrt{3}}{2}$
- $- 3 \sqrt{3}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=2 \cos {2 t},\,y'(t)=- 6 \sin {t} \cos {t}=- 3 \sin {2 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- 3 \sin {2 t}\right)}{\left(2 \cos {2 t}\right)} \\  & =- \frac{3 \tan {2 t}}{2}.\end{aligned}
$$

Therefore, when $t=\frac{5 \pi}{6},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{3 \tan {2 \left(\frac{5 \pi}{6}\right)}}{2} \\  & =- \frac{3 \left(- \sqrt{3}\right)}{2} \\  & =\frac{3 \sqrt{3}}{2}.\end{aligned}
$$

## Generated variant — poly5_radio / observed-expression-pattern / observed_q-102940 / observed / seed 37

For the parametric curve 

$$
x=6 t^{2} - 3,\,y=5 t^{5} + t^{3},\,0\le t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=3.$

- $57$
- $\frac{675}{4}$
- $\frac{411}{2}$
- $\frac{411}{4}$
- $\frac{9}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=12 t,\,y'(t)=t^{2} \left(25 t^{2} + 3\right).
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(t^{2} \left(25 t^{2} + 3\right)\right)}{\left(12 t\right)} \\  & =\frac{t \left(25 t^{2} + 3\right)}{12}.\end{aligned}
$$

Therefore, when $t=3,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(3\right) \left(25 \left(3\right)^{2} + 3\right)}{12} \\  & =\frac{684}{12} \\  & =57.\end{aligned}
$$

## Generated variant — poly5_radio / observed-expression-pattern / observed_q-102940 / observed / seed 49

For the parametric curve 

$$
x=t^{2} + 2,\,y=3 t^{5} + t^{3},\,0\le t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=1.$

- $\frac{15}{2}$
- $9$
- $3$
- $\frac{11}{2}$
- $11$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=2 t,\,y'(t)=3 t^{2} \left(5 t^{2} + 1\right).
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(3 t^{2} \left(5 t^{2} + 1\right)\right)}{\left(2 t\right)} \\  & =\frac{3 t \left(5 t^{2} + 1\right)}{2}.\end{aligned}
$$

Therefore, when $t=1,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{3 \left(1\right) \left(5 \left(1\right)^{2} + 1\right)}{2} \\  & =\frac{18}{2} \\  & =9.\end{aligned}
$$

## Generated variant — trig_poly_radio / observed-expression-pattern / observed_q-102941 / observed / seed 37

For the parametric curve 

$$
x=6 \sin {t},\,y=\frac{5 t^{2}}{\pi},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi}{4}.$

- $\frac{5}{12}$
- $\frac{5 \sqrt{2}}{3}$
- $\frac{5 \sqrt{2}}{6}$
- $\frac{5 \sqrt{2}}{12}$
- $\frac{5}{3}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=6 \cos {t},\,y'(t)=\frac{10 t}{\pi}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(\frac{10 t}{\pi}\right)}{\left(6 \cos {t}\right)} \\  & =\frac{5 t \sec {t}}{3 \pi}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{4},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{5 \left(\frac{\pi}{4}\right) \sec {\left(\frac{\pi}{4}\right)}}{3 \pi} \\  & =\frac{5 \left(\frac{\pi}{4}\right) \left(\sqrt{2}\right)}{3 \pi} \\  & =\frac{5 \sqrt{2}}{12}.\end{aligned}
$$

## Generated variant — trig_poly_radio / observed-expression-pattern / observed_q-102941 / observed / seed 49

For the parametric curve 

$$
x=\sin {t},\,y=\frac{3 t^{2}}{\pi},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{7 \pi}{4}.$

- $42 \sqrt{2}$
- $42$
- $\frac{21}{2}$
- $21 \sqrt{2}$
- $\frac{21 \sqrt{2}}{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=\cos {t},\,y'(t)=\frac{6 t}{\pi}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(\frac{6 t}{\pi}\right)}{\left(\cos {t}\right)} \\  & =\frac{6 t \sec {t}}{\pi}.\end{aligned}
$$

Therefore, when $t=\frac{7 \pi}{4},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{6 \left(\frac{7 \pi}{4}\right) \sec {\left(\frac{7 \pi}{4}\right)}}{\pi} \\  & =\frac{6 \left(\frac{7 \pi}{4}\right) \left(\sqrt{2}\right)}{\pi} \\  & =\frac{21 \sqrt{2}}{2}.\end{aligned}
$$

## Generated variant — cubic_radio / observed-expression-pattern / observed_q-6730 / observed / seed 37

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/curve-312a55e67826b37c664b.png)

For the parametric curve 

$$
x=t^{3} + 6 t^{2},\,y=5 t^{2},\,-\infty<t<\infty,
$$

shown above, calculate the slope of the tangent to the curve at the point where $t=-3.$

- $\frac{10}{13}$
- $\frac{10}{3}$
- $- \frac{1}{9}$
- $\frac{20}{3}$
- $- \frac{10}{9}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=3 t^{2} + 12 t,\,y'(t)=10 t.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(10 t\right)}{\left(3 t^{2} + 12 t\right)} \\  & =\frac{10}{3 t + 12}.\end{aligned}
$$

Therefore, when $t=-3,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{10}{3 \left(-3\right) + 12} \\  & =\frac{10}{3} \\  & =\frac{10}{3}.\end{aligned}
$$

## Generated variant — cubic_radio / observed-expression-pattern / observed_q-6730 / observed / seed 49

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/curve-bac204aa0d311099ac80.png)

For the parametric curve 

$$
x=t^{3} + t^{2},\,y=3 t^{2},\,-\infty<t<\infty,
$$

shown above, calculate the slope of the tangent to the curve at the point where $t=1.$

- $\frac{6}{5}$
- $2$
- $\frac{6}{11}$
- $\frac{1}{3}$
- $\frac{12}{5}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=3 t^{2} + 2 t,\,y'(t)=6 t.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(6 t\right)}{\left(3 t^{2} + 2 t\right)} \\  & =\frac{6}{3 t + 2}.\end{aligned}
$$

Therefore, when $t=1,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{6}{3 \left(1\right) + 2} \\  & =\frac{6}{5} \\  & =\frac{6}{5}.\end{aligned}
$$

## Generated variant — linear_trig_radio / observed-expression-pattern / observed_q-15465 / observed / seed 37

For the parametric curve 

$$
x=6 t + \sin {t},\,y=5 t + \cos {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi}{2}.$

- $\frac{5 \sqrt{2}}{12}$
- $\frac{5}{12}$
- $\frac{5}{6}$
- $\frac{5 \sqrt{2}}{6}$
- $\frac{2}{3}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=\cos {t} + 6,\,y'(t)=5 - \sin {t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(5 - \sin {t}\right)}{\left(\cos {t} + 6\right)} \\  & =\frac{5 - \sin {t}}{\cos {t} + 6}.\end{aligned}
$$

Therefore, when $t=\frac{\pi}{2},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{5 - \sin {\left(\frac{\pi}{2}\right)}}{\cos {\left(\frac{\pi}{2}\right)} + 6} \\  & =\frac{5 - \left(1\right)}{\left(0\right) + 6} \\  & =\frac{2}{3}.\end{aligned}
$$

## Generated variant — linear_trig_radio / observed-expression-pattern / observed_q-15465 / observed / seed 49

For the parametric curve 

$$
x=t + \sin {t},\,y=3 t + \cos {t},\,0\le t<2\pi,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{3 \pi}{2}.$

- $\frac{3}{2}$
- $4$
- $\frac{3 \sqrt{2}}{2}$
- $3$
- $3 \sqrt{2}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=\cos {t} + 1,\,y'(t)=3 - \sin {t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(3 - \sin {t}\right)}{\left(\cos {t} + 1\right)} \\  & =\frac{3 - \sin {t}}{\cos {t} + 1}.\end{aligned}
$$

Therefore, when $t=\frac{3 \pi}{2},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{3 - \sin {\left(\frac{3 \pi}{2}\right)}}{\cos {\left(\frac{3 \pi}{2}\right)} + 1} \\  & =\frac{3 - \left(-1\right)}{\left(0\right) + 1} \\  & =4.\end{aligned}
$$

## Generated variant — poly4_radio / observed-expression-pattern / observed_q-15469 / observed / seed 37

For the parametric curve 

$$
x=6 t^{3} + 1,\,y=5 t^{4} + t^{2},\,0\le t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=3.$

- $\frac{27}{91}$
- $\frac{182}{27}$
- $\frac{91}{27}$
- $\frac{91}{54}$
- $\frac{54}{91}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=18 t^{2},\,y'(t)=2 t \left(10 t^{2} + 1\right).
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(2 t \left(10 t^{2} + 1\right)\right)}{\left(18 t^{2}\right)} \\  & =\frac{10 t^{2} + 1}{9 t}.\end{aligned}
$$

Therefore, when $t=3,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{10 \left(3\right)^{2} + 1}{9 \left(3\right)} \\  & =\frac{91}{27} \\  & =\frac{91}{27}.\end{aligned}
$$

## Generated variant — poly4_radio / observed-expression-pattern / observed_q-15469 / observed / seed 49

For the parametric curve 

$$
x=t^{3} + 1,\,y=3 t^{4} + 4 t^{2},\,0\le t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=1.$

- $\frac{40}{3}$
- $\frac{3}{20}$
- $\frac{3}{10}$
- $\frac{10}{3}$
- $\frac{20}{3}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=3 t^{2},\,y'(t)=4 t \left(3 t^{2} + 2\right).
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(4 t \left(3 t^{2} + 2\right)\right)}{\left(3 t^{2}\right)} \\  & =\frac{4 \left(3 t^{2} + 2\right)}{3 t}.\end{aligned}
$$

Therefore, when $t=1,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{4 \left(3 \left(1\right)^{2} + 2\right)}{3 \left(1\right)} \\  & =\frac{20}{3} \\  & =\frac{20}{3}.\end{aligned}
$$

## Generated variant — harmonic_radio / observed-expression-pattern / observed_q-6808 / observed / seed 37

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/curve-b87214dba417f11d565d.png)

For the parametric curve 

$$
x=6 \cos {t},\,y=5 \sin {2 t},\,0\le t<2\pi,
$$

shown above, calculate the slope of the tangent to the curve at the point where $t=\frac{5 \pi}{3}.$

- $- \frac{5 \sqrt{2}}{3}$
- $- \frac{3}{5}$
- $- \frac{1}{2}$
- $- \frac{\sqrt{2}}{2}$
- $- \frac{5 \sqrt{3}}{9}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- 6 \sin {t},\,y'(t)=10 \cos {2 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(10 \cos {2 t}\right)}{\left(- 6 \sin {t}\right)} \\  & =- \frac{5 \cos {2 t}}{3 \sin {t}}.\end{aligned}
$$

Therefore, when $t=\frac{5 \pi}{3},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{5 \cos {2 \left(\frac{5 \pi}{3}\right)}}{3 \sin {\left(\frac{5 \pi}{3}\right)}} \\  & =- \frac{5 \left(- \frac{1}{2}\right)}{3 \left(- \frac{\sqrt{3}}{2}\right)} \\  & =- \frac{5 \sqrt{3}}{9}.\end{aligned}
$$

## Generated variant — harmonic_radio / observed-expression-pattern / observed_q-6808 / observed / seed 49

![](/home/jake/Developer/Course_Academy/generate/scratch/17592186083243/plots/curve-6ecbf0c8c84cbbdd6d77.png)

For the parametric curve 

$$
x=3 \cos {t},\,y=5 \sin {2 t},\,0\le t<2\pi,
$$

shown above, calculate the slope of the tangent to the curve at the point where $t=\frac{7 \pi}{4}.$

- $- \frac{10 \sqrt{2}}{3}$
- $- \frac{3}{10}$
- $0$
- $- \frac{5}{4}$
- $- \frac{5 \sqrt{2}}{4}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- 3 \sin {t},\,y'(t)=10 \cos {2 t}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(10 \cos {2 t}\right)}{\left(- 3 \sin {t}\right)} \\  & =- \frac{10 \cos {2 t}}{3 \sin {t}}.\end{aligned}
$$

Therefore, when $t=\frac{7 \pi}{4},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{10 \cos {2 \left(\frac{7 \pi}{4}\right)}}{3 \sin {\left(\frac{7 \pi}{4}\right)}} \\  & =- \frac{10 \left(0\right)}{3 \left(- \frac{\sqrt{2}}{2}\right)} \\  & =0.\end{aligned}
$$

## Generated variant — exp_root_radio / observed-expression-pattern / observed_q-20991 / observed / seed 37

For the parametric curve 

$$
x=\frac{1}{5 \sqrt{t}},\,y=\frac{e^{t}}{6 t},\,0<t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=6.$

- $\frac{5 \sqrt{6} e^{4}}{36}$
- $- \frac{25 \sqrt{6} e^{6}}{18}$
- $- \frac{5 \sqrt{7} e^{5}}{7}$
- $- \frac{25 \sqrt{3} e^{6}}{18}$
- $\frac{25 e^{6}}{6}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{1}{10 t^{\frac{3}{2}}},\,y'(t)=\frac{6 t e^{t} - 6 e^{t}}{36 t^{2}}=\frac{\left(t - 1\right) e^{t}}{6 t^{2}}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(t - 1\right) e^{t}}{6 t^{2}}\cdot \left(- 10 t^{\frac{3}{2}}\right) \\  & =- \frac{5 \left(t - 1\right) e^{t}}{3 \sqrt{t}}.\end{aligned}
$$

Therefore, when $t=6,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{5 \left(\left(6\right) - 1\right) e^{\left(6\right)}}{3 \sqrt{\left(6\right)}} \\  & =\frac{- 25 e^{6}}{3 \sqrt{6}} \\  & =- \frac{25 \sqrt{6} e^{6}}{18}.\end{aligned}
$$

## Generated variant — exp_root_radio / observed-expression-pattern / observed_q-20991 / observed / seed 49

For the parametric curve 

$$
x=\frac{1}{\sqrt{t}},\,y=\frac{e^{t}}{3 t},\,0<t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=5.$

- $- \frac{5 \sqrt{6} e^{4}}{18}$
- $- \frac{8 \sqrt{5} e^{5}}{15}$
- $\frac{\sqrt{5} e^{3}}{15}$
- $- \frac{2 \sqrt{2} e^{5}}{3}$
- $\frac{8 \sqrt{3} e^{5}}{9}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{1}{2 t^{\frac{3}{2}}},\,y'(t)=\frac{3 t e^{t} - 3 e^{t}}{9 t^{2}}=\frac{\left(t - 1\right) e^{t}}{3 t^{2}}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(t - 1\right) e^{t}}{3 t^{2}}\cdot \left(- 2 t^{\frac{3}{2}}\right) \\  & =- \frac{2 \left(t - 1\right) e^{t}}{3 \sqrt{t}}.\end{aligned}
$$

Therefore, when $t=5,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{2 \left(\left(5\right) - 1\right) e^{\left(5\right)}}{3 \sqrt{\left(5\right)}} \\  & =\frac{- 8 e^{5}}{3 \sqrt{5}} \\  & =- \frac{8 \sqrt{5} e^{5}}{15}.\end{aligned}
$$

## Generated variant — reciprocal_exp_root_radio / observed-expression-pattern / observed_q-15475 / observed / seed 37

For the parametric curve 

$$
x=e^{\frac{6}{t}},\,y=\frac{5}{\sqrt{t^{2} - 1}},\,1<t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=4.$

- $\frac{16}{15 e^{\frac{3}{2}}}$
- $\frac{8 \sqrt{15} e^{\frac{3}{2}}}{225}$
- $\frac{15 e^{\frac{3}{2}}}{16}$
- $\frac{32 \sqrt{15}}{135 e^{\frac{3}{2}}}$
- $\frac{15}{8 e^{\frac{3}{2}}}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{6 e^{\frac{6}{t}}}{t^{2}},\,y'(t)=- \frac{5 t}{\left(t^{2} - 1\right)^{\frac{3}{2}}}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- \frac{5 t}{\left(t^{2} - 1\right)^{\frac{3}{2}}}\right)}{\left(- \frac{6 e^{\frac{6}{t}}}{t^{2}}\right)} \\  & =\frac{5 t^{3} e^{- \frac{6}{t}}}{6 \left(t^{2} - 1\right)^{\frac{3}{2}}}.\end{aligned}
$$

Therefore, when $t=4,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{5 \left(4\right)^{3} e^{- \frac{6}{\left(4\right)}}}{6 \left(\left(4\right)^{2} - 1\right)^{\frac{3}{2}}} \\  & =\frac{320}{90 \sqrt{15} e^{\frac{3}{2}}} \\  & =\frac{32 \sqrt{15}}{135 e^{\frac{3}{2}}}.\end{aligned}
$$

## Generated variant — reciprocal_exp_root_radio / observed-expression-pattern / observed_q-15475 / observed / seed 49

For the parametric curve 

$$
x=e^{\frac{1}{t}},\,y=\frac{3}{\sqrt{t^{2} + 3}},\,0<t<\infty,
$$

calculate the slope of the tangent to the curve at the point where $t=2.$

- $\frac{2 \sqrt{14} e^{\frac{1}{2}}}{49}$
- $\frac{4}{7 e^{\frac{1}{2}}}$
- $\frac{7 \sqrt{2}}{4 e^{\frac{1}{2}}}$
- $\frac{24 \sqrt{7}}{49 e^{\frac{1}{2}}}$
- $\frac{7 e^{\frac{1}{2}}}{4}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
x'(t)=- \frac{e^{\frac{1}{t}}}{t^{2}},\,y'(t)=- \frac{3 t}{\left(t^{2} + 3\right)^{\frac{3}{2}}}.
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- \frac{3 t}{\left(t^{2} + 3\right)^{\frac{3}{2}}}\right)}{\left(- \frac{e^{\frac{1}{t}}}{t^{2}}\right)} \\  & =\frac{3 t^{3} e^{- \frac{1}{t}}}{\left(t^{2} + 3\right)^{\frac{3}{2}}}.\end{aligned}
$$

Therefore, when $t=2,$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =\frac{3 \left(2\right)^{3} e^{- \frac{1}{\left(2\right)}}}{\left(\left(2\right)^{2} + 3\right)^{\frac{3}{2}}} \\  & =\frac{24}{7 \sqrt{7} e^{\frac{1}{2}}} \\  & =\frac{24 \sqrt{7}}{49 e^{\frac{1}{2}}}.\end{aligned}
$$

## Generated variant — nested_trig_radio / observed-expression-pattern / observed_q-15476 / observed / seed 37

For the parametric curve 

$$
x=6 \sqrt{\sin{\left(e^{t} \right)}},\,y=5 \cot{\left(e^{t} \right)},\,-\infty<t<1,
$$

calculate the slope of the tangent to the curve at the point where $t=\ln{\left(\frac{\pi}{6} \right)}.$

- $- \frac{5 \sqrt{6}}{3}$
- $- \frac{5 \sqrt{6}}{9}$
- $- \frac{5 \sqrt{6}}{36}$
- $- \frac{20 \sqrt{6}}{9}$
- $- \frac{5 \sqrt{6}}{6}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
\begin{aligned}x'(t)&=\frac{6}{2 \sqrt{\sin{\left(e^{t} \right)}}}\cdot \cos{\left(e^{t} \right)}\cdot e^{t}\\ &= \frac{3 e^{t} \cos{\left(e^{t} \right)}}{\sqrt{\sin{\left(e^{t} \right)}}},\\ y'(t)&=- 5 e^{t} \csc^{2}{\left(e^{t} \right)}.\end{aligned}
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- 5 e^{t} \csc^{2}{\left(e^{t} \right)}\right)}{\left(\frac{3 e^{t} \cos{\left(e^{t} \right)}}{\sqrt{\sin{\left(e^{t} \right)}}}\right)} \\  & =\frac{- 10 \sqrt{\sin{\left(e^{t} \right)}}}{6 \sin^{2}{\left(e^{t} \right)} \cos{\left(e^{t} \right)}} \\  & =- \frac{5}{3 \sin^{\frac{3}{2}}{\left(e^{t} \right)} \cos{\left(e^{t} \right)}}.\end{aligned}
$$

Therefore, when $t=\ln{\left(\frac{\pi}{6} \right)},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{5}{3 \sin^{\frac{3}{2}}{\left(e^{\left(\ln{\left(\frac{\pi}{6} \right)}\right)} \right)} \cos{\left(e^{\left(\ln{\left(\frac{\pi}{6} \right)}\right)} \right)}} \\  & =- \frac{5}{3 \sin^{\frac{3}{2}}{\left(e^{\left(\ln{\left(\frac{\pi}{6} \right)}\right)} \right)} \left(\frac{\sqrt{3}}{2}\right)} \\  & =- \frac{20 \sqrt{6}}{9}.\end{aligned}
$$

## Generated variant — nested_trig_radio / observed-expression-pattern / observed_q-15476 / observed / seed 49

For the parametric curve 

$$
x=\sqrt{\sin{\left(e^{t} \right)}},\,y=3 \cot{\left(e^{t} \right)},\,-\infty<t<1,
$$

calculate the slope of the tangent to the curve at the point where $t=\ln{\left(\frac{5 \pi}{6} \right)}.$

- $2 \sqrt{6}$
- $3 \sqrt{6}$
- $6 \sqrt{6}$
- $\frac{\sqrt{6}}{2}$
- $8 \sqrt{6}$

We will use the formula

$$
\frac{dy}{dx}=\frac{y'(t)}{x'(t)}.
$$

Differentiating $x$ and $y,$ we get

$$
\begin{aligned}x'(t)&=\frac{1}{2 \sqrt{\sin{\left(e^{t} \right)}}}\cdot \cos{\left(e^{t} \right)}\cdot e^{t}\\ &= \frac{e^{t} \cos{\left(e^{t} \right)}}{2 \sqrt{\sin{\left(e^{t} \right)}}},\\ y'(t)&=- 3 e^{t} \csc^{2}{\left(e^{t} \right)}.\end{aligned}
$$

 

So we have

$$
\begin{aligned}\frac{dy}{dx} & =\frac{\left(- 3 e^{t} \csc^{2}{\left(e^{t} \right)}\right)}{\left(\frac{e^{t} \cos{\left(e^{t} \right)}}{2 \sqrt{\sin{\left(e^{t} \right)}}}\right)} \\  & =\frac{- 6 \sqrt{\sin{\left(e^{t} \right)}}}{\sin^{2}{\left(e^{t} \right)} \cos{\left(e^{t} \right)}} \\  & =- \frac{6}{\sin^{\frac{3}{2}}{\left(e^{t} \right)} \cos{\left(e^{t} \right)}}.\end{aligned}
$$

Therefore, when $t=\ln{\left(\frac{5 \pi}{6} \right)},$ the slope of the tangent to the curve is

$$
\begin{aligned}\frac{dy}{dx} & =- \frac{6}{\sin^{\frac{3}{2}}{\left(e^{\left(\ln{\left(\frac{5 \pi}{6} \right)}\right)} \right)} \cos{\left(e^{\left(\ln{\left(\frac{5 \pi}{6} \right)}\right)} \right)}} \\  & =- \frac{6}{\sin^{\frac{3}{2}}{\left(e^{\left(\ln{\left(\frac{5 \pi}{6} \right)}\right)} \right)} \left(- \frac{\sqrt{3}}{2}\right)} \\  & =8 \sqrt{6}.\end{aligned}
$$
