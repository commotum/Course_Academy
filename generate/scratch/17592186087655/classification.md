# Classification — math basis 1356

KP 17592186087655 / 82d6988b-3220-578f-ba1c-cd86b9e3dbf9, **Finding the Equation of a Circle Given the Center and the Radius**. Immutable capture source, topic, lesson wrappers retain database math, basis 1356, lineage 01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1. `source.json`, `topics.json`, `lessons.json` are byte-preserved capture copies.

Eight practice questions: six explicitly easy, two unrated. Seven radio layouts and one blank. One graph-radio mathematical/Markdown family has seven complete bank profiles; the blank is a separate layout and solution sequence with an absent input diagram. Axis-radio differs in zero-coordinate conditional components and bank, rather than a new assessed method. The raw stripped blank has its own `missing_input_blank` template; repaired normal blank uses `graph_blank`. Rating **moderate plots**: every usable source assesses a labeled diagram, with one red circle, center tuple and marked radius, though no coordinate grid reading. No answer or solution plots.

| Source | Observed difficulty | Field | Center; radius | Bank |
|---|---|---|---|---|
| q-54187 | absent | radio selection, 5 | (1,3); 3 | q-54187 |
| q-54210 | absent | radio selection, 5 | (-2,5); 7 | q-54210 |
| q-167932 | easy | blank field-1, full equation | (3,0); 3, from solution | blank |
| q-116929 | easy | radio selection, 5 | (-4,-3); 6 | q-116929 |
| q-117077 | easy | radio selection, 5 | (2,-3); 4 | q-117077 |
| q-117081 | easy | radio selection, 5 | (-5,0); 7 | q-117081 |
| q-70896 | easy | radio selection, 5 | (1,2); 5 | q-70896 |
| q-70898 | easy | radio selection, 5 | (-2,-3); 8 | q-70898 |

Canonical e-3224 uses labeled (-1,1), radius 3, and the same general/substitution/simplification sequence. It is contextual evidence, not one of the eight practice questions. The raw full banks, answer type, values, IDs, correct refs and attribute presence are retained in `source.json`; `source-components.json` maps every choice to an operation tuple.

## Source anomalies

q-54187/q-54210 omit difficulty, correct reference and worked solution. Inspected original rasters unambiguously supply center and radius. Authoritative lesson widget capture (`original-widget-evidence.json`, originally MA lesson 843 JSON) confirms each five-choice radio layout and source values. Raw public replay **omits** all three absent attributes and is explicitly evidence only. `completed:q-ID` supplies an authored easy assignment, correct equation and common worked solution; the correct value is inferred directly by independently squaring the displayed radius. Missing correct designations are reported absent, never matched.

q-167932's source prompt says “this circle” but contains no diagram or center/radius. The authoritative local 843 capture does not contain this later question; no original diagram is recovered. Raw replay preserves exact stripped whitespace/prompt and is evidence only. Its answer and solution imply center (3,0), radius 3. Completed/default blank presentation restores a **new parameterized diagram**; this is an explicit source presentation repair, not an original asset recovery. No mathematical answer repair is required.

## Curriculum and level boundaries

Lesson route is reconstructed by `activity/first-step` then `step/next`: introduction 17592186088461 → this KP 17592186088462 → center/radius extraction 17592186088463 → center+point 17592186088636 → diameter-endpoints 17592186088464. The introduction derives `(x-a)^2+(y-b)^2=r^2` from the distance definition. Key prerequisite is topic 842, Equations of Circles Centered at the Origin. Sibling KPs own reverse extraction, midpoint, distance-to-given-point and completing-square work; none is introduced here.

Moderate and hard are **authored absent-level designs** anchored in that same substitution/squaring formula and existing exact arithmetic, not recovered labels. Every normal instance asks for the complete standard equation; no expansion is required.

- Easy default: two nonzero integer shifts with magnitude 1..8; integer radius 2..9. Both shift substitutions and one integer square. Observed profiles retain integer coordinates <=10, radius 2..10, including source zero-coordinate axis cases (q-117081/q-167932 require k=0). Easy source zero cases preserve their observed difficulty rather than pretending every historical example had identical arithmetic.
- Moderate: two nonzero integer shifts of magnitude 1..6; reduced noninteger rational radius n/d with d∈{2,3,4}, n<=19, 1<r<5. Every instance retains both shifts and squares both numerator and denominator; integer radius cases are rejected.
- Hard: both coordinates reduced noninteger rationals with denominators 2..4, magnitude 1..6 and opposite signs, and the same noninteger rational radius bounds. Every instance preserves two fractional shifts including a subtraction of a negative fraction, and squares numerator/denominator. Integer-coordinate or same-sign cases are rejected. Extra number-form bookkeeping creates a disjoint workload from moderate, without adding geometry or an equation-extraction response.

All bounds are applied to reduced exact values for both sampler and explicit API calls. Random sampling and explicit parameters use the same guards. Source profiles restrict integer parameters; an explicitly supplied radical radius is rejected. q-116929's observed sqrt(r) wrong equation still requires an algebraic complete coefficient field, exercised at r=2. Profiles select a complete five-option operation bank before sampling, and collision/ambiguity rejection discards the entire instance.

`capabilities.json` enumerates mathematical task domains, excluding bank/layout/orientation aliases. Default common banks admit every task in those domains. Numerical change affects the assessed center or squared radius rather than only incidental labels. These are substantial repeat-practice families, not static source lookup banks.

## Native support boundary

The native `learning::grade_field` symbolic parser accepts expressions, but fails on a complete equation's equals sign with `unconsumed mathematical notation`. The original q-167932 full-equation math blank, expanded equivalent entries, nonzero scalar equation multiples and wrong equations all exhibit that same exact unsupported syntax. Its field type/complete-equation response is preserved, never changed into a fragment. Explicit graph-blank/source-blank draft output has `evidence_only=true`, `eligible_for_learning=false` and `grading_compatibility.supported=false` plus the exact reason. Native unresolved counts are separate from bank fidelity and mathematical correctness. Validator permits only this documented exact error for those ineligible blanks; all unexpected errors fail.

Every normal/default learning call generates the existing observed **radio** field type at every level, retaining complete equations and method-derived banks. All eligible radios must pass native correct/wrong ID checks. Raw missing-correct radios are evidence only and declare their missing canonical ref in compatibility metadata. `validation.json` reports eligible-native validation success, full blank support incomplete and the exact unsupported findings separately.
