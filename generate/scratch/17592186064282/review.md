## q-31330 — Math Academy captured source and raw replay

Original:
Calculate $\frac{dy}{dx}$ for $y = 3\cot (x + 1)$.

[Absent]

Exact raw replay:
Calculate $\frac{dy}{dx}$ for $y = 3\cot (x + 1)$.

- $3\csc (x + 1)$
- $-\csc (x + 1)$
- $\csc^{2} (x + 1)$
- $-3\csc^{2} (x + 1)$
- $3\csc^{2} (x + 1)$

[Absent]

Changed raw (evidence only):
Calculate $\frac{dy}{dx}$ for $y = 6\cot (x + 1)$.

- $6\csc (x + 1)$
- $-\csc (x + 1)$
- $\csc^{2} (x + 1)$
- $-6\csc^{2} (x + 1)$
- $6\csc^{2} (x + 1)$

[Absent]

## q-48640 — Math Academy captured source and raw replay

Original:
Given that $y = \sec (8x^{3} + 1)$, find $\frac{dy}{dx}$.

[Absent]

Exact raw replay:
Given that $y = \sec (8x^{3} + 1)$, find $\frac{dy}{dx}$.

- $(24x^{2} + 1)\sec^{2} (8x^{3} + 1)$
- $(24x^{2} + 1)\sec (8x^{3} + 1)\tan (8x^{3} + 1)$
- $24x^{2}\sec (8x^{3} + 1)\tan (8x^{3} + 1)$
- $24x^{2}\sec^{2} (8x^{3} + 1)\tan (8x^{3} + 1)$
- $24x^{2}\tan (8x^{3} + 1)$

[Absent]

Changed raw (evidence only):
Given that $y = \sec (16x^{3} + 1)$, find $\frac{dy}{dx}$.

- $(48x^{2} + 1)\sec^{2} (16x^{3} + 1)$
- $(48x^{2} + 1)\sec (16x^{3} + 1)\tan (16x^{3} + 1)$
- $48x^{2}\sec (16x^{3} + 1)\tan (16x^{3} + 1)$
- $48x^{2}\sec^{2} (16x^{3} + 1)\tan (16x^{3} + 1)$
- $48x^{2}\tan (16x^{3} + 1)$

[Absent]

## q-31333 — Math Academy captured source and raw replay

Original:
Calculate $\dfrac {\textrm d y}{\textrm d x}$ for $y =8\csc(10x).$

First, we express $y$ as the composite function

\[
y = 8\csc{u}, \qquad u = 10x
\]

Differentiating gives

\[
\dfrac{\textrm d y}{\textrm d u} = -8\csc u \cot u \qquad \style{font-family:inherit;}{\text{and}} \qquad \dfrac{\textrm d u}{\textrm d x} = 10.
\]

We now apply the chain rule, and get

\begin{align*}
\dfrac{\textrm d y}{\textrm d x} & = \dfrac{\textrm d y}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=-8\csc u \cot u \cdot (10)\\[5pt]
&=-80\csc u \cot u \\[5pt]
&=-80\csc (10x) \cot (10x).
\end{align*}

Exact raw replay:
Calculate $\dfrac {\textrm d y}{\textrm d x}$ for $y =8\csc(10x).$



First, we express $y$ as the composite function

\[
y = 8\csc{u}, \qquad u = 10x
\]

Differentiating gives

\[
\dfrac{\textrm d y}{\textrm d u} = -8\csc u \cot u \qquad \style{font-family:inherit;}{\text{and}} \qquad \dfrac{\textrm d u}{\textrm d x} = 10.
\]

We now apply the chain rule, and get

\begin{align*}
\dfrac{\textrm d y}{\textrm d x} & = \dfrac{\textrm d y}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=-8\csc u \cot u \cdot (10)\\[5pt]
&=-80\csc u \cot u \\[5pt]
&=-80\csc (10x) \cot (10x).
\end{align*}

Changed raw (evidence only):
Calculate $\dfrac {\textrm d y}{\textrm d x}$ for $y =16\csc(10x).$



First, we express $y$ as the composite function

\[
y = 16\csc{u}, \qquad u = 10x
\]

Differentiating gives

\[
\dfrac{\textrm d y}{\textrm d u} = -16\csc u \cot u \qquad \style{font-family:inherit;}{\text{and}} \qquad \dfrac{\textrm d u}{\textrm d x} = 10.
\]

We now apply the chain rule, and get

\begin{align*}
\dfrac{\textrm d y}{\textrm d x} & = \dfrac{\textrm d y}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=-16\csc u \cot u \cdot (10)\\[5pt]
&=-160\csc u \cot u \\[5pt]
&=-160\csc (10x) \cot (10x).
\end{align*}

## q-31333 — normal source-family completion or repaired presentation

Normal generated:
Calculate $\dfrac {\textrm d y}{\textrm d x}$ for $y =8\csc(10x).$

$\frac{\mathrm{d}y}{\mathrm{d}x} =$
{{field-1}}

- $- 80 \cot{(10 x )} \csc{(10 x )}$

First, we express $y$ as the composite function

$$
y = 8\csc{u}, \qquad u = 10x
$$

Differentiating gives

$$
\dfrac{\textrm d y}{\textrm d u} = -8\csc u \cot u \qquad \text{and} \qquad \dfrac{\textrm d u}{\textrm d x} = 10.
$$

We now apply the chain rule, and get


$$
\begin{aligned}
\dfrac{\textrm d y}{\textrm d x} & = \dfrac{\textrm d y}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=-8\csc u \cot u \cdot (10)\\[5pt]
&=-80\csc u \cot u \\[5pt]
&=-80\csc (10x) \cot (10x).
\end{aligned}
$$

Normal generated:
Calculate $\dfrac {\textrm d y}{\textrm d x}$ for $y =16\csc(10x).$

$\frac{\mathrm{d}y}{\mathrm{d}x} =$
{{field-1}}

- $- 160 \cot{(10 x )} \csc{(10 x )}$

First, we express $y$ as the composite function

$$
y = 16\csc{u}, \qquad u = 10x
$$

Differentiating gives

$$
\dfrac{\textrm d y}{\textrm d u} = -16\csc u \cot u \qquad \text{and} \qquad \dfrac{\textrm d u}{\textrm d x} = 10.
$$

We now apply the chain rule, and get


$$
\begin{aligned}
\dfrac{\textrm d y}{\textrm d x} & = \dfrac{\textrm d y}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=-16\csc u \cot u \cdot (10)\\[5pt]
&=-160\csc u \cot u \\[5pt]
&=-160\csc (10x) \cot (10x).
\end{aligned}
$$

## q-31341 — Math Academy captured source and raw replay

Original:
Find the slope of the tangent to the curve $y=\cot\left(1-\dfrac x 5 \right)$ at the point where $x =1.$

The slope of $y = f(x)$ at $x=1$ is given by $f'(1).$

We will calculate $f'(x)$ using the chain rule. First, we express $f(x)$ as the composite function

\[
f = \cot{u}, \qquad u = 1-\dfrac x 5.
\]

Differentiating gives

\[
\dfrac{\textrm d f}{\textrm d u} = -\csc^2 u \qquad \text{and}\qquad \dfrac{\textrm d u}{\textrm d x} = -\dfrac{1}{5}.
\]

We now apply the chain rule, and get

\begin{align*}
\dfrac{\textrm d f}{\textrm d x} &= \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=-\csc^2 u \cdot  \left( -\dfrac{1}{5}\right)\\[5pt]
&= \dfrac{1}{5}\csc^2 \left(1-\dfrac{x}{5}\right).
\end{align*}

Evaluating at $x=1,$ we find

\begin{eqnarray}
    \eqalign{

f'(x) & =\dfrac 1 5\csc^2\left(1-\dfrac 1 5 \right) \\[3pt]
	& =\dfrac 1 5\csc^2\left(\dfrac 4 5 \right) .
       
    }
\end{eqnarray}
Therefore, the slope of the tangent to the curve $y = f(x)$ at $x = 1$ is $\dfrac{1}{5}\csc^2\left(\dfrac{4}{5}\right).$

Exact raw replay:
Find the slope of the tangent to the curve $y=\cot\left(1-\dfrac x 5 \right)$ at the point where $x =1.$



The slope of $y = f(x)$ at $x=1$ is given by $f'(1).$

We will calculate $f'(x)$ using the chain rule. First, we express $f(x)$ as the composite function

\[
f = \cot{u}, \qquad u = 1-\dfrac x 5.
\]

Differentiating gives

\[
\dfrac{\textrm d f}{\textrm d u} = -\csc^2 u \qquad \text{and}\qquad \dfrac{\textrm d u}{\textrm d x} = -\dfrac{1}{5}.
\]

We now apply the chain rule, and get

\begin{align*}
\dfrac{\textrm d f}{\textrm d x} &= \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=-\csc^2 u \cdot  \left( -\dfrac{1}{5}\right)\\[5pt]
&= \dfrac{1}{5}\csc^2 \left(1-\dfrac{x}{5}\right).
\end{align*}

Evaluating at $x=1,$ we find

\begin{eqnarray}
    \eqalign{

f'(x) & =\dfrac 1 5\csc^2\left(1-\dfrac 1 5 \right) \\[3pt]
	& =\dfrac 1 5\csc^2\left(\dfrac 4 5 \right) .
       
    }
\end{eqnarray}
Therefore, the slope of the tangent to the curve $y = f(x)$ at $x = 1$ is $\dfrac{1}{5}\csc^2\left(\dfrac{4}{5}\right).$

Changed raw (evidence only):
Find the slope of the tangent to the curve $y=\cot\left(1-\dfrac x 6 \right)$ at the point where $x =1.$



The slope of $y = f(x)$ at $x=1$ is given by $f'(1).$

We will calculate $f'(x)$ using the chain rule. First, we express $f(x)$ as the composite function

\[
f = \cot{u}, \qquad u = 1-\dfrac x 6.
\]

Differentiating gives

\[
\dfrac{\textrm d f}{\textrm d u} = -\csc^2 u \qquad \text{and}\qquad \dfrac{\textrm d u}{\textrm d x} = -\dfrac{1}{6}.
\]

We now apply the chain rule, and get

\begin{align*}
\dfrac{\textrm d f}{\textrm d x} &= \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=-\csc^2 u \cdot  \left( -\dfrac{1}{6}\right)\\[5pt]
&= \dfrac{1}{6}\csc^2 \left(1-\dfrac{x}{6}\right).
\end{align*}

Evaluating at $x=1,$ we find

\begin{eqnarray}
    \eqalign{

f'(x) & =\dfrac 1 6\csc^2\left(1-\dfrac 1 6 \right) \\[3pt]
	& =\dfrac 1 6\csc^2\left(\dfrac 5 6 \right) .
       
    }
\end{eqnarray}
Therefore, the slope of the tangent to the curve $y = f(x)$ at $x = 1$ is $\dfrac{1}{6}\csc^2\left(\dfrac{5}{6}\right).$

## q-31341 — normal source-family completion or repaired presentation

Normal generated:
Find the slope of the tangent to the curve $y=\cot\left(1-\dfrac x 5 \right)$ at the point where $x =1.$

$m =$
{{field-1}}

- $\frac{\csc^{2}{(\frac{4}{5} )}}{5}$

The slope of $y = f(x)$ at $x=1$ is given by $f'(1).$

We will calculate $f'(x)$ using the chain rule. First, we express $f(x)$ as the composite function

$$
f = \cot{u}, \qquad u = 1-\dfrac x 5.
$$

Differentiating gives

$$
\dfrac{\textrm d f}{\textrm d u} = -\csc^2 u \qquad \text{and}\qquad \dfrac{\textrm d u}{\textrm d x} = -\dfrac{1}{5}.
$$

We now apply the chain rule, and get


$$
\begin{aligned}
\dfrac{\textrm d f}{\textrm d x} &= \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=-\csc^2 u \cdot  \left( -\dfrac{1}{5}\right)\\[5pt]
&= \dfrac{1}{5}\csc^2 \left(1-\dfrac{x}{5}\right).
\end{aligned}
$$

Evaluating at $x=1,$ we find


$$
\begin{aligned}

f'(1) & =\dfrac 1 5\csc^2\left(1-\dfrac 1 5 \right) \\[3pt]
	& =\dfrac 1 5\csc^2\left(\dfrac 4 5 \right) .
       
    \end{aligned}
$$
Therefore, the slope of the tangent to the curve $y = f(x)$ at $x = 1$ is $\dfrac{1}{5}\csc^2\left(\dfrac{4}{5}\right).$

Normal generated:
Find the slope of the tangent to the curve $y=\cot\left(1-\dfrac x 6 \right)$ at the point where $x =1.$

$m =$
{{field-1}}

- $\frac{\csc^{2}{(\frac{5}{6} )}}{6}$

The slope of $y = f(x)$ at $x=1$ is given by $f'(1).$

We will calculate $f'(x)$ using the chain rule. First, we express $f(x)$ as the composite function

$$
f = \cot{u}, \qquad u = 1-\dfrac x 6.
$$

Differentiating gives

$$
\dfrac{\textrm d f}{\textrm d u} = -\csc^2 u \qquad \text{and}\qquad \dfrac{\textrm d u}{\textrm d x} = -\dfrac{1}{6}.
$$

We now apply the chain rule, and get


$$
\begin{aligned}
\dfrac{\textrm d f}{\textrm d x} &= \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=-\csc^2 u \cdot  \left( -\dfrac{1}{6}\right)\\[5pt]
&= \dfrac{1}{6}\csc^2 \left(1-\dfrac{x}{6}\right).
\end{aligned}
$$

Evaluating at $x=1,$ we find


$$
\begin{aligned}

f'(1) & =\dfrac 1 6\csc^2\left(1-\dfrac 1 6 \right) \\[3pt]
	& =\dfrac 1 6\csc^2\left(\dfrac 5 6 \right) .
       
    \end{aligned}
$$
Therefore, the slope of the tangent to the curve $y = f(x)$ at $x = 1$ is $\dfrac{1}{6}\csc^2\left(\dfrac{5}{6}\right).$

## q-342405 — Math Academy captured source and raw replay

Original:
Find the slope $m$ of $f(x) = \sec\left(\pi x^{2}\right)$ at $x = \dfrac{1}{2}.$

$m=$
{{field-1}}

First, the slope of $y = f(x)$ at $x = \dfrac{1}{2}$ is given by $f'\left( \dfrac{1}{2} \right).$

We will calculate $f'(x)$ using the chain rule. We express $f(x)$ as the composite function
\[
f = \sec{u}, \qquad u = \pi x^{2}.
\]

Differentiating gives
\[
\dfrac{\textrm d f}{\textrm d u} = \sec{u}\tan{u}, \qquad\dfrac{\textrm d u}{\textrm d x} = 2\pi x.
\]

We now apply the chain rule, and get
\begin{align*}
\dfrac{\textrm d f}{\textrm d x} & = \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]

&= \sec{u}\tan{u} \cdot 2\pi x \\[5pt]

&= 2\pi x \sec{\left(\pi x^{2}\right)}\tan{\left(\pi x^{2}\right)}.
\end{align*}

Evaluating at $x=\dfrac{1}{2}$, we find 
\begin{eqnarray}
 \eqalign{
f'\left( \dfrac{1}{2} \right) &= 2\pi \cdot \dfrac{1}{2}\cdot \sec{\left[\pi\cdot\left(\dfrac{1}{2}\right)^{2}\right]}\tan{\left[\pi\cdot\left(\dfrac{1}{2}\right)^{2}\right]} \\[5pt]
&= \pi \sec{\left(\dfrac{\pi}{4}\right)} \tan{\left(\dfrac{\pi}{4}\right)} \\[5pt]
&= \pi \cdot \sqrt{2}\cdot 1 \\[5pt]
&= \pi\sqrt{2}.}
\end{eqnarray}

Therefore, the slope of $y = f(x)$ at $x=\dfrac{1}{2}$ is $\bbox[4pt, border: 1px solid lightgray]{\pi\sqrt{2}}.$

Exact raw replay:
Find the slope $m$ of $f(x) = \sec\left(\pi x^{2}\right)$ at $x = \dfrac{1}{2}.$

$m=$
{{field-1}}

- $$\pi\sqrt{2}$$

First, the slope of $y = f(x)$ at $x = \dfrac{1}{2}$ is given by $f'\left( \dfrac{1}{2} \right).$

We will calculate $f'(x)$ using the chain rule. We express $f(x)$ as the composite function
\[
f = \sec{u}, \qquad u = \pi x^{2}.
\]

Differentiating gives
\[
\dfrac{\textrm d f}{\textrm d u} = \sec{u}\tan{u}, \qquad\dfrac{\textrm d u}{\textrm d x} = 2\pi x.
\]

We now apply the chain rule, and get
\begin{align*}
\dfrac{\textrm d f}{\textrm d x} & = \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]

&= \sec{u}\tan{u} \cdot 2\pi x \\[5pt]

&= 2\pi x \sec{\left(\pi x^{2}\right)}\tan{\left(\pi x^{2}\right)}.
\end{align*}

Evaluating at $x=\dfrac{1}{2}$, we find 
\begin{eqnarray}
 \eqalign{
f'\left( \dfrac{1}{2} \right) &= 2\pi \cdot \dfrac{1}{2}\cdot \sec{\left[\pi\cdot\left(\dfrac{1}{2}\right)^{2}\right]}\tan{\left[\pi\cdot\left(\dfrac{1}{2}\right)^{2}\right]} \\[5pt]
&= \pi \sec{\left(\dfrac{\pi}{4}\right)} \tan{\left(\dfrac{\pi}{4}\right)} \\[5pt]
&= \pi \cdot \sqrt{2}\cdot 1 \\[5pt]
&= \pi\sqrt{2}.}
\end{eqnarray}

Therefore, the slope of $y = f(x)$ at $x=\dfrac{1}{2}$ is $\bbox[4pt, border: 1px solid lightgray]{\pi\sqrt{2}}.$

Changed raw (evidence only):
Find the slope $m$ of $f(x) = 2\sec\left(\pi x^{2}\right)$ at $x = \dfrac{1}{2}.$

$m=$
{{field-1}}

- $$2\pi\sqrt{2}$$

First, the slope of $y = f(x)$ at $x = \dfrac{1}{2}$ is given by $f'\left( \dfrac{1}{2} \right).$

We will calculate $f'(x)$ using the chain rule. We express $f(x)$ as the composite function
\[
f = 2\sec{u}, \qquad u = \pi x^{2}.
\]

Differentiating gives
\[
\dfrac{\textrm d f}{\textrm d u} = 2\sec{u}\tan{u}, \qquad\dfrac{\textrm d u}{\textrm d x} = 2\pi x.
\]

We now apply the chain rule, and get
\begin{align*}
\dfrac{\textrm d f}{\textrm d x} & = \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]

&= 2\sec{u}\tan{u} \cdot 2\pi x \\[5pt]

&= 2\pi x 2\sec{\left(\pi x^{2}\right)}\tan{\left(\pi x^{2}\right)}.
\end{align*}

Evaluating at $x=\dfrac{1}{2}$, we find 
\begin{eqnarray}
 \eqalign{
f'\left( \dfrac{1}{2} \right) &= 2\pi \cdot \dfrac{1}{2}\cdot 2\sec{\left[\pi\cdot\left(\dfrac{1}{2}\right)^{2}\right]}\tan{\left[\pi\cdot\left(\dfrac{1}{2}\right)^{2}\right]} \\[5pt]
&= \pi 2\sec{\left(\dfrac{\pi}{4}\right)} \tan{\left(\dfrac{\pi}{4}\right)} \\[5pt]
&= 2\pi \cdot \sqrt{2}\cdot 1 \\[5pt]
&= 2\pi\sqrt{2}.}
\end{eqnarray}

Therefore, the slope of $y = f(x)$ at $x=\dfrac{1}{2}$ is $\bbox[4pt, border: 1px solid lightgray]{2\pi\sqrt{2}}.$

## q-342405 — normal source-family completion or repaired presentation

Normal generated:
Find the slope $m$ of $f(x) = \sec\left(\pi x^{2}\right)$ at $x = \dfrac{1}{2}.$

$m=$
{{field-1}}

- $\pi\sqrt{2}$

First, the slope of $y = f(x)$ at $x = \dfrac{1}{2}$ is given by $f'\left( \dfrac{1}{2} \right).$

We will calculate $f'(x)$ using the chain rule. We express $f(x)$ as the composite function
$$
f = \sec{u}, \qquad u = \pi x^{2}.
$$

Differentiating gives
$$
\dfrac{\textrm d f}{\textrm d u} = \sec{u}\tan{u}, \qquad\dfrac{\textrm d u}{\textrm d x} = 2\pi x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}
\dfrac{\textrm d f}{\textrm d x} & = \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]

&= \sec{u}\tan{u} \cdot 2\pi x \\[5pt]

&= 2\pi x \sec{\left(\pi x^{2}\right)}\tan{\left(\pi x^{2}\right)}.
\end{aligned}
$$

Evaluating at $x=\dfrac{1}{2}$, we find 

$$
\begin{aligned}
f'\left( \dfrac{1}{2} \right) &= 2\pi \cdot \dfrac{1}{2}\cdot \sec{\left[\pi\cdot\left(\dfrac{1}{2}\right)^{2}\right]}\tan{\left[\pi\cdot\left(\dfrac{1}{2}\right)^{2}\right]} \\[5pt]
&= \pi \sec{\left(\dfrac{\pi}{4}\right)} \tan{\left(\dfrac{\pi}{4}\right)} \\[5pt]
&= \pi \cdot \sqrt{2}\cdot 1 \\[5pt]
&= \pi\sqrt{2}.\end{aligned}
$$

Therefore, the slope of $y = f(x)$ at $x=\dfrac{1}{2}$ is $\bbox[4pt, border: 1px solid lightgray]{\pi\sqrt{2}}.$

Normal generated:
Find the slope $m$ of $f(x) = 2\sec\left(\pi x^{2}\right)$ at $x = \dfrac{1}{2}.$

$m=$
{{field-1}}

- $2\pi\sqrt{2}$

First, the slope of $y = f(x)$ at $x = \dfrac{1}{2}$ is given by $f'\left( \dfrac{1}{2} \right).$

We will calculate $f'(x)$ using the chain rule. We express $f(x)$ as the composite function
$$
f = 2\sec{u}, \qquad u = \pi x^{2}.
$$

Differentiating gives
$$
\dfrac{\textrm d f}{\textrm d u} = 2\sec{u}\tan{u}, \qquad\dfrac{\textrm d u}{\textrm d x} = 2\pi x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}
\dfrac{\textrm d f}{\textrm d x} & = \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]

&= 2\sec{u}\tan{u} \cdot 2\pi x \\[5pt]

&= 2\pi x 2\sec{\left(\pi x^{2}\right)}\tan{\left(\pi x^{2}\right)}.
\end{aligned}
$$

Evaluating at $x=\dfrac{1}{2}$, we find 

$$
\begin{aligned}
f'\left( \dfrac{1}{2} \right) &= 2\pi \cdot \dfrac{1}{2}\cdot 2\sec{\left[\pi\cdot\left(\dfrac{1}{2}\right)^{2}\right]}\tan{\left[\pi\cdot\left(\dfrac{1}{2}\right)^{2}\right]} \\[5pt]
&= \pi 2\sec{\left(\dfrac{\pi}{4}\right)} \tan{\left(\dfrac{\pi}{4}\right)} \\[5pt]
&= 2\pi \cdot \sqrt{2}\cdot 1 \\[5pt]
&= 2\pi\sqrt{2}.\end{aligned}
$$

Therefore, the slope of $y = f(x)$ at $x=\dfrac{1}{2}$ is $\bbox[4pt, border: 1px solid lightgray]{2\pi\sqrt{2}}.$

## q-342412 — Math Academy captured source and raw replay

Original:
Find the equation of the tangent to the curve $f(x) = \csc{\left(\dfrac{\pi x^{3}}{6}\right)}$ at the point $(1,2).$

$y =$
{{field-1}}$x \: + \:$
{{field-2}}

First, the slope of $y = f(x)$ at $x = 1$ is given by $f'(1).$

We will calculate $f'(x)$ using the chain rule. First, we express $f(x)$ as the composite function
\[
f = \csc{u}, \qquad u = \dfrac{\pi x^{3}}{6}.
\]

Differentiating gives
\[
\dfrac{\textrm d f}{\textrm d u} = -\csc{u}\cot{u}  \qquad \text{and} \qquad \dfrac{\textrm d u}{\textrm d x} = \dfrac{\pi}{2} x^{2}.
\]

We now apply the chain rule, and get
\begin{align*}
\dfrac{\textrm d f}{\textrm d x} &= \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=\left(-\csc{u}\cot{u}\right) \cdot \dfrac{\pi}{2} x^{2} \\[5pt]
&= -\dfrac{\pi}{2} x^{2} \csc{\left(\dfrac{\pi x^{3}}{6}\right)\cot{\left(\dfrac{\pi x^{3}}{6}\right)}}.
\end{align*}

Evaluating at $x=1,$ we find
\begin{align}
m=f'(1)& =-\dfrac{\pi}{2} \cdot 1^2 \cdot \csc{\left(\dfrac{\pi}{6}\right)\cot{\left(\dfrac{\pi}{6}\right)}} \\[5pt] 

&= -\dfrac{\pi}{2} \cdot 2 \cdot \sqrt{3} \\[5pt]

& = -\pi\sqrt{3}.
\end{align}

Finally, we find the equation of the tangent at the point $\left(1,2\right) \mathbin{:}$

\begin{align*}
y-y_1 &= m(x-x_1)\\[5pt]

y-2 &= -\pi\sqrt{3}(x-1)\\[5pt]

y &= \bbox[4pt, border: 1px solid lightgray]{-\pi\sqrt{3}}x + \bbox[4pt, border: 1px solid lightgray]{\pi\sqrt{3} + 2}
\end{align*}

Exact raw replay:
Find the equation of the tangent to the curve $f(x) = \csc{\left(\dfrac{\pi x^{3}}{6}\right)}$ at the point $(1,2).$

$y =$
{{field-1}}$x \: + \:$
{{field-2}}

- $$-\pi\sqrt{3}$$
- $$\pi\sqrt{3}+2$$

First, the slope of $y = f(x)$ at $x = 1$ is given by $f'(1).$

We will calculate $f'(x)$ using the chain rule. First, we express $f(x)$ as the composite function
\[
f = \csc{u}, \qquad u = \dfrac{\pi x^{3}}{6}.
\]

Differentiating gives
\[
\dfrac{\textrm d f}{\textrm d u} = -\csc{u}\cot{u}  \qquad \text{and} \qquad \dfrac{\textrm d u}{\textrm d x} = \dfrac{\pi}{2} x^{2}.
\]

We now apply the chain rule, and get
\begin{align*}
\dfrac{\textrm d f}{\textrm d x} &= \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=\left(-\csc{u}\cot{u}\right) \cdot \dfrac{\pi}{2} x^{2} \\[5pt]
&= -\dfrac{\pi}{2} x^{2} \csc{\left(\dfrac{\pi x^{3}}{6}\right)\cot{\left(\dfrac{\pi x^{3}}{6}\right)}}.
\end{align*}

Evaluating at $x=1,$ we find
\begin{align}
m=f'(1)& =-\dfrac{\pi}{2} \cdot 1^2 \cdot \csc{\left(\dfrac{\pi}{6}\right)\cot{\left(\dfrac{\pi}{6}\right)}} \\[5pt] 

&= -\dfrac{\pi}{2} \cdot 2 \cdot \sqrt{3} \\[5pt]

& = -\pi\sqrt{3}.
\end{align}

Finally, we find the equation of the tangent at the point $\left(1,2\right) \mathbin{:}$

\begin{align*}
y-y_1 &= m(x-x_1)\\[5pt]

y-2 &= -\pi\sqrt{3}(x-1)\\[5pt]

y &= \bbox[4pt, border: 1px solid lightgray]{-\pi\sqrt{3}}x + \bbox[4pt, border: 1px solid lightgray]{\pi\sqrt{3} + 2}
\end{align*}

Changed raw (evidence only):
Find the equation of the tangent to the curve $f(x) = 2\csc{\left(\dfrac{\pi x^{3}}{6}\right)}$ at the point $(1,4).$

$y =$
{{field-1}}$x \: + \:$
{{field-2}}

- $$-2\pi\sqrt{3}$$
- $$2\pi\sqrt{3}+4$$

First, the slope of $y = f(x)$ at $x = 1$ is given by $f'(1).$

We will calculate $f'(x)$ using the chain rule. First, we express $f(x)$ as the composite function
\[
f = 2\csc{u}, \qquad u = \dfrac{\pi x^{3}}{6}.
\]

Differentiating gives
\[
\dfrac{\textrm d f}{\textrm d u} = -2\csc{u}\cot{u}  \qquad \text{and} \qquad \dfrac{\textrm d u}{\textrm d x} = \dfrac{\pi}{2} x^{2}.
\]

We now apply the chain rule, and get
\begin{align*}
\dfrac{\textrm d f}{\textrm d x} &= \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=\left(-2\csc{u}\cot{u}\right) \cdot \dfrac{\pi}{2} x^{2} \\[5pt]
&= -\dfrac{\pi}{2} x^{2} 2\csc{\left(\dfrac{\pi x^{3}}{6}\right)\cot{\left(\dfrac{\pi x^{3}}{6}\right)}}.
\end{align*}

Evaluating at $x=1,$ we find
\begin{align}
m=f'(1)& =-\dfrac{\pi}{2} \cdot 1^2 \cdot 2\csc{\left(\dfrac{\pi}{6}\right)\cot{\left(\dfrac{\pi}{6}\right)}} \\[5pt] 

&= -\dfrac{\pi}{2} \cdot 4 \cdot \sqrt{3} \\[5pt]

& = -2\pi\sqrt{3}.
\end{align}

Finally, we find the equation of the tangent at the point $\left(1,4\right) \mathbin{:}$

\begin{align*}
y-y_1 &= m(x-x_1)\\[5pt]

y-4 &= -2\pi\sqrt{3}(x-1)\\[5pt]

y &= \bbox[4pt, border: 1px solid lightgray]{-2\pi\sqrt{3}}x + \bbox[4pt, border: 1px solid lightgray]{2\pi\sqrt{3} + 4}
\end{align*}

## q-342412 — normal source-family completion or repaired presentation

Normal generated:
Find the equation of the tangent to the curve $f(x) = \csc{\left(\dfrac{\pi x^{3}}{6}\right)}$ at the point $(1,2).$

$y =$
{{field-1}}$x \: + \:$
{{field-2}}

- $-\pi\sqrt{3}$
- $\pi\sqrt{3}+2$

First, the slope of $y = f(x)$ at $x = 1$ is given by $f'(1).$

We will calculate $f'(x)$ using the chain rule. First, we express $f(x)$ as the composite function
$$
f = \csc{u}, \qquad u = \dfrac{\pi x^{3}}{6}.
$$

Differentiating gives
$$
\dfrac{\textrm d f}{\textrm d u} = -\csc{u}\cot{u}  \qquad \text{and} \qquad \dfrac{\textrm d u}{\textrm d x} = \dfrac{\pi}{2} x^{2}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}
\dfrac{\textrm d f}{\textrm d x} &= \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=\left(-\csc{u}\cot{u}\right) \cdot \dfrac{\pi}{2} x^{2} \\[5pt]
&= -\dfrac{\pi}{2} x^{2} \csc{\left(\dfrac{\pi x^{3}}{6}\right)}\cot{\left(\dfrac{\pi x^{3}}{6}\right)}.
\end{aligned}
$$

Evaluating at $x=1,$ we find

$$
\begin{aligned}
m=f'(1)& =-\dfrac{\pi}{2} \cdot 1^2 \cdot \csc{\left(\dfrac{\pi}{6}\right)}\cot{\left(\dfrac{\pi}{6}\right)} \\[5pt] 

&= -\dfrac{\pi}{2} \cdot 2 \cdot \sqrt{3} \\[5pt]

& = -\pi\sqrt{3}.
\end{aligned}
$$

Finally, we find the equation of the tangent at the point $\left(1,2\right) \mathbin{:}$


$$
\begin{aligned}
y-y_1 &= m(x-x_1)\\[5pt]

y-2 &= -\pi\sqrt{3}(x-1)\\[5pt]

y &= \bbox[4pt, border: 1px solid lightgray]{-\pi\sqrt{3}}x + \bbox[4pt, border: 1px solid lightgray]{\pi\sqrt{3} + 2}
\end{aligned}
$$

Normal generated:
Find the equation of the tangent to the curve $f(x) = 2\csc{\left(\dfrac{\pi x^{3}}{6}\right)}$ at the point $(1,4).$

$y =$
{{field-1}}$x \: + \:$
{{field-2}}

- $-2\pi\sqrt{3}$
- $2\pi\sqrt{3}+4$

First, the slope of $y = f(x)$ at $x = 1$ is given by $f'(1).$

We will calculate $f'(x)$ using the chain rule. First, we express $f(x)$ as the composite function
$$
f = 2\csc{u}, \qquad u = \dfrac{\pi x^{3}}{6}.
$$

Differentiating gives
$$
\dfrac{\textrm d f}{\textrm d u} = -2\csc{u}\cot{u}  \qquad \text{and} \qquad \dfrac{\textrm d u}{\textrm d x} = \dfrac{\pi}{2} x^{2}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}
\dfrac{\textrm d f}{\textrm d x} &= \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=\left(-2\csc{u}\cot{u}\right) \cdot \dfrac{\pi}{2} x^{2} \\[5pt]
&= -\dfrac{\pi}{2} x^{2} 2\csc{\left(\dfrac{\pi x^{3}}{6}\right)}\cot{\left(\dfrac{\pi x^{3}}{6}\right)}.
\end{aligned}
$$

Evaluating at $x=1,$ we find

$$
\begin{aligned}
m=f'(1)& =-\dfrac{\pi}{2} \cdot 1^2 \cdot 2\csc{\left(\dfrac{\pi}{6}\right)}\cot{\left(\dfrac{\pi}{6}\right)} \\[5pt] 

&= -\dfrac{\pi}{2} \cdot 4 \cdot \sqrt{3} \\[5pt]

& = -2\pi\sqrt{3}.
\end{aligned}
$$

Finally, we find the equation of the tangent at the point $\left(1,4\right) \mathbin{:}$


$$
\begin{aligned}
y-y_1 &= m(x-x_1)\\[5pt]

y-4 &= -2\pi\sqrt{3}(x-1)\\[5pt]

y &= \bbox[4pt, border: 1px solid lightgray]{-2\pi\sqrt{3}}x + \bbox[4pt, border: 1px solid lightgray]{2\pi\sqrt{3} + 4}
\end{aligned}
$$

## q-48510 — Math Academy captured source and raw replay

Original:
Find the equation of the tangent to the curve $y=\sec(3x)-2x$ at the point $\left(0,1\right).$

Let $g(x)=\sec(3x )$ and $h(x)=-2x.$ Then,

\begin{align}
f(x)&=g(x)+h(x) . 
\end{align}

First, we differentiate $g(x).$ We express $g(x)=\sec(3x)$ as the composite function
\[
g = \sec u, \qquad u = 3x.
\]

Differentiating gives

\[
\dfrac{\textrm d g}{\textrm d u} = \sec u \tan u \qquad \text{and} \qquad \dfrac{\textrm{d}u}{\textrm d x} = 3.
\]

We now apply the chain rule, and we get
\[
	\eqalign{
\require{cancel}
			\dfrac{\textrm{d}g}{\textrm{d}x}&=\dfrac{\textrm{d}g}{\textrm{d}u}\cdot \dfrac{\textrm{d}u}{\textrm{d}x}\\[5pt]
									&=\sec u \tan u \cdot (3)\\[5pt]
									&=3 \sec u \tan u\\[5pt]
                                                                        & =3\sec (3x) \tan (3x)
}

\]

Next, we differentiate $h(x)=-2x.$ 

Differentiating gives

\[
\dfrac{\textrm d h}{\textrm d x} = -2
\]

Hence,
\[f'(x)=g'(x)+h'(x)=3\sec (3x) \tan (3x) -2.\]

Evaluating at $x=0,$ we find

\begin{align*}
m=f'(0) & =3\sec\left(3\cdot 0\right)\tan\left(3\cdot 0\right) -2\\[3pt]
	& =3\sec 0\tan 0 -2\\[3pt]
	& =3\cdot 1\cdot 0 - 2\\[3pt]
	&=-2.       
\end{align*}

Finally, we find the equation of the tangent at the point $(0,1) \mathbin{:}$

\begin{align}
y-y_1&=m(x-x_1)\\[3pt]
y-1&=-2 \left(x-0 \right)\\[3pt]
y-1&=-2x\\[3pt]
y&=-2x+1.
\end{align}

Exact raw replay:
Find the equation of the tangent to the curve $y=\sec(3x)-2x$ at the point $\left(0,1\right).$



Let $g(x)=\sec(3x )$ and $h(x)=-2x.$ Then,

\begin{align}
f(x)&=g(x)+h(x) . 
\end{align}

First, we differentiate $g(x).$ We express $g(x)=\sec(3x)$ as the composite function
\[
g = \sec u, \qquad u = 3x.
\]

Differentiating gives

\[
\dfrac{\textrm d g}{\textrm d u} = \sec u \tan u \qquad \text{and} \qquad \dfrac{\textrm{d}u}{\textrm d x} = 3.
\]

We now apply the chain rule, and we get
\[
	\eqalign{
\require{cancel}
			\dfrac{\textrm{d}g}{\textrm{d}x}&=\dfrac{\textrm{d}g}{\textrm{d}u}\cdot \dfrac{\textrm{d}u}{\textrm{d}x}\\[5pt]
									&=\sec u \tan u \cdot (3)\\[5pt]
									&=3 \sec u \tan u\\[5pt]
                                                                        & =3\sec (3x) \tan (3x)
}

\]

Next, we differentiate $h(x)=-2x.$ 

Differentiating gives

\[
\dfrac{\textrm d h}{\textrm d x} = -2
\]

Hence,
\[f'(x)=g'(x)+h'(x)=3\sec (3x) \tan (3x) -2.\]

Evaluating at $x=0,$ we find

\begin{align*}
m=f'(0) & =3\sec\left(3\cdot 0\right)\tan\left(3\cdot 0\right) -2\\[3pt]
	& =3\sec 0\tan 0 -2\\[3pt]
	& =3\cdot 1\cdot 0 - 2\\[3pt]
	&=-2.       
\end{align*}

Finally, we find the equation of the tangent at the point $(0,1) \mathbin{:}$

\begin{align}
y-y_1&=m(x-x_1)\\[3pt]
y-1&=-2 \left(x-0 \right)\\[3pt]
y-1&=-2x\\[3pt]
y&=-2x+1.
\end{align}

Changed raw (evidence only):
Find the equation of the tangent to the curve $y=\sec(3x)-3x$ at the point $\left(0,1\right).$



Let $g(x)=\sec(3x )$ and $h(x)=-3x.$ Then,

\begin{align}
f(x)&=g(x)+h(x) . 
\end{align}

First, we differentiate $g(x).$ We express $g(x)=\sec(3x)$ as the composite function
\[
g = \sec u, \qquad u = 3x.
\]

Differentiating gives

\[
\dfrac{\textrm d g}{\textrm d u} = \sec u \tan u \qquad \text{and} \qquad \dfrac{\textrm{d}u}{\textrm d x} = 3.
\]

We now apply the chain rule, and we get
\[
	\eqalign{
\require{cancel}
			\dfrac{\textrm{d}g}{\textrm{d}x}&=\dfrac{\textrm{d}g}{\textrm{d}u}\cdot \dfrac{\textrm{d}u}{\textrm{d}x}\\[5pt]
									&=\sec u \tan u \cdot (3)\\[5pt]
									&=3 \sec u \tan u\\[5pt]
                                                                        & =3\sec (3x) \tan (3x)
}

\]

Next, we differentiate $h(x)=-3x.$ 

Differentiating gives

\[
\dfrac{\textrm d h}{\textrm d x} = -3
\]

Hence,
\[f'(x)=g'(x)+h'(x)=3\sec (3x) \tan (3x) -3.\]

Evaluating at $x=0,$ we find

\begin{align*}
m=f'(0) & =3\sec\left(3\cdot 0\right)\tan\left(3\cdot 0\right) -3\\[3pt]
	& =3\sec 0\tan 0 -3\\[3pt]
	& =3\cdot 1\cdot 0 - 3\\[3pt]
	&=-3.       
\end{align*}

Finally, we find the equation of the tangent at the point $(0,1) \mathbin{:}$

\begin{align}
y-y_1&=m(x-x_1)\\[3pt]
y-1&=-3 \left(x-0 \right)\\[3pt]
y-1&=-3x\\[3pt]
y&=-3x+1.
\end{align}

## q-48510 — normal source-family completion or repaired presentation

Normal generated:
Find the equation of the tangent to the curve $y=\sec(3x)-2x$ at the point $\left(0,1\right).$

$y =$
{{field-1}}

- $1 - 2 x$

Let $g(x)=\sec(3x )$ and $h(x)=-2x.$ Then,


$$
\begin{aligned}
f(x)&=g(x)+h(x) . 
\end{aligned}
$$

First, we differentiate $g(x).$ We express $g(x)=\sec(3x)$ as the composite function
$$
g = \sec u, \qquad u = 3x.
$$

Differentiating gives

$$
\dfrac{\textrm d g}{\textrm d u} = \sec u \tan u \qquad \text{and} \qquad \dfrac{\textrm{d}u}{\textrm d x} = 3.
$$

We now apply the chain rule, and we get
$$
\begin{aligned}
\require{cancel}
			\dfrac{\textrm{d}g}{\textrm{d}x}&=\dfrac{\textrm{d}g}{\textrm{d}u}\cdot \dfrac{\textrm{d}u}{\textrm{d}x}\\[5pt]
									&=\sec u \tan u \cdot (3)\\[5pt]
									&=3 \sec u \tan u\\[5pt]
                                                                        & =3\sec (3x) \tan (3x)
\end{aligned}
$$

Next, we differentiate $h(x)=-2x.$ 

Differentiating gives

$$
\dfrac{\textrm d h}{\textrm d x} = -2
$$

Hence,
$$
f'(x)=g'(x)+h'(x)=3\sec (3x) \tan (3x) -2.
$$

Evaluating at $x=0,$ we find


$$
\begin{aligned}
m=f'(0) & =3\sec\left(3\cdot 0\right)\tan\left(3\cdot 0\right) -2\\[3pt]
	& =3\sec 0\tan 0 -2\\[3pt]
	& =3\cdot 1\cdot 0 - 2\\[3pt]
	&=-2.       
\end{aligned}
$$

Finally, we find the equation of the tangent at the point $(0,1) \mathbin{:}$


$$
\begin{aligned}
y-y_1&=m(x-x_1)\\[3pt]
y-1&=-2 \left(x-0 \right)\\[3pt]
y-1&=-2x\\[3pt]
y&=-2x+1.
\end{aligned}
$$

Normal generated:
Find the equation of the tangent to the curve $y=\sec(3x)-3x$ at the point $\left(0,1\right).$

$y =$
{{field-1}}

- $1 - 3 x$

Let $g(x)=\sec(3x )$ and $h(x)=-3x.$ Then,


$$
\begin{aligned}
f(x)&=g(x)+h(x) . 
\end{aligned}
$$

First, we differentiate $g(x).$ We express $g(x)=\sec(3x)$ as the composite function
$$
g = \sec u, \qquad u = 3x.
$$

Differentiating gives

$$
\dfrac{\textrm d g}{\textrm d u} = \sec u \tan u \qquad \text{and} \qquad \dfrac{\textrm{d}u}{\textrm d x} = 3.
$$

We now apply the chain rule, and we get
$$
\begin{aligned}
\require{cancel}
			\dfrac{\textrm{d}g}{\textrm{d}x}&=\dfrac{\textrm{d}g}{\textrm{d}u}\cdot \dfrac{\textrm{d}u}{\textrm{d}x}\\[5pt]
									&=\sec u \tan u \cdot (3)\\[5pt]
									&=3 \sec u \tan u\\[5pt]
                                                                        & =3\sec (3x) \tan (3x)
\end{aligned}
$$

Next, we differentiate $h(x)=-3x.$ 

Differentiating gives

$$
\dfrac{\textrm d h}{\textrm d x} = -3
$$

Hence,
$$
f'(x)=g'(x)+h'(x)=3\sec (3x) \tan (3x) -3.
$$

Evaluating at $x=0,$ we find


$$
\begin{aligned}
m=f'(0) & =3\sec\left(3\cdot 0\right)\tan\left(3\cdot 0\right) -3\\[3pt]
	& =3\sec 0\tan 0 -3\\[3pt]
	& =3\cdot 1\cdot 0 - 3\\[3pt]
	&=-3.       
\end{aligned}
$$

Finally, we find the equation of the tangent at the point $(0,1) \mathbin{:}$


$$
\begin{aligned}
y-y_1&=m(x-x_1)\\[3pt]
y-1&=-3 \left(x-0 \right)\\[3pt]
y-1&=-3x\\[3pt]
y&=-3x+1.
\end{aligned}
$$

## q-310222 — Math Academy captured source and raw replay

Original:
Given that $f(x)=\operatorname{cot}⁡(2{x}^{3}),$ we have

${f}^{′}(x)=$

{{field-1}}.

First, we express $f(x)$ as the composite function

$$
y=\operatorname{cot}⁡u,\,u=2{x}^{3}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=6{x}^{2}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot 6{x}^{2} \\  & =-6{x}^{2}{csc}^{2}⁡(2{x}^{3}).\end{aligned}
$$

Exact raw replay:
Given that $f(x)=\operatorname{cot}⁡(2{x}^{3}),$ we have

${f}^{′}(x)=$

{{field-1}}.

- $-6{x}^{2}{csc}^{2}(2{x}^{3})$

First, we express $f(x)$ as the composite function

$$
y=\operatorname{cot}⁡u,\,u=2{x}^{3}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=6{x}^{2}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot 6{x}^{2} \\  & =-6{x}^{2}{csc}^{2}⁡(2{x}^{3}).\end{aligned}
$$

Changed raw (evidence only):
Given that $f(x)=\operatorname{cot}⁡(4{x}^{3}),$ we have

${f}^{′}(x)=$

{{field-1}}.

- $-12{x}^{2}{csc}^{2}(4{x}^{3})$

First, we express $f(x)$ as the composite function

$$
y=\operatorname{cot}⁡u,\,u=4{x}^{3}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=12{x}^{2}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot 12{x}^{2} \\  & =-12{x}^{2}{csc}^{2}⁡(4{x}^{3}).\end{aligned}
$$

## q-310222 — normal source-family completion or repaired presentation

Normal generated:
Given that $f(x)=\operatorname{cot}⁡(2{x}^{3}),$ we have

${f}^{′}(x)=$

{{field-1}}.

- $-6{x}^{2}{csc}^{2}(2{x}^{3})$

First, we express $f(x)$ as the composite function

$$
y=\operatorname{cot}⁡u,\,u=2{x}^{3}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=6{x}^{2}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot 6{x}^{2} \\  & =-6{x}^{2}{csc}^{2}⁡(2{x}^{3}).\end{aligned}
$$

Normal generated:
Given that $f(x)=\operatorname{cot}⁡(4{x}^{3}),$ we have

${f}^{′}(x)=$

{{field-1}}.

- $-12{x}^{2}{csc}^{2}(4{x}^{3})$

First, we express $f(x)$ as the composite function

$$
y=\operatorname{cot}⁡u,\,u=4{x}^{3}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=12{x}^{2}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot 12{x}^{2} \\  & =-12{x}^{2}{csc}^{2}⁡(4{x}^{3}).\end{aligned}
$$

## q-31320 — Math Academy captured source and raw replay

Original:
Calculate $\frac{\text{d}y}{\text{d}x}$ for $y=\operatorname{sec}⁡(2x-1).$

First, we express $y$ as the composite function

$$
y=\operatorname{sec}⁡u,\,u=2x-1.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\operatorname{sec}⁡u\operatorname{tan}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=2.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\operatorname{sec}⁡u\operatorname{tan}⁡u\cdot 2 \\  & =2\operatorname{sec}⁡u\operatorname{tan}⁡u \\  & =2\operatorname{sec}⁡(2x-1)\operatorname{tan}⁡(2x-1).\end{aligned}
$$

Exact raw replay:
Calculate $\frac{\text{d}y}{\text{d}x}$ for $y=\operatorname{sec}⁡(2x-1).$

- $-2\operatorname{sec}⁡(2x-1)\operatorname{tan}⁡(2x-1)$
- $-2\operatorname{csc}⁡(2x-1)\operatorname{tan}⁡(2x-1)$
- $\operatorname{sec}⁡(2x-1)\operatorname{tan}⁡(2x-1)$
- $2\operatorname{sec}⁡(2x-1)\operatorname{tan}⁡(2x-1)$
- $-2\operatorname{sec}⁡(x)\operatorname{tan}⁡(x)$

First, we express $y$ as the composite function

$$
y=\operatorname{sec}⁡u,\,u=2x-1.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\operatorname{sec}⁡u\operatorname{tan}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=2.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\operatorname{sec}⁡u\operatorname{tan}⁡u\cdot 2 \\  & =2\operatorname{sec}⁡u\operatorname{tan}⁡u \\  & =2\operatorname{sec}⁡(2x-1)\operatorname{tan}⁡(2x-1).\end{aligned}
$$

Changed raw (evidence only):
Calculate $\frac{\text{d}y}{\text{d}x}$ for $y=\operatorname{sec}⁡(4x-1).$

- $-4\operatorname{sec}⁡(4x-1)\operatorname{tan}⁡(4x-1)$
- $-4\operatorname{csc}⁡(4x-1)\operatorname{tan}⁡(4x-1)$
- $\operatorname{sec}⁡(4x-1)\operatorname{tan}⁡(4x-1)$
- $4\operatorname{sec}⁡(4x-1)\operatorname{tan}⁡(4x-1)$
- $-4\operatorname{sec}⁡(x)\operatorname{tan}⁡(x)$

First, we express $y$ as the composite function

$$
y=\operatorname{sec}⁡u,\,u=4x-1.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\operatorname{sec}⁡u\operatorname{tan}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=4.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\operatorname{sec}⁡u\operatorname{tan}⁡u\cdot 4 \\  & =4\operatorname{sec}⁡u\operatorname{tan}⁡u \\  & =4\operatorname{sec}⁡(4x-1)\operatorname{tan}⁡(4x-1).\end{aligned}
$$

## q-31320 — normal source-family completion or repaired presentation

Normal generated:
Calculate $\frac{\text{d}y}{\text{d}x}$ for $y=\operatorname{sec}⁡(2x-1).$

- $-2\operatorname{sec}⁡(2x-1)\operatorname{tan}⁡(2x-1)$
- $-2\operatorname{csc}⁡(2x-1)\operatorname{tan}⁡(2x-1)$
- $\operatorname{sec}⁡(2x-1)\operatorname{tan}⁡(2x-1)$
- $2\operatorname{sec}⁡(2x-1)\operatorname{tan}⁡(2x-1)$
- $-2\operatorname{sec}⁡(x)\operatorname{tan}⁡(x)$

First, we express $y$ as the composite function

$$
y=\operatorname{sec}⁡u,\,u=2x-1.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\operatorname{sec}⁡u\operatorname{tan}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=2.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\operatorname{sec}⁡u\operatorname{tan}⁡u\cdot 2 \\  & =2\operatorname{sec}⁡u\operatorname{tan}⁡u \\  & =2\operatorname{sec}⁡(2x-1)\operatorname{tan}⁡(2x-1).\end{aligned}
$$

Normal generated:
Calculate $\frac{\text{d}y}{\text{d}x}$ for $y=\operatorname{sec}⁡(4x-1).$

- $-4\operatorname{sec}⁡(4x-1)\operatorname{tan}⁡(4x-1)$
- $-4\operatorname{csc}⁡(4x-1)\operatorname{tan}⁡(4x-1)$
- $\operatorname{sec}⁡(4x-1)\operatorname{tan}⁡(4x-1)$
- $4\operatorname{sec}⁡(4x-1)\operatorname{tan}⁡(4x-1)$
- $-4\operatorname{sec}⁡(x)\operatorname{tan}⁡(x)$

First, we express $y$ as the composite function

$$
y=\operatorname{sec}⁡u,\,u=4x-1.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\operatorname{sec}⁡u\operatorname{tan}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=4.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\operatorname{sec}⁡u\operatorname{tan}⁡u\cdot 4 \\  & =4\operatorname{sec}⁡u\operatorname{tan}⁡u \\  & =4\operatorname{sec}⁡(4x-1)\operatorname{tan}⁡(4x-1).\end{aligned}
$$

## q-31338 — Math Academy captured source and raw replay

Original:
Find the slope of $f(x)=\operatorname{cot}⁡(2\pi -3x)$ at $x=\frac{\pi }{2}.$

The slope of $y=f(x)$ at $x=\frac{\pi }{2}$ is given by ${f}^{′}(\frac{\pi }{2}).$

We will calculate ${f}^{′}(x)$ using the chain rule. First, we express $f(x)$ as the composite function

$$
f=\operatorname{cot}⁡u,\,u=2\pi -3x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=-{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=-3.
$$

We now apply the chain rule, and get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}f}{\text{d}x}=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot (-3) \\  & =3{csc}^{2}⁡(2\pi -3x).\end{aligned}
$$

Evaluating at $x=\frac{\pi }{2},$ we find

$$
\begin{aligned}\begin{aligned}{f}^{′}(\frac{\pi }{2}) & =3{csc}^{2}⁡(2\pi -\frac{3\pi }{2}) \\  & =3{csc}^{2}⁡(\frac{\pi }{2}) \\  & =3\cdot {1}^{2} \\  & =3.\end{aligned}\end{aligned}
$$

Therefore, the slope of $y=f(x)$ at $x=\frac{\pi }{2}$ is $3.$

Exact raw replay:
Find the slope of $f(x)=\operatorname{cot}⁡(2\pi -3x)$ at $x=\frac{\pi }{2}.$

- $-3$
- $3$
- $\frac{\pi }{2}$
- $-1$
- $1$

The slope of $y=f(x)$ at $x=\frac{\pi }{2}$ is given by ${f}^{′}(\frac{\pi }{2}).$

We will calculate ${f}^{′}(x)$ using the chain rule. First, we express $f(x)$ as the composite function

$$
f=\operatorname{cot}⁡u,\,u=2\pi -3x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=-{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=-3.
$$

We now apply the chain rule, and get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}f}{\text{d}x}=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot (-3) \\  & =3{csc}^{2}⁡(2\pi -3x).\end{aligned}
$$

Evaluating at $x=\frac{\pi }{2},$ we find

$$
\begin{aligned}\begin{aligned}{f}^{′}(\frac{\pi }{2}) & =3{csc}^{2}⁡(2\pi -\frac{3\pi }{2}) \\  & =3{csc}^{2}⁡(\frac{\pi }{2}) \\  & =3\cdot {1}^{2} \\  & =3.\end{aligned}\end{aligned}
$$

Therefore, the slope of $y=f(x)$ at $x=\frac{\pi }{2}$ is $3.$

Changed raw (evidence only):
Find the slope of $f(x)=\operatorname{cot}⁡(3\pi -4x)$ at $x=\frac{5\pi }{8}.$

- $-4$
- $4$
- $\frac{5\pi }{8}$
- $-1$
- $1$

The slope of $y=f(x)$ at $x=\frac{5\pi }{8}$ is given by ${f}^{′}(\frac{5\pi }{8}).$

We will calculate ${f}^{′}(x)$ using the chain rule. First, we express $f(x)$ as the composite function

$$
f=\operatorname{cot}⁡u,\,u=3\pi -4x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=-{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=-4.
$$

We now apply the chain rule, and get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}f}{\text{d}x}=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot (-4) \\  & =4{csc}^{2}⁡(3\pi -4x).\end{aligned}
$$

Evaluating at $x=\frac{5\pi }{8},$ we find

$$
\begin{aligned}\begin{aligned}{f}^{′}(\frac{5\pi }{8}) & =4{csc}^{2}⁡(3\pi -\frac{5\pi }{2}) \\  & =4{csc}^{2}⁡(\frac{\pi }{2}) \\  & =4\cdot {1}^{2} \\  & =4.\end{aligned}\end{aligned}
$$

Therefore, the slope of $y=f(x)$ at $x=\frac{5\pi }{8}$ is $4.$

## q-31338 — normal source-family completion or repaired presentation

Normal generated:
Find the slope of $f(x)=\operatorname{cot}⁡(2\pi -3x)$ at $x=\frac{\pi }{2}.$

- $-3$
- $3$
- $\frac{\pi }{2}$
- $-1$
- $1$

The slope of $y=f(x)$ at $x=\frac{\pi }{2}$ is given by ${f}^{′}(\frac{\pi }{2}).$

We will calculate ${f}^{′}(x)$ using the chain rule. First, we express $f(x)$ as the composite function

$$
f=\operatorname{cot}⁡u,\,u=2\pi -3x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=-{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=-3.
$$

We now apply the chain rule, and get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}f}{\text{d}x}=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot (-3) \\  & =3{csc}^{2}⁡(2\pi -3x).\end{aligned}
$$

Evaluating at $x=\frac{\pi }{2},$ we find

$$
\begin{aligned}\begin{aligned}{f}^{′}(\frac{\pi }{2}) & =3{csc}^{2}⁡(2\pi -\frac{3\pi }{2}) \\  & =3{csc}^{2}⁡(\frac{\pi }{2}) \\  & =3\cdot {1}^{2} \\  & =3.\end{aligned}\end{aligned}
$$

Therefore, the slope of $y=f(x)$ at $x=\frac{\pi }{2}$ is $3.$

Normal generated:
Find the slope of $f(x)=\operatorname{cot}⁡(3\pi -4x)$ at $x=\frac{5\pi }{8}.$

- $-4$
- $4$
- $\frac{5\pi }{8}$
- $-1$
- $1$

The slope of $y=f(x)$ at $x=\frac{5\pi }{8}$ is given by ${f}^{′}(\frac{5\pi }{8}).$

We will calculate ${f}^{′}(x)$ using the chain rule. First, we express $f(x)$ as the composite function

$$
f=\operatorname{cot}⁡u,\,u=3\pi -4x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=-{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=-4.
$$

We now apply the chain rule, and get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}f}{\text{d}x}=\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot (-4) \\  & =4{csc}^{2}⁡(3\pi -4x).\end{aligned}
$$

Evaluating at $x=\frac{5\pi }{8},$ we find

$$
\begin{aligned}\begin{aligned}{f}^{′}(\frac{5\pi }{8}) & =4{csc}^{2}⁡(3\pi -\frac{5\pi }{2}) \\  & =4{csc}^{2}⁡(\frac{\pi }{2}) \\  & =4\cdot {1}^{2} \\  & =4.\end{aligned}\end{aligned}
$$

Therefore, the slope of $y=f(x)$ at $x=\frac{5\pi }{8}$ is $4.$

## q-31340 — Math Academy captured source and raw replay

Original:
Find the slope of $f(x)=\operatorname{csc}⁡(5x)$ at $x=-\frac{\pi }{2}.$

First, we express $f(x)$ as the composite function

$$
f=\operatorname{csc}⁡u,\,u=5x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=-\operatorname{csc}⁡u\operatorname{cot}⁡u,\,\frac{\text{d}u}{\text{d}x}=5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-\operatorname{csc}⁡u\operatorname{cot}⁡u\cdot (5) \\  & =-5\operatorname{csc}⁡u\operatorname{cot}⁡u \\  & =-5\operatorname{csc}⁡(5x)\operatorname{cot}⁡(5x).\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=-\frac{\pi }{2}$ is 

$$
\begin{aligned}\begin{aligned}\frac{\text{d}f}{\text{d}x}{|}_{x=-\pi /2} & =-5\operatorname{csc}⁡(5x)\operatorname{cot}⁡(5x){|}_{x=-\pi /2} \\  & =-5\operatorname{csc}⁡(5\cdot (-\frac{\pi }{2}))\operatorname{cot}⁡(5\cdot (-\frac{\pi }{2})) \\  & =-5\operatorname{csc}⁡(-\frac{5\pi }{2})\operatorname{cot}⁡(-\frac{5\pi }{2}) \\  & =-5\cdot (-1)\cdot 0 \\  & =0.\end{aligned}\end{aligned}
$$

Hence, the slope of the tangent to the curve at $x=-\frac{\pi }{2}$ is $0.$

Exact raw replay:
Find the slope of $f(x)=\operatorname{csc}⁡(5x)$ at $x=-\frac{\pi }{2}.$

- $0$
- $-1$
- $5$
- $1$
- $-5$

First, we express $f(x)$ as the composite function

$$
f=\operatorname{csc}⁡u,\,u=5x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=-\operatorname{csc}⁡u\operatorname{cot}⁡u,\,\frac{\text{d}u}{\text{d}x}=5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-\operatorname{csc}⁡u\operatorname{cot}⁡u\cdot (5) \\  & =-5\operatorname{csc}⁡u\operatorname{cot}⁡u \\  & =-5\operatorname{csc}⁡(5x)\operatorname{cot}⁡(5x).\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=-\frac{\pi }{2}$ is 

$$
\begin{aligned}\begin{aligned}\frac{\text{d}f}{\text{d}x}{|}_{x=-\pi /2} & =-5\operatorname{csc}⁡(5x)\operatorname{cot}⁡(5x){|}_{x=-\pi /2} \\  & =-5\operatorname{csc}⁡(5\cdot (-\frac{\pi }{2}))\operatorname{cot}⁡(5\cdot (-\frac{\pi }{2})) \\  & =-5\operatorname{csc}⁡(-\frac{5\pi }{2})\operatorname{cot}⁡(-\frac{5\pi }{2}) \\  & =-5\cdot (-1)\cdot 0 \\  & =0.\end{aligned}\end{aligned}
$$

Hence, the slope of the tangent to the curve at $x=-\frac{\pi }{2}$ is $0.$

Changed raw (evidence only):
Find the slope of $f(x)=\operatorname{csc}⁡(7x)$ at $x=-\frac{\pi }{2}.$

- $0$
- $-1$
- $7$
- $1$
- $-7$

First, we express $f(x)$ as the composite function

$$
f=\operatorname{csc}⁡u,\,u=7x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=-\operatorname{csc}⁡u\operatorname{cot}⁡u,\,\frac{\text{d}u}{\text{d}x}=7.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-\operatorname{csc}⁡u\operatorname{cot}⁡u\cdot (7) \\  & =-7\operatorname{csc}⁡u\operatorname{cot}⁡u \\  & =-7\operatorname{csc}⁡(7x)\operatorname{cot}⁡(7x).\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=-\frac{\pi }{2}$ is 

$$
\begin{aligned}\begin{aligned}\frac{\text{d}f}{\text{d}x}{|}_{x=-\pi /2} & =-7\operatorname{csc}⁡(7x)\operatorname{cot}⁡(7x){|}_{x=-\pi /2} \\  & =-7\operatorname{csc}⁡(7\cdot (-\frac{\pi }{2}))\operatorname{cot}⁡(7\cdot (-\frac{\pi }{2})) \\  & =-7\operatorname{csc}⁡(-\frac{7\pi }{2})\operatorname{cot}⁡(-\frac{7\pi }{2}) \\  & =-7\cdot (1)\cdot 0 \\  & =0.\end{aligned}\end{aligned}
$$

Hence, the slope of the tangent to the curve at $x=-\frac{\pi }{2}$ is $0.$

## q-31340 — normal source-family completion or repaired presentation

Normal generated:
Find the slope of $f(x)=\operatorname{csc}⁡(5x)$ at $x=-\frac{\pi }{2}.$

- $0$
- $-1$
- $5$
- $1$
- $-5$

First, we express $f(x)$ as the composite function

$$
f=\operatorname{csc}⁡u,\,u=5x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=-\operatorname{csc}⁡u\operatorname{cot}⁡u,\,\frac{\text{d}u}{\text{d}x}=5.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-\operatorname{csc}⁡u\operatorname{cot}⁡u\cdot (5) \\  & =-5\operatorname{csc}⁡u\operatorname{cot}⁡u \\  & =-5\operatorname{csc}⁡(5x)\operatorname{cot}⁡(5x).\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=-\frac{\pi }{2}$ is 

$$
\begin{aligned}\begin{aligned}\frac{\text{d}f}{\text{d}x}{|}_{x=-\pi /2} & =-5\operatorname{csc}⁡(5x)\operatorname{cot}⁡(5x){|}_{x=-\pi /2} \\  & =-5\operatorname{csc}⁡(5\cdot (-\frac{\pi }{2}))\operatorname{cot}⁡(5\cdot (-\frac{\pi }{2})) \\  & =-5\operatorname{csc}⁡(-\frac{5\pi }{2})\operatorname{cot}⁡(-\frac{5\pi }{2}) \\  & =-5\cdot (-1)\cdot 0 \\  & =0.\end{aligned}\end{aligned}
$$

Hence, the slope of the tangent to the curve at $x=-\frac{\pi }{2}$ is $0.$

Normal generated:
Find the slope of $f(x)=\operatorname{csc}⁡(7x)$ at $x=-\frac{\pi }{2}.$

- $0$
- $-1$
- $7$
- $1$
- $-7$

First, we express $f(x)$ as the composite function

$$
f=\operatorname{csc}⁡u,\,u=7x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=-\operatorname{csc}⁡u\operatorname{cot}⁡u,\,\frac{\text{d}u}{\text{d}x}=7.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-\operatorname{csc}⁡u\operatorname{cot}⁡u\cdot (7) \\  & =-7\operatorname{csc}⁡u\operatorname{cot}⁡u \\  & =-7\operatorname{csc}⁡(7x)\operatorname{cot}⁡(7x).\end{aligned}
$$

Therefore, the slope $m$ of the tangent line at the point where $x=-\frac{\pi }{2}$ is 

$$
\begin{aligned}\begin{aligned}\frac{\text{d}f}{\text{d}x}{|}_{x=-\pi /2} & =-7\operatorname{csc}⁡(7x)\operatorname{cot}⁡(7x){|}_{x=-\pi /2} \\  & =-7\operatorname{csc}⁡(7\cdot (-\frac{\pi }{2}))\operatorname{cot}⁡(7\cdot (-\frac{\pi }{2})) \\  & =-7\operatorname{csc}⁡(-\frac{7\pi }{2})\operatorname{cot}⁡(-\frac{7\pi }{2}) \\  & =-7\cdot (1)\cdot 0 \\  & =0.\end{aligned}\end{aligned}
$$

Hence, the slope of the tangent to the curve at $x=-\frac{\pi }{2}$ is $0.$

## q-342402 — Math Academy captured source and raw replay

Original:
Given that $f(x)=\frac{1}{2}\operatorname{sec}⁡(2x)-\frac{1}{4}{x}^{4},$ we have

${f}^{′}(x)=$

{{field-1}}.

Let $g(x)=\frac{1}{2}\operatorname{sec}⁡(2x)$ and $h(x)=-\frac{1}{4}{x}^{4}.$ Then

$$
f(x)=g(x)+h(x).
$$

First, we differentiate $g(x).$ We express $g(x)=\frac{1}{2}\operatorname{sec}⁡(2x)$ as the composite function

$$
g=\frac{1}{2}\operatorname{sec}⁡u,\,u=2x.
$$

Differentiating gives

$$
\frac{\text{d}g}{\text{d}u}=\frac{1}{2}\operatorname{sec}⁡u\operatorname{tan}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=2.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}g}{\text{d}x} & =\frac{\text{d}g}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{2}\operatorname{sec}⁡u\operatorname{tan}⁡u\cdot 2 \\  & =\operatorname{sec}⁡(2x)\operatorname{tan}⁡(2x).\end{aligned}
$$

Next, we differentiate $h(x)=-\frac{1}{4}{x}^{4}.$

Differentiating gives

$$
\begin{aligned}\frac{\text{d}h}{\text{d}x} & =-{x}^{3}.\end{aligned}
$$

Hence,

$$
\begin{aligned}{f}^{′}(x) & ={g}^{′}(x)+{h}^{′}(x) \\  & =\operatorname{sec}⁡(2x)\operatorname{tan}⁡(2x)-{x}^{3}.\end{aligned}
$$

Exact raw replay:
Given that $f(x)=\frac{1}{2}\operatorname{sec}⁡(2x)-\frac{1}{4}{x}^{4},$ we have

${f}^{′}(x)=$

{{field-1}}.

- $\operatorname{sec}(2x)\operatorname{tan}(2x)-{x}^{3}$

Let $g(x)=\frac{1}{2}\operatorname{sec}⁡(2x)$ and $h(x)=-\frac{1}{4}{x}^{4}.$ Then

$$
f(x)=g(x)+h(x).
$$

First, we differentiate $g(x).$ We express $g(x)=\frac{1}{2}\operatorname{sec}⁡(2x)$ as the composite function

$$
g=\frac{1}{2}\operatorname{sec}⁡u,\,u=2x.
$$

Differentiating gives

$$
\frac{\text{d}g}{\text{d}u}=\frac{1}{2}\operatorname{sec}⁡u\operatorname{tan}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=2.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}g}{\text{d}x} & =\frac{\text{d}g}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{2}\operatorname{sec}⁡u\operatorname{tan}⁡u\cdot 2 \\  & =\operatorname{sec}⁡(2x)\operatorname{tan}⁡(2x).\end{aligned}
$$

Next, we differentiate $h(x)=-\frac{1}{4}{x}^{4}.$

Differentiating gives

$$
\begin{aligned}\frac{\text{d}h}{\text{d}x} & =-{x}^{3}.\end{aligned}
$$

Hence,

$$
\begin{aligned}{f}^{′}(x) & ={g}^{′}(x)+{h}^{′}(x) \\  & =\operatorname{sec}⁡(2x)\operatorname{tan}⁡(2x)-{x}^{3}.\end{aligned}
$$

Changed raw (evidence only):
Given that $f(x)=\frac{1}{2}\operatorname{sec}⁡(2x)-\frac{2}{4}{x}^{4},$ we have

${f}^{′}(x)=$

{{field-1}}.

- $\operatorname{sec}(2x)\operatorname{tan}(2x)-2{x}^{3}$

Let $g(x)=\frac{1}{2}\operatorname{sec}⁡(2x)$ and $h(x)=-\frac{2}{4}{x}^{4}.$ Then

$$
f(x)=g(x)+h(x).
$$

First, we differentiate $g(x).$ We express $g(x)=\frac{1}{2}\operatorname{sec}⁡(2x)$ as the composite function

$$
g=\frac{1}{2}\operatorname{sec}⁡u,\,u=2x.
$$

Differentiating gives

$$
\frac{\text{d}g}{\text{d}u}=\frac{1}{2}\operatorname{sec}⁡u\operatorname{tan}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=2.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}g}{\text{d}x} & =\frac{\text{d}g}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{2}\operatorname{sec}⁡u\operatorname{tan}⁡u\cdot 2 \\  & =\operatorname{sec}⁡(2x)\operatorname{tan}⁡(2x).\end{aligned}
$$

Next, we differentiate $h(x)=-\frac{2}{4}{x}^{4}.$

Differentiating gives

$$
\begin{aligned}\frac{\text{d}h}{\text{d}x} & =-2{x}^{3}.\end{aligned}
$$

Hence,

$$
\begin{aligned}{f}^{′}(x) & ={g}^{′}(x)+{h}^{′}(x) \\  & =\operatorname{sec}⁡(2x)\operatorname{tan}⁡(2x)-2{x}^{3}.\end{aligned}
$$

## q-342402 — normal source-family completion or repaired presentation

Normal generated:
Given that $f(x)=\frac{1}{2}\operatorname{sec}⁡(2x)-\frac{1}{4}{x}^{4},$ we have

${f}^{′}(x)=$

{{field-1}}.

- $\operatorname{sec}(2x)\operatorname{tan}(2x)-{x}^{3}$

Let $g(x)=\frac{1}{2}\operatorname{sec}⁡(2x)$ and $h(x)=-\frac{1}{4}{x}^{4}.$ Then

$$
f(x)=g(x)+h(x).
$$

First, we differentiate $g(x).$ We express $g(x)=\frac{1}{2}\operatorname{sec}⁡(2x)$ as the composite function

$$
g=\frac{1}{2}\operatorname{sec}⁡u,\,u=2x.
$$

Differentiating gives

$$
\frac{\text{d}g}{\text{d}u}=\frac{1}{2}\operatorname{sec}⁡u\operatorname{tan}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=2.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}g}{\text{d}x} & =\frac{\text{d}g}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{2}\operatorname{sec}⁡u\operatorname{tan}⁡u\cdot 2 \\  & =\operatorname{sec}⁡(2x)\operatorname{tan}⁡(2x).\end{aligned}
$$

Next, we differentiate $h(x)=-\frac{1}{4}{x}^{4}.$

Differentiating gives

$$
\begin{aligned}\frac{\text{d}h}{\text{d}x} & =-{x}^{3}.\end{aligned}
$$

Hence,

$$
\begin{aligned}{f}^{′}(x) & ={g}^{′}(x)+{h}^{′}(x) \\  & =\operatorname{sec}⁡(2x)\operatorname{tan}⁡(2x)-{x}^{3}.\end{aligned}
$$

Normal generated:
Given that $f(x)=\frac{1}{2}\operatorname{sec}⁡(2x)-\frac{2}{4}{x}^{4},$ we have

${f}^{′}(x)=$

{{field-1}}.

- $\operatorname{sec}(2x)\operatorname{tan}(2x)-2{x}^{3}$

Let $g(x)=\frac{1}{2}\operatorname{sec}⁡(2x)$ and $h(x)=-\frac{2}{4}{x}^{4}.$ Then

$$
f(x)=g(x)+h(x).
$$

First, we differentiate $g(x).$ We express $g(x)=\frac{1}{2}\operatorname{sec}⁡(2x)$ as the composite function

$$
g=\frac{1}{2}\operatorname{sec}⁡u,\,u=2x.
$$

Differentiating gives

$$
\frac{\text{d}g}{\text{d}u}=\frac{1}{2}\operatorname{sec}⁡u\operatorname{tan}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=2.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}g}{\text{d}x} & =\frac{\text{d}g}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{1}{2}\operatorname{sec}⁡u\operatorname{tan}⁡u\cdot 2 \\  & =\operatorname{sec}⁡(2x)\operatorname{tan}⁡(2x).\end{aligned}
$$

Next, we differentiate $h(x)=-\frac{2}{4}{x}^{4}.$

Differentiating gives

$$
\begin{aligned}\frac{\text{d}h}{\text{d}x} & =-2{x}^{3}.\end{aligned}
$$

Hence,

$$
\begin{aligned}{f}^{′}(x) & ={g}^{′}(x)+{h}^{′}(x) \\  & =\operatorname{sec}⁡(2x)\operatorname{tan}⁡(2x)-2{x}^{3}.\end{aligned}
$$

## q-48512 — Math Academy captured source and raw replay

Original:
Find the equation of the tangent to the curve $y=\operatorname{cot}⁡(2\pi -3x)$ at the point $(\frac{\pi }{2},0).$

First, the slope of $y=f(x)$ at $x=\frac{\pi }{2}$ is given by ${f}^{′}(\frac{\pi }{2}).$

We will calculate ${f}^{′}(x)$ using the chain rule. First, we express $f(x)$ as the composite function

$$
f=\operatorname{cot}⁡u,\,u=2\pi -3x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=-3.
$$

We now apply the chain rule, and get

$$
\begin{aligned}{y}^{′} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =(-{csc}^{2}⁡u)\cdot (-3) \\  & =3{csc}^{2}⁡(2\pi -3x).\end{aligned}
$$

Evaluating at $x=\frac{\pi }{2},$ we find

$$
\begin{aligned}m={f}^{′}(\frac{\pi }{2}) & =3{csc}^{2}⁡(2\pi -\frac{3\pi }{2}) \\  & =3{csc}^{2}⁡(\frac{\pi }{2}) \\  & =3\cdot {1}^{2} \\  & =3.\end{aligned}
$$

Finally, we find the equation of the tangent at the point $(\frac{\pi }{2},0):$

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-0 & =3(x-\frac{\pi }{2}) \\ y & =3x-\frac{3\pi }{2}.\end{aligned}
$$

Exact raw replay:
Find the equation of the tangent to the curve $y=\operatorname{cot}⁡(2\pi -3x)$ at the point $(\frac{\pi }{2},0).$

- $y=\frac{\pi }{2}$
- $y=0$
- $y=x-\frac{\pi }{2}$
- $y=3x-\frac{\pi }{2}$
- $y=3x-\frac{3\pi }{2}$

First, the slope of $y=f(x)$ at $x=\frac{\pi }{2}$ is given by ${f}^{′}(\frac{\pi }{2}).$

We will calculate ${f}^{′}(x)$ using the chain rule. First, we express $f(x)$ as the composite function

$$
f=\operatorname{cot}⁡u,\,u=2\pi -3x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=-3.
$$

We now apply the chain rule, and get

$$
\begin{aligned}{y}^{′} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =(-{csc}^{2}⁡u)\cdot (-3) \\  & =3{csc}^{2}⁡(2\pi -3x).\end{aligned}
$$

Evaluating at $x=\frac{\pi }{2},$ we find

$$
\begin{aligned}m={f}^{′}(\frac{\pi }{2}) & =3{csc}^{2}⁡(2\pi -\frac{3\pi }{2}) \\  & =3{csc}^{2}⁡(\frac{\pi }{2}) \\  & =3\cdot {1}^{2} \\  & =3.\end{aligned}
$$

Finally, we find the equation of the tangent at the point $(\frac{\pi }{2},0):$

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-0 & =3(x-\frac{\pi }{2}) \\ y & =3x-\frac{3\pi }{2}.\end{aligned}
$$

Changed raw (evidence only):
Find the equation of the tangent to the curve $y=2\operatorname{cot}⁡(2\pi -3x)$ at the point $(\frac{\pi }{2},0).$

- $y=\frac{\pi }{2}$
- $y=0$
- $y=x-\frac{\pi }{2}$
- $y=6x-\frac{\pi }{2}$
- $y=6x-\frac{6\pi }{2}$

First, the slope of $y=f(x)$ at $x=\frac{\pi }{2}$ is given by ${f}^{′}(\frac{\pi }{2}).$

We will calculate ${f}^{′}(x)$ using the chain rule. First, we express $f(x)$ as the composite function

$$
f=2\operatorname{cot}⁡u,\,u=2\pi -3x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-2{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=-3.
$$

We now apply the chain rule, and get

$$
\begin{aligned}{y}^{′} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =(-2{csc}^{2}⁡u)\cdot (-3) \\  & =6{csc}^{2}⁡(2\pi -3x).\end{aligned}
$$

Evaluating at $x=\frac{\pi }{2},$ we find

$$
\begin{aligned}m={f}^{′}(\frac{\pi }{2}) & =6{csc}^{2}⁡(2\pi -\frac{3\pi }{2}) \\  & =6{csc}^{2}⁡(\frac{\pi }{2}) \\  & =6\cdot {1}^{2} \\  & =6.\end{aligned}
$$

Finally, we find the equation of the tangent at the point $(\frac{\pi }{2},0):$

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-0 & =6(x-\frac{\pi }{2}) \\ y & =6x-\frac{6\pi }{2}.\end{aligned}
$$

## q-48512 — normal source-family completion or repaired presentation

Normal generated:
Find the equation of the tangent to the curve $y=\operatorname{cot}⁡(2\pi -3x)$ at the point $(\frac{\pi }{2},0).$

- $y=\frac{\pi }{2}$
- $y=0$
- $y=x-\frac{\pi }{2}$
- $y=3x-\frac{\pi }{2}$
- $y=3x-\frac{3\pi }{2}$

First, the slope of $y=f(x)$ at $x=\frac{\pi }{2}$ is given by ${f}^{′}(\frac{\pi }{2}).$

We will calculate ${f}^{′}(x)$ using the chain rule. First, we express $f(x)$ as the composite function

$$
f=\operatorname{cot}⁡u,\,u=2\pi -3x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=-3.
$$

We now apply the chain rule, and get

$$
\begin{aligned}{y}^{′} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =(-{csc}^{2}⁡u)\cdot (-3) \\  & =3{csc}^{2}⁡(2\pi -3x).\end{aligned}
$$

Evaluating at $x=\frac{\pi }{2},$ we find

$$
\begin{aligned}m={f}^{′}(\frac{\pi }{2}) & =3{csc}^{2}⁡(2\pi -\frac{3\pi }{2}) \\  & =3{csc}^{2}⁡(\frac{\pi }{2}) \\  & =3\cdot {1}^{2} \\  & =3.\end{aligned}
$$

Finally, we find the equation of the tangent at the point $(\frac{\pi }{2},0):$

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-0 & =3(x-\frac{\pi }{2}) \\ y & =3x-\frac{3\pi }{2}.\end{aligned}
$$

Normal generated:
Find the equation of the tangent to the curve $y=2\operatorname{cot}⁡(2\pi -3x)$ at the point $(\frac{\pi }{2},0).$

- $y=\frac{\pi }{2}$
- $y=0$
- $y=x-\frac{\pi }{2}$
- $y=6x-\frac{\pi }{2}$
- $y=6x-\frac{6\pi }{2}$

First, the slope of $y=f(x)$ at $x=\frac{\pi }{2}$ is given by ${f}^{′}(\frac{\pi }{2}).$

We will calculate ${f}^{′}(x)$ using the chain rule. First, we express $f(x)$ as the composite function

$$
f=2\operatorname{cot}⁡u,\,u=2\pi -3x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-2{csc}^{2}⁡u\,\text{and}\,\frac{\text{d}u}{\text{d}x}=-3.
$$

We now apply the chain rule, and get

$$
\begin{aligned}{y}^{′} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =(-2{csc}^{2}⁡u)\cdot (-3) \\  & =6{csc}^{2}⁡(2\pi -3x).\end{aligned}
$$

Evaluating at $x=\frac{\pi }{2},$ we find

$$
\begin{aligned}m={f}^{′}(\frac{\pi }{2}) & =6{csc}^{2}⁡(2\pi -\frac{3\pi }{2}) \\  & =6{csc}^{2}⁡(\frac{\pi }{2}) \\  & =6\cdot {1}^{2} \\  & =6.\end{aligned}
$$

Finally, we find the equation of the tangent at the point $(\frac{\pi }{2},0):$

$$
\begin{aligned}y-{y}_{1} & =m(x-{x}_{1}) \\ y-0 & =6(x-\frac{\pi }{2}) \\ y & =6x-\frac{6\pi }{2}.\end{aligned}
$$
