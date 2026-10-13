# Four-stage extraction

## 1. Specific source descriptions

q-2005 asks `Calculate $\intxdx$.` Its missing separator after the command makes the EDB TeX malformed; the owning widget prints the integral of x. The five exact choices are 2x², x²/2+C, 2+C, x²/2, x²+C. Field key selection/type radio; no difficulty, solution or correct attribute.

q-2022 asks `Calculate $\intx^{4}dx$.` This likewise joins the command to its argument; the owning widget is integral x⁴. Its five choices are x⁵+C, 4x³+C, x⁴/4+C, x⁵/5+C, x³+C. Same field layout and missing attributes.

q-113665 has n=20, q-71121 n=10, both direct integral prompts. Full solutions: shared power-rule sentence with actual n; equality displaying the integral, unsimplified successor in exponent and denominator, then simplified primitive; derivative check in five ordered rows: derivative of primitive+C; sum of derivatives; coefficient outside derivative plus 0; derivative evaluated by the power rule; final integrand with checkmark. No field attributes.

q-113670 supplies f(x)=x^17, F'(x)=f(x), and asks F(x). It retains three formal rows F'=f, integrate each side, F=integral f; then four power-rule rows F=integral f, substituted x^17 integrand, unsimplified successor quotient, reduced primitive; then all five derivative check rows. The evaluated derivative includes a thin-space before x^17. No fields.

q-66126 asks integral 1. Prose explicitly writes x⁰=1. Three primitive rows: integral 1=integral x⁰, unsimplified x^(0+1)/(0+1)+C, x+C. Four derivative-check rows: derivative x+C, sum derivatives, 1+0, 1. No fields.

All variable roles are fixed: x is independent, F is primitive, f is supplied integrand, C arbitrary real constant. Domains are all real x. Integer n>=0 avoids branch choices and the separate reciprocal/radical skill.

## 2. Generalized pattern

Apply the integration power rule to one unit-coefficient monomial, incrementing the exponent once and dividing by the same successor; retain the arbitrary constant. Check by differentiating using linearity, the zero derivative of C and the power rule. The function wrapper additionally expresses integration as inverse differentiation. Constant 1 explicitly becomes x⁰.

## 3. Complete component and bank mapping

| Bank | Original n | Exact option | Parameterized recipe | Match |
|---|---:|---|---|---|
| observed_2005 | 1 | `2x^{2}` | (n+1)x^(n+1), omit C | exact |
| observed_2005 | 1 | `\frac{x^{2}}{2} + C` | x^(n+1)/(n+1)+C | exact, mathematically inferred correct |
| observed_2005 | 1 | `2 + C` | (n+1)+C, drop x | exact |
| observed_2005 | 1 | `\frac{x^{2}}{2}` | correct fixed primitive, omit C | exact |
| observed_2005 | 1 | `x^{2} + C` | increment, omit division | exact |
| observed_2022 | 4 | `x^{5} + C` | increment, omit division | exact |
| observed_2022 | 4 | `4x^{3} + C` | differentiate instead of integrate | exact |
| observed_2022 | 4 | `\frac{x^{4}}{4} + C` | divide by unchanged exponent | exact |
| observed_2022 | 4 | `\frac{x^{5}}{5} + C` | power rule | exact, mathematically inferred correct |
| observed_2022 | 4 | `x^{3} + C` | decrement exponent, omit differentiation factor | exact |

All ten displayed values map to explicit operations, not numerical fits or perturbations. Labels are supported hypotheses about errors, not recovered author intent. A whole bank is selected first; full-family equivalence compares nonconstant parts and presence of arbitrary C, so rescaling/shifting C cannot distinguish answers. A fixed primitive without C is not the complete family asked for by an indefinite integral. Normal observed_2005 presentation adds “Include the arbitrary constant of integration.” to clarify that criterion. Raw replay preserves original wording and missing correct refs, and remains ineligible for learning.

Authored default five-choice bank: correct; omit division; retain n in exponent while dividing by n+1; increment twice and divide by n+2; multiply by n+1 instead of divide. Every wrong expression comes from an actual power-rule operation error. n=0 would collide under division omission, so the constant template selects a blank before bank construction; attempting its radio form fails rather than falling back. observed_2022 requires n>=2. Every complete bank rejects whole-instance duplicates before shuffling/record construction.

## 4. Reusable template and conditions

The script renders mathematical masks from n and m=n+1 rather than returning captured payloads. Replaying a source uses its template and `raw:<source-id>` profile through public generate. Changed parameters produce changed source-style integral/solution/bank values; missing fields remain missing. Fixed shared sentences and stage order match complete source solutions at original parameters byte-for-byte. Formal n+1 expressions remain unevaluated in the learner-facing math; CAS simplification is used only for validation and final primitives. The function wrapper and constant rewrite are structural templates, not new numerical skills. No plotted components exist.

Normal output repairs both legacy integral commands by separating the command and argument. Missing correct designations are inferred by independently differentiating the candidate expression and requiring arbitrary C; they cannot count as matched observed designations. Missing solutions are authored with the complete direct-integral stage sequence. Missing fields use authored radio or blank layouts. Raw output is explicitly evidence-only, preserves missing-key parity and malformed original command strings, and is never included in normal formatting/native-grading eligibility. No source mathematical correction is required.

Content identity hashes actual prompt, solution, difficulty/layout, complete displayed bank and version; shuffling does not alter identity. Mathematical fingerprint hashes the integrand and complete-family response, excluding layout/profile aliases. Raw missing attributes count separately from inferred completion. The finite domains and exact guards are documented in classification and enforced for both explicit calls and samplers.

## Native constant-family limitation

A separate real-grader fixture submits a mathematically equivalent primitive family with `2C` rather than `C`. It is rejected; this is an existing algebraic blank-grading limitation, not a source-bank mismatch. Independent full-family validity treats them as equal. Normal canonical blank values retain `+C` and unreduced successor equivalents grade successfully. `constant-family-native-report.json` preserves the actual result. No engine edits are authorized or made.
