# Applied repairs: four trigonometry lessons

The thirteen KP generators in lessons **17592186048319, 17592186049773,
17592186048703 and 17592186048362** have been repaired and registered. Three
**gpt-6.1-sol agents at high reasoning effort** worked on the sum/difference,
sine double-angle and cosine double-angle packages; root independently checked
their output, requested further fixes, and applied the database changes.

## What changed

The learner now supplies the relevant identity, method and intermediate work.
Formula reminders and prescribed substitutions were removed from independent
practice. Numerical angle decompositions remain where the target KP's imported
questions actually supply them. The cosine exact-value generator therefore
retains supplied decompositions; the sine generator retains its genuinely
imported unhinted hard family.

Harder questions preserve the core operation. The repairs remove reverse-identity
wrappers, two unrelated shifted expansions, hidden quartics, full-turn shifts,
and accidental phase collapse. Source-supported expanded squares and reciprocal
factoring remain. Bands without imported anchors are documented as conservative
authored continuations, rather than claiming calibration from generated examples.
Actual imported references replace inherited generated-prototype references.

Visible unit multipliers are omitted without banning legitimate values of one.
Known original-angle cosine bypasses are excluded. Repeated-double-angle
products and reciprocal quotients must require both applications: a familiar
intermediate angle cannot bypass the second. Source-supported cosecant
cancellation remains a deliberate distinct family. Awkward nested fractional
coefficients, fractional-degree notation and unnecessary three-place decimal
angles were also removed from the affected output.

## Applied pool changes

At final live verification basis **12998**, all thirteen registrations point to
the repaired immutable packages. **162 superseded generated records are retired
from future practice**. This includes four mathematically correct but
pedagogically weak cases caught by the final repeated-angle purpose check.
The active generated pool contains **92 fresh records and two independently
verified existing matches**. Imported questions, canonical examples, observed
imported level coverage, original question/field/answer identities, keys, and
saved learner history are preserved. Retirement does not detach bank membership.

Inventory is deliberately bounded. Sine-radian shifts have four easy records;
an equivalent existing case retains its moderate rating. Repeated-double-angle
practice has three easy records; its fourth sound mathematical case already
exists as imported moderate practice. Other KP/band cells have at least five
complete active records. Neither a duplicate nor a relabeling was introduced to
satisfy an arbitrary stock quota. Exact inventories are in `completion.json`.

## Prevention and verification

`generate/trig_question_pedagogy.py` is enforced by publication and contains
regressions for the demonstrated failures, including the intermediate-angle
bypass. It inspects visible questions rather than trusting generation metadata.
It is a focused guard, not a general mathematical or pedagogical classifier.

The repeated-angle package also declares its four-case easy limit in the hashed
runtime file `generation-limits.json`. The pipeline repair honors declared
finite batch capacities in primary, refill and secondary verification, while
recording requested and actual counts. This resolves the conflict between the
author instructions to preserve finite families and the runner's former minimum
of five verification records. Unlimited families keep their existing behavior.

Independent checks cover **349 final-version CLI records and 5,301 worked-solution
numeric equality witnesses**, using displayed TeX rather than answer recipes.
All sampled keys and wrong alternatives were checked. Initial desktop/phone
previews cover all thirteen KPs and three bands, with the changed repeated-angle
cases rendered again after refinement. **390 final live grading checks pass**,
including wrong responses and representative retired saved questions. The live
verification endpoint creates no learner attempts. Numeric witnesses supplement
the instructional and algebraic review; they are not general symbolic proofs.
Root's combined publication/purpose/finite-capacity suite passes **61 tests**;
the agent also ran **84 existing pipeline, all-band, approval and recovery tests**.
The previously flagged questions 17592186715337, 17592186714557 and
17592186702810 are retired. Final active inventory contains **252 complete
questions**, with the 28 partial imports preserved separately.

Evidence and durable request receipts:

- `pool-review.json`: independent initial samples, runtime hashes and allocation.
- `repeated-angle-refinement/`: final purpose regression, 24 final-version
  records, two rendered replacements, atomic retirement/publication and readback.
- `finite-capacity-registration/`: metadata-only registration preserving questions.
- `publication/<kp>/`: exact requests, stale-request recovery, receipts and readback.
- `verification.json`, `completion.json`: consolidated current registrations,
  retirement, active fresh inventory and native grading.
- `validation-summary.json`: final check totals and executed commands.
- `generate/repairs/2026-11-04-four-trig-lessons/`: instructional accounts,
  actual source anchors, portable runtime closures and executable agent checks.

The separate defects in imported questions identified in
`reference/edb-math/audits/2026-11-04-four-trig-lessons/README.md` remain recorded
there. This task repairs generators and generated stock; it does not silently
rewrite imported keys or worked solutions.
