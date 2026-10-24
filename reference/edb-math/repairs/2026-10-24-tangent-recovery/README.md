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
