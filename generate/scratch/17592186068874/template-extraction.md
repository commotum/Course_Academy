# Template extraction

## 1. Describe each source before generalizing

### q-140276

Rewrite the expression $(x^{2} - 12x + 6^{2}) - 10$ as the difference between a perfect square and a constant.

Variable x; positive half-coefficient a=6; leading square factor b=1; negative linear coefficient 12; perfect-square inner constant 36; outer signed constant -10. Layout `radio_spaced`, stage sequence `power`, field type `radio`. Raw absent attributes: difficulty, solution, correct.

### q-250431

Rewrite the following expression as the sum of a perfect square and a constant.$(x^{2} - 14x + 7^{2}) + 2 = ($ {{field-1}} $)^{2} +$
{{field-2}}

Variable x; positive half-coefficient a=7; leading square factor b=1; negative linear coefficient 14; perfect-square inner constant 49; outer signed constant 2. Layout `blank_spaced`, stage sequence `power`, field type `blank`. Raw absent attributes: difficulty, solution, correct, choices.

### q-140277

Rewrite the expression $({y}^{2}-6y+{3}^{2})+6$ as the sum of a perfect square and a constant.

Variable y; positive half-coefficient a=3; leading square factor b=1; negative linear coefficient 6; perfect-square inner constant 9; outer signed constant 6. Layout `radio_power`, stage sequence `power`, field type `radio`. Raw absent attributes: none.

### q-140279

Rewrite the expression $({y}^{2}-4y+4)+1$ as the sum of a perfect square and a constant.

Variable y; positive half-coefficient a=2; leading square factor b=1; negative linear coefficient 4; perfect-square inner constant 4; outer signed constant 1. Layout `radio_numeric`, stage sequence `numeric`, field type `radio`. Raw absent attributes: none.

### q-140281

Rewrite the expression $({x}^{2}-10x+25)+1$ as the sum of a perfect square and a constant.

Variable x; positive half-coefficient a=5; leading square factor b=1; negative linear coefficient 10; perfect-square inner constant 25; outer signed constant 1. Layout `radio_numeric`, stage sequence `numeric`, field type `radio`. Raw absent attributes: none.

### q-140283

Rewrite the expression $({x}^{2}-22x+121)-4$ as the difference between a perfect square and a constant.

Variable x; positive half-coefficient a=11; leading square factor b=1; negative linear coefficient 22; perfect-square inner constant 121; outer signed constant -4. Layout `radio_numeric`, stage sequence `numeric`, field type `radio`. Raw absent attributes: none.

### q-235868

Rewrite the following expression as the sum of a perfect square and a constant.

$({x}^{2}-8x+16)+5=(${{field-1}}${)}^{2}\,+$
{{field-2}}

Variable x; positive half-coefficient a=4; leading square factor b=1; negative linear coefficient 8; perfect-square inner constant 16; outer signed constant 5. Layout `blank_numeric`, stage sequence `direct`, field type `blank`. Raw absent attributes: none.

### q-250428

Rewrite the following expression as the sum of a perfect square and a constant.

$({x}^{2}-18x+81)+2=(${{field-1}}${)}^{2}\,+$
{{field-2}}

Variable x; positive half-coefficient a=9; leading square factor b=1; negative linear coefficient 18; perfect-square inner constant 81; outer signed constant 2. Layout `blank_numeric`, stage sequence `direct`, field type `blank`. Raw absent attributes: none.

## 2. Shared mathematical pattern

An already-isolated negative-linear perfect-square trinomial $(v^2-2av+a^2)+c$ is rewritten as $(v-a)^2+c$. Recall the negative-sign identity, recognize the positive root a from half the linear coefficient and the perfect-square constant, factor the parenthesized trinomial, and restore the unchanged outer signed constant. Radio responses are complete expressions; blanks are the linear component and positive outside magnitude. No square is inserted and no compensating constant is subtracted.

## 3. Components and every observed choice

The prompt components are the variable, the negative cross coefficient, the inner square presented as a number or explicit power, and the signed outer constant. The source shared sentences are:

> First, we recall the following formula:

> Notice that we have a perfect square in the parentheses that we can factor as follows:

> Therefore, we obtain

All solutions first recall `v²−2av+a²=(v−a)²`. `power` and `direct` contain three factoring rows: displayed trinomial → explicit `−2·a v` and `a²` → `(v−a)²`. `numeric` contains four rows, inserting the numerical square-root recognition row. The final two-row chain preserves the whole original expression and its complete factored result. Blank `direct` sources do not acquire the otherwise redundant square-root row. Raw q-140276/q-250431 have no solution; normal completions author the corresponding power sequence using these same sentences.

### q-140276 component bank

Profile: `half_coefficient`. Public evidence replay: `raw_q-140276`. Parameters `{"a": 6, "b": 1, "c": -10, "variable": "x"}`.

| Field | Exact captured value | Captured correct? | Parameterized operation |
|---|---|---|---|
| selection | `(x - 6)^{2} - 10` | absent | subtract half the linear coefficient: (bv−a)²+c |
| selection | `(x + 6)^{2} - 10` | absent | wrong sign of square-root factor: (bv+a)²+c |
| selection | `(x - 12)^{2} - 10` | absent | use the full cross-coefficient half-factor as shift: (bv−2a)²+c |
| selection | `(x - 3)^{2} - 10` | absent | halve the required half-coefficient again: (bv−a/2)²+c |
| selection | `(x + 12)^{2} - 10` | absent | use the full half-factor with wrong sign: (bv+2a)²+c |

Each displayed source option matches one parameterized generated option exactly, including complete expression and original math answer type. Omitted correct keys remain omitted in raw replay; any mathematical inference is separately authored.

### q-250431 component bank

Profile: `None`. Public evidence replay: `raw_q-250431`. Parameters `{"a": 7, "b": 1, "c": 2, "variable": "x"}`.

| Field | Exact captured value | Captured correct? | Parameterized operation |
|---|---|---|---|
| field-1 | absent | designation absent | authored completion `x-7` |
| field-2 | absent | designation absent | authored completion `2` |

Each displayed source option matches one parameterized generated option exactly, including complete expression and original math answer type. Omitted correct keys remain omitted in raw replay; any mathematical inference is separately authored.

### q-140277 component bank

Profile: `both_constant_signs`. Public evidence replay: `raw_q-140277`. Parameters `{"a": 3, "b": 1, "c": 6, "variable": "y"}`.

| Field | Exact captured value | Captured correct? | Parameterized operation |
|---|---|---|---|
| selection | `(y+3{)}^{2}+6` | False | wrong sign of square-root factor: (bv+a)²+c |
| selection | `(y-9{)}^{2}+6` | False | use the inner squared constant directly as shift: (bv−a²)²+c |
| selection | `(y-3{)}^{2}+6` | True | subtract half the linear coefficient: (bv−a)²+c |
| selection | `(y-6{)}^{2}+6` | False | use the full cross-coefficient half-factor as shift: (bv−2a)²+c |
| selection | `(y+9{)}^{2}+6` | False | use inner squared constant directly with wrong sign: (bv+a²)²+c |

Each displayed source option matches one parameterized generated option exactly, including complete expression and original math answer type. Omitted correct keys remain omitted in raw replay; any mathematical inference is separately authored.

### q-140279 component bank

Profile: `half_coefficient`. Public evidence replay: `raw_q-140279`. Parameters `{"a": 2, "b": 1, "c": 1, "variable": "y"}`.

| Field | Exact captured value | Captured correct? | Parameterized operation |
|---|---|---|---|
| selection | `(y-1{)}^{2}+1` | False | halve the required half-coefficient again: (bv−a/2)²+c |
| selection | `(y-2{)}^{2}+1` | True | subtract half the linear coefficient: (bv−a)²+c |
| selection | `(y+4{)}^{2}+1` | False | use the full half-factor with wrong sign: (bv+2a)²+c |
| selection | `(y-4{)}^{2}+1` | False | use the full cross-coefficient half-factor as shift: (bv−2a)²+c |
| selection | `(y+2{)}^{2}+1` | False | wrong sign of square-root factor: (bv+a)²+c |

Each displayed source option matches one parameterized generated option exactly, including complete expression and original math answer type. Omitted correct keys remain omitted in raw replay; any mathematical inference is separately authored.

### q-140281 component bank

Profile: `square_constant`. Public evidence replay: `raw_q-140281`. Parameters `{"a": 5, "b": 1, "c": 1, "variable": "x"}`.

| Field | Exact captured value | Captured correct? | Parameterized operation |
|---|---|---|---|
| selection | `(x-5{)}^{2}+1` | True | subtract half the linear coefficient: (bv−a)²+c |
| selection | `(x+5{)}^{2}+1` | False | wrong sign of square-root factor: (bv+a)²+c |
| selection | `(x-25{)}^{2}+1` | False | use the inner squared constant directly as shift: (bv−a²)²+c |
| selection | `(x-10{)}^{2}+1` | False | use the full cross-coefficient half-factor as shift: (bv−2a)²+c |
| selection | `(x+10{)}^{2}+1` | False | use the full half-factor with wrong sign: (bv+2a)²+c |

Each displayed source option matches one parameterized generated option exactly, including complete expression and original math answer type. Omitted correct keys remain omitted in raw replay; any mathematical inference is separately authored.

### q-140283 component bank

Profile: `adjacent_opaque`. Public evidence replay: `raw_q-140283`. Parameters `{"a": 11, "b": 1, "c": -4, "variable": "x"}`.

| Field | Exact captured value | Captured correct? | Parameterized operation |
|---|---|---|---|
| selection | `(x+12{)}^{2}-4` | False | observed structural pattern (bv+(a+1))²+c; error intention unresolved |
| selection | `(x-11{)}^{2}-4` | True | subtract half the linear coefficient: (bv−a)²+c |
| selection | `(x-12{)}^{2}-4` | False | observed structural pattern (bv−(a+1))²+c; error intention unresolved |
| selection | `(x-22{)}^{2}-4` | False | use the full cross-coefficient half-factor as shift: (bv−2a)²+c |
| selection | `(x+11{)}^{2}-4` | False | wrong sign of square-root factor: (bv+a)²+c |

Each displayed source option matches one parameterized generated option exactly, including complete expression and original math answer type. Omitted correct keys remain omitted in raw replay; any mathematical inference is separately authored.

### q-235868 component bank

Profile: `None`. Public evidence replay: `raw_q-235868`. Parameters `{"a": 4, "b": 1, "c": 5, "variable": "x"}`.

| Field | Exact captured value | Captured correct? | Parameterized operation |
|---|---|---|---|
| field-1 | `x-4` | True | linear fragment bv−a |
| field-2 | `5` | True | positive outer magnitude abs(c) |

Each displayed source option matches one parameterized generated option exactly, including complete expression and original math answer type. Omitted correct keys remain omitted in raw replay; any mathematical inference is separately authored.

### q-250428 component bank

Profile: `None`. Public evidence replay: `raw_q-250428`. Parameters `{"a": 9, "b": 1, "c": 2, "variable": "x"}`.

| Field | Exact captured value | Captured correct? | Parameterized operation |
|---|---|---|---|
| field-1 | `x-9` | True | linear fragment bv−a |
| field-2 | `2` | True | positive outer magnitude abs(c) |

Each displayed source option matches one parameterized generated option exactly, including complete expression and original math answer type. Omitted correct keys remain omitted in raw replay; any mathematical inference is separately authored.

## 4. Reusable masks, constraints and extensions

Five observed prompt/solution masks are implemented; radio_numeric is reused at its observed easy and moderate ratings. Spaced legacy source masks preserve their full original layout. Masks operate on complete components, never arbitrary substring substitution. Values use source braced closing-parenthesis notation and delimiter-free answer strings. Signed outer terms are constructed once; no ungrouped double minus or plus-minus token is emitted. Choice banks are complete profiles chosen before parameters, with whole-bank collision rejection. Square-constant profiles exclude a=2 because a²=2a collides; half-coefficient banks retain exact rational distractors where a is odd. Fractions in wrong options do not change the even negative prompt coefficient or assessed operation.

Normal default generation samples every source-shaped eligible family and defensible complete bank. Moderate numeric solutions match the observed sequence at a=11, c=−4, while authored bank choice removes the unexplained adjacent-offset pattern. The public raw profile still reproduces all five original adjacent-bank values at original or changed a; its metadata explicitly states evidence-only/ineligible and unresolved intention.

Easy a=2..9 and b=1 requires one familiar monic negative-linear identity. Moderate a=10..15 and b=1 reflects the observed larger integer square 121 and larger even coefficient 22; it preserves the same operation count. The two legacy unrated sources are authored easy assignments because their a=6,7 match observed easy bounds. Normal moderate variants of the other source masks are authored extensions, not recovered labels.

Hard has no observations. The lesson route follows activity first-step 17592186069834 and each step/next: introduction → sibling 68873 already-isolated positive squares → own 68874 → tutorial introducing the later add/subtract trick → general expression siblings 68875/68876. Prerequisite topic 352 is Factoring Perfect Square Trinomials, confirmed by captured MA widget. The inspected prerequisite capture `prerequisite-352.json` teaches monic integer squares and monic fractional squares (for example y²+(2/5)y+1/25 and x²+x+1/4); it does not contain an observed nonunit-leading example. Hard adds a nonunit squared variable factor `(b v)²` inside an already-isolated perfect-square trinomial by substituting b v for the identity variable. This is an explicitly authored applicability inference, not a recovered prerequisite question: matching both roots and the negative cross product is harder recognition of that same identity. It does not borrow the later add/subtract trick or the downstream odd-linear/equation-solving topics. Use coprime a=2..9, b=2..5 to prevent a common scale reducing the intended factor-recognition demand. Every hard instance has this same workload; radio/blank are unordered layouts.

The authored hard factoring chain is displayed trinomial → `(b v)²−2·a·(b v)+a²` → `(b v−a)²`, then the original complete expression → factored expression with unchanged c. Shared source prose and recalled identity remain. Its complete radio bank uses the correct result, wrong inner sign, failure to halve the cross factor, omitted variable factor, and the squared leading coefficient used instead of its root. The latter two apply to the nonunit squared-factor recognition operation.

Both signs of the outer nonzero integer magnitude 1..12 are allowed in every normal family; subtractive blanks expect positive magnitude because the prompt supplies the minus. All displayed inner constants remain perfect squares. Explicit inputs obey the same level bounds and full-bank validity conditions as sampling; invalid inputs raise without replacement. Both radio and blank selectors filter family eligibility before choosing; unsupported selectors fail explicitly.

Meaningful task fingerprints use a,b,c and assessed method, excluding variable-letter aliases, response layout, profile, bank, seed and option order. Full content identities retain displayed prompt, fixed solution and its presence, difficulty and its presence, field type, complete displayed bank and its presence, correct designation and its presence. Changed bank values produce changed content identities. There are 192 easy, 144 moderate and 480 hard meaningful parameter tasks before notation/bank variants.

Fidelity: 8/8 prompts; 6/6 present solutions; 29/29 bank option values, including 20/20 distractors and 5/5 complete radio banks; 8/8 present field correct designations. Missing one radio and two blank designations are inferred only in normal completions. Raw attribute-presence parity is checked for each source individually. No annotation absence is counted as a recovered observation. All raw replay records remain evidence-only.

No plots: source captures contain only formula text and response widgets. Plot extraction/generation require no assets or rendering. Native grading and independently parsed display mathematics remain separate evidence; native tests include original complete banks, authored completions, all three levels, equivalent unsimplified blank fragments and incorrect entries. See validation.json and native-report.json.


## Inventory production scope, 2026-10-14

This production revision supersedes the earlier authored hard and alternate moderate layout claims. Easy retains monic observed layouts; moderate supports only `radio_numeric` and the complete q-140283 `adjacent_opaque` profile. Its recipes use offsets a, -a, a+1, 2a and -(a+1), all with the same outer constant. They reproduce every observed choice at a=11,c=-4, and changed values preserve distinct whole expressions and a unique correct square. The error intention remains unresolved; a label is not needed to reproduce the observed mathematical pattern. Moderate a=10..15 is a conservative same-method sampling range around a=11. Hard is unsupported by this bounded package: b>1 changes the monic expression backbone and introduces an unobserved variable-factor recognition stage. The script rejects that level. See `capability.json`.
