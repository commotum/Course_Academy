# Classification — KP 17592186124470

Captured math database basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Eight practice records, eight distinct mathematical/prompt/solution families and eight five-choice radio profiles. Six records supply worked solutions and difficulty; two are unrated and lack correct references and solutions. Canonical e-3695 supports scope but is not practice coverage. No assets or plots occur; all templates have plot rating **none**.

| Template | Source | Observed difficulty | Generated level | Response/plot |
|---|---|---|---|---|
| pair_products | q-36238 / 17592186124959 | unrated | moderate (authored assignment) | five-choice radio / none |
| trig_product | q-95075 / 17592186125250 | unrated | moderate (authored assignment) | five-choice radio / none |
| constant_coordinate | q-167453 / 17592186284584 | moderate | moderate | five-choice radio / none |
| quartic_trig | q-95070 / 17592186360548 | moderate | moderate | five-choice radio / none |
| log_product | q-95072 / 17592186360550 | moderate | moderate | five-choice radio / none |
| log_difference | q-95142 / 17592186360577 | moderate | moderate | five-choice radio / none |
| exponential_cosine | q-95146 / 17592186360578 | hard | hard | five-choice radio / none |
| log_exp | q-95149 / 17592186360579 | moderate | moderate | five-choice radio / none |

Only easy is missing in the practice snapshot. Authored `affine_polynomial` fills easy: f=ax+by+dz, r=(t,t²,tⁿ), n∈{1,2}, all three nonzero partials, coefficients with absolute magnitude 1–3. This has the same formal gradient → coordinate substitution → vector derivative → dot-product method, with no products in the partials and only first/second powers. Its three contributions remain explicit even when a constant component derivative is zero in observed moderate templates. Equal easy questions do not introduce a progression.

The two unrated questions receive an explicitly authored moderate assignment: one differentiates pairwise products with an exponential coordinate and a constant coordinate; the other substitutes sine/cosine/exponential functions into a product gradient and collects the cancellation. These fit alongside the observed moderate `constant_coordinate` and `quartic_trig` workloads; this is a design claim, not a recovered source label.

Hard retains the observed yz cos(x) / (t²,eᵗ,eᵗ) nested product and authors `canonical_log`, anchored directly to canonical xz ln(y) / (t²,t,t³). Both require three nontrivial chain contributions, exponential/trig or logarithmic reductions, and familiar prerequisite single-variable derivatives. The coefficient and time translation vary the same operations rather than adding another branch. No point evaluation, supplied-gradient-only question, rate context or level-curve interpretation enters this KP.

The owning topic's prerequisites are Differentiating Vector-Valued Functions (4139), The Multivariable Chain Rule (3173), and The Gradient Vector (1934). The actual lesson route, followed from activity/first-step through step/next, is recorded in lesson-route.json: Introduction → two-variable application → this three-variable KP → evaluating at a point → rate interpretation → rate at a point → vector-form intuition. Pull collection order is not used. Point and rate siblings establish explicit scope boundaries.

Original evidence preserves every field and absence in source.json. Byte checks show **zero** adjacent U+005C pairs in all 40 source answers; JSON/repr serialization was initially misread, and no TeX repair is required. Unicode function-application glyphs are retained. Mathematical corrections and presentation repairs: zero. Two independently verified correct refs, two full solutions, and two difficulty assignments are documented completions, not exact source matches.
