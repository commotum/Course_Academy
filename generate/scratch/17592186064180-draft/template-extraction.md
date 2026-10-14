# Template extraction — four stages

## 1. Specific original questions

This analysis uses the complete immutable basis2275 records; no independent inventory row is called an original. Exact full records remain in source.json. No question contains plots.

### q-2035

What is $\displaystyle \int3\sec^{2} zdz$?

Observed parameter values: `{"a": 3}`. Difficulty: absent/unrated. Worked solution absent. Field attribute present.

### q-49118

What is $\displaystyle \int\sec x(\tan x + 8\sec x)dx$?

Observed parameter values: `{"a": 8}`. Difficulty: absent/unrated. Worked solution absent. Field attribute present.

### q-113935

$\int -\frac{3}{2}{sec}^{2}x\,\text{d}x=$

Observed parameter values: `{"n": 3, "d": 2}`. Difficulty: :question.difficulty/easy. Worked solution present. Field attribute absent.

The complete observed wording and calculation stages:

Recall that 

$$
\int {sec}^{2}x\,\text{d}x=\operatorname{tan}x+C
$$

Therefore, we get

$$
\begin{aligned}\begin{aligned}\int -\frac{3}{2}{sec}^{2}x\,\text{d}x & =-\frac{3}{2}\int {sec}^{2}x\,\text{d}x \\  & =-\frac{3}{2}(\operatorname{tan}x)+C \\  & =-\frac{3}{2}\operatorname{tan}x+C.\end{aligned}\end{aligned}
$$

### q-2162

$\int (2{sec}^{2}x-\operatorname{sin}x)\,\text{d}x=$

Observed parameter values: `{"a": 2}`. Difficulty: :question.difficulty/moderate. Worked solution present. Field attribute absent.

The complete observed wording and calculation stages:

Recall that

$$
\begin{aligned}\int \operatorname{sin}x\,\text{d}x & =-\operatorname{cos}x+C, \\ \int {sec}^{2}x\,\text{d}x & =\operatorname{tan}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int (2{sec}^{2}x-\operatorname{sin}x)\,\text{d}x & =\int 2{sec}^{2}x\,\text{d}x-\int \operatorname{sin}x\,\text{d}x \\  & =2\operatorname{tan}x-(-\operatorname{cos}x)+C \\  & =2\operatorname{tan}x+\operatorname{cos}x+C.\end{aligned}\end{aligned}
$$

### q-2165

$\int (\operatorname{sec}x\operatorname{tan}x-{sec}^{2}x)\,\text{d}x=$

Observed parameter values: `{"b": 1}`. Difficulty: :question.difficulty/moderate. Worked solution present. Field attribute absent.

The complete observed wording and calculation stages:

Recall that

$$
\begin{aligned}\int \operatorname{sec}x\operatorname{tan}x\,\text{d}x & =\operatorname{sec}x+C, \\ \int {sec}^{2}x\,\text{d}x & =\operatorname{tan}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int (\operatorname{sec}x\operatorname{tan}x-{sec}^{2}x)\,\text{d}x & =\int \operatorname{sec}x\operatorname{tan}x\,\text{d}x-\int {sec}^{2}x\,\text{d}x \\  & =\operatorname{sec}x-\operatorname{tan}x+C.\end{aligned}\end{aligned}
$$

### q-113936

$\int 2{sec}^{2}⁡\theta \,\text{d}\theta =$

Observed parameter values: `{"a": 2}`. Difficulty: :question.difficulty/easy. Worked solution present. Field attribute present.

The complete observed wording and calculation stages:

Recall that 

$$
\int {sec}^{2}⁡\theta \,\text{d}\theta =tan⁡\theta +C
$$

Therefore, we get

$$
\begin{aligned}\begin{aligned}\int 2{sec}^{2}⁡\theta \,\text{d}\theta  & =2\int {sec}^{2}⁡\theta \,\text{d}\theta  \\  & =2tan⁡\theta +C.\end{aligned}\end{aligned}
$$

### q-113937

$\int -4{sec}^{2}⁡z\,\text{d}z=$

Observed parameter values: `{"a": 4}`. Difficulty: :question.difficulty/easy. Worked solution present. Field attribute present.

The complete observed wording and calculation stages:

Recall that 

$$
\int {sec}^{2}⁡z\,\text{d}z=tan⁡z+C
$$

Therefore, we get

$$
\begin{aligned}\begin{aligned}\int -4{sec}^{2}⁡z\,\text{d}z & =-4\int {sec}^{2}⁡z\,\text{d}z \\  & =-4(tan⁡z)+C \\  & =-4tan⁡z+C.\end{aligned}\end{aligned}
$$

### q-113944

$\int ({sec}^{2}⁡x-2\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x=$

Observed parameter values: `{"b": 2}`. Difficulty: :question.difficulty/moderate. Worked solution present. Field attribute present.

The complete observed wording and calculation stages:

Recall that

$$
\begin{aligned}\int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x & =-\operatorname{csc}⁡x+C \\ \int {sec}^{2}⁡x\,\text{d}x & =\operatorname{tan}⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int ({sec}^{2}⁡x-2\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x & =\int {sec}^{2}⁡x\,\text{d}x-2\int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & =\operatorname{tan}⁡x-2(-\operatorname{csc}⁡x)+C \\  & =\operatorname{tan}⁡x+2\operatorname{csc}⁡x+C.\end{aligned}\end{aligned}
$$

### q-2164

$\int (4csc⁡xcot⁡x+{sec}^{2}⁡x)\,\text{d}x=$

Observed parameter values: `{"b": 4}`. Difficulty: :question.difficulty/moderate. Worked solution present. Field attribute present.

The complete observed wording and calculation stages:

Recall that

$$
\begin{aligned}\int csc⁡xcot⁡x\,\text{d}x & =-csc⁡x+C \\ \int {sec}^{2}⁡x\,\text{d}x & =tan⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int (4csc⁡xcot⁡x+{sec}^{2}⁡x)\,\text{d}x & =\int 4csc⁡xcot⁡x\,\text{d}x+\int {sec}^{2}⁡x\,\text{d}x \\  & =4(-csc⁡x)+tan⁡x+C \\  & =-4csc⁡x+tan⁡x+C.\end{aligned}\end{aligned}
$$

### q-49122

Calculate $\int sec⁡x(7sec⁡x+4tan⁡x)\text{d}x.$

Observed parameter values: `{"a": 7, "b": 4}`. Difficulty: :question.difficulty/moderate. Worked solution present. Field attribute present.

The complete observed wording and calculation stages:

Recall that

$$
\begin{aligned}\int sec⁡xtan⁡x\,\text{d}x & =sec⁡x+C, \\ \int {sec}^{2}⁡x\,\text{d}x & =tan⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int sec⁡x(7sec⁡x+4tan⁡x)\text{d}x & =\int (7{sec}^{2}⁡x+4sec⁡xtan⁡x)\text{d}x \\  & =\int 7{sec}^{2}⁡x\,\text{d}x+\int 4sec⁡xtan⁡x\,\text{d}x \\  & =7\int {sec}^{2}⁡x\,\text{d}x+4\int sec⁡xtan⁡x\,\text{d}x \\  & =7tan⁡x+4sec⁡x+C.\end{aligned}\end{aligned}
$$

## 2. Generalized backbone

Every original applies direct primitive recall to sec² at an unchanged variable. Some multiply by a constant; two-term families apply the sum rule and, in the secant-product family, distribute secant first. Different stage sequences remain separate families. A sec² primitive is tan+C; preceding-lesson primitives sec tan→sec, csc cot→-csc and sin→-cos support only the combinations already captured. Radio fields own complete five-choice banks; fieldless originals and unrated/missing-key originals remain incomplete raw evidence.

## 3. Complete component and bank mapping

`source-profiles.json` stores every full prompt, full solution, answer-field attribute, answer type, answer value and correct designation as parameterized masks. Attribute omissions stay absent. No feedback occurs in any original. Every source is replayed by the public generate API through `raw:q-ID`. The symbol a/b denotes the observed integer magnitude; n/d denotes the observed reduced rational magnitude. Replacement uses complete masks, never generic correct-answer-plus-literal residual lookup.

### q-2035 profile

Prompt mask: `What is $\displaystyle \int@a@\sec^{2} zdz$?`

| Position | Exact original value | Full parameterized value recipe | Operation/pattern |
|---|---|---|---|
| 1 | `3\cot z + C` | `@a@\cot z + C` | Replace tangent primitive by cotangent. |
| 2 | `3\sec z\tan z + C` | `@a@\sec z\tan z + C` | Retain the secant derivative product instead of its primitive. |
| 3 | `3\tan z + C` | `@a@\tan z + C` | Correct: retain scalar, replace sec² by tan. |
| 4 | `3\sec z + C` | `@a@\sec z + C` | Replace tangent primitive by secant. |
| 5 | `3\csc z + C` | `@a@\csc z + C` | Replace tangent primitive by cosecant. |

Field: selection / radio, five complete choices. Correct value: `ABSENT`.

### q-49118 profile

Prompt mask: `What is $\displaystyle \int\sec x(\tan x + @a@\sec x)dx$?`

| Position | Exact original value | Full parameterized value recipe | Operation/pattern |
|---|---|---|---|
| 1 | `\csc x - 8\cot x + C` | `\csc x - @a@\cot x + C` | Replace sec by csc and tan by negative cot. |
| 2 | `\sec x + 8\tan x + C` | `\sec x + @a@\tan x + C` | Correct mathematical primitive, but original has no designation. |
| 3 | `-\sec x + 4\csc x + C` | `-\sec x + @half@\csc x + C` | Observed negative sec plus half-coefficient csc: numerical pattern only, error intent opaque. |
| 4 | `8\sec x\tan x + C` | `@a@\sec x\tan x + C` | Observed a sec tan: scalar/function pattern only, intent opaque. |
| 5 | `-8\sec x\csc x + C` | `-@a@\sec x\csc x + C` | Observed -a sec csc: product pattern only, intent opaque. |

Field: selection / radio, five complete choices. Correct value: `ABSENT`.

### q-113935 profile

Prompt mask: `$\int -\frac{@n@}{@d@}{sec}^{2}x\,\text{d}x=$`

Field attribute absent: retain absence. Any normal radio completion is authored.

### q-2162 profile

Prompt mask: `$\int (@a@{sec}^{2}x-\operatorname{sin}x)\,\text{d}x=$`

Field attribute absent: retain absence. Any normal radio completion is authored.

### q-2165 profile

Prompt mask: `$\int (\operatorname{sec}x\operatorname{tan}x-@coef@{sec}^{2}x)\,\text{d}x=$`

Field attribute absent: retain absence. Any normal radio completion is authored.

### q-113936 profile

Prompt mask: `$\int @a@{sec}^{2}⁡\theta \,\text{d}\theta =$`

| Position | Exact original value | Full parameterized value recipe | Operation/pattern |
|---|---|---|---|
| 1 | `2sec⁡\theta +C` | `@a@sec⁡\theta +C` | Scalar times sec instead of scalar times tan. |
| 2 | `-2csc⁡\theta +C` | `-@a@csc⁡\theta +C` | Negative scalar times csc instead of scalar times tan. |
| 3 | `-{csc}^{2}⁡\theta +C` | `-{csc}^{2}⁡\theta +C` | Drop scalar; negative squared csc instead of tangent. |
| 4 | `{tan}^{2}⁡\theta +C` | `{tan}^{2}⁡\theta +C` | Drop scalar; squared tangent instead of tangent. |
| 5 | `2tan⁡\theta +C` | `@a@tan⁡\theta +C` | Correct: retain scalar times tangent. |

Field: selection / radio, five complete choices. Correct value: `@a@tan⁡\theta +C`.

### q-113937 profile

Prompt mask: `$\int -@a@{sec}^{2}⁡z\,\text{d}z=$`

| Position | Exact original value | Full parameterized value recipe | Operation/pattern |
|---|---|---|---|
| 1 | `-4sec⁡z+C` | `-@a@sec⁡z+C` | Keep negative scalar, wrong sec primitive. |
| 2 | `4tan⁡z+C` | `@a@tan⁡z+C` | Lose coefficient minus sign. |
| 3 | `4{sec}^{2}⁡z+C` | `@a@{sec}^{2}⁡z+C` | Lose minus sign and retain sec² input instead of integrating. |
| 4 | `4cot⁡z+C` | `@a@cot⁡z+C` | Lose minus sign; replace tangent by cotangent. |
| 5 | `-4tan⁡z+C` | `-@a@tan⁡z+C` | Correct: retain negative scalar times tangent. |

Field: selection / radio, five complete choices. Correct value: `-@a@tan⁡z+C`.

### q-113944 profile

Prompt mask: `$\int ({sec}^{2}⁡x-@b@\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x=$`

| Position | Exact original value | Full parameterized value recipe | Operation/pattern |
|---|---|---|---|
| 1 | `\operatorname{tan}⁡x+2\operatorname{csc}⁡x+C` | `\operatorname{tan}⁡x+@b@\operatorname{csc}⁡x+C` | Correct: tan+b csc, two primitive signs combined. |
| 2 | `\operatorname{cot}⁡x-2{csc}^{2}⁡x+C` | `\operatorname{cot}⁡x-@b@{csc}^{2}⁡x+C` | sec² maps to cot; -b csc cot maps to -b csc² (wrong exponent/sign). |
| 3 | `\operatorname{tan}⁡x-2\operatorname{cot}⁡x+C` | `\operatorname{tan}⁡x-@b@\operatorname{cot}⁡x+C` | First primitive correct; second replaced by -b cot. |
| 4 | `\operatorname{cot}⁡x+2\operatorname{csc}⁡x+C` | `\operatorname{cot}⁡x+@b@\operatorname{csc}⁡x+C` | sec² maps to cot; second primitive/sign correct. |
| 5 | `-\operatorname{tan}⁡x+2{csc}^{2}⁡x+C` | `-\operatorname{tan}⁡x+@b@{csc}^{2}⁡x+C` | First primitive negated; second replaced by positive b csc². |

Field: selection / radio, five complete choices. Correct value: `\operatorname{tan}⁡x+@b@\operatorname{csc}⁡x+C`.

### q-2164 profile

Prompt mask: `$\int (@b@csc⁡xcot⁡x+{sec}^{2}⁡x)\,\text{d}x=$`

| Position | Exact original value | Full parameterized value recipe | Operation/pattern |
|---|---|---|---|
| 1 | `4csc⁡x+tan⁡x+C` | `@b@csc⁡x+tan⁡x+C` | Lose negative csc primitive sign. |
| 2 | `-4csc⁡x-tan⁡x+C` | `-@b@csc⁡x-tan⁡x+C` | Csc primitive sign correct; negate tangent primitive. |
| 3 | `4csc⁡x+sec⁡x+C` | `@b@csc⁡x+sec⁡x+C` | Lose csc primitive sign and replace tangent by sec. |
| 4 | `-4cot⁡x+tan⁡x+C` | `-@b@cot⁡x+tan⁡x+C` | Replace -b csc by -b cot. |
| 5 | `-4csc⁡x+tan⁡x+C` | `-@b@csc⁡x+tan⁡x+C` | Correct: -b csc+tan. |

Field: selection / radio, five complete choices. Correct value: `-@b@csc⁡x+tan⁡x+C`.

### q-49122 profile

Prompt mask: `Calculate $\int sec⁡x(@a@sec⁡x+@b@tan⁡x)\text{d}x.$`

| Position | Exact original value | Full parameterized value recipe | Operation/pattern |
|---|---|---|---|
| 1 | `-7tan⁡x+4csc⁡x+C` | `-@a@tan⁡x+@b@csc⁡x+C` | Negate a tangent primitive; replace b sec by b csc. |
| 2 | `-7tan⁡x-4csc⁡x+C` | `-@a@tan⁡x-@b@csc⁡x+C` | Negate a tangent primitive and use negative b csc instead of b sec. |
| 3 | `7tan⁡x+4sec⁡x+C` | `@a@tan⁡x+@b@sec⁡x+C` | Correct: a tan+b sec after distribution/splitting/scalar extraction. |
| 4 | `7cot⁡x+4sec⁡x+C` | `@a@cot⁡x+@b@sec⁡x+C` | Replace a tangent primitive by a cot. |
| 5 | `7cot⁡x-4sec⁡x+C` | `@a@cot⁡x-@b@sec⁡x+C` | Replace a tan by a cot and negate b sec. |

Field: selection / radio, five complete choices. Correct value: `@a@tan⁡x+@b@sec⁡x+C`.

## 4. Reusable templates and slot constraints

Source profiles preserve their own complete prose and operative masks. Original integer slots range1..9, except nonunit easy magnitudes2..9; raw q-49118 uses even a2..8 to keep its half-scale coefficient integral. Fraction n,d are coprime2..9 and unequal. q-2165 varies the coefficient of the sec² component while retaining its source recall, termwise split and primitive stages; b=1 has the exact omitted-unit notation. All explicit calls enforce the same bounds as samplers.

Five complete rated banks are normal defaults in their source families. Their coefficient/exponent/function/sign patterns are fully recovered as expression patterns, not inferred learner intentions. The opaque unrated q-49118 bank is evidence-only; its reverse-product normal family uses a separate authored method bank: correct a tan+b sec, second primitive sign error, first primitive sign error, tangent→cot, secant→csc. No opaque source scalar fit is promoted to default learning.

Completed fraction normal bank: coefficient times tan (correct), reversed coefficient sign, tangent→sec, tangent→cot, retained sec² input. Completed single positive bank follows all five q-2035 expression patterns with a derived key/solution/level. Sine-sum normal bank: correct a tan+b cos; miss negative-sine cancellation; retain sec²; tangent→cot; sine primitive incorrectly remains sine. Secant-difference bank: correct a sec-b tan; wrong sec sign; wrong subtraction sign; retain sec²; tangent→cot.

Authored hard has one distribution, three termwise integrals, three scalar extractions, three primitive substitutions and sign collection. Its complete bank is correct a tan+b sec∓c csc; wrong cosecant sign; wrong tangent sign; retain sec²; replace csc primitive by cot. Choose the plus/minus complete profile before coefficients; all a,b,c in1..9 are nonzero, so hard cannot collapse to moderate. These are same-method errors tied to actual components. There are no answer-specific feedback or diagnostic sentences.

Correct values are derived from the actual direct-primitive method before distractor construction; every wrong value comes from the listed component transformations. The whole instance is rejected if any member is equivalent modulo an additive constant, any designation is invalid, or any member is ambiguous. All normal options have one shared worked solution independent of response.

Domains: use connected real intervals excluding poles of every rendered primitive and input; compare antiderivative families modulo additive constants. No definite endpoint/domain branch is introduced. Mathematical fingerprints use the expanded actual integrand after alpha-renaming its variable; they exclude profile names, bank aliases, seeds, ordering and incidental notation. Content identities include version, actual difficulty/omission, prompt, complete solution, every field, every displayed value/feedback and key. Distinct banks therefore retain different identities even when their integral task matches.

The full original worked-solution text appears above. Raw replay verifies bytes and attribute presence independently through rootF.check; normal source families retain these operative stage sequences at changed coefficients, with only shared UI normalization. Raw source masks are explicit public evidence-only profiles. Generated normal completions and missing hard difficulty are authored claims, with conservative scope and calibration uncertainty.
