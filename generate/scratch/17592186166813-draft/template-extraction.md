# Template extraction — all four stages

Provenance matches source.json: math basis2275, captured lineage. Original prompt, exact field shapes, complete bank and whole solution follow for every practice case. No source is omitted. Exact whitespace in the blank is preserved by source.json and public observed replay; code fences below show decoded strings.

## Stage1 — describe originals before generalizing

### q-95982 / easy

Derivative occurrence orders, in printed order: [2, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
What is the order of the ordinary differential equation $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+{x}^{3}y=5{y}^{4}\frac{\text{d}y}{\text{d}x}?$
```

Full worked solution:

```text
The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.

The highest derivative in the given ODE is $\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}},$ which has order $2.$

Therefore, the order of the ODE is $2.$
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| selection | :answer-field.type/radio | :answer.type/math | 4, 1, 2, 3, 5 | 2 |


Exact source answer feedback and attribute presence:

```json
[
  {
    "field": "selection",
    "answers": [
      {
        ":answer/id": "1f4efdc2-0db6-5c05-93a3-dc37ed677c69",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "4"
      },
      {
        ":answer/id": "259dd133-5bb9-5064-ab22-10c2ff0d0e41",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1"
      },
      {
        ":answer/id": "51e56ff6-776f-5f56-9c5b-1b8c442dae31",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2"
      },
      {
        ":answer/id": "e0e79109-ddec-555e-b8e9-91c639217e9a",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3"
      },
      {
        ":answer/id": "e1b99836-5aa4-5130-9573-30541e38e184",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5"
      }
    ]
  }
]
```


Source solution stages: 3 double-newline paragraphs; exact sentence sequence above. Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs. No solution-stage omissions introduced.

### q-95983 / moderate

Derivative occurrence orders, in printed order: [3, 1, 2, 1, 1, 1, 2]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Which of the following are third-order ordinary differential equations?

Select all that apply.

- **I.** ${y}^{‴}+3x{y}^{′}=xy$
- **II.** $3{y}^{″}{y}^{′}-2xy=2{y}^{′}$
- **III.** ${x}^{3}{y}^{′}-2x={y}^{″}$
```

Full worked solution:

```text
A differential equation is of third-order if the largest derivative term in the equation is ${y}^{‴}.$

Keeping this in mind, let's check each given equation.

- Equation I is a third-order differential equation. The highest derivative in this equation is ${y}^{‴}.$

- Equation II is not a third-order differential equation. The highest derivative in this equation is ${y}^{″},$ so this is a second-order differential equation.

- Equation III is not a third-order differential equation. The highest derivative in this equation is ${y}^{″},$ so this is a second-order differential equation.

Therefore, the correct answer is "I only."
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| I | :answer-field.type/checkbox | :answer.type/text | false, true | true |

| II | :answer-field.type/checkbox | :answer.type/text | false, true | false |

| III | :answer-field.type/checkbox | :answer.type/text | false, true | false |


Exact source answer feedback and attribute presence:

```json
[
  {
    "field": "I",
    "answers": [
      {
        ":answer/id": "68bd231d-9e13-571c-877b-269bf3710fa5",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "7ed54d05-d26e-52c1-9f98-8a77b88ca5f2",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  },
  {
    "field": "II",
    "answers": [
      {
        ":answer/id": "690c87af-9ba3-5188-a6c9-7004cd7ed245",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "3abb4d56-10ee-58da-b334-bd3d4d312f6b",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  },
  {
    "field": "III",
    "answers": [
      {
        ":answer/id": "b3fcb428-35a7-5079-97a4-0ee4b813532c",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "71d4db59-c3a1-5b9f-be64-7507b8ddd8d3",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  }
]
```


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion. No solution-stage omissions introduced.

### q-118780 / easy

Derivative occurrence orders, in printed order: [7, 1, 8]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
What is the order of the ordinary differential equation ${x}^{2}\frac{{\text{d}}^{7}y}{\text{d}{x}^{7}}-9{x}^{7}\frac{\text{d}y}{\text{d}x}=2\frac{{\text{d}}^{8}y}{\text{d}{x}^{8}}?$
```

Full worked solution:

```text
The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.

The highest derivative in the given ODE is $\frac{{\text{d}}^{8}y}{\text{d}{x}^{8}},$ which has order $8.$

Therefore, the order of the ODE is $8.$
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| selection | :answer-field.type/radio | :answer.type/math | 9, 6, 8, 2, 7 | 8 |


Exact source answer feedback and attribute presence:

```json
[
  {
    "field": "selection",
    "answers": [
      {
        ":answer/id": "15565682-eecd-527d-bdad-636bfbf7050a",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "9"
      },
      {
        ":answer/id": "6f7ccbe7-06c3-5517-a28c-85c2c93dd1cc",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "6"
      },
      {
        ":answer/id": "d660a7a7-dc36-5e4d-a9c3-166dbc8a4519",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "8"
      },
      {
        ":answer/id": "ee8b6705-43a0-5e03-9cf5-13a5fd9b86d4",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2"
      },
      {
        ":answer/id": "f84a8157-12d6-59ae-8ec7-46e3a067045a",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "7"
      }
    ]
  }
]
```


Source solution stages: 3 double-newline paragraphs; exact sentence sequence above. Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs. No solution-stage omissions introduced.

### q-118782 / moderate

Derivative occurrence orders, in printed order: [2, 1, 2, 3, 2]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Which of the following are second-order ordinary differential equations?

Select all that apply.

- **I.** $9x{y}^{''}+8{y}^{'}=4$
- **II.** $\sqrt{{y}^{''}+x}=3y$
- **III.** ${y}^{‴}+{x}^{2}{y}^{''}=3$
```

Full worked solution:

```text
A differential equation is of second-order if the largest derivative term in the equation is ${y}^{''}.$

Keeping this in mind, let's check each given equation.

- Equation I is a second-order differential equation. The highest derivative in this equation is ${y}^{''}.$

- Equation II is also a second-order differential equation. The highest derivative in this equation is ${y}^{''}.$

- Equation III is not a second-order differential equation. The highest derivative in this equation is ${y}^{‴},$ so this is a third-order differential equation.

Therefore, the correct answer is "I and II only."
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| I | :answer-field.type/checkbox | :answer.type/text | false, true | true |

| II | :answer-field.type/checkbox | :answer.type/text | false, true | true |

| III | :answer-field.type/checkbox | :answer.type/text | false, true | false |


Exact source answer feedback and attribute presence:

```json
[
  {
    "field": "I",
    "answers": [
      {
        ":answer/id": "8743aa26-cf69-5449-934f-38ba3af38f5b",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "74efbd4d-220e-5275-80bd-028967ae7884",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  },
  {
    "field": "II",
    "answers": [
      {
        ":answer/id": "49500573-2ce0-590c-86df-84246df6d5a8",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "7af8cf24-f331-507c-bd22-14b25419399e",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  },
  {
    "field": "III",
    "answers": [
      {
        ":answer/id": "018e22bf-4426-5c0c-af3b-e62372d8a525",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "92695221-a3db-5b8c-9073-f364bca40787",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  }
]
```


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion. No solution-stage omissions introduced.

### q-96669 / moderate

Derivative occurrence orders, in printed order: [3, 1, 2, 1, 1, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Which of the following are first-order ordinary differential equations?

Select all that apply.

- **I.** ${y}^{‴}+(\operatorname{sin}⁡x){y}^{′}={x}^{2}y$
- **II.** $5{y}^{″}{y}^{′}+3xy=4{y}^{′}$
- **III.** ${({y}^{′})}^{2}-2{x}^{2}=y$
```

Full worked solution:

```text
A differential equation is of first-order if the largest derivative term in the equation is ${y}^{′}.$

Keeping this in mind, let's check each given equation.

- Equation I is not a first-order differential equation. The highest derivative in this equation is ${y}^{‴},$ so this is a third-order differential equation.

- Equation II is not a first-order differential equation. The highest derivative in this equation is ${y}^{″},$ so this is a second-order differential equation.

- Equation III is a first-order differential equation. The highest derivative in this equation is ${y}^{′}.$

Therefore, the correct answer is "III only."
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| I | :answer-field.type/checkbox | :answer.type/text | false, true | false |

| II | :answer-field.type/checkbox | :answer.type/text | false, true | false |

| III | :answer-field.type/checkbox | :answer.type/text | false, true | true |


Exact source answer feedback and attribute presence:

```json
[
  {
    "field": "I",
    "answers": [
      {
        ":answer/id": "8b78f5f8-eebd-57fd-8d9c-03ba838f7aef",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "4c109920-c2c8-5c61-8b61-0f78d91253a1",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  },
  {
    "field": "II",
    "answers": [
      {
        ":answer/id": "42ef4fc5-634b-5120-a4df-e7cd35583cb2",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "5957af20-d016-564c-98a5-0dad4377e784",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  },
  {
    "field": "III",
    "answers": [
      {
        ":answer/id": "084c63a5-b227-5826-b684-c0eef7a795da",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "265170ce-4178-5220-a328-3f5bd0ec833b",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  }
]
```


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion. No solution-stage omissions introduced.

### q-96676 / moderate

Derivative occurrence orders, in printed order: [2, 1, 1, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Which of the following are first-order ordinary differential equations?

Select all that apply.

- **I.** $3{y}^{''}+2x{y}^{'}={x}^{2}y$
- **II.** $5{x}^{2}y+3{y}^{5}{y}^{'}=4x$
- **III.** $\sqrt{{y}^{2}+{y}^{'}}+7{x}^{3}={e}^{y}$
```

Full worked solution:

```text
A differential equation is of first-order if the largest derivative term in the equation is ${y}^{'}.$

Keeping this in mind, let's check each given equation.

- Equation I is not a first-order differential equation. The highest derivative in this equation is ${y}^{''},$ so this is a second-order differential equation.

- Equation II is a first-order differential equation. The highest derivative in this equation is ${y}^{'}.$

- Equation III is also a first-order differential equation. The highest derivative in this equation is ${y}^{'}.$

Therefore, the correct answer is "II and III only."
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| I | :answer-field.type/checkbox | :answer.type/text | false, true | false |

| II | :answer-field.type/checkbox | :answer.type/text | false, true | true |

| III | :answer-field.type/checkbox | :answer.type/text | false, true | true |


Exact source answer feedback and attribute presence:

```json
[
  {
    "field": "I",
    "answers": [
      {
        ":answer/feedback": "Equation I contains y'', so its highest derivative is second order.",
        ":answer/id": "6fddfc61-ae75-5f4b-8b2e-b3415ea0d369",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/feedback": "Equation I contains y'', so its highest derivative is second order.",
        ":answer/id": "c834636a-bbd4-5759-b671-beb2e4da2abb",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  },
  {
    "field": "II",
    "answers": [
      {
        ":answer/feedback": "Equation II contains y' and no higher derivative. The factor y^5 does not change the differential order.",
        ":answer/id": "df851142-894b-5bfb-8ece-98c5eb3b201e",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/feedback": "Equation II contains y' and no higher derivative. The factor y^5 does not change the differential order.",
        ":answer/id": "a4f9a0af-45e8-5e36-aa37-2b6d226dc143",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  },
  {
    "field": "III",
    "answers": [
      {
        ":answer/feedback": "Equation III contains y' and no higher derivative. The square root does not change the differential order.",
        ":answer/id": "1bb8cc3c-94ce-5d96-9edb-479fa67563b6",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/feedback": "Equation III contains y' and no higher derivative. The square root does not change the differential order.",
        ":answer/id": "6e1d4c62-4dd2-5856-8d10-6a84849ff212",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  }
]
```


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion. No solution-stage omissions introduced.

### q-96680 / moderate

Derivative occurrence orders, in printed order: [1, 2, 3, 1, 1, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Which of the following are first-order ordinary differential equations?

Select all that apply.

- **I.** $3{y}^{'}+2x{y}^{''}={x}^{2}y$
- **II.** $5{x}^{2}{y}^{‴}+3x{y}^{'}={e}^{x}$
- **III.** $4{({y}^{'})}^{3}+7{x}^{3}=x({y}^{2}+{({y}^{'})}^{2})$
```

Full worked solution:

```text
A differential equation is of first-order if the largest derivative term in the equation is ${y}^{'}.$

Keeping this in mind, let's check each given equation.

- Equation I is not a first-order differential equation. The highest derivative in this equation is ${y}^{''},$ so this is a second-order differential equation.

- Equation II is not a first-order differential equation. The highest derivative in this equation is ${y}^{‴},$ so this is a third-order differential equation.

- Equation III is a first-order differential equation. The highest derivative in this equation is ${y}^{'}.$

Therefore, the correct answer is "III only."
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| I | :answer-field.type/checkbox | :answer.type/text | false, true | false |

| II | :answer-field.type/checkbox | :answer.type/text | false, true | false |

| III | :answer-field.type/checkbox | :answer.type/text | false, true | true |


Exact source answer feedback and attribute presence:

```json
[
  {
    "field": "I",
    "answers": [
      {
        ":answer/id": "8d0d894d-c809-5dae-b04c-777fa7f1b329",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "3ef08266-c8b5-5d86-ba6c-38cec94b0b81",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  },
  {
    "field": "II",
    "answers": [
      {
        ":answer/id": "ccb30e5b-1e6e-5289-8a92-1d1a6eb3264f",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "5090af3c-f638-5321-a137-c61895760b06",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  },
  {
    "field": "III",
    "answers": [
      {
        ":answer/id": "7601c375-892a-5f42-948b-dc68c11393c9",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "4fae8008-076c-53ed-87cb-e76c044c94bf",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  }
]
```


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion. No solution-stage omissions introduced.

### q-167787 / easy

Derivative occurrence orders, in printed order: [4, 2, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Consider the following differential equation.

$$
{x}^{3}\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}}-x\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+\frac{\text{d}y}{\text{d}x}=f(x)
$$

The order of this differential equation is

                            
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        .
```

Full worked solution:

```text
We have the differential equation

$$
{x}^{3}\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}}-x\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+\frac{\text{d}y}{\text{d}x}=\frac{1}{2}{e}^{x}.
$$

 

The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.

The highest derivative in the given ODE is $\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}},$ which has order $4.$

Therefore, the order of the ODE is $4.$
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| field-1 | :answer-field.type/blank | :answer.type/math | 4 | 4 |


Exact source answer feedback and attribute presence:

```json
[
  {
    "field": "field-1",
    "answers": [
      {
        ":answer/id": "4ecd7d48-e192-56ba-a9eb-6c4280135677",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "4"
      }
    ]
  }
]
```


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs. No solution-stage omissions introduced.

### q-118779 / easy

Derivative occurrence orders, in printed order: [6, 3]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
What is the order of the ordinary differential equation $y\frac{{\text{d}}^{6}y}{\text{d}{x}^{6}}+3x\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}}={x}^{8}?$
```

Full worked solution:

```text
The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.

The highest derivative in the given ODE is $\frac{{\text{d}}^{6}y}{\text{d}{x}^{6}},$ which has order $6.$

Therefore, the order of the ODE is $6.$
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| selection | :answer-field.type/radio | :answer.type/math | 6, 8, 7, 3, 4 | 6 |


Exact source answer feedback and attribute presence:

```json
[
  {
    "field": "selection",
    "answers": [
      {
        ":answer/id": "22ac80f9-d1a9-57b5-8a75-ee4e690886f3",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "6"
      },
      {
        ":answer/id": "254a46ec-eea5-5a9e-b90d-ccb407bc95b2",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "8"
      },
      {
        ":answer/id": "625479f9-bef7-5c1a-937a-158ca732f7fc",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "7"
      },
      {
        ":answer/id": "c2b7f046-3e73-5ab4-abac-a3903f00d5ae",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3"
      },
      {
        ":answer/id": "d1ca56e0-ad02-5c3f-97f9-85ad61671b34",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "4"
      }
    ]
  }
]
```


Source solution stages: 3 double-newline paragraphs; exact sentence sequence above. Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs. No solution-stage omissions introduced.

### q-118781 / easy

Derivative occurrence orders, in printed order: [3, 4]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
What is the order of the ordinary differential equation $x\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}}-{y}^{2}\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}}={y}^{5}?$
```

Full worked solution:

```text
The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.

The highest derivative in the given ODE is $\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}},$ which has order $4.$

Therefore, the order of the ODE is $4.$
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| selection | :answer-field.type/radio | :answer.type/math | 4, 3, 2, 6, 5 | 4 |


Exact source answer feedback and attribute presence:

```json
[
  {
    "field": "selection",
    "answers": [
      {
        ":answer/id": "18ed852c-a746-5e34-8210-a1c6c19157ed",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "4"
      },
      {
        ":answer/id": "36e85211-b2b9-5649-bb4b-17bb47e95e41",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3"
      },
      {
        ":answer/id": "7c9ca850-3368-5c8e-a5b8-495183e07f87",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2"
      },
      {
        ":answer/id": "9e263215-e831-5e53-a204-bd8750fe03b0",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "6"
      },
      {
        ":answer/id": "a7d903f5-c111-595f-8377-514289f9d574",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5"
      }
    ]
  }
]
```


Source solution stages: 3 double-newline paragraphs; exact sentence sequence above. Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs. No solution-stage omissions introduced.

### q-118783 / moderate

Derivative occurrence orders, in printed order: [2, 1, 3, 2, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Which of the following are second-order ordinary differential equations?

Select all that apply.

- **I.** ${y}^{″}+{y}^{′}={x}^{2}-x$
- **II.** ${y}^{‴}-y=x-{y}^{″}$
- **III.** ${x}^{3}{y}^{′}+x=y$
```

Full worked solution:

```text
A differential equation is of second-order if the largest derivative term in the equation is ${y}^{″}.$

Keeping this in mind, let's check each given equation.

- Equation I is a second-order differential equation. The highest derivative in this equation is ${y}^{″}.$

- Equation II is not a second-order differential equation. The highest derivative in this equation is ${y}^{‴},$ so this is a third-order differential equation.

- Equation III is not a second-order differential equation. The highest derivative in this equation is ${y}^{′},$ so this is a first-order differential equation.

Therefore, the correct answer is "I only."
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| I | :answer-field.type/checkbox | :answer.type/text | false, true | true |

| II | :answer-field.type/checkbox | :answer.type/text | false, true | false |

| III | :answer-field.type/checkbox | :answer.type/text | false, true | false |


Exact source answer feedback and attribute presence:

```json
[
  {
    "field": "I",
    "answers": [
      {
        ":answer/id": "860b7136-4797-5983-a802-c78784e3f2c9",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "1ef28afe-8d1f-5280-9074-b3d607cfb6f5",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  },
  {
    "field": "II",
    "answers": [
      {
        ":answer/id": "62539b47-6fac-5fcf-9503-61e8367eec33",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "e4034300-7163-55c2-9f5c-bcf30334285a",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  },
  {
    "field": "III",
    "answers": [
      {
        ":answer/id": "de826aab-09ea-5a31-9751-6dc8761d2c0b",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "099306fc-1518-5f1a-b302-f2ae896069b6",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  }
]
```


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion. No solution-stage omissions introduced.

### q-96662 / easy

Derivative occurrence orders, in printed order: [3, 2]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
What is the order of the ordinary differential equation $\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}}+5{y}^{2}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+3{y}^{5}=0?$
```

Full worked solution:

```text
The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.

The highest derivative in the given ODE is $\frac{{\text{d}}^{3}y}{\text{d}{x}^{3}},$ which has order $3.$

Therefore, the order of the ODE is $3.$
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| selection | :answer-field.type/radio | :answer.type/math | 5, 1, 2, 3, 4 | 3 |


Exact source answer feedback and attribute presence:

```json
[
  {
    "field": "selection",
    "answers": [
      {
        ":answer/id": "53060f3c-37ba-5269-99e6-437127908eb9",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5"
      },
      {
        ":answer/id": "779e8577-9f6e-5fa7-924b-e37a99f1b28c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1"
      },
      {
        ":answer/id": "8704391c-698c-5b53-8da1-2de5b7777a0a",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2"
      },
      {
        ":answer/id": "aab69c40-d839-5b4b-94d1-7d9e857ba71c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3"
      },
      {
        ":answer/id": "d2d51d2e-5951-5e07-ab5d-d620a48d77f5",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "4"
      }
    ]
  }
]
```


Source solution stages: 3 double-newline paragraphs; exact sentence sequence above. Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs. No solution-stage omissions introduced.

### q-96663 / easy

Derivative occurrence orders, in printed order: [4, 2, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
What is the order of the ordinary differential equation $y\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}}-4{x}^{2}\frac{{\text{d}}^{2}y}{\text{d}{x}^{2}}+\operatorname{sin}⁡x\frac{\text{d}y}{\text{d}x}=2x?$
```

Full worked solution:

```text
The order of an ordinary differential equation (ODE) is the order of the highest derivative in the equation.

The highest derivative in the given ODE is $\frac{{\text{d}}^{4}y}{\text{d}{x}^{4}},$ which has order $4.$

Therefore, the order of the ODE is $4.$
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| selection | :answer-field.type/radio | :answer.type/math | 1, 5, 2, 4, 3 | 4 |


Exact source answer feedback and attribute presence:

```json
[
  {
    "field": "selection",
    "answers": [
      {
        ":answer/id": "4a7c8253-2398-5844-ab87-9f569178c088",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1"
      },
      {
        ":answer/id": "604bb718-8188-5706-9d5e-bc5e825254c1",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5"
      },
      {
        ":answer/id": "64729ba5-db61-5904-a7f3-3348bf688c82",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2"
      },
      {
        ":answer/id": "95c21078-c3b5-5a29-a41b-fa3dd5c92b1d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "4"
      },
      {
        ":answer/id": "9903b498-b87b-528c-9348-0e7f32f90a53",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3"
      }
    ]
  }
]
```


Source solution stages: 3 double-newline paragraphs; exact sentence sequence above. Definition → identify highest derivative and order → conclusion; q-167787 additionally restates an equation and includes whitespace paragraphs. No solution-stage omissions introduced.

### q-96672 / moderate

Derivative occurrence orders, in printed order: [2, 1, 2, 1, 1, 3, 1]. Independent variable x and dependent function y=y(x); all derivatives are ordinary. Positive integer polynomial powers and simple coefficients/functions are visual context, not differentiation tasks. No reduction or cancellation removes a derivative term.

Prompt:

```text
Which of the following are second-order ordinary differential equations?

Select all that apply.

- **I.** ${y}^{″}{x}^{3}-2y{y}^{′}=\operatorname{sin}⁡x$
- **II.** $3{y}^{″}{y}^{′}-2y=2{y}^{′}$
- **III.** $4{y}^{‴}x-7{x}^{2}{y}^{′}=y{e}^{x}$
```

Full worked solution:

```text
A differential equation is of second-order if the largest derivative term in the equation is ${y}^{″}.$

Keeping this in mind, let's check each given equation.

- Equation I is a second-order differential equation. The highest derivative in this equation is ${y}^{″}.$

- Equation II is also a second-order differential equation. The highest derivative in this equation is ${y}^{″}.$

- Equation III is not a second-order differential equation. The highest derivative in this equation is ${y}^{‴},$ so this is a third-order differential equation.

Therefore, the correct answer is "I and II only."
```

Fields and complete observed bank:

| Field | Type | Answer type | Every original value | Correct |
|---|---|---|---|---|

| I | :answer-field.type/checkbox | :answer.type/text | false, true | true |

| II | :answer-field.type/checkbox | :answer.type/text | false, true | true |

| III | :answer-field.type/checkbox | :answer.type/text | false, true | false |


Exact source answer feedback and attribute presence:

```json
[
  {
    "field": "I",
    "answers": [
      {
        ":answer/id": "30abb0c4-1bff-50f9-9fca-c00eba3cf9ff",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "ebe184a0-615a-5d44-a917-af918964b500",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  },
  {
    "field": "II",
    "answers": [
      {
        ":answer/id": "18a407fa-f792-5416-9af8-1c23d1ca46fc",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "d6eee552-87f0-587e-9972-7d671e2c86b2",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  },
  {
    "field": "III",
    "answers": [
      {
        ":answer/id": "ed3c95ff-45e3-5a8f-97c1-8b53553ad9b8",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "false"
      },
      {
        ":answer/id": "5ae2557d-e9db-57cc-b828-db6340b0d291",
        ":answer/type": {
          ":db/ident": ":answer.type/text"
        },
        ":answer/value": "true"
      }
    ]
  }
]
```


Source solution stages: 6 double-newline paragraphs; exact sentence sequence above. Target-order definition → invitation to check → I classification → II classification → III classification → selected-set conclusion. No solution-stage omissions introduced.


## Stage2 — shared pattern and response

Scalar: recognize each formal Leibniz derivative, read its differentiation order, take the maximum across the full equation, and return that integer through the original radio or blank. Ordinary x/y exponents and coefficient functions do not determine order. Three-way selection: read requested order and independently compare it with the largest prime/Leibniz derivative in each equation; preserve one checkbox field for each I/II/III. Products, powers or a square root containing a derivative do not change the derivative's order. Nothing is differentiated or solved.

## Stage3 — components and complete original choice mapping

`choice-recipes.json` maps all73 original choices to owning field, original UUID, exact value, correct designation, recipe, original parameters and bank profile. It is generated from immutable source evidence and cross-checked by validate.py, not an answer lookup used by generation. Source numerical component catalogs are interpretation-limited explicit replay profiles; no arbitrary numerical regression is promoted as a historical error operation. Source checkbox banks always contain false and true. Their keys remain I/II/III and their correct choice derives from printed highest order equal to target. The blank contains a single math answer and retains {{field-1}}.

The source renderer masks **whole derivative components**, including their full numerator and denominator. It also slots complete ordinal words in prose and the whole $n.$ order fragment in scalar conclusions. No blind coefficient substitution touches prose, function names, labels or derivative arguments. Variable/component notation style remains exact whenever order is unchanged; changed prime orders above3 switch to unambiguous Leibniz notation. No derivative-free equation can be generated.

## Stage4 — reusable masks, domains and computations

Public observed replay: template is the source ID, profile observed; parameters are a complete `orders` dictionary from old source order to new order. The six q-96676 answer feedback attributes have full derivative-token and ordinal-word slots; source y^5 and square-root explanations remain attached to their original fields. Feedback is normalized before IDs and participates in content identity. Every other original choice preserves absence of the feedback attribute. Values are integer1–8, strictly increasing in old-order order; every complete source-component radio option must stay positive, distinct, and include the new highest exactly once. Thus preserved source sentence truth and selected-set layout remain valid. The entire complete bank is chosen before rendering and rejected together on collision/domain failure. Original maps are identity maps; every source is also tested with a nonidentity map through the same public API. Raw q-167787 RHS prose anomaly remains visible; source_repaired changes only the wrong restated RHS.

Authored easy: n3–7; m1–n−2; ordinary exponent e in n+2..9. Left layout yD_n+3xD_m=x^e; right layout x^eD_m−3x=yD_n. Both have exactly two derivative occurrences. Correct n; complete bank [n,m,e,n−1,n+1]. Wrong operations read lower derivative, read an ordinary exponent, or count one too few/many differentiations. All five values are distinct under the bounds; the profile is selected as a whole. The source numerical banks motivate recognition of ordinary exponents and nearby order labels, without asserting recovered intention. Seventy meaningful bounded tasks are exhaustively checked; coefficient and variable aliases do not inflate counts.

Authored moderate: target and each of three highest orders1–3, forms0–2. Per-equation forms are D_n+3xD_1=x^5 y; sqrt(D_n+x)=3y^4; (D_n)^2+xD_1=y^5. Same first–third-order membership judgment in all forms, with one or two derivative occurrences; prime glyphs match observed source conventions. All252 meaningful tasks (3 target orders × C(9 distinct assessed equation shapes,3)) are exhaustively checked. Parallel equation permutations are aliases and are canonicalized jointly before rendering and identity; repeated assessed shapes are rejected, retaining three independent decisions. The second form reduces derivative occurrence count as in observed q-118782 but still requires reading derivative under a radical rather than confusing its power/placement with order.

Authored hard: target and each highest order4–8; lower m1..n−2; highest-derivative power2–5; ordinary exponent e in n+1..10; layout0–2. Define A=D_m(D_n)^p, B=x^eD_1, C=yD_(m+1). Layouts are A+B=C, A=B+C, B+C=A. Each has exactly four derivative occurrences; orders m and m+1 are lower than n, and highest power and ordinary exponent are irrelevant to true order. Boolean bank and full definition/check-each/conclusion solution remain fixed independently of a selected learner error. The factorized finite catalog has840 genuinely distinct per-equation structures, independently enumerated and parsed. Unordered sets of three distinct assessed equation shapes with five target orders total5×C(840,3)=492157400. This is a factorized bound, not a claim to render every triplet. Per-shape QA holds two other valid distinct companion shapes fixed; full joint tuples are sorted before rendering and identity. Equation-label permutations are aliases; identical repeated equations are ineligible. Powers/exponents and equation-side placement are retained because they create distinct order-versus-exponent/read-all-terms recognition tasks; symbol names, coefficients, profile and seed are excluded.

Mathematics reads back actual displayed derivatives independently in validate.py; exact derivative counts are confirmed with SymPy. Public generation stores domain, complete recipe set, source lineage, actual Python/SymPy versions, seed and original parameters outside learner content. Mathematical task identity excludes bank/profile/seed and coefficient magnitudes; content identity includes version, level, actual prompt, entire fixed solution, full displayed bank and correct values. Shuffling radio options cannot change identity. Distinct non-order coefficients are not exposed as purported task diversity.

All original profiles and variants appear in review.md/review.json, followed by at least two clearly labeled authored examples per level. No plots, native engine edits, database writes or post-step7 registration occur.

This is a local feedback-repair draft. The registered numeric script and its entire existing evidence tree are immutable; registered-baseline.json lists all65 full file paths with their original SHA256 hashes. validate.py rechecks exact file/directory coverage and every digest. The refreshed basis2275 wrapper contains14 original MA questions and zero independent inventory questions; independent-inventory.json records that separate current-inventory coverage. No generated inventory establishes observed difficulty labels.

The reported omission is repaired on all6 q-96676 answers. Feedback presence is exact on all73 answers (6 present,67 absent). Full derivative references and ordinal words are slots; y^5 and the square-root explanation stay fixed because they describe their respective source equations. Every one of the28 strictly increasing two-order maps from1–8 is independently checked:168 feedback instances. Changed orders above3 use an inline Leibniz derivative in feedback. Content identity includes feedback, while mathematical task identity excludes feedback, bank profiles and seed.

Source radio recipe definitions are explicit component operations rather than fitted offsets: highest/lowest/next-highest displayed derivative, ordinary independent/dependent exponent, and predecessor/successor order-count candidates. The complete seven scalar catalogs, including the one-answer blank, are mapped choice by choice. These operations reproduce the full original banks, but the historical author intent is underdetermined. Public observed replay therefore stays evidence-only; authored default banks have specified displayed-method operations. validate.py sweeps every bounded source order map, rejects colliding complete catalogs, and independently recomputes each eligible bank from the actual printed equation.

Independent QA parses the full printed equations to exact SymPy jet-coordinate expressions, verifies their ordinary x/y binding, and checks that the highest derivative survives simplification with nonzero coefficient. Negative controls cover zero/cancelled highest terms, foreign derivative variables, PDE notation, stale/drop/wrong-factor feedback, stale solution derivatives and changed-target solution text. Shared math-content normalization and checked_math_content run before identity and at the public API boundary; feedback is also explicitly normalized and validated. Native grading uses the unchanged memory-only engine; no registration, transactions, baseline edits or shared QA writes occur.

Authored three-equation questions require three distinct assessed shapes. Sampling chooses a complete eligible triplet without replacement; explicit duplicate inputs raise ValueError. Complete joint tuples (order, form, and hard lower-order/power/exponent slots) are sorted before presentation, parameter metadata and identity. Therefore all six permutations of one triplet have the same displayed question, owned fields/banks, full solution and mathematical/content IDs. Source replay keeps its original I/II/III ordering and feedback exactly. The moderate meaningful catalog is3×C(9,3)=252; hard is5×C(840,3)=492157400, with840 independently checked per-equation shapes. Canonical sorting positions are presentation roles, not extra assessed-task diversity. Authored eighth-order sentences use an; other ordinals use a. Matching, nonmatching and final classification cases plus article mutations are tested.
