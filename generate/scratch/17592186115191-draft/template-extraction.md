# Four-stage template extraction

## 1. Each original before generalization

| Family | Prompt object and response | Ordered worked stages |
| --- | --- | --- |
| q-17639 | 23tan x -5x⁵ -cot x; whole derivative radio | source solution absent; authored formalD, termwise rules with signed cot derivative, collect |
| q-31279 | 2x -cot x; whole derivative radio | source solution absent; authored formalD, signed derivative substitution, collect |
| q-31288 | -6cot x, evaluate first derivative at pi/6; fieldless | formalD, constant times negative csc², cancel signs; substitute angle, csc value2 squared, multiply24 |
| q-31355 | cot x/x²; fieldless | formalD, quotient-rule products over x⁴, cancel a factorx to denominatorx³ |
| q-105309 | 5^x -cot x; whole derivative radio | formalD, base-log derivative and negative cot derivative, collect signs |
| q-340595 | e^x -3cot x; whole derivative blank | formalD, signed termwise derivatives, collect signs |
| q-340597 | ln(x)cot(x); blank cot(x)/x with supplied negative log term | formalD, two product-rule terms, quotient notation and signed term |
| q-340598 | x cot(x); blank x csc²(x) with supplied cot-minus | formalD, two product-rule factors including1, collect |
| q-340599 | ln(x)/cot(x); blank x ln(x) in numerator of displayed derivative fraction table | formalD, quotient rule, nested common-denominator fraction, reorder numerator product |
| q-340603 | x/cot(x); blank x csc²(x) in numerator of displayed derivative fraction table | formalD, quotient-rule products, collect numerator signs |
| q-1913 | -2x⁴cot x; whole derivative radio | formalD, signed product-rule factors, collect |

Raw records preserve redundant nested aligned environments and historical roman/Unicode function notation. Normal formatting uses the frozen shared formatter; formatting normalization is separate from source exactness. All functions have the inner argumentx and all derivatives have order1. Table response layouts are preserved, with full table numerator/denominator checked after inserting the generated answer. No complete equation is stored in a blank answer.

## 2. Shared pattern and instructional purpose

Use d(cot x)/dx=-csc²x within each original direct sum, product or quotient; hard then evaluates at one familiar angle. Fix the source operation/field contract and ordered operative chain, varying only complete coefficients or the already-observed exponential base. Different equal-level coefficient choices are unordered alternatives, not progression. No second derivative, chain-rule inner function, new answer type, or new trigonometric angle family is introduced.

## 3. Every component and complete bank

`source-bank-mapping.json` retains every exact original choice with its complete raw field/answer records, original parameter, designated-correct status, and parameterized displayed expression pattern. `source.json` contains the entire source prompts and worked prose/chains. Each bank is selected as a COMPLETE profile before parameters; a collision rejects the entire instance. There is no pooled option selection or first-valid substitution.

q-31279's bank contains omitted linear derivative, wrong cot sign, wrong linear sign with unsquared csc, and unsquared csc. q-105309's bank contains omitted ln(base), missing csc square and cot-derivative sign changes. q-17639's coefficient permutations and q-1913's x²csc and other compound changes do not uniquely identify the original wrong operation. Their complete historical masks are retained under public `observed-q-...` profiles with explicit bounded interpretation limits and evidence-only flags.

Normal authored q-17639 bank: correct a sec²x -25x⁴ +csc²x; omit tangent coefficient; wrong cot derivative sign; retain -5x⁵ unchanged; omit cot derivative. Normal authored q-1913 bank: correct a x⁴csc²x -4a x³cot x; lose the negative sign in the cot derivative; lose the negative sign in the polynomial derivative; omit the cot derivative term; omit the polynomial derivative term. These are complete method-derived banks, labeled authored. A raw wrong expression being reproducible does not establish its author's intent.

q-17639 and q-31279 have absent original correct refs: independent differentiation identifies their unique correct choices only in normal completion. Their two absent solutions receive the minimal chains above. q-31288 and q-31355 have absent fields: normal completion adds scalar/full-derivative blanks, respectively. These additions never count as matched original attributes. Raw output retains every omission.

## 4. Backbone, slots, domains and identities

`a` is always a builtin integer; bool, floats, strings, unknown keys and values outside the shared explicit/sampler domain are rejected. No seed may silently alter explicit parameters. Domains are finite and enumerable:

- q-17639: tangent coefficienta=2..24, source23; the polynomial stays -5x⁵ and cot coefficient stays -1. This keeps the source three-term derivative arithmetic. Historical coefficient25 collision is outside this bounded family; no supported native gap is hidden by changing the domain.
- q-31279: linear coefficienta=1..12, source2.
- q-105309: exponential basea=2..9, source5; base and logarithm move together, with exactly the same derivative rule and stages.
- q-340595: cotangent coefficienta=1..12, source3.
- q-31288: negative cotangent coefficient-a for a=1..24, source6; pi/6 remains fixed. The existing independently authored inventory coefficients5,12,18,20,23 lie in this same family, but are not additional MA observations.
- All six moderate families: coefficienta=1..12. q-31355 scales the numerator cotangent; q-340597 scales the supplied logarithmic factor; q-340598 scales the linear factor; q-340599 and q-340603 scale the quotient numerator; q-1913 varies original coefficient2 and dependent derivative coefficient8=4a, keeping power4 and derivative power3. Unit coefficients omit their printed1 exactly where the source omits it, preserving original anchors and avoiding accidental numeric concatenation.

Coefficient scaling affects the actual differentiated object and every dependent formal operand, product/quotient term, supplied fragment, answer, and final expression. The masks operate on complete mathematical components, with all exponents fixed. Numeric math slots never visit prose or field identifiers. In hard, the entire pi/6 component is protected from coefficient6 substitution. First-derivative and inner-argument roles remain fixed.

Domains: use real connected intervals avoiding sin(x)=0. Quotients by cotangent also avoid cos(x)=0. Logarithmic families require x>0; the x² quotient excludes0. The hard endpoint pi/6 lies in (0,pi), away from poles. Historical secant distractors can introduce their own poles; equivalence comparisons use common real open intervals and never substitute a pole.

Content identity hashes actual prompt, fixed solution, difficulty, complete unordered banks and correct values. Field/answer UUIDs are owned by that content. Seed, option order and profile aliases cannot alter identity. Mathematical fingerprints use the canonical supplied function plus evaluation point, excluding response fragments, bank profiles and notation. No extra counted tasks are created by cosmetic field names, option shuffles or different target roles.
