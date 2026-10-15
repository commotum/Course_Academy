# Repeated chain rule private draft

Raw replay preserves omissions and is evidence-only. Easy is tentatively authored from unrated MA trig cubics. Fieldless source excluded from normal API; q342927 normal shifts bounded1..24, raw-only expanded bounds expose engine gap.

## MA original q-48569 / observed_raw

Find $f^{′}(x)$ when $f(x) = \cos^{3} 3x$.

- -9\cos^{2} 3x\sin 3x
- -9\cos^{2} x\sin x
- -3\sin^{2} 3x
- 9\sin^{2} 3x\cos 3x
- 3\cos^{2} 3x\sin 3x

## MA original q-48570 / observed_raw

Find $f^{′}(x)$ when $f(x) = \sin^{3} 4x$.

- 12\sin^{2} 4x\cos 4x
- 3\sin^{2} 4x\cos 4x
- 12\sin^{2} x\cos x
- 12\sin 4x\cos 4x
- 3\sin x\cos x

## MA original q-16699 / observed_raw

Find ${f}^{'}(1)$ when $f(x)={cos}^{3}(5{x}^{2}+2).$

First, we express $f$ as the composite function

$$
f={u}^{3},\,u=\operatorname{cos}v,\,v=5{x}^{2}+2.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=3{u}^{2},\,\frac{\text{d}u}{\text{d}v}=-\operatorname{sin}v,\,\frac{\text{d}v}{\text{d}x}=10x.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =3{u}^{2}\cdot (-\operatorname{sin}v)\cdot 10x \\  & =3(\operatorname{cos}(5{x}^{2}+2))^{2}\cdot (-\operatorname{sin}(5{x}^{2}+2))\cdot 10x \\  & =-30x{cos}^{2}(5{x}^{2}+2)\operatorname{sin}(5{x}^{2}+2)\end{aligned}
$$

Now we compute ${f}^{'}(1):$

$$
\begin{aligned}{f}^{'}(1) & =-30(1){cos}^{2}(5(1)^{2}+2)\operatorname{sin}(5(1)^{2}+2) \\  & =-30{cos}^{2}7\operatorname{sin}7\end{aligned}
$$

## MA original q-312907 / observed_raw

Find ${f}^{'}(x)$ when $f(x)={cos}^{8}(5{x}^{3}).$

${f}^{'}(x)=$
{{field-1}} ${cos}^{7}(5{x}^{3})\operatorname{sin}(5{x}^{3})$

* -120{x}^{2}

First, we express $f$ as the composite function

$$
f={u}^{8},\,u=\operatorname{cos}v,\,v=5{x}^{3}.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=8{u}^{7},\,\frac{\text{d}u}{\text{d}v}=-\operatorname{sin}v,\,\frac{\text{d}v}{\text{d}x}=15{x}^{2}.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =8{u}^{7}\cdot (-\operatorname{sin}v)\cdot 15{x}^{2} \\  & =8{(\operatorname{cos}(5{x}^{3}))}^{7}\cdot (-\operatorname{sin}(5{x}^{3}))\cdot 15{x}^{2} \\  & =-120{x}^{2}{cos}^{7}(5{x}^{3})\operatorname{sin}(5{x}^{3}).\end{aligned}
$$

## MA original q-2397 / observed_raw

Find ${f}^{′}(x)$ when $f(x)={sin}^{3}⁡(9{x}^{2}-1).$

* 54x{sin}^{2}⁡(9{x}^{2}-1)\,\operatorname{cos}⁡(9{x}^{2}-1)
- 3x{sin}^{2}⁡(9{x}^{2}-1)\,{cos}^{2}⁡(9{x}^{2}-1)
- 18x{sin}^{2}⁡(9{x}^{2}-1)\,{cos}^{2}⁡(9{x}^{2}-1)
- 18x{sin}^{2}⁡(9{x}^{2}-1)\,\operatorname{cos}⁡(9{x}^{2}-1)
- 54x{sin}^{3}⁡(9{x}^{2}-1)\,{cos}^{3}⁡(9{x}^{2}-1)

First, we express $f$ as the composite function

$$
f={u}^{3},\,u=\operatorname{sin}⁡v,\,v=9{x}^{2}-1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=3{u}^{2},\,\frac{\text{d}u}{\text{d}v}=\operatorname{cos}⁡v,\,\frac{\text{d}v}{\text{d}x}=18x.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =3{u}^{2}\cdot (\operatorname{cos}⁡v)\cdot 18x \\  & =3(\operatorname{sin}⁡(9{x}^{2}-1))^{2}\cdot (\operatorname{cos}⁡(9{x}^{2}-1))\cdot 18x \\  & =54x{sin}^{2}⁡(9{x}^{2}-1)\operatorname{cos}⁡(9{x}^{2}-1)\end{aligned}
$$

## MA original q-28655 / observed_raw

Find ${h}^{′}(0)$ when $h(x)={5}^{\operatorname{ln}⁡(\operatorname{cos}⁡x)}.$

* 0
- -1
- -5
- 5
- 1

First, we express $h$ as the composite function

$$
h={5}^{u},\,u=\operatorname{ln}⁡v\,v=\operatorname{cos}⁡x.
$$

Differentiating gives

$$
\frac{\text{d}h}{\text{d}u}={5}^{u}\operatorname{ln}⁡5,\,\frac{\text{d}u}{\text{d}v}=\frac{1}{v},\,\frac{\text{d}v}{\text{d}x}=-\operatorname{sin}⁡x.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}h}{\text{d}x} & =\frac{\text{d}h}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}h}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & ={5}^{u}\operatorname{ln}⁡5\cdot (\frac{1}{v})\cdot (-\operatorname{sin}⁡x) \\  & ={5}^{\operatorname{ln}⁡\operatorname{cos}⁡x}\operatorname{ln}⁡5\cdot (\frac{1}{\operatorname{cos}⁡x})\cdot (-\operatorname{sin}⁡x) \\  & =-{5}^{\operatorname{ln}⁡(\operatorname{cos}⁡x)}\operatorname{ln}⁡5\operatorname{tan}⁡x\end{aligned}
$$

Now we compute ${h}^{′}(0):$

$$
\begin{aligned}{h}^{′}(0) & =-{5}^{\operatorname{ln}⁡(\operatorname{cos}⁡0)}\operatorname{ln}⁡5\operatorname{tan}⁡0 \\  & =-{5}^{\operatorname{ln}⁡1}\operatorname{ln}⁡5(0) \\  & =0.\end{aligned}
$$

## MA original q-31352 / observed_raw

Find ${y}^{′}$ when $y=\operatorname{cot}⁡[(x+6)^{2}].$

* -2(x+6){csc}^{2}⁡[(x+6)^{2}]
- -{csc}^{2}⁡[(x+6)^{2}]
- 2x{csc}^{2}⁡[(x+6)^{2}]
- -2(x+6)\operatorname{csc}⁡(x+6)
- 4(x+6)

First, we express $y$ as the composite function

$$
y=\operatorname{cot}⁡u,\,u={v}^{2},\,v=x+6.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-{csc}^{2}⁡u,\,\frac{\text{d}u}{\text{d}v}=2v,\,\frac{\text{d}v}{\text{d}x}=1.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot (2v)\cdot 1 \\  & =-2(x+6){csc}^{2}⁡[(x+6)^{2}].\end{aligned}
$$

## MA original q-31361 / observed_raw

Find ${f}^{′}(0)$ when $f(x)={cot}^{4}⁡(5x-1).$

* 20{cot}^{3}⁡1{csc}^{2}⁡1
- 5{cot}^{3}⁡1{sec}^{2}⁡1
- -4{cot}^{2}⁡1{csc}^{2}⁡1
- 20\operatorname{cot}⁡1{sec}^{2}⁡1
- -4{cot}^{3}⁡1{csc}^{2}⁡1

First, we express $f$ as the composite function

$$
f={u}^{4},\,u=\operatorname{cot}⁡v,\,v=5x-1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=4{u}^{3},\,\frac{\text{d}u}{\text{d}v}=-{csc}^{2}⁡v,\,\frac{\text{d}v}{\text{d}x}=5.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =4{u}^{3}\cdot (-{csc}^{2}⁡v)\cdot 5 \\  & =4(\operatorname{cot}⁡(5x-1))^{3}\cdot (-{csc}^{2}⁡(5x-1))\cdot 5 \\  & =-20{cot}^{3}⁡(5x-1){csc}^{2}⁡(5x-1)\end{aligned}
$$

Now we compute ${f}^{′}(0):$

$$
\begin{aligned}{f}^{′}(0) & =-20{cot}^{3}⁡(5(0)-1){csc}^{2}⁡(5(0)-1) \\  & =-20{cot}^{3}⁡(-1){csc}^{2}⁡(-1) \\  & =-20(-{cot}^{3}⁡1){csc}^{2}⁡1 \\  & =20{cot}^{3}⁡1{csc}^{2}⁡1\end{aligned}
$$

## MA original q-342927 / observed_raw

Find ${y}^{′}$ when $y=\sqrt{\operatorname{cos}⁡(2x-1)}.$

| ${y}^{′}$ | $=$ | {{field-1}} |
| --- | --- | --- |
|  |  | $\sqrt{\operatorname{cos}⁡(2x-1)}$ |

* -\operatorname{sin}(2x-1)

First, we express $y$ as the composite function

$$
y=\sqrt{u},\,u=\operatorname{cos}⁡v,\,v=2x-1.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{2\sqrt{u}},\,\frac{\text{d}u}{\text{d}v}=-\operatorname{sin}⁡v,\,\frac{\text{d}v}{\text{d}x}=2.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =\frac{1}{2\sqrt{u}}\cdot (-\operatorname{sin}⁡v)\cdot 2 \\  & =\frac{1}{2\sqrt{\operatorname{cos}⁡(2x-1)}}\cdot (-\operatorname{sin}⁡(2x-1))\cdot 2 \\  & =\frac{-2\operatorname{sin}⁡(2x-1)}{2\sqrt{\operatorname{cos}⁡(2x-1)}} \\  & =\frac{-\operatorname{sin}⁡(2x-1)}{\sqrt{\operatorname{cos}⁡(2x-1)}}.\end{aligned}
$$

## Changed parameter q-48569 / source-bank

Find $f^{′}(x)$ when $f(x) = \cos^{3} 2x$.

- -3\sin^{2} 2x
- -6\cos^{2} x\sin x
* -6\cos^{2} 2x\sin 2x
- 3\cos^{2} 2x\sin 2x
- 6\sin^{2} 2x\cos 2x

First, we express $f$ as the composite function

$$
f=u^3,\,u=\cos v,\,v=2x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=3u^2,\,\frac{\text{d}u}{\text{d}v}=-\sin v,\,\frac{\text{d}v}{\text{d}x}=2.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\ & =3u^2\cdot (-\sin v)\cdot 2 \\ & =3(\cos(2x))^2\cdot (-\sin(2x))\cdot 2 \\ & =-6\cos^{2} 2x\sin 2x.\end{aligned}
$$

## Changed parameter q-48569 / source-bank

Find $f^{′}(x)$ when $f(x) = \cos^{3} 31x$.

- 93\sin^{2} 31x\cos 31x
- -3\sin^{2} 31x
- -93\cos^{2} x\sin x
* -93\cos^{2} 31x\sin 31x
- 3\cos^{2} 31x\sin 31x

First, we express $f$ as the composite function

$$
f=u^3,\,u=\cos v,\,v=31x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=3u^2,\,\frac{\text{d}u}{\text{d}v}=-\sin v,\,\frac{\text{d}v}{\text{d}x}=31.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\ & =3u^2\cdot (-\sin v)\cdot 31 \\ & =3(\cos(31x))^2\cdot (-\sin(31x))\cdot 31 \\ & =-93\cos^{2} 31x\sin 31x.\end{aligned}
$$

## Changed parameter q-48569 / observed_raw

Find $f^{′}(x)$ when $f(x) = \cos^{3} 2x$.

- -6\cos^{2} 2x\sin 2x
- -6\cos^{2} x\sin x
- -3\sin^{2} 2x
- 6\sin^{2} 2x\cos 2x
- 3\cos^{2} 2x\sin 2x

## Changed parameter q-48569 / observed_raw

Find $f^{′}(x)$ when $f(x) = \cos^{3} 31x$.

- -93\cos^{2} 31x\sin 31x
- -93\cos^{2} x\sin x
- -3\sin^{2} 31x
- 93\sin^{2} 31x\cos 31x
- 3\cos^{2} 31x\sin 31x

## Changed parameter q-48570 / source-bank

Find $f^{′}(x)$ when $f(x) = \sin^{3} 2x$.

- 6\sin^{2} x\cos x
- 3\sin^{2} 2x\cos 2x
* 6\sin^{2} 2x\cos 2x
- 3\sin x\cos x
- 6\sin 2x\cos 2x

First, we express $f$ as the composite function

$$
f=u^3,\,u=\sin v,\,v=2x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=3u^2,\,\frac{\text{d}u}{\text{d}v}=\cos v,\,\frac{\text{d}v}{\text{d}x}=2.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\ & =3u^2\cdot (\cos v)\cdot 2 \\ & =3(\sin(2x))^2\cdot (\cos(2x))\cdot 2 \\ & =6\sin^{2} 2x\cos 2x.\end{aligned}
$$

## Changed parameter q-48570 / source-bank

Find $f^{′}(x)$ when $f(x) = \sin^{3} 31x$.

- 93\sin 31x\cos 31x
- 93\sin^{2} x\cos x
- 3\sin^{2} 31x\cos 31x
* 93\sin^{2} 31x\cos 31x
- 3\sin x\cos x

First, we express $f$ as the composite function

$$
f=u^3,\,u=\sin v,\,v=31x.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=3u^2,\,\frac{\text{d}u}{\text{d}v}=\cos v,\,\frac{\text{d}v}{\text{d}x}=31.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\ & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\ & =3u^2\cdot (\cos v)\cdot 31 \\ & =3(\sin(31x))^2\cdot (\cos(31x))\cdot 31 \\ & =93\sin^{2} 31x\cos 31x.\end{aligned}
$$

## Changed parameter q-48570 / observed_raw

Find $f^{′}(x)$ when $f(x) = \sin^{3} 2x$.

- 6\sin^{2} 2x\cos 2x
- 3\sin^{2} 2x\cos 2x
- 6\sin^{2} x\cos x
- 6\sin 2x\cos 2x
- 3\sin x\cos x

## Changed parameter q-48570 / observed_raw

Find $f^{′}(x)$ when $f(x) = \sin^{3} 31x$.

- 93\sin^{2} 31x\cos 31x
- 3\sin^{2} 31x\cos 31x
- 93\sin^{2} x\cos x
- 93\sin 31x\cos 31x
- 3\sin x\cos x

## Changed parameter q-16699 / observed_raw

Find ${f}^{'}(1)$ when $f(x)={cos}^{3}(1{x}^{2}+1).$

First, we express $f$ as the composite function

$$
f={u}^{3},\,u=\operatorname{cos}v,\,v=1{x}^{2}+1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=3{u}^{2},\,\frac{\text{d}u}{\text{d}v}=-\operatorname{sin}v,\,\frac{\text{d}v}{\text{d}x}=2x.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =3{u}^{2}\cdot (-\operatorname{sin}v)\cdot 2x \\  & =3(\operatorname{cos}(1{x}^{2}+1))^{2}\cdot (-\operatorname{sin}(1{x}^{2}+1))\cdot 2x \\  & =-6x{cos}^{2}(1{x}^{2}+1)\operatorname{sin}(1{x}^{2}+1)\end{aligned}
$$

Now we compute ${f}^{'}(1):$

$$
\begin{aligned}{f}^{'}(1) & =-6(1){cos}^{2}(1(1)^{2}+1)\operatorname{sin}(1(1)^{2}+1) \\  & =-6{cos}^{2}2\operatorname{sin}2\end{aligned}
$$

## Changed parameter q-16699 / observed_raw

Find ${f}^{'}(1)$ when $f(x)={cos}^{3}(16{x}^{2}+6).$

First, we express $f$ as the composite function

$$
f={u}^{3},\,u=\operatorname{cos}v,\,v=16{x}^{2}+6.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=3{u}^{2},\,\frac{\text{d}u}{\text{d}v}=-\operatorname{sin}v,\,\frac{\text{d}v}{\text{d}x}=32x.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =3{u}^{2}\cdot (-\operatorname{sin}v)\cdot 32x \\  & =3(\operatorname{cos}(16{x}^{2}+6))^{2}\cdot (-\operatorname{sin}(16{x}^{2}+6))\cdot 32x \\  & =-96x{cos}^{2}(16{x}^{2}+6)\operatorname{sin}(16{x}^{2}+6)\end{aligned}
$$

Now we compute ${f}^{'}(1):$

$$
\begin{aligned}{f}^{'}(1) & =-96(1){cos}^{2}(16(1)^{2}+6)\operatorname{sin}(16(1)^{2}+6) \\  & =-96{cos}^{2}22\operatorname{sin}22\end{aligned}
$$

## Changed parameter q-312907 / source-blank

Find ${f}^{'}(x)$ when $f(x)={cos}^{8}(1{x}^{3}).$

${f}^{'}(x)=$
{{field-1}} ${cos}^{7}(1{x}^{3})\operatorname{sin}(1{x}^{3})$

* -24{x}^{2}

First, we express $f$ as the composite function

$$
f={u}^{8},\,u=\operatorname{cos}v,\,v=1{x}^{3}.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=8{u}^{7},\,\frac{\text{d}u}{\text{d}v}=-\operatorname{sin}v,\,\frac{\text{d}v}{\text{d}x}=3{x}^{2}.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =8{u}^{7}\cdot (-\operatorname{sin}v)\cdot 3{x}^{2} \\  & =8{(\operatorname{cos}(1{x}^{3}))}^{7}\cdot (-\operatorname{sin}(1{x}^{3}))\cdot 3{x}^{2} \\  & =-24{x}^{2}{cos}^{7}(1{x}^{3})\operatorname{sin}(1{x}^{3}).\end{aligned}
$$

## Changed parameter q-312907 / source-blank

Find ${f}^{'}(x)$ when $f(x)={cos}^{8}(31{x}^{3}).$

${f}^{'}(x)=$
{{field-1}} ${cos}^{7}(31{x}^{3})\operatorname{sin}(31{x}^{3})$

* -744{x}^{2}

First, we express $f$ as the composite function

$$
f={u}^{8},\,u=\operatorname{cos}v,\,v=31{x}^{3}.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=8{u}^{7},\,\frac{\text{d}u}{\text{d}v}=-\operatorname{sin}v,\,\frac{\text{d}v}{\text{d}x}=93{x}^{2}.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =8{u}^{7}\cdot (-\operatorname{sin}v)\cdot 93{x}^{2} \\  & =8{(\operatorname{cos}(31{x}^{3}))}^{7}\cdot (-\operatorname{sin}(31{x}^{3}))\cdot 93{x}^{2} \\  & =-744{x}^{2}{cos}^{7}(31{x}^{3})\operatorname{sin}(31{x}^{3}).\end{aligned}
$$

## Changed parameter q-312907 / observed_raw

Find ${f}^{'}(x)$ when $f(x)={cos}^{8}(1{x}^{3}).$

${f}^{'}(x)=$
{{field-1}} ${cos}^{7}(1{x}^{3})\operatorname{sin}(1{x}^{3})$

* -24{x}^{2}

First, we express $f$ as the composite function

$$
f={u}^{8},\,u=\operatorname{cos}v,\,v=1{x}^{3}.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=8{u}^{7},\,\frac{\text{d}u}{\text{d}v}=-\operatorname{sin}v,\,\frac{\text{d}v}{\text{d}x}=3{x}^{2}.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =8{u}^{7}\cdot (-\operatorname{sin}v)\cdot 3{x}^{2} \\  & =8{(\operatorname{cos}(1{x}^{3}))}^{7}\cdot (-\operatorname{sin}(1{x}^{3}))\cdot 3{x}^{2} \\  & =-24{x}^{2}{cos}^{7}(1{x}^{3})\operatorname{sin}(1{x}^{3}).\end{aligned}
$$

## Changed parameter q-312907 / observed_raw

Find ${f}^{'}(x)$ when $f(x)={cos}^{8}(31{x}^{3}).$

${f}^{'}(x)=$
{{field-1}} ${cos}^{7}(31{x}^{3})\operatorname{sin}(31{x}^{3})$

* -744{x}^{2}

First, we express $f$ as the composite function

$$
f={u}^{8},\,u=\operatorname{cos}v,\,v=31{x}^{3}.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=8{u}^{7},\,\frac{\text{d}u}{\text{d}v}=-\operatorname{sin}v,\,\frac{\text{d}v}{\text{d}x}=93{x}^{2}.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =8{u}^{7}\cdot (-\operatorname{sin}v)\cdot 93{x}^{2} \\  & =8{(\operatorname{cos}(31{x}^{3}))}^{7}\cdot (-\operatorname{sin}(31{x}^{3}))\cdot 93{x}^{2} \\  & =-744{x}^{2}{cos}^{7}(31{x}^{3})\operatorname{sin}(31{x}^{3}).\end{aligned}
$$

## Changed parameter q-2397 / source-bank

Find ${f}^{′}(x)$ when $f(x)={sin}^{3}⁡(1{x}^{2}-1).$

- 2x{sin}^{2}⁡(1{x}^{2}-1)\,{cos}^{2}⁡(1{x}^{2}-1)
- 3x{sin}^{2}⁡(1{x}^{2}-1)\,{cos}^{2}⁡(1{x}^{2}-1)
* 6x{sin}^{2}⁡(1{x}^{2}-1)\,\operatorname{cos}⁡(1{x}^{2}-1)
- 6x{sin}^{3}⁡(1{x}^{2}-1)\,{cos}^{3}⁡(1{x}^{2}-1)
- 2x{sin}^{2}⁡(1{x}^{2}-1)\,\operatorname{cos}⁡(1{x}^{2}-1)

First, we express $f$ as the composite function

$$
f={u}^{3},\,u=\operatorname{sin}⁡v,\,v=1{x}^{2}-1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=3{u}^{2},\,\frac{\text{d}u}{\text{d}v}=\operatorname{cos}⁡v,\,\frac{\text{d}v}{\text{d}x}=2x.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =3{u}^{2}\cdot (\operatorname{cos}⁡v)\cdot 2x \\  & =3(\operatorname{sin}⁡(1{x}^{2}-1))^{2}\cdot (\operatorname{cos}⁡(1{x}^{2}-1))\cdot 2x \\  & =6x{sin}^{2}⁡(1{x}^{2}-1)\operatorname{cos}⁡(1{x}^{2}-1)\end{aligned}
$$

## Changed parameter q-2397 / source-bank

Find ${f}^{′}(x)$ when $f(x)={sin}^{3}⁡(31{x}^{2}-1).$

- 3x{sin}^{2}⁡(31{x}^{2}-1)\,{cos}^{2}⁡(31{x}^{2}-1)
* 186x{sin}^{2}⁡(31{x}^{2}-1)\,\operatorname{cos}⁡(31{x}^{2}-1)
- 62x{sin}^{2}⁡(31{x}^{2}-1)\,\operatorname{cos}⁡(31{x}^{2}-1)
- 62x{sin}^{2}⁡(31{x}^{2}-1)\,{cos}^{2}⁡(31{x}^{2}-1)
- 186x{sin}^{3}⁡(31{x}^{2}-1)\,{cos}^{3}⁡(31{x}^{2}-1)

First, we express $f$ as the composite function

$$
f={u}^{3},\,u=\operatorname{sin}⁡v,\,v=31{x}^{2}-1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=3{u}^{2},\,\frac{\text{d}u}{\text{d}v}=\operatorname{cos}⁡v,\,\frac{\text{d}v}{\text{d}x}=62x.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =3{u}^{2}\cdot (\operatorname{cos}⁡v)\cdot 62x \\  & =3(\operatorname{sin}⁡(31{x}^{2}-1))^{2}\cdot (\operatorname{cos}⁡(31{x}^{2}-1))\cdot 62x \\  & =186x{sin}^{2}⁡(31{x}^{2}-1)\operatorname{cos}⁡(31{x}^{2}-1)\end{aligned}
$$

## Changed parameter q-2397 / observed_raw

Find ${f}^{′}(x)$ when $f(x)={sin}^{3}⁡(1{x}^{2}-1).$

* 6x{sin}^{2}⁡(1{x}^{2}-1)\,\operatorname{cos}⁡(1{x}^{2}-1)
- 3x{sin}^{2}⁡(1{x}^{2}-1)\,{cos}^{2}⁡(1{x}^{2}-1)
- 2x{sin}^{2}⁡(1{x}^{2}-1)\,{cos}^{2}⁡(1{x}^{2}-1)
- 2x{sin}^{2}⁡(1{x}^{2}-1)\,\operatorname{cos}⁡(1{x}^{2}-1)
- 6x{sin}^{3}⁡(1{x}^{2}-1)\,{cos}^{3}⁡(1{x}^{2}-1)

First, we express $f$ as the composite function

$$
f={u}^{3},\,u=\operatorname{sin}⁡v,\,v=1{x}^{2}-1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=3{u}^{2},\,\frac{\text{d}u}{\text{d}v}=\operatorname{cos}⁡v,\,\frac{\text{d}v}{\text{d}x}=2x.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =3{u}^{2}\cdot (\operatorname{cos}⁡v)\cdot 2x \\  & =3(\operatorname{sin}⁡(1{x}^{2}-1))^{2}\cdot (\operatorname{cos}⁡(1{x}^{2}-1))\cdot 2x \\  & =6x{sin}^{2}⁡(1{x}^{2}-1)\operatorname{cos}⁡(1{x}^{2}-1)\end{aligned}
$$

## Changed parameter q-2397 / observed_raw

Find ${f}^{′}(x)$ when $f(x)={sin}^{3}⁡(31{x}^{2}-1).$

* 186x{sin}^{2}⁡(31{x}^{2}-1)\,\operatorname{cos}⁡(31{x}^{2}-1)
- 3x{sin}^{2}⁡(31{x}^{2}-1)\,{cos}^{2}⁡(31{x}^{2}-1)
- 62x{sin}^{2}⁡(31{x}^{2}-1)\,{cos}^{2}⁡(31{x}^{2}-1)
- 62x{sin}^{2}⁡(31{x}^{2}-1)\,\operatorname{cos}⁡(31{x}^{2}-1)
- 186x{sin}^{3}⁡(31{x}^{2}-1)\,{cos}^{3}⁡(31{x}^{2}-1)

First, we express $f$ as the composite function

$$
f={u}^{3},\,u=\operatorname{sin}⁡v,\,v=31{x}^{2}-1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=3{u}^{2},\,\frac{\text{d}u}{\text{d}v}=\operatorname{cos}⁡v,\,\frac{\text{d}v}{\text{d}x}=62x.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =3{u}^{2}\cdot (\operatorname{cos}⁡v)\cdot 62x \\  & =3(\operatorname{sin}⁡(31{x}^{2}-1))^{2}\cdot (\operatorname{cos}⁡(31{x}^{2}-1))\cdot 62x \\  & =186x{sin}^{2}⁡(31{x}^{2}-1)\operatorname{cos}⁡(31{x}^{2}-1)\end{aligned}
$$

## Changed parameter q-28655 / source-compatibility

Find ${h}^{′}(0)$ when $h(x)={5}^{\operatorname{ln}⁡(\operatorname{cos}⁡x)}.$

- -5
- -1
* 0
- 1
- 5

First, we express $h$ as the composite function

$$
h={5}^{u},\,u=\operatorname{ln}⁡v\,v=\operatorname{cos}⁡x.
$$

Differentiating gives

$$
\frac{\text{d}h}{\text{d}u}={5}^{u}\operatorname{ln}⁡5,\,\frac{\text{d}u}{\text{d}v}=\frac{1}{v},\,\frac{\text{d}v}{\text{d}x}=-\operatorname{sin}⁡x.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}h}{\text{d}x} & =\frac{\text{d}h}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}h}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & ={5}^{u}\operatorname{ln}⁡5\cdot (\frac{1}{v})\cdot (-\operatorname{sin}⁡x) \\  & ={5}^{\operatorname{ln}⁡\operatorname{cos}⁡x}\operatorname{ln}⁡5\cdot (\frac{1}{\operatorname{cos}⁡x})\cdot (-\operatorname{sin}⁡x) \\  & =-{5}^{\operatorname{ln}⁡(\operatorname{cos}⁡x)}\operatorname{ln}⁡5\operatorname{tan}⁡x\end{aligned}
$$

Now we compute ${h}^{′}(0):$

$$
\begin{aligned}{h}^{′}(0) & =-{5}^{\operatorname{ln}⁡(\operatorname{cos}⁡0)}\operatorname{ln}⁡5\operatorname{tan}⁡0 \\  & =-{5}^{\operatorname{ln}⁡1}\operatorname{ln}⁡5(0) \\  & =0.\end{aligned}
$$

## Changed parameter q-28655 / observed_raw

Find ${h}^{′}(0)$ when $h(x)={2}^{\operatorname{ln}⁡(\operatorname{cos}⁡x)}.$

* 0
- -1
- -2
- 2
- 1

First, we express $h$ as the composite function

$$
h={2}^{u},\,u=\operatorname{ln}⁡v\,v=\operatorname{cos}⁡x.
$$

Differentiating gives

$$
\frac{\text{d}h}{\text{d}u}={2}^{u}\operatorname{ln}⁡2,\,\frac{\text{d}u}{\text{d}v}=\frac{1}{v},\,\frac{\text{d}v}{\text{d}x}=-\operatorname{sin}⁡x.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}h}{\text{d}x} & =\frac{\text{d}h}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}h}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & ={2}^{u}\operatorname{ln}⁡2\cdot (\frac{1}{v})\cdot (-\operatorname{sin}⁡x) \\  & ={2}^{\operatorname{ln}⁡\operatorname{cos}⁡x}\operatorname{ln}⁡2\cdot (\frac{1}{\operatorname{cos}⁡x})\cdot (-\operatorname{sin}⁡x) \\  & =-{2}^{\operatorname{ln}⁡(\operatorname{cos}⁡x)}\operatorname{ln}⁡2\operatorname{tan}⁡x\end{aligned}
$$

Now we compute ${h}^{′}(0):$

$$
\begin{aligned}{h}^{′}(0) & =-{2}^{\operatorname{ln}⁡(\operatorname{cos}⁡0)}\operatorname{ln}⁡2\operatorname{tan}⁡0 \\  & =-{2}^{\operatorname{ln}⁡1}\operatorname{ln}⁡2(0) \\  & =0.\end{aligned}
$$

## Changed parameter q-28655 / observed_raw

Find ${h}^{′}(0)$ when $h(x)={16}^{\operatorname{ln}⁡(\operatorname{cos}⁡x)}.$

* 0
- -1
- -16
- 16
- 1

First, we express $h$ as the composite function

$$
h={16}^{u},\,u=\operatorname{ln}⁡v\,v=\operatorname{cos}⁡x.
$$

Differentiating gives

$$
\frac{\text{d}h}{\text{d}u}={16}^{u}\operatorname{ln}⁡16,\,\frac{\text{d}u}{\text{d}v}=\frac{1}{v},\,\frac{\text{d}v}{\text{d}x}=-\operatorname{sin}⁡x.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}h}{\text{d}x} & =\frac{\text{d}h}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}h}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & ={16}^{u}\operatorname{ln}⁡16\cdot (\frac{1}{v})\cdot (-\operatorname{sin}⁡x) \\  & ={16}^{\operatorname{ln}⁡\operatorname{cos}⁡x}\operatorname{ln}⁡16\cdot (\frac{1}{\operatorname{cos}⁡x})\cdot (-\operatorname{sin}⁡x) \\  & =-{16}^{\operatorname{ln}⁡(\operatorname{cos}⁡x)}\operatorname{ln}⁡16\operatorname{tan}⁡x\end{aligned}
$$

Now we compute ${h}^{′}(0):$

$$
\begin{aligned}{h}^{′}(0) & =-{16}^{\operatorname{ln}⁡(\operatorname{cos}⁡0)}\operatorname{ln}⁡16\operatorname{tan}⁡0 \\  & =-{16}^{\operatorname{ln}⁡1}\operatorname{ln}⁡16(0) \\  & =0.\end{aligned}
$$

## Changed parameter q-31352 / source-bank

Find ${y}^{′}$ when $y=\operatorname{cot}⁡[(x+1)^{2}].$

- 2x{csc}^{2}⁡[(x+1)^{2}]
- -{csc}^{2}⁡[(x+1)^{2}]
* -2(x+1){csc}^{2}⁡[(x+1)^{2}]
- 4(x+1)
- -2(x+1)\operatorname{csc}⁡(x+1)

First, we express $y$ as the composite function

$$
y=\operatorname{cot}⁡u,\,u={v}^{2},\,v=x+1.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-{csc}^{2}⁡u,\,\frac{\text{d}u}{\text{d}v}=2v,\,\frac{\text{d}v}{\text{d}x}=1.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot (2v)\cdot 1 \\  & =-2(x+1){csc}^{2}⁡[(x+1)^{2}].\end{aligned}
$$

## Changed parameter q-31352 / source-bank

Find ${y}^{′}$ when $y=\operatorname{cot}⁡[(x+31)^{2}].$

- -{csc}^{2}⁡[(x+31)^{2}]
* -2(x+31){csc}^{2}⁡[(x+31)^{2}]
- -2(x+31)\operatorname{csc}⁡(x+31)
- 2x{csc}^{2}⁡[(x+31)^{2}]
- 4(x+31)

First, we express $y$ as the composite function

$$
y=\operatorname{cot}⁡u,\,u={v}^{2},\,v=x+31.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-{csc}^{2}⁡u,\,\frac{\text{d}u}{\text{d}v}=2v,\,\frac{\text{d}v}{\text{d}x}=1.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot (2v)\cdot 1 \\  & =-2(x+31){csc}^{2}⁡[(x+31)^{2}].\end{aligned}
$$

## Changed parameter q-31352 / observed_raw

Find ${y}^{′}$ when $y=\operatorname{cot}⁡[(x+1)^{2}].$

* -2(x+1){csc}^{2}⁡[(x+1)^{2}]
- -{csc}^{2}⁡[(x+1)^{2}]
- 2x{csc}^{2}⁡[(x+1)^{2}]
- -2(x+1)\operatorname{csc}⁡(x+1)
- 4(x+1)

First, we express $y$ as the composite function

$$
y=\operatorname{cot}⁡u,\,u={v}^{2},\,v=x+1.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-{csc}^{2}⁡u,\,\frac{\text{d}u}{\text{d}v}=2v,\,\frac{\text{d}v}{\text{d}x}=1.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot (2v)\cdot 1 \\  & =-2(x+1){csc}^{2}⁡[(x+1)^{2}].\end{aligned}
$$

## Changed parameter q-31352 / observed_raw

Find ${y}^{′}$ when $y=\operatorname{cot}⁡[(x+31)^{2}].$

* -2(x+31){csc}^{2}⁡[(x+31)^{2}]
- -{csc}^{2}⁡[(x+31)^{2}]
- 2x{csc}^{2}⁡[(x+31)^{2}]
- -2(x+31)\operatorname{csc}⁡(x+31)
- 4(x+31)

First, we express $y$ as the composite function

$$
y=\operatorname{cot}⁡u,\,u={v}^{2},\,v=x+31.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=-{csc}^{2}⁡u,\,\frac{\text{d}u}{\text{d}v}=2v,\,\frac{\text{d}v}{\text{d}x}=1.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =-{csc}^{2}⁡u\cdot (2v)\cdot 1 \\  & =-2(x+31){csc}^{2}⁡[(x+31)^{2}].\end{aligned}
$$

## Changed parameter q-31361 / source-bank

Find ${f}^{′}(0)$ when $f(x)={cot}^{4}⁡(1x-1).$

- -4{cot}^{2}⁡1{csc}^{2}⁡1
- 1{cot}^{3}⁡1{sec}^{2}⁡1
* 4{cot}^{3}⁡1{csc}^{2}⁡1
- -4{cot}^{3}⁡1{csc}^{2}⁡1
- 4\operatorname{cot}⁡1{sec}^{2}⁡1

First, we express $f$ as the composite function

$$
f={u}^{4},\,u=\operatorname{cot}⁡v,\,v=1x-1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=4{u}^{3},\,\frac{\text{d}u}{\text{d}v}=-{csc}^{2}⁡v,\,\frac{\text{d}v}{\text{d}x}=1.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =4{u}^{3}\cdot (-{csc}^{2}⁡v)\cdot 1 \\  & =4(\operatorname{cot}⁡(1x-1))^{3}\cdot (-{csc}^{2}⁡(1x-1))\cdot 1 \\  & =-4{cot}^{3}⁡(1x-1){csc}^{2}⁡(1x-1)\end{aligned}
$$

Now we compute ${f}^{′}(0):$

$$
\begin{aligned}{f}^{′}(0) & =-4{cot}^{3}⁡(1(0)-1){csc}^{2}⁡(1(0)-1) \\  & =-4{cot}^{3}⁡(-1){csc}^{2}⁡(-1) \\  & =-4(-{cot}^{3}⁡1){csc}^{2}⁡1 \\  & =4{cot}^{3}⁡1{csc}^{2}⁡1\end{aligned}
$$

## Changed parameter q-31361 / source-bank

Find ${f}^{′}(0)$ when $f(x)={cot}^{4}⁡(16x-6).$

- -4{cot}^{2}⁡6{csc}^{2}⁡6
* 64{cot}^{3}⁡6{csc}^{2}⁡6
- 64\operatorname{cot}⁡6{sec}^{2}⁡6
- 16{cot}^{3}⁡6{sec}^{2}⁡6
- -4{cot}^{3}⁡6{csc}^{2}⁡6

First, we express $f$ as the composite function

$$
f={u}^{4},\,u=\operatorname{cot}⁡v,\,v=16x-6.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=4{u}^{3},\,\frac{\text{d}u}{\text{d}v}=-{csc}^{2}⁡v,\,\frac{\text{d}v}{\text{d}x}=16.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =4{u}^{3}\cdot (-{csc}^{2}⁡v)\cdot 16 \\  & =4(\operatorname{cot}⁡(16x-6))^{3}\cdot (-{csc}^{2}⁡(16x-6))\cdot 16 \\  & =-64{cot}^{3}⁡(16x-6){csc}^{2}⁡(16x-6)\end{aligned}
$$

Now we compute ${f}^{′}(0):$

$$
\begin{aligned}{f}^{′}(0) & =-64{cot}^{3}⁡(16(0)-6){csc}^{2}⁡(16(0)-6) \\  & =-64{cot}^{3}⁡(-6){csc}^{2}⁡(-6) \\  & =-64(-{cot}^{3}⁡6){csc}^{2}⁡6 \\  & =64{cot}^{3}⁡6{csc}^{2}⁡6\end{aligned}
$$

## Changed parameter q-31361 / observed_raw

Find ${f}^{′}(0)$ when $f(x)={cot}^{4}⁡(1x-1).$

* 4{cot}^{3}⁡1{csc}^{2}⁡1
- 1{cot}^{3}⁡1{sec}^{2}⁡1
- -4{cot}^{2}⁡1{csc}^{2}⁡1
- 4\operatorname{cot}⁡1{sec}^{2}⁡1
- -4{cot}^{3}⁡1{csc}^{2}⁡1

First, we express $f$ as the composite function

$$
f={u}^{4},\,u=\operatorname{cot}⁡v,\,v=1x-1.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=4{u}^{3},\,\frac{\text{d}u}{\text{d}v}=-{csc}^{2}⁡v,\,\frac{\text{d}v}{\text{d}x}=1.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =4{u}^{3}\cdot (-{csc}^{2}⁡v)\cdot 1 \\  & =4(\operatorname{cot}⁡(1x-1))^{3}\cdot (-{csc}^{2}⁡(1x-1))\cdot 1 \\  & =-4{cot}^{3}⁡(1x-1){csc}^{2}⁡(1x-1)\end{aligned}
$$

Now we compute ${f}^{′}(0):$

$$
\begin{aligned}{f}^{′}(0) & =-4{cot}^{3}⁡(1(0)-1){csc}^{2}⁡(1(0)-1) \\  & =-4{cot}^{3}⁡(-1){csc}^{2}⁡(-1) \\  & =-4(-{cot}^{3}⁡1){csc}^{2}⁡1 \\  & =4{cot}^{3}⁡1{csc}^{2}⁡1\end{aligned}
$$

## Changed parameter q-31361 / observed_raw

Find ${f}^{′}(0)$ when $f(x)={cot}^{4}⁡(16x-6).$

* 64{cot}^{3}⁡6{csc}^{2}⁡6
- 16{cot}^{3}⁡6{sec}^{2}⁡6
- -4{cot}^{2}⁡6{csc}^{2}⁡6
- 64\operatorname{cot}⁡6{sec}^{2}⁡6
- -4{cot}^{3}⁡6{csc}^{2}⁡6

First, we express $f$ as the composite function

$$
f={u}^{4},\,u=\operatorname{cot}⁡v,\,v=16x-6.
$$

Differentiating gives

$$
\frac{\text{d}f}{\text{d}u}=4{u}^{3},\,\frac{\text{d}u}{\text{d}v}=-{csc}^{2}⁡v,\,\frac{\text{d}v}{\text{d}x}=16.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}f}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =4{u}^{3}\cdot (-{csc}^{2}⁡v)\cdot 16 \\  & =4(\operatorname{cot}⁡(16x-6))^{3}\cdot (-{csc}^{2}⁡(16x-6))\cdot 16 \\  & =-64{cot}^{3}⁡(16x-6){csc}^{2}⁡(16x-6)\end{aligned}
$$

Now we compute ${f}^{′}(0):$

$$
\begin{aligned}{f}^{′}(0) & =-64{cot}^{3}⁡(16(0)-6){csc}^{2}⁡(16(0)-6) \\  & =-64{cot}^{3}⁡(-6){csc}^{2}⁡(-6) \\  & =-64(-{cot}^{3}⁡6){csc}^{2}⁡6 \\  & =64{cot}^{3}⁡6{csc}^{2}⁡6\end{aligned}
$$

## Changed parameter q-342927 / source-blank

Find ${y}^{′}$ when $y=\sqrt{\operatorname{cos}⁡(2x-1)}.$

| ${y}^{′}$ | $=$ | {{field-1}} |
| --- | --- | --- |
|  |  | $\sqrt{\operatorname{cos}⁡(2x-1)}$ |

* -\operatorname{sin}(2x-1)

First, we express $y$ as the composite function

$$
y=\sqrt{u},\,u=\operatorname{cos}⁡v,\,v=2x-1.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{2\sqrt{u}},\,\frac{\text{d}u}{\text{d}v}=-\operatorname{sin}⁡v,\,\frac{\text{d}v}{\text{d}x}=2.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =\frac{1}{2\sqrt{u}}\cdot (-\operatorname{sin}⁡v)\cdot 2 \\  & =\frac{1}{2\sqrt{\operatorname{cos}⁡(2x-1)}}\cdot (-\operatorname{sin}⁡(2x-1))\cdot 2 \\  & =\frac{-2\operatorname{sin}⁡(2x-1)}{2\sqrt{\operatorname{cos}⁡(2x-1)}} \\  & =\frac{-\operatorname{sin}⁡(2x-1)}{\sqrt{\operatorname{cos}⁡(2x-1)}}.\end{aligned}
$$

## Changed parameter q-342927 / source-blank

Find ${y}^{′}$ when $y=\sqrt{\operatorname{cos}⁡(2x-24)}.$

| ${y}^{′}$ | $=$ | {{field-1}} |
| --- | --- | --- |
|  |  | $\sqrt{\operatorname{cos}⁡(2x-24)}$ |

* -\operatorname{sin}(2x-24)

First, we express $y$ as the composite function

$$
y=\sqrt{u},\,u=\operatorname{cos}⁡v,\,v=2x-24.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{2\sqrt{u}},\,\frac{\text{d}u}{\text{d}v}=-\operatorname{sin}⁡v,\,\frac{\text{d}v}{\text{d}x}=2.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =\frac{1}{2\sqrt{u}}\cdot (-\operatorname{sin}⁡v)\cdot 2 \\  & =\frac{1}{2\sqrt{\operatorname{cos}⁡(2x-24)}}\cdot (-\operatorname{sin}⁡(2x-24))\cdot 2 \\  & =\frac{-2\operatorname{sin}⁡(2x-24)}{2\sqrt{\operatorname{cos}⁡(2x-24)}} \\  & =\frac{-\operatorname{sin}⁡(2x-24)}{\sqrt{\operatorname{cos}⁡(2x-24)}}.\end{aligned}
$$

## MA original q-342927 / observed_raw

Find ${y}^{′}$ when $y=\sqrt{\operatorname{cos}⁡(2x-1)}.$

| ${y}^{′}$ | $=$ | {{field-1}} |
| --- | --- | --- |
|  |  | $\sqrt{\operatorname{cos}⁡(2x-1)}$ |

* -\operatorname{sin}(2x-1)

First, we express $y$ as the composite function

$$
y=\sqrt{u},\,u=\operatorname{cos}⁡v,\,v=2x-1.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{2\sqrt{u}},\,\frac{\text{d}u}{\text{d}v}=-\operatorname{sin}⁡v,\,\frac{\text{d}v}{\text{d}x}=2.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =\frac{1}{2\sqrt{u}}\cdot (-\operatorname{sin}⁡v)\cdot 2 \\  & =\frac{1}{2\sqrt{\operatorname{cos}⁡(2x-1)}}\cdot (-\operatorname{sin}⁡(2x-1))\cdot 2 \\  & =\frac{-2\operatorname{sin}⁡(2x-1)}{2\sqrt{\operatorname{cos}⁡(2x-1)}} \\  & =\frac{-\operatorname{sin}⁡(2x-1)}{\sqrt{\operatorname{cos}⁡(2x-1)}}.\end{aligned}
$$

## Changed parameter q-342927 / observed_raw

Find ${y}^{′}$ when $y=\sqrt{\operatorname{cos}⁡(2x-31)}.$

| ${y}^{′}$ | $=$ | {{field-1}} |
| --- | --- | --- |
|  |  | $\sqrt{\operatorname{cos}⁡(2x-31)}$ |

* -\operatorname{sin}(2x-31)

First, we express $y$ as the composite function

$$
y=\sqrt{u},\,u=\operatorname{cos}⁡v,\,v=2x-31.
$$

Differentiating gives

$$
\frac{\text{d}y}{\text{d}u}=\frac{1}{2\sqrt{u}},\,\frac{\text{d}u}{\text{d}v}=-\operatorname{sin}⁡v,\,\frac{\text{d}v}{\text{d}x}=2.
$$

Applying now the chain rule twice, we get

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}x} \\  & =\frac{\text{d}y}{\text{d}u}\cdot \frac{\text{d}u}{\text{d}v}\cdot \frac{\text{d}v}{\text{d}x} \\  & =\frac{1}{2\sqrt{u}}\cdot (-\operatorname{sin}⁡v)\cdot 2 \\  & =\frac{1}{2\sqrt{\operatorname{cos}⁡(2x-31)}}\cdot (-\operatorname{sin}⁡(2x-31))\cdot 2 \\  & =\frac{-2\operatorname{sin}⁡(2x-31)}{2\sqrt{\operatorname{cos}⁡(2x-31)}} \\  & =\frac{-\operatorname{sin}⁡(2x-31)}{\sqrt{\operatorname{cos}⁡(2x-31)}}.\end{aligned}
$$
