# Investigation: alternative cosine double-angle forms

Target KP **17592186087670**, “Using Alternative Forms of Double-Angle Formula to Simplify Expressions.” Read the supplied source, inventory, and reference snapshots at **math basis 7317**, lineage **01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1**, plus `generate/principles.md`, `generate/docs/3-classify.md`, and the validation-tool instructions. No additional database selection or queries were used.

The learner identifies either $2\cos^2x-1$ or $1-2\sin^2x$, exposes that structure if necessary, and replaces it by $\cos(2x)$ while preserving any outside multiplier. This is expression rewriting, not finding an exact numerical trig value or solving for an angle. The canonical example **17592186087478 / e-3667** rewrites $2\cos^2(\pi/3)-1$ as $\cos(2\pi/3)$.

The full lesson **17592186087908** derives the cosine double-angle formula from the sum formula, derives both alternative forms using the Pythagorean identity in tutorial **2639**, then introduces this KP. Its preceding KP **17592186087669** uses $\cos^2x-\sin^2x$; its following KP **17592186087671** asks for exact numerical values. The captured prerequisite collection is empty: these lesson relationships supply context, not an invented prerequisite inventory. The source has no diagrams or image assets, and its eligibility ledger excludes no questions.

## Target evidence retained

All 15 imported questions have one radio field, five math choices, and a worked solution. All were read, including their complete banks. Two mathematical backbones occur at each observed level; angle units and outside coefficient types vary within them. Plot requirement is **none** throughout.

| Level and backbone | Supplied practice IDs (database / captured ID) | Bank distinctions |
| --- | --- | --- |
| Easy: $2\cos^2x-1$ | 17592186088095 / q-24490; 17592186345262 / q-7692; 17592186345265 / q-7695; 17592186345266 / q-7697; 17592186598566 / q-24502 | Radian angle errors, or degree choices confusing sine/cosine, powers and factors |
| Easy: $1-2\sin^2x$ | 17592186256396 / q-120357; 17592186290546 / q-24341; 17592186600356 / q-24487 | Undoubled/halved/incorrect angles, sign, coefficient or function errors |
| Moderate: $a(2\cos^2x-1)$, initially expanded | 17592186341956 / q-7338; 17592186600406 / q-7340 | Outside-factor, radical, function and angle errors |
| Moderate: $a(1-2\sin^2x)$, initially expanded | 17592186088339 / q-7698; 17592186256397 / q-120358; 17592186256398 / q-120362; 17592186344970 / q-7469; 17592186345263 / q-7693 | Integer, radical and fractional multipliers; distractors lose/change the multiplier or misapply the identity |

Preserved components: the “single trigonometric ratio” task, five-choice radio response, both cosine identities, degree/radian notation, explicit identity/substitution steps, and factoring before identity use where needed. The source permits a constant multiple of a ratio, as in q-120358. Formula reminders and factorization appear **after submission in solutions**, not as advance hints. Each new prompt likewise requires the learner to decide the transformation before choosing.

Two source banks have accidental equivalent alternatives: q-7695 offers $\cos(90^\circ)$, $\cos^2(90^\circ)$ and $2\cos^2(90^\circ)$, all zero; q-24502 offers both $\cos(8\pi/5)$ and $\cos(2\pi/5)$. Imports remain unchanged. The new banks avoid these collisions rather than reproducing source mistakes.

## Reference progression and adaptation

Reference KP **17592186059673**, “Using the Double-Angle Formula to Simplify Ratios,” supplies these six complete examples:

- Easy: **17592186335850 / q-65612**, direct sine double-angle substitution and cancellation; **17592186335851 / q-65614**, also rewriting cotangent.
- Moderate: **17592186060241 / q-24642**, expanding the denominator and recognizing a reciprocal; **17592186253627 / q-120017**, reciprocal rewriting and cancellation.
- Hard: **17592186253632 / q-120029**, sine double-angle substitution, tangent rewriting, Pythagorean substitution, factoring and cancellation; **17592186253633 / q-120030**, the analogous cotangent/sine-denominator case.

Each reference remains one five-choice radio field. No prompt supplies intermediate transformations. Difficulty grows through less visible structure and coordinated algebra, not response-format changes, bigger angles or longer post-answer prose. The easy reference itself varies in workload, so it would be inaccurate to assign levels purely by counting displayed solution lines.

The three new examples in `exemplars.json` apply that progression to this KP:

| Level | Required operation before selection | Result |
| --- | --- | --- |
| Easy | Recognize $2\cos^2(26^\circ)-1$ and double the angle once | $\cos(52^\circ)$ |
| Moderate | Factor $3$ from $3-6\sin^2(\pi/10)$, use the other alternative form, retain the multiplier | $3\cos(\pi/5)$ |
| Hard | Regroup $8\cos^4(18^\circ)-8\cos^2(18^\circ)+1$ as $2(2\cos^2(18^\circ)-1)^2-1$, then apply the same identity twice | $\cos(72^\circ)$ |

Hard is a deliberate same-skill extension, not an imported hard template: polynomial regrouping exposes a nested use of the already taught identity. No sine-ratio cancellation, cotangent, new trig identity, or memorized quadruple-angle formula is required. The solution verifies the regrouping by expansion, but the prompt does not supply it. Recognition and two coordinated substitutions create the extra demand; the coefficient 8 alone does not establish difficulty.

Observed coverage remains **easy and moderate**: 8 complete easy, 7 complete moderate, 0 hard, no incomplete imports. These three ordinary questions supply construction examples without changing that historical observation. They have fresh question, field and answer UUIDs and no Math Academy identities or reconstruction tags.

## Checks and usable result

- `evidence/verify_math.py` independently expanded the target cosines and proved all three general identities with SymPy. It evaluated each original and every option at 30-digit precision, verified exactly one correct choice and five distinct mathematical values per bank, and checked all 21 UUIDs. See `evidence/independent-math.json`.
- Actual native `learning::grade_field`, through `generate/runs/current/check-engine`, accepted all 3 correct choices and rejected all 12 plausible wrong choices, with zero unresolved responses. Full records and submissions: `evidence/grader-cases.json`; results: `evidence/grading.json`.
- Ran `generate/pipeline/check_delivery.py` separately for each difficulty against the supplied inventory. Each accepted 1 of 1 records, with no duplicates. See `evidence/delivery/{easy,moderate,hard}/delivery.json`. This was offline validation, not publication.
- Ran `generate/pipeline/render_preview.py` through the unchanged learning UI. Inspected all three screenshots and the JSON report, including all choices and full solutions. Initially a long hard-solution equation clipped; split that local content into two rows, reran mathematical, grading, hard-delivery and all rendering checks, and inspected the corrected hard screenshot. Final report passes all 3 with no raw TeX, math errors, missing glyphs, broken images or JavaScript errors. These are radio controls; there are no dropdown menus or diagrams to inspect. Final screenshots: `evidence/rendering/question-001.png` through `question-003.png`.

No shared repository code needed repair. No imports, other KP jobs, services or database state were changed. The examples and evidence are ready for the next scripted phase. This verifies these three instructional examples, not a randomized generator, arbitrary screen widths or live publication/selection behavior.
