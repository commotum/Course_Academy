# Four-stage template extraction

Frozen database math, basis 2275, lineage as recorded in `source.json`. Four MA originals are covered by `source-cases.json`; five exact independent inventory records are separate in `independent-inventory.json`. `choice-map.json` records every source option, full value, recipe and field, including all wrong values.

## 1. Describe each original specifically

q-1300: u=⟨-3,1⟩, v=⟨4,6⟩, lower-case overset arrows, componentwise sum. Prompt uses three inline fragments in “If … and …, then …=”. The easy label exists; answer-fields do not. Worked solution has the exact common opening, then compact aligned substitution, two unevaluated component sums, and collected ⟨1,7⟩.

q-1324: upper-case overset U,V; vectors ⟨1,3⟩,⟨6,3⟩, sum ⟨7,6⟩. Equal y-coordinates are an original parameter feature, not an inferred sampler constraint. Same three-row solution/prose and fieldlessness; captured easy.

q-1323: historical u^(→),v^(→); vectors ⟨4,1⟩,⟨1,-4⟩; subtraction u-v. Single selection radio with five full coordinate pairs; no rating, solution or correct ref. Ordered components and negative second y-coordinate are substantive arithmetic inputs.

q-1386: historical v^(→)=⟨8,-7⟩ and scalar 3; response is 3v as a full coordinate pair. Five radio choices; rating, solution and correct ref absent. Both products are nonzero and the scalar is nonunit.

The five independent records are complete easy inventory variants of the same sum and scalar masks: (8,2)+(-1,8); (-5,-2)+(-2,-1); -4(-4,4); (6,1)+(-3,4); 5(8,-5). Their whole worked solutions use the exact source-shaped sum/scalar stages, and their banks use the method-derived operations below. They are not additional recovered MA templates. Every record is inspected and publicly replayed; exact captured copies remain inventory evidence.

## 2. Generalized backbone and required response

Observed backbone: supplied arrow-labelled vectors with ordered integer coordinate pairs; requested sum, subtraction or nonunit scaling; response is a complete coordinate pair. Sum/subtraction identifies corresponding coordinates and performs one ordered arithmetic operation in each. Scalar multiplication distributes the given scalar into both components. Lower/upper label case does not alter the task.

Authored missing moderate backbone: two supplied nonzero integer pairs, positive nonunit p,q, and pu±qv; distribute four products, evaluate products, collect two coordinates. Authored hard backbone: three supplied nonzero integer pairs, positive nonunit p,q,r, and pu-(qv±rw); six products, evaluate each scaled pair, collect inner pair, apply outer subtraction, collect final pair. Both are scalar/addition operations already demonstrated by the canonical and preceding lesson route; they are authoring decisions, not inferred original difficulty labels. Vary only the declared coefficient, coordinate and sign slots. Never alter grouping, number of supplied vectors, answer shape or solution stages within these backbones.

## 3. Complete component and choice-bank mapping

Let a=(aₓ,aᵧ), b=(bₓ,bᵧ), c=(cₓ,cᵧ), and compute correct z before wrong values. Source spacing below is retained exactly in raw replay.

| Raw original bank | Source complete value | Parameterized operation | Interpretation |
|---|---|---|---|
| q-1323 | ⟨3, 5⟩ | z=a-b | independently inferred correct value; designation missing |
| q-1323 | ⟨4,-4⟩ | (aₓ,bᵧ) | opaque coordinate selector, evidence-only |
| q-1323 | ⟨ - 3,-3⟩ | (-zₓ,aᵧ+bᵧ) | mixed-operation replay, intention unresolved |
| q-1323 | ⟨3,-5⟩ | (zₓ,-zᵧ) | inferred final-y sign flip |
| q-1323 | ⟨1, 3⟩ | (bₓ,aₓ-bₓ) | opaque cross-coordinate selector/difference |
| q-1386 | ⟨24,-21⟩ | n a | independently inferred correct value |
| q-1386 | ⟨ - 24, 21⟩ | -n a | inferred reversed scalar sign |
| q-1386 | ⟨11,-4⟩ | a+(n,n) | inferred scalar addition instead of multiplication |
| q-1386 | ⟨ - 24,-21⟩ | (-n aₓ,n aᵧ) | inferred scaled-x sign flip |
| q-1386 | ⟨ - 11, 4⟩ | -a-(n,n) | inferred negated scalar-addition result |

All original 10 values match exactly, including eight wrong choices. The entire opaque q-1323 bank is replay-only; its selectors are numerical evidence, not claimed recovered educational recipes. The scalar bank has a complete defensible method-operation interpretation, labeled inferred. Each raw original and inventory profile carries `evidence_only=true`, `eligible_for_learning=false` even when its mathematical bank is usable. Normal profiles are separately marked eligible.

Complete normal banks, fixed before parameters, are:

| Template/profile | Five operations, including correct first in construction |
|---|---|
| sum_lower/sum_upper, component_bank | a+b; a-b; b-a; (aₓ+bₓ,aᵧ-bᵧ); (aₓ-bₓ,aᵧ+bᵧ) |
| subtract, component_bank (authored) | a-b; a+b; b-a; (aₓ-bₓ,aᵧ+bᵧ); (aₓ+bₓ,aᵧ-bᵧ) |
| scalar, scalar_source_bank | n a; -n a; a+(n,n); (-n aₓ,n aᵧ); -a-(n,n) |
| linear_combination, distribution_bank (authored) | p a+s q b; p a-s q b; a+s q b; p a+s b; (p aₓ+s q bₓ,aᵧ+s bᵧ) |
| nested_combination, nested_bank (authored) | p a-(q b+s r c); p a-q b+s r c; p a+q b+s r c; a-(q b+s r c); p a-(b+s c) |

Moderate wrong operations reverse the combining sign, omit the first scalar, omit the second scalar, or omit both y-scalars. Hard wrong operations fail the outer minus on the final term, omit outer subtraction, omit first scaling, or omit both inner scalars. These derive from the actual printed method, not answer perturbations. Learner choices have no invented feedback/diagnoses.

Independent inventory sum banks are precisely the above complete sum bank, and scalar banks the above complete scalar bank. `choice-map.json` joins all 35 captured values across seven complete banks to their exact field/value/recipe and designation-presence status. `independent-replay.json` verifies five captured correct designations independently of missing original refs. No fieldless original is assigned a fabricated original bank.

## 4. Slots, reusable masks and guards

| Slot | Role/domain | Dependent parts |
|---|---|---|
| a,b coordinates (easy) | integer -9…9, two coordinates each | definitions, corresponding operation operands, all choices, intermediate and final tuples |
| n (easy scalar) | ±2…±6, nonunit scaling | requested scalar, both distributed products, whole bank and result |
| a,b (moderate) | nonzero ±1…±6 coordinates | supplied pairs, four ordered products, evaluated terms, collection and errors |
| p,q (moderate) | integers 2…6 | nonunit products remain substantive in all four component slots |
| a,b,c (hard) | nonzero ±1…±6 coordinates | three definitions, six products, individual evaluated pairs, inner pair, outer subtraction and all errors |
| p,q,r (hard) | integers 2…4 | fixed three-term scaling workload |
| s (moderate/hard) | +1 or -1 combining sign, same workload | requested sign, distribution, evaluation, inner arithmetic and complete bank |
| label case | lower/upper sum masks from originals | cosmetic prompt/solution references only; excluded from content/math identity |

The source common opening is fixed: “To compute the result, we just need to perform the required operations with each component separately:”. Normal sum solutions keep the exact compact three-row source chain. Missing subtraction/scalar solutions are explicit authored completions with substitution, individually performed component operations and final collection. Every instance has one concrete solution independent of selected choice.

Moderate solutions have four rows: vector substitution; four unevaluated distributed products in ordered x/y components; individually evaluated signed products; collected pair. Hard has six: vector substitution; six individually distributed products; three individually evaluated vector terms; inner collected pair; componentwise outer subtractions; final collected pair. Numeric factors use visible `\cdot`, and negative factors/subtracted negative coordinates are parenthesized. Components are rendered as complete slots; no blind digit or short-expression prose replacement is used.

All sampled and explicit inputs obey the same level guards. Five complete vectors must be mathematically distinct pairwise; full coordinate equality, rather than direction/parallel equivalence, is the response criterion. Reversed-vector and scalar-sign errors can coincide, so any collision rejects the whole bank. No first-valid pooling or replacement of one option occurs. Displayed choice components are bounded by 120 (actual supported workloads remain below that bound). Raw fieldless originals have no invisible authored-bank restriction; their missing field stays absent.

Source replay masks reconstruct actual strings from parameters and recipes. q-1323/q-1386 retain historical spelling and raw omissions; no branch returns the captured payload or an answer table. Independent replays use the supported normal masks, preserving complete source prose and banks at their parameters while retaining their no-MA-id attribute omission.

Content UUIDs use version, difficulty, actual prompt/solution with cosmetic upper/lower vector case normalized, complete displayed bank independent of order, and raw presence state. Seed and profile aliases do not create identity. `presentation_fingerprint` retains exact displayed spelling for review. Mathematical fingerprints exclude banks/order/case and conservatively deduplicate sum operand swaps, scalar-factor aliases with the same result, and moderate positive-sum operand swaps. Stable task fingerprints retain requested operator grouping and substantive parameters otherwise. Different bank content changes identity; changing only labels does not inflate capacity.

## Variety and verification limits

Exact independent enumeration gives 115,668 valid parameter sets for each easy sum/subtraction profile, collapsing to 63,342 sum mathematical tasks after operand-swap aliases; subtraction retains 115,668. Scalar has 3,228 valid parameter sets and 1,406 distinct results under conservative factor-alias deduplication. Lower/upper masks are never added as a second sum capacity. Moderate and hard have witnessed lower bounds of 1,599 and 1,600 valid distinct same-method tasks, with explicit parameters in `capacity-witnesses.json`. Unfiltered domains of 1,036,800 and 161,243,136 are reported as domain sizes, not valid-bank counts. Coverage exercises both signs, every scalar value and every allowed coordinate value for authored slots.

`validate.py` reads actual displayed definitions/operation and every equality row independently. It checks the two components of each substituted vector, every separately distributed product, individually evaluated primitive vector terms, inner reduction, component subtractions, final conclusion, every displayed choice and the actual correct reference. Structure checks prevent replacing a required row by an algebraically equal collapsed stage. Mutations include correlated intermediate errors that leave the final result unchanged and an unintended C0 character. It compares complete original solution prose, row sequence and attribute presence exactly, and retains separate inventory denominators. Real native choice grading is memory-only and supplementary to mathematical checks. No DB writes, registration, engine edits or changes to registered files occur.
