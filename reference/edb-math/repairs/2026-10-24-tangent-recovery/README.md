# Tangent generator recovery

KP 17592186059664: Finding an Exact Value Using the Sum and Difference Formulas for Tangent.
Original blocked pipeline: `cea5ef8806843ed0b2bb5238a66a67bd04433f91f5a991d967ed98734da9438d.pipeline/2`.

This folder is an isolated candidate and investigation. It is not a publication or an independent approval.

## What failed

The first generator used all four exact result values plus an unrelated fifth distractor. Sign and magnitude alone selected one explicit choice in 2/5 delivered questions and 98/128 catalog cases. The first repair required a wrong choice in the correct interval, which removed that issue but left the correct answer as the sole expression of the form ±2±sqrt(3) in 3/5 delivered questions. That second defect was real: the learner could ignore the prompt entirely.

The next reviewer requested that exact-family recognition followed by sign/magnitude also leave at least two choices. That extra requirement is impossible for this source-supported finite family. The four values ±2±sqrt(3) lie in four distinct sign/magnitude intervals. Once the learner knows the complete exact-answer family, the target's interval determines the exact value independently of the bank. Both original source banks have the same property. Adding a second distinct exact-family value in the correct interval would require a second correct answer or a change of assessed skill. The author's impossibility argument was sound for this combined test, but it did not fix the separable, prompt-blind unique-shape defect.

## Candidate correction

The candidate chooses an unordered pair of possible exact answers and constructs the five-choice bank symmetrically around that pair. It gives each member its own fraction-free wrong interval competitor, then adds one further error value. Both possible answers are canonical-form expressions. Every generated bank can serve a different target with a different correct answer without changing any choices.

The correct special-angle domain, sum/difference formulas, quadratic-surd rationalization, simplified answer form, five-choice radio response, authored moderate band, and complete original replay banks remain unchanged. No seed selection or fixed batch overrides are used.

## Verification and limits

`verify.py` uses independent exact SymPy calculations from displayed prompts and options, checks every displayed solution transition, reproduces both earlier defects, covers all 128 catalog cases, tests 250 additional five-question seeds, and creates a different-target/same-bank control for every catalog bank. The native grader and actual publication filter are used separately. The generated candidate's source and delivery evidence are the captured basis 6389; final publication must recheck current source and inventory.

The family-knowledge-plus-bounds strategy remains possible and is documented in `evidence/finite-family-proof.json`. This is not a claim that every shortcut or every possible future batch has been eliminated. A final-answer multiple-choice question cannot distinguish formula execution from correct recall of the finite exact-value identities. The fix prevents the demonstrated bank-only unique-shape cue and unique interval candidate; it does not invent a different mathematical task to defeat learned knowledge.

## Frozen candidate and completed checks

The runtime package hash is `e7b15035bab20db925c7ca95b4898285773fae170428ca83c375a3bf94a3bd8e`. Only `package/generator.py` changes relative to the blocked package: the symmetric distractor-bank construction and generation version. Source replay banks, formatting helper, and manifest are unchanged. The independent reviewer must accept this exact candidate before it replaces the live workspace.

- `evidence/verification.json`: exact mathematics for all 128 bounded cases, 128 different-target/same-bank controls, 1,250 further generated records, complete replay of both original five-choice banks, and retained negative examples.
- `evidence/grader-verification.json`: actual `course_academy_engine::learning::grade_field`, 141 correct choices accepted, 564 distractors rejected, zero unresolved checks or database writes.
- `evidence/delivery-{requested,fresh,catalog}/delivery.json`: actual publication filter retains 5/5, 8/8, and 128/128 records.
- `evidence/delivery-regression.json`: the protected properties survive filtering; requested CLI replay is byte-identical.
- `evidence/render/rendering.json`: five requested records pass the unmodified UI renderer. All five screenshots were also visually inspected; math, answer banks, and worked steps are readable.
- `evidence/portable-regression/regression.json`: the standalone workspace regression passes against current CLI output and delivery survivors, with all mathematical comparisons performed exactly in the quadratic field using only Python's standard library.

## Retained finding map and deployment files

`workspace-regressions/repair-regressions.json` maps both historical IDs to `check_tangent_regressions.py`. The script and the adjacent `tangent-regression-fixtures/` directory are portable: copy all three into the workspace after independent review accepts the corrected criterion. Running the script without arguments then resolves `generator.py` beside itself and `../source/{source,inventory}.json`. It does not modify runtime files or contact a database. Override `--package`, `--source`, `--inventory`, and `--output` for isolated runs.

| Finding | Preserved failing evidence | Current acceptance criterion |
| --- | --- | --- |
| `0c0b5701fdc1e1f51385` | Review 1 has 2/5 unique interval answers and additional sole fraction-free interval answers. | Every current record has at least two interval candidates and at least two fraction-free interval candidates, before and after shared delivery filtering. |
| `5177439f65fd0aa4269e` | Review 2 has 3/5 prompt-blind unique-family-shape answers. | Every current record has at least two literal fraction-free canonical-family forms (including reversed term order), as well as two algebraic family members, before and after filtering. |

The second review's added requirement that *family recognition intersected with bounds* also remain ambiguous is explicitly classified as impossible within the source-supported finite family. The regression reports its success on all current questions, instead of claiming the strategy disappeared. It recomputes the four disjoint intervals and tests both retained original source banks. This is a mathematical correction to the criterion, not a deleted counterexample. `evidence/portable-regression/negative-controls.json` also verifies that both historical batches fail the repaired-defect guard.

Independent review caught a distinction in the regression: algebraic membership alone cannot test a visible formatting cue. The retained script now counts literal two-term forms separately and includes a synthetic negative control with a second family member displayed as a fraction. That bank passes the algebraic and interval checks but fails the literal-shape guard, preserving the original defect's precise meaning.

The recurring workflow failure was treating a compound reviewer request as one indivisible requirement. The author proved one component impossible and stopped even though another component was still a concrete, repairable defect. Future repairs should preserve and test each separable counterexample, identify any impossible component with a source-backed witness, and request independent review of the revised criterion rather than allow contradiction to stall the whole generator.
