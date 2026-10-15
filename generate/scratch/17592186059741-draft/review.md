## Original MA q-11442

If $kG = \begin{bmatrix}5 & 0 \\ 10 & 30\end{bmatrix}$,
where $G = \begin{bmatrix}1 & 0 \\ 2 & 6\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k$.

[
  {
    ":answer-field/id": "1bdc0807-b068-5460-a651-4d7bc531199b",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "3b7a310a-2ebc-5691-b8d6-bef20be08aab",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k = 5"
      },
      {
        ":answer/id": "ab7b36f6-472c-5ee0-984d-5f37fa8673df",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k = 2"
      },
      {
        ":answer/id": "3fd91969-eaf5-5227-984a-f28d15399c23",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k = 3"
      },
      {
        ":answer/id": "e6e6597b-5199-52c0-9772-360c44e7e2bb",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k = 4"
      },
      {
        ":answer/id": "79c4729e-9cca-5a6b-a8d5-bd3923dd638c",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k = 0"
      }
    ]
  }
]

[Source has no worked solution]

## Changed empirical evidence q-11442

If $kG = \begin{bmatrix}6 & 0 \\ 12 & 36\end{bmatrix}$,
where $G = \begin{bmatrix}1 & 0 \\ 2 & 6\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k$.

[
  {
    ":answer-field/id": "23812ae0-ba5a-5bdf-93c9-ef1bfda77118",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "75ee7721-c324-5e96-9d4a-f58f582fb73a",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k = 6"
      },
      {
        ":answer/id": "8078e396-4532-5c9a-9394-e23d38ac8252",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k = 3"
      },
      {
        ":answer/id": "ff47dc70-5463-5317-9e50-c361fb2c9c20",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k = 4"
      },
      {
        ":answer/id": "70285884-cbb4-5dbe-83af-92bf564ce39f",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k = 5"
      },
      {
        ":answer/id": "5026e3bc-18be-5412-9bab-fa8a7153aa07",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k = 0"
      }
    ]
  }
]

[Source has no worked solution]

## Authored method bank q-11442

If $kG = \begin{bmatrix}28 & 0 \\ 21 & 49\end{bmatrix}$,
where $G = \begin{bmatrix}4 & 0 \\ 3 & 7\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k$.

[
  {
    ":answer-field/id": "eca4ebfe-94d8-5bac-b8d3-29d9b9865957",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "ca9f0ed1-5f79-5727-89a7-46cb5ecad3ca",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=42"
      },
      {
        ":answer/id": "0f72e741-fbea-56ad-b56a-70bec65ac707",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=7"
      },
      {
        ":answer/id": "7d1e9110-5535-5058-96f2-a2e3708831e3",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=\\frac{1}{7}"
      },
      {
        ":answer/id": "9ec0c566-3562-5062-b651-a44b2a68aedf",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=56"
      },
      {
        ":answer/id": "cfb8ab01-6530-5af5-b287-b705715dc677",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=343"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "0f72e741-fbea-56ad-b56a-70bec65ac707"
    ]
  }
]

To express $kG,$ we multiply each entry of $G$ by $k,$ as follows:

$$
\begin{aligned}kG & =k\begin{bmatrix}4 & 0 \\ 3 & 7\end{bmatrix} \\  & =\begin{bmatrix}4k & 0 \\ 3k & 7k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kG$ in the problem statement:

$$
\begin{bmatrix}4k & 0 \\ 3k & 7k\end{bmatrix}=\begin{bmatrix}28 & 0 \\ 21 & 49\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $2$ and column $2$, $7k$ and $49.$ Equating these elements, we get

$$
\begin{aligned}7k & =49 \\ k & =7.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Authored method bank q-11442

If $kG = \begin{bmatrix}27 & 0 \\ 24 & 30\end{bmatrix}$,
where $G = \begin{bmatrix}9 & 0 \\ 8 & 10\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k$.

[
  {
    ":answer-field/id": "3e5e4aad-a8d7-5740-96f2-a6be3567a927",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "e4e1dfc2-73d5-5597-94a5-69a275620586",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=\\frac{1}{3}"
      },
      {
        ":answer/id": "b0e17d2f-2672-5dab-b329-a584346240c1",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=3"
      },
      {
        ":answer/id": "d60cb7a7-0fb7-527f-b9c6-66fac24930ba",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=36"
      },
      {
        ":answer/id": "bc108cf8-db1a-5226-94c5-716cb7010935",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=243"
      },
      {
        ":answer/id": "b2751ec7-9878-5005-8ebf-aa291bf1a16c",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=18"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "b0e17d2f-2672-5dab-b329-a584346240c1"
    ]
  }
]

To express $kG,$ we multiply each entry of $G$ by $k,$ as follows:

$$
\begin{aligned}kG & =k\begin{bmatrix}9 & 0 \\ 8 & 10\end{bmatrix} \\  & =\begin{bmatrix}9k & 0 \\ 8k & 10k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kG$ in the problem statement:

$$
\begin{bmatrix}9k & 0 \\ 8k & 10k\end{bmatrix}=\begin{bmatrix}27 & 0 \\ 24 & 30\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the top-left elements, $9k$ and $27.$ Equating these elements, we get

$$
\begin{aligned}9k & =27 \\ k & =3.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Original MA q-981

If $kA=\begin{bmatrix}-7 & -21 & 56\end{bmatrix}$,
where $A=\begin{bmatrix}-1 & -3 & 8\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "f303b9b7-7030-5cb1-a151-611df9cd3e03",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "9422a3df-27c5-5725-83c9-086cc200ae53",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=6"
      },
      {
        ":answer/id": "47713414-129f-57f8-93be-ceacd90b90f8",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=7"
      },
      {
        ":answer/id": "a511f0c0-3163-5691-b50c-adc384cb0b02",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=4"
      },
      {
        ":answer/id": "3ea51956-23f0-5416-814c-9ef709ecac2d",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=5"
      },
      {
        ":answer/id": "1790e7a3-8018-5adb-9111-7d6a00bcfa7c",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "47713414-129f-57f8-93be-ceacd90b90f8"
    ]
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

## Changed empirical evidence q-981

If $kA=\begin{bmatrix}-8 & -24 & 64\end{bmatrix}$,
where $A=\begin{bmatrix}-1 & -3 & 8\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "23218b3b-4de9-5b5e-835f-c28b662e53b5",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "8a10975e-749a-56de-b42b-c515229cee24",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=7"
      },
      {
        ":answer/id": "3228a251-523b-56dd-bd63-922d252b3c1c",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=8"
      },
      {
        ":answer/id": "fd1317f0-9424-571d-991a-267092f3df58",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=5"
      },
      {
        ":answer/id": "3f5b1cad-1dd5-5d76-b30b-9b856c9b84ef",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=6"
      },
      {
        ":answer/id": "7e0e637d-7463-5ee1-9dee-2a0f417f58ee",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=4"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "3228a251-523b-56dd-bd63-922d252b3c1c"
    ]
  }
]

To express $kA,$ we multiply each entry of $A$ by $k,$ as follows:

$$
\begin{aligned}kA & =k\cdot \begin{bmatrix}-1 & -3 & 8\end{bmatrix} \\  & =\begin{bmatrix}-k & -3k & 8k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kA$ in the problem statement:

$$
\begin{bmatrix}-k & -3k & 8k\end{bmatrix}=\begin{bmatrix}-8 & -24 & 64\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the leftmost elements, $-k$ and $-8.$ Equating these elements, we get

$$
\begin{aligned}-k & =-8 \\ k & =8.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Authored method bank q-981

If $kA=\begin{bmatrix}-28 & -21 & 49\end{bmatrix}$,
where $A=\begin{bmatrix}-4 & -3 & 7\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "6d59c3a7-5b09-5593-9f91-3c5dd18f6ddd",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "00c0d343-aec4-5cf8-b91d-23a4332d0efa",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=42"
      },
      {
        ":answer/id": "b02d3d86-c20c-5093-8978-28e57ac9283d",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=7"
      },
      {
        ":answer/id": "add7301f-9ffa-514d-9302-03cae8a6eb68",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=\\frac{1}{7}"
      },
      {
        ":answer/id": "cce6bf5a-50c1-5808-bd31-ed498a43a9e7",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=56"
      },
      {
        ":answer/id": "19b84813-f9da-5088-9fd6-c7c652bb13c3",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=343"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "b02d3d86-c20c-5093-8978-28e57ac9283d"
    ]
  }
]

To express $kA,$ we multiply each entry of $A$ by $k,$ as follows:

$$
\begin{aligned}kA & =k\cdot \begin{bmatrix}-4 & -3 & 7\end{bmatrix} \\  & =\begin{bmatrix}-4k & -3k & 7k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kA$ in the problem statement:

$$
\begin{bmatrix}-4k & -3k & 7k\end{bmatrix}=\begin{bmatrix}-28 & -21 & 49\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $3$, $7k$ and $49.$ Equating these elements, we get

$$
\begin{aligned}7k & =49 \\ k & =7.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Authored method bank q-981

If $kA=\begin{bmatrix}-27 & -24 & 30\end{bmatrix}$,
where $A=\begin{bmatrix}-9 & -8 & 10\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "e9463b32-451b-5c1f-a4bc-3a54725d80f0",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "6b05ddf5-acaa-561e-b5e3-343e5f6691fa",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=\\frac{1}{3}"
      },
      {
        ":answer/id": "16faa863-89e8-5f3e-866d-0a3c6f70a862",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=3"
      },
      {
        ":answer/id": "b373c0b8-aea0-564f-8c55-25514a11007d",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-36"
      },
      {
        ":answer/id": "3cc7a980-224e-5304-82fe-31939b2036ba",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=243"
      },
      {
        ":answer/id": "8cb17254-2264-546c-89d5-728d18412b84",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-18"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "16faa863-89e8-5f3e-866d-0a3c6f70a862"
    ]
  }
]

To express $kA,$ we multiply each entry of $A$ by $k,$ as follows:

$$
\begin{aligned}kA & =k\cdot \begin{bmatrix}-9 & -8 & 10\end{bmatrix} \\  & =\begin{bmatrix}-9k & -8k & 10k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kA$ in the problem statement:

$$
\begin{bmatrix}-9k & -8k & 10k\end{bmatrix}=\begin{bmatrix}-27 & -24 & 30\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the leftmost elements, $-9k$ and $-27.$ Equating these elements, we get

$$
\begin{aligned}-9k & =-27 \\ k & =3.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Original MA q-139431

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
    ":answer-field/id": "36d11733-4788-5075-ba10-201e2d026a19",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "ffcc0a34-970c-5240-b806-bacc8f0243b3",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "ffcc0a34-970c-5240-b806-bacc8f0243b3"
    ]
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

## Changed empirical evidence q-139431

Maria and John agreed to increase the bet. After increasing, Maria's payoff matrix became

$$
\begin{bmatrix}0 & -8 & 8 \\ 8 & 0 & -8 \\ -8 & 8 & 0\end{bmatrix}.
$$

This new matrix is obtained from matrix $P$ using the scalar multiplication $kP$, where

                            
                                    
                                        
$\,k=$

                                    
                                
                                    
                            
                                        {{field-1}}                
                                    
                                
                                    
                                        
                                        .

[
  {
    ":answer-field/id": "9020299d-5729-5c86-a0d2-2ded48eee0b4",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "08e1c100-8ece-5e4f-9908-71dde7b10dde",
        ":answer/type": ":answer.type/math",
        ":answer/value": "4"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "08e1c100-8ece-5e4f-9908-71dde7b10dde"
    ]
  }
]

To express $kP,$ we multiply each entry of $P$ by $k,$ as follows:

$$
\begin{aligned}kP & =k\begin{bmatrix}0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0\end{bmatrix} \\  & =\begin{bmatrix}0 & -2k & 2k \\ 2k & 0 & -2k \\ -2k & 2k & 0\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the value given for $kP$ in the problem statement:

$$
\begin{bmatrix}0 & -2k & 2k \\ 2k & 0 & -2k \\ -2k & 2k & 0\end{bmatrix}=\begin{bmatrix}0 & -8 & 8 \\ 8 & 0 & -8 \\ -8 & 8 & 0\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the top-right elements, $2k$ and $8.$ Equating these elements, we get

$$
\begin{aligned}2k & =8 \\ k & =4.\end{aligned}
$$

**Note:** We would get the same result by equating any two corresponding (nonzero) elements.

## Authored method bank q-139431

Maria and John agreed to increase the bet. After increasing, Maria's payoff matrix became

$$
\begin{bmatrix}0 & -10 & 10 \\ 10 & 0 & -10 \\ -10 & 10 & 0\end{bmatrix}.
$$

The original payoff matrix is $P=\begin{bmatrix}0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0\end{bmatrix}$.

This new matrix is obtained from matrix $P$ using the scalar multiplication $kP$, where




$\,k=$





{{field-1}}                




.

[
  {
    ":answer-field/id": "02f5afcd-05dd-54af-b5ba-d09eb022bbbe",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "3e3da42e-f480-54cc-bc50-02c28fb7681b",
        ":answer/type": ":answer.type/math",
        ":answer/value": "5"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "3e3da42e-f480-54cc-bc50-02c28fb7681b"
    ]
  }
]

To express $kP,$ we multiply each entry of $P$ by $k,$ as follows:

$$
\begin{aligned}kP & =k\begin{bmatrix}0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0\end{bmatrix} \\  & =\begin{bmatrix}0 & -2k & 2k \\ 2k & 0 & -2k \\ -2k & 2k & 0\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the value given for $kP$ in the problem statement:

$$
\begin{bmatrix}0 & -2k & 2k \\ 2k & 0 & -2k \\ -2k & 2k & 0\end{bmatrix}=\begin{bmatrix}0 & -10 & 10 \\ 10 & 0 & -10 \\ -10 & 10 & 0\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the top-right elements, $2k$ and $10.$ Equating these elements, we get

$$
\begin{aligned}2k & =10 \\ k & =5.\end{aligned}
$$

**Note:** We would get the same result by equating any two corresponding (nonzero) elements.

## Authored method bank q-139431

Maria and John agreed to increase the bet. After increasing, Maria's payoff matrix became

$$
\begin{bmatrix}0 & -18 & 18 \\ 18 & 0 & -18 \\ -18 & 18 & 0\end{bmatrix}.
$$

The original payoff matrix is $P=\begin{bmatrix}0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0\end{bmatrix}$.

This new matrix is obtained from matrix $P$ using the scalar multiplication $kP$, where




$\,k=$





{{field-1}}                




.

[
  {
    ":answer-field/id": "8d297f11-9e12-5145-b696-5f7b270c89e3",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "226bf31c-fdfa-53c9-b822-b16c51795c3c",
        ":answer/type": ":answer.type/math",
        ":answer/value": "9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "226bf31c-fdfa-53c9-b822-b16c51795c3c"
    ]
  }
]

To express $kP,$ we multiply each entry of $P$ by $k,$ as follows:

$$
\begin{aligned}kP & =k\begin{bmatrix}0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0\end{bmatrix} \\  & =\begin{bmatrix}0 & -2k & 2k \\ 2k & 0 & -2k \\ -2k & 2k & 0\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the value given for $kP$ in the problem statement:

$$
\begin{bmatrix}0 & -2k & 2k \\ 2k & 0 & -2k \\ -2k & 2k & 0\end{bmatrix}=\begin{bmatrix}0 & -18 & 18 \\ 18 & 0 & -18 \\ -18 & 18 & 0\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $3$ and column $1$, $-2k$ and $-18.$ Equating these elements, we get

$$
\begin{aligned}-2k & =-18 \\ k & =9.\end{aligned}
$$

**Note:** We would get the same result by equating any two corresponding (nonzero) elements.

## Original MA q-320536

If $kB=\begin{bmatrix}33 & 36 \\ -12 & -24\end{bmatrix}$,
where $B=\begin{bmatrix}11 & 12 \\ -4 & -8\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "10141a9b-d9b5-5699-a6f4-413f305b575a",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "64eb72d1-83a5-53d8-8aba-16b9443d83d6",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "64eb72d1-83a5-53d8-8aba-16b9443d83d6"
    ]
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

## Changed empirical evidence q-320536

If $kB=\begin{bmatrix}44 & 48 \\ -16 & -32\end{bmatrix}$,
where $B=\begin{bmatrix}11 & 12 \\ -4 & -8\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "1ce579a9-6d21-56ae-96f6-bfd8efcac63d",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "cd4a3e29-7a56-5019-93c1-bc0c9fb565d7",
        ":answer/type": ":answer.type/math",
        ":answer/value": "4"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "cd4a3e29-7a56-5019-93c1-bc0c9fb565d7"
    ]
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}11 & 12 \\ 4 & -8\end{bmatrix} \\  & =\begin{bmatrix}11k & 12k \\ 4k & -8k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}11k & 12k \\ -4k & -8k\end{bmatrix}=\begin{bmatrix}44 & 48 \\ -16 & -32\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the bottom-left elements, $-4k$ and $-16.$ Equating these elements, we get

$$
\begin{aligned}-4k & =-16 \\ k & =4.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Authored method bank q-320536

If $kB=\begin{bmatrix}28 & 21 \\ -49 & -70\end{bmatrix}$,
where $B=\begin{bmatrix}4 & 3 \\ -7 & -10\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "b5e2fbf1-a943-5774-844c-a782779db997",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "dfaa9cc8-ada8-5e49-9ffe-981ec4fd5453",
        ":answer/type": ":answer.type/math",
        ":answer/value": "7"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "dfaa9cc8-ada8-5e49-9ffe-981ec4fd5453"
    ]
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}4 & 3 \\ -7 & -10\end{bmatrix} \\  & =\begin{bmatrix}4k & 3k \\ -7k & -10k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}4k & 3k \\ -7k & -10k\end{bmatrix}=\begin{bmatrix}28 & 21 \\ -49 & -70\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the bottom-left elements, $-7k$ and $-49.$ Equating these elements, we get

$$
\begin{aligned}-7k & =-49 \\ k & =7.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Authored method bank q-320536

If $kB=\begin{bmatrix}27 & 24 \\ -30 & -9\end{bmatrix}$,
where $B=\begin{bmatrix}9 & 8 \\ -10 & -3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "ed6404b4-df9c-530f-a685-d113a935e8a5",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "35c67a04-bb4e-5aee-9d6c-b9391ec4cfa3",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "35c67a04-bb4e-5aee-9d6c-b9391ec4cfa3"
    ]
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}9 & 8 \\ -10 & -3\end{bmatrix} \\  & =\begin{bmatrix}9k & 8k \\ -10k & -3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}9k & 8k \\ -10k & -3k\end{bmatrix}=\begin{bmatrix}27 & 24 \\ -30 & -9\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $2$ and column $2$, $-3k$ and $-9.$ Equating these elements, we get

$$
\begin{aligned}-3k & =-9 \\ k & =3.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Original MA q-320551

If $kW=\begin{bmatrix}5 & 0 & 0 \\ 0 & 20 & -15 \\ 10 & -10 & 25\end{bmatrix}$,
where $W=\begin{bmatrix}1 & 0 & 0 \\ 0 & 4 & -3 \\ 2 & -2 & 5\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "e5048b83-dc70-5347-b2a4-9b3d143a7886",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "5aa7bbfe-c4fd-59a2-8f9a-c9c0436d7fa9",
        ":answer/type": ":answer.type/math",
        ":answer/value": "5"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "5aa7bbfe-c4fd-59a2-8f9a-c9c0436d7fa9"
    ]
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

## Changed empirical evidence q-320551

If $kW=\begin{bmatrix}6 & 0 & 0 \\ 0 & 24 & -18 \\ 12 & -12 & 30\end{bmatrix}$,
where $W=\begin{bmatrix}1 & 0 & 0 \\ 0 & 4 & -3 \\ 2 & -2 & 5\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "239d137c-0fd8-5430-80ce-7ccfc2666af4",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "c25b5d68-fa12-5b7d-b72e-6147bd43db98",
        ":answer/type": ":answer.type/math",
        ":answer/value": "6"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "c25b5d68-fa12-5b7d-b72e-6147bd43db98"
    ]
  }
]

To express $kW,$ we multiply each entry of $W$ by $k,$ as follows:

$$
\begin{aligned}kW & =k\begin{bmatrix}1 & 0 & 0 \\ 0 & 4 & -3 \\ 2 & -2 & 5\end{bmatrix} \\  & =\begin{bmatrix}k & 0 & 0 \\ 0 & 4k & -3k \\ 2k & -2k & 5k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kW$ in the problem statement:

$$
\begin{bmatrix}k & 0 & 0 \\ 0 & 4k & -3k \\ 2k & -2k & 5k\end{bmatrix}=\begin{bmatrix}6 & 0 & 0 \\ 0 & 24 & -18 \\ 12 & -12 & 30\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the  leftmost elements of the third row, $2k$ and $12.$ Equating these elements, we get

$$
\begin{aligned}2k & =12 \\ k & =6.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Authored method bank q-320551

If $kW=\begin{bmatrix}28 & 0 & 0 \\ 0 & 21 & -49 \\ 70 & -84 & 35\end{bmatrix}$,
where $W=\begin{bmatrix}4 & 0 & 0 \\ 0 & 3 & -7 \\ 10 & -12 & 5\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "d60abbdb-409e-588f-9c6a-23fc6964990e",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "5010ac02-167e-5c93-b7d0-e5e9b8f6591d",
        ":answer/type": ":answer.type/math",
        ":answer/value": "7"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "5010ac02-167e-5c93-b7d0-e5e9b8f6591d"
    ]
  }
]

To express $kW,$ we multiply each entry of $W$ by $k,$ as follows:

$$
\begin{aligned}kW & =k\begin{bmatrix}4 & 0 & 0 \\ 0 & 3 & -7 \\ 10 & -12 & 5\end{bmatrix} \\  & =\begin{bmatrix}4k & 0 & 0 \\ 0 & 3k & -7k \\ 10k & -12k & 5k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kW$ in the problem statement:

$$
\begin{bmatrix}4k & 0 & 0 \\ 0 & 3k & -7k \\ 10k & -12k & 5k\end{bmatrix}=\begin{bmatrix}28 & 0 & 0 \\ 0 & 21 & -49 \\ 70 & -84 & 35\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $3$ and column $2$, $-12k$ and $-84.$ Equating these elements, we get

$$
\begin{aligned}-12k & =-84 \\ k & =7.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Authored method bank q-320551

If $kW=\begin{bmatrix}27 & 0 & 0 \\ 0 & 24 & -30 \\ 9 & -24 & 15\end{bmatrix}$,
where $W=\begin{bmatrix}9 & 0 & 0 \\ 0 & 8 & -10 \\ 3 & -8 & 5\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "246603a9-fd6b-5006-a622-75eca847ef17",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "456326c3-6d16-51a4-bca2-2191c7d0b9f9",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "456326c3-6d16-51a4-bca2-2191c7d0b9f9"
    ]
  }
]

To express $kW,$ we multiply each entry of $W$ by $k,$ as follows:

$$
\begin{aligned}kW & =k\begin{bmatrix}9 & 0 & 0 \\ 0 & 8 & -10 \\ 3 & -8 & 5\end{bmatrix} \\  & =\begin{bmatrix}9k & 0 & 0 \\ 0 & 8k & -10k \\ 3k & -8k & 5k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kW$ in the problem statement:

$$
\begin{bmatrix}9k & 0 & 0 \\ 0 & 8k & -10k \\ 3k & -8k & 5k\end{bmatrix}=\begin{bmatrix}27 & 0 & 0 \\ 0 & 24 & -30 \\ 9 & -24 & 15\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $3$ and column $2$, $-8k$ and $-24.$ Equating these elements, we get

$$
\begin{aligned}-8k & =-24 \\ k & =3.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Original MA q-320563

If $kB=\begin{bmatrix}8 & -4 & 2\end{bmatrix}$,
where $B=\begin{bmatrix}24 & -12 & 6\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "74718ed4-2d4f-56d9-8d64-3e22e165819b",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "65adac17-470c-5bc7-8cd4-5d1ee63e55a6",
        ":answer/type": ":answer.type/math",
        ":answer/value": "\\frac{1}{3}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "65adac17-470c-5bc7-8cd4-5d1ee63e55a6"
    ]
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

## Changed empirical evidence q-320563

If $kB=\begin{bmatrix}16 & -8 & 4\end{bmatrix}$,
where $B=\begin{bmatrix}24 & -12 & 6\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "bab8f725-12c9-562f-a18c-7c0972ecd55a",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "7af95a21-f756-5cc7-9a7e-ef7ff0d6c3d1",
        ":answer/type": ":answer.type/math",
        ":answer/value": "\\frac{2}{3}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "7af95a21-f756-5cc7-9a7e-ef7ff0d6c3d1"
    ]
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}24 & -12 & 6\end{bmatrix} \\  & =\begin{bmatrix}24k & -12k & 6k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}24k & -12k & 6k\end{bmatrix}=\begin{bmatrix}16 & -8 & 4\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the rightmost elements, $6k$ and $4.$ Equating these elements, we get

$$
\begin{aligned}6k & =4 \\ k & =\frac{2}{3}.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Authored method bank q-320563

If $kB=\begin{bmatrix}28 & -21 & 49\end{bmatrix}$,
where $B=\begin{bmatrix}4 & -3 & 7\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "0f14bdc2-396e-5344-af86-4af65d05b978",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "8cac90ec-19ae-56df-b0fc-f6220aef6bda",
        ":answer/type": ":answer.type/math",
        ":answer/value": "7"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "8cac90ec-19ae-56df-b0fc-f6220aef6bda"
    ]
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}4 & -3 & 7\end{bmatrix} \\  & =\begin{bmatrix}4k & -3k & 7k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}4k & -3k & 7k\end{bmatrix}=\begin{bmatrix}28 & -21 & 49\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the rightmost elements, $7k$ and $49.$ Equating these elements, we get

$$
\begin{aligned}7k & =49 \\ k & =7.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Authored method bank q-320563

If $kB=\begin{bmatrix}27 & -24 & 30\end{bmatrix}$,
where $B=\begin{bmatrix}9 & -8 & 10\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "611d2cb8-30fc-5e59-a8b2-49497140886a",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "21cdf30d-4b45-54d3-b257-3c7d70088743",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "21cdf30d-4b45-54d3-b257-3c7d70088743"
    ]
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}9 & -8 & 10\end{bmatrix} \\  & =\begin{bmatrix}9k & -8k & 10k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}9k & -8k & 10k\end{bmatrix}=\begin{bmatrix}27 & -24 & 30\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $1$, $9k$ and $27.$ Equating these elements, we get

$$
\begin{aligned}9k & =27 \\ k & =3.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Original MA q-69670

If $kS=\begin{bmatrix}63 & -28 \\ 0 & -56\end{bmatrix}$,
where $S=\begin{bmatrix}-9 & 4 \\ 0 & 8\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "a5beeebc-0fc8-5290-9b78-2d4cbab6c422",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "d7b6cfbf-5a82-5f30-ab29-a93a295bd2ec",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-7"
      },
      {
        ":answer/id": "616e98fd-9a00-5c31-bbba-c9c5b8258435",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=0"
      },
      {
        ":answer/id": "c29b5a92-e50a-5285-b555-3ade5464407d",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-2"
      },
      {
        ":answer/id": "87e8a7ff-7b31-5133-a2be-bc65407b2277",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-6"
      },
      {
        ":answer/id": "6c3b178a-2935-5ef6-a700-bf6c25a529f4",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "d7b6cfbf-5a82-5f30-ab29-a93a295bd2ec"
    ]
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

## Changed empirical evidence q-69670

If $kS=\begin{bmatrix}72 & -32 \\ 0 & -64\end{bmatrix}$,
where $S=\begin{bmatrix}-9 & 4 \\ 0 & 8\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "a15707d7-3dc1-5b9c-9236-12c3d40cdf28",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "caf3eb08-feb4-5c4a-a558-127300b5e3cd",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-8"
      },
      {
        ":answer/id": "73b67f5b-db70-5b59-ba41-7728d0e98b99",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=0"
      },
      {
        ":answer/id": "4ca6c64f-26a6-5092-b453-6ed051b6dfa7",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-3"
      },
      {
        ":answer/id": "26c96570-3af5-5190-9fe6-0f09abbaa46a",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-7"
      },
      {
        ":answer/id": "3bf60066-e00e-5026-adb6-55ba1166cb80",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-4"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "caf3eb08-feb4-5c4a-a558-127300b5e3cd"
    ]
  }
]

To express $kS,$ we multiply each entry of $S$ by $k,$ as follows:

$$
\begin{aligned}kS & =k\begin{bmatrix}-9 & 4 \\ 0 & 8\end{bmatrix} \\  & =\begin{bmatrix}-9k & 4k \\ 0 & 8k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kS$ in the problem statement:

$$
\begin{bmatrix}-9k & 4k \\ 0 & 8k\end{bmatrix}=\begin{bmatrix}72 & -32 \\ 0 & -64\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the top-left elements, $-9k$ and $72.$ Equating these elements, we get

$$
\begin{aligned}-9k & =72 \\ k & =-8.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Authored method bank q-69670

If $kS=\begin{bmatrix}-28 & 21 \\ 0 & 49\end{bmatrix}$,
where $S=\begin{bmatrix}-4 & 3 \\ 0 & 7\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "698a80ff-1225-5b3a-b809-ad2ce6841bdc",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "d05217f4-d23f-5537-9311-ac61f89f75c6",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=42"
      },
      {
        ":answer/id": "6e6190e9-b78e-5017-b659-9bbbd65b9cb7",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=7"
      },
      {
        ":answer/id": "77a77a8d-5ac9-5eb0-803d-3d88fef681d9",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=\\frac{1}{7}"
      },
      {
        ":answer/id": "58b20730-264a-53f8-ae07-e460c434fb21",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=56"
      },
      {
        ":answer/id": "3cbeb865-b964-5fd1-9ead-ed801b21ffbc",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=343"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "6e6190e9-b78e-5017-b659-9bbbd65b9cb7"
    ]
  }
]

To express $kS,$ we multiply each entry of $S$ by $k,$ as follows:

$$
\begin{aligned}kS & =k\begin{bmatrix}-4 & 3 \\ 0 & 7\end{bmatrix} \\  & =\begin{bmatrix}-4k & 3k \\ 0 & 7k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kS$ in the problem statement:

$$
\begin{bmatrix}-4k & 3k \\ 0 & 7k\end{bmatrix}=\begin{bmatrix}-28 & 21 \\ 0 & 49\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $2$ and column $2$, $7k$ and $49.$ Equating these elements, we get

$$
\begin{aligned}7k & =49 \\ k & =7.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Authored method bank q-69670

If $kS=\begin{bmatrix}-27 & 24 \\ 0 & 30\end{bmatrix}$,
where $S=\begin{bmatrix}-9 & 8 \\ 0 & 10\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "eeacdb77-77ed-503b-a7f0-844a048cb7e1",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "40258f8b-c793-57ad-92df-629bd488bf84",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=\\frac{1}{3}"
      },
      {
        ":answer/id": "2fbee3fa-c6ef-56e5-88a9-d202d5eb54e1",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=3"
      },
      {
        ":answer/id": "51b8840d-7f44-5977-960b-1dc40f9af57a",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-36"
      },
      {
        ":answer/id": "169778d9-2e0d-5802-92e9-d64b5a432f93",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=243"
      },
      {
        ":answer/id": "a7d56688-3c5a-5578-a09e-e798b9a89e68",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-18"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "2fbee3fa-c6ef-56e5-88a9-d202d5eb54e1"
    ]
  }
]

To express $kS,$ we multiply each entry of $S$ by $k,$ as follows:

$$
\begin{aligned}kS & =k\begin{bmatrix}-9 & 8 \\ 0 & 10\end{bmatrix} \\  & =\begin{bmatrix}-9k & 8k \\ 0 & 10k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kS$ in the problem statement:

$$
\begin{bmatrix}-9k & 8k \\ 0 & 10k\end{bmatrix}=\begin{bmatrix}-27 & 24 \\ 0 & 30\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the top-left elements, $-9k$ and $-27.$ Equating these elements, we get

$$
\begin{aligned}-9k & =-27 \\ k & =3.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Generated easy

If $kS=\begin{bmatrix}-8 & 40 \\ 0 & 72\end{bmatrix}$,
where $S=\begin{bmatrix}-1 & 5 \\ 0 & 9\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "15026c2d-dafa-5e20-b734-90241d01d8f5",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "7b8d7eee-019b-59b4-97c6-851b795c7398",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=8"
      },
      {
        ":answer/id": "73714ceb-138b-5ba5-982b-8635248cccc5",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=45"
      },
      {
        ":answer/id": "fdb31191-3ca6-5576-9119-f8d66d47fbce",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=\\frac{1}{8}"
      },
      {
        ":answer/id": "27038e7b-4971-5beb-8fbf-c2ab48fa17d7",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=200"
      },
      {
        ":answer/id": "55b63e85-4021-5d5f-b46f-e90f3b0e8e53",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=35"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "7b8d7eee-019b-59b4-97c6-851b795c7398"
    ]
  }
]

To express $kS,$ we multiply each entry of $S$ by $k,$ as follows:

$$
\begin{aligned}kS & =k\begin{bmatrix}-1 & 5 \\ 0 & 9\end{bmatrix} \\  & =\begin{bmatrix}-k & 5k \\ 0 & 9k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kS$ in the problem statement:

$$
\begin{bmatrix}-k & 5k \\ 0 & 9k\end{bmatrix}=\begin{bmatrix}-8 & 40 \\ 0 & 72\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $2$, $5k$ and $40.$ Equating these elements, we get

$$
\begin{aligned}5k & =40 \\ k & =8.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Generated easy

If $kA=\begin{bmatrix}12 & 48 & -48\end{bmatrix}$,
where $A=\begin{bmatrix}-2 & -8 & 8\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "cffceb5a-3c06-5234-8d86-b75ee2ea64bb",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "5ae97172-3fba-5bc2-9e98-baaf2b88fc09",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-384"
      },
      {
        ":answer/id": "35fe34c3-b2d0-5006-a98b-ae49a79f8c48",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=40"
      },
      {
        ":answer/id": "ddec5cd5-63dd-5056-9dba-05ee42c11f44",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-6"
      },
      {
        ":answer/id": "b4f9d09d-29fc-54a9-a05f-dd005631d7f5",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-\\frac{1}{6}"
      },
      {
        ":answer/id": "0192c271-61b2-5147-96b2-f610a2b07406",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=56"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "ddec5cd5-63dd-5056-9dba-05ee42c11f44"
    ]
  }
]

To express $kA,$ we multiply each entry of $A$ by $k,$ as follows:

$$
\begin{aligned}kA & =k\cdot \begin{bmatrix}-2 & -8 & 8\end{bmatrix} \\  & =\begin{bmatrix}-2k & -8k & 8k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kA$ in the problem statement:

$$
\begin{bmatrix}-2k & -8k & 8k\end{bmatrix}=\begin{bmatrix}12 & 48 & -48\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $2$, $-8k$ and $48.$ Equating these elements, we get

$$
\begin{aligned}-8k & =48 \\ k & =-6.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Generated moderate

If $kW=\begin{bmatrix}5 & 0 & 0 \\ 0 & 9 & -8 \\ 7 & -5 & 8\end{bmatrix}$,
where $W=\begin{bmatrix}10 & 0 & 0 \\ 0 & 18 & -16 \\ 14 & -10 & 16\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "fb651857-9183-5b48-a155-a1bd7969dda6",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "3d9961d5-37c5-55ef-878b-d78063721dba",
        ":answer/type": ":answer.type/math",
        ":answer/value": "\\frac{1}{2}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "3d9961d5-37c5-55ef-878b-d78063721dba"
    ]
  }
]

To express $kW,$ we multiply each entry of $W$ by $k,$ as follows:

$$
\begin{aligned}kW & =k\begin{bmatrix}10 & 0 & 0 \\ 0 & 18 & -16 \\ 14 & -10 & 16\end{bmatrix} \\  & =\begin{bmatrix}10k & 0 & 0 \\ 0 & 18k & -16k \\ 14k & -10k & 16k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kW$ in the problem statement:

$$
\begin{bmatrix}10k & 0 & 0 \\ 0 & 18k & -16k \\ 14k & -10k & 16k\end{bmatrix}=\begin{bmatrix}5 & 0 & 0 \\ 0 & 9 & -8 \\ 7 & -5 & 8\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $2$ and column $3$, $-16k$ and $-8.$ Equating these elements, we get

$$
\begin{aligned}-16k & =-8 \\ k & =\frac{1}{2}.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Generated moderate

If $kA=\begin{bmatrix}2 & 8 & -8\end{bmatrix}$,
where $A=\begin{bmatrix}-8 & -32 & 32\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "5a3f95b6-06c1-5cfb-9aca-693d74fd4470",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "49313cce-284f-5026-8659-2b208324bd95",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-256"
      },
      {
        ":answer/id": "d8a68363-370b-531e-8b34-c281e7838da0",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-24"
      },
      {
        ":answer/id": "3734477f-5c32-503d-b18a-c921e5b2ff2a",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-\\frac{1}{4}"
      },
      {
        ":answer/id": "b3bc5d42-ea91-5e9d-a7f3-8bce72a6b3e4",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-4"
      },
      {
        ":answer/id": "8c6f2b30-51eb-5893-a46c-4c439565f35b",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=40"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "3734477f-5c32-503d-b18a-c921e5b2ff2a"
    ]
  }
]

To express $kA,$ we multiply each entry of $A$ by $k,$ as follows:

$$
\begin{aligned}kA & =k\cdot \begin{bmatrix}-8 & -32 & 32\end{bmatrix} \\  & =\begin{bmatrix}-8k & -32k & 32k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kA$ in the problem statement:

$$
\begin{bmatrix}-8k & -32k & 32k\end{bmatrix}=\begin{bmatrix}2 & 8 & -8\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $2$, $-32k$ and $8.$ Equating these elements, we get

$$
\begin{aligned}-32k & =8 \\ k & =-\frac{1}{4}.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Generated hard

If $kW=\begin{bmatrix}-9 & 0 & 0 \\ 0 & -6 & 30 \\ -15 & 27 & -36\end{bmatrix}$,
where $W=\begin{bmatrix}12 & 0 & 0 \\ 0 & 8 & -40 \\ 20 & -36 & 48\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "041e8a20-2ab2-5c99-a35c-5a21c2e1200a",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "40b62eac-df7e-5771-9cf8-bb283c4fcab4",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-\\frac{3}{4}"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "40b62eac-df7e-5771-9cf8-bb283c4fcab4"
    ]
  }
]

To express $kW,$ we multiply each entry of $W$ by $k,$ as follows:

$$
\begin{aligned}kW & =k\begin{bmatrix}12 & 0 & 0 \\ 0 & 8 & -40 \\ 20 & -36 & 48\end{bmatrix} \\  & =\begin{bmatrix}12k & 0 & 0 \\ 0 & 8k & -40k \\ 20k & -36k & 48k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kW$ in the problem statement:

$$
\begin{bmatrix}12k & 0 & 0 \\ 0 & 8k & -40k \\ 20k & -36k & 48k\end{bmatrix}=\begin{bmatrix}-9 & 0 & 0 \\ 0 & -6 & 30 \\ -15 & 27 & -36\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $3$ and column $2$, $-36k$ and $27.$ Equating these elements, we get

$$
\begin{aligned}-36k & =27 \\ k & =-\frac{3}{4}.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Generated hard

If $kA=\begin{bmatrix}-24 & -3 & 21\end{bmatrix}$,
where $A=\begin{bmatrix}-16 & -2 & 14\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "9017f391-958e-5725-9d0e-58543ba1a2d2",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "97b82f0b-f824-5e9e-9372-e0a179b52c7c",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-1"
      },
      {
        ":answer/id": "660bf586-7b94-5274-a11f-367c8c3db8c9",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=\\frac{2}{3}"
      },
      {
        ":answer/id": "bf4e7451-9528-54cf-bb10-35710f4e44ef",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=6"
      },
      {
        ":answer/id": "fc2837c6-60ae-5b56-97e9-46de6404506b",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=\\frac{3}{2}"
      },
      {
        ":answer/id": "9dee9c64-3110-5549-948c-445d94f5a33a",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-5"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "fc2837c6-60ae-5b56-97e9-46de6404506b"
    ]
  }
]

To express $kA,$ we multiply each entry of $A$ by $k,$ as follows:

$$
\begin{aligned}kA & =k\cdot \begin{bmatrix}-16 & -2 & 14\end{bmatrix} \\  & =\begin{bmatrix}-16k & -2k & 14k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kA$ in the problem statement:

$$
\begin{bmatrix}-16k & -2k & 14k\end{bmatrix}=\begin{bmatrix}-24 & -3 & 21\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $2$, $-2k$ and $-3.$ Equating these elements, we get

$$
\begin{aligned}-2k & =-3 \\ k & =\frac{3}{2}.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-11442 0,0

If $kG = \begin{bmatrix}-18 & 0 \\ -63 & -27\end{bmatrix}$,
where $G = \begin{bmatrix}2 & 0 \\ 7 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k$.

[
  {
    ":answer-field/id": "ad4d6431-0886-505f-b597-6cba8c6697c5",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "05f40225-88f3-5862-bb9c-464b33b183eb",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-36"
      },
      {
        ":answer/id": "daa67eaf-db5d-5049-9760-8b8b4427da9e",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-\\frac{1}{9}"
      },
      {
        ":answer/id": "a58244cf-a607-58ce-8564-9010eb503d1d",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-16"
      },
      {
        ":answer/id": "cdea81b3-2c7f-5d66-a1ac-d3241ef979a4",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-20"
      },
      {
        ":answer/id": "28939f48-29e2-51bc-b7b4-5bb95b95ccc1",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "28939f48-29e2-51bc-b7b4-5bb95b95ccc1"
    ]
  }
]

To express $kG,$ we multiply each entry of $G$ by $k,$ as follows:

$$
\begin{aligned}kG & =k\begin{bmatrix}2 & 0 \\ 7 & 3\end{bmatrix} \\  & =\begin{bmatrix}2k & 0 \\ 7k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kG$ in the problem statement:

$$
\begin{bmatrix}2k & 0 \\ 7k & 3k\end{bmatrix}=\begin{bmatrix}-18 & 0 \\ -63 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the top-left elements, $2k$ and $-18.$ Equating these elements, we get

$$
\begin{aligned}2k & =-18 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-11442 1,0

If $kG = \begin{bmatrix}-18 & 0 \\ -63 & -27\end{bmatrix}$,
where $G = \begin{bmatrix}2 & 0 \\ 7 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k$.

[
  {
    ":answer-field/id": "4808d0d0-b086-5872-ab5c-9314523f2449",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "2e3d2d30-0947-57ee-84bc-16e1ccebc1f9",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-441"
      },
      {
        ":answer/id": "45734819-5fe6-58ca-9a1b-b811e65284ec",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-\\frac{1}{9}"
      },
      {
        ":answer/id": "d8b727c5-f38b-5e1d-a61f-5e72b3ec340e",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-56"
      },
      {
        ":answer/id": "e7c80fa6-fa08-517a-a851-98190a63c078",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-70"
      },
      {
        ":answer/id": "9512a8c2-685d-5f5a-a0ef-04dc73e0abd0",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "9512a8c2-685d-5f5a-a0ef-04dc73e0abd0"
    ]
  }
]

To express $kG,$ we multiply each entry of $G$ by $k,$ as follows:

$$
\begin{aligned}kG & =k\begin{bmatrix}2 & 0 \\ 7 & 3\end{bmatrix} \\  & =\begin{bmatrix}2k & 0 \\ 7k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kG$ in the problem statement:

$$
\begin{bmatrix}2k & 0 \\ 7k & 3k\end{bmatrix}=\begin{bmatrix}-18 & 0 \\ -63 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $2$ and column $1$, $7k$ and $-63.$ Equating these elements, we get

$$
\begin{aligned}7k & =-63 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-11442 1,1

If $kG = \begin{bmatrix}-18 & 0 \\ -63 & -27\end{bmatrix}$,
where $G = \begin{bmatrix}2 & 0 \\ 7 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k$.

[
  {
    ":answer-field/id": "9573de0e-9a96-5b2e-912f-4ea67833a83f",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "d5199b81-deb0-5162-94b6-b6ab85157ff8",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-81"
      },
      {
        ":answer/id": "a89442fd-0677-55b1-b357-c3898efe2315",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-\\frac{1}{9}"
      },
      {
        ":answer/id": "cd14a917-da35-55c5-96a9-a399219992b0",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-24"
      },
      {
        ":answer/id": "960e45f7-08f5-565f-a61c-32345a0a4dd0",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-30"
      },
      {
        ":answer/id": "c163379d-007f-56b6-9fdf-d166123d6c57",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "c163379d-007f-56b6-9fdf-d166123d6c57"
    ]
  }
]

To express $kG,$ we multiply each entry of $G$ by $k,$ as follows:

$$
\begin{aligned}kG & =k\begin{bmatrix}2 & 0 \\ 7 & 3\end{bmatrix} \\  & =\begin{bmatrix}2k & 0 \\ 7k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kG$ in the problem statement:

$$
\begin{bmatrix}2k & 0 \\ 7k & 3k\end{bmatrix}=\begin{bmatrix}-18 & 0 \\ -63 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $2$ and column $2$, $3k$ and $-27.$ Equating these elements, we get

$$
\begin{aligned}3k & =-27 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-981 0,0

If $kA=\begin{bmatrix}18 & 63 & -27\end{bmatrix}$,
where $A=\begin{bmatrix}-2 & -7 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "5ab29fab-317a-5ddc-9dbd-2adfa4aa2891",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "d2788ac5-0be1-5401-bd99-db6159cada2f",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-36"
      },
      {
        ":answer/id": "44315a0a-3cbe-5173-9dfa-dc205873d3ec",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-\\frac{1}{9}"
      },
      {
        ":answer/id": "f48e3df4-10ea-5326-b970-69d82f64f2a7",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=16"
      },
      {
        ":answer/id": "83ef9c3a-ddbd-5062-9cf8-78641a8c948b",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=20"
      },
      {
        ":answer/id": "a619447e-a020-582e-b043-c75157364761",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "a619447e-a020-582e-b043-c75157364761"
    ]
  }
]

To express $kA,$ we multiply each entry of $A$ by $k,$ as follows:

$$
\begin{aligned}kA & =k\cdot \begin{bmatrix}-2 & -7 & 3\end{bmatrix} \\  & =\begin{bmatrix}-2k & -7k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kA$ in the problem statement:

$$
\begin{bmatrix}-2k & -7k & 3k\end{bmatrix}=\begin{bmatrix}18 & 63 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the leftmost elements, $-2k$ and $18.$ Equating these elements, we get

$$
\begin{aligned}-2k & =18 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-981 0,1

If $kA=\begin{bmatrix}18 & 63 & -27\end{bmatrix}$,
where $A=\begin{bmatrix}-2 & -7 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "86d27336-8ace-5842-9b70-41a14ef1a270",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "97963a0a-1b4f-5070-a492-85b27e14e57e",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-441"
      },
      {
        ":answer/id": "a5c61b16-ab3b-5c4e-9ea3-f2e215ac519b",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-\\frac{1}{9}"
      },
      {
        ":answer/id": "c61ff051-e227-5499-80f1-9213b0752dc4",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=56"
      },
      {
        ":answer/id": "0ed4f1b4-f02a-5d5d-85ba-86f08c058e6e",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=70"
      },
      {
        ":answer/id": "d28fb7c3-e150-5838-88f7-c97694014189",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "d28fb7c3-e150-5838-88f7-c97694014189"
    ]
  }
]

To express $kA,$ we multiply each entry of $A$ by $k,$ as follows:

$$
\begin{aligned}kA & =k\cdot \begin{bmatrix}-2 & -7 & 3\end{bmatrix} \\  & =\begin{bmatrix}-2k & -7k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kA$ in the problem statement:

$$
\begin{bmatrix}-2k & -7k & 3k\end{bmatrix}=\begin{bmatrix}18 & 63 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $2$, $-7k$ and $63.$ Equating these elements, we get

$$
\begin{aligned}-7k & =63 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-981 0,2

If $kA=\begin{bmatrix}18 & 63 & -27\end{bmatrix}$,
where $A=\begin{bmatrix}-2 & -7 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "6e1aefae-ad6a-59fc-8077-b919af299132",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "3cfbaf07-2e7a-5bbd-ba98-9f06670d27ab",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-81"
      },
      {
        ":answer/id": "2b1ae46e-d6c7-5eb4-a120-ab6ffd6ab963",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-\\frac{1}{9}"
      },
      {
        ":answer/id": "433d9fd4-c290-5f65-ad5c-91d6f47ff63c",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-24"
      },
      {
        ":answer/id": "a28bee17-6218-5652-8c60-29df9177cf8b",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-30"
      },
      {
        ":answer/id": "8fc465f7-4e30-5421-b6ee-afa1a84c747f",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "8fc465f7-4e30-5421-b6ee-afa1a84c747f"
    ]
  }
]

To express $kA,$ we multiply each entry of $A$ by $k,$ as follows:

$$
\begin{aligned}kA & =k\cdot \begin{bmatrix}-2 & -7 & 3\end{bmatrix} \\  & =\begin{bmatrix}-2k & -7k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kA$ in the problem statement:

$$
\begin{bmatrix}-2k & -7k & 3k\end{bmatrix}=\begin{bmatrix}18 & 63 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $3$, $3k$ and $-27.$ Equating these elements, we get

$$
\begin{aligned}3k & =-27 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-139431 0,1

Maria and John agreed to increase the bet. After increasing, Maria's payoff matrix became

$$
\begin{bmatrix}0 & -6 & 6 \\ 6 & 0 & -6 \\ -6 & 6 & 0\end{bmatrix}.
$$

The original payoff matrix is $P=\begin{bmatrix}0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0\end{bmatrix}$.

This new matrix is obtained from matrix $P$ using the scalar multiplication $kP$, where




$\,k=$





{{field-1}}                




.

[
  {
    ":answer-field/id": "18ef48b9-3df7-580b-a84f-6ef239c45938",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "a4404a06-eac7-574f-b44c-6356e52b6034",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "a4404a06-eac7-574f-b44c-6356e52b6034"
    ]
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

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $2$, $-2k$ and $-6.$ Equating these elements, we get

$$
\begin{aligned}-2k & =-6 \\ k & =3.\end{aligned}
$$

**Note:** We would get the same result by equating any two corresponding (nonzero) elements.

## Held data target q-139431 0,2

Maria and John agreed to increase the bet. After increasing, Maria's payoff matrix became

$$
\begin{bmatrix}0 & -6 & 6 \\ 6 & 0 & -6 \\ -6 & 6 & 0\end{bmatrix}.
$$

The original payoff matrix is $P=\begin{bmatrix}0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0\end{bmatrix}$.

This new matrix is obtained from matrix $P$ using the scalar multiplication $kP$, where




$\,k=$





{{field-1}}                




.

[
  {
    ":answer-field/id": "24e6e813-636e-59fc-8778-2c4b286601db",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "3778a2e7-50be-5c39-a30b-650e6a0bc682",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "3778a2e7-50be-5c39-a30b-650e6a0bc682"
    ]
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

## Held data target q-139431 1,0

Maria and John agreed to increase the bet. After increasing, Maria's payoff matrix became

$$
\begin{bmatrix}0 & -6 & 6 \\ 6 & 0 & -6 \\ -6 & 6 & 0\end{bmatrix}.
$$

The original payoff matrix is $P=\begin{bmatrix}0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0\end{bmatrix}$.

This new matrix is obtained from matrix $P$ using the scalar multiplication $kP$, where




$\,k=$





{{field-1}}                




.

[
  {
    ":answer-field/id": "4a5d1bb0-1a05-50bd-a6c0-77fd3ba10196",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "0e8b8139-23ee-505f-bdcd-ca13eddb2e26",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "0e8b8139-23ee-505f-bdcd-ca13eddb2e26"
    ]
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

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $2$ and column $1$, $2k$ and $6.$ Equating these elements, we get

$$
\begin{aligned}2k & =6 \\ k & =3.\end{aligned}
$$

**Note:** We would get the same result by equating any two corresponding (nonzero) elements.

## Held data target q-139431 1,2

Maria and John agreed to increase the bet. After increasing, Maria's payoff matrix became

$$
\begin{bmatrix}0 & -6 & 6 \\ 6 & 0 & -6 \\ -6 & 6 & 0\end{bmatrix}.
$$

The original payoff matrix is $P=\begin{bmatrix}0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0\end{bmatrix}$.

This new matrix is obtained from matrix $P$ using the scalar multiplication $kP$, where




$\,k=$





{{field-1}}                




.

[
  {
    ":answer-field/id": "91421546-1815-53a1-8d97-3979a31e6330",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "7c764768-162b-53cc-b72b-16d1851e8c3e",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "7c764768-162b-53cc-b72b-16d1851e8c3e"
    ]
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

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $2$ and column $3$, $-2k$ and $-6.$ Equating these elements, we get

$$
\begin{aligned}-2k & =-6 \\ k & =3.\end{aligned}
$$

**Note:** We would get the same result by equating any two corresponding (nonzero) elements.

## Held data target q-139431 2,0

Maria and John agreed to increase the bet. After increasing, Maria's payoff matrix became

$$
\begin{bmatrix}0 & -6 & 6 \\ 6 & 0 & -6 \\ -6 & 6 & 0\end{bmatrix}.
$$

The original payoff matrix is $P=\begin{bmatrix}0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0\end{bmatrix}$.

This new matrix is obtained from matrix $P$ using the scalar multiplication $kP$, where




$\,k=$





{{field-1}}                




.

[
  {
    ":answer-field/id": "504dfd38-3060-5552-852a-b7031996d237",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "71c98d10-25ca-5332-b515-389aa0016aa2",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "71c98d10-25ca-5332-b515-389aa0016aa2"
    ]
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

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $3$ and column $1$, $-2k$ and $-6.$ Equating these elements, we get

$$
\begin{aligned}-2k & =-6 \\ k & =3.\end{aligned}
$$

**Note:** We would get the same result by equating any two corresponding (nonzero) elements.

## Held data target q-139431 2,1

Maria and John agreed to increase the bet. After increasing, Maria's payoff matrix became

$$
\begin{bmatrix}0 & -6 & 6 \\ 6 & 0 & -6 \\ -6 & 6 & 0\end{bmatrix}.
$$

The original payoff matrix is $P=\begin{bmatrix}0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0\end{bmatrix}$.

This new matrix is obtained from matrix $P$ using the scalar multiplication $kP$, where




$\,k=$





{{field-1}}                




.

[
  {
    ":answer-field/id": "b11d381c-9075-5400-9d3e-8807a7723b6a",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "3cbab831-728e-589d-b060-289995338552",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "3cbab831-728e-589d-b060-289995338552"
    ]
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

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $3$ and column $2$, $2k$ and $6.$ Equating these elements, we get

$$
\begin{aligned}2k & =6 \\ k & =3.\end{aligned}
$$

**Note:** We would get the same result by equating any two corresponding (nonzero) elements.

## Held data target q-320536 0,0

If $kB=\begin{bmatrix}-18 & -63 \\ 27 & 99\end{bmatrix}$,
where $B=\begin{bmatrix}2 & 7 \\ -3 & -11\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "25bdd232-3514-57c8-92ba-fb36de7b811c",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "fb698d1e-7887-5fd5-8360-19d4deebaeee",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "fb698d1e-7887-5fd5-8360-19d4deebaeee"
    ]
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}2 & 7 \\ -3 & -11\end{bmatrix} \\  & =\begin{bmatrix}2k & 7k \\ -3k & -11k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}2k & 7k \\ -3k & -11k\end{bmatrix}=\begin{bmatrix}-18 & -63 \\ 27 & 99\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $1$, $2k$ and $-18.$ Equating these elements, we get

$$
\begin{aligned}2k & =-18 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-320536 0,1

If $kB=\begin{bmatrix}-18 & -63 \\ 27 & 99\end{bmatrix}$,
where $B=\begin{bmatrix}2 & 7 \\ -3 & -11\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "8dc79ad7-b8c8-5542-a0a1-fcc36568321a",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "6515f29c-d4c0-5cff-b777-09f69e959b61",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "6515f29c-d4c0-5cff-b777-09f69e959b61"
    ]
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}2 & 7 \\ -3 & -11\end{bmatrix} \\  & =\begin{bmatrix}2k & 7k \\ -3k & -11k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}2k & 7k \\ -3k & -11k\end{bmatrix}=\begin{bmatrix}-18 & -63 \\ 27 & 99\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $2$, $7k$ and $-63.$ Equating these elements, we get

$$
\begin{aligned}7k & =-63 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-320536 1,0

If $kB=\begin{bmatrix}-18 & -63 \\ 27 & 99\end{bmatrix}$,
where $B=\begin{bmatrix}2 & 7 \\ -3 & -11\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "9e35c4e0-ba4b-5bcd-aa36-87ff9a391086",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "ed695ab5-512c-5306-8910-6e8bf26d1ede",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "ed695ab5-512c-5306-8910-6e8bf26d1ede"
    ]
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}2 & 7 \\ -3 & -11\end{bmatrix} \\  & =\begin{bmatrix}2k & 7k \\ -3k & -11k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}2k & 7k \\ -3k & -11k\end{bmatrix}=\begin{bmatrix}-18 & -63 \\ 27 & 99\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the bottom-left elements, $-3k$ and $27.$ Equating these elements, we get

$$
\begin{aligned}-3k & =27 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-320536 1,1

If $kB=\begin{bmatrix}-18 & -63 \\ 27 & 99\end{bmatrix}$,
where $B=\begin{bmatrix}2 & 7 \\ -3 & -11\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "72d80a9e-251e-5e6a-9701-82199082221e",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "fc512a49-30e0-54ff-8693-8cc2a59dfd71",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "fc512a49-30e0-54ff-8693-8cc2a59dfd71"
    ]
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}2 & 7 \\ -3 & -11\end{bmatrix} \\  & =\begin{bmatrix}2k & 7k \\ -3k & -11k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}2k & 7k \\ -3k & -11k\end{bmatrix}=\begin{bmatrix}-18 & -63 \\ 27 & 99\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $2$ and column $2$, $-11k$ and $99.$ Equating these elements, we get

$$
\begin{aligned}-11k & =99 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-320551 0,0

If $kW=\begin{bmatrix}-18 & 0 & 0 \\ 0 & -63 & 27 \\ -99 & 9 & -27\end{bmatrix}$,
where $W=\begin{bmatrix}2 & 0 & 0 \\ 0 & 7 & -3 \\ 11 & -1 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "07acac0c-d414-5139-9b7c-b7f9f654a196",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "8521a4dc-2c03-5b2b-bd36-c939b5c699d2",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "8521a4dc-2c03-5b2b-bd36-c939b5c699d2"
    ]
  }
]

To express $kW,$ we multiply each entry of $W$ by $k,$ as follows:

$$
\begin{aligned}kW & =k\begin{bmatrix}2 & 0 & 0 \\ 0 & 7 & -3 \\ 11 & -1 & 3\end{bmatrix} \\  & =\begin{bmatrix}2k & 0 & 0 \\ 0 & 7k & -3k \\ 11k & -k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kW$ in the problem statement:

$$
\begin{bmatrix}2k & 0 & 0 \\ 0 & 7k & -3k \\ 11k & -k & 3k\end{bmatrix}=\begin{bmatrix}-18 & 0 & 0 \\ 0 & -63 & 27 \\ -99 & 9 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $1$, $2k$ and $-18.$ Equating these elements, we get

$$
\begin{aligned}2k & =-18 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-320551 1,1

If $kW=\begin{bmatrix}-18 & 0 & 0 \\ 0 & -63 & 27 \\ -99 & 9 & -27\end{bmatrix}$,
where $W=\begin{bmatrix}2 & 0 & 0 \\ 0 & 7 & -3 \\ 11 & -1 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "288b921a-e452-57c8-a276-3c70ab1c0b1b",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "746c857a-3f73-5f6b-a5ed-20c9c7cb47f5",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "746c857a-3f73-5f6b-a5ed-20c9c7cb47f5"
    ]
  }
]

To express $kW,$ we multiply each entry of $W$ by $k,$ as follows:

$$
\begin{aligned}kW & =k\begin{bmatrix}2 & 0 & 0 \\ 0 & 7 & -3 \\ 11 & -1 & 3\end{bmatrix} \\  & =\begin{bmatrix}2k & 0 & 0 \\ 0 & 7k & -3k \\ 11k & -k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kW$ in the problem statement:

$$
\begin{bmatrix}2k & 0 & 0 \\ 0 & 7k & -3k \\ 11k & -k & 3k\end{bmatrix}=\begin{bmatrix}-18 & 0 & 0 \\ 0 & -63 & 27 \\ -99 & 9 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $2$ and column $2$, $7k$ and $-63.$ Equating these elements, we get

$$
\begin{aligned}7k & =-63 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-320551 1,2

If $kW=\begin{bmatrix}-18 & 0 & 0 \\ 0 & -63 & 27 \\ -99 & 9 & -27\end{bmatrix}$,
where $W=\begin{bmatrix}2 & 0 & 0 \\ 0 & 7 & -3 \\ 11 & -1 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "34375e0a-ff6e-5529-a2f7-e17d62565e78",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "3f98c49a-d980-52ed-ae30-954db9d8e2a2",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "3f98c49a-d980-52ed-ae30-954db9d8e2a2"
    ]
  }
]

To express $kW,$ we multiply each entry of $W$ by $k,$ as follows:

$$
\begin{aligned}kW & =k\begin{bmatrix}2 & 0 & 0 \\ 0 & 7 & -3 \\ 11 & -1 & 3\end{bmatrix} \\  & =\begin{bmatrix}2k & 0 & 0 \\ 0 & 7k & -3k \\ 11k & -k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kW$ in the problem statement:

$$
\begin{bmatrix}2k & 0 & 0 \\ 0 & 7k & -3k \\ 11k & -k & 3k\end{bmatrix}=\begin{bmatrix}-18 & 0 & 0 \\ 0 & -63 & 27 \\ -99 & 9 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $2$ and column $3$, $-3k$ and $27.$ Equating these elements, we get

$$
\begin{aligned}-3k & =27 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-320551 2,0

If $kW=\begin{bmatrix}-18 & 0 & 0 \\ 0 & -63 & 27 \\ -99 & 9 & -27\end{bmatrix}$,
where $W=\begin{bmatrix}2 & 0 & 0 \\ 0 & 7 & -3 \\ 11 & -1 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "26da7105-bafe-5ee8-a3bd-12232119f60e",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "319b7819-5ad7-5c8b-97cf-c29eecd376fa",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "319b7819-5ad7-5c8b-97cf-c29eecd376fa"
    ]
  }
]

To express $kW,$ we multiply each entry of $W$ by $k,$ as follows:

$$
\begin{aligned}kW & =k\begin{bmatrix}2 & 0 & 0 \\ 0 & 7 & -3 \\ 11 & -1 & 3\end{bmatrix} \\  & =\begin{bmatrix}2k & 0 & 0 \\ 0 & 7k & -3k \\ 11k & -k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kW$ in the problem statement:

$$
\begin{bmatrix}2k & 0 & 0 \\ 0 & 7k & -3k \\ 11k & -k & 3k\end{bmatrix}=\begin{bmatrix}-18 & 0 & 0 \\ 0 & -63 & 27 \\ -99 & 9 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the  leftmost elements of the third row, $11k$ and $-99.$ Equating these elements, we get

$$
\begin{aligned}11k & =-99 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-320551 2,1

If $kW=\begin{bmatrix}-18 & 0 & 0 \\ 0 & -63 & 27 \\ -99 & 9 & -27\end{bmatrix}$,
where $W=\begin{bmatrix}2 & 0 & 0 \\ 0 & 7 & -3 \\ 11 & -1 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "80ea0d47-c855-5980-8cb8-0aa007630848",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "c1cf00c5-8cf2-5b0f-a67b-3b6f183a41cf",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "c1cf00c5-8cf2-5b0f-a67b-3b6f183a41cf"
    ]
  }
]

To express $kW,$ we multiply each entry of $W$ by $k,$ as follows:

$$
\begin{aligned}kW & =k\begin{bmatrix}2 & 0 & 0 \\ 0 & 7 & -3 \\ 11 & -1 & 3\end{bmatrix} \\  & =\begin{bmatrix}2k & 0 & 0 \\ 0 & 7k & -3k \\ 11k & -k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kW$ in the problem statement:

$$
\begin{bmatrix}2k & 0 & 0 \\ 0 & 7k & -3k \\ 11k & -k & 3k\end{bmatrix}=\begin{bmatrix}-18 & 0 & 0 \\ 0 & -63 & 27 \\ -99 & 9 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $3$ and column $2$, $-k$ and $9.$ Equating these elements, we get

$$
\begin{aligned}-k & =9 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-320551 2,2

If $kW=\begin{bmatrix}-18 & 0 & 0 \\ 0 & -63 & 27 \\ -99 & 9 & -27\end{bmatrix}$,
where $W=\begin{bmatrix}2 & 0 & 0 \\ 0 & 7 & -3 \\ 11 & -1 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "e31ff660-b407-5fd1-acce-009be3ed8695",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "adbf7fcd-a709-5e33-8852-c3d5ffaa1ce6",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "adbf7fcd-a709-5e33-8852-c3d5ffaa1ce6"
    ]
  }
]

To express $kW,$ we multiply each entry of $W$ by $k,$ as follows:

$$
\begin{aligned}kW & =k\begin{bmatrix}2 & 0 & 0 \\ 0 & 7 & -3 \\ 11 & -1 & 3\end{bmatrix} \\  & =\begin{bmatrix}2k & 0 & 0 \\ 0 & 7k & -3k \\ 11k & -k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kW$ in the problem statement:

$$
\begin{bmatrix}2k & 0 & 0 \\ 0 & 7k & -3k \\ 11k & -k & 3k\end{bmatrix}=\begin{bmatrix}-18 & 0 & 0 \\ 0 & -63 & 27 \\ -99 & 9 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $3$ and column $3$, $3k$ and $-27.$ Equating these elements, we get

$$
\begin{aligned}3k & =-27 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-320563 0,0

If $kB=\begin{bmatrix}-18 & 63 & -27\end{bmatrix}$,
where $B=\begin{bmatrix}2 & -7 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "2fb12c7f-1637-5627-a684-d2c7a0634d1d",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "f134cb84-55fc-5c69-8a4f-1bf6259d8aa6",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "f134cb84-55fc-5c69-8a4f-1bf6259d8aa6"
    ]
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}2 & -7 & 3\end{bmatrix} \\  & =\begin{bmatrix}2k & -7k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}2k & -7k & 3k\end{bmatrix}=\begin{bmatrix}-18 & 63 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $1$, $2k$ and $-18.$ Equating these elements, we get

$$
\begin{aligned}2k & =-18 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-320563 0,1

If $kB=\begin{bmatrix}-18 & 63 & -27\end{bmatrix}$,
where $B=\begin{bmatrix}2 & -7 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "075a28fc-3a19-505a-8549-b5a036bc5e20",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "d41cd22e-9d71-524a-b219-efb85edfe47d",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "d41cd22e-9d71-524a-b219-efb85edfe47d"
    ]
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}2 & -7 & 3\end{bmatrix} \\  & =\begin{bmatrix}2k & -7k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}2k & -7k & 3k\end{bmatrix}=\begin{bmatrix}-18 & 63 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $2$, $-7k$ and $63.$ Equating these elements, we get

$$
\begin{aligned}-7k & =63 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-320563 0,2

If $kB=\begin{bmatrix}-18 & 63 & -27\end{bmatrix}$,
where $B=\begin{bmatrix}2 & -7 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

$k=$
{{field-1}}

[
  {
    ":answer-field/id": "783f7ba8-ec24-5544-b9d2-e1f19b28fa2f",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/id": "51153ddb-0c9e-5f28-afa1-2b01a7e16392",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "51153ddb-0c9e-5f28-afa1-2b01a7e16392"
    ]
  }
]

To express $kB,$ we multiply each entry of $B$ by $k,$ as follows:

$$
\begin{aligned}kB & =k\begin{bmatrix}2 & -7 & 3\end{bmatrix} \\  & =\begin{bmatrix}2k & -7k & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kB$ in the problem statement:

$$
\begin{bmatrix}2k & -7k & 3k\end{bmatrix}=\begin{bmatrix}-18 & 63 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the rightmost elements, $3k$ and $-27.$ Equating these elements, we get

$$
\begin{aligned}3k & =-27 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-69670 0,0

If $kS=\begin{bmatrix}18 & -63 \\ 0 & -27\end{bmatrix}$,
where $S=\begin{bmatrix}-2 & 7 \\ 0 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "05c9aeb9-938f-5810-8236-73dbc5a865ca",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "418d785e-65a1-55d2-b62b-7a1951ceb088",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-36"
      },
      {
        ":answer/id": "b9154b01-a638-56a0-9108-eb5681cbb767",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-\\frac{1}{9}"
      },
      {
        ":answer/id": "b56048d6-a560-50f7-9757-45348a11abea",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=16"
      },
      {
        ":answer/id": "c5afa06e-a9e8-53af-bd91-00dd29ce936e",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=20"
      },
      {
        ":answer/id": "08be40ee-fa25-5d34-bc0e-47f62c2f557c",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "08be40ee-fa25-5d34-bc0e-47f62c2f557c"
    ]
  }
]

To express $kS,$ we multiply each entry of $S$ by $k,$ as follows:

$$
\begin{aligned}kS & =k\begin{bmatrix}-2 & 7 \\ 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}-2k & 7k \\ 0 & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kS$ in the problem statement:

$$
\begin{bmatrix}-2k & 7k \\ 0 & 3k\end{bmatrix}=\begin{bmatrix}18 & -63 \\ 0 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the top-left elements, $-2k$ and $18.$ Equating these elements, we get

$$
\begin{aligned}-2k & =18 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-69670 0,1

If $kS=\begin{bmatrix}18 & -63 \\ 0 & -27\end{bmatrix}$,
where $S=\begin{bmatrix}-2 & 7 \\ 0 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "0730fbc6-504f-526e-9615-5d37d7864ffd",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "c8f98367-1e6d-520f-b11f-323a4595c389",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-441"
      },
      {
        ":answer/id": "fdd5708c-5823-5f55-ae66-7b101c64f342",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-\\frac{1}{9}"
      },
      {
        ":answer/id": "4d12504b-f746-598b-a465-ab7dc26c2489",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-56"
      },
      {
        ":answer/id": "9ed16655-bd2b-58cd-bd35-bcfade54d73a",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-70"
      },
      {
        ":answer/id": "e9b836a5-918b-5c95-94b6-d5cb09916e8b",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "e9b836a5-918b-5c95-94b6-d5cb09916e8b"
    ]
  }
]

To express $kS,$ we multiply each entry of $S$ by $k,$ as follows:

$$
\begin{aligned}kS & =k\begin{bmatrix}-2 & 7 \\ 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}-2k & 7k \\ 0 & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kS$ in the problem statement:

$$
\begin{bmatrix}-2k & 7k \\ 0 & 3k\end{bmatrix}=\begin{bmatrix}18 & -63 \\ 0 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $1$ and column $2$, $7k$ and $-63.$ Equating these elements, we get

$$
\begin{aligned}7k & =-63 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.

## Held data target q-69670 1,1

If $kS=\begin{bmatrix}18 & -63 \\ 0 & -27\end{bmatrix}$,
where $S=\begin{bmatrix}-2 & 7 \\ 0 & 3\end{bmatrix}$
and $k$ is a scalar, calculate the value of $k.$

[
  {
    ":answer-field/id": "b1bfa2ba-c20d-54ff-af65-d83067946572",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/id": "e876dc4c-819b-5657-955e-2943af2c2dc1",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-81"
      },
      {
        ":answer/id": "45132b37-7677-5ff5-96ed-849d0fb1ae94",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-\\frac{1}{9}"
      },
      {
        ":answer/id": "051424a3-9580-5fc1-a69c-144f39873d38",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-24"
      },
      {
        ":answer/id": "f19b6f88-df57-59bb-afbc-d1b0a4edb94e",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-30"
      },
      {
        ":answer/id": "3990ac0b-dbea-5f5d-b907-cb502b06ccd0",
        ":answer/type": ":answer.type/math",
        ":answer/value": "k=-9"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "3990ac0b-dbea-5f5d-b907-cb502b06ccd0"
    ]
  }
]

To express $kS,$ we multiply each entry of $S$ by $k,$ as follows:

$$
\begin{aligned}kS & =k\begin{bmatrix}-2 & 7 \\ 0 & 3\end{bmatrix} \\  & =\begin{bmatrix}-2k & 7k \\ 0 & 3k\end{bmatrix}\end{aligned}
$$

Now, we set the above result equal to the matrix given for $kS$ in the problem statement:

$$
\begin{bmatrix}-2k & 7k \\ 0 & 3k\end{bmatrix}=\begin{bmatrix}18 & -63 \\ 0 & -27\end{bmatrix}
$$

We can solve for $k$ by equating any two corresponding (nonzero) elements. Let's choose the elements in row $2$ and column $2$, $3k$ and $-27.$ Equating these elements, we get

$$
\begin{aligned}3k & =-27 \\ k & =-9.\end{aligned}
$$

**Note:** We would still get the same result if we chose any other two corresponding (nonzero) elements.
