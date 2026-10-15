Consider the matrices

$$
A=\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix},\,B=\begin{bmatrix}-\frac{1}{4} & -\frac{3}{4} \\ \frac{1}{2} & -\frac{1}{2}\end{bmatrix},\,C=\begin{bmatrix}-\frac{1}{4} & -\frac{3}{4} \\ \frac{1}{2} & \frac{1}{2}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix}\begin{bmatrix}-\frac{1}{4} & -\frac{3}{4} \\ \frac{1}{2} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}∗ & -3 \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is false too.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix}\begin{bmatrix}-\frac{1}{4} & -\frac{3}{4} \\ \frac{1}{2} & \frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}-\frac{1}{4} & -\frac{3}{4} \\ \frac{1}{2} & \frac{1}{2}\end{bmatrix}\begin{bmatrix}2 & 3 \\ -2 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II only".

[
  {
    ":answer-field/id": "7c803419-9276-5165-ad10-b381828948dd",
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "b810c8f7-229d-5d40-870f-c3f8060e47b4",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "dd41e147-a87c-5d39-a698-0e9166154903",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "dd41e147-a87c-5d39-a698-0e9166154903"
    ]
  },
  {
    ":answer-field/id": "7bf2a116-d332-5fa5-ad24-fee13aeeef9b",
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "4b99ab47-f438-51cf-94cf-68be9d817c07",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "18d2458d-fd3e-5dae-847c-b5a4feb35268",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "18d2458d-fd3e-5dae-847c-b5a4feb35268"
    ]
  },
  {
    ":answer-field/id": "ac68011a-f137-563c-8e51-d7912bc0cadd",
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "649b88e8-36eb-535a-9d7d-c616e3706841",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "612eaedc-bb65-5c1d-9229-3394e9e42ac1",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "612eaedc-bb65-5c1d-9229-3394e9e42ac1"
    ]
  }
]

---

Consider the matrices

$$
A=\begin{bmatrix}-2 & 1 \\ -2 & -1\end{bmatrix},\,B=\begin{bmatrix}-\frac{1}{4} & -\frac{1}{4} \\ \frac{1}{2} & -\frac{1}{2}\end{bmatrix},\,C=\begin{bmatrix}-\frac{1}{4} & \frac{1}{2} \\ -\frac{1}{4} & -\frac{1}{2}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $C\ne {A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-2 & 1 \\ -2 & -1\end{bmatrix}\begin{bmatrix}-\frac{1}{4} & -\frac{1}{4} \\ \frac{1}{2} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}-\frac{1}{4} & -\frac{1}{4} \\ \frac{1}{2} & -\frac{1}{2}\end{bmatrix}\begin{bmatrix}-2 & 1 \\ -2 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-2 & 1 \\ -2 & -1\end{bmatrix}\begin{bmatrix}-\frac{1}{4} & \frac{1}{2} \\ -\frac{1}{4} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}\frac{1}{4} & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $C\ne {A}^{-1}$ and statement III is true.

Therefore, the correct answer is "I and III only".

[
  {
    ":answer-field/id": "3583ba2a-bb42-5b1a-b10d-98b42a330396",
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "e4092b17-5e2b-5dae-8d40-155034ad4c5c",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "af7d221a-e506-58c2-b708-2dc6e0aecacc",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "af7d221a-e506-58c2-b708-2dc6e0aecacc"
    ]
  },
  {
    ":answer-field/id": "30ed5c96-6ee0-5f39-93b3-2c433c407047",
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "c064270a-45b0-5d37-a64c-f9bd3cd9b591",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "fc515591-2d15-5fb3-814a-53134068b49e",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "fc515591-2d15-5fb3-814a-53134068b49e"
    ]
  },
  {
    ":answer-field/id": "48af3418-177d-51b4-8173-40bf69d832e1",
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "c58b7fa5-e8fb-56df-8329-c2b7be0a6bab",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "56893b98-2738-501f-917d-58a00ce969f4",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "c58b7fa5-e8fb-56df-8329-c2b7be0a6bab"
    ]
  }
]

---

Consider the matrices

$$
C=\begin{bmatrix}2 & -1 \\ 2 & -3\end{bmatrix},\,D=\begin{bmatrix}\frac{3}{4} & -\frac{1}{4} \\ \frac{1}{2} & -\frac{1}{2}\end{bmatrix},\,E=\begin{bmatrix}-3 & 1 \\ -2 & 2\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $CD=DC={I}_{2}$

- **II.** $DE=ED={I}_{2}$

- **III.** $D={C}^{-1}$

- First, we check whether $CD=DC={I}_{2}.$ Computing $CD$, we get

$$
\begin{aligned}CD & =\begin{bmatrix}2 & -1 \\ 2 & -3\end{bmatrix}\begin{bmatrix}\frac{3}{4} & -\frac{1}{4} \\ \frac{1}{2} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DC$, we get

$$
\begin{aligned}DC & =\begin{bmatrix}\frac{3}{4} & -\frac{1}{4} \\ \frac{1}{2} & -\frac{1}{2}\end{bmatrix}\begin{bmatrix}2 & -1 \\ 2 & -3\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $D={C}^{-1}$ and statement III is true too.

- Now, we check whether $DE=ED={I}_{2}.$ Computing $DE$, we get

$$
\begin{aligned}DE & =\begin{bmatrix}\frac{3}{4} & -\frac{1}{4} \\ \frac{1}{2} & -\frac{1}{2}\end{bmatrix}\begin{bmatrix}-3 & 1 \\ -2 & 2\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ \\ ∗ & -\frac{1}{2}\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".

[
  {
    ":answer-field/id": "70d7643b-6104-537f-a2f7-ea56fddc6fea",
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "c2c423f1-fa46-5046-b322-201462bc9092",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "9e9106c5-004e-5923-a1ee-f8a8ed480e8a",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "9e9106c5-004e-5923-a1ee-f8a8ed480e8a"
    ]
  },
  {
    ":answer-field/id": "6ee91bd2-1a95-558f-be1a-abb6d916f84b",
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "e9d8a19d-14c7-57f9-99cc-9cac0d153cd9",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "e1f18c79-3b49-530d-8454-86379c0b9403",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "e1f18c79-3b49-530d-8454-86379c0b9403"
    ]
  },
  {
    ":answer-field/id": "eb7d7075-905e-5751-8aff-80da43bf5d97",
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "6daf8fd9-1eff-5d73-b495-b7b1e84dd3ca",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "bc243859-b6cc-502a-bf95-259667fad729",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "6daf8fd9-1eff-5d73-b495-b7b1e84dd3ca"
    ]
  }
]

---

Consider the matrices

$$
E=\begin{bmatrix}-2 & -2 \\ 3 & 1\end{bmatrix},\,F=\begin{bmatrix}\frac{1}{4} & \frac{1}{2} \\ -\frac{3}{4} & -\frac{1}{2}\end{bmatrix},\,G=\begin{bmatrix}\frac{1}{4} & \frac{1}{2} \\ \frac{3}{4} & -\frac{1}{2}\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $EF=FE={I}_{2}$
- **II.** $EG=GE={I}_{2}$
- **III.** $G={E}^{-1}$

- First, we check whether $EF=FE={I}_{2}.$ Computing $EF$, we get

$$
\begin{aligned}EF & =\begin{bmatrix}-2 & -2 \\ 3 & 1\end{bmatrix}\begin{bmatrix}\frac{1}{4} & \frac{1}{2} \\ -\frac{3}{4} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $FE$, we get

$$
\begin{aligned}FE & =\begin{bmatrix}\frac{1}{4} & \frac{1}{2} \\ -\frac{3}{4} & -\frac{1}{2}\end{bmatrix}\begin{bmatrix}-2 & -2 \\ 3 & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $EG=GE={I}_{2}.$ Computing $EG$, we get

$$
\begin{aligned}EG & =\begin{bmatrix}-2 & -2 \\ 3 & 1\end{bmatrix}\begin{bmatrix}\frac{1}{4} & \frac{1}{2} \\ \frac{3}{4} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ \\ \frac{3}{2} & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $G\ne {E}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".

[
  {
    ":answer-field/id": "5b8c5578-01e3-5343-9d4f-ceab9a95811c",
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "bd898e4d-5a1c-5b90-9026-8badc38ea15a",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "af6e0e43-fe72-533d-8ce8-b52921a85d3e",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "af6e0e43-fe72-533d-8ce8-b52921a85d3e"
    ]
  },
  {
    ":answer-field/id": "7f089b2b-28ab-5800-9e30-9367b30f8877",
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "c4677bc8-584e-5a37-8e85-d19023d4fd41",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "9fd317b7-c798-5691-b1ba-0c74608dec81",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "c4677bc8-584e-5a37-8e85-d19023d4fd41"
    ]
  },
  {
    ":answer-field/id": "e1e6cee0-56d4-5f73-a00c-baa130261c3e",
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "ea9329d8-1756-5b87-ba25-77527208f215",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "e13b5f01-cf51-5c98-9332-666698fbdfbd",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "e13b5f01-cf51-5c98-9332-666698fbdfbd"
    ]
  }
]

---

Consider the matrices

$$
A=\begin{bmatrix}-1 & -1 \\ 3 & -1\end{bmatrix},\,B=\begin{bmatrix}-\frac{1}{4} & -\frac{3}{4} \\ \frac{1}{4} & -\frac{1}{4}\end{bmatrix},\,C=\begin{bmatrix}-\frac{1}{4} & \frac{1}{4} \\ -\frac{3}{4} & -\frac{1}{4}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $C={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-1 & -1 \\ 3 & -1\end{bmatrix}\begin{bmatrix}-\frac{1}{4} & -\frac{3}{4} \\ \frac{1}{4} & -\frac{1}{4}\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ \\ -1 & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-1 & -1 \\ 3 & -1\end{bmatrix}\begin{bmatrix}-\frac{1}{4} & \frac{1}{4} \\ -\frac{3}{4} & -\frac{1}{4}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}-\frac{1}{4} & \frac{1}{4} \\ -\frac{3}{4} & -\frac{1}{4}\end{bmatrix}\begin{bmatrix}-1 & -1 \\ 3 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $C={A}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".

[
  {
    ":answer-field/id": "ec8284a8-0bf3-544a-9c54-cec969c7eca3",
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "16f19bf8-5330-5aec-a447-97d784a2f670",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "8ad1cbe5-05ab-50d4-a52f-2752023f71df",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "16f19bf8-5330-5aec-a447-97d784a2f670"
    ]
  },
  {
    ":answer-field/id": "13d4c9e5-cfb7-5da5-a46f-651c8e8beaf2",
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "58cf03af-8176-5bb0-b78f-02e392065bcc",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "ae2bfeeb-8629-57aa-9218-a109b80f97f7",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "ae2bfeeb-8629-57aa-9218-a109b80f97f7"
    ]
  },
  {
    ":answer-field/id": "c8de493c-224a-5509-ba23-047e3c23f50d",
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "b9235f58-a9e8-5ebf-aaec-2e2f7723f631",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "5f11ee68-1cd3-56f2-85d3-5aada7c69161",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "b9235f58-a9e8-5ebf-aaec-2e2f7723f631"
    ]
  }
]

---

Consider the matrices

$$
A=\begin{bmatrix}-1 & -\frac{3}{2} \\ -1 & \frac{1}{2}\end{bmatrix},\,B=\begin{bmatrix}-\frac{1}{4} & \frac{3}{4} \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix},\,C=\begin{bmatrix}-\frac{1}{4} & -\frac{3}{4} \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $B={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-1 & -\frac{3}{2} \\ -1 & \frac{1}{2}\end{bmatrix}\begin{bmatrix}-\frac{1}{4} & \frac{3}{4} \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ \\ ∗ & -\frac{1}{2}\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false. As a result, $B\ne {A}^{-1}$ and statement III is false too.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-1 & -\frac{3}{2} \\ -1 & \frac{1}{2}\end{bmatrix}\begin{bmatrix}-\frac{1}{4} & -\frac{3}{4} \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}-\frac{1}{4} & -\frac{3}{4} \\ -\frac{1}{2} & \frac{1}{2}\end{bmatrix}\begin{bmatrix}-1 & -\frac{3}{2} \\ -1 & \frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true.

Therefore, the correct answer is "II only".

[
  {
    ":answer-field/id": "352475c6-893f-5d15-8bd4-4fc7d65c9b40",
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "bf82865b-b7f8-5978-a65d-6ceaeecc7985",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "d2c67902-8586-522d-8128-26d6372edb3c",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "d2c67902-8586-522d-8128-26d6372edb3c"
    ]
  },
  {
    ":answer-field/id": "5aac40eb-e4b1-5a40-92f2-d09ca0cd77c3",
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "e8f869e2-c759-591a-9c02-906bc98f760f",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "e9e346c7-807b-58b0-9826-de71aa5abe49",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "e9e346c7-807b-58b0-9826-de71aa5abe49"
    ]
  },
  {
    ":answer-field/id": "765fa93c-fc92-5c91-8fc2-7219896e12df",
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "ae4cf946-1ca5-5f24-9b50-8c5503ce3a04",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "023a940e-0586-53bb-85a2-7d425b0cf6a9",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "023a940e-0586-53bb-85a2-7d425b0cf6a9"
    ]
  }
]

---

Consider the matrices

$$
A=\begin{bmatrix}\frac{1}{3} & \frac{2}{3} \\ 1 & -\frac{1}{2}\end{bmatrix},\,B=\begin{bmatrix}\frac{3}{5} & \frac{4}{5} \\ \frac{6}{5} & -\frac{2}{5}\end{bmatrix},\,C=\begin{bmatrix}\frac{3}{5} & \frac{6}{5} \\ \frac{4}{5} & -\frac{2}{5}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $C\ne {A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}\frac{1}{3} & \frac{2}{3} \\ 1 & -\frac{1}{2}\end{bmatrix}\begin{bmatrix}\frac{3}{5} & \frac{4}{5} \\ \frac{6}{5} & -\frac{2}{5}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $BA$, we get

$$
\begin{aligned}BA & =\begin{bmatrix}\frac{3}{5} & \frac{4}{5} \\ \frac{6}{5} & -\frac{2}{5}\end{bmatrix}\begin{bmatrix}\frac{1}{3} & \frac{2}{3} \\ 1 & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}\frac{1}{3} & \frac{2}{3} \\ 1 & -\frac{1}{2}\end{bmatrix}\begin{bmatrix}\frac{3}{5} & \frac{6}{5} \\ \frac{4}{5} & -\frac{2}{5}\end{bmatrix} \\  & =\begin{bmatrix}∗ & \frac{2}{15} \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $C\ne {A}^{-1}$ and statement III is true.

Therefore, the correct answer is "I and III only".

[
  {
    ":answer-field/id": "d9e9e3af-3b8c-5fe9-9bf6-926f2aefd6ba",
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "e59853dc-024a-5613-8bda-a7a5ad6a4077",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "539f2745-380c-5c87-9c4b-698d2d8a5ae1",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "e59853dc-024a-5613-8bda-a7a5ad6a4077"
    ]
  },
  {
    ":answer-field/id": "8f860d9c-0f4b-51cc-941b-fa8e0bb36f8f",
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "35a0f523-b1e4-57b4-8986-3d408f116ada",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "4f30ad3a-ebca-54d0-80d8-eb5e24d49530",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "4f30ad3a-ebca-54d0-80d8-eb5e24d49530"
    ]
  },
  {
    ":answer-field/id": "e71d7935-1ded-546e-be49-1b0bba791d94",
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "1373a24c-5358-54bd-954f-2cee9ede5935",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "d2d87237-4b30-5309-9ba1-cf6d51133951",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "d2d87237-4b30-5309-9ba1-cf6d51133951"
    ]
  }
]

---

Consider the matrices

$$
C=\begin{bmatrix}\frac{1}{2} & -\frac{2}{3} \\ -\frac{3}{2} & 1\end{bmatrix},\,D=\begin{bmatrix}-2 & -\frac{4}{3} \\ -3 & -1\end{bmatrix},\,E=\begin{bmatrix}1 & \frac{2}{3} \\ \frac{3}{2} & \frac{1}{2}\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $CD=DC={I}_{2}$

- **II.** $DE=ED={I}_{2}$

- **III.** $D={C}^{-1}$

- First, we check whether $CD=DC={I}_{2}.$ Computing $CD$, we get

$$
\begin{aligned}CD & =\begin{bmatrix}\frac{1}{2} & -\frac{2}{3} \\ -\frac{3}{2} & 1\end{bmatrix}\begin{bmatrix}-2 & -\frac{4}{3} \\ -3 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $DC$, we get

$$
\begin{aligned}DC & =\begin{bmatrix}-2 & -\frac{4}{3} \\ -3 & -1\end{bmatrix}\begin{bmatrix}\frac{1}{2} & -\frac{2}{3} \\ -\frac{3}{2} & 1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true. As a result, $D={C}^{-1}$ and statement III is true too.

- Now, we check whether $DE=ED={I}_{2}.$ Computing $DE$, we get

$$
\begin{aligned}DE & =\begin{bmatrix}-2 & -\frac{4}{3} \\ -3 & -1\end{bmatrix}\begin{bmatrix}1 & \frac{2}{3} \\ \frac{3}{2} & \frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}-4 & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false.

Therefore, the correct answer is "I and III only".

[
  {
    ":answer-field/id": "99d4eefb-99fe-57f0-b1dd-b1f21dc966d7",
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "5336188a-41c0-5ee3-b5ff-b215f42ed5a3",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "99f095f1-43c3-57d7-b82b-34e083cf0de1",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "99f095f1-43c3-57d7-b82b-34e083cf0de1"
    ]
  },
  {
    ":answer-field/id": "c6950a7a-77e0-5196-930a-37b6e5fb6219",
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "1fac1f39-7be8-5bdd-8437-10ddf03fd830",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "cadbd61f-38c2-5075-adb8-c50598a25814",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "1fac1f39-7be8-5bdd-8437-10ddf03fd830"
    ]
  },
  {
    ":answer-field/id": "00fcb256-4dfb-5083-89d1-c76082b6d89b",
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "eabda44b-f9a8-5f27-b2fa-00740c2ab541",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "696039bf-4b19-5cb1-b178-6b29548d1105",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "696039bf-4b19-5cb1-b178-6b29548d1105"
    ]
  }
]

---

Consider the matrices

$$
E=\begin{bmatrix}1 & -1 \\ \frac{3}{2} & -\frac{2}{3}\end{bmatrix},\,F=\begin{bmatrix}-\frac{4}{5} & \frac{6}{5} \\ -\frac{9}{5} & \frac{6}{5}\end{bmatrix},\,G=\begin{bmatrix}\frac{4}{5} & \frac{6}{5} \\ -\frac{9}{5} & \frac{6}{5}\end{bmatrix}.
$$

Which of the following statements are true?

Select all that apply.

- **I.** $EF=FE={I}_{2}$
- **II.** $EG=GE={I}_{2}$
- **III.** $G={E}^{-1}$

- First, we check whether $EF=FE={I}_{2}.$ Computing $EF$, we get

$$
\begin{aligned}EF & =\begin{bmatrix}1 & -1 \\ \frac{3}{2} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}-\frac{4}{5} & \frac{6}{5} \\ -\frac{9}{5} & \frac{6}{5}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $FE$, we get

$$
\begin{aligned}FE & =\begin{bmatrix}-\frac{4}{5} & \frac{6}{5} \\ -\frac{9}{5} & \frac{6}{5}\end{bmatrix}\begin{bmatrix}1 & -1 \\ \frac{3}{2} & -\frac{2}{3}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement I is true.

- Now, we check whether $EG=GE={I}_{2}.$ Computing $EG$, we get

$$
\begin{aligned}EG & =\begin{bmatrix}1 & -1 \\ \frac{3}{2} & -\frac{2}{3}\end{bmatrix}\begin{bmatrix}\frac{4}{5} & \frac{6}{5} \\ -\frac{9}{5} & \frac{6}{5}\end{bmatrix} \\  & =\begin{bmatrix}\frac{13}{5} & ∗ \\ ∗ & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement II is false. As a result, $G\ne {E}^{-1}$ and statement III is false too.

Therefore, the correct answer is "I only".

[
  {
    ":answer-field/id": "8f42970f-4984-520d-941e-e0592ead25ff",
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "7103b14f-02cf-5a7f-805e-a0dd3de7e261",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "a027df56-7799-5590-ae3e-34bad820b71b",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "7103b14f-02cf-5a7f-805e-a0dd3de7e261"
    ]
  },
  {
    ":answer-field/id": "efc99372-454a-53a1-8310-b02c6bdf8cea",
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "6e1002bb-1bee-5820-8a26-10c073faf6de",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "a6603c9f-0137-5233-b184-8534c9f0657b",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "6e1002bb-1bee-5820-8a26-10c073faf6de"
    ]
  },
  {
    ":answer-field/id": "012c00fa-4cb0-5960-a536-d71799c397f9",
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "3a595b9f-2009-5cbb-a94f-e043f6b53b8d",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "a8fa3fb1-f140-51b8-b6f4-7871b12200fe",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "3a595b9f-2009-5cbb-a94f-e043f6b53b8d"
    ]
  }
]

---

Consider the matrices

$$
A=\begin{bmatrix}-\frac{2}{3} & \frac{2}{3} \\ -1 & -1\end{bmatrix},\,B=\begin{bmatrix}-\frac{3}{4} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{2}\end{bmatrix},\,C=\begin{bmatrix}-\frac{3}{4} & -\frac{1}{2} \\ \frac{3}{4} & -\frac{1}{2}\end{bmatrix}.
$$

Which of the following statements are true?
- **I.** $AB=BA={I}_{2}$
- **II.** $AC=CA={I}_{2}$
- **III.** $C={A}^{-1}$

Select all that apply. If none apply, leave all boxes unchecked.

- First, we check whether $AB=BA={I}_{2}.$ Computing $AB$, we get

$$
\begin{aligned}AB & =\begin{bmatrix}-\frac{2}{3} & \frac{2}{3} \\ -1 & -1\end{bmatrix}\begin{bmatrix}-\frac{3}{4} & \frac{3}{4} \\ -\frac{1}{2} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}∗ & ∗ \\ \frac{5}{4} & ∗\end{bmatrix} \\  & \ne {I}_{2}.\,\times \end{aligned}
$$

So, statement I is false.

- Now, we check whether $AC=CA={I}_{2}.$ Computing $AC$, we get

$$
\begin{aligned}AC & =\begin{bmatrix}-\frac{2}{3} & \frac{2}{3} \\ -1 & -1\end{bmatrix}\begin{bmatrix}-\frac{3}{4} & -\frac{1}{2} \\ \frac{3}{4} & -\frac{1}{2}\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

Likewise, computing $CA$, we get

$$
\begin{aligned}CA & =\begin{bmatrix}-\frac{3}{4} & -\frac{1}{2} \\ \frac{3}{4} & -\frac{1}{2}\end{bmatrix}\begin{bmatrix}-\frac{2}{3} & \frac{2}{3} \\ -1 & -1\end{bmatrix} \\  & =\begin{bmatrix}1 & 0 \\ 0 & 1\end{bmatrix} \\  & ={I}_{2}.\,✓\end{aligned}
$$

So, statement II is true. As a result, $C={A}^{-1}$ and statement III is true too.

Therefore, the correct answer is "II and III only".

[
  {
    ":answer-field/id": "1281b5f6-888b-5076-9c9c-6a0a1e2ba68c",
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "bf65268d-df33-5a1f-9cae-9aa588043c0d",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      },
      {
        ":answer/id": "93963a8b-5efe-5721-9483-a5516fd22aaf",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "bf65268d-df33-5a1f-9cae-9aa588043c0d"
    ]
  },
  {
    ":answer-field/id": "9bb2ac6e-0288-5117-97c1-496add602f0a",
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "019f13c6-52ea-5ad2-ba8b-986d2c633b53",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "b5129bd9-eefd-510d-82da-6a82b0ccc061",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "019f13c6-52ea-5ad2-ba8b-986d2c633b53"
    ]
  },
  {
    ":answer-field/id": "0010b0e8-07d9-539f-b46c-d9a9cc6cbc1b",
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/id": "ac5ff699-83f3-5502-8863-b5603f0fa78e",
        ":answer/type": ":answer.type/text",
        ":answer/value": "true"
      },
      {
        ":answer/id": "d38a16ac-5ef0-5fbd-96ac-5b7ea626f6aa",
        ":answer/type": ":answer.type/text",
        ":answer/value": "false"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "ac5ff699-83f3-5502-8863-b5603f0fa78e"
    ]
  }
]