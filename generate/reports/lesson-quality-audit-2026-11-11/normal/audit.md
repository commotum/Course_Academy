# Normal-line lesson audit

Read-only audit at saved **basis 14220**. Both untouched generators retain the calculus work in independent prompts; no wrong generated slope/intersection, domain error, supplied derivative or supplied normal rule was found in the scoped checks. Two bounded stored-content findings remain.

| KP | Stored inventory | Generator assessment | Stored assessment |
| --- | --- | --- | --- |
| `17592186092384`, normal slope | 31: 15 imported, 16 authored | No confirmed defect; all three bands checked | One minor imported solution notation error; three incomplete imports |
| `17592186092385`, normal intercepts | 27: 12 imported, 15 authored | No confirmed defect; all three bands and both axes checked | All eight complete radio banks permit the same bank-only shortcut; two incomplete imports |
| `17592186092240`, normal equation | 36: 20 imported, 16 authored | Repaired registration and independent authored prompts remain consistent | One incomplete import; five context-dependent multistep parts already excluded from standalone source eligibility |

## Confirmed findings

**The entire eight-question intercept radio subgroup can be answered from its banks alone.** Identify which coordinate varies among the offered points and choose its unique numerical maximum. The reproduction never reads the prompt, function, key or solution to select an answer. It succeeds on all eight captured complete radio records:

`17592186092507`, `17592186092510`, `17592186233120`, `17592186240795`, `17592186240796`, `17592186493316`, `17592186578858`, `17592186710717`.

Six are imported and two authored. The native grader accepted all eight selections and rejected all 32 alternative options; all eight records also passed native practice eligibility at this captured basis. This is a demonstrated shortcut in the **complete current finite radio subgroup**, not a claim about future populations or blank questions. It bypasses differentiation, slope evaluation, reciprocal recall, normal construction and axis intersection. Current ordinary generator `8c7c9b…/generator.py:119` uses two coordinate blanks and does not emit these banks. Evidence: [bank-only reproduction](bank_probe.py), [all banks and selections](bank-probe.json), [native proof](bank-probe-native-report.json), and [actual authored radio UI](render/question-022-active-390x1000.png).

**Imported slope question `17592186317210` (`q-342153`) retains a free variable in an evaluated-derivative equality.** Its solution writes `f′(1/4)=1/(2√(x³))` before the next equality substitutes `x=1/4`. The final tangent slope 4 and normal-slope key −1/4 are correct. This is a minor notation defect, not a wrong answer. Actual UI confirms the chain; the existing slope generator’s replay branch already removes the free-x intermediate at `3692ddb…/generator.py:186–187`. Ordinary sampled solutions do not repeat it. Evidence: [completed mobile UI](render/question-020-completed-390x1000.png) and [right edge](render/question-020-completed-390x1000-math-scroll-right.png).

## Import completeness and context

Six records have missing gradeable data. The actual native `validate_practice_question` rejects all six, with repaired question `17592186710391` passing as a positive control; these imports are screened from practice, not counted as served defects ([native proof](eligibility-verification.json)):

- Equation `17592186234077` (`q-47405`): no answer fields.
- Slope `17592186092723` (`q-47407`) and `17592186092725` (`q-47413`): missing correct-answer links and worked solutions.
- Slope `17592186234307` (`q-71525`): no answer fields.
- Intercepts `17592186233928` (`q-342222`): coordinate fields have no banks or keys.
- Intercepts `17592186234308` (`q-71542`): no answer fields.

The five equation fragments `17592186235432`, `17592186235480`, `17592186514424`, `17592186578848`, `17592186600817` depend on f/h definitions or earlier parts absent from their individual stems. Current structural source eligibility explicitly excludes all five. Their need for parent context is not a generator defect or a complete standalone task.

## Coverage and limits

Inspected all **94 stored records**, distinguishing **47 imported and 47 authored**. Independently checked all **89 standalone displayed functions/points** and **83 complete standalone final keys**. All available final keys agreed with calculus. Intermediate solution equations received targeted review rather than an exhaustive symbolic proof.

For the two untouched generators, ordinary declared-file-only copies produced **240 raw samples** across all three bands and saved seeds `202611111` and `202611112`; independent calculus checked their displayed functions, points and keys. The first seed produced **117 actual delivery survivors**, with **177 accepted equivalents and 177 rejected wrong responses** through the native grader. Three slope samples deduplicated against current inventory. All **22 source replays** also passed independent function/point/key checks.

Actual unchanged learner UI passed **92 cases**: 19 exact delivered representatives plus four stored records, active and completed, at 1280 and 390 pixels. These cover each slope band, every intercept function-family/axis pair, both stored response shapes and the suspect solution. Long completed equations retain accessible horizontal scrolling; paired right-edge screenshots were retained. Generated representatives are exact final survivor objects, not resampled raw approximations.

The slope generator’s ordinary domain is narrower than the full imported family set: quadratics, factored cubics and signed `(x+b)²/√x`. Imported degree-five and other reciprocal-power cases are replayed but not ordinary sampled families. This is a coverage limitation, not a demonstrated wrong task or key. Hard intercept prompts require finding the ordinate from a supplied abscissa; they preserve normal/intersection work while adding that prerequisite evaluation. Authored bands are not empirical difficulty calibration.

No database changes, package edits or dependency changes were made. Machine-readable details: [audit.json](audit.json), [stored ledger](stored-ledger.json), [sample/native coverage](coverage.json), [all raw mathematical checks](extra-math.json), [source-only checkpoint](source-only.md), and [actual UI report](render/rendering.json).
