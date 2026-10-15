# General-base affine exponent integration, private draft

Script: ../17592186096656-draft.py. This is a local basis2275 replacement candidate; registered ../17592186096656.py and its entire evidence/cache tree are preserved byte-for-byte. No registration, database, shared engine, or queue edits occur.

Run from repository root:

```sh
.venv/bin/python generate/scratch/17592186096656-draft/validate.py
.venv/bin/python generate/scratch/17592186096656-draft.py --difficulty all --count 2 --seed 42 --format markdown
```

Public API: generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None), generate_easy/moderate/hard, batch. Source templates are the MA IDs in source-cases.json and accept exactly {"n":integer}; choose profile="observed_raw" for faithful ineligible evidence or "method" for normal source-shaped work. Raw missing attributes stay omitted. Expanded template="affine" accepts a,k,b,n and (for definite levels) L,H. All parameter and workload guards apply to explicit inputs. Profiles are selected before construction; default sampling covers all supported source-shaped families and expanded affine work. JSON is local review data.

Fidelity and math are separate from native grading. Raw round wording rejects valid equivalent forms; other native equivalence limits are measured in native evidence and never drive parameter exclusion. Radio owned identities, invalid IDs and mathematical text are tested separately. See validation.json, native-summary.json, review.md, and classification.md for exact counts and limitations. The private formatter/parser are explicitly loaded by file path; native check-engine binary/source and hashes are frozen here. Runtime never imports the registered generator, its evidence, or live question_capture.
