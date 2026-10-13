# Template extraction

## Stage 1 — specific observed questions

Each original prompt, field type, entire five-option bank, key, and complete worked solution is reproduced in review.md and remains byte-preserved in source.json. Source-cases.json supplies the public generate API arguments for every original. No source-return lookup branch exists: original and changed cases use the same formula/prose builders and computed intermediate values.

- **q-15595 / coffee / easy**: parameters `{"ambient": 25, "initial": 100, "rate": "0.05", "time": 6}`; field `radio`, key `selection`, correct `${81}^{∘}\text{C}$`. Complete bank: ${83}^{∘}\text{C}$; ${79}^{∘}\text{C}$; ${85}^{∘}\text{C}$; ${81}^{∘}\text{C}$ (correct); ${77}^{∘}\text{C}$.
- **q-107118 / iron / easy**: parameters `{"ambient": 28, "initial": 140, "rate": "0.1", "time": 5}`; field `radio`, key `selection`, correct `${96}^{∘}\text{C}$`. Complete bank: ${96}^{∘}\text{C}$ (correct); ${92}^{∘}\text{C}$; ${79}^{∘}\text{C}$; ${76}^{∘}\text{C}$; ${81}^{∘}\text{C}$.
- **q-107120 / cake / easy**: parameters `{"ambient": 70, "initial": 340, "rate": "0.09", "time": 8}`; field `radio`, key `selection`, correct `${201}^{∘}\text{F}$`. Complete bank: ${198}^{∘}\text{F}$; ${223}^{∘}\text{F}$; ${194}^{∘}\text{F}$; ${201}^{∘}\text{F}$ (correct); ${189}^{∘}\text{F}$.
- **q-107129 / compressor / easy**: parameters `{"ambient": 21, "initial": 65, "rate": "0.12", "time": 8}`; field `radio`, key `selection`, correct `${38}^{∘}\text{C}$`. Complete bank: ${31}^{∘}\text{C}$; ${38}^{∘}\text{C}$ (correct); ${43}^{∘}\text{C}$; ${29}^{∘}\text{C}$; ${58}^{∘}\text{C}$.
- **q-15384 / bath / moderate**: parameters `{"ambient": 10, "initial": 50, "observed": 40, "target": 30, "time": 5}`; field `radio`, key `selection`, correct `$12\,\text{min}$`. Complete bank: $12\,\text{min}$ (correct); $15\,\text{min}$; $13\,\text{min}$; $14\,\text{min}$; $10\,\text{min}$.
- **q-107122 / outside / moderate**: parameters `{"ambient": 15, "initial": 72, "observed": 54, "target": 25, "time": 2}`; field `radio`, key `selection`, correct `$9\,\text{min}$`. Complete bank: $11\,\text{min}$; $15\,\text{min}$; $9\,\text{min}$ (correct); $8\,\text{min}$; $13\,\text{min}$.
- **q-15589 / water / moderate**: parameters `{"ambient": 25, "initial": 100, "observed": 90, "target": 30, "time": 5}`; field `radio`, key `selection`, correct `$95\,\text{min}$`. Complete bank: $87\,\text{min}$; $95\,\text{min}$ (correct); $98\,\text{min}$; $89\,\text{min}$; $67\,\text{min}$.
- **q-107125 / tea / moderate**: parameters `{"ambient": 28, "initial": 60, "observed": 52, "target": 40, "time": 10}`; field `radio`, key `selection`, correct `$34\,\text{min}$`. Complete bank: $23\,\text{min}$; $31\,\text{min}$; $45\,\text{min}$; $34\,\text{min}$ (correct); $28\,\text{min}$.

## Stage 2 — shared assessed pattern

Easy solves T′=−k(T−A), T(0)=I and evaluates T(s), rounding once at the final stage. Moderate solves T′=−k(T−A) with I and O at positive time s, then solves T(t₁)=Z, again rounding only at the final stage. All assumptions are A>0, k>0, I>A, s>0; moderate A<Z<O<I. The answer is a full scalar with declared temperature scale or elapsed minutes. The general family T=A+Ke^(−kt) is an intermediate, not the requested answer fragment. K=e^C is positive here because the stated branch is T>A. General families must be compared modulo arbitrary-constant rescaling/shift; the calibrated model is uniquely fixed by readings and the final scalar must equal its rounded evaluation.

## Stage 3 — components and complete bank mapping

Prompt slots are complete temperatures, the complete decimal-rate term, complete time slots, context noun phrases and unit declarations. They are constructed as f-string components, not global numeric substitution. Every occurrence of time in story, hint, condition prose, substitution and exponent uses the displayed given. No calendars occur.

Common fixed solution prose and math stages: stated ODE → separated differentials → both integrals → natural log absolute value → positive branch justification → exponent with C → split exponential factors → rename e^C to K → isolate T → initial condition statement and three K substitution/isolation rows → calibrated model. Easy then has one final evaluation row. Moderate additionally has observed condition prose and five rate-calibration rows, target prose and six target-isolation rows, then the log-quotient substitution/rounding row. Source row counts including stated ODE(s): easy13, moderate25. All stages/prose match exactly on all originals, including outside's unreduced39/57 ratio and tea's original “initial temperature reading” wording.

Each observed bank maps to `round(correct mathematical scalar)+offset`, retaining the original unit shape. This is a parameterized evidence profile only; offsets reproduce observed values but do not identify the source author's intended mistakes. No arbitrary interpolating fit or unrelated random perturbation is used for default generation.

| Explicit profile | Template | Complete ordered offsets from rounded correct | Default? |
|---|---|---|---|
| q-15595 | coffee | `[2, -2, 4, 0, -4]` | no; underdetermined intent |
| q-107118 | iron | `[0, -4, -17, -20, -15]` | no; underdetermined intent |
| q-107120 | cake | `[-3, 22, -7, 0, -12]` | no; underdetermined intent |
| q-107129 | compressor | `[-7, 0, 5, -9, 20]` | no; underdetermined intent |
| q-15384 | bath | `[0, 3, 1, 2, -2]` | no; underdetermined intent |
| q-107122 | outside | `[2, 6, 0, -1, 4]` | no; underdetermined intent |
| q-15589 | water | `[-8, 0, 3, -6, -28]` | no; underdetermined intent |
| q-107125 | tea | `[-11, -3, 11, 0, -6]` | no; underdetermined intent |

Authored default banks are complete operation banks, chosen before computing their five answers. With D=I−A, x=ks, easy options are round(A+De^(−x)), round(De^(−x)) [omit ambient], round(A+Ie^(−x)) [do not subtract ambient from K], round(A+De^(−x/2)), round(A+De^(−2x)). All must be distinct and strictly inside (A,I); entire cases are rejected otherwise.

With k=−ln((O−A)/(I−A))/s and τ=−ln((Z−A)/(I−A))/k, moderate options are round(τ), round(s ln(Z/I)/ln(O/I)) [omit ambient in both ratios], round(−ln(Z/I)/k) [omit ambient only in target ratio], round(τ/2), round(2τ). Every result must be distinct and later than s. Their symbolic operations, not just their selected UUIDs, are independently checked.

For authored hard observations O at a and L at b=a+h, define r=(L−A)/(O−A), k=−ln(r)/h, K=(O−A)e^(ka), and τ=a+h ln((Z−A)/(O−A))/ln(r). Complete options are round(τ), round(τ−a) [report interval from first observation instead of beginning], round(a+(τ−a)/2), round(a+2(τ−a)), round(a+h ln(Z/O)/ln(L/O)) [omit ambient in both ratios]. All must be distinct and later than b. Hard retains the explicit model as an intermediate, verifies both observations by substitution, then gives the complete six-row target isolation and two substitution/evaluation rows (30 displayed rows total). K is displayed as an unevaluated rational power; eager CAS radicals do not introduce an extraneous radical-simplification workload.

## Stage 4 — reusable template and bounds

The documented script has shared helpers and separate easy/moderate/hard builders and entrypoints. `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` supports every observed profile at original and changed parameters. Profile selection implies its source layout; conflicting layout or difficulty is rejected. All fields stay radio, five owned math choices with a correct lookup ref, one fixed solution independent of chosen mistake. Options are shuffled deterministically. Fixed parameters/template/profile produce identical content ID across seeds; IDs include actual prompt, solution and full bank. Mathematical fingerprints exclude banks/profile/layout and normalize exact rate spelling, while retaining temperature scale.

Easy explicit workload bounds: ambient5..80, initial≥ambient+15 and≤400, positive time1..15, hundredth rates .02..25. Context guards cap ordinary Celsius liquids at100, compressor140, and Fahrenheit fresh-baked cake initial180..400. Default coffee samples70..100C, iron100..200C, compressor65..100C, cake250..370F; ambient15..35C or60..80F; rates.03..20, time3..12. Moderate explicit bounds use the same initial/time/ambient ranges with A<target<observed<initial; bath and tea initial≤100C. Boiling-water template must retain initial100C in both sampler and explicit API. Samplers vary ambient10..35, initialambient+35..100 except water100, observed strictly below initial, target strictly below observed, time2..12. All source parameters pass these guards. Hard bounds and level rationale are in classification.md. Normal physical temperature/time distractors and complete-bank uniqueness are enforced for explicit replay profiles too.

Raw source Fahrenheit unit error: q-107122 labels ambient15, observed54 and final target25 with C while the problem and initial reading specify F. The explicit observed profile preserves raw teaching evidence; the normal authored default corrects C→F only. Validation distinguishes8/8 raw exact strings from7/8 raw unit-consistent solutions and1/1 supported repair. Native radio grading cannot detect this unit error; actual displayed prose is checked independently.

The no-plot decision is based on every prompt, answer and worked solution, all text/math; lesson narrative illustration is curriculum evidence and is not a practice-question asset. Steps5/7 therefore need no renderer or image cache.

The outside family describes ordinary room air: its initial reading is explicitly constrained to50..90F, with the positive ambient and cooling-order guards also enforced. The outside sampler uses max(50,ambient+35)..90F. Its source72F and changed replay73F are retained. A400F room input is rejected.
