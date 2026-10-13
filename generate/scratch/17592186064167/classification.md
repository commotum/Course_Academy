# Classification — math basis 1356

Provenance: database `math`, basis `1356`, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. `source.json` copies the complete capture wrapper unchanged. All six practice records are included; canonical e-364 is context, not a seventh practice question.

| Source | Original level | Template | Captured field | Bank | Solution |
|---|---|---|---|---|---|
| q-2005 | absent/unrated | legacy_x | radio selection, five choices, no correct ref | observed_2005 | absent |
| q-2022 | absent/unrated | legacy_power | radio selection, five choices, no correct ref | observed_2022 | absent |
| q-113665 | easy | integral_spaced | absent | none | present, full power rule + derivative check |
| q-113670 | easy | function | absent | none | present, integrate both sides + power rule + check |
| q-66126 | easy | constant | absent | none | present, 1=x^0 + power rule + check |
| q-71121 | easy | integral_thin | absent | none | present, full power rule + derivative check |

The two direct integral source solutions are identical except parameters; their separate presentation profiles retain full source strings. Four easy records have missing fields, not observed blanks. Normal radio/blank fields are explicitly authored completion. The two unrated records receive an authored easy assignment in source-cases, while raw replay leaves their difficulty absent. Raw replay retains absence of solutions/correct references as well.

Plot requirement: **none**, across all templates, banks and levels. No image reference occurs in these captures or owning widgets. Captured original MA lesson widget `.../MA/DATA/Lessons/308/Source/308.json` confirms two five-choice radios and their entire banks, but does not supply missing correct designations or solutions.

Moderate and hard have zero observed examples. Ordered lesson route follows first-step 65001 → 65154 (power-rule tutorial) → 65002 (this KP) → 65003 (radical KP) → 65004 (reciprocal KP) → 65005 (recap); IDs are abbreviated by their shared prefix 175921860. This KP's prerequisite is Power Rule for Differentiation. Constant Multiple Rule for Indefinite Integrals follows this topic. Scope therefore remains coefficient-one x^n with integer n>=0: no coefficients, sums, radicals, reciprocals, logarithms, conditions, or different variables as supposed skill diversity.

## Supported capability policy (revised after current inventory check)

Easy remains supported over the explicitly bounded integer exponents 0..20,
which include every observed value. There are 21 mathematical tasks before source
and canonical exclusions; layout, bank profile, field type and option order do not
multiply that capacity. Production replenishment uses radio fields at n>=1.
The n=0 constant preview is a blank and has only one meaningful task.

Moderate and hard are unsupported under this package and rejected by the public
API. The former n=21..40 / n=41..60 author-assigned bands lacked a defensible
change in mathematical workload: every case merely increments one exponent and
divides by its successor. No observed source supports those bands; this is a
bounded capability decision, not a claim that their absence alone proves them
impossible. Coefficients, sums, radicals and reciprocals belong to other KPs.
New source evidence reopens classification. Their nominal shortages remain five
each, explicitly unfilled. Easy finite depletion likewise remains explicit.

The native blank grader rejects rescaled arbitrary C, even though the primitive
families agree. Production radio selection avoids that response limitation;
blank previews are diagnostic and are not submitted by this replenisher.
