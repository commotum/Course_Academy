# Original replays and normal variants

Original MA grades are retained; easy and unrated circle completion are authored calibrations.


## q-122478 — original raw replay

Suppose $\displaystyle \int_{C_{1}}f(x, y)ds = 2$ for some function $f(x, y)$, where $C_{1}$ is parametrized by $r_{1}(t) = ⟨t, t^{2}⟩$ for $0 \le t \le 1$.

Which of the following must be true?

1. $\displaystyle \int_{-C_{1}}f(x, y)ds =-2$
2. $\displaystyle \int_{-C_{1}}f(x, y)ds = 2$
3. $\displaystyle \int_{C_{2}}f(x, y)ds = 4$, where $C_{2}$ is parametrized by $r_{2}(u) = ⟨2u, 4u^{2}⟩$ for $0 \le u \le \frac{1}{2}$.

[Absent in captured original.]

[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "III only",
        ":answer/id": "99784edc-4f16-5358-95de-f5431c754ebf"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I only",
        ":answer/id": "c4c73538-2099-5148-badc-86547de05aed"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I and III only",
        ":answer/id": "db896aa2-0682-5437-b2e1-ea3b32cb813b"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "II only",
        ":answer/id": "8fa8db2e-c151-5498-bdd1-6858221ebac2"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "II and III only",
        ":answer/id": "fcfa9a77-aed6-5fda-89f6-dfb238e4c887"
      }
    ],
    ":answer-field/id": "60412669-0f56-55df-b098-fa16a293e978"
  }
]


## q-122478 — generated normal variant

Suppose $\displaystyle \int_{C_{1}}f(x, y)ds = -7$ for some function $f(x, y)$, where $C_{1}$ is parametrized by $r_{1}(t) = ⟨t, t^{2}⟩$ for $0 \le t \le 1$.

Which of the following must be true?

1. $\displaystyle \int_{-C_{1}}f(x, y)ds =7$
2. $\displaystyle \int_{-C_{1}}f(x, y)ds = -7$
3. $\displaystyle \int_{C_{2}}f(x, y)ds = -14$, where $C_{2}$ is parametrized by $r_{2}(u) = ⟨2u, 4u^{2}⟩$ for $0 \le u \le \frac{1}{2}$.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false, while statement II is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=-7.
$$

- Statement III is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=-7.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
y={x}^{2},\,0\le x\le 1.
$$

Therefore, the correct answer is "II only."

[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I only",
        ":answer/id": "9cbbbf6d-1e7d-5f3f-ad98-ebce673414ed"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I and III only",
        ":answer/id": "3efe40fd-6067-559c-9eec-16753fc5919f"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "II and III only",
        ":answer/id": "b46d0f95-6ba0-5f51-bd02-0854158d8ba6"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "II only",
        ":answer/id": "d0d12b86-44b1-59fa-bb18-2efcc18473ef"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "III only",
        ":answer/id": "784bf83c-a55a-5191-a900-a646d4f5c675"
      }
    ],
    ":answer-field/id": "7ba69f10-7113-5253-8682-5cbd92d03972",
    ":answer-field/correct": [
      ":answer/id",
      "d0d12b86-44b1-59fa-bb18-2efcc18473ef"
    ]
  }
]


## q-122478 — generated normal variant

Suppose $\displaystyle \int_{C_{1}}f(x, y)ds = 5$ for some function $f(x, y)$, where $C_{1}$ is parametrized by $r_{1}(t) = ⟨t, 6t^{2}⟩$ for $0 \le t \le 4$.

Which of the following must be true?

1. $\displaystyle \int_{-C_{1}}f(x, y)ds =-5$
2. $\displaystyle \int_{-C_{1}}f(x, y)ds = 5$
3. $\displaystyle \int_{C_{2}}f(x, y)ds = 25$, where $C_{2}$ is parametrized by $r_{2}(u) = ⟨5u, 150u^{2}⟩$ for $0 \le u \le \frac{4}{5}$.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false, while statement II is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=5.
$$

- Statement III is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=5.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
y=6{x}^{2},\,0\le x\le 4.
$$

Therefore, the correct answer is "II only."

[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I only",
        ":answer/id": "40d3a955-4916-5535-9c2b-e817ad9a9e5d"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I and III only",
        ":answer/id": "74ec7dfc-ff10-5ac3-a736-483bc0441e04"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "II and III only",
        ":answer/id": "7e39dda7-db0b-5190-a11d-6d435630dc22"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "II only",
        ":answer/id": "6b73eb39-18e5-5e1d-baf4-8b693d01622a"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "III only",
        ":answer/id": "e733cc03-6f41-54ee-b942-520186e9e226"
      }
    ],
    ":answer-field/id": "aab8fd9b-8be4-58af-9c9d-be66f8d8db53",
    ":answer-field/correct": [
      ":answer/id",
      "6b73eb39-18e5-5e1d-baf4-8b693d01622a"
    ]
  }
]


## q-122571 — original raw replay

Consider the curves $C_{1}$ and $C_{2}$, defined parametrically as follows:

$\begin{bmatrix}C_{1}:r_{1}(t)|= ⟨\sin t, \cos t⟩, & 0 \le t \le 2π \\ C_{2}:r_{2}(θ)|= ⟨\sin 2θ, \cos 2θ⟩, & 0 \le θ \le π\end{bmatrix}$

Now suppose $\displaystyle \int_{C_{1}}f(x, y)ds = k$ for some function $f(x, y)$ and real number $k$. Which of the following must be true?

1. $\displaystyle \int_{-C_{1}}f(x, y)ds = k$
2. $\displaystyle \int_{C_{2}}f(x, y)ds = k$
3. $\displaystyle \int_{C_{2}}f(x, y)ds = \frac{1}{2}k$

[Absent in captured original.]

[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "II and III only",
        ":answer/id": "3e6c0541-032d-523a-b179-6db86feef8a8"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "II only",
        ":answer/id": "3c9dd03a-3d63-5434-8ce8-7d5808d384e5"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I only",
        ":answer/id": "2c2467a3-d3f3-5167-ab4d-6645d124aa30"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I and III only",
        ":answer/id": "a34ec6ca-aeac-5f89-9534-9dba1a74fb5c"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I and II only",
        ":answer/id": "a4d34b04-ac46-54b7-b036-fd403c9251e3"
      }
    ],
    ":answer-field/id": "0764a24b-ad28-5b86-bef0-758261ffb590"
  }
]


## q-122571 — generated normal variant

Consider the curves $C_{1}$ and $C_{2}$, defined parametrically as follows:

$\begin{aligned}C_{1}:r_{1}(t) &= ⟨\sin t, \cos t⟩, & 0 \le t \le 2π \\ C_{2}:r_{2}(θ) &= ⟨\sin 2θ, \cos 2θ⟩, & 0 \le θ \le π\end{aligned}$

Now suppose $\displaystyle \int_{C_{1}}f(x, y)ds = k$ for some function $f(x, y)$ and real number $k$. Which of the following must be true?

1. $\displaystyle \int_{-C_{1}}f(x, y)ds = k$
2. $\displaystyle \int_{C_{2}}f(x, y)ds = k$
3. $\displaystyle \int_{C_{2}}f(x, y)ds = \frac{1}{2}k$

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement II is true, while statement III is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=k.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we note that both parameterizations traverse a circle of radius $1$ centered at $O$ between $0$ and $2\pi .$

- Statement I is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=k.
$$

Therefore, the correct answer is "I and II only."

[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "II only",
        ":answer/id": "b3a8257d-dfec-5284-ac9f-7ac0bdfdc2d3"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I only",
        ":answer/id": "4a7112e4-8b66-5bba-ae44-04ee5b72dba6"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I and II only",
        ":answer/id": "2ad1e75a-4e59-5fc8-8011-160afe81049e"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I and III only",
        ":answer/id": "6ccb33df-deee-5e85-a5b8-1c96c384f2b3"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "II and III only",
        ":answer/id": "cd075a75-e4cd-5575-a3be-33c2e4b61156"
      }
    ],
    ":answer-field/id": "e47e5bfc-04ec-523a-9455-de0a1dc94dfc",
    ":answer-field/correct": [
      ":answer/id",
      "2ad1e75a-4e59-5fc8-8011-160afe81049e"
    ]
  }
]


## q-122571 — generated normal variant

Consider the curves $C_{1}$ and $C_{2}$, defined parametrically as follows:

$\begin{aligned}C_{1}:r_{1}(t) &= ⟨12\sin t, 12\cos t⟩, & 0 \le t \le 2π \\ C_{2}:r_{2}(θ) &= ⟨12\sin 5θ, 12\cos 5θ⟩, & 0 \le θ \le \frac{2\pi}{5}\end{aligned}$

Now suppose $\displaystyle \int_{C_{1}}f(x, y)ds = k$ for some function $f(x, y)$ and real number $k$. Which of the following must be true?

1. $\displaystyle \int_{-C_{1}}f(x, y)ds = k$
2. $\displaystyle \int_{C_{2}}f(x, y)ds = k$
3. $\displaystyle \int_{C_{2}}f(x, y)ds = \frac{1}{5}k$

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement II is true, while statement III is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=k.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we note that both parameterizations traverse a circle of radius $12$ centered at $O$ between $0$ and $2\pi .$

- Statement I is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=k.
$$

Therefore, the correct answer is "I and II only."

[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "II only",
        ":answer/id": "d90f4056-05a5-5810-ab5b-a6327ab25cb6"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I only",
        ":answer/id": "06c7c427-9b92-5ee1-938f-f9eb348873a6"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I and II only",
        ":answer/id": "a40afce8-08b6-58cd-88c2-f5ec80d49ce6"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "I and III only",
        ":answer/id": "09a990d9-de61-5c33-bd84-1aeabbf61240"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "II and III only",
        ":answer/id": "c0dc1e22-acbe-52f0-92ce-a216a6476e34"
      }
    ],
    ":answer-field/id": "22aa4ea1-8264-5964-bfee-eee1d1e4e9b2",
    ":answer-field/correct": [
      ":answer/id",
      "a40afce8-08b6-58cd-88c2-f5ec80d49ce6"
    ]
  }
]


## q-122814 — original raw replay

Suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=4$ for some function $f(x,y),$ where ${C}_{1}$ is parametrized by ${r}_{1}(t)=⟨{t}^{4}-3{t}^{2},\,t⟩$ for $0\le t\le 2.$

Which of the following must be true?
- **I.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-4$
- **II.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=8,$ where ${C}_{2}$ is parametrized by ${r}_{2}(u)=⟨16{u}^{4}-12{u}^{2},\,2u⟩$ for $0\le u\le 1.$
- **III.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=4$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false, while statement III is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=4.
$$

- Statement II is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=4.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
x={y}^{4}-3{y}^{2},\,0\le y\le 2.
$$

Therefore, the correct answer is "III only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "ae0b722f-cf26-5c77-a5a0-8124759fb09b"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "cec182a8-a6c8-5bde-a615-29649bcdafcc"
      }
    ],
    ":answer-field/id": "7a35fb31-a9ce-5573-ab07-aa217c9f72fe",
    ":answer-field/correct": [
      ":answer/id",
      "ae0b722f-cf26-5c77-a5a0-8124759fb09b"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "7cdb5696-7813-5093-a83a-aef891010c47"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "a67c8526-51ab-595f-af4f-5cf31f540892"
      }
    ],
    ":answer-field/id": "cf9b1f9b-47c4-5a91-8d2c-941859e7cf1b",
    ":answer-field/correct": [
      ":answer/id",
      "7cdb5696-7813-5093-a83a-aef891010c47"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "66b4954d-20c7-5af5-8ae6-5577ec194edc"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "bb170738-f70e-58a8-846f-b9c41d3bcc64"
      }
    ],
    ":answer-field/id": "a38b1e35-63ac-5c83-a335-3d7948be4a20",
    ":answer-field/correct": [
      ":answer/id",
      "66b4954d-20c7-5af5-8ae6-5577ec194edc"
    ]
  }
]


## q-122814 — generated normal variant

Suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=5$ for some function $f(x,y),$ where ${C}_{1}$ is parametrized by ${r}_{1}(t)=⟨{t}^{4}-{t}^{2},\,t⟩$ for $0\le t\le 2.$

Which of the following must be true?
- **I.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-5$
- **II.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=10,$ where ${C}_{2}$ is parametrized by ${r}_{2}(u)=⟨16{u}^{4}-4{u}^{2},\,2u⟩$ for $0\le u\le 1.$
- **III.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=5$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false, while statement III is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=5.
$$

- Statement II is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=5.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
x={y}^{4}-{y}^{2},\,0\le y\le 2.
$$

Therefore, the correct answer is "III only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "edc9de9b-1126-528c-a7c5-e5321e8fd4fc"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "203d6da6-0953-5a6c-8bc5-e81113baa687"
      }
    ],
    ":answer-field/id": "3dbfdb93-3fea-5738-92d9-56e845222401",
    ":answer-field/correct": [
      ":answer/id",
      "edc9de9b-1126-528c-a7c5-e5321e8fd4fc"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "db2000e9-9450-52ff-9146-9a1d08a07a18"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "1db39a9f-f11d-55b5-8ec3-56645c7bb7ab"
      }
    ],
    ":answer-field/id": "31bf0bc3-dae6-509b-bbb0-83ad93a8b04f",
    ":answer-field/correct": [
      ":answer/id",
      "db2000e9-9450-52ff-9146-9a1d08a07a18"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "4f545164-655e-5868-8358-eed48f02c466"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "fa630544-9014-5ebb-be40-cf9e6b432e2a"
      }
    ],
    ":answer-field/id": "4580f3b4-1570-55cc-86d5-9d0bc9888e57",
    ":answer-field/correct": [
      ":answer/id",
      "4f545164-655e-5868-8358-eed48f02c466"
    ]
  }
]


## q-122814 — generated normal variant

Suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=8$ for some function $f(x,y),$ where ${C}_{1}$ is parametrized by ${r}_{1}(t)=⟨3{t}^{4}-6{t}^{2},\,t⟩$ for $0\le t\le 6.$

Which of the following must be true?
- **I.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-8$
- **II.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=48,$ where ${C}_{2}$ is parametrized by ${r}_{2}(u)=⟨3888{u}^{4}-216{u}^{2},\,6u⟩$ for $0\le u\le 1.$
- **III.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=8$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false, while statement III is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=8.
$$

- Statement II is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=8.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
x=3{y}^{4}-6{y}^{2},\,0\le y\le 6.
$$

Therefore, the correct answer is "III only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "6abe8677-8c66-5bd5-b68f-ff34bd2b7492"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "b0fa0d4d-9f0b-522b-945a-87f92ca60b4d"
      }
    ],
    ":answer-field/id": "ed034512-bede-596f-b0cd-794c67bd06fb",
    ":answer-field/correct": [
      ":answer/id",
      "6abe8677-8c66-5bd5-b68f-ff34bd2b7492"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "68a228c6-c5d4-50d6-aade-6050910ed3c7"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "f7c92b77-d267-5ef9-bd72-eefbe8114b67"
      }
    ],
    ":answer-field/id": "c286fcbd-ae22-59b4-b2aa-215f94bd828f",
    ":answer-field/correct": [
      ":answer/id",
      "68a228c6-c5d4-50d6-aade-6050910ed3c7"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "336468d5-c705-5b13-8e65-0d9902ecd4b9"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "0b703b20-eb1a-56be-a2fb-7a46f1662b19"
      }
    ],
    ":answer-field/id": "d73b3a69-5df1-510b-a20d-346cde6c81c4",
    ":answer-field/correct": [
      ":answer/id",
      "336468d5-c705-5b13-8e65-0d9902ecd4b9"
    ]
  }
]


## q-122815 — original raw replay

Suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=1$ for some function $f(x,y),$ where ${C}_{1}$ is parametrized by ${r}_{1}(u)=⟨\operatorname{cos}⁡(\frac{u}{2}),\,\operatorname{sin}⁡(\frac{u}{2})⟩$ for $0\le u\le 2\pi .$ 

Which of the following must be true?
- **I.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=2,$ where ${C}_{2}$ is parametrized by ${r}_{2}(t)=⟨\operatorname{cos}⁡t,\,\operatorname{sin}⁡t⟩$ for $0\le t\le \pi .$
- **II.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-1$
- **III.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=1$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=1.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we note that both parameterizations traverse a half-circle of radius $1$ centered at $O$ between $0$ and $\pi .$

- Statement II is false, while statement III is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=1.
$$

Therefore, the correct answer is "III only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "1aeb96d9-6ca5-5bb3-928a-89f5595f6579"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "f6c8e7f0-17b0-50d6-bfd9-64500bc59af9"
      }
    ],
    ":answer-field/id": "791b7d89-dcd6-5fd0-9997-b241a7bb84fe",
    ":answer-field/correct": [
      ":answer/id",
      "1aeb96d9-6ca5-5bb3-928a-89f5595f6579"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "6f5c90be-9185-5bb3-8468-f333856ea8fb"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "de0c743b-88b2-57de-a8ab-e987e2b44076"
      }
    ],
    ":answer-field/id": "33fcbd0f-2c19-55b8-906c-0e2dc2e4ce23",
    ":answer-field/correct": [
      ":answer/id",
      "6f5c90be-9185-5bb3-8468-f333856ea8fb"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "7753c9d9-3c2d-57f5-b87e-0a53c6402c25"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "f86bab50-e3c3-58aa-9916-5c3d4a2bf264"
      }
    ],
    ":answer-field/id": "1fd29cfd-26fd-5d3c-aeb8-12af45ad06e3",
    ":answer-field/correct": [
      ":answer/id",
      "7753c9d9-3c2d-57f5-b87e-0a53c6402c25"
    ]
  }
]


## q-122815 — generated normal variant

Suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=-5$ for some function $f(x,y),$ where ${C}_{1}$ is parametrized by ${r}_{1}(u)=⟨\operatorname{cos}⁡(\frac{u}{2}),\,\operatorname{sin}⁡(\frac{u}{2})⟩$ for $0\le u\le 2\pi .$ 

Which of the following must be true?
- **I.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=-10,$ where ${C}_{2}$ is parametrized by ${r}_{2}(t)=⟨\operatorname{cos}⁡t,\,\operatorname{sin}⁡t⟩$ for $0\le t\le \pi .$
- **II.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=5$
- **III.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-5$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=-5.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we note that both parameterizations traverse a half-circle of radius $1$ centered at $O$ between $0$ and $\pi .$

- Statement II is false, while statement III is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=-5.
$$

Therefore, the correct answer is "III only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "eb47a392-c489-52e1-87b9-2133d7877a60"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "ad9d48bd-8d84-5fe6-b39a-762f006e5ee6"
      }
    ],
    ":answer-field/id": "5d110f22-2a55-54bc-b1ed-55e2f7ce94be",
    ":answer-field/correct": [
      ":answer/id",
      "eb47a392-c489-52e1-87b9-2133d7877a60"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "ba4ec572-1671-51e8-95ba-f5709d872fa6"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "27d9d2f4-d747-5396-a5b8-1d3837cca3cc"
      }
    ],
    ":answer-field/id": "c45ae806-a140-5510-9127-a4610ba89802",
    ":answer-field/correct": [
      ":answer/id",
      "ba4ec572-1671-51e8-95ba-f5709d872fa6"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "239534b2-7354-5327-abee-dcafe5d6735f"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "f663dadb-0d33-5ef9-9390-0444e9bb043a"
      }
    ],
    ":answer-field/id": "ce7285d9-d477-5abb-8b4e-e8b53db83e6e",
    ":answer-field/correct": [
      ":answer/id",
      "239534b2-7354-5327-abee-dcafe5d6735f"
    ]
  }
]


## q-122815 — generated normal variant

Suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=4$ for some function $f(x,y),$ where ${C}_{1}$ is parametrized by ${r}_{1}(u)=⟨12\operatorname{cos}⁡(\frac{u}{4}),\,12\operatorname{sin}⁡(\frac{u}{4})⟩$ for $0\le u\le 4\pi .$ 

Which of the following must be true?
- **I.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=48,$ where ${C}_{2}$ is parametrized by ${r}_{2}(t)=⟨12\operatorname{cos}⁡3t,\,12\operatorname{sin}⁡3t⟩$ for $0\le t\le \frac{\pi}{3} .$
- **II.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-4$
- **III.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=4$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=4.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we note that both parameterizations traverse a half-circle of radius $12$ centered at $O$ between $0$ and $\pi .$

- Statement II is false, while statement III is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=4.
$$

Therefore, the correct answer is "III only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "9b2730ff-c0a7-5faf-978d-a1093cb85e2a"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "143ec71b-13e9-54a4-b844-949ae1369f1a"
      }
    ],
    ":answer-field/id": "b8324785-9061-5c4c-9e18-542e891a86b6",
    ":answer-field/correct": [
      ":answer/id",
      "9b2730ff-c0a7-5faf-978d-a1093cb85e2a"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "023aa903-85e1-51c5-8099-fa26607bd543"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "c2bb660d-ed27-5e1c-a386-dc6390a83c27"
      }
    ],
    ":answer-field/id": "49307450-9da7-58fc-b16b-1c4e3198f16e",
    ":answer-field/correct": [
      ":answer/id",
      "023aa903-85e1-51c5-8099-fa26607bd543"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "42378fb6-64c1-50e8-9271-ebe7ea081ba2"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "52235751-aa26-5787-be83-67c30bcd1bce"
      }
    ],
    ":answer-field/id": "a871d8bb-d911-5d30-8510-4880680d342d",
    ":answer-field/correct": [
      ":answer/id",
      "42378fb6-64c1-50e8-9271-ebe7ea081ba2"
    ]
  }
]


## q-122816 — original raw replay

Suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=3$ for some function $f(x,y),$ where ${C}_{1}$ is parametrized by ${r}_{1}(t)=⟨t,\,{t}^{3/2}⟩$ for $0\le t\le 4.$

Which of the following must be true?
- **I.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=3$
- **II.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-3$
- **III.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=12,$ where ${C}_{2}$ is parametrized by ${r}_{2}(u)=⟨4u,\,8{u}^{3/2}⟩$ for $0\le u\le 1.$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is true, while statement II is false. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=3.
$$

- Statement III is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=3.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
y={x}^{3/2},\,0\le x\le 4.
$$

Therefore, the correct answer is "I only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "44060da7-5152-5bde-8e84-9dfcf31d4ca5"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "2217d387-a01f-5977-8ba2-0dc3f56f4ece"
      }
    ],
    ":answer-field/id": "b2b704d4-66bf-5397-84cb-10c1eb66fdb7",
    ":answer-field/correct": [
      ":answer/id",
      "2217d387-a01f-5977-8ba2-0dc3f56f4ece"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "cd086a35-adb4-509c-a53e-e60e507204cb"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "105cf9c7-2e54-52cf-a93e-96965df323e0"
      }
    ],
    ":answer-field/id": "861cca10-118e-5dfd-9614-6f30c0f5e22b",
    ":answer-field/correct": [
      ":answer/id",
      "cd086a35-adb4-509c-a53e-e60e507204cb"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "127c22ac-5212-5a66-ada0-e469d27c360b"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "b840651a-4605-57d1-927e-68c2c9560ce4"
      }
    ],
    ":answer-field/id": "dbf577fb-eeb5-5ea6-a7f6-e18ddf94107f",
    ":answer-field/correct": [
      ":answer/id",
      "b840651a-4605-57d1-927e-68c2c9560ce4"
    ]
  }
]


## q-122816 — generated normal variant

Suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=2$ for some function $f(x,y),$ where ${C}_{1}$ is parametrized by ${r}_{1}(t)=⟨t,\,{t}^{3/2}⟩$ for $0\le t\le 4.$

Which of the following must be true?
- **I.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=2$
- **II.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-2$
- **III.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=8,$ where ${C}_{2}$ is parametrized by ${r}_{2}(u)=⟨4u,\,8{u}^{3/2}⟩$ for $0\le u\le 1.$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is true, while statement II is false. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=2.
$$

- Statement III is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=2.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
y={x}^{3/2},\,0\le x\le 4.
$$

Therefore, the correct answer is "I only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "d8686a94-b0de-54b6-9f0b-4acc5c79bc16"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "9222af70-d870-59b6-b90f-75e927dbe458"
      }
    ],
    ":answer-field/id": "4903c52f-e81d-584c-9d5d-849750af912e",
    ":answer-field/correct": [
      ":answer/id",
      "9222af70-d870-59b6-b90f-75e927dbe458"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "e341c007-f700-555c-a560-ceb54076deea"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "3c596ee5-4271-5b17-8dac-60f2dd490192"
      }
    ],
    ":answer-field/id": "a0481898-8e47-5039-83a3-eb67ca803222",
    ":answer-field/correct": [
      ":answer/id",
      "e341c007-f700-555c-a560-ceb54076deea"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "35817233-809d-544c-a977-0d53695bfa19"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "0c341dcc-3f63-5c6c-83a3-3ec9cbf5be61"
      }
    ],
    ":answer-field/id": "367c92da-385f-553b-9a95-8354ebfedf4d",
    ":answer-field/correct": [
      ":answer/id",
      "0c341dcc-3f63-5c6c-83a3-3ec9cbf5be61"
    ]
  }
]


## q-122816 — generated normal variant

Suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=9$ for some function $f(x,y),$ where ${C}_{1}$ is parametrized by ${r}_{1}(t)=⟨t,\,5{t}^{3/2}⟩$ for $0\le t\le 16.$

Which of the following must be true?
- **I.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=9$
- **II.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-9$
- **III.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=144,$ where ${C}_{2}$ is parametrized by ${r}_{2}(u)=⟨16u,\,320{u}^{3/2}⟩$ for $0\le u\le 1.$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is true, while statement II is false. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=9.
$$

- Statement III is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=9.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
y=5{x}^{3/2},\,0\le x\le 16.
$$

Therefore, the correct answer is "I only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "db6f4f63-4060-5b7f-bb88-6298868c5c78"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "1cf38802-3e0f-52fe-ada0-0ae5f6e8f0f3"
      }
    ],
    ":answer-field/id": "034ff5a7-ed94-561c-8e43-d660cfd73f06",
    ":answer-field/correct": [
      ":answer/id",
      "1cf38802-3e0f-52fe-ada0-0ae5f6e8f0f3"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "79943aeb-e5d5-588b-8ef5-4044b22cce6d"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "96701f7c-54fa-5938-9e57-b9d07eb52376"
      }
    ],
    ":answer-field/id": "3c7e13dd-db5c-57c3-9699-b652be873df4",
    ":answer-field/correct": [
      ":answer/id",
      "79943aeb-e5d5-588b-8ef5-4044b22cce6d"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "36c3ef39-8405-5c6e-9dc7-0571b35a1308"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "625a9a85-71ba-55dc-ba36-719514c7a42b"
      }
    ],
    ":answer-field/id": "e8da4ef9-d36e-5437-aad8-37c3a609ad00",
    ":answer-field/correct": [
      ":answer/id",
      "625a9a85-71ba-55dc-ba36-719514c7a42b"
    ]
  }
]


## q-122851 — original raw replay

Consider the curves ${C}_{1}$ and ${C}_{2},$ defined parametrically as follows:

$$
\begin{aligned}{C}_{1}:\,{r}_{1}(t) & =⟨\sqrt{9{t}^{2}+1},\,3t⟩, & 0\le t\le \frac{1}{3} \\ {C}_{2}:\,{r}_{2}(u) & =⟨\sqrt{4{u}^{2}+1},\,2u⟩, & 0\le u\le \frac{1}{2}\end{aligned}
$$

Now suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=k$ for some function $f(x,y)$ and real number $k.$ Which of the following must be true?
- **I.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-k$
- **II.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=\frac{2k}{3}$
- **III.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=k$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=k.
$$

- Statement II is false, while statement III is true. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=k.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
x=\sqrt{{y}^{2}+1},\,0\le y\le 1.
$$

Therefore, the correct answer is "III only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "64a48869-a7ea-5657-bd12-934014fe72d8"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "ec05016b-0425-5b69-b2ac-6b7ed6852dd8"
      }
    ],
    ":answer-field/id": "010f3bd2-7013-5637-9766-686fd0763046",
    ":answer-field/correct": [
      ":answer/id",
      "64a48869-a7ea-5657-bd12-934014fe72d8"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "6dbda171-988d-5497-b4a2-44e804e441ef"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "5a9e1a2d-4d4d-511f-b010-a6563f7074d5"
      }
    ],
    ":answer-field/id": "e5faab86-bff2-5389-8cc0-081dac2f132d",
    ":answer-field/correct": [
      ":answer/id",
      "6dbda171-988d-5497-b4a2-44e804e441ef"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "3508d762-7ae7-5690-a1b5-ee990a9bff5e"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "4bb09f88-190d-55d8-abf4-18f8a6796653"
      }
    ],
    ":answer-field/id": "5b9a0813-f745-50f1-89ab-052e9b7704a6",
    ":answer-field/correct": [
      ":answer/id",
      "3508d762-7ae7-5690-a1b5-ee990a9bff5e"
    ]
  }
]


## q-122851 — generated normal variant

Consider the curves ${C}_{1}$ and ${C}_{2},$ defined parametrically as follows:

$$
\begin{aligned}{C}_{1}:\,{r}_{1}(t) & =⟨\sqrt{9{t}^{2}+1},\,3t⟩, & 0\le t\le \frac{1}{3} \\ {C}_{2}:\,{r}_{2}(u) & =⟨\sqrt{16{u}^{2}+1},\,4u⟩, & 0\le u\le \frac{1}{4}\end{aligned}
$$

Now suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=k$ for some function $f(x,y)$ and real number $k.$ Which of the following must be true?
- **I.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-k$
- **II.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=\frac{4k}{3}$
- **III.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=k$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=k.
$$

- Statement II is false, while statement III is true. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=k.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
x=\sqrt{{y}^{2}+1},\,0\le y\le 1.
$$

Therefore, the correct answer is "III only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "0e67a673-9f53-5e49-a037-a249b0dd88cc"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "6e072fd3-0a6c-5af3-bb5e-ef6bdc02e4e7"
      }
    ],
    ":answer-field/id": "704ecc03-a1b9-5e3d-9606-dcb9a89b5dbd",
    ":answer-field/correct": [
      ":answer/id",
      "0e67a673-9f53-5e49-a037-a249b0dd88cc"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "b8ffb64e-e63b-57ee-b837-9eab33052622"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "38c14a01-055f-5fca-bc37-2965d9dfdc2c"
      }
    ],
    ":answer-field/id": "0d03c786-4ad5-597b-bd29-2e5054ccf036",
    ":answer-field/correct": [
      ":answer/id",
      "b8ffb64e-e63b-57ee-b837-9eab33052622"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "bf1530ed-c882-55b7-bcfd-3693d7c66a64"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "2b11248c-e5bf-59c5-9a41-cc01fbade378"
      }
    ],
    ":answer-field/id": "535b3c4b-7d87-585e-860c-3ce529552061",
    ":answer-field/correct": [
      ":answer/id",
      "bf1530ed-c882-55b7-bcfd-3693d7c66a64"
    ]
  }
]


## q-122851 — generated normal variant

Consider the curves ${C}_{1}$ and ${C}_{2},$ defined parametrically as follows:

$$
\begin{aligned}{C}_{1}:\,{r}_{1}(t) & =⟨\sqrt{9{t}^{2}+9},\,3t⟩, & 0\le t\le \frac{5}{3} \\ {C}_{2}:\,{r}_{2}(u) & =⟨\sqrt{16{u}^{2}+9},\,4u⟩, & 0\le u\le \frac{5}{4}\end{aligned}
$$

Now suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=k$ for some function $f(x,y)$ and real number $k.$ Which of the following must be true?
- **I.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=-k$
- **II.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=\frac{4k}{3}$
- **III.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=k$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is false. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=k.
$$

- Statement II is false, while statement III is true. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=k.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
x=\sqrt{{y}^{2}+9},\,0\le y\le 5.
$$

Therefore, the correct answer is "III only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "9beb63a3-3dab-51da-a751-58bee96e6aed"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "175c5d0e-6f7b-5293-b488-9844dcd74947"
      }
    ],
    ":answer-field/id": "19494321-fb17-526d-a6e5-d0c6265e1544",
    ":answer-field/correct": [
      ":answer/id",
      "9beb63a3-3dab-51da-a751-58bee96e6aed"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "b20b6f24-d2e0-56c9-8951-842e783891eb"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "2c204783-5206-5515-8492-8a52df7b6fcd"
      }
    ],
    ":answer-field/id": "0cf608bf-ade1-5139-938e-28321aa94e1f",
    ":answer-field/correct": [
      ":answer/id",
      "b20b6f24-d2e0-56c9-8951-842e783891eb"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "6d20b12a-417b-5eb4-972c-19cedac0b77a"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "73d8d536-2c4b-54fd-9f2b-19ad27604148"
      }
    ],
    ":answer-field/id": "633fffdf-5f59-567b-9728-eb549aa22795",
    ":answer-field/correct": [
      ":answer/id",
      "6d20b12a-417b-5eb4-972c-19cedac0b77a"
    ]
  }
]


## q-122868 — original raw replay

Consider the curves ${C}_{1}$ and ${C}_{2},$ defined parametrically as follows:

$$
\begin{aligned}{C}_{1}:\,{r}_{1}(t) & =⟨2t,\,2\sqrt{t}⟩, & 0\le t\le 2 \\ {C}_{2}:\,{r}_{2}(u) & =⟨4u,\,2\sqrt{2u}⟩, & 0\le u\le 1\end{aligned}
$$

Now suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=k$ for some function $f(x,y)$ and real number $k.$ Which of the following must be true?
- **I.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=k$
- **II.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=2k$
- **III.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=k$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is true, while statement II is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=k.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
y=\sqrt{2x},\,0\le x\le 4.
$$

- Statement III is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=k.
$$

Therefore, the correct answer is "I and III only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "7c13b371-2f8d-5c3e-b70c-0661dfcf3502"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "b9b87a7e-5ce0-5cce-ad00-a6853b801be1"
      }
    ],
    ":answer-field/id": "cce511ee-e8af-591e-b22e-b2c6dc370e50",
    ":answer-field/correct": [
      ":answer/id",
      "b9b87a7e-5ce0-5cce-ad00-a6853b801be1"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "1ead5a06-e12f-5d87-b4b9-5bec35458799"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "9dd0e7cf-264d-5d62-9d20-9a609f993615"
      }
    ],
    ":answer-field/id": "51895633-608e-59da-b447-a16b0c5658c2",
    ":answer-field/correct": [
      ":answer/id",
      "1ead5a06-e12f-5d87-b4b9-5bec35458799"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "81dd390e-0a40-5074-b4aa-6b797be4ccee"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "98e59d93-a8f8-5cb4-a88a-e01bce407374"
      }
    ],
    ":answer-field/id": "c521b727-f9e2-5daf-9735-60b0a72eccd3",
    ":answer-field/correct": [
      ":answer/id",
      "81dd390e-0a40-5074-b4aa-6b797be4ccee"
    ]
  }
]


## q-122868 — generated normal variant

Consider the curves ${C}_{1}$ and ${C}_{2},$ defined parametrically as follows:

$$
\begin{aligned}{C}_{1}:\,{r}_{1}(t) & =⟨2t,\,2\sqrt{t}⟩, & 0\le t\le 2 \\ {C}_{2}:\,{r}_{2}(u) & =⟨8u,\,2\sqrt{4u}⟩, & 0\le u\le \frac{1}{2}\end{aligned}
$$

Now suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=k$ for some function $f(x,y)$ and real number $k.$ Which of the following must be true?
- **I.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=k$
- **II.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=4k$
- **III.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=k$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is true, while statement II is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=k.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
y=\sqrt{2x},\,0\le x\le 4.
$$

- Statement III is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=k.
$$

Therefore, the correct answer is "I and III only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "f3ac011a-f151-582e-8d03-4e0333473670"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "7c997843-f6a5-55a1-824b-8ac909331d66"
      }
    ],
    ":answer-field/id": "621d94ce-d615-5de9-94be-dd9184067025",
    ":answer-field/correct": [
      ":answer/id",
      "7c997843-f6a5-55a1-824b-8ac909331d66"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "d6cffc74-938c-5e5d-84e2-fa20608c2086"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "354ec05d-485c-587e-8ad1-0da11f6be4ef"
      }
    ],
    ":answer-field/id": "362d0cdd-214f-59c0-8869-fb0597f105b2",
    ":answer-field/correct": [
      ":answer/id",
      "d6cffc74-938c-5e5d-84e2-fa20608c2086"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "726e5a7d-65e8-5ee8-9727-b8e985560f87"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "ccb659e8-b0b7-5c8b-9fa6-56c046979528"
      }
    ],
    ":answer-field/id": "c5a04009-f8fa-5b98-a523-3d83fa20b372",
    ":answer-field/correct": [
      ":answer/id",
      "726e5a7d-65e8-5ee8-9727-b8e985560f87"
    ]
  }
]


## q-122868 — generated normal variant

Consider the curves ${C}_{1}$ and ${C}_{2},$ defined parametrically as follows:

$$
\begin{aligned}{C}_{1}:\,{r}_{1}(t) & =⟨6t,\,6\sqrt{t}⟩, & 0\le t\le 5 \\ {C}_{2}:\,{r}_{2}(u) & =⟨18u,\,6\sqrt{3u}⟩, & 0\le u\le \frac{5}{3}\end{aligned}
$$

Now suppose ${\int }_{{C}_{1}}f(x,y)\,\text{d}s=k$ for some function $f(x,y)$ and real number $k.$ Which of the following must be true?
- **I.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=k$
- **II.** ${\int }_{{C}_{2}}f(x,y)\,\text{d}s=3k$
- **III.** ${\int }_{-{C}_{1}}f(x,y)\,\text{d}s=k$

Select all that apply.

Line integrals with respect to arc length are independent of the choice of parametrization and orientation.

With that in mind, let's examine each statement. 

- Statement I is true, while statement II is false. Notice that ${C}_{1}$ and ${C}_{2}$ are different parameterizations of the same curve. Since line integrals with respect to arc length are independent of the choice of parameterization, we have

$$
{\int }_{{C}_{2}}f(x,y)\,\text{d}s=k.
$$

 
To see that ${C}_{1}$ and ${C}_{2}$ represent the same curve, we can convert each parametrization to Cartesian form. In doing so, we find that both parameterizations give the Cartesian curve

$$
y=\sqrt{6x},\,0\le x\le 30.
$$

- Statement III is true. Reversing the curve's orientation does *not* change the value of a line integral with respect to arc length. Therefore, we have

$$
{\int }_{-{C}_{1}}f(x,y)\,\text{d}s={\int }_{{C}_{1}}f(x,y)\,\text{d}s=k.
$$

Therefore, the correct answer is "I and III only."

[
  {
    ":answer-field/key": "I",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "a746b18f-3f9f-5d43-9b71-7f1186c90e67"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "c008fd39-a248-5713-a62e-10167de01643"
      }
    ],
    ":answer-field/id": "93145d21-f709-513b-8934-bb78bd072ae2",
    ":answer-field/correct": [
      ":answer/id",
      "c008fd39-a248-5713-a62e-10167de01643"
    ]
  },
  {
    ":answer-field/key": "II",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "a4497a6b-f69b-50bc-bc32-4cbc53ca776e"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "52ef3629-14f5-5dd9-aca3-0d13830a2f7f"
      }
    ],
    ":answer-field/id": "3380fabf-1ce7-52bc-ad6a-86d81b081dc6",
    ":answer-field/correct": [
      ":answer/id",
      "a4497a6b-f69b-50bc-bc32-4cbc53ca776e"
    ]
  },
  {
    ":answer-field/key": "III",
    ":answer-field/type": ":answer-field.type/checkbox",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "true",
        ":answer/id": "b661550f-7ad0-5d78-86b0-2fc9aeabcf9e"
      },
      {
        ":answer/type": ":answer.type/text",
        ":answer/value": "false",
        ":answer/id": "eba4a9ee-fa9b-5d37-bf44-fec252687331"
      }
    ],
    ":answer-field/id": "36eda92a-5663-5619-b846-ef6ad61ed2fd",
    ":answer-field/correct": [
      ":answer/id",
      "b661550f-7ad0-5d78-86b0-2fc9aeabcf9e"
    ]
  }
]
