# Remaining trig-substitution generators: strengths and weaknesses

Read-only audit, 2026-10-24, database basis **T6393**. Topic **17592186050489**, “Integrating Trigonometric Functions Using Substitution” (MA topic478). The previously repaired linear sine/cosine KP, 17592186068915, is excluded.

No generators, question records, retirement flags, or learner history were changed by this audit.

## Inventory and source coverage

Imported counts below are the stored labels, not independently endorsed difficulty ratings. “Unrated” is separate from easy.

| KP | Imported easy / moderate / hard / unrated | Current generated pool | Generator status | Imported questions represented in code |
| --- | --- | --- | --- | --- |
| 17592186068916: reciprocal trig, linear arguments | 4 / 8 / 6 / 1 | 0 | Local draft; no registered generator | 10 of 19, including one evidence-only source |
| 17592186068917: products | 0 / 7 / 11 / 0 | 3 moderate | Registered | 8 of 18 |
| 17592186068918: quotients | 0 / 0 / 17 / 2 | 5 authored easy | Registered | 7 of 19 |

The registered script paths at this basis are `generate/scratch/17592186068917.py` and `generate/scratch/17592186068918.py`. The reciprocal draft is `generate/scratch/17592186068916.py`.

The structural source-eligibility check found no retired or multistep-contained source questions in these three pools. That earlier contamination problem was not reproduced here. Missing source coverage is an inventory gap, not a requirement to copy every imported question: some sources require correction or placement review first.

## Main diagnosis

Both active generators implement **amplitude transport of whole imported answer banks**: choose a source, multiply its integrand and every answer by a positive integer from 2 through 12, retain its inner expression, bounds, and difficulty label, then reconstruct a solution.

This preserves much of the source mathematics, but treats a numerical variant as sufficient pedagogical variety. Neither implementation specifies and balances the mathematical decisions a learner should practice. Their fingerprints distinguish numerical prompts, so several near-identical questions count as distinct pool members. Inherited source labels also substitute for a workload-based difficulty model.

The quotient generator adds a separate consistency failure: its answer bank comes from scaled source expressions, while the solution comes from an independently simplified symbolic primitive. Mathematical equivalence does not supply the missing learner-facing explanation connecting the two forms.

## Reciprocal trig with linear arguments — KP 17592186068916

### Strengths

- The local draft varies meaningful parameters: inner slope, outside coefficient, angular shifts in hard questions, and endpoint pairs. It is more than an amplitude-only wrapper.
- Its finite parameter guards keep secant/cosecant definite integrals within appropriate pole-free components and familiar endpoint angles.
- It checks derivative-equivalent primitive banks and unique correct answers, rather than relying only on textual equality.
- It explicitly keeps the nonlinear source q-113983 as evidence-only. It also records its authored completion and easy rating for the incomplete, unrated source q-10157.

### Weaknesses

- **There is no deployed generator or generated pool for this KP.** A working local draft must not be confused with registered production coverage.
- Normal easy practice contains only secant–tangent and cosecant–cotangent with positive integer inner slopes and zero shifts. The canonical example, `e-465`, is \(\int 5\csc(6x+\pi/3)\cot(6x+\pi/3)\,dx\). The draft cannot produce that shifted easy form. A constant angular shift adds no derivative step to an indefinite integral, so excluding every easy shift is poorly justified.
- **Every moderate template uses cosecant squared, and every transformed upper endpoint is \(\pi/2\).** Consequently the upper primitive contribution is always zero. Learners repeatedly avoid part of the endpoint arithmetic.
- The code models only two of the eight currently imported moderate questions. It misses available moderate secant-squared, secant–tangent, and cosecant–cotangent cases, among others.
- All normal inner slopes are positive, limiting sign practice.
- Two easy imports need placement review: q-113983 uses \(u=\sec x\), and q-113979 uses \(u=\tan x\). These are nonlinear substitutions despite this KP’s linear-argument title. Their presence does not justify silently broadening the generator’s objective.

### Appropriate repair direction

Resolve those source-placement questions, then complete and register the draft. Balance all four reciprocal derivative families across appropriate bands. Include harmless shifts in indefinite practice; diversify moderate endpoint pairs so both primitive evaluations sometimes contribute; reserve hard for a supported combination of fractional slopes, shifts, and more demanding endpoint arithmetic. Avoid treating a shift alone as a universal hard/easy boundary.

## Products containing trig functions — KP 17592186068917

### Strengths

- The mathematical model preserves the derivative factor needed for substitution and supports nonlinear inner functions, definite integrals with transformed root bounds, and a reciprocal-inner case.
- The generator transports complete source answer banks instead of inventing unsupported distractors.
- All three currently stored generated questions have a derivative-verified unique correct choice. The native grader accepts their keys and rejects their other choices.

### Weaknesses

- **Only the amplitude changes.** The substitution, trig function, inner exponent, inner coefficient, phase, and bounds remain fixed within each source family. This rehearses recognition of a small set of silhouettes.
- The current three-question pool consists of \(2x\csc^2(x^2)\), \(2x\sin(x^2)\), and \(8x^2\sec^2(x^3)\). These are mathematically valid, but narrow coverage of the KP.
- The canonical example uses \(x^3-\pi/6\); the generator cannot vary phase or reproduce that shifted family. It represents 8 of the 18 current imports and misses, for example, the square-root-inner family \(\cos(\sqrt{x})/\sqrt{x}\).
- **22 of its 55 available hard candidates equal zero: 40%.** The two fixed-bound families q-13533 and q-13537 each contribute 11 amplitude variants, all with zero final answer. After recognizing the family, the learner can answer without practicing the full substitution. This is a property of the entire finite candidate set, not a sampling estimate.
- Difficulty is inherited from the source. Changing the amplitude can remove coefficient work—for example, \(2x\sin(x^2)\) has an exact \(du\)—without changing the label. Some imported hard indefinite examples use essentially the same substitution workload as moderate examples, so the labels need review before expansion.

### Appropriate repair direction

Generate from a dependency-preserving substitution model: choose a supported inner function, derive its required outside factor, and choose trig family and coefficients separately. Balance families in each published pool, vary bounds within safe intervals, and limit zero-result definite questions. Include the supported shifted and root/reciprocal cases where curriculum scope permits. Use recognition, coefficient handling, substitution form, and endpoint workload to justify bands; larger coefficients alone do not justify hard.

## Quotients containing trig functions — KP 17592186068918

### Strengths

- The core \(f'/f\) substitution model is appropriate, including absolute values in indefinite real logarithms and explicit domain restrictions.
- It recognizes unusable imported banks: q-10046 contains nonreal logarithm options, and q-10045 has duplicate wrong choices. Avoiding direct transport of those banks is sensible, although valid mathematical families can be retained with repaired banks.
- All five currently stored generated questions have a derivative-verified unique correct choice, and their native grading checks pass.

### Weaknesses

- **The entire current pool is five coefficient variants of \(\cos x/\sin x\).** Their outside coefficients are 12, 10, 4, 6, and 8. This is repeated practice of one substitution, not five meaningfully varied questions.
- Code supports one authored easy family and six inherited hard families, with no moderate band. The current imports have 17 hard and 2 unrated labels, so there is no imported easy/moderate calibration to inherit. The easy rating is an explicit local inference, not a source-backed label.
- Only 7 of 19 imports are modeled. Of the 12 absent sources, two are explicitly excluded for bank defects and ten are additional unmodeled sources. The canonical \(\tan x\sec^2x/(1+\tan^2x)\) denominator family is not generated.
- **Reproduced solution/key conversion gap:** q-350887 at amplitude 2 has key \(2\ln(4/3)\), but its worked solution ends at \(\ln(16/9)\), without showing the logarithm power rule connecting them. q-350901 similarly gives \(2\ln(6/5)\) versus \(\ln(36/25)\). The native symbolic comparator confirms equivalence; the explanation remains incomplete.
- **Reproduced lost constant explanation:** q-113997 at amplitude 2 has a key ending \(2\tan x-2\ln|\tan x+1|+C\), while its worked solution retains an extra \(+2\) with the same \(+C\). The imported solution explicitly introduced a new constant to absorb its \(+1\). The generator discards that explanation when rebuilding the solution.
- **Reproduced publication failure:** q-350904 has two accepted source spellings of the same logarithm. Scaling by 2 renders both answers identically. The shared publication-preparation function rejects the record with `Answer bank contains duplicate identities or typed values`. This affects a future hard output; none of the five stored easy questions uses that template.

### Appropriate repair direction

First repair the answer/solution rendering contract and alias normalization. Have the solution explicitly reach the displayed key, or show the conversion and any renamed integration constant. Deduplicate accepted aliases when transformation makes them identical.

Then build a progression around actual work: transparent \(f'/f\) recognition; coefficient/sign adjustment and definite evaluation; then supported nested substitutions or algebraic rearrangement. Vary denominator families and safe parameters rather than amplitude alone. Newly authored bands need explicit calibration because the imported labels supply no easy/moderate baseline here.

## Priority and pipeline implications

1. **Quotients:** fix the reproducible explanation gaps and publication failure, then replace the five near-clones with a balanced pool.
2. **Products:** replace amplitude-only generation, cap zero-result repetition, and calibrate the hard band.
3. **Reciprocal linear:** resolve source placement, broaden the draft’s moderate coverage, validate it fully, and register it.

The generation instructions should require an explicit target move and allowed prerequisites, a difficulty model based on mathematical work, coverage targets for each pool, and a shared derivation behind the key and worked solution. Validation should check three different things: mathematical correctness, publication/grading contracts, and whether the explanation reaches the accepted answer without an unshown identity or constant change. Exact prompt fingerprints alone cannot enforce pedagogical variety; family balance and shortcut checks are also needed.

## Verification and limits

- Captured the complete topic/KP/question snapshot at T6393 in [topic.json](topic.json).
- Compared current imported inventories with code templates: [source-coverage.json](source-coverage.json).
- Checked source retirement/multistep eligibility: [excluded-sources.json](excluded-sources.json) is empty.
- Independently differentiated every answer in all eight current generated radio questions: each has exactly one mathematically correct choice. See [existing-math-verification.json](existing-math-verification.json) and [check_existing.py](check_existing.py).
- Ran those eight questions through `course_academy_engine::learning::grade_field`: **8 expected accepts and 32 expected rejects**, zero unresolved checks. See [existing-grader-verification.json](existing-grader-verification.json).
- Enumerated all 55 product hard candidate parameter combinations to establish the 22 zero answers. This enumeration uses the generator’s symbolic model; the independently checked stored questions use parsed printed prompts and answers.
- Inspected code, generated five reciprocal-draft examples per band, ten product-hard examples, five quotient-hard examples, and four explicit quotient probes. These sample artifacts are in this directory. This is not an exhaustive mathematical certification of every future output or every imported question.
- Confirmed the two different logarithm forms with the native symbolic comparator: [log-form-comparison.json](log-form-comparison.json).
- Reproduced the duplicate-bank rejection at the actual shared publication-preparation boundary without writing to the database: [duplicate-bank-publication-check.json](duplicate-bank-publication-check.json).
- The learning UI shuffles radio choices by question/answer identity; fixed source-array order is therefore not counted as a demonstrated learner-facing shortcut.

No rendered visual-layout audit was performed. The priorities above concern demonstrated content, explanation, coverage, and publication behavior.
