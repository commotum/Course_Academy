# Classification

Captured database math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. Source wrapper is preserved unchanged in source.json.

11 practices: 9 explicitly easy (5 radio with five choices, 4 blank with one answer); 2 unrated five-choice radios lack correct refs and worked solutions. There are no moderate/hard practice labels. All 11 remain in source-cases.json. None require plots.

| Source | Recorded level | Field | Full bank | Vectors | Solution layout |
|---|---|---|---|---|---|
| q-40214 | unrated | radio | observed_q-40214 | [['3', '5', '0'], ['3', '2', '0'], ['3', '4', '5']] | (('full', 'full', 'full'), False, (), False) |
| q-42052 | unrated | radio | observed_q-42052 | [['-3', '0', '-2'], ['1', '5', '-3'], ['2', '-1', '4']] | (('full', 'full', 'full'), False, (), False) |
| q-128421 | easy | radio | observed_q-128421 | [['2', '2', '3'], ['4', '2', '-1'], ['-5', '0', '3']] | (('full', 'full', 'full'), True, (), False) |
| q-128433 | easy | radio | observed_q-128433 | [['0', '-1', '4'], ['3', '9', '2'], ['2', '7', '6']] | (('zero', 'omit', 'full'), True, (0,), False) |
| q-18259 | easy | radio | observed_q-18259 | [['-3', '3', '1'], ['2', '-1', '3'], ['0', '4', '1']] | (('full', 'full', 'omit'), True, (), False) |
| q-280670 | easy | blank | none | [['1', '2', '3'], ['0', '1', '-1'], ['2', '0', '1']] | (('full', 'full', 'full'), False, (), False) |
| q-280671 | easy | blank | none | [['1', '1', '2'], ['-3', '2', '0'], ['4', '-2', '1']] | (('full', 'full', 'full'), False, (), False) |
| q-280712 | easy | blank | none | [['1', '2', '3'], ['0', '5', '0'], ['4', '0', '6']] | (('full', 'full', 'full'), False, (), True) |
| q-280716 | easy | blank | none | [['3', '1', '4'], ['0', '2', '5'], ['6', '0', '1']] | (('full', 'omit', 'full'), False, (), False) |
| q-40221 | easy | radio | observed_q-40221 | [['-5', '3', '0'], ['2', '-1', '4'], ['1', '1', '1']] | (('full', 'full', 'zero'), True, (2,), False) |
| q-42050 | easy | radio | observed_q-42050 | [['1', '-2', '1'], ['2', '-4', '1'], ['0', '2', '5']] | (('omit', 'full', 'omit'), True, (), False) |

The templates preserve source prompt phrasing (Calculate/Compute, V/implicit volume, and exact tuple spacing), field shape, complete solution prose and five-row expansion structure. Five observed Markdown/value families are distinguished: radio_missing_solution (2), radio_calculate_products (5), blank_calculate_products (2), blank_compute_evaluated_minors (1), and blank_compute_products (1). Eleven named source-layout selectors preserve source-specific whitespace, unit-factor omissions and factor ordering within these five families. These selectors are provenance/layout variants, not eleven distinct skills or eleven recovered mathematical templates. Seven complete observed banks are opaque catalogs. Four blank layouts have no distractor profile. Normal authored templates are one radio and one blank per level, sharing the same worked method.

Lesson route, read through activity/first-step and step/next: Introduction → this KP → Volume Spanned by Coplanar Vectors → Determining Whether Three Vectors are Coplanar → coordinate-vertex volume tutorial → position-vector-coordinate volume KP → proof. This generator stops at the first supplied-vector KP. Its key prerequisites are Absolute Value Expressions and The Scalar Triple Product. Its canonical example e-4350 evaluates a signed integer determinant then takes absolute value. It never solves for a coplanarity parameter, builds displacement vectors from points, computes a tetrahedron, or tests a proof.

Authored missing levels: moderate uses all nine nonzero integer coordinates of magnitude ≤5 and requires three nonzero cofactor terms, so six signed minor products and three weighted terms contribute. Hard applies exactly the same formula to nonzero reduced integers/halves/thirds of magnitude ≤5, requiring at least three reduced fractions and three nonzero cofactor terms. This adds bounded exact rational arithmetic already inherent in the prerequisite scalar triple product, without a new branch or skill. These are design assignments rather than recovered ratings. Each difficulty is an unordered collection of questions at one workload. Explicit inputs are guarded by the same reduced-coordinate requirements.

Normal easy preserves source integer workload (magnitude ≤9, one to three zero coordinates). Unlike source replay, authored default banks use four specified cofactor-method operations. Entire five-choice bank is selected together, then rejected if any scalar is duplicated or zero; positive volumes are used throughout. The valid mathematical task catalog is large: moderate alone has 10^9 nonzero integer-coordinate candidates before exclusions, hard has additional reduced rational candidates. Variety validation counts actual distinct vector tasks, not profiles, seeds, labels, or option order.
