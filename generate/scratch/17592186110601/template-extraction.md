# Four-stage template extraction

## 1. Describe every original specifically

Full original prompts, solutions, fields, UUIDs and exact values remain in source.json. Parameter records below preserve each signed numeric component; raw originals and generated replays are juxtaposed in review.md. Every answer is one delimiter-free exact scalar parameter, never an equation fragment.

| Source | Family / level | Original parameters | Captured answer / bank |
|---|---|---|---|
| q-215415 | both_blank / easy (authored unrated placement) | `{"m": "1/3", "b": 2, "a": 1, "d": -1}` | absent — supported authored repair |
| q-215416 | one_positive / moderate (authored unrated placement) | `{"m": 3, "b": -5, "a": 1, "B": 6, "C": 4}` | absent — supported authored repair |
| q-215417 | two_blank / hard (authored unrated placement) | `{"A": 2, "B": -3, "C": -6, "a": 1, "D": 2, "E": 2}` | absent — supported authored repair |
| q-72548 | known_standard / moderate | `{"A": 10, "B": 2, "C": 3, "a": 1, "d": -3}` | absent — supported authored repair |
| q-215939 | one_negative_spaced / moderate | `{"m": 2, "b": 1, "a": 1, "B": -10, "C": 3}` | $-5$ |
| q-215941 | one_negative / moderate | `{"m": -5, "b": 3, "a": 3, "B": -5, "C": 9}` | $\frac{1}{3}$ |
| q-215942 | one_negative / moderate | `{"m": 7, "b": -2, "a": 1, "B": -14, "C": 7}` | $-2$ |
| q-215944 | two_positive / hard | `{"A": 10, "B": 5, "C": 3, "a": 2, "D": 1, "E": 2}` | $-\frac{1}{4}$ |
| q-28328 | both_radio / easy | `{"a": 5, "b": 9, "m": -3, "d": -8}` | $-12$, $\frac{1}{3}$, $\frac{1}{15}$, $3$, $-\frac{2}{15}$ |
| q-44407 | two_negative / hard | `{"A": 4, "B": -8, "C": 7, "a": -1, "D": 3, "E": 9}` | $6$, $-6$, $\frac{1}{6}$, $\frac{3}{2}$, $-\frac{3}{2}$ |
| q-44515 | two_zero / hard | `{"A": 15, "B": 5, "C": 9, "a": 3, "D": 4, "E": 0}` | $-\frac{1}{3}$, $-\frac{5}{9}$, $-\frac{4}{5}$, $-\frac{4}{9}$, $\frac{2}{3}$ |

## 2. Generalize the common mathematical pattern

Write each nonvertical line as y=m x+b. One slope has unknown parameter multiplier c; the other slope is m. Perpendicularity gives m c z=-1, so z=-1/(m c). Easy reads both slopes; moderate converts exactly one equation; hard converts two. Distinct source sign normalization rows and the omission of an unnecessary division by one remain structural, not simplification artifacts. Intercepts are displayed and retained in conversions but do not affect the assessed task identity.

## 3. Map components and complete banks

Parameters a and m are slope multipliers/known slope for slope-intercept forms. A,B,C denote the known standard form A x+B y=C. For an unknown standard-form line a z x+D y=E (or a z x+B y=C), c=-a/D (or -a/B). Variables k/p/q/t retain their original names and roles. Conversion rows are constructed from complete LHS/RHS components in their original order; no numerical text substitution occurs across prose.

The source banks below list every original value and its parameterized operation. Correct denotes z=-1/(m c). Ambiguous profiles are explicit source replay expressions, not recovered learner error intent. Their arbitrary source offset/constant transformations are evidence-only and never default distractors.

| Source | Original value | Operation in replay profile | Correct? |
|---|---|---|---|
| q-215939 | $-5$ | z=-1/(m c), exact blank fragment | True |
| q-215941 | $\frac{1}{3}$ | z=-1/(m c), exact blank fragment | True |
| q-215942 | $-2$ | z=-1/(m c), exact blank fragment | True |
| q-215944 | $-\frac{1}{4}$ | z=-1/(m c), exact blank fragment | True |
| q-28328 | $-12$ | -(a+abs(m)+4): fixed replay offset 4; intent unresolved | False |
| q-28328 | $\frac{1}{3}$ | -1/m: omit parameter scale a | False |
| q-28328 | $\frac{1}{15}$ | -1/(a m) | True |
| q-28328 | $3$ | -m: omit reciprocal and scale | False |
| q-28328 | $-\frac{2}{15}$ | -2z: factor 2 replay; intent unresolved | False |
| q-44407 | $6$ | -z | False |
| q-44407 | $-6$ | z | True |
| q-44407 | $\frac{1}{6}$ | -1/z | False |
| q-44407 | $\frac{3}{2}$ | -D m | False |
| q-44407 | $-\frac{3}{2}$ | D m | False |
| q-44515 | $-\frac{1}{3}$ | 1/m: omit remaining standard coefficients | False |
| q-44515 | $-\frac{5}{9}$ | -(D+1)/C: altered constant ratio; intent unresolved | False |
| q-44515 | $-\frac{4}{5}$ | -D/B: wrong standard denominator | False |
| q-44515 | $-\frac{4}{9}$ | z | True |
| q-44515 | $\frac{2}{3}$ | -2/m: scale/omit coefficients; intent unresolved | False |

Normal authored radio bank, selected as a whole: `[z, -z, 1/z, -1/z, -m/c]`. Operations respectively solve the actual constraint, lose its sign, return its reciprocal, lose sign after reciprocation, or equate slopes instead of making their product -1. There is no diagnosis in learner content. All five must be finite and distinct; reject complete instances on collisions. Blanks have exactly their correct scalar and no distractor profile.

## 4. Extract reusable masks, calculations, domains and samplers

`render()` fills whole inline/display mathematical components into fixed captured prose masks. Dynamic components are line equations, slope fragments, aligned conversion blocks and final product/implication. Fixed components are instructional sentences, bullet structure, field keys, punctuation and spacing. Conditional components: q-44407 adds the sign-normalization row; q-215944 omits division by its unit y coefficient; q-44515 omits zero constants. Source replay uses the same renderer and exact arithmetic as random generation. No original-parameter answer lookup or literal replay branch exists.

Explicit parameters must have exactly the family keys. The easy both_blank template fixes a=1 and prompt sign layout b≥0,d≤0. one_positive fixes a=1, B>1,b≤0. Known-standard fixes a=1,A>0,B>1. Negative-one-conversion requires B<-1. two_blank fixes a=1,A>0,B<0,D>0. two_positive requires B>1,D=1. two_negative fixes a=-1,B<-1,D>1. two_zero requires B>1,D>1,E=0. Required slope/y/parameter coefficients are nonzero, so each equation is a genuine line and the parameter answer is unique and finite. All other coefficients are bounded as documented in README. Explicit profiles yielding nonfinite or duplicate bank entries are rejected.

Signed easy fractions extend the observed unit fraction to numerators 1–6 over denominators 2–9; this still performs one reciprocal and one linear parameter division. Random moderate/hard coefficients remain integers. No source-difficulty progression, new mathematical branch or hidden denominator manipulation is introduced. Identity deduplicates the normalized constraint coefficient m c, deliberately excluding intercepts and line scaling. Content identity includes full prompt, exact fixed solution and sorted complete bank, with field ownership derived from that identity.

### Evidence repairs and fidelity denominators

q-215415, q-215416 and q-215417 contain empty blank fields without answers, solutions or observed difficulty. Supported answers -3, 2 and 3 follow independently from the displayed equations; E/M/H placements are authored. MA widget evidence confirms scalar free response but supplies no missing values. q-72548 supplies a mathematically sound solution yielding 1/5 but no captured field; an authored implicit blank with appended {{field-1}} placeholder is supplied and original widget/correct designation remain unclaimed. Prompt fidelity is 10/11 exact, with q-72548 retaining all original prose and appending the required {{field-1}} placeholder (1/1 supported repair); captured solution fidelity is 8/8; captured values 19/19 across 7/7 complete banks; captured designation fidelity is 7/7. The four repaired missing designations are never counted as observed matches.

### Plots and step 7

No practice plots exist; plot rating none. No renderer or image assets are required. The lesson introduction graph is outside the practice templates. Work stops after local generator and validation; no registration or EDB mutation.
