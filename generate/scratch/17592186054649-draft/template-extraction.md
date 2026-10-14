# Four extraction stages

## 1. Specific original descriptions

Every original operand, choice, correct designation, field key and solution appears in the immutable `source.json`; `review.md` prints each original beside two authored variants. `source-choice-mapping.json` inventories all **38** displayed values one-to-one, including all20 radio choices and18 blank fragments.

q-108 supplies signed2×3 operands [7,−4,9;1,10,−7] and [−8,6,−2;−4,3,−6]. Its correct mathematical result is [15,−10,11;5,7,−1], but the captured field has no correct reference, rating or solution. q-11478 supplies positive2×2 operands [4,3;1,2] and [1,2;3,4], result [3,1;−2,−2], likewise without those three attributes. Both have five radio matrices. The actual MA widget JSON has no answer key or explanation; deriving the key is authorship, not evidence of a captured designation.

q-11441 supplies [5,5;5,4]−[3,2;1,0], four nonnegative operand subtractions with result [2,3;4,4], an observed easy label and correct designation. The three source equality stages show input matrices, entrywise unevaluated differences, then results. q-69603 supplies [4,−8,1;−2,6,−9]−[−2,1,−10;−1,8,−4], result [6,−9,11;−1,−2,−5]. Its two equality stages put the explicit input difference on the LHS, then the unevaluated-difference matrix, then the result. It does not repeat an extra initial equality.

q-319618 uses the named2×3 pair [−4,12,−1;6,−7,3]−[−9,5,2;−8,−1,10]. The six table blanks are the complete difference [5,7,−3;14,−6,−7]. q-319622 uses named3×2 pair [7,7;−6,2;5,−8]−[10,−5;−6,−9;3,−1], six table blanks [−3,12;0,11;2,−7]. q-319625 uses named3×3 pair [−6,4,9;7,−2,5;10,0,−3]−[1,−8,6;−4,3,−7;12,−5,9], six blank cells0,1,4,5,6,8, and supplied cells2=3,3=11,7=5. Its complete result is [−7,12,3;11,−5,12;−2,5,−12]. All three have observed easy labels, six correct references, and the three-stage solution sequence. Blank fragments are bare integers, not matrix answers.

## 2. Shared pattern and purpose

Subtract corresponding entries of two matrices with matching fixed dimensions; retain their positions in the output. Signed subtraction is prerequisite arithmetic. The answer is either a full matrix selected from five matrices, or six scalar entry fragments at table cells, with remaining output cells already supplied. Keep the original names, prompt layout, table padding, six-field keys, source prose and operative stage sequence. The specific six target positions of the partial3×3 can vary: they have the same six scalar-response roles, never a different count or different mathematical relation.

## 3. Component and complete-bank maps

Let a,b be row-major operands and c=a−b. Use zero-based indices. Historical five-member banks are parameterized expression patterns, preserving exact values without inferring the original psychological mistake:

- q-108: c except cell0=a0+b0; c; c except cell2=a2+b2; c except cell1=−(a1+b1); c except cell3=a3+b3. The addition interpretations are defensible, while the negated sum's historical intent remains uncertain.
- q-11478: [a0−a3,a0−a3,c2,c3]; [c2,c3,c1,c0]; c; [c2,c3,c0,c1]; [c0,c1,−c2,−c3]. Permutations/sign flips are visible operations, but repeating a0−a3 is only an exact replay expression pattern; the evidence does not identify its intent.
- q-11441: c except cell3=−c3; [a0,a0,a0,a0]; c except cell1=c0; [c3,c3,c3,c3]; c. The repeated a0/c3 patterns are opaque. They are not promoted as recovered source distractor methods.
- q-69603: [a0+b0,a1+b1,a2+b2,c3,a4+b4,a5+b5]; [c3,c4,c5,c0,c1,c2]; c; [c0,−(a1+b1),c2,c3,a4+b4,b5]; [c0,c2,c1,c3,c5,c4]. Whole-row/within-row swaps are clear expression patterns; the mixed bank's intent remains unresolved.

Every historical member's original value is independently checked in `source-choice-mapping.json`; complete-bank equivalence and correct-reference fidelity are separate. The four historical banks are `observed:<MA-id>` profiles, all explicitly evidence-only and ineligible for learning. Blank observed profiles similarly preserve raw attribute/spacing details; normal blank profiles use the same computed fragments and completed normalized presentation.

Normal radio profile **authored-method** comprises exactly: c; a+b (add instead of subtract every corresponding pair); b−a (reverse subtraction globally); c except cell0=a0+b0 (add at that cell); c except cell1=b1−a1 (reverse that cell). These are independently authored operations on the actual displayed matrices. First choose this complete profile, then parameters; any equivalence between any two of the five matrices rejects the whole instance. No wrong option is replaced by a fallback pool. No learner-facing diagnosis or feedback is added. Profile aliases method-derived/entry do not generate different identities.

Source blanks each own one bare-integer answer and their existing key. Full2×3/3×2 masks request all six entries. Partial3×3 maps field-j to the jth selected ordered target, updates every supplied entry, and preserves six fields.

## 4. Reusable backbone and slots

Fixed: subtraction operator; matching operand dimensions for each mask; source matrix names and prose; one radio field/five complete matrices or six blank scalar fields; table padding; shared “We subtract the corresponding entries” sentence; ordered solution operations. q-69603 retains two equalities. q-108 has no observed solution, so normal completion is independently authored using q-69603's supplied-explicit-difference structure. q-11478 has no observed solution; normal completion uses the canonical/source named-matrix three-stage structure. No missing source stage is counted as recovered.

Variable complete components: every operand integer entry−12…12 (easy0…9); the two full matrix slots in the prompt; each entry's unevaluated subtraction node with a parenthesized negative subtrahend; all result entries; all complete answer matrices. For partial3×3 only, the six ordered distinct target cells, dependent field assignment and supplied cell values vary together. Source-only spacing commands at cells1 and3 are preserved on observed replay; normal presentation omits that incidental padding. Field keys remain field-1…field-6.

Conditional: negative subtrahends are displayed as a−(−b), never a--b. Attribute presence is driven by the original record in observed replay: missing rating, missing solution, missing correct reference remain missing. Normal records supply an authored grade and computed complete solution/key. All normal values pass the shared math_content normalizer before identities are computed.

Constraints: exact integer types (not booleans), rectangular flattened shape, fixed parameter keys, signed workload guards from classification, ordered six-cell target set, and unique complete banks. Exact explicit inputs are either accepted unchanged or rejected. Domain/family selection and sample metadata stay outside learner content. Mathematical fingerprint excludes names, bank, aliases, seed, grade and unqueried operand pairs/supplied cells, but includes actual requested cells and their operand pairs; presentation identity includes actual prompt, solution, grade/presence and complete bank, ignores order/seed, and owns field/answer UUIDs. Changing a bank or displayed prompt changes the ID. Defaults cover all seven masks within each of the three authored bands; 120 distinct assessed tasks per band and exact enumerated capacity slices are checked without counting aliases.

No source math error was found among practice banks or available solutions. The two missing-key/rating/solution sources are evidence limitations, not mathematical errors. The incomplete canonical prompt is retained as context only. Raw exact replay, original designation match, inferred-key fixture grading, authored correctness and native grading have separate denominators in validation.json. No database writes or registration.
