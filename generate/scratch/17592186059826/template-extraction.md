# Four extraction stages

## 1. Specific source descriptions

**q-102204**: Prompt is `The inequality $3 < x < 7$ can be expressed in interval notation as`. Endpoints are distinct positive integers, variable x, two strict inequalities in ascending order. One radio `selection` field contains (3,7), (-∞,7), [3,7], (3,7], [3,7). All are math answers. No correct ref, rating or practice solution is captured. Independent set semantics gives exactly one matching option: (3,7).

**q-59294**: Prompt is `Which inequality corresponds to the interval $x ∈ (3, 4)$?`. Both endpoint parentheses exclude 3 and 4. One radio `selection` field contains 3≤x<4, 3<x<4, 3<x≤4, text `$x < 3$ or $x > 4$`, and 3≤x≤4. No correct ref, rating or practice solution is captured. Independent set semantics gives exactly one matching option: 3<x<4.

The source strings are decoded JSON values. Canonical prompt contains one U+005C backslash, solution 21, and **zero adjacent-backslash pairs**. Four q-59294 bank values have single TeX `\le` commands as expected; serialization escaping does not imply a doubled-slash anomaly. No source TeX changes are made.

## 2. Generalized mathematical pattern

For exact ordered finite endpoints a<b, convert the bounded open interval (a,b) to a<v<b or conversely. Both endpoints remain excluded. Endpoint values and variable are preserved; no endpoint arithmetic is required. The two directions have distinct Markdown prompts, answer shapes, banks and solution row counts.

## 3. Every component and complete observed banks

All rows belong to field `selection`; source type and raw value are retained in `source.json`.

| Source | Raw value | Parameterized recipe | Original correct designation |
|---|---|---|---|
| q-102204 | `(3, 7)` | `(a, b)` | absent; independently derived correct |
| q-102204 | `(- ∞, 7)` | `(- ∞, b)` | absent; independently derived wrong |
| q-102204 | `[3, 7]` | `[a, b]` | absent; independently derived wrong |
| q-102204 | `(3, 7]` | `(a, b]` | absent; independently derived wrong |
| q-102204 | `[3, 7)` | `[a, b)` | absent; independently derived wrong |
| q-59294 | `3 \le x < 4` | `a \le v < b` | absent; independently derived wrong |
| q-59294 | `3 < x < 4` | `a < v < b` | absent; independently derived correct |
| q-59294 | `3 < x \le 4` | `a < v \le b` | absent; independently derived wrong |
| q-59294 | `$x < 3$ or $x > 4$` | `$v < a$ or $v > b$` (text) | absent; independently derived wrong |
| q-59294 | `3 \le x \le 4` | `a \le v \le b` | absent; independently derived wrong |

These direct structural transformations are defensible full-bank recipes: alter endpoint inclusion, omit the lower bound, or replace intersection with the outside disjunction. Labels describe the displayed transformations and do not claim recovered source-author intent. No wrong-answer fitting or incidental random perturbation is used. The complete bank is chosen before constructing its five values. Ordered finite distinct endpoints guarantee five distinct represented sets and exactly one valid answer.

## 4. Reusable Markdown/value templates

Fixed: the two original prompt sentences, one `selection` radio layout, five-option counts, bank text/math answer types, parentheses/brackets and relation operators. Slots: complete rational endpoint components a,b and variable v; substitutions do not operate blindly on prose. Conditional: rational values render as signed `\frac{n}{d}`. Constraints: a<b, all finite, and the authored level catalog guard in classification. A fourth variable alias can change the displayed content but not the mathematical task fingerprint.

The interval→inequality authored solution reuses the canonical example's **complete prose and two displayed stages**: notation rule bullets; explanation that parentheses exclude endpoints; colored interval row; therefore sentence; colored strict inequality row. At a=1,b=5,v=x it is byte-exact with the canonical worked solution. No practice solution exists to compare, so practice solution fidelity denominator is zero.

The reverse solution is explicitly authored using the same lesson rule prose: both strict inequalities exclude endpoints; displayed strict inequality row; therefore sentence; colored open interval row; more-formal membership row. The three mathematical stages and variable endpoints are independently parsed and checked against the actual prompt.

`source_raw` is a public parameterized replay profile that leaves missing original attributes missing. `original_bank` is the normal minimal enrichment: add an independently derived correct ref, the authored canonical-based solution and authored rating. It adds no presentation repair or mathematical change. Thus raw prompt/bank fidelity is 2/2 and 10/10 values, captured correct-reference fidelity is 0/0 with two missing, practice solution fidelity is 0/0 with two missing, canonical solution fidelity is 1/1. All originals remain reviewable. No original plots occur in either bank, prompt or solution; steps 5 and 7 require no plot extraction or renderer.
