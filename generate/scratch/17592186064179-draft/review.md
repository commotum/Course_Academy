# Side-by-side evidence review

Original MA anchors and changed-parameter raw recipes are labeled evidence only. Omitted original fields, keys, solutions and grades remain omitted. Normal variants use complete supported banks with documented repairs/authored fields. Four independent captured records are recorded separately in independent-inventory.json.

## q-2042 original raw anchor

What is $\displaystyle \int - 2\csc y\cot ydy$?

Difficulty: ABSENT; eligible: False; parameters: {'a': 2}.

- -2\csc y + C
- \csc y + C
- 2\csc^{2} y + C
- 2\cot y + C
- 2\csc y + C

[Original worked solution absent]

## q-2042 changed raw parameterized evidence

What is $\displaystyle \int - 11\csc y\cot ydy$?

Difficulty: ABSENT; eligible: False; parameters: {'a': 11}.

- -11\csc y + C
- \csc y + C
- 11\csc^{2} y + C
- 11\csc y + C
- 11\cot y + C

[Original worked solution absent]

## q-2044 original raw anchor

What is $\displaystyle \int - 3\sec θ\tan θdθ$?

Difficulty: ABSENT; eligible: False; parameters: {'a': 3}.

- -3\csc θ + C
- 3\sec θ + C
- -3\csc^{2} θ + C
- -3\sec θ + C
- -3\sec^{2} θ + C

[Original worked solution absent]

## q-2044 changed raw parameterized evidence

What is $\displaystyle \int - 11\sec θ\tan θdθ$?

Difficulty: ABSENT; eligible: False; parameters: {'a': 11}.

- -11\sec^{2} θ + C
- 11\sec θ + C
- -11\csc^{2} θ + C
- -11\sec θ + C
- -11\csc θ + C

[Original worked solution absent]

## q-113923 original raw anchor

$\int (3\operatorname{cos}x-2\operatorname{sec}x\,\operatorname{tan}x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: False; parameters: {'a': 3, 'b': 2}.

Recall that

$$
\begin{aligned}\int \operatorname{cos}x\,\text{d}x & =\operatorname{sin}x+C, \\ \int \operatorname{sec}x\operatorname{tan}x\,\text{d}x & =\operatorname{sec}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (3\operatorname{cos}x-2\operatorname{sec}x\,\operatorname{tan}x)\,\text{d}x & =3\int \operatorname{cos}x\,\text{d}x-2\int \operatorname{sec}x\operatorname{tan}x\,\text{d}x \\  & =3\operatorname{sin}x-2\operatorname{sec}x+C.\end{aligned}
$$

## q-113923 changed raw parameterized evidence

$\int (11\operatorname{cos}x-11\operatorname{sec}x\,\operatorname{tan}x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: False; parameters: {'a': 11, 'b': 11}.

Recall that

$$
\begin{aligned}\int \operatorname{cos}x\,\text{d}x & =\operatorname{sin}x+C, \\ \int \operatorname{sec}x\operatorname{tan}x\,\text{d}x & =\operatorname{sec}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (11\operatorname{cos}x-11\operatorname{sec}x\,\operatorname{tan}x)\,\text{d}x & =11\int \operatorname{cos}x\,\text{d}x-11\int \operatorname{sec}x\operatorname{tan}x\,\text{d}x \\  & =11\operatorname{sin}x-11\operatorname{sec}x+C.\end{aligned}
$$

## q-113925 original raw anchor

$\int (2\operatorname{csc}x\,\operatorname{cot}x+\operatorname{sin}x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: False; parameters: {'a': 2}.

Recall that

$$
\begin{aligned}\int \operatorname{sin}x\,\text{d}x & =-\operatorname{cos}x+C, \\ \int \operatorname{csc}x\operatorname{cot}x\,\text{d}x & =-\operatorname{csc}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (2\operatorname{csc}x\,\operatorname{cot}x+\operatorname{sin}x)\,\text{d}x & =2\int \operatorname{cos}\operatorname{csc}x\,\operatorname{cot}x\,\text{d}x+\int \operatorname{sin}x\,\text{d}x \\  & =2(-\operatorname{csc}x)+(-\operatorname{cos}x)+C \\  & =-2\operatorname{csc}x-\operatorname{cos}x+C.\end{aligned}
$$

## q-113925 changed raw parameterized evidence

$\int (11\operatorname{csc}x\,\operatorname{cot}x+\operatorname{sin}x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: False; parameters: {'a': 11}.

Recall that

$$
\begin{aligned}\int \operatorname{sin}x\,\text{d}x & =-\operatorname{cos}x+C, \\ \int \operatorname{csc}x\operatorname{cot}x\,\text{d}x & =-\operatorname{csc}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (11\operatorname{csc}x\,\operatorname{cot}x+\operatorname{sin}x)\,\text{d}x & =11\int \operatorname{cos}\operatorname{csc}x\,\operatorname{cot}x\,\text{d}x+\int \operatorname{sin}x\,\text{d}x \\  & =11(-\operatorname{csc}x)+(-\operatorname{cos}x)+C \\  & =-11\operatorname{csc}x-\operatorname{cos}x+C.\end{aligned}
$$

## q-71657 original raw anchor

$\int (-8\operatorname{csc}y\,\operatorname{cot}y)\,\text{d}y=$

Difficulty: :question.difficulty/easy; eligible: False; parameters: {'a': 8}.

Recall that

$$
\begin{aligned}\int \operatorname{csc}y\operatorname{cot}y\,\text{d}y & =-\operatorname{csc}y+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (-8\operatorname{csc}y\,\operatorname{cot}y)\,\text{d}y & =-8\int \operatorname{csc}y\operatorname{cot}y\,\text{d}y \\  & =-8(-\operatorname{csc}y)+C \\  & =8\operatorname{csc}y+C.\end{aligned}
$$

## q-71657 changed raw parameterized evidence

$\int (-11\operatorname{csc}y\,\operatorname{cot}y)\,\text{d}y=$

Difficulty: :question.difficulty/easy; eligible: False; parameters: {'a': 11}.

Recall that

$$
\begin{aligned}\int \operatorname{csc}y\operatorname{cot}y\,\text{d}y & =-\operatorname{csc}y+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (-11\operatorname{csc}y\,\operatorname{cot}y)\,\text{d}y & =-11\int \operatorname{csc}y\operatorname{cot}y\,\text{d}y \\  & =-11(-\operatorname{csc}y)+C \\  & =11\operatorname{csc}y+C.\end{aligned}
$$

## q-113920 original raw anchor

$\int -3csc⁡x\,cot⁡x\,\text{d}x=$

Difficulty: :question.difficulty/easy; eligible: False; parameters: {'a': 3}.

- 3sec⁡x+C
- -3csc⁡x+C
- -3sec⁡x+C
* 3csc⁡x+C
- 3sec⁡xcot⁡x+C

Recall that

$$
\int csc⁡xcot⁡x\,\text{d}x=-csc⁡x+C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int -3csc⁡x\,cot⁡x\,\text{d}x & =-3\int csc⁡xcot⁡x\,\text{d}x \\  & =-3(-csc⁡x)+C \\  & =3csc⁡x+C.\end{aligned}\end{aligned}
$$

## q-113920 changed raw parameterized evidence

$\int -11csc⁡x\,cot⁡x\,\text{d}x=$

Difficulty: :question.difficulty/easy; eligible: False; parameters: {'a': 11}.

- -11sec⁡x+C
- 11sec⁡xcot⁡x+C
- 11sec⁡x+C
- -11csc⁡x+C
* 11csc⁡x+C

Recall that

$$
\int csc⁡xcot⁡x\,\text{d}x=-csc⁡x+C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int -11csc⁡x\,cot⁡x\,\text{d}x & =-11\int csc⁡xcot⁡x\,\text{d}x \\  & =-11(-csc⁡x)+C \\  & =11csc⁡x+C.\end{aligned}\end{aligned}
$$

## q-113926 original raw anchor

$\int (4sin⁡x-3csc⁡x\,cot⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: False; parameters: {'a': 4, 'b': 3}.

- -4cos⁡x-3csc⁡x+C
- 4cos⁡x+3sec⁡x+C
* -4cos⁡x+3csc⁡x+C
- -4cos⁡x-3cot⁡x+C
- 4cos⁡x+3{csc}^{2}⁡x+C

Recall that

$$
\begin{aligned}\int sin⁡x\,\text{d}x & =-cos⁡x+C, \\ \int csc⁡xcot⁡x\,\text{d}x & =-csc⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (4sin⁡x-3csc⁡x\,cot⁡x)\,\text{d}x & =4\int sin⁡x\,\text{d}x-3\int csc⁡x\,cot⁡x\,\text{d}x \\  & =4(-cos⁡x)-3(-csc⁡x)+C \\  & =-4cos⁡x+3csc⁡x+C.\end{aligned}
$$

## q-113926 changed raw parameterized evidence

$\int (11sin⁡x-11csc⁡x\,cot⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: False; parameters: {'a': 11, 'b': 11}.

- 11cos⁡x+11{csc}^{2}⁡x+C
- -11cos⁡x-11cot⁡x+C
- -11cos⁡x-11csc⁡x+C
* -11cos⁡x+11csc⁡x+C
- 11cos⁡x+11sec⁡x+C

Recall that

$$
\begin{aligned}\int sin⁡x\,\text{d}x & =-cos⁡x+C, \\ \int csc⁡xcot⁡x\,\text{d}x & =-csc⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (11sin⁡x-11csc⁡x\,cot⁡x)\,\text{d}x & =11\int sin⁡x\,\text{d}x-11\int csc⁡x\,cot⁡x\,\text{d}x \\  & =11(-cos⁡x)-11(-csc⁡x)+C \\  & =-11cos⁡x+11csc⁡x+C.\end{aligned}
$$

## q-113928 original raw anchor

$\int (\operatorname{sec}⁡x\operatorname{tan}⁡x-5\operatorname{cos}⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: False; parameters: {'b': 5}.

- -\operatorname{sec}⁡x+5\operatorname{sin}⁡x+C
- \operatorname{tan}⁡x-5\operatorname{sin}⁡x+C
- -\operatorname{sec}⁡x-5\operatorname{sin}⁡x+C
* \operatorname{sec}⁡x-5\operatorname{sin}⁡x+C
- {tan}^{2}⁡x+5\operatorname{sin}⁡x+C

Recall that

$$
\begin{aligned}\int \operatorname{cos}⁡x\,\text{d}x & =\operatorname{sin}⁡x+C, \\ \int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x & =\operatorname{sec}⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (\operatorname{sec}⁡x\operatorname{tan}⁡x-5\operatorname{cos}⁡x)\,\text{d}x & =\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x-5\int \operatorname{cos}⁡x\,\text{d}x \\  & =\operatorname{sec}⁡x-5\operatorname{sin}⁡x+C\end{aligned}
$$

## q-113928 changed raw parameterized evidence

$\int (\operatorname{sec}⁡x\operatorname{tan}⁡x-11\operatorname{cos}⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: False; parameters: {'b': 11}.

- {tan}^{2}⁡x+11\operatorname{sin}⁡x+C
- -\operatorname{sec}⁡x+11\operatorname{sin}⁡x+C
* \operatorname{sec}⁡x-11\operatorname{sin}⁡x+C
- \operatorname{tan}⁡x-11\operatorname{sin}⁡x+C
- -\operatorname{sec}⁡x-11\operatorname{sin}⁡x+C

Recall that

$$
\begin{aligned}\int \operatorname{cos}⁡x\,\text{d}x & =\operatorname{sin}⁡x+C, \\ \int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x & =\operatorname{sec}⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (\operatorname{sec}⁡x\operatorname{tan}⁡x-11\operatorname{cos}⁡x)\,\text{d}x & =\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x-11\int \operatorname{cos}⁡x\,\text{d}x \\  & =\operatorname{sec}⁡x-11\operatorname{sin}⁡x+C\end{aligned}
$$

## q-113930 original raw anchor

$\int (3\operatorname{sec}⁡x\operatorname{tan}⁡x+7\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: False; parameters: {'a': 3, 'b': 7}.

- -3\operatorname{tan}⁡x+7\operatorname{cot}⁡x+C
* 3\operatorname{sec}⁡x-7\operatorname{csc}⁡x+C
- 10{sec}^{2}⁡x+C
- -3\operatorname{sec}⁡x-7\operatorname{cot}⁡x+C
- 3\operatorname{sec}⁡x+7\operatorname{csc}⁡x+C

Recall that

$$
\begin{aligned}\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x & =\operatorname{sec}⁡x+C, \\ \int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x & =-\operatorname{csc}⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (3\operatorname{sec}⁡x\operatorname{tan}⁡x+7\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x & =3\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x+7\int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & =3\operatorname{sec}⁡x+7(-\operatorname{csc}⁡x)+C \\  & =3\operatorname{sec}⁡x-7\operatorname{csc}⁡x+C.\end{aligned}
$$

## q-113930 changed raw parameterized evidence

$\int (11\operatorname{sec}⁡x\operatorname{tan}⁡x+11\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: False; parameters: {'a': 11, 'b': 11}.

* 11\operatorname{sec}⁡x-11\operatorname{csc}⁡x+C
- 11\operatorname{sec}⁡x+11\operatorname{csc}⁡x+C
- -11\operatorname{sec}⁡x-11\operatorname{cot}⁡x+C
- -11\operatorname{tan}⁡x+11\operatorname{cot}⁡x+C
- 22{sec}^{2}⁡x+C

Recall that

$$
\begin{aligned}\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x & =\operatorname{sec}⁡x+C, \\ \int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x & =-\operatorname{csc}⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (11\operatorname{sec}⁡x\operatorname{tan}⁡x+11\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x & =11\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x+11\int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & =11\operatorname{sec}⁡x+11(-\operatorname{csc}⁡x)+C \\  & =11\operatorname{sec}⁡x-11\operatorname{csc}⁡x+C.\end{aligned}
$$

## q-2038 original raw anchor

$\int (-sec⁡\theta tan⁡\theta )\text{d}\theta =$

Difficulty: :question.difficulty/easy; eligible: False; parameters: {'a': 1}.

* -sec⁡\theta +C
- csc⁡\theta +C
- sec⁡\theta +C
- csc⁡xcot⁡x+C
- -csc⁡\theta +C

Recall that

$$
\int sec⁡\theta tan⁡\theta \,\text{d}\theta =sec⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int (-sec⁡\theta tan⁡\theta )\text{d}\theta  & =-\int sec⁡\theta tan⁡\theta \,\text{d}\theta  \\  & =-(sec⁡\theta )+C \\  & =-sec⁡\theta +C.\end{aligned}\end{aligned}
$$

## q-2038 changed raw parameterized evidence

$\int (-11sec⁡\theta tan⁡\theta )\text{d}\theta =$

Difficulty: :question.difficulty/easy; eligible: False; parameters: {'a': 11}.

* -11sec⁡\theta +C
- 11sec⁡\theta +C
- 11csc⁡\theta +C
- 11csc⁡xcot⁡x+C
- -11csc⁡\theta +C

Recall that

$$
\int sec⁡\theta tan⁡\theta \,\text{d}\theta =sec⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int (-11sec⁡\theta tan⁡\theta )\text{d}\theta  & =-11\int sec⁡\theta tan⁡\theta \,\text{d}\theta  \\  & =-11(sec⁡\theta )+C \\  & =-11sec⁡\theta +C.\end{aligned}\end{aligned}
$$

## q-71656 original raw anchor

$\int 5sec⁡\theta tan⁡\theta \,\text{d}\theta =$

Difficulty: :question.difficulty/easy; eligible: False; parameters: {'a': 5}.

- -5sec⁡\theta +C
- -5csc⁡\theta +C
- 5csc⁡\theta +C
- 5csc⁡\theta cot⁡\theta +C
* 5sec⁡\theta +C

Recall that

$$
\int sec⁡\theta tan⁡\theta \,\text{d}\theta =sec⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int 5sec⁡\theta tan⁡\theta \,\text{d}\theta  & =5\int sec⁡\theta tan⁡\theta \,\text{d}\theta  \\  & =5sec⁡\theta +C.\end{aligned}\end{aligned}
$$

## q-71656 changed raw parameterized evidence

$\int 11sec⁡\theta tan⁡\theta \,\text{d}\theta =$

Difficulty: :question.difficulty/easy; eligible: False; parameters: {'a': 11}.

- 11csc⁡\theta +C
- -11csc⁡\theta +C
* 11sec⁡\theta +C
- 11csc⁡\theta cot⁡\theta +C
- -11sec⁡\theta +C

Recall that

$$
\int sec⁡\theta tan⁡\theta \,\text{d}\theta =sec⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int 11sec⁡\theta tan⁡\theta \,\text{d}\theta  & =11\int sec⁡\theta tan⁡\theta \,\text{d}\theta  \\  & =11sec⁡\theta +C.\end{aligned}\end{aligned}
$$

## q-71659 original raw anchor

$\int (-4sec⁡\theta tan⁡\theta )\,\text{d}\theta =$

Difficulty: :question.difficulty/easy; eligible: False; parameters: {'a': 4}.

- -4csc⁡\theta +C
- 4sec⁡\theta +C
- {csc}^{4}⁡\theta +C
- {sec}^{4}⁡\theta +C
* -4sec⁡\theta +C

Recall that

$$
\int sec⁡\theta tan⁡\theta \,\text{d}\theta =sec⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int (-4sec⁡\theta tan⁡\theta )\,\text{d}\theta  & =-4\int sec⁡\theta tan⁡\theta \,\text{d}\theta  \\  & =-4sec⁡\theta +C.\end{aligned}\end{aligned}
$$

## q-71659 changed raw parameterized evidence

$\int (-11sec⁡\theta tan⁡\theta )\,\text{d}\theta =$

Difficulty: :question.difficulty/easy; eligible: False; parameters: {'a': 11}.

- 11sec⁡\theta +C
- -11csc⁡\theta +C
- {sec}^{11}⁡\theta +C
- {csc}^{11}⁡\theta +C
* -11sec⁡\theta +C

Recall that

$$
\int sec⁡\theta tan⁡\theta \,\text{d}\theta =sec⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int (-11sec⁡\theta tan⁡\theta )\,\text{d}\theta  & =-11\int sec⁡\theta tan⁡\theta \,\text{d}\theta  \\  & =-11sec⁡\theta +C.\end{aligned}\end{aligned}
$$

## easy q-113920 normal generated variant 1

$\int -4csc⁡x\,cot⁡x\,\text{d}x=$

Difficulty: :question.difficulty/easy; eligible: True; parameters: {'a': 4}.

- 4csc⁡xcot⁡x+C
- -4sec⁡x+C
- -4csc⁡x+C
- 4sec⁡x+C
* 4csc⁡x+C

Recall that

$$
\int csc⁡xcot⁡x\,\text{d}x=-csc⁡x+C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int -4csc⁡x\,cot⁡x\,\text{d}x & =-4\int csc⁡xcot⁡x\,\text{d}x \\  & =-4(-csc⁡x)+C \\  & =4csc⁡x+C.\end{aligned}\end{aligned}
$$

## easy q-113920 normal generated variant 2

$\int -9csc⁡x\,cot⁡x\,\text{d}x=$

Difficulty: :question.difficulty/easy; eligible: True; parameters: {'a': 9}.

- -9sec⁡x+C
- 9csc⁡xcot⁡x+C
- -9csc⁡x+C
- 9sec⁡x+C
* 9csc⁡x+C

Recall that

$$
\int csc⁡xcot⁡x\,\text{d}x=-csc⁡x+C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int -9csc⁡x\,cot⁡x\,\text{d}x & =-9\int csc⁡xcot⁡x\,\text{d}x \\  & =-9(-csc⁡x)+C \\  & =9csc⁡x+C.\end{aligned}\end{aligned}
$$

## easy q-71656 normal generated variant 1

$\int 4sec⁡\theta tan⁡\theta \,\text{d}\theta =$

Difficulty: :question.difficulty/easy; eligible: True; parameters: {'a': 4}.

- -4sec⁡\theta +C
* 4sec⁡\theta +C
- 4csc⁡\theta cot⁡\theta +C
- -4csc⁡\theta +C
- 4csc⁡\theta +C

Recall that

$$
\int sec⁡\theta tan⁡\theta \,\text{d}\theta =sec⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int 4sec⁡\theta tan⁡\theta \,\text{d}\theta  & =4\int sec⁡\theta tan⁡\theta \,\text{d}\theta  \\  & =4sec⁡\theta +C.\end{aligned}\end{aligned}
$$

## easy q-71656 normal generated variant 2

$\int 9sec⁡\theta tan⁡\theta \,\text{d}\theta =$

Difficulty: :question.difficulty/easy; eligible: True; parameters: {'a': 9}.

- 9csc⁡\theta cot⁡\theta +C
- -9sec⁡\theta +C
* 9sec⁡\theta +C
- 9csc⁡\theta +C
- -9csc⁡\theta +C

Recall that

$$
\int sec⁡\theta tan⁡\theta \,\text{d}\theta =sec⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int 9sec⁡\theta tan⁡\theta \,\text{d}\theta  & =9\int sec⁡\theta tan⁡\theta \,\text{d}\theta  \\  & =9sec⁡\theta +C.\end{aligned}\end{aligned}
$$

## easy q-71659 normal generated variant 1

$\int (-4sec⁡\theta tan⁡\theta )\,\text{d}\theta =$

Difficulty: :question.difficulty/easy; eligible: True; parameters: {'a': 4}.

- -4csc⁡\theta +C
- 4sec⁡\theta +C
- {csc}^{4}⁡\theta +C
- {sec}^{4}⁡\theta +C
* -4sec⁡\theta +C

Recall that

$$
\int sec⁡\theta tan⁡\theta \,\text{d}\theta =sec⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int (-4sec⁡\theta tan⁡\theta )\,\text{d}\theta  & =-4\int sec⁡\theta tan⁡\theta \,\text{d}\theta  \\  & =-4sec⁡\theta +C.\end{aligned}\end{aligned}
$$

## easy q-71659 normal generated variant 2

$\int (-9sec⁡\theta tan⁡\theta )\,\text{d}\theta =$

Difficulty: :question.difficulty/easy; eligible: True; parameters: {'a': 9}.

- {csc}^{9}⁡\theta +C
- {sec}^{9}⁡\theta +C
- 9sec⁡\theta +C
- -9csc⁡\theta +C
* -9sec⁡\theta +C

Recall that

$$
\int sec⁡\theta tan⁡\theta \,\text{d}\theta =sec⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int (-9sec⁡\theta tan⁡\theta )\,\text{d}\theta  & =-9\int sec⁡\theta tan⁡\theta \,\text{d}\theta  \\  & =-9sec⁡\theta +C.\end{aligned}\end{aligned}
$$

## easy q-71657 normal generated variant 1

$\int (-4\operatorname{csc}y\,\operatorname{cot}y)\,\text{d}y=$

Difficulty: :question.difficulty/easy; eligible: True; parameters: {'a': 4}.

- - 4 \sec{\left(y \right)}+C
* 4 \csc{\left(y \right)}+C
- - 4 \csc{\left(y \right)}+C
- - 4 \cot{\left(y \right)} \csc{\left(y \right)}+C
- 4 \sec{\left(y \right)}+C

Recall that

$$
\begin{aligned}\int \operatorname{csc}y\operatorname{cot}y\,\text{d}y & =-\operatorname{csc}y+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (-4\operatorname{csc}y\,\operatorname{cot}y)\,\text{d}y & =-4\int \operatorname{csc}y\operatorname{cot}y\,\text{d}y \\  & =-4(-\operatorname{csc}y)+C \\  & =4\operatorname{csc}y+C.\end{aligned}
$$

## easy q-71657 normal generated variant 2

$\int (-9\operatorname{csc}y\,\operatorname{cot}y)\,\text{d}y=$

Difficulty: :question.difficulty/easy; eligible: True; parameters: {'a': 9}.

* 9 \csc{\left(y \right)}+C
- - 9 \sec{\left(y \right)}+C
- 9 \sec{\left(y \right)}+C
- - 9 \cot{\left(y \right)} \csc{\left(y \right)}+C
- - 9 \csc{\left(y \right)}+C

Recall that

$$
\begin{aligned}\int \operatorname{csc}y\operatorname{cot}y\,\text{d}y & =-\operatorname{csc}y+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (-9\operatorname{csc}y\,\operatorname{cot}y)\,\text{d}y & =-9\int \operatorname{csc}y\operatorname{cot}y\,\text{d}y \\  & =-9(-\operatorname{csc}y)+C \\  & =9\operatorname{csc}y+C.\end{aligned}
$$

## moderate q-113926 normal generated variant 1

$\int (4sin⁡x-4csc⁡x\,cot⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: True; parameters: {'a': 4, 'b': 4}.

- -4cos⁡x-4csc⁡x+C
- -4cos⁡x-4cot⁡x+C
* -4cos⁡x+4csc⁡x+C
- 4cos⁡x+4{csc}^{2}⁡x+C
- 4cos⁡x+4sec⁡x+C

Recall that

$$
\begin{aligned}\int sin⁡x\,\text{d}x & =-cos⁡x+C, \\ \int csc⁡xcot⁡x\,\text{d}x & =-csc⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (4sin⁡x-4csc⁡x\,cot⁡x)\,\text{d}x & =4\int sin⁡x\,\text{d}x-4\int csc⁡x\,cot⁡x\,\text{d}x \\  & =4(-cos⁡x)-4(-csc⁡x)+C \\  & =-4cos⁡x+4csc⁡x+C.\end{aligned}
$$

## moderate q-113926 normal generated variant 2

$\int (9sin⁡x-9csc⁡x\,cot⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: True; parameters: {'a': 9, 'b': 9}.

- -9cos⁡x-9cot⁡x+C
* -9cos⁡x+9csc⁡x+C
- 9cos⁡x+9{csc}^{2}⁡x+C
- -9cos⁡x-9csc⁡x+C
- 9cos⁡x+9sec⁡x+C

Recall that

$$
\begin{aligned}\int sin⁡x\,\text{d}x & =-cos⁡x+C, \\ \int csc⁡xcot⁡x\,\text{d}x & =-csc⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (9sin⁡x-9csc⁡x\,cot⁡x)\,\text{d}x & =9\int sin⁡x\,\text{d}x-9\int csc⁡x\,cot⁡x\,\text{d}x \\  & =9(-cos⁡x)-9(-csc⁡x)+C \\  & =-9cos⁡x+9csc⁡x+C.\end{aligned}
$$

## moderate q-113928 normal generated variant 1

$\int (\operatorname{sec}⁡x\operatorname{tan}⁡x-4\operatorname{cos}⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: True; parameters: {'b': 4}.

* \operatorname{sec}⁡x-4\operatorname{sin}⁡x+C
- -\operatorname{sec}⁡x+4\operatorname{sin}⁡x+C
- {tan}^{2}⁡x+4\operatorname{sin}⁡x+C
- \operatorname{tan}⁡x-4\operatorname{sin}⁡x+C
- -\operatorname{sec}⁡x-4\operatorname{sin}⁡x+C

Recall that

$$
\begin{aligned}\int \operatorname{cos}⁡x\,\text{d}x & =\operatorname{sin}⁡x+C, \\ \int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x & =\operatorname{sec}⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (\operatorname{sec}⁡x\operatorname{tan}⁡x-4\operatorname{cos}⁡x)\,\text{d}x & =\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x-4\int \operatorname{cos}⁡x\,\text{d}x \\  & =\operatorname{sec}⁡x-4\operatorname{sin}⁡x+C\end{aligned}
$$

## moderate q-113928 normal generated variant 2

$\int (\operatorname{sec}⁡x\operatorname{tan}⁡x-9\operatorname{cos}⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: True; parameters: {'b': 9}.

* \operatorname{sec}⁡x-9\operatorname{sin}⁡x+C
- {tan}^{2}⁡x+9\operatorname{sin}⁡x+C
- -\operatorname{sec}⁡x-9\operatorname{sin}⁡x+C
- \operatorname{tan}⁡x-9\operatorname{sin}⁡x+C
- -\operatorname{sec}⁡x+9\operatorname{sin}⁡x+C

Recall that

$$
\begin{aligned}\int \operatorname{cos}⁡x\,\text{d}x & =\operatorname{sin}⁡x+C, \\ \int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x & =\operatorname{sec}⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (\operatorname{sec}⁡x\operatorname{tan}⁡x-9\operatorname{cos}⁡x)\,\text{d}x & =\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x-9\int \operatorname{cos}⁡x\,\text{d}x \\  & =\operatorname{sec}⁡x-9\operatorname{sin}⁡x+C\end{aligned}
$$

## moderate q-113930 normal generated variant 1

$\int (4\operatorname{sec}⁡x\operatorname{tan}⁡x+4\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: True; parameters: {'a': 4, 'b': 4}.

- 4\operatorname{sec}⁡x+4\operatorname{csc}⁡x+C
- 8{sec}^{2}⁡x+C
- -4\operatorname{tan}⁡x+4\operatorname{cot}⁡x+C
* 4\operatorname{sec}⁡x-4\operatorname{csc}⁡x+C
- -4\operatorname{sec}⁡x-4\operatorname{cot}⁡x+C

Recall that

$$
\begin{aligned}\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x & =\operatorname{sec}⁡x+C, \\ \int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x & =-\operatorname{csc}⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (4\operatorname{sec}⁡x\operatorname{tan}⁡x+4\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x & =4\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x+4\int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & =4\operatorname{sec}⁡x+4(-\operatorname{csc}⁡x)+C \\  & =4\operatorname{sec}⁡x-4\operatorname{csc}⁡x+C.\end{aligned}
$$

## moderate q-113930 normal generated variant 2

$\int (9\operatorname{sec}⁡x\operatorname{tan}⁡x+9\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: True; parameters: {'a': 9, 'b': 9}.

* 9\operatorname{sec}⁡x-9\operatorname{csc}⁡x+C
- -9\operatorname{sec}⁡x-9\operatorname{cot}⁡x+C
- 18{sec}^{2}⁡x+C
- -9\operatorname{tan}⁡x+9\operatorname{cot}⁡x+C
- 9\operatorname{sec}⁡x+9\operatorname{csc}⁡x+C

Recall that

$$
\begin{aligned}\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x & =\operatorname{sec}⁡x+C, \\ \int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x & =-\operatorname{csc}⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (9\operatorname{sec}⁡x\operatorname{tan}⁡x+9\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x & =9\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x+9\int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & =9\operatorname{sec}⁡x+9(-\operatorname{csc}⁡x)+C \\  & =9\operatorname{sec}⁡x-9\operatorname{csc}⁡x+C.\end{aligned}
$$

## moderate q-113923 normal generated variant 1

$\int (4\operatorname{cos}x-4\operatorname{sec}x\,\operatorname{tan}x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: True; parameters: {'a': 4, 'b': 4}.

* 4 \sin{\left(x \right)} - 4 \sec{\left(x \right)}+C
- - 4 \sin{\left(x \right)} - 4 \sec{\left(x \right)}+C
- 4 \sin{\left(x \right)} + 4 \sec{\left(x \right)}+C
- - 4 \sin{\left(x \right)} + 4 \sec{\left(x \right)}+C
- 4 \cos{\left(x \right)} - 4 \tan{\left(x \right)} \sec{\left(x \right)}+C

Recall that

$$
\begin{aligned}\int \operatorname{cos}x\,\text{d}x & =\operatorname{sin}x+C, \\ \int \operatorname{sec}x\operatorname{tan}x\,\text{d}x & =\operatorname{sec}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (4\operatorname{cos}x-4\operatorname{sec}x\,\operatorname{tan}x)\,\text{d}x & =4\int \operatorname{cos}x\,\text{d}x-4\int \operatorname{sec}x\operatorname{tan}x\,\text{d}x \\  & =4\operatorname{sin}x-4\operatorname{sec}x+C.\end{aligned}
$$

## moderate q-113923 normal generated variant 2

$\int (9\operatorname{cos}x-9\operatorname{sec}x\,\operatorname{tan}x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: True; parameters: {'a': 9, 'b': 9}.

- 9 \cos{\left(x \right)} - 9 \tan{\left(x \right)} \sec{\left(x \right)}+C
* 9 \sin{\left(x \right)} - 9 \sec{\left(x \right)}+C
- 9 \sin{\left(x \right)} + 9 \sec{\left(x \right)}+C
- - 9 \sin{\left(x \right)} + 9 \sec{\left(x \right)}+C
- - 9 \sin{\left(x \right)} - 9 \sec{\left(x \right)}+C

Recall that

$$
\begin{aligned}\int \operatorname{cos}x\,\text{d}x & =\operatorname{sin}x+C, \\ \int \operatorname{sec}x\operatorname{tan}x\,\text{d}x & =\operatorname{sec}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (9\operatorname{cos}x-9\operatorname{sec}x\,\operatorname{tan}x)\,\text{d}x & =9\int \operatorname{cos}x\,\text{d}x-9\int \operatorname{sec}x\operatorname{tan}x\,\text{d}x \\  & =9\operatorname{sin}x-9\operatorname{sec}x+C.\end{aligned}
$$

## moderate q-113925 normal generated variant 1

$\int (4\operatorname{csc}x\,\operatorname{cot}x+\operatorname{sin}x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: True; parameters: {'a': 4}.

- \cos{\left(x \right)} + 4 \csc{\left(x \right)}+C
- \sin{\left(x \right)} + 4 \cot{\left(x \right)} \csc{\left(x \right)}+C
- \cos{\left(x \right)} - 4 \csc{\left(x \right)}+C
* - \cos{\left(x \right)} - 4 \csc{\left(x \right)}+C
- - \cos{\left(x \right)} + 4 \csc{\left(x \right)}+C

Recall that

$$
\begin{aligned}\int \operatorname{sin}x\,\text{d}x & =-\operatorname{cos}x+C, \\ \int \operatorname{csc}x\operatorname{cot}x\,\text{d}x & =-\operatorname{csc}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (4\operatorname{csc}x\,\operatorname{cot}x+\operatorname{sin}x)\,\text{d}x & =4\int \operatorname{csc}x\,\operatorname{cot}x\,\text{d}x+\int \operatorname{sin}x\,\text{d}x \\  & =4(-\operatorname{csc}x)+(-\operatorname{cos}x)+C \\  & =-4\operatorname{csc}x-\operatorname{cos}x+C.\end{aligned}
$$

## moderate q-113925 normal generated variant 2

$\int (9\operatorname{csc}x\,\operatorname{cot}x+\operatorname{sin}x)\,\text{d}x=$

Difficulty: :question.difficulty/moderate; eligible: True; parameters: {'a': 9}.

- \sin{\left(x \right)} + 9 \cot{\left(x \right)} \csc{\left(x \right)}+C
- \cos{\left(x \right)} + 9 \csc{\left(x \right)}+C
* - \cos{\left(x \right)} - 9 \csc{\left(x \right)}+C
- \cos{\left(x \right)} - 9 \csc{\left(x \right)}+C
- - \cos{\left(x \right)} + 9 \csc{\left(x \right)}+C

Recall that

$$
\begin{aligned}\int \operatorname{sin}x\,\text{d}x & =-\operatorname{cos}x+C, \\ \int \operatorname{csc}x\operatorname{cot}x\,\text{d}x & =-\operatorname{csc}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (9\operatorname{csc}x\,\operatorname{cot}x+\operatorname{sin}x)\,\text{d}x & =9\int \operatorname{csc}x\,\operatorname{cot}x\,\text{d}x+\int \operatorname{sin}x\,\text{d}x \\  & =9(-\operatorname{csc}x)+(-\operatorname{cos}x)+C \\  & =-9\operatorname{csc}x-\operatorname{cos}x+C.\end{aligned}
$$

## hard q-113926 normal generated variant 1 (authored hard)

$\int (\frac{3}{2}sin⁡x-\frac{5}{2}csc⁡x\,cot⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/hard; eligible: True; parameters: {'a': '3/2', 'b': '5/2'}.

- -\frac{3}{2}cos⁡x-\frac{5}{2}cot⁡x+C
- -\frac{3}{2}cos⁡x-\frac{5}{2}csc⁡x+C
* -\frac{3}{2}cos⁡x+\frac{5}{2}csc⁡x+C
- \frac{3}{2}cos⁡x+\frac{5}{2}{csc}^{2}⁡x+C
- \frac{3}{2}cos⁡x+\frac{5}{2}sec⁡x+C

Recall that

$$
\begin{aligned}\int sin⁡x\,\text{d}x & =-cos⁡x+C, \\ \int csc⁡xcot⁡x\,\text{d}x & =-csc⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (\frac{3}{2}sin⁡x-\frac{5}{2}csc⁡x\,cot⁡x)\,\text{d}x & =\frac{3}{2}\int sin⁡x\,\text{d}x-\frac{5}{2}\int csc⁡x\,cot⁡x\,\text{d}x \\  & =\frac{3}{2}(-cos⁡x)-\frac{5}{2}(-csc⁡x)+C \\  & =-\frac{3}{2}cos⁡x+\frac{5}{2}csc⁡x+C.\end{aligned}
$$

## hard q-113926 normal generated variant 2 (authored hard)

$\int (\frac{17}{2}sin⁡x-\frac{4}{3}csc⁡x\,cot⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/hard; eligible: True; parameters: {'a': '17/2', 'b': '4/3'}.

* -\frac{17}{2}cos⁡x+\frac{4}{3}csc⁡x+C
- -\frac{17}{2}cos⁡x-\frac{4}{3}csc⁡x+C
- \frac{17}{2}cos⁡x+\frac{4}{3}{csc}^{2}⁡x+C
- -\frac{17}{2}cos⁡x-\frac{4}{3}cot⁡x+C
- \frac{17}{2}cos⁡x+\frac{4}{3}sec⁡x+C

Recall that

$$
\begin{aligned}\int sin⁡x\,\text{d}x & =-cos⁡x+C, \\ \int csc⁡xcot⁡x\,\text{d}x & =-csc⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (\frac{17}{2}sin⁡x-\frac{4}{3}csc⁡x\,cot⁡x)\,\text{d}x & =\frac{17}{2}\int sin⁡x\,\text{d}x-\frac{4}{3}\int csc⁡x\,cot⁡x\,\text{d}x \\  & =\frac{17}{2}(-cos⁡x)-\frac{4}{3}(-csc⁡x)+C \\  & =-\frac{17}{2}cos⁡x+\frac{4}{3}csc⁡x+C.\end{aligned}
$$

## hard q-113930 normal generated variant 1 (authored hard)

$\int (\frac{3}{2}\operatorname{sec}⁡x\operatorname{tan}⁡x+\frac{5}{2}\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/hard; eligible: True; parameters: {'a': '3/2', 'b': '5/2'}.

- 4{sec}^{2}⁡x+C
- -\frac{3}{2}\operatorname{sec}⁡x-\frac{5}{2}\operatorname{cot}⁡x+C
* \frac{3}{2}\operatorname{sec}⁡x-\frac{5}{2}\operatorname{csc}⁡x+C
- -\frac{3}{2}\operatorname{tan}⁡x+\frac{5}{2}\operatorname{cot}⁡x+C
- \frac{3}{2}\operatorname{sec}⁡x+\frac{5}{2}\operatorname{csc}⁡x+C

Recall that

$$
\begin{aligned}\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x & =\operatorname{sec}⁡x+C, \\ \int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x & =-\operatorname{csc}⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (\frac{3}{2}\operatorname{sec}⁡x\operatorname{tan}⁡x+\frac{5}{2}\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x & =\frac{3}{2}\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x+\frac{5}{2}\int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & =\frac{3}{2}\operatorname{sec}⁡x+\frac{5}{2}(-\operatorname{csc}⁡x)+C \\  & =\frac{3}{2}\operatorname{sec}⁡x-\frac{5}{2}\operatorname{csc}⁡x+C.\end{aligned}
$$

## hard q-113930 normal generated variant 2 (authored hard)

$\int (\frac{17}{2}\operatorname{sec}⁡x\operatorname{tan}⁡x+\frac{4}{3}\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x=$

Difficulty: :question.difficulty/hard; eligible: True; parameters: {'a': '17/2', 'b': '4/3'}.

- -\frac{17}{2}\operatorname{tan}⁡x+\frac{4}{3}\operatorname{cot}⁡x+C
- \frac{17}{2}\operatorname{sec}⁡x+\frac{4}{3}\operatorname{csc}⁡x+C
- -\frac{17}{2}\operatorname{sec}⁡x-\frac{4}{3}\operatorname{cot}⁡x+C
- \frac{59}{6}{sec}^{2}⁡x+C
* \frac{17}{2}\operatorname{sec}⁡x-\frac{4}{3}\operatorname{csc}⁡x+C

Recall that

$$
\begin{aligned}\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x & =\operatorname{sec}⁡x+C, \\ \int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x & =-\operatorname{csc}⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (\frac{17}{2}\operatorname{sec}⁡x\operatorname{tan}⁡x+\frac{4}{3}\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x & =\frac{17}{2}\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x+\frac{4}{3}\int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & =\frac{17}{2}\operatorname{sec}⁡x+\frac{4}{3}(-\operatorname{csc}⁡x)+C \\  & =\frac{17}{2}\operatorname{sec}⁡x-\frac{4}{3}\operatorname{csc}⁡x+C.\end{aligned}
$$

## hard q-113923 normal generated variant 1 (authored hard)

$\int (\frac{3}{2}\operatorname{cos}x-\frac{5}{2}\operatorname{sec}x\,\operatorname{tan}x)\,\text{d}x=$

Difficulty: :question.difficulty/hard; eligible: True; parameters: {'a': '3/2', 'b': '5/2'}.

- \frac{3 \cos{\left(x \right)}}{2} - \frac{5 \tan{\left(x \right)} \sec{\left(x \right)}}{2}+C
- - \frac{3 \sin{\left(x \right)}}{2} - \frac{5 \sec{\left(x \right)}}{2}+C
- - \frac{3 \sin{\left(x \right)}}{2} + \frac{5 \sec{\left(x \right)}}{2}+C
* \frac{3 \sin{\left(x \right)}}{2} - \frac{5 \sec{\left(x \right)}}{2}+C
- \frac{3 \sin{\left(x \right)}}{2} + \frac{5 \sec{\left(x \right)}}{2}+C

Recall that

$$
\begin{aligned}\int \operatorname{cos}x\,\text{d}x & =\operatorname{sin}x+C, \\ \int \operatorname{sec}x\operatorname{tan}x\,\text{d}x & =\operatorname{sec}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (\frac{3}{2}\operatorname{cos}x-\frac{5}{2}\operatorname{sec}x\,\operatorname{tan}x)\,\text{d}x & =\frac{3}{2}\int \operatorname{cos}x\,\text{d}x-\frac{5}{2}\int \operatorname{sec}x\operatorname{tan}x\,\text{d}x \\  & =\frac{3}{2}\operatorname{sin}x-\frac{5}{2}\operatorname{sec}x+C.\end{aligned}
$$

## hard q-113923 normal generated variant 2 (authored hard)

$\int (\frac{17}{2}\operatorname{cos}x-\frac{4}{3}\operatorname{sec}x\,\operatorname{tan}x)\,\text{d}x=$

Difficulty: :question.difficulty/hard; eligible: True; parameters: {'a': '17/2', 'b': '4/3'}.

- \frac{17 \sin{\left(x \right)}}{2} + \frac{4 \sec{\left(x \right)}}{3}+C
- - \frac{17 \sin{\left(x \right)}}{2} - \frac{4 \sec{\left(x \right)}}{3}+C
* \frac{17 \sin{\left(x \right)}}{2} - \frac{4 \sec{\left(x \right)}}{3}+C
- \frac{17 \cos{\left(x \right)}}{2} - \frac{4 \tan{\left(x \right)} \sec{\left(x \right)}}{3}+C
- - \frac{17 \sin{\left(x \right)}}{2} + \frac{4 \sec{\left(x \right)}}{3}+C

Recall that

$$
\begin{aligned}\int \operatorname{cos}x\,\text{d}x & =\operatorname{sin}x+C, \\ \int \operatorname{sec}x\operatorname{tan}x\,\text{d}x & =\operatorname{sec}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (\frac{17}{2}\operatorname{cos}x-\frac{4}{3}\operatorname{sec}x\,\operatorname{tan}x)\,\text{d}x & =\frac{17}{2}\int \operatorname{cos}x\,\text{d}x-\frac{4}{3}\int \operatorname{sec}x\operatorname{tan}x\,\text{d}x \\  & =\frac{17}{2}\operatorname{sin}x-\frac{4}{3}\operatorname{sec}x+C.\end{aligned}
$$

