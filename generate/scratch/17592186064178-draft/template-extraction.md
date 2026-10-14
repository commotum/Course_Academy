# Four extraction stages

## 1. Specific source records

### q-2033
What is $\displaystyle \int2\cos ydy$?

Observed difficulty: absent. Fields: [('selection', ':answer-field.type/radio', 5)]

### q-2034
What is $\displaystyle \int - \sin θdθ$?

Observed difficulty: absent. Fields: [('selection', ':answer-field.type/radio', 5)]

### q-71653
$\int 4\operatorname{cos}y\,\text{d}y=$

Observed difficulty: :question.difficulty/easy. Fields: []

### q-71654
$\int (\operatorname{sin}x+5\operatorname{cos}x)\,\text{d}x=$

Observed difficulty: :question.difficulty/moderate. Fields: []

### q-167331
$\int h(x)\,\text{d}x\,=$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$+\,C,\,$ where $C$ is an arbitrary constant.

Observed difficulty: :question.difficulty/easy. Fields: [('field-1', ':answer-field.type/blank', 1)]

### q-167785
$\int h(x)\,\text{d}x\,=$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        
$+\,C,\,$ where $C$ is an arbitrary constant.

Observed difficulty: :question.difficulty/easy. Fields: [('field-1', ':answer-field.type/blank', 1)]

### q-113907
$\int (-6sin⁡\theta )\,\text{d}\theta =$

Observed difficulty: :question.difficulty/easy. Fields: [('selection', ':answer-field.type/radio', 5)]

### q-113908
$\int 5cos⁡y\,\text{d}y=$

Observed difficulty: :question.difficulty/easy. Fields: [('selection', ':answer-field.type/radio', 5)]

### q-113909
$\int (2cos⁡x+3sin⁡x)\,\text{d}x=$

Observed difficulty: :question.difficulty/moderate. Fields: [('selection', ':answer-field.type/radio', 5)]

### q-17654
$\int (-cos⁡\theta )\,\text{d}\theta =$

Observed difficulty: :question.difficulty/easy. Fields: [('selection', ':answer-field.type/radio', 5)]

### q-2161
$\int (cos⁡x-sin⁡x)\,\text{d}x=$

Observed difficulty: :question.difficulty/moderate. Fields: [('selection', ':answer-field.type/radio', 5)]

### q-166078
$\int h(x)\,\text{d}x\,=${{field-1}}
$+\,C,\,$ where $C$ is an arbitrary constant.

Observed difficulty: :question.difficulty/easy. Fields: [('field-1', ':answer-field.type/blank', 1)]

## 2. Shared mathematical pattern
Single weighted sine/cosine or two-term linear combination at the unchanged independent variable. Reverse d(sin)/dx=cos and d(cos)/dx=-sin, extract constant multipliers, apply sum rule; supplied +C blanks require only the nonconstant fragment. Source-specific spacing, function notation, recalled-rule paragraphs and ordered operator stages remain raw masks. Normal source profiles undergo separately documented UI notation normalization only.

## 3. Complete component and bank mapping

### q-2033
Parameter anchors: {"a": 2}
Prompt mask: `What is $\displaystyle \int{a}\cos ydy$?`

- Field selection, option 1: `{a}\sin y + C` → correct reverse derivative (designation absent)
- Field selection, option 2: `\sin y + C` → omit coefficient
- Field selection, option 3: `-2\sin y + C` → reverse primitive sign
- Field selection, option 4: `{a}\cos y + C` → leave cosine unchanged
- Field selection, option 5: `-2\cos y + C` → differentiate cosine
Worked-solution stage mask:
```text
ABSENT (preserved)
```

### q-2034
Parameter anchors: {"a": 1}
Prompt mask: `What is $\displaystyle \int - {ua}\sin θdθ$?`

- Field selection, option 1: `{ua}\tan θ + C` → wrong trig-function reversal to tan (evidence only)
- Field selection, option 2: `-{ua}\cos θ + C` → wrong sign for cosine primitive
- Field selection, option 3: `{ua}\sin θ + C` → keep sine unchanged with reversed sign
- Field selection, option 4: `-{ua}\sin θ + C` → keep sine unchanged
- Field selection, option 5: `{ua}\cos θ + C` → correct cosine primitive (designation absent)
Worked-solution stage mask:
```text
ABSENT (preserved)
```

### q-71653
Parameter anchors: {"a": 4}
Prompt mask: `$\int {a}\operatorname{cos}y\,\text{d}y=$`

Worked-solution stage mask:
```text
Recall that

$$
\int \operatorname{cos}y\,\text{d}y=\operatorname{sin}y+C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int {a}\operatorname{cos}y\,\text{d}y & ={a}\int \operatorname{cos}y\,\text{d}y \\  & ={a}(\operatorname{sin}y)+C \\  & ={a}\operatorname{sin}y+C.\end{aligned}\end{aligned}
$$
```

### q-71654
Parameter anchors: {"a": 5}
Prompt mask: `$\int (\operatorname{sin}x+{a}\operatorname{cos}x)\,\text{d}x=$`

Worked-solution stage mask:
```text
Recall that

$$
\begin{aligned}\int \operatorname{sin}x\,\text{d}x & =-\operatorname{cos}x+C, \\ \int \operatorname{cos}x\,\text{d}x & =\operatorname{sin}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (\operatorname{sin}x+{a}\operatorname{cos}x)\,\text{d}x & =\int \operatorname{sin}x\,\text{d}x+{a}\int \operatorname{cos}x\,\text{d}x \\  & =-\operatorname{cos}x+{a}\operatorname{sin}x+C.\end{aligned}
$$
```

### q-167331
Parameter anchors: {"a": 4}
Prompt mask: `$\int h(x)\,\text{d}x\,=$\n\n                            \n                                    \n                            \n                                        {{field-1}}                \n                                    \n                                \n                                    \n                                        \n                                        \n$+\,C,\,$ where $C$ is an arbitrary constant.`

- Field field-1, option 1: `{a}\operatorname{cos}x` → required nonconstant primitive fragment; arbitrary C already supplied.
Worked-solution stage mask:
```text
Recall that

$$
\int \operatorname{sin}⁡x\,\text{d}x=-\operatorname{cos}⁡x+C.
$$

Therefore, we have

$$
\begin{aligned}\int h(x)\,\text{d}x & =\int -{a}\operatorname{sin}⁡x\,\text{d}x \\  & =-{a}\int \operatorname{sin}⁡x\,\text{d}x \\  & =-{a}(-\operatorname{cos}⁡x)+C \\  & ={a}\operatorname{cos}⁡x+C,\end{aligned}
$$

where $C$ is an arbitrary constant.
```

### q-167785
Parameter anchors: {"a": 4}
Prompt mask: `$\int h(x)\,\text{d}x\,=$\n\n                            \n                                    \n                            \n                                        {{field-1}}                \n                                    \n                                \n                                    \n                                        \n                                        \n$+\,C,\,$ where $C$ is an arbitrary constant.`

- Field field-1, option 1: `{a}\operatorname{cos}(x)` → required nonconstant primitive fragment; arbitrary C already supplied.
Worked-solution stage mask:
```text
Recall that

$$
\int \operatorname{sin}⁡(x)\,\text{d}x=-\operatorname{cos}⁡(x)+C.
$$

Therefore, we have

$$
\begin{aligned}\int h(x)\,\text{d}x & =\int -{a}\operatorname{sin}⁡(x)\,\text{d}x \\  & =-{a}\int \operatorname{sin}⁡(x)\,\text{d}x \\  & =-{a}(-\operatorname{cos}⁡(x))+C \\  & ={a}\operatorname{cos}⁡(x)+C,\end{aligned}
$$

where $C$ is an arbitrary constant.
```

### q-113907
Parameter anchors: {"a": 6}
Prompt mask: `$\int (-{a}sin⁡\theta )\,\text{d}\theta =$`

- Field selection, option 1: `-\frac{1}{{a}}cos⁡\theta +C` → reciprocal multiplier and incorrect sine primitive sign
- Field selection, option 2: `{a}cos⁡\theta +C` → correct reverse derivative
- Field selection, option 3: `-{a}sin⁡\theta +C` → leave sine unchanged
- Field selection, option 4: `{a}sin⁡\theta +C` → sine unchanged and reverse coefficient sign
- Field selection, option 5: `-{a}cos⁡\theta +C` → forget minus in primitive
Worked-solution stage mask:
```text
Recall that

$$
\int sin⁡\theta \,\text{d}\theta =-cos⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int (-{a}sin⁡\theta )\,\text{d}\theta  & =-{a}\int sin⁡\theta \,\text{d}\theta  \\  & =-{a}(-cos⁡\theta )+C \\  & ={a}cos⁡\theta +C.\end{aligned}\end{aligned}
$$
```

### q-113908
Parameter anchors: {"a": 5}
Prompt mask: `$\int {a}cos⁡y\,\text{d}y=$`

- Field selection, option 1: `-\frac{1}{{a}}sin⁡y+C` → reciprocal coefficient with wrong sign
- Field selection, option 2: `\frac{1}{{a}}sin⁡y+C` → reciprocal coefficient
- Field selection, option 3: `{a}cos⁡y+C` → leave cosine unchanged
- Field selection, option 4: `{a}sin⁡y+C` → correct reverse derivative
- Field selection, option 5: `-{a}cos⁡y+C` → differentiate cosine instead of integrate
Worked-solution stage mask:
```text
Recall that

$$
\int cos⁡y\,\text{d}y=sin⁡y+C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int {a}cos⁡y\,\text{d}y & ={a}\int cos⁡y\,\text{d}y \\  & ={a}(sin⁡y)+C \\  & ={a}sin⁡y+C.\end{aligned}\end{aligned}
$$
```

### q-113909
Parameter anchors: {"a": 2, "b": 3}
Prompt mask: `$\int ({a}cos⁡x+{b}sin⁡x)\,\text{d}x=$`

- Field selection, option 1: `{a}sin⁡x-{b}cos⁡x+C` → correct separate primitives
- Field selection, option 2: `{a}sin⁡x+{b}cos⁡x+C` → forget minus in sine primitive
- Field selection, option 3: `{a}cos⁡x-{b}sin⁡x+C` → keep trig functions unchanged with changed sine sign
- Field selection, option 4: `{b}cos⁡x-{a}sin⁡x+C` → swap coefficient roles and signs
- Field selection, option 5: `{b}sin⁡x-{a}cos⁡x+C` → swap coefficient roles
Worked-solution stage mask:
```text
Recall that

$$
\begin{aligned}\int sin⁡x\,\text{d}x & =-cos⁡x+C, \\ \int cos⁡x\,\text{d}x & =sin⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int ({a}cos⁡x+{b}sin⁡x)\,\text{d}x & ={a}\int cos⁡x\,\text{d}x+{b}\int sin⁡x\,\text{d}x \\  & ={a}sin⁡x+{b}(-cos⁡x)+C \\  & ={a}sin⁡x-{b}cos⁡x+C.\end{aligned}
$$
```

### q-17654
Parameter anchors: {"a": 1}
Prompt mask: `$\int (-{ua}cos⁡\theta )\,\text{d}\theta =$`

- Field selection, option 1: `-{ua}{sin}^{2}⁡\theta +C` → wrong squared sine primitive
- Field selection, option 2: `{ua}sin⁡\theta +C` → lose leading minus
- Field selection, option 3: `{ua}{cos}^{2}⁡\theta +C` → wrong squared cosine primitive (same family as squared sine option)
- Field selection, option 4: `-{ua}sin⁡\theta +C` → correct reverse derivative
- Field selection, option 5: `-{ua}cos⁡\theta +C` → leave cosine unchanged
Worked-solution stage mask:
```text
Recall that

$$
\int cos⁡\theta \,\text{d}\theta =sin⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int (-{ua}cos⁡\theta )\text{d}\theta  & =-{ua}\int cos⁡\theta \,\text{d}\theta  \\  & =-{ua}sin⁡\theta +C.\end{aligned}\end{aligned}
$$
```

### q-2161
Parameter anchors: {"a": 1, "b": 1}
Prompt mask: `$\int ({ua}cos⁡x-{ub}sin⁡x)\,\text{d}x=$`

- Field selection, option 1: `-{ua}sin⁡x-{ub}cos⁡x+C` → negate both correct components
- Field selection, option 2: `-{ua}sin⁡x+{ub}cos⁡x+C` → lose cosine-integral sign
- Field selection, option 3: `{sum}sin⁡x+C` → combine both coefficients on sine (wrongly integrate -sin as +sin)
- Field selection, option 4: `{ua}sin⁡x+{ub}cos⁡x+C` → correct separate primitives
- Field selection, option 5: `{ua}sin⁡x-{ub}cos⁡x+C` → forget double negative
Worked-solution stage mask:
```text
Recall that

$$
\begin{aligned}\int sin⁡x\,\text{d}x & =-cos⁡x+C, \\ \int cos⁡x\,\text{d}x & =sin⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int ({ua}cos⁡x-{ub}sin⁡x)\,\text{d}x & ={ua}\int cos⁡x\,\text{d}x-{ub}\int sin⁡x\,\text{d}x \\  & ={ua}sin⁡x-{ub}(-cos⁡x)+C \\  & ={ua}sin⁡x+{ub}cos⁡x+C.\end{aligned}
$$
```

### q-166078
Parameter anchors: {"a": 4}
Prompt mask: `$\int h(x)\,\text{d}x\,=${{field-1}}\n$+\,C,\,$ where $C$ is an arbitrary constant.`

- Field field-1, option 1: `{a}\cos x` → required nonconstant primitive fragment; arbitrary C already supplied.
Worked-solution stage mask:
```text
Recall that

$$
\int \operatorname{sin}⁡x\,\text{d}x=-\operatorname{cos}⁡x+C.
$$

Therefore, we have

$$
\begin{aligned}\int h(x)\,\text{d}x & =\int -{a}\operatorname{sin}⁡x\,\text{d}x \\  & =-{a}\int \operatorname{sin}⁡x\,\text{d}x \\  & =-{a}(-\operatorname{cos}⁡x)+C \\  & ={a}\operatorname{cos}⁡x+C,\end{aligned}
$$

where $C$ is an arbitrary constant.
```

## 4. Reusable backbone and variable slots
Templates are public in templates.json. Scalar placeholders a,b replace complete coefficient roles, including each factor extracted from its integral and reciprocal error denominators; ua,ub conditionally omit unit coefficients, and sum computes a+b for q-2161's wrong combination. Raw domains are positive integers1..9; profiles remain public and ineligible even when repaired keys could be inferred. Original q-17654 exponent2 is an error-operation stage, not a sampled exponent or a supported sine-square integration family.

Each supported source solution retains its distinct recalled rules, extraction/sum rows, substituted primitives and final collection, including q-71654's omission of a redundant intermediate primitive row and the three h recipes' explicit formal substitution row. Normal source banks are parameterized, not source literals or correct-plus-offset lookups. Fixed observed variables are notation only; they do not inflate fingerprints.

Authored signed easy complete bank computes correct primitive first, sign reversal, reciprocal/sign factor mistake, unchanged integrand, and derivative-sign unchanged integrand. Moderate uses the complete q-113909 coefficient/sign/function-role bank. For hard let A=a+b and B=b-a. Correct A sin−B cos; bank2 (a−b) sin−(a+b) cos comes from exchanging sum/difference coefficient roles during collection; bank3 a sin−b cos omits one component from each distributed group; bank4 A cos−B sin keeps trig functions unchanged while copying primitive signs; bank5 −A sin+B cos reverses both primitive signs. These five operations are selected together before parameters, and any pair equivalent modulo a constant rejects the whole instance. No pooled distractor replacement occurs.

Authored hard solution shows the two groups, the four individually distributed signed terms, the two collected terms, constant-multiple/sum split, substituted sine/cosine primitives, then final collection. Every actual printed formal-input and primitive row is checked by differentiating an independently component-derived primitive, and operative stage counts are checked separately. Raw source replay exactness is not counted as mathematical correctness.

Source IDs/answer UUIDs are replaced with field-owned deterministic IDs after rendering. Full content identity uses version, actual difficulty presence/value, prompt, fixed solution and complete keyed bank (including correct designation); mathematical identity canonicalizes the actual printed integrand and separately records hard grouped distribution demand. Alias names/seed/option order do not affect either identity. C is arbitrary in radio family comparisons; blanks state the exact requested fragment with C supplied separately and native scalar-fragment grading is tested separately.

Source coefficient guards reject nonunit-profile a=1 for q-2033,q-113907,q-113908 and equal coefficients for q-113909, including raw changed-parameter calls. Original source anchors remain accepted. Authored optional blanks at every level use the observed supplied-C fragment response shape; their field key, fragment placeholder and explicit no-added-constant instruction vary together and are checked natively. Meaningful equivalent blank entries distribute one printed coefficient into (coefficient−1) and1 or reorder components; these are parsed separately and checked for exact equality before submission.


## Analytic domains and arbitrary-constant roles

For every normal family, sine and cosine take the actual displayed independent variable (x, y or theta) over all real numbers. Their constant multiples, sums and grouped linear combinations are defined and continuous on the whole real line, and every correct primitive is defined and differentiable on that same domain. There are no branches, restricted arguments or endpoint conditions. C is an arbitrary real integration constant. Analytic domains are distinct from the finite coefficient sampling domains above.

Radio responses represent complete antiderivative families and are compared modulo an arbitrary additive constant, including comparisons between two wrong choices. A normal blank retains the source-shaped supplied +C, asks for the displayed nonconstant primitive fragment without another constant, and expects equality of that fragment; family equivalence does not make an added constant a valid fragment response. These roles and the actual displayed variable are recorded in generation.domain without changing learner content or identity.

Raw q-167331, q-167785 and q-166078 do not define h in the prompt. Their analytic domain and requested primitive cannot be established from the raw prompt, even though the worked solution substitutes -a sin x. Their generation.domain status is unresolved and they remain evidence-only/ineligible. The separately authored repaired_h prompt explicitly defines h, giving it the all-real sine domain. Other raw source integrands and their correct primitives have all-real domains. Raw q-2034 contains a wrong tangent choice with poles at theta=pi/2+k*pi; that distractor's restricted domain is recorded separately and does not restrict the given sine integrand or correct cosine primitive.
