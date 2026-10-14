# Template extraction

## 1. Specific originals

Each row below gives its exact mask, source coefficient values, complete field banks, key positions and exact solution sequence. `source.json` retains the unmodified captured record and identifiers. `recipes.json` contains these parameterized masks. A raw replay renders masks through the normal public generate API; it does not select a literal original payload or answer lookup.

### q-2042

Anchor parameters: `{'a': 2}`. Raw profile: `raw_q-2042`.

Prompt mask:

```text
What is $\displaystyle \int - {a}\csc y\cot ydy$?
```

Field `selection`, `:answer-field.type/radio`; key index ABSENT. Complete ordered mask bank:

1. `{a}\cot y + C`
2. `{a}\csc y + C`
3. `{a}\csc^{2} y + C`
4. `-{a}\csc y + C`
5. `\csc y + C`

Solution mask (absent originally):

```text
[ABSENT]
```

### q-2044

Anchor parameters: `{'a': 3}`. Raw profile: `raw_q-2044`.

Prompt mask:

```text
What is $\displaystyle \int - {a}\sec θ\tan θdθ$?
```

Field `selection`, `:answer-field.type/radio`; key index ABSENT. Complete ordered mask bank:

1. `{a}\sec θ + C`
2. `-{a}\csc^{2} θ + C`
3. `-{a}\csc θ + C`
4. `-{a}\sec^{2} θ + C`
5. `-{a}\sec θ + C`

Solution mask (absent originally):

```text
[ABSENT]
```

### q-113923

Anchor parameters: `{'a': 3, 'b': 2}`. Raw profile: `raw_q-113923`.

Prompt mask:

```text
$\int ({a}\operatorname{cos}x-{b}\operatorname{sec}x\,\operatorname{tan}x)\,\text{d}x=$
```

Solution mask (full preserved sequence):

```text
Recall that

$$
\begin{aligned}\int \operatorname{cos}x\,\text{d}x & =\operatorname{sin}x+C, \\ \int \operatorname{sec}x\operatorname{tan}x\,\text{d}x & =\operatorname{sec}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int ({a}\operatorname{cos}x-{b}\operatorname{sec}x\,\operatorname{tan}x)\,\text{d}x & ={a}\int \operatorname{cos}x\,\text{d}x-{b}\int \operatorname{sec}x\operatorname{tan}x\,\text{d}x \\  & ={a}\operatorname{sin}x-{b}\operatorname{sec}x+C.\end{aligned}
$$
```

### q-113925

Anchor parameters: `{'a': 2}`. Raw profile: `raw_q-113925`.

Prompt mask:

```text
$\int ({a}\operatorname{csc}x\,\operatorname{cot}x+\operatorname{sin}x)\,\text{d}x=$
```

Solution mask (full preserved sequence):

```text
Recall that

$$
\begin{aligned}\int \operatorname{sin}x\,\text{d}x & =-\operatorname{cos}x+C, \\ \int \operatorname{csc}x\operatorname{cot}x\,\text{d}x & =-\operatorname{csc}x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int ({a}\operatorname{csc}x\,\operatorname{cot}x+\operatorname{sin}x)\,\text{d}x & ={a}\int \operatorname{cos}\operatorname{csc}x\,\operatorname{cot}x\,\text{d}x+\int \operatorname{sin}x\,\text{d}x \\  & ={a}(-\operatorname{csc}x)+(-\operatorname{cos}x)+C \\  & =-{a}\operatorname{csc}x-\operatorname{cos}x+C.\end{aligned}
$$
```

### q-71657

Anchor parameters: `{'a': 8}`. Raw profile: `raw_q-71657`.

Prompt mask:

```text
$\int (-{a}\operatorname{csc}y\,\operatorname{cot}y)\,\text{d}y=$
```

Solution mask (full preserved sequence):

```text
Recall that

$$
\begin{aligned}\int \operatorname{csc}y\operatorname{cot}y\,\text{d}y & =-\operatorname{csc}y+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (-{a}\operatorname{csc}y\,\operatorname{cot}y)\,\text{d}y & =-{a}\int \operatorname{csc}y\operatorname{cot}y\,\text{d}y \\  & =-{a}(-\operatorname{csc}y)+C \\  & ={a}\operatorname{csc}y+C.\end{aligned}
$$
```

### q-113920

Anchor parameters: `{'a': 3}`. Raw profile: `raw_q-113920`.

Prompt mask:

```text
$\int -{a}csc⁡x\,cot⁡x\,\text{d}x=$
```

Field `selection`, `:answer-field.type/radio`; key index 2. Complete ordered mask bank:

1. `{a}sec⁡xcot⁡x+C`
2. `-{a}csc⁡x+C`
3. `{a}csc⁡x+C`
4. `{a}sec⁡x+C`
5. `-{a}sec⁡x+C`

Solution mask (full preserved sequence):

```text
Recall that

$$
\int csc⁡xcot⁡x\,\text{d}x=-csc⁡x+C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int -{a}csc⁡x\,cot⁡x\,\text{d}x & =-{a}\int csc⁡xcot⁡x\,\text{d}x \\  & =-{a}(-csc⁡x)+C \\  & ={a}csc⁡x+C.\end{aligned}\end{aligned}
$$
```

### q-113926

Anchor parameters: `{'a': 4, 'b': 3}`. Raw profile: `raw_q-113926`.

Prompt mask:

```text
$\int ({a}sin⁡x-{b}csc⁡x\,cot⁡x)\,\text{d}x=$
```

Field `selection`, `:answer-field.type/radio`; key index 2. Complete ordered mask bank:

1. `-{a}cos⁡x-{b}csc⁡x+C`
2. `{a}cos⁡x+{b}{csc}^{2}⁡x+C`
3. `-{a}cos⁡x+{b}csc⁡x+C`
4. `{a}cos⁡x+{b}sec⁡x+C`
5. `-{a}cos⁡x-{b}cot⁡x+C`

Solution mask (full preserved sequence):

```text
Recall that

$$
\begin{aligned}\int sin⁡x\,\text{d}x & =-cos⁡x+C, \\ \int csc⁡xcot⁡x\,\text{d}x & =-csc⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int ({a}sin⁡x-{b}csc⁡x\,cot⁡x)\,\text{d}x & ={a}\int sin⁡x\,\text{d}x-{b}\int csc⁡x\,cot⁡x\,\text{d}x \\  & ={a}(-cos⁡x)-{b}(-csc⁡x)+C \\  & =-{a}cos⁡x+{b}csc⁡x+C.\end{aligned}
$$
```

### q-113928

Anchor parameters: `{'b': 5}`. Raw profile: `raw_q-113928`.

Prompt mask:

```text
$\int (\operatorname{sec}⁡x\operatorname{tan}⁡x-{b}\operatorname{cos}⁡x)\,\text{d}x=$
```

Field `selection`, `:answer-field.type/radio`; key index 4. Complete ordered mask bank:

1. `-\operatorname{sec}⁡x+{b}\operatorname{sin}⁡x+C`
2. `-\operatorname{sec}⁡x-{b}\operatorname{sin}⁡x+C`
3. `{tan}^{2}⁡x+{b}\operatorname{sin}⁡x+C`
4. `\operatorname{tan}⁡x-{b}\operatorname{sin}⁡x+C`
5. `\operatorname{sec}⁡x-{b}\operatorname{sin}⁡x+C`

Solution mask (full preserved sequence):

```text
Recall that

$$
\begin{aligned}\int \operatorname{cos}⁡x\,\text{d}x & =\operatorname{sin}⁡x+C, \\ \int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x & =\operatorname{sec}⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int (\operatorname{sec}⁡x\operatorname{tan}⁡x-{b}\operatorname{cos}⁡x)\,\text{d}x & =\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x-{b}\int \operatorname{cos}⁡x\,\text{d}x \\  & =\operatorname{sec}⁡x-{b}\operatorname{sin}⁡x+C\end{aligned}
$$
```

### q-113930

Anchor parameters: `{'a': 3, 'b': 7}`. Raw profile: `raw_q-113930`.

Prompt mask:

```text
$\int ({a}\operatorname{sec}⁡x\operatorname{tan}⁡x+{b}\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x=$
```

Field `selection`, `:answer-field.type/radio`; key index 2. Complete ordered mask bank:

1. `{sum}{sec}^{2}⁡x+C`
2. `-{a}\operatorname{tan}⁡x+{b}\operatorname{cot}⁡x+C`
3. `{a}\operatorname{sec}⁡x-{b}\operatorname{csc}⁡x+C`
4. `-{a}\operatorname{sec}⁡x-{b}\operatorname{cot}⁡x+C`
5. `{a}\operatorname{sec}⁡x+{b}\operatorname{csc}⁡x+C`

Solution mask (full preserved sequence):

```text
Recall that

$$
\begin{aligned}\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x & =\operatorname{sec}⁡x+C, \\ \int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x & =-\operatorname{csc}⁡x+C.\end{aligned}
$$

Therefore, we have

$$
\begin{aligned}\int ({a}\operatorname{sec}⁡x\operatorname{tan}⁡x+{b}\operatorname{csc}⁡x\operatorname{cot}⁡x)\,\text{d}x & ={a}\int \operatorname{sec}⁡x\operatorname{tan}⁡x\,\text{d}x+{b}\int \operatorname{csc}⁡x\operatorname{cot}⁡x\,\text{d}x \\  & ={a}\operatorname{sec}⁡x+{b}(-\operatorname{csc}⁡x)+C \\  & ={a}\operatorname{sec}⁡x-{b}\operatorname{csc}⁡x+C.\end{aligned}
$$
```

### q-2038

Anchor parameters: `{'a': 1}`. Raw profile: `raw_q-2038`.

Prompt mask:

```text
$\int (-{unit}sec⁡\theta tan⁡\theta )\text{d}\theta =$
```

Field `selection`, `:answer-field.type/radio`; key index 3. Complete ordered mask bank:

1. `{unit}sec⁡\theta +C`
2. `{unit}csc⁡xcot⁡x+C`
3. `{unit}csc⁡\theta +C`
4. `-{unit}sec⁡\theta +C`
5. `-{unit}csc⁡\theta +C`

Solution mask (full preserved sequence):

```text
Recall that

$$
\int sec⁡\theta tan⁡\theta \,\text{d}\theta =sec⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int (-{unit}sec⁡\theta tan⁡\theta )\text{d}\theta  & =-{unit}\int sec⁡\theta tan⁡\theta \,\text{d}\theta  \\  & =-{unit}(sec⁡\theta )+C \\  & =-{unit}sec⁡\theta +C.\end{aligned}\end{aligned}
$$
```

### q-71656

Anchor parameters: `{'a': 5}`. Raw profile: `raw_q-71656`.

Prompt mask:

```text
$\int {a}sec⁡\theta tan⁡\theta \,\text{d}\theta =$
```

Field `selection`, `:answer-field.type/radio`; key index 2. Complete ordered mask bank:

1. `{a}csc⁡\theta +C`
2. `-{a}sec⁡\theta +C`
3. `{a}sec⁡\theta +C`
4. `-{a}csc⁡\theta +C`
5. `{a}csc⁡\theta cot⁡\theta +C`

Solution mask (full preserved sequence):

```text
Recall that

$$
\int sec⁡\theta tan⁡\theta \,\text{d}\theta =sec⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int {a}sec⁡\theta tan⁡\theta \,\text{d}\theta  & ={a}\int sec⁡\theta tan⁡\theta \,\text{d}\theta  \\  & ={a}sec⁡\theta +C.\end{aligned}\end{aligned}
$$
```

### q-71659

Anchor parameters: `{'a': 4}`. Raw profile: `raw_q-71659`.

Prompt mask:

```text
$\int (-{a}sec⁡\theta tan⁡\theta )\,\text{d}\theta =$
```

Field `selection`, `:answer-field.type/radio`; key index 2. Complete ordered mask bank:

1. `{a}sec⁡\theta +C`
2. `{csc}^{{a}}⁡\theta +C`
3. `-{a}sec⁡\theta +C`
4. `-{a}csc⁡\theta +C`
5. `{sec}^{{a}}⁡\theta +C`

Solution mask (full preserved sequence):

```text
Recall that

$$
\int sec⁡\theta tan⁡\theta \,\text{d}\theta =sec⁡\theta +C.
$$

Therefore, we have

$$
\begin{aligned}\begin{aligned}\int (-{a}sec⁡\theta tan⁡\theta )\,\text{d}\theta  & =-{a}\int sec⁡\theta tan⁡\theta \,\text{d}\theta  \\  & =-{a}sec⁡\theta +C.\end{aligned}\end{aligned}
$$
```

## 2. Shared mathematical pattern

Reverse the derivative identities for sec·tan and csc·cot, optionally combine with the already taught sine/cosine primitive, move constant coefficients outside the integral, substitute each primitive and reduce signs. Assessment asks for a full indefinite antiderivative with one arbitrary C. Complete wrong choices must be inequivalent modulo C on pole-free real intervals.

## 3. Components and error operations

All coefficient slots above are real operand roles and propagate into prompt, constant-factor row, substituted primitive row, reduced conclusion and every choice. `sum` is derived a+b, not an independent slot. Powers in q-71659 are derived from its observed coefficient a: confusing multiplication by a with raising the primitive to a. q-113930's (a+b) sec² is a compound merge-coefficients/squared-primitive pattern; other choices replace sec by tan or csc by cot and flip explicit signs. q-113926 flips the csc sign, wrongly squares csc, substitutes sec or cot, and combines those errors with the first primitive sign error. q-113928 flips either/both signs or replaces sec by tan/tan². The complete masks account for every bank member, including all captured notation and feedback presence. These are identifiable displayed operator/scale/exponent transformations, not numerical residual offsets or fitted lookup tables. Historical error intent remains an interpretation; exact expression-pattern reproduction is established separately.

q-2042 includes omitted coefficient as its fifth wrong choice; q-2044's squared-function choices retain the historical sign and squared primitive. Their absent keys/solutions are never invented in raw evidence and their source presentations are not eligible defaults. q-2038 has an optional unit coefficient slot: coefficient 1 prints nothing, larger coefficients propagate through every assessed term. Its wrong choice uses x rather than theta; it remains evidence only.

For fieldless authored completions, choose a complete method bank before parameters: correct A+B, first-sign error −A+B, second-sign error A−B, both-sign error −A−B, unchanged integrand plus C. Single-term fieldless q-71657 uses correct csc, sign error, wrong sec primitive with either sign, and unchanged integrand. No invented learner feedback.

## 4. Reusable backbone and constraints

Fixed: requested full antiderivative, direct primitive arguments, number of terms within each source family, source shared prose and order of operative stages, five-option radio contract when observed, no plots. Variable: coefficient magnitudes only; all signs and trig-function roles retain source masks. Unit q-2038 has an optional coefficient rendering role with exact anchor 1. No arbitrary variable-letter changes count toward variety.

Easy defaults cover four signed target families. Moderate defaults cover all five source-shaped sum families, including two explicitly authored field completions. Hard defaults select one of three two-slot families before sampling two reduced fractions. Explicit calls enforce the same bounds as random sampling. Correct primitive is computed from the actual prompt first, then complete bank/solution stages derive from the same coefficients. Whole banks reject any pair equivalent modulo C; no pooled replacement or seed-dependent bank selection after parameters.

Task fingerprints hash the canonical integrand after variable normalization; they exclude banks, profile labels, solution cosmetic forms, C, seed and option order. Content IDs hash actual prompt, fixed solution, complete fields/banks/correct values and actual difficulty, then namespace all field-owned IDs. Source alias/profile names and incidental metadata never create identities.

## Source anomalies and minimal normal repairs

- q-113920: sec x cot x = csc x makes its first choice equivalent to the keyed answer. Raw replay retains both; normal replaces only that member with csc x cot x (the displayed integration-versus-differentiation error). Exact raw bank count is separate from repaired valid bank count.
- q-113925: first distributed formal integral incorrectly inserts an extra cos operator. Raw retains it; normal removes only that operator. Its missing field gets an explicitly authored complete bank.
- q-2042 and q-2044: absent difficulty, key and solution; decoded source byte checks show ordinary single backslashes. Raw preserves exact bytes and omissions, remains ineligible. Inferred mathematics is respectively +a csc(y)+C and −a sec(theta)+C; no present designation is claimed.
- q-2038: mixed-variable wrong option remains ineligible raw; the signed secant family has a supported separate normal profile.
- q-113923 and q-71657: absent fields remain absent in raw; normal fields are authored. q-113925 shares this condition.
- Decoded byte checks show actual Unicode function-application characters, not literal escaped unicode. Shared math_format normalizes learner prose/answer TeX before IDs; raw preserves exact source bytes.

No errors or missing keys count as mathematical/grading passes. All native tests use the actual supported radio IDs, including every wrong ID, through the in-memory engine; malformed raw evidence is deliberately not served or native-graded.
