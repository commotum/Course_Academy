# Canonical example migration

On 2026-10-04, `course-academy-v2` retired `question/is-example` in one atomic transaction from basis 415 to 416. Questions now derive their worked-example role from incoming `knowledge-point/canonical-example` references. Canonical targets are excluded from every KP practice pool. Having a worked solution does not determine a question's role.

The transaction retracted all 30,452 current flag facts, removed the flag from the installed `question/validate` required attributes, and marked its installed definition retired. EDB retains that definition and historical assertions. Fresh schema files omit the attribute. The schema readback confirms that `question/validate` requires only `question/id` and `question/problem`.

The Rust and Python readers, lesson delivery and completion handlers, assignment and topic views, capture reconciliation, seed generators, and importers use canonical references. The API's `isExample` property remains a derived presentation value. Saved capture payloads, checkpoints, and test fixtures were subsequently normalized to remove `is_example`; their `canonical_examples` collections retain the observed canonical references. Imports reject the retired capture field. Actual transaction receipts remain unchanged.

Completed import plans affected by the payload normalization are retained with their original transaction and receipt under `edb-import/committed-before-capture-format-migration/`. Subsequent imports plan against the current database rather than replaying those historical transactions. Completion checkpoints and import verification records are retained. The local capture-format migration report is `.local/question_capture/canonical-reference-check/capture-format-migration.json`.

## Content preservation

| Verified at basis 416 | Count |
| --- | ---: |
| Questions | 30,452 |
| Canonical examples | 9,637 |
| Ordinary questions | 20,815 |
| Distinct questions in KP practice pools | 20,711 |
| Questions added since the previous active export | 1,170 |
| Other domain facts, all unchanged | 840,524 |

The latest export of legacy `course-academy` at basis 143 is byte-for-byte identical to the original migration source. The newer questions are in the active database. All legacy content identities are accounted for using the original 45 duplicate-answer UUID replacements and the previously retired, unreferenced, empty Self-Directed course placeholder. No questions or answers were dropped by this retirement.

Before/after hashes cover every domain fact except `question/is-example`, including learner state and answer keys. The preserved-fact SHA-256 is `d10bc1b6b41c0ce1638eb714a522b9ceabdd1127bff4f4202527dd389ac4ed59`.

No new backup was made, as requested. Read-only exports capture immutable database values for verification. The transaction used an exact basis guard and a stable request key; its committed transaction hash is `87a493dad9bc66834625032cc55067e266e45d73dd5abdb10d50b09e49829379`.

## Reproducing the verification

[retire_question_example_flag.py](../scripts/retire_question_example_flag.py) prepares transaction files and verifies captured exports; it does not submit writes. [export_edb_snapshot.rs](../scripts/export_edb_snapshot.rs) supports read-only live exports as well as backup exports.

Local evidence is under ignored `.local/edb/canonical-example-migration/`: `atomic/plan.json`, `atomic/retire.edn`, `atomic/preview.edn`, `atomic/commit.edn`, `schema-after.edn`, `current-before-415.jsonl`, `current-after.jsonl`, and `verification.json`.

```sh
python scripts/retire_question_example_flag.py verify \
  --before .local/edb/canonical-example-migration/current-before-415.jsonl \
  --after .local/edb/canonical-example-migration/current-after.jsonl \
  --report .local/edb/canonical-example-migration/verification.json
```

Readers must capture canonical references with their question records. Curriculum changes must refresh the derived role index. Interpret historical presentations against their historical database value if canonical references have changed.

## Application checks

All 66 Rust engine tests, 142 Python engine tests, and 136 capture tests passed. The native learning helper passed 13 tests and the native graph/topic reader passed eight. The lesson view JavaScript check passed.

The live home, assignments, topic, and lesson preview routes returned successfully. A lesson preview contained four canonical examples with worked solutions and 11 ordinary practice questions; topic sections also displayed worked solutions.

The durable integration check completed a lesson with 13 presentations using an isolated learner, persisted answer results, XP, accuracy, and FIRe progress, and then removed the temporary learner. Final live queries confirmed zero `question/is-example` facts and no remaining temporary learner. The application and writer services remained active after migration.
