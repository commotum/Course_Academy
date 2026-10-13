# Four-stage template extraction

## 1. Specific sources

All questions ask for a whole definite integral equivalent to a displayed scalar line integral. No free-entry blank occurs. Every bank has five choices and one `selection` radio field. Exact strings, enum types and original keyed values remain in source.json; parameter recipes below account for every option rather than just the correct one.

### q-167608 — parabola

Which of the following is equivalent to the integral ${\int }_{C}\frac{x}{4y+1}\text{d}s,$ where the curve $C$ is parametrized by $r(t)=t\,i+{t}^{2}\,j\,$ for $0\le t\le 1?$

Curve: `(t, t**2)`; scalar: `x/(4*y + 1)`; interval `(0, 1)`. Captured rating: :question.difficulty/easy. Full observed bank profile: `observed:q-167608`.

| Source option UUID | Type | Exact captured value | Parameterized integrand recipe | Original correct designation |
|---|---|---|---|---|
| 263de2e3-27ae-52e2-8582-4dfb39ba6ffc | :answer.type/math | `{\int }_{0}^{1}(4{t}^{2}+1)\text{d}t` | `m*(4*t**2 + 1)`, bounds lo,hi | no |
| 75614e75-3308-50a7-a253-f1f9b76e3296 | :answer.type/math | `{\int }_{0}^{1}\frac{{t}^{2}}{\sqrt{2t+1}}\text{d}t` | `m*(t**2/sqrt(2*t + 1))`, bounds lo,hi | no |
| 76433ca0-b7f8-577e-a495-c0ae272242e3 | :answer.type/math | `{\int }_{0}^{1}\frac{t}{\sqrt{4{t}^{2}+1}}\text{d}t` | `m*(t/sqrt(4*t**2 + 1))`, bounds lo,hi | yes |
| 89172764-a6f4-5672-8136-d35db577b74a | :answer.type/math | `{\int }_{0}^{1}t(2t+1)\text{d}t` | `m*(t*(2*t + 1))`, bounds lo,hi | no |
| 8caffd9e-930e-5e4b-b97e-bcbc15c29c0d | :answer.type/math | `{\int }_{0}^{1}t\sqrt{4{t}^{2}+1}\text{d}t` | `m*(t*sqrt(4*t**2 + 1))`, bounds lo,hi | no |

Captured aligned row counts in order: [6, 1, 3]. The complete original solution prose is retained; amplitude multiplies each complete scalar RHS once and each concrete definite integral once. Generic f(r(t)) and ||r′(t)|| already refer to the printed objects and receive no extra numerical factor.

### q-40253 — difference

Which of the following is equivalent to ${\int }_{C}f(x,y)\,\text{d}s,$ where $f(x,y)=\sqrt{2}(x-y)$ and the curve $C$ is parametrized 
 by $r(t)=⟨{t}^{2}+t,\,{t}^{2}-t⟩$ for $t\in [0,\sqrt{2}]?$

Curve: `(t**2 + t, t**2 - t)`; scalar: `sqrt(2)*(x - y)`; interval `(0, sqrt(2))`. Captured rating: :question.difficulty/moderate. Full observed bank profile: `observed:q-40253`.

| Source option UUID | Type | Exact captured value | Parameterized integrand recipe | Original correct designation |
|---|---|---|---|---|
| 2e006fbf-73db-5714-80d3-da70e1961752 | :answer.type/math | `4{\int }_{0}^{\sqrt{2}}t\sqrt{4{t}^{2}+1}\,\text{d}t.` | `m*(4*t*sqrt(4*t**2 + 1))`, bounds lo,hi | yes |
| 4454bda2-b710-5b8e-962a-af8f72db9bed | :answer.type/math | `{\int }_{0}^{\sqrt{2}}t\sqrt{2{t}^{2}+1}\,\text{d}t.` | `m*(t*sqrt(2*t**2 + 1))`, bounds lo,hi | no |
| 969d3d60-bae9-5b94-bb58-6e2e78279810 | :answer.type/math | `\sqrt{2}{\int }_{0}^{\sqrt{2}}t\sqrt{2{t}^{2}-1}\,\text{d}t.` | `m*(sqrt(2)*t*sqrt(2*t**2 - 1))`, bounds lo,hi | no |
| dc88ce8a-6d69-5cce-ae62-6e652a14c027 | :answer.type/math | `4{\int }_{0}^{\sqrt{2}}t\sqrt{8{t}^{2}+1}\,\text{d}t.` | `m*(4*t*sqrt(8*t**2 + 1))`, bounds lo,hi | no |
| e1fc0716-e381-59ad-99c7-f5348e2706dd | :answer.type/math | `2{\int }_{0}^{\sqrt{2}}t\sqrt{4{t}^{2}+1}\,\text{d}t.` | `m*(2*t*sqrt(4*t**2 + 1))`, bounds lo,hi | no |

Captured aligned row counts in order: [8, 2, 3]. The complete original solution prose is retained; amplitude multiplies each complete scalar RHS once and each concrete definite integral once. Generic f(r(t)) and ||r′(t)|| already refer to the printed objects and receive no extra numerical factor.

### q-76377 — squares

Which of the following is equivalent to ${\int }_{C}f(x,y,z)\,\text{d}s,$ where $f(x,y,z)=2x-{y}^{2}-{z}^{2}$ and the curve $C$ is parametrized by $r(t)=⟨{t}^{2},\,t-1,\,t+1⟩$ for $t\in [0,3]?$

Curve: `(t**2, t - 1, t + 1)`; scalar: `2*x - y**2 - z**2`; interval `(0, 3)`. Captured rating: :question.difficulty/moderate. Full observed bank profile: `observed:q-76377`.

| Source option UUID | Type | Exact captured value | Parameterized integrand recipe | Original correct designation |
|---|---|---|---|---|
| 372a5048-17c2-5076-9635-4ff4ad531da9 | :answer.type/math | `-2{\int }_{0}^{3}({t}^{2}+2t-1)\sqrt{{t}^{2}+1}\,\text{d}t` | `m*(sqrt(t**2 + 1)*(-2*t**2 - 4*t + 2))`, bounds lo,hi | no |
| 60710012-7ccb-54d9-aac8-7c21a4db39de | :answer.type/math | `-2\sqrt{2}{\int }_{0}^{3}\sqrt{2{t}^{2}+1}\,\text{d}t` | `m*(-2*sqrt(2)*sqrt(2*t**2 + 1))`, bounds lo,hi | yes |
| 7143c54a-f0e9-502c-b646-975daaf14a0b | :answer.type/math | `-2{\int }_{0}^{3}t\sqrt{{t}^{2}+1}\,\text{d}t` | `m*(-2*t*sqrt(t**2 + 1))`, bounds lo,hi | no |
| 77d755de-6003-5532-a85f-2d9e8cb137d2 | :answer.type/math | `\sqrt{2}{\int }_{0}^{3}({t}^{2}-2t)\sqrt{2{t}^{2}+1}\,\text{d}t` | `m*(sqrt(2)*(t**2 - 2*t)*sqrt(2*t**2 + 1))`, bounds lo,hi | no |
| bc8c1d1a-5321-50f7-aff8-7b81e9c745ec | :answer.type/math | `{\int }_{0}^{3}({t}^{2}+2t)\sqrt{2{t}^{2}+1}\,\text{d}t` | `m*((t**2 + 2*t)*sqrt(2*t**2 + 1))`, bounds lo,hi | no |

Captured aligned row counts in order: [6, 4, 5]. The complete original solution prose is retained; amplitude multiplies each complete scalar RHS once and each concrete definite integral once. Generic f(r(t)) and ||r′(t)|| already refer to the printed objects and receive no extra numerical factor.

### q-76356 — quadratic3

Which of the following is equivalent to ${\int }_{C}f(x,y,z)\,\text{d}s,$ where $f(x,y,z)=x+y-z$ and the curve $C$ is parametrized by $r(t)=⟨{t}^{2}+1,\,{t}^{2}-1,\,{t}^{2}⟩$ for $t\in [0,2]?$

Curve: `(t**2 + 1, t**2 - 1, t**2)`; scalar: `x + y - z`; interval `(0, 2)`. Captured rating: :question.difficulty/moderate. Full observed bank profile: `observed:q-76356`.

| Source option UUID | Type | Exact captured value | Parameterized integrand recipe | Original correct designation |
|---|---|---|---|---|
| f72ef384-5e6e-52c5-839e-3beee185405e | :answer.type/math | `2{\int }_{0}^{2}{t}^{2}\sqrt{t+1}\,\text{d}t` | `m*(2*t**2*sqrt(t + 1))`, bounds lo,hi | no |
| 42147aee-d1b6-54a9-a34c-6883f2cfc5ab | :answer.type/math | `2\sqrt{3}{\int }_{0}^{2}{t}^{3}\,\text{d}t` | `m*(2*sqrt(3)*t**3)`, bounds lo,hi | yes |
| 38308454-7a76-5601-988c-cc81a2d49d69 | :answer.type/math | `\sqrt{2}{\int }_{0}^{2}({t}^{2}-t)\sqrt{t+1}\,\text{d}t` | `m*(sqrt(2)*sqrt(t + 1)*(t**2 - t))`, bounds lo,hi | no |
| 9d940168-caf2-55dc-abc9-6478a8eb7fed | :answer.type/math | `2{\int }_{0}^{2}{t}^{2}\sqrt{{t}^{2}-t}\,\text{d}t` | `m*(2*t**2*sqrt(t**2 - t))`, bounds lo,hi | no |
| 89f9a881-2016-5d9d-b0c2-417ca0dbf7d0 | :answer.type/math | `\sqrt{3}{\int }_{0}^{2}{t}^{2}\sqrt{{t}^{2}+1}\,\text{d}t` | `m*(sqrt(3)*t**2*sqrt(t**2 + 1))`, bounds lo,hi | no |

Captured aligned row counts in order: [9, 3, 3]. The complete original solution prose is retained; amplitude multiplies each complete scalar RHS once and each concrete definite integral once. Generic f(r(t)) and ||r′(t)|| already refer to the printed objects and receive no extra numerical factor.

### q-76379 — helix

Which of the following is equivalent to the integral ${\int }_{C}z({x}^{2}-{y}^{2})\,\text{d}s,$ where the curve $C$ is parametrized by $r(t)=\operatorname{cos}⁡t\,i+\operatorname{sin}⁡t\,j\,+t\,k$ for $\,0\le t\le \frac{\pi }{2}?$

Curve: `(cos(t), sin(t), t)`; scalar: `z*(x**2 - y**2)`; interval `(0, pi/2)`. Captured rating: :question.difficulty/moderate. Full observed bank profile: `observed:q-76379`.

| Source option UUID | Type | Exact captured value | Parameterized integrand recipe | Original correct designation |
|---|---|---|---|---|
| fa31ddbb-d2dc-5e24-b119-3e57906a0e43 | :answer.type/math | `\sqrt{2}{\int }_{0}^{\pi /2}t\operatorname{cos}⁡t\sqrt{2{cos}^{2}⁡t+1}\,\text{d}t` | `m*(sqrt(2)*t*sqrt(2*cos(t)**2 + 1)*cos(t))`, bounds lo,hi | no |
| 6e191add-76d4-52b0-a4d0-b55782dad06f | :answer.type/math | `\sqrt{2}{\int }_{0}^{\pi /2}t\operatorname{cos}⁡2t\,\text{d}t` | `m*(sqrt(2)*t*cos(2*t))`, bounds lo,hi | yes |
| e78b94bc-a9b3-5508-8e70-1864ef024d69 | :answer.type/math | `2\sqrt{2}{\int }_{0}^{\pi /2}t\operatorname{sin}⁡t\sqrt{2{cos}^{2}⁡t+3}\,\text{d}t` | `m*(2*sqrt(2)*t*sqrt(2*cos(t)**2 + 3)*sin(t))`, bounds lo,hi | no |
| 0c7e2485-49a8-54d2-9942-acfa1e262b9a | :answer.type/math | `2{\int }_{0}^{\pi /2}t(\operatorname{cos}⁡t-\operatorname{sin}⁡t)\,\text{d}t` | `m*(2*t*(-sin(t) + cos(t)))`, bounds lo,hi | no |
| 1e167558-c450-5d8c-885f-dd7f2edd9925 | :answer.type/math | `2{\int }_{0}^{\pi /2}t(\operatorname{cos}⁡t-\operatorname{sin}⁡t)^{2}\,\text{d}t` | `m*(2*t*(-sin(t) + cos(t))**2)`, bounds lo,hi | no |

Captured aligned row counts in order: [8, 3, 3]. The complete original solution prose is retained; amplitude multiplies each complete scalar RHS once and each concrete definite integral once. Generic f(r(t)) and ||r′(t)|| already refer to the printed objects and receive no extra numerical factor.

### q-76368 — linear_cubic

Which of the following is equivalent to the integral $\displaystyle \int_(C)(x^{3} - y)ds$, where the curve $C$ is parametrized by $r(t) = 2ti + (2 - t)j$ for $-1 \le t \le 2$?

Curve: `(2*t, 2 - t)`; scalar: `x**3 - y`; interval `(-1, 2)`. Captured rating: **absent**. Full observed bank profile: `observed:q-76368`.

| Source option UUID | Type | Exact captured value | Parameterized integrand recipe | Original correct designation |
|---|---|---|---|---|
| f149a5c8-374a-5613-9e94-f7a85f4e3578 | :answer.type/text | `$\sqrt{5}\displaystyle \int_{-1}^{2}(8t^{3} + t - 2)dt$.` | `m*(sqrt(5)*(8*t**3 + t - 2))`, bounds lo,hi | missing entire key |
| 07f01a2c-6102-5f57-9a81-827ca9995533 | :answer.type/math | `\sqrt{2}\displaystyle \int_{-1}^{2}(4t^{3} - 3)dt` | `m*(sqrt(2)*(4*t**3 - 3))`, bounds lo,hi | missing entire key |
| 0e53f525-69b5-5819-9c6b-7b1f40a1280e | :answer.type/math | `2\displaystyle \int_{-1}^{2}(t^{3} - t^{2} + 4t)dt` | `m*(2*t**3 - 2*t**2 + 8*t)`, bounds lo,hi | missing entire key |
| 0f8c7275-20d2-58af-b910-a3018cd7a77a | :answer.type/math | `3\displaystyle \int_{-1}^{2}(8t^{3} - t^{2} + 4t - 4)dt` | `m*(24*t**3 - 3*t**2 + 12*t - 12)`, bounds lo,hi | missing entire key |
| 4cb682b0-7b0d-59e5-8435-a35378e856c6 | :answer.type/math | `\displaystyle \int_{-1}^{2}(8t^{3} + t^{2} - 4)dt` | `m*(8*t**3 + t**2 - 4)`, bounds lo,hi | missing entire key |

Captured aligned row counts in order: []. The complete original solution prose is retained; amplitude multiplies each complete scalar RHS once and each concrete definite integral once. Generic f(r(t)) and ||r′(t)|| already refer to the printed objects and receive no extra numerical factor.

## 2. Generalized pattern

Given a scalar f, actual displayed r(t) and actual interval [lo,hi], write integral_C f ds = integral_lo^hi f(r(t)) ||r′(t)|| dt. The requested response is the whole definite integral. Every option must have an unequal **full evaluated value**, even if two integrands/bounds look structurally different. Default construction computes coordinate derivatives, squared speed, speed, substituted f, and their product, preserving source prose/stage ordering. It never teaches evaluating the integral. The validator may evaluate it to reject ambiguous choices.

## 3. Components and complete banks

The table above maps all30 captured choices one-to-one to full expression recipes. Parameters m,lo,hi preserve each complete historical pattern. Historical numerical wrong choices do not identify original author intent; these recipes recover expression shape, **not** a method-error explanation. All observed profiles therefore have evidence_only=true and eligible_for_learning=false, even when their choices happen to be real and unequal. Public raw q-76368 still omits its missing key/rating/solution. Separate evidence-only completed-source supplies the independently proven key sqrt5 integral(8t^3+t-2)dt and an authored solution/rating; it is not counted as an exact captured designation.

Normal complete `method` profile (the cubic family retains its correct text option with dollar delimiters and period; its other four choices remain math): [f(r)*speed, f(r), f(r)*speed², f(r)/speed, wrong_f(r)*speed]. Labels respectively correct, omitted metric factor, duplicated metric factor (actual speed squared), inverted metric factor, wrong coordinate substitution/sign. Each family's final wrong substitution is explicit: parabola substitutes y into numerator instead of x; difference uses x+y instead of x-y; squares reverses the two scalar square signs; quadratic3 uses x+y+z; helix uses z(x²+y²); linear cubic uses x³+y; hard uses xy+z². No unrelated final perturbation occurs. Every eligible bank is chosen before sampling, built entirely and rejected as a whole on an equal full scalar value or an unresolved exact inequality. Choice order alone cannot alter content identity.

## 4. Reusable masks and constraints

Full scalar components, full source interval components and full definite-integral bounds are explicit slots. No short x/y/t string substitution is used. Source aligned scalar rows are full RHS masks; derivative/magnitude rows stay tied to the actual fixed source curve. Source concrete-integral rows receive amplitude once; generic formal rows are unchanged. Intermediate expansion, cancellation and trig identity rows are preserved, including q-76377's four scalar rows and q-76356's absolute value stage. Source questions with no solution retain omission raw; completed normal cubic and hard use full operator/component/substitution/reduction/integral chains and shared prose.

Observed-family endpoint sampler chooses from reduced rationals n/d, d in{1,2,3}, between0 and6 plus sqrt2 and sqrt3. Intervals are increasing and nonnegative; amplitudes are nonzero integer ±1..6. Cubic completion uses lower∈{-2,-3/2,-1,-1/2}, upper∈{1,3/2,2,5/2,3}. Helix bounds are distinct pi/12 multiples from0 throughpi/2. Workload guards apply identically to explicit calls and sampling. Hard limits are in classification.md. Endpoint choices alter the assessed integral bounds and traversal segment; amplitude affects f and answers. Fingerprints use the actual mathematical curve/scalar/interval, excluding seed, bank, profile and notation aliases.

### Source findings and minimal supported repairs

* q-40253's wrong option sqrt2 integral t sqrt(2t²-1)dt is non-real for0≤t<1/sqrt2. Its correct option4 integral t sqrt(4t²+1)dt is sound. Original bank is preserved public and ineligible, not silently rewritten.
* q-76356's wrong option2 integral t²sqrt(t²-t)dt is non-real for0<t<1. The keyed2sqrt3 integral t³dt is sound. Its prose states t>0 on[0,2]; raw retains that phrase, while normal minimally uses t≥0 to justify |t|=t at the endpoint too.
* q-76368 has no rating, correct key or solution. Its captured first option is a text answer with dollar delimiters and a period, preserved raw/completed-source; no conversion is claimed faithful. Mathematical derivation: r′=(2,-1), speed=sqrt5, x³-y=8t³+t-2. The supported completion is explicitly authored, and malformed int_(C) spelling becomes int_C only in normal presentation.

No ambiguous equal-valued complete source banks were identified by the mathematical readback; nonreal historical members are reported separately. Historical intent remains unresolved, not disguised as recovered explanation. Exact raw fidelity counts include30 options,6 banks,6 prompts,5 available solutions and5 available correct designations. Missing metadata is not a denominator success.
