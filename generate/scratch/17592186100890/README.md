# Trigonometric Cartesian-equation generator draft

Rebuilt **Finding the Cartesian Equation of a Curve Defined Parametrically With Trigonometric Functions**, KP `17592186100890`, from all 20 practice questions at database basis `1356`.

**Review status: all captured source banks reproduce in full.** Draft version `trig-cartesian-guide-draft-4` retains 14 observed radio bank profiles within 13 observed templates and adds two cotangent templates with four authored moderate banks (15 templates and 18 banks total). It reproduces all 56 original distractors and the correct designation in all 14 radio banks, plus all six blank answers. Mathematical correctness, actual grading, and source fidelity are reported separately. This validates the captured examples; inferred recipes do not establish how the original authors generated unseen questions.

- [Classification](classification.md): seven easy, two observed moderate, and four hard templates, plus two authored moderate cotangent counterparts; original field types are preserved and moderate remains radio.
- [Template extraction](template-extraction.md): source features, fixed wording, answer fragments, constraints, optional components, and inferred distractor transformations; [extraction.json](extraction.json) retains all four extraction stages.
- [Choice-bank extraction](choice-bank-extraction.md): all 14 profiles, their formulas and constraints; [choice-extraction.json](choice-extraction.json) maps all 76 original answer values to replay results.
- [Generator](../17592186100890.py): SymPy arithmetic, deterministic parameters and field-owned identities, correct-answer-first construction, and one fixed source-style worked solution.
- [Review](review.md): all 20 originals, each followed by two distinct variants using the same observed bank profile or blank template, plus the authored moderate variations; difficulty and origin are labeled. `review.json` includes all 56 generated examples displayed in the review.
- [Moderate variations](moderate-variations.md): agreed scope, correct-answer formulas, four authored distractor transformations, domains, and source provenance.
- [Moderate review](moderate-review.md): all sixteen family/quadrant combinations, with equal moderate difficulty and no instructional sequence.
- [Moderate validation](moderate-variation-validation.json): 64 family/quadrant/coefficient-boundary cases checked against independent exact curve coordinates, branch/domain assertions, displayed real incorrect choices, stable identity, and actual radio grading.
- [Source-bank fidelity](source-bank-fidelity.json): 24/24 ellipse distractors, 8/8 cosine double-angle distractors, and 24/24 other radio distractors, with one-to-one matching of complete displayed equations and correct flags, independent of choice order.
- [Validation](validation.json): 255 cases covering every template and profile, sampling and boundaries, source parameters, deterministic replay, content identity, answer ownership, and rejected invalid inputs; 34 original answer-side comparisons passed the native comparator. Additional selection checks exercise every default profile, including identity errors with shifted unequal-scale ellipses.
- [Actual grader results](engine-validation.json): 296 accepted checks, 946 rejected checks, and 39 documented unresolved checks using `learning::grade_field` with temporary in-memory fixtures.

Profiles are selected as complete banks before sampling; one invalid option rejects the entire instance rather than being replaced from a pooled list. Fixed parameters and profile retain identity across seed/order changes; changing the authored bank changes content identity while its parameter fingerprint remains the same. Radio samplers now include observed unit-scale shapes and offsets down to −5. The observed easy cotangent/cosecant radio bank requires a≥3 because the source's scale-minus-one recipe duplicates another option at a=2.

Classification, extraction, and local generator validation are complete through step 7. Steps 5 and 7 need no plot renderer because every template has plot rating **none**. This draft stops before steps 8 and 9; database writes are **zero**. The product-rule knowledge point has not been rebuilt.

The 39 unresolved grading checks are complete equations submitted to blanks that expect only an expression. Canonical entries and the tested correctly shaped equivalents pass, including `2√(1+x²/9)` versus `√(4+4x²/9)`. This rebuild does not edit the engine; the validation report records hashes of the engine sources used.

Moderate generation uniformly selects one of four sine/cosine × tangent/cotangent families, positive coefficients `a,b` from 1 through 4, and one open quadrant. These are unordered variations at the same difficulty. Normal sampling uses each family’s authored bank: wrong root sign, inverted quotient, omitted root, and incorrect y-scale. The two observed first-quadrant banks remain explicit source-replay profiles, including every original distractor. There is no unit/scaled switch or instructional-stage mode. Omitting `quadrant` in explicit parameters means quadrant I and produces the same identity as explicitly supplying `quadrant: 1`. Metadata distinguishes observed banks, authored extensions, coefficient variation, and method references. Sampling bounds and interpretations of observed recipes remain draft policies, not recovered source code.

Generate an author preview:

```bash
.venv/bin/python generate/scratch/17592186100890.py --difficulty easy --template ellipse_cos_blank --seed 42 --count 2
.venv/bin/python generate/scratch/17592186100890.py --difficulty moderate --seed 42 --format json
.venv/bin/python generate/scratch/17592186100890.py --difficulty moderate --template sin_cot_radio --seed 42
.venv/bin/python generate/scratch/17592186100890.py --difficulty moderate --profile sin_tan_source --seed 42
.venv/bin/python generate/scratch/17592186100890.py --difficulty easy --profile sin_unit_x_shift_identity --seed 42
```

Reproduce validation and rebuild the review:

```bash
.venv/bin/python generate/scratch/17592186100890/validate.py
```

Validation parses the original and generated displayed values with an independent strict checker for this KP's expression grammar, compares whole equations up to nonzero constant rescaling, and verifies rendered choices against symbolic formulas. Unsupported notation fails rather than being counted as a match. It also builds the existing Rust comparator offline and links a temporary harness to the actual application grader. It performs no database operations. Source evidence is already captured locally in [source.json](source.json), with the read query and inputs beside it. JSON previews are local review records, not transaction EDN. The version remains a draft pending review.

Current audit uses [source-capture.json](source-capture.json), the complete basis-1356 wrapper, with its record in [source.json](source.json). [source-basis-1308.json](source-basis-1308.json) retains prior evidence. [Current-source comparison](current-source-comparison.json) confirms no practice-question or canonical changes; the only new source metadata is the explicit key-prerequisite list. [Source and pedagogical QA](current-audit.md) records the scope assessment.

The public `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` interface now supplies the documented defaults. Validation also independently parses each displayed intermediate solution equality, evaluates it at exact rational unit-circle coordinates, and rejects a deliberately corrupted scale. Generator mathematics, approved moderate behavior, existing profiles, and draft-4 content identities are preserved.

The shared native grader independently reruns the same grading fixtures:

```bash
generate/runs/current/check-engine generate/scratch/17592186100890/engine-input.json generate/scratch/17592186100890/shared-engine-validation.json
```

[Shared-engine results](shared-engine-validation.json) contain the actual outcomes; [build provenance](shared-engine-provenance.json) records the harness/library-facing executable and engine-source hashes.
