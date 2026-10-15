# Generator and validation contract (doc6)

The owned public script is ../17592186092264-draft.py. The registered numeric script and its entire evidence/cache tree are outside the owned draft. baseline.json captures their 91 absolute file paths and SHA256 hashes before imports. Validation compares both the exact file set and contents; imports set sys.dont_write_bytecode=True. No DB, manifest, registry, engine or git mutations occur.

Public APIs: generate(level, seed=..., template=..., parameters=..., source_id=..., bank_profile=...), generate_easy, generate_moderate, generate_hard, batch and source_case. Raw replay is a separate ineligible raw_replay(source_id) API; its original record is exact, including missing attributes. Normal source_case output minimally completes or corrects defects, explicitly attributed in generation.authored_changes. Parameters are finite, typed integer slots; source original values are included. Complete profile selection precedes parameter sampling. All bank options are derived together, with whole-bank rejection on collisions. In-memory memoization caches the same exact instance after mathematical validation; it does not change profile selection or store external files.

The public generator imports only its private frozen math_format.py through an explicit module spec. It applies normalize_prose and normalize_tex before question/field/answer IDs, and checked_math_content at the public return boundary. Its mathematical work uses exact SymPy rationals, real unrestricted x, and the actual log-argument inequality U(x)>0. There are no live capture dependencies. The parser and validator also live in this private tree, using explicit imports.

The independent math_parser.py never imports generator expressions. It reads the actual printed prompt function and supplied point, solves the original domain before simplification, verifies every formal derivative's operand, composite assignment, outer derivative, inner derivative, separate chain product factors, actual combined numerator/denominator, cancellation operands and ordered stages, evaluation targets and supplied point-slope substitutions. Full tangent equations are compared through whole line residuals, and the point must actually lie on the curve. It independently reconstructs each complete bank from the printed function/point. Blank expected fragments are interpreted in their full surrounding prompt. Shared prose's repeated function, point, abscissa and slope references are checked.

validate.py reproduces source prompts/banks/keys/prose/ordered operations separately from correctness, tests all eligible declared slot values and preserves profile-driven exclusions, verifies seed-independent actual-task identity and deterministic content, and exercises 60 distinct actual tasks at each level. Source/correctness tests are distinct from grading tests. Mutations cover wrong formal derivative operands, stale inner coefficients, erased true intermediate equalities, changed banks and stale evaluation targets. Explicit domain checks exercise both branches of ln(x⁴), odd-power positivity and the excluded x=0 hole, while review cases retain a valid zero slope and unit scale.

Actual application grading uses only the SHA-pinned generate/runs/current/check-engine (71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea), in independent one-record batches. Every observed/authored original and two changed review cases are checked. Radio tests submit every field-owned answer ID; unknown numeric and malformed IDs are separate ownership/syntax fixtures expected to return the engine's unresolved errors. Blank tests submit canonical TeX, a true doubled-numerator/denominator equivalent, and a wrong plus-one value. Any genuine equivalence gap is recorded without changing the question, pruning valid mathematics or modifying the engine.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186092264-draft/validate.py
.venv/bin/python generate/scratch/17592186092264-draft.py --difficulty easy --count 5 --seed 47 --format markdown
```

The source tables, per-case JSON, Markdown review, slot coverage, mutation report, native fixtures/reports, final validation and frozen hashes form the reviewable artifact. This is a local draft, pending the parent's independent review; there is no registration or serving change.
