# Circle arc generator (local review)

Run from the repository root:

```sh
.venv/bin/python generate/scratch/17592186087784/validate.py
.venv/bin/python generate/scratch/17592186087784.py --difficulty all --seed 40 --count 2 --format markdown
```

API: `generate(level, seed=0, template=None, field_type=None, parameters=None, profile=None)` and the three level wrappers. `field_type` is `radio` or `blank`; parameters are r,h,k integers and start/end rational multiples of π. Explicit invalid inputs fail. `observed-q-<ID>` profiles preserve complete original banks at their eligible arc; default profiles are clearly authored half-arc/full/complement banks. All generated parameter-dependent graphics use Matplotlib and write only here.

15 originals, 11 presentation templates, 11 radio profiles, 4 two-blank questions. q-79205 has an independently derived correct-reference repair and authored moderate label/solution, separated from fidelity counts. All three observed levels have same-method angular variations. Raw capture, whole-bank ledger, extraction stages, plot inventory, native grader checks, review records and validation results are included. Nothing is registered or written to EDB. The native grader harness operates on memory-only fixtures.

Final checks: 15/15 source prompts, 14/14 available worked solutions, 11/11 complete radio banks (55/55 options), 8/8 blank fragments, and 18/18 available correct field designations matched. One missing designation/solution is explicitly repaired, not counted as matched. Independent math covers 52 records; 2,200 sampler instances cover all declared angular families. Native grader: 73 accepted, 124 rejected, 0 unresolved across 37 fixtures. Visual QA covers 31 originals and 44 authored plots, with the coincident 0/2π label defect corrected before delivery.
