# Practice Question Rules

Practice is the main test of whether the lesson stayed focused.

## Defaults

- Use `type: radio` quiz blocks for multiple-choice practice.
- Use five choices when natural, but preserve the original option count when copying or adapting a provided homework question.
- Give every quiz block an `id`.
- Give every option an `id`.
- Mark exactly one option with `correct: true` for radio questions.

## Mirrored Practice

The first practice item after a worked example should mirror the worked example closely:

- same reasoning move
- same answer form
- same notation style
- only small surface changes

## Controlled Variation

Later practice may vary one dimension:

- numbers or constants
- sign
- exponent or power
- representation: equation, table, graph, diagram, or word description
- requested output
- hidden cue
- common trap
- edge case

Do not vary several of these at once unless the section explicitly teaches that combined variant.

## Distractor Strategy

Distractors should come from actual mistakes:

- using the wrong quantity's units
- forgetting a factor or exponent
- confusing coefficient and whole term
- treating a constant term like a multiplied term
- using a linear instead of angular unit
- choosing the result from a previous section

Do not use random-looking wrong answers when a meaningful distractor is available.

## Explanations

Follow `$quiz-block-factory` and its `references/feedback-standard.md`; that skill owns
feedback placement and quality rules. For generated radio and checkbox practice:

- Give every option nonempty, response-specific feedback.
- For a correct answer, state the governing rule in natural language, apply it to the
  prompt, and finish with the requested symbolic, numerical, or graphical conclusion.
- For a distractor, identify the actual misconception or failed step behind that
  option, clarify the role of the confused quantity or operation, and contrast it with
  what controls the answer here.
- Add the boundary condition that would make a tempting claim true when it improves
  discrimination and transfer.
- Do not substitute generic praise, rejection, an unexplained formula, or the same
  answer explanation for every distractor.
