# Classification at math basis 1356

Capture: lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, KP17592186152116, topic17592186049228 / MA2626. The seven practice records are retained in `source.json` with their wrapper, separate from the canonical example.

| Captured level | Template/layout | Practice records | Complete banks | Plots |
|---|---|---|---|---|
| easy | factored radio, common monic binomial squared | q-111582 | one five-choice bank | none |
| easy | factored blank, common monic binomial | q-221994 | one singleton answer | none |
| moderate | factored blank, common monic binomial squared | q-221998, q-221999 | two singleton answers | none |
| moderate | factored radio, common monic binomial | q-76409 | one five-choice bank | none |
| unrated | spaced factored radio, common monic binomial | q-76238 | five choices, missing key | none |
| unrated | spaced factored blank, common monic binomial | q-218482 | missing answer and key | none |

There are two mathematical prompt/field families (radio and blank), with four observed layout/solution variants: compact radio, compact blank, spaced radio and spaced blank. Compact variants have source-specific multiple-list lengths and punctuation; each source is its own explicit replay profile. Source difficulty is not inferred from exponent alone: easy q-111582 is squared and moderate q-76409 is linear. Thus normal moderate bounds require a nontrivial shared numerical content; linear instances additionally have nondividing contents. Both rated easy records have coprime contents (2,7 and4,9), while all three rated moderate records have a shared GCF. Normal easy therefore requires small positive coprime contents, retaining exponent1/2; normal moderate requires gcd>1. These bounds apply to explicit/default sampling and observed/derived source profiles, so squared3F/9F is rejected at easy.

The original MA widget `/home/jake/Developer/MA/DATA/Lessons/2626/Source/2626.json` confirms a five-choice radio q-76238 and a single math-editor blank q-218482. It supplies no answer key, difficulty or explanation for either. The authored completion assigns q-76238 to easy because gcd(3,5)=1, and q-218482 to moderate because gcd(6,15)=3 with neither content dividing the other, matching the rated moderate numerical-content method. The raw observed profiles retain the absent difficulty attributes; these assignments remain author metadata and are not counted as observed labels.

No captured source requires a plot. Hard is absent and explicitly authored. Its two field layouts use signed expanded scalar multiples of the SAME primitive three-term nonmonic quadratic. Only integer GCF/content extraction and the canonical numerical-content/shared-polynomial LCM method are required; the common quadratic is retained intact. No perfect-square recognition, root finding, maximum of differing powers, distinct polynomial factors, multivariable inputs or third input is assessed.
