# Template extraction

## 1. Specific original questions

All12 MA questions follow below with their original full prompt and worked solution. Independent records are retained separately and are not source-bank evidence.

### q-2037

What is $\displaystyle \int2\csc^{2} θdθ$?

Observed parameters: `{"a": 2}`. Rating absent/unrated.

Worked solution absent in source.

### q-49093

What is $\displaystyle \int\csc x(\csc x - 2\cot x)dx$?

Observed parameters: `{"a": 2}`. Rating absent/unrated.

Worked solution absent in source.

### q-113948

$\int -\frac{5}{2}{csc}^{2}x\,\text{d}x=$

Observed parameters: `{"n": 5, "d": 2}`. Rating :question.difficulty/easy.

Recall that 

$$
\int {csc}^{2}x\,\text{d}x=-\operatorname{cot}x+C
$$

Therefore, we get

$$
\begin{aligned}\begin{aligned}\int -\frac{5}{2}{csc}^{2}x\,\text{d}x & =-\frac{5}{2}\int {csc}^{2}x\,\text{d}x \\  & =-\frac{5}{2}(-\operatorname{cot}x)+C \\  & =\frac{5}{2}\operatorname{cot}x+C.\end{aligned}\end{aligned}
$$

### q-113952

$\int 3{csc}^{2}x-4\operatorname{sec}x\operatorname{tan}x\,\text{d}x=$

Observed parameters: `{"a": 3, "b": 4}`. Rating :question.difficulty/moderate.

Recall that 

$$
\begin{aligned}\int \operatorname{sec}x\operatorname{tan}x\,\text{d}x & =\operatorname{sec}x+C, \\ \int {csc}^{2}x\,\text{d}x & =-\operatorname{cot}x+C.\end{aligned}
$$

Therefore, we get

$$
\begin{aligned}\begin{aligned}\int 3{csc}^{2}x-4\operatorname{sec}x\operatorname{tan}x\,\text{d}x & =3\int {csc}^{2}x\,\text{d}x-4\int \operatorname{sec}x\operatorname{tan}x\,\text{d}x \\  & =3(-\operatorname{cot}x)-4(\operatorname{sec}x)+C \\  & =-3\operatorname{cot}x-4\operatorname{sec}x+C.\end{aligned}\end{aligned}
$$

### q-113958

$\int (\operatorname{sec}x\operatorname{tan}x-2{csc}^{2}x+\operatorname{sin}x)\,\text{d}x=$

Observed parameters: `{"a": 1, "b": 2, "c": 1}`. Rating :question.difficulty/hard.

Recall that 

$$
\begin{aligned}\int {csc}^{2}x\,\text{d}x & =-\operatorname{cot}x+C, \\ \int \operatorname{sec}x\operatorname{tan}x\,\text{d}x & =\operatorname{sec}x+C, \\ \int sin\,\text{d}x & =-\operatorname{cos}x+C.\end{aligned}
$$

Therefore, we get

$$
\begin{aligned}\begin{aligned}\int (\operatorname{sec}x\operatorname{tan}x-2{csc}^{2}x+\operatorname{sin}x)\,\text{d}x & =\int \operatorname{sec}x\operatorname{tan}x\,\text{d}x-2\int {csc}^{2}x\,\text{d}x+\int \operatorname{sin}x\,\text{d}x \\  & =\operatorname{sec}x-2(-\operatorname{cot}x)+(-\operatorname{cos}x)+C \\  & =\operatorname{sec}x+2\operatorname{cot}x-\operatorname{cos}x+C.\end{aligned}\end{aligned}
$$

### q-143522

$\int v(t)\,\text{d}t\,\,=\,${{field-1}} $+\text{ }C$

Observed parameters: `{"a": 4}`. Rating :question.difficulty/easy.

Recall that 

$$
\int {csc}^{2}t\,\text{d}t=-\operatorname{cot}t+C.
$$

Therefore, we get

$$
\begin{aligned}\begin{aligned}\int 4{csc}^{2}t\,\text{d}t & =4\int {csc}^{2}t\,\text{d}t \\  & =4(-\operatorname{cot}t)+C \\  & =-4\operatorname{cot}t+C.\end{aligned}\end{aligned}
$$

### q-167569

$\int v(t)\,\text{d}t\,\,=\,$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                         $+\text{ }C$

Observed parameters: `{"a": 2}`. Rating :question.difficulty/easy.

Recall that 

$$
\int {csc}^{2}⁡t\,\text{d}t=-\operatorname{cot}⁡t+C.
$$

Therefore, we get

$$
\begin{aligned}\begin{aligned}\int 2{csc}^{2}⁡t\,\text{d}t & =2\int {csc}^{2}⁡t\,\text{d}t \\  & =2(-\operatorname{cot}⁡t)+C \\  & =-2\operatorname{cot}⁡t+C.\end{aligned}\end{aligned}
$$

### q-113947

$\int 5{csc}^{2}⁡\theta \,\text{d}\theta =$

Observed parameters: `{"a": 5}`. Rating :question.difficulty/easy.

Recall that 

$$
\int {csc}^{2}⁡\theta \,\text{d}\theta =-cot⁡\theta +C
$$

Therefore, we get

$$
\begin{aligned}\begin{aligned}\int 5{csc}^{2}⁡\theta \,\text{d}\theta  & =5\int {csc}^{2}⁡\theta \,\text{d}\theta  \\  & =5(-cot⁡\theta )+C \\  & =-5cot⁡\theta +C.\end{aligned}\end{aligned}
$$

### q-49121

Calculate $\int csc⁡x(3cot⁡x+2csc⁡x)\text{d}x.$

Observed parameters: `{"a": 3, "b": 2}`. Rating :question.difficulty/moderate.

Recall that 

$$
\begin{aligned}\int {csc}^{2}⁡x\,\text{d}x & =-cot⁡x+C, \\ \int csc⁡xcot⁡x\,\text{d}x & =-csc⁡x+C.\end{aligned}
$$

Therefore, we get

$$
\begin{aligned}\begin{aligned}\int csc⁡x(3cot⁡x+2csc⁡x)\text{d}x & =\int (3csc⁡xcot⁡x+2{csc}^{2}⁡x)\,\text{d}x \\  & =\int 3csc⁡xcot⁡x\,\text{d}x+\int 2{csc}^{2}⁡x\,\text{d}x \\  & =3\int csc⁡xcot⁡x\,\text{d}x+2\int {csc}^{2}⁡x\,\text{d}x \\  & =3(-csc⁡x)+2(-cot⁡x)+C \\  & =-3csc⁡x-2cot⁡x+C.\end{aligned}\end{aligned}
$$

### q-71663

$\int -3{csc}^{2}⁡y\,\text{d}y=$

Observed parameters: `{"a": 3}`. Rating :question.difficulty/easy.

Recall that 

$$
\int {csc}^{2}⁡y\,\text{d}y=-cot⁡y+C
$$

Therefore, we get

$$
\begin{aligned}\begin{aligned}\int -3{csc}^{2}⁡y\,\text{d}y & =-3\int {csc}^{2}⁡y\,\text{d}y \\  & =-3(-cot⁡y)+C \\  & =3cot⁡y+C.\end{aligned}\end{aligned}
$$

### q-71664

$\int -{csc}^{2}⁡y\,\text{d}y=$

Observed parameters: `{}`. Rating :question.difficulty/easy.

Recall that 

$$
\int {csc}^{2}⁡y\,\text{d}y=-cot⁡y+C
$$

Therefore, we get

$$
\begin{aligned}\begin{aligned}\int -{csc}^{2}⁡y\,\text{d}y & =-\int {csc}^{2}⁡y\,\text{d}y \\  & =-(-cot⁡y)+C \\  & =cot⁡y+C.\end{aligned}\end{aligned}
$$

### q-71666

$\int sin⁡x-5{csc}^{2}⁡x\,\text{d}x=$

Observed parameters: `{"b": 5}`. Rating :question.difficulty/moderate.

Recall that 

$$
\begin{aligned}\int sin⁡x\,\text{d}x & =-cos⁡x+C, \\ \int {csc}^{2}⁡x\,\text{d}x & =-cot⁡x+C.\end{aligned}
$$

Therefore, we get

$$
\begin{aligned}\begin{aligned}\int sin⁡x-5{csc}^{2}⁡x\,\text{d}x & =\int sin⁡x\,\text{d}x-5\int {csc}^{2}⁡x\,\text{d}x \\  & =-cos⁡x-5(-cot⁡x)+C \\  & =-cos⁡x+5cot⁡x+C.\end{aligned}\end{aligned}
$$

## 2. Generalized mathematical and instructional backbone

Recall csc²→-cot, extract scalar coefficients, substitute and simplify signs. Two-term source families also recall sin→-cos, sec tan→sec or csc cot→-csc and use signed sum linearity. Product csc(a cot+b csc) expands first, splits its two integrals, extracts both scalars, substitutes each negative primitive, and simplifies. Hard recalls three primitives, splits/scales the three integrals, substitutes signed primitives, and collects signs. The source ordering and wording are retained by explicit masks; standalone blank answers omit C because the prompt supplies +C.

Lesson wrappers establish all five primitive pairs and the sum-rule prerequisite. Changing integral arguments or performing substitution/identity reduction would add a method and is outside scope. The fixed sin and cosine companion terms are source roles; they are not replaced by unrelated functions to inflate variety.

## 3. Complete components and profile mapping

Every prompt, solution, field key/type, choice value/type, designation and missing attribute is parameterized in source-profiles.json. A raw profile is a public evidence-only mode with original omission/rating parity. The tables below map every original choice one-to-one to its complete recipe; bank profiles are never pooled.

### q-2037 complete profile

Prompt mask: `What is $\displaystyle \int@a@\csc^{2} θdθ$?`

Field key/type: `selection / :answer-field.type/radio`. Captured correct designation: `ABSENT`.

| Position | Exact original value | Complete recipe | Operation/pattern |
|---|---|---|---|
| 1 | `-2\cot θ + C` | `-@a@\cot θ + C` | Correct mathematical value -a cot; no captured key. |
| 2 | `-2\tan θ + C` | `-@a@\tan θ + C` | Replace cot by tan. |
| 3 | `-2\sec θ\tan θ + C` | `-@a@\sec θ\tan θ + C` | Replace cot by sec tan product, retain negative sign. |
| 4 | `2\sec θ\tan θ + C` | `@a@\sec θ\tan θ + C` | Replace negative cot by positive sec tan. |
| 5 | `2\cot θ + C` | `@a@\cot θ + C` | Reverse primitive sign. |

### q-49093 complete profile

Prompt mask: `What is $\displaystyle \int\csc x(\csc x - @a@\cot x)dx$?`

Field key/type: `selection / :answer-field.type/radio`. Captured correct designation: `ABSENT`.

| Position | Exact original value | Complete recipe | Operation/pattern |
|---|---|---|---|
| 1 | `-\cot x + 2\csc x + C` | `-\cot x + @a@\csc x + C` | Correct -cot+a csc; no captured key. |
| 2 | `2\cot x - \csc x + C` | `@a@\cot x - \csc x + C` | Swap coefficient roles and signs: a cot-csc. |
| 3 | `-\cot x + \csc x + C` | `-\cot x + \csc x + C` | Drop coefficient on csc: -cot+csc. |
| 4 | `-\cot x - 2\csc x + C` | `-\cot x - @a@\csc x + C` | Reverse csc primitive term sign: -cot-a csc. |
| 5 | `2\cot x + \csc x + C` | `@a@\cot x + \csc x + C` | Swap coefficient roles: a cot+csc. |

### q-113948 complete profile

Prompt mask: `$\int -\frac{@n@}{@d@}{csc}^{2}x\,\text{d}x=$`

Field attribute absent; any default radio field is explicitly authored.

### q-113952 complete profile

Prompt mask: `$\int @a@{csc}^{2}x-@b@\operatorname{sec}x\operatorname{tan}x\,\text{d}x=$`

Field attribute absent; any default radio field is explicitly authored.

### q-113958 complete profile

Prompt mask: `$\int (@acoef@\operatorname{sec}x\operatorname{tan}x-@b@{csc}^{2}x+@ccoef@\operatorname{sin}x)\,\text{d}x=$`

Field attribute absent; any default radio field is explicitly authored.

### q-143522 complete profile

Prompt mask: `$\int v(t)\,\text{d}t\,\,=\,${{field-1}} $+\text{ }C$`

Field key/type: `field-1 / :answer-field.type/blank`. Captured correct designation: `-@a@\operatorname{cot}t`.

| Position | Exact original value | Complete recipe | Operation/pattern |
|---|---|---|---|
| 1 | `-4\operatorname{cot}t` | `-@a@\operatorname{cot}t` | Correct blank primitive -a cot(t); C supplied outside the field. |

### q-167569 complete profile

Prompt mask: `$\int v(t)\,\text{d}t\,\,=\,$

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                         $+\text{ }C$`

Field key/type: `field-1 / :answer-field.type/blank`. Captured correct designation: `-@a@\operatorname{cot}t`.

| Position | Exact original value | Complete recipe | Operation/pattern |
|---|---|---|---|
| 1 | `-2\operatorname{cot}t` | `-@a@\operatorname{cot}t` | Correct blank primitive -a cot(t); C supplied outside the field. |

### q-113947 complete profile

Prompt mask: `$\int @a@{csc}^{2}⁡\theta \,\text{d}\theta =$`

Field key/type: `selection / :answer-field.type/radio`. Captured correct designation: `-@a@cot⁡\theta +C`.

| Position | Exact original value | Complete recipe | Operation/pattern |
|---|---|---|---|
| 1 | `-5csc⁡\theta cot⁡\theta +C` | `-@a@csc⁡\theta cot⁡\theta +C` | Replace -cot by -csc cot. |
| 2 | `5sec⁡\theta tan⁡\theta +C` | `@a@sec⁡\theta tan⁡\theta +C` | Replace -cot by positive sec tan. |
| 3 | `-5cot⁡\theta +C` | `-@a@cot⁡\theta +C` | Correct: -a cot. |
| 4 | `-5tan⁡\theta +C` | `-@a@tan⁡\theta +C` | Replace cot by tan, retaining negative sign. |
| 5 | `5cot⁡\theta +C` | `@a@cot⁡\theta +C` | Reverse primitive sign to a cot. |

### q-49121 complete profile

Prompt mask: `Calculate $\int csc⁡x(@a@cot⁡x+@b@csc⁡x)\text{d}x.$`

Field key/type: `selection / :answer-field.type/radio`. Captured correct designation: `-@a@csc⁡x-@b@cot⁡x+C`.

| Position | Exact original value | Complete recipe | Operation/pattern |
|---|---|---|---|
| 1 | `-3csc⁡x-2cot⁡x+C` | `-@a@csc⁡x-@b@cot⁡x+C` | Correct -a csc-b cot. |
| 2 | `-2cos⁡x+2tan⁡x+C` | `-@b@cos⁡x+@b@tan⁡x+C` | Observed compound pattern -b cos+b tan; ignores a, intent unresolved. |
| 3 | `3csc⁡x-2sec⁡x+C` | `@a@csc⁡x-@b@sec⁡x+C` | Reverse first primitive sign; replace cot by sec: a csc-b sec. |
| 4 | `-3csc⁡x-2tan⁡x+C` | `-@a@csc⁡x-@b@tan⁡x+C` | Replace cot by tan: -a csc-b tan. |
| 5 | `3{sin}^{3}⁡x-2cot⁡x+C` | `@a@{sin}^{3}⁡x-@b@cot⁡x+C` | Replace -csc by positive sin^3: a sin^3-b cot; exponent3 fixed, intent unresolved. |

### q-71663 complete profile

Prompt mask: `$\int -@a@{csc}^{2}⁡y\,\text{d}y=$`

Field key/type: `selection / :answer-field.type/radio`. Captured correct designation: `@a@cot⁡y+C`.

| Position | Exact original value | Complete recipe | Operation/pattern |
|---|---|---|---|
| 1 | `3tan⁡y+C` | `@a@tan⁡y+C` | Replace cot by tan. |
| 2 | `3cot⁡y+C` | `@a@cot⁡y+C` | Correct a cot after negative scalar and negative primitive cancel. |
| 3 | `-3tan⁡y+C` | `-@a@tan⁡y+C` | Replace cot by negative tan. |
| 4 | `-3cot⁡y+C` | `-@a@cot⁡y+C` | Lose negative-scalar cancellation: -a cot. |
| 5 | `3csc⁡ycot⁡y+C` | `@a@csc⁡ycot⁡y+C` | Retain derivative product a csc cot. |

### q-71664 complete profile

Prompt mask: `$\int -{csc}^{2}⁡y\,\text{d}y=$`

Field key/type: `selection / :answer-field.type/radio`. Captured correct designation: `cot⁡y+C`.

| Position | Exact original value | Complete recipe | Operation/pattern |
|---|---|---|---|
| 1 | `sec⁡ytan⁡y+C` | `sec⁡ytan⁡y+C` | Use sec tan instead of cot. |
| 2 | `tan⁡y+C` | `tan⁡y+C` | Use tan instead of cot. |
| 3 | `-tan⁡y+C` | `-tan⁡y+C` | Use -tan instead of cot. |
| 4 | `cot⁡y+C` | `cot⁡y+C` | Correct cot. |
| 5 | `-cot⁡y+C` | `-cot⁡y+C` | Lose negative-scalar cancellation: -cot. |

### q-71666 complete profile

Prompt mask: `$\int sin⁡x-@b@{csc}^{2}⁡x\,\text{d}x=$`

Field key/type: `selection / :answer-field.type/radio`. Captured correct designation: `-cos⁡x+@b@cot⁡x+C`.

| Position | Exact original value | Complete recipe | Operation/pattern |
|---|---|---|---|
| 1 | `cos⁡x+5cot⁡x+C` | `cos⁡x+@b@cot⁡x+C` | Reverse cosine primitive sign. |
| 2 | `-cos⁡x+5cot⁡x+C` | `-cos⁡x+@b@cot⁡x+C` | Correct -cos+b cot. |
| 3 | `-cos⁡x-5cot⁡x+C` | `-cos⁡x-@b@cot⁡x+C` | Lose negative-scalar cancellation on csc² term: -cos-b cot. |
| 4 | `-csc+5tan⁡x+C` | `-csc+@b@tan⁡x+C` | Observed -csc+b tan: csc argument ABSENT; undefined mathematical value, evidence-only. |
| 5 | `csc-5tan⁡x+C` | `csc-@b@tan⁡x+C` | Observed csc-b tan: csc argument ABSENT; undefined mathematical value, evidence-only. |

## 4. Reusable templates, slots and normal completion policy

Integer magnitude slots a,b,c range1..9; source nonunit easy masks q113947 and q71663 require a2..9. Fraction numerator/denominator n,d are coprime2..9, unequal, so the coefficient stays a reduced noninteger rational. Original numerator5/denominator2 is included. Raw q49093 requires a>=2 because a=1 collides with its coefficient-drop option. Raw q71664 has no parameter slots: it remains an exact unit instance.

Normal easy families: q113947 uses its full five-option bank; q71663 uses its distinct complete bank; single-negative generalizes the unit q71664 bank by multiplying every primitive value by a and retaining all three calculation stages; fraction uses q113948 full source solution with a new complete bank (correct n/d cot, opposite sign, cot→tan, cot→csc, retain csc²). Blank adds v(t)=a csc²(t) from the captured solution, keeps field-1/blank/one canonical choice and omits C from the answer. Blank and radio aliases of the same scalar integral do not add mathematical novelty.

Normal moderate q49121 keeps all five source expression patterns at changed a,b. Secant-difference preserves q113952 source three stages; authored bank: correct -a cot-b sec, cot sign error, sec sign error, cot→tan, retain sec tan product. Sine-difference preserves q71666 recall/split/substitute/simplify stages but uses an independent authored bank: correct -cos+a cot, cosine sign error, cot sign error, wrong sine primitive -sin+a cot, cot→tan. Its final two malformed source options are never implicitly completed. Reverse-product conservatively generalizes q49093 input to csc(a csc-b cot); authored solution follows canonical e385 and q49121 distribution/split/extraction/substitution/simplification; bank is correct -a cot+b csc, wrong cot sign, wrong csc sign, cot→tan, csc→cot.

Normal hard three-term preserves q113958 source order and all three operative rows. Positive a,b,c in1..9 scale sec tan, negative csc² and positive sin respectively. Its missing-field radio completion is authored: correct a sec+b cot-c cos, individual sign reversal in each primitive, and full sign reversal. Source sin recall argument x is supplied only in normal completion and supported-correction verification; exact raw evidence remains unchanged. No difficultly is inferred for the source; it is captured hard.

Source errors are in source-defects.json. Source replay fidelity37/37 value bytes (including2 undefined expressions) is a separate claim from mathematics35/35 defined values checked. The missing sin argument cannot be differentiated as printed; its explicit completion is separately derivative-checked. Undefined v(t) raw prompt is not a self-contained mathematical task and must not be served.

Every served primitive is derived first by a finite lesson table from actual printed integrand, then the complete selected bank is constructed. All distractors must differentiate to a different input and all pairs must represent distinct antiderivative families, modulo C; +constant distractors are rejected. Validation interprets each formal integral on each displayed row and compares derivatives, then separately checks ordered teaching stages.

Domain: connected real intervals excluding sin(variable)=0 and all cos(variable)=0 poles introduced by the input or options. Primitive comparisons are local to those intervals. Mathematical fingerprints expand the actual input and alpha-rename its variable; unused parameters, seed, label, bank and C never add task novelty. Content identities include the actual full field layouts/values/designations/solution/difficulty and generator version, keeping distinct banks separate. All parameters are guarded in public calls. There are no plots and no answer-specific feedback.
