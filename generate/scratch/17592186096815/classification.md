# Classification

Provenance: math database basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` preserves the complete capture wrapper. There are two practice questions; neither has a rating, worked solution, or correct reference. Neither original designation can count as matched.

| Source | Observed prompt/value template | Widget | Complete bank | Rating | Plot |
|---|---|---|---|---|---|
| q-12184 | cardinal_sum: right/down, magnitudes3/4 | one radio, key selection, five math choices | observed_cardinal | absent | none |
| q-12185 | compass_sum: NE/SE, magnitudes20/13 | one radio, key selection, five math choices | observed_compass | absent | none |

These are two wording templates for one orthogonal-sum method, not two mathematical branches. Original lesson JSON and full section rasters were inspected: both show the complete five-choice multiple-choice widget and the same calculator instruction. `widget-evidence.json` records authoritative layout evidence. The stored radio fields agree with those widgets; only the designation is absent. All options are positive multiples of a+b. Unit and parallel permits either sign; testing every option's squared norm yields exactly one valid answer in each bank. No direction clarification or negative-choice exclusion is needed.

The activity chain is Introduction → given vector → given vector in a diagram → vector sum, from first-step/next traversal. Parallel Vectors (1103) is the topic prerequisite. The owning next topic is component form (1165), so no component-form question is authored here. The canonical example uses magnitudes10/20, triangle addition, Pythagorean magnitude, and reciprocal normalization. Its single image was inspected: rightward a, downward b, red diagonal a+b, right-angle marker. It supports the geometric method but is not a practice plot requirement. No plots are generated or reused in practice.

All three authored difficulty policies are design claims, not recovered source labels. Easy: unequal integer cardinal magnitudes2..30 with integer hypotenuse. Moderate: unequal cardinal integer magnitudes2..12 with nonsquare squared norm. Hard: unequal diagonal compass integer magnitudes10..25 with nonsquare squared norm, requiring recognition that the bearings differ by90degrees, without angle arithmetic/trigonometry. All use the identical square–add–root–normalize sequence. Within each level the magnitude pairs and eligible perpendicular orientations are unordered alternatives; there is no progression. Source q-12184 is associated with authored easy and q-12185 with authored hard for source-case organization only; evidence replay accepts magnitudes1..50 without claiming an observed level.

There are13,51,115 meaningful unordered magnitude pairs respectively. Rotations, swaps, profile changes, and option order do not inflate task counts. The upper easy bound30 admits more familiar Pythagorean pairs while keeping integer-root arithmetic; this is an explicit extension rather than cosmetic copies of3/4. Changing scale changes the scalar normalization requested in terms of the given vectors. Direction rotation is retained in presentation identity only.
