# Template extraction at basis 1356

## 1. Specific questions
Every original is a five-choice single radio field `selection`: four math formulas named F/G/H/K plus text None. All domains are qualitative full 3D regions. Scalar coefficients are integers; wrong components include constants, coordinate-linear terms, squares, exp, ln and sin. The formulas are alternatives to identify, not functions to differentiate or trajectories to compute.

## 2. Shared mathematical pattern
Read the 3D diagram, eliminate incompatible components/signs/constancy, and choose the sole possible formula or None. Moderate rejects three formulas and concludes a named formula; hard rejects all four. Source bank operations below are declarative formula recipes, not recovered original cognitive-error intent. Positive coefficient scale and signed coordinate permutations produce consistent geometric variants.

## 3. Complete component map

### q-122559 (`505eb075-afb5-5225-b846-447773bcc89d`)
Level moderate, original target ('x', 1, 1) (axis, sign, source magnitude). Prompt asset ![](images/cf/cfc15b6202167211b7d6c0e8f6635dd9e571810d5296a209a4c317350604c4a4.png)

| Choice | Type | Original correct? | Exact component recipe |
|---|---|---|---|
| `G(x,y,z)=-i` | :answer.type/math | False | `-1 × (1) × i` |
| `K(x,y,z)={e}^{x}\,i` | :answer.type/math | False | `1 × ({e}^{x}) × i` |
| `H(x,y,z)=i+j+k` | :answer.type/math | False | `1 × (1) × i; 1 × (1) × j; 1 × (1) × k` |
| `F(x,y,z)=i` | :answer.type/math | True | `1 × (1) × i` |
| `None of the listed` | :answer.type/text | False | `None fallback` |

Complete prose/stage skeleton (whole equations slotted):
```text
We notice the following:

- Each vector in our vector field is parallel to the $x$-axis. So, the $j$ and $k$ components of our vector field are zero everywhere. Therefore, we can rule out the following option:

$$
@@equation2@@,\,
$$

- Moreover, each vector in our vector field is pointing in the *positive* $x$-direction, so the $i$ component of our vector field is positive. Therefore, we can rule out the following option:

$$
@@equation0@@
$$

- Finally, we note that each vector in our vector field has the same length, so the $i$ component of our vector field is constant. Therefore, we can rule out the following option:

$$
@@equation1@@
$$

Therefore, we conclude that the diagram corresponds to the vector field $@@equation3@@.$
```
Slots: {"G(x,y,z)=-i": "@@equation0@@", "K(x,y,z)={e}^{x}\\,i": "@@equation1@@", "H(x,y,z)=i+j+k": "@@equation2@@", "F(x,y,z)=i": "@@equation3@@"}

### q-122664 (`0777fbfe-65b4-5afe-92ce-361fbbf5b37f`)
Level moderate, original target ('z', 1, 2) (axis, sign, source magnitude). Prompt asset ![](images/7a/7a0a919af689e9c332ba6ceb3d606208dab9eabadef9b4871ac8e164843ebe88.png)

| Choice | Type | Original correct? | Exact component recipe |
|---|---|---|---|
| `F(x,y,z)=\operatorname{ln}⁡x\,k` | :answer.type/math | False | `1 × (\operatorname{ln}⁡x) × k` |
| `H(x,y,z)=-k` | :answer.type/math | False | `-1 × (1) × k` |
| `G(x,y,z)=i-k` | :answer.type/math | False | `1 × (1) × i; -1 × (1) × k` |
| `None of the listed` | :answer.type/text | False | `None fallback` |
| `K(x,y,z)=2\,k` | :answer.type/math | True | `2 × (1) × k` |

Complete prose/stage skeleton (whole equations slotted):
```text
We notice the following:

- Each vector in our vector field is parallel to the $z$-axis. So, the $i$ and $j$ components of our vector field are zero everywhere. Therefore, we can rule out the following option:

$$
@@equation2@@
$$

- Moreover, each vector in our vector field is pointing in the *positive* $z$-direction, so the $k$ component of our vector field is positive. Therefore, we can rule out the following option:

$$
@@equation1@@
$$

- Finally, we note that each vector in our vector field has the same length, so the $k$ component of our vector field is constant. Therefore, we can rule out the following option:

$$
@@equation0@@
$$

Therefore, we conclude that the diagram corresponds to the vector field $@@equation4@@.$
```
Slots: {"F(x,y,z)=\\operatorname{ln}⁡x\\,k": "@@equation0@@", "H(x,y,z)=-k": "@@equation1@@", "G(x,y,z)=i-k": "@@equation2@@", "K(x,y,z)=2\\,k": "@@equation4@@"}

### q-122651 (`b83bfdca-4e4b-517b-aad8-aed17555d2d8`)
Level moderate, original target ('x', 1, 2) (axis, sign, source magnitude). Prompt asset ![](images/7c/7cb4dd61f9d42a48c022a183e7f4310a8a4ed7ae881edd136881ef6863282e2c.png)

| Choice | Type | Original correct? | Exact component recipe |
|---|---|---|---|
| `F(x,y,z)=i+x\,j` | :answer.type/math | False | `1 × (1) × i; 1 × (x) × j` |
| `None of the listed` | :answer.type/text | False | `None fallback` |
| `G(x,y,z)=-i` | :answer.type/math | False | `-1 × (1) × i` |
| `K(x,y,z)=2\,i` | :answer.type/math | True | `2 × (1) × i` |
| `H(x,y,z)=x\,i` | :answer.type/math | False | `1 × (x) × i` |

Complete prose/stage skeleton (whole equations slotted):
```text
We notice the following:

- Each vector in our vector field is parallel to the $x$-axis. So, the $j$ and $k$ components of our vector field are zero everywhere. Therefore, we can rule out the following option:

$$
@@equation0@@
$$

- Moreover, each vector in our vector field is pointing in the *positive* $x$-direction, so the $i$ component of our vector field is positive. Therefore, we can rule out the following option:

$$
@@equation2@@
$$

- Finally, we note that each vector in our vector field has the same length, so the $i$ component of our vector field is constant. Therefore, we can rule out the following option:

$$
@@equation4@@
$$

Therefore, we conclude that the diagram corresponds to the vector field $@@equation3@@.$
```
Slots: {"F(x,y,z)=i+x\\,j": "@@equation0@@", "G(x,y,z)=-i": "@@equation2@@", "K(x,y,z)=2\\,i": "@@equation3@@", "H(x,y,z)=x\\,i": "@@equation4@@"}

### q-122668 (`db25e593-34c2-554c-af14-c5a728ea4219`)
Level moderate, original target ('y', -1, 1) (axis, sign, source magnitude). Prompt asset ![](images/f8/f89653698d9c2bad0c2e6a77d4dad1953a9fd72f89cbfc08fd68aac802acd284.png)

| Choice | Type | Original correct? | Exact component recipe |
|---|---|---|---|
| `K(x,y,z)=2\,j` | :answer.type/math | False | `2 × (1) × j` |
| `H(x,y,z)=x\,j` | :answer.type/math | False | `1 × (x) × j` |
| `G(x,y,z)=4\,k` | :answer.type/math | False | `4 × (1) × k` |
| `None of the listed` | :answer.type/text | False | `None fallback` |
| `F(x,y,z)=-j` | :answer.type/math | True | `-1 × (1) × j` |

Complete prose/stage skeleton (whole equations slotted):
```text
We notice the following:

- Each vector in our vector field is parallel to the $y$-axis. So, the $i$ and $k$ components of our vector field are zero everywhere. Therefore, we can rule out the following option:

$$
@@equation2@@
$$

- Moreover, each vector in our vector field is pointing in the *negative* $y$-direction, so the $j$ component of our vector field is negative. Therefore, we can rule out the following option:

$$
@@equation0@@
$$

- Finally, we note that each vector in our vector field has the same length, so the $j$ component of our vector field is constant. Therefore, we can rule out the following option:

$$
@@equation1@@
$$

Therefore, we conclude that the diagram corresponds to the vector field $@@equation4@@.$
```
Slots: {"K(x,y,z)=2\\,j": "@@equation0@@", "H(x,y,z)=x\\,j": "@@equation1@@", "G(x,y,z)=4\\,k": "@@equation2@@", "F(x,y,z)=-j": "@@equation4@@"}

### q-122670 (`548bbae5-603d-5bc6-9f7d-4ca6dbc971eb`)
Level hard, original target ('z', -1, 1) (axis, sign, source magnitude). Prompt asset ![](images/64/64f02fa7dcd23b20e61801c0453d8fe7ed013936572e1ee63f748361edd4dec5.png)

| Choice | Type | Original correct? | Exact component recipe |
|---|---|---|---|
| `None of the listed` | :answer.type/text | True | `None fallback` |
| `F(x,y,z)=i` | :answer.type/math | False | `1 × (1) × i` |
| `H(x,y,z)=k` | :answer.type/math | False | `1 × (1) × k` |
| `G(x,y,z)=-j` | :answer.type/math | False | `-1 × (1) × j` |
| `K(x,y,z)=-{x}^{2}\,k` | :answer.type/math | False | `-1 × ({x}^{2}) × k` |

Complete prose/stage skeleton (whole equations slotted):
```text
We notice the following:

- Each vector in our vector field is parallel to the $z$-axis. So, the $i$ and $j$ components of our vector field are zero everywhere. Therefore, we can rule out the following option:

$$
@@equation1@@,\,@@equation3@@
$$

- Moreover, each vector in our vector field is pointing in the *negative* $z$-direction, so the $k$ component of our vector field is negative. Therefore, we can rule out the following option:

$$
@@equation2@@
$$

- Finally, we note that each vector in our vector field has the same length, so the $k$ component of our vector field is constant. Therefore, we can rule out the following option:

$$
@@equation4@@
$$

Therefore, we conclude that the diagram doesn't correspond to any of the listed vector fields.
```
Slots: {"F(x,y,z)=i": "@@equation1@@", "H(x,y,z)=k": "@@equation2@@", "G(x,y,z)=-j": "@@equation3@@", "K(x,y,z)=-{x}^{2}\\,k": "@@equation4@@"}

### q-123748 (`1c63175a-a455-54b8-b784-f9c30e4507e1`)
Level moderate, original target ('x', -1, 2) (axis, sign, source magnitude). Prompt asset ![](images/bf/bff60466ca8abba4fd849c046c02af3a4811279774975fc981cafad91d734ed5.png)

| Choice | Type | Original correct? | Exact component recipe |
|---|---|---|---|
| `None of the listed` | :answer.type/text | False | `None fallback` |
| `H(x,y,z)=-2\,i` | :answer.type/math | True | `-2 × (1) × i` |
| `F(x,y,z)=i` | :answer.type/math | False | `1 × (1) × i` |
| `K(x,y,z)=-i+j` | :answer.type/math | False | `-1 × (1) × i; 1 × (1) × j` |
| `G(x,y,z)=-y\,i` | :answer.type/math | False | `-1 × (y) × i` |

Complete prose/stage skeleton (whole equations slotted):
```text
We notice the following:

- Each vector in our vector field is parallel to the $x$-axis. So, the $j$ and $k$ components of our vector field are zero everywhere. Therefore, we can rule out the following option:

$$
@@equation3@@
$$

- Moreover, each vector in our vector field is pointing in the *negative* $x$-direction, so the $i$ component of our vector field is negative. Therefore, we can rule out the following option:

$$
@@equation2@@
$$

- Finally, we note that each vector in our vector field has the same length, so the $i$ component of our vector field is constant. Therefore, we can rule out the following option:

$$
@@equation4@@
$$

Therefore, we conclude that the diagram corresponds to the vector field $@@equation1@@.$
```
Slots: {"H(x,y,z)=-2\\,i": "@@equation1@@", "F(x,y,z)=i": "@@equation2@@", "K(x,y,z)=-i+j": "@@equation3@@", "G(x,y,z)=-y\\,i": "@@equation4@@"}

### q-123749 (`589ce8fd-18ca-5044-bdd6-238376c16f16`)
Level hard, original target ('y', -1, 1) (axis, sign, source magnitude). Prompt asset ![](images/f8/f89653698d9c2bad0c2e6a77d4dad1953a9fd72f89cbfc08fd68aac802acd284.png)

| Choice | Type | Original correct? | Exact component recipe |
|---|---|---|---|
| `H(x,y,z)=i+k` | :answer.type/math | False | `1 × (1) × i; 1 × (1) × k` |
| `G(x,y,z)=-{x}^{2}\,j` | :answer.type/math | False | `-1 × ({x}^{2}) × j` |
| `F(x,y,z)=j` | :answer.type/math | False | `1 × (1) × j` |
| `None of the listed` | :answer.type/text | True | `None fallback` |
| `K(x,y,z)=i+{e}^{x}\,k` | :answer.type/math | False | `1 × (1) × i; 1 × ({e}^{x}) × k` |

Complete prose/stage skeleton (whole equations slotted):
```text
We notice the following:

- Each vector in our vector field is parallel to the $y$-axis. So, the $i$ and $k$ components of our vector field are zero everywhere. Therefore, we can rule out the following options:

$$
@@equation0@@,\,@@equation4@@
$$

- Moreover, each vector in our vector field is pointing in the *negative* $y$-direction, so the $j$ component of our vector field is negative. Therefore, we can rule out the following option:

$$
@@equation2@@
$$

- Finally, we note that each vector in our vector field has the same length, so the $j$ component of our vector field is constant. Therefore, we can rule out the following option:

$$
@@equation1@@
$$

Therefore, we conclude that the diagram doesn't correspond to any of the listed vector fields.
```
Slots: {"H(x,y,z)=i+k": "@@equation0@@", "G(x,y,z)=-{x}^{2}\\,j": "@@equation1@@", "F(x,y,z)=j": "@@equation2@@", "K(x,y,z)=i+{e}^{x}\\,k": "@@equation4@@"}

### q-123750 (`c9c83b42-2a92-533d-be7a-98b1b72e544d`)
Level hard, original target ('x', 1, 1) (axis, sign, source magnitude). Prompt asset ![](images/cf/cfc15b6202167211b7d6c0e8f6635dd9e571810d5296a209a4c317350604c4a4.png)

| Choice | Type | Original correct? | Exact component recipe |
|---|---|---|---|
| `H(x,y,z)=-\,i` | :answer.type/math | False | `-1 × (1) × i` |
| `K(x,y,z)=-{e}^{y}\,k` | :answer.type/math | False | `-1 × ({e}^{y}) × k` |
| `None of the listed` | :answer.type/text | True | `None fallback` |
| `G(x,y,z)=i-j` | :answer.type/math | False | `1 × (1) × i; -1 × (1) × j` |
| `F(x,y,z)=-2\,i` | :answer.type/math | False | `-2 × (1) × i` |

Complete prose/stage skeleton (whole equations slotted):
```text
We notice the following:

- Each vector in our vector field is parallel to the $x$-axis. So, the $j$ and $k$ components of our vector field are zero everywhere. Therefore, we can rule out the following option:

$$
@@equation3@@
$$

- Moreover, each vector in our vector field is pointing in the *positive* $x$-direction, so the $i$ component of our vector field is positive. Therefore, we can rule out the following options:

$$
@@equation4@@,\,@@equation0@@
$$

- Finally, we note that each vector in our vector field has the same length, so the $i$ component of our vector field is constant. Therefore, we can rule out the following option:

$$
@@equation1@@
$$

Therefore, we conclude that the diagram doesn't correspond to any of the listed vector fields.
```
Slots: {"H(x,y,z)=-\\,i": "@@equation0@@", "K(x,y,z)=-{e}^{y}\\,k": "@@equation1@@", "G(x,y,z)=i-j": "@@equation3@@", "F(x,y,z)=-2\\,i": "@@equation4@@"}

### q-122662 (`f6439da6-7b28-559c-9b9e-cf7883c3a650`)
Level moderate, original target ('y', 1, 3) (axis, sign, source magnitude). Prompt asset ![](images/8d/8d978a63c661ddb2adfca6f0be5315778abb2464a1e1f45f78dedfa4cbaa5d12.png)

| Choice | Type | Original correct? | Exact component recipe |
|---|---|---|---|
| `None of the listed` | :answer.type/text | False | `None fallback` |
| `H(x,y,z)=i+k` | :answer.type/math | False | `1 × (1) × i; 1 × (1) × k` |
| `F(x,y,z)=-2\,j` | :answer.type/math | False | `-2 × (1) × j` |
| `G(x,y,z)=3\,j` | :answer.type/math | True | `3 × (1) × j` |
| `K(x,y,z)=\operatorname{sin}⁡y\,j` | :answer.type/math | False | `1 × (\operatorname{sin}⁡y) × j` |

Complete prose/stage skeleton (whole equations slotted):
```text
We notice the following:

- Each vector in our vector field is parallel to the $y$-axis. So, the $i$ and $k$ components of our vector field are zero everywhere. Therefore, we can rule out the following option:

$$
@@equation1@@
$$

- Moreover, each vector in our vector field is pointing in the *positive* $y$-direction, so the $j$ component of our vector field is positive. Therefore, we can rule out the following option:

$$
@@equation2@@
$$

- Finally, we note that each vector in our vector field has the same length, so the $j$ component of our vector field is constant. Therefore, we can rule out the following option:

$$
@@equation4@@
$$

Therefore, we conclude that the diagram corresponds to the vector field $@@equation3@@.$
```
Slots: {"H(x,y,z)=i+k": "@@equation1@@", "F(x,y,z)=-2\\,j": "@@equation2@@", "G(x,y,z)=3\\,j": "@@equation3@@", "K(x,y,z)=\\operatorname{sin}⁡y\\,j": "@@equation4@@"}

### q-122667 (`76f85577-2f56-52c7-abc0-220aedba2d13`)
Level moderate, original target ('x', -1, 1) (axis, sign, source magnitude). Prompt asset ![](images/9d/9db14c13d03cb99846a40622a9633f229e8bd18942f2d03635961529e6970771.png)

| Choice | Type | Original correct? | Exact component recipe |
|---|---|---|---|
| `None of the listed` | :answer.type/text | False | `None fallback` |
| `K(x,y,z)=i-j-k` | :answer.type/math | False | `1 × (1) × i; -1 × (1) × j; -1 × (1) × k` |
| `F(x,y,z)=y\,i` | :answer.type/math | False | `1 × (y) × i` |
| `G(x,y,z)=i` | :answer.type/math | False | `1 × (1) × i` |
| `H(x,y,z)=-i` | :answer.type/math | True | `-1 × (1) × i` |

Complete prose/stage skeleton (whole equations slotted):
```text
We notice the following:

- Each vector in our vector field is parallel to the $x$-axis. So, the $j$ and $k$ components of our vector field are zero everywhere. Therefore, we can rule out the following option:

$$
@@equation1@@
$$

- Moreover, each vector in our vector field is pointing in the *negative* $x$-direction, so the $i$ component of our vector field is negative. Therefore, we can rule out the following option:

$$
@@equation3@@
$$

- Finally, we note that each vector in our vector field has the same length, so the $i$ component of our vector field is constant. Therefore, we can rule out the following option:

$$
@@equation2@@
$$

Therefore, we conclude that the diagram corresponds to the vector field $@@equation4@@.$
```
Slots: {"K(x,y,z)=i-j-k": "@@equation1@@", "F(x,y,z)=y\\,i": "@@equation2@@", "G(x,y,z)=i": "@@equation3@@", "H(x,y,z)=-i": "@@equation4@@"}

## 4. Reusable template and calculations
Fixed prompt: image, blank line, “Which of the following could be the function that generates the vector field above?” Fixed solution opening: “We notice the following:” and source bullet/TeX/conclusion sequence. Whole formulas are slots; isolated axis/basis labels in prose are replaced through coordinate/basis maps. Never replace short expressions inside function labels or basis tokens.
Moderate has three bullets: missing components; sign; constancy. Hard likewise has three bullets, with profile-specific one/two eliminated formula row groupings. All complete original banks remain distinct. Easy is authored with the same prose and two bullets: wrong axes; opposite sign. It adds no variable target or calculus. Each generated instance has a single fixed solution regardless of submission.
Parameters: coordinate permutation in S3, uniform coefficient sign flip ±1, positive common integer scale 1..3. Apply all choices simultaneously, including wrong terms, keep exact relative integer ratios and signs, and transform scalar variable dependencies with the same coordinate permutation. Reject the whole bank if complete formulas coincide or more than one option matches the qualitative target. Correctness is computed from the formulas; no source correct-ID lookup determines generated answers.
Task fingerprint records only signed constant target axis, excluding scale, profile and names. Content identity includes complete displayed bank/prompt/solution; seed and shuffling do not enter. Domain restrictions and provenance stay outside learner content. Plots are central, heavy; see plot-extraction.md.

## Source anomalies and supported handling
q-123750’s third bullet claims its i component constancy rules out K=-e^y k. That K has i=0, so this component-only implication is invalid. Whole-vector constancy rules it out. Raw source is available under explicit public profile `observed:q-123750`, with exact original bank/prose. Normal `q-123750` changes only “so the $i$ component of our vector field is constant” to “so every component of our vector field is constant,” after axis rotation. No correct designation changes. Exact raw solution replay denominator is 10/10; mathematically supported normal solutions are 10/10 with this one repair.
Canonical e-9473 incorrectly calls the i component constant when the displayed field is -k; evidence retained, no practice denominator, and not used to write easy prose. q-122559 has a trailing comma/thinspace after a worked equation; raw presentation is retained as valid punctuation, parser strips it for mathematical checks. Invisible function-application Unicode in ln/sin is retained at source replay, not treated as doubled slashes. No missing fields, incomplete banks or unresolved source comparisons remain.