# Quality audit of the three reported lessons

The lessons still contain problems. This read-only audit inspected **9 registered generators and 287 stored questions** across the normal-line, position-vector and Gaussian-elimination lessons: **151 imported and 136 authored questions**. Seven generators were untouched by the preceding repair; the two repaired generators received sanity checks using their completed repair evidence and current captured content.

All reads use **math EDB basis 14220**. A [closing readback at basis 14225](closing-verification.json) confirms that all nine registrations and their complete question pools remained unchanged. No questions, packages, dependencies, learner records or service settings were modified during this audit.

## Repair targets

| Priority | Finding | Exact affected question or generator |
| --- | --- | --- |
| High | An imported unanswered prompt prints both correct scalar answers, followed by empty input widgets. Native practice eligibility accepts it. | Question **17592186292807**, `q-275128`; KP **17592186096652**. The exposed answers are −1/2 and −5/2. |
| High | Every radio question in the complete current intercept subgroup can be answered by choosing the largest varying coordinate, without calculating a normal or intercept. Root independently reproduced the choices-only rule on all eight records. | KP **17592186092385**: **17592186092507, 17592186092510, 17592186233120, 17592186240795, 17592186240796, 17592186493316, 17592186578858, 17592186710717**. Six imported, two authored; all eight eligible. |
| Medium | A stored authored question draws and supplies the vector decomposition route before answering. | Question **17592186735008**, KP **17592186096652**. |
| Medium | A stored authored ratio question supplies both `OX = OA + AX` and `AB = b − a`, removing two source-required decisions. | Question **17592186734994**, KP **17592186096653**. |
| Medium | Two current vector generators can put labels closer to the other reference arrow or crowd them into a narrow wedge. Coordinates and keys remain correct; mobile association becomes ambiguous. | KPs **17592186096652** and **17592186096701**. Exact seeds, indices and delivered screenshots are in the [vector report](vector/audit.md). Stored question **17592186735423** is a confirmed example of the latter defect. |
| Low | An imported evaluated-derivative equality still contains a free `x` before substitution. Its final key is correct. | Question **17592186317210**, `q-342153`; KP **17592186092384**. |

The first four rows require stored-question cleanup. The two label defects also require changes to current generator renderers. The current two-factor and ratio generators do not reproduce the old supplied-path hints; the current intercept generator uses blanks rather than the vulnerable radio banks. Fixing future generation alone therefore would leave the bad stored practice available.

The maximum-coordinate finding concerns the **entire captured eight-question radio subgroup**, not a statistical claim about future generation. No sign, answer-rank or family-balance quota is proposed.

## Findings by lesson

| Lesson | Generator assessment | Stored content |
| --- | --- | --- |
| Normal lines: 3 KPs, 94 questions | No additional confirmed mathematical or scaffolding defect in ordinary sampled slope/intercept output; repaired equation generator remains consistent. | Eight vulnerable radio banks, one minor solution-notation defect, six screened incomplete imports. Five context-dependent multistep parts are already excluded and are not counted as defects. |
| Position vectors: 4 KPs, 139 questions | Two confirmed labeling defects. Ratio generator and repaired reversal generator had no additional confirmed defect within the checked scope. | Two supplied-path questions, one answer-contaminated import, one confirmed stored label example, two screened incomplete imports. |
| Gaussian elimination: 2 KPs, 54 questions | No confirmed defect in checked code, mathematical constructions, banks, solutions or UI. | No confirmed additional defect. Echelon-only questions are explicitly supported by imported question families; back substitution is required only for the solve-system family. |

Eight incomplete imported records are rejected by the native practice validator: normal-equation **17592186234077**; normal-slope **17592186092723, 17592186092725, 17592186234307**; intercepts **17592186233928, 17592186234308**; vector ratios **17592186097046, 17592186097240**. These are import-completeness issues, distinguished from eligible bad practice.

## Evidence and limits

- [Package/runtime audit](package-runtime-audit.json): all nine immutable packages are intact and compatible with the configured runtime.
- **534 fresh ordinary samples** received independent mathematical checks across all three bands: 240 normal-line, 216 Gaussian, 78 vector. Native grading covered **411 actual delivery survivors** plus stored controls. Normal-line second-seed samples were mathematical checks; they are not counted as extra delivery/native checks.
- **276 actual player presentations** cover 69 selected records in unanswered/completed states at desktop and narrow widths. Generated UI inputs bind to actual delivered survivor objects. DOM/MathJax success does not negate the visually confirmed label defects.
- Root independently reproduced the [eight-bank shortcut](root-bank-cue-check.json) and viewed the actual unanswered screenshots for the printed answers, both supplied-path questions, a vulnerable bank, and the label counterexamples. The paired reports retain record and image byte identities.
- [Normal-line audit](normal/audit.md), [vector audit](vector/audit.md), [Gaussian audit](gaussian/audit.md) contain exact IDs, source comparisons, current package paths, deterministic reproductions, grading reports and screenshots. Their machine-readable reports retain coverage and limitations. The initial vector enum-fixture failure is explicitly discarded, not treated as practice-ineligibility evidence.

This is a bounded quality audit, not a guarantee about every future output. Imported grid-vector keys were checked against their complete worked-solution endpoints and all prompt diagrams were visually screened; every raster geometry was not independently reconstructed. Fresh sampled geometry was independently solved. Normal-line ordinary family coverage is narrower than some imported power cases, and authored difficulty bands lack empirical calibration. Long completed mathematics uses accessible horizontal scrolling where required.
