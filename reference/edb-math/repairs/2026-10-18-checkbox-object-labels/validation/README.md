# Checkbox label repair validation

All helpers in this directory are read-only. They do not send a durable transaction.

`refresh DIRECTORY BASIS` opens one immutable native database value, reads
`DIRECTORY/native-pulls.edn`, and writes `capture-NAME.edn` for every Pull group.
The group format is `[["questions" "FULL_PULL_PATTERN" [ENTITY_IDS...]] ...]`.
It uses an `as_of(BASIS)` view even if the connection opens at a newer basis.
For every pulled entity containing `:question/id`, it also walks the actual
question→field→choice links and scans incoming references with VAET. `incoming.edn`
rows are `[source_entity attribute_eid target_entity tx contributor added]`.
The third cell is always a reference entity ID. `incoming-targets.edn` records the
complete reference census universe; `refresh-complete.json` certifies reaching
the end of all scans. The build uses the deployed writer's EDB library and its
fingerprint is retained in `refresh-build.json`.

The question Pull should include full question attributes, difficulty, KP/topic
and canonical memberships, every field and every choice/correct answer, and all
saved task items with complete responses. Every many-valued relationship must
specify `:limit nil`; the parent run's `audit.py` defines this exact shape.
Incoming references identify shared fields, shared answers and uses outside the
question's own task-item list; those require review before preparing changes.

`verify.py PLAN.json --output DIRECTORY` validates a plan with this shape:

```json
{"cases":[{"question":17592186272202,"before":{"...":"full Pull"},
"after":{"...":"full Pull"},"objects":[{"source_label":"I",
"field_id":17592186439013,"content":"The complete selectable statement"}]}]}
```

Optional `--before FILE --after FILE` use native preview or committed Pull results
instead of the plan's snapshots. Both snapshots must exactly match the reviewed
case. Files may be JSON arrays, EDN Pull arrays, or EDN query rows containing Pull
maps. Optional `--items-before FILE --items-after FILE` and
`--incoming-before FILE --incoming-after FILE` enforce unchanged complete item
state and incoming datoms. Inline `:task-item/_content` state is also compared.

The verifier permits only `:answer-field/key`, `:question/problem`, and
`:question/worked-solution` differences. All field/answer IDs and UUIDs, Boolean
banks, correct references, memberships, difficulty, answers and saved item state
must remain identical. It writes before/after presentation lint; the after lint
must pass. Shared-image exceptions require the skill's explicit reviewed proof.

`grade-preservation.rs` calls the real `course_academy_engine::learning::grade`
in memory using the actual entity IDs. It compares every Boolean subset when a
question has at most 12 checkboxes, always verifies the canonical subset, each
single-checkbox flip, incomplete submissions, and every saved response. Existing
incomplete saved responses must remain incomplete with the same native error.
`verify.py` uses the immutable checker in `pinned-grader/` when its manifest is
present. It verifies the executable, helper source and build record hashes on
each run and writes the exact version to `native-grader-version.json` and the
verification report. The build record retains the helper, engine library and
engine source hashes from the successful native build. This statically linked
artifact keeps long readback runs reproducible while unrelated engine work
continues. Without a pinned manifest, the helper builds against the current
engine library and checks that library against source modification times.

```sh
.venv/bin/python reference/edb-math/repairs/2026-10-18-checkbox-object-labels/validation/verify.py content-plan.json --output checks
node reference/edb-math/repairs/2026-10-18-checkbox-object-labels/validation/render.cjs checks
```

`render.cjs` reads `checks/render-cases.json` produced by verification. It renders
every before and after question at widths 893 and 375 through the real learning
page Markdown renderer, `fieldControl`, checkbox component and `collectResponses`.
It toggles every checkbox and verifies the submitted false/true answer entity IDs.
The local page may fetch static assets and a GET-only proxy to `/api/asset`; CSP
blocks connection APIs. `CA_ASSET_ORIGIN` defaults to `http://127.0.0.1:8765`.
Image loads, MathJax errors, empty labels, control counts and overflow are recorded
separately. `--widths=893,375,320` adds another narrow-width check. Targeted
screenshots cover the user's example, matrix/image/long options and failed cases.
Inspect those screenshots and any error or overflow differences before commit.
The rendering helper never calls learner, completion or transaction endpoints.

Native speculative preview remains the existing helper:

```text
reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/preview DIRECTORY SOURCE_IDENT EXPECTED_BASIS
```

It reads `transaction.edn` and `native-pulls.edn`, applies installed native schema
callbacks, and writes `preview-NAME-before.edn`, `preview-NAME-after.edn` plus a
speculative report on stdout. Verify exact transaction datoms/provenance using the
parent run's receipt checker; these presentation/grading checks supplement that
verification. Retain the original logical forms for durable submission.

Smoke evidence in `smoke/` uses one historical matrix-label repair: all eight
subsets, three single flips and incomplete responses passed native grading;
four before/after renders passed with no after errors or overflow. `refresh-smoke/`
captured the user's question at basis 3704, including three fields, six answers,
its saved response and 17 incoming reference datoms. These are helper checks, not
evidence that the current requested repair has been committed.
