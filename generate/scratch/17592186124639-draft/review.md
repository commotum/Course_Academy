# Original Math Academy sources and generated variants

Immutable basis 2275; all original records retained in source.json.

## Original q-132241

Find $f_{y}(x, y)$ for $f(x, y) = xy^{2} + x^{2}\cos y$.

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "bf04fd45-6472-58ca-94d4-d15d2e211452",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2xy - x^{2}\\sin y",
        ":db/id": 17592186121314
      },
      {
        ":answer/id": "e86f2714-6951-57a6-9a39-8cf927f5a779",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2y - \\sin y",
        ":db/id": 17592186121315
      },
      {
        ":answer/id": "f1c60716-d08f-5601-a61d-2122e60c3f07",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "y^{2} + 2x\\sin y",
        ":db/id": 17592186121316
      },
      {
        ":answer/id": "f9c2f3ce-5cce-5e2c-9e3f-2b7a5ddf7527",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "y^{2} - 2x\\sin y",
        ":db/id": 17592186121317
      },
      {
        ":answer/id": "5027f72a-8193-5afe-a1d0-c7fc0aa88343",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2xy + x^{2}\\sin y",
        ":db/id": 17592186121318
      }
    ],
    ":answer-field/id": "ea625c07-3c2c-5ede-a249-984720aa8ae8",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186121313
  }
]

Original solution absent; not counted as matched.

### easy — cos_poly

Bank profile: `completed`

Find $f_{x}(x, y)$ for $f(x, y) = x^{2} y+8 y^{3} \cos{\left(x \right)}$.

Field `selection` — :answer-field.type/radio

- $x^{2} - 24 y^{2} \sin{\left(x \right)}$

- $2 x y + 8 y^{3} \sin{\left(x \right)}$

- $2 x y - 8 y^{3} \sin{\left(x \right)}$ **correct**

- $x^{2} + 24 y^{2} \sin{\left(x \right)}$

- $2 x - 8 \sin{\left(x \right)}$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(x^{2} y+8 y^{3} \cos{\left(x \right)}) \\  & =\frac{∂}{∂x}(x^{2} y)+\frac{∂}{∂x}(8 y^{3} \cos{\left(x \right)}) \\  & =y\cdot \frac{∂}{∂x}(x^{2})+8 y^{3}\cdot \frac{∂}{∂x}(\cos{\left(x \right)}) \\  & =y\cdot 2 x+8 y^{3}\cdot (- \sin{\left(x \right)}) \\  & =2 x y - 8 y^{3} \sin{\left(x \right)}\end{aligned}
$$

### easy — cos_poly

Bank profile: `completed`

Find $f_{x}(x, y)$ for $f(x, y) = 2 x^{2} y+4 y^{3} \cos{\left(x \right)}$.

Field `selection` — :answer-field.type/radio

- $4 x y - 4 y^{3} \sin{\left(x \right)}$ **correct**

- $4 x - 4 \sin{\left(x \right)}$

- $2 x^{2} - 12 y^{2} \sin{\left(x \right)}$

- $2 x^{2} + 12 y^{2} \sin{\left(x \right)}$

- $4 x y + 4 y^{3} \sin{\left(x \right)}$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(2 x^{2} y+4 y^{3} \cos{\left(x \right)}) \\  & =\frac{∂}{∂x}(2 x^{2} y)+\frac{∂}{∂x}(4 y^{3} \cos{\left(x \right)}) \\  & =2 y\cdot \frac{∂}{∂x}(x^{2})+4 y^{3}\cdot \frac{∂}{∂x}(\cos{\left(x \right)}) \\  & =2 y\cdot 2 x+4 y^{3}\cdot (- \sin{\left(x \right)}) \\  & =4 x y - 4 y^{3} \sin{\left(x \right)}\end{aligned}
$$

## Original q-35709

Find $\frac{∂f}{∂x}$ given that $f(x,y)={x}^{2}\operatorname{sin}⁡y+xy.$

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "3d51dd88-5fb4-58d8-b18a-5b73f6038ce2",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "{x}^{2}\\operatorname{cos}⁡y+y",
        ":db/id": 17592186321625
      },
      {
        ":answer/id": "4e0a7575-fad3-5707-8f9c-c326fac5c503",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "{x}^{2}\\operatorname{cos}⁡y+x",
        ":db/id": 17592186321762
      },
      {
        ":answer/id": "7057a38f-1089-58e3-bde4-e5476dcb3488",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "x\\operatorname{sin}⁡y+x",
        ":db/id": 17592186322024
      },
      {
        ":answer/id": "82655c13-b022-54cb-aa00-3eb726e84da0",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2x\\operatorname{sin}⁡y+y",
        ":db/id": 17592186322175
      },
      {
        ":answer/id": "840b82a4-0f9f-5b0b-83ec-b64aea5d144b",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2y\\operatorname{sin}⁡y+x",
        ":db/id": 17592186322189
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "82655c13-b022-54cb-aa00-3eb726e84da0",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "2x\\operatorname{sin}⁡y+y",
      ":db/id": 17592186322175
    },
    ":answer-field/id": "1b693047-cc14-523f-9435-46452a8f9f15",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186323222
  }
]

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}({x}^{2}\operatorname{sin}⁡y+xy) \\  & =\frac{∂}{∂x}({x}^{2}\operatorname{sin}⁡y)+\frac{∂}{∂x}(xy) \\  & =\operatorname{sin}⁡y\cdot \frac{∂}{∂x}({x}^{2})+y\cdot \frac{∂}{∂x}(x) \\  & =\operatorname{sin}⁡y\cdot (2x)+y\cdot (1) \\  & =2x\operatorname{sin}⁡y+y\end{aligned}
$$

### easy — sin_poly

Bank profile: `observed`

Find $\frac{∂f}{∂y}$ given that $f(x,y)=y^{2} \sin{\left(x \right)}+8 x y.$

Field `selection` — :answer-field.type/radio

- $8 x + 2 y \sin{\left(x \right)}$ **correct**

- $2 x \sin{\left(x \right)} + 8 y$

- $8 x + y^{2} \cos{\left(x \right)}$

- $y \sin{\left(x \right)} + 8 y$

- $y^{2} \cos{\left(x \right)} + 8 y$

We differentiate the given function with respect to $y,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(y^{2} \sin{\left(x \right)}+8 x y) \\  & =\frac{∂}{∂y}(y^{2} \sin{\left(x \right)})+\frac{∂}{∂y}(8 x y) \\  & =\sin{\left(x \right)}\cdot \frac{∂}{∂y}(y^{2})+8 x\cdot \frac{∂}{∂y}(y) \\  & =\sin{\left(x \right)}\cdot (2 y)+8 x\cdot (1) \\  & =8 x + 2 y \sin{\left(x \right)}\end{aligned}
$$

### easy — sin_poly

Bank profile: `observed`

Find $\frac{∂f}{∂y}$ given that $f(x,y)=2 y^{2} \sin{\left(x \right)}+4 x y.$

Field `selection` — :answer-field.type/radio

- $4 x + 2 y^{2} \cos{\left(x \right)}$

- $2 y^{2} \cos{\left(x \right)} + 4 y$

- $4 x + 4 y \sin{\left(x \right)}$ **correct**

- $2 y \sin{\left(x \right)} + 4 y$

- $4 x \sin{\left(x \right)} + 4 y$

We differentiate the given function with respect to $y,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(2 y^{2} \sin{\left(x \right)}+4 x y) \\  & =\frac{∂}{∂y}(2 y^{2} \sin{\left(x \right)})+\frac{∂}{∂y}(4 x y) \\  & =2 \sin{\left(x \right)}\cdot \frac{∂}{∂y}(y^{2})+4 x\cdot \frac{∂}{∂y}(y) \\  & =2 \sin{\left(x \right)}\cdot (2 y)+4 x\cdot (1) \\  & =4 x + 4 y \sin{\left(x \right)}\end{aligned}
$$

## Original q-159613

Find $\frac{∂f}{∂y}$ given that $f(x,y)=xy+{x}^{2}\operatorname{ln}⁡y.$

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "19f6c148-0885-5d60-9101-a64f4e2c0577",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "x+\\frac{{x}^{2}}{y}",
        ":db/id": 17592186275720
      },
      {
        ":answer/id": "48d4574b-09ae-5cd7-8667-6addc311e93c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "xy+\\frac{{x}^{2}}{y}",
        ":db/id": 17592186276125
      },
      {
        ":answer/id": "5524be5e-28f5-5433-a5d3-d73957b779a9",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "x+{x}^{2}\\operatorname{ln}⁡y",
        ":db/id": 17592186276234
      },
      {
        ":answer/id": "60ced972-1fd7-5d9e-89b4-5b1ed89abe9f",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "y+2x\\operatorname{ln}⁡y",
        ":db/id": 17592186276347
      },
      {
        ":answer/id": "c6e6df92-0fe0-52bf-ad68-64d6651fef07",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "y+\\frac{2x}{y}",
        ":db/id": 17592186277246
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "19f6c148-0885-5d60-9101-a64f4e2c0577",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "x+\\frac{{x}^{2}}{y}",
      ":db/id": 17592186275720
    },
    ":answer-field/id": "9501b870-d0cb-5b61-aa64-68a74b0b08a3",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186277990
  }
]

We differentiate the given function with respect to $y,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(xy+{x}^{2}\operatorname{ln}⁡y) \\  & =\frac{∂}{∂y}(xy)+\frac{∂}{∂y}({x}^{2}\operatorname{ln}⁡y) \\  & =x\cdot \frac{∂}{∂y}(y)+{x}^{2}\cdot \frac{∂}{∂y}(\operatorname{ln}⁡y) \\  & =x\cdot 1+{x}^{2}\cdot \frac{1}{y} \\  & =x+\frac{{x}^{2}}{y}\end{aligned}
$$

### easy — log

Bank profile: `observed`

Find $\frac{∂f}{∂y}$ given that $f(x,y)=x y+8 x^{2} \ln{\left(y \right)}.$

Field `selection` — :answer-field.type/radio

- $16 x \ln{\left(y \right)} + y$

- $\frac{16 x}{y} + y$

- $\frac{8 x^{2}}{y} + x$ **correct**

- $8 x^{2} \ln{\left(y \right)} + x$

- $\frac{8 x^{2}}{y} + x y$

We differentiate the given function with respect to $y,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(x y+8 x^{2} \ln{\left(y \right)}) \\  & =\frac{∂}{∂y}(x y)+\frac{∂}{∂y}(8 x^{2} \ln{\left(y \right)}) \\  & =x\cdot \frac{∂}{∂y}(y)+8 x^{2}\cdot \frac{∂}{∂y}(\ln{\left(y \right)}) \\  & =x\cdot 1+8 x^{2}\cdot \frac{1}{y} \\  & =\frac{8 x^{2}}{y} + x\end{aligned}
$$

### easy — log

Bank profile: `observed`

Find $\frac{∂f}{∂y}$ given that $f(x,y)=2 x y+4 x^{2} \ln{\left(y \right)}.$

Field `selection` — :answer-field.type/radio

- $\frac{4 x^{2}}{y} + 2 x$ **correct**

- $\frac{4 x^{2}}{y} + 2 x y$

- $8 x \ln{\left(y \right)} + 2 y$

- $4 x^{2} \ln{\left(y \right)} + 2 x$

- $\frac{8 x}{y} + 2 y$

We differentiate the given function with respect to $y,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(2 x y+4 x^{2} \ln{\left(y \right)}) \\  & =\frac{∂}{∂y}(2 x y)+\frac{∂}{∂y}(4 x^{2} \ln{\left(y \right)}) \\  & =2 x\cdot \frac{∂}{∂y}(y)+4 x^{2}\cdot \frac{∂}{∂y}(\ln{\left(y \right)}) \\  & =2 x\cdot 1+4 x^{2}\cdot \frac{1}{y} \\  & =\frac{4 x^{2}}{y} + 2 x\end{aligned}
$$

## Original q-159616

Find $\frac{∂f}{∂x}$ given that $f(x,y)=\frac{x}{y}-\frac{y}{{x}^{2}}.$

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "3fb6e91c-e353-5113-a18f-0395e4a6e343",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{1}{{y}^{2}}+\\frac{2}{{x}^{3}}",
        ":db/id": 17592186276032
      },
      {
        ":answer/id": "4118aa52-6cf2-5999-9929-8a5819037289",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{x}{y}+\\frac{2y}{{x}^{3}}",
        ":db/id": 17592186276047
      },
      {
        ":answer/id": "68a80167-5ca4-5b8a-9c46-29004434201b",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{1}{y}+\\frac{2y}{{x}^{3}}",
        ":db/id": 17592186276416
      },
      {
        ":answer/id": "ebaecd0a-b971-5e92-b62d-28ceae190dc8",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{x}{{y}^{2}}-\\frac{1}{{x}^{2}}",
        ":db/id": 17592186277539
      },
      {
        ":answer/id": "f0a09a6f-356b-5b97-85dc-4fbfa42ac95a",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{1}{y}-\\frac{y}{{x}^{2}}",
        ":db/id": 17592186277589
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "68a80167-5ca4-5b8a-9c46-29004434201b",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{1}{y}+\\frac{2y}{{x}^{3}}",
      ":db/id": 17592186276416
    },
    ":answer-field/id": "e473ea39-99a3-5f5a-9eb6-13ee0b150617",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186278125
  }
]

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the constant multiple rule for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}(\frac{x}{y}-\frac{y}{{x}^{2}}) \\  & =\frac{∂}{∂x}(\frac{x}{y})-\frac{∂}{∂x}(\frac{y}{{x}^{2}}) \\  & =\frac{1}{y}\cdot \frac{∂}{∂x}(x)-y\cdot \frac{∂}{∂x}(\frac{1}{{x}^{2}}) \\  & =\frac{1}{y}\cdot (1)-y\cdot (-\frac{2}{{x}^{3}}) \\  & =\frac{1}{y}+\frac{2y}{{x}^{3}}\end{aligned}
$$

### easy — reciprocal

Bank profile: `observed`

Find $\frac{∂f}{∂y}$ given that $f(x,y)=\frac{y}{x}- \frac{8 x}{y^{2}}.$

Field `selection` — :answer-field.type/radio

- $- \frac{8}{y^{2}} - \frac{y}{x^{2}}$

- $- \frac{8 x}{y^{2}} + \frac{1}{x}$

- $\frac{16}{y^{3}} - \frac{1}{x^{2}}$

- $\frac{16 x}{y^{3}} + \frac{1}{x}$ **correct**

- $\frac{16 x}{y^{3}} + \frac{y}{x}$

We differentiate the given function with respect to $y,$ treating all other variables as constants.

Additionally, we use the constant multiple rule for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(\frac{y}{x}- \frac{8 x}{y^{2}}) \\  & =\frac{∂}{∂y}(\frac{y}{x})-\frac{∂}{∂y}(\frac{8 x}{y^{2}}) \\  & =\frac{1}{x}\cdot \frac{∂}{∂y}(y)-8 x\cdot \frac{∂}{∂y}(\frac{1}{y^{2}}) \\  & =\frac{1}{x}\cdot (1)-8 x\cdot (- \frac{2}{y^{3}}) \\  & =\frac{16 x}{y^{3}} + \frac{1}{x}\end{aligned}
$$

### easy — reciprocal

Bank profile: `observed`

Find $\frac{∂f}{∂y}$ given that $f(x,y)=\frac{2 y}{x}- \frac{4 x}{y^{2}}.$

Field `selection` — :answer-field.type/radio

- $\frac{8}{y^{3}} - \frac{2}{x^{2}}$

- $\frac{8 x}{y^{3}} + \frac{2 y}{x}$

- $- \frac{4}{y^{2}} - \frac{2 y}{x^{2}}$

- $\frac{8 x}{y^{3}} + \frac{2}{x}$ **correct**

- $- \frac{4 x}{y^{2}} + \frac{2}{x}$

We differentiate the given function with respect to $y,$ treating all other variables as constants.

Additionally, we use the constant multiple rule for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(\frac{2 y}{x}- \frac{4 x}{y^{2}}) \\  & =\frac{∂}{∂y}(\frac{2 y}{x})-\frac{∂}{∂y}(\frac{4 x}{y^{2}}) \\  & =\frac{2}{x}\cdot \frac{∂}{∂y}(y)-4 x\cdot \frac{∂}{∂y}(\frac{1}{y^{2}}) \\  & =\frac{2}{x}\cdot (1)-4 x\cdot (- \frac{2}{y^{3}}) \\  & =\frac{8 x}{y^{3}} + \frac{2}{x}\end{aligned}
$$

## Original q-159619

Find ${f}_{x}(x,y)$ for $f(x,y)=y\operatorname{arcsin}⁡x-8{y}^{2}.$

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "06f139b4-7520-5359-86c4-cc976c2a0da2",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{y}{\\sqrt{1-{x}^{2}}}",
        ":db/id": 17592186275545
      },
      {
        ":answer/id": "2959b683-8721-5d47-ae28-bfdae8458730",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{y}{\\sqrt{1-{x}^{2}}}-16y",
        ":db/id": 17592186275851
      },
      {
        ":answer/id": "8368ea87-f533-59c5-8779-19322eca007e",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\operatorname{arcsin}⁡x-16y",
        ":db/id": 17592186276659
      },
      {
        ":answer/id": "bd6ef288-08fc-5b25-a851-71488d467d63",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{1}{\\sqrt{1-{x}^{2}}}",
        ":db/id": 17592186277165
      },
      {
        ":answer/id": "ecc63446-669b-52c7-a4ab-fb4eec89773e",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "y\\operatorname{arcsin}⁡x",
        ":db/id": 17592186277553
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "06f139b4-7520-5359-86c4-cc976c2a0da2",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{y}{\\sqrt{1-{x}^{2}}}",
      ":db/id": 17592186275545
    },
    ":answer-field/id": "ad8d61fd-1884-5c25-bcf8-efd036093e2d",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186278023
  }
]

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(y\operatorname{arcsin}⁡x-8{y}^{2}) \\  & =\frac{∂}{∂x}(y\operatorname{arcsin}⁡x)-\frac{∂}{∂x}(8{y}^{2}) \\  & =y\cdot \frac{∂}{∂x}(\operatorname{arcsin}⁡x)-8{y}^{2}\frac{∂}{∂x}(1) \\  & =y\cdot \frac{1}{\sqrt{1-{x}^{2}}}-0 \\  & =\frac{y}{\sqrt{1-{x}^{2}}}\end{aligned}
$$

### moderate — asin

Bank profile: `observed`

Find ${f}_{x}(x,y)$ for $f(x,y)=y \arcsin{\left(x \right)}- 8 y^{2}.$

Field `selection` — :answer-field.type/radio

- $\frac{1}{\sqrt{- x^{2} + 1}}$

- $y \arcsin{\left(x \right)}$

- $\frac{y}{\sqrt{- x^{2} + 1}}$ **correct**

- $- 16 y + \arcsin{\left(x \right)}$

- $- 16 y + \frac{y}{\sqrt{- x^{2} + 1}}$

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(y \arcsin{\left(x \right)}- 8 y^{2}) \\  & =\frac{∂}{∂x}(y \arcsin{\left(x \right)})-\frac{∂}{∂x}(8 y^{2}) \\  & =y\cdot \frac{∂}{∂x}(\arcsin{\left(x \right)})-8 y^{2}\cdot \frac{∂}{∂x}(1) \\  & =y\cdot \frac{1}{\sqrt{- x^{2} + 1}}-0 \\  & =\frac{y}{\sqrt{- x^{2} + 1}}\end{aligned}
$$

### moderate — asin

Bank profile: `observed`

Find ${f}_{x}(x,y)$ for $f(x,y)=2 y \arcsin{\left(x \right)}- 4 y^{2}.$

Field `selection` — :answer-field.type/radio

- $\frac{2 y}{\sqrt{- x^{2} + 1}}$ **correct**

- $- 8 y + \frac{2 y}{\sqrt{- x^{2} + 1}}$

- $\frac{2}{\sqrt{- x^{2} + 1}}$

- $- 8 y + 2 \arcsin{\left(x \right)}$

- $2 y \arcsin{\left(x \right)}$

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(2 y \arcsin{\left(x \right)}- 4 y^{2}) \\  & =\frac{∂}{∂x}(2 y \arcsin{\left(x \right)})-\frac{∂}{∂x}(4 y^{2}) \\  & =2 y\cdot \frac{∂}{∂x}(\arcsin{\left(x \right)})-4 y^{2}\cdot \frac{∂}{∂x}(1) \\  & =2 y\cdot \frac{1}{\sqrt{- x^{2} + 1}}-0 \\  & =\frac{2 y}{\sqrt{- x^{2} + 1}}\end{aligned}
$$

## Original q-159623

Find ${f}_{y}(x,y)$ for $f(x,y)={e}^{2x+3y}+{x}^{2}{y}^{3}.$

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "1d0ec142-6a42-5919-bfa1-4366a65092fd",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "{e}^{2x+3y}+3{x}^{2}{y}^{2}",
        ":db/id": 17592186275741
      },
      {
        ":answer/id": "4619d482-5733-51a3-96e0-8ad693700d75",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "6{e}^{2x+3y}+6x{y}^{2}",
        ":db/id": 17592186276096
      },
      {
        ":answer/id": "4c062e4a-ec8c-5adf-8963-947c77e772cf",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3{e}^{2x+3y}+6x{y}^{2}",
        ":db/id": 17592186276145
      },
      {
        ":answer/id": "733056c4-4ea1-5358-977a-a7c64e073092",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2{e}^{2x+3y}+2x{y}^{3}",
        ":db/id": 17592186276520
      },
      {
        ":answer/id": "ad5a9b83-408b-502e-b6e9-1db4afeef584",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3{e}^{2x+3y}+3{x}^{2}{y}^{2}",
        ":db/id": 17592186277035
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "ad5a9b83-408b-502e-b6e9-1db4afeef584",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "3{e}^{2x+3y}+3{x}^{2}{y}^{2}",
      ":db/id": 17592186277035
    },
    ":answer-field/id": "4348a5dd-f992-5c0f-a358-d3667a2d63fb",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186277829
  }
]

The notation ${f}_{y}$ denotes the partial derivative of $f$ with respect to $y.$

We differentiate the given function with respect to $y,$ treating all other variables as constants.

Additionally, we use the sum rule for differentiation, as follows:

$$
\begin{aligned}{f}_{y}(x,y) & =\frac{∂}{∂y}({e}^{2x+3y}+{x}^{2}{y}^{3}) \\  & =\frac{∂}{∂y}({e}^{2x}\cdot {e}^{3y})+\frac{∂}{∂y}({x}^{2}{y}^{3}) \\  & ={e}^{2x}\cdot \frac{∂}{∂y}({e}^{3y})+{x}^{2}\cdot \frac{∂}{∂y}({y}^{3}) \\  & ={e}^{2x}\cdot 3{e}^{3y}+{x}^{2}\cdot 3{y}^{2} \\  & =3{e}^{2x+3y}+3{x}^{2}{y}^{2}\end{aligned}
$$

### moderate — exp_sum

Bank profile: `observed`

Find ${f}_{y}(x,y)$ for $f(x,y)=e^{3 x + 4 y}+x^{4} y^{4}.$

Field `selection` — :answer-field.type/radio

- $4 x^{3} y^{4} + 3 e^{3 x + 4 y}$

- $4 x^{4} y^{3} + 4 e^{3 x + 4 y}$ **correct**

- $4 x^{4} y^{3} + e^{3 x + 4 y}$

- $16 x^{3} y^{3} + 4 e^{3 x + 4 y}$

- $16 x^{3} y^{3} + 12 e^{3 x + 4 y}$

The notation ${f}_{y}$ denotes the partial derivative of $f$ with respect to $y.$

We differentiate the given function with respect to $y,$ treating all other variables as constants.

Additionally, we use the sum rule for differentiation, as follows:

$$
\begin{aligned}{f}_{y}(x,y) & =\frac{∂}{∂y}(e^{3 x + 4 y}+x^{4} y^{4}) \\  & =\frac{∂}{∂y}(e^{3 x}\cdot e^{4 y})+\frac{∂}{∂y}(x^{4} y^{4}) \\  & =e^{3 x}\cdot \frac{∂}{∂y}(e^{4 y})+x^{4}\cdot \frac{∂}{∂y}(y^{4}) \\  & =e^{3 x}\cdot 4 e^{4 y}+x^{4}\cdot 4 y^{3} \\  & =4 x^{4} y^{3} + 4 e^{3 x + 4 y}\end{aligned}
$$

### moderate — exp_sum

Bank profile: `observed`

Find ${f}_{x}(x,y)$ for $f(x,y)=e^{4 x + 2 y}+x^{3} y^{2}.$

Field `selection` — :answer-field.type/radio

- $3 x^{2} y^{2} + e^{4 x + 2 y}$

- $6 x^{2} y + 8 e^{4 x + 2 y}$

- $2 x^{3} y + 2 e^{4 x + 2 y}$

- $6 x^{2} y + 4 e^{4 x + 2 y}$

- $3 x^{2} y^{2} + 4 e^{4 x + 2 y}$ **correct**

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum rule for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(e^{4 x + 2 y}+x^{3} y^{2}) \\  & =\frac{∂}{∂x}(e^{2 y}\cdot e^{4 x})+\frac{∂}{∂x}(x^{3} y^{2}) \\  & =e^{2 y}\cdot \frac{∂}{∂x}(e^{4 x})+y^{2}\cdot \frac{∂}{∂x}(x^{3}) \\  & =e^{2 y}\cdot 4 e^{4 x}+y^{2}\cdot 3 x^{2} \\  & =3 x^{2} y^{2} + 4 e^{4 x + 2 y}\end{aligned}
$$

## Original q-159611

Find $\frac{∂f}{∂y}$ given that $f(x,y)={x}^{3}\operatorname{tan}⁡y-{3}^{x+y}.$

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "051af5b2-726e-5b49-a969-9796e797ae3e",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "{x}^{3}{sec}^{2}⁡y-{3}^{x+y}",
        ":db/id": 17592186381218
      },
      {
        ":answer/id": "ecde6fb6-675d-59f3-9850-531e953ba33d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3{x}^{2}\\operatorname{tan}⁡y-{3}^{x+y}\\operatorname{ln}⁡3",
        ":db/id": 17592186381219
      },
      {
        ":answer/id": "20ae591f-fa16-5672-9d61-61d8a2e3a05d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "{x}^{3}{sec}^{2}⁡y-{3}^{x+y}\\operatorname{ln}⁡3",
        ":db/id": 17592186381220
      },
      {
        ":answer/id": "a24feefe-3cbe-5e42-b271-0ac95ae87b92",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "{x}^{3}{csc}^{2}⁡y-{3}^{x+y}\\operatorname{ln}⁡3",
        ":db/id": 17592186381221
      },
      {
        ":answer/id": "faa81e86-4ae1-53c8-8b77-4618058650b4",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3{x}^{2}\\operatorname{tan}⁡y-{3}^{x+y}",
        ":db/id": 17592186381222
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "20ae591f-fa16-5672-9d61-61d8a2e3a05d",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "{x}^{3}{sec}^{2}⁡y-{3}^{x+y}\\operatorname{ln}⁡3",
      ":db/id": 17592186381220
    },
    ":answer-field/id": "e9775693-9681-5414-8d66-ab2776e2f417",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186381217
  }
]

We differentiate the given function with respect to $y,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}({x}^{3}\operatorname{tan}⁡y-{3}^{x+y}) \\  & =\frac{∂}{∂y}({x}^{3}\operatorname{tan}⁡y)-\frac{∂}{∂y}({3}^{x}\cdot {3}^{y}) \\  & ={x}^{3}\cdot \frac{∂}{∂y}(\operatorname{tan}⁡y)-{3}^{x}\cdot \frac{∂}{∂y}({3}^{y}) \\  & ={x}^{3}\cdot {sec}^{2}⁡y-{3}^{x}\cdot {3}^{y}\operatorname{ln}⁡3 \\  & ={x}^{3}{sec}^{2}⁡y-{3}^{x+y}\operatorname{ln}⁡3\end{aligned}
$$

### easy — tan_power

Bank profile: `observed`

Find $\frac{∂f}{∂x}$ given that $f(x,y)=y^{2} \tan{\left(x \right)}-8 \cdot 3^{x + y}.$

Field `selection` — :answer-field.type/radio

- $- 8 \cdot 3^{x + y} \ln{\left(3 \right)} + y^{2} \csc^{2}{\left(x \right)}$

- $- 8 \cdot 3^{x + y} + 2 y \tan{\left(x \right)}$

- $- 8 \cdot 3^{x + y} + y^{2} \sec^{2}{\left(x \right)}$

- $- 8 \cdot 3^{x + y} \ln{\left(3 \right)} + y^{2} \sec^{2}{\left(x \right)}$ **correct**

- $- 8 \cdot 3^{x + y} \ln{\left(3 \right)} + 2 y \tan{\left(x \right)}$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}(y^{2} \tan{\left(x \right)}-8 \cdot 3^{x + y}) \\  & =\frac{∂}{∂x}(y^{2} \tan{\left(x \right)})-\frac{∂}{∂x}(8 \cdot 3^{y}\cdot 3^{x}) \\  & =y^{2}\cdot \frac{∂}{∂x}(\tan{\left(x \right)})-8 \cdot 3^{y}\cdot \frac{∂}{∂x}(3^{x}) \\  & =y^{2}\cdot \sec^{2}{\left(x \right)}-8 \cdot 3^{y}\cdot 3^{x} \ln{\left(3 \right)} \\  & =- 8 \cdot 3^{x + y} \ln{\left(3 \right)} + y^{2} \sec^{2}{\left(x \right)}\end{aligned}
$$

### easy — tan_power

Bank profile: `observed`

Find $\frac{∂f}{∂x}$ given that $f(x,y)=2 y^{2} \tan{\left(x \right)}-4 \cdot 3^{x + y}.$

Field `selection` — :answer-field.type/radio

- $- 4 \cdot 3^{x + y} + 2 y^{2} \sec^{2}{\left(x \right)}$

- $- 4 \cdot 3^{x + y} \ln{\left(3 \right)} + 4 y \tan{\left(x \right)}$

- $- 4 \cdot 3^{x + y} \ln{\left(3 \right)} + 2 y^{2} \csc^{2}{\left(x \right)}$

- $- 4 \cdot 3^{x + y} \ln{\left(3 \right)} + 2 y^{2} \sec^{2}{\left(x \right)}$ **correct**

- $- 4 \cdot 3^{x + y} + 4 y \tan{\left(x \right)}$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}(2 y^{2} \tan{\left(x \right)}-4 \cdot 3^{x + y}) \\  & =\frac{∂}{∂x}(2 y^{2} \tan{\left(x \right)})-\frac{∂}{∂x}(4 \cdot 3^{y}\cdot 3^{x}) \\  & =2 y^{2}\cdot \frac{∂}{∂x}(\tan{\left(x \right)})-4 \cdot 3^{y}\cdot \frac{∂}{∂x}(3^{x}) \\  & =2 y^{2}\cdot \sec^{2}{\left(x \right)}-4 \cdot 3^{y}\cdot 3^{x} \ln{\left(3 \right)} \\  & =- 4 \cdot 3^{x + y} \ln{\left(3 \right)} + 2 y^{2} \sec^{2}{\left(x \right)}\end{aligned}
$$

## Original q-159614

Find $\frac{∂f}{∂x}$ given that $f(x,y)=5y-2\operatorname{sin}⁡x.$

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "1cc01c4d-160a-5eea-af63-34bb0d6f5cfe",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5-2\\operatorname{cos}⁡x",
        ":db/id": 17592186381225
      },
      {
        ":answer/id": "c56e8f59-813f-5140-bc33-6355f2e8c8f2",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5-2\\operatorname{sin}⁡x",
        ":db/id": 17592186381226
      },
      {
        ":answer/id": "f4c320e0-173a-55b6-b2fe-6e2df1ef3a1a",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2\\operatorname{sin}⁡x",
        ":db/id": 17592186381227
      },
      {
        ":answer/id": "23510347-ad72-510f-9453-61fb93eb4c94",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5y-2\\operatorname{sin}⁡x",
        ":db/id": 17592186381228
      },
      {
        ":answer/id": "e9546bf2-57cd-503b-97b1-de16a6c90894",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-2\\operatorname{cos}⁡x",
        ":db/id": 17592186381229
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "e9546bf2-57cd-503b-97b1-de16a6c90894",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-2\\operatorname{cos}⁡x",
      ":db/id": 17592186381229
    },
    ":answer-field/id": "107fee59-5ae8-5849-9751-9c38f3f036ee",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186381224
  }
]

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}(5y-2\operatorname{sin}⁡x) \\  & =\frac{∂}{∂x}(5y)-\frac{∂}{∂x}(2\operatorname{sin}⁡x) \\  & =5\cdot \frac{∂}{∂x}(y)-2\cdot \frac{∂}{∂x}(\operatorname{sin}⁡x) \\  & =5\cdot (0)-2\cdot (\operatorname{cos}⁡x) \\  & =-2\operatorname{cos}⁡x\end{aligned}
$$

### easy — constant_sin

Bank profile: `observed`

Find $\frac{∂f}{∂x}$ given that $f(x,y)=y- 8 \sin{\left(x \right)}.$

Field `selection` — :answer-field.type/radio

- $y - 8 \sin{\left(x \right)}$

- $- 8 \cos{\left(x \right)}$ **correct**

- $- 8 \cos{\left(x \right)} + 1$

- $8 \sin{\left(x \right)}$

- $- 8 \sin{\left(x \right)} + 1$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}(y- 8 \sin{\left(x \right)}) \\  & =\frac{∂}{∂x}(y)-\frac{∂}{∂x}(8 \sin{\left(x \right)}) \\  & =1\cdot \frac{∂}{∂x}(y)-8\cdot \frac{∂}{∂x}(\sin{\left(x \right)}) \\  & =1\cdot (0)-8\cdot (\cos{\left(x \right)}) \\  & =- 8 \cos{\left(x \right)}\end{aligned}
$$

### easy — constant_sin

Bank profile: `observed`

Find $\frac{∂f}{∂x}$ given that $f(x,y)=2 y- 4 \sin{\left(x \right)}.$

Field `selection` — :answer-field.type/radio

- $- 4 \cos{\left(x \right)} + 2$

- $- 4 \sin{\left(x \right)} + 2$

- $2 y - 4 \sin{\left(x \right)}$

- $4 \sin{\left(x \right)}$

- $- 4 \cos{\left(x \right)}$ **correct**

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}(2 y- 4 \sin{\left(x \right)}) \\  & =\frac{∂}{∂x}(2 y)-\frac{∂}{∂x}(4 \sin{\left(x \right)}) \\  & =2\cdot \frac{∂}{∂x}(y)-4\cdot \frac{∂}{∂x}(\sin{\left(x \right)}) \\  & =2\cdot (0)-4\cdot (\cos{\left(x \right)}) \\  & =- 4 \cos{\left(x \right)}\end{aligned}
$$

## Original q-159618

Find ${f}_{x}(x,y)$ for $f(x,y)=\frac{{x}^{3}}{{y}^{4}}+6xy.$

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "42294efd-0726-56da-9ff2-aacaa739035d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{4{x}^{3}}{{y}^{5}}+6x",
        ":db/id": 17592186381232
      },
      {
        ":answer/id": "e692a74c-4360-52d2-9a3b-14b7bb724d4d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{12{x}^{2}}{{y}^{4}}+6",
        ":db/id": 17592186381233
      },
      {
        ":answer/id": "e8ed405c-d0bb-58ec-9cb0-db66e314a0e5",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{4{x}^{3}}{{y}^{5}}+6y",
        ":db/id": 17592186381234
      },
      {
        ":answer/id": "8e0ae37b-c8dd-5e79-8516-1915e55fc497",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{3{x}^{2}}{{y}^{4}}+6y",
        ":db/id": 17592186381235
      },
      {
        ":answer/id": "1c43e727-621e-5491-9269-e9a7064dc12d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{12{x}^{2}}{{y}^{5}}+6",
        ":db/id": 17592186381236
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "8e0ae37b-c8dd-5e79-8516-1915e55fc497",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{3{x}^{2}}{{y}^{4}}+6y",
      ":db/id": 17592186381235
    },
    ":answer-field/id": "88fa3ce5-5c28-5db2-ada3-b42ead245d4c",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186381231
  }
]

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(\frac{{x}^{3}}{{y}^{4}}+6xy) \\  & =\frac{∂}{∂x}(\frac{{x}^{3}}{{y}^{4}})+\frac{∂}{∂x}(6xy) \\  & =\frac{1}{{y}^{4}}\frac{∂}{∂x}({x}^{3})+6y\cdot \frac{∂}{∂x}(x) \\  & =\frac{1}{{y}^{4}}\cdot 3{x}^{2}+6y\cdot 1 \\  & =\frac{3{x}^{2}}{{y}^{4}}+6y\end{aligned}
$$

### moderate — power_ratio

Bank profile: `observed`

Find ${f}_{x}(x,y)$ for $f(x,y)=\frac{x^{2}}{y^{3}}+8 x y.$

Field `selection` — :answer-field.type/radio

- $\frac{2 x}{y^{3}} + 8 y$ **correct**

- $- \frac{6 x}{y^{4}} + 8$

- $- \frac{3 x^{2}}{y^{4}} + 8 x$

- $\frac{3 x^{2}}{y^{4}} + 8 y$

- $\frac{6 x}{y^{3}} + 8$

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(\frac{x^{2}}{y^{3}}+8 x y) \\  & =\frac{∂}{∂x}(\frac{x^{2}}{y^{3}})+\frac{∂}{∂x}(8 x y) \\  & =\frac{1}{y^{3}}\cdot \frac{∂}{∂x}(x^{2})+8 y\cdot \frac{∂}{∂x}(x) \\  & =\frac{1}{y^{3}}\cdot 2 x+8 y\cdot 1 \\  & =\frac{2 x}{y^{3}} + 8 y\end{aligned}
$$

### moderate — power_ratio

Bank profile: `observed`

Find ${f}_{x}(x,y)$ for $f(x,y)=\frac{2 x^{2}}{y^{3}}+4 x y.$

Field `selection` — :answer-field.type/radio

- $- \frac{6 x^{2}}{y^{4}} + 4 x$

- $\frac{12 x}{y^{3}} + 4$

- $\frac{4 x}{y^{3}} + 4 y$ **correct**

- $\frac{6 x^{2}}{y^{4}} + 4 y$

- $- \frac{12 x}{y^{4}} + 4$

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(\frac{2 x^{2}}{y^{3}}+4 x y) \\  & =\frac{∂}{∂x}(\frac{2 x^{2}}{y^{3}})+\frac{∂}{∂x}(4 x y) \\  & =\frac{2}{y^{3}}\cdot \frac{∂}{∂x}(x^{2})+4 y\cdot \frac{∂}{∂x}(x) \\  & =\frac{2}{y^{3}}\cdot 2 x+4 y\cdot 1 \\  & =\frac{4 x}{y^{3}} + 4 y\end{aligned}
$$

## Original q-159621

Find ${f}_{x}(x,y)$ for $f(x,y)=8x{y}^{4}+\frac{3{y}^{2}}{{x}^{4}}.$

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "2b6f0ef5-d53d-5837-98c8-631186129434",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "32{y}^{3}-\\frac{24y}{{x}^{5}}",
        ":db/id": 17592186381239
      },
      {
        ":answer/id": "cd8e251a-8b10-5e05-b8e9-664d5a11015b",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "32x{y}^{3}+\\frac{6y}{{x}^{4}}",
        ":db/id": 17592186381240
      },
      {
        ":answer/id": "b39b7828-0e78-591c-b643-6a8cdf575bd5",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "32x{y}^{3}-\\frac{12{y}^{2}}{{x}^{5}}",
        ":db/id": 17592186381241
      },
      {
        ":answer/id": "20a23aa3-24e9-590f-adc4-61e10bc87a84",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "8{y}^{4}-\\frac{12{y}^{2}}{{x}^{5}}",
        ":db/id": 17592186381242
      },
      {
        ":answer/id": "4b9203e9-d678-558b-b50c-6a4193709f98",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "8{y}^{4}+\\frac{6y}{{x}^{4}}",
        ":db/id": 17592186381243
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "20a23aa3-24e9-590f-adc4-61e10bc87a84",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "8{y}^{4}-\\frac{12{y}^{2}}{{x}^{5}}",
      ":db/id": 17592186381242
    },
    ":answer-field/id": "3225480b-17a3-5de3-a894-3b9c909ffb27",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186381238
  }
]

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(8x{y}^{4}+\frac{3{y}^{2}}{{x}^{4}}) \\  & =\frac{∂}{∂x}(8x{y}^{4})+\frac{∂}{∂x}(\frac{3{y}^{2}}{{x}^{4}}) \\  & =8{y}^{4}\cdot \frac{∂}{∂x}(x)+3{y}^{2}\cdot \frac{∂}{∂x}(\frac{1}{{x}^{4}}) \\  & =8{y}^{4}\cdot 1+3{y}^{2}\cdot (-\frac{4}{{x}^{5}}) \\  & =8{y}^{4}-\frac{12{y}^{2}}{{x}^{5}}\end{aligned}
$$

### moderate — inverse_power

Bank profile: `observed`

Find ${f}_{x}(x,y)$ for $f(x,y)=x y^{3}+\frac{8 y^{2}}{x^{2}}.$

Field `selection` — :answer-field.type/radio

- $y^{3} - \frac{16 y^{2}}{x^{3}}$ **correct**

- $y^{3} + \frac{16 y}{x^{2}}$

- $3 y^{2} - \frac{32 y}{x^{3}}$

- $3 x y^{2} - \frac{16 y^{2}}{x^{3}}$

- $3 x y^{2} + \frac{16 y}{x^{2}}$

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(x y^{3}+\frac{8 y^{2}}{x^{2}}) \\  & =\frac{∂}{∂x}(x y^{3})+\frac{∂}{∂x}(\frac{8 y^{2}}{x^{2}}) \\  & =y^{3}\cdot \frac{∂}{∂x}(x)+8 y^{2}\cdot \frac{∂}{∂x}(\frac{1}{x^{2}}) \\  & =y^{3}\cdot (1)+8 y^{2}\cdot (- \frac{2}{x^{3}}) \\  & =y^{3} - \frac{16 y^{2}}{x^{3}}\end{aligned}
$$

### moderate — inverse_power

Bank profile: `observed`

Find ${f}_{x}(x,y)$ for $f(x,y)=2 x y^{3}+\frac{4 y^{4}}{x^{2}}.$

Field `selection` — :answer-field.type/radio

- $6 y^{2} - \frac{32 y^{3}}{x^{3}}$

- $6 x y^{2} + \frac{16 y^{3}}{x^{2}}$

- $2 y^{3} - \frac{8 y^{4}}{x^{3}}$ **correct**

- $6 x y^{2} - \frac{8 y^{4}}{x^{3}}$

- $2 y^{3} + \frac{16 y^{3}}{x^{2}}$

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(2 x y^{3}+\frac{4 y^{4}}{x^{2}}) \\  & =\frac{∂}{∂x}(2 x y^{3})+\frac{∂}{∂x}(\frac{4 y^{4}}{x^{2}}) \\  & =2 y^{3}\cdot \frac{∂}{∂x}(x)+4 y^{4}\cdot \frac{∂}{∂x}(\frac{1}{x^{2}}) \\  & =2 y^{3}\cdot (1)+4 y^{4}\cdot (- \frac{2}{x^{3}}) \\  & =2 y^{3} - \frac{8 y^{4}}{x^{3}}\end{aligned}
$$

## Original q-159624

Find ${f}_{y}(x,y)$ for $f(x,y)=x{e}^{y}+y{e}^{x}.$

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "21514dc3-fd5d-565c-a5dd-41b334024de1",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "x{e}^{y}+{e}^{x}",
        ":db/id": 17592186436293
      },
      {
        ":answer/id": "9023fe86-f4d4-53cf-afa7-ceab284c385c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "{e}^{y}",
        ":db/id": 17592186436306
      },
      {
        ":answer/id": "a479ae38-298e-5258-8558-f1d904df696f",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "{e}^{y}+y{e}^{x}",
        ":db/id": 17592186436312
      },
      {
        ":answer/id": "e1294690-bb34-5896-b0c1-f42f98fe8355",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "{e}^{y}+{e}^{x}",
        ":db/id": 17592186436319
      },
      {
        ":answer/id": "ffa0af21-05d8-5b41-b926-c8615ac23faf",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "{e}^{x}",
        ":db/id": 17592186436323
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "21514dc3-fd5d-565c-a5dd-41b334024de1",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "x{e}^{y}+{e}^{x}",
      ":db/id": 17592186436293
    },
    ":answer-field/id": "ec0f419d-2a0d-5de9-af19-f4de7b215052",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186436328
  }
]

The notation ${f}_{y}$ denotes the partial derivative of $f$ with respect to $y.$

We differentiate the given function with respect to $y,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{y}(x,y) & =\frac{∂}{∂y}(x{e}^{y}+y{e}^{x}) \\  & =\frac{∂}{∂y}(x{e}^{y})+\frac{∂}{∂y}(y{e}^{x}) \\  & =x\cdot \frac{∂}{∂y}({e}^{y})+{e}^{x}\cdot \frac{∂}{∂y}(y) \\  & =x\cdot {e}^{y}+{e}^{x}\cdot 1 \\  & =x{e}^{y}+{e}^{x}\end{aligned}
$$

### moderate — cross_exp

Bank profile: `observed`

Find ${f}_{x}(x,y)$ for $f(x,y)=y e^{x}+8 x e^{y}.$

Field `selection` — :answer-field.type/radio

- $e^{x} + 8 e^{y}$

- $8 e^{y}$

- $y e^{x} + 8 e^{y}$ **correct**

- $8 x e^{y} + e^{x}$

- $e^{x}$

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(y e^{x}+8 x e^{y}) \\  & =\frac{∂}{∂x}(y e^{x})+\frac{∂}{∂x}(8 x e^{y}) \\  & =y\cdot \frac{∂}{∂x}(e^{x})+8 e^{y}\cdot \frac{∂}{∂x}(x) \\  & =y\cdot e^{x}+8 e^{y}\cdot 1 \\  & =y e^{x} + 8 e^{y}\end{aligned}
$$

### moderate — cross_exp

Bank profile: `observed`

Find ${f}_{x}(x,y)$ for $f(x,y)=2 y e^{x}+4 x e^{y}.$

Field `selection` — :answer-field.type/radio

- $2 y e^{x} + 4 e^{y}$ **correct**

- $2 e^{x}$

- $2 e^{x} + 4 e^{y}$

- $4 x e^{y} + 2 e^{x}$

- $4 e^{y}$

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(2 y e^{x}+4 x e^{y}) \\  & =\frac{∂}{∂x}(2 y e^{x})+\frac{∂}{∂x}(4 x e^{y}) \\  & =2 y\cdot \frac{∂}{∂x}(e^{x})+4 e^{y}\cdot \frac{∂}{∂x}(x) \\  & =2 y\cdot e^{x}+4 e^{y}\cdot 1 \\  & =2 y e^{x} + 4 e^{y}\end{aligned}
$$

## Original q-159612

Find $\frac{∂f}{∂y}$ given that $f(x,y)=3\operatorname{arctan}⁡y-x{y}^{2}.$

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "5347b519-c490-5531-86d9-c47823454ef5",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-{y}^{2}",
        ":db/id": 17592186436298
      },
      {
        ":answer/id": "55c2293e-6cda-5e44-a3be-cf42f0b0106e",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3\\operatorname{arctan}⁡y-{y}^{2}",
        ":db/id": 17592186436299
      },
      {
        ":answer/id": "6d40833e-3b6e-5b26-96b6-154dbe238c17",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{6xy}{1+{y}^{2}}",
        ":db/id": 17592186436304
      },
      {
        ":answer/id": "a2853c1d-4c78-58f1-877e-d34353665049",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{3}{1+{y}^{2}}-{y}^{2}",
        ":db/id": 17592186436310
      },
      {
        ":answer/id": "ab9e0b79-350f-56ca-97e1-d432fc67e8d3",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{3}{1+{y}^{2}}-2xy",
        ":db/id": 17592186436313
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "ab9e0b79-350f-56ca-97e1-d432fc67e8d3",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{3}{1+{y}^{2}}-2xy",
      ":db/id": 17592186436313
    },
    ":answer-field/id": "1ad15885-4f52-5353-a9a6-c3dae29fe5c9",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186436324
  }
]

We differentiate the given function with respect to $y,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(3\operatorname{arctan}⁡y-x{y}^{2}) \\  & =\frac{∂}{∂y}(3\operatorname{arctan}⁡y)-\frac{∂}{∂y}(x{y}^{2}) \\  & =3\cdot \frac{∂}{∂y}(\operatorname{arctan}⁡y)-x\cdot \frac{∂}{∂y}({y}^{2}) \\  & =3\cdot \frac{1}{1+{y}^{2}}-x\cdot 2y \\  & =\frac{3}{1+{y}^{2}}-2xy\end{aligned}
$$

### easy — atan

Bank profile: `observed`

Find $\frac{∂f}{∂y}$ given that $f(x,y)=\arctan{\left(y \right)}- 8 x y^{2}.$

Field `selection` — :answer-field.type/radio

- $- 8 y^{2} + \frac{1}{y^{2} + 1}$

- $- 16 x y + \frac{1}{y^{2} + 1}$ **correct**

- $- 8 y^{2}$

- $\frac{16 x y}{y^{2} + 1}$

- $- 8 y^{2} + \arctan{\left(y \right)}$

We differentiate the given function with respect to $y,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(\arctan{\left(y \right)}- 8 x y^{2}) \\  & =\frac{∂}{∂y}(\arctan{\left(y \right)})-\frac{∂}{∂y}(8 x y^{2}) \\  & =1\cdot \frac{∂}{∂y}(\arctan{\left(y \right)})-8 x\cdot \frac{∂}{∂y}(y^{2}) \\  & =1\cdot \frac{1}{y^{2} + 1}-8 x\cdot 2 y \\  & =- 16 x y + \frac{1}{y^{2} + 1}\end{aligned}
$$

### easy — atan

Bank profile: `observed`

Find $\frac{∂f}{∂y}$ given that $f(x,y)=2 \arctan{\left(y \right)}- 4 x y^{2}.$

Field `selection` — :answer-field.type/radio

- $- 4 y^{2}$

- $- 4 y^{2} + 2 \arctan{\left(y \right)}$

- $- 4 y^{2} + \frac{2}{y^{2} + 1}$

- $\frac{16 x y}{y^{2} + 1}$

- $- 8 x y + \frac{2}{y^{2} + 1}$ **correct**

We differentiate the given function with respect to $y,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}\frac{∂f}{∂y} & =\frac{∂}{∂y}(2 \arctan{\left(y \right)}- 4 x y^{2}) \\  & =\frac{∂}{∂y}(2 \arctan{\left(y \right)})-\frac{∂}{∂y}(4 x y^{2}) \\  & =2\cdot \frac{∂}{∂y}(\arctan{\left(y \right)})-4 x\cdot \frac{∂}{∂y}(y^{2}) \\  & =2\cdot \frac{1}{y^{2} + 1}-4 x\cdot 2 y \\  & =- 8 x y + \frac{2}{y^{2} + 1}\end{aligned}
$$

### hard — hard_log_exp

Bank profile: `authored`

Find ${f}_{x}(x,y)$ for $f(x,y)=y^{2} \ln{\left(x \right)}+8 y e^{x}- \frac{2 y^{2}}{x^{3}}.$

Field `selection` — :answer-field.type/radio

- $8 e^{x} + \frac{y^{2}}{x} + \frac{6 y^{2}}{x^{4}}$

- $2 y \ln{\left(x \right)} + 8 e^{x} - \frac{4 y}{x^{3}}$

- $8 y e^{x} + \frac{y^{2}}{x} + \frac{6 y^{2}}{x^{4}}$ **correct**

- $y^{2} \ln{\left(x \right)} + 8 y e^{x} + \frac{6 y^{2}}{x^{4}}$

- $8 y e^{x} + \frac{y^{2}}{x} - \frac{6 y^{2}}{x^{4}}$

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(y^{2} \ln{\left(x \right)}+8 y e^{x}- \frac{2 y^{2}}{x^{3}}) \\  & =\frac{∂}{∂x}(y^{2} \ln{\left(x \right)})+\frac{∂}{∂x}(8 y e^{x})-\frac{∂}{∂x}(\frac{2 y^{2}}{x^{3}}) \\  & =y^{2}\cdot \frac{∂}{∂x}(\ln{\left(x \right)})+8 y\cdot \frac{∂}{∂x}(e^{x})-2 y^{2}\cdot \frac{∂}{∂x}(\frac{1}{x^{3}}) \\  & =y^{2}\cdot \frac{1}{x}+8 y\cdot e^{x}-2 y^{2}\cdot (- \frac{3}{x^{4}}) \\  & =8 y e^{x} + \frac{y^{2}}{x} + \frac{6 y^{2}}{x^{4}}\end{aligned}
$$

### hard — hard_log_exp

Bank profile: `authored`

Find ${f}_{x}(x,y)$ for $f(x,y)=2 y^{4} \ln{\left(x \right)}+4 y e^{x}- \frac{3 y^{2}}{x^{3}}.$

Field `selection` — :answer-field.type/radio

- $4 y e^{x} + \frac{2 y^{4}}{x} + \frac{9 y^{2}}{x^{4}}$ **correct**

- $4 y e^{x} + \frac{2 y^{4}}{x} - \frac{9 y^{2}}{x^{4}}$

- $4 e^{x} + \frac{2 y^{4}}{x} + \frac{9 y^{2}}{x^{4}}$

- $2 y^{4} \ln{\left(x \right)} + 4 y e^{x} + \frac{9 y^{2}}{x^{4}}$

- $8 y^{3} \ln{\left(x \right)} + 4 e^{x} - \frac{6 y}{x^{3}}$

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(2 y^{4} \ln{\left(x \right)}+4 y e^{x}- \frac{3 y^{2}}{x^{3}}) \\  & =\frac{∂}{∂x}(2 y^{4} \ln{\left(x \right)})+\frac{∂}{∂x}(4 y e^{x})-\frac{∂}{∂x}(\frac{3 y^{2}}{x^{3}}) \\  & =2 y^{4}\cdot \frac{∂}{∂x}(\ln{\left(x \right)})+4 y\cdot \frac{∂}{∂x}(e^{x})-3 y^{2}\cdot \frac{∂}{∂x}(\frac{1}{x^{3}}) \\  & =2 y^{4}\cdot \frac{1}{x}+4 y\cdot e^{x}-3 y^{2}\cdot (- \frac{3}{x^{4}}) \\  & =4 y e^{x} + \frac{2 y^{4}}{x} + \frac{9 y^{2}}{x^{4}}\end{aligned}
$$

### hard — hard_trig_reciprocal

Bank profile: `authored`

Find ${f}_{x}(x,y)$ for $f(x,y)=y^{2} \sin{\left(x \right)}+8 y \arctan{\left(x \right)}- \frac{2 y^{2}}{x^{3}}.$

Field `selection` — :answer-field.type/radio

- $y^{2} \cos{\left(x \right)} + \frac{8}{x^{2} + 1} + \frac{6 y^{2}}{x^{4}}$

- $2 y \sin{\left(x \right)} + 8 \arctan{\left(x \right)} - \frac{4 y}{x^{3}}$

- $y^{2} \cos{\left(x \right)} + \frac{8 y}{x^{2} + 1} + \frac{6 y^{2}}{x^{4}}$ **correct**

- $y^{2} \sin{\left(x \right)} + \frac{8 y}{x^{2} + 1} + \frac{6 y^{2}}{x^{4}}$

- $y^{2} \cos{\left(x \right)} + \frac{8 y}{x^{2} + 1} - \frac{6 y^{2}}{x^{4}}$

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(y^{2} \sin{\left(x \right)}+8 y \arctan{\left(x \right)}- \frac{2 y^{2}}{x^{3}}) \\  & =\frac{∂}{∂x}(y^{2} \sin{\left(x \right)})+\frac{∂}{∂x}(8 y \arctan{\left(x \right)})-\frac{∂}{∂x}(\frac{2 y^{2}}{x^{3}}) \\  & =y^{2}\cdot \frac{∂}{∂x}(\sin{\left(x \right)})+8 y\cdot \frac{∂}{∂x}(\arctan{\left(x \right)})-2 y^{2}\cdot \frac{∂}{∂x}(\frac{1}{x^{3}}) \\  & =y^{2}\cdot \cos{\left(x \right)}+8 y\cdot \frac{1}{x^{2} + 1}-2 y^{2}\cdot (- \frac{3}{x^{4}}) \\  & =y^{2} \cos{\left(x \right)} + \frac{8 y}{x^{2} + 1} + \frac{6 y^{2}}{x^{4}}\end{aligned}
$$

### hard — hard_trig_reciprocal

Bank profile: `authored`

Find ${f}_{x}(x,y)$ for $f(x,y)=2 y^{4} \sin{\left(x \right)}+4 y \arctan{\left(x \right)}- \frac{3 y^{2}}{x^{3}}.$

Field `selection` — :answer-field.type/radio

- $2 y^{4} \cos{\left(x \right)} + \frac{4 y}{x^{2} + 1} + \frac{9 y^{2}}{x^{4}}$ **correct**

- $2 y^{4} \cos{\left(x \right)} + \frac{4 y}{x^{2} + 1} - \frac{9 y^{2}}{x^{4}}$

- $2 y^{4} \cos{\left(x \right)} + \frac{4}{x^{2} + 1} + \frac{9 y^{2}}{x^{4}}$

- $2 y^{4} \sin{\left(x \right)} + \frac{4 y}{x^{2} + 1} + \frac{9 y^{2}}{x^{4}}$

- $8 y^{3} \sin{\left(x \right)} + 4 \arctan{\left(x \right)} - \frac{6 y}{x^{3}}$

The notation ${f}_{x}$ denotes the partial derivative of $f$ with respect to $x.$

We differentiate the given function with respect to $x,$ treating all other variables as constants.

Additionally, we use the sum and constant multiple rules for differentiation, as follows:

$$
\begin{aligned}{f}_{x}(x,y) & =\frac{∂}{∂x}(2 y^{4} \sin{\left(x \right)}+4 y \arctan{\left(x \right)}- \frac{3 y^{2}}{x^{3}}) \\  & =\frac{∂}{∂x}(2 y^{4} \sin{\left(x \right)})+\frac{∂}{∂x}(4 y \arctan{\left(x \right)})-\frac{∂}{∂x}(\frac{3 y^{2}}{x^{3}}) \\  & =2 y^{4}\cdot \frac{∂}{∂x}(\sin{\left(x \right)})+4 y\cdot \frac{∂}{∂x}(\arctan{\left(x \right)})-3 y^{2}\cdot \frac{∂}{∂x}(\frac{1}{x^{3}}) \\  & =2 y^{4}\cdot \cos{\left(x \right)}+4 y\cdot \frac{1}{x^{2} + 1}-3 y^{2}\cdot (- \frac{3}{x^{4}}) \\  & =2 y^{4} \cos{\left(x \right)} + \frac{4 y}{x^{2} + 1} + \frac{9 y^{2}}{x^{4}}\end{aligned}
$$
