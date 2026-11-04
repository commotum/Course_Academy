# Critical audit of four trigonometry lessons

The failures are systematic, but the lessons should not all be rebuilt indiscriminately. The strongest pattern is that missing source difficulty bands were filled by changing the student's task: easy supplies the method, while hard adds an extra problem. Other generators preserve the imported progression quite well. Mathematical correctness and technical validation have not reliably distinguished these cases.

This was a read-only audit at **math T12673** of all four requested topics: 13 KPs and registered generator packages, **346 practice questions** (186 imported, 160 generated), 13 imported canonical examples, and 9 tutorial sections. The question-by-question review covers all 359 questions/examples, their available worked solutions, response fields, choices and keys. No questions, registrations, learner history or services were changed.

The complete per-question review is in [question-review.json](question-review.json); [question-ledger.json](question-ledger.json) retains the text, keys and solutions. [kp-review.json](kp-review.json) and [findings.json](findings.json) bind the conclusions below to exact entities. Canonical examples normally have no response fields; that is not a defect. Twenty-eight practice imports have incomplete response keys, and fourteen lack worked solutions. They remain partial source evidence, not invented completions or generator failures. No retired or structurally contained multipart question was used as a standalone anchor.

## What the student is being asked to do

An ordinary question should still require the target identity, choice of representation, substitutions and sign decisions. Simpler arithmetic can make that task easy without giving it away. Conversely, a hard question should place a controlled demand on that same skill, or have an explicitly justified extension. Adding algebra, reversing an identity and then applying it again, or making the learner discover a decomposition that all source examples provide is not automatically a calibrated hard band.

Scaffolding must be judged by its role. An angle decomposition in the exact-value sum/difference KPs is supported by their imported prompts: the learner still selects and applies the identity. A prompt that supplies that identity, the special-angle values, and the order of substitutions gives away the assessed decisions. The tutorial appropriately shows these steps; that does not establish that independent practice should print them.

There are two particularly strong patterns across the 13 KPs:

- **All three KPs with no imported easy examples** generated easy questions by adding procedural help. There are **19 such stored easy questions**: five cosine-radian shifts, nine sine-radian shifts, and five repeated sine-double-angle questions.
- **All six KPs with no imported hard examples** introduced new hard structures. Four families substantially alter or compound the task; two factoring extensions are plausible but uncalibrated and deserve a reasoned review rather than an automatic ban.

Missing source levels require judgment. They do not require inventing a different procedure at each label. The current author prompt already explicitly says this; more prompt prose alone will not repair the registered packages or existing question pools.

## Review of every KP and generator

The counts below are imported/generated practice counts; canonical examples are additional. “No hard import” and “no easy import” refer to this KP, not an unrelated lesson.

| Lesson / KP | Imported / generated | Assessment and required action |
| --- | ---: | --- |
| **Cosine sum/difference — 17592186048319** | **51 / 37** | All three generators have a band requiring attention. |
| 17592186059665 — Radian shifts | 18 / 12 | Easy supplies both identity and exact values; no easy import does this. Remove that help from ordinary practice. Moderate axis shifts and hard non-axis shifts are broadly source-aligned. Reduce full-turn and variable-renaming repeats. Examples: 17592186714557, 17592186714906. |
| 17592186059666 — Exact values | 16 / 13 | Keep the source-supported decompositions in easy/moderate. Hard adds reverse identity recognition, removes the decomposition, then applies an identity a second time. No hard import establishes this synthesis task. Example: 17592186715337; compare imported 17592186233854, which reaches the same exact value through a supplied split of 75 degrees. |
| 17592186059821 — Degree shifts | 17 / 12 | Easy axis shifts and moderate single non-axis shifts are appropriate. Hard invents weighted pairs of expansions and coefficient collection despite no hard imports. Some sampled pairs are coterminal/antipodal and collapse to one shift. Example: 17592186715695. A moderate response frame, 17592186715668, unnecessarily requires a negative entry after a printed minus. |
| **Sine sum/difference — 17592186049773** | **39 / 46** | One largely aligned generator, one overscaffolded easy band, one inflated hard band. |
| 17592186059662 — Degree shifts | 15 / 14 | Easy/moderate preserve the source task. Hard combines two expansions and can require collection of unrelated radicals without a hard imported anchor. Its hard source metadata includes generated prototype 17592186701660. Moderate 17592186701793 adds double-negative response bookkeeping. |
| 17592186059663 — Exact values | 8 / 16 | **Mostly sound.** Unlike the cosine counterpart, this KP has an imported hard question, 17592186253530, asking for sin(75 degrees) without a decomposition. The generated hard family preserves that one-forward-identity task. Keep source-supported splits in easy/moderate. Unit choice alone should not be treated as proof of difficulty. |
| 17592186059820 — Radian shifts | 16 / 16 | Easy supplies the identity and both values, though its cited imported support is moderate independent practice. Remove that assistance; retain manageable axis angles. Moderate and non-axis hard are broadly aligned. There are several variable-renaming duplicates and an imported worked-solution angle error. |
| **Sine double angle — 17592186048362** | **54 / 43** | Two strong generators; one over-guided easy band and a coverage gap; one hard extension needing review. |
| 17592186059671 — Products | 10 / 15 | Direct easy practice preserves the target. Two moderate prompts tell the learner to use the sine of twice the angle, narrowing method selection more than the generic source prompts. Quartic hard hides the product behind factoring and the Pythagorean identity. This is a plausible transfer extension, but there are no hard imported anchors; calibrate it explicitly instead of accepting its label from a generated predecessor. |
| 17592186059672 — Multiple applications | 15 / 12 | Easy prints the identity and says exactly which angle to substitute first and second, removing the central recognition task. Example: 17592186696011. The moderate sampler also drops the reciprocal-cancellation family represented by five of six moderate imports; its constructor supports that family, but normal generation never schedules it. Source-supported reciprocal hard families should be retained. |
| 17592186059673 — Ratios | 15 / 9 | **Strong alignment.** Learners must independently choose the double-angle rewrite, reciprocal/quotient rewrite and cancellation. Hard factoring is actually present in imported questions, such as 17592186253633. Keep it. A source easy cotangent quotient is generated as moderate, so ratings overlap and deserve calibration, but this is not wholesale task drift. |
| 17592186059674 — Exact values | 14 / 7 | **Mostly sound.** Product, binomial-square and reciprocal-denominator families have imported support. Guidance stays in the solution. Simple numbers or a unit coefficient are not defects. Repair the sign typo in the conclusion of partial import 17592186233281 separately. |
| **Cosine double angle — 17592186048703** | **42 / 34** | Basic bands are useful; unsupported hard extensions and source-bank defects need attention. |
| 17592186087669 — Basic difference form | 12 / 16 | Easy direct recognition and moderate common-factor extraction match imports. Quartic hard adds difference-of-squares/Pythagorean work without a hard imported anchor: review as an extension. The bank-first construction also creates geometric angle ladders and clustered variants. Two imported answer banks are genuinely ambiguous. |
| 17592186087670 — Alternative forms | 15 / 12 | Easy and moderate preserve recognition of the alternative forms, with common-factor extraction. Hard invents quartic regrouping and a second double-angle application, citing generated prototype 17592186698910. That is a substantial uncalibrated change. One imported bank has a valid single-cosine option marked wrong; another has equal-valued choices whose acceptability depends on the requested response form. |
| 17592186087671 — Exact values | 15 / 6 | **Mostly source-aligned.** Its expanded-perfect-square hard family is genuinely imported. However, the only stored generated hard item, 17592186702810, uses 135 degrees: both squared values are known halves, so the answer can be obtained directly without the target double-angle identity. An imported hard example at pi/4 has the same weakness. Preserve the good family and guard its non-diagnostic cases. |

## Concrete failures that matter to learners

**Over-guided easy questions.** In 17592186696011, the prompt says to use the identity first at pi/16 and then at pi/8. Recognizing that the first transformation creates another matching sine-cosine pair is the entire “multiple times” skill. The question gives away that sequence. The analogous radian-shift easy questions supply both the identity and the values, reducing the task to substituting into a printed recipe.

**Manufactured hard questions.** In 17592186715337 the learner must reverse a sum formula, combine angles, invent a split, and expand again. The imported exact-value tasks supply the split and require one forward application. In the alternative-cosine hard family, expressions such as 8 cos^4(t) - 8 cos^2(t) + 1 require recognizing a hidden quadratic square and applying the identity twice; no hard import in that KP establishes this demand.

**Hard in print, ordinary after simplification.** Question 17592186715695 uses cos(x - 300 degrees) - 2 cos(x + 60 degrees). Those two shifted cosines are the same function, so it reduces to one negative shifted cosine. Three of ten sampled hard outputs from this generator have equivalent or antipodal phases. Counting two printed expansions as hard misses the effective task.

**Artificial response-sign work.** Nine imported coefficient-entry prompts print a minus between their fields, and none requires a negative second entry after that minus. Two generated prompts do: 17592186715668 and 17592186701793. They are mathematically consistent, but add double-negative bookkeeping rather than a trig decision. This should not be added merely to vary an output frame.

**Repetition presented as variety.** Examples include 17592186714557 versus 17592186714906, and 17592186701792 / 17592186705180 / 17592186705223. Their displayed mathematical inputs coincide after renaming the variable, with the same band and response demand. Different wording, variables or distractor order should not count as fresh mathematical coverage. Four such clusters are retained in renaming-only-clusters.json.

**Replay support that normal sampling never uses.** The multiple-applications generator has a cancellation constructor, but its moderate generate() path schedules only the three-factor product. Five of six imported moderate examples use a doubled sine with a reciprocal cancellation; all six stored generated moderate questions use the product family. Its hard sampler also restricts itself to the secant quotient families, while two imported hard cases use a plain product. Those source labels should be reviewed against their actual workload rather than copied unquestioningly, but the omitted family still needs explicit coverage or a documented reclassification. Replaying a source family does not establish that normal generation covers it.

## Imported material also needs critical review

The imported questions are evidence of task structure, not infallible authority.

Three radio banks offer another mathematically valid single-cosine answer and grade it incorrect. Each case was checked using the read-only live preview grader:

| Question | Stored correct option | Another offered, valid option |
| --- | --- | --- |
| 17592186088094 | cos(3pi/2) | cos(5pi/2), also zero |
| 17592186290550 | cos(6pi/5) | cos(4pi/5), exactly equal |
| 17592186598566 | cos(8pi/5) | cos(2pi/5), exactly equal |

These alternatives satisfy the stated single-ratio response form. That differs from 17592186345265, where cos^2(90 degrees) and 2 cos^2(90 degrees) also have value zero but do not plainly satisfy “a single trigonometric ratio.” That fourth case is a response-contract question, not the same unambiguous two-correct-options defect.

Two imported worked solutions contain false equalities:

- **17592186233281:** the prompt and derivation use (sin 165 degrees - cos 165 degrees)^2, correctly reaching 3/2. The final line changes the minus to a plus, while keeping 3/2. The plus expression actually equals 1/2. This record has an incomplete response key and was treated as partial evidence.
- **17592186272322:** the question asks for sin(x + 4pi/3), but the first solution line writes sin(x + pi/6) before expanding the 4pi/3 expression. The final answer corresponds to the intended question; that intermediate equality is false.

There are also **16 notation fields across 9 imported questions and one tutorial** with residual bare powered function names such as {cos}^2 or {sin}^2. Six are question stems. The UI renders these as italic letters rather than proper operators; representative 17592186304985 was visually inspected. The earlier operator-repair rule missed this spelling. These are source/import notation defects, not evidence that the new generator keys are mathematically wrong.

## Why the pipeline allowed this

The evidence supports a failure of purpose-sensitive acceptance, not an inference about malicious intent.

1. **Band labels became construction instructions.** The code literally appends formulas/values in easy branches and adds wrappers, powers or extra expansions in hard branches. It often changes the knowledge demand instead of adjusting a controlled workload.
2. **Authored exemplars became their own calibration evidence.** Four hard families cite only generated hard predecessors: exact cosine, sine products, basic cosine double angle and alternative cosine double angle. Other invented bands cite a generated prototype alongside an imported canonical example or cite an import from a different band. These can be legitimate authored examples, but their publication is not independent evidence that their pedagogy or rating is sound.
3. **Technical success was an insufficient acceptance condition.** All 78 sampled CLI calls succeeded. All 390 sampled generated keys passed independent numeric witnesses, and their sampled radio options were numerically distinct from the key. Those checks still admitted the overscaffolded and overcomplicated families. Correctness, source replay, seeded variety and rendered TeX do not establish that the learner is practicing the intended skill.
4. **Normal generation and delivered coverage were not checked against the source families.** The missing cancellation family is a direct example. Inventory counts by difficulty can look healthy while a meaningful family is absent. Bank-first role variation can also produce cosmetic clusters rather than better practice.
5. **Generator changes do not repair existing pools.** A new package registration or stronger prompt does not retire already-published bad questions. The current ordinary-practice instructions already prohibit supplying the assessed method and tell reviewers to challenge published exemplars. The live packages and questions still exhibit those failures. A repair must explicitly address both future construction and existing inventory.

The existing source-capture helper does filter ordinary KP practice evidence to imported Math Academy questions. The problem is not that it indiscriminately treats every generated pool member as an import. The weakness is treating separately published authored exemplars, source IDs, or source replays as sufficient calibration evidence without independently comparing the learner's required task.

## Repair priorities

First correct the three ambiguous imported banks, two solution inconsistencies and remaining notation defects, preserving original evidence and learner history. Do not silently discard an already-used answer entity to change a bank.

Then repair the three overscaffolded easy families and their 19 stored questions. Keep the simple mathematical instances; move the identity, values and procedural sequence into the worked solution. Preserve the decomposition hints that the exact-value sum/difference imports actually supply.

Redesign the four clearly inflated hard families: exact cosine, degree shifts for sine and cosine, and alternative cosine double angle. Review the two unanchored factoring extensions separately. Keep the hard reciprocal-ratio and exact-value perfect-square families that the sources genuinely support; “more steps” is not, by itself, a reason to remove them.

Add effective-workload guards for coterminal/antipodal collapse and already-known-angle bypasses, restore the omitted cancellation family, clean up double-negative response frames, and reject renaming-only duplicates as new mathematical inventory.

The acceptance evidence should compare a matched imported and generated question before feedback: what must the student recall, identify, choose and calculate; what is supplied; what the response frame or choices reveal; and exactly what changes across bands. Generated anchors should remain explicitly authored evidence. A source example with a flaw should be flagged, not promoted into an immutable rule. Do not require a different procedure for every difficulty label, and do not invent unrelated work merely to populate all three bands.

Finally, audit the delivered pool after filtering and publish a separate retirement/replenishment plan. Re-registration alone is not completion. The safer aim is useful independent practice, not minimum difficulty counts or a longer solution transcript.

## Verification and limits

- All 13 registered packages were captured, including their declared runtime files; all four lessons' tutorials and canonical examples were reviewed.
- 78 CLI probes covered each package, all three bands, seeds 7 and 31, with five records per call: 390 generated records, no runtime failures.
- Numeric witnesses covered all **318 stored complete answer keys** and all 390 sampled keys. Three variable assignments were used for symbolic shift expressions; closed-angle expressions were evaluated directly. No key mismatch was found. These are independent numerical checks, not exhaustive symbolic proofs of every possible future output.
- The same independent reader checked **11,976 worked-solution equality instances** across stored material and samples. Parse limitations were resolved in the audit reader; the two retained failures above were manually confirmed. Fourteen absent imported solutions were retained as missing evidence.
- Twelve representative cases rendered through the actual learning UI, including positive controls, overscaffolding, inflated hard tasks, source notation and the known-angle bypass. Representative screenshots were visually inspected. This was not a screenshot-by-screenshot visual review of all 359 records.
- Six live read-only grading calls confirmed that the three ambiguous banks accept the designated key and reject the valid alternative. No learner attempts were created.

See [completion.json](completion.json) for the fixed-basis scope, [generator-probes.json](generator-probes.json) for runtime coverage, [numeric-results.json](numeric-results.json), [solution-results.json](solution-results.json), [ambiguous-choice-grading.json](ambiguous-choice-grading.json), [source-reference-origins.json](source-reference-origins.json), and [renders/rendering.json](renders/rendering.json). This audit contains findings and recommendations; it does not claim the live repairs have been applied.
