# Template extraction

## 1. Specific original records

Each record is retained at frozen basis 2275 in source.json. observed_raw is evidence-only and returns the exact record including original question/field/answer identities, complete banks, raw Markdown, all available attrs and all absent attrs. It does not invent missing metadata. Normal source-pattern instances use the explicitly defined original masks and complete parameterized recipes below. All original feedback is absent and remains absent.

### q-30990

Find $\frac{df}{dx}$ for $f(x) = 8\tan x - 3x$.

Original parameters {'a': 8, 'b': 3}. Difficulty absent; field :answer-field.type/radio; key selection.

f(x)=a tan(x)−b x. Radio whole derivative. Captured unrated source has no solution or key. Unique mathematically correct third choice is authored as a repair, together with easy difficulty and full formal derivative/sum-and-constant stage/result. Source csc errors are just bank values; their derivative formulas are not taught or required.

| Original choice identity | Exact captured complete value | Parameterized recipe | Captured correct? |
|---|---|---|---|
| bc30ef38-cbec-55b9-a2fa-eac62f6febaf | `-8\csc^{2} x - 3x` | −a csc²(x)−bx | designation absent |
| d639cc01-99a5-5305-b28d-b0e55d5fff5d | `-8\sec^{2} x - 3x` | −a sec²(x)−bx | designation absent |
| 4360cf12-9eb7-5492-ba39-14a61f0ea3ed | `8\sec^{2} x - 3` | a sec²(x)−b | designation absent |
| 5374242e-ca7e-5305-910c-cf4057c4f398 | `8\csc^{2} x + 3` | a csc²(x)+b | designation absent |
| 74e8baf7-d99f-5f98-8217-2cecba703059 | `8\csc x - 3` | a csc(x)−b | designation absent |

### q-47905

Find $f^{′}(x)$ for $f(x) = \tan x - 2\sin x$.

Original parameters {'a': 1, 'b': 2}. Difficulty absent; field :answer-field.type/radio; key selection.

f(x)=a tan(x)−b sin(x). Radio whole derivative. Captured unrated source has no solution or key. Unique correct second choice is authored as a repair, together with easy difficulty and full formal derivative/sum-and-constant stage/result.

| Original choice identity | Exact captured complete value | Parameterized recipe | Captured correct? |
|---|---|---|---|
| adc7af23-27d3-5800-85f7-40e2e95401d0 | `\sec x - 2\cos x` | a sec(x)−b cos(x) | designation absent |
| c2f5c0af-db3f-55ac-8c07-d38d151f1a43 | `\sec^{2} x - 2\cos x` | a sec²(x)−b cos(x) | designation absent |
| d514319d-4a07-51e2-af80-85110a494628 | `\sec x + 2\cos x` | a sec(x)+b cos(x) | designation absent |
| 1e8937f1-c9a6-5053-b5a8-e4ec71c26952 | `\sec^{2} x + 2\cos x` | a sec²(x)+b cos(x) | designation absent |
| 371011a2-7f50-5ecd-b514-127e20613ac6 | `-\sec^{2} x + 2\cos x` | −a sec²(x)+b cos(x) | designation absent |

### q-103081

The derivative of $y=x-\operatorname{tan}⁡x$ when $x=\frac{\pi }{4}$ is

Original parameters {'a': 1, 'b': 1}. Difficulty :question.difficulty/moderate; field :answer-field.type/radio; key selection.

y=bx−a tan(x), evaluation input pi/4. Radio derivative value. Stages: formal derivative; b−a sec²(x); substitute actual pi/4; use sec(pi/4)=sqrt(2); square and collect b−2a. Fixed source target is a conservative replay policy, not an intrinsic method restriction.

| Original choice identity | Exact captured complete value | Parameterized recipe | Captured correct? |
|---|---|---|---|
| 32e29ce2-4554-5558-8c72-8422675e24c1 | `3` | b+2a | False |
| 3c164c19-1e2a-5b97-a1d5-77c725311763 | `1` | b | False |
| 66361318-9219-58c5-bcda-75129baaa714 | `1-\sqrt{2}` | b−a sqrt(2) | False |
| 8d01f3a1-7ccb-5a54-ae3f-83fd2498b7ea | `-3` | −b−2a | False |
| b7289c68-237a-522e-b56e-57064d776048 | `-1` | b−2a | True |

### q-17912

Calculate the instantaneous rate of change of the function $f(x)=-tan⁡x$ when $x=\pi .$

Original parameters {'a': 1}. Difficulty :question.difficulty/moderate; field :answer-field.type/radio; key selection.

f(x)=−a tan(x), evaluation input pi. Radio derivative value. Stages: formal derivative; −a sec²(x); substitute pi; sec(pi)=−1 squared; simplify −a. Historical incorrect radical values retain their full observed patterns.

| Original choice identity | Exact captured complete value | Parameterized recipe | Captured correct? |
|---|---|---|---|
| 7b4dddb2-8ce0-518b-941e-482ca5265f7c | `-1` | −a | True |
| bc54686a-049f-5040-b7a9-b8062cc1c750 | `-\sqrt{2}` | −a sqrt(2) | False |
| be37be01-215e-5391-bca4-f872aefba533 | `\frac{1}{\sqrt{3}}` | a/sqrt(3) | False |
| ea403761-0f48-5b27-a322-4bdbfaf43080 | `\sqrt{2}` | a sqrt(2) | False |
| f3762c53-5b99-5615-8c9e-e78f50dd46f8 | `1` | a | False |

### q-341495

Find ${f}^{′}(x)$ if $f(x)=4\sqrt{x}+3tan⁡x.$

${f}^{′}(x)=$
{{field-1}}

Original parameters {'a': 4, 'b': 3}. Difficulty :question.difficulty/easy; field :answer-field.type/blank; key field-1.

f(x)=a sqrt(x)+b tan(x). Blank is the whole derivative RHS. Stages: formal derivative of the supplied sum; distribute a,b to individual formal derivatives; apply sqrt and tangent derivative formulas; simplify the radical coefficient. Positive radical branch x>0, cos(x)≠0.

| Original choice identity | Exact captured complete value | Parameterized recipe | Captured correct? |
|---|---|---|---|
| f7cb390c-e572-53a0-b9de-83c29e711d66 | `\frac{2}{\sqrt{x}}+3{sec}^{2}x` | a/(2 sqrt(x))+b sec²(x) | True |

### q-341825

Calculate the instantaneous rate of change of the function $f(x)=\operatorname{tan}⁡x-{x}^{2}$ when $x=0.$

${f}^{′}(0)=$
{{field-1}}

Original parameters {'a': 1, 'b': 1}. Difficulty :question.difficulty/moderate; field :answer-field.type/blank; key field-1.

f(x)=a tan(x)−b x² at zero. Blank f′(0). Stages: derivative; a sec²(x)−2bx; substitute zero; sec(0) via reciprocal cosine; evaluate cos(0)=1; simplify to a. b remains a real supplied-expression slot even though the derivative value at zero is independent of it.

| Original choice identity | Exact captured complete value | Parameterized recipe | Captured correct? |
|---|---|---|---|
| a4265357-1f5a-572b-b951-6c8731bedf0a | `1` | a | True |

### q-341858

Find the slope of $y=tan⁡x+2sin⁡x$ at $x=0.$

${y}^{′}(0)=$
{{field-1}}

Original parameters {'a': 1, 'b': 2}. Difficulty :question.difficulty/moderate; field :answer-field.type/blank; key field-1.

y=a tan(x)+b sin(x) at zero. Blank y′(0). Stages: derivative; a sec²(x)+b cos(x); evaluate zero; use sec²(0)=cos(0)=1; collect a+b.

| Original choice identity | Exact captured complete value | Parameterized recipe | Captured correct? |
|---|---|---|---|
| 5bcc3b9e-9aa6-5680-ac1b-555091e408db | `3` | a+b | True |

### q-47983

Find the derivative of $y=\sqrt{x}+tan⁡x.$

Original parameters {'a': 1, 'b': 1}. Difficulty :question.difficulty/easy; field :answer-field.type/radio; key selection.

y=a sqrt(x)+b tan(x). Radio asks for the whole derivative. Stages: derivative of supplied sum; a/(2 sqrt(x))+b sec²(x); combine over 2 sqrt(x). Distractor profiles change tangent coefficient, tangent input to sqrt(x), spurious x factor, or secant power. These are explicit observed expression patterns; their historical error intent is not claimed recovered. x>0 and cos(x)≠0.

| Original choice identity | Exact captured complete value | Parameterized recipe | Captured correct? |
|---|---|---|---|
| 026a56b8-1115-5684-ac6e-ef1630e64970 | `\frac{1+\sqrt{x}{sec}^{2}⁡x}{2\sqrt{x}}` | (a+b sqrt(x) sec²(x))/(2 sqrt(x)) | False |
| 0393bd6c-c00c-5794-bb05-1c8299be09b2 | `\frac{1+2{sec}^{2}⁡\sqrt{x}}{2\sqrt{x}}` | (a+2b sec²(sqrt(x)))/(2 sqrt(x)) | False |
| 25ff194a-cfcd-58a0-adba-8bc91fdf1efe | `\frac{1+2x{sec}^{2}⁡x}{2\sqrt{x}}` | (a+2b x sec²(x))/(2 sqrt(x)) | False |
| 44d191be-38a4-500e-8cfb-76a9d83fe2e6 | `\frac{1+2\sqrt{x}sec⁡x}{2\sqrt{x}}` | (a+2b sqrt(x) sec(x))/(2 sqrt(x)) | False |
| 9336f84c-bb60-54b1-ba79-495700d341f9 | `\frac{1+2\sqrt{x}{sec}^{2}⁡x}{2\sqrt{x}}` | a/(2 sqrt(x))+b sec²(x) | True |

### q-70911

Find ${y}^{′}$ for $y=3({x}^{2}-2tan⁡x)+4.$

Original parameters {'a': 3, 'b': 2, 'c': 4}. Difficulty :question.difficulty/easy; field :answer-field.type/radio; key selection.

y=a(x²−b tan(x))+c. Radio asks y′. Stages: formal derivative of original parentheses; expand outer a; differentiate expanded terms; simplify. Every bank expression retains its source’s distinct x/constant/power pattern. cos(x)≠0.

| Original choice identity | Exact captured complete value | Parameterized recipe | Captured correct? |
|---|---|---|---|
| 15d90aaf-3c7e-502e-a562-e8e30a2e4f44 | `6-3{cos}^{2}⁡x+4` | 2a−a cos²(x)+c | False |
| 54e94de8-7041-5cb7-8ea3-b142551e7f53 | `3-6{sec}^{2}⁡x` | a−ab sec²(x) | False |
| 962192cb-bb3f-5f88-bfc0-61f615078d44 | `6x-2{sec}^{2}⁡x` | 2ax−b sec²(x) | False |
| ab1f8bc7-61bf-53fe-b692-8455b9959c1b | `6x-6{sec}^{2}⁡x` | 2ax−ab sec²(x) | True |
| fb2a1768-76da-50c5-bba8-68baff7dd8fd | `x-3sec⁡x+4` | x−a sec(x)+c | False |

## 2. Generalized backbone and scope

Differentiate the actual displayed tangent expression using the sum, constant multiple and power rules and the learned sin/cos/tan rules. Preserve the displayed variable x, function/prime notation, requested complete derivative or derivative-at-point, response field, original operative stage order and concrete evaluation target. For moderate, compute the derivative before substituting the actual input. Original masks remain separate by field type, supplied functions and operative layout. Every original answer bank is selected as one whole profile, not a pool of errors.

## 3. Components and parameter dependencies

Source-pattern normal masks are parameterized by a,b,c and rendered from the original complete prompt/solution strings using full mathematical component substitutions. Numeric derivative-at-point banks are rendered field-by-field, never by global digit replacement. Coefficients appearing in derivatives, expanded expressions, evaluated terms and final prose all depend on the same supplied expression. The 1 coefficient suppresses itself where the source did; no cosmetic label/option shuffle is used for variation. The two unrated repairs retain the captured exact prompt backbone and full mathematical banks but add only explicitly authored difficulty, key and same-method solution. No option-specific feedback is invented.

A recipe is the complete mathematical expression printed above, including changed powers, constants, coefficients and operator inputs. q-47983’s second option differentiates a tangent at sqrt(x), not at x; its full input remains part of the recipe. q-70911’s five banks preserve their compound wrong operations and retained constants exactly. Ambiguity rejects an entire bank. In particular, a=1 in q-70911 makes the third choice equal its correct fourth choice, so those radio instances are rejected. No fallback radio-to-blank conversion occurs. Every source bank is fully replayed at its original parameters and changed parameters, including both incomplete source banks; only original captured designations are counted as recovered keys.

The authored moderate point family supplies bx−a tan(x) at a regular point. Its correct answer is b−a sec²(t). Its whole bank uses correct; tangent-derivative sign error b+a sec²(t); omit tangent derivative b; omit secant square b−a sec(t); negate both derivative components −b−a sec²(t). Some familiar points make that five-value bank ambiguous; radios reject those entire combinations, while separately authored blanks may use them. The emitted solution has actual formal input, constant-multiple formal stage, derivative result, explicit point substitution, component evaluation and final exact answer. The moderate point slot has a changed-input test with a=2,b=3 held fixed.

The authored hard expression is a(tan(x)+b sin(x)−c cos(x))+d x^n. Correct derivative is a(sec²(x)+b cos(x)+c sin(x))+dn x^(n−1). Its complete bank changes sec² to sec; keeps the erroneous negative cosine-derivative sign; omits power multiplier n; or omits outer factor a on all three trig derivatives. These are independently authored method errors, explicitly separate from observed banks. Its actual formal input is differentiated independently, then the solution distributes coefficients to the four formal derivatives and gives the concrete result. Hard is a bounded workload extension in the same KP’s learned rules; there is no source hard difficulty claim.

## 4. Slots, bounds, domains and identities

All complete source coefficients a,b,c range over positive integers 1..6. q-30990 allows a 1..8 so its original coefficient 8 is included; b stays 1..6. Every declared coefficient is enforced exactly and extra/missing/fractional/unbounded parameters reject. q-70911’s additive constant c changes the actual supplied expression but does not add differentiation workload; it is not counted as a fresh derivative target by itself. All source evaluation targets remain at their captured points to preserve their exact operative sequence; this conservative policy is extended explicitly by the authored point family.

Authored moderate a,b range 1..6 and point∈{0,pi/4,−pi/4,pi,−pi}. These are all regular unit-circle points supported by the topic’s prerequisite. Hard a∈{2,3,4}, b,c,d∈{1,2,3}, n∈{2,3,4}. a excludes 1 so the distribution-error bank remains meaningful. Every hard trig and polynomial component is present; n is an actual supplied polynomial exponent and all subsequent derivative powers/coefficient stages must change together. No tan argument other than x appears in an eligible prompt. The derivative-at-point stages separately use the actual chosen point. Coefficient and exponent changes remain within comparable arithmetic workload at each difficulty.

Domain is real x with cos(x)≠0 for tangent expressions. Radical masks also require x>0 for their derivative; the original sqrt function at zero does not provide a finite derivative there. Every evaluation input is regular and explicitly checked. Distractor values are read as complete expressions; the q-47983 sqrt(x) input and csc distractors are permitted only as incorrect banks, not supplied-function branches. Secant poles are never valid evaluation points.

Mathematical task fingerprints depend on actual expanded supplied expression and actual evaluation input, not seed, identities, fields, option order, aliases or bank selection. A constant-only change in q-70911 is not a new assessed derivative task: the validator’s distinct derivative-task counts remove additive constants for unevaluated derivative requests, while the content identity still retains the supplied prompt. Source field contract/solution/backbone is fixed. Content identities depend on normalized prompt, full solution, difficulty, field layout, complete bank and correct designation. Answer identities belong to their field.

## Source omissions and supported presentation repairs

q-30990 and q-47905 omit difficulty, key and worked solution. Exact observed_raw preserves all omissions and is ineligible; normal source-pattern repairs independently author easy assignment, infer the unique mathematical key and supply the three same-method derivative stages. No missing metadata is described as recovered source evidence.

The frozen bank values for q-341495 and q-47983 have actual two-backslash command tokens before frac/sqrt. This is checked on the deserialized string rather than inferred from JSON appearance. Raw evidence keeps them. Served normal values repair only two-backslash frac/sqrt command prefixes to one canonical slash before shared normalization. Complete mathematical banks are compared separately from typography. Raw question/problem and solution layouts are retained for all seven complete source cases; shared normalize_prose is applied before served IDs. Bare answer values contain no dollar delimiters. No other source math errors were identified. Original feedback/unknown attrs remain solely exact evidence when not part of the standard generated serving record; source absence of feedback remains absence in normal output.
