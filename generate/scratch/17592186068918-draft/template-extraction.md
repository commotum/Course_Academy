# Template extraction

## Stage 1: individual observations

Each original record below is reproduced with all captured attribute omissions. Source prompts contain radians and no figures. q-10046 has exactly the familiar secant values 1 and sqrt(2); q-49557 has numerator 2, independent variable y and a bare indefinite integral. Rated originals use x except q-73674 (y with y²); constants C and K are preserved. The exact per-source prompt, full choices, key status and formal solution stages follow.

### q-10046

Evaluate the integral
$\displaystyle \int_{0}^{π/4}\frac{\sec x\tan x}{1 + \sec x}dx$.

| Original value | Designation | Parameterized expression pattern |
|---|---|---|
| $1 + \sqrt{2} - \ln 2$ | key absent | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\ln (1 + \sqrt{2}) - \ln 2$ | key absent | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\ln (1 + \sqrt{2}) + \ln 2$ | key absent | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\ln (1 - \sqrt{2}) + \ln 2$ | key absent | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\ln (1 - \sqrt{2}) - \ln 2$ | key absent | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |

No original worked solution, difficulty or correct designation is captured. Normal completion is separately authored.

### q-49557

What is $\displaystyle \int\frac{2\cos y}{\sin y}dy$?

| Original value | Designation | Parameterized expression pattern |
|---|---|---|
| $\ln \mid \cos y \mid + C$ | key absent | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\ln \mid \sin y \mid + C$ | key absent | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $2\ln \mid \cos y \mid + C$ | key absent | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\ln \mid \cos 2y \mid + C$ | key absent | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $2\ln \mid \sin y \mid + C$ | key absent | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |

No original worked solution, difficulty or correct designation is captured. Normal completion is separately authored.

### q-10045

${\int }_{-1}^{1}\frac{\operatorname{cos}⁡x}{1+\operatorname{sin}⁡x}\,\text{d}x=$

| Original value | Designation | Parameterized expression pattern |
|---|---|---|
| $\operatorname{ln}⁡(2+\operatorname{sin}⁡(1))+\operatorname{ln}⁡(2-\operatorname{sin}⁡(1))$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\operatorname{ln}⁡(1-\operatorname{sin}⁡(2))-\operatorname{ln}⁡(1+\operatorname{sin}⁡(2))$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\operatorname{ln}⁡(2-\operatorname{sin}⁡(1))+\operatorname{ln}⁡(2+\operatorname{sin}⁡(1))$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\operatorname{ln}⁡(1+\operatorname{sin}⁡(1))-\operatorname{ln}⁡(1-\operatorname{sin}⁡(1))$ | correct | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $-\operatorname{ln}⁡(1+\operatorname{sin}⁡(2))-\operatorname{ln}⁡(1-\operatorname{sin}⁡(2))$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |

Notice that the numerator is proportional to the derivative of the denominator, because

$$
\frac{\text{d}}{\text{d}x}(1+\operatorname{sin}⁡x)=\operatorname{cos}⁡x.
$$

So, let $u=1+\operatorname{sin}⁡x.$ Differentiating, we have 

$$
\frac{\text{d}u}{\text{d}x}=\operatorname{cos}⁡x\,⟹\,\text{d}u=\operatorname{cos}⁡x\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $-1$ | $1$ |
| --- | --- | --- |
| $u$ | $1-\operatorname{sin}⁡(1)$ | $1+\operatorname{sin}⁡(1)$ |

We now substitute and evaluate, as follows:

$$
\begin{aligned}{\int }_{-1}^{1}\frac{\operatorname{cos}⁡x}{1+\operatorname{sin}⁡x}\,\text{d}x & ={\int }_{-1}^{1}\frac{1}{1+\operatorname{sin}⁡x}\cdot \operatorname{cos}⁡x\,\text{d}x \\  & ={\int }_{1-\operatorname{sin}⁡(1)}^{1+\operatorname{sin}⁡(1)}\frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|{|}_{1-\operatorname{sin}⁡(1)}^{1+\operatorname{sin}⁡(1)} \\  & =\operatorname{ln}⁡(1+\operatorname{sin}⁡(1))-\operatorname{ln}⁡(1-\operatorname{sin}⁡(1))\end{aligned}
$$

### q-113998

Calculate $\int \frac{2\operatorname{csc}⁡x\operatorname{cot}⁡x}{\operatorname{csc}⁡x+2}\,\text{d}x.$

| Original value | Designation | Parameterized expression pattern |
|---|---|---|
| $\operatorname{ln}⁡|\operatorname{csc}⁡x|+C$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $-2\operatorname{ln}⁡|\operatorname{csc}⁡x|+C$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $2\operatorname{ln}⁡|\operatorname{csc}⁡x+2|+C$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\operatorname{ln}⁡|\operatorname{csc}⁡x+2|+C$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $-2\operatorname{ln}⁡|\operatorname{csc}⁡x+2|+C$ | correct | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |

Let $u=\operatorname{csc}⁡x+2.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=-\operatorname{csc}⁡x\operatorname{cot}⁡x\,⟹\,-\text{d}u=\operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{2\operatorname{csc}⁡x\operatorname{cot}⁡x}{\operatorname{csc}⁡x+2}\,\text{d}x & =2\int \frac{1}{\operatorname{csc}⁡x+2}\cdot \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & =2\int \frac{1}{u}\cdot (-\text{d}u) \\  & =-2\int \frac{1}{u}\,\text{d}u \\  & =-2\operatorname{ln}⁡|u|+C \\  & =-2\operatorname{ln}⁡|\operatorname{csc}⁡x+2|+C\end{aligned}
$$

### q-350887

Evaluate the following integral. Do not round the answer.

${\int }_{0}^{\pi /2}\frac{2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)}{{sin}^{2}⁡(x)+3}\,\text{d}x=$
{{field-1}}

| Original value | Designation | Parameterized expression pattern |
|---|---|---|
| $\operatorname{ln}(\frac{4}{3})$ | correct | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |

If we let $u={sin}^{2}⁡(x)+3,$ then

$$
\frac{\text{d}u}{\text{d}x}=2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)\,⟹\,\text{d}u=2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $0$ | $\pi /2$ |
| --- | --- | --- |
| $u$ | $3$ | $4$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{0}^{\pi /2}\frac{2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)}{{sin}^{2}⁡(x)+3}\,\text{d}x & ={\int }_{0}^{\pi /2}\frac{1}{{sin}^{2}⁡(x)+3}\cdot 2\operatorname{sin}⁡(x)\operatorname{cos}⁡(x)\,\text{d}x \\  & ={\int }_{3}^{4}\frac{1}{u}\,\text{d}u \\  & =\operatorname{ln}⁡|u|\,{|}_{3}^{4} \\  & =\operatorname{ln}⁡4-\operatorname{ln}⁡3 \\  & =\operatorname{ln}⁡(\frac{4}{3})\end{aligned}
$$

### q-350901

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /3}^{\pi /2}\frac{24\operatorname{sin}⁡(x){cos}^{2}⁡(x)}{8{cos}^{3}⁡(x)+5}\,\text{d}x=$
{{field-1}}

| Original value | Designation | Parameterized expression pattern |
|---|---|---|
| $\operatorname{ln}(\frac{6}{5})$ | correct | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |

If we let $u=8{cos}^{3}⁡(x)+5,$ then

$$
\frac{\text{d}}{\text{d}x}(8{cos}^{3}⁡(x)+5)=-24{cos}^{2}⁡(x)\operatorname{sin}⁡(x).
$$

So, differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}=-24{cos}^{2}⁡(x)\operatorname{sin}⁡(x)\,⟹\,-\text{d}u=24\operatorname{sin}⁡(x){cos}^{2}⁡(x)\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $\pi /3$ | $\pi /2$ |
| --- | --- | --- |
| $u$ | $6$ | $5$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{\pi /3}^{\pi /2}\frac{24\operatorname{sin}⁡(x){cos}^{2}⁡(x)}{8{cos}^{3}⁡(x)+5}\,\text{d}x & ={\int }_{\pi /3}^{\pi /2}\frac{1}{8{cos}^{3}⁡(x)+5}\cdot 24\operatorname{sin}⁡(x){cos}^{2}⁡(x)\,\text{d}x \\  & ={\int }_{6}^{5}\frac{1}{u}\cdot (-\text{d}u) \\  & =-{\int }_{6}^{5}\frac{1}{u}\,\text{d}u \\  & =-\operatorname{ln}⁡|u|{|}_{6}^{5} \\  & =-(\operatorname{ln}⁡5-\operatorname{ln}⁡6) \\  & =\operatorname{ln}⁡(\frac{6}{5})\end{aligned}
$$

### q-350904

Evaluate the following integral. Do not round the answer.

${\int }_{\pi /6}^{\pi /2}\frac{\operatorname{csc}⁡(x)\operatorname{cot}⁡(x)}{2+\operatorname{csc}⁡(x)}\,\text{d}x=$
{{field-1}}

| Original value | Designation | Parameterized expression pattern |
|---|---|---|
| $\operatorname{ln}(\frac{4}{3})$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\ln\left(\frac{4}{3}\right)$ | correct | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |

If we let $u=2+\operatorname{csc}⁡(x),$ then

$$
\frac{\text{d}u}{\text{d}x}=-\operatorname{csc}⁡(x)\operatorname{cot}⁡(x)\,⟹\,-\text{d}u=\operatorname{csc}⁡(x)\operatorname{cot}⁡(x)\,\text{d}x.
$$

Calculating the limits for $u$ gives

| $x$ | $\pi /6$ | $\pi /2$ |
| --- | --- | --- |
| $u$ | $4$ | $3$ |

Using the above, we can rewrite the integral in terms of $u$ and evaluate:

$$
\begin{aligned}{\int }_{\pi /6}^{\pi /2}\frac{\operatorname{csc}⁡(x)\operatorname{cot}⁡(x)}{2+\operatorname{csc}⁡(x)}\,\text{d}x & ={\int }_{\pi /6}^{\pi /2}\frac{1}{2+\operatorname{csc}⁡(x)}\cdot (\operatorname{csc}⁡(x)\operatorname{cot}⁡(x))\,\text{d}x \\  & ={\int }_{4}^{3}\frac{1}{u}\,(-\text{d}u) \\  & =-{\int }_{4}^{3}\frac{1}{u}\,\text{d}u \\  & =-\operatorname{ln}⁡|u|{|}_{4}^{3} \\  & =-(\operatorname{ln}⁡3-\operatorname{ln}⁡4) \\  & =\operatorname{ln}⁡(\frac{4}{3})\end{aligned}
$$

### q-73674

Calculate the integral $\int \frac{y\operatorname{cos}⁡({y}^{2})}{\operatorname{sin}⁡({y}^{2})}\,\text{d}y.$

| Original value | Designation | Parameterized expression pattern |
|---|---|---|
| $\operatorname{ln}⁡|\operatorname{cos}⁡({y}^{2})|+C$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\frac{1}{2}\operatorname{ln}⁡|\operatorname{cos}⁡({y}^{2})|+C$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\operatorname{ln}⁡|\operatorname{sin}⁡({y}^{2})|+C$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $2\operatorname{ln}⁡|\operatorname{cos}⁡({y}^{2})|+C$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\frac{1}{2}\operatorname{ln}⁡|\operatorname{sin}⁡({y}^{2})|+C$ | correct | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |

Notice that the numerator is proportional to the derivative of the denominator, because

$$
\frac{\text{d}}{\text{d}y}(\operatorname{sin}⁡({y}^{2}))=2y\operatorname{cos}⁡({y}^{2}).
$$

So, let $u=\operatorname{sin}⁡({y}^{2}).$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}y}=2y\operatorname{cos}⁡({y}^{2})\,⟹\,\frac{1}{2}\,\text{d}u=y\operatorname{cos}⁡({y}^{2})\,\text{d}y.
$$

We now substitute and evaluate, as follows:

$$
\begin{aligned}\int \frac{y\operatorname{cos}⁡({y}^{2})}{\operatorname{sin}⁡({y}^{2})}\,\text{d}y & =\int \frac{1}{\operatorname{sin}⁡({y}^{2})}\cdot (y\operatorname{cos}⁡({y}^{2}))\,\text{d}y \\  & =\int \frac{1}{u}\cdot \frac{1}{2}\,\text{d}u \\  & =\frac{1}{2}\int \frac{1}{u}\,\text{d}u \\  & =\frac{1}{2}\operatorname{ln}⁡|u|+C \\  & =\frac{1}{2}\operatorname{ln}⁡|\operatorname{sin}⁡({y}^{2})|+C\end{aligned}
$$

### q-113997

Calculate $\int \frac{{sec}^{2}⁡x\operatorname{tan}⁡x}{\operatorname{tan}⁡x+1}\,\text{d}x.$

| Original value | Designation | Parameterized expression pattern |
|---|---|---|
| $\frac{{tan}^{2}⁡x}{2}-\operatorname{tan}⁡x+K$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\operatorname{tan}⁡x-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|+K$ | correct | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\operatorname{tan}⁡(x-1)-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|+K$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\operatorname{tan}⁡(x+1)-\operatorname{ln}⁡|\operatorname{tan}⁡x|+K$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |
| $\operatorname{tan}⁡x-\operatorname{ln}⁡|\operatorname{tan}⁡x|+K$ | wrong | m times the full displayed value, with C/K kept arbitrary; historical intent unresolved |

Let $u=\operatorname{tan}⁡x+1.$ Differentiating, we have

$$
\frac{\text{d}u}{\text{d}x}={sec}^{2}⁡x\,⟹\,\text{d}u={sec}^{2}⁡x\,\text{d}x.
$$

Using the above, we can write the integral in terms of $u$ and evaluate:

$$
\begin{aligned}\int \frac{{sec}^{2}⁡x\operatorname{tan}⁡x}{\operatorname{tan}⁡x+1}\,\text{d}x & =\int \frac{1}{\operatorname{tan}⁡x+1}\cdot {sec}^{2}⁡x\operatorname{tan}⁡x\,\text{d}x \\  & =\int \frac{1}{\operatorname{tan}⁡x+1}\cdot \operatorname{tan}⁡x\cdot {sec}^{2}⁡x\,\text{d}x \\  & =\int \frac{1}{u}(u-1)\text{d}u \\  & =\int (1-\frac{1}{u})\,\text{d}u \\  & =u-\operatorname{ln}⁡|u|+C \\  & =(\operatorname{tan}⁡x+1)-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|+C \\  & =\operatorname{tan}⁡x-\operatorname{ln}⁡|\operatorname{tan}⁡x+1|+K\end{aligned}
$$

where $K=C+1.$

## Stage 2: shared pattern

Recognize the denominator as u and its derivative as the numerator up to a constant; substitute into 1/u and integrate to ln|u|. The tangent+1 source additionally replaces tan x by u-1 and integrates 1-1/u. Definite sources transform both bounds and evaluate the same primitive at each endpoint in order. The shared instructional purpose is quotient substitution, following the lesson's product substitution skill.

## Stage 3: components and complete bank profiles

The table above maps every option one-to-one, including both q350904 blank aliases, the duplicate wrong sums in q10045 and the two nonreal q10046 logarithms. The profile `observed` (alias `raw`) applies positive amplitude m to every full source expression; this is an expression-pattern transport, not a claim to recover a misconception. Source errors stay in these evidence-only, ineligible public profiles. There is no cross-source pooling. A missing key remains missing. A blank alias is a correct representation, not an incorrect distractor.

The method profile computes the answer independently and uses complete operation banks. Direct sine: logarithm, logarithm of cosine instead, opposite derivative sign, omit reciprocal before integration, and use u^-2 primitive. Shifted sine: logarithm, omitted shift, opposite sign, omitted reciprocal, u^-2 primitive. Cosecant: logarithm, reversed sign, omitted original numerator factor, omitted denominator shift, and u^-2 primitive. Nested-square sine: logarithm, omitted inner derivative 2, reversed sign, cosine instead of sine, and u^-2 primitive. Tangent+1: full u-ln|u|, wrong logarithm sign, omitted u primitive term, omitted shift inside logarithm, and integration after omitting the transformed denominator. Definite radio: correct upper-minus-lower, reversed limits, addition of endpoints, omitted lower, omitted upper. Definite blanks retain the observed response form and have no wrong answers. Every complete bank is verified for pairwise mathematical distinctness; indefinite answers compare derivatives, so additive constants cannot disguise duplicates.

## Stage 4: masks, slots and bounds

The fixed backbone is each source's exact prose and ordered formal rows, including distinct first-derivative blocks, parentheses, factorizations, grouped endpoint differences and the final K=C+1 absorption. The amplitude slot m is a strict built-in integer in 1..12. It multiplies every actual integral operand and every complete primitive/component; it does not change substitution u or bounds. Constants remain arbitrary, and the final prose becomes K=C+m. The renderer's identity case for a multiplier of 1 preserves exact original bytes; the same transformation recipe is used at all amplitudes. It does not return a literal payload based on source parameters. Normal presentation removes the native form-sensitive word 'round' only when the original intention was exactness, and uses the frozen formatter. Those normalized normal records are distinct from public raw evidence.

The added `shifted-sine` family has strict integer k=1..12, a=2..6. These parameters are substantive numerator and denominator slots, with all 60 tasks enumerated. Its fixed stages are u, du, reciprocal separation, substitution with k, factor extraction, primitive and back substitution. The positive shift bounds ensure denominator a+sin x>=1 and avoid zeros; no additional algebra or topic is introduced. Easy direct sine has 12 amplitudes; moderate has these 60 plus 12 separately authored completions of q10046; hard has seven families times 12 amplitudes. Samplers and explicit inputs use this same domain. The family/bank is selected before its parameters in ordinary single-instance sampling. Batch requests exhaust the finite domain and deduplicate mathematical integrand, limits and answer role across profile aliases.

Source banks are all evidence-only because full historical error intent is not known. Normal defaults sample every supported family through the separately method-derived bank. Independent inventory is preserved in `independent-inventory.json`, with the exact wrapper basis/lineage and complete records; it establishes no original MA template or difficulty.

## Domains and anomalies

For indefinite expressions use connected real intervals after removing every denominator zero and every logarithm argument zero. For sine(y²), remove y²=k*pi and, for cosine choices, y²=pi/2+k*pi. For csc x, remove x=k*pi, plus zeros of csc x+2 where applicable. Direct sine/cosine choices remove their zeros. Tangent source banks additionally remove x=pi/2+k*pi, tan x=-1, tan x=0 for the unshifted log choices, and x=pi/2±1+k*pi for historical tan(x∓1) choices. Real logarithms use absolute values in indefinite answers; equivalence is local on each common connected interval. No choices are compared across disconnected branches.

Definite integrands are continuous on their entire closed intervals: 1+sin x>0 on [-1,1]; 1+sec x>=2 on [0,pi/4] with no secant pole; sin²x+3>=3 on [0,pi/2]; 8cos³x+5>=5 on [pi/3,pi/2]; csc x+2>=3 on [pi/6,pi/2] with no cosecant pole. All normal answer log arguments are positive or absolute-valued. The two historical ln(1-sqrt2) choices are not real and remain raw evidence only. q10045 has two equal wrong log sums; both remain raw evidence and the method bank repairs this ambiguity. q10046 and q49557 lack difficulty, correct key and solution; the public raw generator retains all three omissions, while normal completions are explicitly authored. q350904's two blank aliases are legitimate equivalent answers and retained in raw replay.
