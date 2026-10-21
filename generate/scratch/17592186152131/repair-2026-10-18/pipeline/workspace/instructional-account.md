# Radicals as Fractional Exponents: generator repair, 2026-10-18

Topic `17592186049089` has four KPs. The initial live inventory at basis 4301
showed usable generators and 7, 9 and 7 available questions respectively for:

- `17592186152128`: Converting a Fractional Exponent to a Radical.
- `17592186152129`: Converting a Radical to a Fractional Exponent.
- `17592186152130`: Converting a Unit Fraction Exponent to a Radical.

Only `17592186152131`, Converting a Radical to a Unit Fraction Exponent, lacked
a registered generator. Its two usable questions fell three short of the lesson
minimum. A fresh source and delivery inventory were captured at basis 4319 in
`current-source/`.

## Defect and repair

The failed automatic build's indexed-root answer bank contained a distinctive
`1^(x/n)` distractor. A learner could read x and n from that option and choose
`x^(1/n)` without looking at the radical. The previous independent review
reproduced this for every indexed item tested. The arithmetic was correct; the
choice design leaked the answer. Existing successful square-root repairs are
retained.

Version 1.3.1 uses an explicitly authored indexed practice bank with two bases
and two indices. All four base/index combinations are eligible prompt targets,
and all four corresponding unit-fraction powers are offered. A fifth source-style
base-1 distractor samples its numerator and denominator independently of the
target. Holding the entire bank fixed while changing the prompt produces four
different correct choices. Exact checks exclude banks with equal-valued choices.
This preserves the tutorial's one-step operation: copy the radicand as the base
and put the root index in the denominator. It adds no evaluation or exponent-law
steps, so easy remains the sole supported band.

Original question banks are preserved only in explicit `source_replay()`;
ordinary sampling never emits those leaky legacy banks. Replay preserves all
three supplied source banks and fifteen choices, including the source question
whose missing key, solution and difficulty must be inferred rather than claimed
as captured. No original questions or learner history are edited.

## Validation

Run `.venv/bin/python generate/scratch/17592186152131/repair-2026-10-18/workspace/indexed_repair_checks.py`.
The script checks every eligible indexed bank, each of four independent foil
assignments and all four prompt targets, using an exact rational-power reader
of the served prompts, choices and solutions. It also checks all 336 retained
square configurations, source replay, capacity boundaries, full-capacity seeded
batches, determinism, and relocation with only declared runtime files.

`validation/` retains sampled records, original-shortcut success rates, native
grader input/results, read-only delivery filtering and actual-UI screenshots.
The old `workspace/evidence/` and square-repair scripts are historical evidence;
`indexed_repair_checks.py` is the current combined check.

The five-choice blind baseline is 20%. Eliminating base 1 mathematically leaves
four plausible unit-fraction choices; the formerly perfect indexed shortcut must
score 25% across complete target groups, including within template, base and
root-index subgroups. This finite check does not claim to exclude every possible
strategy. Live publication requires independent review under policy 2.

Completed author checks: all 28,240 indexed counterfactual records, 336 square
configurations and 1,008 seeded records pass independent exact arithmetic.
The real grader passes 42,195 raw/source/control submissions and 40,583
post-delivery submissions, with no unresolved results. Delivery deduplicates
8,404 records to 8,116 while retaining all 1,765 complete indexed banks, 168
complete square-bank pairs and 126 semantic instances. All ten actual-UI
previews pass; screenshots 1, 4, 5, 8 and 9 were visually inspected. The staged
five-question publication batch has no duplicates against basis 4319.

`validation/final-author-report.json` records these separate claims. The
standard pipeline job is staged at `validate`, with no reviewer acceptance or
publication claimed. The earlier 1.3.0 candidate hash (before the sampling correction) is
`bda8b394095519e4d595c32d26e3eee13ec5a1e7c7cff367d09aa6fbe52c6ab4`.
Once a separate reviewer is explicitly authorized, resume with:

```bash
.venv/bin/python generate/scratch/17592186152131/repair-2026-10-18/run_pipeline.py --review-and-publish
```

This takes the same shared KP lock as the existing builders and uses the
standard independent reviewer, preparation, preview, commit, readback and
approval path. A failed review stops for repair; it does not publish or launch
another author automatically. The original rejected job is preserved.

## Independent review correction: square-root sampling

The first independent review of 1.3.0 found an additional bias in the retained
square sampler: choosing the x<n / x=n / x>n category first made x=2 much more
likely than x=3 within the recognizable {2,3} choice bank. The first-square
conditional preference was exactly 34/37, despite both targets being supported.
This is a sampling defect rather than a mathematical error.

Version 1.3.1 draws a neighboring base pair, foil index and inverted-power base
before uniformly choosing either unused prompt target. The first-square
conditional probability is now exactly 1/2. `square_sampler_checks.py` tests
2,560 fresh batches / 12,800 records: within the {2,3} pair, first-square targets
are 2 in 49 cases and 3 in 52; across all batch positions, 92 versus 102. Every
eligible pair supports both observed targets. Later positions respect exclusion
of already-used semantic tasks; no exact empirical balance is claimed.

The independent review evidence and the original runtime remain preserved under
`pipeline/`. This correction changes sampling only; source banks, prompts,
solutions, five-choice contract and easy-only scope remain intact. The root
validation directory contains the repeated arithmetic, capacity, deterministic,
relocation, native grader and delivery checks for the revised code.

Current manually repaired version 1.3.1 package hash: `7b5bac4709e2f880cfe064b51fb60cbe5a087fa7e4461aa77f7c7eafdb1b367e`.
The repeated delivery audit retains 8,111 records (293 duplicates removed),
all 1,765 indexed banks and 168 square pairs. Native post-delivery checks:
8,111 accepted and 32,447 rejected, with none unresolved.
