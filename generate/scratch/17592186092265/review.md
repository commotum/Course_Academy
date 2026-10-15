# Original and two same-method variants per source family

## q-1948 — hard

### Captured original

Calculate $\frac{dy}{dx}$ for $y = \log_{2} (\sqrt{x})$.

[No worked solution captured.]

### Served original parameters

Calculate $\frac{\mathrm{d}y}{\mathrm{d}x}$ for $y=\log_{2}(\sqrt{x}).$

First, we express $y$ as the composite function

$$
y=\log_{2}(u),\quad u=\sqrt{x}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(2)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=\frac{1}{2\sqrt{x}}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(2)}\cdot (\frac{1}{2\sqrt{x}})\\ &=\frac{1}{(\sqrt{x})\ln(2)}\cdot (\frac{1}{2\sqrt{x}})\\ &=\frac{1}{2 x}\frac{1}{\ln(2)}.\end{aligned}
$$

### Variant 1

Calculate $\frac{\mathrm{d}y}{\mathrm{d}x}$ for $y=\log_{7}(\sqrt{- 5 x}).$

First, we express $y$ as the composite function

$$
y=\log_{7}(u),\quad u=\sqrt{- 5 x}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=\frac{-5}{2\sqrt{- 5 x}}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (\frac{-5}{2\sqrt{- 5 x}})\\ &=\frac{1}{(\sqrt{- 5 x})\ln(7)}\cdot (\frac{-5}{2\sqrt{- 5 x}})\\ &=\frac{1}{2 x}\frac{1}{\ln(7)}.\end{aligned}
$$

Parameters: `{"a": -5, "b": 7, "c": 0, "k": 0, "n": 1, "t": null}`

### Variant 2

Calculate $\frac{\mathrm{d}y}{\mathrm{d}x}$ for $y=\log_{9}(\sqrt{9 x}).$

First, we express $y$ as the composite function

$$
y=\log_{9}(u),\quad u=\sqrt{9 x}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(9)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=\frac{9}{2\sqrt{9 x}}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(9)}\cdot (\frac{9}{2\sqrt{9 x}})\\ &=\frac{1}{(\sqrt{9 x})\ln(9)}\cdot (\frac{9}{2\sqrt{9 x}})\\ &=\frac{1}{2 x}\frac{1}{\ln(9)}.\end{aligned}
$$

Parameters: `{"a": 9, "b": 9, "c": 0, "k": 0, "n": 1, "t": null}`

## q-48008 — easy

### Captured original

Calculate $\frac{dy}{dx}$ for $y = \log_{3} (5x - 2)$.

[No worked solution captured.]

### Served original parameters

Calculate $\frac{\mathrm{d}y}{\mathrm{d}x}$ for $y=\log_{3}(5 x - 2).$

First, we express $y$ as the composite function

$$
y=\log_{3}(u),\quad u=5 x - 2.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(3)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(3)}\cdot (5)\\ &=\frac{1}{(5 x - 2)\ln(3)}\cdot (5)\\ &=\frac{5}{5 x - 2}\frac{1}{\ln(3)}.\end{aligned}
$$

### Variant 1

Calculate $\frac{\mathrm{d}y}{\mathrm{d}x}$ for $y=\log_{7}(4 x - 7).$

First, we express $y$ as the composite function

$$
y=\log_{7}(u),\quad u=4 x - 7.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=4.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (4)\\ &=\frac{1}{(4 x - 7)\ln(7)}\cdot (4)\\ &=\frac{4}{4 x - 7}\frac{1}{\ln(7)}.\end{aligned}
$$

Parameters: `{"a": 4, "b": 7, "c": -7, "k": 0, "n": 1, "t": null}`

### Variant 2

Calculate $\frac{\mathrm{d}y}{\mathrm{d}x}$ for $y=\log(5 x - 3).$

First, we express $y$ as the composite function

$$
y=\log(u),\quad u=5 x - 3.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(10)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(10)}\cdot (5)\\ &=\frac{1}{(5 x - 3)\ln(10)}\cdot (5)\\ &=\frac{5}{5 x - 3}\frac{1}{\ln(10)}.\end{aligned}
$$

Parameters: `{"a": 5, "b": 10, "c": -3, "k": 0, "n": 1, "t": null}`

## q-1949 — easy

### Captured original

Find ${y}^{'}$ for $y={log}_{5}(5x).$

First, we express $y$ as the composite function

$$
y={log}_{5}(u),\,u=5x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{u\operatorname{ln}(5)},\,\frac{\text{d}u}{\text{d}x}=5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{u\operatorname{ln}(5)}\cdot 5 \\  & =\frac{1}{(5x)\operatorname{ln}(5)}\cdot 5 \\  & =\frac{\cancel{5}}{\cancel{5}x\operatorname{ln}(5)} \\  & =\frac{1}{x\operatorname{ln}(5)}.\end{aligned}
$$

### Served original parameters

Find $y'$ for $y=\log_{5}(5 x).$

$y'=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{5}(u),\quad u=5 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(5)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(5)}\cdot (5)\\ &=\frac{1}{(5 x)\ln(5)}\cdot (5)\\ &=\frac{\cancel{5}}{\cancel{5}x\ln(5)}\\ &=\frac{1}{x \ln{(5 )}}.\end{aligned}
$$

### Variant 1

Find $y'$ for $y=\log_{7}(- 5 x).$

$y'=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{7}(u),\quad u=- 5 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (-5)\\ &=\frac{1}{(- 5 x)\ln(7)}\cdot (-5)\\ &=\frac{\cancel{-5}}{\cancel{-5}x\ln(7)}\\ &=\frac{1}{x \ln{(7 )}}.\end{aligned}
$$

Parameters: `{"a": -5, "b": 7, "c": 0, "k": 0, "n": 1, "t": null}`

### Variant 2

Find $y'$ for $y=\log_{9}(9 x).$

$y'=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{9}(u),\quad u=9 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(9)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=9.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(9)}\cdot (9)\\ &=\frac{1}{(9 x)\ln(9)}\cdot (9)\\ &=\frac{\cancel{9}}{\cancel{9}x\ln(9)}\\ &=\frac{1}{x \ln{(9 )}}.\end{aligned}
$$

Parameters: `{"a": 9, "b": 9, "c": 0, "k": 0, "n": 1, "t": null}`

## q-310148 — easy

### Captured original

Given that $f(x)={log}_{5}(7-6x),$ find ${f}^{'}(x).$

${f}^{'}(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
{f}^{'}(x)={log}_{5}(u),\,u=7-6x.
$$

Differentiating gives 

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u\operatorname{ln}(5)},\,\frac{\text{d}u}{\text{d}x}=-6.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{u\operatorname{ln}(5)}\cdot (-6) \\  & =\frac{1}{(7-6x)\operatorname{ln}(5)}\cdot (-6) \\  & =\frac{6}{(6x-7)\operatorname{ln}(5)}.\end{aligned}
$$

### Served original parameters

Given that $f(x)=\log_{5}(7 - 6 x),$ find $f'(x)$.

$f'(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
f(x)=\log_{5}(u),\quad u=7 - 6 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}f}{\mathrm{d}u}=\frac{1}{u\ln(5)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-6.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}f}{\mathrm{d}x} &=\frac{\mathrm{d}f}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(5)}\cdot (-6)\\ &=\frac{1}{(7 - 6 x)\ln(5)}\cdot (-6)\\ &=- \frac{6}{7 - 6 x}\frac{1}{\ln(5)}.\end{aligned}
$$

### Variant 1

Given that $f(x)=\log_{7}(- 5 x),$ find $f'(x)$.

$f'(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
f(x)=\log_{7}(u),\quad u=- 5 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}f}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}f}{\mathrm{d}x} &=\frac{\mathrm{d}f}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (-5)\\ &=\frac{1}{(- 5 x)\ln(7)}\cdot (-5)\\ &=\frac{1}{x}\frac{1}{\ln(7)}.\end{aligned}
$$

Parameters: `{"a": -5, "b": 7, "c": 0, "k": 0, "n": 1, "t": null}`

### Variant 2

Given that $f(x)=\log_{9}(9 x + 12),$ find $f'(x)$.

$f'(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
f(x)=\log_{9}(u),\quad u=9 x + 12.
$$

Differentiating gives

$$
\frac{\mathrm{d}f}{\mathrm{d}u}=\frac{1}{u\ln(9)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=9.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}f}{\mathrm{d}x} &=\frac{\mathrm{d}f}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(9)}\cdot (9)\\ &=\frac{1}{(9 x + 12)\ln(9)}\cdot (9)\\ &=\frac{9}{9 x + 12}\frac{1}{\ln(9)}.\end{aligned}
$$

Parameters: `{"a": 9, "b": 9, "c": 12, "k": 0, "n": 1, "t": null}`

## q-341686 — easy

### Captured original

Given that $f(x)={log}_{7}(4x-9),$ find ${f}^{'}(x).$

${f}^{'}(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
{f}^{'}(x)={log}_{7}(u),\,u=4x-9.
$$

Differentiating gives 

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u\operatorname{ln}(7)},\,\frac{\text{d}u}{\text{d}x}=4.
$$

We now apply the chain rule, and get 

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{u\operatorname{ln}(7)}\cdot 4 \\  & =\frac{1}{(4x-9)\operatorname{ln}(7)}\cdot 4 \\  & =\frac{4}{(4x-9)\operatorname{ln}(7)}.\end{aligned}
$$

### Served original parameters

Given that $f(x)=\log_{7}(4 x - 9),$ find $f'(x)$.

$f'(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
f(x)=\log_{7}(u),\quad u=4 x - 9.
$$

Differentiating gives

$$
\frac{\mathrm{d}f}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=4.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}f}{\mathrm{d}x} &=\frac{\mathrm{d}f}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (4)\\ &=\frac{1}{(4 x - 9)\ln(7)}\cdot (4)\\ &=\frac{4}{4 x - 9}\frac{1}{\ln(7)}.\end{aligned}
$$

### Variant 1

Given that $f(x)=\log_{7}(- 5 x),$ find $f'(x)$.

$f'(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
f(x)=\log_{7}(u),\quad u=- 5 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}f}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}f}{\mathrm{d}x} &=\frac{\mathrm{d}f}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (-5)\\ &=\frac{1}{(- 5 x)\ln(7)}\cdot (-5)\\ &=\frac{1}{x}\frac{1}{\ln(7)}.\end{aligned}
$$

Parameters: `{"a": -5, "b": 7, "c": 0, "k": 0, "n": 1, "t": null}`

### Variant 2

Given that $f(x)=\log_{9}(9 x + 12),$ find $f'(x)$.

$f'(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
f(x)=\log_{9}(u),\quad u=9 x + 12.
$$

Differentiating gives

$$
\frac{\mathrm{d}f}{\mathrm{d}u}=\frac{1}{u\ln(9)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=9.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}f}{\mathrm{d}x} &=\frac{\mathrm{d}f}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(9)}\cdot (9)\\ &=\frac{1}{(9 x + 12)\ln(9)}\cdot (9)\\ &=\frac{9}{9 x + 12}\frac{1}{\ln(9)}.\end{aligned}
$$

Parameters: `{"a": 9, "b": 9, "c": 12, "k": 0, "n": 1, "t": null}`

## q-341688 — easy

### Captured original

Given that $f(x)=\operatorname{log}(8x),$ find ${f}^{'}(x).$

${f}^{'}(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
{f}^{'}(x)=\operatorname{log}(u),\,u=8x.
$$

Differentiating gives 

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u\operatorname{ln}(10)},\,\frac{\text{d}u}{\text{d}x}=8.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{u\operatorname{ln}(10)}\cdot 8 \\  & =\frac{8}{8x\operatorname{ln}(10)} \\  & =\frac{\cancel{8}}{\cancel{8}x\operatorname{ln}(10)} \\  & =\frac{1}{x\operatorname{ln}(10)}.\end{aligned}
$$

### Served original parameters

Given that $f(x)=\log(8 x),$ find $f'(x)$.

$f'(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
f(x)=\log(u),\quad u=8 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}f}{\mathrm{d}u}=\frac{1}{u\ln(10)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=8.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}f}{\mathrm{d}x} &=\frac{\mathrm{d}f}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(10)}\cdot (8)\\ &=\frac{8}{(8 x)\ln(10)}\\ &=\frac{\cancel{8}}{\cancel{8}x\ln(10)}\\ &=\frac{1}{x \ln{(10 )}}.\end{aligned}
$$

### Variant 1

Given that $f(x)=\log_{7}(- 5 x),$ find $f'(x)$.

$f'(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
f(x)=\log_{7}(u),\quad u=- 5 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}f}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}f}{\mathrm{d}x} &=\frac{\mathrm{d}f}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (-5)\\ &=\frac{-5}{(- 5 x)\ln(7)}\\ &=\frac{\cancel{-5}}{\cancel{-5}x\ln(7)}\\ &=\frac{1}{x \ln{(7 )}}.\end{aligned}
$$

Parameters: `{"a": -5, "b": 7, "c": 0, "k": 0, "n": 1, "t": null}`

### Variant 2

Given that $f(x)=\log_{9}(9 x),$ find $f'(x)$.

$f'(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
f(x)=\log_{9}(u),\quad u=9 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}f}{\mathrm{d}u}=\frac{1}{u\ln(9)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=9.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}f}{\mathrm{d}x} &=\frac{\mathrm{d}f}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(9)}\cdot (9)\\ &=\frac{9}{(9 x)\ln(9)}\\ &=\frac{\cancel{9}}{\cancel{9}x\ln(9)}\\ &=\frac{1}{x \ln{(9 )}}.\end{aligned}
$$

Parameters: `{"a": 9, "b": 9, "c": 0, "k": 0, "n": 1, "t": null}`

## q-48001 — easy

### Captured original

Find ${f}^{'}(x)$ for $f(x)={log}_{2}(3-2x).$

First, we express $f(x)$ as the composite function

$$
{f}^{'}(x)={log}_{2}(u),\,u=3-2x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u\operatorname{ln}(2)},\,\frac{\text{d}u}{\text{d}x}=-2.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{u\operatorname{ln}(2)}\cdot (-2) \\  & =\frac{1}{(3-2x)\operatorname{ln}(2)}\cdot (-2) \\  & =-\frac{2}{(3-2x)\operatorname{ln}(2)}.\end{aligned}
$$

### Served original parameters

Find $f'(x)$ for $f(x)=\log_{2}(3 - 2 x).$

$f'(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
f(x)=\log_{2}(u),\quad u=3 - 2 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}f}{\mathrm{d}u}=\frac{1}{u\ln(2)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-2.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}f}{\mathrm{d}x} &=\frac{\mathrm{d}f}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(2)}\cdot (-2)\\ &=\frac{1}{(3 - 2 x)\ln(2)}\cdot (-2)\\ &=- \frac{2}{3 - 2 x}\frac{1}{\ln(2)}.\end{aligned}
$$

### Variant 1

Find $f'(x)$ for $f(x)=\log_{7}(- 5 x).$

$f'(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
f(x)=\log_{7}(u),\quad u=- 5 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}f}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}f}{\mathrm{d}x} &=\frac{\mathrm{d}f}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (-5)\\ &=\frac{1}{(- 5 x)\ln(7)}\cdot (-5)\\ &=\frac{1}{x}\frac{1}{\ln(7)}.\end{aligned}
$$

Parameters: `{"a": -5, "b": 7, "c": 0, "k": 0, "n": 1, "t": null}`

### Variant 2

Find $f'(x)$ for $f(x)=\log_{9}(9 x + 12).$

$f'(x)=$
{{field-1}}

First, we express $f(x)$ as the composite function

$$
f(x)=\log_{9}(u),\quad u=9 x + 12.
$$

Differentiating gives

$$
\frac{\mathrm{d}f}{\mathrm{d}u}=\frac{1}{u\ln(9)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=9.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}f}{\mathrm{d}x} &=\frac{\mathrm{d}f}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(9)}\cdot (9)\\ &=\frac{1}{(9 x + 12)\ln(9)}\cdot (9)\\ &=\frac{9}{9 x + 12}\frac{1}{\ln(9)}.\end{aligned}
$$

Parameters: `{"a": 9, "b": 9, "c": 12, "k": 0, "n": 1, "t": null}`

## q-71479 — easy

### Captured original

Find ${y}^{'}$ for $y={log}_{4}(2-5x).$

First, we express $y$ as the composite function

$$
y={log}_{4}(u),\,u=2-5x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{u\operatorname{ln}(4)},\,\frac{\text{d}u}{\text{d}x}=-5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{u\operatorname{ln}(4)}\cdot (-5) \\  & =\frac{1}{(2-5x)\operatorname{ln}(4)}\cdot (-5) \\  & =-\frac{5}{(2-5x)\operatorname{ln}(4)}.\end{aligned}
$$

### Served original parameters

Find $y'$ for $y=\log_{4}(2 - 5 x).$

$y'=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{4}(u),\quad u=2 - 5 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(4)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(4)}\cdot (-5)\\ &=\frac{1}{(2 - 5 x)\ln(4)}\cdot (-5)\\ &=- \frac{5}{2 - 5 x}\frac{1}{\ln(4)}.\end{aligned}
$$

### Variant 1

Find $y'$ for $y=\log_{7}(- 5 x).$

$y'=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{7}(u),\quad u=- 5 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (-5)\\ &=\frac{1}{(- 5 x)\ln(7)}\cdot (-5)\\ &=\frac{1}{x}\frac{1}{\ln(7)}.\end{aligned}
$$

Parameters: `{"a": -5, "b": 7, "c": 0, "k": 0, "n": 1, "t": null}`

### Variant 2

Find $y'$ for $y=\log_{9}(9 x + 12).$

$y'=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{9}(u),\quad u=9 x + 12.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(9)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=9.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(9)}\cdot (9)\\ &=\frac{1}{(9 x + 12)\ln(9)}\cdot (9)\\ &=\frac{9}{9 x + 12}\frac{1}{\ln(9)}.\end{aligned}
$$

Parameters: `{"a": 9, "b": 9, "c": 12, "k": 0, "n": 1, "t": null}`

## q-310145 — moderate

### Captured original

Find the slope $m$ of the tangent to the curve $y={log}_{4}⁡(6x-2)+7$ at the point where $x=1.$

$m=$
{{field-1}}

First, we express $y$ as the composite function

$$
y={log}_{4}⁡(u)+7,\,u=6x-2.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{uln⁡(4)},\,\frac{\text{d}u}{\text{d}x}=6.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{uln⁡(4)}\cdot 6 \\  & =\frac{1}{(6x-2)ln⁡(4)}\cdot 6 \\  & =\frac{6}{(6x-2)ln⁡(4)} \\  & =\frac{3}{(3x-1)ln⁡(4)}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=1$ is 

$$
\begin{aligned}\begin{aligned}m=\frac{\text{d}y}{\text{d}x}{|}_{x=1} & =\frac{3}{(3x-1)ln⁡(4)}{|}_{x=1} \\  & =\frac{3}{(3(1)-1)ln⁡(4)} \\  & =\frac{3}{2ln⁡(4)}.\end{aligned}\end{aligned}
$$

### Served original parameters

Find the slope $m$ of the tangent to the curve $y=\log_{4}(6 x - 2)+7$ at the point where $x=1.$

$m=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{4}(u)+7,\quad u=6 x - 2.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(4)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=6.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(4)}\cdot (6)\\ &=\frac{1}{(6 x - 2)\ln(4)}\cdot (6)\\ &=\frac{6}{6 x - 2}\frac{1}{\ln(4)}\\ &=\frac{3}{(3 x - 1) \ln{(4 )}}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=1$ is

$$
\begin{aligned}m=\frac{\mathrm{d}y}{\mathrm{d}x}\big|_{x=1} &=\left.(\frac{3}{(3 x - 1) \ln{(4 )}})\right|_{x=1}\\ &=\frac{3}{(3 (1) - 1) \ln{(4 )}}\\ &=\frac{3}{4 \ln{(2 )}}.\end{aligned}
$$

### Variant 1

Find the slope $m$ of the tangent to the curve $y=\log_{7}(- 8 x - 10)+8$ at the point where $x=- \frac{31}{24}.$

$m=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{7}(u)+8,\quad u=- 8 x - 10.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-8.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (-8)\\ &=\frac{1}{(- 8 x - 10)\ln(7)}\cdot (-8)\\ &=- \frac{8}{- 8 x - 10}\frac{1}{\ln(7)}\\ &=\frac{4}{(4 x + 5) \ln{(7 )}}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=- \frac{31}{24}$ is

$$
\begin{aligned}m=\frac{\mathrm{d}y}{\mathrm{d}x}\big|_{x=- \frac{31}{24}} &=\left.(\frac{4}{(4 x + 5) \ln{(7 )}})\right|_{x=- \frac{31}{24}}\\ &=\frac{4}{(4 (- \frac{31}{24}) + 5) \ln{(7 )}}\\ &=- \frac{24}{\ln{(7 )}}.\end{aligned}
$$

Parameters: `{"a": -8, "b": 7, "c": -10, "k": 8, "n": 1, "t": "-31/24"}`

### Variant 2

Find the slope $m$ of the tangent to the curve $y=\log_{9}(8 x + 2)+7$ at the point where $x=\frac{1}{16}.$

$m=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{9}(u)+7,\quad u=8 x + 2.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(9)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=8.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(9)}\cdot (8)\\ &=\frac{1}{(8 x + 2)\ln(9)}\cdot (8)\\ &=\frac{8}{8 x + 2}\frac{1}{\ln(9)}\\ &=\frac{4}{(4 x + 1) \ln{(9 )}}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=\frac{1}{16}$ is

$$
\begin{aligned}m=\frac{\mathrm{d}y}{\mathrm{d}x}\big|_{x=\frac{1}{16}} &=\left.(\frac{4}{(4 x + 1) \ln{(9 )}})\right|_{x=\frac{1}{16}}\\ &=\frac{4}{(4 (\frac{1}{16}) + 1) \ln{(9 )}}\\ &=\frac{8}{5 \ln{(3 )}}.\end{aligned}
$$

Parameters: `{"a": 8, "b": 9, "c": 2, "k": 7, "n": 1, "t": "1/16"}`

## q-310149 — moderate

### Captured original

Given that $y=log⁡({x}^{5}-2),$ find $\frac{\text{d}y}{\text{d}x}$ in terms of $x.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=log⁡(u),\,u={x}^{5}-2.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{uln⁡(10)},\,\frac{\text{d}u}{\text{d}x}=5{x}^{4}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{uln⁡(10)}\cdot 5{x}^{4} \\  & =\frac{5{x}^{4}}{({x}^{5}-2)ln⁡(10)}.\end{aligned}
$$

### Served original parameters

Given that $y=\log(x^{5} - 2),$ find $\frac{\mathrm{d}y}{\mathrm{d}x}$ in terms of $x.$

$\frac{\mathrm{d}y}{\mathrm{d}x}=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log(u),\quad u=x^{5} - 2.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(10)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=5 x^{4}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(10)}\cdot (5 x^{4})\\ &=5 x^{4}\frac{1}{(x^{5} - 2)\ln(10)}.\end{aligned}
$$

### Variant 1

Given that $y=\log_{7}(x^{3} + 1),$ find $\frac{\mathrm{d}y}{\mathrm{d}x}$ in terms of $x.$

$\frac{\mathrm{d}y}{\mathrm{d}x}=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{7}(u),\quad u=x^{3} + 1.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=3 x^{2}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (3 x^{2})\\ &=3 x^{2}\frac{1}{(x^{3} + 1)\ln(7)}.\end{aligned}
$$

Parameters: `{"a": 1, "b": 7, "c": 1, "k": 0, "n": 3, "t": null}`

### Variant 2

Given that $y=\log_{9}(x^{6} + 2),$ find $\frac{\mathrm{d}y}{\mathrm{d}x}$ in terms of $x.$

$\frac{\mathrm{d}y}{\mathrm{d}x}=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{9}(u),\quad u=x^{6} + 2.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(9)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=6 x^{5}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(9)}\cdot (6 x^{5})\\ &=6 x^{5}\frac{1}{(x^{6} + 2)\ln(9)}.\end{aligned}
$$

Parameters: `{"a": 1, "b": 9, "c": 2, "k": 0, "n": 6, "t": null}`

## q-341691 — moderate

### Captured original

Given that $y={log}_{6}⁡(-3{x}^{3}),$ find $\frac{\text{d}y}{\text{d}x}$ in terms of $x.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

First, we express $y$ as the composite function

$$
y={log}_{6}⁡(u),\,u=-3{x}^{3}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{uln⁡(6)},\,\frac{\text{d}u}{\text{d}x}=-9{x}^{2}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{uln⁡(6)}\cdot (-9{x}^{2}) \\  & =\frac{-9{x}^{2}}{-3{x}^{3}ln⁡(6)} \\  & =\frac{\cancel{-3{x}^{2}}\cdot 3}{\cancel{-3{x}^{2}}\cdot xln⁡(6)} \\  & =\frac{3}{xln⁡(6)}.\end{aligned}
$$

### Served original parameters

Given that $y=\log_{6}(- 3 x^{3}),$ find $\frac{\mathrm{d}y}{\mathrm{d}x}$ in terms of $x.$

$\frac{\mathrm{d}y}{\mathrm{d}x}=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{6}(u),\quad u=- 3 x^{3}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(6)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=- 9 x^{2}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(6)}\cdot (- 9 x^{2})\\ &=\frac{- 9 x^{2}}{(- 3 x^{3})\ln(6)}\\ &=\frac{\cancel{- 3 x^{2}}\cdot 3}{\cancel{- 3 x^{2}}\cdot x\ln(6)}\\ &=\frac{3}{x \ln{(6 )}}.\end{aligned}
$$

### Variant 1

Given that $y=\log_{7}(2 x^{3}),$ find $\frac{\mathrm{d}y}{\mathrm{d}x}$ in terms of $x.$

$\frac{\mathrm{d}y}{\mathrm{d}x}=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{7}(u),\quad u=2 x^{3}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=6 x^{2}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (6 x^{2})\\ &=\frac{6 x^{2}}{(2 x^{3})\ln(7)}\\ &=\frac{\cancel{2 x^{2}}\cdot 3}{\cancel{2 x^{2}}\cdot x\ln(7)}\\ &=\frac{3}{x \ln{(7 )}}.\end{aligned}
$$

Parameters: `{"a": 2, "b": 7, "c": 0, "k": 0, "n": 3, "t": null}`

### Variant 2

Given that $y=\log_{9}(3 x^{6}),$ find $\frac{\mathrm{d}y}{\mathrm{d}x}$ in terms of $x.$

$\frac{\mathrm{d}y}{\mathrm{d}x}=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{9}(u),\quad u=3 x^{6}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(9)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=18 x^{5}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(9)}\cdot (18 x^{5})\\ &=\frac{18 x^{5}}{(3 x^{6})\ln(9)}\\ &=\frac{\cancel{3 x^{5}}\cdot 6}{\cancel{3 x^{5}}\cdot x\ln(9)}\\ &=\frac{6}{x \ln{(9 )}}.\end{aligned}
$$

Parameters: `{"a": 3, "b": 9, "c": 0, "k": 0, "n": 6, "t": null}`

## q-341694 — hard

### Captured original

Given that $y={log}_{4}⁡(\sqrt{7x}),$ find $\frac{\text{d}y}{\text{d}x}$  in terms of $x.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

First, we express $y$ as the composite function

$$
y={log}_{4}⁡(u),\,u=\sqrt{7x}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{uln⁡(4)},\,\frac{\text{d}u}{\text{d}x}=\frac{7}{2\sqrt{7x}}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{uln⁡(4)}\cdot \frac{7}{2\sqrt{7x}} \\  & =\frac{1}{\sqrt{7x}ln⁡(4)}\cdot \frac{7}{2\sqrt{7x}} \\  & =\frac{7}{2\cdot 7xln⁡(4)} \\  & =\frac{\cancel{7}}{2\cdot \cancel{7}xln⁡(4)} \\  & =\frac{1}{2xln⁡(4)}.\end{aligned}
$$

### Served original parameters

Given that $y=\log_{4}(\sqrt{7 x}),$ find $\frac{\mathrm{d}y}{\mathrm{d}x}$ in terms of $x.$

$\frac{\mathrm{d}y}{\mathrm{d}x}=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{4}(u),\quad u=\sqrt{7 x}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(4)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=\frac{7}{2\sqrt{7 x}}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(4)}\cdot (\frac{7}{2\sqrt{7 x}})\\ &=\frac{1}{(\sqrt{7 x})\ln(4)}\cdot (\frac{7}{2\sqrt{7 x}})\\ &=\frac{7}{2(7 x)\ln(4)}\\ &=\frac{\cancel{7}}{2\cdot \cancel{7}x\ln(4)}\\ &=\frac{1}{2 x \ln{(4 )}}.\end{aligned}
$$

### Variant 1

Given that $y=\log_{7}(\sqrt{- 5 x}),$ find $\frac{\mathrm{d}y}{\mathrm{d}x}$ in terms of $x.$

$\frac{\mathrm{d}y}{\mathrm{d}x}=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{7}(u),\quad u=\sqrt{- 5 x}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=\frac{-5}{2\sqrt{- 5 x}}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (\frac{-5}{2\sqrt{- 5 x}})\\ &=\frac{1}{(\sqrt{- 5 x})\ln(7)}\cdot (\frac{-5}{2\sqrt{- 5 x}})\\ &=\frac{-5}{2(- 5 x)\ln(7)}\\ &=\frac{\cancel{-5}}{2\cdot \cancel{-5}x\ln(7)}\\ &=\frac{1}{2 x \ln{(7 )}}.\end{aligned}
$$

Parameters: `{"a": -5, "b": 7, "c": 0, "k": 0, "n": 1, "t": null}`

### Variant 2

Given that $y=\log_{9}(\sqrt{9 x}),$ find $\frac{\mathrm{d}y}{\mathrm{d}x}$ in terms of $x.$

$\frac{\mathrm{d}y}{\mathrm{d}x}=$
{{field-1}}

First, we express $y$ as the composite function

$$
y=\log_{9}(u),\quad u=\sqrt{9 x}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(9)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=\frac{9}{2\sqrt{9 x}}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(9)}\cdot (\frac{9}{2\sqrt{9 x}})\\ &=\frac{1}{(\sqrt{9 x})\ln(9)}\cdot (\frac{9}{2\sqrt{9 x}})\\ &=\frac{9}{2(9 x)\ln(9)}\\ &=\frac{\cancel{9}}{2\cdot \cancel{9}x\ln(9)}\\ &=\frac{1}{2 x \ln{(9 )}}.\end{aligned}
$$

Parameters: `{"a": 9, "b": 9, "c": 0, "k": 0, "n": 1, "t": null}`

## q-48559 — moderate

### Captured original

Given that $y={log}_{2}⁡({x}^{3}),$ find $\frac{\text{d}y}{\text{d}x}.$

First, we express $y$ as the composite function

$$
y={log}_{2}⁡(u),\,u={x}^{3}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{uln⁡(2)},\,\frac{\text{d}u}{\text{d}x}=3{x}^{2}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{uln⁡(2)}\cdot 3{x}^{2} \\  & =\frac{3{x}^{2}}{{x}^{3}ln⁡(2)} \\  & =\frac{\cancel{{x}^{2}}\cdot 3}{\cancel{{x}^{2}}\cdot xln⁡(2)} \\  & =\frac{3}{xln⁡(2)}.\end{aligned}
$$

### Served original parameters

Given that $y=\log_{2}(x^{3}),$ find $\frac{\mathrm{d}y}{\mathrm{d}x}$.

First, we express $y$ as the composite function

$$
y=\log_{2}(u),\quad u=x^{3}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(2)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=3 x^{2}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(2)}\cdot (3 x^{2})\\ &=\frac{3 x^{2}}{(x^{3})\ln(2)}\\ &=\frac{\cancel{x^{2}}\cdot 3}{\cancel{x^{2}}\cdot x\ln(2)}\\ &=\frac{3}{x \ln{(2 )}}.\end{aligned}
$$

### Variant 1

Given that $y=\log_{7}(x^{3}),$ find $\frac{\mathrm{d}y}{\mathrm{d}x}$.

First, we express $y$ as the composite function

$$
y=\log_{7}(u),\quad u=x^{3}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=3 x^{2}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (3 x^{2})\\ &=\frac{3 x^{2}}{(x^{3})\ln(7)}\\ &=\frac{\cancel{x^{2}}\cdot 3}{\cancel{x^{2}}\cdot x\ln(7)}\\ &=\frac{3}{x \ln{(7 )}}.\end{aligned}
$$

Parameters: `{"a": 1, "b": 7, "c": 0, "k": 0, "n": 3, "t": null}`

### Variant 2

Given that $y=\log_{9}(x^{6}),$ find $\frac{\mathrm{d}y}{\mathrm{d}x}$.

First, we express $y$ as the composite function

$$
y=\log_{9}(u),\quad u=x^{6}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(9)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=6 x^{5}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(9)}\cdot (6 x^{5})\\ &=\frac{6 x^{5}}{(x^{6})\ln(9)}\\ &=\frac{\cancel{x^{5}}\cdot 6}{\cancel{x^{5}}\cdot x\ln(9)}\\ &=\frac{6}{x \ln{(9 )}}.\end{aligned}
$$

Parameters: `{"a": 1, "b": 9, "c": 0, "k": 0, "n": 6, "t": null}`

## q-48656 — moderate

### Captured original

Find the slope of the tangent to the curve $y={log}_{3}⁡(5x-2)+5$ at the point where $x=\frac{7}{15}.$

First, we express $y$ as the composite function

$$
y={log}_{3}⁡(u)+5,\,u=5x-2.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{uln⁡(3)},\,\frac{\text{d}u}{\text{d}x}=5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{uln⁡(3)}\cdot 5 \\  & =\frac{1}{(5x-2)ln⁡(3)}\cdot 5 \\  & =\frac{5}{(5x-2)ln⁡(3)}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=\frac{7}{15}$ is 

$$
\begin{aligned}\begin{aligned}m=\frac{\text{d}y}{\text{d}x}{|}_{x=7/15} & =\frac{5}{(5x-2)ln⁡(3)}{|}_{x=7/15} \\  & =\frac{5}{(5(\frac{7}{15})-2)ln⁡(3)} \\  & =\frac{5}{\frac{1}{3}ln⁡(3)} \\  & =\frac{15}{ln⁡(3)}.\end{aligned}\end{aligned}
$$

### Served original parameters

Find the slope of the tangent to the curve $y=\log_{3}(5 x - 2)+5$ at the point where $x=\frac{7}{15}.$

First, we express $y$ as the composite function

$$
y=\log_{3}(u)+5,\quad u=5 x - 2.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(3)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(3)}\cdot (5)\\ &=\frac{1}{(5 x - 2)\ln(3)}\cdot (5)\\ &=\frac{5}{5 x - 2}\frac{1}{\ln(3)}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=\frac{7}{15}$ is

$$
\begin{aligned}m=\frac{\mathrm{d}y}{\mathrm{d}x}\big|_{x=\frac{7}{15}} &=\left.(\frac{5}{(5 x - 2) \ln{(3 )}})\right|_{x=\frac{7}{15}}\\ &=\frac{5}{(5 (\frac{7}{15}) - 2) \ln{(3 )}}\\ &=\frac{5}{(\frac{1}{3})\ln(3)}\\ &=\frac{15}{\ln{(3 )}}.\end{aligned}
$$

### Variant 1

Find the slope of the tangent to the curve $y=\log_{7}(- 5 x)-8$ at the point where $x=- \frac{1}{25}.$

First, we express $y$ as the composite function

$$
y=\log_{7}(u)-8,\quad u=- 5 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (-5)\\ &=\frac{1}{(- 5 x)\ln(7)}\cdot (-5)\\ &=\frac{1}{x}\frac{1}{\ln(7)}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=- \frac{1}{25}$ is

$$
\begin{aligned}m=\frac{\mathrm{d}y}{\mathrm{d}x}\big|_{x=- \frac{1}{25}} &=\left.(\frac{1}{x \ln{(7 )}})\right|_{x=- \frac{1}{25}}\\ &=\frac{1}{(- \frac{1}{25}) \ln{(7 )}}\\ &=\frac{-5}{(\frac{1}{5})\ln(7)}\\ &=- \frac{25}{\ln{(7 )}}.\end{aligned}
$$

Parameters: `{"a": -5, "b": 7, "c": 0, "k": -8, "n": 1, "t": "-1/25"}`

### Variant 2

Find the slope of the tangent to the curve $y=\log_{5}(4 - 4 x)+6$ at the point where $x=\frac{3}{8}.$

First, we express $y$ as the composite function

$$
y=\log_{5}(u)+6,\quad u=4 - 4 x.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(5)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-4.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(5)}\cdot (-4)\\ &=\frac{1}{(4 - 4 x)\ln(5)}\cdot (-4)\\ &=- \frac{4}{4 - 4 x}\frac{1}{\ln(5)}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=\frac{3}{8}$ is

$$
\begin{aligned}m=\frac{\mathrm{d}y}{\mathrm{d}x}\big|_{x=\frac{3}{8}} &=\left.(\frac{1}{(x - 1) \ln{(5 )}})\right|_{x=\frac{3}{8}}\\ &=\frac{1}{((\frac{3}{8}) - 1) \ln{(5 )}}\\ &=\frac{-4}{(\frac{5}{2})\ln(5)}\\ &=- \frac{8}{5 \ln{(5 )}}.\end{aligned}
$$

Parameters: `{"a": -4, "b": 5, "c": 4, "k": 6, "n": 1, "t": "3/8"}`

## q-51317 — easy

### Captured original

Find ${y}^{′}$ for $y=log⁡(1-x).$

First, we express $y$ as the composite function

$$
y=log⁡u={log}_{10}⁡(u),\,u=1-x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{uln⁡(10)},\,\frac{\text{d}u}{\text{d}x}=-1.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{uln⁡(10)}\cdot (-1) \\  & =\frac{1}{(1-x)ln⁡(10)}\cdot (-1) \\  & =-\frac{1}{(1-x)ln⁡(10)}.\end{aligned}
$$

### Served original parameters

Find $y'$ for $y=\log(1 - x).$

First, we express $y$ as the composite function

$$
y=\log(u)=\log_{10}(u),\quad u=1 - x.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(10)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-1.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(10)}\cdot (-1)\\ &=\frac{1}{(1 - x)\ln(10)}\cdot (-1)\\ &=- \frac{1}{1 - x}\frac{1}{\ln(10)}.\end{aligned}
$$

### Variant 1

Find $y'$ for $y=\log(- x - 8).$

First, we express $y$ as the composite function

$$
y=\log(u)=\log_{10}(u),\quad u=- x - 8.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(10)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-1.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(10)}\cdot (-1)\\ &=\frac{1}{(- x - 8)\ln(10)}\cdot (-1)\\ &=- \frac{1}{- x - 8}\frac{1}{\ln(10)}.\end{aligned}
$$

Parameters: `{"a": -1, "b": 10, "c": -8, "k": 0, "n": 1, "t": null}`

### Variant 2

Find $y'$ for $y=\log(5 - x).$

First, we express $y$ as the composite function

$$
y=\log(u)=\log_{10}(u),\quad u=5 - x.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(10)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=-1.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(10)}\cdot (-1)\\ &=\frac{1}{(5 - x)\ln(10)}\cdot (-1)\\ &=- \frac{1}{5 - x}\frac{1}{\ln(10)}.\end{aligned}
$$

Parameters: `{"a": -1, "b": 10, "c": 5, "k": 0, "n": 1, "t": null}`

## q-71478 — hard

### Captured original

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={log}_{3}⁡(\sqrt{2x}).$

First, we express $y$ as the composite function

$$
y={log}_{3}⁡(u),\,u=\sqrt{2x}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{uln⁡(3)},\,\frac{\text{d}u}{\text{d}x}=\frac{\sqrt{2}}{2\sqrt{x}}=\frac{1}{\sqrt{2x}}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{uln⁡(3)}\cdot \frac{1}{\sqrt{2x}} \\  & =\frac{1}{\sqrt{2x}ln⁡(3)}\cdot \frac{1}{\sqrt{2x}} \\  & =\frac{1}{2xln⁡(3)}.\end{aligned}
$$

### Served original parameters

Calculate $\frac{\mathrm{d}y}{\mathrm{d}x}$ for $y=\log_{3}(\sqrt{2 x}).$

First, we express $y$ as the composite function

$$
y=\log_{3}(u),\quad u=\sqrt{2 x}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(3)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=\frac{\sqrt{2}}{2\sqrt{x}}=\frac{2}{2\sqrt{2 x}}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(3)}\cdot (\frac{2}{2\sqrt{2 x}})\\ &=\frac{1}{(\sqrt{2 x})\ln(3)}\cdot (\frac{2}{2\sqrt{2 x}})\\ &=\frac{1}{2 x}\frac{1}{\ln(3)}.\end{aligned}
$$

### Variant 1

Calculate $\frac{\mathrm{d}y}{\mathrm{d}x}$ for $y=\log_{7}(\sqrt{- 5 x}).$

First, we express $y$ as the composite function

$$
y=\log_{7}(u),\quad u=\sqrt{- 5 x}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(7)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=\frac{\sqrt{5}}{2\sqrt{-x}}\cdot(-1)=\frac{-5}{2\sqrt{- 5 x}}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(7)}\cdot (\frac{-5}{2\sqrt{- 5 x}})\\ &=\frac{1}{(\sqrt{- 5 x})\ln(7)}\cdot (\frac{-5}{2\sqrt{- 5 x}})\\ &=\frac{1}{2 x}\frac{1}{\ln(7)}.\end{aligned}
$$

Parameters: `{"a": -5, "b": 7, "c": 0, "k": 0, "n": 1, "t": null}`

### Variant 2

Calculate $\frac{\mathrm{d}y}{\mathrm{d}x}$ for $y=\log_{9}(\sqrt{9 x}).$

First, we express $y$ as the composite function

$$
y=\log_{9}(u),\quad u=\sqrt{9 x}.
$$

Differentiating gives

$$
\frac{\mathrm{d}y}{\mathrm{d}u}=\frac{1}{u\ln(9)},\quad \frac{\mathrm{d}u}{\mathrm{d}x}=\frac{\sqrt{9}}{2\sqrt{x}}=\frac{9}{2\sqrt{9 x}}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\mathrm{d}y}{\mathrm{d}x} &=\frac{\mathrm{d}y}{\mathrm{d}u}\cdot \frac{\mathrm{d}u}{\mathrm{d}x}\\ &=\frac{1}{u\ln(9)}\cdot (\frac{9}{2\sqrt{9 x}})\\ &=\frac{1}{(\sqrt{9 x})\ln(9)}\cdot (\frac{9}{2\sqrt{9 x}})\\ &=\frac{1}{2 x}\frac{1}{\ln(9)}.\end{aligned}
$$

Parameters: `{"a": 9, "b": 9, "c": 0, "k": 0, "n": 1, "t": null}`


Native-equivalence limitation: the frozen engine accepts canonical keys, but broader valid equivalents can return “answer comparison has unresolved domain differences.” This includes the original unreduced radical chain 7/(2 sqrt(7x) sqrt(7x) ln4) on x>0 and logarithm-power rewrites ln4=2ln2, ln8=3ln2, ln9=2ln3. `equivalent-probe-validation.json` records the mathematical expectation separately from the actual grader result. All valid parameters and outputs remain available.
