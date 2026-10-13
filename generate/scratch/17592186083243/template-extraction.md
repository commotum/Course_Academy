# Template extraction

Snapshot provenance: math / basis 1356 / lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1.

## Stage 1 — specific original descriptions

### q-20991

For the parametric curve 

$$
x=\frac{1}{2\sqrt{t}},\,y=\frac{{e}^{t}}{2t},\,-\infty <t<\infty ,
$$

calculate the slope of the tangent to the curve at the point where $t=5.$

Original parameters: `{"a": 2, "b": 2, "u": 5}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=1/(a√t), y=eᵗ/(bt): negative half-power and quotient derivatives; cancel t powers and evaluate exponential/root.

Field `selection`, `:answer-field.type/radio`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$-\,\frac{8{e}^{5}}{\sqrt{5}}$`. Plot role: none.

### q-6808

![](images/17/1739317bf1b1c567f74dccf5b24a1b1dde8eb101d20ceec9652f604dc6f84543.png)

For the parametric curve 

$$
x=4\operatorname{cos}⁡t,\,y=3\operatorname{sin}⁡2t,\,0\le t<2\pi ,
$$

shown above, calculate the slope of the tangent to the curve at the point where $t=\frac{\pi }{6}.$

Original parameters: `{"a": 4, "b": 3, "n": 2, "u": "pi/6"}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=a cos(t), y=b sin(nt), n=2 or 3: retain frequency from chain rule; evaluate different exact angles.

Field `selection`, `:answer-field.type/radio`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$-\,\frac{3}{2}$`. Plot role: blue parametric curve on grid before the prompt.

### q-102922

For the parametric curve 

$$
x=\operatorname{sin}⁡2t,\,y={sin}^{2}⁡t,\,0\le t<2\pi ,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi }{12}.$

Original parameters: `{"a": 1, "b": 1, "u": "pi/12"}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=a sin(2t), y=b sin²(t): power/chain derivatives, double-angle identity, half-tangent evaluation.

Field `selection`, `:answer-field.type/radio`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$\frac{\sqrt{3}}{6}$`. Plot role: none.

### q-102940

For the parametric curve 

$$
x=2{t}^{2}+3,\,y=3{t}^{5}+{t}^{3},\,0\le t<\infty ,
$$

calculate the slope of the tangent to the curve at the point where $t=1.$

Original parameters: `{"a": 2, "b": 3, "c": 3, "u": 1}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=a t²+c, y=b t⁵+t³: two power-rule terms, factor a quadratic in t², cancel t, evaluate.

Field `selection`, `:answer-field.type/radio`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$\frac{9}{2}$`. Plot role: none.

### q-102941

For the parametric curve 

$$
x=4\operatorname{sin}⁡t,\,y=\frac{4}{\pi }{t}^{2},\,0\le t<2\pi ,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi }{4}.$

Original parameters: `{"a": 4, "b": 4, "u": "pi/4"}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=a sin(t), y=(b/π)t²: basic trig and power derivatives, secant quotient, exact angle and π cancellation.

Field `selection`, `:answer-field.type/radio`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$\frac{\sqrt{2}}{2}$`. Plot role: none.

### q-15457

For the parametric curve 

$$
x=\operatorname{sin}⁡(2t),\,y={cos}^{2}⁡(t),\,0\le t<2\pi ,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi }{6}.$

Original parameters: `{"a": 1, "b": 1, "u": "pi/6"}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=a sin(2t), y=b cos²(t): negative power/chain derivative, double-angle identity, half-tangent evaluation.

Field `selection`, `:answer-field.type/radio`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$-\,\frac{\sqrt{3}}{2}$`. Plot role: none.

### q-15475

For the parametric curve 

$$
x={e}^{1/t},\,y=\frac{1}{\sqrt{{t}^{2}-1}},\,1<t<\infty ,
$$

calculate the slope of the tangent to the curve at the point where $t=2.$

Original parameters: `{"a": 1, "b": 1, "c": -1, "u": 2}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=e^(a/t), y=b/√(t²+c): two chain derivatives, cancel negative signs, evaluate fractional exponent and root powers.

Field `selection`, `:answer-field.type/radio`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$\frac{8}{\sqrt{27e}}$`. Plot role: none.

### q-15476

For the parametric curve 

$$
x=\sqrt{\operatorname{sin}⁡({e}^{t})},\,y=\operatorname{cot}⁡({e}^{t}),\,-\infty <t<1,
$$

calculate the slope of the tangent to the curve at the point where $t=\operatorname{ln}⁡(\frac{\pi }{6}).$

Original parameters: `{"a": 1, "b": 1, "u": "log(pi/6)"}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=a√sin(eᵗ), y=b cot(eᵗ): nested root/trig/exponential chains; cancel common eᵗ and evaluate e^(ln θ).

Field `selection`, `:answer-field.type/radio`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$-8\sqrt{\frac{2}{3}}$`. Plot role: none.

### q-348303

![](images/59/59f053b9a122018d78cd9c30f5a53cd67cd2ff645d02ccb6d311e6183e081102.png)

For the parametric curve 

$$
x={t}^{3}+2{t}^{2},\,y={t}^{2},\,-\infty <t<\infty ,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=2.$ Do not round the answer.

$m=$
{{field-1}}

Original parameters: `{"a": 2, "b": 1, "u": 2}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=t³+a t², y=b t²: polynomial derivatives, cancellation of a common t, rational slope.

Field `field-1`, `:answer-field.type/blank`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$\frac{1}{5}$`. Plot role: blue parametric curve on grid before the prompt.

### q-348304

![](images/7a/7ae65c873838ede4cce89c953ff2654fa1e58e65fdc87896c8ba85bbf947be20.png)

For the parametric curve 

$$
x=6\operatorname{cos}⁡t,\,y=2\operatorname{sin}⁡3t,\,0\le t<2\pi ,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=\frac{\pi }{4}.$ Do not round the answer.

$m=$
{{field-1}}

Original parameters: `{"a": 6, "b": 2, "n": 3, "u": "pi/4"}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=a cos(t), y=b sin(nt), n=2 or 3: retain frequency from chain rule; evaluate different exact angles.

Field `field-1`, `:answer-field.type/blank`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$1$`. Plot role: blue parametric curve on grid before the prompt.

### q-353350

![](images/ab/abab926e465522d30b236577bf8a1654502807b864c9fed8a4cebb84efffd3a2.png)

For the parametric curve 

$$
x=2\operatorname{sin}⁡t,\,y=3\operatorname{cos}⁡t,\,0\le t<2\pi ,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=\frac{\pi }{4}.$ Do not round the answer.

$m=$ 
{{field-1}}

Original parameters: `{"a": 2, "b": 3, "u": "pi/4"}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=a sin(t), y=b cos(t): basic derivatives and signed scaled tangent at a standard angle.

Field `field-1`, `:answer-field.type/blank`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$-\frac{3}{2}$`. Plot role: blue parametric curve on grid before the prompt.

### q-353351

![](images/35/35c62ccf48c4d0a49729da04b443cb94d112e673e0c24e7784d22f48eaabf8f7.png)

For the parametric curve 

$$
x=3\operatorname{cos}⁡t,\,y=4\operatorname{sin}⁡2t,\,0\le t<2\pi ,
$$

shown above, calculate the slope $m$ of the tangent to the curve at the point where $t=\frac{\pi }{3}.$ Do not round the answer.

$m=$ 
{{field-1}}

Original parameters: `{"a": 3, "b": 4, "n": 2, "u": "pi/3"}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=a cos(t), y=b sin(nt), n=2 or 3: retain frequency from chain rule; evaluate different exact angles.

Field `field-1`, `:answer-field.type/blank`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$\frac{8\sqrt{3}}{9}$`. Plot role: blue parametric curve on grid before the prompt.

### q-363490

For the parametric curve 

$$
x={e}^{3/t},\,y=\frac{1}{\sqrt{{t}^{2}+4}},\,0<t<\infty ,
$$

calculate the slope $m$ of the tangent to the curve at the point where $t=1.$ Do not round the answer.

$m=$ 
{{field-1}}

Original parameters: `{"a": 3, "b": 1, "c": 4, "u": 1}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=e^(a/t), y=b/√(t²+c): two chain derivatives, cancel negative signs, evaluate fractional exponent and root powers.

Field `field-1`, `:answer-field.type/blank`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$\frac{\sqrt{5}}{75{e}^{3}}$`. Plot role: none.

### q-348305

For the parametric curve 

$$
x=\frac{1}{3\sqrt{t}},\,y=\frac{{e}^{t}}{3t},\,-\infty <t<\infty ,
$$

calculate the slope $m$ of the tangent to the curve at the point where $t=4.$ Do not round the answer.

$m=$
{{field-1}}

Original parameters: `{"a": 3, "b": 3, "u": 4}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=1/(a√t), y=eᵗ/(bt): negative half-power and quotient derivatives; cancel t powers and evaluate exponential/root.

Field `field-1`, `:answer-field.type/blank`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$-3{e}^{4}$`. Plot role: none.

### q-353363

For the parametric curve 

$$
x={e}^{2/t},\,y=\frac{1}{\sqrt{{t}^{2}+1}},\,0<t<\infty ,
$$

calculate the slope $m$ of the tangent to the curve at the point where $t=1.$ Do not round the answer.

$m=$ 
{{field-1}}

Original parameters: `{"a": 2, "b": 1, "c": 1, "u": 1}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=e^(a/t), y=b/√(t²+c): two chain derivatives, cancel negative signs, evaluate fractional exponent and root powers.

Field `field-1`, `:answer-field.type/blank`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$\frac{\sqrt{2}}{8{e}^{2}}$`. Plot role: none.

### q-6730

![](images/94/9434dda63c08fc1202d16ab5410fe7061050515876ffa473d8720db39079af3e.png)

For the parametric curve 

$$
x={t}^{3}+{t}^{2},\,y={t}^{2},\,-\infty <t<\infty ,
$$

shown above, calculate the slope of the tangent to the curve at the point where $t=2.$

Original parameters: `{"a": 1, "b": 1, "u": 2}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=t³+a t², y=b t²: polynomial derivatives, cancellation of a common t, rational slope.

Field `selection`, `:answer-field.type/radio`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$\frac{1}{4}$`. Plot role: blue parametric curve on grid before the prompt.

### q-15465

For the parametric curve 

$$
x=t+\operatorname{sin}⁡t,\,y=t+\operatorname{cos}⁡t,\,0\le t<2\pi ,
$$

calculate the slope of the tangent to the curve at the point where $t=\frac{\pi }{2}.$

Original parameters: `{"a": 1, "b": 1, "u": "pi/2"}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=a t+sin(t), y=b t+cos(t): additive linear/trig derivatives; evaluate exact sine/cosine values.

Field `selection`, `:answer-field.type/radio`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$0$`. Plot role: none.

### q-15469

For the parametric curve 

$$
x=2{t}^{3}+1,\,y={t}^{4}+2{t}^{2},\,0\le t<\infty ,
$$

calculate the slope of the tangent to the curve at the point where $t=1.$

Original parameters: `{"a": 2, "b": 1, "c": 2, "u": 1}`. Exact input numbers are integers, rational multiples of π, or ln(π/6). Required slope is an exact rational, radical or exponential/radical value, with sign preserved. x=a t³+1, y=b t⁴+c t²: two power-rule terms, factor/cancel t; rational slope.

Field `selection`, `:answer-field.type/radio`; expected fragment contains only the slope (not `m=` or a tangent equation). Original correct value: `$\frac{4}{3}$`. Plot role: none.

## Stage 2 — shared patterns

All questions supply t explicitly, differentiate both coordinate functions, form the quotient y′/x′, simplify, substitute the given t, and return one exact finite slope. They do not require recovering t from a coordinate point. Same parameters at different supplied t remain separate math instances.

- **double_sin**: x=a sin(2t), y=b sin²(t): power/chain derivatives, double-angle identity, half-tangent evaluation.

- **double_cos**: x=a sin(2t), y=b cos²(t): negative power/chain derivative, double-angle identity, half-tangent evaluation.

- **poly5**: x=a t²+c, y=b t⁵+t³: two power-rule terms, factor a quadratic in t², cancel t, evaluate.

- **trig_poly**: x=a sin(t), y=(b/π)t²: basic trig and power derivatives, secant quotient, exact angle and π cancellation.

- **cubic**: x=t³+a t², y=b t²: polynomial derivatives, cancellation of a common t, rational slope.

- **linear_trig**: x=a t+sin(t), y=b t+cos(t): additive linear/trig derivatives; evaluate exact sine/cosine values.

- **poly4**: x=a t³+1, y=b t⁴+c t²: two power-rule terms, factor/cancel t; rational slope.

- **harmonic**: x=a cos(t), y=b sin(nt), n=2 or 3: retain frequency from chain rule; evaluate different exact angles.

- **ellipse**: x=a sin(t), y=b cos(t): basic derivatives and signed scaled tangent at a standard angle.

- **exp_root**: x=1/(a√t), y=eᵗ/(bt): negative half-power and quotient derivatives; cancel t powers and evaluate exponential/root.

- **reciprocal_exp_root**: x=e^(a/t), y=b/√(t²+c): two chain derivatives, cancel negative signs, evaluate fractional exponent and root powers.

- **nested_trig**: x=a√sin(eᵗ), y=b cot(eᵗ): nested root/trig/exponential chains; cancel common eᵗ and evaluate e^(ln θ).

## Stage 3 — every original choice and its complete bank

Each table maps one original field/choice to an explicit normal-generator expression recipe at the source parameters. Formula implementations are in `bank` in the sibling script. Scalar evidence alone underdetermines error intent. “Empirical” means expression-pattern preservation, not a recovered diagnosis; these banks are offered only through explicit observed profiles.

### q-20991 / observed_q-20991

Parameters: `{"a": 2, "b": 2, "u": 5}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| selection | `$\frac{8{e}^{5}}{\sqrt{3}}$` | False | alter sign and radical | `$\frac{8 \sqrt{3} e^{5}}{3}$` |

| selection | `$-\,\frac{5{e}^{4}}{\sqrt{6}}$` | False | alter factors and exponential | `$- \frac{5 \sqrt{6} e^{4}}{6}$` |

| selection | `$-\,\frac{4{e}^{5}}{\sqrt{2}}$` | False | alter factor and radical | `$- 2 \sqrt{2} e^{5}$` |

| selection | `$\frac{{e}^{3}}{\sqrt{5}}$` | False | alter factors exponent and sign | `$\frac{\sqrt{5} e^{3}}{5}$` |

| selection | `$-\,\frac{8{e}^{5}}{\sqrt{5}}$` | True | correct | `$- \frac{8 \sqrt{5} e^{5}}{5}$` |

### q-6808 / observed_q-6808

Parameters: `{"a": 4, "b": 3, "n": 2, "u": "pi/6"}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| selection | `$-\,\frac{1}{\sqrt{2}}$` | False | empirical sqrt2 scaled | `$- \frac{\sqrt{2}}{2}$` |

| selection | `$-\,\frac{2}{3}$` | False | coefficient reciprocal sign | `$- \frac{2}{3}$` |

| selection | `$-\,\frac{1}{2}$` | False | alter coefficient/frequency | `$- \frac{1}{2}$` |

| selection | `$-\,\frac{3}{\sqrt{2}}$` | False | empirical scale sqrt2 | `$- \frac{3 \sqrt{2}}{2}$` |

| selection | `$-\,\frac{3}{2}$` | True | correct | `$- \frac{3}{2}$` |

### q-102922 / observed_q-102922

Parameters: `{"a": 1, "b": 1, "u": "pi/12"}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| selection | `$\frac{\sqrt{3}}{6}$` | True | correct | `$\frac{\sqrt{3}}{6}$` |

| selection | `$-\frac{\sqrt{3}}{2}$` | False | empirical -3m | `$- \frac{\sqrt{3}}{2}$` |

| selection | `$\sqrt{3}$` | False | empirical 6m | `$\sqrt{3}$` |

| selection | `$-\frac{\sqrt{3}}{6}$` | False | sign reversal | `$- \frac{\sqrt{3}}{6}$` |

| selection | `$\frac{\sqrt{3}}{2}$` | False | empirical 3m | `$\frac{\sqrt{3}}{2}$` |

### q-102940 / observed_q-102940

Parameters: `{"a": 2, "b": 3, "c": 3, "u": 1}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| selection | `$\frac{11}{4}$` | False | alter derivative powers | `$\frac{11}{4}$` |

| selection | `$\frac{15}{4}$` | False | omit cubic derivative | `$\frac{15}{4}$` |

| selection | `$\frac{11}{2}$` | False | compound scale error | `$\frac{11}{2}$` |

| selection | `$\frac{9}{2}$` | True | correct | `$\frac{9}{2}$` |

| selection | `$\frac{3}{2}$` | False | omit fifth derivative | `$\frac{3}{2}$` |

### q-102941 / observed_q-102941

Parameters: `{"a": 4, "b": 4, "u": "pi/4"}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| selection | `$\frac{\sqrt{2}}{2}$` | True | correct | `$\frac{\sqrt{2}}{2}$` |

| selection | `$2\sqrt{2}$` | False | empirical 4m | `$2 \sqrt{2}$` |

| selection | `$\sqrt{2}$` | False | omit factor cancellation | `$\sqrt{2}$` |

| selection | `$\frac{1}{2}$` | False | omit sec | `$\frac{1}{2}$` |

| selection | `$2$` | False | omit sec and double | `$2$` |

### q-15457 / observed_q-15457

Parameters: `{"a": 1, "b": 1, "u": "pi/6"}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| selection | `$\sqrt{3}$` | False | empirical -2m | `$\sqrt{3}$` |

| selection | `$-\,\frac{1}{2}$` | False | omit tan | `$- \frac{1}{2}$` |

| selection | `$-\,\frac{\sqrt{3}}{2}$` | True | correct | `$- \frac{\sqrt{3}}{2}$` |

| selection | `$-\,\sqrt{3}$` | False | omit half factor | `$- \sqrt{3}$` |

| selection | `$\frac{1}{2}$` | False | omit tan and sign | `$\frac{1}{2}$` |

### q-15475 / observed_q-15475

Parameters: `{"a": 1, "b": 1, "c": -1, "u": 2}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| selection | `$\frac{8}{\sqrt{27e}}$` | True | correct | `$\frac{8 \sqrt{3}}{9 e^{\frac{1}{2}}}$` |

| selection | `$\sqrt{\frac{8e}{27}}$` | False | compound root/exponential error | `$\frac{2 \sqrt{6} e^{\frac{1}{2}}}{9}$` |

| selection | `$\frac{\sqrt{9e}}{4}$` | False | alter power and exponent | `$\frac{3 e^{\frac{1}{2}}}{4}$` |

| selection | `$\frac{4}{\sqrt{9e}}$` | False | alter powers | `$\frac{4}{3 e^{\frac{1}{2}}}$` |

| selection | `$\sqrt{\frac{9}{8e}}$` | False | compound reciprocal-root error | `$\frac{3 \sqrt{2}}{4 e^{\frac{1}{2}}}$` |

### q-15476 / observed_q-15476

Parameters: `{"a": 1, "b": 1, "u": "log(pi/6)"}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| selection | `$-8\sqrt{\frac{2}{3}}$` | True | correct | `$- \frac{8 \sqrt{6}}{3}$` |

| selection | `$-2\sqrt{\frac{2}{3}}$` | False | empirical quarter slope | `$- \frac{2 \sqrt{6}}{3}$` |

| selection | `$-\,\frac{1}{\sqrt{6}}$` | False | empirical root/cosine expression | `$- \frac{\sqrt{6}}{6}$` |

| selection | `$-4\sqrt{\frac{3}{2}}$` | False | empirical cosine-squared factor | `$- 2 \sqrt{6}$` |

| selection | `$-2\sqrt{\frac{3}{2}}$` | False | empirical half cosine-squared factor | `$- \sqrt{6}$` |

### q-348303 / blank

Parameters: `{"a": 2, "b": 1, "u": 2}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| field-1 | `$\frac{1}{5}$` | True | correct slope fragment | `$\frac{1}{5}$` |

### q-348304 / blank

Parameters: `{"a": 6, "b": 2, "n": 3, "u": "pi/4"}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| field-1 | `$1$` | True | correct slope fragment | `$1$` |

### q-353350 / blank

Parameters: `{"a": 2, "b": 3, "u": "pi/4"}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| field-1 | `$-\frac{3}{2}$` | True | correct slope fragment | `$- \frac{3}{2}$` |

### q-353351 / blank

Parameters: `{"a": 3, "b": 4, "n": 2, "u": "pi/3"}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| field-1 | `$\frac{8\sqrt{3}}{9}$` | True | correct slope fragment | `$\frac{8 \sqrt{3}}{9}$` |

### q-363490 / blank

Parameters: `{"a": 3, "b": 1, "c": 4, "u": 1}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| field-1 | `$\frac{\sqrt{5}}{75{e}^{3}}$` | True | correct slope fragment | `$\frac{\sqrt{5}}{75 e^{3}}$` |

### q-348305 / blank

Parameters: `{"a": 3, "b": 3, "u": 4}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| field-1 | `$-3{e}^{4}$` | True | correct slope fragment | `$- 3 e^{4}$` |

### q-353363 / blank

Parameters: `{"a": 2, "b": 1, "c": 1, "u": 1}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| field-1 | `$\frac{\sqrt{2}}{8{e}^{2}}$` | True | correct slope fragment | `$\frac{\sqrt{2}}{8 e^{2}}$` |

### q-6730 / observed_q-6730

Parameters: `{"a": 1, "b": 1, "u": 2}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| selection | `$\frac{1}{2}$` | False | empirical double | `$\frac{1}{2}$` |

| selection | `$\frac{1}{4}$` | True | correct | `$\frac{1}{4}$` |

| selection | `$\frac{1}{6}$` | False | omit quadratic derivative and y factor | `$\frac{1}{6}$` |

| selection | `$\frac{1}{5}$` | False | empirical denominator shift | `$\frac{1}{5}$` |

| selection | `$\frac{1}{3}$` | False | omit quadratic derivative | `$\frac{1}{3}$` |

### q-15465 / observed_q-15465

Parameters: `{"a": 1, "b": 1, "u": "pi/2"}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| selection | `$\sqrt{2}$` | False | empirical sqrt2 scale | `$\sqrt{2}$` |

| selection | `$\frac{1}{2}$` | False | empirical half scale | `$\frac{1}{2}$` |

| selection | `$1$` | False | linear coefficient ratio | `$1$` |

| selection | `$\frac{1}{\sqrt{2}}$` | False | empirical reciprocal sqrt2 | `$\frac{\sqrt{2}}{2}$` |

| selection | `$0$` | True | correct | `$0$` |

### q-15469 / observed_q-15469

Parameters: `{"a": 2, "b": 1, "c": 2, "u": 1}`.

| Source field | Complete source value | Correct? | Parameterized recipe / pattern | Generated exact value |

|---|---|---|---|---|

| selection | `$\frac{2}{3}$` | False | omit y factor | `$\frac{2}{3}$` |

| selection | `$\frac{8}{3}$` | False | extra y factor | `$\frac{8}{3}$` |

| selection | `$\frac{4}{3}$` | True | correct | `$\frac{4}{3}$` |

| selection | `$\frac{3}{4}$` | False | reciprocal | `$\frac{3}{4}$` |

| selection | `$\frac{3}{2}$` | False | double reciprocal | `$\frac{3}{2}$` |

## Stage 4 — reusable Markdown/value templates

There are 16 observed field/value templates. Different numbers within a template do not count as another template. Blank harmonic n=2/n=3 cases share one layout; reciprocal exponential/root blanks with c=1/c=4 share another. Radio/blank prompt endings and field fragments remain distinct.

Fixed source wording: “For the parametric curve”; “shown above” iff plotted; “calculate the slope … of the tangent to the curve at the point where t=…”; blank source replay (API profile="observed") adds “Do not round the answer.” and `$m=$ {{field-1}}`. Normal blanks use “Give an exact answer.” as a minimal native-grading compatibility repair: the current grader treats any “round” substring as requiring normalized identical form, so even “Do not round” rejects a valid unreduced derivative quotient. The exact mathematical demand, field fragment, level and fixed solution are unchanged. Original-wording rejection evidence is separate from accepted algebraically equivalent normal entries. Worked solution retains “We will use the formula”, “Differentiating x and y, we get”, “So we have” (radio) / “So, we have” (blank), then “Therefore, when …”. Exactly one fixed worked solution is independent of option selection.

Variable components are x(t), y(t), interval, t₀, derivative factors, unreduced derivative quotient, simplified ratio, substitution, special-angle or exact numerator/denominator evaluation, final slope, and complete bank. Optional plots depend on the same curve parameters. Standard LaTeX and algebraically equivalent factorization normalize mathematical blocks; source text/math evidence remains in source.json and review.md. Exact raw source strings are reported separately from mathematical bank fidelity.

Sampling policies (authored, not recovered code): positive small coordinate coefficients a,b∈1..6; polynomial shifts −4..6; low positive secondary coefficients; integer t values of magnitude 1..4 (cubic includes signed t); standard exact trig angles within the original [0,2π) interval (linear/trig: π/2 or 3π/2; trig/polynomial: odd multiples of π/4; harmonic/ellipse: common multiples of π/6, π/4, π/3); harmonic n∈{2,3}; hard exponential/root t in 2..6; reciprocal-root c∈{−1,1,2,3,4} with positive radicand; nested eᵗ is π/6 or 5π/6, below e, preserving sin(eᵗ)=1/2 and the original half-power workload. All source parameters remain accepted with explicit replay profiles. Scope stays at the same derivative method and algebra size. There is no within-level progression.

Validation constraints: supplied parameter in displayed interval, both coordinate values real, x′(t₀)≠0, slope finite, and all required bank options real, finite, pairwise inequivalent, with exactly one correct. Choose the complete bank before sampling and reject the entire instance on any failure. Explicit parameter input fails rather than silently resampling. No coordinate-point ambiguity arises because t₀ is supplied.

Authored normal banks: slope; reversed derivative sign; reversed derivative ratio; omit division by x′; use y/x. The linear/trig template instead uses reverse cosine derivative sign, omit cosine derivative, leave y undifferentiated, and evaluate at half the supplied parameter, which supports the observed zero slope without a reciprocal-zero option. These are complete authored banks, never claims about original author intent. Instance eligibility rejects any collisions (including zero slopes for banks whose sign-reversal options collide).

Source correction: q-20991 and q-348305 have x=1/(a√t), y=eᵗ/(at) yet −∞<t<∞. √t must be real and nonzero, so t>0. Evaluated source slopes remain correct and all source options replay. The generated interval alone is corrected.
