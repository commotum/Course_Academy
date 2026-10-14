# Classification at math basis 1356

The preserved source wrapper has lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Seven practice questions form seven Markdown/value families and seven five-choice radio bank profiles. No practice prompt, answer or solution contains a plot. Steps 5 and 7 therefore require no renderer.

| Family | Source | Captured difficulty | Field | Plot | Evidence |
|---|---|---|---|---|---|
| `quotient` | q-36297 | absent | selection radio, five math choices | none | Function x²/y, point (2,1), vector (-1,3); solution/key absent |
| `sinlog` | q-37074 | absent | selection radio, five math choices | none | sin(y ln x), point (e,π), greatest increase; solution/key absent |
| `ratio_sum` | q-130801 | moderate | selection radio, five math choices | none | x/y+y/x, (-1,1), (1,-√2); zero gradient |
| `sine_quotient` | q-83608 | moderate | selection radio, five math choices | none | sin(πx)/y+πxy, (1,1), (-2,2); reduce common vector scale and evaluate sine/cosine |
| `tangent` | q-83613 | moderate | selection radio, five math choices | none | 2x tan y−2y tan x, (π/4,π/4), (-1,1); tan/sec² evaluations and two derivative products |
| `exp_bilinear` | q-36300 | hard | selection radio, five math choices | none | 2xy+e^(3x−y), (1,3), fastest decrease; source returns positive norm |
| `sumlog` | q-37083 | hard | selection radio, five math choices | none | (x+y)ln(x+y), (2,-1), fastest decrease; source formal reduction drops two minus signs and returns positive norm |

## Curriculum and authored difficulty decisions

The actual route is reconstructed from `activity/first-step` and `step/next`, not the unordered Pull collection: introduction → calculating a directional derivative → gradient as direction of maximum increase → finding the direction of maximum increase/decrease → directional derivative as generalization of partial derivative → rate in the direction of the gradient → this KP → deriving the formula. The owning topic's prerequisite is The Gradient Vector (MA1934), confirmed by original `1938.json`.

Easy is missing as an observed label. Its authored scope assigns the unrated elementary quotient to easy: positive small integer coordinates, c x²/y (c=1..4), two elementary partials, normalization, substitution and dot product. Moderate retains the three observed derivative families and their distinct quotient, trig/product partial sequences. Hard retains the observed bilinear/exponential and log/product families and assigns the unrated sine/log composition to hard, justified by two nested chain-rule components and an exact logarithm/trig evaluation before finding the greatest rate. These are design claims, not recovered source ratings. They assess scalar rate throughout; no authored task asks for a maximizing direction or a new geometric interpretation. Within a level the independent families are alternatives, not a progression.

## Source anomalies and recovery limits

Both unrated original MA widgets (captured in `original-widgets.json`) confirm five-option radio layout and complete banks, but contain no worked solutions or correct designations. Their missing solutions and keys remain absent in public raw replay. Normal keys are independently inferred: -16/√10 and √(π²+e²)/e. No prior unknown function is needed or reconstructed; both widgets explicitly supply their functions.

For fastest decrease the lesson theorem states the directional derivative's minimum is -||∇f||. q36300 correctly computes -∇f=(-9,-1), then incorrectly identifies its positive norm √82 as the rate. q37083 similarly reports √2, and its generic negative-gradient line is erroneously positive. Raw public replay retains these errors as ineligible evidence. Normal solutions retain the useful norm chain, repair q37083's generic negative signs, and explicitly conclude the signed negative rate. The original keys still match their original positive options for raw evidence; native acceptance of those IDs is not a correctness claim.

Direct decoded byte checks (e.g. first option code points `[45,92,102,114,97,99,...]`, zero adjacent backslash pairs) establish that answer TeX has ordinary single backslashes. No TeX escape repair is claimed. This supersedes an initial incorrect interpretation of serialized tool output.
