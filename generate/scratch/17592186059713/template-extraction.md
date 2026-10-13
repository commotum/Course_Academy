# Four-stage extraction

Frozen source: math basis 1356, lineage as in `source.json`. Parameterized public source cases are in `source-cases.json`; complete raw replay is produced by the ordinary `generate` API with `raw-q-*` profiles. No source payload lookup branch supplies a literal answer or solution.

## 1. Describe each observed question

q-1300: two signed-integer 2D vectors, u=⟨-3,1⟩ and v=⟨4,6⟩, displayed with lower-case overset arrows. The prompt is “If … and …, then …=” in three inline math fragments; no blank placeholder or field exists in the capture. Solution opening: “To compute the result, we just need to perform the required operations with each component separately:” followed by a compact three-row aligned chain: vector substitution, individual component addition, collected tuple ⟨1,7⟩.

q-1324: same sequence using upper-case overset U,V, vectors ⟨1,3⟩ and ⟨6,3⟩, result ⟨7,6⟩. Captured easy label; answer-fields omitted. Equal y-components are preserved as an observed feature, not imposed on the sampler.

q-1323: historical arrow serialization u^(→),v^(→), vectors ⟨4,1⟩,⟨1,-4⟩ and subtraction u-v. The response is a full angle-bracket vector. Five radio math values under `selection`, detailed below; no captured difficulty, correct reference or solution. The original widget matches the five complete values.

q-1386: historical v^(→)=⟨8,-7⟩ and scalar multiplication 3v. Five radio math choices under `selection`; difficulty, correct designation and solution omitted. Original widget matches the complete bank. Signs and nonunit scalar define the arithmetic workload.

No practice source has a plot or an image choice. The canonical raster is separately inspected in `plot-extraction.md`.

## 2. Generalized mathematical patterns

Sum: identify arrow-labelled vectors with their given ordered coordinate pairs and add corresponding components. Subtraction: subtract the second pair componentwise while retaining signs. Scalar: distribute the given scalar into both components. These are three assessed families and four source rendering masks (letter case is incidental). Source tuples are not basis-vector expressions or column vectors; outputs remain complete coordinate pairs.

Normal authored levels use the same representation and componentwise method: moderate pu±qv; hard pu-(qv±rw). The scalar-product count, not larger incidental labels or parameter aliasing, separates their workloads.

## 3. Map components and all complete banks

Write a=(aₓ,aᵧ), b=(bₓ,bᵧ); z is the independently computed correct vector. Observed raw options preserve their exact spacing and signs at the source parameters. Answer choices are whole ordered pairs, compared one-to-one; captured order is irrelevant.

| Source/profile | Original complete value | Parameterized operation | Interpretation status |
|---|---|---|---|
| raw-q-1323 | ⟨3, 5⟩ | z=a-b | correct value independently inferred; no captured designation |
| raw-q-1323 | ⟨4,-4⟩ | (aₓ,bᵧ) | opaque coordinate-selection evidence |
| raw-q-1323 | ⟨ - 3,-3⟩ | (-zₓ,aᵧ+bᵧ) | mixed-operation replay; intention unresolved |
| raw-q-1323 | ⟨3,-5⟩ | (zₓ,-zᵧ) | inferred final-y sign flip |
| raw-q-1323 | ⟨1, 3⟩ | (bₓ,aₓ-bₓ) | opaque selector/cross-component evidence; intention unresolved |
| raw-q-1386 | ⟨24,-21⟩ | n a | correct value independently inferred |
| raw-q-1386 | ⟨ - 24, 21⟩ | -n a | inferred negated scalar |
| raw-q-1386 | ⟨11,-4⟩ | a+(n,n) | inferred componentwise addition instead of scaling |
| raw-q-1386 | ⟨ - 24,-21⟩ | (-n aₓ,n aᵧ) | inferred x sign flip after scaling |
| raw-q-1386 | ⟨ - 11, 4⟩ | -a-(n,n) | inferred negated componentwise scalar addition |

All 10 displayed values reproduce exactly at original parameters. The subtraction profile is evidence-only, including changed-parameter replay; the numerical selectors are not claimed to recover a defensible learning bank. The scalar profile has a full operation-derived interpretation, labeled inferred rather than recovered author intent, and supports normal sampling. Each raw profile has explicit `evidence_only=true`, `eligible_for_learning=false`; neither fills missing raw fields/refs or difficulty.

Complete authored banks are fixed and not selected from a first-valid pool:

| Family | Complete five-vector bank |
|---|---|
| sum (both cases) | a+b; a-b; b-a; (aₓ+bₓ,aᵧ-bᵧ); (aₓ-bₓ,aᵧ+bᵧ) |
| subtraction default | a-b; a+b; b-a; (aₓ-bₓ,aᵧ+bᵧ); (aₓ+bₓ,aᵧ-bᵧ) |
| scalar default | n a; -n a; a+(n,n); (-n aₓ,n aᵧ); -a-(n,n) |
| moderate | p a+s q b; p a-s q b; a+s q b; p a+s b; (p aₓ+s q bₓ,aᵧ+s bᵧ) |
| hard | p a-(q b+s r c); p a-q b+s r c; p a+q b+s r c; a-(q b+s r c); p a-(b+s c) |

Moderate errors reverse the combining sign, omit one scalar or omit both y-scalars. Hard errors omit distribution of the outer minus on the final term, omit outer subtraction, omit the first scalar, or omit inner scalars. Those are errors in the displayed operation, not arbitrary perturbations. No invented option diagnosis appears in learner text.

## 4. Reusable masks and constraints

Fixed opening and inline fragment layout follow the sources. Variable components are complete arrow labels, complete tuples, scalar coefficients, binary operation signs and full solution stage components. No global replacement of individual digits or variable letters is used. Negative numeric factors and subtracted negative components are parenthesized; coefficient-coordinate multiplication uses `\cdot` to prevent accidental numeric concatenation.

Easy sum chain: labelled formal operation = pair + pair → pair of two unevaluated sums → collected pair. It retains the original compact aligned structure and exact source sentences/rows. Subtraction completion adds formal operation → vector substitution → individual component subtraction → collected pair (three rows after the formal LHS shares the first). Scalar completion adds vector substitution → individually distributed products → collected pair, borrowing the common source instruction while acknowledging absent original solution evidence.

Moderate chain has four aligned rows: vector substitution; four individually distributed products in ordered x/y components; individually evaluated signed products; collected pair. Hard has six: vector substitution; six distributed component products with nested signs; individually evaluated three vector terms; inner collected vector; ordered component subtractions; final collected pair. These extra levels are authored, not literal recovered source chains. Whole solution is fixed regardless of the learner's selected error.

Sampling and explicit guards: easy coordinates -9…9; scalar n from ±2…±6. Moderate nonzero coordinates ±1…±6, p,q in 2…6, s=±1. Hard nonzero coordinates ±1…±6, p,q,r in 2…4, s=±1. Maximum absolute displayed choice component 120. Distinct complete vectors are required throughout each bank. Any missing, equivalent or invalid member rejects the whole sampled instance; explicit invalid parameters fail instead of resampling. Raw fieldless evidence has no hidden authored-bank collision restriction.

The unfiltered finite parameter domains contain 19⁴=130,321 easy coordinate pairs for each sum/subtraction family, 361×10=3,610 scalar inputs, 12⁴×25×2=1,036,800 moderate inputs and 12⁶×27×2=161,243,136 hard inputs. Those are domain sizes, not claimed eligible-bank counts. QA reports measured unique valid tasks among sampled records (lower/upper sum aliases deduplicated), rather than multiplying by notation or bank profiles. These broad signed integer domains provide repeated-practice variety without a new method. All level guards apply to public explicit parameters.

Identity uses generator version, actual prompt, actual fixed solution, complete displayed bank, difficulty and raw/normal presence state. Choice ordering/seed is excluded. Mathematical fingerprints exclude banks/profiles/letter-case aliases but retain coefficients, ordered coordinates and operation grouping. Local raw `:db/id` and Math Academy IDs are captured provenance only; generated UUIDs are stable content identities and none of these records are transaction data.

## Validation and limits

`validate.py` reads coordinates and requested operation from actual prompt fragments, then independently checks formal operation, every solution row, individual distributed products, intermediate vector shape and collected conclusion. It verifies complete bank operation values, unique mathematical choices and owned correct refs, original key-presence parity, exact original solution prose/row sequence, explicit workload guards, normal family coverage and deterministic identities. Mutations of a prompt coordinate, distributed sign, choice collision, final conclusion and correlated individually evaluated vectors (preserving the final total) must fail. Native grading is an independent selection check and is never counted as mathematical proof.

No captured correct designation exists in either original bank: matched designation denominator is 0, with 2 missing refs reported. Four raw records remain ungradeable; four separately completed original instances exercise the native grader. No mathematical source error was found. The two missing fields and two missing correct refs/solutions are source-format omissions, not silently repaired raw evidence.
