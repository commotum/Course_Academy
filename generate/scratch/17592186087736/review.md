# Trigonometric parametric ranges: source and generated review



All generated variants are labeled. Raw snapshots remain unchanged.



## Original q-16201 (easy)



Given that a curve is defined parametrically as

$$
x=7\operatorname{cos}⁡\theta ,\,\,\,y=3\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "399f8d43-8f84-5c44-94d4-0b0dd69e8268",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1\\le x\\le 1,\\,1\\le y\\le 1",
        ":db/id": 17592186279098
      },
      {
        ":answer/id": "4759a2f7-a933-59e3-957d-8ccee01e9143",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-3\\le x\\le 3,\\,-7\\le y\\le 7",
        ":db/id": 17592186279231
      },
      {
        ":answer/id": "87d0badb-d995-50bf-b63f-47523b429a32",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-7\\le x\\le 7,\\,-3\\le y\\le 3",
        ":db/id": 17592186279804
      },
      {
        ":answer/id": "ebd6c89c-69a3-5f3f-b152-dc3c96d08337",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "0\\le x\\le 3,\\,0\\le y\\le 7",
        ":db/id": 17592186280666
      },
      {
        ":answer/id": "f95e3399-d4d4-5fb0-82b3-fbc31ee229f7",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "0\\le x\\le 7,\\,0\\le y\\le 3",
        ":db/id": 17592186280782
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "87d0badb-d995-50bf-b63f-47523b429a32",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-7\\le x\\le 7,\\,-3\\le y\\le 3",
      ":db/id": 17592186279804
    },
    ":answer-field/id": "7930e983-ef79-5ead-aefc-e8d03715f738",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186281054
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -7 & \le 7\operatorname{cos}⁡\theta \le 7 \\ -7 & \le x\le 7.\end{aligned}
$$

So, we can conclude that $-7\le x\le 7.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -3 & \le 3\operatorname{sin}⁡\theta \le 3 \\ -3 & \le y\le 3.\end{aligned}
$$

So, we can conclude that $-3\le y\le 3.$

Therefore, the ranges are $-7\le x\le 7$ and $-3\le y\le 3.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=7\operatorname{cos}⁡\theta ,\,\,\,y=3\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $-7\le x\le 7,\,-3\le y\le 3$ (correct)
- $-3\le x\le 3,\,-7\le y\le 7$
- $1\le x\le 1,\,1\le y\le 1$
- $0\le x\le 7,\,0\le y\le 3$
- $0\le x\le 3,\,0\le y\le 7$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -7 & \le 7\operatorname{cos}⁡\theta \le 7 \\ -7 & \le x\le 7.\end{aligned}
$$

So, we can conclude that $-7\le x\le 7.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -3 & \le 3\operatorname{sin}⁡\theta \le 3 \\ -3 & \le y\le 3.\end{aligned}
$$

So, we can conclude that $-3\le y\le 3.$

Therefore, the ranges are $-7\le x\le 7$ and $-3\le y\le 3.$



### Generated variant — observed:q-16201

Given that a curve is defined parametrically as

$$
x=7\operatorname{cos}⁡\theta ,\,\,\,y=2\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $0\le x\le 2,\,0\le y\le 7$
- $-2\le x\le 2,\,-7\le y\le 7$
- $-7\le x\le 7,\,-2\le y\le 2$ (correct)
- $0\le x\le 7,\,0\le y\le 2$
- $1\le x\le 1,\,1\le y\le 1$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -7 & \le 7\operatorname{cos}⁡\theta \le 7 \\ -7 & \le x\le 7.\end{aligned}
$$

So, we can conclude that $-7\le x\le 7.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -2 & \le 2\operatorname{sin}⁡\theta \le 2 \\ -2 & \le y\le 2.\end{aligned}
$$

So, we can conclude that $-2\le y\le 2.$

Therefore, the ranges are $-7\le x\le 7$ and $-2\le y\le 2.$



### Generated variant — authored:full-period

Given that a curve is defined parametrically as

$$
x=7\operatorname{cos}⁡\theta ,\,\,\,y=2\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $-\frac{7}{2}\le x\le \frac{7}{2},\,-1\le y\le 1$
- $0\le x\le 7,\,0\le y\le 2$
- $-14\le x\le 14,\,-4\le y\le 4$
- $-2\le x\le 2,\,-7\le y\le 7$
- $-7\le x\le 7,\,-2\le y\le 2$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -7 & \le 7\operatorname{cos}⁡\theta \le 7 \\ -7 & \le x\le 7.\end{aligned}
$$

So, we can conclude that $-7\le x\le 7.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -2 & \le 2\operatorname{sin}⁡\theta \le 2 \\ -2 & \le y\le 2.\end{aligned}
$$

So, we can conclude that $-2\le y\le 2.$

Therefore, the ranges are $-7\le x\le 7$ and $-2\le y\le 2.$



## Original q-70341 (unrated; authored moderate assignment)



Given that a curve is defined parametrically as
$x = 3\cos θ - 1, y = 2\sin θ + 2, 0 \le θ < 2π$,
what are the ranges of $x$ and $y$?



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "86dadee3-7d6d-5185-ab3b-b85a361a52e3",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "0 \\le x \\le 4, 2 \\le y \\le 4",
        ":db/id": 17592186086341
      },
      {
        ":answer/id": "d5399094-f398-56ed-9f79-a44406253676",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-4 \\le x \\le - 2,-4 \\le y \\le 0",
        ":db/id": 17592186086342
      },
      {
        ":answer/id": "45d78f20-324c-515d-a7d7-5a8cca623062",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-4 \\le x \\le 0,-2 \\le y \\le 4",
        ":db/id": 17592186086343
      },
      {
        ":answer/id": "49999e5c-859b-52f5-9853-47952d52774d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-4 \\le x \\le 2, 0 \\le y \\le 4",
        ":db/id": 17592186086344
      },
      {
        ":answer/id": "6f7a3f21-dc25-5a43-bc94-3ffe87b345a9",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2 \\le x \\le 4, 0 \\le y \\le 4",
        ":db/id": 17592186086345
      }
    ],
    ":answer-field/id": "5333b62b-8f5a-5314-ac5f-0d3282feeb1b",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186086340
  }
]



Original worked solution:

**Absent in capture.**



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as
$x = 3\cos θ - 1, y = 2\sin θ + 2, 0 \le θ < 2π$,
what are the ranges of $x$ and $y$?

**selection**
- $-4\le x\le 0,\,-2\le y\le 4$
- $-4\le x\le -2,\,-4\le y\le 0$
- $0\le x\le 4,\,2\le y\le 4$
- $2\le x\le 4,\,0\le y\le 4$
- $-4\le x\le 2,\,0\le y\le 4$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi,$ we have $-1\le \operatorname{cos}\theta\le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}\theta \le 1 \\ -3 & \le 3\operatorname{cos}\theta \le 3 \\ -3-1 & \le 3\operatorname{cos}\theta -1\le 3-1 \\ -4 & \le x\le 2.\end{aligned}
$$

So, we can conclude that $-4\le x\le 2.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi,$ we have $-1\le \operatorname{sin}\theta\le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}\theta \le 1 \\ -2 & \le 2\operatorname{sin}\theta \le 2 \\ -2+2 & \le 2\operatorname{sin}\theta +2\le 2+2 \\ 0 & \le y\le 4.\end{aligned}
$$

So, we can conclude that $0\le y\le 4.$



### Generated variant — observed:q-70341

Given that a curve is defined parametrically as
$x = 7\cos θ - 1, y = 2\sin θ + 5, 0 \le θ < 2π$,
what are the ranges of $x$ and $y$?

**selection**
- $-8\le x\le 6,\,3\le y\le 7$ (correct)
- $-8\le x\le -6,\,-7\le y\le 0$
- $-8\le x\le 0,\,-5\le y\le 7$
- $6\le x\le 8,\,3\le y\le 7$
- $0\le x\le 8,\,5\le y\le 7$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi,$ we have $-1\le \operatorname{cos}\theta\le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}\theta \le 1 \\ -7 & \le 7\operatorname{cos}\theta \le 7 \\ -7-1 & \le 7\operatorname{cos}\theta -1\le 7-1 \\ -8 & \le x\le 6.\end{aligned}
$$

So, we can conclude that $-8\le x\le 6.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi,$ we have $-1\le \operatorname{sin}\theta\le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}\theta \le 1 \\ -2 & \le 2\operatorname{sin}\theta \le 2 \\ -2+5 & \le 2\operatorname{sin}\theta +5\le 2+5 \\ 3 & \le y\le 7.\end{aligned}
$$

So, we can conclude that $3\le y\le 7.$



### Generated variant — authored:full-period

Given that a curve is defined parametrically as
$x = 7\cos θ - 1, y = 2\sin θ + 5, 0 \le θ < 2π$,
what are the ranges of $x$ and $y$?

**selection**
- $-\frac{9}{2}\le x\le \frac{5}{2},\,4\le y\le 6$
- $-7\le x\le 7,\,-2\le y\le 2$
- $-15\le x\le 13,\,1\le y\le 9$
- $-6\le x\le 8,\,-7\le y\le -3$
- $-8\le x\le 6,\,3\le y\le 7$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi,$ we have $-1\le \operatorname{cos}\theta\le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}\theta \le 1 \\ -7 & \le 7\operatorname{cos}\theta \le 7 \\ -7-1 & \le 7\operatorname{cos}\theta -1\le 7-1 \\ -8 & \le x\le 6.\end{aligned}
$$

So, we can conclude that $-8\le x\le 6.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi,$ we have $-1\le \operatorname{sin}\theta\le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}\theta \le 1 \\ -2 & \le 2\operatorname{sin}\theta \le 2 \\ -2+5 & \le 2\operatorname{sin}\theta +5\le 2+5 \\ 3 & \le y\le 7.\end{aligned}
$$

So, we can conclude that $3\le y\le 7.$



## Original q-276258 (easy)



Given that a curve is defined parametrically as

$$
x=4\operatorname{cos}\theta ,\,y=2\operatorname{sin}\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}{{field-2}}
$x\le $
{{field-3}}.

 

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "ca60fdcc-dda9-5409-bb81-344b09986ac5",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-4",
        ":db/id": 17592186232410
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "ca60fdcc-dda9-5409-bb81-344b09986ac5",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-4",
      ":db/id": 17592186232410
    },
    ":answer-field/id": "ca56b8e5-8405-5ba4-ada6-394dce99dea5",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232409
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "03eb58f9-5c4d-5704-b1f3-24df3d108cb0",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186232412
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "03eb58f9-5c4d-5704-b1f3-24df3d108cb0",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186232412
    },
    ":answer-field/id": "91d59c0f-f0c5-5b07-bebb-1320bc54f3be",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232411
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "9a7e0156-a9f9-52f5-af28-277e2c6df336",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "4",
        ":db/id": 17592186232414
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "9a7e0156-a9f9-52f5-af28-277e2c6df336",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "4",
      ":db/id": 17592186232414
    },
    ":answer-field/id": "225a0b88-6817-55d6-a3db-6d411d484997",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232413
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "957fdecf-4769-50cf-b898-f2272fca2edc",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-2",
        ":db/id": 17592186232416
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "957fdecf-4769-50cf-b898-f2272fca2edc",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-2",
      ":db/id": 17592186232416
    },
    ":answer-field/id": "61313d60-2a62-55d9-b1c5-2d9707ea6eb2",
    ":answer-field/key": "field-4",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232415
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "a2ef4612-07ce-57c4-8427-f0e2c2f142da",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186232418
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "a2ef4612-07ce-57c4-8427-f0e2c2f142da",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186232418
    },
    ":answer-field/id": "4531d739-aa50-5c78-a314-c0d516f7b7b2",
    ":answer-field/key": "field-5",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232417
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "dc6ca0f1-8049-59b6-9424-d6d0d4f4577d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2",
        ":db/id": 17592186232420
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "dc6ca0f1-8049-59b6-9424-d6d0d4f4577d",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "2",
      ":db/id": 17592186232420
    },
    ":answer-field/id": "35c71493-7df0-5a0d-b2fb-741a03aba773",
    ":answer-field/key": "field-6",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232419
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{cos}\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}\theta \le 1 \\ -4 & \le 4\operatorname{cos}\theta \le 4 \\ -4 & \le x\le 4.\end{aligned}
$$

So, we can conclude that $-4\le x\le 4.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{sin}\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}\theta \le 1 \\ -2 & \le 2\operatorname{sin}\theta \le 2 \\ -2 & \le y\le 2.\end{aligned}
$$

So, we can conclude that $-2\le y\le 2.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=4\operatorname{cos}\theta ,\,y=2\operatorname{sin}\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}{{field-2}}
$x\le $
{{field-3}}.

 

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.

**field-1**
- $-4$ (correct)
**field-2**
- $\le $ (correct)
**field-3**
- $4$ (correct)
**field-4**
- $-2$ (correct)
**field-5**
- $\le $ (correct)
**field-6**
- $2$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{cos}\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}\theta \le 1 \\ -4 & \le 4\operatorname{cos}\theta \le 4 \\ -4 & \le x\le 4.\end{aligned}
$$

So, we can conclude that $-4\le x\le 4.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{sin}\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}\theta \le 1 \\ -2 & \le 2\operatorname{sin}\theta \le 2 \\ -2 & \le y\le 2.\end{aligned}
$$

So, we can conclude that $-2\le y\le 2.$



### Generated variant — blank

Given that a curve is defined parametrically as

$$
x=7\operatorname{cos}\theta ,\,y=2\operatorname{sin}\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}{{field-2}}
$x\le $
{{field-3}}.

 

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.

**field-1**
- $-7$ (correct)
**field-2**
- $\le $ (correct)
**field-3**
- $7$ (correct)
**field-4**
- $-2$ (correct)
**field-5**
- $\le $ (correct)
**field-6**
- $2$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{cos}\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}\theta \le 1 \\ -7 & \le 7\operatorname{cos}\theta \le 7 \\ -7 & \le x\le 7.\end{aligned}
$$

So, we can conclude that $-7\le x\le 7.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{sin}\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}\theta \le 1 \\ -2 & \le 2\operatorname{sin}\theta \le 2 \\ -2 & \le y\le 2.\end{aligned}
$$

So, we can conclude that $-2\le y\le 2.$



## Original q-327882 (moderate)



Given that a curve is defined parametrically as

$$
x=5\operatorname{cos}\theta -3,\,y=7\operatorname{sin}\theta +1,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}
$\le x$
{{field-2}}{{field-3}}.

The range of $y$ is 
{{field-4}}{{field-5}}
$y\le $
{{field-6}}.



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "ba3839b9-52c3-5c2d-8eb0-66915070f5c7",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-8",
        ":db/id": 17592186232653
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "ba3839b9-52c3-5c2d-8eb0-66915070f5c7",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-8",
      ":db/id": 17592186232653
    },
    ":answer-field/id": "523ba8a1-21b9-506b-9e69-898d01fca170",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232652
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "874a3212-0376-540b-8ad7-1c3642cb863a",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186232655
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "874a3212-0376-540b-8ad7-1c3642cb863a",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186232655
    },
    ":answer-field/id": "64e564a7-8774-510d-802b-7a665e5a8cad",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232654
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "556377da-a872-595e-bb33-f1b354b23d8d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2",
        ":db/id": 17592186232657
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "556377da-a872-595e-bb33-f1b354b23d8d",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "2",
      ":db/id": 17592186232657
    },
    ":answer-field/id": "55e4f41e-4653-5e03-81e3-e1414dff8e55",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232656
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "c5afb992-6a89-5dd8-a6b6-c7935703391a",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-6",
        ":db/id": 17592186232659
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "c5afb992-6a89-5dd8-a6b6-c7935703391a",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-6",
      ":db/id": 17592186232659
    },
    ":answer-field/id": "fd3b7b31-2fd8-5dc1-9e4b-cbc564bf0f26",
    ":answer-field/key": "field-4",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232658
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "4485c0b2-8f41-5cc1-9591-e764086b3eed",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186232661
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "4485c0b2-8f41-5cc1-9591-e764086b3eed",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186232661
    },
    ":answer-field/id": "e0451796-cc4a-5691-9da6-6d50eb33e69d",
    ":answer-field/key": "field-5",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232660
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "4a852a54-4426-54da-bb97-f452c07cc0ea",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "8",
        ":db/id": 17592186232663
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "4a852a54-4426-54da-bb97-f452c07cc0ea",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "8",
      ":db/id": 17592186232663
    },
    ":answer-field/id": "63e5c6e1-de4c-5909-8f20-a774fbc6e6ba",
    ":answer-field/key": "field-6",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232662
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{cos}\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}\theta \le 1 \\ -5 & \le 5\operatorname{cos}\theta \le 5 \\ -5-3 & \le 5\operatorname{cos}\theta -3\le 5-3 \\ -8 & \le x\le 2.\end{aligned}
$$

So, we can conclude that $-8\le x\le 2.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{sin}\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}\theta \le 1 \\ -7 & \le 7\operatorname{sin}\theta \le 7 \\ -7+1 & \le 7\operatorname{sin}\theta +1\le 7+1 \\ -6 & \le y\le 8.\end{aligned}
$$

So, we can conclude that $-6\le y\le 8.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=5\operatorname{cos}\theta -3,\,y=7\operatorname{sin}\theta +1,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}
$\le x$
{{field-2}}{{field-3}}.

The range of $y$ is 
{{field-4}}{{field-5}}
$y\le $
{{field-6}}.

**field-1**
- $-8$ (correct)
**field-2**
- $\le $ (correct)
**field-3**
- $2$ (correct)
**field-4**
- $-6$ (correct)
**field-5**
- $\le $ (correct)
**field-6**
- $8$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{cos}\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}\theta \le 1 \\ -5 & \le 5\operatorname{cos}\theta \le 5 \\ -5-3 & \le 5\operatorname{cos}\theta -3\le 5-3 \\ -8 & \le x\le 2.\end{aligned}
$$

So, we can conclude that $-8\le x\le 2.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{sin}\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}\theta \le 1 \\ -7 & \le 7\operatorname{sin}\theta \le 7 \\ -7+1 & \le 7\operatorname{sin}\theta +1\le 7+1 \\ -6 & \le y\le 8.\end{aligned}
$$

So, we can conclude that $-6\le y\le 8.$



### Generated variant — blank

Given that a curve is defined parametrically as

$$
x=7\operatorname{cos}\theta -1,\,y=2\operatorname{sin}\theta +5,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}
$\le x$
{{field-2}}{{field-3}}.

The range of $y$ is 
{{field-4}}{{field-5}}
$y\le $
{{field-6}}.

**field-1**
- $-8$ (correct)
**field-2**
- $\le $ (correct)
**field-3**
- $6$ (correct)
**field-4**
- $3$ (correct)
**field-5**
- $\le $ (correct)
**field-6**
- $7$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{cos}\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}\theta \le 1 \\ -7 & \le 7\operatorname{cos}\theta \le 7 \\ -7-1 & \le 7\operatorname{cos}\theta -1\le 7-1 \\ -8 & \le x\le 6.\end{aligned}
$$

So, we can conclude that $-8\le x\le 6.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{sin}\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}\theta \le 1 \\ -2 & \le 2\operatorname{sin}\theta \le 2 \\ -2+5 & \le 2\operatorname{sin}\theta +5\le 2+5 \\ 3 & \le y\le 7.\end{aligned}
$$

So, we can conclude that $3\le y\le 7.$



## Original q-123777 (easy)



Given that a curve is defined parametrically as

$$
x=\operatorname{cos}⁡\theta +3,\,y=\operatorname{sin}⁡\theta -1,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "384f72db-1382-5e20-bf1f-b36c690e33cc",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-3\\le x\\le 3,\\,-2\\le y\\le 0",
        ":db/id": 17592186257278
      },
      {
        ":answer/id": "801fd8d9-9053-54df-9ced-8c85c3bdf98c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2\\le x\\le 4,\\,-2\\le y\\le 0",
        ":db/id": 17592186257921
      },
      {
        ":answer/id": "8c14b075-1888-5849-bc15-60accafaa842",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-4\\le x\\le -2,\\,0\\le y\\le 2",
        ":db/id": 17592186258010
      },
      {
        ":answer/id": "e2d3bd46-7af0-528b-a6fd-981273814a13",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-3\\le x\\le 3,\\,-1\\le y\\le 1",
        ":db/id": 17592186258756
      },
      {
        ":answer/id": "f26d173c-5784-55a7-aa52-c3e3759de69c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2\\le x\\le 4,\\,-1\\le y\\le 1",
        ":db/id": 17592186258893
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "801fd8d9-9053-54df-9ced-8c85c3bdf98c",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "2\\le x\\le 4,\\,-2\\le y\\le 0",
      ":db/id": 17592186257921
    },
    ":answer-field/id": "069877ab-6f59-5111-82b1-30e0cd6529a7",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186259045
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -1+3 & \le \operatorname{cos}⁡\theta +3\le 1+3 \\ 2 & \le x\le 4.\end{aligned}
$$

So, we can conclude that $2\le x\le 4.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -1-1 & \le \operatorname{sin}⁡\theta -1\le 1-1 \\ -2 & \le y\le 0.\end{aligned}
$$

So, we can conclude that $-2\le y\le 0.$

Therefore, the ranges are $2\le x\le 4$ and $-2\le y\le 0.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=\operatorname{cos}⁡\theta +3,\,y=\operatorname{sin}⁡\theta -1,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $-4\le x\le -2,\,0\le y\le 2$
- $2\le x\le 4,\,-2\le y\le 0$ (correct)
- $-3\le x\le 3,\,-2\le y\le 0$
- $2\le x\le 4,\,-1\le y\le 1$
- $-3\le x\le 3,\,-1\le y\le 1$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -1+3 & \le \operatorname{cos}⁡\theta +3\le 1+3 \\ 2 & \le x\le 4.\end{aligned}
$$

So, we can conclude that $2\le x\le 4.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -1-1 & \le \operatorname{sin}⁡\theta -1\le 1-1 \\ -2 & \le y\le 0.\end{aligned}
$$

So, we can conclude that $-2\le y\le 0.$

Therefore, the ranges are $2\le x\le 4$ and $-2\le y\le 0.$



### Generated variant — observed:q-123777

Given that a curve is defined parametrically as

$$
x=\operatorname{cos}⁡\theta +2,\,y=\operatorname{sin}⁡\theta -1,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $-2\le x\le 2,\,-1\le y\le 1$
- $1\le x\le 3,\,-2\le y\le 0$ (correct)
- $-3\le x\le -1,\,0\le y\le 2$
- $1\le x\le 3,\,-1\le y\le 1$
- $-2\le x\le 2,\,-2\le y\le 0$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -1+2 & \le \operatorname{cos}⁡\theta +2\le 1+2 \\ 1 & \le x\le 3.\end{aligned}
$$

So, we can conclude that $1\le x\le 3.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -1-1 & \le \operatorname{sin}⁡\theta -1\le 1-1 \\ -2 & \le y\le 0.\end{aligned}
$$

So, we can conclude that $-2\le y\le 0.$

Therefore, the ranges are $1\le x\le 3$ and $-2\le y\le 0.$



### Generated variant — authored:full-period

Given that a curve is defined parametrically as

$$
x=\operatorname{cos}⁡\theta +2,\,y=\operatorname{sin}⁡\theta -1,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $\frac{3}{2}\le x\le \frac{5}{2},\,-\frac{3}{2}\le y\le -\frac{1}{2}$
- $-1\le x\le 1,\,-1\le y\le 1$
- $0\le x\le 4,\,-3\le y\le 1$
- $-3\le x\le -1,\,0\le y\le 2$
- $1\le x\le 3,\,-2\le y\le 0$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -1+2 & \le \operatorname{cos}⁡\theta +2\le 1+2 \\ 1 & \le x\le 3.\end{aligned}
$$

So, we can conclude that $1\le x\le 3.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -1-1 & \le \operatorname{sin}⁡\theta -1\le 1-1 \\ -2 & \le y\le 0.\end{aligned}
$$

So, we can conclude that $-2\le y\le 0.$

Therefore, the ranges are $1\le x\le 3$ and $-2\le y\le 0.$



## Original q-276261 (moderate)



Given that a curve is defined parametrically as

$$
x=3\operatorname{cos}⁡\theta -2,\,y=-5\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}
$\le x$
{{field-2}}{{field-3}}.

The range of $y$ is 
{{field-4}}{{field-5}}
$y\le $
{{field-6}}.



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "890558a3-9356-5d6e-aa4a-ad58edb49c63",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-5",
        ":db/id": 17592186291214
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "890558a3-9356-5d6e-aa4a-ad58edb49c63",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-5",
      ":db/id": 17592186291214
    },
    ":answer-field/id": "03bdef3a-470f-56e8-a9e2-85dfe88918ed",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186291745
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "21859e3d-c55d-5cf1-b718-09d763da06c0",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5",
        ":db/id": 17592186290774
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "21859e3d-c55d-5cf1-b718-09d763da06c0",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "5",
      ":db/id": 17592186290774
    },
    ":answer-field/id": "0e7a8943-85f6-5e4b-8ed7-baf1b5c1290e",
    ":answer-field/key": "field-6",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186291786
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "2297de4e-8799-5789-9a4f-d7a28df071f6",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186290781
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "2297de4e-8799-5789-9a4f-d7a28df071f6",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186290781
    },
    ":answer-field/id": "1770cd36-566a-540a-9664-6096e07a7c7f",
    ":answer-field/key": "field-5",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186291821
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "e2c8c936-8e63-5e01-b130-1618f40a1130",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186291580
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "e2c8c936-8e63-5e01-b130-1618f40a1130",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186291580
    },
    ":answer-field/id": "56220752-c878-53e6-b767-353f3b803e6f",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186291997
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "c0c9fc2f-9440-50b7-99bb-6b61ac0be963",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1",
        ":db/id": 17592186291461
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "c0c9fc2f-9440-50b7-99bb-6b61ac0be963",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "1",
      ":db/id": 17592186291461
    },
    ":answer-field/id": "9b940c17-3920-5ba9-9e64-fea7544b7c01",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186292227
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "fe1e4193-5dae-59e5-9a11-ed901a28f7f7",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-5",
        ":db/id": 17592186291715
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "fe1e4193-5dae-59e5-9a11-ed901a28f7f7",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-5",
      ":db/id": 17592186291715
    },
    ":answer-field/id": "e309bee4-101d-5be8-8271-cb9e7e983669",
    ":answer-field/key": "field-4",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186292440
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -3 & \le 3\operatorname{cos}⁡\theta \le 3 \\ -3-2 & \le 3\operatorname{cos}⁡\theta -2\le 3-2 \\ -5 & \le x\le 1.\end{aligned}
$$

So, we can conclude that $-5\le x\le 1.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ 5 & \text{ }\ge -5\operatorname{sin}⁡\theta \text{ }\ge -5 \\ -5 & \le -5\operatorname{sin}⁡\theta \le 5 \\ -5 & \le y\le 5.\end{aligned}
$$

So, we can conclude that $-5\le y\le 5.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=3\operatorname{cos}⁡\theta -2,\,y=-5\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}
$\le x$
{{field-2}}{{field-3}}.

The range of $y$ is 
{{field-4}}{{field-5}}
$y\le $
{{field-6}}.

**field-1**
- $-5$ (correct)
**field-6**
- $5$ (correct)
**field-5**
- $\le $ (correct)
**field-2**
- $\le $ (correct)
**field-3**
- $1$ (correct)
**field-4**
- $-5$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -3 & \le 3\operatorname{cos}⁡\theta \le 3 \\ -3-2 & \le 3\operatorname{cos}⁡\theta -2\le 3-2 \\ -5 & \le x\le 1.\end{aligned}
$$

So, we can conclude that $-5\le x\le 1.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ 5 & \text{ }\ge -5\operatorname{sin}⁡\theta \text{ }\ge -5 \\ -5 & \le -5\operatorname{sin}⁡\theta \le 5 \\ -5 & \le y\le 5.\end{aligned}
$$

So, we can conclude that $-5\le y\le 5.$



### Generated variant — blank

Given that a curve is defined parametrically as

$$
x=7\operatorname{cos}⁡\theta -1,\,y=-2\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}
$\le x$
{{field-2}}{{field-3}}.

The range of $y$ is 
{{field-4}}{{field-5}}
$y\le $
{{field-6}}.

**field-1**
- $-8$ (correct)
**field-6**
- $2$ (correct)
**field-5**
- $\le $ (correct)
**field-2**
- $\le $ (correct)
**field-3**
- $6$ (correct)
**field-4**
- $-2$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -7 & \le 7\operatorname{cos}⁡\theta \le 7 \\ -7-1 & \le 7\operatorname{cos}⁡\theta -1\le 7-1 \\ -8 & \le x\le 6.\end{aligned}
$$

So, we can conclude that $-8\le x\le 6.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ 2 & \text{ }\ge -2\operatorname{sin}⁡\theta \text{ }\ge -2 \\ -2 & \le -2\operatorname{sin}⁡\theta \le 2 \\ -2 & \le y\le 2.\end{aligned}
$$

So, we can conclude that $-2\le y\le 2.$



## Original q-327861 (easy)



Given that a curve is defined parametrically as

$$
x=6\operatorname{cos}⁡\theta ,\,y=-3\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}} $\le $
$x$
{{field-2}}{{field-3}}.

 

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "44d09dea-aace-573a-a9c0-aba161ed95be",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186300305
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "44d09dea-aace-573a-a9c0-aba161ed95be",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186300305
    },
    ":answer-field/id": "2a7e8232-4ea7-50da-a729-8ae332ab2b56",
    ":answer-field/key": "field-5",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301361
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "67a265f0-04cb-52e1-9228-78c09deadd1b",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186300483
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "67a265f0-04cb-52e1-9228-78c09deadd1b",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186300483
    },
    ":answer-field/id": "409be484-6063-58b7-a05a-f2fdc00614c3",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301443
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "0f4feec6-f58b-5688-be02-649cde464b11",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-3",
        ":db/id": 17592186300021
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "0f4feec6-f58b-5688-be02-649cde464b11",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-3",
      ":db/id": 17592186300021
    },
    ":answer-field/id": "4e8f8b3d-430d-56b6-8191-d86f99809ba0",
    ":answer-field/key": "field-4",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301483
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "dd85e24d-182c-5f16-8f66-d77e2d0e26ce",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3",
        ":db/id": 17592186301060
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "dd85e24d-182c-5f16-8f66-d77e2d0e26ce",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "3",
      ":db/id": 17592186301060
    },
    ":answer-field/id": "56b9a56f-898b-5829-80c8-dec8f63fd5f7",
    ":answer-field/key": "field-6",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301509
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "c66424ca-46b9-57b2-9359-7ad964c9f421",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "6",
        ":db/id": 17592186300951
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "c66424ca-46b9-57b2-9359-7ad964c9f421",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "6",
      ":db/id": 17592186300951
    },
    ":answer-field/id": "58079772-113a-5e1a-94fb-1527fec1d568",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301515
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "ceaac6f2-a111-52f7-b826-6ea0183d9e4c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-6",
        ":db/id": 17592186300992
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "ceaac6f2-a111-52f7-b826-6ea0183d9e4c",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-6",
      ":db/id": 17592186300992
    },
    ":answer-field/id": "6eb6ad91-eafa-5bb6-9bee-ac536e160dce",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301571
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -6 & \le 6\operatorname{cos}⁡\theta \le 6 \\ -6 & \le x\le 6.\end{aligned}
$$

So, we can conclude that $-6\le x\le 6.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ 3 & \text{ }\ge -3\operatorname{sin}⁡\theta \text{ }\ge -3 \\ -3 & \le -3\operatorname{sin}⁡\theta \le 3 \\ -3 & \le y\le 3.\end{aligned}
$$

So, we can conclude that $-3\le y\le 3.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=6\operatorname{cos}⁡\theta ,\,y=-3\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}} $\le $
$x$
{{field-2}}{{field-3}}.

 

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.

**field-5**
- $\le $ (correct)
**field-2**
- $\le $ (correct)
**field-4**
- $-3$ (correct)
**field-6**
- $3$ (correct)
**field-3**
- $6$ (correct)
**field-1**
- $-6$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -6 & \le 6\operatorname{cos}⁡\theta \le 6 \\ -6 & \le x\le 6.\end{aligned}
$$

So, we can conclude that $-6\le x\le 6.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ 3 & \text{ }\ge -3\operatorname{sin}⁡\theta \text{ }\ge -3 \\ -3 & \le -3\operatorname{sin}⁡\theta \le 3 \\ -3 & \le y\le 3.\end{aligned}
$$

So, we can conclude that $-3\le y\le 3.$



### Generated variant — blank

Given that a curve is defined parametrically as

$$
x=7\operatorname{cos}⁡\theta ,\,y=-2\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}} $\le $
$x$
{{field-2}}{{field-3}}.

 

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.

**field-5**
- $\le $ (correct)
**field-2**
- $\le $ (correct)
**field-4**
- $-2$ (correct)
**field-6**
- $2$ (correct)
**field-3**
- $7$ (correct)
**field-1**
- $-7$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -7 & \le 7\operatorname{cos}⁡\theta \le 7 \\ -7 & \le x\le 7.\end{aligned}
$$

So, we can conclude that $-7\le x\le 7.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ 2 & \text{ }\ge -2\operatorname{sin}⁡\theta \text{ }\ge -2 \\ -2 & \le -2\operatorname{sin}⁡\theta \le 2 \\ -2 & \le y\le 2.\end{aligned}
$$

So, we can conclude that $-2\le y\le 2.$



## Original q-327866 (easy)



Given that a curve is defined parametrically as

$$
x=-\frac{9}{2}\operatorname{cos}⁡\theta ,\,y=\frac{5}{3}\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}{{field-2}}
$x\le $
{{field-3}}.

 

The range of $y$ is 
{{field-4}}{{field-5}}
$y\le $
{{field-6}}.



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "2f06285d-068b-5fa4-944b-e6233b16f402",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{9}{2}",
        ":db/id": 17592186300188
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "2f06285d-068b-5fa4-944b-e6233b16f402",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-\\frac{9}{2}",
      ":db/id": 17592186300188
    },
    ":answer-field/id": "3376a37b-a13f-5ab8-bbfb-f1f487da216b",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301389
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "819b15e1-b8f0-59e0-9418-1c05f5a38bb3",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{9}{2}",
        ":db/id": 17592186300606
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "819b15e1-b8f0-59e0-9418-1c05f5a38bb3",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{9}{2}",
      ":db/id": 17592186300606
    },
    ":answer-field/id": "86e1fd89-d176-5b5d-b50d-d31e5d3ad549",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301650
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "e801f68b-131d-5519-b2d8-74dc57eab834",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186301109
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "e801f68b-131d-5519-b2d8-74dc57eab834",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186301109
    },
    ":answer-field/id": "91ad3017-52b1-5370-a4ca-bf9c517b5a10",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301692
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "f2c07c65-a41d-5ccb-b882-47b8d03801e5",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186301160
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "f2c07c65-a41d-5ccb-b882-47b8d03801e5",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186301160
    },
    ":answer-field/id": "b842ecca-6eeb-5e12-a9ab-4581991c50c9",
    ":answer-field/key": "field-5",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301830
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "acf85b81-1b05-58a1-af4a-efe05db7b3a1",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{5}{3}",
        ":db/id": 17592186300828
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "acf85b81-1b05-58a1-af4a-efe05db7b3a1",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-\\frac{5}{3}",
      ":db/id": 17592186300828
    },
    ":answer-field/id": "be8dec0f-2a33-5e07-a73f-5e7684c3f26c",
    ":answer-field/key": "field-4",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301850
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "69ec357b-1fff-5c11-ae8a-d1015ea3e5ec",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{5}{3}",
        ":db/id": 17592186300494
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "69ec357b-1fff-5c11-ae8a-d1015ea3e5ec",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{5}{3}",
      ":db/id": 17592186300494
    },
    ":answer-field/id": "f07a0108-c4ed-546b-a41a-5190fbafa2bc",
    ":answer-field/key": "field-6",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301993
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ \frac{9}{2} & \text{ }\ge -\frac{9}{2}\operatorname{cos}⁡\theta \text{ }\ge -\frac{9}{2} \\ -\frac{9}{2} & \le -\frac{9}{2}\operatorname{cos}⁡\theta \le \frac{9}{2} \\ -\frac{9}{2} & \le x\le \frac{9}{2}.\end{aligned}
$$

So, we can conclude that $-\frac{9}{2}\le x\le \frac{9}{2}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -\frac{5}{3} & \le \frac{5}{3}\operatorname{sin}⁡\theta \le \frac{5}{3} \\ -\frac{5}{3} & \le y\le \frac{5}{3}.\end{aligned}
$$

So, we can conclude that $-\frac{5}{3}\le y\le \frac{5}{3}.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=-\frac{9}{2}\operatorname{cos}⁡\theta ,\,y=\frac{5}{3}\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}{{field-2}}
$x\le $
{{field-3}}.

 

The range of $y$ is 
{{field-4}}{{field-5}}
$y\le $
{{field-6}}.

**field-1**
- $-\frac{9}{2}$ (correct)
**field-3**
- $\frac{9}{2}$ (correct)
**field-2**
- $\le $ (correct)
**field-5**
- $\le $ (correct)
**field-4**
- $-\frac{5}{3}$ (correct)
**field-6**
- $\frac{5}{3}$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ \frac{9}{2} & \text{ }\ge -\frac{9}{2}\operatorname{cos}⁡\theta \text{ }\ge -\frac{9}{2} \\ -\frac{9}{2} & \le -\frac{9}{2}\operatorname{cos}⁡\theta \le \frac{9}{2} \\ -\frac{9}{2} & \le x\le \frac{9}{2}.\end{aligned}
$$

So, we can conclude that $-\frac{9}{2}\le x\le \frac{9}{2}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -\frac{5}{3} & \le \frac{5}{3}\operatorname{sin}⁡\theta \le \frac{5}{3} \\ -\frac{5}{3} & \le y\le \frac{5}{3}.\end{aligned}
$$

So, we can conclude that $-\frac{5}{3}\le y\le \frac{5}{3}.$



### Generated variant — blank

Given that a curve is defined parametrically as

$$
x=-\frac{2}{3}\operatorname{cos}⁡\theta ,\,y=\frac{1}{2}\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}{{field-2}}
$x\le $
{{field-3}}.

 

The range of $y$ is 
{{field-4}}{{field-5}}
$y\le $
{{field-6}}.

**field-1**
- $-\frac{2}{3}$ (correct)
**field-3**
- $\frac{2}{3}$ (correct)
**field-2**
- $\le $ (correct)
**field-5**
- $\le $ (correct)
**field-4**
- $-\frac{1}{2}$ (correct)
**field-6**
- $\frac{1}{2}$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ \frac{2}{3} & \text{ }\ge -\frac{2}{3}\operatorname{cos}⁡\theta \text{ }\ge -\frac{2}{3} \\ -\frac{2}{3} & \le -\frac{2}{3}\operatorname{cos}⁡\theta \le \frac{2}{3} \\ -\frac{2}{3} & \le x\le \frac{2}{3}.\end{aligned}
$$

So, we can conclude that $-\frac{2}{3}\le x\le \frac{2}{3}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -\frac{1}{2} & \le \frac{1}{2}\operatorname{sin}⁡\theta \le \frac{1}{2} \\ -\frac{1}{2} & \le y\le \frac{1}{2}.\end{aligned}
$$

So, we can conclude that $-\frac{1}{2}\le y\le \frac{1}{2}.$



## Original q-327871 (easy)



Given that a curve is defined parametrically as

$$
x=\frac{5}{2}\operatorname{cos}⁡\theta ,\,y=\frac{3}{4}\operatorname{sin}⁡\theta +2,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}{{field-2}}
$x\le $
{{field-3}}.

 

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "d30f187b-fbc7-5555-9352-52347a050623",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{5}{2}",
        ":db/id": 17592186301012
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "d30f187b-fbc7-5555-9352-52347a050623",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{5}{2}",
      ":db/id": 17592186301012
    },
    ":answer-field/id": "1c05764c-5a04-56aa-a88e-2abb2ff9e4b4",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301318
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "5748af4d-f841-52ef-8c55-174c66be49ad",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{5}{4}",
        ":db/id": 17592186300419
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "5748af4d-f841-52ef-8c55-174c66be49ad",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{5}{4}",
      ":db/id": 17592186300419
    },
    ":answer-field/id": "2229e40d-bb23-5bd7-85e9-34c30902bf76",
    ":answer-field/key": "field-4",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301336
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "d9902947-2ecb-5bba-b051-fa145700a481",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{5}{2}",
        ":db/id": 17592186301042
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "d9902947-2ecb-5bba-b051-fa145700a481",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-\\frac{5}{2}",
      ":db/id": 17592186301042
    },
    ":answer-field/id": "7d3342c2-7bdf-51b9-b165-a756ff5d30ef",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301616
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "928c6b31-6fbf-51b7-acf7-5ed12f3060cd",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186300697
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "928c6b31-6fbf-51b7-acf7-5ed12f3060cd",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186300697
    },
    ":answer-field/id": "89ce4367-0546-5a09-a511-7fbfab096ea1",
    ":answer-field/key": "field-5",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301660
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "5f832796-ed38-535c-9798-9c2eb492cf5c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186300449
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "5f832796-ed38-535c-9798-9c2eb492cf5c",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186300449
    },
    ":answer-field/id": "93ed438b-5800-5495-83cb-c0d5c94685dc",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301699
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "8d273f0d-e310-5f65-81da-3843b4526f67",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{11}{4}",
        ":db/id": 17592186300675
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "8d273f0d-e310-5f65-81da-3843b4526f67",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{11}{4}",
      ":db/id": 17592186300675
    },
    ":answer-field/id": "ddd586d3-d4ab-5e96-8d5f-97950983ae94",
    ":answer-field/key": "field-6",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301933
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -\frac{5}{2} & \le \frac{5}{2}\operatorname{cos}⁡\theta \le \frac{5}{2} \\ -\frac{5}{2} & \le x\le \frac{5}{2}.\end{aligned}
$$

So, we can conclude that $-\frac{5}{2}\le x\le \frac{5}{2}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -\frac{3}{4} & \le \frac{3}{4}\operatorname{sin}⁡\theta \le \frac{3}{4} \\ -\frac{3}{4}+2 & \le \frac{3}{4}\operatorname{sin}⁡\theta +2\le \frac{3}{4}+2 \\ \frac{5}{4} & \le y\le \frac{11}{4}.\end{aligned}
$$

So, we can conclude that $\frac{5}{4}\le y\le \frac{11}{4}.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=\frac{5}{2}\operatorname{cos}⁡\theta ,\,y=\frac{3}{4}\operatorname{sin}⁡\theta +2,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}{{field-2}}
$x\le $
{{field-3}}.

 

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.

**field-3**
- $\frac{5}{2}$ (correct)
**field-4**
- $\frac{5}{4}$ (correct)
**field-1**
- $-\frac{5}{2}$ (correct)
**field-5**
- $\le $ (correct)
**field-2**
- $\le $ (correct)
**field-6**
- $\frac{11}{4}$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -\frac{5}{2} & \le \frac{5}{2}\operatorname{cos}⁡\theta \le \frac{5}{2} \\ -\frac{5}{2} & \le x\le \frac{5}{2}.\end{aligned}
$$

So, we can conclude that $-\frac{5}{2}\le x\le \frac{5}{2}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -\frac{3}{4} & \le \frac{3}{4}\operatorname{sin}⁡\theta \le \frac{3}{4} \\ -\frac{3}{4}+2 & \le \frac{3}{4}\operatorname{sin}⁡\theta +2\le \frac{3}{4}+2 \\ \frac{5}{4} & \le y\le \frac{11}{4}.\end{aligned}
$$

So, we can conclude that $\frac{5}{4}\le y\le \frac{11}{4}.$



### Generated variant — blank

Given that a curve is defined parametrically as

$$
x=\frac{2}{3}\operatorname{cos}⁡\theta ,\,y=\frac{1}{2}\operatorname{sin}⁡\theta +5,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}{{field-2}}
$x\le $
{{field-3}}.

 

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.

**field-3**
- $\frac{2}{3}$ (correct)
**field-4**
- $\frac{9}{2}$ (correct)
**field-1**
- $-\frac{2}{3}$ (correct)
**field-5**
- $\le $ (correct)
**field-2**
- $\le $ (correct)
**field-6**
- $\frac{11}{2}$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -\frac{2}{3} & \le \frac{2}{3}\operatorname{cos}⁡\theta \le \frac{2}{3} \\ -\frac{2}{3} & \le x\le \frac{2}{3}.\end{aligned}
$$

So, we can conclude that $-\frac{2}{3}\le x\le \frac{2}{3}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have 
$-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -\frac{1}{2} & \le \frac{1}{2}\operatorname{sin}⁡\theta \le \frac{1}{2} \\ -\frac{1}{2}+5 & \le \frac{1}{2}\operatorname{sin}⁡\theta +5\le \frac{1}{2}+5 \\ \frac{9}{2} & \le y\le \frac{11}{2}.\end{aligned}
$$

So, we can conclude that $\frac{9}{2}\le y\le \frac{11}{2}.$



## Original q-327880 (moderate)



Given that a curve is defined parametrically as

$$
x=4\operatorname{cos}⁡\theta +1,\,y=-\frac{7}{2}\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}{{field-2}}
$x\le $
{{field-3}}.

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "5fc55285-7159-598c-b031-86c3a09369ab",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186300452
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "5fc55285-7159-598c-b031-86c3a09369ab",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186300452
    },
    ":answer-field/id": "5454d034-fb34-5c9d-9fdc-5040c6123974",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301500
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "c6f2b08d-def0-5143-ae5b-f41692d30357",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{7}{2}",
        ":db/id": 17592186300959
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "c6f2b08d-def0-5143-ae5b-f41692d30357",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{7}{2}",
      ":db/id": 17592186300959
    },
    ":answer-field/id": "8a9096a0-c2c7-59b6-b3c3-5386eaf386e7",
    ":answer-field/key": "field-6",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301664
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "7c95b9b0-7ba0-5073-9f2d-563965383d18",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186300583
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "7c95b9b0-7ba0-5073-9f2d-563965383d18",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186300583
    },
    ":answer-field/id": "96bcc7e2-f339-5182-b5f0-bfde676ee25e",
    ":answer-field/key": "field-5",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301712
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "a59b66b8-bb6c-5716-8359-9841a785b96e",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{7}{2}",
        ":db/id": 17592186300796
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "a59b66b8-bb6c-5716-8359-9841a785b96e",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-\\frac{7}{2}",
      ":db/id": 17592186300796
    },
    ":answer-field/id": "c60c382b-7d82-57a8-8cef-69926f265ce4",
    ":answer-field/key": "field-4",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301870
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "d4247821-e580-5fc8-98d1-a08e417bfbaf",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5",
        ":db/id": 17592186301015
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "d4247821-e580-5fc8-98d1-a08e417bfbaf",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "5",
      ":db/id": 17592186301015
    },
    ":answer-field/id": "ee9fa8e4-1c0b-5d54-9a59-99c1788d4265",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301985
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "3ebdcead-7efa-5de3-8e9c-264e42042a3a",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-3",
        ":db/id": 17592186300269
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "3ebdcead-7efa-5de3-8e9c-264e42042a3a",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-3",
      ":db/id": 17592186300269
    },
    ":answer-field/id": "f3cbff61-4663-5522-a8be-014cc1f10714",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186302004
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -4 & \le 4\operatorname{cos}⁡\theta \le 4 \\ -4+1 & \le 4\operatorname{cos}⁡\theta +1\le 4+1 \\ -3 & \le x\le 5.\end{aligned}
$$

So, we can conclude that $-3\le x\le 5.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ \frac{7}{2} & \text{ }\ge -\frac{7}{2}\operatorname{sin}⁡\theta \text{ }\ge -\frac{7}{2} \\ -\frac{7}{2} & \le -\frac{7}{2}\operatorname{sin}⁡\theta \le \frac{7}{2} \\ -\frac{7}{2} & \le y\le \frac{7}{2}.\end{aligned}
$$

So, we can conclude that $-\frac{7}{2}\le y\le \frac{7}{2}.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=4\operatorname{cos}⁡\theta +1,\,y=-\frac{7}{2}\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}{{field-2}}
$x\le $
{{field-3}}.

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.

**field-2**
- $\le $ (correct)
**field-6**
- $\frac{7}{2}$ (correct)
**field-5**
- $\le $ (correct)
**field-4**
- $-\frac{7}{2}$ (correct)
**field-3**
- $5$ (correct)
**field-1**
- $-3$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -4 & \le 4\operatorname{cos}⁡\theta \le 4 \\ -4+1 & \le 4\operatorname{cos}⁡\theta +1\le 4+1 \\ -3 & \le x\le 5.\end{aligned}
$$

So, we can conclude that $-3\le x\le 5.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ \frac{7}{2} & \text{ }\ge -\frac{7}{2}\operatorname{sin}⁡\theta \text{ }\ge -\frac{7}{2} \\ -\frac{7}{2} & \le -\frac{7}{2}\operatorname{sin}⁡\theta \le \frac{7}{2} \\ -\frac{7}{2} & \le y\le \frac{7}{2}.\end{aligned}
$$

So, we can conclude that $-\frac{7}{2}\le y\le \frac{7}{2}.$



### Generated variant — blank

Given that a curve is defined parametrically as

$$
x=7\operatorname{cos}⁡\theta +1,\,y=-\frac{2}{3}\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}{{field-2}}
$x\le $
{{field-3}}.

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.

**field-2**
- $\le $ (correct)
**field-6**
- $\frac{2}{3}$ (correct)
**field-5**
- $\le $ (correct)
**field-4**
- $-\frac{2}{3}$ (correct)
**field-3**
- $8$ (correct)
**field-1**
- $-6$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -7 & \le 7\operatorname{cos}⁡\theta \le 7 \\ -7+1 & \le 7\operatorname{cos}⁡\theta +1\le 7+1 \\ -6 & \le x\le 8.\end{aligned}
$$

So, we can conclude that $-6\le x\le 8.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ \frac{2}{3} & \text{ }\ge -\frac{2}{3}\operatorname{sin}⁡\theta \text{ }\ge -\frac{2}{3} \\ -\frac{2}{3} & \le -\frac{2}{3}\operatorname{sin}⁡\theta \le \frac{2}{3} \\ -\frac{2}{3} & \le y\le \frac{2}{3}.\end{aligned}
$$

So, we can conclude that $-\frac{2}{3}\le y\le \frac{2}{3}.$



## Original q-327884 (moderate)



Given that a curve is defined parametrically as

$$
x=\frac{1}{3}-\frac{4}{3}\operatorname{cos}⁡\theta ,\,y=\frac{5}{2}\operatorname{sin}⁡\theta -\frac{7}{3},\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}
$\le x$
{{field-2}}{{field-3}}.

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "e53605c5-4363-5d5f-b627-9bba58dd0c48",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{29}{6}",
        ":db/id": 17592186301099
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "e53605c5-4363-5d5f-b627-9bba58dd0c48",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-\\frac{29}{6}",
      ":db/id": 17592186301099
    },
    ":answer-field/id": "086d7618-2535-5345-9129-765eb6f7c1c8",
    ":answer-field/key": "field-4",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301247
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "9fa32927-57bc-54aa-b114-9579aa439c4e",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{5}{3}",
        ":db/id": 17592186300768
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "9fa32927-57bc-54aa-b114-9579aa439c4e",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{5}{3}",
      ":db/id": 17592186300768
    },
    ":answer-field/id": "405f7999-f299-5f59-acf3-e6e5e6a0b45d",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301439
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "9f28241e-65cb-5b80-acc1-026bd48c7da6",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186300766
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "9f28241e-65cb-5b80-acc1-026bd48c7da6",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186300766
    },
    ":answer-field/id": "b4d049d7-b2b7-57d2-8e2a-eb4b0f23b4ff",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301814
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "dd0530d4-6382-56f0-b554-f39db23d32aa",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\le ",
        ":db/id": 17592186301055
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "dd0530d4-6382-56f0-b554-f39db23d32aa",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\le ",
      ":db/id": 17592186301055
    },
    ":answer-field/id": "b5d19a88-e498-5a2d-88ed-85da032971ff",
    ":answer-field/key": "field-5",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301819
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "b00d5423-c232-574f-bf45-5b3f5a0e5fc7",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{1}{6}",
        ":db/id": 17592186300840
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "b00d5423-c232-574f-bf45-5b3f5a0e5fc7",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{1}{6}",
      ":db/id": 17592186300840
    },
    ":answer-field/id": "b68a5aa9-6b04-5d45-8715-32adf9ead188",
    ":answer-field/key": "field-6",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301824
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "72c185d8-fa43-53bf-b4a9-350d066cb586",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-1",
        ":db/id": 17592186300533
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "72c185d8-fa43-53bf-b4a9-350d066cb586",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-1",
      ":db/id": 17592186300533
    },
    ":answer-field/id": "f117f64d-057e-5a62-a0f1-b60e45fc5a11",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301995
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ \frac{4}{3} & \text{ }\ge -\frac{4}{3}\operatorname{cos}⁡\theta \text{ }\ge -\frac{4}{3} \\ -\frac{4}{3} & \le -\frac{4}{3}\operatorname{cos}⁡\theta \le \frac{4}{3} \\ \frac{1}{3}-\frac{4}{3} & \le \frac{1}{3}-\frac{4}{3}\operatorname{cos}⁡\theta \le \frac{1}{3}+\frac{4}{3} \\ -1 & \le x\le \frac{5}{3}.\end{aligned}
$$

So, we can conclude that $-1\le x\le \frac{5}{3}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -\frac{5}{2} & \le \frac{5}{2}\operatorname{sin}⁡\theta \le \frac{5}{2} \\ -\frac{5}{2}-\frac{7}{3} & \le \frac{5}{2}\operatorname{sin}⁡\theta -\frac{7}{3}\le \frac{5}{2}-\frac{7}{3} \\ -\frac{29}{6} & \le y\le \frac{1}{6}.\end{aligned}
$$

So, we can conclude that $-\frac{29}{6}\le y\le \frac{1}{6}.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=\frac{1}{3}-\frac{4}{3}\operatorname{cos}⁡\theta ,\,y=\frac{5}{2}\operatorname{sin}⁡\theta -\frac{7}{3},\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}
$\le x$
{{field-2}}{{field-3}}.

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.

**field-4**
- $-\frac{29}{6}$ (correct)
**field-3**
- $\frac{5}{3}$ (correct)
**field-2**
- $\le $ (correct)
**field-5**
- $\le $ (correct)
**field-6**
- $\frac{1}{6}$ (correct)
**field-1**
- $-1$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ \frac{4}{3} & \text{ }\ge -\frac{4}{3}\operatorname{cos}⁡\theta \text{ }\ge -\frac{4}{3} \\ -\frac{4}{3} & \le -\frac{4}{3}\operatorname{cos}⁡\theta \le \frac{4}{3} \\ \frac{1}{3}-\frac{4}{3} & \le \frac{1}{3}-\frac{4}{3}\operatorname{cos}⁡\theta \le \frac{1}{3}+\frac{4}{3} \\ -1 & \le x\le \frac{5}{3}.\end{aligned}
$$

So, we can conclude that $-1\le x\le \frac{5}{3}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -\frac{5}{2} & \le \frac{5}{2}\operatorname{sin}⁡\theta \le \frac{5}{2} \\ -\frac{5}{2}-\frac{7}{3} & \le \frac{5}{2}\operatorname{sin}⁡\theta -\frac{7}{3}\le \frac{5}{2}-\frac{7}{3} \\ -\frac{29}{6} & \le y\le \frac{1}{6}.\end{aligned}
$$

So, we can conclude that $-\frac{29}{6}\le y\le \frac{1}{6}.$



### Generated variant — blank

Given that a curve is defined parametrically as

$$
x=\frac{5}{2}-\frac{2}{3}\operatorname{cos}⁡\theta ,\,y=\frac{1}{2}\operatorname{sin}⁡\theta -\frac{4}{3},\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is 
{{field-1}}
$\le x$
{{field-2}}{{field-3}}.

The range of $y$ is 
{{field-4}}
$\le y$
{{field-5}}{{field-6}}.

**field-4**
- $-\frac{11}{6}$ (correct)
**field-3**
- $\frac{19}{6}$ (correct)
**field-2**
- $\le $ (correct)
**field-5**
- $\le $ (correct)
**field-6**
- $-\frac{5}{6}$ (correct)
**field-1**
- $\frac{11}{6}$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ \frac{2}{3} & \text{ }\ge -\frac{2}{3}\operatorname{cos}⁡\theta \text{ }\ge -\frac{2}{3} \\ -\frac{2}{3} & \le -\frac{2}{3}\operatorname{cos}⁡\theta \le \frac{2}{3} \\ \frac{5}{2}-\frac{2}{3} & \le \frac{5}{2}-\frac{2}{3}\operatorname{cos}⁡\theta \le \frac{5}{2}+\frac{2}{3} \\ \frac{11}{6} & \le x\le \frac{19}{6}.\end{aligned}
$$

So, we can conclude that $\frac{11}{6}\le x\le \frac{19}{6}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ 
we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -\frac{1}{2} & \le \frac{1}{2}\operatorname{sin}⁡\theta \le \frac{1}{2} \\ -\frac{1}{2}-\frac{4}{3} & \le \frac{1}{2}\operatorname{sin}⁡\theta -\frac{4}{3}\le \frac{1}{2}-\frac{4}{3} \\ -\frac{11}{6} & \le y\le -\frac{5}{6}.\end{aligned}
$$

So, we can conclude that $-\frac{11}{6}\le y\le -\frac{5}{6}.$



## Original q-70523 (moderate)



Given that a curve is defined parametrically as

$$
x=\operatorname{cos}⁡\theta +5,\,\,\,y=6\operatorname{sin}⁡\theta -7,\,0\le \theta <2\pi ,
$$

determine the ranges of $x$ and $y.$



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "05970e26-5821-56d5-9192-cd54ac992296",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1\\le x\\le 5,\\,-9\\le y\\le -2",
        ":db/id": 17592186336077
      },
      {
        ":answer/id": "66a3960b-62dc-53fd-84aa-3678e0fb86aa",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-2\\le x\\le 13,\\,3\\le y\\le 7",
        ":db/id": 17592186336947
      },
      {
        ":answer/id": "712b9c6e-788b-5ba0-8229-df8fca209a1f",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "4\\le x\\le 6,\\,-13\\le y\\le -1",
        ":db/id": 17592186337040
      },
      {
        ":answer/id": "8f5bbdd7-51a4-577f-a287-db618f622b13",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "0\\le x\\le 5,\\,-7\\le y\\le 0",
        ":db/id": 17592186337327
      },
      {
        ":answer/id": "fa563dbb-82b3-57bc-8de5-0041f39c1575",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-6\\le x\\le 0,\\,1\\le y\\le 7",
        ":db/id": 17592186338226
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "712b9c6e-788b-5ba0-8229-df8fca209a1f",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "4\\le x\\le 6,\\,-13\\le y\\le -1",
      ":db/id": 17592186337040
    },
    ":answer-field/id": "f957fa19-2286-54e9-bed6-f7be3613a470",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186338716
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -1+5 & \le \operatorname{cos}⁡\theta +5\le 1+5 \\ 4 & \le x\le 6.\end{aligned}
$$

So, we can conclude that $4\le x\le 6.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -6 & \le 6\operatorname{sin}⁡\theta \le 6 \\ -6-7 & \le 6\operatorname{sin}⁡\theta -7\le 6-7 \\ -13 & \le y\le -1.\end{aligned}
$$

So, we can conclude that $-13\le y\le -1.$

Therefore, the ranges are $4\le x\le 6$ and $-13\le y\le -1.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=\operatorname{cos}⁡\theta +5,\,\,\,y=6\operatorname{sin}⁡\theta -7,\,0\le \theta <2\pi ,
$$

determine the ranges of $x$ and $y.$

**selection**
- $4\le x\le 6,\,-13\le y\le -1$ (correct)
- $-2\le x\le 13,\,3\le y\le 7$
- $1\le x\le 5,\,-9\le y\le -2$
- $-6\le x\le 0,\,1\le y\le 7$
- $0\le x\le 5,\,-7\le y\le 0$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -1+5 & \le \operatorname{cos}⁡\theta +5\le 1+5 \\ 4 & \le x\le 6.\end{aligned}
$$

So, we can conclude that $4\le x\le 6.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -6 & \le 6\operatorname{sin}⁡\theta \le 6 \\ -6-7 & \le 6\operatorname{sin}⁡\theta -7\le 6-7 \\ -13 & \le y\le -1.\end{aligned}
$$

So, we can conclude that $-13\le y\le -1.$

Therefore, the ranges are $4\le x\le 6$ and $-13\le y\le -1.$



### Generated variant — observed:q-70523

Given that a curve is defined parametrically as

$$
x=\operatorname{cos}⁡\theta +2,\,\,\,y=7\operatorname{sin}⁡\theta -1,\,0\le \theta <2\pi ,
$$

determine the ranges of $x$ and $y.$

**selection**
- $0\le x\le 2,\,-1\le y\le 0$
- $-2\le x\le 8,\,0\le y\le 1$
- $1\le x\le 3,\,-8\le y\le 6$ (correct)
- $-3\le x\le 0,\,1\le y\le 1$
- $1\le x\le 2,\,-3\le y\le 1$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -1+2 & \le \operatorname{cos}⁡\theta +2\le 1+2 \\ 1 & \le x\le 3.\end{aligned}
$$

So, we can conclude that $1\le x\le 3.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -7 & \le 7\operatorname{sin}⁡\theta \le 7 \\ -7-1 & \le 7\operatorname{sin}⁡\theta -1\le 7-1 \\ -8 & \le y\le 6.\end{aligned}
$$

So, we can conclude that $-8\le y\le 6.$

Therefore, the ranges are $1\le x\le 3$ and $-8\le y\le 6.$



### Generated variant — authored:full-period

Given that a curve is defined parametrically as

$$
x=\operatorname{cos}⁡\theta +2,\,\,\,y=7\operatorname{sin}⁡\theta -1,\,0\le \theta <2\pi ,
$$

determine the ranges of $x$ and $y.$

**selection**
- $\frac{3}{2}\le x\le \frac{5}{2},\,-\frac{9}{2}\le y\le \frac{5}{2}$
- $-1\le x\le 1,\,-7\le y\le 7$
- $0\le x\le 4,\,-15\le y\le 13$
- $-3\le x\le -1,\,-6\le y\le 8$
- $1\le x\le 3,\,-8\le y\le 6$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -1+2 & \le \operatorname{cos}⁡\theta +2\le 1+2 \\ 1 & \le x\le 3.\end{aligned}
$$

So, we can conclude that $1\le x\le 3.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -7 & \le 7\operatorname{sin}⁡\theta \le 7 \\ -7-1 & \le 7\operatorname{sin}⁡\theta -1\le 7-1 \\ -8 & \le y\le 6.\end{aligned}
$$

So, we can conclude that $-8\le y\le 6.$

Therefore, the ranges are $1\le x\le 3$ and $-8\le y\le 6.$



## Original q-73626 (moderate)



Given that a curve is defined parametrically as

$$
x=1-2\operatorname{cos}⁡\theta ,\,\,\,y=2\operatorname{sin}⁡\theta -3,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "0f6b6688-7ebd-5b25-83b7-5c07ad7c688a",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2\\le x\\le 5,\\,1\\le y\\le 5",
        ":db/id": 17592186339270
      },
      {
        ":answer/id": "25d8d7af-c8e4-5ebb-980e-a55d3a4cd6d7",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-1\\le x\\le 3,\\,-5\\le y\\le -1",
        ":db/id": 17592186339454
      },
      {
        ":answer/id": "3320f739-78f0-51e9-9081-4e93b3163fc2",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1\\le x\\le 4,\\,-1\\le y\\le 5",
        ":db/id": 17592186339582
      },
      {
        ":answer/id": "94fae60d-72de-52be-8e5a-de4200f76d69",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1\\le x\\le 6,\\,-5\\le y\\le -1",
        ":db/id": 17592186340469
      },
      {
        ":answer/id": "dbd74067-cc9b-5848-b108-229097ff8d94",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-1\\le x\\le 0,\\,-5\\le y\\le 0",
        ":db/id": 17592186341079
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "25d8d7af-c8e4-5ebb-980e-a55d3a4cd6d7",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-1\\le x\\le 3,\\,-5\\le y\\le -1",
      ":db/id": 17592186339454
    },
    ":answer-field/id": "b483317f-a4a2-5639-8bcf-ae196dafce5d",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186341697
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ 2 & \text{ }\ge -2\operatorname{cos}⁡\theta \text{ }\ge -2 \\ -2 & \le -2\operatorname{cos}⁡\theta \le 2 \\ 1-2 & \le 1-2\operatorname{cos}⁡\theta \le 1+2 \\ -1 & \le x\le 3.\end{aligned}
$$

So, we can conclude that $-1\le x\le 3.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -2 & \le 2\operatorname{sin}⁡\theta \le 2 \\ -2-3 & \le 2\operatorname{sin}⁡\theta -3\le 2-3 \\ -5 & \le y\le -1.\end{aligned}
$$

So, we can conclude that $-5\le y\le -1.$

Therefore, the ranges are $-1\le x\le 3$ and $-5\le y\le -1.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=1-2\operatorname{cos}⁡\theta ,\,\,\,y=2\operatorname{sin}⁡\theta -3,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $1\le x\le 4,\,-1\le y\le 5$
- $-1\le x\le 3,\,-5\le y\le -1$ (correct)
- $2\le x\le 5,\,1\le y\le 5$
- $-1\le x\le 0,\,-5\le y\le 0$
- $1\le x\le 6,\,-5\le y\le -1$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ 2 & \text{ }\ge -2\operatorname{cos}⁡\theta \text{ }\ge -2 \\ -2 & \le -2\operatorname{cos}⁡\theta \le 2 \\ 1-2 & \le 1-2\operatorname{cos}⁡\theta \le 1+2 \\ -1 & \le x\le 3.\end{aligned}
$$

So, we can conclude that $-1\le x\le 3.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -2 & \le 2\operatorname{sin}⁡\theta \le 2 \\ -2-3 & \le 2\operatorname{sin}⁡\theta -3\le 2-3 \\ -5 & \le y\le -1.\end{aligned}
$$

So, we can conclude that $-5\le y\le -1.$

Therefore, the ranges are $-1\le x\le 3$ and $-5\le y\le -1.$



### Generated variant — observed:q-73626

Given that a curve is defined parametrically as

$$
x=1-7\operatorname{cos}⁡\theta ,\,\,\,y=2\operatorname{sin}⁡\theta -5,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $1\le x\le 6,\,-7\le y\le -3$
- $-6\le x\le 8,\,-7\le y\le -3$ (correct)
- $1\le x\le 4,\,-3\le y\le 7$
- $-6\le x\le 0,\,-7\le y\le 0$
- $2\le x\le 7,\,3\le y\le 7$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ 7 & \text{ }\ge -7\operatorname{cos}⁡\theta \text{ }\ge -7 \\ -7 & \le -7\operatorname{cos}⁡\theta \le 7 \\ 1-7 & \le 1-7\operatorname{cos}⁡\theta \le 1+7 \\ -6 & \le x\le 8.\end{aligned}
$$

So, we can conclude that $-6\le x\le 8.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -2 & \le 2\operatorname{sin}⁡\theta \le 2 \\ -2-5 & \le 2\operatorname{sin}⁡\theta -5\le 2-5 \\ -7 & \le y\le -3.\end{aligned}
$$

So, we can conclude that $-7\le y\le -3.$

Therefore, the ranges are $-6\le x\le 8$ and $-7\le y\le -3.$



### Generated variant — authored:full-period

Given that a curve is defined parametrically as

$$
x=1-7\operatorname{cos}⁡\theta ,\,\,\,y=2\operatorname{sin}⁡\theta -5,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $-\frac{5}{2}\le x\le \frac{9}{2},\,-6\le y\le -4$
- $-7\le x\le 7,\,-2\le y\le 2$
- $-13\le x\le 15,\,-9\le y\le -1$
- $-8\le x\le 6,\,3\le y\le 7$
- $-6\le x\le 8,\,-7\le y\le -3$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ 7 & \text{ }\ge -7\operatorname{cos}⁡\theta \text{ }\ge -7 \\ -7 & \le -7\operatorname{cos}⁡\theta \le 7 \\ 1-7 & \le 1-7\operatorname{cos}⁡\theta \le 1+7 \\ -6 & \le x\le 8.\end{aligned}
$$

So, we can conclude that $-6\le x\le 8.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -2 & \le 2\operatorname{sin}⁡\theta \le 2 \\ -2-5 & \le 2\operatorname{sin}⁡\theta -5\le 2-5 \\ -7 & \le y\le -3.\end{aligned}
$$

So, we can conclude that $-7\le y\le -3.$

Therefore, the ranges are $-6\le x\le 8$ and $-7\le y\le -3.$



## Original q-73632 (moderate)



Given that a curve is defined parametrically as

$$
x=2\operatorname{cos}⁡\theta +1,\,\,\,y=\frac{1}{2}\operatorname{sin}⁡\theta +\frac{3}{2},\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "0fcf5022-4812-5cf2-a745-37302fcd5dc9",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-2\\le x\\le -1,\\,-1\\le y\\le 3",
        ":db/id": 17592186339275
      },
      {
        ":answer/id": "4915a118-a0a0-5db9-914a-1721d3b42565",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-3\\le x\\le 1,\\,-2\\le y\\le 1",
        ":db/id": 17592186339784
      },
      {
        ":answer/id": "b457cadc-b9f6-5c2c-9f2c-42f3a633bbd8",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-1\\le x\\le 3,\\,1\\le y\\le 2",
        ":db/id": 17592186340764
      },
      {
        ":answer/id": "d4206d0e-3e82-51c1-8e8c-9cad7033e6f5",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1\\le x\\le 3,\\,-1\\le y\\le 2",
        ":db/id": 17592186341005
      },
      {
        ":answer/id": "e66ef8b5-6026-532a-a34b-a4ed72b384c0",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-1\\le x\\le 2,\\,1\\le y\\le 3",
        ":db/id": 17592186341166
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "b457cadc-b9f6-5c2c-9f2c-42f3a633bbd8",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-1\\le x\\le 3,\\,1\\le y\\le 2",
      ":db/id": 17592186340764
    },
    ":answer-field/id": "c59dee8b-2e72-5994-98ef-02b4aa2af213",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186341726
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -2 & \le 2\operatorname{cos}⁡\theta \le 2 \\ -2+1 & \le 2\operatorname{cos}⁡\theta +1\le 2+1 \\ -1 & \le x\le 3.\end{aligned}
$$

So, we can conclude that $-1\le x\le 3.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -\frac{1}{2} & \le \frac{1}{2}\operatorname{sin}⁡\theta \le \frac{1}{2} \\ -\frac{1}{2}+\frac{3}{2} & \le \frac{1}{2}\operatorname{sin}⁡\theta +\frac{3}{2}\le \frac{1}{2}+\frac{3}{2} \\ 1 & \le y\le 2.\end{aligned}
$$

So, we can conclude that $1\le y\le 2.$

Therefore, the ranges are $-1\le x\le 3$ and $1\le y\le 2.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=2\operatorname{cos}⁡\theta +1,\,\,\,y=\frac{1}{2}\operatorname{sin}⁡\theta +\frac{3}{2},\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $-1\le x\le 3,\,1\le y\le 2$ (correct)
- $-3\le x\le 1,\,-2\le y\le 1$
- $-2\le x\le -1,\,-1\le y\le 3$
- $-1\le x\le 2,\,1\le y\le 3$
- $1\le x\le 3,\,-1\le y\le 2$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -2 & \le 2\operatorname{cos}⁡\theta \le 2 \\ -2+1 & \le 2\operatorname{cos}⁡\theta +1\le 2+1 \\ -1 & \le x\le 3.\end{aligned}
$$

So, we can conclude that $-1\le x\le 3.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -\frac{1}{2} & \le \frac{1}{2}\operatorname{sin}⁡\theta \le \frac{1}{2} \\ -\frac{1}{2}+\frac{3}{2} & \le \frac{1}{2}\operatorname{sin}⁡\theta +\frac{3}{2}\le \frac{1}{2}+\frac{3}{2} \\ 1 & \le y\le 2.\end{aligned}
$$

So, we can conclude that $1\le y\le 2.$

Therefore, the ranges are $-1\le x\le 3$ and $1\le y\le 2.$



### Generated variant — observed:q-73632

Given that a curve is defined parametrically as

$$
x=7\operatorname{cos}⁡\theta +1,\,\,\,y=\frac{2}{3}\operatorname{sin}⁡\theta +\frac{5}{2},\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $1\le x\le 8,\,-1\le y\le \frac{19}{6}$
- $-8\le x\le 1,\,-7\le y\le 1$
- $-6\le x\le 8,\,\frac{11}{6}\le y\le \frac{19}{6}$ (correct)
- $-6\le x\le 7,\,\frac{11}{6}\le y\le 8$
- $-7\le x\le -1,\,-1\le y\le 8$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -7 & \le 7\operatorname{cos}⁡\theta \le 7 \\ -7+1 & \le 7\operatorname{cos}⁡\theta +1\le 7+1 \\ -6 & \le x\le 8.\end{aligned}
$$

So, we can conclude that $-6\le x\le 8.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -\frac{2}{3} & \le \frac{2}{3}\operatorname{sin}⁡\theta \le \frac{2}{3} \\ -\frac{2}{3}+\frac{5}{2} & \le \frac{2}{3}\operatorname{sin}⁡\theta +\frac{5}{2}\le \frac{2}{3}+\frac{5}{2} \\ \frac{11}{6} & \le y\le \frac{19}{6}.\end{aligned}
$$

So, we can conclude that $\frac{11}{6}\le y\le \frac{19}{6}.$

Therefore, the ranges are $-6\le x\le 8$ and $\frac{11}{6}\le y\le \frac{19}{6}.$



### Generated variant — authored:full-period

Given that a curve is defined parametrically as

$$
x=7\operatorname{cos}⁡\theta +1,\,\,\,y=\frac{2}{3}\operatorname{sin}⁡\theta +\frac{5}{2},\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $-\frac{5}{2}\le x\le \frac{9}{2},\,\frac{13}{6}\le y\le \frac{17}{6}$
- $-7\le x\le 7,\,-\frac{2}{3}\le y\le \frac{2}{3}$
- $-13\le x\le 15,\,\frac{7}{6}\le y\le \frac{23}{6}$
- $-8\le x\le 6,\,-\frac{19}{6}\le y\le -\frac{11}{6}$
- $-6\le x\le 8,\,\frac{11}{6}\le y\le \frac{19}{6}$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -7 & \le 7\operatorname{cos}⁡\theta \le 7 \\ -7+1 & \le 7\operatorname{cos}⁡\theta +1\le 7+1 \\ -6 & \le x\le 8.\end{aligned}
$$

So, we can conclude that $-6\le x\le 8.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -\frac{2}{3} & \le \frac{2}{3}\operatorname{sin}⁡\theta \le \frac{2}{3} \\ -\frac{2}{3}+\frac{5}{2} & \le \frac{2}{3}\operatorname{sin}⁡\theta +\frac{5}{2}\le \frac{2}{3}+\frac{5}{2} \\ \frac{11}{6} & \le y\le \frac{19}{6}.\end{aligned}
$$

So, we can conclude that $\frac{11}{6}\le y\le \frac{19}{6}.$

Therefore, the ranges are $-6\le x\le 8$ and $\frac{11}{6}\le y\le \frac{19}{6}.$



## Original q-123773 (easy)



Given that a curve is defined parametrically as

$$
x=1-\operatorname{cos}⁡\theta ,\,y=\operatorname{sin}⁡\theta +2,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "befcfe4a-abd3-5984-a1a3-1a1bf2b0cd72",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-2\\le x\\le 0,\\,-3\\le y\\le -1",
        ":db/id": 17592186400123
      },
      {
        ":answer/id": "9ee13255-e4e9-52e6-b06e-d0aeddb3bb38",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-1\\le x\\le 1,\\,1\\le y\\le 3",
        ":db/id": 17592186400124
      },
      {
        ":answer/id": "c3236814-4c23-5fc9-a82d-b9432370c830",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-1\\le x\\le 1,\\,-3\\le y\\le -1",
        ":db/id": 17592186400125
      },
      {
        ":answer/id": "bcd316cc-7219-5b56-b38c-fa0c32ea3d94",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "0\\le x\\le 2,\\,-2\\le y\\le 2",
        ":db/id": 17592186400126
      },
      {
        ":answer/id": "5fb2b3dc-0e10-5966-a703-a0088b75ec08",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "0\\le x\\le 2,\\,1\\le y\\le 3",
        ":db/id": 17592186400127
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "5fb2b3dc-0e10-5966-a703-a0088b75ec08",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "0\\le x\\le 2,\\,1\\le y\\le 3",
      ":db/id": 17592186400127
    },
    ":answer-field/id": "806b0a66-23a8-530b-9fd2-35a679c8dd3c",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186400122
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ 1 & \text{ }\ge -\operatorname{cos}⁡\theta \text{ }\ge -1 \\ -1 & \le -\operatorname{cos}⁡\theta \le 1 \\ 1-1 & \le 1-\operatorname{cos}⁡\theta \le 1+1 \\ 0 & \le x\le 2.\end{aligned}
$$

So, we can conclude that $0\le x\le 2.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -1+2 & \le \operatorname{sin}⁡\theta +2\le 1+2 \\ 1 & \le y\le 3.\end{aligned}
$$

So, we can conclude that $1\le y\le 3.$

Therefore, the ranges are $0\le x\le 2$ and $1\le y\le 3.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=1-\operatorname{cos}⁡\theta ,\,y=\operatorname{sin}⁡\theta +2,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $-1\le x\le 1,\,-3\le y\le -1$
- $-1\le x\le 1,\,1\le y\le 3$
- $-2\le x\le 0,\,-3\le y\le -1$
- $0\le x\le 2,\,1\le y\le 3$ (correct)
- $0\le x\le 2,\,-2\le y\le 2$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ 1 & \text{ }\ge -\operatorname{cos}⁡\theta \text{ }\ge -1 \\ -1 & \le -\operatorname{cos}⁡\theta \le 1 \\ 1-1 & \le 1-\operatorname{cos}⁡\theta \le 1+1 \\ 0 & \le x\le 2.\end{aligned}
$$

So, we can conclude that $0\le x\le 2.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -1+2 & \le \operatorname{sin}⁡\theta +2\le 1+2 \\ 1 & \le y\le 3.\end{aligned}
$$

So, we can conclude that $1\le y\le 3.$

Therefore, the ranges are $0\le x\le 2$ and $1\le y\le 3.$



### Generated variant — observed:q-123773

Given that a curve is defined parametrically as

$$
x=2-\operatorname{cos}⁡\theta ,\,y=\operatorname{sin}⁡\theta +1,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $1\le x\le 3,\,-1\le y\le 1$
- $-1\le x\le 1,\,0\le y\le 2$
- $-1\le x\le 1,\,-2\le y\le 0$
- $1\le x\le 3,\,0\le y\le 2$ (correct)
- $-3\le x\le -1,\,-2\le y\le 0$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ 1 & \text{ }\ge -\operatorname{cos}⁡\theta \text{ }\ge -1 \\ -1 & \le -\operatorname{cos}⁡\theta \le 1 \\ 2-1 & \le 2-\operatorname{cos}⁡\theta \le 2+1 \\ 1 & \le x\le 3.\end{aligned}
$$

So, we can conclude that $1\le x\le 3.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -1+1 & \le \operatorname{sin}⁡\theta +1\le 1+1 \\ 0 & \le y\le 2.\end{aligned}
$$

So, we can conclude that $0\le y\le 2.$

Therefore, the ranges are $1\le x\le 3$ and $0\le y\le 2.$



### Generated variant — authored:full-period

Given that a curve is defined parametrically as

$$
x=2-\operatorname{cos}⁡\theta ,\,y=\operatorname{sin}⁡\theta +1,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $\frac{3}{2}\le x\le \frac{5}{2},\,\frac{1}{2}\le y\le \frac{3}{2}$
- $-1\le x\le 1,\,-1\le y\le 1$
- $0\le x\le 4,\,-1\le y\le 3$
- $-3\le x\le -1,\,-2\le y\le 0$
- $1\le x\le 3,\,0\le y\le 2$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ 1 & \text{ }\ge -\operatorname{cos}⁡\theta \text{ }\ge -1 \\ -1 & \le -\operatorname{cos}⁡\theta \le 1 \\ 2-1 & \le 2-\operatorname{cos}⁡\theta \le 2+1 \\ 1 & \le x\le 3.\end{aligned}
$$

So, we can conclude that $1\le x\le 3.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -1+1 & \le \operatorname{sin}⁡\theta +1\le 1+1 \\ 0 & \le y\le 2.\end{aligned}
$$

So, we can conclude that $0\le y\le 2.$

Therefore, the ranges are $1\le x\le 3$ and $0\le y\le 2.$



## Original q-123775 (easy)



Given that a curve is defined parametrically as

$$
x=\frac{1}{2}\operatorname{cos}⁡\theta ,\,y=\operatorname{sin}⁡\theta +3,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$



Original fields/bank:

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "64998bfc-bfc7-5d3e-8ee6-300d3a38797d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-2\\le x\\le 2,\\,-4\\le y\\le -2",
        ":db/id": 17592186400130
      },
      {
        ":answer/id": "42492b12-0052-541d-8cee-a36023e92984",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-2\\le x\\le 2,\\,-3\\le y\\le 3",
        ":db/id": 17592186400131
      },
      {
        ":answer/id": "2c4ef62b-01d3-5f37-819a-bf2a72b19db1",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{1}{2}\\le x\\le \\frac{1}{2},\\,-3\\le y\\le 3",
        ":db/id": 17592186400132
      },
      {
        ":answer/id": "79eb9da7-f01c-5dfb-a236-47a585231977",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{1}{2}\\le x\\le \\frac{1}{2},\\,2\\le y\\le 4",
        ":db/id": 17592186400133
      },
      {
        ":answer/id": "617de8a7-03f5-5305-95c8-3f2f2a0cf8cd",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1\\le x\\le 3,\\,2\\le y\\le 4",
        ":db/id": 17592186400134
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "79eb9da7-f01c-5dfb-a236-47a585231977",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-\\frac{1}{2}\\le x\\le \\frac{1}{2},\\,2\\le y\\le 4",
      ":db/id": 17592186400133
    },
    ":answer-field/id": "ef6815f3-6a4d-5946-a00b-a698526a94b2",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186400129
  }
]



Original worked solution:

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -\frac{1}{2} & \le \frac{1}{2}\operatorname{cos}⁡\theta \le \frac{1}{2} \\ -\frac{1}{2} & \le x\le \frac{1}{2}.\end{aligned}
$$

So, we can conclude that $-\frac{1}{2}\le x\le \frac{1}{2}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -1+3 & \le \operatorname{sin}⁡\theta +3\le 1+3 \\ 2 & \le y\le 4.\end{aligned}
$$

So, we can conclude that $2\le y\le 4.$

Therefore, the ranges are $-\frac{1}{2}\le x\le \frac{1}{2}$ and $2\le y\le 4.$



### Source replay (generated at original parameters)

Given that a curve is defined parametrically as

$$
x=\frac{1}{2}\operatorname{cos}⁡\theta ,\,y=\operatorname{sin}⁡\theta +3,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $-\frac{1}{2}\le x\le \frac{1}{2},\,-3\le y\le 3$
- $-2\le x\le 2,\,-3\le y\le 3$
- $-2\le x\le 2,\,-4\le y\le -2$
- $1\le x\le 3,\,2\le y\le 4$
- $-\frac{1}{2}\le x\le \frac{1}{2},\,2\le y\le 4$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -\frac{1}{2} & \le \frac{1}{2}\operatorname{cos}⁡\theta \le \frac{1}{2} \\ -\frac{1}{2} & \le x\le \frac{1}{2}.\end{aligned}
$$

So, we can conclude that $-\frac{1}{2}\le x\le \frac{1}{2}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -1+3 & \le \operatorname{sin}⁡\theta +3\le 1+3 \\ 2 & \le y\le 4.\end{aligned}
$$

So, we can conclude that $2\le y\le 4.$

Therefore, the ranges are $-\frac{1}{2}\le x\le \frac{1}{2}$ and $2\le y\le 4.$



### Generated variant — observed:q-123775

Given that a curve is defined parametrically as

$$
x=\frac{2}{3}\operatorname{cos}⁡\theta ,\,y=\operatorname{sin}⁡\theta +1,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $-\frac{2}{3}\le x\le \frac{2}{3},\,0\le y\le 2$ (correct)
- $-\frac{3}{2}\le x\le \frac{3}{2},\,-1\le y\le 1$
- $-\frac{2}{3}\le x\le \frac{2}{3},\,-1\le y\le 1$
- $-1\le x\le 1,\,0\le y\le 2$
- $-\frac{3}{2}\le x\le \frac{3}{2},\,-2\le y\le 0$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -\frac{2}{3} & \le \frac{2}{3}\operatorname{cos}⁡\theta \le \frac{2}{3} \\ -\frac{2}{3} & \le x\le \frac{2}{3}.\end{aligned}
$$

So, we can conclude that $-\frac{2}{3}\le x\le \frac{2}{3}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -1+1 & \le \operatorname{sin}⁡\theta +1\le 1+1 \\ 0 & \le y\le 2.\end{aligned}
$$

So, we can conclude that $0\le y\le 2.$

Therefore, the ranges are $-\frac{2}{3}\le x\le \frac{2}{3}$ and $0\le y\le 2.$



### Generated variant — authored:full-period

Given that a curve is defined parametrically as

$$
x=\frac{2}{3}\operatorname{cos}⁡\theta ,\,y=\operatorname{sin}⁡\theta +1,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $-\frac{1}{3}\le x\le \frac{1}{3},\,\frac{1}{2}\le y\le \frac{3}{2}$
- $-\frac{2}{3}\le x\le \frac{2}{3},\,-1\le y\le 1$
- $-\frac{4}{3}\le x\le \frac{4}{3},\,-1\le y\le 3$
- $-\frac{2}{3}\le x\le \frac{2}{3},\,-2\le y\le 0$
- $-\frac{2}{3}\le x\le \frac{2}{3},\,0\le y\le 2$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -\frac{2}{3} & \le \frac{2}{3}\operatorname{cos}⁡\theta \le \frac{2}{3} \\ -\frac{2}{3} & \le x\le \frac{2}{3}.\end{aligned}
$$

So, we can conclude that $-\frac{2}{3}\le x\le \frac{2}{3}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -1+1 & \le \operatorname{sin}⁡\theta +1\le 1+1 \\ 0 & \le y\le 2.\end{aligned}
$$

So, we can conclude that $0\le y\le 2.$

Therefore, the ranges are $-\frac{2}{3}\le x\le \frac{2}{3}$ and $0\le y\le 2.$



## Generated easy example 1

Given that a curve is defined parametrically as

$$
x=2-\operatorname{cos}⁡\theta ,\,y=\operatorname{sin}⁡\theta +7,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $-3\le x\le -1,\,-8\le y\le -6$
- $0\le x\le 4,\,5\le y\le 9$
- $-1\le x\le 1,\,-1\le y\le 1$
- $1\le x\le 3,\,6\le y\le 8$ (correct)
- $\frac{3}{2}\le x\le \frac{5}{2},\,\frac{13}{2}\le y\le \frac{15}{2}$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ 1 & \text{ }\ge -\operatorname{cos}⁡\theta \text{ }\ge -1 \\ -1 & \le -\operatorname{cos}⁡\theta \le 1 \\ 2-1 & \le 2-\operatorname{cos}⁡\theta \le 2+1 \\ 1 & \le x\le 3.\end{aligned}
$$

So, we can conclude that $1\le x\le 3.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -1+7 & \le \operatorname{sin}⁡\theta +7\le 1+7 \\ 6 & \le y\le 8.\end{aligned}
$$

So, we can conclude that $6\le y\le 8.$

Therefore, the ranges are $1\le x\le 3$ and $6\le y\le 8.$



## Generated easy example 2

Given that a curve is defined parametrically as

$$
x=3\operatorname{cos}⁡\theta ,\,\,\,y=8\operatorname{sin}⁡\theta ,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $-6\le x\le 6,\,-16\le y\le 16$
- $-\frac{3}{2}\le x\le \frac{3}{2},\,-4\le y\le 4$
- $-8\le x\le 8,\,-3\le y\le 3$
- $0\le x\le 3,\,0\le y\le 8$
- $-3\le x\le 3,\,-8\le y\le 8$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ -3 & \le 3\operatorname{cos}⁡\theta \le 3 \\ -3 & \le x\le 3.\end{aligned}
$$

So, we can conclude that $-3\le x\le 3.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -8 & \le 8\operatorname{sin}⁡\theta \le 8 \\ -8 & \le y\le 8.\end{aligned}
$$

So, we can conclude that $-8\le y\le 8.$

Therefore, the ranges are $-3\le x\le 3$ and $-8\le y\le 8.$



## Generated moderate example 1

Given that a curve is defined parametrically as

$$
x=2-7\operatorname{cos}⁡\theta ,\,\,\,y=8\operatorname{sin}⁡\theta -7,\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

**selection**
- $-9\le x\le 5,\,-1\le y\le 15$
- $-12\le x\le 16,\,-23\le y\le 9$
- $-7\le x\le 7,\,-8\le y\le 8$
- $-5\le x\le 9,\,-15\le y\le 1$ (correct)
- $-\frac{3}{2}\le x\le \frac{11}{2},\,-11\le y\le -3$

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{cos}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}⁡\theta \le 1 \\ 7 & \text{ }\ge -7\operatorname{cos}⁡\theta \text{ }\ge -7 \\ -7 & \le -7\operatorname{cos}⁡\theta \le 7 \\ 2-7 & \le 2-7\operatorname{cos}⁡\theta \le 2+7 \\ -5 & \le x\le 9.\end{aligned}
$$

So, we can conclude that $-5\le x\le 9.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi ,$ we have $-1\le \operatorname{sin}⁡\theta \le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}⁡\theta \le 1 \\ -8 & \le 8\operatorname{sin}⁡\theta \le 8 \\ -8-7 & \le 8\operatorname{sin}⁡\theta -7\le 8-7 \\ -15 & \le y\le 1.\end{aligned}
$$

So, we can conclude that $-15\le y\le 1.$

Therefore, the ranges are $-5\le x\le 9$ and $-15\le y\le 1.$



## Generated moderate example 2

Given that a curve is defined parametrically as
$x = 8\cos θ - 4, y = 8\sin θ + 2, 0 \le θ < 2π$,
what are the ranges of $x$ and $y$?

**selection**
- $-20\le x\le 12,\,-14\le y\le 18$
- $-8\le x\le 0,\,-2\le y\le 6$
- $-4\le x\le 12,\,-10\le y\le 6$
- $-8\le x\le 8,\,-8\le y\le 8$
- $-12\le x\le 4,\,-6\le y\le 10$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi,$ we have $-1\le \operatorname{cos}\theta\le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}\theta \le 1 \\ -8 & \le 8\operatorname{cos}\theta \le 8 \\ -8-4 & \le 8\operatorname{cos}\theta -4\le 8-4 \\ -12 & \le x\le 4.\end{aligned}
$$

So, we can conclude that $-12\le x\le 4.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi,$ we have $-1\le \operatorname{sin}\theta\le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}\theta \le 1 \\ -8 & \le 8\operatorname{sin}\theta \le 8 \\ -8+2 & \le 8\operatorname{sin}\theta +2\le 8+2 \\ -6 & \le y\le 10.\end{aligned}
$$

So, we can conclude that $-6\le y\le 10.$



## Generated hard example 1

Given that a curve is defined parametrically as

$$
x=-\frac{3}{4}\operatorname{cos}\theta -\frac{5}{2},\,y=-\frac{1}{3}\operatorname{sin}\theta -\frac{5}{2},\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is {{field-1}}{{field-2}}$x\le ${{field-3}}.

The range of $y$ is {{field-4}}$\le y${{field-5}}{{field-6}}.

**field-1**
- $-\frac{13}{4}$ (correct)
**field-2**
- $\le $ (correct)
**field-3**
- $-\frac{7}{4}$ (correct)
**field-4**
- $-\frac{17}{6}$ (correct)
**field-5**
- $\le $ (correct)
**field-6**
- $-\frac{13}{6}$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi,$ we have $-1\le \operatorname{cos}\theta\le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}\theta \le 1 \\ \frac{3}{4} & \text{ }\ge -\frac{3}{4}\operatorname{cos}\theta \text{ }\ge -\frac{3}{4} \\ -\frac{3}{4} & \le -\frac{3}{4}\operatorname{cos}\theta \le \frac{3}{4} \\ -\frac{3}{4}-\frac{5}{2} & \le -\frac{3}{4}\operatorname{cos}\theta -\frac{5}{2}\le \frac{3}{4}-\frac{5}{2} \\ -\frac{13}{4} & \le x\le -\frac{7}{4}.\end{aligned}
$$

So, we can conclude that $-\frac{13}{4}\le x\le -\frac{7}{4}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi,$ we have $-1\le \operatorname{sin}\theta\le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}\theta \le 1 \\ \frac{1}{3} & \text{ }\ge -\frac{1}{3}\operatorname{sin}\theta \text{ }\ge -\frac{1}{3} \\ -\frac{1}{3} & \le -\frac{1}{3}\operatorname{sin}\theta \le \frac{1}{3} \\ -\frac{1}{3}-\frac{5}{2} & \le -\frac{1}{3}\operatorname{sin}\theta -\frac{5}{2}\le \frac{1}{3}-\frac{5}{2} \\ -\frac{17}{6} & \le y\le -\frac{13}{6}.\end{aligned}
$$

So, we can conclude that $-\frac{17}{6}\le y\le -\frac{13}{6}.$



## Generated hard example 2

Given that a curve is defined parametrically as

$$
x=-\frac{7}{4}\operatorname{cos}\theta -\frac{1}{4},\,y=-\frac{3}{4}\operatorname{sin}\theta +\frac{9}{4},\,0\le \theta <2\pi ,
$$

what are the ranges of $x$ and $y?$

The range of $x$ is {{field-1}}{{field-2}}$x\le ${{field-3}}.

The range of $y$ is {{field-4}}$\le y${{field-5}}{{field-6}}.

**field-1**
- $-2$ (correct)
**field-2**
- $\le $ (correct)
**field-3**
- $\frac{3}{2}$ (correct)
**field-4**
- $\frac{3}{2}$ (correct)
**field-5**
- $\le $ (correct)
**field-6**
- $3$ (correct)

**Worked solution**

Let's consider each variable in turn.

- To find the range of $x,$ notice that for $0\le \theta <2\pi,$ we have $-1\le \operatorname{cos}\theta\le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{cos}\theta \le 1 \\ \frac{7}{4} & \text{ }\ge -\frac{7}{4}\operatorname{cos}\theta \text{ }\ge -\frac{7}{4} \\ -\frac{7}{4} & \le -\frac{7}{4}\operatorname{cos}\theta \le \frac{7}{4} \\ -\frac{7}{4}-\frac{1}{4} & \le -\frac{7}{4}\operatorname{cos}\theta -\frac{1}{4}\le \frac{7}{4}-\frac{1}{4} \\ -2 & \le x\le \frac{3}{2}.\end{aligned}
$$

So, we can conclude that $-2\le x\le \frac{3}{2}.$

- To find the range of $y,$ notice that for $0\le \theta <2\pi,$ we have $-1\le \operatorname{sin}\theta\le 1.$ Consequently,

$$
\begin{aligned}-1 & \le \operatorname{sin}\theta \le 1 \\ \frac{3}{4} & \text{ }\ge -\frac{3}{4}\operatorname{sin}\theta \text{ }\ge -\frac{3}{4} \\ -\frac{3}{4} & \le -\frac{3}{4}\operatorname{sin}\theta \le \frac{3}{4} \\ -\frac{3}{4}+\frac{9}{4} & \le -\frac{3}{4}\operatorname{sin}\theta +\frac{9}{4}\le \frac{3}{4}+\frac{9}{4} \\ \frac{3}{2} & \le y\le 3.\end{aligned}
$$

So, we can conclude that $\frac{3}{2}\le y\le 3.$
