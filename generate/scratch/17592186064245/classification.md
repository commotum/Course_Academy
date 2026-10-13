# Classification

Source: `math`, basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The complete immutable capture wrapper is copied to source.json. There are 14 practice questions: 2 easy, 6 moderate, 5 hard, 1 unrated. All 14 contain a single five-option `radio` field with key `selection` and whole mathematical primitives followed by `+C`. No blank fields, mixed fields, or plots occur. Plot rating: **none** for every template.

The canonical example is e-491, integral of x exp(7x); the key prerequisite is Integrating Exponential Functions Using Linear Substitution (topic 1112). The lesson's introduction uses x exp(2x), chooses u=x and v'=exp(2x), applies by parts once, and then integrates the remaining exponential. Later sibling KPs handle trigonometric expressions and definite integrals; this generator does neither. Lesson traversal follows first-step/next links:

- 17592186065114: Introduction
- 17592186065115: Using Integration by Parts to Compute an Indefinite Integral Containing an Exponential Expression
- 17592186065116: Using Integration by Parts to Compute an Indefinite Integral Containing a Trigonometric Expression
- 17592186065160: Computing a Definite Integral Using Integration by Parts
- 17592186065117: Deriving the By Parts Formula From the Product Rule
- 17592186065118: Final Remark

Easy varies a positive coefficient and positive exponential slope, with two arithmetic divisions and one by-parts application. Moderate retains one application but uses a negative slope, a shifted exponent, or an integer exponential base with ln(base); these are observed peer demands, not a progression. Hard replaces ax with ax+b, preserving derivative a and one residual exponential integral, with signs and final affine simplification comparable to the observed hard sources. No repeated by parts, powers beyond a linear polynomial, transcendental new factors, or definite limits are added.

| Source | Original level | Template | Parameters | Bank profile | Plots |
|---|---|---|---|---|---|
| q-14434 | easy | e_positive | `{"a": 6, "b": 0, "h": 0, "k": 4}` | `observed:q-14434` | none |
| q-114288 | easy | e_positive | `{"a": 4, "b": 0, "h": 0, "k": 8}` | `observed:q-114288` | none |
| q-2425 | unrated | base_legacy | `{"a": 1, "b": 0, "r": 2}` | `observed:q-2425` | none |
| q-114287 | moderate | e_negative_distributed | `{"a": 6, "b": 0, "h": 0, "k": -3}` | `observed:q-114287` | none |
| q-114289 | moderate | base_calculate | `{"a": 1, "b": 0, "r": 3}` | `observed:q-114289` | none |
| q-114290 | hard | hard_shift_unit | `{"a": 1, "b": -2, "h": 3, "k": 1}` | `observed:q-114290` | none |
| q-114293 | hard | hard_negative_factor | `{"a": 3, "b": -4, "h": 0, "k": -3}` | `observed:q-114293` | none |
| q-12462 | moderate | e_negative_integral | `{"a": 3, "b": 0, "h": 0, "k": -1}` | `observed:q-12462` | none |
| q-12556 | moderate | e_negative_integral | `{"a": 1, "b": 0, "h": 0, "k": -3}` | `observed:q-12556` | none |
| q-12559 | hard | hard_negative_split | `{"a": 3, "b": 5, "h": 0, "k": -5}` | `observed:q-12559` | none |
| q-12560 | hard | hard_shift_split | `{"a": 1, "b": 7, "h": 5, "k": 2}` | `observed:q-12560` | none |
| q-2420 | moderate | base_equals | `{"a": 1, "b": 0, "r": 5}` | `observed:q-2420` | none |
| q-114291 | hard | hard_positive_factor | `{"a": 2, "b": 1, "h": 0, "k": 3}` | `observed:q-114291` | none |
| q-12558 | moderate | e_shift | `{"a": 3, "b": 0, "h": 5, "k": 2}` | `observed:q-12558` | none |

The 12 presentation/value layouts cover all source variants, including the supported legacy base layout. Thirteen rated questions have worked solutions and correct designations. q-2425 is unrated and has neither; it receives an explicitly authored moderate level because its base-2 calculation is exactly the base-3/base-5 moderate method. The original prompt's `\intx` is repaired to `\int x`. The independently differentiated answer is the option `(2^x/ln 2)(x-1/ln 2)+C`; this is an inferred supported designation, never a matched original ref.

The original lesson JSON and Markdown also omit the q-2425 correct designation. Its widget is five-option multiple choice with no blanks; the local evidence copy lesson-widget-q2425.json retains this corroboration. No source question is excluded.
