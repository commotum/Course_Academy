# Four-stage template extraction

Basis/provenance, level rationale, source anomalies and bank eligibility are in classification.md. All practice sources are mapped here. source-cases.json replays each through the public generate API.

## Stage 1 — specific original descriptions

### sqrt_product — q-36918 / 4903eb08-1095-52c0-bd3a-a8d7c39455f8

Square root of xyz, symbolic gradient. Outer reciprocal-square-root factor and three inner product derivatives; then rationalized coordinate denominators and common factor.

Original prompt: Given $f(x,y,z)=\sqrt{xyz}$, find $∇f(x,y,z).$

Observed field: selection / radio / 5 mathematical vector choices; correct value: $\frac{\sqrt{xyz}}{2}(\frac{1}{x}\text{ }i+\frac{1}{y}\text{ }j+\frac{1}{z}\text{ }k)$.

### root_log — q-36968 / e287a6b3-141e-5735-ae69-360760a9ed55

Square root of x+2 plus ln(sqrt(yz)), symbolic gradient. Explicit +0 and 0+ chain contributions retained; two nested log/root derivatives.

Original prompt: Find $∇g(x,y,z)$ given that  $g(x,y,z)=\sqrt{x+2}+\operatorname{ln}⁡(\sqrt{yz}).$

Observed field: selection / radio / 5 mathematical vector choices; correct value: $\frac{1}{2\sqrt{x+2}}i+\frac{1}{2y}\text{ }j+\frac{1}{2z}\text{ }k$.

### log_point — q-36969 / 5313963c-57a3-55b2-bdc3-c997dcee0402

ln(sqrt(xyz)) at (2,3,1). Three log/root/product chain rows, simplified coordinate reciprocal derivatives, denominator substitutions, numeric fractions.

Original prompt: Evaluate $∇f(x,y,z)$ at the point $(2,3,1)$ if $f(x,y,z)=\operatorname{ln}⁡(\sqrt{xyz}).$

Observed field: selection / radio / 5 mathematical vector choices; correct value: $\frac{1}{4}\text{ }i+\frac{1}{6}\text{ }j+\frac{1}{2}\text{ }k$.

### product_log — q-71422 / c4f224f8-09b2-598d-bc90-7a090ce4820d

xy ln(z), symbolic gradient. Two held-z log constants and one reciprocal derivative; xy·1/z stage retained.

Original prompt: Given $h(x,y,z)=xy\operatorname{ln}⁡(z)$, find $∇h(x,y,z).$

Observed field: selection / radio / 5 mathematical vector choices; correct value: $y\operatorname{ln}⁡(z)\text{ }i+x\operatorname{ln}⁡(z)\text{ }j+\frac{xy}{z}\text{ }k$.

### power_exp — q-71425 / 2d8f2390-7ede-5da9-be05-731bb79d1f06

x²y²z²+e^(xyz), symbolic gradient. Held-coordinate power rule plus exponential inner-product chain term in every coordinate.

Original prompt: Find $∇g(x,y,z)$ given that  $g(x,y,z)={x}^{2}{y}^{2}{z}^{2}+{e}^{xyz}.$

Observed field: selection / radio / 5 mathematical vector choices; correct value: $(2x{y}^{2}{z}^{2}+yz{e}^{xyz})\text{ }i+(2{x}^{2}y{z}^{2}+xz{e}^{xyz})\text{ }j+(2{x}^{2}{y}^{2}z+xy{e}^{xyz})\text{ }k$.

### variable_power — q-127945 / cf052c6a-faee-5b8c-b178-4c397426507c

x^y+y^z, symbolic gradient. x derivative holds exponent y; y derivative includes exponential-base log and power derivative of y^z; z derivative holds base y.

Original prompt: If $f(x,y,z)={x}^{y}+{y}^{z},$ find $∇f(x,y,z).$

Observed field: selection / radio / 5 mathematical vector choices; correct value: $y{x}^{y-1}\,i+({x}^{y}\operatorname{ln}⁡x+z{y}^{z-1})j+{y}^{z}\operatorname{ln}⁡y\,k$.

### expcos_point — q-127947 / 804d417e-4fe8-53d3-ae3f-56da60f7d4fb

e^(xy)cos(yz) at (1/2,1,π). x chain; y product+both chains, factored reduction; z trig chain; vector common factor; explicit substitution, trig values including zero, final two-component factor.

Original prompt: Evaluate $∇h(x,y,z)$ at the point $(\frac{1}{2},1,\pi )$ if $h(x,y,z)={e}^{xy}\operatorname{cos}⁡(yz).$

Observed field: selection / radio / 5 mathematical vector choices; correct value: $-\sqrt{e}(i+\frac{1}{2}\,j)$.

### exp_sin — q-35989 / 7f2c8781-0baa-5cdd-8cbc-03cc6b1166f3

e^(2xz)sin(y²−1), symbolic gradient. x/z exponential chains, y trig-power chain; factored vector.

Original prompt: Given  $g(x,y,z)={e}^{2xz}\operatorname{sin}⁡({y}^{2}-1)$, find $∇g(x,y,z).$

Observed field: selection / radio / 5 mathematical vector choices; correct value: $2{e}^{2xz}\text{ }(z\operatorname{sin}⁡({y}^{2}-1)i+y\operatorname{cos}⁡({y}^{2}-1)\text{ }j+x\operatorname{sin}⁡({y}^{2}-1)\text{ }k)$.

### composite_log — q-36012 / bcc7ffb5-272b-56a1-a959-51ef6109597c

xyz ln(xyz), symbolic gradient. Product plus log-chain quotients in every coordinate; cancellation to log+1 and common-vector factor.

Original prompt: Given $h(x,y,z)=xyz\operatorname{ln}⁡(xyz)$, find  $∇h(x,y,z).$

Observed field: selection / radio / 5 mathematical vector choices; correct value: $(\operatorname{ln}⁡(xyz)+1)(yz\text{ }i+xz\text{ }j+xy\text{ }k)$.

### sine_point — q-71426 / aef7acb8-89a1-5016-aa4c-ee6f59af7efc

sin(xyz) at (1,−1,π). Three product inner chains, signed coordinate substitution and cos(−π), individually evaluated signed products, final vector.

Original prompt: Evaluate $∇h(x,y,z)$ at the point $(1,-1,\pi )$ if $h(x,y,z)=\operatorname{sin}⁡(xyz).$

Observed field: selection / radio / 5 mathematical vector choices; correct value: $\pi \text{ }i-\pi \text{ }j+\text{ }k$.

## Stage 2 — shared patterns

The common assessed move is hold two independent coordinates constant, compute the first partial with respect to the remaining coordinate, and assemble these three ordered coefficients against i,j,k. Families remain separate because their mathematical rules and reduction/evaluation chains differ. A correct response is the exact gradient, not merely a parallel vector.

## Stage 3 — components and complete original banks

Each choice below is a complete vector, not independently compared scalar sides. The expression itself is the recovered parameterized operation pattern: symbolic families substitute complete translated-argument atoms; point families derive all entries from (a,b,c). An unclear historical error is explicitly evidence only, never an inferred default operation.

### sqrt_product

Historical profile observed_raw: evidence only; opaque/partly opaque intent.

| Choice UUID | Full source vector | Recovered pattern / interpretation |

|---|---|---|

| 35a99596-2194-56d8-b34a-8cf33e24d509 | $\sqrt{xyz}(x\text{ }i+y\text{ }j+z\text{ }k)$ | direct coordinates instead of inverse; omitted outer 1/2 |

| 6fa3bf93-c16d-5b28-921e-41079fe50f98 | $\frac{xyz}{2}(\frac{1}{x}\text{ }i+\frac{1}{y}\text{ }j+\frac{1}{z}\text{ }k)$ | radicand instead of root, inverse coordinates |

| bdfd3cdb-b6de-5b57-8bc2-55f6cfdc0358 | $\frac{\sqrt{xyz}}{2}(\frac{1}{x}\text{ }i+\frac{1}{y}\text{ }j+\frac{1}{z}\text{ }k)$ | correct root derivative |

| ce59c82e-5d51-5485-be48-7fb4d8c385b9 | $\frac{\sqrt{xyz}}{2}(x\text{ }i+y\text{ }j+z\text{ }k)$ | direct coordinates instead of inverse |

| def79f1e-967d-536d-901e-8b6506e4e5d0 | $\sqrt{xyz}(\frac{1}{yz}\text{ }i+\frac{1}{xz}\text{ }j+\frac{1}{xz}\text{ }k)$ | asymmetric pair-product denominators: interpretation unresolved |

Original fixed worked solution (all prose and stages):

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}(\sqrt{xyz}) \\  & =\frac{1}{2\sqrt{xyz}}\cdot (yz) \\  & =\frac{\sqrt{xyz}}{2x} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}(\sqrt{xyz}) \\  & =\frac{1}{2\sqrt{xyz}}\cdot (xz) \\  & =\frac{\sqrt{xyz}}{2y} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}(\sqrt{xyz}) \\  & =\frac{1}{2\sqrt{xyz}}\cdot (xy) \\  & =\frac{\sqrt{xyz}}{2z}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\text{ }i+{f}_{y}(x,y,z)\text{ }j+{f}_{z}(x,y,z)\text{ }k \\  & =\frac{\sqrt{xyz}}{2x}\text{ }i+\frac{\sqrt{xyz}}{2y}\text{ }j+\frac{\sqrt{xyz}}{2z}\text{ }k \\  & =\frac{\sqrt{xyz}}{2}(\frac{1}{x}\text{ }i+\frac{1}{y}\text{ }j+\frac{1}{z}\text{ }k)\end{aligned}
$$

### root_log

Historical profile observed_raw: defensible observed expression operations; identical bank is eligible observed_method.

| Choice UUID | Full source vector | Recovered pattern / interpretation |

|---|---|---|

| 05e393b4-8a81-5128-9ba6-326770dd3c30 | $\frac{1}{2\sqrt{x+2}}i+\frac{1}{2y}\text{ }j+\frac{1}{2z}\text{ }k$ | correct nested root/log partials |

| 46cf9748-7a8c-51e8-a98f-bf480e7d4abd | $\frac{1}{\sqrt{x+2}}i+\frac{1}{yz}\text{ }j+\frac{1}{yz}\text{ }k$ | omit root factor in x; differentiate yz as the same reciprocal product twice |

| 5277d147-5423-52ea-9448-c91d7f890aac | $\frac{1}{2\sqrt{x+2}}i+\frac{1}{2\sqrt{y}}\text{ }j+\frac{1}{2\sqrt{z}}\text{ }k$ | treat ln(sqrt(yz)) as sqrt(y)+sqrt(z) |

| 76d89040-9cda-5314-8747-132b54e35625 | $\frac{1}{2\sqrt{x+2}}i+\frac{1}{2yz}\text{ }j+\frac{1}{2yz}\text{ }k$ | omit inner-coordinate chain in both y/z |

| fa45680f-55c0-5cbc-847f-d3b13a4ac29e | $\frac{1}{\sqrt{x+2}}i+\frac{1}{y}\text{ }j+\frac{1}{z}\text{ }k$ | omit all 1/2 root factors |

Original fixed worked solution (all prose and stages):

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}(\sqrt{x+2}+\operatorname{ln}⁡(\sqrt{yz})) \\  & =\frac{1}{2\sqrt{x+2}}+0 \\  & =\frac{1}{2\sqrt{x+2}} \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}(\sqrt{x+2}+\operatorname{ln}⁡(\sqrt{yz})) \\  & =0+\frac{1}{\sqrt{yz}}\cdot \frac{1}{2\sqrt{yz}}\cdot z \\  & =\frac{1}{2y} \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}(\sqrt{x+2}+\operatorname{ln}⁡(\sqrt{yz})) \\  & =0+\frac{1}{\sqrt{yz}}\cdot \frac{1}{2\sqrt{yz}}\cdot y \\  & =\frac{1}{2z}\end{aligned}
$$

Hence,  the gradient is:

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =\frac{1}{2\sqrt{x+2}}i+\frac{1}{2y}\text{ }j+\frac{1}{2z}\text{ }k\end{aligned}
$$

### log_point

Historical profile observed_raw: evidence only; opaque/partly opaque intent.

| Choice UUID | Full source vector | Recovered pattern / interpretation |

|---|---|---|

| 0404f2a9-3d08-5a53-a026-f44a816bf37f | $\frac{1}{2}\text{ }i+\frac{1}{3}\text{ }j+k$ | omit square-root 1/2 factor |

| 13134d6f-499b-591c-bde5-f5b16ff56598 | $\frac{1}{2}\text{ }i+\frac{\sqrt{6}}{6}\text{ }j-\frac{\sqrt{2}}{2}\text{ }k$ | opaque radical vector expression pattern |

| 39e1fd9f-c905-53ce-88ed-48a994829d3c | $\frac{1}{4}\text{ }i+\frac{1}{6}\text{ }j+\frac{1}{2}\text{ }k$ | correct reciprocal chain result |

| 457eb332-a887-58f4-9e71-5175afe5b10a | $4\text{ }i+6\text{ }j-2\text{ }k$ | opaque signed twice-coordinate pattern |

| 6f462375-be9f-527c-9fe5-1e84d47ed3f9 | $\frac{1}{2}\text{ }i+\frac{1}{3}\text{ }j-k$ | omit square-root factor and negate final coordinate |

Original fixed worked solution (all prose and stages):

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot yz \\  & =\frac{1}{2x} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot xz \\  & =\frac{1}{2y} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}(\operatorname{ln}⁡(\sqrt{xyz})) \\  & =\frac{1}{\sqrt{xyz}}\cdot \frac{1}{2\sqrt{xyz}}\cdot xy \\  & =\frac{1}{2z}\end{aligned}
$$

 

Therefore, the gradient is

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\text{ }i+{f}_{x}(x,y,z)\text{ }j+{f}_{x}(x,y,z)\text{ }k \\  & =\frac{1}{2x}\text{ }i+\frac{1}{2y}\text{ }j+\frac{1}{2z}\text{ }k \\ ∇f(2,3,1) & =\frac{1}{2\cdot 2}\text{ }i+\frac{1}{2\cdot 3}\text{ }j+\frac{1}{2\cdot 1}\text{ }k \\  & =\frac{1}{4}\text{ }i+\frac{1}{6}\text{ }j+\frac{1}{2}\text{ }k.\end{aligned}
$$

### product_log

Historical profile observed_raw: evidence only; opaque/partly opaque intent.

| Choice UUID | Full source vector | Recovered pattern / interpretation |

|---|---|---|

| 0c165a4b-7842-5080-b22d-dd998f4efc33 | $y\operatorname{ln}⁡(yz+zx)\text{ }i+y\operatorname{ln}⁡(yz+zx)\text{ }j+\frac{xy}{z}\text{ }k$ | opaque changed logarithm argument and repeated coefficient |

| 546a4641-9ee2-54b1-9a19-949510d27139 | $x\operatorname{ln}⁡(z)\text{ }i+y\operatorname{ln}⁡(z)\text{ }j+xy\operatorname{ln}⁡(z)\text{ }k$ | differentiate each coordinate with the other role and retain original function for z |

| c3ad8a94-3343-5d3e-a1c5-41b03ebbd768 | $y\operatorname{ln}⁡(z)\text{ }i+xy\text{ }j+\frac{xy}{z}\text{ }k$ | omit y differentiation, replace by xy |

| d4f50290-6f7b-5795-9900-ef50d3f55007 | $xy\operatorname{ln}⁡(z)\text{ }i+xy\operatorname{ln}⁡(z)\text{ }j+\frac{xy}{z}\text{ }k$ | omit x/y differentiation, retain whole function |

| efe0a9c2-3996-5cde-90b0-22cd1b0fb18a | $y\operatorname{ln}⁡(z)\text{ }i+x\operatorname{ln}⁡(z)\text{ }j+\frac{xy}{z}\text{ }k$ | correct product/log partials |

Original fixed worked solution (all prose and stages):

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}(xy\operatorname{ln}⁡(z)) \\  & =y\operatorname{ln}⁡(z) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}(xy\operatorname{ln}⁡(z)) \\  & =x\operatorname{ln}⁡(z) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}(xy\operatorname{ln}⁡(z)) \\  & =xy\cdot \frac{1}{z} \\  & =\frac{xy}{z}\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{y}(x,y,z)\text{ }j+{h}_{z}(x,y,z)\text{ }k \\  & =y\operatorname{ln}⁡(z)\text{ }i+x\operatorname{ln}⁡(z)\text{ }j+\frac{xy}{z}\text{ }k\end{aligned}
$$

### power_exp

Historical profile observed_raw: defensible observed expression operations; identical bank is eligible observed_method.

| Choice UUID | Full source vector | Recovered pattern / interpretation |

|---|---|---|

| 2a21b9f7-4aaa-5471-bf82-f2d8ab4a05d3 | $(2x{y}^{2}{z}^{2}+{e}^{xyz})\text{ }i+(2{x}^{2}y{z}^{2}+{e}^{xyz})\text{ }j+(2{x}^{2}{y}^{2}z+{e}^{xyz})\text{ }k$ | omit exponential inner chain derivatives |

| 71cc0d72-27c7-5788-8341-714d4d503875 | $(2x+yz{e}^{xyz})\text{ }i+(2y+xz{e}^{xyz})\text{ }j+(2z+xy{e}^{xyz})\text{ }k$ | drop held-coordinate powers of polynomial |

| 78722099-cc9a-5084-9630-ca6c5d2d30e3 | $(2x{y}^{2}{z}^{2}+yz{e}^{xyz})\text{ }i+(2{x}^{2}y{z}^{2}+xz{e}^{xyz})\text{ }j+(2{x}^{2}{y}^{2}z+xy{e}^{xyz})\text{ }k$ | correct power+chain derivatives |

| 7a839402-601f-5953-874b-788c1ff02eff | $(x{y}^{2}{z}^{2}+yz{e}^{xyz-1})\text{ }i+({x}^{2}y{z}^{2}+xz{e}^{xyz-1})\text{ }j+({x}^{2}{y}^{2}z+xy{e}^{xyz-1})\text{ }k$ | drop polynomial power coefficient and lower exponential exponent as power rule |

| ac9d6b72-745e-56b9-86ea-4dab4db1e685 | $(2x{y}^{2}{z}^{2}+x{e}^{xyz})\text{ }i+(2{x}^{2}y{z}^{2}+y{e}^{xyz})\text{ }j+(2{x}^{2}{y}^{2}z+z{e}^{xyz})\text{ }k$ | use differentiated coordinate as exponential inner factor |

Original fixed worked solution (all prose and stages):

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}({x}^{2}{y}^{2}{z}^{2}+{e}^{xyz}) \\  & =2x{y}^{2}{z}^{2}+yz{e}^{xyz} \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}({x}^{2}{y}^{2}{z}^{2}+{e}^{xyz}) \\  & =2{x}^{2}y{z}^{2}+xz{e}^{xyz} \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}({x}^{2}{y}^{2}{z}^{2}+{e}^{xyz}) \\  & =2{x}^{2}{y}^{2}z+xy{e}^{xyz}\end{aligned}
$$

Hence,  the gradient is:

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =(2x{y}^{2}{z}^{2}+yz{e}^{xyz})\text{ }i+(2{x}^{2}y{z}^{2}+xz{e}^{xyz})\text{ }j+(2{x}^{2}{y}^{2}z+xy{e}^{xyz})\text{ }k\end{aligned}
$$

### variable_power

Historical profile observed_raw: defensible observed expression operations; identical bank is eligible observed_method.

| Choice UUID | Full source vector | Recovered pattern / interpretation |

|---|---|---|

| 514f6510-65a6-5c71-8eca-34568a35dcba | $y{x}^{y-1}\,i+({x}^{y}\operatorname{ln}⁡x+z{y}^{z-1})j+{y}^{z}\operatorname{ln}⁡y\,k$ | correct held-base/held-exponent rules |

| 6a1164dc-4f74-5f63-8956-517c46e081b5 | $y{x}^{y-1}\,i+z{y}^{z-1}\,j+{y}^{z}\operatorname{ln}⁡y\,k$ | omit x^y derivative in y |

| 37e9d54a-963a-50c9-af62-5869773b3bbc | ${x}^{y}\operatorname{ln}⁡y\,i+{x}^{y}\operatorname{ln}⁡x\,j+({x}^{y}\operatorname{ln}⁡x+z{y}^{z-1})k$ | mixed base/exponent roles and reassigned components |

| daceaefe-76b2-57db-9142-cb9036ed18b4 | $({x}^{y}\operatorname{ln}⁡x+z{y}^{z-1})i+{x}^{y}\operatorname{ln}⁡y\,j+{y}^{z}\operatorname{ln}⁡z\,k$ | mixed logs/base roles and reassigned components |

| b6a91458-30b5-5353-b216-4f46dc771583 | $y{x}^{y-1}\,i+z{y}^{z-1}\,j+z{y}^{z-1}\,k$ | omit exponent derivatives and repeat y power derivative in z |

Original fixed worked solution (all prose and stages):

First, we find the partial derivatives:

$$
\begin{aligned}{f}_{x}(x,y,z) & =\frac{∂}{∂x}({x}^{y}+{y}^{z}) \\  & =y{x}^{y-1} \\ {f}_{y}(x,y,z) & =\frac{∂}{∂y}({x}^{y}+{y}^{z}) \\  & ={x}^{y}\operatorname{ln}⁡x+z{y}^{z-1} \\ {f}_{z}(x,y,z) & =\frac{∂}{∂z}({x}^{y}+{y}^{z}) \\  & ={y}^{z}\operatorname{ln}⁡y\end{aligned}
$$

Hence, the gradient is

$$
\begin{aligned}∇f(x,y,z) & ={f}_{x}(x,y,z)\,i+{f}_{y}(x,y,z)\,j+{f}_{z}(x,y,z)\,k \\  & =y{x}^{y-1}\,i+({x}^{y}\operatorname{ln}⁡x+z{y}^{z-1})j+{y}^{z}\operatorname{ln}⁡y\,k.\end{aligned}
$$

### expcos_point

Historical profile observed_raw: evidence only; opaque/partly opaque intent.

| Choice UUID | Full source vector | Recovered pattern / interpretation |

|---|---|---|

| 6b8c5a90-83e7-5f9f-b520-1eaae67e52b7 | $e(i-\frac{1}{2}\,j)$ | opaque exponent twice xy with changed j sign |

| de50d21e-e598-5ea9-bc0f-adeed68ca073 | $e(i-\frac{1}{2}\,j+k)$ | same with added exponential k component |

| 86a0af6e-4435-566d-a878-c8e589b685c7 | $\sqrt{e}(-i+\pi \,j-k)$ | opaque replacement j by z and k by −1, preserving exp(xy) |

| 7f1d0ab5-cfea-5a4b-924a-7f3b508a6a85 | $-\sqrt{e}(i+\pi \,j-k)$ | opaque replacement j by z and k by −1 under common negative factor |

| ce237491-8288-54ff-835f-4ec66f6ccaa7 | $-\sqrt{e}(i+\frac{1}{2}\,j)$ | correct familiar-angle gradient |

Original fixed worked solution (all prose and stages):

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =y{e}^{xy}\operatorname{cos}⁡(yz) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =x{e}^{xy}\operatorname{cos}⁡(yz)+{e}^{xy}(-\operatorname{sin}⁡(yz))(z) \\  & ={e}^{xy}(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz)) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}({e}^{xy}\operatorname{cos}⁡(yz)) \\  & =-y{e}^{xy}\operatorname{sin}⁡(yz)\end{aligned}
$$

 

Therefore, the gradient is

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\,i+{h}_{x}(x,y,z)\,j+{h}_{x}(x,y,z)\,k \\  & =y{e}^{xy}\operatorname{cos}⁡(yz)\,i+{e}^{xy}(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz))\,j-y{e}^{xy}\operatorname{sin}⁡(yz)\,k \\  & ={e}^{xy}(y\operatorname{cos}⁡(yz)\,i+(x\operatorname{cos}⁡(yz)-z\operatorname{sin}⁡(yz))\,j-y\operatorname{sin}⁡(yz)\,k) \\ ∇h(\frac{1}{2},1,\pi ) & ={e}^{(1/2)(1)}(1\operatorname{cos}⁡(1\pi )\,i+(\frac{1}{2}\operatorname{cos}⁡(1\pi )-\pi \operatorname{sin}⁡(1\pi ))\,j-1\operatorname{sin}⁡(1\pi )\,k) \\  & =\sqrt{e}(-i-\frac{1}{2}\,j-0\,k) \\  & =-\sqrt{e}(i+\frac{1}{2}\,j).\end{aligned}
$$

### exp_sin

Historical profile observed_raw: defensible observed expression operations; identical bank is eligible observed_method.

| Choice UUID | Full source vector | Recovered pattern / interpretation |

|---|---|---|

| 94b23f6d-fcbc-5f05-bdfa-551e5a601813 | $2{e}^{2xz}\text{ }(z\operatorname{sin}⁡({y}^{2}-1)i+y\operatorname{cos}⁡({y}^{2}-1)\text{ }j+x\operatorname{sin}⁡({y}^{2}-1)\text{ }k)$ | correct three chains with common 2e factor |

| 5cb1b5c1-0c20-551c-a0c4-1c105471790f | $2{e}^{2xz}\text{ }(zi+y\operatorname{cos}⁡({y}^{2}-1)\text{ }j+x\text{ }k)$ | drop sine in x/z |

| 0886912b-e3e5-5d97-a4f7-8d67907aca83 | $z\operatorname{sin}⁡({y}^{2}-1)i+y\operatorname{cos}⁡({y}^{2}-1)\text{ }j+x\operatorname{sin}⁡({y}^{2}-1)\text{ }k$ | omit common exponential and factor 2 |

| d8f5b6bf-05e5-54bc-b294-aa5357db39ab | $2{e}^{2xz}\operatorname{sin}⁡({y}^{2}-1)\text{ }(zi+y\text{ }j+x\text{ }k)$ | use sine for y where cosine required |

| 24c26190-fbac-5847-9741-c5fdf4a37862 | $2{e}^{2xz}\text{ }(zi+y\text{ }j+x\text{ }k)$ | drop sine/cosine factors in all coordinates |

Original fixed worked solution (all prose and stages):

First, we find the partial derivatives:

$$
\begin{aligned}{g}_{x}(x,y,z) & =\frac{∂}{∂x}({e}^{2xz}\operatorname{sin}⁡({y}^{2}-1)) \\  & =2z{e}^{2xz}\operatorname{sin}⁡({y}^{2}-1) \\ {g}_{y}(x,y,z) & =\frac{∂}{∂y}({e}^{2xz}\operatorname{sin}⁡({y}^{2}-1)) \\  & =2y{e}^{2xz}\operatorname{cos}⁡({y}^{2}-1) \\ {g}_{z}(x,y,z) & =\frac{∂}{∂z}({e}^{2xz}\operatorname{sin}⁡({y}^{2}-1)) \\  & =2x{e}^{2xz}\operatorname{sin}⁡({y}^{2}-1).\end{aligned}
$$

Hence, the gradient is: 

$$
\begin{aligned}∇g(x,y,z) & ={g}_{x}(x,y,z)\text{ }i+{g}_{y}(x,y,z)\text{ }j+{g}_{z}(x,y,z)\text{ }k \\  & =2z{e}^{2xz}\operatorname{sin}⁡({y}^{2}-1)\text{ }i+2y{e}^{2xz}\operatorname{cos}⁡({y}^{2}-1)\text{ }j+2x{e}^{2xz}\operatorname{sin}⁡({y}^{2}-1)\text{ }k \\  & =2{e}^{2xz}\text{ }(z\operatorname{sin}⁡({y}^{2}-1)i+y\operatorname{cos}⁡({y}^{2}-1)\text{ }j+x\operatorname{sin}⁡({y}^{2}-1)\text{ }k)\end{aligned}
$$

### composite_log

Historical profile observed_raw: defensible observed expression operations; identical bank is eligible observed_method.

| Choice UUID | Full source vector | Recovered pattern / interpretation |

|---|---|---|

| 633422e1-8e43-5c9f-91f7-5f1b7bac7900 | $yz\text{ }i+xz\text{ }j+xy\text{ }k$ | omit product-derivative logarithm contribution |

| c843fcb2-eb1c-505e-b82f-631646ec1f8e | $(\operatorname{ln}⁡(xyz)+1)(yz\text{ }i+xz\text{ }j+xy\text{ }k)$ | correct product+log-chain result |

| 021bd062-132f-5e06-92b6-5a56c9d30357 | $(\operatorname{ln}⁡(xyz)+1)(x\text{ }i+y\text{ }j+z\text{ }k)$ | replace pair-product inner factors by individual coordinates |

| 3e3b7394-d1cf-599d-a5a4-871fc9682748 | $\operatorname{ln}⁡(xyz)(yz\text{ }i+xz\text{ }j+xy\text{ }k)$ | omit log-chain +1 |

| 8fef3c82-4839-5c58-8b07-a4fabcf9cc44 | $(\operatorname{ln}⁡(xyz)+1)(\text{ }i+\text{ }j+\text{ }k)$ | omit all inner product factors |

Original fixed worked solution (all prose and stages):

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}(xyz\operatorname{ln}⁡(xyz)) \\  & =yz\operatorname{ln}⁡(xyz)+xyz\frac{yz}{xyz} \\  & =yz(\operatorname{ln}⁡(xyz)+1) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}(xyz\operatorname{ln}⁡(xyz)) \\  & =xz\operatorname{ln}⁡(xyz)+xyz\frac{xz}{xyz} \\  & =xz(\operatorname{ln}⁡(xyz)+1) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}(xyz\operatorname{ln}⁡(xyz)) \\  & =xy\operatorname{ln}⁡(xyz)+xyz\frac{xy}{xyz} \\  & =xy(\operatorname{ln}⁡(xyz)+1)\end{aligned}
$$

Hence, the gradient is:

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{y}(x,y,z)\text{ }j+{h}_{z}(x,y,z)\text{ }k \\  & =yz(\operatorname{ln}⁡(xyz)+1)\text{ }i+xz(\operatorname{ln}⁡(xyz)+1)\text{ }j+xy(\operatorname{ln}⁡(xyz)+1)\text{ }k \\  & =(\operatorname{ln}⁡(xyz)+1)(yz\text{ }i+xz\text{ }j+xy\text{ }k).\end{aligned}
$$

### sine_point

Historical profile observed_raw: evidence only; opaque/partly opaque intent.

| Choice UUID | Full source vector | Recovered pattern / interpretation |

|---|---|---|

| 7ac0e82c-e65c-52b4-92cf-ea9eef5506dc | $\pi \text{ }i-\pi \text{ }j+\text{ }k$ | correct signed cosine chain |

| 725ac3d7-7213-5bdb-b47f-4954c2a469c7 | $\pi \text{ }i+\pi \text{ }j+\pi \text{ }k$ | opaque z copied into all components |

| 44d96ff8-6e7a-5e3c-bdfc-e4fa56a64251 | $\pi \text{ }i+\pi \text{ }j+\text{ }k$ | opaque z copied into first two and constant k |

| 5a3bbb8f-e6f1-5641-8261-340795b58dda | $\text{ }i-\pi \text{ }j+\text{ }k$ | opaque unit first coefficient and −z second |

| fa3e1f03-a9e4-5b31-b950-95579c95df2e | $-\pi \text{ }i+\pi \text{ }j+\text{ }k$ | opaque swapped signs of first two |

Original fixed worked solution (all prose and stages):

First, we find the partial derivatives:

$$
\begin{aligned}{h}_{x}(x,y,z) & =\frac{∂}{∂x}(\operatorname{sin}⁡(xyz)) \\  & =yz\operatorname{cos}⁡(xyz) \\ {h}_{y}(x,y,z) & =\frac{∂}{∂y}(\operatorname{sin}⁡(xyz)) \\  & =xz\operatorname{cos}⁡(xyz) \\ {h}_{z}(x,y,z) & =\frac{∂}{∂z}(\operatorname{sin}⁡(xyz)) \\  & =xy\operatorname{cos}⁡(xyz)\end{aligned}
$$

 
Hence, the gradient is

$$
\begin{aligned}∇h(x,y,z) & ={h}_{x}(x,y,z)\text{ }i+{h}_{x}(x,y,z)\text{ }j+{h}_{x}(x,y,z)\text{ }k \\  & =yz\operatorname{cos}⁡(xyz)\text{ }i+xz\operatorname{cos}⁡(xyz)\text{ }j+xy\operatorname{cos}⁡(xyz)\text{ }k \\ ∇h(1,-1,\pi ) & =(-1)(\pi )\operatorname{cos}⁡(-\pi )\text{ }i+(1)(\pi )\operatorname{cos}⁡(-\pi )\text{ }j+(1)(-1)\operatorname{cos}⁡(-\pi )\text{ }k \\  & =(-\pi )(-1)\text{ }i+\pi (-1)\text{ }j-(-1)\text{ }k \\  & =\pi \text{ }i-\pi \text{ }j+\text{ }k\end{aligned}
$$

## Stage 4 — reusable masks, constraints and calculation plan

Symbolic renderer slots only complete scalar mathematical components. It protects TeX command names, retains function argument tuples and held-coordinate operator denominators outside the argument slot, then replaces mathematical coordinate atoms by grouped (coordinate+shift) expressions. First formal derivative inputs, chain factors, reductions and factored complete choices use the same shifted object. The template-level prose and ordered rows come from each original source; rows are never merged into a generic CAS solution. No chain term is introduced or deleted. Explicit shift inputs must be three integers with absolute value ≤3. Open positive translated-argument domains support roots/logs/variable powers.

Point renderer keeps the formal derivatives and symbolic gradient rows, changes the full point tuple in prompt and evaluation labels, then renders source-specific substitution, trig/component evaluation and conclusion stages. log_point uses point coordinates 1…6; sine_point uses x,y in ±1,±2 and xyz/π in ±1,±2; expcos_point uses x in {1/3,1/2,1,2}, y in {1,2,3}, x≠y, yz/π in ±1,±2. Complete-bank collisions and invalid raw expression patterns reject the whole parameter instance. The raw opaque expcos bank is eligible as evidence only when its historical designated expression actually equals the requested gradient (odd cosine angles); otherwise explicit replay fails instead of silently changing the point.

Authored method banks for historical opaque families: sqrt_product uses omitted 1/2, omitted root chain, direct rather than reciprocal coordinate factors, and omitted x inner-chain; product_log retains whole function instead of x, y, or z differentiation and swapped x/y held-coordinate factors; log_point omits outer-root 1/2 and negates each individual component; sine_point negates each chain component and negates all; expcos_point omits exponential factor, doubles its exponent, reverses trig sign, and uses y instead of x in the middle component. Their five values are constructed together, not pooled. Correct full vectors are calculated first; all other required members must be finite, unequal and wrong before acceptance.

Easy and hard solutions contain full formal inputs, individual held-coordinate zero terms (easy), quotient numerator/denominator differentiation products (hard), vector assembly and hard point substitution with signed component arithmetic before reduction. Exact SymPy calculates values but unevaluated explicit arithmetic masks preserve the teaching operations.

Identity: UUIDs depend on actual prompt, fixed solution, level and whole bank; order/seed/profile aliases do not create new content IDs. Mathematical fingerprints omit choice banks, order, source IDs and template/profile aliases; canonical differentiation object and meaningful evaluation data establish the assessed task. All defaults choose eligible whole families/banks before parameter sampling; reject whole instances on collisions or workload degeneracy.

Raw fidelity and corrected learning output are reported separately. Raw replay preserves all original component-label mistakes; eligible generation corrects labels without changing mathematical stages. Native radio grading does not test equivalent typed vectors because these questions do not have blank fields. Independent parser checks every actual displayed scalar row, vector stage, formal operator input, point and choice. No unsupported or unrated field shapes were invented. No plots apply.

Independent operation structure results: all 54 source-shaped fixture chains preserve row ordering and per-row fractions, explicit products, roots, named functions, zero contributions and powers (point numeric notation is checked mathematically separately). The suite detects 96 equal-row deletion mutations and 22 zero/explicit-product omission mutations. Independent authored-bank readback matches all 90 values across 18 whole authored banks.
