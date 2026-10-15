# Original and changed review examples

Each family has its exact original/reference parameters and two changed examples. The easy reference is authored; unrated and missing-field completions are explicitly attributed in metadata. Raw captures and raw omissions remain in raw-source-replays.json.

## q-11934 / original

{"difficulty": "moderate", "template": "shift-power-radio", "parameters": {"n": 3, "b": 4}, "bank_profile": "shift-power-radio-complete"}

Given that $f(x)=\ln(x^{3} - 4)$, find $\frac{df}{dx}.$

- $\frac{3 x^{2}}{x^{3} - 4}$
- $\frac{6}{x^{3} - 4}$
- $2 x \ln{(x^{3} - 4 )}$
- $\frac{x}{x^{3} - 4}$
- $\frac{x^{2}}{x^{3} - 4}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=x^{3} - 4.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=3 x^{2}.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (3 x^{2}) \\ &=\frac{1}{x^{3} - 4}\cdot (3 x^{2}) \\ &=\frac{3 x^{2}}{x^{3} - 4}.\end{aligned}
$$

## q-11934 / changed-1

{"difficulty": "moderate", "template": "shift-power-radio", "parameters": {"n": 4, "b": 7}, "bank_profile": "shift-power-radio-complete"}

Given that $f(x)=\ln(x^{4} - 7)$, find $\frac{df}{dx}.$

- $\frac{4 x^{3}}{x^{4} - 7}$
- $\frac{12}{x^{4} - 7}$
- $3 x \ln{(x^{4} - 7 )}$
- $\frac{x}{x^{4} - 7}$
- $\frac{x^{3}}{x^{4} - 7}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=x^{4} - 7.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=4 x^{3}.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (4 x^{3}) \\ &=\frac{1}{x^{4} - 7}\cdot (4 x^{3}) \\ &=\frac{4 x^{3}}{x^{4} - 7}.\end{aligned}
$$

## q-11934 / changed-2

{"difficulty": "moderate", "template": "shift-power-radio", "parameters": {"n": 5, "b": 2}, "bank_profile": "shift-power-radio-complete"}

Given that $f(x)=\ln(x^{5} - 2)$, find $\frac{df}{dx}.$

- $\frac{5 x^{4}}{x^{5} - 2}$
- $\frac{20}{x^{5} - 2}$
- $4 x \ln{(x^{5} - 2 )}$
- $\frac{x}{x^{5} - 2}$
- $\frac{x^{4}}{x^{5} - 2}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=x^{5} - 2.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=5 x^{4}.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (5 x^{4}) \\ &=\frac{1}{x^{5} - 2}\cdot (5 x^{4}) \\ &=\frac{5 x^{4}}{x^{5} - 2}.\end{aligned}
$$

## q-28632 / original

{"difficulty": "moderate", "template": "scale-legacy-radio", "parameters": {"a": 2}, "bank_profile": "scale-legacy-radio-complete"}

For $g(x)=\ln(2 x)$, find $g^{′}(x).$

- $\frac{1}{2 x}$
- $1 + \frac{2}{x}$
- $\frac{1}{x}$
- $2 + \frac{1}{x}$
- $\frac{2}{x}$

First, we express $g(x)$ as the composite function

$$
g=\ln u,\,u=2 x.
$$

Differentiating gives

$$
\frac{\text{d}g}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=2.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}g}{\text{d}x} &=\frac{\text{d}g}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (2) \\ &=\frac{1}{2 x}\cdot (2) \\ &=\frac{2}{2 x} \\ &=\frac{\cancel{2}}{\cancel{2}x} \\ &=\frac{1}{x}.\end{aligned}
$$

## q-28632 / changed-1

{"difficulty": "moderate", "template": "scale-legacy-radio", "parameters": {"a": 3}, "bank_profile": "scale-legacy-radio-complete"}

For $g(x)=\ln(3 x)$, find $g^{′}(x).$

- $\frac{1}{3 x}$
- $1 + \frac{3}{x}$
- $\frac{1}{x}$
- $3 + \frac{1}{x}$
- $\frac{3}{x}$

First, we express $g(x)$ as the composite function

$$
g=\ln u,\,u=3 x.
$$

Differentiating gives

$$
\frac{\text{d}g}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=3.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}g}{\text{d}x} &=\frac{\text{d}g}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (3) \\ &=\frac{1}{3 x}\cdot (3) \\ &=\frac{3}{3 x} \\ &=\frac{\cancel{3}}{\cancel{3}x} \\ &=\frac{1}{x}.\end{aligned}
$$

## q-28632 / changed-2

{"difficulty": "moderate", "template": "scale-legacy-radio", "parameters": {"a": -2}, "bank_profile": "scale-legacy-radio-complete"}

For $g(x)=\ln(- 2 x)$, find $g^{′}(x).$

- $- \frac{1}{2 x}$
- $1 - \frac{2}{x}$
- $\frac{1}{x}$
- $-2 + \frac{1}{x}$
- $- \frac{2}{x}$

First, we express $g(x)$ as the composite function

$$
g=\ln u,\,u=- 2 x.
$$

Differentiating gives

$$
\frac{\text{d}g}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-2.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}g}{\text{d}x} &=\frac{\text{d}g}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-2) \\ &=\frac{1}{- 2 x}\cdot (-2) \\ &=\frac{-2}{- 2 x} \\ &=\frac{\cancel{-2}}{\cancel{-2}x} \\ &=\frac{1}{x}.\end{aligned}
$$

## q-107469 / original

{"difficulty": "hard", "template": "tangent-affine", "parameters": {"a": 2, "b": 2, "t": 1}, "bank_profile": "tangent-affine-complete"}

Find the equation of the tangent to the curve $f(x)=\ln(- 2 x + 4)$ at the point $(1,\ln{(2 )}).$

- $y=x - 1 + \ln{(2 )}$
- $y=x + \ln{(2 )} + 1$
- $y=- x + \ln{(2 )} + 1$
- $y=- x + \ln{(2 )}$
- $y=2 x + \ln{(2 )}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- 2 x + 4.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-2.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-2) \\ &=\frac{1}{- 2 x + 4}\cdot (-2) \\ &=\frac{-2}{- 2 x + 4} \\ &=-\frac{\cancel{2}}{\cancel{2}\cdot(- x + 2)} \\ &=\frac{1}{x - 2}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=1$ is 

$$
\begin{aligned}\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=1} &=\left.(\frac{1}{x - 2})\right|_{x=1} \\ &=\frac{(-2)}{(- 2 (1) + 4)} \\ &=-1.\end{aligned}
$$

Hence, the slope of the tangent line at the point $(1,\ln{(2 )})$ is $m=-1.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(\ln{(2 )}) &=(-1)(x-(1)) \\ y &=- x + \ln{(2 )} + 1\end{aligned}
$$

## q-107469 / changed-1

{"difficulty": "hard", "template": "tangent-affine", "parameters": {"a": 3, "b": 4, "t": -1}, "bank_profile": "tangent-affine-complete"}

Find the equation of the tangent to the curve $f(x)=\ln(- 3 x + 12)$ at the point $(-1,\ln{(15 )}).$

- $y=\frac{x}{5} + \frac{1}{5} + \ln{(15 )}$
- $y=\frac{x}{5} - \frac{1}{5} + \ln{(15 )}$
- $y=- \frac{x}{5} - \frac{1}{5} + \ln{(15 )}$
- $y=- \frac{x}{5} + \ln{(15 )}$
- $y=\frac{2 x}{5} + \ln{(15 )}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- 3 x + 12.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-3.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-3) \\ &=\frac{1}{- 3 x + 12}\cdot (-3) \\ &=\frac{-3}{- 3 x + 12} \\ &=-\frac{\cancel{3}}{\cancel{3}\cdot(- x + 4)} \\ &=\frac{1}{x - 4}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=-1$ is 

$$
\begin{aligned}\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=-1} &=\left.(\frac{1}{x - 4})\right|_{x=-1} \\ &=\frac{(-3)}{(- 3 (-1) + 12)} \\ &=- \frac{1}{5}.\end{aligned}
$$

Hence, the slope of the tangent line at the point $(-1,\ln{(15 )})$ is $m=- \frac{1}{5}.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(\ln{(15 )}) &=(- \frac{1}{5})(x-(-1)) \\ y &=- \frac{x}{5} - \frac{1}{5} + \ln{(15 )}\end{aligned}
$$

## q-107469 / changed-2

{"difficulty": "hard", "template": "tangent-affine", "parameters": {"a": 1, "b": 3, "t": 2}, "bank_profile": "tangent-affine-complete"}

Find the equation of the tangent to the curve $f(x)=\ln(- x + 3)$ at the point $(2,0).$

- $y=x - 2$
- $y=x + 2$
- $y=- x + 2$
- $y=- x$
- $y=2 x$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- x + 3.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-1.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-1) \\ &=\frac{1}{- x + 3}\cdot (-1) \\ &=\frac{-1}{- x + 3} \\ &=-\frac{\cancel{1}}{\cancel{1}\cdot(- x + 3)} \\ &=\frac{1}{x - 3}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=2$ is 

$$
\begin{aligned}\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=2} &=\left.(\frac{1}{x - 3})\right|_{x=2} \\ &=\frac{(-1)}{(- (2) + 3)} \\ &=-1.\end{aligned}
$$

Hence, the slope of the tangent line at the point $(2,0)$ is $m=-1.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(0) &=(-1)(x-(2)) \\ y &=- x + 2\end{aligned}
$$

## q-341676 / original

{"difficulty": "moderate", "template": "polynomial-blank", "parameters": {"a": 3, "b": 5, "n": 6}, "bank_profile": null}

Given that $f(x)=\ln(- 5 x^{6} + 3)$, find $\frac{\text{d}f}{\text{d}x}.$

$\frac{\text{d}f}{\text{d}x}=$
{{field-1}}

- $\frac{30 x^{5}}{5 x^{6} - 3}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- 5 x^{6} + 3.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=- 30 x^{5}.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (- 30 x^{5}) \\ &=\frac{1}{- 5 x^{6} + 3}\cdot (- 30 x^{5}) \\ &=\frac{- 30 x^{5}}{- 5 x^{6} + 3}.\end{aligned}
$$

## q-341676 / changed-1

{"difficulty": "moderate", "template": "polynomial-blank", "parameters": {"a": 1, "b": 2, "n": 3}, "bank_profile": null}

Given that $f(x)=\ln(- 2 x^{3} + 1)$, find $\frac{\text{d}f}{\text{d}x}.$

$\frac{\text{d}f}{\text{d}x}=$
{{field-1}}

- $\frac{6 x^{2}}{2 x^{3} - 1}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- 2 x^{3} + 1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=- 6 x^{2}.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (- 6 x^{2}) \\ &=\frac{1}{- 2 x^{3} + 1}\cdot (- 6 x^{2}) \\ &=\frac{- 6 x^{2}}{- 2 x^{3} + 1}.\end{aligned}
$$

## q-341676 / changed-2

{"difficulty": "moderate", "template": "polynomial-blank", "parameters": {"a": 5, "b": 1, "n": 4}, "bank_profile": null}

Given that $f(x)=\ln(- x^{4} + 5)$, find $\frac{\text{d}f}{\text{d}x}.$

$\frac{\text{d}f}{\text{d}x}=$
{{field-1}}

- $\frac{4 x^{3}}{x^{4} - 5}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- x^{4} + 5.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=- 4 x^{3}.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (- 4 x^{3}) \\ &=\frac{1}{- x^{4} + 5}\cdot (- 4 x^{3}) \\ &=\frac{- 4 x^{3}}{- x^{4} + 5}.\end{aligned}
$$

## q-11930 / original

{"difficulty": "moderate", "template": "scale-radio", "parameters": {"a": 8}, "bank_profile": "scale-radio-complete"}

Given that $f(x)=\ln(8 x)$, find $\frac{\text{d}f}{\text{d}x}.$

- $\frac{8}{x}$
- $8 \ln{(8 x )}$
- $\frac{1}{\ln{(8 x )}}$
- $\frac{1}{x}$
- $\frac{1}{8 x}$

Here $f(x)=\ln(8 x)$ is a function of a function. We use the chain rule. First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=8 x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=8.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (8) \\ &=\frac{1}{8 x}\cdot (8) \\ &=\frac{8}{8 x} \\ &=\frac{\cancel{8}}{\cancel{8}x} \\ &=\frac{1}{x}.\end{aligned}
$$

## q-11930 / changed-1

{"difficulty": "moderate", "template": "scale-radio", "parameters": {"a": 3}, "bank_profile": "scale-radio-complete"}

Given that $f(x)=\ln(3 x)$, find $\frac{\text{d}f}{\text{d}x}.$

- $\frac{3}{x}$
- $3 \ln{(3 x )}$
- $\frac{1}{\ln{(3 x )}}$
- $\frac{1}{x}$
- $\frac{1}{3 x}$

Here $f(x)=\ln(3 x)$ is a function of a function. We use the chain rule. First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=3 x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=3.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (3) \\ &=\frac{1}{3 x}\cdot (3) \\ &=\frac{3}{3 x} \\ &=\frac{\cancel{3}}{\cancel{3}x} \\ &=\frac{1}{x}.\end{aligned}
$$

## q-11930 / changed-2

{"difficulty": "moderate", "template": "scale-radio", "parameters": {"a": -2}, "bank_profile": "scale-radio-complete"}

Given that $f(x)=\ln(- 2 x)$, find $\frac{\text{d}f}{\text{d}x}.$

- $- \frac{2}{x}$
- $- 2 \ln{(- 2 x )}$
- $\frac{1}{\ln{(- 2 x )}}$
- $\frac{1}{x}$
- $- \frac{1}{2 x}$

Here $f(x)=\ln(- 2 x)$ is a function of a function. We use the chain rule. First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- 2 x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-2.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-2) \\ &=\frac{1}{- 2 x}\cdot (-2) \\ &=\frac{-2}{- 2 x} \\ &=\frac{\cancel{-2}}{\cancel{-2}x} \\ &=\frac{1}{x}.\end{aligned}
$$

## q-11932 / original

{"difficulty": "moderate", "template": "power-radio", "parameters": {"n": 2}, "bank_profile": "power-radio-complete"}

Given that $g(x)=\ln(x^{2})$, find $\frac{\text{d}g}{\text{d}x}.$

- $2 x \ln{(x^{2} )}$
- $\frac{1}{x}$
- $\frac{2}{x^{2}}$
- $\frac{2}{x}$
- $\frac{1}{x^{2}}$

First, we express $g(x)$ as the composite function

$$
g=\ln u,\,u=x^{2}.
$$

Differentiating gives

$$
\frac{\text{d}g}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=2 x.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}g}{\text{d}x} &=\frac{\text{d}g}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (2 x) \\ &=\frac{1}{x^{2}}\cdot (2 x) \\ &=\frac{2 x}{x^{2}} \\ &=\frac{2\cancel{x^{1}}}{x\cdot\cancel{x^{1}}} \\ &=\frac{2}{x}.\end{aligned}
$$

## q-11932 / changed-1

{"difficulty": "moderate", "template": "power-radio", "parameters": {"n": 3}, "bank_profile": "power-radio-complete"}

Given that $g(x)=\ln(x^{3})$, find $\frac{\text{d}g}{\text{d}x}.$

- $3 x^{2} \ln{(x^{3} )}$
- $\frac{1}{x}$
- $\frac{3}{x^{3}}$
- $\frac{3}{x}$
- $\frac{1}{x^{3}}$

First, we express $g(x)$ as the composite function

$$
g=\ln u,\,u=x^{3}.
$$

Differentiating gives

$$
\frac{\text{d}g}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=3 x^{2}.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}g}{\text{d}x} &=\frac{\text{d}g}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (3 x^{2}) \\ &=\frac{1}{x^{3}}\cdot (3 x^{2}) \\ &=\frac{3 x^{2}}{x^{3}} \\ &=\frac{3\cancel{x^{2}}}{x\cdot\cancel{x^{2}}} \\ &=\frac{3}{x}.\end{aligned}
$$

## q-11932 / changed-2

{"difficulty": "moderate", "template": "power-radio", "parameters": {"n": 4}, "bank_profile": "power-radio-complete"}

Given that $g(x)=\ln(x^{4})$, find $\frac{\text{d}g}{\text{d}x}.$

- $4 x^{3} \ln{(x^{4} )}$
- $\frac{1}{x}$
- $\frac{4}{x^{4}}$
- $\frac{4}{x}$
- $\frac{1}{x^{4}}$

First, we express $g(x)$ as the composite function

$$
g=\ln u,\,u=x^{4}.
$$

Differentiating gives

$$
\frac{\text{d}g}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=4 x^{3}.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}g}{\text{d}x} &=\frac{\text{d}g}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (4 x^{3}) \\ &=\frac{1}{x^{4}}\cdot (4 x^{3}) \\ &=\frac{4 x^{3}}{x^{4}} \\ &=\frac{4\cancel{x^{3}}}{x\cdot\cancel{x^{3}}} \\ &=\frac{4}{x}.\end{aligned}
$$

## q-150014 / original

{"difficulty": "hard", "template": "tangent-origin", "parameters": {"a": 3, "t": 0}, "bank_profile": "tangent-origin-complete"}

Find the equation of the tangent to the curve $f(x)=\ln(3 x + 1)$ at the point $(0,0).$

- $y=3 x + 1$
- $y=3 x$
- $y=x$
- $y=x + 3$
- $y=3 x + \ln{(3 )}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=3 x + 1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=3.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (3) \\ &=\frac{1}{3 x + 1}\cdot (3) \\ &=\frac{3}{3 x + 1}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=0$ is 

$$
\begin{aligned}\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=0} &=\left.(\frac{3}{3 x + 1})\right|_{x=0} \\ &=\frac{(3)}{(3 (0) + 1)} \\ &=3.\end{aligned}
$$

Hence, the slope of the tangent line at the point $(0,0)$ is $m=3.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(0) &=(3)(x-(0)) \\ y &=3 x\end{aligned}
$$

## q-150014 / changed-1

{"difficulty": "hard", "template": "tangent-origin", "parameters": {"a": 2, "t": -2}, "bank_profile": "tangent-origin-complete"}

Find the equation of the tangent to the curve $f(x)=\ln(2 x + 5)$ at the point $(-2,0).$

- $y=2 x + 5$
- $y=2 x + 4$
- $y=x + 2$
- $y=x + 4$
- $y=2 x + \ln{(2 )} + 4$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=2 x + 5.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=2.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (2) \\ &=\frac{1}{2 x + 5}\cdot (2) \\ &=\frac{2}{2 x + 5}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=-2$ is 

$$
\begin{aligned}\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=-2} &=\left.(\frac{2}{2 x + 5})\right|_{x=-2} \\ &=\frac{(2)}{(2 (-2) + 5)} \\ &=2.\end{aligned}
$$

Hence, the slope of the tangent line at the point $(-2,0)$ is $m=2.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(0) &=(2)(x-(-2)) \\ y &=2 x + 4\end{aligned}
$$

## q-150014 / changed-2

{"difficulty": "hard", "template": "tangent-origin", "parameters": {"a": 5, "t": 3}, "bank_profile": "tangent-origin-complete"}

Find the equation of the tangent to the curve $f(x)=\ln(5 x - 14)$ at the point $(3,0).$

- $y=5 x - 14$
- $y=5 x - 15$
- $y=x - 3$
- $y=x + 2$
- $y=5 x - 15 + \ln{(5 )}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=5 x - 14.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=5.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (5) \\ &=\frac{1}{5 x - 14}\cdot (5) \\ &=\frac{5}{5 x - 14}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=3$ is 

$$
\begin{aligned}\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=3} &=\left.(\frac{5}{5 x - 14})\right|_{x=3} \\ &=\frac{(5)}{(5 (3) - 14)} \\ &=5.\end{aligned}
$$

Hence, the slope of the tangent line at the point $(3,0)$ is $m=5.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(0) &=(5)(x-(3)) \\ y &=5 x - 15\end{aligned}
$$

## q-150015 / original

{"difficulty": "hard", "template": "tangent-shift", "parameters": {"t": 1}, "bank_profile": "tangent-shift-complete"}

Find the equation of the tangent to the curve $f(x)=\ln(- x + 2)$ at the point $(1,0).$

- $y=x - 1$
- $y=x + 1$
- $y=- x + 1$
- $y=- x$
- $y=2 x$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- x + 2.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-1.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-1) \\ &=\frac{1}{- x + 2}\cdot (-1) \\ &=\frac{1}{x - 2}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=1$ is 

$$
\begin{aligned}\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=1} &=\left.(\frac{1}{x - 2})\right|_{x=1} \\ &=\frac{(-1)}{(- (1) + 2)} \\ &=-1.\end{aligned}
$$

Hence, the slope of the tangent line at the point $(1,0)$ is $m=-1.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(0) &=(-1)(x-(1)) \\ y &=- x + 1\end{aligned}
$$

## q-150015 / changed-1

{"difficulty": "hard", "template": "tangent-shift", "parameters": {"t": -2}, "bank_profile": "tangent-shift-complete"}

Find the equation of the tangent to the curve $f(x)=\ln(- x - 1)$ at the point $(-2,0).$

- $y=x + 2$
- $y=x - 2$
- $y=- x - 2$
- $y=- x$
- $y=2 x$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- x - 1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-1.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-1) \\ &=\frac{1}{- x - 1}\cdot (-1) \\ &=\frac{1}{x + 1}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=-2$ is 

$$
\begin{aligned}\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=-2} &=\left.(\frac{1}{x + 1})\right|_{x=-2} \\ &=\frac{(-1)}{(- (-2) - 1)} \\ &=-1.\end{aligned}
$$

Hence, the slope of the tangent line at the point $(-2,0)$ is $m=-1.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(0) &=(-1)(x-(-2)) \\ y &=- x - 2\end{aligned}
$$

## q-150015 / changed-2

{"difficulty": "hard", "template": "tangent-shift", "parameters": {"t": 7}, "bank_profile": "tangent-shift-complete"}

Find the equation of the tangent to the curve $f(x)=\ln(- x + 8)$ at the point $(7,0).$

- $y=x - 7$
- $y=x + 7$
- $y=- x + 7$
- $y=- x$
- $y=2 x$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- x + 8.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-1.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-1) \\ &=\frac{1}{- x + 8}\cdot (-1) \\ &=\frac{1}{x - 8}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=7$ is 

$$
\begin{aligned}\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=7} &=\left.(\frac{1}{x - 8})\right|_{x=7} \\ &=\frac{(-1)}{(- (7) + 8)} \\ &=-1.\end{aligned}
$$

Hence, the slope of the tangent line at the point $(7,0)$ is $m=-1.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(0) &=(-1)(x-(7)) \\ y &=- x + 7\end{aligned}
$$

## q-310144 / original

{"difficulty": "moderate", "template": "slope-polynomial", "parameters": {"a": 5, "b": 4, "t": 1}, "bank_profile": null}

Find the slope $m$ of the tangent to the curve $f(x)=\ln(5 x^{2} + 4)$ at the point where $x=1.$

$m=$
{{field-1}}

- $\frac{10}{9}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=5 x^{2} + 4.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=10 x.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (10 x) \\ &=\frac{1}{5 x^{2} + 4}\cdot (10 x) \\ &=\frac{10 x}{5 x^{2} + 4}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=1$ is 

$$
\begin{aligned}m=\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=1} &=\left.(\frac{10 x}{5 x^{2} + 4})\right|_{x=1} \\ &=\frac{(10 (1))}{(5 (1)^{2} + 4)} \\ &=\frac{10}{9}.\end{aligned}
$$

## q-310144 / changed-1

{"difficulty": "moderate", "template": "slope-polynomial", "parameters": {"a": 2, "b": 3, "t": 0}, "bank_profile": null}

Find the slope $m$ of the tangent to the curve $f(x)=\ln(2 x^{2} + 3)$ at the point where $x=0.$

$m=$
{{field-1}}

- $0$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=2 x^{2} + 3.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=4 x.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (4 x) \\ &=\frac{1}{2 x^{2} + 3}\cdot (4 x) \\ &=\frac{4 x}{2 x^{2} + 3}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=0$ is 

$$
\begin{aligned}m=\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=0} &=\left.(\frac{4 x}{2 x^{2} + 3})\right|_{x=0} \\ &=\frac{(4 (0))}{(2 (0)^{2} + 3)} \\ &=0.\end{aligned}
$$

## q-310144 / changed-2

{"difficulty": "moderate", "template": "slope-polynomial", "parameters": {"a": 6, "b": 1, "t": -2}, "bank_profile": null}

Find the slope $m$ of the tangent to the curve $f(x)=\ln(6 x^{2} + 1)$ at the point where $x=-2.$

$m=$
{{field-1}}

- $- \frac{24}{25}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=6 x^{2} + 1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=12 x.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (12 x) \\ &=\frac{1}{6 x^{2} + 1}\cdot (12 x) \\ &=\frac{12 x}{6 x^{2} + 1}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=-2$ is 

$$
\begin{aligned}m=\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=-2} &=\left.(\frac{12 x}{6 x^{2} + 1})\right|_{x=-2} \\ &=\frac{(12 (-2))}{(6 (-2)^{2} + 1)} \\ &=- \frac{24}{25}.\end{aligned}
$$

## q-341671 / original

{"difficulty": "moderate", "template": "scale-blank", "parameters": {"a": 9}, "bank_profile": null}

Given that $f(x)=\ln(9 x)$, find $\frac{\text{d}f}{\text{d}x}.$

$\frac{\text{d}f}{\text{d}x}=$
{{field-1}}

- $\frac{1}{x}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=9 x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=9.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (9) \\ &=\frac{1}{9 x}\cdot (9) \\ &=\frac{9}{9 x} \\ &=\frac{\cancel{9}}{\cancel{9}x} \\ &=\frac{1}{x}.\end{aligned}
$$

## q-341671 / changed-1

{"difficulty": "moderate", "template": "scale-blank", "parameters": {"a": 1}, "bank_profile": null}

Given that $f(x)=\ln(x)$, find $\frac{\text{d}f}{\text{d}x}.$

$\frac{\text{d}f}{\text{d}x}=$
{{field-1}}

- $\frac{1}{x}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=1.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (1) \\ &=\frac{1}{x}\cdot (1) \\ &=\frac{1}{x} \\ &=\frac{\cancel{1}}{\cancel{1}x} \\ &=\frac{1}{x}.\end{aligned}
$$

## q-341671 / changed-2

{"difficulty": "moderate", "template": "scale-blank", "parameters": {"a": -1}, "bank_profile": null}

Given that $f(x)=\ln(- x)$, find $\frac{\text{d}f}{\text{d}x}.$

$\frac{\text{d}f}{\text{d}x}=$
{{field-1}}

- $\frac{1}{x}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-1.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-1) \\ &=\frac{1}{- x}\cdot (-1) \\ &=\frac{-1}{- x} \\ &=\frac{\cancel{-1}}{\cancel{-1}x} \\ &=\frac{1}{x}.\end{aligned}
$$

## q-341679 / original

{"difficulty": "moderate", "template": "slope-affine", "parameters": {"a": 4, "b": 7, "t": -1}, "bank_profile": null}

Find the slope $m$ of the tangent to the curve $f(x)=\ln(- 4 x + 7)$ at the point where $x=-1.$

$m=$
{{field-1}}

- $- \frac{4}{11}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- 4 x + 7.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-4.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-4) \\ &=\frac{1}{- 4 x + 7}\cdot (-4) \\ &=\frac{-4}{- 4 x + 7}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=-1$ is 

$$
\begin{aligned}m=\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=-1} &=\left.(\frac{4}{4 x - 7})\right|_{x=-1} \\ &=\frac{(-4)}{(- 4 (-1) + 7)} \\ &=- \frac{4}{11}.\end{aligned}
$$

## q-341679 / changed-1

{"difficulty": "moderate", "template": "slope-affine", "parameters": {"a": 1, "b": 0, "t": -2}, "bank_profile": null}

Find the slope $m$ of the tangent to the curve $f(x)=\ln(- x)$ at the point where $x=-2.$

$m=$
{{field-1}}

- $- \frac{1}{2}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-1.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-1) \\ &=\frac{1}{- x}\cdot (-1) \\ &=\frac{-1}{- x}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=-2$ is 

$$
\begin{aligned}m=\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=-2} &=\left.(\frac{1}{x})\right|_{x=-2} \\ &=\frac{(-1)}{(- (-2))} \\ &=- \frac{1}{2}.\end{aligned}
$$

## q-341679 / changed-2

{"difficulty": "moderate", "template": "slope-affine", "parameters": {"a": 3, "b": 5, "t": 0}, "bank_profile": null}

Find the slope $m$ of the tangent to the curve $f(x)=\ln(- 3 x + 5)$ at the point where $x=0.$

$m=$
{{field-1}}

- $- \frac{3}{5}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- 3 x + 5.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-3.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-3) \\ &=\frac{1}{- 3 x + 5}\cdot (-3) \\ &=\frac{-3}{- 3 x + 5}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=0$ is 

$$
\begin{aligned}m=\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=0} &=\left.(\frac{3}{3 x - 5})\right|_{x=0} \\ &=\frac{(-3)}{(- 3 (0) + 5)} \\ &=- \frac{3}{5}.\end{aligned}
$$

## q-48654 / original

{"difficulty": "hard", "template": "tangent-scaled", "parameters": {"c": 4, "a": 2, "t": 4}, "bank_profile": "tangent-scaled-complete"}

Find the equation of the tangent to the curve $f(x)=4\ln(2 x)$ at the point $(4,4 \ln{(8 )}).$

- $y=2 x - \ln{(8 )} - 2$
- $y=2 x - 8 + 4 \ln{(8 )}$
- $y=x - 4$
- $y=x - 4 + 12 \ln{(2 )}$
- $y=x + 4$

First, we express $f(x)$ as the composite function

$$
f=4\ln u,\,u=2 x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{4}{u},\,\frac{\text{d}u}{\text{d}x}=2.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{4}{u}\cdot (2) \\ &=\frac{4}{2 x}\cdot (2) \\ &=\frac{8}{2 x} \\ &=\frac{\cancel{2}\cdot 4}{\cancel{2}\cdot x} \\ &=\frac{4}{x}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=4$ is 

$$
\begin{aligned}\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=4} &=\left.(\frac{4}{x})\right|_{x=4} \\ &=\frac{(8)}{(2 (4))} \\ &=1.\end{aligned}
$$

Hence, the slope of the tangent line at the point $(4,4 \ln{(8 )})$ is $m=1.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(4 \ln{(8 )}) &=(1)(x-(4)) \\ y &=x - 4 + 12 \ln{(2 )}\end{aligned}
$$

## q-48654 / changed-1

{"difficulty": "hard", "template": "tangent-scaled", "parameters": {"c": 3, "a": 1, "t": 2}, "bank_profile": "tangent-scaled-complete"}

Find the equation of the tangent to the curve $f(x)=3\ln(x)$ at the point $(2,3 \ln{(2 )}).$

- $y=3 x - \frac{3}{2} - \ln{(2 )}$
- $y=3 x - 6 + 3 \ln{(2 )}$
- $y=\frac{3 x}{2} - 3$
- $y=\frac{3 x}{2} - 3 + 3 \ln{(2 )}$
- $y=\frac{3 x}{2} + 3$

First, we express $f(x)$ as the composite function

$$
f=3\ln u,\,u=x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{3}{u},\,\frac{\text{d}u}{\text{d}x}=1.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{3}{u}\cdot (1) \\ &=\frac{3}{x}\cdot (1) \\ &=\frac{3}{x} \\ &=\frac{\cancel{1}\cdot 3}{\cancel{1}\cdot x} \\ &=\frac{3}{x}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=2$ is 

$$
\begin{aligned}\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=2} &=\left.(\frac{3}{x})\right|_{x=2} \\ &=\frac{(3)}{((2))} \\ &=\frac{3}{2}.\end{aligned}
$$

Hence, the slope of the tangent line at the point $(2,3 \ln{(2 )})$ is $m=\frac{3}{2}.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(3 \ln{(2 )}) &=(\frac{3}{2})(x-(2)) \\ y &=\frac{3 x}{2} - 3 + 3 \ln{(2 )}\end{aligned}
$$

## q-48654 / changed-2

{"difficulty": "hard", "template": "tangent-scaled", "parameters": {"c": 1, "a": 4, "t": 3}, "bank_profile": "tangent-scaled-complete"}

Find the equation of the tangent to the curve $f(x)=\ln(4 x)$ at the point $(3,\ln{(12 )}).$

- $y=\frac{2 x}{3} - \ln{(12 )} - \frac{1}{2}$
- $y=\frac{2 x}{3} - 2 + \ln{(12 )}$
- $y=\frac{x}{3} - 1$
- $y=\frac{x}{3} - 1 + \ln{(12 )}$
- $y=\frac{x}{3} + 1$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=4 x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=4.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (4) \\ &=\frac{1}{4 x}\cdot (4) \\ &=\frac{4}{4 x} \\ &=\frac{\cancel{4}\cdot 1}{\cancel{4}\cdot x} \\ &=\frac{1}{x}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=3$ is 

$$
\begin{aligned}\left.(\frac{\text{d}f}{\text{d}x})\right|_{x=3} &=\left.(\frac{1}{x})\right|_{x=3} \\ &=\frac{(4)}{(4 (3))} \\ &=\frac{1}{3}.\end{aligned}
$$

Hence, the slope of the tangent line at the point $(3,\ln{(12 )})$ is $m=\frac{1}{3}.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(\ln{(12 )}) &=(\frac{1}{3})(x-(3)) \\ y &=\frac{x}{3} - 1 + \ln{(12 )}\end{aligned}
$$

## nonMA-17592186490400 / original

{"difficulty": "hard", "template": "tangent-scaled", "parameters": {"c": 12, "a": 2, "t": 12}, "bank_profile": "tangent-scaled-complete"}

Find the equation of the tangent to the curve $f(x)=12\ln(2 x)$ at the point $(12,12 \ln{(24 )}).$

- $y=2 x - 6 - \ln{(24 )}$
- $y=2 x - 24 + 12 \ln{(24 )}$
- $y=x - 12$
- $y=x - 12 + 12 \ln{(24 )}$
- $y=x + 12$

First, we express $f(x)$ as the composite function

$$
f=12\ln u,\,u=2 x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{12}{u},\,\frac{\text{d}u}{\text{d}x}=2.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{12}{u}\cdot (2) \\ &=\frac{12}{2 x}\cdot (2) \\ &=\frac{12}{x}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=12$ is

$$
m=\left.(\frac{12}{x})\right|_{x=12}=1.
$$

Hence, the slope of the tangent line at the point $(12,12 \ln{(24 )})$ is $m=1.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(12 \ln{(24 )}) &=(1)(x-(12)) \\ y &=x - 12 + 12 \ln{(24 )}\end{aligned}
$$

## nonMA-17592186490400 / changed-1

{"difficulty": "hard", "template": "tangent-scaled", "parameters": {"c": 3, "a": 1, "t": 2}, "bank_profile": "tangent-scaled-complete"}

Find the equation of the tangent to the curve $f(x)=3\ln(x)$ at the point $(2,3 \ln{(2 )}).$

- $y=3 x - \frac{3}{2} - \ln{(2 )}$
- $y=3 x - 6 + 3 \ln{(2 )}$
- $y=\frac{3 x}{2} - 3$
- $y=\frac{3 x}{2} - 3 + 3 \ln{(2 )}$
- $y=\frac{3 x}{2} + 3$

First, we express $f(x)$ as the composite function

$$
f=3\ln u,\,u=x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{3}{u},\,\frac{\text{d}u}{\text{d}x}=1.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{3}{u}\cdot (1) \\ &=\frac{3}{x}\cdot (1) \\ &=\frac{3}{x}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=2$ is

$$
m=\left.(\frac{3}{x})\right|_{x=2}=\frac{3}{2}.
$$

Hence, the slope of the tangent line at the point $(2,3 \ln{(2 )})$ is $m=\frac{3}{2}.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(3 \ln{(2 )}) &=(\frac{3}{2})(x-(2)) \\ y &=\frac{3 x}{2} - 3 + 3 \ln{(2 )}\end{aligned}
$$

## nonMA-17592186490400 / changed-2

{"difficulty": "hard", "template": "tangent-scaled", "parameters": {"c": 1, "a": 4, "t": 3}, "bank_profile": "tangent-scaled-complete"}

Find the equation of the tangent to the curve $f(x)=\ln(4 x)$ at the point $(3,\ln{(12 )}).$

- $y=\frac{2 x}{3} - \ln{(12 )} - \frac{1}{2}$
- $y=\frac{2 x}{3} - 2 + \ln{(12 )}$
- $y=\frac{x}{3} - 1$
- $y=\frac{x}{3} - 1 + \ln{(12 )}$
- $y=\frac{x}{3} + 1$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=4 x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=4.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (4) \\ &=\frac{1}{4 x}\cdot (4) \\ &=\frac{1}{x}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=3$ is

$$
m=\left.(\frac{1}{x})\right|_{x=3}=\frac{1}{3}.
$$

Hence, the slope of the tangent line at the point $(3,\ln{(12 )})$ is $m=\frac{1}{3}.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(\ln{(12 )}) &=(\frac{1}{3})(x-(3)) \\ y &=\frac{x}{3} - 1 + \ln{(12 )}\end{aligned}
$$

## nonMA-17592186490408 / original

{"difficulty": "hard", "template": "tangent-shift", "parameters": {"t": 20}, "bank_profile": "tangent-shift-complete"}

Find the equation of the tangent to the curve $f(x)=\ln(- x + 21)$ at the point $(20,0).$

- $y=x - 20$
- $y=x + 20$
- $y=- x + 20$
- $y=- x$
- $y=2 x$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- x + 21.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-1.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-1) \\ &=\frac{1}{- x + 21}\cdot (-1) \\ &=\frac{1}{x - 21}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=20$ is

$$
m=\left.(\frac{1}{x - 21})\right|_{x=20}=-1.
$$

Hence, the slope of the tangent line at the point $(20,0)$ is $m=-1.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(0) &=(-1)(x-(20)) \\ y &=- x + 20\end{aligned}
$$

## nonMA-17592186490408 / changed-1

{"difficulty": "hard", "template": "tangent-shift", "parameters": {"t": -2}, "bank_profile": "tangent-shift-complete"}

Find the equation of the tangent to the curve $f(x)=\ln(- x - 1)$ at the point $(-2,0).$

- $y=x + 2$
- $y=x - 2$
- $y=- x - 2$
- $y=- x$
- $y=2 x$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- x - 1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-1.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-1) \\ &=\frac{1}{- x - 1}\cdot (-1) \\ &=\frac{1}{x + 1}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=-2$ is

$$
m=\left.(\frac{1}{x + 1})\right|_{x=-2}=-1.
$$

Hence, the slope of the tangent line at the point $(-2,0)$ is $m=-1.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(0) &=(-1)(x-(-2)) \\ y &=- x - 2\end{aligned}
$$

## nonMA-17592186490408 / changed-2

{"difficulty": "hard", "template": "tangent-shift", "parameters": {"t": 7}, "bank_profile": "tangent-shift-complete"}

Find the equation of the tangent to the curve $f(x)=\ln(- x + 8)$ at the point $(7,0).$

- $y=x - 7$
- $y=x + 7$
- $y=- x + 7$
- $y=- x$
- $y=2 x$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- x + 8.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-1.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-1) \\ &=\frac{1}{- x + 8}\cdot (-1) \\ &=\frac{1}{x - 8}.\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=7$ is

$$
m=\left.(\frac{1}{x - 8})\right|_{x=7}=-1.
$$

Hence, the slope of the tangent line at the point $(7,0)$ is $m=-1.$ Now, we find the equation of the tangent at that point:

$$
\begin{aligned}y-y_1 &=m(x-x_1) \\ y-(0) &=(-1)(x-(7)) \\ y &=- x + 7\end{aligned}
$$

## authored-easy / authored-reference

{"difficulty": "easy", "template": "affine-blank", "parameters": {"a": 2, "b": 1}, "bank_profile": null}

Given that $f(x)=\ln(2 x + 1)$, find $\frac{\text{d}f}{\text{d}x}.$

$\frac{\text{d}f}{\text{d}x}=$
{{field-1}}

- $\frac{2}{2 x + 1}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=2 x + 1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=2.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (2) \\ &=\frac{1}{2 x + 1}\cdot (2) \\ &=\frac{2}{2 x + 1}.\end{aligned}
$$

## authored-easy / changed-1

{"difficulty": "easy", "template": "affine-blank", "parameters": {"a": 1, "b": 0}, "bank_profile": null}

Given that $f(x)=\ln(x)$, find $\frac{\text{d}f}{\text{d}x}.$

$\frac{\text{d}f}{\text{d}x}=$
{{field-1}}

- $\frac{1}{x}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=1.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (1) \\ &=\frac{1}{x}\cdot (1) \\ &=\frac{1}{x}.\end{aligned}
$$

## authored-easy / changed-2

{"difficulty": "easy", "template": "affine-blank", "parameters": {"a": -2, "b": 3}, "bank_profile": null}

Given that $f(x)=\ln(- 2 x + 3)$, find $\frac{\text{d}f}{\text{d}x}.$

$\frac{\text{d}f}{\text{d}x}=$
{{field-1}}

- $\frac{2}{2 x - 3}$

First, we express $f(x)$ as the composite function

$$
f=\ln u,\,u=- 2 x + 3.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=\frac{1}{u},\,\frac{\text{d}u}{\text{d}x}=-2.
$$

We now apply the chain rule, and we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} &=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=\frac{1}{u}\cdot (-2) \\ &=\frac{1}{- 2 x + 3}\cdot (-2) \\ &=\frac{-2}{- 2 x + 3}.\end{aligned}
$$
