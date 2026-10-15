# KP68916 source and served variant review

Basis2275. Raw source wrapper is immutable evidence; all generated records below come through the public generator. Observed profile preserves exact-answer wording; method profile uses Give an exact answer for the native grader.

## q-10143

### Original

Calculate the integral $\int \operatorname{sec}⁡(7x)\operatorname{tan}⁡(7x)\,\text{d}x.$

If we let $u=7x,$ then

$$
\frac{\text{d}u}{\text{d}x}=7\,⟹\,\text{d}x=\frac{1}{7}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \operatorname{sec}⁡(7x)\operatorname{tan}⁡(7x)\,\text{d}x & =\int \operatorname{sec}⁡u\operatorname{tan}⁡u\cdot \frac{1}{7}\,\text{d}u \\  & =\frac{1}{7}\int \operatorname{sec}⁡u\operatorname{tan}⁡u\,\text{d}u \\  & =\frac{1}{7}\operatorname{sec}⁡u+C \\  & =\frac{1}{7}\operatorname{sec}⁡(7x)+C\end{aligned}
$$

$\frac{1}{7}\operatorname{sec}⁡(7x)+C$
$\operatorname{sec}⁡(7x)+C$
$-7\operatorname{sec}⁡(7x)+C$
$-\frac{1}{7}\operatorname{sec}⁡(7x)+C$
$7\operatorname{sec}⁡(7x)+C$

### Observed source parameters

Calculate the integral $\int \sec(7 x)\tan(7 x)\,\text{d}x.$

1532655d-5327-5d07-b339-0af4ab6b7b75 $C - 7 \sec{\left(7 x \right)}$
f5e576df-8c75-5179-8d62-440dd28bb3d0 $C + \sec{\left(7 x \right)}$
b6a827b9-e2bd-5462-810c-1a13f9c61444 $C + \frac{\sec{\left(7 x \right)}}{7}$
58a77cf7-3437-502b-967b-3c878beb7b89 $C + 7 \sec{\left(7 x \right)}$
54a8123d-04b9-50b6-bce0-af7b4b688c57 $C - \frac{\sec{\left(7 x \right)}}{7}$

If we let $u=7 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=7\,⟹\,\text{d}x=\frac{1}{7}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \sec(7 x)\tan(7 x)\,\text{d}x & =\int \sec(u)\tan(u)\cdot \frac{1}{7}\,\text{d}u \\ & =\frac{1}{7}\int \sec(u)\tan(u)\,\text{d}u \\ & =\frac{1}{7}\sec(u)+C \\ & =C + \frac{\sec{\left(7 x \right)}}{7}\end{aligned}
$$

### Served changed-parameter variant seed321

Calculate the integral $\int 5\sec(3 x)\tan(3 x)\,\text{d}x.$

dd8725d6-4df3-56f5-a877-57c71d20e9b0 $C - \frac{5 \sec{\left(3 x \right)}}{3}$
a0cdca74-fea8-5c05-b6d9-7e85779671ef $C + 15 \sec{\left(3 x \right)}$
973633df-570f-56e0-b2d4-94e300308880 $C + 5 \sec{\left(3 x \right)}$
9ff2ed7c-52e4-5443-bd03-535a58e0e713 $C + \frac{5 \sec{\left(3 x \right)}}{3}$
cbd3b9e7-bbdf-5013-a73b-d1dbe9068b7d $C - 15 \sec{\left(3 x \right)}$

If we let $u=3 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 5\sec(3 x)\tan(3 x)\,\text{d}x & =\int 5\sec(u)\tan(u)\cdot \frac{1}{3}\,\text{d}u \\ & =\frac{5}{3}\int \sec(u)\tan(u)\,\text{d}u \\ & =\frac{5}{3}\sec(u)+C \\ & =C + \frac{5 \sec{\left(3 x \right)}}{3}\end{aligned}
$$

Parameters: `{"a": "3", "b": "0", "c": 5}`.

### Served changed-parameter variant seed654

Calculate the integral $\int 2\sec(10 x)\tan(10 x)\,\text{d}x.$

d8dd80f9-06fe-5efc-b665-130cbd6e4694 $C - \frac{\sec{\left(10 x \right)}}{5}$
b82d8162-a3bf-5ca3-807e-60139c25386a $C + 20 \sec{\left(10 x \right)}$
32572e97-f4c4-5e9b-a72d-067cb5f34041 $C - 20 \sec{\left(10 x \right)}$
277fc570-e487-5430-a353-bba8aad16cae $C + \frac{\sec{\left(10 x \right)}}{5}$
3b875ba8-9b10-58de-8e3f-ff6790f63297 $C + 2 \sec{\left(10 x \right)}$

If we let $u=10 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=10\,⟹\,\text{d}x=\frac{1}{10}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 2\sec(10 x)\tan(10 x)\,\text{d}x & =\int 2\sec(u)\tan(u)\cdot \frac{1}{10}\,\text{d}u \\ & =\frac{1}{5}\int \sec(u)\tan(u)\,\text{d}u \\ & =\frac{1}{5}\sec(u)+C \\ & =C + \frac{\sec{\left(10 x \right)}}{5}\end{aligned}
$$

Parameters: `{"a": "10", "b": "0", "c": 2}`.

## q-10157

### Original

Calculate the integral $\displaystyle \int\csc (8x)\cot (8x)dx$.

[Missing original solution]

$\csc (8x) + C$
$\frac{1}{8}\csc (8x) + C$
$8\csc (8x) + C$
$-\frac{1}{8}\csc (8x) + C$
$-8\csc (8x) + C$

### Observed source parameters

Calculate the integral $\int \csc(8 x)\cot(8 x)\,\text{d}x.$

d787c54d-9b2b-5f1b-b0eb-25405a1a90d9 $C + 8 \csc{\left(8 x \right)}$
6a9a881c-73ff-5ee5-a116-f496fbd269ec $C + \frac{\csc{\left(8 x \right)}}{8}$
467b0606-2800-58bf-b09d-6ffaa4a43e8a $C + \csc{\left(8 x \right)}$
58a15004-9b32-55e7-a400-428d7d9f885e $C - 8 \csc{\left(8 x \right)}$
d11c5093-2f21-50b0-8548-0f45e84e41af $C - \frac{\csc{\left(8 x \right)}}{8}$

If we let $u=8 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=8\,⟹\,\text{d}x=\frac{1}{8}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \csc(8 x)\cot(8 x)\,\text{d}x & =\int \csc(u)\cot(u)\cdot \frac{1}{8}\,\text{d}u \\ & =\frac{1}{8}\int \csc(u)\cot(u)\,\text{d}u \\ & =- \frac{1}{8}\csc(u)+C \\ & =C - \frac{\csc{\left(8 x \right)}}{8}\end{aligned}
$$

### Served changed-parameter variant seed321

Calculate the integral $\int 5\csc(3 x)\cot(3 x)\,\text{d}x.$

38b910fc-2200-5f27-b97d-f8170e2b9f37 $C - \frac{5 \csc{\left(3 x \right)}}{3}$
7bd6bf54-61f0-5d4c-9dae-8030355b3bf4 $C - 15 \csc{\left(3 x \right)}$
89a4e7b4-0cbd-5593-9484-727e582095bc $C + \frac{5 \csc{\left(3 x \right)}}{3}$
43dd5c14-1a71-5541-9b1d-c8178ba3412c $C + 5 \csc{\left(3 x \right)}$
b8a3e27d-e4bc-53a3-a991-710971fe3351 $C + 15 \csc{\left(3 x \right)}$

If we let $u=3 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 5\csc(3 x)\cot(3 x)\,\text{d}x & =\int 5\csc(u)\cot(u)\cdot \frac{1}{3}\,\text{d}u \\ & =\frac{5}{3}\int \csc(u)\cot(u)\,\text{d}u \\ & =- \frac{5}{3}\csc(u)+C \\ & =C - \frac{5 \csc{\left(3 x \right)}}{3}\end{aligned}
$$

Parameters: `{"a": "3", "b": "0", "c": 5}`.

### Served changed-parameter variant seed654

Calculate the integral $\int 2\csc(10 x)\cot(10 x)\,\text{d}x.$

caeb52d8-a4fb-587e-9ba4-b5d15b35901e $C - \frac{\csc{\left(10 x \right)}}{5}$
74b38a3a-c76d-5e42-98d2-c169e6a89e4a $C - 20 \csc{\left(10 x \right)}$
6e3c8b8f-9545-5754-b3ba-1c5d319c57bd $C + 20 \csc{\left(10 x \right)}$
78a38b59-16c6-53ac-a612-a333f912373b $C + 2 \csc{\left(10 x \right)}$
82d59f03-db21-533a-8e90-e0d37255307f $C + \frac{\csc{\left(10 x \right)}}{5}$

If we let $u=10 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=10\,⟹\,\text{d}x=\frac{1}{10}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 2\csc(10 x)\cot(10 x)\,\text{d}x & =\int 2\csc(u)\cot(u)\cdot \frac{1}{10}\,\text{d}u \\ & =\frac{1}{5}\int \csc(u)\cot(u)\,\text{d}u \\ & =- \frac{1}{5}\csc(u)+C \\ & =C - \frac{\csc{\left(10 x \right)}}{5}\end{aligned}
$$

Parameters: `{"a": "10", "b": "0", "c": 2}`.

## q-113983

### Original

Calculate the integral $\int ({sec}^{2}⁡x+1)\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x.$

If we let $u=\operatorname{sec}⁡x,$ then

$$
\frac{\text{d}u}{\text{d}x}=\operatorname{sec}⁡x\operatorname{tan}⁡x\,⟹\,\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x=\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int ({sec}^{2}⁡x+1)\operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x & =\int ({u}^{2}+1)\,\text{d}u \\  & =\frac{{u}^{3}}{3}+u+C \\  & =\frac{{sec}^{3}⁡x}{3}+\operatorname{sec}⁡x+C\end{aligned}
$$

$\frac{{tan}^{3}⁡x}{3}+\operatorname{tan}⁡x+C$
$\frac{{sec}^{2}⁡x}{2}+C$
$\frac{{sec}^{3}⁡x}{3}+\operatorname{sec}⁡x+C$
$\frac{{sec}^{3}⁡x}{3}+C$
$\frac{{tan}^{3}⁡x}{3}+\operatorname{sec}⁡x+C$

### Observed source parameters

Calculate the integral $\int (\sec^{2}(x)+1)\sec(x)\tan(x)\,\text{d}x.$

2f99c212-c1fd-5b60-912b-cf6acc13133c $C + \frac{\sec^{3}{\left(x \right)}}{3} + \sec{\left(x \right)}$
4e776f91-3367-5e50-8fc2-207295eaaa41 $C + \frac{\sec^{2}{\left(x \right)}}{2}$
bfd73a4f-4e29-5c54-99a8-bad9a400e2cf $C + \frac{\tan^{3}{\left(x \right)}}{3} + \tan{\left(x \right)}$
7b366a66-baec-51f1-9b29-8d483988c4b1 $C + \frac{\tan^{3}{\left(x \right)}}{3} + \sec{\left(x \right)}$
49f98300-556d-5420-89cb-e243a05c82ce $C + \frac{\sec^{3}{\left(x \right)}}{3}$

If we let $u=\sec(x),$ then

$$
\frac{\text{d}u}{\text{d}x}=\sec(x)\tan(x)\,⟹\,\sec(x)\tan(x)\,\text{d}x=\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int (\sec^{2}(x)+1)\sec(x)\tan(x)\,\text{d}x & =\int (u^{2}+1)\,\text{d}u \\ & =\frac{1}{3}u^{3}+u+C \\ & =\frac{1}{3}\sec^{3}(x)+\sec(x)+C\end{aligned}
$$

This nonlinear source is reference-only at original parameters and is excluded from ordinary inventory; no nonlinear variants are authorized by the linear-argument curriculum.

## q-2203

### Original

$\int \operatorname{sec}⁡(10x)\operatorname{tan}⁡(10x)\,\text{d}x=$

If we let $u=10x,$ then

$$
\frac{\text{d}u}{\text{d}x}=10\,⟹\,\text{d}x=\frac{1}{10}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \operatorname{sec}⁡(10x)\operatorname{tan}⁡(10x)\,\text{d}x & =\int \operatorname{sec}⁡u\operatorname{tan}⁡u\cdot \frac{1}{10}\,\text{d}u \\  & =\frac{1}{10}\int \operatorname{sec}⁡u\operatorname{tan}⁡u\,\text{d}u \\  & =\frac{1}{10}\operatorname{sec}⁡u+C \\  & =\frac{1}{10}\operatorname{sec}⁡(10x)+C\end{aligned}
$$

$10\operatorname{sec}⁡(10x)+C$
$\frac{1}{10}\operatorname{csc}⁡(10x)+C$
${sec}^{2}⁡(10x)+C$
$\frac{1}{10}\operatorname{sec}⁡x+C$
$\frac{1}{10}\operatorname{sec}⁡(10x)+C$

### Observed source parameters

$\int \sec(10 x)\tan(10 x)\,\text{d}x=$

38805875-f5f6-55f7-9724-4dfc0df97c37 $C + \sec^{2}{\left(10 x \right)}$
21c559b1-021a-556a-ae29-12f8b69c4ff8 $C + \frac{\csc{\left(10 x \right)}}{10}$
326adfbf-8c83-527e-a1b3-f5c9058c6fd7 $C + 10 \sec{\left(10 x \right)}$
a9d563e3-0676-56c1-9828-1f0445ed8cf8 $C + \frac{\sec{\left(10 x \right)}}{10}$
127b819f-7cf4-5e6f-8fa3-243a1746e208 $C + \frac{\sec{\left(x \right)}}{10}$

If we let $u=10 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=10\,⟹\,\text{d}x=\frac{1}{10}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \sec(10 x)\tan(10 x)\,\text{d}x & =\int \sec(u)\tan(u)\cdot \frac{1}{10}\,\text{d}u \\ & =\frac{1}{10}\int \sec(u)\tan(u)\,\text{d}u \\ & =\frac{1}{10}\sec(u)+C \\ & =C + \frac{\sec{\left(10 x \right)}}{10}\end{aligned}
$$

### Served changed-parameter variant seed321

$\int 5\sec(3 x)\tan(3 x)\,\text{d}x=$

947f598e-040b-5cdc-a854-021c4f36852e $C + \frac{5 \sec{\left(x \right)}}{3}$
ece08b74-c6f1-57d1-b128-4c72a12229a3 $C + \frac{5 \sec{\left(3 x \right)}}{3}$
0ceb07ed-bd55-5a94-92e7-a84665b287b2 $C + \frac{5 \csc{\left(3 x \right)}}{3}$
ea968615-f842-53c5-986b-8fd03e9a9806 $C + 15 \sec{\left(3 x \right)}$
9319063c-99c6-53cc-90c7-d3c82c920a71 $C + 5 \sec^{2}{\left(3 x \right)}$

If we let $u=3 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 5\sec(3 x)\tan(3 x)\,\text{d}x & =\int 5\sec(u)\tan(u)\cdot \frac{1}{3}\,\text{d}u \\ & =\frac{5}{3}\int \sec(u)\tan(u)\,\text{d}u \\ & =\frac{5}{3}\sec(u)+C \\ & =C + \frac{5 \sec{\left(3 x \right)}}{3}\end{aligned}
$$

Parameters: `{"a": "3", "b": "0", "c": 5}`.

### Served changed-parameter variant seed654

$\int 2\sec(10 x)\tan(10 x)\,\text{d}x=$

24fc823f-e14a-5506-b994-76fb47e0b158 $C + \frac{\sec{\left(x \right)}}{5}$
f015ccb2-65d4-54e3-be59-0fedc0e91219 $C + \frac{\sec{\left(10 x \right)}}{5}$
fbaae0cc-dda2-552c-a350-c426b4b777d3 $C + 2 \sec^{2}{\left(10 x \right)}$
d910a77e-1d3e-5858-974a-2ce2273814bb $C + 20 \sec{\left(10 x \right)}$
3bc17d7c-cd8a-58f9-aab8-65cc9cfa8f07 $C + \frac{\csc{\left(10 x \right)}}{5}$

If we let $u=10 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=10\,⟹\,\text{d}x=\frac{1}{10}\text{d}u.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int 2\sec(10 x)\tan(10 x)\,\text{d}x & =\int 2\sec(u)\tan(u)\cdot \frac{1}{10}\,\text{d}u \\ & =\frac{1}{5}\int \sec(u)\tan(u)\,\text{d}u \\ & =\frac{1}{5}\sec(u)+C \\ & =C + \frac{\sec{\left(10 x \right)}}{5}\end{aligned}
$$

Parameters: `{"a": "10", "b": "0", "c": 2}`.

## q-13663

### Original

Evaluate the integral ${\int }_{\pi /9}^{\pi /6}2{csc}^{2}⁡(3x)\,\text{d}x.$

If we let $u=3x,$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\pi /9$ | $\pi /6$ |
| --- | --- | --- |
| $u$ | $\pi /3$ | $\pi /2$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{\pi /9}^{\pi /6}2{csc}^{2}⁡(3x)\,\text{d}x & ={\int }_{\pi /3}^{\pi /2}2{csc}^{2}⁡u\cdot \frac{1}{3}\,\text{d}u \\  & =\frac{2}{3}{\int }_{\pi /3}^{\pi /2}{csc}^{2}⁡u\,\text{d}u \\  & =-\frac{2}{3}\operatorname{cot}⁡u{|}_{\pi /3}^{\pi /2} \\  & =-\frac{2}{3}(\operatorname{cot}⁡(\frac{\pi }{2})-\operatorname{cot}⁡(\frac{\pi }{3})) \\  & =-\frac{2}{3}(0-\frac{\sqrt{3}}{3}) \\  & =\frac{2\sqrt{3}}{9}\end{aligned}
$$

$-\frac{\sqrt{3}}{2}$
$2\sqrt{3}$
$-\frac{2\sqrt{3}}{3}$
$\frac{2\sqrt{3}}{9}$
$\frac{\sqrt{3}}{3}$

### Observed source parameters

Evaluate the integral $\int_{\frac{\pi}{9}}^{\frac{\pi}{6}} 2\csc^{2}(3 x)\,\text{d}x.$

c7730210-008c-551c-b966-bdf10ab9cc67 $- \frac{2 \sqrt{3}}{3}$
f83dfedb-6cf6-502d-9ad7-81e638b7f367 $2 \sqrt{3}$
1c1f0f3a-79e2-59bc-8ef3-ed8301188747 $- \frac{\sqrt{3}}{2}$
bd37b9dd-c10e-5d30-820d-1a10f6a32d24 $\frac{\sqrt{3}}{3}$
6ea4e152-1deb-53ff-8604-88281568e7a7 $\frac{2 \sqrt{3}}{9}$

If we let $u=3 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{\pi}{9}$ | $\frac{\pi}{6}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{3}$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{\pi}{9}}^{\frac{\pi}{6}} 2\csc^{2}(3 x)\,\text{d}x & =\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 2\csc^{2}(u)\cdot \frac{1}{3}\,\text{d}u \\ & =\frac{2}{3}\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \csc^{2}(u)\,\text{d}u \\ & =- \frac{2}{3}\cot(u)\big|_{\frac{\pi}{3}}^{\frac{\pi}{2}} \\ & =- \frac{2}{3}(\cot(\frac{\pi}{2})-\cot(\frac{\pi}{3})) \\ & =- \frac{2}{3}(0-\frac{\sqrt{3}}{3}) \\ & =\frac{2 \sqrt{3}}{9}\end{aligned}
$$

### Served changed-parameter variant seed321

Evaluate the integral $\int_{\frac{\pi}{18}}^{\frac{\pi}{12}} 2\csc^{2}(6 x)\,\text{d}x.$

e8706643-d525-5220-9141-b0a43b12858b $\frac{\sqrt{3}}{3}$
7f7b6f06-35d2-5cf5-a41c-93b7d02340b2 $- \sqrt{3}$
c664b3a4-f9e9-5405-a25a-69f7060c66fb $4 \sqrt{3}$
5a59d215-bc9c-5c83-b928-bb26f60c239a $\frac{\sqrt{3}}{9}$
65465254-24b1-5ab7-9bff-b15a5e8bfa74 $- \frac{2 \sqrt{3}}{3}$

If we let $u=6 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=6\,⟹\,\text{d}x=\frac{1}{6}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{\pi}{18}$ | $\frac{\pi}{12}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{3}$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{\pi}{18}}^{\frac{\pi}{12}} 2\csc^{2}(6 x)\,\text{d}x & =\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 2\csc^{2}(u)\cdot \frac{1}{6}\,\text{d}u \\ & =\frac{1}{3}\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \csc^{2}(u)\,\text{d}u \\ & =- \frac{1}{3}\cot(u)\big|_{\frac{\pi}{3}}^{\frac{\pi}{2}} \\ & =- \frac{1}{3}(\cot(\frac{\pi}{2})-\cot(\frac{\pi}{3})) \\ & =- \frac{1}{3}(0-\frac{\sqrt{3}}{3}) \\ & =\frac{\sqrt{3}}{9}\end{aligned}
$$

Parameters: `{"a": "6", "b": "0", "c": 2, "hi": "1/2", "lo": "1/3"}`.

### Served changed-parameter variant seed654

Evaluate the integral $\int_{\frac{\pi}{12}}^{\frac{\pi}{6}} 4\csc^{2}(3 x)\,\text{d}x.$

4447aed1-0363-531f-a2bd-99781b1e5d63 $\frac{4}{3}$
dc6266c2-b66e-5688-9719-f393f6023ecb $-4$
f0795885-b87c-5990-851c-30bc0cfebe53 $1$
e1271c7f-aac0-5e08-afd6-053fa7b20294 $12$
c0d33736-c6f4-5536-a8fc-f84bcf580398 $- \frac{3}{4}$

If we let $u=3 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{\pi}{12}$ | $\frac{\pi}{6}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{4}$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{\pi}{12}}^{\frac{\pi}{6}} 4\csc^{2}(3 x)\,\text{d}x & =\int_{\frac{\pi}{4}}^{\frac{\pi}{2}} 4\csc^{2}(u)\cdot \frac{1}{3}\,\text{d}u \\ & =\frac{4}{3}\int_{\frac{\pi}{4}}^{\frac{\pi}{2}} \csc^{2}(u)\,\text{d}u \\ & =- \frac{4}{3}\cot(u)\big|_{\frac{\pi}{4}}^{\frac{\pi}{2}} \\ & =- \frac{4}{3}(\cot(\frac{\pi}{2})-\cot(\frac{\pi}{4})) \\ & =- \frac{4}{3}(0-1) \\ & =\frac{4}{3}\end{aligned}
$$

Parameters: `{"a": "3", "b": "0", "c": 4, "hi": "1/2", "lo": "1/4"}`.

## q-355818

### Original

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /20}^{\pi /10}5{csc}^{2}⁡(5x)\,\text{d}x=$
{{field-1}}

If we let $u=5x,$ then

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\text{d}x=\frac{1}{5}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\pi /20$ | $\pi /10$ |
| --- | --- | --- |
| $u$ | $\pi /4$ | $\pi /2$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{\pi /20}^{\pi /10}5{csc}^{2}⁡(5x)\,\text{d}x & ={\int }_{\pi /4}^{\pi /2}5{csc}^{2}⁡(u)\cdot \frac{1}{5}\,\text{d}u \\  & ={\int }_{\pi /4}^{\pi /2}{csc}^{2}⁡(u)\,\text{d}u \\  & =-\operatorname{cot}⁡(u){|}_{\pi /4}^{\pi /2} \\  & =-(\operatorname{cot}⁡(\frac{\pi }{2})-\operatorname{cot}⁡(\frac{\pi }{4})) \\  & =-(0-1) \\  & =1\end{aligned}
$$

$1$

### Observed source parameters

Evaluate the following integral. Do not round the answer.

$\int_{\frac{\pi}{20}}^{\frac{\pi}{10}} 5\csc^{2}(5 x)\,\text{d}x=$
{{field-1}}

76ea5264-381f-5c91-94b7-1b048e4d732a $1$

If we let $u=5 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=5\,⟹\,\text{d}x=\frac{1}{5}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{\pi}{20}$ | $\frac{\pi}{10}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{4}$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{\pi}{20}}^{\frac{\pi}{10}} 5\csc^{2}(5 x)\,\text{d}x & =\int_{\frac{\pi}{4}}^{\frac{\pi}{2}} 5\csc^{2}(u)\cdot \frac{1}{5}\,\text{d}u \\ & =\int_{\frac{\pi}{4}}^{\frac{\pi}{2}} \csc^{2}(u)\,\text{d}u \\ & =-\cot(u)\big|_{\frac{\pi}{4}}^{\frac{\pi}{2}} \\ & =-(\cot(\frac{\pi}{2})-\cot(\frac{\pi}{4})) \\ & =-(0-1) \\ & =1\end{aligned}
$$

### Served changed-parameter variant seed321

Evaluate the following integral. Give an exact answer.

$\int_{\frac{\pi}{18}}^{\frac{\pi}{12}} 2\csc^{2}(6 x)\,\text{d}x=$
{{field-1}}

3fd6e5b2-caa6-57b3-a2e6-270ab0581380 $\frac{\sqrt{3}}{9}$

If we let $u=6 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=6\,⟹\,\text{d}x=\frac{1}{6}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{\pi}{18}$ | $\frac{\pi}{12}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{3}$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{\pi}{18}}^{\frac{\pi}{12}} 2\csc^{2}(6 x)\,\text{d}x & =\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} 2\csc^{2}(u)\cdot \frac{1}{6}\,\text{d}u \\ & =\frac{1}{3}\int_{\frac{\pi}{3}}^{\frac{\pi}{2}} \csc^{2}(u)\,\text{d}u \\ & =- \frac{1}{3}\cot(u)\big|_{\frac{\pi}{3}}^{\frac{\pi}{2}} \\ & =- \frac{1}{3}(\cot(\frac{\pi}{2})-\cot(\frac{\pi}{3})) \\ & =- \frac{1}{3}(0-\frac{\sqrt{3}}{3}) \\ & =\frac{\sqrt{3}}{9}\end{aligned}
$$

Parameters: `{"a": "6", "b": "0", "c": 2, "hi": "1/2", "lo": "1/3"}`.

### Served changed-parameter variant seed654

Evaluate the following integral. Give an exact answer.

$\int_{\frac{\pi}{12}}^{\frac{\pi}{6}} 4\csc^{2}(3 x)\,\text{d}x=$
{{field-1}}

bcd1006a-5f1c-538b-a091-72328cd0f65d $\frac{4}{3}$

If we let $u=3 x,$ then

$$
\frac{\text{d}u}{\text{d}x}=3\,⟹\,\text{d}x=\frac{1}{3}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{\pi}{12}$ | $\frac{\pi}{6}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{4}$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{\pi}{12}}^{\frac{\pi}{6}} 4\csc^{2}(3 x)\,\text{d}x & =\int_{\frac{\pi}{4}}^{\frac{\pi}{2}} 4\csc^{2}(u)\cdot \frac{1}{3}\,\text{d}u \\ & =\frac{4}{3}\int_{\frac{\pi}{4}}^{\frac{\pi}{2}} \csc^{2}(u)\,\text{d}u \\ & =- \frac{4}{3}\cot(u)\big|_{\frac{\pi}{4}}^{\frac{\pi}{2}} \\ & =- \frac{4}{3}(\cot(\frac{\pi}{2})-\cot(\frac{\pi}{4})) \\ & =- \frac{4}{3}(0-1) \\ & =\frac{4}{3}\end{aligned}
$$

Parameters: `{"a": "3", "b": "0", "c": 4, "hi": "1/2", "lo": "1/4"}`.

## q-346368

### Original

Evaluate the following integral. Do not round the answer.

${\int }_{2\pi /3}^{2\pi }\operatorname{csc}⁡(\frac{x}{4})\operatorname{cot}⁡(\frac{x}{4})\,\text{d}x=$
{{field-1}}

If we let $u=\frac{x}{4},$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{4}\,⟹\,\text{d}x=4\,\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $2\pi /3$ | $2\pi $ |
| --- | --- | --- |
| $u$ | $\pi /6$ | $\pi /2$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{2\pi /3}^{2\pi }\operatorname{csc}⁡(\frac{x}{4})\operatorname{cot}⁡(\frac{x}{4})\,\text{d}x & ={\int }_{\pi /6}^{\pi /2}\operatorname{csc}⁡(u)\operatorname{cot}⁡(u)\cdot 4\,\text{d}u \\  & =4{\int }_{\pi /6}^{\pi /2}\operatorname{csc}⁡(u)\operatorname{cot}⁡(u)\,\text{d}u \\  & =4(-\operatorname{csc}⁡(u))\,{|}_{\pi /6}^{\pi /2} \\  & =4(-\operatorname{csc}⁡(\frac{\pi }{2})+\operatorname{csc}⁡(\frac{\pi }{6})) \\  & =4(-1+2) \\  & =4\end{aligned}
$$

$4$

### Observed source parameters

Evaluate the following integral. Do not round the answer.

$\int_{\frac{2 \pi}{3}}^{2 \pi} \csc(\frac{x}{4})\cot(\frac{x}{4})\,\text{d}x=$
{{field-1}}

9c0b3e0b-33f8-5b49-859d-be8fb5c1f040 $4$

If we let $u=\frac{x}{4},$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{4}\,⟹\,\text{d}x=4\,\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{2 \pi}{3}$ | $2 \pi$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{6}$ | $\frac{\pi}{2}$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{2 \pi}{3}}^{2 \pi} \csc(\frac{x}{4})\cot(\frac{x}{4})\,\text{d}x & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \csc(u)\cot(u)\cdot 4\,\text{d}u \\ & =4\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \csc(u)\cot(u)\,\text{d}u \\ & =4(-\csc(u))\big|_{\frac{\pi}{6}}^{\frac{\pi}{2}} \\ & =4(-\csc(\frac{\pi}{2})+\csc(\frac{\pi}{6})) \\ & =4(-1+2) \\ & =4\end{aligned}
$$

### Served changed-parameter variant seed321

Evaluate the following integral. Give an exact answer.

$\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}} 6\csc(\frac{x}{3})\cot(\frac{x}{3})\,\text{d}x=$
{{field-1}}

24d4a5cc-e519-579c-9d6a-6d6b7d0884f9 $18$

If we let $u=\frac{x}{3},$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{3}\,⟹\,\text{d}x=3\,\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{\pi}{2}$ | $\frac{3 \pi}{2}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{6}$ | $\frac{\pi}{2}$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{\pi}{2}}^{\frac{3 \pi}{2}} 6\csc(\frac{x}{3})\cot(\frac{x}{3})\,\text{d}x & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} 6\csc(u)\cot(u)\cdot 3\,\text{d}u \\ & =18\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \csc(u)\cot(u)\,\text{d}u \\ & =18(-\csc(u))\big|_{\frac{\pi}{6}}^{\frac{\pi}{2}} \\ & =18(-\csc(\frac{\pi}{2})+\csc(\frac{\pi}{6})) \\ & =18(-1+2) \\ & =18\end{aligned}
$$

Parameters: `{"a": "1/3", "b": "0", "c": 6, "hi": "1/2", "lo": "1/6"}`.

### Served changed-parameter variant seed654

Evaluate the following integral. Give an exact answer.

$\int_{\frac{3 \pi}{4}}^{\frac{3 \pi}{2}} 3\csc(\frac{x}{3})\cot(\frac{x}{3})\,\text{d}x=$
{{field-1}}

232aaa71-b85d-54bc-9b67-4d224ef9ded6 $-9 + 9 \sqrt{2}$

If we let $u=\frac{x}{3},$ then

$$
\frac{\text{d}u}{\text{d}x}=\frac{1}{3}\,⟹\,\text{d}x=3\,\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{3 \pi}{4}$ | $\frac{3 \pi}{2}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{4}$ | $\frac{\pi}{2}$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{3 \pi}{4}}^{\frac{3 \pi}{2}} 3\csc(\frac{x}{3})\cot(\frac{x}{3})\,\text{d}x & =\int_{\frac{\pi}{4}}^{\frac{\pi}{2}} 3\csc(u)\cot(u)\cdot 3\,\text{d}u \\ & =9\int_{\frac{\pi}{4}}^{\frac{\pi}{2}} \csc(u)\cot(u)\,\text{d}u \\ & =9(-\csc(u))\big|_{\frac{\pi}{4}}^{\frac{\pi}{2}} \\ & =9(-\csc(\frac{\pi}{2})+\csc(\frac{\pi}{4})) \\ & =9(-1+\sqrt{2}) \\ & =-9 + 9 \sqrt{2}\end{aligned}
$$

Parameters: `{"a": "1/3", "b": "0", "c": 3, "hi": "1/2", "lo": "1/4"}`.

## q-350060

### Original

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /4}3{sec}^{2}⁡(x-\frac{\pi }{4})\,\text{d}x=$
{{field-1}}

If we let $u=x-\frac{\pi }{4},$ then

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}x=\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\pi /4$ |
| --- | --- | --- |
| $u$ | $-\pi /4$ | $0$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\pi /4}3{sec}^{2}⁡(x-\frac{\pi }{4})\,\text{d}x & =3{\int }_{-\pi /4}^{0}{sec}^{2}⁡(u)\,\text{d}u \\  & =3\operatorname{tan}⁡(u){|}_{-\pi /4}^{0} \\  & =3(0-(-1)) \\  & =3\end{aligned}
$$

$3$

### Observed source parameters

Evaluate the following integral. Do not round the answer.

$\int_{0}^{\frac{\pi}{4}} 3\sec^{2}(x - \frac{\pi}{4})\,\text{d}x=$
{{field-1}}

8d19445d-d334-59e5-89d8-0c5030295ff5 $3$

If we let $u=x - \frac{\pi}{4},$ then

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}x=\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{\pi}{4}$ |
| --- | --- | --- |
| $u$ | $- \frac{\pi}{4}$ | $0$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\pi}{4}} 3\sec^{2}(x - \frac{\pi}{4})\,\text{d}x & =3\int_{- \frac{\pi}{4}}^{0} \sec^{2}(u)\,\text{d}u \\ & =3\tan(u)\big|_{- \frac{\pi}{4}}^{0} \\ & =3(0-(-1)) \\ & =3\end{aligned}
$$

### Served changed-parameter variant seed321

Evaluate the following integral. Give an exact answer.

$\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}} 2\sec^{2}(x + \frac{\pi}{4})\,\text{d}x=$
{{field-1}}

2d24bb8c-d2ae-524c-803e-88068b92cc30 $2$

If we let $u=x + \frac{\pi}{4},$ then

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}x=\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $- \frac{\pi}{2}$ | $- \frac{\pi}{4}$ |
| --- | --- | --- |
| $u$ | $- \frac{\pi}{4}$ | $0$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{- \frac{\pi}{2}}^{- \frac{\pi}{4}} 2\sec^{2}(x + \frac{\pi}{4})\,\text{d}x & =2\int_{- \frac{\pi}{4}}^{0} \sec^{2}(u)\,\text{d}u \\ & =2\tan(u)\big|_{- \frac{\pi}{4}}^{0} \\ & =2(0-(-1)) \\ & =2\end{aligned}
$$

Parameters: `{"a": "1", "b": "1/4", "c": 2, "hi": "0", "lo": "-1/4"}`.

### Served changed-parameter variant seed654

Evaluate the following integral. Give an exact answer.

$\int_{- \frac{5 \pi}{48}}^{- \frac{\pi}{24}} \sec^{2}(4 x + \frac{\pi}{6})\,\text{d}x=$
{{field-1}}

57164b53-98fd-57a5-94ce-2a4a626151a7 $\frac{1}{4}$

If we let $u=4 x + \frac{\pi}{6},$ then

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\text{d}x=\frac{1}{4}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $- \frac{5 \pi}{48}$ | $- \frac{\pi}{24}$ |
| --- | --- | --- |
| $u$ | $- \frac{\pi}{4}$ | $0$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{- \frac{5 \pi}{48}}^{- \frac{\pi}{24}} \sec^{2}(4 x + \frac{\pi}{6})\,\text{d}x & =\frac{1}{4}\int_{- \frac{\pi}{4}}^{0} \sec^{2}(u)\,\text{d}u \\ & =\frac{1}{4}\tan(u)\big|_{- \frac{\pi}{4}}^{0} \\ & =\frac{1}{4}(0-(-1)) \\ & =\frac{1}{4}\end{aligned}
$$

Parameters: `{"a": "4", "b": "1/6", "c": 1, "hi": "0", "lo": "-1/4"}`.

## q-350071

### Original

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /3}^{2\pi /3}4\operatorname{csc}⁡(x-\frac{\pi }{6})\operatorname{cot}⁡(x-\frac{\pi }{6})\,\text{d}x=$
{{field-1}}

If we let $u=x-\frac{\pi }{6},$ then

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}x=\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\pi /3$ | $2\pi /3$ |
| --- | --- | --- |
| $u$ | $\pi /6$ | $\pi /2$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{\pi /3}^{2\pi /3}4\operatorname{csc}⁡(x-\frac{\pi }{6})\operatorname{cot}⁡(x-\frac{\pi }{6})\,\text{d}x & ={\int }_{\pi /6}^{\pi /2}4\operatorname{csc}⁡(u)\operatorname{cot}⁡(u)\,\text{d}u \\  & =4{\int }_{\pi /6}^{\pi /2}\operatorname{csc}⁡(u)\operatorname{cot}⁡(u)\,\text{d}u \\  & =-4\operatorname{csc}⁡(u){|}_{\pi /6}^{\pi /2} \\  & =-4(\operatorname{csc}⁡(\frac{\pi }{2})-\operatorname{csc}⁡(\frac{\pi }{6})) \\  & =-4(1-2) \\  & =4\end{aligned}
$$

$4$

### Observed source parameters

Evaluate the following integral. Do not round the answer.

$\int_{\frac{\pi}{3}}^{\frac{2 \pi}{3}} 4\csc(x - \frac{\pi}{6})\cot(x - \frac{\pi}{6})\,\text{d}x=$
{{field-1}}

2f18acb1-ff13-56a7-9663-944668cdbeff $4$

If we let $u=x - \frac{\pi}{6},$ then

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}x=\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $\frac{\pi}{3}$ | $\frac{2 \pi}{3}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{6}$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{\frac{\pi}{3}}^{\frac{2 \pi}{3}} 4\csc(x - \frac{\pi}{6})\cot(x - \frac{\pi}{6})\,\text{d}x & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} 4\csc(u)\cot(u)\,\text{d}u \\ & =4\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \csc(u)\cot(u)\,\text{d}u \\ & =-4\csc(u)\big|_{\frac{\pi}{6}}^{\frac{\pi}{2}} \\ & =-4(\csc(\frac{\pi}{2})-\csc(\frac{\pi}{6})) \\ & =-4(1-2) \\ & =4\end{aligned}
$$

### Served changed-parameter variant seed321

Evaluate the following integral. Give an exact answer.

$\int_{- \frac{\pi}{12}}^{\frac{\pi}{4}} 2\csc(x + \frac{\pi}{4})\cot(x + \frac{\pi}{4})\,\text{d}x=$
{{field-1}}

f4272c3d-70d4-5b30-b9b5-9d2f0cbb7a67 $2$

If we let $u=x + \frac{\pi}{4},$ then

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}x=\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $- \frac{\pi}{12}$ | $\frac{\pi}{4}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{6}$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{- \frac{\pi}{12}}^{\frac{\pi}{4}} 2\csc(x + \frac{\pi}{4})\cot(x + \frac{\pi}{4})\,\text{d}x & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} 2\csc(u)\cot(u)\,\text{d}u \\ & =2\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \csc(u)\cot(u)\,\text{d}u \\ & =-2\csc(u)\big|_{\frac{\pi}{6}}^{\frac{\pi}{2}} \\ & =-2(\csc(\frac{\pi}{2})-\csc(\frac{\pi}{6})) \\ & =-2(1-2) \\ & =2\end{aligned}
$$

Parameters: `{"a": "1", "b": "1/4", "c": 2, "hi": "1/2", "lo": "1/6"}`.

### Served changed-parameter variant seed654

Evaluate the following integral. Give an exact answer.

$\int_{0}^{\frac{\pi}{12}} \csc(4 x + \frac{\pi}{6})\cot(4 x + \frac{\pi}{6})\,\text{d}x=$
{{field-1}}

d21db28b-b180-5b38-a5e3-a65fcdaf5a42 $\frac{1}{4}$

If we let $u=4 x + \frac{\pi}{6},$ then

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\text{d}x=\frac{1}{4}\text{d}u.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\frac{\pi}{12}$ |
| --- | --- | --- |
| $u$ | $\frac{\pi}{6}$ | $\frac{\pi}{2}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\pi}{12}} \csc(4 x + \frac{\pi}{6})\cot(4 x + \frac{\pi}{6})\,\text{d}x & =\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \csc(u)\cot(u)\cdot \frac{1}{4}\,\text{d}u \\ & =\frac{1}{4}\int_{\frac{\pi}{6}}^{\frac{\pi}{2}} \csc(u)\cot(u)\,\text{d}u \\ & =- \frac{1}{4}\csc(u)\big|_{\frac{\pi}{6}}^{\frac{\pi}{2}} \\ & =- \frac{1}{4}(\csc(\frac{\pi}{2})-\csc(\frac{\pi}{6})) \\ & =- \frac{1}{4}(1-2) \\ & =\frac{1}{4}\end{aligned}
$$

Parameters: `{"a": "4", "b": "1/6", "c": 1, "hi": "1/2", "lo": "1/6"}`.

## q-10578

### Original

${\int }_{0}^{\pi /2}\operatorname{sec}⁡(x-\frac{\pi }{3})\operatorname{tan}⁡(x-\frac{\pi }{3})\,\text{d}x=$

If we let $u=x-\frac{\pi }{3},$ then

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}x=\text{d}u.
$$

Calculating the limits for $u$ gives 

| $x$ | $0$ | $\pi /2$ |
| --- | --- | --- |
| $u$ | $-\pi /3$ | $\pi /6$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\pi /2}\operatorname{sec}⁡(x-\frac{\pi }{3})\operatorname{tan}⁡(x-\frac{\pi }{3})\,\text{d}x & ={\int }_{-\pi /3}^{\pi /6}\operatorname{sec}⁡u\operatorname{tan}⁡u\,\text{d}u \\  & =\operatorname{sec}⁡u{|}_{-\pi /3}^{\pi /6} \\  & =\operatorname{sec}⁡(\frac{\pi }{6})-\operatorname{sec}⁡(-\frac{\pi }{3}) \\  & =\frac{2\sqrt{3}}{3}-2\end{aligned}
$$

$\frac{2\sqrt{3}}{3}-2$
$-\frac{2\sqrt{3}}{3}-1$
$\sqrt{3}-1$
$-2\sqrt{3}+1$
$\frac{\sqrt{3}}{3}+2$

### Observed source parameters

$\int_{0}^{\frac{\pi}{2}} \sec(x - \frac{\pi}{3})\tan(x - \frac{\pi}{3})\,\text{d}x=$

61c8035d-2772-51a0-8a47-b3b09e8fc6c1 $-1 + \sqrt{3}$
6c55e0e8-3fae-5dfd-955c-89b40975e1be $- \frac{2 \sqrt{3}}{3} - 1$
4c23f3fc-69c9-5770-b07d-cebca4f9f10f $-2 + \frac{2 \sqrt{3}}{3}$
9f021037-03da-52fc-979b-2a028814fe69 $\frac{\sqrt{3}}{3} + 2$
1000b408-8d4b-59c6-81da-2aad38cd587c $1 - 2 \sqrt{3}$

If we let $u=x - \frac{\pi}{3},$ then

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}x=\text{d}u.
$$

Calculating the limits for $u$ gives 

| $x$ | $0$ | $\frac{\pi}{2}$ |
| --- | --- | --- |
| $u$ | $- \frac{\pi}{3}$ | $\frac{\pi}{6}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{0}^{\frac{\pi}{2}} \sec(x - \frac{\pi}{3})\tan(x - \frac{\pi}{3})\,\text{d}x & =\int_{- \frac{\pi}{3}}^{\frac{\pi}{6}} \sec(u)\tan(u)\,\text{d}u \\ & =\sec(u)\big|_{- \frac{\pi}{3}}^{\frac{\pi}{6}} \\ & =(\sec(\frac{\pi}{6})-(\sec(- \frac{\pi}{3}))) \\ & =-2 + \frac{2 \sqrt{3}}{3}\end{aligned}
$$

### Served changed-parameter variant seed321

$\int_{- \frac{7 \pi}{12}}^{- \frac{\pi}{12}} 2\sec(x + \frac{\pi}{4})\tan(x + \frac{\pi}{4})\,\text{d}x=$

2a8d4d16-4bbf-5fe7-a63d-1589e0e584ee $4 - \frac{4 \sqrt{3}}{3}$
c03ec013-e404-5e95-acb4-adf9fe75c267 $\frac{4 \sqrt{3}}{3}$
c1f93e47-0c1d-5175-8d25-00e3f624fa2f $-4 + \frac{4 \sqrt{3}}{3}$
0d85a706-7897-5f2e-94ef-5ba0784bf317 $\frac{4 \sqrt{3}}{3} + 4$
651aba89-a9de-5f7f-b099-abf95a5a11de $\frac{8 \sqrt{3}}{3}$

If we let $u=x + \frac{\pi}{4},$ then

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}x=\text{d}u.
$$

Calculating the limits for $u$ gives 

| $x$ | $- \frac{7 \pi}{12}$ | $- \frac{\pi}{12}$ |
| --- | --- | --- |
| $u$ | $- \frac{\pi}{3}$ | $\frac{\pi}{6}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{- \frac{7 \pi}{12}}^{- \frac{\pi}{12}} 2\sec(x + \frac{\pi}{4})\tan(x + \frac{\pi}{4})\,\text{d}x & =2\int_{- \frac{\pi}{3}}^{\frac{\pi}{6}} \sec(u)\tan(u)\,\text{d}u \\ & =2\sec(u)\big|_{- \frac{\pi}{3}}^{\frac{\pi}{6}} \\ & =2(\sec(\frac{\pi}{6})-(\sec(- \frac{\pi}{3}))) \\ & =-4 + \frac{4 \sqrt{3}}{3}\end{aligned}
$$

Parameters: `{"a": "1", "b": "1/4", "c": 2, "hi": "1/6", "lo": "-1/3"}`.

### Served changed-parameter variant seed654

$\int_{- \frac{\pi}{8}}^{0} \sec(4 x + \frac{\pi}{6})\tan(4 x + \frac{\pi}{6})\,\text{d}x=$

227a4074-18df-5901-959f-6de8829d24f9 $\frac{\sqrt{3}}{6}$
86612fa1-1bb4-5df0-ab29-f7a62c311d1c $\frac{\sqrt{3}}{6} + \frac{1}{2}$
091a9c18-8747-5328-b1c2-032dc582d4a2 $\frac{\sqrt{3}}{3}$
2bf96284-5032-59db-8378-3e2c35f12978 $\frac{1}{2} - \frac{\sqrt{3}}{6}$
7f578aa9-ce07-5190-8a8b-bf07eb3dcd31 $- \frac{1}{2} + \frac{\sqrt{3}}{6}$

If we let $u=4 x + \frac{\pi}{6},$ then

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\text{d}x=\frac{1}{4}\text{d}u.
$$

Calculating the limits for $u$ gives 

| $x$ | $- \frac{\pi}{8}$ | $0$ |
| --- | --- | --- |
| $u$ | $- \frac{\pi}{3}$ | $\frac{\pi}{6}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{- \frac{\pi}{8}}^{0} \sec(4 x + \frac{\pi}{6})\tan(4 x + \frac{\pi}{6})\,\text{d}x & =\frac{1}{4}\int_{- \frac{\pi}{3}}^{\frac{\pi}{6}} \sec(u)\tan(u)\,\text{d}u \\ & =\frac{1}{4}\sec(u)\big|_{- \frac{\pi}{3}}^{\frac{\pi}{6}} \\ & =\frac{1}{4}(\sec(\frac{\pi}{6})-(\sec(- \frac{\pi}{3}))) \\ & =- \frac{1}{2} + \frac{\sqrt{3}}{6}\end{aligned}
$$

Parameters: `{"a": "4", "b": "1/6", "c": 1, "hi": "1/6", "lo": "-1/3"}`.

## q-10578 observed-bank changed parameters seed321

$\int_{- \frac{7 \pi}{12}}^{- \frac{\pi}{12}} 2\sec(x + \frac{\pi}{4})\tan(x + \frac{\pi}{4})\,\text{d}x=$

86bb1332-14ae-5795-a517-32687c951d4a $- \frac{4 \sqrt{3}}{3} - 2$
9afd0848-e63b-5ef4-8f2f-a7095bd7704e $2 - 4 \sqrt{3}$
5324657a-0e79-587d-9be4-e040fd901cd7 $-4 + \frac{4 \sqrt{3}}{3}$
7423aac8-3e89-52da-b773-0bd6b5618a45 $-2 + 2 \sqrt{3}$
7e136765-9f2d-5540-a7e0-0a1b079692a4 $\frac{2 \sqrt{3}}{3} + 4$

If we let $u=x + \frac{\pi}{4},$ then

$$
\frac{\text{d}u}{\text{d}x}=1\,⟹\,\text{d}x=\text{d}u.
$$

Calculating the limits for $u$ gives 

| $x$ | $- \frac{7 \pi}{12}$ | $- \frac{\pi}{12}$ |
| --- | --- | --- |
| $u$ | $- \frac{\pi}{3}$ | $\frac{\pi}{6}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{- \frac{7 \pi}{12}}^{- \frac{\pi}{12}} 2\sec(x + \frac{\pi}{4})\tan(x + \frac{\pi}{4})\,\text{d}x & =2\int_{- \frac{\pi}{3}}^{\frac{\pi}{6}} \sec(u)\tan(u)\,\text{d}u \\ & =2\sec(u)\big|_{- \frac{\pi}{3}}^{\frac{\pi}{6}} \\ & =2(\sec(\frac{\pi}{6})-(\sec(- \frac{\pi}{3}))) \\ & =-4 + \frac{4 \sqrt{3}}{3}\end{aligned}
$$

## q-10578 observed-bank changed parameters seed654

$\int_{- \frac{\pi}{8}}^{0} \sec(4 x + \frac{\pi}{6})\tan(4 x + \frac{\pi}{6})\,\text{d}x=$

5edcd277-4e9f-5fe6-8dac-f4af7440dbbb $\frac{1}{4} - \frac{\sqrt{3}}{2}$
aafc8cbe-197d-5eaa-a4fa-ac37ede45330 $- \frac{1}{4} + \frac{\sqrt{3}}{4}$
53f3d578-0d9d-5927-a759-8cd070a25ec4 $\frac{\sqrt{3}}{12} + \frac{1}{2}$
d5ec7545-2f9c-59c2-a5eb-160a21ddad4c $- \frac{\sqrt{3}}{6} - \frac{1}{4}$
a52db1c4-d47e-5f24-9c71-fd7ba974526f $- \frac{1}{2} + \frac{\sqrt{3}}{6}$

If we let $u=4 x + \frac{\pi}{6},$ then

$$
\frac{\text{d}u}{\text{d}x}=4\,⟹\,\text{d}x=\frac{1}{4}\text{d}u.
$$

Calculating the limits for $u$ gives 

| $x$ | $- \frac{\pi}{8}$ | $0$ |
| --- | --- | --- |
| $u$ | $- \frac{\pi}{3}$ | $\frac{\pi}{6}$ |

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int_{- \frac{\pi}{8}}^{0} \sec(4 x + \frac{\pi}{6})\tan(4 x + \frac{\pi}{6})\,\text{d}x & =\frac{1}{4}\int_{- \frac{\pi}{3}}^{\frac{\pi}{6}} \sec(u)\tan(u)\,\text{d}u \\ & =\frac{1}{4}\sec(u)\big|_{- \frac{\pi}{3}}^{\frac{\pi}{6}} \\ & =\frac{1}{4}(\sec(\frac{\pi}{6})-(\sec(- \frac{\pi}{3}))) \\ & =- \frac{1}{2} + \frac{\sqrt{3}}{6}\end{aligned}
$$
