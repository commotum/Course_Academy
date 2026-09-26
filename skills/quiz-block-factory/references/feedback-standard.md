# Corrective Feedback Standard

## Contents

- [Purpose](#purpose)
- [Core sequence for a correct response](#core-sequence-for-a-correct-response)
- [Core sequence for a distractor](#core-sequence-for-a-distractor)
- [Principles](#principles)
- [Type-specific placement](#type-specific-placement)
- [Quality failures to reject](#quality-failures-to-reject)
- [Final review questions](#final-review-questions)

## Purpose

Treat each response as a tiny corrective lesson. Feedback should help a student reconstruct the reasoning on a nearby problem, not merely learn which option was marked correct.

## Core sequence for a correct response

Use this order when the task is conceptual or physical:

1. State the governing physical or conceptual rule in natural language.
2. Interpret the given symbols, graph feature, or situation using that rule.
3. State the requested conclusion in the question's notation.

Example:

> An SHM acceleration always points back toward equilibrium. Here the oscillator is left of equilibrium because $x<0$, so “back” is the positive direction. Therefore, $a>0$.

For a calculation, use:

1. Name why the relationship applies.
2. Map each given to its role.
3. Substitute with guard digits.
4. Give the requested result with sign, units, and justified precision.

Do not lead with unexplained symbol manipulation when a physical or conceptual statement can explain the relationship.

## Core sequence for a distractor

Write feedback for the selected option, not generic feedback for the question:

1. Diagnose the exact misconception or failed step that produces the choice.
2. State what the misused quantity, sign, graph feature, or operation actually means.
3. Contrast it with the quantity or rule that controls the answer.
4. Apply the corrected distinction to this situation.
5. When useful, state the condition under which the choice would have been valid.

If a supplied distractor's construction is unclear, state the objective rule or operation it violates and apply the correction. Do not invent a psychological explanation that the option does not support.

Example:

> Velocity tells which way the oscillator is moving, but position determines the restoring acceleration's direction. At $x<0$, acceleration points right regardless of the current sign of $v$.

## Principles

### Physical intuition before algebra

Explain why the equation applies. “The restoring force points toward equilibrium” is more useful than merely citing $a=-\omega^2x$.

### Minimum sufficient explanation

Use the shortest feedback that fully reconstructs the reasoning. Correct feedback is usually a compact rule → prompt interpretation → conclusion chain. Once the physical or conceptual rule settles the result, do not append algebra that merely repeats it.

Distractor feedback may be longer because it must diagnose and repair a specific error. Add only the contrast, boundary condition, or symbolic step needed to make that repair transferable.

### Natural-language-to-symbol bridge

Translate both ways:

- $x<0$ means left of equilibrium.
- Acceleration points right means positive acceleration.
- Therefore $a>0$.

Use the question's own symbols in the conclusion so verbal understanding and notation stay connected.

### Clear variable roles

Explicitly separate nearby quantities students often confuse. For example:

- position identifies location relative to equilibrium;
- velocity identifies direction of motion;
- acceleration identifies how velocity changes;
- amplitude identifies the maximum possible displacement;
- wave speed describes propagation while particle speed describes local medium motion.

Preserve the valid meaning of the student's chosen quantity before explaining why it does not answer this question.

### Contrast rather than contradiction

Prefer:

> The graph's slope gives velocity, while acceleration magnitude follows distance from equilibrium.

Avoid:

> Wrong. Use $|a|=\omega^2|x|$.

The contrast repairs the underlying category error.

### Boundary conditions

State when a tempting claim becomes true:

- acceleration is zero at equilibrium;
- velocity is zero at a turning point;
- two paths tie when their absolute displacements are equal;
- a formula applies only under its stated boundary conditions.

This converts a wrong option into a discriminating rule.

### Transferability

Phrase the governing idea so it survives a change of numbers, direction, notation, or representation. Use the current values only after stating the reusable rule.

## Type-specific placement

### `radio`

- Give every option feedback.
- Correct option: rule → application → conclusion.
- Each distractor: its own misconception and repair.

### `checkbox`

- Give every option feedback because each statement is independently judged.
- Explain why each selected statement is true and why each unselected statement fails.
- Do not use one generic root explanation.

### `select`, `multi-select`, and `noodle`

- Put feedback on each question item.
- Explain the classification or match cue and the correct mapping.
- Shared option labels may have option feedback in the runtime schema, but those renderers ignore it. Question-level feedback is the canonical teaching location.

### `free`

- Put the model response or required-feature checklist in `correct`.
- Use root `feedback` for strategy, self-checks, common omissions, units, or a supporting-work checklist.
- Do not imply that wording must match exactly.

### `blank`

- Put the literal typed response inside `==...==`.
- Use root `feedback` to show polished notation, the governing relationship, calculation, units, precision, and common traps.

## Quality failures to reject

- “Correct.” or “Try again.”
- Restating the option without explaining it.
- Giving only a formula when its physical meaning is the learning target.
- Giving every distractor the same correct solution without diagnosing different errors.
- Appending algebra or extra facts after a complete conceptual explanation when they add no new reason or check.
- Claiming a value “does not follow” without identifying what operation produced it.
- Explaining an irrelevant mistake that would not produce the selected option.
- Omitting sign conventions, units, boundary conditions, or graph semantics when they decide the result.
- Giving away the answer in prose before the student responds.

## Final review questions

For every response, ask:

1. Does it explain why this exact choice is right or wrong?
2. Does it connect an intuitive model to the relevant symbols or representation?
3. Does it assign potentially confused quantities distinct roles?
4. Does it identify a real misconception rather than inventing one?
5. Is the corrected rule usable on a nearby variant?
6. Are the signs, arithmetic, units, significant figures, and physical claims independently verified?
