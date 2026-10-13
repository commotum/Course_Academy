# Classification — 17592186100890

Finding the Cartesian Equation of a Curve Defined Parametrically With Trigonometric Functions

Database `math`; basis `1356`; lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The current capture wrapper preserves database, basis, lineage, and the full record. Comparison with the prior basis-1308 capture confirms all 20 practice records and the canonical example are identical; only explicit key-prerequisite metadata was added. [Current comparison](current-source-comparison.json) retains source hashes.

| Difficulty | Practice questions | Radio | Blank | Markdown/value templates | Radio bank profiles | Plot rating |
|---|---:|---:|---:|---:|---:|---|
| Easy | 11 | 8 | 3 | 7 | 8 | None |
| Moderate | 2 | 2 | 0 | 2 | 2 | None |
| Hard | 7 | 4 | 3 | 4 | 4 | None |

The separate canonical example is excluded from practice counts. Radio banks contain five math values; blanks contain one canonical math value. No option feedback or plots occur.

| Template | Difficulty | Field / expected value | Source questions |
|---|---|---|---|
| `ellipse_sin_radio` | easy | radio / equation | q-15751, q-102680, q-102682, q-15657 |
| `ellipse_cos_radio` | easy | radio / equation | q-15752, q-15679 |
| `ellipse_sin_blank` | easy | blank / lhs | q-320946 |
| `ellipse_cos_blank` | easy | blank / lhs | q-319828 |
| `tan_sec_radio` | easy | radio / equation | q-102677 |
| `cot_csc_radio` | easy | radio / equation | q-15761 |
| `cot_csc_blank` | easy | blank / rhs | q-321400 |
| `cos_tan_radio` | moderate | radio / equation | q-102687 |
| `sin_tan_radio` | moderate | radio / equation | q-15759 |
| `sin_double_factored_radio` | hard | radio / equation | q-24378 |
| `sin_double_expanded_radio` | hard | radio / equation | q-24576 |
| `cos_double_radio` | hard | radio / equation | q-24574, q-24575 |
| `cos_double_blank` | hard | blank / rhs | q-321314, q-321315, q-321318 |

Numeric coefficient changes are variants. Sine/cosine orientation, field placement, root-versus-squared answer, and the hard factored-versus-expanded solution endings define separate templates. Conditional omission of unit scales/zero shifts stays within a template.

The 14 complete radio bank profiles are listed in [choice-bank-extraction.md](choice-bank-extraction.md). Each source bank has four mapped distractors; the sine ellipse template has four profiles, the cosine ellipse template has two, and the cosine double-angle radio template has two. Other radio templates each have one. Profiles preserve different choice patterns without inflating the prompt/field/solution template count.

Steps 5 and 7 are not needed: every plot rating is none. The product-rule KP is outside this rebuild.

## Authored moderate variations

The source table above remains an account of captured questions. Draft 4 adds `sin_cot_radio` and `cos_cot_radio` as authored templates and one authored bank for each of the four moderate families. The implementation therefore has 15 templates and 18 banks: 13 observed templates / 14 observed banks plus 2 authored templates / 4 authored banks.

All four moderate families support positive scales 1–4 and any one open quadrant. Every moderate field remains radio. These are unordered variations of the same skill, with no difficulty stages. Normal sampling uses the authored banks; the two observed moderate profiles remain explicit source-replay profiles. See [moderate-variations.md](moderate-variations.md) for feature extraction, formulas, constraints, and provenance.
