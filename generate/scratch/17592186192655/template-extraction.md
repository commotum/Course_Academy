# Template extraction: four stages

## 1. Specific sources

q-210947 displays `9x+10y=3; −2x−y=3`, asks to eliminate the **second** variable y, and requests the multiplied row and scalar using separate dropdowns. The target coefficients10 and−1 require multiplying the second row by10 and leaving the first row unchanged before adding. The complete multiplier bank is±10,±9. Both constants are3; first-variable coefficients9 and−2 do not affect the target multiplier. The prompt has no worked solution or correct refs. Its system starts with an unescaped literal open brace.

q-211000 displays `3w+2z=−1; 7w+10z=3`, asks to eliminate the **second** variable z with the same two dropdowns, and has a blank paragraph before the system. The target coefficients2 and10 require multiplying the first row by−5 and leaving the second row unchanged before adding. Its bank is±5,±10. Again no worked solution, rating or correct refs exist. The source's first RHS is printed `=-1` without a following space. That source formatting is preserved in raw replay.

The canonical solution notices both target coefficients, marks just the second row with multiplication, displays the original/scaled equations in source order, displays the grouped surviving-variable and constant sums, collects them, and concludes the row/multiplier description. It ends at `5x=10`; it does **not** solve x or y. Normal generation retains this full chain and all shared sentences, conditions the changed row/unchanged row and signs, and independently slots the concluding row/multiplier values.

## 2. Generalized family

Display ordered linear equations `a1 u+b1 v=c1; a2 u+b2 v=c2` where u is the first variable and v is the second. One nonzero target coefficient is an integer multiple in magnitude of the other, with ratio≥2. Choose the smaller-target row and multiply it by the signed negative coefficient ratio, so adding eliminates v. The requested object is the actual row operation (changed row, integer multiplier, other row left unchanged), not the whole system's solution set.

## 3. All components and every original choice

`bank-mapping.json` maps **every one of12 original options** to its source, field, original answer ID, exact value, profile and explicit parameterized recipe. `source-cases.json` maps both unrated practice sources through the public `generate` API. `source.json` preserves raw Pull data and provenance, while generated enums use the required local ident-string shape.

| Public bank profile | Complete multiplier formulas | Row bank | Status |
|---|---|---|---|
| `raw-q-210947`, `completed-q-210947` | `±r`, `±abs(a1)` | first/second | Exact historical scalar pattern; ±a1 is opaque evidence, not recovered distractor intent |
| `raw-q-211000`, `completed-q-211000` | `±r`, `±abs(unchanged target coefficient)` | first/second | Exact historical numerical pattern; copied coefficient interpretation plausible, retained as evidence |
| `difference` | `m`, `−m`, `r−1`, `−(r−1)` | first/second | Authored method bank: signed integer ratio versus difference of target magnitudes divided by smaller magnitude |
| `coefficient` | `m`, `−m`, `abs(unchanged target coefficient)`, its negative | first/second | Authored method bank: signed ratio versus copying the target coefficient without division; nonunit levels only |

Here `r=abs(m)`, `m=−b_unchanged/b_changed`. A source scalar alone underdetermines its intended error. In particular source1's9 equals r−1 at its anchor and also equals a1. The **raw** profile deliberately exposes the opaque ±a1 numerical pattern. The **normal** authored difference profile computes `(abs(b_unchanged)−abs(b_changed))/abs(b_changed)`, independently of a1; it makes no claim to recover the source author's intent. Changed-parameter examples distinguish these formulas.

There is one fixed correct solution per displayed problem, independent of an error choice. No distractor diagnosis appears in learner prose. The complete source bank remains together; no choice is excluded, patched or substituted after parameters. All normal banks are selected before sampling parameters and the entire instance is rejected for collisions, unsupported input, degeneration or ambiguous full row/multiplier combinations.

## 4. Reusable masks, guards and calculations

The two masks preserve their respective newline/paragraph layout and the `{{field-1}}` / `{{field-2}}` placeholders. Complete equation components are formatted independently; short-letter or arbitrary text replacement never touches prose. Raw compact sign domain is positive/positive first row and negative/negative second row; raw spaced domain has positive coefficients. These source-anchored masks are parameterized, not copied payload branches. Normal masks permit signed coefficients in either row. Variable pairs x/y, w/z, u/v, a/b are cosmetic aliases and never inflate task counts.

Correctness is full combination eligibility: for each available multiplier k and each row i, test `k*b_i+b_other=0`, while verifying the actually transformed row and unchanged row. Both reciprocal directions can eliminate a variable in unrestricted mathematics; the added normal wording **“Use an integer multiplier and leave the other equation unchanged.”** makes the intended one-row integer operation explicit. Banks never contain a competing reciprocal answer anyway; all8 available row/multiplier combinations are enumerated and exactly one must be valid. Independent per-field native grading is tested through the real engine, with conjunction of both correct selections corresponding to the unique valid operation.

From the displayed prompt, compute scaled row components `(m*a_i,m*b_i,m*c_i)`. Preserve the other row exactly, cancel the target coefficients, display grouped surviving-variable/constant sums, and collect. Validate every actual printed equation, the marked operation, prose coefficients and concluding row/multiplier. The canonical complete solution is compared byte-for-byte after documented presentation normalization. Structural regression replaces grouped addition with an algebraically equal collected row and must fail validation.

Difficulty bounds and source exceptions appear in `classification.md` and in separately documented easy/moderate/hard API sections. Positive common scaling of the complete system does not create a new assessed task. Mathematical fingerprints retain the ordered target division operands, divided by the complete system's common integer factor, and normalize a common sign; they exclude the remaining incidental coefficients except their effect on genuine global scaling, constant presentation aliases, variables, profiles and bank order. Different rendered questions/banks remain different content identities. Exact full catalog: **24 easy,36 moderate,36 hard substantive operand tasks**, after common-sign aliases are removed. All finite target operand combinations and supported normal profiles are validated, not just the sampled minimum. These modest finite counts accurately reflect this narrow operation-selection KP.
