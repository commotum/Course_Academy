# Template extraction

## 1. Specific observed instances

Each row below describes the actual source function, point and derived gradient. The full ordered fields, every answer UUID/value, designation attribute presence and component recipes are mapped in `source-components.json`; no choices are omitted. Source cases cover all 12 questions.

| Source | Function | Point | Gradient |
|---|---|---|---|
| q-37570 | $xy+5x+{z}^{2}$ | [1, -1, 2] | ['4', '1', '4'] |
| q-65167 | $x{y}^{2}-2yz+z$ | [1, -1, 1] | ['1', '-4', '3'] |
| q-131115 | $\sqrt{xy}+\sqrt{yz}$ | [1, 4, 1] | ['1', '1/2', '1'] |
| q-65168 | $x{y}^{2}+y{z}^{2}+{x}^{2}z$ | [-1, 1, -1] | ['3', '-1', '-1'] |
| q-71403 | $\sqrt{{x}^{2}+{y}^{2}+{z}^{2}}$ | [3, 4, 0] | ['3/5', '4/5', '0'] |
| q-71404 | $\operatorname{ln}⁡({z}^{2}-xy)-yz$ | [1, -2, 0] | ['1', '-1/2', '2'] |
| q-131119 | $x{e}^{y}+y{e}^{z}+z{e}^{x}$ | [0, 0, 1] | ['2', 'E', '1'] |
| q-131117 | ${x}^{3}yz-xy{z}^{2}$ | [1, -2, 1] | ['-4', '0', '2'] |
| q-131116 | ${x}^{3}+{z}^{2}{y}^{2}+2z$ | [1, -1, -1] | ['3', '-2', '0'] |
| q-71396 | ${x}^{2}+{y}^{2}+{z}^{2}$ | [-1, 0, 1] | ['-2', '0', '2'] |
| q-71399 | ${e}^{x+y+z}+x+y+z$ | [0, 0, 0] | ['2', '2', '2'] |
| q-71397 | $2{x}^{2}+{z}^{2}-xy$ | [-2, -3, 1] | ['-5', '2', '2'] |

## 2. Shared mathematical pattern

For a differentiable scalar function of three variables, compute all three ordered partial derivatives and evaluate them at the given point. A nonzero gradient is perpendicular to the level surface f(x,y,z)=f(point). The response asks for **a normal vector**, so every nonzero scalar multiple qualifies. Equality to the gradient is a different criterion. If a unit normal were requested, either sign of the normalized gradient would qualify; this KP's observed sources do not request one.

## 3. Components and complete banks

`source-components.json` maps every original option to its field, original scalar/vector, and a complete coefficient-scaling recipe. For each component whose original gradient is nonzero, the explicit opaque observed pattern is (source option component / source gradient component) × current gradient component; components associated with zero original gradient remain their observed constants. This retains the observed expression pattern under point variation. A changed opaque evidence bank can acquire duplicate choices or multiple valid normals; it remains visibly ineligible and is never counted as normal bank correctness. It does not recover author intention and is **public evidence-only**, including original mathematically valid banks. It is never sampled as normal practice. The same fixed worked solution applies regardless of selected answer.

The separately authored complete default bank consists of the computed gradient, omitting its x partial, omitting its y partial, omitting its z partial, and omitting its x and y partials. These are actual missing-component operations in the assessed gradient method. The complete bank is selected before point/coefficient sampling; a zero partial, zero option, duplicate option or second valid normal rejects the whole instance. No replacement distractor or first-valid pooled recipe is used. Source-choice correctness is independently checked by full vector parallelism, never UUID equality alone. All 13 original field banks have exactly one valid normal; the old q-37570 field lacks a recorded designation, which cannot be counted as matched.

## 4. Reusable template and constraints

Observed easy templates keep the actual function and symbolic partial masks, parameterize all point occurrences, and use explicit per-family substituted-component masks. The original five ordered aligned stages and shared prose are retained in normal variants. Each final row and final prose vector is separately re-rendered; formerly absent zero components are added when a changed point makes them nonzero. The complete original source strings are preserved at original values through these same masks, without a source payload return branch.

Normal easy integer points have magnitude at most 4, with cyclic exponential points limited to -1,0,1. Root-product points may use 1,4,9, preserving familiar exact square roots; products must be positive perfect squares. Radial-root points require a nonzero perfect-square norm radicand. Function-domain, finite-real evaluation and nonzero-gradient guards apply to explicit and sampled inputs. Moderate uses coefficients of magnitude 1..3 and coordinate magnitudes 2..3. Hard uses those same coefficients and nonintegral rational coordinate magnitudes 1..3 with reduced denominators 2 or 3. All six coefficients stay nonzero before any final cancellation.

Normal solution repairs are minimal and are distinct from source fidelity: q-131115 removes the unsupported trailing plus from the y formal derivative argument; q-65168 removes one unmatched closing parenthesis in the substituted y component; q-131117 corrects the introductory point (1,-1,2) to the actual displayed point. q-37570 removes a legacy duplicate assessment field only in normal authored records. No source bank is claimed mathematically ambiguous. Decoded backslash runs were measured as one character in answer strings; serialized visual escaping is not a defect and no escape repair is claimed.

Normal content identity hashes actual displayed prompt, fixed solution, complete bank, designation and difficulty, ignoring seed/order. Mathematical task identity uses normalized symbolic partials and point/criterion and excludes bank/profile and incidental common function scalar/constant aliases. Answer coefficients that are sums receive grouping to preserve their complete vector component meaning under changed signs.

Variety bounds: every source family is served by defaults. Root-product normal points have 27 familiar square-coordinate tasks. The radial root has 48 signed coordinate tasks from permutations of (1,2,2) and (2,4,4), all with the same exact-root workload. Cyclic exponential points are a finite 27-point candidate domain; explicit enumeration found 20 eligible tasks after complete-bank guards. Other easy integer-point families have up to 729 candidates each before guards. Moderate has 6^6×4^3 candidates and hard has 6^6×|R|^3, with R the documented reduced rationals; these are candidate bounds, not a claim that all banks qualify or that every function scalar alias is substantive. Validation reports measured independent task counts separately.

No variable/function-name/unit aliases are used to inflate task counts. No source difficulty labels are changed. No gradient-field, tangent-plane or normal-line question is authored.
