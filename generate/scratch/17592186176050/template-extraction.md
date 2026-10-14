# Template extraction

## Stage 1: original descriptions

All questions give the tangent of an unspecified real angle and request a tangent at that same angle plus an integer multiple of π. There is no negative coefficient on x inside tangent and no half-period shift. Thus the assessed trigonometric step is precisely periodicity. The domain is any x at which the supplied tangent is defined; integer shifts preserve definedness. Correct-answer refs are absent in two raw records.

### q-29382

If $\tan x = 2$, for some value of $x$, find the value of $2\tan (x - 4π) - 1$.

Parameters: `{"v": "2", "a": "2", "b": "-1", "n": -4}`. Field: `selection`, radio, five complete scalar answers.

**No worked solution in the snapshot.**

### q-66218

If $\tan x = 4$, for some value of $x$, find the value of $\tan (x + 7π)$.

Parameters: `{"v": "4", "a": "1", "b": "0", "n": 7}`. Field: `selection`, radio, five complete scalar answers.

**No worked solution in the snapshot.**

### q-103307

If $tan⁡x=\frac{1}{3},$ for some value of $x,$ find the value of $12tan⁡(x+5\pi )-6.$

Parameters: `{"v": "1/3", "a": "12", "b": "-6", "n": 5}`. Field: `selection`, radio, five complete scalar answers.

The period of $y=tan⁡x$ is $\pi .$ Therefore, for any integer $n,$ we have

$$
tan⁡x=tan⁡(x+n\pi ).
$$

Substituting $n=5$ into the above gives

$$
\begin{aligned}tan⁡x=tan⁡(x+5\cdot \pi )=tan⁡(x+5\pi ).\end{aligned}
$$

Since $tan⁡x=\frac{1}{3},$ we get that $tan⁡(x+5\pi )=\frac{1}{3}.$ Therefore

$$
12tan⁡(x+5\pi )-6=12(\frac{1}{3})-6=4-6=-2.
$$

### q-103312

If $tan⁡x=16,$ for some value of $x,$ find the value of $\frac{3}{4}tan⁡(x-9\pi ).$

Parameters: `{"v": "16", "a": "3/4", "b": "0", "n": -9}`. Field: `selection`, radio, five complete scalar answers.

The period of $y=tan⁡x$ is $\pi .$ Therefore, for any integer $n,$ we have

$$
tan⁡x=tan⁡(x+n\pi ).
$$

Substituting $n=-9$ into the above gives

$$
\begin{aligned}tan⁡x=tan⁡(x+(-9)\cdot \pi )=tan⁡(x-9\pi ).\end{aligned}
$$

Since $tan⁡x=16,$ we get that $tan⁡(x-9\pi )=16.$ Therefore

$$
\frac{3}{4}tan⁡(x-9\pi )=\frac{3}{4}(16)=12.
$$

### q-66594

If $tan⁡x=\sqrt{3},$ for some $x$, find the value of $tan⁡(x-5\pi ).$

Parameters: `{"v": "sqrt(3)", "a": "1", "b": "0", "n": -5}`. Field: `selection`, radio, five complete scalar answers.

The period of $y=tan⁡x$ is $\pi .$ Therefore, for integer $n$ we have

$$
tan⁡x=tan⁡(x+n\pi ).
$$

Substituting $n=-5$ into the right-hand-side of the above gives

$$
\begin{aligned}tan⁡x=tan⁡(x+(-5)\cdot \pi )=tan⁡(x-5\pi ).\end{aligned}
$$

Therefore, if $tan⁡x=\sqrt{3},$ we get that $tan⁡(x-5\pi )=\sqrt{3}.$

### q-70998

If $tan⁡x=3,$ for some $x$, find the value of $tan⁡(x+5\pi )+2.$

Parameters: `{"v": "3", "a": "1", "b": "2", "n": 5}`. Field: `selection`, radio, five complete scalar answers.

The period of $y=tan⁡x$ is $\pi .$ Therefore, for integer $n$ we have

$$
tan⁡x=tan⁡(x+n\pi ).
$$

Substituting $n=5$ into the right-hand-side of the above gives

$$
\begin{aligned}tan⁡x=tan⁡(x+5\cdot \pi )=tan⁡(x+5\pi ).\end{aligned}
$$

Therefore, if $tan⁡x=3,$ we get that $tan⁡(x+5\pi )=3.$

Finally, then

$$
tan⁡(x+5\pi )+2=(3)+2=5.
$$

### q-71002

If $tan⁡x=\sqrt{2},$ for some $x$, find the value of $tan⁡(x-11\pi ).$

Parameters: `{"v": "sqrt(2)", "a": "1", "b": "0", "n": -11}`. Field: `selection`, radio, five complete scalar answers.

The period of $y=tan⁡x$ is $\pi .$ Therefore, for integer $n$ we have

$$
tan⁡x=tan⁡(x+n\pi ).
$$

Substituting $n=-11$ into the right-hand-side of the above gives

$$
\begin{aligned}tan⁡x=tan⁡(x+(-11)\cdot \pi )=tan⁡(x-11\pi ).\end{aligned}
$$

Therefore, if $tan⁡x=\sqrt{2},$ we get that $tan⁡(x-11\pi )=\sqrt{2}.$

## Stage 2: generalized family

Given tan(x)=v, use tan(x+nπ)=tan(x)=v and evaluate a·v+b. Direct uses a=1,b=0; additive uses a=1,b≠0; scaling uses nonunit a,b=0; affine uses nonunit a,b≠0. The distinct source shared sentences, comma placements, function token style and arithmetic stages are retained in explicit replay. Normal authored output changes the source's Unicode `tan⁡` token into standard `	an ` only. It retains the same formal identity, substituted-integer identity, value substitution and family-specific final arithmetic chain. No chosen distractor changes the solution.

## Stage 3: component and complete-bank mapping

The following exact operation formulas reproduce every displayed scalar. They are explicit parameterizations of observed forms, not claims to recover the original error-generation code. In particular, a singleton constant, π coefficient or squared radical can fit several explanations. Every observed profile is evidence-only; the normal bank is separately authored. `anum` and `aden` are the reduced numerator and denominator of a. Each row belongs to the complete five-entry source bank; no pooled option picking occurs.

### q-29382

| Original choice | Parameterized operation | Match | Source designation |
|---|---|---|---|
| `2 + 4π` | `-pi*n + v` | exact mathematical value | absent |
| `-1` | `b` | exact mathematical value | absent |
| `4π` | `-pi*n` | exact mathematical value | absent |
| `3` | `a*v + b` | exact mathematical value | absent |
| `5` | `a*v - b` | exact mathematical value | absent |

The uniquely correct derived value is `3`. That designation is independently inferred for completed practice; raw replay omits it.

### q-66218

| Original choice | Parameterized operation | Match | Source designation |
|---|---|---|---|
| `\frac{1}{4}` | `1/v` | exact mathematical value | absent |
| `1` | `1` | exact mathematical value | absent |
| `4` | `v` | exact mathematical value | absent |
| `-4` | `-v` | exact mathematical value | absent |
| `-\frac{1}{4}` | `-1/v` | exact mathematical value | absent |

The uniquely correct derived value is `4`. That designation is independently inferred for completed practice; raw replay omits it.

### q-103307

| Original choice | Parameterized operation | Match | Source designation |
|---|---|---|---|
| `-2` | `a*v + b` | exact mathematical value | correct |
| `4` | `a*v` | exact mathematical value | wrong |
| `2` | `-a*v - b` | exact mathematical value | wrong |
| `4\pi -2` | `a*v + pi*a*v + b` | exact mathematical value | wrong |
| `6` | `-b` | exact mathematical value | wrong |

The uniquely correct derived value is `-2`. The captured designation agrees with the derivation.

### q-103312

| Original choice | Parameterized operation | Match | Source designation |
|---|---|---|---|
| `4` | `v/aden` | exact mathematical value | wrong |
| `12` | `a*v` | exact mathematical value | correct |
| `12-3\pi ` | `a*v + pi*n/anum` | exact mathematical value | wrong |
| `12+\pi ` | `a*v + pi` | exact mathematical value | wrong |
| `15` | `a*v + anum` | exact mathematical value | wrong |

The uniquely correct derived value is `12`. The captured designation agrees with the derivation.

### q-66594

| Original choice | Parameterized operation | Match | Source designation |
|---|---|---|---|
| `\sqrt{3}+2\pi ` | `v + 2*pi` | exact mathematical value | wrong |
| `-1` | `-1` | exact mathematical value | wrong |
| `-\sqrt{3}` | `-v` | exact mathematical value | wrong |
| `\sqrt{3}` | `v` | exact mathematical value | correct |
| `\frac{\sqrt{3}}{2}` | `v/2` | exact mathematical value | wrong |

The uniquely correct derived value is `\sqrt{3}`. The captured designation agrees with the derivation.

### q-70998

| Original choice | Parameterized operation | Match | Source designation |
|---|---|---|---|
| `5-5\pi ` | `b - pi*n + v` | exact mathematical value | wrong |
| `5\pi ` | `pi*n` | exact mathematical value | wrong |
| `2` | `b` | exact mathematical value | wrong |
| `-1` | `b - v` | exact mathematical value | wrong |
| `5` | `b + v` | exact mathematical value | correct |

The uniquely correct derived value is `5`. The captured designation agrees with the derivation.

### q-71002

| Original choice | Parameterized operation | Match | Source designation |
|---|---|---|---|
| `-\sqrt{2}` | `-v` | exact mathematical value | wrong |
| `-2` | `-v**2` | exact mathematical value | wrong |
| `2` | `v**2` | exact mathematical value | wrong |
| `\sqrt{2}-11\pi ` | `pi*n + v` | exact mathematical value | wrong |
| `\sqrt{2}` | `v` | exact mathematical value | correct |

The uniquely correct derived value is `\sqrt{2}`. The captured designation agrees with the derivation.

## Stage 4: reusable templates and constraints

All mathematical slots are complete components: given v; shift x±|n|π; integer multiplier `(n)·π` when negative; entire scalar coefficient a; entire offset b; product a·v and collected answer. No blind replacement of short numerals or variable letters is used. Signed outside coefficients are grouped. Substitution products retain visible parentheses, so adjacent numbers cannot merge. The final product-before-collection row is preserved for affine questions. Direct and additive sources use their original “Therefore, if …” and “Finally, then” wording; scale/affine use their original “Since … Therefore” wording.

Normal banks are chosen whole, before parameters, with five required expressions:

| Workload | Complete authored bank |
|---|---|
| Direct | v; 1/v; -v; -1/v; v+nπ |
| Additive | v+b; v; b; -v+b; v+nπ+b |
| Scaling | av; v; v/a; -av; a(v+nπ) |
| Affine | av+b; av; av-b; a+bv; a(v+nπ)+b |

The operations arise from the printed method: reciprocating tangent as cotangent, applying an erroneous sign change, adding the angle shift outside tangent, omitting the outside scaling/offset, dividing rather than multiplying, reversing the offset sign, or exchanging coefficient and offset roles. No learner-facing distractor diagnosis is invented. These are authored error operations, not inferred source intent.

A collision, a second mathematically correct option, an invalid scalar or a missing required option rejects the entire sampled instance. Explicit invalid parameters raise an error and are never resampled. Stable IDs use the actual prompt, fixed solution, complete displayed bank, difficulty and source key-presence state; option order and seed do not affect identity. Mathematical fingerprints use the given value and requested affine operation plus difficulty. Integer shift magnitude, function-token style and bank profile are excluded as incidental to the mathematical task.

## Scope and all three levels

Lesson order is reconstructed from activity first-step and step/next: introduction → describing tangent → periodicity tutorial → **this KP** → oddness tutorial → oddness KP. The sole key prerequisite is **Periodic Functions** (topic 17592186049353 / MA 2148). Therefore negative x, oddness, quarter-period identities, evaluating tangent at familiar angles, solving trig equations and tangent addition formulas are excluded.

Easy: integer v with 2≤|v|≤16, a=1,b=0. Exactly one integer-period substitution, anchored to canonical e-11005 and unrated q-66218. The given integer bound matches observed integer 16 elsewhere in this same KP. Moderate uses unordered equivalent-workload families observed here: familiar roots ±√k (k=2,3,5,6,7); integer additive v (2≤|v|≤9), 1≤|b|≤6; fractional scaling (denominator 2–4, numerator magnitude ≤3) of an integer value |v|≤16, with an integral product; affine integer coefficient 2≤|a|≤12, reduced given numerator magnitude ≤8 and denominator ≤4, integral |av|≤24, nonzero integer offset |b|≤6. The normalized affine legacy name is a presentation alias, not an extra substantive family.

Hard: authored noninteger rational a and v, reduced denominators 2–4, reduced numerator magnitude ≤6, noninteger av, integer 1≤|b|≤5. Every item requires the same period substitution, rational multiplication and rational offset collection. It adds arithmetic demand already represented by moderate scaling/offsets, without adding a trigonometric property. Inputs that cancel to an integer product or omit the offset are rejected. All levels use nonzero integer n of magnitude ≤12. These domains are finite; integer-shift, spelling and profile aliases do not inflate task counts. `variety.json` enumerates substantive parameter tasks in the supported domains before counting seeds.

## Missing-data fidelity and independent evidence

The owning MA widget capture at `/home/jake/Developer/MA/DATA/Lessons/3558/Source/3558.json` confirms q-29382 and q-66218 are ordinary five-choice widgets without captured solutions or correctness. q-29382's last two choices are ordered differently there; source matching treats radio order as incidental. There is no evidence of a mathematical source error. Missing refs and solutions are retained raw, with independently derived values 3 and 4 used only in explicitly authored completion. IDs are new field-owned UUIDs for review records; captured DB/MA identifiers remain in raw `source.json` and case provenance. No fake MA identifier is minted. Presence parity is enforced for difficulty, worked solution, answer fields and correct refs.

Plots: none. Steps 5/7 need no renderer; the tutorial graph is not copied into practice questions. Work stops before registration or database preparation.

