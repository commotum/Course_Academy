# Gaussian elimination extraction

Source snapshot: math, basis 2480, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. All ten practice records and the canonical example were read together. The two unrated records lack keys and solutions and are excluded without editing them.

The supplied object is a nonsingular 2-by-3 augmented matrix with nonzero first pivot. The requested object is either its normalized row echelon form or that form together with the ordered solution x,y. Both use a five-option selection radio field. The two response contracts remain separate. First normalize row 1 when necessary, eliminate its first entry from row 2, then normalize row 2 when necessary. The solve templates additionally display the resulting equations, substitute y into row 1, collect the constant contribution, and conclude x,y. These stages and their order are fixed because they teach the standard algorithm, rather than arbitrary equivalent echelon forms.

| Source | Level | Response | Input rows | Stages | Bank |
|---|---|---|---|---|---|
| q-10329 | moderate | REF | (2,3,7); (3,-2,4) | normalize, eliminate, normalize | five matrices, fractional first row |
| q-1059 | easy | REF and solution | (1,1,8); (-1,-2,3) | eliminate, normalize, substitute | five matrix/point objects, newline layout |
| q-1060 | moderate | REF | (-1,2,1); (5,6,8) | normalize, eliminate, normalize | common first row, five fractional last entries |
| q-130910 | easy | REF and solution | (1,7,-2); (2,10,0) | eliminate, normalize, substitute | five matrix/point objects, inline layout |
| q-20459 | moderate | REF and solution | (3,-6,10); (2,-3,5) | normalize, eliminate, substitute | five matrix/point objects |
| q-20461 | moderate | REF and solution | (2,-6,-9); (1,-2,-4) | normalize, eliminate, substitute | five matrix/point objects |
| q-10512 | moderate | REF | (3,-2,4); (6,4,-8) | normalize, eliminate, normalize | five matrices, three distinct first-row profiles |
| q-130909 | easy | REF | (2,-8,6); (3,-7,4) | normalize, eliminate, normalize | integer REF, five matrices |

The one variable slot is a positive RHS factor k. Both augmented entries, every intermediate augmented entry, and every solution coordinate scale by k. Coefficient entries, row targets, operation multipliers, matrix dimensions, response shape, choice count, field key, and complete bank membership stay fixed. This is a conservative same-method extension: source k=1, bounded generated k=1..5, restricted to factors coprime with every observed fraction denominator in that profile. This preserves signed branches and fractional arithmetic. It changes the represented system and its solution, whereas multiplying all three entries of a row would leave the same system. The identity and novelty fingerprint exclude seed and option order, and normalize whole rows and row permutations.

Each source bank is a separate profile selected before assembly. `choice-recipes.json` accounts for every source choice by its fixed coefficient entries, two augmented-column expressions `original_constant*k`, and, where present, point-coordinate expressions `original_coordinate*k`. These expressions reproduce the complete original objects at k=1. Some source distractors have no clear psychological interpretation; they retain the observed mathematical pattern instead of receiving an invented error label. No profiles are mixed. The full bank is rejected if values collide or the keyed object fails the independently derived standard REF and point contract.

The source prompt and all operative solution prose are replayed exactly at k=1. Variants parameterize the matrix entries, inline equation values, displayed system, substituted y, RHS, collected contribution, and final x. Negative signs and fractions render from exact rationals. Source answer TeX commands are double escaped; generated answers correct those escapes without changing source records. Source replay retains exact original bytes, and mathematical object comparison separately verifies the correction for variants.

No new plots are required. Array typesetting and the canonical SVG assets contain standalone mathematical notation, not graphs or diagrams. They do not require a plot generator. The canonical example is not part of available practice.

Source exception: q-10512 contains both the keyed REF and its RREF as choices. Both satisfy row echelon form and have identical row spaces. The source bank replays exactly for evidence, but neither that source nor its variants contribute to this package's validated inventory. The original record remains untouched. `source-errors.json` retains both values. Seven complete source profiles remain supported.
