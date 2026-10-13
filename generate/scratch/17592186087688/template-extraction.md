# Template extraction

## 1. Describe each source before generalizing

q-214098 prints `The lines $y = 2x + 5$ and $kx + 3y = 9$ are parallel. What is the value of $k$?$k =$` followed by a newline and `{{field-1}}`. Known slope 2, intercept 5, unknown y coefficient +3, RHS 9. One blank with supplied `k =`; expected response is a scalar coefficient fragment, not an equation. No observed bank, correct designation, solution or difficulty. The mathematical inference is −k/3=2, giving k=−6. At that value the second line has intercept 3, so the lines are distinct.

q-214099 uses the same wording/blank but prints `8x - 2y =-2` and `kx - 5y = 15`. Both are standard form. Known slope 4, known intercept 1, known equation scale 2 relative to primitive 4x−y=−1. Unknown slope k/5, giving k=20. Its intercept −3 differs from 1. Same absent attributes. Preserve the first equation's tight equality spacing through its reusable source-style mask, including changed parameters; no anchor-only literal override.

Canonical e-14370 has a worked solution: shared parallel/equal-slope rule; read the known slope; original unknown equation; move kx to RHS; negate both sides when the y coefficient is negative; divide its magnitude; state the x coefficient; equate slopes; conclude k. Practice solution fidelity has denominator zero; authored practice solutions follow this teaching sequence and use aligned math in place of the canonical legacy `|`/`;` layout. If a known standard equation has y coefficient −1, omit a redundant sign-normalization row because the final isolation already performs that operation.

## 2. Generalize the shared assessed method

Known line has reduced slope m=n/d and integer intercept h. Unknown equation is kx+by=c, b≠0. Parallelism requires −k/b=m, so k=−bm. Intercepts must differ after substitution. The two observed information masks stay separate: known slope supplied explicitly, or known line supplied in standard form. The source response shape remains one scalar blank throughout.

## 3. Map components and complete banks

| Component | q-214098 | q-214099 | Parameterized operation |
|---|---|---|---|
| Known slope / intercept | 2 / 5 | 4 / 1 | m=n/d; h |
| Known standard scaling | Not displayed | 2 | a=n·s, d_y=−d·s, RHS=h·d_y |
| Unknown y coefficient / RHS | 3 / 9 | −5 / 15 | b / c |
| Unknown slope | Inferred −k/3 | Inferred k/5 | −k/b |
| Correct scalar | Inferred −6 | Inferred 20 | −bm, derived from prompt |
| Source field | blank field-1 | blank field-1 | Supplied `k =`, exactly one placeholder |
| Source choices | Attribute absent | Attribute absent | Remains absent in raw output |
| Source correct reference | Attribute absent | Attribute absent | Remains absent in raw output |
| Source solution / difficulty | Attributes absent | Attributes absent | Remain absent in raw output |

Complete observed answer-bank count: **0**. Original bank coverage is an empty denominator, not a passed bank comparison. There are no source choice values or distractor recipes to map; do not fabricate radio banks. Completed/authored banks contain one field-owned math answer with a correct lookup ref, computed from the actual algebra. `raw-q-214098`, `raw-q-214099` preserve missing content. `completed-q-214098`, `completed-q-214099` add supported completions with source-style spacing. `authored-blank` is the normal supported bank and renders both observed families through the authored level routing.

## 4. Reusable masks, calculations and limits

Fixed wording and the scalar blank layout are observed. Complete mathematical components vary: m, h, b, c, known scale s; no short textual replacement occurs. Signed coefficient terms and rational fractions render explicitly. Source q-214099's equality whitespace is a profile formatting choice. Raw replay reconstructs prompt/field structure through the normal generator, not copied payloads. Captured `:db/id` attributes remain in raw evidence; local identities are content-derived UUIDs. Enum dictionaries normalize to the required local enum strings. Attribute-presence parity is asserted per source.

Normal bounds: reduced nonzero m with |n|≤12 and denominator≤7; 2≤|b|≤9; h integer −12..12, c integer −15..15; primitive known scale 1. Source evidence/completion profiles allow scales 1..3, covering the original scale2. Easy/mid require integer m; hard requires denominator>1 and gcd(|b|,denominator)=1. Those guards apply equally to explicit inputs and sampling. They prevent unit-coefficient unknown isolation, hidden known-line GCF, and fractional hard solves cancelling to integer. Reject the whole instance if the given lines coincide. No default bank replacement or perturbation is used.

Known conversion stages preserve ordered original equation, moved-x row, optional sign-normalized row, isolation row. Unknown conversion uses the same stages with k. Shared source sentences precede slope equality and conclusion; an authored multiplication row explains coefficient isolation. The validator parses actual displayed equations and all prose coefficient claims independently, checks full equation equivalence up to nonzero scalar, rejects stale conclusions and a mathematically equal but structurally missing conversion stage, and checks exact native scalar grading.

Meaningful task fingerprints include assessed known-form information, reduced known slope and unknown y coefficient. Intercepts, known scaling, notation/profile aliases and seed are incidental and excluded. Content identity includes version, actual prompt, fixed solution, difficulty and full bank/omissions; changed banks/solution cannot share content identity. Finite meaningful domain counts are recorded by the implementation and exhaustively checked; default family coverage is one mixed family at easy and one two-standard family at moderate/hard.
