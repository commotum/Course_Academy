# Template extraction

## Stage 1 — specific originals

Every original prompt, solution and complete field/bank is retained in source.json. The table below records parameters and number forms separately from the proposed finite sampling domains.

### q-94589 (hard)
Let $f(x,y,z)={x}^{2}+2xy-3{z}^{2},$ where $x=st,$ $y=s+3t,$ and $z=2s-t.$ Given that

$$
\frac{∂f}{∂t}=2({s}^{2}t+{s}^{2}+{c}_{1}st+{c}_{2}s+{c}_{3}t),
$$

find the value of ${c}_{1}+{c}_{2}+{c}_{3}.$

Original parameter values={'a': 1, 'b': 3}; outer f=x**2 + 2*x*y - 3*z**2; coordinate maps=[s*t, s + 3*t, 2*s - t]; held variable=t; formal partials=[2*x + 2*y, 2*x, -6*z]; coordinate derivatives=[s, 3, -1]; component products=[2*s**2*t + 2*s**2 + 6*s*t, 6*s*t, 12*s - 6*t]; requested result=9.
Source stages: [1, 3, 5, 3, 4, 2] RHS slots per formal/operator, partial, optional coordinate-substitution, map-derivative, chain/distribution/collection, optional coefficient-sum block. All prose, punctuation, row ordering and omitted redundant rows are preserved.

### q-94814 (moderate)
Let $f(x,y,z)=4x+3y-2z,$ where $x=2{s}^{2}-t,$ $y=s+3{t}^{2}$ and $z=4{s}^{2}+{t}^{2}.$ Calculate $\frac{∂f}{∂s}.$

Original parameter values={'a': 4, 'b': 2}; outer f=4*x + 3*y - 2*z; coordinate maps=[2*s**2 - t, s + 3*t**2, 4*s**2 + t**2]; held variable=s; formal partials=[4, 3, -2]; coordinate derivatives=[4*s, 1, 8*s]; component products=[16*s, 3, -16*s]; requested result=3.
Source stages: [1, 3, 3, 3] RHS slots per formal/operator, partial, optional coordinate-substitution, map-derivative, chain/distribution/collection, optional coefficient-sum block. All prose, punctuation, row ordering and omitted redundant rows are preserved.

### q-170675 (hard)
Let $f(x,y,z)=\frac{y+z}{x},$ where $x=s+t,$ $y={s}^{2}$ and $z={t}^{2}.$ Given that

$$
\frac{∂f}{∂t}=\frac{{c}_{1}{s}^{2}+{c}_{2}st+{c}_{3}{t}^{2}}{(s+t)^{2}},
$$

find the value of ${c}_{1}+{c}_{2}+{c}_{3}.$

Original parameter values={'a': 1, 'b': 1}; outer f=(y + z)/x; coordinate maps=[s + t, s**2, t**2]; held variable=t; formal partials=[-(y + z)/x**2, 1/x, 1/x]; coordinate derivatives=[1, 0, 2*t]; component products=[-s**2/(s**2 + 2*s*t + t**2) - t**2/(s**2 + 2*s*t + t**2), 0, 2*t/(s + t)]; requested result=2.
Source stages: [1, 3, 3, 3, 3, 2] RHS slots per formal/operator, partial, optional coordinate-substitution, map-derivative, chain/distribution/collection, optional coefficient-sum block. All prose, punctuation, row ordering and omitted redundant rows are preserved.

### q-37132 (hard)
Let $f(x,y,z)={x}^{2}y-5yz,$ where $x=st,$ $y={s}^{3}$ and $z=s\operatorname{sin}⁡t.$ Calculate $\frac{∂f}{∂s}.$

Original parameter values={'a': 3, 'b': 5}; outer f=x**2*y - 5*y*z; coordinate maps=[s*t, s**3, s*sin(t)]; held variable=s; formal partials=[2*x*y, x**2 - 5*z, -5*y]; coordinate derivatives=[t, 3*s**2, sin(t)]; component products=[2*s**4*t**2, 3*s**4*t**2 - 15*s**3*sin(t), -5*s**3*sin(t)]; requested result=5*s**3*(s*t**2 - 4*sin(t)).
Source stages: [1, 3, 5, 3, 3] RHS slots per formal/operator, partial, optional coordinate-substitution, map-derivative, chain/distribution/collection, optional coefficient-sum block. All prose, punctuation, row ordering and omitted redundant rows are preserved.

### q-94811 (moderate)
Let $f(x,y,z)=3x-2y+z,$ where $x=s+t,$ $y={s}^{2}-{t}^{2}$ and $z=s.$ Calculate $\frac{∂f}{∂t}.$

Original parameter values={'a': 3, 'b': 2}; outer f=3*x - 2*y + z; coordinate maps=[s + t, s**2 - t**2, s]; held variable=t; formal partials=[3, -2, 1]; coordinate derivatives=[1, -2*t, 0]; component products=[3, 4*t, 0]; requested result=4*t + 3.
Source stages: [1, 3, 3, 2] RHS slots per formal/operator, partial, optional coordinate-substitution, map-derivative, chain/distribution/collection, optional coefficient-sum block. All prose, punctuation, row ordering and omitted redundant rows are preserved.

### q-94812 (moderate)
Let $f(x,y,z)=xyz,$ where $x=2,$ $y=s{e}^{t}$ and $z=t{e}^{s}.$ Calculate $\frac{∂f}{∂t}.$

Original parameter values={'a': 2, 'b': 1, 'c': 1}; outer f=x*y*z; coordinate maps=[2, s*exp(t), t*exp(s)]; held variable=t; formal partials=[y*z, x*z, x*y]; coordinate derivatives=[0, s*exp(t), exp(s)]; component products=[0, 2*s*t*exp(s)*exp(t), 2*s*exp(s)*exp(t)]; requested result=2*s*(t + 1)*exp(s + t).
Source stages: [1, 3, 3, 3, 3] RHS slots per formal/operator, partial, optional coordinate-substitution, map-derivative, chain/distribution/collection, optional coefficient-sum block. All prose, punctuation, row ordering and omitted redundant rows are preserved.

### q-94813 (moderate)
Let $f(x,y,z)={e}^{x+y+z},$ where $x=s-t,$ $y={t}^{2}$ and $z=s+t.$ Calculate $\frac{∂f}{∂t}.$

Original parameter values={'a': 1, 'b': 1}; outer f=exp(x + y + z); coordinate maps=[s - t, t**2, s + t]; held variable=t; formal partials=[exp(x + y + z), exp(x + y + z), exp(x + y + z)]; coordinate derivatives=[-1, 2*t, 1]; component products=[-exp(2*s)*exp(t**2), 2*t*exp(2*s)*exp(t**2), exp(2*s)*exp(t**2)]; requested result=2*t*exp(2*s + t**2).
Source stages: [1, 3, 6, 3, 3] RHS slots per formal/operator, partial, optional coordinate-substitution, map-derivative, chain/distribution/collection, optional coefficient-sum block. All prose, punctuation, row ordering and omitted redundant rows are preserved.

### q-94815 (moderate)
Let $f(x,y,z)={x}^{2}+{y}^{2}+{z}^{2},$ where $x=t+2s,$ $y=3t-s$ and $z=st.$ Calculate $\frac{∂f}{∂s}.$

Original parameter values={'a': 2, 'b': 3}; outer f=x**2 + y**2 + z**2; coordinate maps=[2*s + t, -s + 3*t, s*t]; held variable=s; formal partials=[2*x, 2*y, 2*z]; coordinate derivatives=[2, -1, t]; component products=[8*s + 4*t, 2*s - 6*t, 2*s*t**2]; requested result=2*s*t**2 + 10*s - 2*t.
Source stages: [1, 3, 5, 3, 4] RHS slots per formal/operator, partial, optional coordinate-substitution, map-derivative, chain/distribution/collection, optional coefficient-sum block. All prose, punctuation, row ordering and omitted redundant rows are preserved.

### q-94816 (hard)
Let $f(x,y,z)=\operatorname{ln}⁡x-2{e}^{y}+4z,$ where $x=t{s}^{2},$ $y=\operatorname{ln}⁡({t}^{2}+{s}^{2})$ and $z={s}^{2}.$ Calculate $\frac{∂f}{∂s}.$

Original parameter values={'a': 2, 'b': 4}; outer f=4*z - 2*exp(y) + log(x); coordinate maps=[s**2*t, log(s**2 + t**2), s**2]; held variable=s; formal partials=[1/x, -2*exp(y), 4]; coordinate derivatives=[2*s*t, 2*s/(s**2 + t**2), 2*s]; component products=[2/s, -4*s**3/(s**2 + t**2) - 4*s*t**2/(s**2 + t**2), 8*s]; requested result=4*s + 2/s.
Source stages: [1, 3, 4, 3, 4] RHS slots per formal/operator, partial, optional coordinate-substitution, map-derivative, chain/distribution/collection, optional coefficient-sum block. All prose, punctuation, row ordering and omitted redundant rows are preserved.

### q-170674 (moderate)
Let $f(x,y,z)=z-x-y,$ where $x={e}^{s}+t,$ $y=s+1$ and $z=1-t-s.$ Calculate $\frac{∂f}{∂s}.$

Original parameter values={'a': 1, 'b': 1}; outer f=-x - y + z; coordinate maps=[t + exp(s), s + 1, -s - t + 1]; held variable=s; formal partials=[-1, -1, 1]; coordinate derivatives=[exp(s), 1, -1]; component products=[-exp(s), -1, -1]; requested result=-exp(s) - 2.
Source stages: [1, 3, 3, 2] RHS slots per formal/operator, partial, optional coordinate-substitution, map-derivative, chain/distribution/collection, optional coefficient-sum block. All prose, punctuation, row ordering and omitted redundant rows are preserved.

### q-37208 (hard)
Let $f(x,y,z)=\operatorname{cos}⁡x+{y}^{2}z,$ where $x=3t,$ $y=t-s$ and $z=2st.$ Given that

$$
\frac{∂f}{∂t}=-3\operatorname{sin}⁡3t+{c}_{1}s{t}^{2}+{c}_{2}{s}^{2}t+{c}_{3}{s}^{3},
$$

find the value of ${c}_{1}+{c}_{2}+{c}_{3}.$

Original parameter values={'a': 1, 'b': 2, 'c': 1}; outer f=y**2*z + cos(x); coordinate maps=[3*t, -s + t, 2*s*t]; held variable=t; formal partials=[-sin(x), 2*y*z, y**2]; coordinate derivatives=[3, 1, 2*s]; component products=[-3*sin(3*t), -4*s**2*t + 4*s*t**2, 2*s**3 - 4*s**2*t + 2*s*t**2]; requested result=0.
Source stages: [1, 3, 5, 3, 3, 2] RHS slots per formal/operator, partial, optional coordinate-substitution, map-derivative, chain/distribution/collection, optional coefficient-sum block. All prose, punctuation, row ordering and omitted redundant rows are preserved.

### q-37206 (hard)
Let $f(x,y,z)=xy+yz+{z}^{2},$ where $x={s}^{2}+{t}^{2},$ $y=\frac{s}{t}$ and $z=s{t}^{2}.$ Given that

$$
\frac{∂f}{∂s}=\frac{3{s}^{2}}{t}+{c}_{1}t+{c}_{2}st+{c}_{3}s{t}^{4},
$$

find the value of ${c}_{1}+{c}_{2}+{c}_{3}.$

Original parameter values={'a': 1, 'b': 1}; outer f=x*y + y*z + z**2; coordinate maps=[s**2 + t**2, s/t, s*t**2]; held variable=s; formal partials=[y, x + z, y + 2*z]; coordinate derivatives=[2*s, 1/t, t**2]; component products=[2*s**2/t, s**2/t + s*t + t, 2*s*t**4 + s*t]; requested result=5.
Source stages: [1, 3, 3, 3, 3, 2] RHS slots per formal/operator, partial, optional coordinate-substitution, map-derivative, chain/distribution/collection, optional coefficient-sum block. All prose, punctuation, row ordering and omitted redundant rows are preserved.

## Stage 2 — shared mathematical pattern

Hold the unrequested independent coordinate fixed. Differentiate the actual outer f separately with respect to x,y,z, substitute each coordinate map when those partials are nonconstant, differentiate x,y,z with respect to the requested coordinate, multiply each matching pair including zero paths, and sum/distribute/collect. Four hard families then match the resulting expression to supplied c1,c2,c3 slots and add the coefficients. Six moderate and six hard forms stay distinct; no generic collapsed solution replaces their source arithmetic chain.

## Stage 3 — every component and complete observed bank

Each option below is attached to its exact captured field. The explicit observed profile parameterizes its mathematical value as C+(V−C0), with V the retained original expression and C the new assessed result. These residual formulas reproduce every displayed mathematical object but do not recover historical intent; they are evidence-only, never sampled in learner defaults. Their expressions are parsed, not returned through answer lookups. Original a,b replay retains exact spelling. Complete source banks are kept together; no first-valid selection pools.

### q-94589 — observed profile
Field 0: key `selection`, `:answer-field.type/radio`; original correct attribute ABSENT.

| Original value | Explicit replay operation | Interpretation |
|---|---|---|
| `$3$` | C+(-6) | opaque residual evidence |
| `$6$` | C+(-3) | opaque residual evidence |
| `$-3$` | C+(-12) | opaque residual evidence |
| `$-6$` | C+(-15) | opaque residual evidence |
| `$9$` | C+(0) | opaque residual evidence |
Field 1: key `selection`, `:answer-field.type/radio`; original correct attribute present: 9.

| Original value | Explicit replay operation | Interpretation |
|---|---|---|
| `$9$` | C+(0) | opaque residual evidence |
| `$3$` | C+(-6) | opaque residual evidence |
| `$6$` | C+(-3) | opaque residual evidence |
| `$-3$` | C+(-12) | opaque residual evidence |
| `$-6$` | C+(-15) | opaque residual evidence |

### q-94814 — observed profile
Field 0: key `selection`, `:answer-field.type/radio`; original correct attribute present: 3.

| Original value | Explicit replay operation | Interpretation |
|---|---|---|
| `$3-8s$` | C+(- 8 s) | opaque residual evidence |
| `$t+4s-1$` | C+(-4 + t + 4 s) | opaque residual evidence |
| `$0$` | C+(-3) | opaque residual evidence |
| `$2t-3s$` | C+(-3 - 3 s + 2 t) | opaque residual evidence |
| `$3$` | C+(0) | opaque residual evidence |

### q-170675 — observed profile
Field 0: key `selection`, `:answer-field.type/radio`; original correct attribute present: 2.

| Original value | Explicit replay operation | Interpretation |
|---|---|---|
| `$-2$` | C+(-4) | opaque residual evidence |
| `$2$` | C+(0) | opaque residual evidence |
| `$1$` | C+(-1) | opaque residual evidence |
| `$0$` | C+(-2) | opaque residual evidence |
| `$4$` | C+(2) | opaque residual evidence |

### q-37132 — observed profile
Field 0: key `selection`, `:answer-field.type/radio`; original correct attribute present: 5{s}^{4}{t}^{2}-20{s}^{3}\operatorname{sin}⁡t.

| Original value | Explicit replay operation | Interpretation |
|---|---|---|
| `$3{s}^{4}{t}^{2}+10{s}^{3}\operatorname{sin}⁡t$` | C+(2 s^{3} (15 \sin{(t )} - s t^{2})) | opaque residual evidence |
| `$2{s}^{2}{t}^{4}-20s\operatorname{sin}⁡t$` | C+(s (- 20 \sin{(t )} + 2 s t^{4} + 5 s^{2} (4 \sin{(t )} - s t^{2}))) | opaque residual evidence |
| `$5{s}^{4}t-5{s}^{3}\operatorname{sin}⁡t$` | C+(5 s^{3} (3 \sin{(t )} + s t - s t^{2})) | opaque residual evidence |
| `$5{s}^{4}{t}^{2}-20{s}^{3}\operatorname{sin}⁡t$` | C+(0) | opaque residual evidence |
| `$5{s}^{2}{t}^{4}-15s\operatorname{sin}⁡t-5\operatorname{sin}⁡t$` | C+(- 5 \sin{(t )} - 15 s \sin{(t )} + 5 s^{2} t^{4} + 5 s^{3} (4 \sin{(t )} - s t^{2})) | opaque residual evidence |

### q-94811 — observed profile
Field 0: key `selection`, `:answer-field.type/radio`; original correct attribute present: 4t+3.

| Original value | Explicit replay operation | Interpretation |
|---|---|---|
| `$4t+3$` | C+(0) | opaque residual evidence |
| `$5t+4s-1$` | C+(-4 + t + 4 s) | opaque residual evidence |
| `$8t-s$` | C+(-3 - s + 4 t) | opaque residual evidence |
| `$2s-1$` | C+(-4 - 4 t + 2 s) | opaque residual evidence |
| `$2t-s-3$` | C+(-6 - s - 2 t) | opaque residual evidence |

### q-94812 — observed profile
Field 0: key `selection`, `:answer-field.type/radio`; original correct attribute present: 2s(t+1){e}^{t+s}.

| Original value | Explicit replay operation | Interpretation |
|---|---|---|
| `$2s(t+1){e}^{t+s}$` | C+(0) | opaque residual evidence |
| `$2t(s+1){e}^{t+s}$` | C+(2 (t - s) e^{s + t}) | opaque residual evidence |
| `$2(t+s){e}^{t+s}$` | C+(2 t (1 - s) e^{s + t}) | opaque residual evidence |
| `$4t(s-1){e}^{t+s}$` | C+(2 (- s - 2 t + s t) e^{s + t}) | opaque residual evidence |
| `$4(t-s){e}^{t+s}$` | C+(2 (- 2 s + 2 t - s (1 + t)) e^{s + t}) | opaque residual evidence |

### q-94813 — observed profile
Field 0: key `selection`, `:answer-field.type/radio`; original correct attribute present: 2t{e}^{2s+{t}^{2}}.

| Original value | Explicit replay operation | Interpretation |
|---|---|---|
| `$({t}^{2}-1){e}^{2s+{t}^{2}}$` | C+((-1 + t^{2} - 2 t) e^{t^{2} + 2 s}) | opaque residual evidence |
| `$2t{e}^{2s+{t}^{2}}$` | C+(0) | opaque residual evidence |
| `$(t+2){e}^{2s+{t}^{2}}$` | C+((2 - t) e^{t^{2} + 2 s}) | opaque residual evidence |
| `$st{e}^{2s+{t}^{2}}$` | C+(t (-2 + s) e^{t^{2} + 2 s}) | opaque residual evidence |
| `$4{t}^{2}{e}^{2s+{t}^{2}}$` | C+(2 t (-1 + 2 t) e^{t^{2} + 2 s}) | opaque residual evidence |

### q-94815 — observed profile
Field 0: key `selection`, `:answer-field.type/radio`; original correct attribute present: 2(5s-t+s{t}^{2}).

| Original value | Explicit replay operation | Interpretation |
|---|---|---|
| `$s(t+s)^{2}$` | C+(- 10 s + 2 t + s (s + t)^{2} - 2 s t^{2}) | opaque residual evidence |
| `$t(5-s)^{2}$` | C+(- 10 s + 2 t + t (-5 + s)^{2} - 2 s t^{2}) | opaque residual evidence |
| `$4(st+s-t)$` | C+(- 6 s - 2 t - 2 s t^{2} + 4 s t) | opaque residual evidence |
| `$2(5s-t+s{t}^{2})$` | C+(0) | opaque residual evidence |
| `$3s-5t-1$` | C+(-1 - 7 s - 3 t - 2 s t^{2}) | opaque residual evidence |

### q-94816 — observed profile
Field 0: key `selection`, `:answer-field.type/radio`; original correct attribute present: \frac{2(1+2{s}^{2})}{s}.

| Original value | Explicit replay operation | Interpretation |
|---|---|---|
| `$\frac{st+1}{2}$` | C+(\frac{-4 + s (1 - 8 s + s t)}{2 s}) | opaque residual evidence |
| `$\frac{1+{t}^{2}}{s}$` | C+(\frac{-1 + t^{2} - 4 s^{2}}{s}) | opaque residual evidence |
| `$\frac{{t}^{2}-{s}^{2}}{s}$` | C+(\frac{-2 + t^{2} - 5 s^{2}}{s}) | opaque residual evidence |
| `$st({s}^{2}{t}^{2}+1)$` | C+(- 4 s - \frac{2}{s} + s t + s^{3} t^{3}) | opaque residual evidence |
| `$\frac{2(1+2{s}^{2})}{s}$` | C+(0) | opaque residual evidence |

### q-170674 — observed profile
Field 0: key `selection`, `:answer-field.type/radio`; original correct attribute present: -{e}^{s}-2.

| Original value | Explicit replay operation | Interpretation |
|---|---|---|
| `${e}^{s}$` | C+(2 + 2 e^{s}) | opaque residual evidence |
| `${e}^{s}-2t$` | C+(2 - 2 t + 2 e^{s}) | opaque residual evidence |
| `$-{e}^{s}-2$` | C+(0) | opaque residual evidence |
| `${e}^{s}+2+t$` | C+(4 + t + 2 e^{s}) | opaque residual evidence |
| `$-{e}^{s}+t$` | C+(2 + t) | opaque residual evidence |

### q-37208 — observed profile
Field 0: key `selection`, `:answer-field.type/radio`; original correct attribute present: 0.

| Original value | Explicit replay operation | Interpretation |
|---|---|---|
| `$-5$` | C+(-5) | opaque residual evidence |
| `$3$` | C+(3) | opaque residual evidence |
| `$4$` | C+(4) | opaque residual evidence |
| `$0$` | C+(0) | opaque residual evidence |
| `$-2$` | C+(-2) | opaque residual evidence |

### q-37206 — observed profile
Field 0: key `selection`, `:answer-field.type/radio`; original correct attribute present: 5.

| Original value | Explicit replay operation | Interpretation |
|---|---|---|
| `$4$` | C+(-1) | opaque residual evidence |
| `$-6$` | C+(-11) | opaque residual evidence |
| `$3$` | C+(-2) | opaque residual evidence |
| `$5$` | C+(0) | opaque residual evidence |
| `$-1$` | C+(-6) | opaque residual evidence |

### Method-derived default banks

Banks are selected before parameters. For direct partials, the five operations are correct chain sum, omit first active path, omit second active path, differentiate the displayed composite with respect to the other coordinate, and count the first active path twice. Every omitted/duplicated path is computed from the actual map and outer partial; zero paths remain in the worked solution but cannot supply a duplicate omission option.

For coefficient responses A=c1, B=c2, H=c3, complete banks are:

- q-94589: C, A, H, A+H, −C (individual coefficient, omitted middle coefficient or reversed total sign).
- q-170675: C, −C, A, A+H, −A+B+H (reversed total/sign, individual or omitted middle coefficient).
- q-37208: C, A, B, H, A+B.
- q-37206: C, −C, A, B+H, −B−H.

A collision anywhere rejects the whole instance; no post-parameter replacement. Normal profiles have five unequal mathematical values and exactly one correct designation. Source banks are retained separately from these authored banks.

## Stage 4 — reusable masks and constraints

The script compiles each source into whole expression RHS slots, with fixed shared prose and ordered derivative labels. Its family objects derive outer f, coordinate maps, formal partials, structural substitution expressions, map derivatives, explicit three products, individual distributed components, collection, factorization and conclusions. Per-expression notation anchors preserve exact original spelling at original values; changed expressions render from their symbolic recipe. The concluding coefficient prose is a complete independent slot. This is not an original-payload branch.

Coefficient/power variation changes outer relative coefficients, an inner exponent coefficient, a linear-map coefficient or the held-coordinate power; pure overall f scaling is removed from task fingerprints. Bank/profile/option order/seed/notation aliases are excluded; only f/map derivative data relevant to the actual chain calculation remain. In the product-exponential family the constant x scale is removed while both exponent coefficients vary through 1–6, giving substantive substitution variation. In the trigonometric coefficient family y=ct−as retains the exact source three-term square expansion and both slope coefficients vary through 1–6; proportional coefficient vectors are deduplicated, and z’s common b scaling does not inflate task counts. Presentation identities include all displayed prompt, solution, bank and difficulty.

Finite domain bounds (authored policies, not recovered source code):
- q-94589: {'a': [1, 2, 3, 4, 5, 6], 'b': [1, 2, 3, 4, 5, 6]}.
- q-94814: {'a': [1, 2, 3, 4, 5, 6], 'b': [1, 2, 3, 4, 5, 6]}.
- q-170675: {'a': [1, 2, 3, 4, 5, 6], 'b': [1, 2, 3, 4, 5, 6]}.
- q-37132: {'a': [2, 3, 4, 5], 'b': [1, 2, 3, 4, 5, 6]}.
- q-94811: {'a': [1, 2, 3, 4, 5, 6], 'b': [1, 2, 3, 4, 5, 6]}.
- q-94812: {'a': [1, 2, 3, 4, 5, 6], 'b': [1, 2, 3, 4, 5, 6], 'c': [1, 2, 3, 4, 5, 6]}.
- q-94813: {'a': [1, 2, 3, 4, 5, 6], 'b': [1, 2, 3, 4, 5, 6]}.
- q-94815: {'a': [1, 2, 3, 4, 5, 6], 'b': [1, 2, 3, 4, 5, 6]}.
- q-94816: {'a': [1, 2, 3, 4, 5, 6], 'b': [1, 2, 3, 4, 5, 6]}.
- q-170674: {'a': [1, 2, 3, 4, 5, 6], 'b': [1, 2, 3, 4, 5, 6]}.
- q-37208: {'a': [1, 2, 3, 4, 5, 6], 'b': [1, 2, 3, 4, 5, 6], 'c': [1, 2, 3, 4, 5, 6]}.
- q-37206: {'a': [1, 2, 3, 4, 5, 6], 'b': [1, 2, 3, 4, 5, 6]}.
- affine: {'a': [-3, -2, -1, 1, 2, 3], 'b': [-3, -2, -1, 1, 2, 3], 'c': [-3, -2, -1, 1, 2, 3], 'd': [-3, -2, -1, 1, 2, 3], 'e': [-3, -2, -1, 1, 2, 3], 'h': [-3, -2, -1, 1, 2, 3]}.

q-170675 requires s+t≠0; q-94816 requires t>0,s≠0 (real logarithm); q-37206 requires t≠0. Other maps are real on all s,t. Explicit parameters obey the same finite domains as samples.

Source decoded backslash-run inspection: all mathematical answer slash runs have length1 (ord92). JSON display escaping is not a source anomaly. No TeX-slash repair is made.

Raw attribute presence is retained for difficulty, worked solution, fields and correct refs; the one missing correct ref is reported as missing, never a matched designation. Exact-source replay remains public generate(..., profile="observed"); minimally normalized duplicate layout is public profile="observed-repaired" and remains evidence-only.

The quotient family q-170675 keeps a single numerator in the substituted x partial and first branch product, combines the three branch fractions over (s+t)^2, then expands and collects the numerator. Changed coefficients preserve these operations. Validation rejects an algebraically equivalent sum-of-fractions replacement that skips the common-denominator step.
