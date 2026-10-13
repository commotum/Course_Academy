# Candidate generator run

The user's requested 120 topics contain **384 distinct KPs** at the captured `math` database basis **1356**, lineage `01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. [candidates.json](candidates.json) is the finder result; [manifest.json](manifest.json) tracks each individual KP assignment and independent QA. All work stops after generator/plot creation and validation (steps 3–7); no database writes.

Workers use **gpt-6.1-sol / high**, one assignment per KP, with at most three workers alongside parent QA. Captured source questions and curriculum context are in `sources/`, `topics/`, and `lessons/`, with fixed-basis EDN read evidence. Raw snapshots stay unchanged. Review artifacts are under `generate/scratch/<KP-ID>/` and scripts at `generate/scratch/<KP-ID>.py`.

The principles are [../../principles.md](../../principles.md); [worker-instructions.md](worker-instructions.md) carries the assignment contract. Completion requires parent QA of all three principles, not merely a worker's reported success. Source anomalies, repairs, sparse-level authorship, and grading limitations must be explicit.

## Shared native grader

`check-engine` is compiled from [check-engine.rs](check-engine.rs), linked to the real application `learning::grade_field`, and uses memory-only fixtures. It supports radio, select, checkbox, and blank fields, including multiple fields and math/text/image answer types.

Run:

```sh
generate/runs/current/check-engine INPUT.json REPORT.json
```

Input is an array of objects with `label`, `record` (generator record containing knowledge_point/question/generation), and `checks`. Each check has `field_index` (default zero), `expected` (`accepted`, `rejected`, or explicitly documented `unresolved`), and `purpose`. For choice fields set `submitted_answer_id` to an owned answer UUID; the harness maps it to fixture IDs before actual grading. For blanks set `submitted` to the learner's expression/text, testing canonical values, equivalent supported forms, and wrong answers. All expected and actual results must match or the tool fails. Radio ID grading does not validate displayed choice mathematics or source fidelity; those require independent checks.

Legacy trig validator inputs using `submitted: "100"` etc. remain supported for the first field. UUID submissions are preferred for multiple fields. Engine source files may be under concurrent development; record hashes/build provenance for the library used. This helper performs no EDB reads or writes. Do not treat arbitrary grader errors as successful tests by labeling them unresolved; document substantive restrictions and repair supported generator formats when possible.
