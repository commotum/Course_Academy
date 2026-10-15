# Constant-multiple power substitution

This private replacement candidate uses the immutable math basis 2275 wrapper, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The registered numeric script and its entire 91-file script/evidence set are preserved by `registered-baseline.json`; no imports from those files are used.

There are ten original MA practice records: six labeled easy, three labeled moderate, and unrated/incomplete q-12494. Two additional independent questions are retained exactly, including their wrapper provenance, in `independent-inventory.json`; they are current inventory, not recovered original MA evidence. The canonical e-453 is instructional context, not an additional practice source.

All observed fields are one radio field named `selection`, with five mathematical choices containing the complete primitive and `+C`. No plots or assets occur. Plot rating is **none** at every level.

| Source mask/profile | Captured level | Mathematical form | Prompt/ordered final chain |
|---|---|---|---|
| q-12494 | absent | x(x²+5)^10 | Calculate; solution and correct designation absent; malformed `\intx` |
| q-12496 | easy | x³(x⁴+11)^9 | Calculate; three primitive rows |
| q-113710 | easy | 2x⁵(4+x⁶)^5 | Calculate; four primitive rows |
| q-113711 | easy | x⁶(2+x⁷)^2 | Calculate; four primitive rows |
| q-2388 | easy | x(x²−1)^3 | Calculate; four primitive rows |
| q-72385 | easy | x²(2x³+1)^5 | Equation prompt; three primitive rows |
| q-72386 | easy | 2x⁷(1+x⁸)^7 | Equation prompt; three primitive rows; factor 2 remains in substitution rows |
| q-113715 | moderate | 2x²√(x³+10) | Calculate; root-to-power conversion and five primitive rows |
| q-2379 | moderate | x(3−x²)^5 | Equation prompt; negative differential factor, four primitive rows |
| q-72467 | moderate | x√(x²−5) | Calculate; root-to-power conversion and five primitive rows |

These are separate concrete source masks and ten complete original bank profiles. At the backbone level they are integer-power substitution with positive/negative derivative scaling, and square-root substitution with fractional power arithmetic. Distinct prompt layouts and final row sequences remain separate masks; they are not flattened into a common generic solution.

Normal easy includes an explicitly authored completion of q-12494. Normal moderate serves all three original moderate families. Hard has no observed source difficulty label. Its two authored masks combine the already taught negative differential factor with the already observed square-root conversion: 2x²√(b−x³) and x√(b−x²). Both have the identical formal substitution, differential, reorder, substitute, factor, power rule, simplification and back-substitution stages. Hard is a design claim, not recovered MA difficulty evidence.

The activity route was read from `:activity/first-step` and followed through `:step/next`: Introduction → power times its exact derivative (68722) → this constant-multiple power KP (68723) → rational-substitution tutorial → logarithmic integration (68724) → other fractional expressions (68786). The authoritative local lesson 443 prerequisite is lesson 331, whose prerequisite 334 already teaches algebraic substitution with positive, negative and fractional exponents. Lesson 334 itself requires the chain rule (1108) and sum rule for indefinite integrals (3769). Exact private copies and hashes are in `reference/ma-443.md`, `reference/ma-331.md`, `reference/ma-334.md` and `reference/prerequisite-evidence.json`. The present families use only that established power rule and chain derivative. Exponent −1, logarithms, reciprocal-root integrands, definite bounds, expansion/integration by parts and additional substitutions remain outside the scope. Moderate square-root conversion is directly observed here; combining that conversion with a signed constant factor does not require the later fractional-expression material.

Only a nonzero inner constant varies, bounded to −40…40. This changes the actual integrand and primitive rather than a label or an integration constant. The arithmetic of the power/derivative scaling remains identical within each family; no within-level progression is introduced. A negative even radicand requires a positive constant to give a nonempty real interval. Positive-base real domains for roots are explicit in generation metadata and are independently checked; all integer-power instances are valid on the whole real line. Normal root prompts preserve the source's question wording, with the conventional domain recorded outside learner content.

Actual mathematical capacities, deduplicated independently of profile, layout, seed and choice order, are 560 easy, 240 moderate and 120 hard. `batch` exhausts these finite sets and rejects larger requests. Independent inventory aliases are not counted as extra tasks.
