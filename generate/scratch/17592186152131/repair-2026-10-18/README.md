# Radicals as Fractional Exponents: repaired and published

Topic `17592186049089`; repaired KP `17592186152131`, **Converting a Radical to
a Unit Fraction Exponent**. Version **1.3.1** passed all eight independent review
checks and was published with five new easy questions at basis **4363**. Live
inventory at basis **4364** confirms the registration and question counts.

| KP | Title | Usable questions | Generator |
| --- | --- | ---: | --- |
| 17592186152128 | Converting a Fractional Exponent to a Radical | 7 | Existing, usable |
| 17592186152129 | Converting a Radical to a Fractional Exponent | 9 | Existing, usable |
| 17592186152130 | Converting a Unit Fraction Exponent to a Radical | 7 | Existing, usable |
| 17592186152131 | Converting a Radical to a Unit Fraction Exponent | 7 | Repaired and published |

Only the last KP lacked a registered generator and had a lesson shortage: two
usable questions against a minimum of five. All four now meet that minimum.

## What changed

The rejected indexed-root bank included a distinctive `1^(x/n)` distractor.
Reading x and n from that option revealed the correct `x^(1/n)` choice without
reading the radical. Indexed practice now draws two eligible bases and two root
indices, offers all four unit-fraction combinations, and chooses the prompt
from those four targets. The fifth source-style unit-base foil is independent
of the target. Identical complete banks support four different correct keys.
Exact checks exclude equal-valued options.

Independent review also found a sampling bias in the retained square-root
branch. Choosing x<n / x=n / x>n before choosing the radicand overrepresented
x=2. An answer-only strategy selecting base 2 in the {2,3} bank scored 127/136
in independent trials. Square practice now draws the complete bank before
uniformly selecting either unused target. First-square conditional probability
is exactly 1/2; the review's new trials yielded 15/29 for the former shortcut.

Both changes preserve one-step radical-to-unit-fraction conversion, the radio
response contract and source solution stages. Easy is the sole justified and
approved difficulty. Original source banks remain available for explicit source
replay; ordinary practice uses the repaired banks. The original incomplete
source question remains incomplete in the database and is excluded from the
usable count.

## Verification and evidence

- Author checks: 28,240 indexed bank/foil/target cases, 336 square configurations,
  1,008 full-capacity seeded records, deterministic replay, declared-file
  relocation and capacity boundaries all pass exact arithmetic checks.
- Targeted sampler regression: 2,560 five-item batches / 12,800 records; within
  {2,3}, first-square targets were 49 versus 52, and all positions 92 versus 102.
- Captured-inventory filtering retains all 1,765 complete indexed banks, all
  168 square-bank pairs and all 126 semantic tasks.
- Independent review: source fidelity, mathematics, variety, scope, grading,
  rendering, packaging and decision variation all pass. Its native grader
  checks 39,005 submissions with none unresolved; all 18 actual-UI previews pass.
- Standard publication preview, exact-request commit and readback verify five
  new questions and the registered package. The receipt also verifies that
  learner/engine facts and existing question content were preserved.

See [final-report.json](final-report.json), [live-verification.json](live-verification.json),
[author validation](validation/final-author-report.json), and
[pipeline/job.json](pipeline/job.json). The job links the accepted independent
review and exact publication receipt. The first review and runtime are preserved
as history; their rejection led to the sampling correction.

Published package:
`generators/7b/7b5bac4709e2f880cfe064b51fb60cbe5a087fa7e4461aa77f7c7eafdb1b367e/generator.py`.
Its policy-2 easy approval is recorded under the same package hash in the live
math store. Generator code is in `workspace/generator.py`; immutable published
runtime files are declared by `workspace/package.json`.

The repair-specific runner uses the existing learner KP lock and coordinates
preparation with the application's API lock, avoiding the observed stale-basis
races. Source checks, basis guards and exact-request recovery remain enabled.
No shared publisher implementation or application service was changed.

Reproduce author checks with the project's Python:

```bash
.venv/bin/python generate/scratch/17592186152131/repair-2026-10-18/workspace/indexed_repair_checks.py
.venv/bin/python generate/scratch/17592186152131/repair-2026-10-18/workspace/square_sampler_checks.py
```

A finite audit does not prove the absence of every shortcut. Delivery evidence
uses a captured inventory; future learner history can remove candidates. The
published package is certified for easy questions only.
