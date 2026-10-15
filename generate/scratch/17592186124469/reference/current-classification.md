# Refreshed source classification and generation scope

At math basis 2566, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, the KP has twelve source practice questions. `replenishment/initial/kp.edn` captures their complete prompts, five-choice banks, keys, worked solutions, difficulty, field layout, and the canonical example at that one basis. The earlier basis-1356 capture remains unchanged. The legacy q-95056 omissions have since been completed in the database, and q-95059 now has a different owned question identity. Current identities are authoritative for inventory and are never rewritten from the old capture.

All twelve current source questions are easy, use a single `selection` radio field with five mathematical choices, and need no plots. Their function/curve backbones are distinct; changes of coefficients within a backbone are variants. The original six families and their complete observed-bank mappings remain in `classification.md`, `template-extraction.md`, and `bank-extraction.json`. The following six families are additional current evidence:

| Source | Function | Curve coordinates | Solution stages | Plot rating |
|---|---|---|---|---|
| q-95051 | x⁴−y⁴ | cos t, sin t | gradient, substitution, curve derivative, dot product, Pythagorean and double-angle reduction | none |
| q-95055 | ln(x³y) | t, eᵗ | unreduced logarithmic partials, reduced gradient, substitution, curve derivative, scalar rational reduction | none |
| q-167407 | √(xy) | t³, t | radical partials, substituted radicals, simplified gradient, curve derivative, dot product | none |
| q-167406 | e^(x−y) | t², −t | exponential partials, substitution, curve derivative with negative second rate, dot product and factoring | none |
| q-95053 | x²+xy | t+1, −t² | two-term first partial, substitution, curve derivative, dot product, polynomial expansion and cancellation | none |
| q-95068 | √(x²+y²) | eᵗ, t | radial partial quotients, substitution, curve derivative, dot product and common-denominator reduction | none |

Each additional source has one complete observed five-choice bank. Their exact values, original field ownership, designation and source IDs are retained in the scoped EDN capture; they are not merged with the old six profiles. Their shared purpose is still the full symbolic derivative of a scalar function along a two-coordinate curve. In particular, the radical-of-product source is distinct from the radial-norm source and the x-powered logarithm is distinct from the y-powered logarithm. No new field types or difficulty evidence appear.

Source mathematical review derives the composite derivative independently from the printed function and coordinates, checks all five choices for mathematical uniqueness, checks the designated member, and checks the last displayed solution row. Native grading exercises every owned choice for every source counted as available. q-167407's final answer 2t is correct, but its displayed partial derivatives √y/(2√x) and √x/(2√y) assume positive x,y, whereas the curve also has real negative coordinates with xy>0. Its worked explanation omits this branch restriction. It is conservatively excluded from the validated inventory count, with no alteration to that source or learner history.

## Frozen generator scope

The existing version `two-variable-vector-chain-1` supports its six original easy families plus the separately authored moderate mixed-polynomial and hard squared-product-arctangent families. All original six source banks replay completely (30/30 choices); that fidelity claim applies to the captured basis-1356 banks. It does not claim replay of the six newly captured banks. The additional six families are classified source evidence and are not sampler capabilities of this frozen version. Implementing them is unnecessary to cover the current empty bands, and sampling them without full extraction/replay would exceed this validated package's scope.

All three difficulty levels are supported. Moderate has 54 validated parameter tuples and hard has 64; identities, seed changes, profiles and option ordering add no mathematical capacity. Every tuple in these two finite catalogues was checked by the existing independent rendered-math validator. No shortage is called filled merely from those capacity figures: only distinct, unseen, native-gradable instances verified after commit count. No new plots are needed, so workflow stages 5 and 7 are inapplicable.

The baseline documents' statements that work stops at step 7 describe the historical draft. The scoped `replenish.py` now implements preparation and commit using the application's EDB integration, native validation preview, application contributor, retained exact request/receipt, database basis guard, and `api.lock` held through submission and readback. Registration uses the stable UUID in `capabilities.json` and the repository-relative Python script path, preserving any existing identity.
