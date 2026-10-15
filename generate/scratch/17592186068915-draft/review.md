# KP68915 side-by-side source and served review

Basis2275; actual public generator output at source parameters and changed parameters. Seven MA sources are fidelity denominator. Four generated nonMA records are separately inventoried.

## q-10061

### Raw original

Calculate $\int \operatorname{sin}⁡(2x)\,\text{d}x.$

If we let $u=2x,$ then

$$
\frac{\text{d}u}{\text{d}x}=2\,⟹\,\text{d}x=\frac{1}{2}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}\int \operatorname{sin}⁡(2x)\,\text{d}x & =\int \operatorname{sin}⁡u\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int \operatorname{sin}⁡u\,\text{d}u \\  & =-\frac{1}{2}\operatorname{cos}⁡u+C \\  & =-\frac{1}{2}\operatorname{cos}⁡(2x)+C\end{aligned}\end{aligned}
$$

\frac{1}{2}\operatorname{cos}⁡(2x)+C
-2\operatorname{cos}⁡(2x)+C
2\operatorname{cos}⁡(2x)+C
-\frac{1}{2}\operatorname{sin}⁡(2x)+C
-\frac{1}{2}\operatorname{cos}⁡(2x)+C

### Observed source parameters

Calculate $\int \sin(2 x)\,\text{d}x.$

6acae7fe-273a-5b90-97d9-0c0b183ea2d2 $C + \frac{\cos{\left(2 x \right)}}{2}$
3f8230c5-d5a0-5207-82c5-4ae117b1c764 $C + 2 \cos{\left(2 x \right)}$
f1d488e9-7da6-5fad-a6cc-d609fc062461 $C - \frac{\cos{\left(2 x \right)}}{2}$
5284c4f5-bfba-583e-b37b-6fe2effd8287 $C - 2 \cos{\left(2 x \right)}$
c31b67f5-efa1-5959-a432-d532e837a30e $C - \frac{\sin{\left(2 x \right)}}{2}$

If we let $u=2 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=2\,⟹\,\text{d}x=\frac{1}{2}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \sin(2 x)\,\text{d}x & =\int \sin(u)\cdot \frac{1}{2}\,\text{d}u \\ & =\frac{1}{2}\int \sin(u)\,\text{d}u \\ & =- \frac{1}{2}\cos(u)+C \\ & =C - \frac{\cos{\left(2 x \right)}}{2}\end{aligned}
$$

Parameters `{"a": "2", "b": "0", "c": 1}`.

### Served changed parameters

Calculate $\int 2\sin(9 x)\,\text{d}x.$

652b52a7-fd7f-5668-aa3f-3ed0cf2c4c37 $C + \frac{2 \cos{\left(9 x \right)}}{9}$
3abddc35-5993-5f18-85a6-5c4e89c03e14 $C - \frac{2 \cos{\left(9 x \right)}}{9}$
61435b88-ce7d-5a3d-a117-deb95199e089 $C - \frac{2 \sin{\left(9 x \right)}}{9}$
61607f64-eb25-5502-aa6d-202d32967765 $C - 18 \cos{\left(9 x \right)}$
e07f24f1-190d-5ef1-b0f0-ee4112847ed6 $C + 18 \cos{\left(9 x \right)}$

If we let $u=9 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=9\,⟹\,\text{d}x=\frac{1}{9}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 2\sin(9 x)\,\text{d}x & =\int 2\sin(u)\cdot \frac{1}{9}\,\text{d}u \\ & =\frac{2}{9}\int \sin(u)\,\text{d}u \\ & =- \frac{2}{9}\cos(u)+C \\ & =C - \frac{2 \cos{\left(9 x \right)}}{9}\end{aligned}
$$

Parameters `{"a": "9", "b": "0", "c": 2}`.

### Served second changed parameters

Calculate $\int 4\sin(5 x)\,\text{d}x.$

53e3ca35-bd2a-515f-9d3f-fb5ed2ebcb70 $C - \frac{4 \cos{\left(5 x \right)}}{5}$
37d6b6c1-3f9f-59f2-ab57-7c0eda5d9a99 $C + 20 \cos{\left(5 x \right)}$
aae352e6-be47-58c2-ab3d-64ef33d46634 $C - \frac{4 \sin{\left(5 x \right)}}{5}$
1c87b359-4716-56e9-9c47-6e06f6e2e585 $C + \frac{4 \cos{\left(5 x \right)}}{5}$
58337b9f-a69c-5610-b462-1f9fb85a3456 $C - 20 \cos{\left(5 x \right)}$

If we let $u=5 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\text{d}x=\frac{1}{5}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 4\sin(5 x)\,\text{d}x & =\int 4\sin(u)\cdot \frac{1}{5}\,\text{d}u \\ & =\frac{4}{5}\int \sin(u)\,\text{d}u \\ & =- \frac{4}{5}\cos(u)+C \\ & =C - \frac{4 \cos{\left(5 x \right)}}{5}\end{aligned}
$$

Parameters `{"a": "5", "b": "0", "c": 4}`.

## q-2204

### Raw original

Calculate $\displaystyle \int\sin (5z)dz$.

[Original solution missing]

\cos (5z) + C
-\frac{1}{5}\cos (5z) + C
\frac{1}{5}\cos (5z) + C
-\frac{1}{5}\cos z + C
5\cos (5z) + C

### Observed source parameters

Calculate $\displaystyle \int \sin(5 z)\,\text{d}z$.

7970136c-1cc7-5b2e-9df4-b8c80eca8b3f $C + \cos{\left(5 z \right)}$
aace5098-82b2-59cd-bc17-bf2737c418d5 $C + \frac{\cos{\left(5 z \right)}}{5}$
ee032a5c-a104-5634-be1e-2780c467444c $C + 5 \cos{\left(5 z \right)}$
69d4aa2f-52ca-533f-ae95-10215b6b4df3 $C - \frac{\cos{\left(5 z \right)}}{5}$
185aa763-d7bc-5f02-8de1-8a380470d912 $C - \frac{\cos{\left(z \right)}}{5}$

If we let $u=5 z,$ then

$$
\frac{\text{d}u}{\text{d}z}=5\,⟹\,\text{d}z=\frac{1}{5}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \sin(5 z)\,\text{d}z & =\int \sin(u)\cdot \frac{1}{5}\,\text{d}u \\ & =\frac{1}{5}\int \sin(u)\,\text{d}u \\ & =- \frac{1}{5}\cos(u)+C \\ & =C - \frac{\cos{\left(5 z \right)}}{5}\end{aligned}
$$

Parameters `{"a": "5", "b": "0", "c": 1}`.

### Served changed parameters

Calculate $\displaystyle \int 2\sin(9 z)\,\text{d}z$.

c6319eb6-bdf2-55cb-ba78-dc25b7e07b6b $C + 2 \cos{\left(9 z \right)}$
0e584dd7-b100-5e5c-b34d-2757f087c1d5 $C + 18 \cos{\left(9 z \right)}$
b80e1d6b-8d9d-585e-9dbb-728abc72f1df $C - \frac{2 \cos{\left(z \right)}}{9}$
b8e6b76e-0ec9-5e76-a3bd-0d210b6b6c6d $C - \frac{2 \cos{\left(9 z \right)}}{9}$
13e01814-c505-5e49-9a70-7dd9edc2aac1 $C + \frac{2 \cos{\left(9 z \right)}}{9}$

If we let $u=9 z,$ then

$$
\frac{\text{d}u}{\text{d}z}=9\,⟹\,\text{d}z=\frac{1}{9}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 2\sin(9 z)\,\text{d}z & =\int 2\sin(u)\cdot \frac{1}{9}\,\text{d}u \\ & =\frac{2}{9}\int \sin(u)\,\text{d}u \\ & =- \frac{2}{9}\cos(u)+C \\ & =C - \frac{2 \cos{\left(9 z \right)}}{9}\end{aligned}
$$

Parameters `{"a": "9", "b": "0", "c": 2}`.

### Served second changed parameters

Calculate $\displaystyle \int 4\sin(5 z)\,\text{d}z$.

ce66c638-9def-568c-a40f-f6fc035a02e1 $C + 20 \cos{\left(5 z \right)}$
0ebfdd11-bf7f-5278-9fe3-501fffb2fee3 $C + \frac{4 \cos{\left(5 z \right)}}{5}$
cf2bd1a7-3a62-52fb-b363-bd23a40b718d $C - \frac{4 \cos{\left(z \right)}}{5}$
facc7918-f1c3-525e-b8b8-1a60cb7b9254 $C + 4 \cos{\left(5 z \right)}$
9ed070fe-aa7a-5f04-b8ff-59743d026ba3 $C - \frac{4 \cos{\left(5 z \right)}}{5}$

If we let $u=5 z,$ then

$$
\frac{\text{d}u}{\text{d}z}=5\,⟹\,\text{d}z=\frac{1}{5}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 4\sin(5 z)\,\text{d}z & =\int 4\sin(u)\cdot \frac{1}{5}\,\text{d}u \\ & =\frac{4}{5}\int \sin(u)\,\text{d}u \\ & =- \frac{4}{5}\cos(u)+C \\ & =C - \frac{4 \cos{\left(5 z \right)}}{5}\end{aligned}
$$

Parameters `{"a": "5", "b": "0", "c": 4}`.

## q-10064

### Raw original

Calculate $\int \operatorname{cos}⁡(3-9x)\,\text{d}x.$

If we let $u=3-9x,$ then 

$$
\frac{\text{d}u}{\text{d}x}=-9\,⟹\,\text{d}x=-\frac{1}{9}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \operatorname{cos}⁡(3-9x)\,\text{d}x & =\int \operatorname{cos}⁡u\cdot (-\frac{1}{9}\,\text{d}u) \\  & =-\frac{1}{9}\int \operatorname{cos}⁡u\,\text{d}u \\  & =-\frac{1}{9}\operatorname{sin}⁡u+C \\  & =-\frac{1}{9}\operatorname{sin}⁡(3-9x)+C\end{aligned}
$$

-\frac{1}{3}\operatorname{sin}⁡(3-9x)+C
-\frac{1}{9}\operatorname{sin}⁡(3-9x)+C
\frac{1}{9}\operatorname{cos}⁡(3-9x)+C
\frac{1}{9}\operatorname{sin}⁡(3-9x)+C
-\frac{1}{9}\operatorname{cos}⁡(3-9x)+C

### Observed source parameters

Calculate $\int \cos(3 - 9 x)\,\text{d}x.$

70a19c84-c08d-572a-8c66-74c0a02b6bca $C + \frac{\sin{\left(9 x - 3 \right)}}{3}$
12c7df79-db0d-52bc-ad70-a03362c1b596 $C + \frac{\cos{\left(9 x - 3 \right)}}{9}$
6172d26d-6710-53fe-988b-15de0689fec8 $C - \frac{\cos{\left(9 x - 3 \right)}}{9}$
78ea3933-aecc-5e81-851a-66a6aaaa7aeb $C + \frac{\sin{\left(9 x - 3 \right)}}{9}$
36185c13-340a-5074-9b89-dee82c026307 $C - \frac{\sin{\left(9 x - 3 \right)}}{9}$

If we let $u=3 - 9 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=-9\,⟹\,\text{d}x=- \frac{1}{9}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \cos(3 - 9 x)\,\text{d}x & =\int \cos(u)\cdot (- \frac{1}{9})\,\text{d}u \\ & =- \frac{1}{9}\int \cos(u)\,\text{d}u \\ & =- \frac{1}{9}\sin(u)+C \\ & =C + \frac{\sin{\left(9 x - 3 \right)}}{9}\end{aligned}
$$

Parameters `{"a": "-9", "b": "3", "c": 1}`.

### Served changed parameters

Calculate $\int \cos(4 - 10 x)\,\text{d}x.$

f689af02-a665-51b1-941d-e334c362b9d8 $C + \frac{\sin{\left(10 x - 4 \right)}}{4}$
e9d7fe9d-034f-58d1-936c-60c412c8f8b8 $C - \frac{\cos{\left(10 x - 4 \right)}}{10}$
d36593b3-43a3-5e18-8cb7-95046bcfdb58 $C - \frac{\sin{\left(10 x - 4 \right)}}{10}$
715e83f0-fd9a-5a87-90ee-2e769832a235 $C + \frac{\sin{\left(10 x - 4 \right)}}{10}$
19ebe00b-1854-5d79-92c9-8d56a1ad1a63 $C + \frac{\cos{\left(10 x - 4 \right)}}{10}$

If we let $u=4 - 10 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=-10\,⟹\,\text{d}x=- \frac{1}{10}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \cos(4 - 10 x)\,\text{d}x & =\int \cos(u)\cdot (- \frac{1}{10})\,\text{d}u \\ & =- \frac{1}{10}\int \cos(u)\,\text{d}u \\ & =- \frac{1}{10}\sin(u)+C \\ & =C + \frac{\sin{\left(10 x - 4 \right)}}{10}\end{aligned}
$$

Parameters `{"a": "-10", "b": "4", "c": 1}`.

### Served second changed parameters

Calculate $\int \cos(4 - 7 x)\,\text{d}x.$

bf03d6d0-dc0d-5d45-9f97-18b81ec0372f $C - \frac{\cos{\left(7 x - 4 \right)}}{7}$
65f101ed-e72d-5d89-8777-68d23c6d527f $C + \frac{\cos{\left(7 x - 4 \right)}}{7}$
83acc049-b573-54d6-9499-75ac068278c2 $C - \frac{\sin{\left(7 x - 4 \right)}}{7}$
9c6efe4d-7af9-52a6-9226-9702b8e11577 $C + \frac{\sin{\left(7 x - 4 \right)}}{4}$
db3a1462-4cb7-5b64-823f-03f40623caab $C + \frac{\sin{\left(7 x - 4 \right)}}{7}$

If we let $u=4 - 7 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=-7\,⟹\,\text{d}x=- \frac{1}{7}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \cos(4 - 7 x)\,\text{d}x & =\int \cos(u)\cdot (- \frac{1}{7})\,\text{d}u \\ & =- \frac{1}{7}\int \cos(u)\,\text{d}u \\ & =- \frac{1}{7}\sin(u)+C \\ & =C + \frac{\sin{\left(7 x - 4 \right)}}{7}\end{aligned}
$$

Parameters `{"a": "-7", "b": "4", "c": 1}`.

## q-350040

### Raw original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /4}9\operatorname{sin}⁡(2x)\,\text{d}x=$

{{field-1}}

If we let $u=2x,$ then

$$
\frac{\text{d}u}{\text{d}x}=2\,⟹\,\text{d}x=\frac{1}{2}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\pi /4$ |
| --- | --- | --- |
| $u$ | $0$ | $\pi /2$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\pi /4}9\operatorname{sin}⁡(2x)\,\text{d}x & ={\int }_{0}^{\pi /2}9\operatorname{sin}⁡u\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{9}{2}{\int }_{0}^{\pi /2}\operatorname{sin}⁡u\,\text{d}u \\  & =-\frac{9}{2}\operatorname{cos}⁡u{|}_{0}^{\pi /2} \\  & =-\frac{9}{2}(\operatorname{cos}⁡(\frac{\pi }{2})-\operatorname{cos}⁡(0)) \\  & =-\frac{9}{2}(0-1) \\  & =\frac{9}{2}\end{aligned}
$$

\frac{9}{2}

### Observed source parameters

Evaluate the following integral. Do not round the answer.

$\int_{0}^{\frac{\pi}{4}} 9\sin(2 x)\,\text{d}x=$

{{field-1}}

b6930e6b-938a-50d3-a83f-48426d9d0d8c $\frac{9}{2}$

If we let $u=2 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=2\,⟹\,\text{d}x=\frac{1}{2}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{\pi}{4}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\pi}{4}} 9\sin(2 x)\,\text{d}x & =\int_{0}^{\frac{\pi}{2}} 9\sin(u)\cdot \frac{1}{2}\,\text{d}u \\ & =\frac{9}{2}\int_{0}^{\frac{\pi}{2}} \sin(u)\,\text{d}u \\ & =- \frac{9}{2}\cos(u)\big|_{0}^{\frac{\pi}{2}} \\ & =- \frac{9}{2}(\cos(\frac{\pi}{2})-\cos(0)) \\ & =- \frac{9}{2}(0-1) \\ & =\frac{9}{2}\end{aligned}
$$

Parameters `{"a": "2", "b": "0", "c": 9, "hi": "1/2", "lo": "0"}`.

### Served changed parameters

Evaluate the following integral. Give an exact answer.

$\int_{0}^{\frac{\pi}{15}} 3\sin(5 x)\,\text{d}x=$

{{field-1}}

71518bbe-908f-5e3d-8085-221c962223c6 $\frac{3}{10}$

If we let $u=5 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\text{d}x=\frac{1}{5}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{\pi}{15}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi}{3}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\pi}{15}} 3\sin(5 x)\,\text{d}x & =\int_{0}^{\frac{\pi}{3}} 3\sin(u)\cdot \frac{1}{5}\,\text{d}u \\ & =\frac{3}{5}\int_{0}^{\frac{\pi}{3}} \sin(u)\,\text{d}u \\ & =- \frac{3}{5}\cos(u)\big|_{0}^{\frac{\pi}{3}} \\ & =- \frac{3}{5}(\cos(\frac{\pi}{3})-\cos(0)) \\ & =- \frac{3}{5}(\frac{1}{2}-1) \\ & =\frac{3}{10}\end{aligned}
$$

Parameters `{"a": "5", "b": "0", "c": 3, "hi": "1/3", "lo": "0"}`.

### Served second changed parameters

Evaluate the following integral. Give an exact answer.

$\int_{0}^{\frac{2 \pi}{15}} 2\sin(5 x)\,\text{d}x=$

{{field-1}}

e948faae-a8ad-50b2-81a6-2e648c34628d $\frac{3}{5}$

If we let $u=5 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\text{d}x=\frac{1}{5}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{2 \pi}{15}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{2 \pi}{3}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{2 \pi}{15}} 2\sin(5 x)\,\text{d}x & =\int_{0}^{\frac{2 \pi}{3}} 2\sin(u)\cdot \frac{1}{5}\,\text{d}u \\ & =\frac{2}{5}\int_{0}^{\frac{2 \pi}{3}} \sin(u)\,\text{d}u \\ & =- \frac{2}{5}\cos(u)\big|_{0}^{\frac{2 \pi}{3}} \\ & =- \frac{2}{5}(\cos(\frac{2 \pi}{3})-\cos(0)) \\ & =- \frac{2}{5}(- \frac{1}{2}-1) \\ & =\frac{3}{5}\end{aligned}
$$

Parameters `{"a": "5", "b": "0", "c": 2, "hi": "2/3", "lo": "0"}`.

## q-13647

### Raw original

${\int }_{0}^{\pi /8}5\operatorname{sin}⁡(4x)\,\text{d}x=$

If we let $u=4x,$ then

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\text{d}x=\frac{1}{4}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\pi /8$ |
| --- | --- | --- |
| $u$ | $0$ | $\pi /2$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{0}^{\pi /8}5\operatorname{sin}⁡(4x)\,\text{d}x & ={\int }_{0}^{\pi /2}5\operatorname{sin}⁡u\cdot \frac{1}{4}\,\text{d}u \\  & =\frac{5}{4}{\int }_{0}^{\pi /2}\operatorname{sin}⁡u\,\text{d}u \\  & =-\frac{5}{4}\operatorname{cos}⁡u{|}_{0}^{\pi /2} \\  & =-\frac{5}{4}(\operatorname{cos}⁡(\frac{\pi }{2})-\operatorname{cos}⁡(0)) \\  & =-\frac{5}{4}(0-1) \\  & =\frac{5}{4}\end{aligned}\end{aligned}
$$

0
\frac{5}{4}
-\frac{5}{4}
1
-1

### Observed source parameters

$\int_{0}^{\frac{\pi}{8}} 5\sin(4 x)\,\text{d}x=$

9c755e13-d955-5459-9d9d-2ea242be6770 $0$
2ed56f39-76b8-5a0f-ab0d-8e0556146e08 $- \frac{5}{4}$
44793ed0-0db8-55ce-92d8-decf996ab314 $-1$
b5783d63-8a0c-5924-9964-60bea4576bcd $\frac{5}{4}$
eb918f8f-a623-5a7c-be40-a9e45edcd418 $1$

If we let $u=4 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\text{d}x=\frac{1}{4}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{\pi}{8}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\pi}{8}} 5\sin(4 x)\,\text{d}x & =\int_{0}^{\frac{\pi}{2}} 5\sin(u)\cdot \frac{1}{4}\,\text{d}u \\ & =\frac{5}{4}\int_{0}^{\frac{\pi}{2}} \sin(u)\,\text{d}u \\ & =- \frac{5}{4}\cos(u)\big|_{0}^{\frac{\pi}{2}} \\ & =- \frac{5}{4}(\cos(\frac{\pi}{2})-\cos(0)) \\ & =- \frac{5}{4}(0-1) \\ & =\frac{5}{4}\end{aligned}
$$

Parameters `{"a": "4", "b": "0", "c": 5, "hi": "1/2", "lo": "0"}`.

### Served changed parameters

$\int_{0}^{\frac{\pi}{15}} 3\sin(5 x)\,\text{d}x=$

41b19e8a-e4ba-5124-bee6-e6932cbeb3ac $0$
a90fa379-d802-54ed-9e75-2c25750663d5 $-1$
8360143e-8086-55c6-9e9c-d1e0cb879f3d $1$
dbaa1ba1-5ef5-50c2-b179-ca04165e1b99 $\frac{3}{10}$
914f6c13-818d-5a4b-a6aa-83d392da2a77 $- \frac{3}{10}$

If we let $u=5 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\text{d}x=\frac{1}{5}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{\pi}{15}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi}{3}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\pi}{15}} 3\sin(5 x)\,\text{d}x & =\int_{0}^{\frac{\pi}{3}} 3\sin(u)\cdot \frac{1}{5}\,\text{d}u \\ & =\frac{3}{5}\int_{0}^{\frac{\pi}{3}} \sin(u)\,\text{d}u \\ & =- \frac{3}{5}\cos(u)\big|_{0}^{\frac{\pi}{3}} \\ & =- \frac{3}{5}(\cos(\frac{\pi}{3})-\cos(0)) \\ & =- \frac{3}{5}(\frac{1}{2}-1) \\ & =\frac{3}{10}\end{aligned}
$$

Parameters `{"a": "5", "b": "0", "c": 3, "hi": "1/3", "lo": "0"}`.

### Served second changed parameters

$\int_{0}^{\frac{2 \pi}{15}} 2\sin(5 x)\,\text{d}x=$

906d0aed-f413-5e19-a1f4-2b8709875984 $-1$
d003a6ab-ae6a-5622-809d-023be7fdd4ad $- \frac{3}{5}$
87748169-3fc7-5379-b1ab-db2a22a98c2b $1$
780ff47a-ff59-51fb-9588-e1cdd73cfdd8 $0$
82da8474-c07b-525b-b5a1-2fb5e98e840c $\frac{3}{5}$

If we let $u=5 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\text{d}x=\frac{1}{5}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{2 \pi}{15}$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{2 \pi}{3}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{2 \pi}{15}} 2\sin(5 x)\,\text{d}x & =\int_{0}^{\frac{2 \pi}{3}} 2\sin(u)\cdot \frac{1}{5}\,\text{d}u \\ & =\frac{2}{5}\int_{0}^{\frac{2 \pi}{3}} \sin(u)\,\text{d}u \\ & =- \frac{2}{5}\cos(u)\big|_{0}^{\frac{2 \pi}{3}} \\ & =- \frac{2}{5}(\cos(\frac{2 \pi}{3})-\cos(0)) \\ & =- \frac{2}{5}(- \frac{1}{2}-1) \\ & =\frac{3}{5}\end{aligned}
$$

Parameters `{"a": "5", "b": "0", "c": 2, "hi": "2/3", "lo": "0"}`.

## q-346081

### Raw original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{2}\operatorname{cos}⁡(\frac{\pi x}{4})\,\text{d}x=$
{{field-1}}

If we let $u=\frac{\pi x}{4},$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{\pi }{4}\,⟹\,\text{d}x=\frac{4}{\pi }\,\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $2$ |
| --- | --- | --- |
| $u$ | $0$ | $\pi /2$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{2}\operatorname{cos}⁡(\frac{\pi x}{4})\,\text{d}x & ={\int }_{0}^{\pi /2}\operatorname{cos}⁡u\cdot \frac{4}{\pi }\,\text{d}u \\  & =\frac{4}{\pi }{\int }_{0}^{\pi /2}\operatorname{cos}⁡u\,\text{d}u \\  & =\frac{4}{\pi }\operatorname{sin}⁡u\,{|}_{0}^{\pi /2} \\  & =\frac{4}{\pi }(\operatorname{sin}⁡(\frac{\pi }{2})-\operatorname{sin}⁡(0)) \\  & =\frac{4}{\pi }(1-0) \\  & =\frac{4}{\pi }\end{aligned}
$$

\frac{4}{\pi }

### Observed source parameters

Evaluate the following integral. Do not round the answer.

$\int_{0}^{2} \cos(\frac{\pi x}{4})\,\text{d}x=$
{{field-1}}

d176ca13-aa50-5b04-8ce5-cba4edd159f2 $\frac{4}{\pi}$

If we let $u=\frac{\pi x}{4},$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{\pi}{4}\,⟹\,\text{d}x=\frac{4}{\pi}\,\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $2$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi}{2}$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{2} \cos(\frac{\pi x}{4})\,\text{d}x & =\int_{0}^{\frac{\pi}{2}} \cos(u)\cdot \frac{4}{\pi}\,\text{d}u \\ & =\frac{4}{\pi}\int_{0}^{\frac{\pi}{2}} \cos(u)\,\text{d}u \\ & =\frac{4}{\pi}\sin(u)\big|_{0}^{\frac{\pi}{2}} \\ & =\frac{4}{\pi}(\sin(\frac{\pi}{2})-\sin(0)) \\ & =\frac{4}{\pi}(1-0) \\ & =\frac{4}{\pi}\end{aligned}
$$

Parameters `{"a": "1/4", "b": "0", "c": 1, "hi": "1/2", "lo": "0"}`.

### Served changed parameters

Evaluate the following integral. Give an exact answer.

$\int_{0}^{1} 4\cos(\frac{\pi x}{2})\,\text{d}x=$
{{field-1}}

de5cd5e2-d8bd-54d5-8290-1c6297a8ccdf $\frac{8}{\pi}$

If we let $u=\frac{\pi x}{2},$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{\pi}{2}\,⟹\,\text{d}x=\frac{2}{\pi}\,\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi}{2}$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{1} 4\cos(\frac{\pi x}{2})\,\text{d}x & =\int_{0}^{\frac{\pi}{2}} 4\cos(u)\cdot \frac{2}{\pi}\,\text{d}u \\ & =\frac{8}{\pi}\int_{0}^{\frac{\pi}{2}} \cos(u)\,\text{d}u \\ & =\frac{8}{\pi}\sin(u)\big|_{0}^{\frac{\pi}{2}} \\ & =\frac{8}{\pi}(\sin(\frac{\pi}{2})-\sin(0)) \\ & =\frac{8}{\pi}(1-0) \\ & =\frac{8}{\pi}\end{aligned}
$$

Parameters `{"a": "1/2", "b": "0", "c": 4, "hi": "1/2", "lo": "0"}`.

### Served second changed parameters

Evaluate the following integral. Give an exact answer.

$\int_{0}^{1} 4\cos(\frac{\pi x}{3})\,\text{d}x=$
{{field-1}}

8132ccc2-3343-583c-b70a-85a930a73efc $\frac{6 \sqrt{3}}{\pi}$

If we let $u=\frac{\pi x}{3},$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{\pi}{3}\,⟹\,\text{d}x=\frac{3}{\pi}\,\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $1$ |
| --- | --- | --- |
| $u$ | $0$ | $\frac{\pi}{3}$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{1} 4\cos(\frac{\pi x}{3})\,\text{d}x & =\int_{0}^{\frac{\pi}{3}} 4\cos(u)\cdot \frac{3}{\pi}\,\text{d}u \\ & =\frac{12}{\pi}\int_{0}^{\frac{\pi}{3}} \cos(u)\,\text{d}u \\ & =\frac{12}{\pi}\sin(u)\big|_{0}^{\frac{\pi}{3}} \\ & =\frac{12}{\pi}(\sin(\frac{\pi}{3})-\sin(0)) \\ & =\frac{12}{\pi}(\frac{\sqrt{3}}{2}-0) \\ & =\frac{6 \sqrt{3}}{\pi}\end{aligned}
$$

Parameters `{"a": "1/3", "b": "0", "c": 4, "hi": "1/3", "lo": "0"}`.

## q-10574

### Raw original

Calculate ${\int }_{0}^{\pi /9}\operatorname{sin}⁡(3x+\frac{\pi }{3})\,\text{d}x.$

If we let $u=3x+\frac{\pi }{3},$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\pi /9$ |
| --- | --- | --- |
| $u$ | $\pi /3$ | $2\pi /3$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\begin{aligned}{\int }_{0}^{\pi /9}\operatorname{sin}⁡(3x+\frac{\pi }{3})\,\text{d}x & ={\int }_{\pi /3}^{2\pi /3}\operatorname{sin}⁡u\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{1}{3}{\int }_{\pi /3}^{2\pi /3}\operatorname{sin}⁡u\,\text{d}u \\  & =-\frac{1}{3}\operatorname{cos}⁡u{|}_{\pi /3}^{2\pi /3} \\  & =-\frac{1}{3}(\operatorname{cos}⁡(\frac{2\pi }{3})-\operatorname{cos}⁡(\frac{\pi }{3})) \\  & =-\frac{1}{3}(-\frac{1}{2}-\frac{1}{2}) \\  & =\frac{1}{3}\end{aligned}\end{aligned}
$$

\frac{1}{2}
\frac{1}{3}
\frac{2}{3}
\frac{1}{6}
\frac{3}{2}

### Observed source parameters

Calculate $\int_{0}^{\frac{\pi}{9}} \sin(3 x + \frac{\pi}{3})\,\text{d}x.$

ec7d6371-b215-537f-99cb-7a074d1d6c08 $\frac{1}{2}$
85eaaae0-8400-59ea-9a78-1bdd6e08fb85 $\frac{2}{3}$
a777d448-f77f-525a-904e-7ce17ec74195 $\frac{3}{2}$
3f256a8a-65bb-5b21-83b0-b9041ec7c8cd $\frac{1}{3}$
eb6b8b07-a126-5c26-b8ce-72ec6548c5ae $\frac{1}{6}$

If we let $u=3 x + \frac{\pi}{3},$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{\pi}{9}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{3}$ | $\frac{2 \pi}{3}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\pi}{9}} \sin(3 x + \frac{\pi}{3})\,\text{d}x & =\int_{\frac{\pi}{3}}^{\frac{2 \pi}{3}} \sin(u)\cdot \frac{1}{3}\,\text{d}u \\ & =\frac{1}{3}\int_{\frac{\pi}{3}}^{\frac{2 \pi}{3}} \sin(u)\,\text{d}u \\ & =- \frac{1}{3}\cos(u)\big|_{\frac{\pi}{3}}^{\frac{2 \pi}{3}} \\ & =- \frac{1}{3}(\cos(\frac{2 \pi}{3})-\cos(\frac{\pi}{3})) \\ & =- \frac{1}{3}(- \frac{1}{2}-\frac{1}{2}) \\ & =\frac{1}{3}\end{aligned}
$$

Parameters `{"a": "3", "b": "1/3", "c": 1, "hi": "2/3", "lo": "1/3"}`.

### Served changed parameters

Calculate $\int_{\frac{2 \pi}{9}}^{\frac{\pi}{3}} 3\sin(3 x - \frac{\pi}{6})\,\text{d}x.$

de4c7cf3-3c06-54fe-bf5c-7ed80afd7375 $\frac{3 \sqrt{3}}{4}$
f3088dcc-fdce-5673-8089-747d31e5286c $\frac{9 \sqrt{3}}{4}$
68b22d49-479a-50e9-ac3a-17375129b81d $\frac{\sqrt{3}}{4}$
435fba7b-1d0a-5e00-a129-3572f3a1c0ad $\frac{\sqrt{3}}{2}$
2df9babb-6f41-5026-b0ac-21c5cf476cca $\sqrt{3}$

If we let $u=3 x - \frac{\pi}{6},$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{2 \pi}{9}$ | $\frac{\pi}{3}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{2}$ | $\frac{5 \pi}{6}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{2 \pi}{9}}^{\frac{\pi}{3}} 3\sin(3 x - \frac{\pi}{6})\,\text{d}x & =\int_{\frac{\pi}{2}}^{\frac{5 \pi}{6}} 3\sin(u)\cdot \frac{1}{3}\,\text{d}u \\ & =\int_{\frac{\pi}{2}}^{\frac{5 \pi}{6}} \sin(u)\,\text{d}u \\ & =-\cos(u)\big|_{\frac{\pi}{2}}^{\frac{5 \pi}{6}} \\ & =-(\cos(\frac{5 \pi}{6})-\cos(\frac{\pi}{2})) \\ & =-(- \frac{\sqrt{3}}{2}-0) \\ & =\frac{\sqrt{3}}{2}\end{aligned}
$$

Parameters `{"a": "3", "b": "-1/6", "c": 3, "hi": "5/6", "lo": "1/2"}`.

### Served second changed parameters

Calculate $\int_{\frac{\pi}{15}}^{\frac{2 \pi}{15}} 3\sin(5 x - \frac{\pi}{6})\,\text{d}x.$

deaf5a0a-f364-5a9c-9d2c-105c17cf88d4 $\frac{15 \sqrt{3}}{4}$
cb5decd0-26d7-52e3-9fae-85255f483463 $\frac{3 \sqrt{3}}{5}$
7cd99d4d-8a4b-567d-913e-e0a720d0e949 $\frac{3 \sqrt{3}}{20}$
d111a272-c7a8-5f98-8ae0-86af05b1d713 $\frac{3 \sqrt{3}}{4}$
d96d1945-339f-57b2-b828-add839bf08d2 $\frac{3 \sqrt{3}}{10}$

If we let $u=5 x - \frac{\pi}{6},$ then

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\text{d}x=\frac{1}{5}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{\pi}{15}$ | $\frac{2 \pi}{15}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{6}$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{\pi}{15}}^{\frac{2 \pi}{15}} 3\sin(5 x - \frac{\pi}{6})\,\text{d}x & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} 3\sin(u)\cdot \frac{1}{5}\,\text{d}u \\ & =\frac{3}{5}\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \sin(u)\,\text{d}u \\ & =- \frac{3}{5}\cos(u)\big|_{\frac{\pi}{6}}^{\frac{\pi}{2}} \\ & =- \frac{3}{5}(\cos(\frac{\pi}{2})-\cos(\frac{\pi}{6})) \\ & =- \frac{3}{5}(0-\frac{\sqrt{3}}{2}) \\ & =\frac{3 \sqrt{3}}{10}\end{aligned}
$$

Parameters `{"a": "5", "b": "-1/6", "c": 3, "hi": "1/2", "lo": "1/6"}`.

## Authored hard: provisional rating

Calculate $\int_{\frac{2 \pi}{9}}^{\frac{\pi}{3}} 3\sin(3 x - \frac{\pi}{6})\,\text{d}x.$

a5de85b4-ff5e-5d0f-8e7f-c5103ebec42e $\frac{3 \sqrt{3}}{4}$
c38d5d29-b5d1-5a2f-9455-a581080e52b8 $\frac{9 \sqrt{3}}{4}$
ec44ce78-b547-5e5a-88a9-d8e4d2a434dc $\frac{\sqrt{3}}{4}$
2f0dc13d-b015-526d-8b0a-c4516ade86b3 $\frac{\sqrt{3}}{2}$
f447d415-7f9a-5c5a-bae3-3ff50879a10b $\sqrt{3}$

If we let $u=3 x - \frac{\pi}{6},$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{2 \pi}{9}$ | $\frac{\pi}{3}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{2}$ | $\frac{5 \pi}{6}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{2 \pi}{9}}^{\frac{\pi}{3}} 3\sin(3 x - \frac{\pi}{6})\,\text{d}x & =\int_{\frac{\pi}{2}}^{\frac{5 \pi}{6}} 3\sin(u)\cdot \frac{1}{3}\,\text{d}u \\ & =\int_{\frac{\pi}{2}}^{\frac{5 \pi}{6}} \sin(u)\,\text{d}u \\ & =-\cos(u)\big|_{\frac{\pi}{2}}^{\frac{5 \pi}{6}} \\ & =-(\cos(\frac{5 \pi}{6})-\cos(\frac{\pi}{2})) \\ & =-(- \frac{\sqrt{3}}{2}-0) \\ & =\frac{\sqrt{3}}{2}\end{aligned}
$$

Same shifted definite source backbone as moderate q10574. No hard-source evidence or added steps claimed.

## Authored hard: provisional rating

Calculate $\int_{\frac{\pi}{15}}^{\frac{2 \pi}{15}} 3\sin(5 x - \frac{\pi}{6})\,\text{d}x.$

b9259ede-c0b9-5577-a193-d3971205ee1c $\frac{15 \sqrt{3}}{4}$
440e3c69-cf13-5390-b919-421df6f214e6 $\frac{3 \sqrt{3}}{5}$
16df38fd-a190-596d-8daf-9a0f1eb52e4d $\frac{3 \sqrt{3}}{20}$
bf984381-58f4-5c9e-bd58-a2e2bf6a9e6e $\frac{3 \sqrt{3}}{4}$
4ba8f948-a3c3-5b10-a33e-606bd1f88876 $\frac{3 \sqrt{3}}{10}$

If we let $u=5 x - \frac{\pi}{6},$ then

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\text{d}x=\frac{1}{5}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{\pi}{15}$ | $\frac{2 \pi}{15}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{6}$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{\pi}{15}}^{\frac{2 \pi}{15}} 3\sin(5 x - \frac{\pi}{6})\,\text{d}x & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} 3\sin(u)\cdot \frac{1}{5}\,\text{d}u \\ & =\frac{3}{5}\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \sin(u)\,\text{d}u \\ & =- \frac{3}{5}\cos(u)\big|_{\frac{\pi}{6}}^{\frac{\pi}{2}} \\ & =- \frac{3}{5}(\cos(\frac{\pi}{2})-\cos(\frac{\pi}{6})) \\ & =- \frac{3}{5}(0-\frac{\sqrt{3}}{2}) \\ & =\frac{3 \sqrt{3}}{10}\end{aligned}
$$

Same shifted definite source backbone as moderate q10574. No hard-source evidence or added steps claimed.
