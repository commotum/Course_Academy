# Template extraction

## 1. Describe each original specifically

The complete raw capture is source.json, and review.md displays every original prompt, full bank and full captured solution. The following is the complete parameter/structure inventory. Coefficients remain signed integer components; all observed roots are nonzero integers.

| Source | Original coefficients c | Root | Determinant stages / equation stages | Source bank values |
|---|---|---:|---|---|

| q-11651 | [2, 3, 5] | 9 | 3 / 4 (authored solution) | ["k = 9", "k =-4", "k =-9", "k = 4", "k = 0"] |

| q-19801 | [1, 2, -3] | 3 | 4 / 6 (authored solution) | ["-3", "1", "3", "-1", "2"] |

| q-127614 | [2, 6, 2, -2] | 4 | 3 / 6 | [] |

| q-11653 | [2, 4, 3] | 1 | 3 / 5 | ["-4", "-1", "0", "1", "4"] |

| q-127604 | [3, -5, 2, -1, 2] | -1 | 3 / 5 | ["k=7", "k=-1", "k=-\\frac{3}{2}", "k=-7", "k=-\\frac{1}{4}"] |

| q-127606 | [1, 2, 2, 8] | -2 | 3 / 5 | ["v=4", "v=-2", "v=\\frac{3}{4}", "v=-3", "v=\\frac{7}{3}"] |

| q-127607 | [1, -3, 1, 3] | 3 | 3 / 5 | ["2", "-\\frac{5}{2}", "3", "\\frac{3}{4}", "9"] |

| q-127608 | [1, 5, 1, 3] | 1 | 3 / 6 | ["p=1", "p=\\frac{2}{5}", "p=\\frac{1}{3}", "p=3", "p=-5"] |

| q-127609 | [3, 1, 3, -5] | 3 | 3 / 6 | ["y=3", "y=18", "y=-9", "y=\\frac{9}{2}", "y=\\frac{18}{2}"] |

| q-275598 | [1, 4, 6] | 5 | 3 / 5 | ["5"] |

| q-275601 | [3, 4, 5] | 4 | 5 / 4 | ["4"] |

| q-317377 | [2, 3, 5] | 7 | 3 / 4 | ["7"] |

| q-317382 | [1, 1, 2, -1, -5, 4] | 20 | 4 / 4 | ["20"] |

| q-317385 | [3, 2, -4] | 4 | 4 / 6 | ["4"] |

| q-69661 | [1, -1, 1, 1, -3, 2] | -3 | 4 / 4 | ["2", "-6", "-2", "-3", "3"] |

## 2. Generalize the shared assessed pattern

Substitute the four displayed matrix entries into ad−bc, simplify the determinant, equate it to the specified scalar and solve for the unique requested unknown. Easy determinants are linear, including two affine entries whose products must be distributed. Moderate determinants become repeated-root quadratics; moving to zero, extracting a constant GCF or reversing a sign when needed, and recognizing the perfect-square trinomial give one root. Hard distributes two binomials and subtracts a quadratic entry, visibly cancels opposite quadratic terms, and then solves a linear equation. Hard does not add arbitrary quadratic branches or general two-root solving.

## 3. List and map every original component

observed-choice-mapping.json accounts for all **50 original displayed values**, the exact original answer objects, field UUIDs/keys, correct refs where present, profile and parameterized value pattern. It explicitly leaves original scalar distractor intent unknown. Nine complete profiles each contain the whole five-choice bank, never an arbitrary selection from an error pool. Five blanks expect only the scalar because their variable/equality prefix is supplied in the prompt. The fieldless source has zero observed answer values.

Radio profile values are expressed as the observed scalar-to-solved-root ratio times the solved root, retaining the original equation-prefix spacing and original unreduced fraction mask. This is a restricted numerical replay pattern, not a recovered error operation or a claim about original authoring intent. It is parameterized and exercised with changed inputs, but it is not chosen by default. Normal radio generation uses separately authored whole-operation profiles. No invented diagnosis is placed in learner text.

Normal easy radio bank: correct (N−C)/L; wrong transposition (N+C)/L; reversed numerator (C−N)/L; omitted constant N/L; omitted final division N−C, where det=Lz+C and target=N. The complete profile is rejected when any results coincide. Normal moderate bank: root r; sign reversal −r; unhalved linear coefficient 2r; constant term r²; halving again r/2. These follow the normalized perfect-square equation z²−2rz+r²=0. The whole bank is rejected on equivalence, so roots ±1 and 2 can be ineligible for this authored bank while remaining valid for original-bank replay or blanks.

The q-127609 raw bank is 3,18,−9,9/2,18/2. In particular 18/2=+9 differs from −9; all five are distinct. No collision repair is needed. Raw answer string inspection finds single backslashes in fraction commands; JSON escaping is not a source TeX anomaly.

Prompt slots replace the complete matrix body and complete determinant scalar. Worked-solution masks replace complete mathematical sides, preserving original prose, whitespace, determinant labels, punctuation, variable notation and ordered stages. The formal ad−bc formula block is retained. Optional GCF-normalization rows follow the leading coefficient rather than being inserted redundantly.

## 4. Extract reusable masks, constraints and calculations

The family entry masks and coefficient roles are:

| Family | c components | Entries in row order |
|---|---|---|
| diagonal | a,b,c | a,b,c,z |
| offdiagonal | a,c,d | a,z,c,d |
| bottom_linear | a,b,c,u,v | a,b,cz,uz+v |
| top_linear | a,u,b,v,c,d | a+uz,b+vz,c,d |
| symmetric | h,b,c | h+z,bz,c,h−z |
| quad_bottom | a,b,c,d | az,b,cz,z+d |
| quad_top | a,b,c,d | az,bz,c,z+d |
| quad_right | a,d,b,c | z+d,bz,c,az |
| quad_negative | a,d,b,c | d−z,bz,c,az |
| cancellation | a,b,d | a+z,bz−z²,1,d−z |

The supplied root determines N by evaluating the displayed determinant at that root. Moderate parameters must satisfy det−N=Q(z−r)² with Q≠0 and nonzero linear coefficient. Easy/hard parameters require Q=0 and a nonzero remaining slope. All source and authored parameters are validated, not silently corrected or resampled. Real domain and unique-root restrictions apply to all questions.

Difficulty workload bounds apply to explicit inputs and samples: easy signed nonzero coefficients have magnitude ≤10 and |r|≤24; moderate/hard coefficients have magnitude ≤8, with |r|≤6 / ≤12 respectively. Targets have magnitude ≤200. The hard binomial constants differ so its distribution terms remain substantive; the quadratic entry and both cancelling squares are always present. Sample bounds are authored policies, not recovered source code.

Symmetric sampling uses h in 1…6, b in 1…4, c in {−6,−4,−2,2,4,6} and r=−bc/2. Other moderate families sample a,b in 1…3, c in 1…6 and nonzero integer r in −5…5, deriving the necessary affine constant and rejecting noninteger/out-of-bound values. Easy/hard signed coefficients sample −8…8 excluding zero, with nonzero integer r in −10…10; complete-bank rejection occurs after parameter selection.

Every difficulty is observed. Authored extensions are larger same-method parameter domains, complete normal radio operation profiles, two supported missing difficulty labels/solutions and the explicitly authored fieldless blank. There is no invented missing-level mathematical family or progression.

Identity: mathematical task fingerprint canonicalizes actual matrix entries using z plus target, excluding layout, bank and variable aliases. Matrix entries are substantive because determinant substitution/distribution is assessed. Presentation identity hashes version, actual prompt, fixed full solution, field kind and complete displayed bank sorted without option order; seed/shuffle alone cannot change it. Different valid displayed banks change presentation identity.
