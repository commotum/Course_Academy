# Template extraction

## 1. Specific source descriptions

Every source is preserved in source.json; the following preserves full prompt, complete bank and expected fragment.

### q-1907

Differentiate $x^{2}\cos x$.

Original parameters: {"c": 1, "n": 2}

Factors u=x^{2}, v=\cos{\left(x \right)}.

Field selection :answer-field.type/radio

Choice 1: `x^{2}\cos x - x^{2}\sin x`; complete expression recipe - x^{2} \sin{\left(x \right)} + x^{2} \cos{\left(x \right)}.

Choice 2: `2x\cos x - 2x\sin x`; complete expression recipe - 2 x \sin{\left(x \right)} + 2 x \cos{\left(x \right)}.

Choice 3: `2x\cos x - x^{2}\sin x`; complete expression recipe - x^{2} \sin{\left(x \right)} + 2 x \cos{\left(x \right)}.

Choice 4: `x^{2}\cos x - 2x\sin x`; complete expression recipe x^{2} \cos{\left(x \right)} - 2 x \sin{\left(x \right)}.

Choice 5: `2x\cos x + x^{2}\sin x`; complete expression recipe x^{2} \sin{\left(x \right)} + 2 x \cos{\left(x \right)}.

Missing captured solution: authored four-stage solution uses canonical opening and stages.

### q-47965

Differentiate $x^{2}\tan x$.

Original parameters: {"c": 1, "n": 2}

Factors u=x^{2}, v=\tan{\left(x \right)}.

Field selection :answer-field.type/radio

Choice 1: `2x + x^{2}\sec x\tan x`; complete expression recipe x^{2} \tan{\left(x \right)} \sec{\left(x \right)} + 2 x.

Choice 2: `x\tan x(2x + \sec x)`; complete expression recipe x \left(2 x + \sec{\left(x \right)}\right) \tan{\left(x \right)}.

Choice 3: `2x\sec x\tan x`; complete expression recipe 2 x \tan{\left(x \right)} \sec{\left(x \right)}.

Choice 4: `x(2\tan x + x\sec^{2} x)`; complete expression recipe x^{2} \left(\tan^{2}{\left(x \right)} + 1\right) + 2 x \tan{\left(x \right)}.

Choice 5: `\sec x(2 + x^{2}\tan x)`; complete expression recipe \left(x^{2} \tan{\left(x \right)} + 2\right) \sec{\left(x \right)}.

Missing captured solution: authored four-stage solution uses canonical opening and stages.

### q-310188

Differentiate ${3}^{x}\operatorname{sin}(x).$

$({3}^{x}\operatorname{sin}(x))^{'}=$
{{field-1}} $+\,{3}^{x}\operatorname{cos}(x)$

Original parameters: {"b": 3}

Factors u=3^{x}, v=\sin{\left(x \right)}.

Field field-1 :answer-field.type/blank

Choice 1: `{3}^{x}\operatorname{ln}(3)\operatorname{sin}(x)`; complete expression recipe 3^{x} \ln{\left(3 \right)} \sin{\left(x \right)}.

Here, we have the product of the two functions $u(x)={3}^{x}$ and $v(x)=\operatorname{sin}(x).$ So, we apply the product rule:

$$
\begin{aligned}({3}^{x}\operatorname{sin}(x))^{'} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =({3}^{x})^{'}\cdot \operatorname{sin}(x)+{3}^{x}\cdot (\operatorname{sin}(x))^{'} \\  & =({3}^{x}\operatorname{ln}(3))(\operatorname{sin}(x))+({3}^{x})(\operatorname{cos}(x)) \\  & ={3}^{x}\operatorname{ln}(3)\operatorname{sin}(x)+{3}^{x}\operatorname{cos}(x)\end{aligned}
$$

### q-319402

Differentiate $(2-\operatorname{tan}(x))\operatorname{cos}(x)$

$((2-\operatorname{tan}(x))\operatorname{cos}(x))^{'}=-{sec}^{2}(x)\operatorname{cos}(x)\,+$
{{field-1}}

Original parameters: {"k": 2}

Factors u=2 - \tan{\left(x \right)}, v=\cos{\left(x \right)}.

Field field-1 :answer-field.type/blank

Choice 1: `(\operatorname{tan}(x)-2)\operatorname{sin}(x)`; complete expression recipe - \left(2 - \tan{\left(x \right)}\right) \sin{\left(x \right)}.

Here, we have the product of the two functions $u(x)=2-\operatorname{tan}(x)$ and $v(x)=\operatorname{cos}(x).$ So, we apply the product rule:

$$
\begin{aligned}((2-\operatorname{tan}(x))\operatorname{cos}(x))^{'} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(2-\operatorname{tan}(x))^{'}\cdot \operatorname{cos}(x)+(2-\operatorname{tan}(x))\cdot (\operatorname{cos}(x))^{'} \\  & =(-{sec}^{2}(x))(\operatorname{cos}(x))+(2-\operatorname{tan}(x))(-\operatorname{sin}(x)) \\  & =-{sec}^{2}(x)\operatorname{cos}(x)+(\operatorname{tan}(x)-2)\operatorname{sin}(x)\end{aligned}
$$

### q-71004

Differentiate ${e}^{x}\operatorname{sin}x.$

Original parameters: {"c": 1}

Factors u=e^{x}, v=\sin{\left(x \right)}.

Here, we have the product of the two functions $u(x)={e}^{x}$ and $v(x)=\operatorname{sin}x.$ So, we apply the product rule:

$$
\begin{aligned}({e}^{x}\operatorname{sin}x)^{'} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =({e}^{x})^{'}\cdot \operatorname{sin}x+{e}^{x}\cdot (\operatorname{sin}x)^{'} \\  & =({e}^{x})(\operatorname{sin}x)+({e}^{x})(\operatorname{cos}x) \\  & ={e}^{x}\operatorname{sin}x+{e}^{x}\operatorname{cos}x\end{aligned}
$$

### q-104297

Differentiate ${e}^{x}cos⁡x.$

Original parameters: {"c": 1}

Factors u=e^{x}, v=\cos{\left(x \right)}.

Field selection :answer-field.type/radio

Choice 1: `-{e}^{x}cos⁡x-{e}^{x}sin⁡x`; complete expression recipe - e^{x} \sin{\left(x \right)} - e^{x} \cos{\left(x \right)}.

Choice 2: `{e}^{x}cos⁡x+sin⁡x`; complete expression recipe e^{x} \cos{\left(x \right)} + \sin{\left(x \right)}.

Choice 3: `{e}^{x}cos⁡x-{e}^{x}sin⁡x`; complete expression recipe - e^{x} \sin{\left(x \right)} + e^{x} \cos{\left(x \right)}.

Choice 4: `-{e}^{x}cos⁡x+sin⁡x`; complete expression recipe - e^{x} \cos{\left(x \right)} + \sin{\left(x \right)}.

Choice 5: `{e}^{x}cos⁡x+{e}^{x}sin⁡x`; complete expression recipe e^{x} \sin{\left(x \right)} + e^{x} \cos{\left(x \right)}.

Here, we have the product of the two functions $u(x)={e}^{x}$ and $v(x)=cos⁡x.$ So, we apply the product rule:

$$
\begin{aligned}({e}^{x}cos⁡x)^{′} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({e}^{x})^{′}\cdot cos⁡x+{e}^{x}\cdot (cos⁡x)^{′} \\  & =({e}^{x})(cos⁡x)+({e}^{x})(-sin⁡x) \\  & ={e}^{x}cos⁡x-{e}^{x}sin⁡x\end{aligned}
$$

### q-1931

Differentiate ${e}^{x}tan⁡x.$

Original parameters: {"c": 1}

Factors u=e^{x}, v=\tan{\left(x \right)}.

Field selection :answer-field.type/radio

Choice 1: `{e}^{x}sec⁡x+{e}^{x}{sec}^{2}⁡x`; complete expression recipe e^{x} \sec^{2}{\left(x \right)} + e^{x} \sec{\left(x \right)}.

Choice 2: `{sec}^{2}⁡x+{e}^{x}tan⁡x`; complete expression recipe e^{x} \tan{\left(x \right)} + \sec^{2}{\left(x \right)}.

Choice 3: `{e}^{x}{csc}^{2}⁡x+{e}^{x}tan⁡x`; complete expression recipe e^{x} \tan{\left(x \right)} + e^{x} \csc^{2}{\left(x \right)}.

Choice 4: `{e}^{x}{sec}^{2}⁡x+tan⁡x`; complete expression recipe e^{x} \sec^{2}{\left(x \right)} + \tan{\left(x \right)}.

Choice 5: `{e}^{x}{sec}^{2}⁡x+{e}^{x}tan⁡x`; complete expression recipe \left(\tan^{2}{\left(x \right)} + 1\right) e^{x} + e^{x} \tan{\left(x \right)}.

Here, we have the product of the two functions $u(x)={e}^{x}$ and $v(x)=tan⁡x.$ So, we apply the product rule:

$$
\begin{aligned}({e}^{x}tan⁡x)^{′} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({e}^{x})^{′}\cdot tan⁡x+{e}^{x}\cdot (tan⁡x)^{′} \\  & =({e}^{x})(tan⁡x)+({e}^{x})({sec}^{2}⁡x) \\  & ={e}^{x}{sec}^{2}⁡x+{e}^{x}tan⁡x\end{aligned}
$$

### q-319350

Differentiate ${e}^{x}(2+sin⁡(x)).$

$({e}^{x}(2+sin⁡(x)))^{′}=$
{{field-1}} $+\,{e}^{x}cos⁡(x)$

Original parameters: {"c": 1, "k": 2}

Factors u=e^{x}, v=\sin{\left(x \right)} + 2.

Field field-1 :answer-field.type/blank

Choice 1: `(2+\operatorname{sin}(x)){e}^{x}`; complete expression recipe \left(\sin{\left(x \right)} + 2\right) e^{x}.

Here, we have the product of the two functions $u(x)={e}^{x}$ and $v(x)=2+sin⁡(x).$ So, we apply the product rule:

$$
\begin{aligned}({e}^{x}sec⁡(x))^{′} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({e}^{x})^{′}\cdot (2+sin⁡(x))+{e}^{x}\cdot (2+sin⁡(x))^{′} \\  & =({e}^{x})(2+sin⁡(x))+({e}^{x})(cos⁡(x)) \\  & =(2+sin⁡(x)){e}^{x}+{e}^{x}cos⁡(x)\end{aligned}
$$

### q-319357

Differentiate $2{x}^{2}cos⁡(x).$

$(2{x}^{2}cos⁡(x))^{′}=$
{{field-1}} $-\,2{x}^{2}sin⁡(x)$

Original parameters: {"c": 2, "n": 2}

Factors u=2 x^{2}, v=\cos{\left(x \right)}.

Field field-1 :answer-field.type/blank

Choice 1: `4x\operatorname{cos}(x)`; complete expression recipe 4 x \cos{\left(x \right)}.

Here, we have the product of the two functions $u(x)=2{x}^{2}$ and $v(x)=cos⁡(x).$ So, we apply the product rule:

$$
\begin{aligned}(2{x}^{2}cos⁡(x))^{′} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2{x}^{2})^{′}\cdot cos⁡(x)+2{x}^{2}\cdot (cos⁡(x))^{′} \\  & =(4x)(cos⁡(x))+(2{x}^{2})(-sin⁡(x)) \\  & =4xcos⁡(x)-2{x}^{2}sin⁡(x)\end{aligned}
$$

### q-319385

Differentiate $\sqrt{x}tan⁡(x).$

$(\sqrt{x}tan⁡(x))^{′}=\frac{tan⁡(x)}{2\sqrt{x}}\,+$
{{field-1}}

Original parameters: {"c": 1}

Factors u=\sqrt{x}, v=\tan{\left(x \right)}.

Field field-1 :answer-field.type/blank

Choice 1: `\sqrt{x}{sec}^{2}(x)`; complete expression recipe \sqrt{x} \left(\tan^{2}{\left(x \right)} + 1\right).

Here, we have the product of the two functions $u(x)=\sqrt{x}$ and $v(x)=tan⁡(x).$ So, we apply the product rule:

$$
\begin{aligned}(\sqrt{x}tan⁡(x))^{′} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(\sqrt{x})^{′}\cdot tan⁡(x)+\sqrt{x}\cdot (tan⁡(x))^{′} \\  & =\frac{1}{2\sqrt{x}}(tan⁡(x))+(\sqrt{x})({sec}^{2}⁡(x)) \\  & =\frac{tan⁡(x)}{2\sqrt{x}}+\sqrt{x}{sec}^{2}⁡(x)\end{aligned}
$$

## 2. Generalized descriptions

Observed radios assess a complete derivative; observed blanks assess exactly one product-rule term with the other term already displayed. The fixed worked solution names u,v, applies the product rule, substitutes derivatives, and distributes/collects. Fieldless q-71004 receives an authored full derivative blank. q-1907/q-47965 receive independently derived correct references and canonical four-row solutions; absent source correct refs cannot be counted as matched designations.

## 3. Components and complete bank mapping

Each list above maps all displayed source choices one-to-one. Polynomial-cos choices use u cos−u sin, u′ cos−u′ sin, u′ cos−u sin, u cos−u′ sin, u′ cos+u sin. Polynomial-tan shapes are u′+u sec tan; c x^(n−1)tan(n x+sec); u′sec tan; correct u′tan+u sec²; sec(nc+u tan). These are explicit generalized expression patterns; interpretation of the peculiar tan options is unresolved, and no original authoring-error code is claimed.

Exponential-cos complete bank uses −u cos−u sin; u cos+sin; correct u cos−u sin; −u cos+sin; u cos+u sin. Exponential-tan uses u sec+u sec²; sec²+u tan; u csc²+u tan; u sec²+tan; correct u sec²+u tan. The bare omitted factors remain bare in changed instances; distractor sign/omission interpretations are hypotheses. Blank recipes are u′v or uv′ exactly as their displayed placeholders request. Whole banks are rejected on any equivalent option; no first-valid recipe pool is used.

## 4. Reusable masks, constraints and calculations

One-pass longest-first masks replace complete factor/component expressions; they never replace a bare numeral across exponent/function prose. u,u′,v,v′ and final banks derive exactly using SymPy. Source prose and ordered four-stage structure are retained, with notation-only normalization recorded separately. The authored binomial/affine masks use the same canonical opening and four stages. The authored five-option default bank is the complete set {u′v+uv′, u′v′, u′v, uv′, u′v−uv′}; full-derivative blanks are also supported at authored levels.

Source q-1907 and q-47965 have no observed difficulty/correct ref/worked solution. Authoritative /home/jake/Developer/MA/DATA/Lessons/1109/Source/1109.json independently confirms both 5-choice widgets, without designations. Those records are authored easy based on the canonical power-times-trig example, and inferred correctness is independently differentiated. q-71004 is fieldless; adding a matching placeholder/blank is an explicit presentation repair. q-319350 first LHS says (e^x sec(x))′ whereas the prompt, named factors and remaining rows say e^x(2+sin(x)). `observed_raw` retains that error, and `repaired` changes just that first LHS. Raw error reproduction is excluded from normal teaching correctness; source fidelity and repaired correctness have separate denominators.

Original doubled backslashes and Unicode function-application characters are normalized for mathematical parsing. Original q-319357 2{x}²/4x components become standard CAS coefficient spacing/braces when rendered, preserving all whole solution sentences and ordered stages. Exact literal and component-normalized fidelity are reported separately by validator. No notation repair is allowed to exempt generated formatting. All blank canonical, meaningful equivalent and shifted incorrect entries, plus every radio option, are exercised by the compiled native application grader.

Domain: sqrt products x>0; tan factors avoid cos x=0. Source exponentials have positive bases2..7. Polynomial sin/cos factors are smooth for all real x. Metadata reports restrictions outside learner content. No plots are needed: steps5/7 have no assets or renderer.

