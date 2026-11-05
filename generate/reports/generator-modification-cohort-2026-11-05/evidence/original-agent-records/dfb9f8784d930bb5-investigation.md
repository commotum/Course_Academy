# Using the Double-Angle Formula to Simplify Products

KP **17592186059671**, UUID `143766e0-0ef5-5caf-b699-d394d4a707e9`. This account uses only the supplied math snapshots at basis **7194**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. The target KP, complete question banks, canonical example, lesson, prerequisites, image manifest, reference questions, `generate/principles.md`, and `generate/docs/3-classify.md` were read. No database queries, publication, or imported-content changes were performed.

## Learner operation and retained evidence

Recognize a same-angle product, match it to $2\sin x\cos x=\sin(2x)$, double the whole angle, and retain the correct external multiplier. Canonical example `e95210c5-adb4-519e-bbec-e240dac32fd8` directly replaces $2\sin15^\circ\cos15^\circ$ with $\sin30^\circ$. The lesson derives the identity by putting equal angles into the sine sum formula. The captured prerequisite topic supplies sine sum/difference formulas in degrees and radians, with canonical examples `4cd24c10-1838-5f4b-ac88-cfbfc2ec4c21`, `7341638b-3c0f-5c10-8b7d-a2c313607bed`, and `0ce71d86-7470-5d53-ac94-20b473889dee`.

Complete easy practice is one product-replacement backbone, with angle/function and coefficient-confusion choice-bank profiles:

- `188c3216-6730-58aa-bfa7-8985bab845cd` and `64c46307-6499-587a-8e3d-194000e8c499`: coefficient two, direct replacement, radians/degrees.
- `feecaade-207a-51bf-96ee-61bce1de2e85`, `ff03781e-e811-57da-88cb-583d049585d0`, and `71319f17-956d-5226-b02f-5e0082742e93`: retain an external multiplier after replacement.

Complete moderate question `984868e6-9b0d-5753-97a4-a56b885226b2` first compresses a numerator product, then recognizes a sine/cosine quotient as tangent. Partial moderate question `807c1c95-6fea-5d65-a59b-b497c894ecc9` supplies a different backbone: expand a squared binomial, combine squared terms using the Pythagorean identity, then compress its cross term. Its worked solution is usable teaching evidence despite absent controls.

Partial questions `29b3c524-7b23-5771-a9d9-d475ba18867c` and `af0778bb-fb31-5795-b709-311385ef20eb` retain five-choice radio banks for scaled/direct products. Partial easy question `099149c9-1e5d-5a49-aba3-6528a838f44d` supplies the coefficient-six derivation. All four partial imports remain exactly as stored. Their absent components are ordinary incomplete evidence.

Retained components are the same-angle product, degree/radian notation, five-choice radio response with key `selection`, multiplier tracking, explicit identity substitution, and algebra-to-identity solution steps. No target or reference question supplies a diagram; the target image manifest is empty. All classified families have plot requirement **none**. Existing observed coverage remains **easy and moderate**, with **5/1/0** complete easy/moderate/hard questions. The new examples do not change that observation.

## Reference progression and adaptation

Reference KP **17592186059673** also uses five-choice radio controls throughout. Its easy questions `dde407ba-34c3-55d5-a98c-cb0e2c5bb577` and `95efa6da-7216-501c-8391-1e0cbd18db0c` expand a doubled sine then cancel, with a cotangent rewrite in the latter. Moderate questions `b2050e06-0476-56c1-a7a1-1d0ef234a4b2` and `1a84df43-c63e-5997-bb62-0b42cedd5faa` require choosing the useful expansion inside a quotient or reciprocal product and recognizing secant/cosecant. Hard questions `df53af64-a7fb-5920-a9ae-4765f5d7236c` and `20492e7a-2ad5-5346-9935-34abf42dcea6` coordinate the double-angle identity, tangent/cotangent rewrite, Pythagorean identity, factorization, and cancellation.

The reference prompts offer expressions and alternatives without a pre-answer derivation. Its detailed identity reminders and cancellation demonstrations occur **after answering**. Difficulty rises through structural decisions and combined algebra; neither a new response type nor larger angles establish the progression. Imported labels overlap in workload and are not an exact universal step-count scale.

`exemplars.json` contains exactly three complete new questions:

| Level | Required work before selecting | Result |
| --- | --- | --- |
| Easy | Recognize the visible product and double $23^\circ$. | $\sin46^\circ$ |
| Moderate | Expand $(\sin(\pi/7)-\cos(\pi/7))^2$, preserve the negative cross term, combine squared terms, then compress the product. | $1-\sin(2\pi/7)$ |
| Hard | Discover the common product in $\sin^3(\pi/11)\cos(\pi/11)+\sin(\pi/11)\cos^3(\pi/11)$, factor it, recognize the resulting Pythagorean sum, then account for the missing factor two. | $\tfrac12\sin(2\pi/11)$ |

The moderate example retains the partial target's binomial scaffolding and solution sequence, with a minus sign to test cross-term control. Its wording specifies the requested doubled-angle form but supplies no expansion. The hard example is a pedagogical extension: the useful product is hidden until a common factor exposes a Pythagorean sum. That increases planning demand while keeping the target operation central. It does not import the reference's ratio-cancellation task or the neighboring KP's repeated double-angle/exact-value task. Each example applies the double-angle formula once. Factoring is familiar algebra; the target's moderate evidence already establishes the Pythagorean identity as relevant support. The hard label is this phase's instructional judgment, not an imported label or a claim of learner calibration.

All derivations, identity reminders, and factorization instructions appear in worked solutions after answering. The actual response demand remains one five-choice selection. Distractors target coefficient loss, incorrect angle doubling, sine/cosine confusion, cross-term sign loss, and dropping the cross term. Non-special angles avoid turning the examples into special-angle evaluation. Future variants should vary signs, angles, and eligible coefficients while deriving every dependent value; they should not infer a fixed answer position or coefficient from these three examples.

## Checks and result

- `verify_exemplars.py` independently proved all three generic identities with SymPy, evaluated the instantiated expressions and all fifteen choices to 50 digits, and found exactly one mathematical answer per bank. It also checked schema, math normalization, all 21 distinct UUIDs, supported difficulties, ownership of correct references, and absence of new Math Academy IDs. See `evidence/independent-solutions.json`.
- The actual native `learning::grade_field` accepted all **3** correct choice IDs and rejected all **12** wrong choice IDs; **0** unresolved. Inputs and report are `evidence/engine-input.json` and `evidence/native-grading.json`.
- The publisher's offline filtering/validation accepted one example per level against the supplied inventory, with **0** duplicates and **0** database writes. Reports are `evidence/delivery-{easy,moderate,hard}/delivery.json`. These checks do not publish or simulate learner selection.
- `generate/pipeline/render_preview.py` rendered the actual UI. All three final reports passed, with no raw TeX, math errors, broken images, JavaScript errors, or internal field labels. All final screenshots were opened and inspected, including every radio choice and the full solutions. There are no dropdowns to open or diagrams to verify.
- The initial moderate expansion exceeded the solution width even though the DOM report passed. `evidence/render-initial/question-002.png` preserves that observation. The solution now defines $x=\pi/7$, expands using compact notation, and substitutes back. Final screenshots in `evidence/render/` show the complete equations without clipping. Math/schema, grading, filtering, and rendering were rerun on the revised file.

No shared renderer, script, or engine repair was needed. Final evidence hashes and visual findings are saved in `evidence/completion.json` and `evidence/visual-inspection.md`. The three examples, complete solutions, and verified response contracts are ready for the next phase; no generator or database publication is claimed.
