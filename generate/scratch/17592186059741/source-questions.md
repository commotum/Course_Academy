# Source evidence

Captured at math EDB basis 2509.

## q-11442

If $kG = \begin{bmatrix}5 & 0 \\ 10 & 30\end{bmatrix}$,
where $G = \begin{bmatrix}1 & 0 \\ 2 & 6\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k$.

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "ceb712c3-34be-5d56-b1da-c9f3dc12f14a",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k = 3",
        ":db/id": 17592186056329
      },
      {
        ":answer/id": "f430dc96-0627-52c0-96f8-3dd0d1fdc011",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k = 2",
        ":db/id": 17592186056330
      },
      {
        ":answer/id": "025ff679-230d-51ee-b4fc-f25b59e718f3",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k = 5",
        ":db/id": 17592186056331
      },
      {
        ":answer/id": "0f7de378-142c-5f3e-bed2-3c5acc9ca509",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k = 0",
        ":db/id": 17592186056332
      },
      {
        ":answer/id": "2632bad7-b0a0-5089-b585-44e7f1909169",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k = 4",
        ":db/id": 17592186056333
      }
    ],
    ":answer-field/id": "14689557-d421-5d15-9b0f-08b601e5a6d0",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186056328
  }
]

No solution.

## q-981

If $kA=\begin{bmatrix}-7 & -21 & 56\end{bmatrix}$,
where $A=\begin{bmatrix}-1 & -3 & 8\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "3b6c7feb-e1e4-5887-9269-a70c549b3932",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k=4",
        ":db/id": 17592186361110
      },
      {
        ":answer/id": "4da79416-6947-54f4-88ab-d36dbb592119",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k=7",
        ":db/id": 17592186361174
      },
      {
        ":answer/id": "53376dd3-6051-57be-9178-00766c6ec74e",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k=6",
        ":db/id": 17592186361206
      },
      {
        ":answer/id": "69e380fe-b63f-5b7d-8e40-f4c2783aa85f",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k=3",
        ":db/id": 17592186361312
      },
      {
        ":answer/id": "83d9f12d-1a74-5c6d-b0b8-9182fdd9e2a8",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k=5",
        ":db/id": 17592186361423
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "4da79416-6947-54f4-88ab-d36dbb592119",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "k=7",
      ":db/id": 17592186361174
    },
    ":answer-field/id": "a5735c9d-1438-5c01-a0eb-1e4ffee8d379",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186362137
  }
]

To express $kA,$ we multiply each entry of $A$ by $k,$ as follows:

$$
\begin{aligned}kA & =k\cdot \begin{bmatrix}-1 & -3 & 8\end{bmatrix} \\  & =\begin{bmatrix}-k & -3k & 8k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kA$ in the problem statement:

$$
\begin{bmatrix}-k & -3k & 8k\end{bmatrix}=\begin{bmatrix}-7 & -21 & 56\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the leftmost elements, $-k$ and $-7.$ Equating these elements, we get

$$
\begin{aligned}-k & =-7 \\ k & =7.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## q-139431

Maria and John agreed to increase the bet. After increasing, Maria's payoff matrix became

$$
\begin{bmatrix}0 & -6 & 6 \\ 6 & 0 & -6 \\ -6 & 6 & 0\end{bmatrix}.
$$

This new matrix is obtained from matrix $P$ using the scalar multiplication $kP$, where

                            
                                    
                                        
                                        $\,k=$

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        .

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "19a27d10-05f6-5852-96f7-8b0934d40235",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3",
        ":db/id": 17592186234581
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "19a27d10-05f6-5852-96f7-8b0934d40235",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "3",
      ":db/id": 17592186234581
    },
    ":answer-field/id": "0a51b386-9333-5451-874c-d530eb586091",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186234983
  }
]

To express $kP,$ we multiply each entry of $P$ by $k,$ as follows:

$$
\begin{aligned}kP & =k\begin{bmatrix}0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0\end{bmatrix} \\  & =\begin{bmatrix}0 & -2k & 2k \\ 2k & 0 & -2k \\ -2k & 2k & 0\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the value given for $kP$ in the problem statement:

$$
\begin{bmatrix}0 & -2k & 2k \\ 2k & 0 & -2k \\ -2k & 2k & 0\end{bmatrix}=\begin{bmatrix}0 & -6 & 6 \\ 6 & 0 & -6 \\ -6 & 6 & 0\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the top-right elements, $2k$ and $6.$ Equating these elements, we get

$$
\begin{aligned}2k & =6 \\ k & =3.\end{aligned}
$$

**Note:** We would get the same result by equating any two corresponding (nonzero) elements.

## q-320536

If $kB=\begin{bmatrix}33 & 36 \\ -12 & -24\end{bmatrix}$,
where $B=\begin{bmatrix}11 & 12 \\ -4 & -8\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "cfd27dc5-4894-5e37-b2e5-2578b1696b56",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "3",
        ":db/id": 17592186298457
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "cfd27dc5-4894-5e37-b2e5-2578b1696b56",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "3",
      ":db/id": 17592186298457
    },
    ":answer-field/id": "e4e3dc78-835d-58b6-b211-120e5ef09fdf",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186299409
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}11 & 12 \\ 4 & -8\end{bmatrix} \\  & =\begin{bmatrix}11k & 12k \\ 4k & -8k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}11k & 12k \\ -4k & -8k\end{bmatrix}=\begin{bmatrix}33 & 36 \\ -12 & -24\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the bottom-left elements, $-4k$ and $-12.$ Equating these elements, we get

$$
\begin{aligned}-4k & =-12 \\ k & =3.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## q-320551

If $kW=\begin{bmatrix}5 & 0 & 0 \\ 0 & 20 & -15 \\ 10 & -10 & 25\end{bmatrix}$,
where $W=\begin{bmatrix}1 & 0 & 0 \\ 0 & 4 & -3 \\ 2 & -2 & 5\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "826094f3-db02-59ba-a855-db50607dea6c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "5",
        ":db/id": 17592186298115
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "826094f3-db02-59ba-a855-db50607dea6c",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "5",
      ":db/id": 17592186298115
    },
    ":answer-field/id": "fa1a2567-d705-58f3-ad50-ac8337bd9075",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186299481
  }
]

To express $kW,$ we multiply each entry of $W$ by $k,$ as follows:

$$
\begin{aligned}kW & =k\begin{bmatrix}1 & 0 & 0 \\ 0 & 4 & -3 \\ 2 & -2 & 5\end{bmatrix} \\  & =\begin{bmatrix}k & 0 & 0 \\ 0 & 4k & -3k \\ 2k & -2k & 5k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kW$ in the problem statement:

$$
\begin{bmatrix}k & 0 & 0 \\ 0 & 4k & -3k \\ 2k & -2k & 5k\end{bmatrix}=\begin{bmatrix}5 & 0 & 0 \\ 0 & 20 & -15 \\ 10 & -10 & 25\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the  leftmost elements of the third row, $2k$ and $10.$ Equating these elements, we get

$$
\begin{aligned}2k & =10 \\ k & =5.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## q-320563

If $kB=\begin{bmatrix}8 & -4 & 2\end{bmatrix}$,
where $B=\begin{bmatrix}24 & -12 & 6\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "796aff8c-2d9c-5570-96ae-5278b9bf5a36",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "\\frac{1}{3}",
        ":db/id": 17592186298082
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "796aff8c-2d9c-5570-96ae-5278b9bf5a36",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "\\frac{1}{3}",
      ":db/id": 17592186298082
    },
    ":answer-field/id": "83ce9b97-3a4a-54e6-b6b8-b4ed177d7ed4",
    ":answer-field/key": "field-1",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/blank"
    },
    ":db/id": 17592186299082
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}24 & -12 & 6\end{bmatrix} \\  & =\begin{bmatrix}24k & -12k & 6k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}24k & -12k & 6k\end{bmatrix}=\begin{bmatrix}8 & -4 & 2\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the rightmost elements, $6k$ and $2.$ Equating these elements, we get

$$
\begin{aligned}6k & =2 \\ k & =\frac{1}{3}.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## q-69670

If $kS=\begin{bmatrix}63 & -28 \\ 0 & -56\end{bmatrix}$,
where $S=\begin{bmatrix}-9 & 4 \\ 0 & 8\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "0cb162c3-0886-56a8-8bdd-ea309941ad8c",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k=-2",
        ":db/id": 17592186333101
      },
      {
        ":answer/id": "8f762ea6-9c19-57f6-b072-412e84452fb2",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k=0",
        ":db/id": 17592186334268
      },
      {
        ":answer/id": "9d0d7a0c-6212-5441-ab1d-b3033727fa78",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k=-7",
        ":db/id": 17592186334372
      },
      {
        ":answer/id": "c39b8c34-08f9-5cf0-b9ab-91abc406aa2e",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k=-3",
        ":db/id": 17592186334686
      },
      {
        ":answer/id": "e8a450c5-8b1d-5254-b15a-90a7c2647a52",
        ":answer/type": {
          ":db/ident": ":answer.type/math"
        },
        ":answer/value": "k=-6",
        ":db/id": 17592186335019
      }
    ],
    ":answer-field/correct": {
      ":answer/id": "9d0d7a0c-6212-5441-ab1d-b3033727fa78",
      ":answer/type": {
        ":db/ident": ":answer.type/math"
      },
      ":answer/value": "k=-7",
      ":db/id": 17592186334372
    },
    ":answer-field/id": "0dd5fe3a-0ae8-537c-ab9c-6c666f2d1465",
    ":answer-field/key": "selection",
    ":answer-field/type": {
      ":db/ident": ":answer-field.type/radio"
    },
    ":db/id": 17592186335264
  }
]

To express $kS,$ we multiply each entry of $S$ by $k,$ as follows:

$$
\begin{aligned}kS & =k\begin{bmatrix}-9 & 4 \\ 0 & 8\end{bmatrix} \\  & =\begin{bmatrix}-9k & 4k \\ 0 & 8k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kS$ in the problem statement:

$$
\begin{bmatrix}-9k & 4k \\ 0 & 8k\end{bmatrix}=\begin{bmatrix}63 & -28 \\ 0 & -56\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the top-left elements, $-9k$ and $63.$ Equating these elements, we get

$$
\begin{aligned}-9k & =63 \\ k & =-7.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.