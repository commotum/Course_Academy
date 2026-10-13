# Template extraction

Fixed prose, exact source notation and layout are preserved by simultaneous numerical substitution in the script. Complete original component evidence follows. Changed values are numerical variants within these templates; not additional templates.

Sampling extension: integer k=2..12; c=1..6; b=-5..5. Coefficients originally observed are retained. For q-9942 k=2 is invalid because bank choices coincide. All three singleton profiles replay only; no inference from unexplained numerical distractors.

Each choice retains original source field identity only as evidence. Generated answer UUIDs are owned by the new field. Templates without complete source field data or standalone context are excluded, never repaired in the served original.

## q-11599

Incomplete source: missing difficulty, solution, field, bank or correct designation. Do not reconstruct field shape or grade identity by guessing.

Prompt:

If $y = x^{3}(2x^{2} + 1)^{3}$, find $\frac{dy}{dx}$.

Fixed worked solution:

(missing)

Exact field components, source choices and canonical designation:

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "3e1e3fd3-5561-53bf-af94-2a5a56a62b18",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "(12x^{4} + x^{2})(2x^{2} + 1)^{2}",
        ":db/id": 17592186093867
      },
      {
        ":answer/id": "529892d3-fe64-52a5-9433-8978cd66fb3b",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "(12x^{4} + 3x^{2})(2x^{2} + 1)^{2}",
        ":db/id": 17592186093868
      },
      {
        ":answer/id": "5a109ebf-3786-5269-8945-bc9bc7404324",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "(18x^{4} + 3x^{2})(2x^{2} + 1)^{3}",
        ":db/id": 17592186093869
      },
      {
        ":answer/id": "68c92ca2-1813-5e7f-851a-bc0bbc3787a8",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "(18x^{4} + 3x^{2})(2x^{2} + 1)^{2}",
        ":db/id": 17592186093870
      },
      {
        ":answer/id": "6a4336dc-86ac-5e7f-88fc-c903df1cb1eb",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "(3x^{4} + 12x^{2})(2x^{2} + 1)^{2}",
        ":db/id": 17592186093871
      }
    ],
    ":answer-field/id": "66469be4-8083-5074-a455-8084fdaf504e",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186093866
  }
]
```

## q-31240

Incomplete source: missing difficulty, solution, field, bank or correct designation. Do not reconstruct field shape or grade identity by guessing.

Prompt:

Find the slope of $y = 2x\cos (2x + 3)$ at $x =-1$.

Fixed worked solution:

(missing)

Exact field components, source choices and canonical designation:

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "a44fe7a2-5e5a-5eb8-805d-7b829fc0d942",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2\\cos 1 + 2\\sin 1",
        ":db/id": 17592186095244
      },
      {
        ":answer/id": "b40b5c59-e2e7-53be-8069-7947875a60a6",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\cos 1 + 2\\sin 1",
        ":db/id": 17592186095245
      },
      {
        ":answer/id": "db1afcf3-0d9f-569f-a120-5478079a6104",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2\\cos 1 + \\sin 1",
        ":db/id": 17592186095246
      },
      {
        ":answer/id": "f98a997b-dd95-5cc3-9f1d-cafac532e26a",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2\\cos 1 + 4\\sin 1",
        ":db/id": 17592186095247
      },
      {
        ":answer/id": "48f9401d-07df-5bd6-beef-7e93a2c1e92b",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\cos 5 + 2\\sin 5",
        ":db/id": 17592186095248
      }
    ],
    ":answer-field/id": "9708991f-d3ee-5d1d-b2fe-2d10b43d24eb",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186095243
  }
]
```

## q-11602

Incomplete source: missing difficulty, solution, field, bank or correct designation. Do not reconstruct field shape or grade identity by guessing.

Prompt:

If $y=2{x}^{3}\sqrt{2{x}^{2}+7},$ find the value of $\frac{\text{d}y}{\text{d}x}$ at $x=2.$

Fixed worked solution:

This question requires the product rule. Let $u(x)=2{x}^{3}$ and $v(x)=\sqrt{2{x}^{2}+7}.$ Then

$$
{u}^{'}(x)=6{x}^{2},\,{v}^{'}(x)=\frac{2x}{\sqrt{2{x}^{2}+7}}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(6{x}^{2})(\sqrt{2{x}^{2}+7})+(2{x}^{3})(\frac{2x}{\sqrt{2{x}^{2}+7}}) \\  & =6{x}^{2}\sqrt{2{x}^{2}+7}+\frac{4{x}^{4}}{\sqrt{2{x}^{2}+7}}.\end{aligned}
$$

Therefore, the value of $\frac{\text{d}y}{\text{d}x}$ at $x=2$ is

$$
\begin{aligned}{(\frac{\text{d}y}{\text{d}x})|}_{x=2} & =6(2)^{2}\sqrt{2(2)^{2}+7}+\frac{4(2)^{4}}{\sqrt{2(2)^{2}+7}} \\  & =24\sqrt{15}+\frac{64}{\sqrt{15}} \\  & =\frac{360+64}{\sqrt{15}} \\  & =\frac{424}{\sqrt{15}}.\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[]
```

## q-11603

Incomplete source: missing difficulty, solution, field, bank or correct designation. Do not reconstruct field shape or grade identity by guessing.

Prompt:

If $y=3{x}^{2}{({x}^{3}-1)}^{4}$, find the value of $\frac{\text{d}y}{\text{d}x}$ at $x=1.$

Fixed worked solution:

This question requires the product rule. Let $u(x)=3{x}^{2}$ and $v(x)={({x}^{3}-1)}^{4}.$ Then

$$
{u}^{'}(x)=6x,\,{v}^{'}(x)=12{x}^{2}{({x}^{3}-1)}^{3}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(6x)(({x}^{3}-1)^{4})+(3{x}^{2})(12{x}^{2}({x}^{3}-1)^{3}) \\  & =6x({x}^{3}-1)^{4}+36{x}^{4}{({x}^{3}-1)}^{3} \\  & =(6x({x}^{3}-1)+36{x}^{4})\,{({x}^{3}-1)}^{3} \\  & =(6{x}^{4}-6x+36{x}^{4})\,{({x}^{3}-1)}^{3} \\  & =(42{x}^{4}-6x)\,{({x}^{3}-1)}^{3}.\end{aligned}
$$

To evaluate $\frac{\text{d}y}{\text{d}x}$ at $x=1$, we substitute $x=1:$

$$
\begin{aligned}{(\frac{\text{d}y}{\text{d}x})|}_{x=1} & =(42\cdot {1}^{4}-6\cdot 1){({1}^{3}-1)}^{3} \\  & =36\cdot 0 \\  & =0.\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[]
```

## q-11939

Incomplete source: missing difficulty, solution, field, bank or correct designation. Do not reconstruct field shape or grade identity by guessing.

Prompt:

Given that $y=x\operatorname{ln}3x,$ find $\frac{\text{d}y}{\text{d}x}.$

Fixed worked solution:

This question requires the product rule. Let $u(x)=x$ and $v(x)=\operatorname{ln}3x.$ Then

$$
{u}^{'}(x)=1,\,{v}^{'}(x)=\frac{1}{x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(1)(\operatorname{ln}3x)+(x)(\frac{1}{x}) \\  & =\operatorname{ln}3x+1.\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[]
```

## q-143518

Requires preceding multipart context: velocity function absent from standalone prompt

Prompt:

Find the acceleration function ${a}_{2}(t)$ of the second particle.

${a}_{2}(t)\,=\,$
{{field-1}}

Fixed worked solution:

In part 3, we saw that the derivative of a particle's velocity with respect to time gives its acceleration.

To differentiate ${v}_{2}(t),$ we require the product rule. Let $g(t)={t}^{2}$ and $h(t)=\operatorname{sin}(3t).$ Then

$$
{g}^{'}(t)=2t,\,{h}^{'}(t)=3\operatorname{cos}(3t).
$$

We used the chain rule to calculate ${h}^{'}(t).$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{a}_{2}(t) & ={v}_{2}^{'}(t) \\  & ={g}^{'}(t)\cdot h(t)+g(t)\cdot {h}^{'}(t) \\  & =(2t)(\operatorname{sin}(3t))+({t}^{2})(3\operatorname{cos}(3t)) \\  & =2t\operatorname{sin}(3t)+3{t}^{2}\operatorname{cos}(3t).\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "ec192c70-e569-50ff-8384-af86c7a4c091",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2t\\operatorname{sin}(3t)+3{t}^{2}\\operatorname{cos}(3t)",
        ":db/id": 17592186232208
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "ec192c70-e569-50ff-8384-af86c7a4c091",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "2t\\operatorname{sin}(3t)+3{t}^{2}\\operatorname{cos}(3t)",
      ":db/id": 17592186232208
    },
    ":answer-field/id": "591ef578-25d3-5e0e-9800-62864943c1c1",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232207
  }
]
```

## q-16698

Incomplete source: missing difficulty, solution, field, bank or correct designation. Do not reconstruct field shape or grade identity by guessing.

Prompt:

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{x}\operatorname{cos}3x.$

Fixed worked solution:

This question requires the product rule. Let $u(x)={e}^{x}$ and $v(x)=\operatorname{cos}3x.$ Then

$$
{u}^{'}(x)={e}^{x},\,{v}^{'}(x)=-3\operatorname{sin}3x.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =({e}^{x})(\operatorname{cos}3x)+({e}^{x})(-3\operatorname{sin}3x) \\  & ={e}^{x}\operatorname{cos}3x-3{e}^{x}\operatorname{sin}3x \\  & ={e}^{x}(\operatorname{cos}3x-3\operatorname{sin}3x).\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[]
```

## q-313299

Incomplete source: missing difficulty, solution, field, bank or correct designation. Do not reconstruct field shape or grade identity by guessing.

Prompt:

Find the slope $m$ of the tangent line to the curve $y={x}^{2}\operatorname{sin}(2x)$ at $x=\frac{\pi }{4}.$

$m=$
{{field-1}}

Fixed worked solution:

To find the slope at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

This question requires the product rule. Let $u(x)={x}^{2}$ and $v(x)=\operatorname{sin}2x.$ Then

$$
{u}^{'}(x)=2x,\,{v}^{'}(x)=2\operatorname{cos}2x.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(2x)(\operatorname{sin}2x)+({x}^{2})(2\operatorname{cos}2x) \\  & =2x\operatorname{sin}2x+2{x}^{2}\operatorname{cos}2x.\end{aligned}
$$

Therefore, the slope $m$ at $x=\frac{\pi }{4}$ is

$$
\begin{aligned}m & ={(\frac{\text{d}y}{\text{d}x})|}_{x=\pi /4} \\  & =2(\frac{\pi }{4})\cdot \operatorname{sin}(2\cdot \frac{\pi }{4})+2{(\frac{\pi }{4})}^{2}\operatorname{cos}(2\cdot \frac{\pi }{4}) \\  & =\frac{\pi }{2}\cdot \operatorname{sin}(\frac{\pi }{2})+2\cdot \frac{{\pi }^{2}}{16}\cdot \operatorname{cos}(\frac{\pi }{2}) \\  & =\frac{\pi }{2}\cdot 1+\frac{{\pi }^{2}}{8}\cdot 0 \\  & =\frac{\pi }{2}.\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[
  {
    ":answer-field/id": "4aac1b00-ccaf-57eb-98c1-277328cf34e0",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232543
  }
]
```

## q-343333

e^(kx) ln(x), requested bracket k ln(x)+1/x; domain x>0. Original k=5. No distractors.

Prompt:

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{5x}\operatorname{ln}x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{5x}$

Fixed worked solution:

This question requires the product rule. Let $u(x)={e}^{5x}$ and $v(x)=\operatorname{ln}x.$ Then

$$
{u}^{'}(x)=5{e}^{5x},\,{v}^{'}(x)=\frac{1}{x}.
$$

Note that we used the chain rule to differentiate $u.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{'}(x)\cdot v(x)+u(x)\cdot {v}^{'}(x) \\  & =(5{e}^{5x})(\operatorname{ln}x)+({e}^{5x})\,(\frac{1}{x}) \\  & =(5\operatorname{ln}x+\frac{1}{x}){e}^{5x}.\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "05a14ea0-cb64-5f19-aac2-523068cc3521",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5\\operatorname{ln}x+\\frac{1}{x}",
        ":db/id": 17592186232899
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "05a14ea0-cb64-5f19-aac2-523068cc3521",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "5\\operatorname{ln}x+\\frac{1}{x}",
      ":db/id": 17592186232899
    },
    ":answer-field/id": "60ccd4ce-b471-58b7-b799-fc85b9ac5283",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232898
  }
]
```

## q-167572

Requires preceding multipart context: velocity function absent from standalone prompt

Prompt:

Find the acceleration function ${a}_{2}(t)$ of the second particle.

                            
                                    
                                        
                                            

                                                

                                        
                                        
                                        

                                    
                                
                                    
                                        
                                        ${a}_{2}(t)\,=\,$

                                    
                                
                                    
                            
                                        {{field-1}}

Fixed worked solution:

In part 3, we saw that the derivative of a particle's velocity with respect to time gives its acceleration.

To differentiate ${v}_{2}(t),$ we require the product rule. Let $g(t)=t$ and $h(t)=\operatorname{cos}⁡(\frac{t}{2}).$ Then

$$
{g}^{′}(t)=1,\,{h}^{′}(t)=-\frac{1}{2}\operatorname{sin}⁡(\frac{t}{2}).
$$

We used the chain rule to calculate ${h}^{′}(t).$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{a}_{2}(t) & ={v}_{2}^{′}(t) \\  & ={g}^{′}(t)\cdot h(t)+g(t)\cdot {h}^{′}(t) \\  & =(1)(\operatorname{cos}⁡(\frac{t}{2}))+(t)(-\frac{1}{2}\operatorname{sin}⁡(\frac{t}{2})) \\  & =\operatorname{cos}⁡(\frac{t}{2})-\frac{1}{2}t\operatorname{sin}⁡(\frac{t}{2}).\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "8d0654e0-d49d-534f-9b33-68e3e971d9e5",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\operatorname{cos}(t/2)-t/2\\operatorname{sin}(t/2)",
        ":db/id": 17592186234758
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "8d0654e0-d49d-534f-9b33-68e3e971d9e5",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\operatorname{cos}(t/2)-t/2\\operatorname{sin}(t/2)",
      ":db/id": 17592186234758
    },
    ":answer-field/id": "bdafbc71-e376-54dc-999f-eac8f84227b6",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186235208
  }
]
```

## q-10009

sin(2x)cos(3x), derivative evaluated at pi/2 is 0. Bank {-1,0,1,2,3} has unestablished parameter recipes; retain one exact observed task only. No seed variants.

Prompt:

Find the slope of $y=\operatorname{sin}⁡2x\operatorname{cos}⁡3x$ at $x=\frac{\pi }{2}.$

Fixed worked solution:

To find the slope at a given point, we have to find $\frac{\text{d}y}{\text{d}x}$ at that point.

This question requires the product rule. Let $u(x)=\operatorname{sin}⁡2x$ and $v(x)=\operatorname{cos}⁡3x.$ Then

$$
{u}^{′}(x)=2\operatorname{cos}⁡2x,\,{v}^{′}(x)=-3\operatorname{sin}⁡3x.
$$

Note that we used the chain rule to differentiate $u$ and $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2\operatorname{cos}⁡2x)(\operatorname{cos}⁡3x)+(\operatorname{sin}⁡2x)(-3\operatorname{sin}⁡3x) \\  & =2\operatorname{cos}⁡2x\operatorname{cos}⁡3x-3\operatorname{sin}⁡2x\operatorname{sin}⁡3x.\end{aligned}
$$

Therefore, the slope at $x=\frac{\pi }{2}$ is

$$
\begin{aligned}{(\frac{\text{d}y}{\text{d}x})|}_{x=\pi /2} & =2\operatorname{cos}⁡(2\cdot \frac{\pi }{2})\operatorname{cos}⁡(3\cdot \frac{\pi }{2})-3\operatorname{sin}⁡(2\cdot \frac{\pi }{2})\operatorname{sin}⁡(3\cdot \frac{\pi }{2}) \\  & =2\operatorname{cos}⁡(\pi )\operatorname{cos}⁡(\frac{3\pi }{2})-3\operatorname{sin}⁡(\pi )\operatorname{sin}⁡(\frac{3\pi }{2}) \\  & =0.\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "3c304fc9-c9da-5d97-9759-ccf6e138d12f",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-1",
        ":db/id": 17592186236194
      },
      {
        ":answer/id": "53809d10-dcef-5e85-886e-cc325cd763be",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "0",
        ":db/id": 17592186236347
      },
      {
        ":answer/id": "77c7b91a-bbc1-589a-884f-c42b2bb99fab",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1",
        ":db/id": 17592186236569
      },
      {
        ":answer/id": "78657ffb-16ea-5821-a776-4f1b2747a9b1",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2",
        ":db/id": 17592186236573
      },
      {
        ":answer/id": "c385379d-8237-5252-97dc-f26a22711a71",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3",
        ":db/id": 17592186237053
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "53809d10-dcef-5e85-886e-cc325cd763be",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "0",
      ":db/id": 17592186236347
    },
    ":answer-field/id": "9a6e6951-f040-51c5-a0b5-e70540d8f884",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186237642
  }
]
```

## q-11824

(x+1)e^(kx); full bank [(kx+1)e^(kx), (kx+k+1)e^(kx) correct, (x+1)e^(kx), kx e^(kx), k(x+1)e^(kx)]. Original k=9. Every original option maps exactly; the last bank value omits the derivative of x+1, first omits k from the constant; other mistakes are retained algebraic recipes.

Prompt:

Given that $y=(x+1){e}^{9x},$ find $\frac{\text{d}y}{\text{d}x}.$

Fixed worked solution:

This question requires the product rule. Let $u(x)=x+1$ and $v(x)={e}^{9x}.$ Then

$$
{u}^{′}(x)=1,\,{v}^{′}(x)=9{e}^{9x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(1)({e}^{9x})+(x+1)(9{e}^{9x}) \\  & ={e}^{9x}+9(x+1){e}^{9x} \\  & =(1+9(x+1)){e}^{9x} \\  & =(9x+10){e}^{9x}.\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "46092d6a-5809-530b-96aa-d18ca741a149",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "(9x+1){e}^{9x}",
        ":db/id": 17592186251132
      },
      {
        ":answer/id": "9449d2c4-40c8-5886-a8f8-d377e92abd71",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "(9x+10){e}^{9x}",
        ":db/id": 17592186251828
      },
      {
        ":answer/id": "9fcc1d83-99af-5f5a-b373-703da0e18e92",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "(x+1){e}^{9x}",
        ":db/id": 17592186251929
      },
      {
        ":answer/id": "a8022752-cd20-552c-942e-08b64f288227",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "9x{e}^{9x}",
        ":db/id": 17592186252002
      },
      {
        ":answer/id": "af7653ed-b253-50e2-9a68-8c72c94c9870",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "9(x+1){e}^{9x}",
        ":db/id": 17592186252083
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "9449d2c4-40c8-5886-a8f8-d377e92abd71",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "(9x+10){e}^{9x}",
      ":db/id": 17592186251828
    },
    ":answer-field/id": "2531d2a5-3c0e-51d6-8cfe-475ebfb26445",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186252873
  }
]
```

## q-2392

a^(kx)tan(x); domain a>0, cos(x)!=0. Full bank [a^(kx)(sec^2(x)+k ln(a)tan(x)) correct, a^(kx)(sec^2(x)+k tan(x)), a^(kx)sec^2(x)+k tan(x), k a^(kx)(sec^2(x)+ln(a)tan(x)), k sec^2(x)+k a^(kx)tan(x)]. Original k=3. Distinct a-symbol expressions; do not specialize a to 1/e where choices might collide.

Prompt:

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={a}^{3x}\operatorname{tan}⁡x.$

Fixed worked solution:

This question requires the product rule. Let $u(x)=\operatorname{tan}⁡x$ and $v(x)={a}^{3x}.$ Then

$$
{u}^{′}(x)={sec}^{2}⁡x,\,{v}^{′}(x)=3{a}^{3x}\operatorname{ln}⁡a.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({sec}^{2}⁡x)({a}^{3x})+(\operatorname{tan}⁡x)(3{a}^{3x}\operatorname{ln}⁡a) \\  & ={a}^{3x}({sec}^{2}⁡x+3\operatorname{ln}⁡a\operatorname{tan}⁡x).\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "38e395c8-f565-5740-959d-6bf0c34f8710",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "{a}^{3x}({sec}^{2}\u2061x+3\\operatorname{ln}\u2061a\\operatorname{tan}\u2061x)",
        ":db/id": 17592186288420
      },
      {
        ":answer/id": "47d8a58a-8445-5585-bc47-18b1d4683989",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "{a}^{3x}({sec}^{2}\u2061x+3\\operatorname{tan}\u2061x)",
        ":db/id": 17592186288526
      },
      {
        ":answer/id": "60da0eec-e09f-556c-977c-0afa9bca8118",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "{a}^{3x}{sec}^{2}\u2061x+3\\operatorname{tan}\u2061x",
        ":db/id": 17592186288710
      },
      {
        ":answer/id": "9efacfe8-4ef9-586f-935e-d85e18391332",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3{a}^{3x}({sec}^{2}\u2061x+\\operatorname{ln}\u2061a\\operatorname{tan}\u2061x)",
        ":db/id": 17592186289098
      },
      {
        ":answer/id": "d7f42cff-705d-5052-8de2-d67ef0b14a77",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3{sec}^{2}\u2061x+3{a}^{3x}\\operatorname{tan}\u2061x",
        ":db/id": 17592186289468
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "38e395c8-f565-5740-959d-6bf0c34f8710",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "{a}^{3x}({sec}^{2}\u2061x+3\\operatorname{ln}\u2061a\\operatorname{tan}\u2061x)",
      ":db/id": 17592186288420
    },
    ":answer-field/id": "84733a66-1c91-5acb-9908-573c1e35d199",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186290021
  }
]
```

## q-2401

4x^2 sqrt(sin x), derivative (8x sin x+2x^2 cos x)/sqrt(sin x). Real differentiable domain sin x>0. All five original banks retained exactly. Distractor containing sqrt(cos x) has different domain; must not transfer its recipe to sampled parameters without evidence. No new variants declared.

Prompt:

Find ${y}^{′}$ for $y=4{x}^{2}\sqrt{\operatorname{sin}⁡x}.$

Fixed worked solution:

This question requires the product rule. Let $u(x)=4{x}^{2}$ and $v(x)=\sqrt{\operatorname{sin}⁡x}.$ Then

$$
{u}^{′}(x)=8x,\,{v}^{′}(x)=\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{y}^{′}=\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(8x)(\sqrt{\operatorname{sin}⁡x})+(4{x}^{2})(\frac{\operatorname{cos}⁡x}{2\sqrt{\operatorname{sin}⁡x}}) \\  & =8x\sqrt{\operatorname{sin}⁡x}+\frac{2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}} \\  & =\frac{8x\operatorname{sin}⁡x+2{x}^{2}\operatorname{cos}⁡x}{\sqrt{\operatorname{sin}⁡x}}.\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "25db7b46-2d5d-595a-8da7-747d2ddd12b4",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{x\\operatorname{cos}\u2061x+2x\\operatorname{sin}\u2061x}{\\operatorname{sin}\u2061x}",
        ":db/id": 17592186288282
      },
      {
        ":answer/id": "5d85a103-3ef8-59d4-8e84-637387fa0c40",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{2{x}^{2}\\operatorname{sin}\u2061x}{\\sqrt{\\operatorname{sin}\u2061x}}-x\\sqrt{\\operatorname{sin}\u2061x}",
        ":db/id": 17592186288686
      },
      {
        ":answer/id": "922058af-c9bd-5099-865a-eed92655f212",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{2{x}^{2}\\operatorname{sin}\u2061x-8x\\operatorname{sin}\u2061x}{\\sqrt{\\operatorname{sin}\u2061x}}",
        ":db/id": 17592186289014
      },
      {
        ":answer/id": "99fc2ea7-0124-5d04-bc08-8eef810aff45",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{8x\\operatorname{sin}\u2061x+2{x}^{2}\\operatorname{cos}\u2061x}{\\sqrt{\\operatorname{sin}\u2061x}}",
        ":db/id": 17592186289061
      },
      {
        ":answer/id": "b4a9b433-04de-5c42-b250-5744d10efff4",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{2{x}^{2}\\operatorname{cos}\u2061x}{\\sqrt{\\operatorname{cos}\u2061x}}+8x\\sqrt{\\operatorname{sin}\u2061x}",
        ":db/id": 17592186289226
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "99fc2ea7-0124-5d04-bc08-8eef810aff45",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{8x\\operatorname{sin}\u2061x+2{x}^{2}\\operatorname{cos}\u2061x}{\\sqrt{\\operatorname{sin}\u2061x}}",
      ":db/id": 17592186289061
    },
    ":answer-field/id": "04b0a0d1-3edc-5da1-b114-a49367e0bb38",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186289737
  }
]
```

## q-343332

e^x sin(kx), requested bracket sin(kx)+k cos(kx); product terms e^x sin(kx), k e^x cos(kx). Original k=4. No distractors.

Prompt:

Calculate $\frac{\text{d}y}{\text{d}x}$ for $y={e}^{x}\operatorname{sin}⁡4x.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{x}$

Fixed worked solution:

This question requires the product rule. Let $u(x)={e}^{x}$ and $v(x)=\operatorname{sin}⁡4x.$ Then

$$
{u}^{′}(x)={e}^{x},\,{v}^{′}(x)=4\operatorname{cos}⁡4x.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =({e}^{x})(\operatorname{sin}⁡4x)+(4\operatorname{cos}⁡4x)({e}^{x}) \\  & =(\operatorname{sin}⁡4x+4\operatorname{cos}⁡4x){e}^{x}.\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "44207d6e-a407-5515-8b9e-f67da1b5db73",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\operatorname{sin}4x+4\\operatorname{cos}4x",
        ":db/id": 17592186315515
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "44207d6e-a407-5515-8b9e-f67da1b5db73",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\operatorname{sin}4x+4\\operatorname{cos}4x",
      ":db/id": 17592186315515
    },
    ":answer-field/id": "165c0e8f-7c32-58b2-bd8b-4210c1bded3b",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186316597
  }
]
```

## q-343354

c x e^(kx), requested bracket ckx+c. Original c=2,k=6. No distractors.

Prompt:

Given that $y=2x{e}^{6x},$ find $\frac{\text{d}y}{\text{d}x}.$

$\frac{\text{d}y}{\text{d}x}=($
{{field-1}} $){e}^{6x}$

Fixed worked solution:

This question requires the product rule. Let $u(x)=2x$ and $v(x)={e}^{6x}.$ Then

$$
{u}^{′}(x)=2,\,{v}^{′}(x)=6{e}^{6x}.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}y}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2)({e}^{6x})+(2x)(6{e}^{6x}) \\  & =(12x+2){e}^{6x}.\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "4cc31045-6721-506d-b85c-975fcd9e3e95",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "12x+2",
        ":db/id": 17592186315556
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "4cc31045-6721-506d-b85c-975fcd9e3e95",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "12x+2",
      ":db/id": 17592186315556
    },
    ":answer-field/id": "7be93c96-933c-5510-b979-c109a0def8ed",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186316843
  }
]
```

## q-9942

x^2 sin(kx+b), full bank [2x^2 sin(kx+b)+kx cos(kx+b), 2x sin(kx+b)+x^2 cos(kx+b), 2 sin(kx+b)+kx^2 cos(kx+b), 2x sin(kx+b)+kx^2 cos(kx+b) correct, kx sin(kx+b)+2x^2 cos(kx+b)]. Original k=5,b=2. Changed shifts preserve power 2. k=2 excluded since last choice becomes correct.

Prompt:

If $f(x)={x}^{2}\operatorname{sin}⁡(5x+2),$ find ${f}^{′}(x).$

Fixed worked solution:

This question requires the product rule. Let $u(x)={x}^{2}$ and $v(x)=\operatorname{sin}⁡(5x+2).$ Then

$$
{u}^{′}(x)=2x,\,{v}^{′}(x)=5\operatorname{cos}⁡(5x+2).
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}{f}^{′}=\frac{\text{d}f}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2x)(\operatorname{sin}⁡(5x+2))+({x}^{2})(5\operatorname{cos}⁡(5x+2)) \\  & =2x\operatorname{sin}⁡(5x+2)+5{x}^{2}\operatorname{cos}⁡(5x+2).\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "20f4b495-e5fb-55a4-b9fd-82586fb5a57e",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2{x}^{2}\\operatorname{sin}\u2061(5x+2)+5x\\operatorname{cos}\u2061(5x+2)",
        ":db/id": 17592186360977
      },
      {
        ":answer/id": "553cde80-173f-5c83-990b-953883f6a78f",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2x\\operatorname{sin}\u2061(5x+2)+{x}^{2}\\operatorname{cos}\u2061(5x+2)",
        ":db/id": 17592186361220
      },
      {
        ":answer/id": "6048e77d-cff3-5a2c-a13d-9857f23b54a7",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2\\operatorname{sin}\u2061(5x+2)+5{x}^{2}\\operatorname{cos}\u2061(5x+2)",
        ":db/id": 17592186361271
      },
      {
        ":answer/id": "6c3805d8-997f-5a7d-a009-fb4112187474",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2x\\operatorname{sin}\u2061(5x+2)+5{x}^{2}\\operatorname{cos}\u2061(5x+2)",
        ":db/id": 17592186361319
      },
      {
        ":answer/id": "c0543623-6d50-5d27-965b-5debe119e83e",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5x\\operatorname{sin}\u2061(5x+2)+2{x}^{2}\\operatorname{cos}\u2061(5x+2)",
        ":db/id": 17592186361696
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "6c3805d8-997f-5a7d-a009-fb4112187474",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "2x\\operatorname{sin}\u2061(5x+2)+5{x}^{2}\\operatorname{cos}\u2061(5x+2)",
      ":db/id": 17592186361319
    },
    ":answer-field/id": "28d57a36-0a6c-5441-82df-3d718e622317",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186362018
  }
]
```

## q-9944

x^2 sin^3(x), slope at 0 is 0. Bank {-1,3,0,2,5} has unestablished parameter recipes; retain one exact task only. Varying scale at this evaluation point would keep a trivial zero answer and is not used for replenishment.

Prompt:

Find the slope of $f(x)={x}^{2}{sin}^{3}⁡x$ at $x=0.$

Fixed worked solution:

To find the slope at a given point, we have to find $\frac{\text{d}f}{\text{d}x}$ at that point.

This question requires the product rule. Let $u(x)={x}^{2}$ and $v(x)={sin}^{3}⁡x.$ Then

$$
{u}^{′}(x)=2x,\,{v}^{′}(x)=3{sin}^{2}⁡x\operatorname{cos}⁡x.
$$

Note that we used the chain rule to differentiate $v.$

Now, applying the product rule and simplifying, we have

$$
\begin{aligned}\frac{\text{d}f}{\text{d}x} & ={u}^{′}(x)\cdot v(x)+u(x)\cdot {v}^{′}(x) \\  & =(2x)({sin}^{3}⁡x)+({x}^{2})(3{sin}^{2}⁡x\operatorname{cos}⁡x) \\  & =2x{sin}^{3}⁡x+3{x}^{2}{sin}^{2}⁡x\operatorname{cos}⁡x.\end{aligned}
$$

Therefore, the slope at $x=0$ is

$$
\begin{aligned}{(\frac{\text{d}f}{\text{d}x})|}_{x=0} & =2\cdot 0\cdot {sin}^{3}⁡(0)+3\cdot {0}^{2}\cdot {sin}^{2}⁡(0)\operatorname{cos}⁡(0) \\  & =0.\end{aligned}
$$

Exact field components, source choices and canonical designation:

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "2089f74f-7bb1-531f-9f54-4e2969f07e4d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-1",
        ":db/id": 17592186360974
      },
      {
        ":answer/id": "54599985-5dd3-502a-b9ef-88b1d618a930",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3",
        ":db/id": 17592186361211
      },
      {
        ":answer/id": "5e9b1f0e-03d5-557f-83d3-fc825eebaa97",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "0",
        ":db/id": 17592186361263
      },
      {
        ":answer/id": "72ddff39-ee62-599f-a890-d26c22490faf",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2",
        ":db/id": 17592186361340
      },
      {
        ":answer/id": "93d239b8-90ad-5454-b0f7-400662e44c87",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5",
        ":db/id": 17592186361494
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "5e9b1f0e-03d5-557f-83d3-fc825eebaa97",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "0",
      ":db/id": 17592186361263
    },
    ":answer-field/id": "e03caba5-0350-5e9d-aa7c-ebd7a638e046",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186362179
  }
]
```