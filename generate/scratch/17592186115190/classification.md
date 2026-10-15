# Cosecant derivatives at math basis 2275

The immutable source wrapper is copied byte for byte as `source.json` (math,
lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`). Before importing code, the
numeric script and evidence directory were absent. `baseline.json` records the
manifest entry: queued, latest inventory `has_generator=false`. There was no
existing numeric tree to preserve. The wrapper contains eight MA-identified
practice questions and no independently authored records; the exact standard
inventory wrapper therefore has an empty `questions` list.

| Family | Captured level | Fields/bank | Plot requirement |
|---|---|---|---|
| q1889: csc + scaled tan − cos | unrated | radio, 5, no correct ref or solution | none |
| q31283: quadratic − scaled csc | easy | radio, 5 | none |
| q104316: exp(x)csc(x) | moderate | answer fields absent | none |
| q313722: scaled linear times csc | moderate | blank, 1 | none |
| q105299: constant-base exponential times csc | moderate | radio, 5 | none |
| q340582: ln(x)csc(x) | moderate | blank, 1 | none |
| q105298: ln(x) − scaled csc, derivative at pi/2 | hard | radio, 5 | none |
| q313723: csc − scaled cubic + cos, derivative at pi/4 | hard | blank, 1 | none |

There are eight prompt/solution families, four captured full radio profiles,
three captured blanks, and one fieldless family. Easy/moderate/hard are all
observed; no missing difficulty level was invented. q1889's easy label is an
explicit authored assignment, supported by the sum-rule treatment of q31283,
the introductory lesson, and the constant-multiple canonical example e3644.
It adds no chain rule, quotient, or derivative order. Its extra terms each
require a memorized first derivative.

The lesson route was reconstructed from activity/first-step and step/next:
Introduction (116045), Mnemonic Tricks (116214), Cosecant KP (116046), Cotangent
KP (116047), Secant KP (116048), Slope KP (116049), Justifying Reciprocal
Derivatives (116050), all IDs with prefix 17592186. Collection order was not
used. The introduction explicitly permits combinations of reciprocal trig
functions; mnemonic content states csc'=-csc*cot. Key prerequisites are Product
Rule, Quotient Rule, and Reciprocal Trig Ratios. The topic next boundary includes
Chain Rule With Trigonometric Functions, so inner arguments remain exactly x.
Sibling slope questions use quotient rules and tangent slopes; this generator
keeps the existing hard differentiate-then-evaluate scalar response and adds no
line-finding or quotient family.

All c slots are integers 1..24 (observed examples include 2,4,5,6); base b is an
integer 2..12. The larger coefficient range changes only a single exact
multiplication, retaining the same number of terms, powers and derivative
stages. Hard authored evaluation varies familiar unit-circle angles pi/6,
pi/4, pi/3, 2pi/3, 3pi/4, 5pi/6, already supported by reciprocal trig ratios.
Each level has a fixed workload across its variants: two/three term sums at
easy, one product rule at moderate, derivative then substitution at hard.

Raw anomalous records are public parameterized `profile="evidence"` outputs:
all retain attribute-presence parity and are `evidence_only=true`,
`eligible_for_learning=false`. q1889 retains its full five choices but no
correct ref, rating or solution. q104316 retains its moderate rating and
solution but omits answer fields. q313723 retains a source formal-operand sign
typo. Normal output completes q1889 and q104316 and minimally corrects that
sign; these are separately documented below and never counted as recovered
missing source fields.
