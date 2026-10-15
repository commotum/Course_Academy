# Four-stage template extraction

## 1. Specific source descriptions

`source-components.json` maps every original matrix shape/support, witness, field, full answer value, correct designation (where present), and radio subset mask. Exact complete records are in `source-cases.json`; descriptions do not replace raw evidence. MA practice labels and display order are retained at replay.

q-11553 displays H3x2 zero, G3x5 zero, K3x3 with three diagonal ones. Its complete subsets are HGK, HK, H, HG, K (order is not semantic); HG is the uniquely correct subset. q-7827 displays A2x5 zero, B2x2 with b22=1, C1x2 with c11=10. Its complete subsets are C, B, AC, ABC, A; A is uniquely correct. The original862 JSON and screenshots confirm these are radio widgets; the absent key/solution remains a capture omission, not recovered evidence.

q-126201 displays H3x2 zero, I3x2 with two0.1 entries on row2, G1x1 zero. The solution's i12 witness is wrong, independently detected against the displayed matrix; choose i21. q-126204 displays R3x3, S2x2, T2x3, all zero; its conclusion lacks "only" and names all three. q-68729 displays T2x2 with t12=1, U3x3 with u32=1, V4x4 zero; each negative bullet says "one of its entries is not zero". q-68725 displays P3x2 with three ones, Q2x4 zero, R4x3 zero; witness p21. q-68727 displays W4x4 with four ones, X3x4 zero, Y3x6 with y16=1,y21=1,y33=3; witnesses w22 and y33. Its first "not" is unitalicized; preserved by the profile mask.

## 2. General pattern and instructional purpose

Read each explicitly named numerical matrix. Classify it as zero iff every entry is0. A single nonzero entry suffices to refute the property. Record the complete subset via the original five-choice radio bank or three Boolean checkbox fields. Explain each matrix separately, then collect the zero labels. No matrix calculation, simplification, or classification of a different special matrix is assessed.

## 3. Component and bank mapping

The complete checkbox bank is exactly text false and text true for EACH named field; true is correct iff the entire displayed matrix has zero support. These are Boolean response values, not arbitrary numerical distractors. Each answer is owned by its field with a unique UUID. Source fields can appear in a different Pull collection order; field keys identify their matrices. Per-field bank matching ignores choice order only.

Every radio option is a complete subset, parameterized by source label-position indices, not disconnected text fragments. The q-11553 masks are [0,1,2],[0,2],[0],[0,1],[2]. The q-7827 masks are [2],[1],[0,2],[0,1,2],[0]. The whole bank remains fixed to its profile; no correct-only lookup, answer resampling, or bank mixing. Mathematically equal subsets collide regardless of wording/order and are rejected. The five observed masks are distinct at every valid label substitution. These banks are defensible selection patterns from the assessed predicate; no claim to recovered distractor psychology is made.

`templates.json` contains extraction masks and operative bullet prose only, never completed source payloads or a seed-to-answer table. `source-cases.json` records the seven MA source records and explicit replay parameters. `independent-inventory.json` contains the entire non-MA record and its concrete relationship to q-126201; it is not a source-case. `canonical.json` separately holds raw canonical and screenshot-restored parameters.

## 4. Reusable backbone and variable slots

Fixed: three named matrices; source field contract; source source-shaped zero/nonzero count per role; all five radio subsets or both Boolean values; one bullet per displayed matrix and a concluding list. The five original checkbox solution styles remain exact at their source anchor, except the documented incorrect witness. Changing parameters retains the same operative sentence masks. Missing legacy solutions borrow the same entrywise proof backbone and are labeled authored.

Variable slots: three distinct uppercase labels; each rectangular shape1–4 rows and1–6 columns; zero/nonzero supports within that rectangle retaining each role's exact nonzero count; each nonzero number independently from observed {1,0.1,3,10}; a witness chosen from the actual nonzero support. Total displayed entries<=46 (observed easy maximum). All these guards apply to explicit calls and samplers equally, for every level. Positive nonzero magnitudes are incidental to zero recognition and do not inflate task counts. No expressions, signed algebra, or entries requiring evaluation are introduced.

Shape and support positions are substantive reading tasks. Any feasible cell is an eligible nonzero witness: no source position is pedagogically fixed. Tests exercise all24 row/column cells in a4x6 rectangle for each nonzero role and all3 levels (720 explicit instances across30 groups). The supplied object and proof method remain unchanged when the witness moves.

Sampling chooses the complete source family/bank first, samples all matrices together, and retries the WHOLE instance when shape/count/entry-budget constraints fail. It never patches a colliding option from a pool. All7 profiles occur in normal sampling at all3 levels. A batch rejects mathematical duplicates across levels and all captured current inventory tasks plus the restored canonical. The mathematical fingerprint sorts unlabeled shape/support objects, ignoring label aliases, matrix order, nonzero magnitudes, witness choice, bank profile, seed, option order and difficulty. Presentation UUID additionally includes actual level, normalized prompt, fixed worked solution and complete keyed banks. Presentation metadata/profile aliases and option shuffling cannot create new content IDs.

Formatting: shared matrix_tex/normalize_prose and checked_math_content at the public boundary, before IDs. Text answer values use intended prose rendering, with math label spans only in radio subsets. No answer feedback exists in the sources or output. Source replay uses ordinary numerical parameters through the same public generate API; no literal-source branch exists.

Validation reads the actual printed matrices, every printed witness coordinate/value and classification, all subset answer values and the final conclusion. Complete original worked solutions are compared, with an exact replacement check for the single witness repair. Negative mutations keep the final correct lookup references unchanged but alter witness values/coordinates, remove a witness, change the conclusion, remove a bullet, or inject a C0 control. Each must fail independent validation. Native grading uses current verified application code, no database operations; all displayed answer IDs (correct and wrong) pass/reject as intended. Discrete fields have no numeric-equivalent-entry parser requirement or hidden scalar-entry exception.
