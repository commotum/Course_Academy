# Investigation: Using the Double-Angle Formula to Simplify Expressions

KP **17592186087669**, math lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, captured basis **7316**. Only the supplied snapshots were used; no database queries or publication were performed. Read the complete target practice bank, lesson, canonical example, prerequisites, image manifest, all six reference questions, `generate/principles.md`, `generate/docs/3-classify.md`, and the validation-tool documentation.

## Learner operation and retained instruction

Recognize the same angle in $\cos^2 x-\sin^2 x$, replace the difference by $\cos(2x)$, and simplify the doubled angle. With a common coefficient, factor it out and retain it outside cosine. This is expression rewriting, not finding an exact numerical trig value. The lesson derives the identity from the cosine sum formula; its prerequisite topic is **The Sum and Difference Formulas for Cosine**. Alternative double-angle forms and exact-value evaluation occur in later, separate KPs and are not assessed here.

Canonical example `7826cd52-8603-51ff-902e-c7764639dccd` supplies the identity–substitution–angle-simplification explanation. Easy sources include degree example `d5d50fd1-bc8e-514c-8dca-56cd8a6999fe` and radian example `d38b6d10-21f4-5ec6-94ba-9141257529fc`. Moderate sources `6bb4ecb6-0b76-51e4-aa33-5be6f12e1dbb`, `cf1faff6-afe0-59ea-a58f-f8289c637840`, and `a4d26858-a337-5218-af76-0e3d4aac3fca` add factoring, with integer, radical, and fractional coefficients. Coefficient size/type is variation within that method, not a hard tier.

All twelve target imports have one five-choice math radio field keyed `selection`. Retained: the “single trigonometric ratio” task, degree/radian notation, five complete alternatives, common-factor scaffolding in solutions, identity recall, substitution, and final ratio. Plot requirement is **none**: the captured image list is empty and these questions contain no diagrams. Source easy banks vary between angle-only alternatives and function/coefficient errors; moderate banks mix lost/doubled coefficients with unchanged/incorrect angles. The complete ID-to-bank ledger is `../investigation/source-analysis.json`.

The prompts supply expressions and alternatives, without an identity hint or intermediate fields. Identity recall and factoring are learner work **before choosing**. Detailed worked solutions appear afterward; their length is not itself evidence of difficulty. Each new prompt preserves this separation.

## Reference progression and adaptation

Reference KP **17592186059673**, “Using the Double-Angle Formula to Simplify Ratios,” uses five-choice radio fields at every level:

- Easy `dde407ba-34c3-55d5-a98c-cb0e2c5bb577` expands sine then cancels a visible factor; `95efa6da-7216-501c-8391-1e0cbd18db0c` also rewrites cotangent.
- Moderate `b2050e06-0476-56c1-a7a1-1d0ef234a4b2` requires choosing the denominator for expansion, cancelling, and recognizing a reciprocal. `1a84df43-c63e-5997-bb62-0b42cedd5faa` first exposes a reciprocal hidden in cosecant notation. Radians alone do not explain the level change; the second example also permits a special-angle shortcut.
- Hard `df53af64-a7fb-5920-a9ae-4765f5d7236c` and `20492e7a-2ad5-5346-9935-34abf42dcea6` require a longer chain: double-angle expansion, quotient rewriting, cancellation, Pythagorean substitution, difference-of-squares factoring, and another cancellation.

The transferable design is increasing the structural work needed to expose and use an identity, with unchanged response controls and explanatory support after answering. The target examples do not import the reference's sine-ratio mathematics.

| Level | New question ID | Required work and answer |
| --- | --- | --- |
| Easy | `1985f423-dac4-4d96-8378-c5f534458e6e` | Directly rewrite $\cos^2 23^\circ-\sin^2 23^\circ=\cos 46^\circ$. |
| Moderate | `939e9116-37c9-4ab5-a00e-ece7e775b4b8` | Factor $2$ before applying the identity at $\pi/14$, obtaining $2\cos(\pi/7)$. |
| Hard | `483748f2-ba12-48fb-9e7b-d1d8b5b8b134` | Factor $2(\cos^4 19^\circ-\sin^4 19^\circ)$ as a difference of squares, reduce the sum-of-squares factor to $1$, then apply the target identity, obtaining $2\cos38^\circ$. |

Hard is an authored extension, not an observed imported level. It uses the Pythagorean identity already treated as known in the supplied lesson, solely to expose the target difference. It uses neither the later alternative cosine formulas nor a numerical exact-value task. The same coefficient $2$ appears in moderate and hard: the added demand is factorization and identity composition, not larger numbers. Distractors test function, angle, coefficient, and fourth-power/difference-of-squares mistakes.

For the next phase, retain these three backbones. Degrees/radians and simple nonzero coefficients may vary without changing level. Keep fourth powers fixed in the hard backbone; higher powers need a separate scope justification. Recompute complete banks, reject mathematically equivalent alternatives, and vary choice order. Three exemplars establish usable constructions, not a tested randomized generator or broad variation coverage.

## Source limits and checks

Observed coverage remains **easy, moderate**, with **6 easy, 5 moderate, 0 hard** complete imports. Partial import `46b65a20-2a00-5f23-9147-67e515b42d14` lacks a difficulty, key, and worked solution; it remains exactly as stored. No import was repaired. Exactly three complete new records appear in `exemplars.json`, with fresh UUIDs, explicit levels, full fields and lookup references, and no Math Academy IDs or authorship tags.

Two source banks contain equivalent alternatives: `eda88667-03a3-54d2-bc45-5bd8cd910c52` offers both $\cos(3\pi/2)$ and $\cos(5\pi/2)$; `ccbcdf42-d0d6-5ef1-b1a3-dd2467d078f8` offers both $\cos(6\pi/5)$ and $\cos(4\pi/5)$. Both pairs have equal values. Preserved the imports but did not reproduce those ambiguities.

Independent symbolic checks reduce all three general identities to zero; separate direct evaluations verify every displayed choice, with exactly one mathematical answer per bank (`independent-math.json`). Actual native `learning::grade_field` checks all **15 choices: 3 accepted, 12 rejected, 0 unresolved** (`native-grading.json`). Per-level offline publisher checks each accept one record with zero duplicates at basis 7316 (`delivery-*/delivery.json`).

Rendered all three final records through `generate/pipeline/render_preview.py` and inspected full-page screenshots and reports. Initial moderate/hard solution equations overflowed despite passing automated reports; explicit equation line breaks fixed the content, followed by rerendering and repeated affected validation. Initial screenshots remain under `preview-before-linebreaks`; final screenshots under `preview` show every equation and all five radio choices without clipping. Final reports have no raw TeX, MathJax/JavaScript errors, missing glyphs, or broken images. There are no dropdown controls or image assets to inspect. No shared script or grader defect required a repository repair.

All checks were offline. Publication and database identity checks remain the runner's responsibility. No generator implementation or live learner-selection behavior is claimed here.
