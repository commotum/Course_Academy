# Template extraction: four stages

## 1. Describe every source specifically

Each source below is a complete scalar equation-solving task. Its outer exponents are affine in one variable; both displayed bases are proper powers of the same base. The hard reciprocal sources add quotient and negative-exponent stages; the product source adds one exponent-combination stage. No source asks for logarithms, quadratic substitutions, multiple solutions, or graphical interpretation. All values are exact.

| Source | Rating | Family | Original parameters | Original answer values | Missing attributes |
|---|---|---|---|---|---|
| q-66788 | unrated; authored moderate | coefficient | `{"b": 2, "p": 2, "q": 3, "a": 1, "h": 1, "c": 2, "k": 0, "var": "x"}` | $2$; $1$; $\frac{1}{4}$; $-\frac{1}{2}$; $\frac{1}{2}$ | :question/difficulty, :question/worked-solution, :answer-field/correct |
| q-66893 | unrated; authored moderate | two_shifts | `{"b": 2, "p": 4, "q": 5, "a": 1, "h": -2, "c": 1, "k": 1, "var": "d"}` | $-13$; $-1$; $-3$; $-6$; $-18$ | :question/difficulty, :question/worked-solution, :answer-field/correct |
| q-100459 | hard | reciprocal | `{"b": 6, "p": 3, "q": 2, "a": 3, "h": 4, "c": 6, "k": -2, "var": "a"}` | absent | :question/answer-fields |
| q-3362 | hard | reciprocal | `{"b": 3, "p": 3, "q": 4, "a": 2, "h": 2, "c": -2, "k": 8, "var": "n"}` | absent | :question/answer-fields |
| q-100462 | moderate | two_shifts | `{"b": 3, "p": 2, "q": 5, "a": 1, "h": -4, "c": 1, "k": 3, "var": "d"}` | $-\frac{3}{23}$; $\frac{21}{2}$; $-\frac{20}{3}$; $-\frac{23}{3}$; $\frac{3}{32}$ | none |
| q-100468 | moderate | two_shifts | `{"b": 5, "p": 2, "q": 4, "a": 1, "h": -7, "c": 1, "k": 10, "var": "d"}` | $-20$; $25$; $-24$; $-27$; $-7$ | none |
| q-110544 | easy | one_shift | `{"b": 3, "p": 4, "q": 3, "a": 1, "h": 0, "c": 1, "k": 5, "var": "y"}` | $15$; $9$; $10$; $5$; $3$ | none |
| q-3304 | hard | product | `{"b": 2, "p": 3, "q": 2, "a": 1, "h": 0, "c": 2, "k": -1, "t": 5, "var": "x"}` | $2$; $5$; $3$; $1$; $-3$ | none |
| q-66889 | easy | one_shift | `{"b": 4, "p": 2, "q": 3, "a": 1, "h": 0, "c": 1, "k": 4, "var": "b"}` | $-2$; $-4$; $-12$; $-10$; $-3$ | none |
| q-66892 | easy | one_shift | `{"b": 5, "p": 2, "q": 3, "a": 1, "h": 1, "c": 1, "k": 0, "var": "q"}` | $4$; $3$; $2$; $-1$; $1$ | none |
| q-66895 | moderate | coefficient | `{"b": 3, "p": 4, "q": 3, "a": 3, "h": 0, "c": 1, "k": 5, "var": "m"}` | $\frac{5}{3}$; $6$; $\frac{1}{3}$; $\frac{5}{6}$; $5$ | none |
| q-3090 | moderate | coefficient | `{"b": 2, "p": 4, "q": 3, "a": 2, "h": 0, "c": 1, "k": 1, "var": "n"}` | $\frac{5}{3}$; $-\frac{2}{5}$; $5$; $\frac{3}{5}$; $3$ | none |

## 2. Generalized pattern and purpose

Let B>1, with different nonunit powers P,Q≥2. Rewrite both bases B^P and B^Q before equating exponents. In ordinary equations the outer exponents are A z+H and C z+K, giving P(Az+H)=Q(Cz+K). Reciprocal equations have (1/B^Q)^(Cz+K), giving P(Az+H)=-Q(Cz+K). Product equations have B^(P(Az+H)) B^(Q(Cz+K))=B^T, giving P(Az+H)+Q(Cz+K)=T. Every answer is a single exact rational.

Ordinary/reciprocal root: `(s*Q*K-P*H)/(P*A-s*Q*C)`, s=+1/-1. Product root: `(T-P*H-Q*K)/(P*A+Q*C)`. These are computed from parameters. Prompt/solution renderers insert whole mathematical components; they do not replace short strings across prose or return literal source payloads.

## 3. Components and complete observed bank mapping

Each source field is `selection`, radio, five math answers; source omission cases are kept exactly. Tables below map every displayed answer, including correct values. For an observed scalar v₀ and independently derived original correct value r₀, the explicitly opaque continuation is `v₀/r₀ * r(parameters)`. This is a rational proportional bank profile, **not a recovered error recipe**. Its ratio is an observed numeric expression pattern and its interpretation is unresolved. All five expressions are evaluated as one complete bank; no candidate pool, first-valid replacement, answer lookup, or fitted polynomial is used. Such profiles are evidence-only, never selected as the normal learner bank. The purpose of the continuation is to retain auditable exact observed banks while satisfying parameterized replay.

### q-66788 / `observed:q-66788`

Correct value independently derived: $\frac{1}{2}$. Original correct designation absent.

| Field | Original answer UUID | Complete value | Proportional recipe | Original correct |
|---|---|---|---|---|
| selection | 9cbf6a27-5abf-56f0-96e5-2773ce7b62d2 | $2$ | `(4) * r(parameters)` | not designated |
| selection | b9c8f896-da87-5acf-9e69-d5217e45288c | $1$ | `(2) * r(parameters)` | not designated |
| selection | d540f591-4bda-5ebc-ab94-b52d44948574 | $\frac{1}{4}$ | `(1/2) * r(parameters)` | not designated |
| selection | 454abe14-6e0c-5bf5-bef1-9a0c39ff0237 | $-\frac{1}{2}$ | `(-1) * r(parameters)` | not designated |
| selection | 7e914151-9093-5276-be19-33078b973cc7 | $\frac{1}{2}$ | `(1) * r(parameters)` | not designated |
### q-66893 / `observed:q-66893`

Correct value independently derived: $-13$. Original correct designation absent.

| Field | Original answer UUID | Complete value | Proportional recipe | Original correct |
|---|---|---|---|---|
| selection | 23547e2f-726d-5dfc-b054-2ce0415151fc | $-13$ | `(1) * r(parameters)` | not designated |
| selection | 3498e3e5-6e90-5be9-bb54-42fcd765fdfd | $-1$ | `(1/13) * r(parameters)` | not designated |
| selection | 455fc955-6206-569b-97bb-4995d8be74ed | $-3$ | `(3/13) * r(parameters)` | not designated |
| selection | 59e3a8bb-f7e0-5a24-a1b4-7b6a7b3efeee | $-6$ | `(6/13) * r(parameters)` | not designated |
| selection | 5f3a0735-31d0-5b62-ac91-4e7b4e6178fa | $-18$ | `(18/13) * r(parameters)` | not designated |
### q-100459 / `observed:q-100459`

Correct value independently derived: $-\frac{8}{21}$. Original correct designation absent.

No original field/bank. Raw replay omits the attribute; normal radio completion is authored.

### q-3362 / `observed:q-3362`

Correct value independently derived: $19$. Original correct designation absent.

No original field/bank. Raw replay omits the attribute; normal radio completion is authored.

### q-100462 / `observed:q-100462`

Correct value independently derived: $-\frac{23}{3}$. Original correct designation present.

| Field | Original answer UUID | Complete value | Proportional recipe | Original correct |
|---|---|---|---|---|
| selection | 3e6c4527-389f-53df-a817-0ed1f3abbe45 | $-\frac{3}{23}$ | `(9/529) * r(parameters)` | no |
| selection | b8bbfad5-b2b8-56ce-9add-a4ac75631348 | $\frac{21}{2}$ | `(-63/46) * r(parameters)` | no |
| selection | cd32b9be-49e7-5180-9502-60b22eb68cac | $-\frac{20}{3}$ | `(20/23) * r(parameters)` | no |
| selection | e390ede5-d86c-5365-9c30-858c8f0cdd13 | $-\frac{23}{3}$ | `(1) * r(parameters)` | yes |
| selection | eecf47c3-0f1e-5617-9305-4edb271f4bc7 | $\frac{3}{32}$ | `(-9/736) * r(parameters)` | no |
### q-100468 / `observed:q-100468`

Correct value independently derived: $-27$. Original correct designation present.

| Field | Original answer UUID | Complete value | Proportional recipe | Original correct |
|---|---|---|---|---|
| selection | 2e0a433d-875a-5565-9005-946fce25e302 | $-20$ | `(20/27) * r(parameters)` | no |
| selection | 60857dad-8f5f-54c0-abcd-6348c81a747d | $25$ | `(-25/27) * r(parameters)` | no |
| selection | 7ab2d528-c28f-586f-a1b1-e63ca9352c62 | $-24$ | `(8/9) * r(parameters)` | no |
| selection | b9537422-626f-5c29-bb8f-3ab1f00e5485 | $-27$ | `(1) * r(parameters)` | yes |
| selection | ec35a75a-8c11-5f78-8b61-6c72af99292e | $-7$ | `(7/27) * r(parameters)` | no |
### q-110544 / `observed:q-110544`

Correct value independently derived: $15$. Original correct designation present.

| Field | Original answer UUID | Complete value | Proportional recipe | Original correct |
|---|---|---|---|---|
| selection | 5590a848-eae9-5089-bdc1-7f789ac62064 | $15$ | `(1) * r(parameters)` | yes |
| selection | 5f338793-8672-5f89-9124-424dc680305c | $9$ | `(3/5) * r(parameters)` | no |
| selection | a0029015-9d7a-5b76-8132-425f8e5b1369 | $10$ | `(2/3) * r(parameters)` | no |
| selection | caf954cd-bb67-553d-8e8c-ae5436312352 | $5$ | `(1/3) * r(parameters)` | no |
| selection | f2f19e3a-8e8b-5a89-b39e-a28325288d1b | $3$ | `(1/5) * r(parameters)` | no |
### q-3304 / `observed:q-3304`

Correct value independently derived: $1$. Original correct designation present.

| Field | Original answer UUID | Complete value | Proportional recipe | Original correct |
|---|---|---|---|---|
| selection | 0afd78c4-898a-5dcb-acd8-ccd10775c767 | $2$ | `(2) * r(parameters)` | no |
| selection | 43924541-f7eb-59bb-bc12-3b2b676d62c0 | $5$ | `(5) * r(parameters)` | no |
| selection | 948cfa4d-d1dc-5ad4-90ba-e697cdb0adf1 | $3$ | `(3) * r(parameters)` | no |
| selection | a2a106f1-8046-5175-bb97-e0b1842bc7b3 | $1$ | `(1) * r(parameters)` | yes |
| selection | d63fdb98-6f65-5c38-ba7d-66e1d91d04bc | $-3$ | `(-3) * r(parameters)` | no |
### q-66889 / `observed:q-66889`

Correct value independently derived: $-12$. Original correct designation present.

| Field | Original answer UUID | Complete value | Proportional recipe | Original correct |
|---|---|---|---|---|
| selection | 0789c91d-4133-552b-8e70-d28f7dc1b01d | $-2$ | `(1/6) * r(parameters)` | no |
| selection | 0f652d2a-88fb-598a-a277-6b88d22c44ca | $-4$ | `(1/3) * r(parameters)` | no |
| selection | 22144aed-0092-5ef2-a430-b40baca139b4 | $-12$ | `(1) * r(parameters)` | yes |
| selection | 3b441be5-b06c-5167-83a7-2c634e4ab505 | $-10$ | `(5/6) * r(parameters)` | no |
| selection | 6e070fca-f0f9-58a6-a692-9afdb70d5363 | $-3$ | `(1/4) * r(parameters)` | no |
### q-66892 / `observed:q-66892`

Correct value independently derived: $2$. Original correct designation present.

| Field | Original answer UUID | Complete value | Proportional recipe | Original correct |
|---|---|---|---|---|
| selection | 573690ae-6cda-5d43-b52b-e9b6645c5f67 | $4$ | `(2) * r(parameters)` | no |
| selection | 655306ca-f081-5fd5-9ed9-84da858807a1 | $3$ | `(3/2) * r(parameters)` | no |
| selection | 6fd009f8-6e8a-549d-9a4d-ab1bb878a030 | $2$ | `(1) * r(parameters)` | yes |
| selection | e1c4d8a9-1010-5a2a-9648-8736181856d3 | $-1$ | `(-1/2) * r(parameters)` | no |
| selection | fcc51cc3-bdf5-5249-90fb-98347db0ac3c | $1$ | `(1/2) * r(parameters)` | no |
### q-66895 / `observed:q-66895`

Correct value independently derived: $\frac{5}{3}$. Original correct designation present.

| Field | Original answer UUID | Complete value | Proportional recipe | Original correct |
|---|---|---|---|---|
| selection | 13d8d4f1-069f-5999-90cd-de6a076c1b15 | $\frac{5}{3}$ | `(1) * r(parameters)` | yes |
| selection | 18fcade8-3d85-57f2-9926-025f7f6bda40 | $6$ | `(18/5) * r(parameters)` | no |
| selection | c7c31d51-ffad-5ede-a608-d0a37966955d | $\frac{1}{3}$ | `(1/5) * r(parameters)` | no |
| selection | ded55b8b-cc37-5917-a902-1f995ea97dfd | $\frac{5}{6}$ | `(1/2) * r(parameters)` | no |
| selection | f3f1e514-ed0c-50dc-9391-5f7fc7b497c6 | $5$ | `(3) * r(parameters)` | no |
### q-3090 / `observed:q-3090`

Correct value independently derived: $\frac{3}{5}$. Original correct designation present.

| Field | Original answer UUID | Complete value | Proportional recipe | Original correct |
|---|---|---|---|---|
| selection | 083bbb43-125e-530a-a0bf-4e386e0fef8e | $\frac{5}{3}$ | `(25/9) * r(parameters)` | no |
| selection | 2ebed13b-65b6-5f09-b6ac-5843bb401594 | $-\frac{2}{5}$ | `(-2/3) * r(parameters)` | no |
| selection | 8a7cd739-dad9-5004-a078-dfdfdfb9ad48 | $5$ | `(25/3) * r(parameters)` | no |
| selection | c45e66f0-50f2-598c-b5d0-5402c3cbc44b | $\frac{3}{5}$ | `(1) * r(parameters)` | yes |
| selection | e52fbbd7-076f-5ca8-a202-557210987158 | $3$ | `(5) * r(parameters)` | no |

### Authored complete default operation banks

Write D=P A−s Q C and N=s Q K−P H. Ordinary bank: `[N/D, -N/D, (sK−H)/D, (sPK−QH)/(QA−sPC), N/(PA+sQC)]`. The operations are correct isolation, reversed constant transfer, omitted shift distribution factors, exchanged rewrite factors, and added variable coefficients. For reciprocal banks use `[N/D, (QK−PH)/(PA−QC), (-K−H)/D, -N/D, N/(PA−QC)]`: ignore reciprocal sign, omit shift distribution, reverse the transferred constant, or subtract variable coefficients.

Product bank: `[r, (T−H−QK)/(A+QC), (T−PH−K)/(PA+C), (T−H−K)/(PA+QC), (T−PH+QK)/(PA−QC)]`. These omit the left/right rewrite factor, omit shift distribution, or subtract instead of add exponents. Every member comes from an actual displayed operation. These are authored banks, not inferences about original distractor intent. All undefined denominators, duplicate values, correct-value collisions, and zero-numerator collisions reject the entire instance.

## 4. Reusable masks, constraints and stage sequence

Fixed prose comes from source solutions: common-base opening, rewrite sentence, power-rule sentence, common-base equating sentence. Mathematical slots are both full base-power identities; both full outer exponents; full rewrite, power-rule, optional product/negative-exponent displays; the ordered linear rows; the final scalar. Source punctuation and `\,` spacing are preserved. The eleven presentation templates keep all original stages and row omissions; this includes easy omission of a redundant collected row and q-3362 reversing both collected signs before division. No error-dependent worked solution is generated.

Ordinary stages: (1) explicitly rewritten bases, (2) multiplied inner/outer exponents, (3) equate exponents, distribute, collect (moderate only), solve. Reciprocal stages add quotient display and conversion to a negative exponent before linear solving. Product stages contain the separate two powers and combined exponent in the same aligned block; the next block retains the uncollected distributed sum `P A z+Q C z+Q K` before collection. Independent QA parses every stage from the actual printed strings, including that uncollected sum.

### Sampling and explicit-input bounds

Every guard applies to explicit parameters and samplers. B∈{2,…,6}; P,Q∈{2,…,5}, P≠Q, both displayed integer powers ≤1296. The original source base 6 and power 5 (e.g. 243) are retained. Easy: A=C=1, |P−Q|=1, exactly one nonzero shift of magnitude 1…8; every item has one distribution and integer isolation with three linear rows. Moderate two-shift: A=C=1, H∈−10…−1, K∈1…10; every item distributes two offsets. Moderate coefficient: exactly one of A,C is 1 and the other lies in 2…4, exactly one nonzero shift of magnitude 1…8; every item multiplies a nonunit variable coefficient and distributes one offset. q-66788 additionally retains a left shift and right scaled exponent. Hard reciprocal: |A|,|C|∈2…6, |H|,|K|∈1…8, |PA|,|QC|≤24; every item converts a reciprocal to a negative exponent and distributes two affine expressions. Hard product: A=1,H=0,C∈2…4, |K|∈1…4,T∈2…6; every item uses two power rewrites plus the product rule and one affine distribution. Moderate instances reject collected coefficient +1 (which would duplicate the final row); coefficient −1 retains the observed sign-isolation case q-66893. Hard reciprocals require absolute collected coefficient ≥2 so the last step genuinely divides. These are unordered same-workload family variants within observed level anchors. Broader familiar shifts/base powers are authored sampling policy, not recovered MA generator bounds.

Missing original attributes: q-66788 and q-66893 receive explicitly authored moderate assignments because they match the observed coefficient and two-shift moderate families. Their missing correct values (1/2 and −13) are independently derived and present only in normal output. q-100459 and q-3362 receive authored five-choice radio fields only in normal output. Raw public replay omits fields, difficulty, correct refs and solutions wherever absent; presence parity is checked individually. Correct-designation fidelity has denominator 8, not 12. No mathematical source errors were found in present banks or worked solutions. Raw and presentation-exact solutions are identical for all 10 present sources; no TeX repair was required.

### Identity, eligibility and audit

Canonical mathematical fingerprints normalize variable letters, common prime-power bases, common outer-exponent scaling and equation-side order. Profiles/banks/layouts are excluded. Presentation identity hashes version, actual prompt, actual fixed solution, difficulty and complete sorted bank, with field-owned answer UUIDs; seed and shuffle order are excluded. Evidence-only raw replay never silently becomes a learning record. Normal output uses the authored-method profile. Native grading tests all displayed choice IDs; separate exact printed-expression checks establish correctness and all fifty source option matches. No blank equivalence checks apply because no supported source/normal layout is a blank.

## Meaningful repeated-practice capacity

`variety.json` enumerates the complete easy one-shift and moderate two-shift domains, including whole-bank rejection and canonical deduplication. Easy has 832 eligible parameter sets representing 416 canonical tasks; moderate two-shift has 3147. An additional 1500-seed audit establishes lower bounds of 1237 coefficient, 1498 reciprocal, and 1276 product tasks. These count actual mathematical parameter variation, excluding variable aliases, bank aliases, seed and choice order. They are distinct from the smaller 960-instance detailed printed-math QA sample. The latter covers all twelve presentation styles and all three levels.
