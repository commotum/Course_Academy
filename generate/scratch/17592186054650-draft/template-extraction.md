# Four-stage extraction

## 1. Describe each original before generalizing

All source operands are signed integers with magnitude ≤16 and exactly six entries. q-103 asks “What is” a direct 3×2 sum; q-105 names X/Y inline; q-125722 names P/Q in a display and parenthesizes negative first addends in the expanded stage; q-319601 supplies P/Q inline, then six scalar blanks in a two-row Markdown table; q-69622 and q-69635 display the unnamed sum directly, respectively 2×3 and 3×2; q-106 names M/N in a display. Original parameters are recorded completely in `source-cases.json`, and the immutable wrapper retains all original strings/IDs. q-103/q-105 have no recorded rating, solution or correct ref. Their missing values are independently derivable but are never reported as matched designations.

q-125722/q-319601/q-106 solutions name the sum, substitute both whole matrices, write all six component additions without evaluation, then show the evaluated matrix. q-69622/q-69635 begin with both operand matrices on the left and omit the redundant named-substitution row. The q-69635 opening contains its original trailing space; raw and normal solutions retain it. Each family preserves its own complete prose and operative sequence at changed parameters.

## 2. Shared pattern and instructional purpose

Add two matrices of equal, non-square dimensions by adding corresponding entries. Return the entire matrix: one five-option radio choice or six integer fragments at the positions specified by the original table. The requested operator is always addition. Distractor subtraction is a wrong sign operation on the same displayed entries, not a new assessed skill. No scalar multiplication, inverse operation, products, dimension-recognition question, extra unknowns or extra response target is introduced.

## 3. Complete component and bank mapping

`source-choice-mapping.json` maps every one of the **36** original displayed values to its field and captured answer UUID, including all **24** radio distractors. `source-cases.json` records complete operands and the public profile. The script's `historical_bank` function is the full parameter recipe, with the following index convention: a,b are row-major operand entries 0…5, c=a+b; unlisted entries stay c. Profile ordering below is source bank ordering, subsequently shuffled only for display.

| Profile | Five complete option recipes (or blank fragments) |
|---|---|
| q-103 | c with {2:a₂−b₂,5:−c₅}; c; c with {3:−a₃+b₃,5:−c₅}; c with {0:−c₀,4:−a₄+b₄}; c with {1:−c₁,2:−c₂} |
| q-105 | c with {0:−c₀,4:c₄+12}; c; c with {4:c₄+12,5:−c₅}; c with {1:−c₁,4:c₄+12}; c with {3:−c₃,4:c₄+12} |
| q-125722 | c; c with {0:b₀,1:a₁}; c with {2:a₄,5:c₂}; c with {4:b₄−a₄,5:b₅−a₅}; c with {2:a₃} |
| q-69622 | c+(-2,-1,-3,-4,-1,-10); c+(0,8,-6,1,0,-15); c+(0,0,-3,-11,0,-10); c+(4,0,-4,8,0,-11); c |
| q-69635 | c with {3:c₃+6,4:−c₄,5:−c₅}; c with {0:a₀−b₀,2:−c₂,5:a₅−b₅}; c; c with {2:c₂−10,3:c₃+5,4:−c₄,5:−c₅}; c with {2:−c₂,3:c₃+28,5:−c₅} |
| q-106 | c with {3:−c₃}; c; c with {1:−c₁}; c with {5:−a₄+b₄}; c with {1:−c₁,4:−c₄} |
| q-319601 | field-1…field-6 return c₀…c₅ (captured field collection order is retained, positions are determined by keys) |

These formulas reproduce entire original banks exactly, but sparse evidence does **not** establish cognitive intent. In particular q-105, q-69622 and q-69635 contain arbitrary historical residuals (+12, +6, −10, +5, +28, vectors). They are honest parameterized historical evidence profiles, not polynomial fits masquerading as plausible mistakes. Even the more interpretable historical profiles remain evidence-only. All changed-profile review records use the public generator and explicit evidence flags.

Normal authored defaults use separately named complete method banks, selected before any operand sample:

- `method-omission`: A+B, A, B, A−B, B−A. The two omissions keep one displayed operand; the other errors reverse one addend's sign.
- `method-sign`: A+B, −(A+B), A−B, B−A, |A|+|B| entrywise. Errors reverse both signs, reverse one sign, or drop operand signs.

These are complete five-option recipes; every pair of complete matrices must be distinct, with exactly one correct option. A collision rejects the whole instance. No first-valid distractor pool or numerical perturbation is used. For blanks the bank profile is incidental; both aliases yield the identical displayed content and IDs. No feedback is invented.

## 4. Backbone, slots, domains and boundaries

Fixed: two matrices, six requested entries, source orientation per family, prompt masks, field count/type/layout, three or two equality stages, shared prose, correct correspondence. Variable: all twelve integer operands (each influences the assessed sum), eligible source-shaped family, complete authored bank. Operand labels are source fixed; there is no claim of semantic variety from letter aliases or shuffled options. Negative second addends receive parentheses; q-125722 also groups negative first addends. Complete matrix slots prevent unrelated prose substitutions.

Historical replay has integer magnitude ≤16, source profile and explicit operands. `source:<id>` preserves omitted attributes; `source-completed:<id>` provides authored missing attributes for independent native grading while remaining ineligible evidence. Replays do not mutate captures or add a missing source designation to the fidelity denominator.

Authored workload bounds (applied to sampling **and** explicit inputs):

| Level | Six additions and number-form demand | Evidence limits |
|---|---|---|
| easy | magnitude ≤9; at most two opposite-sign pairs; zero accepted at explicit boundaries if the complete bank remains unique | Conservative authored subset of observed easy; observed easy originals can exceed these bounds through evidence replay |
| moderate | exactly three negative-negative pairs and three opposite-sign pairs; every operand nonzero, magnitude ≤16 | Three decisions about sign/magnitude plus three two-negative additions, all within source observed number forms; no MA moderate examples |
| hard | all six pairs opposite-sign; both operand magnitudes 10…16; every sum nonzero, with positive and negative outcomes | Six two-digit sign/magnitude comparisons; arithmetic ceiling remains observed 16; no MA hard examples |

These domains are conservative design claims with uncertain relative calibration. They do not form a progression within a level; each level samples equivalent workload. The observed easy labels are not overwritten. The canonical/sibling route supports integer entrywise addition and sign arithmetic, not fractions or additional matrix operations, so those are excluded.

Capacity is much larger than a small QA sample. A constructive fixed-operand subfamily gives at least 9⁶−1=531,440 easy tasks per orientation (A entries alternating ±9, B same-sign magnitudes 1…9, excluding B=A); 16³·15³=13,824,000 moderate tasks (three A=-16/B∈[-16,-1], three A=16/B∈[-15,-1]); and 6⁶=46,656 hard tasks (A alternating ±16, B opposite-sign magnitudes 10…15). Both authored method banks are distinct throughout these subfamilies except the excluded easy B=A case. Commutative operand swaps do not double capacity: fingerprints canonically sort whole operands; banks, difficulty and aliases are excluded from mathematical-task counts. Displayed prompt, solution, complete bank, attribute presence and actual difficulty determine content identity.

Independent validation reads actual displayed operand matrices and every displayed stage/choice. It verifies unevaluated component-sum **structure**, not merely equality with the final result; exact source prose/stage masks; complete bank recipes; key/position ownership; absence parity; boundaries; defaults covering every family/profile; seed/order-independent IDs; bank-dependent content IDs; and memory-only native grading. Mutation regressions replace the expanded row by the equal final row, introduce a control character, duplicate a displayed choice, change the prompt's operator, and add an omitted raw rating. Every mutation must fail.
