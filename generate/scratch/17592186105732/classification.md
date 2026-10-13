# Classification

Snapshot: math, basis 1356, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. Canonical e-4344 is method evidence, not one of the 11 practice questions.

Observed: 6 easy (3 radio, 3 blank), 4 moderate (2 radio, 2 blank), 1 unrated radio. Easy sources ask parallelogram area; moderate sources ask triangle area, adding the half-area step. No practice plots. All vectors are given in 3D, integers, with mixed signs/zeros. Source coordinate magnitudes reach 6. Answer fields are one math-valued radio field `selection` with five choices or one scalar blank `field-1`; vector and determinant matrices are worked-solution structures, not answer-vector fields.

| Source | Observed level | Template | Bank | Field |
|---|---|---|---|---|
| q-19983 | moderate | triangle_radio_radical | q-19983 | radio |
| q-20003 | unrated | parallelogram_radio_unrated | q-20003 | radio |
| q-18580 | moderate | triangle_radio_radical | q-18580 | radio |
| q-19981 | easy | parallelogram_radio_radical | q-19981 | radio |
| q-19997 | easy | parallelogram_radio_simplified | q-19997 | radio |
| q-20004 | easy | parallelogram_radio_simplified | q-20004 | radio |
| q-275220 | easy | parallelogram_blank_direct | none | blank |
| q-275222 | moderate | triangle_blank_direct | none | blank |
| q-316345 | easy | parallelogram_blank_expanded | none | blank |
| q-316350 | easy | parallelogram_blank_expanded | none | blank |
| q-316355 | moderate | triangle_blank_expanded | none | blank |

Eight observed template/layout families including one source missing its solution; hard adds two authored field layouts. The source direct/simplified/expanded/radical sequences remain distinct; numerical examples sharing a sequence and response shape share a template. The unrated spaced prompt is retained separately for presentation fidelity.

## Curriculum scope and authored hard

Owning topic 1299 / db 17592186049108 is Finding Areas Using the Cross Product. The lesson is traversed from activity first-step 17592186106616 through step/next: introduction → 17592186106617 (this KP) → 17592186106618 (triangle given vertices) → 17592186106619 (altitude). This order comes from first-step/next, not Pull array order. Canonical e-4344 supplies given vectors (4,0,-3), (5,-1,2), determinant cross product, norm sqrt(554), triangle half sqrt(554)/2. Prerequisites explicitly include Calculating the Cross Product Using Determinants (245) and Calculating the Magnitude of Cartesian Vectors in 3D (1277).

Hard is a design claim, not a recovered source label. It still asks triangle area from two given integer vectors. Both are primitive (gcd 1), all six coordinates are nonzero, at least four have absolute magnitude at least 2, and the pair includes a negative coordinate. This requires all six substantive determinant products; primitive-input checks prevent inflated integer presentations from pretending to increase workload. Every cross component is nonzero and at least one has magnitude at least 8; the norm radicand must actually simplify. Coordinates satisfy |n|≤6 and norm squared≤20000. These bounds keep the existing signed determinant/magnitude prerequisites while increasing arithmetic density. No vertex subtraction, altitude, angle-based branch, symbolic parameter, or new cross-product method is introduced. Radio and blank are unordered equivalent assessments of this same skill. Moderate does not promise sparse vectors; its source q-19983 already has six nonzero coordinates, so dense-hard workload is an authored policy rather than a disjoint observed taxonomy.

## Source anomaly

q-20003 has a complete five-choice bank and radio layout but no difficulty, correct reference, or worked solution. The owning authoritative lesson Source/1299.json confirms the same prompt and five-choice widget without an available designation/solution. Independently, (-2,-3,-1)×(1,2,1)=(-1,1,-1), so parallelogram area is sqrt(3), uniquely present. The missing normal key and shared-style solution are authored mathematical repairs; easy is assigned because the prompt matches observed easy parallelogram tasks. No original designation or solution fidelity is credited for this source. No original math errors/ambiguous banks were found. Raw captured source.json remains immutable.
