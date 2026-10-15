# Original source backbones and authored variants

Raw evidence remains in source-cases.json; supported replay and variable-slot rendering are separate.

## source-q-18787

Find the solution $(x,y)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}4x-5y &=0 \\ 2x-3y &=2\end{aligned}\right.
$$

*Hint: Eliminate the variable $x.$*

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "f9dc4fdb-fc7f-57b9-bbcb-171440bb6b43",
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-5,-4)",
        ":db/id": 17592186191189
      },
      {
        ":answer/id": "7891246f-146f-5da4-be15-343b7425f61f",
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-5,3)",
        ":db/id": 17592186508564
      },
      {
        ":answer/id": "8468d23b-6f42-50bf-9e79-d910d35e0ee2",
        ":answer/type": ":answer.type/math",
        ":answer/value": "(4,5)",
        ":db/id": 17592186508587
      },
      {
        ":answer/id": "ac47150e-5e39-5c69-9314-ddb4609e8210",
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-5,2)",
        ":db/id": 17592186508651
      },
      {
        ":answer/id": "f55c1c33-5ff5-5f10-90f5-08f56a27906c",
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-5,1)",
        ":db/id": 17592186508791
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "f9dc4fdb-fc7f-57b9-bbcb-171440bb6b43"
    ],
    ":answer-field/id": "3d02a81e-fa71-57d8-a298-b58e206ffcea",
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":db/id": 17592186191187
  }
]
```

Notice that the $x$-coefficient in the first equation is $4,$ while in the second equation it is $2.$ 

If we multiply the second equation by $-2,$ then the $x$-coefficient will become $-4,$ which will cancel with the coefficient of $4$ in the first equation.

$$
\left\{\begin{aligned}4x-5y &=0 \\ (\,2x-3y &=2\,)\,\times (-2)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}4x-5y &=0 \\ -4x+6y &=-4\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}\begin{aligned}\cancel{4x}-5y & =0 \\ -\cancel{4x}+6y & =-4 \\ (-5y+6y) & =(0-4) \\ y & =-4\end{aligned}\end{aligned}
$$

So, the solution must have $y=-4.$ However, we still need to find $x.$ To do this, we substitute $y=-4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}\begin{aligned}4x-5y & =0 \\ 4x-5(-4) & =0 \\ 4x+20 & =0 \\ 4x & =-20 \\ x & =-5\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-5,\,y=-4,$ which can be expressed as $(-5,-4).$

## source-q-208816

Consider the following system of equations:

$$
\left\{\begin{aligned}4x + 3y &=5 \\ -x + 7y &=-9\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $x$.

The solution is $($
{{field-1}}
$,$
{{field-2}}
$)$.

```json
[
  {
    ":answer-field/id": "1baa2398-4954-5c79-9541-1319e47e02cd",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":db/id": 17592186191226,
    ":answer-field/choices": [
      {
        ":answer/id": "0a2d306d-f360-56da-8e14-985ae3e0ad66",
        ":answer/type": ":answer.type/math",
        ":answer/value": "2"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "0a2d306d-f360-56da-8e14-985ae3e0ad66"
    ]
  },
  {
    ":answer-field/id": "652cda5c-8a31-5ce3-bccf-786c2da038cc",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":db/id": 17592186191227,
    ":answer-field/choices": [
      {
        ":answer/id": "2488282a-021b-59bb-8aea-895802898158",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1"
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "2488282a-021b-59bb-8aea-895802898158"
    ]
  }
]
```

Notice that the coefficient of $x$ in the first equation is $4$, while in the second equation it is $-1$.

If we multiply the second equation by $4$, then the $x$-coefficient will become $-4$, which will cancel with the coefficient of $4$ in the first equation.

$$
\left\{\begin{aligned}4x + 3y &=5 \\ \bigl(-x + 7y &=-9\bigr)\times\left(4\right)\end{aligned}\right.\;\Longrightarrow\;\left\{\begin{aligned}4x + 3y &=5 \\ -4x + 28y &=-36\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}
\cancel{4x} + 3y &= 5 \\
\cancel{-4x} + 28y &= -36 \\
(3y + 28y) &= (5 - 36) \\
31y &= -31 \\
y &= -1
\end{aligned}
$$

So, the solution must have $y = -1$. However, we still need to find $x.$ To do this, we substitute $y = -1$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}
-x + 7y &= -9 \\
-x + 7(-1) &= -9 \\
-x - 7 &= -9 \\
-x &= -2 \\
x &= 2
\end{aligned}
$$

Therefore, the solution to the system of equations is $x=2, \,y=-1$, which can be expressed as $(2,-1)$.

## source-q-238082

Consider the following system of equations:

$$
\left\{\begin{aligned}6x+13y &=21 \\ 2x+6y &=12\end{aligned}\right.
$$

The solution $(x,y)$ to this system is $($
{{field-1}}$\,,$
{{field-2}}
$).$

```json
[
  {
    ":answer-field/choices": [
      {
        ":answer/id": "9dddb3dd-6633-5329-a169-4b39e35735ca",
        ":answer/type": ":answer.type/math",
        ":answer/value": "-3",
        ":db/id": 17592186508628
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "9dddb3dd-6633-5329-a169-4b39e35735ca"
    ],
    ":answer-field/id": "2696769d-e344-58f2-b122-e8524fb62262",
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":db/id": 17592186508826
  },
  {
    ":answer-field/choices": [
      {
        ":answer/id": "5032cf38-f7e1-5f19-b56e-8d84bbbcec8a",
        ":answer/type": ":answer.type/math",
        ":answer/value": "3",
        ":db/id": 17592186508509
      }
    ],
    ":answer-field/correct": [
      ":answer/id",
      "5032cf38-f7e1-5f19-b56e-8d84bbbcec8a"
    ],
    ":answer-field/id": "2adc4195-f1d2-500e-8a09-82e4a8b25e53",
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":db/id": 17592186508827
  }
]
```

Notice that the coefficient of $x$ in the  first  equation is $6,$ while in the second equation it is $2.$ 

If we multiply the second equation by $-3,$ then the $x$-coefficient will become $-6,$ which will cancel with the coefficient of $6$ in the first equation.

$$
\left\{\begin{aligned}6x+13y &=21 \\ (\,2x+6y &=12\,)\,\times (-3)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}6x+13y &=21 \\ -6x-18y &=-36\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}\cancel{6x}+13y & =21 \\ -\cancel{6x}-18y & =-36 \\ (13y-18y) & =(21-36) \\ -5y & =-15 \\ y & =3\end{aligned}
$$

So, the solution must have $y=3.$ However, we still need to find $x.$ To do this, we substitute $y=3$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}6x+13y & =21 \\ 6x+13(3) & =21 \\ 6x+39 & =21 \\ 6x & =-18 \\ x & =-3\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-3,\,y=3,$ which can be expressed as $(-3,3).$

## easy-radio_solution

Find the solution $(s,t)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}-s+2t &=-4 \\ 5s+t &=9\end{aligned}\right.
$$

*Hint: Eliminate the variable $s.$*

```json
[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{102}{11}, \\frac{29}{11})",
        ":answer/id": "02e2354d-20a8-531a-825a-51672ebc7697"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(2, -1)",
        ":answer/id": "22d401c7-a142-51d7-9274-5a9a6fc7b22e"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(6, -1)",
        ":answer/id": "92babad3-9654-53fb-9754-a1939cb3a97c"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{54}{11}, \\frac{5}{11})",
        ":answer/id": "3fd17d09-e1d3-5bd1-ad36-c7b98cca9f53"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(- \\frac{10}{3}, - \\frac{11}{3})",
        ":answer/id": "8fdbf8f1-5bef-5ec6-8bc2-fd0335bb700b"
      }
    ],
    ":answer-field/id": "4b592bd6-7cda-5dbd-adab-229e3f3151fe",
    ":answer-field/correct": [
      ":answer/id",
      "22d401c7-a142-51d7-9274-5a9a6fc7b22e"
    ]
  }
]
```

Notice that the $s$-coefficient in the first equation is $-1,$ while in the second equation it is $5.$ 

If we multiply the first equation by $5,$ then the $s$-coefficient will become $-5,$ which will cancel with the coefficient of $5$ in the second equation.

$$
\left\{\begin{aligned}(\,-s+2t &=-4\,)\,\times (5) \\ 5s+t &=9\end{aligned}\right.\,⟹\,\left\{\begin{aligned}-5s+10t &=-20 \\ 5s+t &=9\end{aligned}\right.
$$

Now, when we add the two equations, the variable $s$ will be eliminated:

$$
\begin{aligned}\begin{aligned}-\cancel{5s}+10t & =-20 \\ \cancel{5s}+t & =9 \\ (10t+t) & =(-20+9) \\ 11t & =-11 \\ t & =-1\end{aligned}\end{aligned}
$$

So, the solution must have $t=-1.$ However, we still need to find $s.$ To do this, we substitute $t=-1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}\begin{aligned}-s+2t & =-4 \\ -s+2(-1) & =-4 \\ -s-2 & =-4 \\ -s & =-2 \\ s & =2\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $s=2,\,t=-1,$ which can be expressed as $(2,-1).$

## easy-radio_solution

Find the solution $(s,t)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}3s+t &=12 \\ -s+6t &=15\end{aligned}\right.
$$

*Hint: Eliminate the variable $s.$*

```json
[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{237}{7}, \\frac{57}{7})",
        ":answer/id": "589066c0-9b3b-573b-bb42-98312b05706a"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(- \\frac{483}{19}, - \\frac{33}{19})",
        ":answer/id": "fee952a2-194b-542b-b39a-51b1e1a91200"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-33, 3)",
        ":answer/id": "68b7ebfe-3ed6-5bb1-b217-4b1abda689e4"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(3, 3)",
        ":answer/id": "9703d0e3-8372-5ed2-89b8-ac1ad313de79"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(- \\frac{123}{19}, \\frac{27}{19})",
        ":answer/id": "2ad9d854-281d-5935-b42b-9a57f87816c7"
      }
    ],
    ":answer-field/id": "42c5a122-6b4e-563c-aec7-2497bb0f4764",
    ":answer-field/correct": [
      ":answer/id",
      "9703d0e3-8372-5ed2-89b8-ac1ad313de79"
    ]
  }
]
```

Notice that the $s$-coefficient in the first equation is $3,$ while in the second equation it is $-1.$ 

If we multiply the second equation by $3,$ then the $s$-coefficient will become $-3,$ which will cancel with the coefficient of $3$ in the first equation.

$$
\left\{\begin{aligned}3s+t &=12 \\ (\,-s+6t &=15\,)\,\times (3)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}3s+t &=12 \\ -3s+18t &=45\end{aligned}\right.
$$

Now, when we add the two equations, the variable $s$ will be eliminated:

$$
\begin{aligned}\begin{aligned}\cancel{3s}+t & =12 \\ -\cancel{3s}+18t & =45 \\ (t+18t) & =(12+45) \\ 19t & =57 \\ t & =3\end{aligned}\end{aligned}
$$

So, the solution must have $t=3.$ However, we still need to find $s.$ To do this, we substitute $t=3$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}\begin{aligned}3s+t & =12 \\ 3s+(3) & =12 \\ 3s+3 & =12 \\ 3s & =9 \\ s & =3\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $s=3,\,t=3,$ which can be expressed as $(3,3).$

## easy-radio_solution

Find the solution $(a,b)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}-2a+7b &=-5 \\ a-5b &=4\end{aligned}\right.
$$

*Hint: Eliminate the variable $a.$*

```json
[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{17}{3}, \\frac{1}{3})",
        ":answer/id": "a050793b-fd0f-5f15-9c9a-7e40d4f400bc"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{77}{3}, \\frac{13}{3})",
        ":answer/id": "108887cb-351e-5f76-ba40-b525b6aff975"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{23}{2}, \\frac{3}{2})",
        ":answer/id": "1f2f8116-ab3e-5873-ad4f-809dd589d06f"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-1, -1)",
        ":answer/id": "994a3d09-8658-53ec-a694-f1fa8b68ea2e"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(9, -1)",
        ":answer/id": "5ab2426f-dc8a-52cc-83c2-7904527a2dcc"
      }
    ],
    ":answer-field/id": "941340e5-2737-5132-8b19-f4c45e2e4f70",
    ":answer-field/correct": [
      ":answer/id",
      "994a3d09-8658-53ec-a694-f1fa8b68ea2e"
    ]
  }
]
```

Notice that the $a$-coefficient in the first equation is $-2,$ while in the second equation it is $1.$ 

If we multiply the second equation by $2,$ then the $a$-coefficient will become $2,$ which will cancel with the coefficient of $-2$ in the first equation.

$$
\left\{\begin{aligned}-2a+7b &=-5 \\ (\,a-5b &=4\,)\,\times (2)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}-2a+7b &=-5 \\ 2a-10b &=8\end{aligned}\right.
$$

Now, when we add the two equations, the variable $a$ will be eliminated:

$$
\begin{aligned}\begin{aligned}-\cancel{2a}+7b & =-5 \\ \cancel{2a}-10b & =8 \\ (7b-10b) & =(-5+8) \\ -3b & =3 \\ b & =-1\end{aligned}\end{aligned}
$$

So, the solution must have $b=-1.$ However, we still need to find $a.$ To do this, we substitute $b=-1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}\begin{aligned}-2a+7b & =-5 \\ -2a+7(-1) & =-5 \\ -2a-7 & =-5 \\ -2a & =2 \\ a & =-1\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-1,\,b=-1,$ which can be expressed as $(-1,-1).$

## easy-radio_solution

Find the solution $(x,y)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}3x+4y &=8 \\ x+3y &=11\end{aligned}\right.
$$

*Hint: Eliminate the variable $x.$*

```json
[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{112}{5}, - \\frac{19}{5})",
        ":answer/id": "b493b100-f88e-5a6d-88ed-ffc14a3257ee"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-4, 5)",
        ":answer/id": "589e263f-3248-5389-bb4a-b79d524f8fc6"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(26, 5)",
        ":answer/id": "9ccaa218-102a-5993-b1c7-43965a996c66"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{152}{7}, - \\frac{25}{7})",
        ":answer/id": "2798c37f-5144-5eba-aefc-758cc2fe905f"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{178}{5}, - \\frac{41}{5})",
        ":answer/id": "d17cc948-3dc4-555e-8495-38687ef8c3da"
      }
    ],
    ":answer-field/id": "f68c1968-3cf0-50ea-915f-481783015acc",
    ":answer-field/correct": [
      ":answer/id",
      "589e263f-3248-5389-bb4a-b79d524f8fc6"
    ]
  }
]
```

Notice that the $x$-coefficient in the first equation is $3,$ while in the second equation it is $1.$ 

If we multiply the second equation by $-3,$ then the $x$-coefficient will become $-3,$ which will cancel with the coefficient of $3$ in the first equation.

$$
\left\{\begin{aligned}3x+4y &=8 \\ (\,x+3y &=11\,)\,\times (-3)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}3x+4y &=8 \\ -3x-9y &=-33\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}\begin{aligned}\cancel{3x}+4y & =8 \\ -\cancel{3x}-9y & =-33 \\ (4y-9y) & =(8-33) \\ -5y & =-25 \\ y & =5\end{aligned}\end{aligned}
$$

So, the solution must have $y=5.$ However, we still need to find $x.$ To do this, we substitute $y=5$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}\begin{aligned}3x+4y & =8 \\ 3x+4(5) & =8 \\ 3x+20 & =8 \\ 3x & =-12 \\ x & =-4\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-4,\,y=5,$ which can be expressed as $(-4,5).$

## easy-blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}-s + 2t &=-4 \\ 5s + t &=9\end{aligned}\right.
$$

Find the solution $(s, t)$ to this system by eliminating the variable $s$.

The solution is $($
{{field-1}}
$,$
{{field-2}}
$)$.

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "2",
        ":answer/id": "12031297-fa2b-579c-a021-645548bb7b0c"
      }
    ],
    ":answer-field/id": "f5d35ecb-5ac4-5741-bcfe-eb6288aaf8d5",
    ":answer-field/correct": [
      ":answer/id",
      "12031297-fa2b-579c-a021-645548bb7b0c"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1",
        ":answer/id": "d40f7700-dc99-51da-a59b-7681533009e7"
      }
    ],
    ":answer-field/id": "d2350bd6-9fd8-50e3-8494-57b7a39438cd",
    ":answer-field/correct": [
      ":answer/id",
      "d40f7700-dc99-51da-a59b-7681533009e7"
    ]
  }
]
```

Notice that the coefficient of $s$ in the first equation is $-1$, while in the second equation it is $5$.

If we multiply the first equation by $5$, then the $s$-coefficient will become $-5$, which will cancel with the coefficient of $5$ in the second equation.

$$
\left\{\begin{aligned}\bigl(-s + 2t &=-4\bigr)\times\left(5\right) \\ 5s + t &=9\end{aligned}\right.\;\Longrightarrow\;\left\{\begin{aligned}-5s + 10t &=-20 \\ 5s + t &=9\end{aligned}\right.
$$

Now, when we add the two equations, the variable $s$ will be eliminated:

$$
\begin{aligned}
\cancel{-5s} + 10t &= -20 \\
\cancel{5s} + t &= 9 \\
(10t + t) &= (-20 + 9) \\
11t &= -11 \\
t &= -1
\end{aligned}
$$

So, the solution must have $t = -1$. However, we still need to find $s.$ To do this, we substitute $t = -1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
-s + 2t &= -4 \\
-s + 2(-1) &= -4 \\
-s - 2 &= -4 \\
-s &= -2 \\
s &= 2
\end{aligned}
$$

Therefore, the solution to the system of equations is $s=2, \,t=-1$, which can be expressed as $(2,-1)$.

## easy-blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}3s + t &=12 \\ -s + 6t &=15\end{aligned}\right.
$$

Find the solution $(s, t)$ to this system by eliminating the variable $s$.

The solution is $($
{{field-1}}
$,$
{{field-2}}
$)$.

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "3",
        ":answer/id": "ec921896-b24f-5964-9a6d-a4b148fcfd5c"
      }
    ],
    ":answer-field/id": "0bb4e15c-198d-5ab4-8ef0-501ad217407f",
    ":answer-field/correct": [
      ":answer/id",
      "ec921896-b24f-5964-9a6d-a4b148fcfd5c"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "3",
        ":answer/id": "f06f5472-39a2-56a4-b4dc-2f6d663950fd"
      }
    ],
    ":answer-field/id": "85a1ad80-1760-53b7-9552-b5ae1d8e1110",
    ":answer-field/correct": [
      ":answer/id",
      "f06f5472-39a2-56a4-b4dc-2f6d663950fd"
    ]
  }
]
```

Notice that the coefficient of $s$ in the first equation is $3$, while in the second equation it is $-1$.

If we multiply the second equation by $3$, then the $s$-coefficient will become $-3$, which will cancel with the coefficient of $3$ in the first equation.

$$
\left\{\begin{aligned}3s + t &=12 \\ \bigl(-s + 6t &=15\bigr)\times\left(3\right)\end{aligned}\right.\;\Longrightarrow\;\left\{\begin{aligned}3s + t &=12 \\ -3s + 18t &=45\end{aligned}\right.
$$

Now, when we add the two equations, the variable $s$ will be eliminated:

$$
\begin{aligned}
\cancel{3s} + t &= 12 \\
\cancel{-3s} + 18t &= 45 \\
(t + 18t) &= (12 + 45) \\
19t &= 57 \\
t &= 3
\end{aligned}
$$

So, the solution must have $t = 3$. However, we still need to find $s.$ To do this, we substitute $t = 3$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}
-s + 6t &= 15 \\
-s + 6(3) &= 15 \\
-s + 18 &= 15 \\
-s &= -3 \\
s &= 3
\end{aligned}
$$

Therefore, the solution to the system of equations is $s=3, \,t=3$, which can be expressed as $(3,3)$.

## easy-blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}-2a + 7b &=-5 \\ a - 5b &=4\end{aligned}\right.
$$

Find the solution $(a, b)$ to this system by eliminating the variable $a$.

The solution is $($
{{field-1}}
$,$
{{field-2}}
$)$.

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1",
        ":answer/id": "d87297ca-da3d-5bb6-a06b-33523b43ea16"
      }
    ],
    ":answer-field/id": "b550aba8-f8b8-557d-ad43-d6bff2472ac1",
    ":answer-field/correct": [
      ":answer/id",
      "d87297ca-da3d-5bb6-a06b-33523b43ea16"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1",
        ":answer/id": "d8d8a8f6-d1fa-5b2f-897f-890eb3f9dd45"
      }
    ],
    ":answer-field/id": "69b7ecbf-63b5-50c9-85a7-f23389aaff7b",
    ":answer-field/correct": [
      ":answer/id",
      "d8d8a8f6-d1fa-5b2f-897f-890eb3f9dd45"
    ]
  }
]
```

Notice that the coefficient of $a$ in the first equation is $-2$, while in the second equation it is $1$.

If we multiply the second equation by $2$, then the $a$-coefficient will become $2$, which will cancel with the coefficient of $-2$ in the first equation.

$$
\left\{\begin{aligned}-2a + 7b &=-5 \\ \bigl(a - 5b &=4\bigr)\times\left(2\right)\end{aligned}\right.\;\Longrightarrow\;\left\{\begin{aligned}-2a + 7b &=-5 \\ 2a - 10b &=8\end{aligned}\right.
$$

Now, when we add the two equations, the variable $a$ will be eliminated:

$$
\begin{aligned}
\cancel{-2a} + 7b &= -5 \\
\cancel{2a} - 10b &= 8 \\
(7b - 10b) &= (-5 + 8) \\
-3b &= 3 \\
b &= -1
\end{aligned}
$$

So, the solution must have $b = -1$. However, we still need to find $a.$ To do this, we substitute $b = -1$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}
a - 5b &= 4 \\
a - 5(-1) &= 4 \\
a + 5 &= 4 \\
a &= -1
\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-1, \,b=-1$, which can be expressed as $(-1,-1)$.

## easy-blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}3x + 4y &=8 \\ x + 3y &=11\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $x$.

The solution is $($
{{field-1}}
$,$
{{field-2}}
$)$.

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-4",
        ":answer/id": "04be72bd-5431-53d1-bf05-7f93a64beb30"
      }
    ],
    ":answer-field/id": "31f8a0a9-6897-5b58-8c49-5474f64c2975",
    ":answer-field/correct": [
      ":answer/id",
      "04be72bd-5431-53d1-bf05-7f93a64beb30"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "5",
        ":answer/id": "c3e15f7c-1e2c-5946-b255-b90d761713df"
      }
    ],
    ":answer-field/id": "92102c84-871f-5bc3-b420-9d48c234472a",
    ":answer-field/correct": [
      ":answer/id",
      "c3e15f7c-1e2c-5946-b255-b90d761713df"
    ]
  }
]
```

Notice that the coefficient of $x$ in the first equation is $3$, while in the second equation it is $1$.

If we multiply the second equation by $-3$, then the $x$-coefficient will become $-3$, which will cancel with the coefficient of $3$ in the first equation.

$$
\left\{\begin{aligned}3x + 4y &=8 \\ \bigl(x + 3y &=11\bigr)\times\left(-3\right)\end{aligned}\right.\;\Longrightarrow\;\left\{\begin{aligned}3x + 4y &=8 \\ -3x - 9y &=-33\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}
\cancel{3x} + 4y &= 8 \\
\cancel{-3x} - 9y &= -33 \\
(4y - 9y) &= (8 - 33) \\
-5y &= -25 \\
y &= 5
\end{aligned}
$$

So, the solution must have $y = 5$. However, we still need to find $x.$ To do this, we substitute $y = 5$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}
x + 3y &= 11 \\
x + 3(5) &= 11 \\
x + 15 &= 11 \\
x &= -4
\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-4, \,y=5$, which can be expressed as $(-4,5)$.

## easy-moderate_blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}-s+2t &=-4 \\ 5s+t &=9\end{aligned}\right.
$$

The solution $(s,t)$ to this system is $($
{{field-1}}$\,,$
{{field-2}}
$).$

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "2",
        ":answer/id": "0341e29e-69e3-5cf4-b389-356d9ea06593"
      }
    ],
    ":answer-field/id": "8e8a2f32-dd5e-5486-af58-98f2de80020d",
    ":answer-field/correct": [
      ":answer/id",
      "0341e29e-69e3-5cf4-b389-356d9ea06593"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1",
        ":answer/id": "95d34ba0-4049-5f23-a0c7-3aaa0ff16042"
      }
    ],
    ":answer-field/id": "093f8fd3-c302-5c43-9dfd-e8d63856467d",
    ":answer-field/correct": [
      ":answer/id",
      "95d34ba0-4049-5f23-a0c7-3aaa0ff16042"
    ]
  }
]
```

Notice that the coefficient of $s$ in the  first  equation is $-1,$ while in the second equation it is $5.$ 

If we multiply the first equation by $5,$ then the $s$-coefficient will become $-5,$ which will cancel with the coefficient of $5$ in the second equation.

$$
\left\{\begin{aligned}(\,-s+2t &=-4\,)\,\times (5) \\ 5s+t &=9\end{aligned}\right.\,⟹\,\left\{\begin{aligned}-5s+10t &=-20 \\ 5s+t &=9\end{aligned}\right.
$$

Now, when we add the two equations, the variable $s$ will be eliminated:

$$
\begin{aligned}-\cancel{5s}+10t & =-20 \\ \cancel{5s}+t & =9 \\ (10t+t) & =(-20+9) \\ 11t & =-11 \\ t & =-1\end{aligned}
$$

So, the solution must have $t=-1.$ However, we still need to find $s.$ To do this, we substitute $t=-1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}-s+2t & =-4 \\ -s+2(-1) & =-4 \\ -s-2 & =-4 \\ -s & =-2 \\ s & =2\end{aligned}
$$

Therefore, the solution to the system of equations is $s=2,\,t=-1,$ which can be expressed as $(2,-1).$

## easy-moderate_blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}3s+t &=12 \\ -s+6t &=15\end{aligned}\right.
$$

The solution $(s,t)$ to this system is $($
{{field-1}}$\,,$
{{field-2}}
$).$

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "3",
        ":answer/id": "6cd6811b-e232-521c-844c-6c5ea88a9205"
      }
    ],
    ":answer-field/id": "ed014598-7b58-53d5-a22b-3c5de2e06266",
    ":answer-field/correct": [
      ":answer/id",
      "6cd6811b-e232-521c-844c-6c5ea88a9205"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "3",
        ":answer/id": "84853ccc-ed47-5293-85c5-9d6b10a5df95"
      }
    ],
    ":answer-field/id": "69a9b69f-5c64-580f-8e55-551b6da71b32",
    ":answer-field/correct": [
      ":answer/id",
      "84853ccc-ed47-5293-85c5-9d6b10a5df95"
    ]
  }
]
```

Notice that the coefficient of $s$ in the  first  equation is $3,$ while in the second equation it is $-1.$ 

If we multiply the second equation by $3,$ then the $s$-coefficient will become $-3,$ which will cancel with the coefficient of $3$ in the first equation.

$$
\left\{\begin{aligned}3s+t &=12 \\ (\,-s+6t &=15\,)\,\times (3)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}3s+t &=12 \\ -3s+18t &=45\end{aligned}\right.
$$

Now, when we add the two equations, the variable $s$ will be eliminated:

$$
\begin{aligned}\cancel{3s}+t & =12 \\ -\cancel{3s}+18t & =45 \\ (t+18t) & =(12+45) \\ 19t & =57 \\ t & =3\end{aligned}
$$

So, the solution must have $t=3.$ However, we still need to find $s.$ To do this, we substitute $t=3$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}3s+t & =12 \\ 3s+(3) & =12 \\ 3s+3 & =12 \\ 3s & =9 \\ s & =3\end{aligned}
$$

Therefore, the solution to the system of equations is $s=3,\,t=3,$ which can be expressed as $(3,3).$

## easy-moderate_blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}-2a+7b &=-5 \\ a-5b &=4\end{aligned}\right.
$$

The solution $(a,b)$ to this system is $($
{{field-1}}$\,,$
{{field-2}}
$).$

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1",
        ":answer/id": "efa52e6f-7f11-55f3-b4d6-b4ad934eccca"
      }
    ],
    ":answer-field/id": "a5a479d5-2c57-59f9-b77e-b8a2d269e1d0",
    ":answer-field/correct": [
      ":answer/id",
      "efa52e6f-7f11-55f3-b4d6-b4ad934eccca"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1",
        ":answer/id": "9347c939-3808-5f47-8564-b97af935fe28"
      }
    ],
    ":answer-field/id": "7ef588eb-72cb-5592-891d-1600edf31155",
    ":answer-field/correct": [
      ":answer/id",
      "9347c939-3808-5f47-8564-b97af935fe28"
    ]
  }
]
```

Notice that the coefficient of $a$ in the  first  equation is $-2,$ while in the second equation it is $1.$ 

If we multiply the second equation by $2,$ then the $a$-coefficient will become $2,$ which will cancel with the coefficient of $-2$ in the first equation.

$$
\left\{\begin{aligned}-2a+7b &=-5 \\ (\,a-5b &=4\,)\,\times (2)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}-2a+7b &=-5 \\ 2a-10b &=8\end{aligned}\right.
$$

Now, when we add the two equations, the variable $a$ will be eliminated:

$$
\begin{aligned}-\cancel{2a}+7b & =-5 \\ \cancel{2a}-10b & =8 \\ (7b-10b) & =(-5+8) \\ -3b & =3 \\ b & =-1\end{aligned}
$$

So, the solution must have $b=-1.$ However, we still need to find $a.$ To do this, we substitute $b=-1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}-2a+7b & =-5 \\ -2a+7(-1) & =-5 \\ -2a-7 & =-5 \\ -2a & =2 \\ a & =-1\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-1,\,b=-1,$ which can be expressed as $(-1,-1).$

## easy-moderate_blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}3x+4y &=8 \\ x+3y &=11\end{aligned}\right.
$$

The solution $(x,y)$ to this system is $($
{{field-1}}$\,,$
{{field-2}}
$).$

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-4",
        ":answer/id": "49d5f7f8-e20a-5647-a9b9-f52dcd4f8821"
      }
    ],
    ":answer-field/id": "ecccf5d3-1880-5238-8c23-5f79e8133c83",
    ":answer-field/correct": [
      ":answer/id",
      "49d5f7f8-e20a-5647-a9b9-f52dcd4f8821"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "5",
        ":answer/id": "fd884a58-9535-5af0-97ed-9365116e601e"
      }
    ],
    ":answer-field/id": "3eb9f39e-44ce-5520-bbba-25bc9f4a5c81",
    ":answer-field/correct": [
      ":answer/id",
      "fd884a58-9535-5af0-97ed-9365116e601e"
    ]
  }
]
```

Notice that the coefficient of $x$ in the  first  equation is $3,$ while in the second equation it is $1.$ 

If we multiply the second equation by $-3,$ then the $x$-coefficient will become $-3,$ which will cancel with the coefficient of $3$ in the first equation.

$$
\left\{\begin{aligned}3x+4y &=8 \\ (\,x+3y &=11\,)\,\times (-3)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}3x+4y &=8 \\ -3x-9y &=-33\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}\cancel{3x}+4y & =8 \\ -\cancel{3x}-9y & =-33 \\ (4y-9y) & =(8-33) \\ -5y & =-25 \\ y & =5\end{aligned}
$$

So, the solution must have $y=5.$ However, we still need to find $x.$ To do this, we substitute $y=5$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}3x+4y & =8 \\ 3x+4(5) & =8 \\ 3x+20 & =8 \\ 3x & =-12 \\ x & =-4\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-4,\,y=5,$ which can be expressed as $(-4,5).$

## moderate-radio_solution

Find the solution $(x,y)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}-8x-7y &=-13 \\ -2x+3y &=11\end{aligned}\right.
$$

*Hint: Eliminate the variable $x.$*

```json
[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(- \\frac{151}{19}, - \\frac{31}{19})",
        ":answer/id": "b2a456d3-61a6-5a5c-978b-d8346f4a0822"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{127}{8}, \\frac{57}{4})",
        ":answer/id": "59d607c8-8ac6-55ed-893b-984f072a35de"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-10, 3)",
        ":answer/id": "0b5a77b1-2036-5489-93ba-eee8e60e3915"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(- \\frac{203}{38}, \\frac{2}{19})",
        ":answer/id": "8324dadc-3004-5991-800b-af71897ce373"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-1, 3)",
        ":answer/id": "f6244d5d-1312-5f7d-b238-513cf1e3bbae"
      }
    ],
    ":answer-field/id": "1da10994-9fec-577d-987b-d3694b9f8297",
    ":answer-field/correct": [
      ":answer/id",
      "f6244d5d-1312-5f7d-b238-513cf1e3bbae"
    ]
  }
]
```

Notice that the $x$-coefficient in the first equation is $-8,$ while in the second equation it is $-2.$ 

If we multiply the second equation by $-4,$ then the $x$-coefficient will become $8,$ which will cancel with the coefficient of $-8$ in the first equation.

$$
\left\{\begin{aligned}-8x-7y &=-13 \\ (\,-2x+3y &=11\,)\,\times (-4)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}-8x-7y &=-13 \\ 8x-12y &=-44\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}\begin{aligned}-\cancel{8x}-7y & =-13 \\ \cancel{8x}-12y & =-44 \\ (-7y-12y) & =(-13-44) \\ -19y & =-57 \\ y & =3\end{aligned}\end{aligned}
$$

So, the solution must have $y=3.$ However, we still need to find $x.$ To do this, we substitute $y=3$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}\begin{aligned}-8x-7y & =-13 \\ -8x-7(3) & =-13 \\ -8x-21 & =-13 \\ -8x & =8 \\ x & =-1\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-1,\,y=3,$ which can be expressed as $(-1,3).$

## moderate-radio_solution

Find the solution $(x,y)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}-8x-2y &=34 \\ 2x+y &=-7\end{aligned}\right.
$$

*Hint: Eliminate the variable $x.$*

```json
[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(- \\frac{41}{4}, \\frac{27}{2})",
        ":answer/id": "fda16c4e-4b1d-5fde-b83f-bf7505e1f71f"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-5, 3)",
        ":answer/id": "77befadc-804e-5047-a7c0-8424ccefafc3"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-2, 3)",
        ":answer/id": "04824da7-ee6d-563d-b4b0-2b291fbc835d"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-19, 31)",
        ":answer/id": "8dbe28d5-a586-5ad0-953d-ae5a3a15bc13"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(- \\frac{1}{2}, -6)",
        ":answer/id": "5bb88002-b281-5261-9007-20322cc19ffd"
      }
    ],
    ":answer-field/id": "cd6ac5dd-300f-508c-9166-37b9576d924d",
    ":answer-field/correct": [
      ":answer/id",
      "77befadc-804e-5047-a7c0-8424ccefafc3"
    ]
  }
]
```

Notice that the $x$-coefficient in the first equation is $-8,$ while in the second equation it is $2.$ 

If we multiply the second equation by $4,$ then the $x$-coefficient will become $8,$ which will cancel with the coefficient of $-8$ in the first equation.

$$
\left\{\begin{aligned}-8x-2y &=34 \\ (\,2x+y &=-7\,)\,\times (4)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}-8x-2y &=34 \\ 8x+4y &=-28\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}\begin{aligned}-\cancel{8x}-2y & =34 \\ \cancel{8x}+4y & =-28 \\ (-2y+4y) & =(34-28) \\ 2y & =6 \\ y & =3\end{aligned}\end{aligned}
$$

So, the solution must have $y=3.$ However, we still need to find $x.$ To do this, we substitute $y=3$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}\begin{aligned}-8x-2y & =34 \\ -8x-2(3) & =34 \\ -8x-6 & =34 \\ -8x & =40 \\ x & =-5\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-5,\,y=3,$ which can be expressed as $(-5,3).$

## moderate-radio_solution

Find the solution $(a,b)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}2a-b &=-10 \\ 8a+2b &=-16\end{aligned}\right.
$$

*Hint: Eliminate the variable $a.$*

```json
[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(- \\frac{29}{3}, - \\frac{28}{3})",
        ":answer/id": "ad0b84ee-90a2-572d-9450-f8f392fb9057"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(7, 24)",
        ":answer/id": "33e3e946-f3f2-5ce8-b03a-f35fa3bbf5f7"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-3, 4)",
        ":answer/id": "b8a7f579-22b2-5ebe-ab2d-65afa793d8a8"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-7, 4)",
        ":answer/id": "dab8f0d8-7cc6-59d6-bf71-a5b174576155"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(- \\frac{43}{6}, - \\frac{13}{3})",
        ":answer/id": "9dca7652-ef7c-5d8e-be22-3edfc786f49b"
      }
    ],
    ":answer-field/id": "d788ee19-f0d0-5c89-b41c-ae1daea99671",
    ":answer-field/correct": [
      ":answer/id",
      "b8a7f579-22b2-5ebe-ab2d-65afa793d8a8"
    ]
  }
]
```

Notice that the $a$-coefficient in the first equation is $2,$ while in the second equation it is $8.$ 

If we multiply the first equation by $-4,$ then the $a$-coefficient will become $-8,$ which will cancel with the coefficient of $8$ in the second equation.

$$
\left\{\begin{aligned}(\,2a-b &=-10\,)\,\times (-4) \\ 8a+2b &=-16\end{aligned}\right.\,⟹\,\left\{\begin{aligned}-8a+4b &=40 \\ 8a+2b &=-16\end{aligned}\right.
$$

Now, when we add the two equations, the variable $a$ will be eliminated:

$$
\begin{aligned}\begin{aligned}-\cancel{8a}+4b & =40 \\ \cancel{8a}+2b & =-16 \\ (4b+2b) & =(40-16) \\ 6b & =24 \\ b & =4\end{aligned}\end{aligned}
$$

So, the solution must have $b=4.$ However, we still need to find $a.$ To do this, we substitute $b=4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}\begin{aligned}2a-b & =-10 \\ 2a-(4) & =-10 \\ 2a-4 & =-10 \\ 2a & =-6 \\ a & =-3\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-3,\,b=4,$ which can be expressed as $(-3,4).$

## moderate-radio_solution

Find the solution $(a,b)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}2a+3b &=3 \\ -6a-7b &=-11\end{aligned}\right.
$$

*Hint: Eliminate the variable $a.$*

```json
[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(3, -1)",
        ":answer/id": "bfce76c8-20b7-50c8-b3a5-c8d419d746e2"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(0, -1)",
        ":answer/id": "f5aa34d6-f027-5b44-b36b-519a3500158f"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{3}{4}, \\frac{1}{2})",
        ":answer/id": "3e639604-8434-5920-9f6a-04d7292d77bd"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{33}{2}, -10)",
        ":answer/id": "346e860d-11da-5214-aa4d-be5e88972257"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{15}{2}, -4)",
        ":answer/id": "14bb958a-3c82-59a2-bbe4-356c17e9bedd"
      }
    ],
    ":answer-field/id": "36e3b308-0d5e-5d02-a339-dd288516c622",
    ":answer-field/correct": [
      ":answer/id",
      "bfce76c8-20b7-50c8-b3a5-c8d419d746e2"
    ]
  }
]
```

Notice that the $a$-coefficient in the first equation is $2,$ while in the second equation it is $-6.$ 

If we multiply the first equation by $3,$ then the $a$-coefficient will become $6,$ which will cancel with the coefficient of $-6$ in the second equation.

$$
\left\{\begin{aligned}(\,2a+3b &=3\,)\,\times (3) \\ -6a-7b &=-11\end{aligned}\right.\,⟹\,\left\{\begin{aligned}6a+9b &=9 \\ -6a-7b &=-11\end{aligned}\right.
$$

Now, when we add the two equations, the variable $a$ will be eliminated:

$$
\begin{aligned}\begin{aligned}\cancel{6a}+9b & =9 \\ -\cancel{6a}-7b & =-11 \\ (9b-7b) & =(9-11) \\ 2b & =-2 \\ b & =-1\end{aligned}\end{aligned}
$$

So, the solution must have $b=-1.$ However, we still need to find $a.$ To do this, we substitute $b=-1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}\begin{aligned}2a+3b & =3 \\ 2a+3(-1) & =3 \\ 2a-3 & =3 \\ 2a & =6 \\ a & =3\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $a=3,\,b=-1,$ which can be expressed as $(3,-1).$

## moderate-blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}-8x - 7y &=-13 \\ -2x + 3y &=11\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $x$.

The solution is $($
{{field-1}}
$,$
{{field-2}}
$)$.

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1",
        ":answer/id": "52054331-c168-5fe6-b96e-f46b209cba3d"
      }
    ],
    ":answer-field/id": "441ff019-6f61-54da-b34a-b7772104e9cb",
    ":answer-field/correct": [
      ":answer/id",
      "52054331-c168-5fe6-b96e-f46b209cba3d"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "3",
        ":answer/id": "6cabfda2-862c-52ce-a21a-efc7e7740d95"
      }
    ],
    ":answer-field/id": "3a4e2076-794d-5673-bfa3-ce95a75c6eb8",
    ":answer-field/correct": [
      ":answer/id",
      "6cabfda2-862c-52ce-a21a-efc7e7740d95"
    ]
  }
]
```

Notice that the coefficient of $x$ in the first equation is $-8$, while in the second equation it is $-2$.

If we multiply the second equation by $-4$, then the $x$-coefficient will become $8$, which will cancel with the coefficient of $-8$ in the first equation.

$$
\left\{\begin{aligned}-8x - 7y &=-13 \\ \bigl(-2x + 3y &=11\bigr)\times\left(-4\right)\end{aligned}\right.\;\Longrightarrow\;\left\{\begin{aligned}-8x - 7y &=-13 \\ 8x - 12y &=-44\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}
\cancel{-8x} - 7y &= -13 \\
\cancel{8x} - 12y &= -44 \\
(-7y - 12y) &= (-13 - 44) \\
-19y &= -57 \\
y &= 3
\end{aligned}
$$

So, the solution must have $y = 3$. However, we still need to find $x.$ To do this, we substitute $y = 3$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}
-2x + 3y &= 11 \\
-2x + 3(3) &= 11 \\
-2x + 9 &= 11 \\
-2x &= 2 \\
x &= -1
\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-1, \,y=3$, which can be expressed as $(-1,3)$.

## moderate-blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}-8x - 2y &=34 \\ 2x + y &=-7\end{aligned}\right.
$$

Find the solution $(x, y)$ to this system by eliminating the variable $x$.

The solution is $($
{{field-1}}
$,$
{{field-2}}
$)$.

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-5",
        ":answer/id": "615c04f9-eb52-505e-94fe-609bf2b95bac"
      }
    ],
    ":answer-field/id": "a060264b-9bc5-559a-9a8f-a234016329af",
    ":answer-field/correct": [
      ":answer/id",
      "615c04f9-eb52-505e-94fe-609bf2b95bac"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "3",
        ":answer/id": "ece7b485-d6cc-5364-896e-1987bc46fa30"
      }
    ],
    ":answer-field/id": "60d67160-ed35-56a2-835e-3a9b2d878f11",
    ":answer-field/correct": [
      ":answer/id",
      "ece7b485-d6cc-5364-896e-1987bc46fa30"
    ]
  }
]
```

Notice that the coefficient of $x$ in the first equation is $-8$, while in the second equation it is $2$.

If we multiply the second equation by $4$, then the $x$-coefficient will become $8$, which will cancel with the coefficient of $-8$ in the first equation.

$$
\left\{\begin{aligned}-8x - 2y &=34 \\ \bigl(2x + y &=-7\bigr)\times\left(4\right)\end{aligned}\right.\;\Longrightarrow\;\left\{\begin{aligned}-8x - 2y &=34 \\ 8x + 4y &=-28\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}
\cancel{-8x} - 2y &= 34 \\
\cancel{8x} + 4y &= -28 \\
(-2y + 4y) &= (34 - 28) \\
2y &= 6 \\
y &= 3
\end{aligned}
$$

So, the solution must have $y = 3$. However, we still need to find $x.$ To do this, we substitute $y = 3$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}
2x + y &= -7 \\
2x + (3) &= -7 \\
2x + 3 &= -7 \\
2x &= -10 \\
x &= -5
\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-5, \,y=3$, which can be expressed as $(-5,3)$.

## moderate-blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}2a - b &=-10 \\ 8a + 2b &=-16\end{aligned}\right.
$$

Find the solution $(a, b)$ to this system by eliminating the variable $a$.

The solution is $($
{{field-1}}
$,$
{{field-2}}
$)$.

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-3",
        ":answer/id": "39e7172c-dc94-5ba1-a78a-fdbbe6361c5d"
      }
    ],
    ":answer-field/id": "9435b7cb-0d81-5461-9576-92d328b2b3e7",
    ":answer-field/correct": [
      ":answer/id",
      "39e7172c-dc94-5ba1-a78a-fdbbe6361c5d"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "4",
        ":answer/id": "5548b584-a3ba-5dea-afe4-a04fb91fe4e7"
      }
    ],
    ":answer-field/id": "aea28908-01c1-582a-bc29-5e06d0c99310",
    ":answer-field/correct": [
      ":answer/id",
      "5548b584-a3ba-5dea-afe4-a04fb91fe4e7"
    ]
  }
]
```

Notice that the coefficient of $a$ in the first equation is $2$, while in the second equation it is $8$.

If we multiply the first equation by $-4$, then the $a$-coefficient will become $-8$, which will cancel with the coefficient of $8$ in the second equation.

$$
\left\{\begin{aligned}\bigl(2a - b &=-10\bigr)\times\left(-4\right) \\ 8a + 2b &=-16\end{aligned}\right.\;\Longrightarrow\;\left\{\begin{aligned}-8a + 4b &=40 \\ 8a + 2b &=-16\end{aligned}\right.
$$

Now, when we add the two equations, the variable $a$ will be eliminated:

$$
\begin{aligned}
\cancel{-8a} + 4b &= 40 \\
\cancel{8a} + 2b &= -16 \\
(4b + 2b) &= (40 - 16) \\
6b &= 24 \\
b &= 4
\end{aligned}
$$

So, the solution must have $b = 4$. However, we still need to find $a.$ To do this, we substitute $b = 4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
2a - b &= -10 \\
2a - (4) &= -10 \\
2a - 4 &= -10 \\
2a &= -6 \\
a &= -3
\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-3, \,b=4$, which can be expressed as $(-3,4)$.

## moderate-blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}2a + 3b &=3 \\ -6a - 7b &=-11\end{aligned}\right.
$$

Find the solution $(a, b)$ to this system by eliminating the variable $a$.

The solution is $($
{{field-1}}
$,$
{{field-2}}
$)$.

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "3",
        ":answer/id": "3ab20386-ab05-57c9-b658-cbf412303cea"
      }
    ],
    ":answer-field/id": "29b9e9d2-d8b9-567a-bf3f-9975005c4da9",
    ":answer-field/correct": [
      ":answer/id",
      "3ab20386-ab05-57c9-b658-cbf412303cea"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1",
        ":answer/id": "c18b8bfd-d535-5f64-9dc3-29443f7b0111"
      }
    ],
    ":answer-field/id": "a13a4978-2cfb-5005-a848-fea98ceb20d5",
    ":answer-field/correct": [
      ":answer/id",
      "c18b8bfd-d535-5f64-9dc3-29443f7b0111"
    ]
  }
]
```

Notice that the coefficient of $a$ in the first equation is $2$, while in the second equation it is $-6$.

If we multiply the first equation by $3$, then the $a$-coefficient will become $6$, which will cancel with the coefficient of $-6$ in the second equation.

$$
\left\{\begin{aligned}\bigl(2a + 3b &=3\bigr)\times\left(3\right) \\ -6a - 7b &=-11\end{aligned}\right.\;\Longrightarrow\;\left\{\begin{aligned}6a + 9b &=9 \\ -6a - 7b &=-11\end{aligned}\right.
$$

Now, when we add the two equations, the variable $a$ will be eliminated:

$$
\begin{aligned}
\cancel{6a} + 9b &= 9 \\
\cancel{-6a} - 7b &= -11 \\
(9b - 7b) &= (9 - 11) \\
2b &= -2 \\
b &= -1
\end{aligned}
$$

So, the solution must have $b = -1$. However, we still need to find $a.$ To do this, we substitute $b = -1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
2a + 3b &= 3 \\
2a + 3(-1) &= 3 \\
2a - 3 &= 3 \\
2a &= 6 \\
a &= 3
\end{aligned}
$$

Therefore, the solution to the system of equations is $a=3, \,b=-1$, which can be expressed as $(3,-1)$.

## moderate-moderate_blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}-8x-7y &=-13 \\ -2x+3y &=11\end{aligned}\right.
$$

The solution $(x,y)$ to this system is $($
{{field-1}}$\,,$
{{field-2}}
$).$

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1",
        ":answer/id": "6f9cf277-d253-5291-8bc9-166ca05ae3d5"
      }
    ],
    ":answer-field/id": "eec27de0-c8f5-5336-a646-9269d800d3c1",
    ":answer-field/correct": [
      ":answer/id",
      "6f9cf277-d253-5291-8bc9-166ca05ae3d5"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "3",
        ":answer/id": "4718fc67-4277-5da6-92af-ffa04020ff53"
      }
    ],
    ":answer-field/id": "f49989ef-8453-5dcb-a8d0-9505860de49b",
    ":answer-field/correct": [
      ":answer/id",
      "4718fc67-4277-5da6-92af-ffa04020ff53"
    ]
  }
]
```

Notice that the coefficient of $x$ in the  first  equation is $-8,$ while in the second equation it is $-2.$ 

If we multiply the second equation by $-4,$ then the $x$-coefficient will become $8,$ which will cancel with the coefficient of $-8$ in the first equation.

$$
\left\{\begin{aligned}-8x-7y &=-13 \\ (\,-2x+3y &=11\,)\,\times (-4)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}-8x-7y &=-13 \\ 8x-12y &=-44\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}-\cancel{8x}-7y & =-13 \\ \cancel{8x}-12y & =-44 \\ (-7y-12y) & =(-13-44) \\ -19y & =-57 \\ y & =3\end{aligned}
$$

So, the solution must have $y=3.$ However, we still need to find $x.$ To do this, we substitute $y=3$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}-8x-7y & =-13 \\ -8x-7(3) & =-13 \\ -8x-21 & =-13 \\ -8x & =8 \\ x & =-1\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-1,\,y=3,$ which can be expressed as $(-1,3).$

## moderate-moderate_blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}-8x-2y &=34 \\ 2x+y &=-7\end{aligned}\right.
$$

The solution $(x,y)$ to this system is $($
{{field-1}}$\,,$
{{field-2}}
$).$

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-5",
        ":answer/id": "2f2bc314-ee40-53e3-97dc-b99aa833f664"
      }
    ],
    ":answer-field/id": "e0b9c629-2fdf-53d9-9f02-30c8e4e1ca3f",
    ":answer-field/correct": [
      ":answer/id",
      "2f2bc314-ee40-53e3-97dc-b99aa833f664"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "3",
        ":answer/id": "9ff6ad4b-9a75-5977-95f1-57484fba822d"
      }
    ],
    ":answer-field/id": "b76914aa-aa22-5ad3-821d-6535023a49cd",
    ":answer-field/correct": [
      ":answer/id",
      "9ff6ad4b-9a75-5977-95f1-57484fba822d"
    ]
  }
]
```

Notice that the coefficient of $x$ in the  first  equation is $-8,$ while in the second equation it is $2.$ 

If we multiply the second equation by $4,$ then the $x$-coefficient will become $8,$ which will cancel with the coefficient of $-8$ in the first equation.

$$
\left\{\begin{aligned}-8x-2y &=34 \\ (\,2x+y &=-7\,)\,\times (4)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}-8x-2y &=34 \\ 8x+4y &=-28\end{aligned}\right.
$$

Now, when we add the two equations, the variable $x$ will be eliminated:

$$
\begin{aligned}-\cancel{8x}-2y & =34 \\ \cancel{8x}+4y & =-28 \\ (-2y+4y) & =(34-28) \\ 2y & =6 \\ y & =3\end{aligned}
$$

So, the solution must have $y=3.$ However, we still need to find $x.$ To do this, we substitute $y=3$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}-8x-2y & =34 \\ -8x-2(3) & =34 \\ -8x-6 & =34 \\ -8x & =40 \\ x & =-5\end{aligned}
$$

Therefore, the solution to the system of equations is $x=-5,\,y=3,$ which can be expressed as $(-5,3).$

## moderate-moderate_blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}2a-b &=-10 \\ 8a+2b &=-16\end{aligned}\right.
$$

The solution $(a,b)$ to this system is $($
{{field-1}}$\,,$
{{field-2}}
$).$

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-3",
        ":answer/id": "c5aea3fa-e538-5c53-8639-60f35b6c96e1"
      }
    ],
    ":answer-field/id": "ac734739-16e8-5d60-b0f6-e0cf723f211e",
    ":answer-field/correct": [
      ":answer/id",
      "c5aea3fa-e538-5c53-8639-60f35b6c96e1"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "4",
        ":answer/id": "9ab5531b-42fb-5184-b875-d120bfd5a6dc"
      }
    ],
    ":answer-field/id": "4ccf04f4-0a2e-5a2f-b8e4-fcdb5b106840",
    ":answer-field/correct": [
      ":answer/id",
      "9ab5531b-42fb-5184-b875-d120bfd5a6dc"
    ]
  }
]
```

Notice that the coefficient of $a$ in the  first  equation is $2,$ while in the second equation it is $8.$ 

If we multiply the first equation by $-4,$ then the $a$-coefficient will become $-8,$ which will cancel with the coefficient of $8$ in the second equation.

$$
\left\{\begin{aligned}(\,2a-b &=-10\,)\,\times (-4) \\ 8a+2b &=-16\end{aligned}\right.\,⟹\,\left\{\begin{aligned}-8a+4b &=40 \\ 8a+2b &=-16\end{aligned}\right.
$$

Now, when we add the two equations, the variable $a$ will be eliminated:

$$
\begin{aligned}-\cancel{8a}+4b & =40 \\ \cancel{8a}+2b & =-16 \\ (4b+2b) & =(40-16) \\ 6b & =24 \\ b & =4\end{aligned}
$$

So, the solution must have $b=4.$ However, we still need to find $a.$ To do this, we substitute $b=4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}2a-b & =-10 \\ 2a-(4) & =-10 \\ 2a-4 & =-10 \\ 2a & =-6 \\ a & =-3\end{aligned}
$$

Therefore, the solution to the system of equations is $a=-3,\,b=4,$ which can be expressed as $(-3,4).$

## moderate-moderate_blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}2a+3b &=3 \\ -6a-7b &=-11\end{aligned}\right.
$$

The solution $(a,b)$ to this system is $($
{{field-1}}$\,,$
{{field-2}}
$).$

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "3",
        ":answer/id": "440b2f6d-788e-5283-afde-ae3c7ce63203"
      }
    ],
    ":answer-field/id": "fed1fb2c-cf17-50a5-95fb-018083912417",
    ":answer-field/correct": [
      ":answer/id",
      "440b2f6d-788e-5283-afde-ae3c7ce63203"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1",
        ":answer/id": "eb3d6679-d9c2-5e91-8994-3b2a47475938"
      }
    ],
    ":answer-field/id": "c01c27fc-175f-5054-8842-bb5ecba52554",
    ":answer-field/correct": [
      ":answer/id",
      "eb3d6679-d9c2-5e91-8994-3b2a47475938"
    ]
  }
]
```

Notice that the coefficient of $a$ in the  first  equation is $2,$ while in the second equation it is $-6.$ 

If we multiply the first equation by $3,$ then the $a$-coefficient will become $6,$ which will cancel with the coefficient of $-6$ in the second equation.

$$
\left\{\begin{aligned}(\,2a+3b &=3\,)\,\times (3) \\ -6a-7b &=-11\end{aligned}\right.\,⟹\,\left\{\begin{aligned}6a+9b &=9 \\ -6a-7b &=-11\end{aligned}\right.
$$

Now, when we add the two equations, the variable $a$ will be eliminated:

$$
\begin{aligned}\cancel{6a}+9b & =9 \\ -\cancel{6a}-7b & =-11 \\ (9b-7b) & =(9-11) \\ 2b & =-2 \\ b & =-1\end{aligned}
$$

So, the solution must have $b=-1.$ However, we still need to find $a.$ To do this, we substitute $b=-1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}2a+3b & =3 \\ 2a+3(-1) & =3 \\ 2a-3 & =3 \\ 2a & =6 \\ a & =3\end{aligned}
$$

Therefore, the solution to the system of equations is $a=3,\,b=-1,$ which can be expressed as $(3,-1).$

## hard-radio_solution

Find the solution $(u,v)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}2u-7v &=34 \\ -10u-3v &=-18\end{aligned}\right.
$$

*Hint: Eliminate the variable $u.$*

```json
[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(31, -4)",
        ":answer/id": "828cd120-b319-56b2-b824-659f46b155cd"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{652}{19}, \\frac{94}{19})",
        ":answer/id": "fc92f2f4-a871-5f8b-841a-15fd0b8a7212"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(3, -4)",
        ":answer/id": "2fe2ef7e-7c82-5a3a-a550-da2199c302ea"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(- \\frac{181}{5}, - \\frac{76}{5})",
        ":answer/id": "af020339-0c79-5e6c-ba74-947a3a899c56"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{295}{19}, - \\frac{8}{19})",
        ":answer/id": "7b164591-f1d2-501a-8c7b-64a62f92210d"
      }
    ],
    ":answer-field/id": "b38b5620-49ed-5b10-9247-5f6e497a64e2",
    ":answer-field/correct": [
      ":answer/id",
      "2fe2ef7e-7c82-5a3a-a550-da2199c302ea"
    ]
  }
]
```

Notice that the $u$-coefficient in the first equation is $2,$ while in the second equation it is $-10.$ 

If we multiply the first equation by $5,$ then the $u$-coefficient will become $10,$ which will cancel with the coefficient of $-10$ in the second equation.

$$
\left\{\begin{aligned}(\,2u-7v &=34\,)\,\times (5) \\ -10u-3v &=-18\end{aligned}\right.\,⟹\,\left\{\begin{aligned}10u-35v &=170 \\ -10u-3v &=-18\end{aligned}\right.
$$

Now, when we add the two equations, the variable $u$ will be eliminated:

$$
\begin{aligned}\begin{aligned}\cancel{10u}-35v & =170 \\ -\cancel{10u}-3v & =-18 \\ (-35v-3v) & =(170-18) \\ -38v & =152 \\ v & =-4\end{aligned}\end{aligned}
$$

So, the solution must have $v=-4.$ However, we still need to find $u.$ To do this, we substitute $v=-4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}\begin{aligned}2u-7v & =34 \\ 2u-7(-4) & =34 \\ 2u+28 & =34 \\ 2u & =6 \\ u & =3\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $u=3,\,v=-4,$ which can be expressed as $(3,-4).$

## hard-radio_solution

Find the solution $(u,v)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}-14u+v &=12 \\ -2u-7v &=16\end{aligned}\right.
$$

*Hint: Eliminate the variable $u.$*

```json
[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-15, -2)",
        ":answer/id": "630ca7a5-18c8-52f7-a4f0-2f640810277e"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(- \\frac{199}{3}, \\frac{50}{3})",
        ":answer/id": "c2bec2c9-ab07-5008-bd6a-3b226114f0a6"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(- \\frac{417}{25}, \\frac{62}{25})",
        ":answer/id": "194e8a90-fa68-5e1d-ac01-418c6bfe0504"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(- \\frac{249}{25}, \\frac{14}{25})",
        ":answer/id": "b2ef68f4-77c6-5724-b4be-cfdac775bfcf"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-1, -2)",
        ":answer/id": "6c98ad27-4350-542b-8aaf-5df0125c292b"
      }
    ],
    ":answer-field/id": "e2953c63-fc8f-5cd9-89bc-c32319f5b3e5",
    ":answer-field/correct": [
      ":answer/id",
      "6c98ad27-4350-542b-8aaf-5df0125c292b"
    ]
  }
]
```

Notice that the $u$-coefficient in the first equation is $-14,$ while in the second equation it is $-2.$ 

If we multiply the second equation by $-7,$ then the $u$-coefficient will become $14,$ which will cancel with the coefficient of $-14$ in the first equation.

$$
\left\{\begin{aligned}-14u+v &=12 \\ (\,-2u-7v &=16\,)\,\times (-7)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}-14u+v &=12 \\ 14u+49v &=-112\end{aligned}\right.
$$

Now, when we add the two equations, the variable $u$ will be eliminated:

$$
\begin{aligned}\begin{aligned}-\cancel{14u}+v & =12 \\ \cancel{14u}+49v & =-112 \\ (v+49v) & =(12-112) \\ 50v & =-100 \\ v & =-2\end{aligned}\end{aligned}
$$

So, the solution must have $v=-2.$ However, we still need to find $u.$ To do this, we substitute $v=-2$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}\begin{aligned}-14u+v & =12 \\ -14u+(-2) & =12 \\ -14u-2 & =12 \\ -14u & =14 \\ u & =-1\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $u=-1,\,v=-2,$ which can be expressed as $(-1,-2).$

## hard-radio_solution

Find the solution $(u,v)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}3u-5v &=8 \\ 15u+7v &=8\end{aligned}\right.
$$

*Hint: Eliminate the variable $u.$*

```json
[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{7}{2}, \\frac{1}{2})",
        ":answer/id": "741b61e5-f76d-5538-93ad-19b60cc66336"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(1, -1)",
        ":answer/id": "5b17df3e-3c4f-5e7c-adcc-b6d75414e036"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(-24, -16)",
        ":answer/id": "6e751183-6730-5e9b-ae3a-3e5ca6a281f3"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{31}{6}, \\frac{3}{2})",
        ":answer/id": "cb3992a1-c0bf-5995-aa8d-0492667eddde"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{13}{3}, -1)",
        ":answer/id": "c9a64feb-c9e8-510f-84e5-5de92c77be8c"
      }
    ],
    ":answer-field/id": "6e35176c-1967-5044-8953-d6efbe3347b3",
    ":answer-field/correct": [
      ":answer/id",
      "5b17df3e-3c4f-5e7c-adcc-b6d75414e036"
    ]
  }
]
```

Notice that the $u$-coefficient in the first equation is $3,$ while in the second equation it is $15.$ 

If we multiply the first equation by $-5,$ then the $u$-coefficient will become $-15,$ which will cancel with the coefficient of $15$ in the second equation.

$$
\left\{\begin{aligned}(\,3u-5v &=8\,)\,\times (-5) \\ 15u+7v &=8\end{aligned}\right.\,⟹\,\left\{\begin{aligned}-15u+25v &=-40 \\ 15u+7v &=8\end{aligned}\right.
$$

Now, when we add the two equations, the variable $u$ will be eliminated:

$$
\begin{aligned}\begin{aligned}-\cancel{15u}+25v & =-40 \\ \cancel{15u}+7v & =8 \\ (25v+7v) & =(-40+8) \\ 32v & =-32 \\ v & =-1\end{aligned}\end{aligned}
$$

So, the solution must have $v=-1.$ However, we still need to find $u.$ To do this, we substitute $v=-1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}\begin{aligned}3u-5v & =8 \\ 3u-5(-1) & =8 \\ 3u+5 & =8 \\ 3u & =3 \\ u & =1\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $u=1,\,v=-1,$ which can be expressed as $(1,-1).$

## hard-radio_solution

Find the solution $(u,v)$ to the following system of equations using the elimination method:

$$
\left\{\begin{aligned}2u+5v &=7 \\ -12u-7v &=-19\end{aligned}\right.
$$

*Hint: Eliminate the variable $u.$*

```json
[
  {
    ":answer-field/key": "selection",
    ":answer-field/type": ":answer-field.type/radio",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(1, 1)",
        ":answer/id": "918117f9-06ae-54ac-b0ca-bb34d99659b0"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{129}{4}, - \\frac{23}{2})",
        ":answer/id": "3aaf74de-bf1f-5df4-87b6-5c1de6901fc9"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(6, 1)",
        ":answer/id": "dfda67b7-a1fe-5176-a3e1-52dbfbfa97f6"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{233}{23}, - \\frac{61}{23})",
        ":answer/id": "de54d075-1c93-5bc8-84cb-280b8642db4f"
      },
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "(\\frac{221}{46}, - \\frac{12}{23})",
        ":answer/id": "41144b91-3215-5a05-9946-f7bacaed00d2"
      }
    ],
    ":answer-field/id": "726e34ef-bbc2-5921-b3da-ed738d155848",
    ":answer-field/correct": [
      ":answer/id",
      "918117f9-06ae-54ac-b0ca-bb34d99659b0"
    ]
  }
]
```

Notice that the $u$-coefficient in the first equation is $2,$ while in the second equation it is $-12.$ 

If we multiply the first equation by $6,$ then the $u$-coefficient will become $12,$ which will cancel with the coefficient of $-12$ in the second equation.

$$
\left\{\begin{aligned}(\,2u+5v &=7\,)\,\times (6) \\ -12u-7v &=-19\end{aligned}\right.\,⟹\,\left\{\begin{aligned}12u+30v &=42 \\ -12u-7v &=-19\end{aligned}\right.
$$

Now, when we add the two equations, the variable $u$ will be eliminated:

$$
\begin{aligned}\begin{aligned}\cancel{12u}+30v & =42 \\ -\cancel{12u}-7v & =-19 \\ (30v-7v) & =(42-19) \\ 23v & =23 \\ v & =1\end{aligned}\end{aligned}
$$

So, the solution must have $v=1.$ However, we still need to find $u.$ To do this, we substitute $v=1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}\begin{aligned}2u+5v & =7 \\ 2u+5(1) & =7 \\ 2u+5 & =7 \\ 2u & =2 \\ u & =1\end{aligned}\end{aligned}
$$

Therefore, the solution to the system of equations is $u=1,\,v=1,$ which can be expressed as $(1,1).$

## hard-blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}21a - 4b &=37 \\ 3a + 5b &=-17\end{aligned}\right.
$$

Find the solution $(a, b)$ to this system by eliminating the variable $a$.

The solution is $($
{{field-1}}
$,$
{{field-2}}
$)$.

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "1",
        ":answer/id": "c39470a1-b2d6-51f8-a8c6-6ff391ea2ed4"
      }
    ],
    ":answer-field/id": "53e0f6d2-9fbb-5bfc-9234-d04030c48020",
    ":answer-field/correct": [
      ":answer/id",
      "c39470a1-b2d6-51f8-a8c6-6ff391ea2ed4"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-4",
        ":answer/id": "cc13afb8-895d-5723-a4f1-5134f31a0dde"
      }
    ],
    ":answer-field/id": "03f86b55-fe65-5a7a-a9ad-6c1eaacee476",
    ":answer-field/correct": [
      ":answer/id",
      "cc13afb8-895d-5723-a4f1-5134f31a0dde"
    ]
  }
]
```

Notice that the coefficient of $a$ in the first equation is $21$, while in the second equation it is $3$.

If we multiply the second equation by $-7$, then the $a$-coefficient will become $-21$, which will cancel with the coefficient of $21$ in the first equation.

$$
\left\{\begin{aligned}21a - 4b &=37 \\ \bigl(3a + 5b &=-17\bigr)\times\left(-7\right)\end{aligned}\right.\;\Longrightarrow\;\left\{\begin{aligned}21a - 4b &=37 \\ -21a - 35b &=119\end{aligned}\right.
$$

Now, when we add the two equations, the variable $a$ will be eliminated:

$$
\begin{aligned}
\cancel{21a} - 4b &= 37 \\
\cancel{-21a} - 35b &= 119 \\
(-4b - 35b) &= (37 + 119) \\
-39b &= 156 \\
b &= -4
\end{aligned}
$$

So, the solution must have $b = -4$. However, we still need to find $a.$ To do this, we substitute $b = -4$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}
3a + 5b &= -17 \\
3a + 5(-4) &= -17 \\
3a - 20 &= -17 \\
3a &= 3 \\
a &= 1
\end{aligned}
$$

Therefore, the solution to the system of equations is $a=1, \,b=-4$, which can be expressed as $(1,-4)$.

## hard-blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}-14u + v &=12 \\ -2u - 7v &=16\end{aligned}\right.
$$

Find the solution $(u, v)$ to this system by eliminating the variable $u$.

The solution is $($
{{field-1}}
$,$
{{field-2}}
$)$.

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1",
        ":answer/id": "e08d3b81-cc79-526c-9864-6244cdaa82d4"
      }
    ],
    ":answer-field/id": "906363b3-4f1d-56dc-bc0a-1c4672be7a1e",
    ":answer-field/correct": [
      ":answer/id",
      "e08d3b81-cc79-526c-9864-6244cdaa82d4"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-2",
        ":answer/id": "ee5d5002-6366-5f99-8e5b-53cb004f6f7a"
      }
    ],
    ":answer-field/id": "de33ed8b-d0cd-5c06-bc4c-9e4dcec4b64e",
    ":answer-field/correct": [
      ":answer/id",
      "ee5d5002-6366-5f99-8e5b-53cb004f6f7a"
    ]
  }
]
```

Notice that the coefficient of $u$ in the first equation is $-14$, while in the second equation it is $-2$.

If we multiply the second equation by $-7$, then the $u$-coefficient will become $14$, which will cancel with the coefficient of $-14$ in the first equation.

$$
\left\{\begin{aligned}-14u + v &=12 \\ \bigl(-2u - 7v &=16\bigr)\times\left(-7\right)\end{aligned}\right.\;\Longrightarrow\;\left\{\begin{aligned}-14u + v &=12 \\ 14u + 49v &=-112\end{aligned}\right.
$$

Now, when we add the two equations, the variable $u$ will be eliminated:

$$
\begin{aligned}
\cancel{-14u} + v &= 12 \\
\cancel{14u} + 49v &= -112 \\
(v + 49v) &= (12 - 112) \\
50v &= -100 \\
v &= -2
\end{aligned}
$$

So, the solution must have $v = -2$. However, we still need to find $u.$ To do this, we substitute $v = -2$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}
-2u - 7v &= 16 \\
-2u - 7(-2) &= 16 \\
-2u + 14 &= 16 \\
-2u &= 2 \\
u &= -1
\end{aligned}
$$

Therefore, the solution to the system of equations is $u=-1, \,v=-2$, which can be expressed as $(-1,-2)$.

## hard-blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}15a - 2b &=22 \\ 3a - b &=2\end{aligned}\right.
$$

Find the solution $(a, b)$ to this system by eliminating the variable $a$.

The solution is $($
{{field-1}}
$,$
{{field-2}}
$)$.

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "2",
        ":answer/id": "18749c5f-f53b-5d87-a982-22581acf87cc"
      }
    ],
    ":answer-field/id": "92bf03f9-46a9-5468-8940-2deb4959240b",
    ":answer-field/correct": [
      ":answer/id",
      "18749c5f-f53b-5d87-a982-22581acf87cc"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "4",
        ":answer/id": "cb3579f3-4c52-5a89-8c66-ed7687c9d48c"
      }
    ],
    ":answer-field/id": "1a6af1ed-dd6f-54c0-ac8a-6ad408919ec2",
    ":answer-field/correct": [
      ":answer/id",
      "cb3579f3-4c52-5a89-8c66-ed7687c9d48c"
    ]
  }
]
```

Notice that the coefficient of $a$ in the first equation is $15$, while in the second equation it is $3$.

If we multiply the second equation by $-5$, then the $a$-coefficient will become $-15$, which will cancel with the coefficient of $15$ in the first equation.

$$
\left\{\begin{aligned}15a - 2b &=22 \\ \bigl(3a - b &=2\bigr)\times\left(-5\right)\end{aligned}\right.\;\Longrightarrow\;\left\{\begin{aligned}15a - 2b &=22 \\ -15a + 5b &=-10\end{aligned}\right.
$$

Now, when we add the two equations, the variable $a$ will be eliminated:

$$
\begin{aligned}
\cancel{15a} - 2b &= 22 \\
\cancel{-15a} + 5b &= -10 \\
(-2b + 5b) &= (22 - 10) \\
3b &= 12 \\
b &= 4
\end{aligned}
$$

So, the solution must have $b = 4$. However, we still need to find $a.$ To do this, we substitute $b = 4$ back into one of the equations. Let's choose the second equation:

$$
\begin{aligned}
3a - b &= 2 \\
3a - (4) &= 2 \\
3a - 4 &= 2 \\
3a &= 6 \\
a &= 2
\end{aligned}
$$

Therefore, the solution to the system of equations is $a=2, \,b=4$, which can be expressed as $(2,4)$.

## hard-blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}2u + 5v &=7 \\ -12u - 7v &=-19\end{aligned}\right.
$$

Find the solution $(u, v)$ to this system by eliminating the variable $u$.

The solution is $($
{{field-1}}
$,$
{{field-2}}
$)$.

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "1",
        ":answer/id": "e9b41cdf-77d9-5744-a379-faad5a81f700"
      }
    ],
    ":answer-field/id": "b3aa3a98-bd11-5c18-a934-fdd6e238f359",
    ":answer-field/correct": [
      ":answer/id",
      "e9b41cdf-77d9-5744-a379-faad5a81f700"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "1",
        ":answer/id": "59f719a7-9577-5485-8df0-8e85a0bc4f3a"
      }
    ],
    ":answer-field/id": "5c281d41-36ea-5864-a7ea-a962582bb6d0",
    ":answer-field/correct": [
      ":answer/id",
      "59f719a7-9577-5485-8df0-8e85a0bc4f3a"
    ]
  }
]
```

Notice that the coefficient of $u$ in the first equation is $2$, while in the second equation it is $-12$.

If we multiply the first equation by $6$, then the $u$-coefficient will become $12$, which will cancel with the coefficient of $-12$ in the second equation.

$$
\left\{\begin{aligned}\bigl(2u + 5v &=7\bigr)\times\left(6\right) \\ -12u - 7v &=-19\end{aligned}\right.\;\Longrightarrow\;\left\{\begin{aligned}12u + 30v &=42 \\ -12u - 7v &=-19\end{aligned}\right.
$$

Now, when we add the two equations, the variable $u$ will be eliminated:

$$
\begin{aligned}
\cancel{12u} + 30v &= 42 \\
\cancel{-12u} - 7v &= -19 \\
(30v - 7v) &= (42 - 19) \\
23v &= 23 \\
v &= 1
\end{aligned}
$$

So, the solution must have $v = 1$. However, we still need to find $u.$ To do this, we substitute $v = 1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}
2u + 5v &= 7 \\
2u + 5(1) &= 7 \\
2u + 5 &= 7 \\
2u &= 2 \\
u &= 1
\end{aligned}
$$

Therefore, the solution to the system of equations is $u=1, \,v=1$, which can be expressed as $(1,1)$.

## hard-moderate_blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}21a-4b &=37 \\ 3a+5b &=-17\end{aligned}\right.
$$

The solution $(a,b)$ to this system is $($
{{field-1}}$\,,$
{{field-2}}
$).$

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "1",
        ":answer/id": "5e9574e3-be8c-574d-81b7-41a056c95d25"
      }
    ],
    ":answer-field/id": "43ce7f93-cc52-5298-9362-1884fbad9710",
    ":answer-field/correct": [
      ":answer/id",
      "5e9574e3-be8c-574d-81b7-41a056c95d25"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-4",
        ":answer/id": "728d4eb1-6e03-57a5-bff7-58b78e6e6156"
      }
    ],
    ":answer-field/id": "ee5f41c9-00e3-5c52-b957-29e2d228839b",
    ":answer-field/correct": [
      ":answer/id",
      "728d4eb1-6e03-57a5-bff7-58b78e6e6156"
    ]
  }
]
```

Notice that the coefficient of $a$ in the  first  equation is $21,$ while in the second equation it is $3.$ 

If we multiply the second equation by $-7,$ then the $a$-coefficient will become $-21,$ which will cancel with the coefficient of $21$ in the first equation.

$$
\left\{\begin{aligned}21a-4b &=37 \\ (\,3a+5b &=-17\,)\,\times (-7)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}21a-4b &=37 \\ -21a-35b &=119\end{aligned}\right.
$$

Now, when we add the two equations, the variable $a$ will be eliminated:

$$
\begin{aligned}\cancel{21a}-4b & =37 \\ -\cancel{21a}-35b & =119 \\ (-4b-35b) & =(37+119) \\ -39b & =156 \\ b & =-4\end{aligned}
$$

So, the solution must have $b=-4.$ However, we still need to find $a.$ To do this, we substitute $b=-4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}21a-4b & =37 \\ 21a-4(-4) & =37 \\ 21a+16 & =37 \\ 21a & =21 \\ a & =1\end{aligned}
$$

Therefore, the solution to the system of equations is $a=1,\,b=-4,$ which can be expressed as $(1,-4).$

## hard-moderate_blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}-14u+v &=12 \\ -2u-7v &=16\end{aligned}\right.
$$

The solution $(u,v)$ to this system is $($
{{field-1}}$\,,$
{{field-2}}
$).$

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-1",
        ":answer/id": "fe201aba-beb0-5f50-b1d5-8f9f75c5e65a"
      }
    ],
    ":answer-field/id": "678d7dd5-f53e-5bad-a1a7-4908413555c0",
    ":answer-field/correct": [
      ":answer/id",
      "fe201aba-beb0-5f50-b1d5-8f9f75c5e65a"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "-2",
        ":answer/id": "bde62e8d-fe32-5136-99bd-4dc4961646ab"
      }
    ],
    ":answer-field/id": "c8447b88-0ca1-51a6-9992-e626668c71ec",
    ":answer-field/correct": [
      ":answer/id",
      "bde62e8d-fe32-5136-99bd-4dc4961646ab"
    ]
  }
]
```

Notice that the coefficient of $u$ in the  first  equation is $-14,$ while in the second equation it is $-2.$ 

If we multiply the second equation by $-7,$ then the $u$-coefficient will become $14,$ which will cancel with the coefficient of $-14$ in the first equation.

$$
\left\{\begin{aligned}-14u+v &=12 \\ (\,-2u-7v &=16\,)\,\times (-7)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}-14u+v &=12 \\ 14u+49v &=-112\end{aligned}\right.
$$

Now, when we add the two equations, the variable $u$ will be eliminated:

$$
\begin{aligned}-\cancel{14u}+v & =12 \\ \cancel{14u}+49v & =-112 \\ (v+49v) & =(12-112) \\ 50v & =-100 \\ v & =-2\end{aligned}
$$

So, the solution must have $v=-2.$ However, we still need to find $u.$ To do this, we substitute $v=-2$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}-14u+v & =12 \\ -14u+(-2) & =12 \\ -14u-2 & =12 \\ -14u & =14 \\ u & =-1\end{aligned}
$$

Therefore, the solution to the system of equations is $u=-1,\,v=-2,$ which can be expressed as $(-1,-2).$

## hard-moderate_blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}15a-2b &=22 \\ 3a-b &=2\end{aligned}\right.
$$

The solution $(a,b)$ to this system is $($
{{field-1}}$\,,$
{{field-2}}
$).$

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "2",
        ":answer/id": "c141adca-ad72-502b-aad9-af97bfc6ac63"
      }
    ],
    ":answer-field/id": "45ca5c70-7b2c-50a0-a931-69f8e67754ce",
    ":answer-field/correct": [
      ":answer/id",
      "c141adca-ad72-502b-aad9-af97bfc6ac63"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "4",
        ":answer/id": "a250b226-5a2a-50f6-95de-62466127b869"
      }
    ],
    ":answer-field/id": "4370507a-081a-5c20-9383-2d53a11af6fd",
    ":answer-field/correct": [
      ":answer/id",
      "a250b226-5a2a-50f6-95de-62466127b869"
    ]
  }
]
```

Notice that the coefficient of $a$ in the  first  equation is $15,$ while in the second equation it is $3.$ 

If we multiply the second equation by $-5,$ then the $a$-coefficient will become $-15,$ which will cancel with the coefficient of $15$ in the first equation.

$$
\left\{\begin{aligned}15a-2b &=22 \\ (\,3a-b &=2\,)\,\times (-5)\end{aligned}\right.\,⟹\,\left\{\begin{aligned}15a-2b &=22 \\ -15a+5b &=-10\end{aligned}\right.
$$

Now, when we add the two equations, the variable $a$ will be eliminated:

$$
\begin{aligned}\cancel{15a}-2b & =22 \\ -\cancel{15a}+5b & =-10 \\ (-2b+5b) & =(22-10) \\ 3b & =12 \\ b & =4\end{aligned}
$$

So, the solution must have $b=4.$ However, we still need to find $a.$ To do this, we substitute $b=4$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}15a-2b & =22 \\ 15a-2(4) & =22 \\ 15a-8 & =22 \\ 15a & =30 \\ a & =2\end{aligned}
$$

Therefore, the solution to the system of equations is $a=2,\,b=4,$ which can be expressed as $(2,4).$

## hard-moderate_blank_solution

Consider the following system of equations:

$$
\left\{\begin{aligned}2u+5v &=7 \\ -12u-7v &=-19\end{aligned}\right.
$$

The solution $(u,v)$ to this system is $($
{{field-1}}$\,,$
{{field-2}}
$).$

```json
[
  {
    ":answer-field/key": "field-1",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "1",
        ":answer/id": "db1bc017-79ad-546b-a673-66fceaeb6b16"
      }
    ],
    ":answer-field/id": "46d6319e-bcb8-56ce-a428-99b859c19ee7",
    ":answer-field/correct": [
      ":answer/id",
      "db1bc017-79ad-546b-a673-66fceaeb6b16"
    ]
  },
  {
    ":answer-field/key": "field-2",
    ":answer-field/type": ":answer-field.type/blank",
    ":answer-field/choices": [
      {
        ":answer/type": ":answer.type/math",
        ":answer/value": "1",
        ":answer/id": "751ace90-8034-5608-b783-9eefc19f7e7d"
      }
    ],
    ":answer-field/id": "353164d9-68f5-5610-9887-15bb7e46c1b2",
    ":answer-field/correct": [
      ":answer/id",
      "751ace90-8034-5608-b783-9eefc19f7e7d"
    ]
  }
]
```

Notice that the coefficient of $u$ in the  first  equation is $2,$ while in the second equation it is $-12.$ 

If we multiply the first equation by $6,$ then the $u$-coefficient will become $12,$ which will cancel with the coefficient of $-12$ in the second equation.

$$
\left\{\begin{aligned}(\,2u+5v &=7\,)\,\times (6) \\ -12u-7v &=-19\end{aligned}\right.\,⟹\,\left\{\begin{aligned}12u+30v &=42 \\ -12u-7v &=-19\end{aligned}\right.
$$

Now, when we add the two equations, the variable $u$ will be eliminated:

$$
\begin{aligned}\cancel{12u}+30v & =42 \\ -\cancel{12u}-7v & =-19 \\ (30v-7v) & =(42-19) \\ 23v & =23 \\ v & =1\end{aligned}
$$

So, the solution must have $v=1.$ However, we still need to find $u.$ To do this, we substitute $v=1$ back into one of the equations. Let's choose the first equation:

$$
\begin{aligned}2u+5v & =7 \\ 2u+5(1) & =7 \\ 2u+5 & =7 \\ 2u & =2 \\ u & =1\end{aligned}
$$

Therefore, the solution to the system of equations is $u=1,\,v=1,$ which can be expressed as $(1,1).$
