# Trig composition source and changed-input review

## Original MA evidence / q-31356 / {'b': 0}

Find the derivative of $y = \cot (\cos x)$.

- \sin x\cot^{2} (\cos x)
- \sin x\csc^{2} (\cos x)
- \csc x\sin^{2} (\cos x)
- \sin x\cos^{2} (\csc x)
- \csc x\cos^{2} (\sin x)

## Original MA evidence / q-48643 / {'b': 0}

Find the derivative of $y=\operatorname{sin}⁡(\operatorname{cos}⁡x).$

- -\operatorname{cos}⁡x\operatorname{sin}⁡(\operatorname{cos}⁡x)
* -\operatorname{sin}⁡x\operatorname{cos}⁡(\operatorname{cos}⁡x)
- -\operatorname{sin}⁡x\operatorname{cos}⁡(\operatorname{sin}⁡x)
- -\operatorname{cos}⁡x\operatorname{cos}⁡(\operatorname{sin}⁡x)
- -\operatorname{sin}⁡x\operatorname{sin}⁡(\operatorname{cos}⁡x)

First, we express $y$ as the composite function

$$
y=\operatorname{sin}⁡u,\,u=\operatorname{cos}⁡x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\operatorname{cos}⁡u,\,\frac{\text{d}u}{\text{d}x}=-\operatorname{sin}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\operatorname{cos}⁡u\cdot (-\operatorname{sin}⁡x) \\  & =-\operatorname{sin}⁡x\operatorname{cos}⁡(\operatorname{cos}⁡x).\end{aligned}
$$

## Original MA evidence / q-48644 / {'a': 1, 'b': 0, 'phase': '0'}

Find the equation of the tangent to the curve $y =\cos \left(\sin x \right)$ at the point $\left(0,1 \right).$

First, the slope of $y = f(x)$ at $x = 0$ is given by $f'(0).$

We will calculate $f'(x)$ using the chain rule. First, we express $f(x)$ as the composite function

\[
f = \cos{u}, \qquad u = \sin x.
\]

Differentiating gives

\[
\dfrac{\textrm d f}{\textrm d u} = -\sin{u}, \qquad \dfrac{\textrm d u}{\textrm d x} =\cos x.
\]

We now apply the chain rule, and get

\begin{align*}
 \dfrac{\textrm d f}{\textrm d x} &= \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]
&=-\sin u \cdot (\cos x)\\[5pt]
&=-\cos x \sin (\sin x).
\end{align*}

Evaluating at $x=0,$ we find
\[
	\eqalign{
	f'(0)&=-\cos (0) \sin (\sin (0))\\[3pt]
	&=-1 \cdot 0 \\[3pt]
        &=0.
}
\]

Finally, we find the equation of the tangent at the point $(0,1) \mathbin{:}$

\begin{align}
y-y_1 &= m(x-x_1)\\[3pt]
y-1 &= (0)\cdot\left(x-0\right)\\[3pt]
y&=1.
\end{align}

## Original MA evidence / q-72163 / {'b': 0}

Find the derivative of $y=\operatorname{sin}(\operatorname{sec}x).$

First, we express $y$ as the composite function

$$
y=\operatorname{sin}u,\,u=\operatorname{sec}x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\operatorname{cos}u,\,\frac{\text{d}u}{\text{d}x}=\operatorname{sec}x\operatorname{tan}x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\operatorname{cos}u\cdot (\operatorname{sec}x\operatorname{tan}x) \\  & =\operatorname{sec}x\operatorname{tan}x\operatorname{cos}(\operatorname{sec}x).\end{aligned}
$$

## Original MA evidence / q-72170 / {'b': 0}

Find the derivative of $y =\csc ( \cos x).$

First, we express $y$ as the composite function

\[
y = \csc{u}, \qquad u = \cos{x}.
\]

Differentiating gives

\[
\dfrac{\textrm d y}{\textrm d u} = -\csc{u}\cot u,\qquad \dfrac{\textrm{d}u}{\textrm d x} = -\sin{x}.
\]

We now apply the chain rule, and get

\begin{align*}
\dfrac{\textrm d y}{\textrm d x} &= \dfrac{\textrm d y}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\[5pt]

&=-\csc u \cot u \cdot  (-\sin x)\\[5pt]

&=\sin x\csc \left(\cos x\right) \cot \left(\cos x\right).
\end{align*}

## Original MA evidence / q-341223 / {'a': 4, 'b': 0}

Given that $y=4\operatorname{cos}⁡(\operatorname{sin}⁡(x)),$ we have

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}$\cdot \operatorname{sin}⁡($
{{field-2}} $).$

* -4\operatorname{cos}(x)

* \operatorname{sin}(x)

First, we express $y$ as the composite function

$$
y=4\operatorname{cos}⁡(u),\,u=\operatorname{sin}⁡(x).
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-4\operatorname{sin}⁡(u),\,\frac{\text{d}u}{\text{d}x}=\operatorname{cos}⁡(x).
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-4\operatorname{sin}⁡(u)\cdot \operatorname{cos}⁡(x) \\  & =-4\operatorname{cos}⁡(x)\cdot \operatorname{sin}⁡(\operatorname{sin}⁡(x)).\end{aligned}
$$

## Original MA evidence / q-342436 / {'b': 0}

Given that $y=\operatorname{tan}⁡(\operatorname{tan}⁡(x)),$ we have

$\frac{\text{d}y}{\text{d}x}={sec}^{2}⁡(x)\,\cdot $
{{field-1}}.

* {sec}^{2}(\operatorname{tan}(x))

First, we express $y$ as the composite function

$$
y=\operatorname{tan}⁡(u),\,u=\operatorname{tan}⁡(x).
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}={sec}^{2}⁡(u),\,\frac{\text{d}u}{\text{d}x}={sec}^{2}⁡(x).
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & ={sec}^{2}⁡(u)\cdot {sec}^{2}⁡(x) \\  & ={sec}^{2}⁡(x)\cdot {sec}^{2}⁡(\operatorname{tan}⁡(x)).\end{aligned}
$$

## Original MA evidence / q-342443 / {'a': 4, 'b': 0}

Given that $y=4\operatorname{sec}⁡(\operatorname{sin}⁡(x)),$ we have

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}$\operatorname{sec}⁡($
{{field-2}} $)\operatorname{tan}⁡($
{{field-3}} $).$

* \operatorname{sin}(x)

* \operatorname{sin}(x)

* 4\operatorname{cos}x

First, we express $y$ as the composite function

$$
y=4\operatorname{sec}⁡(u),\,u=\operatorname{sin}⁡(x).
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=4\operatorname{sec}⁡(u)\operatorname{tan}⁡(u),\,\frac{\text{d}u}{\text{d}x}=\operatorname{cos}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =4\operatorname{sec}⁡(u)\operatorname{tan}⁡(u)\cdot \operatorname{cos}⁡x \\  & =4\operatorname{cos}⁡x\operatorname{sec}⁡(\operatorname{sin}⁡(x))\operatorname{tan}⁡(\operatorname{sin}⁡(x)).\end{aligned}
$$

## Original MA evidence / q-342445 / {'b': 0}

Given that $y=\operatorname{sec}⁡(\operatorname{csc}⁡(x)),$ we have

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}$\cdot \,\operatorname{sec}⁡(\operatorname{csc}⁡(x))\cdot \operatorname{tan}⁡($
{{field-2}} $).$

* -\operatorname{csc}x\operatorname{cot}x

* \operatorname{csc}(x)

First, we express $y$ as the composite function

$$
y=\operatorname{sec}⁡(u),\,u=\operatorname{csc}⁡(x).
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\operatorname{sec}⁡(u)\operatorname{tan}⁡(u),\,\frac{\text{d}u}{\text{d}x}=-\operatorname{csc}⁡x\operatorname{cot}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\operatorname{sec}⁡(u)\operatorname{tan}⁡(u)\cdot (-\operatorname{csc}⁡x\operatorname{cot}⁡x) \\  & =-\operatorname{csc}⁡x\operatorname{cot}⁡x\cdot \operatorname{sec}⁡(\operatorname{csc}⁡(x))\cdot \operatorname{tan}⁡(\operatorname{csc}⁡(x)).\end{aligned}
$$

## Original MA evidence / q-72161 / {'b': 0}

Find the derivative of $y=\operatorname{cot}⁡(\operatorname{sin}⁡x).$

- -\operatorname{cos}⁡x{csc}^{2}⁡(\operatorname{cos}⁡x)
* -\operatorname{cos}⁡x{csc}^{2}⁡(\operatorname{sin}⁡x)
- -{csc}^{2}⁡(\operatorname{sin}⁡x)
- {csc}^{2}⁡(\operatorname{cos}⁡x)
- \operatorname{cos}⁡x{csc}^{2}⁡(\operatorname{cos}⁡x)

First, we express $y$ as the composite function

$$
y=\operatorname{cot}⁡u,\,u=\operatorname{sin}⁡x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-{csc}^{2}⁡u,\,\frac{\text{d}u}{\text{d}x}=\operatorname{cos}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot (\operatorname{cos}⁡x) \\  & =-\operatorname{cos}⁡x{csc}^{2}⁡(\operatorname{sin}⁡x).\end{aligned}
$$

## Original MA evidence / q-72173 / {'a': 3, 'b': 0}

Find the derivative of $y=3\operatorname{sec}⁡(\operatorname{cos}⁡x).$

- 3\operatorname{sec}⁡x\operatorname{tan}⁡(-\operatorname{sin}⁡x)
- 3\operatorname{sin}⁡x\operatorname{sec}⁡(-\operatorname{sin}⁡x)\operatorname{tan}⁡(-\operatorname{sin}⁡x)
- 3\operatorname{cos}⁡x\operatorname{sec}⁡(\operatorname{cos}⁡x)\operatorname{tan}⁡(\operatorname{cos}⁡x)
- 3\operatorname{sin}⁡x\operatorname{sec}⁡x\operatorname{tan}⁡(\operatorname{cos}⁡x)
* -3\operatorname{sin}⁡x\operatorname{sec}⁡(\operatorname{cos}⁡x)\operatorname{tan}⁡(\operatorname{cos}⁡x)

First, we express $y$ as the composite function

$$
y=3\operatorname{sec}⁡u,\,u=\operatorname{cos}⁡x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=3\operatorname{sec}⁡u\operatorname{tan}⁡u,\,\frac{\text{d}u}{\text{d}x}=-\operatorname{sin}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =3\operatorname{sec}⁡u\operatorname{tan}⁡u\cdot (-\operatorname{sin}⁡x) \\  & =-3\operatorname{sin}⁡x\operatorname{sec}⁡(\operatorname{cos}⁡x)\operatorname{tan}⁡(\operatorname{cos}⁡x).\end{aligned}
$$

## Eligible moderate / q-31356 / {'a': 1, 'b': 0}

Find the derivative of $y = \cot (\cos x)$.

- \csc x\sin^{2} (\cos x)
* \sin x\csc^{2} (\cos x)
- \sin x\cot^{2} (\cos x)
- \csc x\cos^{2} (\sin x)
- \sin x\cos^{2} (\csc x)

First, we express $y$ as the composite function

$$
y=\cot{\left(u \right)},\qquad u=\cos{\left(x \right)}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=- \cot^{2}{\left(u \right)} - 1,\qquad \frac{\text{d}u}{\text{d}x}=- \sin{\left(x \right)}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} &=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=(- \cot^{2}{\left(u \right)} - 1)\cdot (- \sin{\left(x \right)}) \\ &=- \left(- \cot^{2}{\left(\cos{\left(x \right)} \right)} - 1\right) \sin{\left(x \right)}.\end{aligned}
$$

## Eligible moderate / q-31356 / {'a': 9, 'b': 0}

Find the derivative of $y = 9\cot (\cos x)$.

- 9\left(\sin x\cos^{2} (\csc x)\right)
- 9\left(\sin x\cot^{2} (\cos x)\right)
- 9\left(\csc x\cos^{2} (\sin x)\right)
- 9\left(\csc x\sin^{2} (\cos x)\right)
* 9\left(\sin x\csc^{2} (\cos x)\right)

First, we express $y$ as the composite function

$$
y=9 \cot{\left(u \right)},\qquad u=\cos{\left(x \right)}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=- 9 \cot^{2}{\left(u \right)} - 9,\qquad \frac{\text{d}u}{\text{d}x}=- \sin{\left(x \right)}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} &=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=(- 9 \cot^{2}{\left(u \right)} - 9)\cdot (- \sin{\left(x \right)}) \\ &=- 9 \left(- \cot^{2}{\left(\cos{\left(x \right)} \right)} - 1\right) \sin{\left(x \right)}.\end{aligned}
$$

## Eligible moderate / q-48643 / {'a': 1, 'b': 0}

Find the derivative of $y=\operatorname{sin}⁡(\operatorname{cos}⁡x).$

- -\operatorname{sin}⁡x\operatorname{cos}⁡(\operatorname{sin}⁡x)
* -\operatorname{sin}⁡x\operatorname{cos}⁡(\operatorname{cos}⁡x)
- -\operatorname{cos}⁡x\operatorname{sin}⁡(\operatorname{cos}⁡x)
- -\operatorname{sin}⁡x\operatorname{sin}⁡(\operatorname{cos}⁡x)
- -\operatorname{cos}⁡x\operatorname{cos}⁡(\operatorname{sin}⁡x)

First, we express $y$ as the composite function

$$
y=\operatorname{sin}⁡u,\,u=\operatorname{cos}⁡x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\operatorname{cos}⁡u,\,\frac{\text{d}u}{\text{d}x}=-\operatorname{sin}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\operatorname{cos}⁡u\cdot (-\operatorname{sin}⁡x) \\  & =-\operatorname{sin}⁡x\operatorname{cos}⁡(\operatorname{cos}⁡x).\end{aligned}
$$

## Eligible moderate / q-48643 / {'a': 9, 'b': 0}

Find the derivative of $y=9\operatorname{sin}⁡(\operatorname{cos}⁡x).$

- 9\left(-\operatorname{cos}⁡x\operatorname{cos}⁡(\operatorname{sin}⁡x)\right)
- 9\left(-\operatorname{cos}⁡x\operatorname{sin}⁡(\operatorname{cos}⁡x)\right)
- 9\left(-\operatorname{sin}⁡x\operatorname{sin}⁡(\operatorname{cos}⁡x)\right)
- 9\left(-\operatorname{sin}⁡x\operatorname{cos}⁡(\operatorname{sin}⁡x)\right)
* 9\left(-\operatorname{sin}⁡x\operatorname{cos}⁡(\operatorname{cos}⁡x)\right)

First, we express $y$ as the composite function

$$
y=9\operatorname{sin}⁡u,\,u=\operatorname{cos}⁡x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=9\operatorname{cos}⁡u,\,\frac{\text{d}u}{\text{d}x}=-\operatorname{sin}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =9\operatorname{cos}⁡u\cdot (-\operatorname{sin}⁡x) \\  & =-9\operatorname{sin}⁡x\operatorname{cos}⁡(\operatorname{cos}⁡x).\end{aligned}
$$

## Eligible hard / q-48644 / {'a': 1, 'b': 0, 'phase': '0'}

Find the equation of the tangent to the curve $y =\cos \left(\sin x \right)$ at the point $\left(0,1 \right).$

$y=$ {{field-1}}

* 1

First, the slope of $y = f(x)$ at $x = 0$ is given by $f'(0).$

We will calculate $f'(x)$ using the chain rule. First, we express $f(x)$ as the composite function

$$
f = \cos{u}, \qquad u = \sin x.
$$

Differentiating gives

$$
\dfrac{\textrm d f}{\textrm d u} = -\sin{u}, \qquad \dfrac{\textrm d u}{\textrm d x} =\cos x.
$$

We now apply the chain rule, and get


$$
\begin{aligned}
 \dfrac{\textrm d f}{\textrm d x} &= \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\
&=-\sin u \cdot (\cos x)\\
&=-\cos x \sin (\sin x).
\end{aligned}
$$


Evaluating at $x=0,$ we find
$$
\begin{aligned}
	f'(0)&=-\cos (0) \sin (\sin (0))\\
	&=-1 \cdot 0 \\
        &=0.
\end{aligned}
$$

Finally, we find the equation of the tangent at the point $(0,1) \mathbin{:}$


$$
\begin{aligned}
y-y_1 &= m(x-x_1)\\
y-1 &= (0)\cdot\left(x-0\right)\\
y&=1.
\end{aligned}
$$


## Eligible hard / q-48644 / {'a': 9, 'b': 0, 'phase': '-1/2'}

Find the equation of the tangent to the curve $y =9 \cos{\left(\sin{\left(x \right)} - \frac{\pi}{2} \right)}$ at the point $\left(0,0 \right).$

$y=$ {{field-1}}

* 9 x

First, the slope of $y = f(x)$ at $x = 0$ is given by $f'(0).$

We will calculate $f'(x)$ using the chain rule. First, we express $f(x)$ as the composite function

$$
f = 9 \cos{\left(u \right)}, \qquad u = \sin{\left(x \right)} - \frac{\pi}{2}.
$$

Differentiating gives

$$
\dfrac{\textrm d f}{\textrm d u} = - 9 \sin{\left(u \right)}, \qquad \dfrac{\textrm d u}{\textrm d x} =\cos{\left(x \right)}.
$$

We now apply the chain rule, and get


$$
\begin{aligned}
 \dfrac{\textrm d f}{\textrm d x} &= \dfrac{\textrm d f}{\textrm d u} \cdot \dfrac{\textrm d u}{\textrm d x}\\
&=- 9 \sin{\left(u \right)} \cdot (\cos{\left(x \right)})\\
&=- 9 \sin{\left(\sin{\left(x \right)} - \frac{\pi}{2} \right)} \cos{\left(x \right)}.
\end{aligned}
$$


Evaluating at $x=0,$ we find
$$
\begin{aligned}
	f'(0)&=- 9 \sin{\left(- \frac{\pi}{2} + \sin{\left(0 \right)} \right)} \cos{\left(0 \right)}\\
	&=-9 \cdot -1 \\
        &=9.
\end{aligned}
$$

Finally, we find the equation of the tangent at the point $(0,0) \mathbin{:}$


$$
\begin{aligned}
y-y_1 &= m(x-x_1)\\
y-\left(0\right) &= (9)\cdot\left(x-(0)\right)\\
y&=9 x.
\end{aligned}
$$


## Eligible moderate / q-341223 / {'a': 1, 'b': 0}

Given that $y=1\operatorname{cos}⁡(\operatorname{sin}⁡(x)),$ we have

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}$\cdot \operatorname{sin}⁡($
{{field-2}} $).$

* -1\operatorname{cos}(x)

* \operatorname{sin}(x)

First, we express $y$ as the composite function

$$
y=1\operatorname{cos}⁡(u),\,u=\operatorname{sin}⁡(x).
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-1\operatorname{sin}⁡(u),\,\frac{\text{d}u}{\text{d}x}=\operatorname{cos}⁡(x).
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-1\operatorname{sin}⁡(u)\cdot \operatorname{cos}⁡(x) \\  & =-1\operatorname{cos}⁡(x)\cdot \operatorname{sin}⁡(\operatorname{sin}⁡(x)).\end{aligned}
$$

## Eligible moderate / q-341223 / {'a': 9, 'b': 0}

Given that $y=9\operatorname{cos}⁡(\operatorname{sin}⁡(x)),$ we have

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}$\cdot \operatorname{sin}⁡($
{{field-2}} $).$

* -9\operatorname{cos}(x)

* \operatorname{sin}(x)

First, we express $y$ as the composite function

$$
y=9\operatorname{cos}⁡(u),\,u=\operatorname{sin}⁡(x).
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-9\operatorname{sin}⁡(u),\,\frac{\text{d}u}{\text{d}x}=\operatorname{cos}⁡(x).
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-9\operatorname{sin}⁡(u)\cdot \operatorname{cos}⁡(x) \\  & =-9\operatorname{cos}⁡(x)\cdot \operatorname{sin}⁡(\operatorname{sin}⁡(x)).\end{aligned}
$$

## Eligible moderate / q-342443 / {'a': 1, 'b': 0}

Given that $y=1\operatorname{sec}⁡(\operatorname{sin}⁡(x)),$ we have

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}$\operatorname{sec}⁡($
{{field-2}} $)\operatorname{tan}⁡($
{{field-3}} $).$

* \operatorname{sin}(x)

* \operatorname{sin}(x)

* 1\operatorname{cos}x

First, we express $y$ as the composite function

$$
y=1\operatorname{sec}⁡(u),\,u=\operatorname{sin}⁡(x).
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=1\operatorname{sec}⁡(u)\operatorname{tan}⁡(u),\,\frac{\text{d}u}{\text{d}x}=\operatorname{cos}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =1\operatorname{sec}⁡(u)\operatorname{tan}⁡(u)\cdot \operatorname{cos}⁡x \\  & =1\operatorname{cos}⁡x\operatorname{sec}⁡(\operatorname{sin}⁡(x))\operatorname{tan}⁡(\operatorname{sin}⁡(x)).\end{aligned}
$$

## Eligible moderate / q-342443 / {'a': 9, 'b': 0}

Given that $y=9\operatorname{sec}⁡(\operatorname{sin}⁡(x)),$ we have

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}$\operatorname{sec}⁡($
{{field-2}} $)\operatorname{tan}⁡($
{{field-3}} $).$

* \operatorname{sin}(x)

* \operatorname{sin}(x)

* 9\operatorname{cos}x

First, we express $y$ as the composite function

$$
y=9\operatorname{sec}⁡(u),\,u=\operatorname{sin}⁡(x).
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=9\operatorname{sec}⁡(u)\operatorname{tan}⁡(u),\,\frac{\text{d}u}{\text{d}x}=\operatorname{cos}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =9\operatorname{sec}⁡(u)\operatorname{tan}⁡(u)\cdot \operatorname{cos}⁡x \\  & =9\operatorname{cos}⁡x\operatorname{sec}⁡(\operatorname{sin}⁡(x))\operatorname{tan}⁡(\operatorname{sin}⁡(x)).\end{aligned}
$$

## Eligible moderate / q-342445 / {'a': 1, 'b': 0}

Given that $y=\operatorname{sec}⁡(\operatorname{csc}⁡(x)),$ we have

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}$\cdot \,\operatorname{sec}⁡(\operatorname{csc}⁡(x))\cdot \operatorname{tan}⁡($
{{field-2}} $).$

* -\operatorname{csc}x\operatorname{cot}x

* \operatorname{csc}(x)

First, we express $y$ as the composite function

$$
y=\operatorname{sec}⁡(u),\,u=\operatorname{csc}⁡(x).
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\operatorname{sec}⁡(u)\operatorname{tan}⁡(u),\,\frac{\text{d}u}{\text{d}x}=-\operatorname{csc}⁡x\operatorname{cot}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\operatorname{sec}⁡(u)\operatorname{tan}⁡(u)\cdot (-\operatorname{csc}⁡x\operatorname{cot}⁡x) \\  & =-\operatorname{csc}⁡x\operatorname{cot}⁡x\cdot \operatorname{sec}⁡(\operatorname{csc}⁡(x))\cdot \operatorname{tan}⁡(\operatorname{csc}⁡(x)).\end{aligned}
$$

## Eligible moderate / q-342445 / {'a': 9, 'b': 0}

Given that $y=9\operatorname{sec}⁡(\operatorname{csc}⁡(x)),$ we have

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}$\cdot \,\operatorname{sec}⁡(\operatorname{csc}⁡(x))\cdot \operatorname{tan}⁡($
{{field-2}} $).$

* 9\left(-\operatorname{csc}x\operatorname{cot}x\right)

* \operatorname{csc}(x)

First, we express $y$ as the composite function

$$
y=9\operatorname{sec}⁡(u),\,u=\operatorname{csc}⁡(x).
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=9\operatorname{sec}⁡(u)\operatorname{tan}⁡(u),\,\frac{\text{d}u}{\text{d}x}=-\operatorname{csc}⁡x\operatorname{cot}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =9\operatorname{sec}⁡(u)\operatorname{tan}⁡(u)\cdot (-\operatorname{csc}⁡x\operatorname{cot}⁡x) \\  & =-9\operatorname{csc}⁡x\operatorname{cot}⁡x\cdot \operatorname{sec}⁡(\operatorname{csc}⁡(x))\cdot \operatorname{tan}⁡(\operatorname{csc}⁡(x)).\end{aligned}
$$

## Eligible moderate / q-72161 / {'a': 1, 'b': 0}

Find the derivative of $y=\operatorname{cot}⁡(\operatorname{sin}⁡x).$

- -\csc^{2}⁡(\operatorname{sin}⁡x)
* -\operatorname{cos}⁡x\csc^{2}⁡(\operatorname{sin}⁡x)
- -\operatorname{cos}⁡x\csc^{2}⁡(\operatorname{cos}⁡x)
- \operatorname{cos}⁡x\csc^{2}⁡(\operatorname{cos}⁡x)
- \csc^{2}⁡(\operatorname{cos}⁡x)

First, we express $y$ as the composite function

$$
y=\operatorname{cot}⁡u,\,u=\operatorname{sin}⁡x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-\csc^{2}⁡u,\,\frac{\text{d}u}{\text{d}x}=\operatorname{cos}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-\csc^{2}⁡u\cdot (\operatorname{cos}⁡x) \\  & =-\operatorname{cos}⁡x\csc^{2}⁡(\operatorname{sin}⁡x).\end{aligned}
$$

## Eligible moderate / q-72161 / {'a': 9, 'b': 0}

Find the derivative of $y=9\operatorname{cot}⁡(\operatorname{sin}⁡x).$

- 9\left(\csc^{2}⁡(\operatorname{cos}⁡x)\right)
- 9\left(-\operatorname{cos}⁡x\csc^{2}⁡(\operatorname{cos}⁡x)\right)
- 9\left(\operatorname{cos}⁡x\csc^{2}⁡(\operatorname{cos}⁡x)\right)
- 9\left(-\csc^{2}⁡(\operatorname{sin}⁡x)\right)
* 9\left(-\operatorname{cos}⁡x\csc^{2}⁡(\operatorname{sin}⁡x)\right)

First, we express $y$ as the composite function

$$
y=9\operatorname{cot}⁡u,\,u=\operatorname{sin}⁡x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-9\csc^{2}⁡u,\,\frac{\text{d}u}{\text{d}x}=\operatorname{cos}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =-9\csc^{2}⁡u\cdot (\operatorname{cos}⁡x) \\  & =-9\operatorname{cos}⁡x\csc^{2}⁡(\operatorname{sin}⁡x).\end{aligned}
$$

## Eligible moderate / q-72173 / {'a': 1, 'b': 0}

Find the derivative of $y=1\operatorname{sec}⁡(\operatorname{cos}⁡x).$

- 1\operatorname{cos}⁡x\operatorname{sec}⁡(\operatorname{cos}⁡x)\operatorname{tan}⁡(\operatorname{cos}⁡x)
- 1\operatorname{sin}⁡x\operatorname{sec}⁡(-\operatorname{sin}⁡x)\operatorname{tan}⁡(-\operatorname{sin}⁡x)
- 1\operatorname{sec}⁡x\operatorname{tan}⁡(-\operatorname{sin}⁡x)
* -1\operatorname{sin}⁡x\operatorname{sec}⁡(\operatorname{cos}⁡x)\operatorname{tan}⁡(\operatorname{cos}⁡x)
- 1\operatorname{sin}⁡x\operatorname{sec}⁡x\operatorname{tan}⁡(\operatorname{cos}⁡x)

First, we express $y$ as the composite function

$$
y=1\operatorname{sec}⁡u,\,u=\operatorname{cos}⁡x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=1\operatorname{sec}⁡u\operatorname{tan}⁡u,\,\frac{\text{d}u}{\text{d}x}=-\operatorname{sin}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =1\operatorname{sec}⁡u\operatorname{tan}⁡u\cdot (-\operatorname{sin}⁡x) \\  & =-1\operatorname{sin}⁡x\operatorname{sec}⁡(\operatorname{cos}⁡x)\operatorname{tan}⁡(\operatorname{cos}⁡x).\end{aligned}
$$

## Eligible moderate / q-72173 / {'a': 9, 'b': 0}

Find the derivative of $y=9\operatorname{sec}⁡(\operatorname{cos}⁡x).$

- 9\operatorname{sin}⁡x\operatorname{sec}⁡x\operatorname{tan}⁡(\operatorname{cos}⁡x)
- 9\operatorname{sec}⁡x\operatorname{tan}⁡(-\operatorname{sin}⁡x)
* -9\operatorname{sin}⁡x\operatorname{sec}⁡(\operatorname{cos}⁡x)\operatorname{tan}⁡(\operatorname{cos}⁡x)
- 9\operatorname{cos}⁡x\operatorname{sec}⁡(\operatorname{cos}⁡x)\operatorname{tan}⁡(\operatorname{cos}⁡x)
- 9\operatorname{sin}⁡x\operatorname{sec}⁡(-\operatorname{sin}⁡x)\operatorname{tan}⁡(-\operatorname{sin}⁡x)

First, we express $y$ as the composite function

$$
y=9\operatorname{sec}⁡u,\,u=\operatorname{cos}⁡x.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=9\operatorname{sec}⁡u\operatorname{tan}⁡u,\,\frac{\text{d}u}{\text{d}x}=-\operatorname{sin}⁡x.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =9\operatorname{sec}⁡u\operatorname{tan}⁡u\cdot (-\operatorname{sin}⁡x) \\  & =-9\operatorname{sin}⁡x\operatorname{sec}⁡(\operatorname{cos}⁡x)\operatorname{tan}⁡(\operatorname{cos}⁡x).\end{aligned}
$$

## Eligible easy / authored-easy / {'a': 1, 'b': 0, 'outer': 'sin', 'inner': 'sin'}

Find the derivative of $y=\sin{\left(\sin{\left(x \right)} \right)}.$

- - \cos{\left(x \right)} \cos{\left(\sin{\left(x \right)} \right)}
- \cos{\left(\sin{\left(x \right)} \right)}
* \cos{\left(x \right)} \cos{\left(\sin{\left(x \right)} \right)}
- \cos{\left(x \right)} \cos{\left(\cos{\left(x \right)} \right)}
- \sin{\left(\sin{\left(x \right)} \right)} \cos{\left(x \right)}

First, we express $y$ as the composite function

$$
y=\sin{\left(u \right)},\qquad u=\sin{\left(x \right)}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\cos{\left(u \right)},\qquad \frac{\text{d}u}{\text{d}x}=\cos{\left(x \right)}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} &=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=(\cos{\left(u \right)})\cdot (\cos{\left(x \right)}) \\ &=\cos{\left(x \right)} \cos{\left(\sin{\left(x \right)} \right)}.\end{aligned}
$$

## Eligible easy / authored-easy / {'a': 9, 'b': 0, 'outer': 'cos', 'inner': 'cos'}

Find the derivative of $y=9 \cos{\left(\cos{\left(x \right)} \right)}.$

- - 9 \sin{\left(x \right)} \cos{\left(\cos{\left(x \right)} \right)}
- - 9 \sin{\left(\cos{\left(x \right)} \right)}
* 9 \sin{\left(x \right)} \sin{\left(\cos{\left(x \right)} \right)}
- - 9 \sin{\left(x \right)} \sin{\left(\cos{\left(x \right)} \right)}
- 9 \sin{\left(x \right)} \sin{\left(\sin{\left(x \right)} \right)}

First, we express $y$ as the composite function

$$
y=9 \cos{\left(u \right)},\qquad u=\cos{\left(x \right)}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=- 9 \sin{\left(u \right)},\qquad \frac{\text{d}u}{\text{d}x}=- \sin{\left(x \right)}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} &=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=(- 9 \sin{\left(u \right)})\cdot (- \sin{\left(x \right)}) \\ &=9 \sin{\left(x \right)} \sin{\left(\cos{\left(x \right)} \right)}.\end{aligned}
$$

## Eligible easy / authored-easy / {'a': 4, 'b': 0, 'outer': 'sin', 'inner': 'sin'}

Find the derivative of $y=4 \sin{\left(\sin{\left(x \right)} \right)}.$

- - 4 \cos{\left(x \right)} \cos{\left(\sin{\left(x \right)} \right)}
- 4 \cos{\left(\sin{\left(x \right)} \right)}
* 4 \cos{\left(x \right)} \cos{\left(\sin{\left(x \right)} \right)}
- 4 \cos{\left(x \right)} \cos{\left(\cos{\left(x \right)} \right)}
- 4 \sin{\left(\sin{\left(x \right)} \right)} \cos{\left(x \right)}

First, we express $y$ as the composite function

$$
y=4 \sin{\left(u \right)},\qquad u=\sin{\left(x \right)}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=4 \cos{\left(u \right)},\qquad \frac{\text{d}u}{\text{d}x}=\cos{\left(x \right)}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} &=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=(4 \cos{\left(u \right)})\cdot (\cos{\left(x \right)}) \\ &=4 \cos{\left(x \right)} \cos{\left(\sin{\left(x \right)} \right)}.\end{aligned}
$$

## Eligible easy / authored-easy / {'a': 4, 'b': 0, 'outer': 'sin', 'inner': 'cos'}

Find the derivative of $y=4 \sin{\left(\cos{\left(x \right)} \right)}.$

- 4 \sin{\left(x \right)} \cos{\left(\cos{\left(x \right)} \right)}
- 4 \cos{\left(\cos{\left(x \right)} \right)}
* - 4 \sin{\left(x \right)} \cos{\left(\cos{\left(x \right)} \right)}
- - 4 \sin{\left(x \right)} \cos{\left(\sin{\left(x \right)} \right)}
- - 4 \sin{\left(x \right)} \sin{\left(\cos{\left(x \right)} \right)}

First, we express $y$ as the composite function

$$
y=4 \sin{\left(u \right)},\qquad u=\cos{\left(x \right)}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=4 \cos{\left(u \right)},\qquad \frac{\text{d}u}{\text{d}x}=- \sin{\left(x \right)}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} &=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=(4 \cos{\left(u \right)})\cdot (- \sin{\left(x \right)}) \\ &=- 4 \sin{\left(x \right)} \cos{\left(\cos{\left(x \right)} \right)}.\end{aligned}
$$

## Eligible easy / authored-easy / {'a': 4, 'b': 0, 'outer': 'cos', 'inner': 'sin'}

Find the derivative of $y=4 \cos{\left(\sin{\left(x \right)} \right)}.$

- 4 \sin{\left(\sin{\left(x \right)} \right)} \cos{\left(x \right)}
- - 4 \sin{\left(\sin{\left(x \right)} \right)}
* - 4 \sin{\left(\sin{\left(x \right)} \right)} \cos{\left(x \right)}
- - 4 \sin{\left(\cos{\left(x \right)} \right)} \cos{\left(x \right)}
- 4 \cos{\left(x \right)} \cos{\left(\sin{\left(x \right)} \right)}

First, we express $y$ as the composite function

$$
y=4 \cos{\left(u \right)},\qquad u=\sin{\left(x \right)}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=- 4 \sin{\left(u \right)},\qquad \frac{\text{d}u}{\text{d}x}=\cos{\left(x \right)}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} &=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=(- 4 \sin{\left(u \right)})\cdot (\cos{\left(x \right)}) \\ &=- 4 \sin{\left(\sin{\left(x \right)} \right)} \cos{\left(x \right)}.\end{aligned}
$$

## Eligible easy / authored-easy / {'a': 4, 'b': 0, 'outer': 'cos', 'inner': 'cos'}

Find the derivative of $y=4 \cos{\left(\cos{\left(x \right)} \right)}.$

- - 4 \sin{\left(x \right)} \sin{\left(\cos{\left(x \right)} \right)}
- - 4 \sin{\left(\cos{\left(x \right)} \right)}
* 4 \sin{\left(x \right)} \sin{\left(\cos{\left(x \right)} \right)}
- 4 \sin{\left(x \right)} \sin{\left(\sin{\left(x \right)} \right)}
- - 4 \sin{\left(x \right)} \cos{\left(\cos{\left(x \right)} \right)}

First, we express $y$ as the composite function

$$
y=4 \cos{\left(u \right)},\qquad u=\cos{\left(x \right)}.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=- 4 \sin{\left(u \right)},\qquad \frac{\text{d}u}{\text{d}x}=- \sin{\left(x \right)}.
$$

We now apply the chain rule, and get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} &=\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ &=(- 4 \sin{\left(u \right)})\cdot (- \sin{\left(x \right)}) \\ &=4 \sin{\left(x \right)} \sin{\left(\cos{\left(x \right)} \right)}.\end{aligned}
$$
