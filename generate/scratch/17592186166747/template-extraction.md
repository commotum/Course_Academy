# Four extraction stages

## 1. Specific source inventory

### exp_product: 17592186167326 (q-94587)

If $f(x, y) = xe^{xy}, x = t^{2}$, and $y = t$, compute $\frac{df}{dt}$.

Observed rating: absent. Independent variable: t. Exactly two coordinate functions. One five-choice radio field, complete derivative response.

Solution blocks: 0. Absent: normal solution is explicitly authored from the canonical full path rule.

### log_trig: 17592186167331 (q-95078)

If $f(x,y)=\operatorname{ln}⁡(x{y}^{2}),x=\operatorname{cos}⁡t$ and $y=\operatorname{sin}⁡t,$ compute $\frac{\text{d}f}{\text{d}t}$ for $0<t<\frac{\pi }{2}.$

Observed rating: {':db/ident': ':question.difficulty/easy'}. Independent variable: t. Exactly two coordinate functions. One five-choice radio field, complete derivative response.

Solution blocks: 5. formal chain rule, both partial derivatives, both substituted partials, both ordinary coordinate derivatives, ordered product and reduction chain.

The complete observed ordered mathematical blocks (including every internal equality) are preserved below:

```tex
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
```

```tex
\begin{aligned}\frac{∂f}{∂x}=\frac{{y}^{2}}{x{y}^{2}}=\frac{1}{x},\,\frac{∂f}{∂y}=\frac{2xy}{x{y}^{2}}=\frac{2}{y}\end{aligned}
```

```tex
\begin{aligned}\frac{∂f}{∂x} & =\frac{1}{\operatorname{cos}⁡t}, \\ \frac{∂f}{∂y} & =\frac{2}{\operatorname{sin}⁡t}.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}x}{\text{d}t}=-\operatorname{sin}⁡t,\,\frac{\text{d}y}{\text{d}t}=\operatorname{cos}⁡t.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =\frac{1}{\operatorname{cos}⁡t}\cdot (-\operatorname{sin}⁡t)+\frac{2}{\operatorname{sin}⁡t}\cdot \operatorname{cos}⁡t \\  & =-\frac{\operatorname{sin}⁡t}{\operatorname{cos}⁡t}+2\cdot \frac{\operatorname{cos}⁡t}{\operatorname{sin}⁡t} \\  & =2\operatorname{cot}⁡t-\operatorname{tan}⁡t.\end{aligned}
```

### trig_product: 17592186284666 (q-170668)

If $f(x,y)=\operatorname{sin}⁡x\operatorname{cos}⁡y,x={t}^{2},$ and $y=t,$ compute $\frac{\text{d}f}{\text{d}t}.$

Observed rating: {':db/ident': ':question.difficulty/easy'}. Independent variable: t. Exactly two coordinate functions. One five-choice radio field, complete derivative response.

Solution blocks: 5. formal chain rule, both partial derivatives, both substituted partials, both ordinary coordinate derivatives, ordered product and reduction chain.

The complete observed ordered mathematical blocks (including every internal equality) are preserved below:

```tex
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
```

```tex
\begin{aligned}\frac{∂f}{∂x}=\operatorname{cos}⁡x\operatorname{cos}⁡y,\,\frac{∂f}{∂y}=-\operatorname{sin}⁡x\operatorname{sin}⁡y\end{aligned}
```

```tex
\begin{aligned}\frac{∂f}{∂x} & =\operatorname{cos}⁡({t}^{2})\operatorname{cos}⁡(t), \\ \frac{∂f}{∂y} & =-\operatorname{sin}⁡({t}^{2})\operatorname{sin}⁡(t).\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}x}{\text{d}t}=2t,\,\frac{\text{d}y}{\text{d}t}=1.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =\operatorname{cos}⁡({t}^{2})\operatorname{cos}⁡(t)\cdot 2t+(-\operatorname{sin}⁡({t}^{2})\operatorname{sin}⁡(t))\cdot 1 \\  & =2t\operatorname{cos}⁡({t}^{2})\operatorname{cos}⁡(t)-\operatorname{sin}⁡({t}^{2})\operatorname{sin}⁡(t).\end{aligned}
```

### power_exp: 17592186360551 (q-95076)

If $f(x,y)={x}^{2}{e}^{y},x=2t$ and $y={t}^{2},$ compute $\frac{\text{d}f}{\text{d}t}.$

Observed rating: {':db/ident': ':question.difficulty/easy'}. Independent variable: t. Exactly two coordinate functions. One five-choice radio field, complete derivative response.

Solution blocks: 5. formal chain rule, both partial derivatives, both substituted partials, both ordinary coordinate derivatives, ordered product and reduction chain.

The complete observed ordered mathematical blocks (including every internal equality) are preserved below:

```tex
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
```

```tex
\begin{aligned}\frac{∂f}{∂x}=2x{e}^{y},\,\frac{∂f}{∂y}={x}^{2}{e}^{y}\end{aligned}
```

```tex
\begin{aligned}\frac{∂f}{∂x} & =2(2t){e}^{{t}^{2}}=4t{e}^{{t}^{2}}, \\ \frac{∂f}{∂y} & =(2t)^{2}{e}^{{t}^{2}}=4{t}^{2}{e}^{{t}^{2}}.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}x}{\text{d}t}=2,\,\frac{\text{d}y}{\text{d}t}=2t.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =4t{e}^{{t}^{2}}\cdot 2+4{t}^{2}{e}^{{t}^{2}}\cdot 2t \\  & =8t{e}^{{t}^{2}}+8{t}^{3}{e}^{{t}^{2}} \\  & =8t(1+{t}^{2}){e}^{{t}^{2}}.\end{aligned}
```

### root_log: 17592186360552 (q-95077)

If $f(x,y)=\sqrt{2xy},x=t$ and $y=\operatorname{ln}⁡t,$ compute $\frac{\text{d}f}{\text{d}t}.$

Observed rating: {':db/ident': ':question.difficulty/easy'}. Independent variable: t. Exactly two coordinate functions. One five-choice radio field, complete derivative response.

Solution blocks: 5. formal chain rule, both partial derivatives, both substituted partials, both ordinary coordinate derivatives, ordered product and reduction chain.

The complete observed ordered mathematical blocks (including every internal equality) are preserved below:

```tex
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
```

```tex
\begin{aligned}\frac{∂f}{∂x}=\frac{y}{\sqrt{2xy}},\,\frac{∂f}{∂y}=\frac{x}{\sqrt{2xy}}\end{aligned}
```

```tex
\begin{aligned}\frac{∂f}{∂x} & =\frac{\operatorname{ln}⁡t}{\sqrt{2t\operatorname{ln}⁡t}}, \\ \frac{∂f}{∂y} & =\frac{t}{\sqrt{2t\operatorname{ln}⁡t}}.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}x}{\text{d}t}=1,\,\frac{\text{d}y}{\text{d}t}=\frac{1}{t}.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =\frac{\operatorname{ln}⁡t}{\sqrt{2t\operatorname{ln}⁡t}}\cdot 1+\frac{t}{\sqrt{2t\operatorname{ln}⁡t}}\cdot \frac{1}{t} \\  & =\frac{\operatorname{ln}⁡t}{\sqrt{2t\operatorname{ln}⁡t}}+\frac{1}{\sqrt{2t\operatorname{ln}⁡t}} \\  & =\frac{1+\operatorname{ln}⁡t}{\sqrt{2t\operatorname{ln}⁡t}}.\end{aligned}
```

### linear_cos: 17592186360553 (q-95079)

If $f(x,y)=x\operatorname{cos}⁡y,x=4t$ and $y=t,$ compute $\frac{\text{d}f}{\text{d}t}.$

Observed rating: {':db/ident': ':question.difficulty/easy'}. Independent variable: t. Exactly two coordinate functions. One five-choice radio field, complete derivative response.

Solution blocks: 5. formal chain rule, both partial derivatives, both substituted partials, both ordinary coordinate derivatives, ordered product and reduction chain.

The complete observed ordered mathematical blocks (including every internal equality) are preserved below:

```tex
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
```

```tex
\begin{aligned}\frac{∂f}{∂x}=\operatorname{cos}⁡y,\,\frac{∂f}{∂y}=-x\operatorname{sin}⁡y\end{aligned}
```

```tex
\begin{aligned}\frac{∂f}{∂x} & =\operatorname{cos}⁡t \\ \frac{∂f}{∂y} & =-4t\operatorname{sin}⁡t.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}x}{\text{d}t}=4,\,\frac{\text{d}y}{\text{d}t}=1.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =\operatorname{cos}⁡t\cdot 4+(-4t\operatorname{sin}⁡t)\cdot 1 \\  & =4(\operatorname{cos}⁡t-t\operatorname{sin}⁡t).\end{aligned}
```

### exp_power: 17592186360554 (q-95080)

If $f(x,y)={e}^{x+2y},x={s}^{2},$ and $y=s,$ compute $\frac{\text{d}f}{\text{d}s}.$

Observed rating: {':db/ident': ':question.difficulty/easy'}. Independent variable: s. Exactly two coordinate functions. One five-choice radio field, complete derivative response.

Solution blocks: 5. formal chain rule, both partial derivatives, both substituted partials, both ordinary coordinate derivatives, ordered product and reduction chain.

The complete observed ordered mathematical blocks (including every internal equality) are preserved below:

```tex
\frac{\text{d}f}{\text{d}s}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}s}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}s}
```

```tex
\begin{aligned}\frac{∂f}{∂x}={e}^{x+2y},\,\frac{∂f}{∂y}=2{e}^{x+2y}\end{aligned}
```

```tex
\begin{aligned}\frac{∂f}{∂x} & ={e}^{{s}^{2}+2s}, \\ \frac{∂f}{∂y} & =2{e}^{{s}^{2}+2s}.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}x}{\text{d}s}=2s,\,\frac{\text{d}y}{\text{d}s}=1.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}f}{\text{d}s} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}s}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}s} \\  & ={e}^{{s}^{2}+2s}\cdot 2s+2{e}^{{s}^{2}+2s}\cdot 1 \\  & =2s{e}^{{s}^{2}+2s}+2{e}^{{s}^{2}+2s} \\  & =2(s+1){e}^{{s}^{2}+2s}.\end{aligned}
```

### linear_log: 17592186360555 (q-95081)

If $f(x,y)=y+x\operatorname{ln}⁡y,\,x=s$ and $y=2s,$ compute $\frac{\text{d}f}{\text{d}s}.$

Observed rating: {':db/ident': ':question.difficulty/easy'}. Independent variable: s. Exactly two coordinate functions. One five-choice radio field, complete derivative response.

Solution blocks: 5. formal chain rule, both partial derivatives, both substituted partials, both ordinary coordinate derivatives, ordered product and reduction chain.

The complete observed ordered mathematical blocks (including every internal equality) are preserved below:

```tex
\frac{\text{d}f}{\text{d}s}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}s}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}s}
```

```tex
\begin{aligned}\frac{∂f}{∂x}=\operatorname{ln}⁡y,\,\frac{∂f}{∂y}=1+\frac{x}{y}\end{aligned}
```

```tex
\begin{aligned}\frac{∂f}{∂x} & =\operatorname{ln}⁡2s, \\ \frac{∂f}{∂y} & =1+\frac{s}{2s}=\frac{3}{2}.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}x}{\text{d}s}=1,\,\frac{\text{d}y}{\text{d}s}=2.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}f}{\text{d}s} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}s}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}s} \\  & =\operatorname{ln}⁡2s\cdot 1+\frac{3}{2}\cdot 2 \\  & =3+\operatorname{ln}⁡2s.\end{aligned}
```

### trig_quotient: 17592186360556 (q-95084)

If $f(x,y)=\frac{x}{y},x=\operatorname{cos}⁡2s$ and $y=\operatorname{sin}⁡2s,$ compute $\frac{\text{d}f}{\text{d}s}.$

Observed rating: {':db/ident': ':question.difficulty/easy'}. Independent variable: s. Exactly two coordinate functions. One five-choice radio field, complete derivative response.

Solution blocks: 5. formal chain rule, both partial derivatives, both substituted partials, both ordinary coordinate derivatives, ordered product and reduction chain.

The complete observed ordered mathematical blocks (including every internal equality) are preserved below:

```tex
\frac{\text{d}f}{\text{d}s}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}s}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}s}
```

```tex
\begin{aligned}\frac{∂f}{∂x}=\frac{1}{y},\,\frac{∂f}{∂y}=-\frac{x}{{y}^{2}}\end{aligned}
```

```tex
\begin{aligned}\frac{∂f}{∂x} & =\frac{1}{\operatorname{sin}⁡2s}, \\ \frac{∂f}{∂y} & =-\frac{\operatorname{cos}⁡2s}{{sin}^{2}⁡2s}.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}x}{\text{d}s}=-2\operatorname{sin}⁡2s,\,\frac{\text{d}y}{\text{d}s}=2\operatorname{cos}⁡2s.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}f}{\text{d}s} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}s}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}s} \\  & =\frac{1}{\operatorname{sin}⁡2s}\cdot (-2\operatorname{sin}⁡2s)+(-\frac{\operatorname{cos}⁡2s}{{sin}^{2}⁡2s})\cdot 2\operatorname{cos}⁡2s \\  & =-2-2\cdot \frac{{cos}^{2}⁡2s}{{sin}^{2}⁡2s} \\  & =-2-2{cot}^{2}⁡2s \\  & =-2{csc}^{2}⁡2s.\end{aligned}
```

### rational_power: 17592186360557 (q-95085)

If $f(x,y)=\frac{x}{1+y},$ $x={s}^{2}$ and $y=s,$ compute $\frac{\text{d}f}{\text{d}s}.$

Observed rating: {':db/ident': ':question.difficulty/easy'}. Independent variable: s. Exactly two coordinate functions. One five-choice radio field, complete derivative response.

Solution blocks: 5. formal chain rule, both partial derivatives, both substituted partials, both ordinary coordinate derivatives, ordered product and reduction chain.

The complete observed ordered mathematical blocks (including every internal equality) are preserved below:

```tex
\frac{\text{d}f}{\text{d}s}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}s}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}s}
```

```tex
\begin{aligned}\frac{∂f}{∂x}=\frac{1}{1+y},\,\frac{∂f}{∂y}=-\frac{x}{(1+y)^{2}}\end{aligned}
```

```tex
\begin{aligned}\frac{∂f}{∂x} & =\frac{1}{1+s}, \\ \frac{∂f}{∂y} & =-\frac{{s}^{2}}{(1+s)^{2}}.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}x}{\text{d}s}=2s,\,\frac{\text{d}y}{\text{d}s}=1.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}f}{\text{d}s} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}s}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}s} \\  & =\frac{1}{1+s}\cdot 2s-\frac{{s}^{2}}{(1+s)^{2}}\cdot 1 \\  & =\frac{2s}{1+s}-\frac{{s}^{2}}{(1+s)^{2}} \\  & =\frac{2s(1+s)-{s}^{2}}{(1+s)^{2}} \\  & =\frac{s(2+s)}{(1+s)^{2}}.\end{aligned}
```

### exp_trig: 17592186383607 (q-170669)

If $f(x,y)={e}^{2y-x},x=\operatorname{cos}⁡t$ and $y=\operatorname{sin}⁡t,$ compute $\frac{\text{d}f}{\text{d}t}.$

Observed rating: {':db/ident': ':question.difficulty/easy'}. Independent variable: t. Exactly two coordinate functions. One five-choice radio field, complete derivative response.

Solution blocks: 5. formal chain rule, both partial derivatives, both substituted partials, both ordinary coordinate derivatives, ordered product and reduction chain.

The complete observed ordered mathematical blocks (including every internal equality) are preserved below:

```tex
\frac{\text{d}f}{\text{d}t}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t}
```

```tex
\begin{aligned}\frac{∂f}{∂x}=-{e}^{2y-x},\,\frac{∂f}{∂y}=2{e}^{2y-x}\end{aligned}
```

```tex
\begin{aligned}\frac{∂f}{∂x} & =-{e}^{2\operatorname{sin}⁡t-\operatorname{cos}⁡t}, \\ \frac{∂f}{∂y} & =2{e}^{2\operatorname{sin}⁡t-\operatorname{cos}⁡t}.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}x}{\text{d}t}=-\operatorname{sin}⁡t,\,\frac{\text{d}y}{\text{d}t}=\operatorname{cos}⁡t.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}f}{\text{d}t} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}t}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}t} \\  & =-{e}^{2\operatorname{sin}⁡t-\operatorname{cos}⁡t}\cdot (-\operatorname{sin}⁡t)+2{e}^{2\operatorname{sin}⁡t-\operatorname{cos}⁡t}\cdot \operatorname{cos}⁡t \\  & =(\operatorname{sin}⁡t+2\operatorname{cos}⁡t){e}^{2\operatorname{sin}⁡t-\operatorname{cos}⁡t}.\end{aligned}
```

### root_exp: 17592186385838 (q-95083)

If $f(x,y)=y{e}^{x},$ $x=\sqrt{s}$ and $y=s,$ compute $\frac{\text{d}f}{\text{d}s}$ for $s>0.$

Observed rating: {':db/ident': ':question.difficulty/easy'}. Independent variable: s. Exactly two coordinate functions. One five-choice radio field, complete derivative response.

Solution blocks: 5. formal chain rule, both partial derivatives, both substituted partials, both ordinary coordinate derivatives, ordered product and reduction chain.

The complete observed ordered mathematical blocks (including every internal equality) are preserved below:

```tex
\frac{\text{d}f}{\text{d}s}=\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}s}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}s}
```

```tex
\begin{aligned}\frac{∂f}{∂x}=y{e}^{x},\,\frac{∂f}{∂y}={e}^{x}\end{aligned}
```

```tex
\begin{aligned}\frac{∂f}{∂x} & =s{e}^{\sqrt{s}}, \\ \frac{∂f}{∂y} & ={e}^{\sqrt{s}}.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}x}{\text{d}s}=\frac{1}{2\sqrt{s}},\,\frac{\text{d}y}{\text{d}s}=1.\end{aligned}
```

```tex
\begin{aligned}\frac{\text{d}f}{\text{d}s} & =\frac{∂f}{∂x}\cdot \frac{\text{d}x}{\text{d}s}+\frac{∂f}{∂y}\cdot \frac{\text{d}y}{\text{d}s} \\  & =s{e}^{\sqrt{s}}\cdot \frac{1}{2\sqrt{s}}+{e}^{\sqrt{s}}\cdot 1 \\  & =\frac{\sqrt{s}}{2}{e}^{\sqrt{s}}+{e}^{\sqrt{s}} \\  & =(1+\frac{\sqrt{s}}{2}){e}^{\sqrt{s}}.\end{aligned}
```

## 2. Shared pattern

Compute df/dv=f_x dx/dv+f_y dy/dv with x=x(v),y=y(v). Observe the two partials in x,y, substitute BOTH coordinate maps into ALL arguments/products, independently differentiate the two maps, multiply each partial by its own derivative, add and perform the family-specific reduction. The outer functions differ in actual elementary derivative operations; they are not cosmetic function renamings.

## 3. Complete components and original banks

Every row below belongs to its original selection field. Its mathematical replay recipe is precisely the displayed source expression with v replaced by v+h at mathematical token slots; all other complete components remain as printed. Original h=0 reproduces the complete raw byte string via the same mask, not a source-answer lookup. This evidence-only parameterization preserves mathematical products and derivatives because d(v+h)/dv=1. It does not claim recovered distractor intention or contribute to substantive variety counts. Correct refs are exactly those captured; the one missing designation is separately inferred only in repaired evidence.

### exp_product: bank observed_raw / observed_repaired, field b9b1652d-93ab-5313-9296-f0aa0f63c08f

1. `837ffa1c-bea1-5c32-a487-a5e0c1fa8464`; correct designation=False; original value `(3t + 2t^{4})e^{t^{3}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

2. `f892b757-7eae-5c63-89c8-63741963fd61`; correct designation=False; original value `(2t + 3t^{4})e^{t^{3}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

3. `11856d3c-08b0-5dec-a86d-009e03dc99e4`; correct designation=False; original value `(2 + 3t^{3})e^{t^{2}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

4. `198e92a0-3964-5d71-ae13-52081c329e74`; correct designation=False; original value `(2 + t^{2})e^{t^{3}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

5. `761d1b61-36d9-5b0f-b98f-40748d738557`; correct designation=False; original value `(3t + 2t^{3})e^{t^{2}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

### log_trig: bank observed_raw / observed_repaired, field a955c8c5-959c-5957-86ce-5b5f4f04ba90

1. `7aa7cb58-130b-52e2-9ffc-cc9e52330663`; correct designation=False; original value `\operatorname{cot}⁡t+2\operatorname{csc}⁡t`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

2. `a1a9cb0c-c43b-5a83-8c67-e7c35f7eae70`; correct designation=False; original value `2\operatorname{csc}⁡t-\operatorname{tan}⁡t`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

3. `ea13c98f-b638-5d97-8167-fa566662cb6b`; correct designation=False; original value `2\operatorname{tan}⁡t-\operatorname{cot}⁡t`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

4. `ec49dc46-0ba5-5fda-b9c2-6bec956ac528`; correct designation=True; original value `2\operatorname{cot}⁡t-\operatorname{tan}⁡t`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

5. `f7162188-93f3-50e1-8684-87bec1a6cf00`; correct designation=False; original value `\operatorname{sec}⁡t-\operatorname{tan}⁡t`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

### trig_product: bank observed_raw / observed_repaired, field db0740db-ef2c-573e-a13f-6da541dd04e7

1. `546085f7-b447-560f-8e03-5f9f83d6f2d4`; correct designation=False; original value `{t}^{2}\operatorname{cos}⁡({t}^{2})\operatorname{cos}⁡(t)-t\operatorname{sin}⁡({t}^{2})`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

2. `74f33be1-f6b9-527c-9c36-b38596ce0f41`; correct designation=False; original value `\operatorname{cos}⁡({t}^{2})\operatorname{cos}⁡(t)-\operatorname{sin}⁡({t}^{2})\operatorname{sin}⁡(t)`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

3. `8d6ac22c-45ee-5e02-aa23-fa2d93a62a90`; correct designation=True; original value `2t\operatorname{cos}⁡({t}^{2})\operatorname{cos}⁡(t)-\operatorname{sin}⁡({t}^{2})\operatorname{sin}⁡(t)`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

4. `8d8a9385-1ddd-50d1-9fa6-1227b2a8f619`; correct designation=False; original value `-2t\operatorname{sin}⁡({t}^{2})\operatorname{cos}⁡(t)`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

5. `91107c67-4b51-563a-9b9f-7ec21682f202`; correct designation=False; original value `-2t\operatorname{cos}⁡({t}^{2})\operatorname{cos}⁡(t)`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

### power_exp: bank observed_raw / observed_repaired, field d9bfd21b-4c44-5c5c-ba56-5fadb4ae0273

1. `0906d5df-95ee-50f2-a42b-09e69555e339`; correct designation=False; original value `4t(1+2t){e}^{{t}^{2}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

2. `140ea72d-9a0d-57b5-b67c-2049bb317343`; correct designation=False; original value `2{t}^{2}(1+{t}^{2}){e}^{{t}^{2}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

3. `9cea513d-612f-5290-b731-384d792ca237`; correct designation=True; original value `8t(1+{t}^{2}){e}^{{t}^{2}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

4. `c0ba0846-4e92-5a2d-b302-7d756aa55faa`; correct designation=False; original value `8{t}^{3}(2+t){e}^{{t}^{2}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

5. `e95d1d3f-a370-59d0-97ce-9062ff9fd3d0`; correct designation=False; original value `4t(2+t){e}^{{t}^{2}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

### root_log: bank observed_raw / observed_repaired, field 146b2117-94cd-5963-92fa-afe7f73a78f1

1. `1830bf59-5084-598f-b1f6-81191dfbfbcf`; correct designation=False; original value `\frac{2+t}{\sqrt{t\operatorname{ln}⁡t}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

2. `26a1cc25-ba10-5462-a7f5-4b6c422818d1`; correct designation=False; original value `\frac{\operatorname{ln}⁡t}{\sqrt{2t\operatorname{ln}⁡t}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

3. `72ac5140-e75a-5b93-834e-7afad4225743`; correct designation=False; original value `\frac{1}{\sqrt{2\operatorname{ln}⁡t}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

4. `8cdd033a-0457-5b60-bc47-43fcb08320c4`; correct designation=False; original value `\frac{1+\sqrt{t}}{\sqrt{2\operatorname{ln}⁡t}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

5. `8ddb28d7-a49c-5dad-b528-bbf182a53bcb`; correct designation=True; original value `\frac{1+\operatorname{ln}⁡t}{\sqrt{2t\operatorname{ln}⁡t}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

### linear_cos: bank observed_raw / observed_repaired, field ee046ec2-08f8-5c58-bfb3-059a2ba841f7

1. `181e483e-0db4-5bd1-964b-afa6fc2ecf27`; correct designation=False; original value `\operatorname{sin}⁡t+4t\operatorname{cos}⁡t`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

2. `719dcb03-d975-5054-b48a-74dd57cccf20`; correct designation=True; original value `4(\operatorname{cos}⁡t-t\operatorname{sin}⁡t)`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

3. `76fada7e-bbdf-508e-9127-190df8ac22e6`; correct designation=False; original value `4(\operatorname{sin}⁡t-t\operatorname{cos}⁡t)`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

4. `81dec9c1-74ca-5c5c-9366-b27ffa80a962`; correct designation=False; original value `4(\operatorname{cos}⁡t+t\operatorname{sin}⁡t)`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

5. `c17c2336-706c-5cd5-8b88-2ef24b3288c9`; correct designation=False; original value `\operatorname{sin}⁡t-4t\operatorname{cos}⁡t`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

### exp_power: bank observed_raw / observed_repaired, field 1991f021-d4bd-5ba5-9a63-d5673c4d3078

1. `5774d438-8549-5c81-9843-45d115052cfc`; correct designation=False; original value `2s{e}^{{s}^{2}+2s}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

2. `63dc5334-1342-5ac0-8adc-34168c5ef7c5`; correct designation=False; original value `2(s+2){e}^{{s}^{2}+2s}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

3. `97245f20-2357-5a46-9419-5584f26e4952`; correct designation=True; original value `2(s+1){e}^{{s}^{2}+2s}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

4. `bc07b503-6a18-5c74-b532-0d144efdccab`; correct designation=False; original value `s(s+2){e}^{{s}^{2}+2s}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

5. `c201f1bf-9034-567f-9849-2029c4f2719a`; correct designation=False; original value `{s}^{2}{e}^{{s}^{2}+2s}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

### linear_log: bank observed_raw / observed_repaired, field ef608987-b651-5ccb-b9c8-ffdc510994e1

1. `46f944b8-e799-5036-80f1-5ba5c1a7411f`; correct designation=False; original value `\operatorname{ln}⁡2s`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

2. `82479d60-5437-50e5-882f-1cefac414e6e`; correct designation=True; original value `3+\operatorname{ln}⁡2s`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

3. `f1724fb0-eb83-58dc-8a3f-92689c7862c9`; correct designation=False; original value `3\operatorname{ln}⁡2s`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

4. `fe84e3ca-9757-54b8-a1da-085a92705bae`; correct designation=False; original value `\frac{3}{4}+\operatorname{ln}⁡2s`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

5. `fede68b1-836b-57e9-a83f-57bb56eb0c3a`; correct designation=False; original value `\frac{3}{2}+\operatorname{ln}⁡2s`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

### trig_quotient: bank observed_raw / observed_repaired, field ce0a50c8-6fe1-52e2-992d-16da1ca6ce29

1. `1b80e388-89f0-55d3-9647-29eb1e7d21a2`; correct designation=True; original value `-2{csc}^{2}⁡2s`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

2. `2931a144-34bf-5b91-9fd0-2c8561636d73`; correct designation=False; original value `\operatorname{tan}⁡2s+{csc}^{2}⁡2s`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

3. `5f982da7-fadd-5a18-83b3-b5af485d42fd`; correct designation=False; original value `\operatorname{cot}⁡2s`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

4. `981660b8-6d8e-5d6b-a353-cc9e60ac0aac`; correct designation=False; original value `\operatorname{tan}⁡2s`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

5. `d2b01e60-3c8a-5b80-ab36-ad8a68a5308f`; correct designation=False; original value `2{sec}^{2}⁡2s`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

### rational_power: bank observed_raw / observed_repaired, field 083d442a-f627-5528-9841-283282543ad1

1. `0cdc706a-1707-5c09-affb-248453b8b3de`; correct designation=False; original value `\frac{2+{s}^{2}}{1+s}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

2. `154db3be-7d69-5ebc-979b-f406345e0c58`; correct designation=False; original value `\frac{s(1-s)}{(1+s)^{2}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

3. `1cc9a21b-0849-5652-a19d-cd8b9c45a0a8`; correct designation=False; original value `\frac{{s}^{2}(2+s)}{(1+s)}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

4. `7cec9aba-8f27-55a0-917c-38e83d5f0aee`; correct designation=False; original value `\frac{1+{s}^{2}}{(1+s)^{2}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

5. `e28edfdb-62cd-569f-b9f0-d31cb58213f9`; correct designation=True; original value `\frac{s(2+s)}{(1+s)^{2}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

### exp_trig: bank observed_raw / observed_repaired, field 614acb07-1733-5745-addd-2f741b4bd7c1

1. `97cfef0b-b2e9-52d1-81b0-399192df2eb0`; correct designation=False; original value `{e}^{2\operatorname{sin}⁡t-\operatorname{cos}⁡t}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

2. `4bd4c4de-e1e5-5ff6-83aa-88f43410589b`; correct designation=True; original value `(\operatorname{sin}⁡t+2\operatorname{cos}⁡t){e}^{2\operatorname{sin}⁡t-\operatorname{cos}⁡t}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

3. `a4d046f0-8479-5ddd-8e29-9cf04c57ccd5`; correct designation=False; original value `(2\operatorname{sin}⁡t-\operatorname{cos}⁡t){e}^{2\operatorname{sin}⁡t-\operatorname{cos}⁡t}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

4. `6cf412ac-5ff2-5717-972e-75f25275ddc1`; correct designation=False; original value `(2\operatorname{sin}⁡t\operatorname{cos}⁡t+1){e}^{2\operatorname{sin}⁡t-\operatorname{cos}⁡t}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

5. `9e75a459-147f-5daa-8fd7-55841122ff55`; correct designation=False; original value `2{e}^{2\operatorname{sin}⁡t-\operatorname{cos}⁡t}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

### root_exp: bank observed_raw / observed_repaired, field 8f70704d-2718-514e-b670-1b5ed75416ae

1. `247ee7d0-904c-5d01-8297-06a98015037c`; correct designation=False; original value `(1+\frac{1}{\sqrt{s}}){e}^{\sqrt{s}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

2. `7cec0dc1-33bb-5f04-a034-05527df9b19d`; correct designation=False; original value `(1+s){e}^{\sqrt{s}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

3. `323b91bd-668a-507d-8f83-8a04b4f2b115`; correct designation=False; original value `(2+\sqrt{s}){e}^{\sqrt{s}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

4. `ffd6bb8a-7411-5765-b787-90052e6b40f0`; correct designation=False; original value `(1+\frac{1}{2\sqrt{s}}){e}^{\sqrt{s}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

5. `0fbb05f2-b967-534b-9feb-494c22d63500`; correct designation=True; original value `(1+\frac{\sqrt{s}}{2}){e}^{\sqrt{s}}`; recipe token-substitution $v\mapsto v+h$. Historical error operation **unresolved**, not promoted to normal generation.

## 4. Reusable normal templates, masks and guards

Normal shared prose is copied from each observed solution around its five mathematical blocks. Each block is regenerated as a complete mathematical component: formal path rule, ordered x/y partials (including logarithm numerator/denominator derivation), ordered substitutions (with explicit arithmetic equality for power_exp and linear_log), ordered x/y derivatives, formal path rule again then two multiplied contributions, optional source distribution, quotient common-denominator and trig identity stages, and conclusion. Families with three final rows retain three; the rational and trig quotient families retain five; the others retain four. Normal typography is standardized to valid TeX with \ln. The radical and quotient expressions retain their source operator forms. The authoritative MA JSON confirms q-94587 is a five-option multiple-choice widget; it does not supply the missing EDB correct designation/solution/rating, so these are not invented as observed attributes.

Default bank selection precedes parameters: one complete method-derived profile, [A+B, A, B, A-B, -(A+B)], with A=f_x(X,Y)X′, B=f_y(X,Y)Y′. The four wrong operations are omission of the second branch, omission of the first, subtraction of the second branch instead of addition, and reversal of the full derivative sign. All five values must be distinct; any collision rejects the WHOLE instance. There is no pooled choice replacement. The unchanged solution does not diagnose chosen errors.

Easy guard n=1–4,a=1–6,b=1–5, |h|,|k|≤3; equal angles for log_trig and a shared phase for trig_quotient. Default easy offsets zero. Moderate n,b=2–5 unequal,a=1–4,h=k=0. Hard n=2–3,a,b=1–3,nonzero signed h,k of magnitude≤3. All explicit calls share those guards. Log_trig lies in an open first-quadrant common-angle interval; root_log requires v+h>0 and b(v+k)>1; linear_log has v+k>0; root_exp has both shifted coordinates positive; rational denominators and sine quotient denominators are excluded from zero. Source domain omissions are left intact in raw evidence and minimally supplied in normal prompts.

Meaningful normal variety comes from source outer structures, independent coordinate powers/frequencies and non-cosmetic argument coefficients. All content identities include actual prompt, solution, level, complete displayed bank and correct designation; no seed, option order or parameter/profile aliases. The mathematical fingerprint canonicalizes the independent symbol, removes multiplicative output scaling and excludes banks. Source time-shift replay profiles are not used to inflate mathematical-task counts. Exhaustive default-domain enumeration in variety.py/variety.json gives easy **375 canonical mathematical tasks** from 765 nominal parameter combinations (741 presentation identities), moderate **48 tasks** from 48 combinations, and hard **636 tasks** from 648 combinations. Common independent-variable aliases, unchanged/unused parameters and multiplicative output scaling do not add tasks. The exponential-product fingerprint additionally canonicalizes its expanded exponent polynomial modulo an additive constant and its polynomial prefactor modulo leading output scale; the hard swapped-coordinate-scaling alias is explicitly tested. Individual easy families range from 5 linear-cosine tasks to 90 trig-product tasks; narrow family limits are reported rather than inflated. Default family coverage is explicitly checked across all twelve families.

## Source defects, repairs and limits

Direct decoded inspection of all 60 answer strings proves **zero** adjacent ord(92) pairs and **zero** literal six-character backslash-u2061 substrings. The function application marks are actual U+2061 characters and the source TeX commands have ordinary single backslashes. Source-errors.json records every ordinal prefix/count and asserts complete decoded capture/private-wrapper equality. The original capture is valid TeX; no escape repair is warranted. Both raw and repaired evidence profiles preserve these valid choice bytes. The repaired profile completes only the unrated missing attributes; the other eleven banks remain unchanged. All historical banks remain evidence-only because their wrong-operation intentions are opaque. Normal authored typography replaces operatorname/function application marks with conventional commands, a presentation convention rather than a defect correction. Missing q-94587 correct value is independently derived as (2t+3t^4)e^(t^3); its correct ref, easy level and five-block solution are additions counted separately from 11 captured designations/solutions. Normal source bank defaults are separately method-derived. No historical bank has been thrown away.
