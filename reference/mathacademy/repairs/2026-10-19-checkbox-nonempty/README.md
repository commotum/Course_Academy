# Checkbox selection policy and line-definition spacing

Committed and verified in `math` at basis **5054**. Exact transaction, preview,
stable request, receipt and before/after reads are retained here.

## Reported questions

- `17592186561248`: the line definitions used four alignment columns, leaving
  padding between a short left side and its equals sign. Complete equations now
  occupy one natural-width column beside their aligned labels. The same
  spacing-only correction was applied to all 23 questions in that KP's pool and
  its registered generator. Parameters, solutions, answer keys and responses
  retain their values. `formatting/ui/` contains the rendered comparison.
- `17592186272199` is original Math Academy `q-141084`. Its three false keys are
  mathematically correct: the derivative of `-1/x^2` is `2/x^3`, and it does not
  satisfy `y'=y/x^2` on the stated domain. Its original None answer became an
  empty checkbox subset during migration. Its content and recorded response
  are preserved; the fresh-practice filter now excludes it.

## Complete registration audit

The basis-5048 registry contained 631 generators. Reading declared code found
50 checkbox-capable candidates. Cross-checking all 10,081 checkbox fields and
their 3,231 owning questions identified 12 additional registered KPs whose
field types may be inherited from source data. All 62 registrations are covered.
Some inherited-source candidates currently emit radio/blank questions or
evidence-only checkbox replays; the policy also guards future learner-facing
checkbox output through those entrypoints.

Ordinary pre-policy samples from 16 of the first 50 candidates produced empty
subsets. Further explicit/finite-template checks found a Bernoulli family
(`q-108916`) that always has no correct option, and empty variants in the rank
inspection catalog. Those families/cases are excluded from learner generation.
The ODE generator's empty derivative/solution decision branch is excluded both
from normal sampling and its finite batch buckets. The scripted-set membership
sampler now chooses a nonzero membership mask before constructing numbers.

## Enforcement

- `scripts/generator_policy.py` guards public generated records and batches.
  Valid calls retain their question data; empty seeded instances are resampled
  deterministically. Explicit mathematical inputs are rejected instead of
  silently changed. Large batches replace empty slots individually. Attempts
  are bounded, and historical evidence-only output remains distinct.
- All 62 identified generators use this guard: 39 active legacy repository
  scripts and 23 new immutable package revisions. Each new package bundles and
  declares the same standalone helper. A further immutable revision fixes the
  labelled-line layout, making 24 package registrations in the transaction.
- `scripts/generator_publish.py` independently rejects empty correct checkbox
  subsets before publication.
- `engine/rust/learning.rs::validate_practice_question` independently excludes
  them from fresh lesson/review/assessment selection. General validation and
  grading retain historical empty-subset semantics. The existing 126 all-false
  checkbox questions (104 with Math Academy source IDs) remain in their pools
  for history and ownership, while becoming ineligible for fresh practice.
- `generate/docs/6-template-generator.md` records the new authoring rule.

The live learner workers are already running the exact tested binary with the
fresh-practice guard. `deployment-verification.json` verifies its bytes and
active workers; no service restart was required.

## Verification

- 2,942 ordinary generated records, 67 special/catalog/explicit-case records,
  and 36 final ODE records: **3,045 checked records**, no empty learner subsets.
- Nonstandard CLIs and finite-capacity cases are covered by
  `special-audit.json`; unsupported difficulty requests and earlier failed
  audit attempts remain recorded rather than being mistaken for supported
  generated output. Explicit empty ODE inputs and the invariant Bernoulli
  family are rejected.
- **111** representative examples passed the current native learner grader,
  including distractor rejection. Revised line-definition generations preserve
  parameters and outcomes across all three levels; the actual learner UI
  rendered the original/corrected comparison without errors.
- **163** engine unit tests, **26** publication tests, **6** policy tests,
  **5** delivery tests and **35** pipeline tests passed. The engine regression
  confirms an old all-false response still grades correctly while fresh
  selection rejects that question.
- Exact CAS guards and native question validation protected the database
  write. Every receipt datom and complete question readback were verified;
  question answer keys and learner records were unchanged.

Start with `verification.json`, `quality-verification.json`,
`deployment-verification.json`, `package-updates.json` and
`patched-generators.json`. Original legacy script bytes are retained under
`legacy-before/`; original immutable packages are retained under
`original-packages/`. Do not regenerate a saved request to recover an already
committed submission.
