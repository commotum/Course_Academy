# Other exponential products: private draft

KP 17592186184350, immutable `math` basis 2275, lineage
`01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1`. This draft is unregistered. The
registered numeric script and every preexisting evidence file are protected by
the byte/path manifest in `baseline.json`; validation checks them before and
after execution. No database operations, shared engine changes, or registration.

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186184350-draft/validate.py
.venv/bin/python generate/scratch/17592186184350-draft.py --difficulty all --count 2 --seed 7 --format markdown
```

The import API is `generate(level, seed=0, template=None, field_type=None,
parameters=None, profile=None)`, plus the three difficulty entrypoints and
`batch`. Explicit parameters require exactly the keys in `DOMAINS[template]`;
observed replay requires only `{"base": original_base}`. Booleans, unknown
keys, unsupported field types, levels, templates, profiles and out-of-domain
values fail rather than being silently repaired.

`profile="observed"` or `"observed-q-…"` publicly replays an entire original
MA bank under an integer base change. These profiles are explicitly
`evidence_only=true`, `eligible_for_learning=false`: transported expression
structure does not recover historical misconception intent. The default
`method-derived` profile has one complete authored bank derived from the
actual chain ratio and logarithm operation, using the source family and fixed
worked solution. The original banks stay available without entering defaults.

Eight original MA records are covered, including raw q-73800, whose difficulty,
worked solution and correct designation remain absent. Its separate normal
completion is authored and mathematically/natively checked. Four independent
inventory records are copied completely into `independent-inventory.json` with
the original wrapper provenance; they do not count as original MA templates or
new difficulty evidence. Hard is an authored negative-quartic workload anchored
to canonical e-14403, not an observed hard label.

The formatter, strict elementary parser, native grader binary and grader source
are frozen privately. Runtime never imports live `question_capture` helpers,
the registered generator or shared QA. Exact source prose and all ordered stages
are checked independently of banks; every generated primitive and integral row
is differentiated from the actual displayed text. Complete banks are checked
modulo additive integration constants and are real on all real x. Prime-base
task fingerprints collapse equivalent assessed integrands across templates,
profiles, base powers and denominator spelling. Content IDs separately include
the actual prompt, solution, difficulty and complete bank, and ignore seed/order.

Native grading tests each owned radio ID individually. Math text, foreign IDs
and malformed IDs deliberately yield the native structured contract errors;
the harness calls these `unresolved`. They are reported separately from actual
owned-answer grading failures and from mathematical equivalence. There are no
blank fields or blank-equivalence claims. Raw q-73800 cannot be natively graded
without fabricating a key, so only its separate normal completion is graded.
