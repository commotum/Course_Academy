# Substitution review at frozen basis 2275

Immutable raw source records remain in source-cases.json. Missing observed fields and malformed/omitted source context remain raw-ineligible; supported completions are separate. Prior generated inventory retains its raw records and identities in independent-inventory.json.

## Original q-171690

```text
Consider the following system of equations:
${x + 5y = 13; y = x + 5$
Find the solution $(x, y)$ to this system using the method of substitution.The solution is
$($
{{field-1}}
$$,
{{field-2}}
$)$
```

Captured answer fields:
```json
[
  {
    ":answer-field/id": "c3a49164-4f9d-597a-9dc6-abf7860aa4ba",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186070261
  },
  {
    ":answer-field/id": "795f6bc6-c4b4-5520-883c-77f20cec08ce",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186070262
  }
]
```

```text
No captured worked solution.
```

## Supported replay q-171690

Consider the following system of equations:
$$
\left\{\begin{aligned}x+5y &=13 \\ y &=x+5\end{aligned}\right.
$$
Find the solution $(x, y)$ to this system using the method of substitution.The solution is
$($
{{field-1}}
$,$
{{field-2}}
$)$

```json
[
  {
    ":answer-field/id": "3b9915b6-680b-5f59-b75b-e92784e17367",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "2fa8f128-73bd-571b-9c92-794cefa7eea1",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-2"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "2fa8f128-73bd-571b-9c92-794cefa7eea1"
    ]
  },
  {
    ":answer-field/id": "cd0e893f-e996-5c7e-953b-ad11eb547735",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "f5ac8207-df44-50b3-b78a-dc38d44dac6d",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "f5ac8207-df44-50b3-b78a-dc38d44dac6d"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the second equation is already solved for $y:$

$$
y=x+5
$$

So, we replace $y$ in the first equation and solve for $x:$

$$
\begin{aligned}x+5y & =13 \\ x+5(x+5) & =13 \\ x+5x+25 & =13 \\ 6x+25 & =13 \\ 6x & =-12 \\ x & =-2\end{aligned}
$$

If we now substitute $x=-2$ into $y=x+5,$ we can then find the value of $y:$

$$
\begin{aligned}y & =(-2)+5 \\ y & =3\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-2,\,y=3.$

## Original q-4133

```text
Given the system of equations below, what is the value of $a - b$?

${3a + 2b = 4; - 4a + b = 2$
```

Captured answer fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "b643d8b6-388a-54ab-b235-3715b075ca10",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-1",
        ":db/id": 17592186071271
      },
      {
        ":answer/id": "b7ca0af2-c9e2-50b8-aa82-29c811387109",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2",
        ":db/id": 17592186071272
      },
      {
        ":answer/id": "db6b16f5-5009-56b0-8dbc-feec7e3509af",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "1",
        ":db/id": 17592186071273
      },
      {
        ":answer/id": "4284c760-b4f9-5590-8b60-e0effdb4b5dd",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3",
        ":db/id": 17592186071274
      },
      {
        ":answer/id": "4fbb9be1-44f2-5b9e-84d5-cc040bbae729",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-2",
        ":db/id": 17592186071275
      }
    ],
    ":answer-field/id": "4b7102cd-5458-52ab-8b4b-346cb2e5c0d3",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186071270
  }
]
```

```text
No captured worked solution.
```

## Supported replay q-4133

Given the system of equations below, what is the value of $a - b$?

$$
\left\{\begin{aligned}3a+2b &=4 \\ -4a+b &=2\end{aligned}\right.
$$

```json
[
  {
    ":answer-field/id": "bc8994c9-8a2c-56d4-aa1c-cb2be7e9dc57",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "0479593b-5625-56eb-a8fe-c4958a8e9cfb",
        ":answer/type": ":answer.type/math",
        ":answer/value": "1"
      },
      {
        ":answer/id": "b33f5f6e-269e-54db-b5c8-018e3458e232",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-2"
      },
      {
        ":answer/id": "107fb6cb-e8c2-52af-b223-8cff3c5961c9",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1"
      },
      {
        ":answer/id": "35e52cca-c0d6-5278-a7bb-a55ec228ae96",
        ":answer/type": ":answer.type/math",
        ":answer/value": "2"
      },
      {
        ":answer/id": "69f9b4db-c1ef-564c-8b35-b99f2032c8c3",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "b33f5f6e-269e-54db-b5c8-018e3458e232"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the second equation, we can isolate $b$:

$$
\begin{aligned}-4a+b & =2 \\ b & =2+4a\end{aligned}
$$

Then, we substitute $b=2+4a$ into the first equation and solve for $a:$

$$
\begin{aligned}3a+2b & =4 \\ 3a+2(2+4a) & =4 \\ 3a+4+8a & =4 \\ 11a+4 & =4 \\ 11a & =0 \\ a & =0\end{aligned}
$$

If we now substitute $a=0$ into $b=2+4a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =2+4(0) \\ b & =2\end{aligned}
$$

Therefore, $a-b=0-(2)=-2.$

## Original q-5179

```text
Given the system of equations below, what is the value of $p - q$?

${3p = 15; p + 2q = 9$
```

Captured answer fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "831b8a12-3240-5543-8f0b-63a066174430",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3",
        ":db/id": 17592186071349
      },
      {
        ":answer/id": "e71abec1-af90-564e-96cc-65f749dff99a",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-4",
        ":db/id": 17592186071350
      },
      {
        ":answer/id": "f9bd14c8-f201-5c70-ba77-5489006197a2",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-3",
        ":db/id": 17592186071351
      },
      {
        ":answer/id": "30891c0a-e32e-5e99-9826-2629f5f5792b",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2",
        ":db/id": 17592186071352
      },
      {
        ":answer/id": "424e6c76-ef65-55f4-bb2c-05129500785f",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5",
        ":db/id": 17592186071353
      }
    ],
    ":answer-field/id": "4ff0f62d-b46f-5fed-abea-e9c339cbff76",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186071348
  }
]
```

```text
No captured worked solution.
```

## Supported replay q-5179

Given the system of equations below, what is the value of $p - q$?

$$
\left\{\begin{aligned}3p &=15 \\ p+2q &=9\end{aligned}\right.
$$

```json
[
  {
    ":answer-field/id": "d7e78fdb-6264-5a65-b9e1-f45a80e34bf4",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "2bf32267-c1b6-5d99-bf01-18c23c2228db",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-3"
      },
      {
        ":answer/id": "2f3dffb2-dcea-579e-8566-79bceec82b09",
        ":answer/type": ":answer.type/math",
        ":answer/value": "5"
      },
      {
        ":answer/id": "d75c7cfb-ce5a-5a80-a13e-36d4af609999",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3"
      },
      {
        ":answer/id": "fbe39ca0-4a3d-5467-8543-e4753dc48047",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-4"
      },
      {
        ":answer/id": "11bb2fc4-7a93-5404-a601-e2aafc35a3ad",
        ":answer/type": ":answer.type/math",
        ":answer/value": "2"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "d75c7cfb-ce5a-5a80-a13e-36d4af609999"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the first equation, we can isolate $p$ by dividing both sides by $3:$

$$
\begin{aligned}3p & =15 \\ p & =5\end{aligned}
$$

Then, we substitute $p=5$ into the second equation and solve for $q:$

$$
\begin{aligned}p+2q & =9 \\ (5)+2q & =9 \\ 2q & =4 \\ q & =2\end{aligned}
$$

Therefore, $p-q=5-(2)=3.$

## Original q-167194

```text
The coefficients $a$ and $b$ also satisfy the equation $20b+400a=7\,200.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}
```

Captured answer fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "d447476e-6786-52c0-9a5b-aa6aa6b42f96",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-12",
        ":db/id": 17592186232246
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "d447476e-6786-52c0-9a5b-aa6aa6b42f96",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-12",
      ":db/id": 17592186232246
    },
    ":answer-field/id": "e6f81397-282c-55bf-a574-31b7a7eb6872",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232245
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "e0d9ee9f-e333-5485-a7ba-ff333f3a6931",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "600",
        ":db/id": 17592186232248
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "e0d9ee9f-e333-5485-a7ba-ff333f3a6931",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "600",
      ":db/id": 17592186232248
    },
    ":answer-field/id": "e81a89a6-5e45-5c38-944f-815f8eebc873",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232247
  }
]
```

```text
We have the following system of linear equations:

$$
{\begin{aligned}b=480-10a \\ 20b+400a=7\,200\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=480-10a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}20b+400a & =7\,200 \\ 20(480-10a)+400a & =7\,200 \\ 9\,600-200a+400a & =7\,200 \\ 9\,600+200a & =7\,200 \\ 200a & =-2\,400 \\ a & =-12\end{aligned}
$$

If we now substitute $a=-12$ into $b=480-10a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =480-10(-12) \\ b & =600\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-12,\,b=600.$
```

## Supported replay q-167194

The coefficients $a$ and $b$ also satisfy the equation $20b+400a=7\,200.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

```json
[
  {
    ":answer-field/id": "88248dd5-dcc4-56bc-8293-c815433e9c38",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "5b750f7a-2efc-53e3-a0df-f5f561e3ee70",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-12"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "5b750f7a-2efc-53e3-a0df-f5f561e3ee70"
    ]
  },
  {
    ":answer-field/id": "afb96b7d-7975-54e2-b947-829e204fcfcb",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "6f094dd9-c2bb-5ac3-984a-bbb157f804f0",
        ":answer/type": ":answer.type/math",
        ":answer/value": "600"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "6f094dd9-c2bb-5ac3-984a-bbb157f804f0"
    ]
  }
]
```

We have the following system of linear equations:

$$
\left\{\begin{aligned}b &=480-10a \\ 20b+400a &=7\,200\end{aligned}\right.
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=480-10a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}20b+400a & =7\,200 \\ 20(480-10a)+400a & =7\,200 \\ 9\,600-200a+400a & =7\,200 \\ 9\,600+200a & =7\,200 \\ 200a & =-2\,400 \\ a & =-12\end{aligned}
$$

If we now substitute $a=-12$ into $b=480-10a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =480-10(-12) \\ b & =600\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-12,\,b=600.$

## Original q-167210

```text
The coefficients $a$ and $b$ also satisfy the equation $30b+900a=6\,000.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}
```

Captured answer fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "25f6ebe2-11a4-50a4-afb6-e54166d6b757",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-4",
        ":db/id": 17592186232262
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "25f6ebe2-11a4-50a4-afb6-e54166d6b757",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-4",
      ":db/id": 17592186232262
    },
    ":answer-field/id": "d89c06a2-d40d-59be-aba2-b51cfcb77eb2",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232261
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "81d5e96b-1699-54bb-87d3-abe3b34a48dc",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "320",
        ":db/id": 17592186232264
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "81d5e96b-1699-54bb-87d3-abe3b34a48dc",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "320",
      ":db/id": 17592186232264
    },
    ":answer-field/id": "80788b1d-1ccd-5c42-ae32-41ab3f383746",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232263
  }
]
```

```text
We have the following system of linear equations:

$$
{\begin{aligned}b=240-20a \\ 30b+900a=6\,000\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=240-20a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}30b+900a & =6\,000 \\ 30(240-20a)+900a & =6\,000 \\ 7\,200-600a+900a & =6\,000 \\ 7\,200+300a & =6\,000 \\ 300a & =-1\,200 \\ a & =-4\end{aligned}
$$

If we now substitute $a=-4$ into $b=240-20a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =240-20(-4) \\ b & =320\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-4,\,b=320.$
```

## Supported replay q-167210

The coefficients $a$ and $b$ also satisfy the equation $30b+900a=6\,000.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

```json
[
  {
    ":answer-field/id": "b83da9ad-697f-5630-8f5d-bf30387270df",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "e6241d80-de68-54a6-b0d3-b874533b5167",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-4"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "e6241d80-de68-54a6-b0d3-b874533b5167"
    ]
  },
  {
    ":answer-field/id": "dfe40e68-0fd9-5cbd-b9a8-52a4ed875cef",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "021e02c0-b054-5726-954f-c54653151d8c",
        ":answer/type": ":answer.type/math",
        ":answer/value": "320"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "021e02c0-b054-5726-954f-c54653151d8c"
    ]
  }
]
```

We have the following system of linear equations:

$$
\left\{\begin{aligned}b &=240-20a \\ 30b+900a &=6\,000\end{aligned}\right.
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=240-20a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}30b+900a & =6\,000 \\ 30(240-20a)+900a & =6\,000 \\ 7\,200-600a+900a & =6\,000 \\ 7\,200+300a & =6\,000 \\ 300a & =-1\,200 \\ a & =-4\end{aligned}
$$

If we now substitute $a=-4$ into $b=240-20a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =240-20(-4) \\ b & =320\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-4,\,b=320.$

## Original q-167226

```text
The coefficients $a$ and $b$ also satisfy the equation $70a+9b=600.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}
```

Captured answer fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "74b8ef99-22cc-5e49-9884-ae62824c5059",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-3",
        ":db/id": 17592186232278
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "74b8ef99-22cc-5e49-9884-ae62824c5059",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-3",
      ":db/id": 17592186232278
    },
    ":answer-field/id": "194751b6-0ff6-5047-a6e8-f7e3cfbe1451",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232277
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "39731897-add5-5068-a83a-649fb0aa6e48",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "90",
        ":db/id": 17592186232280
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "39731897-add5-5068-a83a-649fb0aa6e48",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "90",
      ":db/id": 17592186232280
    },
    ":answer-field/id": "03a21b91-803e-51b3-8b0d-859c1f623d17",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186232279
  }
]
```

```text
We have the following system of linear equations:

$$
{\begin{aligned}b=75-5a \\ 70a+9b=600\end{aligned}
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=75-5a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}70a+9b & =600 \\ 70a+9(75-5a) & =600 \\ 70a+675-45a & =600 \\ 25a+675 & =600 \\ 25a & =-75 \\ a & =-3\end{aligned}
$$

If we now substitute $a=-3$ into $b=75-5a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =75-5(-3) \\ b & =90\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-3,\,b=90.$
```

## Supported replay q-167226

The coefficients $a$ and $b$ also satisfy the equation $70a+9b=600.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

```json
[
  {
    ":answer-field/id": "f1e5b85c-d2c0-5699-9acb-3f89f9ed64e4",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "fc8e6765-67ac-5da5-af9a-90347c7015a4",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "fc8e6765-67ac-5da5-af9a-90347c7015a4"
    ]
  },
  {
    ":answer-field/id": "28358181-743b-55c3-a9e5-42748570b39a",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "d74a5d51-a0bc-5b32-a2c4-87017b67f258",
        ":answer/type": ":answer.type/math",
        ":answer/value": "90"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "d74a5d51-a0bc-5b32-a2c4-87017b67f258"
    ]
  }
]
```

We have the following system of linear equations:

$$
\left\{\begin{aligned}b &=75-5a \\ 70a+9b &=600\end{aligned}\right.
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=75-5a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}70a+9b & =600 \\ 70a+9(75-5a) & =600 \\ 70a+675-45a & =600 \\ 25a+675 & =600 \\ 25a & =-75 \\ a & =-3\end{aligned}
$$

If we now substitute $a=-3$ into $b=75-5a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =75-5(-3) \\ b & =90\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-3,\,b=90.$

## Original q-181149

```text
Consider the following system of equations:

$$
\{\begin{aligned}4u-6v=-3 \\ u=-v-2\end{aligned}
$$

Find the solution $(u,v)$ to this system using the method of substitution.

$(u,v)=($
{{field-1}}
$,$
{{field-2}}
$)$
```

Captured answer fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "51c5dada-d996-51cf-94d1-ca897ceda4c8",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{1}{2}",
        ":db/id": 17592186495696
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "51c5dada-d996-51cf-94d1-ca897ceda4c8",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-\\frac{1}{2}",
      ":db/id": 17592186495696
    },
    ":answer-field/id": "da300820-d65a-54b5-a122-648e1be4ca42",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186496194
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "0db68d80-560b-5294-a3e9-812966c11801",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "-\\frac{3}{2}",
        ":db/id": 17592186495542
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "0db68d80-560b-5294-a3e9-812966c11801",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "-\\frac{3}{2}",
      ":db/id": 17592186495542
    },
    ":answer-field/id": "e16e42d5-5e57-5702-bb36-98fb0bad0dd6",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186496198
  }
]
```

```text
We will isolate a variable in one of the equations and then substitute it into the other equation. It so happens that the second equation is already solved for $u:$

$$
u=-v-2
$$

So, we replace $u$ with $-v-2$ in the first equation and solve for $v:$

$$
\begin{aligned}4u-6v & =-3 \\ 4(-v-2)-6v & =-3 \\ -4v-8-6v & =-3 \\ -10v & =5 \\ v & =-\frac{1}{2}\end{aligned}
$$

If we now substitute $v=-\frac{1}{2}$ into $u=-v-2,$ then we can find the value of $u:$

$$
\begin{aligned}u & =-v-2 \\ u & =-(-\frac{1}{2})-2 \\ u & =-\frac{3}{2}\end{aligned}
$$

Therefore, the solution to the system of equations is $u=-\frac{3}{2},\,v=-\frac{1}{2},$ which can be expressed as $(-\frac{3}{2},-\frac{1}{2}).$
```

## Supported replay q-181149

Consider the following system of equations:

$$
\left\{\begin{aligned}4u-6v &=-3 \\ u &=-v-2\end{aligned}\right.
$$

Find the solution $(u,v)$ to this system using the method of substitution.

$(u,v)=($
{{field-1}}
$,$
{{field-2}}
$)$

```json
[
  {
    ":answer-field/id": "24371384-a3f6-5d45-9c76-5d62d71a2ffc",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "d945dffb-c13b-5701-a4a8-ad7c4b3ff241",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-\\frac{3}{2}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "d945dffb-c13b-5701-a4a8-ad7c4b3ff241"
    ]
  },
  {
    ":answer-field/id": "a5661be3-3e1c-5a21-84f4-0da51e30c4db",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "29460352-350a-504d-9dc4-c8f6d68d7a4a",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-\\frac{1}{2}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "29460352-350a-504d-9dc4-c8f6d68d7a4a"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. It so happens that the second equation is already solved for $u:$

$$
u=-v-2
$$

So, we replace $u$ with $-v-2$ in the first equation and solve for $v:$

$$
\begin{aligned}4u-6v & =-3 \\ 4(-v-2)-6v & =-3 \\ -4v-8-6v & =-3 \\ -10v & =5 \\ v & =-\frac{1}{2}\end{aligned}
$$

If we now substitute $v=-\frac{1}{2}$ into $u=-v-2,$ then we can find the value of $u:$

$$
\begin{aligned}u & =-v-2 \\ u & =-(-\frac{1}{2})-2 \\ u & =-\frac{3}{2}\end{aligned}
$$

Therefore, the solution to the system of equations is $u=-\frac{3}{2},\,v=-\frac{1}{2},$ which can be expressed as $(-\frac{3}{2},-\frac{1}{2}).$

## Original q-181175

```text
Consider the following system of equations:

$$
\{\begin{aligned}-2x+y=-4 \\ x-3y=-8\end{aligned}
$$

Find the solution $(x,y)$ to this system using the method of substitution.

$(x,y)=($
{{field-1}}
$,$
{{field-2}}
$)$
```

Captured answer fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "001fa025-6178-5ba4-b287-f99d23255489",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "4",
        ":db/id": 17592186495509
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "001fa025-6178-5ba4-b287-f99d23255489",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "4",
      ":db/id": 17592186495509
    },
    ":answer-field/id": "7c44ea3f-ae01-5f06-b1d9-d8a1d677d43e",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186496138
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "e2cf528e-9238-53c7-ac72-2595f6c61117",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "4",
        ":db/id": 17592186496013
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "e2cf528e-9238-53c7-ac72-2595f6c61117",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "4",
      ":db/id": 17592186496013
    },
    ":answer-field/id": "d81fe473-caed-55d0-ae06-56890f9a6929",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186496191
  }
]
```

```text
We will isolate a variable in one of the equations and then substitute it into the other equation. It doesn't matter which equation we pick first, so we choose the easiest one. In this case, the second equation looks like the easiest.

Using the second equation, we can isolate $x$ by adding $3y$ from both sides of the equation:

$$
x=3y-8
$$

So, we replace $x$ with $3y-8$ in the first equation and solve for $y:$

$$
\begin{aligned}-2x+y & =-4 \\ -2(3y-8)+y & =-4 \\ -6y+16+y & =-4 \\ -5y & =-20 \\ y & =4\end{aligned}
$$

If we now substitute $y=4$ into $x=3y-8,$ then we can find the value of $x:$

$$
\begin{aligned}x & =3y-8 \\ x & =3(4)-8 \\ x & =12-8 \\ x & =4\end{aligned}
$$

Therefore, the solution to the system of equations is $x=4,\,y=4,$ which can be expressed as $(4,4).$
```

## Supported replay q-181175

Consider the following system of equations:

$$
\left\{\begin{aligned}-2x+y &=-4 \\ x-3y &=-8\end{aligned}\right.
$$

Find the solution $(x,y)$ to this system using the method of substitution.

$(x,y)=($
{{field-1}}
$,$
{{field-2}}
$)$

```json
[
  {
    ":answer-field/id": "b19e1ebc-9737-55e3-bf4a-6e84a056104e",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "8e4e25a5-4054-5ba2-892e-b0367ff037ac",
        ":answer/type": ":answer.type/math",
        ":answer/value": "4"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "8e4e25a5-4054-5ba2-892e-b0367ff037ac"
    ]
  },
  {
    ":answer-field/id": "898d6ca6-1643-5b6a-9816-790defcc3824",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "7eb36f4f-0ccf-59fc-9f92-c0983280688c",
        ":answer/type": ":answer.type/math",
        ":answer/value": "4"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "7eb36f4f-0ccf-59fc-9f92-c0983280688c"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. It doesn't matter which equation we pick first, so we choose the easiest one. In this case, the second equation looks like the easiest.

Using the second equation, we can isolate $x$ by adding $3y$ from both sides of the equation:

$$
x=3y-8
$$

So, we replace $x$ with $3y-8$ in the first equation and solve for $y:$

$$
\begin{aligned}-2x+y & =-4 \\ -2(3y-8)+y & =-4 \\ -6y+16+y & =-4 \\ -5y & =-20 \\ y & =4\end{aligned}
$$

If we now substitute $y=4$ into $x=3y-8,$ then we can find the value of $x:$

$$
\begin{aligned}x & =3y-8 \\ x & =3(4)-8 \\ x & =12-8 \\ x & =4\end{aligned}
$$

Therefore, the solution to the system of equations is $x=4,\,y=4,$ which can be expressed as $(4,4).$

## Original q-166843

```text
The pastry shop's total cost and revenue per month (in dollars) from selling cakes can be modeled by the equations $y=1\,600+5n$ and $y=64+17n,$ respectively, where $n$ is the number of cakes sold. 

Solve the system below using the substitution method to find the exact number of cakes needed to break even and the revenue made.

$$
\{\begin{aligned}y=1\,600+5n \\ y=64+17n\end{aligned}
$$

The pastry shop breaks even when$\,$
{{field-1}}
$\,$cakes are produced. 

The revenue made when selling this number of cakes is$\,$
{{field-2}}
$\,$dollars.
```

Captured answer fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "951ed025-e4b5-517b-830a-a3da54b9c6e7",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "128",
        ":db/id": 17592186496968
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "951ed025-e4b5-517b-830a-a3da54b9c6e7",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "128",
      ":db/id": 17592186496968
    },
    ":answer-field/id": "1c523c48-ec60-5fa0-9eec-5d07498f1571",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186497224
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "eebbe5cc-91ee-5b03-9257-cc5f956ce523",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "2240",
        ":db/id": 17592186497171
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "eebbe5cc-91ee-5b03-9257-cc5f956ce523",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "2240",
      ":db/id": 17592186497171
    },
    ":answer-field/id": "fb7943f0-b18a-5a1c-9e1c-77a8a3b53234",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186497319
  }
]
```

```text
We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that $y$ is isolated in the first equation. Therefore, we can replace $y$ with $1\,600+5n$ in the second equation and solve for $n:$

$$
\begin{aligned}y & =64+17n \\ 1\,600+5n & =64+17n \\ 1\,600+5n-64 & =64+17n-64 \\ 1\,536+5n & =17n \\ 1\,536+5n-5n & =17n-5n \\ 1\,536 & =12n \\ \frac{1\,536}{12} & =\frac{12n}{12} \\ 128 & =n \\ n & =128\end{aligned}
$$

If we now substitute $n=128$ into $y=64+17n$, then we can find the value of $y:$

$$
\begin{aligned}y=64+17(128)=2\,240\end{aligned}
$$

Hence, the solution to the system of equations is $n=128$ and $y=2\,240.$
Therefore, the pastry shop breaks even when $128$ units are produced, and the revenue made when selling this number of units is $$2\,240.$
```

## Supported replay q-166843

The pastry shop's total cost and revenue per month (in dollars) from selling cakes can be modeled by the equations $y=1\,600+5n$ and $y=64+17n,$ respectively, where $n$ is the number of cakes sold. 

Solve the system below using the substitution method to find the exact number of cakes needed to break even and the revenue made.

$$
\left\{\begin{aligned}y &=1\,600+5n \\ y &=64+17n\end{aligned}\right.
$$

The pastry shop breaks even when$\,$
{{field-1}}
$\,$cakes are produced. 

The revenue made when selling this number of cakes is$\,$
{{field-2}}
$\,$dollars.

```json
[
  {
    ":answer-field/id": "b43b5109-d13d-56c6-9e20-ae4fdf864ab3",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "3d7274d9-440c-559f-a566-07b186cb907c",
        ":answer/type": ":answer.type/math",
        ":answer/value": "128"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "3d7274d9-440c-559f-a566-07b186cb907c"
    ]
  },
  {
    ":answer-field/id": "5d06792c-7a43-5ac7-b604-e6be1d88c76c",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "98fb35e2-69ea-5fe0-b7dc-5efff36830c7",
        ":answer/type": ":answer.type/math",
        ":answer/value": "2240"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "98fb35e2-69ea-5fe0-b7dc-5efff36830c7"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that $y$ is isolated in the first equation. Therefore, we can replace $y$ with $1\,600+5n$ in the second equation and solve for $n:$

$$
\begin{aligned}y & =64+17n \\ 1\,600+5n & =64+17n \\ 1\,600+5n-64 & =64+17n-64 \\ 1\,536+5n & =17n \\ 1\,536+5n-5n & =17n-5n \\ 1\,536 & =12n \\ \frac{1\,536}{12} & =\frac{12n}{12} \\ 128 & =n \\ n & =128\end{aligned}
$$

If we now substitute $n=128$ into $y=64+17n$, then we can find the value of $y:$

$$
\begin{aligned}y &=64+17(128)=2\,240\end{aligned}
$$

Hence, the solution to the system of equations is $n=128$ and $y=2\,240.$
Therefore, the pastry shop breaks even when $128$ units are produced, and the revenue made when selling this number of units is $2\,240.$

## Original q-166761

```text
Mary wonders where and when they'd meet if Sam left home $3.8$ minutes earlier and walked with a speed of $50$ meters per minute. She finds that the distance $d$ from home they'd meet can be modeled using the following system of equations.

$$
\{\begin{aligned}d+60t=960 \\ d-50t=190.\end{aligned}
$$

where $t$ is the time (in minutes) since Mary left the community park.

Mary and Sam would meet$\,$
{{field-1}}$\,$minutes after Mary left the community park.

Mary and Sam would meet at a distance of $\,$
{{field-2}}$\,$meters from home.
```

Captured answer fields:
```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "1e2466bb-be73-57a5-a448-e2ae0ba60c2d",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "7",
        ":db/id": 17592186503039
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "1e2466bb-be73-57a5-a448-e2ae0ba60c2d",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "7",
      ":db/id": 17592186503039
    },
    ":answer-field/id": "163d9f6a-4519-5200-83a3-6d401cb44c91",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186503523
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "13a5bcc9-bf29-57f7-9c4f-15fe366965e6",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "540",
        ":db/id": 17592186503022
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "13a5bcc9-bf29-57f7-9c4f-15fe366965e6",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "540",
      ":db/id": 17592186503022
    },
    ":answer-field/id": "5d99e451-ff6c-54c5-be9e-d8c096902ab9",
    ":answer-field/key": "field-2",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186503554
  }
]
```

```text
To solve the given system of linear equations, we will isolate a variable in one of the equations and then substitute it into the other equation. It doesn't matter which equation we pick first, so we choose the easiest one. In this case, the second equation looks like the easiest.

Using the second equation, we can isolate $d$ adding to both sides of the equation $50t:$

$$
\begin{aligned}d-50t=190 \\ d=190+50t\end{aligned}
$$

So, we replace $d$ with $190+50t$ in the first equation and solve for $t:$

$$
\begin{aligned}d+60t=960 \\ (190+50t)+60t & =960 \\ 190+110t & =960 \\ 110t & =960-190 \\ 110t & =770 \\ t & =\frac{770}{110} \\ t & =7.\end{aligned}
$$

Therefore, they would have met after $t=7$ minutes.

If we substitute $t=7$ into $d=190+50t$, we can find the value of $d:$

$$
\begin{aligned}d & =190+50t \\  & =190+50(7) \\  & =540\end{aligned}
$$

Therefore, they meet at a distance of $540$ meters from home.
```

## Supported replay q-166761

Mary wonders where and when they'd meet if Sam left home $3.8$ minutes earlier and walked with a speed of $50$ meters per minute. She finds that the distance $d$ from home they'd meet can be modeled using the following system of equations.

$$
\left\{\begin{aligned}d+60t &=960 \\ d-50t &=190.\end{aligned}\right.
$$

where $t$ is the time (in minutes) since Mary left the community park.

Mary and Sam would meet$\,$
{{field-1}}$\,$minutes after Mary left the community park.

Mary and Sam would meet at a distance of $\,$
{{field-2}}$\,$meters from home.

```json
[
  {
    ":answer-field/id": "72c55d14-fd00-5c9c-b8e9-15ba81eb8c16",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "8c2e6daa-8b6b-51df-90d5-7da0ce0ba637",
        ":answer/type": ":answer.type/math",
        ":answer/value": "7"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "8c2e6daa-8b6b-51df-90d5-7da0ce0ba637"
    ]
  },
  {
    ":answer-field/id": "7ea3b7b9-8ed4-59ff-923e-67b82330e4d4",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "2f6a97a1-7982-5b09-9345-72306a915a34",
        ":answer/type": ":answer.type/math",
        ":answer/value": "540"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "2f6a97a1-7982-5b09-9345-72306a915a34"
    ]
  }
]
```

To solve the given system of linear equations, we will isolate a variable in one of the equations and then substitute it into the other equation. It doesn't matter which equation we pick first, so we choose the easiest one. In this case, the second equation looks like the easiest.

Using the second equation, we can isolate $d$ adding to both sides of the equation $50t:$

$$
\begin{aligned}d-50t & =190 \\ d & =190+50t\end{aligned}
$$

So, we replace $d$ with $190+50t$ in the first equation and solve for $t:$

$$
\begin{aligned}d+60t & =960 \\ (190+50t)+60t & =960 \\ 190+110t & =960 \\ 110t & =960-190 \\ 110t & =770 \\ t & =\frac{770}{110} \\ t & =7.\end{aligned}
$$

Therefore, they would have met after $t=7$ minutes.

If we substitute $t=7$ into $d=190+50t$, we can find the value of $d:$

$$
\begin{aligned}d & =190+50t \\  & =190+50(7) \\  & =540\end{aligned}
$$

Therefore, they meet at a distance of $540$ meters from home.

## Variant coefficient_b_first 0

The coefficients $a$ and $b$ satisfy $b=180-15a.$

The coefficients $a$ and $b$ also satisfy the equation $3b+95a=90.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

```json
[
  {
    ":answer-field/id": "0af1552d-0375-55a3-89af-798e67ee2e8b",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "d1359401-b9f7-5351-ab69-c82607555f1a",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "d1359401-b9f7-5351-ab69-c82607555f1a"
    ]
  },
  {
    ":answer-field/id": "36fb9f54-c247-582e-9d2f-1eea7ffa3741",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "f2c22500-9066-5932-99b0-2d22c41b60d1",
        ":answer/type": ":answer.type/math",
        ":answer/value": "315"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "f2c22500-9066-5932-99b0-2d22c41b60d1"
    ]
  }
]
```

We have the following system of linear equations:

$$
\left\{\begin{aligned}b &=180-15a \\ 3b+95a &=90\end{aligned}\right.
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=180-15a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}3b+95a & =90 \\ 3(180-15a)+95a & =90 \\ 540-45a+95a & =90 \\ 540+50a & =90 \\ 50a & =-450 \\ a & =-9\end{aligned}
$$

If we now substitute $a=-9$ into $b=180-15a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =180-15(-9) \\ b & =315\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-9,\,b=315.$

## Variant coefficient_b_first 1

The coefficients $a$ and $b$ satisfy $b=100-20a.$

The coefficients $a$ and $b$ also satisfy the equation $29b+600a=2\,800.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

```json
[
  {
    ":answer-field/id": "9eb44c0f-1fe5-5bd4-ab47-0b6e2fa7988d",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "d0b6e404-e233-5211-943f-bb312b518d44",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-5"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "d0b6e404-e233-5211-943f-bb312b518d44"
    ]
  },
  {
    ":answer-field/id": "bf3b0a1c-5c05-58d8-8210-e24cad551fff",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "e2cff01b-78ae-5113-877b-6d1fc6122629",
        ":answer/type": ":answer.type/math",
        ":answer/value": "200"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "e2cff01b-78ae-5113-877b-6d1fc6122629"
    ]
  }
]
```

We have the following system of linear equations:

$$
\left\{\begin{aligned}b &=100-20a \\ 29b+600a &=2\,800\end{aligned}\right.
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=100-20a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}29b+600a & =2\,800 \\ 29(100-20a)+600a & =2\,800 \\ 2\,900-580a+600a & =2\,800 \\ 2\,900+20a & =2\,800 \\ 20a & =-100 \\ a & =-5\end{aligned}
$$

If we now substitute $a=-5$ into $b=100-20a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =100-20(-5) \\ b & =200\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-5,\,b=200.$

## Variant coefficient_a_first 0

The coefficients $a$ and $b$ satisfy $b=180-15a.$

The coefficients $a$ and $b$ also satisfy the equation $95a+3b=90.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

```json
[
  {
    ":answer-field/id": "9aff6bb2-2f15-500b-99a0-5aa6b4dba2c4",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "1405bcf5-10f0-5223-9618-85c6033f8124",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "1405bcf5-10f0-5223-9618-85c6033f8124"
    ]
  },
  {
    ":answer-field/id": "8a06d32f-3b2e-5667-9ac7-16d21a09cf86",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "a61f46b2-01d4-5592-a583-99b4df0e68f0",
        ":answer/type": ":answer.type/math",
        ":answer/value": "315"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "a61f46b2-01d4-5592-a583-99b4df0e68f0"
    ]
  }
]
```

We have the following system of linear equations:

$$
\left\{\begin{aligned}b &=180-15a \\ 95a+3b &=90\end{aligned}\right.
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=180-15a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}95a+3b & =90 \\ 95a+3(180-15a) & =90 \\ 95a+540-45a & =90 \\ 50a+540 & =90 \\ 50a & =-450 \\ a & =-9\end{aligned}
$$

If we now substitute $a=-9$ into $b=180-15a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =180-15(-9) \\ b & =315\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-9,\,b=315.$

## Variant coefficient_a_first 1

The coefficients $a$ and $b$ satisfy $b=100-20a.$

The coefficients $a$ and $b$ also satisfy the equation $600a+29b=2\,800.$ Find the values of $a$ and $b.$

$a\,=$
{{field-1}}

$b\,=$
{{field-2}}

```json
[
  {
    ":answer-field/id": "9e26ddee-47f0-5391-9df8-236e76f9d03e",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "027e46c4-2779-5647-aee9-3e589f8ee690",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-5"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "027e46c4-2779-5647-aee9-3e589f8ee690"
    ]
  },
  {
    ":answer-field/id": "63c3c8fd-60f0-59d0-b988-6eceddfd2235",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "9f95f204-adcd-572a-8305-5c1b9bfed765",
        ":answer/type": ":answer.type/math",
        ":answer/value": "200"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "9f95f204-adcd-572a-8305-5c1b9bfed765"
    ]
  }
]
```

We have the following system of linear equations:

$$
\left\{\begin{aligned}b &=100-20a \\ 600a+29b &=2\,800\end{aligned}\right.
$$

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the first equation is already solved for $b:$

$$
b=100-20a
$$

So, we replace $b$ in the second equation and solve for $a:$

$$
\begin{aligned}600a+29b & =2\,800 \\ 600a+29(100-20a) & =2\,800 \\ 600a+2\,900-580a & =2\,800 \\ 20a+2\,900 & =2\,800 \\ 20a & =-100 \\ a & =-5\end{aligned}
$$

If we now substitute $a=-5$ into $b=100-20a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =100-20(-5) \\ b & =200\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-5,\,b=200.$

## Variant tuple_xy 0

Consider the following system of equations:
$$
\left\{\begin{aligned}x+5y &=-10 \\ y &=x-8\end{aligned}\right.
$$
Find the solution $(x, y)$ to this system using the method of substitution.The solution is
$($
{{field-1}}
$,$
{{field-2}}
$)$

```json
[
  {
    ":answer-field/id": "ab798331-674e-5382-b326-4281bc5a650e",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "14164a7d-bf01-5832-82f9-e695632a04db",
        ":answer/type": ":answer.type/math",
        ":answer/value": "5"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "14164a7d-bf01-5832-82f9-e695632a04db"
    ]
  },
  {
    ":answer-field/id": "b0348b72-f25a-5af6-8193-9ccd47fb3cdf",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "e5a703c3-b6dc-5de7-b88f-c11542f47bc7",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "e5a703c3-b6dc-5de7-b88f-c11542f47bc7"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the second equation is already solved for $y:$

$$
y=x-8
$$

So, we replace $y$ in the first equation and solve for $x:$

$$
\begin{aligned}x+5y & =-10 \\ x+5(x-8) & =-10 \\ x+5x-40 & =-10 \\ 6x-40 & =-10 \\ 6x & =30 \\ x & =5\end{aligned}
$$

If we now substitute $x=5$ into $y=x-8,$ we can then find the value of $y:$

$$
\begin{aligned}y & =(5)-8 \\ y & =-3\end{aligned}
$$

Therefore, the solution to the system of equations is $x=5,\,y=-3.$

## Variant tuple_xy 1

Consider the following system of equations:
$$
\left\{\begin{aligned}x+3y &=-33 \\ y &=x-3\end{aligned}\right.
$$
Find the solution $(x, y)$ to this system using the method of substitution.The solution is
$($
{{field-1}}
$,$
{{field-2}}
$)$

```json
[
  {
    ":answer-field/id": "057ade19-4fc8-5b49-9593-8b83d0550057",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "611729c0-7c6e-5499-a08c-acbfc57982e0",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-6"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "611729c0-7c6e-5499-a08c-acbfc57982e0"
    ]
  },
  {
    ":answer-field/id": "4c0043a4-694b-5e41-804d-102226d7cb29",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "f466d7b3-19f5-5a10-8d17-5bddb198e127",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "f466d7b3-19f5-5a10-8d17-5bddb198e127"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that the second equation is already solved for $y:$

$$
y=x-3
$$

So, we replace $y$ in the first equation and solve for $x:$

$$
\begin{aligned}x+3y & =-33 \\ x+3(x-3) & =-33 \\ x+3x-9 & =-33 \\ 4x-9 & =-33 \\ 4x & =-24 \\ x & =-6\end{aligned}
$$

If we now substitute $x=-6$ into $y=x-3,$ we can then find the value of $y:$

$$
\begin{aligned}y & =(-6)-3 \\ y & =-9\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-6,\,y=-9.$

## Variant direct_pq 0

Given the system of equations below, what is the value of $q - p$?

$$
\left\{\begin{aligned}4p &=24 \\ p+5q &=-29\end{aligned}\right.
$$

```json
[
  {
    ":answer-field/id": "820a3f92-d989-5d83-bbab-c0dc3612046b",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "0bafb94a-7ac5-5d59-8667-fe8857e443cc",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-13"
      },
      {
        ":answer/id": "19b9a513-fe95-5465-b7aa-8a1358e3a186",
        ":answer/type": ":answer.type/math",
        ":answer/value": "13"
      },
      {
        ":answer/id": "f611a2b3-ec37-5012-9710-1729f4879461",
        ":answer/type": ":answer.type/math",
        ":answer/value": "6"
      },
      {
        ":answer/id": "41410809-9adf-5820-bf7b-27a47533b255",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1"
      },
      {
        ":answer/id": "ee8dc6cb-ed22-5089-9c1a-4b70d5bf14ee",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-7"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "0bafb94a-7ac5-5d59-8667-fe8857e443cc"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the first equation, we can isolate $p$ by dividing both sides by $4:$

$$
\begin{aligned}4p & =24 \\ p & =6\end{aligned}
$$

Then, we substitute $p=6$ into the second equation and solve for $q:$

$$
\begin{aligned}p+5q & =-29 \\ (6)+5q & =-29 \\ 5q & =-35 \\ q & =-7\end{aligned}
$$

Therefore, $q-p=-7-(6)=-13.$

## Variant direct_pq 1

Given the system of equations below, what is the value of $p - q$?

$$
\left\{\begin{aligned}2p &=-12 \\ p+5q &=-1\end{aligned}\right.
$$

```json
[
  {
    ":answer-field/id": "22d24da1-be44-57b9-9bc5-67375f2726ae",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "4a4a3252-7312-510e-a919-2c080eee137a",
        ":answer/type": ":answer.type/math",
        ":answer/value": "7"
      },
      {
        ":answer/id": "388ba7e1-caea-50d0-8ae6-5f932e139382",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-7"
      },
      {
        ":answer/id": "37d038e9-decd-5dae-be91-39909dc567db",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-6"
      },
      {
        ":answer/id": "90146c7d-30a5-5775-aaa9-d96e347e87f5",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-5"
      },
      {
        ":answer/id": "a88cb29c-e6df-57f7-9d61-be99ffd891fc",
        ":answer/type": ":answer.type/math",
        ":answer/value": "1"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "388ba7e1-caea-50d0-8ae6-5f932e139382"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the first equation, we can isolate $p$ by dividing both sides by $2:$

$$
\begin{aligned}2p & =-12 \\ p & =-6\end{aligned}
$$

Then, we substitute $p=-6$ into the second equation and solve for $q:$

$$
\begin{aligned}p+5q & =-1 \\ (-6)+5q & =-1 \\ 5q & =5 \\ q & =1\end{aligned}
$$

Therefore, $p-q=-6-(1)=-7.$

## Variant difference_ab 0

Given the system of equations below, what is the value of $b - a$?

$$
\left\{\begin{aligned}2a-4b &=-26 \\ -2a+b &=8\end{aligned}\right.
$$

```json
[
  {
    ":answer-field/id": "8287df2d-8906-5d88-9abb-bd32f4a05369",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "9a9d95de-295c-561a-b7ad-a9d3fded0f35",
        ":answer/type": ":answer.type/math",
        ":answer/value": "7"
      },
      {
        ":answer/id": "e9234b40-fc35-50e8-9e69-21392d342e1b",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-7"
      },
      {
        ":answer/id": "227a079d-b837-517a-a7c5-460c4ba1cc2a",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1"
      },
      {
        ":answer/id": "8560a8bb-2bca-5e4f-ace9-bf6590238dbc",
        ":answer/type": ":answer.type/math",
        ":answer/value": "5"
      },
      {
        ":answer/id": "6a7fccb4-ffa2-5bf8-9b57-6886b2ded9a9",
        ":answer/type": ":answer.type/math",
        ":answer/value": "6"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "9a9d95de-295c-561a-b7ad-a9d3fded0f35"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the second equation, we can isolate $b$:

$$
\begin{aligned}-2a+b & =8 \\ b & =8+2a\end{aligned}
$$

Then, we substitute $b=8+2a$ into the first equation and solve for $a:$

$$
\begin{aligned}2a-4b & =-26 \\ 2a-4(8+2a) & =-26 \\ 2a-32-8a & =-26 \\ -6a-32 & =-26 \\ -6a & =6 \\ a & =-1\end{aligned}
$$

If we now substitute $a=-1$ into $b=8+2a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =8+2(-1) \\ b & =6\end{aligned}
$$

Therefore, $b-a=6-(-1)=7.$

## Variant difference_ab 1

Given the system of equations below, what is the value of $a - b$?

$$
\left\{\begin{aligned}3a-4b &=15 \\ -2a+b &=-5\end{aligned}\right.
$$

```json
[
  {
    ":answer-field/id": "00f318b0-27af-5398-90eb-aed6c59f28fa",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "dd5999b6-1e01-58cf-bfd1-f5df00d4d79a",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-4"
      },
      {
        ":answer/id": "e25bcb81-bbee-5d5f-bd00-46ddcc793210",
        ":answer/type": ":answer.type/math",
        ":answer/value": "4"
      },
      {
        ":answer/id": "a75f2aa5-0217-5ba7-ab6c-7e49e9f063a0",
        ":answer/type": ":answer.type/math",
        ":answer/value": "1"
      },
      {
        ":answer/id": "a5faddb6-ff43-5c61-ad03-a7229dfa4081",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-2"
      },
      {
        ":answer/id": "97126f49-d264-52a0-a60a-70f00f2302bb",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "e25bcb81-bbee-5d5f-bd00-46ddcc793210"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the second equation, we can isolate $b$:

$$
\begin{aligned}-2a+b & =-5 \\ b & =-5+2a\end{aligned}
$$

Then, we substitute $b=-5+2a$ into the first equation and solve for $a:$

$$
\begin{aligned}3a-4b & =15 \\ 3a-4(-5+2a) & =15 \\ 3a+20-8a & =15 \\ -5a+20 & =15 \\ -5a & =-5 \\ a & =1\end{aligned}
$$

If we now substitute $a=1$ into $b=-5+2a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =-5+2(1) \\ b & =-3\end{aligned}
$$

Therefore, $a-b=1-(-3)=4.$

## Variant unit_pair 0

Find the solution $(x,y)$ to this system using the method of substitution.

$$
\left\{\begin{aligned}-2x+3y &=-6 \\ 4x+y &=-4\end{aligned}\right.
$$

The solution is $($ {{field-1}} $,$ {{field-2}} $)$

```json
[
  {
    ":answer-field/id": "f7783438-9acf-5af8-a159-e318163d97fa",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "a082636b-7946-55ff-8426-3f38fb362cb0",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-\\frac{3}{7}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "a082636b-7946-55ff-8426-3f38fb362cb0"
    ]
  },
  {
    ":answer-field/id": "f92baf97-530f-5ef7-8718-557cbf1f2bfa",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "6c46e4e7-acc5-57d4-a4fc-a6d856063d9e",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-\\frac{16}{7}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "6c46e4e7-acc5-57d4-a4fc-a6d856063d9e"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the second equation, we can isolate $y$:

$$
\begin{aligned}4x+y & =-4 \\ y & =-4-4x\end{aligned}
$$

Then, we substitute $y=-4-4x$ into the first equation and solve for $x:$

$$
\begin{aligned}-2x+3y & =-6 \\ -2x+3(-4-4x) & =-6 \\ -2x-12-12x & =-6 \\ -14x-12 & =-6 \\ -14x & =6 \\ x & =-\frac{3}{7}\end{aligned}
$$

If we now substitute $x=-\frac{3}{7}$ into $y=-4-4x,$ we can then find the value of $y:$

$$
\begin{aligned}y & =-4-4(-\frac{3}{7}) \\ y & =-\frac{16}{7}\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-\frac{3}{7},\,y=-\frac{16}{7}.$

## Variant unit_pair 1

Find the solution $(x,y)$ to this system using the method of substitution.

$$
\left\{\begin{aligned}-3x+3y &=-12 \\ -4x+y &=1\end{aligned}\right.
$$

The solution is $($ {{field-1}} $,$ {{field-2}} $)$

```json
[
  {
    ":answer-field/id": "374e5025-0b9f-5172-8310-e372a7e7af6f",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "a87afe01-2861-5031-af0d-e6d76361ee46",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-\\frac{5}{3}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "a87afe01-2861-5031-af0d-e6d76361ee46"
    ]
  },
  {
    ":answer-field/id": "e6e6b122-cd90-5ae7-a833-9de4382b685d",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "834484ce-a70b-5507-8603-37dbbb1a8a7a",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-\\frac{17}{3}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "834484ce-a70b-5507-8603-37dbbb1a8a7a"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the second equation, we can isolate $y$:

$$
\begin{aligned}-4x+y & =1 \\ y & =1+4x\end{aligned}
$$

Then, we substitute $y=1+4x$ into the first equation and solve for $x:$

$$
\begin{aligned}-3x+3y & =-12 \\ -3x+3(1+4x) & =-12 \\ -3x+3+12x & =-12 \\ 9x+3 & =-12 \\ 9x & =-15 \\ x & =-\frac{5}{3}\end{aligned}
$$

If we now substitute $x=-\frac{5}{3}$ into $y=1+4x,$ we can then find the value of $y:$

$$
\begin{aligned}y & =1+4(-\frac{5}{3}) \\ y & =-\frac{17}{3}\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-\frac{5}{3},\,y=-\frac{17}{3}.$

## Variant preisolated_uv 0

Consider the following system of equations:

$$
\left\{\begin{aligned}3u+v &=7 \\ u &=v+8\end{aligned}\right.
$$

Find the solution $(u,v)$ to this system using the method of substitution.

$(u,v)=($
{{field-1}}
$,$
{{field-2}}
$)$

```json
[
  {
    ":answer-field/id": "0d73e632-7c7e-5265-a6f8-862b01c64cb6",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "09aa7ea4-53f8-578b-8667-ccd5e65f30b0",
        ":answer/type": ":answer.type/math",
        ":answer/value": "\\frac{15}{4}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "09aa7ea4-53f8-578b-8667-ccd5e65f30b0"
    ]
  },
  {
    ":answer-field/id": "88a7b4a9-76cd-59cc-8ea8-efac62ecb5a8",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "d3a495e3-2fe8-57a2-a334-6aa3d428de15",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-\\frac{17}{4}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "d3a495e3-2fe8-57a2-a334-6aa3d428de15"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. It so happens that the second equation is already solved for $u:$

$$
u=v+8
$$

So, we replace $u$ with $v+8$ in the first equation and solve for $v:$

$$
\begin{aligned}3u+v & =7 \\ 3(v+8)+v & =7 \\ 3v+24+v & =7 \\ 4v & =-17 \\ v & =-\frac{17}{4}\end{aligned}
$$

If we now substitute $v=-\frac{17}{4}$ into $u=v+8,$ then we can find the value of $u:$

$$
\begin{aligned}u & =v+8 \\ u & =(-\frac{17}{4})+8 \\ u & =\frac{15}{4}\end{aligned}
$$

Therefore, the solution to the system of equations is $u=\frac{15}{4},\,v=-\frac{17}{4},$ which can be expressed as $(\frac{15}{4},-\frac{17}{4}).$

## Variant preisolated_uv 1

Consider the following system of equations:

$$
\left\{\begin{aligned}-4u+2v &=-14 \\ u &=v-5\end{aligned}\right.
$$

Find the solution $(u,v)$ to this system using the method of substitution.

$(u,v)=($
{{field-1}}
$,$
{{field-2}}
$)$

```json
[
  {
    ":answer-field/id": "2c9bbc49-8565-595f-be67-1451845f6c05",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "a9947033-6b1f-52b8-b6c7-a4be911acbd5",
        ":answer/type": ":answer.type/math",
        ":answer/value": "12"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "a9947033-6b1f-52b8-b6c7-a4be911acbd5"
    ]
  },
  {
    ":answer-field/id": "670d8527-93a8-5523-b644-029d176520ae",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "9f94f13f-fb36-5a98-8ed4-386553f935de",
        ":answer/type": ":answer.type/math",
        ":answer/value": "17"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "9f94f13f-fb36-5a98-8ed4-386553f935de"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. It so happens that the second equation is already solved for $u:$

$$
u=v-5
$$

So, we replace $u$ with $v-5$ in the first equation and solve for $v:$

$$
\begin{aligned}-4u+2v & =-14 \\ -4(v-5)+2v & =-14 \\ -4v+20+2v & =-14 \\ -2v & =-34 \\ v & =17\end{aligned}
$$

If we now substitute $v=17$ into $u=v-5,$ then we can find the value of $u:$

$$
\begin{aligned}u & =v-5 \\ u & =(17)-5 \\ u & =12\end{aligned}
$$

Therefore, the solution to the system of equations is $u=12,\,v=17,$ which can be expressed as $(12,17).$

## Variant isolate_xy 0

Consider the following system of equations:

$$
\left\{\begin{aligned}3x+y &=7 \\ x+y &=8\end{aligned}\right.
$$

Find the solution $(x,y)$ to this system using the method of substitution.

$(x,y)=($
{{field-1}}
$,$
{{field-2}}
$)$

```json
[
  {
    ":answer-field/id": "c0eb69ba-5867-5965-9f83-746cf8c014cc",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "0c0c69f6-8248-5b9a-885b-251b9beeda31",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-\\frac{1}{2}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "0c0c69f6-8248-5b9a-885b-251b9beeda31"
    ]
  },
  {
    ":answer-field/id": "36bab2b2-bf83-5612-9650-0ff0db2a3481",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "0b9c4e2d-66de-5be2-a234-cb7f2991634d",
        ":answer/type": ":answer.type/math",
        ":answer/value": "\\frac{17}{2}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "0b9c4e2d-66de-5be2-a234-cb7f2991634d"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. It doesn't matter which equation we pick first, so we choose the easiest one. In this case, the second equation looks like the easiest.

Using the second equation, we can isolate $x$ by subtracting $y$ from both sides of the equation:

$$
x=-y+8
$$

So, we replace $x$ with $-y+8$ in the first equation and solve for $y:$

$$
\begin{aligned}3x+y & =7 \\ 3(-y+8)+y & =7 \\ -3y+24+y & =7 \\ -2y & =-17 \\ y & =\frac{17}{2}\end{aligned}
$$

If we now substitute $y=\frac{17}{2}$ into $x=-y+8,$ then we can find the value of $x:$

$$
\begin{aligned}x & =-y+8 \\ x & =-(\frac{17}{2})+8 \\ x & =-\frac{17}{2}+8 \\ x & =-\frac{1}{2}\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-\frac{1}{2},\,y=\frac{17}{2},$ which can be expressed as $(-\frac{1}{2},\frac{17}{2}).$

## Variant isolate_xy 1

Consider the following system of equations:

$$
\left\{\begin{aligned}-4x+2y &=-14 \\ x+y &=-5\end{aligned}\right.
$$

Find the solution $(x,y)$ to this system using the method of substitution.

$(x,y)=($
{{field-1}}
$,$
{{field-2}}
$)$

```json
[
  {
    ":answer-field/id": "4455eef2-a9ac-5911-a645-c6e005c3c702",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "96964a48-804e-5de3-937d-47cdc4955ffc",
        ":answer/type": ":answer.type/math",
        ":answer/value": "\\frac{2}{3}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "96964a48-804e-5de3-937d-47cdc4955ffc"
    ]
  },
  {
    ":answer-field/id": "da8932a0-c7ee-5a96-b0c3-5220d6f4d25a",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "a71e1d51-14df-533e-88a8-13143aef8f16",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-\\frac{17}{3}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "a71e1d51-14df-533e-88a8-13143aef8f16"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. It doesn't matter which equation we pick first, so we choose the easiest one. In this case, the second equation looks like the easiest.

Using the second equation, we can isolate $x$ by subtracting $y$ from both sides of the equation:

$$
x=-y-5
$$

So, we replace $x$ with $-y-5$ in the first equation and solve for $y:$

$$
\begin{aligned}-4x+2y & =-14 \\ -4(-y-5)+2y & =-14 \\ 4y+20+2y & =-14 \\ 6y & =-34 \\ y & =-\frac{17}{3}\end{aligned}
$$

If we now substitute $y=-\frac{17}{3}$ into $x=-y-5,$ then we can find the value of $x:$

$$
\begin{aligned}x & =-y-5 \\ x & =-(-\frac{17}{3})-5 \\ x & =\frac{17}{3}-5 \\ x & =\frac{2}{3}\end{aligned}
$$

Therefore, the solution to the system of equations is $x=\frac{2}{3},\,y=-\frac{17}{3},$ which can be expressed as $(\frac{2}{3},-\frac{17}{3}).$

## Variant cake_context 0

The pastry shop's total cost and revenue per month (in dollars) from selling cakes can be modeled by the equations $y=386+8n$ and $y=56+19n,$ respectively, where $n$ is the number of cakes sold. 

Solve the system below using the substitution method to find the exact number of cakes needed to break even and the revenue made.

$$
\left\{\begin{aligned}y &=386+8n \\ y &=56+19n\end{aligned}\right.
$$

The pastry shop breaks even when$\,$
{{field-1}}
$\,$cakes are produced. 

The revenue made when selling this number of cakes is$\,$
{{field-2}}
$\,$dollars.

```json
[
  {
    ":answer-field/id": "216b0bab-1b93-5599-b0a2-0c18490e8bc8",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "01b0c92e-2cfe-572e-be03-e2caccedb712",
        ":answer/type": ":answer.type/math",
        ":answer/value": "30"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "01b0c92e-2cfe-572e-be03-e2caccedb712"
    ]
  },
  {
    ":answer-field/id": "ff1c5856-32c2-5d80-a1dd-d63e2504677d",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "16db46ad-f7d7-5c23-8db9-193145f1c6f0",
        ":answer/type": ":answer.type/math",
        ":answer/value": "626"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "16db46ad-f7d7-5c23-8db9-193145f1c6f0"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that $y$ is isolated in the first equation. Therefore, we can replace $y$ with $386+8n$ in the second equation and solve for $n:$

$$
\begin{aligned}y & =56+19n \\ 386+8n & =56+19n \\ 386+8n-56 & =56+19n-56 \\ 330+8n & =19n \\ 330+8n-8n & =19n-8n \\ 330 & =11n \\ \frac{330}{11} & =\frac{11n}{11} \\ 30 & =n \\ n & =30\end{aligned}
$$

If we now substitute $n=30$ into $y=56+19n$, then we can find the value of $y:$

$$
\begin{aligned}y &=56+19(30)=626\end{aligned}
$$

Hence, the solution to the system of equations is $n=30$ and $y=626.$
Therefore, the pastry shop breaks even when $30$ units are produced, and the revenue made when selling this number of units is $626.$

## Variant cake_context 1

The pastry shop's total cost and revenue per month (in dollars) from selling cakes can be modeled by the equations $y=672+6n$ and $y=24+24n,$ respectively, where $n$ is the number of cakes sold. 

Solve the system below using the substitution method to find the exact number of cakes needed to break even and the revenue made.

$$
\left\{\begin{aligned}y &=672+6n \\ y &=24+24n\end{aligned}\right.
$$

The pastry shop breaks even when$\,$
{{field-1}}
$\,$cakes are produced. 

The revenue made when selling this number of cakes is$\,$
{{field-2}}
$\,$dollars.

```json
[
  {
    ":answer-field/id": "479a74ef-9d10-5b22-8f5e-b4fc859286be",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "bc048f49-9347-56a2-b012-ba90b13ed21c",
        ":answer/type": ":answer.type/math",
        ":answer/value": "36"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "bc048f49-9347-56a2-b012-ba90b13ed21c"
    ]
  },
  {
    ":answer-field/id": "cf63408b-bd74-58ad-b3c2-a4ee5cbfca82",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "dd970284-01c6-5362-8768-4bbd32990202",
        ":answer/type": ":answer.type/math",
        ":answer/value": "888"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "dd970284-01c6-5362-8768-4bbd32990202"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Notice that $y$ is isolated in the first equation. Therefore, we can replace $y$ with $672+6n$ in the second equation and solve for $n:$

$$
\begin{aligned}y & =24+24n \\ 672+6n & =24+24n \\ 672+6n-24 & =24+24n-24 \\ 648+6n & =24n \\ 648+6n-6n & =24n-6n \\ 648 & =18n \\ \frac{648}{18} & =\frac{18n}{18} \\ 36 & =n \\ n & =36\end{aligned}
$$

If we now substitute $n=36$ into $y=24+24n$, then we can find the value of $y:$

$$
\begin{aligned}y &=24+24(36)=888\end{aligned}
$$

Hence, the solution to the system of equations is $n=36$ and $y=888.$
Therefore, the pastry shop breaks even when $36$ units are produced, and the revenue made when selling this number of units is $888.$

## Variant meeting_context 0

Mary wonders where and when they'd meet if Sam left home $2$ minutes earlier and walked with a speed of $60$ meters per minute. She finds that the distance $d$ from home they'd meet can be modeled using the following system of equations.

$$
\left\{\begin{aligned}d+70t &=1\,030 \\ d-60t &=120.\end{aligned}\right.
$$

where $t$ is the time (in minutes) since Mary left the community park.

Mary and Sam would meet$\,$
{{field-1}}$\,$minutes after Mary left the community park.

Mary and Sam would meet at a distance of $\,$
{{field-2}}$\,$meters from home.

```json
[
  {
    ":answer-field/id": "ca33f086-ec26-5b8c-af9d-8c1477ad58ae",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "662dccb4-06e8-5837-81a0-e32b1821c6ff",
        ":answer/type": ":answer.type/math",
        ":answer/value": "7"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "662dccb4-06e8-5837-81a0-e32b1821c6ff"
    ]
  },
  {
    ":answer-field/id": "b2c0b93b-a68c-5e53-90b2-8123f65a7581",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "b3367781-b220-5bdb-81b6-d653f704c51f",
        ":answer/type": ":answer.type/math",
        ":answer/value": "540"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "b3367781-b220-5bdb-81b6-d653f704c51f"
    ]
  }
]
```

To solve the given system of linear equations, we will isolate a variable in one of the equations and then substitute it into the other equation. It doesn't matter which equation we pick first, so we choose the easiest one. In this case, the second equation looks like the easiest.

Using the second equation, we can isolate $d$ adding to both sides of the equation $60t:$

$$
\begin{aligned}d-60t & =120 \\ d & =120+60t\end{aligned}
$$

So, we replace $d$ with $120+60t$ in the first equation and solve for $t:$

$$
\begin{aligned}d+70t & =1\,030 \\ (120+60t)+70t & =1\,030 \\ 120+130t & =1\,030 \\ 130t & =1\,030-120 \\ 130t & =910 \\ t & =\frac{910}{130} \\ t & =7.\end{aligned}
$$

Therefore, they would have met after $t=7$ minutes.

If we substitute $t=7$ into $d=120+60t$, we can find the value of $d:$

$$
\begin{aligned}d & =120+60t \\  & =120+60(7) \\  & =540\end{aligned}
$$

Therefore, they meet at a distance of $540$ meters from home.

## Variant meeting_context 1

Mary wonders where and when they'd meet if Sam left home $4$ minutes earlier and walked with a speed of $30$ meters per minute. She finds that the distance $d$ from home they'd meet can be modeled using the following system of equations.

$$
\left\{\begin{aligned}d+50t &=440 \\ d-30t &=120.\end{aligned}\right.
$$

where $t$ is the time (in minutes) since Mary left the community park.

Mary and Sam would meet$\,$
{{field-1}}$\,$minutes after Mary left the community park.

Mary and Sam would meet at a distance of $\,$
{{field-2}}$\,$meters from home.

```json
[
  {
    ":answer-field/id": "501d98d2-968c-507c-9f6c-4a8b13ce0915",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "91fa6cca-f29d-5288-a361-5f6e3e8203db",
        ":answer/type": ":answer.type/math",
        ":answer/value": "4"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "91fa6cca-f29d-5288-a361-5f6e3e8203db"
    ]
  },
  {
    ":answer-field/id": "691ee0ab-ecc6-51a9-9b58-cf08571982b6",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "2b480234-8967-5de3-8025-4d24bae5b0e3",
        ":answer/type": ":answer.type/math",
        ":answer/value": "240"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "2b480234-8967-5de3-8025-4d24bae5b0e3"
    ]
  }
]
```

To solve the given system of linear equations, we will isolate a variable in one of the equations and then substitute it into the other equation. It doesn't matter which equation we pick first, so we choose the easiest one. In this case, the second equation looks like the easiest.

Using the second equation, we can isolate $d$ adding to both sides of the equation $30t:$

$$
\begin{aligned}d-30t & =120 \\ d & =120+30t\end{aligned}
$$

So, we replace $d$ with $120+30t$ in the first equation and solve for $t:$

$$
\begin{aligned}d+50t & =440 \\ (120+30t)+50t & =440 \\ 120+80t & =440 \\ 80t & =440-120 \\ 80t & =320 \\ t & =\frac{320}{80} \\ t & =4.\end{aligned}
$$

Therefore, they would have met after $t=4$ minutes.

If we substitute $t=4$ into $d=120+30t$, we can find the value of $d:$

$$
\begin{aligned}d & =120+30t \\  & =120+30(4) \\  & =240\end{aligned}
$$

Therefore, they meet at a distance of $240$ meters from home.

## Fixed-system forward target

Given the system of equations below, what is the value of $a - b$?

$$
\left\{\begin{aligned}2a-2b &=10 \\ -3a+b &=-3\end{aligned}\right.
$$

```json
[
  {
    ":answer-field/id": "8fc2bdb9-73a9-5da9-9b22-8867f41955b6",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "24fcc5de-618f-567e-aada-9728c88c3df0",
        ":answer/type": ":answer.type/math",
        ":answer/value": "5"
      },
      {
        ":answer/id": "431fba4e-2b58-5571-b58c-cb35fcc15c43",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-5"
      },
      {
        ":answer/id": "ffe90381-e60d-5d7c-9db9-0f0d70a98df3",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-7"
      },
      {
        ":answer/id": "2e1f8cdf-cfc4-5ae1-8663-dcdf3a2410e7",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-6"
      },
      {
        ":answer/id": "f1043d28-e4de-5c58-858d-e1dbbc96a610",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "24fcc5de-618f-567e-aada-9728c88c3df0"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the second equation, we can isolate $b$:

$$
\begin{aligned}-3a+b & =-3 \\ b & =-3+3a\end{aligned}
$$

Then, we substitute $b=-3+3a$ into the first equation and solve for $a:$

$$
\begin{aligned}2a-2b & =10 \\ 2a-2(-3+3a) & =10 \\ 2a+6-6a & =10 \\ -4a+6 & =10 \\ -4a & =4 \\ a & =-1\end{aligned}
$$

If we now substitute $a=-1$ into $b=-3+3a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =-3+3(-1) \\ b & =-6\end{aligned}
$$

Therefore, $a-b=-1-(-6)=5.$

## Fixed-system reverse target

Given the system of equations below, what is the value of $b - a$?

$$
\left\{\begin{aligned}2a-2b &=10 \\ -3a+b &=-3\end{aligned}\right.
$$

```json
[
  {
    ":answer-field/id": "060c6ac1-9f68-5d71-9a69-ce04a518e434",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "2ddf37fc-ac17-5abf-8625-b9a6952b6a5f",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-5"
      },
      {
        ":answer/id": "e5959f15-f072-549f-accb-b59497b47828",
        ":answer/type": ":answer.type/math",
        ":answer/value": "5"
      },
      {
        ":answer/id": "2e8a8d17-6fb1-55cd-a46e-94b224c157cc",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-7"
      },
      {
        ":answer/id": "9b405c7a-d209-53ef-83a0-c148b7c2415a",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-6"
      },
      {
        ":answer/id": "5b7ea07e-729c-5c16-86c2-9b4816bdd1dc",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "2ddf37fc-ac17-5abf-8625-b9a6952b6a5f"
    ]
  }
]
```

We will isolate a variable in one of the equations and then substitute it into the other equation. 

Using the second equation, we can isolate $b$:

$$
\begin{aligned}-3a+b & =-3 \\ b & =-3+3a\end{aligned}
$$

Then, we substitute $b=-3+3a$ into the first equation and solve for $a:$

$$
\begin{aligned}2a-2b & =10 \\ 2a-2(-3+3a) & =10 \\ 2a+6-6a & =10 \\ -4a+6 & =10 \\ -4a & =4 \\ a & =-1\end{aligned}
$$

If we now substitute $a=-1$ into $b=-3+3a,$ we can then find the value of $b:$

$$
\begin{aligned}b & =-3+3(-1) \\ b & =-6\end{aligned}
$$

Therefore, $b-a=-6-(-1)=-5.$
