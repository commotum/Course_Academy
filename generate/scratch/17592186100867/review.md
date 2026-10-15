# Source and variant review

Original parameters and changed operands are shown for every supported profile. Comparison covers the full prompt, field contract, bank, and three solution stages. Source notation and generated notation are intentionally kept separate.

## q-127267

Source:

$\begin{bmatrix}6 & -4 & -6 \\ -2 & 5 & 2 \\ -1 & -4 & 1\end{bmatrix}\begin{bmatrix}2 \\ -1 \\ 2\end{bmatrix}=$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}\begin{bmatrix}6 & -4 & -6 \\ -2 & 5 & 2 \\ -1 & -4 & 1\end{bmatrix}\begin{bmatrix}2 \\ -1 \\ 2\end{bmatrix} & =\begin{bmatrix}6\cdot 2+(-4)\cdot (-1)+(-6)\cdot 2 \\ (-2)\cdot 2+5\cdot (-1)+2\cdot 2 \\ (-1)\cdot 2+(-4)\cdot (-1)+1\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}12+4-12 \\ -4-5+4 \\ -2+4+2\end{bmatrix} \\  & =\begin{bmatrix}4 \\ -5 \\ 4\end{bmatrix}\end{aligned}
$$

Original-parameter replay:

$\begin{bmatrix}6 & -4 & -6 \\ -2 & 5 & 2 \\ -1 & -4 & 1\end{bmatrix}\begin{bmatrix}2 \\ -1 \\ 2\end{bmatrix}=$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}\begin{bmatrix}6 & -4 & -6 \\ -2 & 5 & 2 \\ -1 & -4 & 1\end{bmatrix}\begin{bmatrix}2 \\ -1 \\ 2\end{bmatrix} & =\begin{bmatrix}6\cdot 2+(-4)\cdot (-1)+(-6)\cdot 2 \\ (-2)\cdot 2+5\cdot (-1)+2\cdot 2 \\ (-1)\cdot 2+(-4)\cdot (-1)+1\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}12+4-12 \\ -4-5+4 \\ -2+4+2\end{bmatrix} \\  & =\begin{bmatrix}4 \\ -5 \\ 4\end{bmatrix}\end{aligned}
$$

Variant:

$\begin{bmatrix}4 & 5 & -7 \\ 0 & 8 & 7 \\ 4 & 1 & 7\end{bmatrix}\begin{bmatrix}3 \\ -2 \\ 8\end{bmatrix}=$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}\begin{bmatrix}4 & 5 & -7 \\ 0 & 8 & 7 \\ 4 & 1 & 7\end{bmatrix}\begin{bmatrix}3 \\ -2 \\ 8\end{bmatrix} & =\begin{bmatrix}4\cdot 3+5\cdot (-2)+(-7)\cdot 8 \\ 0\cdot 3+8\cdot (-2)+7\cdot 8 \\ 4\cdot 3+1\cdot (-2)+7\cdot 8\end{bmatrix} \\  & =\begin{bmatrix}12-10-56 \\ 0-16+56 \\ 12-2+56\end{bmatrix} \\  & =\begin{bmatrix}-54 \\ 40 \\ 66\end{bmatrix}\end{aligned}
$$

[{":answer-field/id": "25a08e17-7025-5e46-8ab9-13a69b548ed4", ":answer-field/key": "selection", ":answer-field/type": ":answer-field.type/radio", ":answer-field/choices": [{":answer/id": "3d26fe06-2bdb-5011-9e6a-c7e097d088d3", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ -40 \\\\ 66\\end{bmatrix}"}, {":answer/id": "1af1fac1-9eb3-579d-b7a4-8a6961685367", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ -54 \\\\ -66\\end{bmatrix}"}, {":answer/id": "cb456a44-a490-591e-a804-003ec45a33b3", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ -40 \\\\ -66\\end{bmatrix}"}, {":answer/id": "fd17a6c8-616a-5bb7-8d48-7972579183b9", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ 40 \\\\ 66\\end{bmatrix}"}, {":answer/id": "62f78ef0-c292-5b12-9a01-1bbebc812828", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ 40 \\\\ -66\\end{bmatrix}"}], ":answer-field/correct": [":answer/id", "fd17a6c8-616a-5bb7-8d48-7972579183b9"]}]

Variant:

$\begin{bmatrix}-4 & -6 & 0 \\ -5 & 7 & 6 \\ 7 & 4 & -2\end{bmatrix}\begin{bmatrix}-5 \\ 7 \\ -8\end{bmatrix}=$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}\begin{bmatrix}-4 & -6 & 0 \\ -5 & 7 & 6 \\ 7 & 4 & -2\end{bmatrix}\begin{bmatrix}-5 \\ 7 \\ -8\end{bmatrix} & =\begin{bmatrix}(-4)\cdot (-5)+(-6)\cdot 7+0\cdot (-8) \\ (-5)\cdot (-5)+7\cdot 7+6\cdot (-8) \\ 7\cdot (-5)+4\cdot 7+(-2)\cdot (-8)\end{bmatrix} \\  & =\begin{bmatrix}20-42+0 \\ 25+49-48 \\ -35+28+16\end{bmatrix} \\  & =\begin{bmatrix}-22 \\ 26 \\ 9\end{bmatrix}\end{aligned}
$$

[{":answer-field/id": "0e798698-7ed6-57a6-8df1-658d6cc83a9b", ":answer-field/key": "selection", ":answer-field/type": ":answer-field.type/radio", ":answer-field/choices": [{":answer/id": "de9eb5ce-c448-57fd-955d-1f4ff93b1332", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ -26 \\\\ 9\\end{bmatrix}"}, {":answer/id": "82c58228-f7b3-5e7c-b3d9-7a8e05e5504a", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ 26 \\\\ -9\\end{bmatrix}"}, {":answer/id": "bde6d1c9-1423-5f6b-8514-0b5f3ca50a7a", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ -26 \\\\ -9\\end{bmatrix}"}, {":answer/id": "11fa6bf5-49c5-5568-94b3-8ceed32d7f41", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ 26 \\\\ 9\\end{bmatrix}"}, {":answer/id": "a53d6bc8-b401-51c4-94ca-6bacde004531", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ -22 \\\\ -9\\end{bmatrix}"}], ":answer-field/correct": [":answer/id", "11fa6bf5-49c5-5568-94b3-8ceed32d7f41"]}]

## q-318606

Source:

Find $Nz$ if
$N=\begin{bmatrix}-8 & 1 & 2 \\ 3 & -6 & 5 \\ 4 & 2 & 7\end{bmatrix}$
and
$z=\begin{bmatrix}3 \\ -4 \\ 2\end{bmatrix}.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| $Nz=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Nz & =\begin{bmatrix}-8 & 1 & 2 \\ 3 & -6 & 5 \\ 4 & 2 & 7\end{bmatrix}\begin{bmatrix}3 \\ -4 \\ 2\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}(-8)\cdot 3 & + & \,\,\,\,\,\,\,1\cdot (-4) & + & 2\cdot 2 \\ 3\cdot 3 & + & (-6)\cdot (-4) & + & 5\cdot 2 \\ 4\cdot 3 & + & \,\,\,\,\,\,\,2\cdot (-4) & + & 7\cdot 2\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}-24 & + & (-4) & + & 4 \\ 9 & + & \,\,\,24 & + & 10 \\ 12 & + & (-8) & + & 14\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}-24 \\ 43 \\ 18\end{bmatrix}\end{aligned}
$$

Original-parameter replay:

Find $Nz$ if
$N=\begin{bmatrix}-8 & 1 & 2 \\ 3 & -6 & 5 \\ 4 & 2 & 7\end{bmatrix}$
and
$z=\begin{bmatrix}3 \\ -4 \\ 2\end{bmatrix}.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| $Nz=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Nz & =\begin{bmatrix}-8 & 1 & 2 \\ 3 & -6 & 5 \\ 4 & 2 & 7\end{bmatrix}\begin{bmatrix}3 \\ -4 \\ 2\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}(-8)\cdot 3 & + & 1\cdot (-4) & + & 2\cdot 2 \\ 3\cdot 3 & + & (-6)\cdot (-4) & + & 5\cdot 2 \\ 4\cdot 3 & + & 2\cdot (-4) & + & 7\cdot 2\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}(-24) & + & (-4) & + & 4 \\ 9 & + & 24 & + & 10 \\ 12 & + & (-8) & + & 14\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}-24 \\ 43 \\ 18\end{bmatrix}\end{aligned}
$$

Variant:

Find $Bz$ if
$B=\begin{bmatrix}4 & 5 & -7 \\ 0 & 8 & 7 \\ 4 & 1 & 7\end{bmatrix}$
and
$z=\begin{bmatrix}3 \\ -2 \\ 8\end{bmatrix}.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| $Bz=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Bz & =\begin{bmatrix}4 & 5 & -7 \\ 0 & 8 & 7 \\ 4 & 1 & 7\end{bmatrix}\begin{bmatrix}3 \\ -2 \\ 8\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}4\cdot 3 & + & 5\cdot (-2) & + & (-7)\cdot 8 \\ 0\cdot 3 & + & 8\cdot (-2) & + & 7\cdot 8 \\ 4\cdot 3 & + & 1\cdot (-2) & + & 7\cdot 8\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}12 & + & (-10) & + & (-56) \\ 0 & + & (-16) & + & 56 \\ 12 & + & (-2) & + & 56\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}-54 \\ 40 \\ 66\end{bmatrix}\end{aligned}
$$

[{":answer-field/id": "e28cca66-e70a-5d72-9daa-935ca3d3824b", ":answer-field/key": "field-1", ":answer-field/type": ":answer-field.type/blank", ":answer-field/choices": [{":answer/id": "a67ad6a9-18e3-58c5-94ef-f27775ffba43", ":answer/type": ":answer.type/math", ":answer/value": "-54"}], ":answer-field/correct": [":answer/id", "a67ad6a9-18e3-58c5-94ef-f27775ffba43"]}, {":answer-field/id": "59322ef5-2f58-577d-8180-767e8522a0c4", ":answer-field/key": "field-2", ":answer-field/type": ":answer-field.type/blank", ":answer-field/choices": [{":answer/id": "fe7164a8-7a19-56d4-89d7-4ae8a10db90c", ":answer/type": ":answer.type/math", ":answer/value": "40"}], ":answer-field/correct": [":answer/id", "fe7164a8-7a19-56d4-89d7-4ae8a10db90c"]}, {":answer-field/id": "bc4060ad-84a5-551d-bafb-d15107ae0a41", ":answer-field/key": "field-3", ":answer-field/type": ":answer-field.type/blank", ":answer-field/choices": [{":answer/id": "22eac632-4194-50fd-8a48-c09ba269ca39", ":answer/type": ":answer.type/math", ":answer/value": "66"}], ":answer-field/correct": [":answer/id", "22eac632-4194-50fd-8a48-c09ba269ca39"]}]

Variant:

Find $Pv$ if
$P=\begin{bmatrix}-4 & -6 & 0 \\ -5 & 7 & 6 \\ 7 & 4 & -2\end{bmatrix}$
and
$v=\begin{bmatrix}-5 \\ 7 \\ -8\end{bmatrix}.$

|  |  | {{field-1}} |  |
| --- | --- | --- | --- |
| $Pv=\,\,$ |  | {{field-2}} |  |
|  |  | {{field-3}} |  |

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Pv & =\begin{bmatrix}-4 & -6 & 0 \\ -5 & 7 & 6 \\ 7 & 4 & -2\end{bmatrix}\begin{bmatrix}-5 \\ 7 \\ -8\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}(-4)\cdot (-5) & + & (-6)\cdot 7 & + & 0\cdot (-8) \\ (-5)\cdot (-5) & + & 7\cdot 7 & + & 6\cdot (-8) \\ 7\cdot (-5) & + & 4\cdot 7 & + & (-2)\cdot (-8)\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}\begin{aligned}20 & + & (-42) & + & 0 \\ 25 & + & 49 & + & (-48) \\ (-35) & + & 28 & + & 16\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}-22 \\ 26 \\ 9\end{bmatrix}\end{aligned}
$$

[{":answer-field/id": "e7ea7947-d27b-5ce7-b2eb-aba999edcb9f", ":answer-field/key": "field-1", ":answer-field/type": ":answer-field.type/blank", ":answer-field/choices": [{":answer/id": "51b93a6e-0104-5b72-adb5-1abd6e0133db", ":answer/type": ":answer.type/math", ":answer/value": "-22"}], ":answer-field/correct": [":answer/id", "51b93a6e-0104-5b72-adb5-1abd6e0133db"]}, {":answer-field/id": "256c8c37-c407-5b9a-8dd6-c79c867b0ea3", ":answer-field/key": "field-2", ":answer-field/type": ":answer-field.type/blank", ":answer-field/choices": [{":answer/id": "0d473660-1646-5aa4-b6ef-40c589838d22", ":answer/type": ":answer.type/math", ":answer/value": "26"}], ":answer-field/correct": [":answer/id", "0d473660-1646-5aa4-b6ef-40c589838d22"]}, {":answer-field/id": "76c1372c-8615-54ef-abb9-82ba47c74bb3", ":answer-field/key": "field-3", ":answer-field/type": ":answer-field.type/blank", ":answer-field/choices": [{":answer/id": "6486ff8a-6d8e-5220-b599-906ba89bef03", ":answer/type": ":answer.type/math", ":answer/value": "9"}], ":answer-field/correct": [":answer/id", "6486ff8a-6d8e-5220-b599-906ba89bef03"]}]

## q-318622

Source:

Compute the following:

| $\begin{bmatrix}-4 & 6 & 2 \\ 5 & -3 & 7 \\ 1 & 8 & -2\end{bmatrix}\begin{bmatrix}3 \\ -1 \\ 4\end{bmatrix}=\,\,$ |  | {{field-1}} |  |
| --- | --- | --- | --- |
|  | {{field-2}} |  |  |
|  | {{field-3}} |  |  |

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}\begin{bmatrix}-4 & 6 & 2 \\ 5 & -3 & 7 \\ 1 & 8 & -2\end{bmatrix}\begin{bmatrix}3 \\ -1 \\ 4\end{bmatrix} & =\begin{bmatrix}\begin{aligned}-4\cdot 3 & + & \,\,\,\,\,\,\,6\cdot (-1) & + & \,\,\,\,\,\,\,2\cdot 4 \\ 5\cdot 3 & + & (-3)\cdot (-1) & + & \,\,\,\,\,\,\,7\cdot 4 \\ 1\cdot 3 & + & \,\,\,\,\,\,\,8\cdot (-1) & + & (-2)\cdot 4\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}-12 & + & (-6) & + & 8 \\ 15 & + & 3 & + & 28 \\ 3 & + & (-8) & + & (-8)\end{bmatrix} \\  & =\begin{bmatrix}-10 \\ 46 \\ -13\end{bmatrix}.\end{aligned}
$$

Original-parameter replay:

Compute the following:

| $\begin{bmatrix}-4 & 6 & 2 \\ 5 & -3 & 7 \\ 1 & 8 & -2\end{bmatrix}\begin{bmatrix}3 \\ -1 \\ 4\end{bmatrix}=\,\,$ |  | {{field-1}} |  |
| --- | --- | --- | --- |
|  | {{field-2}} |  |  |
|  | {{field-3}} |  |  |

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}\begin{bmatrix}-4 & 6 & 2 \\ 5 & -3 & 7 \\ 1 & 8 & -2\end{bmatrix}\begin{bmatrix}3 \\ -1 \\ 4\end{bmatrix} & =\begin{bmatrix}\begin{aligned}(-4)\cdot 3 & + & 6\cdot (-1) & + & 2\cdot 4 \\ 5\cdot 3 & + & (-3)\cdot (-1) & + & 7\cdot 4 \\ 1\cdot 3 & + & 8\cdot (-1) & + & (-2)\cdot 4\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}(-12) & + & (-6) & + & 8 \\ 15 & + & 3 & + & 28 \\ 3 & + & (-8) & + & (-8)\end{bmatrix} \\  & =\begin{bmatrix}-10 \\ 46 \\ -13\end{bmatrix}.\end{aligned}
$$

Variant:

Compute the following:

| $\begin{bmatrix}4 & 5 & -7 \\ 0 & 8 & 7 \\ 4 & 1 & 7\end{bmatrix}\begin{bmatrix}3 \\ -2 \\ 8\end{bmatrix}=\,\,$ |  | {{field-1}} |  |
| --- | --- | --- | --- |
|  | {{field-2}} |  |  |
|  | {{field-3}} |  |  |

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}\begin{bmatrix}4 & 5 & -7 \\ 0 & 8 & 7 \\ 4 & 1 & 7\end{bmatrix}\begin{bmatrix}3 \\ -2 \\ 8\end{bmatrix} & =\begin{bmatrix}\begin{aligned}4\cdot 3 & + & 5\cdot (-2) & + & (-7)\cdot 8 \\ 0\cdot 3 & + & 8\cdot (-2) & + & 7\cdot 8 \\ 4\cdot 3 & + & 1\cdot (-2) & + & 7\cdot 8\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}12 & + & (-10) & + & (-56) \\ 0 & + & (-16) & + & 56 \\ 12 & + & (-2) & + & 56\end{bmatrix} \\  & =\begin{bmatrix}-54 \\ 40 \\ 66\end{bmatrix}.\end{aligned}
$$

[{":answer-field/id": "14380ec8-318c-53e1-882e-3e1d58f29416", ":answer-field/key": "field-1", ":answer-field/type": ":answer-field.type/blank", ":answer-field/choices": [{":answer/id": "098321db-17ae-5afd-94fd-851df3a94895", ":answer/type": ":answer.type/math", ":answer/value": "-54"}], ":answer-field/correct": [":answer/id", "098321db-17ae-5afd-94fd-851df3a94895"]}, {":answer-field/id": "08f79317-799f-5a68-a591-c2d778a822b9", ":answer-field/key": "field-2", ":answer-field/type": ":answer-field.type/blank", ":answer-field/choices": [{":answer/id": "14d0d74c-fa4b-5eac-90b1-39a62599b4c1", ":answer/type": ":answer.type/math", ":answer/value": "40"}], ":answer-field/correct": [":answer/id", "14d0d74c-fa4b-5eac-90b1-39a62599b4c1"]}, {":answer-field/id": "4dd3c1b2-e1c1-594d-8ee8-360ebfa44fdd", ":answer-field/key": "field-3", ":answer-field/type": ":answer-field.type/blank", ":answer-field/choices": [{":answer/id": "df7a5bbc-e344-5f3e-8e49-149c17f889db", ":answer/type": ":answer.type/math", ":answer/value": "66"}], ":answer-field/correct": [":answer/id", "df7a5bbc-e344-5f3e-8e49-149c17f889db"]}]

Variant:

Compute the following:

| $\begin{bmatrix}-4 & -6 & 0 \\ -5 & 7 & 6 \\ 7 & 4 & -2\end{bmatrix}\begin{bmatrix}-5 \\ 7 \\ -8\end{bmatrix}=\,\,$ |  | {{field-1}} |  |
| --- | --- | --- | --- |
|  | {{field-2}} |  |  |
|  | {{field-3}} |  |  |

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}\begin{bmatrix}-4 & -6 & 0 \\ -5 & 7 & 6 \\ 7 & 4 & -2\end{bmatrix}\begin{bmatrix}-5 \\ 7 \\ -8\end{bmatrix} & =\begin{bmatrix}\begin{aligned}(-4)\cdot (-5) & + & (-6)\cdot 7 & + & 0\cdot (-8) \\ (-5)\cdot (-5) & + & 7\cdot 7 & + & 6\cdot (-8) \\ 7\cdot (-5) & + & 4\cdot 7 & + & (-2)\cdot (-8)\end{aligned}\end{bmatrix} \\  & =\begin{bmatrix}20 & + & (-42) & + & 0 \\ 25 & + & 49 & + & (-48) \\ (-35) & + & 28 & + & 16\end{bmatrix} \\  & =\begin{bmatrix}-22 \\ 26 \\ 9\end{bmatrix}.\end{aligned}
$$

[{":answer-field/id": "256527d0-c427-587e-8fe6-931760f1242e", ":answer-field/key": "field-1", ":answer-field/type": ":answer-field.type/blank", ":answer-field/choices": [{":answer/id": "b9f22c81-bac5-5aa7-ab4a-e4dcac019d6e", ":answer/type": ":answer.type/math", ":answer/value": "-22"}], ":answer-field/correct": [":answer/id", "b9f22c81-bac5-5aa7-ab4a-e4dcac019d6e"]}, {":answer-field/id": "0c82ba27-537f-5714-b1a5-5249fd1b2f98", ":answer-field/key": "field-2", ":answer-field/type": ":answer-field.type/blank", ":answer-field/choices": [{":answer/id": "93d14cdd-ade8-5825-9eb2-feaa3e6128a4", ":answer/type": ":answer.type/math", ":answer/value": "26"}], ":answer-field/correct": [":answer/id", "93d14cdd-ade8-5825-9eb2-feaa3e6128a4"]}, {":answer-field/id": "70fa1a7e-9fac-5812-8367-ac192b635913", ":answer-field/key": "field-3", ":answer-field/type": ":answer-field.type/blank", ":answer-field/choices": [{":answer/id": "74e8a03e-38e6-57a1-8e92-1f9d39823b54", ":answer/type": ":answer.type/math", ":answer/value": "9"}], ":answer-field/correct": [":answer/id", "74e8a03e-38e6-57a1-8e92-1f9d39823b54"]}]

## q-70188

Source:

Find $By$ if 
$B=\begin{bmatrix}2 & 1 & 1 \\ -3 & 2 & -1 \\ 4 & 0 & -3\end{bmatrix}$
and
$y=\begin{bmatrix}6 \\ -3 \\ 1\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}By & =\begin{bmatrix}2 & 1 & 1 \\ -3 & 2 & -1 \\ 4 & 0 & -3\end{bmatrix}\begin{bmatrix}6 \\ -3 \\ 1\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 6+1\cdot (-3)+1\cdot 1 \\ (-3)\cdot 6+2\cdot (-3)+(-1)\cdot 1 \\ 4\cdot 6+0\cdot (-3)+(-3)\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}12-3+1 \\ -18-6-1 \\ 24-0-3\end{bmatrix} \\  & =\begin{bmatrix}10 \\ -25 \\ 21\end{bmatrix}\end{aligned}
$$

Original-parameter replay:

Find $By$ if 
$B=\begin{bmatrix}2 & 1 & 1 \\ -3 & 2 & -1 \\ 4 & 0 & -3\end{bmatrix}$
and
$y=\begin{bmatrix}6 \\ -3 \\ 1\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}By & =\begin{bmatrix}2 & 1 & 1 \\ -3 & 2 & -1 \\ 4 & 0 & -3\end{bmatrix}\begin{bmatrix}6 \\ -3 \\ 1\end{bmatrix} \\  & =\begin{bmatrix}2\cdot 6+1\cdot (-3)+1\cdot 1 \\ (-3)\cdot 6+2\cdot (-3)+(-1)\cdot 1 \\ 4\cdot 6+0\cdot (-3)+(-3)\cdot 1\end{bmatrix} \\  & =\begin{bmatrix}12-3+1 \\ -18-6-1 \\ 24+0-3\end{bmatrix} \\  & =\begin{bmatrix}10 \\ -25 \\ 21\end{bmatrix}\end{aligned}
$$

Variant:

Find $Bz$ if 
$B=\begin{bmatrix}4 & 5 & -7 \\ 0 & 8 & 7 \\ 4 & 1 & 7\end{bmatrix}$
and
$z=\begin{bmatrix}3 \\ -2 \\ 8\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Bz & =\begin{bmatrix}4 & 5 & -7 \\ 0 & 8 & 7 \\ 4 & 1 & 7\end{bmatrix}\begin{bmatrix}3 \\ -2 \\ 8\end{bmatrix} \\  & =\begin{bmatrix}4\cdot 3+5\cdot (-2)+(-7)\cdot 8 \\ 0\cdot 3+8\cdot (-2)+7\cdot 8 \\ 4\cdot 3+1\cdot (-2)+7\cdot 8\end{bmatrix} \\  & =\begin{bmatrix}12-10-56 \\ 0-16+56 \\ 12-2+56\end{bmatrix} \\  & =\begin{bmatrix}-54 \\ 40 \\ 66\end{bmatrix}\end{aligned}
$$

[{":answer-field/id": "873e4412-74ef-5ba1-a82a-5fe92a2152b6", ":answer-field/key": "selection", ":answer-field/type": ":answer-field.type/radio", ":answer-field/choices": [{":answer/id": "9101d80d-ee0c-505d-a939-184d9f516a2b", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}54 \\\\ -40 \\\\ 66\\end{bmatrix}"}, {":answer/id": "56b6a448-d78e-53eb-a466-dd6a9f653572", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ -40 \\\\ 66\\end{bmatrix}"}, {":answer/id": "25544328-d85c-59bc-adb8-88892b2c6de3", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ 40 \\\\ -66\\end{bmatrix}"}, {":answer/id": "0b3f833f-10f3-5ac8-aede-c863c1f7b8a2", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ 40 \\\\ 66\\end{bmatrix}"}, {":answer/id": "5722ccb8-d042-5cb9-8a8d-62f684100f35", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ -40 \\\\ -66\\end{bmatrix}"}], ":answer-field/correct": [":answer/id", "0b3f833f-10f3-5ac8-aede-c863c1f7b8a2"]}]

Variant:

Find $Pv$ if 
$P=\begin{bmatrix}-4 & -6 & 0 \\ -5 & 7 & 6 \\ 7 & 4 & -2\end{bmatrix}$
and
$v=\begin{bmatrix}-5 \\ 7 \\ -8\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Pv & =\begin{bmatrix}-4 & -6 & 0 \\ -5 & 7 & 6 \\ 7 & 4 & -2\end{bmatrix}\begin{bmatrix}-5 \\ 7 \\ -8\end{bmatrix} \\  & =\begin{bmatrix}(-4)\cdot (-5)+(-6)\cdot 7+0\cdot (-8) \\ (-5)\cdot (-5)+7\cdot 7+6\cdot (-8) \\ 7\cdot (-5)+4\cdot 7+(-2)\cdot (-8)\end{bmatrix} \\  & =\begin{bmatrix}20-42+0 \\ 25+49-48 \\ -35+28+16\end{bmatrix} \\  & =\begin{bmatrix}-22 \\ 26 \\ 9\end{bmatrix}\end{aligned}
$$

[{":answer-field/id": "28495cc6-9b98-5882-aa79-e83eaa3d5a20", ":answer-field/key": "selection", ":answer-field/type": ":answer-field.type/radio", ":answer-field/choices": [{":answer/id": "fd1edfc9-ce90-50fe-a553-a8f0a89a0cbf", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}22 \\\\ -26 \\\\ 9\\end{bmatrix}"}, {":answer/id": "193c2e6a-13e0-5b20-bd77-c0dd0521fca8", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ -26 \\\\ -9\\end{bmatrix}"}, {":answer/id": "62741299-4835-53c6-bdc5-38c4ca37ba06", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ 26 \\\\ -9\\end{bmatrix}"}, {":answer/id": "3daeb227-7590-5eab-ab0b-31e56180c489", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ 26 \\\\ 9\\end{bmatrix}"}, {":answer/id": "a201fb2c-1363-52c2-94b1-4f5e8ad64c11", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ -26 \\\\ 9\\end{bmatrix}"}], ":answer-field/correct": [":answer/id", "3daeb227-7590-5eab-ab0b-31e56180c489"]}]

## q-70191

Source:

$\begin{bmatrix}0 & -4 & 1 \\ 1 & 2 & -3 \\ -1 & 2 & 4\end{bmatrix}\begin{bmatrix}8 \\ 4 \\ 2\end{bmatrix}=$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}\begin{bmatrix}0 & -4 & 1 \\ 1 & 2 & -3 \\ -1 & 2 & 4\end{bmatrix}\begin{bmatrix}8 \\ 4 \\ 2\end{bmatrix} & =\begin{bmatrix}0\cdot 8+(-4)\cdot 4+1\cdot 2 \\ 1\cdot 8+2\cdot 4+(-3)\cdot 2 \\ (-1)\cdot 8+2\cdot 4+4\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}0-16+2 \\ 8+8-6 \\ -8+8+8\end{bmatrix} \\  & =\begin{bmatrix}-14 \\ 10 \\ 8\end{bmatrix}\end{aligned}
$$

Original-parameter replay:

$\begin{bmatrix}0 & -4 & 1 \\ 1 & 2 & -3 \\ -1 & 2 & 4\end{bmatrix}\begin{bmatrix}8 \\ 4 \\ 2\end{bmatrix}=$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}\begin{bmatrix}0 & -4 & 1 \\ 1 & 2 & -3 \\ -1 & 2 & 4\end{bmatrix}\begin{bmatrix}8 \\ 4 \\ 2\end{bmatrix} & =\begin{bmatrix}0\cdot 8+(-4)\cdot 4+1\cdot 2 \\ 1\cdot 8+2\cdot 4+(-3)\cdot 2 \\ (-1)\cdot 8+2\cdot 4+4\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}0-16+2 \\ 8+8-6 \\ -8+8+8\end{bmatrix} \\  & =\begin{bmatrix}-14 \\ 10 \\ 8\end{bmatrix}\end{aligned}
$$

Variant:

$\begin{bmatrix}4 & 5 & -7 \\ 0 & 8 & 7 \\ 4 & 1 & 7\end{bmatrix}\begin{bmatrix}3 \\ -2 \\ 8\end{bmatrix}=$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}\begin{bmatrix}4 & 5 & -7 \\ 0 & 8 & 7 \\ 4 & 1 & 7\end{bmatrix}\begin{bmatrix}3 \\ -2 \\ 8\end{bmatrix} & =\begin{bmatrix}4\cdot 3+5\cdot (-2)+(-7)\cdot 8 \\ 0\cdot 3+8\cdot (-2)+7\cdot 8 \\ 4\cdot 3+1\cdot (-2)+7\cdot 8\end{bmatrix} \\  & =\begin{bmatrix}12-10-56 \\ 0-16+56 \\ 12-2+56\end{bmatrix} \\  & =\begin{bmatrix}-54 \\ 40 \\ 66\end{bmatrix}\end{aligned}
$$

[{":answer-field/id": "36ab1abf-a455-536c-aa44-caac59aa1372", ":answer-field/key": "selection", ":answer-field/type": ":answer-field.type/radio", ":answer-field/choices": [{":answer/id": "1c4abd76-6dcd-5d59-8f7f-71306b5cbc77", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}54 \\\\ 40 \\\\ 66\\end{bmatrix}"}, {":answer/id": "90267384-7ab1-5029-924b-1379d6092d29", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ 40 \\\\ -66\\end{bmatrix}"}, {":answer/id": "6c6bf3b3-2c87-57c7-8e2d-b95ce614df48", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ -40 \\\\ -66\\end{bmatrix}"}, {":answer/id": "d135904f-a226-5f4e-8d5b-ebd570e23190", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ 40 \\\\ 66\\end{bmatrix}"}, {":answer/id": "a9649601-8943-5bcf-8d90-8ff05e194929", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ -40 \\\\ 66\\end{bmatrix}"}], ":answer-field/correct": [":answer/id", "d135904f-a226-5f4e-8d5b-ebd570e23190"]}]

Variant:

$\begin{bmatrix}-4 & -6 & 0 \\ -5 & 7 & 6 \\ 7 & 4 & -2\end{bmatrix}\begin{bmatrix}-5 \\ 7 \\ -8\end{bmatrix}=$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}\begin{bmatrix}-4 & -6 & 0 \\ -5 & 7 & 6 \\ 7 & 4 & -2\end{bmatrix}\begin{bmatrix}-5 \\ 7 \\ -8\end{bmatrix} & =\begin{bmatrix}(-4)\cdot (-5)+(-6)\cdot 7+0\cdot (-8) \\ (-5)\cdot (-5)+7\cdot 7+6\cdot (-8) \\ 7\cdot (-5)+4\cdot 7+(-2)\cdot (-8)\end{bmatrix} \\  & =\begin{bmatrix}20-42+0 \\ 25+49-48 \\ -35+28+16\end{bmatrix} \\  & =\begin{bmatrix}-22 \\ 26 \\ 9\end{bmatrix}\end{aligned}
$$

[{":answer-field/id": "41b48d1c-097a-5155-afe3-a78df33ddfbe", ":answer-field/key": "selection", ":answer-field/type": ":answer-field.type/radio", ":answer-field/choices": [{":answer/id": "ed9744bd-2b0a-5186-a3f5-b19ddcbac612", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}22 \\\\ 26 \\\\ 9\\end{bmatrix}"}, {":answer/id": "811d53a7-14d3-5387-a425-e5d24f19a0d0", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ -26 \\\\ 9\\end{bmatrix}"}, {":answer/id": "2f06714c-3336-5e73-9730-6e2f2ffea31e", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ -26 \\\\ -9\\end{bmatrix}"}, {":answer/id": "dda83063-b745-57dc-a868-0d00bd4b3b38", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ 26 \\\\ 9\\end{bmatrix}"}, {":answer/id": "9943f452-9b12-50fb-9e63-87d9d087fc26", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ 26 \\\\ -9\\end{bmatrix}"}], ":answer-field/correct": [":answer/id", "dda83063-b745-57dc-a868-0d00bd4b3b38"]}]

## q-70190

Source:

Find $Lz$ if 
$L=\begin{bmatrix}1 & 0 & 4 \\ 1 & 3 & -2 \\ 2 & 0 & -5\end{bmatrix}$
and
$z=\begin{bmatrix}-3 \\ 8 \\ 2\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Lz & =\begin{bmatrix}1 & 0 & 4 \\ 1 & 3 & -2 \\ 2 & 0 & -5\end{bmatrix}\begin{bmatrix}-3 \\ 8 \\ 2\end{bmatrix} \\  & =\begin{bmatrix}1\cdot (-3)+0\cdot 8+4\cdot 2 \\ 1\cdot (-3)+3\cdot 8+(-2)\cdot 2 \\ 2\cdot (-3)+0\cdot 8+(-5)\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}-3+0+8 \\ -3+24-4 \\ -6+0-10\end{bmatrix} \\  & =\begin{bmatrix}5 \\ 17 \\ -16\end{bmatrix}\end{aligned}
$$

Original-parameter replay:

Find $Lz$ if 
$L=\begin{bmatrix}1 & 0 & 4 \\ 1 & 3 & -2 \\ 2 & 0 & -5\end{bmatrix}$
and
$z=\begin{bmatrix}-3 \\ 8 \\ 2\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Lz & =\begin{bmatrix}1 & 0 & 4 \\ 1 & 3 & -2 \\ 2 & 0 & -5\end{bmatrix}\begin{bmatrix}-3 \\ 8 \\ 2\end{bmatrix} \\  & =\begin{bmatrix}1\cdot (-3)+0\cdot 8+4\cdot 2 \\ 1\cdot (-3)+3\cdot 8+(-2)\cdot 2 \\ 2\cdot (-3)+0\cdot 8+(-5)\cdot 2\end{bmatrix} \\  & =\begin{bmatrix}-3+0+8 \\ -3+24-4 \\ -6+0-10\end{bmatrix} \\  & =\begin{bmatrix}5 \\ 17 \\ -16\end{bmatrix}\end{aligned}
$$

Variant:

Find $Bz$ if 
$B=\begin{bmatrix}4 & 5 & -7 \\ 0 & 8 & 7 \\ 4 & 1 & 7\end{bmatrix}$
and
$z=\begin{bmatrix}3 \\ -2 \\ 8\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Bz & =\begin{bmatrix}4 & 5 & -7 \\ 0 & 8 & 7 \\ 4 & 1 & 7\end{bmatrix}\begin{bmatrix}3 \\ -2 \\ 8\end{bmatrix} \\  & =\begin{bmatrix}4\cdot 3+5\cdot (-2)+(-7)\cdot 8 \\ 0\cdot 3+8\cdot (-2)+7\cdot 8 \\ 4\cdot 3+1\cdot (-2)+7\cdot 8\end{bmatrix} \\  & =\begin{bmatrix}12-10-56 \\ 0-16+56 \\ 12-2+56\end{bmatrix} \\  & =\begin{bmatrix}-54 \\ 40 \\ 66\end{bmatrix}\end{aligned}
$$

[{":answer-field/id": "60ffce21-2c3f-596c-a6a6-9c2343aae629", ":answer-field/key": "selection", ":answer-field/type": ":answer-field.type/radio", ":answer-field/choices": [{":answer/id": "28ad5992-a894-58f1-b972-520384c1c524", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}54 \\\\ 40 \\\\ 66\\end{bmatrix}"}, {":answer/id": "d60a38d8-5904-5672-aec8-16729819a882", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}54 \\\\ -40 \\\\ 66\\end{bmatrix}"}, {":answer/id": "5b164dbe-e3f5-5272-8f9d-01c81bffc5ff", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ -40 \\\\ 66\\end{bmatrix}"}, {":answer/id": "867017aa-c920-5430-9ab9-24fbd4c3eb2a", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ 40 \\\\ 66\\end{bmatrix}"}, {":answer/id": "25a9afdf-cb14-5f89-8a02-f120d8ca901f", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ 40 \\\\ -66\\end{bmatrix}"}], ":answer-field/correct": [":answer/id", "867017aa-c920-5430-9ab9-24fbd4c3eb2a"]}]

Variant:

Find $Pv$ if 
$P=\begin{bmatrix}-4 & -6 & 0 \\ -5 & 7 & 6 \\ 7 & 4 & -2\end{bmatrix}$
and
$v=\begin{bmatrix}-5 \\ 7 \\ -8\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Pv & =\begin{bmatrix}-4 & -6 & 0 \\ -5 & 7 & 6 \\ 7 & 4 & -2\end{bmatrix}\begin{bmatrix}-5 \\ 7 \\ -8\end{bmatrix} \\  & =\begin{bmatrix}(-4)\cdot (-5)+(-6)\cdot 7+0\cdot (-8) \\ (-5)\cdot (-5)+7\cdot 7+6\cdot (-8) \\ 7\cdot (-5)+4\cdot 7+(-2)\cdot (-8)\end{bmatrix} \\  & =\begin{bmatrix}20-42+0 \\ 25+49-48 \\ -35+28+16\end{bmatrix} \\  & =\begin{bmatrix}-22 \\ 26 \\ 9\end{bmatrix}\end{aligned}
$$

[{":answer-field/id": "491d6f8d-d25e-5211-960b-69c73e536e3f", ":answer-field/key": "selection", ":answer-field/type": ":answer-field.type/radio", ":answer-field/choices": [{":answer/id": "8da7fcfd-5bd0-51e0-a08b-6e78bb437937", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}22 \\\\ 26 \\\\ 9\\end{bmatrix}"}, {":answer/id": "eadcc368-43e2-5974-8c9e-728007fdc728", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ 26 \\\\ -9\\end{bmatrix}"}, {":answer/id": "ad1106d1-851e-5c6d-961e-46bdfdc82ae2", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ -26 \\\\ 9\\end{bmatrix}"}, {":answer/id": "c79eeece-2f2e-50c6-aaf1-f90bb9e55c08", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ 26 \\\\ 9\\end{bmatrix}"}, {":answer/id": "abca50c5-c1eb-5108-a8d4-b071709b809e", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}22 \\\\ -26 \\\\ 9\\end{bmatrix}"}], ":answer-field/correct": [":answer/id", "c79eeece-2f2e-50c6-aaf1-f90bb9e55c08"]}]

## q-77350

Source:

Find $Pv$ if 
$P=\begin{bmatrix}1 & -1 & 2 \\ 1 & -1 & 3 \\ 1 & -1 & 4\end{bmatrix}$
and
$v=\begin{bmatrix}0 \\ 4 \\ -1\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Pv & =\begin{bmatrix}1 & -1 & 2 \\ 1 & -1 & 3 \\ 1 & -1 & 4\end{bmatrix}\begin{bmatrix}0 \\ 4 \\ -1\end{bmatrix} \\  & =\begin{bmatrix}1\cdot 0+(-1)\cdot 4+2\cdot (-1) \\ 1\cdot 0+(-1)\cdot 4+3\cdot (-1) \\ 1\cdot 0+(-1)\cdot 4+4\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}0-4-2 \\ 0-4-3 \\ 0-4-4\end{bmatrix} \\  & =\begin{bmatrix}-6 \\ -7 \\ -8\end{bmatrix}\end{aligned}
$$

Original-parameter replay:

Find $Pv$ if 
$P=\begin{bmatrix}1 & -1 & 2 \\ 1 & -1 & 3 \\ 1 & -1 & 4\end{bmatrix}$
and
$v=\begin{bmatrix}0 \\ 4 \\ -1\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Pv & =\begin{bmatrix}1 & -1 & 2 \\ 1 & -1 & 3 \\ 1 & -1 & 4\end{bmatrix}\begin{bmatrix}0 \\ 4 \\ -1\end{bmatrix} \\  & =\begin{bmatrix}1\cdot 0+(-1)\cdot 4+2\cdot (-1) \\ 1\cdot 0+(-1)\cdot 4+3\cdot (-1) \\ 1\cdot 0+(-1)\cdot 4+4\cdot (-1)\end{bmatrix} \\  & =\begin{bmatrix}0-4-2 \\ 0-4-3 \\ 0-4-4\end{bmatrix} \\  & =\begin{bmatrix}-6 \\ -7 \\ -8\end{bmatrix}\end{aligned}
$$

Variant:

Find $Bz$ if 
$B=\begin{bmatrix}4 & 5 & -7 \\ 0 & 8 & 7 \\ 4 & 1 & 7\end{bmatrix}$
and
$z=\begin{bmatrix}3 \\ -2 \\ 8\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Bz & =\begin{bmatrix}4 & 5 & -7 \\ 0 & 8 & 7 \\ 4 & 1 & 7\end{bmatrix}\begin{bmatrix}3 \\ -2 \\ 8\end{bmatrix} \\  & =\begin{bmatrix}4\cdot 3+5\cdot (-2)+(-7)\cdot 8 \\ 0\cdot 3+8\cdot (-2)+7\cdot 8 \\ 4\cdot 3+1\cdot (-2)+7\cdot 8\end{bmatrix} \\  & =\begin{bmatrix}12-10-56 \\ 0-16+56 \\ 12-2+56\end{bmatrix} \\  & =\begin{bmatrix}-54 \\ 40 \\ 66\end{bmatrix}\end{aligned}
$$

[{":answer-field/id": "59ac9efd-3bbc-57c4-a752-b5cd967a9538", ":answer-field/key": "selection", ":answer-field/type": ":answer-field.type/radio", ":answer-field/choices": [{":answer/id": "e9f3f3d9-afbd-5c7a-ac4b-352c666a6bbd", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ -40 \\\\ 66\\end{bmatrix}"}, {":answer/id": "356e86d7-dadf-5272-8bb7-bf3d1a0afe11", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}66 \\\\ 40 \\\\ -54\\end{bmatrix}"}, {":answer/id": "b1aacd8f-54cd-5a69-865e-f000116a7c21", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ 66 \\\\ 40\\end{bmatrix}"}, {":answer/id": "2e7c3224-2489-5242-a5bb-cc2d391be0be", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-54 \\\\ 40 \\\\ 66\\end{bmatrix}"}, {":answer/id": "a7c4049e-6d5f-51fd-970c-8a9f4d55af0e", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}54 \\\\ -40 \\\\ 66\\end{bmatrix}"}], ":answer-field/correct": [":answer/id", "2e7c3224-2489-5242-a5bb-cc2d391be0be"]}]

Variant:

Find $Pv$ if 
$P=\begin{bmatrix}-4 & -6 & 0 \\ -5 & 7 & 6 \\ 7 & 4 & -2\end{bmatrix}$
and
$v=\begin{bmatrix}-5 \\ 7 \\ -8\end{bmatrix}.$

We multiply each row in the matrix by the column vector using the dot product:

$$
\begin{aligned}Pv & =\begin{bmatrix}-4 & -6 & 0 \\ -5 & 7 & 6 \\ 7 & 4 & -2\end{bmatrix}\begin{bmatrix}-5 \\ 7 \\ -8\end{bmatrix} \\  & =\begin{bmatrix}(-4)\cdot (-5)+(-6)\cdot 7+0\cdot (-8) \\ (-5)\cdot (-5)+7\cdot 7+6\cdot (-8) \\ 7\cdot (-5)+4\cdot 7+(-2)\cdot (-8)\end{bmatrix} \\  & =\begin{bmatrix}20-42+0 \\ 25+49-48 \\ -35+28+16\end{bmatrix} \\  & =\begin{bmatrix}-22 \\ 26 \\ 9\end{bmatrix}\end{aligned}
$$

[{":answer-field/id": "a9e76bbb-084f-568f-87de-6688c7e174db", ":answer-field/key": "selection", ":answer-field/type": ":answer-field.type/radio", ":answer-field/choices": [{":answer/id": "d1ee1d0a-537e-589c-948b-5069d32c2cdd", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ -26 \\\\ 9\\end{bmatrix}"}, {":answer/id": "36dd0b11-b90c-55e8-b510-d4e353d2d733", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}22 \\\\ -26 \\\\ 9\\end{bmatrix}"}, {":answer/id": "49dba7b8-2ea0-52ad-b592-b51b44b10ab4", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ 9 \\\\ 26\\end{bmatrix}"}, {":answer/id": "f519fbbe-ed43-52c8-857e-fc4bbeddb4e5", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}-22 \\\\ 26 \\\\ 9\\end{bmatrix}"}, {":answer/id": "1c43e820-0897-5dfe-b6ba-5d73fbcaa258", ":answer/type": ":answer.type/math", ":answer/value": "\\begin{bmatrix}9 \\\\ 26 \\\\ -22\\end{bmatrix}"}], ":answer-field/correct": [":answer/id", "f519fbbe-ed43-52c8-857e-fc4bbeddb4e5"]}]
