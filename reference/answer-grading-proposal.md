# Answer grading proposal

Keep the existing question → answer-field → answer model. Grade selections by answer identity and entered mathematics by a deterministic checker that understands both mathematical meaning and the task's requested form. Store the learner's original response and the final result in the existing task item. The application then calls the completion engine; FIRe does not decide whether an answer is mathematically correct.

This is a proposed Course Academy policy, grounded in the captured content. It is not a claim to have recovered Math Academy's private grader. No schema or grading implementation is changed by this proposal.

## What the captured questions establish

A fresh count of the normalized lesson JSON on September 29, 2026 found 19,646 question placements: 16,570 multiple-choice, 2,010 free-response, and 1,066 select-list. They contain 19,644 distinct question IDs. These are content placements, not learner submissions. The current EDB model correctly interprets the captured free-response questions as structured blanks.

The following are actual inspected questions. Their prompts and response structures are captured; the mathematical conclusions below are our own checks, not recovered answer keys.

| Captured question | What it requires from the grader |
| --- | --- |
| [37721, tangent plane](../../MA/DATA/Lessons/1980/Source/1980.json) | Five mathematical options. Selecting the correct answer entity is sufficient; grading need not parse the chosen plane equation. |
| [213011, mapping diagram](../../MA/DATA/Lessons/4837/Source/4837.json) | Five image options. Grade the selected entity exactly as for textual options. The image filename or shuffled letter is not the answer identity. |
| [215061, rational equation](../../MA/DATA/Lessons/3555/Source/3555.json) | One blank after `y =`. The solution is `-6/7`. Accept equivalent exact values, while respecting the equation's excluded denominators. |
| [215327, simplifying polynomials](../../MA/DATA/Lessons/1783/Source/1783.json) | Explicitly requests standard form for `6z³ − 5z − 4z³ − 1`. `2z³ − 5z − 1` satisfies the task; merely re-entering the original expression must fail even though it is equivalent. |
| [69242, factoring](../../MA/DATA/Lessons/2337/Source/2337.json) | Asks to factor `4x³ − x`, with `x(2x+1)(2x−1)` among its choices. This capture is multiple-choice; a generated blank version would additionally need a factored-form check. |
| [213469, modular arithmetic](../../MA/DATA/Lessons/4839/Source/4839.json) | Five blanks: four intermediate modular powers and the solution. The final answer must be a nonnegative integer below 25. `13` is valid; the congruent integer `38` violates the instruction. |
| [222843, principal normal vector](../../MA/DATA/Lessons/1795/Source/1795.json) | Two separate vector-component blanks. Their field identities matter; correct components in exchanged fields do not form the requested vector. |
| [267352, unit-circle angle](../../MA/DATA/Lessons/112/Source/112.json) | A degree answer rounded to two decimal places, with a scientific calculator required. The prompt supplies the unit outside the blank. |
| [234173, binomial approximation](../../MA/DATA/Lessons/1158/Source/1158.json) | Requests the first four terms to approximate `1.02⁸`, rounded to five decimal places. Those terms give `1.17165`; rounding the exact power gives `1.17166`. Grading the exact expression instead of the requested approximation would mark the intended answer wrong. |
| [214575, interval/inequality conversion](../../MA/DATA/Lessons/4028/Source/4028.json) | Two blanks after `x`, one for the relation symbol and one for the boundary. The expected entries are `<` and `-1`; not every math-editor blank represents an arithmetic expression. |
| [251528, paired-sample confidence interval](../../MA/DATA/Lessons/3970/Source/3970.json) | Four dropdowns, mixing mathematical and textual options. Each field has its own correct answer, and the whole question has one outcome. |
| [212995, relation on a finite set](../../MA/DATA/Lessons/2817/Source/2817.json) | A set of ordered pairs appears in multiple-choice answers. A future entered version must ignore order between set members while preserving order inside each pair. |

The normalized captures do not contain a complete canonical answer key or grading contract. [answers.md](answers.md) was an earlier answer-key proposal, including suggested nullable fields and a non-exact blank mode; it is not evidence that those rules were implemented or are sufficient. The newer [answer model](answer-model.md) is the current schema design. [explanation-format.md](explanation-format.md) demonstrates a worked solution, not a general acceptance algorithm.

## Selection questions

For multiple choice and each dropdown, resolve the supplied answer ref, verify that it belongs to that question's field, and compare it with `answer-field/correct-answer`.

Use entity identity, never displayed letter, option position, image path, or rendered text. Shuffling changes presentation only. A selected answer already identifies its field through the field's choices, so there is no extra submission wrapper or duplicated field relationship to store for it. Image choices require no image-recognition grader.

Before an item becomes eligible for delivery, verify that it has one correct choice per field and that no distractor is also valid under the stated task. Finding two valid options is a content defect to fix, not a reason to punish the learner for choosing the other valid one.

## Entered mathematics

The initial checker should apply these rules:

1. **Parse notation, not executable code.** Convert supported editor output or typed syntax into a mathematical syntax tree. Normalize harmless notation differences, such as Unicode minus, multiplication spelling, `\\frac` versus `\\dfrac`, and redundant grouping. Preserve the original response string and preserve the unsimplified tree for form checks. Never execute input as Python or another programming language.
2. **Use exact comparison by default.** Integers, finite decimals, fractions, radicals, and supported symbolic expressions represent exact values unless the problem requests approximation. For example, `1/2`, `2/4`, and `0.5` can denote the same exact value; `0.333333` is not automatically equal to `1/3`.
3. **Require both equivalence and the requested form.** For factoring, check equality to the expected polynomial and the required factor structure. For standard-form polynomials, check that like terms are combined and nonzero terms occur in the requested power order. For a reduced fraction, check coprime numerator and denominator with a normalized denominator sign. Harmless rearrangement of factors and equivalent sign placements remain acceptable. Do not simplify the submitted tree before checking what the learner actually entered.
4. **Compare over the stated domain.** Real/complex assumptions, denominator exclusions, branch restrictions, and variable constraints are part of the question's acceptance requirements. `sqrt(x²)` is not `x` for unrestricted real `x`. For equation-solving questions, compare the complete permitted solution set and check proposed solutions in the original equation; matching only a transformed equation can accept extraneous roots.
5. **Use the correct mathematical structure.** Sets are unordered and discard duplicate members; tuples, vector components, and matrix entries are ordered. Interval endpoints and open/closed boundaries matter. Relation-symbol fields accept only the appropriate relation tokens. Congruence-class questions compare residue classes only when the prompt permits that representation; a request for the least nonnegative representative additionally constrains the entered value.

Exact symbolic checks should prove equality within the supported expression families. Numerical sampling can help find counterexamples during authoring; it must not be the sole reason to accept a symbolic identity. A checker that cannot decide a supported-looking expression should report a grading limitation, not invent a correct or incorrect result. Initially, make only questions whose required mathematics is supported eligible for automated grading; do not promise universal mathematical equivalence.

### Rounding and numerical answers

For a question asking for `d` decimal places, compute the intended quantity at sufficient precision and produce its decimal value rounded to `d` places, with halfway cases rounded away from zero. Accept the learner's parsed numeric value only if it equals that rounded value. Ignore cosmetic trailing zeros: `2.50` and `2.5` have the same accepted value. A more precise unrounded answer does not satisfy an explicit rounding instruction. Apply the same principle to significant figures; do not infer the number of significant figures from a stored string's trailing zeros.

This avoids a universal tolerance such as “within 1%,” which would accept distinct intended answers. It also avoids adding a tolerance to every answer entity. If a future numerical-method or measurement question genuinely permits a range, give that question an explicit absolute/relative tolerance in its grading contract. For such a contract, use `abs(submitted − expected) <= max(absolute_tolerance, relative_tolerance * abs(expected))`. Do not apply this approximate rule to exact integers, exact symbolic mathematics, or selection questions.

Units printed outside a blank are supplied by the problem; do not require the learner to type them again. Where entering units is part of the task, validate dimensions and allowed conversions explicitly. Do not infer degrees versus radians from which value looks closer to the expected answer. For numerical approximation questions such as 234173, the expected value must come from the requested approximation procedure, not a more accurate but different calculation.

## Text, multiple fields, and submission errors

For genuinely textual entries, default to exact text after Unicode NFC normalization, trimming outer whitespace, and collapsing repeated whitespace. Preserve case and punctuation when they can carry meaning. Broader equivalence—aliases, spelling alternatives, or case-insensitivity—must be explicitly permitted for the question. Do not use an LLM to decide routine text correctness during a timed task. The inspected mixed text/math questions mainly use selections; they do not establish a need for grading arbitrary essays or code.

Require one response for each field. A question is correct only when every required field is correct. Keep field-level feedback in the grader's result for display, but record one final question result for the engine. Five blanks do not become five accuracy observations or five independent repetitions. Unordered collections within a single field and equivalent systems of answers need a question-level check; the field key is not an instruction to impose an order the prompt never required.

An empty or syntactically malformed entry should trigger a clear input message before submission is accepted, without revealing mathematical correctness. The learner can correct the syntax; this does not create a wrong answer or a retry. The task timer continues normally. An explicit Skip action is recorded as `skipped`. A well-formed but mathematically wrong answer is `incorrect`, including a well-formed answer that fails the stated form or domain requirements. Missing answer keys, unsupported notation that the question requires, and checker failures are application/content errors, not incorrect learner answers.

This proposal does not introduce partial correctness into FIRe or XP. Partial field feedback can help instruction without pretending that a partially completed question has supplied the same evidence as a correct solution.

## Where the grading requirements live

Retain the current simple EDB attributes. `answer/type` specifies representation, not a complete grading method. A string value of `x²−1` cannot tell the application whether a problem asks to factor, expand, evaluate, or simplify it. Even an arithmetic “calculate” task can need a numeric-form rule to reject simply copying an unevaluated expression. Requirements that distinguish these tasks must exist somewhere explicit; they cannot reliably be guessed from the prompt on every submission.

For the initial implementation, use a small versioned grading registry alongside the application and question-generation code:

- Common defaults handle selections, exact scalar mathematics, and normalized text.
- A question family supplies a deterministic checker and any domain/form requirements it needs. A generator uses the same declared requirements when producing its questions.
- When an imported question needs an exception, an entry keyed by its stable question UUID and field key supplies just the missing requirement, such as decimal places or polynomial standard form. Do not copy its problem, expected answer, choices, topic membership, or learner state into that registry.

These are authored content requirements interpreted by application code, not a new mutable learner record, a second answer bank, or a generic grading enum. Migrations can prepare these entries, but automatic extraction from prose needs verification before delivery. The registry must be available on every serving installation. If editing grading requirements without deploying code later becomes important, move those concrete requirements into EDB using narrowly named attributes then; that need does not justify adding a large evaluation schema now.

This follows EDB's recommendations to [model a relationship once, query through refs, and grow the schema as concrete needs appear](/home/jake/Developer/EDB/docs/02_core_concepts/05_best_practices.md). The current expected-answer ref remains the authoritative answer. Its canonical value alone is sufficient for the common cases, and only requirements absent from that value belong in the registry.

## Completion-engine integration

The existing [`complete_item`](../engine/rust/runtime.rs) accepts an already graded `result` and selected answer refs or entered response entities. It derives elapsed time from status history. Implement the grader directly before that boundary:

```text
question + expected answers + explicit requirements + learner responses
    → validate and grade
    → correct / incorrect, or explicit skip
    → complete_item
    → task-item responses/result/time and normal engine updates
```

The authoritative application checks membership and grades; it does not trust a browser-supplied correctness flag. Use one consistent database value to retrieve the question and expected answers. Store entered values through `learner-response/field` and `learner-response/value`; selections point directly to existing answer entities. Persist completion through the existing transaction path rather than recording a second grading event.

Elapsed time, question difficulty, and calculator requirements do not change mathematical correctness. They may independently affect scheduling or performance magnitude under the engine's policy. A correct but slow answer remains correct. The same checker applies in lessons, reviews, assessments, diagnostics, and self-selected study. A diagnostic's accepted silly-mistake retry replaces the original outcome for knowledge-frontier inference, as decided; both actual submissions remain in the activity history.

## Generator storage recommendation

Keep Python source in the versioned repository. A repository-relative string such as `generators/polynomials/difference_of_squares.py` is enough to locate a script; a UUID alone does not locate code, and EDB need not contain the source text. For the current single-generator-per-KP use case, store that relative path directly on the KP as a string. The existing `knowledge-point/question-generator` is a ref, so adopting this proposal would require changing that attribute definition before database creation. Do not introduce another entity merely to hold one path; no such schema change is made here.

Git preserves edits to the script; the application must still know which repository and checkout it runs. Git history alone does not associate a previously generated question with a particular commit. Reproducing an old generation would additionally require its code revision, parameters, and random seed, but that is separate from storing and serving the resulting verified question. Do not add those records merely to make a path usable.

Use one fixed runner interface: the application supplies a seed and validated generation parameters, and receives ordinary question/field/answer records plus any explicit acceptance requirements. The runner resolves the path beneath the configured repository root. Family code may share grader logic, but generated per-question requirements resolve by stable question UUID and field key; the registry does not duplicate the canonical expected answer. A generator should produce a compatible acceptance contract. Verify the mathematical property independently—for example, expand generated factors or substitute roots into the original equation—before adding a question to the usable bank. Keep a generated question's verified answer in EDB; do not rerun the current generator during grading to rediscover what its answer used to be.

The practical first implementation is selection grading plus exact scalar blanks, followed by the explicit form, domain, and rounding checkers needed by the first topics chosen for study. Other captures can remain available for content recovery until their answer keys and required checkers are ready.
