# Template extraction

## Stage 1: specific source descriptions

Below, each original coordinate pair, domain, supplied parameter, complete field layout and bank are preserved separately. Exact prompt and solution prose is retained in source.json and review.md. Numbers are exact; positive square-root arguments and familiar trigonometric arguments remain fixed under coordinate scaling. Original variable theta is preserved in trig answers; t is used elsewhere.

### trig — 17592186083909 (q-6731)

Original x: `$3\operatorname{sin}⁡\theta `; y: `$5\operatorname{cos}⁡\theta `; domain: `$0\le \theta <2\pi ,`; supplied parameter: `None`.

Field 0: `:answer-field.type/radio`, key `selection`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$\frac{dy}{dx}=-\frac{5}{3}\operatorname{tan}⁡\theta ` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |
| `$\frac{dy}{dx}=-\frac{5}{3}\operatorname{cot}⁡\theta ` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$\frac{dy}{dx}=\frac{5}{3}\operatorname{tan}⁡\theta ` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$\frac{dy}{dx}=-\frac{3}{5}\operatorname{cot}⁡\theta ` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$\frac{dy}{dx}=-\frac{3}{5}\operatorname{tan}⁡\theta ` | `(s/r) × entire original RHS`; no recovered intent asserted | no |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(\theta )}{{x}^{′}(\theta )}.
$$

$$
{x}^{′}(\theta )=3\operatorname{cos}⁡\theta ,\,{y}^{′}(\theta )=-5\operatorname{sin}⁡\theta .
$$

$$
\frac{dy}{dx}=\frac{-5\operatorname{sin}⁡\theta }{3\operatorname{cos}⁡\theta }=-\frac{5}{3}\operatorname{tan}⁡\theta .
$$

### exp_poly — 17592186083911 (q-6809)

Original x: `${e}^{t}`; y: `$2{t}^{2}`; domain: `$-\infty <t<\infty ,`; supplied parameter: `5`.

Field 0: `:answer-field.type/radio`, key `selection`; correct designation absent legacy.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$5 \cdot e^{2}` | `(s/r) × entire original RHS`; no recovered intent asserted | no original designation |
| `$4 \cdot e^{5}` | `(s/r) × entire original RHS`; no recovered intent asserted | no original designation |
| `$\frac{20}{e^{5}}` | `(s/r) × entire original RHS`; no recovered intent asserted | no original designation |
| `$\frac{5}{e^{2}}` | `(s/r) × entire original RHS`; no recovered intent asserted | no original designation |
| `$20 \cdot e^{5}` | `(s/r) × entire original RHS`; no recovered intent asserted | no original designation |
Field 1: `:answer-field.type/radio`, key `selection`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$4\cdot {e}^{5}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$5\cdot {e}^{2}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$20\cdot {e}^{5}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$\frac{20}{{e}^{5}}` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |
| `$\frac{5}{{e}^{2}}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)={e}^{t},\,{y}^{′}(t)=4t.
$$

$$
\frac{dy}{dx}=\frac{4t}{{e}^{t}}.
$$

$$
\begin{aligned}\frac{dy}{dx} & =\frac{4\cdot 5}{{e}^{5}} \\  & =\frac{20}{{e}^{5}}\,.\end{aligned}
$$

### quadratic — 17592186290260 (q-20988)

Original x: `$3{t}^{2}-2t`; y: `${t}^{2}-1`; domain: `$-\infty <t<\infty ,`; supplied parameter: `2`.

Field 0: `:answer-field.type/radio`, key `selection`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$\frac{2}{7}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$\frac{2}{5}` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |
| `$\frac{3}{4}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$\frac{3}{7}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$\frac{4}{5}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=6t-2,\,{y}^{′}(t)=2t.
$$

$$
\frac{dy}{dx}=\frac{2t}{6t-2}=\frac{t}{3t-1}.
$$

$$
\begin{aligned}\frac{dy}{dx} & =\frac{2}{3(2)-1} \\  & =\frac{2}{6-1} \\  & =\frac{2}{5}.\end{aligned}
$$

### expneg_poly — 17592186321110 (q-353340)

Original x: `$4{e}^{-t}`; y: `${t}^{2}+6t`; domain: `$0\le t<\infty ,`; supplied parameter: `1`.

Field 0: `:answer-field.type/blank`, key `field-1`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$-2e` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=-4{e}^{-t},\,{y}^{′}(t)=2t+6.
$$

$$
\frac{dy}{dx}=\frac{2t+6}{(-4{e}^{-t})}.
$$

$$
\begin{aligned}\frac{dy}{dx}{|}_{t\,=\,1} & =\frac{2(1)+6}{(-4{e}^{-1})} \\  & =\frac{8e}{(-4)} \\  & =-2e.\end{aligned}
$$

### trig_double — 17592186321111 (q-353341)

Original x: `$5\operatorname{sin}⁡2t`; y: `$\sqrt{3}\operatorname{cos}⁡2t`; domain: `$0\le t<2\pi ,`; supplied parameter: `pi/6`.

Field 0: `:answer-field.type/blank`, key `field-1`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$-\frac{3}{5}` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=10\operatorname{cos}⁡2t,\,{y}^{′}(t)=-2\sqrt{3}\operatorname{sin}⁡2t.
$$

$$
\frac{dy}{dx}=\frac{(-2\sqrt{3}\operatorname{sin}⁡2t)}{10\operatorname{cos}⁡2t}=-\frac{\sqrt{3}}{5}\operatorname{tan}⁡2t.
$$

$$
\begin{aligned}\frac{dy}{dx} & =-\frac{\sqrt{3}}{5}\cdot \operatorname{tan}⁡(2\cdot \frac{\pi }{6}) \\  & =-\frac{\sqrt{3}}{5}\cdot \operatorname{tan}⁡(\frac{\pi }{3}) \\  & =-\frac{\sqrt{3}}{5}\cdot \sqrt{3} \\  & =-\frac{3}{5}\,.\end{aligned}
$$

### exp_poly_chain — 17592186321112 (q-353343)

Original x: `${e}^{2t}`; y: `$3{t}^{2}`; domain: `$-\infty <t<\infty ,`; supplied parameter: `2`.

Field 0: `:answer-field.type/blank`, key `field-1`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$\frac{6}{{e}^{4}}` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=2{e}^{2t},\,{y}^{′}(t)=6t.
$$

$$
\frac{dy}{dx}=\frac{6t}{2{e}^{2t}}=\frac{3t}{{e}^{2t}}.
$$

$$
\begin{aligned}\frac{dy}{dx}{|}_{t\,=\,2} & =\frac{3\cdot 2}{{e}^{4}} \\  & =\frac{6}{{e}^{4}}.\end{aligned}
$$

### line_poly — 17592186321113 (q-353344)

Original x: `$5t-3`; y: `${t}^{4}+2t`; domain: `$-\infty <t<\infty ,`; supplied parameter: `1`.

Field 0: `:answer-field.type/blank`, key `field-1`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$\frac{6}{5}` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=5,\,{y}^{′}(t)=4{t}^{3}+2.
$$

$$
\frac{dy}{dx}=\frac{4{t}^{3}+2}{5}.
$$

$$
\begin{aligned}\frac{dy}{dx}{|}_{t\,=\,1} & =\frac{4(1)^{3}+2}{5} \\  & =\frac{6}{5}.\end{aligned}
$$

### sqrt_linear — 17592186321114 (q-353346)

Original x: `$\sqrt{t}`; y: `$8t-3`; domain: `$0\le t<\infty ,`; supplied parameter: `4`.

Field 0: `:answer-field.type/blank`, key `field-1`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$32` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=\frac{1}{2\sqrt{t}},\,{y}^{′}(t)=8.
$$

$$
\frac{dy}{dx}=\frac{8}{(\frac{1}{2\sqrt{t}})}=16\sqrt{t}.
$$

$$
\begin{aligned}\frac{dy}{dx}{|}_{t\,=\,4} & =16\sqrt{4} \\  & =16(2) \\  & =32.\end{aligned}
$$

### exp_pair — 17592186321115 (q-353347)

Original x: `${e}^{3t}`; y: `$2{e}^{t}`; domain: `$-\infty <t<\infty ,`; supplied parameter: `None`.

Field 0: `:answer-field.type/blank`, key `field-1`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$\frac{2}{3}{e}^{-2t}` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=3{e}^{3t},\,{y}^{′}(t)=2{e}^{t}.
$$

$$
\frac{dy}{dx}=\frac{2{e}^{t}}{3{e}^{3t}}=\frac{2}{3}{e}^{-2t}.
$$

### quartic — 17592186335950 (q-6810)

Original x: `${t}^{4}+t-1`; y: `${t}^{3}`; domain: `$-\infty <t<\infty ,`; supplied parameter: `-1`.

Field 0: `:answer-field.type/radio`, key `selection`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$-2` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$-\,\frac{1}{4}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$-1` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |
| `$-\,\frac{2}{3}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$-\,\frac{1}{2}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=4{t}^{3}+1,\,{y}^{′}(t)=3{t}^{2}.
$$

$$
\frac{dy}{dx}=\frac{3{t}^{2}}{4{t}^{3}+1}.
$$

$$
\begin{aligned}\frac{dy}{dx} & =\frac{3(-1)^{2}}{4(-1)^{3}+1} \\  & =\frac{3}{(-4)+1} \\  & =-1\,.\end{aligned}
$$

### exp_product — 17592186335953 (q-6816)

Original x: `${e}^{2t}`; y: `$({t}^{2}-1){e}^{-t}`; domain: `$-\infty <t<\infty ,`; supplied parameter: `1`.

Field 0: `:answer-field.type/radio`, key `selection`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$\frac{{e}^{2}}{3}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `${e}^{-2}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$2{e}^{-2}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `${e}^{-3}` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |
| `$\frac{{e}^{-3}}{4}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=2{e}^{2t},\,{y}^{′}(t)=(1+2t-{t}^{2}){e}^{-t}.
$$

$$
\frac{dy}{dx}=\frac{(1+2t-{t}^{2}){e}^{-t}}{2{e}^{2t}}=\frac{1}{2}(1+2t-{t}^{2}){e}^{-3t}.
$$

$$
\begin{aligned}\frac{dy}{dx} & =\frac{1}{2}(1+2(1)-(1)^{2}){e}^{-3(1)} \\  & =\frac{1}{2}(1+2-1){e}^{-3} \\  & ={e}^{-3}\,.\end{aligned}
$$

### quintic — 17592186335963 (q-6848)

Original x: `${t}^{5}-2t`; y: `$1-{t}^{3}`; domain: `$-\infty <t<\infty ,`; supplied parameter: `-1`.

Field 0: `:answer-field.type/radio`, key `selection`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$-\,\frac{1}{3}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$-\,\frac{3}{2}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$-\,\frac{1}{2}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$-3` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$-1` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=5{t}^{4}-2,\,{y}^{′}(t)=-3{t}^{2}.
$$

$$
\frac{dy}{dx}=\frac{-3{t}^{2}}{5{t}^{4}-2}.
$$

$$
\begin{aligned}\frac{dy}{dx} & =\frac{-3(-1)^{2}}{5(-1)^{4}-2} \\  & =\frac{-3}{5-2} \\  & =-1\,.\end{aligned}
$$

### root_power — 17592186368467 (q-353349)

Original x: `$\sqrt{t}`; y: `$3{t}^{3/2}`; domain: `$0<t<\infty ,`; supplied parameter: `None`.

Field 0: `:answer-field.type/blank`, key `field-1`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$9t` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=\frac{1}{2\sqrt{t}},\,{y}^{′}(t)=\frac{9}{2}\sqrt{t}.
$$

$$
\frac{dy}{dx}=\frac{(\frac{9}{2}\sqrt{t})}{(\frac{1}{2\sqrt{t}})}=9t.
$$

### line_quad — 17592186395776 (q-20849)

Original x: `$2(t+1)`; y: `$4{t}^{2}`; domain: `$-1\le t<1,`; supplied parameter: `0`.

Field 0: `:answer-field.type/radio`, key `selection`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$3` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$2` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$1` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$0` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |
| `$-1` | `(s/r) × entire original RHS`; no recovered intent asserted | no |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=2,\,{y}^{′}(t)=8t.
$$

$$
\frac{dy}{dx}=\frac{8t}{2}=4t.
$$

$$
\begin{aligned}\frac{dy}{dx} & =4(0) \\  & =0\,.\end{aligned}
$$

### sqrt_scaled — 17592186401840 (q-20851)

Original x: `$2\sqrt{t}`; y: `$12t+1`; domain: `$0\le t<\infty ,`; supplied parameter: `1`.

Field 0: `:answer-field.type/radio`, key `selection`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$12` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |
| `$10` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$3` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$15` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$7` | `(s/r) × entire original RHS`; no recovered intent asserted | no |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=\frac{1}{\sqrt{t}},\,{y}^{′}(t)=12.
$$

$$
\frac{dy}{dx}=\frac{12}{\frac{1}{\sqrt{t}}}=12\sqrt{t}.
$$

$$
\begin{aligned}\frac{dy}{dx} & =12\sqrt{1} \\  & =12\,.\end{aligned}
$$

### texp_poly — 17592186401853 (q-20990)

Original x: `$2t{e}^{t}`; y: `${t}^{2}+2t`; domain: `$0\le t<\infty ,`; supplied parameter: `1`.

Field 0: `:answer-field.type/radio`, key `selection`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$\frac{1}{2e}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$\frac{1}{{e}^{2}}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$\frac{1}{3e}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$\frac{1}{{e}^{3}}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$\frac{1}{e}` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=2{e}^{t}(t+1),\,{y}^{′}(t)=2t+2.
$$

$$
\frac{dy}{dx}=\frac{2t+2}{2{e}^{t}(t+1)}=\frac{1}{{e}^{t}}.
$$

$$
\begin{aligned}\frac{dy}{dx} & =\frac{1}{{e}^{1}} \\  & =\frac{1}{e}\,.\end{aligned}
$$

### product_sin — 17592186403272 (q-6812)

Original x: `$({t}^{3}-1){e}^{t}`; y: `$2\operatorname{sin}⁡t`; domain: `$-\infty <t<\infty ,`; supplied parameter: `0`.

Field 0: `:answer-field.type/radio`, key `selection`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$-\,\frac{1}{2}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$-\,\frac{1}{2e}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$-\,\frac{e}{2}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$-2` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |
| `$-\,\frac{1}{3e}` | `(s/r) × entire original RHS`; no recovered intent asserted | no |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(t)}{{x}^{′}(t)}.
$$

$$
{x}^{′}(t)=({t}^{3}+3{t}^{2}-1){e}^{t},\,{y}^{′}(t)=2\operatorname{cos}⁡t.
$$

$$
\frac{dy}{dx}=\frac{2\operatorname{cos}⁡t}{({t}^{3}+3{t}^{2}-1){e}^{t}}.
$$

$$
\begin{aligned}\frac{dy}{dx} & =\frac{2\operatorname{cos}⁡0}{({0}^{3}+3\cdot {0}^{2}-1){e}^{0}} \\  & =\frac{2(1)}{(-1)\cdot 1} \\  & =-2\,.\end{aligned}
$$

### trig_scaled — 17592186403279 (q-6836)

Original x: `$12\operatorname{sin}⁡\theta `; y: `$15\operatorname{cos}⁡\theta `; domain: `$0\le \theta <2\pi ,`; supplied parameter: `None`.

Field 0: `:answer-field.type/radio`, key `selection`; correct designation present.

| Complete original value | Recipe in public observed profile | Correct |
|---|---|---|
| `$\frac{dy}{dx}=-\frac{4}{5}\operatorname{tan}⁡\theta ` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$\frac{dy}{dx}=-\frac{4}{5}\operatorname{cot}⁡\theta ` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$\frac{dy}{dx}=-\frac{5}{4}\operatorname{cot}⁡\theta ` | `(s/r) × entire original RHS`; no recovered intent asserted | no |
| `$\frac{dy}{dx}=-\frac{5}{4}\operatorname{tan}⁡\theta ` | `(s/r) × entire original RHS`; no recovered intent asserted | yes |
| `$\frac{dy}{dx}=\frac{5}{4}\operatorname{tan}⁡\theta ` | `(s/r) × entire original RHS`; no recovered intent asserted | no |

Observed fixed solution blocks:

$$
\frac{dy}{dx}=\frac{{y}^{′}(\theta )}{{x}^{′}(\theta )}.
$$

$$
{x}^{′}(\theta )=12\operatorname{cos}⁡\theta ,\,{y}^{′}(\theta )=-15\operatorname{sin}⁡\theta .
$$

$$
\frac{dy}{dx}=\frac{-15\operatorname{sin}⁡\theta }{12\operatorname{cos}⁡\theta }=-\frac{5}{4}\operatorname{tan}⁡\theta .
$$

## Stage 2: generalized instructional pattern

Differentiate x and y with respect to their common parameter, divide y′ by x′, simplify in the source family’s order, and, when t is supplied, substitute and evaluate exactly. Curve values x and y are not slope values. The easy sources use directly recognizable power, exponential, sine/cosine or root derivatives. Moderate sources require a product/chain rule or signed simplification before the same quotient/evaluation. The authored hard families require the prerequisite product or quotient rule for both coordinate derivatives.

## Stage 3: component mapping

Every source has complete component slots for x(t), y(t), its derivative pair, each successive quotient expression and each aligned substitution/evaluation expression. Source prose is shared unchanged and answer feedback is not invented. The formula y′/x′ stays fixed. Coordinate scaling parameters r,s transform x→rx and y→sy, x′→rx′ and y′→sy′. Each initial displayed fraction scales its complete numerator by s and denominator by r; each remaining algebraic stage scales by s/r. Thus factorization, cancellation, power evaluation and collected stages are retained independently. Scalar historical banks generalize the complete mathematical value by the same s/r scaling; complete-equation trig choices scale only their RHS. This mapping reproduces all values and stage shapes but does not infer historical distractor intent.

Normal radio banks are complete operation families, not a first-valid pool: correct y′/x′; reciprocal x′/y′; undifferentiated y/x; derivative product x′y′; and y′/x (omit differentiation of x). The exp_poly family replaces the last member with y″/x′ because x′=x makes that omission indistinguishable. At the product_sin anchor t=0, x′=−x's magnitude and y=0 cause generic banks to collide; its complete bank uses correct, sign omission, reciprocal, reciprocal plus sign omission, and undifferentiated ratio. At line_quad's zero derivative, the complete bank uses correct, y″/x′, x′/y″, x/x′ and y″. These labeled author operations are metadata only; no option-specific explanations are added to learner content. All five entries must be finite and pairwise inequivalent.

## Stage 4: reusable masks and parameter policy

Public API uses easy/moderate/hard entrypoints and generate(level,seed,template,field_type,parameters,profile). Observed:<source ID> selects faithful evidence; method is the normal bank. Explicit source parameters r,s are positive half-integers 1/2..6 (12 choices each). Their roles affect the actual coordinate functions and derivative components; this yields broad same-method coefficient variation without adding new function arguments or harder evaluation angles. Rejected explicit banks raise ValueError instead of resampling. Defaults select the family first and then sample a complete valid instance, so every supported source family is served.

Authored product_pair uses x=at exp(bt), y=c(t²+d) exp(−bt); quotient_pair uses x=at/(t+b), y=ct²/(t+d), t>0. Bounds: a,c integers 1..5, b 1..3, d 1..4 (300 parameter tuples each). Both rules show formal differentiated component operators, substituted derivatives, factor/expansion and collection, initial dy/dx fraction, and final quotient/exponential simplification. Boundaries apply equally to samplers and explicit calls. These difficulty labels and masks are authored, not observed. Hard defaults are blanks, consistent with the supported source blank fragment shape.

Mathematical fingerprints normalize the complete parameterized coordinate pair and supplied t/domain/level; parameter variable spelling, profile and answer ordering are absent. They identify the functions actually differentiated, rather than treating identical final slopes of different curves as duplicate input tasks. Presentation fingerprints use actual prompt, fixed solution, complete bank, difficulty and version; IDs are seed/order independent. Legacy/source provenance and domain/recipe metadata remain outside learner question fields.
