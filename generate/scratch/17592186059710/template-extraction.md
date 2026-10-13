# Template extraction — frozen math basis 1356

## 1. Specific descriptions before generalizing

q70401: prompt `Find $a + b$ if $a = 7i - 6j$ and $b = 3i + 2j$.` Two full integer vectors; one negative coordinate; two coordinate additions; original five-choice radio `selection`. Bank: 10i+4j, −4i−8j, 4i−4j, 10i−4j, 4i+4j. Correct value independently computed as (10,−4); no captured correct ref, difficulty, or worked solution.

q70402: `Find $2a + b$ if $a = 4i + 2j$ and $b = 6i - 4j$.` Scale a by2 then add b, with exact j cancellation. Same five-choice radio layout. Bank: 2i−2j, 6j, 14i+2j, 14i, 14i−2j. Correct value independently (14,0); no captured designation/difficulty/solution. Original widget confirms all five values. The 6j option has unresolved intention.

q125086: `Find $a+3b$ if $a=8i-5j$ and $b=-3i+2j.$` Easy; scalar only on b; two negative coordinates; final −i+j (unit coefficients elided). Fields absent. Full fixed source solution: opening “To compute $a+3b,$ we just need to compute all of the $i$'s and $j$'s, as follows:”, substitution (8i−5j)+3(−3i+2j), distribution 8i−5j−9i+6j, collection (8i−9i)+(−5j+6j), reduction −i+j. Source compact aligned layout and comma/period positions remain exact.

q125088: `Find $3a-2b$ if $a=-2i-2j$ and $b=4i-3j.$` Easy; scales on both vectors with subtraction of the second; cancellation in j. Fields absent. Same shared opening with the actual operation. Rows: 3(−2i−2j)−2(4i−3j), −6i−6j−8i+6j, (−6i−8i)+(−6j+6j), −14i+0j, −14i. The extra zero-coordinate row is retained at cancellation, not collapsed by CAS.

Decoded strings were inspected directly: q125086 slash-run lengths [1,2,2,2,1] and q125088 [1,2,2,2,2,1]. These are ordinary single-slash commands and double-slash row separators, **not** doubled TeX command bytes. No TeX escape repair is warranted or applied. Captured bold notation in the canonical example is contextual; practice sources use bare a,b,i,j and normal families keep that notation.

## 2. Generalized shared pattern and purpose

Compute a supplied two-dimensional component-form linear combination by substituting whole vectors, distributing integer scalars over both coordinates, collecting i and j terms separately, then reducing arithmetic. Required response is the complete vector expression, not a magnitude, angle, scalar product, or coordinates inferred from a figure. Prompt/worked masks retain distinct layouts; bank profiles are separate from masks. Complete solutions are fixed independent of learner choice.

## 3. Components and complete bank maps

Parameters are complete components ax,ay,bx,by and only scalars that actually appear. Add uses implicit p=q=1 and **rejects** unused p/q input aliases; left uses explicit p and implicit q=1; right uses q and implicit p=1; both uses p,q. Five-option profiles contain one independently correct value and four full wrong vectors. All original answer UUIDs, exact spellings, inferred correctness and parameterized operations are mapped in source-distractor-ledger.json; no option was discarded.

Let X=p ax+q bx and Y=p ay+q by where the family's missing scalar is1.

| Complete profile | Ordered mathematical values | Interpretation / learning eligibility |
|---|---|---|
| q70401 / observed-add | (X,Y); (ax−bx,−ay−by); (X,−Y); (bx−ax,ay−by); (ax−bx,Y) | Complete sign/subtraction operations on displayed components. Hypotheses, not recovered original intent. Eligible with pairwise distinctness. |
| q70402 historical | (X,Y); (X,ay); (X,−ay); (bx−ax,ay+by); (0,bx) | Exact observed expression-pattern replay. Keeping ±ay/using bx as y is underdetermined; opaque whole bank evidence-only. |
| authored add | (X,Y); (ax−bx,ay−by); (X,−Y); (ax−bx,Y); (X,ay−by) | Complete add/subtract/sign operations from displayed method. |
| authored scaled / flat-three | correct; omit one nonunit scalar; reverse the final whole term; scale x only; scale y only | Let ws,vs be actual printed linear weights/vectors. Pick the first nonunit weight index k; wrong=(X+(1−wk)vkx,Y+(1−wk)vky), then correct−2 wn vn, then (X,Σvy), then (Σvx,Y). First nonunit selection is a deterministic recipe, not a pooled-option fallback. |
| authored nested-three | correct; p a−q b−q r c; p a−q b+r c; p a−q b+q c; (X,ay+by+cy) | Outer sign, omitted outer distribution on c, omitted inner scalar, and scale-x-only errors. |

At anchor parameters q70401 yields exact full bank (10,−4),(4,4),(10,4),(−4,−8),(4,−4). q70402 yields (14,0),(14,2),(14,−2),(2,−2),(0,6). The “correct” label here is independent mathematical inference: it cannot count as a source-designation match. The q125 sources have no observed banks; all completed answer fields/banks are authored. The API retains all raw omissions and tags every raw/opaque profile `evidence_only=true`, `eligible_for_learning=false`.

Normal q70401 default may use its complete defensible source-shaped operations or the separately labeled authored bank. Normal q70402 uses its original left-scaled prompt mask plus the complete authored distribution bank. All four eligible observed masks are reached by default sampling. Opaque historical profiles never enter default sampling, even when their five numeric values are distinct.

## 4. Reusable masks, constraints and consistency calculations

Fixed components: “Find ... if ...”; basis i,j; radio key `selection`; complete five-option math bank; shared opening; ordered substitution, distribution, component collection and reduction; one fixed solution. Variable slots: complete linear combination, complete a/b (or authored c) vector, complete substituted terms and complete intermediate/final rows. Never global-replace short numeric strings. Conditional components: unit coefficient elision; plus/minus separators; grouped negative coefficients; explicit zero-component intermediate row before final omission. Compact q125 aligned masks reproduce both full source worked solutions byte-for-byte at anchors.

Two missing radio solutions are authored using the canonical formal substitution/distribution/collection/conclusion sequence and clearly labeled. Two missing fields are authored supported radio completions; no original blank layout is claimed. Raw source records retain absent difficulty, fields, solutions and correct refs. Generated identity UUIDs and normalized enum strings replace storage identities/enums; source identifiers/provenance remain author metadata. Fidelity checks concern all public content attributes and omissions, not reusing original EDB storage IDs.

Easy bounds: full nonzero signed integer input coordinates of magnitude≤12; displayed scalar magnitude1..3 when explicit, default nonunit2..3. This retains all observed anchors, signed vectors, unit outputs, and cancellation stages. The canonical sparse b=12i shows omitted-component semantics but is not an additional practice family or claimed default bank. Normal bounds deliberately avoid absent input components to keep each sampled family’s multiplication workload stable.

Authored moderate/hard constraints and curriculum rationale are in classification.md and in separate generator sections. Moderate has exactly three scaled full vectors, flat weights of magnitude2..4, coordinates≤9. Hard uses exactly p a−q(b−r c), with p/r signed2..3, q positive2..3, coordinates≤6; it prints inner evaluation before expanded distribution and collection. Explicit calls enforce every bound. No rational-arithmetic branch, geometry or notation migration is introduced. Default scalar sign variants are unordered same-workload variations.

The eligible family/complete bank is selected **before** parameters. Any duplicate full vector answer, wrong option equal to the correct value, or final-coordinate ceiling failure rejects the whole instance; explicit inputs raise instead of resampling. Bank recipes are not randomly perturbed values. Seeds only sample/shuffle; fixed displayed content has stable identity. Complete bank/profile aliases that produce identical display cannot alter identity. Math fingerprints include actual operands and flat/nested operation structure; bank, seed, notation and unused scalar aliases do not inflate task counts.

Validation independently parses the actual printed expression and supplied components; substitutes vectors; checks every answer and correct designation; compares every ordered distributed component term, each solution row and final result; checks exact source prompt/bank/solution and omission parity; tests mutation controls, explicit boundary failures, deterministic identity, unrestricted default coverage and radio position coverage. Native checks separately use the real application grader on completed/normal fields. Raw records lacking fields/correct refs are ungradable evidence, not native successes. No source designation has a nonzero fidelity denominator. The large numeric domain is sampled broadly; validated distinct-task counts are honest lower bounds rather than exhaustive-domain counts.
