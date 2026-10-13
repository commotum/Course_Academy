# Source components and extracted templates

Every original source is retained in source.json and source.edn. Positive amplitude transport k multiplies the complete function and every choice. This is an explicit narrow sampling policy, not an inferred distractor misconception. k=1 replays the original bank; k=2..12 supplies stock. Every profile is kept separate. Blank values have no distractors. All variables are real; negative powers require x != 0. Slope point stays pi/6. Coefficient signs, exact fractions, operator structure and field shapes remain fixed under transport. Constants alone, seed and order are not distinct questions.

## q-47906

Excluded from supported generation; see classification and exact source evidence.

Prompt: Find $\frac{d}{dx}(5\cos x - \sin x)$.

Field selection, :answer-field.type/radio.

- Source answer ac9634ef-7d12-5fc7-8486-2002f0e1b8ed: `-5\cos x - \sin x`; excluded; preserved without recipe implementation.
- Source answer ddf9d360-ecae-5c9e-add7-78fe278e27ec: `-5\sin x + \cos x`; excluded; preserved without recipe implementation.
- Source answer 0f0dde70-457d-5a46-bc08-91d7ac21d219: `-5\tan x - \cos x`; excluded; preserved without recipe implementation.
- Source answer 4379eca7-3b91-591d-9449-1811c5ba0348: `-\sin x - 5\cos x`; excluded; preserved without recipe implementation.
- Source answer 508dcb97-0602-5582-91d6-429a0c4dd46f: `-5\sin x - \cos x`; excluded; preserved without recipe implementation.

Worked solution: absent; not inferred for source

## q-47908

Excluded from supported generation; see classification and exact source evidence.

Prompt: Find the derivative of $y = \frac{\cos x}{8} - \frac{\sin x}{4}$.

Field selection, :answer-field.type/radio.

- Source answer a436ea41-7313-5f7c-9e5e-d7cf92a31fc9: `-\frac{2\sin x + \cos x}{8}`; excluded; preserved without recipe implementation.
- Source answer a5c29a6a-9465-540f-9e67-a9a86fe45e11: `-\frac{\sin x + 2\cos x}{8}`; excluded; preserved without recipe implementation.
- Source answer 309d2c30-5a79-5940-9d8f-f1c473e37e97: `\frac{\sin x + 2\cos x}{8}`; excluded; preserved without recipe implementation.
- Source answer 72172321-c1b7-54ae-8b91-b2981e5b8f5f: `-\frac{\sin x + \cos x}{8}`; excluded; preserved without recipe implementation.
- Source answer 7cef5fd1-fd37-5e84-8a6c-a2ed441e0417: `\frac{\sin x - 2\cos x}{8}`; excluded; preserved without recipe implementation.

Worked solution: absent; not inferred for source

## q-167324

Excluded from supported generation; see classification and exact source evidence.

Prompt: $\frac{\text{d}h}{\text{d}x}\,=$

                            
                                    
                            
                                        {{field-1}}

Field field-1, :answer-field.type/blank.

- Source answer f82a959f-469c-580d-b699-744a01e1a73e: `-4\operatorname{cos}x`; excluded; preserved without recipe implementation.

Worked solution: We know that 

$$
\,\frac{\text{d}}{\text{d}x}(\operatorname{sin}⁡x)=\operatorname{cos}⁡x.
$$

Applying this formula and the constant multiple rules, we have

$$
\begin{aligned}\frac{\text{d}h}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(-4\operatorname{sin}⁡x) \\  & =-4\cdot \frac{\text{d}}{\text{d}x}(\operatorname{sin}⁡x) \\  & =-4\cdot (\operatorname{cos}⁡x) \\  & =-4\operatorname{cos}⁡x.\end{aligned}
$$

## q-167778

Excluded from supported generation; see classification and exact source evidence.

Prompt: $\frac{\text{d}h}{\text{d}x}\,=$

                            
                                    
                            
                                        {{field-1}}

Field field-1, :answer-field.type/blank.

- Source answer bff132e5-2ee2-59aa-8aea-3502c866b4de: `-4\operatorname{cos}(x)`; excluded; preserved without recipe implementation.

Worked solution: We know that 

$$
\,\frac{\text{d}}{\text{d}x}(\operatorname{sin}⁡(x))=\operatorname{cos}⁡(x).
$$

Applying this formula and the constant multiple rules, we have

$$
\begin{aligned}\frac{\text{d}h}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(-4\operatorname{sin}⁡(x)) \\  & =-4\cdot \frac{\text{d}}{\text{d}x}(\operatorname{sin}⁡(x)) \\  & =-4\cdot (\operatorname{cos}⁡(x)) \\  & =-4\operatorname{cos}⁡(x).\end{aligned}
$$

## q-1847

Two terms: 4 cos(x)+2 sin(x); derivative display, radio selection, 5 choices. Correct 2 cos(x)-4 sin(x). Solution recalls sine/cosine derivatives, applies each coefficient, collects terms.

Prompt: $\frac{\text{d}}{\text{d}x}(4cos⁡x+2sin⁡x)=$

Field selection, :answer-field.type/radio.

- Source answer 203dab4a-3058-5e0e-90fa-52dcc35d2407: `4cos⁡x+2sin⁡x`; transport recipe `k * (4cos⁡x+2sin⁡x)` at source k=1, profile q-1847. Exact complete value replay required.
- Source answer 46da0d85-3682-54d0-b58f-5f7b61e746ee: `2cos⁡x+4sin⁡x`; transport recipe `k * (2cos⁡x+4sin⁡x)` at source k=1, profile q-1847. Exact complete value replay required.
- Source answer 55c1f225-5772-53df-9957-91ede62f7763: `2cos⁡x-4sin⁡x`; transport recipe `k * (2cos⁡x-4sin⁡x)` at source k=1, profile q-1847. Exact complete value replay required.
- Source answer 66e054b3-95bb-5323-86e6-76b98c6154cc: `-4cos⁡x-2sin⁡x`; transport recipe `k * (-4cos⁡x-2sin⁡x)` at source k=1, profile q-1847. Exact complete value replay required.
- Source answer 92c0eef2-67dc-58fb-baa0-cc77ea56c821: `4cos⁡x-2sin⁡x`; transport recipe `k * (4cos⁡x-2sin⁡x)` at source k=1, profile q-1847. Exact complete value replay required.

Worked solution: We know that $\frac{\text{d}}{\text{d}x}(sin⁡x)=cos⁡x,$ and that $\frac{\text{d}}{\text{d}x}(cos⁡x)=-sin⁡x.$ Applying these formulas, we have

$$
\begin{aligned}\frac{\text{d}}{\text{d}x}(4cos⁡x+2sin⁡x) & =4(-sin⁡x)+2(cos⁡x) \\  & =2cos⁡x-4sin⁡x.\end{aligned}
$$

## q-1900

Tangent slope for 2x-5 cos(x) at pi/6; 5-choice radio. Differentiate to 2+5 sin(x), substitute pi/6, use sin(pi/6)=1/2, simplify to 9/2. Profile includes unexplained scalar offsets/denominators; preserve observed mathematical pattern without guessing learner mistakes.

Prompt: What is the slope of the tangent line to the curve $y=2x-5cos⁡x$ at the point $x=\frac{\pi }{6}?$

Field selection, :answer-field.type/radio.

- Source answer 04fa2ca0-5410-5738-8228-11c0d9ec4e4e: `\frac{11}{2}`; transport recipe `k * (\frac{11}{2})` at source k=1, profile q-1900. Exact complete value replay required.
- Source answer 21163962-dbce-5c4a-9b9a-9ca9a5b9852a: `\frac{21}{5}`; transport recipe `k * (\frac{21}{5})` at source k=1, profile q-1900. Exact complete value replay required.
- Source answer 3b82e03f-7320-5fd8-aa40-e2facea3ab8c: `-\frac{21}{6}`; transport recipe `k * (-\frac{21}{6})` at source k=1, profile q-1900. Exact complete value replay required.
- Source answer 9eea7b77-2513-5960-bc9f-8572e987d50f: `\frac{9}{2}`; transport recipe `k * (\frac{9}{2})` at source k=1, profile q-1900. Exact complete value replay required.
- Source answer e5038023-5b22-563c-be39-21b7f5c99eca: `\frac{9}{4}`; transport recipe `k * (\frac{9}{4})` at source k=1, profile q-1900. Exact complete value replay required.

Worked solution: The slope at $x=\frac{\pi }{6}$ is given by the value of the derivative ${y}^{′}$ at $x=\frac{\pi }{6}.$ 

First, we compute the derivative, using the fact that $\frac{\text{d}}{\text{d}x}(cos⁡x)=-sin⁡x.$ We get

$$
\begin{aligned}{f}^{′}(x) & =\frac{\text{d}}{\text{d}x}(2x-5cos⁡x) \\  & =2-5(-sin⁡x) \\  & =2+5sin⁡x.\end{aligned}
$$

Evaluating at $x=\frac{\pi }{6},$ we get

$$
\begin{aligned}{f}^{′}(30) & =2+5sin⁡(\frac{\pi }{6}) \\  & =2+5(\frac{1}{2}) \\  & =2+\frac{5}{2} \\  & =\frac{9}{2}.\end{aligned}
$$

Therefore,  the instantaneous rate of change is $\frac{9}{2}.$

## q-30991

Factored 6(x^2-cos(x))+5; 5-choice radio. Differentiate to 6*2x+6 sin(x)+0, then collect 12x+6 sin(x). Preserve constant term in source/amplitude policy, but ignore it for novelty.

Prompt: Find $\frac{\text{d}y}{\text{d}x}$ for $y=6({x}^{2}-cos⁡x)+5.$

Field selection, :answer-field.type/radio.

- Source answer 0eda8d71-b593-5d95-86c9-5bba5f41ecdd: `12x+6sin⁡x`; transport recipe `k * (12x+6sin⁡x)` at source k=1, profile q-30991. Exact complete value replay required.
- Source answer 9cdb325f-ae0b-5a49-b609-cab3e9c25d86: `6x+6sin⁡x`; transport recipe `k * (6x+6sin⁡x)` at source k=1, profile q-30991. Exact complete value replay required.
- Source answer a190184d-f11f-593d-b408-9b37e070ca95: `12x-6sin⁡x`; transport recipe `k * (12x-6sin⁡x)` at source k=1, profile q-30991. Exact complete value replay required.
- Source answer d3db1a2e-d54f-5696-906b-c48583e1acb5: `12x-sin⁡x`; transport recipe `k * (12x-sin⁡x)` at source k=1, profile q-30991. Exact complete value replay required.
- Source answer ef4b1b52-780c-57c9-9707-2dacfce41710: `12x+sin⁡x`; transport recipe `k * (12x+sin⁡x)` at source k=1, profile q-30991. Exact complete value replay required.

Worked solution: We know that $\frac{\text{d}}{\text{d}x}(cos⁡x)=-sin⁡x.$ Applying this formula, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(6({x}^{2}-cos⁡x)+5) \\  & =6\cdot 2x+6sin⁡x+0 \\  & =12x+6sin⁡x.\end{aligned}
$$

## q-341383

5 sin(x)/4+x^4/4; exact blank RHS of derivative equation with field-1. Apply constant and power rules to get 5 cos(x)/4+x^3. No distractors.

Prompt: Find the derivative of $y=\frac{5sin⁡x}{4}+\frac{{x}^{4}}{4}.$

$\frac{\text{d}y}{\text{d}x}=$
{{field-1}}

Field field-1, :answer-field.type/blank.

- Source answer 4888f926-ac9b-5bbc-8435-71b677b35500: `\frac{5\operatorname{cos}x}{4}+{x}^{3}`; transport recipe `k * (\frac{5\operatorname{cos}x}{4}+{x}^{3})` at source k=1, profile q-341383. Exact complete value replay required.

Worked solution: We know that $\frac{\text{d}}{\text{d}x}(sin⁡x)=cos⁡x.$ Applying this formula, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(\frac{5sin⁡x}{4}+\frac{{x}^{4}}{4}) \\  & =\frac{5}{4}(cos⁡x)+\frac{1}{4}(4{x}^{3}) \\  & =\frac{5cos⁡x}{4}+{x}^{3}.\end{aligned}
$$

## q-47985

-2 cos(x)+x^-2; 5-choice radio. Differentiate to -2(-sin(x))+(-2)x^(-2-1), simplify to 2 sin(x)-2x^-3. Domain x != 0.

Prompt: Find the derivative of $y=-2cos⁡x+{x}^{-2}.$

Field selection, :answer-field.type/radio.

- Source answer 58178d4f-4abd-58b7-80f3-235da8563710: `2sin⁡x-2{x}^{-1}`; transport recipe `k * (2sin⁡x-2{x}^{-1})` at source k=1, profile q-47985. Exact complete value replay required.
- Source answer 6e8ba3a3-8163-54a7-a89c-617f3758ea02: `-2sin⁡x-2{x}^{-3}`; transport recipe `k * (-2sin⁡x-2{x}^{-3})` at source k=1, profile q-47985. Exact complete value replay required.
- Source answer abf48582-4f98-5a96-ba7c-6645540d8053: `2sin⁡x-2{x}^{-3}`; transport recipe `k * (2sin⁡x-2{x}^{-3})` at source k=1, profile q-47985. Exact complete value replay required.
- Source answer b8c3ad30-bf9c-5740-9f1f-85721ef68822: `-2sin⁡x+2{x}^{-3}`; transport recipe `k * (-2sin⁡x+2{x}^{-3})` at source k=1, profile q-47985. Exact complete value replay required.
- Source answer fb5d65e6-8cdc-5871-afa6-4d5b3c079a97: `-2sin⁡x-2{x}^{-2}`; transport recipe `k * (-2sin⁡x-2{x}^{-2})` at source k=1, profile q-47985. Exact complete value replay required.

Worked solution: We know that $\frac{\text{d}}{\text{d}x}(cos⁡x)=-sin⁡x.$ Applying this formula, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & =\frac{\text{d}}{\text{d}x}(-2cos⁡x+{x}^{-2}) \\  & =-2(-sin⁡x)+(-2){x}^{-2-1} \\  & =2sin⁡x-2{x}^{-3}.\end{aligned}
$$

## Generalized template

Task: differentiate k times the source function using the sum, constant multiple, sine/cosine and power rules; for moderate, evaluate the derivative at pi/6. Variable components are coefficients and answer values, linked by exact SymPy calculations. Fixed components: original functional terms/exponents/arguments, slope point, field key/type/count, full profile membership, recalled formulas and the original operation sequence. For k>1 render expanded individual term derivatives and collect them; for moderate additionally show substitution and special-angle evaluation. This simplified aligned layout is an explicit rendering change. At k=1 the prompt, all choices and field shape are exact source replay; source solutions retained except the documented q-1900 label correction.

Finite bounds: k integer in 1..12, positive only. Signed coefficients and rational coefficients observed in the supported source tasks remain covered; independent coefficient variation, argument shifts and chain rules are outside this package. q-1900 profile recipes at k are [11k/2,21k/5,-21k/6,9k/2,9k/4]; interpretation unresolved, exact expressions preserved. Source order is retained. Correct answer designated by exact derivative equivalence; all distractor pairs must be non-equivalent.
