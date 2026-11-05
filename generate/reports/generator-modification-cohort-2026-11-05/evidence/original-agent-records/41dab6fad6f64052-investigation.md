# Finding Exact Values Using the Sum and Difference Formulas

KP **17592186059663**, UUID `213eda96-c41d-5361-9da9-8349617014f1`. Evidence: supplied math snapshots, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`, basis **7429**. Read `generate/principles.md`, `generate/docs/3-classify.md`, and `generate/pipeline/validation-tools.md`.

## Decision and learner operation

The seven complete imported questions supply usable easy, moderate, and hard examples: **2 / 4 / 1** respectively. No reconstruction is needed; `exemplars_file` is **null**. The complete imports below are the instructional examples for the next phase. Observed coverage remains easy/moderate/hard. No imported question, database state, shared code, or published asset was changed.

The learner expresses a non-special angle as a sum or difference of special angles, applies

$$\sin(u\pm v)=\sin u\cos v\pm\cos u\sin v,$$

substitutes signed unit-circle values, multiplies radicals, and combines the exact terms. This KP assesses numerical sine values. Its enclosing lesson also teaches symbolic expansions and derives the identities; those are context, not additional response demands here. Do not expand the scope to cosine/tangent addition formulas, double-angle expressions, or identity proofs.

## Retained source instruction

The lesson, *The Sum and Difference Formulas for Sine*, introduces both identities and works through $75^\circ=45^\circ+30^\circ$, then places this KP before neighboring symbolic degree/radian KPs and the later proofs. Canonical example **7341638b-3c0f-5c10-8b7d-a2c313607bed** supplies $\pi/12=\pi/3-\pi/4$ and derives $(\sqrt6-\sqrt2)/4$. It supports the method but is not counted as a practice question.

Retain the explicit angle-split hints where present, exact-value instructions, single radio or embedded blank response, full banks, and solutions that state the formula, identify its arguments, substitute all four trigonometric values, and simplify. Formula recall and intermediate algebra in the worked solution are shown after answering; they are not interactive steps or prompt support.

Prerequisite topics are *The Product Rule for Radicals* and *Evaluating Trigonometric Expressions*. Read their canonical examples and inspected both supplied degree/radian unit-circle PNGs (`d93c490a…955e.png`, `dbf36192…aa6.png`): their coordinates support signed sine/cosine retrieval. These diagrams occur in prerequisite solutions, not target practice prompts. Preserve that role; do not add a unit-circle scaffold to target questions silently. All target templates have plot rating **none**; no new diagrams are needed.

## Complete target examples and progression

All radio fields use key `selection`, five math choices, and one correct reference. Blanks use key `field-1`, one math answer value and its correct reference. There are no dropdowns or mixed fields.

| Imported level | Question ID | Supplied task/support | Response and exact result |
|---|---|---|---|
| Easy | `d93d90d2-8105-59cb-a801-47640240ddbd` | $\sin(5\pi/12)$; hint $\pi/4+\pi/6$ | Radio; $(\sqrt6+\sqrt2)/4$ |
| Easy | `4bf1dbaf-6e61-5607-8543-7f1dda28cf3f` | $\sin(11\pi/12)$; hint $7\pi/6-\pi/4$ | Radio; $(\sqrt6-\sqrt2)/4$ |
| Moderate | `2f345820-3d37-51b7-9bb6-51dedb3880f8` | $\sin75^\circ$; given $45^\circ+30^\circ$ | Blank; $(\sqrt6+\sqrt2)/4$ |
| Moderate | `16e4e461-f621-53d1-96fa-7b2df72cfebc` | $\sin105^\circ$; given $60^\circ+45^\circ$ | Blank; $(\sqrt6+\sqrt2)/4$ |
| Moderate | `996eb380-c7f3-58b2-8258-bc17318d5244` | $\sin75^\circ$; given $135^\circ-60^\circ$ | Blank; $(\sqrt2+\sqrt6)/4$ |
| Moderate | `585e18d7-2aa5-5d3f-86ad-587ffce85678` | $\sin(-105^\circ)$; hint $30^\circ-135^\circ$ | Radio; $-(\sqrt2+\sqrt6)/4$ |
| Hard | `97e8e577-5bc3-50c1-b8c6-66747cc71a22` | $\sin75^\circ$; **no split supplied** | Radio; $(\sqrt6+\sqrt2)/4$ |

Easy assesses execution with a supplied decomposition and answer recognition. Moderate either removes the answer bank while retaining the decomposition, or retains recognition while requiring negative-angle/quadrant sign handling. Hard removes decomposition support: finding a usable special-angle pair is work required before selection. The $45^\circ+30^\circ$ split appears only in its solution. Retain its radio format rather than imposing a hard-level blank requirement.

These are overlapping demands, not a perfectly ordered scale: the easy difference item already uses signed values, and hard returns to radio. The meaningful increase is independence in selecting a decomposition, not angle magnitude or larger coefficients. This corrects any assumption that response type alone determines difficulty.

For classification, separate the two easy sum/difference solution backbones; moderate has guided-sum blank (two parameter variants), guided-difference blank, and hinted-difference radio; hard has unhinted-sum radio. Each radio backbone has one observed complete bank profile; blanks have no distractor profile. Keep the distinct radio banks in `evidence/existing-target-records.json`: they include sign, sum/difference, radical-product and denominator errors, not a universal interchangeable bank.

## Reference comparison

Reference KP **17592186087671**, *Finding Exact Values of Trigonometric Expressions Using the Double-Angle Formula*, supplies:

| Level | Supplied question IDs | Learner demand |
|---|---|---|
| Easy | `baeab088-833a-54f7-96df-e4a2e1a80c83`, `908ae38c-0e5f-5da6-8253-8eb427ca6c40` | Recognize $\cos^2x-\sin^2x$, evaluate the doubled special angle; radio |
| Moderate | `a0283435-c23b-5d26-b5af-8d4a513ca18b`, `f9ed8218-8b72-5f11-b5f2-bf16df5e7136` | Recognize $1-2\sin^2x$ as another cosine double-angle form; radio |
| Hard | `7227f9ac-0ffc-5d99-83ac-2d10c6986d6c`, `7667b041-07ed-5199-9efb-833c8da623ff` | First recognize a hidden perfect square, then apply the identity and square the value; blank |

The reference identities and factorization appear in solutions, not as pre-answer scaffolds. Its useful design principle is requiring an additional structural recognition before the familiar identity, with response production also increasing at hard. Adapt structural recognition here as independently choosing the angle split. Do not import its quartic algebra or assume this target must match its radio/radio/blank sequence.

## Partial evidence and limits

Partial import **a3970135-b09a-510a-8a49-4f060f0ca725** supplies $\sin345^\circ$, the hint $300^\circ+45^\circ$, and a five-choice radio bank. Its solution, difficulty and correct reference are absent. It remains exactly as stored, supplies partial scaffold/bank evidence, and is neither a complete template nor a repair task. No level or stored answer key was inferred for it.

The single complete hard item supports only unhinted degree-sum practice directly. Three of four moderate answers and the hard answer coincide; these examples establish instruction, not sufficient variety for a future generator. Future same-method variation must derive the split, signed products, answer, bank and explanation together, rather than always returning the same radical sum. Larger angles alone do not establish a new difficulty band. No sampling, publication, or variety audit is claimed in this phase.

## Checks and evidence

- Independently evaluated all seven complete target expressions and all six reference expressions symbolically from their prompt angles, then checked every supplied bank value and unique correct reference (`evidence/independent-math.json`). Read all worked derivations; their signs, products, and results agree.
- Ran the actual native `learning::grade_field` via `generate/runs/current/check-engine`: **18 accepted, 42 rejected, zero unresolved**, across 13 target/reference questions. Every radio option was tested; blank checks include exact/equivalent forms and sign/scale mistakes. Inputs and full report: `evidence/native-checks.json`, `evidence/native-grading.json`.
- Rendered all seven complete target records through `generate/pipeline/render_preview.py --limit 7`, using the installed browser and unmodified learner UI. Inspected every screenshot and the full `evidence/preview/rendering.json`: all seven pass, with no raw TeX, math/JavaScript errors, broken images or dangling glyphs. Inspected prompts, banks, inline answer locations and complete solutions; no dropdown menus exist. One long radian solution uses the UI's horizontal math scrolling; supplemental scroll inspection is saved under `evidence/scroll-preview/`.
- Validation copies only change pulled correct-answer maps into UUID lookup references for the offline harness; they retain imported identities/content and are evidence, not new exemplars or publication input. Reproducible math/case preparation is in `evidence/verify_snapshot.py`. Snapshot SHA-256 values in `evidence/snapshot-hashes.json` bind this account to the supplied files. No shared helper/grader defect was found and no shared repair was necessary.
