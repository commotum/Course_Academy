# Four-stage template extraction

## 1. Specific source analysis

Every source is described below, including its exact prompt, primitive parameters, answer types, full observed choice mapping and ordered mathematical rows. source.json preserves every raw field; review.md preserves full original solution prose. No source question is omitted. The source-case order here has no pedagogical progression.

## 2. Shared pattern

Factor the numerator and denominator, cancel their greatest common polynomial factor, and identify the entire set of real zeros of the reduced denominator. The original domain excludes all original denominator zeros. A removed zero is a hole only when no denominator factor remains there. Responses are numeric root fragments in blank fields or complete root sets in radio fields. Every supported family has a nontrivial common factor and at least one surviving real pole.

## 3. Components and bank profiles

Each per-source specialization preserves its exact Markdown mask: complete math blocks are slots, prose and delimiters are fixed. Every source choice is retained in its source field and value type. The six complete observed radio banks have evidence_only=true and eligible_for_learning=false, even where a plausible root operation can describe several members. Independent opaque slots make interpretation limits explicit; they are not fitted distractor formulas and never enter normal sampling. Profiles are chosen whole before parameter sampling; all five required values are computed and any root-set equivalence/collision rejects the entire instance.

## 4. Reusable mask and calculations

The generator builds ordered unsimplified numerator/denominator components, factored components, explicit cancellation components and reduced components. For grouping, it preserves six rows: original cubic; common-binomial grouping; difference-of-squares grouping; complete linear factors; cancellation; reduced quotient. The cube family preserves five rows, including splitting its cube into one cancelled factor and a remaining square. The easy supplied-factors family preserves three rows. All other families preserve four rows. Only the final reduced expression uses CAS cancellation; structural masks carry the preceding teaching operations.

Fixed prose comes from each source solution, including omission of “solve for x” in q-39931 and trailing spaces in q-269990/q-278545. Source solutions absent in the three unrated captures use the canonical factor/cancel/set-denominator/solve wording with all intermediate rows. Source prompt math, denominator equation and every prose root occurrence derive from the same parameters; no substring replacement touches function arguments or arbitrary prose.

### Scope and finite sampling policy

All independent variables/function names remain actual source x and f. Easy supplied-factors: cancellation and remaining roots are integers |a|≤6, |b|≤8, distinct; the literal x-factor variant fixes a=0. Moderate monic quadratics retain nonzero constant and middle terms; monomial family retains exactly x² as common factor and a nonzero surviving root |b|≤8. Moderate nonmonic common factors m x+n have 2≤m≤4, 1≤|n|≤5, gcd(m,n)=1; remaining integer root has 1≤|b|≤6, differs from −n/m and preserves a nonzero middle coefficient. Thus nonunit coefficients cannot reduce to a monic/integer-root task.

Moderate cubic grouping fixes denominator (x²−a²)(x−b), 1≤a≤4, 1≤|b|≤8, b≠±a, and linear numerator x+a. Hard cubic grouping uses the same bounded cubic plus quadratic numerator (x−c)(x+a), 1≤|c|≤6, c distinct from all denominator roots and nonzero numerator middle coefficient. Hard quadratic ratios use three distinct nonzero integer roots |a|,|c|≤6, |b|≤8, with nonzero middle terms in both quadratics. Hard cube retains a nonzero cubic perfect-power root 1≤|a|≤4 and distinct nonzero repeated pole 1≤|b|≤8. Hard difference-of-squares family preserves x² as surviving denominator, with 1≤a≤6. These guards apply identically to explicit calls and random sampling, including primitive/reduced requirements.

No difficulty is missing in the capture. Extensions provide deterministic signed/root choices and separate normal complete radio banks; they do not introduce complex roots, discriminants, holes-coordinate calculations, higher degrees or a within-level progression. Narrow zero-pole families have genuinely finite variation (six meaningful square magnitudes for q-39931; sixteen nonzero shifts in the zero-pole linear family). Variable aliases and opaque evidence slots do not inflate mathematical-task counts.

### Normal method bank

The five root-set operations are: the full reduced denominator zero set; all removed original-domain zeros; all original denominator zeros; the empty set; sign-reversed surviving roots. When the surviving set is {0}, the final member is the sign-reversed removed-root set. Every whole bank must have five distinct sets and exactly one correct set, otherwise the entire instance is rejected. This is an authored default bank, not claimed recovered source intent. Displayed complete sets are independently re-read in validation and native grade checks submit every option. Blank checks submit an independently unevaluated linear or quadratic root formula and a wrong number.

### Evidence versus completions

Public raw profile keeps q-39800/q-39801/q-80690 without refs and solutions, and q-39802 without fields. Completed observed profile derives the missing correct root sets and adds q-39802 two ascending-order blanks. These changes have distinct denominators: original refs 10/10 matched, inferred refs 3/3 correct; original solutions 10/10 exact, authored missing solutions 3; raw prompts/layouts 13/13 exact, fieldless completion 1. No mathematical source error or proven escape anomaly exists. q-39804 uses balanced but unconventional parenthesis brace placement, exactly retained for replay and normalized in normal output.


## q-278535 — factored

Original label: :question.difficulty/easy. Generator level: easy. Plot rating: none.

The vertical asymptote of $f(x)=\frac{x-1}{(x+2)(x-1)}$ is $x=${{field-1}}.

Primitive parameters: `{"a": 1, "b": -2}`.

Original domain exclusions: -2, 1. Remaining pole set: -2. Removed zeros/holes: 1.

Observed ordered rational-expression stages:

1. $\frac{x-1}{(x+2)(x-1)}$

2. $\frac{\cancel{x-1}}{(x+2)(\cancel{x-1})}$

3. $\frac{1}{x+2}$

Field `field-1` — :answer-field.type/blank

| Original complete value | Value type | Recipe/slot | Original designation |

|---|---|---|---|

| `-2` | :answer.type/math | ordered remaining numeric root fragment field-1 | correct |


## q-80690 — factored_zero

Original label: unrated. Generator level: easy (authored assignment). Plot rating: none.

Calculate the vertical asymptotes of $f(x) = (x)/(x(x - 2))$.

Primitive parameters: `{"a": 0, "b": 2}`.

Original domain exclusions: 0, 2. Remaining pole set: 2. Removed zeros/holes: 0.

No captured worked solution; the same stages listed in review.md are authored from the canonical method.

Field `selection` — :answer-field.type/radio

| Original complete value | Value type | Recipe/slot | Original designation |

|---|---|---|---|

| `x = 0, x = 2` | :answer.type/math | original denominator roots {a,b} | absent; not a matched designation |

| `$x = 0$ only` | :answer.type/text | cancelled root a | absent; not a matched designation |

| `$x = 2$ only` | :answer.type/text | remaining pole b | absent; not a matched designation |

| `The function has no vertical asymptotes` | :answer.type/text | empty set | absent; not a matched designation |

| `x =-2, x = 2` | :answer.type/math | observed reflected set {−b,b}; intent unresolved | absent; not a matched designation |


## q-269990 — linear

Original label: :question.difficulty/moderate. Generator level: moderate. Plot rating: none.

The vertical asymptote of $f(x)=\frac{x+3}{{x}^{2}+x-6}$ is $x=${{field-1}}.

Primitive parameters: `{"a": -3, "b": 2}`.

Original domain exclusions: -3, 2. Remaining pole set: 2. Removed zeros/holes: -3.

Observed ordered rational-expression stages:

1. $\frac{x+3}{{x}^{2}+x-6}$

2. $\frac{x+3}{(x+3)(x-2)}$

3. $\frac{\cancel{x+3}}{\cancel{(x+3)}(x-2)}$

4. $\frac{1}{x-2}$

Field `field-1` — :answer-field.type/blank

| Original complete value | Value type | Recipe/slot | Original designation |

|---|---|---|---|

| `2` | :answer.type/math | ordered remaining numeric root fragment field-1 | correct |


## q-39801 — linear_space

Original label: unrated. Generator level: moderate (authored assignment). Plot rating: none.

Determine the vertical asymptotes of $f(x) = \frac{x - 2}{x^{2} + 2x - 8}$.

Primitive parameters: `{"a": 2, "b": -4, "opaque": [-2, 0]}`.

Original domain exclusions: -4, 2. Remaining pole set: -4. Removed zeros/holes: 2.

No captured worked solution; the same stages listed in review.md are authored from the canonical method.

Field `selection` — :answer-field.type/radio

| Original complete value | Value type | Recipe/slot | Original designation |

|---|---|---|---|

| `$x = 2$ only` | :answer.type/text | cancelled root a | absent; not a matched designation |

| `x =-4, x = 2` | :answer.type/math | original denominator roots {b,a} | absent; not a matched designation |

| `x = 2, x = 4` | :answer.type/math | observed sign-reflection shape {a,−b}; intent unresolved | absent; not a matched designation |

| `x =-2, x = 0` | :answer.type/math | independent opaque evidence slots {opaque[0],opaque[1]}; not a recovered error operation | absent; not a matched designation |

| `$x =-4$ only` | :answer.type/text | remaining pole b | absent; not a matched designation |


## q-278556 — nonmonic

Original label: :question.difficulty/moderate. Generator level: moderate. Plot rating: none.

The vertical asymptote of $f(x)=\frac{2x-1}{2{x}^{2}+x-1}$ is $x=${{field-1}}.

Primitive parameters: `{"b": -1, "m": 2, "n": -1}`.

Original domain exclusions: -1, \frac{1}{2}. Remaining pole set: -1. Removed zeros/holes: \frac{1}{2}.

Observed ordered rational-expression stages:

1. $\frac{2x-1}{2{x}^{2}+x-1}$

2. $\frac{2x-1}{(x+1)(2x-1)}$

3. $\frac{\cancel{2x-1}}{(x+1)\cancel{(2x-1)}}$

4. $\frac{1}{x+1}$

Field `field-1` — :answer-field.type/blank

| Original complete value | Value type | Recipe/slot | Original designation |

|---|---|---|---|

| `-1` | :answer.type/math | ordered remaining numeric root fragment field-1 | correct |


## q-278536 — monomial

Original label: :question.difficulty/moderate. Generator level: moderate. Plot rating: none.

The vertical asymptote of $f(x)=\frac{{x}^{2}}{{x}^{3}-2{x}^{2}}$ is $x=${{field-1}}.

Primitive parameters: `{"b": 2}`.

Original domain exclusions: 0, 2. Remaining pole set: 2. Removed zeros/holes: 0.

Observed ordered rational-expression stages:

1. $\frac{{x}^{2}}{{x}^{3}-2{x}^{2}}$

2. $\frac{{x}^{2}}{{x}^{2}(x-2)}$

3. $\frac{\cancel{{x}^{2}}}{\cancel{{x}^{2}}(x-2)}$

4. $\frac{1}{x-2}$

Field `field-1` — :answer-field.type/blank

| Original complete value | Value type | Recipe/slot | Original designation |

|---|---|---|---|

| `2` | :answer.type/math | ordered remaining numeric root fragment field-1 | correct |


## q-278545 — grouped_linear

Original label: :question.difficulty/moderate. Generator level: moderate. Plot rating: none.

In **ascending order**, the vertical asymptotes of $f(x)=\frac{x+2}{{x}^{3}-{x}^{2}-4x+4}$ are

$x=$
{{field-1}} $\,$ and $\,x=$
{{field-2}}.

Primitive parameters: `{"a": 2, "b": 1}`.

Original domain exclusions: -2, 1, 2. Remaining pole set: 1, 2. Removed zeros/holes: -2.

Observed ordered rational-expression stages:

1. $\frac{x+2}{{x}^{3}-{x}^{2}-4x+4}$

2. $\frac{x+2}{{x}^{2}(x-1)-4(x-1)}$

3. $\frac{x+2}{({x}^{2}-4)(x-1)}$

4. $\frac{x+2}{(x-2)(x+2)(x-1)}$

5. $\frac{\cancel{x+2}}{(x-2)\cancel{(x+2)}(x-1)}$

6. $\frac{1}{(x-2)(x-1)}$

Field `field-2` — :answer-field.type/blank

| Original complete value | Value type | Recipe/slot | Original designation |

|---|---|---|---|

| `2` | :answer.type/math | ordered remaining numeric root fragment field-2 | correct |

Field `field-1` — :answer-field.type/blank

| Original complete value | Value type | Recipe/slot | Original designation |

|---|---|---|---|

| `1` | :answer.type/math | ordered remaining numeric root fragment field-1 | correct |


## q-80691 — linear_zero

Original label: :question.difficulty/moderate. Generator level: moderate. Plot rating: none.

Calculate the vertical asymptotes of $f(x)=\frac{x+2}{{x}^{2}+2x}.$

Primitive parameters: `{"a": -2}`.

Original domain exclusions: -2, 0. Remaining pole set: 0. Removed zeros/holes: -2.

Observed ordered rational-expression stages:

1. $\frac{x+2}{{x}^{2}+2x}$

2. $\frac{x+2}{x(x+2)}$

3. $\frac{\cancel{x+2}}{x\cancel{(x+2)}}$

4. $\frac{1}{x}$

Field `selection` — :answer-field.type/radio

| Original complete value | Value type | Recipe/slot | Original designation |

|---|---|---|---|

| `$x=2$ only` | :answer.type/text | observed reflected cancelled root −a | wrong |

| `x=0,\,x=-2` | :answer.type/math | original denominator roots {0,a} | wrong |

| `$x=0$ only` | :answer.type/text | remaining pole 0 | correct |

| `The function has no vertical asymptotes` | :answer.type/text | empty set | wrong |

| `x=-2` | :answer.type/math | cancelled root a | wrong |


## q-278543 — quadratic

Original label: :question.difficulty/hard. Generator level: hard. Plot rating: none.

The vertical asymptote of $f(x)=\frac{{x}^{2}-x-6}{{x}^{2}+x-2}$ is $x=${{field-1}}.

Primitive parameters: `{"a": -2, "b": 1, "c": 3}`.

Original domain exclusions: -2, 1. Remaining pole set: 1. Removed zeros/holes: -2.

Observed ordered rational-expression stages:

1. $\frac{{x}^{2}-x-6}{{x}^{2}+x-2}$

2. $\frac{(x-3)(x+2)}{(x-1)(x+2)}$

3. $\frac{(x-3)\cancel{(x+2)}}{(x-1)\cancel{(x+2)}}$

4. $\frac{x-3}{x-1}$

Field `field-1` — :answer-field.type/blank

| Original complete value | Value type | Recipe/slot | Original designation |

|---|---|---|---|

| `1` | :answer.type/math | ordered remaining numeric root fragment field-1 | correct |


## q-39800 — quadratic_space

Original label: unrated. Generator level: hard (authored assignment). Plot rating: none.

Calculate the vertical asymptotes of $f(x) = \frac{x^{2} - 3x + 2}{x^{2} + x - 2}$.

Primitive parameters: `{"a": 1, "b": -2, "c": 2}`.

Original domain exclusions: -2, 1. Remaining pole set: -2. Removed zeros/holes: 1.

No captured worked solution; the same stages listed in review.md are authored from the canonical method.

Field `selection` — :answer-field.type/radio

| Original complete value | Value type | Recipe/slot | Original designation |

|---|---|---|---|

| `$x =-2$ only` | :answer.type/text | remaining pole b | absent; not a matched designation |

| `$x = 2$ only` | :answer.type/text | residual numerator zero c | absent; not a matched designation |

| `x =-2, x = 1` | :answer.type/math | original denominator roots {b,a} | absent; not a matched designation |

| `$x = 1$ only` | :answer.type/text | cancelled root a | absent; not a matched designation |

| `x = ± 2, x = 1` | :answer.type/math | observed pattern {−|c|,+|c|,a}; intent unresolved | absent; not a matched designation |


## q-39802 — grouped_quadratic

Original label: :question.difficulty/hard. Generator level: hard. Plot rating: none.

Find the vertical asymptotes of $f(x)=\frac{{x}^{2}-x-2}{{x}^{3}+7{x}^{2}-x-7}.$

Primitive parameters: `{"a": 1, "b": -7, "c": 2}`.

Original domain exclusions: -7, -1, 1. Remaining pole set: -7, 1. Removed zeros/holes: -1.

Observed ordered rational-expression stages:

1. $\frac{{x}^{2}-x-2}{{x}^{3}+7{x}^{2}-x-7}$

2. $\frac{(x-2)(x+1)}{{x}^{2}(x+7)-(x+7)}$

3. $\frac{(x-2)(x+1)}{({x}^{2}-1)(x+7)}$

4. $\frac{(x-2)(x+1)}{(x-1)(x+1)(x+7)}$

5. $\frac{(x-2)\cancel{(x+1)}}{(x-1)\cancel{(x+1)}(x+7)}$

6. $\frac{x-2}{(x-1)(x+7)}$

Original field layout is empty. Raw profile preserves it. Authored completion supplies field-1 (minimum pole) and field-2 (maximum pole), with a minimal ascending-order instruction.


## q-39804 — cube

Original label: :question.difficulty/hard. Generator level: hard. Plot rating: none.

Find the vertical asymptotes of $f(x)=\frac{{x}^{3}-3{x}^{2}+3x-1}{(x-1)(x+5{)}^{2}}.$

Primitive parameters: `{"a": 1, "b": -5, "opaque": [0]}`.

Original domain exclusions: -5, 1. Remaining pole set: -5. Removed zeros/holes: 1.

Observed ordered rational-expression stages:

1. $\frac{{x}^{3}-3{x}^{2}+3x-1}{(x-1)(x+5{)}^{2}}$

2. $\frac{(x-1{)}^{3}}{(x-1)(x+5{)}^{2}}$

3. $\frac{(x-1)(x-1{)}^{2}}{(x-1)(x+5{)}^{2}}$

4. $\frac{\cancel{(x-1)}(x-1{)}^{2}}{\cancel{(x-1)}(x+5{)}^{2}}$

5. $\frac{(x-1{)}^{2}}{(x+5{)}^{2}}$

Field `selection` — :answer-field.type/radio

| Original complete value | Value type | Recipe/slot | Original designation |

|---|---|---|---|

| `$x=-5$ only` | :answer.type/text | remaining pole b | correct |

| `x=0,\,x=5` | :answer.type/math | independent opaque slot with reflected pole {opaque[0],−b}; intent unresolved | wrong |

| `x=-5,\,x=1` | :answer.type/math | original denominator roots {b,a} | wrong |

| `$x=1$ only` | :answer.type/text | cancelled root a | wrong |

| `x=-5,\,x=-1,\,x=1` | :answer.type/math | observed shape {b,−a,a}; intent unresolved | wrong |


## q-39931 — squares

Original label: :question.difficulty/hard. Generator level: hard. Plot rating: none.

Determine the vertical asymptotes of the function $f(x)=\frac{{x}^{2}-4}{{x}^{3}+2{x}^{2}}.$

Primitive parameters: `{"a": 2, "opaque": [-1, 1, 0]}`.

Original domain exclusions: -2, 0. Remaining pole set: 0. Removed zeros/holes: -2.

Observed ordered rational-expression stages:

1. $\frac{{x}^{2}-4}{{x}^{3}+2{x}^{2}}$

2. $\frac{(x-2)(x+2)}{{x}^{2}(x+2)}$

3. $\frac{(x-2)\cancel{(x+2)}}{{x}^{2}\cancel{(x+2)}}$

4. $\frac{x-2}{{x}^{2}}$

Field `selection` — :answer-field.type/radio

| Original complete value | Value type | Recipe/slot | Original designation |

|---|---|---|---|

| `$x=1$ only` | :answer.type/text | independent opaque singleton opaque[1] | wrong |

| `The function has no vertical asymptotes` | :answer.type/text | empty set | wrong |

| `x=-1,\,x=1` | :answer.type/math | independent opaque pair {opaque[0],opaque[1]} | wrong |

| `$x=0$ only` | :answer.type/text | independent opaque singleton opaque[2] (the correct 0 at source) | correct |

| `$x=-1$ only` | :answer.type/text | independent opaque singleton opaque[0] | wrong |

## Enumerated normal catalog

The finite primitive parameter domains yield 208 easy, 496 moderate and 2,198 hard mathematical tasks. `catalog.json` records the family enumeration and excluded layout/subset aliases. The cube family rejects eight a=−b cases as whole-bank root-set collisions. Independent opaque evidence slots do not count as normal tasks. Raw key-presence checks separately assert absence of unrated difficulty, absent worked solutions and the fieldless answer-fields attribute.
