# Source and generated review

Raw immutable source and full mathematical component/bank inventory are in source.json and source-bank-extraction.json. Source fields absent in two records are explicitly authored combination blanks. Source scalar replay banks are opaque evidence profiles.


## Original q-6827

Observed difficulty: unrated

For the parametric curve
$x = t^{2} + t, y = t^{2} - t,-4 \le t \le 4$,
consider the following table of values:

| **$t$** | $-4$ | $-2$ | $-1$ | $0$ | $1$ | $3$ | $4$ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| $x$ | $12$ | $a$ | $0$ | $0$ | $2$ | $c$ | $20$ |
| $y$ | $20$ | $6$ | $2$ | $b$ | $0$ | $6$ | $12$ |

Find the value of $a + b + c$.


Raw solution:
not captured


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "c5c9c6f1-88a9-5814-8d7f-824388fe769d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-15",
        ":db/id": 17592186086269
      },
      {
        ":answer/id": "c95ef482-a715-5d27-8322-272d06aefa28",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-10",
        ":db/id": 17592186086270
      },
      {
        ":answer/id": "dd13ebf0-fcc4-5780-a2ef-c58a92669901",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "9",
        ":db/id": 17592186086271
      },
      {
        ":answer/id": "3ae5b9a5-e0be-5b47-b2de-3e04a707aebe",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "14",
        ":db/id": 17592186086272
      },
      {
        ":answer/id": "70b93ffd-0a6c-5e4b-a149-c7a58e10d173",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "12",
        ":db/id": 17592186086273
      }
    ],
    ":answer-field/id": "155c89c2-1972-5fdf-8d50-c32635afc935",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186086268
  }
]
```


## Original q-6834

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

For the parametric curve

$$
x={t}^{2}-4,\,\,\,y=\frac{5}{2}-\frac{t}{2},\,-1\le t\le 5,
$$

consider the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $a$ | $-4$ | $-3$ | $0$ | $5$ | $12$ | $21$ |
| $y$ | $3$ | $\frac{5}{2}$ | $b$ | $\frac{3}{2}$ | $1$ | $\frac{1}{2}$ | $c$ |

$$

$$

Find the value of $a-b+c.$


Raw solution:
- To find the value of $a,$ we substitute $t=-1$ into $x={t}^{2}-4.$ This gives

$$
a=(-1)^{2}-4=1-4=-3.
$$

- To find the value of $b,$ we substitute $t=1$ into $y=\frac{5}{2}-\frac{t}{2}.$ This gives

$$
b=\frac{5}{2}-\frac{1}{2}=\frac{4}{2}=2.
$$

- To find the value of $c,$ we substitute $t=5$ into $y=\frac{5}{2}-\frac{t}{2}.$ This gives

$$
c=\frac{5}{2}-\frac{5}{2}=0.
$$

Finally, we have

$$
a-b+c=-3-2+0=-5.
$$


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "3c987a4c-ef82-50f8-9c2f-24369b52299f",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-5",
        ":db/id": 17592186333562
      },
      {
        ":answer/id": "448c0861-60dc-5277-abf0-6324c4313b9c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-6",
        ":db/id": 17592186333623
      },
      {
        ":answer/id": "4ec62518-f2da-54a6-b78e-7803c2af25ea",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3",
        ":db/id": 17592186333712
      },
      {
        ":answer/id": "4f618bb1-1a30-5478-b04d-5d8c290174ad",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-2",
        ":db/id": 17592186333716
      },
      {
        ":answer/id": "cc14822b-2861-53db-8d57-7b85cd391a64",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "4",
        ":db/id": 17592186334768
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "3c987a4c-ef82-50f8-9c2f-24369b52299f",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-5",
      ":db/id": 17592186333562
    },
    ":answer-field/id": "e19de855-513e-569d-b86d-f599dde05f25",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186335632
  }
]
```


## Original q-123754

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

For the parametric curve

$$
x=t-4,\,\,\,y=1-2{t}^{2},\,0\le t\le 4,
$$

consider the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- |
| $x$ | $a$ | $-3$ | $-2$ | $-1$ | $0$ |
| $y$ | $1$ | $-1$ | $b$ | $c$ | $-31$ |

$$

$$

Find the value of $a+b+c.$


Raw solution:
- To find the value of $a,$ we substitute $t=0$ into $x=t-4.$ This gives

$$
a=0-4=-4.
$$

- To find the value of $b,$ we substitute $t=2$ into $y=1-2{t}^{2}.$ This gives

$$
b=1-2(2)^{2}=-7.
$$

- To find the value of $c,$ we substitute $t=3$ into $y=1-2{t}^{2}.$ This gives

$$
c=1-2(3)^{2}=-17
$$

Finally, we have

$$
a+b+c=-4+(-7)+(-17)=-28.
$$


Raw fields:
```json
[]
```


## Original q-326248

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

Consider the curve with parametric equations

$$
x={t}^{3}-\frac{1}{2}t,\,y=1-{t}^{2},\,1\le t\le 6.
$$

Fill in the blanks in the following table of values:

| **$t$** | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $\frac{1}{2}$ | {{field-1}} | $\frac{51}{2}$ | $62$ | $\frac{245}{2}$ | {{field-2}} |
| $y$ | $0$ | $-3$ | {{field-3}} | $-15$ | $-24$ | $-35$ |


Raw solution:
- To find the value of $x(2),$ we substitute $t=2$ into $x={t}^{3}-\frac{1}{2}t.$ This gives

$$
x(2)=(2)^{3}-\frac{1}{2}(2)=8-1=7.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=1-{t}^{2}.$ This gives

$$
y(3)=1-(3)^{2}=1-9=-8.
$$

- To find the value of $x(6),$ we substitute $t=6$ into $x={t}^{3}-\frac{1}{2}t.$ This gives

$$
x(6)=(6)^{3}-\frac{1}{2}(6)=216-3=213.
$$

Then the table is 

| **$t$** | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $\frac{1}{2}$ | $7$ | $\frac{51}{2}$ | $62$ | $\frac{245}{2}$ | $213$ |
| $y$ | $0$ | $-3$ | $-8$ | $-15$ | $-24$ | $-35$ |


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "d258e642-b9a6-5bf1-b482-5f152ab7aaad",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "7",
        ":db/id": 17592186232635
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "d258e642-b9a6-5bf1-b482-5f152ab7aaad",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "7",
      ":db/id": 17592186232635
    },
    ":answer-field/id": "52f71c9c-2f6b-5370-8a49-95e60baaf004",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232634
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "49847da4-c519-552f-850e-48e4275cefef",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "213",
        ":db/id": 17592186232637
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "49847da4-c519-552f-850e-48e4275cefef",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "213",
      ":db/id": 17592186232637
    },
    ":answer-field/id": "415b1ff5-fd3e-5864-b71e-dcccb0c3c658",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232636
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "b3cfa260-48a2-5cf6-94ef-725c7428f7f1",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-8",
        ":db/id": 17592186232639
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "b3cfa260-48a2-5cf6-94ef-725c7428f7f1",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-8",
      ":db/id": 17592186232639
    },
    ":answer-field/id": "858a5c87-649c-59d5-a39d-60ba696bb7d6",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232638
  }
]
```


## Original q-6832

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

For the parametric curve

$$
x=\operatorname{sin}⁡(\frac{\pi t}{2}),\,\,\,y=\operatorname{cos}⁡(\frac{\pi t}{3}),\,-3\le t\le 3,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $1$ | $0$ | $b$ | $0$ | $1$ | $0$ | $c$ |
| $y$ | $a$ | $-\frac{1}{2}$ | $\frac{1}{2}$ | $1$ | $\frac{1}{2}$ | $-\frac{1}{2}$ | $-1$ |

$$

$$

Find the value of $-a+b+c.$


Raw solution:
- To find the value of $a,$ we substitute $t=-3$ into $y=\operatorname{cos}⁡(\frac{\pi t}{3}).$ This gives

$$
a=\operatorname{cos}⁡(\frac{\pi (-3)}{3})=\operatorname{cos}⁡(-\pi )=-1.
$$

- To find the value of $b,$ we substitute $t=-1$ into $y=\operatorname{sin}⁡(\frac{\pi t}{2}).$ This gives

$$
b=\operatorname{sin}⁡(\frac{\pi (-1)}{2})=\operatorname{sin}⁡(-\frac{\pi }{2})=-1.
$$

- To find the value of $c,$ we substitute $t=3$ into $y=\operatorname{sin}⁡(\frac{\pi t}{2}).$ This gives

$$
c=\operatorname{sin}⁡(\frac{\pi (3)}{2})=\operatorname{sin}⁡(\frac{3\pi }{2})=-1.
$$

Finally, we have

$$
-a+b+c=-(-1)+(-1)+(-1)=-1.
$$


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "280e1cee-68f8-59f3-a023-f6dd1f086b41",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-2",
        ":db/id": 17592186333358
      },
      {
        ":answer/id": "c16fb7f6-a00e-595d-a28e-2f0a7397869c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "0",
        ":db/id": 17592186334666
      },
      {
        ":answer/id": "d02e3a07-a9eb-5ee2-9205-057f65384e6c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1",
        ":db/id": 17592186334807
      },
      {
        ":answer/id": "e4417143-3102-5cc2-b8d4-db87db4085b3",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-1",
        ":db/id": 17592186334978
      },
      {
        ":answer/id": "eacbc418-3efa-5b4c-a585-26704419f165",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3",
        ":db/id": 17592186335043
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "e4417143-3102-5cc2-b8d4-db87db4085b3",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-1",
      ":db/id": 17592186334978
    },
    ":answer-field/id": "0b5f293a-3b57-563b-b236-87b7649c6cbf",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186335256
  }
]
```


## Original q-69923

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

For the parametric curve

$$
x=-3t,\,\,\,y=2t,\,-5\le t\le 0,
$$

consider the following table of values:

| **$t$** | $-5$ | $-4$ | $-3$ | $-2$ | $-1$ | $0$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $15$ | $12$ | $9$ | $6$ | $3$ | $c$ |
| $y$ | $-10$ | $a$ | $-6$ | $b$ | $-2$ | $0$ |

$$

$$

Find the value of $a-b+c.$


Raw solution:
- To find the value of $a,$ we substitute $t=-4$ into $y=2t.$ This gives

$$
a=2(-4)=-8.
$$

- To find the value of $b,$ we substitute $t=-2$ into $y=2t.$ This gives

$$
b=2(-2)-4.
$$

- To find the value of $c,$ we substitute $t=0$ into $x=-3t.$ This gives

$$
c=-3(0)=0.
$$

Finally, we have

$$
a-b+c=-8-(-4)+0=-4.
$$


Raw fields:
```json
[]
```


## Original q-123753

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

For the parametric curve

$$
x=1-{t}^{2},\,\,\,y=3t+2,\,-2\le t\le 2,
$$

consider the following table of values:

| **$t$** | $-2$ | $-1$ | $0$ | $1$ | $2$ |
| --- | --- | --- | --- | --- | --- |
| $x$ | $-3$ | $a$ | $1$ | $0$ | $c$ |
| $y$ | $-4$ | $-1$ | $b$ | $5$ | $8$ |

$$

$$

Find the value of $a+b+c.$


Raw solution:
- To find the value of $a,$ we substitute $t=-1$ into $x=1-{t}^{2}.$ This gives

$$
a=1-(-1)^{2}=0.
$$

- To find the value of $b,$ we substitute $t=0$ into $y=3t+2.$ This gives

$$
b=3(0)+2=2.
$$

- To find the value of $c,$ we substitute $t=2$ into $x=1-{t}^{2}.$ This gives

$$
c=1-(2)^{2}=-3.
$$

Finally, we have

$$
a+b+c=0+2+(-3)=-1.
$$


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "3260f191-357e-5fd6-b3f9-51c178134db5",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-4",
        ":db/id": 17592186257221
      },
      {
        ":answer/id": "6d128ce0-efb8-56e1-8023-f299f3be850c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2",
        ":db/id": 17592186257742
      },
      {
        ":answer/id": "b18c0515-7610-54e6-b101-c84deb16e608",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-1",
        ":db/id": 17592186258326
      },
      {
        ":answer/id": "f075feb5-f3f8-5129-a941-46db050b2214",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "0",
        ":db/id": 17592186258873
      },
      {
        ":answer/id": "f211cf5f-df49-5a9e-9bde-8f90da57b9b2",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3",
        ":db/id": 17592186258888
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "b18c0515-7610-54e6-b101-c84deb16e608",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-1",
      ":db/id": 17592186258326
    },
    ":answer-field/id": "7b2b0b8a-76aa-5a6d-9974-c88122a91939",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186259240
  }
]
```


## Original q-123755

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

For the parametric curve

$$
x=4t,\,\,\,y=-{t}^{3},\,-3\le t\le 1,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ |
| --- | --- | --- | --- | --- | --- |
| $x$ | $-12$ | $-8$ | $a$ | $b$ | $4$ |
| $y$ | $27$ | $8$ | $1$ | $0$ | $c$ |

$$

$$

Find the value of $a+b+c.$


Raw solution:
- To find the value of $a,$ we substitute $t=-1$ into $x=4t.$ This gives

$$
a=4(-1)=-4.
$$

- To find the value of $b,$ we substitute $t=0$ into $x=4t.$ This gives

$$
b=4(0)=0.
$$

- To find the value of $c,$ we substitute $t=1$ into $y=-{t}^{3}.$ This gives

$$
c=-(1)^{3}=-1.
$$

Finally, we have

$$
a+b+c=-4+0+(-1)=-5.
$$


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "04f211ed-ddd7-5784-b0dc-35bcae2cefaa",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-5",
        ":db/id": 17592186256825
      },
      {
        ":answer/id": "2de8af09-195f-5b8c-bab0-ef80dd63e84b",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2",
        ":db/id": 17592186257188
      },
      {
        ":answer/id": "43228c86-2dad-5bf2-9955-abab71f85368",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-2",
        ":db/id": 17592186257373
      },
      {
        ":answer/id": "7b84009a-c3a3-57ac-ba2b-c913c4990eb7",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-3",
        ":db/id": 17592186257875
      },
      {
        ":answer/id": "8153caf4-964a-58e3-bef6-6c7992bf2466",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1",
        ":db/id": 17592186257931
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "04f211ed-ddd7-5784-b0dc-35bcae2cefaa",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-5",
      ":db/id": 17592186256825
    },
    ":answer-field/id": "7d2fb483-072d-5aac-a385-71833c68e6fd",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186259245
  }
]
```


## Original q-326242

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

Consider the curve with parametric equations

$$
x=\frac{3}{2}t+1,\,y=-\frac{5}{4}t+2,\,-1\le t\le 4.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | {{field-1}} | $1$ | $\frac{5}{2}$ | $4$ | {{field-2}} | $7$ |
| $y$ | {{field-3}} | $2$ | $\frac{3}{4}$ | $-\frac{1}{2}$ | $-\frac{7}{4}$ | $-3$ |


Raw solution:
- To find the value of $x(-1),$ we substitute $t=-1$ into $x=\frac{3}{2}t+1.$ This gives

$$
x(-1)=\frac{3}{2}(-1)+1=-\frac{3}{2}+\frac{2}{2}=-\frac{1}{2}.
$$

- To find the value of $y(-1),$ we substitute $t=-1$ into $y=-\frac{5}{4}t+2.$ This gives

$$
y(-1)=-\frac{5}{4}(-1)+2=\frac{5}{4}+\frac{8}{4}=\frac{13}{4}.
$$

- To find the value of $x(3),$ we substitute $t=3$ into $x=\frac{3}{2}t+1.$ This gives

$$
x(2)=\frac{3}{2}(3)+1=\frac{9}{2}+\frac{2}{2}=\frac{11}{2}.
$$

Then the table is 

 

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-\frac{1}{2}$ | $1$ | $\frac{5}{2}$ | $4$ | $\frac{11}{2}$ | $7$ |
| $y$ | $\frac{13}{4}$ | $2$ | $\frac{3}{4}$ | $-\frac{1}{2}$ | $-\frac{7}{4}$ | $-3$ |


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "bf11f1c2-7e84-52d0-82eb-f0bec75d951c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{1}{2}",
        ":db/id": 17592186300917
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "bf11f1c2-7e84-52d0-82eb-f0bec75d951c",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-\\frac{1}{2}",
      ":db/id": 17592186300917
    },
    ":answer-field/id": "909ca647-782d-5026-97c2-4f69d2dbc2de",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301688
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "ca352a99-e4be-5a50-b2d8-376ac2cbd696",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{13}{4}",
        ":db/id": 17592186300970
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "ca352a99-e4be-5a50-b2d8-376ac2cbd696",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{13}{4}",
      ":db/id": 17592186300970
    },
    ":answer-field/id": "be23546a-6789-50c1-b0de-9f43e3206e3b",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301847
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "315f9757-1b3f-500e-b71c-be24341277dc",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{11}{2}",
        ":db/id": 17592186300203
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "315f9757-1b3f-500e-b71c-be24341277dc",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{11}{2}",
      ":db/id": 17592186300203
    },
    ":answer-field/id": "cdc547cb-e485-57de-acc6-c64ddfd515ba",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301887
  }
]
```


## Original q-326246

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

Consider the curve with parametric equations

$$
x={t}^{3}-2t,\,y=-2t+\frac{3}{2},\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | $-1$ | {{field-1}} | $21$ | $56$ | {{field-2}} |
| $y$ | $\frac{3}{2}$ | $-\frac{1}{2}$ | $-\frac{5}{2}$ | {{field-3}} | $-\frac{13}{2}$ | $-\frac{17}{2}$ |


Raw solution:
- To find the value of $x(2),$ we substitute $t=2$ into $x={t}^{3}-2t.$ This gives

$$
x(2)=(2)^{3}-2(2)=8-4=4.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=-2t+\frac{3}{2}.$ This gives

$$
y(3)=-2(3)+\frac{3}{2}=-6+\frac{3}{2}=-\frac{12}{2}+\frac{3}{2}=-\frac{9}{2}.
$$

- To find the value of $x(5),$ we substitute $t=5$ into $x={t}^{3}-2t.$ This gives

$$
x(5)=(5)^{3}-2(5)=125-10=115.
$$

Then the table is 

 

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | $-1$ | $4$ | $21$ | $56$ | $115$ |
| $y$ | $\frac{3}{2}$ | $-\frac{1}{2}$ | $-\frac{5}{2}$ | $-\frac{9}{2}$ | $-\frac{13}{2}$ | $-\frac{17}{2}$ |


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "43263775-6a23-5d97-906a-a6f79d7a0456",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{9}{2}",
        ":db/id": 17592186300292
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "43263775-6a23-5d97-906a-a6f79d7a0456",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-\\frac{9}{2}",
      ":db/id": 17592186300292
    },
    ":answer-field/id": "32519836-bf08-5075-8849-e308dea3e240",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301387
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "2d011c6c-58a6-561f-ae10-6109748dcac4",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "115",
        ":db/id": 17592186300180
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "2d011c6c-58a6-561f-ae10-6109748dcac4",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "115",
      ":db/id": 17592186300180
    },
    ":answer-field/id": "57c14b01-f4ee-5c68-bf97-0b1dcdace2d4",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301512
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "1466bd40-3acf-591c-b003-9c0f787e6551",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "4",
        ":db/id": 17592186300044
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "1466bd40-3acf-591c-b003-9c0f787e6551",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "4",
      ":db/id": 17592186300044
    },
    ":answer-field/id": "aeaa33c7-8e94-592c-baee-0f58e084a228",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301794
  }
]
```


## Original q-326247

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

Consider the curve with parametric equations

$$
x={t}^{2}-2t+2,\,y=2{t}^{3}-3{t}^{2}+12,\,-1\le t\le 4.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $5$ | $2$ | {{field-1}} | $2$ | $5$ | $10$ |
| $y$ | $7$ | $12$ | $11$ | {{field-2}} | $39$ | {{field-3}} |


Raw solution:
- To find the value of $x(1),$ we substitute $t=1$ into $x={t}^{2}-2t+2.$ This gives

$$
x(1)=(1)^{2}-2(1)+2=1-2+2=1.
$$

- To find the value of $y(2),$ we substitute $t=2$ into $y=2{t}^{3}-3{t}^{2}+12.$ This gives

$$
y(2)=2(2)^{3}-3(2)^{2}+12=16-12+12=16.
$$

- To find the value of $y(4),$ we substitute $t=4$ into $y=2{t}^{3}-3{t}^{2}+12.$ This gives

$$
y(4)=2(4)^{3}-3(4)^{2}+12=128-48+12=92.
$$

Then the table is 

 

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $5$ | $2$ | $1$ | $2$ | $5$ | $10$ |
| $y$ | $7$ | $12$ | $11$ | $16$ | $39$ | $92$ |


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "d7d2c9b6-3f61-5b0c-8d40-7c8c3ad00a08",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "16",
        ":db/id": 17592186301036
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "d7d2c9b6-3f61-5b0c-8d40-7c8c3ad00a08",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "16",
      ":db/id": 17592186301036
    },
    ":answer-field/id": "475eb211-fdac-5ef1-a7b1-d7c876368b09",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301462
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "01f65e8b-4617-531e-b590-48e7cae4c340",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "92",
        ":db/id": 17592186299937
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "01f65e8b-4617-531e-b590-48e7cae4c340",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "92",
      ":db/id": 17592186299937
    },
    ":answer-field/id": "56a825ae-6d12-5ca9-bc21-522636b5fc85",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301508
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "d7bc2368-2d49-58ef-9f8a-804b443a1d10",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1",
        ":db/id": 17592186301035
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "d7bc2368-2d49-58ef-9f8a-804b443a1d10",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "1",
      ":db/id": 17592186301035
    },
    ":answer-field/id": "ceb7fcf1-d976-5665-b741-fc69d5d0b030",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301890
  }
]
```


## Original q-326250

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

Consider the curve with parametric equations

$$
x=\frac{1}{2}{t}^{3}-2,\,y=\frac{t-1}{t+1},\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-2$ | $-\frac{3}{2}$ | $2$ | $\frac{23}{2}$ | $30$ | {{field-1}} |
| $y$ | $-1$ | $0$ | {{field-2}} | $\frac{1}{2}$ | $\frac{3}{5}$ | {{field-3}} |


Raw solution:
- To find the value of $x(5),$ we substitute $t=5$ into $x=\frac{1}{2}{t}^{3}-2.$ This gives

$$
x(5)=\frac{1}{2}(5)^{3}-2=\frac{125}{2}-\frac{4}{2}=\frac{121}{2}.
$$

- To find the value of $y(2),$ we substitute $t=2$ into $y=\frac{t-1}{t+1}.$ This gives

$$
y(2)=\frac{2-1}{2+1}=\frac{1}{3}.
$$

- To find the value of $y(5),$ we substitute $t=5$ into $y=\frac{t-1}{t+1}.$ This gives

$$
y(0)=\frac{5-1}{5+1}=\frac{4}{6}=\frac{2}{3}.
$$

Then the table is 

 

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-2$ | $-\frac{3}{2}$ | $2$ | $\frac{23}{2}$ | $30$ | $\frac{121}{2}$ |
| $y$ | $-1$ | $0$ | $\frac{1}{3}$ | $\frac{1}{2}$ | $\frac{3}{5}$ | $\frac{2}{3}$ |


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "0b2f74f3-79cd-574f-9238-6fcdf77522bb",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{1}{3}",
        ":db/id": 17592186299987
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "0b2f74f3-79cd-574f-9238-6fcdf77522bb",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{1}{3}",
      ":db/id": 17592186299987
    },
    ":answer-field/id": "27b250f4-4f05-544b-8ebc-03ff71447626",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301351
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "bf5af01e-616b-5c46-a431-35738aad2c1d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{2}{3}",
        ":db/id": 17592186300920
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "bf5af01e-616b-5c46-a431-35738aad2c1d",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{2}{3}",
      ":db/id": 17592186300920
    },
    ":answer-field/id": "cf8b63ee-6e28-54cd-8eb2-72e238c6f9eb",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301894
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "521f8156-1852-5b70-b978-7d31f5f9d99c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{121}{2}",
        ":db/id": 17592186300388
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "521f8156-1852-5b70-b978-7d31f5f9d99c",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{121}{2}",
      ":db/id": 17592186300388
    },
    ":answer-field/id": "ec5a0f5f-9550-5151-a6a5-e2b91e74b30c",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301978
  }
]
```


## Original q-326251

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

Consider the curve with parametric equations

$$
x=\sqrt{\,t+4\,},\,y=\frac{3}{2}{t}^{2}-t,\,-3\le t\le 2.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | {{field-1}} | $\sqrt{2}$ | $\sqrt{3}$ | $2$ | $\sqrt{5}$ | $\sqrt{6}$ |
| $y$ | $\frac{33}{2}$ | $8$ | {{field-2}} | $0$ | $\frac{1}{2}$ | {{field-3}} |


Raw solution:
- To find the value of $x(-3),$ we substitute $t=-3$ into $x=\sqrt{\,t+4\,}.$ This gives

$$
x(-3)=\sqrt{-3+4}=\sqrt{1}=1.
$$

- To find the value of $y(-1),$ we substitute $t=-1$ into $y=\frac{3}{2}{t}^{2}-t.$ This gives

$$
y(-1)=\frac{3}{2}(-1)^{2}-(-1)=\frac{3}{2}+1=\frac{3}{2}+\frac{2}{2}=\frac{5}{2}.
$$

- To find the value of $y(2),$ we substitute $t=2$ into $y=\frac{3}{2}{t}^{2}-t.$ This gives

$$
y(2)=\frac{3}{2}(2)^{2}-(2)=6-2=4.
$$

Then the table is 

 

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $1$ | $\sqrt{2}$ | $\sqrt{3}$ | $2$ | $\sqrt{5}$ | $\sqrt{6}$ |
| $y$ | $\frac{33}{2}$ | $8$ | $\frac{5}{2}$ | $0$ | $\frac{1}{2}$ | $4$ |


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "dea4c418-a2a3-5eb1-914f-abfb1e44f530",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{5}{2}",
        ":db/id": 17592186301065
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "dea4c418-a2a3-5eb1-914f-abfb1e44f530",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{5}{2}",
      ":db/id": 17592186301065
    },
    ":answer-field/id": "0f6a1cf6-f1e9-5324-a0cd-8de8748825b8",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301277
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "42ca4294-13f5-564a-9c61-bfe51e2f5894",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "4",
        ":db/id": 17592186300288
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "42ca4294-13f5-564a-9c61-bfe51e2f5894",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "4",
      ":db/id": 17592186300288
    },
    ":answer-field/id": "af402e53-ece3-5170-871d-14635b65690e",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301800
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "3dbec592-362f-5cb8-838b-38b868c54f30",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1",
        ":db/id": 17592186300263
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "3dbec592-362f-5cb8-838b-38b868c54f30",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "1",
      ":db/id": 17592186300263
    },
    ":answer-field/id": "d785ba22-7770-5336-8681-5b6890e427ef",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301920
  }
]
```


## Original q-326255

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

Consider the curve with parametric equations

$$
x=cos\,(\frac{\pi t}{4}),\,y=sin\,(\frac{\pi t}{6}),\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $1$ | $\frac{\sqrt{2}}{2}$ | {{field-1}} | $-\frac{\sqrt{2}}{2}$ | $-1$ | $-\frac{\sqrt{2}}{2}$ |
| $y$ | $0$ | $\frac{1}{2}$ | $\frac{\sqrt{3}}{2}$ | {{field-2}} | {{field-3}} | $\frac{1}{2}$ |


Raw solution:
- To find the value of $x(2),$ we substitute $t=2$ into $x=cos\,(\frac{\pi t}{4}).$ This gives

$$
x(2)=cos\,(\frac{\pi (2)}{4})=cos\,(\frac{\pi }{2})=0.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=sin\,(\frac{\pi t}{6}).$ This gives

$$
y(3)=sin\,(\frac{\pi (3)}{6})=sin\,(\frac{\pi }{2})=1.
$$

- To find the value of $y(4),$ we substitute $t=4$ into $y=sin\,(\frac{\pi t}{6}).$ This gives

$$
y(1)=sin\,(\frac{\pi (4)}{6})=sin\,(\frac{2\pi }{3})=\frac{\sqrt{3}}{2}.
$$

Then the table is 

 

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $1$ | $\frac{\sqrt{2}}{2}$ | $0$ | $-\frac{\sqrt{2}}{2}$ | $-1$ | $-\frac{\sqrt{2}}{2}$ |
| $y$ | $0$ | $\frac{1}{2}$ | $\frac{\sqrt{3}}{2}$ | $1$ | $\frac{\sqrt{3}}{2}$ | $\frac{1}{2}$ |


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "503204c2-5202-5eb6-9c99-1d89a4256bc4",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1",
        ":db/id": 17592186300382
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "503204c2-5202-5eb6-9c99-1d89a4256bc4",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "1",
      ":db/id": 17592186300382
    },
    ":answer-field/id": "775ffea0-6f09-507b-ba4a-f5929a9c5ece",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301596
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "20d2ae08-199c-5474-adf2-cfd379ea5346",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{\\sqrt{3}}{2}",
        ":db/id": 17592186300115
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "20d2ae08-199c-5474-adf2-cfd379ea5346",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{\\sqrt{3}}{2}",
      ":db/id": 17592186300115
    },
    ":answer-field/id": "9fdb03f8-a8af-5dff-897a-1a48b028739f",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301740
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "8236cfbf-50c1-52a1-9051-6e2573a692b6",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "0",
        ":db/id": 17592186300611
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "8236cfbf-50c1-52a1-9051-6e2573a692b6",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "0",
      ":db/id": 17592186300611
    },
    ":answer-field/id": "be04d349-7486-598b-9dcd-fc83d123cadf",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301846
  }
]
```


## Original q-326256

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

Consider the curve with parametric equations

$$
x=cos\,(\frac{\pi t}{2}),\,y=tan\,(\frac{\pi t}{3}),\,-1\le t\le 4.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | {{field-1}} | $0$ | {{field-2}} | $0$ | $1$ |
| $y$ | $-\sqrt{3}$ | $0$ | {{field-3}} | $-\sqrt{3}$ | $0$ | $\sqrt{3}$ |


Raw solution:
- To find the value of $x(0),$ we substitute $t=0$ into $x=cos\,(\frac{\pi t}{2}).$ This gives

$$
x(0)=cos\,(\frac{\pi (0)}{2})=\operatorname{cos}⁡(0)=1.
$$

- To find the value of $y(1),$ we substitute $t=1$ into $y=tan\,(\frac{\pi t}{3}).$ This gives

$$
y(1)=tan\,(\frac{\pi (1)}{3})=tan\,(\frac{\pi }{3})=\sqrt{3}.
$$

- To find the value of $x(2),$ we substitute $t=2$ into $x=cos\,(\frac{\pi t}{2}).$ This gives

$$
x(2)=cos\,(\frac{\pi (2)}{2})=\operatorname{cos}⁡(\pi )=-1.
$$

Then the table is 

 

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | $1$ | $0$ | $-1$ | $0$ | $1$ |
| $y$ | $-\sqrt{3}$ | $0$ | $\sqrt{3}$ | $-\sqrt{3}$ | $0$ | $\sqrt{3}$ |


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "0cda53e7-8da8-5d86-a98c-5728719bc41b",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\sqrt{3}",
        ":db/id": 17592186300000
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "0cda53e7-8da8-5d86-a98c-5728719bc41b",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\sqrt{3}",
      ":db/id": 17592186300000
    },
    ":answer-field/id": "926f273e-d8b0-5e4d-9631-40e611c24ed3",
    ":answer-field/key": "field-3",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301693
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "25f796a4-f9bc-52c2-95c4-861c28462e0f",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-1",
        ":db/id": 17592186300143
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "25f796a4-f9bc-52c2-95c4-861c28462e0f",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-1",
      ":db/id": 17592186300143
    },
    ":answer-field/id": "d4c15bfd-ddd4-56df-9248-59fef4cfb8ff",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301912
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "011fae4e-c40e-5543-bf07-c0c1656584a7",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1",
        ":db/id": 17592186299934
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "011fae4e-c40e-5543-bf07-c0c1656584a7",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "1",
      ":db/id": 17592186299934
    },
    ":answer-field/id": "da7a0f49-5d74-598d-9cc7-a44f9d26dfa4",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186301928
  }
]
```


## Original q-6742

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

For the parametric curve

$$
x=t+1,\,\,\,y={t}^{2}-6,-3\le t\le 3,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ | $c$ |
| $y$ | $a$ | $-2$ | $-5$ | $b$ | $-5$ | $-2$ | $3$ |

$$

$$

Find the value of $a-b-c.$


Raw solution:
- To find the value of $a,$ we substitute $t=-3$ into $y={t}^{2}-6.$ This gives

$$
a=(-3)^{2}-6=9-6=3.
$$

- To find the value of $b,$ we substitute $t=0$ into $y={t}^{2}-6.$ This gives

$$
b={0}^{2}-6=0-6=-6.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=t+1.$ This gives

$$
c=3+1=4.
$$

Finally, we have

$$
a-b-c=3-(-6)-4=5.
$$


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "054e45cb-ef1a-592f-8ce5-2215be471cc4",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "7",
        ":db/id": 17592186333032
      },
      {
        ":answer/id": "79eda04b-781c-5fda-aa4a-bb2479352bdd",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3",
        ":db/id": 17592186334085
      },
      {
        ":answer/id": "9a6d0cbe-1f59-57f6-aefd-5d53e15a7b1d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-6",
        ":db/id": 17592186334353
      },
      {
        ":answer/id": "b7b9a71e-ffbd-5091-8899-773c38323464",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5",
        ":db/id": 17592186334599
      },
      {
        ":answer/id": "ecb2865c-3deb-55d1-a152-eed996480e2f",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-4",
        ":db/id": 17592186335064
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "b7b9a71e-ffbd-5091-8899-773c38323464",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "5",
      ":db/id": 17592186334599
    },
    ":answer-field/id": "fcd68d1f-2e2e-53b3-8c88-e40a6b095d8e",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186335680
  }
]
```


## Original q-6825

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

For the parametric curve

$$
x=3t-2,\,\,\,y=\frac{10}{{t}^{2}+1},\,-3\le t\le 3,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $a$ | $-8$ | $-5$ | $-2$ | $1$ | $4$ | $c$ |
| $y$ | $1$ | $b$ | $5$ | $10$ | $5$ | $2$ | $1$ |

$$

$$

Find the value of $a+b+c.$


Raw solution:
- To find the value of $a,$ we substitute $t=-3$ into $x=3t-2.$ This gives

$$
a=3(-3)-2=-9-2=-11.
$$

- To find the value of $b,$ we substitute $t=-2$ into $y=\frac{10}{{t}^{2}+1}.$ This gives

$$
b=\frac{10}{(-2)^{2}+1}=\frac{10}{5}=2.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=3t-2.$ This gives

$$
a=3(3)-2=9-2=7.
$$

Finally, we have

$$
a+b+c=-11+2+7=-2.
$$


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "06ea7064-8984-5ac6-91ea-ed8921bbc138",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3",
        ":db/id": 17592186333056
      },
      {
        ":answer/id": "827b89fe-a572-54cd-b9cb-dcc0569b217e",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-2",
        ":db/id": 17592186334153
      },
      {
        ":answer/id": "c8f91035-840a-59fe-a14a-8ded740896f0",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1",
        ":db/id": 17592186334736
      },
      {
        ":answer/id": "d3a7c0bf-869c-5788-8888-00b2ca3dcdac",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "0",
        ":db/id": 17592186334846
      },
      {
        ":answer/id": "ed2e747f-c905-58fc-9adb-fb9c26ba7608",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-1",
        ":db/id": 17592186335069
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "827b89fe-a572-54cd-b9cb-dcc0569b217e",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-2",
      ":db/id": 17592186334153
    },
    ":answer-field/id": "4a546347-737e-5d85-bf73-af24c4b5c1f5",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186335386
  }
]
```


## Original q-69922

Observed difficulty: {':db/ident': ':question.difficulty/easy'}

For the parametric curve

$$
x=2t+1,\,\,\,y=2t-1,\,0\le t\le 5,
$$

consider the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $1$ | $3$ | $b$ | $7$ | $9$ | $11$ |
| $y$ | $a$ | $1$ | $3$ | $5$ | $c$ | $9$ |

$$

$$

Find the value of $a-b-c.$


Raw solution:
- To find the value of $a,$ we substitute $t=0$ into $y=2t-1.$ This gives

$$
a=2(0)-1=0-1=-1.
$$

- To find the value of $b,$ we substitute $t=2$ into $x=2t+1.$ This gives

$$
b=2(2)+1=4+1=5.
$$

- To find the value of $c,$ we substitute $t=4$ into $y=2t-1.$ This gives

$$
c=2(4)-1=8-1=7.
$$

Finally, we have

$$
a-b-c=-1-5-7=-13.
$$


Raw fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "06475ed3-8f81-5f2a-92d7-37b61ba3d841",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-13",
        ":db/id": 17592186333047
      },
      {
        ":answer/id": "1675a734-ba42-53ad-bacc-d3d9a7ecfb02",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-10",
        ":db/id": 17592186333190
      },
      {
        ":answer/id": "379b5cc9-a398-5f20-b13a-5820843260de",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "15",
        ":db/id": 17592186333501
      },
      {
        ":answer/id": "4e027385-3e35-564e-88cf-8f5955ad0320",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "12",
        ":db/id": 17592186333708
      },
      {
        ":answer/id": "bbabf68e-a37c-54df-b8af-32120f8b5dfd",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "8",
        ":db/id": 17592186334625
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "06475ed3-8f81-5f2a-92d7-37b61ba3d841",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-13",
      ":db/id": 17592186333047
    },
    ":answer-field/id": "be306b92-cfe4-5ecc-9451-b14d1a1a3e42",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186335589
  }
]
```


## q-6827 replay

For the parametric curve
$x = t^{2} + t, y = t^{2} - t,-4 \le t \le 4$,
consider the following table of values:

| **$t$** | $-4$ | $-2$ | $-1$ | $0$ | $1$ | $3$ | $4$ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| $x$ | $12$ | $a$ | $0$ | $0$ | $2$ | $c$ | $20$ |
| $y$ | $20$ | $6$ | $2$ | $b$ | $0$ | $6$ | $12$ |

Find the value of $a + b + c$.

selection (review choices):

- A. $-15$
- B. $-10$
- C. $9$
- D. $14$ [correct]
- E. $12$

Worked solution:

- To find the value of $a,$ we substitute $t=-2$ into $x=t^{2} + t.$ This gives

$$
a=(-2)^{2} + (-2)=2.
$$

- To find the value of $b,$ we substitute $t=0$ into $y=t^{2} - t.$ This gives

$$
b=(0)^{2} - (0)=0.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=t^{2} + t.$ This gives

$$
c=(3)^{2} + (3)=12.
$$

Finally, we have

$$
a + b + c=2+0+12=14.
$$


## q-6827 generated scalar-replay variant k=-2

For the parametric curve
$x = -2\left(t^{2} + t\right), y = -2\left(t^{2} - t\right),-4 \le t \le 4$,
consider the following table of values:

| **$t$** | $-4$ | $-2$ | $-1$ | $0$ | $1$ | $3$ | $4$ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| $x$ | $-24$ | $a$ | $0$ | $0$ | $-4$ | $c$ | $-40$ |
| $y$ | $-40$ | $-12$ | $-4$ | $b$ | $0$ | $-12$ | $-24$ |

Find the value of $a + b + c$.

selection (review choices):

- A. $30$
- B. $20$
- C. $-18$
- D. $-28$ [correct]
- E. $-24$

Worked solution:

- To find the value of $a,$ we substitute $t=-2$ into $x=-2\left(t^{2} + t\right).$ This gives

$$
a=-2\left((-2)^{2} + (-2)\right)=-4.
$$

- To find the value of $b,$ we substitute $t=0$ into $y=-2\left(t^{2} - t\right).$ This gives

$$
b=-2\left((0)^{2} - (0)\right)=0.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=-2\left(t^{2} + t\right).$ This gives

$$
c=-2\left((3)^{2} + (3)\right)=-24.
$$

Finally, we have

$$
a + b + c=-2\left(2+0+12\right)=-28.
$$


## q-6827 generated scalar-replay variant k=2

For the parametric curve
$x = 2\left(t^{2} + t\right), y = 2\left(t^{2} - t\right),-4 \le t \le 4$,
consider the following table of values:

| **$t$** | $-4$ | $-2$ | $-1$ | $0$ | $1$ | $3$ | $4$ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| $x$ | $24$ | $a$ | $0$ | $0$ | $4$ | $c$ | $40$ |
| $y$ | $40$ | $12$ | $4$ | $b$ | $0$ | $12$ | $24$ |

Find the value of $a + b + c$.

selection (review choices):

- A. $-30$
- B. $-20$
- C. $18$
- D. $28$ [correct]
- E. $24$

Worked solution:

- To find the value of $a,$ we substitute $t=-2$ into $x=2\left(t^{2} + t\right).$ This gives

$$
a=2\left((-2)^{2} + (-2)\right)=4.
$$

- To find the value of $b,$ we substitute $t=0$ into $y=2\left(t^{2} - t\right).$ This gives

$$
b=2\left((0)^{2} - (0)\right)=0.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=2\left(t^{2} + t\right).$ This gives

$$
c=2\left((3)^{2} + (3)\right)=24.
$$

Finally, we have

$$
a + b + c=2\left(2+0+12\right)=28.
$$


## q-6834 replay

For the parametric curve

$$
x={t}^{2}-4,\,\,\,y=\frac{5}{2}-\frac{t}{2},\,-1\le t\le 5,
$$

consider the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $a$ | $-4$ | $-3$ | $0$ | $5$ | $12$ | $21$ |
| $y$ | $3$ | $\frac{5}{2}$ | $b$ | $\frac{3}{2}$ | $1$ | $\frac{1}{2}$ | $c$ |

$$

$$

Find the value of $a-b+c.$

selection (review choices):

- A. $-5$ [correct]
- B. $-6$
- C. $3$
- D. $-2$
- E. $4$

Worked solution:

- To find the value of $a,$ we substitute $t=-1$ into $x={t}^{2}-4.$ This gives

$$
a=(-1)^{2}-4=1-4=-3.
$$

- To find the value of $b,$ we substitute $t=1$ into $y=\frac{5}{2}-\frac{t}{2}.$ This gives

$$
b=\frac{5}{2}-\frac{1}{2}=\frac{4}{2}=2.
$$

- To find the value of $c,$ we substitute $t=5$ into $y=\frac{5}{2}-\frac{t}{2}.$ This gives

$$
c=\frac{5}{2}-\frac{5}{2}=0.
$$

Finally, we have

$$
a-b+c=-3-2+0=-5.
$$


## q-6834 generated scalar-replay variant k=-2

For the parametric curve

$$
x=-2\left({t}^{2}-4\right),\,\,\,y=-2\left(\frac{5}{2}-\frac{t}{2}\right),\,-1\le t\le 5,
$$

consider the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $a$ | $8$ | $6$ | $0$ | $-10$ | $-24$ | $-42$ |
| $y$ | $-6$ | $-5$ | $b$ | $-3$ | $-2$ | $-1$ | $c$ |

$$

$$

Find the value of $a-b+c.$

selection (review choices):

- A. $10$ [correct]
- B. $12$
- C. $-6$
- D. $4$
- E. $-8$

Worked solution:

- To find the value of $a,$ we substitute $t=-1$ into $x=-2\left({t}^{2}-4\right).$ This gives

$$
a=-2\left((-1)^{2}-4\right)=-2\left(1-4\right)=6.
$$

- To find the value of $b,$ we substitute $t=1$ into $y=-2\left(\frac{5}{2}-\frac{t}{2}\right).$ This gives

$$
b=-2\left(\frac{5}{2}-\frac{1}{2}\right)=-2\left(\frac{4}{2}\right)=-4.
$$

- To find the value of $c,$ we substitute $t=5$ into $y=-2\left(\frac{5}{2}-\frac{t}{2}\right).$ This gives

$$
c=-2\left(\frac{5}{2}-\frac{5}{2}\right)=0.
$$

Finally, we have

$$
a-b+c=-2\left(-3-2+0\right)=10.
$$


## q-6834 generated scalar-replay variant k=2

For the parametric curve

$$
x=2\left({t}^{2}-4\right),\,\,\,y=2\left(\frac{5}{2}-\frac{t}{2}\right),\,-1\le t\le 5,
$$

consider the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $a$ | $-8$ | $-6$ | $0$ | $10$ | $24$ | $42$ |
| $y$ | $6$ | $5$ | $b$ | $3$ | $2$ | $1$ | $c$ |

$$

$$

Find the value of $a-b+c.$

selection (review choices):

- A. $-10$ [correct]
- B. $-12$
- C. $6$
- D. $-4$
- E. $8$

Worked solution:

- To find the value of $a,$ we substitute $t=-1$ into $x=2\left({t}^{2}-4\right).$ This gives

$$
a=2\left((-1)^{2}-4\right)=2\left(1-4\right)=-6.
$$

- To find the value of $b,$ we substitute $t=1$ into $y=2\left(\frac{5}{2}-\frac{t}{2}\right).$ This gives

$$
b=2\left(\frac{5}{2}-\frac{1}{2}\right)=2\left(\frac{4}{2}\right)=4.
$$

- To find the value of $c,$ we substitute $t=5$ into $y=2\left(\frac{5}{2}-\frac{t}{2}\right).$ This gives

$$
c=2\left(\frac{5}{2}-\frac{5}{2}\right)=0.
$$

Finally, we have

$$
a-b+c=2\left(-3-2+0\right)=-10.
$$


## q-123754 replay

For the parametric curve

$$
x=t-4,\,\,\,y=1-2{t}^{2},\,0\le t\le 4,
$$

consider the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- |
| $x$ | $a$ | $-3$ | $-2$ | $-1$ | $0$ |
| $y$ | $1$ | $-1$ | $b$ | $c$ | $-31$ |

$$

$$

Find the value of $a+b+c.$

{{selection}}

selection: $-28$

Worked solution:

- To find the value of $a,$ we substitute $t=0$ into $x=t-4.$ This gives

$$
a=0-4=-4.
$$

- To find the value of $b,$ we substitute $t=2$ into $y=1-2{t}^{2}.$ This gives

$$
b=1-2(2)^{2}=-7.
$$

- To find the value of $c,$ we substitute $t=3$ into $y=1-2{t}^{2}.$ This gives

$$
c=1-2(3)^{2}=-17
$$

Finally, we have

$$
a+b+c=-4+(-7)+(-17)=-28.
$$


## q-123754 generated scalar-replay variant k=-2

For the parametric curve

$$
x=-2\left(t-4\right),\,\,\,y=-2\left(1-2{t}^{2}\right),\,0\le t\le 4,
$$

consider the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- |
| $x$ | $a$ | $6$ | $4$ | $2$ | $0$ |
| $y$ | $-2$ | $2$ | $b$ | $c$ | $62$ |

$$

$$

Find the value of $a+b+c.$

{{selection}}

selection: $56$

Worked solution:

- To find the value of $a,$ we substitute $t=0$ into $x=-2\left(t-4\right).$ This gives

$$
a=-2\left(0-4\right)=8.
$$

- To find the value of $b,$ we substitute $t=2$ into $y=-2\left(1-2{t}^{2}\right).$ This gives

$$
b=-2\left(1-2(2)^{2}\right)=14.
$$

- To find the value of $c,$ we substitute $t=3$ into $y=-2\left(1-2{t}^{2}\right).$ This gives

$$
c=-2\left(1-2(3)^{2}\right)=34
$$

Finally, we have

$$
a+b+c=-2\left(-4+(-7)+(-17)\right)=56.
$$


## q-123754 generated scalar-replay variant k=2

For the parametric curve

$$
x=2\left(t-4\right),\,\,\,y=2\left(1-2{t}^{2}\right),\,0\le t\le 4,
$$

consider the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- |
| $x$ | $a$ | $-6$ | $-4$ | $-2$ | $0$ |
| $y$ | $2$ | $-2$ | $b$ | $c$ | $-62$ |

$$

$$

Find the value of $a+b+c.$

{{selection}}

selection: $-56$

Worked solution:

- To find the value of $a,$ we substitute $t=0$ into $x=2\left(t-4\right).$ This gives

$$
a=2\left(0-4\right)=-8.
$$

- To find the value of $b,$ we substitute $t=2$ into $y=2\left(1-2{t}^{2}\right).$ This gives

$$
b=2\left(1-2(2)^{2}\right)=-14.
$$

- To find the value of $c,$ we substitute $t=3$ into $y=2\left(1-2{t}^{2}\right).$ This gives

$$
c=2\left(1-2(3)^{2}\right)=-34
$$

Finally, we have

$$
a+b+c=2\left(-4+(-7)+(-17)\right)=-56.
$$


## q-326248 replay

Consider the curve with parametric equations

$$
x={t}^{3}-\frac{1}{2}t,\,y=1-{t}^{2},\,1\le t\le 6.
$$

Fill in the blanks in the following table of values:

| **$t$** | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $\frac{1}{2}$ | {{field-1}} | $\frac{51}{2}$ | $62$ | $\frac{245}{2}$ | {{field-2}} |
| $y$ | $0$ | $-3$ | {{field-3}} | $-15$ | $-24$ | $-35$ |

field-1: $7$

field-2: $213$

field-3: $-8$

Worked solution:

- To find the value of $x(2),$ we substitute $t=2$ into $x={t}^{3}-\frac{1}{2}t.$ This gives

$$
x(2)=(2)^{3}-\frac{1}{2}(2)=8-1=7.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=1-{t}^{2}.$ This gives

$$
y(3)=1-(3)^{2}=1-9=-8.
$$

- To find the value of $x(6),$ we substitute $t=6$ into $x={t}^{3}-\frac{1}{2}t.$ This gives

$$
x(6)=(6)^{3}-\frac{1}{2}(6)=216-3=213.
$$

Then the table is 

| **$t$** | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $\frac{1}{2}$ | $7$ | $\frac{51}{2}$ | $62$ | $\frac{245}{2}$ | $213$ |
| $y$ | $0$ | $-3$ | $-8$ | $-15$ | $-24$ | $-35$ |


## q-326248 generated scalar-replay variant k=-2

Consider the curve with parametric equations

$$
x=-2\left({t}^{3}-\frac{1}{2}t\right),\,y=-2\left(1-{t}^{2}\right),\,1\le t\le 6.
$$

Fill in the blanks in the following table of values:

| **$t$** | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-1$ | {{field-1}} | $-51$ | $-124$ | $-245$ | {{field-2}} |
| $y$ | $0$ | $6$ | {{field-3}} | $30$ | $48$ | $70$ |

field-1: $-14$

field-2: $-426$

field-3: $16$

Worked solution:

- To find the value of $x(2),$ we substitute $t=2$ into $x=-2\left({t}^{3}-\frac{1}{2}t\right).$ This gives

$$
x(2)=-2\left((2)^{3}-\frac{1}{2}(2)\right)=-2\left(8-1\right)=-14.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=-2\left(1-{t}^{2}\right).$ This gives

$$
y(3)=-2\left(1-(3)^{2}\right)=-2\left(1-9\right)=16.
$$

- To find the value of $x(6),$ we substitute $t=6$ into $x=-2\left({t}^{3}-\frac{1}{2}t\right).$ This gives

$$
x(6)=-2\left((6)^{3}-\frac{1}{2}(6)\right)=-2\left(216-3\right)=-426.
$$

Then the table is 

| **$t$** | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-1$ | $-14$ | $-51$ | $-124$ | $-245$ | $-426$ |
| $y$ | $0$ | $6$ | $16$ | $30$ | $48$ | $70$ |


## q-326248 generated scalar-replay variant k=2

Consider the curve with parametric equations

$$
x=2\left({t}^{3}-\frac{1}{2}t\right),\,y=2\left(1-{t}^{2}\right),\,1\le t\le 6.
$$

Fill in the blanks in the following table of values:

| **$t$** | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $1$ | {{field-1}} | $51$ | $124$ | $245$ | {{field-2}} |
| $y$ | $0$ | $-6$ | {{field-3}} | $-30$ | $-48$ | $-70$ |

field-1: $14$

field-2: $426$

field-3: $-16$

Worked solution:

- To find the value of $x(2),$ we substitute $t=2$ into $x=2\left({t}^{3}-\frac{1}{2}t\right).$ This gives

$$
x(2)=2\left((2)^{3}-\frac{1}{2}(2)\right)=2\left(8-1\right)=14.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=2\left(1-{t}^{2}\right).$ This gives

$$
y(3)=2\left(1-(3)^{2}\right)=2\left(1-9\right)=-16.
$$

- To find the value of $x(6),$ we substitute $t=6$ into $x=2\left({t}^{3}-\frac{1}{2}t\right).$ This gives

$$
x(6)=2\left((6)^{3}-\frac{1}{2}(6)\right)=2\left(216-3\right)=426.
$$

Then the table is 

| **$t$** | $1$ | $2$ | $3$ | $4$ | $5$ | $6$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $1$ | $14$ | $51$ | $124$ | $245$ | $426$ |
| $y$ | $0$ | $-6$ | $-16$ | $-30$ | $-48$ | $-70$ |


## q-6832 replay

For the parametric curve

$$
x=\operatorname{sin}⁡(\frac{\pi t}{2}),\,\,\,y=\operatorname{cos}⁡(\frac{\pi t}{3}),\,-3\le t\le 3,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $1$ | $0$ | $b$ | $0$ | $1$ | $0$ | $c$ |
| $y$ | $a$ | $-\frac{1}{2}$ | $\frac{1}{2}$ | $1$ | $\frac{1}{2}$ | $-\frac{1}{2}$ | $-1$ |

$$

$$

Find the value of $-a+b+c.$

selection (review choices):

- A. $-2$
- B. $0$
- C. $1$
- D. $-1$ [correct]
- E. $3$

Worked solution:

- To find the value of $a,$ we substitute $t=-3$ into $y=\operatorname{cos}⁡(\frac{\pi t}{3}).$ This gives

$$
a=\operatorname{cos}⁡(\frac{\pi (-3)}{3})=\operatorname{cos}⁡(-\pi )=-1.
$$

- To find the value of $b,$ we substitute $t=-1$ into $x=\operatorname{sin}⁡(\frac{\pi t}{2}).$ This gives

$$
b=\operatorname{sin}⁡(\frac{\pi (-1)}{2})=\operatorname{sin}⁡(-\frac{\pi }{2})=-1.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=\operatorname{sin}⁡(\frac{\pi t}{2}).$ This gives

$$
c=\operatorname{sin}⁡(\frac{\pi (3)}{2})=\operatorname{sin}⁡(\frac{3\pi }{2})=-1.
$$

Finally, we have

$$
-a+b+c=-(-1)+(-1)+(-1)=-1.
$$


## q-6832 generated scalar-replay variant k=-2

For the parametric curve

$$
x=-2\left(\operatorname{sin}⁡(\frac{\pi t}{2})\right),\,\,\,y=-2\left(\operatorname{cos}⁡(\frac{\pi t}{3})\right),\,-3\le t\le 3,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-2$ | $0$ | $b$ | $0$ | $-2$ | $0$ | $c$ |
| $y$ | $a$ | $1$ | $-1$ | $-2$ | $-1$ | $1$ | $2$ |

$$

$$

Find the value of $-a+b+c.$

selection (review choices):

- A. $4$
- B. $0$
- C. $-2$
- D. $2$ [correct]
- E. $-6$

Worked solution:

- To find the value of $a,$ we substitute $t=-3$ into $y=-2\left(\operatorname{cos}⁡(\frac{\pi t}{3})\right).$ This gives

$$
a=-2\left(\operatorname{cos}⁡(\frac{\pi (-3)}{3})\right)=-2\left(\operatorname{cos}⁡(-\pi )\right)=2.
$$

- To find the value of $b,$ we substitute $t=-1$ into $x=-2\left(\operatorname{sin}⁡(\frac{\pi t}{2})\right).$ This gives

$$
b=-2\left(\operatorname{sin}⁡(\frac{\pi (-1)}{2})\right)=-2\left(\operatorname{sin}⁡(-\frac{\pi }{2})\right)=2.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=-2\left(\operatorname{sin}⁡(\frac{\pi t}{2})\right).$ This gives

$$
c=-2\left(\operatorname{sin}⁡(\frac{\pi (3)}{2})\right)=-2\left(\operatorname{sin}⁡(\frac{3\pi }{2})\right)=2.
$$

Finally, we have

$$
-a+b+c=-2\left(-(-1)+(-1)+(-1)\right)=2.
$$


## q-6832 generated scalar-replay variant k=2

For the parametric curve

$$
x=2\left(\operatorname{sin}⁡(\frac{\pi t}{2})\right),\,\,\,y=2\left(\operatorname{cos}⁡(\frac{\pi t}{3})\right),\,-3\le t\le 3,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $2$ | $0$ | $b$ | $0$ | $2$ | $0$ | $c$ |
| $y$ | $a$ | $-1$ | $1$ | $2$ | $1$ | $-1$ | $-2$ |

$$

$$

Find the value of $-a+b+c.$

selection (review choices):

- A. $-4$
- B. $0$
- C. $2$
- D. $-2$ [correct]
- E. $6$

Worked solution:

- To find the value of $a,$ we substitute $t=-3$ into $y=2\left(\operatorname{cos}⁡(\frac{\pi t}{3})\right).$ This gives

$$
a=2\left(\operatorname{cos}⁡(\frac{\pi (-3)}{3})\right)=2\left(\operatorname{cos}⁡(-\pi )\right)=-2.
$$

- To find the value of $b,$ we substitute $t=-1$ into $x=2\left(\operatorname{sin}⁡(\frac{\pi t}{2})\right).$ This gives

$$
b=2\left(\operatorname{sin}⁡(\frac{\pi (-1)}{2})\right)=2\left(\operatorname{sin}⁡(-\frac{\pi }{2})\right)=-2.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=2\left(\operatorname{sin}⁡(\frac{\pi t}{2})\right).$ This gives

$$
c=2\left(\operatorname{sin}⁡(\frac{\pi (3)}{2})\right)=2\left(\operatorname{sin}⁡(\frac{3\pi }{2})\right)=-2.
$$

Finally, we have

$$
-a+b+c=2\left(-(-1)+(-1)+(-1)\right)=-2.
$$


## q-69923 replay

For the parametric curve

$$
x=-3t,\,\,\,y=2t,\,-5\le t\le 0,
$$

consider the following table of values:

| **$t$** | $-5$ | $-4$ | $-3$ | $-2$ | $-1$ | $0$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $15$ | $12$ | $9$ | $6$ | $3$ | $c$ |
| $y$ | $-10$ | $a$ | $-6$ | $b$ | $-2$ | $0$ |

$$

$$

Find the value of $a-b+c.$

{{selection}}

selection: $-4$

Worked solution:

- To find the value of $a,$ we substitute $t=-4$ into $y=2t.$ This gives

$$
a=2(-4)=-8.
$$

- To find the value of $b,$ we substitute $t=-2$ into $y=2t.$ This gives

$$
b=2(-2)=-4.
$$

- To find the value of $c,$ we substitute $t=0$ into $x=-3t.$ This gives

$$
c=-3(0)=0.
$$

Finally, we have

$$
a-b+c=-8-(-4)+0=-4.
$$


## q-69923 generated scalar-replay variant k=-2

For the parametric curve

$$
x=-2\left(-3t\right),\,\,\,y=-2\left(2t\right),\,-5\le t\le 0,
$$

consider the following table of values:

| **$t$** | $-5$ | $-4$ | $-3$ | $-2$ | $-1$ | $0$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-30$ | $-24$ | $-18$ | $-12$ | $-6$ | $c$ |
| $y$ | $20$ | $a$ | $12$ | $b$ | $4$ | $0$ |

$$

$$

Find the value of $a-b+c.$

{{selection}}

selection: $8$

Worked solution:

- To find the value of $a,$ we substitute $t=-4$ into $y=-2\left(2t\right).$ This gives

$$
a=-2\left(2(-4)\right)=16.
$$

- To find the value of $b,$ we substitute $t=-2$ into $y=-2\left(2t\right).$ This gives

$$
b=-2\left(2(-2)\right)=8.
$$

- To find the value of $c,$ we substitute $t=0$ into $x=-2\left(-3t\right).$ This gives

$$
c=-2\left(-3(0)\right)=0.
$$

Finally, we have

$$
a-b+c=-2\left(-8-(-4)+0\right)=8.
$$


## q-69923 generated scalar-replay variant k=2

For the parametric curve

$$
x=2\left(-3t\right),\,\,\,y=2\left(2t\right),\,-5\le t\le 0,
$$

consider the following table of values:

| **$t$** | $-5$ | $-4$ | $-3$ | $-2$ | $-1$ | $0$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $30$ | $24$ | $18$ | $12$ | $6$ | $c$ |
| $y$ | $-20$ | $a$ | $-12$ | $b$ | $-4$ | $0$ |

$$

$$

Find the value of $a-b+c.$

{{selection}}

selection: $-8$

Worked solution:

- To find the value of $a,$ we substitute $t=-4$ into $y=2\left(2t\right).$ This gives

$$
a=2\left(2(-4)\right)=-16.
$$

- To find the value of $b,$ we substitute $t=-2$ into $y=2\left(2t\right).$ This gives

$$
b=2\left(2(-2)\right)=-8.
$$

- To find the value of $c,$ we substitute $t=0$ into $x=2\left(-3t\right).$ This gives

$$
c=2\left(-3(0)\right)=0.
$$

Finally, we have

$$
a-b+c=2\left(-8-(-4)+0\right)=-8.
$$


## q-123753 replay

For the parametric curve

$$
x=1-{t}^{2},\,\,\,y=3t+2,\,-2\le t\le 2,
$$

consider the following table of values:

| **$t$** | $-2$ | $-1$ | $0$ | $1$ | $2$ |
| --- | --- | --- | --- | --- | --- |
| $x$ | $-3$ | $a$ | $1$ | $0$ | $c$ |
| $y$ | $-4$ | $-1$ | $b$ | $5$ | $8$ |

$$

$$

Find the value of $a+b+c.$

selection (review choices):

- A. $-4$
- B. $2$
- C. $-1$ [correct]
- D. $0$
- E. $3$

Worked solution:

- To find the value of $a,$ we substitute $t=-1$ into $x=1-{t}^{2}.$ This gives

$$
a=1-(-1)^{2}=0.
$$

- To find the value of $b,$ we substitute $t=0$ into $y=3t+2.$ This gives

$$
b=3(0)+2=2.
$$

- To find the value of $c,$ we substitute $t=2$ into $x=1-{t}^{2}.$ This gives

$$
c=1-(2)^{2}=-3.
$$

Finally, we have

$$
a+b+c=0+2+(-3)=-1.
$$


## q-123753 generated scalar-replay variant k=-2

For the parametric curve

$$
x=-2\left(1-{t}^{2}\right),\,\,\,y=-2\left(3t+2\right),\,-2\le t\le 2,
$$

consider the following table of values:

| **$t$** | $-2$ | $-1$ | $0$ | $1$ | $2$ |
| --- | --- | --- | --- | --- | --- |
| $x$ | $6$ | $a$ | $-2$ | $0$ | $c$ |
| $y$ | $8$ | $2$ | $b$ | $-10$ | $-16$ |

$$

$$

Find the value of $a+b+c.$

selection (review choices):

- A. $8$
- B. $-4$
- C. $2$ [correct]
- D. $0$
- E. $-6$

Worked solution:

- To find the value of $a,$ we substitute $t=-1$ into $x=-2\left(1-{t}^{2}\right).$ This gives

$$
a=-2\left(1-(-1)^{2}\right)=0.
$$

- To find the value of $b,$ we substitute $t=0$ into $y=-2\left(3t+2\right).$ This gives

$$
b=-2\left(3(0)+2\right)=-4.
$$

- To find the value of $c,$ we substitute $t=2$ into $x=-2\left(1-{t}^{2}\right).$ This gives

$$
c=-2\left(1-(2)^{2}\right)=6.
$$

Finally, we have

$$
a+b+c=-2\left(0+2+(-3)\right)=2.
$$


## q-123753 generated scalar-replay variant k=2

For the parametric curve

$$
x=2\left(1-{t}^{2}\right),\,\,\,y=2\left(3t+2\right),\,-2\le t\le 2,
$$

consider the following table of values:

| **$t$** | $-2$ | $-1$ | $0$ | $1$ | $2$ |
| --- | --- | --- | --- | --- | --- |
| $x$ | $-6$ | $a$ | $2$ | $0$ | $c$ |
| $y$ | $-8$ | $-2$ | $b$ | $10$ | $16$ |

$$

$$

Find the value of $a+b+c.$

selection (review choices):

- A. $-8$
- B. $4$
- C. $-2$ [correct]
- D. $0$
- E. $6$

Worked solution:

- To find the value of $a,$ we substitute $t=-1$ into $x=2\left(1-{t}^{2}\right).$ This gives

$$
a=2\left(1-(-1)^{2}\right)=0.
$$

- To find the value of $b,$ we substitute $t=0$ into $y=2\left(3t+2\right).$ This gives

$$
b=2\left(3(0)+2\right)=4.
$$

- To find the value of $c,$ we substitute $t=2$ into $x=2\left(1-{t}^{2}\right).$ This gives

$$
c=2\left(1-(2)^{2}\right)=-6.
$$

Finally, we have

$$
a+b+c=2\left(0+2+(-3)\right)=-2.
$$


## q-123755 replay

For the parametric curve

$$
x=4t,\,\,\,y=-{t}^{3},\,-3\le t\le 1,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ |
| --- | --- | --- | --- | --- | --- |
| $x$ | $-12$ | $-8$ | $a$ | $b$ | $4$ |
| $y$ | $27$ | $8$ | $1$ | $0$ | $c$ |

$$

$$

Find the value of $a+b+c.$

selection (review choices):

- A. $-5$ [correct]
- B. $2$
- C. $-2$
- D. $-3$
- E. $1$

Worked solution:

- To find the value of $a,$ we substitute $t=-1$ into $x=4t.$ This gives

$$
a=4(-1)=-4.
$$

- To find the value of $b,$ we substitute $t=0$ into $x=4t.$ This gives

$$
b=4(0)=0.
$$

- To find the value of $c,$ we substitute $t=1$ into $y=-{t}^{3}.$ This gives

$$
c=-(1)^{3}=-1.
$$

Finally, we have

$$
a+b+c=-4+0+(-1)=-5.
$$


## q-123755 generated scalar-replay variant k=-2

For the parametric curve

$$
x=-2\left(4t\right),\,\,\,y=-2\left(-{t}^{3}\right),\,-3\le t\le 1,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ |
| --- | --- | --- | --- | --- | --- |
| $x$ | $24$ | $16$ | $a$ | $b$ | $-8$ |
| $y$ | $-54$ | $-16$ | $-2$ | $0$ | $c$ |

$$

$$

Find the value of $a+b+c.$

selection (review choices):

- A. $10$ [correct]
- B. $-4$
- C. $4$
- D. $6$
- E. $-2$

Worked solution:

- To find the value of $a,$ we substitute $t=-1$ into $x=-2\left(4t\right).$ This gives

$$
a=-2\left(4(-1)\right)=8.
$$

- To find the value of $b,$ we substitute $t=0$ into $x=-2\left(4t\right).$ This gives

$$
b=-2\left(4(0)\right)=0.
$$

- To find the value of $c,$ we substitute $t=1$ into $y=-2\left(-{t}^{3}\right).$ This gives

$$
c=-2\left(-(1)^{3}\right)=2.
$$

Finally, we have

$$
a+b+c=-2\left(-4+0+(-1)\right)=10.
$$


## q-123755 generated scalar-replay variant k=2

For the parametric curve

$$
x=2\left(4t\right),\,\,\,y=2\left(-{t}^{3}\right),\,-3\le t\le 1,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ |
| --- | --- | --- | --- | --- | --- |
| $x$ | $-24$ | $-16$ | $a$ | $b$ | $8$ |
| $y$ | $54$ | $16$ | $2$ | $0$ | $c$ |

$$

$$

Find the value of $a+b+c.$

selection (review choices):

- A. $-10$ [correct]
- B. $4$
- C. $-4$
- D. $-6$
- E. $2$

Worked solution:

- To find the value of $a,$ we substitute $t=-1$ into $x=2\left(4t\right).$ This gives

$$
a=2\left(4(-1)\right)=-8.
$$

- To find the value of $b,$ we substitute $t=0$ into $x=2\left(4t\right).$ This gives

$$
b=2\left(4(0)\right)=0.
$$

- To find the value of $c,$ we substitute $t=1$ into $y=2\left(-{t}^{3}\right).$ This gives

$$
c=2\left(-(1)^{3}\right)=-2.
$$

Finally, we have

$$
a+b+c=2\left(-4+0+(-1)\right)=-10.
$$


## q-326242 replay

Consider the curve with parametric equations

$$
x=\frac{3}{2}t+1,\,y=-\frac{5}{4}t+2,\,-1\le t\le 4.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | {{field-1}} | $1$ | $\frac{5}{2}$ | $4$ | {{field-2}} | $7$ |
| $y$ | {{field-3}} | $2$ | $\frac{3}{4}$ | $-\frac{1}{2}$ | $-\frac{7}{4}$ | $-3$ |

field-1: $- \frac{1}{2}$

field-2: $\frac{11}{2}$

field-3: $\frac{13}{4}$

Worked solution:

- To find the value of $x(-1),$ we substitute $t=-1$ into $x=\frac{3}{2}t+1.$ This gives

$$
x(-1)=\frac{3}{2}(-1)+1=-\frac{3}{2}+\frac{2}{2}=-\frac{1}{2}.
$$

- To find the value of $y(-1),$ we substitute $t=-1$ into $y=-\frac{5}{4}t+2.$ This gives

$$
y(-1)=-\frac{5}{4}(-1)+2=\frac{5}{4}+\frac{8}{4}=\frac{13}{4}.
$$

- To find the value of $x(3),$ we substitute $t=3$ into $x=\frac{3}{2}t+1.$ This gives

$$
x(3)=\frac{3}{2}(3)+1=\frac{9}{2}+\frac{2}{2}=\frac{11}{2}.
$$

Then the table is 

 

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-\frac{1}{2}$ | $1$ | $\frac{5}{2}$ | $4$ | $\frac{11}{2}$ | $7$ |
| $y$ | $\frac{13}{4}$ | $2$ | $\frac{3}{4}$ | $-\frac{1}{2}$ | $-\frac{7}{4}$ | $-3$ |


## q-326242 generated scalar-replay variant k=-2

Consider the curve with parametric equations

$$
x=-2\left(\frac{3}{2}t+1\right),\,y=-2\left(-\frac{5}{4}t+2\right),\,-1\le t\le 4.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | {{field-1}} | $-2$ | $-5$ | $-8$ | {{field-2}} | $-14$ |
| $y$ | {{field-3}} | $-4$ | $- \frac{3}{2}$ | $1$ | $\frac{7}{2}$ | $6$ |

field-1: $1$

field-2: $-11$

field-3: $- \frac{13}{2}$

Worked solution:

- To find the value of $x(-1),$ we substitute $t=-1$ into $x=-2\left(\frac{3}{2}t+1\right).$ This gives

$$
x(-1)=-2\left(\frac{3}{2}(-1)+1\right)=-2\left(-\frac{3}{2}+\frac{2}{2}\right)=1.
$$

- To find the value of $y(-1),$ we substitute $t=-1$ into $y=-2\left(-\frac{5}{4}t+2\right).$ This gives

$$
y(-1)=-2\left(-\frac{5}{4}(-1)+2\right)=-2\left(\frac{5}{4}+\frac{8}{4}\right)=- \frac{13}{2}.
$$

- To find the value of $x(3),$ we substitute $t=3$ into $x=-2\left(\frac{3}{2}t+1\right).$ This gives

$$
x(3)=-2\left(\frac{3}{2}(3)+1\right)=-2\left(\frac{9}{2}+\frac{2}{2}\right)=-11.
$$

Then the table is 

 

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $1$ | $-2$ | $-5$ | $-8$ | $-11$ | $-14$ |
| $y$ | $- \frac{13}{2}$ | $-4$ | $- \frac{3}{2}$ | $1$ | $\frac{7}{2}$ | $6$ |


## q-326242 generated scalar-replay variant k=2

Consider the curve with parametric equations

$$
x=2\left(\frac{3}{2}t+1\right),\,y=2\left(-\frac{5}{4}t+2\right),\,-1\le t\le 4.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | {{field-1}} | $2$ | $5$ | $8$ | {{field-2}} | $14$ |
| $y$ | {{field-3}} | $4$ | $\frac{3}{2}$ | $-1$ | $- \frac{7}{2}$ | $-6$ |

field-1: $-1$

field-2: $11$

field-3: $\frac{13}{2}$

Worked solution:

- To find the value of $x(-1),$ we substitute $t=-1$ into $x=2\left(\frac{3}{2}t+1\right).$ This gives

$$
x(-1)=2\left(\frac{3}{2}(-1)+1\right)=2\left(-\frac{3}{2}+\frac{2}{2}\right)=-1.
$$

- To find the value of $y(-1),$ we substitute $t=-1$ into $y=2\left(-\frac{5}{4}t+2\right).$ This gives

$$
y(-1)=2\left(-\frac{5}{4}(-1)+2\right)=2\left(\frac{5}{4}+\frac{8}{4}\right)=\frac{13}{2}.
$$

- To find the value of $x(3),$ we substitute $t=3$ into $x=2\left(\frac{3}{2}t+1\right).$ This gives

$$
x(3)=2\left(\frac{3}{2}(3)+1\right)=2\left(\frac{9}{2}+\frac{2}{2}\right)=11.
$$

Then the table is 

 

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-1$ | $2$ | $5$ | $8$ | $11$ | $14$ |
| $y$ | $\frac{13}{2}$ | $4$ | $\frac{3}{2}$ | $-1$ | $- \frac{7}{2}$ | $-6$ |


## q-326246 replay

Consider the curve with parametric equations

$$
x={t}^{3}-2t,\,y=-2t+\frac{3}{2},\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | $-1$ | {{field-1}} | $21$ | $56$ | {{field-2}} |
| $y$ | $\frac{3}{2}$ | $-\frac{1}{2}$ | $-\frac{5}{2}$ | {{field-3}} | $-\frac{13}{2}$ | $-\frac{17}{2}$ |

field-1: $4$

field-2: $115$

field-3: $- \frac{9}{2}$

Worked solution:

- To find the value of $x(2),$ we substitute $t=2$ into $x={t}^{3}-2t.$ This gives

$$
x(2)=(2)^{3}-2(2)=8-4=4.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=-2t+\frac{3}{2}.$ This gives

$$
y(3)=-2(3)+\frac{3}{2}=-6+\frac{3}{2}=-\frac{12}{2}+\frac{3}{2}=-\frac{9}{2}.
$$

- To find the value of $x(5),$ we substitute $t=5$ into $x={t}^{3}-2t.$ This gives

$$
x(5)=(5)^{3}-2(5)=125-10=115.
$$

Then the table is 

 

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | $-1$ | $4$ | $21$ | $56$ | $115$ |
| $y$ | $\frac{3}{2}$ | $-\frac{1}{2}$ | $-\frac{5}{2}$ | $-\frac{9}{2}$ | $-\frac{13}{2}$ | $-\frac{17}{2}$ |


## q-326246 generated scalar-replay variant k=-2

Consider the curve with parametric equations

$$
x=-2\left({t}^{3}-2t\right),\,y=-2\left(-2t+\frac{3}{2}\right),\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | $2$ | {{field-1}} | $-42$ | $-112$ | {{field-2}} |
| $y$ | $-3$ | $1$ | $5$ | {{field-3}} | $13$ | $17$ |

field-1: $-8$

field-2: $-230$

field-3: $9$

Worked solution:

- To find the value of $x(2),$ we substitute $t=2$ into $x=-2\left({t}^{3}-2t\right).$ This gives

$$
x(2)=-2\left((2)^{3}-2(2)\right)=-2\left(8-4\right)=-8.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=-2\left(-2t+\frac{3}{2}\right).$ This gives

$$
y(3)=-2\left(-2(3)+\frac{3}{2}\right)=-2\left(-6+\frac{3}{2}\right)=-2\left(-\frac{12}{2}+\frac{3}{2}\right)=9.
$$

- To find the value of $x(5),$ we substitute $t=5$ into $x=-2\left({t}^{3}-2t\right).$ This gives

$$
x(5)=-2\left((5)^{3}-2(5)\right)=-2\left(125-10\right)=-230.
$$

Then the table is 

 

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | $2$ | $-8$ | $-42$ | $-112$ | $-230$ |
| $y$ | $-3$ | $1$ | $5$ | $9$ | $13$ | $17$ |


## q-326246 generated scalar-replay variant k=2

Consider the curve with parametric equations

$$
x=2\left({t}^{3}-2t\right),\,y=2\left(-2t+\frac{3}{2}\right),\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | $-2$ | {{field-1}} | $42$ | $112$ | {{field-2}} |
| $y$ | $3$ | $-1$ | $-5$ | {{field-3}} | $-13$ | $-17$ |

field-1: $8$

field-2: $230$

field-3: $-9$

Worked solution:

- To find the value of $x(2),$ we substitute $t=2$ into $x=2\left({t}^{3}-2t\right).$ This gives

$$
x(2)=2\left((2)^{3}-2(2)\right)=2\left(8-4\right)=8.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=2\left(-2t+\frac{3}{2}\right).$ This gives

$$
y(3)=2\left(-2(3)+\frac{3}{2}\right)=2\left(-6+\frac{3}{2}\right)=2\left(-\frac{12}{2}+\frac{3}{2}\right)=-9.
$$

- To find the value of $x(5),$ we substitute $t=5$ into $x=2\left({t}^{3}-2t\right).$ This gives

$$
x(5)=2\left((5)^{3}-2(5)\right)=2\left(125-10\right)=230.
$$

Then the table is 

 

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | $-2$ | $8$ | $42$ | $112$ | $230$ |
| $y$ | $3$ | $-1$ | $-5$ | $-9$ | $-13$ | $-17$ |


## q-326247 replay

Consider the curve with parametric equations

$$
x={t}^{2}-2t+2,\,y=2{t}^{3}-3{t}^{2}+12,\,-1\le t\le 4.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $5$ | $2$ | {{field-1}} | $2$ | $5$ | $10$ |
| $y$ | $7$ | $12$ | $11$ | {{field-2}} | $39$ | {{field-3}} |

field-1: $1$

field-2: $16$

field-3: $92$

Worked solution:

- To find the value of $x(1),$ we substitute $t=1$ into $x={t}^{2}-2t+2.$ This gives

$$
x(1)=(1)^{2}-2(1)+2=1-2+2=1.
$$

- To find the value of $y(2),$ we substitute $t=2$ into $y=2{t}^{3}-3{t}^{2}+12.$ This gives

$$
y(2)=2(2)^{3}-3(2)^{2}+12=16-12+12=16.
$$

- To find the value of $y(4),$ we substitute $t=4$ into $y=2{t}^{3}-3{t}^{2}+12.$ This gives

$$
y(4)=2(4)^{3}-3(4)^{2}+12=128-48+12=92.
$$

Then the table is 

 

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $5$ | $2$ | $1$ | $2$ | $5$ | $10$ |
| $y$ | $7$ | $12$ | $11$ | $16$ | $39$ | $92$ |


## q-326247 generated scalar-replay variant k=-2

Consider the curve with parametric equations

$$
x=-2\left({t}^{2}-2t+2\right),\,y=-2\left(2{t}^{3}-3{t}^{2}+12\right),\,-1\le t\le 4.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-10$ | $-4$ | {{field-1}} | $-4$ | $-10$ | $-20$ |
| $y$ | $-14$ | $-24$ | $-22$ | {{field-2}} | $-78$ | {{field-3}} |

field-1: $-2$

field-2: $-32$

field-3: $-184$

Worked solution:

- To find the value of $x(1),$ we substitute $t=1$ into $x=-2\left({t}^{2}-2t+2\right).$ This gives

$$
x(1)=-2\left((1)^{2}-2(1)+2\right)=-2\left(1-2+2\right)=-2.
$$

- To find the value of $y(2),$ we substitute $t=2$ into $y=-2\left(2{t}^{3}-3{t}^{2}+12\right).$ This gives

$$
y(2)=-2\left(2(2)^{3}-3(2)^{2}+12\right)=-2\left(16-12+12\right)=-32.
$$

- To find the value of $y(4),$ we substitute $t=4$ into $y=-2\left(2{t}^{3}-3{t}^{2}+12\right).$ This gives

$$
y(4)=-2\left(2(4)^{3}-3(4)^{2}+12\right)=-2\left(128-48+12\right)=-184.
$$

Then the table is 

 

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-10$ | $-4$ | $-2$ | $-4$ | $-10$ | $-20$ |
| $y$ | $-14$ | $-24$ | $-22$ | $-32$ | $-78$ | $-184$ |


## q-326247 generated scalar-replay variant k=2

Consider the curve with parametric equations

$$
x=2\left({t}^{2}-2t+2\right),\,y=2\left(2{t}^{3}-3{t}^{2}+12\right),\,-1\le t\le 4.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $10$ | $4$ | {{field-1}} | $4$ | $10$ | $20$ |
| $y$ | $14$ | $24$ | $22$ | {{field-2}} | $78$ | {{field-3}} |

field-1: $2$

field-2: $32$

field-3: $184$

Worked solution:

- To find the value of $x(1),$ we substitute $t=1$ into $x=2\left({t}^{2}-2t+2\right).$ This gives

$$
x(1)=2\left((1)^{2}-2(1)+2\right)=2\left(1-2+2\right)=2.
$$

- To find the value of $y(2),$ we substitute $t=2$ into $y=2\left(2{t}^{3}-3{t}^{2}+12\right).$ This gives

$$
y(2)=2\left(2(2)^{3}-3(2)^{2}+12\right)=2\left(16-12+12\right)=32.
$$

- To find the value of $y(4),$ we substitute $t=4$ into $y=2\left(2{t}^{3}-3{t}^{2}+12\right).$ This gives

$$
y(4)=2\left(2(4)^{3}-3(4)^{2}+12\right)=2\left(128-48+12\right)=184.
$$

Then the table is 

 

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $10$ | $4$ | $2$ | $4$ | $10$ | $20$ |
| $y$ | $14$ | $24$ | $22$ | $32$ | $78$ | $184$ |


## q-326250 replay

Consider the curve with parametric equations

$$
x=\frac{1}{2}{t}^{3}-2,\,y=\frac{t-1}{t+1},\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-2$ | $-\frac{3}{2}$ | $2$ | $\frac{23}{2}$ | $30$ | {{field-1}} |
| $y$ | $-1$ | $0$ | {{field-2}} | $\frac{1}{2}$ | $\frac{3}{5}$ | {{field-3}} |

field-1: $\frac{121}{2}$

field-2: $\frac{1}{3}$

field-3: $\frac{2}{3}$

Worked solution:

- To find the value of $x(5),$ we substitute $t=5$ into $x=\frac{1}{2}{t}^{3}-2.$ This gives

$$
x(5)=\frac{1}{2}(5)^{3}-2=\frac{125}{2}-\frac{4}{2}=\frac{121}{2}.
$$

- To find the value of $y(2),$ we substitute $t=2$ into $y=\frac{t-1}{t+1}.$ This gives

$$
y(2)=\frac{2-1}{2+1}=\frac{1}{3}.
$$

- To find the value of $y(5),$ we substitute $t=5$ into $y=\frac{t-1}{t+1}.$ This gives

$$
y(5)=\frac{5-1}{5+1}=\frac{4}{6}=\frac{2}{3}.
$$

Then the table is 

 

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-2$ | $-\frac{3}{2}$ | $2$ | $\frac{23}{2}$ | $30$ | $\frac{121}{2}$ |
| $y$ | $-1$ | $0$ | $\frac{1}{3}$ | $\frac{1}{2}$ | $\frac{3}{5}$ | $\frac{2}{3}$ |


## q-326250 generated scalar-replay variant k=-2

Consider the curve with parametric equations

$$
x=-2\left(\frac{1}{2}{t}^{3}-2\right),\,y=-2\left(\frac{t-1}{t+1}\right),\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $4$ | $3$ | $-4$ | $-23$ | $-60$ | {{field-1}} |
| $y$ | $2$ | $0$ | {{field-2}} | $-1$ | $- \frac{6}{5}$ | {{field-3}} |

field-1: $-121$

field-2: $- \frac{2}{3}$

field-3: $- \frac{4}{3}$

Worked solution:

- To find the value of $x(5),$ we substitute $t=5$ into $x=-2\left(\frac{1}{2}{t}^{3}-2\right).$ This gives

$$
x(5)=-2\left(\frac{1}{2}(5)^{3}-2\right)=-2\left(\frac{125}{2}-\frac{4}{2}\right)=-121.
$$

- To find the value of $y(2),$ we substitute $t=2$ into $y=-2\left(\frac{t-1}{t+1}\right).$ This gives

$$
y(2)=-2\left(\frac{2-1}{2+1}\right)=- \frac{2}{3}.
$$

- To find the value of $y(5),$ we substitute $t=5$ into $y=-2\left(\frac{t-1}{t+1}\right).$ This gives

$$
y(5)=-2\left(\frac{5-1}{5+1}\right)=-2\left(\frac{4}{6}\right)=- \frac{4}{3}.
$$

Then the table is 

 

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $4$ | $3$ | $-4$ | $-23$ | $-60$ | $-121$ |
| $y$ | $2$ | $0$ | $- \frac{2}{3}$ | $-1$ | $- \frac{6}{5}$ | $- \frac{4}{3}$ |


## q-326250 generated scalar-replay variant k=2

Consider the curve with parametric equations

$$
x=2\left(\frac{1}{2}{t}^{3}-2\right),\,y=2\left(\frac{t-1}{t+1}\right),\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-4$ | $-3$ | $4$ | $23$ | $60$ | {{field-1}} |
| $y$ | $-2$ | $0$ | {{field-2}} | $1$ | $\frac{6}{5}$ | {{field-3}} |

field-1: $121$

field-2: $\frac{2}{3}$

field-3: $\frac{4}{3}$

Worked solution:

- To find the value of $x(5),$ we substitute $t=5$ into $x=2\left(\frac{1}{2}{t}^{3}-2\right).$ This gives

$$
x(5)=2\left(\frac{1}{2}(5)^{3}-2\right)=2\left(\frac{125}{2}-\frac{4}{2}\right)=121.
$$

- To find the value of $y(2),$ we substitute $t=2$ into $y=2\left(\frac{t-1}{t+1}\right).$ This gives

$$
y(2)=2\left(\frac{2-1}{2+1}\right)=\frac{2}{3}.
$$

- To find the value of $y(5),$ we substitute $t=5$ into $y=2\left(\frac{t-1}{t+1}\right).$ This gives

$$
y(5)=2\left(\frac{5-1}{5+1}\right)=2\left(\frac{4}{6}\right)=\frac{4}{3}.
$$

Then the table is 

 

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-4$ | $-3$ | $4$ | $23$ | $60$ | $121$ |
| $y$ | $-2$ | $0$ | $\frac{2}{3}$ | $1$ | $\frac{6}{5}$ | $\frac{4}{3}$ |


## q-326251 replay

Consider the curve with parametric equations

$$
x=\sqrt{\,t+4\,},\,y=\frac{3}{2}{t}^{2}-t,\,-3\le t\le 2.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | {{field-1}} | $\sqrt{2}$ | $\sqrt{3}$ | $2$ | $\sqrt{5}$ | $\sqrt{6}$ |
| $y$ | $\frac{33}{2}$ | $8$ | {{field-2}} | $0$ | $\frac{1}{2}$ | {{field-3}} |

field-1: $1$

field-2: $\frac{5}{2}$

field-3: $4$

Worked solution:

- To find the value of $x(-3),$ we substitute $t=-3$ into $x=\sqrt{\,t+4\,}.$ This gives

$$
x(-3)=\sqrt{-3+4}=\sqrt{1}=1.
$$

- To find the value of $y(-1),$ we substitute $t=-1$ into $y=\frac{3}{2}{t}^{2}-t.$ This gives

$$
y(-1)=\frac{3}{2}(-1)^{2}-(-1)=\frac{3}{2}+1=\frac{3}{2}+\frac{2}{2}=\frac{5}{2}.
$$

- To find the value of $y(2),$ we substitute $t=2$ into $y=\frac{3}{2}{t}^{2}-t.$ This gives

$$
y(2)=\frac{3}{2}(2)^{2}-(2)=6-2=4.
$$

Then the table is 

 

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $1$ | $\sqrt{2}$ | $\sqrt{3}$ | $2$ | $\sqrt{5}$ | $\sqrt{6}$ |
| $y$ | $\frac{33}{2}$ | $8$ | $\frac{5}{2}$ | $0$ | $\frac{1}{2}$ | $4$ |


## q-326251 generated scalar-replay variant k=-2

Consider the curve with parametric equations

$$
x=-2\left(\sqrt{\,t+4\,}\right),\,y=-2\left(\frac{3}{2}{t}^{2}-t\right),\,-3\le t\le 2.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | {{field-1}} | $- 2 \sqrt{2}$ | $- 2 \sqrt{3}$ | $-4$ | $- 2 \sqrt{5}$ | $- 2 \sqrt{6}$ |
| $y$ | $-33$ | $-16$ | {{field-2}} | $0$ | $-1$ | {{field-3}} |

field-1: $-2$

field-2: $-5$

field-3: $-8$

Worked solution:

- To find the value of $x(-3),$ we substitute $t=-3$ into $x=-2\left(\sqrt{\,t+4\,}\right).$ This gives

$$
x(-3)=-2\left(\sqrt{-3+4}\right)=-2\left(\sqrt{1}\right)=-2.
$$

- To find the value of $y(-1),$ we substitute $t=-1$ into $y=-2\left(\frac{3}{2}{t}^{2}-t\right).$ This gives

$$
y(-1)=-2\left(\frac{3}{2}(-1)^{2}-(-1)\right)=-2\left(\frac{3}{2}+1\right)=-2\left(\frac{3}{2}+\frac{2}{2}\right)=-5.
$$

- To find the value of $y(2),$ we substitute $t=2$ into $y=-2\left(\frac{3}{2}{t}^{2}-t\right).$ This gives

$$
y(2)=-2\left(\frac{3}{2}(2)^{2}-(2)\right)=-2\left(6-2\right)=-8.
$$

Then the table is 

 

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-2$ | $- 2 \sqrt{2}$ | $- 2 \sqrt{3}$ | $-4$ | $- 2 \sqrt{5}$ | $- 2 \sqrt{6}$ |
| $y$ | $-33$ | $-16$ | $-5$ | $0$ | $-1$ | $-8$ |


## q-326251 generated scalar-replay variant k=2

Consider the curve with parametric equations

$$
x=2\left(\sqrt{\,t+4\,}\right),\,y=2\left(\frac{3}{2}{t}^{2}-t\right),\,-3\le t\le 2.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | {{field-1}} | $2 \sqrt{2}$ | $2 \sqrt{3}$ | $4$ | $2 \sqrt{5}$ | $2 \sqrt{6}$ |
| $y$ | $33$ | $16$ | {{field-2}} | $0$ | $1$ | {{field-3}} |

field-1: $2$

field-2: $5$

field-3: $8$

Worked solution:

- To find the value of $x(-3),$ we substitute $t=-3$ into $x=2\left(\sqrt{\,t+4\,}\right).$ This gives

$$
x(-3)=2\left(\sqrt{-3+4}\right)=2\left(\sqrt{1}\right)=2.
$$

- To find the value of $y(-1),$ we substitute $t=-1$ into $y=2\left(\frac{3}{2}{t}^{2}-t\right).$ This gives

$$
y(-1)=2\left(\frac{3}{2}(-1)^{2}-(-1)\right)=2\left(\frac{3}{2}+1\right)=2\left(\frac{3}{2}+\frac{2}{2}\right)=5.
$$

- To find the value of $y(2),$ we substitute $t=2$ into $y=2\left(\frac{3}{2}{t}^{2}-t\right).$ This gives

$$
y(2)=2\left(\frac{3}{2}(2)^{2}-(2)\right)=2\left(6-2\right)=8.
$$

Then the table is 

 

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $2$ | $2 \sqrt{2}$ | $2 \sqrt{3}$ | $4$ | $2 \sqrt{5}$ | $2 \sqrt{6}$ |
| $y$ | $33$ | $16$ | $5$ | $0$ | $1$ | $8$ |


## q-326255 replay

Consider the curve with parametric equations

$$
x=cos\,(\frac{\pi t}{4}),\,y=sin\,(\frac{\pi t}{6}),\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $1$ | $\frac{\sqrt{2}}{2}$ | {{field-1}} | $-\frac{\sqrt{2}}{2}$ | $-1$ | $-\frac{\sqrt{2}}{2}$ |
| $y$ | $0$ | $\frac{1}{2}$ | $\frac{\sqrt{3}}{2}$ | {{field-2}} | {{field-3}} | $\frac{1}{2}$ |

field-1: $0$

field-2: $1$

field-3: $\frac{\sqrt{3}}{2}$

Worked solution:

- To find the value of $x(2),$ we substitute $t=2$ into $x=cos\,(\frac{\pi t}{4}).$ This gives

$$
x(2)=cos\,(\frac{\pi (2)}{4})=cos\,(\frac{\pi }{2})=0.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=sin\,(\frac{\pi t}{6}).$ This gives

$$
y(3)=sin\,(\frac{\pi (3)}{6})=sin\,(\frac{\pi }{2})=1.
$$

- To find the value of $y(4),$ we substitute $t=4$ into $y=sin\,(\frac{\pi t}{6}).$ This gives

$$
y(4)=sin\,(\frac{\pi (4)}{6})=sin\,(\frac{2\pi }{3})=\frac{\sqrt{3}}{2}.
$$

Then the table is 

 

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $1$ | $\frac{\sqrt{2}}{2}$ | $0$ | $-\frac{\sqrt{2}}{2}$ | $-1$ | $-\frac{\sqrt{2}}{2}$ |
| $y$ | $0$ | $\frac{1}{2}$ | $\frac{\sqrt{3}}{2}$ | $1$ | $\frac{\sqrt{3}}{2}$ | $\frac{1}{2}$ |


## q-326255 generated scalar-replay variant k=-2

Consider the curve with parametric equations

$$
x=-2\left(cos\,(\frac{\pi t}{4})\right),\,y=-2\left(sin\,(\frac{\pi t}{6})\right),\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-2$ | $- \sqrt{2}$ | {{field-1}} | $\sqrt{2}$ | $2$ | $\sqrt{2}$ |
| $y$ | $0$ | $-1$ | $- \sqrt{3}$ | {{field-2}} | {{field-3}} | $-1$ |

field-1: $0$

field-2: $-2$

field-3: $- \sqrt{3}$

Worked solution:

- To find the value of $x(2),$ we substitute $t=2$ into $x=-2\left(cos\,(\frac{\pi t}{4})\right).$ This gives

$$
x(2)=-2\left(cos\,(\frac{\pi (2)}{4})\right)=-2\left(cos\,(\frac{\pi }{2})\right)=0.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=-2\left(sin\,(\frac{\pi t}{6})\right).$ This gives

$$
y(3)=-2\left(sin\,(\frac{\pi (3)}{6})\right)=-2\left(sin\,(\frac{\pi }{2})\right)=-2.
$$

- To find the value of $y(4),$ we substitute $t=4$ into $y=-2\left(sin\,(\frac{\pi t}{6})\right).$ This gives

$$
y(4)=-2\left(sin\,(\frac{\pi (4)}{6})\right)=-2\left(sin\,(\frac{2\pi }{3})\right)=- \sqrt{3}.
$$

Then the table is 

 

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-2$ | $- \sqrt{2}$ | $0$ | $\sqrt{2}$ | $2$ | $\sqrt{2}$ |
| $y$ | $0$ | $-1$ | $- \sqrt{3}$ | $-2$ | $- \sqrt{3}$ | $-1$ |


## q-326255 generated scalar-replay variant k=2

Consider the curve with parametric equations

$$
x=2\left(cos\,(\frac{\pi t}{4})\right),\,y=2\left(sin\,(\frac{\pi t}{6})\right),\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $2$ | $\sqrt{2}$ | {{field-1}} | $- \sqrt{2}$ | $-2$ | $- \sqrt{2}$ |
| $y$ | $0$ | $1$ | $\sqrt{3}$ | {{field-2}} | {{field-3}} | $1$ |

field-1: $0$

field-2: $2$

field-3: $\sqrt{3}$

Worked solution:

- To find the value of $x(2),$ we substitute $t=2$ into $x=2\left(cos\,(\frac{\pi t}{4})\right).$ This gives

$$
x(2)=2\left(cos\,(\frac{\pi (2)}{4})\right)=2\left(cos\,(\frac{\pi }{2})\right)=0.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=2\left(sin\,(\frac{\pi t}{6})\right).$ This gives

$$
y(3)=2\left(sin\,(\frac{\pi (3)}{6})\right)=2\left(sin\,(\frac{\pi }{2})\right)=2.
$$

- To find the value of $y(4),$ we substitute $t=4$ into $y=2\left(sin\,(\frac{\pi t}{6})\right).$ This gives

$$
y(4)=2\left(sin\,(\frac{\pi (4)}{6})\right)=2\left(sin\,(\frac{2\pi }{3})\right)=\sqrt{3}.
$$

Then the table is 

 

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $2$ | $\sqrt{2}$ | $0$ | $- \sqrt{2}$ | $-2$ | $- \sqrt{2}$ |
| $y$ | $0$ | $1$ | $\sqrt{3}$ | $2$ | $\sqrt{3}$ | $1$ |


## q-326256 replay

Consider the curve with parametric equations

$$
x=cos\,(\frac{\pi t}{2}),\,y=tan\,(\frac{\pi t}{3}),\,-1\le t\le 4.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | {{field-1}} | $0$ | {{field-2}} | $0$ | $1$ |
| $y$ | $-\sqrt{3}$ | $0$ | {{field-3}} | $-\sqrt{3}$ | $0$ | $\sqrt{3}$ |

field-1: $1$

field-2: $-1$

field-3: $\sqrt{3}$

Worked solution:

- To find the value of $x(0),$ we substitute $t=0$ into $x=cos\,(\frac{\pi t}{2}).$ This gives

$$
x(0)=cos\,(\frac{\pi (0)}{2})=\operatorname{cos}⁡(0)=1.
$$

- To find the value of $y(1),$ we substitute $t=1$ into $y=tan\,(\frac{\pi t}{3}).$ This gives

$$
y(1)=tan\,(\frac{\pi (1)}{3})=tan\,(\frac{\pi }{3})=\sqrt{3}.
$$

- To find the value of $x(2),$ we substitute $t=2$ into $x=cos\,(\frac{\pi t}{2}).$ This gives

$$
x(2)=cos\,(\frac{\pi (2)}{2})=\operatorname{cos}⁡(\pi )=-1.
$$

Then the table is 

 

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | $1$ | $0$ | $-1$ | $0$ | $1$ |
| $y$ | $-\sqrt{3}$ | $0$ | $\sqrt{3}$ | $-\sqrt{3}$ | $0$ | $\sqrt{3}$ |


## q-326256 generated scalar-replay variant k=-2

Consider the curve with parametric equations

$$
x=-2\left(cos\,(\frac{\pi t}{2})\right),\,y=-2\left(tan\,(\frac{\pi t}{3})\right),\,-1\le t\le 4.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | {{field-1}} | $0$ | {{field-2}} | $0$ | $-2$ |
| $y$ | $2 \sqrt{3}$ | $0$ | {{field-3}} | $2 \sqrt{3}$ | $0$ | $- 2 \sqrt{3}$ |

field-1: $-2$

field-2: $2$

field-3: $- 2 \sqrt{3}$

Worked solution:

- To find the value of $x(0),$ we substitute $t=0$ into $x=-2\left(cos\,(\frac{\pi t}{2})\right).$ This gives

$$
x(0)=-2\left(cos\,(\frac{\pi (0)}{2})\right)=-2\left(\operatorname{cos}⁡(0)\right)=-2.
$$

- To find the value of $y(1),$ we substitute $t=1$ into $y=-2\left(tan\,(\frac{\pi t}{3})\right).$ This gives

$$
y(1)=-2\left(tan\,(\frac{\pi (1)}{3})\right)=-2\left(tan\,(\frac{\pi }{3})\right)=- 2 \sqrt{3}.
$$

- To find the value of $x(2),$ we substitute $t=2$ into $x=-2\left(cos\,(\frac{\pi t}{2})\right).$ This gives

$$
x(2)=-2\left(cos\,(\frac{\pi (2)}{2})\right)=-2\left(\operatorname{cos}⁡(\pi )\right)=2.
$$

Then the table is 

 

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | $-2$ | $0$ | $2$ | $0$ | $-2$ |
| $y$ | $2 \sqrt{3}$ | $0$ | $- 2 \sqrt{3}$ | $2 \sqrt{3}$ | $0$ | $- 2 \sqrt{3}$ |


## q-326256 generated scalar-replay variant k=2

Consider the curve with parametric equations

$$
x=2\left(cos\,(\frac{\pi t}{2})\right),\,y=2\left(tan\,(\frac{\pi t}{3})\right),\,-1\le t\le 4.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | {{field-1}} | $0$ | {{field-2}} | $0$ | $2$ |
| $y$ | $- 2 \sqrt{3}$ | $0$ | {{field-3}} | $- 2 \sqrt{3}$ | $0$ | $2 \sqrt{3}$ |

field-1: $2$

field-2: $-2$

field-3: $2 \sqrt{3}$

Worked solution:

- To find the value of $x(0),$ we substitute $t=0$ into $x=2\left(cos\,(\frac{\pi t}{2})\right).$ This gives

$$
x(0)=2\left(cos\,(\frac{\pi (0)}{2})\right)=2\left(\operatorname{cos}⁡(0)\right)=2.
$$

- To find the value of $y(1),$ we substitute $t=1$ into $y=2\left(tan\,(\frac{\pi t}{3})\right).$ This gives

$$
y(1)=2\left(tan\,(\frac{\pi (1)}{3})\right)=2\left(tan\,(\frac{\pi }{3})\right)=2 \sqrt{3}.
$$

- To find the value of $x(2),$ we substitute $t=2$ into $x=2\left(cos\,(\frac{\pi t}{2})\right).$ This gives

$$
x(2)=2\left(cos\,(\frac{\pi (2)}{2})\right)=2\left(\operatorname{cos}⁡(\pi )\right)=-2.
$$

Then the table is 

 

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | $2$ | $0$ | $-2$ | $0$ | $2$ |
| $y$ | $- 2 \sqrt{3}$ | $0$ | $2 \sqrt{3}$ | $- 2 \sqrt{3}$ | $0$ | $2 \sqrt{3}$ |


## q-6742 replay

For the parametric curve

$$
x=t+1,\,\,\,y={t}^{2}-6,-3\le t\le 3,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ | $c$ |
| $y$ | $a$ | $-2$ | $-5$ | $b$ | $-5$ | $-2$ | $3$ |

$$

$$

Find the value of $a-b-c.$

selection (review choices):

- A. $7$
- B. $3$
- C. $-6$
- D. $5$ [correct]
- E. $-4$

Worked solution:

- To find the value of $a,$ we substitute $t=-3$ into $y={t}^{2}-6.$ This gives

$$
a=(-3)^{2}-6=9-6=3.
$$

- To find the value of $b,$ we substitute $t=0$ into $y={t}^{2}-6.$ This gives

$$
b={0}^{2}-6=0-6=-6.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=t+1.$ This gives

$$
c=3+1=4.
$$

Finally, we have

$$
a-b-c=3-(-6)-4=5.
$$


## q-6742 generated scalar-replay variant k=-2

For the parametric curve

$$
x=-2\left(t+1\right),\,\,\,y=-2\left({t}^{2}-6\right),-3\le t\le 3,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $4$ | $2$ | $0$ | $-2$ | $-4$ | $-6$ | $c$ |
| $y$ | $a$ | $4$ | $10$ | $b$ | $10$ | $4$ | $-6$ |

$$

$$

Find the value of $a-b-c.$

selection (review choices):

- A. $-14$
- B. $-6$
- C. $12$
- D. $-10$ [correct]
- E. $8$

Worked solution:

- To find the value of $a,$ we substitute $t=-3$ into $y=-2\left({t}^{2}-6\right).$ This gives

$$
a=-2\left((-3)^{2}-6\right)=-2\left(9-6\right)=-6.
$$

- To find the value of $b,$ we substitute $t=0$ into $y=-2\left({t}^{2}-6\right).$ This gives

$$
b=-2\left({0}^{2}-6\right)=-2\left(0-6\right)=12.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=-2\left(t+1\right).$ This gives

$$
c=-2\left(3+1\right)=-8.
$$

Finally, we have

$$
a-b-c=-2\left(3-(-6)-4\right)=-10.
$$


## q-6742 generated scalar-replay variant k=2

For the parametric curve

$$
x=2\left(t+1\right),\,\,\,y=2\left({t}^{2}-6\right),-3\le t\le 3,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-4$ | $-2$ | $0$ | $2$ | $4$ | $6$ | $c$ |
| $y$ | $a$ | $-4$ | $-10$ | $b$ | $-10$ | $-4$ | $6$ |

$$

$$

Find the value of $a-b-c.$

selection (review choices):

- A. $14$
- B. $6$
- C. $-12$
- D. $10$ [correct]
- E. $-8$

Worked solution:

- To find the value of $a,$ we substitute $t=-3$ into $y=2\left({t}^{2}-6\right).$ This gives

$$
a=2\left((-3)^{2}-6\right)=2\left(9-6\right)=6.
$$

- To find the value of $b,$ we substitute $t=0$ into $y=2\left({t}^{2}-6\right).$ This gives

$$
b=2\left({0}^{2}-6\right)=2\left(0-6\right)=-12.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=2\left(t+1\right).$ This gives

$$
c=2\left(3+1\right)=8.
$$

Finally, we have

$$
a-b-c=2\left(3-(-6)-4\right)=10.
$$


## q-6825 replay

For the parametric curve

$$
x=3t-2,\,\,\,y=\frac{10}{{t}^{2}+1},\,-3\le t\le 3,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $a$ | $-8$ | $-5$ | $-2$ | $1$ | $4$ | $c$ |
| $y$ | $1$ | $b$ | $5$ | $10$ | $5$ | $2$ | $1$ |

$$

$$

Find the value of $a+b+c.$

selection (review choices):

- A. $3$
- B. $-2$ [correct]
- C. $1$
- D. $0$
- E. $-1$

Worked solution:

- To find the value of $a,$ we substitute $t=-3$ into $x=3t-2.$ This gives

$$
a=3(-3)-2=-9-2=-11.
$$

- To find the value of $b,$ we substitute $t=-2$ into $y=\frac{10}{{t}^{2}+1}.$ This gives

$$
b=\frac{10}{(-2)^{2}+1}=\frac{10}{5}=2.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=3t-2.$ This gives

$$
c=3(3)-2=9-2=7.
$$

Finally, we have

$$
a+b+c=-11+2+7=-2.
$$


## q-6825 generated scalar-replay variant k=-2

For the parametric curve

$$
x=-2\left(3t-2\right),\,\,\,y=-2\left(\frac{10}{{t}^{2}+1}\right),\,-3\le t\le 3,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $a$ | $16$ | $10$ | $4$ | $-2$ | $-8$ | $c$ |
| $y$ | $-2$ | $b$ | $-10$ | $-20$ | $-10$ | $-4$ | $-2$ |

$$

$$

Find the value of $a+b+c.$

selection (review choices):

- A. $-6$
- B. $4$ [correct]
- C. $-2$
- D. $0$
- E. $2$

Worked solution:

- To find the value of $a,$ we substitute $t=-3$ into $x=-2\left(3t-2\right).$ This gives

$$
a=-2\left(3(-3)-2\right)=-2\left(-9-2\right)=22.
$$

- To find the value of $b,$ we substitute $t=-2$ into $y=-2\left(\frac{10}{{t}^{2}+1}\right).$ This gives

$$
b=-2\left(\frac{10}{(-2)^{2}+1}\right)=-2\left(\frac{10}{5}\right)=-4.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=-2\left(3t-2\right).$ This gives

$$
c=-2\left(3(3)-2\right)=-2\left(9-2\right)=-14.
$$

Finally, we have

$$
a+b+c=-2\left(-11+2+7\right)=4.
$$


## q-6825 generated scalar-replay variant k=2

For the parametric curve

$$
x=2\left(3t-2\right),\,\,\,y=2\left(\frac{10}{{t}^{2}+1}\right),\,-3\le t\le 3,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $a$ | $-16$ | $-10$ | $-4$ | $2$ | $8$ | $c$ |
| $y$ | $2$ | $b$ | $10$ | $20$ | $10$ | $4$ | $2$ |

$$

$$

Find the value of $a+b+c.$

selection (review choices):

- A. $6$
- B. $-4$ [correct]
- C. $2$
- D. $0$
- E. $-2$

Worked solution:

- To find the value of $a,$ we substitute $t=-3$ into $x=2\left(3t-2\right).$ This gives

$$
a=2\left(3(-3)-2\right)=2\left(-9-2\right)=-22.
$$

- To find the value of $b,$ we substitute $t=-2$ into $y=2\left(\frac{10}{{t}^{2}+1}\right).$ This gives

$$
b=2\left(\frac{10}{(-2)^{2}+1}\right)=2\left(\frac{10}{5}\right)=4.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=2\left(3t-2\right).$ This gives

$$
c=2\left(3(3)-2\right)=2\left(9-2\right)=14.
$$

Finally, we have

$$
a+b+c=2\left(-11+2+7\right)=-4.
$$


## q-69922 replay

For the parametric curve

$$
x=2t+1,\,\,\,y=2t-1,\,0\le t\le 5,
$$

consider the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $1$ | $3$ | $b$ | $7$ | $9$ | $11$ |
| $y$ | $a$ | $1$ | $3$ | $5$ | $c$ | $9$ |

$$

$$

Find the value of $a-b-c.$

selection (review choices):

- A. $-13$ [correct]
- B. $-10$
- C. $15$
- D. $12$
- E. $8$

Worked solution:

- To find the value of $a,$ we substitute $t=0$ into $y=2t-1.$ This gives

$$
a=2(0)-1=0-1=-1.
$$

- To find the value of $b,$ we substitute $t=2$ into $x=2t+1.$ This gives

$$
b=2(2)+1=4+1=5.
$$

- To find the value of $c,$ we substitute $t=4$ into $y=2t-1.$ This gives

$$
c=2(4)-1=8-1=7.
$$

Finally, we have

$$
a-b-c=-1-5-7=-13.
$$


## q-69922 generated scalar-replay variant k=-2

For the parametric curve

$$
x=-2\left(2t+1\right),\,\,\,y=-2\left(2t-1\right),\,0\le t\le 5,
$$

consider the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-2$ | $-6$ | $b$ | $-14$ | $-18$ | $-22$ |
| $y$ | $a$ | $-2$ | $-6$ | $-10$ | $c$ | $-18$ |

$$

$$

Find the value of $a-b-c.$

selection (review choices):

- A. $26$ [correct]
- B. $20$
- C. $-30$
- D. $-24$
- E. $-16$

Worked solution:

- To find the value of $a,$ we substitute $t=0$ into $y=-2\left(2t-1\right).$ This gives

$$
a=-2\left(2(0)-1\right)=-2\left(0-1\right)=2.
$$

- To find the value of $b,$ we substitute $t=2$ into $x=-2\left(2t+1\right).$ This gives

$$
b=-2\left(2(2)+1\right)=-2\left(4+1\right)=-10.
$$

- To find the value of $c,$ we substitute $t=4$ into $y=-2\left(2t-1\right).$ This gives

$$
c=-2\left(2(4)-1\right)=-2\left(8-1\right)=-14.
$$

Finally, we have

$$
a-b-c=-2\left(-1-5-7\right)=26.
$$


## q-69922 generated scalar-replay variant k=2

For the parametric curve

$$
x=2\left(2t+1\right),\,\,\,y=2\left(2t-1\right),\,0\le t\le 5,
$$

consider the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $2$ | $6$ | $b$ | $14$ | $18$ | $22$ |
| $y$ | $a$ | $2$ | $6$ | $10$ | $c$ | $18$ |

$$

$$

Find the value of $a-b-c.$

selection (review choices):

- A. $-26$ [correct]
- B. $-20$
- C. $30$
- D. $24$
- E. $16$

Worked solution:

- To find the value of $a,$ we substitute $t=0$ into $y=2\left(2t-1\right).$ This gives

$$
a=2\left(2(0)-1\right)=2\left(0-1\right)=-2.
$$

- To find the value of $b,$ we substitute $t=2$ into $x=2\left(2t+1\right).$ This gives

$$
b=2\left(2(2)+1\right)=2\left(4+1\right)=10.
$$

- To find the value of $c,$ we substitute $t=4$ into $y=2\left(2t-1\right).$ This gives

$$
c=2\left(2(4)-1\right)=2\left(8-1\right)=14.
$$

Finally, we have

$$
a-b-c=2\left(-1-5-7\right)=-26.
$$


## authored easy generated variant 0

For the parametric curve

$$
x=5 t + 3,\,y=3 t - 2,\,-1\le t\le 4.
$$

consider the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $a$ | $3$ | $8$ | $13$ | $b$ | $23$ |
| $y$ | $-5$ | $-2$ | $c$ | $4$ | $7$ | $10$ |

Find the value of $a-b-c.$

selection (review choices):

- A. $-21$ [correct]
- B. $21$
- C. $-17$
- D. $15$
- E. $-19$

Worked solution:

- To find the value of $a,$ we substitute $t=-1$ into $x=5 t + 3.$ This gives

$$
a=5 (-1) + 3=(3)+(-5)=-2.
$$

- To find the value of $b,$ we substitute $t=3$ into $x=5 t + 3.$ This gives

$$
b=5 (3) + 3=(3)+(15)=18.
$$

- To find the value of $c,$ we substitute $t=1$ into $y=3 t - 2.$ This gives

$$
c=3 (1) - 2=(-2)+(3)=1.
$$

Finally, we have

$$
a-b-c=(-2)-(18)-(1)=-21.
$$


## authored easy generated variant 1

Consider the curve with parametric equations

$$
x=3 t + 3,\,y=- 5 t - 1,\,-1\le t\le 4.
$$

Fill in the blanks in the following table of values:

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | {{field-1}} | $3$ | $6$ | $9$ | {{field-2}} | $15$ |
| $y$ | $4$ | $-1$ | {{field-3}} | $-11$ | $-16$ | $-21$ |

field-1: $0$

field-2: $12$

field-3: $-6$

Worked solution:

- To find the value of $x(-1),$ we substitute $t=-1$ into $x=3 t + 3.$ This gives

$$
x(-1)=3 (-1) + 3=(3)+(-3)=0.
$$

- To find the value of $x(3),$ we substitute $t=3$ into $x=3 t + 3.$ This gives

$$
x(3)=3 (3) + 3=(3)+(9)=12.
$$

- To find the value of $y(1),$ we substitute $t=1$ into $y=- 5 t - 1.$ This gives

$$
y(1)=- 5 (1) - 1=(-1)+(-5)=-6.
$$

Then the table is

| **$t$** | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $0$ | $3$ | $6$ | $9$ | $12$ | $15$ |
| $y$ | $4$ | $-1$ | $-6$ | $-11$ | $-16$ | $-21$ |


## authored moderate generated variant 0

Consider the curve with parametric equations

$$
x=\frac{t^{2}}{4} + \frac{t}{3} - 6,\,y=- \frac{t^{2}}{4} + \frac{2 t}{3} + 2,\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-6$ | $- \frac{65}{12}$ | {{field-1}} | $- \frac{11}{4}$ | {{field-3}} | $\frac{23}{12}$ |
| $y$ | $2$ | $\frac{29}{12}$ | $\frac{7}{3}$ | {{field-2}} | $\frac{2}{3}$ | $- \frac{11}{12}$ |

field-1: $- \frac{13}{3}$

field-2: $\frac{7}{4}$

field-3: $- \frac{2}{3}$

Worked solution:

- To find the value of $x(2),$ we substitute $t=2$ into $x=\frac{t^{2}}{4} + \frac{t}{3} - 6.$ This gives

$$
x(2)=\frac{(2)^{2}}{4} + \frac{(2)}{3} - 6=(-6)+(\frac{2}{3})+(1)=- \frac{13}{3}.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=- \frac{t^{2}}{4} + \frac{2 t}{3} + 2.$ This gives

$$
y(3)=- \frac{(3)^{2}}{4} + \frac{2 (3)}{3} + 2=(2)+(- \frac{9}{4})+(2)=\frac{7}{4}.
$$

- To find the value of $x(4),$ we substitute $t=4$ into $x=\frac{t^{2}}{4} + \frac{t}{3} - 6.$ This gives

$$
x(4)=\frac{(4)^{2}}{4} + \frac{(4)}{3} - 6=(-6)+(\frac{4}{3})+(4)=- \frac{2}{3}.
$$

Then the table is

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-6$ | $- \frac{65}{12}$ | $- \frac{13}{3}$ | $- \frac{11}{4}$ | $- \frac{2}{3}$ | $\frac{23}{12}$ |
| $y$ | $2$ | $\frac{29}{12}$ | $\frac{7}{3}$ | $\frac{7}{4}$ | $\frac{2}{3}$ | $- \frac{11}{12}$ |


## authored moderate generated variant 1

Consider the curve with parametric equations

$$
x=- \frac{3 t^{2}}{4} + \frac{2 t}{3} - 5,\,y=- \frac{t^{2}}{4} - \frac{4 t}{3} + 2,\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-5$ | $- \frac{61}{12}$ | {{field-1}} | $- \frac{39}{4}$ | {{field-3}} | $- \frac{245}{12}$ |
| $y$ | $2$ | $\frac{5}{12}$ | $- \frac{5}{3}$ | {{field-2}} | $- \frac{22}{3}$ | $- \frac{131}{12}$ |

field-1: $- \frac{20}{3}$

field-2: $- \frac{17}{4}$

field-3: $- \frac{43}{3}$

Worked solution:

- To find the value of $x(2),$ we substitute $t=2$ into $x=- \frac{3 t^{2}}{4} + \frac{2 t}{3} - 5.$ This gives

$$
x(2)=- \frac{3 (2)^{2}}{4} + \frac{2 (2)}{3} - 5=(-5)+(-3)+(\frac{4}{3})=- \frac{20}{3}.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=- \frac{t^{2}}{4} - \frac{4 t}{3} + 2.$ This gives

$$
y(3)=- \frac{(3)^{2}}{4} - \frac{4 (3)}{3} + 2=(2)+(-4)+(- \frac{9}{4})=- \frac{17}{4}.
$$

- To find the value of $x(4),$ we substitute $t=4$ into $x=- \frac{3 t^{2}}{4} + \frac{2 t}{3} - 5.$ This gives

$$
x(4)=- \frac{3 (4)^{2}}{4} + \frac{2 (4)}{3} - 5=(-5)+(-12)+(\frac{8}{3})=- \frac{43}{3}.
$$

Then the table is

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-5$ | $- \frac{61}{12}$ | $- \frac{20}{3}$ | $- \frac{39}{4}$ | $- \frac{43}{3}$ | $- \frac{245}{12}$ |
| $y$ | $2$ | $\frac{5}{12}$ | $- \frac{5}{3}$ | $- \frac{17}{4}$ | $- \frac{22}{3}$ | $- \frac{131}{12}$ |


## authored hard generated variant 0

Consider the curve with parametric equations

$$
x=\frac{t^{3}}{4} + \frac{t^{2}}{3} - 6,\,y=- \frac{t^{3}}{4} + \frac{2 t^{2}}{3} + 2,\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-6$ | $- \frac{65}{12}$ | {{field-1}} | $\frac{15}{4}$ | {{field-3}} | $\frac{403}{12}$ |
| $y$ | $2$ | $\frac{29}{12}$ | $\frac{8}{3}$ | {{field-2}} | $- \frac{10}{3}$ | $- \frac{151}{12}$ |

field-1: $- \frac{8}{3}$

field-2: $\frac{5}{4}$

field-3: $\frac{46}{3}$

Worked solution:

- To find the value of $x(2),$ we substitute $t=2$ into $x=\frac{t^{3}}{4} + \frac{t^{2}}{3} - 6.$ This gives

$$
x(2)=\frac{(2)^{3}}{4} + \frac{(2)^{2}}{3} - 6=(-6)+(\frac{4}{3})+(2)=- \frac{8}{3}.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=- \frac{t^{3}}{4} + \frac{2 t^{2}}{3} + 2.$ This gives

$$
y(3)=- \frac{(3)^{3}}{4} + \frac{2 (3)^{2}}{3} + 2=(2)+(- \frac{27}{4})+(6)=\frac{5}{4}.
$$

- To find the value of $x(4),$ we substitute $t=4$ into $x=\frac{t^{3}}{4} + \frac{t^{2}}{3} - 6.$ This gives

$$
x(4)=\frac{(4)^{3}}{4} + \frac{(4)^{2}}{3} - 6=(-6)+(\frac{16}{3})+(16)=\frac{46}{3}.
$$

Then the table is

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-6$ | $- \frac{65}{12}$ | $- \frac{8}{3}$ | $\frac{15}{4}$ | $\frac{46}{3}$ | $\frac{403}{12}$ |
| $y$ | $2$ | $\frac{29}{12}$ | $\frac{8}{3}$ | $\frac{5}{4}$ | $- \frac{10}{3}$ | $- \frac{151}{12}$ |


## authored hard generated variant 1

Consider the curve with parametric equations

$$
x=- \frac{3 t^{3}}{4} + \frac{2 t^{2}}{3} - 5,\,y=- \frac{t^{3}}{4} - \frac{4 t^{2}}{3} + 2,\,0\le t\le 5.
$$

Fill in the blanks in the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-5$ | $- \frac{61}{12}$ | {{field-1}} | $- \frac{77}{4}$ | {{field-3}} | $- \frac{985}{12}$ |
| $y$ | $2$ | $\frac{5}{12}$ | $- \frac{16}{3}$ | {{field-2}} | $- \frac{106}{3}$ | $- \frac{751}{12}$ |

field-1: $- \frac{25}{3}$

field-2: $- \frac{67}{4}$

field-3: $- \frac{127}{3}$

Worked solution:

- To find the value of $x(2),$ we substitute $t=2$ into $x=- \frac{3 t^{3}}{4} + \frac{2 t^{2}}{3} - 5.$ This gives

$$
x(2)=- \frac{3 (2)^{3}}{4} + \frac{2 (2)^{2}}{3} - 5=(-5)+(-6)+(\frac{8}{3})=- \frac{25}{3}.
$$

- To find the value of $y(3),$ we substitute $t=3$ into $y=- \frac{t^{3}}{4} - \frac{4 t^{2}}{3} + 2.$ This gives

$$
y(3)=- \frac{(3)^{3}}{4} - \frac{4 (3)^{2}}{3} + 2=(2)+(-12)+(- \frac{27}{4})=- \frac{67}{4}.
$$

- To find the value of $x(4),$ we substitute $t=4$ into $x=- \frac{3 t^{3}}{4} + \frac{2 t^{2}}{3} - 5.$ This gives

$$
x(4)=- \frac{3 (4)^{3}}{4} + \frac{2 (4)^{2}}{3} - 5=(-5)+(-48)+(\frac{32}{3})=- \frac{127}{3}.
$$

Then the table is

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-5$ | $- \frac{61}{12}$ | $- \frac{25}{3}$ | $- \frac{77}{4}$ | $- \frac{127}{3}$ | $- \frac{985}{12}$ |
| $y$ | $2$ | $\frac{5}{12}$ | $- \frac{16}{3}$ | $- \frac{67}{4}$ | $- \frac{106}{3}$ | $- \frac{751}{12}$ |


## q-6742 authored complete sign-error bank

For the parametric curve

$$
x=2\left(t+1\right),\,\,\,y=2\left({t}^{2}-6\right),-3\le t\le 3,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $-4$ | $-2$ | $0$ | $2$ | $4$ | $6$ | $c$ |
| $y$ | $a$ | $-4$ | $-10$ | $b$ | $-10$ | $-4$ | $6$ |

$$

$$

Find the value of $a-b-c.$

selection (review choices):

- A. $10$ [correct]
- B. $-10$
- C. $-2$
- D. $-14$
- E. $26$

Worked solution:

- To find the value of $a,$ we substitute $t=-3$ into $y=2\left({t}^{2}-6\right).$ This gives

$$
a=2\left((-3)^{2}-6\right)=2\left(9-6\right)=6.
$$

- To find the value of $b,$ we substitute $t=0$ into $y=2\left({t}^{2}-6\right).$ This gives

$$
b=2\left({0}^{2}-6\right)=2\left(0-6\right)=-12.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=2\left(t+1\right).$ This gives

$$
c=2\left(3+1\right)=8.
$$

Finally, we have

$$
a-b-c=2\left(3-(-6)-4\right)=10.
$$


## q-6825 authored complete sign-error bank

For the parametric curve

$$
x=2\left(3t-2\right),\,\,\,y=2\left(\frac{10}{{t}^{2}+1}\right),\,-3\le t\le 3,
$$

consider the following table of values:

| **$t$** | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ | $a$ | $-16$ | $-10$ | $-4$ | $2$ | $8$ | $c$ |
| $y$ | $2$ | $b$ | $10$ | $20$ | $10$ | $4$ | $2$ |

$$

$$

Find the value of $a+b+c.$

selection (review choices):

- A. $-4$ [correct]
- B. $4$
- C. $40$
- D. $-12$
- E. $-32$

Worked solution:

- To find the value of $a,$ we substitute $t=-3$ into $x=2\left(3t-2\right).$ This gives

$$
a=2\left(3(-3)-2\right)=2\left(-9-2\right)=-22.
$$

- To find the value of $b,$ we substitute $t=-2$ into $y=2\left(\frac{10}{{t}^{2}+1}\right).$ This gives

$$
b=2\left(\frac{10}{(-2)^{2}+1}\right)=2\left(\frac{10}{5}\right)=4.
$$

- To find the value of $c,$ we substitute $t=3$ into $x=2\left(3t-2\right).$ This gives

$$
c=2\left(3(3)-2\right)=2\left(9-2\right)=14.
$$

Finally, we have

$$
a+b+c=2\left(-11+2+7\right)=-4.
$$


## q-69922 authored complete sign-error bank

For the parametric curve

$$
x=2\left(2t+1\right),\,\,\,y=2\left(2t-1\right),\,0\le t\le 5,
$$

consider the following table of values:

| **$t$** | $0$ | $1$ | $2$ | $3$ | $4$ | $5$ |
| --- | --- | --- | --- | --- | --- | --- |
| $x$ | $2$ | $6$ | $b$ | $14$ | $18$ | $22$ |
| $y$ | $a$ | $2$ | $6$ | $10$ | $c$ | $18$ |

$$

$$

Find the value of $a-b-c.$

selection (review choices):

- A. $-26$ [correct]
- B. $26$
- C. $-22$
- D. $-6$
- E. $2$

Worked solution:

- To find the value of $a,$ we substitute $t=0$ into $y=2\left(2t-1\right).$ This gives

$$
a=2\left(2(0)-1\right)=2\left(0-1\right)=-2.
$$

- To find the value of $b,$ we substitute $t=2$ into $x=2\left(2t+1\right).$ This gives

$$
b=2\left(2(2)+1\right)=2\left(4+1\right)=10.
$$

- To find the value of $c,$ we substitute $t=4$ into $y=2\left(2t-1\right).$ This gives

$$
c=2\left(2(4)-1\right)=2\left(8-1\right)=14.
$$

Finally, we have

$$
a-b-c=2\left(-1-5-7\right)=-26.
$$
