# Four-stage template extraction



Provenance: {"database": "math", "basis": 1356, "lineage": "01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1"}. Source wrapper remains unchanged.



## 1. Describe each original specifically



Every original has three systems in a single unordered-list prompt, a fixed definition paragraph, a formal first-order equation display, a paragraph per system, and a final selection sentence. The exact original prompt and complete solution appear in review.md; all numerical/notation/condition components are listed below. Original difficulty is easy for every source.



### q-95985 (17592186167442)

- **I:** ODE `$2x{y}^{′}=y`; initial data `$y(0)=1`.

- **II:** ODE `${y}^{′}-2xy={e}^{y}`; no initial condition.

- **III:** ODE `$2x{y}^{″}={y}^{′}`; initial data `$y(1)=1,\,{y}^{′}(1)=1`.

Original complete fixed solution:

A first-order initial value problem (or IVP) is a first-order ordinary differential equation together with an initial condition that specifies a value of the unknown function at a point in its domain. A first-order initial value problem typically takes the form

$$
{y}^{′}=f(x,y),\,y({x}_{0})={y}_{0},
$$

where ${x}_{0}$ and ${y}_{0}$ are constants.

With that in mind, let's check each option.

- System I is a first-order initial value problem. It consists of a first-order differential equation $2x{y}^{′}=y$ together with the initial condition $y(0)=1.$

- System II is not a first-order initial value problem. We have a first-order ordinary differential equation, but there is no initial condition.

- System III is not a first-order initial value problem. It consists of a *second*-order differential equation $2x{y}^{″}={y}^{′}$ together with *two* initial conditions $y(1)=1,\,{y}^{′}(1)=1.$ This is a second-order initial value problem.

Therefore, the correct answer is "I only."



### q-96986 (17592186167499)

- **I:** ODE `$\frac{1}{2}{x}^{2}{y}^{″}=3{y}^{′}`; initial data `$y(1)=2,\,{y}^{′}(1)=1`.

- **II:** ODE `$2{x}^{2}{y}^{′}=y`; initial data `$y(0)=2`.

- **III:** ODE `$4{y}^{′}-\frac{1}{3}xy=\operatorname{ln}⁡y`; no initial condition.

Original complete fixed solution:

A first-order initial value problem (or IVP) is a first-order ordinary differential equation together with an initial condition that specifies a value of the unknown function at a point in its domain. A first-order initial value problem typically takes the form

$$
{y}^{′}=f(x,y),\,y({x}_{0})={y}_{0},
$$

where ${x}_{0}$ and ${y}_{0}$ are constants.

With that in mind, let's check each option.

- System I is not a first-order initial value problem. It consists of a *second*-order differential equation $\frac{1}{2}{x}^{2}{y}^{″}=3{y}^{′}$ together with *two* initial conditions $y(1)=2,\,{y}^{′}(1)=1.$ This is a second-order initial value problem.

- System II is a first-order initial value problem. It consists of a first-order differential equation $2{x}^{2}{y}^{′}=y$ together with the initial condition $y(0)=2.$

- System III is not a first-order initial value problem. We have a first-order ordinary differential equation, but there is no initial condition.

Therefore, the correct answer is "II only."



### q-118786 (17592186233254)

- **I:** ODE `$(1+{x}^{2}){y}^{′}=8y`; initial data `$y(-1)=3`.

- **II:** ODE `$8{y}^{′}-xy=3`; no initial condition.

- **III:** ODE `$3{y}^{″}=4y`; initial data `$y(-1)=0,\,{y}^{′}(-1)=1`.

Original complete fixed solution:

A first-order initial value problem (or IVP) is a first-order ordinary differential equation together with an initial condition that specifies a value of the unknown function at a point in its domain. A first-order initial value problem typically takes the form

$$
{y}^{′}=f(x,y),\,y({x}_{0})={y}_{0},
$$

where ${x}_{0}$ and ${y}_{0}$ are constants.

With that in mind, let's check each option.

- System I is a first-order initial value problem. It consists of a first-order differential equation $(1+{x}^{2}){y}^{′}=8y$ together with the initial condition $y(-1)=3.$

- System II is not a first-order initial value problem. We have a first-order ordinary differential equation, but there is no initial condition.

- System III is not a first-order initial value problem. It consists of a *second*-order differential equation $3{y}^{″}=4y$ together with *two* initial conditions $y(-1)=0,\,{y}^{′}(-1)=1.$ This is a second-order initial value problem.

Therefore, the correct answer is "I only."



### q-96987 (17592186234496)

- **I:** ODE `${x}^{2}{y}^{''}-y=2x`; initial data `$y(1)=1,\,{y}^{'}(1)=3`.

- **II:** ODE `$x{y}^{‴}-{e}^{x}{y}^{'}=9y`; initial data `$y(0)=1,\,{y}^{'}(0)=1,\,{y}^{''}(0)=2`.

- **III:** ODE `$2{y}^{'}-\frac{1}{x}={e}^{y}`; initial data `$y(0)=1`.

Original complete fixed solution:

A first-order initial value problem (or IVP) is a first-order ordinary differential equation together with an initial condition that specifies a value of the unknown function at a point in its domain. A first-order initial value problem typically takes the form

$$
{y}^{'}=f(x,y),\,y({x}_{0})={y}_{0},
$$

where ${x}_{0}$ and ${y}_{0}$ are constants.

With that in mind, let's check each option.

- System I is not a first-order initial value problem. It consists of a *second*-order differential equation ${x}^{2}{y}^{''}-y=2x$ together with *two* initial conditions $y(1)=1,\,{y}^{'}(1)=3.$ This is a second-order initial value problem.

- System II is not a first-order initial value problem. It consists of a *third*-order differential equation $x{y}^{‴}-{e}^{x}{y}^{'}=9y$ together with *three* initial conditions $y(0)=1,\,{y}^{'}(0)=1,$ and ${y}^{''}(0)=2.$ This is a third-order initial value problem.

- System III is a first-order initial value problem. It consists of a first-order differential equation $2{y}^{'}-\frac{1}{x}={e}^{y}$ together with the initial condition $y(0)=1.$

Therefore, the correct answer is "III only."



### q-96992 (17592186234497)

- **I:** ODE `$3{x}^{2}{y}^{′}={y}^{2}`; initial data `$y(0)=1`.

- **II:** ODE `$\frac{{y}^{′}}{2}-{x}^{2}{y}^{2}=y`; initial data `$y(1)=2`.

- **III:** ODE `${y}^{′}-x\sqrt{y}={e}^{x}`; no initial condition.

Original complete fixed solution:

A first-order initial value problem (or IVP) is a first-order ordinary differential equation together with an initial condition that specifies a value of the unknown function at a point in its domain. A first-order initial value problem typically takes the form

$$
{y}^{′}=f(x,y),\,y({x}_{0})={y}_{0},
$$

where ${x}_{0}$ and ${y}_{0}$ are constants.

With that in mind, let's check each option.

- System I is a first-order initial value problem. It consists of a first-order differential equation $3{x}^{2}{y}^{′}={y}^{2}$ together with the initial condition $y(0)=1.$

- System II is a first-order initial value problem. It consists of a first-order differential equation $\frac{{y}^{′}}{2}-{x}^{2}{y}^{2}=y$ together with the initial condition $y(1)=2.$

- System III  is not a first-order initial value problem. We have a first-order ordinary differential equation, but there is no initial condition.

Therefore, the correct answer is "I and II only."



### q-118787 (17592186253512)

- **I:** ODE `${y}^{′}-x=-7y`; initial data `$y(2)=3`.

- **II:** ODE `${x}^{4}{y}^{‴}+3y={2}^{y}`; initial data `$y(0)=1,\,{y}^{′}(0)=-1,\,{y}^{″}(0)=0`.

- **III:** ODE `$x{y}^{″}-6y=14`; initial data `$y(0)=-3,\,{y}^{′}(0)=3`.

Original complete fixed solution:

A first-order initial value problem (or IVP) is a first-order ordinary differential equation together with an initial condition that specifies a value of the unknown function at a point in its domain. A first-order initial value problem typically takes the form

$$
{y}^{′}=f(x,y),\,y({x}_{0})={y}_{0},
$$

where ${x}_{0}$ and ${y}_{0}$ are constants.

With that in mind, let's check each option.

- System I is a first-order initial value problem. It consists of a first-order differential equation ${y}^{′}-x=-7y$ together with the initial condition $y(2)=3.$

- System II is not a first-order initial value problem. It consists of a *third*-order differential equation ${x}^{4}{y}^{‴}+3y={2}^{y}$ together with *three* initial conditions $y(0)=1,\,{y}^{′}(0)=-1,$ and ${y}^{″}(0)=0.$ This is a third-order initial value problem.

- System III is not a first-order initial value problem. It consists of a *second*-order differential equation $x{y}^{″}-6y=14$ together with *two* initial conditions $y(0)=-3,\,{y}^{′}(0)=3.$ This is a second-order initial value problem.

Therefore, the correct answer is "I only."



### q-118788 (17592186253513)

- **I:** ODE `${x}^{2}{y}^{‴}+9{x}^{3}{y}^{′}=-7y`; initial data `$y(0)={y}^{′}(0)={y}^{″}(0)=-4`.

- **II:** ODE `$x{y}^{′}+{e}^{x}y=6`; initial data `$y(0)=2`.

- **III:** ODE `$6{y}^{″}+xy={e}^{x}`; no initial condition.

Original complete fixed solution:

A first-order initial value problem (or IVP) is a first-order ordinary differential equation together with an initial condition that specifies a value of the unknown function at a point in its domain. A first-order initial value problem typically takes the form

$$
{y}^{′}=f(x,y),\,y({x}_{0})={y}_{0},
$$

where ${x}_{0}$ and ${y}_{0}$ are constants.

With that in mind, let's check each option.

- System I is not a first-order initial value problem. It consists of a *third*-order differential equation ${x}^{2}{y}^{‴}+9{x}^{3}{y}^{′}=-7y$ together with *three* initial conditions $y(0)={y}^{′}(0)={y}^{″}(0)=-4.$ This is a third-order initial value problem.

- System II is a first-order initial value problem. It consists of a first-order differential equation $x{y}^{′}+{e}^{x}y=6$ together with the initial condition $y(0)=2.$

- System III is not a first-order initial value problem. We have here a second-order ordinary differential equation.

Therefore, the correct answer is "II only."



### q-118790 (17592186253514)

- **I:** ODE `${y}^{′}=-9x`; initial data `$y(1)=-4`.

- **II:** ODE `${y}^{′}-8{x}^{3}=-y`; initial data `$y(0)=-3`.

- **III:** ODE `${y}^{″}+y=3`; no initial condition.

Original complete fixed solution:

A first-order initial value problem (or IVP) is a first-order ordinary differential equation together with an initial condition that specifies a value of the unknown function at a point in its domain. A first-order initial value problem typically takes the form

$$
{y}^{′}=f(x,y),\,y({x}_{0})={y}_{0},
$$

where ${x}_{0}$ and ${y}_{0}$ are constants.

With that in mind, let's check each option.

- System I is a first-order initial value problem. It consists of a first-order differential equation ${y}^{′}=-9x$ together with the initial condition $y(1)=-4.$

- System II is a first-order initial value problem. It consists of a first-order differential equation ${y}^{′}-8{x}^{3}=-y$ together with the initial condition $y(0)=-3.$

- System III is not a first-order initial value problem. We have here a second-order ordinary differential equation.

Therefore, the correct answer is "I and II only."



### q-118791 (17592186253515)

- **I:** ODE `${y}^{‴}+{y}^{″}+{y}^{′}+y=0`; initial data `$y(1)={y}^{′}(1)={y}^{″}(1)=2`.

- **II:** ODE `${y}^{′}\operatorname{ln}⁡x+y={3}^{x}`; initial data `$y(1)=6`.

- **III:** ODE `$\sqrt{x}{y}^{′}+{e}^{x}y=6`; initial data `$y(4)=-3`.

Original complete fixed solution:

A first-order initial value problem (or IVP) is a first-order ordinary differential equation together with an initial condition that specifies a value of the unknown function at a point in its domain. A first-order initial value problem typically takes the form

$$
{y}^{′}=f(x,y),\,y({x}_{0})={y}_{0},
$$

where ${x}_{0}$ and ${y}_{0}$ are constants.

With that in mind, let's check each option.

- System I is not a first-order initial value problem. It consists of a *third*-order differential equation ${y}^{‴}+{y}^{″}+{y}^{′}+y=0$ together with *three* initial conditions $y(1)={y}^{′}(1)={y}^{″}(1)=2.$ This is a third-order initial value problem.

- System II is a first-order initial value problem. It consists of a first-order differential equation ${y}^{′}\operatorname{ln}⁡x+y={3}^{x}$ together with the initial condition $y(1)=6.$

- System III is a first-order initial value problem. It consists of a first-order differential equation $\sqrt{x}{y}^{′}+{e}^{x}y=6$ together with the initial condition $y(4)=-3.$

Therefore, the correct answer is "II and III only."



### q-96988 (17592186360737)

- **I:** ODE `$2x-{y}^{′}=\frac{1}{y}`; no initial condition.

- **II:** ODE `$3{y}^{′}-2{e}^{x}y={y}^{2}`; initial data `$y(\operatorname{ln}⁡2)=1`.

- **III:** ODE `$2x{y}^{″}-\frac{1}{x}={y}^{′}`; initial data `$y(2)=1,\,{y}^{′}(2)=1`.

Original complete fixed solution:

A first-order initial value problem (or IVP) is a first-order ordinary differential equation together with an initial condition that specifies a value of the unknown function at a point in its domain. A first-order initial value problem typically takes the form

$$
{y}^{′}=f(x,y),\,y({x}_{0})={y}_{0},
$$

where ${x}_{0}$ and ${y}_{0}$ are constants.

With that in mind, let's check each option.

- System I  is not a first-order initial value problem. We have a first-order ordinary differential equation, but there is no initial condition.

- System II is a first-order initial value problem. It consists of a first-order differential equation $3{y}^{′}-2{e}^{x}y={y}^{2}$ together with the initial condition $y(\operatorname{ln}⁡2)=1.$

- System III is not a first-order initial value problem. It consists of a *second*-order differential equation $2x{y}^{″}-\frac{1}{x}={y}^{′}$ together with *two* initial conditions $y(2)=1,\,{y}^{′}(2)=1.$ This is a second-order initial value problem.

Therefore, the correct answer is "II only."



### q-96990 (17592186360738)

- **I:** ODE `${x}^{3}{y}^{′}-\sqrt{x}=\operatorname{ln}⁡y`; initial data `$y(1)=1`.

- **II:** ODE `$\sqrt{x}{y}^{‴}-x{y}^{′}=\frac{y}{4}`; initial data `$y(0)=2,\,{y}^{′}(0)=2,\,{y}^{″}(0)=1`.

- **III:** ODE `$\sqrt{3}{y}^{′}-3x=2y`; initial data `$y(\operatorname{cos}⁡2)=1`.

Original complete fixed solution:

A first-order initial value problem (or IVP) is a first-order ordinary differential equation together with an initial condition that specifies a value of the unknown function at a point in its domain. A first-order initial value problem typically takes the form

$$
{y}^{′}=f(x,y),\,y({x}_{0})={y}_{0},
$$

where ${x}_{0}$ and ${y}_{0}$ are constants.

With that in mind, let's check each option.

- System I is a first-order initial value problem. It consists of a first-order differential equation ${x}^{3}{y}^{′}-\sqrt{x}=\operatorname{ln}⁡y$ together with the initial condition $y(1)=1.$

- System II is not a first-order initial value problem. It consists of a *third*-order differential equation $\sqrt{x}{y}^{‴}-x{y}^{′}=\frac{y}{4}$ together with *three* initial conditions $y(0)=2,\,{y}^{′}(0)=2,$ and ${y}^{″}(0)=1.$ This is a third-order initial value problem.

- System III is a first-order initial value problem. It consists of a first-order differential equation $\sqrt{3}{y}^{′}-3x=2y$ together with the initial condition $y(\operatorname{cos}⁡2)=1.$

Therefore, the correct answer is "I and III only."



## 2. Generalize the shared pattern



The question asks for the finite subset of systems that combine an order-1 ODE with an explicit value of y at a constant point. Check the highest displayed derivative, then check the supplied point value. Higher-order systems can be IVPs generally but are not **first-order** IVPs. No ODE is solved; no consistency or existence theorem is required. Every checkbox owns the two text values false/true, so the wrong value is the exact logical negation of the displayed system classification. The known q-96987 point-domain defect is kept separately from formal order-and-condition fidelity.



## 3. Map complete components and every original choice



The coefficient slots below are complete ODE component recipes. Initial data have one constant point slot per system and one last-value slot per separate or chained fragment. In a chain all displayed function/derivative values share that last value. Every original answer UUID and designation is listed; no wrong-choice intent is unresolved. The recipes derive true/false from the actual printed structure; there is no source-ID answer table.



### source_q-95985; profile observed_raw

Parameter values:

```json

{
  "a": 2,
  "b": 2,
  "c": 2,
  "conditions": [
    {
      "point": "0",
      "values": [
        "1"
      ]
    },
    null,
    {
      "point": "1",
      "values": [
        "1",
        "1"
      ]
    }
  ]
}

```

ODE component masks:

- I: `@a@x{y}^{′}=y`

- II: `{y}^{′}-@b@xy={e}^{y}`

- III: `@c@x{y}^{″}={y}^{′}`

Complete answer bank mapping:

- Field I, `b3c3a223-c2a8-5949-b84f-fa769ba4b994`: text `false`; incorrect, logical negation of the structural predicate.

- Field I, `2a84d494-2aef-50d3-8cf8-8db249714a50`: text `true`; correct, derived structural predicate.

- Field II, `cc5c8df0-0441-5501-a1ad-fe7911ffce95`: text `false`; correct, derived structural predicate.

- Field II, `077d77c6-30fd-55f9-a1d3-9a54c78855cc`: text `true`; incorrect, logical negation of the structural predicate.

- Field III, `64826bbf-2236-5228-a180-82aed0ae287a`: text `false`; correct, derived structural predicate.

- Field III, `b08b77cf-69a9-541b-947c-c12cefd2115b`: text `true`; incorrect, logical negation of the structural predicate.



### source_q-96986; profile observed_raw

Parameter values:

```json

{
  "a": 2,
  "b": 3,
  "c": 2,
  "d": 4,
  "e": 3,
  "conditions": [
    {
      "point": "1",
      "values": [
        "2",
        "1"
      ]
    },
    {
      "point": "0",
      "values": [
        "2"
      ]
    },
    null
  ]
}

```

ODE component masks:

- I: `\frac{1}{@a@}{x}^{2}{y}^{″}=@b@{y}^{′}`

- II: `@c@{x}^{2}{y}^{′}=y`

- III: `@d@{y}^{′}-\frac{1}{@e@}xy=\operatorname{ln}⁡y`

Complete answer bank mapping:

- Field I, `9b1657ec-ee94-56ab-9624-eb98b93a3f8f`: text `false`; correct, derived structural predicate.

- Field I, `7ba78363-9c7b-5138-bdae-fcc1c1e8b161`: text `true`; incorrect, logical negation of the structural predicate.

- Field II, `3baf4f4e-994c-5a3d-8cd7-a08d6815e9e7`: text `false`; incorrect, logical negation of the structural predicate.

- Field II, `ca77a9c5-67ca-5442-a2b6-728548b85c73`: text `true`; correct, derived structural predicate.

- Field III, `e9b50315-f8d9-5f53-a15e-c35152183cd5`: text `false`; correct, derived structural predicate.

- Field III, `00362934-c6f7-5519-a9c5-57cedf485a65`: text `true`; incorrect, logical negation of the structural predicate.



### source_q-118786; profile observed_raw

Parameter values:

```json

{
  "a": 8,
  "b": 8,
  "c": 3,
  "d": 3,
  "e": 4,
  "conditions": [
    {
      "point": "-1",
      "values": [
        "3"
      ]
    },
    null,
    {
      "point": "-1",
      "values": [
        "0",
        "1"
      ]
    }
  ]
}

```

ODE component masks:

- I: `(1+{x}^{2}){y}^{′}=@a@y`

- II: `@b@{y}^{′}-xy=@c@`

- III: `@d@{y}^{″}=@e@y`

Complete answer bank mapping:

- Field I, `853427ec-ff39-510f-b5b9-b9b3063c4fc0`: text `false`; incorrect, logical negation of the structural predicate.

- Field I, `26f5c7b4-02a7-523d-971a-7bb512830680`: text `true`; correct, derived structural predicate.

- Field II, `2303430c-0704-550c-b6ae-374bc966f21d`: text `false`; correct, derived structural predicate.

- Field II, `a9a09a9d-3bac-5120-8742-15c47fbf484c`: text `true`; incorrect, logical negation of the structural predicate.

- Field III, `6e36a2e5-c84a-5bb7-86bc-439a8b342c25`: text `false`; correct, derived structural predicate.

- Field III, `707a477f-c377-547a-845c-170d00c19430`: text `true`; incorrect, logical negation of the structural predicate.



### source_q-96987; profile observed_raw

Parameter values:

```json

{
  "a": 2,
  "b": 9,
  "c": 2,
  "conditions": [
    {
      "point": "1",
      "values": [
        "1",
        "3"
      ]
    },
    {
      "point": "0",
      "values": [
        "1",
        "1",
        "2"
      ]
    },
    {
      "point": "0",
      "values": [
        "1"
      ]
    }
  ]
}

```

ODE component masks:

- I: `{x}^{2}{y}^{''}-y=@a@x`

- II: `x{y}^{‴}-{e}^{x}{y}^{'}=@b@y`

- III: `@c@{y}^{'}-\frac{1}{x}={e}^{y}`

Complete answer bank mapping:

- Field I, `31ed816f-dcc9-55e7-a7ee-b8893ddc6b9c`: text `false`; correct, derived structural predicate.

- Field I, `7c033af8-4e67-5059-a3d7-2ee152e006ff`: text `true`; incorrect, logical negation of the structural predicate.

- Field II, `891fce35-cd60-5014-954c-b452492c406b`: text `false`; correct, derived structural predicate.

- Field II, `c19a760c-5182-53bb-9e1c-45300e79eda9`: text `true`; incorrect, logical negation of the structural predicate.

- Field III, `f1015ba8-7c86-5225-bd73-031db89ebe78`: text `false`; captured as incorrect under order-and-condition recognition. At the displayed x=0 the ODE is undefined, so this designation is a documented source domain-wording issue.

- Field III, `7b79acea-a0fa-5455-a4fd-773c08b30342`: text `true`; captured as correct under order-and-condition recognition; fails the lesson's point-domain requirement at x=0. Exact replay is evidence-only; the repaired profile changes this point to 2.



### source_q-96992; profile observed_raw

Parameter values:

```json

{
  "a": 3,
  "b": 2,
  "conditions": [
    {
      "point": "0",
      "values": [
        "1"
      ]
    },
    {
      "point": "1",
      "values": [
        "2"
      ]
    },
    null
  ]
}

```

ODE component masks:

- I: `@a@{x}^{2}{y}^{′}={y}^{2}`

- II: `\frac{{y}^{′}}{@b@}-{x}^{2}{y}^{2}=y`

- III: `{y}^{′}-x\sqrt{y}={e}^{x}`

Complete answer bank mapping:

- Field I, `8efe158e-5199-5887-8b3f-0d56b86243f5`: text `false`; incorrect, logical negation of the structural predicate.

- Field I, `802b1980-87f7-5e28-9c43-ca80dce3ab91`: text `true`; correct, derived structural predicate.

- Field II, `7b3fe1fd-a8ce-5d7b-bd4f-b4fbe96c661f`: text `false`; incorrect, logical negation of the structural predicate.

- Field II, `82cb1afb-17dc-54bc-9444-9e13f04751f4`: text `true`; correct, derived structural predicate.

- Field III, `82a05862-f216-5d32-b34b-f327419d2f68`: text `false`; correct, derived structural predicate.

- Field III, `f8675194-82ce-500b-a188-7d2c2088e9ae`: text `true`; incorrect, logical negation of the structural predicate.



### source_q-118787; profile observed_raw

Parameter values:

```json

{
  "a": 7,
  "b": 3,
  "c": 2,
  "d": 6,
  "e": 14,
  "conditions": [
    {
      "point": "2",
      "values": [
        "3"
      ]
    },
    {
      "point": "0",
      "values": [
        "1",
        "-1",
        "0"
      ]
    },
    {
      "point": "0",
      "values": [
        "-3",
        "3"
      ]
    }
  ]
}

```

ODE component masks:

- I: `{y}^{′}-x=-@a@y`

- II: `{x}^{4}{y}^{‴}+@b@y={@c@}^{y}`

- III: `x{y}^{″}-@d@y=@e@`

Complete answer bank mapping:

- Field I, `8fc37352-81e0-514c-bedf-fa91579d6398`: text `false`; incorrect, logical negation of the structural predicate.

- Field I, `00fbec5e-2569-5e70-887a-76fd721447ec`: text `true`; correct, derived structural predicate.

- Field II, `6d471821-5101-5272-a1e9-64c5df191a7c`: text `false`; correct, derived structural predicate.

- Field II, `e79714fa-47cd-53d1-87a1-cb84a5b63e67`: text `true`; incorrect, logical negation of the structural predicate.

- Field III, `4d77c166-99a6-5b75-9890-9bbf922be8bb`: text `false`; correct, derived structural predicate.

- Field III, `d2d66aee-5929-509b-ad21-8bd403ae74fa`: text `true`; incorrect, logical negation of the structural predicate.



### source_q-118788; profile observed_raw

Parameter values:

```json

{
  "a": 9,
  "b": 7,
  "c": 6,
  "d": 6,
  "conditions": [
    {
      "point": "0",
      "values": [
        "-4"
      ]
    },
    {
      "point": "0",
      "values": [
        "2"
      ]
    },
    null
  ]
}

```

ODE component masks:

- I: `{x}^{2}{y}^{‴}+@a@{x}^{3}{y}^{′}=-@b@y`

- II: `x{y}^{′}+{e}^{x}y=@c@`

- III: `@d@{y}^{″}+xy={e}^{x}`

Complete answer bank mapping:

- Field I, `289bb35b-99fe-5106-99b0-f71c04163a88`: text `false`; correct, derived structural predicate.

- Field I, `2302fbb6-0adc-5661-bbf7-af76484dacc0`: text `true`; incorrect, logical negation of the structural predicate.

- Field II, `beef713f-b9cc-55dc-8f1d-6cf37ec09f6e`: text `false`; incorrect, logical negation of the structural predicate.

- Field II, `e499fae0-7b48-5f3b-93bb-81ab64c9da66`: text `true`; correct, derived structural predicate.

- Field III, `aac407af-d819-550f-805d-c2f156435fe9`: text `false`; correct, derived structural predicate.

- Field III, `983242a4-a136-5392-8243-ada487eed7f7`: text `true`; incorrect, logical negation of the structural predicate.



### source_q-118790; profile observed_raw

Parameter values:

```json

{
  "a": 9,
  "b": 8,
  "c": 3,
  "conditions": [
    {
      "point": "1",
      "values": [
        "-4"
      ]
    },
    {
      "point": "0",
      "values": [
        "-3"
      ]
    },
    null
  ]
}

```

ODE component masks:

- I: `{y}^{′}=-@a@x`

- II: `{y}^{′}-@b@{x}^{3}=-y`

- III: `{y}^{″}+y=@c@`

Complete answer bank mapping:

- Field I, `d275665e-21d6-5021-9af4-963d5728df52`: text `false`; incorrect, logical negation of the structural predicate.

- Field I, `c3b7cd67-3643-54bb-814b-c0117b35907e`: text `true`; correct, derived structural predicate.

- Field II, `9417f602-3568-5efe-94c7-501d5cff75d2`: text `false`; incorrect, logical negation of the structural predicate.

- Field II, `86b7ef39-bf9a-54c6-a085-f31d633793e8`: text `true`; correct, derived structural predicate.

- Field III, `89bb1fe1-b3be-5274-ac26-302e27a47abf`: text `false`; correct, derived structural predicate.

- Field III, `7ab84d7e-d700-5891-a5c2-71baae4994b4`: text `true`; incorrect, logical negation of the structural predicate.



### source_q-118791; profile observed_raw

Parameter values:

```json

{
  "a": 3,
  "b": 6,
  "conditions": [
    {
      "point": "1",
      "values": [
        "2"
      ]
    },
    {
      "point": "1",
      "values": [
        "6"
      ]
    },
    {
      "point": "4",
      "values": [
        "-3"
      ]
    }
  ]
}

```

ODE component masks:

- I: `{y}^{‴}+{y}^{″}+{y}^{′}+y=0`

- II: `{y}^{′}\operatorname{ln}⁡x+y={@a@}^{x}`

- III: `\sqrt{x}{y}^{′}+{e}^{x}y=@b@`

Complete answer bank mapping:

- Field I, `0e5caf84-b369-53c1-92d8-3daf6511f002`: text `false`; correct, derived structural predicate.

- Field I, `d814dbc8-353f-574a-8589-9891a880a534`: text `true`; incorrect, logical negation of the structural predicate.

- Field II, `fccfea10-d196-5af8-881d-6efaf713593e`: text `false`; incorrect, logical negation of the structural predicate.

- Field II, `26116a3c-17a4-5e07-abc8-396b55612f60`: text `true`; correct, derived structural predicate.

- Field III, `10764352-ef44-5719-87cb-3b2d8938735f`: text `false`; incorrect, logical negation of the structural predicate.

- Field III, `e37e4e1a-2748-569f-9af1-4faf43505566`: text `true`; correct, derived structural predicate.



### source_q-96988; profile observed_raw

Parameter values:

```json

{
  "a": 2,
  "b": 3,
  "c": 2,
  "d": 2,
  "conditions": [
    null,
    {
      "point": "\\operatorname{ln}⁡2",
      "values": [
        "1"
      ]
    },
    {
      "point": "2",
      "values": [
        "1",
        "1"
      ]
    }
  ]
}

```

ODE component masks:

- I: `@a@x-{y}^{′}=\frac{1}{y}`

- II: `@b@{y}^{′}-@c@{e}^{x}y={y}^{2}`

- III: `@d@x{y}^{″}-\frac{1}{x}={y}^{′}`

Complete answer bank mapping:

- Field I, `33d1ca0c-c077-564f-bbd3-6bd589f331e1`: text `false`; correct, derived structural predicate.

- Field I, `87ce1d0c-32be-5143-a872-7d49dc66b488`: text `true`; incorrect, logical negation of the structural predicate.

- Field II, `5727dd59-2f56-5c06-9b43-b63ff7c2bfb7`: text `false`; incorrect, logical negation of the structural predicate.

- Field II, `842ba921-5998-5c95-bb52-17e348e3161e`: text `true`; correct, derived structural predicate.

- Field III, `6b8203d5-1002-51cb-9411-d4a83fc42ace`: text `false`; correct, derived structural predicate.

- Field III, `ad4c0de1-0610-56fb-9005-f107985bbfef`: text `true`; incorrect, logical negation of the structural predicate.



### source_q-96990; profile observed_raw

Parameter values:

```json

{
  "a": 4,
  "b": 3,
  "c": 3,
  "d": 2,
  "conditions": [
    {
      "point": "1",
      "values": [
        "1"
      ]
    },
    {
      "point": "0",
      "values": [
        "2",
        "2",
        "1"
      ]
    },
    {
      "point": "\\operatorname{cos}⁡2",
      "values": [
        "1"
      ]
    }
  ]
}

```

ODE component masks:

- I: `{x}^{3}{y}^{′}-\sqrt{x}=\operatorname{ln}⁡y`

- II: `\sqrt{x}{y}^{‴}-x{y}^{′}=\frac{y}{@a@}`

- III: `\sqrt{@b@}{y}^{′}-@c@x=@d@y`

Complete answer bank mapping:

- Field I, `dc873da1-dcb5-58cd-bcdc-f6dfaecd44eb`: text `false`; incorrect, logical negation of the structural predicate.

- Field I, `aabe49eb-f60e-59a4-8e8e-b51a643069e1`: text `true`; correct, derived structural predicate.

- Field II, `1e61410e-bb7d-5fd5-a42c-93728f72a519`: text `false`; correct, derived structural predicate.

- Field II, `3904d9fc-81e9-58dc-b100-87ee0a13dfc3`: text `true`; incorrect, logical negation of the structural predicate.

- Field III, `4347d9eb-3074-5e4f-bb59-94bee475caab`: text `false`; incorrect, logical negation of the structural predicate.

- Field III, `82b802ce-94eb-52a4-a016-7da0aee33a6b`: text `true`; correct, derived structural predicate.



## 4. Extract reusable Markdown/value templates



Observed templates share fixed opening/request text and a fixed formal display. Each numbered system owns a complete ODE slot and, when present, whole initial-condition fragment slots. Slots are installed simultaneously **inside math spans in that system only** before values are inserted. The source worked solution uses those identical component slots in its original paragraphs. Its original sequence, spaces, punctuation, equation notation, missing-equation paragraphs, and final selection sentence are retained. There is exactly one solution independent of any learner selection. Changing coefficients never changes the source recipe order or initial-condition layout.



For original source parameters, observed_raw is an exact full-prompt/full-solution/bank replay. All raw profiles are evidence_only=true and eligible_for_learning=false. The observed_regular profile uses the same recipe and wording, with positive integer coefficients 2–9, point slots 2–4 and value slots 1–6 (positive ln arguments). Public explicit observed coefficients admit 1–14 to include every captured coefficient, points have magnitude at most 4 or familiar source ln/cos constants, and initial values have magnitude at most 6. No classification arithmetic is performed on these coefficients, so larger source coefficient 14 creates no harder calculation. Explicit invalid inputs are rejected rather than resampled.



The q-96987-only observed_domain_repair profile permits its otherwise-original defined-point data, requiring a positive nonzero integer point 1–4 for the literal 1/x system. With no parameters supplied it changes only that point from 0 to 2, including the corresponding worked-solution slot. Raw source-domain correctness and designation reproduction are reported separately.



Authored defaults use one complete boolean bank before constructing any options; the only wrong answer is logical negation. There is no pool, no fitted scalar distractor, no numerical-collision problem and no answer feedback. The three categorical component choices are selected together from an enumerated eligible catalog; at least one system is true and at least one is false. Moderate/hard additionally require at least one order-2/3 system. No derivative-only condition was added.



Authored masks: easy `a y^(n)=b x+y`; moderate `(a+x²)y^(n)+b L=e^x`, with L=y for order 1 and L=y′ for higher orders; hard `(a+x²)(d^n y/dx^n-b y)+x y′=e^x`. Conditions are absent, y(t)=v for order 1, two explicit conditions for easy order 2, chained equalities for moderate higher order, or separately supplied derivative values for hard. Highest derivatives are already displayed; no nested differentiation is requested. Bounds and workload distinctions are in classification.md and the individual generator entrypoint sections.



Plot extraction (step 5): none. Plot generation (step 7): none. No reference images occur in prompt, banks, or fixed solutions.



Identity: presentation UUIDs include generator version, actual difficulty, complete displayed prompt, complete fixed solution and owned complete bank. Order shuffling and profile aliases do not create new content identities. Mathematical fingerprints exclude incidental numbers and complete banks. Authored fingerprints retain the actual notation/scan workload and an unordered multiset of condition/order categories. The meaningful finite catalogs are 9/12/12; the separate 36/54/54 counts describe ordered display layouts, not additional mathematical tasks. Source fingerprints likewise canonicalize system order. No unbounded number diversity is claimed.



Independent validation parses the actual displayed ODE as a formal residual and finds the highest surviving derivative symbol. It separately reads every initial-condition chain, compares each fixed-solution equation and point/value component, confirms all boolean values, checks complete source strings and attribute-presence parity, and uses all owned choices in the native grader. Numeric alias, changed-parameter, boundary and invalid-input checks are separate from fidelity.
