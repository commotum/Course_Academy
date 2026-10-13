# Template extraction — four stages

## 1. Specific source descriptions

q1304: u=⟨12,5⟩, v=⟨9,−2⟩; subtract two components. “If … and …, then u−v=” has no terminal period. One selection radio has five whole vector responses and no correct designation; no solution or difficulty attribute exists. Frozen answer order differs from widget order, so banks are sets for fidelity, while whitespace spellings remain exact.

q17611: a=⟨−2,1⟩, b=⟨4,−1⟩; compute a+2b. “Let … and … . Find … .” Two products precede two additions. One five-choice selection radio lacks correct ref, worked solution and difficulty. Both component signs matter.

q1301: arrow-labelled A=⟨10,5⟩, B=⟨8,−2⟩; sum. Easy, no field attribute. Prompt has question mark inside the final inline math. Source prose “To compute …, we just need to perform the required operations with each component separately:” precedes a two-row aligned block: direct vector substitution, then⟨18,3⟩. No extra component-arithmetic row is inserted.

q1389: A=⟨4,1/2⟩; compute−4A. Easy, no field attribute. Same shared prose, then three aligned rows: scalar times supplied vector; separately printed (−4)·4 and (−4)·1/2; evaluated⟨−16,−2⟩. Parentheses preserve the signed scalar multiplication. Fraction remains exact.

## 2. Generalized pattern

Use supplied two-dimensional angle-bracket components to perform the requested addition, subtraction or scalar multiplication separately, returning one whole angle-bracket vector. Sum and scalar retain their distinct source prose/layouts and stage counts. The existing radio families retain their prompt masks and full five-option banks. Missing fields/solutions are author completions, not observed templates. No equations, basis notation, column representation, diagram reading, or magnitude/direction computation is assessed.

## 3. Component and complete-bank maps

Let a=(a₁,a₂), b=(b₁,b₂), c be the correct vector. Every recipe listed here is applied as a complete bank, with collision rejection for the whole instance. Operation interpretations are plausible explicit generalizations of observed values; the authoring intent is not claimed recovered.

### Observed subtraction bank — q1304 (`subtract_observed`)

| Complete captured value | Parameterized operation | At source parameters | Role |
|---|---|---|---|
| ⟨3,7⟩ | (a₁−b₁,a₂−b₂) | (12−9,5−(−2)) | independently inferred correct |
| ⟨3,3⟩ | (a₁−b₁,a₂+b₂) | (12−9,5+(−2)) | add second component |
| ⟨−3,7⟩ | (b₁−a₁,a₂−b₂) | (9−12,5−(−2)) | reverse first subtraction |
| ⟨21,7⟩ | (a₁+b₁,a₂−b₂) | (12+9,5−(−2)) | add first component |
| ⟨21,3⟩ | (a₁+b₁,a₂+b₂) | (12+9,5+(−2)) | add both components |

All five exact mathematical values and original whitespace spellings are reproduced. Normal worked solution is authored using source shared prose and the canonical componentwise sequence: substitution, signed component arithmetic, result. Raw replay omits it.

### Observed one-scaled-vector bank — q17611 (`linear_observed`)

Here c=a+kb, k=2 at source.

| Captured value | Parameterized operation | At source parameters | Role |
|---|---|---|---|
| ⟨6,−1⟩ | (a₁+kb₁,a₂+kb₂) | (−2+2·4,1+2·(−1)) | independently inferred correct |
| ⟨10,−1⟩ | (−a₁+kb₁,a₂+kb₂) | (2+8,1−2) | negate first a component |
| ⟨10,−3⟩ | (−a₁+kb₁,−a₂+kb₂) | (2+8,−1−2) | negate both a components |
| ⟨6,−3⟩ | (a₁+kb₁,−a₂+kb₂) | (−2+8,−1−2) | negate second a component |
| ⟨6,1⟩ | (c₁,−c₂) | (6,1) | reverse final second sign |

Five exact values and whitespace spellings replay. The scalar, signs, complete vector slots and target operation vary; no unrelated random perturbation or opaque number fit is used. Normal solution is authored: substitution, evaluated scaled vector, separately printed signed component sums, result. Its four stages follow canonical e4293.

### Authored complete banks for missing fields/level

`sum_method`: c=a+b; wrong vectors (a₁−b₁,c₂), (c₁,a₂−b₂), a−b, (c₂,c₁). These are actual addition/component errors. `scalar_method`: c=ka; wrong vectors (ka₁,a₂), (a₁,ka₂), −ka, (a₁+k,a₂+k). These represent scaling only one component, scalar sign reversal, or adding the scalar instead of multiplying.

`hard_method`: c=ra+kb; wrong vectors a+kb, ra+b, ra−kb, (ra₁+kb₂,ra₂+kb₁). These omit one requested scaling, reverse a scalar's sign, or exchange the second vector's coordinates. Four wrong recipes are selected together before parameter generation. Source replay for fieldless questions omits all invented choices; the normal authored banks are separately marked.

## 4. Reusable masks, constraints and calculation sequence

Complete mathematical slots are vectors, scalar coefficients, requested vector expression, arithmetic component row, and complete result vector. Prose is fixed except the complete target expression. Every conclusion is recomputed; no final original value survives a changed input. Integer/fraction rendering and grouping distinguish multiplication from numeric concatenation and avoid bare +− or −−. Aligned chains preserve source row counts for sum/scalar; authored two-vector chains preserve distribution, evaluated scaled vectors, component arithmetic and final result as separate strings, simplifying only the final values.

Easy integer-vector components are signed nonzero integers of magnitude1..15, matching the familiar two-digit source arithmetic. Scalar uses first component integer1..15 in absolute value, second component a noninteger half with absolute value≤15; scalar is a signed integer of absolute magnitude2..5. This retains exactly two products and an exact half arithmetic operation. Moderate integer components have magnitude1..15, scalar signed magnitude2..5; exactly two products and two additions. Hard integer components have magnitude1..8, both signed scalars magnitude2..4; exactly four products and two additions. The smaller hard magnitudes limit arithmetic size while increasing bookkeeping. Source originals fit these policies. All guards apply equally to explicit API parameters. Zero components and unit/zero scalars are excluded because they remove advertised work; fractions are not permitted outside the observed scalar family. A degenerate bank is rejected, never partly replaced.

There are no within-level stages or ordered learning progression. Defaults choose all observed supported easy families before their parameters. Each family has one complete defensible bank. Raw replay profiles are evidence-only. All normal output uses radio responses, including explicit author completions of fieldless sources. These profile labels cannot create identity differences when displayed content is identical.

### Meaningful variation catalog

The finite domains are substantive arithmetic operands: 30 signed integer values for each easy/moderate component;30 eligible signed noninteger halves for the scalar second component;8 signed nonunit scalar values. Hard has16 signed integer component values and6 signed nonunit coefficient values. Candidate counts before whole-bank rejection: sum/subtraction30⁴ each; scalar30·30·8; moderate30⁴·8; hard16⁴·6². These are upper bounds, not counts of valid unique tasks. The validator reports an independently checked lower bound of over1100 distinct canonical arithmetic tasks in1200 default seeds for each level. No notation variants, bank/profile aliases, unused variables, or copied same-answer distractors inflate that count.

Task fingerprints encode the individually evaluated component products and whether each supplied vector requires nonunit scaling, with commutative term sorting to deduplicate exchanged addition terms. They omit bank, presentation, seed and source alias. A common relabelling or profile alias leaves a task unchanged. Inverse rescaling of a supplied vector with its coefficient is deduplicated when its evaluated products and scaling workload agree; these scaling aliases do not inflate meaningful variety. Scalar products are likewise canonicalized while retaining the half-component workload tag. Content IDs additionally include actual prompt, solution, full bank, difficulty/attribute presence and version. Seed/shuffle never affects content IDs for fixed parameters/template/profile. Different displayed banks change content identity.

No plot extraction is needed: none of the four source practice questions or assigned canonical example contains any graphic.
