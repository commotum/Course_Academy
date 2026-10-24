# Two-topic substitution pedagogy repair — 2026-10-24

Topics: **17592186048189**, Integration by Substitution With Inverse Trigonometric Functions; **17592186048245**, Integrating Exponential Functions Using Substitution. Original source/inventory snapshots were captured at **T6550**. Publication receipts and final live verification below bind the replacement pools to the database.

## Findings

The inverse-trig generators separated mathematical roles correctly and had valid derivatives and answers, but their hard contracts explicitly required irrational scaling, noncancelling factors, and sometimes fractional numerators or two awkward nonzero bounds simultaneously. The sampler even rejected useful cancellation. Those conditions increased prerequisite arithmetic together rather than adding one target decision. Worked solutions alone did not scaffold the learner before answering.

The active other-base exponential generator changed only the base in a small source subset, keeping exponent, differential relationship, and most question structure fixed. The other three exponential KPs had local drafts but no registered generator. Registration and executable delivery, rather than the presence of a draft, determine coverage.

The imports' strengths are compact derivative relationships and controlled structural changes. Examples: inverse sine q-2505 recognizes 2x, while q-2503 factors a square constant; inverse tangent q-49540 accounts for a differential factor, while q-49548 normalizes 9+x². Secant q-69476 keeps |8x| visible; q-73717 instead requires rewriting |x| after substitution. Exponential q-2382 uses x², q-73798 uses x³, and q-113847 introduces a negative derivative. Other-base q-73801 has a matching 2x differential; q-211992 changes the power to four without requiring integration by parts. Complex-case q-49577/q-73670 change the outer function to a square root/reciprocal square root; q-113873 tests recognition of the entire denominator's derivative. Definite q-346400 transforms simple power bounds; q-350751 uses a logarithmic derivative with exponential bounds.

Source labels are evidence, not an arithmetic sizing rule. Some easy imports themselves have larger constants or log/radical endpoints; these were not copied wholesale into the new easy band. The previous benchmark KP17592186064172 has two easy, three moderate and two hard imports: simple general-base exponentials, one scalar multiple, then a reciprocal base. Its useful lesson is one bounded conceptual change. See [the benchmark review](../../audits/2026-10-24-difficulty-pedagogy/README.md).

## Imported practice inventory

| KP | Skill | Easy | Moderate | Hard | Unclassified |
|---|---|---:|---:|---:|---:|
|17592186064218|Inverse sine|9|6|0|0|
|17592186064219|Inverse tangent|9|7|0|0|
|17592186064250|Inverse secant|0|5|12|0|
|17592186064220|Definite inverse trig|5|14|8|0|
|17592186184349|Products with e|2|3|1|2|
|17592186184350|Products with other bases|6|2|1|1|
|17592186184351|More complex cases|2|4|5|1|
|17592186184352|Definite exponential|5|3|1|1|

Counts describe stored imported practice labels, not an assertion that every import is complete or eligible as a generation template. Canonicals, original answers/solutions, source eligibility, and prerequisites remain in each source snapshot. No imported or canonical record is changed by this repair.

## Replacement contracts

Easy supplies u and asks only for the transformed integral, with five distinct choices. Moderate asks for the supported full calculation with a supplied primitive. Hard keeps that support and adds one target condition:

| KP | Moderate | Relative hard challenge |
|---|---|---|
|Inverse sine/tangent|One constant normalization|Both small perfect-square coefficients require normalization|
|Inverse secant|Visible \|ax\| and a small differential factor|Rewrite \|x\| using \|u\|, explicitly on both real components|
|Definite inverse trig|Normalize and evaluate from zero|Evaluate between two nonzero symmetric transformed bounds; inverse values, including negative values, supplied|
|Products with e / another base|Recognize a positive power inner function|Recognize a negative inner derivative|
|More complex exponential|Recognize a root or simple logarithmic outer function|Recognize the derivative of an entire composite denominator|
|Definite exponential|Transform simple base-exponential bounds|Transform bounds for a logarithmic derivative; exponential endpoint facts supplied|

These are **source-informed authored bands**, not inherited or empirically calibrated ratings. In particular, sine/tangent have no imported hard anchors, and secant has no easy anchor. The new scaffolding and controlled extra decision justify relative progression; no external calibration is claimed.

Numerators are integers 1–4. Inverse scales use small integers 2–5 and their ratios, with perfect-square constants at most 25. Exponential power inners use degree 2 or 3 and slope magnitude at most 2. Cancellation is allowed. The sampler balances source-supported families, requires several substitutions in an eight-question band, avoids duplicate mathematical tasks, and excludes prior full-calculation integrands. Easy transformations may share the integrand of an imported full-calculation question because they assess a different stage; this distinction is explicit in the contract.

Inverse antiderivatives use complete five-choice banks, including wrong factors and wrong arguments. Native free-entry grading does **not** currently support inverse-function notation; publishing such blanks would leave valid entries unresolved. The repair uses the supported response format rather than publishing those broken blanks. Other full calculations use exact blanks, with an external +C for indefinite answers so numerical constant shifts are accepted. No decimal padding is demanded.

Solutions show du, the differential factor, normalization (including the absolute-value conversion for secant), both new bounds when applicable, primitive evaluation, and the exact final answer. Negative inverse values are supplied before feedback. Log differences are retained rather than silently converted using a log identity.

## Implementation and verification

Shared implementation: `generate/substitution_pedagogy.py`; eight public entrypoints under `generate/scratch/<kp>.py`; immutable relocated packages retained per KP. `scripts/substitution_pedagogy_batch_policy.py` is called by the actual shared publication filter. Author/reviewer/template prompts now explicitly prohibit manufacturing difficulty by rejecting cancellation, require meaningful endpoint support, and call out base-only exponential variation.

Each band has eight fresh questions: **192 total**. Printed-math checks independently parse questions, substitutions, differential factors, primitive formulas, answer banks, and final keys across the intended pools and an additional seed: **384 records**, then recheck all 192 normalized delivery records. Native checks exercise every radio choice and accepted/equivalent/constant-shift/wrong blank entries: **320 accepted and 528 rejected checks, with zero unresolved outcomes**. The native engine source and binary hashes match the previously verified current build. Publication-filter/source-policy regression tests: **45 passed**. Actual unmodified learner UI rendering covers easy/moderate/hard for every KP; screenshots are visually inspected as well as machine checked.

`deploy.py` uses the shared KP/API locks, source/basis checks, exact transaction previews, durable request keys, receipt verification, and historical readback. It retires only unimported, noncanonical generated questions. The 106 superseded generated records retain their entities, answers, KP membership, and saved-attempt references. All 115 imported practice questions and eight canonicals remain unchanged. `completion.json` and `live-pool-verification.json` record the final committed counts; `live-grading-verification.json` records read-only live application checks.

## Final answer-bank correction

The first unserved preview banks had a deterministic numerical-rank shortcut in easy, and overly regular coefficient/argument combinations in inverse antiderivatives. `check_banks.py` reproduces that failure in all eight initial pools. The final generator samples complete diagnostic error profiles deterministically per mathematical instance, balances correct-factor ranks within each easy batch, and checks numerical-rank, sign-counterpart, and component-mode guesses against the delivered questions. Option shuffling alone is explicitly rejected as a fix. The publication guard and author/reviewer prompts now enforce this additional check.

Before release, `refine_banks.py` replaced 112 unserved multiple-choice previews and preserved the other 80 exact-entry questions. No answered question was rewritten. The final active generated pool remains 192 questions. There are 218 retirement flags from this run: 106 prior-pool questions plus 112 discarded unserved previews. Each refinement uses a fresh basis and an explicit no-task-reference check, archives the exact transaction/receipt, and verifies all source content and learner facts remain intact.
