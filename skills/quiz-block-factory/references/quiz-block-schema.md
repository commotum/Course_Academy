# Canonical Quiz-Block Schema

## Contents

- [Authority and policy](#authority-and-policy)
- [Common root fields](#common-root-fields)
- [Shared option object](#shared-option-object)
- [Shared select-style question object](#shared-select-style-question-object)
- [`radio`](#radio)
- [`checkbox`](#checkbox)
- [`select`](#select)
- [`multi-select`](#multi-select)
- [`noodle`](#noodle)
- [`free`](#free)
- [`blank`](#blank)
- [Runtime compatibility aliases](#runtime-compatibility-aliases)
- [Deterministic validation boundary](#deterministic-validation-boundary)

## Authority and policy

The supported runtime is Quiz Blocks `1.0.1`, installed at:

- `/Users/jake/Developer/study/vault/.obsidian/plugins/quiz-blocks/main.js`
- `/Users/jake/Developer/study/vault/.obsidian/plugins/quiz-blocks/manifest.json`

The complete interactive catalog is:

- `/Users/jake/Developer/study/vault/Old/admin/quiz-test.md`

The development path `/Users/jake/Developer/study/plugins/obsidian-quiz-blocks` is currently an uninitialized Git submodule. Do not treat its empty working directory as evidence that a type or field is unsupported.

The runtime accepts several legacy aliases and can synthesize option IDs from content. Those behaviors preserve older notes; they are not canonical authoring format. Emit only the field names and explicit IDs below.

## Common root fields

Every type accepts these root fields:

| Field | Canonical policy | Meaning |
|---|---|---|
| `type` | Required | One of the seven exact type names below |
| `id` | Required for authored blocks | Stable document-wide text ID; quote values that resemble numbers, booleans, or null |
| `content` | Required and nonempty | Prompt or shared directions; the runtime converts scalar numbers and booleans to display text |
| `gated` | Optional boolean | Plugin gating behavior; default `false` |
| `shuffle` | Optional boolean at runtime; required as `true` by factory policy for `radio` | Shuffle choices; runtime default `false` |

Root objects are strict. Do not place `feedback`, `correct`, `options`, `questions`, `input_mode`, or `require_exact` on a type that does not list them.

Set `shuffle: true` on every canonical `radio` block so the correct answer does not remain in a predictable position. For other choice types, use it only when order carries no meaning.

## Shared option object

Allowed fields:

| Field | Policy |
|---|---|
| `id` | Required for canonical authored choices; nonempty text unique within its bank |
| `content` | Required and nonempty; a scalar number or boolean is converted to display text |
| `correct` | Optional boolean; defaults to `false` |
| `feedback` | Option-level text; required by factory policy for radio/checkbox practice |

Do not add other option fields.

Although the runtime accepts option feedback inside dropdown and noodle option banks, those renderers do not display it. Use question-level feedback for `select`, `multi-select`, and `noodle`.

## Shared select-style question object

Allowed fields:

| Field | Policy |
|---|---|
| `id` | Required for canonical authored grouped questions |
| `content` | Required and nonempty; a scalar number or boolean is converted to display text |
| `correct_option` | Required; must match an option ID in the applicable bank |
| `feedback` | Canonical teaching location; required by factory policy for generated study practice |

`multi-select` question objects also contain their own `options` list.

## `radio`

Additional root field: `options`.

- At least two options.
- Exactly one `correct: true`.
- Set root `shuffle: true`; canonical multiple-choice answers must not remain in authored order.
- Put feedback inside every option, never at the root.

```quiz
type: radio
id: q-1
shuffle: true
content: |-
  Which statement is correct?
options:
- id: a
  content: |-
    First statement
  correct: true
  feedback: |-
    State the rule, apply it here, and conclude.
- id: b
  content: |-
    Second statement
  feedback: |-
    Diagnose the misconception represented by this statement.
```

## `checkbox`

Additional root field: `options`.

- At least two options.
- Mark every independently correct option `correct: true`; require at least one.
- Put feedback inside every option.

```quiz
type: checkbox
id: q-2
content: |-
  Which statements are true? Select all that apply.
options:
- id: a
  content: |-
    True statement
  correct: true
  feedback: |-
    Explain why it is independently true.
- id: b
  content: |-
    False statement
  feedback: |-
    Identify the condition or distinction it violates.
```

## `select`

Additional root fields: `options`, `questions`.

- Use one shared option bank containing at least two options.
- Give option IDs explicitly and uniquely.
- Each question uses `content`, `correct_option`, and canonical question-level `feedback`.
- Each `correct_option` must reference a shared option ID.

```quiz
type: select
id: q-3
content: |-
  Choose the correct category for each situation.
options:
- id: increasing
  content: Increasing
- id: decreasing
  content: Decreasing
questions:
- id: q-3a
  content: |-
    Situation A
  correct_option: increasing
  feedback: |-
    Explain the cue that makes this increasing.
```

## `multi-select`

Additional root field: `questions`. There is no top-level option bank.

- Each question contains its own `options` list with at least two explicit unique IDs.
- Each question uses `correct_option` to reference one of its own option IDs.
- Put feedback on the question item.

```quiz
type: multi-select
id: q-4
content: |-
  Choose one answer in each row.
questions:
- id: q-4a
  content: |-
    First prompt
  options:
  - id: yes
    content: "Yes"
  - id: no
    content: "No"
  correct_option: yes
  feedback: |-
    Explain the deciding rule for this row.
```

## `noodle`

Additional root fields: `options`, `questions`.

- Use for one-to-one matching with at least two choices and two questions.
- Require equal option and question counts and use every correct option exactly once.
- Give shared options explicit unique IDs.
- Each question points to an option ID with `correct_option`; generated study practice includes question-level feedback.

```quiz
type: noodle
id: q-5
content: |-
  Match each quantity with its role.
options:
- id: position
  content: Position
- id: velocity
  content: Velocity
questions:
- id: q-5a
  content: |-
    Identifies direction of motion
  correct_option: velocity
  feedback: |-
    Velocity, rather than position, identifies direction of motion.
- id: q-5b
  content: |-
    Identifies location relative to equilibrium
  correct_option: position
  feedback: |-
    Position identifies where the object is, not which way it is moving.
```

The demo catalog uses `correct` with matching option text and omits option IDs. The runtime preprocessor accepts that compatibility form. Canonical new output uses explicit option IDs and `correct_option`.

## `free`

Additional root fields: `correct`, `feedback`.

- The runtime permits empty `correct` and `feedback` fields. Factory-generated study practice includes both.
- `correct` is the reference answer or required-feature checklist displayed after checking.
- `feedback` supplies strategy, checks, or common omissions.
- Do not use `options`, `questions`, or `require_exact`.

```quiz
type: free
id: q-6
content: |-
  Explain why the result has this sign.
correct: |-
  A complete response should connect the sign convention to the governing physical rule.
feedback: |-
  Check that you identified both the positive direction and the quantity that determines the sign.
```

## `blank`

Additional root fields: `input_mode`, `require_exact`, `feedback`.

- Put at least one nonempty answer inside `==...==` in `content`.
- Match blank granularity to the source response shape. Preserve multiple source answer slots even when their entries combine into one mathematical expression. If the source provides one response slot, keep one blank rather than inventing separately labeled component blanks.
- `input_mode` is optional, accepts `text` or `math`, and defaults to `text`.
- Use `input_mode: math` for symbolic or numerical mathematics that should appear as live visual notation while the learner types. Keep the authored answer keyboard-friendly, such as `(x+3)^2-2`, `x_1`, `sqrt(x+1)`, or `2pi/5`; the runtime converts it to the math field's internal LaTeX.
- Display math supports multiple live blanks on the same LaTeX row and across `\\` row breaks. The fixed math fragments surrounding each field render independently, so keep blank markers outside LaTeX brace groups that must remain syntactically indivisible.
- `require_exact` is optional and defaults to `true`. The runtime trims surrounding whitespace and compares case-insensitively despite the field name.
- With exact text grading enabled, the runtime compares the normalized typed text. With exact math grading enabled, it compares math structure without algebraic simplification, so an algebraically equivalent expression with a different structure may not pass.
- With exact grading enabled in either mode, hidden answers must be literal keyboard-enterable responses, not Markdown or LaTeX.
- With `require_exact: false`, the control reveals answers without grading, so a hidden answer may use display markup such as Markdown or LaTeX.
- Put polished notation, derivation, units, and precision in root `feedback`.

```quiz
type: blank
id: q-7
input_mode: math
require_exact: true
content: |-
  Complete the two answer slots.

  $$
  (x^2+6x+9)-2=(==x+3==)^2-==2==
  $$
feedback: |-
  Since $x^2+6x+9=(x+3)^2$, the expression is $(x+3)^2-2$.
```

## Runtime compatibility aliases

The installed runtime normalizes these older forms before applying strict schemas:

- Root prompt: `text` or `question` → `content`.
- Option text: `text`, `answer`, or `option` → `content`.
- Select-style question prompt: `text` or `question` → `content`.
- Select-style answer pointer: `correctOption`, `correct`, `correctId`, or `correct_option_id` → `correct_option`.
- Scalar options are converted to option objects, and missing option IDs default to option content.

Do not emit these aliases. They make validation, stable state, and later maintenance less reliable.

Radio and checkbox renderers show feedback after checking for correct options and for options the student selected. Feedback on an unselected incorrect option remains hidden. This does not weaken the authoring rule: write specific feedback for every option so any selected misconception receives a useful correction.

## Deterministic validation boundary

The bundled validator enforces canonical root fields, scalar types, required content, cardinality, correctness counts, ID uniqueness, answer references, blank markers, displayed feedback placement, and optional feedback-presence policy. The JSON schema in `schemas/quiz-block.schema.json` documents the same field surface and directly expressible authoring constraints; cross-field references and matching bijections remain procedural validator checks.

Neither mechanism can prove that feedback gives correct physical intuition or diagnoses the actual misconception. Apply `references/feedback-standard.md` and perform a content review.
