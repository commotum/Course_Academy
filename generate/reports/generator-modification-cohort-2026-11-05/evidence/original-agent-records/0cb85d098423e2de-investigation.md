# Investigation: cosine sums and differences in radians

Target KP **17592186059665**, “Simplifying Expressions in Radians Using the Sum and Difference Formulas”; supplied math snapshot, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, basis **8015**. Read the target KP, all 18 practice records and their supplied banks/solutions, canonical example, containing lesson, source eligibility, image manifest and reference questions. Also read `generate/principles.md`, `generate/docs/3-classify.md`, `docs/math-content.md` and the offline validation-tool instructions. No database queries or publication were performed.

## Learner operation and retained evidence

The learner identifies a cosine sum or difference, chooses the correct product sign, evaluates the fixed radian angle, and simplifies into sine/cosine of the variable. The lesson specifically warns that cosine's sum formula uses subtraction and its difference formula uses addition. Canonical example `1d8679d3-8922-5471-811f-60c8c41c853a` models formula → substitution → exact values → simplification for a quarter-turn shift.

Partial records remain exactly as supplied: `b7de6c52-4228-5d94-88f7-fec44c37c50f` supplies the half-turn prompt and five-way radio bank; `641fc75f-8c1c-588f-b1c6-9dde40645507` supplies a sum and radical/sign distractors; `609d2236-8468-565e-9ebe-8fd019ac095c` supplies a quarter-turn sum and complete explanation; `11214dee-7d32-5b34-bc7e-86bbedbaab36` supplies a quadrant-II difference and its explanation. Their absent fields/keys/labels are partial evidence, not defects.

Complete moderate example `e50bbccc-38f5-586c-b552-2dd92be5a0c5` uses one expression blank. Complete hard evidence includes five radio questions and eight two-coefficient questions. Radio example `8f2cac98-d46c-5a68-832a-abb863407c09` requires the sum sign and quadrant-II values. Coefficient examples `31d126d7-a9c2-531e-862e-71990d0a9843`, `9aca0bad-fb3b-5bb9-b62a-e54827012cdd` and `54143b7e-cf85-50bc-aa52-bc77e56d6283` preserve sine-before-cosine ordering, radicals and signed coefficients, sometimes with a sign already printed outside a blank. Retained these response families and the stepwise explanations. No select menus occur.

The supplied prerequisite list is empty; the mathematical prerequisites are special-angle values, quadrant signs and signed arithmetic. Adjacent lesson examples address degrees and exact numerical cosine values; those are outside these examples' variable-angle task. Inspected the sole diagram (`images/5e/5ed2cf9e528e7ec6762875f3dfaf211aba656e6b39025109315539a7dd4b013a.png`): unit-circle points P/Q, angles A/B and their difference support the lesson's distance/law-of-cosines proof. No target practice question uses it. It stays lesson context; these algebraic practice prompts need no image or new asset (plot requirement: none).

## Reference comparison and authored progression

Reference KP **17592186054787** assesses distribution over a signed term and collection of like terms. Easy `e47c7dff-9b13-5c86-8db2-973382940a0f` and `5d0b6029-5d16-5038-805d-6574595234a2` combine one distribution with one collection. Moderate `e474bc44-1cd0-59d9-b243-4f2f3cc65ac2` and `7ece68ae-b0bf-5eed-aec9-db4933ac6a74` put the multiplier after the parentheses and require organizing the resulting terms. Hard `fadc73be-dedf-5384-82b7-e3c8b9123466` and `4d334025-0c34-5846-8199-851ecb05753e` require two collections after distribution. Blanks prescribe term order and sometimes signs; radio appears at both easy and hard. The reference's detailed distribution steps appear **after** answering, so they are explanations, not prior scaffolding. Its levels overlap; neither response type nor coefficient magnitude alone defines difficulty.

Exactly three complete new questions are in `exemplars.json`:

| Level / question UUID | Before-answer demands and support |
| --- | --- |
| Easy / `1a6e479f-9657-40a1-8a10-607e4e3d30a3` | Simplify cos(t−π). Formula and special-angle values are supplied in the prompt. Substitute and collapse the zero term; choose −cos t from the retained five-way sign/function/zero bank. |
| Moderate / `dce93679-0d3f-4452-91c5-82d9e1bb898f` | Simplify cos(t+π/2) in one expression blank. Retrieve the sum formula and axis values without a prompt hint; resolve the surviving minus sign to obtain −sin t. |
| Hard / `855dff12-bedd-4c08-a5d9-0da320486081` | Expand cos(t−5π/6) into two signed coefficients in the supplied sine/cosine order. Retrieve quadrant-II values, keep both nonzero terms, apply the difference sign, reorder, and enter 1/2 and −√3/2. |

This transfers the reference's increase in independent organization and simultaneous signed components, while using the target's mathematics. Easy adds explicit support because no complete easy import exists. Moderate removes that support; hard adds quadrant reasoning and two surviving coefficients. The hard layout keeps source coefficient scaffolding but prints a plus between the blanks so the learner supplies the second coefficient's negative sign. All formula/value reminders in moderate and hard are in the worked solutions only.

Imported labels remain evidence rather than a binding difficulty rule: `094c30c7-640d-5075-b2ee-56000c80b71b` is labeled hard despite an axis-angle collapse. There is no pedagogical reason to force a zero term into our hard exemplar merely to match that label. Observed coverage stays **moderate, hard**, with **0/1/13 complete imported easy/moderate/hard examples**; authored examples do not change those counts. All new question/field/answer UUIDs are fresh, and no Math Academy identity or authored/reconstructed tag was added.

## Checks and evidence

Independently solve using complex rotations: the real parts of `(cos t+i sin t)` multiplied respectively by `−1`, `i`, and `−√3/2−i/2` are `−cos t`, `−sin t`, and `−√3 cos t/2+sin t/2`. This checks the signs without reusing the written solution steps. Coefficients were also recovered from cosine at t=0 and t=π/2; direct cosine evaluation at 25 angles per identity agreed within 6×10⁻¹⁶ (`evidence/independent-math.json`).

The actual native `learning::grade_field` passed **26 checks: 10 accepted, 16 rejected, 0 unresolved** (`evidence/grader-input.json`, `evidence/grading.json`). Tested every radio choice; canonical and equivalent blank answers; wrong signs, swapped coefficients, wrong functions, zero and lost denominators. Equivalent fractions/radicals are allowed because these prompts do not require simplest form.

Ran `check_delivery.py` separately at each difficulty against the supplied source/inventory: each accepted its one record, with zero duplicates (`evidence/delivery/{easy,moderate,hard}/delivery.json`). These checks cover actual publication preparation without writing to the database.

Rendered all three records through `generate/pipeline/render_preview.py`. Inspected **all three screenshots** and `evidence/rendered/rendering.json`: prompts, five radio alternatives, inline blanks, negative radical coefficient, aligned equations and full solutions are readable, without clipping or exposed TeX. Reports show loaded fonts and no math, image, JavaScript or dangling-glyph errors. No dropdowns or question diagrams require additional inspection. No grader/renderer/helper defect was encountered; no shared repair was needed.

These are instructional anchors, not a generator or a claim of exhaustive variation. The next phase can vary the sum/difference, axis/non-axis angle, quadrant, surviving function and signed coefficient roles within these demands; it must avoid making answer sign or position predictable from a template.
