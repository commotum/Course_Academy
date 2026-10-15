# Period generator and inventory replenishment

Frozen math basis 1356. Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186129122/validate.py
.venv/bin/python generate/scratch/17592186129122.py --difficulty all --count 2 --seed 19 --format markdown
.venv/bin/python generate/scratch/17592186129122.py --difficulty easy --profile raw:q-53457 --format json
```

Public API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` plus easy/moderate/hard entrypoints. `profile='method'` is the learner-eligible default; `raw:<source-id>` renders a parameterized evidence profile preserving original fields and omissions, with eligible_for_learning false. Exact original parameters and full independent bank-component inputs are in source-cases.json. Raw evidence is not a source-answer lookup branch: prompts, complete stages and banks render through component masks and rational parameters. Option UUIDs are field-owned and content-stable across seed/order changes.

Easy samples all eight source-shaped families. Moderate and hard are authored missing-level scope, documented in classification.md and template-extraction.md. Every bank uses all five specified operations; collisions reject the entire explicit instance or resample all parameters. The generator itself has no database access. The scoped `replenish.py` runner uses the existing EDB integration for inventory reads, registration and additive content commits. Original opaque banks, fieldless records, unrated records and the q-43411 teaching-rule error remain publicly reviewable; their limitations are explicit in validation.json.

Validation independently parses actual printed prompt frequency, every bank value, every displayed calculation equality, the opening formula and final period conclusion. It exhausts finite frequency domains, samples signed forms, checks source key presence, complete source prose/value fidelity, identity invariants, negative mutation controls and real `course_academy_engine::learning::grade_field` UUID selection. Raw missing fields/keys remain ungraded; completed normal radio records are graded. review.md includes every original/profile and two changed easy examples per template, plus four examples at each authored level.


The learner path normalizes prose and bare math values with `math_format.py` before assigning identities and checks every record with `checked_math_content`. Raw evidence preserves the captured spelling and missing fields separately.

Inventory replenishment is scoped to this KP:

```sh
.venv/bin/python generate/scratch/17592186129122/replenish.py
```

The runner holds the application `api.lock` from its current basis/inventory recheck through submission and readback. It retains exact requests, native validation previews, receipts, mathematical checks, actual grader results and source-preservation verification under `reference/replenishment/`. Saved requests are reconciled before new work. Contributor: `:application/ca-engine`. Registered generator UUID: `e271c703-96fb-5dae-b1ad-7dc8b8c5ac21`; script: `generate/scratch/17592186129122.py`.

The first replenishment read basis 2533, independently counted 4 complete, mathematically validated fresh easy sources, and committed 1 easy, 5 moderate and 5 hard questions at basis 2534. All eight source questions and the canonical example were preserved. The source q-43411 is additionally excluded from this job's validated reserve because its introductory teaching formula is false; its stored content is unchanged. `capabilities.json` distinguishes source-supported easy forms from the validated authored moderate/hard extensions. No unsupported levels are claimed filled.
