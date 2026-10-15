# Template extraction

## 1. Specific original descriptions

All full original records and canonical/prerequisite references are frozen in source.json. Every original component is mapped below. Literal source value and corresponding recipe use the captured choice order; the generator may shuffle output, retaining field-owned identities. Recipes are complete displayed expression patterns, not claims about inferred learner psychology.

### q-29934

Prompt: Calculate $\displaystyle \int\frac{7}{x}dx$.

Observed parameters: `{"n": 7}`; coefficient family integer. Field selection: five-choice math radio. Source omits difficulty, correct designation and worked solution.

| Choice | Captured exact value | Parameter recipe | Captured key |
|---|---|---|---|
| 0 | `\ln \mid x \mid + C` | `\ln \mid x \mid + C` | missing |
| 1 | `7 + \ln \mid x \mid + C` | `@@n@@ + \ln \mid x \mid + C` | missing |
| 2 | `\frac{7}{\ln \mid x \mid} + C` | `\frac{@@n@@}{\ln \mid x \mid} + C` | missing |
| 3 | `\frac{\ln \mid x \mid}{7} + C` | `\frac{\ln \mid x \mid}{@@n@@} + C` | missing |
| 4 | `7\ln \mid x \mid + C` | `@@n@@\ln \mid x \mid + C` | missing |

Ordered source solution: absent; authored served repair follows canonical e-374 constant extraction then reciprocal primitive.

### q-49097

Prompt: Calculate $\int \frac{\text{d}x}{9x}.$

Observed parameters: `{"n": 9}`; coefficient family reciprocal. Field selection: five-choice math radio. Source has its key and worked solution.

| Choice | Captured exact value | Parameter recipe | Captured key |
|---|---|---|---|
| 0 | `ln⁡\|x\|+9x+C` | `ln⁡\|x\|+@@n@@x+C` | no |
| 1 | `\frac{1}{9}ln⁡\|x\|+C` | `\frac{1}{@@n@@}ln⁡\|x\|+C` | yes |
| 2 | `9ln⁡\|x\|+C` | `@@n@@ln⁡\|x\|+C` | no |
| 3 | `ln⁡(9+x)+C` | `ln⁡(@@n@@+x)+C` | no |
| 4 | `ln⁡(9-x)+C` | `ln⁡(@@n@@-x)+C` | no |

Ordered source solution: First, we apply the constant factor rule and take the coefficient $\frac{1}{9}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{\text{d}x}{9x} & =\frac{1}{9}\int \frac{\text{d}x}{x} \\  & =\frac{1}{9}\int \frac{1}{x}\,\text{d}x \\  & =\frac{1}{9}ln⁡|x|+C.\end{aligned}
$$

### q-103369

Prompt: Calculate $\int \frac{5}{x}\,\text{d}x.$

Observed parameters: `{"n": 5}`; coefficient family integer. Field selection: five-choice math radio. Source has its key and worked solution.

| Choice | Captured exact value | Parameter recipe | Captured key |
|---|---|---|---|
| 0 | `\frac{5}{\operatorname{ln}⁡\|x\|}+C` | `\frac{@@n@@}{\operatorname{ln}⁡\|x\|}+C` | no |
| 1 | `\frac{\operatorname{ln}⁡\|x\|}{5}+C` | `\frac{\operatorname{ln}⁡\|x\|}{@@n@@}+C` | no |
| 2 | `5+\operatorname{ln}⁡\|x\|+C` | `@@n@@+\operatorname{ln}⁡\|x\|+C` | no |
| 3 | `5\operatorname{ln}⁡\|x\|+C` | `@@n@@\operatorname{ln}⁡\|x\|+C` | yes |
| 4 | `\operatorname{ln}⁡\|x\|+C` | `\operatorname{ln}⁡\|x\|+C` | no |

Ordered source solution: First, we apply the constant factor rule and take the coefficient $5$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{5}{x}\,\text{d}x & =5\int \frac{1}{x}\,\text{d}x \\  & =5\operatorname{ln}⁡|x|+C.\end{aligned}
$$

### q-103590

Prompt: Calculate $\int \frac{10}{x}\,\text{d}x.$

Observed parameters: `{"n": 10}`; coefficient family integer. Field selection: five-choice math radio. Source has its key and worked solution.

| Choice | Captured exact value | Parameter recipe | Captured key |
|---|---|---|---|
| 0 | `ln⁡\|x\|+C` | `ln⁡\|x\|+C` | no |
| 1 | `\frac{ln⁡\|x\|}{10}+C` | `\frac{ln⁡\|x\|}{@@n@@}+C` | no |
| 2 | `10ln⁡\|x\|+C` | `@@n@@ln⁡\|x\|+C` | yes |
| 3 | `10+ln⁡\|x\|+C` | `@@n@@+ln⁡\|x\|+C` | no |
| 4 | `\frac{10}{ln⁡\|x\|}+C` | `\frac{@@n@@}{ln⁡\|x\|}+C` | no |

Ordered source solution: First, we apply the constant factor rule and take the coefficient $10$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{10}{x}\,\text{d}x & =10\int \frac{1}{x}\,\text{d}x \\  & =10ln⁡|x|+C.\end{aligned}
$$

### q-29831

Prompt: Calculate $\int -\frac{3}{x}\,\text{d}x=$

Observed parameters: `{"n": 3}`; coefficient family negative_integer. Field selection: five-choice math radio. Source has its key and worked solution.

| Choice | Captured exact value | Parameter recipe | Captured key |
|---|---|---|---|
| 0 | `3ln⁡x+C` | `@@n@@ln⁡x+C` | no |
| 1 | `\frac{3}{ln⁡x}+C` | `\frac{@@n@@}{ln⁡x}+C` | no |
| 2 | `3ln⁡\|x\|+C` | `@@n@@ln⁡\|x\|+C` | no |
| 3 | `-3ln⁡\|x\|+C` | `-@@n@@ln⁡\|x\|+C` | yes |
| 4 | `\frac{-3}{ln⁡\|x\|}+C` | `\frac{-@@n@@}{ln⁡\|x\|}+C` | no |

Ordered source solution: First, we apply the constant factor rule and take the coefficient $-3$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int -\frac{3}{x}\,\text{d}x & =-3\int \frac{1}{x}\,\text{d}x \\  & =-3ln⁡|x|+C.\end{aligned}
$$

### q-29838

Prompt: Calculate $\int \frac{1}{x\sqrt{2}}\,\text{d}x.$

Observed parameters: `{"n": 2}`; coefficient family radical. Field selection: five-choice math radio. Source has its key and worked solution.

| Choice | Captured exact value | Parameter recipe | Captured key |
|---|---|---|---|
| 0 | `\frac{\sqrt{2}}{2}\operatorname{ln}⁡\|x\|+C` | `\frac{\sqrt{@@n@@}}{@@n@@}\operatorname{ln}⁡\|x\|+C` | yes |
| 1 | `\sqrt{2}\operatorname{ln}⁡\|x\|+C` | `\sqrt{@@n@@}\operatorname{ln}⁡\|x\|+C` | no |
| 2 | `\frac{\sqrt{2}}{2}\operatorname{ln}⁡(\|x\|+C)` | `\frac{\sqrt{@@n@@}}{@@n@@}\operatorname{ln}⁡(\|x\|+C)` | no |
| 3 | `\operatorname{ln}⁡(\frac{\sqrt{2}\|x\|}{2}+C)` | `\operatorname{ln}⁡(\frac{\sqrt{@@n@@}\|x\|}{@@n@@}+C)` | no |
| 4 | `\operatorname{ln}⁡(\sqrt{2}\|x\|)+C` | `\operatorname{ln}⁡(\sqrt{@@n@@}\|x\|)+C` | no |

Ordered source solution: First, we apply the constant factor rule and take the coefficient $\frac{1}{\sqrt{2}}=\frac{1}{\sqrt{2}}\frac{\sqrt{2}}{\sqrt{2}}=\frac{\sqrt{2}}{2}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int \frac{1}{x\sqrt{2}}\,\text{d}x & =\frac{1}{\sqrt{2}}\int \frac{1}{x}\,\,\text{d}x \\  & =\frac{\sqrt{2}}{2}\operatorname{ln}⁡|x|+C.\end{aligned}
$$

### q-71098

Prompt: Calculate $\int -\frac{2}{5x}\,\text{d}x=$

Observed parameters: `{"a": 2, "b": 5}`; coefficient family negative_rational. Field selection: five-choice math radio. Source has its key and worked solution.

| Choice | Captured exact value | Parameter recipe | Captured key |
|---|---|---|---|
| 0 | `-\frac{2}{5}ln⁡\|x\|+C` | `-\frac{@@a@@}{@@b@@}ln⁡\|x\|+C` | yes |
| 1 | `\frac{2}{5}ln⁡\|x\|+C` | `\frac{@@a@@}{@@b@@}ln⁡\|x\|+C` | no |
| 2 | `\frac{5}{2}ln⁡\|x\|+C` | `\frac{@@b@@}{@@a@@}ln⁡\|x\|+C` | no |
| 3 | `-\frac{5}{2}ln⁡\|x\|+C` | `-\frac{@@b@@}{@@a@@}ln⁡\|x\|+C` | no |
| 4 | `2ln⁡\|x\|+C` | `@@a@@ln⁡\|x\|+C` | no |

Ordered source solution: First, we apply the constant factor rule and take the coefficient $-\frac{2}{5}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int -\frac{2}{5x}\,\text{d}x & =-\frac{2}{5}\int \frac{1}{x}\,\text{d}x \\  & =-\frac{2}{5}ln⁡|x|+C.\end{aligned}
$$

### q-72059

Prompt: Calculate $\int -\frac{1}{\sqrt{7}x}\,\text{d}x.$

Observed parameters: `{"n": 7}`; coefficient family negative_radical. Field selection: five-choice math radio. Source has its key and worked solution.

| Choice | Captured exact value | Parameter recipe | Captured key |
|---|---|---|---|
| 0 | `-\frac{\sqrt{7}}{7}ln⁡\|x\|+C` | `-\frac{\sqrt{@@n@@}}{@@n@@}ln⁡\|x\|+C` | yes |
| 1 | `-\frac{\sqrt{7}}{ln⁡\|x\|}+C` | `-\frac{\sqrt{@@n@@}}{ln⁡\|x\|}+C` | no |
| 2 | `-\frac{1}{7}ln⁡\|x\|+C` | `-\frac{1}{@@n@@}ln⁡\|x\|+C` | no |
| 3 | `-\frac{7}{\sqrt{7}}ln⁡\|x\|+C` | `-\frac{@@n@@}{\sqrt{@@n@@}}ln⁡\|x\|+C` | no |
| 4 | `-ln⁡\|\sqrt{7}x\|+C` | `-ln⁡\|\sqrt{@@n@@}x\|+C` | no |

Ordered source solution: First, we apply the constant factor rule and take the coefficient $-\frac{1}{\sqrt{7}}=-\frac{1}{\sqrt{7}}\frac{\sqrt{7}}{\sqrt{7}}=-\frac{\sqrt{7}}{7}$ out of the integral. Then we compute the integral of $\frac{1}{x},$ and get

$$
\begin{aligned}\int -\frac{1}{\sqrt{7}x}\,\text{d}x & =-\frac{1}{\sqrt{7}}\int \frac{1}{x}\,\,\text{d}x \\  & =-\frac{\sqrt{7}}{7}ln⁡|x|+C.\end{aligned}
$$

## 2. Shared family pattern

Calculate the indefinite integral c/x by extracting one nonzero constant, then applying integral(1/x)=ln|x|+C on each connected real interval x>0 or x<0. Radical coefficients use the existing source rationalization before the same integration. The supplied object is always one constant multiple of the reciprocal function and the requested object is its whole antiderivative. Every normal instance retains one five-choice radio selection; no sums, substitutions, shifted reciprocal functions, definite limits, initial conditions or logarithmic arbitrary-constant transformations are introduced.

## 3. Components, profiles and source repairs

Source prompts, field key/type/count, correct coefficient, full banks, sentences, coefficient factors, integral operands and final primitive are generated together. Profiles are chosen as complete banks; recipes are never pooled. `raw` is a normalized parameterized schema reference: it reproduces every captured mathematical value, prompt, ordered source solution and relevant omission after required TeX normalization. It is not the full captured Pull record; only source.json preserves that exact full immutable wrapper and attributes. It is explicitly evidence-only. Unchanged normal `observed` banks are the four valid source profiles. `repaired` changes exactly one wrong option in each defective bank:

- q-29934: n+ln|x|+C duplicates ln|x|+C modulo constant. Replace the former by -n ln|x|+C (wrong extracted sign). Its missing key is independently derived as n ln|x|+C, its solution is authored from canonical e-374, and its missing level receives an authored easy assignment.
- q-103369 and q-103590: n+ln|x|+C duplicates ln|x|+C. Replace that sole wrong value by -n ln|x|+C, preserving all other values and the supplied key, prompt and source solution.
- q-29831: n ln x+C and n ln|x|+C coincide as primitive families on x>0. Retain n ln|x|+C and replace n ln x+C by -(1/n)ln|x|+C (reciprocated extracted magnitude). All four other original choices remain. The n/ln x+C wrong choice has real domain x>0,x!=1; it is not claimed to define a real primitive on x<0. It is a source distractor with insufficient domain and a wrong derivative even where defined.

Original C-inside-log errors in q-29838 are retained: they fail as arbitrary primitive families even if a special C=0 yields a valid member. A distractor ln(k|x|)+C has derivative 1/x; it is wrong only when the required coefficient differs from one. Our nonsquare radical bounds enforce that difference. All ordinary choices are pairwise different derivative families on both admissible branch intervals; raw defective banks are never passed as ordinary compatibility tests. Original complete-bank replication, unchanged served-bank fidelity, narrow repair comparisons and authored completeness are separate denominators in source-fidelity.json/validation.json.

TeX normalization removes invisible function-application characters, replaces bare ln/operatorname ln by a delimited \ln command, decodes legacy double-escaped answer commands and applies the shared course-academy-tex-v1 normalizer before IDs. This presentation normalization preserves operands and ordered rows. Raw source JSON remains byte-for-byte unchanged.

## 4. Backbone and bounded slots

Fixed: c/x structure, constant multiple rule then reciprocal integral, one global arbitrary additive C, whole primitive answer contract, five complete choices, source instructional prose and ordered solution operands. Each source profile freezes its own differential layout/row sequence as observed; these are not counted as distinct assessed tasks. Exact source parameters remain legal and replayable.

Variable slots:

| Level | Slot | Bounds and constraints | Dependent components |
|---|---|---|---|
| easy | integer magnitude n | 2..20 for positive, negative and reciprocal integer families | coefficient, integrand, extracted coefficient, all five complete recipes and final primitive |
| easy | radical radicand n | squarefree 2,3,5,6,7,10,11,13,14,15 | radical denominator and rationalization, five choices |
| easy | rational a,b | a=2..7,b=2..11,gcd(a,b)=1 | signed reduced coefficient, reciprocal/sign distractors and all printed operands |
| moderate authored | rational a,b | a=2..14,b=2..15,gcd(a,b)=1 | exactly the q-71098 complete bank/prose/row structure |
| hard authored | radical numerator a, radicand n | a=2..9; n in the squarefree set above | exactly q-72059 rationalization and integral structure, numerator propagated to all five recipe values |

Source coefficients and domains are distinguished from these author-defined bounds. Squarefree radicands and reduced fractions exclude aliases; no C changes or option shuffles count as variation. A canonical task fingerprint is the exact coefficient c of c/x, independent of bank/prompt/seed. Finite catalog batches deduplicate across source layouts and bank profiles, reject requests above the meaningful count, and never silently truncate. All slots are enumerated exhaustively; capacity.json records each slot's observed coverage and the meaningful count per level.

### Missing-level authorship and curricular calibration

The frozen lesson route is reconstructed from activity/first-step17592186106584 through step/next, not collection order: introduction (derivative of ln|x| on x!=0), this KP (step17592186106585), integrating a reciprocal-plus-power sum (17592186106586, KP17592186105716), arbitrary-constant log tutorial (17592186106587), then KP17592186105720. The canonical e-374 extracts integer2. Prerequisites are the Constant Multiple Rule for Indefinite Integrals (topic43) and Differentiating Logarithmic Functions (topic1116). Those anchors permit coefficient arithmetic and the same ln|x| rule, while adjacent KPs exclude sums and constant-law rewrites from this draft.

No observed medium/hard label is inferred. Moderate is an authored calibration to reduced negative nonunit rational coefficients, retaining one extraction and two aligned rows. Hard is an authored calibration to nonunit radical numerators, retaining the observed q-72059 rationalization identity and two integral rows. Numerator multiplication/rationalization increases coefficient bookkeeping but requires no additional integration method, new operator branch or subsequent lesson. Each level has a single comparable workload policy; there is no progression within a level. Some coefficient forms overlap original easy evidence; the level distinction is an explicit conservative authorship claim, not source-confirmed difficulty. We do not multiply capacities with new operators to manufacture variety.
